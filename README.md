# Cadence Stone Age Research Environment

A small Stone Age survival environment and a set of Cadence benchmarks used to study:

- survival learning versus Random
- prerequisite chains
- delayed credit
- state-dependent action selection
- backward lessons
- training-budget / over-drilling effects
- interference and retention across learned prerequisite mappings

The project grew out of a visual Stone Age survival game, then was reduced into controlled chambers so the learning behavior could be measured.

## Main survival environment

The original visual environment is in:

`stone_age_game/main.py`

It contains:

- trees
- rocks
- berries
- rabbits
- hunger
- warmth
- energy
- fire
- spear crafting
- shelter
- sleep
- day/night cycle

The original game used an earlier Cadence package version and is kept here primarily as the environment/testbed that motivated the controlled experiments.

## Cadence 0.81 sequence experiments

The current controlled experiments are in:

`benchmarks/cadence_081/`

### V4.2 — lesson budget sweep

Tests fixed balanced backward-lesson budgets from the same founder.

Question:
Does more drilling help all prerequisite mappings, or does it eventually damage some of them?

### V4.3 — competency-based backward lessons

Stops direct training once a lesson reaches a target validation accuracy and only rehearses older skills if measured retention falls.

On seed 42 this produced the first positive frozen full-chain result:

- trained sampled: 11%
- founder sampled: 5%
- uniform Random: 2%

### V4.4 — retention rescue

Repeatedly rescues the weakest learned mapping and then runs final consolidation.

This did **not** improve the chain. The consolidation budget was exhausted and strong destructive interference remained between prerequisite mappings.

## COLD prerequisite chain

The controlled chain is:

`GATHER_WOOD -> GATHER_STONE -> CRAFT_FIRE -> WARM_UP`

Cadence observes the prerequisite state, including wood, stone, fire and warmth.

The target action is never included in the observation.

Cadence chooses an action itself and the executed action is graded by reward.

Cadence 0.81 `Brain.wait` is used in the delayed-observation experiments.

## Key observed results

See [`docs/RESULTS.md`](docs/RESULTS.md).

## Run the 0.81 benchmarks

Create an environment inside `benchmarks/cadence_081` and install:

```bash
pip install -r requirements.txt
```

Then, for example:

```bash
python v4_3_competency.py --target 0.70 --maintenance 0.55 --block 4 --rescue 2 --validation 80 --max-direct 60 --eval 100 --seeds 1 --name quick
```

or:

```bash
python v4_4_retention_rescue.py --target 0.70 --maintenance 0.55 --block 4 --rescue 2 --validation 80 --max-direct 60 --stabilize-budget 24 --final-budget 80 --eval 100 --seeds 1 --name quick
```

## Notes

These are research experiments, not claims that Cadence generally outperforms Random. Several versions intentionally produced null or negative results, and those failures are included because they helped isolate the sequence / interference problem.

The most interesting finding so far is that one-step prerequisite mappings can be acquired, but keeping several of them simultaneously stable in one settled brain remains difficult in this Stone Age chain.
