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

### Stone Age V7.15R
`AUTONOMOUS_GOAL_ROUTING_CONFIRMED`

Strict fresh confirmation on Cadence 0.88.1.

Fresh founders:
- 82001..82016

Results:
- valid founders: 16/16
- caretaker oracle: 768/768
- autonomous final static medians: 100% overall and all routed groups
- all 8 autonomous scenario medians: 100%
- all final autonomous caretaker-agreement medians: 100%
- autonomous-ready founders: 16/16
- corrected tasked all-scenario ready founders: 16/16
- tasked standard medians: 100/100 on all four skills

Minor diagnostic:
- tasked standard all-four readiness 15/16
- founder 82011 has one HUNT static miss but HUNT loop remains 6/6
- this does not affect frozen control confirmation gates

Training trajectory:
- DAgger64 reduces autonomous overall static median to 55.8%
- FIRE_COLD, FOOD_THEN_FIRE, HUNT_THEN_SLEEP and ALL_NEEDS fall to 0% median loop
- full reset semantic replay restores all final static/scenario medians to 100%
- replay reconsolidation is therefore freshly confirmed on the autonomous policy

Confirmed boundary:
A plain Cadence brain can autonomously route among FOOD/FIRE/HUNT/SHELTER from current global semantic need/world state without external task identity.

See: [stone-age-v7-15r](./stone-age-v7-15r/README.md)

## Next direction

**Stone Age V7.16 — Positional Recall Temporal-History Bridge**

Move to Cadence 0.89.0.

Primary comparison:
- recall_position=0
- recall_position=32

Keep the confirmed autonomous semantic executor as the stable base.

Construct tasks where:
- current visible semantic state is identical across conditions
- correct action depends only on temporal history / event order
- a current-state-only policy cannot solve the task by construction

First positional-recall experiment should not add attention, reward learning, or unrelated representation changes.
