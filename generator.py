import json, csv, argparse
from dateutil.parser import isoparse

def load_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def build_timeline(alert, actions):
    rows = []
    rows.append(("T0", alert["time"], "Alert Triggered", alert["title"], alert.get("severity", "")))
    for i, a in enumerate(actions, start=1):
        rows.append((f"T{i}", a["time"], a["type"], a["detail"], a.get("owner", "")))
    rows.sort(key=lambda r: isoparse(r[1]))
    return rows

def write_timeline_csv(rows, out_path):
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Marker", "Time", "ActionType", "Detail", "Owner/Notes"])
        w.writerows(rows)

def write_casefile_md(alert, rows, out_path):
    indicators = "\n".join([f"- {ioc}" for ioc in alert.get("indicators", [])]) or "- (none)"
    actions_md = "\n".join([f"- **{r[0]}** {r[1]} — {r[2]}: {r[3]}" for r in rows])

    md = f"""# SOC Incident Casefile

## Summary
- **Title:** {alert["title"]}
- **Time:** {alert["time"]}
- **Severity:** {alert.get("severity", "")}
- **Source:** {alert.get("source", "")}
- **Entity:** {alert.get("entity", "")}

## Indicators
{indicators}

## Timeline
{actions_md}

## Response Notes
- Containment: (add)
- Eradication: (add)
- Recovery: (add)
- Lessons Learned: (add)
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--alert", default="inputs/alert.json")
    ap.add_argument("--actions", default="inputs/actions.json")
    ap.add_argument("--outdir", default="outputs")
    args = ap.parse_args()

    alert = load_json(args.alert)
    actions = load_json(args.actions)

    rows = build_timeline(alert, actions)
    write_timeline_csv(rows, f"{args.outdir}/timeline.csv")
    write_casefile_md(alert, rows, f"{args.outdir}/casefile.md")

    print("[OK] Generated outputs/ casefile.md and timeline.csv")

if __name__ == "__main__":
    main()
