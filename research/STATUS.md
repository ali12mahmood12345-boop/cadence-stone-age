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

### Stone Age V7.10R — Replay Boundary Correction
`RESET_BOUNDARY_RECOVERY_RESCUE`

- 8/8 founders valid
- reset-matched replay restores all-skill median static readiness
- RESET_REPLAY REPLAY_FULL exact/fresh medians are 100/100 for FOOD/FIRE/HUNT/SHELTER
- FOOD/HUNT/SHELTER also retain 100% median loop success
- FIRE remains 0% median loop despite 100/100 static recovery
- current dominant boundary: FIRE dynamic trajectory invariance

## Active frozen experiment

### Stone Age V7.11 — FIRE Dynamic Invariance Microscope

FIRE only.

Fresh founders:
- 74001..74008

Representation arms:
- CONTRAST18
- FIRE_MINIMAL
- FIRE_MINIMAL_PLUS_PROGRESS

Common sequence:
- reset-per-row static bootstrap
- DAgger64
- reset-per-row full static replay
- exact/fresh/6-episode loop evaluation

FIRE_MINIMAL removes all nuisance dimensions and keeps only wood>=4, stone>=2 and fire_exists.

FIRE_MINIMAL_PLUS_PROGRESS additionally exposes current gather/craft action and normalized action_progress.

Environment sanity:
- direct deterministic caretaker must solve all 6 held-out FIRE episodes for every founder.

Primary question:
Does nuisance-invariant task state let the FIRE policy persist across the multiple consecutive decisions required to complete gathering, or is explicit action-progress state required?

See: [stone-age-v7-11](./stone-age-v7-11/README.md)

Shared-brain memory/attention remains closed until the FIRE dynamic boundary is resolved.
