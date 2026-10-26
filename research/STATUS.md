# Cadence Research Status

Updated: 2026-10-26

## Confirmed

### Representation Keys V0.3D
Fresh confirmation on Cadence 0.85.1.

### Memory Keys V0.4B
Fresh confirmation on Cadence 0.85.1.

## Development boundary results

### Attention V0.5A
Original held split was underdetermined; behavioral conjunction conclusion retired.
Retrieval evidence remains informative.

### Stone Age V7–V7.5
Acquisition and representation bottleneck development sequence.

### Stone Age V7.6R
`THRESHOLD_ENCODING_RESCUE_SURVIVES_SURPRISE`

### Stone Age V7.7R
`SURPRISE_CONTRAST_STATIC_RESCUE_CLOSED_LOOP_BOTTLENECK`

### Stone Age V7.8
`DYNAMIC_STATE_TEACHING_INSUFFICIENT`

### Stone Age V7.9
`STATIC_REPLAY_NO_RETENTION_RESCUE`

### Stone Age V7.10
Frozen-run classification:
`STATIC_POLICY_NOT_RECOVERABLE_BY_ONE_PASS`

Interpretation reopened after runner audit:
- successful static bootstrap reset before every row
- V7.10 replay did not
- valid narrow claim: continuing no-reset replay failed
- broader irrecoverability claim is provisional

## Active frozen experiment

### Stone Age V7.10R — Replay Boundary Correction

Cadence 0.88.1, CONTRAST18, full11, surprise from lesson 0.

Common path:
- static bootstrap
- DAgger64
- branch exact post-DAGGER64 brain

Matched replay branches:
- CONTINUING_REPLAY
- RESET_REPLAY

Only branch difference:
- RESET_REPLAY calls `brain.reset()` immediately before every replay lesson.

Both branches use identical replay rows, ordering, labels and checkpoints:
- REPLAY32
- REPLAY64
- REPLAY_FULL

Primary question: does matching the successful static teaching boundary restore recoverability?

See: [stone-age-v7-10r](./stone-age-v7-10r/README.md)

Shared-brain memory/attention remains closed until this boundary is resolved.
