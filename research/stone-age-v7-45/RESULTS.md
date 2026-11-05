# V7.45 — Exact versus native position-target acquisition (completed)

**Run:** cadence-net 0.91.1, eight paired fresh founders 105001..105008; 16/16 arms and 8/8 pairs valid. All 17,424 lessons per arm qualified; no stage runtime errors. Solver residual maxima <=0.003. Frozen P_c and content-address map unchanged. Native recall_boundary=True, no manual START.

| Checkpoint | EXACT median BASE | NATIVE median BASE | Median paired NATIVE - EXACT |
|---|---:|---:|---:|
| D198 | 77.18% | 75.18% | -0.95 pp |
| D396 | 92.14% | 87.59% | -5.41 pp |
| D792 | 97.82% | 91.59% | -7.41 pp |

At D792, median map-top was 100% EXACT / 90.91% NATIVE. Forced-predecessor oracle was 100% in both arms. The D792 NATIVE-minus-EXACT gaps were negative in all eight founders: -8.36, -5.18, -6.36, -8.91, -10.55, -4.09, -7.91, -6.91 pp (seeds in ascending order).

The exact-arm positive control passes; the prespecified 5-pp matched native gap criterion **fails** despite NATIVE median BASE >=90%. This supports operational dependence on exact position teaching *under this training protocol*; not a general autonomy result.

Paired datasets were provided as V7_45_RESULTS(1).json plus all sixteen full founder files. Validation independently matched aggregate versus per-arm files and recomputed all TEST/CAL accuracies and 22 map-top checks at each checkpoint; no discrepancies. NATIVE has teacher_accuracy=null, not zero. Answer supervision and BLOCK_VALUE_TRAIN steering remained in both arms.

See ../stone-age-v7-46/RESULTS.md for a posthoc trial-level error attribution (not fresh confirmation).
