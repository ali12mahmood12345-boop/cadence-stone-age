# Cadence Stone Age V7

## 0.88 Memory / Attention Integration

Status: **development / running**

Cadence: **0.88.0**

V7 returns the research line to the public Stone Age environment after the V0.5A conjunctive chamber produced a clean negative result.

### Question

Do Cadence 0.88 memory systems improve useful behavior in a continuing survival world, especially when current observations stop exposing inventory prerequisites directly?

### Source environment

Headless matched-run port of:

`stone_age_game/main.py`

Source blob:

`dd59769349e7b6e9dea4ddcc321af8fa86b4e660`

The port retains the game's 18 inputs, 11 actions, survival rates, resource/crafting requirements, reward constants, 150-second day, rabbit mechanics and 0.55-second decision interval. Pygame rendering is removed so matched experimental arms can run quickly.

### Panels

**VISIBLE**
- original observation

**HIDDEN_INVENTORY**
- true body/world unchanged
- Cadence receives zero for wood, stone, carried food and spear possession

### Arms

- DEFAULT
- EPISODIC — `memory_choice=True`
- H1 — learned-code attention, 1 Recall head
- H2 — learned-code attention, 2 Recall heads
- H2_EPISODIC — H2 + episodic choice

Attention arms use:

```python
learned_code=16
attention=True
recall_address_reward=0.1
```

### Important 0.88 boundary

The Cadence 0.88 founder uses `recall_address_reward=0`, so reward-only experience does not train Recall address maps.

V7 explicitly opts into `0.1`, the value shown in the 0.88 memory-guide example. This is an experimental operating point, not a default-brain claim.

### Lifecycle

Fresh founders: `60001..60006`

Per founder / arm / panel:
- 6 sampled training episodes with `brain.step`
- persistent learned brain and memory across episodes
- 3 fresh greedy evaluation episodes with `brain.act`
- learned code frozen during evaluation
- max 2.0 Stone Age days per episode

### Primary development signal

H2_EPISODIC in HIDDEN_INVENTORY must beat:
- DEFAULT
- EPISODIC alone
- H2 alone

with paired founder wins and precommitted survival-day gains, while reaching at least 50% night survival and avoiding a large visible-panel regression.

No result is claimed until the run completes.
