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

- 8/8 founders valid
- caretaker oracle 48/48
- final static exact/fresh 100/100 medians for all three representation arms
- final loop medians:
  - CONTRAST18 0%
  - FIRE_MINIMAL 0%
  - FIRE_MINIMAL_PLUS_PROGRESS 25%
- failure traces concentrate on mid-gather action switches
- explicit progress state is informative but not sufficient
- current dominant boundary: temporal action commitment / motor primitive persistence

## Active frozen experiment

### Stone Age V7.12 — FIRE Temporal Action-Commitment Control

FIRE only.

Fresh founders:
- 75001..75008

Representations:
- CONTRAST18
- FIRE_MINIMAL
- FIRE_MINIMAL_PLUS_PROGRESS

Training matches V7.11.

Final frozen brain is evaluated under:
- DECISION_LEVEL
- COMMIT_TO_COMPLETION

COMMIT_TO_COMPLETION holds GATHER_WOOD or GATHER_STONE until the corresponding resource increases before querying the brain again.

Fairness:
- both modes share the same 14 decision-window episode budget
- internal committed windows consume that same budget
- same held-out seeds and variants
- no extra learning

Primary question:
Does the learned FIRE policy succeed when gather actions are treated as temporally extended motor primitives rather than re-decided every 0.55 s?

See: [stone-age-v7-12](./stone-age-v7-12/README.md)

Shared-brain memory/attention remains closed until this temporal-action boundary is resolved.
