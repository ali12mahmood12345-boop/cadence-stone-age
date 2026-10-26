# Frozen Protocol — Stone Age V7.8

Status: DEVELOPMENT / frozen before run.

Cadence:
- cadence-net==0.88.1

Fresh founders:
- 70001..70008
- minimum valid 6/8
- primary all-four readiness requires 6/8

Base policy:
- CONTRAST18
- full 11 actions
- modules=(32,16)
- teaching="normalized"
- learning_surprise=True from lesson 0
- qualified teaching
- static bootstrap identical in structure to V7.7R

Static data:
- 64 rows/prototype
- 24 fresh rows/prototype

Dynamic training budget:
- 128 labeled decision states per skill
- exactly matched between SCRIPTED_EXPERT_TRAJECTORY and CARETAKER_DAGGER

Arms:
1. STATIC_ONLY
2. SCRIPTED_EXPERT_TRAJECTORY
3. CARETAKER_DAGGER

SCRIPTED_EXPERT_TRAJECTORY:
- observe current state
- caretaker labels it
- lesson on contrast observation
- execute caretaker action
- repeat
- restart on success or episode cap until 128 labels

CARETAKER_DAGGER:
- observe current state
- brain chooses greedy action
- caretaker labels the same state
- lesson on contrast observation
- execute brain action
- repeat from resulting state
- restart on success or episode cap until 128 labels

Caretaker policy:
FOOD:
- observed food > 0 -> EAT
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
- shelter_exists -> SLEEP
- else wood < 10 -> GATHER_WOOD
- else stone < 4 -> GATHER_STONE
- else BUILD_SHELTER

Training episode caps:
- FOOD 12 decisions
- FIRE 14 decisions
- HUNT 16 decisions
- SHELTER 22 decisions

Evaluation:
- retained exact static
- retained fresh static
- 6 fresh closed-loop episodes per skill
- no teaching during evaluation
- separate brain copy per evaluation episode

Gates:
- exact >=90%
- fresh >=80%
- loop >=4/6
- primary DAgger all-four founder gate >=6/8

Diagnostics:
- dynamic accepted presentations
- dynamic agreed presentations
- brain/caretaker action agreement
- episode restarts
- action traces for failed held-out loops

Classification:
1. insufficient -> INSUFFICIENT_V7_8_RUNS
2. DAgger full criterion -> CARETAKER_DAGGER_DYNAMIC_BRIDGE_PASS
3. expert full criterion but DAgger fails -> EXPERT_TRAJECTORY_COVERAGE_ONLY
4. DAgger loop passes all skills but static retention fails -> DAGGER_RETENTION_TRADEOFF
5. otherwise -> DYNAMIC_STATE_TEACHING_INSUFFICIENT

No post-hoc changes.
