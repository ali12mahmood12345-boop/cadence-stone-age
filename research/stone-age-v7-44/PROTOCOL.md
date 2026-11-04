# V7.44 — Two-founder full-dose migration bridge

V7.43 produced exact agreement in reported behavior, trial records, geometry and phase summaries on both matched founders and both repeats, at only 22 examples/pair. Timings were close to parity. It did not establish full-dose preservation or a meaningful speedup.

Extend matched founders 104001 and 104002 to the original cumulative doses D198/D396/D792, with unchanged full calibration/test panels (20/50 examples per pair). One continuous brain per founder/version. Run old/new for 104001 and new/old for 104002; isolated processes and virtual environments, common thread caps and recorded environment metadata. Report end-to-end run time descriptively: only one timed run per founder/version, including composition and evaluations, so do not treat noise-level differences as reliable speedups.

Retain V7.43's shared configuration: qualified phases, tolerance=.003, free/nudged caps=4096, damping=3 starting at full dt. This differs from the half-dt start in V7.41/V7.42. Retain the documented 0.93.1 signature-only exact-teacher adapter and read-only diagnostic properties. Native recall_boundary=True; no manual START; original exact teacher and frozen address/P_c. Warnings and failed phases stop that founder.

Primary question: do both versions complete both founders validly and preserve matched checkpoint metrics, trial records and map records? Exact equality is the strict compatibility endpoint, not an assertion of whole-state identity. Retain raw files for any mismatch. Additionally inspect predecessor oracle integrity and BASE acquisition. Do not use eight-founder validity thresholds for this two-founder diagnostic or claim population confirmation. Even successful parity requires a later full-cohort migration confirmation before declaring the library upgrade validated for general use.

The launcher smoke-tests each version before the full runs. Results save after each complete founder/version; no within-founder resume. Require run_complete=true and same_environment=true for final comparison. If invalid, inspect the actual error before continuing migration.

