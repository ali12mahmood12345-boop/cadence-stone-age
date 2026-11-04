import argparse,json,time,sys,platform
from pathlib import Path
from importlib.metadata import version
import qualified_reference as q
from dataclasses import replace,fields
import types
original_teacher=q.v.install_exact_position_teacher

def install_teacher(brain,state):
    original_teacher(brain,state)
    if version('cadence-net')=='0.93.1':
        old_step=brain.recall._position_step
        def adapted(self,rows,head,found):
            # Same eight-item found tuple; only the caller signature changed.
            return old_step(None,rows,None,None,head,found=found)
        brain.recall._position_step=types.MethodType(adapted,brain.recall)

q.v.install_exact_position_teacher=install_teacher

def shared_compose(seed):
    brain=q.original_compose(seed)
    options=dict(qualified=True,free_steps=4096,nudged_steps=4096,damping=3,tolerance=.003)
    if 'initial_damping' in {f.name for f in fields(brain.learner.config)}:
        options['initial_damping']=0
    brain.learner.config=replace(brain.learner.config,**options)
    if version('cadence-net')=='0.93.1' and not hasattr(type(brain.recall),'attended'):
        type(brain.recall).attended=property(lambda self:self._attended)
    if version('cadence-net')=='0.93.1' and not hasattr(type(brain.recall),'position_c'):
        type(brain.recall).position_c=property(lambda self:self.position_map(0)[1])
    return brain

q.compose=shared_compose

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--seed',type=int,default=104001); ap.add_argument('--dose',type=int,default=22); ap.add_argument('--out',required=True); args=ap.parse_args()
    actual=version('cadence-net'); assert actual in ('0.91.1','0.93.1')
    v=q.v
    result={'version':actual,'numpy':q.np.__version__,'python':sys.version,'platform':platform.platform(),'seed':args.seed,'dose':args.dose,'valid':False}
    try:
        # Warm up separately; exclude imports, setup and warmup from timing.
        warm=q.compose(999001); state={'episode':None,'teacher_rows':0,'teacher_correct':0}
        v.install_exact_position_teacher(warm,state)
        check=q.train(warm,v._make_panel(999001,99,1),state)
        assert not check['runtime_errors'],check
        brain=q.compose(args.seed); state={'episode':None,'teacher_rows':0,'teacher_correct':0}
        v.install_exact_position_teacher(brain,state)
        episodes=v.make_stage(args.seed,1,args.dose)
        start=time.perf_counter(); training=q.train(brain,episodes,state); elapsed=time.perf_counter()-start
        result.update(training=training,training_seconds=elapsed)
        assert training['lessons']==len(episodes) and not training['runtime_errors'],training
        panel=v._make_panel(args.seed,30,2)
        result['conditions']={}; result['trial_records']={}
        start=time.perf_counter()
        for cond in v.CONDS:
            metrics,records=v.eval_condition(brain,panel,cond,'PILOT',panel='TEST')
            assert metrics['valid']==1,metrics
            result['conditions'][cond]=metrics; result['trial_records'][cond]=records
        result['evaluation_seconds']=time.perf_counter()-start
        result['map_geometry'],result['map_records']=v.position_map_geometry(brain,'PILOT')
        result['teacher_accuracy']=state['teacher_correct']/state['teacher_rows']
        assert result['teacher_accuracy']==1 and v._address_map_max_abs(brain)==0 and q.np.max(q.np.abs(brain.recall.position_c))==0
        result['valid']=True
    except Exception as exc:
        result['error']=f'{type(exc).__name__}: {exc}'
    Path(args.out).write_text(json.dumps(result,indent=2,default=str),encoding='utf-8')
    print(actual,'valid=',result['valid'],result.get('error',''),flush=True)

if __name__=='__main__':main()

