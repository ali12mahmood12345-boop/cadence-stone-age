# Frozen Protocol — Stone Age V7.9

Status: DEVELOPMENT / frozen before run.

Cadence:
- cadence-net==0.88.1

Fresh founders:
- 71001..71008
- minimum valid 6/8
- primary all-four readiness requires 6/8

Base policy:
- CONTRAST18
- full 11 actions
- modules=(32,16)
- teaching="normalized"
- learning_surprise=True from lesson 0
- qualified teaching
- static bootstrap identical in structure to V7.7R/V7.8

Static data:
- 64 rows/prototype
- 24 fresh rows/prototype

Arms:
1. STATIC_ONLY
2. DAGGER128
3. DAGGER64
4. DAGGER64_STATIC_REPLAY64

DAgger rule:
- observe current real environment state
- brain chooses greedy action
- caretaker labels that same state
- teach caretaker label
- execute the brain's chosen action
- continue from resulting state

Dynamic budgets:
- DAGGER128: 128 dynamic labels/skill
- DAGGER64: 64 dynamic labels/skill
- DAGGER64_STATIC_REPLAY64: 64 dynamic labels/skill

Replay budget:
- DAGGER64_STATIC_REPLAY64: exactly 64 balanced static-anchor lesson calls/skill
- one replay call after each dynamic step
- total post-bootstrap lesson calls = 128

Static anchors:
- deterministic
- drawn from original static training generator
- balanced across prototypes
- 64 total per skill
- transformed with the exact CONTRAST18 representation

Caretaker policy:
FOOD:
- food present -> EAT
- otherwise -> PICK_BERRIES

FIRE:
- wood < 4 -> GATHER_WOOD
- else stone < 2 -> GATHER_STONE
- else -> CRAFT_FIRE

HUNT:
- has_spear -> HUNT_RABBIT
- else stone < 2 -> GATHER_STONE
- else wood < 2 -> GATHER_WOOD
- else -> CRAFT_SPEAR

SHELTER:
- shelter exists -> SLEEP
- else wood < 10 -> GATHER_WOOD
- else stone < 4 -> GATHER_STONE
- else -> BUILD_SHELTER

Evaluation:
- retained static exact
- retained static fresh
- 6 held-out closed-loop episodes/skill
- no teaching during evaluation
- separate brain copy per evaluation episode

Gates:
- exact >=90%
- fresh >=80%
- loop >=4/6
- replay all-four founder readiness >=6/8

Diagnostics:
- dynamic accepted/agreed
- replay accepted/agreed
- brain/caretaker agreement
- episode restarts
- failed loop action traces

Classification:
1. insufficient -> INSUFFICIENT_V7_9_RUNS
2. replay full criterion -> STATIC_REPLAY_RETENTION_BRIDGE_PASS
3. DAGGER64 full criterion without replay -> DYNAMIC_DOSE_REDUCTION_SUFFICIENT
4. replay static all-skill passes but loop all-skill fails -> REPLAY_PRESERVES_POLICY_BUT_BLOCKS_DYNAMIC_ADAPTATION
5. replay improves both retention and loop but misses full criterion -> PARTIAL_RETENTION_PROTECTION_SIGNAL
6. otherwise -> STATIC_REPLAY_NO_RETENTION_RESCUE

No post-hoc changes.
