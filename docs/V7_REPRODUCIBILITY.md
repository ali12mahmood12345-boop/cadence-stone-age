# V7 reproducibility notes

The V7 Stone Age series uses `cadence-net==0.83.0` and the strict four-action chain:

`GATHER_WOOD -> GATHER_STONE -> CRAFT_FIRE -> WARM_UP`

Unless otherwise noted, a strict attempt fails on the first wrong action.

## Common training setup

- modules: `(48, 24)`
- action space: five actions (`GATHER_WOOD`, `GATHER_STONE`, `CRAFT_FIRE`, `WARM_UP`, `WAIT`)
- selective caregiver schedule: 4 guided decisions / 8 autonomous decisions
- terminal reward: `+2` for success, `-1` for failed attempt
- maximum decisions per attempt: 10
- paired founder seeds within each comparison

## V7.0

Fully observed chain, 50 paired seeds, checkpoints 10/20/40/60/80/120.

- MEMORY_OFF: no `memory_choice`
- MEMORY_ON: `memory_choice=True`
- frozen native efference: amplitude `0.5`, decay `0.2`
- evaluation-time ablation clears `hippocampus` and `context_memory` on a saved evaluation clone only

## V7.1

Ambiguous visible chain:

`A -> WOOD, B -> STONE, A -> FIRE, B -> WARM`

- A(stage0) and A(stage2) are byte-identical observations
- B(stage1) and B(stage3) are byte-identical observations
- memory-off vs memory-on training
- memory-on evaluation modes: intact, place-only, context-only, none
- post-training lesions only; training brain is not modified by evaluation

## V7.2

Training-time causal comparison on the same A-B-A-B ambiguity.

100 paired seeds, checkpoints 10/20/40/60/80/120.

All arms set native efference to zero:

`efference_amplitude=0.0`

Arms:

- BASELINE: `memory_choice=False`
- PLACE_ONLY: `memory_choice=True, memory_context=0.0`
- TEMPORAL_CONTEXT: `memory_choice=True, memory_context=0.5`

Primary pre-registered endpoint: ep120 robust-lock frequency, context vs place.

## V7.3

Long-horizon confirmatory A-B-A-B test.

100 fresh paired seeds, checkpoints 120/180/240.

- PLACE_ONLY: `memory_choice=True, memory_context=0.0`
- TEMPORAL_CONTEXT: `memory_choice=True, memory_context=0.5`
- `efference_amplitude=0.0` in both arms
- continuous training brain across checkpoints

Pre-registered primary: ep240 ROBUST_LOCK context vs place, exact paired McNemar.

ROBUST_LOCK means:

- greedy exact-chain pass, and
- sampled strict exact-chain success >= 50%

## V7.3R

Exact V7.3 protocol with a completely fresh set of 100 paired founders.

Only seed identities / output labels changed.

## V7.4

Generalization test with a different alias topology:

`A -> WOOD, A -> STONE, B -> FIRE, B -> WARM`

The two A observations are byte-identical and consecutive; the two B observations are byte-identical and consecutive.

100 fresh paired seeds, checkpoints 120/180/240.

- PLACE_ONLY: `memory_choice=True, memory_context=0.0`
- TEMPORAL_CONTEXT: `memory_choice=True, memory_context=0.5`
- `efference_amplitude=0.0` in both arms

Pre-registered primary: ep240 any greedy exact-chain pass, context vs place, exact paired McNemar.

## Interpretation boundary

These experiments test the behavior of Cadence 0.83's current episodic and fixed fading temporal-context mechanisms in a controlled micro-benchmark. They do not establish learned attention, learned relevance selection, or general episodic reasoning.
