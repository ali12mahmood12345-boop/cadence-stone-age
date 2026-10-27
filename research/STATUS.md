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

- 16/16 valid founders
- SHARED all-four readiness 16/16
- CONTROL all-four readiness 16/16
- final shared/control static and loop scores 100%

## Development results

### Stone Age V7.15 — Autonomous Goal Routing Bridge
`TASKED_EXECUTOR_CONTROL_NOT_STABLE`

Fresh founders:
- 80001..80008
- 8/8 valid

AUTONOMOUS_GLOBAL final:
- 26-key overall static median 100%
- FOOD/HUNT/FIRE/SHELTER/NEUTRAL medians 100%
- all 8 autonomous scenario loop medians 100%
- all 8 scenario caretaker-agreement medians 100%
- autonomous-ready founders 8/8

TASKED_SHARED_CONTROL:
- standard V7.14 four-skill exam remains 100/100 on all skills
- standard all-four readiness 8/8
- oracle-routed scenarios pass 7/8 families
- HUNT_THEN_SLEEP median 0%
- all-scenario ready founders only 1/8

Frozen control gate therefore fails and official classification remains TASKED_EXECUTOR_CONTROL_NOT_STABLE.

Control audit:
- HUNT_THEN_SLEEP begins with surplus wood/stone
- after CRAFT_SPEAR the tasked control sees has_spear=1 while wood/stone prerequisite bits remain 1/1
- confirmed V7.14 HUNT canonical terminal state is has_spear=1 with prerequisite bits 0/0
- 7/8 tasked founders therefore encounter an out-of-table HUNT semantic state and usually repeat CRAFT_SPEAR
- founder 80004 generalizes successfully
- AUTONOMOUS_GLOBAL explicitly contains the abundant-resource HUNT-with-spear state and succeeds 8/8

Training trajectory:
- AUTONOMOUS_GLOBAL static bootstrap is strong
- DAgger destabilizes global routing
- final reset semantic replay restores all static/scenario medians to 100%
- replay reconsolidation therefore generalizes beyond externally tasked four-skill execution

See: [stone-age-v7-15](./stone-age-v7-15/README.md)

## Next direction

**Stone Age V7.15C — Tasked Control Canonicalization Correction**

Fresh founders:
- recommended 81001..81008

Keep autonomous arm unchanged.

Only correct the tasked-control observation adapter:
- HUNT + has_spear -> canonical HUNT_HAS_SPEAR key regardless of surplus resources
- SHELTER + shelter_exists -> canonical SHELTER_EXISTS key regardless of surplus resources
- preserve all V7.15 scenarios, budgets, autonomous representation, training and gates

Do not add attention, episodic memory, reward learning, or Cadence 0.89.0 positional recall until the corrected control is resolved.
