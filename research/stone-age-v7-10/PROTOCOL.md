# Frozen Protocol — Stone Age V7.10

Status: DEVELOPMENT / frozen before run.

Cadence:
- cadence-net==0.88.1

Fresh founders:
- 72001..72008
- minimum valid 6/8
- full bridge requires >=6/8 all-four founders at the same checkpoint

Base:
- CONTRAST18
- full 11 actions
- modules=(32,16)
- teaching="normalized"
- learning_surprise=True from lesson 0
- qualified teaching
- static bootstrap identical in structure to V7.7R–V7.9

Static data:
- 64 rows/prototype
- 24 fresh rows/prototype

Common non-control history:
- static bootstrap
- DAgger64 on learner-path states
- no replay during DAgger
- then post-DAGGER replay

DAgger rule:
- observe current real environment state
- brain chooses greedy action
- caretaker labels that same state
- teach caretaker label
- execute the brain's chosen action
- continue from resulting state
- exactly 64 dynamic labels/skill

Caretaker:
FOOD:
- food present -> EAT
- else PICK_BERRIES

FIRE:
- wood < 4 -> GATHER_WOOD
- else stone < 2 -> GATHER_STONE
- else CRAFT_FIRE

HUNT:
- has_spear -> HUNT_RABBIT
- else stone < 2 -> GATHER_STONE
- else wood < 2 -> GATHER_WOOD
- else CRAFT_SPEAR

SHELTER:
- shelter exists -> SLEEP
- else wood < 10 -> GATHER_WOOD
- else stone < 4 -> GATHER_STONE
- else BUILD_SHELTER

Checkpoints:
1. STATIC_ONLY
2. POST_DAGGER64
3. REPLAY32
4. REPLAY64
5. REPLAY_FULL

Replay:
- begins only after DAgger64 is complete
- deterministic balanced ordering from the original static training rows
- cumulative doses:
  - REPLAY32 = 32 calls
  - REPLAY64 = 64 calls
  - REPLAY_FULL = one complete original static pass
- FOOD full pass = 128 calls
- FIRE/HUNT/SHELTER full pass = 192 calls
- same continuing brain across replay checkpoints
- evaluation uses deep copies and does not mutate the training brain

Evaluation at every checkpoint:
- exact static
- fresh static
- 6 held-out closed-loop episodes
- output dominance
- replay accepted/agreed counts
- all-four founder readiness

Gates:
- exact >=90%
- fresh >=80%
- loop >=4/6

Classification:
1. insufficient -> INSUFFICIENT_V7_10_RUNS
2. any replay checkpoint full criterion -> POST_DAGGER_CONSOLIDATION_BRIDGE_PASS
3. static all-skill readiness recovered but loop all-skill not -> STATIC_RECOVERABLE_DYNAMIC_POLICY_COMPETES
4. REPLAY_FULL static all-skill still fails -> STATIC_POLICY_NOT_RECOVERABLE_BY_ONE_PASS
5. otherwise material recovery without full criterion -> PARTIAL_POST_DAGGER_RECOVERY_SIGNAL

No post-hoc changes.
