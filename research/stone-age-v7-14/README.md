# Stone Age V7.14 — Four-Skill Semantic Integration Bridge

Status: **development complete**

Cadence: **0.88.1**

Official frozen classification:

`FOUR_SKILL_SHARED_SEMANTIC_BRIDGE_PASS`

## Result

Fresh founders:
- `78001..78008`
- valid: **8/8**

Caretaker oracle:
- **192/192**

Final post-replay medians:

| Skill | SHARED static | SHARED loop | CONTROL static | CONTROL loop |
| --- | ---: | ---: | ---: | ---: |
| FOOD | 100% | 100% | 100% | 100% |
| FIRE | 100% | 100% | 100% | 100% |
| HUNT | 100% | 100% | 100% | 100% |
| SHELTER | 100% | 100% | 100% | 100% |

Founder all-four readiness:
- SHARED4: **7/8**
- SEPARATE4_CONTROL: **8/8**
- frozen requirement: >=6/8

All frozen shared and control median gates passed.

## Training trajectory

The important trajectory is:

### STATIC_ONLY
Shared and separate controls were already at 100% median static and loop performance on all four skills.

### POST_DAGGER64
Online learner-path correction destabilized both the shared brain and the separate controls.

Shared median static / loop:
- FOOD: 75% / 50%
- FIRE: 75% / 50%
- HUNT: 70% / 100%
- SHELTER: 50% / 100%

Control median static / loop:
- FOOD: 75% / 50%
- FIRE: 62.5% / 50%
- HUNT: 80% / 100%
- SHELTER: 60% / 100%

This shows the post-DAgger collapse is not uniquely a shared-brain interference effect.

### POST_REPLAY_FULL
Reset-matched semantic replay restored:
- all skill medians to 100/100 in SHARED4
- all skill medians to 100/100 in controls
- 7/8 shared all-four founders
- 8/8 control all-four founders

Therefore reset-matched semantic replay acts as a strong reconsolidation step after online correction.

## Residual shared miss

Founder **78001** is the only shared founder that does not satisfy all-four readiness after final replay.

Final shared results for 78001:
- FOOD: static 100%, loop 6/6
- FIRE: static 75%, loop 0/6
- HUNT: static 80%, loop 6/6
- SHELTER: static 100%, loop 6/6

The decisive FIRE error is:
- semantic state `FIRE_W1_S1`
- target: `CRAFT_FIRE`
- prediction: `BUILD_SHELTER`

The residual HUNT static error is:
- `HUNT_W0_S1_NO_SPEAR`
- target: `GATHER_WOOD`
- prediction: `CRAFT_SPEAR`

This is consistent with a small seed-specific cross-skill semantic collision rather than a broad capacity or controller failure.

## Development claim

V7.14 establishes a development bridge:

> One plain Cadence brain can hold and execute FOOD, FIRE, HUNT and SHELTER together when task identity is explicit, visible state is semantic, persistent actions are treated as motor primitives, stream state is reset at semantic queries, and the policy is reconsolidated with reset-matched replay after DAgger.

No attention or episodic memory was required for this bridge.

## Scientific status

V7.14 is a **development result**, not yet a fresh confirmation.

The next step should be an exact replication on a larger untouched founder panel before adding attention, episodic memory, or removing explicit task context.

## Next direction

**Stone Age V7.14R — Fresh Four-Skill Shared Semantic Confirmation**

Freeze the V7.14 recipe unchanged:
- SHARED4 and SEPARATE4_CONTROL
- explicit task one-hot
- same 16 semantic keys
- same base-brain matched initialization
- 64 presentations/key bootstrap
- DAgger64/skill
- 64 presentations/key final reset replay
- semantic motor primitives
- stream reset before every high-level query
- unchanged skill budgets
- no attention or episodic memory

Recommended fresh panel:
- `79001..79016`

Confirmation gates:
- >=12/16 valid founders
- controls stable in >=12/16
- all shared skill median static and loop gates pass
- shared all-four readiness >=12/16

If confirmed, the next experiment can remove or weaken explicit task context, or then test whether attention/memory adds value beyond the now-stable semantic shared baseline.
