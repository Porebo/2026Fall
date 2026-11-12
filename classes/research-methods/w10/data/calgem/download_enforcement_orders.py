import csv, datetime, hashlib, html, io, json, pathlib, re, sys, time, urllib.parse, urllib.request
import pypdf

DEST = pathlib.Path(sys.argv[1])          # project folder for the PDFs and index
HITS = pathlib.Path(sys.argv[2])          # scratch JSON with text snippets
DEST.mkdir(parents=True, exist_ok=True)
BASE = 'https://www.conservation.ca.gov'
UA = {'User-Agent': 'Mozilla/5.0 (research script)'}

page = urllib.request.urlopen(urllib.request.Request(BASE + '/calgem/Pages/Division_Orders.aspx', headers=UA), timeout=60).read().decode('utf8', 'replace')
links, seen = [], set()
for m in re.finditer(r'<a[^>]+href="([^"]+\.pdf)"[^>]*>(.*?)</a>', page, re.I | re.S):
    href = html.unescape(m.group(1))
    label = re.sub(r'<[^>]+>|\s+|​', ' ', html.unescape(m.group(2))).strip()
    label = re.sub(r'\s+', ' ', label)
    if href.startswith('/'):
        href = BASE + href
    if href not in seen:
        seen.add(href); links.append((href, label))

pat = re.compile(r'well\s*-?bore\s+diagram|casing\s+diagram|well\s+diagram|schematic|1724\.7\.1|1772\.1\.3|well summary|history of (oil or gas )?well', re.I)
index, hits = [], []
for i, (href, label) in enumerate(links):
    url = urllib.parse.quote(urllib.parse.unquote(href), safe=':/')
    name = urllib.parse.unquote(href.rsplit('/', 1)[1])
    target = DEST / name
    rec = {'list_order': i + 1, 'label': label, 'url': url, 'file': name}
    try:
        if target.exists():
            b = target.read_bytes()
        else:
            b = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
            target.write_bytes(b)
            time.sleep(0.5)
        rec['downloaded'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        rec['bytes'] = len(b)
        rec['sha256'] = hashlib.sha256(b).hexdigest().upper()
        r = pypdf.PdfReader(io.BytesIO(b))
        rec['pages'] = len(r.pages)
        txt = re.sub(r'\s+', ' ', ' '.join((p.extract_text() or '') for p in r.pages))
        rec['text_chars'] = len(txt)
        snippets = [txt[max(0, m.start() - 300): m.end() + 400] for m in pat.finditer(txt)][:12]
        if snippets:
            hits.append({'label': label, 'file': name, 'hits': snippets})
    except Exception as e:
        rec['error'] = str(e)[:200]
    index.append(rec)
    if i % 25 == 0:
        print(i, len(links), flush=True)

cols = ['list_order', 'label', 'file', 'url', 'downloaded', 'bytes', 'pages', 'text_chars', 'sha256', 'error']
with open(DEST / '_index.csv', 'w', newline='', encoding='utf-8') as h:
    w = csv.DictWriter(h, fieldnames=cols); w.writeheader()
    for rec in index:
        w.writerow({k: rec.get(k, '') for k in cols})
json.dump(hits, open(HITS, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('done', len(index), 'errors', sum(1 for r in index if 'error' in r), 'with diagram hits', len(hits))
