"""Claude4 r5 helper: audit prereg r5 against r4 from bytes. (1) every leaf that differs from r4 lies inside a clause the r5 change log
(DELTA_R4_R5.md) names; (2) every untouched r4 clause is byte-identical; (3) census of PENDING / PENDING_ROOT_RULING markers; (4) every
entry-table row's section sha re-derived from the generation byte copy. Read-only except its own exclusive-create output.
usage: python3 -I -B audit_r5_vs_r4_c4v001.py R4.json R5.json DELTA.md ADDENDUM_COPY OUT.json"""
import hashlib, json, re, sys
from pathlib import Path
r4p, r5p, deltap, addp, outp = sys.argv[1:6]
a, b = json.loads(Path(r4p).read_bytes()), json.loads(Path(r5p).read_bytes())


def leaves(o, p=()):
    if isinstance(o, dict):
        r = {}
        for k, v in o.items():
            r.update(leaves(v, p + (str(k),)))
        return r or {p: '{}'}
    if isinstance(o, list):
        r = {}
        for i, v in enumerate(o):
            r.update(leaves(v, p + (str(i),)))
        return r or {p: '[]'}
    return {p: json.dumps(o, ensure_ascii=False)}


la, lb = leaves(a), leaves(b)
diff = sorted(k for k in set(la) | set(lb) if la.get(k) != lb.get(k))
logged = re.findall(r'^\| \d+ \| `([^`]+)` \|', Path(deltap).read_text(), re.M)
names = set()
for c in logged:
    parts = [q for part in c.split(' / ') for q in part.split(', ')]
    head = parts[0]
    pre = head.rsplit('.', 1)[0] + '.' if '.' in head else ''
    for q in parts:
        if '.' not in q and pre and not q.startswith(('status', 'assembly', 'decision_pins_pending_at_seal', 'cites_by_name')):
            q = pre + q
        names.add(q)


def clause_of(k):
    s = '.'.join(k)
    s = re.sub(r'^seal_record_requirements\.(\d+)', r'seal_record_requirements[\1]', s)
    return s


def covered(k):
    s = clause_of(k)
    if k[0] in ('root_items',):          # re-sorted list: checked by id below
        return True
    for n in names:
        nn = n.split('..')[0]
        if s == nn or s.startswith(nn + '.') or s.startswith(nn + '['):
            return True
    return False


uncovered = [clause_of(k) for k in diff if not covered(k)]
ra = {r['id']: r for r in a['root_items']}
rb = {r['id']: r for r in b['root_items']}
root_changed = sorted(i for i in ra if ra[i] != rb.get(i))
root_new = sorted(i for i in rb if i not in ra)
pend = []


def walk(o, p=''):
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, p + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, '%s[%d]' % (p, i))
    elif isinstance(o, str) and 'PENDING' in o:
        pend.append((p, re.findall(r'PENDING[A-Z_]*', o)))


walk(b)
vb = Path(addp).read_bytes()
starts = [m.start() for m in re.finditer(rb'(?m)^## ', vb)]
sec = {}
for i, s in enumerate(starts):
    e = starts[i + 1] if i + 1 < len(starts) else len(vb)
    m = re.match(rb'## (A\d+):', vb[s:s + 12])
    if m:
        sec[m.group(1).decode()] = hashlib.sha256(vb[s:e]).hexdigest()
rows = b['entries_after_A81']['rows']
row_ok = all(sec.get(r['entry']) == r['section_sha256'] for r in rows)
out = {'r4': {'path': r4p, 'sha256': hashlib.sha256(Path(r4p).read_bytes()).hexdigest()},
       'r5': {'path': r5p, 'sha256': hashlib.sha256(Path(r5p).read_bytes()).hexdigest()},
       'differing_leaves': len(diff), 'logged_clauses': len(logged), 'uncovered_differing_leaves': uncovered,
       'root_items_changed_by_id': root_changed, 'root_items_new': root_new,
       'pending_markers': [{'path': p, 'markers': sorted(set(m))} for p, m in pend],
       'entry_rows': len(rows), 'entry_rows_rehash_ok': row_ok,
       'entries_covered': [r['entry'] for r in rows], 'addendum_copy_sha256': hashlib.sha256(vb).hexdigest(),
       'verdict': 'PASS' if (not uncovered and root_changed == ['RI-24', 'RI-27'] and row_ok) else 'FAIL'}
with open(outp, 'x') as f:
    f.write(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
print(out['verdict'], '| differing leaves', len(diff), '| uncovered', uncovered[:10], '| root changed', root_changed, '| new', root_new,
      '| rows', len(rows), row_ok)
for x in out['pending_markers']:
    print('  PENDING at', x['path'][:110], x['markers'])
print('out', outp, hashlib.sha256(Path(outp).read_bytes()).hexdigest())
