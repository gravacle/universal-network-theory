# Claude4 (dispatch 0585) generator for the miss-reading prereg r2. It reads the draft folder, fills the open-V005 pins from the
# addendum's current bytes, writes every file into --out with exclusive create (a new, empty folder), runs the target-free check
# on the written bytes, and writes INDEX and HASHES. It opens no target data, launches nothing and overwrites nothing.
# It also runs the mutation test (each violation kind must FAIL) on mutated copies in --mutation-work (a new scratch folder outside --out).
# usage: python3 -I -B make_miss_reading_c4v002.py --draft DRAFT_DIR --out NEW_DIR --label LABEL --mutation-work NEW_SCRATCH_DIR
import argparse, hashlib, json, os, re, shutil, sys

V005 = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/'
        'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md')
SLOTS = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json'
SLOTS_SHA = 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'
CITED = [
    (48, 'the governing principle: where the text is silent, the stricter reading'),
    (56, 'the 0531 roster-binding ruling (v003f B1)'),
    (60, 'gap rows; cut binding; the V001 summary and its open root items'),
    (62, 'the two-pass freeze procedure'),
    (63, 'the stage-0 outcome; the SUPPORTED k = 0 drift reading; R-DRIFT; the disclosure'),
    (64, 'the C1′ scope; NGC K_big 32; N3′; coverage 91'),
    (65, 'STAGE0_GRID_OUTER; the grid differences; check R-3; the disclosure (its trailing block also logs the 0518 contract)'),
    (66, 'the N1 consequence; TRUNCATION_SHAPE_RESIDUAL; R-TSR'),
    (70, 'the v003g PASS note ("Step 6\'s freeze code is ready")'),
    (81, 'RI-22, the DOUBLING NGC half; RI-23, the M_s 128 condition, slotting and LO_NGC'),
    (82, 'V005 closes at the freeze'),
]
FILES = ('PREREG_MISS_READING_R2.md', 'CLAUSE_SOURCE_MAP_R2.md', 'ROOT_ITEMS_R2.md', 'NUMBER_PROVENANCE_R2.json')
TOOLS = ('check_target_free_c4v001.py', 'test_check_target_free_c4v001.py', 'make_miss_reading_c4v002.py')


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def main():
    p = argparse.ArgumentParser(allow_abbrev=False)
    p.add_argument('--draft', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--label', required=True)
    p.add_argument('--mutation-work', required=True)
    a = p.parse_args()
    out = os.path.abspath(a.out)
    os.makedirs(out)                      # must not exist yet
    os.makedirs(os.path.join(out, 'tools'))
    sys.path.insert(0, os.path.join(a.draft, 'tools'))
    import check_target_free_c4v001 as T

    v_bytes = open(V005, 'rb').read()
    v_text = v_bytes.decode('utf-8')
    secs = T.entry_sections(v_text)
    rows = []
    for n, use in CITED:
        assert len(secs.get(n, [])) == 1, 'A%d heading count %d' % (n, len(secs.get(n, [])))
        rows.append('| A%d | %s | `%s` |' % (n, use, sha_bytes(secs[n][0].encode('utf-8'))))
    last = max(secs)
    texts = {}
    for name in FILES:
        texts[name] = open(os.path.join(a.draft, name), 'rb').read().decode('utf-8')
    t = texts['PREREG_MISS_READING_R2.md']
    for ph, val in (('@@V005_SHA@@', sha_bytes(v_bytes)), ('@@V005_ENTRY_ROWS@@', '\n'.join(rows)), ('@@V005_LAST@@', 'A%d' % last)):
        assert t.count(ph) == 1, ph
        t = t.replace(ph, val)
    assert '@@' not in t
    texts['PREREG_MISS_READING_R2.md'] = t
    for name in FILES:
        with open(os.path.join(out, name), 'x', encoding='utf-8') as f:
            f.write(texts[name])
    for name in TOOLS:
        src = os.path.join(a.draft, 'tools', name)
        with open(os.path.join(out, 'tools', name), 'xb') as f:
            f.write(open(src, 'rb').read())

    class Args:
        pass
    ca = Args()
    ca.dir, ca.provenance, ca.slots, ca.expect_slots_sha = out, os.path.join(out, 'NUMBER_PROVENANCE_R2.json'), SLOTS, SLOTS_SHA
    res = T.run(ca)
    chk = json.dumps(res, indent=1, sort_keys=True, ensure_ascii=False) + '\n'
    with open(os.path.join(out, 'TARGET_FREE_CHECK_R2.json'), 'x', encoding='utf-8') as f:
        f.write(chk)
    import io, contextlib
    import test_check_target_free_c4v001 as MT
    buf = io.StringIO()
    saved = sys.argv
    sys.argv = ['test_check_target_free_c4v001.py', '--built', out, '--work', os.path.abspath(a.mutation_work)]
    with contextlib.redirect_stdout(buf):
        mt_rc = MT.main()
    sys.argv = saved
    mt = json.loads(buf.getvalue())
    with open(os.path.join(out, 'TARGET_FREE_MUTATION_TEST_R2.json'), 'x', encoding='utf-8') as f:
        f.write(json.dumps(mt, indent=1, sort_keys=True) + '\n')

    def h(name):
        return sha_bytes(open(os.path.join(out, name), 'rb').read())
    idx = [
        '# INDEX_R2 (%s) — miss-reading prereg r2, Claude4, dispatch 0585' % a.label, '',
        'Built by `tools/make_miss_reading_c4v002.py` from the draft folder, with exclusive create into a new folder.',
        'The V005 per-entry pins in section 11 of the prereg were read from the addendum bytes at assembly.', '',
        '| file | role | sha256 |', '|---|---|---|',
        '| PREREG_MISS_READING_R2.md | the prereg text r2 (unsealed) | `%s` |' % h('PREREG_MISS_READING_R2.md'),
        '| CLAUSE_SOURCE_MAP_R2.md | where each clause comes from, plus the 0585 coverage table | `%s` |' % h('CLAUSE_SOURCE_MAP_R2.md'),
        '| ROOT_ITEMS_R2.md | M-1 to M-12, each with a recommendation | `%s` |' % h('ROOT_ITEMS_R2.md'),
        '| NUMBER_PROVENANCE_R2.json | the target-free source of every numeric token in the prereg | `%s` |' % h('NUMBER_PROVENANCE_R2.json'),
        '| TARGET_FREE_CHECK_R2.json | the T1–T6 result on these bytes: **%s** | `%s` |' % (res['verdict'], h('TARGET_FREE_CHECK_R2.json')),
        '| TARGET_FREE_MUTATION_TEST_R2.json | the check FAILs on each of %d violation kinds (all_ok %s) | `%s` |' % (mt['n_cases'], mt['all_ok'], h('TARGET_FREE_MUTATION_TEST_R2.json')),
        '| tools/check_target_free_c4v001.py | the target-free check | `%s` |' % h('tools/check_target_free_c4v001.py'),
        '| tools/test_check_target_free_c4v001.py | the mutation test | `%s` |' % h('tools/test_check_target_free_c4v001.py'),
        '| tools/make_miss_reading_c4v002.py | this generator | `%s` |' % h('tools/make_miss_reading_c4v002.py'), '',
        'V005 at assembly: `%s` (last entry A%d).' % (sha_bytes(v_bytes), last), '',
        '**What the check proves, and what it does not.**',
        '- **Proved (by construction, from bytes):** the text names no target file, data source, velocity value or target symbol value (T1–T3).',
        '  - Every number in it has a target-free source (T4). The query radii are verified against the slots bytes.',
        '  - Every pinned source is target-free and hashes as stated (T5). The open V005 is pinned per entry.',
        '  - Every clause is mapped (T6).',
        '- **Not proved by the script:** that no rule depends on a target value. That is a semantic property.',
        '  - The rules use only frozen quantities, plus (v_q, sigma_q) inside the score output (I-2, I-3).',
        '  - The independent lens checks review this property.',
        '- **No target was ever opened.** The check cannot compare against target values; it never needs to.', '']
    with open(os.path.join(out, 'INDEX_R2.md'), 'x', encoding='utf-8') as f:
        f.write('\n'.join(idx))
    names = sorted(n for n in FILES) + ['INDEX_R2.md', 'TARGET_FREE_CHECK_R2.json', 'TARGET_FREE_MUTATION_TEST_R2.json'] + ['tools/' + n for n in TOOLS]
    with open(os.path.join(out, 'HASHES_R2.txt'), 'x', encoding='utf-8') as f:
        for n in names:
            f.write('%s  %s\n' % (h(n), n))
    print(json.dumps({'out': out, 'verdict': res['verdict'], 'v005_sha': sha_bytes(v_bytes), 'last': last,
                      'hashes': {n: h(n) for n in names}}, indent=1))
    return 0 if res['verdict'] == 'PASS' and mt['all_ok'] and mt_rc == 0 else 2


if __name__ == '__main__':
    raise SystemExit(main())
