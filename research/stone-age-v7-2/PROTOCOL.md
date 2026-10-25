# Frozen Protocol — Stone Age V7.2 Acquisition Microscope

Status: DEVELOPMENT.

Runtime:
- cadence-net==0.88.0

Fresh founders:
- 62001..62008
- minimum valid: 6/8

## Brain branches

Separate:
- FOOD-only
- FIRE-only
- HUNT-only
- SHELTER-only

Shared:
- one four-skill brain

All use:
- inputs=18
- actions=11
- modules=(32,16)
- normalized qualified teaching
- the exact V7.1 prototype generator and StoneAgeEnv mechanics

## Critical matching rule

For each founder, skill and stage, the single-skill and shared brains receive the exact same teacher observation vectors and labels.

The shared brain differs only because it also receives lessons from the other three skills.

## Curriculum

Frozen from V7.1:

1. terminal useful actions — 8 rounds
2. immediate predecessors — 8 rounds
3. resource-gap states — 12 rounds
4. mixed replay — 24 rounds

## Probes after every stage

EXACT:
- cumulative taught rows for that skill
- greedy act
- reset before each row

FRESH_STATIC:
- six fresh variants per cumulative prototype type
- greedy act
- reset before each row

CLOSED_LOOP:
- three fresh StoneAgeEnv variants per skill
- greedy act only
- no teacher
- no reward

## Frozen thresholds

- exact good >=90%
- fresh static good >=80%
- closed-loop good >=2/3
- interference gap >=0.25

Global classification order:

1. insufficient runs
2. basic acquisition bottleneck if any single-skill final exact median <90%
3. static generalization bottleneck if exact passes but any single fresh-static median <80%
4. transition-switch bottleneck if fewer than three single skills reach >=2/3 closed-loop
5. cross-skill interference if single acquisition works but shared drops >=0.25
6. acquisition pipeline healthy otherwise

Do not relax these thresholds after seeing V7.2.
