# V7.38 — Failing-lesson free-solver diagnostics

V7.37 still completed only 2/8 founders. Founder 102007 stopped after 7665 successful lessons under both 4096 and 16384 budgets. Replay that founder separately under each budget, including the original D198 checkpoint evaluations, then intercept the free phase of lesson 7666 before its learning update.

Preserve cadence-net 0.91.1, original panels/seeds, exact predecessor teaching, frozen address/P_c, native recall_boundary=True and no manual START. Warnings remain errors during replay. Any earlier warning or invalid checkpoint ends the arm and is reported.

At the diagnostic target, snapshot the complete free-solver core, drive and warm state. Solve disposable copies at 4096 and 16384 steps with the unchanged tolerance. Repeat 16384 once to check determinism. Record steps and equation residuals; no diagnostic solve is accepted as a training lesson. The pickle is a local solver-input checkpoint, not a resumable full-training checkpoint. Load pickle files only when trusted.

Primary reproduction checks: reach lesson 7666 without an earlier failure, D198 BASE matches the prior founder (0.759090909090909), and the matching-budget diagnostic exhausts its budget. Check these before interpreting the cross-budget probe. This is a targeted diagnostic, not an eight-founder confirmation or a behavioral improvement experiment. A residual above tolerance supports non-settlement at that cap, but cannot alone establish cycling or divergence.

The two budget trajectories may reach different internal states; budget comparisons within each arm use identical saved solver inputs. Report cross-arm differences separately. The package records Python, NumPy and platform metadata. Original runtime differences remain a possible explanation for replay mismatches.

No gain changes, larger-budget training, or read-strength interventions are included. Inspect these diagnostics before choosing the next intervention. Founder 102003's completion reversal remains a separate follow-up.

