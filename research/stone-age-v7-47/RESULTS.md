# Cadence Stone Age V7.47 — 8/8 triplets valid; native rate intervention passes

**Status:** Complete; independently audited from the 24 submitted founder JSON files and `V7_47_RESULTS.json` on 2026-11-07. The experiment is a controlled task-level rate intervention, not a general autonomy test.

## Main finding

Doubling released **native position learning rate** from 0.10 to 0.20 strongly improved BASE performance at the fixed D198/D396/D792 checkpoints, under otherwise matched teaching, evaluation and numerical qualification.

| Checkpoint | EXACT 0.10 median BASE | NATIVE 0.10 median BASE | NATIVE 0.20 median BASE | Median paired NATIVE 0.20−0.10 |
|---|---:|---:|---:|---:|
| D198 | 78.14% | 75.32% | 84.14% | +7.23 pp |
| D396 | 91.86% | 86.23% | 91.59% | +5.68 pp |
| D792 | 98.50% | 91.41% | 98.14% | **+4.77 pp** |

D792 median map-top predecessor: EXACT 0.10 **100%**, NATIVE 0.10 **90.91%**, NATIVE 0.20 **100%**. Median paired map-top improvement: **+6.82 pp**, above the preregistered +1/22 = 4.545 pp gate. The forced-predecessor oracle median was **100% in all three arms**. D792 predecessor-mass medians NATIVE 0.10 **0.62680** vs NATIVE 0.20 **0.67280**.

All **8/8 paired founders improved** their D792 BASE accuracy under NATIVE 0.20 versus NATIVE 0.10, paired differences +1.00 to +9.09 pp (mean +4.78 pp). One-sided sign test for eight positive differences has p = 1/256 = 0.00390625, conditional on the predesignated directional test and ignoring selection/multiplicity across broader research. Native 0.20 minus EXACT D792 median paired difference: **−0.45 pp**. No claim of general model equivalence is warranted.

### D792 founder-level BASE (%)

| Founder | EXACT_010 | NATIVE_010 | NATIVE_020 | Paired gain NATIVE_020−010 |
|---|---:|---:|---:|---:|
| 107001 | 99.45 | 89.73 | 95.55 | +5.82 |
| 107002 | 96.27 | 97.82 | 99.18 | +1.36 |
| 107003 | 98.82 | 90.73 | 94.45 | +3.73 |
| 107004 | 98.82 | 95.91 | 96.91 | +1.00 |
| 107005 | 94.27 | 90.09 | 99.18 | +9.09 |
| 107006 | 97.91 | 89.18 | 97.64 | +8.45 |
| 107007 | 99.91 | 97.00 | 99.27 | +2.27 |
| 107008 | 98.18 | 92.09 | 98.64 | +6.55 |

## Validity / independent audit

24/24 arm files, 8/8 matched triplets, `run_complete=true`, all 17,424 accepted lessons per arm residual-qualified, no reported stage runtime errors, three finite phase maxima each ≤0.003. Frozen address and P_c were zero. For each arm and checkpoint, independently recomputed TEST BASE, FORCE_PREDECESSOR, FORCE_TARGET metrics from 1,100 trial records each, CAL BASE accuracy from 440 records, all per-length/per-position/per-pair accuracies, and 22 map-position entries. Verified metadata, test-index uniqueness, founder/arm identities, the supplied aggregate pair results, native teacher_accuracy=null and 0 teacher rows, and exact teacher scored 100% whenever it supplied a target.

Source file hashes, per-founder audit, and the complete input bundle are included in the separate downloadable audit archive. Raw 24 × ~4.45 MB JSON files were supplied in a RAR; they are **not** embedded in this GitHub text report.

## Outcome classification

- **valid triplets gate:** PASS (8 ≥ 6)
- **EXACT positive-control D792 BASE/map-top/oracle gate:** PASS
- **both native oracle gates:** PASS
- **predefined NATIVE 0.20 rate effect** (paired median BASE gain ≥3 pp and map-top gain ≥1/22): **PASS**
- **classification:** `NATIVE_POSITION_RATE_EFFECT_CONFIRMED_ON_THIS_TASK` (within this initial experiment).

**Interpretation:** The released native position learner is able to approach exact-teacher test accuracy on the controlled variable-length predecessor task when its position-update rate is increased from 0.10 to 0.20. This is not unsupervised learning: answer labels and BLOCK_VALUE_TRAIN routing supervision remain. The rate effect does not establish that 0.20 is optimal, nor does the descriptive map-top association isolate the full causal mechanism.

## Next experiment

V7.48 should attempt **fresh matched-seed confirmation** with the same three arms (EXACT_010, NATIVE_010, NATIVE_020), identical numeric rules, and new founders 108001–108008, rather than adding an exploratory fourth rate. Predefine validity and effect gates before running. A fresh confirmation can evaluate reproducibility of the effect and any remaining per-founder failures.
