# Frozen Protocol — Stone Age V7.12

Status: DEVELOPMENT / frozen before run.

Cadence:
- cadence-net==0.88.1

Scope:
- FIRE only

Fresh founders:
- 75001..75008
- minimum valid 6/8
- representation pass requires >=6/8 final-ready founders

Representations:
- CONTRAST18
- FIRE_MINIMAL
- FIRE_MINIMAL_PLUS_PROGRESS

Training:
- same structure as V7.11
- reset before every independent static bootstrap lesson
- DAgger64 learner-path teaching
- full 192-row reset-matched static replay
- no learning during execution-mode comparison

Execution modes:

DECISION_LEVEL
- query brain every normal decision window
- switching action resets action_progress
- max 14 decision windows

COMMIT_TO_COMPLETION
- query brain at a high-level boundary
- if GATHER_WOOD:
  - execute same action repeatedly until wood increases, death, or shared window budget exhausted
- if GATHER_STONE:
  - execute same action repeatedly until stone increases, death, or shared window budget exhausted
- all other actions:
  - execute one normal decision window
- then query brain again
- max total 14 decision windows, including internal committed windows

Fairness:
- same held-out seeds/variants between modes
- same 14-window environment budget
- no extra training
- no extra world time
- only re-decision frequency differs

Environment oracle:
- deterministic caretaker must solve 6/6 held-out FIRE episodes per founder

Evaluation:
- exact static
- fresh static
- 6 DECISION_LEVEL episodes
- 6 COMMIT_TO_COMPLETION episodes
- high-level queries
- total decision windows
- committed primitive lengths
- full action/resource/progress traces

Gates:
- exact >=90%
- fresh >=80%
- loop >=4/6

Representation commitment pass:
- median static gates pass
- median commit loop >=4/6
- >=6/8 founders individually pass static + commit loop

Material improvement:
- commit median loop gain >=2/6 vs decision-level for same representation

Classification:
1. FIRE_MINIMAL pass -> FIRE_TEMPORAL_COMMITMENT_RESCUE
2. only PLUS_PROGRESS pass -> FIRE_PROGRESS_PLUS_COMMITMENT_REQUIRED
3. only CONTRAST18 pass -> FIRE_CONTRAST_COMMITMENT_PASS
4. any representation gains >=2/6 but misses full pass -> PARTIAL_FIRE_COMMITMENT_SIGNAL
5. otherwise -> FIRE_TEMPORAL_COMMITMENT_UNRESOLVED

No post-hoc changes.
