# Stone Age V7.6 — State Separability / Representation Microscope

Cadence: **0.88.0**

Status: **development complete**

Official classification:

`STONE_AGE_SENSOR_ENCODING_BOTTLENECK`

## Question

Do Stone Age binary acquisition failures come from the raw sensory representation, or does Cadence still fail even when prototype identity is made explicit?

## Design

Fresh founders: `66001..66008`.

Arms:

- `RAW18`: original 18-input Stone Age observation
- `CONTRAST18`: same 18 inputs with action-relevant thresholds made explicit
- `TASK_ONLY`: only task-relevant original dimensions
- `ORACLE_ONEHOT`: explicit prototype identity ceiling

All arms used the same balanced binary one-vs-rest tasks, normalized one-row qualified teaching, modules `(32,16)`, and cold exact/fresh evaluation.

## Result

All **8/8 founders were valid**.

Median worst-classifier EXACT / FRESH:

| Skill | RAW18 | CONTRAST18 | TASK_ONLY | ORACLE_ONEHOT |
| --- | --- | --- | --- | --- |
| FOOD | 50 / 50% | 100 / 100% | 100 / 100% | 100 / 100% |
| FIRE | 50 / 50% | 100 / 100% | 50 / 50% | 100 / 100% |
| HUNT | 75 / 75% | 98.0 / 97.9% | 89.5 / 86.5% | 100 / 100% |
| SHELTER | 75 / 75% | 100 / 100% | 75 / 75% | 100 / 100% |

Arm readiness:

- RAW18: fail
- CONTRAST18: **pass**
- TASK_ONLY: fail
- ORACLE_ONEHOT: **pass**

## Interpretation

The supervised association ceiling is healthy: ORACLE_ONEHOT reached 100% on every skill.

The decisive result is that **CONTRAST18 also passes the all-skill readiness gate without adding inputs**.

This isolates the primary bottleneck to the raw Stone Age sensory encoding of important threshold transitions.

Simply removing irrelevant dimensions was not sufficient:

- FOOD task-only passed.
- HUNT task-only improved strongly but remained just below the exact gate.
- FIRE and SHELTER task-only did not rescue the worst classifier.

That pattern shows the useful intervention is not merely dimensionality reduction; it is making threshold state changes explicit.

The relevant contrast features were:

- FOOD: carried food present
- FIRE: wood>=4 and stone>=2
- HUNT: wood>=2, stone>=2, spear present
- SHELTER: wood>=10, stone>=4, shelter present

## Boundary

V7.6 is still a **binary static development assay**.

It does not yet prove that contrast encoding rescues:

- multiclass skill acquisition,
- closed-loop action switching,
- shared four-skill acquisition,
- hidden-inventory memory,
- attention or episodic memory.

## Next direction

**Stone Age V7.7 — Contrast Encoding Integration Bridge**

Use the same transformed 18-input observation dynamically and test:

1. RAW18 + full 11-action single-skill control
2. CONTRAST18 + full 11-action single-skill brain
3. CONTRAST18 + skill-local output control

Measure:

- exact multiclass readback
- fresh static multiclass generalization
- closed-loop chain execution

If CONTRAST18 + FULL11 becomes acquisition-ready, proceed to a shared four-skill contrast brain before reopening hidden-state memory.

If only CONTRAST18 + skill-local passes, action competition remains a secondary bottleneck after sensory encoding is fixed.
