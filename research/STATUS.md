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

### Stone Age V7.16
`POSITIONAL_RECALL_TEMPORAL_HISTORY_BRIDGE_PASS`

Cadence:
- 0.89.0

Fresh founders:
- 83001..83008
- 7/8 paired-valid

POSITION32:
- median overall/FIRST/LAST 100/100/100
- robust 7/7 valid founders
- position maps moved 7/7 valid

POSITION0:
- median overall 47.9%
- FIRST 29.1%
- LAST 69.7%

RECALL_OFF:
- median overall 55.0%
- FIRST 23.6%
- LAST 83.2%
- interpreted as no Recall with default working trace retained

Paired advantage:
- POSITION32 - POSITION0 +52.1 points median
- 7/7 valid founders gain >=15 points
- POSITION32 - RECALL_OFF +45.0 points median

Founder 83007:
- paired-invalid because RECALL_OFF hit a finite free-phase warning
- POSITION32 itself still scored 100/100/100

## Active confirmation

### Stone Age V7.16R — Fresh Positional Recall Temporal-History Confirmation

Strict replication of V7.16.

Fresh founders:
- 84001..84016

Frozen:
- Cadence 0.89.0
- POSITION32 / POSITION0 / RECALL_OFF
- same five-event streams
- first != last
- same 1200 training episodes
- same 240 held-out episodes
- same pairing
- same lesson-before-query-act boundary
- same recency-off setting
- same modules
- same gates

Confirmation requires:
- >=12/16 paired-valid
- POSITION32 median overall/FIRST/LAST >=90%
- >=12 robust POSITION32 founders
- position maps moved >=12 valid founders
- median gain vs POSITION0 >=20 points
- >=12 valid founders gain >=15 points vs POSITION0
- median gain vs RECALL_OFF >=40 points

Target:
`POSITIONAL_RECALL_TEMPORAL_HISTORY_CONFIRMED`

Do not integrate Recall into the full autonomous Stone Age agent until V7.16R is complete.

See: [stone-age-v7-16r](./stone-age-v7-16r/README.md)
