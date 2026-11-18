import re
import sqlite3
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation


ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "casing_specs.db"
MARKDOWN_PATH = ROOT / "W01-human-review-questions.md"
OUTPUT_PATH = ROOT / "W01-human-review-51point-score.xlsx"

DESTINATIONS = {
    1: "operators.operator_name",
    2: "wells.lease_name",
    3: "wells.well_number",
    4: "wells.api_number",
    5: "wells.spud_date",
    6: "wells.ground_elevation_ft",
    7: "wells.reference_elevation_ft; wells.reference_elevation_type",
    8: "wells.base_freshwater_md_ft",
    9: "wells.base_usdw_md_ft",
    10: "casing_intervals.casing_diameter_in",
    11: "casing_intervals.grade_or_schedule",
    12: "casing_intervals.connection_type",
    13: "casing_intervals.weight_ppf",
    14: "casing_intervals.bottom_md_ft (SHOE)",
    15: "casing_intervals.bottom_md_ft (STUB)",
    16: "casing_intervals.top_md_ft (LINER_TOP)",
    17: "perforation_intervals.top_md_ft; bottom_md_ft",
    18: "perforation_intervals.top_md_ft; bottom_md_ft",
    19: "well_features (OPEN_HOLE_COMPLETION)",
    20: "well_features (WATER_SHUTOFF_HOLE)",
    21: "well_features (CEMENT_PORT)",
    22: "well_features (CAVITY_SHOT)",
    23: "well_features (CUT)",
    24: "well_features.description (CASING_DAMAGE)",
    25: "well_features depths/description (CASING_DAMAGE)",
    26: "well_features.description (JUNK_OR_FISH)",
    27: "well_features depths/description (JUNK_OR_FISH)",
    28: "well_features (OTHER_FLOW_OR_INTEGRITY_FEATURE)",
    29: "well_features (SUBSURFACE_SAFETY_VALVE)",
    30: "well_features (PACKER)",
    31: "well_features (GAS_LIFT_MANDREL)",
    32: "drilled_intervals.hole_diameter_in",
    33: "drilled_intervals.top_md_ft; bottom_md_ft",
    34: "cement_placements (INSIDE_CASING)",
    35: "cement_placements.top_md_ft",
    36: "cement_placements.bottom_md_ft",
    37: "cement_placements (BEHIND_CASING)",
    38: "cement_placements.top_md_ft",
    39: "cement_placements.bottom_md_ft",
    40: "GAP: fluid_type is not implemented",
    41: "GAP: fluid_density and unit are not implemented",
    42: "geological_features.feature_name (FORMATION)",
    43: "geological_features depths (FORMATION)",
    44: "geological_features.feature_name (ZONE)",
    45: "geological_features depths (ZONE)",
    46: "geological_features.feature_name (MARKER)",
    47: "geological_features depths (MARKER)",
    48: "geological_features.top_md_ft (INJECTION_ZONE)",
    49: "geological_features.bottom_md_ft (INJECTION_ZONE)",
    50: "geological_features.top_md_ft (CONFINING_LAYER)",
    51: "geological_features.bottom_md_ft (CONFINING_LAYER)",
    52: "GAP: yield calculation steps are combined",
    53: "GAP: other calculation steps are combined",
    54: "cement_jobs.cement_volume_cf; supporting inputs not structured",
    55: "cement_jobs.density_ppg",
    56: "cement_jobs.yield_cf_per_sack",
    57: "cement_components.component_name; cement_jobs.remarks",
    58: "cement_components.component_name; quantity; unit",
    59: "borehole_surveys.md_ft",
    60: "borehole_surveys.inclination_deg",
    61: "borehole_surveys.azimuth_deg",
}


def load_requirements():
    with sqlite3.connect(DB_PATH) as connection:
        return connection.execute(
            """
            SELECT requirement_id, requirement_code, requirement_name,
                   requirement_text, scope_type, is_conditional
            FROM spec_requirements
            ORDER BY requirement_id
            """
        ).fetchall()


def load_questions():
    markdown = MARKDOWN_PATH.read_text(encoding="utf-8")
    matches = re.findall(
        r"^(\d+)\. \*\*(.+?)\*\*\s*$",
        markdown,
        flags=re.MULTILINE,
    )
    return {int(number): question for number, question in matches}


def style_review_sheet(sheet, row_count):
    navy = "17365D"
    red = "FCE4D6"
    gold = "FFF2CC"
    green = "E2F0D9"
    gray = "E7E6E6"
    input_fill = PatternFill("solid", fgColor="FFFDF2")
    thin = Side(style="thin", color="B7B7B7")

    for cell in sheet[1]:
        cell.fill = PatternFill("solid", fgColor=navy)
        cell.font = Font(color="FFFFFF", bold=True)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = Border(bottom=thin)

    for row in sheet.iter_rows(min_row=2, max_row=row_count):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = Border(bottom=Side(style="hair", color="D9D9D9"))
        for column in range(7, 12):
            row[column - 1].fill = input_fill
        if row[4].value == "Yes":
            row[4].fill = PatternFill("solid", fgColor=gold)
        if str(row[5].value).startswith("GAP:"):
            row[5].fill = PatternFill("solid", fgColor=red)

    validation = DataValidation(
        type="list",
        formula1='"MET,MISSING"',
        allow_blank=True,
    )
    validation.error = "Choose MET or MISSING."
    validation.errorTitle = "Invalid status"
    validation.prompt = "Select the review outcome for this requirement."
    validation.promptTitle = "Requirement status"
    sheet.add_data_validation(validation)
    validation.add(f"G2:G{row_count}")

    for status, color in (
        ("MET", green),
        ("MISSING", red),
    ):
        sheet.conditional_formatting.add(
            f"G2:G{row_count}",
            FormulaRule(
                formula=[f'$G2="{status}"'],
                fill=PatternFill("solid", fgColor=color),
            ),
        )

    widths = [7, 30, 25, 56, 13, 48, 18, 32, 24, 38, 20]
    for index, width in enumerate(widths, 1):
        sheet.column_dimensions[get_column_letter(index)].width = width
    sheet.freeze_panes = "D2"
    sheet.auto_filter.ref = f"A1:K{row_count}"
    sheet.sheet_view.showGridLines = False
    sheet.row_dimensions[1].height = 34
    for row_index in range(2, row_count + 1):
        sheet.row_dimensions[row_index].height = 52


def build_workbook():
    questions = load_questions()
    requirements = load_requirements()
    expected_ids = set(range(1, 62))
    if set(questions) != expected_ids:
        raise RuntimeError("The Markdown questions are not numbered exactly 1 through 61.")
    if {row[0] for row in requirements} != expected_ids:
        raise RuntimeError("The database requirements are not numbered exactly 1 through 61.")

    workbook = Workbook()
    review = workbook.active
    review.title = "Review W01"
    summary = workbook.create_sheet("Summary")
    instructions = workbook.create_sheet("Instructions")

    review.append(
        [
            "No.",
            "Spec Code",
            "Requirement",
            "Human Question",
            "Conditional?",
            "Database Destination",
            "Status",
            "Answer / Value Seen",
            "Diagram Location",
            "Evidence / Notes",
            "MD / TVD Note",
        ]
    )
    for row_id, code, name, _, _, conditional in requirements:
        review.append(
            [
                row_id,
                code,
                name,
                questions[row_id],
                "Yes" if conditional else "No",
                DESTINATIONS[row_id],
                "",
                "",
                "",
                "",
                "",
            ]
        )
    style_review_sheet(review, 62)

    summary.sheet_view.showGridLines = False
    summary["A1"] = "W01 HUMAN REVIEW SUMMARY"
    summary["A1"].font = Font(size=18, bold=True, color="FFFFFF")
    summary["A1"].fill = PatternFill("solid", fgColor="17365D")
    summary.merge_cells("A1:B1")
    summary.append([])
    summary.append(["Metric", "Value"])
    for cell in summary[3]:
        cell.fill = PatternFill("solid", fgColor="1F6D78")
        cell.font = Font(color="FFFFFF", bold=True)
    summary_rows = [
        ("Stored specification requirements", "=COUNTA('Review W01'!A2:A62)"),
        ("Diagram-scoring requirements", "=COUNTA('Review W01'!A2:A52)"),
        ("Scoring rows completed", "=COUNTA('Review W01'!G2:G52)"),
        ("MET", '=COUNTIF(\'Review W01\'!G2:G52,"MET")'),
        ("MISSING", '=COUNTIF(\'Review W01\'!G2:G52,"MISSING")'),
        ("Scoring denominator", "=B5"),
        ("Completeness %", "=IFERROR(B7/(B7+B8),0)"),
    ]
    for label, formula in summary_rows:
        summary.append([label, formula])
    summary["B10"].number_format = "0.0%"
    summary.column_dimensions["A"].width = 30
    summary.column_dimensions["B"].width = 20
    summary.freeze_panes = "A3"

    instruction_lines = [
        ("W01 HUMAN REVIEW WORKBOOK", "17365D"),
        ("Purpose", "1F6D78"),
        ("Open this workbook beside W01.pdf. Answer one row for each of the 61 atomic specification requirements.", None),
        ("Recommended workflow", "1F6D78"),
        ("1. Read the Human Question.", None),
        ("2. Select MET or MISSING in Status.", None),
        ("3. Copy the exact value seen into Answer / Value Seen.", None),
        ("4. Record where it appears on the diagram.", None),
        ("5. Add optional notes in Evidence / Notes without changing the presence decision.", None),
        ("6. For repeated items, list every casing, interval, job, marker, or feature on separate lines.", None),
        ("Status meanings", "1F6D78"),
        ("MET — an answer is supplied, including N/A, none, or an unusual value.", None),
        ("MISSING — no answer is supplied.", None),
        ("Make only a presence decision, not a truth, quality, or plausibility judgment.", None),
        ("Database readiness", "1F6D78"),
        ("A Database Destination beginning GAP exposes a schema field that must still be added or separated.", None),
        ("Use MD / TVD Note to identify whether both depth systems are visible.", None),
    ]
    instructions.sheet_view.showGridLines = False
    for index, (line, color) in enumerate(instruction_lines, 1):
        instructions.cell(index, 1, line)
        instructions.merge_cells(start_row=index, start_column=1, end_row=index, end_column=2)
        instructions.cell(index, 1).alignment = Alignment(wrap_text=True, vertical="top")
        if color:
            instructions.cell(index, 1).fill = PatternFill("solid", fgColor=color)
            instructions.cell(index, 1).font = Font(
                color="FFFFFF",
                bold=True,
                size=14 if index == 1 else 12,
            )
        instructions.row_dimensions[index].height = 30
    instructions.column_dimensions["A"].width = 85
    instructions.column_dimensions["B"].width = 10

    workbook.save(OUTPUT_PATH)

    verified = load_workbook(OUTPUT_PATH, data_only=False)
    review_check = verified["Review W01"]
    if review_check.max_row != 62 or review_check.max_column != 11:
        raise RuntimeError("Workbook dimensions do not match the expected 61-row checklist.")
    if review_check["A2"].value != 1 or review_check["A62"].value != 61:
        raise RuntimeError("Workbook requirement numbering is incomplete.")
    print(f"Created {OUTPUT_PATH.name}: 61 rows, 11 columns, {OUTPUT_PATH.stat().st_size} bytes")


if __name__ == "__main__":
    build_workbook()
