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
- `/templates/` — starter files for future course home, assignment, and lecture pages

## Semester template workflow

Use the files in `templates/` when starting a new semester or adding a new class pattern:

- `templates/course-home.html` — starter class landing page with the shared deadline, assignment, and lecture widgets
- `templates/assignment-page.html` — starter homework page with details, resources, and a persistent checkbox checklist
- `templates/lecture-page.html` — starter lecture page with recording, notes, and action items

Replace every `{{PLACEHOLDER}}` value before publishing the page. After adding course or homework entries, run the validator below so missing fields and broken local links are caught early.

## Deadlines

Add or edit entries in `data/deadlines.json`. Each deadline supports:

- `date` (required) and optional `endDate` for multi-day events
- `timeDisplay` for human-readable due times
- `course` slug matching a class folder name
- `type`: `homework`, `exam`, `admin`, or `event`
- `title` and optional `url` to the assignment or reference page

Homework entries also support:

- `assignmentNumber`, `assignmentName`, and `assignedDate`
- `description` for the tracker preview
- `submissionLocation` and optional `blackboardUrl`
- `points`, `estimatedHours`, `status`, and `grade`

Validate local links referenced by the central deadline data with:

```powershell
python scripts/validate_deadline_links.py
```

The validator also checks that:

- course entries include `name` and `home`
- deadlines include `id`, `date`, `course`, `type`, and `title`
- deadline `course` values match a course in `data/deadlines.json`
- homework entries include the required tracker fields

Each course entry in `data/deadlines.json` also includes a `home` URL used for linked course names in deadline lists and the calendar.

The semester page shows all upcoming action items plus a Fall calendar. Each class home page shows filtered upcoming items and assignments for that course.

Research Methods also uses `data/research-methods-lectures.json` to render the month-by-month lecture sidebar on its class home page.

Principles of IQ uses `data/principles-of-iq-lectures.json` with the same shared `scripts/lecture-channel.js` calendar component.

## Courses

| Course | Folder | Home page |
|---|---|---|
| Graduate Project (IFSC 78603) | `classes/graduate-project/` | `home-graduate-project.html` |
| Principles of IQ (INFQ 70303) | `classes/principles-of-iq/` | `home-principles-of-iq.html` |
| Research Methods (INFQ 72203) | `classes/research-methods/` | `home-research-methods.html` |
| Master Thesis | `classes/master-thesis/` | `home-master-thesis.html` |

## Conventions

- Meeting pages use `YYYY-MM-DD.html` where possible (e.g. `2026-08-25.html`) and live inside that week's folder (`w01/`, `w02/`, etc.) alongside any assignment/lab files for that week.
- Breadcrumbs follow: Home → Class → Page.

## Reference

- [MS in Information Science graduation requirements](https://ualr.edu/informationscience/ms-in-information-science/graduation-requirements-for-master-of-science-in-information-science/)
