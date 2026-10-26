# Cadence Research Status

Updated: 2026-10-26

## Confirmed

### Representation Keys V0.3D
Fresh confirmation on Cadence 0.85.1.

### Memory Keys V0.4B
Fresh confirmation on Cadence 0.85.1.

### Stone Age V7.13R
`FIRE_STREAM_STATE_RESET_CONFIRMED`

Fresh confirmation:
- 16/16 valid founders
- 16/16 founder readiness
- exact/fresh/loop/ready-to-craft medians 100%
- confirmed recipe: FIRE_MINIMAL + committed gather primitives + stream reset before semantic query

## Development boundary results

### Stone Age V7.14 — Four-Skill Semantic Integration Bridge
`FOUR_SKILL_SHARED_SEMANTIC_BRIDGE_PASS`

- cadence-net 0.88.1
- 8/8 valid founders
- caretaker oracle 192/192
- final SHARED medians:
  - FOOD 100% static / 100% loop
  - FIRE 100% / 100%
  - HUNT 100% / 100%
  - SHELTER 100% / 100%
- final CONTROL medians:
  - all four skills 100% / 100%
- shared all-four readiness: 7/8
- control all-four readiness: 8/8
- frozen bridge gate passed

Key training result:
- DAgger destabilized both SHARED4 and separate controls
- final reset-matched semantic replay restored both
- therefore the DAgger collapse is not uniquely shared-brain interference
- replay is an important reconsolidation stage

Residual miss:
- founder 78001 only
- FIRE ready state `FIRE_W1_S1`: CRAFT_FIRE -> BUILD_SHELTER
- FIRE loop 0/6
- HUNT has one static miss but still loops 6/6
- consistent with a small seed-specific cross-skill semantic collision

See: [stone-age-v7-14](./stone-age-v7-14/README.md)

## Next direction

**Stone Age V7.14R — Fresh Four-Skill Shared Semantic Confirmation**

Strict replication only.

Recommended untouched founders:
- 79001..79016

Freeze:
- SHARED4 vs SEPARATE4_CONTROL
- explicit task context
- 16 semantic keys
- matched base-brain initialization
- static bootstrap
- DAgger64/skill
- full reset semantic replay
- semantic motor primitives
- stream reset before each high-level query
- unchanged skill budgets
- no attention or episodic-memory arm

Confirmation target:
- >=12/16 valid
- controls stable >=12/16
- all shared median static/loop gates pass
- shared all-four readiness >=12/16

Do not open attention/memory or remove task context until V7.14R is complete.
