# Memory Keys V0.4B — Fresh Confirmation

Cadence: **0.85.1**

Status: **fresh confirmation PASS**

## Question

After native learned code has acquired hidden-group structure from context, can Cadence's own default associative memory use that key to transfer a stored group action to held-out members that were never written to the store?

## Frozen confirmation

V0.4B froze V0.4A exactly and changed only the founder block.

Fresh founders: `58001..58064`.

Memory under test:

`brain.hippocampus` / Cadence `SynapticMemory`

Frozen settings:

- `memory_rate=0.0`
- `consolidation=1.0`
- `memory_amplitude=4.0`
- 3 held-out members/group
- 5 bank members/group
- exactly one persistent memory write per bank member
- founder-randomized group→action mapping
- direct store read plus whole-brain memory-active vs `hippocampus.clear()` causal test

## Result

- **63/64 valid founders**
- CONTEXT64 held-out associative-store accuracy: **100%**
- SHUFFLED64: **25%**
- BOTTOMUP64: **25%**
- FIXED128: **25%**
- RAW: **25%**
- CONTEXT beat every control in **63/63 valid founders**
- median CONTEXT gain over every control: **+0.750**
- whole-brain behavior with memory active: **100%**
- after hippocampus erasure: **25%**
- median causal lift: **+0.750**
- active memory beat erased memory in **63/63 valid founders**
- every frozen confirmation gate passed

Official classification:

`NATIVE_KEY_ASSOCIATIVE_MEMORY_FRESH_CONFIRMATION_PASS`

The single excluded founder, 58057, was excluded because FIXED128 bank fit was 85%, below the frozen 90% validity floor. Its CONTEXT result itself remained 100%.

## Defensible claim

Cadence 0.85.1's context-derived native learned keys are not only geometrically meaningful: Cadence's own associative SynapticMemory can use them to transfer a stored action to held-out members that receive no memory write. The transfer disappears with shuffled context, top-down disabled, raw/fixed keys, and after causal hippocampal erasure.

## Boundary

The memory phase used a controlled direct SynapticMemory write with `consolidation=1.0`. This does not yet establish natural reward-driven episodic recording, replay, or continual revision.
