"""Build the Research Methods course archive pages from the raw Blackboard dumps."""
import html, json, os, re
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(r"e:/2026Fall/classes/research-methods/archive")
RAW = ROOT / "raw"
pub = json.load(open(RAW / "blackboard-dump.json", encoding="utf-8"))
prv = json.load(open(RAW / "blackboard-dump-private.json", encoding="utf-8"))
CAPTURED = "November 11, 2026"
BB = "https://blackboard.ualr.edu/ultra/courses/_294361_1/outline"

# ---------- helpers ----------
def central(iso):
    if not iso:
        return None
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    # US Central: CDT (UTC-5) until 2026-11-01 07:00 UTC, CST (UTC-6) after.
    off = -5 if dt < datetime(2026, 11, 1, 7, tzinfo=timezone.utc) else -6
    return dt + timedelta(hours=off), ("CDT" if off == -5 else "CST")

def fmt_dt(iso, with_time=True):
    r = central(iso)
    if not r:
        return "—"
    dt, tz = r
    s = dt.strftime("%a, %b %d, %Y").replace(" 0", " ")
    if with_time:
        s += " " + dt.strftime("%I:%M %p").lstrip("0") + f" {tz}"
    return s

def esc(s):
    return html.escape(s or "", quote=True)

# local file map: Blackboard resource id (rid / xid) -> archive-relative path
FILEMAP = {
    "68621384_1": "files/week-02/A Framework for Analysis of Data Quality Research.pdf",
    "68621385_1": "files/week-02/Fifteen Years of Data and Information Quality Literature.pdf",
    "68621386_1": "files/week-02/A Short Review of the Literature on Automatic Data Quality.pdf",
    "68621389_1": "files/week-03/Beyond Accuracy - What Data Quality Means to Data Consumers.pdf",
    "68621390_1": "files/week-03/Data Quality Assessment.pdf",
    "68621391_1": "files/week-03/Measuring Data Accuracy.pdf",
    "68621392_1": "files/week-03/A Cubic Framework For Chief Data Officers.pdf",
    "68621393_1": "files/week-03/A Balanced Scorecard for Maximizing Data Performance.pdf",
    "68621396_1": "files/week-04/Introduction to Design Science Research.pdf",
    "68621399_1": "files/week-05/A Brief Introduction to Experimental Design.pdf",
    "68621400_1": "files/week-05/Survey Design.pdf",
    "68621380_1": "files/week-07/Assessing Business Impact by Danette McGilvray.pdf",
    "68621381_1": "files/week-07/Danette McGilvray Presentation on Communication Techniques.pdf",
    "68621374_1": "files/assignment-files/Literature Review Assignment - Systematic Review on How Educators Teach AI in K-12 Education.pdf",
    "68621372_1": "files/assignment-files/CITI Training Assignment - Sample CITI Completion Report.jpg",
    "68621367_1": "files/assignment-files/Analysis Assignment - ma37grap-l1-quiz.pdf",
}
# content-item attachments (by content id) -> local path
ATTACH = {
    "_5994327_1": "../../Books/Ranjit_Kumar_Research_Methodology_A_Step.pdf",
    "_5994329_1": "../../Books/Art_of_Discovery_Oliver2.pdf",
    "_5994331_1": "../../Books/Student-Guide-to-AI-final-081224.pdf",
    "_6074876_1": "files/week-01/ResearchTypes.pdf",
    "_6071510_1": "files/week-01/TheDissertationResearchProposalProcess.pdf",
    "_5994336_1": "files/week-01/An Overview of Information Quality Research.pdf",
    "_5994375_1": "files/week-04/Navigating the Dissertation Process.pdf",
    "_5994388_1": "files/week-05/SurveyMonkey_71529783.pdf",
    "_5994389_1": "files/week-05/pierce-2016-07-state_of_iq_dg_report.pdf",
    "_5994398_1": "files/week-06/Sakthivel - IRB Request-emp.pdf",
    "_5994399_1": "files/week-06/Informed-Consent-Template-4-2-24.pdf",
    "_5994400_1": "files/week-06/Letter - NHPR 22-068.pdf",
}

# Archive files removed as duplicates of copies kept elsewhere in the site (archive-relative paths).
DEDUPE = {
    "files/week-01/An Overview of Information Quality Research.pdf": "../w01/An Overview of Information Quality Research.pdf",
    "files/week-02/Fifteen Years of Data and Information Quality Literature.pdf": "../w02/15YearsOfIQ_JISV25N1_20011.pdf",
    "files/week-02/A Framework for Analysis of Data Quality Research.pdf": "../w10/literature/Wang, 1995, A Framework for Analysis of Data Quality Research, IEEE TKDE.pdf",
    "files/week-02/A Short Review of the Literature on Automatic Data Quality.pdf": "../w10/literature/Chandran, 2022, A Short Review of the Literature on Automatic Data Quality, Journal of Computer and Communications.pdf",
    "files/assignment-files/Literature Review Assignment - Systematic Review on How Educators Teach AI in K-12 Education.pdf": "../w10/literature/Liu, 2024, A Systematic Review on How Educators Teach AI in K-12 Education, Educational Research Review.pdf",
    "files/my-submissions/Humanities Responsible Conduct of Research.pdf": "../CITI/Humanities Responsible Conduct of Research.pdf",
    "files/my-submissions/Research Security A Basic Course.pdf": "../CITI/Research Security A Basic Course.pdf",
    "files/my-submissions/Social and Behavioral Responsible Conduct of Research.pdf": "../CITI/Social and Behavioral Responsible Conduct of Research.pdf",
}

def href(path):
    path = DEDUPE.get(path, path)
    return esc(path.replace(" ", "%20").replace("#", "%23"))

def clean_html(raw):
    """Strip Blackboard markup down to plain semantic HTML; rewrite file links to local copies."""
    s = raw or ""
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", s, flags=re.S | re.I)

    def fix_a(m):
        attrs = m.group(1)
        hm = re.search(r'href="([^"]*)"', attrs)
        url = html.unescape(hm.group(1)) if hm else ""
        rid = re.search(r"xid-(\d+_1)", url)
        if rid and rid.group(1) in FILEMAP:
            return f'<a href="{href(FILEMAP[rid.group(1)])}">'
        yt = re.match(r"https://www\.youtube\.com/embed/([\w-]+)", url)
        if yt:
            url = f"https://www.youtube.com/watch?v={yt.group(1)}"
        if url:
            return f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">'
        return "<a>"
    s = re.sub(r"<a\b([^>]*)>", fix_a, s, flags=re.I)
    # drop attributes on every other tag
    s = re.sub(r"<(?!a\b)(\w+)\b[^>]*?(/?)>", lambda m: f"<{m.group(1)}{m.group(2)}>", s)
    s = re.sub(r"</?(span|div|font)>", "", s, flags=re.I)
    s = re.sub(r"</a>\s*<a", "</a><br><a", s)
    s = re.sub(r"(<br/?>\s*){2,}", "<br>", s)
    s = re.sub(r"<p>(\s|&nbsp;|<br/?>)*</p>", "", s)
    return s.strip()

def page(title, crumb, body, depth="../../../"):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta name="robots" content="noindex, nofollow">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <link rel="stylesheet" href="{depth}styles.css">
</head>
<body>
  <main class="page">
    <nav class="breadcrumb"><a href="{depth}index.html">Home</a> / <a href="../home-research-methods.html">Research Methods</a> / {crumb}</nav>
{body}
    <p class="lede"><small>Archived from Blackboard (INFQ 72203, Fall 2026) on {CAPTURED}.</small></p>
  </main>
  <script src="{depth}scripts/site-nav.js"></script>
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

# ---------- grade / attempt lookups ----------
cols = {c["id"]: c for c in pub["columns"] if "id" in c}
grades = {g["columnId"]: g for g in pub["myGrades"] if "columnId" in g}
col_by_name = {c["name"]: c for c in cols.values()}
attempt_by_col = {}
for cid, atts in pub["attempts"].items():
    for a in atts:
        if a.get("id"):
            attempt_by_col[cid] = prv["attempts"].get(a["id"], a)

def asmt_info(content_id):
    t = prv["assessments"][content_id]["content"]["contentDetail"]["resource/x-bb-asmt-test-link"]["test"]
    return t["assessment"], t["gradingColumn"]

def grade_text(col_id):
    g = grades.get(col_id, {})
    dg = g.get("displayGrade") or {}
    if "score" in dg:
        return f"{dg['score']:g} / {dg.get('possible', cols[col_id]['score']['possible']):g}"
    a = attempt_by_col.get(col_id)
    if a and a.get("status") in ("NEEDS_GRADING", "NeedsGrading"):
        return "Submitted, not graded yet"
    return "Not submitted"

def submission_links(col_id):
    a = attempt_by_col.get(col_id)
    if not a:
        return ""
    files = a.get("studentSubmissionFiles") or []
    links = ", ".join(f'<a href="{href("files/my-submissions/" + f["name"])}">{esc(f["name"])}</a>' for f in files)
    when = fmt_dt((a.get("attemptReceipt") or {}).get("submissionDate"))
    return f"{links} <small>(submitted {when})</small>" if links else ""

# ---------- weekly module pages ----------
def material_li(c):
    h = (c.get("contentHandler") or {})
    hid = h.get("id", "")
    title = esc(c["title"])
    desc = c.get("description") or ""
    d = f"<br><small>{esc(desc)}</small>" if desc else ""
    if hid == "resource/x-bb-externallink":
        return f'<li><a href="{esc(h.get("url"))}" target="_blank" rel="noopener noreferrer">{title}</a>{d}</li>'
    if c["id"] in ATTACH:
        return f'<li><a href="{href(ATTACH[c["id"]])}">{title}</a> <small>(PDF)</small>{d}</li>'
    return f"<li>{title}{d}</li>"

def assignment_block(c):
    asmt, gc = asmt_info(c["id"])
    col_id = gc.get("id") or col_by_name[c["title"]]["id"]
    instr = clean_html((asmt.get("instructions") or {}).get("rawText"))
    sub = submission_links(col_id)
    return f"""      <h3>{esc(c['title'])}</h3>
      <dl class="details-list">
        <div><dt>Due</dt><dd>{fmt_dt(gc.get('dueDate'))}</dd></div>
        <div><dt>Points</dt><dd>{gc.get('possible', 0):g}</dd></div>
        <div><dt>My grade</dt><dd>{grade_text(col_id)}</dd></div>
        <div><dt>My submission</dt><dd>{sub or '—'}</dd></div>
        <div><dt>Feedback</dt><dd>None posted on Blackboard as of {CAPTURED}</dd></div>
      </dl>
      <h4>Instructions</h4>
      <div class="archive-body">
{instr}
      </div>"""

modules = [c for c in pub["contents"] if (c.get("contentHandler") or {}).get("id") == "resource/x-bb-lesson"]
week_pages = []
for i, m in enumerate(modules):
    slug = "weeks-09-14" if m["title"].startswith("Weeks 9") else f"week-{int(re.search(r'Week (\d+)', m['title']).group(1)):02d}"
    week_pages.append((slug, m))

for idx, (slug, m) in enumerate(week_pages):
    parts = [f"""
    <header class="hero">
      <p class="eyebrow">Learning Module</p>
      <h1>{esc(m['title'])}</h1>
      <p class="lede">{esc(m.get('description'))}</p>
    </header>"""]
    n = 0
    for c in m.get("_children", []):
        n += 1
        hid = f"sec-{n}"
        h = (c.get("contentHandler") or {}).get("id", "")
        if h == "resource/x-bb-folder" and "Reading" in c["title"]:
            body = "".join(clean_html(x.get("body")) for x in c.get("_children", []))
            parts.append(card("Reading List", c["title"], f'      <div class="archive-body">\n{body}\n      </div>', hid))
        elif h == "resource/x-bb-folder":
            intro = f"      <p>{esc(c.get('description'))}</p>\n" if c.get("description") else ""
            lis = "\n".join("        " + material_li(x) for x in c.get("_children", []))
            parts.append(card("Class Materials", c["title"], f'{intro}      <ul class="link-list">\n{lis}\n      </ul>', hid))
        elif "asmt" in h:
            parts.append(card("Assignment", c.get("description") or "Assignment", assignment_block(c), hid))
    prev = f'<a href="{week_pages[idx-1][0]}.html">&larr; {esc(week_pages[idx-1][1]["title"])}</a>' if idx > 0 else ""
    nxt = f'<a href="{week_pages[idx+1][0]}.html">{esc(week_pages[idx+1][1]["title"])} &rarr;</a>' if idx + 1 < len(week_pages) else ""
    parts.append(f'\n    <nav class="meeting-nav">{prev} &nbsp; <a href="index.html">Archive home</a> &nbsp; {nxt}</nav>')
    (ROOT / f"{slug}.html").write_text(page(m["title"], f'<a href="index.html">Course Archive</a> / {esc(m["title"])}', "".join(parts)), encoding="utf-8")

# ---------- syllabus & policies ----------
def doc_body(title_prefix):
    item = next(c for c in pub["contents"] if c["title"].startswith(title_prefix))
    return clean_html(item["_children"][0]["body"])
syl = f"""
    <header class="hero">
      <p class="eyebrow">Course Document</p>
      <h1>INFQ 72203 Syllabus &amp; University Policies</h1>
      <p class="lede">The syllabus and the university policy page exactly as posted on Blackboard.</p>
    </header>""" + card("Syllabus", "INFQ 72203 Syllabus - Fall 2026", f'      <div class="archive-body">\n{doc_body("INFQ 72203 Syllabus")}\n      </div>', "syl") \
    + card("Policies", "University Policies & Resources", f'      <div class="archive-body">\n{doc_body("University Policies")}\n      </div>', "pol")
(ROOT / "syllabus.html").write_text(page("Syllabus & Policies (Archive)", '<a href="index.html">Course Archive</a> / Syllabus', syl), encoding="utf-8")

# ---------- announcements ----------
anns = sorted(pub["announcements"], key=lambda a: a["created"], reverse=True)
items = []
for k, a in enumerate(anns):
    by = (a.get("creator") or {})
    who = " ".join(filter(None, [(by.get("name") or {}).get("given"), (by.get("name") or {}).get("family")])) if isinstance(by, dict) else ""
    items.append(card(fmt_dt(a["created"]) + (f" · {who}" if who else ""), a["title"], f'      <div class="archive-body">\n{clean_html(a["body"])}\n      </div>', f"ann-{k}"))
ann_body = f"""
    <header class="hero">
      <p class="eyebrow">Course Communication</p>
      <h1>Announcements</h1>
      <p class="lede">All {len(anns)} announcements, newest first. Lecture recording links point to Zoom and stop working when access ends; local copies are on the <a href="recordings.html">recordings page</a>.</p>
    </header>""" + "".join(items)
(ROOT / "announcements.html").write_text(page("Announcements (Archive)", '<a href="index.html">Course Archive</a> / Announcements', ann_body), encoding="utf-8")

# ---------- grades ----------
rows = []
total_earned = total_possible = 0
for c in pub["columns"]:
    if c.get("grading", {}).get("type") == "Calculated":
        continue
    cid = c["id"]
    g = grades.get(cid, {})
    dg = g.get("displayGrade") or {}
    if "score" in dg:
        total_earned += dg["score"]; total_possible += c["score"]["possible"]
    due = c.get("grading", {}).get("due")
    rows.append(f"""          <tr><td>{esc(c['name'])}</td><td>{fmt_dt(due, False) if due else '—'}</td><td>{c['score']['possible']:g}</td><td>{grade_text(cid)}</td><td>{submission_links(cid) or '—'}</td></tr>""")
grades_body = f"""
    <header class="hero">
      <p class="eyebrow">Gradebook</p>
      <h1>Grades, Submissions &amp; Feedback</h1>
      <p class="lede">Graded so far: {total_earned:g} of {total_possible:g} points. No written feedback had been posted on any assignment as of {CAPTURED}.</p>
    </header>""" + card("My Record", "Gradebook", f"""      <div class="table-wrap"><table class="assignment-table">
        <thead><tr><th>Item</th><th>Due</th><th>Points</th><th>My grade</th><th>My submission</th></tr></thead>
        <tbody>
{chr(10).join(rows)}
        </tbody>
      </table></div>
      <p><small>Grading scale (syllabus): A 90–100, B 80–89, C 70–79, D 60–69, F below 60. Weekly assignments total 50 points; the Final Research Proposal is 50 points.</small></p>""", "gb")
(ROOT / "grades.html").write_text(page("Grades (Archive)", '<a href="index.html">Course Archive</a> / Grades', grades_body), encoding="utf-8")

# ---------- recordings ----------
REC = [
    ("2026-08-24", "Week 1"), ("2026-08-31", "Week 2"), ("2026-09-14", "Week 3"), ("2026-09-21", "Week 4"),
    ("2026-09-28", "Week 5"), ("2026-10-05", "Week 6"), ("2026-10-12", "Week 7"), ("2026-10-19", "Week 8"), ("2026-10-26", "Week 9"),
]
rec_rows = []
for date, wk in REC:
    d = ROOT / "recordings" / date
    files = sorted(os.listdir(d)) if d.exists() else []
    def pick(pred, label):
        f = next((x for x in files if pred(x)), None)
        return f'<a href="{href(f"recordings/{date}/{f}")}">{label}</a>' if f else ""
    links = " · ".join(filter(None, [
        pick(lambda x: x.endswith(".mp4"), "Video"),
        pick(lambda x: x.endswith(".m4a"), "Audio"),
        pick(lambda x: x.endswith(".transcript.vtt") or x.endswith(".txt"), "Transcript"),
        pick(lambda x: x.endswith(".cc.vtt"), "Captions"),
    ]))
    if not links:
        links = "Not archived: Zoom asked for a passcode that was not posted"
    label = datetime.strptime(date, "%Y-%m-%d").strftime("%a, %b %d, %Y").replace(" 0", " ")
    rec_rows.append(f"          <tr><td>{label}</td><td>{wk}</td><td>{links}</td></tr>")
rec_body = f"""
    <header class="hero">
      <p class="eyebrow">Lecture Recordings</p>
      <h1>Class Recordings</h1>
      <p class="lede">Zoom recordings of the Monday class sessions, downloaded from the links in the announcements. Video and audio files stay on this computer only (they are excluded from git); transcripts are kept with the site.</p>
    </header>""" + card("Recordings", "Monday Sessions", f"""      <div class="table-wrap"><table class="assignment-table">
        <thead><tr><th>Date</th><th>Course week</th><th>Files</th></tr></thead>
        <tbody>
{chr(10).join(rec_rows)}
        </tbody>
      </table></div>""", "rec")
(ROOT / "recordings.html").write_text(page("Recordings (Archive)", '<a href="index.html">Course Archive</a> / Recordings', rec_body), encoding="utf-8")

# ---------- archive home ----------
ebooks = next(c for c in pub["contents"] if c["title"].startswith("INFQ 72203 E-Books"))
eb = "\n".join("        " + material_li(x) for x in ebooks["_children"])
week_list = "\n".join(f'        <li><a href="{s}.html">{esc(m["title"])}</a><br><small>{esc((m.get("description") or "")[:180])}{"…" if len(m.get("description") or "") > 180 else ""}</small></li>' for s, m in week_pages)
home = f"""
    <header class="hero">
      <p class="eyebrow">Course Archive</p>
      <h1>INFQ 72203 Research Methods &mdash; Fall 2026</h1>
      <p>Instructors: Dr. Ningning Wu and Dr. Serhan Dagtas</p>
      <p class="lede">A complete copy of the Blackboard course, captured {CAPTURED}: every module, reading list, class material, assignment instruction, announcement, lecture recording, and my grades and submissions.</p>
    </header>""" \
    + card("Course Documents", "Start Here", """      <ul class="link-list">
        <li><a href="syllabus.html">Syllabus &amp; University Policies</a></li>
        <li><a href="announcements.html">Announcements</a></li>
        <li><a href="recordings.html">Lecture Recordings</a></li>
        <li><a href="grades.html">Grades, Submissions &amp; Feedback</a></li>
      </ul>""", "start") \
    + card("Course Content", "Learning Modules", f'      <ol class="link-list">\n{week_list}\n      </ol>', "mods") \
    + card("Course Books", "E-Books Folder", f'      <p>{esc(ebooks.get("description"))}</p>\n      <ul class="link-list">\n{eb}\n      </ul>', "books") \
    + card("Source Data", "Raw Blackboard Export", """      <p>The JSON files this archive was built from, straight from the Blackboard API.</p>
      <ul class="link-list">
        <li><a href="raw/blackboard-dump.json">blackboard-dump.json</a> &mdash; content tree, announcements, gradebook</li>
        <li><a href="raw/blackboard-dump-private.json">blackboard-dump-private.json</a> &mdash; assignment instructions and submission records</li>
      </ul>""", "raw")
(ROOT / "index.html").write_text(page("Research Methods Course Archive", "Course Archive", home), encoding="utf-8")
print("built:", sorted(p.name for p in ROOT.glob("*.html")))
