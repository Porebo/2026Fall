"""Draw the random order of UIC injection wells for the 14 CCR 1724.7.1 sample.

Usage (from any folder; the CSV path defaults to ../05-data/calgem/all-wells-2026-11-18/):
    python select_sample_uic.py [path/to/AllWells_20261118.csv]

Writes ../06-study/sample-uic/screening-log.csv (every frame well, in one random
order) and ../06-study/sample-uic/frame-summary.csv (frame counts by well type,
status and district). Rules are in ../06-study/sample-uic/README.txt. Same method
as select_sample.py (sort by API, shuffle once with a fixed seed, screen in order).

Requires only the Python standard library.
"""
import csv
import random
import sys
from collections import Counter
from pathlib import Path

SEED = 20261118          # fixed before any well was screened; recorded in README.txt
PRIMARY_N = 30
STATUSES = {"Active", "Idle"}
# CalGEM well-type codes counted as Class II UIC injection wells (README.txt, section 2).
# 14 CCR 1720.1(p): an underground injection project includes waterflood, steamflood,
# cyclic steam, disposal and pressure-maintenance injection; gas storage is excluded.
INJECTION_TYPES = {
    "WF": "Waterflood", "SF": "Steamflood", "SC": "Cyclic Steam",
    "WD": "Water Disposal", "PM": "Pressure Maintenance", "GD": "Gas Disposal",
    "AI": "Air Injection", "INJ": "Injection",
}
HERE = Path(__file__).parent
OUTDIR = HERE.parent / "06-study" / "sample-uic"
DEFAULT_CSV = HERE.parent / "05-data" / "calgem" / "all-wells-2026-11-18" / "AllWells_20261118.csv"
OLD_LOG = HERE.parent / "06-study" / "sample" / "screening-log.csv"

KEEP = {"API": "API", "LeaseName": "LeaseName", "WellNumber": "WellNumber",
        "WellStatus": "WellStatus", "WellType": "WellTypeCode", "WellTypeLa": "WellTypeLabel",
        "FieldName": "FieldName", "AreaName": "AreaName", "CountyName": "County",
        "District": "District"}
LOG_FIELDS = (["Order", "Role", "SampleCode", "API10"] + list(KEEP.values()) +
              ["UIC_Project", "Outcome", "WellSTAR_Status", "WellSTAR_WellType", "DocumentID",
               "DocumentRelevantDate", "DocumentDescription", "CheckedOn", "Notes",
               "DiagramFile", "WellSTAR_FileName", "SHA256", "InW_Sample"])


def load_frame(path):
    rows, seen = [], set()
    counts = Counter()
    with open(path, encoding="utf-8-sig", newline="") as handle:
        for r in csv.DictReader(handle):
            api = r["API"].strip()
            if api in seen:
                continue
            seen.add(api)
            counts["all"] += 1
            if r["WellStatus"] not in STATUSES:
                continue
            counts["active_idle"] += 1
            if r["WellType"] not in INJECTION_TYPES:
                continue
            counts["injection_type"] += 1
            if r["CountyName"].strip().endswith("Offshore"):
                counts["offshore_excluded"] += 1
                continue
            rows.append(r)
    return rows, counts


def old_sample_apis():
    out = {}
    if OLD_LOG.exists():
        with open(OLD_LOG, encoding="utf-8-sig", newline="") as h:
            for r in csv.DictReader(h):
                if r["SampleCode"]:
                    out[r["API10"]] = r["SampleCode"]
    return out


def main(path):
    frame, counts = load_frame(path)
    frame.sort(key=lambda r: r["API"])
    random.Random(SEED).shuffle(frame)
    old = old_sample_apis()

    OUTDIR.mkdir(exist_ok=True)
    with open(OUTDIR / "screening-log.csv", "w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=LOG_FIELDS)
        w.writeheader()
        for order, r in enumerate(frame, start=1):
            row = {v: r[k].strip() for k, v in KEEP.items()}
            row.update(Order=order, API10=r["API"][:10], InW_Sample=old.get(r["API"][:10], ""),
                       Role="Primary" if order <= PRIMARY_N else "Replacement")
            w.writerow(row)

    with open(OUTDIR / "frame-summary.csv", "w", encoding="utf-8", newline="") as h:
        w = csv.writer(h)
        w.writerow(["Group", "Value", "Wells"])
        for k in ("all", "active_idle", "injection_type", "offshore_excluded"):
            w.writerow(["Filter step", k, counts[k]])
        w.writerow(["Filter step", "frame", len(frame)])
        for key, col in (("WellType", "WellType"), ("WellStatus", "WellStatus"),
                         ("District", "District")):
            for val, n in sorted(Counter(r[col] for r in frame).items(), key=lambda t: -t[1]):
                w.writerow([key, val, n])

    print(f"Distinct wells: {counts['all']:,}; Active/Idle: {counts['active_idle']:,}; "
          f"injection types: {counts['injection_type']:,}; offshore removed: "
          f"{counts['offshore_excluded']:,}; frame N = {len(frame):,}")
    print(f"Seed {SEED}. Wrote {OUTDIR}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV)
