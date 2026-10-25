# Stone Age V7.4 — Few-Lesson Teaching Regime Isolation

Cadence: **0.88.0**

Status: **development complete**

Official classification:

`PERSISTENT_FEW_LESSON_ACQUISITION_BOTTLENECK`

## Question

Does the Cadence founder teaching point solve the short-budget Stone Age static acquisition problem that normalized teaching did not?

## Design

Fresh founders: `64001..64008`.

All arms used the same balanced single-skill Stone Age rows.

Arms:

- `FOUNDER_ROW`
- `FOUNDER_BATCH32`
- `NORMALIZED_ROW`
- `NORMALIZED_BATCH32_E16`

Primary evaluation used cold `brain.predict` on exact training rows and fresh static rows.

## Result

All **8/8 founders were valid**.

Final median EXACT / FRESH:

| Skill | FOUNDER_ROW | FOUNDER_BATCH32 | NORMALIZED_ROW | NORMALIZED_BATCH32_E16 |
| --- | --- | --- | --- | --- |
| FOOD | 50.0 / 50.0% | 50.0 / 50.0% | 50.0 / 50.0% | 50.0 / 50.0% |
| FIRE | 33.3 / 33.3% | 33.3 / 33.3% | 33.3 / 33.3% | 33.3 / 33.3% |
| HUNT | 33.3 / 33.3% | 33.3 / 33.3% | 66.7 / 66.7% | 66.7 / 66.7% |
| SHELTER | 66.7 / 66.7% | 43.5 / 44.4% | 66.7 / 66.7% | 66.7 / 66.7% |

No arm reached the frozen 90% exact / 80% fresh gate.

Founder teaching did not rescue acquisition.

The 16-epoch normalized batch dose also did not rescue acquisition.

## Key interpretation

Exact and fresh-static accuracies are nearly identical in every arm. That makes local generalization a poor explanation for the failure.

The dominant pattern is that each policy often retains only a subset of the competing prototype-to-action mappings:

- FOOD commonly retains one of PICK/EAT and loses the other.
- FIRE commonly retains only one of WOOD/STONE/CRAFT.
- HUNT normalized arms often retain two of three.
- SHELTER often retains two of three.

This persistence across founder vs normalized teaching, row vs batch updates, and a much larger normalized dose suggests the next microscope should target **readout capacity / action competition / mapping interference**, not teaching schedule.

## Next direction

**Stone Age V7.5 — Action-Competition / Readout Capacity Microscope**

Hold the same single-skill states fixed and vary only the action output problem:

1. full 11-action Stone Age output space,
2. skill-local output space (2 actions for FOOD, 3 for FIRE/HUNT/SHELTER),
3. one-vs-rest binary decisions for each prototype,
4. optionally wider module/readout capacity as a secondary control.

Primary question:

> Can Cadence retain all static mappings when irrelevant competing actions are removed?

If skill-local outputs jump to near-perfect while the full 11-action brain stays at 33–67%, the bottleneck is action competition/readout capacity rather than state encoding.

No attention/episodic-memory or hidden-state test should reopen yet.
