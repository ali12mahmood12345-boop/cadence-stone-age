# Cadence 0.84 Agency Door benchmarks

This folder contains a small controllable-vs-yoked intervention benchmark inspired by Cadence issue #114, **"Qualify causal agency and learned controllability."**

The project is separate from the Stone Age sequence benchmark but is published in this repository so the existing research trail stays easy to inspect.

## Scope

The chamber asks whether one continuing Cadence brain behaves differently when its own action actually controls a door versus when it receives the same observed outcome/reward timeline but its own action does not control the outcome.

Three actions are available:

- `PRESS`
- `PULL`
- `WAIT`

No controllability flag, phase flag, reversal flag, or world identity is included in the observation.

Cadence version:

`cadence-net==0.84.0`

Common composition:

`Brain.compose(inputs=3, actions=3, modules=(16,), arousal=True, recall=False)`

No teacher labels are used. Other genes remain at the released founder defaults.

## Experiment sequence

### V1 — development

One life:

`PRESS -> PULL`

The first 120 trials reward PRESS opening the controllable door; the next 120 reward PULL.

The matched YOKED arm receives the exact same observed OPEN/CLOSED and reward timeline as its controllable twin, independent of its own action.

Development result:

- chamber validity gate passed
- controllable late acquisition: 97.5%
- yoked late acquisition: 36.5%
- controllable late reversal: 100.0%
- yoked late reversal: 41.7%

### V1R — fresh 50-seed confirmation

Fresh base seeds `22001..22050`.

Primary endpoint: late reversal CONTROLLABLE vs YOKED, exact two-sided sign test across non-tied paired schedules.

Result:

- late acquisition: 96.6% controllable vs 32.0% yoked
- late reversal: 98.9% controllable vs 30.0% yoked
- primary late-reversal paired comparison: 35 controllable wins, 0 yoked wins, 15 ties
- exact two-sided sign p ≈ `5.82e-11`
- secondary late-acquisition comparison: 40 wins, 6 losses, 4 ties, p ≈ `3.10e-7`

Interpretation: Cadence 0.84 shows reproducible **contingency-sensitive action learning and reversal adaptation** in this chamber. This is not yet a claim of an explicit causal world model or learned transition forecast.

### V2 — A -> B -> A reacquisition

Fresh seeds `23001..23050`.

One life:

`PRESS -> PULL -> PRESS`

Primary question: does the returned PRESS contingency recover faster than the original PRESS contingency was learned?

Result:

- initial PRESS early20: 75.8%
- returned PRESS early20: 26.5%
- A2 higher on 1/50 seeds; A1 higher on 49/50
- mean A2-A1: -49.3 percentage points
- exact sign p ≈ `9.06e-14`
- fresh naive PRESS early20: 75.3%
- returned PRESS was worse than naive on 49/50 seeds, 1 tie

This rejected the behavioral-savings hypothesis under that ordering.

### V2B — counterbalanced reacquisition

V2B removes the action-order / action-0 preference confound.

Fresh seeds `24001..24050`.

For each founder seed two independent continuing lives begin from the same founder:

- PPP: `PRESS -> PULL -> PRESS`
- QPQ: `PULL -> PRESS -> PULL`

Primary per-seed statistic:

`counterbalanced savings = (PRESS return - PRESS initial + PULL return - PULL initial) / 2`

Results:

- founder first-action distribution: PRESS 18, PULL 19, WAIT 13
- initial PRESS early20: 77.7%
- returned PRESS early20: 28.4%
- initial PULL early20: 77.8%
- returned PULL early20: 25.7%
- counterbalanced mean savings: **-50.7 percentage points**
- positive savings: **0/50**
- negative savings: **49/50**
- ties: **1/50**
- exact two-sided sign p ≈ `3.55e-15`
- returned-action early20: 27.1%
- fresh naive matched-action early20: 78.2%
- return higher than naive: 0/50
- controllable returned late40: 99.0%
- yoked returned late40: 31.2%

The negative savings result survives action counterbalancing.

## Current interpretation

A cautious summary is:

> Cadence 0.84 reproducibly learns which action currently controls the door and adapts after reversals in a controllable-vs-yoked chamber. However, in an A -> B -> A return test it shows no behavioral savings for the previously useful contingency. Counterbalancing PRESS and PULL confirms a large reacquisition/interference cost rather than an action-0 founder preference. Despite this early return cost, the current contingency is eventually relearned to near-perfect late performance.

The simple tabular control also shows negative counterbalanced savings, so the reacquisition cost should not be described as uniquely specific to Cadence.

## Files

- [RESULTS.md](RESULTS.md) — consolidated measurements and interpretation boundaries
- [V2B_PROTOCOL.md](V2B_PROTOCOL.md) — frozen counterbalanced protocol
- [V2B_REPORT.txt](V2B_REPORT.txt) — final V2B report
- [requirements.txt](requirements.txt) — pinned environment

The benchmark is a component instrument. It does **not** establish an explicit causal world model, counterfactual reasoning, or learned transition forecasting.
