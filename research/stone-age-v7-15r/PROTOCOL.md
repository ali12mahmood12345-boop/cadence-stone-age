# Frozen Protocol — Stone Age V7.15R

Status: CONFIRMATION / frozen before run.

Cadence:
- cadence-net==0.88.1

Fresh founders:
- 82001..82016
- 16 total
- minimum valid 12
- autonomous confirmation requires >=12 ready
- corrected tasked control requires >=12 all-scenario ready

Strict replication:
- exact corrected V7.15C setup
- AUTONOMOUS_GLOBAL unchanged
- TASKED_SHARED_CONTROL canonicalization unchanged

AUTONOMOUS_GLOBAL:
- same global semantic representation
- same 26 canonical keys
- same caretaker priority
- same 64 presentations/key bootstrap
- same DAgger64/scenario
- same full reset replay
- same eight scenarios/budgets
- same motor primitives
- same stream reset before every high-level query

TASKED_SHARED_CONTROL:
- exact V7.14 shared executor recipe
- corrected V7.15C oracle-routed adapter:
  - HUNT + has_spear -> canonical HUNT_HAS_SPEAR
  - SHELTER + shelter_exists -> canonical SHELTER_EXISTS

Scenarios:
- FORAGE
- HUNT_EAT
- FIRE_COLD
- FIRE_EVENING
- SHELTER_SLEEP
- FOOD_THEN_FIRE
- HUNT_THEN_SLEEP
- ALL_NEEDS

Confirmation gates:
- >=12 valid
- autonomous overall static median >=90%
- autonomous FOOD/HUNT/FIRE/SHELTER static medians >=90%
- all 8 autonomous scenario medians >=4/6
- >=12 autonomous-ready founders
- all tasked standard skill median static/loop gates pass
- all 8 corrected tasked scenario medians >=4/6
- >=12 corrected tasked all-scenario ready founders

Classification:
1. valid<12 -> INSUFFICIENT_V7_15R_RUNS
2. corrected tasked control unstable -> TASKED_CONTROL_NOT_CONFIRMED
3. all confirmation gates pass -> AUTONOMOUS_GOAL_ROUTING_CONFIRMED
4. autonomous static fails -> AUTONOMOUS_ROUTING_ACQUISITION_NOT_CONFIRMED
5. autonomous static passes but dynamic/scenario confirmation fails -> AUTONOMOUS_DYNAMIC_ROUTING_NOT_CONFIRMED
6. otherwise -> AUTONOMOUS_GOAL_ROUTING_NOT_CONFIRMED

No attention.
No episodic memory.
No reward learning.
No Cadence 0.89.0 positional recall.
No post-hoc changes.
