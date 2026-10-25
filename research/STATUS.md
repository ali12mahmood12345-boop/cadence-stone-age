# Cadence Research Status

Updated: 2026-10-25

## Confirmed

### Representation Keys V0.3D
Fresh confirmation on Cadence 0.85.1.

### Memory Keys V0.4B
Fresh confirmation on Cadence 0.85.1.

## Development boundary results

### Attention V0.5A
`NO_CONJUNCTIVE_MULTI_FACT_SIGNAL`

### Stone Age V7
`NO_STONE_AGE_MEMORY_ATTENTION_ADVANTAGE`

### Stone Age V7.1
`NO_STONE_AGE_ACQUISITION_READINESS`

### Stone Age V7.2
`STONE_AGE_BASIC_ACQUISITION_BOTTLENECK`

### Stone Age V7.3
`PERSISTENT_STATIC_ACQUISITION_BOTTLENECK`

### Stone Age V7.4
`PERSISTENT_FEW_LESSON_ACQUISITION_BOTTLENECK`

### Stone Age V7.5
`DEEPER_REPRESENTATION_ASSOCIATION_BOTTLENECK`

### Stone Age V7.6 — State Separability / Representation Microscope
`STONE_AGE_SENSOR_ENCODING_BOTTLENECK`

- 8/8 founders valid.
- ORACLE_ONEHOT passed all four skills at 100/100% median worst-classifier exact/fresh.
- CONTRAST18 also passed the all-skill readiness gate:
  - FOOD 100/100%
  - FIRE 100/100%
  - HUNT 98.0/97.9%
  - SHELTER 100/100%
- RAW18 failed:
  - FOOD 50/50%
  - FIRE 50/50%
  - HUNT 75/75%
  - SHELTER 75/75%
- TASK_ONLY did not pass all skills.
- Threshold encoding, not simple input removal, is the effective rescue.

Interpretation: the primary static acquisition bottleneck is the raw Stone Age sensory encoding of action-relevant threshold transitions.

See: [stone-age-v7-6](./stone-age-v7-6/README.md)

## Next direction

**Stone Age V7.7 — Contrast Encoding Integration Bridge**

Test contrast-encoded observations in multiclass single-skill acquisition and closed-loop chain execution, with RAW18 and skill-local controls.

If contrast + full 11-action output becomes acquisition-ready, proceed to a shared four-skill contrast brain before reopening hidden-state memory.

Attention/episodic-memory comparisons remain closed until the contrast representation is validated in the real multiclass chain.
