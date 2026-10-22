# Claude4 (dispatch 0585): the target-free check must FAIL on each kind of violation (so its PASS is not vacuous).
# Mutated copies of a built r2 folder are written into a fresh scratch folder (--work, must not exist). Nothing else is written.
# usage: python3 -I -B test_check_target_free_c4v001.py --built R2DIR --work NEW_SCRATCH_DIR
import argparse, json, os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_target_free_c4v001 as T

SLOTS = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json'
SLOTS_SHA = 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'
P, M, R, N = 'PREREG_MISS_READING_R2.md', 'CLAUSE_SOURCE_MAP_R2.md', 'ROOT_ITEMS_R2.md', 'NUMBER_PROVENANCE_R2.json'


def mutate_text(name, fn):
    def f(d):
        p = os.path.join(d, name)
        t = open(p, encoding='utf-8').read()
        t2 = fn(t)
        assert t2 != t, 'mutation did not change ' + name
        open(p, 'w', encoding='utf-8').write(t2)
    return f


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


CASES = [
    ('velocity_value', mutate_text(P, lambda t: t.replace('## 0. Invariants', 'The quoted value is 150.2 km/s.\n\n## 0. Invariants', 1)), {'T2_NO_VELOCITY_VALUE', 'T4_NUMBER_PROVENANCE'}),
    ('target_symbol_value', mutate_text(P, lambda t: t.replace('## 0. Invariants', 'Here v_q = 151 for Q40.\n\n## 0. Invariants', 1)), {'T3_NO_TARGET_SYMBOL_VALUE', 'T4_NUMBER_PROVENANCE'}),
    ('forbidden_term', mutate_text(P, lambda t: t.replace('## 0. Invariants', 'See the rotmod table.\n\n## 0. Invariants', 1)), {'T1_FORBIDDEN_TERMS'}),
    ('forbidden_term_in_map', mutate_text(M, lambda t: t + '\nSource: the SPARC catalogue.\n'), {'T1_FORBIDDEN_TERMS'}),
    ('forbidden_extension', mutate_text(R, lambda t: t + '\nSee NGC3198_table.dat.\n'), {'T1_FORBIDDEN_TERMS'}),
    ('unlisted_number', mutate_text(P, lambda t: t.replace('## 0. Invariants', 'A quantity of 147.3 appears here.\n\n## 0. Invariants', 1)), {'T4_NUMBER_PROVENANCE'}),
    ('radius_wrong_id', mutate_prov(lambda d: d['numbers']['9.04'].update(query_ids=['NGC3198-Q23'])), {'T4_NUMBER_PROVENANCE'}),
    ('bad_category', mutate_prov(lambda d: d['numbers']['43'].update(category='FROM_TARGETS')), {'T4_NUMBER_PROVENANCE'}),
    ('v005_entry_pin_changed', mutate_text(P, first_v005_pin), {'T5_SOURCES_TARGET_FREE_AND_PINNED'}),
    ('dispatch_sha_changed', mutate_text(P, lambda t: t.replace('`0748fb2091a66d0671c478535a3b4c19ee216cc6be6ce4134a26c264f0861279`', '`1748fb2091a66d0671c478535a3b4c19ee216cc6be6ce4134a26c264f0861279`', 1)), {'T5_SOURCES_TARGET_FREE_AND_PINNED'}),
    ('duplicate_tag', mutate_text(P, lambda t: t.replace('### 1.2 Sign [C-1.2]', '### 1.2 Sign [C-1.2] [C-1.3]', 1)), {'T6_CLAUSE_TAGS_MAPPED'}),
    ('unmapped_tag', mutate_text(P, lambda t: t.replace('### 1.2 Sign [C-1.2]', '### 1.2 Sign [C-1.2] [C-9.9]', 1)), {'T6_CLAUSE_TAGS_MAPPED'}),
    ('map_row_without_tag', mutate_text(M, lambda t: t.replace('| C-P |', '| C-ZZ | phantom | — | NEW | none |\n| C-P |', 1)), {'T6_CLAUSE_TAGS_MAPPED'}),
]


def check(d, slots_sha=SLOTS_SHA):
    class A:
        pass
    a = A()
    a.dir, a.provenance, a.slots, a.expect_slots_sha = d, os.path.join(d, N), SLOTS, slots_sha
    return T.run(a)


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--built', required=True)
    ap.add_argument('--work', required=True)
    a = ap.parse_args()
    os.makedirs(a.work)
    out = {'baseline': None, 'cases': []}
    base = check(a.built)
    out['baseline'] = base['verdict']
    ok = base['verdict'] == 'PASS'
    for i, (name, fn, expect) in enumerate(CASES):
        d = os.path.join(a.work, '%02d_%s' % (i, name))
        os.makedirs(d)
        for n in (P, M, R, N):
            shutil.copyfile(os.path.join(a.built, n), os.path.join(d, n))
        fn(d)
        r = check(d)
        failed = {k for k, v in r['checks'].items() if not v['pass']}
        good = r['verdict'] == 'FAIL' and expect <= failed
        ok &= good
        out['cases'].append({'case': name, 'verdict': r['verdict'], 'failed_checks': sorted(failed), 'expected_at_least': sorted(expect), 'ok': good})
    d = os.path.join(a.work, '99_slots_sha_expected_wrong')
    os.makedirs(d)
    for n in (P, M, R, N):
        shutil.copyfile(os.path.join(a.built, n), os.path.join(d, n))
    r = check(d, slots_sha='0' * 64)
    good = r['verdict'] == 'FAIL' and not r['checks']['T4_NUMBER_PROVENANCE']['pass']
    ok &= good
    out['cases'].append({'case': 'slots_sha_expected_wrong', 'verdict': r['verdict'], 'ok': good})
    out['all_ok'] = bool(ok)
    out['n_cases'] = len(out['cases'])
    print(json.dumps(out, indent=1))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
