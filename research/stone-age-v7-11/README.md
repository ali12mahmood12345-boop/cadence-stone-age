# Stone Age V7.11 — FIRE Dynamic Invariance Microscope

Status: **running protocol / frozen before run**

Cadence: **0.88.1**

V7.10R resolved the replay-boundary confound. Reset-matched replay restores the static policy to 100/100 median exact/fresh on all four skills, while FOOD/HUNT/SHELTER also retain 100% median loop success. FIRE remains the only dominant failure: 100/100 static but 0% median closed-loop.

## Question

Is FIRE's remaining failure caused by changing nuisance state during the multiple decisions required to finish gathering, or does the policy require explicit current-action/progress state?

## Scope

FIRE only.

Fresh founders: `74001..74008`.

All brain arms use:
- cadence-net==0.88.1
- full 11 actions
- modules `(32,16)`
- normalized qualified teaching
- `learning_surprise=True` from lesson 0
- 64 static rows per FIRE prototype
- 24 fresh rows per FIRE prototype
- exactly 64 learner-path DAgger labels
- one full reset-matched static replay pass after DAgger
- `brain.reset()` before every independent static bootstrap/replay lesson
- 6 held-out FIRE loop episodes

## Representation arms

### CONTRAST18
Current V7.10R representation.

All 18 raw Stone Age inputs remain visible, except:
- input 5 = `wood >= 4`
- input 6 = `stone >= 2`

This arm retains changing nuisance state such as body needs, world time and distances.

### FIRE_MINIMAL
18-wide matched input vector, but all nuisance dimensions are zeroed.

Only:
- input 5 = `wood >= 4`
- input 6 = `stone >= 2`
- input 9 = `fire_exists`

remain visible.

This representation is invariant across movement and partial gathering while the task-relevant prerequisite state is unchanged.

### FIRE_MINIMAL_PLUS_PROGRESS
Same minimal task state, plus explicit action-continuation state:

- input 0 = clipped `action_progress / 1.25`
- input 1 = currently `GATHER_WOOD`
- input 2 = currently `GATHER_STONE`
- input 3 = currently `CRAFT_FIRE`
- input 5 = `wood >= 4`
- input 6 = `stone >= 2`
- input 9 = `fire_exists`

Static independent samples use no-current-action and progress 0. Dynamic DAgger/loop states use the environment's real current action and progress.

## Common training sequence

For each representation/founder:

1. static bootstrap, reset before every lesson
2. evaluate `STATIC_ONLY`
3. DAgger64 on learner-path FIRE states
4. evaluate `POST_DAGGER64`
5. one full balanced static replay pass, reset before every replay lesson
6. evaluate `POST_RESET_REPLAY_FULL`

## Environment sanity control

The deterministic caretaker is also executed directly on the same six held-out FIRE episodes.

Required validity:
- caretaker oracle must solve 6/6 held-out episodes for every founder

This confirms that the environment/episode cap itself permits the frozen FIRE policy.

## Evaluation

At all three checkpoints:
- exact static accuracy
- fresh static accuracy
- 6 held-out FIRE loop episodes
- output dominance

Training diagnostics:
- DAgger accepted/agreed
- brain/caretaker agreement
- reset replay accepted/agreed
- failed loop action traces
- real `wood`, `stone`, `current_action` and `action_progress` in each trace

## Frozen gates

Per founder/representation at final checkpoint:
- exact >=90%
- fresh >=80%
- closed-loop >=4/6

Representation-level readiness:
- median exact >=90%
- median fresh >=80%
- median loop >=4/6
- >=6/8 valid founders individually pass all three final gates

## Frozen interpretation

Classification precedence:

1. `FIRE_MINIMAL` passes final criterion -> `FIRE_NUISANCE_INVARIANCE_RESCUE`
2. only `FIRE_MINIMAL_PLUS_PROGRESS` passes -> `FIRE_PROGRESS_STATE_REQUIRED`
3. `CONTRAST18` unexpectedly passes -> `FIRE_CONTRAST_BASELINE_PASS`
4. minimal arms materially improve loop but miss frozen founder gate -> `PARTIAL_FIRE_INVARIANCE_SIGNAL`
5. otherwise -> `FIRE_DYNAMIC_INVARIANCE_UNRESOLVED`

No other Stone Age skill, shared brain, memory/attention, hidden inventory or reward-learning comparison is opened in V7.11.
