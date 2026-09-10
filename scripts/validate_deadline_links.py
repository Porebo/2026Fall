import json
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "deadlines.json"
VALID_TYPES = {"homework", "exam", "admin", "event"}
HARD_HOMEWORK_REQUIRED_FIELDS = [
    "assignmentNumber",
    "assignmentName",
    "assignedDate",
    "description",
    "submissionLocation",
    "status",
    "grade",
]
SOFT_HOMEWORK_REQUIRED_FIELDS = [
    "assignmentNumber",
    "assignmentName",
    "assignedDate",
    "description",
    "status",
    "grade",
]


def is_external_url(url):
    return urlsplit(url).scheme in {"http", "https"}


def local_path_from_url(url):
    return url.split("#", 1)[0].split("?", 1)[0]


def check_local_url(label, url, failures):
    if not url or is_external_url(url):
        return

    relative_path = local_path_from_url(url)
    if not (ROOT / relative_path).exists():
        failures.append(f"{label}: missing {relative_path}")


def require_field(record, field_name, label, failures):
    if field_name not in record or record[field_name] in (None, ""):
        failures.append(f"{label}: missing required field '{field_name}'")


def validate_deadline(deadline, courses, failures):
    label = f"deadline {deadline.get('id') or deadline.get('title') or '<unknown>'}"

    for field_name in ["id", "date", "course", "type", "title"]:
        require_field(deadline, field_name, label, failures)

    deadline_type = deadline.get("type")
    if deadline_type and deadline_type not in VALID_TYPES:
        failures.append(f"{label}: unsupported type '{deadline_type}'")

    course_key = deadline.get("course")
    if course_key and course_key not in courses:
        failures.append(f"{label}: course '{course_key}' is not listed in courses")

    if deadline_type == "homework":
        required_fields = SOFT_HOMEWORK_REQUIRED_FIELDS if deadline.get("workType") == "soft" else HARD_HOMEWORK_REQUIRED_FIELDS
        for field_name in required_fields:
            require_field(deadline, field_name, label, failures)

    check_local_url(label, deadline.get("url"), failures)


def main():
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    failures = []
    courses = data.get("courses", {})

    for course_key, course in courses.items():
        if not course_key:
            failures.append("course entry: missing course key")
        if isinstance(course, dict):
            require_field(course, "name", f"course {course_key}", failures)
            require_field(course, "home", f"course {course_key}", failures)
            check_local_url(f"course {course_key}", course.get("home"), failures)
        else:
            failures.append(f"course {course_key}: course entry must be an object")

    for deadline in data.get("deadlines", []):
        validate_deadline(deadline, courses, failures)

    if failures:
        print("Deadline link validation failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("Deadline link validation passed.")


if __name__ == "__main__":
    main()