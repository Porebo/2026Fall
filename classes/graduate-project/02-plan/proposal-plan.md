# Research Proposal Plan

**Goal:** the signed Project Proposal Approval Form.
**Deliver to the committee by:** Monday, November 16, 2026.
**Course final proposal due:** Friday, December 4, 2026, 9:59 PM on Blackboard (see `../03-proposal/REQUIREMENTS.md`).
**Scope:** the proposal only. The research itself is not run before delivery; the runs done so far are dry runs.

**Principle:** the body comes first. A strong argument and a complete method can be dressed in any format later. Format, length, and citation style are handled last.

**Updated November 12, 2026.** The study design changed on November 11. The earlier design injected errors into CalGEM well and production tables and asked AI to fix them. The current design gives an AI assistant one real wellbore diagram and the state's casing diagram rule, and asks whether the diagram meets the rule. Section 2 records which decisions this settled. Paths are relative to `classes/graduate-project/`.

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

- [x] **Prompt types.** Four levels, each adding one technique: (1) unstructured zero-shot ("naive"), (2) structured zero-shot (persona, task, context, format: PTCF), (3) few-shot, (4) chain-of-thought. Source: `06-study/design/prompts/prompt-design-methods.txt`.
- [x] **Task and scenario.** A regulatory or engineering staff member checks whether an existing wellbore diagram meets the State's requirements before reusing it in a Notice of Intention to Abandon. Source: `06-study/design/scenario-business-need.txt`.
- [x] **Standard that defines an error.** California Code of Regulations, title 14, § 1726.4.1 (casing diagrams). A requirement is Present, Absent, or Illegible on the diagram. Verbatim text: `06-study/design/casing-diagram-specification.txt`.
- [x] **Dataset and sample.** Frame: every Active or Idle well in CalGEM's 2021 wells file (N = 107,952). Random order (seed 20261111), screened until 30 wells had a usable diagram in WellSTAR: W01 to W30. Source: `06-study/sample/sampling-plan.txt` (v1.2), data in `05-data/calgem/`.
- [x] **Sample size.** n = 30 as a pilot, justified by Lancaster (2004), Julious (2005), and Hertzog (2008).
- [x] **Input quality.** The 30 PDFs are profiled as Native, Mixed, or Scanned, and results will be reported by type. Source: `06-study/sample/sample-quality-evaluation.txt`.
- [x] **What the AI returns.** A free-text response to the prompt. From level 2 on, the prompt states the output format.
- [x] **Scoring.** (a) Accuracy: each requirement is judged correctly, judged wrongly, or not addressed, compared with the researcher's reference answers. (b) Cost to the worker: word count, share of the response that is on task, sources used from outside the attachments, and whether the response ends by asking the user a question. Source: `prompt-design-methods.txt`, section 8.
- [x] **Controls.** The same two attachments every time, one prompt in a new conversation, the first response only, and the same AI service and account within a comparison.

### Dropped by the new design

- [x] ~~Error types to inject~~. Nothing is injected; the diagrams are used as filed.
- [x] ~~ISO 8000-61 versus ISO/IEC 25012 as the error definition~~. The regulation is now the reference standard. Whether either ISO standard is still cited, for example to frame the quality dimensions, is open (section 3).

### Still open

- [ ] **Title.** The form's "Approximate title" field is blank.
- [ ] **Repetitions.** The methods draft sends each prompt once. The committee email promises several runs "to confirm that the results are consistent." Decide the number of runs, or change what the proposal promises.
- [ ] **AI service.** On the free ChatGPT tier, the attachment limit stopped the level 4 dry run after three runs (`06-study/runs/4-chain-of-thought-prompt/W01-chatgpt-free-NOT-RUN.txt`). Level 4 was then run on Gemini, which breaks the same-service control. Choose one service and tier for the study, or the rule for using two.
- [ ] **Reference answers.** Who prepares them, and whether a second person checks a subset.
- [ ] **Use of the 10-well Ventura pilot set** (`06-study/pilot-ventura/`). Keep it as background in the proposal, or leave it out.

---

## 3. Open questions about the argument

- [ ] **Does the introduction still lead to the study?** Paragraph 2 (`03-proposal/draft-introduction-paragraphs.txt`) leads to data cleaning of tables and "a training dataset." It needs to lead to checking documents against a regulation.
- [ ] **The committee email describes the old design.** It mentions injected errors in production data, and corrections. Decide whether the professors need a short note or summary that describes the current design.
- [ ] **Does the opening hold together?** Orlikowski (1992) to global reach (Liu & Wang, 2026) to organizations to for-profit fit.
- [ ] **Source linking data quality to profit or cost.** Candidate to verify: Redman (1998), *Communications of the ACM*. Order 1517 (Sentinel Peak, $1,500 penalty for deficient wellbore diagrams) gives a concrete cost of the specific problem (`05-data/calgem/enforcement-orders/`).
- [ ] **Sources for the four prompt types.** Kojima et al. (2022) covers chain-of-thought. PTCF and few-shot still need a citation.
- [ ] **Source for 2026 adoption figures.** Liu & Wang's data ends March 2024. Candidate to verify: Stanford AI Index 2026.
- [ ] **Do the three research questions from the Week 5 draft still fit?** They were written for the old design (`classes/research-methods/w05/study-design-draft.md`).

---

## 4. Sections of the body and what already exists

- [ ] **Introduction.** Have: paragraph 1 approved and paragraph 2 drafted (`03-proposal/draft-introduction-paragraphs.txt`); the business scenario (`06-study/design/scenario-business-need.txt`). Needs: paragraph 2 rewritten for the new design.
- [ ] **Research objectives and questions.** Have: three research questions in the Week 5 draft (old design). Needs: rewrite.
- [ ] **Literature review.** Have: 25 papers and regulation texts in `04-literature/papers/`, rules documents in `04-literature/regulatory/`, slides in `03-proposal/Research Proposal Lester S Carcamo.pptx`. Course rule: at least 20 cited in the body.
- [ ] **Method.** Have: draft section 3 (`03-proposal/3. Research Design and Methods.md`; 3.2.1 done), prompt design and evaluation (`06-study/design/prompts/prompt-design-methods.txt`), the sampling plan and its results (`06-study/sample/sampling-plan.txt`), input quality (`06-study/sample/sample-quality-evaluation.txt`), and data provenance (`05-data/calgem/PROVENANCE.md`). Missing: the open items in section 2.
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
