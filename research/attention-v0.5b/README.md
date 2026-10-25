# Cadence Attention V0.5B (proposed)

V0.5A asked whether two held Recall heads can combine two witnessed facts when neither alone
predicts the answer. Its heads found both facts on 100% of held trials, but its held split could
not test the combination: the taught pairs determine none of the held answers (`split_check.py`),
so every learner belongs at chance there.

V0.5B keeps the rule, arms, controls and gates and changes the world to nine values with a held
set every row and column of which loses one cell per residue class. Single facts stay at chance in
both panels, every held answer is determined by the taught pairs, and a memorizer stays at chance.
See [PROTOCOL.md](PROTOCOL.md).

```sh
python split_check.py   # V0.5A: 0/18 held pairs determined; V0.5B: 27/27
```
