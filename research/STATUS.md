# Cadence Research Status

Updated: 2026-10-26

## Confirmed

### Representation Keys V0.3D
Fresh confirmation on Cadence 0.85.1.

### Memory Keys V0.4B
Fresh confirmation on Cadence 0.85.1.

## Development boundary results

### Attention V0.5A
Original held split was underdetermined; behavioral conjunction conclusion retired.
Retrieval evidence remains informative. V0.5B / PR #1 provides an identifiable held split.

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
Original classification `STONE_AGE_SENSOR_ENCODING_BOTTLENECK`, subsequently reopened because 0.88.1 corrected normalized-teaching guidance.

### Stone Age V7.6R — Surprise-Corrected Representation Replication
`THRESHOLD_ENCODING_RESCUE_SURVIVES_SURPRISE`

- Cadence 0.88.1.
- 8/8 founders valid.
- Surprise enabled from lesson 0 in corrected arms.
- RAW18_SURPRISE still failed all-skill readiness.
- CONTRAST18_SURPRISE passed all-skill median readiness.
- Founder-level all-four readiness:
  - RAW18_CALM 0/8
  - RAW18_SURPRISE 0/8
  - CONTRAST18_CALM 3/8
  - CONTRAST18_SURPRISE **7/8**
- Median CONTRAST18_SURPRISE worst-classifier exact/fresh:
  - FOOD 100/100%
  - FIRE 99.6/99.0%
  - HUNT 100/100%
  - SHELTER 99.2/100%
- Surprise materially reduced raw collapse in some skills, especially FOOD and HUNT, but did not remove the raw-vs-threshold representation gap.

Interpretation: the 0.88.1 teaching correction is important and must be used going forward, but the threshold-encoding rescue remains robust under that corrected rule.

See: [stone-age-v7-6r](./stone-age-v7-6r/README.md)

### Stone Age V7.7
Original 0.88.0/calm protocol superseded before run by the 0.88.1 teaching correction.

## Next direction

**Stone Age V7.7R — Surprise-Corrected Contrast Integration Bridge**

Cadence 0.88.1, `learning_surprise=True` from lesson 0.

Compare:
- RAW18_SURPRISE_FULL11
- CONTRAST18_SURPRISE_FULL11
- CONTRAST18_SURPRISE_LOCAL

Measure multiclass exact/fresh plus real closed-loop chain execution.

If contrast + full11 passes, proceed to shared four-skill contrast acquisition before reopening hidden-state memory or attention.

## Active experiment

### Stone Age V7.7R — Surprise-Corrected Contrast Integration Bridge

Protocol frozen before run.

- Cadence 0.88.1
- fresh founders 69001..69008
- learning_surprise=True from lesson 0 in every arm
- RAW-vs-CONTRAST full11 seed matched
- multiclass exact/fresh + real closed-loop execution
- primary contrast full11 requires exact>=90%, fresh>=80%, loop>=2/3 and >=6/8 all-four-ready founders

See: [stone-age-v7-7r](./stone-age-v7-7r/README.md)
