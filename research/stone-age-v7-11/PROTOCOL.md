# Frozen Protocol — Stone Age V7.11

Status: DEVELOPMENT / frozen before run.

Cadence:
- cadence-net==0.88.1

Scope:
- FIRE only

Fresh founders:
- 74001..74008
- minimum valid 6/8
- representation pass requires >=6/8 final-ready founders

Common architecture:
- inputs=18
- actions=11
- modules=(32,16)
- teaching="normalized"
- learning_surprise=True from lesson 0
- qualified teaching

Static data:
- FIRE_CRAFT, FIRE_WOOD, FIRE_STONE
- 64 rows/prototype train
- 24 rows/prototype fresh

Training sequence:
1. static bootstrap
   - brain.reset() before every independent row
2. STATIC_ONLY evaluation
3. DAgger64
   - learner acts first
   - caretaker labels same state
   - teach caretaker label
   - execute learner pre-lesson action
4. POST_DAGGER64 evaluation
5. full static replay
   - complete 192-row balanced original FIRE static curriculum
   - brain.reset() before every replay lesson
6. POST_RESET_REPLAY_FULL evaluation

Representation arms:

CONTRAST18
- raw 18 inputs retained
- input 5 = wood>=4
- input 6 = stone>=2

FIRE_MINIMAL
- all 18 inputs zero except:
  - input 5 = wood>=4
  - input 6 = stone>=2
  - input 9 = fire_exists

FIRE_MINIMAL_PLUS_PROGRESS
- all 18 inputs zero except:
  - input 0 = clip(action_progress/1.25,0,1)
  - input 1 = current_action==GATHER_WOOD
  - input 2 = current_action==GATHER_STONE
  - input 3 = current_action==CRAFT_FIRE
  - input 5 = wood>=4
  - input 6 = stone>=2
  - input 9 = fire_exists
- independent static rows: action flags=0, progress=0
- dynamic rows: real env current_action/action_progress

Caretaker:
- wood < 4 -> GATHER_WOOD
- else stone < 2 -> GATHER_STONE
- else -> CRAFT_FIRE

Held-out FIRE setup:
- 6 variants
- same frozen V7.10R FIRE setup
- variants alternate missing wood / missing stone

Environment oracle:
- execute caretaker directly on each held-out episode
- validity requires 6/6 successes for every founder

Evaluation:
- exact
- fresh
- loop success over 6 episodes
- output dominance
- per-prototype static accuracy
- action/resource/progress traces on loop failures

Final gates:
- exact >=90%
- fresh >=80%
- loop >=4/6

Representation pass:
- median final exact/fresh/loop gates all pass
- >=6/8 founders final-ready

Classification:
1. FIRE_MINIMAL pass -> FIRE_NUISANCE_INVARIANCE_RESCUE
2. only FIRE_MINIMAL_PLUS_PROGRESS pass -> FIRE_PROGRESS_STATE_REQUIRED
3. CONTRAST18 pass -> FIRE_CONTRAST_BASELINE_PASS
4. either minimal arm gains >=2/6 (+33.3 percentage points) median final loop vs CONTRAST18 but no full pass -> PARTIAL_FIRE_INVARIANCE_SIGNAL
5. otherwise -> FIRE_DYNAMIC_INVARIANCE_UNRESOLVED

No post-hoc changes.