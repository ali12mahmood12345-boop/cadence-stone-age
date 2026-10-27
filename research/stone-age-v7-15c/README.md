# Stone Age V7.15C — Tasked Control Canonicalization Correction

Status: **correction protocol / frozen before run**

Cadence: **0.88.1**

V7.15 produced a perfect autonomous arm but failed its frozen control gate because the oracle-routed TASKED_SHARED_CONTROL was exposed to a HUNT state outside the confirmed V7.14 semantic truth table.

V7.15C corrects only that control adapter.

## Fresh founders
`81001..81008`

## AUTONOMOUS_GLOBAL
Unchanged from V7.15:
- same global representation
- same 26 semantic keys
- same priority
- same bootstrap / DAgger / replay
- same eight scenarios and budgets
- same motor primitives and gates

## TASKED_SHARED_CONTROL
Training remains the exact V7.14/V7.15 recipe.

Only the oracle-routed scenario observation adapter changes.

### HUNT canonicalization
If has_spear=False:
- input4 = wood>=2
- input5 = stone>=2
- input6 = 0

If has_spear=True:
- force the confirmed V7.14 HUNT_HAS_SPEAR key:
- input4 = 0
- input5 = 0
- input6 = 1

### SHELTER canonicalization
If shelter_exists=False:
- input4 = wood>=10
- input5 = stone>=4
- input6 = 0

If shelter_exists=True:
- force the confirmed V7.14 SHELTER_EXISTS key:
- input4 = 0
- input5 = 0
- input6 = 1

FOOD and FIRE are unchanged.

## Frozen gates
- >=6/8 valid founders
- autonomous static routed gates unchanged
- every autonomous scenario median >=4/6
- >=6/8 autonomous-ready
- tasked standard V7.14 control stable
- every tasked oracle-routed scenario median >=4/6
- >=6/8 tasked all-scenario ready

## Classification
1. valid<6 -> `INSUFFICIENT_V7_15C_RUNS`
2. corrected control unstable -> `TASKED_CONTROL_CANONICALIZATION_NOT_SUFFICIENT`
3. corrected control stable + autonomous gates pass -> `AUTONOMOUS_GOAL_ROUTING_BRIDGE_PASS`
4. autonomous static fails -> `AUTONOMOUS_ROUTING_ACQUISITION_BOTTLENECK`
5. autonomous static passes but dynamic fails -> `AUTONOMOUS_DYNAMIC_ROUTING_BOTTLENECK`
6. otherwise -> `PARTIAL_AUTONOMOUS_ROUTING_SIGNAL`

No attention, episodic memory, reward learning, or Cadence 0.89.0 positional recall.
No post-hoc changes.
