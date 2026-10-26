# Stone Age V7.13 — FIRE Semantic Boundary Reset Control

Status: **running protocol / frozen before run**

Cadence: **0.88.1**

V7.12 showed a partial FIRE commitment signal. Treating gather actions as temporally extended primitives improved the FIRE_MINIMAL median loop from 0% to 50%, but only 3/8 founders passed the frozen commitment gate.

Trace audit showed the remaining committed failures usually occur **after** the required resource has already been acquired. At that semantic boundary the visible FIRE_MINIMAL state is ready-to-craft, yet the continuing brain often repeats a gather action instead of selecting `CRAFT_FIRE`.

## Question

Does clearing Cadence's per-stream state at semantic high-level action boundaries restore the cold static `CRAFT_FIRE` mapping after a gather primitive completes?

## Scope

FIRE only.

Fresh founders: `76001..76008`.

Primary representation:
- `FIRE_MINIMAL`

The representation is unchanged from V7.11/V7.12:
- input 5 = `wood >= 4`
- input 6 = `stone >= 2`
- input 9 = `fire_exists`
- all other inputs = 0

## Training

Training is identical in structure to V7.12:

1. reset-per-row static bootstrap
2. DAgger64 learner-path teaching
3. full 192-row reset-per-row static replay
4. freeze the final trained brain
5. evaluate the exact same final brain under two execution modes

No learning occurs during the execution comparison.

## Execution modes

### COMMIT_CONTINUING

V7.12 commitment behavior:
- brain queried at high-level action boundaries
- `GATHER_WOOD` held until wood increases
- `GATHER_STONE` held until stone increases
- other actions execute one normal decision window
- continuing brain stream state is preserved between high-level queries

### COMMIT_RESET_QUERY

Identical execution except:
- immediately before **every high-level brain query**, call `brain.reset()`
- learned weights/records remain unchanged
- environment state is not reset
- current world/resource state continues normally

This gives each semantic high-level decision a cold stream boundary while preserving the learned policy and the exact same environment trajectory budget.

## Fairness

Both modes:
- use the same frozen final brain
- use the same held-out seeds and six FIRE variants
- have the same 14 decision-window environment budget
- use the same gather commitment rule
- receive no additional training or world time

The only difference is stream-state reset before a high-level query.

## Diagnostics

For every high-level query record:
- wood / stone / fire
- current environment action and action_progress
- chosen action
- whether query was preceded by `brain.reset()`
- decision windows consumed by the chosen primitive

Also record the first **ready-to-craft** boundary in each episode:
- `wood >= 4`
- `stone >= 2`
- `fire_exists == false`

and whether the chosen action was `CRAFT_FIRE`.

## Environment oracle

The deterministic caretaker must solve 6/6 held-out FIRE episodes for every founder.

## Frozen gates

Static:
- exact >=90%
- fresh >=80%

Loop:
- >=4/6 success

RESET_QUERY pass:
- median reset-query loop >=4/6
- median exact/fresh gates pass
- >=6/8 valid founders individually pass static + reset-query loop gates

Material reset effect:
- median RESET_QUERY loop gain >=2/6 (+33.3 percentage points) over COMMIT_CONTINUING

## Frozen interpretation

Classification precedence:

1. RESET_QUERY passes full criterion -> `FIRE_STREAM_STATE_RESET_RESCUE`
2. COMMIT_CONTINUING itself passes full criterion -> `FIRE_CONTINUING_COMMIT_PASS`
3. RESET_QUERY gains >=2/6 median loop but misses founder gate -> `PARTIAL_FIRE_STREAM_RESET_SIGNAL`
4. otherwise -> `FIRE_STREAM_STATE_RESET_UNRESOLVED`

No shared brain, memory/attention, hidden inventory, or reward-learning comparison is opened in V7.13.
