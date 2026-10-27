# Frozen Protocol — Stone Age V7.16R

Status: CONFIRMATION / frozen before run.

Cadence:
- cadence-net==0.89.0

Fresh founders:
- 84001..84016
- 16 total
- minimum paired-valid 12

Strict replication of V7.16.

Task:
- five resource events
- WOOD / STONE / BERRY / RABBIT
- first != last
- then FIRST or LAST query
- answer with corresponding Stone Age semantic action

Arms:
1. POSITION32
   - recall=True
   - recall_position=32
   - recall_recency=0
   - recall_temperature=.25
2. POSITION0
   - identical except recall_position=0
3. RECALL_OFF
   - recall=False
   - default working trace retained

Shared:
- inputs=6
- actions=4
- modules=(24,)
- episodic=False
- teaching="normalized"

Pairing:
- same founder seed
- same training episodes across arms
- same test episodes across arms

Episode:
- brain.reset()
- hear 5 resource events
- lesson(query,label)
- then act(query)
- only query taught

Training:
- 1200 episodes/arm/founder

Testing:
- 240 fresh paired episodes/arm/founder

Confirmation gates:
- valid >=12/16
- POSITION32 median overall >=.90
- POSITION32 median FIRST >=.90
- POSITION32 median LAST >=.90
- >=12 valid founders FIRST>=.80 and LAST>=.80
- position maps moved >=12 valid founders
- median POSITION32-POSITION0 >=.20
- >=12 valid founders gain >=.15 vs POSITION0
- median POSITION32-RECALL_OFF >=.40

Classification:
1. valid<12 -> INSUFFICIENT_V7_16R_RUNS
2. maps fail -> POSITION_TERM_NOT_CONFIRMED
3. all gates pass -> POSITIONAL_RECALL_TEMPORAL_HISTORY_CONFIRMED
4. POSITION32 solves without POSITION0 advantage -> TEMPORAL_TASK_REPLICATED_WITHOUT_POSITION_ADVANTAGE
5. POSITION32 temporal gates fail -> POSITIONAL_RECALL_TEMPORAL_HISTORY_NOT_CONFIRMED
6. otherwise -> PARTIAL_POSITIONAL_RECALL_REPLICATION_SIGNAL

No attention.
No episodic memory.
No reward learning.
No full-game integration.
No post-hoc changes.
