# Cadence 0.84 Agency Door results

## V1R — confirmed contingency-sensitive behavior

Fresh confirmation seeds: `22001..22050`.

Randomized chamber validity:

| measure | value |
|---|---:|
| controllable pre effect | 1.0000 |
| controllable post effect | 1.0000 |
| yoked pre effect | 0.0062 |
| yoked post effect | 0.0022 |
| shuffled pre effect | -0.0013 |
| shuffled post effect | 0.0308 |

Mean phase-correct action rate:

| arm | acquisition early | acquisition late | reversal early | reversal late |
|---|---:|---:|---:|---:|
| controllable | 83.8% | 96.6% | 48.1% | 98.9% |
| yoked | 27.6% | 32.0% | 29.2% | 30.0% |
| random | 33.6% | 34.3% | 32.9% | 32.6% |
| tabular | 83.4% | 86.7% | 60.8% | 87.2% |

Pre-registered primary, reversal late:

- controllable higher: 35
- yoked higher: 0
- ties: 15
- mean difference: +68.9 percentage points
- exact two-sided sign p ≈ `5.82e-11`

Secondary, acquisition late:

- controllable higher: 40
- yoked higher: 6
- ties: 4
- mean difference: +64.6 percentage points
- p ≈ `3.10e-7`

## V2 — no behavioral savings in PRESS -> PULL -> PRESS

Fresh seeds: `23001..23050`.

Mean phase-correct rate:

| arm | A1 early20 | A1 late40 | B early20 | B late40 | A2 early20 | A2 late40 |
|---|---:|---:|---:|---:|---:|---:|
| controllable | 75.8% | 97.8% | 23.6% | 96.8% | 26.5% | 100.0% |
| yoked | 31.6% | 30.2% | 35.2% | 35.9% | 29.4% | 26.0% |
| random | 32.6% | 34.0% | 33.0% | 33.2% | 35.0% | 31.8% |
| tabular | 79.9% | 86.8% | 27.1% | 88.7% | 33.9% | 87.0% |

Fresh naive PRESS:

- early20: 75.3%
- late40: 95.2%

Pre-registered primary:

- A2 early higher than A1 early: 1
- A1 early higher than A2 early: 49
- ties: 0
- mean A2-A1: -49.3 percentage points
- exact two-sided sign p ≈ `9.06e-14`

Returned A2 versus fresh naive PRESS:

- A2 higher: 0
- naive higher: 49
- ties: 1
- mean A2-naive: -48.8 percentage points
- p ≈ `3.55e-15`

## V2B — counterbalanced negative savings

Fresh seeds: `24001..24050`.

Founder first-action distribution:

- PRESS: 18
- PULL: 19
- WAIT: 13

Early20 means:

| measurement | value |
|---|---:|
| PPP initial PRESS | 77.7% |
| PPP returned PRESS | 28.4% |
| QPQ initial PULL | 77.8% |
| QPQ returned PULL | 25.7% |
| returned action mean | 27.1% |
| fresh naive matched-action mean | 78.2% |

Late returned-phase control:

| arm | late40 |
|---|---:|
| controllable | 99.0% |
| yoked | 31.2% |

### Primary

Counterbalanced savings versus zero:

- positive: 0
- negative: 49
- ties: 1
- mean savings: **-50.7 percentage points**
- exact two-sided sign p ≈ `3.55e-15`

### Secondary

Returned early20 versus fresh naive matched-action early20:

- return higher: 0
- naive higher: 50
- ties: 0
- mean return-naive: **-51.1 percentage points**
- p ≈ `1.78e-15`

Controllable returned late40 versus yoked:

- controllable higher: 43
- yoked higher: 0
- ties: 7
- mean difference: **+67.9 percentage points**
- p ≈ `2.27e-13`

### Action-specific descriptives

PRESS savings:

- return higher: 1
- initial higher: 48
- ties: 1
- mean: -49.3 percentage points
- p ≈ `1.78e-13`

PULL savings:

- return higher: 2
- initial higher: 47
- ties: 1
- mean: -52.1 percentage points
- p ≈ `4.36e-12`

Conventional control counterbalanced savings:

- random: -0.2 percentage points
- tabular: -41.9 percentage points

## Interpretation boundary

The strongest supported statement is:

> Cadence 0.84 reproducibly learns which action currently controls the door and adapts after reversals in this controllable-vs-yoked chamber. However, when a previously useful contingency returns after an intervening contingency, the benchmark shows no early behavioral savings. Counterbalancing PRESS and PULL rules out a fixed action-0 preference as the explanation. The active contingency is nevertheless relearned to near-perfect late performance.

The result does not establish whether an older internal relationship is erased, retained but behaviorally suppressed, or represented elsewhere. It also does not establish an explicit causal world model, counterfactual reasoning, or learned environmental transition forecasting.

The tabular control also shows negative savings, so the switch/reacquisition cost is not claimed to be unique to Cadence.
