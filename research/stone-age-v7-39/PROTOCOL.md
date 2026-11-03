# V7.39 — Solver trajectory and numerical time-step probes

Use the byte-identical V7.38 snapshot from founder 102007, before the free solve of lesson 7666. Reproduce the original dt endpoints at 4096 and 16384 steps with tolerance 0.003; require both budget exhaustion and residual agreement within 1e-10 of 1.7105146077639979 before interpreting intervention results.

On fresh copies of the same saved inputs, compare original dt with dt/2, dt/4 and dt/8 at a cap of 16384 steps. Use cadence-net 0.91.1's numerical `_with_dt` copy; do not change neural gain, weights, drive, tolerance or initial state. This private API is version pinned. Smaller dt changes the numerical integration and elapsed model time at a given step count. These are budget-limited solver probes, not matched-duration simulations.

After each endpoint, disable early stopping and record 32 successive full states (v, activation, adaptation), equation residuals and maximum absolute one- and two-step state differences. Persistent nonzero one-step differences with near-zero two-step differences would support period-two behavior in this tail, not a theorem about the entire system.

Finite settling stops on movement, so a smaller step might stop early without a small equation residual. Report residual <=0.003 separately from stopping status; neither alone establishes a valid training repair. No training occurs. Original native recall_boundary=True / no manual START task state is inherited from the snapshot.

A successful numerical probe requires later checks on other failed lessons and full eight-founder training before any general convergence claim. Runtime differences and failed baseline reproduction must be reported explicitly. The supplied snapshot is verified by SHA256 before deserialization. Only the known V7.38 snapshot is accepted.

