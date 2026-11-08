"""Independent stdlib audit; run after run.py, from any working directory."""
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from statistics import median, mean

HERE = Path(__file__).resolve().parent
OUT = HERE / 'v7_48_results'
ARMS = ('EXACT_010', 'NATIVE_010', 'NATIVE_020')
CKS = ('D198', 'D396', 'D792')
CONDS = ('BASE', 'FORCE_PREDECESSOR', 'FORCE_TARGET')

def finite(x):
    if isinstance(x, float):
        assert math.isfinite(x)
    elif isinstance(x, dict):
        for v in x.values(): finite(v)
    elif isinstance(x, list):
        for v in x: finite(v)

def main():
    aggregate = json.loads((OUT/'V7_48_RESULTS.json').read_text())
    rows, hashes = [], {}
    expected = {f'founder_{s}_{a}.json' for s in range(108001,108009) for a in ARMS}
    assert {p.name for p in OUT.glob('founder_*.json')} == expected
    for seed in range(108001,108009):
        for arm in ARMS:
            path=OUT/f'founder_{seed}_{arm}.json'
            hashes[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
            obj=json.loads(path.read_text()); finite(obj)
            f=obj['founder']; assert f['founder']==seed and obj['arm']==arm and f['valid']==1
            assert f['address_map_max_abs']<=1e-12 and f['position_c_max_abs']<=1e-12
            assert f['position_rate']==(.2 if arm=='NATIVE_020' else .1)
            assert len(f['stages'])==3
            for s,n,c in zip(f['stages'],(4356,4356,8712),(198,396,792)):
                assert s['lessons']==s['qualified_lessons']==n and not s['runtime_errors']
                assert s['cumulative_per_pair']==c and s['per_pair']*22==n
                assert set(s['phase_max_residual'])=={'free','nudged','opposite'}
                assert all(0<=r<=.003 for r in s['phase_max_residual'].values())
            if arm=='EXACT_010':
                assert f['teacher_rows']>0 and f['teacher_correct']==f['teacher_rows'] and f['teacher_accuracy']==1
            else:
                assert f['teacher_rows']==0 and f['teacher_accuracy'] is None
            row={'seed':seed,'arm':arm,'checkpoints':{}}
            assert len(obj['attention'])==3*(440+3*1100) and len(obj['maps'])==66
            for ck in CKS:
                c=f['checkpoints'][ck]; assert c['valid'] and c['calibration']['valid']
                vals={}
                for panel,cond,n in [('CAL','BASE',440)]+[('TEST',x,1100) for x in CONDS]:
                    rec=[r for r in obj['attention'] if (r['checkpoint'],r['panel'],r['condition'])==(ck,panel,cond)]
                    assert len(rec)==n and {r['test_index'] for r in rec}==set(range(n))
                    counts=Counter((r['length'],r['query']) for r in rec)
                    assert len(counts)==22 and set(counts.values())=={n//22}
                    assert all(r['founder']==seed and r['correct'] in (0,1) for r in rec)
                    accuracy=mean(r['correct'] for r in rec)
                    saved=c['calibration'] if panel=='CAL' else c['conditions'][cond]
                    assert saved['valid'] and not saved['runtime_errors']
                    assert math.isclose(accuracy,saved['accuracy'],abs_tol=1e-12)
                    if panel=='TEST': vals[cond]=accuracy
                maps=[m for m in obj['maps'] if m['checkpoint']==ck]
                assert len(maps)==22 and len({(m['length'],m['query']) for m in maps})==22
                vals['map_top']=mean(m['top_is_predecessor'] for m in maps)
                vals['map_mass']=mean(m['predecessor_mass'] for m in maps)
                assert math.isclose(vals['map_top'],c['map_geometry']['top_predecessor_rate'],abs_tol=1e-12)
                assert math.isclose(vals['map_mass'],c['map_geometry']['mean_predecessor_mass'],abs_tol=1e-12)
                row['checkpoints'][ck]=vals
            rows.append(row)
    paired=[]
    for seed in range(108001,108009):
        r={x['arm']:x['checkpoints'] for x in rows if x['seed']==seed}
        paired.append({'seed':seed,**{ck:{'base_gain':r['NATIVE_020'][ck]['BASE']-r['NATIVE_010'][ck]['BASE'],'map_top_gain':r['NATIVE_020'][ck]['map_top']-r['NATIVE_010'][ck]['map_top']} for ck in CKS}})
    med={ck:{a:{k:median(r['checkpoints'][ck][k] for r in rows if r['arm']==a) for k in ('BASE','FORCE_PREDECESSOR','FORCE_TARGET','map_top','map_mass')} for a in ARMS} for ck in CKS}
    gains={ck:{k:median(p[ck][k] for p in paired) for k in ('base_gain','map_top_gain')} for ck in CKS}
    d=med['D792']; e=d['EXACT_010']; positive=sum(p['D792']['base_gain']>0 for p in paired)
    gates={'six_valid_triplets':True,'exact_control':e['BASE']>=.9 and e['map_top']>=.95 and e['FORCE_PREDECESSOR']>=.95,'native_oracle':all(d[a]['FORCE_PREDECESSOR']>=.95 for a in ARMS[1:]),'rate_effect':gains['D792']['base_gain']>=.03 and gains['D792']['map_top_gain']>=1/22,'six_positive_founders':positive>=6,'native020_high':d['NATIVE_020']['BASE']>=.95}
    gates['replication_confirmed']=all(gates.values())
    assert gates==aggregate['gates'] and aggregate['run_complete'] and aggregate['completed_arms']==24
    for ck in CKS:
        for a in ARMS:
            for k,old in [('BASE','base'),('FORCE_PREDECESSOR','oracle'),('map_top','map_top'),('map_mass','map_mass')]:
                assert math.isclose(med[ck][a][k],aggregate['summary']['checkpoints'][ck][a][old],abs_tol=1e-12)
    doc={'audited_runs':24,'valid_triplets':8,'positive_founders':positive,'medians':med,'paired_median_gains':gains,'gates':gates,'runs':rows,'paired':paired,'sha256':hashes}
    (HERE/'AUDIT.json').write_text(json.dumps(doc,indent=2,allow_nan=False)+'\n')
    lines=['# V7.48 verified laptop rerun — 2026-11-08','','**24/24 runs complete; 8/8 valid triplets. Overall preregistered outcome: NOT REPLICATED.**','',f'All {24*17424:,} lessons qualified. Independently recomputed all checkpoint accuracy values from trial records, map-top/mass from 22 map records per checkpoint, and checked finite residuals <= .003, zero address/P_c invariants, balanced panels and founder identities. No recorded runtime errors. Native refusal counters are not persisted; a refusal raises in the runner.','','The directional rate benefit passed, but NATIVE 0.20 D792 median BASE = 94.00%, below the frozen 95% criterion. This threshold is unchanged. This laptop rerun is separate from any unavailable previous-PC run.','','Runtime: cadence-net 0.91.1; Python '+aggregate['python']+'; NumPy '+aggregate['numpy']+'. Native recall_boundary=True, no manual START. Answer supervision retained.','','## Median accuracy (%)','','| Arm | D198 | D396 | D792 |','|---|---:|---:|---:|']
    for a in ARMS: lines.append('| '+a+' | '+' | '.join(f'{100*med[c][a]["BASE"]:.2f}' for c in CKS)+' |')
    lines+=['','## All 24 runs — BASE accuracy (%)','','| Founder | Arm | D198 | D396 | D792 |','|---|---|---:|---:|---:|']
    for r in rows: lines.append(f'| {r["seed"]} | {r["arm"]} | '+' | '.join(f'{100*r["checkpoints"][c]["BASE"]:.2f}' for c in CKS)+' |')
    lines+=['','## Paired NATIVE 0.20 minus 0.10 (percentage points)','','| Founder | D198 | D396 | D792 | D792 map-top |','|---|---:|---:|---:|---:|']
    for p in paired: lines.append(f'| {p["seed"]} | '+' | '.join(f'{100*p[c]["base_gain"]:+.2f}' for c in CKS)+f' | {100*p["D792"]["map_top_gain"]:+.2f} |')
    lines.append('| Median paired gain | '+' | '.join(f'{100*gains[c]["base_gain"]:+.2f}' for c in CKS)+f' | {100*gains["D792"]["map_top_gain"]:+.2f} |')
    lines+=['','## Preregistered gates','','| Gate | Result | Evidence |','|---|---|---|','| 1. At least 6 valid triplets | PASS | 8/8 |','| 2. EXACT control | PASS | BASE 97.77%; map-top 100%; oracle 100% |','| 3. Native oracle medians >=95% | PASS | Both 100% |','| 4. Paired BASE >=3 pp; map-top >=4.545 pp | PASS | +4.27 pp; +6.82 pp |',f'| 5. At least 6 positive founders AND native median >=95% | FAIL | {positive}/8 positive; median 94.00% |','','The 0.20 rate improves this cohort, but the prespecified full replication claim fails. The gap between NATIVE 0.20 map-top median (100%) and behavior (94%) motivates a separate, exploratory read-temperature experiment; it cannot rescue V7.48.','','AUDIT.json includes every forced-control accuracy, map metric, paired value and SHA-256 of every raw run. Reproduce with `python audit_results.py` beside the original v7_48_results directory. Raw trials are in the downloadable archive; they are not embedded in this report.']
    (HERE/'RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'runs':24,'gates':gates,'positive':positive,'medians':med,'gains':gains},indent=2))

if __name__=='__main__': main()

