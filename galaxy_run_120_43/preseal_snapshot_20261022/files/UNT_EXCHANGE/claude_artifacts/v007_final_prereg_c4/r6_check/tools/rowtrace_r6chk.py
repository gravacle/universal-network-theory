# Claude4 r6 refute helper (r6_check), check (2) continued: the new entry-table rows A102-A106 against my own leaf diff.
#  (a) every clause a "revised here" row names (JSON path or SEAL_CHECKLIST_R6 step) really differs between r5 and r6;
#  (b) every DELTA row whose trace cites one of A102-A106 (A106.1/.2/.3 count as A106) is named by that entry's row
#      (the row may name the clause itself or a parent of it);
#  (c) every clause the rows name is covered by some DELTA row (no row names a clause the delta does not record).
# Read-only; writes OUT.json by exclusive create.
# usage: python3 -I -B rowtrace_r6chk.py R5.json R6.json DELTA_R5_R6.md CHECKLIST_R5.md CHECKLIST_R6.md OUT.json
import json, re, sys
sys.path.insert(0, '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r6_check/tools')
import leafdiff_r6chk as L   # my own flattener, DELTA parser and checklist parser (same folder)

NEW = ('A102', 'A103', 'A104', 'A105', 'A106')


def norm(c):
    m = re.fullmatch(r'root_items\.(RI-\d+)', c)
    return 'root_items[%s]' % m.group(1) if m else c


def main():
    r5p, r6p, deltap, c5p, c6p, outp = sys.argv[1:7]
    d5, _ = L.load(r5p)
    d6, _ = L.load(r6p)
    f5, f6 = {}, {}
    L.flatten(d5, '', f5)
    L.flatten(d6, '', f6)
    diff = sorted(set(k for k in set(f5) | set(f6) if f5.get(k, '<absent>') != f6.get(k, '<absent>')))
    k5 = L.checklist_steps(open(c5p, 'rb').read().decode('utf-8'))
    k6 = L.checklist_steps(open(c6p, 'rb').read().decode('utf-8'))
    ck_changed = set(k for k in set(k5) | set(k6) if k5.get(k) != k6.get(k))
    rows = L.parse_delta(open(deltap, 'rb').read().decode('utf-8'))
    erows = {r['entry']: r for r in d6['entries_after_A81']['rows']}
    out = {'a_named_clause_changed': {}, 'b_delta_trace_named_by_row': [], 'c_named_clause_has_delta_row': {}}
    for e in NEW:
        r = erows[e]
        res = {}
        for c in r['revised_clauses']:
            if c.startswith('SEAL_CHECKLIST_R6 '):
                steps = [s.strip() for s in c.split(' ', 1)[1].split(',')]
                res[c] = {s: (s in ck_changed) for s in steps}
            else:
                p = norm(c)
                res[c] = any(L.covers(p, k) for k in diff)
        out['a_named_clause_changed'][e] = res
    # (b)
    for dr in rows:
        cited = set()
        for t in dr['trace']:
            m = re.match(r'^(A10[2-6])(\.\d+)?$', t)
            if m:
                cited.add(m.group(1))
        for e in sorted(cited):
            named = erows[e]['revised_clauses']
            if dr['clause'].startswith('SEAL_CHECKLIST_R6 '):
                step = dr['clause'].split(' ', 1)[1]
                ok = any(c.startswith('SEAL_CHECKLIST_R6 ') and step in [s.strip() for s in c.split(' ', 1)[1].split(',')] for c in named)
            elif dr['clause'] == 'root_items (order)':
                ok = None     # ordering only; no row names it
            else:
                p = norm(dr['clause'])
                ok = any(p == norm(c) or L.covers(norm(c), p) for c in named if not c.startswith('SEAL_CHECKLIST_R6 '))
            out['b_delta_trace_named_by_row'].append({'delta_row': dr['n'], 'clause': dr['clause'], 'entry': e, 'named_by_row': ok})
    # (c)
    for e in NEW:
        res = {}
        for c in erows[e]['revised_clauses']:
            if c.startswith('SEAL_CHECKLIST_R6 '):
                steps = [s.strip() for s in c.split(' ', 1)[1].split(',')]
                res[c] = {s: any(dr['clause'] == 'SEAL_CHECKLIST_R6 ' + s and any(t.startswith(e) for t in dr['trace']) for dr in rows) for s in steps}
            else:
                p = norm(c)
                res[c] = [dr['n'] for dr in rows if (norm(dr['clause']) == p or L.covers(p, norm(dr['clause'])))
                          and any(t == e or t.startswith(e + '.') for t in dr['trace'])]
        out['c_named_clause_has_delta_row'][e] = res
    fails_a = [(e, c) for e, m in out['a_named_clause_changed'].items() for c, v in m.items() if (v is False or (isinstance(v, dict) and not all(v.values())))]
    fails_b = [x for x in out['b_delta_trace_named_by_row'] if x['named_by_row'] is False]
    fails_c = [(e, c) for e, m in out['c_named_clause_has_delta_row'].items() for c, v in m.items() if (v == [] or (isinstance(v, dict) and not all(v.values())))]
    out['summary'] = {'a_fail': fails_a, 'b_fail': fails_b, 'c_fail': fails_c,
                      'b_checked': len(out['b_delta_trace_named_by_row'])}
    with open(outp, 'x') as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(json.dumps(out['summary'], indent=1))


if __name__ == '__main__':
    main()
