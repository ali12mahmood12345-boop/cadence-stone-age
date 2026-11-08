"""V7.49: fixed evaluation-only position-logit gain 1 vs 2."""
import argparse
import importlib.util
import json
import math
import platform
import sys
from pathlib import Path
from statistics import median
from importlib.metadata import version

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v748',HERE.parent/'stone-age-v7-48'/'run.py')
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
v=r.v; np=r.q.np
ORIGINAL_EVAL=v.evaluate_checkpoint
EXTRA={}

def evaluate(brain, founder, checkpoint, cal, test):
    original=[tuple(np.asarray(a).copy() for a in m) for m in brain.recall.position_maps]
    baseline=ORIGINAL_EVAL(brain,founder,checkpoint,cal,test)
    try:
        brain.recall.position_maps=[tuple(2*a for a in m) for m in original]
        sharp=ORIGINAL_EVAL(brain,founder,checkpoint,cal,test)
    finally:
        brain.recall.position_maps=[tuple(a.copy() for a in m) for m in original]
    repeated=ORIGINAL_EVAL(brain,founder,checkpoint,cal,test)
    assert baseline==repeated, 'Restored baseline changed'
    assert baseline[0]['valid'] and sharp[0]['valid']
    assert all(np.array_equal(a,b) for m,n in zip(original,brain.recall.position_maps) for a,b in zip(m,n))
    EXTRA[checkpoint]={'gain2':sharp[0],'attention':sharp[1],'maps':sharp[2],'baseline_repeat_identical':True}
    return baseline

def save(path,obj):
    tmp=path.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj,indent=2,allow_nan=False),encoding='utf-8'); tmp.replace(path)

def summarize(out):
    docs=[json.loads(p.read_text()) for p in sorted(out.glob('founder_*.json'))]
    valid=[d for d in docs if d['valid']]
    summary={'experiment':'V7.49','complete':len(docs)==8,'completed_founders':len(docs),'valid_founders':len(valid),'cadence_net':version('cadence-net'),'numpy':np.__version__,'python':sys.version,'platform':platform.platform(),'checkpoints':{}}
    for ck in r.CHECKPOINTS:
        if not valid: continue
        pairs=[{'founder':d['founder']['founder'],'gain1':d['founder']['checkpoints'][ck]['conditions']['BASE']['accuracy'],'gain2':d['intervention'][ck]['gain2']['conditions']['BASE']['accuracy']} for d in valid]
        for p in pairs: p['paired_gain']=p['gain2']-p['gain1']
        summary['checkpoints'][ck]={'pairs':pairs,'median_gain1':median(p['gain1'] for p in pairs),'median_gain2':median(p['gain2'] for p in pairs),'median_paired_gain':median(p['paired_gain'] for p in pairs),'positive_founders':sum(p['paired_gain']>0 for p in pairs)}
    controls=bool(valid)
    if valid:
        for gain in (1,2):
            checkpoints=[d['founder']['checkpoints']['D792'] if gain==1 else d['intervention']['D792']['gain2'] for d in valid]
            controls &= median(c['conditions']['FORCE_PREDECESSOR']['accuracy'] for c in checkpoints)>=.95
            controls &= median(c['conditions']['FORCE_TARGET']['accuracy'] for c in checkpoints)<=.20
    eligible=len(valid)==8 and controls
    d=summary['checkpoints'].get('D792',{})
    summary['decision']='RUNNING' if len(docs)<8 else ('INCONCLUSIVE' if not eligible else ('PROMISING' if d['median_paired_gain']>=.02 and d['positive_founders']>=6 else 'NO SUPPORT'))
    summary['controls_pass']=controls
    save(out/'V7_49_RESULTS.json',summary)
    return summary

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--smoke',action='store_true'); ap.add_argument('--resume',action='store_true'); args=ap.parse_args()
    assert version('cadence-net')=='0.91.1'
    r.configure('NATIVE_020'); v.evaluate_checkpoint=evaluate
    if args.smoke:
        brain=r.q.compose(109999); state={'episode':None,'teacher_rows':0,'teacher_correct':0}; r.install(brain,state)
        stage=r.q.train(brain,v._make_panel(109999,99,1),state)
        assert stage['qualified_lessons']==22 and not stage['runtime_errors']
        panel=v._make_panel(109999,98,1)
        evaluate(brain,109999,'SMOKE',panel,panel)
        assert EXTRA['SMOKE']['baseline_repeat_identical']
        assert any(abs(a['predecessor_weight']-b['predecessor_weight'])>1e-8 for a,b in zip(ORIGINAL_EVAL(brain,109999,'SMOKE',panel,panel)[1],EXTRA['SMOKE']['attention']))
        print('V7.49 smoke passed: 22 qualified lessons; sharpening changes attention; baseline restored exactly.',flush=True); return
    out=HERE/'v7_49_results'; out.mkdir(exist_ok=True)
    for seed in range(109001,109009):
        path=out/f'founder_{seed}.json'
        if path.exists():
            if args.resume:
                saved=json.loads(path.read_text()); assert saved['valid'] and saved['founder']['founder']==seed
                continue
            raise FileExistsError(path)
        EXTRA.clear(); print('V7.49 founder',seed,'NATIVE_020 training; evaluation gains 1 and 2',flush=True)
        try:
            f,att,maps=v.run_founder(seed); f['teacher_accuracy']=None; f['position_rate']=.2
            ok=r.verify(f,'NATIVE_020') and set(EXTRA)==set(r.CHECKPOINTS)
            ok=ok and all(math.isfinite(x) and 0<=x<=.003 for s in f['stages'] for x in s['phase_max_residual'].values())
            doc={'valid':bool(ok),'founder':f,'attention':att,'maps':maps,'intervention':dict(EXTRA)}
        except Exception as exc:
            doc={'valid':False,'founder':{'founder':seed},'error':f'{type(exc).__name__}: {exc}'}
        save(path,doc); result=summarize(out)
        print('Saved',seed,'valid',doc['valid'],'completed',result['completed_founders'],'/8',flush=True)
        if not doc['valid']: raise RuntimeError('Founder invalid; stopped for inspection')
    print(json.dumps(summarize(out),indent=2),flush=True)

if __name__=='__main__': main()

