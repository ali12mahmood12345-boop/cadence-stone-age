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

- 16/16 valid
- caretaker oracle 768/768
- autonomous-ready 16/16
- corrected tasked scenario-ready 16/16
- all final autonomous static/scenario medians 100%
- replay reconsolidation confirmed again after DAgger destabilization

## Active development experiment

### Stone Age V7.16 — Positional Recall Temporal-History Bridge

Cadence:
- 0.89.0

Fresh founders:
- 83001..83008

Arms:
- POSITION32
- POSITION0
- RECALL_OFF

Task:
- stream five Stone Age resource events
- first and last forced different
- identical FIRST/LAST query observations
- answer with the semantic action matching the queried endpoint resource

Purpose:
- make current-state inference impossible by construction
- isolate learned slot-age positional recall
- compare Cadence 0.89.0 founder position term against the same Recall memory with position disabled

Training:
- 1200 episodes/founder/arm
- only query moment taught
- lesson before query act
- recency off
- no episodic memory or reward learning

Testing:
- 240 held-out episodes/founder/arm

Primary pass:
`POSITIONAL_RECALL_TEMPORAL_HISTORY_BRIDGE_PASS`

See: [stone-age-v7-16](./stone-age-v7-16/README.md)
