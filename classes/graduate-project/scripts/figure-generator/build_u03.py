"""Build the U03 reference record and atomic-point map from its two-page PDF."""

import base64
import csv
import hashlib
import html
import json
import os
import re
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "06-study/sample-uic/diagrams/U03.pdf"
CHECKLIST = ROOT / "06-study/design/prompts/casing-diagram-atomic-checklist-v4.2.txt"
SVG = Path(os.environ.get("FIG_OUT", ROOT / "06-study/sample-uic/diagrams/U03.svg"))
PNG = SVG.with_suffix(".png")
PDF = Path(os.environ.get("PDF_OUT", ROOT / "06-study/design/figures/U03-atomic-map.pdf"))
JSON = Path(os.environ.get("REF_OUT", ROOT / "06-study/sample-uic/reference/U03.json"))

with CHECKLIST.open(encoding="utf-8") as stream:
    points = []
    for line in stream:
        match = re.fullmatch(r"(\d\d) \| (\S+) \| (.+)", line.strip())
        if match:
            points.append((int(match[1]), match[2], match[3]))
assert [point[0] for point in points] == list(range(1, 91))

doc = pymupdf.open(SOURCE)
assert doc.page_count == 2
assert all(tuple(page.rect) == (0, 0, 612, 792) for page in doc)


def loc(page_number, *box):
    return {"page": page_number, "bbox_pt": list(box)}


evidence = {
    1: ("SENTINEL PEAK RESOURCES CALIFORNIA LLC", [loc(1, 23.9, 18.0, 241.2, 28.4)]),
    2: ("MCKITTRICK FEE", [loc(1, 125.2, 50.3, 204.2, 60.7)]),
    3: ("409", [loc(1, 23.9, 28.8, 87.4, 39.2)]),
    4: ("0403033302", [loc(1, 53.0, 39.5, 105.1, 50.0)]),
    5: ("7/31/2007", [loc(1, 303.6, 29.1, 346.3, 39.8)]),
    7: ("KB: 904.00 ft; Datum: 10.00 ft", [loc(1, 273.8, 51.1, 461.1, 61.8)]),
    8: ("BFW: N/A ft", [loc(1, 273.8, 51.1, 317.8, 61.8)]),
    10: ("Conductor 16 in; Surface 10 3/4 in; Inner Casing 5 1/2 in; Production 7 in", [
        loc(1, 403.6, 97.2, 410.7, 104.4), loc(1, 398.2, 107.3, 416.2, 114.5),
        loc(1, 400.0, 117.4, 414.3, 124.6), loc(1, 405.4, 127.5, 408.9, 134.7),
    ]),
    11: ("A53B; J-55; K-55; N-80", [
        loc(1, 565.5, 97.2, 581.4, 104.4), loc(1, 567.2, 107.3, 579.8, 114.5),
        loc(1, 566.6, 117.4, 580.3, 124.6), loc(1, 566.5, 127.5, 580.5, 134.7),
    ]),
    14: ("Set depths: 50, 280, 2,180, and 2,222 ftKB", [
        loc(1, 448.2, 97.2, 455.4, 104.4), loc(1, 446.4, 107.3, 457.2, 114.5),
        loc(1, 443.7, 117.4, 459.9, 124.6), loc(1, 443.7, 127.5, 459.9, 134.7),
    ]),
    17: ("Perforation top depths: 1,980; 2,000; 2,040; 2,082 ftKB", [
        loc(1, 397.8, 677.5, 415.8, 684.8), loc(1, 397.8, 695.5, 415.8, 702.8),
        loc(1, 397.8, 713.5, 415.8, 720.8), loc(1, 397.8, 731.5, 415.8, 738.8),
    ]),
    18: ("Perforation intervals: 1,980–2,020; 2,000–2,020; 2,040–2,070; 2,082–2,110 ftKB", [
        loc(1, 397.8, 677.5, 441.0, 692.2), loc(1, 397.8, 695.5, 441.0, 710.2),
        loc(1, 397.8, 713.5, 441.0, 728.2), loc(1, 397.8, 731.5, 440.8, 746.2),
    ]),
    28: ("Squeeze cement through perforations", [loc(1, 474.1, 571.7, 593.0, 608.7)]),
    32: ("Tubing killstring and tubing components", [loc(2, 322.1, 78.5, 582.2, 208.1)]),
    34: ("TD: 2,230.00 ftKB", [loc(1, 273.8, 62.2, 350.0, 72.9)]),
    35: ("Plug Cement; Plug Cement", [
        loc(1, 322.3, 348.2, 363.2, 355.7), loc(1, 322.3, 504.5, 363.2, 512.0),
    ]),
    36: ("Plug tops: 2,103 and 2,180 ftKB", [
        loc(1, 376.0, 372.3, 392.2, 379.5), loc(1, 376.0, 528.5, 392.2, 535.7),
    ]),
    37: ("Plug bottoms: 2,180 and 2,230 ftKB", [
        loc(1, 406.3, 372.3, 422.5, 379.5), loc(1, 406.3, 528.5, 422.5, 535.7),
    ]),
    38: ("Conductor, Surface, Inner Casing, Production, and Squeeze Cement", [
        loc(1, 322.3, 148.8, 382.6, 156.3), loc(1, 322.3, 199.9, 373.3, 207.4),
        loc(1, 322.3, 282.0, 389.3, 289.5), loc(1, 322.3, 391.4, 384.1, 398.9),
        loc(1, 322.3, 547.7, 375.9, 555.2),
    ]),
    39: ("Fill tops: 10, 10, 10, 10, and 2,179.9 ftKB", [
        loc(1, 380.5, 172.8, 387.7, 180.0), loc(1, 380.5, 223.9, 387.7, 231.2),
        loc(1, 380.5, 306.0, 387.7, 313.2), loc(1, 380.5, 415.5, 387.7, 422.7),
        loc(1, 373.3, 571.7, 394.9, 578.9),
    ]),
    40: ("Fill bottoms: 50, 280, 2,180, 2,230, and 2,180 ftKB", [
        loc(1, 410.8, 172.8, 418.0, 180.0), loc(1, 409.0, 223.9, 419.8, 231.2),
        loc(1, 406.3, 306.0, 422.5, 313.2), loc(1, 406.3, 415.5, 422.5, 422.7),
        loc(1, 406.3, 571.7, 422.5, 578.9),
    ]),
    45: ("Zone names: TULARE; TULARE UCL; TOP HYDROCARBON; SAN JOAQUIN/ETCHEGOIN; DIATOMITE UCL; DIATOMITE", [
        loc(2, 322.2, 228.3, 347.8, 235.5), loc(2, 322.2, 238.3, 362.6, 245.6),
        loc(2, 322.2, 248.4, 388.4, 255.6), loc(2, 322.2, 258.5, 406.5, 265.7),
        loc(2, 322.2, 268.6, 372.3, 275.8), loc(2, 322.2, 278.7, 357.5, 285.9),
    ]),
    46: ("Zone top depths: 273.3, 391.7, 437.0, 1,096.7, 1,615.5, 1,792.0 ftKB", [
        loc(2, 575.3, 228.3, 591.5, 235.5), loc(2, 575.3, 238.3, 591.5, 245.6),
        loc(2, 575.3, 248.4, 591.5, 255.6), loc(2, 569.9, 258.5, 591.5, 265.7),
        loc(2, 569.9, 268.6, 591.5, 275.8), loc(2, 569.9, 278.7, 591.5, 285.9),
    ]),
    81: ("Cement job dates: 7/1/2007; 7/31/2007; 3/9/2022; 3/9/2022; 8/3/2007; 8/3/2007; 1/25/2022", [
        loc(1, 331.9, 172.8, 357.1, 180.0), loc(1, 330.1, 223.9, 358.9, 231.2),
        loc(1, 331.9, 306.0, 357.1, 313.2), loc(1, 331.9, 372.3, 357.1, 379.5),
        loc(1, 331.9, 415.5, 357.1, 422.7), loc(1, 331.9, 528.5, 357.1, 535.7),
        loc(1, 330.1, 571.7, 358.9, 578.9),
    ]),
    87: ("Directional survey MD stations (ftKB)", [
        loc(1, 85.7, 76.8, 252.7, 85.7), loc(1, 29.1, 134.6, 44.9, 752.4),
    ]),
}

NA = {90}
met = set(evidence)
status = {n: ("MET" if n in met else "NOT_APPLICABLE" if n in NA else "MISSING")
          for n, _, _ in points}

uncertain = [
    {"points": [6, 7], "reason": "The header gives KB 904.00 ft and Datum 10.00 ft, but no separate ground-elevation label. The draft treats 904.00 as the reference elevation and leaves ground elevation missing."},
    {"points": [13], "reason": "Three casing weights are listed, but the conductor row has no weight; the repeated-instance rule makes the point MISSING."},
    {"points": [28], "reason": "The diagram describes squeeze cement through perforations. The draft counts this as an other flow/integrity feature; Lester should confirm that classification."},
    {"points": [34], "reason": "TD 2,230 ftKB is shown. The draft treats this as the hole-depth answer; it is not separately labeled 'hole depth'."},
    {"points": [38, 39, 40], "reason": "The draft treats the squeeze-cement entry as a cement fill in addition to the conductor, surface, inner-casing, and production fills."},
    {"points": [43, 45, 46, 47, 48], "reason": "The page 2 table is titled 'Zones and Sand Markers'; all six names and tops appear under 'Zone Name', while the 'Geological Marker' column is blank. The draft scores zone names/depths only, not formations or markers."},
    {"points": [82, 83, 84, 85, 86], "reason": "Cement data is present for several jobs, but not all entries. The conductor mix/volume is labeled unknown, and the two plug rows refer to earlier casing-cement jobs without repeating slurry data. The draft applies the repeated-job rule and marks each point MISSING."},
    {"points": [87, 88, 89], "reason": "The diagram has a Directional heading and MD stations, but no inclination or azimuth values. The draft scores the MD path only."},
    {"points": [90], "reason": "The document is labeled Original Hole and shows one borehole, so point 90 is NOT_APPLICABLE."},
]


def find(page_number, phrase, occurrence=0):
    found = doc[page_number - 1].search_for(phrase)
    if occurrence >= len(found):
        raise ValueError(f"Could not locate {phrase!r} occurrence {occurrence} on page {page_number}")
    return tuple(round(value, 1) for value in found[occurrence])


excess = [
    ("E1", "Well location (field and PLSS)", [
        ("Field name", "CYMRIC", 1, find(1, "CYMRIC")),
        ("PLSS locator", "Sec. 6, T. 30S, R. 22E, MD B&M", 1, find(1, "Sec. 6, T. 30S, R. 22E, MD B&M")),
    ]),
    ("E2", "KB-ground height", [
        ("Datum / KB-ground height", "10.00 ft", 1, find(1, "10.00")),
    ]),
    ("E3", "Rig-release and completion dates", [
        ("Rig release date", "8/4/2007", 1, find(1, "8/4/2007")),
        ("Completion date", "10/12/2007", 1, find(1, "10/12/2007")),
    ]),
    ("E4", "Perforation dates", [
        ("Perforation date 1", "10/11/2007", 1, find(1, "10/11/2007", 0)),
        ("Perforation date 2", "6/7/2022", 1, find(1, "6/7/2022")),
        ("Perforation date 3", "10/11/2007", 1, find(1, "10/11/2007", 1)),
        ("Perforation date 4", "10/10/2007", 1, find(1, "10/10/2007")),
    ]),
    ("E5", "Perforation shot density", [
        (f"Shot density {i + 1}", "4.0 shots/ft", 1, box)
        for i, box in enumerate((
            (450.2, 677.5, 459.2, 684.8), (450.2, 695.5, 459.2, 702.8),
            (450.2, 713.5, 459.2, 720.8), (450.2, 731.5, 459.2, 738.8),
        ))
    ]),
    ("E6", "Perforation gun size / comment", [
        ("Gun size", "3 1/8 in", 1, find(1, "3 1/8")),
        ("Gun comment", "4 JHPF", 1, find(1, "4 JHPF")),
    ]),
    ("E7", "Perforation status", [
        ("Perforation status 1", "Closed / abandoned", 1, (536.8, 677.5, 589.7, 692.2)),
        ("Perforation status 2", "Open", 1, (536.8, 695.5, 585.3, 710.2)),
        ("Perforation status 3", "Closed / abandoned", 1, (536.8, 713.5, 589.7, 728.2)),
        ("Perforation status 4", "Closed / abandoned", 1, (536.8, 731.5, 589.7, 746.2)),
    ]),
    ("E8", "Plug-back depth and date", [
        ("Plug-back depth", "2,103 ft", 1, find(1, "2,103", 1)),
        ("Plug-back/tag date", "3/9/2022", 1, find(1, "3/9/2022", 2)),
    ]),
    ("E9", "Casing inside diameters", [
        ("Conductor ID", "15.25 in", 1, find(1, "15.25")),
        ("Surface casing ID", "10.05 in", 1, find(1, "10.05")),
        ("Inner casing ID", "4.89 in", 1, find(1, "4.89")),
        ("Production casing ID", "6.37 in", 1, find(1, "6.37")),
    ]),
]

provenance = [
    {"item": "Directional-profile timestamp", "text": "8/3/2022 2:04:37 PM", "page": 1,
     "bbox_pt": [178.5, 76.8, 252.7, 85.7]},
    {"item": "Repeated directional-profile timestamp", "text": "8/3/2022 2:04:37 PM", "page": 2,
     "bbox_pt": [178.5, 76.8, 252.7, 85.7]},
]
na_evidence = {
    "point": 90, "item": 'Wellbore designation "Original Hole"', "text": "Original Hole",
    "page": 1, "bbox_pt": list(find(1, "Original Hole")),
}
with (ROOT / "06-study/sample-uic/screening-log.csv").open(encoding="utf-8", newline="") as stream:
    screening = next(row for row in csv.DictReader(stream) if row["SampleCode"] == "U03")
assert screening["SHA256"].upper() == hashlib.sha256(SOURCE.read_bytes()).hexdigest().upper()

ad_met = sum(n in met for n in range(1, 79))
bc_met = sum(n in met for n in range(79, 91))
applicable = 90 - len(NA)
score = 100 * len(met) / applicable

point_records = []
for n, code, name in points:
    answer, locations = evidence.get(n, (None, []))
    record = {
        "number": n, "code": code, "label": name, "status": status[n],
        "displayed_answer": answer, "locations": locations,
    }
    if n == 90:
        record["note"] = "One borehole shown: Original Hole."
    for item in uncertain:
        if n in item["points"]:
            record["note"] = item["reason"]
    point_records.append(record)
for record in point_records:
    for location in record["locations"]:
        page = doc[location["page"] - 1]
        x0, y0, x1, y1 = location["bbox_pt"]
        assert page.rect.contains(pymupdf.Rect(x0, y0, x1, y1)), (record["number"], location)

excess_data = [
    {
        "type": type_id, "label": title, "count": len(items),
        "instances": [
            {"item": name, "text": value, "reason": "Present on the diagram but not a scored point.",
             "page": page_number, "bbox_pt": list(box)}
            for name, value, page_number, box in items
        ],
    }
    for type_id, title, items in excess
]
excess_total = {"instances": sum(len(items) for _, _, items in excess), "types": len(excess)}

reference = {
    "diagram_id": "U03",
    "source_pdf": "06-study/sample-uic/diagrams/U03.pdf",
    "page_scored": "1-2",
    "well": {
        "well_name": f"{screening['LeaseName']} {screening['WellNumber']}",
        "lease_name": screening["LeaseName"], "well_number": screening["WellNumber"],
        "api": screening["API10"], "operator": "Sentinel Peak Resources California LLC",
        "field": screening["FieldName"], "county": screening["County"],
        "district": screening["District"],
        "well_type": f"{screening['WellTypeCode']} {screening['WellTypeLabel']}",
        "well_status": screening["WellStatus"], "uic_project": screening["UIC_Project"],
        "diagram_printed_date": "08/03/2022",
        "wellstar_document_id": screening["DocumentID"],
        "wellstar_document_date": screening["DocumentRelevantDate"],
        "wellstar_file_name": screening["WellSTAR_FileName"],
        "sha256": screening["SHA256"],
    },
    "checklist_version": "v4.2", "reviewer": "Lester S. Carcamo", "review_date": "2026-11-18",
    "score": {
        "met": len(met), "applicable": applicable, "not_applicable": len(NA),
        "missing": applicable - len(met), "percent": round(score, 1),
        "subdivisions_a_d": {
            "met": ad_met, "of": 78, "md_non_depth_met": ad_met,
            "md_non_depth_of": 52, "tvd_met": 0, "tvd_of": 26,
        },
        "subdivisions_b_c": {"met": bc_met, "applicable": 11},
    },
    "points": point_records, "excess_data": excess_data, "provenance": provenance,
    "supporting_another_requirement": [], "not_applicable_evidence": [na_evidence],
    "excess_total": excess_total, "uncertain_calls": uncertain,
}

groups = [
    ((1, 1), "(a)(1) Well identification", "#0072B2"),
    ((2, 4), "(a)(2)–(4) Spud, elevations", "#E69F00"),
    ((5, 6), "(a)(5)–(6) Water bases", "#009E73"),
    ((7, 8), "(a)(7)–(8) Casing and shoe", "#009E73"),
    ((9, 9), "(a)(9) Perforations", "#CC79A7"),
    ((10, 11), "(a)(10)–(11) Equipment; hole", "#8C564B"),
    ((12, 13), "(a)(12)–(13) Cement plugs, fill", "#332288"),
    ((15, 15), "(a)(15) Formations, zones", "#999933"),
    ((79, 90), "(b)–(c) Cement, wellbore path", "#56B4E9"),
]


def group(number):
    if number >= 79:
        return groups[-1]
    match = re.match(r"\(a\)\((\d+)\)", points[number - 1][1])
    if match:
        for item in groups[:-1]:
            if item[0][0] <= int(match[1]) <= item[0][1]:
                return item
    raise ValueError(f"No colour group for point {number}")


def ink(color):
    rgb = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    rgb = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in rgb]
    luminance = .2126 * rgb[0] + .7152 * rgb[1] + .0722 * rgb[2]
    return "#111" if (luminance + .05) / .055 >= 4.5 else "#fff"


def safe(value):
    return html.escape(str(value), quote=True)


def text(x, y, value, size=8.7, color="#333", bold=False, anchor="start"):
    weight = ' font-weight="bold"' if bold else ""
    return (f'<text font-family="Helvetica, Arial, sans-serif" x="{x:.2f}" y="{y:.2f}" '
            f'font-size="{size}" fill="{color}"{weight} text-anchor="{anchor}">{safe(value)}</text>')


main_clip = pymupdf.Rect(18, 12, 594, 756)
main_pix = doc[0].get_pixmap(dpi=180, clip=main_clip, alpha=False)
main_png = base64.b64encode(main_pix.tobytes("png")).decode("ascii")
main_x, main_y, main_w = 230, 92, 450
main_scale = main_w / main_clip.width
main_h = main_clip.height * main_scale

inset_clip = pymupdf.Rect(315, 75, 595, 290)
inset_pix = doc[1].get_pixmap(dpi=260, clip=inset_clip, alpha=False)
inset_png = base64.b64encode(inset_pix.tobytes("png")).decode("ascii")
inset_x, inset_y, inset_w = 520, 690, 240
inset_scale = inset_w / inset_clip.width
inset_h = inset_clip.height * inset_scale


def display_box(location):
    page_number = location["page"]
    x0, y0, x1, y1 = location["bbox_pt"]
    if page_number == 1:
        return (main_x + (x0 - main_clip.x0) * main_scale,
                main_y + (y0 - main_clip.y0) * main_scale,
                main_x + (x1 - main_clip.x0) * main_scale,
                main_y + (y1 - main_clip.y0) * main_scale)
    return (inset_x + (x0 - inset_clip.x0) * inset_scale,
            inset_y + (y0 - inset_clip.y0) * inset_scale,
            inset_x + (x1 - inset_clip.x0) * inset_scale,
            inset_y + (y1 - inset_clip.y0) * inset_scale)


X1, W1, X2, W2 = 48, 130, 181, 18
Y0, PITCH, PH = 102, 10, 9
md = [item for item in points if not item[1].endswith(".tvd")]
tvd = {item[1][:-4]: item for item in points if item[1].endswith(".tvd")}
assert len(md) == 64 and len(tvd) == 26

short = {
    "Other equipment in the well (e.g., tubing, pumps, rods)": "Other equipment in the well",
    "Cement-yield calculation steps": "Cement-yield calc. steps",
    "Cement job identification (date or stage)": "Cement job identification",
    "Slurry volume (or sacks) for each cement job": "Slurry volume (or sacks)",
    "Slurry density for each cement job": "Slurry density",
    "Slurry yield for each cement job": "Slurry yield",
    "Cement type for each cement job": "Cement type",
    "Cement additives for each cement job": "Cement additives",
    "Wellbore path: measured depth (MD)": "Wellbore path: MD",
    "Borehole designation (original hole, redrill, or sidetrack; conditional: multiple boreholes only)": "Borehole designation: N/A",
}


def label(value):
    return short.get(value, value).replace(" (MD)", "")


def tw(value, size=8.7, bold=False):
    return pymupdf.get_text_length(value, fontname="hebo" if bold else "helv", fontsize=size)


svg = [
    '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
    'width="8.5in" height="11in" viewBox="0 0 816 1056" font-family="Helvetica, Arial, sans-serif">',
    "<title>U03 atomic data-point map</title>", '<rect width="816" height="1056" fill="#fff"/>',
    text(48, 65, f"Casing Diagram U03 · Checklist v4.2 · Final score {score:.1f}% "
         f"({len(met)} of {applicable} applicable points MET)", 14.7, "#111", True),
    text(48, 79, "Scored by Lester S. Carcamo · November 18, 2026", 9.3, "#444"),
    text(51, 98, "MD / non-depth", 8.7, "#333", True),
    text(190, 98, "TVD", 8.7, "#333", True, "middle"),
    f'<image x="{main_x}" y="{main_y}" width="{main_w}" height="{main_h:.2f}" '
    f'preserveAspectRatio="none" xlink:href="data:image/png;base64,{main_png}"/>',
    f'<rect x="{main_x}" y="{main_y}" width="{main_w}" height="{main_h:.2f}" '
    'fill="none" stroke="#bbb" stroke-width=".5"/>',
    text(inset_x, inset_y - 5, "Page 2 evidence: tubing and zones", 8.4, "#333", True),
    f'<image x="{inset_x}" y="{inset_y}" width="{inset_w}" height="{inset_h:.2f}" '
    f'preserveAspectRatio="none" xlink:href="data:image/png;base64,{inset_png}"/>',
    f'<rect x="{inset_x}" y="{inset_y}" width="{inset_w}" height="{inset_h:.2f}" '
    'fill="none" stroke="#bbb" stroke-width=".5"/>',
]

row_y = {}
for index, (n, code, name) in enumerate(md):
    y = Y0 + (index + (n >= 79)) * PITCH
    row_y[n] = y + PH / 2
    if n == 79:
        svg.append(text(50, y - 2, "§ 1724.7.1(b)–(c) (no TVD pair)", 8.7, "#333", True))
    current = status[n]
    color = group(n)[2] if current == "MET" else "#6b6b6b" if current == "NOT_APPLICABLE" else "#cfcfcf"
    fill = color if current == "MET" else "#fff" if current == "NOT_APPLICABLE" else "#f0f0f0"
    foreground = ink(color) if current == "MET" else "#666" if current == "NOT_APPLICABLE" else "#999"
    dash = ' stroke-dasharray="2.2 1.4"' if current == "NOT_APPLICABLE" else ""
    svg.append(f'<rect x="{X1}" y="{y}" width="{W1}" height="{PH}" rx="4.5" '
               f'fill="{fill}" stroke="{color}" stroke-width=".6"{dash}/>')
    if current == "MET":
        svg.append(f'<rect x="{X1+1}" y="{y+1}" width="12" height="7" rx="3.5" fill="#fff"/>')
    svg.append(text(X1 + 7, y + 7.3, f"{n:02d}", 8.1,
                    color if current == "MET" else foreground, True, "middle"))
    assert tw(label(name), 8.7) <= W1 - 18, (n, name)
    svg.append(text(X1 + 17, y + 7.4, label(name), 8.7, foreground))
    if code.endswith(".md"):
        paired = tvd[code[:-3]]
        svg.append(f'<rect x="{X2}" y="{y}" width="{W2}" height="{PH}" rx="4.5" '
                   'fill="#f0f0f0" stroke="#cfcfcf" stroke-width=".6"/>')
        svg.append(text(X2 + W2 / 2, y + 7.4, f"{paired[0]:02d}", 8.7, "#999", anchor="middle"))

# Connectors and evidence frames for page 1. Page 2's frames carry matching point badges in the inset.
for index, n in enumerate(sorted(met)):
    _, color = group(n)[1:]
    first = evidence[n][1][0]
    if first["page"] == 1:
        x0, y0, _, _ = display_box(first)
        lane = 204 + index * .65
        source_path = f'{X1+W1},{row_y[n]:.2f}'
        if points[n - 1][1].endswith(".md"):
            gutter_x, gap_y = X1 + W1 + 1.5, row_y[n] - 5
            source_path += (f' {gutter_x:.2f},{row_y[n]:.2f} '
                            f'{gutter_x:.2f},{gap_y:.2f} {lane:.2f},{gap_y:.2f}')
        else:
            source_path += f' {lane:.2f},{row_y[n]:.2f}'
        svg.append(f'<polyline points="{source_path} {lane:.2f},{y0-1:.2f} {x0:.2f},{y0-1:.2f}" '
                   f'fill="none" stroke="{color}" stroke-width=".65" stroke-linejoin="round"/>')
    for item in evidence[n][1]:
        x0, y0, x1, y1 = display_box(item)
        svg.append(f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{x1-x0:.2f}" height="{y1-y0:.2f}" '
                   f'fill="none" stroke="{color}" stroke-width=".85"><title>{n:02d}: '
                   f'{safe(evidence[n][0])}</title></rect>')
    if first["page"] == 2:
        x0, y0, _, _ = display_box(first)
        svg.append(f'<rect x="{x0:.2f}" y="{y0-8:.2f}" width="14" height="8" rx="1.2" '
                   f'fill="{color}"/>')
        svg.append(text(x0 + 7, y0 - 1.5, f"{n:02d}", 6.8, ink(color), True, "middle"))

na_box = display_box(na_evidence)
a, b, c, d0 = na_box
svg.append(f'<rect x="{a:.2f}" y="{b:.2f}" width="{c-a:.2f}" height="{d0-b:.2f}" '
           'fill="none" stroke="#6b6b6b" stroke-width=".8" stroke-dasharray="2 1.4"/>')
svg.append(text(a, b - 2, "90 N/A", 8, "#6b6b6b", True))

excess_badge_positions = {
    "E1": [(122, 50), (131, 61)], "E2": [(456, 51)],
    "E3": [(475, 29), (564, 29)], "E4": [(357, 677), (352, 695), (357, 713), (357, 731)],
    "E5": [(460, 677), (460, 695), (460, 713), (460, 731)],
    "E6": [(485, 695), (514, 695)], "E7": [(590, 677), (585, 695), (590, 713), (590, 731)],
    "E8": [(377, 630), (348, 630)], "E9": [(246, 161), (246, 231), (241, 671), (301, 715)],
}
for type_id, _, items in excess:
    for name, value, page_number, box in items:
        item = loc(page_number, *box)
        x0, y0, x1, y1 = display_box(item)
        svg.append(f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{x1-x0:.2f}" height="{y1-y0:.2f}" '
                   f'fill="none" stroke="#d62728" stroke-width=".7"><title>{safe(type_id)}: '
                   f'{safe(name)} {safe(value)}</title></rect>')
    for bx, by in excess_badge_positions[type_id]:
        x, y, _, _ = display_box(loc(1, bx, by, bx + 15, by + 9))
        svg.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="15" height="9" rx="1.5" '
                   'fill="#d62728" stroke="#fff" stroke-width=".4"/>')
        svg.append(text(x + 7.5, y + 7.1, type_id, 7.2, "#fff", True, "middle"))

for item in provenance:
    if item["page"] != 1:
        continue
    x0, y0, x1, y1 = display_box(item)
    svg.append(f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{x1-x0:.2f}" height="{y1-y0:.2f}" '
               'fill="none" stroke="#111" stroke-width=".9" stroke-dasharray=".1 1.6" '
               'stroke-linecap="round"/>')

key_y = Y0 + (len(md) + 1) * PITCH + 12
svg.append(text(48, key_y, "Key: MET, by requirement group", 9.3, "#111", True))
key_y += 11
for _, title, color in groups:
    svg.append(f'<rect x="48" y="{key_y-7:.2f}" width="16" height="9" rx="4.5" fill="{color}"/>')
    svg.append(text(69, key_y, title, 8.2))
    key_y += 10
for line in ["Grey pill: MISSING; no connector", "Coloured frame + badge: answer",
             "Red frame: Excess data, not scored", "Dashed grey: point 90 not applicable",
             "Dotted black: document provenance"]:
    svg.append(text(48, key_y, line, 8.2))
    key_y += 10

sy = 691
svg.append(text(230, sy, "Completeness score (Equation 1)", 9.3, "#111", True))
sy += 13
svg.append(text(230, sy, "Completeness = points marked MET ÷ applicable points", 8.7, "#111", True))
sy += 11
for line in [
    f"(a), (d) MET: {ad_met} of 78 (MD/non-depth {ad_met} of 52; TVD 0 of 26)",
    f"(b), (c) MET: {bc_met} of 11 applicable (90 N/A: one borehole)",
    f"Total MET: {len(met)}; applicable: {applicable}; missing: {applicable-len(met)}",
]:
    svg.append(text(238, sy, line, 8.0))
    sy += 9.5
svg.append(text(238, sy + 1, f"Completeness(U03) = {len(met)} ÷ {applicable} = "
                f"{len(met)/applicable:.3f} → {score:.1f}%", 9.1, "#111", True))
sy += 14
for line in [
    "MD stations are shown; no inclination or azimuth values appear.",
    "Source: U03.pdf (2 pages); checklist v4.2. Lester reviews calls.",
]:
    svg.append(text(230, sy, line, 7.8, "#444"))
    sy += 9.2

ex_x, ex_y = 230, 785
svg.append(text(ex_x, ex_y, "Excess data found in U03", 9.2, "#111", True))
ex_y += 11
svg.append(text(ex_x, ex_y, "(present, not required; not scored)", 8.0))
ex_y += 12
for type_id, title, items in excess:
    svg.append(f'<rect x="{ex_x}" y="{ex_y-7:.2f}" width="15" height="9" rx="1.5" fill="#d62728"/>')
    svg.append(text(ex_x + 7.5, ex_y, type_id, 7.2, "#fff", True, "middle"))
    svg.append(text(ex_x + 20, ex_y, title, 7.6))
    svg.append(text(500, ex_y, f"×{len(items)}", 7.6, "#111", anchor="end"))
    ex_y += 9.5
svg.append(text(ex_x, ex_y + 1, f"{excess_total['instances']} instances in "
                f"{excess_total['types']} types", 8.1, "#111", True))
prov_y = 910
svg.append(text(520, prov_y, "Document provenance (not required; not scored)", 7.8, "#111", True))
svg.append(text(520, prov_y + 11, "Directional timestamp: 8/3/2022 2:04:37 PM ×2", 7.5))
assert max(key_y, ex_y + 2, prov_y + 14, inset_y + inset_h) < 1008
svg.append("</svg>")

for path in (SVG, PDF, JSON):
    path.parent.mkdir(parents=True, exist_ok=True)
svg_text = "\n".join(svg)
SVG.write_text(svg_text, encoding="utf-8")
svg_doc = pymupdf.open(stream=svg_text.encode("utf-8"), filetype="svg")
svg_page = svg_doc[0]
svg_page.get_pixmap(matrix=pymupdf.Matrix(1224 / svg_page.rect.width,
                                          1584 / svg_page.rect.height),
                    alpha=False).save(PNG)
out_pdf = pymupdf.open(stream=svg_doc.convert_to_pdf(), filetype="pdf")
out_pdf.save(PDF)
out_pdf.close()
JSON.write_text(json.dumps(reference, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"U03: {len(met)}/{applicable} = {score:.1f}%")
print(f"(a)/(d): {ad_met}/78; (b)/(c): {bc_met}/11; excess: {excess_total}")
print(f"Outputs: {SVG}, {PNG}, {PDF}, {JSON}")
