# V7.36 FIXED — Position Convergence / Dose Scaling

Run on Windows:

`START_STONE_AGE_V7_36.bat`

Cadence: `0.91.1`

## Why this fixed rerun exists

The first V7.36 run produced the expected convergence curve but only 2/8 founders completed all three checkpoints. Six founders eventually triggered Cadence's finite teaching free-phase budget warning.

The scientific protocol is unchanged. The fixed rerun raises only:

`learning_free_steps: 1024 -> 4096`

Warnings remain errors, so unsettled lessons are not silently accepted.

## First-run signal

Among the founders that completed the full curve:
- D198 BASE: 83.1%
- D396 BASE: 91.5%
- D792 BASE: 97.6%
- D792 natural top-predecessor: 100%
- D792 learned-map top-predecessor: 100%

The first run remains formally inconclusive because the minimum valid-founder gate was not met.

## Output files

- `STONE_AGE_V7_36_REPORT.txt`
- `STONE_AGE_V7_36_RESULTS.json`
- `STONE_AGE_V7_36_SUMMARY.csv`
- `STONE_AGE_V7_36_PER_FOUNDER.csv`
- `STONE_AGE_V7_36_ATTENTION.csv`
- `STONE_AGE_V7_36_MAP_GEOMETRY.csv`

See `PROTOCOL.md` for the frozen protocol.
