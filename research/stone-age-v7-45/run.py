"""V7.45: paired exact versus native position-target acquisition."""
import argparse,json,sys,types,platform
from pathlib import Path
from importlib.metadata import version
import qualified_reference as q
v=q.v
exact_installer=v.install_exact_position_teacher
MODE='EXACT'

def install(brain,state):
    if MODE=='EXACT':
        exact_installer(brain,state); return
    native=brain.recall._position_step
    def frozen_pc(self,*args,**kwargs):
        saved=[q.np.asarray(m[1]).copy() for m in self.position_maps]
        result=native(*args,**kwargs)
        self.position_maps=[(m[0],saved[i],m[2]) for i,m in enumerate(self.position_maps)]
        state['native_rows']=state.get('native_rows',0)+int(result[0])
        state['native_refused']=state.get('native_refused',0)+int(result[1])
        if result[1]: raise RuntimeError('Native position update refused')
        return result
    brain.recall._position_step=types.MethodType(frozen_pc,brain.recall)

def main():
    global MODE
    ap=argparse.ArgumentParser(); ap.add_argument('--smoke',action='store_true'); a=ap.parse_args()
    assert version('cadence-net')=='0.91.1'
    v.LEARNING_FREE_STEPS=4096; v.compose=q.compose; v.train_stage=q.train; v.install_exact_position_teacher=install
    if a.smoke:
        for MODE in ('EXACT','NATIVE'):
            brain=q.compose(105001); state={'episode':None,'teacher_rows':0,'teacher_correct':0}
            install(brain,state)
            tr=q.train(brain,v._make_panel(105001,99,1),state)
            assert tr['lessons']==22 and not tr['runtime_errors'],tr
            assert v._address_map_max_abs(brain)==0 and q.np.max(q.np.abs(brain.recall.position_c))==0
            if MODE=='EXACT':assert state['teacher_correct']==22
            else:assert state['teacher_rows']==0 and state.get('native_rows',0)>0 and state.get('native_refused',0)==0
            print(MODE,'smoke passed',flush=True)
        return
    out=Path(__file__).resolve().parent/'v7_45_results';out.mkdir(exist_ok=False)
    runs=[]
    def save():
        pairs=[]
        for seed in range(105001,105009):
            group=[r for r in runs if r['founder']['founder']==seed]
            if len(group)!=2:continue
            x=next(r['founder'] for r in group if r['arm']=='EXACT');n=next(r['founder'] for r in group if r['arm']=='NATIVE')
            pair={'seed':seed,'both_valid':bool(x['valid'] and n['valid']),'checkpoints':{}}
            for ck in ('D198','D396','D792'):
                if ck not in x['checkpoints'] or ck not in n['checkpoints']:continue
                e=x['checkpoints'][ck]; b=n['checkpoints'][ck]
                pair['checkpoints'][ck]={'exact_BASE':e['conditions']['BASE']['accuracy'],'native_BASE':b['conditions']['BASE']['accuracy'],
                    'native_minus_exact':b['conditions']['BASE']['accuracy']-e['conditions']['BASE']['accuracy'],
                    'exact_oracle':e['conditions']['FORCE_PREDECESSOR']['accuracy'],'native_oracle':b['conditions']['FORCE_PREDECESSOR']['accuracy'],
                    'exact_map_top':e['map_geometry']['top_predecessor_rate'],'native_map_top':b['map_geometry']['top_predecessor_rate']}
            pairs.append(pair)
        (out/'V7_45_RESULTS.json').write_text(json.dumps({'experiment':'V7.45','run_complete':len(runs)==16,'python':sys.version,'numpy':q.np.__version__,
            'cadence_net':version('cadence-net'),'platform':platform.platform(),'runs':runs,'pairs':pairs},indent=2,default=str),encoding='utf-8')
    for seed in range(105001,105009):
        order=('EXACT','NATIVE') if seed%2 else ('NATIVE','EXACT')
        for MODE in order:
            print(seed,MODE,flush=True)
            f,attention,maps=v.run_founder(seed)
            if MODE=='NATIVE':f['teacher_accuracy']=None;f['teacher_metric_note']='No exact teacher; native targets not scored against oracle'
            data={'arm':MODE,'founder':f,'attention':attention,'maps':maps}
            (out/f'founder_{seed}_{MODE}.json').write_text(json.dumps(data,indent=2,default=str),encoding='utf-8')
            runs.append({'arm':MODE,'founder':f});save()
    print('Send back V7_45_RESULTS.json and the founder arm files.')
if __name__=='__main__':main()

