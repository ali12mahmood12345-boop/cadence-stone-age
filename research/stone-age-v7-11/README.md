# Stone Age V7.11 — FIRE Dynamic Invariance Microscope

Status: **development complete**

Cadence: **0.88.1**

Official classification:

`FIRE_DYNAMIC_INVARIANCE_UNRESOLVED`

## Question

Does nuisance-invariant FIRE state preserve the correct gather/craft action across multiple decisions, or is explicit action/progress state required?

## Frozen design

FIRE only.

Fresh founders: `74001..74008`.

Representation arms:

- `CONTRAST18`
- `FIRE_MINIMAL`
- `FIRE_MINIMAL_PLUS_PROGRESS`

All arms used:
- same graph seed per founder
- full 11 actions
- modules `(32,16)`
- normalized qualified teaching
- `learning_surprise=True` from lesson 0
- reset-per-row static bootstrap
- DAgger64
- one full reset-per-row static replay pass
- 6 held-out FIRE loop episodes

Environment validity required the deterministic caretaker to solve all 6 held-out episodes.

## Result

All **8/8 founders were valid**.

Caretaker oracle: **48/48 held-out episodes**.

### Final medians after reset replay — EXACT / FRESH / CLOSED-LOOP

| Arm | Exact | Fresh | Loop | Final-ready founders |
| --- | ---: | ---: | ---: | ---: |
| CONTRAST18 | 100% | 100% | 0% | 2/8 |
| FIRE_MINIMAL | 100% | 100% | 0% | 2/8 |
| FIRE_MINIMAL_PLUS_PROGRESS | 100% | 100% | 25% | 0/8 |

No arm passed the frozen representation criterion.

Pairwise final loop improvement over CONTRAST18:
- FIRE_MINIMAL: median gain 0.0
- FIRE_MINIMAL_PLUS_PROGRESS: median gain 0.0

Therefore neither nuisance removal nor explicit action/progress state meets the frozen rescue threshold.

## What the traces add

The remaining failure is highly structured.

For `FIRE_MINIMAL_PLUS_PROGRESS`, common first failures occur exactly on action-continuation states:

- missing stone, current action `GATHER_STONE`, progress ~0.55 -> switches to `GATHER_WOOD`
- missing wood, current action `GATHER_WOOD`, progress ~0.55 -> switches early to `CRAFT_FIRE`
- after a resource becomes ready, some founders continue the previous gather action rather than switching to `CRAFT_FIRE`

Success patterns are frequently resource-branch specific:
- some founders solve all three missing-wood variants but no missing-stone variants
- others solve all three missing-stone variants but no missing-wood variants

This is important because the deterministic caretaker demonstrates the required temporal structure:

- wood gathering needs repeated consecutive `GATHER_WOOD` decisions
- stone gathering needs even longer repeated consecutive `GATHER_STONE` decisions
- only after the inventory threshold changes should the policy switch to `CRAFT_FIRE`

The explicit progress representation therefore contains useful state, but learner-path DAgger does not reliably stabilize the required continuation policy.

## Replay interaction

Dynamic progress mappings are also fragile under later cold static replay.

In the PLUS_PROGRESS arm:
- founder 74005 was 6/6 post-DAGGER and fell to 3/6 after reset replay
- founder 74006 was 6/6 post-DAGGER and fell to 3/6 after reset replay

So V7.11 reveals two interacting boundaries:

1. **mid-action continuation / temporal commitment**
2. **retention of progress-conditioned dynamic mappings during static reconsolidation**

## Development claim

> FIRE is no longer primarily a static representation problem. The brain can recover perfect cold prerequisite mappings, but the decision-level controller often re-decides before a multi-decision gather action has completed.

The current evidence does **not** support either:
- `FIRE_NUISANCE_INVARIANCE_RESCUE`
- `FIRE_PROGRESS_STATE_REQUIRED`

The progress arm is informative but not sufficient.

## Next direction

**Stone Age V7.12 — FIRE Temporal Action-Commitment Control**

Before adding more learning complexity, directly test whether the remaining FIRE failure is caused by querying the brain too often during a semantically continuing action.

Use the same final FIRE brains and compare two evaluation modes:

### DECISION_LEVEL
Current evaluation:
- brain queried every 0.55 s decision window
- switching actions resets gather progress

### COMMIT_TO_COMPLETION
Brain chooses a high-level FIRE action once.

If it chooses:
- `GATHER_WOOD`: execute that same action until wood increases or a fixed safety cap is reached
- `GATHER_STONE`: execute that same action until stone increases or a fixed safety cap is reached
- `CRAFT_FIRE`: execute once

Then query the brain again only after the action has completed or failed.

Primary representation:
- FIRE_MINIMAL

Diagnostic representation:
- FIRE_MINIMAL_PLUS_PROGRESS

No additional learning is required for the core commitment control.

Primary question:

> Does the already-learned high-level FIRE policy succeed when gather actions are treated as temporally extended motor primitives rather than re-decided every 0.55 seconds?

Interpretation:
- commitment rescues FIRE -> temporal action granularity / persistence is the bottleneck
- commitment still fails -> action selection itself remains unstable even at meaningful action boundaries

Do not reopen shared-brain memory/attention until this control is resolved.
