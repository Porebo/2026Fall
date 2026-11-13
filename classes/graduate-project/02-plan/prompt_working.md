# Working Notes: Research Proposal Session of November 10, 2026

**Purpose of this file:** carry the work of one long conversation into a new Claude Code session. Read this file and `proposal-plan.md` (same folder) before continuing.

**How to resume:** tell Claude: "Read `classes/graduate-project/02-plan/prompt_working.md` and `proposal-plan.md`, then continue from 'Next steps'."

**Note, November 12, 2026.** The project folder was reorganized from `w10/` into `classes/graduate-project/` (map in `README.md` there; every move in `_reorg-log.txt`). Paths below were updated. The study design in section 7 was replaced on November 11 by the wellbore diagram design; `proposal-plan.md` is the current record of decisions. This file is kept as the history of the November 10 session.

---

## 1. The goal

- **Final product:** Lester's master's project research proposal (MS Information Science), in full academic format.
- **Deadline:** deliver to committee members on **Monday, November 16, 2026**.
- **End of the whole thing:** the signed Project Proposal Approval Form.
- **Scope:** the proposal only. The research is not run before delivery.
- **Principle Lester set:** the body comes first. Format, length, and citation style are secondary and are applied last ("dress it later").
- **Advisor:** Dr. Ningning Wu. Draft form also lists Dr. Nitin Agarwal.

---

## 2. Files touched or created today

| File | State |
|---|---|
| `04-literature/papers/Orlikowski, 1992, The Duality of Technology - Rethinking the Concept of Technology in Organizations, Organization Science.pdf` | Renamed to the folder convention. Untracked in git |
| `04-literature/papers/Liu, 2026, Who on Earth Is Using Generative AI, World Development.pdf` | Renamed to the folder convention. Untracked in git |
| `02-plan/proposal-plan.md` | The plan, with checkboxes |
| `02-plan/prompt_working.md` | This file |

Folder naming convention for papers: `FirstAuthor, Year, Title, Journal.pdf`.

Nothing has been committed. Commit only when Lester asks.

---

## 3. Draft text of the proposal so far

### Paragraph 1 (Lester approved this wording, including the period after "however")

> Technology is both a product and a medium of human action (Orlikowski, 1992). In 2026, this statement is especially relevant to artificial intelligence (AI), a technology that people now build, shape, and work through every day. From east to west and from north to south, AI has reached nearly every country: ChatGPT traffic was recorded in 209 of 218 economies within 16 months of its release, although use remains far heavier in wealthier countries (Liu & Wang, 2026). People do not act alone, however. Much of their action takes place inside organizations, and those organizations are being affected as well. Individuals have embraced AI faster than the firms that employ them, and most firms are still working out how it can add value to their business (Liu & Wang, 2026). Interest and curiosity are widespread, but many people and organizations may not yet know with precision whether, or how, AI fits their for-profit activities.

Notes on paragraph 1:

- The first sentence is a paraphrase, not a quotation. Orlikowski's own wordings are "Technology is the product of human action" (p. 409) and "Technology is the medium of human action" (p. 410).
- "Build" is not supported by Liu & Wang, who measure use only. It rests on Orlikowski, for whom using and adapting a technology is part of producing it. Lester may keep or drop it.
- The firm sentence paraphrases Liu & Wang p. 3: most firms "are still trying to figure out how AI can add value to their businesses." Their firm evidence is from 2023 to 2024 and mostly from the United States.
- The last sentence is Lester's own claim and carries no citation.

### Paragraph 2 (draft, not yet reviewed by Lester)

> For a for-profit organization, much of that fit depends on information. Decisions, operations, and customer relationships rest on data, and data of poor quality harms both decision-making and customer satisfaction (Chandran, 2022; Wang et al., 1995). AI may help. Large language models have matched state-of-the-art results on data cleaning and integration tasks posed as prompts (Narayan et al., 2022), and they can fill in missing values in data tables (Naeem et al., 2024). AI may also fail to help. The same models can struggle with enterprise data they have never seen (Naeem et al., 2024), and they return answers with no indication of where the answer came from or whether it can be trusted (Lin et al., 2026). This paper examines that uncertainty on a small scale: using a commonly available AI tool, it tests how four basic types of prompts perform data quality actions on a training dataset.

Notes on paragraph 2:

- Lester's idea for it: profit resides much in the exactitude or quality of information, and AI may or may not help with data quality.
- Every citation here rests on the paper's **abstract only**. Each must be checked against the body.
- Author counts were not checked. "Chandran (2022)" and the "et al." forms need confirming.
- Change "training dataset" to "test dataset" (see section 7).
- No paper in the folder links data quality to profit or cost. See section 9.

### Reference entries built so far

- Orlikowski, W. J. (1992). The duality of technology: Rethinking the concept of technology in organizations. *Organization Science, 3*(3), 398–427.
- Liu, Y., & Wang, H. (2026). Who on earth is using generative AI? *World Development, 199*, Article 107260. https://doi.org/10.1016/j.worlddev.2025.107260

---

## 4. Orlikowski (1992): what the paper says

Read in full (30 pages, from extracted text; figures seen only as captions and labels).

**Problem.** Prior research splits technology into a false dichotomy:

- **Technological imperative:** technology is an objective, external force that determines structure.
- **Strategic choice:** technology is a product of human design, interpretation, and politics.
- **Technology as trigger (Barley):** closest to her view, but treats the artifact as physically fixed after deployment.

**Reconstruction**, drawing on Giddens' structuration theory:

- **Duality of technology:** technology is created and changed by human action and is also the medium through which humans act. Once deployed it tends to be reified.
- **Interpretive flexibility:** users can keep reshaping a technology physically or socially. The degree is bounded by the artifact, the institutional context, and users' knowledge and power.
- **Time-space discontinuity:** design and use usually happen in different places and times (vendor versus customer), which is why researchers see only one half.

**Model:** three components (human agents, technology, institutional properties) and four influences.

| Arrow | Influence |
|---|---|
| a | Technology is a product of human action |
| b | Technology is a medium of human action; it enables and constrains |
| c | Institutional conditions shape how people interact with technology |
| d | Using technology reinforces, or occasionally transforms, structures of signification, domination, and legitimation |

**Case:** "Beta," a software consulting firm with in-house CASE "productivity tools." Eight-month ethnography, 120 interviews, five projects.

- Tools encoded the firm's existing methodology, so standardization preceded the tools.
- Diffusion "was incremental at first, until the technology proved sufficiently robust to become mandatory on all large projects."
- Consultants told clients "the tools require it this way," which was not true: the "technological imperative" was socially constructed.
- Tools narrowed thinking: "you can't pick the 53rd" card.
- Some consultants secretly bypassed the tools, were caught, and still won modifications.
- New hires trained only on tools develop a "trained incapacity."
- Users "can always choose (at the risk of censure) not to utilize a technology."

**Weaknesses noted:**

- One case, from her own dissertation; it illustrates, it does not test.
- Beta built its tools in-house, so the vendor-to-customer argument is untested.
- Hard to falsify: actors' ability to act otherwise "may undermine any causal expectations."
- Tension with Giddens: she describes structures as "embedded" in artifacts.
- From background knowledge, not verified this session: she revised the model in 2000 ("technologies-in-practice") and later wrote on sociomateriality. Check before claiming a gap.

---

## 5. Lester's observations and the ideas developed from them

**Lester's own experience.** He sees AI as a benefit in his personal space and in his professional space as a salaried worker. It has become like an extension of himself. Two barriers are gone for him: writing code with precision, and getting acquainted with a scientific paper's content and unfamiliar vocabulary. He sees himself as **reaching for** AI, not being **pushed** into it. He notes this is only his case.

**Reaching versus pushed.** This maps onto institutional conditions (arrow c). Beta's consultants were mandated; Lester chooses. Same kind of technology, different conditions.

**Allowing versus expecting.** Lester flagged this as quite important.

- An organization can move from allowing AI to expecting it without the artifact changing.
- Expectation needs no formal rule: deadlines set at AI speed remove the real option of working without it.
- Under allowing, declining is free. Under expecting, it carries a penalty.
- Extension (Claude's, not Orlikowski's): the people who reach create the expectation, because their output becomes the baseline for everyone.
- It is a spectrum: prohibited, allowed, encouraged, expected, mandated.
- It connects to Oliver (1992): allowing-to-expecting is institutionalization, the reverse of deinstitutionalization.

**Where the paper pushes back on Lester's experience.**

- Enabling always comes with constraining.
- "Extension of myself" is the seamless state she warns makes a tool harder to question.
- Lester learned to code and read papers before AI, so he can judge its output. That may be a cohort effect.

**Age of the paper.** Written in 1992. AI was already discussed then as expert systems (her references include Collins 1987 and Woolgar 1985), but not as a general-purpose tool. Assumptions AI strains: technology is "inanimate"; designers knowingly build in the rules; the tool mediates but does not interpret; designers and users are distinct.

**Pillars.** Lester's view: her base concepts are pillars or definitions with little need or capability of changing. Agreed in the main, with a distinction: definitions cannot be tested, but propositions built on them can. The one pillar under pressure from AI is that all agency sits on the human side.

**Possible variables for research:** voluntary versus mandated use; pre-AI experience of the task.

---

## 6. Liu & Wang (2026): what the paper says

Read: full main text and conclusion. Not read: appendix tables A.3 to A.8 and the reference list.

- **Method:** Semrush website traffic for the top 40 generative AI tools, January 2022 to March 2024, plus Google Trends. Correlational; the authors make no causal claims.
- **Reach:** "Generative AI has reached nearly every corner of the world." ChatGPT traffic in 209 of 218 economies within 16 months.
- **Scale:** about 500 million monthly ChatGPT users, about 6% of world population or 12.5% of the global workforce, possibly overestimated.
- **Geography:** middle-income economies produce over half of traffic. Top five: United States, India, Brazil, Philippines, Indonesia. Low-income countries under 1%.
- **Intensity:** median visits per internet user in high-income economies are 5.3 times those in lower-middle-income economies.
- **Users:** skew young, highly educated, male. About half of chatbot users are college graduates. ChatGPT's female share was 33% in March 2024.
- **Use:** traffic drops about 40% on weekends and is mostly desktop, read as work and education use.
- **Predictors:** internet quality, English proficiency, literacy, youth share.
- **Effects:** Stack Overflow traffic fell about 30%; Google Translate about 20%; searches for "learn" declined as ChatGPT use rose.
- **Firms versus individuals:** fewer than 6% of US firms used AI (cited studies); four out of five AI users bring their own tools to work (cited survey).

**Limits when citing:** data ends March 2024; it measures website visits, not surveyed people; it misses app, API, enterprise, and most Chinese use.

**Fit with Lester's argument:** supports global reach, "work through," "reaching not pushed," and "barriers removed." Shows his case is the typical adopter profile. Does not support "settled into everyday use" everywhere or "build."

---

## 7. The study design as discussed today

**Design (Lester's):** obtain public California oil well dimensional and fact data; save it in a SQLite database; inject several known data quality errors; have AI prompts fix those errors.

**Why it is sound:** clean data plus injected known errors plus scoring against the original is a recognized method in data cleaning research. It supplies an answer key.

**Points raised:**

- Call it a **test dataset**, not a training dataset. Readers will otherwise assume machine-learning training data.
- Dimension and fact tables allow cross-table errors, such as production rows pointing to a well that does not exist.
- Public data is not perfectly clean. Score only the cells that were changed.
- From background knowledge, not verified: the public source is CalGEM, California's oil and gas regulator.

### Four prompt types, simple to complex (proposed Nov 10)

Each level adds exactly one thing, so differences can be traced to that addition.

| Level | Type | What it adds |
|---|---|---|
| 1 | Zero-shot instruction | Nothing: the baseline |
| 2 | Zero-shot with context | Table definitions, column meanings, valid values, table links |
| 3 | Few-shot | A few examples of an error and its correction |
| 4 | Chain-of-thought | Instruction to identify each error, explain it, then fix it |

**Conflict to resolve:** the Week 5 study design draft lists zero-shot, few-shot, role-based, and multistep. Role prompting was left out of the ladder because it changes framing without adding complexity. Lester has not yet chosen.

### Error types and ISO (Lester wants errors taken from ISO standards)

This part is **outside Lester's IQ library** and from general knowledge at medium confidence. The standards are paywalled; check the originals.

- ISO does not document "error types." It documents characteristics and measures. An error type is derived as a violation of a characteristic.
- **ISO/IEC 25012:** the data quality model, 15 characteristics (inherent, system-dependent, both).
- **ISO/IEC 25024:** measures for each 25012 characteristic.
- **ISO 8000:** mostly master data exchange and quality management processes. Part 8 separates syntactic, semantic, and pragmatic quality. The Week 5 draft cites ISO 8000-61:2016 (an error is a nonconformity with a documented requirement).

| 25012 characteristic | Injected error in the well data |
|---|---|
| Accuracy, syntactic | An API well number with the wrong length or a letter in it |
| Accuracy, semantic | A valid-looking but wrong value, such as the wrong county |
| Completeness | A null in a required field |
| Consistency | A production row for a nonexistent well; a duplicate well; completion date before spud date |
| Precision | Latitude and longitude rounded to one decimal |
| Currentness | A plugged well still marked active |

Credibility cannot be injected. System-dependent characteristics do not apply.

**Conflict to resolve:** ISO 8000-61 (Week 5 draft) versus ISO/IEC 25012 (today). They can work together: 8000-61 defines what an error is, 25012 classifies the kinds.

### Still for Lester to design (he said these are his to determine)

- What the AI returns (corrected rows or SQL), since it is part of the prompt.
- Scoring and the number of repetitions.
- Controls.

---

## 8. What the committee email promised

Source: `01-admin/committee-request-email-final.txt`.

- **Question:** whether AI can safely correct data quality errors.
- **Audience:** data workers who use SQL and their managers.
- **Positioning:** existing work uses specialized, laboratory-style setups; this builds on it with off-the-shelf, publicly available LLMs that need no special infrastructure or costly subscriptions.
- **Data:** public California oil-production data.
- **Errors:** "documented errors" introduced into the data.
- **Prompts:** four common prompting strategies.
- **Measures:** what each strategy corrects, what it misses, and whether it changes data that was already valid.
- **Repetition:** several runs to confirm results are consistent and not chance.
- **Timeline:** agreement to serve this semester, reply requested by November 20, 2026; report and final defense in spring.

---

## 9. Sources: verified, unverified, and missing

**Read in full this session:** Orlikowski (1992); Liu & Wang (2026) main text.

**Abstracts only this session:** Wang et al. (1995); Chandran (2022); Narayan et al. (2022); Naeem et al. (2024); He et al. (2026); Ju (2026); Guo (2025); Lin et al. (2026); Heuwinkel (2026). Anh-Hoang (2025) was seen by title only.

**Found by web search, not opened in full:**

- Stanford HAI, *AI Index Report 2026*: generative AI reached 53% population adoption within three years; 88% of surveyed organizations use AI. https://hai.stanford.edu/ai-index/2026-ai-index-report/economy
- Liu, Huang, & Wang (2025), World Bank Policy Research Working Paper 11231: update through mid-2025; 24% of internet users in high-income countries use ChatGPT versus 0.7% in low-income countries. Not peer-reviewed.
- Ali, ul Mustafa, & Aysan (2025), "Global adoption of generative AI: What matters most?", *Journal of Economy and Technology*. Peer-reviewed; 136 countries, 2023 data. No DOI found.

**Missing and needed:**

- A source linking data quality to profit or cost. Candidate from background knowledge, unverified: Redman (1998), "The Impact of Poor Data Quality on the Typical Enterprise," *Communications of the ACM*.
- A source defining the four prompt types, once the list is chosen.
- Access to the ISO standards, or a published paper describing them.

---

## 10. Tools and environment

- **Playwright MCP server:** registered today for this project with `claude mcp add playwright -- cmd /c npx -y @playwright/mcp@latest`. Health check reported Connected. It becomes usable after a new session starts. The browser is visible; Lester types logins himself; logins persist in the server's own profile. Remove with `claude mcp remove playwright -s local`.
- **Intended use:** reach sources behind a login (library databases, ISO text). Keep to reading pages Lester is entitled to; no bulk downloading.
- **PDF reading:** the Read tool cannot render PDFs here (no `pdftoppm`). Extract text with `python -P -X utf8` and `pypdf`, writing to the session scratchpad.
- **research-papers-sqlite MCP server:** configured but failed to connect this session (pending approval).

---

## 11. How Lester wants to work

- One step at a time; describe the largest unit first, then go down.
- His idea leads. Answer what he asked; do not add unrequested observations.
- Label anything from outside his IQ library or outside the papers read as such.
- Short quotes and paraphrases need citations; he asks about grammar and wording as he goes.
- Delete helper scripts when done; keep only deliverables.

---

## 11a. Session of November 10–11, 2026 (late): CalGEM data gathered

Everything was gathered in `w10/data/calgem/` (now spread across `04-literature/regulatory/`, `05-data/calgem/`, `06-study/`, and `scripts/`), documented in `05-data/calgem/PROVENANCE.md` (sources, dates, checksums, how to reproduce). Nothing committed.

- 2021 wells and monthly production CSVs, with spec files; GIS well metadata PDF.
- Wellbore diagram spec: 14 CCR § 1724.7.1 (15 required elements; MD and TVD; flat-file option) and § 1772.1.3; sources in `04-literature/regulatory/wellbore-diagram-sources/`.
- 14 real wellbore diagrams for 10 Ventura field wells, now in `06-study/pilot-ventura/` (text PDFs, renamed to well names).
- 436 enforcement orders in `enforcement-orders/` (PDFs git-ignored; `_index.csv` tracked).
- NOV sources in `04-literature/regulatory/nov-sources/`: 2021 annual report (1,789 NOVs vs 43 orders), SB 406 reports (NOVs only searchable per well in WellSTAR), NTO 2024-03.
- **Key source for the problem statement:** Order 1517 (Sentinel Peak, Inglewood), $1,500 penalty for wellbore diagrams failing § 1724.7.1: missing TVD and spud date, undocumented kickoff points, inaccurate data, graphic diagrams not matching flat-file data.
- Scripts kept (Lester's rule: data-collection scripts are deliverables): `select_ventura_wells.py`, `wellstar_wellbore_diagrams.js`, `download_enforcement_orders.py` (now in `scripts/`).
- Open offer: collect WellSTAR Violations grids for Ventura wells to count regulation sections cited.
- `.playwright-mcp/` folder in repo root holds browser snapshots; not yet cleaned or git-ignored.

## 12. Next steps

Per `proposal-plan.md`, Tuesday and Wednesday are for locking decisions:

1. Settle the title.
2. Choose the four prompt types (resolve the conflict in section 7).
3. Choose the standard that defines errors, then the error types to inject.
4. Lester designs: what the AI returns, scoring, repetitions, controls.
5. Review paragraph 2 and find the data-quality-to-profit source.
6. Use the Playwright browser, after restart, for sources behind a login.
