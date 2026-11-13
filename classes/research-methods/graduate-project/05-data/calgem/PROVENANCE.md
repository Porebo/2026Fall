# Data Provenance: CalGEM Oil and Gas Well Data

**Project:** MS Information Science master's project, research proposal (Lester S. Carcamo)
**Folder:** `classes/research-methods/graduate-project/05-data/calgem/` (was `classes/research-methods/w10/data/calgem/` until November 12, 2026)
**Record created:** November 10, 2026
**Times:** Pacific Standard Time (UTC−8)

**Relocation, November 12, 2026.** The project folder was reorganized. Files were moved, never edited (checksums below are unchanged). Where this record says "this folder" or names a subfolder, read it as the new location below. Paths are relative to `graduate-project/`.

| Was (under `w10/data/calgem/`) | Now |
|---|---|
| CSV, `.xls`, code PDFs, GIS readme, this record | `05-data/calgem/` |
| `enforcement-orders/` | `05-data/calgem/enforcement-orders/` |
| `wellbore-diagram-sources/` | `04-literature/regulatory/wellbore-diagram-sources/` |
| `nov-sources/` | `04-literature/regulatory/nov-sources/` |
| `wellbore-diagrams/*.pdf` (10 Ventura wells) | `06-study/pilot-ventura/` |
| `wellbore-diagrams/scenario-business-need.txt`, `casing-diagram-specification.txt` | `06-study/design/` |
| `wellbore-diagrams/prompts/` and the four `*-copy-and-paste.txt` files | `06-study/design/prompts/` |
| `sample/` | `06-study/sample/` |
| `N-*-prompt/runs/` | `06-study/runs/N-*-prompt/` |
| `*.py`, `*.js` | `scripts/` |

The full move list is in `graduate-project/_reorg-log.txt`.

---

## 1. Publisher

All files were published by the California Department of Conservation, Geologic Energy Management Division (CalGEM), formerly the Division of Oil, Gas, and Geothermal Resources (DOGGR). All are public records, obtained at no cost and without an account or login.

**Publisher's disclaimer (summarized):** the Department provides the data for informational purposes and makes no warranty, expressed or implied, of accuracy, completeness, or fitness for a particular purpose. Data may be updated, amended, or deleted without notice. Full text: Department of Conservation, Conditions of Use (https://www.conservation.ca.gov).

---

## 2. How the files were obtained

| Step | Date and time | Action |
|---|---|---|
| 1 | Nov 10, 2026, about 11:10 PM | Downloaded the well metadata PDF directly from the CalGEM website (Group A below) |
| 2 | Nov 10, 2026, 11:12 PM | Requested five files through the CalGEM File Request system, https://filerequest.conservation.ca.gov/, searching the keyword `production_injection_data`. The system sends requested files by email; the site states this is required "until it is updated to ADA standards" |
| 3 | Nov 10, 2026, 11:12–11:13 PM | Received the email at 11:12 PM and downloaded the files through its links (Group B below). Details of the email are below this table |
| 4 | Nov 10, 2026 | Moved all files into this folder, renamed two of them (section 4), and computed SHA-256 checksums |

**Delivery email (step 3):**

| Item | Value |
|---|---|
| From | DOC File Request, `no-reply.filerequest@conservation.ca.gov` |
| Subject | Your Requested DOC File |
| Received | Nov 10, 2026, 11:12 PM |
| Files listed | `prod & inj reporting codes.pdf`, `status and type codes.pdf`, `Report File Definition.xls`, `2021CaliforniaOilAndGasWells.xls`, `2021CaliforniaOilAndGasWellMonthlyProduction.csv` |
| Link expiry | 14 days from sending, per the email ("expires in 14 days") |
| Accessibility | The email includes an Alternative Means of Access Notice with the contact `DOCAccessibility@conservation.ca.gov` |

The five files listed in the email are the five files requested in step 2.

Navigation path to the File Request system: CalGEM, Online Data Tools (https://www.conservation.ca.gov/calgem/Online_Data), "Well Production and Injection Summary Reports."

The File Request system identified the requested files with these internal IDs: 36919, 36920, 2813663, 2825828, 2901017. Which ID belongs to which file was not recorded.

---

## 3. File inventory

### Group A: downloaded directly

| File in this folder | Source URL | Bytes | SHA-256 |
|---|---|---|---|
| `GIS-metadata-ReadMe.pdf` | https://www.conservation.ca.gov/calgem/maps/Documents/GIS-metadata-ReadMe.pdf | 142,984 | `41E1C4CE54A81C1E42BE010C9CA27E388EE1C1BDCCBC50FBA604621CDB6BF725` |

**Contents:** "Oil and Gas Wells Metadata," 3 pages. It defines 21 well attributes and their allowed values (well status, well type, base meridian, GIS source, and others). It describes CalGEM's current WellSTAR well data. The PDF carries no publication date.

### Group B: requested through the File Request system

| File in this folder | Bytes | SHA-256 |
|---|---|---|
| `2021CaliforniaOilAndGasWells.csv` | 41,347,512 | `ADCDEFD1B3659FC08E3472DF77AE458EF246C01334B560FF1128FCF4CE4804A2` |
| `2021CaliforniaOilAndGasWellMonthlyProduction.csv` | 92,571,772 | `2826F0743408BF177A037BC062C90CF30EA773CDF7393C02400E59D361348B7A` |
| `Report File Definition.xls` | 26,112 | `4ADDE61955E0B1E3DE2BF8D6A5C09C54499CDC3F0A6042AFD6149FEAB6309D18` |
| `prod & inj reporting codes.pdf` | 63,063 | `B9DCC67E4801B83F3B0C81156F3048B06F2C856D82B912D5F60CF9F2AD85F923` |
| `status and type codes.pdf` | 97,059 | `0BD54552B62BE7FDDC349F8A51C775A28CF3091F2DFEAB08FCBA47A01F97369F` |

**Contents:**

- **`2021CaliforniaOilAndGasWells.csv`:** well records, 221,945 rows and 23 columns; 197,169 distinct API numbers. One row per well and producing pool.
- **`2021CaliforniaOilAndGasWellMonthlyProduction.csv`:** monthly production reports (report type OG110), 1,053,051 rows and 19 columns, January to December 2021, covering 88,529 wells.
- **`Report File Definition.xls`:** field layout of CalGEM's older fixed-width report file ("NEW Report File Version 2"). Its monthly fields correspond to the production CSV's columns.
- **`prod & inj reporting codes.pdf`:** production and injection reporting codes (method of operation, water disposition, reason a well is not producing, and injection codes). Dated "Created 9/25/2014."
- **`status and type codes.pdf`:** well status and well type codes, one page. It carries no date.

The row and column counts above include no header rows. They were counted on November 10, 2026.

---

## 4. Changes made to the files

The contents of every file are unchanged from what CalGEM delivered. Only names and locations changed.

| Original name | Name in this folder | Reason |
|---|---|---|
| `2021CaliforniaOilAndGasWells.xls` (saved by the browser as `2021CaliforniaOilAndGasWells (1).xls`) | `2021CaliforniaOilAndGasWells.csv` | The file is comma-separated text, not an Excel workbook. The extension was corrected and the browser's duplicate marker "(1)" was removed |
| `gis-metadata.pdf` (temporary download name) | `GIS-metadata-ReadMe.pdf` | Restored the publisher's file name from the source URL |

The checksums in section 3 were computed after these changes. Because only names changed, they also match the files as delivered.

---

## 5. Known characteristics of the data as delivered

These were observed in the original files before any errors were introduced for the study. They are recorded so that they are not mistaken for injected errors.

- **Production rows with no matching well:** 3,132 rows carry an API number that does not appear in the wells file.
- **Duplicate production keys:** 515 combinations of API number, field, area, pool, and report date appear more than once.
- **Duplicate well rows:** 83 rows in the wells file repeat an API, field, area, and pool combination.
- **Missing value:** one well has a blank base meridian (`BM`).
- **The documents disagree with each other and with the data:**
  - **API number length:** 12 digits in the 2021 files, 10 digits in the current WellSTAR well layer, 8 digits in `Report File Definition.xls`.
  - **Status and type codes:** `status and type codes.pdf` uses single-letter status codes (A, I, P, and others), but the 2021 data uses words (Active, Idle, Plugged, PluggedOnly, Abeyance). Several well types in the data (SC, UNK, Multi, INJ, GAS, DH) are missing from that PDF. `GIS-metadata-ReadMe.pdf` matches the data's wording more closely.

---

## 6. Wellbore diagram sources (now `04-literature/regulatory/wellbore-diagram-sources/`)

**Purpose:** documents that state what a wellbore (casing) diagram must contain or show how CalGEM uses diagrams.

**How obtained:** found on November 10, 2026, about 11:20 PM, through the Department of Conservation site search (https://www.conservation.ca.gov/search) for the phrase "wellbore diagram," and through CalGEM's "For Operators – Underground Injection Control" page and its "Laws and Rulemaking" page. Each file was downloaded directly from the URL shown, at 11:21 PM, with no login or request form. File names are the publisher's names taken from the URLs; contents are unchanged.

All URLs begin with `https://www.conservation.ca.gov/`.

| File | Path after the base URL | Pages | Bytes | SHA-256 |
|---|---|---|---|---|
| `Final Text of the UIC Regulations (Clean).pdf` | `calgem/Documents/UIC%20regulations/Final%20Text%20of%20the%20UIC%20Regulations%20(Clean).pdf` | 32 | 279,972 | `CDA96FDF3F092B88B669F5AA6CB49B45E59C9BE8C64C568825D03CAF14913B05` |
| `IW Final Text of Regulations (Marked).pdf` | `calgem/idle_well/Documents/Idle_Well_workshop_regs/IW%20Final%20Text%20of%20Regulations%20(Marked).pdf` | 23 | 229,846 | `24C22888357F1A1EAA72A75D7C0F16A8921BED489463E039CFC850ECF867F2B2` |
| `Public Works Well Abandonment Contract Template Labor Code.pdf` | `calgem/Documents/Public%20Works%20Well%20Abandonment%20Contract%20Template%20Labor%20Code.pdf` | 35 | 323,409 | `1AE28EF5FCAE86676E748B915187F829BF49183385F921FDA5F497DCCC4C966F` |
| `2026-02 UIC Approval Process Update.pdf` | `calgem/Documents/2026-02%20UIC%20Approval%20Process%20Update.pdf` | 5 | 398,223 | `FB0A3095CDBC6215654793CDA21349F8B7E9C8F61788EF984BC0E1DF1F844A60` |
| `Guidance_for_NOI_and_Permit_Search_Draft 1 1.pdf` | `calgem/Documents/WellSTAR/All-Training/Guidance_for_NOI_and_Permit_Search_Draft%201%201.pdf` | 5 | 543,728 | `17740881730BB2F362B0C488D838DDD57E5FC2009709DC1E2AF56FAA6F23F227` |
| `1422 PA Order Temple Resources_ADA.pdf` | `calgem/Documents/Orders/1422%20PA%20Order%20Temple%20Resources_ADA.pdf` | 6 | 203,515 | `64B13C3A977F4A1C302D96C72B5432D76F91EE5537704B8EDD4EC6760DF10B83` |
| `UGS 2nd Revised Text of the Regulations.pdf` | `calgem/Documents/GasStorage/UGS%202nd%20Revised%20Text%20of%20the%20Regulations.pdf` | 19 | 216,244 | `51EDC6FAE3C30190ED8D2056F696009E6E4CB796F5FE8C8A431FFD6529EC55B4` |
| `MOA UIC Checklist_2026.03.xlsx` | `calgem/Documents/UIC%20regulations/MOA%20UIC%20Checklist_2026.03.xlsx` | — | 62,933 | `141F04579DB45D4B250E954BAFC25AFE3BC0E2F7319762254D4BE78B437D9C26` |
| `Casing Diagram Submission_UGS NTO_Dec 2025.pdf` | Internet Archive copy, captured Jan 25, 2026, of `calgem/gas-storage-disclosure/Documents/Casing%20Diagram%20Submission_UGS%20NTO_Dec%202025.pdf` (see note below) | 2 | 190,761 | `174BE8C733A58FC78FFD78AE7D3AB87EFCEC976E4EF53CD85378DE01CA577A3A` |
| `14 CCR 1726.4.1 Casing Diagrams.md` | Regulation text copied from Justia (see note below) | — | — | `BE7235BAFE66CB43F7D35B46723C9FC614309CB81CABA53EDE5E9F607C432C58` |

**What each contains that bears on wellbore diagrams:**

- **UIC Regulations, final text:** Title 14 CCR § 1724.7.1, "Casing Diagrams" (pp. 9–11). It lists 15 required data elements, accompanying cement and wellbore-path documentation, a rule for sidetracked wellbores, a requirement for both measured and true vertical depth, and permission to submit "a flat-file data set" in place of a graphic diagram.
- **Idle Well Regulations, final text (marked):** Title 14 CCR § 1772.1.3, "Casing Diagrams" (pp. 15–17). The same list as § 1724.7.1, applied to idle wells.
- **Well abandonment contract template:** pages 1–2 list 17 items, (a) to (q), that a wellbore diagram must show in a Notice of Intention to Abandon (Form OG 108).
- **2026-02 UIC Approval Process Update (NTO 2026-02):** page 3 describes an early review of area-of-review wellbore diagrams, "focusing on cement calculation methodology and well construction accuracy."
- **NOI and Permit Search guidance:** page 3 lists current and proposed wellbore diagrams as attachments to a Notice of Intention in WellSTAR.
- **Order No. 1422:** page 4 requires an operator to furnish "a wellbore diagram accurately depicting the information included on the Well Summary."
- **Underground Gas Storage regulations, 2nd revised text:** searched; no passage on wellbore or casing diagrams was found.
- **MOA UIC Checklist (2026.03):** searched; no passage on wellbore or casing diagrams was found.
- **Casing Diagram Submission Requirements (Notice to UGS Operators, December 5, 2025):** reminds underground gas storage operators to submit updated casing diagrams within 60 days after well work that does not need a Notice of Intention, whenever wellbore equipment changes (packers, safety valves, gas lift mandrels, tubing, wellhead components). It quotes § 1726.4(a)(5)(F): the § 1726.4.1 data must be provided "in the form of graphical casing diagrams or flat file data sets."
- **14 CCR § 1726.4.1, "Casing Diagrams" (underground gas storage):** lists 18 required data elements, (A) to (R); requires measured and true vertical depth for every measurement, a directional survey for directional wells, electronic submission, and the mechanical barrier elements for injection and withdrawal wells. Subdivision (b): "In lieu of graphical casing diagrams, operators may satisfy the requirements … by submitting a flat file data set containing all of the information described in this section."

**Limits:** these PDFs are CalGEM's postings of regulation texts, not the official code. Before citing a section in the proposal, confirm its current text in the official California Code of Regulations. CalGEM publishes no dataset of wellbore diagram contents; diagrams exist as document attachments to individual well records in WellSTAR.

**Added November 11, 2026.** A coworker reported that CalGEM now asks for wellbore diagram data as a table (Excel). Searches of CalGEM's site and the web found the flat-file option in three regulations (§ 1724.7.1 UIC, § 1772.1.3 idle wells, § 1726.4.1 gas storage) and the December 2025 notice above, but no CalGEM Excel template or column specification for a casing-diagram table. The notice is listed on CalGEM's "Notices to Operators – Underground Gas Storage Facilities" page (https://www.conservation.ca.gov/calgem/Pages/UGS-Operator-notices.aspx), whose link now goes to the File Request system (https://filerequest.conservation.ca.gov/RequestFile/2911544); the former direct PDF URL returns 404. The copy kept here came from the Internet Archive snapshot at https://web.archive.org/web/20260125125658/https://www.conservation.ca.gov/calgem/gas-storage-disclosure/Documents/Casing%20Diagram%20Submission_UGS%20NTO_Dec%202025.pdf, saved through the browser on November 11, 2026. The regulation text was copied on November 11, 2026, from https://regulations.justia.com/states/california/title-14/division-2/chapter-4/subchapter-1/article-5/section-1726-4-1/, which states it is current through Register 2025, No. 26 (June 27, 2025).

---

## 7. Wellbore diagrams for 10 Ventura field wells (now `06-study/pilot-ventura/`)

**Purpose:** real examples of the casing diagrams specified in Title 14 CCR § 1724.7.1 (section 6).

**Source:** WellSTAR public portal, https://wellstar-public.conservation.ca.gov/. Entry requires accepting a data disclosure (no-warranty disclaimer); Lester Carcamo accepted it in the browser on November 10, 2026. No account or login was used.

**Retrieval date:** November 10, 2026, about 11:36–11:45 PM.

### 7.1 How the wells were selected

1. **Population:** wells in the Ventura oil field (field code 814, Ventura County) in `2021CaliforniaOilAndGasWells.csv`: 2,088 distinct API numbers, nearly all held by a single operator. Operator identity is not used in this study.
2. **First draw:** 10 wells by stratified random sample (Python `random`, seed `20261110`): 4 active oil and gas, 2 active water flood, 2 idle, 2 plugged.
3. **Check:** for each well, the WellSTAR Well Detail page, Documents view, was searched for documents of type "Wellbore Diagram." Five of the 10 had none.
4. **Replacements:** a second ordered draw of candidates (seed `20261111`) in the same strata. Candidates were checked in order, and the first ones with a wellbore diagram replaced the wells without one.
5. **Exception:** none of the 12 plugged-well candidates checked had a wellbore diagram in WellSTAR. The plugged slot was filled with the next idle-well candidate. Plugged-and-abandoned conditions are still represented by three "as plugged" diagrams (Hartman 5, Taylor 154, Taylor 711).

**Wells checked that had no wellbore diagram (API, 10 digits):**

- First draw: 0411122058 (RBU Gosnell 56), 0411104661 (Hartman East 42), 0411105235 (Taylor 392), 0411104921 (V. L. & W. 16), 0411105089 (Taylor 223)
- Active oil and gas candidates: 0411104825, 0411104531, 0411105287, 0411104800, 0411121338
- Active water flood candidates: 0411104647, 0411104706
- Plugged candidates: 0411104930, 0411104982, 0411103893, 0411120519, 0411104808, 0411120159, 0411105332, 0411104751, 0411104556, 0411104713, 0411104371, 0411105335

### 7.2 Final set: 10 wells, 14 documents

Status and type are from the 2021 wells file. "Doc ID" is the Document ID shown in WellSTAR; files were downloaded through Explore Data → Documents by searching that ID.

| # | API (10) | Well | 2021 status, type | WellSTAR well page | Doc ID | Description in WellSTAR | Relevant date |
|---|---|---|---|---|---|---|---|
| 1 | 0411105027 | V.L. & W. 118 | Active, OG | Detail/227443 | 485119 | WBD | 07/23/2021 |
| 2 | 0411121560 | Hartman East 73 | Active, OG | Detail/227887 | 545690 | WBD | 12/07/2021 |
| 3 | 0411105257 | Taylor 420 | Active, OG | Detail/228442 | 635292 | WBD | 04/25/2022 |
| 4 | 0411122017 | Lloyd 265 | Active, OG | Detail/226878 | 705345 | WBD | 09/14/2022 |
| 5 | 0411104888 | McGonigle 21 | Active, WF | Detail/227304 | 522606 | WBD (v2) | 11/08/2021 |
| 6 | 0411103998 | RBU L. Hartmann 2 | Active, WF | Detail/227028 | 243866 | WBD | 11/19/2019 |
| 7 | 0411104441 | Hartman 5 | Idle, OG | Detail/228174 | 359964 | Current wellbore diagram | 08/17/2020 |
| | | | | | 359965 | Wellbore diagram proposed | 08/17/2020 |
| | | | | | 1046587 | Well P&A schematic | 12/14/2021 |
| 8 | 0411121506 | Taylor 711 | Idle, OG | Detail/227876 | 911948 | Well P&A schematic | 03/30/2021 |
| 9 | 0411104246 | Lloyd Corp. 75 | Idle, OG | Detail/228019 | 16045 | WBD | 06/07/2018 |
| 10 | 0411104595 | Taylor 154 | Plugged, OG | Detail/228328 | 55777 | Wellbore Schematic Current | 10/23/2018 |
| | | | | | 55778 | Wellbore Schematic Proposed | 10/23/2018 |
| | | | | | 185579 | Wellbore Schematic – As P&A | 07/12/2019 |

Well page URLs are `https://wellstar-public.conservation.ca.gov/Well/Well/` followed by the value shown.

Wells 3, 4, 6, 8, and 9 are replacements (section 7.1). Hartman 5 and Taylor 711 are idle in the 2021 file but have later plugged-and-abandoned schematics; their status in WellSTAR may have changed since 2021.

### 7.3 File inventory

Files were renamed to the well name on November 10, 2026; where a well has more than one diagram, the name adds "Current," "Proposed," or "As P&A." The original WellSTAR file name is kept in the table. Contents are unchanged, so the checksums match the files as delivered. All are PDFs with extractable text (not scanned images).

| Doc ID | File in this folder | Original WellSTAR file name | Pages | Bytes | SHA-256 |
|---|---|---|---|---|---|
| 485119 | `V.L. & W. 118.pdf` | `WBD_VLW118 - 01 - 02 - 5_11_2021.pdf` | 1 | 311,078 | `D692831ED2C1F22E669109307D6A9AA3F7DF03D4326D94703899A605F4D6C95A` |
| 545690 | `Hartman East 73.pdf` | `WBD_HTM073 - 00 - HTM073 - 12_3_2021.pdf` | 1 | 717,160 | `7786F2B2AEA1B2F3B803319933641B2F92CDA38EC3C2C95266C68F1427219229` |
| 635292 | `Taylor 420.pdf` | `New_WBD_TAY420 - 01 - 02 - 4_7_2022.pdf` | 1 | 328,955 | `3FEA5D95160AE69D1D2274ADA0EF0F0257DB185E5575084D936243D4A2674883` |
| 705345 | `Lloyd 265.pdf` | `WBD_0411122017 00_LYD265.pdf` | 1 | 97,122 | `1CE7805A467201971AC33473DB4D0C2737886E827C65DF3D41D7BBB70EE003F6` |
| 522606 | `McGonigle 21.pdf` | `WBD_MCG021 - 07 - 08 - 7_27_2020_v2.pdf` | 1 | 326,066 | `F261D716C52480E33EAB849EEB82CB7A4B9C94D5E9E2B915F4870F632E472D6A` |
| 243866 | `RBU L. Hartmann 2.pdf` | `88a06a54-b0f5-4cf8-b3c9-5bfdeb78fdd6_WBD_11103998_01_RBH2.pdf` | 1 | 137,939 | `0E4844F9655B5F87EACBCA2A9D38A2B48EBFE1C955EBD210E7F1E42DB5E3B3F1` |
| 359964 | `Hartman 5 - Current.pdf` | `Hartman 5 Wellbore Diagram- Current.pdf` | 1 | 102,215 | `A5DF11ADB1BFE84E5781F5D20B34890F0AC1A9992A4A261FD8F138CA873FF2A1` |
| 359965 | `Hartman 5 - Proposed.pdf` | `Hartman 5 Wellbore Diagram- Proposed.pdf` | 1 | 135,567 | `8AABE6D786F8F1E2998A98B72DDD56F403D44A12341C90DE117C57824D889D08` |
| 1046587 | `Hartman 5 - As P&A.pdf` | `HARTMAN 5 P&A'd schematic (01).pdf` | 1 | 376,046 | `EFF10D72DAB9C403B531E4FD4F4E2BF885674E1AB5A58FA82B16EE164A754183` |
| 911948 | `Taylor 711 - As P&A.pdf` | `TAYLOR 711 P&A'd schematic.pdf` | 1 | 389,783 | `526FE4C51A44039BEE1D551F9CAC88CCD7CF3E459139E11FD905F9E707114EA9` |
| 16045 | `Lloyd Corp. 75.pdf` | `85e54b75-3823-4787-9ca3-435c03c156b9_11104246 01_LCP075.pdf` | 2 | 64,289 | `5A641FDE318CFD12F4E10DE8035F4AAD083B9CE857D4250066E9FD54A69BFBCE` |
| 55777 | `Taylor 154 - Current.pdf` | `8b1ca805-faa5-4f22-9db4-3dbe8f57afb3_Tay 154 Wellbore Schematic Current.pdf` | 1 | 11,957 | `2EE12EFC3D1F3C47976C5D9B86058938A955AD7078B003EBAB01A4246D49656E` |
| 55778 | `Taylor 154 - Proposed.pdf` | `37cea0c6-f05a-4f09-935d-3adc85a445da_Tay 154 Wellbore Schematic Proposed.pdf` | 1 | 17,777 | `E36CE57CD244F3B0E5589A76E2660F91447D11A76C68ED086922125A4ABF7F5C` |
| 185579 | `Taylor 154 - As P&A.pdf` | `410c8c01-1851-4fb7-8a8a-436e00b6cc2f_Taylor 154 As P&A.pdf` | 1 | 310,666 | `AD72909D9F791F054476759BBE899BF3DA6B7AC63949B814C6084128436B0AA0` |

### 7.4 How to reproduce the selection and download

**Step 1. Selection.** Run the script, now kept in `graduate-project/scripts/` (Python 3, standard library only), from this folder:

```
python ../../scripts/select_ventura_wells.py 2021CaliforniaOilAndGasWells.csv
```

It prints the first draw and the ordered replacement candidates for each stratum. Rules the script implements:

- A well is a distinct 12-digit API in the wells file; when an API appears in several rows (one per pool), the first row in file order is used.
- Field name equal to "Ventura" (ignoring case and surrounding spaces).
- Strata: Active with type OG (4 wells), Active with type WF (2), Idle of any type (2), Plugged of any type (2).
- First draw: `random.seed(20261110)`, then `random.sample` once per stratum, in the order listed.
- Replacements: `random.seed(20261111)`, then `random.shuffle` of each stratum (excluding the first draw), in the order listed.

Rules applied by hand while checking candidates:

- Candidates were checked in printed order, and the first ones with at least one document of type "Wellbore Diagram" were taken.
- WellSTAR identifies wells by the first 10 digits of the API. A candidate whose 10-digit API had already been checked was skipped (Lloyd 150, which appears in both the Active OG and the Active WF lists).
- The plugged slot was filled from the idle list once all 12 plugged candidates had been checked without result (section 7.1, step 5).

**Step 2. Find a well's wellbore diagrams in WellSTAR.**

1. Open https://wellstar-public.conservation.ca.gov/ and accept the data disclosure.
2. In the search box at the top right, choose "Well API," type the 10-digit API, and press Enter.
3. Click the API link in the results to open the Well Detail page.
4. Open the drop-down at the right of the well name (it shows "Summary") and choose "Documents."
5. In the documents grid, find rows whose Type is "Wellbore Diagram." Note each row's Document ID.

**Step 3. Download each diagram.** The grid on the Well Detail page has no working download link for public users; CalGEM's own guidance (`wellbore-diagram-sources/Guidance_for_NOI_and_Permit_Search_Draft 1 1.pdf`, pages 4–5) describes this workaround:

1. Go to Explore Data → Documents (https://wellstar-public.conservation.ca.gov/General/DocumentSearch/Index).
2. Type the Document ID in the "Document ID" field and click Search.
3. Click the file name in the result to download it.

**Step 4. Verify.** Compute the SHA-256 of each downloaded file and compare it with the table in section 7.3. A mismatch means the operator or CalGEM has replaced the document since November 10, 2026.

**Tooling used on November 10, 2026:** steps 2 and 3 were carried out in a Chrome browser driven by the Playwright MCP server from Claude Code, using the same pages and clicks described above. The browser automation was not saved; the manual steps reproduce it.

**Notes:**

- The download address uses a different internal number from the Document ID shown in WellSTAR. For example, Doc ID 485119 downloads from `/Common/Document/DownloadDocument/?documentId=484887`.
- The diagrams were prepared by the operator and filed with CalGEM. CalGEM's disclaimer applies: no warranty of accuracy or completeness.

---

## 8. Enforcement orders (subfolder `enforcement-orders/`, unchanged)

**Purpose:** the published record of CalGEM enforcement, to learn which violations lead to orders and whether wellbore diagrams are among them.

**Source:** CalGEM, "Enforcement Orders" page, https://www.conservation.ca.gov/calgem/Pages/Division_Orders.aspx, linked from the Office of Enforcement page (https://www.conservation.ca.gov/calgem/Pages/Enforcement.aspx).

**Retrieval:** November 10–11, 2026, by the script `download_enforcement_orders.py` (section 10). The script reads the page, collects every link to a PDF, and downloads each one with a half-second pause between requests.

**Result:**

- The page had 448 PDF links, of which 437 were distinct.
- 436 were downloaded and are kept under the publisher's file names, unchanged.
- One link was broken on CalGEM's site: Order 1197 to Tunnel Oil Company, dated May 19, 2021 (HTTP 404, Not Found).
- Total size: about 253 MB.

**Index:** `enforcement-orders/_index.csv` lists, for each link, its position on the page, the link text, file name, URL, download time, size in bytes, page count, characters of extractable text, and SHA-256 checksum, or the error.

**Storage:** the PDFs are kept on local disk only and are excluded from git by `.gitignore`. The index is kept in the repository, so the set can be re-downloaded and verified.

**Key finding (Order 1517):** Order to Perform Remedial Work and Pay Civil Penalties No. 1517, to Sentinel Peak Resources California LLC, Inglewood field, UIC Projects 324-00-015 and 324-00-016. The date line in the extracted text is incomplete (only "4/24/" survives near the signature); from the sequence below, the order was issued after December 24, 2024, probably on April 24, 2025 (inferred, not confirmed).

- **Violation:** wellbore casing diagrams did not comply with Title 14 CCR §§ 1724.7(a) and 1724.7.1.
- **Deficiencies named:** true vertical depth not given at all depths (§ 1724.7.1(d)); formation locations (cited as § 1724.7(a)(15)); spud date (§ 1724.7.1(a)(2)); inaccurate wellbore data (§ 1724.7(a)); kickoff points (casing cuts or modifications) not documented (§ 1724.7.1(a)(9)); graphical diagrams not matching the flat-file data sets (§ 1724.7.1(e)).
- **Sequence:** CalGEM email listing deficiencies, October 1, 2024; extension granted to December 20, 2024; operator asked for 12 more weeks, December 18, 2024; Notice of Violation, December 24, 2024; then this order.
- **Penalty:** $1,500 (2 violations at $750), characterized as "minor" under PRC § 3236.5(b), plus submission of corrected project data within 30 days; daily penalties accrue after that.

Other orders mentioning casing diagrams (Orders 1268, 1270, 1273, 1274, 1282) quote the idle-well requirement of § 1772.1.3 as part of plug-and-abandon orders; they do not penalize diagram defects as such.

---

## 9. Notice of Violation sources (now `04-literature/regulatory/nov-sources/`)

**Purpose:** documents that explain what a Notice of Violation (NOV) is, how many are issued, and where they are published.

**How obtained:** Department of Conservation site search for "Notice of Violation" and related phrases on November 10, 2026; each file downloaded directly on November 11, 2026, about 12:00 AM, with no login. File names are the publisher's; contents unchanged.

All URLs begin with `https://www.conservation.ca.gov/calgem/Documents/`.

| File | Path after the base URL | Bytes | SHA-256 |
|---|---|---|---|
| `SB 406 Implementation Report 2024-2025.pdf` | `SB%20406%20Implementation%20Report%202024-2025.pdf` | 592,197 | `AC8B2F5B11D31898A253724D9C8B5BA24000D56F16DF138CF562DD38850D8E0C` |
| `SB 406 Implementation Report 2023-24.pdf` | `SB%20406%20Implementation%20Report%202023-24.pdf` | 698,033 | `B47FDB41D69D648903DAED42C96C0CA91DCE45E139C494AB6F00C57942E7C701` |
| `SB 406 Implementation Report 2023.pdf` | `SB%20406%20Implementation%20Report%202023.pdf` | 1,072,798 | `92670CD69D89B5E8EBE09FD2094C39036CBAD1121A8A02ACED62732596EDD3EC` |
| `2021 CalGEM Supervisor Annual Report.pdf` | `2021%20CalGEM%20Supervisor%20Annual%20Report.pdf` | 3,049,573 | `15BF0F9916FA014F9AD6826C4C1BC009C12F14AA4FB1DCFC2140ADF2602F9165` |
| `NTO 2024-03 Enhanced Field Enforcement Final.pdf` | `NTO%202024-03%20Enhanced%20Field%20Enforcement%20Final.pdf` | 237,327 | `16F3B2525B5CAD5801A0DEA9A2610D47CE0ED49FFFB00EB6CE7282E8E7ACA1D8` |
| `R4-Compliance-UG.pdf` | `WellSTAR/All-Training/R4-Compliance-UG.pdf` | 1,567,385 | `4CE9ADDE73C9979B8EE161A76ECDD9EF339B86CD678606FD1F42ECEBDA62FE76` |
| `NOV_19_0033_CVX_McPhee_36W_SE_21Aug19.pdf` | `NOV_19_0033_CVX_McPhee_36W_SE_21Aug19.pdf` | 784,046 | `DEFDD822BB9CB5740E2C517FCA9AE1119AB6CCD4FC805068BF2CB6F81179182A` |
| `NOV_V19_0032_GS5_23Aug19.pdf` | `NOV_V19_0032_GS5_23Aug19.pdf` | 1,920,247 | `AFBD29E46EB295ABAD85B80C4B57E175051411C4B73D2BF0E1440F82E9C1E45E` |
| `NOV V19-0037 Sentinel Peak Midway Sunset Reardon Surface Expression May 16 2019 (1).pdf` | `Cymric%20chevron%20oil%20spill/NOV%20V19-0037%20Sentinel%20Peak%20Midway%20Sunset%20Reardon%20Surface%20Expression%20May%2016%202019%20(1).pdf` | 805,883 | `ED4501C320B5F11341AB1E3368BBE2A5A2B546781CB03AEF6981AA34908ADF2E` |
| `NOV-V20-0039-Sentinel-Peak-Cymric-Star-Fee-Surface-Expression-Rev.5-29-20.pdf` | `Surface-Expressions/NOV-V20-0039-Sentinel-Peak-Cymric-Star-Fee-Surface-Expression-Rev.5-29-20.pdf` | 3,306,660 | `F5523442CE9F4517EAB7E8A82AA14423DBBE7814A3ADB8757EEA63EFC520AC97` |
| `NOV_V20_0231 Berry Midway Sunset Southwestern Surface_Expression_August 15 2020.pdf` | `Surface-Expressions/NOV_V20_0231%20Berry%20Midway%20Sunset%20Southwestern%20Surface_Expression_August%2015%202020.pdf` | 1,098,579 | `9CEA2F5A796EB383B061FCA444A20D1B71EA0270728FFDE5F15CCBE291FC26CC` |

**What they establish:**

- **Volume (2021 Supervisor Annual Report, enforcement overview):** 60,792 inspections; 1,789 NOVs issued; 1,027 NOVs returned to compliance at time of publication; 43 orders (32 civil penalty, 4 plug and abandon); $1,520,550 in civil penalties issued; 6 orders appealed.
- **Publication (SB 406 reports; PRC § 3108.5(a)(2)):** NOVs and Supervisor orders were to be online by July 1, 2024. Per the 2024–2025 report (dated October 2026), NOVs are "generally available in WellSTAR" but "searchable only by well or facility associated with the violations"; orders are posted on the Enforcement Orders page.
- **Enforcement practice (NTO 2024-03, March 13, 2024):** operators still receive an NOV or inspection report with a deadline, but correcting the violation "does not preclude the issuance of a civil penalty for an observed violation."
- **Example NOVs:** five standalone NOVs from 2019–2020 (four oil surface expressions and one gas storage well, GS-5).
- **WellSTAR compliance user guide:** describes how violations and NOVs are recorded in WellSTAR.

---

## 10. Scripts kept for reproducibility

| Script | Purpose | Sections |
|---|---|---|
| `select_ventura_wells.py` | Random selection of Ventura field wells (Python, standard library) | 7.1, 7.4 |
| `wellstar_wellbore_diagrams.js` | Find and download wellbore diagrams in WellSTAR (Playwright; the data disclosure is accepted by hand) | 7.4 |
| `download_enforcement_orders.py` | Download and index all enforcement orders (Python with `pypdf`) | 8 |
| `select_sample.py` | Random order of all Active or Idle wells for the 30-well sample; writes `06-study/sample/screening-log.csv` | `06-study/sample/sampling-plan.txt` |
| `profile_pdf_quality.py` | Profiles the 30 sample PDFs; writes `06-study/sample/pdf-quality-profile.csv` | `06-study/sample/sample-quality-evaluation.txt` |

All five scripts are in `graduate-project/scripts/` since November 12, 2026.

Usage: `python download_enforcement_orders.py <folder for PDFs> <file for text snippets>`. The script skips files already present, so it can be re-run to fill gaps.

---

## 11. Storage

- The two CSV files (about 134 MB together) and the 436 enforcement order PDFs (about 253 MB) are kept on local disk only and are excluded from the git repository by `.gitignore`. The checksums in section 3 let anyone confirm that a copy is identical.
- The four documentation files (one `.xls` and three `.pdf`), the eight files in `wellbore-diagram-sources/`, the 14 diagrams in `wellbore-diagrams/` (about 3.2 MB; now `06-study/pilot-ventura/`), the 11 files in `nov-sources/` (about 15 MB), `enforcement-orders/_index.csv`, the three scripts in section 10, and this record are kept in the repository.
- A future copy obtained from CalGEM may differ, because the publisher may update or remove files without notice.
