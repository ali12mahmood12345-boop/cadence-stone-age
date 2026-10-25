# Cadence Attention V0.5A

## Conjunctive Multi-Fact Memory

Cadence: **0.88.0**

Status: **development complete — negative**

Official classification:

`NO_CONJUNCTIVE_MULTI_FACT_SIGNAL`

## Question

Can two supported held Recall heads combine two independently witnessed facts when neither fact alone predicts the answer?

## Task

Four roles are witnessed. Roles 0 and 1 matter; roles 2 and 3 are distractors.

Each relevant role has one of six values.

```text
action = (role0_value + role1_value) mod 3
```

The 36 possible role0/role1 pairs were split into 18 taught and 18 held pairs. The split was balanced so that, within both panels, either relevant fact alone predicts each action equally often. Single-fact accuracy is therefore exactly **33.3% chance**.

## Arms

- H2: `attention=True, recall_heads=2`
- H1: matched `attention=True, recall_heads=1`

Both used:

- `learned_code=16`
- `modules=(64,)`
- `recall_address=0.01`
- `recall_temperature=0.25`
- normalized qualified teaching
- 1024 lessons

Fresh development founders: `59001..59008`.

## Result

All 8/8 founders were valid.

Median accuracy:

- H2 taught: **100.0%**
- H2 held: **31.6%**
- H1 taught: **72.8%**
- H1 held: **33.8%**
- chance: **33.3%**

H2 beat H1 on held combinations in only **3/8** founders; median H2-H1 held difference was **-0.023**.

## Important diagnostic

The two heads did learn distinct, apparently correct record addresses:

- median H2 held distinct-top heads: **100%**
- median H2 top roles exactly `{0,1}`: **100%**

So the failure is not simply that both heads selected the same or wrong role. The brain often retrieved the two requested facts but did not generalize the conjunction into the correct unseen action combination.

## Causal controls

Held-panel medians:

- intact H2: **31.6%**
- erase role0: **33.3%**
- erase role1: **33.3%**
- erase distractors role2/3: **30.6%**
- erase all Recall records: **33.3%**
- clone head1 address map from head0: **32.9%**

Because intact held performance itself was at chance, the erasure controls cannot establish useful conjunctive memory use.

## Frozen gates

Only these structural gates passed:

- enough valid founders
- H2 taught median >=95%
- distinct heads >=90%
- relevant-erasure absolute accuracy <=55%
- memory-off absolute accuracy <=50%
- H2 > clone fraction

The held accuracy, H2-vs-H1 advantage, causal-loss and clone-gain gates failed.

## Interpretation

Cadence 0.88.0 can learn two distinct relevant Recall addresses in this chamber, and H2 can perfectly fit many taught conjunctions. But the supported two-head reader did **not** learn a compositional rule that generalized to held role-value combinations.

This is a useful boundary result: **retrieving two relevant facts is not sufficient, by itself, for systematic conjunctive generalization in the shared downstream association/action network.**

## Boundary

This does not show that multi-head attention is useless in continuing environments or Stone Age. It only closes this specific bounded symbolic conjunction assay at the tested operating point.

No fresh confirmation is warranted because the frozen development signal failed.
