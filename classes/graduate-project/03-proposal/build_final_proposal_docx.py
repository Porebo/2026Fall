import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "Final Research Proposal Draft.md"
OUTPUT = ROOT / "Final Research Proposal Draft.docx"


def add_inline_markdown(paragraph, text: str) -> None:
    pattern = re.compile(r"(\*\*.*?\*\*|\*.*?\*|`.*?`)")
    position = 0
    for match in pattern.finditer(text):
        if match.start() > position:
            paragraph.add_run(text[position : match.start()])
        token = match.group(0)
        if token.startswith("**"):
            run = paragraph.add_run(token[2:-2])
            run.bold = True
        elif token.startswith("*"):
            run = paragraph.add_run(token[1:-1])
            run.italic = True
        else:
            paragraph.add_run(token[1:-1]).font.name = "Consolas"
        position = match.end()
    if position < len(text):
        paragraph.add_run(text[position:])


def configure_styles(document: Document) -> None:
    styles = document.styles
    styles["Normal"].font.name = "Times New Roman"
    styles["Normal"].font.size = Pt(11)
    styles["Normal"].paragraph_format.line_spacing = 1.0
    styles["Normal"].paragraph_format.space_after = Pt(6)
    for style_name in ("Title", "Subtitle", "Heading 1", "Heading 2", "Heading 3", "Heading 4"):
        styles[style_name].font.name = "Times New Roman"
        styles[style_name].font.color.rgb = None
    styles["Heading 1"].font.size = Pt(14)
    styles["Heading 1"].font.bold = True
    styles["Heading 1"].paragraph_format.space_before = Pt(12)
    styles["Heading 1"].paragraph_format.space_after = Pt(6)
    styles["Heading 2"].font.size = Pt(12)
    styles["Heading 2"].font.bold = True
    styles["Heading 3"].font.size = Pt(11)
    styles["Heading 3"].font.bold = True
    styles["Heading 4"].font.size = Pt(11)
    styles["Heading 4"].font.bold = True
    styles["Heading 4"].font.italic = True


def add_table(document: Document, rows: list[list[str]]) -> None:
    column_count = len(rows[0])
    table = document.add_table(rows=len(rows), cols=column_count)
    table.style = "Table Grid"
    for row_index, values in enumerate(rows):
        for column_index, value in enumerate(values):
            cell = table.cell(row_index, column_index)
            cell.text = ""
            add_inline_markdown(cell.paragraphs[0], value.strip())
            if row_index == 0:
                for run in cell.paragraphs[0].runs:
                    run.bold = True
            cell.vertical_alignment = 1
    document.add_paragraph()


def title_page(document: Document, lines: list[str]) -> int:
    document.add_heading(lines[0][2:], level=0)
    title = document.paragraphs[-1]
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle = document.add_paragraph(lines[2][3:])
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.runs[0].italic = True
    for line in lines[4:14]:
        if line.startswith("<div"):
            continue
        if line.strip():
            paragraph = document.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.add_run(line.replace("**", ""))
    document.add_page_break()
    return 17


def add_toc(document: Document) -> None:
    paragraph = document.add_paragraph()
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = ' TOC \\o "1-4" \\h \\z \\u '
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    placeholder = OxmlElement("w:t")
    placeholder.text = "Right-click and select Update Field to populate the table of contents."
    separate_run = OxmlElement("w:r")
    separate_run.append(placeholder)
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.append(begin)
    run._r.append(instruction)
    run._r.append(separate)
    paragraph._p.append(separate_run)
    paragraph._p.append(end)

    update_fields = OxmlElement("w:updateFields")
    update_fields.set(qn("w:val"), "true")
    document.settings.element.append(update_fields)


def build_document() -> None:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    document = Document()
    configure_styles(document)
    section = document.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

    index = title_page(document, lines)
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
            continue
        if stripped.startswith("<div"):
            document.add_page_break()
            index += 1
            continue
        if stripped.startswith("#### ") or stripped.startswith("### ") or stripped.startswith("## "):
            if stripped == "## Table of Contents":
                document.add_paragraph("Table of Contents", style="Title")
                add_toc(document)
                while index < len(lines) and not lines[index].strip().startswith("<div"):
                    index += 1
                continue
            heading_text = stripped.lstrip("#").lstrip()
            match = re.match(r"^(\d+(?:\.\d+)*)(?:\.)?\s", heading_text)
            if match:
                heading_level = min(match.group(1).count(".") + 1, 4)
            else:
                heading_level = 3
            document.add_heading(heading_text, level=heading_level)
        elif stripped.startswith("# "):
            document.add_heading(stripped[2:], level=1)
        elif stripped.startswith("|"):
            table_rows = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                row = lines[index].strip().strip("|")
                if not re.fullmatch(r"[-:| ]+", row):
                    table_rows.append([cell.strip() for cell in row.split("|")])
                index += 1
            if table_rows:
                add_table(document, table_rows)
            continue
        elif stripped.startswith("- **") or stripped.startswith("- "):
            paragraph = document.add_paragraph(style="List Bullet")
            add_inline_markdown(paragraph, stripped[2:])
        elif re.match(r"^\d+\.\s", stripped):
            paragraph = document.add_paragraph(style="List Number")
            add_inline_markdown(paragraph, re.sub(r"^\d+\.\s+", "", stripped))
        elif stripped.startswith("> "):
            paragraph = document.add_paragraph()
            paragraph.paragraph_format.left_indent = Inches(0.5)
            paragraph.paragraph_format.right_indent = Inches(0.5)
            add_inline_markdown(paragraph, stripped[2:])
        else:
            paragraph = document.add_paragraph()
            add_inline_markdown(paragraph, stripped)
            if stripped in ("**Table 1**", "**Table 2**", "**Table 3**", "**Figure 1**", "**Figure 2**"):
                paragraph.runs[0].bold = True
        index += 1

    document.core_properties.title = (
        "Prompt Structure and AI-Assisted Completeness Assessment of CalGEM Casing Diagrams"
    )
    document.core_properties.subject = "Research proposal in Information Science"
    document.core_properties.author = "Lester S. Carcamo"
    document.save(OUTPUT)
    print(f"Created {OUTPUT.name}: {OUTPUT.stat().st_size} bytes")


if __name__ == "__main__":
    build_document()
