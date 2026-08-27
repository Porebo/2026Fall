# 2026Fall

Static website for the Fall 2026 college term.

## Site structure

- `/index.html` — semester gateway with links to each class
- `/classes/<course-slug>/home-<course-slug>.html` — class landing page
- `/classes/<course-slug>/meetings/` or dated pages — lecture and session notes
- `/classes/<course-slug>/assignments/` or week folders — homework pages
- `/classes/<course-slug>/documents/` — syllabi and course PDFs
- `/classes/Books/` — shared reading PDFs used across courses
- `/data/deadlines.json` — single source of truth for homework, exams, admin dates, and events
- `/scripts/term-calendar.js` — renders upcoming deadlines, assignments, and the term calendar

## Deadlines

Add or edit entries in `data/deadlines.json`. Each deadline supports:

- `date` (required) and optional `endDate` for multi-day events
- `timeDisplay` for human-readable due times
- `course` slug matching a class folder name
- `type`: `homework`, `exam`, `admin`, or `event`
- `title` and optional `url` to the assignment or reference page

Each course entry in `data/deadlines.json` also includes a `home` URL used for linked course names in deadline lists and the calendar.

The semester page shows all upcoming action items plus a Fall calendar. Each class home page shows filtered upcoming items and assignments for that course.

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
