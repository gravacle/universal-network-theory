# Claude4 (dispatch 0585) generator v003 for the miss-reading prereg r2, round 2.
# It reads the draft folder, fills the dispatch and open-V005 pins from current bytes, and writes every file into --out (a new folder)
# with exclusive create. It then runs the target-free check v002 and the mutation test v002 as separate processes, each with its own
# audit hook, and writes INDEX and HASHES. It opens no target data, launches nothing and overwrites nothing.
# usage: python3 -I -B make_miss_reading_c4v003.py --draft DRAFT_DIR --out NEW_DIR --label LABEL --mutation-work NEW_SCRATCH_DIR
import argparse, hashlib, json, os, subprocess, sys

PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
V005 = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/'
        'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md')
DISPATCH_DIR = '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/'
SLOTS = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json'
SLOTS_SHA = 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'
NODES = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json'
NODES_SHA = 'ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d'
CITED = [
    (48, 'the governing principle: where the text is silent, the stricter reading', ''),
    (50, 'the PROVISIONAL rule (used by analogy in I-7)', ''),
    (52, 'item 4: LO_NGC is the readout-coupled share; NGC I1-T before any NGC N-test is read', ''),
    (56, 'the 0531 roster-binding ruling (v003f B1)', ''),
    (60, 'gap rows; cut binding; the V001 summary and its open root items', ''),
    (62, 'the two-pass freeze procedure', ''),
    (63, 'the stage-0 outcome; the SUPPORTED k = 0 drift reading; R-DRIFT; the disclosure', ''),
    (64, 'the C1′ scope; NGC K_big 32; N3′; coverage 91; N1 on production records', ''),
    (65, 'STAGE0_GRID_OUTER; the grid differences and single-chain range; check R-3; the disclosure', '**Lanes.**'),
    (66, 'the N1 consequence; TRUNCATION_SHAPE_RESIDUAL; R-TSR', ''),
    (70, 'the v003g PASS note ("Step 6\'s freeze code is ready")', ''),
    (81, 'RI-22, the DOUBLING NGC half; RI-23, the M_s 128 condition, slotting and LO_NGC', ''),
    (82, 'V005 closes at the freeze', ''),
    (90, 'the formal K32 N-test result (N_FAIL_N1, gate OPEN); LO_NGC_K32_CERT_V001 coverage to 91; the step-5 LO I1-T item', ''),
]
FILES = ('PREREG_MISS_READING_R2.md', 'CLAUSE_SOURCE_MAP_R2.md', 'ROOT_ITEMS_R2.md', 'NUMBER_PROVENANCE_R2.json')
TOOLS = ('check_target_free_c4v002.py', 'test_check_target_free_c4v002.py', 'make_miss_reading_c4v003.py')


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
    import check_target_free_c4v002 as T

    v_bytes = open(V005, 'rb').read()
    v_text = v_bytes.decode('utf-8')
    markers = {n: mk for n, _, mk in CITED if mk}
    secs = T.entry_sections(v_text, markers)
    rows = []
    for n, use, mk in CITED:
        got = secs.get(n, [])
        assert len(got) == 1 and got[0] is not None, 'A%d heading/marker problem' % n
        rows.append('| A%d | %s | %s | `%s` |' % (n, use, ('`%s`' % mk) if mk else 'next heading', sha_bytes(got[0].encode('utf-8'))))
    heads = sorted(set(x for x in T.all_headings(v_text) if x >= 47))
    cited_n = {n for n, _, _ in CITED}
    unc = [n for n in heads if n not in cited_n]
    runs, cur = [], []
    for n in unc:
        if cur and n == cur[-1] + 1:
            cur.append(n)
        else:
            if cur:
                runs.append(cur)
            cur = [n]
    if cur:
        runs.append(cur)
    uncited_text = ', '.join(('A%d' % r[0]) if len(r) == 1 else ('A%d–A%d' % (r[0], r[-1])) for r in runs)

    def dsha(num):
        names = [x for x in os.listdir(DISPATCH_DIR) if x.startswith(num + '_')]
        assert len(names) == 1, num
        return sha_bytes(open(os.path.join(DISPATCH_DIR, names[0]), 'rb').read())

    texts = {name: open(os.path.join(a.draft, name), 'rb').read().decode('utf-8') for name in FILES}
    t = texts['PREREG_MISS_READING_R2.md']
    fills = [('@@V005_SHA@@', sha_bytes(v_bytes)), ('@@V005_ENTRY_ROWS@@', '\n'.join(rows)), ('@@V005_UNCITED@@', uncited_text),
             ('@@SHA_0519@@', dsha('0519')), ('@@SHA_0521@@', dsha('0521')), ('@@SHA_0523@@', dsha('0523'))]
    for ph, val in fills:
        assert t.count(ph) == 1, ph
        t = t.replace(ph, val)
    assert '@@' not in t
    texts['PREREG_MISS_READING_R2.md'] = t
    for name in FILES:
        with open(os.path.join(out, name), 'x', encoding='utf-8') as f:
            f.write(texts[name])
    for name in TOOLS:
        with open(os.path.join(out, 'tools', name), 'xb') as f:
            f.write(open(os.path.join(a.draft, 'tools', name), 'rb').read())

    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1')
    chk_out = os.path.join(out, 'TARGET_FREE_CHECK_R2.json')
    rc_chk = subprocess.run([PY, '-I', '-B', os.path.join(out, 'tools', 'check_target_free_c4v002.py'), '--dir', out,
                             '--provenance', os.path.join(out, 'NUMBER_PROVENANCE_R2.json'), '--slots', SLOTS, '--expect-slots-sha', SLOTS_SHA,
                             '--nodes', NODES, '--expect-nodes-sha', NODES_SHA, '--out', chk_out],
                            env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    res = json.load(open(chk_out, encoding='utf-8'))
    mt = subprocess.run([PY, '-I', '-B', os.path.join(out, 'tools', 'test_check_target_free_c4v002.py'), '--built', out,
                         '--work', os.path.abspath(a.mutation_work)], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    mtd = json.loads(mt.stdout)
    with open(os.path.join(out, 'TARGET_FREE_MUTATION_TEST_R2.json'), 'x', encoding='utf-8') as f:
        f.write(json.dumps(mtd, indent=1, sort_keys=True) + '\n')

    def h(name):
        return sha_bytes(open(os.path.join(out, name), 'rb').read())
    idx = [
        '# INDEX_R2 (%s) — miss-reading prereg r2, round 2. Claude4, dispatches 0585 and 0606' % a.label, '',
        'Built by `tools/make_miss_reading_c4v003.py` from the draft folder, with exclusive create into a new folder.',
        'The V005 per-entry pins and the uncited list in section 11 of the prereg were read from the addendum bytes at assembly.', '',
        '| file | role | sha256 |', '|---|---|---|',
        '| PREREG_MISS_READING_R2.md | the prereg text r2, round 2 (unsealed) | `%s` |' % h('PREREG_MISS_READING_R2.md'),
        '| CLAUSE_SOURCE_MAP_R2.md | where each clause comes from; 0585 and 0606 coverage; the round-1 closure table | `%s` |' % h('CLAUSE_SOURCE_MAP_R2.md'),
        '| ROOT_ITEMS_R2.md | M-1 to M-14, each with a recommendation | `%s` |' % h('ROOT_ITEMS_R2.md'),
        '| NUMBER_PROVENANCE_R2.json | the target-free source of every numeric token in the three text files | `%s` |' % h('NUMBER_PROVENANCE_R2.json'),
        '| TARGET_FREE_CHECK_R2.json | T1–T6 target-free: **%s**; T7 currency: **%s**; with the occurrence census | `%s` |' % (res['verdict_target_free'], res['verdict_currency'], h('TARGET_FREE_CHECK_R2.json')),
        '| TARGET_FREE_MUTATION_TEST_R2.json | the check FAILs on each of %d violation kinds (all_ok %s) | `%s` |' % (mtd['n_cases'], mtd['all_ok'], h('TARGET_FREE_MUTATION_TEST_R2.json')),
        '| tools/check_target_free_c4v002.py | the target-free check | `%s` |' % h('tools/check_target_free_c4v002.py'),
        '| tools/test_check_target_free_c4v002.py | the mutation test | `%s` |' % h('tools/test_check_target_free_c4v002.py'),
        '| tools/make_miss_reading_c4v003.py | this generator | `%s` |' % h('tools/make_miss_reading_c4v003.py'), '',
        'V005 at assembly: `%s` (headings up to A%d).' % (sha_bytes(v_bytes), max(heads)), '',
        '**What the check establishes, and what it does not.** It is a mechanical check, not a proof.',
        '- **Checked from bytes:**',
        '  - no target term, data-source name, data extension, velocity value or target symbol value appears in any text file (T1–T3);',
        '  - every numeric token is listed with a target-free source, and query and node radii are verified against their bytes (T4); the census lists every occurrence with context, for review;',
        '  - every pinned source hashes as stated, with the open V005 pinned per entry (T5);',
        '  - every clause is mapped (T6).',
        '  - T7 reports V005 entries added after assembly. That is currency, not target-freeness.',
        '- **Not established by the script:**',
        '  - that no rule depends on a target value. That is a semantic property, which the lens reviews check;',
        '  - that the self-declared provenance categories are right. Review checks them against the cited sources.',
        '- **No target was ever opened.** The check cannot compare against target values, and never needs to.', '']
    with open(os.path.join(out, 'INDEX_R2.md'), 'x', encoding='utf-8') as f:
        f.write('\n'.join(idx))
    names = sorted(FILES) + ['INDEX_R2.md', 'TARGET_FREE_CHECK_R2.json', 'TARGET_FREE_MUTATION_TEST_R2.json'] + ['tools/' + n for n in TOOLS]
    with open(os.path.join(out, 'HASHES_R2.txt'), 'x', encoding='utf-8') as f:
        for n in names:
            f.write('%s  %s\n' % (h(n), n))
    print(json.dumps({'out': out, 'target_free': res['verdict_target_free'], 'currency': res['verdict_currency'],
                      'mutation_all_ok': mtd['all_ok'], 'n_cases': mtd['n_cases'], 'check_stderr': rc_chk.stderr[-400:],
                      'missing_from_provenance': res['checks']['T4_NUMBER_PROVENANCE']['missing_from_provenance'],
                      'radius_mismatch': res['checks']['T4_NUMBER_PROVENANCE']['radius_mismatch'],
                      'problems_T5': res['checks']['T5_SOURCES_TARGET_FREE_AND_PINNED']['problems'],
                      'T6': {k: v for k, v in res['checks']['T6_CLAUSE_TAGS_MAPPED'].items() if k != 'pass' and v},
                      'T1': res['checks']['T1_FORBIDDEN_TERMS']['hits'], 'T2': res['checks']['T2_NO_VELOCITY_VALUE']['hits'],
                      'T3': res['checks']['T3_NO_TARGET_SYMBOL_VALUE']['hits'],
                      'failed_cases': [c['case'] for c in mtd['cases'] if not c['ok']], 'v005_sha': sha_bytes(v_bytes),
                      'hashes': {n: h(n) for n in names}}, indent=1))
    return 0 if res['verdict_target_free'] == 'PASS' and res['verdict_currency'] == 'PASS' and mtd['all_ok'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
