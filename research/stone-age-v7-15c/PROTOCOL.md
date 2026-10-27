# Frozen Protocol — Stone Age V7.15C

Status: CORRECTION / frozen before run.

Cadence:
- cadence-net==0.88.1

Fresh founders:
- 81001..81008
- minimum valid 6/8

Purpose:
- strict correction of V7.15 TASKED_SHARED_CONTROL observation adapter
- AUTONOMOUS_GLOBAL remains unchanged

Only correction:
- oracle-routed scenario observation canonicalization

HUNT adapter:
- if has_spear=False: input4=wood>=2, input5=stone>=2, input6=0
- if has_spear=True: input4=0, input5=0, input6=1

SHELTER adapter:
- if shelter_exists=False: input4=wood>=10, input5=stone>=4, input6=0
- if shelter_exists=True: input4=0, input5=0, input6=1

FOOD and FIRE:
- unchanged

Everything else remains V7.15:
- AUTONOMOUS_GLOBAL representation
- 26 keys
- caretaker priority
- bootstrap
- DAgger64/scenario
- replay
- scenarios
- budgets
- motor primitives
- gates

Classification:
1. valid<6 -> INSUFFICIENT_V7_15C_RUNS
2. corrected control unstable -> TASKED_CONTROL_CANONICALIZATION_NOT_SUFFICIENT
3. control stable + autonomous pass -> AUTONOMOUS_GOAL_ROUTING_BRIDGE_PASS
4. autonomous static fails -> AUTONOMOUS_ROUTING_ACQUISITION_BOTTLENECK
5. autonomous static passes but dynamic fails -> AUTONOMOUS_DYNAMIC_ROUTING_BOTTLENECK
6. otherwise -> PARTIAL_AUTONOMOUS_ROUTING_SIGNAL

No attention.
No episodic memory.
No reward learning.
No Cadence 0.89.0 positional recall.
No post-hoc changes.
