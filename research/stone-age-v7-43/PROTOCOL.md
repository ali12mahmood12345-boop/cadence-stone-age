# V7.43 — Short cross-version compatibility and timing pilot

V7.42 independently confirms qualified-learning convergence in 8/8 fresh founders. Before migrating, compare cadence-net 0.91.1 with 0.93.1 on two fresh matched founders 104001/104002. Each trains 22 examples per pair (484 lessons), then tests 44 matched episodes under BASE, forced predecessor and forced target. This is deliberately shorter than D198 and is not a convergence confirmation.

Use the unchanged Stone Age task, native recall_boundary=True, no manual START, exact teacher and frozen address/P_c. Both versions use qualified learning with 4096 free/nudged caps, tolerance 0.003 and adaptive damping=3 STARTING AT FULL DT. This differs from V7.41/V7.42: initial_damping=1 was removed in 0.93.0. It is a shared-configuration migration pilot, not an unchanged-protocol upgrade.

The 0.93.1 adapter translates the new three-argument position-step call into the old exact-teacher implementation using the supplied eight-item found tuple; the mathematical update remains in the original function. Read-only compatibility properties expose _attended and position_map(0)[1] to the old diagnostics. These private adapters are version-specific and must be checked before any later migration. Both versions passed a 22-lesson smoke run including controls and geometry. This is not full-dose validation.

Each condition runs twice in separate processes; order old/new then new/old within each founder. Separate virtual environments use the same interpreter and NumPy must match before interpreting speed. Constrain common BLAS thread variables to one. Exclude imports, brain setup and a separate 22-lesson warmup from measured training and evaluation time.

Compare trial records, condition summaries, map records and phase report maxima for exact equality, while retaining raw metrics for numerical-difference analysis. An exact mismatch is not automatically a scientific regression; it requires inspection. Validity and small residuals are necessary. No full-dose behavior or speed claim follows from this pilot. Only consider a full-dose migration bridge after inspecting these results. The official 0.93.1 equivalence statement is versus 0.93.0, not 0.91.1.

