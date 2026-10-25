# Frozen Protocol — Stone Age V7.4

Status: DEVELOPMENT.

Cadence:
- cadence-net==0.88.0

Fresh founders:
- 64001..64008
- minimum valid 6/8

Skills:
- FOOD
- FIRE
- HUNT
- SHELTER

Datasets:
- same balanced single-skill Stone Age prototype generator as V7.3
- 64 training samples per prototype
- 24 fresh static samples per prototype
- same underlying rows across all arms

## Arms

FOUNDER_ROW
- teaching="founder"
- qualified teaching
- one-row Brain.lesson
- one pass

FOUNDER_BATCH32
- teaching="founder"
- qualified teaching
- learner.step(stimulus(memory=False), labels)
- batch size 32
- one pass

NORMALIZED_ROW
- teaching="normalized"
- qualified teaching
- one-row Brain.lesson
- one pass

NORMALIZED_BATCH32_E16
- teaching="normalized"
- qualified teaching
- learner.step(stimulus(memory=False), labels)
- batch size 32
- 16 shuffled epochs

The repeated normalized batch arm is deliberately a DOSE control and is not matched
for sample presentations.

## Primary evaluation

Cold graph:
- brain.predict exact rows
- brain.predict fresh static rows

Frozen gates:
- exact >=90%
- fresh >=80%

## Classification

1. insufficient
2. FOUNDER_ROW passes all skills -> FOUNDER_FEW_LESSON_TEACHING_RESCUE
3. FOUNDER_BATCH32 passes all -> FOUNDER_BATCH_TEACHING_RESCUE
4. NORMALIZED_BATCH32_E16 passes all -> NORMALIZED_BATCH_DOSE_RESCUE
5. NORMALIZED_ROW passes all -> NORMALIZED_ROW_RESCUE
6. otherwise -> PERSISTENT_FEW_LESSON_ACQUISITION_BOTTLENECK

No post-hoc changes.
