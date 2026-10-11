
"""
CADENCE // STONE AGE V4.2
Balanced Lesson Budget Sweep — cadence-net 0.81.0

Question:
Does more backward-lesson drilling eventually damage the state-dependent policy?

Every budget:
- starts from the EXACT SAME founder checkpoint
- uses the same four observable one-step COLD lessons
- gives every lesson equal total exposure
- uses Brain.wait for delayed physical observations
- grades the action with reward; no target-action label is observed
- freezes immediately after lessons
- evaluates the full COLD chain
- records canonical state/action fingerprints

There is NO extra full-chain training in V4.2.
This isolates lesson budget as the independent variable.
"""

import argparse
import csv
import json
import random
import statistics
from collections import Counter
from importlib.metadata import version as pkg_version
from pathlib import Path

import numpy as np
from cadence import ActorCriticConfig, Brain

ACTIONS = [
    "GATHER_WOOD",
    "GATHER_STONE",
    "CRAFT_FIRE",
    "WARM_UP",
    "WAIT",
]

INPUTS = 10
OUTPUT_DIR = Path(__file__).resolve().parent / "benchmark_output_v4_2"

ACTOR_ETA = 0.03
ACTOR_ETA_BIAS = 0.003
ACTOR_GAMMA = 0.95
ACTOR_LAM = 0.60
ACTOR_ETA_CRITIC = 5.0

ACTION_DELAY_WAITS = 2
LESSON_REWARD_CORRECT = 1.0
LESSON_REWARD_WRONG = -0.25

MAX_DECISIONS = 8


def mean(values):
    return statistics.fmean(values) if values else 0.0


# ============================================================
# OBSERVATION / COLD WORLD
# ============================================================

def observation(
    *,
    wood,
    stone,
    fire,
    warmth,
    action_phase=0.0,
    decision_fraction=0.0,
):
    has_wood = 1.0 if wood >= 1 else 0.0
    has_stone = 1.0 if stone >= 1 else 0.0
    has_fire = 1.0 if fire else 0.0

    return np.asarray([[
        float(np.clip(warmth, 0.0, 1.0)),
        has_wood,
        has_stone,
        has_fire,
        min(1.0, wood / 2.0),
        min(1.0, stone / 2.0),
        float(np.clip(action_phase, 0.0, 1.0)),
        float(np.clip(decision_fraction, 0.0, 1.0)),
        1.0,  # cold-task cue
        1.0,  # bias/world cue
    ]], dtype=np.float64)


class ColdWorld:
    def __init__(self):
        self.reset()

    def reset(self):
        self.wood = 0
        self.stone = 0
        self.fire = False
        self.warmth = 0.48
        self.decisions = 0
        self.done = False
        self.success = False
        self.outcome = ""

    def obs(self, phase=0.0):
        return observation(
            wood=self.wood,
            stone=self.stone,
            fire=self.fire,
            warmth=self.warmth,
            action_phase=phase,
            decision_fraction=self.decisions / MAX_DECISIONS,
        )

    def mid_action_tick(self):
        self.warmth -= 0.015
        if self.fire:
            self.warmth += 0.006

    def apply_action(self, action_name):
        self.decisions += 1

        if action_name == "GATHER_WOOD":
            self.wood = min(2, self.wood + 1)

        elif action_name == "GATHER_STONE":
            self.stone = min(2, self.stone + 1)

        elif action_name == "CRAFT_FIRE":
            if self.wood >= 1 and self.stone >= 1:
                self.fire = True

        elif action_name == "WARM_UP":
            if self.fire:
                self.warmth += 0.52

        self.warmth -= 0.015
        if self.fire:
            self.warmth += 0.006

        self.warmth = min(1.0, self.warmth)

        if self.fire and self.warmth >= 0.75:
            self.done = True
            self.success = True
            self.outcome = "SUCCESS"

        elif self.warmth <= 0.0:
            self.done = True
            self.outcome = "HYPOTHERMIA"

        elif self.decisions >= MAX_DECISIONS:
            self.done = True
            self.outcome = "TIMEOUT"


# ============================================================
# BRAIN
# ============================================================

def new_brain(seed):
    reward_cfg = ActorCriticConfig(
        gamma=ACTOR_GAMMA,
        lam=ACTOR_LAM,
        eta=ACTOR_ETA,
        eta_bias=ACTOR_ETA_BIAS,
        eta_critic=ACTOR_ETA_CRITIC,
    )

    return Brain.compose(
        inputs=INPUTS,
        actions=len(ACTIONS),
        modules=(24, 12),
        seed=int(seed),
        arousal=True,
        reward=reward_cfg,
    )


def action_from(output):
    idx = int(np.asarray(output).reshape(-1)[0])
    idx = max(0, min(len(ACTIONS) - 1, idx))
    return idx, ACTIONS[idx]


def safe_reset(brain):
    brain.reset()


# ============================================================
# BALANCED BACKWARD LESSONS
# ============================================================

LESSONS = [
    {
        "name": "warm_up",
        "wood": 0,
        "stone": 0,
        "fire": True,
        "warmth": 0.42,
        "correct": "WARM_UP",
    },
    {
        "name": "craft_fire",
        "wood": 1,
        "stone": 1,
        "fire": False,
        "warmth": 0.42,
        "correct": "CRAFT_FIRE",
    },
    {
        "name": "gather_stone",
        "wood": 1,
        "stone": 0,
        "fire": False,
        "warmth": 0.42,
        "correct": "GATHER_STONE",
    },
    {
        "name": "gather_wood",
        "wood": 0,
        "stone": 0,
        "fire": False,
        "warmth": 0.42,
        "correct": "GATHER_WOOD",
    },
]


def lesson_obs(lesson, phase=0.0):
    return observation(
        wood=lesson["wood"],
        stone=lesson["stone"],
        fire=lesson["fire"],
        warmth=lesson["warmth"],
        action_phase=phase,
        decision_fraction=0.0,
    )


def post_lesson_state(lesson, chosen_action):
    wood = lesson["wood"]
    stone = lesson["stone"]
    fire = lesson["fire"]
    warmth = lesson["warmth"]

    if chosen_action == "GATHER_WOOD":
        wood = min(2, wood + 1)

    elif chosen_action == "GATHER_STONE":
        stone = min(2, stone + 1)

    elif chosen_action == "CRAFT_FIRE":
        if wood >= 1 and stone >= 1:
            fire = True

    elif chosen_action == "WARM_UP":
        if fire:
            warmth = min(1.0, warmth + 0.45)

    return observation(
        wood=wood,
        stone=stone,
        fire=fire,
        warmth=warmth,
        action_phase=1.0,
        decision_fraction=0.0,
    )


def balanced_schedule(total_trips, seed):
    """
    Equal total exposure per lesson.

    Approximately half of each lesson's exposures are isolated, introduced
    backwards; the rest are placed into one equally balanced interleaved pool.
    """
    if total_trips < len(LESSONS):
        raise ValueError("Budget must be >= number of lessons.")

    rng = random.Random(8200 + seed + total_trips)

    base = total_trips // len(LESSONS)
    remainder = total_trips % len(LESSONS)

    targets = {}

    for index, lesson in enumerate(LESSONS):
        targets[lesson["name"]] = base + (1 if index < remainder else 0)

    schedule = []
    isolated_counts = {}

    for lesson in LESSONS:
        target = targets[lesson["name"]]
        isolated = max(1, target // 2)
        isolated_counts[lesson["name"]] = isolated

        for _ in range(isolated):
            schedule.append((lesson, "isolated"))

    pool = []

    for lesson in LESSONS:
        remaining = targets[lesson["name"]] - isolated_counts[lesson["name"]]

        for _ in range(remaining):
            pool.append((lesson, "interleaved"))

    rng.shuffle(pool)
    schedule.extend(pool)

    return schedule


def train_lessons(brain, total_trips, seed):
    schedule = balanced_schedule(total_trips, seed)

    records = []

    first_lesson, first_stage = schedule[0]

    output = brain.live(
        lesson_obs(first_lesson)
    )

    _, action_name = action_from(output)
    owner = brain.decision_id

    for index, (lesson, schedule_stage) in enumerate(schedule):
        # Observation-only physical delay.
        brain.wait(
            lesson_obs(
                lesson,
                phase=0.5,
            )
        )

        brain.wait(
            post_lesson_state(
                lesson,
                action_name,
            )
        )

        correct = action_name == lesson["correct"]

        reward = (
            LESSON_REWARD_CORRECT
            if correct
            else LESSON_REWARD_WRONG
        )

        if index + 1 < len(schedule):
            next_lesson, next_stage = schedule[index + 1]
        else:
            next_lesson = LESSONS[0]

        output = brain.live(
            lesson_obs(next_lesson),
            reward=np.asarray(
                [reward],
                dtype=np.float64,
            ),
            done=np.asarray(
                [True],
                dtype=bool,
            ),
            decision_id=owner,
        )

        records.append({
            "trip": index + 1,
            "lesson": lesson["name"],
            "correct_action": lesson["correct"],
            "chosen_action": action_name,
            "correct": int(correct),
            "reward": reward,
            "schedule_stage": schedule_stage,
        })

        _, action_name = action_from(output)
        owner = brain.decision_id

    # Discard action issued for dummy next life.
    safe_reset(brain)

    return records


# ============================================================
# FROZEN EVALUATION / FINGERPRINT
# ============================================================

def apply_eval_action(world, action_name):
    world.mid_action_tick()
    world.apply_action(action_name)


def evaluate_cadence(brain, episodes, greedy):
    rows = []
    counts = Counter()

    for episode in range(1, episodes + 1):
        safe_reset(brain)
        world = ColdWorld()

        while not world.done:
            output = brain.act(
                world.obs(),
                greedy=bool(greedy),
            )

            _, action_name = action_from(output)

            counts[action_name] += 1

            apply_eval_action(
                world,
                action_name,
            )

        rows.append({
            "episode": episode,
            "success": int(world.success),
            "outcome": world.outcome,
            "decisions": world.decisions,
        })

    safe_reset(brain)

    return rows, counts


def evaluate_random(episodes, seed):
    rng = random.Random(
        99000 + seed
    )

    rows = []
    counts = Counter()

    for episode in range(1, episodes + 1):
        world = ColdWorld()

        while not world.done:
            action_name = rng.choice(ACTIONS)
            counts[action_name] += 1
            apply_eval_action(
                world,
                action_name,
            )

        rows.append({
            "episode": episode,
            "success": int(world.success),
            "outcome": world.outcome,
            "decisions": world.decisions,
        })

    return rows, counts


CANONICAL_SITUATIONS = [
    (
        "empty",
        dict(
            wood=0,
            stone=0,
            fire=False,
            warmth=0.42,
        ),
        "GATHER_WOOD",
    ),
    (
        "has_wood",
        dict(
            wood=1,
            stone=0,
            fire=False,
            warmth=0.42,
        ),
        "GATHER_STONE",
    ),
    (
        "has_materials",
        dict(
            wood=1,
            stone=1,
            fire=False,
            warmth=0.42,
        ),
        "CRAFT_FIRE",
    ),
    (
        "has_fire",
        dict(
            wood=0,
            stone=0,
            fire=True,
            warmth=0.42,
        ),
        "WARM_UP",
    ),
]


def fingerprint(brain, samples=300):
    result = {}

    for name, state, expected in CANONICAL_SITUATIONS:
        counts = Counter()

        for _ in range(samples):
            safe_reset(brain)

            obs = observation(
                **state,
                action_phase=0.0,
                decision_fraction=0.25,
            )

            output = brain.act(
                obs,
                greedy=False,
            )

            _, action_name = action_from(output)

            counts[action_name] += 1

        safe_reset(brain)

        obs = observation(
            **state,
            action_phase=0.0,
            decision_fraction=0.25,
        )

        greedy_output = brain.act(
            obs,
            greedy=True,
        )

        _, greedy_action = action_from(
            greedy_output
        )

        total = sum(counts.values())

        result[name] = {
            "expected": expected,
            "greedy": greedy_action,
            "sampled_expected_percent": (
                counts[expected] / total * 100.0
                if total
                else 0.0
            ),
            "sampled_distribution": {
                action: (
                    counts[action] / total * 100.0
                    if total
                    else 0.0
                )
                for action in ACTIONS
            },
        }

    safe_reset(brain)

    return result


def summarize_eval(rows):
    return {
        "episodes": len(rows),
        "success_rate": mean(
            [row["success"] for row in rows]
        ),
        "mean_decisions": mean(
            [row["decisions"] for row in rows]
        ),
        "outcomes": dict(
            Counter(
                row["outcome"]
                for row in rows
            )
        ),
    }


def action_percent(counter):
    total = sum(counter.values())

    return {
        action: (
            counter[action] / total * 100.0
            if total
            else 0.0
        )
        for action in ACTIONS
    }


def lesson_metrics(records):
    by_lesson = {}

    for lesson in LESSONS:
        name = lesson["name"]

        rows = [
            row
            for row in records
            if row["lesson"] == name
        ]

        by_lesson[name] = {
            "accuracy": mean(
                [row["correct"] for row in rows]
            ),
            "exposure": len(rows),
            "isolated": sum(
                1
                for row in rows
                if row["schedule_stage"] == "isolated"
            ),
            "interleaved": sum(
                1
                for row in rows
                if row["schedule_stage"] == "interleaved"
            ),
        }

    return {
        "overall_accuracy": mean(
            [row["correct"] for row in records]
        ),
        "by_lesson": by_lesson,
    }


def write_csv(path, rows):
    if not rows:
        return

    with open(
        path,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(
                rows[0].keys()
            ),
        )

        writer.writeheader()
        writer.writerows(rows)


# ============================================================
# ONE SEED / BUDGET SWEEP
# ============================================================

def run_seed(
    *,
    seed,
    budgets,
    eval_episodes,
    name,
):
    # ONE founder. Every budget branches independently from this exact state.
    founder = new_brain(seed)

    founder_path = OUTPUT_DIR / (
        f"{name}_founder_seed_{seed}.npz"
    )

    founder.save(
        founder_path
    )

    founder_eval_brain = Brain.load(
        founder_path
    )

    founder_sampled_rows, founder_sampled_actions = evaluate_cadence(
        founder_eval_brain,
        eval_episodes,
        greedy=False,
    )

    founder_greedy_brain = Brain.load(
        founder_path
    )

    founder_greedy_rows, founder_greedy_actions = evaluate_cadence(
        founder_greedy_brain,
        eval_episodes,
        greedy=True,
    )

    founder_fp_brain = Brain.load(
        founder_path
    )

    founder_result = {
        "sampled": summarize_eval(
            founder_sampled_rows
        ),
        "greedy": summarize_eval(
            founder_greedy_rows
        ),
        "sampled_actions": action_percent(
            founder_sampled_actions
        ),
        "greedy_actions": action_percent(
            founder_greedy_actions
        ),
        "fingerprint": fingerprint(
            founder_fp_brain
        ),
    }

    random_rows, random_actions = evaluate_random(
        eval_episodes,
        seed,
    )

    random_result = {
        "sampled": summarize_eval(
            random_rows
        ),
        "sampled_actions": action_percent(
            random_actions
        ),
    }

    budget_results = {}
    all_records = []

    for budget in budgets:
        # Independent branch from same founder.
        brain = Brain.load(
            founder_path
        )

        records = train_lessons(
            brain,
            total_trips=budget,
            seed=seed,
        )

        for row in records:
            out = dict(row)
            out["seed"] = seed
            out["budget"] = budget
            all_records.append(out)

        checkpoint = OUTPUT_DIR / (
            f"{name}_budget_{budget}_seed_{seed}.npz"
        )

        brain.save(
            checkpoint
        )

        sampled_brain = Brain.load(
            checkpoint
        )

        greedy_brain = Brain.load(
            checkpoint
        )

        fp_brain = Brain.load(
            checkpoint
        )

        sampled_rows, sampled_actions = evaluate_cadence(
            sampled_brain,
            eval_episodes,
            greedy=False,
        )

        greedy_rows, greedy_actions = evaluate_cadence(
            greedy_brain,
            eval_episodes,
            greedy=True,
        )

        metrics = lesson_metrics(
            records
        )

        budget_results[str(budget)] = {
            "lessons": metrics,
            "sampled": summarize_eval(
                sampled_rows
            ),
            "greedy": summarize_eval(
                greedy_rows
            ),
            "sampled_actions": action_percent(
                sampled_actions
            ),
            "greedy_actions": action_percent(
                greedy_actions
            ),
            "fingerprint": fingerprint(
                fp_brain
            ),
        }

    return {
        "seed": seed,
        "founder": founder_result,
        "random": random_result,
        "budgets": budget_results,
        "lesson_records": all_records,
    }


# ============================================================
# REPORT
# ============================================================

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--budgets",
        default="20,40,80,160",
    )

    parser.add_argument(
        "--eval",
        type=int,
        default=100,
    )

    parser.add_argument(
        "--seeds",
        type=int,
        default=1,
    )

    parser.add_argument(
        "--name",
        default="quick",
    )

    args = parser.parse_args()

    budgets = [
        int(item.strip())
        for item in args.budgets.split(",")
        if item.strip()
    ]

    OUTPUT_DIR.mkdir(
        exist_ok=True
    )

    version = pkg_version(
        "cadence-net"
    )

    if version != "0.81.0":
        raise RuntimeError(
            f"V4.2 requires cadence-net 0.81.0, found {version}"
        )

    if not hasattr(Brain, "wait"):
        raise RuntimeError(
            "Cadence 0.81 Brain.wait is unavailable."
        )

    print("")
    print("=" * 80)
    print(
        " CADENCE // STONE AGE V4.2 — BALANCED LESSON BUDGET SWEEP"
    )
    print("=" * 80)
    print(
        "budgets:",
        budgets,
    )
    print(
        "frozen eval episodes:",
        args.eval,
    )
    print(
        "fresh founder seeds:",
        args.seeds,
    )
    print(
        "NO extra full-chain training — lesson budget is isolated."
    )
    print("")

    seed_results = []
    all_lesson_records = []

    for offset in range(
        args.seeds
    ):
        seed = 42 + offset

        print(
            f"--- SEED {seed} ---"
        )

        result = run_seed(
            seed=seed,
            budgets=budgets,
            eval_episodes=args.eval,
            name=args.name,
        )

        seed_results.append(
            result
        )

        all_lesson_records.extend(
            result["lesson_records"]
        )

        print(
            "  founder sampled:",
            f"{result['founder']['sampled']['success_rate']*100:.1f}%"
        )

        print(
            "  random sampled:",
            f"{result['random']['sampled']['success_rate']*100:.1f}%"
        )

        for budget in budgets:
            item = result[
                "budgets"
            ][str(budget)]

            empty = item[
                "fingerprint"
            ]["empty"][
                "sampled_expected_percent"
            ]

            stone = item[
                "fingerprint"
            ]["has_wood"][
                "sampled_expected_percent"
            ]

            fire = item[
                "fingerprint"
            ]["has_materials"][
                "sampled_expected_percent"
            ]

            warm = item[
                "fingerprint"
            ]["has_fire"][
                "sampled_expected_percent"
            ]

            print(
                f"  budget {budget:>3}: "
                f"full={item['sampled']['success_rate']*100:5.1f}% | "
                f"wood={empty:5.1f} "
                f"stone={stone:5.1f} "
                f"fire={fire:5.1f} "
                f"warm={warm:5.1f}"
            )

        print("")

    write_csv(
        OUTPUT_DIR / (
            f"{args.name}_lesson_records.csv"
        ),
        all_lesson_records,
    )

    # Aggregate each budget across seeds.
    aggregate = {}

    for budget in budgets:
        key = str(budget)

        aggregate[key] = {
            "mean_sampled_success": mean([
                result["budgets"][key]["sampled"]["success_rate"]
                for result in seed_results
            ]),
            "mean_greedy_success": mean([
                result["budgets"][key]["greedy"]["success_rate"]
                for result in seed_results
            ]),
            "mean_lesson_accuracy": mean([
                result["budgets"][key]["lessons"]["overall_accuracy"]
                for result in seed_results
            ]),
            "mean_fingerprint": {
                situation: mean([
                    result["budgets"][key]["fingerprint"][situation][
                        "sampled_expected_percent"
                    ]
                    for result in seed_results
                ])
                for situation, _, _ in CANONICAL_SITUATIONS
            },
        }

    founder_sampled = mean([
        result["founder"]["sampled"]["success_rate"]
        for result in seed_results
    ])

    founder_greedy = mean([
        result["founder"]["greedy"]["success_rate"]
        for result in seed_results
    ])

    random_sampled = mean([
        result["random"]["sampled"]["success_rate"]
        for result in seed_results
    ])

    summary = {
        "cadence_net_version": version,
        "protocol": {
            "chain": [
                "GATHER_WOOD",
                "GATHER_STONE",
                "CRAFT_FIRE",
                "WARM_UP",
            ],
            "budgets": budgets,
            "eval_episodes": args.eval,
            "seeds": args.seeds,
            "same_founder_per_budget": True,
            "balanced_equal_exposure": True,
            "uses_brain_wait": True,
            "extra_full_chain_training": False,
            "actor_eta_critic": ACTOR_ETA_CRITIC,
        },
        "controls": {
            "founder_sampled_success": founder_sampled,
            "founder_greedy_success": founder_greedy,
            "random_sampled_success": random_sampled,
        },
        "aggregate": aggregate,
        "per_seed": [
            {
                "seed": result["seed"],
                "founder": result["founder"],
                "random": result["random"],
                "budgets": result["budgets"],
            }
            for result in seed_results
        ],
    }

    (
        OUTPUT_DIR
        / f"{args.name}_summary.json"
    ).write_text(
        json.dumps(
            summary,
            indent=2,
        ),
        encoding="utf-8",
    )

    report = []

    def add(line=""):
        report.append(str(line))

    add(
        "CADENCE // STONE AGE V4.2 — BALANCED LESSON BUDGET SWEEP"
    )
    add("=" * 80)
    add(
        f"cadence-net: {version}"
    )
    add(
        "Every lesson budget branches independently from the exact same founder."
    )
    add(
        "No extra full-chain training is performed after lessons."
    )
    add(
        f"Budgets: {budgets}"
    )
    add(
        f"Frozen eval episodes: {args.eval} per seed"
    )
    add(
        f"Fresh founder seeds: {args.seeds}"
    )
    add("")

    add("CONTROLS")
    add(
        f"  founder sampled={founder_sampled*100:5.1f}% "
        f"greedy={founder_greedy*100:5.1f}%"
    )
    add(
        f"  random  sampled={random_sampled*100:5.1f}%"
    )
    add("")

    add("BUDGET SWEEP")
    add(
        "  budget | lesson | full sampled | full greedy | "
        "empty→wood | wood→stone | materials→fire | fire→warm"
    )

    for budget in budgets:
        item = aggregate[
            str(budget)
        ]

        fp = item[
            "mean_fingerprint"
        ]

        add(
            f"  {budget:>6} | "
            f"{item['mean_lesson_accuracy']*100:6.1f}% | "
            f"{item['mean_sampled_success']*100:11.1f}% | "
            f"{item['mean_greedy_success']*100:10.1f}% | "
            f"{fp['empty']:10.1f}% | "
            f"{fp['has_wood']:10.1f}% | "
            f"{fp['has_materials']:14.1f}% | "
            f"{fp['has_fire']:9.1f}%"
        )

    add("")
    add("PER-SEED LESSON ACCURACY")

    for result in seed_results:
        add("")
        add(
            f"SEED {result['seed']}"
        )

        for budget in budgets:
            item = result[
                "budgets"
            ][str(budget)]

            add(
                f"  BUDGET {budget}"
            )

            for lesson in LESSONS:
                name = lesson["name"]
                lm = item[
                    "lessons"
                ]["by_lesson"][name]

                add(
                    f"    {name:<13} "
                    f"accuracy={lm['accuracy']*100:5.1f}% "
                    f"exposure={lm['exposure']:>3} "
                    f"(isolated={lm['isolated']}, interleaved={lm['interleaved']})"
                )

    add("")
    add("HOW TO READ THIS")
    add(
        "Look for a middle budget where empty→GATHER_WOOD and full-chain success "
        "peak, followed by degradation at a larger budget."
    )
    add(
        "That pattern would be direct evidence of an over-drilling effect in this "
        "Stone Age COLD chain."
    )
    add(
        "If all fingerprints improve monotonically, more lesson exposure is helping."
    )
    add(
        "If GATHER_WOOD stays weak at every budget, the issue is not simply lesson "
        "overexposure and we should change how the first prerequisite is represented/taught."
    )

    report_text = "\n".join(
        report
    )

    (
        OUTPUT_DIR
        / f"{args.name}_REPORT.txt"
    ).write_text(
        report_text,
        encoding="utf-8",
    )

    print("")
    print(
        report_text
    )
    print("")
    print(
        "Results:",
        OUTPUT_DIR,
    )


if __name__ == "__main__":
    main()
