"""Build the Principles of IQ course archive pages from the raw Blackboard dumps.

Run from anywhere:  python classes/principles-of-iq/archive/raw/build_archive.py
"""
import html, json, os, re
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # .../principles-of-iq/archive
REPO = ROOT.parent.parent.parent                         # repo root
RAW = ROOT / "raw"
d = json.load(open(RAW / "blackboard-dump.json", encoding="utf-8"))
gf = json.load(open(RAW / "blackboard-grades-feedback.json", encoding="utf-8"))
dedupe = json.load(open(RAW / "dedupe-map.json", encoding="utf-8"))
CAPTURED = "November 11, 2026"

# ---------- helpers ----------
def central(iso):
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    off = -5 if dt < datetime(2026, 11, 1, 7, tzinfo=timezone.utc) else -6
    return dt + timedelta(hours=off), ("CDT" if off == -5 else "CST")

def fmt_dt(iso, with_time=True):
    if not iso:
        return "—"
    dt, tz = central(iso)
    s = dt.strftime("%a, %b %d, %Y").replace(" 0", " ")
    return s + (" " + dt.strftime("%I:%M %p").lstrip("0") + f" {tz}" if with_time else "")

def esc(s):
    return html.escape(s or "", quote=True)

def href(path):
    return esc(path.replace("%", "%25").replace(" ", "%20").replace("#", "%23").replace("(", "%28").replace(")", "%29"))

def local(folder, name):
    """Archive-relative link for a downloaded file, pointing at the existing site copy when identical."""
    repo_rel = f"classes/principles-of-iq/archive/files/{folder}/{name}"
    target = dedupe.get(repo_rel, repo_rel)
    return os.path.relpath(REPO / target, ROOT).replace(os.sep, "/")

def clean_html(raw, files=None):
    """Strip Blackboard markup to plain HTML; point embedded file links at local copies."""
    s = raw or ""
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", s, flags=re.S | re.I)
    def fix_a(m):
        attrs = m.group(1)
        hm = re.search(r'href="([^"]*)"', attrs)
        url = html.unescape(hm.group(1)) if hm else ""
        if "bbcswebdav" in url and files:
            bf = re.search(r'data-bbfile="([^"]+)"', attrs)
            name = json.loads(html.unescape(bf.group(1))).get("fileName") if bf else None
            if name and name in files:
                return f'<a href="{href(files[name])}">'
        if url:
            return f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">'
        return "<a>"
    s = re.sub(r"<a\b([^>]*)>", fix_a, s, flags=re.I)
    s = re.sub(r"<(?!a\b)(\w+)\b[^>]*?(/?)>", lambda m: f"<{m.group(1)}{m.group(2)}>", s)
    s = re.sub(r"</?(span|div|font)>", "", s, flags=re.I)
    s = re.sub(r"</a>\s*<a", "</a><br><a", s)
    s = re.sub(r"(<br/?>\s*){2,}", "<br>", s)
    s = re.sub(r"<p>(\s|&nbsp;|<br/?>)*</p>", "", s)
    return s.strip()

def page(title, crumb, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta name="robots" content="noindex, nofollow">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <link rel="stylesheet" href="../../../styles.css">
</head>
<body>
  <main class="page">
    <nav class="breadcrumb"><a href="../../../index.html">Home</a> / <a href="../home-principles-of-iq.html">Principles of IQ</a> / {crumb}</nav>
{body}
    <p class="lede"><small>Archived from Blackboard (INFQ 70303, Fall 2026) on {CAPTURED}.</small></p>
  </main>
  <script src="../../../scripts/site-nav.js"></script>
</body>
</html>
"""

def card(eyebrow, heading, inner, hid):
    return f"""
    <section class="card" aria-labelledby="{hid}">
      <p class="eyebrow">{esc(eyebrow)}</p>
      <h2 id="{hid}">{esc(heading)}</h2>
{inner}
    </section>"""

def hero(eyebrow, title, lede):
    return f"""
    <header class="hero">
      <p class="eyebrow">{esc(eyebrow)}</p>
      <h1>{title}</h1>
      <p class="lede">{lede}</p>
    </header>"""

def write(name, title, crumb, body):
    (ROOT / name).write_text(page(title, f'<a href="index.html">Course Archive</a> / {crumb}' if name != "index.html" else crumb, body), encoding="utf-8")

# ---------- lookups ----------
top = {c["title"]: c for c in d["contents"]}
cols = {c["id"]: c for c in d["columns"]}
grade_rec = {g["columnId"]: g for g in gf["results"]}
attempts = d["attempts"]
priv = d["attemptsPrivate"]
FILES_HANDOUT = {n: local("assignment-files", n) for n in os.listdir(ROOT / "files" / "assignment-files")} if (ROOT / "files" / "assignment-files").exists() else {}
for k, v in dedupe.items():
    if "/assignment-files/" in k:
        FILES_HANDOUT[k.rsplit("/", 1)[1]] = os.path.relpath(REPO / v, ROOT).replace(os.sep, "/")

def feedback_html(col_id):
    raw = ((grade_rec.get(col_id) or {}).get("instructorFeedback") or {}).get("rawText")
    return clean_html(raw) if raw else ""

def score_text(col_id):
    g = grade_rec.get(col_id) or {}
    sc = (g.get("displayGrade") or {}).get("score")
    poss = cols[col_id]["score"]["possible"]
    return f"{sc:g} / {poss:g}" if sc is not None else "Not graded"

def col_for(title):
    return next(c["id"] for c in d["columns"] if c["name"] == title)

def item_link(c, folder):
    att = next((a for a in c.get("_attachments", []) if "id" in a), None)
    if not att:
        return f"<li>{esc(c['title'])}</li>"
    return f'<li><a href="{href(local(folder, att["fileName"]))}">{esc(c["title"])}</a></li>'

# ---------- assignments ----------
blocks = []
for k, a in enumerate(top["Homework Assignments"]["_children"]):
    t = d["assessments"][a["id"]]["contentDetail"]["resource/x-bb-asmt-test-link"]["test"]
    asmt, gc = t["assessment"], t["gradingColumn"]
    cid = col_for(a["title"])
    subs = []
    for at in attempts.get(cid, []):
        p = priv.get(at["id"]) or {}
        for f in p.get("studentSubmissionFiles", []):
            subs.append(f'<a href="{href("files/my-submissions/" + f["name"])}">{esc(f["name"])}</a> <small>(submitted {fmt_dt(p.get("attemptReceipt", {}).get("submissionDate"))})</small>')
    fb = feedback_html(cid)
    blocks.append(card("Homework", a["title"], f"""      <dl class="details-list">
        <div><dt>Due</dt><dd>{fmt_dt(gc.get('dueDate'))}</dd></div>
        <div><dt>Points</dt><dd>{gc.get('possible', 0):g}</dd></div>
        <div><dt>My grade</dt><dd>{score_text(cid)}</dd></div>
        <div><dt>My submission</dt><dd>{'<br>'.join(subs) or '—'}</dd></div>
      </dl>
      <h3>Instructor feedback</h3>
      {('<blockquote class="carcamo-interpretation">' + fb + '</blockquote>') if fb else '<p>None posted.</p>'}
      <h3>Instructions</h3>
      <div class="archive-body">
{clean_html((asmt.get('instructions') or {}).get('rawText'), FILES_HANDOUT)}
      </div>""", f"hw-{k}"))
write("assignments.html", "Homework (Archive)", "Homework",
      hero("Homework Assignments", "Homework, Instructions &amp; Feedback",
           "Each assignment as posted on Blackboard, with the handout files, my submission, my grade, and the instructor's written feedback.") + "".join(blocks))

# ---------- exams ----------
ex = []
for k, title in enumerate(["Practice Exam", "Mid-Term Exam Second Attempt"]):
    c = top[title]
    t = d["assessments"][c["id"]]["contentDetail"]["resource/x-bb-asmt-test-link"]["test"]
    asmt, gc, ds = t["assessment"], t["gradingColumn"], t["deploymentSettings"]
    cid = col_for(title)
    rows = "\n".join(
        f"          <tr><td>{i + 1}</td><td>{fmt_dt(at.get('attemptReceipt', {}).get('submissionDate'))}</td><td>{(at.get('displayGrade') or {}).get('score', '—'):g} / {gc.get('possible', 0):g}</td></tr>"
        for i, at in enumerate(sorted(attempts.get(cid, []), key=lambda x: x.get("created", ""))))
    ex.append(card("Exam", title, f"""      <dl class="details-list">
        <div><dt>Due</dt><dd>{fmt_dt(gc.get('dueDate'))}</dd></div>
        <div><dt>Questions</dt><dd>{asmt.get('questionCount', '—')}</dd></div>
        <div><dt>Points</dt><dd>{gc.get('possible', 0):g}</dd></div>
        <div><dt>Recorded grade</dt><dd>{score_text(cid)}</dd></div>
        <div><dt>Delivery</dt><dd>Proctored (LockDown Browser and Respondus Monitor){', ' + str(ds.get('attemptCount')) + ' attempts allowed' if ds.get('attemptCount') else ''}</dd></div>
      </dl>
      <div class="table-wrap"><table class="assignment-table">
        <thead><tr><th>Attempt</th><th>Submitted</th><th>Score</th></tr></thead>
        <tbody>
{rows}
        </tbody>
      </table></div>""", f"ex-{k}"))
write("exams.html", "Exams (Archive)", "Exams",
      hero("Exams", "Practice Exam &amp; Mid-Term",
           "Scores and attempt history. The questions and my answers could not be archived: Blackboard restricts review of these exams because they were secured for proctoring.") + "".join(ex))

# ---------- announcements ----------
anns = sorted(d["announcements"], key=lambda a: a["created"], reverse=True)
write("announcements.html", "Announcements (Archive)", "Announcements",
      hero("Course Communication", "Announcements", f"All {len(anns)} announcements, newest first.")
      + "".join(card(fmt_dt(a["created"]), a["title"], f'      <div class="archive-body">\n{clean_html(a["body"])}\n      </div>', f"a{k}") for k, a in enumerate(anns)))

# ---------- syllabus & policies ----------
syl = top["INFQ 70303 Fall 2026 Syllabus.pdf"]
write("syllabus.html", "Syllabus & Policies (Archive)", "Syllabus",
      hero("Course Document", "INFQ 70303 Syllabus &amp; University Policies", "The syllabus PDF and the university policy page as posted on Blackboard.")
      + card("Syllabus", "INFQ 70303 Fall 2026 Syllabus", f'      <p><a href="{href(local("general", "INFQ 70303 Fall 2026 Syllabus.pdf"))}">Open the syllabus (PDF, Blackboard version)</a></p>', "s")
      + card("Policies", "University Policies & Resources", f'      <div class="archive-body">\n{clean_html(top["University Policies & Resources"]["_children"][0]["body"])}\n      </div>', "p"))

# ---------- grades ----------
rows, earned, possible = [], 0, 0
for c in d["columns"]:
    cid = c["id"]
    g = grade_rec.get(cid) or {}
    sc = (g.get("displayGrade") or {}).get("score")
    if sc is not None:
        earned += sc; possible += c["score"]["possible"]
    fb = feedback_html(cid)
    rows.append(f"          <tr><td>{esc(c['name'])}</td><td>{fmt_dt(c.get('grading', {}).get('due'), False)}</td><td>{score_text(cid)}</td><td>{fb or '—'}</td></tr>")
write("grades.html", "Grades (Archive)", "Grades",
      hero("Gradebook", "Grades &amp; Feedback", f"Points earned on graded items: {earned:g} of {possible:g}. Written feedback is shown exactly as the instructor posted it.")
      + card("My Record", "Gradebook", f"""      <div class="table-wrap"><table class="assignment-table">
        <thead><tr><th>Item</th><th>Due</th><th>My grade</th><th>Instructor feedback</th></tr></thead>
        <tbody>
{chr(10).join(rows)}
        </tbody>
      </table></div>""", "gb"))

# ---------- recordings ----------
TOPICS = {
    "2026-08-25": "Program and Course Overview", "2026-08-27": "IQ Principles and Domains",
    "2026-09-01": "IQ Value and Business Impact", "2026-09-03": "Data Categories, Requirements & Data Exploration",
    "2026-09-08": "Quality Pioneers & the Evolution of Information Quality", "2026-09-10": "Principles of Data Quality Management & ISO 8000-61",
}
rec_rows = []
for date in sorted(os.listdir(ROOT / "recordings")):
    files = sorted(os.listdir(ROOT / "recordings" / date))
    def pick(suffix, label):
        f = next((x for x in files if x.endswith(suffix)), None)
        return f'<a href="{href(f"recordings/{date}/{f}")}">{label}</a>' if f else ""
    links = " · ".join(filter(None, [pick(".mp4", "Video"), pick(".m4a", "Audio"), pick(".transcript.vtt", "Transcript"), pick(".cc.vtt", "Captions")]))
    label = datetime.strptime(date, "%Y-%m-%d").strftime("%a, %b %d, %Y").replace(" 0", " ")
    rec_rows.append(f"          <tr><td>{label}</td><td>{esc(TOPICS.get(date, ''))}</td><td>{links}</td></tr>")
write("recordings.html", "Recordings (Archive)", "Recordings",
      hero("Lecture Recordings", "Class Recordings",
           "Zoom recordings of the class sessions whose links were saved on my lecture pages (Aug 25 to Sep 10). Later sessions had no recording link to download. Video and audio stay on this computer only (excluded from git); transcripts are kept with the site.")
      + card("Recordings", "Class Sessions", f"""      <div class="table-wrap"><table class="assignment-table">
        <thead><tr><th>Date</th><th>Topic</th><th>Files</th></tr></thead>
        <tbody>
{chr(10).join(rec_rows)}
        </tbody>
      </table></div>""", "rec"))

# ---------- archive home ----------
slides = "\n".join("        " + item_link(c, "lecture-slides") for c in top["Lecture Slides"]["_children"])
res = "\n".join("        " + item_link(c, "resources") for c in top["Resources"]["_children"])
home = hero("Course Archive", "INFQ 70303 Principles of Information Quality &mdash; Fall 2026",
            f"Instructor: Dr. John R. Talburt. A complete copy of the Blackboard course, captured {CAPTURED}: syllabus, lecture slides, homework with instructions and feedback, exams, resources, announcements, recordings, and my grades.") \
    + card("Course Documents", "Start Here", """      <ul class="link-list">
        <li><a href="syllabus.html">Syllabus &amp; University Policies</a></li>
        <li><a href="assignments.html">Homework, Instructions &amp; Feedback</a></li>
        <li><a href="exams.html">Practice Exam &amp; Mid-Term</a></li>
        <li><a href="grades.html">Grades &amp; Feedback</a></li>
        <li><a href="announcements.html">Announcements</a></li>
        <li><a href="recordings.html">Lecture Recordings</a></li>
      </ul>""", "start") \
    + card("Lecture Slides", "Lecture Slides", f'      <ul class="link-list">\n{slides}\n      </ul>', "slides") \
    + card("Resources", "Course Resources", f'      <ul class="link-list">\n{res}\n      </ul>', "res") \
    + card("Source Data", "Raw Blackboard Export", """      <ul class="link-list">
        <li><a href="raw/blackboard-dump.json">blackboard-dump.json</a> &mdash; content tree, assignments, announcements, gradebook, attempts</li>
        <li><a href="raw/blackboard-grades-feedback.json">blackboard-grades-feedback.json</a> &mdash; grade records with instructor feedback</li>
        <li><a href="raw/dedupe-map.json">dedupe-map.json</a> &mdash; downloaded files that already existed elsewhere in the site</li>
      </ul>""", "raw")
write("index.html", "Principles of IQ Course Archive", "Course Archive", home)
print("built:", sorted(p.name for p in ROOT.glob("*.html")))
