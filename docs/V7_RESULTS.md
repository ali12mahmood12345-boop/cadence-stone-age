# V7 — Cadence 0.83 episodic and temporal-context results

This document summarizes the Stone Age V7 series run on `cadence-net==0.83.0`.

The purpose of the series was to move from the broad question "does episodic memory help?" toward the narrower mechanism question "does Cadence's fixed fading temporal context itself help when the current observation is insufficient?"

## Strict task

Four required actions:

`GATHER_WOOD -> GATHER_STONE -> CRAFT_FIRE -> WARM_UP`

One wrong action fails a strict attempt.

## V7.0 — episodic memory A/B

Fully observed states, 50 paired seeds, ep120.

| condition | robust | mean strict | independent all-four greedy |
|---|---:|---:|---:|
| memory off | 11/50 | 17.242% | 0/50 |
| memory on | 45/50 | 85.534% | 45/50 |
| memory on, stores cleared for evaluation | 6/50 | 18.904% | 0/50 |

Interpretation: episodic memory produced a very large acquisition advantage, and clearing the stores removed most of the ep120 capability. Because the chain was fully observed, this did not isolate temporal context from place memory.

## V7.1 — ambiguous A-B-A-B lesion probe

Ambiguous visible chain:

`A -> WOOD, B -> STONE, A -> FIRE, B -> WARM`

A(stage0) = A(stage2), and B(stage1) = B(stage3).

At ep120:

| condition | mean strict | robust |
|---|---:|---:|
| memory off | 2.830% | 1/50 |
| intact episodic memory | 22.450% | 9/50 |
| place-store only after lesion | 18.046% | 7/50 |
| context-store only after lesion | 20.924% | 10/50 |
| both stores cleared | 10.704% | 5/50 |

Intact memory vs off: robust paired McNemar p=0.021484; strict wins 41 vs 6, ties 3.

Interpretation: episodic memory clearly helped, but post-training lesions did not cleanly prove acquisition-time necessity of one store because all memory-on brains had trained with both stores intact.

## V7.2 — training-time causal context test

Same ambiguous A-B-A-B task, 100 fresh paired seeds.

Native efference disabled in all arms:

`efference_amplitude=0.0`

Construction-time arms:

- baseline: memory off
- place only: `memory_choice=True, memory_context=0.0`
- temporal context: `memory_choice=True, memory_context=0.5`

### Strict trajectory

| episode | baseline | place only | temporal context |
|---:|---:|---:|---:|
| 10 | 0.140% | 2.160% | 6.220% |
| 20 | 0.100% | 2.600% | 7.270% |
| 40 | 0.180% | 1.660% | 6.165% |
| 60 | 0.255% | 1.855% | 6.890% |
| 80 | 0.235% | 2.035% | 7.525% |
| 120 | 0.434% | 1.966% | 10.039% |

At ep120:

- robust: place 0/100 vs context 3/100, p=0.25
- any greedy exact chain: place 0/100 vs context 11/100, p=0.000977
- sampled strict paired wins: context 74, place 23, ties 3

Interpretation: the pre-registered robust-lock endpoint was too sparse, but the greedy and sampled outcomes strongly favored training with temporal context. Because efference was zero and the arms differed from construction, this was a much cleaner causal test than V7.1.

## V7.3 — long-horizon confirmatory test

Same A-B-A-B task and same place-vs-context construction, 100 fresh paired seeds, extended to ep240.

### Strict trajectory

| episode | place mean | context mean | place median | context median |
|---:|---:|---:|---:|---:|
| 120 | 2.360% | 10.236% | 1.200% | 10.700% |
| 180 | 2.114% | 9.936% | 0.800% | 7.800% |
| 240 | 2.512% | 16.783% | 1.200% | 12.100% |

At ep240:

- robust: place 0/100 vs context 7/100, paired McNemar p=0.015625
- greedy exact chain: place 0/100 vs context 21/100, p≈0.000001
- sampled strict paired wins: context 75, place 21, ties 4

This confirmed the pre-registered strongest endpoint in this founder population.

## V7.3R — fresh replication

Exact V7.3 protocol, another 100 fresh paired seeds.

### Strict trajectory

| episode | place mean | context mean | place median | context median |
|---:|---:|---:|---:|---:|
| 120 | 2.164% | 10.948% | 0.900% | 8.800% |
| 180 | 2.470% | 14.574% | 0.900% | 12.500% |
| 240 | 2.478% | 14.163% | 1.000% | 12.200% |

At ep240:

- robust: place 0/100 vs context 2/100, p=0.5
- greedy exact chain: place 0/100 vs context 16/100, p=0.000031
- sampled strict paired wins: context 78, place 21, ties 1

Interpretation: the reproducible effect is the temporal-context advantage in sequence formation / sampled performance. The >=50% robust-lock threshold is founder-sensitive and did not independently replicate.

## V7.4 — generalization boundary

New ambiguity topology:

`A -> WOOD, A -> STONE, B -> FIRE, B -> WARM`

The aliases are now consecutive rather than separated. Same place-vs-context settings, efference disabled, 100 fresh paired seeds.

### Strict trajectory

| episode | place mean | context mean | place median | context median |
|---:|---:|---:|---:|---:|
| 120 | 0.440% | 1.750% | 0.200% | 1.000% |
| 180 | 0.716% | 2.696% | 0.400% | 1.200% |
| 240 | 0.781% | 3.465% | 0.450% | 1.850% |

At ep240:

- greedy exact chain: place 0/100 vs context 1/100, p=1.0
- robust: 0/100 in both arms
- sampled strict paired wins: context 72, place 26, ties 2

Conditional stage accuracy at ep240:

| condition | S0 A->WOOD | S1 A->STONE | S2 B->FIRE | S3 B->WARM |
|---|---:|---:|---:|---:|
| place only | 39.7% | 56.2% | 31.0% | 43.5% |
| temporal context | 27.0% | 80.8% | 31.1% | 74.8% |

The pre-registered greedy generalization endpoint failed. Temporal context still improved sampled performance and especially the second occurrence of each identical observation, but it almost never formed the full exact greedy sequence.

## Consolidated conclusion

A defensible summary is:

> Cadence 0.83's fixed fading temporal context causally improves behavior in this ambiguous Stone Age sequence benchmark when the current observation alone is insufficient. The effect reproducibly improves sampled performance and exact greedy sequence formation on the separated A-B-A-B structure, but stable high-probability lock-in is founder-sensitive, and exact greedy sequence formation does not generalize cleanly to the consecutive A-A-B-B alias structure.

This is a mechanism result for a controlled micro-benchmark. It is **not** evidence that Cadence has learned attention or learned which memories are relevant. The natural next research problem is selective, learned memory relevance rather than more tuning of this Stone Age benchmark.
