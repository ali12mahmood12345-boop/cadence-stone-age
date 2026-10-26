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
Frozen-run classification:
`STATIC_POLICY_NOT_RECOVERABLE_BY_ONE_PASS`

Interpretation reopened after runner audit because replay did not reset before independent static rows.

### Stone Age V7.10R — Replay Boundary Correction
`RESET_BOUNDARY_RECOVERY_RESCUE`

- cadence-net 0.88.1
- 8/8 founders valid
- exact post-DAGGER branch matched before reset/no-reset replay split
- only branch difference: `brain.reset()` before each RESET_REPLAY lesson
- RESET_REPLAY static all-skill median readiness recovered by REPLAY64
- RESET_REPLAY REPLAY_FULL median exact/fresh:
  - FOOD 100/100%
  - FIRE 100/100%
  - HUNT 100/100%
  - SHELTER 100/100%
- CONTINUING_REPLAY REPLAY_FULL median exact/fresh:
  - FOOD 95.7/93.8%
  - FIRE 33.3/33.3%
  - HUNT 66.7/66.7%
  - SHELTER 66.7/66.7%
- RESET_REPLAY mean median retention at REPLAY_FULL = 1.000
- 7/8 founders recover all-four static exact/fresh gates under RESET_REPLAY REPLAY_FULL
- full all-four readiness remains 0/8 because FIRE loop remains below gate in every founder
- RESET_REPLAY REPLAY_FULL median loops:
  - FOOD 100%
  - FIRE 0%
  - HUNT 100%
  - SHELTER 100%

Interpretation:
V7.10's apparent static irrecoverability was primarily a replay-boundary/context artifact. Static knowledge is recoverable after DAgger64 when replay uses the same reset boundary as the original cold curriculum.

Current dominant boundary:
**FIRE dynamic trajectory invariance.**

See: [stone-age-v7-10r](./stone-age-v7-10r/README.md)

## Next direction

**Stone Age V7.11 — FIRE Dynamic Invariance Microscope**

FIRE-only representation comparison:

- CONTRAST18
- FIRE_MINIMAL
- FIRE_MINIMAL_PLUS_PROGRESS

Question:
Does removing changing nuisance state allow the learned FIRE policy to persist across the multiple consecutive gather decisions, or is explicit action-progress state required?

Shared-brain memory/attention remains closed until the FIRE dynamic boundary is resolved.
