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

- 8/8 founders valid.
- Skill-local outputs did not rescue all mappings.
- Binary one-vs-rest improved some FIRE/HUNT/SHELTER distinctions, but worst classifiers stayed below gate.
- Widening `(32,16)` to `(128,64)` did not rescue acquisition.
- Simple action competition and network width are not the primary bottleneck.

See: [stone-age-v7-5](./stone-age-v7-5/README.md)

## Running

### Stone Age V7.6 — State Separability / Representation Microscope

Fresh founders: `66001..66008`.

Frozen arms:
- RAW18
- CONTRAST18
- TASK_ONLY
- ORACLE_ONEHOT

All arms keep the same balanced binary one-vs-rest tasks, teaching route and module size.

Primary question: does explicit state representation rescue acquisition, and does pure prototype one-hot provide a healthy ceiling?

Attention/episodic-memory comparisons remain closed until static acquisition is solved.

See: [stone-age-v7-6](./stone-age-v7-6/README.md)
