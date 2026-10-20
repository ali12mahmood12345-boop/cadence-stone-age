# Cadence Representation Keys V0.1A

## Learned Compact Key — Proof of Principle

This is a small development experiment motivated by Bernhard Mueller's suggestion to use a **learned, smaller internal representation of an observation as a memory key**, rather than keying memory only on the raw observation.

The question is deliberately narrow:

> After Cadence learns a nuisance-variable task, does its learned internal association state become a better similarity key for held-out variants than the raw observation or the same founder's untrained association state?

This is **development evidence only**. It does not modify Cadence core memory and it is not a confirmation or default-change proposal.

## Result

Cadence version: `0.84.3`  
Fresh founders: `45001..45024`

Of 24 founders, **22 passed the frozen task-learning eligibility gate** (`>=85%` held-out policy accuracy). Median held-out policy accuracy among eligible founders was **99.6%**.

| Memory key | Median held-out retrieval |
|---|---:|
| RAW observation | 71.9% |
| FIXED_SPARSE observation code (128) | 77.1% |
| UNTRAINED_ASSOC (12 neurons) | 51.6% |
| **TRAINED_ASSOC (12 neurons)** | **99.0%** |

Across the 22 eligible founders:

- `TRAINED_ASSOC > UNTRAINED_ASSOC`: **22/22**
- median gain over exact untrained founder: **+47.3 percentage points**
- `TRAINED_ASSOC > RAW`: **22/22**
- median gain over RAW: **+26.6 percentage points**
- median gain over FIXED_SPARSE: **+21.7 percentage points** (descriptive)

Frozen development classification:

**`LEARNED_COMPACT_KEY_SIGNAL`**

## World

Each observation has 36 values:

- 4 stable semantic coordinates: one-hot concept identity
- 32 independent nuisance coordinates sampled from `Uniform(-0.7, +0.7)`

There are 4 concepts and 4 actions.

Cadence uses:

```text
Brain.compose(inputs=36, actions=4, modules=(24,12), ...)
```

The final 12-neuron association region is treated as the candidate compact representation.

Training uses 8,192 balanced supervised presentations. Evaluation uses entirely fresh nuisance variants.

## Compared key representations

1. **RAW** — 36-dimensional observation.
2. **FIXED_SPARSE** — Cadence's existing fixed `observation_code` from an untrained `code=128` brain.
3. **UNTRAINED_ASSOC** — 12-neuron association activity from the exact founder before task learning.
4. **TRAINED_ASSOC** — the same 12-neuron association activity after task learning.

Bank/query retrieval is nearest-key cosine similarity. The memory bank contains 4 fresh variants per concept; the query set contains 64 fresh variants per concept.

The exact `UNTRAINED_ASSOC` vs `TRAINED_ASSOC` comparison is the main learning control.

## Frozen gate

A founder is analyzed only if its learned policy reaches `>=85%` held-out accuracy.

`LEARNED_COMPACT_KEY_SIGNAL` required all of the following:

- at least 12 eligible founders;
- TRAINED_ASSOC beats UNTRAINED_ASSOC in at least 2/3 of eligible founders;
- median TRAINED_ASSOC − UNTRAINED_ASSOC retrieval >= `+0.10`;
- TRAINED_ASSOC beats RAW in at least 2/3;
- median TRAINED_ASSOC − RAW retrieval >= `+0.10`;
- median TRAINED_ASSOC retrieval >= `0.80`.

All frozen gates passed.

## Important limitation

In V0.1A, **concept identity equals taught action**. Therefore a trained association state can succeed by compressing observations toward the policy class. This does **not** yet show that the representation preserves distinctions that are irrelevant to the current policy but important to memory.

The next experiment should therefore be a collision test where **multiple distinct memory identities share the same action**. If the trained association key still separates those identities, it is much stronger evidence that it can serve as a general learned memory key. If it collapses them, the result would instead argue for a dedicated learned memory-key representation/objective rather than directly reusing the policy representation.

## Reproduction

Windows:

```text
START_REPRESENTATION_KEYS_V0_1A.bat
```

Dependencies:

```text
cadence-net==0.84.3
numpy>=2.0,<3
```

The launcher creates a private virtual environment, runs the API/representation smoke test, then runs the experiment.

A Cadence warning about some finite teaching free phases reaching their `free_steps` budget was observed during the run. V0.1A therefore remains development evidence; a follow-up should explicitly tighten settlement qualification/budget and record residual/refusal statistics.

## Files

- `representation_keys_v0_1a.py` — experiment
- `smoke_test_v0_1a.py` — API + association-state smoke test
- `PROTOCOL.md` — frozen protocol
- `results/REPRESENTATION_KEYS_V0_1A_REPORT.txt` — compact final report
- `results/REPRESENTATION_KEYS_V0_1A_RESULTS.json` — complete machine-readable results
- `results/REPRESENTATION_KEYS_V0_1A_SUMMARY.csv` — per-founder summary

## Interpretation boundary

A positive V0.1A means task learning produced a compact association representation that was useful as a similarity key for held-out nuisance variants in this aligned concept/action chamber.

It does **not** establish a general memory architecture, semantic abstraction, compositional representation, preservation of task-irrelevant identity, or a reason to change Cadence defaults.
