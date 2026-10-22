"""Lens R2-B: independent byte-level recomputation of the V005 per-entry section pins of PREREG r2 section 11.
Reads only V005 (open root addendum) and the prereg text. Writes one JSON with exclusive create."""
import hashlib, json, re, sys
V005 = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
PREREG = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/miss_reading_prereg_c4/r2/round2/PREREG_MISS_READING_R2.md'
out_path = sys.argv[1]
raw = open(V005, 'rb').read()
pre = open(PREREG, 'rb').read().decode('utf-8')
lines = raw.split(b'\n')
heads = [i for i, l in enumerate(lines) if l.startswith(b'## ')]
pins = []
for line in pre.split('\n'):
    m = re.match(r'^\| A(\d{1,3}) \|(.*)\| `([0-9a-f]{64})` \|$', line)
    if m:
        cells = [c.strip() for c in m.group(2).split('|')]
        pins.append((int(m.group(1)), cells[-1], m.group(3)))
res = {'v005_sha256': hashlib.sha256(raw).hexdigest(), 'n_lines': len(lines), 'entries': []}
for n, marker, stated in pins:
    idx = [j for j, i in enumerate(heads) if re.match(rb'^## A%d:' % n, lines[i])]
    rec = {'entry': 'A%d' % n, 'marker': marker, 'stated': stated, 'n_headings': len(idx)}
    if len(idx) != 1:
        res['entries'].append(rec); continue
    j = idx[0]; i = heads[j]
    end = heads[j + 1] if j + 1 < len(heads) else len(lines)
    mk = marker.strip('`')
    if mk and mk not in ('next heading', '—'):
        hits = [k for k in range(i + 1, end) if lines[k].startswith(mk.encode())]
        rec['marker_hits_in_heading_region'] = [k + 1 for k in hits]
        rec['heading_region_lines'] = [i + 1, end]
        if hits:
            tail = b'\n'.join(lines[hits[0]:end]) + (b'\n' if end < len(lines) else b'')
            rec['unpinned_tail_lines'] = [hits[0] + 1, end]
            rec['unpinned_tail_sha256'] = hashlib.sha256(tail).hexdigest()
            rec['unpinned_tail_first_lines'] = [l.decode('utf-8')[:120] for l in lines[hits[0]:hits[0] + 3]]
            end = hits[0]
    body = b'\n'.join(lines[i:end]) + (b'\n' if end < len(lines) else b'')
    rec['current'] = hashlib.sha256(body).hexdigest()
    rec['match'] = rec['current'] == stated
    rec['lines'] = [i + 1, end]
    res['entries'].append(rec)
res['all_match'] = all(e.get('match') for e in res['entries'])
res['n_pins'] = len(pins)
with open(out_path, 'x') as f:
    json.dump(res, f, indent=1, sort_keys=True)
print(json.dumps({'all_match': res['all_match'], 'n_pins': len(pins), 'v005': res['v005_sha256']}))
for e in res['entries']:
    print(e['entry'], e.get('match'), e.get('lines'), e.get('marker_hits_in_heading_region', ''), e.get('unpinned_tail_lines', ''))
