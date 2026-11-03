# V7.39 results — period-two tail and smaller-step convergence

The supplied run completed with baseline_reproduced=true, using Python 3.15.2, NumPy 2.5.4 and cadence-net 0.91.1. This is one saved free solve: founder 102007, lesson 7666.

At original dt, both the 4096-step and 16384-step endpoints have residual 1.7105146077639979. Across all 32 recorded continuation steps, the reported full-state two-step difference is exactly zero wherever defined; the last one-step difference is 1.7105146077639979. This is exact period-two behavior at recorded precision in the sampled tail, not merely a slowly improving residual.

| dt factor | Initial stop, steps | Residual at stop | Residual after 32 additional steps |
|---|---:|---:|---:|
| 1, cap 4096 | 4096 | 1.710514607764 | 1.710514607764 |
| 1, cap 16384 | 16384 | 1.710514607764 | 1.710514607764 |
| 0.5 | 63 | 0.016504257211 | 0.000810754264 |
| 0.25 | 99 | 0.032541661113 | 0.008980582915 |
| 0.125 | 47 | 0.086458484353 | 0.036400163544 |

With dt/2 the first recorded continuation residual below 0.003 occurs 19 steps after the original movement-based stop: 82 steps in total. At 95 total steps the residual is 0.000810754264. Thus a small-residual state exists and is accessible from the same starting input under this numerical change. The initial finite-mode movement stopping rule stopped too early to meet the proposed equation-residual threshold.

The smaller dt/4 and dt/8 probes also reduced residuals but did not cross 0.003 in the recorded continuation window. This does not establish their inability to converge; their step durations and stopping points differ.

## Scope and next experiment

The result supports a numerical integration/stopping explanation for this particular failure. It does not prove that every failed founder has the same mechanism, or that full training is repaired. No weights or neural gain were intentionally changed by these solver probes, and no probe was accepted as a training lesson.

V7.40 should test a residual-checked free solve with controlled dt reduction, beginning with the released qualified-settling implementation and its actual semantics. Require equation residual <=0.003, preserve complete state and explicitly account for nudged/opposite phases. Do not simply halve dt while retaining movement-only acceptance. Validate other failed lessons before an eight-founder behavioral confirmation; use identical pre-lesson snapshots for paired numerical comparisons. Preserve native recall_boundary=True and no manual START.

V7.40 is a recommendation, not implemented or run here. V7.36/V7.37 remain population-level inconclusive.

