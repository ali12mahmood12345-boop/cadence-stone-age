# Cadence Research Status

Updated: 2026-10-26

## Confirmed

### Representation Keys V0.3D
Fresh confirmation on Cadence 0.85.1.

### Memory Keys V0.4B
Fresh confirmation on Cadence 0.85.1.

## Attention correction

### Attention V0.5A
Previous behavioral label `NO_CONJUNCTIVE_MULTI_FACT_SIGNAL` is **retired**.

The original held split was underdetermined: multiple hidden residue assignments fit every taught pair but disagree on the held panel. V0.5A's retrieval observation remains useful, but its held behavioral score cannot test conjunctive generalization.

A corrected identifiable split is proposed in PR #1 as Attention V0.5B. It has not yet received a frozen fresh confirmation run.

## Stone Age development history

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
Original development classification: `STONE_AGE_SENSOR_ENCODING_BOTTLENECK`.

Important correction: this diagnosis is now **provisional** because V7.6 used normalized row-by-row teaching without `learning_surprise=True` from lesson 0.

Cadence 0.88.1 documents that this can cause one-action readout collapse under long normalized curricula.

The V7.6 measurements remain valid for their frozen 0.88.0 recipe, but the causal interpretation is reopened.

See: [stone-age-v7-6](./stone-age-v7-6/README.md)

## Running

### Stone Age V7.6R — Surprise-Corrected Representation Replication

Cadence: `0.88.1`.

Fresh founders: `68001..68008`.

Frozen 2×2 arms:

- RAW18_CALM
- RAW18_SURPRISE
- CONTRAST18_CALM
- CONTRAST18_SURPRISE

Question: does surprise-from-lesson-0 rescue raw Stone Age binary acquisition, or does threshold encoding remain necessary under the corrected teaching rule?

See: [stone-age-v7-6r](./stone-age-v7-6r/README.md)

## Superseded before run

### Stone Age V7.7 — Contrast Encoding Integration Bridge

The original 0.88.0 V7.7 package is superseded before run because it used the now-confounded normalized teaching rule.

Rebuild V7.7 only after V7.6R.

See: [stone-age-v7-7](./stone-age-v7-7/README.md)
