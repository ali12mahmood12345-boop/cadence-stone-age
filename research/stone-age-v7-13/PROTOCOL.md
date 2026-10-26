# Frozen Protocol — Stone Age V7.13

Status: DEVELOPMENT / frozen before run.

Cadence:
- cadence-net==0.88.1

Scope:
- FIRE only

Fresh founders:
- 76001..76008
- minimum valid 6/8
- full reset-query pass requires >=6/8 ready founders

Representation:
- FIRE_MINIMAL only
- 18-wide input
- input5 = wood>=4
- input6 = stone>=2
- input9 = fire_exists
- all others zero

Training:
- same structure as V7.12
- reset before every independent static bootstrap row
- DAgger64 learner-path teaching
- full 192-row reset-matched static replay
- freeze final brain
- no learning during execution comparison

Modes:

COMMIT_CONTINUING
- same V7.12 commitment rule
- preserve brain stream state between high-level queries

COMMIT_RESET_QUERY
- same commitment rule
- call brain.reset() immediately before every high-level query
- do not reset environment
- learned weights/records remain unchanged

Commitment:
- GATHER_WOOD held until wood increases
- GATHER_STONE held until stone increases
- other actions execute one normal decision window

Fairness:
- same frozen final brain
- same held-out seeds/variants
- same 14 total decision-window budget
- same commitment rule
- no extra learning
- no extra world time
- only difference is reset before high-level query

Environment oracle:
- deterministic caretaker must solve 6/6 per founder

Evaluation:
- exact static
- fresh static
- 6 COMMIT_CONTINUING episodes
- 6 COMMIT_RESET_QUERY episodes
- high-level query count
- decision-window count
- primitive lengths
- full state/action trace
- first ready-to-craft boundary and whether CRAFT_FIRE chosen

Gates:
- exact >=90%
- fresh >=80%
- loop >=4/6

Reset-query pass:
- median exact/fresh/loop gates pass
- >=6/8 founders individually pass

Material reset effect:
- median reset-query loop gain >=2/6 vs commit-continuing

Classification:
1. reset-query full pass -> FIRE_STREAM_STATE_RESET_RESCUE
2. continuing commit full pass -> FIRE_CONTINUING_COMMIT_PASS
3. reset-query median gain >=2/6 without full pass -> PARTIAL_FIRE_STREAM_RESET_SIGNAL
4. otherwise -> FIRE_STREAM_STATE_RESET_UNRESOLVED

No post-hoc changes.
