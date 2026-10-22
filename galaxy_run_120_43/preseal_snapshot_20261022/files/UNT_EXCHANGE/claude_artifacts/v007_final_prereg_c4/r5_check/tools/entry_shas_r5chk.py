# entry_shas_r5chk.py -- independent re-extraction of V005 entry section shas (r5_check helper).
# usage: python3 -I -B entry_shas_r5chk.py ADDENDUM.md PREREG_R5.json OUT.json
# Section rule (as r5 states it): bytes from the first byte of the heading line "## A<n>:" up to,
# not including, the first byte of the next line beginning with "## " (or EOF).
# Implemented independently on raw bytes (no text decoding of the boundaries).
import sys, json, hashlib, re
addp, prp, outp = sys.argv[1:4]
b = open(addp, 'rb').read()
# line starts
starts = [0] + [i + 1 for i, c in enumerate(b) if c == 0x0A and i + 1 < len(b)]
heads = [s for s in starts if b.startswith(b'## ', s)]
entries = {}
dups = []
for idx, s in enumerate(heads):
    m = re.match(rb'## (A[0-9]+):', b[s:s + 16])
    if not m:
        continue
    e = m.group(1).decode()
    nxt = [h for h in heads if h > s]
    end = nxt[0] if nxt else len(b)
    sec = b[s:end]
    if e in entries:
        dups.append(e)
    entries[e] = {'sha256': hashlib.sha256(sec).hexdigest(), 'bytes': len(sec),
                  'heading': b[s:b.index(b'\n', s)].decode('utf-8')}
pr = json.load(open(prp))
rows = pr['entries_after_A81']['rows']
res = {'schema': 'R5CHK_ENTRY_SHAS_V001', 'addendum_sha256': hashlib.sha256(b).hexdigest(),
       'addendum_bytes': len(b), 'entries_found': sorted(entries, key=lambda x: int(x[1:])),
       'duplicate_headings': dups, 'rows': []}
for r in rows:
    e = r['entry']
    mine = entries.get(e)
    res['rows'].append({'entry': e, 'decision': r['decision'],
                        'r5_sha256': r['section_sha256'], 'mine_sha256': mine and mine['sha256'],
                        'r5_bytes': r.get('section_bytes'), 'mine_bytes': mine and mine['bytes'],
                        'heading_equal': bool(mine) and mine['heading'] == r.get('heading'),
                        'match': bool(mine) and mine['sha256'] == r['section_sha256']})
covered = {r['entry'] for r in rows}
later = [e for e in entries if int(e[1:]) >= 82]
res['entries_ge_A82_without_row'] = sorted([e for e in later if e not in covered], key=lambda x: int(x[1:]))
res['rows_without_entry'] = sorted([e for e in covered if e not in entries])
res['all_match'] = all(x['match'] and x['heading_equal'] for x in res['rows'])
with open(outp, 'x') as f:
    json.dump(res, f, indent=1)
print('rows', len(rows), 'all_match', res['all_match'], 'uncovered>=A82', res['entries_ge_A82_without_row'],
      'rows_without_entry', res['rows_without_entry'], 'dups', dups, 'addendum', res['addendum_sha256'][:8])
for x in res['rows']:
    if not (x['match'] and x['heading_equal']):
        print('MISMATCH', x)
