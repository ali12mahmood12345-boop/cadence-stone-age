import argparse,json,time,sys,platform
from pathlib import Path
from importlib.metadata import version
import bench
q=bench.q
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--seed',type=int,required=True); ap.add_argument('--out',required=True); ap.add_argument('--smoke',action='store_true'); a=ap.parse_args()
    actual=version('cadence-net'); assert actual in ('0.91.1','0.93.1')
    v=q.v; v.compose=bench.shared_compose; v.train_stage=q.train
    if a.smoke:
        v.STAGE_PER_PAIR=(1,); v.CHECKPOINTS=(1,); v.CAL_PER_PAIR=1; v.TEST_PER_PAIR=1
    report={'experiment':'V7.44','version':actual,'python':sys.version,'numpy':q.np.__version__,
        'platform':platform.platform(),'seed':a.seed,'smoke':a.smoke,'initial_damping':0}
    try:
        start=time.perf_counter(); f,attention,maps=v.run_founder(a.seed)
        report.update(elapsed_seconds=time.perf_counter()-start,founder=f,attention=attention,maps=maps,valid=bool(f['valid']))
    except Exception as exc:
        report.update(valid=False,error=f'{type(exc).__name__}: {exc}')
    Path(a.out).write_text(json.dumps(report,indent=2,default=str),encoding='utf-8')
    print(actual,a.seed,'valid=',report['valid'],report.get('error',''),flush=True)
    if a.smoke and not report['valid']: raise RuntimeError('Smoke failed')
if __name__=='__main__':main()

