# diff_r4_r5_r5chk.py -- independent leaf diff of prereg r4 vs r5 (r5_check helper, Claude4).
# usage: python3 -I -B diff_r4_r5_r5chk.py R4.json R5.json OUT.json OUT_TEXT.txt
# Reads only the two named JSON files. Writes two new files by exclusive create.
import json, sys, hashlib

def strict_load(p):
    def hook(pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                raise ValueError('DUPLICATE_KEY %r in %s' % (k, p))
            d[k] = v
        return d
    b = open(p, 'rb').read()
    return json.loads(b.decode('utf-8'), object_pairs_hook=hook), hashlib.sha256(b).hexdigest()

def keyed(doc):
    # root_items keyed by id (positional order is not a rule); everything else as is.
    out = dict(doc)
    if isinstance(doc.get('root_items'), list):
        ids = [x.get('id') for x in doc['root_items']]
        assert len(ids) == len(set(ids)), 'duplicate root item id'
        out['root_items'] = {x['id']: x for x in doc['root_items']}
    return out

def flatten(x, path=()):
    if isinstance(x, dict):
        if not x:
            yield path, {}
        for k, v in x.items():
            yield from flatten(v, path + (str(k),))
    elif isinstance(x, list):
        if not x:
            yield path, []
        for i, v in enumerate(x):
            yield from flatten(v, path + ('[%d]' % i,))
    else:
        yield path, x

def main():
    r4p, r5p, outp, txtp = sys.argv[1:5]
    r4, s4 = strict_load(r4p)
    r5, s5 = strict_load(r5p)
    f4 = dict(flatten(keyed(r4)))
    f5 = dict(flatten(keyed(r5)))
    added = sorted(p for p in f5 if p not in f4)
    removed = sorted(p for p in f4 if p not in f5)
    changed = sorted(p for p in f4 if p in f5 and (f4[p] != f5[p] or type(f4[p]) is not type(f5[p])))
    res = {
        'schema': 'R5CHK_DIFF_R4_R5_V001',
        'r4': {'path': r4p, 'sha256': s4, 'leaves': len(f4)},
        'r5': {'path': r5p, 'sha256': s5, 'leaves': len(f5)},
        'counts': {'added': len(added), 'removed': len(removed), 'changed': len(changed),
                   'total_differing': len(added) + len(removed) + len(changed)},
        'added': ['/'.join(p) for p in added],
        'removed': ['/'.join(p) for p in removed],
        'changed': ['/'.join(p) for p in changed],
    }
    with open(outp, 'x') as f:
        json.dump(res, f, indent=1, sort_keys=True)
    # Text: per second-level clause, the old and new text of each differing leaf.
    lines = []
    def show(v):
        s = json.dumps(v, ensure_ascii=False)
        return s
    groups = {}
    for kind, plist in (('ADDED', added), ('REMOVED', removed), ('CHANGED', changed)):
        for p in plist:
            g = '/'.join(p[:2]) if len(p) > 1 else p[0]
            groups.setdefault(g, []).append((kind, p))
    for g in sorted(groups):
        lines.append('=' * 3 + ' CLAUSE ' + g + ' (' + str(len(groups[g])) + ' leaves)')
        for kind, p in groups[g]:
            lines.append('  [' + kind + '] ' + '/'.join(p))
            if kind != 'ADDED':
                lines.append('     R4: ' + show(f4[p]))
            if kind != 'REMOVED':
                lines.append('     R5: ' + show(f5[p]))
    with open(txtp, 'x') as f:
        f.write('\n'.join(lines) + '\n')
    print(json.dumps(res['counts']), 'r4', s4[:8], 'r5', s5[:8])

main()
