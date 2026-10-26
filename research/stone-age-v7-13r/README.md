# Stone Age V7.13R — Fresh FIRE Boundary Confirmation

Status: **confirmation protocol / frozen before run**

Cadence: **0.88.1**

V7.13 development established a successful FIRE controller recipe:

1. FIRE_MINIMAL visible task state
2. commit GATHER_WOOD / GATHER_STONE until the immediate resource increment completes
3. call `brain.reset()` before the next semantic high-level query

The V7.13 development panel reached 8/8 founder readiness under that recipe.

V7.13R is a strict fresh confirmation. No mechanism or recipe changes are allowed.

## Question

Does the exact V7.13 FIRE recipe reproduce on a larger untouched founder panel?

## Fresh founder panel

`77001..77016`

- 16 founders total
- minimum valid: 12/16
- confirmation readiness threshold: 12/16 individually ready

## Frozen representation

`FIRE_MINIMAL` only.

18-wide vector:
- input 5 = `wood >= 4`
- input 6 = `stone >= 2`
- input 9 = `fire_exists`
- all other inputs = 0

## Frozen training

Exactly the V7.13 recipe:

1. reset before every independent static bootstrap row
2. DAgger64 learner-path teaching
3. one full 192-row reset-matched static replay pass
4. freeze final brain
5. no learning during confirmation evaluation

Architecture:
- full 11 actions
- modules `(32,16)`
- normalized qualified teaching
- `learning_surprise=True` from lesson 0

## Frozen controller

At every semantic high-level query:

1. call `brain.reset()`
2. query the FIRE_MINIMAL brain
3. if `GATHER_WOOD`, hold it until wood increases
4. if `GATHER_STONE`, hold it until stone increases
5. otherwise execute one normal decision window
6. repeat until success/death/shared episode budget

Environment budget:
- 14 total decision windows

No extra world time is introduced by commitment.

## Evaluation

For every founder:

- exact static accuracy
- fresh static accuracy
- 6 held-out FIRE episodes
- ready-to-craft boundary accuracy
- high-level query count
- total decision windows
- primitive lengths
- full failure traces

Environment validity:
- deterministic caretaker must solve 6/6 held-out FIRE episodes

## Frozen confirmation gates

Run-level validity:
- at least 12/16 valid founders

Median gates:
- exact >=90%
- fresh >=80%
- loop >=4/6
- ready-to-craft accuracy = 100%

Founder-level confirmation:
- at least 12/16 valid founders individually satisfy:
  - exact >=90%
  - fresh >=80%
  - loop >=4/6

## Frozen classification

1. valid founders <12 -> `INSUFFICIENT_V7_13R_RUNS`
2. all median gates pass and >=12/16 founders individually ready -> `FIRE_STREAM_STATE_RESET_CONFIRMED`
3. otherwise -> `FIRE_STREAM_STATE_RESET_NOT_CONFIRMED`

No new representation, no alternate controller mode, no new teaching schedule, and no post-hoc gate changes.
