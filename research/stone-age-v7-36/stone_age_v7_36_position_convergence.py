"""Cadence Stone Age V7.36 — Position Convergence / Dose Scaling.

V7.31 proved the additive P+length position representation can express the exact variable-
length predecessor rule. V7.33-V7.35 then progressively removed target error, P_c, and content-
address learning; the cleanest exact-teacher arm still reached only ~79% BASE at 198 examples
per (length,position) pair while FORCE_PREDECESSOR remained 100%.

V7.36 asks whether that residual gap is a structural ceiling or simply finite-dose convergence
of the released online position-map optimizer.

A single brain per founder trains continuously with the clean V7.35 configuration:
  * cadence-net 0.91.1
  * exact one-hot predecessor position teacher
  * recall_address=0.0 (content-address map frozen)
  * position P_c frozen at zero
  * recall_position_rate=0.10
  * native recall_boundary=True
  * BLOCK_VALUE_TRAIN to keep the behavioral readout on predecessor->next

The same brain is evaluated at cumulative exact-balanced doses of 198, 396, and 792 examples
per one of the 22 variable-length pairs. No test-time intervention is used in BASE.
"""
from __future__ import annotations

import argparse, csv, json, statistics, types, warnings
from contextlib import contextmanager
from importlib.metadata import version as pkg_version
from pathlib import Path

import numpy as np
import cadence as cd
import stone_age_v7_21_variable_length as v721

VERSION = "0.91.1"
FOUNDER_START = 102001
DEFAULT_FOUNDERS = 8
MIN_VALID = 6
LENGTHS = (3, 4, 5, 6, 7)
PAIRS = v721.variable_pairs()
N_PAIRS = len(PAIRS)
CHECKPOINTS = (198, 396, 792)
STAGE_PER_PAIR = (198, 198, 396)
CAL_PER_PAIR = 20
CAL_EPISODES = CAL_PER_PAIR * N_PAIRS
TEST_PER_PAIR = 50
TEST_EPISODES = TEST_PER_PAIR * N_PAIRS
EVENT_INPUTS = 4
POSITION_INPUTS = 5
CONTEXT_INPUTS = 5
POSITION_OFFSET = EVENT_INPUTS
CONTEXT_OFFSET = POSITION_OFFSET + POSITION_INPUTS
INPUTS = CONTEXT_OFFSET + CONTEXT_INPUTS
N_ACTIONS = 4
POSITION_RATE = 0.10
LEARNING_FREE_STEPS = 4096
FORCE_LOGIT = 50.0
ROUTE_MARGIN = 0.15
CONDS = ("BASE", "FORCE_PREDECESSOR", "FORCE_TARGET")


def median(xs):
    xs = list(xs)
    return statistics.median(xs) if xs else 0.0


def mean(xs):
    xs = list(xs)
    return statistics.fmean(xs) if xs else 0.0


def one_hot(i: int):
    x = np.zeros((1, INPUTS), dtype=np.float64)
    x[0, int(i)] = 1.0
    return x


def event_vector(resource: int):
    return one_hot(int(resource))


def query_vector(ep: v721.Episode):
    x = np.zeros((1, INPUTS), dtype=np.float64)
    x[0, POSITION_OFFSET + ep.query_position] = 1.0
    x[0, CONTEXT_OFFSET + (ep.length - LENGTHS[0])] = 1.0
    return x


def query_vector_pair(length: int, q: int):
    x = np.zeros((1, INPUTS), dtype=np.float64)
    x[0, POSITION_OFFSET + q] = 1.0
    x[0, CONTEXT_OFFSET + (length - LENGTHS[0])] = 1.0
    return x


def predecessor_age(ep: v721.Episode):
    return int(ep.length - ep.query_position)


def target_age(ep: v721.Episode):
    return predecessor_age(ep) - 1


def compose(founder: int):
    brain = cd.Brain.compose(
        inputs=INPUTS,
        actions=N_ACTIONS,
        modules=(24,),
        seed=founder,
        episodic=False,
        teaching="normalized",
        learning_free_steps=LEARNING_FREE_STEPS,
        recall=True,
        recall_address=0.0,
        recall_position=32,
        recall_position_rate=POSITION_RATE,
        recall_recency=0.0,
        recall_temperature=0.25,
        recall_boundary=True,
    )
    if abs(float(brain.recall.address)) > 1e-12:
        raise AssertionError(("recall_address mismatch", brain.recall.address))
    if abs(float(brain.recall.position_rate) - POSITION_RATE) > 1e-12:
        raise AssertionError(("position_rate mismatch", brain.recall.position_rate))
    if int(brain.learner.config.free_steps) != LEARNING_FREE_STEPS:
        raise AssertionError(("learning_free_steps mismatch", brain.learner.config.free_steps))
    return brain


def _make_panel(founder: int, phase: int, per_pair: int):
    rng = np.random.default_rng(np.random.SeedSequence([founder, 736, phase, per_pair]))
    schedule = PAIRS * per_pair
    rng.shuffle(schedule)
    out = []
    for length, q in schedule:
        events = v721.make_stream(rng, length, q)
        out.append(v721.Episode(events, q, int(events[q]), length))
    return out


def make_stage(founder: int, stage_index: int, per_pair: int):
    return _make_panel(founder, 10 + stage_index, per_pair)


def make_cal(founder: int):
    return _make_panel(founder, 20, CAL_PER_PAIR)


def make_test(founder: int):
    return _make_panel(founder, 30, TEST_PER_PAIR)


def hear(brain: cd.Brain, ep: v721.Episode):
    brain.reset()
    for e in ep.events:
        brain.act(event_vector(e), greedy=True)


def _address_map_max_abs(brain):
    wx, wc, b = brain.recall.head_map(0)
    return float(max(np.max(np.abs(np.asarray(wx))), np.max(np.abs(np.asarray(wc))), np.max(np.abs(np.asarray(b)))))


def install_exact_position_teacher(brain: cd.Brain, state: dict):
    """Exact one-hot predecessor p* using the released 0.91.1 gradient and energy bound.

    P_c is deliberately frozen at zero, but the released energy normalization still includes
    cortex energy, exactly matching the clean V7.35 ADDR_OFF_PC_OFF arm. Thus V7.36 changes
    only cumulative dose.
    """
    recall = brain.recall

    def exact_step(self, moment, rows, d_value, d_next, head, found=None):
        if found is None:
            found = self._row_steps(moment, rows, d_value, d_next, head)
        if found is None:
            return 0, 0
        _, x, c, _, _, _, _, prior_log = found
        if len(x) != 1 or len(rows) != 1:
            raise AssertionError("V7.36 exact teacher requires batch=1 lessons")
        ep = state.get("episode")
        if ep is None:
            raise AssertionError("V7.36 exact teacher missing current episode")
        row = int(rows[0])
        held = np.asarray(self.held[row:row + 1])
        pred_slot = int(ep.query_position)
        if pred_slot >= held.shape[1] or not bool(held[0, pred_slot]):
            raise AssertionError(("predecessor slot not held", pred_slot, held.shape, held.tolist()))

        target = np.zeros_like(np.asarray(prior_log), dtype=float)
        target[0, pred_slot] = 1.0
        state["teacher_rows"] += 1
        if int(np.argmax(target[0])) == pred_slot:
            state["teacher_correct"] += 1

        prior = np.exp(prior_log)
        rate = float(self.position_rate)
        count = self.position_buckets
        p_x, p_c, p = self.position_maps[head]
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            gradient = np.where(np.isfinite(prior_log), target - prior, 0.0)
            terms = np.zeros((len(gradient), count))
            np.add.at(terms, (np.arange(len(gradient))[:, None], self.buckets()[None, :]), gradient)
            energy = np.einsum("bi,bi->b", x, x) + np.einsum("bi,bi->b", c, c) + 1.0
            step = terms * np.minimum(1.0, 1.0 / (rate * energy))[:, None]
            maps = (
                p_x + rate * x.T @ step / len(x),
                p_c,  # frozen at zero
                p + rate * step.mean(axis=0),
            )
        if not all(np.isfinite(a).all() for a in maps):
            return 0, int(len(x))
        self.position_maps = [maps if h == head else kept for h, kept in enumerate(self.position_maps)]
        return int(len(x)), 0

    recall._position_step = types.MethodType(exact_step, recall)


def train_stage(brain, episodes, state):
    out = {"lessons": 0, "runtime_errors": []}
    for ep in episodes:
        state["episode"] = ep
        try:
            hear(brain, ep)
            qx = query_vector(ep)
            brain.recall.values[...] = 0.0
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                brain.lesson(qx, np.asarray([ep.label]))
                brain.act(qx, greedy=True)
            out["lessons"] += 1
        except Exception as exc:
            out["runtime_errors"].append(f"{type(exc).__name__}: {exc}")
            break
    state["episode"] = None
    return out


@contextmanager
def forced_age(brain: cd.Brain, age: int | None):
    if age is None:
        yield
        return
    maps = brain.recall.position_map(0)
    saved = [np.asarray(a).copy() for a in maps]
    try:
        px, pc, p = maps
        px[...] = 0.0
        pc[...] = 0.0
        p[...] = -FORCE_LOGIT
        if not (0 <= int(age) < len(p)):
            raise ValueError(f"age {age} outside position buckets")
        p[int(age)] = FORCE_LOGIT
        yield
    finally:
        for dst, src in zip(maps, saved, strict=True):
            dst[...] = src


def route_from_records(records):
    pred = mean(r["top_is_predecessor"] for r in records)
    targ = mean(r["top_is_target"] for r in records)
    delta = pred - targ
    return {
        "top_predecessor_rate": pred,
        "top_target_rate": targ,
        "delta": delta,
        "preferred_route": "NEXT_ROUTE" if delta >= 0 else "VALUE_ROUTE",
        "clear": int(abs(delta) >= ROUTE_MARGIN),
    }


def eval_condition(brain, episodes, condition, checkpoint, panel="TEST"):
    hits = 0
    errors = []
    records = []
    lh = {l: 0 for l in LENGTHS}; lc = {l: 0 for l in LENGTHS}
    ph = {q: 0 for q in range(5)}; pcnt = {q: 0 for q in range(5)}
    pair_hits = {f"L{l}_P{q+1}": 0 for l, q in PAIRS}
    pair_counts = {k: 0 for k in pair_hits}
    try:
        for ti, ep in enumerate(episodes):
            hear(brain, ep)
            qx = query_vector(ep)
            age = None
            if condition == "FORCE_PREDECESSOR":
                age = predecessor_age(ep)
            elif condition == "FORCE_TARGET":
                age = target_age(ep)
            elif condition != "BASE":
                raise ValueError(condition)
            with forced_age(brain, age):
                ans = int(np.asarray(brain.act(qx, greedy=True)).reshape(-1)[0])
            ans = max(0, min(N_ACTIONS - 1, ans))
            ok = int(ans == ep.label)
            hits += ok
            lh[ep.length] += ok; lc[ep.length] += 1
            ph[ep.query_position] += ok; pcnt[ep.query_position] += 1
            pair = f"L{ep.length}_P{ep.query_position+1}"
            pair_hits[pair] += ok; pair_counts[pair] += 1
            w = [] if brain.recall.attended is None else np.asarray(brain.recall.attended, dtype=float).reshape(-1).tolist()
            top = int(np.argmax(w)) if w else -1
            pred = ep.query_position
            target = ep.query_position + 1
            records.append({
                "checkpoint": checkpoint, "panel": panel, "condition": condition,
                "test_index": ti, "length": ep.length, "query": f"P{ep.query_position+1}",
                "correct": ok, "top_is_predecessor": int(top == pred),
                "top_is_target": int(top == target), "top_weight": float(w[top]) if top >= 0 else 0.0,
                "predecessor_weight": float(w[pred]) if w and pred < len(w) else 0.0,
                "target_weight": float(w[target]) if w and target < len(w) else 0.0,
            })
    except Exception as exc:
        errors.append(f"{type(exc).__name__}: {exc}")
    expected = len(episodes) // N_PAIRS
    balanced = len(episodes) % N_PAIRS == 0 and all(v == expected for v in pair_counts.values())
    return ({
        "valid": int(not errors and balanced and len(records) == len(episodes)),
        "accuracy": hits / len(episodes) if episodes else 0.0,
        "per_length": {f"L{l}": lh[l] / lc[l] if lc[l] else 0.0 for l in LENGTHS},
        "per_position": {f"P{q+1}": ph[q] / pcnt[q] if pcnt[q] else 0.0 for q in range(5)},
        "per_pair": {k: pair_hits[k] / pair_counts[k] if pair_counts[k] else 0.0 for k in pair_hits},
        "tests": {"total": len(records), "pair_count": expected},
        "runtime_errors": errors,
    }, records)


def position_map_geometry(brain, checkpoint):
    px, pc, p = brain.recall.position_map(0)
    rows = []
    correct = 0
    masses = []
    margins = []
    for length, q in PAIRS:
        x = query_vector_pair(length, q)
        scores_all = np.asarray(x @ px + p, dtype=float).reshape(-1)
        ages = np.arange(length + 1, dtype=int)
        scores = scores_all[ages]
        top_age = int(ages[int(np.argmax(scores))])
        desired = int(length - q)
        z = scores - np.max(scores)
        probs = np.exp(z); probs /= probs.sum()
        pred_mass = float(probs[desired])
        others = np.delete(scores, desired)
        margin = float(scores[desired] - np.max(others)) if len(others) else float("inf")
        ok = int(top_age == desired)
        correct += ok; masses.append(pred_mass); margins.append(margin)
        rows.append({
            "checkpoint": checkpoint, "length": length, "query": f"P{q+1}",
            "desired_age": desired, "top_age": top_age, "top_is_predecessor": ok,
            "predecessor_mass": pred_mass, "margin": margin,
        })
    return {
        "top_predecessor_rate": correct / N_PAIRS,
        "mean_predecessor_mass": mean(masses),
        "median_margin": median(margins),
        "min_margin": min(margins) if margins else 0.0,
    }, rows


def evaluate_checkpoint(brain, founder, checkpoint, cal, test):
    out = {"checkpoint": checkpoint, "conditions": {}, "valid": 1}
    records = []
    cal_result, cal_records = eval_condition(brain, cal, "BASE", checkpoint, panel="CAL")
    out["calibration"] = cal_result
    out["route"] = route_from_records(cal_records)
    out["valid"] &= cal_result["valid"]
    records.extend(cal_records)
    for cond in CONDS:
        rr, recs = eval_condition(brain, test, cond, checkpoint, panel="TEST")
        out["conditions"][cond] = rr
        out["valid"] &= rr["valid"]
        records.extend(recs)
    geom, map_rows = position_map_geometry(brain, checkpoint)
    out["map_geometry"] = geom
    for r in records:
        r["founder"] = founder
    for r in map_rows:
        r["founder"] = founder
    return out, records, map_rows


def run_founder(founder):
    brain = compose(founder)
    state = {"episode": None, "teacher_rows": 0, "teacher_correct": 0}
    install_exact_position_teacher(brain, state)
    cal = make_cal(founder)
    test = make_test(founder)
    out = {"founder": founder, "valid": 1, "stages": [], "checkpoints": {}}
    eval_records = []
    map_records = []
    cumulative = 0
    for stage_index, per_pair in enumerate(STAGE_PER_PAIR, start=1):
        episodes = make_stage(founder, stage_index, per_pair)
        tr = train_stage(brain, episodes, state)
        cumulative += per_pair
        out["stages"].append({"stage": stage_index, "per_pair": per_pair, "cumulative_per_pair": cumulative, **tr})
        if tr["runtime_errors"] or tr["lessons"] != per_pair * N_PAIRS:
            out["valid"] = 0
            break
        if cumulative in CHECKPOINTS:
            ck = f"D{cumulative}"
            result, recs, maps = evaluate_checkpoint(brain, founder, ck, cal, test)
            out["checkpoints"][ck] = result
            out["valid"] &= result["valid"]
            eval_records.extend(recs); map_records.extend(maps)
    pc_max = float(np.max(np.abs(np.asarray(brain.recall.position_c)))) if brain.recall.position_maps else 0.0
    addr_max = _address_map_max_abs(brain)
    out["position_c_max_abs"] = pc_max
    out["address_map_max_abs"] = addr_max
    out["teacher_rows"] = int(state["teacher_rows"])
    out["teacher_correct"] = int(state["teacher_correct"])
    out["teacher_accuracy"] = state["teacher_correct"] / state["teacher_rows"] if state["teacher_rows"] else 0.0
    if pc_max > 1e-12 or addr_max > 1e-12:
        out["valid"] = 0
    if set(out["checkpoints"]) != {f"D{x}" for x in CHECKPOINTS}:
        out["valid"] = 0
    return out, eval_records, map_records


def summarize(founders, eval_records):
    valid = [f for f in founders if f["valid"]]
    s = {"founders": len(founders), "valid_founders": len(valid)}
    attention = {}
    maps = {}
    for dose in CHECKPOINTS:
        ck = f"D{dose}"
        cks = [f["checkpoints"][ck] for f in valid]
        for cond in CONDS:
            s[f"{ck}_{cond}_median_overall"] = median(c["conditions"][cond]["accuracy"] for c in cks)
        for l in LENGTHS:
            s[f"{ck}_BASE_median_L{l}"] = median(c["conditions"]["BASE"]["per_length"][f"L{l}"] for c in cks)
        for p in range(1, 6):
            s[f"{ck}_BASE_median_P{p}"] = median(c["conditions"]["BASE"]["per_position"][f"P{p}"] for c in cks)
        s[f"{ck}_clear_next_routes"] = sum(c["route"]["clear"] and c["route"]["preferred_route"] == "NEXT_ROUTE" for c in cks)
        s[f"{ck}_map_top_pred_median"] = median(c["map_geometry"]["top_predecessor_rate"] for c in cks)
        s[f"{ck}_map_pred_mass_median"] = median(c["map_geometry"]["mean_predecessor_mass"] for c in cks)
        s[f"{ck}_map_margin_median"] = median(c["map_geometry"]["median_margin"] for c in cks)
        rows = [r for r in eval_records if r["checkpoint"] == ck and r["panel"] == "TEST" and r["condition"] == "BASE"]
        attention[ck] = {
            "n": len(rows), "accuracy": mean(r["correct"] for r in rows),
            "top_predecessor_rate": mean(r["top_is_predecessor"] for r in rows),
            "top_target_rate": mean(r["top_is_target"] for r in rows),
            "median_top_weight": median(r["top_weight"] for r in rows),
            "mean_predecessor_weight": mean(r["predecessor_weight"] for r in rows),
        }
        maps[ck] = {
            "top_predecessor_rate_median": s[f"{ck}_map_top_pred_median"],
            "mean_predecessor_mass_median": s[f"{ck}_map_pred_mass_median"],
            "median_margin_median": s[f"{ck}_map_margin_median"],
        }

    def paired_gain(a, b):
        return median(
            f["checkpoints"][a]["conditions"]["BASE"]["accuracy"] -
            f["checkpoints"][b]["conditions"]["BASE"]["accuracy"]
            for f in valid
        )
    s["gain_D396_vs_D198"] = paired_gain("D396", "D198") if valid else 0.0
    s["gain_D792_vs_D396"] = paired_gain("D792", "D396") if valid else 0.0
    s["gain_D792_vs_D198"] = paired_gain("D792", "D198") if valid else 0.0
    s["position_c_max_abs_median"] = median(f["position_c_max_abs"] for f in valid)
    s["address_map_max_abs_median"] = median(f["address_map_max_abs"] for f in valid)
    s["teacher_accuracy_median"] = median(f["teacher_accuracy"] for f in valid)

    gates = {
        "valid_founders": len(valid) >= MIN_VALID,
        "exact_teacher": s["teacher_accuracy_median"] >= 0.999999,
        "pc_frozen": s["position_c_max_abs_median"] <= 1e-12,
        "address_frozen": s["address_map_max_abs_median"] <= 1e-12,
        "all_next_routes": all(s[f"D{d}_clear_next_routes"] >= MIN_VALID for d in CHECKPOINTS),
        "oracle_intact_all": all(s[f"D{d}_FORCE_PREDECESSOR_median_overall"] >= 0.95 for d in CHECKPOINTS),
        "wrong_route_low_all": all(s[f"D{d}_FORCE_TARGET_median_overall"] <= 0.20 for d in CHECKPOINTS),
        "D198_reproduces_clean_ceiling": 0.68 <= s["D198_BASE_median_overall"] <= 0.86,
        "D396_improves": s["gain_D396_vs_D198"] >= 0.04,
        "D792_improves_strongly": s["gain_D792_vs_D198"] >= 0.10,
        "D792_high_behavior": s["D792_BASE_median_overall"] >= 0.90,
        "D792_map_near_complete": s["D792_map_top_pred_median"] >= 0.95,
        "monotonic_behavior": s["D396_BASE_median_overall"] >= s["D198_BASE_median_overall"] and s["D792_BASE_median_overall"] >= s["D396_BASE_median_overall"],
    }
    essentials = all(gates[k] for k in ("valid_founders", "exact_teacher", "pc_frozen", "address_frozen", "oracle_intact_all", "wrong_route_low_all", "D198_reproduces_clean_ceiling"))
    if essentials and gates["D792_high_behavior"] and gates["D792_map_near_complete"] and gates["D792_improves_strongly"]:
        diagnosis = "FINITE_DOSE_POSITION_CONVERGENCE_CONFIRMED"
    elif essentials and gates["D792_improves_strongly"] and gates["monotonic_behavior"]:
        diagnosis = "POSITION_CONVERGENCE_WITH_DOSE_CONFIRMED_BUT_NOT_COMPLETE"
    elif essentials and s["gain_D792_vs_D198"] < 0.05:
        diagnosis = "POSITION_CONVERGENCE_PLATEAUS_BELOW_CEILING"
    elif essentials:
        diagnosis = "POSITION_CONVERGENCE_DOSE_TEST_MIXED"
    else:
        diagnosis = "POSITION_CONVERGENCE_DOSE_TEST_INCONCLUSIVE"
    return {"summary": s, "attention": attention, "map_summary": maps, "gates": gates, "diagnosis": diagnosis}


def write_outputs(outdir, founders, eval_records, map_records, result):
    outdir.mkdir(parents=True, exist_ok=True)
    payload = {
        "experiment": "Cadence Stone Age V7.36 Position Convergence / Dose Scaling",
        "cadence_net_version": VERSION,
        "protocol": {
            "founder_start": FOUNDER_START, "founders": len(founders), "lengths": list(LENGTHS),
            "valid_pairs": N_PAIRS, "checkpoints_per_pair": list(CHECKPOINTS),
            "stage_per_pair": list(STAGE_PER_PAIR), "training_episodes_total": CHECKPOINTS[-1] * N_PAIRS,
            "calibration_episodes_per_checkpoint": CAL_EPISODES,
            "test_episodes_per_condition_per_checkpoint": TEST_EPISODES,
            "conditions": list(CONDS), "position_teacher": "exact one-hot predecessor",
            "training_route": "BLOCK_VALUE_TRAIN -> predecessor->next",
            "recall_address": 0.0, "position_pc": "frozen zero", "position_rate": POSITION_RATE,
            "released_cortex_energy_bound_retained": True,
            "learning_free_steps": LEARNING_FREE_STEPS,
            "recall_boundary": True, "manual_start": False, "recall_position": 32,
            "recall_recency": 0.0, "recall_temperature": 0.25, "recall_copy": 0.0,
            "full_game": False, "episodic_memory": False, "reward_learning": False,
        },
        **result, "founders": founders,
    }
    (outdir / "STONE_AGE_V7_36_RESULTS.json").write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")

    with (outdir / "STONE_AGE_V7_36_SUMMARY.csv").open("w", newline="") as f:
        w = csv.writer(f); w.writerow(["metric", "value"])
        for k, v in result["summary"].items(): w.writerow([k, v])
        for ck, stats in result["attention"].items():
            for k, v in stats.items(): w.writerow([f"attention_{ck}_{k}", v])
        for ck, stats in result["map_summary"].items():
            for k, v in stats.items(): w.writerow([f"map_{ck}_{k}", v])
        for k, v in result["gates"].items(): w.writerow([f"gate_{k}", int(bool(v))])
        w.writerow(["diagnosis", result["diagnosis"]])

    fields = ["founder", "valid", "teacher_accuracy", "position_c_max_abs", "address_map_max_abs"]
    for d in CHECKPOINTS:
        ck = f"D{d}"
        fields += [f"{ck}_route", f"{ck}_route_delta", f"{ck}_map_top_pred", f"{ck}_map_pred_mass", f"{ck}_map_margin"]
        for cond in CONDS: fields.append(f"{ck}_{cond}_overall")
        fields += [f"{ck}_BASE_L{l}" for l in LENGTHS] + [f"{ck}_BASE_P{p}" for p in range(1, 6)]
    with (outdir / "STONE_AGE_V7_36_PER_FOUNDER.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for fd in founders:
            row = {
                "founder": fd["founder"], "valid": fd["valid"], "teacher_accuracy": fd.get("teacher_accuracy", 0.0),
                "position_c_max_abs": fd.get("position_c_max_abs", 0.0), "address_map_max_abs": fd.get("address_map_max_abs", 0.0),
            }
            for d in CHECKPOINTS:
                ck = f"D{d}"; c = fd.get("checkpoints", {}).get(ck, {})
                rt = c.get("route", {}); mg = c.get("map_geometry", {})
                row[f"{ck}_route"] = rt.get("preferred_route", "")
                row[f"{ck}_route_delta"] = rt.get("delta", "")
                row[f"{ck}_map_top_pred"] = mg.get("top_predecessor_rate", "")
                row[f"{ck}_map_pred_mass"] = mg.get("mean_predecessor_mass", "")
                row[f"{ck}_map_margin"] = mg.get("median_margin", "")
                for cond in CONDS:
                    row[f"{ck}_{cond}_overall"] = c.get("conditions", {}).get(cond, {}).get("accuracy", "")
                for l in LENGTHS:
                    row[f"{ck}_BASE_L{l}"] = c.get("conditions", {}).get("BASE", {}).get("per_length", {}).get(f"L{l}", "")
                for p in range(1, 6):
                    row[f"{ck}_BASE_P{p}"] = c.get("conditions", {}).get("BASE", {}).get("per_position", {}).get(f"P{p}", "")
            w.writerow(row)

    afields = ["founder", "checkpoint", "panel", "condition", "test_index", "length", "query", "correct", "top_is_predecessor", "top_is_target", "top_weight", "predecessor_weight", "target_weight"]
    with (outdir / "STONE_AGE_V7_36_ATTENTION.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=afields); w.writeheader(); w.writerows(eval_records)

    mfields = ["founder", "checkpoint", "length", "query", "desired_age", "top_age", "top_is_predecessor", "predecessor_mass", "margin"]
    with (outdir / "STONE_AGE_V7_36_MAP_GEOMETRY.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=mfields); w.writeheader(); w.writerows(map_records)

    s = result["summary"]; a = result["attention"]; g = result["gates"]
    lines = [
        "CADENCE STONE AGE V7.36 — POSITION CONVERGENCE / DOSE SCALING", "=" * 118,
        f"cadence-net: {VERSION}", f"fresh founders: {FOUNDER_START}..{FOUNDER_START + len(founders) - 1}", "",
        "QUESTION",
        "With exact predecessor supervision and the clean V7.35 map (address off, P_c frozen), does more balanced training close the learned-position gap?", "",
        f"VALID FOUNDERS: {s['valid_founders']}/{s['founders']} (minimum {MIN_VALID})", "", "MEDIAN CHECKPOINTS",
    ]
    for d in CHECKPOINTS:
        ck = f"D{d}"
        lines.append(
            f"  {ck:4s} BASE {100*s[f'{ck}_BASE_median_overall']:.1f}% | FORCE_PRED {100*s[f'{ck}_FORCE_PREDECESSOR_median_overall']:.1f}% | "
            f"top pred {100*a[ck]['top_predecessor_rate']:.1f}% | map-top-pred {100*s[f'{ck}_map_top_pred_median']:.1f}% | map mass {100*s[f'{ck}_map_pred_mass_median']:.1f}%"
        )
    lines += ["",
        f"  D396 - D198 paired BASE gain: {100*s['gain_D396_vs_D198']:+.1f}%",
        f"  D792 - D396 paired BASE gain: {100*s['gain_D792_vs_D396']:+.1f}%",
        f"  D792 - D198 paired BASE gain: {100*s['gain_D792_vs_D198']:+.1f}%", "",
        "PRE-REGISTERED GATES",
    ] + [f"- {k}: {v}" for k, v in g.items()]
    lines += ["", f"DIAGNOSTIC CLASSIFICATION: {result['diagnosis']}", "", "INTERPRETATION",
        "- One brain per founder trains continuously; checkpoints are cumulative, so this is a convergence curve rather than separate-arm founder noise.",
        "- Every lesson uses the exact predecessor position target. Content-address learning is frozen and position P_c stays zero.",
        "- The released 0.91.1 position update and its cortex-energy bound are otherwise unchanged; only cumulative balanced dose changes.",
        f"- Numerical teaching free-phase budget is fixed at {LEARNING_FREE_STEPS} sweeps for every founder/checkpoint to avoid the 1024-sweep exhaustion that invalidated the first V7.36 run.",
        "- MAP_GEOMETRY reads the learned additive position map directly, independent of neural answer accuracy.",
        "- FORCE_PREDECESSOR verifies that the downstream predecessor->next route remains capable of perfect behavior.", "", "BOUNDARIES",
        "1. Component task only; no full-game claim.", "2. Native recall_boundary=True; no manual START.",
        "3. BLOCK_VALUE_TRAIN fixes predecessor->next during acquisition; values are normal at evaluation.",
        "4. Exact predecessor p* is training-only diagnostic supervision; BASE uses ordinary learned Recall.",
        "5. Doses are exact-balanced at every checkpoint: 198, 396, and 792 examples per one of 22 (length,position) pairs.",
        "6. learning_free_steps=4096 is a solver-budget repair only; the learning rule, tolerance, nudged budget, task, seeds, and interventions are unchanged.",
    ]
    (outdir / "STONE_AGE_V7_36_REPORT.txt").write_text("\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--founders", type=int, default=DEFAULT_FOUNDERS)
    ap.add_argument("--outdir", default="v7_36_results")
    args = ap.parse_args()
    actual = pkg_version("cadence-net")
    if actual != VERSION:
        raise RuntimeError(f"V7.36 requires cadence-net=={VERSION}, found {actual}")
    founders = []; eval_records = []; map_records = []
    for i in range(args.founders):
        founder = FOUNDER_START + i
        print(f"[{i+1}/{args.founders}] founder {founder}", flush=True)
        fd, recs, maps = run_founder(founder)
        founders.append(fd); eval_records.extend(recs); map_records.extend(maps)
        bits = []
        for d in CHECKPOINTS:
            ck = f"D{d}"
            acc = fd.get("checkpoints", {}).get(ck, {}).get("conditions", {}).get("BASE", {}).get("accuracy", 0.0)
            bits.append(f"{ck}={acc:.3f}")
        print("    valid=" + str(fd["valid"]) + " " + " ".join(bits), flush=True)
    result = summarize(founders, eval_records)
    write_outputs(Path(args.outdir), founders, eval_records, map_records, result)
    print("", flush=True)
    print("V7.36 complete:", result["diagnosis"], flush=True)
    print(f"valid founders: {result['summary']['valid_founders']}/{len(founders)}", flush=True)
    for d in CHECKPOINTS:
        ck = f"D{d}"
        print(f"{ck} BASE: {100*result['summary'][f'{ck}_BASE_median_overall']:.1f}%", flush=True)


if __name__ == "__main__":
    main()

