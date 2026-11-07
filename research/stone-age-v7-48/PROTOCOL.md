# V7.48 — Fresh founder confirmation of the native position-rate effect

**Status: preregistered plan; no V7.48 training data yet.**

V7.47 found that increasing native position-learning rate from 0.10 to 0.20 improved D792 BASE on all eight paired founders, with median paired improvement +4.77 percentage points; median native BASE reached 98.14% and map-top 100%. V7.48 tests reproducibility with independent seed panels.

## Design

- Eight fresh founders: **108001–108008** (separate from the V7.47 seeds 107001–107008).
- Three independently composed matched brains per founder: `EXACT_010` rate=.10 (positive control), `NATIVE_010` rate=.10, `NATIVE_020` rate=.20.
- Retain `cadence-net==0.91.1`, original identical panels within each seed, 22 (length, position) pairs, 17,424 lessons per arm, D198/D396/D792 checkpoints, CAL and TEST evaluations and both forced-recall oracles.
- All phase residuals must be finite and <=.003; qualified learning; 4096 free/nudged caps; damping=3; initial_damping=1; warnings as errors. No failed phase counts as a lesson.
- Native position update is released native target estimation with the native x/b maps intact; restore P_c after each update (frozen zero). Content-address weights frozen zero. EXACT retains the original exact predecessor position teacher. Answer supervision and BLOCK_VALUE_TRAIN steering retained throughout; **not unsupervised**.
- Native `teacher_accuracy` is null, never 0. `recall_boundary=True`, **no manual START**, read temperature .25, position 32. Save each full arm; do not resume partly trained brains. Alternate three-arm sequence over odd/even seeds.
- Source is the V7.47 runner copied to this directory with seed/output/experiment labels updated; no model, task or solver changes.

## Primary gates — prespecified before running

1. At least 6/8 matched triplets complete validly, all lessons qualified, map invariants preserved, no unexpected warnings or native position refusals.
2. EXACT D792 median BASE >= 0.90, map-top >= 0.95, forced predecessor >= 0.95.
3. Each native arm's D792 forced-predecessor median >= 0.95.
4. Paired D792 NATIVE_020 minus NATIVE_010 median BASE gain >= +0.03; paired median map-top gain >= +1/22 (4.545 percentage points).
5. At least **6/8** matched founders have positive D792 BASE gain and NATIVE_020 D792 median BASE >= 0.95.

The causal rate effect is supported on the tested task only if all gates pass. Otherwise use **not replicated** (if 1–3 qualify and 4–5 fail) or **inconclusive** (if numerical/validity/control checks fail), never silently discard failed founders. Secondary: report D198/D396 effects, paired native-versus-exact gaps, predecessor mass, trial-level attention proxy, and all eight founder-level values, even if effect small.

## Implementation and usage

From the full repository, run `python -m pip install -r requirements.txt`, then `python run.py --smoke`, `python run.py --resume` inside `research/stone-age-v7-48`. Upload `v7_48_results` folder as a ZIP/RAR after full run. `--limit 2` is a pilot and does **not** qualify as replication.
