# Cadence Stone Age Research Environment

A Stone Age survival environment and a sequence of controlled Cadence benchmarks used to study prerequisite chains, interference, action history, episodic memory, temporal context, learned Recall routing, and variable-length temporal addressing.

The project started as a visual survival game and was progressively reduced into controlled chambers so individual learning mechanisms could be measured.

## Current research line: Cadence 0.91.1 learned Recall

The current Stone Age line is the V7.28-V7.36 temporal-addressing series.

Latest consolidated summary:

[`docs/V7_28_TO_V7_36_RESULTS.md`](docs/V7_28_TO_V7_36_RESULTS.md)

Current experiment:

[`research/stone-age-v7-36/`](research/stone-age-v7-36/)

### Current picture

The recent series establishes that:

- native `recall_boundary=True` can replace the earlier manual zero-START workaround for the Stone Age Recall experiments;
- training can causally steer Recall toward predecessor->next or value-route strategies;
- on the variable-length 3..7 task, one fixed analytic `P + length` position map solves all 22 valid temporal addresses perfectly;
- the remaining learned-map gap is therefore an acquisition/sample-efficiency issue rather than an inability of the representation to express the rule;
- removing the current-attention prior, giving an exact predecessor teacher, freezing position `P_c`, disabling the content-address map, and lowering the position rate did not individually explain the old ~70-80% ceiling;
- the first V7.36 convergence run showed a strong dose curve: D198 83.1% -> D396 91.5% -> D792 97.6%, with the learned map reaching 100% top-predecessor selection at D792, but only 2/8 founders completed because six hit the finite free-phase settling budget;
- V7.36 FIXED keeps the science unchanged and raises only `learning_free_steps` from 1024 to 4096 so the full 8-founder convergence confirmation can run.

The current working hypothesis is that much of the apparent variable-length "ceiling" was finite-dose convergence of the released online position-map learner.

## Earlier confirmed Stone Age milestones

The repository retains the earlier V7 series under `research/`, including:

- V7.13R — `FIRE_STREAM_STATE_RESET_CONFIRMED`
- V7.14R — `FOUR_SKILL_SHARED_SEMANTIC_BRIDGE_CONFIRMED`
- V7.15R — `AUTONOMOUS_GOAL_ROUTING_CONFIRMED`
- V7.16R — `POSITIONAL_RECALL_TEMPORAL_HISTORY_CONFIRMED`

See the live research summary:

[`research/STATUS.md`](research/STATUS.md)

## Cadence 0.83 episodic / temporal-context series

The earlier controlled episodic and temporal-context results remain here:

[`docs/V7_RESULTS.md`](docs/V7_RESULTS.md)

Protocol details:

[`docs/V7_REPRODUCIBILITY.md`](docs/V7_REPRODUCIBILITY.md)

That series showed that fixed fading temporal context causally helped ambiguous sequence behavior on the separated A-B-A-B task, while robust lock-in was founder-sensitive and the exact greedy advantage did not generalize cleanly to A-A-B-B.

## Cadence 0.84 Agency Door benchmark

The controllable-vs-yoked intervention benchmark is published here:

[`benchmarks/agency_door_084/`](benchmarks/agency_door_084/)

It studies contingency-sensitive action learning, reversal adaptation, and A -> B -> A reacquisition.

## Earlier 0.81 work

The original controlled 0.81 experiments remain in:

[`benchmarks/cadence_081/`](benchmarks/cadence_081/)

Historical results:

[`docs/RESULTS.md`](docs/RESULTS.md)

## Main survival environment

The original visual environment is in:

`stone_age_game/main.py`

It contains trees, rocks, berries, rabbits, hunger, warmth, energy, fire, spear crafting, shelter, sleep, and a day/night cycle.

## Research stance

Null, negative, partial, and invalid runs are intentionally retained. The repository is meant to show what was tested, what worked, what failed, what was repaired, and where the current mechanism reaches its boundary.

Component-task results are not treated as claims about full-game intelligence or general episodic reasoning.
