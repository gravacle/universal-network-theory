# Lens B (target-free and blinding), miss-reading prereg r2 round1: adversarial mutations of the r2 text that SHOULD make
# tools/check_target_free_c4v001.py FAIL. A case whose verdict is PASS is a false negative of the check.
# Synthetic only: every injected value is a non-physical sentinel (778, 987, 1.48e3 ...) or a listed provenance number used
# as a stand-in; no NGC3198 target or observed value is known to, or used by, this script. Nothing outside --work and --out
# is written. The check module is imported read-only from the object's tools folder (run with -I -B, so no pycache is written).
# usage: python3 -I -B adversarial_check_lensb.py --round1 R1DIR --work NEW_DIR --out RESULT.json
import argparse, hashlib, json, os, shutil, sys

SLOTS = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json'
SLOTS_SHA = 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'
P, M, R, N = 'PREREG_MISS_READING_R2.md', 'CLAUSE_SOURCE_MAP_R2.md', 'ROOT_ITEMS_R2.md', 'NUMBER_PROVENANCE_R2.json'
ANCHOR = '## 0. Invariants'
ZW = '​'      # zero-width space
UMINUS = '−'  # minus sign


def ins(sentence):
    """insert a synthetic sentence into the prereg just before section 0 (the object's own mutation-test anchor)"""
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
    """add a pinned source row for a synthetic file to the last section-11 table ('Claude4's own')"""
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
        # --- T4 checks token VALUES, not occurrences: a listed number may stand anywhere
        ('A01_listed_number_as_target_value', ins('The quoted value v_q of %s is 778.' % Q)),
        ('A02_listed_number_as_sigma_bound', ins('The quoted σ_q of every OUTER row is below 93.6.')),
        ('A03_listed_number_unit_with_unicode_minus', ins('The quoted value of %s is 778 km s%s1.' % (Q, UMINUS))),
        ('A04_listed_number_unit_middle_dot', ins('The quoted value of %s is 778 km·s⁻¹.' % Q)),
        ('A05_listed_number_unit_in_words', ins('The quoted value of %s is 778 kilometres per second.' % Q)),
        ('A06_listed_number_unit_division_slash', ins('The quoted value of %s is 778 km∕s.' % Q)),
        ('A07_listed_mantissa_m_per_s', ins('The quoted value of %s is 1.48e5 m/s.' % Q)),
        # --- unlisted numbers hidden from NUM / VEL
        ('B01_zero_width_split_digits_unicode_minus_unit', ins('The quoted value of %s is 9%s8%s7 km s%s1.' % (Q, ZW, ZW, UMINUS))),
        ('B02_markdown_bold_split_digits', ins('The quoted value of %s is 9**8**7.' % Q)),
        ('B03_superscript_digits_with_km_s', ins('The quoted value of %s is ⁹⁸⁷ km/s.' % Q)),
        ('B04_sci_notation_superscript_exponent_km_s', ins('The quoted value of %s is 1.48×10³ km/s.' % Q)),
        ('B05_number_words_km_s', ins('The quoted value of %s is nine hundred eighty-seven km/s.' % Q)),
        ('B06_glued_to_identifier_slash', ins('Quoted pair: %s/987.6.' % Q)),
        ('B07_glued_to_identifier_underscore', ins('Quoted pair: %s_987.' % Q)),
        ('B08_eight_digit_number_hex_stripped_cm_s', ins('The quoted value of %s is 98760000 cm/s.' % Q)),
        ('B09_section_sign_strip', ins('The quoted value of %s is §987.6.' % Q)),
        ('B10_code_span_K1_control', ins('The quoted value of %s is `987.6`.' % Q)),
        ('B11_code_span_symbol_defeats_T3', ins('For %s, `v_q` = 778.' % Q)),
        ('B12_escaped_underscore_symbol_defeats_T3', ins('For %s, v\\_q = 778.' % Q)),
        ('B13a_indexed_symbol_unlisted_value_control', ins('v_q(%s) = 987.6.' % Q)),
        ('B13b_indexed_symbol_listed_value', ins('v_q(%s) = 778.' % Q)),
        ('B14_symbol_with_approx_sign_variant', ins('For %s, v_q ≃ 778.' % Q)),
        ('B15_number_in_ROOT_ITEMS_not_scanned_by_T4', app(R, 'The outermost quoted value is 987.6.')),
        ('B16_number_in_CLAUSE_MAP_not_scanned_by_T4', app(M, 'The outermost quoted value is 987.6.')),
        ('B17_self_declared_category', both(ins('The outermost quoted value is 987.6.'),
                                            prov(lambda d: d['numbers'].update({'987.6': {'category': 'MODEL_DIAGNOSTIC', 'uses': ['synthetic']}})))),
        # --- T1 naming (deny-list of 7 substrings and 7 extensions)
        ('C01_target_path_elided_root_txt', ins('Rows were read from `…/data/NGC3198_observed_curve.txt`.')),
        ('C02_target_path_json', ins('Rows were read from `…/NGC3198_OBSERVED_VELOCITIES.json`.')),
        ('C03_extension_variant_data', ins('Rows were read from NGC3198.data.')),
        ('C04_extension_variant_dat_suffix', ins('Rows were read from NGC3198.dat_v2.')),
        ('C05_extension_variant_tsv_xlsx_fts', ins('Rows were read from NGC3198.tsv, NGC3198.xlsx and NGC3198.fts.')),
        ('C06_other_target_data_source_names', ins('Rows were read from the THINGS curve of de Blok et al., and the van Albada data.')),
        ('C07_fullwidth_SPARC', ins('Rows were read from the ＳＰＡＲＣ table.')),
        ('C08_soft_hyphen_rotmod', ins('Rows were read from the rot­mod file.')),
        ('C09_spaced_or_underscored_mass_models', ins('Rows were read from the Mass Models table (Mass_Models).')),
        ('C10_forbidden_term_in_provenance_json', prov(lambda d: d['numbers']['43']['uses'].append('row count read from the rotmod table'))),
        ('C11_vobs_variants', ins('Rows were read from the V obs and v-obs columns.')),
        ('C12_program_blinded_run_named', ins('Compare with runs_ext/KMAX_A2F10_C5H_RUN_V001 and UVT_Z2_A2F10_RUN_V001.')),
        # --- T5 judges target-freeness of a pinned source by its path string only
        ('D01_sec11_pins_targetlike_named_synthetic_file', sec11_row(synth_path)),
    ]


def run_check(T, d):
    class A:
        pass
    a = A()
    a.dir, a.provenance, a.slots, a.expect_slots_sha = d, os.path.join(d, N), SLOTS, SLOTS_SHA
    return T.run(a)


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--round1', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    sys.path.insert(0, os.path.join(a.round1, 'tools'))
    import check_target_free_c4v001 as T
    os.makedirs(a.work)                       # must not exist
    synth = os.path.join(os.path.abspath(a.work), 'SYNTH_NGC3198_OBSERVED_VELOCITY_TABLE_NOT_DATA.json')
    with open(synth, 'x', encoding='utf-8') as f:
        f.write('{"synthetic": "lens-B canary; holds no data of any kind"}\n')
    out = {'schema': 'LENSB_ADVERSARIAL_TARGET_FREE_CHECK_V001', 'round1': os.path.abspath(a.round1),
           'check_sha256': hashlib.sha256(open(os.path.join(a.round1, 'tools', 'check_target_free_c4v001.py'), 'rb').read()).hexdigest(),
           'baseline': run_check(T, a.round1)['verdict'], 'cases': []}
    for name, fn in cases(synth):
        d = os.path.join(a.work, name)
        os.makedirs(d)
        for n in (P, M, R, N):
            shutil.copyfile(os.path.join(a.round1, n), os.path.join(d, n))
        fn(d)
        changed = [n for n in (P, M, R, N) if open(os.path.join(d, n), 'rb').read() != open(os.path.join(a.round1, n), 'rb').read()]
        assert changed, name
        r = run_check(T, d)
        failed = sorted(k for k, v in r['checks'].items() if not v['pass'])
        out['cases'].append({'case': name, 'files_changed': changed, 'verdict': r['verdict'], 'failed_checks': failed,
                             'false_negative': r['verdict'] == 'PASS'})
    out['n_cases'] = len(out['cases'])
    out['n_false_negative'] = sum(c['false_negative'] for c in out['cases'])
    with open(a.out, 'x', encoding='utf-8') as f:
        f.write(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
    for c in out['cases']:
        print('%-50s %-4s %s' % (c['case'], c['verdict'], ','.join(c['failed_checks'])))
    print('baseline', out['baseline'], 'false negatives', out['n_false_negative'], 'of', out['n_cases'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
