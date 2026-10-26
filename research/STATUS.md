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

### Stone Age V7.6R
`THRESHOLD_ENCODING_RESCUE_SURVIVES_SURPRISE`

### Stone Age V7.7R
`SURPRISE_CONTRAST_STATIC_RESCUE_CLOSED_LOOP_BOTTLENECK`

### Stone Age V7.8
`DYNAMIC_STATE_TEACHING_INSUFFICIENT`

### Stone Age V7.9
`STATIC_REPLAY_NO_RETENTION_RESCUE`

- one-for-one replay was active but did not stabilize retention
- replay anchors repeatedly became surprising again
- dynamic behavior remained strong while static mappings degraded
- current boundary: continual supervised interference / consolidation schedule

## Active frozen experiment

### Stone Age V7.10 — Post-DAgger Consolidation / Recoverability Microscope

Cadence 0.88.1, CONTRAST18, full11, surprise from lesson 0.

Common history:
- static bootstrap
- DAgger64
- then a separate static consolidation block

Checkpoints:
- STATIC_ONLY
- POST_DAGGER64
- REPLAY32
- REPLAY64
- REPLAY_FULL

Primary questions:
- can the original static policy be recovered after DAgger?
- if recovered, does the acquired dynamic behavior survive?
- was V7.9's interleaved replay schedule itself the failure mode?

See: [stone-age-v7-10](./stone-age-v7-10/README.md)

Shared-brain memory/attention remains closed until this retention/consolidation boundary is resolved.
