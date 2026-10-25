# Stone Age V7.1 — Acquisition Readiness

Cadence: **0.88.0**

Status: **development / running**

V7 showed that the hidden-memory comparison was premature because median evaluation fire, spear, shelter and food-use rates were zero across all arms.

V7.1 asks the prerequisite question first:

> Can one visible-world Cadence brain acquire and execute the intended Stone Age chains at all?

## Skills

- FOOD: `PICK_BERRIES -> EAT`
- FIRE: gather missing wood/stone -> `CRAFT_FIRE`
- HUNT: `CRAFT_SPEAR -> HUNT_RABBIT`
- SHELTER: `BUILD_SHELTER -> SLEEP`

## Curriculum

Backward curriculum on one shared brain:

1. terminal useful actions
2. immediate predecessors + terminal replay
3. missing-resource states + previous skills
4. balanced mixed replay

Every teacher example begins after `brain.reset()`, so acquisition cannot depend on an accidental carried working trace.

## Strict exam

Fresh founders: `61001..61008`.

For each founder:
- trained brain receives the frozen curriculum
- same-seed untrained brain is the control
- both face identical fresh teacher-independent scenarios
- 3 variants per skill
- real headless Stone Age mechanics
- greedy `brain.act` only
- no lessons
- no reward feedback

The trained brain is checkpointed before exam so a passing acquired brain can be reused unchanged in the next hidden-memory experiment.

## Frozen readiness signal

`STONE_AGE_ACQUISITION_READINESS_SIGNAL` requires:

- >=6 valid founders
- median FOOD >=2/3
- median FIRE >=2/3
- median HUNT >=2/3
- median SHELTER >=2/3
- median overall >=80%
- >=6 founders pass all four skills at >=2/3
- trained beats untrained in >=6 founders
- median trained-untrained overall gain >=+0.40

No result is claimed until the run completes.
