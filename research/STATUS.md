# Cadence Research Status

Updated: 2026-10-26

## Confirmed

### Representation Keys V0.3D
Fresh confirmation on Cadence 0.85.1.

### Memory Keys V0.4B
Fresh confirmation on Cadence 0.85.1.

### Stone Age V7.13R — Fresh FIRE Boundary Confirmation
`FIRE_STREAM_STATE_RESET_CONFIRMED`

Strict fresh confirmation on Cadence 0.88.1.

Fresh founders:
- 77001..77016

Frozen successful recipe:
- FIRE_MINIMAL
- reset-per-row static bootstrap
- DAgger64
- full reset static replay
- commit gather primitive until immediate resource increment
- brain.reset() before every semantic high-level query
- 14-window budget
- no alternate arms or recipe changes

Results:
- valid founders: 16/16
- caretaker oracle: 96/96
- median exact: 100%
- median fresh: 100%
- median loop: 100%
- median ready-to-craft accuracy: 100%
- founder readiness: 16/16
- median high-level queries / decision windows: 2.0 / 3.5

All frozen confirmation gates passed.

Interpretation:
FIRE's dynamic failure was a controller-boundary problem: mid-primitive re-decision and per-stream hysteresis across semantic action transitions. Temporally extended gather primitives plus stream reset before the next semantic query reliably resolve it on a larger untouched founder panel.

See: [stone-age-v7-13r](./stone-age-v7-13r/README.md)

## Prior development boundary results

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

### Stone Age V7.13
`FIRE_STREAM_STATE_RESET_RESCUE`

## Next direction

**Stone Age V7.14 — Four-Skill Semantic Integration Bridge**

Reopen shared-brain integration now that the FIRE controller boundary is confirmed.

Initial integration should remain conservative:
- explicit task/goal context
- one shared full-11-action brain
- semantic task-state representation
- reset before independent teaching rows
- semantic-boundary stream resets
- temporally extended motor primitives where actions require persistence
- separate-brain controls retained
- no attention or episodic-memory arm yet

Primary question:
Can one plain Cadence brain retain and execute FOOD, FIRE, HUNT and SHELTER policies together without catastrophic cross-skill interference?

Attention/memory should only be reopened if plain shared capacity is first characterized.
