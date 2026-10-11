
import os
import sys
import math
import json
import csv
import random
import shutil

import numpy as np
import pygame
from cadence import Brain

# ============================================================
# CADENCE // STONE AGE SURVIVAL
# V1 — Learn to survive one full day and night
# ============================================================

WIDTH = 1920
HEIGHT = 1080

WORLD_W = 1320
BRAIN_X = WORLD_W

FPS = 60
DECISION_INTERVAL = 0.55

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BRAIN_PATH = os.path.join(BASE_DIR, "cadence_stone_age_brain_v1.npz")
BRAIN_BACKUP = os.path.join(BASE_DIR, "cadence_stone_age_brain_v1_backup.npz")
STATS_PATH = os.path.join(BASE_DIR, "cadence_stone_age_stats.json")
CURVE_PATH = os.path.join(BASE_DIR, "cadence_stone_age_runs.csv")

# One game day = 150 real seconds.
DAY_LENGTH_SECONDS = 150.0

# Cadence high-level survival actions.
ACTIONS = [
    "EXPLORE",
    "GATHER_WOOD",
    "GATHER_STONE",
    "PICK_BERRIES",
    "EAT",
    "CRAFT_FIRE",
    "CRAFT_SPEAR",
    "HUNT_RABBIT",
    "BUILD_SHELTER",
    "SLEEP",
    "WARM_UP",
]

# Observation vector length.
INPUTS = 18

# ============================================================
# PYGAME
# ============================================================

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CADENCE // STONE AGE SURVIVAL")

clock = pygame.time.Clock()

FONT_BIG = pygame.font.SysFont("consolas", 36, bold=True)
FONT = pygame.font.SysFont("consolas", 23)
FONT_SMALL = pygame.font.SysFont("consolas", 18)
FONT_TINY = pygame.font.SysFont("consolas", 14)

# ============================================================
# COLORS
# ============================================================

BG = (8, 10, 12)
WORLD_BG = (41, 54, 34)
PANEL = (15, 19, 25)
PANEL_2 = (20, 26, 34)

WHITE = (235, 240, 244)
MUTED = (145, 155, 168)

GREEN = (80, 220, 105)
DARK_GREEN = (41, 112, 58)

BROWN = (127, 87, 54)
DARK_BROWN = (77, 51, 34)

STONE = (125, 130, 134)
BERRY = (151, 70, 180)

CYAN = (62, 204, 255)
YELLOW = (245, 205, 72)
ORANGE = (244, 138, 50)
RED = (232, 72, 72)
BLUE = (78, 130, 225)

# ============================================================
# WORLD
# ============================================================

WORLD = pygame.Rect(30, 90, WORLD_W - 60, HEIGHT - 130)

random.seed(42)

def make_points(count, margin=80):
    pts = []
    for _ in range(count):
        pts.append([
            random.randint(WORLD.left + margin, WORLD.right - margin),
            random.randint(WORLD.top + margin, WORLD.bottom - margin),
        ])
    return pts

TREES = make_points(16)
ROCKS = make_points(10)
BERRY_BUSHES = make_points(8)

RABBITS = []
for _ in range(4):
    x = random.randint(WORLD.left + 100, WORLD.right - 100)
    y = random.randint(WORLD.top + 100, WORLD.bottom - 100)
    RABBITS.append({
        "x": float(x),
        "y": float(y),
        "vx": random.choice([-1, 1]) * random.uniform(20, 42),
        "vy": random.choice([-1, 1]) * random.uniform(20, 42),
        "alive": True,
        "respawn": 0.0,
    })

# ============================================================
# CADENCE BODY / SURVIVAL STATE
# ============================================================

cx = float(WORLD.centerx)
cy = float(WORLD.centery)

HEALTH_MAX = 100.0
HUNGER_MAX = 100.0
WARMTH_MAX = 100.0
ENERGY_MAX = 100.0

health = 100.0
hunger = 100.0
warmth = 100.0
energy = 100.0

wood = 0
stone = 0
berries = 0
raw_meat = 0
cooked_meat = 0

has_spear = False
has_axe = False

fire_exists = False
fire_x = 0.0
fire_y = 0.0
fire_time = 0.0

shelter_exists = False
shelter_x = 0.0
shelter_y = 0.0

sleeping = False
sleep_timer = 0.0

current_action = "WAKE"
last_reward = 0.0
last_event = "Cadence entered the Stone Age."

target_pos = None

run_time = 0.0
world_time = 0.20  # 0..1, 0.0 midnight, 0.25 morning, 0.5 noon, 0.75 evening
day_count = 1
nights_survived = 0
previous_phase = "DAY"

decision_timer = 0.0

# ============================================================
# STATS / MASTERY
# ============================================================

def default_stats():
    return {
        "runs": 0,
        "deaths": 0,
        "best_days": 0.0,
        "total_days": 0.0,
        "nights_survived": 0,

        "food_eaten": 0,
        "fires_built": 0,
        "fires_when_cold": 0,
        "spears_crafted": 0,
        "shelters_built": 0,
        "rabbits_hunted": 0,
        "hunt_attempts": 0,
        "safe_sleeps": 0,
        "sleep_attempts": 0,

        "recent_days": [],

        "skills": {
            "foraging": 0.0,
            "fire": 0.0,
            "hunting": 0.0,
            "shelter": 0.0,
            "sleep": 0.0,
        },

        "mastery": 0.0,
    }

def load_stats():
    if not os.path.exists(STATS_PATH):
        return default_stats()

    try:
        with open(STATS_PATH, "r", encoding="utf-8") as f:
            incoming = json.load(f)

        base = default_stats()

        for key, value in incoming.items():
            if key != "skills":
                base[key] = value

        if isinstance(incoming.get("skills"), dict):
            base["skills"].update(incoming["skills"])

        return base

    except Exception:
        return default_stats()

stats = load_stats()

def save_stats():
    try:
        with open(STATS_PATH, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)
    except Exception as exc:
        print("Stats save failed:", exc)

def ensure_curve():
    if os.path.exists(CURVE_PATH):
        return

    with open(CURVE_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "run",
            "days_survived",
            "nights_survived",
            "cause",
            "food_eaten",
            "fires_built",
            "rabbits_hunted",
            "shelters_built",
            "safe_sleeps",
            "mastery",
        ])

ensure_curve()

def clamp(v, lo=0.0, hi=100.0):
    return max(lo, min(hi, v))

def update_skill_scores():
    food_score = min(
        100.0,
        stats["food_eaten"] * 3.0 +
        stats["nights_survived"] * 4.0
    )

    fire_accuracy = (
        stats["fires_when_cold"] / stats["fires_built"]
        if stats["fires_built"] > 0
        else 0.0
    )

    fire_score = min(
        100.0,
        stats["fires_built"] * 4.0 +
        fire_accuracy * 45.0
    )

    hunt_accuracy = (
        stats["rabbits_hunted"] / stats["hunt_attempts"]
        if stats["hunt_attempts"] > 0
        else 0.0
    )

    hunting_score = min(
        100.0,
        stats["rabbits_hunted"] * 5.0 +
        hunt_accuracy * 40.0
    )

    shelter_score = min(
        100.0,
        stats["shelters_built"] * 12.0 +
        stats["nights_survived"] * 5.0
    )

    sleep_accuracy = (
        stats["safe_sleeps"] / stats["sleep_attempts"]
        if stats["sleep_attempts"] > 0
        else 0.0
    )

    sleep_score = min(
        100.0,
        stats["safe_sleeps"] * 5.0 +
        sleep_accuracy * 45.0
    )

    stats["skills"]["foraging"] = round(food_score, 1)
    stats["skills"]["fire"] = round(fire_score, 1)
    stats["skills"]["hunting"] = round(hunting_score, 1)
    stats["skills"]["shelter"] = round(shelter_score, 1)
    stats["skills"]["sleep"] = round(sleep_score, 1)

    avg_skill = sum(stats["skills"].values()) / len(stats["skills"])

    survival_bonus = min(
        100.0,
        stats["best_days"] * 18.0
    )

    stats["mastery"] = round(
        avg_skill * 0.65 +
        survival_bonus * 0.35,
        1
    )

update_skill_scores()

# ============================================================
# OFFICIAL CADENCE BRAIN
# ============================================================

brain = None
pending = False
pending_reward = 0.0

def create_brain():
    print("CADENCE: creating Stone Age brain...")

    b = Brain.compose(
        inputs=INPUTS,
        actions=len(ACTIONS),
        modules=(32, 16),
        seed=42,
    )

    print("CADENCE: brain ready.")
    return b

def load_brain():
    global brain, pending

    for path in (BRAIN_PATH, BRAIN_BACKUP):
        if not os.path.exists(path):
            continue

        try:
            brain = Brain.load(path)
            pending = False
            print("CADENCE: loaded checkpoint:", path)
            return
        except Exception as exc:
            print("Brain load failed:", exc)

    brain = create_brain()
    pending = False

def save_brain():
    if brain is None:
        return

    try:
        if os.path.exists(BRAIN_PATH):
            try:
                shutil.copy2(BRAIN_PATH, BRAIN_BACKUP)
            except Exception:
                pass

        brain.save(BRAIN_PATH)

    except Exception as exc:
        print("Brain save failed:", exc)

# ============================================================
# WORLD HELPERS
# ============================================================

def distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

def nearest_point(points):
    if not points:
        return None

    return min(
        points,
        key=lambda p: distance(cx, cy, p[0], p[1])
    )

def nearest_rabbit():
    alive = [r for r in RABBITS if r["alive"]]

    if not alive:
        return None

    return min(
        alive,
        key=lambda r: distance(cx, cy, r["x"], r["y"])
    )

def normalized_distance_to(pos):
    if pos is None:
        return 1.0

    d = distance(cx, cy, pos[0], pos[1])
    max_d = math.hypot(WORLD.width, WORLD.height)

    return min(1.0, d / max_d)

def is_night():
    return world_time >= 0.75 or world_time < 0.20

def is_evening():
    return 0.66 <= world_time < 0.75

def phase_name():
    if world_time < 0.20:
        return "NIGHT"
    if world_time < 0.32:
        return "MORNING"
    if world_time < 0.66:
        return "DAY"
    if world_time < 0.75:
        return "EVENING"
    return "NIGHT"

def distance_to_fire():
    if not fire_exists:
        return 9999.0
    return distance(cx, cy, fire_x, fire_y)

def distance_to_shelter():
    if not shelter_exists:
        return 9999.0
    return distance(cx, cy, shelter_x, shelter_y)

# ============================================================
# OBSERVATION
# ============================================================

def observation():
    rabbit = nearest_rabbit()

    tree_d = normalized_distance_to(nearest_point(TREES))
    rock_d = normalized_distance_to(nearest_point(ROCKS))
    berry_d = normalized_distance_to(nearest_point(BERRY_BUSHES))

    rabbit_d = (
        normalized_distance_to((rabbit["x"], rabbit["y"]))
        if rabbit is not None
        else 1.0
    )

    fire_d = (
        min(1.0, distance_to_fire() / 1000.0)
        if fire_exists
        else 1.0
    )

    shelter_d = (
        min(1.0, distance_to_shelter() / 1000.0)
        if shelter_exists
        else 1.0
    )

    inventory_food = min(
        1.0,
        (berries + raw_meat + cooked_meat) / 8.0
    )

    return np.asarray([
        health / 100.0,
        hunger / 100.0,
        warmth / 100.0,
        energy / 100.0,

        world_time,

        min(1.0, wood / 12.0),
        min(1.0, stone / 8.0),
        inventory_food,

        1.0 if has_spear else 0.0,
        1.0 if fire_exists else 0.0,
        1.0 if shelter_exists else 0.0,

        tree_d,
        rock_d,
        berry_d,
        rabbit_d,
        fire_d,
        shelter_d,

        1.0 if is_night() else 0.0,
    ], dtype=np.float64)

# ============================================================
# BODY CONTROLLER
# ============================================================

def move_toward(pos, dt, speed=135.0):
    global cx, cy

    if pos is None:
        return False

    tx, ty = pos

    dx = tx - cx
    dy = ty - cy

    d = math.hypot(dx, dy)

    if d <= 34:
        return True

    if d > 0:
        step = speed * dt

        cx += (dx / d) * min(step, d)
        cy += (dy / d) * min(step, d)

    cx = max(WORLD.left + 20, min(WORLD.right - 20, cx))
    cy = max(WORLD.top + 20, min(WORLD.bottom - 20, cy))

    return False

def wander(dt):
    global cx, cy

    angle = (pygame.time.get_ticks() * 0.00035) % (math.tau)

    cx += math.cos(angle) * 22.0 * dt
    cy += math.sin(angle * 1.37) * 22.0 * dt

    cx = max(WORLD.left + 20, min(WORLD.right - 20, cx))
    cy = max(WORLD.top + 20, min(WORLD.bottom - 20, cy))

# ============================================================
# HIGH-LEVEL ACTION EXECUTION
# ============================================================

action_target = None
action_progress = 0.0

def set_event(text):
    global last_event
    last_event = text

def execute_action(action, dt):
    global wood, stone, berries, raw_meat, cooked_meat
    global hunger, warmth, energy, health

    global has_spear
    global fire_exists, fire_x, fire_y, fire_time
    global shelter_exists, shelter_x, shelter_y
    global sleeping, sleep_timer
    global action_target, action_progress

    reward = 0.003  # small reward for staying alive

    # --------------------------------------------------------
    # EXPLORE
    # --------------------------------------------------------

    if action == "EXPLORE":
        wander(dt)

        energy = clamp(
            energy - 0.16 * dt
        )

        reward += 0.002

    # --------------------------------------------------------
    # GATHER WOOD
    # --------------------------------------------------------

    elif action == "GATHER_WOOD":

        target = nearest_point(TREES)

        if move_toward(target, dt):

            action_progress += dt

            if action_progress >= 1.1:

                wood += 1
                energy = clamp(
                    energy - 1.3
                )

                set_event(
                    "Cadence gathered wood."
                )

                reward += 0.12
                action_progress = 0.0

    # --------------------------------------------------------
    # GATHER STONE
    # --------------------------------------------------------

    elif action == "GATHER_STONE":

        target = nearest_point(ROCKS)

        if move_toward(target, dt):

            action_progress += dt

            if action_progress >= 1.25:

                stone += 1
                energy = clamp(
                    energy - 1.6
                )

                set_event(
                    "Cadence gathered stone."
                )

                reward += 0.13
                action_progress = 0.0

    # --------------------------------------------------------
    # PICK BERRIES
    # --------------------------------------------------------

    elif action == "PICK_BERRIES":

        target = nearest_point(BERRY_BUSHES)

        if move_toward(target, dt):

            action_progress += dt

            if action_progress >= 0.8:

                berries += 1
                energy = clamp(
                    energy - 0.7
                )

                set_event(
                    "Cadence picked berries."
                )

                reward += (
                    0.16
                    if hunger < 65
                    else 0.04
                )

                action_progress = 0.0

    # --------------------------------------------------------
    # EAT
    # --------------------------------------------------------

    elif action == "EAT":

        old_hunger = hunger

        if cooked_meat > 0:

            cooked_meat -= 1
            hunger = clamp(
                hunger + 48
            )

            health = clamp(
                health + 3
            )

            stats["food_eaten"] += 1

            set_event(
                "Cadence ate cooked meat."
            )

            reward += (
                1.1
                if old_hunger < 55
                else 0.12
            )

        elif berries > 0:

            berries -= 1
            hunger = clamp(
                hunger + 18
            )

            stats["food_eaten"] += 1

            set_event(
                "Cadence ate berries."
            )

            reward += (
                0.55
                if old_hunger < 55
                else 0.08
            )

        elif raw_meat > 0:

            raw_meat -= 1
            hunger = clamp(
                hunger + 28
            )

            health = clamp(
                health - 4
            )

            stats["food_eaten"] += 1

            set_event(
                "Cadence ate raw meat."
            )

            reward += (
                0.35
                if old_hunger < 35
                else -0.15
            )

        else:

            reward -= 0.18

    # --------------------------------------------------------
    # CRAFT FIRE
    # --------------------------------------------------------

    elif action == "CRAFT_FIRE":

        if (
            not fire_exists
            and wood >= 4
            and stone >= 2
        ):

            wood -= 4
            stone -= 2

            fire_exists = True
            fire_x = cx
            fire_y = cy
            fire_time = 52.0

            stats["fires_built"] += 1

            useful = (
                warmth < 65
                or is_evening()
                or is_night()
            )

            if useful:
                stats["fires_when_cold"] += 1

            set_event(
                "Cadence discovered fire."
            )

            reward += (
                1.8
                if useful
                else 0.25
            )

        elif fire_exists:

            reward -= 0.06

        else:

            reward -= 0.12

    # --------------------------------------------------------
    # CRAFT SPEAR
    # --------------------------------------------------------

    elif action == "CRAFT_SPEAR":

        if (
            not has_spear
            and wood >= 2
            and stone >= 2
        ):

            wood -= 2
            stone -= 2
            has_spear = True

            stats["spears_crafted"] += 1

            set_event(
                "Cadence crafted a stone spear."
            )

            reward += 0.9

        elif has_spear:
            reward -= 0.05

        else:
            reward -= 0.10

    # --------------------------------------------------------
    # HUNT RABBIT
    # --------------------------------------------------------

    elif action == "HUNT_RABBIT":

        rabbit = nearest_rabbit()

        if rabbit is None:

            reward -= 0.08

        else:

            arrived = move_toward(
                (rabbit["x"], rabbit["y"]),
                dt,
                speed=150.0
            )

            if arrived:

                action_progress += dt

                if action_progress >= 0.55:

                    stats["hunt_attempts"] += 1

                    chance = (
                        0.82
                        if has_spear
                        else 0.18
                    )

                    if random.random() < chance:

                        rabbit["alive"] = False
                        rabbit["respawn"] = 28.0

                        raw_meat += (
                            2
                            if has_spear
                            else 1
                        )

                        stats["rabbits_hunted"] += 1

                        energy = clamp(
                            energy - 5.0
                        )

                        set_event(
                            "Cadence hunted a rabbit."
                        )

                        reward += (
                            1.55
                            if has_spear
                            else 0.65
                        )

                    else:

                        energy = clamp(
                            energy - 4.0
                        )

                        set_event(
                            "The rabbit escaped."
                        )

                        reward -= 0.30

                    action_progress = 0.0

    # --------------------------------------------------------
    # BUILD SHELTER
    # --------------------------------------------------------

    elif action == "BUILD_SHELTER":

        if (
            not shelter_exists
            and wood >= 10
            and stone >= 4
        ):

            wood -= 10
            stone -= 4

            shelter_exists = True
            shelter_x = cx
            shelter_y = cy

            stats["shelters_built"] += 1

            set_event(
                "Cadence built a shelter."
            )

            reward += (
                2.0
                if is_evening() or is_night()
                else 0.75
            )

        elif shelter_exists:
            reward -= 0.04

        else:
            reward -= 0.10

    # --------------------------------------------------------
    # SLEEP
    # --------------------------------------------------------

    elif action == "SLEEP":

        stats["sleep_attempts"] += 1

        safe = (
            shelter_exists
            and distance_to_shelter() < 100
        )

        if safe:

            sleeping = True

            energy = clamp(
                energy + 7.5 * dt
            )

            hunger = clamp(
                hunger - 0.12 * dt
            )

            if is_night():
                reward += 0.20 * dt

            if energy >= 88:

                stats["safe_sleeps"] += 1

                set_event(
                    "Cadence slept safely."
                )

                reward += 1.25

        else:

            # Sleeping outside is possible but risky.
            sleeping = True

            energy = clamp(
                energy + 4.0 * dt
            )

            if is_night():
                warmth = clamp(
                    warmth - 1.8 * dt
                )

            reward -= 0.06 * dt

    # --------------------------------------------------------
    # WARM UP
    # --------------------------------------------------------

    elif action == "WARM_UP":

        if fire_exists:

            arrived = move_toward(
                (fire_x, fire_y),
                dt
            )

            if arrived:

                old = warmth

                warmth = clamp(
                    warmth + 10.0 * dt
                )

                if old < 60:
                    reward += 0.22 * dt

        else:

            reward -= 0.12

    return reward

# ============================================================
# WORLD SIMULATION
# ============================================================

def update_rabbits(dt):
    for rabbit in RABBITS:

        if not rabbit["alive"]:

            rabbit["respawn"] -= dt

            if rabbit["respawn"] <= 0:

                rabbit["alive"] = True
                rabbit["x"] = random.randint(
                    WORLD.left + 90,
                    WORLD.right - 90
                )
                rabbit["y"] = random.randint(
                    WORLD.top + 90,
                    WORLD.bottom - 90
                )

            continue

        # Rabbits wander and flee from Cadence.
        d = distance(
            rabbit["x"],
            rabbit["y"],
            cx,
            cy
        )

        if d < 140:

            dx = rabbit["x"] - cx
            dy = rabbit["y"] - cy

            length = max(
                1.0,
                math.hypot(dx, dy)
            )

            rabbit["vx"] = (
                dx / length
            ) * 82

            rabbit["vy"] = (
                dy / length
            ) * 82

        rabbit["x"] += rabbit["vx"] * dt
        rabbit["y"] += rabbit["vy"] * dt

        if rabbit["x"] < WORLD.left + 30 or rabbit["x"] > WORLD.right - 30:
            rabbit["vx"] *= -1

        if rabbit["y"] < WORLD.top + 30 or rabbit["y"] > WORLD.bottom - 30:
            rabbit["vy"] *= -1

        rabbit["x"] = max(
            WORLD.left + 30,
            min(WORLD.right - 30, rabbit["x"])
        )

        rabbit["y"] = max(
            WORLD.top + 30,
            min(WORLD.bottom - 30, rabbit["y"])
        )

def update_survival(dt):
    global health, hunger, warmth, energy
    global world_time, run_time
    global day_count, nights_survived, previous_phase
    global fire_exists, fire_time
    global pending_reward

    run_time += dt

    # Day progression.
    old_time = world_time

    world_time += dt / DAY_LENGTH_SECONDS

    if world_time >= 1.0:

        world_time -= 1.0
        day_count += 1

    # Fire burns out.
    if fire_exists:

        fire_time -= dt

        if fire_time <= 0:
            fire_exists = False

    # Core needs.
    hunger = clamp(
        hunger - 0.52 * dt
    )

    energy = clamp(
        energy - 0.26 * dt
    )

    # Temperature / warmth.
    if is_night():

        warmth = clamp(
            warmth - 0.70 * dt
        )

    elif is_evening():

        warmth = clamp(
            warmth - 0.20 * dt
        )

    else:

        warmth = clamp(
            warmth + 0.16 * dt
        )

    # Fire warmth.
    if (
        fire_exists
        and distance_to_fire() < 130
    ):

        warmth = clamp(
            warmth + 2.5 * dt
        )

    # Shelter slows cold loss.
    if (
        shelter_exists
        and distance_to_shelter() < 120
        and is_night()
    ):

        warmth = clamp(
            warmth + 0.22 * dt
        )

    # Damage.
    damage = 0.0

    if hunger <= 5:
        damage += 2.6 * dt

    if warmth <= 8:
        damage += 3.4 * dt

    if energy <= 3:
        damage += 1.4 * dt

    if damage > 0:

        health = clamp(
            health - damage
        )

        pending_reward -= (
            damage * 0.12
        )

    # Detect surviving a night -> morning.
    phase = phase_name()

    if (
        previous_phase == "NIGHT"
        and phase == "MORNING"
    ):

        nights_survived += 1
        stats["nights_survived"] += 1

        pending_reward += 5.0

        set_event(
            "Cadence survived the night."
        )

        update_skill_scores()

    previous_phase = phase

# ============================================================
# CADENCE DECISION LOOP
# ============================================================

def cadence_step(dt):
    global pending, pending_reward
    global current_action, last_reward
    global action_progress, sleeping

    sleeping = False

    obs = observation().reshape(
        1,
        INPUTS
    )

    try:

        if pending:

            result = brain.step(
                obs,
                reward=np.asarray(
                    [float(pending_reward)],
                    dtype=np.float64
                ),
                done=np.asarray(
                    [False],
                    dtype=bool
                ),
            )

        else:

            result = brain.step(obs)

        action_index = int(
            np.asarray(result).reshape(-1)[0]
        )

        action_index = max(
            0,
            min(
                len(ACTIONS) - 1,
                action_index
            )
        )

        new_action = ACTIONS[
            action_index
        ]

        if new_action != current_action:
            action_progress = 0.0

        current_action = new_action

        pending = True
        pending_reward = 0.0

    except Exception as exc:

        print(
            "Cadence decision failed:",
            exc
        )

def execute_current_action(dt):
    global last_reward, pending_reward

    reward = execute_action(
        current_action,
        dt
    )

    last_reward = reward
    pending_reward += reward

# ============================================================
# DEATH / RESET
# ============================================================

death_timer = 0.0
death_cause = ""

def detect_death():
    if health > 0:
        return None

    if hunger <= 5:
        return "STARVATION"

    if warmth <= 8:
        return "HYPOTHERMIA"

    if energy <= 3:
        return "EXHAUSTION"

    return "SURVIVAL FAILURE"

def finish_run(cause):
    global pending, pending_reward
    global death_timer, death_cause

    days_survived = (
        run_time /
        DAY_LENGTH_SECONDS
    )

    # Close the current Cadence action as terminal.
    try:
        if pending:
            brain.step(
                observation().reshape(
                    1,
                    INPUTS
                ),
                reward=np.asarray(
                    [-10.0],
                    dtype=np.float64
                ),
                done=np.asarray(
                    [True],
                    dtype=bool
                ),
            )
    except Exception:
        pass

    pending = False
    pending_reward = 0.0

    stats["runs"] += 1
    stats["deaths"] += 1

    stats["total_days"] += (
        days_survived
    )

    stats["best_days"] = max(
        stats["best_days"],
        days_survived
    )

    stats["recent_days"] = (
        stats["recent_days"] +
        [round(days_survived, 3)]
    )[-20:]

    update_skill_scores()

    with open(
        CURVE_PATH,
        "a",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            stats["runs"],
            round(days_survived, 3),
            nights_survived,
            cause,
            stats["food_eaten"],
            stats["fires_built"],
            stats["rabbits_hunted"],
            stats["shelters_built"],
            stats["safe_sleeps"],
            stats["mastery"],
        ])

    save_stats()
    save_brain()

    death_cause = cause
    death_timer = 2.0

def reset_run():
    global cx, cy
    global health, hunger, warmth, energy
    global wood, stone, berries, raw_meat, cooked_meat
    global has_spear, has_axe
    global fire_exists, fire_time
    global shelter_exists
    global sleeping
    global run_time, world_time, day_count, nights_survived, previous_phase
    global current_action, last_reward, last_event
    global pending, pending_reward
    global action_progress

    cx = float(WORLD.centerx)
    cy = float(WORLD.centery)

    health = 100.0
    hunger = 100.0
    warmth = 100.0
    energy = 100.0

    wood = 0
    stone = 0
    berries = 0
    raw_meat = 0
    cooked_meat = 0

    has_spear = False
    has_axe = False

    fire_exists = False
    fire_time = 0.0

    shelter_exists = False

    sleeping = False

    run_time = 0.0
    world_time = 0.20
    day_count = 1
    nights_survived = 0
    previous_phase = "DAY"

    current_action = "WAKE"
    last_reward = 0.0
    last_event = "A new Stone Age life begins."

    pending = False
    pending_reward = 0.0

    action_progress = 0.0

# ============================================================
# DRAWING HELPERS
# ============================================================

def draw_text(text, x, y, font=FONT_SMALL, color=WHITE):
    screen.blit(
        font.render(
            str(text),
            True,
            color
        ),
        (x, y)
    )

def draw_bar(
    label,
    value,
    x,
    y,
    width=210,
    color=GREEN
):
    draw_text(
        label,
        x,
        y - 2,
        FONT_TINY,
        MUTED
    )

    bar = pygame.Rect(
        x,
        y + 18,
        width,
        15
    )

    pygame.draw.rect(
        screen,
        (36, 41, 48),
        bar,
        border_radius=7
    )

    fill = bar.copy()

    fill.width = int(
        width *
        max(
            0.0,
            min(1.0, value / 100.0)
        )
    )

    pygame.draw.rect(
        screen,
        color,
        fill,
        border_radius=7
    )

def draw_world():
    # Sky/time tint.
    if is_night():
        base = (22, 29, 29)
    elif is_evening():
        base = (66, 66, 36)
    else:
        base = WORLD_BG

    pygame.draw.rect(
        screen,
        base,
        WORLD,
        border_radius=18
    )

    # Ground texture.
    for gx in range(
        WORLD.left + 20,
        WORLD.right,
        70
    ):
        pygame.draw.line(
            screen,
            (47, 60, 40),
            (gx, WORLD.top),
            (gx, WORLD.bottom),
            1
        )

    for gy in range(
        WORLD.top + 20,
        WORLD.bottom,
        70
    ):
        pygame.draw.line(
            screen,
            (47, 60, 40),
            (WORLD.left, gy),
            (WORLD.right, gy),
            1
        )

    # Trees.
    for x, y in TREES:

        pygame.draw.rect(
            screen,
            DARK_BROWN,
            (x - 6, y + 4, 12, 30),
            border_radius=4
        )

        pygame.draw.circle(
            screen,
            DARK_GREEN,
            (x, y),
            28
        )

        pygame.draw.circle(
            screen,
            (60, 145, 67),
            (x - 6, y - 7),
            21
        )

    # Rocks.
    for x, y in ROCKS:

        pygame.draw.polygon(
            screen,
            STONE,
            [
                (x - 24, y + 15),
                (x - 14, y - 18),
                (x + 15, y - 22),
                (x + 28, y + 8),
                (x + 7, y + 22),
            ]
        )

    # Berry bushes.
    for x, y in BERRY_BUSHES:

        pygame.draw.circle(
            screen,
            (54, 119, 63),
            (x, y),
            22
        )

        for ox, oy in (
            (-8, -5),
            (7, -9),
            (-2, 8),
            (10, 7),
        ):

            pygame.draw.circle(
                screen,
                BERRY,
                (x + ox, y + oy),
                4
            )

    # Rabbits.
    for rabbit in RABBITS:

        if not rabbit["alive"]:
            continue

        rx = int(rabbit["x"])
        ry = int(rabbit["y"])

        pygame.draw.ellipse(
            screen,
            (205, 195, 175),
            (rx - 13, ry - 8, 26, 17)
        )

        pygame.draw.ellipse(
            screen,
            (220, 211, 192),
            (rx + 5, ry - 18, 5, 14)
        )

        pygame.draw.ellipse(
            screen,
            (220, 211, 192),
            (rx - 2, ry - 19, 5, 15)
        )

    # Shelter.
    if shelter_exists:

        sx = int(shelter_x)
        sy = int(shelter_y)

        pygame.draw.polygon(
            screen,
            (108, 82, 54),
            [
                (sx - 38, sy + 30),
                (sx, sy - 36),
                (sx + 38, sy + 30),
            ]
        )

        pygame.draw.rect(
            screen,
            (66, 48, 35),
            (sx - 10, sy + 4, 20, 26)
        )

    # Fire.
    if fire_exists:

        fx = int(fire_x)
        fy = int(fire_y)

        # Glow.
        glow = pygame.Surface(
            (220, 220),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            glow,
            (255, 125, 35, 34),
            (110, 110),
            100
        )

        screen.blit(
            glow,
            (fx - 110, fy - 110)
        )

        pygame.draw.line(
            screen,
            BROWN,
            (fx - 15, fy + 14),
            (fx + 15, fy - 7),
            7
        )

        pygame.draw.line(
            screen,
            BROWN,
            (fx + 15, fy + 14),
            (fx - 15, fy - 7),
            7
        )

        flame_h = int(
            26 +
            math.sin(
                pygame.time.get_ticks() *
                0.012
            ) * 5
        )

        pygame.draw.polygon(
            screen,
            ORANGE,
            [
                (fx, fy - flame_h),
                (fx - 13, fy + 11),
                (fx + 13, fy + 11),
            ]
        )

        pygame.draw.polygon(
            screen,
            YELLOW,
            [
                (fx, fy - flame_h + 8),
                (fx - 7, fy + 8),
                (fx + 7, fy + 8),
            ]
        )

    # Cadence shadow.
    pygame.draw.ellipse(
        screen,
        (9, 11, 10),
        (
            int(cx - 18),
            int(cy + 12),
            36,
            14
        )
    )

    # Primitive Cadence character.
    pygame.draw.circle(
        screen,
        (205, 175, 132),
        (int(cx), int(cy - 19)),
        10
    )

    pygame.draw.rect(
        screen,
        (96, 63, 42),
        (
            int(cx - 11),
            int(cy - 9),
            22,
            29
        ),
        border_radius=5
    )

    # Spear visual.
    if has_spear:

        pygame.draw.line(
            screen,
            (126, 93, 55),
            (
                int(cx + 5),
                int(cy + 3)
            ),
            (
                int(cx + 36),
                int(cy - 34)
            ),
            4
        )

        pygame.draw.polygon(
            screen,
            STONE,
            [
                (
                    int(cx + 36),
                    int(cy - 34)
                ),
                (
                    int(cx + 30),
                    int(cy - 22)
                ),
                (
                    int(cx + 42),
                    int(cy - 26)
                ),
            ]
        )

    draw_text(
        "CADENCE",
        int(cx - 35),
        int(cy - 58),
        FONT_TINY,
        CYAN
    )

def brain_shape(cx, cy, scale):
    pts = [
        (-88,-62), (-62,-88), (-25,-101),
        (12,-99), (48,-83), (78,-58),
        (98,-21), (96,15), (82,48),
        (57,75), (22,88), (-12,89),
        (-45,80), (-75,59), (-96,27),
        (-102,-10), (-97,-40)
    ]

    return [
        (
            int(cx + px * scale),
            int(cy + py * scale)
        )
        for px, py in pts
    ]

def draw_brain_panel():
    panel = pygame.Rect(
        BRAIN_X + 20,
        22,
        WIDTH - BRAIN_X - 40,
        HEIGHT - 44
    )

    pygame.draw.rect(
        screen,
        PANEL_2,
        panel,
        border_radius=24
    )

    pygame.draw.rect(
        screen,
        (40, 51, 65),
        panel,
        2,
        border_radius=24
    )

    draw_text(
        "CADENCE BRAIN",
        BRAIN_X + 52,
        52,
        FONT_BIG,
        CYAN
    )

    draw_text(
        "Stone Age survival learning",
        BRAIN_X + 54,
        96,
        FONT_SMALL,
        MUTED
    )

    mastery = stats["mastery"]

    brain_scale = (
        0.48 +
        (mastery / 100.0) *
        0.90
    )

    bcx = BRAIN_X + 300
    bcy = 300

    outline = brain_shape(
        bcx,
        bcy,
        brain_scale
    )

    pygame.draw.polygon(
        screen,
        (23, 49, 58),
        outline
    )

    pygame.draw.polygon(
        screen,
        CYAN,
        outline,
        3
    )

    # Nodes increase with mastery.
    node_count = (
        7 +
        int(
            mastery / 4.0
        )
    )

    rng = random.Random(9001)

    nodes = []

    for _ in range(node_count):

        angle = rng.uniform(
            0,
            math.tau
        )

        rx = rng.uniform(
            16,
            72
        ) * brain_scale

        ry = rng.uniform(
            13,
            60
        ) * brain_scale

        nodes.append(
            (
                int(
                    bcx +
                    math.cos(angle) *
                    rx
                ),
                int(
                    bcy +
                    math.sin(angle) *
                    ry
                )
            )
        )

    for i in range(
        len(nodes)
    ):

        for j in range(
            i + 1,
            min(
                i + 4,
                len(nodes)
            )
        ):

            pygame.draw.line(
                screen,
                (38, 108, 141),
                nodes[i],
                nodes[j],
                1
            )

    pulse = (
        pygame.time.get_ticks() //
        180
    ) % max(
        1,
        len(nodes)
    )

    for i, p in enumerate(nodes):

        pygame.draw.circle(
            screen,
            WHITE
            if i == pulse
            else CYAN,
            p,
            6
            if i == pulse
            else 4
        )

    draw_text(
        f"OVERALL MASTERY  {mastery:0.1f}%",
        BRAIN_X + 52,
        454,
        FONT,
        WHITE
    )

    # Current thought.
    draw_text(
        "CURRENT THOUGHT",
        BRAIN_X + 52,
        505,
        FONT,
        YELLOW
    )

    draw_text(
        current_action,
        BRAIN_X + 52,
        542,
        FONT_BIG,
        WHITE
    )

    draw_text(
        last_event[:43],
        BRAIN_X + 52,
        590,
        FONT_TINY,
        MUTED
    )

    # Skill bars.
    draw_text(
        "LEARNED SKILLS",
        BRAIN_X + 52,
        636,
        FONT,
        YELLOW
    )

    skill_rows = [
        (
            "Foraging",
            stats["skills"]["foraging"],
            GREEN
        ),
        (
            "Fire",
            stats["skills"]["fire"],
            ORANGE
        ),
        (
            "Hunting",
            stats["skills"]["hunting"],
            RED
        ),
        (
            "Shelter",
            stats["skills"]["shelter"],
            BROWN
        ),
        (
            "Sleep",
            stats["skills"]["sleep"],
            BLUE
        ),
    ]

    y = 680

    for label, value, color in skill_rows:

        draw_bar(
            label,
            value,
            BRAIN_X + 54,
            y,
            width=245,
            color=color
        )

        draw_text(
            f"{value:0.0f}%",
            BRAIN_X + 315,
            y + 13,
            FONT_TINY,
            WHITE
        )

        y += 58

    draw_text(
        "Brain growth = measured mastery",
        BRAIN_X + 52,
        997,
        FONT_TINY,
        MUTED
    )

    draw_text(
        "not literal physical brain size",
        BRAIN_X + 52,
        1019,
        FONT_TINY,
        MUTED
    )

def draw_hud():
    draw_text(
        "CADENCE // STONE AGE SURVIVAL",
        42,
        28,
        FONT_BIG,
        WHITE
    )

    draw_text(
        f"DAY {day_count}  •  {phase_name()}",
        44,
        69,
        FONT_SMALL,
        YELLOW
        if not is_night()
        else CYAN
    )

    # Needs panel.
    draw_bar(
        "HEALTH",
        health,
        55,
        118,
        175,
        GREEN
    )

    draw_bar(
        "HUNGER",
        hunger,
        245,
        118,
        175,
        ORANGE
    )

    draw_bar(
        "WARMTH",
        warmth,
        435,
        118,
        175,
        CYAN
    )

    draw_bar(
        "ENERGY",
        energy,
        625,
        118,
        175,
        YELLOW
    )

    # Inventory.
    inv_x = 842

    draw_text(
        "INVENTORY",
        inv_x,
        116,
        FONT_SMALL,
        WHITE
    )

    draw_text(
        (
            f"Wood {wood}   Stone {stone}   "
            f"Berries {berries}   Meat {raw_meat}/{cooked_meat}"
        ),
        inv_x,
        147,
        FONT_TINY,
        MUTED
    )

    draw_text(
        (
            f"Spear {'YES' if has_spear else 'NO'}   "
            f"Fire {'YES' if fire_exists else 'NO'}   "
            f"Shelter {'YES' if shelter_exists else 'NO'}"
        ),
        inv_x,
        170,
        FONT_TINY,
        MUTED
    )

# ============================================================
# START / MAIN LOOP
# ============================================================

load_brain()

running = True

while running:

    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            running = False

    if death_timer > 0:

        death_timer -= dt

        if death_timer <= 0:
            reset_run()

    else:

        update_rabbits(dt)
        update_survival(dt)

        decision_timer -= dt

        if decision_timer <= 0:

            decision_timer = (
                DECISION_INTERVAL
            )

            cadence_step(dt)

        execute_current_action(dt)

        cause = detect_death()

        if cause is not None:
            finish_run(cause)

    # Draw.
    screen.fill(BG)

    draw_world()
    draw_hud()

    pygame.draw.line(
        screen,
        (43, 54, 68),
        (BRAIN_X, 0),
        (BRAIN_X, HEIGHT),
        2
    )

    draw_brain_panel()

    # Reward/status strip.
    draw_text(
        f"Reward {last_reward:+0.3f}",
        42,
        HEIGHT - 31,
        FONT_TINY,
        WHITE
    )

    draw_text(
        f"Run {stats['runs'] + 1}",
        210,
        HEIGHT - 31,
        FONT_TINY,
        WHITE
    )

    draw_text(
        f"Best {stats['best_days']:.2f} days",
        330,
        HEIGHT - 31,
        FONT_TINY,
        WHITE
    )

    if death_timer > 0:

        overlay = pygame.Surface(
            (WORLD_W, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 125)
        )

        screen.blit(
            overlay,
            (0, 0)
        )

        msg = FONT_BIG.render(
            "CADENCE DIED",
            True,
            RED
        )

        sub = FONT.render(
            death_cause,
            True,
            WHITE
        )

        screen.blit(
            msg,
            msg.get_rect(
                center=(
                    WORLD_W // 2,
                    HEIGHT // 2 - 24
                )
            )
        )

        screen.blit(
            sub,
            sub.get_rect(
                center=(
                    WORLD_W // 2,
                    HEIGHT // 2 + 28
                )
            )
        )

    pygame.display.flip()

# Save current continuation state.
if brain is not None and pending:

    try:

        brain.step(
            observation().reshape(
                1,
                INPUTS
            ),
            reward=np.asarray(
                [float(pending_reward)],
                dtype=np.float64
            ),
            done=np.asarray(
                [True],
                dtype=bool
            ),
        )

    except Exception:
        pass

update_skill_scores()
save_stats()
save_brain()

pygame.quit()
sys.exit()
