"""V7.37: controlled settling-budget confirmation of V7.36 FIXED."""
import json
import sys
from pathlib import Path
from importlib.metadata import version

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'stone-age-v7-36'))
import stone_age_v7_36_position_convergence as v

def main():
    assert version('cadence-net') == v.VERSION
    v.LEARNING_FREE_STEPS = 16384
    out = HERE / 'results'
    out.mkdir(exist_ok=True)
    founders, attention, maps = [], [], []
    for seed in range(v.FOUNDER_START, v.FOUNDER_START + 8):
        print(f'V7.37 founder {seed}, budget={v.LEARNING_FREE_STEPS}', flush=True)
        f, a, m = v.run_founder(seed)
        founders.append(f); attention.extend(a); maps.extend(m)
        (out / f'founder_{seed}.json').write_text(json.dumps({'founder':f,'attention':a,'maps':m}), encoding='utf-8')
        print(f'finished {seed}: valid={f["valid"]}', flush=True)
    summary = v.summarize(founders, attention)
    (out / 'V7_37_RESULTS.json').write_text(json.dumps({'experiment':'V7.37','free_steps':16384,'founders':founders,'analysis':summary}, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2), flush=True)

if __name__ == '__main__':
    main()

