# Stone Age V7.8 — Caretaker / DAgger Dynamic-State Bridge

Status: **development complete**

Cadence: **0.88.1**

Official classification:

`DYNAMIC_STATE_TEACHING_INSUFFICIENT`

## Question

Can matched-budget caretaker teaching on dynamic states convert V7.7R's static contrast policy into robust closed-loop execution?

## Frozen design

Fresh founders: `70001..70008`.

Base recipe:
- CONTRAST18
- full 11 actions
- modules `(32,16)`
- normalized qualified teaching
- `learning_surprise=True` from lesson 0
- same static bootstrap structure as V7.7R

Arms:
- `STATIC_ONLY`
- `SCRIPTED_EXPERT_TRAJECTORY`
- `CARETAKER_DAGGER`

Both dynamic arms received exactly **128 labeled dynamic states per skill**.

## Result

All **8/8 founders were valid**.

Median retained EXACT / FRESH / CLOSED-LOOP:

| Skill | STATIC_ONLY | SCRIPTED_EXPERT_TRAJECTORY | CARETAKER_DAGGER |
| --- | --- | --- | --- |
| FOOD | 100 / 100 / 8.3% | 75 / 75 / 100% | 50 / 50 / 100% |
| FIRE | 100 / 100 / 0% | 49.7 / 50 / 58.3% | 33.3 / 33.3 / 0% |
| HUNT | 100 / 100 / 83.3% | 82.0 / 78.5 / 100% | 86.5 / 88.9 / 100% |
| SHELTER | 100 / 100 / 0% | 66.7 / 66.7 / 100% | 66.7 / 66.7 / 100% |

Founder-level all-four readiness:
- STATIC_ONLY: 0/8
- SCRIPTED_EXPERT_TRAJECTORY: 0/8
- CARETAKER_DAGGER: 0/8

## Interpretation

V7.8 shows that dynamic teaching is powerful enough to rescue behavior on several skills, but it does so by destabilizing the static policy.

### Dynamic behavior rescue

CARETAKER_DAGGER reaches 100% median closed-loop success on:
- FOOD
- HUNT
- SHELTER

SCRIPTED_EXPERT_TRAJECTORY also reaches 100% on FOOD/HUNT/SHELTER and partially improves FIRE.

So trajectory coverage was a real missing ingredient.

### Retention failure

That rescue is not stable continual learning.

Median static retention after CARETAKER_DAGGER:
- FOOD 50 / 50%
- FIRE 33.3 / 33.3%
- HUNT 86.5 / 88.9%
- SHELTER 66.7 / 66.7%

The accepted-correction load tracks this failure qualitatively:
- FOOD: ~14.5 accepted dynamic corrections
- FIRE: ~93
- HUNT: ~8
- SHELTER: ~14.5

FIRE is the strongest interference case: many dynamic corrections, collapse to one prototype/action family, and no reliable loop rescue.

HUNT is the opposite positive control: very high pre-lesson agreement (~99%), very few accepted corrections, full loop success, and comparatively mild retention loss.

This pattern supports a new boundary:

> The caretaker can supply the missing dynamic state coverage, but repeated online supervised corrections interfere with previously acquired static mappings.

The current problem is therefore no longer simply dynamic-state coverage. It is **retention under online correction / continual supervised interference**.

## Next direction

**Stone Age V7.9 — Retention-Protected Caretaker Bridge**

Keep:
- cadence-net 0.88.1
- CONTRAST18
- full 11 actions
- normalized qualified teaching
- `learning_surprise=True` from lesson 0
- same static bootstrap
- separate single-skill brains

Primary question:

Can interleaved rehearsal of the original static mappings preserve V7.7R's policy while keeping the dynamic gains from caretaker correction?

Recommended arms:

1. `STATIC_ONLY`
2. `DAGGER128`
3. `DAGGER64` — dynamic-dose control
4. `DAGGER64_STATIC_REPLAY64` — 64 learner-path dynamic labels interleaved 1:1 with 64 balanced static-anchor labels

This keeps the replay arm at 128 total post-bootstrap lesson calls, matched to DAgger128, while DAgger64 tells us whether any apparent rescue comes merely from reducing dynamic update dose.

Primary gates remain:
- exact >=90%
- fresh >=80%
- closed-loop >=4/6
- >=6/8 founders ready on all four skills

No shared brain, attention, episodic memory, hidden inventory or reward learning should be reopened until retention under correction is resolved.
