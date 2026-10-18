\
"""
CADENCE AGENCY DOOR V2B — COUNTERBALANCED REACQUISITION

Purpose
-------
V2 found strongly negative behavioral savings in PRESS -> PULL -> PRESS, but
fresh Cadence founders also learned PRESS unusually quickly. V2B removes that
action-order confound by giving the SAME founder seed two mirrored lives:

    PPP: PRESS -> PULL -> PRESS
    QPQ: PULL  -> PRESS -> PULL

Each phase lasts 120 trials. No phase/reversal/world flag enters the observation.

Cadence
-------
cadence-net==0.84.0
Brain.compose(inputs=3, actions=3, modules=(16,), arousal=True, recall=False)
No teacher. Every other gene remains at the released founder default.

Fresh seeds
-----------
24001..24050. These are frozen before the run.

Primary endpoint
----------------
For every base seed:

    PRESS savings = PPP.return_early20 - PPP.initial_early20
    PULL savings  = QPQ.return_early20 - QPQ.initial_early20
    counterbalanced savings = (PRESS savings + PULL savings) / 2

The primary test is an exact two-sided sign test of counterbalanced savings
against zero across non-tied seeds.

Interpretation boundary
-----------------------
Positive savings supports faster behavioral reacquisition when an old
contingency returns. Negative savings supports interference/no behavioral
savings under this protocol. Neither result identifies a specific memory
mechanism or establishes an explicit causal world model.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from importlib.metadata import version as pkg_version
from pathlib import Path

import numpy as np
from cadence import Brain

ACTIONS = ("PRESS", "PULL", "WAIT")
PRESS, PULL, WAIT = 0, 1, 2

PHASE_TRIALS = 120
TOTAL_TRIALS = 360
EARLY = 20
LATE = 40

BASE_SEED_START = 24001
DEFAULT_SEEDS = 50
YOKED_SEED_OFFSET = 500_000
NAIVE_SEED_OFFSET = 900_000

TABULAR_ALPHA = 0.20
TABULAR_EPSILON = 0.20

PPP = (PRESS, PULL, PRESS)
QPQ = (PULL, PRESS, PULL)


def mean(xs):
    return statistics.fmean(xs) if xs else 0.0


def exact_two_sided_sign_p(wins: int, losses: int) -> float:
    n = wins + losses
    if n == 0:
        return 1.0
    k = min(wins, losses)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / (2 ** n)
    return min(1.0, 2.0 * tail)


def paired_counts(a, b):
    if len(a) != len(b):
        raise ValueError("paired vectors differ in length")
    wins = sum(x > y for x, y in zip(a, b))
    losses = sum(y > x for x, y in zip(a, b))
    ties = sum(x == y for x, y in zip(a, b))
    return {
        "wins": wins,
        "losses": losses,
        "ties": ties,
        "mean_difference": mean([x - y for x, y in zip(a, b)]),
        "p": exact_two_sided_sign_p(wins, losses),
    }


def observation(previous_open: bool | None) -> np.ndarray:
    if previous_open is None:
        return np.asarray([[1.0, 0.0, 0.0]], dtype=np.float64)
    return np.asarray(
        [[1.0, float(previous_open), float(not previous_open)]],
        dtype=np.float64,
    )


def phase_index(trial: int) -> int:
    return trial % PHASE_TRIALS


def phase_number(trial: int) -> int:
    return trial // PHASE_TRIALS


def target_for(trial: int, schedule: tuple[int, int, int]) -> int:
    return schedule[phase_number(trial)]


def phase_label(trial: int, name: str) -> str:
    return f"{name}_P{phase_number(trial) + 1}"


def window_label(trial: int, name: str) -> str:
    idx = phase_index(trial)
    phase = phase_number(trial) + 1
    if idx < EARLY:
        return f"{name}_P{phase}_early20"
    if idx >= PHASE_TRIALS - LATE:
        return f"{name}_P{phase}_late40"
    return f"{name}_P{phase}_middle"


def new_brain(seed: int) -> Brain:
    return Brain.compose(
        inputs=3,
        actions=3,
        modules=(16,),
        seed=int(seed),
        arousal=True,
        recall=False,
    )


def run_cadence_schedule(base_seed: int, brain_seed: int, schedule, name: str, arm: str):
    brain = new_brain(brain_seed)
    previous_open = None
    action = int(brain.live(observation(previous_open))[0])
    first_action = action
    rows, opens, rewards = [], [], []

    for trial in range(TOTAL_TRIALS):
        target = target_for(trial, schedule)
        opened = int(action) == target
        reward = float(opened)

        rows.append({
            "base_seed": base_seed,
            "brain_seed": brain_seed,
            "arm": arm,
            "schedule": name,
            "trial": trial + 1,
            "phase": phase_label(trial, name),
            "phase_index": phase_index(trial) + 1,
            "window": window_label(trial, name),
            "action": action,
            "action_name": ACTIONS[action],
            "target_action": target,
            "target_action_name": ACTIONS[target],
            "phase_correct_action": int(action == target),
            "opened": int(opened),
            "reward": reward,
        })
        opens.append(bool(opened))
        rewards.append(reward)
        previous_open = bool(opened)
        action = int(brain.live(
            observation(previous_open),
            reward=np.asarray([reward], dtype=np.float64),
        )[0])

    return {
        "rows": rows,
        "opens": opens,
        "rewards": rewards,
        "first_action": first_action,
        "genes": dict(brain.describe().get("genes", {})),
    }


def run_cadence_yoked(base_seed: int, brain_seed: int, master_opens, schedule, name: str):
    brain = new_brain(brain_seed)
    previous_open = None
    action = int(brain.live(observation(previous_open))[0])
    rows, opens, rewards = [], [], []

    for trial in range(TOTAL_TRIALS):
        target = target_for(trial, schedule)
        opened = bool(master_opens[trial])
        reward = float(opened)
        rows.append({
            "base_seed": base_seed,
            "brain_seed": brain_seed,
            "arm": "YOKED",
            "schedule": name,
            "trial": trial + 1,
            "phase": phase_label(trial, name),
            "phase_index": phase_index(trial) + 1,
            "window": window_label(trial, name),
            "action": action,
            "action_name": ACTIONS[action],
            "target_action": target,
            "target_action_name": ACTIONS[target],
            "phase_correct_action": int(action == target),
            "opened": int(opened),
            "reward": reward,
        })
        opens.append(opened)
        rewards.append(reward)
        previous_open = opened
        action = int(brain.live(
            observation(previous_open),
            reward=np.asarray([reward], dtype=np.float64),
        )[0])

    if opens != list(master_opens):
        raise RuntimeError(f"{name} yoked outcome timeline mismatch")
    return {"rows": rows, "opens": opens, "rewards": rewards}


def run_naive(base_seed: int, target: int):
    # PRESS and PULL naive controls intentionally use the same founder seed in
    # separate brains, counterbalancing founder preference across target actions.
    brain_seed = base_seed + NAIVE_SEED_OFFSET
    brain = new_brain(brain_seed)
    previous_open = None
    action = int(brain.live(observation(previous_open))[0])
    rows = []

    name = f"NAIVE_{ACTIONS[target]}"
    for trial in range(PHASE_TRIALS):
        opened = int(action) == target
        reward = float(opened)
        window = (
            f"{name}_early20" if trial < EARLY else
            f"{name}_late40" if trial >= PHASE_TRIALS - LATE else
            f"{name}_middle"
        )
        rows.append({
            "base_seed": base_seed,
            "brain_seed": brain_seed,
            "arm": "NAIVE",
            "schedule": name,
            "trial": trial + 1,
            "phase": name,
            "phase_index": trial + 1,
            "window": window,
            "action": action,
            "action_name": ACTIONS[action],
            "target_action": target,
            "target_action_name": ACTIONS[target],
            "phase_correct_action": int(action == target),
            "opened": int(opened),
            "reward": reward,
        })
        previous_open = bool(opened)
        action = int(brain.live(
            observation(previous_open),
            reward=np.asarray([reward], dtype=np.float64),
        )[0])
    return rows


def run_random_schedule(seed: int, schedule, name: str):
    rng = np.random.default_rng(seed + 3_000_000)
    rows = []
    for trial in range(TOTAL_TRIALS):
        action = int(rng.integers(3))
        target = target_for(trial, schedule)
        rows.append({
            "trial": trial + 1,
            "window": window_label(trial, name),
            "phase_correct_action": int(action == target),
            "reward": float(action == target),
        })
    return rows


def run_tabular_schedule(seed: int, schedule, name: str):
    rng = np.random.default_rng(seed + 4_000_000)
    q = np.zeros(3, dtype=float)
    rows = []
    for trial in range(TOTAL_TRIALS):
        if rng.random() < TABULAR_EPSILON:
            action = int(rng.integers(3))
        else:
            best = np.flatnonzero(q == q.max())
            action = int(rng.choice(best))
        target = target_for(trial, schedule)
        reward = float(action == target)
        q[action] += TABULAR_ALPHA * (reward - q[action])
        rows.append({
            "trial": trial + 1,
            "window": window_label(trial, name),
            "phase_correct_action": int(action == target),
            "reward": reward,
        })
    return rows


def rate(rows, window: str) -> float:
    rr = [r for r in rows if r["window"] == window]
    if not rr:
        raise RuntimeError(f"window not found: {window}")
    return mean([r["phase_correct_action"] for r in rr])


def write_csv(path: Path, rows: list[dict]):
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-start", type=int, default=BASE_SEED_START)
    parser.add_argument("--seeds", type=int, default=DEFAULT_SEEDS)
    parser.add_argument("--output", default="agency_door_v2b_output")
    args = parser.parse_args()

    version = pkg_version("cadence-net")
    if version != "0.84.0":
        raise RuntimeError(f"V2B requires cadence-net==0.84.0; found {version}")

    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)

    print("=" * 96)
    print(" CADENCE AGENCY DOOR V2B — COUNTERBALANCED REACQUISITION")
    print("=" * 96)
    print("cadence-net:", version)
    print("fresh base seeds:", f"{args.seed_start}..{args.seed_start + args.seeds - 1}")
    print("Mirror 1: PRESS -> PULL -> PRESS")
    print("Mirror 2: PULL  -> PRESS -> PULL")
    print("Same founder seed is used for both mirrored controllable lives.")
    print("PRIMARY: seed-level counterbalanced savings, exact two-sided sign test vs zero")
    print("")

    all_rows = []
    per_seed = []
    first_genes = None
    first_action_counts = {name: 0 for name in ACTIONS}

    for base_seed in range(args.seed_start, args.seed_start + args.seeds):
        ppp = run_cadence_schedule(base_seed, base_seed, PPP, "PPP", "CONTROLLABLE")
        qpq = run_cadence_schedule(base_seed, base_seed, QPQ, "QPQ", "CONTROLLABLE")

        # Because the mirrored controllable arms start from the same founder and
        # identical first observation, their first free action should match.
        if ppp["first_action"] != qpq["first_action"]:
            raise RuntimeError("mirrored same-founder first actions unexpectedly differ")
        first_action_counts[ACTIONS[ppp["first_action"]]] += 1

        yoked_seed = base_seed + YOKED_SEED_OFFSET
        y_ppp = run_cadence_yoked(base_seed, yoked_seed, ppp["opens"], PPP, "PPP")
        y_qpq = run_cadence_yoked(base_seed, yoked_seed, qpq["opens"], QPQ, "QPQ")

        naive_press = run_naive(base_seed, PRESS)
        naive_pull = run_naive(base_seed, PULL)

        rand_ppp = run_random_schedule(base_seed, PPP, "PPP")
        rand_qpq = run_random_schedule(base_seed, QPQ, "QPQ")
        tab_ppp = run_tabular_schedule(base_seed, PPP, "PPP")
        tab_qpq = run_tabular_schedule(base_seed, QPQ, "QPQ")

        if first_genes is None:
            first_genes = ppp["genes"]

        ppp_initial = rate(ppp["rows"], "PPP_P1_early20")
        ppp_return = rate(ppp["rows"], "PPP_P3_early20")
        qpq_initial = rate(qpq["rows"], "QPQ_P1_early20")
        qpq_return = rate(qpq["rows"], "QPQ_P3_early20")

        press_savings = ppp_return - ppp_initial
        pull_savings = qpq_return - qpq_initial
        counterbalanced_savings = 0.5 * (press_savings + pull_savings)

        naive_press_e = rate(naive_press, "NAIVE_PRESS_early20")
        naive_pull_e = rate(naive_pull, "NAIVE_PULL_early20")
        return_mean = 0.5 * (ppp_return + qpq_return)
        naive_mean = 0.5 * (naive_press_e + naive_pull_e)

        cont_return_late = 0.5 * (
            rate(ppp["rows"], "PPP_P3_late40") +
            rate(qpq["rows"], "QPQ_P3_late40")
        )
        yoked_return_late = 0.5 * (
            rate(y_ppp["rows"], "PPP_P3_late40") +
            rate(y_qpq["rows"], "QPQ_P3_late40")
        )

        tab_press_savings = rate(tab_ppp, "PPP_P3_early20") - rate(tab_ppp, "PPP_P1_early20")
        tab_pull_savings = rate(tab_qpq, "QPQ_P3_early20") - rate(tab_qpq, "QPQ_P1_early20")
        tab_counterbalanced = 0.5 * (tab_press_savings + tab_pull_savings)

        rand_press_savings = rate(rand_ppp, "PPP_P3_early20") - rate(rand_ppp, "PPP_P1_early20")
        rand_pull_savings = rate(rand_qpq, "QPQ_P3_early20") - rate(rand_qpq, "QPQ_P1_early20")
        rand_counterbalanced = 0.5 * (rand_press_savings + rand_pull_savings)

        item = {
            "base_seed": base_seed,
            "first_action": ACTIONS[ppp["first_action"]],
            "ppp_initial_early20": ppp_initial,
            "ppp_return_early20": ppp_return,
            "ppp_press_savings": press_savings,
            "qpq_initial_early20": qpq_initial,
            "qpq_return_early20": qpq_return,
            "qpq_pull_savings": pull_savings,
            "counterbalanced_savings": counterbalanced_savings,
            "naive_press_early20": naive_press_e,
            "naive_pull_early20": naive_pull_e,
            "return_mean_early20": return_mean,
            "naive_mean_early20": naive_mean,
            "controllable_return_late40": cont_return_late,
            "yoked_return_late40": yoked_return_late,
            "tabular_counterbalanced_savings": tab_counterbalanced,
            "random_counterbalanced_savings": rand_counterbalanced,
            "ppp_phase2_early20": rate(ppp["rows"], "PPP_P2_early20"),
            "qpq_phase2_early20": rate(qpq["rows"], "QPQ_P2_early20"),
            "ppp_phase1_late40": rate(ppp["rows"], "PPP_P1_late40"),
            "ppp_phase2_late40": rate(ppp["rows"], "PPP_P2_late40"),
            "ppp_phase3_late40": rate(ppp["rows"], "PPP_P3_late40"),
            "qpq_phase1_late40": rate(qpq["rows"], "QPQ_P1_late40"),
            "qpq_phase2_late40": rate(qpq["rows"], "QPQ_P2_late40"),
            "qpq_phase3_late40": rate(qpq["rows"], "QPQ_P3_late40"),
        }
        per_seed.append(item)

        all_rows.extend(ppp["rows"])
        all_rows.extend(qpq["rows"])
        all_rows.extend(y_ppp["rows"])
        all_rows.extend(y_qpq["rows"])
        all_rows.extend(naive_press)
        all_rows.extend(naive_pull)

        print(
            f"{base_seed}: first={item['first_action']:<5} | "
            f"PRESS save={press_savings*100:+6.1f} pp | "
            f"PULL save={pull_savings*100:+6.1f} pp | "
            f"CB={counterbalanced_savings*100:+6.1f} pp | "
            f"return-vs-naive={(return_mean-naive_mean)*100:+6.1f} pp"
        )

    cb = [r["counterbalanced_savings"] for r in per_seed]
    zero = [0.0] * len(cb)
    primary = paired_counts(cb, zero)

    returned = [r["return_mean_early20"] for r in per_seed]
    naive = [r["naive_mean_early20"] for r in per_seed]
    secondary_naive = paired_counts(returned, naive)

    cont_late = [r["controllable_return_late40"] for r in per_seed]
    yoked_late = [r["yoked_return_late40"] for r in per_seed]
    secondary_yoked = paired_counts(cont_late, yoked_late)

    press_return = [r["ppp_return_early20"] for r in per_seed]
    press_initial = [r["ppp_initial_early20"] for r in per_seed]
    pull_return = [r["qpq_return_early20"] for r in per_seed]
    pull_initial = [r["qpq_initial_early20"] for r in per_seed]
    press_test = paired_counts(press_return, press_initial)
    pull_test = paired_counts(pull_return, pull_initial)

    tab_cb = [r["tabular_counterbalanced_savings"] for r in per_seed]
    rand_cb = [r["random_counterbalanced_savings"] for r in per_seed]

    aggregate = {
        "ppp_initial_early20": mean(press_initial),
        "ppp_return_early20": mean(press_return),
        "qpq_initial_early20": mean(pull_initial),
        "qpq_return_early20": mean(pull_return),
        "counterbalanced_savings": mean(cb),
        "returned_mean_early20": mean(returned),
        "naive_mean_early20": mean(naive),
        "controllable_return_late40": mean(cont_late),
        "yoked_return_late40": mean(yoked_late),
        "tabular_counterbalanced_savings": mean(tab_cb),
        "random_counterbalanced_savings": mean(rand_cb),
        "ppp_phase2_early20": mean([r["ppp_phase2_early20"] for r in per_seed]),
        "qpq_phase2_early20": mean([r["qpq_phase2_early20"] for r in per_seed]),
        "ppp_phase1_late40": mean([r["ppp_phase1_late40"] for r in per_seed]),
        "ppp_phase2_late40": mean([r["ppp_phase2_late40"] for r in per_seed]),
        "ppp_phase3_late40": mean([r["ppp_phase3_late40"] for r in per_seed]),
        "qpq_phase1_late40": mean([r["qpq_phase1_late40"] for r in per_seed]),
        "qpq_phase2_late40": mean([r["qpq_phase2_late40"] for r in per_seed]),
        "qpq_phase3_late40": mean([r["qpq_phase3_late40"] for r in per_seed]),
    }

    payload = {
        "experiment": "Cadence Agency Door V2B",
        "cadence_net_version": version,
        "fresh_base_seeds": [args.seed_start, args.seed_start + args.seeds - 1],
        "protocol": {
            "mirror_1": "PRESS -> PULL -> PRESS",
            "mirror_2": "PULL -> PRESS -> PULL",
            "phase_trials": PHASE_TRIALS,
            "early_window": EARLY,
            "late_window": LATE,
            "same_founder_for_mirrors": True,
            "cadence": {
                "inputs": 3,
                "actions": 3,
                "modules": [16],
                "arousal": True,
                "recall": False,
                "teacher": False,
                "other_genes": "released founder defaults",
            },
        },
        "first_founder_genes": first_genes,
        "first_action_counts": first_action_counts,
        "aggregate": aggregate,
        "tests": {
            "primary_counterbalanced_savings_vs_zero": primary,
            "secondary_return_early_vs_naive_early": secondary_naive,
            "secondary_return_late_vs_yoked_late": secondary_yoked,
            "descriptive_PRESS_savings": press_test,
            "descriptive_PULL_savings": pull_test,
        },
        "per_seed": per_seed,
    }

    write_csv(out / "AGENCY_DOOR_V2B_TRIALS.csv", all_rows)
    (out / "AGENCY_DOOR_V2B_RESULTS.json").write_text(
        json.dumps(payload, indent=2, default=str), encoding="utf-8"
    )

    report = []
    add = report.append
    add("CADENCE AGENCY DOOR V2B — COUNTERBALANCED REACQUISITION REPORT")
    add("=" * 96)
    add(f"cadence-net: {version}")
    add(f"fresh base seeds: {args.seed_start}..{args.seed_start + args.seeds - 1}")
    add("")
    add("FOUNDER FIRST-ACTION DISTRIBUTION")
    add(
        f"  PRESS={first_action_counts['PRESS']} | "
        f"PULL={first_action_counts['PULL']} | WAIT={first_action_counts['WAIT']}"
    )
    add("")
    add("EARLY20 MEANS")
    add(f"  PPP initial PRESS: {aggregate['ppp_initial_early20']*100:.1f}%")
    add(f"  PPP returned PRESS: {aggregate['ppp_return_early20']*100:.1f}%")
    add(f"  QPQ initial PULL:  {aggregate['qpq_initial_early20']*100:.1f}%")
    add(f"  QPQ returned PULL: {aggregate['qpq_return_early20']*100:.1f}%")
    add(f"  Returned action mean: {aggregate['returned_mean_early20']*100:.1f}%")
    add(f"  Fresh naive matched-action mean: {aggregate['naive_mean_early20']*100:.1f}%")
    add("")
    add("LATE40 CONTINGENCY CONTROL")
    add(f"  Controllable returned phase: {aggregate['controllable_return_late40']*100:.1f}%")
    add(f"  Yoked returned phase:        {aggregate['yoked_return_late40']*100:.1f}%")
    add("")
    add("PRE-REGISTERED V2B TESTS")
    add(
        "PRIMARY — counterbalanced savings vs zero: "
        f"positive={primary['wins']} | negative={primary['losses']} | ties={primary['ties']} | "
        f"mean savings={primary['mean_difference']*100:+.1f} pp | "
        f"exact two-sided sign p={primary['p']:.10g}"
    )
    add(
        "SECONDARY — returned early20 vs fresh naive matched-action early20: "
        f"return higher={secondary_naive['wins']} | naive higher={secondary_naive['losses']} | "
        f"ties={secondary_naive['ties']} | mean(return-naive)={secondary_naive['mean_difference']*100:+.1f} pp | "
        f"exact two-sided sign p={secondary_naive['p']:.10g}"
    )
    add(
        "SECONDARY — controllable returned late40 vs yoked returned late40: "
        f"C higher={secondary_yoked['wins']} | Y higher={secondary_yoked['losses']} | "
        f"ties={secondary_yoked['ties']} | mean(C-Y)={secondary_yoked['mean_difference']*100:+.1f} pp | "
        f"exact two-sided sign p={secondary_yoked['p']:.10g}"
    )
    add("")
    add("ACTION-SPECIFIC DESCRIPTIVES")
    add(
        "  PRESS savings (PPP): "
        f"return higher={press_test['wins']} | initial higher={press_test['losses']} | ties={press_test['ties']} | "
        f"mean={press_test['mean_difference']*100:+.1f} pp | p={press_test['p']:.10g}"
    )
    add(
        "  PULL savings (QPQ):  "
        f"return higher={pull_test['wins']} | initial higher={pull_test['losses']} | ties={pull_test['ties']} | "
        f"mean={pull_test['mean_difference']*100:+.1f} pp | p={pull_test['p']:.10g}"
    )
    add("")
    add("CONVENTIONAL CONTROLS — COUNTERBALANCED SAVINGS")
    add(f"  random mean:  {aggregate['random_counterbalanced_savings']*100:+.1f} pp")
    add(f"  tabular mean: {aggregate['tabular_counterbalanced_savings']*100:+.1f} pp")
    add("")
    add("INTERPRETATION BOUNDARY")
    add("1. Positive primary savings supports faster behavioral reacquisition after an intervening contingency.")
    add("2. Negative primary savings supports interference/no behavioral savings under this protocol.")
    add("3. Counterbalancing prevents PRESS/action-0 founder preference from deciding the primary result.")
    add("4. This does not identify an internal memory mechanism or prove explicit causal forecasting/counterfactual reasoning.")
    add("5. Seeds 24001..24050 are frozen; do not tune on them and reuse them as a new confirmation population.")

    text = "\n".join(report)
    (out / "AGENCY_DOOR_V2B_REPORT.txt").write_text(text, encoding="utf-8")
    print("")
    print(text)
    print("")
    print("Saved to:", out)


if __name__ == "__main__":
    main()
