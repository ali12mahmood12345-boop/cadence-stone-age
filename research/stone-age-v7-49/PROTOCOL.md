# V7.49 — Exploratory position-logit sharpening

Frozen before the full run on 2026-11-08. V7.48 completed all 24 arms but failed its 95% native behavior gate (94.00% median), despite 100% median map-top and forced-predecessor accuracy. This follow-up cannot rescue that replication outcome.

Question: does diffuse position attention explain some remaining errors? Recall temperature scales content logits, not the added position logits in cadence-net 0.91.1. Therefore the intervention scales position maps directly; it is not a recall-temperature change. This corrects the provisional temperature suggestion in the V7.48 report.

Eight fresh founders 109001–109008. Train one NATIVE_020 brain per founder using exactly the V7.48 qualified protocol, 17,424 lessons, D198/D396/D792, frozen zero P_c and content-address maps, cadence-net 0.91.1, native recall_boundary=True and no manual START. Answer supervision remains enabled. Training read temperature stays .25 and position rate .20.

At each checkpoint evaluate the same CAL/TEST panels and all three conditions at position-logit gain 1, then 2 (multiply every position-map array by 2), restore the original arrays and repeat gain 1. No training occurs during these evaluations. Restoring the baseline must reproduce all trial and map records exactly. No scale selection or further sweep. Doubling preserves the ranking of static position logits, but may sharpen incorrect positions too. The intervention applies during the whole evaluation episode, not just its final query.

Primary endpoint: paired D792 TEST BASE accuracy gain (gain 2 minus gain 1) across all eight founders, reporting every value including regressions. Secondary: D198/D396, actual attention predecessor weight and top rate, map mass, forced predecessor and target controls. Fresh founders separate this diagnostic from the V7.48 cohort.

Exploratory decision rules, not a replication claim: all 8 founders valid with 17,424 qualified lessons and every free/nudged/opposite residual finite <=.003; restored baseline identical; D792 forced-predecessor median >=95% and forced-target median <=20% at both gains. If valid, call sharpening promising only if median paired BASE gain >=2 percentage points with >=6/8 positive founders. Otherwise report no support under this intervention; numerical/control failures are inconclusive. Never drop failed founders.

Run `python run_v749.py --smoke` then `python run_v749.py --resume` from the full repository. Smoke uses seed 109999 and 22 lessons and cannot satisfy any experiment gate. Every completed founder is saved atomically; resume only skips saved valid founders. Dependencies: sibling V7.48 runner, V7.45 qualified reference and V7.36 reference files.

