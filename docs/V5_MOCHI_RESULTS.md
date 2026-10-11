# V5 Mochi-Inspired Selective Caregiver — 5-Seed Result

Cadence version: `cadence-net 0.81.0`

This is a **preliminary reproducibility result** from five fresh founder seeds
(42–46). The V5 protocol keeps one continuing Cadence brain per training arm,
alternates guided and autonomous windows, and compares:

- `natural_only`
- `grade_only`
- `corrective_teacher`
- untrained `founder`
- uniform `random`

The Stone Age COLD chain is:

`GATHER_WOOD -> GATHER_STONE -> CRAFT_FIRE -> WARM_UP`

## Protocol

- 120 training episodes
- 4 guided decisions / 8 autonomous decisions
- 100 frozen evaluation episodes
- 80 autonomous-life episodes after the caregiver leaves
- 300 samples per canonical state fingerprint
- 5 fresh seeds: 42, 43, 44, 45, 46

The five-seed run changes only the number of seeds relative to the successful
single-seed Quick run.

## Aggregate full-chain success

| Arm | Immediate sampled | Immediate greedy | After caregiver leaves |
|---|---:|---:|---:|
| natural_only | 1.0% | 0.0% | 4.4% |
| grade_only | 0.2% | 0.0% | 1.0% |
| corrective_teacher | **18.8%** | 0.0% | **22.8%** |
| founder | 7.6% | 0.0% | — |
| random | 12.4% | — | — |

The selective `corrective_teacher` arm is the only trained arm that beat both
the founder and random baselines on immediate sampled full-chain success.

After the caregiver left, the same acquired brains continued living for another
80 episodes with only environmental outcomes. Aggregate sampled success rose
from 18.8% to 22.8%.

## Corrective-teacher result by seed

| Seed | Immediate | After caregiver leaves |
|---:|---:|---:|
| 42 | 28% | 23% |
| 43 | 24% | 18% |
| 44 | 20% | 21% |
| 45 | 11% | 30% |
| 46 | 11% | 22% |

## Training signal

| Arm | Mean agreement | Mean teacher corrections |
|---|---:|---:|
| natural_only | 10.7% | 0.0 |
| grade_only | 16.3% | 0.0 |
| corrective_teacher | 21.9% | 277.4 |

## Important observation

For seed 42, the isolated reset-based canonical fingerprint for
`corrective_teacher` was:

- empty -> `GATHER_WOOD`: 72.7%
- has_wood -> `GATHER_STONE`: 10.0%
- has_materials -> `CRAFT_FIRE`: 11.0%
- has_fire -> `WARM_UP`: 16.3%

Yet the same brain reached 28% full-chain sampled success.

This does **not prove** that Cadence is using sequence memory, but it does show
that isolated reset-based state probes do not fully explain the behavior seen
during a continuing sequence. A dedicated sequence-state probe is the next
experiment.

## Warning observed during training

Cadence emitted a runtime warning stating that a finite teaching free phase used
its entire `free_steps` budget and that the lesson may have been learned from a
state that did not settle.

That warning is preserved as an experimental caveat rather than ignored.

## Interpretation

The result supports a narrower claim:

> Under this five-seed Stone Age COLD-chain test, selective corrective teaching
> produced higher sampled full-chain success than the untrained founder and
> uniform-random baselines, while reward grading alone did not.

The result should still be reproduced under additional seeds and future Cadence
versions before making stronger claims.
