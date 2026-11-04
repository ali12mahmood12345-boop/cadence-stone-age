import os,subprocess,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def main():
    out=HERE/'v7_44_results'; out.mkdir(exist_ok=False)
    env=os.environ.copy()
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):env[k]='1'
    for label in ('old','new'):
        exe=HERE/f'.venv-{label}'/'Scripts/python.exe'
        subprocess.run([str(exe),str(HERE/'full.py'),'--seed','104001','--smoke','--out',str(out/f'smoke_{label}.json')],check=True,cwd=HERE,env=env)
    runs=[]
    def save():
        pairs=[]
        for seed in (104001,104002):
            group=[r for r in runs if r['seed']==seed]
            if len(group)!=2:continue
            old=next(r for r in group if r['version']=='0.91.1'); new=next(r for r in group if r['version']=='0.93.1')
            p={'seed':seed,'both_valid':old['valid'] and new['valid']}
            if p['both_valid']:
                p.update(founder_metrics_exact=old['founder']==new['founder'],trial_records_exact=old['attention']==new['attention'],map_records_exact=old['maps']==new['maps'],new_over_old_elapsed=new['elapsed_seconds']/old['elapsed_seconds'],checkpoints={})
                for ck in ('D198','D396','D792'):
                    x=old['founder']['checkpoints'][ck]; y=new['founder']['checkpoints'][ck]
                    p['checkpoints'][ck]={'old_BASE':x['conditions']['BASE']['accuracy'],'new_BASE':y['conditions']['BASE']['accuracy'],'BASE_delta':y['conditions']['BASE']['accuracy']-x['conditions']['BASE']['accuracy'],'old_oracle':x['conditions']['FORCE_PREDECESSOR']['accuracy'],'new_oracle':y['conditions']['FORCE_PREDECESSOR']['accuracy']}
            pairs.append(p)
        (out/'V7_44_RESULTS.json').write_text(json.dumps({'experiment':'V7.44','run_complete':len(runs)==4,'same_environment':len({(r['python'],r['numpy'],r['platform']) for r in runs})<=1,'pairs':pairs,'runs':[{k:v for k,v in r.items() if k not in ('attention','maps')} for r in runs]},indent=2),encoding='utf-8')
    for seed,order in ((104001,('old','new')),(104002,('new','old'))):
        for label in order:
            target=out/f'{seed}_{label}.json'; exe=HERE/f'.venv-{label}'/'Scripts/python.exe'
            print('Full-dose bridge:',seed,label,flush=True)
            subprocess.run([str(exe),str(HERE/'full.py'),'--seed',str(seed),'--out',str(target)],check=True,cwd=HERE,env=env)
            runs.append(json.loads(target.read_text()));save()
    print('Send back V7_44_RESULTS.json and the four founder-version JSON files.')
if __name__=='__main__':main()

