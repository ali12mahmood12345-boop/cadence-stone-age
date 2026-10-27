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

## Development results

### Stone Age V7.16 — Positional Recall Temporal-History Bridge
`POSITIONAL_RECALL_TEMPORAL_HISTORY_BRIDGE_PASS`

Cadence:
- 0.89.0

Fresh founders:
- 83001..83008
- 7/8 paired-valid
- minimum valid 6/8

POSITION32 medians:
- overall 100%
- FIRST 100%
- LAST 100%
- both-cue robust founders 7/7 valid
- position maps moved 7/7 valid

POSITION0 medians:
- overall 47.9%
- FIRST 29.1%
- LAST 69.7%

RECALL_OFF medians:
- overall 55.0%
- FIRST 23.6%
- LAST 83.2%

Paired advantage:
- POSITION32 - POSITION0 median +52.1 points
- 7/7 valid founders gain >=15 points
- POSITION32 - RECALL_OFF median +45.0 points

Founder 83007:
- paired-invalid only because RECALL_OFF hit a finite free-phase settling warning at lesson 1010
- POSITION32 itself completed and scored 100% overall/FIRST/LAST with position maps moved

Baseline interpretation correction:
- RECALL_OFF is a no-Recall baseline, not truly present-only
- default working trace remains active
- this likely explains strong LAST / weak FIRST asymmetry
- main causal result remains POSITION32 vs POSITION0, where only recall_position differs

All frozen V7.16 gates passed.

Interpretation:
Cadence 0.89.0 learned positional Recall can retrieve a resource event by temporal endpoint in this bounded five-event task.

See: [stone-age-v7-16](./stone-age-v7-16/README.md)

## Next direction

**Stone Age V7.16R — Fresh Positional Recall Temporal-History Confirmation**

Recommended untouched founders:
- 84001..84016

Strict V7.16 replication:
- same POSITION32 / POSITION0 / RECALL_OFF arms
- same training/test episodes and pairing
- same five-event FIRST/LAST task
- same recency-off setting
- same lesson-before-query-act boundary
- same gates

Documentation only:
- describe RECALL_OFF correctly as no Recall with default working trace retained

Target confirmation:
`POSITIONAL_RECALL_TEMPORAL_HISTORY_CONFIRMED`

Do not integrate Recall into full autonomous Stone Age survival until V7.16R is complete.
