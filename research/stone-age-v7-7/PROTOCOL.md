# Frozen Protocol — Stone Age V7.7

Status: DEVELOPMENT.

Cadence:
- cadence-net==0.88.0

Fresh founders:
- 67001..67008
- minimum valid: 6/8

Skills:
- FOOD
- FIRE
- HUNT
- SHELTER

Training rows:
- same balanced prototype generator used by V7.4–V7.6
- 64 training rows/prototype
- 24 fresh static rows/prototype

Teaching:
- teaching="normalized"
- qualified
- one-row Brain.lesson
- modules=(32,16)
- one pass

## Arms

RAW18_FULL11
- original observation
- actions=11

CONTRAST18_FULL11
- same 18 inputs
- FOOD: carried food present
- FIRE: wood>=4, stone>=2
- HUNT: wood>=2, stone>=2, spear present
- SHELTER: wood>=10, stone>=4, shelter present
- actions=11

CONTRAST18_LOCAL
- exact same contrast transformation
- only skill-local semantic actions:
  - FOOD 2
  - FIRE 3
  - HUNT 3
  - SHELTER 3

## Evaluation

Static:
- cold brain.predict exact
- cold brain.predict fresh

Closed loop:
- real StoneAgeEnv mechanics
- greedy brain.act
- no teacher
- no reward feedback
- 3 variants/skill

Gates:
- exact >=90%
- fresh >=80%
- loop >=2/3

Primary full integration:
- all four skill median gates pass
- >=6/8 valid founders individually pass all three gates on all four skills

## Classification

1. insufficient
2. CONTRAST18_FULL11 full integration -> CONTRAST_FULL11_INTEGRATION_PASS
3. CONTRAST18_LOCAL full integration -> CONTRAST_LOCAL_ONLY_INTEGRATION_PASS
4. CONTRAST18_FULL11 static all-skill pass -> CONTRAST_STATIC_RESCUE_CLOSED_LOOP_BOTTLENECK
5. CONTRAST18_LOCAL static all-skill pass -> CONTRAST_LOCAL_STATIC_RESCUE_ONLY
6. otherwise -> NO_CONTRAST_MULTICLASS_INTEGRATION_RESCUE

No post-hoc changes.
