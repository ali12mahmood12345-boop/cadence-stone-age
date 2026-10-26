# Stone Age V7.8 — Caretaker / DAgger Dynamic-State Bridge

Status: **running protocol / frozen before run**

Cadence: **0.88.1**

V7.7R established a clean boundary: `CONTRAST18 + learning_surprise=True + full11` reaches essentially perfect multiclass static exact/fresh accuracy, but FOOD, FIRE and SHELTER still fail in real closed-loop execution. HUNT is the positive control: the same full-11 contrast recipe already reaches 100% median closed-loop success.

## Question

Can caretaker correction on the **states the brain itself reaches** convert the V7.7R static policy into robust closed-loop execution without destroying static retention?

## Fixed base recipe

- cadence-net==0.88.1
- CONTRAST18
- full 11 actions
- modules `(32,16)`
- normalized qualified teaching
- `learning_surprise=True` from lesson 0
- same static bootstrap as V7.7R
- fresh founders `70001..70008`

## Arms

### STATIC_ONLY
Static bootstrap only. No dynamic teaching.

### SCRIPTED_EXPERT_TRAJECTORY
After the same static bootstrap:
- caretaker labels the current dynamic state
- teach that label
- execute the caretaker action
- continue along the clean expert trajectory

### CARETAKER_DAGGER
After the same static bootstrap:
- brain chooses greedy action on the current state
- caretaker labels that **same state**
- teach the caretaker label
- execute the brain's chosen action
- continue from the state produced by the brain's own path

This is the direct test of Bernhard's caretaker / DAgger suggestion.

## Matched dynamic supervision

Both dynamic-training arms receive exactly **128 labeled dynamic states per skill**.

This prevents DAgger from receiving more supervision merely because its mistakes create longer episodes.

## Deterministic caretaker

FOOD:
- food present -> EAT
- otherwise -> PICK_BERRIES

FIRE:
- wood < 4 -> GATHER_WOOD
- else stone < 2 -> GATHER_STONE
- else -> CRAFT_FIRE

HUNT:
- spear present -> HUNT_RABBIT
- else stone < 2 -> GATHER_STONE
- else wood < 2 -> GATHER_WOOD
- else -> CRAFT_SPEAR

SHELTER:
- shelter exists -> SLEEP
- else wood < 10 -> GATHER_WOOD
- else stone < 4 -> GATHER_STONE
- else -> BUILD_SHELTER

The caretaker is fixed before the run.

## Evaluation

After dynamic training, each arm is evaluated on:

1. static exact accuracy
2. static fresh accuracy
3. **6 fresh closed-loop episodes per skill**
4. accepted vs agreed dynamic teaching presentations
5. brain/caretaker agreement during dynamic training

## Frozen gates

Per skill:
- retained exact >=90%
- retained fresh >=80%
- closed-loop >=4/6

Primary DAgger integration requires:
- all four skill median gates pass
- >=6/8 valid founders individually pass all three gates on all four skills

## Frozen interpretation

- DAgger passes full criterion -> `CARETAKER_DAGGER_DYNAMIC_BRIDGE_PASS`
- expert trajectory passes but DAgger fails -> `EXPERT_TRAJECTORY_COVERAGE_ONLY`
- DAgger improves loop but damages static retention -> `DAGGER_RETENTION_TRADEOFF`
- neither dynamic arm rescues loop -> `DYNAMIC_STATE_TEACHING_INSUFFICIENT`

No shared four-skill brain, attention, episodic memory, hidden inventory or reward-learning comparison is opened in V7.8.
