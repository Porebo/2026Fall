# Instructions for an AI assistant: scoring casing diagrams U01–U30

Project root: `classes/graduate-project/`. Read this whole file before doing anything.

## 1. What the study does

A master's study measures the completeness of California casing diagrams against 14 CCR § 1724.7.1. Each diagram is scored on 90 atomic data points (checklist v4.2). The human reviewer of record is **Lester S. Carcamo**. You prepare the scoring; Lester checks every call before it is final.

## 2. Hard rules

- **Study sample = U01–U30 only** (`06-study/sample-uic/diagrams/`). W01–W30 (`07-out-of-study/`) are out of study: never read, score, edit, or add database rows for them.
- Never overwrite a diagram PDF (`Unn.pdf`).
- Never edit versioned instrument files (checklist v2–v4.2, prompts). A change to the rules = a new version + a dated decision line in `02-plan/proposal-plan.md`.
- Back up `04-literature/casing-analysis/casing_specs.db` before any write.
- List every uncertain call for Lester; do not hide anything you were unsure of.

## 3. Instrument

- Checklist: `06-study/design/prompts/casing-diagram-atomic-checklist-v4.2.txt` (authoritative wording).
- Regulation text: `calgem/Casing Diagrams, 2026, Cal. Code Regs. tit. 14, 1724.7.1, Westlaw.txt`.
- Points 1–78: subdivisions (a) and (d) (52 MD/non-depth + 26 TVD). Point 32 = (a)(10) other equipment (tubing, pumps, rods).
- Points 79–90: subdivisions (b) and (c). Point 81 = cement job identification. Point 90 = borehole designation (conditional).

## 4. Scoring rules (presence only)

1. **MET** = the diagram supplies any answer: a value, "none", "N/A", or another explicit word. **MISSING** = blank label or not mentioned. Never judge truth or quality.
2. MD and TVD are separate points. A depth given only in MD leaves the TVD point MISSING.
3. Repeated structures (casings, cement jobs, perforations, boreholes): MET only if every instance shown has an answer.
4. A heading over unrelated content does not answer a point (e.g., tubing listed under "PLUG DETAILS" is not a cement plug).
5. Points 79–89: MET if the information is on the diagram **or** the diagram states it accompanies separately ("see cement report", "directional survey attached").
6. Sack count satisfies slurry volume (82). Any stated deviation ("Deviated (15° to 30°)", a max angle) satisfies inclination (88) only, not MD path or azimuth.
7. Point 90 is **NOT_APPLICABLE** when only one borehole is shown; the denominator then drops from 90 to 89. No other point may be NOT_APPLICABLE.
8. Liner tops and stubs answer points 16/15. Full-string casing tops are not scored and are not excess data.

**Completeness (Equation 1)** = points MET ÷ applicable points (90, or 89 when point 90 is not applicable).

## 5. Classify content that is not a scored point

| Category | Frame on figure | Examples |
| --- | --- | --- |
| Excess data (present, not required) | red, badges E1, E2… | well location (field, county, PLSS, lat/long), KB–ground height, rig-release and TD dates, "Operated?" flag, perforation dates, perforation shot density, PBMD, flag joint, intermediate casing-joint bottoms |
| Document provenance (not required, not excess) | dotted near-black | preparer initials and date, print timestamp, software web address, page number |
| Supports another requirement (not scored) | dashed slate + citation tag | only if something cites a rule outside the 90 points, e.g., well type → § 1724.7(a)(3)(D) |

Never use the word "muda" on figures; use "Excess data". New item types: decide by these examples and flag them for Lester.

## 6. Outputs per diagram Unn

1. **Figure** (model: `06-study/sample-uic/diagrams/U01.svg`), US Letter, 0.5-in margins:
   - Header line 1: `Casing Diagram Unn · Checklist v4.2 · Final score X% (M of A applicable points MET)`
   - Header line 2: `Scored by Lester S. Carcamo · <Month D, YYYY>`
   - No "provisional", "Claude", or AI wording anywhere.
   - Left: pill columns MD | TVD (non-depth points have an empty TVD cell), block for 79–90. MET pills colored by requirement group with number badges; MISSING pills grey; N/A pill dashed.
   - Right: the diagram image; each MET datum framed in its group color with the same number badge and a connector line from its pill.
   - Below: completeness block first (Equation 1 with steps), then legend, Excess data list with counts, provenance list.
   - Save `06-study/sample-uic/diagrams/Unn.svg` and `Unn.png`, and a Letter PDF at `06-study/design/figures/Unn-atomic-map.pdf`.
2. **Decision record** `06-study/sample-uic/reference/Unn.json` (same schema as `U01.json`): well identity, checklist version, reviewer, date, score, all 90 points (status, evidence text, page + bbox for MET), non-scored items by category.
3. **Database**: load the JSON with `scripts/load_reference_json.py` (idempotent; re-running replaces that diagram) and confirm the database score equals the figure score.
4. **Home page**: `home-graduate-project.html` already links U01–U30 diagrams; add links to new figures if missing.

## 7. Report back to Lester

Well identity, score breakdown ((a)/(d) MET of 78; (b)/(c) MET of 11 or 12), the excess-data list, and every uncertain call with the reason. He reviews before the result counts as final.
