# Stone Age V7.10R — Replay Boundary Correction

Status: **running protocol / frozen before run**

Cadence: **0.88.1**

V7.10's frozen run showed that post-DAGGER replay did not recover cold static mappings, but a runner audit found that replay rows were taught in one continuing stream while the original successful static bootstrap called `brain.reset()` before every row.

Cadence 0.88.1 defines `Brain.reset()` as clearing per-stream state and eligibility while keeping learned weights and records. Therefore V7.10 did not test a matched reapplication of the original successful static teaching boundary.

## Question

Is V7.10's apparent irrecoverability caused by **continuing-stream replay context**, or does the static policy still fail to recover when replay is taught under the same reset boundary as the original bootstrap?

## Fixed base recipe

- cadence-net==0.88.1
- CONTRAST18
- full 11 actions
- modules `(32,16)`
- normalized qualified teaching
- `learning_surprise=True` from lesson 0
- same static bootstrap and DAgger64 logic as V7.10
- fresh founders `73001..73008`

## Common history

For each founder/skill:

1. static bootstrap
2. exactly 64 learner-path DAgger labels
3. evaluate `POST_DAGGER64`
4. deep-copy that exact post-DAGGER64 brain into two replay branches

The two replay branches therefore have identical learned parameters, memory, random state, and DAgger history at the branch point.

## Branches

### CONTINUING_REPLAY
Reproduces V7.10:
- no `brain.reset()` before replay rows
- same deterministic balanced replay rows/order

### RESET_REPLAY
Matched cold teaching boundary:
- call `brain.reset()` immediately before every replay row
- otherwise same replay rows, order, labels and doses

## Replay checkpoints

For both branches:

- `REPLAY32`: 32 cumulative calls
- `REPLAY64`: 64 cumulative calls
- `REPLAY_FULL`: one complete original static pass
  - FOOD: 128 calls
  - FIRE/HUNT/SHELTER: 192 calls

## Evaluation

At:
- STATIC_ONLY
- POST_DAGGER64
- each replay checkpoint in each branch

Measure:
- exact static accuracy
- fresh static accuracy
- 6 held-out closed-loop episodes
- output dominance
- replay accepted/agreed presentations
- founder-level all-four readiness

Evaluation uses deep copies and does not mutate training branches.

## Frozen gates

Per skill:
- exact >=90%
- fresh >=80%
- closed-loop >=4/6

Primary reset-replay bridge pass requires:
- all four skill median gates pass at one RESET_REPLAY checkpoint
- >=6/8 valid founders individually pass all three gates on all four skills at that same checkpoint

## Frozen interpretation

- RESET_REPLAY static recovers while CONTINUING_REPLAY does not -> `RESET_BOUNDARY_RECOVERY_RESCUE`
- RESET_REPLAY full static+loop criterion passes -> `RESET_REPLAY_FULL_BRIDGE_PASS`
- both branches fail static recovery after full pass -> `STATIC_IRRECOVERABILITY_SURVIVES_RESET_CONTROL`
- RESET_REPLAY static recovers but loop fails -> `STATIC_RECOVERABLE_DYNAMIC_POLICY_COMPETES_AFTER_RESET`
- otherwise -> `PARTIAL_RESET_BOUNDARY_SIGNAL`

No shared four-skill brain, attention, episodic memory, hidden inventory, or reward-learning comparison is opened in V7.10R.
