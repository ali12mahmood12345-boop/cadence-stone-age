# Stone Age V7.10 — Post-DAgger Consolidation / Recoverability Microscope

Status: **development complete — interpretation reopened by replay-boundary confound**

Cadence: **0.88.1**

Frozen run classification produced:

`STATIC_POLICY_NOT_RECOVERABLE_BY_ONE_PASS`

That classification describes the frozen V7.10 protocol exactly, but its broader recoverability interpretation is now **provisional**.

## Question

After a fixed DAgger64 phase, can a separate post-DAGGER static consolidation block recover the original static policy while preserving the dynamic one?

## Result

All **8/8 founders were valid**.

Median EXACT / FRESH / CLOSED-LOOP:

| Skill | STATIC_ONLY | POST_DAGGER64 | REPLAY32 | REPLAY64 | REPLAY_FULL |
| --- | --- | --- | --- | --- | --- |
| FOOD | 100 / 100 / 0% | 50 / 50 / 100% | 50 / 50 / 100% | 50 / 50 / 100% | 50 / 50 / 100% |
| FIRE | 100 / 100 / 0% | 33.3 / 33.3 / 0% | 33.3 / 33.3 / 16.7% | 33.3 / 33.3 / 0% | 33.3 / 33.3 / 41.7% |
| HUNT | 100 / 100 / 83.3% | 95.3 / 97.2 / 100% | 68.2 / 67.4 / 100% | 62.2 / 58.3 / 100% | 62.2 / 58.3 / 100% |
| SHELTER | 100 / 100 / 0% | 66.7 / 66.7 / 100% | 66.7 / 66.7 / 100% | 66.7 / 66.7 / 100% | 66.7 / 66.7 / 100% |

Founder-level all-four readiness remained 0/8 at every checkpoint.

Mean median retention declined from:
- STATIC_ONLY: 1.000
- POST_DAGGER64: 0.613
- REPLAY32: 0.543
- REPLAY64: 0.521
- REPLAY_FULL: 0.521

Mean median loop rose from 0.208 static-only to 0.854 at REPLAY_FULL.

## Important protocol confound discovered after the run

The successful static bootstrap used:

`brain.reset()` before **every static teaching row**.

The V7.10 post-DAGGER replay loop did **not** call `brain.reset()` before replay rows.

Therefore V7.10 did not actually test a matched reapplication of the original successful static curriculum. It tested a **continuing-stream replay schedule** after DAgger.

This matters because the observed replay accounting is inconsistent with the cold static errors in a way that strongly suggests the lesson's teaching boundary was not equivalent to cold static readback.

Example pattern:
- FOOD POST_DAGGER64 median static accuracy = 50%
- REPLAY32/64 medians report essentially all rows as agreed/skipped
- static accuracy remains 50%

So the strong claim "one full pass cannot recover the static policy" is too broad.

## What remains valid

V7.10 still establishes:

> Continuing no-reset post-DAGGER replay, even through one full static pass, does not restore the cold static policy and can even worsen it.

It does **not** yet establish:

> A matched cold/reset replay of the original successful static curriculum cannot recover the policy.

## Next direction

**Stone Age V7.10R — Replay Boundary Correction**

Start from an identical post-DAGGER64 brain and compare:

1. `CONTINUING_REPLAY`
   - reproduce V7.10
   - no reset before replay rows

2. `RESET_REPLAY`
   - call `brain.reset()` before every replay row
   - otherwise same rows/order/doses

Checkpoints:
- POST_DAGGER64
- REPLAY32
- REPLAY64
- REPLAY_FULL

Primary question:
Does the reset-matched replay recover the cold static mappings that the continuing replay failed to recover?

If RESET_REPLAY restores static accuracy while CONTINUING_REPLAY does not, V7.10's apparent irrecoverability was a teaching-boundary/context artifact.

If both fail, the deeper retention/plasticity interpretation survives.

Do not move to shared-brain memory/attention until V7.10R resolves this.
