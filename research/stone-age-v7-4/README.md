# Cadence Stone Age V7.4 — Few-Lesson Teaching Regime Isolation

Cadence: **0.88.0**

Status: **development / frozen before run**

V7.3 showed a persistent static acquisition bottleneck, but also exposed a protocol mismatch:

Cadence 0.88's teaching guide says the **founder teaching point acquires faster with a few hundred corrections**, while `teaching="normalized"` is aimed at many-lesson imitation.

Our balanced Stone Age static datasets contain only 128–192 rows per skill.

V7.4 therefore keeps the **same balanced single-skill datasets** and changes only the teaching regime.

## Arms

### FOUNDER_ROW
- `teaching="founder"`
- one-row `Brain.lesson`
- one pass

### FOUNDER_BATCH32
- `teaching="founder"`
- 32-row direct learner batches
- one pass

### NORMALIZED_ROW
- `teaching="normalized"`
- one-row `Brain.lesson`
- one pass
- direct control for the V7.3 legacy-balanced route

### NORMALIZED_BATCH32_E16
- `teaching="normalized"`
- batch size 32
- 16 shuffled epochs
- explicit dose control for the weak 4–6 update V7.3 batch arm

## Primary evaluation

Cold `brain.predict` only:

- exact balanced training rows
- fresh held static rows

No state contrast, closed-loop success gate, attention, episodic memory, reward learning, hidden inventory, or shared-brain interference.

## Fresh founders

`64001..64008`

## Frozen interpretation

- founder row passes all skills → `FOUNDER_FEW_LESSON_TEACHING_RESCUE`
- else founder batch passes all → `FOUNDER_BATCH_TEACHING_RESCUE`
- else repeated normalized batch passes all → `NORMALIZED_BATCH_DOSE_RESCUE`
- otherwise → `PERSISTENT_FEW_LESSON_ACQUISITION_BOTTLENECK`

Run:

`START_STONE_AGE_V7_4.bat`
