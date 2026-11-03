# V7.37 — Settling-budget confirmation

The completed V7.36 FIXED run still lost six of eight founders to free-phase budget exhaustion at 4096 sweeps. Only founders 102003 and 102008 completed. Their median BASE scores were 79.64%, 94.73%, and 93.64% at D198/D396/D792. This remains inconclusive; the monotonic-behavior gate also failed.

Before a read-strength intervention, test whether increasing the numerical budget alone restores the minimum six valid founders. V7.37 imports the archived V7.36 runner and changes only learning_free_steps from 4096 to 16384. Same founders 102001..102008, random panels, training doses, exact teacher, frozen address and P_c, rate, tolerances, and evaluation. Native recall_boundary=True; no manual START. Warnings remain errors. No failed lesson is retried or silently accepted.

Primary endpoint: at least six of eight founders complete all checkpoints. Scientific convergence classification retains all V7.36 gates; completion alone is not evidence of monotonic behavioral convergence. Compare matching founders/checkpoints with the archived 4096 run and report attrition explicitly. Save each founder immediately to avoid losing completed work.

Run with cadence-net==0.91.1 and numpy>=2,<3: `python run.py`.

