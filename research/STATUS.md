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

- contrast + surprise + full11 reaches 100/100 median exact/fresh on all four skills
- dynamic execution remains the boundary

### Stone Age V7.8 — Caretaker / DAgger Dynamic-State Bridge
`DYNAMIC_STATE_TEACHING_INSUFFICIENT`

- cadence-net 0.88.1
- 8/8 founders valid
- matched 128 dynamic labels/skill in expert and DAgger arms
- STATIC_ONLY preserves 100/100 median exact/fresh
- CARETAKER_DAGGER closed-loop medians:
  - FOOD 100%
  - FIRE 0%
  - HUNT 100%
  - SHELTER 100%
- but static retention after DAgger falls to:
  - FOOD 50/50%
  - FIRE 33.3/33.3%
  - HUNT 86.5/88.9%
  - SHELTER 66.7/66.7%
- scripted expert trajectories show the same qualitative retention tradeoff
- founder-level all-four readiness remains 0/8 for every arm

Interpretation: caretaker teaching confirms dynamic-state coverage matters, but online corrections interfere with previously learned static mappings. The next bottleneck is retention under continual supervised correction.

See: [stone-age-v7-8](./stone-age-v7-8/README.md)

## Next direction

**Stone Age V7.9 — Retention-Protected Caretaker Bridge**

Proposed frozen comparison:
- STATIC_ONLY
- DAGGER128
- DAGGER64
- DAGGER64_STATIC_REPLAY64

The replay arm interleaves 64 learner-path dynamic labels with 64 balanced static-anchor labels, keeping 128 post-bootstrap lesson calls. DAGGER64 is the dose control.

Question: can static rehearsal preserve the V7.7R policy while retaining caretaker-driven loop gains?

Shared-brain memory/attention remains closed until retention under correction is resolved.
