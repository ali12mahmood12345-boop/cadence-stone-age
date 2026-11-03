# V7.41 — Qualified-learning feasibility and behavior

V7.40 confirms residual-qualified adaptive damping solves one previously failing free phase. All six repeated final-state pairs in the supplied V7.40 files are finite and exactly equal. Undamped residual stays 1.710514607764; adaptive damping reaches 0.001539386377 in 384 steps; starting at half dt reaches 0.000735020866 in 96 steps at either cap.

Test eight founders 102001..102008 from scratch with released cadence-net 0.91.1 qualified learning. Every free, nudged and opposite phase must qualify before the released learner's weight update. Set tolerance=0.003, free_steps=4096, nudged_steps=4096, damping=3 and initial_damping=1. Validate returned phase residuals after every successful lesson. On any exception, warning or failed check, stop that founder and record the error; never continue after failure or retry a partly processed lesson.

This changes the learning procedure: all-phase equation qualification replaces finite phases, and nudged budgets increase from 12 to 4096. It is not a pure free-budget comparison or a reproduction of the old trajectory. These changes are explicit and necessary to test a fully qualified learning path. Compare feasibility and behavioral outcomes descriptively against V7.36/V7.37; do not attribute differences solely to dt.

Preserve original seeds/panels, exact predecessor teacher, frozen address and position P_c, position rate 0.10, native recall_boundary=True, no manual START, route steering, 22 pairs, and checkpoints D198/D396/D792. All required phase budgets are caps, not mandatory iteration counts. Save each founder and a partial aggregate as it completes; the run is complete only when run_complete=true.

Primary endpoint: at least six of eight founders valid at all checkpoints, with every accepted training lesson qualified and all recorded phase residuals <=0.003. Behavioral gates are the inherited V7.36 gates and should be reported separately; numerical completion does not guarantee convergence or preserved behavior. No new biological or full-game claim.

The inherited attention summary uses available checkpoint records while behavioral medians use complete founders; keep those populations distinct. The eight-founder run can be long. The package smoke test validates 22 lessons only; it is not full-run evidence. Snapshot solver success does not guarantee nudged/opposite phase success during training.

