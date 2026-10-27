# Stone Age V7.16R — Fresh Positional Recall Temporal-History Confirmation

Status: **fresh confirmation complete**

Cadence: **0.89.0**

Official frozen classification:

`POSITIONAL_RECALL_TEMPORAL_HISTORY_CONFIRMED`

## Strict replication

V7.16R reused the exact V7.16 `run_founder()` implementation unchanged.

Fresh founders:
- `84001..84016`

Paired-valid founders:
- **14/16**
- frozen minimum: 12/16

The task remained:
- five Stone Age resource events
- first and last forced different
- identical FIRST/LAST query observations
- answer with the semantic action matching the queried temporal endpoint
- 1200 paired training episodes
- 240 paired held-out episodes
- lesson before query act
- recall recency disabled

Arms:
- POSITION32
- POSITION0
- RECALL_OFF

RECALL_OFF remained a no-Recall baseline with the default working trace retained.

## Confirmed result

### POSITION32

Median held-out performance across paired-valid founders:
- overall: **100%**
- FIRST: **100%**
- LAST: **100%**

Mean:
- overall: **97.98%**
- FIRST: **96.44%**
- LAST: **99.52%**

Robust founders:
- both FIRST and LAST >=80%: **13/14**
- frozen requirement: >=12

Position maps moved:
- **14/14**
- frozen requirement: >=12

### POSITION0

Median:
- overall: **48.8%**
- FIRST: **23.8%**
- LAST: **70.4%**

### RECALL_OFF

Median:
- overall: **51.2%**
- FIRST: **20.9%**
- LAST: **82.4%**

## Paired positional advantage

POSITION32 vs POSITION0:
- median gain: **+50.2 percentage points**
- founders gaining >=15 points: **14/14**

POSITION32 vs RECALL_OFF:
- median gain: **+47.3 percentage points**

All frozen confirmation gates passed.

## Founder audit

### Paired-invalid founders

Founder **84011**:
- paired-valid = no
- failure occurred only in RECALL_OFF
- RECALL_OFF stopped at training lesson 825 with the finite teaching free-phase warning
- POSITION32 completed normally
- POSITION32 overall/FIRST/LAST = **100% / 100% / 100%**
- position maps moved

Founder **84013**:
- paired-valid = no
- failure occurred only in RECALL_OFF
- RECALL_OFF stopped at training lesson 916 with the same finite teaching free-phase warning
- POSITION32 completed normally
- POSITION32 overall/FIRST/LAST = **100% / 100% / 100%**
- position maps moved

Thus both excluded founders independently support the POSITION32 effect diagnostically; they are excluded only because the frozen paired-valid rule requires all arms to complete.

### POSITION32 robustness outlier

Founder **84016** is the only paired-valid POSITION32 founder below the predeclared 80% floor on one cue:
- overall: **77.9%**
- FIRST: **59.2%**
- LAST: **96.7%**
- position maps moved: yes

Per-resource:
- WOOD: 88.6%
- STONE: 42.3%
- BERRY: 91.4%
- RABBIT: 98.2%

This leaves **13/14** paired-valid founders above the both-cue robustness threshold, exceeding the frozen >=12 requirement.

## Interpretation

The fresh replication confirms the bounded causal result:

> Cadence 0.89.0's learned Recall position term can retrieve Stone Age resource information by temporal endpoint, distinguishing FIRST from LAST when the present query and event content alone do not identify the requested slot.

The strongest causal control is POSITION32 vs POSITION0:
- same Recall mechanism
- same seeds
- same paired train/test episodes
- same working trace
- same recency=0
- same architecture and teaching
- only `recall_position` differs

The +50.2-point median advantage reproduces the V7.16 development effect.

The control asymmetry also replicates:
- non-positional arms are much stronger on LAST than FIRST
- POSITION32 removes that recency-like asymmetry and brings both cues to 100% median

## Scientific boundary

Confirmed:
- bounded five-event temporal endpoint retrieval
- four Stone Age resource meanings
- FIRST vs LAST
- learned position maps
- no reward learning
- no episodic memory
- no attention/multi-head option

Not yet established:
- full autonomous Stone Age survival with Recall
- temporal-memory-dependent goal routing in a continuing world
- long-horizon recall beyond this bounded stream
- arbitrary temporal reasoning

## Next direction

**Stone Age V7.17 — Autonomous Temporal-Memory Integration Bridge**

Keep the V7.15R confirmed autonomous semantic controller as the stable base and introduce a small number of deliberately memory-dependent states where:

- the current global semantic observation is identical
- the correct next semantic action depends on a recent event/order
- a current-state-only autonomous policy cannot solve the branch by construction

Recommended comparison:
- POSITION32 autonomous memory
- POSITION0 matched Recall control
- CURRENT_STATE control

Use Cadence 0.89.0.

Do not add episodic memory, multi-head attention, reward learning, or unrelated representation changes in the first integration experiment.
