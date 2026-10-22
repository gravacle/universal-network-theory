# Lens B: can T5's per-entry V005 pinning pass when a cited ruling has been changed by a LATER entry?
# Synthetic amendments are applied to a COPY of the V005 addendum (taken at review time) inside --work; the check's
# section-11 source list is patched so that 'decisions V005' points at the copy. The r2 round1 text is not modified.
# Nothing outside --work and --out is written. usage: python3 -I -B t5_v005_amendment_lensb.py --round1 R1 --v005 COPY --work NEW --out RES.json
import argparse, hashlib, json, os, sys

SLOTS = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json'
SLOTS_SHA = 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'
AMEND_81 = ('## A92: A81 RI-23 amended (SYNTHETIC lens-B probe, not a ruling)\n\n'
            'RI-23 is superseded: the NGC gas M_s is 160 in every case, and LO_NGC is not recomputed.\n\n')
AMEND_66_HEAD = ('## A66 amendment (SYNTHETIC lens-B probe, not a ruling)\n\n'
                 'A66.2 is withdrawn: N_FAIL_N1 on a TRUNCATION_SHAPE ring now blocks NGC route A/B.\n\n')


def before_heading(text, heading_prefix, block):
    i = text.index('\n' + heading_prefix) + 1
    return text[:i] + block + text[i:]


def mutations():
    return [
        ('E00_unmodified_copy_with_A90_A91', lambda t: t, 'PASS expected by design; A90 (NGC K32 N-tests) postdates r2 assembly'),
        ('E01_later_entry_amends_A81_inserted_like_root_does', lambda t: before_heading(t, '## A91:', AMEND_81), 'should FAIL'),
        ('E02_supersession_inside_uncited_entry_A90', lambda t: t.replace('The A66 consequence applies at step 5.',
                                                                         'The A66 consequence applies at step 5. A66.2 is withdrawn (SYNTHETIC probe): N_FAIL_N1 blocks NGC route A/B.', 1), 'should FAIL'),
        ('E03_amendment_heading_appended_at_EOF_no_blank', lambda t: t + AMEND_81.replace('A92', 'A93'), 'should FAIL'),
        ('E04_amendment_heading_appended_at_EOF_after_blank', lambda t: t + '\n' + AMEND_81.replace('A92', 'A93'), 'should FAIL'),
        ('E05_in_place_edit_of_A81_control', lambda t: t.replace('the NGC gas M_s becomes 128', 'the NGC gas M_s becomes 160', 1), 'should FAIL'),
        ('E06_duplicate_A81_heading_control', lambda t: before_heading(t, '## A91:', '## A81: duplicate (SYNTHETIC probe)\n\nM_s 160.\n\n'), 'should FAIL'),
        ('E07_variant_heading_A81a', lambda t: before_heading(t, '## A91:', '## A81a: RI-23 amended (SYNTHETIC probe)\n\nM_s 160.\n\n'), 'should FAIL'),
        ('E08_variant_heading_A66_amendment', lambda t: before_heading(t, '## A91:', AMEND_66_HEAD), 'should FAIL'),
        ('E09_edit_in_A65_trailing_0512_block_control', lambda t: t.replace('N_PASS is only an input to NGC route A/B.',
                                                                          'N_PASS and N_INCOMPLETE are inputs to NGC route A/B.', 1), 'should FAIL'),
    ]


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--round1', required=True)
    ap.add_argument('--v005', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    sys.path.insert(0, os.path.join(a.round1, 'tools'))
    import check_target_free_c4v001 as T
    os.makedirs(a.work)
    base_bytes = open(a.v005, 'rb').read()
    base = base_bytes.decode('utf-8')
    orig = T.sources_from_section11
    out = {'schema': 'LENSB_T5_V005_AMENDMENT_PROBE_V001', 'v005_copy': os.path.abspath(a.v005),
           'v005_copy_sha256': hashlib.sha256(base_bytes).hexdigest(), 'cases': []}
    for name, fn, note in mutations():
        t2 = fn(base)
        assert (t2 != base) or name.startswith('E00'), name
        p = os.path.join(os.path.abspath(a.work), name + '_V005.md')
        with open(p, 'x', encoding='utf-8') as f:
            f.write(t2)
        T.sources_from_section11 = lambda text, _p=p: [(l, (_p if l == 'decisions V005' else q), h) for (l, q, h) in orig(text)]

        class A:
            pass
        ca = A()
        ca.dir, ca.provenance, ca.slots, ca.expect_slots_sha = a.round1, os.path.join(a.round1, 'NUMBER_PROVENANCE_R2.json'), SLOTS, SLOTS_SHA
        r = T.run(ca)
        t5 = r['checks']['T5_SOURCES_TARGET_FREE_AND_PINNED']
        out['cases'].append({'case': name, 'note': note, 'v005_variant_sha256': hashlib.sha256(t2.encode('utf-8')).hexdigest(),
                             'T5_pass': t5['pass'], 'verdict': r['verdict'], 'problems': t5['problems'],
                             'entries_mismatched': [e['entry'] for e in t5['v005_entries'] if not e['match']]})
    T.sources_from_section11 = orig
    with open(a.out, 'x', encoding='utf-8') as f:
        f.write(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
    for c in out['cases']:
        print('%-52s T5 %-5s verdict %-4s %s %s' % (c['case'], c['T5_pass'], c['verdict'], c['entries_mismatched'], c['problems'][:1]))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
