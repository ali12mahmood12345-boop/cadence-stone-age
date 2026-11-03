"""V7.39: same-input free-solver trajectory and numerical dt probes."""
import hashlib, json, pickle, platform, sys, types
from pathlib import Path
from importlib.metadata import version
import numpy as np

HERE=Path(__file__).resolve().parent
EXPECTED='23cab22c6e3bebe8141bbb75fed351b26d340ddf8710e4ab89ab3a13b30635b9'

def restore_mapping(data):
    return types.MappingProxyType(data)

def vector(state):
    return np.concatenate([np.asarray(getattr(state,k)).ravel() for k in ('v','activation','adaptation')])

def main():
    assert version('cadence-net')=='0.91.1'
    data=(HERE/'snapshots/pre_free_4096.pkl').read_bytes()
    assert hashlib.sha256(data).hexdigest()==EXPECTED, 'Snapshot hash mismatch'
    out=HERE/'v7_39_results'
    out.mkdir(exist_ok=True)
    report={'experiment':'V7.39','python':sys.version,'numpy':np.__version__,
            'cadence_net':version('cadence-net'),'platform':platform.platform(),
            'snapshot_sha256':EXPECTED,'reference_residual':1.7105146077639979,'arms':[]}
    def save():
        (out/'V7_39_RESULTS.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    try:
        # The included, hash-checked snapshot is the user's V7.38 output.
        for factor,cap in ((1.,4096),(1.,16384),(.5,16384),(.25,16384),(.125,16384)):
            core,drive,warm=pickle.loads(data)
            base_dt=float(core.neuron_model.dt)
            if factor!=1.:
                core=core._with_dt(base_dt*factor)
            result=core.settle_batch(drive,steps=cap,state=warm,tolerance=.003)
            residual=float(np.max(np.abs(core.residual(drive,result))))
            arm={'dt_factor':factor,'dt':float(core.neuron_model.dt),'cap':cap,
                 'steps':int(result.steps),'residual':residual,'budget_exhausted':bool(result.steps>=cap),
                 'residual_below_0_003':bool(np.isfinite(residual) and residual<=.003),'tail':[]}
            # Record full-state one- and two-step differences, with stopping disabled.
            states=[vector(result)]
            for n in range(1,33):
                result=core.settle_batch(drive,steps=1,state=result,tolerance=None)
                value=vector(result)
                arm['tail'].append({'step_after_endpoint':n,
                    'residual':float(np.max(np.abs(core.residual(drive,result)))),
                    'state_delta_1':float(np.max(np.abs(value-states[-1]))),
                    'state_delta_2':None if len(states)<2 else float(np.max(np.abs(value-states[-2])))})
                states.append(value)
            np.savez_compressed(out/f'states_dt_{factor}_cap_{cap}.npz',states=np.array(states))
            report['arms'].append(arm)
            save()
            print(f'dt factor {factor}, cap {cap}: steps={arm["steps"]}, residual={residual:.12g}',flush=True)
        baseline=report['arms'][:2]
        report['baseline_reproduced']=all(a['steps']==a['cap'] and abs(a['residual']-report['reference_residual'])<1e-10 for a in baseline)
        report['status']='diagnostic_complete' if report['baseline_reproduced'] else 'baseline_mismatch_do_not_infer_repair'
    except Exception as exc:
        report['status']='error'
        report['error']=f'{type(exc).__name__}: {exc}'
        save()
        raise
    save()
    print('Results saved to '+str(out),flush=True)

if __name__=='__main__':
    main()

