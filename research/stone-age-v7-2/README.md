# Stone Age V7.2 — Acquisition Microscope

Cadence: **0.88.0**

Status: **development / running**

V7.1 accepted every teacher lesson but failed closed-loop acquisition. V7.2 isolates where that failure occurs.

## Matched branches

For every founder:

- FOOD-only brain
- FIRE-only brain
- HUNT-only brain
- SHELTER-only brain
- SHARED four-skill brain

For each skill, its single-skill brain and the shared brain receive **exactly the same teacher observation vectors and labels**. The shared brain differs only because it also learns the other skills.

Fresh founders: `62001..62008`.

## Probes after every curriculum stage

### EXACT
Greedy readback on the exact taught observation vectors.

### FRESH_STATIC
Greedy action on fresh jittered states with the same semantic meaning.

### CLOSED_LOOP
Actual StoneAgeEnv execution, where the first action changes inventory/body/world state and the policy must switch to the next action.

## Frozen mechanism thresholds

- exact readback good: >=90%
- fresh static good: >=80%
- closed loop good: >=2/3
- cross-skill interference gap: >=0.25

Possible global diagnoses:

- `STONE_AGE_BASIC_ACQUISITION_BOTTLENECK`
- `STONE_AGE_STATIC_GENERALIZATION_BOTTLENECK`
- `STONE_AGE_TRANSITION_SWITCH_BOTTLENECK`
- `STONE_AGE_CROSS_SKILL_INTERFERENCE_SIGNAL`
- `STONE_AGE_ACQUISITION_PIPELINE_HEALTHY`

No attention or episodic-memory comparison is opened in V7.2.
