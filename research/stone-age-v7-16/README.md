# Stone Age V7.16 — Positional Recall Temporal-History Bridge

Status: **development complete**

Cadence: **0.89.0**

Official frozen classification:

`POSITIONAL_RECALL_TEMPORAL_HISTORY_BRIDGE_PASS`

## Purpose

V7.16 tested Cadence 0.89.0's learned recall-position term on a deliberately temporal Stone Age component task.

Each episode contained five resource events:
- WOOD
- STONE
- BERRY
- RABBIT

The first and last resources were always different.

The brain then received an identical `FIRST` or `LAST` query and had to return the semantic action corresponding to that endpoint resource.

The query itself contained no resource identity.

## Fresh founders

`83001..83008`

Valid paired founders:
- **7/8**
- frozen minimum: 6/8

Founder 83007 was excluded from the paired-valid set only because RECALL_OFF emitted a finite free-phase settling warning at training lesson 1010, which the runner treated as an error.

Importantly, founder 83007's POSITION32 arm itself completed training and scored:
- overall: 100%
- FIRST: 100%
- LAST: 100%
- position maps moved: yes

## Result

### POSITION32

Median held-out accuracy across valid founders:
- overall: **100%**
- FIRST: **100%**
- LAST: **100%**

Founder robustness:
- both cues >=80%: **7/7 valid founders**
- position maps moved: **7/7 valid founders**

Diagnostic including the otherwise-invalid founder 83007:
- all 8 POSITION32 arms individually reached 100% overall/FIRST/LAST

### POSITION0

Median held-out:
- overall: **47.9%**
- FIRST: **29.1%**
- LAST: **69.7%**

### RECALL_OFF

Median held-out:
- overall: **55.0%**
- FIRST: **23.6%**
- LAST: **83.2%**

## Paired positional advantage

POSITION32 vs POSITION0:
- median gain: **+52.1 percentage points**
- founders with >=15-point gain: **7/7 valid**

POSITION32 vs RECALL_OFF:
- median gain: **+45.0 percentage points**

All frozen gates passed.

## Important baseline interpretation correction

The frozen protocol described RECALL_OFF as a "current-query-only" baseline.

That wording is too strong.

`recall=False` removes Recall, but Cadence's default working trace remains active unless explicitly silenced. Therefore RECALL_OFF is correctly interpreted as:

> **no-Recall baseline with the default working trace still present**

This explains the strong LAST bias:
- RECALL_OFF median LAST: 83.2%
- RECALL_OFF median FIRST: 23.6%

The default working trace can carry recent information, so the no-Recall arm is not a pure present-only system.

This does **not** undermine the main positional-recall result.

The causal comparison is POSITION32 vs POSITION0:
- same Recall mechanism
- same seed
- same training episodes
- same held-out episodes
- same working trace/default brain machinery
- same recency setting
- only `recall_position` differs: 32 vs 0

That paired comparison shows a +52.1-point median advantage and 7/7 valid founder wins by at least 15 points.

## Scientific interpretation

The result supports the bounded claim:

> Cadence 0.89.0's learned recall-position term can teach a cue to retrieve a past Stone Age resource event by temporal position, distinguishing FIRST from LAST when resource content alone does not identify the requested endpoint.

The asymmetry in the controls is itself informative:
- without learned position, LAST remains much easier than FIRST
- with POSITION32, both cues reach 100%

This is consistent with recent-state information remaining available through non-positional stream dynamics, while the learned slot-age term supplies the missing ability to deliberately address older versus newer events.

## Boundaries

This is a bounded component result.

It does not yet establish:
- arbitrary temporal reasoning
- long-horizon recall
- full Stone Age survival with Recall
- attention-head benefits
- episodic-memory benefits
- reward-trained positional recall

No post-hoc gates or recipe changes were made.

## Next direction

**Stone Age V7.16R — Fresh Positional Recall Temporal-History Confirmation**

Strict replication of V7.16 on a larger untouched founder panel.

Recommended founders:
- `84001..84016`

Keep unchanged:
- Cadence 0.89.0
- POSITION32 / POSITION0 / RECALL_OFF
- five-event streams
- FIRST/LAST endpoints forced different
- 1200 training episodes
- 240 held-out episodes
- lesson-before-query-act
- recall_recency=0
- same modules and teaching
- same frozen gates

For documentation, call RECALL_OFF a **no-Recall baseline with default working trace retained**. Do not change the actual arm.

Recommended confirmation:
- >=12/16 valid paired founders
- POSITION32 median overall/FIRST/LAST >=90%
- >=12 valid founders both cues >=80%
- position maps moved in >=12 valid founders
- median POSITION32-POSITION0 >=20 points
- >=12 valid founders gain >=15 points vs POSITION0
- median POSITION32-RECALL_OFF >=40 points

If these pass, classify:

`POSITIONAL_RECALL_TEMPORAL_HISTORY_CONFIRMED`

Do not integrate Recall into full autonomous Stone Age survival until the fresh confirmation is complete.
