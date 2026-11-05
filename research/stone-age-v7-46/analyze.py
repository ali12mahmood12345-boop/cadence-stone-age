#!/usr/bin/env python3
"""Reproducible V7.46 paired TEST/BASE error attribution; uses V7.45 saved files."""
import argparse
import collections
import csv
import json
import math
import statistics
from pathlib import Path

def read_file(folder, seed, arm):
    candidates = [folder / f"founder_{seed}_{arm}.json", folder / f"founder_{seed}_{arm}(1).json"]
    found = [p for p in candidates if p.exists()]
    if not found:
        raise FileNotFoundError(f"Missing {seed} {arm}")
    data = [json.loads(p.read_text(encoding="utf-8")) for p in found]
    if len(data) > 1 and data[0] != data[1]:
        raise ValueError(f"Conflicting duplicates for {seed} {arm}")
    d = data[-1]
    f = d["founder"]
    assert f["founder"] == seed and d["arm"] == arm and f["valid"] == 1
    assert len(f["stages"]) == 3
    assert sum(s["lessons"] for s in f["stages"]) == 17424
    assert all(s["qualified_lessons"] == s["lessons"] and not s["runtime_errors"]
               and max(s["phase_max_residual"].values()) <= .003 for s in f["stages"])
    assert f["position_c_max_abs"] == f["address_map_max_abs"] == 0
    if arm == "EXACT":
        assert f["teacher_accuracy"] == 1 and f["teacher_rows"] > 0
    else:
        assert f["teacher_accuracy"] is None and f["teacher_rows"] == 0
    return d

def get_test(d, checkpoint, condition):
    records = [a for a in d["attention"] if a["checkpoint"] == checkpoint
               and a["panel"] == "TEST" and a["condition"] == condition]
    records.sort(key=lambda x: x["test_index"])
    assert len(records) == 1100
    expected = d["founder"]["checkpoints"][checkpoint]["conditions"][condition]["accuracy"]
    assert math.isclose(sum(bool(a["correct"]) for a in records)/1100, expected, abs_tol=1e-12)
    return records

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, default=Path("results"))
    args = ap.parse_args()
    data = {(s, a): read_file(args.data_dir, s, a) for s in range(105001, 105009)
            for a in ("EXACT", "NATIVE")}
    rows, summary = [], []
    for checkpoint in ("D198", "D396", "D792"):
        overall = collections.Counter()
        diffs = []
        for seed in range(105001, 105009):
            e, n = data[seed, "EXACT"], data[seed, "NATIVE"]
            for arm in (e, n):
                for cond in ("BASE", "FORCE_PREDECESSOR", "FORCE_TARGET"):
                    get_test(arm, checkpoint, cond)
                cal = [x for x in arm["attention"] if x["checkpoint"] == checkpoint and x["panel"] == "CAL" and x["condition"] == "BASE"]
                assert len(cal) == 440
                assert math.isclose(sum(bool(x["correct"]) for x in cal)/440,
                                    arm["founder"]["checkpoints"][checkpoint]["calibration"]["accuracy"], abs_tol=1e-12)
                maps = [x for x in arm["maps"] if x["checkpoint"] == checkpoint]
                assert len(maps) == 22
                assert math.isclose(sum(bool(x["top_is_predecessor"]) for x in maps)/22,
                    arm["founder"]["checkpoints"][checkpoint]["map_geometry"]["top_predecessor_rate"], abs_tol=1e-12)
            er, nr = get_test(e, checkpoint, "BASE"), get_test(n, checkpoint, "BASE")
            count = collections.Counter()
            for x, y in zip(er, nr):
                assert (x["test_index"], x["length"], x["query"]) == (y["test_index"], y["length"], y["query"])
                ec, nc, top = bool(x["correct"]), bool(y["correct"]), bool(y["top_is_predecessor"])
                count["both_correct"] += ec and nc
                count["exact_only"] += ec and not nc
                count["native_only"] += not ec and nc
                count["both_wrong"] += not ec and not nc
                count["native_wrong_top_not_pred"] += not nc and not top
                count["native_wrong_top_pred"] += not nc and top
                count["native_correct_top_not_pred"] += nc and not top
                count["exact_only_top_not_pred"] += ec and not nc and not top
            exact = e["founder"]["checkpoints"][checkpoint]["conditions"]["BASE"]["accuracy"]
            native = n["founder"]["checkpoints"][checkpoint]["conditions"]["BASE"]["accuracy"]
            assert math.isclose((count["exact_only"]-count["native_only"])/1100, exact-native, abs_tol=1e-12)
            diffs.append(native-exact)
            rows.append({"checkpoint": checkpoint, "seed": seed,
                        "exact_base": exact, "native_base": native, "native_minus_exact": native-exact, **count})
            overall.update(count)
        count_native_wrong = overall["native_wrong_top_not_pred"]+overall["native_wrong_top_pred"]
        chunk = [r for r in rows if r["checkpoint"] == checkpoint]
        summary.append({"checkpoint": checkpoint, "paired_test_trials": 8800,
                        "exact_median_base": statistics.median(r["exact_base"] for r in chunk),
                        "native_median_base": statistics.median(r["native_base"] for r in chunk),
                        "paired_median_native_minus_exact": statistics.median(diffs),
                        "paired_mean_native_minus_exact": statistics.mean(diffs),
                        "native_error_nonpredecessor_fraction": overall["native_wrong_top_not_pred"]/count_native_wrong,
                        **overall})
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir/"V7_46_PER_FOUNDER.csv").open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    (args.output_dir/"V7_46_RESULTS.json").write_text(json.dumps({
        "experiment": "V7.46",
        "method": "posthoc paired trial-level attribution; no new training",
        "checkpoint_results": summary,
        "cautions": "Top attention is descriptive, not a causal hard route. Same V7.45 founders."}, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
