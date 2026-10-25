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

### Stone Age V7.2 — Acquisition Microscope
`STONE_AGE_BASIC_ACQUISITION_BOTTLENECK`

- 8/8 founders valid.
- Single-skill final exact/static/loop:
  - FOOD 54.2/50.0/0%
  - FIRE 41.9/33.3/0%
  - HUNT 72.7/66.7/100%
  - SHELTER 72.7/66.7/0%
- Shared final exact/static/loop:
  - FOOD 50.0/50.0/0%
  - FIRE 29.0/33.3/0%
  - HUNT 50.8/50.0/0%
  - SHELTER 66.7/66.7/0%
- Prototype diagnostics show terminal-action collapse:
  prerequisite states are often read back as the later terminal action.
- HUNT is an important exception: the separate HUNT brain reaches 100% closed-loop, while shared HUNT stays 0%, showing secondary cross-skill interference.

See: [stone-age-v7-2](./stone-age-v7-2/README.md)

## Next direction

**Stone Age V7.3 — State Contrast / Balanced Acquisition**

First remove terminal-action exposure imbalance and test whether adjacent Stone Age states can be retained as distinct action mappings.

Only if balanced exposure still fails should observation contrast be amplified diagnostically.

Attention/episodic-memory comparisons remain closed until basic acquisition is solved.
