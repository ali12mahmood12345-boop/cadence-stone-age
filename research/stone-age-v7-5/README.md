# Stone Age V7.5 — Action Competition / Readout Capacity Microscope

Cadence: **0.88.0**

Status: **development complete**

Official classification:

`DEEPER_REPRESENTATION_ASSOCIATION_BOTTLENECK`

## Question

Can Cadence retain the same static Stone Age state mappings when irrelevant competing action outputs are removed or readout capacity is increased?

## Design

Fresh founders: `65001..65008`.

Arms:

- `FULL11`: 11 Stone Age actions, modules `(32,16)`
- `SKILL_LOCAL`: only the 2–3 actions used by the current skill
- `BINARY_OVR`: balanced one-vs-rest binary classifier per prototype
- `WIDE_FULL11`: 11 actions, wider modules `(128,64)`

All arms used the same V7.4 balanced Stone Age observations and the same normalized one-row qualified teaching route.

Primary evaluation: cold `brain.predict` exact + fresh static.

## Result

All **8/8 founders were valid**.

Final median EXACT / FRESH:

| Skill | FULL11 | SKILL_LOCAL | BINARY_OVR minimum | WIDE_FULL11 |
| --- | --- | --- | --- | --- |
| FOOD | 50.0 / 50.0% | 50.0 / 50.0% | 50.0 / 50.0% | 50.0 / 50.0% |
| FIRE | 33.3 / 33.3% | 40.6 / 43.1% | 50.0 / 50.0% | 33.3 / 33.3% |
| HUNT | 50.0 / 50.0% | 66.7 / 66.7% | 50.0 / 50.0% | 33.3 / 33.3% |
| SHELTER | 66.7 / 66.7% | 66.7 / 66.7% | 75.0 / 75.0% | 66.7 / 66.7% |

No arm reached the frozen 90% exact / 80% fresh gate.

## What V7.5 rules out

### Not mainly irrelevant-action competition

Reducing the output space to only the skill-local actions improved some skills descriptively:

- FIRE local beat full in 5/8 founders, median exact gain +0.029
- HUNT local beat full in 5/8, median +0.174

But FOOD did not improve at all, and no skill-local arm reached the acquisition gate.

### Not mainly network width

The wider `(128,64)` full-11 brain did not rescue any skill.

Median gain over FULL11 was zero for FOOD, FIRE, and HUNT, and effectively zero for SHELTER.

### Binary separability is only partial

The balanced one-vs-rest probes improved some mappings:

- FIRE binary minimum beat FULL11 in 8/8 founders, median +0.167
- HUNT in 6/8, median +0.167
- SHELTER in 7/8, median +0.083

But the **worst binary classifier** still stayed below the frozen gate:

- FOOD 50%
- FIRE 50%
- HUNT 50%
- SHELTER 75%

So removing multiclass output competition is insufficient.

## Important prototype behavior

Some individual binary state distinctions are perfectly learnable, while neighboring distinctions collapse.

Examples include founders where:

- FIRE_STONE reaches 100% binary exact/fresh while FIRE_CRAFT or FIRE_WOOD collapses,
- HUNT_KILL reaches 100% while HUNT_STONE collapses,
- SHELTER_SLEEP reaches 100% while BUILD/WOOD are only partially separated.

This indicates that the Stone Age observation contains usable signal, but Cadence does not robustly associate every nearby state distinction with a separate learned action boundary under this teaching setup.

## Interpretation

V7.5 closes the simple action-count and network-width explanations.

The next mechanism to isolate is the **state representation / association boundary itself**.

We should not return to attention, episodic memory, hidden inventory, or shared-brain interference yet.

## Next direction

**Stone Age V7.6 — State Separability / Representation Microscope**

Use the exact same single-skill samples and binary tasks, then compare:

1. RAW18 — original Stone Age observation
2. CONTRAST18 — threshold-coded task-relevant inventory/state features
3. TASK_ONLY — only the task-relevant dimensions for that skill
4. ORACLE_ONEHOT — explicit prototype identity as a capacity ceiling

Primary evaluation remains balanced binary cold exact/fresh accuracy.

Interpretation:

- ORACLE_ONEHOT passes but RAW/CONTRAST fail → representation/association boundary is the problem
- CONTRAST/TASK_ONLY rescue RAW → Stone Age sensory encoding is the bottleneck
- even ORACLE_ONEHOT fails → deeper learner/association limitation
