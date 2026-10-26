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

Observed:
- 8/8 founders valid
- static bootstrap retained 100/100 medians
- DAgger64 improved dynamic behavior while degrading static mappings
- continuing post-DAGGER replay did not restore static accuracy
- REPLAY_FULL retention score 0.521, loop score 0.854
- no static-recovery checkpoint

**Interpretation reopened after runner audit.**

The original successful static bootstrap resets the brain before every teaching row. V7.10 post-DAGGER replay did not reset before replay rows. Therefore V7.10 tested continuing-stream replay, not a matched replay of the original successful static curriculum.

Valid narrower conclusion:
- continuing no-reset replay does not recover cold static mappings.

Not yet established:
- reset-matched cold replay cannot recover them.

See: [stone-age-v7-10](./stone-age-v7-10/README.md)

## Next direction

**Stone Age V7.10R — Replay Boundary Correction**

Matched branches from the same post-DAGGER64 state:

- CONTINUING_REPLAY
- RESET_REPLAY

Replay checkpoints:
- REPLAY32
- REPLAY64
- REPLAY_FULL

RESET_REPLAY calls `brain.reset()` before every static replay row, matching the successful bootstrap teaching boundary.

Primary question: was V7.10's apparent irrecoverability a continuing-state teaching artifact or a real plasticity/retention boundary?

Shared-brain memory/attention remains closed until this is resolved.
