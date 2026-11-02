# Cadence Stone Age V7.36 — Position Convergence / Dose Scaling

## Question

With the V7.35 clean exact-teacher configuration, is the remaining ~79% BASE result a structural ceiling or simply incomplete convergence of the released online position-map optimizer?

## Fixed configuration

- `cadence-net==0.91.1`
- Fresh founders `102001..102008`
- Variable lengths 3..7, 22 valid `(length, position)` pairs
- Native `recall_boundary=True`; no manual START
- Exact one-hot predecessor position teacher on every training lesson
- `recall_address=0.0` (content-address map frozen)
- Position `P_c` frozen exactly at zero
- `recall_position_rate=0.10`
- Released 0.91.1 cortex-energy bound retained
- `BLOCK_VALUE_TRAIN` keeps acquisition on predecessor->next
- `learning_free_steps=4096` at every stage

The only difference from the first V7.36 run is the free-phase settling budget: the original used the composed default 1024 and six founders eventually exhausted it.

## Cumulative checkpoints

One brain per founder trains continuously. Every checkpoint is exactly balanced across all 22 pairs:

- D198: 198 examples/pair = 4,356 lessons
- D396: +198 examples/pair = 8,712 cumulative lessons
- D792: +396 examples/pair = 17,424 cumulative lessons

The same held-out calibration/test panels are reused at each checkpoint.

## Measurements

At each checkpoint:

- BASE behavior
- FORCE_PREDECESSOR ceiling
- FORCE_TARGET wrong-route control
- natural top-predecessor attention
- direct learned-map geometry over all 22 pairs: top-age correctness, predecessor softmax mass, and margin

## Main interpretation

- D792 >=90% BASE and >=95% map-top-predecessor: finite-dose convergence explains most of the residual ceiling.
- Strong monotonic improvement but D792 <90%: convergence matters, but a residual ceiling persists.
- Little D792 improvement over D198: true plateau under the released online update becomes likely.

## Fixed-rerun note

The first V7.36 run showed a strong convergence curve but only 2/8 founders reached D792 because six founders triggered Cadence's finite teaching free-phase budget warning.

This rerun raises only `learning_free_steps` from 1024 to 4096. The warning remains promoted to an error; no unsettled lesson is silently accepted. All task, seed, learning-rule, position-map, route-steering, checkpoint, and evaluation settings are unchanged.
