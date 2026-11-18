from pathlib import Path


ROOT = Path(__file__).resolve().parent
INTRODUCTION = ROOT / "1. Introduction.md"
LITERATURE_REVIEW = ROOT / "2. Literature review.md"
METHODS = ROOT / "3. Research Design and Methods.md"
OUTPUT = ROOT / "Final Research Proposal Draft.md"

TITLE = "Prompt Structure and AI-Assisted Completeness Assessment of CalGEM Casing Diagrams"
SUBTITLE = "A Repeated-Measures Comparison of ChatGPT, Claude, and Gemini"


def text_before_references(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    for marker in (
        "\n## References cited in this section",
        "\n## References\n",
    ):
        if marker in text:
            return text.split(marker, 1)[0].strip()
    raise RuntimeError(f"No references marker found in {path.name}")


def reference_entries(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    entries: list[str] = []
    collecting = False
    for line in lines:
        if line.startswith("## References cited in this section") or line == "## References":
            collecting = True
            continue
        if collecting and line.startswith("## Google Drive source folder tracker"):
            break
        if collecting and line.strip() and not line.startswith("> Working list"):
            entries.append(line.strip())
    return entries


def renumber_body(text: str, level: int) -> str:
    lines = text.splitlines()
    body: list[str] = []
    for line in lines:
        if line.startswith("# "):
            continue
        if line.startswith("## "):
            body.append(f"{'#' * level}{line[2:]}")
        elif line.startswith("### "):
            body.append(f"{'#' * (level + 1)}{line[3:]}")
        elif line.startswith("#### "):
            body.append(f"{'#' * (level + 2)}{line[4:]}")
        else:
            body.append(line)
    return "\n".join(body).strip()


def main() -> None:
    introduction = renumber_body(text_before_references(INTRODUCTION), 2)
    literature_review = renumber_body(text_before_references(LITERATURE_REVIEW), 2)
    methods = renumber_body(text_before_references(METHODS), 2)

    references = sorted(
        {
            entry
            for path in (INTRODUCTION, LITERATURE_REVIEW, METHODS)
            for entry in reference_entries(path)
        },
        key=str.casefold,
    )

    document = f"""# {TITLE}

## {SUBTITLE}

**A Research Proposal**

Lester S. Carcamo

University of Arkansas at Little Rock

INFQ 72203 Research Methods

Program: Information Science

Dr. Ningning Wu and Dr. Serhan Dagtas

Fall 2026

<div style="page-break-after: always;"></div>

## Table of Contents

1. Introduction
2. Literature Review
3. Data, Research Design, and Methods
4. Closing Remarks
5. References
6. AI Tools Acknowledgement

<div style="page-break-after: always;"></div>

## 1. Introduction

{introduction}

## 2. Literature Review

{literature_review}

## 3. Data, Research Design, and Methods

{methods}

## 4. Closing Remarks

This proposal addresses a practical information-quality question: whether free consumer AI assistants can consistently identify supplied and missing information in regulatory casing diagrams. The study contributes a reproducible, point-level measurement framework that connects a legal specification to observable diagram evidence, distinguishes completeness from accuracy, and treats measured depth and true vertical depth as separate required representations.

The primary contribution is a 77-point presence-only instrument derived from the 15 numbered groups in 14 CCR § 1724.7.1(a) and the MD/TVD requirement in subdivision (d). A human visual review will create the reference record for each diagram. The same frozen record will evaluate the outputs of ChatGPT, Claude, and Gemini under naive, informed, and chain-of-thought prompts. Manual execution, counterbalanced prompt order, service-specific analysis, and documented provider/privacy controls preserve the study's scope and support reproducible interpretation.

Findings will be communicated through the completed research proposal, thesis talk, final project or thesis manuscript, and final submission to the university library. Reproducibility materials will include the prompt files, 77-point checklist, scoring rules, human-review workbook, run log, SQLite schema, de-identified result dataset, and analysis documentation. Any publication will distinguish human-reference judgments from AI-generated output and will not represent the findings as CalGEM endorsement or as an engineering validation of the underlying well data.

## 5. References

{chr(10).join(references)}

## 6. AI Tools Acknowledgement

GitHub Copilot in VS Code was used during proposal development to organize the draft, edit language and formatting, construct the research checklist and SQLite scoring structure, validate cross-document consistency, search current public policy sources, and assist with study-protocol documentation. ChatGPT and Gemini were also used in earlier exploratory dry runs to examine provisional casing-diagram prompts; those outputs are not final-study observations and will not be used as data from the revised protocol.

The researcher retained responsibility for the study design, regulatory interpretation, research questions, variable definitions, scoring rules, source selection, and final wording. AI-generated suggestions were reviewed, revised, and checked against the regulation, cited source material, and project requirements. No AI output is represented as wholly human-generated or as a substitute for the required human-reference review.
"""

    OUTPUT.write_text(document.strip() + "\n", encoding="utf-8")
    print(f"Created {OUTPUT.name}: {len(document.splitlines())} lines")


if __name__ == "__main__":
    main()
