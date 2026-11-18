# Casing diagram requirements: sources and crosswalk to the 77-point instrument

> **Note (2026-11-18):** Superseded counts: instrument adopted as checklist v4 (89 points) on 2026-11-18.

Prepared November 18, 2026. Research only; no existing file was changed. New source copies are in `../calgem/` (listed in Section 1.3).

**Scope.** This note lists every California statute, regulation, and official CalGEM document found that (a) requires a casing diagram or wellbore schematic, (b) says what one must contain or what must go with it, or (c) governs the same well data in another document. It then maps each required data element to the current 77-point checklist (`../06-study/design/prompts/casing-diagram-atomic-checklist-v2.txt`).

**Method.** CCR text came from Cornell LII (HTTP download of each section page, Nov 18, 2026). All 189 sections of 14 CCR Ch. 4, Subch. 1, 1.1 and 2 (Arts. 1–5, 1.1 Art. 3, 2 Arts. 1, 2.5, 3, 4) were downloaded and searched for "diagram", "schematic" and "casing record". PRC text came from leginfo (browser). The full text of PRC Div. 3, Ch. 1, Art. 4 (§§ 3200–3238) was searched the same way, along with §§ 3160, 3180, 3181, 3106, 3206.3, 3208.1, 3236.5 and 3280–3291 (SB 1137). CalGEM pages were read in the browser, with collapsed FAQ and accordion text included. CalGEM spreadsheets and PDFs were downloaded and searched. Westlaw copies already in `calgem/` were reused and not re-fetched.

**Caveat on LII currency.** LII prints no currency date. Its § 1765 heading still reads "Suspended" even though SB 1137 is in force, so LII can lag. Check any LII-only text against Westlaw before quoting it in the proposal.

---

## 1. Sources

### 1.1 Table of sources

Key to the "Diagram role" column:
- **REQ**: requires a casing diagram to be submitted.
- **CONTENT-ON**: lists data that must appear on the diagram.
- **CONTENT-WITH**: lists documentation that must accompany the diagram.
- **RELATED**: governs the same well data in another record.
- **NONE**: searched; no diagram requirement found (a negative result).

| # | Citation | Trigger (well type / event) | Diagram role | File in `calgem/` |
|---|---|---|---|---|
| S1 | 14 CCR § 1724.7.1(a)–(e) | UIC project: every well in the area of review (AOR) that is completed in or penetrates the injection zone or a deeper zone, producers included | CONTENT-ON (a), (c), (d); CONTENT-WITH (b); format (e) | Casing Diagrams, 2026, …1724.7.1, Westlaw.txt; …2026a…LII.pdf (existing) |
| S2 | 14 CCR § 1724.7(a)(1)(C)(iii), (c), (d) | UIC project approval, expansion, data update | REQ (a)(1)(C)(iii); labeling of "all maps, diagrams, and exhibits" (c); licensed-professional cover page (d) | Project Data Requirements, 2026, …1724.7, Westlaw.txt / LII.pdf (existing) |
| S3 | 14 CCR § 1724.7(a)(1)(C)(i) | Same | RELATED: compendium of API number, wellbore path, total depth and completion-interval depths for all AOR wells | Same |
| S4 | 14 CCR § 1724.8 | UIC: evaluation of AOR wells | RELATED: the Division evaluates "cementing records"; may require a cement evaluation log | **NEW** Evaluation of Wells Within the Area of Review, 2026, …1724.8, Legal Information Institute.txt |
| S5 | 14 CCR § 1772.1.2(c), (f) | Idle well reaching 15 years idle (engineering analysis); not required for wells on a Testing Waiver Plan, partially plugged wells (§ 1752(e)) or UGS-tested wells (§ 1772.7) | REQ (c); labeling "scale and purpose" (f) | Engineering Analysis for 15-Year Idle Wells, 2026, …1772.1.2, Westlaw.txt (existing) |
| S6 | 14 CCR § 1772.1.3 | Same as S5 | CONTENT-ON / CONTENT-WITH; same 15 items as S1, with "if applicable" added in (a)(15) | Casing Diagrams, 2026, …1772.1.3, Westlaw.txt (existing) |
| S7 | PRC § 3206.1 | Idle wells (AB 2729) | RELATED: statutory basis for S5 and S6; no content | **NEW** Cal. Pub. Res. Code 3206.1, 2026, California Legislative Information.txt |
| S8 | 14 CCR § 1726.4(a)(5)(F), (c) | Underground gas storage (UGS) project AOR wells | REQ; labeling: scale, north arrow, coordinate system, purpose | Underground Gas Storage Project Data Requirements, 2026, …1726.4, Westlaw.txt (existing) |
| S9 | 14 CCR § 1726.4.1 | UGS | CONTENT-ON (18 items + MD/TVD + barriers); directional survey (a)(3) | Casing Diagrams, 2026, …1726.4.1, Westlaw.txt (existing) |
| S10 | CalGEM NTO to UGS operators, "Casing Diagram Submission Requirements," Dec 5, 2025 | UGS: any change to wellbore equipment, including work that needs no NOI | REQ: updated diagram within 60 days | Casing Diagram Submission_UGS NTO_Dec 2025.pdf; CalGEM 2025a…pdf (existing) |
| S11 | 14 CCR § 1784(a)(2)(A)–(B) | Well stimulation treatment (WST) permit: wells within 2× ADSA | CONTENT-ON (11 items, including "method of determining" cement); wellbore path for directional wells | Well Stimulation Treatment Area Analysis and Design, 2026, …1784, Westlaw.txt (existing) |
| S12 | 14 CCR § 1783.1(a)(21) | WST permit application | REQ (incorporates the § 1784(a) analysis); see also § 1780(d) below | **NEW** Contents of Application for Permit to Perform Well Stimulation Treatment, 2026, …1783.1, Legal Information Institute.txt |
| S13 | 14 CCR § 1753.1.1(a) | Cost-estimate verification, only on written request | REQ (may include casing diagrams); no content | Requirements for Cost Estimates, 2026, …1753.1.1, Westlaw.txt (existing) |
| S14 | PRC §§ 3229, 3230 | Notice of intention (NOI) to abandon (all wells) | CONTENT for the NOI: "(a) The total depth … (b) The complete casing record of the well, including plugs" | Cal. Pub. Res. Code 3229 / 3230 …txt (existing) |
| S15 | PRC § 3203; 14 CCR § 1722(d) | NOI to drill, deepen, redrill, rework, plug and abandon | RELATED: NOI on Division forms with "all information required on the forms" | 3203 (existing); **NEW** General, 2026, …1722, Legal Information Institute.txt |
| S16 | CalGEM "Permitting, Forms, and Compliance" (For Operators) page | Plugging and abandonment NOI (OG106); rework; drilling | P&A: a wellbore schematic is listed among attachments "needed," and "The diagram must include casing intervals and sizes, perforation locations, cement plug depths inside casing, and the location of the cement outside casing." Rework: schematic as attachment. Drill: proposed schematic. | Permitting, Forms, and Compliance, 2026, CalGEM For Operators page.txt (existing) |
| S17 | WellSTAR NOI instructions EICD013 v3.11 (form) and EICD008 v3.13 (EDD) | Every NOI | RELATED: structured "Wellbore Construction" feature records: feature type, top MD, bottom MD (required); OD, ID, weight, grade, new pipe, pulled, install/remove dates, burst pressure, connection type (optional); cement segments inside/outside, top MD, bottom MD (required); volume, sacks, yield, verification method, company, dates (optional). MD only. | Notice of Intention Instructions EICD013 …pdf (existing; identical to the current CalGEM download, same MD5); **NEW** Notice of Intention EDD Instructions EICD008 v3.13 2020-07-22.pdf |
| S18 | DOC Public Works Well Abandonment Contract Template, pp. 1–2 | State-contracted abandonment (orphan wells); OG108 NOI | CONTENT-ON: 17 items for current and proposed diagrams | Public Works Well Abandonment Contract Template Labor Code.pdf (existing) |
| S19 | CalGEM "Guidance: NOI and Permit Search in WellSTAR," p. 3 | NOI document review | RELATED: lists the document type "Wellbore Diagram (current and proposed)" | Guidance_for_NOI_and_Permit_Search_Draft 1 1.pdf (existing) |
| S20 | 14 CCR § 1724; PRC §§ 3210–3213 | Every well drilled, redrilled, deepened or reworked | RELATED: log, core record and history (casing, tubing, packers, hole sizes, cementing and plugging, junk, sidetracked casing, explosives, tests) | **NEW** Required Well Records, 2026, …1724, LII.txt; **NEW** Cal. Pub. Res. Code 3210/3211/3212/3213 …txt |
| S21 | 14 CCR § 1724.1; PRC §§ 3215, 3216 | Within 60 days after completion, abandonment or suspension; on request | RELATED: filing of the well summary, history, logs and surveys | **NEW** Records to be Filed with the Division, 2026, …1724.1, LII.txt; 3215, 3216 (existing) |
| S22 | CalGEM "For Operators – Underground Injection Control" (UIC Application Guidance) page | UIC applications | Guidance: diagrams for all idle, P&A and deeper-zone producing wells in the AOR; CalGEM "must evaluate casing diagrams for all wells within the area affected"; FAQ: base-of-freshwater picks are required even in exempted zones; collated PDF "with diagrams as a separate document"; Appendix C "Casing Diagram Information" | **NEW** For Operators - Underground Injection Control, 2026, CalGEM UIC Application Guidance page.txt |
| S23 | CalGEM MOA UIC Checklist (2026.03) | UIC project (MOA with Water Boards) | Guidance: "Well construction diagrams for all wells and boreholes within the AOR … should identify all of the data specified in Section 1724.7.1, including but not limited to: depth; perforated/slotted interval(s); cement (e.g., annular seal, plugs, and squeezes); casing damage; key geologic markers (e.g. injection zone, confining zone, all oil and gas zones); base of freshwater; base of USDW. Each well and borehole diagram needs to depict the entire history (e.g. sidetracks, redrills, and other mechanical changes)." | MOA UIC Checklist_2026.03.xlsx (existing). PROVENANCE.md line 154 says no diagram passage was found in it; that is incorrect (see Q7). |
| S24 | CalGEM UIC Non-Expansion Checklist (Final 12.08.21), row W-ES(5) | UIC non-expansion (new injectors within an approved project) | Guidance: diagrams for AOR wells that fail zonal isolation show "depth and perforated interval … cement plugs, casing damage, key geologic markers … and USDW"; entire history | **NEW** California Geologic Energy Management Division, 2021, UIC Non-Expansion Checklist (Final 12.08.21).xlsm |
| S25 | CalGEM NTO 2026-02, Updated UIC Project Approval Process | UIC applications | Process: early AOR wellbore-diagram evaluation "focusing on cement calculation methodology and well construction accuracy"; no new content | 2026-02 UIC Approval Process Update.pdf; CalGEM 2026c…pdf (existing) |
| S26 | 40 CFR § 146.24(a)(7) (federal floor, Class II) | Class II injection well permits | REQ: "schematic or other appropriate drawings"; not itemized | Code of Federal Regulations, 2025, 40 CFR 146.24…pdf (existing) |

**Negative results (searched; no casing-diagram requirement):**
- 14 CCR §§ 1723–1723.9 (plugging and abandonment)
- 14 CCR § 1752 (partially plugged wells)
- 14 CCR § 1722.7 (directional survey on order)
- 14 CCR § 1777.4 (well maintenance history)
- 14 CCR §§ 1765–1765.10 and PRC §§ 3280–3291 (SB 1137 health protection zones). § 1765.3(c)(5) asks for test results and cement bond logs, not diagrams.
- PRC §§ 3106, 3160, 3181, 3206.3, 3208, 3208.1, 3220, 3224, 3236.5
- 14 CCR § 1724.10. It requires a water-treatment process flow diagram, not a casing diagram.
- Offshore Subch. 1.1. § 1747.8 is a gas-detection diagram; § 1748.2 is repealed.
- WellSTAR NOI user guide R5.1.1 (document types do not include a required wellbore diagram).
- Idle Well Program For Operators page (restates § 1772.1.3 only).
- CalGEM UIC Project Wells List template (EICD001 project well data, not a diagram specification).

**Context, not content:**
- 14 CCR § 1722.2: "All depths refer to true vertical depth (TVD) below ground level" (casing program). This matters for Q4.
- 14 CCR § 1780(d), operative 10/1/2024: "The Division … will not approve applications for permits to conduct well stimulation treatments." S11 and S12 are therefore dormant.

### 1.2 Count

- **26 sources** are in the table: 13 statutory or regulatory provisions or groups, 12 CalGEM or DOC guidance, form or notice documents, and 1 federal rule. In detail:
  - 14 CCR: 1724.7.1, 1724.7, 1724.8, 1772.1.2, 1772.1.3, 1726.4, 1726.4.1, 1784, 1783.1, 1753.1.1, 1722, 1724, 1724.1
  - PRC: 3229/3230, 3203, 3206.1, 3210–3213, 3215/3216
  - Guidance, forms and notices: S10, S16–S19, S22–S25
- **Newly found:**
  - Regulations and statutes: 14 CCR §§ 1722(d), 1724, 1724.1, 1724.8, 1783.1; PRC §§ 3206.1, 3210–3213.
  - CalGEM documents: the UIC Application Guidance page, the Non-Expansion Checklist, and the EICD008 NOI EDD instructions.
  - Not new files, but newly used content: the diagram rows in the existing MOA UIC Checklist; the existing NOI EICD013 wellbore-construction fields; the 17-item list in the existing contract template.

### 1.3 Files saved (13 new; none overwritten)

All in `c:\repos\2026Fall\classes\graduate-project\calgem\`:

1. `General, 2026, Cal. Code Regs. tit. 14, 1722, Legal Information Institute.txt`
2. `Required Well Records, 2026, Cal. Code Regs. tit. 14, 1724, Legal Information Institute.txt`
3. `Records to be Filed with the Division, 2026, Cal. Code Regs. tit. 14, 1724.1, Legal Information Institute.txt`
4. `Evaluation of Wells Within the Area of Review, 2026, Cal. Code Regs. tit. 14, 1724.8, Legal Information Institute.txt`
5. `Contents of Application for Permit to Perform Well Stimulation Treatment, 2026, Cal. Code Regs. tit. 14, 1783.1, Legal Information Institute.txt`
6. `Cal. Pub. Res. Code 3206.1, 2026, California Legislative Information.txt`
7. `Cal. Pub. Res. Code 3210, 2026, California Legislative Information.txt`
8. `Cal. Pub. Res. Code 3211, 2026, California Legislative Information.txt`
9. `Cal. Pub. Res. Code 3212, 2026, California Legislative Information.txt`
10. `Cal. Pub. Res. Code 3213, 2026, California Legislative Information.txt`
11. `For Operators - Underground Injection Control, 2026, CalGEM UIC Application Guidance page.txt`
12. `California Geologic Energy Management Division, 2021, UIC Non-Expansion Checklist (Final 12.08.21).xlsm` (SHA-256 9fe1c4e31b1a2715450de01863155419276afb975164ab0ef2c4eea6e41ad1ac; source `conservation.ca.gov/calgem/Documents/UIC%20regulations/Nonexpansion%20Checklist_Final_12.08.21.xlsm`)
13. `Notice of Intention EDD Instructions EICD008 v3.13 2020-07-22.pdf` (SHA-256 3076773f6e357e6c6cd76cd1b552a15e59232d32b310720193cf29abbabd48b3; source `conservation.ca.gov/calgem/pubs_stats/Documents/Notice-of-Intention-Instructions-EDD-ADA.pdf`)

Notes on the files:
- The CCR copies are verbatim .txt files extracted from LII HTML. PDF printing was not available in this session, so no PDFs were made.
- Each .txt carries a source, URL and retrieval-date header in the existing style.
- PROVENANCE.md was not updated, because no existing file was to be edited. Add these 13 rows when convenient.

---

## 2. Applicability to the 30 sample wells

**The sample is not a sample of UIC-project wells.** Sampling plan v1.5, Section 1, defines the population as unplugged (Active or Idle) wells with a diagram on file. Selection is by random order only, and "well type" is explicitly not used. `screening-log.csv` (well type codes from the 2021 frame) gives:

| Type code | n | Wells |
|---|---|---|
| OG (oil & gas producer) | 22 | W01, W03, W04, W06, W09, W10, W11, W13–W26, W28 |
| WF (waterflood injector) | 2 | W05, W08 |
| SF (steamflood injector) | 2 | W12, W30 |
| SC (cyclic steam) | 1 | W29 |
| WD (water disposal) | 1 | W07 |
| GD (gas disposal) | 1 | W27 |
| OB (observation) | 1 | W02 |

W01 is API 0403033530, 948C-28, Belridge South, OG (producer). The log does not record the operator, by design.

| Source group | Applies to the 30? | Basis |
|---|---|---|
| S1–S3 (§§ 1724.7.1, 1724.7) | **7 injectors (W05, W07, W08, W12, W27, W29, W30) directly** as project wells. W02 (observation well) and the 22 producers apply **only if** the well lies in a UIC project AOR and penetrates the injection zone or deeper. This is likely in the Kern steam and waterflood fields but **not verified per well** (Q3). | § 1724.7(a)(1)(C)(iii) |
| S5–S6 (§§ 1772.1.2, 1772.1.3) | **Conditional:** only an idle well at 15 years idle, and not on a Waiver, partially plugged, or UGS-tested. 14 wells are Idle now; idle start dates were not checked. | § 1772.1.2(a), (i) |
| S8–S10 (UGS) | **No.** No sampled field is a gas storage field (W27 GD is gas disposal at Midway-Sunset). | Sampling plan §11; scenario doc |
| S11–S12 (WST) | **No.** No permits since 10/1/2024 (§ 1780(d)). | |
| S13 (cost estimates) | Only on CalGEM's written request; no content specified. | |
| S14–S19 (NOI and P&A) | **All 30 at abandonment.** This is the study's own business scenario (scenario-business-need.txt, OG108 NOI). The statute requires only TD and the casing record with plugs in the NOI. Diagram content comes from guidance (S16) and, for state-contracted wells only, the template (S18). | PRC § 3230 |
| S20–S21 (well records) | All 30, but these govern the well file, not the diagram. | § 1724; PRC § 3210 |
| S22–S25 (UIC guidance) | Same footprint as S1. Guidance, not regulation. | |
| S26 (federal) | The 7 Class II injectors; not itemized. | |

**Timing.** W11 (Relevant Date 07/05/2018) and W28 (11/05/2018) pre-date the operative date of §§ 1724.7.1 and 1772.1.3, April 1, 2019. Under the pre-2019 rule (former § 1724.7(a)(4)), no item list applied to them.

---

## 3. Crosswalk of data elements

Columns:
- **In 77?** gives the existing point numbers.
- **New point(s)** uses the checklist's style: `source.element[.md|.tvd]`.
- **Where:**
  - **ON**: must appear on the diagram.
  - **WITH**: accompanying documentation.
  - **FILE**: elsewhere in the project, NOI or well file.
- **Applies** says whether the element binds the sample: Y (yes, for S1/S6 footprint), P&A (at abandonment), G (guidance only), N/A (UGS, WST), CT (state contract template only).

### 3.1 Elements already in the 77 (sources confirming)

| Element | Sources | In 77? | Notes |
|---|---|---|---|
| Operator, lease, well number, API | S1 (a)(1), S6, S9 (A), S18 (a, b), S17 | 1–4 | S18 lacks operator and lease; S9 says "Operator" |
| Spud date | S1 (a)(2), S6, S9, S18 (h) | 5 | |
| Ground elevation | S1 (a)(3), S6, S9, S18 (d) | 6 | |
| Reference elevation (RF/KB) | S1 (a)(4), S6, S9, S18 (e) "KB height" | 7 | |
| Base of freshwater MD/TVD | S1 (a)(5), S6, S18 (k), S22 FAQ, S23 | 8, 52 | S22: required even in exempted zones, so "N/A" is still an answer but a weak one |
| Base of lowermost USDW MD/TVD | S1 (a)(6), S6, S23, S24; S9 (F) "≤10,000 mg/L TDS" is the same concept | 9, 53 | |
| Casing size, grade, connection, weight | S1 (a)(7), S6, S9 (G), S11 (i), S16 "sizes", S17, S18 (m), S20 | 10–13 | |
| Shoe, stub, liner-top MD/TVD | S1 (a)(8), S6, S9 (I), S11 (ii), S18 (m) "run depths" | 14–16, 54–56 | |
| Perforations, intervals, open hole, WSO holes, cement ports, cavity shots, cuts (MD/TVD) | S1 (a)(9), S6, S9 (J), S11 (iii), S16 "perforation locations", S18 (p), S23 "perforated/slotted" | 17–23, 57–63 | |
| Casing damage type and extent; junk/fish type and extent | S1 (a)(9), S6, S9 (J) "casing damage, top of junk or fish", S11 (iii), S20 (§ 1724(a)(10); PRC § 3213), S23, S24 | 24–27, 64–65 | |
| Other flow/integrity feature | S1 (a)(9), S6, S9 (J) | 28 | **Depth not split; see 3.2 G1** |
| SSSV, packers, GLM | S1 (a)(10), S6, S9 (H), S20 (§ 1724(a)(3)) | 29–31 | |
| Hole diameter and depth MD/TVD | S1 (a)(11), S6, S9 (K), S11 (iv), S18 (l), S20 (§ 1724(a)(5)) | 32–33, 66 | PRC § 3230(a) "total depth" = deepest hole depth |
| Cement plugs: ID, top, bottom MD/TVD | S1 (a)(12), S6, S9 (L), S11 (v), S14 "including plugs", S16 "cement plug depths inside casing", S18 (q), S23, S24 | 34–36, 67–68 | |
| Cement fill behind casing: ID, top, bottom MD/TVD | S1 (a)(13), S6, S9 (M), S11 (vi), S16 "location of the cement outside casing", S18 (o), S23 "annular seal … squeezes" | 37–39, 69–70 | Squeezes: treat as cement fill (Q6) |
| Fluid type and density between plugs | S1 (a)(14), S6, S9 (N), S11 (vii) | 40–41 | |
| Formations, zones, markers (names, depths MD/TVD); injection zone and confining layer top/bottom | S1 (a)(15), S6 ("if applicable"), S9 (O), S11 (viii), S18 (k) "tops of hydrocarbon zones", S23 "all oil and gas zones" | 42–51, 71–77 | |
| Multiple boreholes / entire history | S1 (c), S6 (c), S9 (a)(6), (Q), S11 (xi), S23, S24 | coverage rule | Not a point; applied across points |
| MD and TVD for all (a) depths | S1 (d), S6 (d), S9 (a)(2), S18 (i) | split into 26 pairs | |

### 3.2 New elements: candidate atomic points

| ID | Element | Source(s) | New atomic point(s) | Where | Applies |
|---|---|---|---|---|---|
| G1 | Depth of "any other feature that influences flow … or may compromise mechanical integrity" | S1 (a)(9) "Depths of … any other feature" + (d); S6; S9 (J) | `(a)(9).other_integrity_feature_depth.md`, `.tvd` | ON | **Y** (gap within 1724.7.1 itself) |
| L1 | Diagram title | S2 § 1724.7(c): diagrams required in (a) "shall be clearly and appropriately labeled, such as to title, scale, and purpose" | `1724.7(c).diagram_title` | ON | **Y** (S1 footprint; Q1) |
| L2 | Scale (an explicit "not to scale" counts as an answer) | S2 (c); S5 § 1772.1.2(f) "scale and purpose"; S8 (c) | `1724.7(c).diagram_scale` | ON | **Y** |
| L3 | Purpose (e.g., current condition, proposed) | S2 (c); S5 (f); S8 (c); S18 "current and proposed condition" | `1724.7(c).diagram_purpose` | ON | **Y** |
| P1 | Casing interval: top of each string (MD/TVD) | S16 "casing intervals and sizes"; S17 Feature Top MD (required field); S20 § 1724(a)(2) "top, bottom"; S18 (m) "run depths" | `pa.casing_top.md`, `pa.casing_top.tvd` | ON (P&A schematic) | **P&A** (G) |
| E1 | Equipment depths (packers, SSSV, GLM) MD/TVD | S1 (a)(10) "information regarding equipment" with (d); S10 "location of packers … setting depths"; S20 § 1724(a)(3) "type and location of packers" | `(a)(10).equipment_depth.md`, `.tvd` | ON | Ambiguous (Q2), **not counted** |
| C1 | Fluid contacts | S2 (c) "clearly identify … zones, contacts" | `1724.7(c).contacts` | ON | Ambiguous (Q1), **not counted** |
| T1 | Latitude and longitude | S18 (c) | `ct.latitude`, `ct.longitude` | ON | CT |
| T2 | Well type | S18 (f) | `ct.well_type` | ON | CT |
| T3 | Well status | S18 (g) | `ct.well_status` | ON | CT |
| T4 | Plug-back TD | S18 (j) | `ct.pbtd.md`, `ct.pbtd.tvd` | ON | CT |
| T5 | Cement volume pumped per casing job | S18 (n); S9 (P); S11 (x); S1 (b)(2) as WITH | `ct.cement_volume` | ON (CT, UGS) / WITH (1724.7.1) | CT |
| T6 | Cement returns to surface recorded | S18 (n) | `ct.cement_returns` | ON | CT |
| T7 | Top-of-cement determination method (calculated "ETOC" vs. measured "CBL") | S18 (o); S9 (M) "with method of determination"; S11 (vi) | `ct.toc_method` | ON | CT; N/A (UGS, WST) |
| T8 | Perforation status open/closed | S18 (p) | `ct.perf_status` | ON | CT |
| U1 | Base of ≤3,000 mg/L TDS groundwater MD/TVD | S9 (E) | `1726.4.1(a)(1)(E).tds3000_base.md`, `.tvd` | ON | N/A |
| U2 | Tubing size, weight, grade, connection | S9 (G); S10 | 4 points | ON | N/A (but S20 § 1724(a)(3) keeps tubing in the well record) |
| U3 | Patches (depth MD/TVD) | S9 (J); S10 | 2 points | ON | N/A |
| U4 | Cement plug emplacement date(s) | S9 (L) | 1 | ON | N/A |
| U5 | Plug method of determination; fill method of determination | S9 (L), (M); S11 (v), (vi) | 2 | ON | N/A |
| U6 | Slurry data on the diagram (type, additives, volume, density, yield) | S9 (P); S11 (ix), (x) | 5 | ON (UGS, WST) | N/A (already WITH under 1724.7.1(b): DB points 54–58) |
| U7 | Wellhead and valve assembly: model; pressure rating | S9 (R); S10 | 2 | ON | N/A |
| U8 | Primary and secondary mechanical barrier elements | S9 (a)(5); PRC § 3180 | 2 | ON | N/A |
| U9 | Gas storage zone top/bottom MD/TVD | S9 (O) | 4 | ON | N/A |
| W1 | WST zone top/bottom MD/TVD | S11 (viii) | 4 | ON | N/A (dormant) |

### 3.3 Accompanying documentation and file-level elements

| Element | Source(s) | Already stored? | New item(s) | Where | Applies |
|---|---|---|---|---|---|
| Cement yield and calculation steps; slurry inputs (volume, density, yield, type, additives); wellbore path MD, inclination, azimuth | S1 (b), S6 (b) | DB records 52–61 (10) | none | WITH | Y |
| Licensed-professional cover statement; signatures/stamps, or the name and signature of the responsible preparer | S2 § 1724.7(d) | no | `1724.7(d).cover_statement`, `1724.7(d).signature_or_stamp` | WITH (submission) | Y (project submissions) |
| Proposed-condition diagram | S18; S19; S16 (drill "proposed wellbore schematic") | no | `pa.proposed_diagram` | WITH (NOI) | P&A |
| NOI total depth | S14 PRC § 3230(a); S17 | no | `pa.noi_total_depth` | WITH (NOI form) | P&A |
| Directional survey bottom-hole location and surface location | S9 (a)(3) | no | 2 | WITH | N/A (UGS) |
| AOR compendium: API, wellbore path, TD, completion intervals for every AOR well | S3 § 1724.7(a)(1)(C)(i) | no | (4, project-level) | FILE | Y, not per diagram |
| Electronic format; flat file allowed | S1 (e); S9 (a)(4), (b); S2 (c) "digitally" | n/a | none (format) | FILE | Y |
| Log, core record, history: casing condition, tubing, packers, tests, cementing date/volume/pressures, junk, explosives, acid | S20; S21 | n/a | none | FILE (well record) | Y |
| Cementing records / cement evaluation log | S4 § 1724.8(a)(1) | n/a | none | FILE | Y (UIC) |
| NOI wellbore-construction features (ID, new/used, pulled, dates, burst, cementing company) | S17 | n/a | none | FILE (NOI form) | P&A / all NOIs |
| Updated diagram within 60 days of well work | S10 | n/a | none (timeliness, not completeness) | FILE | N/A (UGS) |

---

## 4. Proposed counts

On-diagram points that bind the sample (Y and P&A rows in 3.2):

| Group | Points |
|---|---|
| G1: other-feature depth MD/TVD (gap inside § 1724.7.1(a)(9) + (d)) | 2 |
| L1–L3: title, scale, purpose (§ 1724.7(c); § 1772.1.2(f)) | 3 |
| P1: casing top MD/TVD (P&A guidance S16; § 1724(a)(2)) | 2 |
| **Total new on-diagram points** | **7** (77 → **84**) |

Variants:
- **Strict regulation only** (G1 + L1–L3, dropping P1, which is guidance): **5** (→ 82).
- **Same text only** (G1 only, fixing the existing § 1724.7.1 instrument): **2** (→ 79).
- **Adding the state abandonment contract list** (T1–T8: 2 + 1 + 1 + 2 + 1 + 1 + 1 + 1): **+10** (→ 94). Not binding on operator NOIs.
- **Ambiguous elements** E1 (2) and C1 (1): **+3** if resolved as required.
- **Not applicable** UGS (U1–U9): 24 points, plus WST zone (4), as reference only.

Accompanying documentation:
- **4 new items** that apply: 2 from § 1724.7(d) cover page, plus proposed diagram and NOI TD at P&A. These are in addition to the 10 § 1724.7.1(b) records already in the DB, giving 14.
- UGS adds 2 (BHL, surface location), not applicable.
- The AOR compendium (4) is project-file level and is not proposed for the per-diagram instrument.

---

## 5. Open questions and risk

### 5.1 Open questions

1. **Q1. Does § 1724.7(c) labeling bind each casing diagram, and what is "contacts"?** (c) covers "all maps, diagrams, and exhibits required in subdivision (a)". Casing diagrams are required at (a)(1)(C)(iii), so a literal reading says yes. "Title, scale, and purpose" are "such as" examples, not an exhaustive list. "Contacts" may mean fluid contacts (OWC/GOC) or geologic contacts already covered by (a)(15).
2. **Q2. Depth-bearing scope of (a)(9) "any other feature" and of (a)(10) equipment.** (a)(9) begins "Depths of …", so the other-feature item should arguably carry MD/TVD (G1). The current 77 treat point 28 as non-depth. (a)(10) asks only for "information regarding equipment", so whether (d) MD/TVD applies to equipment setting depths is unclear. The UGS NTO treats "setting depths" as diagram content.
3. **Q3. Which sampled wells are actually in a UIC AOR?** Only the 7 injectors are certainly within § 1724.7.1. For the 22 producers and W02, applicability rests on AOR membership, which could be checked in WellSTAR (UIC project well lists or Project Approval Letters). The scenario framing (pre-abandonment check under PRC § 3230) does not itself impose § 1724.7.1.
4. **Q4. TVD reference.** § 1722.2 defines casing-program depths as TVD below ground level, while diagrams use RKB/KB. This affects only the reading of values, not presence scoring.
5. **Q5. P&A content.** PRC § 3230 asks only for TD and the "complete casing record … including plugs". The four-item P&A schematic list is on a CalGEM web page (guidance). The 17-item list is in a DOC contract for state abandonments. Neither is a regulation.
6. **Q6. Cement squeezes** (S23) are not named in § 1724.7.1. Treat them as cement fill (a)(13) or as a feature under (a)(9)?
7. **Q7. CalGEM Appendix C "Casing Diagram Information".** This UIC guidance appendix is email-only (filerequest `UIC_APP_C.pdf`) and was not obtained. It may contain CalGEM's own content list. Separately, PROVENANCE.md line 154 says the MOA UIC Checklist has no diagram passage, but it has (S23). Correct this in PROVENANCE.md.
8. **Q8. LII currency.** The new CCR copies are from LII. Confirm §§ 1722, 1724, 1724.1, 1724.8 and 1783.1 against Westlaw before citing.

### 5.2 Risk of enlarging the instrument (final proposal due Dec 4, 2026; 16 days)

- **Prompts.** All three prompts hard-code "77-point" and "Return exactly 77 rows". A new checklist v3 needs a new dry run, which is already pending under the current design.
- **DB.** `casing_specs.sql` holds 87 records (77 + 10). Changes needed:
  - Add 7 `spec_requirements` rows plus 4 WITH rows.
  - Update the scoring view denominator.
  - Re-run the W01 human-review workbook (`build_w01_review_workbook.py`), which is built on 77.
- **Human review.** One reviewer, 30 diagrams: +7 points per diagram is +210 judgments (2,310 → 2,520).
  - L1–L3 are fast to score.
  - G1 needs judgment about what counts as an "other feature".
  - P1 needs per-string top depths.
  - The W01 review already done must be redone or extended.
- **Proposal text and equations.**
  - Eqs. 1 and 2 use ÷77. Make the denominator symbolic (N = 84) or keep 77 as the primary measure.
  - Update Table 3, the "25 non-depth / 26 MD / 26 TVD" sentence, the 87-record text, and sampling-plan §4. That section still speaks of 15 items and 450 judgments.
  - The sources must enter the reference list.
- **Validity.**
  - L1–L3 and P1 come from labeling rules and guidance, not § 1724.7.1(a). Mixing them into a single completeness score weakens the claim that the score measures § 1724.7.1 completeness.
  - P&A items apply to a future NOI, not to the existing diagram.
- **Suggestion (for the student to decide).** Keep the 77 as the primary instrument for the Dec 4 proposal. Do one of the following:
  - Add only G1 (2 points, the same regulation; → 79), if a reading of Q2 supports it.
  - Report the 5–7 extra points as a secondary "extended completeness" score.
  - Report them as a limitation and future work.

  Any change should be frozen before the 270 runs begin.
