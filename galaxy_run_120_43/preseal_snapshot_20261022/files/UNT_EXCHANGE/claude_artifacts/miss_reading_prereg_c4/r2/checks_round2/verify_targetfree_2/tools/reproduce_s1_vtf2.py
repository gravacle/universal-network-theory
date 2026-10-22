# verify_targetfree_2: independent reproduction of the evidence behind round-2 finding R2C-S1 (INDEX_R2.md L21-26),
# with controls and fix probes. It imports the object's check v002 read-only (run with -B, so no bytecode is written)
# and calls its run() on mutated copies of the round-2 bundle, written only under --work in my folder.
# Synthetic only: the sentinel 987.6, the fake query id NGC3198-Q99, and model-side radius edits (10.54 -> 10.55,
# 10.91 -> 10.92, 10.22 -> 10.23) of target-free numbers. No target or observed value is known to or used by this script.
# V005 is redirected to my byte snapshot of the live file (or a per-case edited copy of that snapshot).
# usage: python3 -I -B reproduce_s1_vtf2.py --work NEW_DIR --snap NEW_SNAPSHOT.md --out NEW_RESULT.json
import argparse, hashlib, json, os, re, shutil, sys, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fence_vtf2
fence_vtf2.install()

OBJ = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/miss_reading_prereg_c4/r2/round2'
LIVE_V005 = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/'
             'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md')
SLOTS = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json'
SLOTS_SHA = 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'
NODES = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json'
NODES_SHA = 'ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d'
P, M, R, N, I = 'PREREG_MISS_READING_R2.md', 'CLAUSE_SOURCE_MAP_R2.md', 'ROOT_ITEMS_R2.md', 'NUMBER_PROVENANCE_R2.json', 'INDEX_R2.md'
BUNDLE = (P, M, R, N, I)
Q = 'NGC3198-Q99'
LINE = 'Rows were read from the rotmod table; v_q = 987.6 km/s at %s.' % Q
ANCHOR = '## 0. Invariants'
NC_OLD = 'A91–A96. From V005'
A66_OLD = '| Ring | TRUNCATION_SHAPE ordinal 15, R = 10.54 kpc |'
A66_NEW = '| Ring | TRUNCATION_SHAPE ordinal 16, R = 10.54 kpc |'
STATE = {'v005': None}


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def rd(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def wr(p, t, mode='w'):
    with open(p, mode, encoding='utf-8') as f:
        f.write(t)


def edit(name, fn):
    def f(d):
        p = os.path.join(d, name)
        t = rd(p)
        t2 = fn(t)
        assert t2 != t, 'no change in ' + name
        wr(p, t2)
    return f


def prov(fn):
    def f(d):
        p = os.path.join(d, N)
        doc = json.loads(rd(p))
        fn(doc)
        wr(p, json.dumps(doc, indent=1, ensure_ascii=False) + '\n')
    return f


def newfile(name, text):
    def f(d):
        wr(os.path.join(d, name), text, 'x')
    return f


def chain(*fs):
    def f(d):
        for g in fs:
            g(d)
    return f


def before_anchor(s):
    def g(t):
        assert t.count(ANCHOR) == 1
        return t.replace(ANCHOR, s + '\n\n' + ANCHOR, 1)
    return g


def retoken(old, new):
    pat = re.compile(r'(?<![\d.])' + re.escape(old) + r'(?!\d)')

    def g(t):
        n = len(pat.findall(t))
        assert n >= 1, old
        return pat.sub(new, t)
    return g


def rekey(old, new, **upd):
    def g(doc):
        v = doc['numbers'].pop(old)
        v.update(upd)
        doc['numbers'][new] = v
    return g


def recat(key, **upd):
    def g(doc):
        doc['numbers'][key].update(upd)
    return g


def v005_case(fn):
    def f(d, snap):
        t = rd(snap)
        t2 = fn(t)
        assert t2 != t
        p = os.path.join(d, 'V005_CASE_COPY.md')
        wr(p, t2, 'x')
        return p
    return f


def a66_edit(t):
    assert t.count(A66_OLD) == 1
    return t.replace(A66_OLD, A66_NEW, 1)


def insert_heading(h):
    def g(t):
        heads = [m.start() for m in re.finditer(r'^## A\d{1,3}:', t, re.M)]
        k = heads[-1]
        return t[:k] + h + '\n\nSynthetic verify_targetfree_2 entry (not a root entry; never published).\n\n' + t[k:]
    return g


def trailing_space_on_pin(n):
    def g(t):
        m = re.search(r'^\| A%d \|[^\n]*\| `[0-9a-f]{64}` \|$' % n, t, re.M)
        assert m
        return t[:m.end()] + ' ' + t[m.end():]
    return g


def cases():
    TF, CU = 'target_free', 'currency'
    c = []
    c.append(('BASE', TF, None, None, 'baseline', 'unchanged copy; target-free should PASS'))
    # controls: the same line in a scanned file is caught
    c.append(('K1_line_in_root_items', TF, edit(R, lambda t: t + '\n' + LINE + '\n'), None, 'control', 'LINE in ROOT_ITEMS (scanned)'))
    c.append(('K2_line_in_prereg', TF, edit(P, before_anchor(LINE)), None, 'control', 'LINE in PREREG (scanned)'))
    # files and fields outside the scanned set (INDEX L22 "in any text file")
    c.append(('F01_line_in_index', TF, edit(I, lambda t: t + '\n' + LINE + '\n'), None, 'attack', 'LINE appended to INDEX_R2.md'))
    c.append(('F02a_line_in_uses', TF, prov(lambda d: d['numbers']['43']['uses'].append(LINE)), None, 'attack', 'LINE in a provenance uses string'))
    c.append(('F02b_line_in_note', TF, prov(lambda d: d.update(note=d['note'] + ' ' + LINE)), None, 'attack', 'LINE in the provenance note'))
    c.append(('F02c_line_in_category_text', TF, prov(lambda d: d['categories'].update(MODEL_DIAGNOSTIC=d['categories']['MODEL_DIAGNOSTIC'] + ' ' + LINE)), None, 'attack', 'LINE in a category description'))
    c.append(('F03_unused_key_with_line', TF, prov(lambda d: d['numbers'].update({'987.6': {'category': 'MODEL_DIAGNOSTIC', 'uses': [LINE]}})), None, 'attack', 'unused provenance key 987.6 whose uses is LINE'))
    c.append(('F04a_new_md_file', TF, newfile('APPENDIX_R2.md', LINE + '\n'), None, 'attack', 'new .md file in the bundle folder'))
    c.append(('F04b_new_json_file', TF, newfile('EXTRA_R2.json', json.dumps({'note': LINE}) + '\n'), None, 'attack', 'new .json file in the bundle folder'))
    # INDEX L23 "query and node radii are verified against their bytes (T4)"
    c.append(('R1_node15_radius_10p54_to_10p55', TF, chain(edit(P, retoken('10.54', '10.55')), prov(rekey('10.54', '10.55'))), None, 'attack',
              'PREREG L174/L439 ring-15 radius changed to a value node 15 does not round to; still declared MODEL_DIAGNOSTIC'))
    c.append(('R2_node16_radius_10p91_to_10p92', TF, chain(edit(P, retoken('10.91', '10.92')), prov(rekey('10.91', '10.92'))), None, 'control',
              'declared NODE_RADIUS (node 16) changed: T4 should catch it'))
    c.append(('R3_fix_10p54_as_node_radius', TF, prov(recat('10.54', category='NODE_RADIUS', node_index=15)), None, 'fixprobe_pass',
              'fix probe: re-declare 10.54 as NODE_RADIUS node 15; should still PASS'))
    c.append(('R4_fix_10p55_as_node_radius', TF, chain(edit(P, retoken('10.54', '10.55')), prov(rekey('10.54', '10.55', category='NODE_RADIUS', node_index=15))), None, 'fixprobe_fail',
              'fix probe: with that category, the wrong value is caught'))
    c.append(('R5_node_derived_10p22_to_10p23', TF, chain(edit(R, retoken('10.22', '10.23')), prov(rekey('10.22', '10.23'))), None, 'info',
              'NODE_DERIVED midpoint changed; not a query or node radius, so not an INDEX L23 over-claim'))
    # INDEX L24 "every pinned source hashes as stated, with the open V005 pinned per entry (T5)"
    c.append(('E1_control_a66_edited', TF, None, v005_case(a66_edit), 'control', 'A66 section edited in the V005 copy; honest pin row'))
    c.append(('E2_a66_edited_pin_row_trailing_space', TF, edit(P, trailing_space_on_pin(66)), v005_case(a66_edit), 'attack',
              'A66 edited; the A66 pin row has one trailing space and is skipped'))
    # INDEX L26 "T7 reports V005 entries added after assembly"
    c.append(('T0_reviewed_list_A91_A100', CU, edit(P, lambda t: t.replace(NC_OLD, 'A91–A100. From V005', 1)), None, 'baseline',
              'no-change list extended to the snapshot headings; currency should PASS'))
    c.append(('T1_control_new_h2_entry', CU, edit(P, lambda t: t.replace(NC_OLD, 'A91–A100. From V005', 1)), v005_case(insert_heading('## A101: synthetic')), 'control',
              'a new standard heading A101 is reported'))
    c.append(('T2_new_h3_entry', CU, edit(P, lambda t: t.replace(NC_OLD, 'A91–A100. From V005', 1)), v005_case(insert_heading('### A101: synthetic')), 'attack',
              'a new level-3 heading A101 is not seen'))
    c.append(('T3_open_range', CU, edit(P, lambda t: t.replace(NC_OLD, 'A91–A199. From V005', 1)), v005_case(insert_heading('## A101: synthetic')), 'attack',
              'an open-ended no-change range hides A101'))
    return c


def scan_t1_t3(T, text):
    t = T.norm(text)
    low = t.lower()
    hits = ['term %r' % w for w in T.FORBIDDEN if w in low]
    hits += ['ext %r' % m.group(0) for m in T.FORBIDDEN_EXT.finditer(t)]
    hits += ['vel %r' % m.group(0) for m in T.VEL.finditer(t)]
    hits += ['sym %r' % m.group(0) for m in T.SYM.finditer(t)]
    return hits


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--work', required=True)
    ap.add_argument('--snap', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    out = {'schema': 'VTF2_R2C_S1_REPRODUCTION_V001', 'object': OBJ}

    # 1. object bytes against HASHES_R2.txt
    hashes = {}
    for line in rd(os.path.join(OBJ, 'HASHES_R2.txt')).splitlines():
        h, name = line.split('  ', 1)
        hashes[name] = h
    got = {n: sha_b(open(os.path.join(OBJ, n), 'rb').read()) for n in hashes}
    out['object_hashes_match'] = all(got[n] == hashes[n] for n in hashes)
    out['object_hashes'] = got
    assert out['object_hashes_match']

    # 2. V005 snapshot from bytes
    vb = open(LIVE_V005, 'rb').read()
    with open(a.snap, 'xb') as f:
        f.write(vb)
    out['v005_snapshot'] = {'path': a.snap, 'sha256': sha_b(vb), 'bytes': len(vb)}

    sys.path.insert(0, os.path.join(OBJ, 'tools'))
    import check_target_free_c4v002 as T
    orig = T.sources_from_section11

    def patched(text):
        return [(l, (STATE['v005'] if l == 'decisions V005' else p), h) for l, p, h in orig(text)]
    T.sources_from_section11 = patched

    def run_check(d):
        class A:
            pass
        x = A()
        x.dir, x.provenance, x.slots, x.expect_slots_sha = d, os.path.join(d, N), SLOTS, SLOTS_SHA
        x.nodes, x.expect_nodes_sha = NODES, NODES_SHA
        return T.run(x)

    os.makedirs(a.work)
    out['cases'] = []
    for cid, kind, fn, vfn, role, note in cases():
        d = os.path.join(a.work, cid)
        os.makedirs(d)
        for n in BUNDLE:
            shutil.copyfile(os.path.join(OBJ, n), os.path.join(d, n))
        if fn:
            fn(d)
        STATE['v005'] = vfn(d, a.snap) if vfn else a.snap
        r = run_check(d)
        STATE['v005'] = a.snap
        failed = sorted(k for k, v in r['checks'].items() if not v['pass'])
        verdict = r['verdict_target_free'] if kind == 'target_free' else r['verdict_currency']
        t4 = r['checks']['T4_NUMBER_PROVENANCE']
        t5 = r['checks']['T5_SOURCES_TARGET_FREE_AND_PINNED']
        rec = {'case': cid, 'kind': kind, 'role': role, 'note': note, 'verdict_target_free': r['verdict_target_free'],
               'verdict_currency': r['verdict_currency'], 'failed_checks': failed, 'verdict_of_kind': verdict,
               'files_changed': [n for n in BUNDLE if open(os.path.join(d, n), 'rb').read() != open(os.path.join(OBJ, n), 'rb').read()],
               'extra_files': sorted(set(os.listdir(d)) - set(BUNDLE)),
               'T1_T3_hits': {k: r['checks'][k]['hits'] for k in ('T1_FORBIDDEN_TERMS', 'T2_NO_VELOCITY_VALUE', 'T3_NO_TARGET_SYMBOL_VALUE') if r['checks'][k]['hits']},
               'T4_missing': t4['missing_from_provenance'], 'T4_listed_but_absent': t4['listed_but_absent'], 'T4_radius_mismatch': t4['radius_mismatch'],
               'T5_problems': t5['problems'], 'T5_entries_checked': [e['entry'] for e in t5['v005_entries']],
               'T7_later': r['checks']['T7_V005_CURRENCY'].get('later_entries_needing_a_revision_or_no_change_note')}
        expect = {'baseline': 'PASS', 'control': 'FAIL', 'attack': 'FAIL', 'fixprobe_pass': 'PASS', 'fixprobe_fail': 'FAIL', 'info': None}[role]
        rec['should_be'] = expect
        rec['behaves_as_it_should'] = None if expect is None else (verdict == expect)
        rec['false_negative'] = (verdict == 'PASS') if role == 'attack' else None
        out['cases'].append(rec)

    # 3. T1-T3 over every file of the bundle (what "any text file" would mean bundle-wide)
    bw = {}
    for n in sorted(hashes):
        hits = scan_t1_t3(T, open(os.path.join(OBJ, n), 'rb').read().decode('utf-8'))
        bw[n] = {'n_hits': len(hits), 'first_hits': hits[:6], 'scanned_by_check': n in T.TEXT_FILES}
    out['bundle_wide_T1_T3'] = bw

    # 4. what T4 would report if INDEX were also scanned
    prov_doc = json.loads(rd(os.path.join(OBJ, N)))
    itoks = sorted(set(T.numeric_tokens(rd(os.path.join(OBJ, I)))), key=lambda x: (float(x), x))
    out['index_numeric_tokens'] = itoks
    out['index_tokens_not_in_provenance'] = [x for x in itoks if x not in prov_doc['numbers']]

    # 5. section-11 row census of the real PREREG: is every sha-bearing row parsed?
    s11 = T.section(rd(os.path.join(OBJ, P)), '11.')
    lines = s11.splitlines()
    sha_lines = [l for l in lines if re.search(r'[0-9a-f]{64}', l)]
    a_rows = [l for l in sha_lines if re.match(r'^\| A\d{1,3} \|', l)]
    pins = T.v005_entry_pins(rd(os.path.join(OBJ, P)))
    srcs = orig(rd(os.path.join(OBJ, P)))
    out['section11_census'] = {
        'lines_with_64hex': len(sha_lines), 'a_rows': len(a_rows), 'a_rows_parsed_as_pins': len(pins),
        'non_a_lines_with_64hex': len(sha_lines) - len(a_rows), 'sources_parsed': len(srcs),
        'sources_unparsed_or_ambiguous': [s for s in srcs if s[0] == 'UNPARSED' or s[1].startswith(('AMBIGUOUS', 'UNPARSED'))],
        'lines_with_unbackticked_64hex': [l[:120] for l in sha_lines if not re.search(r'`[0-9a-f]{64}`', l)],
        'pins_with_end_marker': [(n, mk) for n, mk, _ in pins if mk]}

    # 6. heading forms in the real V005 snapshot
    vt = vb.decode('utf-8')
    loose = re.compile(r'^\s{0,3}(?:#{1,6}\s*|\*\*\s*)(?:entry\s+)?A\s?\d{1,3}', re.I | re.M)
    loose_lines = [m.group(0) for m in loose.finditer(vt)]
    t7_heads = T.all_headings(vt)
    t5_heads = sorted(T.entry_sections(vt).keys())
    nonstd = [l for l in vt.split('\n') if loose.match(l) and not re.match(r'^## A\d{1,3}:', l)]
    out['v005_heading_census'] = {'loose_heading_like_lines': len(loose_lines), 'T7_all_headings': len(t7_heads),
                                  'T7_unique': len(set(t7_heads)), 'entry_sections_keys': len(t5_heads),
                                  'max_heading': max(t7_heads), 'nonstandard_heading_like_lines': [l[:100] for l in nonstd],
                                  'duplicates': sorted({x for x in t7_heads if t7_heads.count(x) > 1})}
    base = [x for x in out['cases'] if x['case'] == 'BASE'][0]
    out['baseline_T7_later'] = base['T7_later']
    atk = [x for x in out['cases'] if x['role'] == 'attack']
    out['summary'] = {'n_cases': len(out['cases']), 'n_attack': len(atk), 'n_attack_false_negative': sum(1 for x in atk if x['false_negative']),
                      'controls_and_baselines_ok': all(x['behaves_as_it_should'] for x in out['cases'] if x['role'] in ('control', 'baseline')),
                      'fixprobes_ok': all(x['behaves_as_it_should'] for x in out['cases'] if x['role'].startswith('fixprobe'))}
    with open(a.out, 'x', encoding='utf-8') as f:
        f.write(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
    for x in out['cases']:
        print('%-42s %-13s %-11s tf=%-4s cur=%-4s should=%-4s ok=%-5s FN=%-5s %s' % (
            x['case'], x['role'], x['kind'], x['verdict_target_free'], x['verdict_currency'], x['should_be'], x['behaves_as_it_should'],
            x['false_negative'], ','.join(k.split('_')[0] for k in x['failed_checks'])))
    print(json.dumps(out['summary']))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
