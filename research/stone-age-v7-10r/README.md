# Stone Age V7.10R — Replay Boundary Correction

Status: **development complete**

Cadence: **0.88.1**

Official classification:

`RESET_BOUNDARY_RECOVERY_RESCUE`

## Question

Does `brain.reset()` before each replay lesson restore the cold static policy that V7.10's continuing replay failed to recover?

## Frozen design

Fresh founders: `73001..73008`.

Common history per founder/skill:

1. static bootstrap
2. DAgger64
3. evaluate `POST_DAGGER64`
4. deep-copy the exact post-DAGGER brain into two matched replay branches

Branches:

- `CONTINUING_REPLAY`: no reset before replay rows
- `RESET_REPLAY`: `brain.reset()` before every replay row

Everything else was matched:
- branch-point brain
- replay rows
- replay order
- labels
- replay doses
- evaluation

## Result

All **8/8 founders were valid**.

### REPLAY_FULL medians — EXACT / FRESH / CLOSED-LOOP

| Skill | CONTINUING_REPLAY | RESET_REPLAY |
| --- | --- | --- |
| FOOD | 95.7 / 93.8 / 100% | **100 / 100 / 100%** |
| FIRE | 33.3 / 33.3 / 0% | **100 / 100 / 0%** |
| HUNT | 66.7 / 66.7 / 100% | **100 / 100 / 100%** |
| SHELTER | 66.7 / 66.7 / 83.3% | **100 / 100 / 100%** |

Mean median retention:

- CONTINUING_REPLAY REPLAY_FULL: **0.651**
- RESET_REPLAY REPLAY_FULL: **1.000**

Mean median loop:

- CONTINUING_REPLAY REPLAY_FULL: **0.708**
- RESET_REPLAY REPLAY_FULL: **0.750**

Static all-skill median readiness:

- CONTINUING_REPLAY: never recovered
- RESET_REPLAY: recovered by **REPLAY64** and remained recovered at **REPLAY_FULL**

Founder-level reset static recovery at REPLAY_FULL:
- **7/8 founders** passed exact/fresh gates on all four skills

Full static+loop all-four readiness:
- 0/8 in both branches

## Interpretation

V7.10's broad irrecoverability interpretation was a teaching-boundary artifact.

Calling `brain.reset()` before every replay lesson restores the original cold static mappings dramatically. At REPLAY_FULL the RESET_REPLAY branch returns to 100/100 median exact/fresh on all four skills, while the continuing branch remains degraded.

Therefore:

> The static Stone Age policy is recoverable after DAgger64 when replay uses the same reset boundary as the original successful static curriculum.

The V7.10 result remains valid only for continuing no-reset replay.

### What remains unresolved

RESET_REPLAY does **not** produce a full bridge because FIRE closed-loop remains at 0% median despite 100/100 static recovery.

FOOD, HUNT and SHELTER reach 100/100 static and 100% median loop under RESET_REPLAY. FIRE is now the dominant remaining boundary.

Founder-level FIRE RESET_REPLAY REPLAY_FULL closed-loop success:
- 73001: 0/6
- 73002: 3/6
- 73003: 3/6
- 73004: 3/6
- 73005: 0/6
- 73006: 0/6
- 73007: 0/6
- 73008: 0/6

No FIRE founder reaches the frozen 4/6 loop gate.

## FIRE mechanism clue

The FIRE static policy is correct on the three cold prototypes:

- missing wood -> `GATHER_WOOD`
- missing stone -> `GATHER_STONE`
- resources ready -> `CRAFT_FIRE`

But gathering wood/stone takes multiple consecutive environment decisions before the inventory threshold changes. During those intermediate decisions, raw nuisance state such as position, time, energy and distances changes while the resource threshold remains unchanged.

The RESET_REPLAY branch restores the cold prototype mapping, but the FIRE action traces still switch too early or repeat the wrong stage on these intermediate trajectory states.

This suggests the remaining FIRE failure is not static memory retention. It is a **dynamic-state invariance / trajectory representation problem**.

## Next direction

**Stone Age V7.11 — FIRE Dynamic Invariance Microscope**

Do not reopen all four skills yet.

Use FIRE only and compare representations under the now-correct reset teaching boundary:

1. `CONTRAST18`
   - current representation
   - preserves raw nuisance dimensions

2. `FIRE_MINIMAL`
   - retain only task-sufficient FIRE state:
     - wood>=4
     - stone>=2
     - fire_exists
   - zero nuisance dimensions

3. `FIRE_MINIMAL_PLUS_PROGRESS`
   - same task state plus explicit current-action/progress information
   - diagnostic for whether partial gathering itself is hidden state

All arms:
- full 11 actions
- surprise from lesson 0
- matched static bootstrap
- matched DAgger exposure where applicable
- reset before independent static replay rows
- exact/fresh/closed-loop evaluation

Primary question:

Can a nuisance-invariant FIRE representation preserve the correct action across the multiple decisions needed to finish gathering?

Interpretation:
- MINIMAL rescues loop -> nuisance drift was the bottleneck
- only MINIMAL_PLUS_PROGRESS rescues -> hidden action-progress state is required
- neither rescues -> deeper policy/settlement instability remains
