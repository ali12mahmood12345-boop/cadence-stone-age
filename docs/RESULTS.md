# Results Summary

These are the notable quick-run results observed while iterating on the Cadence 0.81 COLD prerequisite chain.

## V4.1 — balanced backward lessons

Frozen full-chain evaluation:

- founder sampled: 2%
- lessons only sampled: 4%
- critic 0.3 sampled: 4%
- critic 5.0 sampled: 4%
- Random sampled: 8%

Lesson accuracy:

- WARM_UP: 72.5%
- CRAFT_FIRE: 67.5%
- GATHER_STONE: 57.5%
- GATHER_WOOD: 35.0%

Canonical sampled right-action rates:

- empty -> GATHER_WOOD: 6.5%
- has wood -> GATHER_STONE: 49.0%
- has materials -> CRAFT_FIRE: 68.0%
- has fire -> WARM_UP: 57.0%

The critic-rate comparison did not materially change the acquired policy in this run.

## V4.2 — balanced lesson budget sweep

Observed one-step accuracy by fixed budget:

### GATHER_WOOD

- 20 trips: 20%
- 40 trips: 70%
- 80 trips: 25%
- 160 trips: 30%

### GATHER_STONE

- 20 trips: 0%
- 40 trips: 0%
- 80 trips: 50%
- 160 trips: 82.5%

### CRAFT_FIRE

- 20 trips: 20%
- 40 trips: 40%
- 80 trips: 55%
- 160 trips: 72.5%

### WARM_UP

- 20 trips: 40%
- 40 trips: 40%
- 80 trips: 50%
- 160 trips: 80%

This suggested a training-budget tradeoff: later prerequisite mappings improved with more drilling while GATHER_WOOD peaked early and then degraded.

## V4.3 — competency-based lessons

Frozen full-chain evaluation on seed 42:

- trained sampled: 11%
- founder sampled: 5%
- Random sampled: 2%
- trained greedy: 0%

Canonical sampled right-action rates:

- empty -> GATHER_WOOD: 71.3%
- has wood -> GATHER_STONE: 43.0%
- has materials -> CRAFT_FIRE: 14.3%
- has fire -> WARM_UP: 13.7%

Final one-step competencies:

- WARM_UP: 8.1% — direct 4, rescue 8
- CRAFT_FIRE: 14.4% — direct 12, rescue 6
- GATHER_STONE: 45.6% — direct 20, rescue 0
- GATHER_WOOD: 71.9% — direct 4, rescue 0

This was the first positive frozen full-chain result versus both Founder and Random, but earlier backward-taught skills were damaged by later acquisition.

## V4.4 — retention rescue

Frozen full-chain evaluation on seed 42:

- trained sampled: 3%
- founder sampled: 5%
- Random sampled: 2%
- trained greedy: 0%

Canonical sampled right-action rates:

- empty -> GATHER_WOOD: 7.3%
- has wood -> GATHER_STONE: 8.7%
- has materials -> CRAFT_FIRE: 70.7%
- has fire -> WARM_UP: 72.7%

Final one-step competencies / training cost:

- WARM_UP: 73.1% — direct 4, rescue 6
- CRAFT_FIRE: 70.0% — direct 12, rescue 12
- GATHER_STONE: 7.5% — direct 60, rescue 438
- GATHER_WOOD: 6.9% — direct 60, rescue 50

Final consolidation:

- rescue budget used: 80
- stable: False

Repeatedly rescuing the weakest mapping did not stabilize all four state-action mappings. GATHER_STONE alone received 438 rescue trips and still ended at 7.5%.

## Current interpretation

The experiment currently points to persistent interference between prerequisite state-action mappings.

Cadence can acquire individual mappings, and competency-based stopping briefly produced full-chain performance above both Founder and Random on one seed. However, learning or rescuing one part of the chain can strongly degrade other prerequisite mappings.

These results are preliminary and should be reproduced across multiple seeds before making stronger claims.
