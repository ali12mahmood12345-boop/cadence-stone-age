# V0.5B local pilot (not the frozen run)

`run_v05b.py` on cadence-net 0.88.0, founders 59101-59104, 1024 lessons, as declared in
[PROTOCOL.md](PROTOCOL.md). These founders were chosen for a local check of the runner; the
frozen run should declare fresh founders. Raw outputs: `results/v05b_<seed>.json`.

Held accuracy on 192 held patterns (chance 1/3), and the held panel under each causal control:

| Founder | Arm | Taught | Held | role0 erased | role1 erased | distractors erased | memory off | clone head |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 59101 | H2 | 0.66 | **0.65** | 0.35 | 0.39 | 0.75 | 0.38 | 0.59 |
| 59101 | H1 | 0.50 | 0.49 | 0.34 | 0.32 | 0.59 | 0.31 | |
| 59102 | H2 | 0.75 | **0.68** | 0.31 | 0.34 | 0.53 | 0.31 | 0.68 |
| 59102 | H1 | 0.68 | 0.53 | 0.31 | 0.31 | 0.40 | 0.31 | |
| 59103 | H2 | 0.84 | **0.72** | 0.34 | 0.39 | 0.78 | 0.38 | 0.68 |
| 59103 | H1 | 0.76 | 0.69 | 0.36 | 0.39 | 0.76 | 0.38 | |
| 59104 | H2 | 0.92 | **0.86** | 0.29 | 0.38 | 1.00 | 0.38 | 0.83 |
| 59104 | H1 | 0.63 | 0.63 | 0.36 | 0.36 | 0.44 | 0.38 | |

- Held accuracy is above chance in every founder and arm; H2 exceeds H1 in all four founders
  (mean 0.73 against 0.58).
- Erasing either relevant fact, or all records, returns the held panel to chance: the answer
  depends on both retrieved facts.
- The two heads attend to different roles on 100% of held trials, and the pair they attend is
  the relevant pair (roles 0 and 1) on 100%.
- Calm teaching never engaged (the running wrong share stayed above 0.02); no lesson was
  refused.

Under V0.5A's split the same question read at chance for both arms, as `split_check.py`
predicts for any learner there. With a split whose held answers the taught pairs determine, the
conjunctive signal appears. Four founders are a pilot, not a test of V0.5A's frozen gates.

## The teaching rule as an arm (26 October 2026)

Will Glynn ran this runner on five founders to 4,096 lessons (cadence-teachers
[EXP-71/EXP-72](https://github.com/WGlynn/cadence-teachers/blob/main/experiments/EXP-72.md)):
under the calm rule three of five learned and then collapsed onto one action; with
`learning_surprise=True` from the first lesson all five answered every taught pair from about
1,024 lessons on, held .72 to .96 (mean .85 against .53), and erasing either relevant fact still
dropped held to chance. `--teaching surprise` adds that arm; `--read-every N` reads taught and
held accuracy on deep copies along the way.

Founder 59201, H2, 4,096 lessons, on this machine (`results/exp72_<teaching>_59201.json`):

| Teaching | Taught / held at 768 | Taught / held at 4,096 | Modal share at 4,096 | Held, role0 / role1 erased |
| --- | --- | --- | --- | --- |
| calm (never reached the .02 switch) | .81 / .79 | .39 / .31 | 1.00 | .31 / .38 |
| surprise from the first lesson | .99 / .88 | 1.00 / .88 | .39 (the largest label class) | .38 / .31 |

Under the calm rule this founder never reached the switch, so every lesson taught every row.
The collapse sits in the cortex graph: putting the lesson-768 graph into the collapsed brain
restores .81 taught, while the collapsed brain's address maps in the healthy brain change
nothing. Lessons on rows already answered keep pushing the readout until the nudge no longer
moves it (its movement of the motor population fell a hundredfold), and a lapse then stays.
For the frozen V0.5B run the teaching rule belongs among the declared arms.
