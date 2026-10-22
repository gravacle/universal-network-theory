# Claude4 r6 refute helper (r6_check), check (2): my own byte-level extractor of the V005 entry sections, applied to the r6
# byte copy and to the live V005 file, both of which must hash to the closed sha; every r6 entries_after_A81 row re-extracted.
# Read-only on its inputs; writes OUT.json by exclusive create.
# usage: python3 -I -B entries_r6chk.py CLOSED_SHA R6_COPY LIVE_V005 R5_COPY R5.json R6.json ENTRY_TABLE_R6.md OUT.json
# Extractor (independent of r6's generator, its verifier and seal tool 1): walk the bytes line by line (a line ends after b"\n"),
# keep each line's start offset; a "section start" is a line whose bytes begin b"## "; an entry line is a section start that
# matches b"## A<digits>:"; the entry section = bytes from its line start up to the next section start (or EOF). This is r5's
# section_rule as written in the prereg text.
import collections, hashlib, json, re, sys


def lines_with_offsets(raw):
    out = []
    i = 0
    n = len(raw)
    while i < n:
        j = raw.find(b'\n', i)
        e = n if j < 0 else j + 1
        out.append((i, raw[i:e]))
        i = e
    return out


def extract(raw):
    ls = lines_with_offsets(raw)
    starts = [(off, ln) for off, ln in ls if ln.startswith(b'## ')]
    secs = []
    for k, (off, ln) in enumerate(starts):
        end = starts[k + 1][0] if k + 1 < len(starts) else len(raw)
        m = re.match(rb'## A([0-9]+):', ln)
        secs.append({'off': off, 'end': end, 'entry': ('A%d' % int(m.group(1))) if m else None,
                     'heading': ln.rstrip(b'\n').decode('utf-8'), 'bytes': raw[off:end]})
    pre_end = starts[0][0] if starts else len(raw)
    return secs, raw[:pre_end]


def by_entry(secs):
    d = collections.defaultdict(list)
    for s in secs:
        if s['entry']:
            d[s['entry']].append(s)
    return d


def strict(path):
    def pairs(p):
        o = {}
        for k, v in p:
            if k in o:
                raise ValueError('duplicate key %r' % k)
            o[k] = v
        return o
    raw = open(path, 'rb').read()
    return json.loads(raw, object_pairs_hook=pairs), hashlib.sha256(raw).hexdigest()


def main():
    closed, copy6, live, copy5, r5p, r6p, tablep, outp = sys.argv[1:9]
    res = {'closed_sha256_expected': closed}
    raws = {}
    for tag, p in (('r6_copy', copy6), ('live_v005', live), ('r5_copy', copy5)):
        raw = open(p, 'rb').read()
        raws[tag] = raw
        res[tag] = {'path': p, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
    res['r6_copy_equals_closed'] = res['r6_copy']['sha256'] == closed
    res['live_equals_closed'] = res['live_v005']['sha256'] == closed
    res['r6_copy_bytes_equal_live'] = raws['r6_copy'] == raws['live_v005']
    if not (res['r6_copy_equals_closed'] and res['live_equals_closed']):
        res['STOP'] = 'a byte source differs from the closed sha; no row check is meaningful'
        with open(outp, 'x') as fh:
            json.dump(res, fh, indent=1, sort_keys=True)
        print(json.dumps(res, indent=1))
        sys.exit(2)
    d5, s5 = strict(r5p)
    d6, s6 = strict(r6p)
    res['r5_json_sha256'] = s5
    res['r6_json_sha256'] = s6
    rows6 = d6['entries_after_A81']['rows']
    rows5 = d5['entries_after_A81']['rows']
    per_source = {}
    for tag in ('r6_copy', 'live_v005'):
        secs, pre = extract(raws[tag])
        be = by_entry(secs)
        nums = sorted(int(e[1:]) for e in be)
        dup = sorted(e for e, v in be.items() if len(v) > 1)
        rowres = []
        for r in rows6:
            hit = be.get(r['entry'], [])
            if len(hit) != 1:
                rowres.append({'entry': r['entry'], 'ok': False, 'why': 'present %d times' % len(hit)})
                continue
            s = hit[0]
            got = hashlib.sha256(s['bytes']).hexdigest()
            ok = (got == r['section_sha256'] and len(s['bytes']) == r['section_bytes'] and s['heading'] == r['heading'])
            rowres.append({'entry': r['entry'], 'ok': ok, 'sha256': got, 'bytes': len(s['bytes']), 'heading_equal': s['heading'] == r['heading']})
        per_source[tag] = {
            'entries_found': len(be), 'min': 'A%d' % nums[0], 'max': 'A%d' % nums[-1],
            'duplicates': dup, 'non_entry_section_starts': [s['heading'] for s in secs if not s['entry']],
            'entries_ge_A82': ['A%d' % n for n in nums if n >= 82],
            'rows_ok': sum(1 for x in rowres if x['ok']), 'rows_total': len(rowres), 'rows': rowres,
            'missing_numbers_A47_max': ['A%d' % n for n in range(47, nums[-1] + 1) if n not in nums],
            'physical_order': [s['entry'] for s in secs if s['entry']],
            'preamble_sha256': hashlib.sha256(pre).hexdigest(),
        }
    res['per_source'] = per_source
    tbl = set(r['entry'] for r in rows6)
    res['table_entries'] = sorted(tbl, key=lambda e: int(e[1:]))
    res['table_equals_every_V005_entry_ge_A82'] = sorted(tbl, key=lambda e: int(e[1:])) == per_source['r6_copy']['entries_ge_A82']
    res['A106_is_the_max_entry'] = per_source['r6_copy']['max'] == 'A106'
    # r5 copy vs r6 copy: A47-A101 sections and preamble byte-equal; exactly which entries were added and where
    s5x, pre5 = extract(raws['r5_copy'])
    s6x, pre6 = extract(raws['r6_copy'])
    b5, b6 = by_entry(s5x), by_entry(s6x)
    res['r5_copy_vs_r6_copy'] = {
        'preamble_equal': pre5 == pre6,
        'entries_only_in_r6_copy': sorted(set(b6) - set(b5), key=lambda e: int(e[1:])),
        'entries_only_in_r5_copy': sorted(set(b5) - set(b6), key=lambda e: int(e[1:])),
        'common_entries_bytes_differ': sorted((e for e in set(b5) & set(b6) if b5[e][0]['bytes'] != b6[e][0]['bytes']), key=lambda e: int(e[1:])),
        'common_entries': len(set(b5) & set(b6)),
    }
    order6 = [s['entry'] for s in s6x]
    order5 = [s['entry'] for s in s5x]
    stripped = [e for e in order6 if e in set(b5)]
    res['r5_copy_vs_r6_copy']['r6_order_minus_new_equals_r5_order'] = stripped == order5
    new = res['r5_copy_vs_r6_copy']['entries_only_in_r6_copy']
    if new:
        idx = [order6.index(e) for e in new]
        res['r5_copy_vs_r6_copy']['new_entries_physical_block'] = [order6[i] for i in range(min(idx), max(idx) + 1)]
        res['r5_copy_vs_r6_copy']['entry_after_new_block'] = order6[max(idx) + 1] if max(idx) + 1 < len(order6) else None
        res['r5_copy_vs_r6_copy']['entry_before_new_block'] = order6[min(idx) - 1] if min(idx) > 0 else None
        # splice check: the r6 copy equals the r5 copy with the new block's bytes inserted at one offset
        first = b6[order6[min(idx)]][0]['off']
        last_end = b6[order6[max(idx)]][0]['end']
        block = raws['r6_copy'][first:last_end]
        res['r5_copy_vs_r6_copy']['splice_equal'] = raws['r6_copy'][:first] + raws['r6_copy'][last_end:] == raws['r5_copy']
        res['r5_copy_vs_r6_copy']['new_block_bytes'] = len(block)
    # rows A82-A101: r5 row dicts equal r6 row dicts
    r5map = {r['entry']: r for r in rows5}
    r6map = {r['entry']: r for r in rows6}
    res['r5_rows_unchanged_in_r6'] = {e: (r5map[e] == r6map.get(e)) for e in r5map}
    res['r5_rows_all_unchanged'] = all(res['r5_rows_unchanged_in_r6'].values())
    res['new_rows'] = sorted(set(r6map) - set(r5map), key=lambda e: int(e[1:]))
    res['new_row_decisions'] = {e: r6map[e]['decision'] for e in res['new_rows']}
    res['decision_values'] = sorted(set(r['decision'] for r in rows6))
    # ENTRY_TABLE_R6.md rows vs the JSON rows
    md = open(tablep, 'rb').read().decode('utf-8')
    mdrows = {}
    for ln in md.splitlines():
        m = re.match(r'^\| (A\d+) \| (revised here|no change) \| `([0-9a-f]{64})` \| (.*) \|$', ln)
        if m:
            mdrows[m.group(1)] = (m.group(2), m.group(3), m.group(4))
    mdchk = {}
    for e, r in r6map.items():
        got = mdrows.get(e)
        if not got:
            mdchk[e] = 'missing in md'
            continue
        dec_ok = got[0] == {'REVISED_HERE': 'revised here', 'NO_CHANGE': 'no change'}[r['decision']]
        sha_ok = got[1] == r['section_sha256']
        if r['decision'] == 'REVISED_HERE':
            text_ok = got[2] == '%s Clauses: %s' % (r['scope'], ', '.join('`%s`' % c for c in r['revised_clauses']))
        else:
            text_ok = got[2] == r.get('reason')
        mdchk[e] = 'ok' if (dec_ok and sha_ok and text_ok) else 'DIFF dec=%s sha=%s text=%s' % (dec_ok, sha_ok, text_ok)
    res['entry_table_md_vs_json'] = mdchk
    res['entry_table_md_rows'] = len(mdrows)
    with open(outp, 'x') as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
    summ = {k: res[k] for k in ('r6_copy_equals_closed', 'live_equals_closed', 'r6_copy_bytes_equal_live', 'table_equals_every_V005_entry_ge_A82',
                                'A106_is_the_max_entry', 'r5_rows_all_unchanged', 'new_rows', 'new_row_decisions', 'decision_values')}
    summ['rows_ok'] = {t: '%d/%d' % (v['rows_ok'], v['rows_total']) for t, v in per_source.items()}
    summ['dups'] = {t: v['duplicates'] for t, v in per_source.items()}
    summ['non_entry_section_starts'] = per_source['r6_copy']['non_entry_section_starts']
    summ['missing_numbers'] = per_source['r6_copy']['missing_numbers_A47_max']
    summ['r5_vs_r6_copy'] = {k: v for k, v in res['r5_copy_vs_r6_copy'].items()}
    summ['md'] = sorted(set(mdchk.values())), res['entry_table_md_rows']
    print(json.dumps(summ, indent=1))


if __name__ == '__main__':
    main()
