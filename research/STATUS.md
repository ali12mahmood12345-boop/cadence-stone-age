# Cadence Research Status

Updated: 2026-11-02

## Current Stone Age line

Cadence: `0.91.1`

### Confirmed / strongly established

#### V7.16R
`POSITIONAL_RECALL_TEMPORAL_HISTORY_CONFIRMED`

On the bounded five-event task, learned position Recall solved FIRST/LAST temporal-history retrieval while matched controls did not.

#### V7.27
Training-path steering established that Recall route strategy is learned plasticity:
- BLOCK_NEXT_TRAIN -> VALUE route
- BLOCK_VALUE_TRAIN -> NEXT route

#### V7.30
`NATIVE_BOUNDARY_ROUTE_STEERING_CONFIRMED`

Native `recall_boundary=True` reproduced the route-steering result without a manual zero START act. The manual START workaround is retired for the current Stone Age branch.

#### V7.31
`LEARNED_POSITION_MAP_ACQUISITION_PRIMARY_VARIABLE_LENGTH_CEILING_CONFIRMED`

One fixed analytic additive `P + length` map solved all 22 valid length/position combinations at 100%, while the learned BASE map remained around 70%. The representation is sufficient; acquisition is the bottleneck.

### Negative / narrowing results

#### V7.32
Current-attention target gating was not the primary ceiling. Removing the prior made BASE worse.

#### V7.33
An exact one-hot predecessor training target improved BASE only modestly (~70.0% -> ~73.8%). Perfect target estimation alone does not remove the ceiling.

#### V7.34
The residual ceiling was not explained by position `P_c` or by lowering `position_rate`. Lowering the rate from 0.10 to 0.02 was worse at matched dose.

#### V7.35
The residual ceiling was not explained by content-address learning or `P_c` alone. The cleanest arm (address off + `P_c` off) improved to ~78.9% BASE but remained below the perfect predecessor oracle.

### V7.36 — convergence / dose scaling

Question: with exact predecessor supervision, address learning off, `P_c=0`, and `position_rate=0.10`, does more balanced dose close the learned-map gap?

First run:
- only 2/8 founders completed all checkpoints because six hit Cadence's finite teaching free-phase budget;
- D198 median BASE: 83.1%
- D396 median BASE: 91.5%
- D792 median BASE: 97.6%
- D792 natural top-predecessor: 100%
- D792 direct learned-map top-predecessor: 100%

Formal classification remains inconclusive because the preregistered minimum valid-founder count was not met.

However, all seven founders that reached D396 improved over D198, and the two that reached D792 improved again. This is strong evidence for a convergence/sample-efficiency explanation.

### Current experiment

V7.36 FIXED reruns the exact same protocol with only the numerical solver budget changed:

- `learning_free_steps: 1024 -> 4096`
- warnings remain errors;
- no unsettled lesson is silently accepted;
- seeds, episodes, teacher, route, map settings, checkpoints and tests are unchanged.

See: [stone-age-v7-36](./stone-age-v7-36/README.md)

## Current working hypothesis

Much of the apparent variable-length position-map ceiling was finite-dose convergence of the released online position learner, not a hard representational limitation.

The fixed V7.36 8-founder rerun is the current confirmation step.

## Other confirmed research lines

- Representation Keys V0.3D — fresh confirmation on Cadence 0.85.1
- Memory Keys V0.4B — fresh confirmation on Cadence 0.85.1
- Stone Age V7.13R — `FIRE_STREAM_STATE_RESET_CONFIRMED`
- Stone Age V7.14R — `FOUR_SKILL_SHARED_SEMANTIC_BRIDGE_CONFIRMED`
- Stone Age V7.15R — `AUTONOMOUS_GOAL_ROUTING_CONFIRMED`
