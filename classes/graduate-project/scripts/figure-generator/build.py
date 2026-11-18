import fitz, base64, sqlite3, re, random, os
import numpy as np

ROOT = r'c:\repos\2026Fall\classes\graduate-project'
OUT = os.path.join(ROOT, r'06-study\sample\diagrams\W01.svg')
os.makedirs(os.path.dirname(OUT), exist_ok=True)

# ================================================================ data
pts = []
for line in open(os.path.join(ROOT, r'06-study\design\prompts\casing-diagram-atomic-checklist-v2.txt'), encoding='utf-8'):
    m = re.match(r'^(\d\d) \| (\S+) \| (.+)$', line.strip())
    if m:
        pts.append((int(m[1]), m[2], m[3]))
db = sqlite3.connect(os.path.join(ROOT, r'04-literature\casing-analysis\casing_specs.db'))
status = dict(db.execute("select s.requirement_code, r.status from diagram_requirement_results r "
                         "join spec_requirements s using(requirement_id) where r.diagram_number='W01'"))
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
score = n_met / n_total
print(f'points {n_total} (md/non-depth {n_md}, tvd {n_tvd}); MET {n_met} = {met_md}+{met_tvd}; score {score:.4f}')

# ================================================================ requirement groups -> colours
# Okabe-Ito (minus vermillion/grey) + Tol indigo/olive + brown; no red, no grey.
GROUPS = [  # (key, label, (a)(n) list, colour)
    ('g1', '(a)(1) Well identification', [1], '#0072B2'),
    ('g2', '(a)(2)–(4) Spud, elevations', [2, 3, 4], '#E69F00'),
    ('g3', '(a)(5)–(6) Freshwater/USDW base', [5, 6], '#56B4E9'),
    ('g4', '(a)(7)–(8) Casing and shoe', [7, 8], '#009E73'),
    ('g5', '(a)(9) Perforations', [9], '#CC79A7'),
    ('g6', '(a)(11) Hole size, depth', [11], '#8C564B'),
    ('g7', '(a)(13) Cement fill', [13], '#332288'),
    ('g8', '(a)(15) Formations, markers', [15], '#999933'),
]


def lum(hexc):
    r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ink(hexc):
    L = lum(hexc)
    cw, cd = 1.05 / (L + 0.05), (L + 0.05) / (lum('#111111') + 0.05)
    return '#ffffff' if cw >= 4.5 and cw >= cd else '#111111'


def group_of(code):
    n = int(re.match(r'\(a\)\((\d+)\)', code)[1])
    for g in GROUPS:
        if n in g[2]:
            return g
    return None


for c in met:
    assert group_of(c), c
used_groups = [g for g in GROUPS if any(group_of(c) is g for c in met)]
for g in GROUPS:
    print(f'{g[1]:40s} {g[3]}  text {ink(g[3])}  contrast-ok')

# ================================================================ diagram raster
doc = fitz.open(os.path.join(ROOT, r'06-study\sample\diagrams\W01.pdf'))
page = doc[0]
words = page.get_text('words')
CX0, CY0, CX1, CY1 = 24, 6, 608, 772
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
PH, PITCH, PADX = 9.6, 11.4, 3.0


def tw(t, bold=False, size=FS):
    return fitz.get_text_length(t, fontname='hebo' if bold else 'helv', fontsize=size)


def label(lab):
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
F_ = {
    '(a)(1).operator_name': ([W('Aera'), W('Energy'), W('LLC')], 'h'),
    '(a)(1).well_number': ([W('948C-28')], 'h'),
    '(a)(1).api_number': ([W('0403033530')], 'h'),
    '(a)(2).spud_date': ([W('7/3/2007', (470, 69))], 'h'),
    '(a)(3).ground_elevation': ([W('591.26ft')], 'right'),
    '(a)(4).reference_elevation': ([W('KELLY'), W('BUSHING'), W('@', (531, 28)), W('603.26ft'), W('(default)')], 'top'),
    '(a)(5).freshwater_base.md': ([W('N/A', (121, 691))], 'h'),
    '(a)(6).usdw_base.md': ([W('N/A', (125, 656))], 'h'),
    '(a)(7).casing_size': (row(142, 163, 30, 60), 'h'),
    '(a)(7).casing_grade': ([W('K-55,', (294, 173.8))], 'h'),
    '(a)(7).connection_type': ([W('PLAIN'), W('END,')], 'h'),
    '(a)(7).casing_weight': ([W('36.00ppf,')], 'h'),
    '(a)(8).shoe_depth.md': (row(142, 163, 150, 180), 'h'),
    '(a)(9).perforation_depths.md': ([W('880.000ft,'), W('881.000ft,')], 'h'),
    '(a)(9).perforation_intervals.md': ([W('1,440.000ft,'), W('1,441.000ft,')], 'h'),
    '(a)(11).hole_diameter': ([W('24.00in')], 'h'),
    '(a)(11).hole_depth.md': ([W('2174.00ft')], 'right'),
    '(a)(13).cement_fill_identification': ([W('CEMENT'), W('STAGES')], 'h'),
    '(a)(13).cement_fill_top.md': ([W('13', (131.9, 205.3))], 'h'),
    '(a)(13).cement_fill_bottom.md': ([W('2,164')], 'h'),
    '(a)(15).formation_names': ([W('Tulare')], 'h'),
    '(a)(15).formation_depths.md': ([W('70.25')], 'h'),
    '(a)(15).marker_names': ([W('Reef'), W('Ridge'), W('Diatomite')], 'h'),
    '(a)(15).marker_depths.md': ([W('710.00')], 'h'),
}
CHAN = {'(a)(2).spud_date': 86.0, '(a)(11).hole_diameter': 91.0}
assert set(met) == set(F_), (set(met) ^ set(F_))
GF = {c: box(ws, GP) for c, (ws, _) in F_.items()}

# ================================================================ red frames: present but not required (excess data)
RED = []  # [name, reason, bbox]


def clip(b, xmax=193.6):
    return (b[0], b[1], min(b[2], xmax), b[3])


RED.append(['Well type ("Type: Producer")', 'well type is not a § 1724.7.1(a) item', box(row(44, 53, 0, 200))])
NEUTRAL = [['Wellbore number ("Wellbore: 00")', 'supports § 1724.7.1(c) borehole coverage; not a scored point', box(row(52, 61, 0, 200)), '§1724.7.1(c)']]
RED.append(['PBMD 2,143.17 ft', 'plugged-back depth is not listed in (a)', box(row(44, 53, 400, 600))])
RED.append(['Orientation: Directional', 'well orientation is not listed in (a)', box(row(60, 69, 400, 600))])
RED.append(['Casing table, Top MD column', 'casing top/hanger depths are not shoe, stub, or liner-top depths ((a)(8))',
            box(wsel(lambda w: 85 <= w[0] and w[2] <= 119 and 128 <= w[1] <= 163))])
csg_lines = sorted({round(w[1], 1) for w in words if w[4] == 'CSG:' and w[0] > 190})
for y in csg_lines:
    lw = sorted(row(y + 1, y + 5, 190, 400), key=lambda w: w[0])
    RED.append([f'Casing string top depth "{lw[-2][4].rstrip(",")}"', 'string/segment top depth is not a shoe, stub, or liner-top depth ((a)(8))', box([lw[-2]], 0.7)])
    if lw[-1][4].rstrip(',') in ('735.17ft', '2,143.17ft'):
        RED.append([f'7-in segment bottom "{lw[-1][4]}"', 'internal segment break in the 7-in string, not a shoe depth ((a)(8))', box([lw[-1]], 0.7)])
RED.append(['Flag joint @ 735 ft', 'marker joint for depth correlation; not an (a)(9)/(a)(10) item', box(row(232, 240, 300, 400))])
for k, w in enumerate(sorted(wsel(lambda w: 'shot/ft' in w[4]), key=lambda w: w[1])):
    RED.append([f'Shot density "4.000shot/ftSPF", perforation line {k + 1} of 24',
                'perforation shot density is not listed; (a)(9) asks for depths/intervals', box([w], 0.7)])
RED.append(['Cement job 1: "Job Type: Primary  Date: 7/3/2007"', 'cement-job type and date are not listed in (a)(13)', box(row(178, 187, 0, 200))])
RED.append(['Cement job 2: "Job Type: Primary  Date: 7/23/2007"', 'cement-job type and date are not listed in (a)(13)', box(row(216, 225, 0, 200))])
RED.append(['REMARKS, 9.625-in surface cement recipe', 'sacks, slurry ppg, yield, additives and returns are subdivision (b) cement data, not (a)',
            clip(box(row(264, 298, 0, 200)))])
RED.append(['REMARKS, 7-in production cement recipe', 'same as above', clip(box(row(304, 332, 0, 202)))])
RED.append(['PLUG DETAILS, tubing assembly (hanger to chamfered collar)', 'tubing components are not cement plugs ((a)(12)) or SSV/packer/gas-lift mandrel ((a)(10))',
            box(row(428, 517, 0, 200))])
RED.append(['PLUG DETAILS, rod-string assembly (polished rod to rod pump)', 'rod-string components are not listed in (a)', box(row(522, 597, 0, 200))])
RED.append(['Drawing sign-off "Initials: xyz  Date: 11/30/2023"', 'preparer initials and drawing date are not listed in (a)', box(row(758, 768, 0, 200))])

RED_BEFORE = len(RED) + 1   # + Wellbore: 00, which was red before the previous revision
RECLASS = {
    'Casing table, Top MD': ('CalGEM P&A guidance', 'CalGEM Permitting, Forms, and Compliance (For Operators) page, P&A wellbore schematic: "casing intervals and sizes"'),
    'Casing string top depth': ('CalGEM P&A guidance', 'CalGEM Permitting, Forms, and Compliance (For Operators) page, P&A wellbore schematic: "casing intervals and sizes"'),
    'Well type': ('§1724.7(a)(3)(D)', 'UIC project data must identify injection vs. production wells'),
    'REMARKS, 9.625-in': ('§1724.7.1(b)(2)', 'cement slurry documentation that must accompany the diagram'),
    'REMARKS, 7-in': ('§1724.7.1(b)(2)', 'cement slurry documentation that must accompany the diagram'),
    'Cement job': ('§1724.7.1(b)(2)', 'cement-slurry information is required for each cement job completed; job type/date identify the job'),
    'Orientation': ('§1724.7.1(b)(3)', 'wellbore path; the diagram flags directional but supplies no survey'),
}
for r in list(RED):
    for k, (tag, why) in RECLASS.items():
        if r[0].startswith(k):
            RED.remove(r)
            NEUTRAL.append([r[0], 'supports ' + tag + ': ' + why + '; not a scored point', r[2], tag])
assert len(NEUTRAL) == 13, [n[0] for n in NEUTRAL]
# one CalGEM tag per cluster of casing-top frames; anchor = cluster bbox
_ct = sorted([n for n in NEUTRAL if n[3] == 'CalGEM P&A guidance'], key=lambda n: n[2][1])
_cl = []
for n in _ct:
    b = n[2]
    hit = None
    for cl in _cl:
        h = cl[1][0][2]
        if abs((b[0] + b[2]) / 2 - (h[0] + h[2]) / 2) < 120:
            hit = cl
    if hit:
        cb = hit[0]
        if b[1] - hit[1][0][2][1] < 70:   # anchor = top sub-group only
            hit[0] = (min(cb[0], b[0]), min(cb[1], b[1]), max(cb[2], b[2]), max(cb[3], b[3]))
        hit[1].append(n)
        continue
    _cl.append([b, [n]])
for cb, members in _cl:
    for j, n in enumerate(members):
        if j:
            n[3] = ''
        else:
            n.append(cb)
print('CalGEM casing-top clusters:', len(_cl))
print(f'red frames: before {RED_BEFORE - 1} (previous revision), now {len(RED)}; dashed slate: {len(NEUTRAL)}')
PROV = [r for r in RED if r[0].startswith('Drawing sign-off')]
RED = [r for r in RED if not r[0].startswith('Drawing sign-off')]
assert len(PROV) == 1
print(f'red frames now {len(RED)}; provenance {len(PROV)}')
MTYPES = [  # (id, label, name prefixes)
    ('E1', 'PBMD (plugged-back depth)', ['PBMD']),
    ('E2', 'Inner 7-in segment bottoms', ['7-in segment bottom']),
    ('E3', 'Flag joint', ['Flag joint']),
    ('E4', 'Perforation shot density (SPF)', ['Shot density']),
    ('E5', 'Tubing assembly (PLUG DETAILS)', ['PLUG DETAILS, tubing']),
    ('E6', 'Rod-string assembly (PLUG DETAILS)', ['PLUG DETAILS, rod']),
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
for r in RED + NEUTRAL + PROV:
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


def rowy(i):
    return ROW0 + i * PITCH + PH / 2


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
for r in RED + NEUTRAL + PROV:
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
print('badge costs (dark px + penalties):', {num[c]: l['badge_cost'] for l in lines for c in [l['code']]})

# ================================================================ SVG
F = "Helvetica, Arial, 'Liberation Sans', sans-serif"
GREY_F, GREY_S, GREY_T = '#f0f0f0', '#cfcfcf', '#9b9b9b'
REDC = '#d62728'
NEUC = '#44546A'
PROVC = '#111111'
o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
         f'width="8.5in" height="11in" viewBox="0 0 816 1056" font-family="{F}">')
o.append('<title>W01 atomic data-point map</title>')
o.append('<rect width="816" height="1056" fill="#ffffff"/>')
o.append(f'<text x="{M0X}" y="{M0Y + 13}" font-size="14.7" font-weight="bold" fill="#111">'
         f'Casing diagram W01: {n_total} atomic data points, 14 CCR § 1724.7.1(a)</text>')
o.append(f'<text x="{M0X}" y="{M0Y + 27}" font-size="9.3" fill="#444">{n_met} MET (coloured by requirement group, framed and '
         f'numbered in W01) · {n_total - n_met} MISSING (grey) · red frames: present but not required · completeness {score * 100:.1f}%</text>')
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


def pill(x, w, y, n, name, code, numbered=True):
    g = group_of(code) if status[code] == 'MET' else None
    if g:
        f, st, t = g[3], g[3], ink(g[3])
    else:
        f, st, t = GREY_F, GREY_S, GREY_T
    r = f'<rect x="{x}" y="{y:.2f}" width="{w}" height="{PH}" rx="{PH / 2}" fill="{f}" stroke="{st}" stroke-width="0.55"/>'
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
    y = ROW0 + i * PITCH
    o.append(pill(X1, W1, y, n, label(lab).replace('&', '&amp;'), c))
    if c.endswith('.md'):
        tp = tvd[c[:-3]]
        o.append(pill(X2, W2, y, tp[0], '', tp[1], numbered=False))
rows_bottom = ROW0 + len(md) * PITCH


def text(x, y, t, size=FS, color='#333', weight=None, anchor=None):
    w = f' font-weight="{weight}"' if weight else ''
    a = f' text-anchor="{anchor}"' if anchor else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}"{w}{a}>{t}</text>'


# ---- key (left column, below the pills)
LY = rows_bottom + 15
LX = X1
o.append(text(LX, LY, 'Key: MET, by requirement group', 9.3, '#111', 'bold'))
LY += 12
for g in used_groups:
    o.append(f'<rect x="{LX}" y="{LY - 7.4}" width="16" height="{PH}" rx="{PH / 2}" fill="{g[3]}"/>')
    o.append(text(LX + 21, LY, g[1].replace('&', '&amp;')))
    LY += 10.6
LY += 2
o.append(f'<rect x="{LX}" y="{LY - 7.4}" width="16" height="{PH}" rx="{PH / 2}" fill="{GREY_F}" stroke="{GREY_S}" stroke-width="0.55"/>')
o.append(text(LX + 21, LY, 'MISSING: no answer in W01, no line'))
LY += 13
o.append(f'<rect x="{LX + 0.5}" y="{LY - 7.6}" width="15" height="9" fill="none" stroke="#0072B2" stroke-width="0.9" rx="0.8"/>'
         f'<rect x="{LX + 18}" y="{LY - 7.6}" width="0" height="0"/>')
o.append(text(LX + 21, LY, 'Coloured frame + badge = the answer'))
LY += 13.6
o.append(f'<rect x="{LX + 0.5}" y="{LY - 7.6}" width="15" height="9" fill="none" stroke="{REDC}" stroke-width="0.7" rx="0.8"/>')
o.append(text(LX + 21, LY, 'Red frame: Excess data — present, not'))
o.append(text(LX + 21, LY + 10.4, 'required by the specification; not scored'))
o.append(text(LX + 21, LY + 20.8, '(overproduction: “more information than'))
o.append(text(LX + 21, LY + 31.2, 'necessary”; Ubarana et al., 2021)'))
LY += 44
o.append(f'<rect x="{LX + 0.5}" y="{LY - 7.6}" width="15" height="9" fill="none" stroke="{NEUC}" stroke-width="0.9" stroke-dasharray="2 1.2" rx="0.8"/>')
o.append(text(LX + 21, LY, 'Dashed slate + tag: supports another'))
o.append(text(LX + 21, LY + 10.4, 'requirement or CalGEM guidance for'))
o.append(text(LX + 21, LY + 20.8, 'this diagram; not one of the 77'))
o.append(text(LX + 21, LY + 31.2, 'scored points'))
LY += 31.2 + 13
o.append(f'<rect x="{LX + 0.5}" y="{LY - 7.6}" width="15" height="9" fill="none" stroke="{PROVC}" stroke-width="1.0" stroke-dasharray="0.1 1.6" stroke-linecap="round"/>')
o.append(text(LX + 21, LY, 'Document provenance: who prepared'))
o.append(text(LX + 21, LY + 10.4, 'the diagram and when; not required'))
LY += 10.4 + 15
# ---- dashed-slate list (left column)
o.append(text(LX, LY, 'Supports another requirement (not scored)', FS, '#111', 'bold'))
LY += 11
SLATE_ROWS = [('"Wellbore: 00"', '§1724.7.1(c)'), ('"Type: Producer"', '§1724.7(a)(3)(D)'),
              ('Cement REMARKS ×2', '§1724.7.1(b)(2)'), ('Cement job type/date ×2', '§1724.7.1(b)(2)'),
              ('"Orientation: Directional"', '§1724.7.1(b)(3)'), ('Casing tops ×6', 'CalGEM P&A guidance')]
assert sum(int(r[0].split('×')[1]) if '×' in r[0] else 1 for r in SLATE_ROWS) == len(NEUTRAL)
RX = IX - 12
for lab_, tag_ in SLATE_ROWS:
    w_ = tw(tag_) + 5
    o.append(text(LX, LY, lab_))
    o.append(f'<rect x="{RX - w_:.2f}" y="{LY - 7.0:.2f}" width="{w_:.2f}" height="9" rx="1.5" fill="{NEUC}"/>')
    o.append(text(RX - w_ / 2, LY, tag_.replace('&', '&amp;'), FS, '#fff', None, 'middle'))
    LY += 10.6
left_bottom = LY - 10.6


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
o.append(text(SX, SY, 'Completeness = number of atomic data points marked MET ÷ 77', FS, '#111', 'bold'))
SY += 11.5
for t_ in [f'MD / non-depth points MET: {met_md} of {n_md}', f'TVD points MET: {met_tvd} of {n_tvd}',
           f'Total MET: {met_md} + {met_tvd} = {n_met}']:
    o.append(text(SX + 8, SY, t_))
    SY += 10.4
o.append(text(SX + 8, SY + 1, f'Completeness(W01) = {n_met} ÷ {n_total} = {score:.3f} → {score * 100:.1f}%', 10.0, '#111', 'bold'))
SY += 16
notes = [
    ('MD vs TVD.', 'MD (measured depth) is distance along the borehole; TVD (true vertical depth) is the vertical depth of the '
     'same point. A row\'s MD and TVD cells are one datum in two measurement types, scored as two points, not duplicates; '
     'rows with no TVD cell are non-depth items. W01 is directional but reports MD only, so every TVD point is MISSING. '
     'Repeated data are framed at one representative instance.'),
    ('Sources.', 'casing-diagram-atomic-checklist-v2.txt; casing_specs.db, diagram_requirement_results (W01), checked against '
     'W01.pdf; frame positions from PDF text boxes.'),
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
o.append(text(MX, MY, 'Excess data found in W01', 9.3, '#111', 'bold'))
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
o.append(text(MX, MY, 'Records who prepared the diagram and when.', FS, '#444'))
MY += 11
o.append(f'<rect x="{MX + 0.5}" y="{MY - 7.6}" width="15" height="9" fill="none" stroke="{PROVC}" stroke-width="1.0" stroke-dasharray="0.1 1.6" stroke-linecap="round"/>')
o.append(text(MX + 23, MY, '"Initials: xyz  Date: 11/30/2023"'))
o.append(text(MR, MY, f'×{len(PROV)}', FS, '#111', None, 'end'))
right_bottom = MY
SY = max(left2_bottom, right_bottom) + 10.8
o.append('</svg>')
open(OUT, 'w', encoding='utf-8').write('\n'.join(o))
print(f'rows bottom {rows_bottom:.1f}, key bottom {left_bottom:.1f}, legend bottom {SY - 10.8:.1f} (limit {M1Y})')
print('groups used:', [(g[1], g[3]) for g in used_groups])
