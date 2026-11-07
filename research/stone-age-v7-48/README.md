# Cadence Stone Age V7.48 — Fresh-seed confirmation

V7.47 rate improvement passed its initial eight-founder gates. This folder performs **fresh independent-seed confirmation** under the same three arms; it does not change the task or Cadence version.

1. Download [the complete repository ZIP](https://github.com/ali12mahmood12345-boop/cadence-stone-age/archive/refs/heads/main.zip) and extract it.
2. Enter `research/stone-age-v7-48`.
3. Windows: double-click `START_STONE_AGE_V7_48.bat`. It installs dependencies, runs the smoke test, then resumes from any **already completed arm files**.
4. Alternative: `python -m pip install -r requirements.txt`, `python run.py --smoke`, `python run.py --resume`.

All 8 seeds 108001–108008 are required, with 3 arms each = **24 full training runs**. `--limit 2` is a pilot only. Run results save into `v7_48_results/` one complete arm at a time. If an arm fails, do not treat it as valid or silently retry it. Upload the entire result directory as ZIP/RAR for independent verification and GitHub reporting.

See [PROTOCOL.md](PROTOCOL.md) for prespecified validity and effect thresholds. The repository checkout provides unchanged V7.45 and V7.36 archived reference modules adjacent to this directory. The experiment requires Cadence 0.91.1.
