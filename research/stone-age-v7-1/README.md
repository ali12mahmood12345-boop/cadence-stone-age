# Stone Age V7.1 — Acquisition Readiness

Cadence: **0.88.0**

Status: **development complete — failed readiness**

Official classification:

`NO_STONE_AGE_ACQUISITION_READINESS`

## Result

Fresh founders: `61001..61008`.

All **8/8 founders were valid** and every founder accepted **484/484 lessons with zero refusals**.

Median trained strict-exam success:

- FOOD: **0%**
- FIRE: **0%**
- HUNT: **0%**
- SHELTER: **0%**
- OVERALL: **0%**

Median untrained overall: **0%**.

Ready founders: **0/8**.

Only two founders showed any complete-skill success:

- 61003: SHELTER 100%
- 61007: FIRE 33.3%, SHELTER 100%

## Diagnostic

The failure was not lesson refusal. It was stage-switch / shared-policy collapse.

Typical trained traces:

- repeated `EAT` before berries existed
- repeated `GATHER_WOOD` after enough wood had already been acquired
- almost no `CRAFT_FIRE`
- almost no `CRAFT_SPEAR`
- repeated `SLEEP` before shelter existed

Across all trained strict exams, the terminal transition actions were very rare:

- FIRE emitted only **2 CRAFT_FIRE** actions
- HUNT emitted only **3 CRAFT_SPEAR** actions
- SHELTER emitted only **6 BUILD_SHELTER** actions

So the shared 11-action policy often learned a dominant stage action but did not reliably switch when inventory/state changed.

## Interpretation

V7.1 does **not** license another hidden-inventory memory test.

The next experiment should determine whether:

1. each skill can be learned by itself,
2. interference appears only when all four skills share one brain,
3. exact taught-state readback succeeds but closed-loop execution fails.

## Next

**Stone Age V7.2 — Acquisition Microscope**

Compare:

- separate FOOD brain
- separate FIRE brain
- separate HUNT brain
- separate SHELTER brain
- matched shared four-skill brain

Measure:

1. exact prototype readback
2. fresh static-state generalization
3. closed-loop chain execution

Do not tune attention or episodic memory yet.
