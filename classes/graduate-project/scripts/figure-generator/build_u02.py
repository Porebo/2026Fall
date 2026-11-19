"""Build the U02 reference record and atomic-point map from the scanned page."""

import base64
import csv
import html
import json
import os
import re
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "06-study/sample-uic/diagrams/U02.pdf"
CHECKLIST = ROOT / "06-study/design/prompts/casing-diagram-atomic-checklist-v4.2.txt"
SVG = Path(os.environ.get("FIG_OUT", ROOT / "06-study/sample-uic/diagrams/U02.svg"))
PNG = SVG.with_suffix(".png")
PDF = Path(os.environ.get("PDF_OUT", ROOT / "06-study/design/figures/U02-atomic-map.pdf"))
JSON = Path(os.environ.get("REF_OUT", ROOT / "06-study/sample-uic/reference/U02.json"))

points = []
for line in CHECKLIST.read_text(encoding="utf-8").splitlines():
    match = re.fullmatch(r"(\d\d) \| (\S+) \| (.+)", line.strip())
    if match:
        points.append((int(match[1]), match[2], match[3]))
assert [p[0] for p in points] == list(range(1, 91))

# Coordinates are measured on the original PDF page, not on the cropped image.
# A list of boxes preserves separately displayed instances of the same point.
evidence = {
    1: ("bry logo", [(79, 68, 122, 82)]),
    2: ("SW", [(124, 90, 136, 96)]),
    3: ("54-59", [(138, 90, 156, 96)]),
    4: ("0403066117", [(77, 109, 112, 115)]),
    5: ("9/18/2019", [(211, 121, 239, 128)]),
    6: ("1,333.00", [(77, 121, 101, 128)]),
    7: ("1,347.00", [(125, 121, 149, 128)]),
    10: ("Conductor: 14 in; production: 5 1/2 in", [(350, 151, 362, 164)]),
    11: ("Conductor: H-40; production: K-55", [(402, 151, 419, 164)]),
    13: ("Conductor: 32.70; production: 17.00 lb/ft", [(383, 151, 398, 164)]),
    14: ("Conductor: 94.0; production: 1,555.0 ftKB", [(488, 151, 513, 164)]),
    17: (
        "Top depths: 1,240.0, 1,250.0, 1,400.0, 1,410.0 ftKB",
        [(335, 201, 358, 234)],
    ),
    18: (
        "1,240.0–1,250.0; 1,250.0–1,260.0; "
        "1,400.0–1,410.0; 1,410.0–1,420.0 ftKB",
        [(389, 201, 412, 234), (335, 201, 358, 234)],
    ),
    30: ("Packers: 1,291.4 and 1,292.4 ftKB", [(253, 355, 277, 374)]),
    32: (
        "Tubing, hanger, fatigue nipple, pup joints and wireline guide; "
        "tubing set at 1,295.0 ftKB",
        [(253, 282, 519, 388)],
    ),
    35: ("Production Casing Cement (plug)", [(184, 548, 242, 559)]),
    36: ("1,514.0 ftKB", [(202, 554, 220, 559)]),
    37: ("1,555.0 ftKB", [(221, 554, 240, 559)]),
    38: (
        "Conductor Cement; Production Casing Cement",
        [(184, 282, 226, 287), (184, 309, 242, 314)],
    ),
    39: ("Conductor: 14.0; production: 14.0 ftKB", [(226, 282, 238, 287), (184, 314, 197, 319)]),
    40: ("Conductor: 94.0; production: 1,555.0 ftKB", [(184, 287, 196, 292), (197, 314, 218, 319)]),
    45: ("Zone labels: San…, Etch…, Low…, Potter, Dia…, UC…", [(94, 306, 111, 402)]),
    81: (
        "Conductor cement: 9/18/2019; production casing cement: "
        "9/20/2019; production casing cement plug: 9/20/2019",
        [(196, 287, 219, 292), (218, 314, 240, 319), (184, 557, 206, 562)],
    ),
    88: ("Deviated (15° to 30°)", [(98, 187, 145, 193)]),
}
NA = {90}
assert not set(evidence).intersection(NA)
met = set(evidence)
status = {n: ("MET" if n in met else "NOT_APPLICABLE" if n in NA else "MISSING") for n, _, _ in points}

location_reason = "Well location is not listed in § 1724.7.1(a)."
excess = [
    ("E1", "Well location (field, county, PLSS, lat/long)", location_reason, [
        ("Field name", "MNDI RPT", (145, 109, 176, 115)),
        ("County", "Kern 030", (213, 109, 239, 115)),
        ("State", "CA", (287, 109, 298, 115)),
        ("Section", "2", (320, 109, 325, 115)),
        ("Township", "31S", (343, 109, 355, 115)),
        ("Range", "22E", (383, 109, 395, 115)),
        ("Survey", "SE Corner", (422, 109, 453, 115)),
        ("Latitude", "35.2536760000", (354, 121, 397, 128)),
        ("Longitude", "-119.5802220000", (423, 121, 474, 128)),
    ]),
    ("E2", "KB-ground height", "Not itself listed in (a).", [
        ("KB-ground height", "14.00", (174, 121, 190, 128)),
    ]),
    ("E3", "Rig-release and TD dates", "These dates are not listed in (a).", [
        ("Rig release date", "9/21/2019", (258, 121, 286, 128)),
        ("TD date", "9/20/2019", (306, 121, 334, 128)),
    ]),
    ("E4", '"Operated?" flag', "The operated flag is not listed in (a).", [
        ("Operated?", "Yes", (494, 121, 505, 128)),
    ]),
    ("E5", "Perforation dates", "Perforation dates are not listed in (a)(9).", [
        (f"Perforation date {i + 1}", "1/20/2020", (253, y, 280, y + 6))
        for i, y in enumerate((201, 209, 217, 225))
    ]),
]
provenance = [
    ("Profile timestamp", "8/11/2022 12:32:07 PM", (180, 187, 229, 193)),
    ("Report source", "www.peloton.com", (77, 594, 131, 600)),
    ("Page number", "Page 1/1", (282, 594, 310, 600)),
    ("Report printed", "Report Printed: 8/11/2022", (433, 594, 513, 600)),
]
na_evidence = {
    "point": 90,
    "item": 'Wellbore designation "Original Hole"',
    "text": "Original Hole",
    "page": 1,
    "bbox_pt": [146, 187, 179, 193],
}
uncertain = [
    {
        "points": [2],
        "reason": 'The diagram displays "SW"; the screening record expands the lease name to Southwestern. '
        "The draft accepts the abbreviation as the displayed answer.",
    },
    {
        "points": [12],
        "reason": 'The production casing shows "Liberty" but the conductor casing connection is blank; '
        "the repeated-instance rule makes the draft result MISSING.",
    },
    {
        "points": [38, 39, 40, 81],
        "reason": "The conductor and production casing cement labels are treated as two fills; "
        "the production cement plug is recorded separately as shown.",
    },
    {
        "points": [45, 46],
        "reason": "Zone labels and zone-depth cells are visibly truncated. The draft treats the displayed "
        "names as answers but marks zone depths MISSING because the UC… value is cut off at '1,'; "
        "the tiny MD-axis values cannot be reliably transcribed.",
    },
]

with (ROOT / "06-study/sample-uic/screening-log.csv").open(encoding="utf-8", newline="") as stream:
    screening = next(row for row in csv.DictReader(stream) if row["SampleCode"] == "U02")

ad_met = sum(n in met for n in range(1, 79))
bc_met = sum(n in met for n in range(79, 91))
applicable = 90 - len(NA)
score = 100 * len(met) / applicable

point_records = []
for n, code, label in points:
    text, boxes = evidence.get(n, (None, []))
    record = {
        "number": n,
        "code": code,
        "label": label,
        "status": status[n],
        "displayed_answer": text,
        "locations": [{"page": 1, "bbox_pt": list(box)} for box in boxes],
    }
    if n == 90:
        record["note"] = "One borehole shown: Original Hole."
    for item in uncertain:
        if n in item["points"]:
            record["note"] = item["reason"]
    point_records.append(record)

excess_data = []
for type_id, label, reason, items in excess:
    excess_data.append({
        "type": type_id,
        "label": label,
        "count": len(items),
        "instances": [
            {"text": value, "item": item, "reason": reason, "page": 1, "bbox_pt": list(box)}
            for item, value, box in items
        ],
    })

reference = {
    "diagram_id": "U02",
    "source_pdf": "06-study/sample-uic/diagrams/U02.pdf",
    "page_scored": 1,
    "well": {
        "well_name": f"{screening['LeaseName']} {screening['WellNumber']}",
        "lease_name": screening["LeaseName"],
        "well_number": screening["WellNumber"],
        "api": screening["API10"],
        "operator": "Berry (bry logo; no text name)",
        "field": screening["FieldName"],
        "county": screening["County"],
        "district": screening["District"],
        "well_type": f"{screening['WellTypeCode']} {screening['WellTypeLabel']}",
        "well_status": screening["WellStatus"],
        "uic_project": screening["UIC_Project"],
        "diagram_printed_date": "08/11/2022",
        "wellstar_document_id": screening["DocumentID"],
        "wellstar_document_date": screening["DocumentRelevantDate"],
        "wellstar_file_name": screening["WellSTAR_FileName"],
        "sha256": screening["SHA256"],
    },
    "checklist_version": "v4.2",
    "reviewer": "Lester S. Carcamo",
    "review_date": "2026-11-18",
    "score": {
        "met": len(met), "applicable": applicable, "not_applicable": len(NA),
        "missing": applicable - len(met), "percent": round(score, 1),
        "subdivisions_a_d": {
            "met": ad_met, "of": 78, "md_non_depth_met": ad_met,
            "md_non_depth_of": 52, "tvd_met": 0, "tvd_of": 26,
        },
        "subdivisions_b_c": {"met": bc_met, "applicable": 11},
    },
    "points": point_records,
    "excess_data": excess_data,
    "provenance": [
        {"item": name, "text": value, "page": 1, "bbox_pt": list(box)}
        for name, value, box in provenance
    ],
    "supporting_another_requirement": [],
    "not_applicable_evidence": [na_evidence],
    "excess_total": {"instances": sum(len(group[3]) for group in excess), "types": len(excess)},
    "uncertain_calls": uncertain,
}

groups = [
    ((1, 1), "(a)(1) Well identification", "#0072B2"),
    ((2, 4), "(a)(2)–(4) Spud, elevations", "#E69F00"),
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
    code = points[number - 1][1]
    match = re.match(r"\(a\)\((\d+)\)", code)
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


def tw(value, size=8.7, bold=False):
    return pymupdf.get_text_length(value, fontname="hebo" if bold else "helv", fontsize=size)


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


md = [p for p in points if not p[1].endswith(".tvd")]
tvd = {p[1][:-4]: p for p in points if p[1].endswith(".tvd")}
assert len(md) == 64 and len(tvd) == 26

doc = pymupdf.open(SOURCE)
assert doc.page_count == 1
page = doc[0]
clip = pymupdf.Rect(75, 65, 520, 605)
pix = page.get_pixmap(dpi=220, clip=clip, alpha=False)
encoded = base64.b64encode(pix.tobytes("png")).decode("ascii")

X1, W1, X2, W2 = 48, 130, 181, 18
IX, IY, IW = 230, 90, 538
scale = IW / clip.width
IH = clip.height * scale
Y0, PITCH, PH = 102, 10, 9


def position(x, y):
    return IX + (x - clip.x0) * scale, IY + (y - clip.y0) * scale


def display_box(box):
    x0, y0 = position(box[0], box[1])
    x1, y1 = position(box[2], box[3])
    return x0, y0, x1, y1


def text(x, y, value, size=8.7, color="#333", bold=False, anchor="start"):
    weight = ' font-weight="bold"' if bold else ""
    return (f'<text font-family="Helvetica, Arial, sans-serif" x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{color}"'
            f'{weight} text-anchor="{anchor}">{safe(value)}</text>')


svg = [
    '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
    'width="8.5in" height="11in" viewBox="0 0 816 1056" '
    'font-family="Helvetica, Arial, sans-serif">',
    "<title>U02 atomic data-point map</title>",
    '<rect width="816" height="1056" fill="#fff"/>',
    text(48, 65, f"Casing Diagram U02 · Checklist v4.2 · Final score {score:.1f}% "
         f"({len(met)} of {applicable} applicable points MET)", 14.7, "#111", True),
    text(48, 79, "Scored by Lester S. Carcamo · November 18, 2026", 9.3, "#444"),
    text(51, 98, "MD / non-depth", 8.7, "#333", True),
    text(190, 98, "TVD", 8.7, "#333", True, "middle"),
    f'<image x="{IX}" y="{IY}" width="{IW:.2f}" height="{IH:.2f}" '
    f'preserveAspectRatio="none" xlink:href="data:image/png;base64,{encoded}"/>',
    f'<rect x="{IX}" y="{IY}" width="{IW:.2f}" height="{IH:.2f}" '
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

# Frame endpoints and evidence boxes use the same PDF coordinates as the JSON.
for index, n in enumerate(sorted(met)):
    _, color = group(n)[1:]
    boxes = evidence[n][1]
    x0, y0, x1, y1 = display_box(boxes[0])
    lane = 201 + index * 1.05
    target_y = y0 - 1
    source_path = f'{X1+W1},{row_y[n]:.2f}'
    if points[n - 1][1].endswith(".md"):
        gutter_x, gap_y = X1 + W1 + 1.5, row_y[n] - 5
        source_path += (f' {gutter_x:.2f},{row_y[n]:.2f} '
                        f'{gutter_x:.2f},{gap_y:.2f} {lane:.2f},{gap_y:.2f}')
    else:
        source_path += f' {lane:.2f},{row_y[n]:.2f}'
    svg.append(f'<polyline points="{source_path} {lane:.2f},{target_y:.2f} '
               f'{x0:.2f},{target_y:.2f} {x0:.2f},{y0:.2f}" '
               f'fill="none" stroke="{color}" stroke-width=".75" stroke-linejoin="round"/>')
    for box in boxes:
        a, b, c, d = display_box(box)
        svg.append(f'<rect x="{a:.2f}" y="{b:.2f}" width="{c-a:.2f}" height="{d-b:.2f}" '
                   f'fill="none" stroke="{color}" stroke-width=".9">'
                   f'<title>{n:02d}: {safe(evidence[n][0])}</title></rect>')

# Manual positions keep badges away from the original text. Coordinates are PDF points.
badge_positions = {
    1: (122, 71), 2: (124, 83), 3: (156, 90), 4: (112, 109),
    5: (239, 121), 6: (101, 121), 7: (149, 121),
    10: (351, 144), 11: (401, 144), 13: (382, 164), 14: (498, 164),
    17: (335, 234), 18: (389, 234), 30: (277, 355), 32: (504, 282),
    35: (230, 541), 36: (202, 564), 37: (221, 564),
    38: (171, 309), 39: (184, 320), 40: (201, 320),
    45: (113, 306), 81: (220, 287), 88: (83, 187),
}
additional_badges = [(38, 170, 280), (39, 239, 281), (40, 170, 288),
                     (81, 222, 321), (81, 184, 563)]
for n, bx, by in [(n, *pos) for n, pos in badge_positions.items()] + additional_badges:
    color = group(n)[2]
    x, y = position(bx, by)
    svg.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="13.5" height="9.4" rx="1.5" '
               f'fill="{color}" stroke="#fff" stroke-width=".4"/>')
    svg.append(text(x + 6.75, y + 7.4, f"{n:02d}", 8, ink(color), True, "middle"))

for type_id, _, _, items in excess:
    for name, value, box in items:
        a, b, c, d = display_box(box)
        svg.append(f'<rect x="{a:.2f}" y="{b:.2f}" width="{c-a:.2f}" height="{d-b:.2f}" '
                   f'fill="none" stroke="#d62728" stroke-width=".75">'
                   f'<title>{safe(type_id)}: {safe(name)} {safe(value)}</title></rect>')
for type_id, bx, by in [
    ("E1", 239, 109), ("E1", 453, 109), ("E1", 474, 121),
    ("E2", 190, 121), ("E3", 334, 121), ("E4", 505, 121), ("E5", 280, 201),
]:
    x, y = position(bx, by)
    svg.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="15" height="9" rx="1.5" '
               'fill="#d62728" stroke="#fff" stroke-width=".4"/>')
    svg.append(text(x + 7.5, y + 7.1, type_id, 8, "#fff", True, "middle"))
for name, value, box in provenance:
    a, b, c, d = display_box(box)
    svg.append(f'<rect x="{a:.2f}" y="{b:.2f}" width="{c-a:.2f}" height="{d-b:.2f}" '
               f'fill="none" stroke="#111" stroke-width="1" stroke-dasharray=".1 1.6" '
               f'stroke-linecap="round"><title>{safe(name)}: {safe(value)}</title></rect>')
a, b, c, d = display_box(na_evidence["bbox_pt"])
svg.append(f'<rect x="{a:.2f}" y="{b:.2f}" width="{c-a:.2f}" height="{d-b:.2f}" '
           'fill="none" stroke="#6b6b6b" stroke-width=".8" stroke-dasharray="2 1.4"/>')
svg.append(text(a, b - 2, "90 N/A", 8, "#6b6b6b", True))

# U01's key sits beneath the checklist; score and item lists sit below the image.
key_y = Y0 + (len(md) + 1) * PITCH + 12
svg.append(text(48, key_y, "Key: MET, by requirement group", 9.3, "#111", True))
key_y += 11
for _, title, color in groups:
    svg.append(f'<rect x="48" y="{key_y-7:.2f}" width="16" height="9" rx="4.5" fill="{color}"/>')
    svg.append(text(69, key_y, title, 8.2))
    key_y += 10
for line in [
    "Grey pill: MISSING; no connector",
    "Coloured frame + badge: answer",
    "Red frame: Excess data, not scored",
    "Dashed grey: point 90 not applicable",
    "Dotted black: document provenance",
]:
    svg.append(text(48, key_y, line, 8.2))
    key_y += 10

sy = IY + IH + 16
svg.append(text(IX, sy, "Completeness score (Equation 1)", 9.3, "#111", True))
sy += 13
svg.append(text(IX, sy, "Completeness = points marked MET ÷ applicable points", 8.7, "#111", True))
sy += 11
for line in [
    f"(a), (d) MET: {ad_met} of 78 (MD/non-depth {ad_met} of 52; TVD 0 of 26)",
    f"(b), (c) MET: {bc_met} of 11 applicable (90 N/A: one borehole)",
    f"Total MET: {ad_met} + {bc_met} = {len(met)}; applicable: 78 + 11 = {applicable}",
]:
    svg.append(text(IX + 8, sy, line, 8.4))
    sy += 10.4
svg.append(text(IX + 8, sy + 1, f"Completeness(U02) = {len(met)} ÷ {applicable} = "
                f"{len(met)/applicable:.3f} → {score:.1f}%", 9.5, "#111", True))
sy += 16
for line in [
    "MD vs TVD. U02 reports measured depth; no separate",
    "true vertical depths are stated. The deviated label answers",
    "inclination only; it does not supply the wellbore path.",
    "Source: U02.pdf; checklist v4.2. Frames use scan coordinates.",
]:
    svg.append(text(IX, sy, line, 8.2, "#444"))
    sy += 10.4

ex = 520
ey = IY + IH + 16
svg.append(text(ex, ey, "Excess data found in U02", 9.3, "#111", True))
ey += 11
svg.append(text(ex, ey, "(present, not required; not scored)", 8.2))
ey += 12
for type_id, title, _, items in excess:
    svg.append(f'<rect x="{ex}" y="{ey-7:.2f}" width="15" height="9" rx="1.5" fill="#d62728"/>')
    svg.append(text(ex + 7.5, ey, type_id, 7.8, "#fff", True, "middle"))
    svg.append(text(ex + 20, ey, title, 8.2))
    svg.append(text(768, ey, f"×{len(items)}", 8.2, "#111", anchor="end"))
    ey += 10.4
svg.append(text(ex, ey + 2, f"{reference['excess_total']['instances']} instances in "
                f"{len(excess)} types", 8.4, "#111", True))
ey += 18
svg.append(text(ex, ey, "Document provenance (not required; not scored)", 8.4, "#111", True))
for name, value, _ in provenance:
    ey += 10.4
    svg.append(text(ex, ey, f"{name}: {value}", 8.2))
assert max(key_y, sy, ey) < 1008, (key_y, sy, ey)
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
pdf_bytes = svg_doc.convert_to_pdf()
out_pdf = pymupdf.open(stream=pdf_bytes, filetype="pdf")
out_pdf.save(PDF)
out_pdf.close()
JSON.write_text(json.dumps(reference, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"U02: {len(met)}/{applicable} = {score:.1f}%")
print(f"(a)/(d): {ad_met}/78; (b)/(c): {bc_met}/11; excess: {reference['excess_total']}")
print(f"Outputs: {SVG}, {PNG}, {PDF}, {JSON}")
