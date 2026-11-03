# V7.40 user-run confirmation

Baseline reproduced; repeated metrics match. All six pairs of saved final states were independently checked for finiteness and exact equality.

At caps 4096 and 16384, undamped qualified solving fails at residual 1.710514607764. Adaptive damping qualifies in 384 steps at residual 0.001539386377. Starting at half dt qualifies in 96 steps at residual 0.000735020866. Both repeats match. User runtime: Python 3.15.2, NumPy 2.5.4, cadence-net 0.91.1.

This confirms one saved free solve, not full learning. V7.41 tests eight founders with all three learning phases qualified, adequate nudged budgets and initial half dt. It is an explicit learning-procedure change, not a pure budget comparison. Native recall_boundary=True and no manual START remain required.
