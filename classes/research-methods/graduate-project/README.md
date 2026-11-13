# Graduate Project: AI Review of Wellbore Diagrams

MS Information Science master's project, Lester S. Carcamo. Advisor: Dr. Ningning Wu.

**Status and next steps:** [02-plan/proposal-plan.md](02-plan/proposal-plan.md)

| Deadline | What | Checklist |
|---|---|---|
| Mon, Nov 16, 2026 | Proposal and approval form to the committee | [02-plan/proposal-plan.md](02-plan/proposal-plan.md) |
| Fri, Dec 4, 2026, 9:59 PM | Final Research Proposal, INFQ 72203 (Blackboard) | [03-proposal/REQUIREMENTS.md](03-proposal/REQUIREMENTS.md) |

## Folder map

| Folder | Contents |
|---|---|
| `01-admin/` | Proposal approval form (blank and draft), committee email and outreach page, Week 10 planning assignment |
| `02-plan/` | `proposal-plan.md` (decisions, schedule, risks); `prompt_working.md` (notes from the Nov 10 session) |
| `03-proposal/` | The proposal draft (`Lester Work.docx`), course requirements, draft introduction text, slides, `samples/` of UT proposals |
| `04-literature/papers/` | Peer-reviewed and other papers, named `FirstAuthor, Year, Title, Journal.pdf` |
| `04-literature/regulatory/` | CalGEM rules, notices, and reports: `wellbore-diagram-sources/`, `nov-sources/` |
| `05-data/calgem/` | CalGEM 2021 wells and production CSVs, code definitions, 436 enforcement orders, and `PROVENANCE.md` (sources, checksums, how to reproduce) |
| `06-study/design/` | Business scenario, the casing diagram rule (14 CCR § 1726.4.1, verbatim), and `prompts/`: the four prompts, their copy-and-paste texts, and the methods draft |
| `06-study/sample/` | Sampling plan, screening log, input quality profile, and the 30 sampled diagrams `diagrams/W01.pdf` to `W30.pdf` |
| `06-study/runs/` | Dry-run responses, one folder per prompt level |
| `06-study/pilot-ventura/` | The earlier 14 diagrams from 10 Ventura field wells (before the random sample) |
| `scripts/` | Data collection and sampling scripts. Run them from any folder; their paths point into `05-data/` and `06-study/` |
| `_backup/` | One backup copy of the 30 sample diagrams, the casing diagram rule, and the naive prompt, in the same layout as `06-study/` |
| `_to-review/` | Extra copies kept until you decide what to do with them (see the note inside) |

## Related material outside this folder

- Week 5 study design draft (earlier design): [../w05/study-design-draft.md](../w05/study-design-draft.md)
- Course archive, including proposal guidance PDFs: [../archive/index.html](../archive/index.html)
- Advisor letter, committee roster, research gaps: [../../master-thesis/](../../master-thesis/)

## Git

The CSV files and enforcement order PDFs in `05-data/calgem/` are kept on local disk only (`.gitignore`). Everything else is tracked.

## Reorganization of November 12, 2026

This folder replaces `w10/` and `final-proposal-requirements/`. Files were moved, not edited, except for path references inside the study documents, `PROVENANCE.md`, the plan, and the scripts. Every move is listed in [_reorg-log.txt](_reorg-log.txt). No file was deleted.
