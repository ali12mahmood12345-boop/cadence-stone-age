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

- temporal commitment materially improves FIRE_MINIMAL for a subset of founders
- median FIRE_MINIMAL loop 0% -> 50%
- only 3/8 founders commit-ready
- remaining failures usually occur after gather completion at the semantic transition to CRAFT_FIRE
- cold FIRE_MINIMAL static readout remains 100/100

Current dominant boundary:
**per-stream state / hysteresis across semantic action boundaries.**

## Active frozen experiment

### Stone Age V7.13 — FIRE Semantic Boundary Reset Control

FIRE only.

Fresh founders:
- 76001..76008

Representation:
- FIRE_MINIMAL

Training:
- same V7.12 static bootstrap / DAgger64 / full reset replay

Final frozen brain comparison:
- COMMIT_CONTINUING
- COMMIT_RESET_QUERY

Only difference:
- COMMIT_RESET_QUERY calls `brain.reset()` immediately before every high-level action query.

Both modes:
- same 14 decision-window budget
- same seeds/variants
- same gather commitment rule
- no extra learning

Primary question:
Does clearing stream state at primitive boundaries restore the correct CRAFT_FIRE transition after gathering completes?

See: [stone-age-v7-13](./stone-age-v7-13/README.md)

Shared-brain memory/attention remains closed until this control is resolved.
