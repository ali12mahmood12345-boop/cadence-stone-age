# Stone Age V7.15C — Tasked Control Canonicalization Correction

Status: **development correction complete**

Cadence: **0.88.1**

Official frozen classification:

`AUTONOMOUS_GOAL_ROUTING_BRIDGE_PASS`

## Purpose

V7.15 produced a perfect autonomous arm but failed its frozen control gate because TASKED_SHARED_CONTROL was evaluated on an out-of-table HUNT terminal/tool state after spear crafting with surplus resources.

V7.15C changed only that tasked-control observation adapter.

AUTONOMOUS_GLOBAL remained unchanged.

Fresh founders:
- `81001..81008`

## Correction

HUNT:
- if `has_spear=False`: encode the ordinary prerequisite bits
- if `has_spear=True`: force the exact canonical V7.14 `HUNT_HAS_SPEAR` key with prerequisite bits 0/0 and tool bit 1

SHELTER:
- if `shelter_exists=False`: encode the ordinary prerequisite bits
- if `shelter_exists=True`: force the exact canonical V7.14 `SHELTER_EXISTS` key with prerequisite bits 0/0 and terminal bit 1

FOOD and FIRE were unchanged.

No autonomous representation, scenario, priority, training, replay, motor primitive, budget, or gate changed.

## Result

All **8/8 founders were valid**.

Autonomous caretaker oracle:
- **384/384**

### AUTONOMOUS_GLOBAL

Final static medians:
- overall: **100%**
- FOOD: **100%**
- HUNT: **100%**
- FIRE: **100%**
- SHELTER: **100%**
- NEUTRAL: **100%**

Final scenario medians:
- FORAGE: **100%**
- HUNT_EAT: **100%**
- FIRE_COLD: **100%**
- FIRE_EVENING: **100%**
- SHELTER_SLEEP: **100%**
- FOOD_THEN_FIRE: **100%**
- HUNT_THEN_SLEEP: **100%**
- ALL_NEEDS: **100%**

Final caretaker agreement:
- **100% median in every scenario**

Founder autonomous readiness:
- **8/8**

### TASKED_SHARED_CONTROL

Standard V7.14 four-skill exam:
- FOOD: **100% static / 100% loop**
- FIRE: **100% / 100%**
- HUNT: **100% / 100%**
- SHELTER: **100% / 100%**

Corrected oracle-routed scenario medians:
- FORAGE: **100%**
- HUNT_EAT: **100%**
- FIRE_COLD: **100%**
- FIRE_EVENING: **100%**
- SHELTER_SLEEP: **100%**
- FOOD_THEN_FIRE: **100%**
- HUNT_THEN_SLEEP: **100%**
- ALL_NEEDS: **100%**

Founder readiness:
- tasked standard: **8/8**
- tasked corrected scenarios: **8/8**

The exact V7.15 control failure is therefore eliminated by canonicalizing terminal/tool task states.

## Training trajectory

AUTONOMOUS_GLOBAL again begins strong after static bootstrap.

After DAgger64, median performance drops sharply:

Static:
- overall: **65.4%**
- FOOD: **81.3%**
- HUNT: **75%**
- FIRE: **66.7%**
- SHELTER: **50%**
- NEUTRAL: **0%**

Scenario medians:
- FORAGE: **100%**
- HUNT_EAT: **91.7%**
- FIRE_COLD: **25%**
- FIRE_EVENING: **100%**
- SHELTER_SLEEP: **0%**
- FOOD_THEN_FIRE: **58.3%**
- HUNT_THEN_SLEEP: **0%**
- ALL_NEEDS: **0%**

Final reset-matched replay restores:
- overall static to **100%**
- every routed static group to **100%**
- every autonomous scenario to **100%**
- every final scenario caretaker agreement to **100%**
- all 8 founders to autonomous readiness

This reproduces the replay-reconsolidation effect on a fresh founder panel.

## Development claim

> A plain Cadence brain can infer the appropriate Stone Age goal from global semantic need/world state and directly select actions across single-goal and multi-goal sequences without receiving an external FOOD/FIRE/HUNT/SHELTER task label.

The matched tasked control is now stable under the same autonomous scenarios, so the V7.15 control objection is resolved.

The current autonomous recipe is:

1. global semantic need/world representation
2. frozen caretaker priority: hunger > fire/warmth > sleep > explore
3. semantic motor primitives
4. stream reset before every high-level query
5. reset-matched replay after DAgger

No attention, episodic memory, reward learning, or recall memory is required for this development bridge.

## Scientific status

V7.15C is a **successful development correction**, not yet the final fresh confirmation of the autonomous bridge.

The autonomous arm was unchanged and reproduced perfectly on fresh founders, which is strong evidence. However the clean next step is a strict larger-panel replication of the corrected full setup.

## Next direction

**Stone Age V7.15R — Fresh Autonomous Goal Routing Confirmation**

Freeze V7.15C exactly:

- AUTONOMOUS_GLOBAL unchanged
- corrected TASKED_SHARED_CONTROL adapter
- same 26 global semantic keys
- same frozen caretaker priority
- same bootstrap
- same DAgger64 per scenario
- same reset replay
- same eight scenarios and budgets
- same semantic motor primitives
- same stream reset
- same gates

Recommended untouched founders:
- `82001..82016`

Confirmation gates:
- >=12/16 valid
- >=12/16 autonomous-ready
- >=12/16 corrected tasked-control all-scenario ready
- all autonomous static medians pass
- all 8 autonomous scenario medians pass
- all tasked standard and corrected-scenario median gates pass

If confirmed, autonomous semantic goal routing can be considered established strongly enough to move to the next frontier.

Only after V7.15R should Cadence 0.89.0 positional recall be opened for genuinely temporal-history tasks.
