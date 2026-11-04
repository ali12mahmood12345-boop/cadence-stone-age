# V7.42 complete — independent founder confirmation

All eight fresh founders 103001..103008 are valid. run_complete=true. Individual files match the aggregate, all 24 BASE test panels reproduce their checkpoint accuracies, and all 139392 recorded lessons qualify with phase maxima <=0.003 and no stage errors. The five preserved founder records and the three continuation founders are present.

Median BASE: D198 79.18%, D396 90.82%, D792 97.68%. Forced-predecessor median is 100% at every checkpoint. D792 natural predecessor selection is 100% across 8800 test records. All inherited gates pass, and the stronger descriptive D792 >=95% target passes. Pooled D792 accuracy is 97.375%, distinct from the median. Diagnosis: FINITE_DOSE_POSITION_CONVERGENCE_CONFIRMED under the qualified-learning protocol.

This independently supports V7.41 on fresh founders, without retroactively validating the earlier finite-learning runs. The continuation metadata records an operating-system build change; Python 3.15.2, NumPy 2.5.4 and cadence-net 0.91.1 are recorded for the continuation.

V7.43 is a short migration pilot comparing 0.91.1 and 0.93.1 with shared full-step adaptive damping. The old half-step-start option is absent in 0.93.1; the teacher hook and read-only diagnostics also require explicit adapters. Both adapted smoke runs passed. This does not establish upgrade equivalence or full-dose preservation; collect matched pilot outcomes before further migration.

