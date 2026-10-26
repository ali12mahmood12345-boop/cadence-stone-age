# Stone Age V7.12 — FIRE Temporal Action-Commitment Control

Status: **running protocol / frozen before run**

Cadence: **0.88.1**

V7.11 showed that FIRE remains dynamically unstable even after nuisance removal and explicit action/progress state. The failure traces repeatedly show the brain changing actions in the middle of a gather operation that requires multiple consecutive 0.55 s decision windows.

## Question

Does the already-learned FIRE policy succeed when `GATHER_WOOD` and `GATHER_STONE` are treated as temporally extended motor primitives rather than re-decided every 0.55 seconds?

## Scope

FIRE only.

Fresh founders: `75001..75008`.

Representation arms:
- `CONTRAST18`
- `FIRE_MINIMAL` — primary
- `FIRE_MINIMAL_PLUS_PROGRESS` — diagnostic

All training is identical in structure to V7.11:
1. reset-per-row static bootstrap
2. DAgger64 learner-path teaching
3. full reset-per-row static replay
4. freeze the final trained brain
5. evaluate that same frozen brain under two execution modes

No learning occurs during the execution-mode comparison.

## Evaluation modes

### DECISION_LEVEL

Current Stone Age controller:
- query the brain every decision window
- one decision window = existing `FRAMES_PER_DECISION`
- switching action resets `action_progress`
- total FIRE evaluation budget = 14 decision windows

### COMMIT_TO_COMPLETION

At each high-level brain query:

- if action is `GATHER_WOOD`, repeatedly execute that same action until:
  - wood increases, or
  - the shared 14-window episode budget is exhausted, or
  - the agent dies

- if action is `GATHER_STONE`, repeatedly execute that same action until:
  - stone increases, or
  - the shared 14-window episode budget is exhausted, or
  - the agent dies

- all other actions execute for exactly one ordinary decision window, then the brain is queried again

The brain is therefore not allowed to switch away from a gather primitive before its immediate resource effect completes.

## Fairness constraint

Both modes have the **same total 14 decision-window environment budget**.

Commit mode does not receive extra world time. Internal gather windows consume the same budget that would have been available to DECISION_LEVEL.

The only difference is the frequency at which the brain may reconsider an unfinished gather action.

## Environment oracle

The deterministic caretaker must again solve 6/6 held-out FIRE episodes for every founder.

## Evaluation

For each trained representation/founder:
- exact static accuracy
- fresh static accuracy
- 6 DECISION_LEVEL held-out FIRE episodes
- 6 COMMIT_TO_COMPLETION episodes on the same seeds/variants
- action traces
- high-level query count
- total decision-window count
- committed primitive lengths

## Frozen gates

Static:
- exact >=90%
- fresh >=80%

Loop:
- >=4/6 success

Representation-level commitment pass:
- median commit loop >=4/6
- static median exact/fresh gates pass
- >=6/8 founders individually pass static + commit-loop gates

Material commitment improvement:
- median COMMIT_TO_COMPLETION loop gain >=2/6 (+33.3 percentage points) over DECISION_LEVEL for the same representation

## Frozen interpretation

Classification precedence:

1. `FIRE_MINIMAL` commitment passes -> `FIRE_TEMPORAL_COMMITMENT_RESCUE`
2. only `FIRE_MINIMAL_PLUS_PROGRESS` commitment passes -> `FIRE_PROGRESS_PLUS_COMMITMENT_REQUIRED`
3. only `CONTRAST18` commitment passes -> `FIRE_CONTRAST_COMMITMENT_PASS`
4. any representation gains >=2/6 median loop but misses the founder gate -> `PARTIAL_FIRE_COMMITMENT_SIGNAL`
5. otherwise -> `FIRE_TEMPORAL_COMMITMENT_UNRESOLVED`

No shared brain, memory/attention, hidden inventory, or reward-learning comparison is opened in V7.12.
