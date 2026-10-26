# Stone Age V7.7R — Surprise-Corrected Contrast Integration Bridge

Status: **running protocol / frozen before run**

Cadence: **0.88.1**

V7.6R showed that `learning_surprise=True` from lesson 0 reduces some RAW18 collapse but does not remove the representation gap. `CONTRAST18_SURPRISE` remained acquisition-ready and passed all four binary skills in 7/8 founders.

## Arms

- `RAW18_SURPRISE_FULL11`
- `CONTRAST18_SURPRISE_FULL11`
- `CONTRAST18_SURPRISE_LOCAL`

All normalized teaching arms use `learning_surprise=True` from lesson 0, qualified teaching, modules `(32,16)`, one-row `Brain.lesson`, one pass.

RAW and CONTRAST full-11 use the same graph seed per founder/skill.

Fresh founders: `69001..69008`.

## Measurements

For FOOD, FIRE, HUNT and SHELTER:

- multiclass exact cold predict
- multiclass fresh cold predict
- closed-loop StoneAgeEnv execution on 3 fresh variants

## Frozen gates

Per skill:
- exact >=90%
- fresh >=80%
- closed-loop >=2/3

Primary `CONTRAST18_SURPRISE_FULL11` integration additionally requires >=6/8 founders to pass all three gates on all four skills.

## Frozen interpretation

- full contrast passes -> `SURPRISE_CONTRAST_FULL11_INTEGRATION_PASS`
- only local contrast passes -> `SURPRISE_CONTRAST_LOCAL_ONLY_INTEGRATION_PASS`
- full contrast static passes but loop fails -> `SURPRISE_CONTRAST_STATIC_RESCUE_CLOSED_LOOP_BOTTLENECK`
- otherwise -> `NO_SURPRISE_CONTRAST_MULTICLASS_INTEGRATION_RESCUE`
