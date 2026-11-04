"""Continue at founder boundaries using the five audited V7.42 results."""
import json, sys, platform, hashlib
from pathlib import Path
from importlib.metadata import version
import run as base

HERE=Path(__file__).resolve().parent

def main():
    assert version('cadence-net')=='0.91.1'
    v=base.v; v.LEARNING_FREE_STEPS=4096; v.compose=base.compose; v.train_stage=base.train
    src=HERE/'completed'
    manifest=json.loads((src/'SHA256.json').read_text())
    for name,digest in manifest.items():
        assert hashlib.sha256((src/name).read_bytes()).hexdigest()==digest, name
    old=json.loads((src/'V7_42_RESULTS.json').read_text())
    assert old['completed_founders']==5 and not old['run_complete']
    founders=[]; records=[]
    out=HERE/'v7_42_results'
    if out.exists(): raise RuntimeError('Output folder already exists; preserve it before another run.')
    # Validate all bundled founders before creating output or starting work.
    for seed in range(103001,103006):
        data=json.loads((src/f'founder_{seed}.json').read_text())
        fd=data['founder']
        assert fd==old['founders'][seed-103001] and fd['founder']==seed and fd['valid']==1
        assert set(fd['checkpoints'])=={'D198','D396','D792'}
        founders.append(fd); records.extend(data['attention'])
    if '--check' in sys.argv:
        print('Five founder records verified; only 103006..103008 will train.')
        return
    out.mkdir()
    for seed in range(103001,103006):
        (out/f'founder_{seed}.json').write_bytes((src/f'founder_{seed}.json').read_bytes())
    meta={k:val for k,val in old.items() if k not in ('founders','analysis','completed_founders','run_complete')}
    meta['continuation']={'preserved_founders':list(range(103001,103006)),
        'new_founders':list(range(103006,103009)),'python':sys.version,
        'numpy':base.np.__version__,'platform':platform.platform(),'cadence_net':version('cadence-net')}
    def save():
        (out/'V7_42_RESULTS.json').write_text(json.dumps({**meta,'completed_founders':len(founders),
            'run_complete':len(founders)==8,'founders':founders,'analysis':v.summarize(founders,records)},indent=2,default=str),encoding='utf-8')
    save()
    for seed in range(103006,103009):
        print(f'Continuing V7.42: founder {seed}',flush=True)
        fd,attention,maps=v.run_founder(seed)
        (out/f'founder_{seed}.json').write_text(json.dumps({'founder':fd,'attention':attention,'maps':maps},indent=2,default=str),encoding='utf-8')
        founders.append(fd); records.extend(attention); save()
        print(f'Finished {seed}: valid={fd["valid"]}',flush=True)
    print('Send back v7_42_results/V7_42_RESULTS.json and founder_103006..103008.json.')

if __name__=='__main__': main()

