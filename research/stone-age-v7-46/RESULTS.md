# V7.46 — Paired trial-level error attribution

**Classification:** POSTHOC_PAIRED_TEST_TRIAL_ERROR_ATTRIBUTION. This is a diagnostic reanalysis of completed V7.45; it did **not** train new brains.

## Method
Use full V7.45 founder records for EXACT/NATIVE seeds 105001..105008. Recompute test and calibration accuracies and maps; confirm 16/16 arm validity, qualified lessons, frozen map and P_c. For each checkpoint D198/D396/D792, align 1,100 TEST/BASE trials per seed on (test_index, length, query), giving 8,800 paired trials per checkpoint. Count joint correctness and split NATIVE mistakes by whether the attention winner is the predecessor. A top-attention winner is *not* a hard or causal routing decision.

## Results

| Checkpoint | EXACT-only correct | NATIVE-only correct | Both correct | Both wrong | NATIVE errors where top is not predecessor |
|---|---:|---:|---:|---:|---:|
| D198 | 828 | 731 | 5,852 | 1,389 | 1,530 / 2,217 (69.01%) |
| D396 | 875 | 350 | 7,192 | 383 | 867 / 1,258 (68.92%) |
| D792 | 750 | 109 | 7,880 | 61 | 565 / 811 (69.67%) |

At D792, 246 NATIVE errors occurred **even with** the predecessor ranked first. NATIVE was correct on 135 trials where its highest attention weight was assigned elsewhere. Of 750 EXACT-only successes, 539 had a non-predecessor NATIVE attention winner. Paired mean D792 native-minus-exact BASE gap was -7.284 pp; median was -7.409 pp.

## Interpretation
Incorrect predecessor ranking is associated with much of native error, but top-rank identity is not enough to predict output under soft attention. No causal mechanism has been isolated and the same eight V7.45 founders are reused; no new intervention or independent replication took place. NATIVE still had answer supervision and route steering, so not unsupervised learning.

## Recommended next causal test
Vary native position-target acquisition/attention strength as a separately labeled intervention under matched new founders. Retain a contemporaneous exact control, unchanged task/evaluation panels, learning qualifications and oracles, and freeze conditions. Keep cadence-net 0.91.1 separate from future version migration.
