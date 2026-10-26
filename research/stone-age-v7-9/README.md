# Stone Age V7.9 — Retention-Protected Caretaker Bridge

Status: **running protocol / frozen before run**

Cadence: **0.88.1**

V7.8 showed that dynamic caretaker teaching can rescue closed-loop behavior, but repeated online corrections destabilize the previously learned static policy. The next question is whether balanced rehearsal protects that policy while preserving the dynamic gains.

## Question

Can interleaved replay of the original static mappings prevent caretaker-driven forgetting?

## Fixed base recipe

- cadence-net==0.88.1
- CONTRAST18
- full 11 actions
- modules `(32,16)`
- normalized qualified teaching
- `learning_surprise=True` from lesson 0
- same static bootstrap as V7.7R/V7.8
- fresh founders `71001..71008`

## Arms

### STATIC_ONLY
Static bootstrap only.

### DAGGER128
Same V7.8 learner-path caretaker training:
- 128 dynamic labels/skill
- brain acts first
- caretaker labels the same state
- teach caretaker label
- execute the brain's chosen action

### DAGGER64
Dose control:
- identical DAgger rule
- only 64 dynamic labels/skill

### DAGGER64_STATIC_REPLAY64
Retention-protected arm:
- 64 learner-path dynamic labels/skill
- after each dynamic step, one balanced static-anchor replay lesson
- 64 static replay calls total
- 128 total post-bootstrap lesson calls

The replay arm therefore has the same total post-bootstrap call budget as DAGGER128, while DAGGER64 separates replay from simply reducing dynamic dose.

## Static replay anchors

The 64 replay anchors are drawn deterministically from the original static training generator and balanced across the skill's prototypes.

Because surprise teaching is enabled, an anchor that is still answered correctly is counted as agreed/skipped; an anchor that was forgotten becomes an accepted corrective lesson.

This makes replay itself a direct retention diagnostic.

## Evaluation

Each arm is evaluated on:

1. retained static exact
2. retained static fresh
3. 6 held-out closed-loop episodes per skill
4. dynamic accepted/agreed presentations
5. replay accepted/agreed presentations
6. brain/caretaker agreement during DAgger

## Frozen gates

Per skill:
- exact >=90%
- fresh >=80%
- closed-loop >=4/6

Primary replay success additionally requires:
- all four skill median gates pass
- >=6/8 valid founders individually pass all three gates on all four skills

## Frozen interpretation

- replay arm passes full criterion -> `STATIC_REPLAY_RETENTION_BRIDGE_PASS`
- DAGGER64 passes but replay not needed -> `DYNAMIC_DOSE_REDUCTION_SUFFICIENT`
- replay preserves static but loop fails -> `REPLAY_PRESERVES_POLICY_BUT_BLOCKS_DYNAMIC_ADAPTATION`
- replay improves both but misses frozen all-skill criterion -> `PARTIAL_RETENTION_PROTECTION_SIGNAL`
- otherwise -> `STATIC_REPLAY_NO_RETENTION_RESCUE`

No shared four-skill brain, attention, episodic memory, hidden inventory or reward-learning comparison is opened in V7.9.
