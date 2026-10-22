# Claude4 (dispatches 0585, 0606 and 0619/A98.2) mutation test for the target-free check v003 (tools-builder revision).
# Every case is a mutated copy of a built r3 bundle (or of the V005 bytes) that must make the check FAIL, with the expected
# checks among the new failures and, where given, the injected token named in their details; the unmutated bundle must PASS
# both verdicts. Groups: the cases of the earlier tests; the 42 adversarial cases replayed by the round-2 closure lens (round-1
# lens B's 38 plus C12 and E01-E03); the round-2 target-free lens's evasion, unit, symbol, stripping, bundle-file and pin
# cases; the T5/T7 probe X1-X8 on a V005 byte copy; the entry-table cases (suffix heading, omission, duplicate row, order,
# cited-but-unpinned, the A65 tail or its unmarked pin); and the provenance rules. Hook probes then exercise the shared hook.
# Case parameters (entries, provenance keys, rows, anchors) are read from the built bundle, so the test runs on the fixture and
# on the real candidate alike; a case whose anchor does not exist in the bundle is listed under not_applicable, never passed.
# Sentinels are non-physical (987.6, 9876, 1.48e9, 987654.321) or listed stand-ins (778, 93.6) with the fake id NGC3198-Q99.
# Writes go only under --work (a new folder): work/case_NNN/bundle/ and, for V005 or V006 cases, work/case_NNN/V00n_MUT.md.
# Fix stage (refute RF-B1/TF-B1, TF-S1, TF-S2, TF-S3): the V006 cases replace the old "a V006 exists" case; controls that must
# PASS both verdicts (a seal entry appended to V006); the refuters' evasion classes for terms, numbers, units, symbols and the
# JSON notes; hook probes for the long-s spelling and the symlink-then-'..' channel, run against an in-process decoy term only.
# usage: python3 -I -B test_check_target_free_c4v003.py --built R3DIR --work NEW_SCRATCH_DIR [--v005 V005_COPY.md]
#        [--v006 V006_COPY.md]
import argparse, hashlib, json, os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_target_free_c4v003 as T

SLOTS = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json'
SLOTS_SHA = 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'
NODES = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json'
NODES_SHA = 'ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d'
P, M, R, N, E, I = T.PREREG, T.CSM, T.ROOT, T.PROV, T.ETAB, T.INDEX
E6 = T.ETAB6
BUNDLE = (P, M, R, N, E, E6, I)
DECOY = 'zqdecoys'                 # an in-process decoy deny term for the live hook probes (never a real deny term)
ANCHOR = '## 0. Invariants'
Q = 'NGC3198-Q99'
T1, T2, T3, T4, T5, T6, T7 = ('T1_FORBIDDEN_TERMS', 'T2_NO_VELOCITY_UNIT', 'T3_NO_TARGET_SYMBOL_VALUE', 'T4_NUMBER_PROVENANCE',
                              'T5_SOURCES_TARGET_FREE_AND_PINNED', 'T6_CLAUSE_TAGS_MAPPED', 'T7_V005_CURRENCY')
ZW, UMINUS = '​', '−'


class NotApplicable(Exception):
    pass


def rd(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def wr(p, t):
    with open(p, 'w', encoding='utf-8') as f:
        f.write(t)


def need(cond, why):
    if not cond:
        raise NotApplicable(why)


# ---------------------------------------------------------------------------------------------------- bundle mutations
def ins(s, name=P):
    def f(d):
        p = os.path.join(d, name)
        t = rd(p)
        t2 = t.replace(ANCHOR, s + '\n\n' + ANCHOR, 1) if (name == P and ANCHOR in t) else t + '\n' + s + '\n'
        assert t2 != t
        wr(p, t2)
    return f


def app(name, s):
    def f(d):
        p = os.path.join(d, name)
        wr(p, rd(p) + '\n' + s + '\n')
    return f


def sub(name, old, new, count=1):
    def f(d):
        p = os.path.join(d, name)
        t = rd(p)
        assert old in t, (name, old[:80])
        wr(p, t.replace(old, new, count))
    return f


def prov(fn):
    def f(d):
        p = os.path.join(d, N)
        doc = json.loads(rd(p))
        fn(doc)
        wr(p, json.dumps(doc, indent=1, ensure_ascii=False) + '\n')
    return f


def etab(fn, name=E):
    def f(d):
        p = os.path.join(d, name)
        doc = json.loads(rd(p))
        fn(doc)
        wr(p, json.dumps(doc, indent=1, ensure_ascii=False) + '\n')
    return f


def v6_append(s):
    def g(v):
        return v + s
    return g


def v6_append_in_first(s):
    """Insert a line inside the first V006 section, before the second heading (or at EOF)."""
    def g(v):
        i = v.index('\n## ') + 1
        j = v.find('\n## ', i)
        j = len(v) if j < 0 else j + 1
        return v[:j] + s + v[j:]
    return g


def v6_sub(old, new):
    def g(v):
        assert v.count(old) == 1, old
        return v.replace(old, new, 1)
    return g


def v6_insert_heading(h):
    def g(v):
        k = v.index('\n## ', v.index('\n## ') + 1) if v.count('\n## ') > 1 else len(v)
        return v[:k + 1] + h + '\n\nSynthetic fix-stage probe entry (not a root entry; never published).\n\n' + v[k + 1:]
    return g


def both(*fs):
    def f(d):
        for g in fs:
            g(d)
    return f


def newfile(name, text):
    def f(d):
        with open(os.path.join(d, name), 'x', encoding='utf-8') as g:
            g.write(text)
    return f


def row_match(t, entry, ncells=6):
    """The rendered row of an entry with ncells cells (6: entry table; 4: legacy pin table), or None."""
    for m in re.finditer(r'^\| %s \| [^\n]*$' % re.escape(entry), t, re.M):
        c = T.split_cells(m.group(0))
        if c is not None and len(c) == ncells:
            return m
    return None


def join_cells(cells):
    return '| ' + ' | '.join(T.esc_cell(c) if k in (1, 3) else c for k, c in enumerate(cells)) + ' |'


def edit_row(entry, fn, ncells=6):
    def f(d):
        p = os.path.join(d, P)
        t = rd(p)
        m = row_match(t, entry, ncells)
        assert m, entry
        new = fn(m.group(0))
        assert new != m.group(0)
        wr(p, t[:m.start()] + new + t[m.end():])
    return f


def drop_legacy(entry):
    def f(d):
        p = os.path.join(d, P)
        t = rd(p)
        m = row_match(t, entry, 4)
        if m:
            wr(p, t[:m.start()] + t[m.end() + 1:])
    return f


def flip_sha(line):
    m = re.search(r'`([0-9a-f])([0-9a-f]{63})` \|$', line)
    c = '0' if m.group(1) != '0' else '1'
    return line[:m.start()] + '`' + c + m.group(2) + '` |'


def drop_row(entry):
    def f(d):
        p = os.path.join(d, P)
        t = rd(p)
        m = row_match(t, entry)
        assert m, entry
        wr(p, t[:m.start()] + t[m.end() + 1:])
    return f


def dup_row(entry):
    def f(d):
        p = os.path.join(d, P)
        t = rd(p)
        m = row_match(t, entry)
        wr(p, t[:m.end()] + '\n' + m.group(0) + t[m.end():])
    return f


def swap_rows(e1, e2):
    def f(d):
        p = os.path.join(d, P)
        t = rd(p)
        a, b = row_match(t, e1), row_match(t, e2)
        assert a.end() < b.start()
        wr(p, t[:a.start()] + b.group(0) + t[a.end():b.start()] + a.group(0) + t[b.end():])
    return f


def insert_after_line(line, new):
    def f(d):
        p = os.path.join(d, P)
        t = rd(p)
        i = t.index(line + '\n') + len(line) + 1
        wr(p, t[:i] + new + '\n' + t[i:])
    return f


# ------------------------------------------------------------------------------------------------------ V005 mutations
def section_end(v, heading_prefix):
    i = v.index('\n' + heading_prefix) + 1
    j = v.find('\n## ', i)
    return len(v) if j < 0 else j + 1


def v_append_in(heading_prefix, text):
    def g(v):
        j = section_end(v, heading_prefix)
        return v[:j] + text + v[j:]
    return g


def v_insert_heading(h):
    def g(v):
        k = v.index('\n## ', v.index('\n## ') + 1)          # before the second '## ' heading of the file
        return v[:k + 1] + h + '\n\nSynthetic tools-lens probe entry (not a root entry; never published).\n\n' + v[k + 1:]
    return g


def v_sub(old, new):
    def g(v):
        assert v.count(old) == 1, old
        return v.replace(old, new, 1)
    return g


def natural_sha(v005_text, entry, marker=''):
    heads = T.v005_headings(v005_text)
    idx = [i for i, _, e in heads if e == entry][0]
    main, tail, prob = T.entry_parts(v005_text, idx, marker)
    assert not prob, prob
    return (hashlib.sha256(main.encode('utf-8')).hexdigest(),
            hashlib.sha256(tail.encode('utf-8')).hexdigest() if tail is not None else None)


def to_no_change(entry, v005_text):
    """Re-state a CITED_PINNED entry as NO_CHANGE, honestly (natural-section sha), in the entry-table row and the JSON, and drop
    its legacy pin row if there is one: only the cited-set rule stops it."""
    h, _ = natural_sha(v005_text, entry)

    def row(line):
        cells = T.split_cells(line)
        cells[2], cells[4], cells[5] = 'NO_CHANGE', T.NEXT_HEADING, '`%s`' % h
        return join_cells(cells)

    def js(doc):
        for x in doc['entries']:
            if x['entry'] == entry:
                x['disposition'] = 'NO_CHANGE'
                for k in ('section_sha256', 'end_marker', 'tail_sha256', 'tail_reason'):
                    x.pop(k, None)
    return both(edit_row(entry, row), etab(js), drop_legacy(entry))


def with_marker(entry, marker, v005_text, tail_row=True):
    """Give a CITED_PINNED entry an honest end-marker (main and tail shas from the bytes), with or without its tail row."""
    hm, ht = natural_sha(v005_text, entry, marker)

    def f(d):
        p = os.path.join(d, P)
        t = rd(p)
        m = row_match(t, entry)
        cells = T.split_cells(m.group(0))
        cells[4], cells[5] = '`%s`' % marker, '`%s`' % hm
        new = join_cells(cells)
        old_tail = row_match(t, entry + T.TAIL_SUFFIX)
        if old_tail:
            t = t[:old_tail.start()] + t[old_tail.end() + 1:]
            m = row_match(t, entry)
        tr = ('\n| %s tail | from `%s` to the next heading or end of file | TAIL_PINNED | synthetic | next heading | `%s` |' % (entry, marker, ht)
              if tail_row else '')
        wr(p, t[:m.start()] + new + tr + t[m.end():])
    return f


# -------------------------------------------------------------------------------------------------------------- cases
def cases(ctx):
    v = ctx['v005_text']
    rows, prereg, csm, root, pv = ctx['rows'], ctx['prereg'], ctx['csm'], ctx['root'], ctx['prov']
    etab_rows = [r for r in rows if r['disposition'] in T.DISPOSITIONS]
    cited_pinned = [r['entry'] for r in etab_rows if r['disposition'] == 'CITED_PINNED']
    nc = [r['entry'] for r in etab_rows if r['disposition'] == 'NO_CHANGE']
    cited = ctx['cited']
    marked = [r for r in rows if r['disposition'] == 'CITED_PINNED' and r['marker']]
    has_tail = any(r['disposition'] == 'TAIL_PINNED' for r in rows)
    synth_path = os.path.join(ctx['work'], 'SYNTH_NGC3198_OBSERVED_VELOCITY_TABLE_NOT_DATA.json')   # never created
    numbers = pv.get('numbers', {})
    bycat = {}
    for k, x in numbers.items():
        bycat.setdefault(x.get('category'), []).append(k)
    c = []

    def add(cid, group, make, expect, needle=None, kind='any', setup=None, v6=None):
        """make() returns (bundle_fn, v005_fn); it raises NotApplicable when its anchor is missing in this bundle. v6 mutates
        the V006 text. kind 'pass' marks a control that must PASS both verdicts, with the needle in the T7 details."""
        c.append({'id': cid, 'group': group, 'make': make, 'expect': set(expect), 'needle': needle, 'kind': kind, 'setup': setup,
                  'v6': v6})

    def B(fn):
        return lambda: (fn, None)

    def V(vfn):
        return lambda: (None, vfn)

    def first(lst, why):
        need(lst, why)
        return lst[0]

    g = 'earlier'
    add('velocity_value', g, B(ins('The quoted value at %s is 987654.321 km/s.' % Q)), [T2, T4], '987654.321')
    add('velocity_unit_variant', g, B(ins('A value of 987654 km s⁻¹ appears.')), [T2], 'km s')
    add('velocity_unicode_digits', g, B(ins('A value of ９８７６５４ km/s appears.')), [T2], 'km/s')
    add('velocity_in_root_items', g, B(ins('Root saw 987654.321 km/s.', R)), [T2, T4], '987654.321')
    add('target_symbol_value', g, B(ins('Here v_q = 999999 for %s.' % Q)), [T3, T4], '999999')
    add('target_symbol_vrot', g, B(ins('Note: v_rot ≈ 999999.', M)), [T3, T4], '999999')
    add('forbidden_term', g, B(ins('See the rotmod table.')), [T1], 'rotmod')
    add('forbidden_term_unicode', g, B(ins('See the ＳＰＡＲＣ catalogue.')), [T1], 'sparc')
    add('forbidden_term_zero_width', g, B(ins('See the rot%smod file.' % ZW, M)), [T1], 'rotmod')
    add('forbidden_extension_tsv', g, B(ins('See targets_q99.tsv.', R)), [T1], '.tsv')
    add('unlisted_number', g, B(ins('A quantity of 765432.1 appears here.')), [T4], '765432.1')
    add('number_in_code_span', g, B(ins('The value is `876543.21` here.')), [T4], '876543.21')
    add('long_digit_run', g, B(ins('Run id 98765432 here.')), [T4], '98765432')
    add('unlisted_number_in_map', g, B(ins('A quantity of 765432.1 appears here.', M)), [T4], '765432.1')

    def m_radius():
        k = first(bycat.get('QUERY_RADIUS', []), 'no QUERY_RADIUS entry')
        other = [q for q, r in ctx['rad'].items() if r != k][0]
        return prov(lambda d: d['numbers'][k].update(query_ids=[other])), None
    add('radius_wrong_id', g, m_radius, [T4], 'claimed')

    def m_node():
        k = first(bycat.get('NODE_RADIUS', []), 'no NODE_RADIUS entry')
        return prov(lambda d: d['numbers'][k].update(node_index=(numbers[k].get('node_index', 0) + 1) % 100)), None
    add('node_radius_wrong_index', g, m_node, [T4], 'does not round')
    anykey = sorted(numbers)[0] if numbers else None
    add('bad_category', g, lambda: (need(anykey, 'empty provenance'), (prov(lambda d: d['numbers'][anykey].update(category='FROM_TARGETS')), None))[1],
        [T4], 'FROM_TARGETS')
    add('listed_but_absent', g, B(prov(lambda d: d['numbers'].update({'987.6': {'category': 'MODEL_DIAGNOSTIC', 'uses': ['quoted v_q at %s' % Q]}}))), [T4], '987.6')

    def m_pin_flip():
        e = first(cited_pinned, 'no CITED_PINNED entry')
        return edit_row(e, flip_sha), None
    add('v005_entry_pin_changed', g, m_pin_flip, [T5], 'section changed')

    def m_marker_changed():
        if marked:
            e = marked[0]['entry']
            return edit_row(e, lambda l: l.replace('| `%s` |' % marked[0]['marker'], '| `**Nonexistent marker.**` |', 1)), None
        e = 'A65' if 'A65' in cited_pinned else first(cited_pinned, 'no CITED_PINNED entry')
        return edit_row(e, lambda l: l.replace('| next heading |', '| `**Nonexistent marker.**` |', 1)), None
    add('v005_end_marker_changed', g, m_marker_changed, [T5], 'Nonexistent marker')

    def m_dispatch():
        m = re.search(r'^\| (0\d{3}) \| `([0-9a-f])([0-9a-f]{63})` \|$', prereg, re.M)
        need(m, 'no dispatch row in the sources section')
        flip = '0' if m.group(2) != '0' else '1'
        return sub(P, m.group(0), '| %s | `%s%s` |' % (m.group(1), flip, m.group(3))), None
    add('dispatch_sha_changed', g, m_dispatch, [T5], 'dispatch')
    tagline = re.search(r'^(#{2,4} [^\n]*?)(\[C-[A-Za-z0-9.]+\])$', prereg, re.M)
    tags = re.findall(r'\[(C-[A-Za-z0-9.]+)\]', prereg)
    other_tag = ([x for x in tags if tagline and '[%s]' % x != tagline.group(2)] or [None])[0]

    def m_dup_tag():
        need(tagline and other_tag, 'no tagged heading')
        return sub(P, tagline.group(0), tagline.group(0) + ' [%s]' % other_tag), None
    add('duplicate_tag', g, m_dup_tag, [T6], '"duplicate_in_text": ["%s"]' % other_tag)

    def m_unmapped_tag():
        need(tagline, 'no tagged heading')
        return sub(P, tagline.group(0), tagline.group(0) + ' [C-9.9]'), None
    add('unmapped_tag', g, m_unmapped_tag, [T6], 'C-9.9')
    maprow = re.search(r'^\| C-[A-Za-z0-9.]+ \|[^\n]*$', csm, re.M)
    add('map_row_without_tag', g, lambda: (need(maprow, 'no map row'), (sub(M, maprow.group(0), '| C-ZZ | phantom | — | NEW | none |\n' + maprow.group(0)), None))[1],
        [T6], 'C-ZZ')
    add('later_entry_uncovered', g, V(v_insert_heading('## A999: synthetic later entry')), [T7], 'A999', kind='cur')

    g = 'provenance_rules'
    free_post = [x for x in ('0998', '0997', '0996', '0995', '0994') if x not in ctx['posts']][0]
    add('category_not_in_closed_list', g, B(prov(lambda d: d.setdefault('categories', {}).update(MY_CATEGORY='self-declared'))), [T4], 'MY_CATEGORY')

    def m_derived():
        ks = bycat.get('NODE_DERIVED', [])
        need(ks, 'no NODE_DERIVED entry')
        k = ks[0]
        x = numbers[k]
        if x.get('formula') == 'midpoint':
            a, b = x['node_indices']
            return prov(lambda d: d['numbers'][k].update(node_indices=[a, b + 1])), None
        mm = re.search(r'midpoint of nodes (\d+) and (\d+)', ' '.join(x.get('uses', [])))
        need(mm, 'NODE_DERIVED entry without a midpoint formula')
        bad = 'midpoint of nodes %s and %d' % (mm.group(1), int(mm.group(2)) + 1)
        return prov(lambda d: d['numbers'][k].update(uses=[bad])), None
    add('node_derived_wrong_formula', g, m_derived, [T4], 'formula gives')
    add('post_number_without_message', g, B(both(ins('See the post %s.' % free_post),
                                                   prov(lambda d: d['numbers'].update({free_post: {'category': 'DISPATCH_OR_POST_NUMBER', 'uses': ['synthetic']}})))),
        [T4], free_post)
    add('declared_identifier_unused', g, B(prov(lambda d: d.setdefault('identifiers', {}).update({'Z9Z9': 'synthetic, used nowhere'}))), [T4], 'Z9Z9')
    add('heading_number_shape', g, B(both(ins('See item 987.6 of the list.'),
                                           prov(lambda d: d['numbers'].update({'987.6': {'category': 'HEADING_OR_ITEM_NUMBER', 'uses': ['synthetic']}})))),
        [T4], '987.6')
    add('unexpected_file_in_tools', g, B(lambda d: (os.makedirs(os.path.join(d, 'tools')), newfile('tools/extra_c4.py', '# synthetic\n')(d))), [T1], 'extra_c4.py')

    g = 'closure42'
    q = Q
    add('A01_listed_number_as_target_value', g, B(ins('The quoted value v_q of %s is 778.' % q)), [T3], '778')
    add('A02_listed_number_as_sigma_bound', g, B(ins('The quoted σ_q of every OUTER row is below 93.6.')), [T3], '93.6')
    add('A03_listed_number_unit_with_unicode_minus', g, B(ins('The quoted value of %s is 778 km s%s1.' % (q, UMINUS))), [T2], 'km s')
    add('A04_listed_number_unit_middle_dot', g, B(ins('The quoted value of %s is 778 km·s⁻¹.' % q)), [T2], 'km')
    add('A05_listed_number_unit_in_words', g, B(ins('The quoted value of %s is 778 kilometres per second.' % q)), [T2], 'kilometres per second')
    add('A06_listed_number_unit_division_slash', g, B(ins('The quoted value of %s is 778 km∕s.' % q)), [T2], 'km∕s')
    add('A07_listed_mantissa_m_per_s', g, B(ins('The quoted value of %s is 1.48e5 m/s.' % q)), [T2, T4], 'm/s')
    add('B01_zero_width_split_digits_unicode_minus_unit', g, B(ins('The quoted value of %s is 9%s8%s7 km s%s1.' % (q, ZW, ZW, UMINUS))), [T2], 'km s')
    add('B02_markdown_bold_split_digits', g, B(ins('The quoted value of %s is 9**8**7.' % q)), [T4], '9**8')
    add('B03_superscript_digits_with_km_s', g, B(ins('The quoted value of %s is ⁹⁸⁷ km/s.' % q)), [T2], 'km/s')
    add('B04_sci_notation_superscript_exponent_km_s', g, B(ins('The quoted value of %s is 1.48×10³ km/s.' % q)), [T2], 'km/s')
    add('B05_number_words_km_s', g, B(ins('The quoted value of %s is nine hundred eighty-seven km/s.' % q)), [T2, T4], 'hundred')
    add('B06_glued_to_identifier_slash', g, B(ins('Quoted pair: %s/987.6.' % q)), [T4], '987.6')
    add('B07_glued_to_identifier_underscore', g, B(ins('Quoted pair: %s_987.' % q)), [T4], '987')
    add('B08_eight_digit_number_cm_s', g, B(ins('The quoted value of %s is 98760000 cm/s.' % q)), [T2], 'cm/s')
    add('B09_section_sign_strip', g, B(ins('The quoted value of %s is §987.6.' % q)), [T4], '987.6')
    add('B10_code_span_K1_control', g, B(ins('The quoted value of %s is `987.6`.' % q)), [T4], '987.6')
    add('B11_code_span_symbol_defeats_T3', g, B(ins('For %s, `v_q` = 778.' % q)), [T3], '778')
    add('B12_escaped_underscore_symbol_defeats_T3', g, B(ins('For %s, v\\_q = 778.' % q)), [T3], '778')
    add('B13a_indexed_symbol_unlisted_value_control', g, B(ins('v_q(%s) = 987.6.' % q)), [T3, T4], '987.6')
    add('B13b_indexed_symbol_listed_value', g, B(ins('v_q(%s) = 778.' % q)), [T3], '778')
    add('B14_symbol_with_approx_sign_variant', g, B(ins('For %s, v_q ≃ 778.' % q)), [T3], '778')
    add('B15_number_in_ROOT_ITEMS', g, B(app(R, 'The outermost quoted value is 987.6.')), [T4], '987.6')
    add('B16_number_in_CLAUSE_MAP', g, B(app(M, 'The outermost quoted value is 987.6.')), [T4], '987.6')
    add('B17_self_declared_category', g, B(both(ins('The outermost quoted value is 987.6.'),
                                                prov(lambda d: d['numbers'].update({'987.6': {'category': 'MODEL_DIAGNOSTIC', 'uses': ['synthetic']}})))),
        [T4], '987.6: not located')
    add('C01_target_path_elided_root_txt', g, B(ins('Rows were read from `…/data/NGC3198_observed_curve.txt`.')), [T1], 'observed_curve')
    add('C02_target_path_json', g, B(ins('Rows were read from `…/NGC3198_OBSERVED_VELOCITIES.json`.')), [T1], 'observed_velocit')
    add('C03_extension_variant_data', g, B(ins('Rows were read from NGC3198.data.')), [T1], 'NGC3198.data')
    add('C04_extension_variant_dat_suffix', g, B(ins('Rows were read from NGC3198.dat_v2.')), [T1], 'NGC3198.dat_v2')
    add('C05_extension_variant_tsv_xlsx_fts', g, B(ins('Rows were read from NGC3198.tsv, NGC3198.xlsx and NGC3198.fts.')), [T1], 'NGC3198.fts')
    add('C05b_extension_xlsx_only', g, B(ins('Rows were read from NGC3198.xlsx.')), [T1], 'NGC3198.xlsx')
    add('C06_other_target_data_source_names', g, B(ins('Rows were read from the THINGS curve of de Blok et al., and the van Albada data.')), [T1], 'THINGS')
    add('C07_fullwidth_SPARC', g, B(ins('Rows were read from the ＳＰＡＲＣ table.')), [T1], 'sparc')
    add('C08_soft_hyphen_rotmod', g, B(ins('Rows were read from the rot­mod file.')), [T1], 'rotmod')
    add('C09_spaced_or_underscored_mass_models', g, B(ins('Rows were read from the Mass Models table (Mass_Models).')), [T1], 'Mass Models')
    add('C10_forbidden_term_in_provenance_json', g, lambda: (need(anykey, 'empty provenance'),
                                                             (prov(lambda d: d['numbers'][anykey]['uses'].append('row count read from the rotmod table')), None))[1], [T1], N)
    add('C11_vobs_variants', g, B(ins('Rows were read from the V obs and v-obs columns.')), [T1], 'V obs')
    add('C12_program_blinded_run_named', g, B(ins('Compare with runs_ext/KMAX_A2F10_C5H_RUN_V001 and UVT_Z2_A2F10_RUN_V001.')), [T1], 'kmax_a2f10_c5h')

    def m_d01():
        m = re.search(r'^\| 0\d{3} \| `[0-9a-f]{64}` \|$', prereg, re.M)
        need(m, 'no dispatch row to insert after')
        return insert_after_line(m.group(0), '| `%s` | `%s` |' % (synth_path, '0' * 64)), None
    add('D01_sec11_pins_targetlike_named_synthetic_file', g, m_d01, [T1, T5], 'not opened')
    add('E01_forbidden_term_in_INDEX', g, lambda: (need(ctx['has_index'], 'no INDEX in the bundle'), (app(I, 'Rows were read from the rotmod table.'), None))[1], [T1], I)
    add('E02_listed_number_unit_m_s_plain', g, B(ins('The quoted value of %s is 778 m/s.' % q)), [T2], 'm/s')
    add('E03_listed_number_code_span_symbol_sigma', g, B(ins('For %s, `σ_q` = 93.6.' % q)), [T3], '93.6')

    g = 'targetfree_lens'
    add('N01_cgj_Mn', g, B(ins('Rows were read from the rot͏mod file.')), [T1], 'rotmod')
    add('N02_vs16_Mn', g, B(ins('Rows were read from the rot️mod file.')), [T1], 'rotmod')
    add('N03_cyrillic_A', g, B(ins('Rows were read from the SPАRC table.')), [T1], 'sparc')
    add('N04_cyrillic_o', g, B(ins('Rows were read from the rоtmod file.')), [T1], 'rotmod')
    add('N05_greek_omicron', g, B(ins('Rows were read from the rοtmod file.')), [T1], 'rotmod')
    add('N06_html_ncr', g, B(ins('Rows were read from the &#x72;otmod file.')), [T1], 'rotmod')
    add('N07_html_shy_entity', g, B(ins('Rows were read from the rot&shy;mod file.')), [T1], 'rotmod')
    add('N08_html_comment_split', g, B(ins('Rows were read from the rot<!-- -->mod file.')), [T1], 'rotmod')
    add('N09_markdown_emphasis_split', g, B(ins('Rows were read from the rot**mod** file.')), [T1], 'rotmod')
    add('N10_hangul_filler', g, B(ins('Rows were read from the rotᅟmod file.')), [T1], 'U+115F')
    add('N11_latex_vsub', g, B(ins('Rows used V_{obs} and V_{\\rm obs} from the table.')), [T1], 'v_obs')
    add('N12_ext_txt_asc_h5_npy', g, B(ins('Rows were read from q99.txt, q99.asc, q99.h5, q99.npy and q99.parquet.')), [T1], 'q99.parquet')
    for cid, unit in [('U01_latex_dollar', 'km s$^{-1}$'), ('U02_latex_thin_space', 'km\\,s$^{-1}$'), ('U03_caret_braces', 'km s^{-1}'),
                      ('U04_html_sup', 'km s<sup>-1</sup>'), ('U05_en_dash', 'km s–1'), ('U06_hyphen_2010', 'km s‐1'), ('U07_fraction_slash', 'km⁄s'),
                      ('U08_parenthesised', '(km/s)'), ('U09_m_per_s', 'm/s'), ('U10_kpc_per_Gyr', 'kpc/Gyr'), ('U11_kilometers_slash_second', 'kilometers/second'),
                      ('U12_kmps', 'kmps'), ('U13_caret_paren', 'km s^(-1)'), ('U14_mathrm', '\\mathrm{km\\,s^{-1}}')]:
        add(cid, g, B(ins('The quoted value at %s is 778 %s.' % (Q, unit))), [T2], None)
    add('U15_unit_in_table_header', g, B(ins('| id | v (km/s) |\n|---|---|\n| %s | 778 |' % Q)), [T2], 'km/s')
    for cid, s, needle in [('S01_braced_subscript', 'v_{q} = 778', '778'), ('S02_walrus', 'v_q := 778', '778'), ('S03_identical_to', 'v_q ≡ 778', '778'),
                           ('S04_tilde_operator', 'v_q ∼ 778', '778'), ('S05_eq_tilde', 'v_q = ~778', '778'), ('S06_eq_paren', 'v_q = (778', '778'),
                           ('S07_is', 'v_q is 778', '778'), ('S08_vflat_no_underscore', 'Vflat = 778', '778'), ('S09_v_c', 'V_c = 778', '778'),
                           ('S10_v_circ', 'v_circ = 778', '778'), ('S11_sigma_braced', 'σ_{q} = 93.6', '93.6'), ('S12_e_v', 'e_v = 93.6', '93.6'),
                           ('S13_observed_rotation_speed', 'the observed rotation speed = 778', '778'), ('S14_less_than', 'v_q < 778', '778'),
                           ('S15_leq', 'v_q ≤ 778', '778')]:
        add(cid, g, B(ins('For %s, %s.' % (Q, s))), [T3], needle)
    add('H01_hex_with_letter', g, B(ins('The quoted value at %s is 9876e5.' % Q)), [T4], '9876e5')
    add('H02_iso_Z_suffix', g, B(ins('The quoted value at %s is 9876Z.' % Q)), [T4], '9876')
    add('H03_iso_time_Z', g, B(ins('The quoted value at %s is 98:76Z.' % Q)), [T4], '98')
    add('H04_tag_free_text', g, B(ins('[C-quoted value at %s is 987.6]' % Q)), [T4], '987.6')
    add('H05_tag_multiline_span', g, B(ins('Note [C-\nThe quoted value at %s is 987.6.\nend]' % Q)), [T4], '987.6')
    add('H06_ident_chain_hyphen', g, B(ins('The quoted value-987.6 is recorded.')), [T4], '987.6')
    add('H07_ident_digit', g, B(ins('The quoted value is v987 at %s.' % Q)), [T4], '987')
    add('H08_greek_glued', g, B(ins('The quoted value is σ987.6 at %s.' % Q)), [T4], '987')
    add('H09_exponent_listed_mantissa', g, B(ins('The quoted value at %s is 1.48e9.' % Q)), [T4], '1.48e9')
    add('H10_html_comment_digits', g, B(ins('The quoted value at %s is 9<!-- -->8<!-- -->7.' % Q)), [T1, T4], '<!--')
    add('H11_html_ncr_digits_unit', g, B(ins('The quoted value at %s is &#x39;&#x38;&#x37; km/s.' % Q)), [T1, T2], '&#x39;')
    add('H12_hex_literal', g, B(ins('The quoted value at %s is 0x3DB.' % Q)), [T4], '0x3DB')
    add('H13_url_path', g, B(ins('See [the row](https://example.invalid/q99/987.6).')), [T1, T4], 'https://')
    add('F01_index_unscanned', g, lambda: (need(ctx['has_index'], 'no INDEX'), (app(I, 'Rows were read from the rotmod table; v_q = 987.6 km/s.'), None))[1],
        [T1, T2, T3], I)
    add('F02_provenance_uses_unscanned', g, lambda: (need(anykey, 'empty provenance'),
                                                     (prov(lambda d: d['numbers'][anykey]['uses'].append('v_q = 987.6 km/s at %s' % Q)), None))[1], [T2, T3], N)
    add('F03_provenance_unused_key', g, B(prov(lambda d: d['numbers'].update({'987.6': {'category': 'MODEL_DIAGNOSTIC', 'uses': ['quoted at %s' % Q]}}))), [T4], '987.6')
    add('F04_new_bundle_file', g, B(newfile('APPENDIX_R3.md', 'Rows were read from the rotmod table; v_q = 987.6 km/s.\n')), [T1], 'APPENDIX_R3.md')

    def m_e01():
        need('A66' in cited_pinned, 'A66 is not CITED_PINNED')
        s = v[v.index('\n## A66:') + 1:]
        s = s[:s.find('\n## ')] if '\n## ' in s else s
        fact = [l for l in s.split('\n')[1:] if l.startswith('**Fact')]
        need(len(fact) == 1, 'no single **Fact line in A66')
        return with_marker('A66', fact[0], v), None
    add('E01_early_end_marker_A66', g, m_e01, [T5], 'not allow-listed')

    def m_e02():
        need('A66' in cited_pinned and 'A66' in cited, 'A66 is not cited and pinned')
        return to_no_change('A66', v), v_sub('is flagged **TRUNCATION_SHAPE_RESIDUAL** in the freeze manifest', 'is not flagged in the freeze manifest')
    add('E02_pin_dropped_listed_no_change', g, m_e02, [T5, T7], 'A66 is cited but not CITED_PINNED')
    add('E03_malformed_pin_row_trailing_space', g, lambda: (edit_row(first(cited_pinned, 'none'), lambda l: l + ' '), None), [T5], 'unparsable')
    rng = 'A91' if 'A91' in nc else (nc[0] if nc else None)
    add('T01_open_ended_range_row', g, lambda: (need(rng, 'no NO_CHANGE entry'),
                                                (edit_row(rng, lambda l: l.replace('| %s |' % rng, '| %s–A999 |' % rng, 1)), None))[1], [T7], rng)
    add('T02b_level3_heading', g, V(v_insert_heading('### A999: synthetic')), [T7], 'whole-file', kind='cur')
    add('T02d_no_space_heading', g, V(v_insert_heading('##A999: synthetic')), [T7], 'whole-file', kind='cur')
    add('T02e_lower_heading', g, V(v_insert_heading('## a999: synthetic')), [T7], 'a999', kind='cur')
    add('T02f_prefix_word_heading', g, V(v_insert_heading('## Entry A999: synthetic')), [T7], 'Entry A999', kind='cur')
    add('T02g_bold_entry', g, V(v_insert_heading('**A999: synthetic**')), [T7], 'whole-file', kind='cur')

    g = 't5_t7_probe'
    add('X1_new_heading', g, V(v_insert_heading('## A999: synthetic probe entry, amends A81 RI-23 (tools lens)')), [T7], 'A999', kind='cur')
    add('X2_inplace_edit_cited_A66', g, lambda: (need('A66' in cited_pinned, 'A66 not pinned'),
                                                 (None, v_append_in('## A66:', 'Synthetic probe: A66.2 is withdrawn.\n\n')))[1], [T5, T7], 'A66')
    x3 = 'A91' if 'A91' in nc else (nc[-1] if nc else None)
    add('X3_inplace_edit_nochange_entry', g, lambda: (need(x3, 'no NO_CHANGE entry'),
                                                      (None, v_append_in('## %s:' % x3, 'Synthetic probe: A66.2 is withdrawn; R-TSR is dropped.\n\n')))[1],
        [T7], x3, kind='cur')
    add('X4_suffix_heading_A81a', g, V(v_insert_heading('## A81a: synthetic probe, amends RI-23 (tools lens)')), [T7], 'A81a', kind='cur')
    add('X5_heading_A66_amendment', g, V(v_insert_heading('## A66 amendment: synthetic probe, withdraws A66.2 (tools lens)')), [T7], 'A66 amendment', kind='cur')
    last_entry = ctx['last_entry']
    add('X6_append_at_EOF_plain_text', g, V(lambda t: t + '\n**Synthetic probe (tools lens).** A66.2 is withdrawn; N_FAIL_N1 now blocks route A/B.\n'),
        [T5, T7] if last_entry in cited_pinned else [T7], last_entry)
    add('X7_edit_inside_A65_trailing_block', g, lambda: (need('A65' in cited_pinned, 'A65 not pinned'),
                                                         (None, v_sub('N_PASS is only an input to NGC route A/B.', 'N_PASS is the only input to NGC route A/B.')))[1],
        [T5, T7], 'A65')
    add('X8_inplace_edit_A47_I3', g, V(v_append_in('## A47:', 'Synthetic probe: RA13 blinding (I3) is withdrawn.\n\n')),
        [T5, T7] if 'A47' in cited_pinned else [T7], 'A47')

    g = 'entry_table'
    add('suffix_heading_A98a', g, V(v_insert_heading('## A98a: synthetic suffix-form entry (tools lens)')), [T7], 'A98a', kind='cur')
    n0 = nc[0] if nc else None
    n1 = nc[1] if len(nc) > 1 else None
    add('entry_table_omission_rendered', g, lambda: (need(n0, 'no NO_CHANGE entry'), (drop_row(n0), None))[1], [T7], n0)
    add('entry_table_omission_json', g, lambda: (need(n0, 'no NO_CHANGE entry'),
                                                 (etab(lambda d: d['entries'].pop([x['entry'] for x in d['entries']].index(n0))), None))[1], [T7], 'JSON')
    add('duplicate_heading_row', g, lambda: (need(n0, 'no NO_CHANGE entry'), (dup_row(n0), None))[1], [T7], n0)
    add('entry_table_out_of_order', g, lambda: (need(n1, 'fewer than two NO_CHANGE entries'), (swap_rows(n0, n1), None))[1], [T7], 'file order')
    add('heading_cell_changed', g, lambda: (need(n0, 'no NO_CHANGE entry'),
                                            (edit_row(n0, lambda l: join_cells([c + (' (edited)' if k == 1 else '') for k, c in enumerate(T.split_cells(l))])), None))[1],
        [T7], n0)
    add('cited_but_unpinned_new_citation', g, lambda: (need(n0, 'no NO_CHANGE entry'), (ins('The note of %s is recorded here.' % n0), None))[1], [T5], '%s is cited' % n0)
    flip = [e for e in cited_pinned if e in cited and e != 'A66']
    add('cited_but_unpinned_flipped', g, lambda: (need(flip, 'no cited entry to flip'), (to_no_change(flip[0], v), None))[1], [T5],
        '%s is cited' % (flip[0] if flip else ''))
    add('json_sha_mismatch', g, B(etab(lambda d: d.update(v005_sha256_read='0' * 64))), [T7], 'v005_sha256_read')
    add('json_reason_differs', g, B(etab(lambda d: d['entries'][1].update(reason=d['entries'][1]['reason'] + ' (edited)'))), [T7], 'differs')
    if has_tail:
        add('a65_tail_edit', g, V(v_sub('Codex2 is a different model family', 'Codex2 is the same model family')), [T5, T7], 'A65 tail')
        add('a65_tail_row_dropped', g, B(drop_row('A65' + T.TAIL_SUFFIX)), [T5], 'not pinned by a tail row')
    else:
        add('a65_tail_edit', g, lambda: (need('A65' in cited_pinned, 'A65 not pinned'),
                                         (None, v_sub('Codex2 is a different model family', 'Codex2 is the same model family')))[1], [T5, T7], 'A65')
        add('a65_marker_without_tail_row', g, lambda: (need('A65' in cited_pinned, 'A65 not pinned'),
                                                       (with_marker('A65', T.END_MARKER_ALLOW['A65'], v, tail_row=False), None))[1],
            [T5], 'not pinned by a tail row')
    add('preamble_edit_whole_file_only', g, V(v_sub('Entries continue from A47.', 'Entries continue from A46.')), [T7], 'whole-file', kind='cur')

    def m_seal():
        m6 = re.search(r'The cited entries are ((?:A\d{1,3}[a-z]?)(?:(?:, |,? and )A\d{1,3}[a-z]?)*)\.', root)
        need(m6, 'no "The cited entries are ..." list in ROOT_ITEMS')
        lst = re.findall(r'A\d{1,3}[a-z]?', m6.group(1))
        need(len(lst) > 1, 'one-entry list')
        short = ', '.join(lst[:-2]) + (', ' if len(lst) > 2 else '') + lst[-2]
        return sub(R, m6.group(0), 'The cited entries are %s.' % short), None
    add('seal_list_differs_from_pins', g, m_seal, [T5], 'seal list')

    # ---------------- fix stage: V006 (RF-B1/TF-B1). The old case "a V006 file exists" is replaced by these.
    g = 'v006'
    v6 = ctx['v006_text']
    rows6 = ctx['rows6']
    ids6 = [r['entry'] for r in rows6]
    nil = lambda: (None, None)

    def need6():
        need(v6 is not None and rows6, 'no V006 addendum or no V006 rows in this bundle')
        return None, None
    psha = ctx['prereg_sha']
    seal = ('\n## A999: seal entry for the miss-reading prereg (synthetic fix-stage control; never published)\n\n'
            'Root registers the rendered prereg `%s` and the classifier. Synthetic.\n\n'
            '## A1000: a later synthetic entry (control)\n\nSynthetic.\n' % psha)
    add('v006_new_heading_uncovered', g, need6, [T7], 'V006 heading not covered', kind='cur',
        v6=v6_insert_heading('## A998: synthetic V006 entry inserted before the seal (fix-stage probe)'))
    add('v006_appended_entry_not_seal', g, need6, [T7], 'V006 heading not covered', kind='cur',
        v6=v6_append('\n## A998: a synthetic later root entry that names no prereg sha (probe)\n\nSynthetic.\n'))
    add('v006_inplace_edit_no_change_entry', g, need6, [T7], 'changed since it was read', kind='cur',
        v6=v6_append_in_first('Synthetic probe: this entry now rules on the miss-reading prereg.\n\n'))
    pre = 'Entries continue the A-numbering.'

    def need_pre():
        need6()
        need(pre in v6, 'no %r sentence in the V006 preamble' % pre)
        return None, None
    add('v006_preamble_edit_whole_file', g, need_pre, [T7], 'whole-file', kind='cur',
        v6=lambda v: v6_sub(pre, 'Entries continue the A numbering.')(v))
    add('v006_table_file_missing', g, need6, [T7], 'V006 heading not covered', kind='cur', setup='no_etab6')
    add('v006_rendered_row_dropped', g, lambda: (need6(), (drop_row(ids6[0]), None))[1], [T7], 'V006 heading not covered')
    add('v006_rows_out_of_order', g, lambda: (need(len(ids6) > 1, 'fewer than two V006 rows'), (swap_rows(ids6[0], ids6[1]), None))[1],
        [T7], 'file order')
    add('v006_heading_cell_changed', g, lambda: (need6(), (edit_row(ids6[0], lambda l: join_cells(
        [c + (' (edited)' if k == 1 else '') for k, c in enumerate(T.split_cells(l))])), None))[1], [T7], 'heading cell differs')
    add('v006_json_sha_mismatch', g, lambda: (need6(), (etab(lambda d: d.update(v006_sha256_read='0' * 64), E6), None))[1], [T7],
        'v006_sha256_read')
    add('v006_json_reason_differs', g, lambda: (need6(), (etab(lambda d: d['entries'][0].update(
        reason=d['entries'][0]['reason'] + ' (edited)'), E6), None))[1], [T7], 'differs from rendered row')
    add('v006_cited_but_unpinned', g, lambda: (need6(), (ins('The note of %s is recorded here.' % ids6[0]), None))[1], [T5],
        'V006 %s is cited' % (ids6[0] if ids6 else ''))
    add('v006_seal_entry_then_prefix_edit', g, need_pre, [T7], 'trimmed sha', kind='cur',
        v6=lambda v: v6_sub(pre, 'Entries continue the A numbering.')(v) + seal)
    add('v006_seal_like_entry_for_another_text', g, need6, [T7], 'V006 heading not covered', kind='cur',
        v6=v6_append(seal.replace(psha, '0' * 64)))
    add('control_v006_seal_entry_appended', 'controls', need6, [T7], 'seal entry found', kind='pass', v6=v6_append(seal))
    add('control_v006_seal_entry_after_blank_lines', 'controls', need6, [T7], 'seal entry found', kind='pass',
        v6=v6_append('\n\n' + seal))

    # ---------------- fix stage: the refuters' evasion classes (TF-S2 terms, numbers, units, JSON notes; TF-S3 symbols)
    g = 'fix_terms_T1'
    for cid, s, needle in [('P01_rot_underscore_mod', 'Rows were read from the rot_mod table.', 'rot'),
                           ('P02_rot_hyphen_mod', 'Rows were read from the rot-mod table.', 'rot'),
                           ('P03_rot_space_mod', 'Rows were read from the rot mod table.', 'rot'),
                           ('P04_spaced_SPARC', 'Rows were read from the S P A R C table.', 'S P A'),
                           ('P05_dotted_SPARC', 'Rows were read from the S.P.A.R.C. table.', 'S.P.A'),
                           ('P06_mixed_case_Things', 'Rows were read from the Things survey.', 'Things'),
                           ('P07_dotted_mass_models', 'Rows were read from Mass.Models.', 'Mass'),
                           ('P08_slashed_v_obs', 'Rows were read from the V/obs column.', 'obs'),
                           ('P09_n3198_json', 'Rows were read from `…/n3198_curve.json`.', 'n3198'),
                           ('P10_spaced_NGC_path', 'Rows were read from `…/NGC 3198/curve.json`.', 'curve'),
                           ('P11_file_scheme_without_slashes', 'Rows were read from file:/Users/x/n.json here.', 'file:'),
                           ('P12_defanged_url', 'Rows were read from hxxps://example.invalid/n here.', 'hxxps'),
                           ('P13_url_encoded_rotmod', 'Rows were read from rot%6Dod here.', 'rotmod'),
                           ('P14_hyphen_C5H_run', 'Compare with the KMAX-A2F10-C5H run.', 'C5H'),
                           ('P15_hyphen_UVT', 'Compare with UVT-Z2-A2F10.', 'UVT')]:
        add(cid, g, B(ins(s)), [T1], needle)
    g = 'fix_numbers_T4'
    for cid, s, needle in [('N01_underscore_digit_group', 'A stand-in quantity of 98_76 appears here.', '9876'),
                           ('N02_underscore_italic_number', 'The stand-in value at %s is _987.6_.' % Q, '987.6'),
                           ('N03_underscore_bold_number', 'The stand-in value at %s is __987.6__.' % Q, '987.6'),
                           ('N04_leading_dot_decimal', 'The stand-in value at %s is .9876 here.' % Q, '9876'),
                           ('N05_prime_after_digits', 'The stand-in offset at %s is 9876′.' % Q, '9876'),
                           ('N06_double_prime_after_digits', 'The stand-in offset at %s is 9876″.' % Q, '9876'),
                           ('N07_listed_integer_prime_hides_decimal', 'The stand-in value at %s is 778.9″.' % Q, '778.9'),
                           ('N08_markdown_escaped_point', 'The stand-in value at %s is 778\\.9 here.' % Q, '778'),
                           ('N11_thousands_comma_listed_parts', 'The stand-in count at %s is 1,778.' % Q, '1778'),
                           ('N16_trailing_underscore', 'The stand-in value is 9876_ here.', '9876')]:
        add(cid, g, B(ins(s)), [T4], needle)
    add('E06_entry_table_json_note_number', g, B(etab(lambda d: d.update(note='read with the stand-in 987.6 in mind'))), [T4], '987.6')
    add('E06b_v006_table_json_note_number', g, lambda: (need6(), (etab(lambda d: d.update(note='stand-in 987.6'), E6), None))[1],
        [T4], '987.6')
    add('E11_provenance_note_number', g, B(prov(lambda d: d.update(note=d.get('note', '') + ' Stand-in 987.6.'))), [T4], '987.6')
    add('E07_no_change_entry_tail_reason', g, lambda: (need(nc, 'no NO_CHANGE entry'), (etab(lambda d: d['entries'][
        [x['entry'] for x in d['entries']].index(nc[0])].update(tail_reason='stand-in note')), None))[1], [T7], 'pin fields')
    g = 'fix_units_T2'
    for cid, unit in [('U02_pc_Myr_caret', 'pc Myr^-1'), ('U03_km_per_h', 'km/h'), ('U04_AU_per_yr', 'AU/yr'),
                      ('U05_km_per_secs', 'km/secs'), ('U06_m_dot_above_precomposed', 'kṁ/s'), ('U07_s_acute_precomposed', 'km/ś'),
                      ('U08_big_solidus_U29F8', 'km⧸s'), ('U09_markdown_italic_s', 'km/_s_'),
                      ('U10_kilometres_a_second', 'kilometres a second'), ('U11_miles_per_second', 'mi/s')]:
        add(cid, g, B(ins('The stand-in rate at %s is 778 %s.' % (Q, unit))), [T2], None)
    g = 'fix_symbols_T3'
    for cid, s, needle in [('S01_underscore_italic_value', 'v_q = _778_', '778'), ('S02_value_first', '778 = v_q', '778'),
                           ('S03_geq_slanted_U2A7E', 'v_q ⩾ 778', '778'), ('S04_arrow', 'v_q → 778', '778'),
                           ('S05_element_of_interval', 'v_q ∈ [93.6, 778]', '93.6'), ('S06_between', 'v_q between 93.6 and 778', '93.6'),
                           ('S08_hyphen_subscript', 'v-q = 778', '778'), ('S09_v_tilde_precomposed', 'ṽ_q = 778', '778'),
                           ('S10_unlisted_symbol_V_last', 'V_last = 778', '778'), ('S11_final_sigma', 'ς_q = 93.6', '93.6'),
                           ('S12_colon_equals_U2254', 'v_q ≔ 778', '778'), ('S13_approx_U2252', 'v_q ≒ 778', '778'),
                           ('S14_leqq_U2266', 'v_q ≦ 778', '778'), ('S16_unlisted_phrase', 'the outer speed is 778', '778')]:
        add(cid, g, B(ins('For %s, %s.' % (Q, s))), [T3], needle)
    add('S07_markdown_table_cell', g, B(ins('| query | v_q |\n|---|---|\n| %s | 778 |' % Q)), [T3], '778')
    return c


def hook_probes(work, hook, link_out):
    """Exercise the shared hook. Filesystem probes are real calls on canaries in --work; process and network probes call the
    hook function directly with synthetic arguments, so nothing can start even if the hook were wrong."""
    res = []
    canary = os.path.join(work, 'hook_canary.txt')
    with open(canary, 'x') as f:
        f.write('hook canary 18 by\n')
    size0 = os.path.getsize(canary)
    outside = os.path.join(os.path.dirname(work), os.path.basename(work) + '_HOOK_PROBE_NEVER_CREATED')
    fake = '/nonexistent_hook_probe_dir_c4'

    def probe(name, fn, want):
        try:
            fn()
            got = 'ALLOWED'
        except PermissionError:
            got = 'REFUSED'
        except OSError as e:
            got = 'OSERROR:%s' % type(e).__name__
        res.append({'probe': name, 'want': want, 'got': got, 'ok': got == want})
    probe('open_append_inside_work', lambda: open(canary, 'a').close(), 'ALLOWED')
    probe('os.truncate_canary', lambda: os.truncate(canary, 0), 'REFUSED')
    probe('os.chmod_canary', lambda: os.chmod(canary, 0o644), 'REFUSED')
    probe('os.utime_canary', lambda: os.utime(canary, None), 'REFUSED')
    probe('os.symlink_in_work', lambda: os.symlink(canary, os.path.join(work, 'probe_symlink')), 'REFUSED')
    probe('os.link_in_work', lambda: os.link(canary, os.path.join(work, 'probe_hardlink')), 'REFUSED')
    probe('os.remove_canary', lambda: os.remove(canary), 'REFUSED')
    probe('os.rename_canary', lambda: os.rename(canary, canary + '.renamed'), 'REFUSED')
    probe('os.mkdir_inside_work', lambda: os.mkdir(os.path.join(work, 'probe_subdir')), 'ALLOWED')
    probe('os.mkdir_outside_work', lambda: os.mkdir(outside), 'REFUSED')
    probe('open_write_outside_work', lambda: open(outside + '.txt', 'x').close(), 'REFUSED')
    probe('open_write_via_symlink_resolving_outside_work', lambda: open(link_out, 'w').close(), 'REFUSED')
    probe('os.listdir_work', lambda: os.listdir(work), 'ALLOWED')
    probe('os.listdir_denylisted_lexical', lambda: os.listdir(fake + '/sparc_tables'), 'REFUSED')
    probe('os.scandir_denylisted_lexical', lambda: os.scandir(fake + '/rotmod_dir'), 'REFUSED')
    probe('glob_denylisted_lexical', lambda: __import__('glob').glob(fake + '/massmodels_*'), 'REFUSED')
    probe('open_denylisted_lexical', lambda: open(fake + '/NGC3198_observed_velocity.json'), 'REFUSED')
    probe('open_uvt_component', lambda: open(fake + '/UVT_PROBE/x.json'), 'REFUSED')
    probe('open_c5h_run_name', lambda: open(fake + '/runs_ext/KMAX_A2F10_C5H_RUN_V001/x'), 'REFUSED')
    # fix stage (TF-S1): the long-s spelling, separator-split names, a deny-named component before '..', and a clean-named
    # symlink into a deny-named place followed by '..'. The live probes use the in-process decoy term only.
    def lexical(p):
        if T.path_denied(p):
            raise PermissionError('denied')
    probe('path_raw_deny_component_before_dotdot', lambda: lexical(fake + '/rotmod_dir/../x.json'), 'REFUSED')
    probe('path_long_s_spelling', lambda: lexical(fake + '/ſparc_tables/x.json'), 'REFUSED')
    probe('path_separator_split_name', lambda: lexical(fake + '/rot_mod/x.json'), 'REFUSED')
    probe('path_kelvin_sign_spelling', lambda: lexical(fake + '/KMAX_A2F10_C5H_RUN_V001/x'), 'REFUSED')
    saved = T._DENY_PATH
    T._DENY_PATH = saved + (DECOY,)
    try:
        dd = os.path.join(work, DECOY + '_dir')
        probe('decoy_open_direct', lambda: open(os.path.join(dd, 'sub', 'f.txt')), 'REFUSED')
        probe('decoy_open_long_s_spelling', lambda: open(os.path.join(work, DECOY[:-1] + 'ſ_dir', 'sub', 'f.txt')), 'REFUSED')
        probe('decoy_listdir_symlink_then_dotdot', lambda: os.listdir(os.path.join(work, 'clean_dir_link_c4') + '/..'), 'REFUSED')
        probe('decoy_open_symlink_then_dotdot', lambda: open(os.path.join(work, 'clean_dir_link_c4') + '/../sub/f.txt'), 'REFUSED')
        probe('decoy_scandir_symlink_then_dotdot', lambda: os.scandir(os.path.join(work, 'clean_dir_link_c4') + '/..'), 'REFUSED')
        probe('decoy_control_clean_file_allowed', lambda: open(os.path.join(work, 'clean_control_c4.txt')).close(), 'ALLOWED')
    finally:
        T._DENY_PATH = saved
    for ev, args in [('subprocess.Popen', ('/usr/bin/true', ['/usr/bin/true'], None, None)), ('os.exec', ('/usr/bin/true', ['true'], None)),
                     ('os.fork', ()), ('os.forkpty', ()), ('os.posix_spawn', ('/usr/bin/true', ['true'], None)),
                     ('os.spawn', (0, '/usr/bin/true', ['true'], None)), ('os.system', (b'true',)),
                     ('socket.connect', (None, ('127.0.0.1', 9))), ('socket.getaddrinfo', ('example.invalid', 80, 0, 0, 0)),
                     ('shutil.rmtree', (work, None)), ('os.kill', (1, 0)), ('ctypes.dlopen', ('libc.dylib',))]:
        probe('hook_direct_' + ev, lambda ev=ev, args=args: hook(ev, args), 'REFUSED')
    res.append({'probe': 'canary_unchanged_after_refused_truncate', 'want': size0, 'got': os.path.getsize(canary),
                'ok': os.path.getsize(canary) == size0})
    res.append({'probe': 'outside_paths_not_created', 'want': False, 'got': os.path.exists(outside) or os.path.exists(outside + '.txt'),
                'ok': not (os.path.exists(outside) or os.path.exists(outside + '.txt'))})
    return res


def make_args(d, v005, v006=None):
    class A:
        pass
    a = A()
    a.dir, a.provenance, a.slots, a.expect_slots_sha = d, os.path.join(d, N), SLOTS, SLOTS_SHA
    a.nodes, a.expect_nodes_sha, a.v005, a.v006 = NODES, NODES_SHA, v005, v006
    return a


def summarize_failed(r, keys):
    out = {}
    for k in keys:
        v = r['checks'].get(k, {})
        out[k] = {kk: vv for kk, vv in v.items() if kk not in ('numeric_tokens', 'closed_category_list', 'sources', 'files_scanned',
                                                               'token_origins_other_than_plain_number')}
    return out


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--built', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--v005', default=None)
    ap.add_argument('--v006', default=None)
    a = ap.parse_args()
    work = os.path.abspath(a.work)
    built = os.path.abspath(a.built)
    os.makedirs(work)
    link_out = os.path.join(work, 'probe_link_resolving_outside')
    os.symlink(os.path.join(os.path.dirname(work), os.path.basename(work) + '_LINK_TARGET_NEVER_WRITTEN.txt'), link_out)
    # the decoy place for the TF-S1 live probes, made before the hook is installed (the decoy term is not a real deny term)
    dd = os.path.join(work, DECOY + '_dir')
    os.makedirs(os.path.join(dd, 'sub'))
    with open(os.path.join(dd, 'sub', 'f.txt'), 'x') as f:
        f.write('decoy\n')
    os.symlink(os.path.join(dd, 'sub'), os.path.join(work, 'clean_dir_link_c4'))
    with open(os.path.join(work, 'clean_control_c4.txt'), 'x') as f:
        f.write('control\n')
    hook = T.make_hook(write_dirs=[work], mkdir_dirs=[work])
    sys.addaudithook(hook)
    v005_path = os.path.abspath(a.v005) if a.v005 else T.V005_PATH
    assert not T.path_denied(v005_path)
    v005_text = rd(v005_path)
    v006_path = os.path.abspath(a.v006) if a.v006 else T.V006_PATH
    assert not T.path_denied(v006_path)
    v006_text = rd(v006_path) if os.path.isfile(v006_path) else None
    out = {'schema': 'UNT_MISS_READING_R3_TARGET_FREE_MUTATION_TEST_C4V003', 'built': built,
           'v005': {'path': v005_path, 'sha256': hashlib.sha256(v005_text.encode('utf-8')).hexdigest(), 'override': bool(a.v005)},
           'v006': {'path': v006_path, 'sha256': hashlib.sha256(v006_text.encode('utf-8')).hexdigest() if v006_text is not None else None,
                    'override': bool(a.v006)},
           'check_sha256': hashlib.sha256(open(T.__file__, 'rb').read()).hexdigest(), 'cases': [], 'not_applicable': []}
    v6arg = a.v006 and v006_path
    base = T.run(make_args(built, a.v005 and v005_path, v6arg))
    base_failed = {k for k, v in base['checks'].items() if not v['pass']}
    out['baseline'] = {'target_free': base['verdict_target_free'], 'currency': base['verdict_currency'], 'failed_checks': sorted(base_failed)}
    ok = base['verdict_target_free'] == 'PASS' and base['verdict_currency'] == 'PASS'
    if not ok:
        out['baseline_details'] = summarize_failed(base, sorted(base_failed))
    prereg = rd(os.path.join(built, P))
    rows = T.parse_v005_tables(prereg)[0]
    heads = T.v005_headings(v005_text)
    ctx = {'v005_text': v005_text, 'work': work, 'posts': T.exchange_numbers(), 'rows': rows, 'prereg': prereg,
           'csm': rd(os.path.join(built, M)), 'root': rd(os.path.join(built, R)), 'prov': json.loads(rd(os.path.join(built, N))),
           'cited': set(base['checks'][T5]['cited_v005_entries']), 'has_index': os.path.isfile(os.path.join(built, I)),
           'last_entry': heads[-1][2] if heads else None,
           'rad': {r['query_id']: r['Rad_text'] for r in T.strict_load(SLOTS)['query_block']['rows']},
           'v006_text': v006_text, 'rows6': T.parse_v006_table(prereg)[0], 'prereg_sha': base['files'][P]}
    for i, cs in enumerate(cases(ctx)):
        try:
            fn, vfn = cs['make']()
        except NotApplicable as e:
            out['not_applicable'].append({'case': cs['id'], 'group': cs['group'], 'why': str(e)})
            continue
        cd = os.path.join(work, 'case_%03d' % i)
        bd = os.path.join(cd, 'bundle')
        os.makedirs(bd)
        for n in BUNDLE:
            if cs['setup'] == 'no_etab6' and n == E6:
                continue
            src = os.path.join(built, n)
            if os.path.isfile(src):
                shutil.copyfile(src, os.path.join(bd, n))
        if fn:
            fn(bd)
        override = a.v005 and v005_path
        if vfn:
            vt = vfn(v005_text)
            assert vt != v005_text, cs['id']
            override = os.path.join(cd, 'V005_MUT.md')
            wr(override, vt)
        override6 = v6arg
        if cs['v6']:
            vt6 = cs['v6'](v006_text)
            assert vt6 != v006_text, cs['id']
            override6 = os.path.join(cd, 'V006_MUT.md')
            wr(override6, vt6)
        r = T.run(make_args(bd, override, override6))
        failed = {k for k, v in r['checks'].items() if not v['pass']}
        new = failed - base_failed
        detail = json.dumps(summarize_failed(r, sorted(cs['expect'])), ensure_ascii=False)
        needle_ok = cs['needle'] is None or cs['needle'] in detail or cs['needle'].lower() in detail.lower()
        if cs['kind'] == 'pass':
            good = r['verdict_target_free'] == 'PASS' and r['verdict_currency'] == 'PASS' and needle_ok
        else:
            verdict_fail = (r['verdict_currency'] == 'FAIL') if cs['kind'] == 'cur' else (r['verdict_target_free'] == 'FAIL' or r['verdict_currency'] == 'FAIL')
            good = cs['expect'] <= new and needle_ok and verdict_fail
        ok &= good
        rec = {'case': cs['id'], 'group': cs['group'], 'dir': 'case_%03d' % i, 'verdict_target_free': r['verdict_target_free'],
               'verdict_currency': r['verdict_currency'], 'failed_checks': sorted(failed), 'expected_at_least': sorted(cs['expect']),
               'needle': cs['needle'], 'needle_found': needle_ok, 'ok': good}
        if not good:
            rec['details'] = summarize_failed(r, sorted(failed | cs['expect']))
        out['cases'].append(rec)
    for name, kw in (('slots_sha_expected_wrong', 'expect_slots_sha'), ('nodes_sha_expected_wrong', 'expect_nodes_sha')):
        args = make_args(built, a.v005 and v005_path, v6arg)
        setattr(args, kw, '0' * 64)
        r = T.run(args)
        good = not r['checks'][T4]['pass']
        ok &= good
        out['cases'].append({'case': name, 'group': 'earlier', 'verdict_target_free': r['verdict_target_free'], 'ok': good,
                             'failed_checks': sorted(k for k, v in r['checks'].items() if not v['pass']), 'expected_at_least': [T4]})
    probes = hook_probes(work, hook, link_out)
    out['hook_probes'] = probes
    out['hook_probes_all_ok'] = all(p['ok'] for p in probes)
    ok &= out['hook_probes_all_ok']
    out['n_cases'] = len(out['cases'])
    out['n_not_applicable'] = len(out['not_applicable'])
    out['n_cases_by_group'] = {g: sum(1 for c in out['cases'] if c['group'] == g) for g in sorted({c['group'] for c in out['cases']})}
    out['failed_cases'] = [c['case'] for c in out['cases'] if not c['ok']]
    out['all_ok'] = bool(ok)
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
