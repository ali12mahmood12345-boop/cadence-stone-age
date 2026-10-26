"""A self-contained V0.5B runner on cadence-net 0.88.0 (see PROTOCOL.md).

Per founder and arm (H2 ``recall_heads=2``, H1 ``recall_heads=1``): warm the learned code,
write every pattern's bank with Recall itself (four ``neutral, role, value`` episodes), teach
1024 lessons of 16 taught patterns with calm teaching (every row while the running share of
wrong answers is at least 0.02, the wrong rows below it), then read taught and held accuracy,
the heads' distinct top role records, and the held panel under each causal control.

    python run_v05b.py --seeds 59101 --out v05b_59101.json
"""

from __future__ import annotations

import argparse
import itertools
import json
import time
from copy import deepcopy

import numpy as np

import cadence as cd

from split_check import report, split_v05b

INPUTS, ROLES, VALUES, ACTIONS = 16, 4, 9, 3
ROLE, VALUE = 0, 4
NEUTRAL, ASK = VALUE + VALUES, VALUE + VALUES + 1
TAUGHT, HELD = (set(s) for s in split_v05b())
RECORD = {j: [3 * j, 3 * j + 1, 3 * j + 2] for j in range(ROLES)}  # each role's episode slots


def event(index: int, n: int = 1) -> np.ndarray:
    x = np.zeros((n, INPUTS))
    x[:, index] = 1.0
    return x


def labels(patterns) -> np.ndarray:
    return np.array([(p[0] + p[1]) % ACTIONS for p in patterns], dtype=np.int64)


def compose(seed: int, heads: int) -> cd.Brain:
    return cd.Brain.compose(
        INPUTS, ACTIONS, modules=(64,), learned_code=16, attention=True, recall_heads=heads,
        recall_address=0.01, recall_temperature=0.25, episodic=False, teaching="normalized",
        learning_qualified=True, learning_damping=3, learning_free_steps=1024,
        learning_nudged_steps=1024, learning_tolerance=0.003, seed=seed,
    )


def warm(brain: cd.Brain, rounds: int = 16) -> None:
    for _ in range(rounds):
        for index in [*range(ROLES), *(VALUE + v for v in range(VALUES)), NEUTRAL, ASK]:
            brain.reset(keep=())
            brain.act(event(index), greedy=True)
    brain.learned_code.learning = False
    brain.reset(keep=())


def banks(brain: cd.Brain) -> dict:
    patterns = list(itertools.product(range(VALUES), repeat=ROLES))
    n, recall = len(patterns), brain.recall
    brain.reset(keep=())
    for j in range(ROLES):
        if j:
            brain.reset(keep=("slots",))
        brain.act(event(NEUTRAL, n), greedy=True)
        brain.act(event(ROLE + j, n), greedy=True)
        values = np.zeros((n, INPUTS))
        values[np.arange(n), VALUE + np.array([p[j] for p in patterns])] = 1.0
        brain.act(values, greedy=True)
    names = ("keys", "values", "nexts", "held")
    out = {p: {k: getattr(recall, k)[i:i + 1].copy() for k in names} for i, p in enumerate(patterns)}
    brain.reset(keep=())
    return out


def install(brain: cd.Brain, bank: dict, patterns, erase=()) -> None:
    recall = brain.recall
    brain.reset(keep=())
    for name in ("keys", "values", "nexts", "held"):
        setattr(recall, name, np.concatenate([bank[p][name] for p in patterns]).copy())
    if erase:
        held = recall.held.copy()
        held[:, list(erase)] = False
        recall.held = held
    n = len(patterns)
    recall.previous = np.zeros((n, len(recall.association)))
    recall.past = np.zeros((n, recall.window - 1, recall.key_width))
    recall.ended = np.zeros(n, dtype=bool)


def answer(brain: cd.Brain, bank: dict, patterns, erase=()) -> np.ndarray:
    n = len(patterns)
    install(brain, bank, patterns, erase)
    brain.act(event(NEUTRAL, n), greedy=True)
    return np.asarray(brain.act(event(ASK, n), greedy=True)).reshape(n)


def sample(rng, n: int, panel: set) -> list:
    out = []
    while len(out) < n:
        p = tuple(int(v) for v in rng.integers(VALUES, size=ROLES))
        if p[:2] in panel:
            out.append(p)
    return out


def train(brain: cd.Brain, bank: dict, lessons: int, seed: int) -> dict:
    rng = np.random.default_rng(1000 + seed)
    level, refused, calm_from = 1.0, 0, None
    for lesson in range(lessons):
        patterns = sample(rng, 16, TAUGHT)
        try:
            wrong = answer(brain, bank, patterns) != labels(patterns)
            level = 0.95 * level + 0.05 * float(wrong.mean())
            calm = level < 0.02
            if calm != brain.learner.config.surprise:
                brain.retune(learning_surprise=calm)
                calm_from = lesson if calm and calm_from is None else calm_from
            n = len(patterns)
            install(brain, bank, patterns)
            brain.act(event(NEUTRAL, n), greedy=True)
            brain.lesson(event(ASK, n), labels(patterns))
        except RuntimeError:
            refused += 1
    return {"lessons": lessons, "refused": refused, "calm_from": calm_from}


def accuracy(brain: cd.Brain, bank: dict, patterns, erase=(), clone=False) -> dict:
    trial = deepcopy(brain)
    if clone and trial.recall.heads > 1:  # head 1 reads with head 0's address
        trial.recall.head_maps[0] = tuple(a.copy() for a in trial.recall.head_map(0))
    try:
        choice = answer(trial, bank, patterns, erase)
    except RuntimeError as error:
        return {"refused": str(error)[:80]}
    out = {"accuracy": float(np.mean(choice == labels(patterns)))}
    heads = trial.recall.attended_heads or ()
    roles = [RECORD[j][1] for j in range(ROLES)]
    tops = [np.asarray(p)[:, roles].argmax(axis=1) for p in heads if p is not None]
    if len(tops) == 2:
        out["distinct_top"] = float(np.mean(tops[0] != tops[1]))
        pair = np.sort(np.stack(tops), axis=0)  # the two heads' top roles, per trial
        out["relevant_pair"] = float(np.mean((pair[0] == 0) & (pair[1] == 1)))
    return out


def run(seed: int, heads: int, lessons: int) -> dict:
    t0 = time.time()
    brain = compose(seed, heads)
    warm(brain)
    bank = banks(brain)
    training = train(brain, bank, lessons, seed)
    rng = np.random.default_rng(99)
    taught, held = sample(rng, 192, TAUGHT), sample(rng, 192, HELD)
    out = {"heads": heads, "training": training,
           "taught": accuracy(brain, bank, taught), "held": accuracy(brain, bank, held),
           "held_controls": {
               "role0_erased": accuracy(brain, bank, held, RECORD[0]),
               "role1_erased": accuracy(brain, bank, held, RECORD[1]),
               "distractors_erased": accuracy(brain, bank, held, RECORD[2] + RECORD[3]),
               "memory_off": accuracy(brain, bank, held, sum(RECORD.values(), [])),
           }}
    if heads == 2:
        out["held_controls"]["clone_head"] = accuracy(brain, bank, held, clone=True)
    out["seconds"] = round(time.time() - t0, 1)
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--seeds", type=int, nargs="+", required=True)
    p.add_argument("--lessons", type=int, default=1024)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    split = report("V0.5B", *split_v05b(), 9)
    assert split["tests_conjunctive_generalization"], split  # the admission gate
    result = {"cadence": cd.__version__, "split": split,
              "founders": [{"seed": s, "H2": run(s, 2, a.lessons), "H1": run(s, 1, a.lessons)}
                           for s in a.seeds]}
    with open(a.out, "w") as f:
        json.dump(result, f, indent=1)
    for f_ in result["founders"]:
        print(f_["seed"], {arm: (f_[arm]["taught"].get("accuracy"), f_[arm]["held"].get("accuracy"))
                           for arm in ("H2", "H1")})


if __name__ == "__main__":
    main()
