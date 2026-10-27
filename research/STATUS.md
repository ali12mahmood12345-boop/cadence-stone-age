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

### Stone Age V7.16R
`POSITIONAL_RECALL_TEMPORAL_HISTORY_CONFIRMED`

Cadence:
- 0.89.0

Strict fresh V7.16 replication:
- exact run_founder reused unchanged
- founders 84001..84016
- 14/16 paired-valid
- minimum 12/16

POSITION32 medians:
- overall 100%
- FIRST 100%
- LAST 100%

POSITION0 medians:
- overall 48.8%
- FIRST 23.8%
- LAST 70.4%

RECALL_OFF medians:
- overall 51.2%
- FIRST 20.9%
- LAST 82.4%

Paired positional advantage:
- POSITION32 - POSITION0 median +50.2 points
- 14/14 paired-valid founders gain >=15 points
- POSITION32 - RECALL_OFF median +47.3 points

Position evidence:
- maps moved 14/14 paired-valid founders
- both cues >=80% in 13/14 paired-valid founders

Founder audit:
- 84011 paired-invalid only because RECALL_OFF hit finite free-phase warning at lesson 825; POSITION32 itself 100/100/100
- 84013 paired-invalid only because RECALL_OFF hit same warning at lesson 916; POSITION32 itself 100/100/100
- 84016 is the only valid POSITION32 robustness miss: overall 77.9%, FIRST 59.2%, LAST 96.7%, maps moved

All frozen confirmation gates passed.

Interpretation:
Cadence 0.89.0 learned positional Recall is confirmed on the bounded five-event Stone Age FIRST/LAST temporal-history task.

See: [stone-age-v7-16r](./stone-age-v7-16r/README.md)

## Next direction

**Stone Age V7.17 — Autonomous Temporal-Memory Integration Bridge**

Use Cadence 0.89.0.

Keep the V7.15R autonomous semantic controller as the stable base.

Introduce only memory-dependent branches where:
- current semantic observation is identical
- correct next action depends on recent event/order
- current-state policy is impossible by construction

Compare:
- POSITION32 autonomous memory
- POSITION0 matched Recall control
- CURRENT_STATE control

Do not add episodic memory, multi-head attention, reward learning, or unrelated representation changes in the first integration experiment.
