# V7.43 — Short migration pilot passed

All eight runs are valid and use matching environment metadata. The individual files match the aggregate; each run completed 484 qualified lessons and recorded phase maxima <=0.003. Across all four old/new pairs, condition summaries, trial records, map records and training summaries match exactly.

Median new/old elapsed ratios: training 0.98905 (about 1.1% less time), evaluation 0.98683 (about 1.3% less time). Individual training ratios span 0.95684..1.00830 and evaluation ratios 0.95717..1.04345. This is near parity, not convincing evidence of a material speedup on this small model.

The dose is only 22 examples/pair. BASE is 27.27% and 45.45% for the two founders, while forced predecessor is 22.73% and 70.45%; the downstream route is not yet learned to its full-dose capability. This is compatibility evidence at low dose, not convergence or full-dose migration evidence.

Both versions use full-step adaptive damping, unlike V7.41/V7.42's half-step start. The documented teacher-call and read-only diagnostic adapters remain required in 0.93.1. V7.44 extends the matched comparison through all three original dose checkpoints before deciding whether to migrate further.

