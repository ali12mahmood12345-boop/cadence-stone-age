# Frozen Protocol — Stone Age V7.13R

Status: CONFIRMATION / frozen before run.

Cadence:
- cadence-net==0.88.1

Fresh founders:
- 77001..77016
- 16 total
- minimum valid 12
- confirmation requires >=12 individually ready

Scope:
- FIRE only
- strict replication of successful V7.13 recipe

Representation:
- FIRE_MINIMAL
- input5 = wood>=4
- input6 = stone>=2
- input9 = fire_exists
- all other inputs zero

Architecture:
- actions=11
- modules=(32,16)
- teaching="normalized"
- learning_surprise=True from lesson 0
- qualified teaching

Training:
1. reset before every independent static bootstrap row
2. DAgger64 learner-path teaching
3. full 192-row reset-matched static replay
4. freeze final brain
5. no learning during confirmation evaluation

Controller:
- call brain.reset() before every high-level query
- query FIRE_MINIMAL brain
- hold GATHER_WOOD until wood increases
- hold GATHER_STONE until stone increases
- all other actions execute one ordinary decision window
- max 14 total decision windows

Evaluation:
- exact static
- fresh static
- 6 held-out FIRE episodes
- ready-to-craft boundary accuracy
- high-level query count
- decision-window count
- primitive lengths
- failure traces

Environment oracle:
- deterministic caretaker must solve 6/6 held-out episodes per founder

Founder-ready:
- exact >=90%
- fresh >=80%
- loop >=4/6

Confirmation gates:
- >=12 valid founders
- median exact >=90%
- median fresh >=80%
- median loop >=4/6
- median ready-to-craft accuracy ==100%
- >=12/16 valid founders individually ready

Classification:
1. valid <12 -> INSUFFICIENT_V7_13R_RUNS
2. all confirmation gates pass -> FIRE_STREAM_STATE_RESET_CONFIRMED
3. otherwise -> FIRE_STREAM_STATE_RESET_NOT_CONFIRMED

No alternate arms.
No mechanism changes.
No post-hoc changes.
