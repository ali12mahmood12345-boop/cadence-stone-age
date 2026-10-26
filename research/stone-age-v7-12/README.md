# Stone Age V7.12 — FIRE Temporal Action-Commitment Control

Status: **development complete**

Cadence: **0.88.1**

Official frozen classification:

`PARTIAL_FIRE_COMMITMENT_SIGNAL`

## Question

Does the learned FIRE policy succeed when `GATHER_WOOD` / `GATHER_STONE` are treated as temporally extended motor primitives rather than re-decided every 0.55 s?

## Frozen design

FIRE only.

Fresh founders: `75001..75008`.

Representations:
- `CONTRAST18`
- `FIRE_MINIMAL`
- `FIRE_MINIMAL_PLUS_PROGRESS`

Training matched V7.11:
1. reset-per-row static bootstrap
2. DAgger64
3. full reset-per-row static replay
4. freeze final brain
5. evaluate the exact same final brain under two execution modes

Modes:
- `DECISION_LEVEL`
- `COMMIT_TO_COMPLETION`

Both modes shared the same 14 decision-window environment budget. No learning occurred during the comparison.

## Result

All **8/8 founders were valid**.

Caretaker oracle: **48/48**.

Final medians — EXACT / FRESH / DECISION / COMMIT:

| Arm | Exact | Fresh | Decision | Commit | Commit-ready founders |
| --- | ---: | ---: | ---: | ---: | ---: |
| CONTRAST18 | 100% | 100% | 0% | 0% | 3/8 |
| FIRE_MINIMAL | 100% | 100% | 0% | **50%** | 3/8 |
| FIRE_MINIMAL_PLUS_PROGRESS | 100% | 100% | 25% | **50%** | 2/8 |

The frozen implementation classified V7.12 as `PARTIAL_FIRE_COMMITMENT_SIGNAL` because FIRE_MINIMAL's difference-of-medians commitment gain was +0.50, above the predeclared +2/6 threshold.

Important descriptive nuance:
- paired founder median gain was 0.0 because the effect was heterogeneous rather than uniform
- FIRE_MINIMAL commitment improved 3/8 founders and tied 5/8
- no representation reached the >=6/8 founder pass gate

## Mechanism

Commitment removes the mid-gather switching failure for some founders.

Under `FIRE_MINIMAL`, founder-level DECISION -> COMMIT successes were:

- 75001: 0/6 -> 0/6
- 75002: 3/6 -> 6/6
- 75003: 6/6 -> 6/6
- 75004: 0/6 -> 3/6
- 75005: 0/6 -> 0/6
- 75006: 0/6 -> 3/6
- 75007: 6/6 -> 6/6
- 75008: 0/6 -> 0/6

So temporal commitment is a real partial mechanism, but it is not the final solution.

### New dominant failure

Trace audit shows a striking pattern:

> Once commitment is used, failed episodes generally finish the required gather primitive successfully, then fail at the **next semantic stage boundary**.

For failed committed episodes, the resource becomes ready:
- wood >= 4
- stone >= 2

The correct next action is `CRAFT_FIRE`.

Yet the continuing brain often chooses another `GATHER_WOOD` or `GATHER_STONE` instead.

This is especially informative for `FIRE_MINIMAL`:

- its visible representation at the ready-to-craft state is the same minimal task key used by the static `FIRE_CRAFT` prototype
- static exact/fresh are 100/100
- but continuing `brain.act` can still choose the previous gather action after a committed primitive

That points to **per-stream internal state / hysteresis across semantic action boundaries** rather than missing visible FIRE state.

## Development claim

> Treating gather operations as temporally extended primitives helps materially for a subset of founders, but the remaining FIRE failure is now concentrated at the transition from completed gather primitive to CRAFT_FIRE.

V7.12 therefore supports temporal action granularity as part of the problem, but does not establish a full commitment rescue.

## Next direction

**Stone Age V7.13 — FIRE Semantic Boundary Reset Control**

Use fresh founders and the same V7.12 training.

Primary representation:
- `FIRE_MINIMAL`

Evaluate the exact same final brain under:

1. `COMMIT_CONTINUING`
   - V7.12 commitment
   - preserve stream state across high-level primitive boundaries

2. `COMMIT_RESET_QUERY`
   - same commitment rule and 14-window budget
   - call `brain.reset()` immediately before each high-level brain query
   - learned weights remain unchanged

Primary question:

> Does clearing per-stream state at semantic action boundaries restore the cold static `CRAFT_FIRE` mapping after a gather primitive completes?

Interpretation:
- RESET_QUERY rescues FIRE -> stream-state hysteresis is the remaining bottleneck
- RESET_QUERY fails -> the discrepancy between cold static readout and dynamic action selection survives stream reset and requires a deeper act/predict or policy-state audit

Keep full 11 actions and do not reopen shared-brain memory/attention until this control is resolved.
