# Stone Age V7.15R — Fresh Autonomous Goal Routing Confirmation

Status: **confirmation protocol / frozen before run**

Cadence: **0.88.1**

V7.15C produced a successful autonomous goal-routing bridge after correcting only the tasked-control terminal/tool observation adapter.

V7.15R is a strict fresh confirmation of that corrected setup.

## Question

Does the V7.15C autonomous goal-routing bridge reproduce on a larger untouched founder panel with no recipe changes?

## Fresh founders

`82001..82016`

- 16 founders total
- minimum valid: 12/16
- autonomous confirmation threshold: 12/16 ready
- corrected tasked-control threshold: 12/16 all-scenario ready

## Frozen arms

### AUTONOMOUS_GLOBAL

Unchanged from V7.15/V7.15C:
- no external FOOD/FIRE/HUNT/SHELTER task label
- same 18-wide global semantic representation
- same 26 canonical semantic keys
- same caretaker priority: hunger > fire/warmth > sleep > explore
- 64 presentations/key bootstrap
- DAgger64 per scenario family
- full reset-matched semantic replay
- same eight scenarios and budgets
- same semantic motor primitives
- brain.reset() before each high-level query

### TASKED_SHARED_CONTROL

Unchanged from corrected V7.15C:
- exact V7.14 shared executor recipe
- explicit task one-hot
- same 16 canonical task keys
- same bootstrap / DAgger64 / replay
- same canonicalized oracle-routed adapter:
  - HUNT + has_spear -> canonical HUNT_HAS_SPEAR
  - SHELTER + shelter_exists -> canonical SHELTER_EXISTS

Both arms start as deep copies of the same untrained base brain per founder.

## Evaluation

AUTONOMOUS_GLOBAL:
- STATIC_ONLY
- POST_DAGGER64
- POST_REPLAY_FULL
- overall 26-key static accuracy
- routed FOOD/HUNT/FIRE/SHELTER/NEUTRAL static accuracy
- six held-out episodes for each of:
  - FORAGE
  - HUNT_EAT
  - FIRE_COLD
  - FIRE_EVENING
  - SHELTER_SLEEP
  - FOOD_THEN_FIRE
  - HUNT_THEN_SLEEP
  - ALL_NEEDS
- caretaker agreement
- founder autonomous readiness

TASKED_SHARED_CONTROL:
- standard V7.14 four-skill static/loop exam
- same eight autonomous scenarios with oracle routing
- founder all-scenario readiness

## Frozen gates

Run validity:
- >=12/16 valid founders

AUTONOMOUS_GLOBAL:
- overall static median >=90%
- FOOD/HUNT/FIRE/SHELTER static medians >=90%
- all eight scenario medians >=4/6
- >=12/16 founders autonomous-ready

TASKED_SHARED_CONTROL:
- all four standard skill median static/loop gates pass
- all eight corrected oracle-routed scenario medians >=4/6
- >=12/16 founders corrected all-scenario ready

## Frozen classification

1. valid founders <12 -> `INSUFFICIENT_V7_15R_RUNS`
2. corrected tasked control unstable -> `TASKED_CONTROL_NOT_CONFIRMED`
3. all confirmation gates pass -> `AUTONOMOUS_GOAL_ROUTING_CONFIRMED`
4. autonomous routed static gates fail -> `AUTONOMOUS_ROUTING_ACQUISITION_NOT_CONFIRMED`
5. autonomous static passes but dynamic/scenario confirmation fails -> `AUTONOMOUS_DYNAMIC_ROUTING_NOT_CONFIRMED`
6. otherwise -> `AUTONOMOUS_GOAL_ROUTING_NOT_CONFIRMED`

No attention.
No episodic memory.
No reward learning.
No Cadence 0.89.0 positional recall.
No post-hoc changes.
