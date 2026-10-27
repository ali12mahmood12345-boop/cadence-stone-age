# Stone Age V7.15R — Fresh Autonomous Goal Routing Confirmation

Status: **fresh confirmation complete**

Cadence: **0.88.1**

Official frozen classification:

`AUTONOMOUS_GOAL_ROUTING_CONFIRMED`

## Purpose

V7.15R was a strict fresh replication of the corrected V7.15C setup.

No representation, controller, scenario, training, replay, control-adapter, or gate changes were introduced.

Fresh founders:
- `82001..82016`

## Result

Valid founders:
- **16/16**

Autonomous caretaker oracle:
- **768/768**

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
- **100% median on all eight scenarios**

Founder autonomous readiness:
- **16/16**
- frozen requirement: >=12/16

### TASKED_SHARED_CONTROL

Standard four-skill medians:
- FOOD: **100% static / 100% loop**
- FIRE: **100% / 100%**
- HUNT: **100% / 100%**
- SHELTER: **100% / 100%**

Corrected oracle-routed scenario medians:
- all eight scenarios: **100%**

Founder corrected all-scenario readiness:
- **16/16**
- frozen requirement: >=12/16

Tasked standard all-four readiness:
- **15/16** diagnostic only

The only standard-control miss was founder **82011**:
- HUNT static accuracy: 80%
- missed key: `HUNT_W0_S0_NO_SPEAR`
- target: `GATHER_STONE`
- prediction: `GATHER_WOOD`
- HUNT loop still: 6/6
- corrected autonomous-scenario control remains fully ready

This does not affect the frozen confirmation because the predeclared control gate uses standard median gates plus corrected all-scenario readiness, and all those gates pass.

## Training trajectory

STATIC_ONLY:
- autonomous static medians: 100%
- autonomous scenario medians: 100%

POST_DAGGER64:
- overall static median: **55.8%**
- FOOD: **68.8%**
- HUNT: **75%**
- FIRE: **50%**
- SHELTER: **66.7%**
- NEUTRAL: **0%**

Scenario medians after DAgger:
- FORAGE: 100%
- HUNT_EAT: 100%
- FIRE_COLD: 0%
- FIRE_EVENING: 100%
- SHELTER_SLEEP: 100%
- FOOD_THEN_FIRE: 0%
- HUNT_THEN_SLEEP: 0%
- ALL_NEEDS: 0%

POST_REPLAY_FULL:
- all routed static medians restored to **100%**
- all eight autonomous scenario medians restored to **100%**
- all final caretaker-agreement medians restored to **100%**
- autonomous readiness restored to **16/16**

This is now a fresh confirmation that reset-matched semantic replay acts as a robust reconsolidation stage after DAgger destabilization.

## Confirmed finding

> One plain Cadence brain can autonomously choose among FOOD, FIRE, HUNT and SHELTER from global semantic world/need state, including multi-goal sequences, without receiving an external task label.

Confirmed recipe:
1. global semantic need/world representation
2. deterministic priority: hunger > fire/warmth > sleep > explore
3. semantic motor primitives
4. stream reset before each high-level query
5. reset-matched semantic replay after DAgger

No attention, episodic memory, reward learning, or recall memory was needed for this confirmation.

## Scientific boundary

This confirmation does **not** test memory-dependent temporal ambiguity.

All successful decisions remain inferable from the current global semantic observation.

Therefore the next meaningful frontier should require two or more situations with the **same current observation but different correct actions depending on temporal history**.

## Next direction

**Stone Age V7.16 — Positional Recall Temporal-History Bridge**

Move to **Cadence 0.89.0** and explicitly test the new positional recall mechanism.

Recommended controlled comparison:
- `RECALL_POSITION_0`
- `RECALL_POSITION_32`

Keep the present autonomous semantic executor as the stable base.

Design history-dependent tasks where:
- visible current semantic state is intentionally identical
- correct action depends on which event happened earlier / later
- current-state-only policy cannot solve the task by construction

Examples:
- choose action based on whether wood or stone was gathered most recently
- distinguish first vs last encountered resource
- remember which need became urgent first
- act differently after identical current states depending on recent goal sequence

Do not mix attention, reward learning, or further representation changes into the first positional-recall test.
