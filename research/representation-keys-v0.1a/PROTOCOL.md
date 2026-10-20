# Frozen Protocol — Representation Keys V0.1A

## Scope

Development proof-of-principle for learned internal representations as memory keys. No Cadence default change. No core-memory modification. No confirmation claim.

## Runtime

- cadence-net 0.84.3
- NumPy >=2,<3
- CPU default backend

## Seeds

Fresh founder seeds: 45001 through 45024 inclusive.

## World

Four latent concepts, labels/actions 0..3.

Each 36-dimensional observation is:

- semantic block `x[0:4]`: one-hot concept identity, amplitude 1.0;
- nuisance block `x[4:36]`: 32 independent `Uniform(-0.7,+0.7)` values.

Training, policy test, memory bank and memory query sets use independent deterministic RNG streams for each founder.

## Brain

`Brain.compose(inputs=36, actions=4, modules=(24,12), seed=founder, recall=False)` using released defaults.

The exact initial brain is checkpointed before learning. Supervised task learning uses `Brain.lesson` on 256 balanced batches of 32 rows (8 rows per concept) for 8192 presentations total. The brain is reset before each independent batch.

## Frozen representation read

On a saved copy:

1. reset;
2. `act(observation, greedy=True)`;
3. read `basal_ganglia.state.activation[association_index]`;
4. L2 normalize only for cosine retrieval.

Greedy probes operate on copies and never change the trained source brain.

## Memory retrieval

Memory bank: 4 independent variants/concept = 16 keys.
Query set: 64 independent variants/concept = 256 queries.

For each key arm, normalize bank/query vectors and choose the bank item with maximum cosine similarity. Payload is the bank concept identity. Score is top-1 concept retrieval accuracy.

Arms:

- RAW: 36-value observation.
- FIXED_SPARSE: `observation_code` from untrained `Brain.compose(..., code=128)`.
- UNTRAINED_ASSOC: 12-value association state from exact pre-learning founder.
- TRAINED_ASSOC: 12-value association state after teaching.

Also report mean query margin: max cosine to a same-concept bank key minus max cosine to a different-concept bank key.

## Eligibility

Trained policy held-out greedy accuracy >= 0.85 on 256 fresh observations.

## Frozen primary classification

Minimum eligible founders: 12.

Among eligible founders:

- TRAINED_ASSOC > UNTRAINED_ASSOC accuracy in >=2/3;
- median(TRAINED_ASSOC - UNTRAINED_ASSOC) >= +0.10;
- TRAINED_ASSOC > RAW accuracy in >=2/3;
- median(TRAINED_ASSOC - RAW) >= +0.10;
- median TRAINED_ASSOC retrieval accuracy >= 0.80.

If all pass: `LEARNED_COMPACT_KEY_SIGNAL`.

If too few founders learn the task: `INSUFFICIENT_TASK_LEARNING`.

If trained association beats its exact untrained founder but fails the RAW comparison: `LEARNED_REPRESENTATION_CHANGED_BUT_NO_RAW_KEY_GAIN`.

Otherwise: `NO_LEARNED_KEY_SIGNAL`.

FIXED_SPARSE is descriptive and cannot rescue or fail the primary gate.

## Interpretation boundary

A positive V0.1A says task learning created a compact association representation that is useful as a similarity key for held-out nuisance variants in this aligned concept/action task. It does not establish a general memory architecture, semantic abstraction, compositional representation, or preservation of task-irrelevant identity.
