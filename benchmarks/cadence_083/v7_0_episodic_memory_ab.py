import argparse,csv,json,statistics
from collections import Counter
from importlib.metadata import version as pkg_version
from pathlib import Path
import numpy as np
from cadence import Brain

ACTIONS=['GATHER_WOOD','GATHER_STONE','CRAFT_FIRE','WARM_UP','WAIT']
AIDX={a:i for i,a in enumerate(ACTIONS)}
EXPECTED=ACTIONS[:4]
STATES=['EMPTY','HAS_WOOD','HAS_MATERIALS','HAS_FIRE']
CHECKPOINTS=[10,20,40,60,80,120]
AMPLITUDE=0.5
DECAY=0.2
ROBUST=0.50
ARMS=[('MEMORY_OFF',False),('MEMORY_ON',True)]

def mean(xs): return statistics.fmean(xs) if xs else 0.0
def rarr(x): return np.asarray([float(x)],dtype=np.float64)
def darr(x): return np.asarray([bool(x)],dtype=bool)
def tarr(a): return np.asarray([AIDX[a]],dtype=np.int64)

def obs(w,s,f,warm=.35):
    return np.asarray([[warm,float(w>=1),float(s>=1),float(f),min(1.,w/2),min(1.,s/2),1.]],dtype=np.float64)

def canon(i):
    return [obs(0,0,False),obs(1,0,False),obs(1,1,False),obs(1,1,True)][i]

class Chamber:
    def __init__(self): self.reset()
    def reset(self):
        self.w=0; self.s=0; self.f=False; self.warm=.35; self.n=0; self.done=False; self.success=False
    def observation(self): return obs(self.w,self.s,self.f,self.warm)
    def oracle(self):
        if self.f:return 'WARM_UP'
        if self.w and self.s:return 'CRAFT_FIRE'
        if self.w:return 'GATHER_STONE'
        return 'GATHER_WOOD'
    def execute(self,a):
        exp=self.oracle(); ok=(a==exp)
        if ok:
            if a=='GATHER_WOOD':self.w=1
            elif a=='GATHER_STONE':self.s=1
            elif a=='CRAFT_FIRE':self.f=True
            elif a=='WARM_UP':self.warm=.9; self.success=True; self.done=True
        self.n+=1
        if not self.done and self.n>=10:self.done=True
        reward=(2.0 if self.success else -1.0) if self.done else 0.0
        return exp,ok,reward

def new_brain(seed,memory_choice):
    kw=dict(inputs=7,actions=5,modules=(48,24),seed=int(seed),arousal=True,
            efference_amplitude=AMPLITUDE,efference_decay=DECAY)
    if memory_choice: kw['memory_choice']=True
    return Brain.compose(**kw)

def decode(out):
    i=int(np.asarray(out).reshape(-1)[0]); return ACTIONS[max(0,min(4,i))]

def guided(n): return n%12<4

def train_block(brain,start,end,stream):
    rows=[]
    if stream is None:
        ch=Chamber(); action=decode(brain.step(ch.observation())); gd=0
    else:
        ch=stream['ch']; action=stream['action']; gd=stream['gd']
    for ep in range(start,end+1):
        while not ch.done:
            exp,ok,reward=ch.execute(action)
            is_guided=guided(gd)
            teacher=tarr(exp) if (is_guided and not ok and not ch.done) else None
            rows.append(dict(episode=ep,global_decision=gd,expected=exp,chosen=action,
                agreement=int(ok),guided=int(is_guided),teacher_used=int(teacher is not None),
                reward=reward,terminal=int(ch.done),success=int(ch.success if ch.done else False),
                decision_in_episode=ch.n))
            gd+=1
            if ch.done:
                nxt=Chamber()
                action=decode(brain.step(nxt.observation(),reward=rarr(reward),done=darr(True)))
                ch=nxt; break
            action=decode(brain.step(ch.observation(),reward=rarr(reward),done=darr(False),teacher=teacher))
    return rows,dict(ch=ch,action=action,gd=gd)

def clear_records(brain):
    if getattr(brain,'hippocampus',None) is not None: brain.hippocampus.clear()
    if getattr(brain,'context_memory',None) is not None: brain.context_memory.clear()

def load_eval(path,forget=False):
    b=Brain.load(path)
    if forget: clear_records(b)
    b.reset(); return b

def chain_sampled(path,n,forget=False):
    b=load_eval(path,forget); wins=0; att=[0]*4; cor=[0]*4; wrong=Counter()
    for _ in range(n):
        b.reset(); passed=True
        for st in range(4):
            att[st]+=1; a=decode(b.act(canon(st),greedy=False))
            if a==EXPECTED[st]: cor[st]+=1
            else: wrong[f'{STATES[st]}->{a}']+=1; passed=False; break
        wins+=int(passed)
    b.reset()
    return dict(episodes=n,successes=wins,success_rate=wins/n,
        conditional_stage_accuracy=[cor[i]/att[i] if att[i] else 0 for i in range(4)],
        first_wrong=dict(wrong))

def chain_greedy(path,forget=False):
    b=load_eval(path,forget); b.reset()
    acts=[decode(b.act(canon(i),greedy=True)) for i in range(4)]; b.reset()
    return dict(passed=int(acts==EXPECTED),actions=acts)

def independent_greedy(path,forget=False):
    answers=[]
    for st in range(4):
        b=load_eval(path,forget)
        a=decode(b.act(canon(st),greedy=True))
        answers.append(dict(stage=STATES[st],expected=EXPECTED[st],chosen=a,correct=int(a==EXPECTED[st])))
    return dict(answers=answers,correct_count=sum(x['correct'] for x in answers),
                all_four_correct=int(all(x['correct'] for x in answers)))

def classify(rate,gpass):
    if not gpass:return 'NO_LOCK'
    return 'ROBUST_LOCK' if rate>=ROBUST else 'GREEDY_ONLY'

def stats(rows):
    terms=[r for r in rows if r['terminal']]
    return dict(success_rate=mean([r['success'] for r in terms]) if terms else 0,
        mean_decisions=mean([r['decision_in_episode'] for r in terms]) if terms else 0,
        corrections=sum(r['teacher_used'] for r in rows),
        agreement_rate=mean([r['agreement'] for r in rows]) if rows else 0)

def write_csv(path,rows):
    if not rows:return
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--seed-start',type=int,default=13001)
    ap.add_argument('--seeds',type=int,default=50)
    ap.add_argument('--checkpoint-strict',type=int,default=200)
    ap.add_argument('--final-strict',type=int,default=1000)
    ap.add_argument('--output',default='v7_0_output')
    args=ap.parse_args()
    v=pkg_version('cadence-net')
    if v!='0.83.0': raise RuntimeError(f'V7.0 requires cadence-net 0.83.0, found {v}')
    out=Path(args.output).resolve(); out.mkdir(exist_ok=True)
    ck=out/'checkpoints'; ck.mkdir(exist_ok=True)
    print('\nCADENCE // STONE AGE V7.0 — 0.83 EPISODIC MEMORY A/B + ABLATION')
    print('fresh paired seeds:',f'{args.seed_start}..{args.seed_start+args.seeds-1}')
    print('checkpoints:',CHECKPOINTS,'\n')
    per=[]; training=[]; checkpoints=[]; stage_rows=[]
    for seed in range(args.seed_start,args.seed_start+args.seeds):
        print('--- SEED',seed,'---'); seed_item={'seed':seed,'arms':{}}
        for arm,mem in ARMS:
            b=new_brain(seed,mem); stream=None; prev=0; arm_item={'memory_choice':mem,'checkpoints':{}}
            genes=b.describe().get('genes',{})
            if abs(float(genes.get('efference_amplitude',-99))-AMPLITUDE)>1e-9: raise RuntimeError('amplitude mismatch')
            if abs(float(genes.get('efference_decay',-99))-DECAY)>1e-9: raise RuntimeError('decay mismatch')
            for cp in CHECKPOINTS:
                rows,stream=train_block(b,prev+1,cp,stream)
                for r in rows: training.append(dict(seed=seed,arm=arm,memory_choice=int(mem),**r))
                path=ck/f'seed_{seed}_{arm}_ep_{cp}.npz'; b.save(path)
                n=args.final_strict if cp==120 else args.checkpoint_strict
                sampled=chain_sampled(path,n); greedy_eval=chain_greedy(path); indep=independent_greedy(path)
                label=classify(sampled['success_rate'],bool(greedy_eval['passed'])); bs=stats(rows)
                res=dict(classification=label,strict_sampled=sampled,strict_greedy=greedy_eval,
                         independent_stage_greedy=indep,training_block=bs)
                if mem:
                    fs=chain_sampled(path,n,True); fg=chain_greedy(path,True); fi=independent_greedy(path,True)
                    res['memory_cleared']=dict(classification=classify(fs['success_rate'],bool(fg['passed'])),
                                               strict_sampled=fs,strict_greedy=fg,independent_stage_greedy=fi)
                arm_item['checkpoints'][str(cp)]=res
                row=dict(seed=seed,arm=arm,memory_choice=int(mem),checkpoint=cp,classification=label,
                    robust_lock=int(label=='ROBUST_LOCK'),greedy_chain_pass=int(greedy_eval['passed']),
                    strict_sampled_percent=sampled['success_rate']*100,independent_all_four=indep['all_four_correct'],
                    independent_correct_count=indep['correct_count'],training_success_percent=bs['success_rate']*100,
                    memory_cleared_strict_percent='',memory_cleared_greedy_chain_pass='',memory_cleared_independent_all_four='')
                if mem:
                    m=res['memory_cleared']; row['memory_cleared_strict_percent']=m['strict_sampled']['success_rate']*100
                    row['memory_cleared_greedy_chain_pass']=m['strict_greedy']['passed']
                    row['memory_cleared_independent_all_four']=m['independent_stage_greedy']['all_four_correct']
                checkpoints.append(row)
                for st,a in enumerate(indep['answers']): stage_rows.append(dict(seed=seed,arm=arm,checkpoint=cp,memory_state='INTACT',stage_index=st,**a))
                if mem:
                    for st,a in enumerate(res['memory_cleared']['independent_stage_greedy']['answers']):
                        stage_rows.append(dict(seed=seed,arm=arm,checkpoint=cp,memory_state='CLEARED',stage_index=st,**a))
                    print(f"  {arm:<10} ep {cp:>3}: {label:<12} strict={sampled['success_rate']*100:6.2f}% independent={indep['correct_count']}/4 cleared={res['memory_cleared']['strict_sampled']['success_rate']*100:6.2f}%")
                else:
                    print(f"  {arm:<10} ep {cp:>3}: {label:<12} strict={sampled['success_rate']*100:6.2f}% independent={indep['correct_count']}/4")
                prev=cp
            seed_item['arms'][arm]=arm_item
        per.append(seed_item); print()
    write_csv(out/'V7_0_TRAINING.csv',training); write_csv(out/'V7_0_CHECKPOINTS.csv',checkpoints); write_csv(out/'V7_0_INDEPENDENT_STAGES.csv',stage_rows)
    agg={}; paired={}
    for cp in CHECKPOINTS:
        key=str(cp); agg[key]={}
        for arm,mem in ARMS:
            vals=[x['arms'][arm]['checkpoints'][key] for x in per]; labels=[x['classification'] for x in vals]
            rates=[x['strict_sampled']['success_rate'] for x in vals]
            stages=[mean([x['independent_stage_greedy']['answers'][s]['correct'] for x in vals]) for s in range(4)]
            e=dict(robust_lock_count=labels.count('ROBUST_LOCK'),greedy_only_count=labels.count('GREEDY_ONLY'),
                no_lock_count=labels.count('NO_LOCK'),greedy_chain_pass_count=sum(x['strict_greedy']['passed'] for x in vals),
                mean_strict_sampled=mean(rates),median_strict_sampled=statistics.median(rates),
                independent_stage_accuracy=stages,independent_all_four_count=sum(x['independent_stage_greedy']['all_four_correct'] for x in vals))
            if mem:
                fv=[x['memory_cleared'] for x in vals]; fr=[x['strict_sampled']['success_rate'] for x in fv]
                e['memory_cleared']=dict(robust_lock_count=sum(classify(x['strict_sampled']['success_rate'],bool(x['strict_greedy']['passed']))=='ROBUST_LOCK' for x in fv),
                    greedy_chain_pass_count=sum(x['strict_greedy']['passed'] for x in fv),mean_strict_sampled=mean(fr),
                    median_strict_sampled=statistics.median(fr),
                    independent_stage_accuracy=[mean([x['independent_stage_greedy']['answers'][s]['correct'] for x in fv]) for s in range(4)],
                    independent_all_four_count=sum(x['independent_stage_greedy']['all_four_correct'] for x in fv))
            agg[key][arm]=e
        on=off=ties=0
        for x in per:
            a=x['arms']['MEMORY_OFF']['checkpoints'][key]['strict_sampled']['success_rate']; b=x['arms']['MEMORY_ON']['checkpoints'][key]['strict_sampled']['success_rate']
            if b>a:on+=1
            elif a>b:off+=1
            else:ties+=1
        paired[key]={'MEMORY_ON_wins':on,'MEMORY_OFF_wins':off,'ties':ties}
    payload=dict(cadence_net_version=v,protocol=dict(seed_start=args.seed_start,seeds=args.seeds,checkpoints=CHECKPOINTS,
        efference_amplitude=AMPLITUDE,efference_decay=DECAY,memory_on_defaults=True,evaluation_on_saved_clones=True,
        memory_ablation='clear hippocampus and context_memory on evaluation clone'),aggregate=agg,paired_strict_wins=paired,per_seed=per)
    (out/'V7_0_RESULTS.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    lines=[]; add=lines.append
    add('CADENCE // STONE AGE V7.0 — 0.83 EPISODIC MEMORY A/B + ABLATION'); add('='*96); add(f'cadence-net: {v}')
    add(f'Fresh paired seeds: {args.seed_start}..{args.seed_start+args.seeds-1}'); add('Frozen efference: amplitude=0.5, decay=0.2'); add('')
    add('FULL-CHAIN STRICT TRAJECTORY'); add('episode   OFF robust   ON robust   OFF mean strict   ON mean strict   ON-cleared mean strict')
    for cp in CHECKPOINTS:
        off=agg[str(cp)]['MEMORY_OFF']; on=agg[str(cp)]['MEMORY_ON']; cl=on['memory_cleared']
        add(f"{cp:>7}   {off['robust_lock_count']:>3}/{args.seeds:<3}      {on['robust_lock_count']:>3}/{args.seeds:<3}      {off['mean_strict_sampled']*100:8.3f}%        {on['mean_strict_sampled']*100:8.3f}%        {cl['mean_strict_sampled']*100:8.3f}%")
    add(''); add('INDEPENDENT PER-STATE GREEDY ACCURACY')
    def fmt(s): return f"WOOD={s[0]*100:5.1f}% STONE={s[1]*100:5.1f}% FIRE={s[2]*100:5.1f}% WARM={s[3]*100:5.1f}%"
    for cp in CHECKPOINTS:
        off=agg[str(cp)]['MEMORY_OFF']; on=agg[str(cp)]['MEMORY_ON']; cl=on['memory_cleared']
        add(f"  ep {cp:>3} OFF      {fmt(off['independent_stage_accuracy'])}"); add(f"         ON       {fmt(on['independent_stage_accuracy'])}"); add(f"         ON-CLEAR {fmt(cl['independent_stage_accuracy'])}")
    add(''); add('ALL FOUR INDEPENDENT GREEDY ANSWERS CORRECT')
    for cp in CHECKPOINTS:
        off=agg[str(cp)]['MEMORY_OFF']; on=agg[str(cp)]['MEMORY_ON']; cl=on['memory_cleared']
        add(f"  ep {cp:>3}: OFF={off['independent_all_four_count']}/{args.seeds} | ON={on['independent_all_four_count']}/{args.seeds} | ON-CLEAR={cl['independent_all_four_count']}/{args.seeds}")
    add(''); add('PAIRED FULL-CHAIN STRICT WINS')
    for cp in CHECKPOINTS:
        p=paired[str(cp)]; add(f"  ep {cp:>3}: MEMORY_ON wins={p['MEMORY_ON_wins']} | MEMORY_OFF wins={p['MEMORY_OFF_wins']} | ties={p['ties']}")
    add(''); add('FINAL EP120 SUMMARY'); off=agg['120']['MEMORY_OFF']; on=agg['120']['MEMORY_ON']; cl=on['memory_cleared']
    add(f"  MEMORY_OFF robust: {off['robust_lock_count']}/{args.seeds}, mean strict={off['mean_strict_sampled']*100:.3f}%")
    add(f"  MEMORY_ON robust:  {on['robust_lock_count']}/{args.seeds}, mean strict={on['mean_strict_sampled']*100:.3f}%")
    add(f"  ON after memory clear: robust={cl['robust_lock_count']}/{args.seeds}, mean strict={cl['mean_strict_sampled']*100:.3f}%")
    add(f"  independent all-four: OFF={off['independent_all_four_count']}/{args.seeds}, ON={on['independent_all_four_count']}/{args.seeds}, ON-CLEAR={cl['independent_all_four_count']}/{args.seeds}")
    add(''); add('INTERPRETATION GUIDE'); add('1. ON >> OFF early means episodic memory accelerates acquisition.'); add('2. High independent-state accuracy means the gain is not only in-attempt search.'); add('3. A large ON -> ON-CLEAR drop means episodic records still carry substantial choice information.'); add('4. ON-CLEAR approaching ON over training is consistent with greater slow-policy consolidation.'); add('5. This fully observed chain does not isolate temporal context from place memory; use an ambiguous-state test later.')
    text='\n'.join(lines); (out/'V7_0_REPORT.txt').write_text(text,encoding='utf-8'); print('\n'+text)

if __name__=='__main__': main()
