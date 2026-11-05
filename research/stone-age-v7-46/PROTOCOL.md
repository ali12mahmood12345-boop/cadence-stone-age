# V7.46 protocol — offline attribution

Input: 16 files founder_105001..105008_{EXACT,NATIVE}.json from V7.45. One rerun of the archived analysis against the supplied full records, no new Cadence training.

1. Verify arm labels and seed, eight complete matched pairs, no runtime errors, all 17,424 lessons per arm qualified, all solver phases <=.003, frozen P_c and address map exactly zero.
2. Recompute each of three checkpoint TEST accuracies (1100 tests x 3 conditions), CAL accuracy (440 records), and map-top (22 entries).
3. Align TEST/BASE episodes between paired arms by test_index, length, query; tally both correct, both wrong, EXACT-only correct, NATIVE-only correct.
4. Partition NATIVE errors into top predecessor versus not top predecessor; report denominators.
5. Label results descriptive, not causal. Native recall_boundary=True and no manual START were inherited from V7.45. No modification or replay of weights occurs.
