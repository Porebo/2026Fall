from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_ROW_HEIGHT_RULE, WD_TABLE_ALIGNMENT


ROOT = Path(__file__).resolve().parent
COURSE_OUTPUT = ROOT / "Final Research Proposal - Course 12 Pages.docx"
SPONSOR_OUTPUT = ROOT / "Employer Sponsor Brief - 2 Pages.docx"

TITLE = "Prompt Structure and AI-Assisted Completeness Assessment of CalGEM Casing Diagrams"
SUBTITLE = "A Repeated-Measures Comparison of ChatGPT, Claude, and Gemini"


def add_field(paragraph, instruction: str, placeholder: str) -> None:
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instruction_node = OxmlElement("w:instrText")
    instruction_node.set(qn("xml:space"), "preserve")
    instruction_node.text = instruction
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text_node = OxmlElement("w:t")
    text_node.text = placeholder
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.append(begin)
    run._r.append(instruction_node)
    run._r.append(separate)
    paragraph._p.append(text_node)
    paragraph._p.append(end)


def set_update_fields(document: Document) -> None:
    settings = OxmlElement("w:updateFields")
    settings.set(qn("w:val"), "true")
    document.settings.element.append(settings)


def configure(document: Document, font_size: int, margin: float) -> None:
    styles = document.styles
    normal = styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(font_size)
    normal.paragraph_format.line_spacing = 1.0
    normal.paragraph_format.space_after = Pt(4)
    for style_name, size in (
        ("Title", 16),
        ("Subtitle", 12),
        ("Heading 1", 14),
        ("Heading 2", 12),
        ("Heading 3", font_size),
    ):
        style = styles[style_name]
        style.font.name = "Times New Roman"
        style.font.size = Pt(size)
        style.font.color.rgb = None
        style.paragraph_format.space_before = Pt(6)
        style.paragraph_format.space_after = Pt(3)
    for section in document.sections:
        section.top_margin = Inches(margin)
        section.bottom_margin = Inches(margin)
        section.left_margin = Inches(margin)
        section.right_margin = Inches(margin)
    set_update_fields(document)


def add_paragraph(document: Document, text: str, bold_label: str | None = None) -> None:
    paragraph = document.add_paragraph()
    if bold_label and text.startswith(bold_label):
        paragraph.add_run(bold_label).bold = True
        paragraph.add_run(text[len(bold_label) :])
    else:
        paragraph.add_run(text)


def add_bullets(document: Document, items: list[str]) -> None:
    for item in items:
        document.add_paragraph(item, style="List Bullet")


def add_numbered(document: Document, items: list[str]) -> None:
    for item in items:
        document.add_paragraph(item, style="List Number")


def add_page_number_footer(section) -> None:
    footer = section.footer
    paragraph = footer.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_field(paragraph, " PAGE ", "1")


def format_table(table) -> None:
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    header = table.rows[0]
    repeat = OxmlElement("w:tblHeader")
    repeat.set(qn("w:val"), "true")
    header._tr.get_or_add_trPr().append(repeat)
    column_count = len(table.columns)
    widths = [Inches(1.2), Inches(5.0)] if column_count == 2 else [
        Inches(6.2 / column_count)
    ] * column_count
    for row in table.rows:
        row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
        cant_split = OxmlElement("w:cantSplit")
        row._tr.get_or_add_trPr().append(cant_split)
        for column_index, cell in enumerate(row.cells):
            cell.width = widths[column_index]
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.space_after = Pt(0)
                paragraph.paragraph_format.line_spacing = 1.0


def add_title_page(document: Document) -> None:
    title = document.add_heading(TITLE, level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle = document.add_paragraph(SUBTITLE)
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.runs[0].italic = True
    document.add_paragraph()
    for text in (
        "A Research Proposal",
        "Lester S. Carcamo",
        "University of Arkansas at Little Rock",
        "Program: Information Science",
        "INFQ 72203 Research Methods",
        "Dr. Ningning Wu and Dr. Serhan Dagtas",
        "Fall 2026",
    ):
        paragraph = document.add_paragraph(text)
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_page_break()


def add_course_heading(document: Document, title: str, level: int = 1) -> None:
    document.add_heading(title, level=level)


def course_document() -> None:
    document = Document()
    configure(document, 11, 1.0)
    add_page_number_footer(document.sections[0])
    add_title_page(document)

    # Page 2: contents
    document.add_heading("Table of Contents", level=0)
    paragraph = document.add_paragraph()
    add_field(paragraph, ' TOC \\o "1-3" \\h \\z \\u ', "Update field to populate the table of contents.")
    document.add_page_break()

    # Page 3: introduction
    add_course_heading(document, "1. Introduction")
    add_course_heading(document, "1.1 Background and Problem", 2)
    add_paragraph(
        document,
        "Information completeness is central to regulatory review because a decision cannot rely on required data that are absent or not visible. California's CalGEM casing diagrams record how oil and gas wells are constructed and must include specified information. This proposal examines whether three free consumer AI assistants can identify whether that information is supplied.",
    )
    add_paragraph(
        document,
        "Section 1724.7.1(a) presents 15 numbered groups, but several groups contain multiple fields. Subdivision (d) separately requires both measured depth (MD) and true vertical depth (TVD) for each depth required under subdivision (a); subdivision (b) requires documentation of the cement calculations, cement slurry, and wellbore path to accompany the diagram; and subdivision (c) extends the requirements to redrilled and sidetracked boreholes. Together these become 90 atomic scoring points: 78 from subdivisions (a) and (d) (52 MD/non-depth and 26 TVD points) and 12 from subdivisions (b) and (c). This atomization prevents a grouped requirement from receiving credit when only part is present.",
    )
    add_paragraph(
        document,
        "The study measures presence only. A point is MET when the diagram supplies any explicit answer, including a value, “none,” or “N/A.” It is MISSING when no answer is supplied. For a subdivision-(b) point, a statement on the diagram that the information accompanies it separately is also MET. Point 90, borehole designation, is NOT_APPLICABLE when only one borehole is shown, so the denominator is 90 or 89. Truth, plausibility, and engineering accuracy are outside scope. In 2025, CalGEM cited multiple deficiencies in an order, including failure to provide accurate TVD at all depths (CalGEM, 2025b). The order was not based on TVD alone, but it demonstrates the regulatory importance of treating TVD as a separately required representation.",
    )
    add_course_heading(document, "1.2 Purpose and Research Questions", 2)
    add_paragraph(document, "The purpose is to measure how accurately ChatGPT, Claude, and Gemini detect the presence of the 90 required data points and whether prompt type affects accuracy.")
    add_bullets(
        document,
        [
            "RQ1. How accurately do the three AI services classify the 90 points as MET or MISSING?",
            "RQ2. Does point-level accuracy differ among naive, informed, and chain-of-thought prompts?",
            "RQ2a. Does accuracy increase across the ordered prompt conditions?",
            "RQ2b. What change occurs between adjacent prompt conditions?",
        ],
    )
    add_course_heading(document, "1.3 Significance", 2)
    add_paragraph(
        document,
        "The study provides operators, information professionals, and researchers with evidence about a bounded AI-assisted review task. It does not propose that AI replace engineering judgment. Its contribution is a repeatable framework for evaluating presence judgments on regulatory drawings and prompt effects on consumer AI interfaces.",
    )
    document.add_page_break()

    # Page 4: literature
    add_course_heading(document, "2. Literature Review")
    add_course_heading(document, "2.1 Completeness and AI Checklist Assessment", 2)
    add_paragraph(
        document,
        "Data quality research defines completeness relative to intended use. Lee et al. (2006) describe column completeness through missing values, while Wang and Strong (1996) place completeness among contextual dimensions. This study therefore evaluates each casing diagram as a record and each atomic requirement as a column. The construct is column completeness, not factual accuracy, timeliness, consistency, or accessibility.",
    )
    add_paragraph(
        document,
        "LLM studies show useful performance on checklist-style text but substantial variation. Srinivasan et al. (2025) reported strong aggregate performance on CONSORT reporting items, but confusion between absent events and unreported information required exclusion decisions. Spiero et al. (2026) found model-dependent performance and recommended human verification. Kataoka et al. (2026) reported that explicit checklists substantially improved PRISMA assessments, while false positives remained.",
    )
    add_paragraph(
        document,
        "Additional studies show task dependence. Chen et al. (2025) found high performance on reporting checklists; Chia et al. (2026) found clearer criteria easier than interpretive criteria; Alharbi and Asiri (2024) found stronger agreement for simple items. Tsybulnik et al. (2026), using standard interfaces, found notable between-model variation but lacked a human reference and repeated trials sufficient to determine correctness.",
    )
    add_course_heading(document, "2.2 Engineering Drawings and Prompt Design", 2)
    add_paragraph(
        document,
        "Engineering-document evidence is less encouraging for general-purpose models. Picard et al. (2025) and Doris et al. (2025) found substantial errors on engineering drawings and rule-linked tasks. Ali et al. (2026) showed that P&ID preprocessing improved information association, while Gupta et al. (2025) found graph conversion and examples improved performance. These systems used specialized pipelines rather than ordinary consumer interfaces.",
    )
    document.add_page_break()

    # Page 5: literature conclusion
    add_course_heading(document, "2.3 Well Records, Scans, and Verification", 2)
    add_paragraph(
        document,
        "Ma et al. (2024) extracted information from historical oil-and-gas records, obtaining high performance on clean PDFs but lower performance on scanned records with handwriting and stamps. Ostrow et al. (2026) similarly reported weaker extraction from scanned and handwritten medical records. These findings are relevant because WellSTAR diagrams may contain typed, mixed, or scanned content.",
    )
    add_paragraph(
        document,
        "Prompt effects are inconsistent. Kojima et al. (2022) reported gains from step-by-step prompting on arithmetic tasks, but limited or adverse effects on other tasks. Sorin et al. (2025) found chain-of-thought less reliable than other techniques for a radiology classification task. Narayan et al. (2022) demonstrated that small wording changes can produce material performance differences. The literature therefore supports testing prompt type rather than presuming improvement with added prompting structure.",
    )
    add_paragraph(
        document,
        "Verification research also warns that plausible evidence is not proof of correctness. Lin et al. (2026) found that cited evidence may reproduce a model's answer without establishing the answer's truth. Waqas et al. (2026) recommend human review for high-stakes uses. The present study responds by using a frozen human-reference record and scoring AI answers against it.",
    )
    add_course_heading(document, "2.4 Research Gap", 2)
    add_paragraph(
        document,
        "No reviewed study directly tests free consumer AI assistants on the completeness of public regulatory casing diagrams using a point-level human reference. Existing studies focus mainly on scientific text, specialized engineering pipelines, or value extraction. The proposed study addresses the gap by comparing three consumer services, three prompt conditions, and 30 actual diagrams under a repeated-measures design.",
    )
    document.add_page_break()

    # Page 6: data and design
    add_course_heading(document, "3. Data, Research Design, and Methods")
    add_course_heading(document, "3.1 Data", 2)
    add_paragraph(
        document,
        "The sample contains 30 publicly available casing diagrams of injection wells in CalGEM-approved underground injection control (UIC) projects, labeled U01–U30 and dated on or after April 1, 2019. Each diagram is reviewed against 90 atomic data points. The human-reference record stores MET or MISSING (or NOT_APPLICABLE, for point 90 only) for each point, the displayed answer, location, and a note when useful. The full AI dataset contains 270 observations: 30 diagrams × 3 services × 3 prompts.",
    )
    add_course_heading(document, "3.2 Research Design and Variables", 2)
    add_paragraph(
        document,
        "The primary independent variable is prompt type: naive, informed, and chain-of-thought. AI service—ChatGPT, Claude, or Gemini—is a blocking and grouping factor. The repeated-measures block is the diagram–service pair, producing 90 blocks. Each block receives all three prompt conditions. Prompt order will be counterbalanced, and every run will use a new chat.",
    )
    add_paragraph(
        document,
        "The primary dependent variable is point-level presence-judgment accuracy: correctly classified points divided by the applicable points (90, or 89 when only one borehole is shown). Secondary outcomes are wrong judgments, unaddressed points, number of rows returned, and response length. Controls are the diagram, regulation, 90-point checklist, reference record, account type, attachment set, presence-only rule, and manual execution procedure.",
    )
    add_course_heading(document, "3.3 Completeness Measure", 2)
    add_paragraph(
        document,
        "Diagram completeness equals the number of MET points divided by the applicable points (90, or 89 when only one borehole is shown). AI judgment accuracy equals the number of correctly classified points divided by the same denominator. These measures are different: the first describes the diagram; the second describes how well the AI matched the human reference. NOT_APPLICABLE is allowed only for point 90; INVALID is not a study status.",
    )
    document.add_page_break()

    # Page 7: human reference and prompt conditions
    add_course_heading(document, "3.4 Human Reference and Instrument", 2)
    add_paragraph(
        document,
        "One human reviewer visually inspects each diagram with a structured 90-row Excel checklist. For repeated structures, a point is MET only if every represented instance has an answer for the requested field or depth representation. MD and TVD are separate points. The reviewer records the visible text and location but does not decide whether the text is true, plausible, or engineering-valid.",
    )
    add_paragraph(
        document,
        "The completed review is loaded into a SQLite database whose parent entity is the diagram identifier. The database stores specification requirements, U01–U30 records, point-level statuses, and completeness infractions. A score view calculates MET divided by the applicable points (90 or 89). The reference is frozen before any AI response is scored.",
    )
    add_course_heading(document, "3.5 Prompt Conditions", 2)
    add_numbered(
        document,
        [
            "Naive: a minimal request for exactly 90 presence decisions.",
            "Informed: the same task framed by persona, task, context, and output format.",
            "Chain-of-thought: the informed prompt unchanged plus a step-by-step review instruction.",
        ],
    )
    add_paragraph(
        document,
        "All prompts receive the same three attachments: the original diagram, verbatim Section 1724.7.1, and the 90-point checklist. All prompt outputs require Point ID, Specification Code, Displayed Answer, and MET/MISSING Status (NOT_APPLICABLE for point 90 only). Explicit values, “none,” or “N/A” count as supplied answers. Prompts prohibit engineering-validity or correctness judgments.",
    )
    document.add_page_break()

    # Page 8: sampling, analysis, ethics
    add_course_heading(document, "3.6 Sampling and Analysis", 2)
    add_paragraph(
        document,
        "The 30 diagrams come from injection wells in CalGEM-approved UIC projects, to which Section 1724.7.1 applies through Section 1724.7. The 22,603 onshore Active or Idle injection-type wells in CalGEM's wells table were placed in a seeded simple random order and screened in WellSTAR. A well is included when it is a current injector in an Active or Suspended UIC project and has a legible PDF diagram of the existing well dated on or after April 1, 2019, when Section 1724.7.1 became operative. If multiple qualifying diagrams exist, the latest is retained. The pilot-sized sample supports repeated prompt comparison while remaining feasible for 270 manual runs.",
    )
    add_paragraph(
        document,
        "Prompt effects are analyzed separately within ChatGPT, Claude, and Gemini. For each service, a Friedman test examines the three related prompt conditions. Significant results are followed by paired Wilcoxon comparisons with Holm correction. Page's trend test may examine the ordered hypothesis. Service-specific estimates, confidence intervals, and point-level error counts will be reported rather than pooling services as independent observations.",
    )
    add_course_heading(document, "3.7 Ethics and Access", 2)
    add_paragraph(
        document,
        "The study uses public records and does not recruit human subjects or obtain private operator information. Institutional guidance or a non-human-subjects determination will be requested before data collection. Source URLs, acquisition dates, and any third-party copyright notices will be retained.",
    )
    add_paragraph(
        document,
        "Runs will be completed manually through ordinary consumer interfaces. The study will not use browser automation, bots, scraping, API substitution, or programmatic extraction. Only public diagrams, the regulation, checklist, and approved prompt are uploaded. Terms, privacy/training settings, model version where shown, and run metadata will be recorded. AI responses will be identified as AI-generated and not represented as authoritative engineering determinations.",
    )
    document.add_page_break()

    # Page 9: schedule and risks
    add_course_heading(document, "3.8 Schedule", 2)
    schedule = [
        ("Jan. 19–22", "Confirm ethics guidance; lock checklist, prompts, database, and counterbalancing"),
        ("Jan. 21–Feb. 3", "Complete and freeze 30 human-reference reviews"),
        ("Feb. 4–5", "Conduct the three-service dry run"),
        ("Feb. 8–26", "Complete 270 manual AI runs"),
        ("Feb. 27–Mar. 9", "Score and validate all responses"),
        ("Mar. 10–15", "Analyze service, prompt, order, and scan-quality results"),
        ("Mar. 16–22", "Draft findings, discussion, and limitations"),
        ("Mar. 23–31", "Committee review, APA editing, and library package"),
        ("Apr. 1", "Final review and university-library submission"),
    ]
    table = document.add_table(rows=1, cols=2)
    table.cell(0, 0).text = "Dates"
    table.cell(0, 1).text = "Activity"
    for dates, activity in schedule:
        row = table.add_row().cells
        row[0].text = dates
        row[1].text = activity
    format_table(table)
    add_course_heading(document, "3.9 Limitations and Risks", 2)
    add_bullets(
        document,
        [
            "Completeness is measured only; values are not verified against private operator records.",
            "One reviewer creates the reference; evidence and source locations will support auditability.",
            "Consumer model versions can change; runs will occur in a short window with versions and dates recorded.",
            "New chats and counterbalanced order reduce, but do not eliminate, carry-over and order effects.",
            "Poor diagram quality may lower performance; input type is recorded for sensitivity analysis.",
            "Manual operation is slower, but it supports provider-term compliance and run-level control.",
        ],
    )
    document.add_page_break()

    # Page 10: closing
    add_course_heading(document, "4. Closing Remarks")
    add_paragraph(
        document,
        "This proposal provides a controlled test of a narrow AI application: recognizing whether required information is supplied on a regulatory casing diagram. The framework separates diagram completeness from AI judgment accuracy, decomposes grouped requirements into 90 traceable points, explicitly scores MD and TVD, and scores the subdivision-(b) and (c) documentation and borehole points. It also preserves the distinction between presence and truth so that the study does not make unsupported engineering claims.",
    )
    add_paragraph(
        document,
        "The study is expected to yield service-specific evidence about prompt structure and practical failure patterns such as wrong presence calls, missed requirements, and incomplete 90-row responses. The deliverables will include a de-identified dataset, human-reference records, scoring logic, prompts, run logs, analytical summaries, and reproducible documentation.",
    )
    add_paragraph(
        document,
        "Results will be communicated through the course proposal, thesis talk, final project or thesis manuscript, and submission to the university library. They will be presented as evidence for supervised evaluation rather than as endorsement of AI autonomy. This scope allows the work to contribute to information science, information quality, and responsible evaluation of consumer AI without exceeding the available public evidence.",
    )
    document.add_page_break()

    # Pages 11–12: references
    add_course_heading(document, "5. References")
    references = [
        "Alharbi, F., & Asiri, S. (2024). Automated assessment of reporting completeness in orthodontic research using LLMs. Applied Sciences, 14(22), 10323. https://doi.org/10.3390/app142210323",
        "Ali, R. H., Park, C. Y., Aryal, A., Jeong, H. D., & Lee, G. (2026). Training-free P&ID information extraction through a hybrid computer vision and vision language model pipeline. Advanced Engineering Informatics, 76, 105125. https://doi.org/10.1016/j.aei.2026.105125",
        "Anh-Hoang, D., Tran, T. D., & Nguyen, L.-M. (2025). Survey and analysis of hallucinations in large language models. Frontiers in Artificial Intelligence, 8, 1622292. https://doi.org/10.3389/frai.2025.1622292",
        "California Department of Conservation. (2000). Conditions of use. https://www.conservation.ca.gov/index/Pages/use.aspx",
        "California Geologic Energy Management Division. (2025b). Order to perform remedial work and pay civil penalties (Order No. 1517). https://www.conservation.ca.gov/calgem/Documents/Orders/1517%20Sentinel%20Peak%20Resources%20California%20LLC_ADA.pdf",
        "Casing Diagrams, Cal. Code Regs. tit. 14, § 1724.7.1 (2026). https://www.law.cornell.edu/regulations/california/14-CCR-1724.7.1",
        "Chandran, D. R., & Gupta, V. (2022). A short review of the literature on automatic data quality. Journal of Computer and Communications, 10(5), 55–73. https://doi.org/10.4236/jcc.2022.105004",
        "Chen, D., Li, P., Khoshkish, E., et al. (2025). AutoReporter: Development of an artificial intelligence tool for automated assessment of research reporting guideline adherence. Journal of the American Medical Informatics Association. https://doi.org/10.1093/jamia/ocaf223",
        "Chia, A. W.-Y., Teo, W. L.-L., Munro, Y. L., & Dalan, R. (2026). Evaluating a generative AI model on qualitative research reporting standards. Scientific Reports, 16, 3258. https://doi.org/10.1038/s41598-025-29591-1",
        "Doris, A. C., et al. (2025). DesignQA: A multimodal benchmark for evaluating LLM understanding of engineering documentation. Journal of Computing and Information Science in Engineering, 25(2), 021009. https://doi.org/10.1115/1.4067333",
        "Guo, Y., Zhou, X., & Tang, S.-K. (2026). LLM-integrated semantic deep learning framework for floor-plan compliance assessment. Applied Sciences, 16(13), 2637. https://doi.org/10.3390/buildings16132637",
        "Gupta, M., Wei, C., Czerniawski, T., & Eiris, R. (2025). PIDQA—Question answering on piping and instrumentation diagrams. Machine Learning and Knowledge Extraction, 7(2), 39. https://doi.org/10.3390/make7020039",
        "He, Y., et al. (2026). Tabular data wrangling in the era of large language models: A survey. IEEE Transactions on Knowledge and Data Engineering, 38(10), 7080–7099. https://doi.org/10.1109/TKDE.2026.3716977",
        "Kataoka, Y., et al. (2026). Large language models for automated PRISMA 2020 adherence checking. International Journal of Medical Informatics, 219, 106561. https://doi.org/10.1016/j.ijmedinf.2026.106561",
        "Kojima, T., Gu, S. S., Reid, M., Matsuo, Y., & Iwasawa, Y. (2022). Large language models are zero-shot reasoners. Advances in Neural Information Processing Systems, 35, 22199–22213.",
        "Lee, J. H., Ji, S. Y., & Ostwald, M. J. (2026). Automated compliance checking across the building lifecycle. Automation in Construction, 185, 106859. https://doi.org/10.1016/j.autcon.2026.106859",
        "Lee, Y. W., Pipino, L. L., Funk, J. D., & Wang, R. Y. (2006). Journey to data quality. MIT Press.",
        "Lin, Y., Zeighami, S., & Parameswaran, A. G. (2026). Bolt-on, verifiable provenance for LLM-powered data processing. Proceedings of the VLDB Endowment, 19(11), 2992–3005. https://doi.org/10.14778/3836663.3836668",
        "Ma, Z., et al. (2024). Information extraction from historical well records using a large language model. Scientific Reports, 14, 31702. https://doi.org/10.1038/s41598-024-81846-5",
        "Naeem, Z. A., Ahmad, M. S., Eltabakh, M., Ouzzani, M., & Tang, N. (2024). RetClean: Retrieval-based data cleaning. Proceedings of the VLDB Endowment, 17(12), 4421–4424. https://doi.org/10.14778/3685800.3685890",
        "Narayan, A., Chami, I., Orr, L., Arora, S., & Ré, C. (2022). Can foundation models wrangle your data? Proceedings of the VLDB Endowment, 16(4), 738–746. https://doi.org/10.14778/3574245.3574258",
        "Ostrow, R. D., et al. (2026). Accuracy and utility of LLMs for extracting stewardship data from scanned records. Antimicrobial Stewardship & Healthcare Epidemiology, 6, e358. https://doi.org/10.1017/ash.2026.10919",
        "Picard, C., et al. (2025). Evaluating vision-language models for engineering design. Artificial Intelligence Review, 58, 288. https://doi.org/10.1007/s10462-025-11290-y",
        "Sorin, V., et al. (2025). Evaluating prompt and data perturbation sensitivity in LLMs for radiology reports. JAMIA Open, 8(4), ooaf073. https://doi.org/10.1093/jamiaopen/ooaf073",
        "Spiero, I., et al. (2026). Using LLMs for automated assessment of reporting quality in prediction-model studies. Journal of Clinical Epidemiology, 196, 112320. https://doi.org/10.1016/j.jclinepi.2026.112320",
        "Srinivasan, A., et al. (2025). LLM analysis of reporting quality of randomized clinical trial articles. JAMA Network Open, 8(8), e2529418. https://doi.org/10.1001/jamanetworkopen.2025.29418",
        "Tsybulnik, D. Y., Gillette, J. J., & Heston, T. F. (2026). Variability among LLMs in assessing CONSORT compliance. PLOS ONE, 21(9), e0358873. https://doi.org/10.1371/journal.pone.0358873",
        "Wang, R. Y., & Strong, D. M. (1996). Beyond accuracy: What data quality means to data consumers. Journal of Management Information Systems, 12(4), 5–34. https://doi.org/10.1080/07421222.1996.11518099",
        "Waqas, S. M., et al. (2026). Hallucination detection, verification, and correction in generative AI: A comprehensive survey. Natural Language Processing Journal, 16, 100231. https://doi.org/10.1016/j.nlp.2026.100231",
    ]
    references = references[:20]
    for index, reference in enumerate(references):
        paragraph = document.add_paragraph(reference)
        paragraph.paragraph_format.left_indent = Inches(0.25)
        paragraph.paragraph_format.first_line_indent = Inches(-0.25)
        if index == 10:
            document.add_page_break()
            document.add_heading("References, continued", level=1)
    add_course_heading(document, "6. AI Tools Acknowledgement")
    add_paragraph(
        document,
        "GitHub Copilot in VS Code was used to organize drafts, edit wording and formatting, construct the checklist and SQLite scoring structure, validate cross-document consistency, and review public policy sources. ChatGPT and Gemini were used in earlier exploratory prompt runs; those outputs are not observations in the final protocol. The researcher retained responsibility for design, interpretation, source selection, scoring rules, and final wording.",
    )
    document.save(COURSE_OUTPUT)
    print(f"Created {COURSE_OUTPUT.name}: {COURSE_OUTPUT.stat().st_size} bytes")


def sponsor_document() -> None:
    document = Document()
    configure(document, 11, 1.0)
    section = document.sections[0]
    add_page_number_footer(section)

    title = document.add_heading(TITLE, level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle = document.add_paragraph(SUBTITLE)
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.runs[0].italic = True
    metadata = document.add_paragraph(
        "Employer Sponsor Brief | Lester S. Carcamo | Information Science | Spring 2027"
    )
    metadata.alignment = WD_ALIGN_PARAGRAPH.CENTER

    document.add_heading("Purpose", level=1)
    add_paragraph(
        document,
        "This graduate research evaluates whether three consumer AI assistants—ChatGPT, Claude, and Gemini—can identify supplied versus missing information in public CalGEM casing diagrams. The study is designed to determine where AI may assist regulated document review and where human oversight remains necessary.",
    )
    document.add_heading("Business-Relevant Question", level=1)
    add_paragraph(
        document,
        "Can widely available AI tools reliably detect missing data in specialized technical drawings, and does the way a user writes the prompt materially change that performance? The study does not ask AI to determine whether the well data are engineering-correct. It measures only whether required information is present.",
    )
    document.add_heading("Research Design", level=1)
    add_bullets(
        document,
        [
            "30 public casing diagrams of UIC injection wells from WellSTAR, dated on or after April 1, 2019",
            "Diagrams are selected through a documented random-selection process from the public CalGEM record across multiple operators, including Aera, Berry, CRC, and others; the sample is not selected to represent any one employer",
            "90 traceable data points derived from California requirements, including separate measured-depth and true-vertical-depth checks",
            "Three AI services and three prompt designs: naive, informed, and step-by-step",
            "270 manual runs using ordinary consumer interfaces",
            "One human-reference review per diagram for controlled comparison",
            "Service-specific repeated-measures analysis and a documented accuracy score",
        ],
    )
    document.add_heading("Controls and Safeguards", level=1)
    add_bullets(
        document,
        [
            "No internal CRC data, records, documents, credentials, or account information will be used or uploaded",
            "No internal or employer-developed CRC AI model will be used; testing is limited to the ordinary consumer versions of ChatGPT, Claude, and Gemini",
            "No browser automation, scraping, or unauthorized programmatic access will be used",
            "AI responses will be preserved as AI-generated outputs, not represented as authoritative engineering findings",
            "Results will not validate well values; they will measure presence of supplied information",
            "Diagrams will be reported by study identifiers, and institutional ethics guidance will be obtained before collection",
        ],
    )
    add_paragraph(
        document,
        "The sample is an independently selected public-record research sample. The inclusion of any CRC, Aera, Berry, or other operator diagram results from the random selection method and does not indicate access to internal employer materials or a CRC-focused study.",
    )

    document.add_page_break()

    document.add_heading("Why This Degree Investment Has Practical Value", level=1)
    add_paragraph(
        document,
        "The project develops capabilities directly applicable to information-intensive work: translating regulatory requirements into structured fields, creating measurable quality criteria, testing technology under controlled conditions, protecting provenance, documenting limitations, and communicating findings to technical and nontechnical audiences.",
    )
    document.add_heading("Expected Deliverables", level=1)
    add_bullets(
        document,
        [
            "A reusable 90-point regulatory completeness checklist",
            "A SQLite data model that links each result to its source diagram and requirement",
            "An Excel human-review instrument and reporting view",
            "A prompt-engineering protocol and complete run log",
            "A comparative analysis of AI services and prompt structures",
            "A final Information Science thesis/project manuscript submitted to the university library",
        ],
    )
    document.add_heading("Schedule", level=1)
    schedule = document.add_table(rows=1, cols=2)
    schedule.cell(0, 0).text = "Dates"
    schedule.cell(0, 1).text = "Work"
    for dates, work in (
        ("Jan. 19–Feb. 5, 2027", "Finalize instruments, ethics confirmation, human reference, and dry run"),
        ("Feb. 8–26", "Complete 270 manual AI runs"),
        ("Feb. 27–Mar. 15", "Score results and perform statistical analysis"),
        ("Mar. 16–31", "Draft, review, format, and prepare publication materials"),
        ("Apr. 1", "Final review and university-library submission"),
    ):
        row = schedule.add_row().cells
        row[0].text = dates
        row[1].text = work
    format_table(schedule)
    document.add_heading("Expected Use and Boundaries", level=1)
    add_paragraph(
        document,
        "The intended value is evidence, not immediate automation. If the study finds strong performance, it may support supervised pilot testing for completeness checks. If performance is weak or inconsistent, the result is still useful because it defines limits and failure patterns before operational reliance. The study does not authorize AI use in company systems, replace qualified engineering review, or make regulatory compliance determinations.",
    )
    document.add_heading("Outcome for the Sponsor", level=1)
    add_paragraph(
        document,
        "The employer's investment supports graduate-level training in applied research, information governance, data quality, risk-aware AI evaluation, reproducibility, and technical communication. The work is directly relevant to organizations assessing whether consumer AI can support—not replace—responsible review of technical records.",
    )
    document.add_paragraph(
        "Contact: Lester S. Carcamo | Information Science | University of Arkansas at Little Rock"
    ).alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.save(SPONSOR_OUTPUT)
    print(f"Created {SPONSOR_OUTPUT.name}: {SPONSOR_OUTPUT.stat().st_size} bytes")


if __name__ == "__main__":
    course_document()
    sponsor_document()
