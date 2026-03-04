# SOC Casefile Generator

Automation tool that converts an alert JSON + actions JSON into:
- `casefile.md` (SOC casefile template)
- `timeline.csv` (chronological incident timeline)

## Run
```bash
pip install -r requirements.txt
python generator.py --alert alert.json --actions actions.json --outdir .
```

## Why this matters (SOC workflow)
- Standardizes case notes and timelines
- Reduces manual documentation
- Supports consistent escalation and post-incident review
