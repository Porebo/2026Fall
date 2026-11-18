# Graduate Project: AI Review of Casing Diagrams

MS Information Science master's project, Lester S. Carcamo. Advisor: Dr. Ningning Wu.

**Status and next steps:** [02-plan/proposal-plan.md](02-plan/proposal-plan.md)

| Deadline | What | Checklist |
|---|---|---|
| Mon, Nov 16, 2026 | Proposal and approval form to the committee | [02-plan/proposal-plan.md](02-plan/proposal-plan.md) |
| Fri, Dec 4, 2026, 9:59 PM | Final Research Proposal, INFQ 72203 (Blackboard) | [03-proposal/REQUIREMENTS.md](03-proposal/REQUIREMENTS.md) |

## Folder map

| Folder | Contents |
|---|---|
| `01-admin/` | Proposal approval form (blank and draft), committee email and outreach page |
| `02-plan/` | `proposal-plan.md` (decisions, schedule, risks); `prompt_working.md` (notes from the Nov 10 session) |
| `03-proposal/` | The proposal draft (`Lester Work.docx`), draft of section 3 (`3. Research Design and Methods.md` and its diagrams), course requirements, draft introduction text, slides, `samples/` of UT proposals |
| [calgem/](calgem/) | CalGEM regulations, notices, reports, annotated regulatory PDFs, comparison sources, current casing-diagram specification, business scenario, research notes, data dictionaries, and provenance records; all directly in one folder |
| `04-literature/papers/` | Academic and other non-regulatory papers, named `FirstAuthor, Year, Title, Journal.pdf` |
| `04-literature/regulatory/wellbore-diagram-sources/` | Historical well-record PDF `11104373_DATA_03-11-2008.pdf`, left with the input records rather than moved with the regulatory documents |
| `04-literature/casing-analysis/` | Casing-analysis database and SQL schema; the interactive regulation page is now in `calgem/` |
| `05-data/calgem/` | CalGEM datasets and enforcement-order index; downloaded CSVs, archives, and enforcement PDFs are gitignored. Documentation is in `calgem/PROVENANCE.md` |
| `06-study/design/` | `prompts/`: prompts, copy-and-paste texts, and the methods draft; `superseded/`: earlier specifications and prompts. The current rule and business scenario are in `calgem/` |
| `06-study/sample/` | Sampling plan, screening log, input quality profile, and the 30 sampled diagrams `diagrams/W01.pdf` to `W30.pdf` |
| `06-study/runs/` | Dry-run responses, one folder per prompt level |
| `06-study/pilot-ventura/` | The earlier 14 diagrams from 10 Ventura field wells (before the random sample) |
| `scripts/` | Data collection and sampling scripts. Run them from any folder; their paths point into `05-data/` and `06-study/` |
| `_backup/` | One backup copy of the 30 sample diagrams, the casing diagram rule, and the naive prompt, in the same layout as `06-study/` |
| `_to-review/` | Extra copies kept until you decide what to do with them (see the note inside) |

## Related material outside this folder

- Week 5 study design draft (earlier design): [../research-methods/w05/study-design-draft.md](../research-methods/w05/study-design-draft.md)
- Course archive, including proposal guidance PDFs: [../research-methods/archive/index.html](../research-methods/archive/index.html)
- Advisor letter, committee roster, research gaps: [../master-thesis/](../master-thesis/)

## Git

The CSV files and enforcement order PDFs in `05-data/calgem/` are kept on local disk only (`.gitignore`). Everything else is tracked.

## CalGEM document consolidation, November 17, 2026

The 74 supporting documents and notes are now directly in [calgem/](calgem/), without category subfolders. This includes the CalGEM provenance note formerly in the Principles of Information Quality data folder. Original filenames, annotated PDFs, and raw versions were preserved; no duplicates were deleted.

Datasets, casing-diagram PDFs, analysis databases, study runs, superseded files, backups, and general proposal plans remain in their existing locations. The move list (formerly `_reorg-log.txt`) is in the git history.

## Reorganization of November 12, 2026

This folder replaces `classes/research-methods/w10/` and `classes/research-methods/final-proposal-requirements/`. The files first went to `classes/research-methods/graduate-project/` and were moved here, to `classes/graduate-project/`, the same day. Files were moved, not edited, except for path references inside the study documents, `PROVENANCE.md`, the plan, and the scripts. The move list (formerly `_reorg-log.txt`) is in the git history. No file was deleted.
