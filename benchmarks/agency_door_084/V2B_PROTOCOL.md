# Cadence Agency Door V2B — Frozen Counterbalanced Protocol

## Why V2B exists

V2 (`PRESS -> PULL -> PRESS`) found strongly negative early reacquisition savings, but its first PRESS phase was also unusually easy for fresh Cadence founders. V2B removes that action-order confound by giving the same founder seed two mirrored lives.

## Mirrored lives

For every fresh base seed:

- PPP: `PRESS -> PULL -> PRESS`
- QPQ: `PULL -> PRESS -> PULL`

Each phase lasts 120 trials.

The PPP and QPQ controllable brains are separately instantiated with the **same founder seed**. Their first observation is identical. The environment never supplies a phase, reversal, world, or controllability flag.

## Observation

At each decision the brain receives:

`[door_closed_now, previous_open, previous_closed]`

The first observation is:

`[1, 0, 0]`

## Reward

Reward is 1.0 if the observed door opened, otherwise 0.0.

The measured outcome of the previously issued action is supplied to the continuing brain on the next call.

## Cadence

- `cadence-net==0.84.0`
- `Brain.compose(inputs=3, actions=3, modules=(16,), arousal=True, recall=False)`
- no teacher
- all other genes at released founder defaults
- fresh base seeds `24001..24050`

## Primary endpoint

For each base seed:

- `PRESS savings = PPP phase-3 early20 - PPP phase-1 early20`
- `PULL savings = QPQ phase-3 early20 - QPQ phase-1 early20`
- `counterbalanced savings = (PRESS savings + PULL savings) / 2`

Primary test: exact two-sided sign test of counterbalanced savings versus zero across non-tied base seeds.

This endpoint was frozen before seeing V2B data.

## Secondary endpoints

1. Mean returned-action early20 across PPP/QPQ versus fresh NAIVE matched-action early20.
2. Mean controllable returned-phase late40 versus matched YOKED returned-phase late40.
3. PRESS and PULL savings reported separately as action-specific descriptive checks.

## Controls

- YOKED twins receive each matched controllable arm's exact observed door-outcome/reward timeline while their own action does not control the outcome.
- Fresh NAIVE PRESS and NAIVE PULL brains use the same fresh founder seed within each base seed.
- Uniform random mirrored schedules.
- Epsilon-greedy tabular mirrored schedules (`alpha=0.20`, `epsilon=0.20`).

## Interpretation

Positive counterbalanced savings supports faster behavioral reacquisition when an old contingency returns.

Negative counterbalanced savings supports interference / no behavioral savings under this protocol.

Counterbalancing prevents a fixed preference for PRESS/action 0 from deciding that conclusion.

Neither result establishes a specific internal memory mechanism, an explicit causal world model, transition forecasts, or counterfactual reasoning.
