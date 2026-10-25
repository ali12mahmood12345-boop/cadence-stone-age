# Stone Age V7 — Cadence 0.88 Memory / Attention Integration

Cadence: **0.88.0**

Status: **development complete — negative primary gate**

Official classification:

`NO_STONE_AGE_MEMORY_ATTENTION_ADVANTAGE`

## Question

Do Cadence 0.88 opt-in memory systems improve useful continuing Stone Age behavior, especially when inventory prerequisites are no longer directly visible?

## Environment

V7 used a headless matched-run port of the public Stone Age game:

- source: `stone_age_game/main.py`
- source blob: `dd59769349e7b6e9dea4ddcc321af8fa86b4e660`
- 18 original sensory dimensions
- 11 original high-level actions
- original resource counts, crafting prerequisites, survival rates, rewards, 150-second day and rabbit mechanics
- rendering removed only

Panels:

- `VISIBLE`: original observation
- `HIDDEN_INVENTORY`: wood, stone, food inventory and spear possession masked from Cadence while true body/world state remains intact

Arms:

- `DEFAULT`
- `EPISODIC`: `memory_choice=True`
- `H1`: learned-code attention, one Recall head
- `H2`: learned-code attention, two Recall heads
- `H2_EPISODIC`: H2 + episodic choice

Because Cadence 0.88 leaves reward-address learning off at `recall_address_reward=0`, the attention arms explicitly used the opt-in `recall_address_reward=0.1`.

Fresh founders: `60001..60006`.

Lifecycle: 6 sampled training episodes + 3 fresh greedy evaluation episodes per founder / panel / arm.

## Primary result

All **6/6 founders were valid**.

Median evaluation survival days:

| panel | DEFAULT | EPISODIC | H1 | H2 | H2+EPISODIC |
| --- | ---: | ---: | ---: | ---: | ---: |
| VISIBLE | 0.930 | 1.356 | 0.919 | 0.991 | 0.937 |
| HIDDEN_INVENTORY | 0.994 | 1.385 | 0.979 | 1.043 | 1.209 |

Hidden-inventory H2+episodic comparisons:

- beat DEFAULT: **2/6**
- beat EPISODIC: **2/6**
- beat H2: **4/6**
- median H2E−DEFAULT: **−0.034 days**
- median H2E−EPISODIC: **−0.101 days**
- median H2E−H2: **+0.129 days**

Night-survival medians in HIDDEN_INVENTORY:

- DEFAULT: **50%**
- EPISODIC: **100%**
- H2: **100%**
- H2+EPISODIC: **100%**

The strict V7 integration signal failed because H2+episodic did not beat DEFAULT or EPISODIC alone.

## Important acquisition-readiness finding

The deeper limitation is that V7 did not yet produce the intended Stone Age skill chain.

Across the median evaluation summaries, all arms had:

- fire rate: **0**
- spear rate: **0**
- shelter rate: **0**
- food-use rate: **0**

Some policies hunted rabbits, but they generally did not execute the downstream eat / craft / shelter behaviors needed for robust survival.

The default brain's visible→hidden survival penalty was also essentially zero:

`−0.0004 days`

That means masking current inventory did not create a strong memory dependency, because the policies were not yet relying on that inventory state to execute the prerequisite chains.

## Descriptive episodic result

EPISODIC alone was the strongest median arm in both panels:

- VISIBLE: **1.356 days**
- HIDDEN_INVENTORY: **1.385 days**
- hidden night survival: **100%**

However this was **not the frozen primary hypothesis**, was not consistent as a paired win on all founders, and should not be promoted to a confirmed episodic advantage from V7 alone.

## Interpretation

V7 gives a valid negative answer to its frozen primary question:

> At this operating point, H2+episodic did not provide a robust continuing-world advantage over the default or episodic-only brain.

But it also shows that the environment was not yet an adequate memory-integration test, because the underlying policies had not acquired the visible food/fire/shelter prerequisite chains.

The next Stone Age step should therefore be an **acquisition-readiness / curriculum control**, not parameter tuning of attention.

## Next direction

Before reopening hidden-state memory comparisons, require a visible-world Stone Age agent to demonstrate:

1. gather food → eat when hungry
2. gather wood + stone → craft fire when cold/evening
3. gather wood + stone → craft spear → hunt
4. gather enough materials → build shelter → sleep safely

Only after those chains are reliably acquired should inventory be hidden and memory mechanisms compared again.

No fresh V7 confirmation is warranted.
