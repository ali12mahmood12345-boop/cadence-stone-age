# Stone Age V7.10 — Post-DAgger Consolidation / Recoverability Microscope

Status: **running protocol / frozen before run**

Cadence: **0.88.1**

V7.9 showed that one-for-one static replay does not stabilize the joint static+dynamic policy. Static anchors are genuinely forgotten and can trigger corrective lessons, but interleaving 64 replay calls with 64 DAgger corrections still leaves poor final retention.

## Question

After a fixed DAgger64 phase, can a **separate post-DAgger consolidation block** recover the original static policy, and if so, does the acquired closed-loop behavior survive?

## Fixed base recipe

- cadence-net==0.88.1
- CONTRAST18
- full 11 actions
- modules `(32,16)`
- normalized qualified teaching
- `learning_surprise=True` from lesson 0
- same static bootstrap as V7.7R–V7.9
- fresh founders `72001..72008`

## Common history

Every non-control checkpoint begins from the same sequence:

1. static bootstrap
2. exactly 64 learner-path DAgger labels
3. no static replay during DAgger
4. freeze a post-DAGGER64 checkpoint
5. begin a separate deterministic balanced static replay block

The replay block is therefore consolidation **after** dynamic learning, not interleaved rehearsal.

## Checkpoints

### STATIC_ONLY
Immediately after static bootstrap.

### POST_DAGGER64
After 64 learner-path dynamic caretaker labels.

### REPLAY32
After 32 post-DAGGER static replay calls.

### REPLAY64
After 64 cumulative post-DAGGER static replay calls.

### REPLAY_FULL
After one cumulative full pass through the original static training rows:
- FOOD: 128 replay calls
- FIRE: 192
- HUNT: 192
- SHELTER: 192

The same brain is followed through the full checkpoint sequence within each founder/skill.

## Replay order

Replay rows are generated from the original static training set, then reordered deterministically so prototype classes are balanced throughout the replay stream rather than appearing in one large block.

## Evaluation at every checkpoint

- static exact accuracy
- static fresh accuracy
- 6 held-out closed-loop episodes
- output dominance
- replay accepted/agreed presentations
- cumulative replay accepted/agreed
- founder-level all-four readiness

Evaluation is read-only on deep copies.

## Frozen gates

Per skill:
- exact >=90%
- fresh >=80%
- closed-loop >=4/6

A checkpoint is a full bridge pass only if:
- all four skill median gates pass, and
- >=6/8 founders individually pass all three gates on all four skills at that same checkpoint

## Frozen interpretation

- any replay checkpoint passes full criterion -> `POST_DAGGER_CONSOLIDATION_BRIDGE_PASS`
- static all-skill readiness returns but closed-loop all-skill readiness fails -> `STATIC_RECOVERABLE_DYNAMIC_POLICY_COMPETES`
- REPLAY_FULL still fails static all-skill readiness -> `STATIC_POLICY_NOT_RECOVERABLE_BY_ONE_PASS`
- replay materially improves retention but misses the frozen criterion -> `PARTIAL_POST_DAGGER_RECOVERY_SIGNAL`

No shared four-skill brain, attention, episodic memory, hidden inventory, or reward learning is opened in V7.10.
