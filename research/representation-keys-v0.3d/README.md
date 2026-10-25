# Representation Keys V0.3D — Fresh Confirmation

Cadence: **0.85.1**

Status: **fresh confirmation PASS**

## Question

Can Cadence's native top-down learned observation code acquire hidden group structure from context alone, when member observations themselves contain no visible group feature?

## Frozen confirmation

V0.3D froze the successful V0.3C design and changed only the founder block.

Fresh founders: `56001..56064` (64 founders).

Primary setup:

- 4 hidden groups × 8 unique member tokens
- member observations share no visible group feature
- 2 PRE and 2 POST context tokens per group
- `learned_code=64`
- `top_down=2`
- 16 parallel streams
- 2 PRE→MEMBER→POST sentences per round
- checkpoints at 64 / 256 / 1024 rounds
- CONTEXT64 / SHUFFLED64 / BOTTOMUP64
- RAW / FIXED64 / FIXED128 controls
- held-out members are heard during unsupervised experience but excluded from the retrieval bank

## Result

The frozen V0.3C result reproduced:

- CONTEXT64 median held-out retrieval: **58.3% → 100% → 100%**
- final SHUFFLED64: **25%**
- final BOTTOMUP64: **25%**
- final FIXED128: **25%**
- CONTEXT64 final retrieval: **100% on all 64 founders**
- CONTEXT64 beat each final control in **64/64 founders**
- median final margin: about **+0.1125**
- median 1024−64 exposure gain: **+0.417**
- every frozen confirmation gate passed

Official classification:

`NATIVE_HIDDEN_GROUP_FRESH_CONFIRMATION_PASS`

## Defensible claim

On Cadence 0.85.1, native top-down learned observation codes can acquire hidden relational structure purely from repeated context. Members with no shared visible group feature become useful context-free memory keys, the effect scales with experience, and it disappears when context is randomized or the top-down boundary is disabled.

## Boundary

This is a representation/memory-key result. Held-out members were heard during unsupervised experience; they were held out from the retrieval bank, not completely unseen observations.
