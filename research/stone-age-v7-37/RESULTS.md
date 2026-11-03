# V7.37 — Settling-budget confirmation results

## Decision

The 16384-sweep run fails its primary endpoint: 2/8 valid founders, below the required six. Classification remains `POSITION_CONVERGENCE_DOSE_TEST_INCONCLUSIVE`. Increasing the budget fourfold did not improve the completion count.

All eight per-founder records match the aggregate. BASE test accuracy was independently recomputed from 1100 trial records for every available checkpoint and matches the saved checkpoint metrics. Input hashes and audited metrics are in V7_37_AUDIT.json.

## Performance

| Checkpoint | Median BASE, two full-run completers | Forced predecessor | Map top-predecessor |
|---|---:|---:|---:|
| D198 | 78.55% | 100% | 86.36% |
| D396 | 91.86% | 100% | 95.45% |
| D792 | 95.73% | 100% | 100% |

Completers are 102006 and 102008. Their D792 BASE scores are 98.27% and 93.18%. Mean predecessor mass at D792 is 59.75%. Perfect top-address selection with imperfect BASE still motivates a future read-strength intervention, but does not establish its cause.

The median curve is monotonic; individual improvement is not universal: founder 102008 declines slightly from 93.27% at D396 to 93.18% at D792. The all_next_routes gate fails its minimum count of six, rather than demonstrating a route reversal among the two completers.

Available-case median BASE values are 81.23% (8 founders), 93.45% (7), and 95.73% (2). These changing populations must not be interpreted as a paired convergence curve. The original attention summary also pools all available checkpoint records, unlike the completer-only behavioral medians.

## Paired numerical comparison

Counts below are completed lessons before the first failure, or all 17424 for a completed founder.

| Founder | V7.36 FIXED, 4096 | V7.37, 16384 | Outcome |
|---|---:|---:|---|
| 102001 | 14745 | 17174 | Failure delayed |
| 102002 | 10436 | 10436 | Same count |
| 102003 | 17424, complete | 14804 | Previously successful, now fails |
| 102004 | 8917 | 8917 | Same count |
| 102005 | 10439 | 10439 | Same count |
| 102006 | 11799 | 17424, complete | Rescued |
| 102007 | 7665 | 7665 | Same count |
| 102008 | 17424, complete | 17424, complete | Complete in both |

Every recorded failure is a finite teaching free-phase budget warning. Shared early checkpoint BASE scores match across runs. However, the changed survivor set means 95.73% versus the prior 93.64% is not an estimate of a paired budget benefit. Repeated failure counts are evidence against assuming that every failure merely needs more sweeps; they do not by themselves prove oscillation or divergence.

## Recommended V7.38: failing-lesson solver diagnostics

Replay founder 102007 first: it fails earliest, at the same count under both budgets. Capture a complete state immediately before lesson 7666 (after 7665 successful lessons), including random state and training context. Verify faithful replay before interventions.

From identical pre-lesson states, compare 4096 and 16384 budgets and record equation residuals, convergence status, and iteration behavior. Inspect the released solver before selecting additional diagnostic budgets or gain changes. No warning should be ignored and no failed lesson counted as valid training. If gain or another numerical parameter changes, label that intervention explicitly and evaluate its effect separately.

Also investigate the 102003 completion reversal with identical environment/version metadata and reproducible pre-lesson states. Do not attribute it to the budget alone without that check.

Preserve native recall_boundary=True, no manual START, task seeds and panels, exact predecessor teaching, frozen address and P_c, and released position-learning settings. V7.38 is recommended here, not yet implemented or run. Defer the read-strength causal experiment until numerical validity is resolved, or explicitly label it exploratory on surviving founders.

