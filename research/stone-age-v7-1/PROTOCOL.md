# Frozen Protocol — Stone Age V7.1 Acquisition Readiness

Status: DEVELOPMENT

Cadence:
- cadence-net==0.88.0

Fresh founders:
- 61001..61008
- minimum valid 6/8

Brain:
- inputs=18
- actions=11
- modules=(32,16)
- teaching="normalized"
- learning_qualified=True
- learning_damping=3
- learning_free_steps=1024
- learning_nudged_steps=1024
- learning_tolerance=0.003

No attention or episodic-memory comparison is opened in V7.1.

## Backward curriculum

Stage 1:
- EAT
- CRAFT_FIRE
- HUNT_RABBIT
- SLEEP

Stage 2:
- PICK_BERRIES -> EAT
- CRAFT_SPEAR -> HUNT_RABBIT
- BUILD_SHELTER -> SLEEP
- CRAFT_FIRE replay

Stage 3:
- missing wood/stone for fire
- missing stone for spear
- missing wood for shelter
- all earlier skills

Stage 4:
- balanced mixed replay

Rounds:
- 8 / 8 / 12 / 24

Every lesson begins after brain.reset().

## Strict exam

Three fresh variants per skill.

FOOD:
- hungry, beside berries, no carried food
- must pick then eat

FIRE:
- cold/evening, one resource short
- must gather then craft

HUNT:
- resources ready, rabbit nearby
- must craft spear then hunt

SHELTER:
- resources ready, low energy/night
- must build then sleep to >=88 energy

Exam:
- greedy brain.act only
- no teacher
- no reward feedback
- same scenarios for trained and untrained control

## Frozen gates

STONE_AGE_ACQUISITION_READINESS_SIGNAL requires:
- >=6 valid founders
- each skill median >=2/3
- overall median >=80%
- >=6 ready founders
- trained > untrained in >=6 founders
- median overall gain >=+0.40
