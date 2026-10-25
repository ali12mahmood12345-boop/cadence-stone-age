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

### Stone Age V7.6
`STONE_AGE_SENSOR_ENCODING_BOTTLENECK`

- CONTRAST18 passed all four binary skills.
- ORACLE_ONEHOT passed all four.
- RAW18 failed.
- Threshold encoding, not simple input removal, was the effective rescue.

See: [stone-age-v7-6](./stone-age-v7-6/README.md)

## Running

### Stone Age V7.7 — Contrast Encoding Integration Bridge

Fresh founders: `67001..67008`.

Frozen arms:
- RAW18_FULL11
- CONTRAST18_FULL11
- CONTRAST18_LOCAL

Measurements:
- multiclass exact readback
- fresh multiclass generalization
- closed-loop chain execution

Frozen gates per skill:
- exact >=90%
- fresh >=80%
- closed-loop >=2/3

Primary pass additionally requires >=6/8 founders ready on all four skills.

See: [stone-age-v7-7](./stone-age-v7-7/README.md)

Attention/episodic-memory comparisons remain closed until contrast encoding is validated in the multiclass closed-loop chain.
