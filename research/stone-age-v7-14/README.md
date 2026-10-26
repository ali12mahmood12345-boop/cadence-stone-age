# Stone Age V7.14 — Four-Skill Semantic Integration Bridge

Status: **development protocol / frozen before run**

Cadence: **0.88.1**

V7.13R freshly confirmed the FIRE controller boundary on 16/16 founders. V7.14 now reopens shared-brain integration.

## Question

Can one plain Cadence brain retain and execute FOOD, FIRE, HUNT and SHELTER together when:

- task identity is explicit,
- visible state is semantic rather than nuisance-heavy,
- temporally extended actions are committed to completion,
- Cadence stream state is reset before each semantic high-level query?

## Scope

Fresh founders:

`78001..78008`

Minimum valid:
- 6/8

Primary arms:

### SHARED4

One shared 18-input / 11-action brain trained on all four skills.

### SEPARATE4_CONTROL

Four separate brains, one per skill.

All five brains for a founder are deep-copied from the same untrained base brain before any teaching. This gives the shared brain and each control the same initial graph/weights.

No attention, episodic memory or reward-learning arm is opened in V7.14.

## Semantic representation

18-wide vector.

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

Task meanings:

### FOOD
- input 4 = has food
- target:
  - no food -> PICK_BERRIES
  - food -> EAT

### FIRE
- input 4 = wood>=4
- input 5 = stone>=2
- target:
  - wood not ready -> GATHER_WOOD
  - wood ready, stone not ready -> GATHER_STONE
  - both ready -> CRAFT_FIRE

### HUNT
- input 4 = wood>=2
- input 5 = stone>=2
- input 6 = has_spear
- target:
  - has_spear -> HUNT_RABBIT
  - otherwise stone not ready -> GATHER_STONE
  - otherwise wood not ready -> GATHER_WOOD
  - otherwise -> CRAFT_SPEAR

### SHELTER
- input 4 = wood>=10
- input 5 = stone>=4
- input 6 = shelter_exists
- target:
  - shelter_exists -> SLEEP
  - otherwise wood not ready -> GATHER_WOOD
  - otherwise stone not ready -> GATHER_STONE
  - otherwise -> BUILD_SHELTER

## Canonical semantic curriculum

The complete reachable semantic policy table contains 16 keys:

- FOOD: 2
- FIRE: 4
- HUNT: 5
- SHELTER: 5

Each canonical key is presented 64 times during static bootstrap and 64 times during final replay.

All independent static lessons call `brain.reset()` immediately before teaching.

SHARED4 uses a deterministic balanced interleaving across all 16 keys.

Each SEPARATE4_CONTROL brain receives the exact subset belonging to its skill with the same per-key dose.

## Dynamic teaching

After static bootstrap:

- exactly 64 learner-path DAgger labels per skill
- SHARED4 receives 256 total labels, interleaved round-robin by skill
- each separate control receives 64 labels for its own skill

At every DAgger semantic query:

1. call `brain.reset()`
2. brain chooses greedily
3. caretaker labels the same semantic state
4. teach caretaker label
5. execute the learner's pre-lesson action as a semantic primitive
6. continue from the resulting environment state

## Semantic motor primitives

The controller commits actions that require persistence:

- PICK_BERRIES -> hold until food inventory increases
- GATHER_WOOD -> hold until wood increases
- GATHER_STONE -> hold until stone increases
- HUNT_RABBIT -> hold until rabbits_hunted increases or budget expires
- SLEEP -> hold until energy>=88 or budget expires

Other actions execute one ordinary decision window.

Before every new high-level brain query:
- call `brain.reset()`

Skill-specific window budgets remain unchanged:
- FOOD: 12
- FIRE: 14
- HUNT: 16
- SHELTER: 22

## Checkpoints

Evaluate both SHARED4 and controls at:

1. `STATIC_ONLY`
2. `POST_DAGGER64`
3. `POST_REPLAY_FULL`

At each checkpoint:
- semantic truth-table accuracy per skill
- 6 held-out closed-loop episodes per skill
- output dominance
- founder-level all-four readiness

Environment sanity:
- deterministic caretaker must solve 6/6 held-out episodes for every skill/founder.

## Frozen gates

Per skill:
- semantic static accuracy >=90%
- closed-loop success >=4/6

Founder all-four ready:
- all four skills pass both gates

Run validity:
- >=6/8 valid founders

Control stability:
- >=6/8 founders all-four ready across the four separate controls

Shared bridge pass:
- all four SHARED4 median static gates pass
- all four SHARED4 median loop gates pass
- >=6/8 SHARED4 founders all-four ready
- controls satisfy their stability gate

## Frozen classification

1. valid founders <6 -> `INSUFFICIENT_V7_14_RUNS`
2. controls fail stability -> `CONTROL_RECIPE_NOT_STABLE`
3. shared full bridge passes -> `FOUR_SKILL_SHARED_SEMANTIC_BRIDGE_PASS`
4. controls pass but shared static retention fails -> `SHARED_STATIC_INTERFERENCE`
5. shared static passes but dynamic all-four bridge fails -> `SHARED_DYNAMIC_INTEGRATION_BOTTLENECK`
6. otherwise -> `PARTIAL_SHARED_SEMANTIC_SIGNAL`

No post-hoc representation, dose, controller, or gate changes.
