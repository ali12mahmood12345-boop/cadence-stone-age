# Cadence Stone Age V7.6 — State Separability / Representation Microscope

Cadence: **0.88.0**

Status: **development / frozen before run**

V7.5 showed that reducing action count and widening the network do not solve the static acquisition problem.

V7.6 keeps the same balanced binary tasks and changes only the state representation.

## Arms

### RAW18
Original 18-input Stone Age observation.

### CONTRAST18
Same 18 inputs, but task-relevant inventory/state thresholds are made explicit as 0/1 values.

### TASK_ONLY
Only the original dimensions relevant to the current skill are retained.

### ORACLE_ONEHOT
Pure one-hot prototype identity.

This is an explicit acquisition ceiling and is not an ecological Stone Age input.

## Teaching

All arms:
- `teaching="normalized"`
- one-row qualified `Brain.lesson`
- modules `(32,16)`
- actions=2
- one balanced one-vs-rest classifier per prototype

## Primary evaluation

Cold `brain.predict`:
- exact rows
- fresh static rows

A skill is judged by its **worst binary prototype classifier**.

## Fresh founders

`66001..66008`

## Frozen interpretation

- RAW passes all → `RAW18_BINARY_SEPARABILITY_HEALTHY`
- ORACLE fails → `SUPERVISED_ASSOCIATION_CEILING_FAILURE`
- ORACLE passes + CONTRAST/TASK_ONLY rescue RAW → `STONE_AGE_SENSOR_ENCODING_BOTTLENECK`
- ORACLE passes but simplified sensory arms fail → `SIMPLIFIED_STATE_ASSOCIATION_BOTTLENECK`

Run:

`START_STONE_AGE_V7_6.bat`
