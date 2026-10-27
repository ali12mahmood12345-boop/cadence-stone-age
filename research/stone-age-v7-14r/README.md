# Stone Age V7.14R — Fresh Four-Skill Shared Semantic Confirmation

Status: **fresh confirmation complete**

Cadence: **0.88.1**

Official classification:

`FOUR_SKILL_SHARED_SEMANTIC_BRIDGE_CONFIRMED`

## Purpose

V7.14R was a strict fresh confirmation of the successful V7.14 four-skill shared semantic bridge.

The exact V7.14 `run_founder()` implementation was reused unchanged.

Fresh founders:
- `79001..79016`

No representation, training, controller, replay, or gate changes were introduced.

## Frozen recipe

Arms:
- `SHARED4`
- `SEPARATE4_CONTROL`

Matched initialization:
- one untrained base brain per founder
- deep-copy into the shared brain and all four single-skill controls before teaching

Representation:
- explicit FOOD/FIRE/HUNT/SHELTER one-hot task context
- compact semantic prerequisite state
- 16 canonical semantic policy keys

Training:
1. 64 reset-per-row presentations per semantic key
2. DAgger64 per skill
3. full 64-presentations-per-key reset-matched semantic replay

Controller:
- `brain.reset()` before every semantic high-level query
- persistent actions committed to their immediate semantic effect
- original skill-specific episode budgets

No attention, episodic memory, reward-learning arm, or task-context weakening.

## Result

All **16/16 founders were valid**.

Caretaker oracle:
- **384/384**

Final post-replay medians:

| Skill | SHARED static | SHARED loop | CONTROL static | CONTROL loop |
| --- | ---: | ---: | ---: | ---: |
| FOOD | 100% | 100% | 100% | 100% |
| FIRE | 100% | 100% | 100% | 100% |
| HUNT | 100% | 100% | 100% | 100% |
| SHELTER | 100% | 100% | 100% | 100% |

Founder all-four readiness:
- SHARED4: **16/16**
- SEPARATE4_CONTROL: **16/16**
- frozen requirement: >=12/16

All frozen confirmation gates passed.

## Stronger founder-level result

The confirmation is stronger than the run-level median gates:

> Every final POST_REPLAY_FULL shared and control static score and loop score is 100% across all 16 founders.

Final pairwise SHARED vs CONTROL:
- FOOD static: 16 ties
- FOOD loop: 16 ties
- FIRE static: 16 ties
- FIRE loop: 16 ties
- HUNT static: 16 ties
- HUNT loop: 16 ties
- SHELTER static: 16 ties
- SHELTER loop: 16 ties

There are no final shared losses on the fresh confirmation panel.

## Training trajectory

The strict replication reproduces the same important qualitative mechanism from V7.14.

### STATIC_ONLY

Shared and control median static/loop performance is 100/100 across all four skills.

### POST_DAGGER64

Online learner-path teaching destabilizes the policy.

Shared medians:
- FOOD: 50% static / 0% loop
- FIRE: 50% / 0%
- HUNT: 50% / 100%
- SHELTER: 40% / 100%

Control medians:
- FOOD: 100% / 100%
- FIRE: 75% / 50%
- HUNT: 60% / 100%
- SHELTER: 60% / 100%

The fresh panel therefore shows stronger transient shared interference than the original V7.14 development panel, especially for FOOD and FIRE.

### POST_REPLAY_FULL

Reset-matched semantic replay restores:
- all shared skill medians to 100/100
- all control skill medians to 100/100
- all 16 shared founders to all-four readiness
- all 16 control founders to all-four readiness

Thus the confirmed final bridge depends on reconsolidation after DAgger rather than on DAgger preserving the policy by itself.

## Confirmed finding

> One plain Cadence brain can reliably retain and execute FOOD, FIRE, HUNT and SHELTER together when task identity is explicit, state is represented semantically, persistent actions are treated as semantic motor primitives, stream state is reset before high-level decisions, and reset-matched semantic replay reconsolidates the policy after online correction.

No attention or episodic memory is required for this confirmed four-skill capacity result.

## Important boundary

Explicit task identity remains part of the confirmed representation.

A naive removal of task context is not a clean next ablation because several semantic prerequisite states are intentionally identical across skills while requiring different actions. For example, the ready state `A=1, B=1, C=0` can mean:
- FIRE -> CRAFT_FIRE
- HUNT -> CRAFT_SPEAR
- SHELTER -> BUILD_SHELTER

Removing task identity without adding other world/goal information would create contradictory labels for the same input.

## Next direction

**Stone Age V7.15 — Autonomous Goal Routing Bridge**

Move beyond externally supplied task identity without creating artificial label aliasing.

Use a global semantic world/need state that makes the active goal inferable from the environment itself, then train one shared policy to choose the next semantic action.

Candidate global state should expose only meaningful need/task variables, for example:
- food available / hunger need
- fire state / warmth need
- spear state / hunting opportunity or food need
- shelter state / energy or night need
- prerequisite resource threshold bits

Freeze a deterministic caretaker priority policy before the run.

Primary question:

> Can the confirmed shared semantic executor become an autonomous Stone Age policy that selects the appropriate goal from world needs rather than receiving FOOD/FIRE/HUNT/SHELTER as an external task label?

Do not add attention or episodic memory in the first autonomous-goal bridge. First characterize plain semantic goal routing.
