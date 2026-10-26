# Cadence Research Status

Updated: 2026-10-26

## Confirmed

### Representation Keys V0.3D
Fresh confirmation on Cadence 0.85.1.

### Memory Keys V0.4B
Fresh confirmation on Cadence 0.85.1.

## Development boundary results

### Attention V0.5A
Original held split was underdetermined; behavioral conjunction conclusion retired.
Retrieval evidence remains informative. V0.5B / PR #1 provides an identifiable held split.

### Stone Age V7
`NO_STONE_AGE_MEMORY_ATTENTION_ADVANTAGE`

### Stone Age V7.1
`NO_STONE_AGE_ACQUISITION_READINESS`

### Stone Age V7.2
`STONE_AGE_BASIC_ACQUISITION_BOTTLENECK`

### Stone Age V7.3
`PERSISTENT_STATIC_ACQUISITION_BOTTLENECK`

### Stone Age V7.4
`PERSISTENT_FEW_LESSON_ACQUISITION_BOTTLENECK`

### Stone Age V7.5
`DEEPER_REPRESENTATION_ASSOCIATION_BOTTLENECK`

### Stone Age V7.6
Original sensory-encoding diagnosis; reopened after the 0.88.1 normalized-teaching correction.

### Stone Age V7.6R
`THRESHOLD_ENCODING_RESCUE_SURVIVES_SURPRISE`

### Stone Age V7.7
Original 0.88.0/calm protocol superseded before run.

### Stone Age V7.7R
`SURPRISE_CONTRAST_STATIC_RESCUE_CLOSED_LOOP_BOTTLENECK`

### Stone Age V7.8
`DYNAMIC_STATE_TEACHING_INSUFFICIENT`

- dynamic teaching rescues FOOD/HUNT/SHELTER loop behavior
- but repeated online corrections damage static retention
- FIRE is the strongest interference case
- the current boundary is retention under continual supervised correction

## Active frozen experiment

### Stone Age V7.9 — Retention-Protected Caretaker Bridge

Cadence 0.88.1, CONTRAST18, full11, surprise from lesson 0.

Arms:
- STATIC_ONLY
- DAGGER128
- DAGGER64
- DAGGER64_STATIC_REPLAY64

Replay arm:
- 64 learner-path dynamic labels
- 64 balanced static-anchor replay calls
- one replay call after each dynamic step
- 128 total post-bootstrap calls, matched to DAGGER128

Primary question: can balanced static rehearsal preserve V7.7R's learned policy while retaining caretaker-driven closed-loop gains?

See: [stone-age-v7-9](./stone-age-v7-9/README.md)

Shared-brain memory/attention remains closed until retention under correction is resolved.
