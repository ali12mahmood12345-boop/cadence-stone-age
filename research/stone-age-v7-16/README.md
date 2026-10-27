# Stone Age V7.16 — Positional Recall Temporal-History Bridge

Status: **development protocol / frozen before run**

Cadence: **0.89.0**

V7.15R freshly confirmed autonomous semantic goal routing when the correct decision is inferable from the current global semantic observation.

V7.16 deliberately removes that possibility.

## Question

Can Cadence 0.89.0's learned recall-position term solve a Stone Age temporal-order task in which the **current query observation is identical** and the correct action depends only on whether a past event happened first or last?

## Fresh founders

`83001..83008`

- 8 founders total
- minimum valid: 6/8

## Stone Age temporal stream

Each episode contains five resource-event moments.

Resource symbols:
- `WOOD`
- `STONE`
- `BERRY`
- `RABBIT`

The first and last resource are always different.
The three middle events are sampled independently.

After the five resource moments, the brain receives one query:
- `FIRST`
- `LAST`

The query observation itself contains **no resource identity**.

Correct answer:
- if the queried event was WOOD -> `GATHER_WOOD`
- STONE -> `GATHER_STONE`
- BERRY -> `PICK_BERRIES`
- RABBIT -> `HUNT_RABBIT`

Thus:
- the visible query state is identical across answers
- both endpoint resources are present in the same episode
- current-state-only inference cannot solve the task
- content alone cannot identify whether the requested slot is first or last

## Inputs / actions

Inputs: 6 one-hot symbols:
- 0 WOOD
- 1 STONE
- 2 BERRY
- 3 RABBIT
- 4 FIRST
- 5 LAST

Actions: 4 semantic Stone Age responses:
- GATHER_WOOD
- GATHER_STONE
- PICK_BERRIES
- HUNT_RABBIT

This is a bounded temporal-memory component test, not a full-game survival evaluation.

## Arms

### POSITION32

```python
Brain.compose(
    inputs=6,
    actions=4,
    modules=(24,),
    episodic=False,
    recall=True,
    recall_position=32,
    recall_recency=0.0,
    recall_temperature=0.25,
    teaching="normalized",
)
```

This is the Cadence 0.89.0 founder positional-recall term.

### POSITION0

Identical recipe except:

`recall_position=0`

This keeps Recall but removes learned positional slot-age terms.

### RECALL_OFF

Identical inputs/actions/modules/seed and teaching, but:
- `recall=False`

This is the current-query-only baseline.

## Pairing

For each founder:
- all arms use the same seed
- all arms receive exactly the same training episodes
- all arms receive exactly the same held-out test episodes

No founder/arm sees another arm's test labels during training.

## Episode boundary

Every episode starts with:

`brain.reset()`

The five resource events are then presented with greedy `brain.act()`.

At the query:
1. call `brain.lesson(query, correct_action)`
2. then call `brain.act(query, greedy=True)`

Teaching therefore occurs **before** the query act writes that same moment into Recall, matching the released 0.89.0 look-back benchmark and avoiding act-then-lesson self-read contamination.

## Training

Per founder / arm:
- 1200 training episodes
- FIRST/LAST sampled approximately 50/50
- endpoint symbols sampled uniformly with first != last
- middle three resource events sampled uniformly
- only the query moment is taught

No reward learning.
No episodic memory.
No attention/multi-head option.
No recency bias.

## Held-out evaluation

Per founder / arm:
- 240 fresh episodes
- same paired test episodes across arms
- no teaching during test
- 120-ish FIRST and 120-ish LAST queries by RNG

Metrics:
- FIRST accuracy
- LAST accuracy
- overall accuracy
- per-resource accuracy
- confusion counts
- POSITION32 position maps moved
- pairwise POSITION32 minus POSITION0
- pairwise POSITION32 minus RECALL_OFF

Chance baseline:
- 25%

## Frozen gates

Run validity:
- >=6/8 valid founders

POSITION32 median performance:
- overall >=90%
- FIRST >=90%
- LAST >=90%

Founder robustness:
- >=6/8 valid founders have FIRST >=80% and LAST >=80%

Position-learning evidence:
- position maps moved in >=6/8 valid founders

Paired advantage:
- median POSITION32 - POSITION0 overall >=20 percentage points
- >=6/8 founders POSITION32 beats POSITION0 overall by >=15 points
- median POSITION32 - RECALL_OFF overall >=40 percentage points

## Frozen classification

1. valid founders <6 -> `INSUFFICIENT_V7_16_RUNS`
2. position maps fail to move -> `POSITION_TERM_NOT_TAUGHT`
3. POSITION32 passes performance and paired-advantage gates -> `POSITIONAL_RECALL_TEMPORAL_HISTORY_BRIDGE_PASS`
4. POSITION32 solves the task but lacks POSITION0 advantage -> `TEMPORAL_TASK_SOLVED_WITHOUT_POSITION_ADVANTAGE`
5. POSITION32 fails temporal performance gates -> `POSITIONAL_RECALL_ACQUISITION_BOTTLENECK`
6. otherwise -> `PARTIAL_POSITIONAL_RECALL_SIGNAL`

## Boundaries

This experiment tests only:
- learned slot-age positional recall
- FIRST versus LAST retrieval
- a bounded five-event stream
- four Stone Age resource event meanings

It does **not** yet test:
- full Stone Age autonomous survival with Recall enabled
- long-horizon memory
- arbitrary natural-language order questions
- attention heads
- episodic memory
- reward-only learning

No post-hoc changes.
