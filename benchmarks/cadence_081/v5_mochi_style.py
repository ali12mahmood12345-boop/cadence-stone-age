
"""
CADENCE // STONE AGE V5
Mochi-inspired selective-caregiver benchmark for cadence-net 0.81.0

This benchmark does NOT copy Mochi's full anatomy or world.

It isolates the training pattern documented by Mochi / Cadence:
- one continuing Brain.compose brain
- alternate guided and autonomous periods
- correct only disagreements
- keep actual action/outcome identity intact
- let the acquired brain continue living after the caregiver leaves

COLD chain:
GATHER_WOOD -> GATHER_STONE -> CRAFT_FIRE -> WARM_UP

Arms:
1. natural_only
2. grade_only
3. corrective_teacher
4. founder
5. random
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
from cadence import Brain

OUTPUT_DIR = Path(__file__).resolve().parent / "benchmark_output_v5"

ACTIONS = [
    "GATHER_WOOD",
    "GATHER_STONE",
    "CRAFT_FIRE",
    "WARM_UP",
    "WAIT",
]
AIDX = {name: i for i, name in enumerate(ACTIONS)}

INPUTS = 7
MAX_DECISIONS = 10

SUCCESS_REWARD = 2.0
FAILURE_REWARD = -1.0

GRADE_RIGHT = 0.50
GRADE_WRONG = -0.50


def mean(values):
    return statistics.fmean(values) if values else 0.0


def obs(*, wood, stone, fire, warmth=0.35):
    """Full prerequisite state; no target action is encoded."""
    return np.asarray([[
        float(np.clip(warmth, 0.0, 1.0)),
        1.0 if wood >= 1 else 0.0,
        1.0 if stone >= 1 else 0.0,
        1.0 if fire else 0.0,
        min(1.0, wood / 2.0),
        min(1.0, stone / 2.0),
        1.0,  # COLD task/world cue
    ]], dtype=np.float64)


class ColdChamber:
    """
    Correct sequence:
      empty         -> GATHER_WOOD
      has wood      -> GATHER_STONE
      has materials -> CRAFT_FIRE
      has fire      -> WARM_UP

    Wrong actions do not advance the prerequisite state.
    This is deliberate: after an executed mistake the failed cue is still
    present, so a corrective teacher can label the current observation.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self.wood = 0
        self.stone = 0
        self.fire = False
        self.warmth = 0.35
        self.decisions = 0
        self.done = False
        self.success = False
        self.outcome = ""

    def observation(self):
        return obs(
            wood=self.wood,
            stone=self.stone,
            fire=self.fire,
            warmth=self.warmth,
        )

    def oracle_action(self):
        if self.fire:
            return "WARM_UP"
        if self.wood >= 1 and self.stone >= 1:
            return "CRAFT_FIRE"
        if self.wood >= 1:
            return "GATHER_STONE"
        return "GATHER_WOOD"

    def execute(self, action_name):
        expected = self.oracle_action()
        agreement = action_name == expected

        if agreement:
            if action_name == "GATHER_WOOD":
                self.wood = 1
            elif action_name == "GATHER_STONE":
                self.stone = 1
            elif action_name == "CRAFT_FIRE":
                self.fire = True
            elif action_name == "WARM_UP":
                self.warmth = 0.90
                self.success = True
                self.done = True
                self.outcome = "SUCCESS"

        self.decisions += 1

        if not self.done and self.decisions >= MAX_DECISIONS:
            self.done = True
            self.outcome = "TIMEOUT"

        reward = 0.0
        if self.done:
            reward = SUCCESS_REWARD if self.success else FAILURE_REWARD

        return {
            "expected": expected,
            "chosen": action_name,
            "agreement": agreement,
            "reward": reward,
            "done": self.done,
        }


def new_brain(seed):
    # Keep defaults as the control. Brain.compose includes the continuing
    # working trace and associative memory in Cadence 0.81.
    return Brain.compose(
        inputs=INPUTS,
        actions=len(ACTIONS),
        modules=(48, 24),
        seed=int(seed),
        arousal=True,
    )


def decode(output):
    idx = int(np.asarray(output).reshape(-1)[0])
    idx = max(0, min(len(ACTIONS) - 1, idx))
    return idx, ACTIONS[idx]


def reward_array(value):
    return np.asarray([float(value)], dtype=np.float64)


def done_array(value):
    return np.asarray([bool(value)], dtype=bool)


def teacher_array(action_name):
    return np.asarray([AIDX[action_name]], dtype=np.int64)


def caregiver_active(global_decision, guided_span, autonomous_span):
    if guided_span <= 0:
        return False

    cycle = guided_span + autonomous_span
    if cycle <= 0:
        return False

    return (global_decision % cycle) < guided_span


def run_continuing_life(
    brain,
    *,
    mode,
    episodes,
    guided_span,
    autonomous_span,
    seed,
):
    """
    One continuing Cadence stream.

    Event order:
      observation -> brain chooses -> body executes -> actual outcome
      -> next observation + outcome -> optional correction of current cue
      -> next action

    corrective_teacher:
      only after an executed disagreement during a guided period.
      Since a wrong action leaves the chamber cue unchanged, the teacher is
      correcting the same state that was just answered incorrectly.

    grade_only:
      no action label is supplied. Guided disagreements/agreements add a
      small grading reward to the actual outcome.
    """

    if mode not in {"natural_only", "grade_only", "corrective_teacher"}:
        raise ValueError(mode)

    rows = []

    chamber = ColdChamber()

    # First decision in the continuing life.
    output = brain.step(chamber.observation())
    _, current_action = decode(output)

    global_decision = 0

    for episode in range(1, episodes + 1):
        while not chamber.done:
            guided = caregiver_active(
                global_decision,
                guided_span,
                autonomous_span,
            )

            state_before = (
                chamber.wood,
                chamber.stone,
                int(chamber.fire),
            )

            outcome = chamber.execute(current_action)

            actual_reward = outcome["reward"]
            consumed_reward = actual_reward

            if mode == "grade_only" and guided:
                consumed_reward += (
                    GRADE_RIGHT
                    if outcome["agreement"]
                    else GRADE_WRONG
                )

            # Teacher labels the CURRENT observation, not the preceding action.
            teacher = None

            if (
                mode == "corrective_teacher"
                and guided
                and not outcome["agreement"]
                and not outcome["done"]
            ):
                teacher = teacher_array(outcome["expected"])

            rows.append({
                "episode": episode,
                "global_decision": global_decision,
                "mode": mode,
                "guided": int(guided),
                "wood_before": state_before[0],
                "stone_before": state_before[1],
                "fire_before": state_before[2],
                "expected": outcome["expected"],
                "chosen": outcome["chosen"],
                "agreement": int(outcome["agreement"]),
                "teacher_used": int(teacher is not None),
                "actual_world_reward": actual_reward,
                "reward_consumed": consumed_reward,
                "terminal": int(outcome["done"]),
                "success": int(chamber.success if outcome["done"] else False),
            })

            global_decision += 1

            if outcome["done"]:
                next_chamber = ColdChamber()

                output = brain.step(
                    next_chamber.observation(),
                    reward=reward_array(consumed_reward),
                    done=done_array(True),
                )

                _, current_action = decode(output)
                chamber = next_chamber
                break

            output = brain.step(
                chamber.observation(),
                reward=reward_array(consumed_reward),
                done=done_array(False),
                teacher=teacher,
            )

            _, current_action = decode(output)

    # The final terminal transition emitted one unexecuted next-life action.
    # Reset transient stream state; acquired parameters/memory remain.
    brain.reset()

    return rows


def eval_cadence(brain, episodes, greedy):
    rows = []
    counts = Counter()

    for ep in range(1, episodes + 1):
        brain.reset()
        chamber = ColdChamber()

        while not chamber.done:
            output = brain.act(
                chamber.observation(),
                greedy=bool(greedy),
            )

            _, action_name = decode(output)
            counts[action_name] += 1
            chamber.execute(action_name)

        rows.append({
            "episode": ep,
            "success": int(chamber.success),
            "decisions": chamber.decisions,
            "outcome": chamber.outcome,
        })

    brain.reset()
    return rows, counts


def eval_random(episodes, seed):
    rng = random.Random(900_000 + seed)
    rows = []
    counts = Counter()

    for ep in range(1, episodes + 1):
        chamber = ColdChamber()

        while not chamber.done:
            action_name = rng.choice(ACTIONS)
            counts[action_name] += 1
            chamber.execute(action_name)

        rows.append({
            "episode": ep,
            "success": int(chamber.success),
            "decisions": chamber.decisions,
            "outcome": chamber.outcome,
        })

    return rows, counts


CANONICAL = [
    (
        "empty",
        dict(wood=0, stone=0, fire=False, warmth=0.35),
        "GATHER_WOOD",
    ),
    (
        "has_wood",
        dict(wood=1, stone=0, fire=False, warmth=0.35),
        "GATHER_STONE",
    ),
    (
        "has_materials",
        dict(wood=1, stone=1, fire=False, warmth=0.35),
        "CRAFT_FIRE",
    ),
    (
        "has_fire",
        dict(wood=1, stone=1, fire=True, warmth=0.35),
        "WARM_UP",
    ),
]


def fingerprint(brain, samples):
    result = {}

    for situation, state, expected in CANONICAL:
        counts = Counter()

        for _ in range(samples):
            brain.reset()
            output = brain.act(
                obs(**state),
                greedy=False,
            )
            _, action_name = decode(output)
            counts[action_name] += 1

        brain.reset()

        greedy_out = brain.act(
            obs(**state),
            greedy=True,
        )

        _, greedy_name = decode(greedy_out)

        result[situation] = {
            "expected": expected,
            "sampled_expected_percent": (
                counts[expected] / samples * 100.0
            ),
            "greedy": greedy_name,
            "sampled_distribution": {
                action: counts[action] / samples * 100.0
                for action in ACTIONS
            },
        }

    brain.reset()
    return result


def summarize(rows):
    return {
        "episodes": len(rows),
        "success_rate": mean([row["success"] for row in rows]),
        "mean_decisions": mean([row["decisions"] for row in rows]),
        "outcomes": dict(Counter(row["outcome"] for row in rows)),
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


def training_metrics(rows):
    terminal = [row for row in rows if row["terminal"]]
    guided = [row for row in rows if row["guided"]]
    autonomous = [row for row in rows if not row["guided"]]

    return {
        "decisions": len(rows),
        "guided_decisions": len(guided),
        "autonomous_decisions": len(autonomous),
        "agreement_overall": mean([row["agreement"] for row in rows]),
        "agreement_guided": mean([row["agreement"] for row in guided]),
        "agreement_autonomous": mean(
            [row["agreement"] for row in autonomous]
        ),
        "teacher_corrections": sum(row["teacher_used"] for row in rows),
        "training_success_rate": mean(
            [row["success"] for row in terminal]
        ),
    }


def write_csv(path, rows):
    if not rows:
        return

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=list(rows[0].keys()),
        )

        writer.writeheader()
        writer.writerows(rows)


def run_seed(
    *,
    seed,
    train_episodes,
    eval_episodes,
    post_life_episodes,
    guided_span,
    autonomous_span,
    fingerprint_samples,
    name,
):
    founder = new_brain(seed)

    founder_path = OUTPUT_DIR / f"{name}_founder_seed_{seed}.npz"
    founder.save(founder_path)

    result = {
        "seed": seed,
        "arms": {},
        "training_rows": [],
        "post_rows": [],
    }

    for mode in [
        "natural_only",
        "grade_only",
        "corrective_teacher",
    ]:
        brain = Brain.load(founder_path)

        training_rows = run_continuing_life(
            brain,
            mode=mode,
            episodes=train_episodes,
            guided_span=guided_span,
            autonomous_span=autonomous_span,
            seed=seed,
        )

        for row in training_rows:
            out = dict(row)
            out["seed"] = seed
            result["training_rows"].append(out)

        trained_path = OUTPUT_DIR / (
            f"{name}_{mode}_trained_seed_{seed}.npz"
        )

        brain.save(trained_path)

        sampled = Brain.load(trained_path)
        greedy = Brain.load(trained_path)
        fp = Brain.load(trained_path)

        sampled_rows, sampled_actions = eval_cadence(
            sampled,
            eval_episodes,
            greedy=False,
        )

        greedy_rows, greedy_actions = eval_cadence(
            greedy,
            eval_episodes,
            greedy=True,
        )

        immediate = {
            "sampled": summarize(sampled_rows),
            "greedy": summarize(greedy_rows),
            "sampled_actions": action_percent(sampled_actions),
            "greedy_actions": action_percent(greedy_actions),
            "fingerprint": fingerprint(
                fp,
                fingerprint_samples,
            ),
        }

        # Caregiver leaves. Same acquired brain continues learning from only
        # actual world outcomes.
        living = Brain.load(trained_path)

        post_rows = run_continuing_life(
            living,
            mode="natural_only",
            episodes=post_life_episodes,
            guided_span=0,
            autonomous_span=1,
            seed=seed,
        )

        for row in post_rows:
            out = dict(row)
            out["seed"] = seed
            out["source_mode"] = mode
            result["post_rows"].append(out)

        post_path = OUTPUT_DIR / (
            f"{name}_{mode}_after_autonomous_life_seed_{seed}.npz"
        )

        living.save(post_path)

        post_eval = Brain.load(post_path)
        post_fp = Brain.load(post_path)

        post_eval_rows, post_eval_actions = eval_cadence(
            post_eval,
            eval_episodes,
            greedy=False,
        )

        after_life = {
            "sampled": summarize(post_eval_rows),
            "sampled_actions": action_percent(post_eval_actions),
            "fingerprint": fingerprint(
                post_fp,
                fingerprint_samples,
            ),
        }

        result["arms"][mode] = {
            "training": training_metrics(training_rows),
            "immediate": immediate,
            "after_autonomous_life": after_life,
            "post_life_training": training_metrics(post_rows),
        }

    # Founder.
    founder_sampled = Brain.load(founder_path)
    founder_greedy = Brain.load(founder_path)
    founder_fp = Brain.load(founder_path)

    fo_s_rows, fo_s_actions = eval_cadence(
        founder_sampled,
        eval_episodes,
        greedy=False,
    )

    fo_g_rows, fo_g_actions = eval_cadence(
        founder_greedy,
        eval_episodes,
        greedy=True,
    )

    result["arms"]["founder"] = {
        "immediate": {
            "sampled": summarize(fo_s_rows),
            "greedy": summarize(fo_g_rows),
            "sampled_actions": action_percent(fo_s_actions),
            "greedy_actions": action_percent(fo_g_actions),
            "fingerprint": fingerprint(
                founder_fp,
                fingerprint_samples,
            ),
        }
    }

    # Random.
    random_rows, random_actions = eval_random(
        eval_episodes,
        seed,
    )

    result["arms"]["random"] = {
        "immediate": {
            "sampled": summarize(random_rows),
            "sampled_actions": action_percent(random_actions),
        }
    }

    return result


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--train", type=int, default=120)
    parser.add_argument("--eval", type=int, default=100)
    parser.add_argument("--post-life", type=int, default=80)
    parser.add_argument("--guided-span", type=int, default=4)
    parser.add_argument("--autonomous-span", type=int, default=8)
    parser.add_argument("--fingerprint-samples", type=int, default=300)
    parser.add_argument("--seeds", type=int, default=1)
    parser.add_argument("--name", default="quick")

    args = parser.parse_args()

    OUTPUT_DIR.mkdir(exist_ok=True)

    version = pkg_version("cadence-net")

    if version != "0.81.0":
        raise RuntimeError(
            f"V5 requires cadence-net 0.81.0, found {version}"
        )

    print("")
    print("=" * 82)
    print(" CADENCE // STONE AGE V5 — MOCHI-INSPIRED SELECTIVE CAREGIVER")
    print("=" * 82)
    print("cadence-net:", version)
    print("chain: GATHER_WOOD -> GATHER_STONE -> CRAFT_FIRE -> WARM_UP")
    print("one continuing brain per training arm")
    print(
        "caregiver schedule:",
        f"{args.guided_span} guided / "
        f"{args.autonomous_span} autonomous decisions",
    )
    print("train episodes:", args.train)
    print("post-caregiver life:", args.post_life, "episodes")
    print("frozen eval:", args.eval, "episodes")
    print("fresh seeds:", args.seeds)
    print("")

    results = []
    all_training = []
    all_post = []

    for offset in range(args.seeds):
        seed = 42 + offset

        print(f"--- SEED {seed} ---")

        result = run_seed(
            seed=seed,
            train_episodes=args.train,
            eval_episodes=args.eval,
            post_life_episodes=args.post_life,
            guided_span=args.guided_span,
            autonomous_span=args.autonomous_span,
            fingerprint_samples=args.fingerprint_samples,
            name=args.name,
        )

        results.append(result)
        all_training.extend(result["training_rows"])
        all_post.extend(result["post_rows"])

        for arm in [
            "natural_only",
            "grade_only",
            "corrective_teacher",
            "founder",
            "random",
        ]:
            rate = (
                result["arms"][arm]["immediate"]["sampled"]["success_rate"]
                * 100.0
            )

            print(
                f"  {arm:<20} immediate sampled={rate:5.1f}%"
            )

        for arm in [
            "natural_only",
            "grade_only",
            "corrective_teacher",
        ]:
            rate = (
                result["arms"][arm][
                    "after_autonomous_life"
                ]["sampled"]["success_rate"]
                * 100.0
            )

            print(
                f"  {arm:<20} after caregiver leaves={rate:5.1f}%"
            )

        print("")

    write_csv(
        OUTPUT_DIR / f"{args.name}_training_life.csv",
        all_training,
    )

    write_csv(
        OUTPUT_DIR / f"{args.name}_post_teacher_life.csv",
        all_post,
    )

    arms = [
        "natural_only",
        "grade_only",
        "corrective_teacher",
        "founder",
        "random",
    ]

    aggregate = {}

    for arm in arms:
        aggregate[arm] = {
            "immediate_sampled_success": mean([
                result["arms"][arm]["immediate"]["sampled"]["success_rate"]
                for result in results
            ]),
        }

        if arm != "random":
            aggregate[arm]["immediate_greedy_success"] = mean([
                result["arms"][arm]["immediate"]["greedy"]["success_rate"]
                for result in results
            ])

        if arm in {
            "natural_only",
            "grade_only",
            "corrective_teacher",
        }:
            aggregate[arm]["after_life_sampled_success"] = mean([
                result["arms"][arm][
                    "after_autonomous_life"
                ]["sampled"]["success_rate"]
                for result in results
            ])

            aggregate[arm]["training_agreement"] = mean([
                result["arms"][arm]["training"]["agreement_overall"]
                for result in results
            ])

            aggregate[arm]["teacher_corrections"] = mean([
                result["arms"][arm]["training"]["teacher_corrections"]
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
            "train_episodes": args.train,
            "eval_episodes": args.eval,
            "post_teacher_life_episodes": args.post_life,
            "guided_span": args.guided_span,
            "autonomous_span": args.autonomous_span,
            "seeds": args.seeds,
            "continuing_brain": True,
            "wrong_action_keeps_failed_cue": True,
            "target_action_in_observation": False,
            "correction_only_on_disagreement": True,
        },
        "aggregate": aggregate,
        "per_seed": [
            {
                "seed": result["seed"],
                "arms": result["arms"],
            }
            for result in results
        ],
    }

    (
        OUTPUT_DIR / f"{args.name}_summary.json"
    ).write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    report = []

    def add(line=""):
        report.append(str(line))

    add(
        "CADENCE // STONE AGE V5 — MOCHI-INSPIRED SELECTIVE CAREGIVER"
    )
    add("=" * 82)
    add(f"cadence-net: {version}")
    add(
        "One continuing brain per training arm. Guided windows alternate with "
        "autonomous windows."
    )
    add(
        f"Schedule: {args.guided_span} guided / "
        f"{args.autonomous_span} autonomous decisions"
    )
    add(
        "corrective_teacher teaches only after an executed disagreement while "
        "the failed cue remains present."
    )
    add(
        "grade_only never supplies an action label; it only grades the brain's "
        "own executed action during guided windows."
    )
    add("")

    add("FROZEN FULL-CHAIN SUCCESS")

    for arm in arms:
        item = aggregate[arm]

        line = (
            f"  {arm:<20} "
            f"sampled={item['immediate_sampled_success']*100:5.1f}%"
        )

        if arm != "random":
            line += (
                f"  greedy={item['immediate_greedy_success']*100:5.1f}%"
            )

        if "after_life_sampled_success" in item:
            line += (
                "  after-caregiver-life="
                f"{item['after_life_sampled_success']*100:5.1f}%"
            )

        add(line)

    add("")
    add("TRAINING SIGNAL")

    for arm in [
        "natural_only",
        "grade_only",
        "corrective_teacher",
    ]:
        item = aggregate[arm]

        add(
            f"  {arm:<20} "
            f"agreement={item['training_agreement']*100:5.1f}% "
            f"mean_teacher_corrections={item['teacher_corrections']:.1f}"
        )

    add("")
    add("CANONICAL STATE FINGERPRINTS — FIRST SEED")

    first = results[0]

    for arm in [
        "natural_only",
        "grade_only",
        "corrective_teacher",
    ]:
        add("")
        add(f"  {arm}")

        fp = first["arms"][arm]["immediate"]["fingerprint"]

        for situation, _, _ in CANONICAL:
            item = fp[situation]

            add(
                f"    {situation:<14} "
                f"expected={item['expected']:<13} "
                f"sampled={item['sampled_expected_percent']:5.1f}% "
                f"greedy={item['greedy']}"
            )

    add("")
    add("HOW TO READ THIS")
    add(
        "1. Compare corrective_teacher and grade_only against natural_only, "
        "Founder and Random."
    )
    add(
        "2. If corrective_teacher beats grade_only, selective correction is "
        "providing value beyond reward grading."
    )
    add(
        "3. after-caregiver-life measures whether the acquired behavior survives "
        "continued autonomous learning after the caregiver leaves."
    )
    add(
        "4. Useful learning should produce state-dependent fingerprints rather "
        "than one-action collapse."
    )
    add(
        "5. This is Mochi-inspired; it does not reproduce Mochi's full anatomy, "
        "world, mother or complete raising protocol."
    )

    report_text = "\n".join(report)

    (
        OUTPUT_DIR / f"{args.name}_REPORT.txt"
    ).write_text(
        report_text,
        encoding="utf-8",
    )

    print(report_text)
    print("")
    print("Results:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
