# V7.45 — Dependence on exact predecessor teaching

Question: after solving numerical validity, can Cadence acquire variable-length temporal addressing using its native position-target learner rather than an exact predecessor label on every lesson?

Paired fresh founders 105001..105008, two freshly composed brains per seed. EXACT retains V7.41's exact predecessor teacher. NATIVE uses the released 0.91.1 position update and target estimation. In NATIVE, restore position P_c immediately after the native position update so it remains frozen, matching EXACT; preserve native x/b updates, target gating and energy bound. Native update refusal stops the arm. No exact predecessor label is supplied to the native position update. Answer labels and BLOCK_VALUE_TRAIN route steering remain, so this is reduced position supervision, not unsupervised learning.

Retain cadence-net 0.91.1 to isolate teaching changes from migration. Same native recall_boundary=True/no manual START, frozen content-address map, rate=0.10, qualified phases at residual tolerance=.003, 4096 free/nudged caps, damping=3 and initial_damping=1. Same 22 pairs, cumulative D198/D396/D792, train/cal/test generation and evaluation controls. Exact and native arms for each seed share identical episode panels. Alternate arm order across seeds.

Primary validity gate: at least six paired founders valid at all checkpoints. All accepted lessons must be qualified; no runtime errors or frozen-map violations. Report all failures. The exact arm is a contemporaneous positive control: median D792 BASE >=.90, map-top >=.95 and forced predecessor >=.95 are required before interpreting the native comparison. Inspect individual oracle results in both arms.

Primary effect: paired native-minus-exact BASE accuracy at D792, with founder-level distribution. A median gap of at most 5 percentage points plus native median BASE >=.90 and map-top >=.95 supports reduced exact-teacher dependence on this task. A larger negative gap with intact native oracle supports position-acquisition dependence; a weak native oracle requires a broader route/readout explanation. These are operational descriptive gates, not a powered equivalence test or a general autonomy claim.

Keep native teacher_accuracy null rather than interpreting lack of exact labels as zero accuracy. No inherited exact-teacher gate is applied to NATIVE. Record both arms independently and analyze matched complete pairs, with attrition shown separately. Sixteen full training runs may take considerably longer. Save after each arm; no within-arm resume. Version migration remains a separate research line.

