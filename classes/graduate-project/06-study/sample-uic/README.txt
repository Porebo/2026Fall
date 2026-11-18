UIC CASING DIAGRAM SAMPLE (14 CCR 1724.7.1)
Sampling plan and screening record
Version 1.0, November 18, 2026

This folder holds a new random sample of 30 casing diagrams, all from wells
governed by 14 CCR 1724.7.1. It reuses the method of ../sample/ (sampling plan
v1.5): sort the frame by API, shuffle once with a fixed seed, screen in that
order in WellSTAR, include the first 30 eligible wells. The earlier sample
(../sample/, W01-W30) is unchanged.

Retrieval date for everything here: November 18, 2026.


1. FILES
========

  README.txt               this plan and record
  frame-summary.csv        frame counts by filter step, well type, status, district
  screening-log.csv        all 22,603 frame wells in random order; rows 1-135
                           screened (outcome, project, diagram, checksum)
  screening-raw/           raw WellSTAR results per batch (JSON), and
                           overrides.json (decisions made after viewing a file)
  diagrams/U01-U30.pdf     the 30 diagrams, exactly as downloaded
  pdf-quality-profile.csv  input-quality measures (same script and definitions
                           as ../sample/sample-quality-evaluation.txt, section 3)

Scripts (../../scripts/):
  select_sample_uic.py      builds the frame and the random order
  classify_uic_screening.py applies the eligibility rules to screening-raw/
  profile_pdf_quality.py    run as: python profile_pdf_quality.py ../06-study/sample-uic U
  WellSTAR steps: same as ../../calgem/PROVENANCE.md section 7.4 and
  wellstar_wellbore_diagrams.js, run through the Playwright MCP browser, with one
  added step (open "Current Associated Projects" on the Well Detail page).


2. POPULATION AND FRAME
=======================

Target population: onshore California wells that are injection wells in an
approved CalGEM UIC (Class II) project, status Active or Idle, whose casing
diagram in WellSTAR is dated on or after April 1, 2019 (operative date of
14 CCR 1724.7.1) and is a legible PDF.

Frame file: CalGEM "Oil and Gas Wells Table, California" (AllWells), portal
item 0d30c4d9ac8f4f84a53a145e7d68eb6b, downloaded November 18, 2026 from
https://gis.conservation.ca.gov/portal/sharing/rest/content/items/0d30c4d9ac8f4f84a53a145e7d68eb6b/data
and kept (git-ignored) in ../../05-data/calgem/all-wells-2026-11-18/.
(The November 13 copy named in PROVENANCE.md section 12 was not on this
computer, so the current nightly file was used.)

  AllWells.zip           7,784,700 bytes  SHA-256 AEAEAFA6E496A4DDBC93A3451EBF52A4ABED9413E8ABAD6346C57FD91A1AF6BB
  AllWells_20261118.csv 58,862,528 bytes  SHA-256 2D2ABA1A9845B0A8FC8298561D032F7E2E40C480A1F93C3B81C7C1057B73B507
  TableMetadata.htm        179,266 bytes  SHA-256 5EBE5853B2B5BB221B468FDAEAB447432221249E21285171A9DB7968B01695F7 (same as Nov 13)

Filters, in order (one row per distinct 10-digit API):
  All wells in the file                                     242,636
  WellStatus = Active or Idle                                83,498
  WellType in the injection codes below                      23,013
  Offshore removed (CountyName ends in "Offshore")              410
  FRAME, N                                                   22,603
                                     (Active 15,231; Idle 7,372)

Injection well-type codes included (GIS-metadata-ReadMe.pdf labels):
  SC Cyclic Steam 9,824   SF Steamflood 5,812   WF Waterflood 5,309
  WD Water Disposal 1,443  PM Pressure Maintenance 112  GD Gas Disposal 82
  INJ Injection 16         AI Air Injection 5
Basis: 14 CCR 1720.1(p) defines an underground injection project as injection
for enhanced recovery, disposal, storage of liquid hydrocarbons, pressure
maintenance, or subsidence mitigation, naming waterflood, steamflood, cyclic
steam and disposal injection; 1720.1(b) defines a cyclic steam well as an
injection well. Cyclic steam is therefore included.
Excluded codes: GS gas storage (1720.1(p) excludes UGS; governed by 1726.4.1),
OG, DG, GAS, OB, DH, CH, WS (water source: a supply well), Multi, UNK, STR.
LG (liquid gas storage) has no Active or Idle wells.

The frame file has no project-membership field. Membership is therefore
checked per well in WellSTAR during screening (rule c below).


3. SAMPLING METHOD
==================

Sort the frame by API; shuffle once with Python random.Random(20261118).shuffle;
screen strictly in that order until 30 wells are INCLUDED. Rows 1-30 are
labeled Primary, the rest Replacement, as in ../sample/. The seed and order were
fixed before any well was screened.

  Seed: 20261118
  SHA-256 select_sample_uic.py:      6A6E8D8D8C313D421DE77493B79E9F17B39AA01A88233B4E594B2CBC50376D1E
  SHA-256 screening-log.csv as generated, before screening:
                                     E0CEF3D2BE972CEB5966A9C1D34984BE30C148658438335AF5ABACC00E585FC6


4. ELIGIBILITY AND OUTCOME CODES
================================

A screened well is INCLUDED when all hold:
  a. The 10-digit API is found in WellSTAR.                    NOT_FOUND
  b. WellSTAR status is Active or Idle.                        STATUS_CHANGED
  c. WellSTAR "Current Associated Projects" lists a project with
     Program = UIC, Planned Use = Injector, and Project Status Active or
     Suspended (approved). AOR-only, Rescinded, Terminated, Proposed, or no
     project does not qualify.                                 NOT_UIC_INJECTOR
  d. At least one document of type "Wellbore Diagram".         NO_DIAGRAM
  e. At least one not describing planned work (description or file name
     containing proposed, abandonment, sidetrack, ST, or permit, as in
     ../sample/ plan v1.1).                                    PROPOSED_ONLY
  f. Such a diagram has a WellSTAR Relevant Date on or after
     04/01/2019.                                               PRE_RULE_ONLY
  g. Such a diagram is a PDF file.                             NOT_PDF
  h. It downloads and is legible.                    DOWNLOAD_FAILED / UNREADABLE
Diagram used: among diagrams meeting e-g, the latest Relevant Date; ties to a
description naming "Current", then the highest Document ID. The diagram date
recorded is the WellSTAR Relevant Date.
NOT_NEEDED: eligible, but screened in the same batch after the 30th INCLUDED.
Stop rule: 300 wells screened (not reached).


5. RESULTS
==========

Screened November 18, 2026: rows 1-135 (30th INCLUDED at row 132).

                      rows 1-132   rows 133-135
  INCLUDED                30            -
  NO_DIAGRAM              73            2
  NOT_UIC_INJECTOR        26            -
  PRE_RULE_ONLY            2            -
  PROPOSED_ONLY            1            -
  NOT_PDF                  0            -
  STATUS_CHANGED           0            -
  NOT_FOUND                0            -
  DOWNLOAD_FAILED          0            -   (2 first attempts returned a web page;
  UNREADABLE               0            -    both succeeded on retry)
  NOT_NEEDED               -            1   (row 133, Doc 1213788)
  Total screened         132            3   = 135

NOT_UIC_INJECTOR (26): 17 wells with no associated project, 9 listed only as
Area of Review wells or with only a rescinded/terminated injector designation.
So 26 of 132 (20%) frame wells coded as injectors in AllWells are not current
UIC project injectors in WellSTAR.

Availability among UIC-project injectors: 30 / 106 = 28.3% (95% CI 19.7% to
36.9%).

Description of the sample (reported, not controlled):
  Well type:  Cyclic steam 13, Steamflood 8, Waterflood 5, Water disposal 4
  Status:     Active 24, Idle 6 (AllWells and WellSTAR agree)
  District:   Central 27, Northern 2, Southern 1
  Fields:     13 distinct (Midway-Sunset 7, Belridge South 6, Cymric 5, ...)
  UIC projects: 27 distinct project listings (UIC_Project column)
  Diagram dates: 2019 (2), 2020 (3), 2021 (1), 2022 (13), 2023 (4), 2024 (1), 2025 (6)
  Input type: Native 21, Mixed 5, Scanned 4 (U02, U17, U18, U22). All viewed; all legible.

Overlap with ../sample/: none. Of the 30 W wells, 10 are in this frame (W03,
W04, W05, W07, W08, W12, W15, W27, W29, W30) at random-order rows 2,532 to
18,766, far beyond row 135. W02 is type OB and not in the frame.


6. DECISIONS MADE DURING SCREENING (rules fixed before; applied as follows)
==========================================================================

- Rule g (PDF) was added when two selected diagrams turned out to be JPEG
  images (rows 58 and 115; Doc 1439336 and 1465795). The latest PDF diagram
  of each well, also dated after 04/01/2019, was used instead (U15 Doc 1241445,
  U26 Doc 1355970). No well was excluded by this rule.
- Row 74: all three diagrams are titled "Sidetrack Permit 7037494" -> PROPOSED_ONLY.
- U03 (Doc 759727, "Rework WBD"): diagram marked Current; kept.
- U16 (Doc 360731, file "WWD10-27 Install Inner Csg"): shows existing
  completion, not labeled proposed; kept.
- U21 (Doc 1360209, "Original WBD"): the same-date "ST WBD" (Doc 1360210) was
  set aside by the sidetrack wording rule; the diagram used shows both the
  original hole and the 2025 sidetrack.
- U23 (Doc 648598): page 1 "Redrill - 02" (current), page 2 "Proposed - 02".
  Kept whole; the file is not described as proposed. Analysts should score
  page 1.
- The WellSTAR data disclosure was accepted in the automated browser at the
  start of the session.
These are recorded per row in screening-log.csv (Notes) and in
screening-raw/overrides.json.

Checksums of the 30 files are in screening-log.csv (SHA256 column).
