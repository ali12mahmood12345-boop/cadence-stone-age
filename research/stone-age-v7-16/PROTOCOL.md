# Frozen Protocol — Stone Age V7.16

Status: DEVELOPMENT / frozen before run.

Cadence:
- cadence-net==0.89.0

Fresh founders:
- 83001..83008
- minimum valid 6/8

Question:
Can learned recall position distinguish FIRST vs LAST when the present query is identical and the answer depends only on temporal order?

Resource events:
- WOOD
- STONE
- BERRY
- RABBIT

Stream:
- 5 events
- first != last
- middle 3 random
- then FIRST or LAST query

Actions:
- WOOD -> GATHER_WOOD
- STONE -> GATHER_STONE
- BERRY -> PICK_BERRIES
- RABBIT -> HUNT_RABBIT

Arms:
1. POSITION32
   - recall=True
   - recall_position=32
   - recall_recency=0
   - recall_temperature=.25
2. POSITION0
   - identical but recall_position=0
3. RECALL_OFF
   - recall=False

Shared settings:
- inputs=6
- actions=4
- modules=(24,)
- episodic=False
- teaching="normalized"

Pairing:
- same founder seed
- same train episodes across arms
- same test episodes across arms

Episode:
- brain.reset()
- hear five resource events using greedy act
- on query: lesson first, then greedy act
- only query moment taught

Training:
- 1200 episodes/arm/founder

Testing:
- 240 fresh episodes/arm/founder
- no teaching
- record FIRST/LAST/overall/per-resource accuracy
- record POSITION32 position-map movement

Chance:
- .25

Gates:
- valid >=6/8
- POSITION32 median overall >=.90
- POSITION32 median FIRST >=.90
- POSITION32 median LAST >=.90
- >=6/8 founders FIRST>=.80 and LAST>=.80
- position maps moved >=6/8
- median POSITION32-POSITION0 >=.20
- >=6/8 founders POSITION32-POSITION0 >=.15
- median POSITION32-RECALL_OFF >=.40

Classification:
1. valid<6 -> INSUFFICIENT_V7_16_RUNS
2. maps fail -> POSITION_TERM_NOT_TAUGHT
3. all pass -> POSITIONAL_RECALL_TEMPORAL_HISTORY_BRIDGE_PASS
4. POSITION32 solves but no POSITION0 advantage -> TEMPORAL_TASK_SOLVED_WITHOUT_POSITION_ADVANTAGE
5. POSITION32 fails temporal gates -> POSITIONAL_RECALL_ACQUISITION_BOTTLENECK
6. otherwise -> PARTIAL_POSITIONAL_RECALL_SIGNAL

No attention.
No episodic memory.
No reward learning.
No full-game integration.
No post-hoc changes.
