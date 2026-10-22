# Claude4 (dispatch 0585): the target-free check v002 must FAIL on each kind of violation, so its PASS is not vacuous.
# Mutated copies of a built r2 folder are written into a fresh scratch folder (--work, must not exist). An audit hook allows writes only
# under --work and refuses target-like opens, processes, network and deletes. Sentinel values are deliberately implausible and use a
# query id that does not exist (NGC3198-Q99), so the bundle carries nothing that reads as a plausible target value.
# usage: python3 -I -B test_check_target_free_c4v002.py --built R2DIR --work NEW_SCRATCH_DIR
import argparse, json, os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_target_free_c4v002 as T

SLOTS = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json'
SLOTS_SHA = 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'
NODES = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json'
NODES_SHA = 'ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d'
P, M, R, N = 'PREREG_MISS_READING_R2.md', 'CLAUSE_SOURCE_MAP_R2.md', 'ROOT_ITEMS_R2.md', 'NUMBER_PROVENANCE_R2.json'
ANCHOR = '## 0. Invariants'
_WORK = []


def _hook(event, args):
    if event == 'open':
        path = args[0]
        if isinstance(path, int):
            return
        p = os.fsdecode(path) if isinstance(path, bytes) else str(path)
        low = p.lower()
        if any(w in low for w in T.FORBIDDEN) or any(w in low for w in T._PROTECT):
            raise PermissionError('target-like path refused: %s' % p)
        mode = args[1] if len(args) > 1 and isinstance(args[1], str) else 'r'
        flags = args[2] if len(args) > 2 and isinstance(args[2], int) else 0
        writing = any(c in mode for c in 'wax+') or (flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND))
        if writing and not any(os.path.abspath(p).startswith(w + os.sep) for w in _WORK):
            raise PermissionError('write outside the work folder refused: %s' % p)
    elif event in ('os.remove', 'os.rmdir', 'shutil.rmtree', 'subprocess.Popen', 'os.system', 'os.posix_spawn', 'socket.connect'):
        raise PermissionError('refused: %s' % event)


def mutate_text(name, fn):
    def f(d):
        p = os.path.join(d, name)
        t = open(p, encoding='utf-8').read()
        t2 = fn(t)
        assert t2 != t, 'mutation did not change ' + name
        open(p, 'w', encoding='utf-8').write(t2)
    return f


def inject(name, line):
    return mutate_text(name, lambda t: t.replace(ANCHOR, line + '\n\n' + ANCHOR, 1) if ANCHOR in t else t + '\n' + line + '\n')


def mutate_prov(fn):
    def f(d):
        p = os.path.join(d, N)
        doc = json.load(open(p, encoding='utf-8'))
        fn(doc)
        open(p, 'w', encoding='utf-8').write(json.dumps(doc, indent=1, ensure_ascii=False) + '\n')
    return f


def first_v005_pin(t):
    m = re.search(r'^(\| A\d{1,3} \|[^\n]*`)([0-9a-f])([0-9a-f]{63})(` \|)$', t, re.M)
    flip = '0' if m.group(2) != '0' else '1'
    return t[:m.start()] + m.group(1) + flip + m.group(3) + m.group(4) + t[m.end():]


def change_end_marker(t):
    return t.replace('| `**Lanes.**` |', '| `**Nonexistent marker.**` |', 1)


def drop_from_no_change(t):
    m = re.search(r'(\*\*Read with no change to this text:\*\*\s*)(A\d{1,3}(?:[–-]A\d{1,3})?)(, )', t)
    assert m, 'no-change list not found'
    return t[:m.start(2)] + t[m.end(3):]


CASES = [
    ('velocity_value', inject(P, 'The quoted value at NGC3198-Q99 is 987654.321 km/s.'), {'T2_NO_VELOCITY_VALUE', 'T4_NUMBER_PROVENANCE'}),
    ('velocity_unit_variant', inject(P, 'A value of 987654 km s⁻¹ appears.'), {'T2_NO_VELOCITY_VALUE'}),
    ('velocity_unicode_digits', inject(P, 'A value of ９８７６５４ km/s appears.'), {'T2_NO_VELOCITY_VALUE'}),
    ('velocity_in_root_items', inject(R, 'Root saw 987654.321 km/s.'), {'T2_NO_VELOCITY_VALUE', 'T4_NUMBER_PROVENANCE'}),
    ('target_symbol_value', inject(P, 'Here v_q = 999999 for NGC3198-Q99.'), {'T3_NO_TARGET_SYMBOL_VALUE', 'T4_NUMBER_PROVENANCE'}),
    ('target_symbol_vrot', inject(M, 'Note: v_rot ≈ 999999.'), {'T3_NO_TARGET_SYMBOL_VALUE', 'T4_NUMBER_PROVENANCE'}),
    ('forbidden_term', inject(P, 'See the rotmod table.'), {'T1_FORBIDDEN_TERMS'}),
    ('forbidden_term_unicode', inject(P, 'See the ＳＰＡＲＣ catalogue.'), {'T1_FORBIDDEN_TERMS'}),
    ('forbidden_term_zero_width', inject(M, 'See the rot​mod file.'), {'T1_FORBIDDEN_TERMS'}),
    ('forbidden_extension_tsv', inject(R, 'See targets_q99.tsv.'), {'T1_FORBIDDEN_TERMS'}),
    ('unlisted_number', inject(P, 'A quantity of 765432.1 appears here.'), {'T4_NUMBER_PROVENANCE'}),
    ('number_in_code_span', inject(P, 'The value is `876543.21` here.'), {'T4_NUMBER_PROVENANCE'}),
    ('long_digit_run', inject(P, 'Run id 98765432 here.'), {'T4_NUMBER_PROVENANCE'}),
    ('unlisted_number_in_map', inject(M, 'A quantity of 765432.1 appears here.'), {'T4_NUMBER_PROVENANCE'}),
    ('radius_wrong_id', mutate_prov(lambda d: d['numbers']['9.04'].update(query_ids=['NGC3198-Q23'])), {'T4_NUMBER_PROVENANCE'}),
    ('node_radius_wrong_index', mutate_prov(lambda d: d['numbers']['9.90'].update(node_index=13)), {'T4_NUMBER_PROVENANCE'}),
    ('bad_category', mutate_prov(lambda d: d['numbers']['43'].update(category='FROM_TARGETS')), {'T4_NUMBER_PROVENANCE'}),
    ('v005_entry_pin_changed', mutate_text(P, first_v005_pin), {'T5_SOURCES_TARGET_FREE_AND_PINNED'}),
    ('v005_end_marker_changed', mutate_text(P, change_end_marker), {'T5_SOURCES_TARGET_FREE_AND_PINNED'}),
    ('dispatch_sha_changed', mutate_text(P, lambda t: t.replace('`0748fb2091a66d0671c478535a3b4c19ee216cc6be6ce4134a26c264f0861279`', '`1748fb2091a66d0671c478535a3b4c19ee216cc6be6ce4134a26c264f0861279`', 1)), {'T5_SOURCES_TARGET_FREE_AND_PINNED'}),
    ('duplicate_tag', mutate_text(P, lambda t: t.replace('### 1.2 Sign [C-1.2]', '### 1.2 Sign [C-1.2] [C-1.3]', 1)), {'T6_CLAUSE_TAGS_MAPPED'}),
    ('unmapped_tag', mutate_text(P, lambda t: t.replace('### 1.2 Sign [C-1.2]', '### 1.2 Sign [C-1.2] [C-9.9]', 1)), {'T6_CLAUSE_TAGS_MAPPED'}),
    ('map_row_without_tag', mutate_text(M, lambda t: t.replace('| C-P |', '| C-ZZ | phantom | — | NEW | none |\n| C-P |', 1)), {'T6_CLAUSE_TAGS_MAPPED'}),
    ('later_entry_uncovered', mutate_text(P, drop_from_no_change), {'T7_V005_CURRENCY'}),
]


def check(d, slots_sha=SLOTS_SHA, nodes_sha=NODES_SHA):
    class A:
        pass
    a = A()
    a.dir, a.provenance, a.slots, a.expect_slots_sha = d, os.path.join(d, N), SLOTS, slots_sha
    a.nodes, a.expect_nodes_sha = NODES, nodes_sha
    return T.run(a)


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--built', required=True)
    ap.add_argument('--work', required=True)
    a = ap.parse_args()
    os.makedirs(a.work)
    _WORK.append(os.path.abspath(a.work))
    sys.addaudithook(_hook)
    out = {'baseline_target_free': None, 'baseline_currency': None, 'cases': []}
    base = check(a.built)
    out['baseline_target_free'], out['baseline_currency'] = base['verdict_target_free'], base['verdict_currency']
    ok = base['verdict_target_free'] == 'PASS' and base['verdict_currency'] == 'PASS'
    for i, (name, fn, expect) in enumerate(CASES):
        d = os.path.join(a.work, '%02d_%s' % (i, name))
        os.makedirs(d)
        for n in (P, M, R, N):
            shutil.copyfile(os.path.join(a.built, n), os.path.join(d, n))
        fn(d)
        r = check(d)
        failed = {k for k, v in r['checks'].items() if not v['pass']}
        good = expect <= failed
        ok &= good
        out['cases'].append({'case': name, 'verdict_target_free': r['verdict_target_free'], 'verdict_currency': r['verdict_currency'],
                             'failed_checks': sorted(failed), 'expected_at_least': sorted(expect), 'ok': good})
    for name, kw in (('slots_sha_expected_wrong', {'slots_sha': '0' * 64}), ('nodes_sha_expected_wrong', {'nodes_sha': '0' * 64})):
        d = os.path.join(a.work, '99_' + name)
        os.makedirs(d)
        for n in (P, M, R, N):
            shutil.copyfile(os.path.join(a.built, n), os.path.join(d, n))
        r = check(d, **kw)
        good = not r['checks']['T4_NUMBER_PROVENANCE']['pass']
        ok &= good
        out['cases'].append({'case': name, 'verdict_target_free': r['verdict_target_free'], 'ok': good})
    out['all_ok'] = bool(ok)
    out['n_cases'] = len(out['cases'])
    print(json.dumps(out, indent=1))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
