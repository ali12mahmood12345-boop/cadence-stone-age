"""Cadence Representation Keys V0.1A — learned compact key proof-of-principle."""
from __future__ import annotations

import argparse
import csv
import json
import statistics
import tempfile
from importlib.metadata import version as pkg_version
from pathlib import Path

import numpy as np
from cadence import Brain

VERSION = "0.84.3"
SEED_START = 45001
DEFAULT_SEEDS = 24
CONCEPTS = 4
INPUTS = 36
NUISANCE = 32
NOISE = 0.7
MODULES = (24, 12)
ASSOC_DIM = 12
FIXED_CODE_DIM = 128
TRAIN_BATCHES = 256
TRAIN_PER_CLASS_PER_BATCH = 8
POLICY_TEST_PER_CLASS = 64
BANK_PER_CLASS = 4
QUERY_PER_CLASS = 64
POLICY_GATE = 0.85
MIN_ELIGIBLE = 12
MEDIAN_GAIN_GATE = 0.10
MEDIAN_TRAINED_RETRIEVAL_GATE = 0.80


def mean(xs):
    return statistics.fmean(xs) if xs else 0.0


def median(xs):
    return statistics.median(xs) if xs else 0.0


def ceil_fraction(n: int, num: int, den: int) -> int:
    return max(1, (num * n + den - 1) // den)


def rng_for(seed: int, salt: int):
    return np.random.default_rng(np.random.SeedSequence([int(seed), int(salt)]))


def make_examples(seed: int, per_class: int, salt: int):
    rng = rng_for(seed, salt)
    rows, labels = [], []
    for c in range(CONCEPTS):
        for _ in range(per_class):
            x = np.zeros(INPUTS, dtype=np.float64)
            x[c] = 1.0
            x[CONCEPTS:] = rng.uniform(-NOISE, NOISE, size=NUISANCE)
            rows.append(x)
            labels.append(c)
    order = rng.permutation(len(rows))
    X = np.asarray(rows, dtype=np.float64)[order]
    y = np.asarray(labels, dtype=np.int64)[order]
    return X, y


def training_batches(seed: int):
    rng = rng_for(seed, 51001)
    for _ in range(TRAIN_BATCHES):
        rows, labels = [], []
        for c in range(CONCEPTS):
            for _ in range(TRAIN_PER_CLASS_PER_BATCH):
                x = np.zeros(INPUTS, dtype=np.float64)
                x[c] = 1.0
                x[CONCEPTS:] = rng.uniform(-NOISE, NOISE, size=NUISANCE)
                rows.append(x)
                labels.append(c)
        order = rng.permutation(len(rows))
        yield np.asarray(rows, dtype=np.float64)[order], np.asarray(labels, dtype=np.int64)[order]


def new_brain(seed: int):
    return Brain.compose(inputs=INPUTS, actions=CONCEPTS, modules=MODULES, seed=int(seed), recall=False)


def normalize_rows(a: np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=np.float64)
    norms = np.linalg.norm(a, axis=1, keepdims=True)
    if not np.isfinite(a).all() or (norms <= 1e-12).any():
        raise RuntimeError("representation contains nonfinite or zero-norm row")
    return a / norms


def assoc_and_actions(brain: Brain, X: np.ndarray):
    idx = np.asarray(brain.association_index, dtype=np.int64)
    if len(idx) != ASSOC_DIM:
        raise RuntimeError(f"unexpected association width {len(idx)}")
    keys, actions = [], []
    for row in X:
        brain.reset()
        action = int(np.asarray(brain.act(row.reshape(1, -1), greedy=True)).reshape(-1)[0])
        state = brain.basal_ganglia.state
        if state is None:
            raise RuntimeError("greedy act left no readable basal-ganglia state")
        key = np.asarray(state.activation[0, idx], dtype=np.float64)
        if key.shape != (ASSOC_DIM,) or not np.isfinite(key).all():
            raise RuntimeError("invalid association key")
        keys.append(key)
        actions.append(action)
    return np.asarray(keys), np.asarray(actions, dtype=np.int64)


def fixed_codes(seed: int, X: np.ndarray):
    brain = Brain.compose(
        inputs=INPUTS,
        actions=CONCEPTS,
        modules=MODULES,
        code=FIXED_CODE_DIM,
        seed=int(seed),
        recall=False,
    )
    out = np.asarray(brain.observation_code(X), dtype=np.float64)
    if out.shape != (len(X), FIXED_CODE_DIM):
        raise RuntimeError(f"unexpected fixed code shape {out.shape}")
    return out


def retrieval(bank_keys, bank_y, query_keys, query_y):
    B = normalize_rows(bank_keys)
    Q = normalize_rows(query_keys)
    sims = Q @ B.T
    best = np.argmax(sims, axis=1)
    pred = bank_y[best]
    acc = float(np.mean(pred == query_y))
    margins = []
    for i, label in enumerate(query_y):
        same = sims[i, bank_y == label]
        other = sims[i, bank_y != label]
        margins.append(float(np.max(same) - np.max(other)))
    return {
        "accuracy": acc,
        "mean_margin": mean(margins),
        "median_margin": median(margins),
    }


def run_seed(seed: int, work: Path):
    bank_X, bank_y = make_examples(seed, BANK_PER_CLASS, 52001)
    query_X, query_y = make_examples(seed, QUERY_PER_CLASS, 52002)
    test_X, test_y = make_examples(seed, POLICY_TEST_PER_CLASS, 52003)

    brain = new_brain(seed)
    init_path = work / f"seed_{seed}_initial.npz"
    trained_path = work / f"seed_{seed}_trained.npz"
    brain.save(init_path)

    accepted = 0.0
    presentations = 0
    for Xb, yb in training_batches(seed):
        brain.reset()
        report = brain.lesson(Xb, yb)
        presentations += len(yb)
        accepted += float(report.get("accepted_presentations", report.get("presentations", len(yb))))
    brain.save(trained_path)

    initial = Brain.load(init_path)
    trained = Brain.load(trained_path)

    trained_test_keys, test_actions = assoc_and_actions(trained, test_X)
    policy_acc = float(np.mean(test_actions == test_y))
    eligible = int(policy_acc >= POLICY_GATE)

    init_bank, _ = assoc_and_actions(initial, bank_X)
    init_query, _ = assoc_and_actions(initial, query_X)
    trained_bank, _ = assoc_and_actions(trained, bank_X)
    trained_query, _ = assoc_and_actions(trained, query_X)

    raw = retrieval(bank_X, bank_y, query_X, query_y)
    fixed = retrieval(fixed_codes(seed, bank_X), bank_y, fixed_codes(seed, query_X), query_y)
    untrained_assoc = retrieval(init_bank, bank_y, init_query, query_y)
    trained_assoc = retrieval(trained_bank, bank_y, trained_query, query_y)

    return {
        "seed": seed,
        "training_presentations": presentations,
        "reported_accepted_presentations": accepted,
        "policy_test_accuracy": policy_acc,
        "eligible": eligible,
        "raw_accuracy": raw["accuracy"],
        "raw_mean_margin": raw["mean_margin"],
        "fixed_sparse_accuracy": fixed["accuracy"],
        "fixed_sparse_mean_margin": fixed["mean_margin"],
        "untrained_assoc_accuracy": untrained_assoc["accuracy"],
        "untrained_assoc_mean_margin": untrained_assoc["mean_margin"],
        "trained_assoc_accuracy": trained_assoc["accuracy"],
        "trained_assoc_mean_margin": trained_assoc["mean_margin"],
        "trained_minus_untrained": trained_assoc["accuracy"] - untrained_assoc["accuracy"],
        "trained_minus_raw": trained_assoc["accuracy"] - raw["accuracy"],
        "trained_minus_fixed_sparse": trained_assoc["accuracy"] - fixed["accuracy"],
    }


def classify(rows):
    eligible = [r for r in rows if r["eligible"]]
    n = len(eligible)
    min_wins = ceil_fraction(n, 2, 3) if n else 1
    wins_untrained = sum(r["trained_assoc_accuracy"] > r["untrained_assoc_accuracy"] for r in eligible)
    wins_raw = sum(r["trained_assoc_accuracy"] > r["raw_accuracy"] for r in eligible)
    med_untrained = median([r["trained_minus_untrained"] for r in eligible])
    med_raw = median([r["trained_minus_raw"] for r in eligible])
    med_trained = median([r["trained_assoc_accuracy"] for r in eligible])
    gates = {
        "enough_eligible": n >= MIN_ELIGIBLE,
        "beats_untrained_fraction": n > 0 and wins_untrained >= min_wins,
        "beats_untrained_median": med_untrained >= MEDIAN_GAIN_GATE,
        "beats_raw_fraction": n > 0 and wins_raw >= min_wins,
        "beats_raw_median": med_raw >= MEDIAN_GAIN_GATE,
        "trained_retrieval_level": med_trained >= MEDIAN_TRAINED_RETRIEVAL_GATE,
    }
    if not gates["enough_eligible"]:
        diagnosis = "INSUFFICIENT_TASK_LEARNING"
    elif all(gates.values()):
        diagnosis = "LEARNED_COMPACT_KEY_SIGNAL"
    elif gates["beats_untrained_fraction"] and gates["beats_untrained_median"]:
        diagnosis = "LEARNED_REPRESENTATION_CHANGED_BUT_NO_RAW_KEY_GAIN"
    else:
        diagnosis = "NO_LEARNED_KEY_SIGNAL"
    return diagnosis, gates, eligible, wins_untrained, wins_raw, min_wins


def write_outputs(out: Path, rows):
    diagnosis, gates, eligible, wins_untrained, wins_raw, min_wins = classify(rows)
    n = len(eligible)
    summary = {
        "founders": len(rows),
        "eligible_founders": n,
        "median_policy_accuracy_eligible": median([r["policy_test_accuracy"] for r in eligible]),
        "trained_beats_untrained": wins_untrained,
        "trained_beats_raw": wins_raw,
        "required_two_thirds_wins": min_wins,
        "median_raw_accuracy": median([r["raw_accuracy"] for r in eligible]),
        "median_fixed_sparse_accuracy": median([r["fixed_sparse_accuracy"] for r in eligible]),
        "median_untrained_assoc_accuracy": median([r["untrained_assoc_accuracy"] for r in eligible]),
        "median_trained_assoc_accuracy": median([r["trained_assoc_accuracy"] for r in eligible]),
        "median_trained_minus_untrained": median([r["trained_minus_untrained"] for r in eligible]),
        "median_trained_minus_raw": median([r["trained_minus_raw"] for r in eligible]),
        "median_trained_minus_fixed_sparse": median([r["trained_minus_fixed_sparse"] for r in eligible]),
        "median_margin_raw": median([r["raw_mean_margin"] for r in eligible]),
        "median_margin_fixed_sparse": median([r["fixed_sparse_mean_margin"] for r in eligible]),
        "median_margin_untrained_assoc": median([r["untrained_assoc_mean_margin"] for r in eligible]),
        "median_margin_trained_assoc": median([r["trained_assoc_mean_margin"] for r in eligible]),
    }
    result = {
        "experiment": "Cadence Representation Keys V0.1A",
        "cadence_net_version": VERSION,
        "scope": "development learned compact key proof-of-principle",
        "protocol": {
            "seed_start": SEED_START,
            "seeds": len(rows),
            "concepts": CONCEPTS,
            "inputs": INPUTS,
            "nuisance_dims": NUISANCE,
            "nuisance_uniform_amplitude": NOISE,
            "modules": list(MODULES),
            "association_width": ASSOC_DIM,
            "fixed_sparse_width": FIXED_CODE_DIM,
            "train_batches": TRAIN_BATCHES,
            "train_rows_per_batch": CONCEPTS * TRAIN_PER_CLASS_PER_BATCH,
            "training_presentations": TRAIN_BATCHES * CONCEPTS * TRAIN_PER_CLASS_PER_BATCH,
            "policy_test_per_class": POLICY_TEST_PER_CLASS,
            "bank_per_class": BANK_PER_CLASS,
            "query_per_class": QUERY_PER_CLASS,
            "policy_gate": POLICY_GATE,
            "min_eligible": MIN_ELIGIBLE,
            "median_gain_gate": MEDIAN_GAIN_GATE,
            "median_trained_retrieval_gate": MEDIAN_TRAINED_RETRIEVAL_GATE,
            "two_thirds_win_gate": True,
        },
        "summary": summary,
        "gates": gates,
        "diagnosis": diagnosis,
        "per_seed": rows,
    }
    (out / "REPRESENTATION_KEYS_V0_1A_RESULTS.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    fields = list(rows[0].keys())
    with (out / "REPRESENTATION_KEYS_V0_1A_PER_SEED.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)

    with (out / "REPRESENTATION_KEYS_V0_1A_SUMMARY.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value"])
        for k, v in summary.items(): w.writerow([k, v])
        for k, v in gates.items(): w.writerow(["gate_" + k, int(bool(v))])
        w.writerow(["diagnosis", diagnosis])

    report = f"""CADENCE REPRESENTATION KEYS V0.1A — LEARNED COMPACT KEY PROOF-OF-PRINCIPLE REPORT
{'='*112}
cadence-net: {VERSION}
fresh development seeds: {SEED_START}..{SEED_START + len(rows) - 1}
4 concepts/actions | input 36 = 4 stable semantic + 32 nuisance Uniform(-0.7,+0.7)
network modules=(24,12) | learned association key width=12 | fixed sparse benchmark width=128
training=256 balanced batches x 32 rows = 8192 presentations
memory bank=4/concept | query=64/concept | cosine nearest-key retrieval
Development proof-of-principle only; no core-memory change and no confirmation claim.

TASK LEARNING SCREEN
policy eligibility: held-out greedy accuracy >= {POLICY_GATE:.0%}
eligible founders: {n}/{len(rows)} (frozen minimum {MIN_ELIGIBLE})
median held-out policy accuracy among eligible: {summary['median_policy_accuracy_eligible']:.1%}

MEMORY-KEY RETRIEVAL — ELIGIBLE FOUNDERS ONLY
median RAW retrieval:               {summary['median_raw_accuracy']:.1%}
median FIXED_SPARSE retrieval:      {summary['median_fixed_sparse_accuracy']:.1%}
median UNTRAINED_ASSOC retrieval:   {summary['median_untrained_assoc_accuracy']:.1%}
median TRAINED_ASSOC retrieval:     {summary['median_trained_assoc_accuracy']:.1%}

TRAINING EFFECT / RAW COMPARISON
TRAINED_ASSOC > UNTRAINED_ASSOC: {wins_untrained}/{n} (need >= {min_wins} when n>0)
median TRAINED - UNTRAINED: {summary['median_trained_minus_untrained']:+.3f} (need >= +{MEDIAN_GAIN_GATE:.2f})
TRAINED_ASSOC > RAW: {wins_raw}/{n} (need >= {min_wins} when n>0)
median TRAINED - RAW: {summary['median_trained_minus_raw']:+.3f} (need >= +{MEDIAN_GAIN_GATE:.2f})
median TRAINED - FIXED_SPARSE: {summary['median_trained_minus_fixed_sparse']:+.3f} (descriptive)
median TRAINED_ASSOC retrieval level: {summary['median_trained_assoc_accuracy']:.1%} (need >= {MEDIAN_TRAINED_RETRIEVAL_GATE:.0%})

FROZEN DEVELOPMENT CLASSIFICATION
DIAGNOSTIC CLASSIFICATION: {diagnosis}

INTERPRETATION BOUNDARY
1. The trained and untrained association arms are the exact same founder before vs after task learning.
2. RAW tests direct observation keys. FIXED_SPARSE is Cadence's current non-learned observation-code benchmark and is descriptive only.
3. A pass means task learning produced a compact association representation useful as a similarity key for held-out nuisance variants in this aligned concept/action task.
4. Concept identity equals taught action in V0.1A, so a pass does not prove the learned key preserves details irrelevant to the policy. A collision benchmark must separate memory identity from task label next.
5. No Cadence default change, memory implementation claim, semantic-abstraction claim, or general representation-learning claim is licensed by this development assay.
"""
    (out / "REPRESENTATION_KEYS_V0_1A_REPORT.txt").write_text(report, encoding="utf-8")
    return report, diagnosis


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="representation_keys_v0_1a_output")
    p.add_argument("--seeds", type=int, default=DEFAULT_SEEDS)
    args = p.parse_args()
    if pkg_version("cadence-net") != VERSION:
        raise RuntimeError(f"expected cadence-net {VERSION}, got {pkg_version('cadence-net')}")
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    work = out / "checkpoints"; work.mkdir(exist_ok=True)

    print("="*120)
    print(" CADENCE REPRESENTATION KEYS V0.1A — LEARNED COMPACT KEY PROOF-OF-PRINCIPLE")
    print("="*120)
    print(f"cadence-net: {VERSION}")
    print(f"fresh development seeds: {SEED_START}..{SEED_START + args.seeds - 1}")
    print("world: 4 semantic one-hot coordinates + 32 nuisance coordinates Uniform(-0.7,+0.7)")
    print("keys: RAW / FIXED_SPARSE(128) / exact UNTRAINED_ASSOC(12) / TRAINED_ASSOC(12)")
    print("DEVELOPMENT ONLY — proof of principle, not a memory-core change or confirmation")
    print()

    rows = []
    for seed in range(SEED_START, SEED_START + args.seeds):
        r = run_seed(seed, work)
        rows.append(r)
        print(
            f"seed={seed} policy={100*r['policy_test_accuracy']:5.1f}% eligible={r['eligible']} | "
            f"raw={100*r['raw_accuracy']:5.1f}% fixed={100*r['fixed_sparse_accuracy']:5.1f}% "
            f"untrained={100*r['untrained_assoc_accuracy']:5.1f}% trained={100*r['trained_assoc_accuracy']:5.1f}% | "
            f"T-U={100*r['trained_minus_untrained']:+5.1f}pp T-R={100*r['trained_minus_raw']:+5.1f}pp"
        )

    report, diagnosis = write_outputs(out, rows)
    print(); print(report)
    print(f"Saved to: {out.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
