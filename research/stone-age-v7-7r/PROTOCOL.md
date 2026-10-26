# Frozen Protocol — Stone Age V7.7R

Status: DEVELOPMENT INTEGRATION.

Cadence:
- cadence-net==0.88.1

Fresh founders:
- 69001..69008
- minimum valid 6/8
- primary all-four readiness requires 6/8

Skills:
- FOOD
- FIRE
- HUNT
- SHELTER

Training:
- same balanced prototype generator used by V7.4–V7.6R
- 64 training rows/prototype
- 24 fresh static rows/prototype
- teaching="normalized"
- learning_surprise=True from lesson 0
- qualified
- modules=(32,16)
- one-row Brain.lesson
- one pass

Arms:
- RAW18_SURPRISE_FULL11: raw 18 inputs, actions=11
- CONTRAST18_SURPRISE_FULL11: V7.6R threshold encoding, actions=11
- CONTRAST18_SURPRISE_LOCAL: same contrast, skill-local actions only

Matching:
- RAW and CONTRAST full11 use the same graph seed per founder/skill.
- local has a separate seed offset because output dimensionality differs.

Evaluation:
- cold exact multiclass accuracy
- cold fresh multiclass accuracy
- real StoneAgeEnv closed-loop execution
- greedy act, no teacher/reward during evaluation
- 3 variants per skill
- separate brain copy per variant

Gates:
- exact >=90%
- fresh >=80%
- loop >=2/3

Classification:
1. insufficient
2. full11 contrast median gates + >=6/8 all-four founders -> SURPRISE_CONTRAST_FULL11_INTEGRATION_PASS
3. local contrast median gates + >=6/8 all-four founders -> SURPRISE_CONTRAST_LOCAL_ONLY_INTEGRATION_PASS
4. full11 contrast static all-skill pass -> SURPRISE_CONTRAST_STATIC_RESCUE_CLOSED_LOOP_BOTTLENECK
5. local contrast static all-skill pass -> SURPRISE_CONTRAST_LOCAL_STATIC_RESCUE_ONLY
6. otherwise -> NO_SURPRISE_CONTRAST_MULTICLASS_INTEGRATION_RESCUE

No post-hoc changes.
