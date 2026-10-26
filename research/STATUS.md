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
Original `STONE_AGE_SENSOR_ENCODING_BOTTLENECK`; reopened after 0.88.1 corrected normalized-teaching guidance.

### Stone Age V7.6R
`THRESHOLD_ENCODING_RESCUE_SURVIVES_SURPRISE`

- 8/8 valid.
- RAW18_SURPRISE failed all-skill readiness.
- CONTRAST18_SURPRISE passed.
- Founder-level all-four readiness: CONTRAST surprise 7/8, RAW surprise 0/8.
- The 0.88.1 surprise correction reduces some raw collapse but does not remove the representation gap.

### Stone Age V7.7
Original 0.88.0/calm protocol superseded before run.

### Stone Age V7.7R — Surprise-Corrected Contrast Integration Bridge
`SURPRISE_CONTRAST_STATIC_RESCUE_CLOSED_LOOP_BOTTLENECK`

- cadence-net 0.88.1.
- 8/8 founders valid.
- learning_surprise=True from lesson 0 in every arm.
- CONTRAST18_SURPRISE_FULL11 median static exact/fresh:
  - FOOD 100/100%
  - FIRE 100/100%
  - HUNT 100/100%
  - SHELTER 100/100%
- Closed-loop medians for the same full-11 contrast arm:
  - FOOD 0%
  - FIRE 0%
  - HUNT 100%
  - SHELTER 0%
- CONTRAST18_SURPRISE_LOCAL static also passes all skills, but closed-loop remains mixed:
  - FOOD 16.7%
  - FIRE 33.3%
  - HUNT 0%
  - SHELTER 100%
- Founder-level all-four readiness:
  - RAW full11 0/8
  - CONTRAST full11 0/8
  - CONTRAST local 1/8

Interpretation: contrast encoding plus corrected teaching solves the tested multiclass static acquisition problem. The remaining boundary is dynamic intermediate-state coverage / trajectory stability, with unused-action competition as a secondary effect.

See: [stone-age-v7-7r](./stone-age-v7-7r/README.md)

## Next direction

**Stone Age V7.8 — Caretaker / DAgger Dynamic-State Bridge**

Bootstrap the successful CONTRAST18 + surprise + full11 policy, then teach on states the brain itself reaches in the real environment using a deterministic caretaker label.

Primary arms:
- STATIC_ONLY
- CARETAKER_DAGGER

Optional diagnostic:
- SCRIPTED_EXPERT_TRAJECTORY

Primary question: can on-path corrective teaching convert V7.7R's perfect static policy into robust closed-loop chain execution while retaining static accuracy?

Keep shared-brain memory/attention closed until this dynamic-state bridge is resolved.
