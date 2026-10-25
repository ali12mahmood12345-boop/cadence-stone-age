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

## Running

### Attention V0.5A — Conjunctive Multi-Fact Memory
Cadence 0.88.0 development assay.

This targets the release boundary where one fact matters only together with another.

- H2: `attention=True, recall_heads=2`
- H1 matched control: `recall_heads=1`
- answer rule: `(role0_value + role1_value) % 3`
- either relevant fact alone is exactly 33.3% chance by construction
- 18 taught and 18 held answer-pair combinations
- causal role-record erasures
- distractor erasure
- complete Recall erasure
- cloned-head address-map lesion

Fresh development founders: `59001..59008`.

Status: **running; no result claimed yet**.

See: [attention-v0.5a](./attention-v0.5a/README.md)
