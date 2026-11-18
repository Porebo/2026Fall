import fitz, base64, sqlite3, re, random, os
import numpy as np

ROOT = r'c:\repos\2026Fall\classes\graduate-project'
OUT = os.environ.get('FIG_OUT') or os.path.join(ROOT, r'06-study\sample-uic\diagrams\U01.svg')
DIAG = 'U01'
CHECKLIST = 'v4.2'
REVIEWER = 'Lester S. Carcamo'
REVIEW_DATE = '2026-11-18'
REVIEW_DATE_LONG = 'November 18, 2026'
os.makedirs(os.path.dirname(OUT), exist_ok=True)

# ================================================================ data
pts = []
for line in open(os.path.join(ROOT, r'06-study\design\prompts\casing-diagram-atomic-checklist-v4.2.txt'), encoding='utf-8'):
    m = re.match(r'^(\d\d) \| (\S+) \| (.+)$', line.strip())
    if m:
        pts.append((int(m[1]), m[2], m[3]))
# Presence decisions for U01 (reference record; reviewer Lester S. Carcamo)
U01_MET = {1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 17, 18, 32, 35, 36, 37, 38, 39, 40, 43, 44, 45, 46, 81, 88}  # checklist v4.1 numbering
U01_NA = {90}   # (c) borehole designation: one borehole shown ("Original Hole" only) -> NOT_APPLICABLE
status = {c: ('MET' if n in U01_MET else 'NA' if n in U01_NA else 'MISSING') for n, c, _ in pts}
assert all(c in status for _, c, _ in pts)
md = [p for p in pts if not p[1].endswith('.tvd')]
tvd = {p[1][:-4]: p for p in pts if p[1].endswith('.tvd')}
assert len(md) + len(tvd) == len(pts)
num = {c: n for n, c, _ in pts}
met = [c for _, c, _ in pts if status[c] == 'MET']
n_total, n_md, n_tvd = len(pts), len(md), len(tvd)
met_md = sum(status[c] == 'MET' for _, c, _ in md)
met_tvd = sum(status[p[1]] == 'MET' for p in tvd.values())
n_met = met_md + met_tvd
assert n_met == len(met)
ad_pts = [p for p in pts if p[0] <= 78]
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
      f'(b)/(c) MET {met_bc} of {app_bc} applicable; total {n_met} / {n_app} = {score:.4f}')

# ================================================================ requirement groups -> colours
# Okabe-Ito (minus vermillion/grey) + Tol indigo/olive + brown; no red, no grey.
GROUPS = [  # (key, label, (a)(n) list, colour)
    ('g1', '(a)(1) Well identification', [1], '#0072B2'),
    ('g2', '(a)(2)–(4) Spud, elevations', [2, 3, 4], '#E69F00'),
    ('g3', '(b)–(c) Cement data, wellbore path', [], '#56B4E9'),   # U01: (a)(5)-(6) unused, colour reused
    ('g4', '(a)(7)–(8) Casing and shoe', [7, 8], '#009E73'),
    ('g5', '(a)(9) Perforations', [9], '#CC79A7'),
    ('g6', '(a)(10)–(11) Other equipment; hole', [10, 11], '#8C564B'),
    ('g7', '(a)(12)–(13) Cement plugs, fill', [12, 13], '#332288'),
    ('g8', '(a)(15) Formations, markers', [15], '#999933'),
]

GBC = [g for g in GROUPS if g[0] == 'g3'][0]


def lum(hexc):
    r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ink(hexc):
    L = lum(hexc)
    cw, cd = 1.05 / (L + 0.05), (L + 0.05) / (lum('#111111') + 0.05)
    return '#ffffff' if cw >= 4.5 and cw >= cd else '#111111'


def group_of(code):
    m_ = re.match(r'\(a\)\((\d+)\)', code)
    if not m_:
        return GBC
    n = int(m_[1])
    for g in GROUPS:
        if n in g[2]:
            return g
    return None


for c in met:
    assert group_of(c), c
used_groups = sorted([g for g in GROUPS if any(group_of(c) is g for c in met)], key=lambda g: g is GBC)
for g in GROUPS:
    print(f'{g[1]:40s} {g[3]}  text {ink(g[3])}  contrast-ok')

# ================================================================ diagram raster
doc = fitz.open(os.path.join(ROOT, r'06-study\sample-uic\diagrams\U01.pdf'))
page = doc[0]
words = page.get_text('words')
CX0, CY0, CX1, CY1 = 26, 12, 592, 772
DPI = 220
pix = page.get_pixmap(dpi=DPI, clip=fitz.Rect(CX0, CY0, CX1, CY1))
b64 = base64.b64encode(pix.tobytes('png')).decode()
if re.search('muda', b64, re.I):   # keep the retired term out of the file, even by chance inside base64
    import io
    from PIL import Image as _Im
    _img = _Im.frombytes('RGB', (pix.width, pix.height), pix.samples)
    for _lvl in range(9, -1, -1):
        _buf = io.BytesIO(); _img.save(_buf, 'PNG', compress_level=_lvl)
        b64 = base64.b64encode(_buf.getvalue()).decode()
        if not re.search('muda', b64, re.I):
            break
    assert not re.search('muda', b64, re.I)
arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3]
dark = (arr.min(axis=2) < 150)
K = DPI / 72

# ================================================================ page layout (0.5 in margins)
M0X, M1X, M0Y, M1Y = 48, 768, 48, 1008
FS = 8.7                      # 6.5 pt minimum
PH, PITCH, PADX = 9.0, 10.0, 3.0


def tw(t, bold=False, size=FS):
    return fitz.get_text_length(t, fontname='hebo' if bold else 'helv', fontsize=size)


SHORT = {'Other equipment in the well (e.g., tubing, pumps, rods)': 'Other equipment in the well',
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
    return lab.replace(' (MD)', '')


BADGE_W = tw('00', True) + 3.2
W1 = round(max(BADGE_W + 3 + tw(label(lab)) for _, _, lab in md) + 2 * PADX + 1, 1)
W2 = round(max(tw(f'{p[0]:02d}') for p in tvd.values()) + 2 * PADX + 1, 1)
X1 = M0X
X2 = X1 + W1 + 2.5
GUT = 30
G0 = X2 + W2 + 3
IX = G0 + GUT
IW = M1X - IX
s = IW / (CX1 - CX0)
IH = (CY1 - CY0) * s
IY = 90
ROW0 = IY + 12
print(f'W1={W1} W2={W2} image x={IX:.1f} w={IW:.1f} h={IH:.1f} bottom={IY + IH:.1f} scale={s:.3f}')


def P(x, y):
    return IX + (x - CX0) * s, IY + (y - CY0) * s


def Pinv(X, Y):
    return CX0 + (X - IX) / s, CY0 + (Y - IY) / s


def darkcount_h(y, x0, x1):
    r = int(round((y - CY0) * K))
    a, b = int((x0 - CX0) * K), int((x1 - CX0) * K)
    return int(dark[max(r - 1, 0):r + 2, max(a, 0):b].any(axis=0).sum())


def darkcount_v(x, y0, y1):
    c = int(round((x - CX0) * K))
    a, b = sorted((int((y0 - CY0) * K), int((y1 - CY0) * K)))
    return int(dark[a:b, max(c - 1, 0):c + 2].any(axis=1).sum())


def dark_rect(x0, y0, x1, y1):  # pdf coords
    a, b = max(int((x0 - CX0) * K), 0), max(int((y0 - CY0) * K), 0)
    c, d = int((x1 - CX0) * K), int((y1 - CY0) * K)
    if c <= 0 or d <= 0 or a >= dark.shape[1] or b >= dark.shape[0]:
        return 0
    return int(dark[b:d, a:c].sum())


def channel(dx, ty, span=14):
    best = None
    for k in range(int(-span * 4), int(span * 4) + 1):
        y = ty + k / 4
        if y < CY0 + 1 or y > CY1 - 1:
            continue
        c = darkcount_h(y, CX0, dx - 1.0) + darkcount_v(dx, y, ty) + abs(y - ty) * 0.4
        if best is None or c < best[0]:
            best = (c, y)
    return best[1]


# ================================================================ helpers on PDF words
def wsel(pred):
    return [w for w in words if pred(w)]


def box(ws, pad=0.9):
    return (min(w[0] for w in ws) - pad, min(w[1] for w in ws) - pad,
            max(w[2] for w in ws) + pad, max(w[3] for w in ws) + pad)


def row(y0, y1, x0=0, x1=999):
    return wsel(lambda w: y0 <= (w[1] + w[3]) / 2 <= y1 and x0 <= w[0] and w[2] <= x1)


def W(text, near=None):
    c = [w for w in words if w[4] == text]
    if near:
        c.sort(key=lambda w: abs(w[0] - near[0]) + abs(w[1] - near[1]))
    return c[0]


# ================================================================ MET frames: code -> (word list, route)
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
mtype_of = {}
for i_, r in enumerate(RED):
    hit = [m[0] for m in MTYPES if any(r[0].startswith(p) for p in m[2])]
    assert len(hit) == 1, r[0]
    mtype_of[i_] = hit[0]
mcount = {m[0]: sum(v == m[0] for v in mtype_of.values()) for m in MTYPES}
assert sum(mcount.values()) == len(RED)
print('excess-data types:', mcount, 'total', len(RED))
# keep >= GAP pt between every red frame and every group frame (inset the red edge)
GAP = 0.9
adjusted = []
for r in RED + NEUTRAL + PROV + NAFR:
    x0, y0, x1, y1 = r[2]
    for c, (a, b, cc, d) in GF.items():
        if x0 < cc + GAP and a - GAP < x1 and y0 < d + GAP and b - GAP < y1:
            pen = {'L': cc + GAP - x0, 'R': x1 - (a - GAP), 'T': d + GAP - y0, 'B': y1 - (b - GAP)}
            side = min(pen, key=pen.get)
            if side == 'L': x0 = cc + GAP
            if side == 'R': x1 = a - GAP
            if side == 'T': y0 = d + GAP
            if side == 'B': y1 = b - GAP
            adjusted.append((r[0], num[c], side, round(pen[side], 2)))
    r[2] = (x0, y0, x1, y1)
for a in adjusted:
    print('inset red frame', a)

# ================================================================ connectors
TOPBUS = [IY - 3 - 2.6 * k for k in range(4)]
BOTBUS = IY + IH + 3.5
DOTOFF = 1.5   # pt outside the frame edge


def rowgap(i):
    return 1 if md[i][0] >= 79 else 0   # one header row before the (b)-(c) block


def rowy(i):
    return ROW0 + (i + rowgap(i)) * PITCH + PH / 2


lines = []
for i, (n, c, lab) in enumerate(md):
    if c not in F_:
        continue
    route = F_[c][1]
    fx0, fy0, fx1, fy1 = GF[c]
    l = dict(code=c, n=n, sy=rowy(i), route=route, col=group_of(c)[3])
    if route == 'h':
        px, py = fx0 - DOTOFF, (fy0 + fy1) / 2
        cy = CHAN.get(c) or channel(px, py)
        l['cy'] = P(0, cy)[1]
    elif route == 'top':
        px, py = fx0 + (fx1 - fx0) * 0.5, fy0 - DOTOFF
    elif route == 'bot':
        px, py = 571.5, fy1 + DOTOFF
    elif route == 'right':
        px, py = fx1 + DOTOFF, (fy0 + fy1) / 2
        l['xr'] = P(605.0 if c.endswith('hole_depth.md') else 601.0, 0)[0]
    l['px'], l['py'] = px, py
    l['tx'], l['ty'] = P(px, py)
    lines.append(l)
tops_ = sorted([l for l in lines if l['route'] in ('top', 'right')], key=lambda l: l.get('xr', l['tx']))
for k, l in enumerate(tops_):          # rightmost drop rides the highest bus -> no crossings
    l['bus'] = TOPBUS[k]
for l in lines:
    if l['route'] == 'bot':
        l['bus'] = BOTBUS


def segs(l, lx):
    st = [(X1 + W1, l['sy']), (lx, l['sy'])]
    if l['route'] == 'h':
        return st + [(lx, l['cy']), (l['tx'], l['cy']), (l['tx'], l['ty'])]
    if l['route'] == 'right':
        return st + [(lx, l['bus']), (l['xr'], l['bus']), (l['xr'], l['ty']), (l['tx'], l['ty'])]
    return st + [(lx, l['bus']), (l['tx'], l['bus']), (l['tx'], l['ty'])]


def cross(a, b):
    n = 0
    for p, q in zip(a, a[1:]):
        for r, t in zip(b, b[1:]):
            for (h1, h2), (v1, v2) in (((p, q), (r, t)), ((r, t), (p, q))):
                if abs(h1[1] - h2[1]) < 1e-6 and abs(v1[0] - v2[0]) < 1e-6:
                    hx0, hx1 = sorted((h1[0], h2[0]))
                    vy0, vy1 = sorted((v1[1], v2[1]))
                    if hx0 < v1[0] < hx1 and vy0 < h1[1] < vy1:
                        n += 1
    return n


N = len(lines)
lanes = [G0 + 2 + (GUT - 5) * k / (N - 1) for k in range(N)]


def cost(order):
    geo = [segs(lines[j], lanes[k]) for k, j in enumerate(order)]
    return sum(cross(geo[a], geo[b]) for a in range(N) for b in range(a + 1, N))


random.seed(1)
best = list(range(N))
bc = cost(best)
for it in range(5000):
    o_ = best[:]
    a, b = random.sample(range(N), 2)
    o_[a], o_[b] = o_[b], o_[a]
    c = cost(o_)
    if c <= bc:
        best, bc = o_, c
print('crossings', bc)
for k, j in enumerate(best):
    lines[j]['lane'] = lanes[k]

# ================================================================ number badges next to frames (display px)
BH = 9.4
obst = []   # display-px rects
for c, b in GF.items():
    x0, y0 = P(b[0], b[1]); x1, y1 = P(b[2], b[3]); obst.append((x0, y0, x1, y1))
for r in RED + NEUTRAL + PROV + NAFR:
    b = r[2]; x0, y0 = P(b[0], b[1]); x1, y1 = P(b[2], b[3]); obst.append((x0, y0, x1, y1))
lineobst = []
for l in lines:
    pp = segs(l, l['lane'])
    for p, q in zip(pp, pp[1:]):
        lineobst.append((l['code'], (min(p[0], q[0]) - 0.6, min(p[1], q[1]) - 0.6, max(p[0], q[0]) + 0.6, max(p[1], q[1]) + 0.6)))
    obst.append((l['tx'] - 2.2, l['ty'] - 2.2, l['tx'] + 2.2, l['ty'] + 2.2))


def ovl(a, b):
    return max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))


badges = {}
for l in sorted(lines, key=lambda l: l['n']):
    c = l['code']
    bw = tw(f'{l["n"]:02d}', True) + 3.6
    x0, y0 = P(GF[c][0], GF[c][1]); x1, y1 = P(GF[c][2], GF[c][3])
    ym = (y0 + y1) / 2
    cands = []
    for dx in [k * 1.5 for k in range(0, 21)]:
        for dy in (0, -1.5, 1.5, -3, 3):
            pen = dx * 0.6 + abs(dy) * 0.8
            cands += [(x1 + 1 + dx, ym - BH / 2 + dy, pen), (x0 - 4 - bw - dx, ym - BH / 2 + dy, 1 + pen)]
    for dx in (0, 4, 8):
        cands += [(x1 - bw + dx, y0 - BH - 0.8, 1.5 + dx), (x1 - bw + dx, y1 + 0.8, 1.5 + dx),
                  (x0 - dx, y0 - BH - 0.8, 2 + dx), (x0 - dx, y1 + 0.8, 2 + dx)]
    best_ = None
    for bx, by, pen in cands:
        rect = (bx, by, bx + bw, by + BH)
        if rect[0] < IX or rect[2] > IX + IW or rect[1] < IY or rect[3] > IY + IH:
            continue
        p0 = Pinv(rect[0], rect[1]); p1 = Pinv(rect[2], rect[3])
        cst = dark_rect(p0[0], p0[1], p1[0], p1[1]) * 5.0 + pen * 6
        cst += sum(ovl(rect, ob) for ob in obst) * 400
        cst += sum(ovl(rect, ob) for who, ob in lineobst if who != c) * 25
        cst += sum(ovl(rect, bb) for bb in badges.values()) * 4000
        if best_ is None or cst < best_[0]:
            best_ = (cst, rect)
    badges[c] = best_[1]
    l['badge_cost'] = round(best_[0], 1)
    obst.append(best_[1])
TH = 9.0
tags = {}
for k_, nt in enumerate(NEUTRAL):
    if not nt[3]:
        continue
    a_, b_, c_, d_ = nt[4] if len(nt) > 4 else nt[2]
    x0, y0 = P(a_, b_); x1, y1 = P(c_, d_)
    own = (x0, y0, x1, y1)
    tw_ = tw(nt[3]) + 5
    ym = (y0 + y1) / 2
    cands = []
    for dx in [i * 2 for i in range(0, 30)]:
        for dy in [j * 0.5 for j in range(-14, 15)]:
            pen = dx * 0.5 + abs(dy) * 0.8
            cands += [(x1 + 1 + dx, ym - TH / 2 + dy, pen), (x0 - 1 - tw_ - dx, ym - TH / 2 + dy, 2 + pen)]
    for dx in [i * 3 for i in range(0, 40)]:
        cands += [(x0 + dx, y0 - TH - 0.8, 1 + dx * 0.2), (x0 + dx, y1 + 0.8, 1 + dx * 0.2)]
    cands += [(x1 - tw_ - 1.2, y1 - TH - 1.2, 0.5), (x1 - tw_ - 1.2, y0 + 1.2, 0.5)]
    best_ = None
    for bx, by, pen in cands:
        rect = (bx, by, bx + tw_, by + TH)
        if rect[0] < IX or rect[2] > IX + IW or rect[1] < IY or rect[3] > IY + IH:
            continue
        p0 = Pinv(rect[0], rect[1]); p1 = Pinv(rect[2], rect[3])
        cst = dark_rect(p0[0], p0[1], p1[0], p1[1]) * 5.0 + pen * 6
        cst += sum(ovl(rect, ob) for ob in obst if ob != own) * 400
        cst += sum(ovl(rect, ob) for who, ob in lineobst) * 25
        if best_ is None or cst < best_[0]:
            best_ = (cst, rect)
    if nt[0].startswith('Casing string top depth'):   # fixed: blank band under the 9.625-in string line
        fx0, fy0 = P(366.5 - (tw_ / s), 145.0)
        best_ = (0.0, (fx0, fy0, fx0 + tw_, fy0 + TH))
    if nt[0].startswith('Casing table, Top MD'):      # fixed: CASING header row, right of the title
        fx0, fy0 = P(120.5, 106.4)
        best_ = (0.0, (fx0, fy0, fx0 + tw_, fy0 + TH))
    for pref_, (px_, py_) in {'Production casing cement job date': (172.0, 461.5),
                              'Production casing cement (plug) job date': (172.0, 675.0)}.items():
        if nt[0].startswith(pref_ + ' "'):
            fx0, fy0 = P(px_, py_)
            best_ = (0.0, (fx0, fy0, fx0 + tw_, fy0 + TH))
    tags[k_] = best_[1]
    obst.append(best_[1])
    print('tag', nt[3], 'for', nt[0], 'cost', round(best_[0], 1))
MH = 9.0
mbadges = []   # (mid, rect)
for m in MTYPES:
    fr = sorted([RED[i_][2] for i_, v in mtype_of.items() if v == m[0]], key=lambda b: b[1])
    clusters = []
    for b in fr:
        if clusters:
            cb = clusters[-1]
            if b[1] - cb[3] < 40 and abs((b[0] + b[2]) / 2 - (cb[0] + cb[2]) / 2) < 120:
                clusters[-1] = (min(cb[0], b[0]), min(cb[1], b[1]), max(cb[2], b[2]), max(cb[3], b[3]))
                continue
        clusters.append(b)
    for cb in clusters:
        x0, y0 = P(cb[0], cb[1]); x1, y1 = P(cb[2], cb[3])
        bw_ = tw(m[0], True) + 4
        ym = (y0 + y1) / 2
        cands = []
        for dx in [i * 1.5 for i in range(0, 30)]:
            for dy in [j * 1.0 for j in range(-6, 7)]:
                pen = dx * 0.5 + abs(dy) * 0.6
                cands += [(x1 + 1 + dx, ym - MH / 2 + dy, pen), (x0 - 1 - bw_ - dx, ym - MH / 2 + dy, 1 + pen)]
        for dx in [i * 3 for i in range(0, 30)]:
            cands += [(x1 - bw_ - dx, y0 - MH - 0.8, 1 + dx * 0.3), (x0 + dx, y0 - MH - 0.8, 1.5 + dx * 0.3),
                      (x1 - bw_ - dx, y1 + 0.8, 1 + dx * 0.3), (x0 + dx, y1 + 0.8, 1.5 + dx * 0.3)]
        best_ = None
        for bx, by, pen in cands:
            rect = (bx, by, bx + bw_, by + MH)
            if rect[0] < IX or rect[2] > IX + IW or rect[1] < IY or rect[3] > IY + IH:
                continue
            p0 = Pinv(rect[0], rect[1]); p1 = Pinv(rect[2], rect[3])
            cst = dark_rect(p0[0], p0[1], p1[0], p1[1]) * 5.0 + pen * 6
            cst += sum(ovl(rect, ob) for ob in obst) * 400
            cst += sum(ovl(rect, ob) for who, ob in lineobst) * 25
            if best_ is None or cst < best_[0]:
                best_ = (cst, rect)
        mbadges.append((m[0], best_[1]))
        obst.append(best_[1])
        print('M-badge', m[0], 'cost', round(best_[0], 1))
# U01 hand placements: blank cell space next to the frame (automatic spots covered callout text)
_x, _y = P(578.0, 337.6)
badges['(a)(10).other_equipment'] = (_x, _y, _x + tw('32', True) + 3.6, _y + BH)
_x, _y = P(296.0, 201.6)
mbadges = [(m_, ((_x, _y, _x + tw('E5', True) + 4, _y + MH) if m_ == 'E5' else r_)) for m_, r_ in mbadges]
print('badge costs (dark px + penalties):', {num[c]: l['badge_cost'] for l in lines for c in [l['code']]})

# ================================================================ SVG
F = "Helvetica, Arial, 'Liberation Sans', sans-serif"
GREY_F, GREY_S, GREY_T = '#f0f0f0', '#cfcfcf', '#9b9b9b'
REDC = '#d62728'
NAC = '#6b6b6b'
NEUC = '#44546A'
PROVC = '#111111'
o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
         f'width="8.5in" height="11in" viewBox="0 0 816 1056" font-family="{F}">')
o.append('<title>U01 atomic data-point map</title>')
o.append('<rect width="816" height="1056" fill="#ffffff"/>')
o.append(f'<text x="{M0X}" y="{M0Y + 13}" font-size="14.7" font-weight="bold" fill="#111">'
         f'Casing Diagram {DIAG} · Checklist {CHECKLIST} · Final score {score * 100:.1f}% ({n_met} of {n_app} applicable points MET)</text>')
o.append(f'<text x="{M0X}" y="{M0Y + 27}" font-size="9.3" fill="#444">Scored by {REVIEWER} · {REVIEW_DATE_LONG}</text>')
o.append(f'<text x="{X1 + PADX}" y="{ROW0 - 3.5}" font-size="{FS}" font-weight="bold" fill="#333">MD / non-depth</text>')
o.append(f'<text x="{X2 + W2 / 2:.1f}" y="{ROW0 - 3.5}" font-size="{FS}" font-weight="bold" fill="#333" text-anchor="middle">TVD</text>')
o.append(f'<line x1="{X1}" y1="{ROW0 - 1.5}" x2="{X2 + W2}" y2="{ROW0 - 1.5}" stroke="#999" stroke-width="0.5"/>')
o.append(f'<image x="{IX:.2f}" y="{IY}" width="{IW:.2f}" height="{IH:.2f}" preserveAspectRatio="none" '
         f'xlink:href="data:image/png;base64,{b64}"/>')
o.append(f'<rect x="{IX:.2f}" y="{IY}" width="{IW:.2f}" height="{IH:.2f}" fill="none" stroke="#bbb" stroke-width="0.5"/>')
# red frames
o.append(f'<g fill="none" stroke="{REDC}" stroke-width="0.7">')
for name, why, (a, b, c2, d) in RED:
    x0, y0 = P(a, b); x1, y1 = P(c2, d)
    o.append(f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{x1 - x0:.2f}" height="{y1 - y0:.2f}" rx="0.8"><title>{name}: {why}</title></rect>')
o.append('</g>')
for k_, nt in enumerate(NEUTRAL):
    name, why, (a, b, c2, d), tag = nt[:4]
    name, why = name.replace('&', '&amp;'), why.replace('&', '&amp;')
    x0, y0 = P(a, b); x1, y1 = P(c2, d)
    o.append(f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{x1 - x0:.2f}" height="{y1 - y0:.2f}" rx="0.8" fill="none" '
             f'stroke="{NEUC}" stroke-width="0.9" stroke-dasharray="2 1.2"><title>{name}: {why}</title></rect>')
    if not tag:
        continue
    if len(nt) > 4:
        x0, y0 = P(nt[4][0], nt[4][1]); x1, y1 = P(nt[4][2], nt[4][3])
    tx0, ty0, tx1, ty1 = tags[k_]
    fx = min(max((tx0 + tx1) / 2, x0), x1); fy = min(max((ty0 + ty1) / 2, y0), y1)
    gx = min(max(fx, tx0), tx1); gy = min(max(fy, ty0), ty1)
    if abs(gx - fx) + abs(gy - fy) > 2.5:
        o.append(f'<line x1="{fx:.2f}" y1="{fy:.2f}" x2="{gx:.2f}" y2="{gy:.2f}" stroke="{NEUC}" stroke-width="0.7" stroke-dasharray="1.5 1"/>')
    o.append(f'<rect x="{tx0:.2f}" y="{ty0:.2f}" width="{tx1 - tx0:.2f}" height="{TH}" rx="1.5" fill="{NEUC}" stroke="#fff" stroke-width="0.4"/>'
             f'<text x="{(tx0 + tx1) / 2:.2f}" y="{ty0 + TH / 2 + 3.05:.2f}" font-size="{FS}" fill="#fff" text-anchor="middle">{tag.replace("&", "&amp;")}</text>')
for name, why, (a, b, c2, d) in NAFR:
    x0, y0 = P(a, b); x1, y1 = P(c2, d)
    o.append(f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{x1 - x0:.2f}" height="{y1 - y0:.2f}" fill="none" stroke="{NAC}" '
             f'stroke-width="0.9" stroke-dasharray="2.2 1.4"><title>{name}: {why}</title></rect>')
    bx_, by_ = P(a + 1.0, b - 10.6)
    bw_ = tw('90 N/A', True) + 4
    o.append(f'<rect x="{bx_:.2f}" y="{by_:.2f}" width="{bw_:.2f}" height="9" rx="1.5" fill="#ffffff" stroke="{NAC}" stroke-width="0.7" stroke-dasharray="2.2 1.4"/>'
             f'<text x="{bx_ + bw_ / 2:.2f}" y="{by_ + 7.5:.2f}" font-size="{FS}" font-weight="bold" fill="{NAC}" text-anchor="middle">90 N/A</text>')
for name, why, (a, b, c2, d) in PROV:
    x0, y0 = P(a, b); x1, y1 = P(c2, d)
    o.append(f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{x1 - x0:.2f}" height="{y1 - y0:.2f}" fill="none" stroke="{PROVC}" '
             f'stroke-width="1.0" stroke-dasharray="0.1 1.6" stroke-linecap="round"><title>{name}: document provenance; not required, not scored</title></rect>')
for mid, (bx0, by0, bx1, by1) in mbadges:
    o.append(f'<rect x="{bx0:.2f}" y="{by0:.2f}" width="{bx1 - bx0:.2f}" height="{MH}" rx="1.5" fill="{REDC}" stroke="#fff" stroke-width="0.4"/>'
             f'<text x="{(bx0 + bx1) / 2:.2f}" y="{by0 + MH / 2 + 3.0:.2f}" font-size="{FS}" font-weight="bold" fill="#fff" text-anchor="middle">{mid}</text>')
# connectors
for l in lines:
    o.append(f'<polyline points="' + ' '.join(f'{x:.2f},{y:.2f}' for x, y in segs(l, l['lane'])) +
             f'" fill="none" stroke="{l["col"]}" stroke-width="0.85" stroke-linejoin="round"/>')
# group frames, dots, badges
for l in lines:
    c, col = l['code'], l['col']
    x0, y0 = P(GF[c][0], GF[c][1]); x1, y1 = P(GF[c][2], GF[c][3])
    o.append(f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{x1 - x0:.2f}" height="{y1 - y0:.2f}" rx="0.8" fill="none" '
             f'stroke="{col}" stroke-width="0.9"><title>{l["n"]:02d} {c}</title></rect>')
    o.append(f'<circle cx="{l["tx"]:.2f}" cy="{l["ty"]:.2f}" r="1.5" fill="{col}" stroke="#fff" stroke-width="0.4"/>')
    bx0, by0, bx1, by1 = badges[c]
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


def pill(x, w, y, n, name, code, numbered=True):
    g = group_of(code) if status[code] == 'MET' else None
    dash = ''
    if g:
        f, st, t = g[3], g[3], ink(g[3])
    elif status[code] == 'NA':
        f, st, t, dash = '#ffffff', NAC, NAC, ' stroke-dasharray="2.2 1.4"'
    else:
        f, st, t = GREY_F, GREY_S, GREY_T
    r = f'<rect x="{x}" y="{y:.2f}" width="{w}" height="{PH}" rx="{PH / 2}" fill="{f}" stroke="{st}" stroke-width="0.7"{dash}/>'
    base = y + PH / 2 + 3.0
    if not numbered:
        return r + f'<text x="{x + w / 2:.2f}" y="{base:.2f}" font-size="{FS}" fill="{t}" text-anchor="middle">{n:02d}</text>'
    bx = x + 1.4
    if g:
        r += (f'<rect x="{bx:.2f}" y="{y + 1.0:.2f}" width="{BADGE_W:.2f}" height="{PH - 2.0:.2f}" rx="{(PH - 2) / 2:.2f}" fill="#ffffff"/>'
              f'<text x="{bx + BADGE_W / 2:.2f}" y="{base:.2f}" font-size="{FS}" font-weight="bold" fill="{g[3] if ink(g[3]) == "#ffffff" else "#111"}" text-anchor="middle">{n:02d}</text>')
    else:
        r += f'<text x="{bx + BADGE_W / 2:.2f}" y="{base:.2f}" font-size="{FS}" font-weight="bold" fill="{t}" text-anchor="middle">{n:02d}</text>'
    r += f'<text x="{bx + BADGE_W + 3:.2f}" y="{base:.2f}" font-size="{FS}" fill="{t}">{name}</text>'
    return r


for i, (n, c, lab) in enumerate(md):
    y = ROW0 + (i + rowgap(i)) * PITCH
    if n == 79:
        o.append(f'<text x="{X1 + PADX}" y="{y - PITCH + PH / 2 + 3.0:.2f}" font-size="{FS}" font-weight="bold" fill="#333">'
                 f'§ 1724.7.1(b)–(c) (no TVD pair)</text>')
    o.append(pill(X1, W1, y, n, label(lab).replace('&', '&amp;'), c))
    if c.endswith('.md'):
        tp = tvd[c[:-3]]
        o.append(pill(X2, W2, y, tp[0], '', tp[1], numbered=False))
rows_bottom = ROW0 + (len(md) + 1) * PITCH


def text(x, y, t, size=FS, color='#333', weight=None, anchor=None):
    w = f' font-weight="{weight}"' if weight else ''
    a = f' text-anchor="{anchor}"' if anchor else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}"{w}{a}>{t}</text>'


# ---- key (left column, below the pills)
LY = rows_bottom + 13
LX = X1
o.append(text(LX, LY, 'Key: MET, by requirement group', 9.3, '#111', 'bold'))
LY += 12
for g in used_groups:
    o.append(f'<rect x="{LX}" y="{LY - 7.4}" width="16" height="{PH}" rx="{PH / 2}" fill="{g[3]}"/>')
    o.append(text(LX + 21, LY, g[1].replace('&', '&amp;')))
    LY += 10.2
LY += 1
o.append(f'<rect x="{LX}" y="{LY - 7.4}" width="16" height="{PH}" rx="{PH / 2}" fill="{GREY_F}" stroke="{GREY_S}" stroke-width="0.55"/>')
o.append(text(LX + 21, LY, 'MISSING: no answer in U01, no line'))
LY += 13
o.append(f'<rect x="{LX + 0.5}" y="{LY - 7.6}" width="15" height="9" fill="none" stroke="#0072B2" stroke-width="0.9" rx="0.8"/>'
         f'<rect x="{LX + 18}" y="{LY - 7.6}" width="0" height="0"/>')
o.append(text(LX + 21, LY, 'Coloured frame + badge = the answer'))
LY += 13.6
o.append(f'<rect x="{LX + 0.5}" y="{LY - 7.6}" width="15" height="9" fill="none" stroke="{REDC}" stroke-width="0.7" rx="0.8"/>')
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
left_bottom = LY + 10.4

def wrap(prefix, body, width, size=FS):
    out, cur, first = [], '', True
    for w_ in body.split():
        trial = (cur + ' ' + w_).strip()
        extra = tw(prefix + ' ', True) if first and prefix else 0
        if tw(trial) + extra > width and cur:
            out.append((prefix if first else '', cur))
            first, cur = False, w_
        else:
            cur = trial
    out.append((prefix if first else '', cur))
    return out


# ---- below the image: left = score + notes, right = excess-data list
COLW = 292
SY = IY + IH + 16
SX = IX
o.append(text(SX, SY, 'Completeness score (Equation 1)', 9.3, '#111', 'bold'))
SY += 13
o.append(text(SX, SY, 'Completeness = points marked MET ÷ applicable points', FS, '#111', 'bold'))
SY += 11.5
for t_ in [f'(a), (d) MET: {met_ad} of {len(ad_pts)} (MD/non-depth {met_ad_md} of {n_ad_md}; TVD {met_tvd} of {n_tvd})',
           f'(b), (c) MET: {met_bc} of {app_bc} applicable (90 N/A: one borehole)',
           f'Total MET: {met_ad} + {met_bc} = {n_met}; applicable: {len(ad_pts)} + {app_bc} = {n_app}']:
    o.append(text(SX + 8, SY, t_))
    SY += 10.4
o.append(text(SX + 8, SY + 1, f'Completeness(U01) = {n_met} ÷ {n_app} = {score:.3f} → {score * 100:.1f}%', 10.0, '#111', 'bold'))
SY += 16
notes = [
    ('MD vs TVD.', 'MD (measured depth) runs along the borehole; TVD (true vertical depth) is the vertical depth of the same '
     'point. A row\'s MD and TVD cells are one datum scored as two points; (b)–(c) points have no TVD pair. U01 is deviated '
     '(15° to 30°) but reports MD only, so every TVD point is MISSING. Repeated data are framed once.'),
    ('Sources.', f'casing-diagram-atomic-checklist-{CHECKLIST}.txt (90 points); {DIAG}.pdf (sample-uic). MET/MISSING/N/A scored by '
     f'{REVIEWER}, {REVIEW_DATE_LONG}. Frames from PDF text boxes.'),
]
for pre, body in notes:
    for p_, line_ in wrap(pre, body, COLW):
        lead = f'<tspan font-weight="bold">{p_}</tspan> ' if p_ else ''
        o.append(text(SX, SY, lead + line_, FS, '#444'))
        SY += 10.4
left2_bottom = SY - 10.4

MX = IX + COLW + 14
MR = M1X
MY = IY + IH + 16
o.append(text(MX, MY, 'Excess data found in U01', 9.3, '#111', 'bold'))
MY += 11
o.append(text(MX, MY, '(present, not required; not scored)', FS, '#444'))
MY += 12
for m in MTYPES:
    bw_ = tw(m[0], True) + 4
    o.append(f'<rect x="{MX:.2f}" y="{MY - 7.0:.2f}" width="{bw_:.2f}" height="9" rx="1.5" fill="{REDC}"/>')
    o.append(text(MX + bw_ / 2, MY, m[0], FS, '#fff', 'bold', 'middle'))
    o.append(text(MX + 23, MY, m[1].replace('&', '&amp;')))
    o.append(text(MR, MY, f'×{mcount[m[0]]}', FS, '#111', None, 'end'))
    MY += 10.6
MY += 2
o.append(f'<line x1="{MX}" y1="{MY - 8.5:.1f}" x2="{MR}" y2="{MY - 8.5:.1f}" stroke="#bbb" stroke-width="0.5"/>')
o.append(text(MX, MY + 1, f'{len(RED)} instances in {len(MTYPES)} types', FS, '#111', 'bold'))
MY += 18
o.append(text(MX, MY, 'Document provenance (not required; not scored)', FS, '#111', 'bold'))
MY += 11
o.append(text(MX, MY, 'Records how and when the report was produced.', FS, '#444'))
for p_ in PROV:
    MY += 10.6
    o.append(f'<rect x="{MX + 0.5}" y="{MY - 7.6}" width="15" height="9" fill="none" stroke="{PROVC}" stroke-width="1.0" stroke-dasharray="0.1 1.6" stroke-linecap="round"/>')
    o.append(text(MX + 23, MY, p_[0].split(' "')[1].rstrip('"') if ' "' in p_[0] else p_[0]))
    o.append(text(MR, MY, '×1', FS, '#111', None, 'end'))
right_bottom = MY
SY = max(left2_bottom, right_bottom) + 10.8
o.append('</svg>')
open(OUT, 'w', encoding='utf-8').write('\n'.join(o))
# ---------------------------------------------------------------- reference JSON
import json, csv
REF = os.environ.get('REF_OUT') or os.path.join(ROOT, r'06-study\sample-uic\reference', DIAG + '.json')
os.makedirs(os.path.dirname(REF), exist_ok=True)
_log = {r['SampleCode']: r for r in csv.DictReader(open(os.path.join(ROOT, r'06-study\sample-uic\screening-log.csv'), encoding='utf-8'))}[DIAG]


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
print(f'rows bottom {rows_bottom:.1f}, key bottom {left_bottom:.1f}, legend bottom {SY - 10.8:.1f} (limit {M1Y})')
print('groups used:', [(g[1], g[3]) for g in used_groups])
