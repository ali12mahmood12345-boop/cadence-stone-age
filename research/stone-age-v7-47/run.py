"""V7.47: 8-founder paired native position-rate 0.10 vs 0.20, EXACT control.
Run from repository checkout. See PROTOCOL.md for frozen controls.
"""
import argparse
import json
import platform
import statistics
import sys
import types
from pathlib import Path
from importlib.metadata import version

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'stone-age-v7-45'))
import qualified_reference as q

v=q.v
EXACT_INSTALL=v.install_exact_position_teacher
ARMS={'EXACT_010':.10,'NATIVE_010':.10,'NATIVE_020':.20}
CHECKPOINTS=('D198','D396','D792')
MODE='EXACT_010'

def install(brain,state):
    if MODE=='EXACT_010':
        EXACT_INSTALL(brain,state)
        return
    native=brain.recall._position_step
    def wrapped(self,*args,**kwargs):
        pcs=[q.np.asarray(m[1]).copy() for m in self.position_maps]
        result=native(*args,**kwargs)
        self.position_maps=[(m[0],pcs[i],m[2]) for i,m in enumerate(self.position_maps)]
        state['native_rows']=state.get('native_rows',0)+int(result[0])
        state['native_refused']=state.get('native_refused',0)+int(result[1])
        if result[1]:
            raise RuntimeError('Native position update refused')
        return result
    brain.recall._position_step=types.MethodType(wrapped,brain.recall)

def configure(arm):
    global MODE
    MODE=arm
    v.POSITION_RATE=ARMS[arm]
    v.LEARNING_FREE_STEPS=4096
    v.compose=q.compose
    v.train_stage=q.train
    v.install_exact_position_teacher=install

def verify(f,arm):
    if f.get('valid')!=1 or set(f.get('checkpoints',{}))!=set(CHECKPOINTS):
        return False
    if len(f.get('stages',[]))!=3 or sum(s['lessons'] for s in f['stages'])!=17424:
        return False
    for s in f['stages']:
        if s['runtime_errors'] or s['qualified_lessons']!=s['lessons'] or s['lessons']!=22*s['per_pair']:
            return False
        if max(s['phase_max_residual'].values())>.003:
            return False
    if f.get('address_map_max_abs',1)>1e-12 or f.get('position_c_max_abs',1)>1e-12:
        return False
    if arm=='EXACT_010':
        if f.get('teacher_rows',0)<=0 or f.get('teacher_accuracy')!=1:
            return False
    else:
        if f.get('teacher_rows')!=0 or f.get('teacher_accuracy') is not None:
            return False
    return all(f['checkpoints'][ck]['valid'] and f['checkpoints'][ck]['calibration']['valid'] and
       all(f['checkpoints'][ck]['conditions'][cond]['valid'] for cond in v.CONDS)
       for ck in CHECKPOINTS)

def aggregate(out,seeds):
    found={}
    for seed in seeds:
        for arm in ARMS:
            p=out/f'founder_{seed}_{arm}.json'
            if p.exists():
                obj=json.loads(p.read_text(encoding='utf-8'))
                assert obj['arm']==arm and obj['founder']['founder']==seed
                found[seed,arm]=obj['founder']
    pairs=[]
    for seed in seeds:
        if not all((seed,a) in found for a in ARMS):
            continue
        f={a:found[seed,a] for a in ARMS}
        ok=all(verify(f[a],a) for a in ARMS)
        row={'seed':seed,'all_valid':ok,'checkpoints':{}}
        if ok:
            for ck in CHECKPOINTS:
                vals={}
                for arm in ARMS:
                    c=f[arm]['checkpoints'][ck]
                    vals[arm]={
                        'base':c['conditions']['BASE']['accuracy'],
                        'oracle':c['conditions']['FORCE_PREDECESSOR']['accuracy'],
                        'force_target':c['conditions']['FORCE_TARGET']['accuracy'],
                        'map_top':c['map_geometry']['top_predecessor_rate'],
                        'map_mass':c['map_geometry']['mean_predecessor_mass']}
                vals['paired_base_gain']=vals['NATIVE_020']['base']-vals['NATIVE_010']['base']
                vals['paired_top_gain']=vals['NATIVE_020']['map_top']-vals['NATIVE_010']['map_top']
                row['checkpoints'][ck]=vals
        pairs.append(row)
    valid=[p for p in pairs if p['all_valid']]
    summary={'valid_triplets':len(valid),'checkpoints':{}}
    for ck in CHECKPOINTS:
        if not valid:
            continue
        xs=[p['checkpoints'][ck] for p in valid]
        summary['checkpoints'][ck]={
            'median_native_base_gain':statistics.median(x['paired_base_gain'] for x in xs),
            'median_native_map_top_gain':statistics.median(x['paired_top_gain'] for x in xs),
            **{a:{k:statistics.median(x[a][k] for x in xs)
               for k in ('base','oracle','map_top','map_mass')} for a in ARMS}}
    gates={'six_valid_triplets':len(valid)>=6}
    if 'D792' in summary['checkpoints']:
        ck=summary['checkpoints']['D792']
        exact=ck['EXACT_010']
        gates['exact_control']=exact['base']>=.90 and exact['oracle']>=.95 and exact['map_top']>=.95
        gates['native_oracle']=all(ck[a]['oracle']>=.95 for a in ('NATIVE_010','NATIVE_020'))
        gates['rate_effect']=ck['median_native_base_gain']>=.03 and ck['median_native_map_top_gain']>=1/22
    doc={'experiment':'V7.47','run_complete':len(seeds)==8 and len(found)==24,
         'requested_founders':len(seeds),'completed_arms':len(found),'expected_arms':24,
         'cadence_net':version('cadence-net'),'python':sys.version,
         'numpy':q.np.__version__,'platform':platform.platform(),
         'pairs':pairs,'summary':summary,'gates':gates}
    tmp=out/'V7_47_RESULTS.json.tmp'
    tmp.write_text(json.dumps(doc,indent=2,allow_nan=False),encoding='utf-8')
    tmp.replace(out/'V7_47_RESULTS.json')
    return doc

def smoke():
    for arm in ARMS:
        configure(arm)
        brain=q.compose(107001)
        assert abs(brain.recall.position_rate-ARMS[arm])<1e-12
        state={'episode':None,'teacher_rows':0,'teacher_correct':0}
        install(brain,state)
        result=q.train(brain,v._make_panel(107001,99,1),state)
        assert result['lessons']==22 and result['qualified_lessons']==22 and not result['runtime_errors'],result
        assert max(result['phase_max_residual'].values())<=.003
        assert v._address_map_max_abs(brain)<=1e-12
        assert q.np.max(q.np.abs(brain.recall.position_c))<=1e-12
        if arm=='EXACT_010':
            assert state['teacher_correct']==22
        else:
            assert state['teacher_rows']==0 and state.get('native_rows',0)>0 and not state.get('native_refused',0)
        print(arm,'smoke passed',flush=True)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--smoke',action='store_true')
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--limit',type=int,default=8)
    args=parser.parse_args()
    assert version('cadence-net')=='0.91.1'
    if args.smoke:
        smoke()
        return
    if args.limit not in range(1,9):
        parser.error('--limit must be 1..8')
    seeds=list(range(107001,107009))[:args.limit]
    out=HERE/'v7_47_results'
    out.mkdir(exist_ok=True)
    if not args.resume and any(out.glob('founder_*.json')):
        parser.error('Files exist; use --resume to skip completed arms')
    for seed in seeds:
        order=list(ARMS) if seed%2 else list(reversed(ARMS))
        for arm in order:
            path=out/f'founder_{seed}_{arm}.json'
            if path.exists():
                if args.resume:
                    print(seed,arm,'skipping saved arm',flush=True)
                    continue
                raise FileExistsError(path)
            configure(arm)
            print(seed,arm,'rate',ARMS[arm],flush=True)
            try:
                f,att,maps=v.run_founder(seed)
                if arm!='EXACT_010':
                    f['teacher_accuracy']=None
                    f['teacher_metric_note']='No exact position labels'
                f['position_rate']=ARMS[arm]
                f['valid']=int(verify(f,arm))
                obj={'arm':arm,'founder':f,'attention':att,'maps':maps}
            except Exception as exc:
                obj={'arm':arm,'founder':{'founder':seed,'valid':0,
                     'position_rate':ARMS[arm],'error':f'{type(exc).__name__}: {exc}'},
                     'attention':[],'maps':[]}
            tmp=path.with_suffix('.json.tmp')
            tmp.write_text(json.dumps(obj,indent=2,default=str,allow_nan=False),encoding='utf-8')
            tmp.replace(path)
            status=aggregate(out,seeds)
            print('saved',seed,arm,'valid=',obj['founder']['valid'],
                  'arms',status['completed_arms'],'/ 24',flush=True)
    print(json.dumps(aggregate(out,seeds)['summary'],indent=2))
    print('Upload V7_47_RESULTS.json and all founder_*.json files for independent audit.')

if __name__=='__main__':
    main()
