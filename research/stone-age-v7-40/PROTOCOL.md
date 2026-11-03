# V7.40 — Released residual-qualified solver

Use the V7.38 founder 102007 pre-free snapshot from lesson 7666. Verify its SHA256, reproduce original finite-mode residuals at caps 4096 and 16384, and abort interpretation if baseline reproduction fails.

From fresh copies of identical inputs, compare the released cadence-net 0.91.1 `equilibrate` API at both budgets: no damping (0), adaptive damping (3, starting at 0), and adaptive damping starting at half dt (3, starting at 1). Use chunk=32 and equation-residual tolerance=0.003. Run every condition twice. No gain, weights, drive or starting-state intervention is made. Damping redistributes a shared step budget across numerical dt halvings according to the released implementation.

Independently recompute residuals against the original core equations, require finite full state and residual <=0.003, compare with the solver's qualified flag, and enforce the total step budget. Record residual checks, stagnation checks, final halving index and repeated metric agreement. Save final states for independent comparison. Warnings remain errors.

Primary question: can the released qualified solver accept this previously failing free solve with residual <=0.003? This is a single-input numerical diagnostic, not a behavioral confirmation. Failure of the undamped control plus success of a damped condition would support numerical damping as a repair for this solve. It does not validate all founders or lessons.

No lesson is learned or accepted for training here. The snapshot does not contain the complete target/readout context required to reconstruct the original nudged/opposite learning phases. Therefore this package deliberately makes no claim about their convergence. A later training experiment must use qualified acceptance for all required phases, explicit adequate nudged budgets, and reject the entire lesson on any phase failure. Do not splice this successful free state into the old finite training path.

Native recall_boundary=True and no manual START are preserved in the inherited task state; no new task interactions occur. Python/NumPy versions are recorded and baseline reproduction is required across environments. The original user runtime was Python 3.15.2 / NumPy 2.5.4. Full-population V7.36/V7.37 classifications remain inconclusive.

