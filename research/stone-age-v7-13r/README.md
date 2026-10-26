# Stone Age V7.13R — Fresh FIRE Boundary Confirmation

Status: **fresh confirmation complete**

Cadence: **0.88.1**

Official classification:

`FIRE_STREAM_STATE_RESET_CONFIRMED`

## Purpose

V7.13R was a strict fresh confirmation of the successful V7.13 FIRE controller recipe.

No alternate arms and no mechanism changes were allowed.

Fresh founders:
- `77001..77016`

Frozen recipe:
- `FIRE_MINIMAL`
- reset-per-row static bootstrap
- DAgger64 learner-path teaching
- full 192-row reset-matched static replay
- commit gather primitive until the immediate resource increment completes
- `brain.reset()` before every semantic high-level query
- 14 total decision-window episode budget
- no evaluation learning

## Result

All **16/16 founders were valid**.

Caretaker oracle:
- **96/96**

Confirmation medians:
- exact: **100%**
- fresh: **100%**
- loop: **100%**
- ready-to-craft accuracy: **100%**
- high-level queries / decision windows: **2.0 / 3.5**

Founder readiness:
- **16/16**
- frozen requirement: >=12/16

Every frozen confirmation gate passed.

## Robustness

The confirmation is stronger than the minimum gate:

- every founder achieved 6/6 held-out FIRE loop success
- every founder reached 100% exact static accuracy
- every founder reached 100% fresh static accuracy
- every founder chose `CRAFT_FIRE` correctly at every first ready-to-craft boundary

Training histories were heterogeneous:
- DAgger accepted corrections ranged from 15 to 55
- DAgger pre-lesson agreement ranged from 15.6% to 90.6%
- final reset replay accepted corrections ranged from 0 to 92

Despite that variability, all 16 founders converged to the same successful final behavior.

## Confirmed development finding

The FIRE dynamic boundary is now considered confirmed for this controller setup:

> FIRE_MINIMAL + temporally extended gather primitives + stream reset before each semantic high-level query reliably restores the intended FIRE policy.

The important mechanism is not additional visible FIRE state.

The critical controller boundaries are:

1. do not re-decide inside an unfinished gather primitive
2. after the primitive completes, clear Cadence per-stream state before the next semantic decision

This preserves the correct cold learned mapping at the semantic transition to `CRAFT_FIRE`.

## Scientific status

Unlike V7.13, which was a targeted development test derived from V7.12 traces, V7.13R used a larger untouched founder panel and made no recipe changes.

Therefore:

`FIRE_STREAM_STATE_RESET_CONFIRMED`

is now the confirmed FIRE boundary result for the current Stone Age controller architecture.

## Next direction

**Stone Age V7.14 — Four-Skill Semantic Integration Bridge**

The FIRE-specific mechanism is resolved strongly enough to reopen broader Stone Age integration.

The next stage should test whether the successful single-skill policies can coexist in one shared controller without reopening low-level persistence failures.

Recommended structure:

- explicit task/goal context during the first shared-brain integration test
- one shared full-11-action brain
- semantic task-state representation rather than raw nuisance-heavy state
- retain reset-before-independent-teaching
- retain semantic-boundary stream resets
- retain temporally extended motor primitives for actions that require persistence
- compare against the already-established separate-brain skill controls

Primary question:

> Can one Cadence brain retain and execute FOOD, FIRE, HUNT and SHELTER policies together when task identity and semantic action boundaries are made explicit?

Do not add attention or episodic memory in the first shared-brain bridge. First establish plain shared-capacity and interference.
