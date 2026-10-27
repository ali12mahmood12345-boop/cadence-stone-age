# Frozen Protocol — Stone Age V7.14R

Status: CONFIRMATION / frozen before run.

Cadence:
- cadence-net==0.88.1

Fresh founders:
- 79001..79016
- 16 total
- minimum valid 12
- shared confirmation requires >=12/16 all-four ready
- controls require >=12/16 all-four ready

Scope:
- strict replication of V7.14
- FOOD / FIRE / HUNT / SHELTER
- SHARED4 vs SEPARATE4_CONTROL

Initialization:
- compose one base brain per founder
- deep-copy into SHARED4 and four skill-control brains before any teaching

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
- FOOD 2
- FIRE 4
- HUNT 5
- SHELTER 5
- total 16

Static bootstrap:
- 64 presentations/key
- reset before every independent lesson
- shared deterministic balanced interleaving
- controls same per-key dose on skill subset

DAgger:
- 64 labels/skill
- shared 256 total labels, round-robin skill interleaving
- control 64 labels on own skill
- reset before each high-level query
- brain acts before lesson
- caretaker labels same state
- execute learner pre-lesson action via semantic primitive

Final replay:
- 64 presentations/key
- reset before every lesson
- deterministic balanced interleaving

Semantic primitives:
- PICK_BERRIES until food increases
- GATHER_WOOD until wood increases
- GATHER_STONE until stone increases
- HUNT_RABBIT until rabbits_hunted increases or budget expires
- SLEEP until energy>=88 or budget expires
- other actions one decision window

Before every high-level query:
- brain.reset()

Skill budgets:
- FOOD 12
- FIRE 14
- HUNT 16
- SHELTER 22

Checkpoints:
- STATIC_ONLY
- POST_DAGGER64
- POST_REPLAY_FULL

Per checkpoint:
- semantic static accuracy/skill
- 6 held-out loops/skill
- output dominance
- all-four founder readiness

Oracle:
- caretaker must solve 6/6 for every skill/founder

Per-skill gates:
- static >=90%
- loop >=4/6

Founder all-four:
- all four skill static+loop gates pass

Control stability:
- >=12/16 control all-four founders
- all four control median static gates pass
- all four control median loop gates pass

Shared confirmation:
- >=12/16 shared all-four founders
- all four shared median static gates pass
- all four shared median loop gates pass
- controls stable

Classification:
1. valid <12 -> INSUFFICIENT_V7_14R_RUNS
2. controls unstable -> CONTROL_RECIPE_NOT_STABLE_IN_CONFIRMATION
3. shared confirmation passes -> FOUR_SKILL_SHARED_SEMANTIC_BRIDGE_CONFIRMED
4. controls stable but shared static fails -> SHARED_STATIC_INTERFERENCE_NOT_CONFIRMED
5. shared static passes but dynamic/all-four fails -> SHARED_DYNAMIC_INTEGRATION_NOT_CONFIRMED
6. otherwise -> FOUR_SKILL_SHARED_SEMANTIC_BRIDGE_NOT_CONFIRMED

No attention.
No episodic memory.
No reward learning.
No task-context weakening.
No post-hoc changes.
