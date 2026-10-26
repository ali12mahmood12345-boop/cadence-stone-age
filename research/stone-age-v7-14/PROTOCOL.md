# Frozen Protocol — Stone Age V7.14

Status: DEVELOPMENT / frozen before run.

Cadence:
- cadence-net==0.88.1

Fresh founders:
- 78001..78008
- minimum valid 6/8

Arms:
- SHARED4
- SEPARATE4_CONTROL

Initialization:
- compose one base brain per founder
- deep-copy base into SHARED4 and four skill-control brains before any teaching

Architecture:
- inputs=18
- actions=11
- modules=(32,16)
- teaching="normalized"
- learning_surprise=True from lesson 0
- qualified teaching

Semantic input:
- 0 FOOD goal
- 1 FIRE goal
- 2 HUNT goal
- 3 SHELTER goal
- 4 prereq A
- 5 prereq B
- 6 tool/terminal flag
- remaining inputs zero

Canonical policy table:
- FOOD 2 states
- FIRE 4 states
- HUNT 5 states
- SHELTER 5 states
- total 16

Static bootstrap:
- 64 presentations/canonical state
- reset before every lesson
- shared: deterministic balanced interleaving
- controls: same per-state dose on skill subset

DAgger:
- 64 labels/skill
- shared = 256 total labels, round-robin skill interleaving
- control = 64 labels on own skill
- reset before each high-level query
- brain acts before lesson
- caretaker labels same state
- execute learner pre-lesson action via semantic primitive

Final replay:
- exact same 64 presentations/canonical state
- reset before every lesson
- deterministic balanced interleaving

Semantic primitives:
- PICK_BERRIES until food inventory increases
- GATHER_WOOD until wood increases
- GATHER_STONE until stone increases
- HUNT_RABBIT until rabbits_hunted increases or budget expires
- SLEEP until energy>=88 or budget expires
- other actions one decision window

Before every high-level query:
- brain.reset()

Skill window budgets:
- FOOD 12
- FIRE 14
- HUNT 16
- SHELTER 22

Evaluation checkpoints:
- STATIC_ONLY
- POST_DAGGER64
- POST_REPLAY_FULL

Per checkpoint:
- canonical semantic static accuracy/skill
- 6 held-out closed-loop episodes/skill
- output dominance
- all-four founder readiness

Environment oracle:
- caretaker must solve 6/6 for each skill/founder

Per-skill gates:
- static >=90%
- loop >=4/6

Founder all-four ready:
- all 4 skills pass both gates

Control stability:
- >=6/8 founders all-four ready across separate controls

Shared bridge:
- all 4 shared median static gates pass
- all 4 shared median loop gates pass
- >=6/8 shared founders all-four ready
- controls stable

Classification:
1. valid <6 -> INSUFFICIENT_V7_14_RUNS
2. controls unstable -> CONTROL_RECIPE_NOT_STABLE
3. shared bridge passes -> FOUR_SKILL_SHARED_SEMANTIC_BRIDGE_PASS
4. controls pass but shared static fails -> SHARED_STATIC_INTERFERENCE
5. shared static passes but shared dynamic bridge fails -> SHARED_DYNAMIC_INTEGRATION_BOTTLENECK
6. otherwise -> PARTIAL_SHARED_SEMANTIC_SIGNAL

No attention.
No episodic memory.
No reward-learning arm.
No post-hoc changes.
