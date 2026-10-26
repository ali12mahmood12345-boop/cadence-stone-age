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

## Active development experiment

### Stone Age V7.14 — Four-Skill Semantic Integration Bridge

Fresh founders:
- 78001..78008

Question:
Can one plain Cadence brain retain and execute FOOD, FIRE, HUNT and SHELTER together when task identity and semantic controller boundaries are explicit?

Arms:
- SHARED4
- SEPARATE4_CONTROL

Shared representation:
- explicit one-hot task context
- compact semantic prerequisite state
- no nuisance-heavy raw state

Controller:
- reset before every semantic high-level query
- temporally extended primitives for persistent actions
- unchanged skill-specific window budgets

Training:
- complete 16-key semantic truth table
- 64 presentations/key static bootstrap
- DAgger64 per skill
- 64 presentations/key final replay
- reset before every independent static lesson

Primary bridge gate:
- controls stable in >=6/8 founders
- shared medians pass all four skill static and loop gates
- shared all-four founder readiness >=6/8

No attention or episodic-memory arm in V7.14.

See: [stone-age-v7-14](./stone-age-v7-14/README.md)
