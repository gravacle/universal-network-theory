# Claude4 r6 refute helper (r6_check), check (1): my own leaf diff of prereg r5 -> r6, mapped to the DELTA_R5_R6 rows.
# Read-only on its inputs; writes OUT.json and OUT.txt by exclusive create.
# usage: python3 -I -B leafdiff_r6chk.py R5.json R6.json DELTA_R5_R6.md CHECKLIST_R5.md CHECKLIST_R6.md OUT.json OUT.txt
# Independent of the builder's verifier: own strict loader, own flattener (root_items keyed by id, entries_after_A81.rows keyed
# by entry, every other list by position), own DELTA parser, own checklist parser.
import collections, hashlib, json, re, sys


class Dup(ValueError):
    pass


def _pairs(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise Dup('duplicate key %r' % k)
        out[k] = v
    return out


def _const(c):
    raise ValueError('non-finite constant %s' % c)


def load(path):
    raw = open(path, 'rb').read()
    return json.loads(raw, object_pairs_hook=_pairs, parse_constant=_const), hashlib.sha256(raw).hexdigest()


def flatten(o, path, out):
    if isinstance(o, dict):
        if not o:
            out[path] = '{}'
        for k, v in o.items():
            flatten(v, (path + '.' + k) if path else k, out)
    elif isinstance(o, list):
        if not o:
            out[path] = '[]'
        if path == 'root_items':
            ids = [r.get('id') for r in o]
            assert len(ids) == len(set(ids)), 'duplicate root item id'
            for r in o:
                flatten(r, '%s[%s]' % (path, r['id']), out)
        elif path == 'entries_after_A81.rows':
            ids = [r.get('entry') for r in o]
            assert len(ids) == len(set(ids)), 'duplicate entry row'
            for r in o:
                flatten(r, '%s[%s]' % (path, r['entry']), out)
        else:
            for i, v in enumerate(o):
                flatten(v, '%s[%d]' % (path, i), out)
    else:
        out[path] = o


def get(doc, path):
    """value at a normalized clause path (dots, [i], root_items[RI-n], entries_after_A81.rows[An])"""
    cur = doc
    for tok in re.findall(r'[^.\[\]]+|\[[^\]]+\]', path):
        if tok.startswith('['):
            key = tok[1:-1]
            if isinstance(cur, list) and key.isdigit():
                cur = cur[int(key)] if int(key) < len(cur) else None
            elif isinstance(cur, list):
                hit = [r for r in cur if isinstance(r, dict) and (r.get('id') == key or r.get('entry') == key)]
                cur = hit[0] if hit else None
            else:
                return None
        else:
            if not isinstance(cur, dict) or tok not in cur:
                return None
            cur = cur[tok]
        if cur is None:
            return None
    return cur


def parse_delta(md):
    rows = []
    for line in md.splitlines():
        m = re.match(r'^\| (\d+) \| (\d+) \| `([^`]+)` \| ([^|]*) \| ([^|]*) \| ([^|]*) \| (.*) \|$', line)
        if m:
            rows.append({'n': int(m.group(1)), 'item': int(m.group(2)), 'clause': m.group(3).strip(), 'kind': m.group(4).strip(),
                         'added_sources': [s.strip() for s in m.group(5).split(';') if s.strip()],
                         'trace': [s.strip() for s in m.group(6).split(';') if s.strip()], 'why': m.group(7).strip()})
    return rows


def norm_clause(c):
    m = re.fullmatch(r'root_items\.(RI-\d+)', c)
    if m:
        return 'root_items[%s]' % m.group(1)
    return c


def covers(prefix, leaf):
    return leaf == prefix or leaf.startswith(prefix + '.') or leaf.startswith(prefix + '[')


def parent_of(path):
    m = re.match(r'^(.*)(\.[^.\[\]]+|\[[^\]]+\])$', path)
    return m.group(1) if m else ''


def checklist_steps(md):
    """{key: row line} for SEAL_CHECKLIST tables; keys: HEADER (title + state line), step ids (A1., B2a., C1.), SECTION:<bold>,
    DONE[i] for the 'Already DONE' rows, SUPERSEDED for the row after the SUPERSEDED header"""
    out = collections.OrderedDict()
    lines = md.splitlines()
    head = []
    section = None
    done_i = 0
    for ln in lines:
        if not ln.startswith('|'):
            if ln.strip():
                head.append(ln)
            continue
        if ln.startswith('| step |') or ln.startswith('|---'):
            continue
        cells = ln.split(' | ')
        first = cells[0][2:] if cells[0].startswith('| ') else cells[0]
        mb = re.match(r'^\*\*(.+?)\*\*', first)
        if mb:
            section = mb.group(1)
            out['SECTION:' + section] = ln
            continue
        ms = re.match(r'^((?:A|B|C)\d+a?)\. ', first)
        if ms:
            key = ms.group(1)
        elif section and section.startswith('SUPERSEDED'):
            key = 'SUPERSEDED'
        elif section and section.startswith('Already DONE'):
            key = 'DONE[%d]' % done_i
            done_i += 1
        else:
            key = 'OTHER:' + first[:40]
        assert key not in out, 'duplicate checklist key %s' % key
        out[key] = ln
    out['HEADER'] = '\n'.join(head)
    return out


def main():
    r5p, r6p, deltap, c5p, c6p, outj, outt = sys.argv[1:8]
    d5, s5 = load(r5p)
    d6, s6 = load(r6p)
    delta_raw = open(deltap, 'rb').read()
    rows = parse_delta(delta_raw.decode('utf-8'))
    f5, f6 = {}, {}
    flatten(d5, '', f5)
    flatten(d6, '', f6)
    added = sorted(set(f6) - set(f5))
    removed = sorted(set(f5) - set(f6))
    changed = sorted(k for k in set(f5) & set(f6) if f5[k] != f6[k] or type(f5[k]) is not type(f6[k]))
    diff = [(k, 'added') for k in added] + [(k, 'removed') for k in removed] + [(k, 'changed') for k in changed]
    diff.sort()
    json_rows = [r for r in rows if not r['clause'].startswith('SEAL_CHECKLIST_R6') and r['clause'] != 'root_items (order)']
    prefixes = {r['n']: norm_clause(r['clause']) for r in json_rows}
    covered_by = collections.defaultdict(list)
    uncovered = []
    sources_leaf = []
    for k, kind in diff:
        hit = [n for n, p in prefixes.items() if covers(p, k)]
        if not hit:
            # a leaf of a parent clause's sources list: covered by any row whose clause is that parent or one of its children
            m = re.match(r'^(.*)\.sources(\[\d+\])?$', k)
            if m:
                par = m.group(1)
                hit = [n for n, p in prefixes.items() if p == par or parent_of(p) == par]
                if hit:
                    sources_leaf.append(k)
        if hit:
            for n in hit:
                covered_by[n].append(k)
        else:
            uncovered.append((k, kind))
    vacuous = sorted(n for n in prefixes if not covered_by.get(n))
    # sources lists: actual additions/removals (multiset) vs the DELTA added-sources column
    src_checks = []
    parents = sorted(set(re.match(r'^(.*)\.sources', k).group(1) for k, _ in diff if re.match(r'^(.*)\.sources(\[\d+\])?$', k)))
    for par in parents:
        a5 = get(d5, par + '.sources') or []
        a6 = get(d6, par + '.sources') or []
        c5, c6 = collections.Counter(a5), collections.Counter(a6)
        act_add = sorted((c6 - c5).elements())
        act_rem = sorted((c5 - c6).elements())
        decl = []
        for r in json_rows:
            p = prefixes[r['n']]
            if p == par or parent_of(p) == par:
                decl += r['added_sources']
        src_checks.append({'parent': par, 'actual_added': act_add, 'actual_removed': act_rem, 'declared_added': sorted(set(decl)),
                           'equal_as_sets': sorted(set(act_add)) == sorted(set(decl)) and not act_rem,
                           'order_only_change': not act_add and not act_rem})
    # root items: the same ids; order rule (open first, then by id)
    ids5 = [r['id'] for r in d5['root_items']]
    ids6 = [r['id'] for r in d6['root_items']]

    def keyf(r):
        return (0 if r.get('status', '').startswith('OPEN') else 1, int(r['id'].split('-')[1]))
    order_ok5 = ids5 == [r['id'] for r in sorted(d5['root_items'], key=keyf)]
    order_ok6 = ids6 == [r['id'] for r in sorted(d6['root_items'], key=keyf)]
    # checklist
    k5 = checklist_steps(open(c5p, 'rb').read().decode('utf-8'))
    k6 = checklist_steps(open(c6p, 'rb').read().decode('utf-8'))
    ck_changed = sorted(k for k in set(k5) | set(k6) if k5.get(k) != k6.get(k))
    ck_rows = [r for r in rows if r['clause'].startswith('SEAL_CHECKLIST_R6')]
    ck_declared = sorted(r['clause'].split(' ', 1)[1] for r in ck_rows)
    ck_declared_keys = sorted('HEADER' if x == 'header' else x for x in ck_declared)
    res = {
        'r5': {'path': r5p, 'sha256': s5}, 'r6': {'path': r6p, 'sha256': s6},
        'delta': {'path': deltap, 'sha256': hashlib.sha256(delta_raw).hexdigest(), 'rows': len(rows)},
        'leaves_r5': len(f5), 'leaves_r6': len(f6),
        'differing_leaves': len(diff), 'added': len(added), 'removed': len(removed), 'changed': len(changed),
        'uncovered_leaves': uncovered,
        'leaves_covered_only_as_parent_sources': sources_leaf,
        'vacuous_rows': vacuous,
        'rows_leaf_counts': {str(n): len(covered_by.get(n, [])) for n in sorted(prefixes)},
        'multi_row_leaves': sorted(k for k, _ in diff if sum(1 for n in prefixes if k in covered_by.get(n, [])) > 1),
        'sources_lists': src_checks,
        'root_items': {'same_id_set': sorted(ids5) == sorted(ids6), 'order_changed': ids5 != ids6,
                       'order_rule_holds_r5': order_ok5, 'order_rule_holds_r6': order_ok6,
                       'order_row_present': any(r['clause'] == 'root_items (order)' for r in rows)},
        'checklist': {'changed_keys': ck_changed, 'declared_rows': ck_declared_keys,
                      'equal': ck_changed == ck_declared_keys,
                      'keys_r5': list(k5), 'keys_r6': list(k6)},
        'top_level_keys_equal': list(d5) == list(d6),
    }
    with open(outj, 'x') as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
    with open(outt, 'x') as fh:
        for r in rows:
            fh.write('=' * 100 + '\n')
            fh.write('ROW %d item %d clause %s kind %s\n  added sources: %s\n  trace: %s\n  why: %s\n' % (
                r['n'], r['item'], r['clause'], r['kind'], r['added_sources'], r['trace'], r['why']))
            if r['clause'].startswith('SEAL_CHECKLIST_R6'):
                key = r['clause'].split(' ', 1)[1]
                key = 'HEADER' if key == 'header' else key
                fh.write('--- r5:\n%s\n--- r6:\n%s\n' % (k5.get(key), k6.get(key)))
                continue
            if r['clause'] == 'root_items (order)':
                fh.write('--- r5 order: %s\n--- r6 order: %s\n' % (ids5, ids6))
                continue
            p = norm_clause(r['clause'])
            fh.write('--- r5 value:\n%s\n--- r6 value:\n%s\n' % (json.dumps(get(d5, p), indent=1, ensure_ascii=False),
                                                              json.dumps(get(d6, p), indent=1, ensure_ascii=False)))
            par = parent_of(p)
            if par and isinstance(get(d6, par), dict) and 'sources' in get(d6, par) and not p.endswith('sources'):
                fh.write('--- parent %s.sources r5: %s\n--- parent sources r6: %s\n' % (par, get(d5, par + '.sources'), get(d6, par + '.sources')))
        fh.write('=' * 100 + '\nUNCOVERED LEAVES\n')
        for k, kind in uncovered:
            fh.write('%s %s\n  r5: %r\n  r6: %r\n' % (kind, k, f5.get(k), f6.get(k)))
    print(json.dumps({k: res[k] for k in ('differing_leaves', 'added', 'removed', 'changed', 'vacuous_rows', 'top_level_keys_equal')}))
    print('uncovered', len(uncovered), 'sources-only leaves', len(sources_leaf))
    print('checklist equal', res['checklist']['equal'], res['checklist']['changed_keys'])
    print('root items', res['root_items'])
    for s in src_checks:
        print('sources', s['parent'], 'eq' if s['equal_as_sets'] else 'DIFF', 'added', s['actual_added'], 'removed', s['actual_removed'], 'declared', s['declared_added'])


if __name__ == '__main__':
    main()
