# Frozen Protocol — Stone Age V7

Status: DEVELOPMENT.

Runtime:
- cadence-net==0.88.0
- numpy>=2,<3

Fresh founders:
- 60001..60006
- minimum valid: 4/6

Source:
- repo: ali12mahmood12345-boop/cadence-stone-age
- file: stone_age_game/main.py
- blob: dd59769349e7b6e9dea4ddcc321af8fa86b4e660

## Environment

Headless matched-run port preserving:
- 18 inputs
- 11 original actions
- modules=(32,16)
- 150-second day
- 0.55-second decision interval
- 33 physics/body frames at 1/60 second per decision
- original crafting prerequisites
- original survival dynamics
- original reward constants
- original rabbit mechanics

## Panels

VISIBLE:
- unchanged 18-input observation

HIDDEN_INVENTORY:
- mask observation indices 5,6,7,8 to zero
- wood
- stone
- carried food
- spear possession
- true body/world state unchanged

## Arms

DEFAULT:
- founder recipe

EPISODIC:
- DEFAULT + memory_choice=True

H1:
- learned_code=16
- attention=True
- recall_heads=1
- recall_address_reward=0.1

H2:
- learned_code=16
- attention=True
- recall_heads=2
- recall_address_reward=0.1

H2_EPISODIC:
- H2 + memory_choice=True

The default associative store remains present in every arm.

## Lifecycle

Per founder / arm / panel:
- 6 sampled training episodes using Brain.step
- persistent brain across episodes
- 3 evaluation episodes using greedy Brain.act
- learned_code frozen before evaluation where present
- no reward feedback during evaluation
- reset between episodes
- max 2.0 days per episode

World seeds are founder/panel/episode-specific and identical across arms.

## Frozen signal gates

`STONE_AGE_0_88_MEMORY_ATTENTION_INTEGRATION_SIGNAL` requires:

- >=4 valid founders

Hidden inventory:
- H2_EPISODIC > DEFAULT in >=2/3 valid founders
- median H2E−DEFAULT >= +0.20 days
- H2_EPISODIC > EPISODIC in >=2/3 valid founders
- median H2E−EPISODIC >= +0.10 days
- H2_EPISODIC > H2 in >=2/3 valid founders
- median H2E−H2 >= +0.10 days
- median H2_EPISODIC night-survival rate >=50%

Visible control:
- median H2E−DEFAULT >= -0.20 days

Secondary descriptive metrics:
- horizon survival
- environmental reward
- fire/spear/shelter construction
- food consumption
- visible→hidden penalty

## Boundaries

- development only
- this is Ali's Stone Age environment mechanics, not Bernhard's Stone Age sequence instrument
- HIDDEN_INVENTORY is experiment-specific
- recall_address_reward=0.1 is explicit opt-in, not the 0.88 founder
- positive results require fresh confirmation
