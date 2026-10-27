# Stone Age V7.15 — Autonomous Goal Routing Bridge

Status: **development complete**

Cadence: **0.88.1**

Official frozen classification:

`TASKED_EXECUTOR_CONTROL_NOT_STABLE`

## Result summary

Fresh founders:
- `80001..80008`
- valid: **8/8**

Autonomous caretaker oracle:
- **384/384**

### AUTONOMOUS_GLOBAL

Final post-replay static medians:
- overall: **100%**
- FOOD route: **100%**
- HUNT route: **100%**
- FIRE route: **100%**
- SHELTER route: **100%**
- NEUTRAL: **100%**

Final autonomous scenario medians:
- FORAGE: **100%**
- HUNT_EAT: **100%**
- FIRE_COLD: **100%**
- FIRE_EVENING: **100%**
- SHELTER_SLEEP: **100%**
- FOOD_THEN_FIRE: **100%**
- HUNT_THEN_SLEEP: **100%**
- ALL_NEEDS: **100%**

Caretaker agreement is also 100% median in every final autonomous scenario.

Founder autonomous readiness:
- **8/8**

This is a strong positive autonomous-arm development result.

### TASKED_SHARED_CONTROL

Standard confirmed V7.14 skill exam:
- FOOD: 100% static / 100% loop
- FIRE: 100% / 100%
- HUNT: 100% / 100%
- SHELTER: 100% / 100%
- standard all-four readiness: **8/8**

Oracle-routed autonomous scenarios:
- FORAGE: 100%
- HUNT_EAT: 100%
- FIRE_COLD: 100%
- FIRE_EVENING: 100%
- SHELTER_SLEEP: 100%
- FOOD_THEN_FIRE: 100%
- HUNT_THEN_SLEEP: **0% median**
- ALL_NEEDS: 100%

Tasked all-scenario readiness:
- **1/8**

Therefore the frozen V7.15 classifier correctly returns:

`TASKED_EXECUTOR_CONTROL_NOT_STABLE`

The official autonomous bridge cannot be declared passed because the predeclared control-stability gate failed.

## Control audit

The failure is highly localized.

In HUNT_THEN_SLEEP:

1. the control correctly begins with `CRAFT_SPEAR`
2. spear crafting consumes 2 wood and 2 stone
3. the scenario intentionally starts with surplus resources: wood=12, stone=6
4. after crafting, the state is:
   - has_spear = 1
   - wood = 10
   - stone = 4
5. the oracle route remains HUNT and the correct next action is `HUNT_RABBIT`

However, 7/8 tasked founders usually choose `CRAFT_SPEAR` again at this state. One founder (80004) generalizes successfully.

This exposes a control-representation mismatch.

The confirmed V7.14 HUNT semantic policy uses the canonical terminal/tool state:

`HUNT_HAS_SPEAR = task=HUNT, wood_ready=0, stone_ready=0, has_spear=1`

In the original V7.14 HUNT episodes, crafting the spear from the minimal prerequisites consumes the resources and naturally produces that canonical state.

V7.15 HUNT_THEN_SLEEP starts with excess resources so, after spear creation, the tasked control adapter exposes:

`task=HUNT, wood_ready=1, stone_ready=1, has_spear=1`

That state is outside the confirmed V7.14 semantic truth table and was not a fair test of the confirmed executor.

AUTONOMOUS_GLOBAL does not have this mismatch because its frozen 26-key curriculum explicitly includes the abundant-resource `HUNT_SLEEP_WITH_SPEAR` state.

## Training trajectory

AUTONOMOUS_GLOBAL is already perfect after static bootstrap.

DAgger64 then destabilizes the policy:
- overall static median: ~71.2%
- FOOD: 75%
- HUNT: 75%
- FIRE: 66.7%
- SHELTER: 91.7%
- NEUTRAL: 0%
- FIRE_COLD loop median: 0%
- HUNT_THEN_SLEEP loop median: 50%
- ALL_NEEDS loop median: 0%

Final reset-matched replay restores:
- all 26 static keys to 100% median
- all routed groups to 100%
- all eight scenario medians to 100%
- all 8 founders to autonomous readiness

This independently extends the V7.14R reconsolidation finding: reset-matched semantic replay can restore a more complex global autonomous policy after DAgger destabilization.

## Scientific interpretation

V7.15 does **not** officially confirm the autonomous bridge because its predeclared tasked-control gate failed.

But the autonomous arm itself gives strong development evidence:

> A plain Cadence brain can map global semantic needs/world state directly to the correct next action across single-goal and multi-goal Stone Age sequences, without an external FOOD/FIRE/HUNT/SHELTER task label.

The failed control is not evidence against autonomous goal routing. It is a mismatch between the V7.14 task-conditioned representation and the surplus-resource HUNT_THEN_SLEEP scenario.

## Next direction

**Stone Age V7.15C — Tasked Control Canonicalization Correction**

Keep the entire autonomous recipe unchanged.

Correct only the oracle-routed TASKED_SHARED_CONTROL adapter so terminal/tool semantic states are canonicalized to the exact confirmed V7.14 policy keys.

For HUNT:
- if `has_spear=True`, encode the canonical HUNT_HAS_SPEAR state regardless of leftover wood/stone

For SHELTER:
- if `shelter_exists=True`, encode the canonical SHELTER_EXISTS state regardless of leftover wood/stone

FOOD remains keyed by food availability.

FIRE terminates when the fire is built, so no post-terminal FIRE query is required.

Recommended fresh founders:
- `81001..81008`

Freeze:
- same AUTONOMOUS_GLOBAL 26-key representation
- same caretaker priority
- same bootstrap/DAgger/replay
- same scenarios and budgets
- same motor primitives
- same gates
- only the tasked-control observation adapter is corrected

If the corrected tasked control is stable and AUTONOMOUS_GLOBAL reproduces its V7.15 performance, classify the bridge under the unchanged autonomous success gates.

No attention, episodic memory, or Cadence 0.89.0 positional recall should be introduced until this correction is resolved.
