# Frozen Protocol — Stone Age V7.5

Status: DEVELOPMENT.

Cadence:
- cadence-net==0.88.0

Fresh founders:
- 65001..65008
- minimum valid 6/8

Skills:
- FOOD
- FIRE
- HUNT
- SHELTER

Dataset:
- same balanced V7.4 generator
- 64 training rows/prototype
- 24 fresh rows/prototype
- original 18-input Stone Age observations

Teaching:
- teaching="normalized"
- qualified
- one-row Brain.lesson
- one pass
- same route for every arm

## Arms

FULL11
- actions=11
- modules=(32,16)

SKILL_LOCAL
- actions equal number of unique semantic actions in the current skill
- FOOD=2, FIRE/HUNT/SHELTER=3
- modules=(32,16)
- same observations, target labels remapped locally

BINARY_OVR
- one actions=2 brain per prototype
- positive = target prototype
- negative = evenly sampled other prototypes
- exactly balanced 50/50 positive/negative
- modules=(32,16)
- report minimum and median binary accuracy across prototype classifiers

WIDE_FULL11
- actions=11
- modules=(128,64)

## Primary evaluation

Cold brain.predict:
- exact training rows
- fresh static rows

Gates:
- exact >=90%
- fresh >=80%

Binary arm passes a skill only if the median founder's MINIMUM prototype classifier meets both gates.

## Classification

1. insufficient
2. FULL11 all skills pass -> FULL11_STATIC_ACQUISITION_HEALTHY
3. LOCAL + BINARY all skills pass -> ACTION_COMPETITION_READOUT_SIGNAL
4. BINARY all skills pass -> MULTICLASS_READOUT_COMPETITION_SIGNAL
5. WIDE_FULL11 all skills pass -> FULL11_CAPACITY_RESCUE_SIGNAL
6. LOCAL all skills pass -> LOCAL_OUTPUT_RESCUE_SIGNAL
7. otherwise -> DEEPER_REPRESENTATION_ASSOCIATION_BOTTLENECK

No post-hoc changes.
