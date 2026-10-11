
"""
CADENCE // STONE AGE V4.3
Competency-Based Backward Lessons — cadence-net 0.81.0

Purpose
-------
V4.2 showed that fixed drilling can help one prerequisite while damaging another.
V4.3 stops teaching a lesson when Cadence demonstrates competency, then only
rehearses an older lesson if its validation accuracy actually falls.

COLD chain:
    GATHER_WOOD -> GATHER_STONE -> CRAFT_FIRE -> WARM_UP

Backward teaching order:
    WARM_UP -> CRAFT_FIRE -> GATHER_STONE -> GATHER_WOOD

Important controls:
- full chain state is observable
- Cadence chooses every action
- correct/wrong actions are graded by reward, never supplied as labels
- Brain.wait is used while the action outcome is delayed
- the final brain is frozen before full-chain evaluation
- founder and uniform Random are controls
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

INPUTS = 9
OUTPUT_DIR = Path(__file__).resolve().parent / "benchmark_output_v4_3"

ACTOR_ETA = 0.03
ACTOR_ETA_BIAS = 0.003
ACTOR_GAMMA = 0.95
ACTOR_LAM = 0.60
ACTOR_ETA_CRITIC = 5.0

LESSON_REWARD_CORRECT = 1.0
LESSON_REWARD_WRONG = -0.25

MAX_DECISIONS = 8


def mean(values):
    return statistics.fmean(values) if values else 0.0


# ============================================================
# OBSERVATION
# ============================================================

def observation(
    *,
    wood,
    stone,
    fire,
    warmth,
    action_phase=0.0,
):
    """
    The entire prerequisite state is visible.
    No target action is encoded in the observation.
    """
    return np.asarray([[
        float(np.clip(warmth, 0.0, 1.0)),
        1.0 if wood >= 1 else 0.0,
        1.0 if stone >= 1 else 0.0,
        1.0 if fire else 0.0,
        min(1.0, wood / 2.0),
        min(1.0, stone / 2.0),
        float(np.clip(action_phase, 0.0, 1.0)),
        1.0,  # COLD task cue
        1.0,  # bias / world-active cue
    ]], dtype=np.float64)


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
# ONE-STEP BACKWARD LESSONS
# ============================================================

LESSONS = [
    # final step first
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

LESSON_BY_NAME = {
    lesson["name"]: lesson
    for lesson in LESSONS
}


def lesson_obs(lesson, phase=0.0):
    return observation(
        wood=lesson["wood"],
        stone=lesson["stone"],
        fire=lesson["fire"],
        warmth=lesson["warmth"],
        action_phase=phase,
    )


def post_lesson_obs(lesson, chosen_action):
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
    )


def one_lesson_trip(brain, lesson):
    """
    One action, delayed observation-only moments, then actual reward.
    The action is graded after execution. It is never supplied as a label.
    """
    safe_reset(brain)

    output = brain.live(
        lesson_obs(lesson, phase=0.0)
    )

    _, chosen = action_from(output)
    owner = brain.decision_id

    # Outcome has not arrived yet.
    brain.wait(
        lesson_obs(lesson, phase=0.5)
    )

    # Physical action has now happened.
    brain.wait(
        post_lesson_obs(lesson, chosen)
    )

    correct = chosen == lesson["correct"]

    reward = (
        LESSON_REWARD_CORRECT
        if correct
        else LESSON_REWARD_WRONG
    )

    # Report the delayed outcome of exactly the action that was executed.
    brain.live(
        lesson_obs(lesson, phase=0.0),
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

    # Discard the newly issued next-life action.
    safe_reset(brain)

    return {
        "lesson": lesson["name"],
        "correct_action": lesson["correct"],
        "chosen_action": chosen,
        "correct": int(correct),
        "reward": reward,
    }


def validate_lesson(brain, lesson, samples):
    """
    Frozen sampled validation. No reward is supplied.
    """
    correct = 0
    counts = Counter()

    for _ in range(samples):
        safe_reset(brain)

        output = brain.act(
            lesson_obs(
                lesson,
                phase=0.0,
            ),
            greedy=False,
        )

        _, chosen = action_from(output)

        counts[chosen] += 1

        if chosen == lesson["correct"]:
            correct += 1

    safe_reset(brain)

    return {
        "accuracy": correct / samples,
        "samples": samples,
        "distribution": {
            action: counts[action] / samples * 100.0
            for action in ACTIONS
        },
    }


def validate_named_lessons(
    brain,
    lesson_names,
    samples,
):
    return {
        name: validate_lesson(
            brain,
            LESSON_BY_NAME[name],
            samples,
        )
        for name in lesson_names
    }


# ============================================================
# ADAPTIVE COMPETENCY CURRICULUM
# ============================================================

def competency_curriculum(
    brain,
    *,
    seed,
    target_accuracy,
    maintenance_accuracy,
    block_size,
    rescue_size,
    validation_samples,
    max_direct_trips,
):
    """
    Backward curriculum with early stopping.

    For each new lesson:
    - train only in small blocks
    - validate it after each block
    - stop direct drilling as soon as target accuracy is reached
    - validate previously mastered lessons
    - only rehearse an old lesson if it fell below maintenance threshold

    This directly tests the team's warning that too much drilling can hurt.
    """
    rng = random.Random(43000 + seed)

    records = []
    history = []
    mastered = []
    direct_counts = Counter()
    rescue_counts = Counter()

    for lesson in LESSONS:
        name = lesson["name"]

        # Baseline before this lesson receives direct training.
        baseline = validate_lesson(
            brain,
            lesson,
            validation_samples,
        )

        history.append({
            "event": "lesson_start",
            "lesson": name,
            "direct_trips": 0,
            "accuracy": baseline["accuracy"],
        })

        while direct_counts[name] < max_direct_trips:
            # Train only a small block on the new lesson.
            for _ in range(block_size):
                if direct_counts[name] >= max_direct_trips:
                    break

                result = one_lesson_trip(
                    brain,
                    lesson,
                )

                direct_counts[name] += 1

                row = dict(result)
                row["kind"] = "direct"
                row["seed"] = seed
                row["trip_for_lesson"] = direct_counts[name]
                records.append(row)

            current = validate_lesson(
                brain,
                lesson,
                validation_samples,
            )

            # Check old skills. Rescue only the weakest skill that actually
            # dropped below the maintenance threshold.
            old_validation = validate_named_lessons(
                brain,
                mastered,
                validation_samples,
            )

            weak = [
                (
                    old_name,
                    old_validation[old_name]["accuracy"],
                )
                for old_name in mastered
                if (
                    old_validation[old_name]["accuracy"]
                    < maintenance_accuracy
                )
            ]

            if weak:
                weak.sort(
                    key=lambda item: item[1]
                )

                rescue_name, rescue_before = weak[0]
                rescue_lesson = LESSON_BY_NAME[
                    rescue_name
                ]

                for _ in range(rescue_size):
                    result = one_lesson_trip(
                        brain,
                        rescue_lesson,
                    )

                    rescue_counts[rescue_name] += 1

                    row = dict(result)
                    row["kind"] = "rescue"
                    row["seed"] = seed
                    row["trip_for_lesson"] = rescue_counts[
                        rescue_name
                    ]
                    records.append(row)

                rescue_after = validate_lesson(
                    brain,
                    rescue_lesson,
                    validation_samples,
                )

                history.append({
                    "event": "rescue",
                    "lesson": rescue_name,
                    "current_lesson": name,
                    "accuracy_before": rescue_before,
                    "accuracy_after": rescue_after["accuracy"],
                    "rescue_trips_total": rescue_counts[rescue_name],
                })

                # Revalidate current after rescue because rehearsal may change it.
                current = validate_lesson(
                    brain,
                    lesson,
                    validation_samples,
                )

            history.append({
                "event": "checkpoint",
                "lesson": name,
                "direct_trips": direct_counts[name],
                "accuracy": current["accuracy"],
                "old_accuracies": {
                    old_name: old_validation[old_name]["accuracy"]
                    for old_name in old_validation
                },
            })

            if current["accuracy"] >= target_accuracy:
                break

        final_current = validate_lesson(
            brain,
            lesson,
            validation_samples,
        )

        mastered.append(name)

        history.append({
            "event": "lesson_end",
            "lesson": name,
            "direct_trips": direct_counts[name],
            "rescue_trips": rescue_counts[name],
            "accuracy": final_current["accuracy"],
            "met_target": (
                final_current["accuracy"]
                >= target_accuracy
            ),
        })

    final_validation = validate_named_lessons(
        brain,
        [lesson["name"] for lesson in LESSONS],
        validation_samples * 2,
    )

    return {
        "records": records,
        "history": history,
        "direct_counts": dict(direct_counts),
        "rescue_counts": dict(rescue_counts),
        "final_validation": final_validation,
    }


# ============================================================
# FULL COLD CHAIN
# ============================================================

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

    def obs(self):
        return observation(
            wood=self.wood,
            stone=self.stone,
            fire=self.fire,
            warmth=self.warmth,
            action_phase=0.0,
        )

    def step(self, action_name):
        self.decisions += 1

        # physical delay
        self.warmth -= 0.015
        if self.fire:
            self.warmth += 0.006

        if action_name == "GATHER_WOOD":
            self.wood = min(
                2,
                self.wood + 1,
            )

        elif action_name == "GATHER_STONE":
            self.stone = min(
                2,
                self.stone + 1,
            )

        elif action_name == "CRAFT_FIRE":
            if (
                self.wood >= 1
                and self.stone >= 1
            ):
                self.fire = True

        elif action_name == "WARM_UP":
            if self.fire:
                self.warmth += 0.52

        self.warmth -= 0.015
        if self.fire:
            self.warmth += 0.006

        self.warmth = min(
            1.0,
            self.warmth,
        )

        if (
            self.fire
            and self.warmth >= 0.75
        ):
            self.done = True
            self.success = True
            self.outcome = "SUCCESS"

        elif self.warmth <= 0.0:
            self.done = True
            self.outcome = "HYPOTHERMIA"

        elif self.decisions >= MAX_DECISIONS:
            self.done = True
            self.outcome = "TIMEOUT"


def evaluate_cadence(
    brain,
    episodes,
    greedy,
):
    rows = []
    action_counts = Counter()

    for episode in range(
        1,
        episodes + 1,
    ):
        safe_reset(brain)
        world = ColdWorld()

        while not world.done:
            output = brain.act(
                world.obs(),
                greedy=bool(greedy),
            )

            _, chosen = action_from(output)

            action_counts[chosen] += 1
            world.step(chosen)

        rows.append({
            "episode": episode,
            "success": int(
                world.success
            ),
            "outcome": world.outcome,
            "decisions": world.decisions,
        })

    safe_reset(brain)

    return rows, action_counts


def evaluate_random(
    episodes,
    seed,
):
    rng = random.Random(
        95000 + seed
    )

    rows = []
    action_counts = Counter()

    for episode in range(
        1,
        episodes + 1,
    ):
        world = ColdWorld()

        while not world.done:
            chosen = rng.choice(
                ACTIONS
            )

            action_counts[chosen] += 1
            world.step(chosen)

        rows.append({
            "episode": episode,
            "success": int(
                world.success
            ),
            "outcome": world.outcome,
            "decisions": world.decisions,
        })

    return rows, action_counts


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
    total = sum(
        counter.values()
    )

    return {
        action: (
            counter[action]
            / total
            * 100.0
            if total
            else 0.0
        )
        for action in ACTIONS
    }


CANONICAL = [
    (
        "empty",
        LESSON_BY_NAME["gather_wood"],
    ),
    (
        "has_wood",
        LESSON_BY_NAME["gather_stone"],
    ),
    (
        "has_materials",
        LESSON_BY_NAME["craft_fire"],
    ),
    (
        "has_fire",
        LESSON_BY_NAME["warm_up"],
    ),
]


def fingerprint(
    brain,
    samples=300,
):
    result = {}

    for situation, lesson in CANONICAL:
        validation = validate_lesson(
            brain,
            lesson,
            samples,
        )

        safe_reset(brain)

        greedy_output = brain.act(
            lesson_obs(
                lesson,
                phase=0.0,
            ),
            greedy=True,
        )

        _, greedy_action = action_from(
            greedy_output
        )

        result[situation] = {
            "expected": lesson["correct"],
            "sampled_expected_percent": (
                validation["accuracy"]
                * 100.0
            ),
            "sampled_distribution": validation[
                "distribution"
            ],
            "greedy": greedy_action,
        }

    safe_reset(brain)

    return result


def write_csv(
    path,
    rows,
):
    if not rows:
        return

    fieldnames = sorted(
        {
            key
            for row in rows
            for key in row.keys()
        }
    )

    with open(
        path,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)


# ============================================================
# EXPERIMENT
# ============================================================

def run_seed(
    *,
    seed,
    eval_episodes,
    target_accuracy,
    maintenance_accuracy,
    block_size,
    rescue_size,
    validation_samples,
    max_direct_trips,
    name,
):
    founder = new_brain(
        seed
    )

    founder_path = OUTPUT_DIR / (
        f"{name}_founder_seed_{seed}.npz"
    )

    founder.save(
        founder_path
    )

    trained = Brain.load(
        founder_path
    )

    curriculum = competency_curriculum(
        trained,
        seed=seed,
        target_accuracy=target_accuracy,
        maintenance_accuracy=maintenance_accuracy,
        block_size=block_size,
        rescue_size=rescue_size,
        validation_samples=validation_samples,
        max_direct_trips=max_direct_trips,
    )

    trained_path = OUTPUT_DIR / (
        f"{name}_trained_seed_{seed}.npz"
    )

    trained.save(
        trained_path
    )

    # Frozen arms.
    trained_sampled = Brain.load(
        trained_path
    )

    trained_greedy = Brain.load(
        trained_path
    )

    trained_fp = Brain.load(
        trained_path
    )

    founder_sampled = Brain.load(
        founder_path
    )

    founder_greedy = Brain.load(
        founder_path
    )

    founder_fp = Brain.load(
        founder_path
    )

    tr_s_rows, tr_s_actions = evaluate_cadence(
        trained_sampled,
        eval_episodes,
        greedy=False,
    )

    tr_g_rows, tr_g_actions = evaluate_cadence(
        trained_greedy,
        eval_episodes,
        greedy=True,
    )

    fo_s_rows, fo_s_actions = evaluate_cadence(
        founder_sampled,
        eval_episodes,
        greedy=False,
    )

    fo_g_rows, fo_g_actions = evaluate_cadence(
        founder_greedy,
        eval_episodes,
        greedy=True,
    )

    random_rows, random_actions = evaluate_random(
        eval_episodes,
        seed,
    )

    return {
        "seed": seed,
        "curriculum": curriculum,
        "trained": {
            "sampled": summarize_eval(
                tr_s_rows
            ),
            "greedy": summarize_eval(
                tr_g_rows
            ),
            "sampled_actions": action_percent(
                tr_s_actions
            ),
            "greedy_actions": action_percent(
                tr_g_actions
            ),
            "fingerprint": fingerprint(
                trained_fp
            ),
        },
        "founder": {
            "sampled": summarize_eval(
                fo_s_rows
            ),
            "greedy": summarize_eval(
                fo_g_rows
            ),
            "sampled_actions": action_percent(
                fo_s_actions
            ),
            "greedy_actions": action_percent(
                fo_g_actions
            ),
            "fingerprint": fingerprint(
                founder_fp
            ),
        },
        "random": {
            "sampled": summarize_eval(
                random_rows
            ),
            "sampled_actions": action_percent(
                random_actions
            ),
        },
    }


# ============================================================
# MAIN / REPORT
# ============================================================

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--target",
        type=float,
        default=0.70,
    )

    parser.add_argument(
        "--maintenance",
        type=float,
        default=0.55,
    )

    parser.add_argument(
        "--block",
        type=int,
        default=4,
    )

    parser.add_argument(
        "--rescue",
        type=int,
        default=2,
    )

    parser.add_argument(
        "--validation",
        type=int,
        default=80,
    )

    parser.add_argument(
        "--max-direct",
        type=int,
        default=60,
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

    OUTPUT_DIR.mkdir(
        exist_ok=True
    )

    version = pkg_version(
        "cadence-net"
    )

    if version != "0.81.0":
        raise RuntimeError(
            f"V4.3 requires cadence-net 0.81.0, found {version}"
        )

    if not hasattr(
        Brain,
        "wait",
    ):
        raise RuntimeError(
            "Cadence 0.81 Brain.wait is unavailable."
        )

    print("")
    print("=" * 80)
    print(
        " CADENCE // STONE AGE V4.3 — COMPETENCY-BASED BACKWARD LESSONS"
    )
    print("=" * 80)
    print(
        f"target accuracy: {args.target*100:.0f}%"
    )
    print(
        f"maintenance floor: {args.maintenance*100:.0f}%"
    )
    print(
        f"direct block: {args.block} trips"
    )
    print(
        f"rescue block: {args.rescue} trips"
    )
    print(
        f"max direct trips / lesson: {args.max_direct}"
    )
    print(
        f"validation samples: {args.validation}"
    )
    print(
        f"frozen eval episodes: {args.eval}"
    )
    print(
        f"fresh seeds: {args.seeds}"
    )
    print("")

    results = []
    all_training_records = []
    all_history_rows = []

    for offset in range(
        args.seeds
    ):
        seed = 42 + offset

        print(
            f"--- SEED {seed} ---"
        )

        result = run_seed(
            seed=seed,
            eval_episodes=args.eval,
            target_accuracy=args.target,
            maintenance_accuracy=args.maintenance,
            block_size=args.block,
            rescue_size=args.rescue,
            validation_samples=args.validation,
            max_direct_trips=args.max_direct,
            name=args.name,
        )

        results.append(
            result
        )

        for record in result[
            "curriculum"
        ]["records"]:
            row = dict(record)
            all_training_records.append(
                row
            )

        for event in result[
            "curriculum"
        ]["history"]:
            row = {
                "seed": seed,
                "event": event.get(
                    "event"
                ),
                "lesson": event.get(
                    "lesson"
                ),
                "current_lesson": event.get(
                    "current_lesson"
                ),
                "direct_trips": event.get(
                    "direct_trips"
                ),
                "accuracy": event.get(
                    "accuracy"
                ),
                "accuracy_before": event.get(
                    "accuracy_before"
                ),
                "accuracy_after": event.get(
                    "accuracy_after"
                ),
                "rescue_trips_total": event.get(
                    "rescue_trips_total"
                ),
                "met_target": event.get(
                    "met_target"
                ),
            }

            all_history_rows.append(
                row
            )

        print(
            "  final lesson validation:"
        )

        for lesson in LESSONS:
            name = lesson[
                "name"
            ]

            accuracy = result[
                "curriculum"
            ][
                "final_validation"
            ][name][
                "accuracy"
            ]

            direct = result[
                "curriculum"
            ][
                "direct_counts"
            ].get(
                name,
                0,
            )

            rescue = result[
                "curriculum"
            ][
                "rescue_counts"
            ].get(
                name,
                0,
            )

            print(
                f"    {name:<13} "
                f"{accuracy*100:5.1f}%  "
                f"direct={direct:>2} "
                f"rescue={rescue:>2}"
            )

        print(
            f"  full sampled: "
            f"{result['trained']['sampled']['success_rate']*100:.1f}%"
        )

        print(
            f"  founder sampled: "
            f"{result['founder']['sampled']['success_rate']*100:.1f}%"
        )

        print(
            f"  random sampled: "
            f"{result['random']['sampled']['success_rate']*100:.1f}%"
        )

        print("")

    write_csv(
        OUTPUT_DIR
        / f"{args.name}_training_records.csv",
        all_training_records,
    )

    write_csv(
        OUTPUT_DIR
        / f"{args.name}_curriculum_history.csv",
        all_history_rows,
    )

    trained_sampled = mean([
        result["trained"]["sampled"]["success_rate"]
        for result in results
    ])

    trained_greedy = mean([
        result["trained"]["greedy"]["success_rate"]
        for result in results
    ])

    founder_sampled = mean([
        result["founder"]["sampled"]["success_rate"]
        for result in results
    ])

    founder_greedy = mean([
        result["founder"]["greedy"]["success_rate"]
        for result in results
    ])

    random_sampled = mean([
        result["random"]["sampled"]["success_rate"]
        for result in results
    ])

    aggregate_fingerprint = {}

    for situation, _ in CANONICAL:
        aggregate_fingerprint[
            situation
        ] = mean([
            result[
                "trained"
            ][
                "fingerprint"
            ][situation][
                "sampled_expected_percent"
            ]
            for result in results
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
            "backward_order": [
                lesson["name"]
                for lesson in LESSONS
            ],
            "target_accuracy": args.target,
            "maintenance_accuracy": args.maintenance,
            "block_size": args.block,
            "rescue_size": args.rescue,
            "validation_samples": args.validation,
            "max_direct_trips": args.max_direct,
            "eval_episodes": args.eval,
            "seeds": args.seeds,
            "uses_brain_wait": True,
            "target_action_in_observation": False,
            "adaptive_early_stopping": True,
            "rehearsal_only_on_validation_drop": True,
        },
        "aggregate": {
            "trained_sampled_success": trained_sampled,
            "trained_greedy_success": trained_greedy,
            "founder_sampled_success": founder_sampled,
            "founder_greedy_success": founder_greedy,
            "random_sampled_success": random_sampled,
            "trained_fingerprint": aggregate_fingerprint,
        },
        "per_seed": results,
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
        report.append(
            str(line)
        )

    add(
        "CADENCE // STONE AGE V4.3 — COMPETENCY-BASED BACKWARD LESSONS"
    )
    add("=" * 80)
    add(
        f"cadence-net: {version}"
    )
    add(
        f"Target competency: {args.target*100:.0f}%"
    )
    add(
        f"Maintenance floor: {args.maintenance*100:.0f}%"
    )
    add(
        f"Direct lesson block: {args.block}"
    )
    add(
        f"Rescue block: {args.rescue}"
    )
    add(
        f"Max direct trips / lesson: {args.max_direct}"
    )
    add(
        "Older lessons are rehearsed ONLY if frozen validation drops below "
        "the maintenance floor."
    )
    add("")

    add(
        "FROZEN FULL-CHAIN EVALUATION"
    )

    add(
        f"  trained sampled={trained_sampled*100:5.1f}% "
        f"greedy={trained_greedy*100:5.1f}%"
    )

    add(
        f"  founder sampled={founder_sampled*100:5.1f}% "
        f"greedy={founder_greedy*100:5.1f}%"
    )

    add(
        f"  random  sampled={random_sampled*100:5.1f}%"
    )

    add("")
    add(
        "TRAINED CANONICAL STATE FINGERPRINT"
    )

    for situation, lesson in CANONICAL:
        add(
            f"  {situation:<14} "
            f"expected={lesson['correct']:<13} "
            f"sampled={aggregate_fingerprint[situation]:5.1f}%"
        )

    add("")
    add(
        "PER-SEED FINAL LESSON COMPETENCY / TRAINING COST"
    )

    for result in results:
        add("")
        add(
            f"SEED {result['seed']}"
        )

        for lesson in LESSONS:
            name = lesson[
                "name"
            ]

            validation = result[
                "curriculum"
            ][
                "final_validation"
            ][name]

            direct = result[
                "curriculum"
            ][
                "direct_counts"
            ].get(
                name,
                0,
            )

            rescue = result[
                "curriculum"
            ][
                "rescue_counts"
            ].get(
                name,
                0,
            )

            add(
                f"  {name:<13} "
                f"final={validation['accuracy']*100:5.1f}% "
                f"direct={direct:>2} "
                f"rescue={rescue:>2}"
            )

    add("")
    add(
        "HOW TO READ THIS"
    )

    add(
        "If GATHER_WOOD now reaches competency without later lessons collapsing, "
        "adaptive stopping is helping."
    )

    add(
        "If all four one-step competencies are strong but full-chain success remains "
        "low, the remaining problem is composition/temporal sequence production rather "
        "than one-step acquisition."
    )

    add(
        "If rescue trips become very large, later lessons are interfering with earlier "
        "ones even under competency-based stopping."
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
