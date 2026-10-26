# Stone Age V7.7R — Surprise-Corrected Contrast Integration Bridge

Status: **development complete**

Cadence: **0.88.1**

Official classification:

`SURPRISE_CONTRAST_STATIC_RESCUE_CLOSED_LOOP_BOTTLENECK`

## Question

Does the V7.6R threshold encoding, under the corrected 0.88.1 surprise rule, rescue real multiclass acquisition and closed-loop action switching in Stone Age?

## Arms

- `RAW18_SURPRISE_FULL11`
- `CONTRAST18_SURPRISE_FULL11`
- `CONTRAST18_SURPRISE_LOCAL`

All normalized teaching arms used `learning_surprise=True` from lesson 0, qualified teaching, modules `(32,16)`, one-row `Brain.lesson`, one pass.

RAW and CONTRAST full-11 used the same graph seed per founder/skill.

Fresh founders: `69001..69008`.

## Result

All **8/8 founders were valid**.

Median EXACT / FRESH / CLOSED-LOOP:

| Skill | RAW18_SURPRISE_FULL11 | CONTRAST18_SURPRISE_FULL11 | CONTRAST18_SURPRISE_LOCAL |
| --- | --- | --- | --- |
| FOOD | 50 / 50 / 0% | **100 / 100 / 0%** | **100 / 100 / 16.7%** |
| FIRE | 33.3 / 33.3 / 0% | **100 / 100 / 0%** | **100 / 100 / 33.3%** |
| HUNT | 82.8 / 81.9 / 33.3% | **100 / 100 / 100%** | **100 / 100 / 0%** |
| SHELTER | 66.7 / 66.7 / 0% | **100 / 100 / 0%** | **100 / 100 / 100%** |

Founder-level all-four readiness:

- RAW18_SURPRISE_FULL11: 0/8
- CONTRAST18_SURPRISE_FULL11: 0/8
- CONTRAST18_SURPRISE_LOCAL: 1/8

Static all-skill readiness:

- RAW18_SURPRISE_FULL11: fail
- CONTRAST18_SURPRISE_FULL11: **pass**
- CONTRAST18_SURPRISE_LOCAL: **pass**

## Interpretation

V7.7R cleanly separates **static policy acquisition** from **dynamic trajectory execution**.

The contrast representation now learns the multiclass skill policies essentially perfectly:

- FOOD 100/100
- FIRE 100/100
- HUNT 100/100
- SHELTER 100/100

This holds with the corrected surprise teaching rule and with the original 11-action output.

The remaining failure is therefore not basic static action association.

### Closed-loop boundary

FOOD, FIRE and SHELTER frequently fail after the first correct action because the real environment produces intermediate states that were not present in the static prototype curriculum.

Typical patterns:

- FOOD: first `PICK_BERRIES` is correct, then full-11 brains drift to unrelated actions before the berry action completes.
- FIRE: first missing-resource action is correct, then brains repeat or switch resource actions instead of completing the prerequisite and crafting.
- SHELTER: build/sleep state transitions are statically learned, but full-11 output can select untaught actions on intermediate states.
- HUNT is the important positive control: `CONTRAST18_SURPRISE_FULL11` reaches 100% median closed-loop success. Its post-craft state closely matches the taught HUNT_KILL prototype, so the static-to-dynamic bridge already works there.

The local-output control improves FOOD/FIRE/SHELTER in several founders, showing that unused-action competition is a secondary factor, but it does not solve the trajectory problem consistently.

## Development claim

> V7.6R contrast encoding solves the tested multiclass static Stone Age acquisition problem under corrected 0.88.1 teaching. The remaining boundary is coverage and stability on real intermediate trajectory states.

This is still development evidence, not a fresh confirmation.

## Next direction

**Stone Age V7.8 — Caretaker / DAgger Dynamic-State Bridge**

Keep:

- cadence-net 0.88.1
- CONTRAST18
- full 11 actions
- `learning_surprise=True` from lesson 0

Bootstrap with the same static curriculum, then let the brain act greedily in the real StoneAgeEnv while a deterministic caretaker labels the **same states the brain actually reaches**.

At each decision:

1. observe current state
2. brain chooses greedy action
3. caretaker supplies the correct skill action for that same state
4. teach with `brain.lesson(observation, caretaker_action)`
5. execute the brain's chosen action
6. continue from the resulting state

Primary comparison:

- STATIC_ONLY
- CARETAKER_DAGGER

Optional matched control:

- SCRIPTED_EXPERT_TRAJECTORY training, to distinguish mere trajectory coverage from brain-path-specific correction.

Measure:

- closed-loop success
- caretaker corrections required
- agreement on expert trajectory states
- retention of V7.7R static exact/fresh accuracy

Do not reopen shared-brain memory/attention until this dynamic-state bridge is resolved.
