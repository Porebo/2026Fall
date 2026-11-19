"""Build checklist reference records and annotated figures from reviewed evidence."""

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
DIAGRAMS = ROOT.joinpath("06-study", "sample-uic", "diagrams")
FIGURES = ROOT.joinpath("06-study", "design", "figures")
REFERENCES = ROOT.joinpath("06-study", "sample-uic", "reference")
CHECKLIST = ROOT.joinpath(
    "06-study", "design", "prompts", "casing-diagram-atomic-checklist-v4.2.txt"
)
SCREENING = ROOT.joinpath("06-study", "sample-uic", "screening-log.csv")

POINTS = []
for line in CHECKLIST.read_text(encoding="utf-8").splitlines():
    match = re.fullmatch(r"(\d\d) \| (\S+) \| (.+)", line.strip())
    if match:
        POINTS.append((int(match[1]), match[2], match[3]))
assert [item[0] for item in POINTS] == list(range(1, 91))

GROUPS = [
    ((1, 1), "(a)(1) Well identification", "#0072B2"),
    ((2, 4), "(a)(2)–(4) Spud, elevations", "#E69F00"),
    ((5, 6), "(a)(5)–(6) Water bases", "#007F82"),
    ((7, 8), "(a)(7)–(8) Casing and shoe", "#009E73"),
    ((9, 9), "(a)(9) Perforations", "#CC79A7"),
    ((10, 11), "(a)(10)–(11) Equipment; hole", "#8C564B"),
    ((12, 14), "(a)(12)–(14) Cement; fluid", "#332288"),
    ((15, 15), "(a)(15) Formations, zones", "#999933"),
    ((79, 90), "(b)–(c) Cement, wellbore path", "#56B4E9"),
]

SHORT_LABELS = {
    "Other equipment in the well (e.g., tubing, pumps, rods)": "Other equipment in the well",
    "Cement-yield calculation steps": "Cement-yield calc. steps",
    "Cement job identification (date or stage)": "Cement job identification",
    "Slurry volume (or sacks) for each cement job": "Slurry volume (or sacks)",
    "Slurry density for each cement job": "Slurry density",
    "Slurry yield for each cement job": "Slurry yield",
    "Cement type for each cement job": "Cement type",
    "Cement additives for each cement job": "Cement additives",
    "Wellbore path: measured depth (MD)": "Wellbore path: MD",
    "Borehole designation (original hole, redrill, or sidetrack; conditional: multiple boreholes only)": "Borehole designation",
}


def group(number):
    if number >= 79:
        return GROUPS[-1]
    code = POINTS[number - 1][1]
    match = re.match(r"\(a\)\((\d+)\)", code)
    if not match:
        raise ValueError(f"No subdivision (a) group for point {number}: {code}")
    section = int(match[1])
    return next(item for item in GROUPS[:-1] if item[0][0] <= section <= item[0][1])


def ink(color):
    rgb = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    rgb = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in rgb]
    luminance = .2126 * rgb[0] + .7152 * rgb[1] + .0722 * rgb[2]
    return "#111" if (luminance + .05) / .055 >= 4.5 else "#fff"


def loc(page, *box):
    if len(box) != 4:
        raise ValueError("A location must have four PDF coordinates")
    return {"page": page, "bbox_pt": [round(float(value), 2) for value in box]}


def safe(value):
    return html.escape(str(value), quote=True)


def text(x, y, value, size=8.7, color="#333", bold=False, anchor="start"):
    weight = ' font-weight="bold"' if bold else ""
    return (f'<text font-family="Helvetica, Arial, sans-serif" x="{x:.2f}" y="{y:.2f}" '
            f'font-size="{size}" fill="{color}"{weight} text-anchor="{anchor}">'
            f'{safe(value)}</text>')


def text_width(value, size=8.7, bold=False):
    return pymupdf.get_text_length(value, fontname="hebo" if bold else "helv", fontsize=size)


def intersection_area(a, b):
    return max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(
        0, min(a[3], b[3]) - max(a[1], b[1])
    )


class Diagram:
    def __init__(self, number, operator, *, printed_date=None):
        if not re.fullmatch(r"U(?:0[1-9]|[12]\d|30)", number):
            raise ValueError(f"Not a U01–U30 study diagram: {number}")
        self.number = number
        self.operator = operator
        self.printed_date = printed_date
        self.source = DIAGRAMS / f"{number}.pdf"
        self.doc = pymupdf.open(self.source)
        with SCREENING.open(encoding="utf-8", newline="") as stream:
            matches = [row for row in csv.DictReader(stream) if row["SampleCode"] == number]
        if len(matches) != 1:
            raise ValueError(f"{number}: expected one screening-log entry, found {len(matches)}")
        self.screening = matches[0]
        digest = hashlib.sha256(self.source.read_bytes()).hexdigest().upper()
        if digest != self.screening["SHA256"].upper():
            raise ValueError(f"{number}: source hash differs from screening log")
        self.evidence = {}
        self.notes = []
        self.excess = []
        self.provenance = []
        self.supporting = []
        self.na = None
        self.multiple_boreholes = False
        self.panels = []
        self.badge_size = None
        self.row_aligned_badges = False

    def find(self, phrase, page=1, occurrence=None):
        matches = self.doc[page - 1].search_for(phrase)
        if occurrence is None:
            if len(matches) != 1:
                raise ValueError(
                    f"{self.number}: {phrase!r} has {len(matches)} matches on page {page}"
                )
            occurrence = 0
        if occurrence < 0 or occurrence >= len(matches):
            raise ValueError(f"{self.number}: no match {occurrence} for {phrase!r} on page {page}")
        return loc(page, *matches[occurrence])

    def add(self, number, answer, *locations):
        if number in self.evidence or not 1 <= number <= 90:
            raise ValueError(f"{self.number}: invalid or duplicate point {number}")
        if not answer or not locations:
            raise ValueError(f"{self.number}: MET point {number} requires text and a location")
        self.evidence[number] = (answer, list(locations))

    def uncertain(self, numbers, reason):
        if not numbers or not reason or not all(1 <= n <= 90 for n in numbers):
            raise ValueError(f"{self.number}: invalid uncertainty")
        self.notes.append({"points": list(numbers), "reason": reason})

    def add_excess(self, label, entries):
        if not entries:
            raise ValueError(f"{self.number}: empty excess-data group {label}")
        type_id = f"E{len(self.excess) + 1}"
        instances = []
        for item, value, location, reason in entries:
            if not all((item, value, reason)):
                raise ValueError(f"{self.number}: incomplete {type_id} entry")
            instances.append({"item": item, "text": value, "reason": reason, **location})
        self.excess.append({"type": type_id, "label": label, "count": len(instances),
                            "instances": instances})

    def add_provenance(self, item, value, location):
        if not item or not value:
            raise ValueError(f"{self.number}: incomplete provenance item")
        self.provenance.append({"item": item, "text": value, **location})

    def single_borehole(self, description, location):
        if self.na is not None or self.multiple_boreholes or 90 in self.evidence:
            raise ValueError(f"{self.number}: borehole status already set")
        self.na = {"point": 90, "item": description, "text": description, **location}

    def applicable_boreholes(self):
        if self.na is not None:
            raise ValueError(f"{self.number}: borehole status already set")
        self.multiple_boreholes = True

    def page_panel(self, page, crop, *, inset=False, layout=None, label=None):
        if not 1 <= page <= len(self.doc):
            raise ValueError(f"{self.number}: invalid page {page}")
        rect = pymupdf.Rect(crop)
        if rect.is_empty or not self.doc[page - 1].rect.contains(rect):
            raise ValueError(f"{self.number}: invalid page crop {crop}")
        if layout is not None and (len(layout) != 4 or
                                   layout[0] < 230 or layout[1] < 90 or
                                   layout[0] + layout[2] > 768 or
                                   layout[1] + layout[3] > 785 or
                                   layout[2] <= 0 or layout[3] <= 0):
            raise ValueError(f"{self.number}: invalid panel layout {layout}")
        self.panels.append({"page": page, "clip": rect, "inset": inset,
                            "layout": layout, "label": label})

    def validate_location(self, location):
        page = location["page"]
        if not 1 <= page <= len(self.doc):
            raise ValueError(f"{self.number}: invalid evidence page {page}")
        box = pymupdf.Rect(location["bbox_pt"])
        if box.is_empty or not self.doc[page - 1].rect.contains(box):
            raise ValueError(f"{self.number}: invalid evidence box {location}")
        if not any(panel["page"] == page and panel["clip"].contains(box) for panel in self.panels):
            raise ValueError(f"{self.number}: evidence not shown in a figure panel: {location}")

    def make_reference(self):
        if not self.panels:
            raise ValueError(f"{self.number}: no source page panels")
        if self.na is None and not self.multiple_boreholes:
            raise ValueError(f"{self.number}: explicitly decide whether point 90 applies")
        for _, locations in self.evidence.values():
            for location in locations:
                self.validate_location(location)
        for entry in self.excess:
            for item in entry["instances"]:
                self.validate_location(item)
        for item in self.provenance + self.supporting:
            self.validate_location(item)
        if self.na:
            self.validate_location(self.na)

        na = {90} if self.na else set()
        met = set(self.evidence)
        applicable = 90 - len(na)
        ad_met = sum(number in met for number in range(1, 79))
        ad_md = sum(number in met for number in range(1, 53))
        ad_tvd = sum(number in met for number in range(53, 79))
        bc_met = sum(number in met for number in range(79, 91))
        bc_applicable = 12 - len(na)
        records = []
        for number, code, name in POINTS:
            answer, locations = self.evidence.get(number, (None, []))
            record = {
                "number": number, "code": code, "label": name,
                "status": "MET" if number in met else "NOT_APPLICABLE" if number in na else "MISSING",
                "displayed_answer": answer, "locations": locations,
            }
            notes = [item["reason"] for item in self.notes if number in item["points"]]
            if notes:
                record["note"] = " ".join(notes)
            records.append(record)

        row = self.screening
        well = {
            "well_name": f"{row['LeaseName']} {row['WellNumber']}",
            "lease_name": row["LeaseName"], "well_number": row["WellNumber"], "api": row["API10"],
            "operator": self.operator, "field": row["FieldName"], "county": row["County"],
            "district": row["District"], "well_type": f"{row['WellTypeCode']} {row['WellTypeLabel']}",
            "well_status": row["WellStatus"], "uic_project": row["UIC_Project"],
            "wellstar_document_id": row["DocumentID"],
            "wellstar_document_date": row["DocumentRelevantDate"],
            "wellstar_file_name": row["WellSTAR_FileName"], "sha256": row["SHA256"],
        }
        if self.printed_date:
            well["diagram_printed_date"] = self.printed_date
        return {
            "diagram_id": self.number,
            "source_pdf": f"06-study/sample-uic/diagrams/{self.number}.pdf",
            "page_scored": 1 if len(self.doc) == 1 else f"1-{len(self.doc)}",
            "well": well, "checklist_version": "v4.2",
            "reviewer": "Lester S. Carcamo", "review_date": "2026-11-18",
            "score": {
                "met": len(met), "applicable": applicable, "not_applicable": len(na),
                "missing": applicable - len(met), "percent": round(100 * len(met) / applicable, 1),
                "subdivisions_a_d": {
                    "met": ad_met, "of": 78, "md_non_depth_met": ad_md,
                    "md_non_depth_of": 52, "tvd_met": ad_tvd, "tvd_of": 26,
                },
                "subdivisions_b_c": {"met": bc_met, "applicable": bc_applicable},
            },
            "points": records, "excess_data": self.excess, "provenance": self.provenance,
            "supporting_another_requirement": self.supporting,
            "not_applicable_evidence": [self.na] if self.na else [],
            "excess_total": {"instances": sum(item["count"] for item in self.excess),
                             "types": len(self.excess)},
            "uncertain_calls": self.notes,
        }

    def build(self):
        reference = self.make_reference()
        svg = make_figure(self, reference)
        preview = os.environ.get("U_ATOMIC_PREVIEW_DIR")
        if preview:
            directory = Path(preview)
            svg_path = directory / f"{self.number}.svg"
            png_path = directory / f"{self.number}.png"
            pdf_path = directory / f"{self.number}-atomic-map.pdf"
            json_path = directory / f"{self.number}.json"
        else:
            svg_path = DIAGRAMS / f"{self.number}.svg"
            png_path = DIAGRAMS / f"{self.number}.png"
            pdf_path = FIGURES / f"{self.number}-atomic-map.pdf"
            json_path = REFERENCES / f"{self.number}.json"
        for path in (svg_path, pdf_path, json_path):
            path.parent.mkdir(parents=True, exist_ok=True)
        svg_path.write_text(svg, encoding="utf-8")
        svg_doc = pymupdf.open(stream=svg.encode("utf-8"), filetype="svg")
        page = svg_doc[0]
        page.get_pixmap(matrix=pymupdf.Matrix(1632 / page.rect.width, 2112 / page.rect.height),
                        alpha=False).save(png_path)
        pdf = pymupdf.open(stream=svg_doc.convert_to_pdf(), filetype="pdf")
        pdf.save(pdf_path)
        pdf.close()
        svg_doc.close()
        json_path.write_text(json.dumps(reference, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        score = reference["score"]
        print(f"{self.number}: {score['met']}/{score['applicable']} = {score['percent']:.1f}%; "
              f"(a)/(d) {score['subdivisions_a_d']['met']}/78; "
              f"(b)/(c) {score['subdivisions_b_c']['met']}/{score['subdivisions_b_c']['applicable']}; "
              f"excess {reference['excess_total']}")
        print(f"Outputs: {svg_path}, {png_path}, {pdf_path}, {json_path}")
        return reference


def make_figure(case, reference):
    panels = case.panels
    custom_layout = all(panel["layout"] is not None for panel in panels)
    if custom_layout:
        layouts = [panel["layout"] for panel in panels]
    elif any(panel["layout"] is not None for panel in panels):
        raise ValueError(f"{case.number}: every custom source panel needs a layout")
    elif len(panels) == 1 and not panels[0]["inset"]:
        layouts = [(230.0, 90.0, 538.0, 695.0)]
    elif len(panels) == 2 and not panels[0]["inset"] and panels[1]["inset"]:
        first = panels[0]["clip"]
        first_scale = min(538 / first.width, 695 / first.height)
        footer = max(765, 90 + first.height * first_scale + 16)
        inset_y = footer + 38 + 9.5 * len(case.excess)
        if inset_y >= 1000:
            raise ValueError(f"{case.number}: no space for the source-page inset")
        layouts = [(230.0, 90.0, 538.0, 695.0),
                   (520.0, inset_y, 248.0, 1006 - inset_y)]
    elif len(panels) == 2 and not any(panel["inset"] for panel in panels):
        layouts = [(230.0, 102.0, 265.0, 680.0), (503.0, 102.0, 265.0, 680.0)]
    else:
        raise ValueError(f"{case.number}: figure supports one or two source panels")

    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        'width="8.5in" height="11in" viewBox="0 0 816 1056">',
        f"<title>{safe(case.number)} atomic data-point map</title>",
        '<rect width="816" height="1056" fill="#fff"/>',
    ]
    score = reference["score"]
    svg.append(text(48, 65, f"Casing Diagram {case.number} · Checklist v4.2 · "
                    f"Final score {score['percent']:.1f}% ({score['met']} of "
                    f"{score['applicable']} applicable points MET)", 14.7, "#111", True))
    svg.append(text(48, 79, "Scored by Lester S. Carcamo · November 18, 2026", 9.3, "#444"))
    svg.append(text(51, 98, "MD / non-depth", 8.7, "#333", True))
    svg.append(text(190, 98, "TVD", 8.7, "#333", True, "middle"))
    words = []
    image_bottom = 0
    for panel, (x, y, max_width, max_height) in zip(panels, layouts):
        clip = panel["clip"]
        scale = min(max_width / clip.width, max_height / clip.height)
        width, height = clip.width * scale, clip.height * scale
        panel.update({"x": x, "y": y, "width": width, "height": height, "scale": scale})
        page = case.doc[panel["page"] - 1]
        pix = page.get_pixmap(dpi=220, clip=clip, alpha=False)
        encoded = base64.b64encode(pix.tobytes("png")).decode("ascii")
        if panel["label"]:
            svg.append(text(x, y - 5, panel["label"], 8.3, "#333", True))
        elif not custom_layout and len(panels) > 1 and (
                panel["inset"] or not any(p["inset"] for p in panels)):
            suffix = " detail" if panel["inset"] else ""
            svg.append(text(x, y - 5, f"Source page {panel['page']}{suffix}", 8.3, "#333", True))
        svg.append(f'<image x="{x:.2f}" y="{y:.2f}" width="{width:.2f}" height="{height:.2f}" '
                   f'preserveAspectRatio="none" xlink:href="data:image/png;base64,{encoded}"/>')
        svg.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{width:.2f}" height="{height:.2f}" '
                   'fill="none" stroke="#bbb" stroke-width=".5"/>')
        for word in page.get_text("words", clip=clip):
            words.append((x + (word[0] - clip.x0) * scale, y + (word[1] - clip.y0) * scale,
                          x + (word[2] - clip.x0) * scale, y + (word[3] - clip.y0) * scale))
        if not panel["inset"]:
            image_bottom = max(image_bottom, y + height)

    def display_box(location):
        box = pymupdf.Rect(location["bbox_pt"])
        panel = next(p for p in panels
                     if p["page"] == location["page"] and p["clip"].contains(box))
        clip, scale = panel["clip"], panel["scale"]
        return (panel["x"] + (box.x0 - clip.x0) * scale,
                panel["y"] + (box.y0 - clip.y0) * scale,
                panel["x"] + (box.x1 - clip.x0) * scale,
                panel["y"] + (box.y1 - clip.y0) * scale)

    status = {item["number"]: item["status"] for item in reference["points"]}
    md = [item for item in POINTS if not item[1].endswith(".tvd")]
    tvd = {item[1][:-4]: item for item in POINTS if item[1].endswith(".tvd")}
    if len(md) != 64 or len(tvd) != 26:
        raise ValueError("Unexpected checklist point layout")
    x1, w1, x2, w2, y0, pitch, ph = 48, 130, 181, 18, 102, 10, 9
    row_y = {}

    def pill(number, name, x, y, width, compact=False):
        state = status[number]
        color = group(number)[2] if state == "MET" else "#6b6b6b" if state == "NOT_APPLICABLE" else "#cfcfcf"
        fill = color if state == "MET" else "#fff" if state == "NOT_APPLICABLE" else "#f0f0f0"
        foreground = ink(color) if state == "MET" else "#666" if state == "NOT_APPLICABLE" else "#999"
        dash = ' stroke-dasharray="2.2 1.4"' if state == "NOT_APPLICABLE" else ""
        svg.append(f'<rect x="{x}" y="{y}" width="{width}" height="{ph}" rx="4.5" '
                   f'fill="{fill}" stroke="{color}" stroke-width=".6"{dash}/>')
        if not compact and state == "MET":
            svg.append(f'<rect x="{x+1}" y="{y+1}" width="12" height="7" rx="3.5" fill="#fff"/>')
        svg.append(text(x + (width / 2 if compact else 7), y + 7.3, f"{number:02d}", 8.1,
                        foreground if compact or state != "MET" else color, not compact, "middle"))
        if not compact:
            label = SHORT_LABELS.get(name, name).replace(" (MD)", "")
            if number == 90 and state == "NOT_APPLICABLE":
                label += ": N/A"
            if text_width(label, 8.7) > width - 18:
                raise ValueError(f"Checklist label too wide: {number} {label}")
            svg.append(text(x + 17, y + 7.4, label, 8.7, foreground))
        row_y[number] = y + ph / 2

    for index, (number, code, name) in enumerate(md):
        y = y0 + (index + (number >= 79)) * pitch
        if number == 79:
            svg.append(text(50, y - 2, "§ 1724.7.1(b)–(c) (no TVD pair)", 8.7, "#333", True))
        pill(number, name, x1, y, w1)
        if code.endswith(".md"):
            paired = tvd[code[:-3]]
            pill(paired[0], paired[2], x2, y, w2, compact=True)

    frames = []
    for number, (_, locations) in case.evidence.items():
        for location in locations:
            frames.append((number, display_box(location)))
    evidence_rects = [box for _, box in frames]
    lane_step = min(.85, 23 / max(len(case.evidence) - 1, 1))
    for index, number in enumerate(sorted(case.evidence)):
        locations = case.evidence[number][1]
        first = display_box(locations[0])
        lane = 201 + index * lane_step
        start = x2 + w2 if 53 <= number <= 78 else x1 + w1
        source_path = f'{start},{row_y[number]:.2f}'
        if POINTS[number - 1][1].endswith(".md"):
            gutter_x = x1 + w1 + 1.5
            gap_y = row_y[number] - 5
            source_path += (f' {gutter_x:.2f},{row_y[number]:.2f} '
                            f'{gutter_x:.2f},{gap_y:.2f} {lane:.2f},{gap_y:.2f}')
        else:
            source_path += f' {lane:.2f},{row_y[number]:.2f}'
        target_y = first[1] - 1
        color = group(number)[2]
        target_panel = next(p for p in panels if p["page"] == locations[0]["page"]
                            and p["clip"].contains(pymupdf.Rect(locations[0]["bbox_pt"])))
        if custom_layout and target_panel["x"] >= 485:
            route_y = image_bottom + 5 + index * min(
                1, max(0, 755 - image_bottom - 5) / max(len(case.evidence) - 1, 1))
            route_x = 479 + index * 4 / max(len(case.evidence) - 1, 1)
            path = (f'{source_path} {lane:.2f},{route_y:.2f} {route_x:.2f},{route_y:.2f} '
                    f'{route_x:.2f},{target_y:.2f} {first[0]:.2f},{target_y:.2f}')
        else:
            path = (f'{source_path} {lane:.2f},{target_y:.2f} '
                    f'{first[0]:.2f},{target_y:.2f}')
        svg.append(f'<polyline points="{path}" fill="none" stroke="{color}" '
                   'stroke-width=".7" stroke-linejoin="round"/>')
        for location in locations[1:]:
            box = pymupdf.Rect(location["bbox_pt"])
            panel = next(p for p in panels
                         if p["page"] == location["page"] and p["clip"].contains(box))
            if panel["inset"]:
                target = display_box(location)
                svg.append(f'<polyline points="{source_path} {lane:.2f},{image_bottom+4:.2f} '
                           f'513,{image_bottom+4:.2f} 513,{target[1]-1:.2f} '
                           f'{target[0]:.2f},{target[1]-1:.2f}" fill="none" '
                           f'stroke="{color}" stroke-width=".7" stroke-linejoin="round"/>')
    seen_boxes = {}
    seen_frames = set()
    for number, (a, b, c, d) in frames:
        box_key = tuple(round(v, 1) for v in (a, b, c, d))
        color = group(number)[2]
        frame_key = (box_key, color)
        if frame_key in seen_frames:
            continue
        seen_frames.add(frame_key)
        pad = .55 * seen_boxes.get(box_key, 0)
        seen_boxes[box_key] = seen_boxes.get(box_key, 0) + 1
        svg.append(f'<rect x="{a-pad:.2f}" y="{b-pad:.2f}" width="{c-a+2*pad:.2f}" '
                   f'height="{d-b+2*pad:.2f}" fill="none" stroke="{color}" stroke-width=".9">'
                   f'<title>{number:02d}: {safe(case.evidence[number][0])}</title></rect>')

    badges = []

    def badge(number, frame, color):
        a, b, c, d = frame
        bw, bh = case.badge_size or (13.0, 8.4)
        candidates = [
            (c + 1, b - bh), (a - bw - 1, b - bh), (a, b - bh - 1),
            (c + 1, d + 1), (a - bw - 1, d + 1), (a, d + 1),
            (c + 1, b), (a - bw - 1, b), (c - bw, b - bh - 1),
        ]
        if case.row_aligned_badges:
            candidates = [(c + 1, b), (a - bw - 1, b)] + candidates
        if case.badge_size:
            if custom_layout and a >= 485:
                candidates = [(700 + offset * (bw + 1), b) for offset in range(7)] + candidates
            for offset in range(8):
                candidates.extend(((c + 1 + offset * (bw + 1), b),
                                   (a - (offset + 1) * (bw + 1), b)))
        best = None
        for x, y in candidates:
            box = (x, y, x + bw, y + bh)
            if x < 225 or x + bw > 768 or y < 90 or y + bh > 1006:
                continue
            penalty = (100 if case.badge_size else 1) * sum(
                intersection_area(box, w) for w in words)
            penalty += (500 if case.badge_size else 5) * sum(
                intersection_area(box, old) for old in badges)
            penalty += (10 if case.badge_size else 2) * sum(
                intersection_area(box, old) for old in evidence_rects)
            if case.badge_size:
                penalty += .03 * max(x - c, a - x - bw, 0)
            row_offset = abs(y - b) if case.row_aligned_badges else 0
            candidate = (penalty, row_offset, x, y)
            if best is None or candidate < best:
                best = candidate
        if best is None:
            raise ValueError(f"{case.number}: cannot place badge {number} at {frame}")
        _, _, x, y = best
        badges.append((x, y, x + bw, y + bh))
        svg.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{bw}" height="{bh}" rx="1.2" '
                   f'fill="{color}" stroke="#fff" stroke-width=".4"/>')
        label = f"{number:02d}" if isinstance(number, int) else number
        svg.append(text(x + bw / 2, y + bh * .8, label,
                        5.4 if case.badge_size else 7.1, ink(color), True, "middle"))

    for number, frame in frames:
        badge(number, frame, group(number)[2])

    for entry in case.excess:
        for item in entry["instances"]:
            a, b, c, d = display_box(item)
            svg.append(f'<rect x="{a:.2f}" y="{b:.2f}" width="{c-a:.2f}" height="{d-b:.2f}" '
                       f'fill="none" stroke="#d62728" stroke-width=".75">'
                       f'<title>{safe(entry["type"])}: {safe(item["item"])} '
                       f'{safe(item["text"])}</title></rect>')
        a, b, c, d = display_box(entry["instances"][0])
        if case.badge_size:
            badge(entry["type"], (a, b, c, d), "#d62728")
        else:
            x, y = min(c + 1, 752), max(90, b - 8.5)
            svg.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="15" height="9" rx="1.2" '
                       'fill="#d62728" stroke="#fff" stroke-width=".4"/>')
            svg.append(text(x + 7.5, y + 7.0, entry["type"], 7.1, "#fff", True, "middle"))
    for item in case.provenance:
        a, b, c, d = display_box(item)
        svg.append(f'<rect x="{a:.2f}" y="{b:.2f}" width="{c-a:.2f}" height="{d-b:.2f}" '
                   'fill="none" stroke="#111" stroke-width=".9" stroke-dasharray=".1 1.6" '
                   'stroke-linecap="round"/>')
    if case.na:
        a, b, c, d = display_box(case.na)
        svg.append(f'<rect x="{a:.2f}" y="{b:.2f}" width="{c-a:.2f}" height="{d-b:.2f}" '
                   'fill="none" stroke="#6b6b6b" stroke-width=".8" stroke-dasharray="2 1.4"/>')
        label_x, label_y = max(230, a - 27), max(90, b - 9)
        svg.append(f'<rect x="{label_x:.2f}" y="{label_y:.2f}" width="27" height="9" rx="1" '
                   'fill="#fff" stroke="#6b6b6b" stroke-width=".6" stroke-dasharray="2 1"/>')
        svg.append(text(label_x + 13.5, label_y + 7, "90 N/A", 7.1, "#555", True, "middle"))

    key_y = y0 + (len(md) + 1) * pitch + 12
    svg.append(text(48, key_y, "Key: MET, by requirement group", 9.0, "#111", True))
    key_y += 11
    for _, title, color in GROUPS:
        if not any(group(number)[1] == title for number in case.evidence):
            continue
        svg.append(f'<rect x="48" y="{key_y-7:.2f}" width="16" height="9" rx="4.5" fill="{color}"/>')
        svg.append(text(69, key_y, title, 8.0))
        key_y += 10
    for line in ["Grey pill: MISSING", "Coloured frame + badge: answer",
                 "Red frame: Excess data, not scored", "Dashed grey: point 90 not applicable",
                 "Dotted black: document provenance"]:
        svg.append(text(48, key_y, line, 7.8))
        key_y += 9.5

    footer_y = max(765, image_bottom + 16)
    sy = footer_y
    svg.append(text(230, sy, "Completeness score (Equation 1)", 9.1, "#111", True))
    sy += 12
    svg.append(text(230, sy, "Completeness = MET ÷ applicable points", 8.1, "#111", True))
    sy += 10
    ad = score["subdivisions_a_d"]
    bc = score["subdivisions_b_c"]
    for line in [
        f"(a), (d): {ad['met']}/78 (MD/non-depth {ad['md_non_depth_met']}/52; TVD {ad['tvd_met']}/26)",
        f"(b), (c): {bc['met']}/{bc['applicable']} applicable",
        f"MET {score['met']}; MISSING {score['missing']}; N/A {score['not_applicable']}",
    ]:
        if text_width(line, 7.8) > 275:
            raise ValueError(f"{case.number}: footer text too wide: {line}")
        svg.append(text(238, sy, line, 7.8))
        sy += 9.3
    svg.append(text(238, sy, f"{case.number}: {score['met']} ÷ {score['applicable']} = "
                    f"{score['met']/score['applicable']:.3f} → {score['percent']:.1f}%",
                    9.0, "#111", True))
    sy += 13
    svg.append(text(230, sy, "MD and TVD are scored as separate points.", 7.7))
    sy += 11
    svg.append(text(230, sy, f"Source: {case.number}.pdf; checklist v4.2.", 7.7))
    sy += 15
    svg.append(text(230, sy, "Document provenance (not required; not scored)", 8.1, "#111", True))
    sy += 10
    for item in case.provenance:
        line = f'{item["item"]}: {item["text"]}'
        if text_width(line, 7.3) > 275:
            line = item["item"]
        svg.append(text(230, sy, line, 7.3))
        sy += 9

    ex_y = footer_y
    svg.append(text(520, ex_y, f"Excess data found in {case.number}", 9.1, "#111", True))
    ex_y += 10
    svg.append(text(520, ex_y, "(present, not required; not scored)", 7.8))
    ex_y += 11
    for item in case.excess:
        if text_width(item["label"], 7.5) > 209:
            raise ValueError(f"{case.number}: excess label too wide: {item['label']}")
        svg.append(f'<rect x="520" y="{ex_y-7:.2f}" width="15" height="9" rx="1.2" fill="#d62728"/>')
        svg.append(text(527.5, ex_y, item["type"], 7.1, "#fff", True, "middle"))
        svg.append(text(539, ex_y, item["label"], 7.5))
        svg.append(text(768, ex_y, f"×{item['count']}", 7.5, "#111", anchor="end"))
        ex_y += 9.5
    total = reference["excess_total"]
    svg.append(text(520, ex_y + 1, f"{total['instances']} instances in {total['types']} types",
                    8.0, "#111", True))
    if max(key_y, sy, ex_y + 5) > 1006:
        raise ValueError(f"{case.number}: figure content exceeds the 0.5-inch bottom margin")
    svg.append("</svg>")
    return "\n".join(svg)
