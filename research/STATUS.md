# Cadence Research Status

Updated: 2026-10-27

## Confirmed

### Representation Keys V0.3D
Fresh confirmation on Cadence 0.85.1.

### Memory Keys V0.4B
Fresh confirmation on Cadence 0.85.1.

### Stone Age V7.13R
`FIRE_STREAM_STATE_RESET_CONFIRMED`

### Stone Age V7.14R
`FOUR_SKILL_SHARED_SEMANTIC_BRIDGE_CONFIRMED`

Fresh confirmation:
- 16/16 valid founders
- caretaker oracle 384/384
- SHARED all-four readiness 16/16
- CONTROL all-four readiness 16/16
- every final shared/control static and loop score 100%
- explicit task identity remains part of the confirmed representation
- semantic replay reconsolidates the policy after DAgger

## Active development experiment

### Stone Age V7.15 — Autonomous Goal Routing Bridge

Fresh founders:
- 80001..80008

Question:
Can one shared Cadence brain choose the appropriate Stone Age goal from global semantic world/need state instead of receiving an external FOOD/FIRE/HUNT/SHELTER task label?

Arms:
- AUTONOMOUS_GLOBAL
- TASKED_SHARED_CONTROL

AUTONOMOUS_GLOBAL:
- no task one-hot
- global semantic need/opportunity/resource representation
- 26 frozen semantic keys
- frozen caretaker priority: hunger > fire/warmth > sleep > explore
- 64 presentations/key bootstrap
- DAgger64 on each of 8 autonomous scenario families
- full reset semantic replay
- confirmed motor primitives + stream reset

TASKED_SHARED_CONTROL:
- starts from the same untrained base brain
- exact V7.14 shared recipe
- oracle supplies goal during the autonomous scenario exam
- isolates goal routing from executor stability

Autonomous scenarios:
- FORAGE
- HUNT_EAT
- FIRE_COLD
- FIRE_EVENING
- SHELTER_SLEEP
- FOOD_THEN_FIRE
- HUNT_THEN_SLEEP
- ALL_NEEDS

Primary pass:
- controls stable
- autonomous routed static medians pass
- all 8 autonomous scenario medians >=4/6
- >=6/8 autonomous founders pass every static and scenario gate

No attention, episodic memory or reward-learning arm.

See: [stone-age-v7-15](./stone-age-v7-15/README.md)
