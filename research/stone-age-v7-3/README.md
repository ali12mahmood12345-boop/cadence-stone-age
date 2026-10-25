# Cadence Stone Age V7.3 — Balanced Teaching / State Contrast

V7.2 found a basic exact-acquisition bottleneck even in separate single-skill brains.

Before changing Cadence architecture, V7.3 tests three protocol explanations.

## New Cadence teaching detail

Cadence 0.88's teaching guide recommends `teaching="normalized"` with about **32 rows per lesson** for many-lesson imitation, and cold graph evaluation with `predict` / `accuracy`.

V7.1/V7.2 used one-row `brain.lesson()` calls.

V7.3 therefore compares three frozen arms on the **same underlying Stone Age samples**.

## Arms

### LEGACY_BALANCED

- equal sample count for every prototype
- one-row `brain.lesson()`
- normalized teaching

This tests whether the old terminal-action exposure imbalance was the main cause.

### DOC_BATCH32

- equal prototype exposure
- normalized teaching
- batches of 32
- `brain.learner.step(brain.stimulus(x, memory=False), labels)`

This follows the documented supervised-imitation route.

### DOC_BATCH32_CONTRAST

Same documented route, but only action-relevant inventory dimensions are threshold encoded:

- FOOD: food present / absent
- FIRE: enough wood / enough stone
- HUNT: enough spear materials / spear present
- SHELTER: enough shelter materials / shelter present

No new inputs are added.

## Primary metrics

Cold `brain.predict`:

- EXACT training rows
- FRESH_STATIC held rows

Closed-loop Stone Age execution is included only as a descriptive secondary panel.

## Fresh founders

`63001..63008`

## Frozen interpretation

- legacy passes all skills → `BALANCED_EXPOSURE_RESCUE`
- documented batch passes all skills → `DOCUMENTED_BATCH_TEACHING_RESCUE`
- only contrast passes all skills → `STATE_CONTRAST_RESCUE`
- otherwise → `PERSISTENT_STATIC_ACQUISITION_BOTTLENECK`
