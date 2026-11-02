# Stone Age V7.28-V7.36 — Native Boundary and Variable-Length Position Acquisition

Cadence: `0.91.1`

This document summarizes the current Stone Age learned-Recall line. The task is a controlled component benchmark, not a full-game intelligence claim.

## V7.28 — native Recall boundary equivalence

Compared:
- no boundary
- manual zero START
- native `recall_boundary=True`

The frozen equivalence gates were not all met, so the run was formally inconclusive. However, manual and native boundary arms showed similar Recall geometry and both exposed the P1 predecessor boundary. The boundary arms also showed a shared read-strength penalty relative to the no-boundary later-position reads.

Interpretation: no evidence that native boundary was semantically different from manual START, but whole-brain equivalence was the wrong target because manual START is a real sensory act while the native boundary is a silent Recall slot.

## V7.29 — boundary read-strength oracle

The exact-predecessor oracle showed that manual START and native boundary use the same predecessor->next causal mechanism, while founder-level neural state differences remained.

Result: retire the goal of proving whole-brain manual/native equivalence.

## V7.30 — native-boundary route steering

The V7.27 route-steering experiment was rerun with native `recall_boundary=True` and no manual START.

Result:
- BLOCK_NEXT_TRAIN -> VALUE route in 8/8 founders
- BLOCK_VALUE_TRAIN -> NEXT route in 8/8 founders
- matching oracle reached 100%

Diagnosis:

`NATIVE_BOUNDARY_ROUTE_STEERING_CONFIRMED`

The manual START workaround is retired.

## V7.31 — analytic position map

Variable lengths 3..7 produce 22 valid `(length, position)` combinations.

The same trained brain was tested with:
- BASE learned Cadence position map
- one fixed analytic predecessor map
- per-trial predecessor oracle
- deliberately wrong target-age map
- analytic predecessor with `next` removed

The analytic additive map implements the predecessor age rule from the existing explicit query:

`age = length - position_zero_based`

Results:
- learned BASE ~70.8%
- analytic predecessor map 100%
- forced predecessor 100%
- wrong target map ~1%
- correct predecessor with next removed ~33%

Diagnosis:

`LEARNED_POSITION_MAP_ACQUISITION_PRIMARY_VARIABLE_LENGTH_CEILING_CONFIRMED`

The representation can express the rule perfectly; learning the map is the bottleneck.

## V7.32 — current-attention prior gating

Hypothesis: multiplying the position lesson target by the current attention prior may self-lock wrong addresses.

Paired result:
- released gated learner BASE ~69.7%
- ungated target BASE ~58.2%
- both predecessor oracles 100%

The released target also corrected wrong weak-pair priors slightly more often than the ungated target.

Conclusion: current-attention prior gating is not the primary ceiling and appears stabilizing in this task.

## V7.33 — exact predecessor teacher

The position learner was given the exact predecessor slot as a one-hot training target.

Results:
- founder target BASE ~70.0%
- exact target BASE ~73.8%
- both predecessor oracles 100%
- exact target diagnostics: 100% correct

Diagnosis:

`POSITION_MAP_UPDATE_INTERFERENCE_REMAINS_AFTER_EXACT_TARGET`

Imperfect target estimation contributes only modestly.

## V7.34 — P_c and position-rate interference

Every arm used the exact predecessor teacher.

Compared:
- full map, rate 0.10
- `P_c` frozen, rate 0.10
- full map, rate 0.02
- `P_c` frozen, rate 0.02

Results:
- freezing `P_c` gave only a small gain
- lowering the rate made performance substantially worse at matched dose
- all predecessor oracles remained 100%

Diagnosis:

`POSITION_UPDATE_INTERFERENCE_NOT_EXPLAINED_BY_PC_OR_RATE`

## V7.35 — content-address and P_c interference

Every arm used exact supervision and `position_rate=0.10`.

Compared address learning ON/OFF crossed with position `P_c` ON/OFF.

Results:
- ADDR_ON_PC_ON ~70.9%
- ADDR_OFF_PC_ON ~70.8%
- ADDR_ON_PC_OFF ~77.4%
- ADDR_OFF_PC_OFF ~78.9%
- all predecessor oracles 100%

Diagnosis:

`POSITION_CEILING_NOT_EXPLAINED_BY_ADDRESS_OR_PC`

Removing `P_c` helps modestly; address learning alone is not the main cause.

## V7.36 — convergence / dose scaling

The clean V7.35 configuration was held fixed:
- exact predecessor teacher
- content-address learning off
- position `P_c=0`
- `position_rate=0.10`
- native boundary
- predecessor->next acquisition route

One brain per founder trains continuously at balanced cumulative checkpoints:
- D198: 198 examples per pair
- D396: 396 examples per pair
- D792: 792 examples per pair

### First run

Only 2/8 founders completed all checkpoints because six founders eventually exhausted the default finite teaching free-phase budget.

Among the completed founders:
- D198 BASE 83.1%
- D396 BASE 91.5%
- D792 BASE 97.6%
- D792 natural top-predecessor 100%
- D792 direct map top-predecessor 100%

Across the seven founders that reached D396, every founder improved from D198.

Formal classification:

`POSITION_CONVERGENCE_DOSE_TEST_INCONCLUSIVE`

The validity failure is numerical/settling-budget related, not a failed scientific prediction.

### V7.36 FIXED

The confirmation rerun changes only:
- `learning_free_steps: 1024 -> 4096`

Warnings remain promoted to errors and no unsettled lesson is silently accepted.

If the fixed 8-founder run reproduces the monotonic curve and reaches high D792 behavior/map correctness, the intended diagnosis is:

`FINITE_DOSE_CONVERGENCE_EXPLAINS_POSITION_MAP_CEILING`

## Current interpretation

The sequence from V7.31 through V7.36 strongly shifts the explanation away from a hard representational ceiling.

The current evidence says:
1. the additive P+length representation is sufficient;
2. the predecessor->next downstream route is perfect-capable;
3. target quality, current-attention gating, P_c, content-address learning, and a lower position rate do not individually explain the residual gap;
4. increased balanced dose produces large, monotonic gains and can drive the learned map to complete top-address correctness in the founders that finish.

The full V7.36 fixed rerun is the current confirmation step.
