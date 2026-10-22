# Claude4 lens_diff (5): first line of every NEW-n id (bracketed [NEW-n] tag and any bare NEW-n) in r13 and r14; compare with the
# c08_table rows of root's SEAL_MANUAL_DISCLOSURES V001 / V002 / V003_DRAFT.  Read-only on author/root files; one exclusive write.
import hashlib, json, re
from pathlib import Path
C = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
SRC = {'r13': C / 'v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py', 'r14': C / 'v007_compare_c2/r14/kmax_tail_compare_c2v007_r14_cx1v001.py'}
WANT = {'r13': 'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157', 'r14': 'f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7'}
DISC = {v: C / ('seal_assembly_c3/root_inputs/SEAL_MANUAL_DISCLOSURES_%s.json' % v) for v in ('V001', 'V002', 'V003_DRAFT')}
OUT = Path(__file__).resolve().parent.parent / 'out' / 'NEW_TAG_LINES_C4.json'
BR = re.compile(r'\[NEW-(\d{1,3})(?!\d)')            # a bracketed tag opening: [NEW-n] or [NEW-n ...]
ANY = re.compile(r'(?<![A-Za-z0-9])NEW-(\d{1,3})(?!\d)')
res = {'sources': {}, 'disclosures': {}}
first = {}
for tag, p in SRC.items():
    b = p.read_bytes()
    assert hashlib.sha256(b).hexdigest() == WANT[tag], tag
    lines = b.decode().split('\n')
    fb, fa, allids = {}, {}, {}
    for n, l in enumerate(lines, 1):
        for m in BR.finditer(l):
            fb.setdefault('NEW-' + m.group(1), n)
        for m in ANY.finditer(l):
            fa.setdefault('NEW-' + m.group(1), n)
            allids.setdefault('NEW-' + m.group(1), []).append(n)
    first[tag] = {'bracketed': fb, 'any': fa, 'all': allids, 'lines': lines}
    res['sources'][tag] = {'sha256': WANT[tag], 'n_ids_any': len(fa), 'n_ids_bracketed': len(fb)}
res['ids_same_r13_r14_any'] = sorted(first['r13']['any']) == sorted(first['r14']['any'])
res['ids_same_r13_r14_bracketed'] = sorted(first['r13']['bracketed']) == sorted(first['r14']['bracketed'])
res['first_line_same_any'] = {k: first['r13']['any'][k] == first['r14']['any'].get(k) for k in first['r13']['any']}
res['first_line_same_bracketed'] = {k: first['r13']['bracketed'][k] == first['r14']['bracketed'].get(k) for k in first['r13']['bracketed']}
res['every_occurrence_line_same'] = first['r13']['all'] == first['r14']['all']
res['ids_any'] = {k: {'first_any': first['r14']['any'][k], 'first_bracketed': first['r14']['bracketed'].get(k),
                      'n_occurrences': len(first['r14']['all'][k])} for k in sorted(first['r14']['any'], key=lambda s: int(s[4:]))}
for v, p in DISC.items():
    raw = p.read_bytes()
    d = json.loads(raw)
    rows = d.get('c08_table', [])
    chk = []
    for r in rows:
        nid, f, ln = r['new_item_id'], r['file'], r['line']
        which = 'r14' if 'r14' in f else ('r13' if 'r13' in f else '?')
        L = first['r14']['lines'] if which == 'r14' else first['r13']['lines']
        text = L[ln - 1] if 0 < ln <= len(L) else None
        chk.append({'id': nid, 'file': f, 'line': ln, 'file_round': which,
                    'line_has_id': bool(text and re.search(r'(?<![A-Za-z0-9])%s(?!\d)' % re.escape(nid), text)),
                    'line_has_bracketed_tag': bool(text and re.search(r'\[%s(?!\d)' % re.escape(nid), text)),
                    'eq_first_any': ln == first[which if which != '?' else 'r14']['any'].get(nid),
                    'eq_first_bracketed': ln == first[which if which != '?' else 'r14']['bracketed'].get(nid),
                    'same_line_text_r13_r14': first['r13']['lines'][ln - 1] == first['r14']['lines'][ln - 1],
                    'text': (text or '')[:160]})
    res['disclosures'][v] = {'sha256': hashlib.sha256(raw).hexdigest(), 'n_rows': len(rows), 'rows': chk,
                             'ids_eq_source_ids_any': sorted(r['new_item_id'] for r in rows) == sorted(first['r14']['any']),
                             'all_rows_eq_first_any': all(c['eq_first_any'] for c in chk),
                             'all_rows_line_has_id': all(c['line_has_id'] for c in chk),
                             'all_rows_bracketed': all(c['line_has_bracketed_tag'] for c in chk),
                             'files': sorted({r['file'] for r in rows})}
with open(OUT, 'x') as f:
    json.dump(res, f, indent=1)
print(json.dumps({k: v for k, v in res.items() if k not in ('disclosures',)}, indent=1))
for v, d in res['disclosures'].items():
    print(v, d['sha256'][:8], 'rows', d['n_rows'], 'files', d['files'], 'ids==source', d['ids_eq_source_ids_any'],
          'all first-any', d['all_rows_eq_first_any'], 'all has id', d['all_rows_line_has_id'], 'all bracketed', d['all_rows_bracketed'])
    for c in d['rows']:
        if not (c['eq_first_any'] and c['line_has_id']):
            print('   MISMATCH', c)
