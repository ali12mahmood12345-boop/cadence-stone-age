# V7.41 — qualified-learning convergence confirmed on eight founders

All eight founders 102001..102008 completed all checkpoints. The eight individual founder records match the aggregate. BASE accuracy was recomputed from all 24 checkpoint test panels (1100 trials each) and agrees with the saved metrics. All 139392 lessons were counted as qualified, with no recorded stage runtime errors; all recorded free/nudged/opposite maximum residuals are <=0.003.

| Checkpoint | Median BASE | Forced predecessor median | Map top-predecessor median |
|---|---:|---:|---:|
| D198 | 77.41% | 100% | 86.36% |
| D396 | 90.59% | 100% | 95.45% |
| D792 | 99.00% | 100% | 100% |

Every founder improved at both checkpoint transitions. D792 founder BASE ranges from 96.91% to 99.91%. Pooled D792 accuracy is 98.72%; distinguish this from the 99.00% founder median. Natural predecessor selection at D792 is 100% across all 8800 test records. All inherited gates pass; the recorded diagnosis is FINITE_DOSE_POSITION_CONVERGENCE_CONFIRMED.

This establishes convergence under V7.41's qualified-learning configuration. It does not retroactively validate the original finite-learning V7.36/V7.37 runs: V7.41 changes phase qualification, numerical integration and nudged budgets, and consequently learning trajectories. The earlier incomplete runs remain inconclusive under their original protocols.

V7.42 is an independent founder confirmation: keep the V7.41 procedure fixed and use seeds 103001..103008. This avoids prematurely attributing the remaining approximately 1% behavioral gap to a particular mechanism. Native recall_boundary=True and no manual START remain mandatory.

