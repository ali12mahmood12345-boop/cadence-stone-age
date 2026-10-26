# Frozen Protocol — Stone Age V7.6R

Status: DEVELOPMENT REPLICATION.

Cadence: `cadence-net==0.88.1`.

Motivation: V7.6 did not use the corrected normalized-teaching rule documented in 0.88.1. V7.6R tests whether `learning_surprise=True` from lesson 0 changes the RAW18 vs CONTRAST18 diagnosis.

Fresh founders: `68001..68008`; minimum valid 6/8.

Dataset and binary selection are exactly the V7.6 design:

- 64 training rows/prototype
- 24 fresh rows/prototype
- balanced 50/50 one-vs-rest classifiers

Architecture:

- actions=2
- modules=(32,16)

All arms:

- `teaching="normalized"`
- qualified one-row `Brain.lesson`
- one pass

Arms:

1. `RAW18_CALM` — raw observation, surprise=False.
2. `RAW18_SURPRISE` — raw observation, surprise=True from lesson 0.
3. `CONTRAST18_CALM` — exact V7.6 threshold transform, surprise=False.
4. `CONTRAST18_SURPRISE` — exact V7.6 threshold transform, surprise=True from lesson 0.

Primary evaluation:

- cold exact `brain.predict`
- cold fresh `brain.predict`

Frozen gates:

- exact >=90%
- fresh >=80%
- representation passes only if the median founder's WORST binary classifier passes.

Diagnostics:

- accepted_presentations
- agreed_presentations
- exact/fresh output dominance

Classification:

- RAW surprise passes all while RAW calm fails -> `NORMALIZED_TEACHING_COLLAPSE_CONFOUNDED_RAW18`
- RAW surprise fails while CONTRAST surprise passes -> `THRESHOLD_ENCODING_RESCUE_SURVIVES_SURPRISE`
- both surprise arms fail -> `SURPRISE_CORRECTION_DOES_NOT_RESOLVE_V7_6`

No post-hoc changes.
