# Cadence Research Status

Updated: 2026-10-25

## Confirmed

### Representation Keys V0.3D
Fresh confirmation on Cadence 0.85.1.

- 64/64 fresh founders completed.
- Context-derived native learned keys reached 100% final hidden-group retrieval.
- Shuffled-context, bottom-up and fixed controls stayed at chance.
- Official classification: `NATIVE_HIDDEN_GROUP_FRESH_CONFIRMATION_PASS`.

See: [representation-keys-v0.3d](./representation-keys-v0.3d/README.md)

### Memory Keys V0.4B
Fresh confirmation on Cadence 0.85.1.

- 63/64 founders valid.
- Native context-derived keys transferred a stored action to held-out members at 100% median accuracy.
- Shuffled, bottom-up, fixed and raw controls were 25%.
- Whole-brain behavior was 100% with the associative memory active and 25% after `hippocampus.clear()`.
- Official classification: `NATIVE_KEY_ASSOCIATIVE_MEMORY_FRESH_CONFIRMATION_PASS`.

See: [memory-keys-v0.4b](./memory-keys-v0.4b/README.md)

## Development boundary results

### Attention V0.5A
`NO_CONJUNCTIVE_MULTI_FACT_SIGNAL`

### Stone Age V7
`NO_STONE_AGE_MEMORY_ATTENTION_ADVANTAGE`

### Stone Age V7.1
`NO_STONE_AGE_ACQUISITION_READINESS`

### Stone Age V7.2
`STONE_AGE_BASIC_ACQUISITION_BOTTLENECK`

### Stone Age V7.3 — Balanced Teaching / State Contrast
`PERSISTENT_STATIC_ACQUISITION_BOTTLENECK`

- 8/8 founders valid.
- LEGACY_BALANCED exact/fresh medians:
  - FOOD 50/50%
  - FIRE 33.3/33.3%
  - HUNT 50/49.3%
  - SHELTER 66.7/66.7%
- DOC_BATCH32 did not rescue acquisition and was often worse.
- DOC_BATCH32_CONTRAST also did not pass.
- Important boundary: contrast was only tested on the weak short-budget batch route, so V7.3 does not independently rule out state contrast.
- Cadence's teaching guide indicates the normalized batch point is intended for many-lesson imitation; with few hundred corrections, founder teaching can acquire faster.

See: [stone-age-v7-3](./stone-age-v7-3/README.md)

## Next direction

**Stone Age V7.4 — Few-Lesson Teaching Regime Isolation**

Keep the balanced single-skill static datasets fixed and compare short-budget teaching regimes, especially the founder teaching point, before revisiting state contrast or closed-loop acquisition.

Attention/episodic-memory comparisons remain closed until static acquisition is solved.
