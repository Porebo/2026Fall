"""Summarize the U01–U30 decision records for the human reviewer."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "06-study" / "sample-uic" / "reference"
OUTPUT = REFERENCES / "scoring-review-U01-U30.txt"


def main():
    records = []
    for number in range(1, 31):
        code = f"U{number:02}"
        record = json.loads((REFERENCES / f"{code}.json").read_text(encoding="utf-8"))
        if record["diagram_id"] != code or len(record["points"]) != 90:
            raise ValueError(f"{code}: invalid decision record")
        if any(group["count"] != len(group["instances"]) for group in record["excess_data"]):
            raise ValueError(f"{code}: excess-data count does not match instances")
        records.append(record)

    lines = [
        "U01–U30 CASING-DIAGRAM SCORING REVIEW",
        "Checklist v4.2 — draft decisions for Lester S. Carcamo to verify.",
        "This is a snapshot of the decision records; regenerate after changes.",
        "From the graduate-project folder, run: python scripts\\build_scoring_review.py",
        "Catalog identity can differ from what the source diagram explicitly states.",
        "",
        "SUMMARY: score; subdivisions (a)/(d); subdivisions (b)/(c); excess instances/types",
    ]
    for record in records:
        score = record["score"]
        ad = score["subdivisions_a_d"]
        bc = score["subdivisions_b_c"]
        excess = record["excess_total"]
        lines.append(
            f'{record["diagram_id"]} | {record["well"]["well_name"]} | '
            f'{score["met"]}/{score["applicable"]} ({score["percent"]:.1f}%) | '
            f'{ad["met"]}/{ad["of"]} | {bc["met"]}/{bc["applicable"]} | '
            f'{excess["instances"]}/{excess["types"]}'
        )

    for record in records:
        code = record["diagram_id"]
        well = record["well"]
        lines.extend([
            "",
            "=" * 72,
            f'{code}: {well["well_name"]}',
            f'Catalog API: {well["api"]}; operator: {well["operator"]}',
            f'Source PDF: ..\\diagrams\\{code}.pdf',
            f'Annotated PDF: ..\\..\\design\\figures\\{code}-atomic-map.pdf',
            f'Decision record: {code}.json',
            "",
            "SOURCE IDENTITY (checklist points 01–04)",
        ])
        for point in record["points"][:4]:
            answer = point["displayed_answer"]
            lines.append(f'  {point["number"]:02} {point["label"]}: '
                         f'{point["status"]}' + (f' — {answer}' if answer is not None else ""))

        score = record["score"]
        ad = score["subdivisions_a_d"]
        bc = score["subdivisions_b_c"]
        lines.extend([
            "",
            f'SCORE: {score["met"]}/{score["applicable"]} ({score["percent"]:.1f}%)',
            f'  MET {score["met"]}; MISSING {score["missing"]}; '
            f'NOT APPLICABLE {score["not_applicable"]}',
            f'  (a)/(d): {ad["met"]}/{ad["of"]}; '
            f'MD/non-depth {ad["md_non_depth_met"]}/{ad["md_non_depth_of"]}; '
            f'TVD {ad["tvd_met"]}/{ad["tvd_of"]}',
            f'  (b)/(c): {bc["met"]}/{bc["applicable"]}',
        ])
        for item in record.get("not_applicable_evidence", []):
            lines.append(f'  Point {item["point"]:02} N/A: {item["item"]} — '
                         f'{item["text"]} (page {item["page"]})')
        lines.extend(["", "EXCESS DATA (present but not scored)"])
        for group in record["excess_data"]:
            lines.append(f'  {group["type"]} {group["label"]} ({group["count"]})')
            for item in group["instances"]:
                lines.append(f'    - {item["item"]}: {item["text"]} '
                             f'(page {item["page"]}; {item["reason"]})')

        notes = record.get("uncertain_calls", [])
        lines.extend(["", "UNCERTAIN CALLS FOR REVIEW"])
        if not notes:
            lines.append("  No separate uncertain calls recorded.")
        for note in notes:
            point_list = ", ".join(f"{number:02}" for number in note["points"])
            lines.append(f'  Points {point_list}: {note["reason"]}')
        for point in record["points"]:
            note = point.get("note")
            related = " ".join(
                item["reason"] for item in notes if point["number"] in item["points"]
            )
            if note and note != related:
                lines.append(f'  Additional point {point["number"]:02} note: {note}')

        if record["provenance"]:
            lines.extend(["", "DOCUMENT PROVENANCE (not excess data)"])
            for item in record["provenance"]:
                lines.append(f'  - {item["item"]}: {item["text"]} (page {item["page"]})')

    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT} for {len(records)} diagrams.")


if __name__ == "__main__":
    main()
