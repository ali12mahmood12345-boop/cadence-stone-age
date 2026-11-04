import json,os,subprocess,statistics
from pathlib import Path
HERE=Path(__file__).resolve().parent
def main():
    out=HERE/'v7_43_results'; out.mkdir(exist_ok=False)
    results=[]
    env=os.environ.copy()
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'): env[k]='1'
    for seed in (104001,104002):
        for repeat in (1,2):
            order=('old','new') if repeat==1 else ('new','old')
            for label in order:
                target=out/f'{seed}_{repeat}_{label}.json'
                exe=HERE/f'.venv-{label}'/'Scripts/python.exe'
                subprocess.run([str(exe),str(HERE/'bench.py'),'--seed',str(seed),'--out',str(target)],check=True,env=env,cwd=HERE)
                r=json.loads(target.read_text()); r['repeat']=repeat; results.append(r)
                (out/'V7_43_RESULTS.json').write_text(json.dumps({'experiment':'V7.43','run_complete':False,'runs':results},indent=2))
    valid=all(r['valid'] for r in results)
    same_env=len({(r['python'],r['numpy'],r['platform']) for r in results})==1
    pairs=[]
    if valid:
        for seed in (104001,104002):
            for repeat in (1,2):
                a=next(r for r in results if r['seed']==seed and r['repeat']==repeat and r['version']=='0.91.1')
                b=next(r for r in results if r['seed']==seed and r['repeat']==repeat and r['version']=='0.93.1')
                pairs.append({'seed':seed,'repeat':repeat,'conditions_exact':a['conditions']==b['conditions'],
                    'trial_records_exact':a['trial_records']==b['trial_records'],'map_records_exact':a['map_records']==b['map_records'],
                    'training_report_exact':a['training']==b['training'],'new_over_old_training_time':b['training_seconds']/a['training_seconds'],
                    'new_over_old_evaluation_time':b['evaluation_seconds']/a['evaluation_seconds']})
    (out/'V7_43_RESULTS.json').write_text(json.dumps({'experiment':'V7.43','run_complete':True,'all_runs_valid':valid,
        'same_environment':same_env,'pairs':pairs,'runs':results,'scope':'short compatibility pilot; no full-dose migration claim'},indent=2))
    print('Send back v7_43_results/V7_43_RESULTS.json')
if __name__=='__main__':main()

