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

Autonomous arm:
- 8/8 valid founders
- 8/8 autonomous-ready
- final 26-key static medians 100%
- all 8 autonomous scenario medians 100%
- all final caretaker-agreement medians 100%

Control issue:
- standard V7.14 control remains perfect
- HUNT_THEN_SLEEP oracle-routed control fails because surplus resources produce an out-of-table HUNT-with-spear semantic state
- frozen classifier correctly blocks the bridge pass

## Active correction

### Stone Age V7.15C — Tasked Control Canonicalization Correction

Fresh founders:
- 81001..81008

AUTONOMOUS_GLOBAL:
- unchanged from V7.15

TASKED_SHARED_CONTROL:
- training unchanged
- only oracle-routed observation adapter corrected

Canonical correction:
- HUNT + has_spear -> canonical HUNT_HAS_SPEAR key regardless of leftover wood/stone
- SHELTER + shelter_exists -> canonical SHELTER_EXISTS key regardless of leftover resources
- FOOD/FIRE unchanged

All scenarios, budgets, motor primitives, training doses, replay, gates and caretaker priority remain unchanged.

Target classification if both arms satisfy frozen gates:
`AUTONOMOUS_GOAL_ROUTING_BRIDGE_PASS`

No attention, episodic memory, reward learning, or Cadence 0.89.0 positional recall.

See: [stone-age-v7-15c](./stone-age-v7-15c/README.md)
