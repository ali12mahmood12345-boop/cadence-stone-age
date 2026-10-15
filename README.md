# Cadence Stone Age Research Environment

A Stone Age survival environment and a sequence of controlled Cadence benchmarks used to study prerequisite chains, interference, action history, episodic memory, and temporal context.

The project started as a visual survival game and was progressively reduced into controlled chambers so individual learning mechanisms could be measured.

## Current result: Cadence 0.83 episodic / temporal-context series

The latest consolidated result is here:

[`docs/V7_RESULTS.md`](docs/V7_RESULTS.md)

Protocol details are here:

[`docs/V7_REPRODUCIBILITY.md`](docs/V7_REPRODUCIBILITY.md)

The key strict chain is:

`GATHER_WOOD -> GATHER_STONE -> CRAFT_FIRE -> WARM_UP`

with repeated visible observations in the ambiguous tests so the current observation alone cannot determine the correct action.

### Main finding

With native efference history disabled, training with Cadence 0.83 temporal context (`memory_context=0.5`) reproducibly outperformed place episodic memory alone (`memory_context=0.0`) on the separated `A-B-A-B` ambiguity structure.

Across two independent 100-seed long-horizon populations at episode 240:

- place-only produced **0/100** greedy exact chains in both runs
- temporal context produced **21/100** and **16/100** greedy exact chains
- sampled strict performance strongly favored temporal context in both runs
- robust >=50% lock-in occurred, but was founder-sensitive (7/100 in one run, 2/100 in the replication)

A final generalization test changed the structure to consecutive aliases, `A-A-B-B`. Temporal context still improved sampled performance, but the exact greedy-chain advantage did not generalize: 1/100 context vs 0/100 place at episode 240.

The resulting boundary is useful: the fixed fading temporal trace genuinely helps disambiguation, but it is not a general solution to sequence memory.

## Earlier 0.81 work

The original controlled 0.81 experiments remain in:

[`benchmarks/cadence_081/`](benchmarks/cadence_081/)

Historical results are in:

[`docs/RESULTS.md`](docs/RESULTS.md)

The 0.81 series established the earlier problems around prerequisite-chain interference, retention, backward lessons, and over-drilling.

## Main survival environment

The original visual environment is in:

`stone_age_game/main.py`

It contains trees, rocks, berries, rabbits, hunger, warmth, energy, fire, spear crafting, shelter, sleep, and a day/night cycle.

The game is retained as the environment/testbed that motivated the controlled experiments.

## Research stance

Null and negative results are intentionally kept. The repository is meant to show what was tested, what worked, what failed, and where the current mechanism reaches its boundary.

The V7 series does **not** claim learned attention, learned memory relevance, or general episodic reasoning. The next research question is whether Cadence can learn which memories are important in a given context rather than relying on a fixed fading trace.
