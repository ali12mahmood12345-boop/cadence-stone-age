"""V7.38: replay founder 102007 and inspect the pre-update free solve."""
import argparse, copyreg, hashlib, json, pickle, platform, sys, types, warnings
from dataclasses import asdict
from importlib.metadata import version
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
reference = HERE / 'reference'
if not reference.exists():
    reference = HERE.parent / 'stone-age-v7-36'
sys.path.insert(0, str(reference))
import stone_age_v7_36_position_convergence as v

def restore_mapping(data):
    return types.MappingProxyType(data)

copyreg.pickle(types.MappingProxyType, lambda value: (restore_mapping, (dict(value),)))

class DiagnosticComplete(Exception):
    pass

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--smoke', action='store_true')
    args=ap.parse_args()
    assert version('cadence-net') == '0.91.1'
    target=1 if args.smoke else 7666
    out=HERE / ('smoke_results' if args.smoke else 'v7_38_results')
    out.mkdir(exist_ok=True)
    summary={'experiment':'V7.38','founder':102007,'target_lesson':target,
             'python':sys.version,'platform':platform.platform(),'numpy':np.__version__,
             'cadence_net':version('cadence-net'),'smoke':args.smoke,'arms':[]}
    for budget in (4096,16384):
        v.LEARNING_FREE_STEPS=budget
        brain=v.compose(102007)
        teacher={'episode':None,'teacher_rows':0,'teacher_correct':0}
        v.install_exact_position_teacher(brain,teacher)
        current={'lesson':0}
        arm={'training_budget':budget,'checkpoints':{},'status':'target_not_reached'}
        original=brain.learner.free
        def diagnostic(self,drive,warm=None):
            if current['lesson'] != target:
                return original(drive,warm)
            # Capture only the free solver's complete inputs before any lesson update.
            # All probes are disposable clones, never used for subsequent learning.
            snapshot=pickle.dumps((self.brain,drive,warm),protocol=pickle.HIGHEST_PROTOCOL)
            (out / f'pre_free_{budget}.pkl').write_bytes(snapshot)
            arm['snapshot_sha256']=hashlib.sha256(snapshot).hexdigest()
            arm['learner_config']=asdict(self.config)
            arm['probes']=[]
            for cap in (4096,16384,16384):
                core,x,start=pickle.loads(snapshot)
                result=core.settle_batch(x,steps=cap,state=start,tolerance=self.config.tolerance)
                residual=np.asarray(core.residual(x,result))
                arm['probes'].append({'budget':cap,'steps':int(result.steps),
                    'residual':residual.tolist(),'max_abs_residual':float(np.max(np.abs(residual))),
                    'finite':bool(np.isfinite(residual).all()),
                    'budget_exhausted':bool(result.steps>=cap)})
            arm['repeat_16384_exact']=arm['probes'][1]==arm['probes'][2]
            arm['status']='pre_update_diagnostic_complete'
            raise DiagnosticComplete('Diagnostic target reached; lesson intentionally not learned')
        brain.learner.free=types.MethodType(diagnostic,brain.learner)
        try:
            cumulative=0
            for stage,per_pair in enumerate(v.STAGE_PER_PAIR,1):
                for ep in v.make_stage(102007,stage,per_pair):
                    current['lesson']+=1
                    teacher['episode']=ep
                    v.hear(brain,ep)
                    q=v.query_vector(ep)
                    brain.recall.values[...]=0.0
                    with warnings.catch_warnings():
                        warnings.simplefilter('error')
                        brain.lesson(q,np.asarray([ep.label]))
                        brain.act(q,greedy=True)
                    if current['lesson']%500==0:
                        print(f'budget {budget}: {current["lesson"]} lessons complete',flush=True)
                cumulative+=per_pair
                teacher['episode']=None
                ck=f'D{cumulative}'
                result,_,_=v.evaluate_checkpoint(brain,102007,ck,v.make_cal(102007),v.make_test(102007))
                arm['checkpoints'][ck]=result
                if not result['valid']:
                    raise RuntimeError('Checkpoint invalid: '+ck)
        except DiagnosticComplete:
            pass
        except Exception as exc:
            arm['status']='replay_failed'
            arm['error']=f'{type(exc).__name__}: {exc}'
        arm['last_attempted_lesson']=current['lesson']
        if not args.smoke and 'D198' in arm['checkpoints']:
            observed=arm['checkpoints']['D198']['conditions']['BASE']['accuracy']
            arm['D198_matches_prior']=abs(observed-0.759090909090909)<1e-12
        summary['arms'].append(arm)
        (out/'V7_38_RESULTS.json').write_text(json.dumps(summary,indent=2,default=str),encoding='utf-8')
        print(f'budget {budget}: {arm["status"]}',flush=True)
    if args.smoke:
        assert all(a['status']=='pre_update_diagnostic_complete' and a['repeat_16384_exact'] for a in summary['arms'])
        print('V7.38 smoke test passed',flush=True)
    print('Results: '+str(out),flush=True)

if __name__=='__main__':
    main()

