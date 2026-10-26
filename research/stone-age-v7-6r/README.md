# Stone Age V7.6R — Surprise-Corrected Representation Replication

Cadence: **0.88.1**

Status: **development replication / frozen before run**

## Why this rerun exists

Stone Age V7.6 found a strong representation result:

- RAW18 failed the balanced binary acquisition gate.
- CONTRAST18 passed all four skills.
- ORACLE_ONEHOT passed all four skills.

After V7.6, Cadence 0.88.1 corrected the normalized-teaching guidance for long row-by-row curricula.

The corrected recipe is:

`learning_surprise=True` **from the first lesson**.

Without it, normalized teaching can continue updating already-correct rows until the readout collapses onto one action.

Therefore the V7.6 sensory-encoding diagnosis is provisional until RAW18 and CONTRAST18 are compared under the corrected rule.

## Frozen 2×2 arms

### RAW18_CALM
- original 18-input Stone Age observation
- `teaching="normalized"`
- `learning_surprise=False`

### RAW18_SURPRISE
- original observation
- `teaching="normalized"`
- `learning_surprise=True` from lesson 0

### CONTRAST18_CALM
- exact V7.6 threshold encoding
- normalized teaching
- surprise disabled

### CONTRAST18_SURPRISE
- exact V7.6 threshold encoding
- normalized teaching
- surprise enabled from lesson 0

## Everything else stays frozen

- fresh founders `68001..68008`
- balanced one-vs-rest binary tasks
- 64 training rows/prototype
- 24 fresh rows/prototype
- modules `(32,16)`
- actions=2
- one-row `Brain.lesson`
- one pass
- exact gate >=90%
- fresh gate >=80%

Additional diagnostics:

- accepted presentations
- agreed/skipped presentations
- output dominance

## Frozen interpretation

If RAW surprise passes all skills while RAW calm fails:

`NORMALIZED_TEACHING_COLLAPSE_CONFOUNDED_RAW18`

If RAW surprise still fails while CONTRAST surprise passes:

`THRESHOLD_ENCODING_RESCUE_SURVIVES_SURPRISE`

If both surprise arms fail:

`SURPRISE_CORRECTION_DOES_NOT_RESOLVE_V7_6`

Do not change arms or gates after seeing results.
