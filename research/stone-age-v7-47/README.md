# Stone Age V7.47 — native position-rate experiment

**Status: COMPLETE — 24/24 valid arms; see [RESULTS.md](RESULTS.md).**

In this repository, run from the `research/stone-age-v7-47` directory. The runner imports the established `stone-age-v7-45/qualified_reference.py` and the archived V7.36 source via adjacent research folders.

Windows: double-click `START_STONE_AGE_V7_47.bat`. Or run:

```powershell
python -m pip install -r requirements.txt
python run.py --smoke
python run.py --resume
```

Eight matched fresh founders, three arms per founder (24 training runs) are required. `--limit 2 --resume` is only a pilot and does not qualify as the complete experiment. Results are written one arm at a time to `v7_47_results`. After running, upload `V7_47_RESULTS.json` and all 24 `founder_*.json` files for independent audit and GitHub reporting.

The standalone downloadable ZIP also includes a SHA-verified bootstrap for archived upstream references. See `PROTOCOL.md` for hypotheses, gates and limitations.

## Verified outcome

V7.47 independent audit: D792 NATIVE 0.20 median BASE 98.14% versus native 0.10 median BASE 91.41%. Median paired improvement +4.77 percentage points with all 8 founders positive. The prespecified native rate effect and validity/control gates passed. See [RESULTS.md](RESULTS.md). Fresh confirmation is preregistered in [V7.48](../stone-age-v7-48/PROTOCOL.md).
