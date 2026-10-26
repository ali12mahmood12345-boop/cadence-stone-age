# Frozen Protocol — Stone Age V7.10R

Status: DEVELOPMENT / frozen before run.

Cadence:
- cadence-net==0.88.1

Fresh founders:
- 73001..73008
- minimum valid 6/8
- primary full bridge >=6/8 all-four founders at same RESET_REPLAY checkpoint

Base:
- CONTRAST18
- full 11 actions
- modules=(32,16)
- teaching="normalized"
- learning_surprise=True from lesson 0
- qualified teaching

Common history:
- static bootstrap exactly as V7.10
- DAgger64 exactly as V7.10
- branch from one identical POST_DAGGER64 state

Branches:

CONTINUING_REPLAY
- no reset before replay lessons
- reproduces V7.10 replay boundary

RESET_REPLAY
- brain.reset() immediately before every replay lesson
- same rows/order/labels/doses as CONTINUING_REPLAY

Replay stream:
- deterministic balanced full replay from original static training rows
- identical ordered row list supplied to both branches
- cumulative checkpoints:
  - REPLAY32 = 32 calls
  - REPLAY64 = 64 calls
  - REPLAY_FULL = full original pass
- FOOD full = 128
- FIRE full = 192
- HUNT full = 192
- SHELTER full = 192

Evaluation:
- STATIC_ONLY before DAgger
- POST_DAGGER64 before branching
- branch REPLAY32
- branch REPLAY64
- branch REPLAY_FULL
- exact
- fresh
- six held-out loops
- output dominance
- replay accepted/agreed
- all evaluation on deep copies

Gates:
- exact >=90%
- fresh >=80%
- loop >=4/6

Classification precedence:
1. insufficient -> INSUFFICIENT_V7_10R_RUNS
2. RESET_REPLAY full static+loop criterion and >=6/8 all-four -> RESET_REPLAY_FULL_BRIDGE_PASS
3. RESET_REPLAY static all-skill recovers while CONTINUING_REPLAY static does not -> RESET_BOUNDARY_RECOVERY_RESCUE
4. RESET_REPLAY static all-skill recovers but loop all-skill fails -> STATIC_RECOVERABLE_DYNAMIC_POLICY_COMPETES_AFTER_RESET
5. both branches fail static all-skill recovery after REPLAY_FULL -> STATIC_IRRECOVERABILITY_SURVIVES_RESET_CONTROL
6. otherwise -> PARTIAL_RESET_BOUNDARY_SIGNAL

No post-hoc changes.
