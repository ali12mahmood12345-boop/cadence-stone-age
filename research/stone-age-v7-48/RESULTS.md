# V7.48 verified laptop rerun — 2026-11-08

**24/24 runs complete; 8/8 valid triplets. Overall preregistered outcome: NOT REPLICATED.**

All 418,176 lessons qualified. Independently recomputed all checkpoint accuracy values from trial records, map-top/mass from 22 map records per checkpoint, and checked finite residuals <= .003, zero address/P_c invariants, balanced panels and founder identities. No recorded runtime errors. Native refusal counters are not persisted; a refusal raises in the runner.

The directional rate benefit passed, but NATIVE 0.20 D792 median BASE = 94.00%, below the frozen 95% criterion. This threshold is unchanged. This laptop rerun is separate from any unavailable previous-PC run.

Runtime: cadence-net 0.91.1; Python 3.12.14 (main, Aug 25 2026, 14:01:42) [MSC v.1944 64 bit (AMD64)]; NumPy 2.3.5. Native recall_boundary=True, no manual START. Answer supervision retained.

## Median accuracy (%)

| Arm | D198 | D396 | D792 |
|---|---:|---:|---:|
| EXACT_010 | 77.50 | 91.45 | 97.77 |
| NATIVE_010 | 74.45 | 83.91 | 89.86 |
| NATIVE_020 | 83.05 | 90.68 | 94.00 |

## All 24 runs — BASE accuracy (%)

| Founder | Arm | D198 | D396 | D792 |
|---|---|---:|---:|---:|
| 108001 | EXACT_010 | 74.64 | 91.18 | 98.36 |
| 108001 | NATIVE_010 | 73.45 | 86.00 | 87.45 |
| 108001 | NATIVE_020 | 81.91 | 92.73 | 95.91 |
| 108002 | EXACT_010 | 73.18 | 91.73 | 99.55 |
| 108002 | NATIVE_010 | 74.45 | 83.18 | 88.18 |
| 108002 | NATIVE_020 | 83.36 | 92.64 | 93.00 |
| 108003 | EXACT_010 | 77.55 | 90.00 | 96.82 |
| 108003 | NATIVE_010 | 73.64 | 83.91 | 91.55 |
| 108003 | NATIVE_020 | 77.64 | 86.09 | 92.27 |
| 108004 | EXACT_010 | 70.91 | 92.91 | 96.18 |
| 108004 | NATIVE_010 | 73.36 | 87.55 | 90.73 |
| 108004 | NATIVE_020 | 83.36 | 88.55 | 98.45 |
| 108005 | EXACT_010 | 77.45 | 90.09 | 97.18 |
| 108005 | NATIVE_010 | 80.09 | 86.18 | 88.09 |
| 108005 | NATIVE_020 | 82.00 | 92.64 | 91.18 |
| 108006 | EXACT_010 | 82.45 | 84.91 | 99.27 |
| 108006 | NATIVE_010 | 79.73 | 83.91 | 90.09 |
| 108006 | NATIVE_020 | 86.09 | 89.00 | 96.73 |
| 108007 | EXACT_010 | 81.00 | 93.09 | 96.73 |
| 108007 | NATIVE_010 | 74.45 | 82.91 | 91.27 |
| 108007 | NATIVE_020 | 82.73 | 88.91 | 95.00 |
| 108008 | EXACT_010 | 80.18 | 92.91 | 99.00 |
| 108008 | NATIVE_010 | 77.18 | 83.18 | 89.64 |
| 108008 | NATIVE_020 | 86.36 | 92.36 | 89.45 |

## Paired NATIVE 0.20 minus 0.10 (percentage points)

| Founder | D198 | D396 | D792 | D792 map-top |
|---|---:|---:|---:|---:|
| 108001 | +8.45 | +6.73 | +8.45 | +9.09 |
| 108002 | +8.91 | +9.45 | +4.82 | +0.00 |
| 108003 | +4.00 | +2.18 | +0.73 | +0.00 |
| 108004 | +10.00 | +1.00 | +7.73 | +4.55 |
| 108005 | +1.91 | +6.45 | +3.09 | +13.64 |
| 108006 | +6.36 | +5.09 | +6.64 | +9.09 |
| 108007 | +8.27 | +6.00 | +3.73 | +13.64 |
| 108008 | +9.18 | +9.18 | -0.18 | -4.55 |
| Median paired gain | +8.36 | +6.23 | +4.27 | +6.82 |

## Preregistered gates

| Gate | Result | Evidence |
|---|---|---|
| 1. At least 6 valid triplets | PASS | 8/8 |
| 2. EXACT control | PASS | BASE 97.77%; map-top 100%; oracle 100% |
| 3. Native oracle medians >=95% | PASS | Both 100% |
| 4. Paired BASE >=3 pp; map-top >=4.545 pp | PASS | +4.27 pp; +6.82 pp |
| 5. At least 6 positive founders AND native median >=95% | FAIL | 7/8 positive; median 94.00% |

The 0.20 rate improves this cohort, but the prespecified full replication claim fails. The gap between NATIVE 0.20 map-top median (100%) and behavior (94%) motivates a separate, exploratory read-temperature experiment; it cannot rescue V7.48.

AUDIT.json includes every forced-control accuracy, map metric, paired value and SHA-256 of every raw run. Reproduce with `python audit_results.py` beside the original v7_48_results directory. Raw trials are in the downloadable archive; they are not embedded in this report.

