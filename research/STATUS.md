# Cadence Research Status

Updated: 2026-10-27

## Confirmed

### Representation Keys V0.3D
Fresh confirmation on Cadence 0.85.1.

### Memory Keys V0.4B
Fresh confirmation on Cadence 0.85.1.

### Stone Age V7.13R
`FIRE_STREAM_STATE_RESET_CONFIRMED`

### Stone Age V7.14R
`FOUR_SKILL_SHARED_SEMANTIC_BRIDGE_CONFIRMED`

## Development results

### Stone Age V7.15
`TASKED_EXECUTOR_CONTROL_NOT_STABLE`

- autonomous arm itself was 8/8 ready with 100% final static/scenario medians
- control failed only on HUNT_THEN_SLEEP because surplus-resource HUNT-with-spear state fell outside confirmed V7.14 canonical task representation

### Stone Age V7.15C — Tasked Control Canonicalization Correction
`AUTONOMOUS_GOAL_ROUTING_BRIDGE_PASS`

Fresh founders:
- 81001..81008
- 8/8 valid

AUTONOMOUS_GLOBAL final:
- overall static median 100%
- FOOD/HUNT/FIRE/SHELTER/NEUTRAL medians 100%
- all 8 autonomous scenario medians 100%
- all final caretaker-agreement medians 100%
- autonomous-ready founders 8/8

TASKED_SHARED_CONTROL:
- standard V7.14 skill medians all 100/100
- corrected oracle-routed scenario medians all 100%
- standard readiness 8/8
- corrected all-scenario readiness 8/8

Correction:
- HUNT + has_spear canonicalized to confirmed HUNT_HAS_SPEAR key
- SHELTER + shelter_exists canonicalized to confirmed SHELTER_EXISTS key
- autonomous arm unchanged
- all other protocol elements unchanged

Training trajectory:
- POST_DAGGER64 autonomous overall static median 65.4%
- FIRE_COLD 25%
- SHELTER_SLEEP 0%
- HUNT_THEN_SLEEP 0%
- ALL_NEEDS 0%
- POST_REPLAY_FULL restores all static/scenario medians to 100%
- replay reconsolidation again reproduced on fresh founders

Interpretation:
The V7.15 control objection is resolved. One plain Cadence brain can autonomously route among FOOD/FIRE/HUNT/SHELTER from global semantic need/world state in this development setup.

See: [stone-age-v7-15c](./stone-age-v7-15c/README.md)

## Next direction

**Stone Age V7.15R — Fresh Autonomous Goal Routing Confirmation**

Strict replication of corrected V7.15C.

Recommended untouched founders:
- 82001..82016

Freeze:
- AUTONOMOUS_GLOBAL
- corrected TASKED_SHARED_CONTROL
- 26 global semantic keys
- caretaker priority
- bootstrap
- DAgger64/scenario
- reset replay
- 8 scenarios/budgets
- semantic motor primitives
- stream reset
- same gates

Confirmation:
- >=12/16 valid
- >=12/16 autonomous-ready
- >=12/16 tasked all-scenario ready
- all autonomous static/scenario median gates pass
- all tasked standard/corrected-scenario median gates pass

Do not open attention, episodic memory, reward learning, or Cadence 0.89.0 positional recall until V7.15R is complete.
