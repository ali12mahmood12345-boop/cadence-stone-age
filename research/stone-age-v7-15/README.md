# Stone Age V7.15 — Autonomous Goal Routing Bridge

Status: **development protocol / frozen before run**

Cadence: **0.88.1**

V7.14R freshly confirmed that one plain Cadence brain can retain and execute FOOD, FIRE, HUNT and SHELTER together when an external task one-hot tells it which skill is active.

V7.15 removes that external task label.

## Question

Can one shared Cadence brain infer the appropriate goal from global semantic world/need state and directly choose the next Stone Age action?

## Fresh founders

`80001..80008`

- 8 founders total
- minimum valid: 6/8

## Arms

### AUTONOMOUS_GLOBAL

One 18-input / 11-action brain.

It receives no FOOD/FIRE/HUNT/SHELTER task bit.

It directly maps global semantic state to the next action.

### TASKED_SHARED_CONTROL

A second brain starts from the exact same untrained base brain.

It uses the exact confirmed V7.14 shared-brain recipe:
- explicit task one-hot
- same 16 semantic skill keys
- 64 presentations/key bootstrap
- DAgger64/skill
- full reset semantic replay
- semantic motor primitives
- stream reset before each high-level query

During the autonomous scenario exam, a frozen oracle supplies the active goal to this control. The control therefore tests whether the confirmed executor can solve the same world sequence when goal routing is supplied externally.

If TASKED_SHARED_CONTROL succeeds and AUTONOMOUS_GLOBAL fails, the new bottleneck is goal routing/global representation rather than four-skill execution.

## Global semantic representation

18-wide input.

Meaningful indices:

- 0 = hunger low (`hunger < 45`)
- 1 = warmth low (`warmth < 55`)
- 2 = energy low (`energy < 45`)
- 3 = evening or night
- 4 = food inventory available
- 5 = berry opportunity near
- 6 = rabbit opportunity near
- 7 = has spear
- 8 = fire exists
- 9 = shelter exists
- 10 = wood >= 2
- 11 = wood >= 4
- 12 = wood >= 10
- 13 = stone >= 2
- 14 = stone >= 4
- 15..17 = 0

No task identity is encoded.

## Frozen autonomous caretaker priority

The deterministic caretaker is frozen before the run.

Priority:

1. **Hunger**
   - food available -> `EAT`
   - else berry near -> `PICK_BERRIES`
   - else rabbit near:
     - spear -> `HUNT_RABBIT`
     - stone <2 -> `GATHER_STONE`
     - wood <2 -> `GATHER_WOOD`
     - otherwise -> `CRAFT_SPEAR`
   - else -> `EXPLORE`

2. **Cold/evening with no fire**
   - wood <4 -> `GATHER_WOOD`
   - stone <2 -> `GATHER_STONE`
   - otherwise -> `CRAFT_FIRE`

3. **Low energy**
   - shelter exists -> `SLEEP`
   - wood <10 -> `GATHER_WOOD`
   - stone <4 -> `GATHER_STONE`
   - otherwise -> `BUILD_SHELTER`

4. Otherwise -> `EXPLORE`

Thus the frozen priority is:

**hunger > fire/warmth > sleep > explore**

## Frozen static curriculum

AUTONOMOUS_GLOBAL uses **26 canonical global semantic keys**:

- 24 fixed semantic states taken from the frozen oracle trajectories for the eight autonomous scenario families
- 2 explicit `EXPLORE` controls:
  - neutral state
  - hungry with no available food source

Each key is presented 64 times during static bootstrap and 64 times during final reset replay.

Every independent static lesson calls `brain.reset()` before teaching.

The 26 vectors are hard-coded in the runner and do not depend on founder outcomes.

## Autonomous DAgger

Eight frozen scenario families are used.

AUTONOMOUS_GLOBAL receives:
- exactly 64 learner-path labels per scenario family
- 512 total dynamic labels
- deterministic round-robin scenario interleaving

At each semantic query:

1. `brain.reset()`
2. learner acts greedily from the global semantic vector
3. caretaker labels the same state
4. teach caretaker action
5. execute the learner's pre-lesson action as a semantic primitive
6. continue in the same world

## Autonomous scenario exam

Six held-out variants per scenario family.

### FORAGE
Hungry, berry opportunity available.

Success:
- food eaten

Budget:
- 12 decision windows

### HUNT_EAT
Hungry, no nearby berries, rabbit opportunity available, spear prerequisites available.

Success:
- rabbit hunted
- food eaten

Budget:
- 20 windows

### FIRE_COLD
Cold, no fire, one fire prerequisite missing.

Success:
- fire exists

Budget:
- 14 windows

### FIRE_EVENING
Warm but evening/night, no fire, fire prerequisites ready.

Success:
- fire exists

Budget:
- 14 windows

### SHELTER_SLEEP
Low energy, no shelter, shelter prerequisites ready.

Success:
- shelter exists
- energy >=88

Budget:
- 22 windows

### FOOD_THEN_FIRE
Hungry and cold.

Frozen priority must first resolve hunger, then FIRE.

Success:
- food eaten
- fire exists

Budget:
- 28 windows

### HUNT_THEN_SLEEP
Hungry with rabbit opportunity and no berries, plus low energy.

Frozen priority must complete:
- spear/hunt
- eat
- shelter/sleep

Success:
- rabbit hunted
- food eaten
- shelter exists
- energy >=88

Budget:
- 45 windows

### ALL_NEEDS
Hungry, cold and low-energy simultaneously.

The frozen priority should produce:
- forage/eat
- fire
- shelter/sleep

Success:
- food eaten
- fire exists
- shelter exists
- energy >=88

Budget:
- 56 windows

## Environment control

Resources used by each scenario are clustered to remove navigation distance as the experimental variable.

Unavailable food opportunities are moved far away rather than removed, so an incorrect action remains executable and consumes budget instead of crashing.

The deterministic autonomous caretaker must solve:
- 6/6 variants for all 8 scenario families
- 48/48 per founder

## Semantic motor primitives

Same confirmed controller boundary:

- `PICK_BERRIES` until food inventory increases
- `GATHER_WOOD` until wood increases
- `GATHER_STONE` until stone increases
- `HUNT_RABBIT` until rabbits_hunted increases or budget expires
- `SLEEP` until energy >=88 or budget expires
- all other actions execute one normal decision window

Before every high-level query:
- `brain.reset()`

## Checkpoints

Evaluate AUTONOMOUS_GLOBAL at:

1. `STATIC_ONLY`
2. `POST_DAGGER64`
3. `POST_REPLAY_FULL`

Metrics:
- overall 26-key static accuracy
- static accuracy by routed goal: FOOD / HUNT / FIRE / SHELTER / NEUTRAL
- 6 held-out loops per scenario
- action agreement with frozen caretaker
- founder all-scenario readiness

TASKED_SHARED_CONTROL is evaluated after its final replay on:
- standard four-skill V7.14 static/loop gates
- the same eight autonomous scenarios with oracle goal routing

## Frozen gates

AUTONOMOUS static:
- overall >=90%
- each FOOD/HUNT/FIRE/SHELTER routed group >=90%
- NEUTRAL reported diagnostically

Per autonomous scenario:
- loop >=4/6

Founder autonomous-ready:
- overall static gate passes
- all four routed-goal static gates pass
- all eight scenario loop gates pass

Run validity:
- >=6/8 valid founders

TASKED_SHARED_CONTROL stability:
- >=6/8 founders pass the standard V7.14 all-four gate
- all eight autonomous scenario median loop gates pass under oracle routing
- >=6/8 founders pass all eight oracle-routed scenarios

AUTONOMOUS bridge pass:
- TASKED_SHARED_CONTROL stable
- all autonomous median static gates pass
- all eight autonomous median scenario gates pass
- >=6/8 AUTONOMOUS_GLOBAL founders autonomous-ready

## Frozen classification

1. valid founders <6 -> `INSUFFICIENT_V7_15_RUNS`
2. tasked control unstable -> `TASKED_EXECUTOR_CONTROL_NOT_STABLE`
3. autonomous bridge passes -> `AUTONOMOUS_GOAL_ROUTING_BRIDGE_PASS`
4. autonomous routed static gates fail -> `AUTONOMOUS_ROUTING_ACQUISITION_BOTTLENECK`
5. autonomous static passes but dynamic/scenario bridge fails -> `AUTONOMOUS_DYNAMIC_ROUTING_BOTTLENECK`
6. otherwise -> `PARTIAL_AUTONOMOUS_ROUTING_SIGNAL`

No attention.
No episodic-memory arm.
No reward-learning arm.
No post-hoc priority or gate changes.
