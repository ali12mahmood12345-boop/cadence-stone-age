# Cadence Attention V0.5A

## Conjunctive Multi-Fact Memory

Cadence 0.88.0 adds supported multi-head learned-code attention:

```python
Brain.compose(
    ...,
    learned_code=16,
    attention=True,
    recall_heads=2,
)
```

The released held-heads benchmark shows that two heads can retrieve several facts in one settle. The release explicitly leaves open a harder case:

> a decision in which one fact matters only together with another.

V0.5A targets that boundary.

### Task

Four roles are witnessed. Roles 0 and 1 matter. Roles 2 and 3 are distractors.

Each role has one of six values: `0..5`.

The answer has three actions:

```text
action = (role0_value + role1_value) mod 3
```

### Why this is conjunctive

The 36 possible `(role0, role1)` pairs are split into:

- 18 taught pairs
- 18 held answer pairs

The split is constructed so that **within both panels**:

- each role-0 value appears equally often;
- each role-1 value appears equally often;
- for any fixed role-0 fact, actions 0/1/2 are exactly equally likely;
- for any fixed role-1 fact, actions 0/1/2 are exactly equally likely.

So either relevant fact alone gives exactly **33.3% chance**. Only their conjunction determines the answer.

Held combinations are never taught, although the constituent fact episodes are witnessed in Recall.

### Primary comparison

- `H2`: `attention=True, recall_heads=2`
- `H1`: matched `attention=True, recall_heads=1`

Both use the released held-head operating point:

- `learned_code=16`
- `modules=(64,)`
- `recall_address=0.01`
- `recall_temperature=0.25`
- normalized qualified teaching
- 1024 lessons

### Causal controls

The trained H2 brain is tested after:

- erasing the whole role-0 fact episode;
- erasing the whole role-1 fact episode;
- erasing both distractor episodes;
- erasing all Recall records;
- cloning head 0's learned address map into head 1, removing learned head-address specialization.

### Fresh development founders

`59001..59008`

Status: **development / currently running**.

A positive result must receive a larger fresh confirmation before a stronger claim.
