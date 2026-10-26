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

### Stone Age V7.10
Frozen run suggested irrecoverability, but interpretation was reopened after replay-boundary audit.

### Stone Age V7.10R
`RESET_BOUNDARY_RECOVERY_RESCUE`

Reset-matched replay restores the static policy. FIRE remains the dominant dynamic failure.

### Stone Age V7.11 — FIRE Dynamic Invariance Microscope
`FIRE_DYNAMIC_INVARIANCE_UNRESOLVED`

- cadence-net 0.88.1
- 8/8 founders valid
- caretaker oracle 48/48
- final reset-replay static medians:
  - CONTRAST18 100/100
  - FIRE_MINIMAL 100/100
  - FIRE_MINIMAL_PLUS_PROGRESS 100/100
- final loop medians:
  - CONTRAST18 0%
  - FIRE_MINIMAL 0%
  - FIRE_MINIMAL_PLUS_PROGRESS 25%
- final-ready founders:
  - CONTRAST18 2/8
  - FIRE_MINIMAL 2/8
  - FIRE_MINIMAL_PLUS_PROGRESS 0/8
- minimal arms show no frozen median loop gain over CONTRAST18

Trace-level interpretation:
- failures concentrate on intermediate gather-continuation states
- the brain often switches away from GATHER_WOOD/GATHER_STONE before the resource increment completes
- some founders specialize by missing-resource branch
- explicit progress state is informative but not sufficient
- some 6/6 post-DAGGER progress policies fall to 3/6 after cold static replay

Current dominant boundary:
**temporal action commitment / multi-decision motor primitive persistence**, with progress-conditioned retention as a secondary interaction.

See: [stone-age-v7-11](./stone-age-v7-11/README.md)

## Next direction

**Stone Age V7.12 — FIRE Temporal Action-Commitment Control**

Compare the same trained FIRE policy under:

- DECISION_LEVEL: current 0.55 s re-decision cadence
- COMMIT_TO_COMPLETION: once a gather action is chosen, execute it until the corresponding resource increment completes, then ask the brain again

Primary question:
Does FIRE succeed when high-level gather actions are treated as temporally extended motor primitives?

No additional learning is required for the core commitment control.

Shared-brain memory/attention remains closed until this temporal-action boundary is resolved.
