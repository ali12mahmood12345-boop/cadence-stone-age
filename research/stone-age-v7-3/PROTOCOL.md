# Frozen Protocol — Stone Age V7.3

Status: DEVELOPMENT.

Cadence:
- cadence-net==0.88.0

Fresh founders:
- 63001..63008
- minimum valid: 6/8

Skills:
- FOOD
- FIRE
- HUNT
- SHELTER

All brains are single-skill.

## Equal exposure

Every prototype within a skill receives exactly 64 training samples.

Fresh static evaluation uses 24 new samples per prototype.

The underlying original Stone Age observation rows are matched across all three arms.

## Arms

LEGACY_BALANCED
- normalized teaching
- one-row `Brain.lesson`
- reset before each lesson

DOC_BATCH32
- normalized teaching
- batch size 32
- `brain.learner.step(brain.stimulus(batch, memory=False), labels)`

DOC_BATCH32_CONTRAST
- same documented batch route
- same sample rows
- selected current-state features threshold encoded:
  - FOOD: carried food present
  - FIRE: wood>=4, stone>=2
  - HUNT: wood>=2, stone>=2, spear present
  - SHELTER: wood>=10, stone>=4, shelter present

## Primary evaluation

Cold graph:
- `brain.predict`
- exact training set
- fresh static held set

Frozen gates:
- exact >=90%
- fresh static >=80%

## Secondary evaluation

Three closed-loop StoneAgeEnv variants per skill.
Descriptive only; not used to choose the mechanism classification.

## Classification order

1. insufficient runs
2. LEGACY_BALANCED passes all skills -> BALANCED_EXPOSURE_RESCUE
3. DOC_BATCH32 passes all skills -> DOCUMENTED_BATCH_TEACHING_RESCUE
4. DOC_BATCH32_CONTRAST passes all skills -> STATE_CONTRAST_RESCUE
5. otherwise -> PERSISTENT_STATIC_ACQUISITION_BOTTLENECK

Do not change gates or arms after seeing results.
