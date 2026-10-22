"""0361 PDF page locator (stdlib only). Maps keyword hits and table/figure-likeness to page numbers WITHOUT printing page text.
Output per page: counts of keyword hits, digit fraction of extracted text, presence of 'Table'/'Figure' captions. No text emitted.
Usage: python3 -I -B pdf_page_locator_0361_v001.py <pdf> <expected_sha256>"""
import hashlib, re, sys, zlib, json
P, H = sys.argv[1], sys.argv[2]
b = open(P, 'rb').read()
assert hashlib.sha256(b).hexdigest() == H, 'E_PIN'
objs = {}
for m in re.finditer(rb'(\d+)\s+0\s+obj(.*?)endobj', b, re.S):
    objs[int(m.group(1))] = m.group(2)
def stream_of(body):
    m = re.search(rb'stream\r?\n(.*?)\r?\nendstream', body, re.S)
    if not m: return None
    data = m.group(1)
    if b'/FlateDecode' in body.split(b'stream')[0]:
        try: return zlib.decompress(data)
        except Exception:
            try: return zlib.decompressobj().decompress(data)
            except Exception: return None
    return data
# object streams
for n, body in list(objs.items()):
    if b'/ObjStm' in body.split(b'stream')[0]:
        s = stream_of(body)
        if s is None: continue
        N = int(re.search(rb'/N\s+(\d+)', body).group(1)); first = int(re.search(rb'/First\s+(\d+)', body).group(1))
        hdr = s[:first].split()
        pairs = [(int(hdr[2*i]), int(hdr[2*i+1])) for i in range(N)]
        for i, (on, off) in enumerate(pairs):
            end = pairs[i+1][1] if i+1 < N else len(s) - first
            objs.setdefault(on, s[first+off:first+end])
def ref(x):
    m = re.match(rb'\s*(\d+)\s+0\s+R', x); return int(m.group(1)) if m else None
root_pages = None
for n, body in objs.items():
    if re.search(rb'/Type\s*/Catalog', body):
        root_pages = int(re.search(rb'/Pages\s+(\d+)\s+0\s+R', body).group(1))
pages = []
def walk(n):
    body = objs[n]
    if re.search(rb'/Type\s*/Pages', body):
        kids = re.search(rb'/Kids\s*\[(.*?)\]', body, re.S).group(1)
        for k in re.findall(rb'(\d+)\s+0\s+R', kids): walk(int(k))
    else:
        pages.append(n)
walk(root_pages)
def contents(n):
    body = objs[n]
    m = re.search(rb'/Contents\s*(\[(.*?)\]|(\d+)\s+0\s+R)', body, re.S)
    refs = [int(x) for x in re.findall(rb'(\d+)\s+0\s+R', m.group(2))] if m.group(2) is not None else [int(m.group(3))]
    out = b''
    for r in refs:
        s = stream_of(objs[r])
        if s: out += s + b'\n'
    return out
def text_of(cs):
    parts = []
    for m in re.finditer(rb'\[(.*?)\]\s*TJ|\((?:\\.|[^\\)])*\)\s*Tj', cs, re.S):
        seg = m.group(0)
        for s in re.findall(rb'\(((?:\\.|[^\\)])*)\)', seg):
            s = re.sub(rb'\\([()\\])', rb'\1', s)
            parts.append(s.decode('latin-1'))
        parts.append(' ')
    return ''.join(parts)
KW = ['kill', 'error', 'uncertaint', 'surface brightness profile', 'sky', 'outer', 'truncat', 'extrapolat', 'archangel', 'ellipse',
      'isophot', 'mask', 'reject', 'photometr', 'rotation curve', 'velocit', 'table', 'figure', 'fig.', 'decomposition', 'bulge']
res = []
for i, n in enumerate(pages, 1):
    t = text_of(contents(n))
    low = t.lower()
    nd = sum(c.isdigit() for c in t); na = sum(c.isalpha() for c in t)
    res.append({'page': i, 'chars': len(t), 'digit_fraction': round(nd / max(1, nd + na), 3),
                'kw': {k: low.count(k) for k in KW if low.count(k)}})
print(json.dumps({'n_pages': len(pages), 'pages': res}))
