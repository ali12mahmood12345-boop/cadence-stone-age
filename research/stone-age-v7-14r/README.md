# Stone Age V7.14R — Fresh Four-Skill Shared Semantic Confirmation

Status: **confirmation protocol / frozen before run**

Cadence: **0.88.1**

V7.14 development established that one plain Cadence brain can retain and execute FOOD, FIRE, HUNT and SHELTER together when task identity is explicit, visible state is semantic, persistent actions are committed to their immediate semantic effects, stream state is reset before high-level queries, and a reset-matched semantic replay is used after DAgger.

V7.14R is a strict fresh confirmation of that exact recipe.

## Question

Does the V7.14 shared four-skill semantic bridge reproduce on a larger untouched founder panel without any recipe changes?

## Fresh founder panel

`79001..79016`

- 16 founders total
- minimum valid: 12/16
- shared confirmation threshold: 12/16 all-four ready
- control stability threshold: 12/16 all-four ready

## Frozen arms

### SHARED4

One shared 18-input / 11-action brain trained on all four skills.

### SEPARATE4_CONTROL

Four separate brains, one per skill.

For each founder, the shared brain and all four controls are deep-copied from the same untrained base brain before any teaching.

## Frozen representation

18-wide semantic vector.

Task context:
- input 0 = FOOD
- input 1 = FIRE
- input 2 = HUNT
- input 3 = SHELTER

Semantic state:
- input 4 = prerequisite A
- input 5 = prerequisite B
- input 6 = terminal/tool flag

All remaining inputs = 0.

The same 16 canonical semantic policy keys from V7.14 are used unchanged:

- FOOD: 2
- FIRE: 4
- HUNT: 5
- SHELTER: 5

## Frozen training

Architecture:
- inputs = 18
- actions = 11
- modules = (32,16)
- teaching = normalized
- learning_surprise=True from lesson 0
- qualified teaching

Static bootstrap:
- 64 presentations per canonical key
- brain.reset() before every independent static lesson
- shared arm uses deterministic balanced interleaving across all 16 keys
- controls use the same per-key dose on their skill subset

DAgger:
- exactly 64 learner-path labels per skill
- SHARED4 receives 256 total labels, round-robin by skill
- each separate control receives 64 labels for its own skill
- brain.reset() before every semantic high-level query
- learner acts before lesson
- caretaker labels the same state
- execute learner pre-lesson action through the frozen semantic primitive controller

Final replay:
- 64 presentations per canonical key
- same reset-before-row boundary
- same deterministic balanced interleaving

## Frozen controller

Before every high-level query:
- call brain.reset()

Persistent semantic primitives:
- PICK_BERRIES until food inventory increases
- GATHER_WOOD until wood increases
- GATHER_STONE until stone increases
- HUNT_RABBIT until rabbits_hunted increases or budget expires
- SLEEP until energy>=88 or budget expires

Other actions execute one normal decision window.

Skill budgets remain unchanged:
- FOOD: 12
- FIRE: 14
- HUNT: 16
- SHELTER: 22

## Evaluation checkpoints

Evaluate SHARED4 and SEPARATE4_CONTROL at:

1. STATIC_ONLY
2. POST_DAGGER64
3. POST_REPLAY_FULL

At every checkpoint:
- canonical semantic static accuracy per skill
- 6 held-out closed-loop episodes per skill
- output dominance
- founder all-four readiness

Environment validity:
- deterministic caretaker must solve 6/6 held-out episodes for every skill/founder

## Frozen gates

Per skill:
- static >=90%
- loop >=4/6

Founder all-four ready:
- all four skills pass both gates

Run validity:
- >=12/16 valid founders

Control stability:
- >=12/16 valid founders all-four ready across the four separate controls
- all four control median static gates pass
- all four control median loop gates pass

Shared confirmation:
- all four SHARED4 median static gates pass
- all four SHARED4 median loop gates pass
- >=12/16 valid SHARED4 founders all-four ready
- controls satisfy the stability gate

## Frozen classification

1. valid founders <12 -> `INSUFFICIENT_V7_14R_RUNS`
2. controls fail stability -> `CONTROL_RECIPE_NOT_STABLE_IN_CONFIRMATION`
3. shared confirmation gates pass -> `FOUR_SKILL_SHARED_SEMANTIC_BRIDGE_CONFIRMED`
4. controls stable but shared static medians fail -> `SHARED_STATIC_INTERFERENCE_NOT_CONFIRMED`
5. shared static medians pass but shared all-four/dynamic gate fails -> `SHARED_DYNAMIC_INTEGRATION_NOT_CONFIRMED`
6. otherwise -> `FOUR_SKILL_SHARED_SEMANTIC_BRIDGE_NOT_CONFIRMED`

No attention.
No episodic-memory arm.
No reward-learning arm.
No task-context weakening.
No post-hoc protocol changes.
