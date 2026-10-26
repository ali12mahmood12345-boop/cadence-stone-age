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

Dynamic caretaker teaching rescues much of closed-loop behavior but damages prior static mappings.

### Stone Age V7.9 — Retention-Protected Caretaker Bridge
`STATIC_REPLAY_NO_RETENTION_RESCUE`

- cadence-net 0.88.1
- 8/8 founders valid
- arms: STATIC_ONLY, DAGGER128, DAGGER64, DAGGER64_STATIC_REPLAY64
- one-for-one replay does not restore retained static policy
- replay arm mean median retention = 0.500 vs 0.524 for DAGGER64
- replay arm mean median loop = 0.875 vs 0.750 for DAGGER64
- accepted replay corrections show anchors were genuinely being forgotten:
  - FOOD ~15/64
  - FIRE 33/64
  - HUNT 23/64
  - SHELTER ~22.5/64
- all-four founder readiness remains 0/8 in every arm

Interpretation: rehearsal is active but does not stabilize a joint static+dynamic policy when interleaved one-for-one. The current boundary is continual supervised interference / consolidation scheduling rather than missing trajectory coverage alone.

See: [stone-age-v7-9](./stone-age-v7-9/README.md)

## Next direction

**Stone Age V7.10 — Post-DAgger Consolidation / Recoverability Microscope**

Freeze a DAgger64 phase first, then apply a separate balanced static-replay block at increasing doses and evaluate after each checkpoint.

Primary questions:
- can the old static policy be recovered?
- does recovery preserve the acquired loop behavior?
- was V7.9's interleaved schedule itself the failure mode?

Shared-brain memory/attention remains closed until this retention/consolidation boundary is resolved.
