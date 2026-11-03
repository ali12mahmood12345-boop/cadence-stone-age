# V7.38 — Reproduced free-solver non-settlement

## Finding

Founder 102007 reaches lesson 7666 in both training-budget arms, with D198 BASE matching the prior run exactly (75.9091%). Both arms produce byte-identical pre-free solver snapshots. Independent SHA256 checks of the two supplied files match the recorded hash:

`23cab22c6e3bebe8141bbb75fed351b26d340ddf8710e4ab89ab3a13b30635b9`

The snapshots were hashed, not deserialized, for this audit. Probe measurements below are from the supplied JSON, not a newly executed replay.

| Probe budget | Steps used | Equation residual | Budget exhausted |
|---|---:|---:|---|
| 4096 | 4096 | 1.7105146077639979 | Yes |
| 16384 | 16384 | 1.7105146077639979 | Yes |
| 16384 repeat | 16384 | 1.7105146077639979 | Yes |

These results are identical in both training arms. All residual values are finite. Repeated 16384 diagnostics match exactly. The configured tolerance is 0.003; finite-mode stopping uses a movement criterion, so this tolerance must not be misrepresented as an enforced equation-residual acceptance rule. Nevertheless the measured equation residual is large and does not decrease at the two recorded endpoints.

## Interpretation

The diagnostic reproduces the numerical obstruction at the intended lesson from the same solver inputs. Raising the cap from 4096 to 16384 provides no endpoint residual improvement for this case. This supports investigating the solver dynamics instead of another blind budget increase.

The identical scalar residual at two endpoints does NOT prove a limit cycle, divergence, or absence of any equilibrium. A trajectory or state-difference measurement is required to distinguish these. The result concerns one founder and one lesson; it does not explain all six failed founders or resolve founder 102003's completion reversal.

The diagnostic lesson was intercepted before learning and no probe result was accepted as training. This is a successful targeted reproduction, not a successful eight-founder convergence confirmation. V7.36/V7.37 remain inconclusive at the population level.

## Next justified step: V7.39 trajectory and damping diagnostics

Reuse the captured solver input rather than replaying thousands of lessons. First reproduce the saved endpoints in the chosen runtime and record Python, NumPy and Cadence versions. The supplied run used Python 3.15.2, NumPy 2.5.4, cadence-net 0.91.1; cross-runtime mismatches must be reported.

Record nearby successive states and equation residuals around the failing solve; test one-step and two-step state differences to distinguish stationary behavior from possible period-two behavior. Inspect the released integration API before specifying a smaller-step/damping intervention. Compare any such intervention on disposable clones of the same inputs, preserving the equations, weights, drive and starting state where possible. Explicitly distinguish numerical step changes from neural-gain changes, which alter the system itself.

Any proposed repair must subsequently reproduce across other failed lessons and pass the full training/behavioral confirmation. Keep native recall_boundary=True, no manual START, and never silently accept failed lessons. V7.39 is recommended here, not yet implemented or run.

