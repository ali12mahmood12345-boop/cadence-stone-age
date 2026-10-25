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

### Stone Age V7.5 — Action Competition / Readout Capacity
`DEEPER_REPRESENTATION_ASSOCIATION_BOTTLENECK`

- 8/8 founders valid.
- Skill-local outputs did not rescue all mappings.
- Binary one-vs-rest improved FIRE/HUNT/SHELTER descriptively but worst classifiers stayed at 50–75%.
- Wider `(128,64)` full-11 modules did not rescue acquisition.
- Exact and fresh-static results remained nearly identical.

Interpretation: simple action competition and network width are not the primary bottleneck. The next target is state representation / association separability.

See: [stone-age-v7-5](./stone-age-v7-5/README.md)

## Next direction

**Stone Age V7.6 — State Separability / Representation Microscope**

Keep the exact V7.5 binary tasks and compare:

- raw 18-input Stone Age observations
- threshold-contrast 18-input observations
- task-only relevant dimensions
- oracle prototype one-hot identity

This will distinguish Stone Age sensory encoding from a deeper Cadence learner/association limitation.

Attention/episodic-memory comparisons remain closed until static acquisition is solved.
