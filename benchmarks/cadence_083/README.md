# Cadence 0.83 episodic / temporal-context benchmarks

This folder is the public index for the Stone Age V7 series on `cadence-net==0.83.0`.

The strict four-action chain is:

`GATHER_WOOD -> GATHER_STONE -> CRAFT_FIRE -> WARM_UP`

One wrong action fails a strict attempt.

## What is published here

- `v7_0_episodic_memory_ab.py` — runnable V7.0 episodic-memory A/B + clear-ablation source.
- `requirements.txt` — pinned Cadence 0.83 environment.
- [`../../docs/V7_RESULTS.md`](../../docs/V7_RESULTS.md) — consolidated V7.0–V7.4 results.
- [`../../docs/V7_REPRODUCIBILITY.md`](../../docs/V7_REPRODUCIBILITY.md) — frozen protocols, arms, endpoints and interpretation boundaries for V7.0–V7.4.

The later V7.1–V7.4 experiment packages were run from frozen local archives. Their protocol definitions and exact reported outcomes are documented in the files above so the research path is visible without hiding null or negative results.

## V7 sequence

### V7.0 — episodic memory A/B

Fully observed chain, 50 paired seeds.

At ep120:

- memory off: 11/50 robust, 17.242% mean strict
- memory on: 45/50 robust, 85.534% mean strict
- memory on after clearing episodic stores: 6/50 robust, 18.904% mean strict
- independent all-four greedy: 0/50 off, 45/50 on, 0/50 after clear

### V7.1 — ambiguous A-B-A-B lesion probe

Visible observations repeat exactly:

`A -> WOOD, B -> STONE, A -> FIRE, B -> WARM`

Memory clearly helped, but post-training lesions did not cleanly prove acquisition-time necessity of one store.

### V7.2 — training-time context causal test

Native efference disabled in all arms.

- place only: `memory_choice=True, memory_context=0.0`
- temporal context: `memory_choice=True, memory_context=0.5`

At ep120 across 100 paired seeds:

- mean strict: 1.966% place vs 10.039% context
- greedy exact chain: 0/100 place vs 11/100 context, McNemar p=0.000977
- robust lock: 0/100 vs 3/100, p=0.25

### V7.3 — long-horizon confirmation

Same clean place-vs-context comparison, 100 new paired seeds, out to ep240.

At ep240:

- mean strict: 2.512% place vs 16.783% context
- robust lock: 0/100 vs 7/100, p=0.015625
- greedy exact chain: 0/100 vs 21/100, p≈0.000001

### V7.3R — fresh replication

Same protocol, fresh 100 paired seeds.

At ep240:

- mean strict: 2.478% place vs 14.163% context
- robust lock: 0/100 vs 2/100, p=0.5
- greedy exact chain: 0/100 vs 16/100, p=0.000031

The greedy / sampled context effect replicated; the >=50% robust-lock threshold was founder-sensitive.

### V7.4 — generalization boundary

New consecutive-alias structure:

`A -> WOOD, A -> STONE, B -> FIRE, B -> WARM`

At ep240 across 100 fresh paired seeds:

- mean strict: 0.781% place vs 3.465% context
- greedy exact chain: 0/100 place vs 1/100 context, p=1.0
- robust lock: 0/100 in both arms
- sampled strict wins: context 72, place 26, ties 2

The exact greedy generalization endpoint failed, although sampled performance still favored temporal context.

## Current interpretation

The V7 series supports a limited mechanism claim: Cadence 0.83's fixed fading temporal context can causally improve behavior when the current observation is ambiguous, but its exact-sequence benefit depends strongly on the temporal structure of that ambiguity.

This does **not** establish learned attention, learned memory relevance, or general episodic reasoning.
