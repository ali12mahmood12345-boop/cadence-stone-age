# Cadence Research Status

Updated: 2026-10-27

## Confirmed

### Representation Keys V0.3D
Fresh confirmation on Cadence 0.85.1.

### Memory Keys V0.4B
Fresh confirmation on Cadence 0.85.1.

### Stone Age V7.13R
`FIRE_STREAM_STATE_RESET_CONFIRMED`

- 16/16 valid founders
- 16/16 founder readiness
- exact/fresh/loop/ready-to-craft medians 100%
- confirmed controller: semantic FIRE state + committed gather primitive + stream reset before semantic query

## Development results

### Stone Age V7.14
`FOUR_SKILL_SHARED_SEMANTIC_BRIDGE_PASS`

Development panel:
- 8/8 valid founders
- caretaker oracle 192/192
- shared final medians 100% static / 100% loop on FOOD/FIRE/HUNT/SHELTER
- controls final medians 100% / 100% on all four skills
- shared all-four readiness 7/8
- control all-four readiness 8/8
- DAgger destabilized both shared and controls
- final reset semantic replay restored both

## Active confirmation

### Stone Age V7.14R — Fresh Four-Skill Shared Semantic Confirmation

Strict replication only.

Fresh founders:
- 79001..79016

Frozen recipe:
- SHARED4 vs SEPARATE4_CONTROL
- same-base-brain matched initialization
- explicit task one-hot
- same 16 semantic keys
- 64 presentations/key static bootstrap
- DAgger64 per skill
- 64 presentations/key final reset replay
- semantic motor primitives
- brain.reset() before every high-level query
- unchanged FOOD/FIRE/HUNT/SHELTER budgets
- no attention, episodic memory, reward learning, or task-context weakening

Confirmation requires:
- >=12/16 valid founders
- controls stable >=12/16 all-four ready
- all control median static/loop gates pass
- shared all-four readiness >=12/16
- all shared median static/loop gates pass

See: [stone-age-v7-14r](./stone-age-v7-14r/README.md)

Do not open attention/memory or remove explicit task context until V7.14R is complete.
