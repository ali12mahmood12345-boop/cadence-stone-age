# Stone Age V7.16R — Fresh Positional Recall Temporal-History Confirmation

Status: **confirmation protocol / frozen before run**

Cadence: **0.89.0**

V7.16 produced a strong development result showing that the learned recall-position term can distinguish FIRST from LAST in a bounded Stone Age temporal-history task.

V7.16R is a strict fresh confirmation of that exact recipe.

## Question

Does the V7.16 positional-recall temporal-history result reproduce on a larger untouched founder panel with no recipe changes?

## Fresh founders

`84001..84016`

- 16 founders total
- minimum paired-valid: 12/16

## Task

Identical to V7.16.

Each episode contains five resource-event moments drawn from:

- WOOD
- STONE
- BERRY
- RABBIT

The first and last resource are always different.

After the five events, the brain receives one query:

- FIRST
- LAST

The query observation contains no resource identity.

Correct answer:

- WOOD -> `GATHER_WOOD`
- STONE -> `GATHER_STONE`
- BERRY -> `PICK_BERRIES`
- RABBIT -> `HUNT_RABBIT`

The answer therefore depends on temporal endpoint information rather than current resource content.

## Arms

### POSITION32

Unchanged from V7.16:

- `recall=True`
- `recall_position=32`
- `recall_recency=0.0`
- `recall_temperature=0.25`

### POSITION0

Identical except:

- `recall_position=0`

### RECALL_OFF

Identical architecture/seed/teaching except:

- `recall=False`

Interpretation:

RECALL_OFF is a **no-Recall baseline with Cadence's default working trace retained**.

No implementation change is made relative to V7.16.

## Shared architecture

- inputs=6
- actions=4
- modules=(24,)
- episodic=False
- teaching="normalized"

## Pairing

Per founder:

- all arms use the same founder seed
- all arms receive exactly the same training episodes
- all arms receive exactly the same held-out test episodes

## Episode boundary

Every episode:

1. `brain.reset()`
2. five resource events via greedy `brain.act()`
3. query moment:
   - `brain.lesson(query, correct_action)`
   - then `brain.act(query, greedy=True)`

Lesson-before-query-act is retained exactly.

## Training

Per founder / arm:

- 1200 training episodes
- only the query moment is taught
- FIRST/LAST sampled approximately 50/50
- first endpoint != last endpoint
- three middle events random

## Held-out evaluation

Per founder / arm:

- 240 fresh paired test episodes
- no teaching during test

Metrics:

- overall accuracy
- FIRST accuracy
- LAST accuracy
- per-resource accuracy
- confusion counts
- POSITION32 position maps moved
- POSITION32 - POSITION0 paired gain
- POSITION32 - RECALL_OFF paired gain

Chance baseline:

- 25%

## Frozen confirmation gates

Run validity:

- >=12/16 paired-valid founders

POSITION32 median performance:

- overall >=90%
- FIRST >=90%
- LAST >=90%

Founder robustness:

- >=12 valid founders have FIRST >=80% and LAST >=80%

Position-learning evidence:

- position maps moved in >=12 valid founders

Paired POSITION32 advantage:

- median POSITION32 - POSITION0 overall >=20 percentage points
- >=12 valid founders POSITION32 beats POSITION0 overall by >=15 points
- median POSITION32 - RECALL_OFF overall >=40 percentage points

## Frozen classification

1. valid founders <12 -> `INSUFFICIENT_V7_16R_RUNS`
2. position maps fail -> `POSITION_TERM_NOT_CONFIRMED`
3. all confirmation gates pass -> `POSITIONAL_RECALL_TEMPORAL_HISTORY_CONFIRMED`
4. POSITION32 solves but lacks POSITION0 advantage -> `TEMPORAL_TASK_REPLICATED_WITHOUT_POSITION_ADVANTAGE`
5. POSITION32 fails temporal performance gates -> `POSITIONAL_RECALL_TEMPORAL_HISTORY_NOT_CONFIRMED`
6. otherwise -> `PARTIAL_POSITIONAL_RECALL_REPLICATION_SIGNAL`

## Boundaries

Strict replication only.

No changes to:

- architecture
- recall settings
- working trace
- training dose
- test dose
- episode generator
- endpoint constraint
- lesson boundary
- gates

No attention.
No episodic memory.
No reward learning.
No full Stone Age integration.
No post-hoc changes.
