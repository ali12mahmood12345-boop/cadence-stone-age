"""V7.41: eight-founder qualified-learning feasibility confirmation."""
import argparse, json, platform, sys, warnings
from dataclasses import replace, asdict
from pathlib import Path
from importlib.metadata import version
import numpy as np
HERE=Path(__file__).resolve().parent
ref=HERE/'reference'
sys.path.insert(0,str(ref if ref.exists() else HERE.parent/'stone-age-v7-36'))
import stone_age_v7_36_position_convergence as v
original_compose=v.compose

def compose(seed):
    brain=original_compose(seed)
    brain.learner.config=replace(brain.learner.config,qualified=True,free_steps=4096,
        nudged_steps=4096,damping=3,initial_damping=1,tolerance=.003)
    return brain

def train(brain,episodes,state):
    out={'lessons':0,'runtime_errors':[],'qualified_lessons':0,'phase_max_residual':{k:0. for k in ('free','nudged','opposite')}}
    for ep in episodes:
        state['episode']=ep
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('error')
                v.hear(brain,ep)
                q=v.query_vector(ep)
                brain.recall.values[...]=0.
                report=brain.lesson(q,np.asarray([ep.label]))
                assert report['qualified']==1., report
                for phase in out['phase_max_residual']:
                    error=float(report[phase+'_residual'])
                    assert np.isfinite(error) and error<=.003, report
                    out['phase_max_residual'][phase]=max(out['phase_max_residual'][phase],error)
                brain.act(q,greedy=True)
            out['lessons']+=1
            out['qualified_lessons']+=1
            if out['lessons']%500==0:
                print(f'  stage progress: {out["lessons"]}/{len(episodes)}',flush=True)
        except Exception as exc:
            out['runtime_errors'].append(f'{type(exc).__name__}: {exc}')
            if hasattr(exc,'report'): out['failure_report']=exc.report
            break
    state['episode']=None
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--smoke',action='store_true'); args=ap.parse_args()
    assert version('cadence-net')=='0.91.1'
    v.LEARNING_FREE_STEPS=4096; v.compose=compose; v.train_stage=train
    if args.smoke:
        brain=compose(73636); state={'episode':None,'teacher_rows':0,'teacher_correct':0}
        v.install_exact_position_teacher(brain,state)
        result=train(brain,v._make_panel(73636,99,1),state)
        assert result['lessons']==22 and not result['runtime_errors'],result
        assert state['teacher_correct']==22
        assert v._address_map_max_abs(brain)==0 and np.max(np.abs(brain.recall.position_c))==0
        print('V7.41 smoke passed: 22 lessons; all three phases residual-qualified; maps frozen.',flush=True)
        return
    out=HERE/'v7_41_results'; out.mkdir(exist_ok=True)
    founders=[]; attention=[]; maps=[]
    meta={'experiment':'V7.41','python':sys.version,'numpy':np.__version__,'platform':platform.platform(),
          'cadence_net':version('cadence-net'),'learning':asdict(compose(102001).learner.config)}
    for seed in range(102001,102009):
        print(f'Founder {seed}: qualified learning, initial half dt',flush=True)
        fd,records,geometry=v.run_founder(seed)
        founders.append(fd); attention.extend(records); maps.extend(geometry)
        (out/f'founder_{seed}.json').write_text(json.dumps({'founder':fd,'attention':records,'maps':geometry},indent=2,default=str),encoding='utf-8')
        (out/'V7_41_RESULTS.json').write_text(json.dumps({**meta,'completed_founders':len(founders),
            'run_complete':len(founders)==8,'founders':founders,'analysis':v.summarize(founders,attention)},indent=2,default=str),encoding='utf-8')
        print(f'Founder {seed} finished: valid={fd["valid"]}',flush=True)
    print('Send back v7_41_results/V7_41_RESULTS.json and founder files.',flush=True)

if __name__=='__main__': main()

