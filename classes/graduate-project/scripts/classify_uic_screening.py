"""Apply the eligibility rules of ../06-study/sample-uic/README.txt to the raw
WellSTAR screening results and fill in ../06-study/sample-uic/screening-log.csv.

Usage: python classify_uic_screening.py [--overrides overrides.json]

Reads every screening-raw/batch-*.json, assigns one outcome code per screened
row, selects the diagram for each eligible well, numbers INCLUDED wells U01...
in screening order, and stops numbering at 30. Manual decisions made after
looking at a downloaded file (for example a diagram titled "Proposed") are
read from screening-raw/overrides.json: {"API10": {"outcome": ..., "note": ...,
"exclude_ids": [...]}}.
Standard library only.
"""
import csv
import json
import re
from datetime import date
from pathlib import Path

HERE = Path(__file__).parent
DIR = HERE.parent / "06-study" / "sample-uic"
RAW = DIR / "screening-raw"
LOG = DIR / "screening-log.csv"
CUTOFF = date(2019, 4, 1)          # operative date of 14 CCR 1724.7.1
TARGET = 30
APPROVED = {"Active", "Suspended"}  # UIC project statuses counted as approved
PLANNED = re.compile(r"propos|abandon|sidetrack|\bST\d*\b|permit", re.I)


def d(s):
    m, dd, y = s.split("/")
    return date(int(y), int(m), int(dd))


def classify(r, ov):
    """Return (outcome, chosen diagram or None, project string, note)."""
    projs = r.get("projects") or []
    uic_inj = [p for p in projs if p[0] == "UIC" and p[4] == "Injector" and p[2] in APPROVED]
    pstr = "; ".join(f"{p[0]} {p[1]} {p[3]} ({p[2]}, {p[4]})" for p in projs)
    if r.get("error"):
        return "NOT_FOUND", None, pstr, r["error"][:80]
    if (r.get("status") or "") not in ("Active", "Idle"):
        return "STATUS_CHANGED", None, pstr, f"WellSTAR status {r.get('status')}"
    if not uic_inj:
        return "NOT_UIC_INJECTOR", None, pstr, ""
    wbd = [w for w in r.get("wbd", []) if w["id"] not in ov.get("exclude_ids", [])]
    if not r.get("wbd"):
        return "NO_DIAGRAM", None, pstr, ""
    existing = [w for w in wbd if not PLANNED.search(w["desc"] + " " + w["file"])]
    if not existing:
        return "PROPOSED_ONLY", None, pstr, ov.get("note", "")
    # latest Relevant Date; ties: description naming "Current", then highest Document ID
    key = lambda w: (d(w["rel"]), "current" in w["desc"].lower(), int(w["id"]))
    existing.sort(key=key, reverse=True)
    recent = [w for w in existing if d(w["rel"]) >= CUTOFF]
    if not recent:
        return "PRE_RULE_ONLY", existing[0], pstr, ""
    pdfs = [w for w in recent if w["file"].lower().endswith(".pdf")]
    if not pdfs:
        return "NOT_PDF", recent[0], pstr, f"Only non-PDF file(s): {recent[0]['file']}"
    best = pdfs[0]
    note = ov.get("note", "")
    if best is not recent[0]:
        note = (f"Latest diagram {recent[0]['id']} ({recent[0]['rel']}) is not a PDF "
                f"({recent[0]['file']}); latest PDF used. " + note).strip()
    return "INCLUDED", best, pstr, note


def main():
    ovf = RAW / "overrides.json"
    overrides = json.loads(ovf.read_text()) if ovf.exists() else {}
    raw = {}
    for f in sorted(RAW.glob("batch-*.json")):
        b = json.loads(f.read_text(encoding="utf-8"))
        for r in b["results"]:
            raw[r["api"]] = (r, b["checkedOn"])
    with open(LOG, encoding="utf-8", newline="") as h:
        rd = csv.DictReader(h)
        fields, rows = rd.fieldnames, list(rd)
    n = 0
    counts = {}
    for row in rows:
        if row["API10"] not in raw:
            continue
        r, checked = raw[row["API10"]]
        ov = overrides.get(row["API10"], {})
        out, best, pstr, note = classify(r, ov)
        if "outcome" in ov:
            out = ov["outcome"]
        if out == "INCLUDED":
            if n >= TARGET:
                out, note = "NOT_NEEDED", "Eligible; screened after the 30th INCLUDED well"
            else:
                n += 1
                row["SampleCode"] = f"U{n:02d}"
                row["DiagramFile"] = f"diagrams/U{n:02d}.pdf"
        counts[out] = counts.get(out, 0) + 1
        row.update(Outcome=out, WellSTAR_Status=r.get("status") or "", WellSTAR_WellType=r.get("type") or "",
                   UIC_Project=pstr, CheckedOn=checked, Notes=note,
                   DocumentID=best["id"] if best else "", DocumentRelevantDate=best["rel"] if best else "",
                   DocumentDescription=best["desc"] if best else "",
                   WellSTAR_FileName=best["file"] if best and out == "INCLUDED" else "")
        if out != "INCLUDED":
            row["SampleCode"] = row["DiagramFile"] = ""
            if out not in ("PRE_RULE_ONLY", "NOT_NEEDED", "NOT_PDF"):
                row.update(DocumentID="", DocumentRelevantDate="", DocumentDescription="")
    with open(LOG, "w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print("screened", sum(counts.values()), counts)


if __name__ == "__main__":
    main()
