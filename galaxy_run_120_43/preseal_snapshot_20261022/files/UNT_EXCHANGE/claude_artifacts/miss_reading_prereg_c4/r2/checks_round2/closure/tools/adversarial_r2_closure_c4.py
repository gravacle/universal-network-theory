# R2-A closure lens: re-run round-1 lens B's 38 adversarial target-free cases (B-7, B-8, B-9 closure) against the ROUND-2
# check tool check_target_free_c4v002.py, plus a few round-2-specific variants. A case whose target-free verdict is PASS is
# a false negative. Synthetic sentinels only (987.6, 778 used as a listed stand-in, a fake id NGC3198-Q99/Q43 label only).
# The object is never edited: its four text/JSON files (and INDEX) are copied into a fresh --work dir in this lens folder.
# An audit hook refuses target-like/protected opens, processes, network and deletes, and any write outside --work/--out.
# usage: python3 -I -B adversarial_r2_closure_c4.py --round2 R2DIR --work NEW_DIR --out RESULT.json
import argparse, hashlib, json, os, shutil, sys

SLOTS = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json'
SLOTS_SHA = 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'
NODES = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json'
NODES_SHA = 'ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d'
P, M, R, N, I = 'PREREG_MISS_READING_R2.md', 'CLAUSE_SOURCE_MAP_R2.md', 'ROOT_ITEMS_R2.md', 'NUMBER_PROVENANCE_R2.json', 'INDEX_R2.md'
ANCHOR = '## 0. Invariants'
ZW, UMINUS = '​', '−'
DENY = ('rotmod', 'vobs', 'v_obs', 'massmodels', 'sparc', 'kmax_a2f10_c5h_run_v001', '/uvt_', 'runs_ext')
_ALLOW = []


def _hook(event, args):
    if event == 'open':
        path = args[0]
        if isinstance(path, int):
            return
        p = os.fsdecode(path) if isinstance(path, bytes) else str(path)
        low = p.lower()
        if any(w in low for w in DENY):
            raise PermissionError('refused target-like/protected open: %s' % p)
        mode = args[1] if len(args) > 1 and isinstance(args[1], str) else 'r'
        flags = args[2] if len(args) > 2 and isinstance(args[2], int) else 0
        writing = any(c in mode for c in 'wax+') or (flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND))
        if writing and not any(os.path.abspath(p) == w or os.path.abspath(p).startswith(w + os.sep) for w in _ALLOW):
            raise PermissionError('write refused: %s' % p)
    elif event in ('os.remove', 'os.rename', 'os.rmdir', 'shutil.rmtree', 'subprocess.Popen', 'os.system', 'os.posix_spawn',
                   'os.exec', 'os.fork', 'socket.connect', 'socket.getaddrinfo', 'os.truncate', 'os.symlink', 'os.link'):
        raise PermissionError('refused: %s' % event)


def ins(sentence):
    def f(d):
        p = os.path.join(d, P)
        t = open(p, encoding='utf-8').read()
        assert t.count(ANCHOR) == 1
        open(p, 'w', encoding='utf-8').write(t.replace(ANCHOR, sentence + '\n\n' + ANCHOR, 1))
    return f


def app(name, sentence):
    def f(d):
        p = os.path.join(d, name)
        t = open(p, encoding='utf-8').read()
        open(p, 'w', encoding='utf-8').write(t + '\n' + sentence + '\n')
    return f


def prov(fn):
    def f(d):
        p = os.path.join(d, N)
        doc = json.load(open(p, encoding='utf-8'))
        fn(doc)
        open(p, 'w', encoding='utf-8').write(json.dumps(doc, indent=1, ensure_ascii=False) + '\n')
    return f


def both(*fs):
    def f(d):
        for g in fs:
            g(d)
    return f


def sec11_row(synth_path):
    def f(d):
        p = os.path.join(d, P)
        t = open(p, encoding='utf-8').read()
        h = hashlib.sha256(open(synth_path, 'rb').read()).hexdigest()
        row = '| `%s` | `%s` |' % (synth_path, h)
        last = '| `claude_artifacts/review_freeze_v003g_c4/REVIEW_FREEZE_V003G_C4V001.md` |'
        i = t.index(last)
        j = t.index('\n', i)
        open(p, 'w', encoding='utf-8').write(t[:j + 1] + row + '\n' + t[j + 1:])
    return f


def cases(synth_path):
    Q = 'NGC3198-Q43'
    return [
        ('A01_listed_number_as_target_value', ins('The quoted value v_q of %s is 778.' % Q)),
        ('A02_listed_number_as_sigma_bound', ins('The quoted σ_q of every OUTER row is below 93.6.')),
        ('A03_listed_number_unit_with_unicode_minus', ins('The quoted value of %s is 778 km s%s1.' % (Q, UMINUS))),
        ('A04_listed_number_unit_middle_dot', ins('The quoted value of %s is 778 km·s⁻¹.' % Q)),
        ('A05_listed_number_unit_in_words', ins('The quoted value of %s is 778 kilometres per second.' % Q)),
        ('A06_listed_number_unit_division_slash', ins('The quoted value of %s is 778 km∕s.' % Q)),
        ('A07_listed_mantissa_m_per_s', ins('The quoted value of %s is 1.48e5 m/s.' % Q)),
        ('B01_zero_width_split_digits_unicode_minus_unit', ins('The quoted value of %s is 9%s8%s7 km s%s1.' % (Q, ZW, ZW, UMINUS))),
        ('B02_markdown_bold_split_digits', ins('The quoted value of %s is 9**8**7.' % Q)),
        ('B03_superscript_digits_with_km_s', ins('The quoted value of %s is ⁹⁸⁷ km/s.' % Q)),
        ('B04_sci_notation_superscript_exponent_km_s', ins('The quoted value of %s is 1.48×10³ km/s.' % Q)),
        ('B05_number_words_km_s', ins('The quoted value of %s is nine hundred eighty-seven km/s.' % Q)),
        ('B06_glued_to_identifier_slash', ins('Quoted pair: %s/987.6.' % Q)),
        ('B07_glued_to_identifier_underscore', ins('Quoted pair: %s_987.' % Q)),
        ('B08_eight_digit_number_cm_s', ins('The quoted value of %s is 98760000 cm/s.' % Q)),
        ('B09_section_sign_strip', ins('The quoted value of %s is §987.6.' % Q)),
        ('B10_code_span_K1_control', ins('The quoted value of %s is `987.6`.' % Q)),
        ('B11_code_span_symbol_defeats_T3', ins('For %s, `v_q` = 778.' % Q)),
        ('B12_escaped_underscore_symbol_defeats_T3', ins('For %s, v\\_q = 778.' % Q)),
        ('B13a_indexed_symbol_unlisted_value_control', ins('v_q(%s) = 987.6.' % Q)),
        ('B13b_indexed_symbol_listed_value', ins('v_q(%s) = 778.' % Q)),
        ('B14_symbol_with_approx_sign_variant', ins('For %s, v_q ≃ 778.' % Q)),
        ('B15_number_in_ROOT_ITEMS', app(R, 'The outermost quoted value is 987.6.')),
        ('B16_number_in_CLAUSE_MAP', app(M, 'The outermost quoted value is 987.6.')),
        ('B17_self_declared_category', both(ins('The outermost quoted value is 987.6.'),
                                            prov(lambda d: d['numbers'].update({'987.6': {'category': 'MODEL_DIAGNOSTIC', 'uses': ['synthetic']}})))),
        ('C01_target_path_elided_root_txt', ins('Rows were read from `…/data/NGC3198_observed_curve.txt`.')),
        ('C02_target_path_json', ins('Rows were read from `…/NGC3198_OBSERVED_VELOCITIES.json`.')),
        ('C03_extension_variant_data', ins('Rows were read from NGC3198.data.')),
        ('C04_extension_variant_dat_suffix', ins('Rows were read from NGC3198.dat_v2.')),
        ('C05_extension_variant_tsv_xlsx_fts', ins('Rows were read from NGC3198.tsv, NGC3198.xlsx and NGC3198.fts.')),
        ('C05b_extension_xlsx_only', ins('Rows were read from NGC3198.xlsx.')),
        ('C06_other_target_data_source_names', ins('Rows were read from the THINGS curve of de Blok et al., and the van Albada data.')),
        ('C07_fullwidth_SPARC', ins('Rows were read from the ＳＰＡＲＣ table.')),
        ('C08_soft_hyphen_rotmod', ins('Rows were read from the rot­mod file.')),
        ('C09_spaced_or_underscored_mass_models', ins('Rows were read from the Mass Models table (Mass_Models).')),
        ('C10_forbidden_term_in_provenance_json', prov(lambda d: d['numbers']['43']['uses'].append('row count read from the rotmod table'))),
        ('C11_vobs_variants', ins('Rows were read from the V obs and v-obs columns.')),
        ('C12_program_blinded_run_named', ins('Compare with runs_ext/KMAX_A2F10_C5H_RUN_V001 and UVT_Z2_A2F10_RUN_V001.')),
        ('D01_sec11_pins_targetlike_named_synthetic_file', sec11_row(synth_path)),
        # round-2 specific
        ('E01_forbidden_term_in_INDEX', app(I, 'Rows were read from the rotmod table.')),
        ('E02_listed_number_unit_m_s_plain', ins('The quoted value of %s is 778 m/s.' % Q)),
        ('E03_listed_number_code_span_symbol_sigma', ins('For %s, `σ_q` = 93.6.' % Q)),
    ]


def run_check(T, d):
    class A:
        pass
    a = A()
    a.dir, a.provenance, a.slots, a.expect_slots_sha = d, os.path.join(d, N), SLOTS, SLOTS_SHA
    a.nodes, a.expect_nodes_sha = NODES, NODES_SHA
    return T.run(a)


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--round2', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    work, outp = os.path.abspath(a.work), os.path.abspath(a.out)
    _ALLOW.extend([work, outp])
    sys.path.insert(0, os.path.join(a.round2, 'tools'))
    import check_target_free_c4v002 as T
    sys.addaudithook(_hook)
    os.makedirs(work)
    synth = os.path.join(work, 'SYNTH_NGC3198_OBSERVED_VELOCITY_TABLE_NOT_DATA.json')
    with open(synth, 'x', encoding='utf-8') as f:
        f.write('{"synthetic": "closure-lens canary; holds no data of any kind"}\n')
    base = run_check(T, a.round2)
    out = {'schema': 'R2A_CLOSURE_ADVERSARIAL_TARGET_FREE_CHECK_V001', 'round2': os.path.abspath(a.round2),
           'check_sha256': hashlib.sha256(open(os.path.join(a.round2, 'tools', 'check_target_free_c4v002.py'), 'rb').read()).hexdigest(),
           'baseline_target_free': base['verdict_target_free'], 'baseline_currency': base['verdict_currency'], 'cases': []}
    for name, fn in cases(synth):
        d = os.path.join(work, "case_%02d" % len(out["cases"]))
        os.makedirs(d)
        for n in (P, M, R, N, I):
            shutil.copyfile(os.path.join(a.round2, n), os.path.join(d, n))
        fn(d)
        changed = [n for n in (P, M, R, N, I) if open(os.path.join(d, n), 'rb').read() != open(os.path.join(a.round2, n), 'rb').read()]
        assert changed, name
        r = run_check(T, d)
        failed = sorted(k for k, v in r['checks'].items() if not v['pass'] and k != 'T7_V005_CURRENCY')
        out['cases'].append({'case': name, 'files_changed': changed, 'verdict_target_free': r['verdict_target_free'],
                             'failed_target_free_checks': failed, 'false_negative': r['verdict_target_free'] == 'PASS'})
    out['n_cases'] = len(out['cases'])
    out['n_false_negative'] = sum(c['false_negative'] for c in out['cases'])
    out['false_negatives'] = [c['case'] for c in out['cases'] if c['false_negative']]
    with open(outp, 'x', encoding='utf-8') as f:
        f.write(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
    for c in out['cases']:
        print('%-50s %-4s %s' % (c['case'], c['verdict_target_free'], ','.join(c['failed_target_free_checks'])))
    print('baseline', out['baseline_target_free'], out['baseline_currency'], '| false negatives', out['n_false_negative'], 'of', out['n_cases'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
