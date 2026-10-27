# Frozen Protocol — Stone Age V7.15

Status: DEVELOPMENT / frozen before run.

Cadence:
- cadence-net==0.88.1

Fresh founders:
- 80001..80008
- minimum valid 6/8

Arms:
- AUTONOMOUS_GLOBAL
- TASKED_SHARED_CONTROL

Initialization:
- compose one base brain per founder
- deep-copy it into both arms before any teaching

TASKED_SHARED_CONTROL:
- exact V7.14 shared recipe
- explicit task one-hot
- 16 semantic skill keys
- 64 presentations/key bootstrap
- DAgger64/skill
- 64 presentations/key reset replay
- standard V7.14 isolated skill evaluation
- autonomous exam uses frozen oracle goal routing

AUTONOMOUS_GLOBAL input:
0 hunger<45
1 warmth<55
2 energy<45
3 evening_or_night
4 food_inventory>0
5 berry_near
6 rabbit_near
7 has_spear
8 fire_exists
9 shelter_exists
10 wood>=2
11 wood>=4
12 wood>=10
13 stone>=2
14 stone>=4
15..17 zero

No task identity.

Caretaker priority:
1 hunger
2 cold/evening if no fire
3 low energy
4 explore

Hunger:
- food -> EAT
- berry -> PICK_BERRIES
- rabbit + spear -> HUNT_RABBIT
- rabbit + stone<2 -> GATHER_STONE
- rabbit + wood<2 -> GATHER_WOOD
- rabbit + prereqs -> CRAFT_SPEAR
- no source -> EXPLORE

Fire:
- wood<4 -> GATHER_WOOD
- stone<2 -> GATHER_STONE
- else CRAFT_FIRE

Sleep:
- shelter -> SLEEP
- wood<10 -> GATHER_WOOD
- stone<4 -> GATHER_STONE
- else BUILD_SHELTER

Static curriculum:
- 26 hard-coded global semantic keys
- 24 frozen oracle-trajectory states
- neutral EXPLORE control
- hungry/no-source EXPLORE control
- 64 presentations/key bootstrap
- 64 presentations/key final replay
- reset before every independent lesson

AUTONOMOUS DAgger:
- 8 scenario families
- 64 labels/family
- 512 total labels
- round-robin family interleaving
- reset before each semantic query
- learner acts before lesson
- caretaker labels same global state
- execute learner pre-lesson action

Scenario exam:
- 6 held-out variants/family

FORAGE:
- budget12
- require food_eaten>0

HUNT_EAT:
- budget20
- require rabbits_hunted>0 and food_eaten>0

FIRE_COLD:
- budget14
- require fire_exists

FIRE_EVENING:
- budget14
- require fire_exists

SHELTER_SLEEP:
- budget22
- require shelter_exists and energy>=88

FOOD_THEN_FIRE:
- budget28
- require food_eaten>0 and fire_exists

HUNT_THEN_SLEEP:
- budget45
- require rabbits_hunted>0, food_eaten>0, shelter_exists, energy>=88

ALL_NEEDS:
- budget56
- require food_eaten>0, fire_exists, shelter_exists, energy>=88

Environment:
- relevant resources clustered
- unavailable berry/rabbit opportunities moved far away, not deleted
- caretaker oracle must solve 48/48/founder

Motor primitives:
- PICK_BERRIES until food increases
- GATHER_WOOD until wood increases
- GATHER_STONE until stone increases
- HUNT_RABBIT until hunt success or budget expires
- SLEEP until energy>=88 or budget expires
- others one decision window
- brain.reset() before every high-level query

Autonomous checkpoints:
- STATIC_ONLY
- POST_DAGGER64
- POST_REPLAY_FULL

Autonomous static gates:
- overall >=90%
- FOOD route >=90%
- HUNT route >=90%
- FIRE route >=90%
- SHELTER route >=90%
- NEUTRAL diagnostic only

Scenario gate:
- >=4/6

Founder autonomous-ready:
- static gates pass
- all eight scenario gates pass

Control stability:
- >=6/8 standard V7.14 all-four ready
- all 8 oracle-routed scenario median gates pass
- >=6/8 founders all-scenario ready under oracle routing

Autonomous bridge:
- control stable
- autonomous median static gates pass
- all 8 autonomous median scenario gates pass
- >=6/8 founders autonomous-ready

Classification:
1. valid<6 -> INSUFFICIENT_V7_15_RUNS
2. control unstable -> TASKED_EXECUTOR_CONTROL_NOT_STABLE
3. bridge pass -> AUTONOMOUS_GOAL_ROUTING_BRIDGE_PASS
4. static routing fails -> AUTONOMOUS_ROUTING_ACQUISITION_BOTTLENECK
5. static passes, dynamic fails -> AUTONOMOUS_DYNAMIC_ROUTING_BOTTLENECK
6. otherwise -> PARTIAL_AUTONOMOUS_ROUTING_SIGNAL

No attention.
No episodic memory.
No reward learning.
No post-hoc changes.
