# Research Proposal Plan

**Goal:** the signed Project Proposal Approval Form.
**Deliver to the committee by:** Monday, November 16, 2026.
**Course final proposal due:** Friday, December 4, 2026, 9:59 PM on Blackboard (see `../03-proposal/REQUIREMENTS.md`).
**Scope:** the proposal only. The research itself is not run before delivery; the runs done so far are dry runs.

**Principle:** the body comes first. A strong argument and a complete method can be dressed in any format later. Format, length, and citation style are handled last.

**Updated November 12, 2026.** The study design changed on November 11. The earlier design injected errors into CalGEM well and production tables and asked AI to fix them. The current design gives an AI assistant one real casing diagram and the state's casing diagram rule, and asks whether the diagram meets the rule. Section 2 records which decisions this settled. Paths are relative to `classes/graduate-project/`.

---

## 1. The end state, worked backward

| Step | What must be true | By |
|---|---|---|
| 5. Signed form | Each committee member has signed, and the form is sent to the program coordinator | After Monday, as professors respond |
| 4. Delivery | Each professor who said yes has the proposal and the form | Mon, Nov 16 |
| 3. Dressed proposal | The finished body is formatted and proofread | Sun, Nov 15 |
| 2. Strong body | Every section is written and every citation is verified | Sat, Nov 14 |
| 1. Locked design | Every method decision is made on paper | Wed, Nov 11 (mostly done; see section 2) |

---

## 2. Decisions about the body

### Settled on November 11

- [x] **Prompt types.** Three levels since November 13, 2026, each adding one technique: (1) naive, (2) informed (persona, task, context, format: PTCF), (3) chain-of-thought (zero-shot). Few-shot was dropped. AI models: ChatGPT, Claude, and Gemini, free tiers. Source: `06-study/design/prompts/prompt-design-methods.txt`.
- [x] **Task and scenario.** A regulatory or engineering staff member checks whether an existing casing diagram meets the State's requirements before reusing it in a Notice of Intention to Abandon. Source: `calgem/scenario-business-need.txt`.
- [x] **Standard that defines an error.** California Code of Regulations, title 14, § 1724.7.1 (casing diagrams for underground injection control; the same 15 items as § 1772.1.3 for idle wells). Changed Nov 12 from § 1726.4.1 (gas storage wells, 18 items), because none of the 30 sampled wells is a gas storage well; changed Nov 13 from § 1772.1.3 to § 1724.7.1 (Onshore Well Regulations; covers producers in a project's area of review; enforced in Order 1517). A requirement is Present, Absent, or Illegible on the diagram. Verbatim text: `calgem/casing-diagram-specification.txt`.
- [x] **Dataset and sample.** Changed Nov 18: redrawn as a UIC-only sample so § 1724.7.1 applies to all 30. Population: onshore Active or Idle injection wells (SC, SF, WF, WD, PM, GD, INJ, AI) listed in WellSTAR as injectors in an Active or Suspended UIC (Class II) project, excluding gas storage, offshore, and plugged wells, with a legible PDF diagram dated on or after April 1, 2019. Frame: AllWells_20261118.csv, N = 22,603. Random order (seed 20261118), 132 screened to reach 30 eligible diagrams: U01 to U30. Source: `06-study/sample-uic/`. The earlier draw (every Active or Idle well in the 2021 file, N = 107,952, seed 20261111; 22 producers, 7 injectors, 1 observation well, 2 diagrams from 2018) is superseded; see `06-study/sample/sampling-plan.txt`.
- [x] **Sample size.** n = 30 as a pilot, justified by Lancaster (2004), Julious (2005), and Hertzog (2008).
- [ ] **Input quality.** The 30 PDFs are profiled as Native, Mixed, or Scanned, and results will be reported by type. Source: `06-study/sample/sample-quality-evaluation.txt` (superseded sample; the UIC sample's profile is `06-study/sample-uic/pdf-quality-profile.csv`: Native 21, Mixed 5, Scanned 4; a written evaluation is not yet done).
- [x] **What the AI returns.** A free-text response to the prompt. From level 2 on, the prompt states the output format.
- [x] **Scoring.** (a) Accuracy: each requirement is judged correctly, judged wrongly, or not addressed, compared with the researcher's reference answers. (b) Cost to the worker: word count, share of the response that is on task, sources used from outside the attachments, and whether the response ends by asking the user a question. Source: `prompt-design-methods.txt`, section 8.
- [x] **Checklist v3: other equipment in the well (Nov 18, 2026).** § 1724.7.1(a)(10) lists equipment "such as" SSSVs, packers, and gas-lift mandrels; "such as" is illustrative, so one non-depth, presence-only point was added: 32 `(a)(10).other_equipment`, "Other equipment in the well (e.g., tubing, pumps, rods)". MET when the diagram gives information on any other in-well equipment, including an explicit "none" or "N/A"; a blank label is MISSING. Points go from 77 to 78 (52 MD/non-depth, 26 TVD); former checklist points 32-77 are renumbered 33-78. Files: `06-study/design/prompts/*-v3.txt` (v2 kept unchanged), `04-literature/casing-analysis/migrate_add_other_equipment.sql` (DB requirement_id 88, appended), and Section 3 of the proposal.
- [x] **Checklist v4: subdivisions (b) and (c) scored (Nov 18, 2026).** Decision: § 1724.7.1(b) and (c) content, until now recorded as "supports another requirement, not scored," is now scored. Eleven presence-only points are appended as 79-89: (b)(1) cement-yield calculation steps, cement calculation steps; (b)(2) slurry volume (or sacks), density, yield, cement type, additives, each for every cement job; (b)(3) wellbore path MD, inclination, azimuth, for every borehole; (c) borehole designation (original hole, redrill, sidetrack). No TVD pairs, because (d) covers only (a) depths. Because (b) says "accompanied by documentation," a (b) point is MET if the published diagram shows the information or states or shows that it accompanies the diagram separately (e.g., "see directional survey"; student decision); MISSING when it neither shows nor references it, which does not mean the documentation was not filed. A sack count satisfies slurry volume (student decision). Point 89 is conditional (student decision): NOT_APPLICABLE when the diagram shows a single borehole, which drops the denominator to 88; with more than one borehole it is MET when each bore is identified and the information is given per bore, else MISSING. `migrate_v4b_point89_conditional.sql` allows NOT_APPLICABLE for id 89 only and makes the score view divide by the applicable points. An explicit "vertical" statement answers all three path points; a deviation range such as "Deviated (15° to 30°)" answers inclination only. Points go from 78 to 89 (63 MD/non-depth, 26 TVD). Files: `06-study/design/prompts/*-v4.txt` (v3 kept unchanged), `04-literature/casing-analysis/migrate_v4_subdivisions_b_c.sql` (reuses DB requirement_id 52-61, adds 89; score view now 89), and Sections 1 and 3 of the proposal.
- [x] **Checklist v4.1: cement job identification (Nov 18, 2026).** Student decision: § 1724.7.1(b)(2) requires slurry information "for each cement job completed," so a scored point identifies each cement job by date, stage number, or job name (e.g., U01 shows "8/1/2013" and "8/11/2013" on its cement entries). It is inserted as the first (b)(2) point, new point 81 `(b)(2).cement_job_identification`, "Cement job identification (date or stage)": MET when every cement job shown is identified (any indication, including "N/A"); blank or not mentioned is MISSING; non-depth, no TVD. Former points 81-89 become 82-90. Points go from 89 to 90 (78 from (a)/(d), 12 from (b)/(c); 64 MD/non-depth, 26 TVD). The conditional borehole point is now 90, and the denominator is 90, or 89 when only one borehole is shown. Files: `06-study/design/prompts/*-v4.1.txt` (v4 kept unchanged), `04-literature/casing-analysis/migrate_v41_cement_job_identification.sql` (DB requirement_id 90, appended; views 90 and 12), Sections 1 and 3 of the proposal, `03-proposal/build_final_proposal.py`, `build_short_deliverables.py`, and the two SVG figures.
- [x] **Controls.** The same two attachments every time, one prompt in a new conversation, the first response only, and the same AI service and account within a comparison.

### Dropped by the new design

- [x] ~~Error types to inject~~. Nothing is injected; the diagrams are used as filed.
- [x] ~~ISO 8000-61 versus ISO/IEC 25012 as the error definition~~. The regulation is now the reference standard. Whether either ISO standard is still cited, for example to frame the quality dimensions, is open (section 3).

### Still open

- [ ] **Title.** The form's "Approximate title" field is blank.
- [ ] **Repetitions.** The methods draft sends each prompt once. The committee email promises several runs "to confirm that the results are consistent." Decide the number of runs, or change what the proposal promises.
- [ ] **AI service and model comparison.** On the free ChatGPT tier, the attachment limit stopped the level 4 dry run after three runs (`06-study/runs/4-chain-of-thought-prompt/W01-chatgpt-free-NOT-RUN.txt`). Level 4 was then run on Gemini, which breaks the same-service control. The current methods draft proposes ChatGPT, Claude, and Gemini (270 runs); clarify whether prompt effects will be compared separately within each service (90 runs per service) or whether one service will be selected, then settle the service and tier.
- [ ] **Reference answers and scoring.** Decide whether a second person checks a subset of the researcher-prepared reference answers. Scoring rule: applicable items are coded Present or Not Present; conditional items that do not apply are excluded from that diagram's accuracy denominator (see `03-proposal/3. Research Design and Methods.md`, Section 3.2.2).
- [ ] **Align the methods draft with the sampling plan.** (Nov 18: Section 3.2.4 rewritten for the UIC-only sample, with counts from `06-study/sample-uic/README.txt`.) Section 3.2.3 still describes older population counts (83,567/83,287) and selection details, while the current plan samples from 107,952 Active or Idle wells. Update the proposal to match the final sampling frame, eligibility rules, and results.
- [ ] **Use of the 10-well Ventura pilot set** (`06-study/pilot-ventura/`). Keep it as background in the proposal, or leave it out.
- [x] **Exclusion rule for gas storage and offshore wells** (added Nov 13; resolved Nov 18: the UIC-only sample excludes both by definition). Section 3.2.4 says the study excludes gas storage and offshore wells, but the sampling plan has no such rule: the frame holds 415 type GS wells and 2,420 wells in offshore counties ("Los Angeles Offshore" and similar), and none was drawn only by chance. Decide whether to add an eligibility rule (a GS or offshore well is coded excluded and the next well in order is used) as change 1.5 in `06-study/sample/sampling-plan.txt`. The current 30 wells would not change.

---

## 3. Open questions about the argument

- [ ] **Does the introduction still lead to the study?** Paragraph 2 (`03-proposal/draft-introduction-paragraphs.txt`) leads to data cleaning of tables and "a training dataset." It needs to lead to checking documents against a regulation.
- [ ] **The committee email describes the old design.** It mentions injected errors in production data, and corrections. Decide whether the professors need a short note or summary that describes the current design.
- [ ] **Does the opening hold together?** Orlikowski (1992) to global reach (Liu & Wang, 2026) to organizations to for-profit fit.
- [ ] **Source linking data quality to profit or cost.** Candidate to verify: Redman (1998), *Communications of the ACM*. Order 1517 (Sentinel Peak, $1,500 penalty for deficient casing diagrams) gives a concrete cost of the specific problem (`05-data/calgem/enforcement-orders/`).
- [ ] **Sources for the three prompt types.** Kojima et al. (2022) covers chain-of-thought. The informed (PTCF) prompt still needs a citation.
- [ ] **Source for 2026 adoption figures.** Liu & Wang's data ends March 2024. Candidate to verify: Stanford AI Index 2026.
- [ ] **Do the three research questions from the Week 5 draft still fit?** They were written for the old design (`classes/research-methods/w05/study-design-draft.md`).

---

## 4. Sections of the body and what already exists

- [ ] **Introduction.** Have: paragraph 1 approved and paragraph 2 drafted (`03-proposal/draft-introduction-paragraphs.txt`); the business scenario (`calgem/scenario-business-need.txt`). Needs: paragraph 2 rewritten for the new design.
- [ ] **Research objectives and questions.** Have: three research questions in the Week 5 draft (old design). Needs: rewrite.
- [ ] **Literature review.** Have: papers in `04-literature/papers/`, regulation texts and supporting documents in `calgem/`, slides in `03-proposal/Research Proposal Lester S Carcamo.pptx`. Course rule: at least 20 cited in the body.
- [ ] **Method.** Have: draft section 3 (`03-proposal/3. Research Design and Methods.md`; 3.2.1 done), prompt design and evaluation (`06-study/design/prompts/prompt-design-methods.txt`), the sampling plan and its results (`06-study/sample/sampling-plan.txt`), input quality (`06-study/sample/sample-quality-evaluation.txt`), and data provenance (`calgem/PROVENANCE.md`). Missing: the open items in section 2.
- [ ] **Significance.** Have: the committee email (who benefits) and the scenario (why the task exists).
- [ ] **Limitations and ethics.** Have: `prompt-design-methods.txt`, section 9; the free-tier attachment limit. Add: no human subjects, no employer data, public records only.
- [ ] **Timeline.** Have: the email promises analysis and defense in spring.
- [ ] **Reference list.** Not compiled yet.
- [ ] **Abstract.** Written last.
- [ ] **Draft document.** `03-proposal/Lester Work.docx` has one placeholder per section required by the course.

---

## 5. Day by day

| Day | Work | Output |
|---|---|---|
| Tue, Nov 10 | Settle the title and the four prompt types | Prompt types settled; title open |
| Wed, Nov 11 | Lock every decision in section 2 | Most decisions locked in the study files; dry runs on W01 |
| Thu, Nov 12 | Reorganize the project folder. Close the open items in section 2. Write the Introduction and the Method | Two sections drafted |
| Fri, Nov 13 | Write the Literature Review | Third section drafted |
| Sat, Nov 14 | Write significance, limitations, timeline. Build the reference list. Verify every citation against its paper | Strong body complete |
| Sun, Nov 15 | Dress the document: format, abstract, title page, proofreading | Final document |
| Mon, Nov 16 | Fill in the form and send the proposal and form | Delivered |

- [x] Tue, Nov 10 done (partly)
- [x] Wed, Nov 11 done (partly)
- [ ] Thu, Nov 12 done
- [ ] Fri, Nov 13 done
- [ ] Sat, Nov 14 done
- [ ] Sun, Nov 15 done
- [ ] Mon, Nov 16 done

After Nov 16, for the course final (Dec 4): adapt the committee version to the course checklist in `03-proposal/REQUIREMENTS.md`, including the Google Drive source-verification folder with annotated PDFs.

---

## 6. Secondary: dressing the document (after the body is strong)

- [ ] **Template.** Ask Dr. Wu whether the department requires one. The course asks for a dissertation-style title page.
- [ ] **Length.** The course asks for a body of about 8 to 10 pages, single spaced, 10 to 12 point font.
- [ ] **Citation style.** Confirm APA or another style.
- [ ] **Title page and headings** applied.
- [ ] **Proofread.**

---

## 7. The form and signatures

- [ ] **Committee size.** The form has three signature lines plus an optional fourth. The draft lists Dr. Wu (chair) and Dr. Agarwal. Confirm how many members are required.
- [ ] **Signing order.** Ask whether Dr. Wu signs first as chair.
- [ ] **E-signatures.** Confirm they are accepted.
- [ ] **Fill in the form** (`01-admin/Proposal-Approval-Form-Carcamo-DRAFT.pdf`): approximate title and names of all committee members.
- [ ] **Send the proposal and form** to each professor who said yes.
- [ ] **Collect signatures.**
- [ ] **Sign as student and send the form** with the approved proposal to the program coordinator.

---

## 8. Risks

- **Reply timing.** The committee email gives professors until November 20 to answer, which is after Monday. On Monday the proposal can go only to those who have already said yes.
- **Review time.** The form says members are "approving the proposal," so they need time to read before signing. The signed form will likely come days after delivery.
- **Design differs from what the email promised.** A professor who agreed to the email's description may be surprised by the proposal. See section 3.
- **Free-tier limits.** About three diagrams a day can be checked on the free ChatGPT tier. Running 30 diagrams × 4 levels (more with repetitions) needs a plan for time or service.
- **Unverified citations.** Several claims drafted on Nov 10 rest on abstracts only. Saturday's check is required.
