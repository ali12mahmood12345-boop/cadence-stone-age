"""Cadence Stone Age V7.21 — Variable-Length Temporal Addressing.

V7.20 confirmed a predecessor->successor solution: with START present during learning,
weak-P1 founders learned P1 by attending START and reading START.next = E1. That closes the
boundary asymmetry. V7.21 asks the next question: did positional recall learn a real
cross-length ordinal rule, or only fixed ages that happened to solve five-event streams?

Fresh founders are trained in three matched arms:

  FIXED5_POSITION32     START + five events only, recall_position=32
  VARIABLE_POSITION32   START + lengths 3..7, recall_position=32
  VARIABLE_POSITION0    same variable curriculum, recall_position=0

All arms are tested on the exact same held-out variable-length panel (lengths 3..7). P1/P2
Recall attention is logged. A genuine cross-length rule should track the correct predecessor
slot as its *age changes with sequence length*, rather than continuing to select the age that
was correct in a five-event story.
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
import warnings
from dataclasses import dataclass
from importlib.metadata import version as pkg_version
from pathlib import Path
from typing import Any

import numpy as np
import cadence as cd

import stone_age_v7_17_reference as v717

VERSION = "0.91.1"
FOUNDER_START = 87001
DEFAULT_FOUNDERS = 12
MIN_VALID = 10

LENGTHS = (3, 4, 5, 6, 7)
MAX_QUERY_POSITIONS = 5
TRAIN_EPISODES = 1980  # 90 of each of the 22 valid (length, position) pairs
TEST_EPISODES = 1100   # 50 of each valid pair
START = True
ARMS = ("FIXED5_POSITION32", "VARIABLE_POSITION32", "VARIABLE_POSITION0")

# Frozen interpretation gates. These are deliberately moderate: V7.21 is a mechanism test,
# not a leaderboard run.
BASELINE_L5_FLOOR = 0.85
VARIABLE_OVERALL_FLOOR = 0.80
VARIABLE_LENGTH_FLOOR = 0.70
OFFLENGTH_GAIN_FLOOR = 0.15
POSITION_GAIN_FLOOR = 0.15
PREDECESSOR_TRACK_FLOOR = 0.70


@dataclass(frozen=True)
class Episode:
    events: tuple[int, ...]
    query_position: int  # 0..4, always < len(events)
    label: int
    length: int


def median(xs):
    xs = list(xs)
    return statistics.median(xs) if xs else 0.0


def mean(xs):
    xs = list(xs)
    return statistics.fmean(xs) if xs else 0.0


def query_name(q: int) -> str:
    return f"P{q + 1}"


def query_vector(ep: Episode) -> np.ndarray:
    return v717.one_hot(v717.QUERY_OFFSET + ep.query_position)


def make_stream(rng: np.random.Generator, length: int, q: int) -> tuple[int, ...]:
    """Random non-degenerate resource stream with the recent-event shortcut blocked."""
    events = [int(rng.integers(v717.N_ACTIONS))]
    for _ in range(1, length):
        candidates = [x for x in range(v717.N_ACTIONS) if x != events[-1]]
        events.append(int(candidates[int(rng.integers(len(candidates)))]) )

    # For every non-last query, the target resource may not equal the final resource.
    if q < length - 1 and events[q] == events[-1]:
        forbidden = {events[-1]}
        if q > 0:
            forbidden.add(events[q - 1])
        if q + 1 < length:
            forbidden.add(events[q + 1])
        candidates = [x for x in range(v717.N_ACTIONS) if x not in forbidden]
        if not candidates:
            candidates = [x for x in range(v717.N_ACTIONS) if x != events[-1]]
        events[q] = int(candidates[int(rng.integers(len(candidates)))])

    assert len(events) == length
    assert all(events[i] != events[i - 1] for i in range(1, length))
    if q < length - 1:
        assert events[q] != events[-1]
    return tuple(events)


def variable_pairs() -> list[tuple[int, int]]:
    return [
        (length, q)
        for length in LENGTHS
        for q in range(min(MAX_QUERY_POSITIONS, length))
    ]


def make_variable_episodes(founder: int, phase: int, count: int) -> list[Episode]:
    pairs = variable_pairs()
    if count % len(pairs) != 0:
        raise ValueError(f"variable episode count must be divisible by {len(pairs)}")
    rng = np.random.default_rng(np.random.SeedSequence([founder, phase, 721]))
    schedule = pairs * (count // len(pairs))
    rng.shuffle(schedule)
    out = []
    for length, q in schedule:
        events = make_stream(rng, length, q)
        out.append(Episode(events, q, int(events[q]), length))
    return out


def make_fixed5_episodes(founder: int, phase: int, count: int) -> list[Episode]:
    if count % 5 != 0:
        raise ValueError("fixed-five episode count must be divisible by 5")
    rng = np.random.default_rng(np.random.SeedSequence([founder, phase, 721]))
    qs = list(range(5)) * (count // 5)
    rng.shuffle(qs)
    out = []
    for q in qs:
        events = make_stream(rng, 5, q)
        out.append(Episode(events, q, int(events[q]), 5))
    return out


def compose(founder: int, arm: str) -> cd.Brain:
    if arm in ("FIXED5_POSITION32", "VARIABLE_POSITION32"):
        return v717.compose(founder, "POSITION32")
    if arm == "VARIABLE_POSITION0":
        return v717.compose(founder, "POSITION0")
    raise ValueError(arm)


def hear(brain: cd.Brain, ep: Episode) -> None:
    brain.reset()
    if START:
        brain.act(np.zeros((1, v717.INPUTS), dtype=np.float64), greedy=True)
    for event in ep.events:
        brain.act(v717.one_hot(event), greedy=True)


def teach(brain: cd.Brain, ep: Episode) -> dict[str, Any]:
    hear(brain, ep)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        report = brain.lesson(query_vector(ep), np.asarray([ep.label]))
        brain.act(query_vector(ep), greedy=True)
    out = {}
    for name in ("accepted", "agreed", "position_rows", "position_refused"):
        if hasattr(report, name):
            value = getattr(report, name)
            if isinstance(value, np.generic):
                value = value.item()
            out[name] = value
    return out


def train(brain: cd.Brain, episodes: list[Episode]) -> dict[str, Any]:
    result = {
        "lessons": 0,
        "accepted_sum": 0.0,
        "agreed_sum": 0.0,
        "position_rows_sum": 0.0,
        "position_refused_sum": 0.0,
        "runtime_errors": [],
    }
    for ep in episodes:
        try:
            report = teach(brain, ep)
            result["lessons"] += 1
            for key, out_key in (
                ("accepted", "accepted_sum"),
                ("agreed", "agreed_sum"),
                ("position_rows", "position_rows_sum"),
                ("position_refused", "position_refused_sum"),
            ):
                if key in report:
                    try:
                        result[out_key] += float(report[key])
                    except (TypeError, ValueError):
                        pass
        except Exception as exc:
            result["runtime_errors"].append(f"{type(exc).__name__}: {exc}")
            break
    return result


def event_name(vec: np.ndarray) -> str:
    a = np.asarray(vec, dtype=float).reshape(-1)
    if not np.any(np.abs(a) > 1e-12):
        return "START/ZERO"
    i = int(np.argmax(a))
    if i < len(v717.EVENTS) and a[i] > 0:
        return v717.EVENTS[i]
    if v717.QUERY_OFFSET <= i < v717.QUERY_OFFSET + 5:
        return query_name(i - v717.QUERY_OFFSET)
    return f"IDX{i}"


def evaluate(brain: cd.Brain, episodes: list[Episode], arm: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if brain.recall is None:
        raise ValueError("V7.21 requires Recall")
    if float(brain.recall.recency) != 0.0:
        raise AssertionError("recall_recency changed")

    hits = 0
    length_hits = {length: 0 for length in LENGTHS}
    length_counts = {length: 0 for length in LENGTHS}
    position_hits = {q: 0 for q in range(5)}
    position_counts = {q: 0 for q in range(5)}
    pair_hits = {f"L{length}_{query_name(q)}": 0 for length, q in variable_pairs()}
    pair_counts = {f"L{length}_{query_name(q)}": 0 for length, q in variable_pairs()}
    records: list[dict[str, Any]] = []
    errors: list[str] = []

    try:
        for ti, ep in enumerate(episodes):
            hear(brain, ep)
            values = np.asarray(brain.recall.values, dtype=float).copy()
            nexts = np.asarray(brain.recall.nexts, dtype=float).copy()
            slots = int(brain.recall.slots)
            expected_slots = ep.length + 1  # START + events
            if slots != expected_slots:
                raise AssertionError(f"{arm}: expected {expected_slots} slots, got {slots}")

            answer = int(np.asarray(brain.act(query_vector(ep), greedy=True)).reshape(-1)[0])
            answer = max(0, min(v717.N_ACTIONS - 1, answer))
            ok = int(answer == ep.label)
            hits += ok
            length_hits[ep.length] += ok
            length_counts[ep.length] += 1
            position_hits[ep.query_position] += ok
            position_counts[ep.query_position] += 1
            pair = f"L{ep.length}_{query_name(ep.query_position)}"
            pair_hits[pair] += ok
            pair_counts[pair] += 1

            if ep.query_position in (0, 1):
                weights = [] if brain.recall.attended is None else np.asarray(
                    brain.recall.attended, dtype=float
                ).reshape(1, -1)[0].tolist()
                n = len(weights)
                target = ep.query_position + 1  # slot 0 is START
                predecessor = ep.query_position
                top = int(np.argmax(weights)) if weights else -1
                ages = list(range(n - 1, -1, -1))
                predecessor_age = ep.length - ep.query_position
                fixed5_predecessor_age = 5 - ep.query_position

                def w(i: int) -> float:
                    return float(weights[i]) if 0 <= i < n else 0.0

                def vn(i: int) -> str:
                    return event_name(values[0, i]) if 0 <= i < values.shape[1] else "NONE"

                def nn(i: int) -> str:
                    return event_name(nexts[0, i]) if 0 <= i < nexts.shape[1] else "NONE"

                role = "other"
                if top == target:
                    role = "target"
                elif top == predecessor:
                    role = "predecessor"
                elif top == 0:
                    role = "oldest"
                elif top == n - 1:
                    role = "newest"

                records.append({
                    "arm": arm,
                    "test_index": ti,
                    "length": ep.length,
                    "query": query_name(ep.query_position),
                    "correct": ok,
                    "answer": v717.ACTIONS[answer],
                    "label": v717.ACTIONS[ep.label],
                    "slots": n,
                    "target_slot": target,
                    "predecessor_slot": predecessor,
                    "predecessor_age": predecessor_age,
                    "fixed5_predecessor_age": fixed5_predecessor_age,
                    "top_slot": top,
                    "top_role": role,
                    "top_age": ages[top] if 0 <= top < len(ages) else -1,
                    "top_weight": w(top),
                    "target_weight": w(target),
                    "predecessor_weight": w(predecessor),
                    "top_is_correct_predecessor": int(top == predecessor),
                    "top_is_fixed5_age": int(0 <= top < len(ages) and ages[top] == fixed5_predecessor_age),
                    "target_value": vn(target),
                    "predecessor_value": vn(predecessor),
                    "predecessor_next": nn(predecessor),
                    "top_value": vn(top),
                    "top_next": nn(top),
                    "weights": weights,
                })
    except Exception as exc:
        errors.append(f"{type(exc).__name__}: {exc}")

    per_length = {
        f"L{length}": (length_hits[length] / length_counts[length] if length_counts[length] else 0.0)
        for length in LENGTHS
    }
    per_position = {
        query_name(q): (position_hits[q] / position_counts[q] if position_counts[q] else 0.0)
        for q in range(5)
    }
    per_pair = {
        key: (pair_hits[key] / pair_counts[key] if pair_counts[key] else 0.0)
        for key in pair_hits
    }
    l5_hits = length_hits[5]
    l5_count = length_counts[5]
    off_hits = sum(length_hits[l] for l in LENGTHS if l != 5)
    off_count = sum(length_counts[l] for l in LENGTHS if l != 5)
    expected_pair_count = len(episodes) // len(variable_pairs())
    balanced = (
        len(episodes) % len(variable_pairs()) == 0
        and all(pair_counts[k] == expected_pair_count for k in pair_counts)
    )

    return ({
        "valid": int(not errors and balanced and sum(length_counts.values()) == len(episodes)),
        "accuracy": hits / len(episodes),
        "l5_accuracy": l5_hits / l5_count if l5_count else 0.0,
        "offlength_accuracy": off_hits / off_count if off_count else 0.0,
        "per_length": per_length,
        "per_position": per_position,
        "per_pair": per_pair,
        "tests": {
            "total": sum(length_counts.values()),
            "pair_count": expected_pair_count,
            **{f"L{l}": length_counts[l] for l in LENGTHS},
        },
        "runtime_errors": errors,
    }, records)


def position_maps_moved(brain: cd.Brain) -> bool:
    maps = getattr(getattr(brain, "recall", None), "position_maps", None)
    if not maps:
        return False
    return bool(any(np.abs(np.asarray(m)).sum() > 0 for hm in maps for m in hm))


def run_founder(founder: int) -> dict[str, Any]:
    fixed_train = make_fixed5_episodes(founder, 1, TRAIN_EPISODES)
    variable_train = make_variable_episodes(founder, 2, TRAIN_EPISODES)
    test = make_variable_episodes(founder, 3, TEST_EPISODES)

    arms = {}
    all_attention = []
    valid = True

    for arm in ARMS:
        brain = compose(founder, arm)
        training_episodes = fixed_train if arm == "FIXED5_POSITION32" else variable_train
        tr = train(brain, training_episodes)
        if tr["runtime_errors"] or tr["lessons"] != TRAIN_EPISODES:
            arms[arm] = {
                "training": tr,
                "position_maps_moved": position_maps_moved(brain),
                "test": None,
            }
            valid = False
            continue
        test_result, attention = evaluate(brain, test, arm)
        for row in attention:
            row["founder"] = founder
        all_attention.extend(attention)
        arms[arm] = {
            "training": tr,
            "position_maps_moved": position_maps_moved(brain),
            "test": test_result,
        }
        valid = valid and bool(test_result["valid"])

    return {"founder": founder, "valid": int(valid), "arms": arms, "attention": all_attention}


def attention_summary(records: list[dict[str, Any]], arm: str, *, offlength_only: bool = False) -> dict[str, Any]:
    rows = [
        r for r in records
        if r["arm"] == arm and (not offlength_only or r["length"] != 5)
    ]
    out = {
        "n": len(rows),
        "accuracy": mean(r["correct"] for r in rows),
        "median_predecessor_weight": median(r["predecessor_weight"] for r in rows),
        "median_target_weight": median(r["target_weight"] for r in rows),
        "top_predecessor_rate": mean(r["top_is_correct_predecessor"] for r in rows),
        "top_fixed5_age_rate": mean(r["top_is_fixed5_age"] for r in rows),
        "by_length": {},
    }
    for length in LENGTHS:
        lr = [r for r in rows if r["length"] == length]
        if lr:
            out["by_length"][f"L{length}"] = {
                "n": len(lr),
                "accuracy": mean(r["correct"] for r in lr),
                "top_predecessor_rate": mean(r["top_is_correct_predecessor"] for r in lr),
                "top_fixed5_age_rate": mean(r["top_is_fixed5_age"] for r in lr),
                "median_predecessor_weight": median(r["predecessor_weight"] for r in lr),
            }
    return out


def summarize(founders: list[dict[str, Any]], records: list[dict[str, Any]]) -> dict[str, Any]:
    valid = [f for f in founders if f["valid"]]
    s: dict[str, Any] = {
        "founders": len(founders),
        "valid_founders": len(valid),
    }

    def test(f, arm):
        return f["arms"][arm]["test"]

    for arm in ARMS:
        rr = [test(f, arm) for f in valid]
        s[f"median_{arm}_overall"] = median(r["accuracy"] for r in rr)
        s[f"median_{arm}_l5"] = median(r["l5_accuracy"] for r in rr)
        s[f"median_{arm}_offlength"] = median(r["offlength_accuracy"] for r in rr)
        for length in LENGTHS:
            s[f"median_{arm}_L{length}"] = median(r["per_length"][f"L{length}"] for r in rr)
        for q in range(5):
            s[f"median_{arm}_P{q + 1}"] = median(r["per_position"][f"P{q + 1}"] for r in rr)
        s[f"position_maps_moved_{arm}"] = sum(
            bool(f["arms"][arm]["position_maps_moved"]) for f in valid
        )

    if valid:
        s["median_variable_minus_fixed_offlength"] = median(
            test(f, "VARIABLE_POSITION32")["offlength_accuracy"]
            - test(f, "FIXED5_POSITION32")["offlength_accuracy"]
            for f in valid
        )
        s["median_variable_minus_position0_overall"] = median(
            test(f, "VARIABLE_POSITION32")["accuracy"]
            - test(f, "VARIABLE_POSITION0")["accuracy"]
            for f in valid
        )
        s["variable_min_length_median"] = min(
            s[f"median_VARIABLE_POSITION32_L{length}"] for length in LENGTHS
        )
    else:
        s["median_variable_minus_fixed_offlength"] = 0.0
        s["median_variable_minus_position0_overall"] = 0.0
        s["variable_min_length_median"] = 0.0

    valid_ids = {f["founder"] for f in valid}
    valid_records = [r for r in records if r["founder"] in valid_ids]
    attention = {
        arm: attention_summary(valid_records, arm) for arm in ARMS
    }
    attention_offlength = {
        arm: attention_summary(valid_records, arm, offlength_only=True) for arm in ARMS
    }

    gates = {
        "valid_founders": len(valid) >= MIN_VALID,
        "fixed5_baseline": s.get("median_FIXED5_POSITION32_L5", 0.0) >= BASELINE_L5_FLOOR,
        "variable_overall": s.get("median_VARIABLE_POSITION32_overall", 0.0) >= VARIABLE_OVERALL_FLOOR,
        "variable_each_length": s.get("variable_min_length_median", 0.0) >= VARIABLE_LENGTH_FLOOR,
        "beats_fixed_offlength": s.get("median_variable_minus_fixed_offlength", 0.0) >= OFFLENGTH_GAIN_FLOOR,
        "beats_position0": s.get("median_variable_minus_position0_overall", 0.0) >= POSITION_GAIN_FLOOR,
        "tracks_predecessor_offlength": attention_offlength["VARIABLE_POSITION32"].get("top_predecessor_rate", 0.0) >= PREDECESSOR_TRACK_FLOOR,
    }

    if all(gates.values()):
        diagnosis = "VARIABLE_LENGTH_POSITION_RULE_CONFIRMED"
    elif (
        gates["valid_founders"] and gates["fixed5_baseline"]
        and s.get("median_variable_minus_fixed_offlength", 0.0) >= 0.10
        and attention_offlength["VARIABLE_POSITION32"].get("top_predecessor_rate", 0.0) >= 0.60
    ):
        diagnosis = "VARIABLE_LENGTH_POSITION_RULE_PARTIAL"
    elif (
        gates["valid_founders"] and gates["fixed5_baseline"]
        and s.get("median_FIXED5_POSITION32_offlength", 0.0)
            <= s.get("median_FIXED5_POSITION32_L5", 0.0) - 0.20
        and s.get("median_variable_minus_fixed_offlength", 0.0) < 0.10
    ):
        diagnosis = "FIXED_AGE_LIMIT_SURVIVES_VARIABLE_TRAINING"
    else:
        diagnosis = "VARIABLE_LENGTH_MECHANISM_INCONCLUSIVE"

    return {
        "summary": s,
        "gates": gates,
        "attention": attention,
        "attention_offlength": attention_offlength,
        "diagnosis": diagnosis,
    }


def write_outputs(outdir: Path, founders: list[dict[str, Any]], records: list[dict[str, Any]], result: dict[str, Any]) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    clean_founders = []
    for founder in founders:
        f = dict(founder)
        f.pop("attention", None)
        clean_founders.append(f)

    payload = {
        "experiment": "Cadence Stone Age V7.21 Variable-Length Temporal Addressing",
        "cadence_net_version": VERSION,
        "protocol": {
            "founder_start": FOUNDER_START,
            "founders": len(founders),
            "lengths": list(LENGTHS),
            "training_episodes_per_arm": TRAIN_EPISODES,
            "test_episodes_per_arm": TEST_EPISODES,
            "valid_length_position_pairs": len(variable_pairs()),
            "fixed5_training": "START + length 5 only; exact-balanced P1..P5",
            "variable_training": "START + lengths 3..7; exact-balanced across all valid (length, position) pairs",
            "test": "same exact-balanced held-out variable panel for every arm",
            "arms": list(ARMS),
            "recall_recency": 0.0,
            "recall_next": True,
            "start_event": "constant all-zero 9D moment before E1 in every arm",
            "attention_log": "P1/P2; correct predecessor vs fixed-five predecessor age",
            "full_game": False,
            "episodic_memory": False,
            "reward_learning": False,
        },
        **result,
        "founders": clean_founders,
    }
    (outdir / "STONE_AGE_V7_21_RESULTS.json").write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")

    with (outdir / "STONE_AGE_V7_21_SUMMARY.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value"])
        for k, v in result["summary"].items():
            w.writerow([k, json.dumps(v) if isinstance(v, (list, dict)) else v])
        for k, v in result["gates"].items():
            w.writerow([f"gate_{k}", int(bool(v))])
        w.writerow(["diagnosis", result["diagnosis"]])

    fields = ["founder", "valid"]
    for arm in ARMS:
        fields += [f"{arm}_overall", f"{arm}_L5", f"{arm}_offlength"]
        fields += [f"{arm}_L{l}" for l in LENGTHS]
        fields += [f"{arm}_P{i}" for i in range(1, 6)]
    with (outdir / "STONE_AGE_V7_21_PER_FOUNDER.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for founder in founders:
            row = {"founder": founder["founder"], "valid": founder["valid"]}
            for arm in ARMS:
                t = founder.get("arms", {}).get(arm, {}).get("test")
                row[f"{arm}_overall"] = t["accuracy"] if t else ""
                row[f"{arm}_L5"] = t["l5_accuracy"] if t else ""
                row[f"{arm}_offlength"] = t["offlength_accuracy"] if t else ""
                for l in LENGTHS:
                    row[f"{arm}_L{l}"] = t["per_length"][f"L{l}"] if t else ""
                for i in range(1, 6):
                    row[f"{arm}_P{i}"] = t["per_position"][f"P{i}"] if t else ""
            w.writerow(row)

    attention_fields = [
        "founder", "arm", "test_index", "length", "query", "correct", "answer", "label",
        "slots", "target_slot", "predecessor_slot", "predecessor_age", "fixed5_predecessor_age",
        "top_slot", "top_role", "top_age", "top_weight", "target_weight", "predecessor_weight",
        "top_is_correct_predecessor", "top_is_fixed5_age", "target_value", "predecessor_value",
        "predecessor_next", "top_value", "top_next", "weights",
    ]
    with (outdir / "STONE_AGE_V7_21_ATTENTION.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=attention_fields)
        w.writeheader()
        for r in records:
            d = dict(r)
            d["weights"] = json.dumps(d["weights"], separators=(",", ":"))
            w.writerow(d)

    s = result["summary"]
    a_var = result["attention_offlength"]["VARIABLE_POSITION32"]
    a_fixed = result["attention_offlength"]["FIXED5_POSITION32"]
    lines = [
        "CADENCE STONE AGE V7.21 — VARIABLE-LENGTH TEMPORAL ADDRESSING",
        "=" * 118,
        f"cadence-net: {VERSION}",
        f"fresh founders: {FOUNDER_START}..{FOUNDER_START + len(founders) - 1}",
        "",
        "QUESTION",
        "After V7.20 confirmed the START->next predecessor route, does positional recall learn",
        "a cross-length ordinal rule, or does five-event training only learn fixed slot ages?",
        "",
        f"VALID FOUNDERS: {s['valid_founders']}/{len(founders)} (minimum {MIN_VALID})",
        "",
        "MEDIANS — HELD-OUT LENGTHS 3..7",
        f"  FIXED5_POSITION32 overall:   {s.get('median_FIXED5_POSITION32_overall', 0):.1%}",
        f"    L5:                        {s.get('median_FIXED5_POSITION32_L5', 0):.1%}",
        f"    off-length:                {s.get('median_FIXED5_POSITION32_offlength', 0):.1%}",
        f"  VARIABLE_POSITION32 overall: {s.get('median_VARIABLE_POSITION32_overall', 0):.1%}",
        f"    min length median:         {s.get('variable_min_length_median', 0):.1%}",
        f"    off-length:                {s.get('median_VARIABLE_POSITION32_offlength', 0):.1%}",
        f"  VARIABLE_POSITION0 overall:  {s.get('median_VARIABLE_POSITION0_overall', 0):.1%}",
        "",
        "PAIRED EFFECTS",
        f"  VARIABLE32 - FIXED5 off-length: {s.get('median_variable_minus_fixed_offlength', 0):+.1%}",
        f"  VARIABLE32 - POSITION0 overall: {s.get('median_variable_minus_position0_overall', 0):+.1%}",
        "",
        "VARIABLE_POSITION32 — PER LENGTH",
    ]
    for l in LENGTHS:
        lines.append(f"  L{l}: {s.get(f'median_VARIABLE_POSITION32_L{l}', 0):.1%}")
    lines += [
        "",
        "ATTENTION P1/P2 — OFF-LENGTH TESTS",
        f"  FIXED5 top correct predecessor:  {a_fixed.get('top_predecessor_rate', 0):.1%}",
        f"  FIXED5 top fixed-five age:       {a_fixed.get('top_fixed5_age_rate', 0):.1%}",
        f"  VARIABLE top correct predecessor:{a_var.get('top_predecessor_rate', 0):.1%}",
        f"  VARIABLE top fixed-five age:     {a_var.get('top_fixed5_age_rate', 0):.1%}",
        "",
        "PRE-REGISTERED GATES",
    ]
    for k, v in result["gates"].items():
        lines.append(f"- {k}: {bool(v)}")
    lines += [
        "",
        f"DIAGNOSTIC CLASSIFICATION: {result['diagnosis']}",
        "",
        "INTERPRETATION",
        "- VARIABLE32 succeeds across lengths and tracks the changing predecessor -> cross-length positional rule.",
        "- FIXED5 stays tied to the five-event predecessor age off-length -> fixed-age solution to the old curriculum.",
        "- VARIABLE_POSITION0 controls whether the learned position term is causally needed.",
        "",
        "BOUNDARIES",
        "1. Bounded resource-stream component test; not full-game Stone Age integration.",
        "2. Query vocabulary remains P1..P5; shorter streams only use valid positions.",
        "3. START is present in every arm to remove the P1 missing-predecessor asymmetry localized in V7.20.",
        "4. Length is not supplied as a dedicated input; any length-sensitive solution must arise from the lived stream state.",
        "5. No episodic memory, attention module, reward learning, or post-hoc gate changes.",
    ]
    (outdir / "STONE_AGE_V7_21_REPORT.txt").write_text("\n".join(lines) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=Path("stone_age_v7_21_output"))
    ap.add_argument("--founders", type=int, default=DEFAULT_FOUNDERS)
    args = ap.parse_args()

    got = pkg_version("cadence-net")
    if got != VERSION:
        raise SystemExit(f"Need cadence-net=={VERSION}, got {got}")
    if args.founders < 1:
        raise SystemExit("--founders must be >=1")

    founders = []
    records = []
    print("=" * 118, flush=True)
    print(" CADENCE STONE AGE V7.21 — VARIABLE-LENGTH TEMPORAL ADDRESSING", flush=True)
    print("=" * 118, flush=True)
    for founder in range(FOUNDER_START, FOUNDER_START + args.founders):
        print(f"FOUNDER {founder}", flush=True)
        r = run_founder(founder)
        records.extend(r.get("attention", []))
        founders.append(r)
        status = "VALID" if r["valid"] else "INVALID"
        print(f"  -> {status}", flush=True)

    result = summarize(founders, records)
    write_outputs(args.output, founders, records, result)
    print("", flush=True)
    print("DIAGNOSIS:", result["diagnosis"], flush=True)
    print("Output:", args.output.resolve(), flush=True)


if __name__ == "__main__":
    main()

