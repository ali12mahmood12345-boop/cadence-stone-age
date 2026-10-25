# Stone Age V7.3 — Balanced Teaching / State Contrast

Cadence: **0.88.0**

Status: **development complete**

Official classification:

`PERSISTENT_STATIC_ACQUISITION_BOTTLENECK`

## Question

Was V7.2's exact-acquisition failure caused by:

- prototype exposure imbalance,
- the one-row normalized teaching route,
- or insufficient state contrast?

## Design

Fresh founders: `63001..63008`.

All three arms used the same underlying single-skill Stone Age samples with equal exposure:

- 64 training rows per prototype
- 24 fresh-static rows per prototype

Arms:

1. `LEGACY_BALANCED`
   - one-row `Brain.lesson`
   - normalized teaching
   - equal prototype exposure

2. `DOC_BATCH32`
   - normalized teaching
   - 32-row batches
   - `brain.learner.step(brain.stimulus(x, memory=False), labels)`

3. `DOC_BATCH32_CONTRAST`
   - same batch route
   - threshold-coded action-relevant inventory state

Primary evaluation was cold `brain.predict` exact + fresh-static accuracy.

## Result

All **8/8 founders were valid**.

Final medians, EXACT / FRESH / CLOSED-LOOP(descriptive):

| Skill | LEGACY_BALANCED | DOC_BATCH32 | DOC_BATCH32_CONTRAST |
| --- | --- | --- | --- |
| FOOD | 50.0 / 50.0 / 0.0% | 25.0 / 25.0 / 0.0% | 0.0 / 0.0 / 0.0% |
| FIRE | 33.3 / 33.3 / 0.0% | 33.3 / 33.3 / 0.0% | 33.3 / 33.3 / 0.0% |
| HUNT | 50.0 / 49.3 / 0.0% | 33.3 / 33.3 / 0.0% | 33.3 / 33.3 / 0.0% |
| SHELTER | 66.7 / 66.7 / 50.0% | 33.9 / 33.3 / 0.0% | 33.3 / 33.3 / 0.0% |

No arm reached the frozen 90% exact / 80% fresh-static gate.

The documented batch-32 arm did not rescue acquisition; on this short dataset it was often worse than one-row normalized teaching.

Pairwise exact-readback descriptors:

- FOOD batch > legacy: 0/8, median gain -0.250
- FIRE: 0/8, median gain 0
- HUNT: 1/8, median gain -0.008
- SHELTER: 0/8, median gain -0.328

## Important interpretation correction

V7.3 does **not** cleanly prove that state contrast is ineffective.

The contrast manipulation was only tested on top of `DOC_BATCH32`, and this batch route had only 4–6 learner updates per skill because the entire dataset contained only 128–192 rows.

Cadence's 0.88 teaching guide describes normalized batch teaching as a many-lesson imitation point and explicitly notes that with only a few hundred corrections the founder teaching point can acquire faster.

Therefore:

- simple exposure balancing is ruled out as the sole fix;
- this short normalized batch-32 regime did not help;
- state contrast remains unresolved because it was confounded with the weak short-budget batch regime.

## Prototype pattern

The legacy-balanced arm still collapses mappings within each skill:

- FOOD often retains one of PICK/EAT and loses the other.
- FIRE tends to retain only one of CRAFT/WOOD/STONE.
- HUNT often retains a subset of KILL/SPEAR/STONE.
- SHELTER is strongest, often retaining two of three prototypes.

This looks like a low-budget multi-mapping acquisition problem more than a simple frequency imbalance.

## Next direction

**Stone Age V7.4 — Few-Lesson Teaching Regime Isolation**

Use the same balanced static single-skill datasets, but compare teaching regimes appropriate to the short correction budget:

- FOUNDER one-row `Brain.lesson`
- FOUNDER balanced minibatch route
- NORMALIZED one-row control
- optional repeated-epoch normalized batch only as a dose control

Primary evaluation remains cold `predict` exact/fresh.

Only after a teaching regime can reach high static acquisition should state contrast or closed-loop Stone Age be reopened.

No attention or episodic-memory test yet.
