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

### Stone Age V7.4 — Few-Lesson Teaching Regime Isolation
`PERSISTENT_FEW_LESSON_ACQUISITION_BOTTLENECK`

- 8/8 founders valid.
- FOUNDER_ROW did not rescue static acquisition.
- FOUNDER_BATCH32 did not rescue it.
- NORMALIZED_ROW reproduced the same partial-map pattern.
- NORMALIZED_BATCH32_E16 also plateaued despite much larger dose.
- Exact and fresh-static scores were effectively identical, arguing against a simple local-generalization problem.
- Persistent fractions were approximately:
  - FOOD 50%
  - FIRE 33.3%
  - HUNT 33–66.7%
  - SHELTER 43–66.7%

Interpretation: the next target is action competition/readout capacity, not teaching regime.

See: [stone-age-v7-4](./stone-age-v7-4/README.md)

## Next direction

**Stone Age V7.5 — Action-Competition / Readout Capacity Microscope**

Compare the same states under:
- full 11-action output
- skill-local action output
- one-vs-rest binary readouts
- optional wider capacity control

Attention/episodic-memory comparisons remain closed until static acquisition is solved.
