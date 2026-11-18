"""Load one human-reference review JSON (06-study/sample-uic/reference/Uxx.json)
into 04-literature/casing-analysis/casing_specs.db.

Idempotent: re-running replaces that diagram's reference rows (results,
completeness infractions, reference_reviews, non_scored_items) and upserts the
diagrams row. W diagrams are refused (out of study).

Checklist points are mapped to requirement ids by requirement code, read from
the checklist table lines "NN | code | label" in the checklist file
(v4.2: point 32 -> id 88, 33-52 -> 32-51, 53-78 -> 62-87, 79-80 -> 52-53,
81 -> 90, 82-89 -> 54-61, 90 -> 89).

After loading, the casing_final_score view must equal the JSON score
(met, applicable, percentage); otherwise the load is rolled back.

Usage (from the graduate-project folder):
    python scripts/load_reference_json.py 06-study/sample-uic/reference/U01.json [more.json ...]
    python scripts/load_reference_json.py --db path/to.db --checklist path/to/checklist.txt U02.json
"""
import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = ROOT / "04-literature" / "casing-analysis" / "casing_specs.db"
DEFAULT_CHECKLIST = ROOT / "06-study" / "design" / "prompts" / "casing-diagram-atomic-checklist-v4.2.txt"
TOTAL_POINTS = 90

STATUS_MAP = {
    "MET": "MET", "YES": "MET", "PRESENT": "MET",
    "MISSING": "MISSING", "NOT_MET": "MISSING", "NOT MET": "MISSING", "NO": "MISSING", "ABSENT": "MISSING",
    "NOT_APPLICABLE": "NOT_APPLICABLE", "NOT APPLICABLE": "NOT_APPLICABLE", "N/A": "NOT_APPLICABLE", "NA": "NOT_APPLICABLE",
}
CATEGORY_MAP = {
    "EXCESS": "EXCESS", "EXCESS_DATA": "EXCESS", "EXCESS DATA": "EXCESS",
    "PROVENANCE": "PROVENANCE",
    "SUPPORTING": "SUPPORTING", "SUPPORTING_ANOTHER_REQUIREMENT": "SUPPORTING",
    "SUPPORTING ANOTHER REQUIREMENT": "SUPPORTING", "SUPPORTS_ANOTHER_REQUIREMENT": "SUPPORTING",
}


def pick(d, *keys, default=None):
    """First non-empty value among keys (case-insensitive) in dict d."""
    if not isinstance(d, dict):
        return default
    low = {k.lower(): v for k, v in d.items()}
    for k in keys:
        v = low.get(k.lower())
        if v not in (None, "", [], {}):
            return v
    return default


def text(v):
    if v is None:
        return None
    if isinstance(v, (list, dict)):
        if isinstance(v, list) and all(isinstance(x, str) for x in v):
            return "; ".join(v)
        return json.dumps(v, ensure_ascii=False)
    return str(v)


def iso_date(v):
    """'10/31/2023' -> '2023-10-31'; ISO dates pass through."""
    if v is None:
        return None
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", str(v).strip())
    return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}" if m else str(v)


def checklist_codes(path):
    codes = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*(\d{1,2})\s*\|\s*(\([a-d]\)[^|\s]*)\s*\|", line)
        if m:
            n = int(m.group(1))
            if n in codes and codes[n] != m.group(2):
                raise SystemExit(f"checklist point {n} has two codes")
            codes[n] = m.group(2)
    if sorted(codes) != list(range(1, TOTAL_POINTS + 1)):
        raise SystemExit(f"checklist table has {len(codes)} points, expected {TOTAL_POINTS}")
    return codes


def point_to_id(conn, codes):
    ids = dict(conn.execute("SELECT requirement_code, requirement_id FROM spec_requirements"))
    mapping = {}
    for n, code in codes.items():
        if code not in ids:
            raise SystemExit(f"checklist point {n} code {code} not in spec_requirements")
        mapping[n] = ids[code]
    if len(set(mapping.values())) != TOTAL_POINTS:
        raise SystemExit("point-to-id map is not one-to-one")
    return mapping


BBOX_KEYS = ("bbox_pt", "bbox", "box")


def location(item):
    """Return (page, bbox_text).

    page = first page cited. bbox_text = JSON [x0, y0, x1, y1] (PDF points) for
    one box; a JSON list of boxes when several boxes are on one page; the full
    JSON list of {page, bbox_pt} when boxes span pages.
    """
    loc = pick(item, "locations", "location", "loc")
    page = pick(item, "page")
    bbox = pick(item, *BBOX_KEYS)
    if isinstance(loc, dict):
        loc = [loc]
    if isinstance(loc, list) and loc and all(isinstance(x, dict) for x in loc):
        pages = [pick(x, "page") for x in loc]
        boxes = [pick(x, *BBOX_KEYS) for x in loc]
        page = page or pages[0]
        if bbox is None:
            if len(set(pages)) == 1:
                bbox = boxes[0] if len(boxes) == 1 else boxes
            else:
                bbox = loc
    elif isinstance(loc, str) and bbox is None:
        bbox = loc
    try:
        page = int(page) if page is not None else None
    except (TypeError, ValueError):
        page = None
    return page, text(bbox)


def iter_points(data):
    pts = pick(data, "points", "point_statuses", "results", "checklist", "items", "scored_points")
    if isinstance(pts, dict):
        out = []
        for k, v in pts.items():
            v = dict(v) if isinstance(v, dict) else {"status": v}
            v.setdefault("point", k)
            out.append(v)
        return out
    if not isinstance(pts, list):
        raise SystemExit("JSON has no list of point statuses")
    return pts


def iter_non_scored(data):
    ns = pick(data, "non_scored_items", "non_scored", "nonscored", "unscored_items")
    out = []
    if isinstance(ns, dict):
        for cat, items in ns.items():
            for it in items if isinstance(items, list) else [items]:
                it = dict(it) if isinstance(it, dict) else {"instance_text": it}
                it.setdefault("category", cat)
                out.append(it)
    elif isinstance(ns, list):
        out = [dict(it) for it in ns]
    # Separate top-level lists. EXCESS groups ({type, label, count, instances})
    # are expanded to one row per instance.
    for cat, keys in (("EXCESS", ("excess_data", "excess")), ("PROVENANCE", ("provenance",)),
                      ("SUPPORTING", ("supporting_another_requirement", "supporting"))):
        items = pick(data, *keys)
        if not isinstance(items, list):
            continue
        for it in items:
            it = dict(it) if isinstance(it, dict) else {"instance_text": it}
            if isinstance(it.get("instances"), list):
                group = {k: v for k, v in it.items() if k not in ("instances", "count")}
                if it.get("count") is not None and it["count"] != len(it["instances"]):
                    raise SystemExit(f"{group.get('type')}: count {it['count']} != {len(it['instances'])} instances")
                for inst in it["instances"]:
                    inst = dict(inst) if isinstance(inst, dict) else {"text": inst}
                    row = {"category": cat, "type_code": group.get("type"), "label": group.get("label"),
                           "instance_text": pick(inst, "text", "instance_text"),
                           "notes": "; ".join(x for x in (text(pick(inst, "item")), text(pick(inst, "reason"))) if x) or None}
                    row.update({k: v for k, v in inst.items() if k in ("page", "citation", "locations") + BBOX_KEYS})
                    out.append(row)
            else:
                it.setdefault("category", cat)
                if "item" in it and "label" not in it:
                    it["label"] = it.pop("item")
                out.append(it)
    return out


def load(conn, path, mapping, codes):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    well = pick(data, "well", "well_identity", "identity", "diagram", default={}) or {}
    src = {**data, **well} if isinstance(well, dict) else data

    dn = text(pick(data, "diagram_id", "diagram_number")) or Path(path).stem
    if not re.fullmatch(r"U\d{2}", dn):
        raise SystemExit(f"{path}: diagram number {dn!r} is not a study diagram (U01-U30); W diagrams are out of study")

    version = text(pick(data, "checklist_version", "checklist", "version") if not isinstance(pick(data, "checklist"), list)
                   else pick(data, "checklist_version", "version"))
    if version and "4.2" not in version:
        raise SystemExit(f"{path}: checklist version {version!r} is not v4.2")
    version = version or "4.2"
    reviewer = text(pick(data, "reviewer", "reviewer_of_record", "reviewed_by"))
    review_date = text(pick(data, "review_date", "reviewed_on", "date"))

    # Evidence for NOT_APPLICABLE points is kept in a separate list.
    na_evidence = {}
    for it in pick(data, "not_applicable_evidence", default=[]) or []:
        na_evidence[int(it["point"])] = it

    # Points
    rows, seen = [], set()
    for p in iter_points(data):
        n0 = pick(p, "number", "point", "point_number", "checklist_point")
        if n0 is not None and int(n0) in na_evidence and not pick(p, "displayed_answer", "evidence"):
            e = na_evidence[int(n0)]
            p = {**p, "evidence": "; ".join(x for x in (text(e.get("item")), text(e.get("text"))) if x),
                 "page": e.get("page"), "bbox_pt": e.get("bbox_pt")}
        n = int(pick(p, "number", "point", "point_number", "checklist_point"))
        code = pick(p, "code", "requirement_code")
        if code and codes[n] != code:
            raise SystemExit(f"{path}: point {n} code {code} != checklist code {codes[n]}")
        raw = str(pick(p, "status", "result", "verdict", "reference_status")).strip().upper()
        if raw not in STATUS_MAP:
            raise SystemExit(f"{path}: point {n} has unknown status {raw!r}")
        status = STATUS_MAP[raw]
        if n in seen:
            raise SystemExit(f"{path}: point {n} appears twice")
        seen.add(n)
        page, bbox = location(p)
        rows.append((dn, mapping[n], status,
                     text(pick(p, "displayed_answer", "evidence", "evidence_text")),
                     text(pick(p, "explanation", "rationale", "reason", "notes", "note", "comment")),
                     n, page, bbox))
    if seen != set(range(1, TOTAL_POINTS + 1)):
        raise SystemExit(f"{path}: points missing from JSON: {sorted(set(range(1, TOTAL_POINTS + 1)) - seen)}")

    met = sum(r[2] == "MET" for r in rows)
    na = sum(r[2] == "NOT_APPLICABLE" for r in rows)
    applicable = TOTAL_POINTS - na

    score = pick(data, "score", "scoring", "summary", default={}) or {}
    if not isinstance(score, dict):
        score = {}
    j_met = pick(score, "met", "met_items", "complete_items", "numerator")
    j_app = pick(score, "applicable", "applicable_items", "scoring_items", "denominator")
    j_pct = pick(score, "completeness_pct", "completeness_percentage", "percentage", "percent", "pct")
    if isinstance(j_pct, str):
        j_pct = float(j_pct.strip().rstrip("%"))
    j_met = met if j_met is None else int(j_met)
    j_app = applicable if j_app is None else int(j_app)
    j_pct = round(100.0 * j_met / j_app, 1) if j_pct is None else float(j_pct)
    if (j_met, j_app) != (met, applicable):
        raise SystemExit(f"{path}: JSON score {j_met}/{j_app} != point statuses {met}/{applicable}")
    for key, val in (("missing", applicable - met), ("not_applicable", na)):
        if pick(score, key) is not None and int(pick(score, key)) != val:
            raise SystemExit(f"{path}: JSON score {key}={pick(score, key)} != point statuses {val}")

    meta = {
        "api_number": text(pick(src, "api_number", "api", "api10")),
        "well_name": text(pick(src, "well_name", "lease_well", "name")),
        "operator_name": text(pick(src, "operator_name", "operator")),
        "field_name": text(pick(src, "field_name", "field")),
        "county": text(pick(src, "county", "county_name")),
        "uic_project": text(pick(src, "uic_project", "project")),
        "well_type": text(pick(src, "well_type", "well_type_label")),
        "wellstar_doc_id": text(pick(src, "wellstar_doc_id", "wellstar_document_id", "document_id", "doc_id")),
        "diagram_date": iso_date(pick(src, "diagram_date", "diagram_printed_date", "wellstar_document_date")),
        "document_title": text(pick(src, "document_title", "wellstar_file_name")),
        # Same style as W01: repo-relative Windows path.
        "source_file": "classes\\graduate-project\\" + (text(pick(src, "source_file", "source_pdf"))
                       or f"06-study/sample-uic/diagrams/{dn}.pdf").replace("/", "\\"),
    }

    cur = conn.cursor()
    cur.execute("BEGIN IMMEDIATE")
    try:
        w_before = cur.execute("SELECT COUNT(*) FROM diagram_requirement_results WHERE diagram_number LIKE 'W%'").fetchone()[0]
        cur.execute("""
            INSERT INTO diagrams (diagram_number, source_file, document_title, diagram_date, submission_format,
                sample, api_number, well_name, operator_name, field_name, county, uic_project, well_type, wellstar_doc_id)
            VALUES (:dn, :source_file, :document_title, :diagram_date, 'PDF', 'UIC', :api_number, :well_name,
                :operator_name, :field_name, :county, :uic_project, :well_type, :wellstar_doc_id)
            ON CONFLICT (diagram_number) DO UPDATE SET
                source_file = excluded.source_file, document_title = excluded.document_title,
                diagram_date = excluded.diagram_date, sample = 'UIC', api_number = excluded.api_number,
                well_name = excluded.well_name, operator_name = excluded.operator_name,
                field_name = excluded.field_name, county = excluded.county,
                uic_project = excluded.uic_project, well_type = excluded.well_type,
                wellstar_doc_id = excluded.wellstar_doc_id""", {"dn": dn, **meta})
        cur.execute("DELETE FROM non_scored_items WHERE diagram_number = ?", (dn,))
        cur.execute("DELETE FROM reference_reviews WHERE diagram_number = ?", (dn,))
        cur.execute("""DELETE FROM completeness_infractions WHERE result_id IN
                       (SELECT result_id FROM diagram_requirement_results WHERE diagram_number = ?)""", (dn,))
        cur.execute("DELETE FROM diagram_requirement_results WHERE diagram_number = ?", (dn,))
        cur.executemany("""
            INSERT INTO diagram_requirement_results (diagram_number, requirement_id, status, evidence, explanation,
                evaluated_at, checklist_point, location_page, location_bbox)
            VALUES (?, ?, ?, ?, ?, COALESCE(?, CURRENT_TIMESTAMP), ?, ?, ?)""",
            [r[:5] + (review_date,) + r[5:] for r in rows])
        cur.execute("""
            INSERT INTO reference_reviews (diagram_number, checklist_version, reviewer, review_date, met_items,
                missing_items, not_applicable_items, applicable_items, completeness_percentage, source_file)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (dn, version, reviewer, review_date, met, applicable - met, na, applicable, j_pct,
             str(Path(path).resolve().relative_to(ROOT.parent.parent)) if ROOT.parent.parent in Path(path).resolve().parents
             else str(path)))
        ns_rows = []
        for it in iter_non_scored(data):
            cat = CATEGORY_MAP.get(str(pick(it, "category", "kind", "class", default="")).strip().upper())
            if cat is None:
                raise SystemExit(f"{path}: non-scored item has unknown category: {it}")
            page, bbox = location(it)
            sup = pick(it, "supports_point", "supports", "point", "checklist_point")
            req_id = None
            if sup is not None and cat == "SUPPORTING":
                m = re.search(r"\d+", str(sup))
                req_id = mapping.get(int(m.group())) if m else None
            notes = pick(it, "notes", "note", "comment", "explanation")
            if sup is not None and cat == "SUPPORTING":
                notes = "; ".join(x for x in (f"supports point {sup}", text(notes)) if x)
            ns_rows.append((dn, cat, text(pick(it, "type_code", "type", "code")),
                            text(pick(it, "label", "type_label", "name")),
                            text(pick(it, "instance_text", "instance", "text", "value", "evidence", "description")),
                            req_id, page, bbox, text(pick(it, "citation", "cite", "source")), text(notes)))
        ex_total = pick(pick(data, "excess_total", default={}) or {}, "instances")
        n_ex = sum(r[1] == "EXCESS" for r in ns_rows)
        if ex_total is not None and int(ex_total) != n_ex:
            raise SystemExit(f"{path}: excess_total.instances={ex_total} but {n_ex} EXCESS rows")
        cur.executemany("""
            INSERT INTO non_scored_items (diagram_number, category, type_code, label, instance_text, requirement_id,
                location_page, location_bbox, citation, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", ns_rows)

        db = cur.execute("""SELECT complete_items, scoring_items, completeness_percentage
                            FROM casing_final_score WHERE diagram_number = ?""", (dn,)).fetchone()
        if db != (j_met, j_app, round(j_pct, 1)):
            raise SystemExit(f"{path}: score view {db} != JSON score {(j_met, j_app, j_pct)}")
        bc = pick(score, "subdivisions_b_c")
        if isinstance(bc, dict):
            db_bc = cur.execute("""SELECT complete_items, scoring_items FROM casing_bc_subtotal
                                   WHERE diagram_number = ?""", (dn,)).fetchone()
            j_bc = (int(pick(bc, "met")), int(pick(bc, "applicable", "of")))
            if db_bc != j_bc:
                raise SystemExit(f"{path}: (b)-(c) subtotal view {db_bc} != JSON {j_bc}")
        w_after = cur.execute("SELECT COUNT(*) FROM diagram_requirement_results WHERE diagram_number LIKE 'W%'").fetchone()[0]
        if w_after != w_before:
            raise SystemExit("W rows changed; aborting")
        fk = cur.execute("PRAGMA foreign_key_check").fetchall()
        if fk:
            raise SystemExit(f"foreign_key_check failed: {fk[:5]}")
        conn.commit()
    except BaseException:
        conn.rollback()
        raise
    inf = conn.execute("""SELECT COUNT(*) FROM completeness_infractions i JOIN diagram_requirement_results r
                          USING (result_id) WHERE r.diagram_number = ?""", (dn,)).fetchone()[0]
    print(f"{dn}: results={len(rows)} infractions={inf} reference_reviews=1 non_scored_items={len(ns_rows)} "
          f"score={db[0]}/{db[1]}={db[2]}% (JSON {j_met}/{j_app}={j_pct}%) OK")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("json_files", nargs="+")
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--checklist", default=str(DEFAULT_CHECKLIST))
    a = ap.parse_args()
    conn = sqlite3.connect(a.db, isolation_level=None)
    conn.execute("PRAGMA foreign_keys = ON")
    codes = checklist_codes(a.checklist)
    mapping = point_to_id(conn, codes)
    for f in a.json_files:
        load(conn, f, mapping, codes)
    print("integrity_check:", conn.execute("PRAGMA integrity_check").fetchone()[0])
    conn.close()


if __name__ == "__main__":
    sys.exit(main())
