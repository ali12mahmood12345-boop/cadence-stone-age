# Stone Age V7.47 — native position-rate experiment

**Status: code prepared, no training results yet.**

In this repository, run from the `research/stone-age-v7-47` directory. The runner imports the established `stone-age-v7-45/qualified_reference.py` and the archived V7.36 source via adjacent research folders.

Windows: double-click `START_STONE_AGE_V7_47.bat`. Or run:

```powershell
python -m pip install -r requirements.txt
python run.py --smoke
python run.py --resume
```

Eight matched fresh founders, three arms per founder (24 training runs) are required. `--limit 2 --resume` is only a pilot and does not qualify as the complete experiment. Results are written one arm at a time to `v7_47_results`. After running, upload `V7_47_RESULTS.json` and all 24 `founder_*.json` files for independent audit and GitHub reporting.

The standalone downloadable ZIP also includes a SHA-verified bootstrap for archived upstream references. See `PROTOCOL.md` for hypotheses, gates and limitations.
