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
- confirmed FIRE controller: semantic state + committed gather primitive + stream reset before semantic query

### Stone Age V7.14R — Fresh Four-Skill Shared Semantic Confirmation
`FOUR_SKILL_SHARED_SEMANTIC_BRIDGE_CONFIRMED`

Strict replication on cadence-net 0.88.1.

Fresh founders:
- 79001..79016

Results:
- valid founders: 16/16
- caretaker oracle: 384/384
- final SHARED medians:
  - FOOD 100% static / 100% loop
  - FIRE 100% / 100%
  - HUNT 100% / 100%
  - SHELTER 100% / 100%
- final CONTROL medians:
  - all four skills 100% / 100%
- SHARED all-four readiness: 16/16
- CONTROL all-four readiness: 16/16
- every final founder-level shared/control static and loop score is 100%
- pairwise SHARED vs CONTROL final scores are 16/16 ties for every skill/metric

Training trajectory:
- STATIC_ONLY is strong
- POST_DAGGER64 transiently destabilizes the policy, especially shared FOOD/FIRE
- POST_REPLAY_FULL restores all 16 shared and control founders completely
- reset-matched semantic replay is therefore a confirmed reconsolidation stage after online correction

Confirmed boundary:
One plain Cadence brain can carry four Stone Age skills simultaneously with explicit task context, semantic state, semantic motor primitives, stream reset at high-level decisions, and replay reconsolidation.

See: [stone-age-v7-14r](./stone-age-v7-14r/README.md)

## Prior development result

### Stone Age V7.14
`FOUR_SKILL_SHARED_SEMANTIC_BRIDGE_PASS`

- development panel 8/8 valid
- shared all-four readiness 7/8
- controls 8/8
- fresh-confirmed by V7.14R

## Next direction

**Stone Age V7.15 — Autonomous Goal Routing Bridge**

Do not simply delete the task one-hot: that would make some semantic states label-ambiguous across FIRE/HUNT/SHELTER.

Instead:
- build a global semantic world/need representation
- freeze a deterministic caretaker priority policy
- let the shared policy infer which goal is active from world needs
- preserve confirmed semantic motor primitives
- preserve stream reset at high-level boundaries
- preserve replay reconsolidation
- no attention or episodic-memory arm yet

Primary question:
Can the shared four-skill policy choose the appropriate goal autonomously rather than receiving FOOD/FIRE/HUNT/SHELTER as an external task label?
