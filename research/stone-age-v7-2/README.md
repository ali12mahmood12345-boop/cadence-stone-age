# Stone Age V7.2 — Acquisition Microscope

Cadence: **0.88.0**

Status: **development complete**

Official classification:

`STONE_AGE_BASIC_ACQUISITION_BOTTLENECK`

## Question

Where does Stone Age acquisition break:

- exact taught-state retention,
- fresh-state generalization,
- closed-loop stage switching,
- or cross-skill interference?

## Design

Fresh founders: `62001..62008`.

Matched branches:

- FOOD-only brain
- FIRE-only brain
- HUNT-only brain
- SHELTER-only brain
- one shared four-skill brain

For each skill, the single-skill and shared branches received the exact same lesson observation vectors and labels. The shared brain additionally learned the other three skills.

After every curriculum stage V7.2 measured:

1. exact taught-state readback
2. fresh static-state generalization
3. closed-loop chain execution

## Final result

All **8/8 founders were valid**.

Final median single-skill exact / static / closed-loop:

- FOOD: **54.2% / 50.0% / 0%**
- FIRE: **41.9% / 33.3% / 0%**
- HUNT: **72.7% / 66.7% / 100%**
- SHELTER: **72.7% / 66.7% / 0%**

Final median shared exact / static / closed-loop:

- FOOD: **50.0% / 50.0% / 0%**
- FIRE: **29.0% / 33.3% / 0%**
- HUNT: **50.8% / 50.0% / 0%**
- SHELTER: **66.7% / 66.7% / 0%**

## Key mechanism finding

The primary bottleneck is already present in the **single-skill brains**, before cross-skill interference is required to explain the failure.

Prototype-level readback shows a strong terminal-action collapse:

- FOOD_EAT is usually retained, while FOOD_PICK is usually read back as EAT.
- FIRE_CRAFT is usually retained, while FIRE_WOOD / FIRE_STONE are usually read back as CRAFT_FIRE.
- HUNT_KILL and HUNT_SPEAR are mostly retained, while HUNT_STONE is usually read back as CRAFT_SPEAR.
- SHELTER_BUILD and SHELTER_SLEEP are mostly retained, while SHELTER_WOOD is usually read back as BUILD_SHELTER.

So adjacent prerequisite states are not being maintained as distinct action mappings.

## Important HUNT exception

HUNT is the strongest single-skill exception:

- final single HUNT exact: **72.7%**
- fresh static: **66.7%**
- closed-loop: **100%**

The shared HUNT brain falls to:

- exact **50.8%**
- static **50.0%**
- closed-loop **0%**

This is descriptive evidence that cross-skill interference exists for HUNT, but the frozen global diagnosis remains BASIC_ACQUISITION because single-skill exact readback still misses the 90% gate.

## Stage trajectory

Closed-loop single-skill HUNT:

- stage1: 0%
- stage2: 0%
- stage3: 66.7%
- stage4: 100%

Shared HUNT remained 0% at every stage.

Single SHELTER briefly reached 16.7% at stage3 but returned to 0% after mixed replay.

## Interpretation

V7.2 shows that the next fix should not be attention or episodic memory.

The first problem is **within-skill state discrimination / retention**: nearby inventory states that require different actions collapse toward the terminal action.

A secondary cross-skill interference effect is visible, especially in HUNT, but it is not yet the first bottleneck.

## Next direction

**Stone Age V7.3 — State Contrast / Balanced Acquisition**

Before changing architecture or memory:

- equalize exposure counts across every prototype within a skill,
- remove the backward-curriculum frequency advantage for terminal actions,
- test exact readback on the same single-skill tasks,
- include a matched amplified-state-contrast arm only as a diagnostic if balanced exposure alone fails.

The immediate question is whether the collapse is caused by **lesson-frequency imbalance** or by insufficient separability of adjacent Stone Age observation states.
