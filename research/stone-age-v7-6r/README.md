# Stone Age V7.6R — Surprise-Corrected Representation Replication

Cadence: **0.88.1**

Status: **development replication complete**

Official classification:

`THRESHOLD_ENCODING_RESCUE_SURVIVES_SURPRISE`

## Question

Was V7.6's RAW18 failure substantially caused by normalized teaching without
`learning_surprise=True` from lesson 0, or does threshold encoding remain necessary
after applying Cadence 0.88.1's corrected teaching rule?

## Design

Fresh founders: `68001..68008`.

2×2 arms:

- `RAW18_CALM`
- `RAW18_SURPRISE`
- `CONTRAST18_CALM`
- `CONTRAST18_SURPRISE`

Everything else was frozen to V7.6:

- balanced one-vs-rest binary tasks
- 64 training rows/prototype
- 24 fresh rows/prototype
- modules `(32,16)`
- actions=2
- normalized one-row qualified teaching
- exact gate 90%
- fresh gate 80%

Additional diagnostics recorded accepted/agreed presentations and output dominance.

## Result

All **8/8 founders were valid**.

Median worst-classifier EXACT / FRESH:

| Skill | RAW18_CALM | RAW18_SURPRISE | CONTRAST18_CALM | CONTRAST18_SURPRISE |
| --- | --- | --- | --- | --- |
| FOOD | 50 / 50% | 65.6 / 68.8% | 100 / 100% | 100 / 100% |
| FIRE | 50 / 50% | 51.2 / 50.0% | 98.4 / 97.9% | 99.6 / 99.0% |
| HUNT | 65.6 / 66.7% | 89.1 / 90.6% | 97.3 / 95.8% | 100 / 100% |
| SHELTER | 75 / 75% | 52.7 / 54.2% | 99.6 / 100% | 99.2 / 100% |

Arm readiness:

- RAW18_CALM: fail
- RAW18_SURPRISE: fail
- CONTRAST18_CALM: pass
- CONTRAST18_SURPRISE: pass

## Founder-level robustness

All-four-skill readiness:

- RAW18_CALM: 0/8
- RAW18_SURPRISE: 0/8
- CONTRAST18_CALM: 3/8
- CONTRAST18_SURPRISE: **7/8**

Per-skill CONTRAST18_SURPRISE readiness:

- FOOD 8/8
- FIRE 7/8
- HUNT 8/8
- SHELTER 8/8

## Interpretation

Bernhard's 0.88.1 teaching correction matters, but it does not explain away the Stone Age representation result.

Surprise-from-lesson-0 clearly reduces some raw collapse:

- FOOD improves substantially.
- HUNT moves close to the exact gate and exceeds the fresh gate.
- output dominance falls strongly in those skills.

But RAW18 still fails the all-skill frozen criterion, with FIRE remaining near chance and SHELTER degrading under surprise.

By contrast, the threshold-coded representation remains acquisition-ready under the corrected teaching rule, and becomes substantially more robust founder-to-founder: 7/8 founders pass all four skills under `CONTRAST18_SURPRISE`.

This strengthens the original conclusion:

> Explicit action-relevant threshold state is still necessary for robust acquisition in this Stone Age microscope, even after correcting the normalized teaching rule.

The teaching-collapse confound was real and should be fixed in all future normalized long-curriculum work, but it was **not** the primary explanation for the V7.6 RAW18 vs CONTRAST18 gap.

## Boundary

V7.6R remains a binary static replication.

It does not yet establish:

- multiclass skill acquisition
- closed-loop action switching
- shared four-skill acquisition
- hidden-state memory
- attention or episodic-memory advantage

## Next direction

**Stone Age V7.7R — Surprise-Corrected Contrast Integration Bridge**

Use Cadence 0.88.1 and `learning_surprise=True` from lesson 0 for every normalized teaching arm.

Compare:

1. `RAW18_SURPRISE_FULL11`
2. `CONTRAST18_SURPRISE_FULL11`
3. `CONTRAST18_SURPRISE_LOCAL`

Measure:

- multiclass exact readback
- multiclass fresh generalization
- real closed-loop chain execution

If contrast + full 11-action output becomes ready, proceed to a shared four-skill contrast brain before reopening memory/attention.
