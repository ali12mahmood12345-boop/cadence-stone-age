CADENCE // STONE AGE V5 — MOCHI-INSPIRED SELECTIVE CAREGIVER

WHY
Our V4 experiments showed that fixed drilling and repeated rescue can create
interference between prerequisite mappings.

Mochi uses a different raising pattern: one continuing brain, a scripted mother
that corrects only disagreements, and periods where the mother holds back so the
animal lives with its own answers.

V5 isolates that pattern in the Stone Age COLD chain.

IMPORTANT
This is Mochi-inspired. It does NOT reproduce Mochi's full anatomy, world,
working stores or exact mother protocol.

CHAIN
GATHER_WOOD -> GATHER_STONE -> CRAFT_FIRE -> WARM_UP

FULL STATE IS OBSERVED
- warmth
- has wood
- has stone
- has fire
- wood count
- stone count

The target action is NOT encoded in the observation.

ONE CONTINUING BRAIN
Every training arm keeps one Brain.compose brain through the whole life.

CAREGIVER SCHEDULE
Default quick run:
4 guided decisions
8 autonomous decisions
repeat

ARMS

natural_only
- no caregiver
- learns only from actual terminal success/failure

grade_only
- no action label
- during guided windows, the executed action gets:
  +0.5 if it agreed with the caregiver
  -0.5 if it disagreed

corrective_teacher
- teacher is NOT supplied continuously
- only after an executed mistake in a guided window
- the wrong action leaves the prerequisite state unchanged
- so the teacher correction labels the same failed cue

founder
- frozen untrained control

random
- uniform-random action baseline

AFTER CAREGIVER LEAVES
Each trained brain continues living with no caregiver for another block.
Then it is frozen and evaluated again.

QUICK
1. setup_v5.bat
2. run_quick_v5.bat

Do NOT run Full until Quick is reviewed.

OUTPUT
benchmark_output_v5/quick_REPORT.txt

REFERENCES
Mochi:
https://github.com/muellerberndt/mochi

Cadence quickstart:
https://github.com/muellerberndt/cadence/blob/main/docs/quickstart.md
