# Cadence Stone Age V7.5 — Action Competition / Readout Capacity Microscope

Cadence: **0.88.0**

Status: **development / frozen before run**

V7.4 ruled out a simple teaching-regime explanation. Across founder/normalized, row/batch, and a much larger normalized dose, the same static Stone Age tasks retained only subsets of competing mappings.

V7.5 keeps the same balanced single-skill Stone Age states and changes only the output/readout problem.

## Arms

### FULL11
- original 11 Stone Age actions
- modules `(32,16)`

### SKILL_LOCAL
Only the actions used by the current skill:
- FOOD: 2
- FIRE: 3
- HUNT: 3
- SHELTER: 3

Same observations and semantic labels, remapped locally.

### BINARY_OVR
One balanced binary one-vs-rest classifier for every prototype/action.

This tests whether each state is separable when multiclass competition is removed.

### WIDE_FULL11
- original 11 actions
- modules `(128,64)`

This is a capacity control.

## Primary evaluation

Cold `brain.predict`:
- exact training rows
- fresh static rows

All arms use the same normalized one-row qualified teaching route.

## Fresh founders

`65001..65008`

## Frozen interpretation

- LOCAL + BINARY pass while FULL11 fails → `ACTION_COMPETITION_READOUT_SIGNAL`
- BINARY passes but LOCAL fails → `MULTICLASS_READOUT_COMPETITION_SIGNAL`
- WIDE_FULL11 passes → `FULL11_CAPACITY_RESCUE_SIGNAL`
- LOCAL alone passes → `LOCAL_OUTPUT_RESCUE_SIGNAL`
- otherwise → `DEEPER_REPRESENTATION_ASSOCIATION_BOTTLENECK`

Binary passes a skill only if the median founder's **minimum** prototype classifier reaches the exact/fresh gates.

Run:

`START_STONE_AGE_V7_5.bat`
