"""Can a taught/held split test conjunctive generalization at all?

A held pair tests generalization only if the taught pairs determine its answer under a
declared hypothesis class; otherwise every learner, Cadence or not, belongs at chance. For
``answer = (role0 + role1) % m`` over symbolic values the class is "each value carries a
hidden residue, and the answer is a fixed map of the residue sum". ``identifiable`` enumerates
every member that fits all taught pairs and counts the held pairs on which they all agree.

Also checked: single-fact balance (either fact alone predicts every answer equally often in a
panel) and a memorizer reference, which has never seen a held pair.

    python split_check.py        # V0.5A's split and the proposed V0.5B split
"""

from __future__ import annotations

import itertools
from collections import Counter

import numpy as np


def answer(a: int, b: int, m: int = 3) -> int:
    return (a + b) % m


def split_v05a() -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    """V0.5A: six values; taught pairs mix a value of 0..2 with one of 3..5, held pairs don't."""
    pairs = [(a, b) for a in range(6) for b in range(6)]
    held = [(a, b) for a, b in pairs if (a < 3) == (b < 3)]
    return [p for p in pairs if p not in held], held


def split_v05b(values: int = 9, held_offsets: tuple[int, ...] = (0, 1, 5)):
    """V0.5B: nine values; held iff (role1 - role0) mod 9 is 0, 1 or 5 (27 held, 54 taught).
    Every row and column of the 9x9 table loses one cell of each residue class, which keeps
    single facts at chance in both panels."""
    pairs = [(a, b) for a in range(values) for b in range(values)]
    held = [(a, b) for a, b in pairs if (b - a) % values in held_offsets]
    return [p for p in pairs if p not in held], held


def single_fact_balanced(panel: list[tuple[int, int]], m: int = 3) -> bool:
    """Either fact alone predicts each answer equally often within the panel."""
    for role in (0, 1):
        for value in {p[role] for p in panel}:
            counts = Counter(answer(*p, m) for p in panel if p[role] == value)
            if len(counts) != m or len(set(counts.values())) != 1:
                return False
    return True


def identifiable(taught, held, values: int, m: int = 3) -> dict:
    """Members of the residue class consistent with every taught pair, and the held pairs whose
    answer they all agree on (and whether that agreed answer is the rule's)."""
    codes = np.array(list(itertools.product(range(m), repeat=values)))
    maps = np.array(list(itertools.product(range(m), repeat=m)))
    ta, tb = (np.array([p[i] for p in taught]) for i in (0, 1))
    target = (ta + tb) % m
    sums = (codes[:, ta] + codes[:, tb]) % m
    fits = np.stack([(g[sums] == target).all(axis=1) for g in maps], axis=1)
    code_index, map_index = np.nonzero(fits)
    ha, hb = (np.array([p[i] for p in held]) for i in (0, 1))
    predicted = maps[map_index][np.arange(len(map_index))[:, None],
                                (codes[code_index][:, ha] + codes[code_index][:, hb]) % m]
    fixed = (predicted == predicted[:1]).all(axis=0)
    return {"consistent_explanations": int(len(code_index)),
            "held_pairs": len(held), "held_pairs_determined": int(fixed.sum()),
            "determined_answers_match_rule": bool((predicted[0][fixed] == ((ha + hb) % m)[fixed]).all()),
            "worst_consistent_held_accuracy": float((predicted == (ha + hb) % m).mean(axis=1).min())}


def report(name: str, taught, held, values: int) -> dict:
    out = {"split": name, "values": values, "taught_pairs": len(taught), "held_pairs": len(held),
           "single_fact_chance_taught": single_fact_balanced(taught),
           "single_fact_chance_held": single_fact_balanced(held),
           "memorizer_held_accuracy": 1 / 3,  # no held pair was ever taught
           **identifiable(taught, held, values)}
    out["tests_conjunctive_generalization"] = (
        out["held_pairs_determined"] == out["held_pairs"] and out["determined_answers_match_rule"]
        and out["single_fact_chance_taught"])
    return out


if __name__ == "__main__":
    import json

    print(json.dumps(report("V0.5A", *split_v05a(), 6), indent=2))
    print(json.dumps(report("V0.5B", *split_v05b(), 9), indent=2))
