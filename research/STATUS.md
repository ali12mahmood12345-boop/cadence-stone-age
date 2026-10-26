# Cadence Research Status

Updated: 2026-10-26

## Confirmed

### Representation Keys V0.3D
Fresh confirmation on Cadence 0.85.1.

### Memory Keys V0.4B
Fresh confirmation on Cadence 0.85.1.

## Development boundary results

### Stone Age V7.6R
`THRESHOLD_ENCODING_RESCUE_SURVIVES_SURPRISE`

### Stone Age V7.7R
`SURPRISE_CONTRAST_STATIC_RESCUE_CLOSED_LOOP_BOTTLENECK`

### Stone Age V7.8
`DYNAMIC_STATE_TEACHING_INSUFFICIENT`

### Stone Age V7.9
`STATIC_REPLAY_NO_RETENTION_RESCUE`

### Stone Age V7.10R
`RESET_BOUNDARY_RECOVERY_RESCUE`

### Stone Age V7.11
`FIRE_DYNAMIC_INVARIANCE_UNRESOLVED`

### Stone Age V7.12
`PARTIAL_FIRE_COMMITMENT_SIGNAL`

### Stone Age V7.13 — FIRE Semantic Boundary Reset Control
`FIRE_STREAM_STATE_RESET_RESCUE`

- cadence-net 0.88.1
- 8/8 founders valid
- caretaker oracle 48/48
- FIRE_MINIMAL static medians 100/100 exact/fresh
- same frozen final brain compared under both modes
- same 14-window environment budget
- COMMIT_CONTINUING:
  - median loop 100%
  - ready founders 5/8
  - median ready-to-craft accuracy 50%
  - median 2.5 high-level queries / 4.5 windows
- COMMIT_RESET_QUERY:
  - median loop 100%
  - ready founders 8/8
  - median ready-to-craft accuracy 100%
  - median 2.0 high-level queries / 3.5 windows
- paired founder loop comparison:
  - reset wins 3/8
  - ties 5/8
  - losses 0/8

Interpretation:
FIRE's remaining dynamic failure was per-stream hysteresis across semantic primitive boundaries. Temporally extended gather primitives plus `brain.reset()` before the next high-level query restore reliable ready-to-craft action selection.

Current successful FIRE controller recipe:
- FIRE_MINIMAL visible task state
- commit gather primitive until immediate resource increment
- reset stream before next semantic high-level query

See: [stone-age-v7-13](./stone-age-v7-13/README.md)

## Next direction

**Stone Age V7.13R — Fresh FIRE Boundary Confirmation**

Exact frozen replication only:
- FIRE_MINIMAL
- static bootstrap
- DAgger64
- full reset replay
- gather commitment
- reset before every high-level query
- 14-window budget
- no recipe changes

Recommended untouched founder panel:
- 77001..77016
- minimum valid 12/16
- confirmation >=12/16 individually ready

If V7.13R confirms, reopen the next Stone Age integration stage. Shared-brain memory/attention remains closed until that fresh confirmation.
