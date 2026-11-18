"""Turn the W01 builder (copied to build_u01.py) into the U01 builder. Run once on a fresh copy."""
import os, shutil
here = os.path.dirname(os.path.abspath(__file__))
shutil.copy(os.path.join(here, 'build.py'), os.path.join(here, 'build_u01.py'))
f = os.path.join(here, 'build_u01.py')
t = open(f, encoding='utf-8').read()


def sub(a, b, count=1):
    global t
    assert t.count(a) == count, (t.count(a), a[:80])
    t = t.replace(a, b)


def cut(start, end, new):
    """replace text from marker start (inclusive) to marker end (exclusive)"""
    global t
    i0 = t.index(start)
    i1 = t.index(end, i0)
    t = t[:i0] + new + t[i1:]


# ---------------------------------------------------------------- paths, status
sub(r"06-study\sample\diagrams\W01.svg", r"06-study\sample-uic\diagrams\U01.svg")
sub(r"06-study\sample\diagrams\W01.pdf", r"06-study\sample-uic\diagrams\U01.pdf")
sub('''db = sqlite3.connect(os.path.join(ROOT, r'04-literature\\casing-analysis\\casing_specs.db'))
status = dict(db.execute("select s.requirement_code, r.status from diagram_requirement_results r "
                         "join spec_requirements s using(requirement_id) where r.diagram_number='W01'"))
''', '''# Presence decisions for U01 (reference record; reviewer Lester S. Carcamo)
U01_MET = {1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 17, 18, 32, 35, 36, 37, 38, 39, 40, 43, 44, 45, 46, 81, 88}  # checklist v4.1 numbering
U01_NA = {90}   # (c) borehole designation: one borehole shown (\"Original Hole\" only) -> NOT_APPLICABLE
status = {c: ('MET' if n in U01_MET else 'NA' if n in U01_NA else 'MISSING') for n, c, _ in pts}
''')
sub("CX0, CY0, CX1, CY1 = 24, 6, 608, 772", "CX0, CY0, CX1, CY1 = 26, 12, 592, 772")

# ---------------------------------------------------------------- frames, categories
cut("# ================================================================ MET frames: code -> (word list, route)",
    "mtype_of = {}",
    r'''# ================================================================ MET frames: code -> (word list, route)
GP = 0.8   # group-frame padding (pt)


def Wp(prefix, near):
    c = [w for w in words if w[4].startswith(prefix)]
    c.sort(key=lambda w: abs(w[0] - near[0]) + abs(w[1] - near[1]))
    return c[0]


def part(w, i0, i1):
    """pseudo-word for characters [i0:i1] of a PDF word (Times metrics, proportional)"""
    s_ = w[4]
    full = fitz.get_text_length(s_, fontname='tiro', fontsize=10)
    a = fitz.get_text_length(s_[:i0], fontname='tiro', fontsize=10) / full
    b = fitz.get_text_length(s_[:i1], fontname='tiro', fontsize=10) / full
    x0 = w[0] + (w[2] - w[0]) * a
    x1 = w[0] + (w[2] - w[0]) * b
    return (x0, w[1], x1, w[3], s_[i0:i1])


LOGO = (36.0, 18.7, 91.4, 39.6, 'bry logo')        # raster logo, bbox from page.get_image_info()
fill_tok = W('10.0-1,078.0;')
plug_tok = W('980.0-1,078.0;')
F_ = {
    '(a)(1).operator_name': ([LOGO], 'h'),
    '(a)(1).lease_name': ([W('Hill')], 'h'),
    '(a)(1).well_number': ([W('44MW')], 'h'),
    '(a)(1).api_number': ([W('0403050708')], 'h'),
    '(a)(2).spud_date': ([W('8/10/2013')], 'h'),
    '(a)(3).ground_elevation': ([W('598.90')], 'h'),
    '(a)(4).reference_elevation': ([W('608.90')], 'h'),
    '(a)(7).casing_size': (row(130, 150, 370, 400), 'h'),
    '(a)(7).casing_grade': (row(130, 150, 445, 470), 'h'),
    '(a)(7).connection_type': (row(130, 150, 490, 515), 'h'),
    '(a)(7).casing_weight': (row(130, 150, 420, 445), 'h'),
    '(a)(8).shoe_depth.md': (row(130, 150, 555, 600), 'h'),
    '(a)(9).perforation_depths.md': (row(200, 272, 365, 395), 'h'),
    '(a)(9).perforation_intervals.md': (row(200, 272, 433, 460), 'h'),
    '(a)(10).other_equipment': (row(336, 505, 255, 600), 'h'),
    '(b)(3).inclination': (row(182, 190, 55, 119), 'h'),
    '(b)(2).cement_job_identification': ([W('8/1/2013')], 'h'),
    '(a)(12).cement_plug_identification': (row(649, 656, 165, 260) + [W('(plug);')], 'h'),
    '(a)(12).cement_plug_top.md': ([part(plug_tok, 0, 5)], 'h'),
    '(a)(12).cement_plug_bottom.md': ([part(plug_tok, 6, 13)], 'h'),
    '(a)(13).cement_fill_identification': (row(430, 437, 165, 260), 'h'),
    '(a)(13).cement_fill_top.md': ([part(fill_tok, 0, 4)], 'h'),
    '(a)(13).cement_fill_bottom.md': ([part(fill_tok, 5, 12)], 'h'),
    '(a)(15).formation_names': ([W('Tulare')], 'h'),
    '(a)(15).formation_depths.md': ([W('359.6')], 'h'),
    '(a)(15).zone_names': ([Wp('San', (55, 608)), Wp('…', (65, 608))], 'h'),
    '(a)(15).zone_depths.md': ([W('934.4')], 'h'),
}
CHAN = {}
assert set(met) == set(F_), (set(met) ^ set(F_))
GF = {c: box(ws, GP) for c, (ws, _) in F_.items()}

# ================================================================ red frames: present but not required (excess data)
RED = []  # [name, reason, bbox]
LOC = 'well location data is not listed in § 1724.7.1(a) (lat/long appears only in the DOC state-contract template)'
for lab_, ws_ in [('Field name', [W('SOUTH'), W('BELRIDGE')]), ('County', [W('Kern'), W('030')]), ('State', [W('CA')]),
                  ('Section', [W('19')]), ('Township', [W('28S')]), ('Range', [W('21E')]),
                  ('Survey', [W('NW'), W('Corner')]), ('Latitude', [W('35.4782753000')]), ('Longitude', [W('-119.7516403200')])]:
    RED.append([f'Location: {lab_}', LOC, box(ws_, 0.7)])
RED.append(['KB-ground height "10.00"', 'derived from the two required elevations; not itself listed in (a)', box([W('10.00')], 0.7)])
RED.append(['Rig release date "8/11/2013"', 'rig-release date is not listed in (a)', box([W('8/11/2013', (263, 94))], 0.7)])
RED.append(['TD date "8/11/2013"', 'TD date is not listed in (a)', box([W('8/11/2013', (323, 94))], 0.7)])
RED.append(['Operated? "Yes"', 'operated flag is not listed in (a)', box([W('Yes')], 0.7)])
for w in sorted(row(200, 272, 255, 300), key=lambda w: w[1]):
    RED.append([f'Perforation date "{w[4]}"', 'perforation dates are not listed in (a)(9)', box([w], 0.7)])
NEUTRAL = []
NAFR = [['Wellbore designation "Original Hole"', 'point 90 is NOT_APPLICABLE: the diagram shows one borehole only', box([W('Original'), W('Hole,')], 0.8)]]
OPERATOR = 'Berry (bry logo; no text name)'
DIAGRAM_DATE = '10/31/2023'
EVID = {'(a)(1).operator_name': 'bry (logo image)'}
EXTRA_TXT = {}
EXTRA_FR = {'(b)(2).cement_job_identification': [box([W('8/11/2013', (207, 439))], 0.6), box([W('8/11/2013', (170, 665))], 0.6)]}
EXTRA_BADGE = {'(b)(2).cement_job_identification': [(172.0, 461.5), (172.0, 675.0)]}   # blank space under each callout
PROV = [
    ['Profile timestamp "10/31/2023 1:57:05 PM"', '', box([W('10/31/2023', (160, 184)), W('1:57:05'), W('PM')], 0.8)],
    ['Report source "www.peloton.com"', '', box([W('www.peloton.com')], 0.8)],
    ['Page number "Page 1/1"', '', box([W('Page'), W('1/1')], 0.8)],
    ['Report printed "Report Printed: 10/31/2023"', '', box([W('Report'), W('Printed:'), W('10/31/2023', (548, 761))], 0.8)],
]
print(f'red frames {len(RED)}; dashed slate {len(NEUTRAL)}; provenance {len(PROV)}')
MTYPES = [  # (id, label, name prefixes)
    ('E1', 'Well location (field, county, PLSS, lat/long)', ['Location:']),
    ('E2', 'KB-ground height', ['KB-ground']),
    ('E3', 'Rig-release and TD dates', ['Rig release', 'TD date']),
    ('E4', '"Operated?" flag', ['Operated?']),
    ('E5', 'Perforation dates', ['Perforation date']),
]
''')
# inset loop and obstacles already use RED + NEUTRAL + PROV

sub("    ('g7', '(a)(13) Cement fill', [13], '#332288'),", "    ('g7', '(a)(12)–(13) Cement plugs, fill', [12, 13], '#332288'),")
# ---------------------------------------------------------------- texts
sub("o.append('<title>W01 atomic data-point map</title>')", "o.append('<title>U01 atomic data-point map</title>')")
sub("f'Casing diagram W01: {n_total} atomic data points, 14 CCR § 1724.7.1(a)</text>')",
    "f'Casing diagram U01: {n_total} atomic data points, 14 CCR § 1724.7.1(a) · PROVISIONAL</text>')")
sub("""{n_met} MET (coloured by requirement group, framed and '
         f'numbered in W01) · {n_total - n_met} MISSING (grey) · red frames: present but not required · completeness {score * 100:.1f}%</text>')""",
    """Provisional — Claude\\'s review, not the frozen human reference · {n_met} MET · '
         f'{n_total - n_met} MISSING · completeness {score * 100:.1f}% · Hill 44MW, API 0403050708 (Berry, South Belridge)</text>')""")
sub("'MISSING: no answer in W01, no line'", "'MISSING: no answer in U01, no line'")
sub("o.append(text(LX + 21, LY, 'Document provenance: who prepared'))\no.append(text(LX + 21, LY + 10.4, 'the diagram and when; not required'))",
    "o.append(text(LX + 21, LY, 'Document provenance: report source,'))\no.append(text(LX + 21, LY + 10.4, 'print/run time, page; not required'))")
sub("""SLATE_ROWS = [('"Wellbore: 00"', '§1724.7.1(c)'), ('"Type: Producer"', '§1724.7(a)(3)(D)'),
              ('Cement REMARKS ×2', '§1724.7.1(b)(2)'), ('Cement job type/date ×2', '§1724.7.1(b)(2)'),
              ('"Orientation: Directional"', '§1724.7.1(b)(3)'), ('Casing tops ×6', 'CalGEM P&A guidance')]""",
    """SLATE_ROWS = [('"Original Hole"', '§1724.7.1(c)'), ('"Deviated (15° to 30°)"', '§1724.7.1(b)(3)'),
              ('Cement job dates ×3', '§1724.7.1(b)(2)')]""")
sub("o.append(text(SX, SY, 'Completeness score (Equation 1)', 9.3, '#111', 'bold'))",
    "o.append(text(SX, SY, 'Completeness score (Equation 1) — provisional', 9.3, '#111', 'bold'))")
sub("f'Completeness(W01) = {n_met}", "f'Completeness(U01) = {n_met}")
sub("""'rows with no TVD cell are non-depth items. W01 is directional but reports MD only, so every TVD point is MISSING. '
     'Repeated data are framed at one representative instance.'),
    ('Sources.', 'casing-diagram-atomic-checklist-v2.txt; casing_specs.db, diagram_requirement_results (W01), checked against '
     'W01.pdf; frame positions from PDF text boxes.'),""",
    """'rows with no TVD cell are non-depth items. U01 is deviated (15° to 30°) but reports MD only, so every TVD point is MISSING. '
     'Repeated data are framed at one representative instance.'),
    ('Sources.', 'casing-diagram-atomic-checklist-v3.txt (78 points); U01.pdf (sample-uic). MET/MISSING: Claude\\'s provisional review; '
     'U01 has no human reference in casing_specs.db. Frame positions from PDF text boxes.'),""")
sub("o.append(text(MX, MY, 'Excess data found in W01', 9.3, '#111', 'bold'))", "o.append(text(MX, MY, 'Excess data found in U01', 9.3, '#111', 'bold'))")
sub("""o.append(text(MX, MY, 'Records who prepared the diagram and when.', FS, '#444'))
MY += 11
o.append(f'<rect x="{MX + 0.5}" y="{MY - 7.6}" width="15" height="9" fill="none" stroke="{PROVC}" stroke-width="1.0" stroke-dasharray="0.1 1.6" stroke-linecap="round"/>')
o.append(text(MX + 23, MY, '"Initials: xyz  Date: 11/30/2023"'))
o.append(text(MR, MY, f'×{len(PROV)}', FS, '#111', None, 'end'))
right_bottom = MY
""", """o.append(text(MX, MY, 'Records how and when the report was produced.', FS, '#444'))
for p_ in PROV:
    MY += 10.6
    o.append(f'<rect x="{MX + 0.5}" y="{MY - 7.6}" width="15" height="9" fill="none" stroke="{PROVC}" stroke-width="1.0" stroke-dasharray="0.1 1.6" stroke-linecap="round"/>')
    o.append(text(MX + 23, MY, p_[0].split(' "')[1].rstrip('"') if ' "' in p_[0] else p_[0]))
    o.append(text(MR, MY, '×1', FS, '#111', None, 'end'))
right_bottom = MY
""")
sub("    tags[k_] = best_[1]\n",
    "    for pref_, (px_, py_) in {'Production casing cement job date': (172.0, 461.5),\n"
    "                              'Production casing cement (plug) job date': (172.0, 675.0)}.items():\n"
    "        if nt[0].startswith(pref_ + ' \"'):\n"
    "            fx0, fy0 = P(px_, py_)\n"
    "            best_ = (0.0, (fx0, fy0, fx0 + tw_, fy0 + TH))\n"
    "    tags[k_] = best_[1]\n")
sub(r"06-study\design\prompts\casing-diagram-atomic-checklist-v2.txt", r"06-study\design\prompts\casing-diagram-atomic-checklist-v3.txt")
sub("    ('g6', '(a)(11) Hole size, depth', [11], '#8C564B'),", "    ('g6', '(a)(10)–(11) Other equipment; hole', [10, 11], '#8C564B'),")
sub("'Completeness = number of atomic data points marked MET ÷ 77'", "'Completeness = number of atomic data points marked MET ÷ 78'")
sub("'this diagram; not one of the 77'", "'this diagram; not one of the 78'")
sub("atomic data points, 14 CCR § 1724.7.1(a) · PROVISIONAL", "atomic data points (checklist v3), 14 CCR § 1724.7.1(a) · PROVISIONAL")
sub("def label(lab):\n    return lab.replace(' (MD)', '')\n",
    "def label(lab):\n    lab = lab.replace('Other equipment in the well (e.g., tubing, pumps, rods)', 'Other equipment in the well')\n"
    "    return lab.replace(' (MD)', '')\n")
sub("print('badge costs (dark px + penalties):'",
    "# U01 hand placements: blank cell space next to the frame (automatic spots covered callout text)\n"
    "_x, _y = P(578.0, 337.6)\n"
    "badges['(a)(10).other_equipment'] = (_x, _y, _x + tw('32', True) + 3.6, _y + BH)\n"
    "_x, _y = P(296.0, 201.6)\n"
    "mbadges = [(m_, ((_x, _y, _x + tw('E5', True) + 4, _y + MH) if m_ == 'E5' else r_)) for m_, r_ in mbadges]\n"
    "print('badge costs (dark px + penalties):'")

# ======== v4 (U01 only) ========
sub(r"casing-diagram-atomic-checklist-v3.txt'), encoding='utf-8')", r"casing-diagram-atomic-checklist-v4.1.txt'), encoding='utf-8')")
sub("""score = n_met / n_total
print(f'points {n_total} (md/non-depth {n_md}, tvd {n_tvd}); MET {n_met} = {met_md}+{met_tvd}; score {score:.4f}')""",
"""ad_pts = [p for p in pts if p[0] <= 78]
bc_pts = [p for p in pts if p[0] >= 79]
met_ad = sum(status[c] == 'MET' for _, c, _ in ad_pts)
met_ad_md = sum(status[c] == 'MET' for n, c, _ in md if n <= 78)
n_ad_md = sum(1 for n, c, _ in md if n <= 78)
met_bc = sum(status[c] == 'MET' for _, c, _ in bc_pts)
app_bc = sum(status[c] != 'NA' for _, c, _ in bc_pts)
n_app = len(ad_pts) + app_bc
n_na = n_total - n_app
assert met_ad + met_bc == n_met
score = n_met / n_app
print(f'points {n_total}; (a)/(d) MET {met_ad} of {len(ad_pts)} (MD/non-depth {met_ad_md} of {n_ad_md}, TVD {met_tvd} of {n_tvd}); '
      f'(b)/(c) MET {met_bc} of {app_bc} applicable; total {n_met} / {n_app} = {score:.4f}')""")
sub("""def group_of(code):
    n = int(re.match(r'\\(a\\)\\((\\d+)\\)', code)[1])""",
"""def group_of(code):
    m_ = re.match(r'\\(a\\)\\((\\d+)\\)', code)
    if not m_:
        return GBC
    n = int(m_[1])""")
sub("    ('g3', '(a)(5)–(6) Freshwater/USDW base', [5, 6], '#56B4E9'),\n",
    "    ('g3', '(b)–(c) Cement data, wellbore path', [], '#56B4E9'),   # U01: (a)(5)-(6) unused, colour reused\n")
sub("\n\ndef lum(hexc):", "\nGBC = [g for g in GROUPS if g[0] == 'g3'][0]\n\n\ndef lum(hexc):")
sub("PH, PITCH, PADX = 9.6, 11.4, 3.0", "PH, PITCH, PADX = 9.0, 10.0, 3.0")
sub("used_groups = [g for g in GROUPS if any(group_of(c) is g for c in met)]",
    "used_groups = sorted([g for g in GROUPS if any(group_of(c) is g for c in met)], key=lambda g: g is GBC)")
sub("""def rowy(i):
    return ROW0 + i * PITCH + PH / 2""",
"""def rowgap(i):
    return 1 if md[i][0] >= 79 else 0   # one header row before the (b)-(c) block


def rowy(i):
    return ROW0 + (i + rowgap(i)) * PITCH + PH / 2""")
sub("""def label(lab):
    lab = lab.replace('Other equipment in the well (e.g., tubing, pumps, rods)', 'Other equipment in the well')
""", """SHORT = {'Other equipment in the well (e.g., tubing, pumps, rods)': 'Other equipment in the well',
         'Cement-yield calculation steps': 'Cement-yield calc. steps',
         'Cement job identification (date or stage)': 'Cement job identification',
         'Slurry volume (or sacks) for each cement job': 'Slurry volume (or sacks)',
         'Slurry density for each cement job': 'Slurry density',
         'Slurry yield for each cement job': 'Slurry yield',
         'Cement type for each cement job': 'Cement type',
         'Cement additives for each cement job': 'Cement additives',
         'Wellbore path: measured depth (MD)': 'Wellbore path: MD',
         'Borehole designation (original hole, redrill, or sidetrack; conditional: multiple boreholes only)': 'Borehole designation: N/A'}


def label(lab):
    lab = SHORT.get(lab, lab)
""")
sub("""    g = group_of(code) if status[code] == 'MET' else None
    if g:
        f, st, t = g[3], g[3], ink(g[3])
    else:
        f, st, t = GREY_F, GREY_S, GREY_T
    r = f'<rect x="{x}" y="{y:.2f}" width="{w}" height="{PH}" rx="{PH / 2}" fill="{f}" stroke="{st}" stroke-width="0.55"/>'""",
"""    g = group_of(code) if status[code] == 'MET' else None
    dash = ''
    if g:
        f, st, t = g[3], g[3], ink(g[3])
    elif status[code] == 'NA':
        f, st, t, dash = '#ffffff', NAC, NAC, ' stroke-dasharray="2.2 1.4"'
    else:
        f, st, t = GREY_F, GREY_S, GREY_T
    r = f'<rect x="{x}" y="{y:.2f}" width="{w}" height="{PH}" rx="{PH / 2}" fill="{f}" stroke="{st}" stroke-width="0.7"{dash}/>'""")
sub("REDC = '#d62728'\n", "REDC = '#d62728'\nNAC = '#6b6b6b'\n")
sub("""for i, (n, c, lab) in enumerate(md):
    y = ROW0 + i * PITCH
""", """for i, (n, c, lab) in enumerate(md):
    y = ROW0 + (i + rowgap(i)) * PITCH
    if n == 79:
        o.append(f'<text x="{X1 + PADX}" y="{y - PITCH + PH / 2 + 3.0:.2f}" font-size="{FS}" font-weight="bold" fill="#333">'
                 f'§ 1724.7.1(b)–(c) (no TVD pair)</text>')
""")
sub("rows_bottom = ROW0 + len(md) * PITCH", "rows_bottom = ROW0 + (len(md) + 1) * PITCH")
# N/A frame + badge for point 89 (drawn with the slate/provenance frames)
sub("for name, why, (a, b, c2, d) in PROV:\n",
    """for name, why, (a, b, c2, d) in NAFR:
    x0, y0 = P(a, b); x1, y1 = P(c2, d)
    o.append(f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{x1 - x0:.2f}" height="{y1 - y0:.2f}" fill="none" stroke="{NAC}" '
             f'stroke-width="0.9" stroke-dasharray="2.2 1.4"><title>{name}: {why}</title></rect>')
    bx_, by_ = P(a + 1.0, b - 10.6)
    bw_ = tw('90 N/A', True) + 4
    o.append(f'<rect x="{bx_:.2f}" y="{by_:.2f}" width="{bw_:.2f}" height="9" rx="1.5" fill="#ffffff" stroke="{NAC}" stroke-width="0.7" stroke-dasharray="2.2 1.4"/>'
             f'<text x="{bx_ + bw_ / 2:.2f}" y="{by_ + 7.5:.2f}" font-size="{FS}" font-weight="bold" fill="{NAC}" text-anchor="middle">90 N/A</text>')
for name, why, (a, b, c2, d) in PROV:
""")
sub("for r in RED + NEUTRAL + PROV:", "for r in RED + NEUTRAL + PROV + NAFR:", 2)
# key: compact red / N/A / slate / provenance entries; drop the slate list (folded into the legend)
cut("""o.append(f'<rect x="{LX + 0.5}" y="{LY - 7.6}" width="15" height="9" fill="none" stroke="{REDC}" stroke-width="0.7" rx="0.8"/>')""",
    "\n\ndef wrap(",
    """o.append(f'<rect x="{LX + 0.5}" y="{LY - 7.6}" width="15" height="9" fill="none" stroke="{REDC}" stroke-width="0.7" rx="0.8"/>')
for k_, s_ in enumerate(['Red frame: Excess data — present, not', 'required by the specification; not scored',
                         '(overproduction; Ubarana et al., 2021)']):
    o.append(text(LX + 21, LY + 10.4 * k_, s_))
LY += 2 * 10.4 + 13
o.append(f'<rect x="{LX}" y="{LY - 7.4}" width="16" height="{PH}" rx="{PH / 2}" fill="#ffffff" stroke="{NAC}" stroke-width="0.7" stroke-dasharray="2.2 1.4"/>')
for k_, s_ in enumerate(['Dashed grey: not applicable to U01', '(90: only one borehole shown); not in', 'the denominator']):
    o.append(text(LX + 21, LY + 10.4 * k_, s_))
LY += 2 * 10.4 + 13
assert len(NEUTRAL) == 0
o.append(f'<rect x="{LX + 0.5}" y="{LY - 7.6}" width="15" height="9" fill="none" stroke="{PROVC}" stroke-width="1.0" stroke-dasharray="0.1 1.6" stroke-linecap="round"/>')
for k_, s_ in enumerate(['Dotted: document provenance (source,', 'print/run time, page); not required']):
    o.append(text(LX + 21, LY + 10.4 * k_, s_))
left_bottom = LY + 10.4""")
sub("LY += 2\no.append(f'<rect x=\"{LX}\" y=\"{LY - 7.4}\" width=\"16\" height=\"{PH}\" rx=\"{PH / 2}\" fill=\"{GREY_F}\"",
    "LY += 1\no.append(f'<rect x=\"{LX}\" y=\"{LY - 7.4}\" width=\"16\" height=\"{PH}\" rx=\"{PH / 2}\" fill=\"{GREY_F}\"")
sub("    o.append(text(LX + 21, LY, g[1].replace('&', '&amp;')))\n    LY += 10.6\n",
    "    o.append(text(LX + 21, LY, g[1].replace('&', '&amp;')))\n    LY += 10.2\n")
sub("LY = rows_bottom + 15\n", "LY = rows_bottom + 13\n")
# score block
sub("""o.append(text(SX, SY, 'Completeness = number of atomic data points marked MET ÷ 78', FS, '#111', 'bold'))
SY += 11.5
for t_ in [f'MD / non-depth points MET: {met_md} of {n_md}', f'TVD points MET: {met_tvd} of {n_tvd}',
           f'Total MET: {met_md} + {met_tvd} = {n_met}']:
    o.append(text(SX + 8, SY, t_))
    SY += 10.4
o.append(text(SX + 8, SY + 1, f'Completeness(U01) = {n_met} ÷ {n_total} = {score:.3f} → {score * 100:.1f}%', 10.0, '#111', 'bold'))""",
"""o.append(text(SX, SY, 'Completeness = points marked MET ÷ applicable points', FS, '#111', 'bold'))
SY += 11.5
for t_ in [f'(a), (d) MET: {met_ad} of {len(ad_pts)} (MD/non-depth {met_ad_md} of {n_ad_md}; TVD {met_tvd} of {n_tvd})',
           f'(b), (c) MET: {met_bc} of {app_bc} applicable (90 N/A: one borehole)',
           f'Total MET: {met_ad} + {met_bc} = {n_met}; applicable: {len(ad_pts)} + {app_bc} = {n_app}']:
    o.append(text(SX + 8, SY, t_))
    SY += 10.4
o.append(text(SX + 8, SY + 1, f'Completeness(U01) = {n_met} ÷ {n_app} = {score:.3f} → {score * 100:.1f}%', 10.0, '#111', 'bold'))""")
cut("notes = [\n", "]\nfor pre, body in notes:",
    """notes = [
    ('MD vs TVD.', 'MD (measured depth) runs along the borehole; TVD (true vertical depth) is the vertical depth of the same '
     'point. A row\\'s MD and TVD cells are one datum scored as two points; (b)–(c) points have no TVD pair. U01 is deviated '
     '(15° to 30°) but reports MD only, so every TVD point is MISSING. Repeated data are framed once.'),
    ('Sources.', 'casing-diagram-atomic-checklist-v4.2.txt (90 points); U01.pdf (sample-uic). MET/MISSING/N/A: Claude\\'s '
     'provisional review; no human reference exists. Frames from PDF text boxes.'),
""")
sub("atomic data points (checklist v3), 14 CCR § 1724.7.1(a) · PROVISIONAL", "atomic data points (checklist v4.2), 14 CCR § 1724.7.1 · PROVISIONAL")
sub("f'{n_total - n_met} MISSING · completeness", "f'{n_app - n_met} MISSING · {n_na} N/A · completeness")
sub("'not one of the 78'", "'not one of the 89'", 0) if False else None

# ======== v4.1 (U01 only): extra frames + badges for multi-instance points ========
sub("""    bx0, by0, bx1, by1 = badges[c]
    o.append(f'<rect x="{bx0:.2f}" y="{by0:.2f}" width="{bx1 - bx0:.2f}" height="{BH}" rx="2" fill="{col}" stroke="#fff" stroke-width="0.4"/>'
             f'<text x="{(bx0 + bx1) / 2:.2f}" y="{by0 + BH / 2 + 3.05:.2f}" font-size="{FS}" font-weight="bold" fill="{ink(col)}" text-anchor="middle">{l["n"]:02d}</text>')
""", """    bx0, by0, bx1, by1 = badges[c]
    o.append(f'<rect x="{bx0:.2f}" y="{by0:.2f}" width="{bx1 - bx0:.2f}" height="{BH}" rx="2" fill="{col}" stroke="#fff" stroke-width="0.4"/>'
             f'<text x="{(bx0 + bx1) / 2:.2f}" y="{by0 + BH / 2 + 3.05:.2f}" font-size="{FS}" font-weight="bold" fill="{ink(col)}" text-anchor="middle">{l["n"]:02d}</text>')
    for k_, eb in enumerate(EXTRA_FR.get(c, [])):
        ex0, ey0 = P(eb[0], eb[1]); ex1, ey1 = P(eb[2], eb[3])
        o.append(f'<rect x="{ex0:.2f}" y="{ey0:.2f}" width="{ex1 - ex0:.2f}" height="{ey1 - ey0:.2f}" rx="0.8" fill="none" '
                 f'stroke="{col}" stroke-width="0.9"><title>{l["n"]:02d} {c} (instance {k_ + 2})</title></rect>')
        qx, qy = P(*EXTRA_BADGE[c][k_])
        qw = tw(f'{l["n"]:02d}', True) + 3.6
        o.append(f'<line x1="{qx + qw / 2:.2f}" y1="{qy:.2f}" x2="{qx + qw / 2:.2f}" y2="{ey1:.2f}" stroke="{col}" stroke-width="0.7"/>'
                 f'<rect x="{qx:.2f}" y="{qy:.2f}" width="{qw:.2f}" height="{BH}" rx="2" fill="{col}" stroke="#fff" stroke-width="0.4"/>'
                 f'<text x="{qx + qw / 2:.2f}" y="{qy + BH / 2 + 3.05:.2f}" font-size="{FS}" font-weight="bold" fill="{ink(col)}" text-anchor="middle">{l["n"]:02d}</text>')
""")

# ======== v4.2 header standard + reference JSON (U01) ========
sub(r"casing-diagram-atomic-checklist-v4.1.txt'), encoding='utf-8')", r"casing-diagram-atomic-checklist-v4.2.txt'), encoding='utf-8')")
sub("OUT = os.path.join(ROOT, r'06-study\\sample-uic\\diagrams\\U01.svg')",
    "OUT = os.environ.get('FIG_OUT') or os.path.join(ROOT, r'06-study\\sample-uic\\diagrams\\U01.svg')\n"
    "DIAG = 'U01'\nCHECKLIST = 'v4.2'\nREVIEWER = 'Lester S. Carcamo'\nREVIEW_DATE = '2026-11-18'\nREVIEW_DATE_LONG = 'November 18, 2026'")
sub("""o.append(f'<text x="{M0X}" y="{M0Y + 13}" font-size="14.7" font-weight="bold" fill="#111">'
         f'Casing diagram U01: {n_total} atomic data points (checklist v4.2), 14 CCR § 1724.7.1 · PROVISIONAL</text>')
o.append(f'<text x="{M0X}" y="{M0Y + 27}" font-size="9.3" fill="#444">Provisional — Claude\\'s review, not the frozen human reference · {n_met} MET · '
         f'{n_app - n_met} MISSING · {n_na} N/A · completeness {score * 100:.1f}% · Hill 44MW, API 0403050708 (Berry, South Belridge)</text>')""",
    """o.append(f'<text x="{M0X}" y="{M0Y + 13}" font-size="14.7" font-weight="bold" fill="#111">'
         f'Casing Diagram {DIAG} · Checklist {CHECKLIST} · Final score {score * 100:.1f}% ({n_met} of {n_app} applicable points MET)</text>')
o.append(f'<text x="{M0X}" y="{M0Y + 27}" font-size="9.3" fill="#444">Scored by {REVIEWER} · {REVIEW_DATE_LONG}</text>')""")
sub("'Completeness score (Equation 1) — provisional'", "'Completeness score (Equation 1)'")
sub("""    ('Sources.', 'casing-diagram-atomic-checklist-v4.2.txt (90 points); U01.pdf (sample-uic). MET/MISSING/N/A: Claude\\'s '
     'provisional review; no human reference exists. Frames from PDF text boxes.'),""",
    """    ('Sources.', f'casing-diagram-atomic-checklist-{CHECKLIST}.txt (90 points); {DIAG}.pdf (sample-uic). MET/MISSING/N/A scored by '
     f'{REVIEWER}, {REVIEW_DATE_LONG}. Frames from PDF text boxes.'),""")
sub("""open(OUT, 'w', encoding='utf-8').write('\\n'.join(o))
""", """open(OUT, 'w', encoding='utf-8').write('\\n'.join(o))
# ---------------------------------------------------------------- reference JSON
import json, csv
REF = os.environ.get('REF_OUT') or os.path.join(ROOT, r'06-study\\sample-uic\\reference', DIAG + '.json')
os.makedirs(os.path.dirname(REF), exist_ok=True)
_log = {r['SampleCode']: r for r in csv.DictReader(open(os.path.join(ROOT, r'06-study\\sample-uic\\screening-log.csv'), encoding='utf-8'))}[DIAG]


def _bb(b):
    return [round(float(v), 1) for v in b[:4]]


def _words_in(b):
    ws = [w for w in words if w[0] >= b[0] - 0.6 and w[2] <= b[2] + 0.6 and w[1] >= b[1] - 0.6 and w[3] <= b[3] + 0.6]
    return ' '.join(w[4] for w in sorted(ws, key=lambda w: (round(w[1]), w[0])))


_pts = []
for n, c, lab in pts:
    rec = {'number': n, 'code': c, 'label': lab, 'status': {'MET': 'MET', 'MISSING': 'MISSING', 'NA': 'NOT_APPLICABLE'}[status[c]],
           'displayed_answer': None, 'locations': []}
    if status[c] == 'MET':
        ws_ = F_[c][0]
        txts = [EVID.get(c) or ' '.join(str(w[4]) for w in ws_)]
        rec['locations'].append({'page': 1, 'bbox_pt': _bb(box(ws_, 0))})
        for eb in EXTRA_FR.get(c, []):
            txts.append(EXTRA_TXT.get(c, {}).get(len(txts) - 1) or _words_in(eb))
            rec['locations'].append({'page': 1, 'bbox_pt': _bb(eb)})
        rec['displayed_answer'] = ' | '.join(txts)
    elif status[c] == 'NA':
        rec['displayed_answer'] = None
        rec['note'] = '; '.join(f'{nf[0]}: {nf[1]}' for nf in NAFR)
    _pts.append(rec)


def _inst(r):
    return (r[3] if len(r) > 3 and r[3] else _words_in(r[2]) or r[0])


ref = {
    'diagram_id': DIAG,
    'source_pdf': f'06-study/sample-uic/diagrams/{DIAG}.pdf', 'page_scored': 1,
    'well': {'well_name': f"{_log['LeaseName']} {_log['WellNumber']}", 'lease_name': _log['LeaseName'], 'well_number': _log['WellNumber'],
             'api': _log['API10'], 'operator': OPERATOR, 'field': _log['FieldName'], 'county': _log['County'], 'district': _log['District'],
             'well_type': f"{_log['WellTypeCode']} {_log['WellTypeLabel']}", 'well_status': _log['WellStatus'], 'uic_project': _log['UIC_Project'],
             'diagram_printed_date': DIAGRAM_DATE, 'wellstar_document_id': _log['DocumentID'],
             'wellstar_document_date': _log['DocumentRelevantDate'], 'wellstar_file_name': _log['WellSTAR_FileName'], 'sha256': _log['SHA256']},
    'checklist_version': CHECKLIST, 'reviewer': REVIEWER, 'review_date': REVIEW_DATE,
    'score': {'met': n_met, 'applicable': n_app, 'not_applicable': n_na, 'missing': n_app - n_met, 'percent': round(score * 100, 1),
              'subdivisions_a_d': {'met': met_ad, 'of': len(ad_pts), 'md_non_depth_met': met_ad_md, 'md_non_depth_of': n_ad_md,
                                   'tvd_met': met_tvd, 'tvd_of': n_tvd},
              'subdivisions_b_c': {'met': met_bc, 'applicable': app_bc}},
    'points': _pts,
    'excess_data': [{'type': m[0], 'label': m[1], 'count': mcount[m[0]],
                     'instances': [{'text': _inst(RED[i_]), 'item': RED[i_][0], 'reason': RED[i_][1], 'page': 1, 'bbox_pt': _bb(RED[i_][2])}
                                   for i_ in sorted(mtype_of) if mtype_of[i_] == m[0]]} for m in MTYPES],
    'provenance': [{'item': r[0], 'text': _inst(r), 'page': 1, 'bbox_pt': _bb(r[2])} for r in PROV],
    'supporting_another_requirement': [{'item': r[0], 'citation': r[3], 'note': r[1], 'page': 1, 'bbox_pt': _bb(r[2])} for r in NEUTRAL],
    'not_applicable_evidence': [{'point': 90, 'item': r[0], 'text': _inst(r), 'page': 1, 'bbox_pt': _bb(r[2])} for r in NAFR],
    'excess_total': {'instances': len(RED), 'types': len(MTYPES)},
}
json.dump(ref, open(REF, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print('reference json:', REF)
""")
open(f, 'w', encoding='utf-8').write(t)
print('build_u01.py written')
