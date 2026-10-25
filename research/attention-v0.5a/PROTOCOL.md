# Frozen Protocol — Cadence Attention V0.5A

Status: DEVELOPMENT.

Runtime:
- cadence-net==0.88.0
- numpy>=2,<3

Fresh founders:
- 59001..59008
- minimum valid: 6/8

## World

- 4 witnessed roles
- 6 values per role
- roles 0 and 1 relevant
- roles 2 and 3 distractors
- 3 actions
- answer = `(role0 + role1) % 3`

## Taught / held split

Held:
- role0 and role1 are both in `0..2`, OR
- role0 and role1 are both in `3..5`

Taught:
- complement: one value is in `0..2`, the other in `3..5`

There are 18 pair combinations in each panel.

Including the two distractor values:
- 648 exhaustive taught patterns
- 648 exhaustive held patterns

Balance property:
within EACH panel, conditioning on role0 alone or role1 alone leaves actions 0/1/2 exactly uniform. Single-fact chance is therefore 1/3.

## H2 / H1

Both:
- inputs=12
- actions=3
- learned_code=16
- modules=(64,)
- attention=True
- recall_address=0.01
- recall_temperature=0.25
- episodic=False
- teaching="normalized"
- learning_qualified=True
- learning_damping=3
- learning_free_steps=1024
- learning_nudged_steps=1024
- learning_tolerance=0.003

H2: recall_heads=2
H1: recall_heads=1

Warm:
- every role token, value token, neutral and ASK token
- 16 rounds
- freeze learned_code afterward

Banks:
- written by Cadence Recall itself
- 4 episodes per pattern
- each episode `[neutral, role, value]`
- 12 slots per pattern

Teaching:
- 1024 lessons
- batch 16
- taught pairs only
- same calm-teaching policy as Cadence 0.88 held_heads.py
- H2 and H1 receive matched founder/task schedules

## Causal controls on held panel

1. Erase role0's complete three-slot fact episode.
2. Erase role1's complete three-slot fact episode.
3. Erase roles2+3 distractor episodes.
4. Erase every Recall held slot (memory off).
5. Clone head0's learned address map into head1.

## Frozen gates

`CONJUNCTIVE_MULTI_FACT_ATTENTION_SIGNAL` requires all:

- >=6 valid founders
- H2 median taught accuracy >=95%
- H2 median held accuracy >=90%
- H2 > H1 on held in >=2/3 valid founders
- median H2-H1 held gain >=+0.20
- median H2 distinct-top heads >=90%
- role0-erased median accuracy <=55%
- median role0 erasure loss >=+0.30
- role1-erased median accuracy <=55%
- median role1 erasure loss >=+0.30
- distractor-erased median accuracy >=85%
- median distractor-erasure loss <=+0.10
- memory-off median accuracy <=50%
- median memory-off loss >=+0.35
- H2 > clone-head lesion in >=2/3 valid founders
- median H2-clone gain >=+0.10

A positive result is development evidence only and requires fresh confirmation.

## Boundaries

This is not:
- a reward-only attention result,
- a continuing-world result,
- a Stone Age result,
- a default-brain change,
- evidence that two heads are always better.

It is specifically a test of conjunctive use of two witnessed facts in one settle.
