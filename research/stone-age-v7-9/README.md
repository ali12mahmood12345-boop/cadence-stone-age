# Stone Age V7.9 — Retention-Protected Caretaker Bridge

Status: **development complete**

Cadence: **0.88.1**

Official classification:

`STATIC_REPLAY_NO_RETENTION_RESCUE`

## Question

Can balanced static rehearsal preserve the acquired Stone Age policy while retaining learner-path caretaker gains?

## Frozen design

Fresh founders: `71001..71008`.

Base recipe:
- CONTRAST18
- full 11 actions
- modules `(32,16)`
- normalized qualified teaching
- `learning_surprise=True` from lesson 0

Arms:
- `STATIC_ONLY`
- `DAGGER128`
- `DAGGER64`
- `DAGGER64_STATIC_REPLAY64`

Replay arm:
- 64 learner-path dynamic labels
- 64 deterministic balanced static-anchor replay calls
- one replay call after each dynamic step
- 128 total post-bootstrap calls

## Result

All **8/8 founders were valid**.

Median retained EXACT / FRESH / CLOSED-LOOP:

| Skill | STATIC_ONLY | DAGGER128 | DAGGER64 | DAGGER64_STATIC_REPLAY64 |
| --- | --- | --- | --- | --- |
| FOOD | 100 / 100 / 0% | 50 / 50 / 100% | 50 / 50 / 100% | 50 / 50 / 100% |
| FIRE | 100 / 99.3 / 0% | 33.3 / 33.3 / 0% | 33.3 / 33.3 / 0% | 33.3 / 33.3 / 50% |
| HUNT | 100 / 100 / 50% | 62.0 / 63.2 / 100% | 59.6 / 61.1 / 100% | 50 / 50 / 100% |
| SHELTER | 100 / 100 / 0% | 66.7 / 66.7 / 100% | 66.7 / 66.7 / 100% | 66.7 / 66.7 / 100% |

Founder-level all-four readiness:
- STATIC_ONLY: 0/8
- DAGGER128: 0/8
- DAGGER64: 0/8
- DAGGER64_STATIC_REPLAY64: 0/8

Mean median scores across the four skills:
- STATIC_ONLY: retention 0.998, loop 0.125
- DAGGER128: retention 0.530, loop 0.750
- DAGGER64: retention 0.524, loop 0.750
- DAGGER64_STATIC_REPLAY64: retention **0.500**, loop **0.875**

## Interpretation

Simple one-for-one static replay does **not** solve the retention problem.

The replay arm frequently detected genuine forgetting:
- FOOD: median 15/64 replay anchors required accepted corrective lessons
- FIRE: 33/64
- HUNT: 23/64
- SHELTER: ~22.5/64

So replay was not merely skipped as already correct. The system was actively correcting forgotten anchors.

However, final static retention remained poor and did not improve over DAGGER64. Pairwise median replay-vs-DAGGER64 exact/fresh gains were zero in every skill, and only a minority of founders improved.

At the same time, the replay arm retained strong dynamic behavior:
- FOOD 100% loop median
- FIRE 50%
- HUNT 100%
- SHELTER 100%

This means the current failure is not simply "too few dynamic examples" and not simply "no rehearsal".

A more specific boundary emerges:

> Online dynamic corrections and static corrections can both be learned locally, but one-for-one alternation does not produce a stable joint policy. The learner appears to oscillate or interfere between nearby mappings rather than consolidate them together.

The accepted replay count is itself evidence of this instability: anchors repeatedly become surprising again after the dynamic stream.

## Next direction

**Stone Age V7.10 — Post-DAgger Consolidation / Recoverability Microscope**

Do not add more representations or memory systems yet.

Use the successful static bootstrap, then a fixed DAgger64 phase, then test whether a **separate consolidation block** can recover static policy without destroying the dynamic behavior.

Recommended arms/checkpoints:

1. `STATIC_ONLY`
2. `DAGGER64`
3. `DAGGER64_THEN_REPLAY32`
4. `DAGGER64_THEN_REPLAY64`
5. `DAGGER64_THEN_FULL_STATIC_REPLAY`

Important difference from V7.9:
- dynamic learning finishes first
- replay happens afterward in a dedicated block
- evaluate static + loop after DAgger and after each replay dose

This answers three distinct questions:

1. **Recoverability** — can the old static policy be restored at all?
2. **Joint capacity** — can static recovery coexist with the dynamic policy?
3. **Schedule dependence** — was V7.9's interleaving itself the problem?

Interpretation:
- static recovers and loop remains -> consolidation scheduling works
- static recovers but loop collapses -> incompatible / competing policies
- static does not recover -> deeper plasticity or representation interference

No shared four-skill brain, attention, episodic memory or hidden-state memory should be reopened before this is resolved.
