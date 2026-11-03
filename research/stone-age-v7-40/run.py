"""V7.40: released residual-qualified free-solver confirmation on saved input."""
import hashlib, json, pickle, platform, sys, types, warnings
from pathlib import Path
from importlib.metadata import version
import numpy as np

HERE=Path(__file__).resolve().parent
EXPECTED='23cab22c6e3bebe8141bbb75fed351b26d340ddf8710e4ab89ab3a13b30635b9'
TOLERANCE=.003

def restore_mapping(data):
    return types.MappingProxyType(data)

def main():
    assert version('cadence-net')=='0.91.1'
    data=(HERE/'snapshots/pre_free_4096.pkl').read_bytes()
    assert hashlib.sha256(data).hexdigest()==EXPECTED, 'Snapshot hash mismatch'
    out=HERE/'v7_40_results'
    out.mkdir(exist_ok=True)
    report={'experiment':'V7.40','scope':'one saved free solve; no training updates',
            'python':sys.version,'numpy':np.__version__,'cadence_net':version('cadence-net'),
            'platform':platform.platform(),'snapshot_sha256':EXPECTED,'tolerance':TOLERANCE,
            'baseline':[],'arms':[]}
    def save():
        (out/'V7_40_RESULTS.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error')
            for cap in (4096,16384):
                core,x,warm=pickle.loads(data)
                state=core.settle_batch(x,steps=cap,state=warm,tolerance=TOLERANCE)
                error=float(np.max(np.abs(core.residual(x,state))))
                report['baseline'].append({'cap':cap,'steps':int(state.steps),'residual':error})
            report['baseline_reproduced']=all(b['steps']==b['cap'] and abs(b['residual']-1.7105146077639979)<1e-10 for b in report['baseline'])
            if not report['baseline_reproduced']:
                report['status']='baseline_mismatch'; save(); return
            for cap in (4096,16384):
                for name,damping,initial in [('QUALIFIED_NO_DAMPING',0,0),('QUALIFIED_ADAPTIVE',3,0),('QUALIFIED_START_HALF_DT',3,1)]:
                    for repeat in (1,2):
                        core,x,warm=pickle.loads(data)
                        phase=core.equilibrate(x,state=warm,budget=cap,chunk=32,tolerance=TOLERANCE,damping=damping,initial_damping=initial)
                        residual=np.asarray(core.residual(x,phase.state))
                        finite=bool(all(np.isfinite(getattr(phase.state,k)).all() for k in ('v','activation','adaptation')) and np.isfinite(residual).all())
                        checked=bool(finite and np.all(residual<=TOLERANCE))
                        row={'name':name,'cap':cap,'repeat':repeat,'damping':damping,'initial_damping':initial,
                             'steps':int(phase.steps),'residual_checks':int(phase.residual_checks),
                             'stagnation_checks':int(phase.stagnation_checks),'final_damping_halvings':int(phase.damping_halvings),
                             'reported_qualified':bool(np.all(phase.qualified)),'independently_verified_qualified':checked,
                             'residual':residual.tolist(),'finite':finite}
                        assert row['reported_qualified']==checked
                        assert row['steps']<=cap
                        report['arms'].append(row)
                        np.savez_compressed(out/f'{name}_{cap}_{repeat}.npz',v=phase.state.v,activation=phase.state.activation,adaptation=phase.state.adaptation)
                        save()
                        print(f'{name}, cap {cap}, repeat {repeat}: qualified={checked}, steps={phase.steps}, residual={float(residual.max()):.12g}',flush=True)
            pairs=[report['arms'][i:i+2] for i in range(0,len(report['arms']),2)]
            report['repeat_metrics_exact']=all({k:v for k,v in a.items() if k!='repeat'}=={k:v for k,v in b.items() if k!='repeat'} for a,b in pairs)
            report['status']='diagnostic_complete'
    except Exception as exc:
        report['status']='error'; report['error']=f'{type(exc).__name__}: {exc}'; save(); raise
    save()
    print('Send back '+str(out/'V7_40_RESULTS.json'),flush=True)

if __name__=='__main__':
    main()

