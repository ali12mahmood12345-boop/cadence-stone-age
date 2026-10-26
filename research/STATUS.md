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

### Stone Age V7.12 — FIRE Temporal Action-Commitment Control
`PARTIAL_FIRE_COMMITMENT_SIGNAL`

- cadence-net 0.88.1
- 8/8 founders valid
- caretaker oracle 48/48
- same frozen final brain compared under decision-level vs commit-to-completion
- same 14-window environment budget
- final static exact/fresh medians 100/100 for all arms
- FIRE_MINIMAL:
  - decision median loop 0%
  - commit median loop 50%
  - commit-ready 3/8 founders
- FIRE_MINIMAL_PLUS_PROGRESS:
  - decision median loop 25%
  - commit median loop 50%
  - commit-ready 2/8
- CONTRAST18:
  - decision median loop 0%
  - commit median loop 0%
  - commit-ready 3/8
- no arm reached the >=6/8 founder pass gate

Interpretation:
Temporal commitment is a real partial mechanism, but the effect is heterogeneous. The frozen classifier used the predeclared difference-of-medians gain and returned PARTIAL_FIRE_COMMITMENT_SIGNAL; paired founder median gain was 0 because most founders tied.

Trace audit:
- commitment removes mid-gather switching in rescued founders
- remaining failed committed episodes typically acquire the required resource, then fail at the semantic transition to CRAFT_FIRE
- FIRE_MINIMAL has the same visible ready-to-craft task key as its 100%-correct static FIRE_CRAFT mapping, yet continuing action selection often repeats a gather action

Current dominant boundary:
**per-stream state / hysteresis across semantic action boundaries.**

See: [stone-age-v7-12](./stone-age-v7-12/README.md)

## Next direction

**Stone Age V7.13 — FIRE Semantic Boundary Reset Control**

Fresh founders, same training, primary FIRE_MINIMAL representation.

Compare:
- COMMIT_CONTINUING
- COMMIT_RESET_QUERY

COMMIT_RESET_QUERY calls `brain.reset()` immediately before each high-level query while preserving learned weights and the same 14-window budget.

Primary question:
Does clearing stream state at primitive boundaries restore the correct CRAFT_FIRE transition after gathering completes?

Shared-brain memory/attention remains closed until this control is resolved.
