# V7.47 — Controlled native position-rate intervention

**Status: runner prepared; NO V7.47 training results yet.**

## Why

V7.45 established a paired D792 median BASE difference of −7.41 percentage points for NATIVE vs EXACT across eight valid founders. The posthoc V7.46 audit found 565/811 native errors had a non-predecessor attention winner, but winner identity alone is not causal proof. V7.47 tests a direct change to the released native position learner, rather than assuming more total training solves the gap.

## Arms

Fresh matched founders **107001–107008**, three freshly composed brains per seed:

- **EXACT_010**: archived exact predecessor position teacher; position rate **0.10**; contemporary positive control.
- **NATIVE_010**: released native target estimation; position rate **0.10**; native baseline.
- **NATIVE_020**: same released native target estimation; position rate **0.20**; only controlled rate intervention.

Native wraps released `_position_step` to restore P_c immediately after update, leaving x/b updates, native target estimation, energy bound and gating intact. Both native arms receive **no exact predecessor position label** but still use the task's answer supervision and BLOCK_VALUE_TRAIN steering. All matched arms use identical deterministic founder panels; reverse arm order on even/odd seeds.

## Hold fixed

`cadence-net==0.91.1`, NumPy >=2,<3, `qualified=True`, free/nudged caps 4096, `damping=3`, `initial_damping=1`, residual tolerance .003 for free/nudged/opposite, all warnings errors, frozen content address map, frozen P_c, read temperature .25, `recall_boundary=True`, no manual START; same 22 length/position pairs, D198/D396/D792, TEST/CAL panels, FORCE_PREDECESSOR/FORCE_TARGET and BASE evaluation.

A failed training phase invalidates that arm. Save complete arms independently and allow restart by **skipping saved whole-arm records only**, never resuming partly trained brains.

## Prespecified gates

At least **six** complete valid matched triplets, all 17,424 lessons per arm fully qualified with no warnings/refusals, all residuals <=.003, frozen maps. At D792: EXACT median BASE >=90%, map-top >=95%, forced predecessor >=95%; native forced predecessor >=95% in both arms.

Define useful increased-rate response as **median paired** (NATIVE_020 − NATIVE_010) D792 BASE >=+3 percentage points **and** median paired map-top >=+1/22 (4.545 pp). Report every founder, secondary D198/D396 effects, predecessor mass and forced-target results. A failure of numerical/control gates means **inconclusive**, not negative.

This is a narrow task-level mechanism experiment, not unsupervised intelligence or the full Stone Age game. Training results will be reported only after running and independently auditing user-supplied result files.

The standalone ZIP package includes a pinned, SHA-verified reference bootstrap, Windows launcher, and a robust runner. When working from the full repository, V7.45 and V7.36 reference folders are adjacent.
