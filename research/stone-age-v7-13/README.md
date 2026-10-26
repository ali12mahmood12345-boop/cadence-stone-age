# Stone Age V7.13 — FIRE Semantic Boundary Reset Control

Status: **development complete**

Cadence: **0.88.1**

Official frozen classification:

`FIRE_STREAM_STATE_RESET_RESCUE`

## Question

Does clearing Cadence's per-stream state at semantic high-level action boundaries restore the correct FIRE transition after a committed gather primitive?

## Frozen design

FIRE only.

Fresh founders: `76001..76008`.

Representation:
- `FIRE_MINIMAL`

Training:
1. reset-per-row static bootstrap
2. DAgger64 learner-path teaching
3. full reset-per-row static replay
4. freeze final brain
5. evaluate the exact same brain under two execution modes

Execution modes:

### COMMIT_CONTINUING
- gather actions committed to immediate completion
- per-stream brain state preserved across high-level queries

### COMMIT_RESET_QUERY
- identical commitment rule
- call `brain.reset()` immediately before every high-level query

Both modes:
- same six held-out seeds/variants
- same 14 decision-window budget
- same frozen learned weights
- no additional learning

## Result

All **8/8 founders were valid**.

Caretaker oracle: **48/48**.

Static:
- median exact: **100%**
- median fresh: **100%**

Loop medians:
- COMMIT_CONTINUING: **100%**
- COMMIT_RESET_QUERY: **100%**

Founder readiness:
- COMMIT_CONTINUING: **5/8**
- COMMIT_RESET_QUERY: **8/8**

Ready-to-craft boundary accuracy:
- COMMIT_CONTINUING median: **50%**
- COMMIT_RESET_QUERY median: **100%**

Efficiency medians:
- COMMIT_CONTINUING: 2.5 high-level queries / 4.5 windows
- COMMIT_RESET_QUERY: 2.0 high-level queries / 3.5 windows

Pairwise founder loop comparison:
- reset wins: 3/8
- ties: 5/8
- losses: 0/8

The frozen full-pass rule is satisfied because RESET_QUERY passes the median static/loop gates and >=6/8 founder readiness.

## Interpretation

V7.13 confirms the mechanism predicted from V7.12:

> FIRE failures after a completed gather primitive are caused by continuing per-stream state biasing the next semantic action selection.

The visible FIRE_MINIMAL state was already sufficient:
- wood threshold
- stone threshold
- fire state

The learned cold policy was also already correct at 100/100 static accuracy.

What prevented reliable execution was **stream-state hysteresis across the semantic primitive boundary**.

Resetting the brain before each high-level query restores the correct ready-to-craft decision reliably:
- ready-to-craft accuracy rises from median 50% to 100%
- all 8/8 founders pass the final static + loop gate
- no founder is harmed by reset-query in the paired comparison

Therefore the current FIRE controller recipe is:

1. use high-level temporally extended gather primitives
2. commit gather actions until the immediate resource increment completes
3. reset Cadence stream state before the next semantic high-level query

This is a controller-boundary solution, not additional representation learning.

## Scientific status

This remains a **development result**, because the semantic-reset hypothesis was derived from V7.12 traces and V7.13 tested that targeted mechanism.

The next step should be exact fresh confirmation before reopening broader Stone Age integration.

## Next direction

**Stone Age V7.13R — Fresh FIRE Boundary Confirmation**

Freeze the successful recipe unchanged:

- FIRE_MINIMAL
- same static bootstrap
- same DAgger64
- same full reset replay
- same gather commitment
- reset before every high-level semantic query
- same 14-window budget
- same exact/fresh/loop gates

Use a larger untouched founder panel.

Recommended:
- founders `77001..77016`
- minimum valid 12/16
- confirmation requires:
  - median exact >=90%
  - median fresh >=80%
  - median loop >=4/6
  - >=12/16 individually ready
  - ready-to-craft accuracy median 100%

No representation changes, no new teaching recipe, and no post-hoc mechanism edits.

If confirmed, the FIRE dynamic boundary can be considered resolved strongly enough to reopen the next Stone Age integration stage.
