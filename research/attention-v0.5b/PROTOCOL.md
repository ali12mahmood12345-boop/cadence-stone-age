# Protocol (proposed) — Cadence Attention V0.5B

Status: PROPOSED. Same question, arms, settings, controls and gates as
[V0.5A](../attention-v0.5a/PROTOCOL.md); only the world's value count, the taught/held
split and one admission gate change.

## Why a new split

A held pair tests generalization only if the taught pairs determine its answer. Under V0.5A's
split they do not. `split_check.py` enumerates every explanation of the form "each value
carries a hidden residue and the action is a fixed map of the residue sum". 18 of them fit
all taught pairs, and they agree on **0 of the 18** held pairs. One is right on every taught
pair and wrong on every held pair. The taught low×high table pins each half's residues only up
to opposite shifts, so no low+low or high+high sum is fixed. Chance on held pairs is
therefore expected from every learner, and V0.5A's held result cannot separate Cadence from
anything else. Its retrieval result stands: the two heads chose the two relevant facts on
100% of held trials.

## World

- 4 witnessed roles, roles 0 and 1 relevant, roles 2 and 3 distractors
- **9 values per role** (inputs=16: 4 roles + 9 values + neutral + ASK)
- 3 actions, `action = (role0 + role1) % 3`

## Taught / held split

Held: `(role1 - role0) mod 9` is 0, 1 or 5 (27 pairs). Taught: the other 54 pairs.
With the two distractors, 4,374 taught and 2,187 held patterns.

Properties, checked by `split_check.py`:
- either relevant fact alone predicts each action equally often, in BOTH panels (single-fact
  chance 1/3);
- all 27 held answers are determined by the taught pairs under the residue hypothesis, and
  equal the rule's (6 consistent explanations, all relabelings of one solution);
- a memorizer of taught pairs is at chance on held pairs.

Passing therefore requires discovering that the nine symbols form three classes from how they
combine, then combining two retrieved facts by class: conjunctive generalization, not
lookup.

## Admission gate (new)

Before any founder runs: `split_check.report(...)["tests_conjunctive_generalization"]` is
true for the declared split. A split that fails it is not run.

## Unchanged

Arms (H2 `recall_heads=2`, H1 `recall_heads=1`), all compose settings, warm-up, Recall-written
banks, 1024 lessons of 16 taught trials with calm teaching, causal controls (role0, role1,
distractor and all-record erasure, cloned head address) and every frozen gate of V0.5A.
Fresh founders are declared before running.

## Suggested beside the gates

A positive control in the same runner, so a pass is detectable: Cadence 0.88's held-heads
benchmark one-action rule (go to the food unless the predator stands at an odd position, then
five steps from it) reached 96-98% on untaught pairs with two heads, against 59-76% for one
head. If that control passes and V0.5B fails, the gap is conjunctive composition in the shared
readout.
