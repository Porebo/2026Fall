# 2026Fall

Static website for the Fall 2026 college term.

## Site structure

- `/index.html` — semester gateway with links to each class
- `/classes/<course-slug>/home-<course-slug>.html` — class landing page
- `/classes/<course-slug>/meetings/` or dated pages — lecture and session notes
- `/classes/<course-slug>/assignments/` or week folders — homework pages
- `/classes/<course-slug>/documents/` — syllabi and course PDFs
- `/classes/Books/` — shared reading PDFs used across courses

## Courses

| Course | Folder | Home page |
|---|---|---|
| Graduate Project (IFSC 78603) | `classes/graduate-project/` | `home-graduate-project.html` |
| Principles of IQ (INFQ 70303) | `classes/principles-of-iq/` | `home-principles-of-iq.html` |
| Research Methods (INFQ 72203) | `classes/research-methods/` | `home-research-methods.html` |
| Master Thesis | `classes/master-thesis/` | `home-master-thesis.html` |

## Conventions

- Meeting pages use `YYYY-MM-DD.html` where possible (e.g. `2026-08-25.html`).
- Research Methods week content lives under `w01/`, `w02/`, etc., linked from the class home page.
- Breadcrumbs follow: Home → Class → Page.

## Reference

- [MS in Information Science graduation requirements](https://ualr.edu/informationscience/ms-in-information-science/graduation-requirements-for-master-of-science-in-information-science/)
