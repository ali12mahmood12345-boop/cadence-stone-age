"""Cadence Stone Age V7.17 — Five-Position Temporal Addressing

Cadence 0.91.1.

Mechanistic extension of V7.16/V7.16R:
V7.16 established that learned Recall position can distinguish FIRST from LAST
in a five-event Stone Age resource stream. V7.17 asks whether the same mechanism
can retrieve the resource at *any* of the five temporal positions.

Task:
    hear five resource events
    receive one of five position-only query cues (P1..P5)
    output the action corresponding to the resource at that exact position

The query contains no resource identity. For P1..P4, the queried resource is
forced to differ from the final resource so the default working trace cannot
solve the non-last queries by simply returning the most recent event.

Arms:
    POSITION32  recall=True, recall_position=32
    POSITION0   recall=True, recall_position=0
    RECALL_OFF  recall=False

Fresh founders:
    85001..85008
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


VERSION = "0.91.1"

FOUNDER_START = 85001
DEFAULT_FOUNDERS = 8
MIN_VALID = 6

TRAIN_EPISODES = 2000
TEST_EPISODES = 500

EVENTS = ("WOOD", "STONE", "BERRY", "RABBIT")
ACTIONS = (
    "GATHER_WOOD",
    "GATHER_STONE",
    "PICK_BERRIES",
    "HUNT_RABBIT",
)

STREAM_LENGTH = 5
N_ACTIONS = 4
EVENT_INPUTS = 4
QUERY_OFFSET = EVENT_INPUTS
INPUTS = EVENT_INPUTS + STREAM_LENGTH  # 4 event symbols + P1..P5 query cues
QUERY_NAMES = tuple(f"P{i}" for i in range(1, STREAM_LENGTH + 1))

UNIFORM_CHANCE = 1.0 / N_ACTIONS
ARMS = ("POSITION32", "POSITION0", "RECALL_OFF")


@dataclass(frozen=True)
class Episode:
    events: tuple[int, int, int, int, int]
    query_position: int  # 0..4
    label: int


def median(xs):
    xs = list(xs)
    return statistics.median(xs) if xs else 0.0


def one_hot(index: int) -> np.ndarray:
    x = np.zeros((1, INPUTS), dtype=np.float64)
    x[0, int(index)] = 1.0
    return x


def make_episodes(founder: int, phase: int, count: int) -> list[Episode]:
    """Paired deterministic, position-balanced episodes shared by every arm."""
    if count % STREAM_LENGTH != 0:
        raise ValueError("episode count must be divisible by 5 for exact position balance")

    rng = np.random.default_rng(np.random.SeedSequence([founder, phase, 717]))
    query_positions = np.tile(np.arange(STREAM_LENGTH), count // STREAM_LENGTH)
    rng.shuffle(query_positions)

    out: list[Episode] = []

    for query_position in query_positions:
        q = int(query_position)

        # Generate a non-degenerate stream with no adjacent duplicate resource.
        events = [int(rng.integers(N_ACTIONS))]
        for _ in range(1, STREAM_LENGTH):
            candidates = [x for x in range(N_ACTIONS) if x != events[-1]]
            events.append(int(candidates[int(rng.integers(len(candidates)))]) )

        # For non-last queries, block the simplest working-trace shortcut:
        # the target resource may not equal the final resource.
        if q < STREAM_LENGTH - 1 and events[q] == events[-1]:
            candidates = [
                x for x in range(N_ACTIONS)
                if x != events[-1]
                and (q == 0 or x != events[q - 1])
                and (q == STREAM_LENGTH - 1 or x != events[q + 1])
            ]
            if not candidates:
                candidates = [x for x in range(N_ACTIONS) if x != events[-1]]
            events[q] = int(candidates[int(rng.integers(len(candidates)))])

        # Keep the stream locally non-degenerate after the edit above.
        for i in range(1, STREAM_LENGTH):
            if events[i] == events[i - 1]:
                candidates = [x for x in range(N_ACTIONS) if x != events[i - 1]]
                # Preserve the target-vs-last diagnostic constraint.
                if i == STREAM_LENGTH - 1 and q < STREAM_LENGTH - 1:
                    candidates = [x for x in candidates if x != events[q]] or candidates
                events[i] = int(candidates[int(rng.integers(len(candidates)))])

        assert len(events) == STREAM_LENGTH
        if q < STREAM_LENGTH - 1:
            assert events[q] != events[-1]

        out.append(
            Episode(
                events=tuple(int(x) for x in events),
                query_position=q,
                label=int(events[q]),
            )
        )

    return out


def compose(founder: int, arm: str) -> cd.Brain:
    common = dict(
        inputs=INPUTS,
        actions=N_ACTIONS,
        modules=(24,),
        seed=founder,
        episodic=False,
        teaching="normalized",
    )

    if arm == "POSITION32":
        return cd.Brain.compose(
            **common,
            recall=True,
            recall_position=32,
            recall_recency=0.0,
            recall_temperature=0.25,
        )

    if arm == "POSITION0":
        return cd.Brain.compose(
            **common,
            recall=True,
            recall_position=0,
            recall_recency=0.0,
            recall_temperature=0.25,
        )

    if arm == "RECALL_OFF":
        return cd.Brain.compose(**common, recall=False)

    raise ValueError(arm)


def hear_events(brain: cd.Brain, episode: Episode) -> None:
    brain.reset()
    for event in episode.events:
        brain.act(one_hot(event), greedy=True)


def query_vector(episode: Episode) -> np.ndarray:
    return one_hot(QUERY_OFFSET + episode.query_position)


def teach_query(brain: cd.Brain, episode: Episode) -> dict[str, Any]:
    """Teach before query act, matching the released 0.89 positional benchmark."""
    hear_events(brain, episode)
    query = query_vector(episode)

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        report = brain.lesson(query, np.asarray([episode.label]))
        brain.act(query, greedy=True)

    result: dict[str, Any] = {}
    for name in ("accepted", "agreed", "position_rows", "position_refused"):
        if hasattr(report, name):
            value = getattr(report, name)
            if isinstance(value, np.generic):
                value = value.item()
            result[name] = value
    return result


def position_maps_moved(brain: cd.Brain) -> bool:
    if getattr(brain, "recall", None) is None:
        return False

    maps = getattr(brain.recall, "position_maps", None)
    if maps is None:
        return False

    try:
        return bool(
            any(
                np.abs(np.asarray(m)).sum() > 0
                for head_maps in maps
                for m in head_maps
            )
        )
    except TypeError:
        return bool(any(np.abs(np.asarray(m)).sum() > 0 for m in maps))


def evaluate(brain: cd.Brain, episodes: list[Episode]) -> dict[str, Any]:
    hits = 0
    pos_hits = [0] * STREAM_LENGTH
    pos_counts = [0] * STREAM_LENGTH
    resource_hits = [0] * N_ACTIONS
    resource_counts = [0] * N_ACTIONS
    confusion = [[0 for _ in range(N_ACTIONS)] for _ in range(N_ACTIONS)]

    for episode in episodes:
        hear_events(brain, episode)
        answer = int(
            np.asarray(brain.act(query_vector(episode), greedy=True)).reshape(-1)[0]
        )
        answer = max(0, min(N_ACTIONS - 1, answer))

        correct = int(answer == episode.label)
        hits += correct
        pos_hits[episode.query_position] += correct
        pos_counts[episode.query_position] += 1
        resource_hits[episode.label] += correct
        resource_counts[episode.label] += 1
        confusion[episode.label][answer] += 1

    per_position = {
        QUERY_NAMES[i]: pos_hits[i] / pos_counts[i]
        for i in range(STREAM_LENGTH)
    }
    nonlast_hits = sum(pos_hits[:-1])
    nonlast_count = sum(pos_counts[:-1])

    return {
        "accuracy": hits / len(episodes),
        "nonlast": nonlast_hits / nonlast_count,
        "last": per_position["P5"],
        "per_position": per_position,
        "tests": {
            "total": len(episodes),
            **{QUERY_NAMES[i]: pos_counts[i] for i in range(STREAM_LENGTH)},
        },
        "per_resource": {
            EVENTS[i]: resource_hits[i] / resource_counts[i]
            if resource_counts[i] else 0.0
            for i in range(N_ACTIONS)
        },
        "resource_counts": {
            EVENTS[i]: resource_counts[i] for i in range(N_ACTIONS)
        },
        "confusion": confusion,
    }


def run_arm(
    founder: int,
    arm: str,
    train_episodes: list[Episode],
    test_episodes: list[Episode],
) -> dict[str, Any]:
    brain = compose(founder, arm)
    runtime_errors: list[str] = []
    training_reports = {
        "lessons": 0,
        "accepted_sum": 0.0,
        "agreed_sum": 0.0,
        "position_rows_sum": 0.0,
        "position_refused_sum": 0.0,
    }

    for episode in train_episodes:
        try:
            report = teach_query(brain, episode)
            training_reports["lessons"] += 1
            for key, out_key in (
                ("accepted", "accepted_sum"),
                ("agreed", "agreed_sum"),
                ("position_rows", "position_rows_sum"),
                ("position_refused", "position_refused_sum"),
            ):
                if key in report:
                    try:
                        training_reports[out_key] += float(report[key])
                    except (TypeError, ValueError):
                        pass
        except Exception as exc:
            runtime_errors.append(f"{type(exc).__name__}: {exc}")
            break

    moved = position_maps_moved(brain)
    test_result = None

    if not runtime_errors and training_reports["lessons"] == TRAIN_EPISODES:
        try:
            test_result = evaluate(brain, test_episodes)
        except Exception as exc:
            runtime_errors.append(f"{type(exc).__name__}: {exc}")

    valid = (
        not runtime_errors
        and training_reports["lessons"] == TRAIN_EPISODES
        and test_result is not None
        and test_result["tests"]["total"] == TEST_EPISODES
        and all(test_result["tests"][q] == TEST_EPISODES // 5 for q in QUERY_NAMES)
    )

    return {
        "arm": arm,
        "valid": int(valid),
        "training": training_reports,
        "position_maps_moved": int(moved),
        "test": test_result,
        "runtime_errors": runtime_errors,
    }


def run_founder(founder: int) -> dict[str, Any]:
    train_episodes = make_episodes(founder, phase=1, count=TRAIN_EPISODES)
    test_episodes = make_episodes(founder, phase=2, count=TEST_EPISODES)

    assert all(
        ep.query_position == STREAM_LENGTH - 1
        or ep.events[ep.query_position] != ep.events[-1]
        for ep in train_episodes + test_episodes
    )

    arms = {
        arm: run_arm(founder, arm, train_episodes, test_episodes)
        for arm in ARMS
    }
    valid = all(arms[arm]["valid"] for arm in ARMS)

    return {"founder": founder, "valid": int(valid), "arms": arms}


def classify(founders: list[dict[str, Any]]) -> dict[str, Any]:
    valid = [f for f in founders if f["valid"]]
    n = len(valid)

    def vals(arm: str, metric: str) -> list[float]:
        return [float(f["arms"][arm]["test"][metric]) for f in valid]

    def pos_vals(arm: str, pos: str) -> list[float]:
        return [
            float(f["arms"][arm]["test"]["per_position"][pos])
            for f in valid
        ]

    summary: dict[str, Any] = {
        "founders": len(founders),
        "valid_founders": n,
        "chance": UNIFORM_CHANCE,
    }

    for arm in ARMS:
        for metric in ("accuracy", "nonlast", "last"):
            xs = vals(arm, metric)
            summary[f"median_{arm.lower()}_{metric}"] = median(xs)
            summary[f"mean_{arm.lower()}_{metric}"] = sum(xs) / len(xs) if xs else 0.0
        for pos in QUERY_NAMES:
            xs = pos_vals(arm, pos)
            summary[f"median_{arm.lower()}_{pos.lower()}"] = median(xs)
            summary[f"mean_{arm.lower()}_{pos.lower()}"] = sum(xs) / len(xs) if xs else 0.0

    pos32 = vals("POSITION32", "accuracy")
    pos0 = vals("POSITION0", "accuracy")
    off = vals("RECALL_OFF", "accuracy")
    gain_pos0 = [a - b for a, b in zip(pos32, pos0)]
    gain_off = [a - b for a, b in zip(pos32, off)]

    summary["median_position32_minus_position0"] = median(gain_pos0)
    summary["median_position32_minus_recall_off"] = median(gain_off)

    robust_founders = sum(
        min(f["arms"]["POSITION32"]["test"]["per_position"].values()) >= 0.70
        for f in valid
    )
    maps_moved_founders = sum(
        bool(f["arms"]["POSITION32"]["position_maps_moved"])
        for f in valid
    )
    paired_win_founders = sum((a - b) >= 0.15 for a, b in zip(pos32, pos0))

    position_medians = [
        summary[f"median_position32_{pos.lower()}"] for pos in QUERY_NAMES
    ]

    performance_pass = (
        summary["median_position32_accuracy"] >= 0.85
        and min(position_medians) >= 0.75
        and robust_founders >= MIN_VALID
    )
    maps_pass = maps_moved_founders >= MIN_VALID
    paired_pass = (
        summary["median_position32_minus_position0"] >= 0.20
        and summary["median_position32_minus_recall_off"] >= 0.20
        and paired_win_founders >= MIN_VALID
    )
    full_pass = n >= MIN_VALID and performance_pass and maps_pass and paired_pass

    if n < MIN_VALID:
        diagnosis = "INSUFFICIENT_V7_17_RUNS"
    elif not maps_pass:
        diagnosis = "POSITION_TERM_NOT_TAUGHT"
    elif full_pass:
        diagnosis = "FIVE_POSITION_TEMPORAL_ADDRESSING_BRIDGE_PASS"
    elif performance_pass and not paired_pass:
        diagnosis = "FIVE_POSITION_TASK_SOLVED_WITHOUT_POSITION_ADVANTAGE"
    elif not performance_pass:
        diagnosis = "FIVE_POSITION_RECALL_ACQUISITION_BOTTLENECK"
    else:
        diagnosis = "PARTIAL_FIVE_POSITION_RECALL_SIGNAL"

    return {
        "valid": valid,
        "summary": summary,
        "robust_position32_founders": robust_founders,
        "position_maps_moved_founders": maps_moved_founders,
        "paired_position32_win_founders": paired_win_founders,
        "performance_pass": performance_pass,
        "maps_pass": maps_pass,
        "paired_pass": paired_pass,
        "full_pass": full_pass,
        "diagnosis": diagnosis,
    }


def flatten(founder: dict[str, Any]) -> dict[str, Any]:
    row: dict[str, Any] = {"founder": founder["founder"], "valid": founder["valid"]}

    for arm in ARMS:
        r = founder["arms"][arm]
        prefix = arm.lower()
        row[f"{prefix}_valid"] = r["valid"]
        row[f"{prefix}_position_maps_moved"] = r["position_maps_moved"]
        if r["test"] is not None:
            row[f"{prefix}_accuracy"] = r["test"]["accuracy"]
            row[f"{prefix}_nonlast"] = r["test"]["nonlast"]
            row[f"{prefix}_last"] = r["test"]["last"]
            for pos, value in r["test"]["per_position"].items():
                row[f"{prefix}_{pos.lower()}"] = value
            for resource, value in r["test"]["per_resource"].items():
                row[f"{prefix}_{resource.lower()}_accuracy"] = value

    if founder["valid"]:
        row["position32_minus_position0"] = (
            founder["arms"]["POSITION32"]["test"]["accuracy"]
            - founder["arms"]["POSITION0"]["test"]["accuracy"]
        )
        row["position32_minus_recall_off"] = (
            founder["arms"]["POSITION32"]["test"]["accuracy"]
            - founder["arms"]["RECALL_OFF"]["test"]["accuracy"]
        )

    return row


def write_outputs(out: Path, founders: list[dict[str, Any]]) -> str:
    result = classify(founders)
    summary = result["summary"]
    valid = result["valid"]

    body = {
        "experiment": "Cadence Stone Age V7.17 Five-Position Temporal Addressing",
        "cadence_net_version": VERSION,
        "scope": "bounded full-position temporal recall component test",
        "protocol": {
            "founder_start": FOUNDER_START,
            "founders": len(founders),
            "events": list(EVENTS),
            "actions": list(ACTIONS),
            "stream_length": STREAM_LENGTH,
            "query_positions": list(QUERY_NAMES),
            "nonlast_target_differs_from_final_event": True,
            "no_adjacent_duplicate_events": True,
            "inputs": INPUTS,
            "actions_count": N_ACTIONS,
            "training_episodes": TRAIN_EPISODES,
            "test_episodes": TEST_EPISODES,
            "exact_position_balance": True,
            "arms": list(ARMS),
            "position32": {
                "recall": True,
                "recall_position": 32,
                "recall_recency": 0.0,
                "recall_temperature": 0.25,
            },
            "position0": {
                "recall": True,
                "recall_position": 0,
                "recall_recency": 0.0,
                "recall_temperature": 0.25,
            },
            "recall_off": {
                "recall": False,
                "default_working_trace_retained": True,
            },
            "modules": [24],
            "episodic": False,
            "teaching": "normalized",
            "lesson_before_query_act": True,
            "chance": UNIFORM_CHANCE,
            "gates": {
                "minimum_valid": MIN_VALID,
                "position32_median_overall": 0.85,
                "position32_each_position_median": 0.75,
                "founder_all_positions": 0.70,
                "robust_founders": MIN_VALID,
                "position_maps_moved_founders": MIN_VALID,
                "median_gain_vs_position0": 0.20,
                "founder_gain_vs_position0": 0.15,
                "paired_win_founders": MIN_VALID,
                "median_gain_vs_recall_off": 0.20,
            },
            "attention": False,
            "episodic_memory": False,
            "reward_learning": False,
            "full_game": False,
        },
        "summary": summary,
        "robust_position32_founders": result["robust_position32_founders"],
        "position_maps_moved_founders": result["position_maps_moved_founders"],
        "paired_position32_win_founders": result["paired_position32_win_founders"],
        "performance_pass": result["performance_pass"],
        "maps_pass": result["maps_pass"],
        "paired_pass": result["paired_pass"],
        "full_pass": result["full_pass"],
        "diagnosis": result["diagnosis"],
        "founders": founders,
    }

    (out / "STONE_AGE_V7_17_RESULTS.json").write_text(
        json.dumps(body, indent=2), encoding="utf-8"
    )

    rows = [flatten(f) for f in founders]
    fields = sorted({k for row in rows for k in row})
    with (out / "STONE_AGE_V7_17_PER_FOUNDER.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    with (out / "STONE_AGE_V7_17_SUMMARY.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        for key, value in summary.items():
            writer.writerow([key, value])
        for key in (
            "robust_position32_founders",
            "position_maps_moved_founders",
            "paired_position32_win_founders",
            "performance_pass",
            "maps_pass",
            "paired_pass",
            "full_pass",
            "diagnosis",
        ):
            writer.writerow([key, result[key]])

    lines = [
        "CADENCE STONE AGE V7.17 — FIVE-POSITION TEMPORAL ADDRESSING",
        "=" * 118,
        f"cadence-net: {VERSION}",
        f"fresh founders: {FOUNDER_START}..{FOUNDER_START + len(founders) - 1}",
        "",
        f"VALID FOUNDERS: {len(valid)}/{len(founders)} (minimum {MIN_VALID})",
        "",
        "TASK",
        "Five resource events -> one of five position-only queries P1..P5.",
        "The query contains no resource identity.",
        "For P1..P4, target != final event to block the simplest working-trace shortcut.",
        "",
        "MEDIAN HELD-OUT ACCURACY",
    ]

    for arm in ARMS:
        parts = [
            f"{arm:<12} overall {summary[f'median_{arm.lower()}_accuracy']:.1%}",
            f"nonlast {summary[f'median_{arm.lower()}_nonlast']:.1%}",
            f"P5 {summary[f'median_{arm.lower()}_last']:.1%}",
        ]
        lines.append("  " + " | ".join(parts))
        lines.append(
            "    " + " | ".join(
                f"{pos} {summary[f'median_{arm.lower()}_{pos.lower()}']:.1%}"
                for pos in QUERY_NAMES
            )
        )

    lines += [
        "",
        "PAIRED POSITION32 ADVANTAGE",
        f"  median vs POSITION0: {summary['median_position32_minus_position0']:+.1%}",
        f"  median vs RECALL_OFF: {summary['median_position32_minus_recall_off']:+.1%}",
        (
            "  founders beating POSITION0 by >=15 points: "
            f"{result['paired_position32_win_founders']}/{len(valid)}"
        ),
        "",
        "POSITION EVIDENCE",
        (
            "  POSITION32 founders with every P1..P5 >=70%: "
            f"{result['robust_position32_founders']}/{len(valid)}"
        ),
        (
            "  POSITION32 founders whose position maps moved: "
            f"{result['position_maps_moved_founders']}/{len(valid)}"
        ),
        "",
        "FROZEN GATES",
        f"- valid >= {MIN_VALID}: {len(valid) >= MIN_VALID}",
        (
            "- POSITION32 median overall >=85%: "
            f"{summary['median_position32_accuracy'] >= .85}"
        ),
        (
            "- POSITION32 every position median >=75%: "
            f"{min(summary[f'median_position32_{p.lower()}'] for p in QUERY_NAMES) >= .75}"
        ),
        (
            f"- >={MIN_VALID} founders all positions >=70%: "
            f"{result['robust_position32_founders'] >= MIN_VALID}"
        ),
        (
            f"- position maps moved >={MIN_VALID} founders: "
            f"{result['position_maps_moved_founders'] >= MIN_VALID}"
        ),
        (
            "- median POSITION32-POSITION0 >=20 points: "
            f"{summary['median_position32_minus_position0'] >= .20}"
        ),
        (
            f"- >={MIN_VALID} founders gain >=15 points vs POSITION0: "
            f"{result['paired_position32_win_founders'] >= MIN_VALID}"
        ),
        (
            "- median POSITION32-RECALL_OFF >=20 points: "
            f"{summary['median_position32_minus_recall_off'] >= .20}"
        ),
        "",
        "FROZEN CLASSIFICATION",
        "- valid <6 -> INSUFFICIENT_V7_17_RUNS",
        "- maps fail -> POSITION_TERM_NOT_TAUGHT",
        "- all gates pass -> FIVE_POSITION_TEMPORAL_ADDRESSING_BRIDGE_PASS",
        "- POSITION32 solves without paired advantage -> FIVE_POSITION_TASK_SOLVED_WITHOUT_POSITION_ADVANTAGE",
        "- POSITION32 performance gates fail -> FIVE_POSITION_RECALL_ACQUISITION_BOTTLENECK",
        "- otherwise -> PARTIAL_FIVE_POSITION_RECALL_SIGNAL",
        "",
        f"DIAGNOSTIC CLASSIFICATION: {result['diagnosis']}",
        "",
        "BOUNDARIES",
        "1. Bounded five-event component test; not full-game integration.",
        "2. Query contains temporal position only; no resource identity.",
        "3. P1..P4 target is forced different from the final event.",
        "4. Query positions are exactly balanced in train and held-out test.",
        "5. Recall recency is disabled.",
        "6. RECALL_OFF retains the default working trace.",
        "7. No episodic memory, attention, or reward learning.",
        "8. No post-hoc gate changes.",
    ]

    report = "\n".join(lines) + "\n"
    (out / "STONE_AGE_V7_17_REPORT.txt").write_text(report, encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="stone_age_v7_17_output")
    parser.add_argument("--founders", type=int, default=DEFAULT_FOUNDERS)
    args = parser.parse_args()

    installed = pkg_version("cadence-net")
    if installed != VERSION:
        raise RuntimeError(f"expected cadence-net {VERSION}, got {installed}")

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    print("=" * 120)
    print(" CADENCE STONE AGE V7.17 — FIVE-POSITION TEMPORAL ADDRESSING")
    print("=" * 120)
    print(f"cadence-net: {VERSION}")
    print(f"fresh founders: {FOUNDER_START}..{FOUNDER_START + args.founders - 1}")
    print("arms: POSITION32 / POSITION0 / RECALL_OFF")
    print("task: five resource events, then P1/P2/P3/P4/P5 query")
    print()

    founders: list[dict[str, Any]] = []
    for founder in range(FOUNDER_START, FOUNDER_START + args.founders):
        print(f"FOUNDER {founder}", flush=True)
        result = run_founder(founder)
        founders.append(result)

        for arm in ARMS:
            r = result["arms"][arm]
            if r["test"] is None:
                print(f"  {arm:<12} INVALID {r['runtime_errors']}")
            else:
                perpos = " ".join(
                    f"{p}={r['test']['per_position'][p]:.1%}" for p in QUERY_NAMES
                )
                print(
                    f"  {arm:<12} overall={r['test']['accuracy']:.1%} "
                    f"nonlast={r['test']['nonlast']:.1%} {perpos} "
                    f"maps={r['position_maps_moved']}"
                )
        print()

    report = write_outputs(out, founders)
    print(report)


if __name__ == "__main__":
    main()

