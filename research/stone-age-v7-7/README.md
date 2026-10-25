# Stone Age V7.7 — Contrast Encoding Integration Bridge

Cadence: **0.88.0**

Status: **development / frozen before run**

V7.6 isolated the Stone Age static acquisition bottleneck to sensory encoding:
`CONTRAST18` passed all four balanced binary skills while `RAW18` failed.

V7.7 tests whether that fix survives real multiclass acquisition and closed-loop
state transitions.

## Arms

### RAW18_FULL11
- original 18-input observation
- original 11 actions
- control

### CONTRAST18_FULL11
- V7.6 threshold-coded 18-input observation
- original 11 actions
- primary integration arm

### CONTRAST18_LOCAL
- same threshold-coded observation
- only the 2–3 actions used by the current skill
- secondary action-competition control

## Training

All arms:
- separate single-skill brains
- normalized one-row qualified teaching
- modules `(32,16)`
- balanced V7.4–V7.6 prototype rows
- one pass

## Measurements

For every skill:
- exact multiclass cold predict
- fresh multiclass cold predict
- closed-loop StoneAgeEnv execution on 3 fresh variants

## Frozen gates

Per skill:
- exact >=90%
- fresh >=80%
- closed-loop >=2/3

Primary `CONTRAST18_FULL11` integration pass also requires at least **6/8**
founders to pass all four skills.

## Fresh founders

`67001..67008`

## Frozen interpretation

- full contrast passes all gates → `CONTRAST_FULL11_INTEGRATION_PASS`
- only local contrast passes → `CONTRAST_LOCAL_ONLY_INTEGRATION_PASS`
- full contrast static passes but loop fails → `CONTRAST_STATIC_RESCUE_CLOSED_LOOP_BOTTLENECK`
- otherwise → `NO_CONTRAST_MULTICLASS_INTEGRATION_RESCUE`

Run:

`START_STONE_AGE_V7_7.bat`
