# R2-C lens (target-free and tools): adversarial mutations of the round-2 bundle that SHOULD make the round-2 check
# (tools/check_target_free_c4v002.py, imported read-only from the object) FAIL. A target-free violation whose
# verdict_target_free is PASS, or a currency violation whose verdict_currency is PASS, is a false negative.
# Synthetic only: every injected value is a non-physical sentinel (987.6, 9876, 1.48e9) or a value already listed in the
# provenance (778, 93.6) used as a stand-in, with the fake query id NGC3198-Q99. No target or observed value is known to,
# or used by, this script. The fence (fence_r2c) refuses target-like/protected opens and any write outside this lens folder.
# V005 is redirected to the lens snapshot (cf9bbf19...) for reproducibility, or to a per-case mutated copy of it.
# usage: python3 -I -B adversarial_r2c.py --object R2DIR --work NEW_DIR --out RESULT.json
import argparse, hashlib, json, os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fence_r2c
fence_r2c.install()

SLOTS = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json'
SLOTS_SHA = 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'
NODES = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json'
NODES_SHA = 'ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d'
SNAP = fence_r2c.LENS + '/snapshots/V005_AT_R2C.md'
SNAP_SHA = 'cf9bbf19eae3d2fb0262c31c3a0af43ecc2f100b9295c4075a591716b6ebb9dc'
P, M, R, N, I = 'PREREG_MISS_READING_R2.md', 'CLAUSE_SOURCE_MAP_R2.md', 'ROOT_ITEMS_R2.md', 'NUMBER_PROVENANCE_R2.json', 'INDEX_R2.md'
ANCHOR = '## 0. Invariants'
Q = 'NGC3198-Q99'
A66_EDIT = ('is flagged **TRUNCATION_SHAPE_RESIDUAL** in the freeze manifest', 'is not flagged in the freeze manifest')
CUR = {'v005': SNAP}


def rd(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def wr(p, t):
    with open(p, 'w', encoding='utf-8') as f:
        f.write(t)


def ins(s, name=P):
    def f(d):
        p = os.path.join(d, name)
        t = rd(p)
        assert t.count(ANCHOR) == 1 or name != P
        t2 = t.replace(ANCHOR, s + '\n\n' + ANCHOR, 1) if ANCHOR in t else t + '\n' + s + '\n'
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
        assert old in t, (name, old[:60])
        wr(p, t.replace(old, new, count))
    return f


def prov(fn):
    def f(d):
        p = os.path.join(d, N)
        doc = json.loads(rd(p))
        fn(doc)
        wr(p, json.dumps(doc, indent=1, ensure_ascii=False) + '\n')
    return f


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


def v005_copy(fn):
    """per-case V005: a mutated copy of the lens snapshot, written in the case folder"""
    def f(d):
        t = rd(SNAP)
        t2 = fn(t)
        assert t2 != t
        p = os.path.join(d, 'V005_CASE_COPY.md')
        wr(p, t2)
        return p
    return f


def a66_edit(t):
    assert t.count(A66_EDIT[0]) == 1
    return t.replace(A66_EDIT[0], A66_EDIT[1], 1)


def insert_heading(h):
    def g(t):
        k = t.index('\n## A98:')
        return t[:k + 1] + h + '\n\nSynthetic lens-R2C entry (not a root entry; never published).\n\n' + t[k + 1:]
    return g


def pin_row_regex(n):
    return re.compile(r'^\| A%d \|[^\n]*\| `[0-9a-f]{64}` \|$' % n, re.M)


def truncate_marker_case(T):
    """E01: the A66 pin is re-stated with an early end-marker; the A66 ruling text below that marker can then change."""
    v = rd(SNAP)
    secs = T.entry_sections(v, {66: '**Fact'})
    sec = secs[66][0]
    h = hashlib.sha256(sec.encode('utf-8')).hexdigest()

    def f(d):
        p = os.path.join(d, P)
        t = rd(p)
        m = pin_row_regex(66).search(t)
        row = m.group(0)
        new = re.sub(r'\| next heading \| `[0-9a-f]{64}` \|$', '| `**Fact` | `%s` |' % h, row)
        assert new != row
        wr(p, t.replace(row, new, 1))
    return f, len(sec)


def drop_pin_row(n, also=None):
    def f(d):
        p = os.path.join(d, P)
        t = rd(p)
        m = pin_row_regex(n).search(t)
        t = t[:m.start()] + t[m.end() + 1:]
        wr(p, t)
    return f


def trailing_space_pin_row(n):
    def f(d):
        p = os.path.join(d, P)
        t = rd(p)
        m = pin_row_regex(n).search(t)
        wr(p, t[:m.end()] + ' ' + t[m.end():])
    return f


def generator_complement(T):
    """the generator's own 'uncited' computation (make_miss_reading_c4v003.py L62-75) applied to the current V005"""
    cited = [48, 50, 52, 56, 60, 62, 63, 64, 65, 66, 70, 81, 82, 90]
    heads = sorted(set(x for x in T.all_headings(rd(SNAP)) if x >= 47))
    unc = [n for n in heads if n not in cited]
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
    text = ', '.join(('A%d' % r[0]) if len(r) == 1 else ('A%d–A%d' % (r[0], r[-1])) for r in runs)

    def f(d):
        p = os.path.join(d, P)
        t = rd(p)
        m = re.search(r'(\*\*Read with no change to this text:\*\*\s*)(.*?)(\.\s)', t)
        wr(p, t[:m.start(2)] + text + t[m.end(2):])
    return f, text


NC_OLD = 'A91–A96. From V005'
NC_98 = 'A91–A98. From V005'


def cases(T, synth_path):
    e01, e01_len = truncate_marker_case(T)
    t03, t03_text = generator_complement(T)
    c = []
    TF, CU = 'target_free', 'currency'
    # ---------- controls (should FAIL and do)
    c += [('K01_control_velocity', TF, ins('The quoted value at %s is 987.6 km/s.' % Q), None, 'control'),
          ('K02_control_symbol', TF, ins('Here v_q = 987.6 for %s.' % Q), None, 'control'),
          ('K03_control_term', TF, ins('See the rotmod table.'), None, 'control'),
          ('K04_control_unlisted', TF, ins('A quantity of 987.6 appears here.'), None, 'control'),
          ('K05_control_v005_a66_edit', TF, None, v005_copy(a66_edit), 'control: V005 A66 edited, honest pin'),
          ('K06_control_appended_A99', CU, sub(P, NC_OLD, NC_98), v005_copy(insert_heading('## A99: synthetic')), 'control: standard heading')]
    # ---------- round-1 lens B false negatives, replayed on v002 (Q43 replaced by the fake Q99)
    c += [('R1_A01_listed_value_v_q_of', TF, ins('The quoted value v_q of %s is 778.' % Q), None, 'round-1 A01'),
          ('R1_A02_listed_sigma_bound', TF, ins('The quoted σ_q of every OUTER row is below 93.6.'), None, 'round-1 A02'),
          ('R1_A03_unicode_minus_unit', TF, ins('The quoted value of %s is 778 km s−1.' % Q), None, 'round-1 A03'),
          ('R1_A04_middle_dot_unit', TF, ins('The quoted value of %s is 778 km·s⁻¹.' % Q), None, 'round-1 A04'),
          ('R1_A05_unit_in_words', TF, ins('The quoted value of %s is 778 kilometres per second.' % Q), None, 'round-1 A05'),
          ('R1_A06_division_slash_unit', TF, ins('The quoted value of %s is 778 km∕s.' % Q), None, 'round-1 A06'),
          ('R1_A07_mantissa_m_per_s', TF, ins('The quoted value of %s is 1.48e9 m/s.' % Q), None, 'round-1 A07 (non-physical exponent)'),
          ('R1_B01_zero_width_split', TF, ins('The quoted value of %s is 9​8​7 km s−1.' % Q), None, 'round-1 B01'),
          ('R1_B02_markdown_bold_split', TF, ins('The quoted value of %s is 9**8**7.' % Q), None, 'round-1 B02'),
          ('R1_B03_superscript_digits', TF, ins('The quoted value of %s is ⁹⁸⁷ km/s.' % Q), None, 'round-1 B03'),
          ('R1_B04_sci_superscript', TF, ins('The quoted value of %s is 1.48×10³ km/s.' % Q), None, 'round-1 B04'),
          ('R1_B05_number_words', TF, ins('The quoted value of %s is nine hundred eighty-seven km/s.' % Q), None, 'round-1 B05'),
          ('R1_B06_glued_slash', TF, ins('Quoted pair: %s/987.6.' % Q), None, 'round-1 B06'),
          ('R1_B07_glued_underscore', TF, ins('Quoted pair: %s_987.' % Q), None, 'round-1 B07'),
          ('R1_B08_cm_per_s', TF, ins('The quoted value of %s is 98760000 cm/s.' % Q), None, 'round-1 B08'),
          ('R1_B09_section_sign', TF, ins('The quoted value of %s is §987.6.' % Q), None, 'round-1 B09'),
          ('R1_B10_code_span', TF, ins('The quoted value of %s is `987.6`.' % Q), None, 'round-1 B10'),
          ('R1_B11_code_span_symbol', TF, ins('For %s, `v_q` = 778.' % Q), None, 'round-1 B11'),
          ('R1_B12_escaped_underscore', TF, ins('For %s, v\\_q = 778.' % Q), None, 'round-1 B12'),
          ('R1_B13a_indexed_unlisted', TF, ins('v_q(%s) = 987.6.' % Q), None, 'round-1 B13a (control)'),
          ('R1_B13b_indexed_listed', TF, ins('v_q(%s) = 778.' % Q), None, 'round-1 B13b'),
          ('R1_B14_approx_variant', TF, ins('For %s, v_q ≃ 778.' % Q), None, 'round-1 B14'),
          ('R1_B15_root_items_number', TF, app(R, 'The outermost quoted value is 987.6.'), None, 'round-1 B15'),
          ('R1_B16_map_number', TF, app(M, 'The outermost quoted value is 987.6.'), None, 'round-1 B16'),
          ('R1_B17_self_declared', TF, both(ins('The outermost quoted value is 987.6.'), prov(lambda d: d['numbers'].update({'987.6': {'category': 'MODEL_DIAGNOSTIC', 'uses': ['synthetic']}}))), None, 'round-1 B17 (stated limit)'),
          ('R1_C01_txt_path', TF, ins('Rows were read from `…/data/NGC3198_observed_curve.txt`.'), None, 'round-1 C01'),
          ('R1_C02_observed_json_path', TF, ins('Rows were read from `…/NGC3198_OBSERVED_VELOCITIES.json`.'), None, 'round-1 C02'),
          ('R1_C03_ext_data', TF, ins('Rows were read from NGC3198.data.'), None, 'round-1 C03'),
          ('R1_C04_ext_dat_suffix', TF, ins('Rows were read from NGC3198.dat_v2.'), None, 'round-1 C04'),
          ('R1_C05_ext_tsv_xlsx_fts', TF, ins('Rows were read from NGC3198.tsv, NGC3198.xlsx and NGC3198.fts.'), None, 'round-1 C05'),
          ('R1_C06_source_names', TF, ins('Rows were read from the THINGS curve of de Blok et al., and the van Albada data.'), None, 'round-1 C06'),
          ('R1_C07_fullwidth', TF, ins('Rows were read from the ＳＰＡＲＣ table.'), None, 'round-1 C07'),
          ('R1_C08_soft_hyphen', TF, ins('Rows were read from the rot­mod file.'), None, 'round-1 C08'),
          ('R1_C09_mm_spaced', TF, ins('Rows were read from the Mass Models table (Mass_Models).'), None, 'round-1 C09'),
          ('R1_C10_term_in_provenance', TF, prov(lambda d: d['numbers']['43']['uses'].append('row count read from the rotmod table')), None, 'round-1 C10'),
          ('R1_C11_vo_variants', TF, ins('Rows were read from the V obs and v-obs columns.'), None, 'round-1 C11'),
          ('R1_D01_targetlike_named_pin', TF, None, None, 'round-1 D01 (stated limit; built below)')]
    # ---------- new: T1 evasion beyond NFKC + Cf stripping
    c += [('N01_cgj_Mn', TF, ins('Rows were read from the rot͏mod file.'), None, 'U+034F COMBINING GRAPHEME JOINER (Mn, invisible)'),
          ('N02_vs16_Mn', TF, ins('Rows were read from the rot️mod file.'), None, 'U+FE0F VARIATION SELECTOR-16 (Mn, invisible)'),
          ('N03_cyrillic_A', TF, ins('Rows were read from the SPАRC table.'), None, 'U+0410 CYRILLIC A homoglyph'),
          ('N04_cyrillic_o', TF, ins('Rows were read from the rоtmod file.'), None, 'U+043E CYRILLIC o homoglyph'),
          ('N05_greek_omicron', TF, ins('Rows were read from the rοtmod file.'), None, 'U+03BF GREEK omicron homoglyph'),
          ('N06_html_ncr', TF, ins('Rows were read from the &#x72;otmod file.'), None, 'HTML numeric reference; Markdown renders it'),
          ('N07_html_shy_entity', TF, ins('Rows were read from the rot&shy;mod file.'), None, 'HTML soft-hyphen entity; renders invisibly'),
          ('N08_html_comment_split', TF, ins('Rows were read from the rot<!-- -->mod file.'), None, 'HTML comment splits the term; renders joined'),
          ('N09_markdown_emphasis_split', TF, ins('Rows were read from the rot**mod** file.'), None, 'emphasis markup splits the term'),
          ('N10_hangul_filler', TF, ins('Rows were read from the rotᅟmod file.'), None, 'U+115F HANGUL CHOSEONG FILLER (Lo)'),
          ('N11_latex_vsub', TF, ins('Rows used V_{obs} and V_{\\rm obs} from the table.'), None, 'LaTeX subscript forms'),
          ('N12_ext_txt_asc_h5_npy', TF, ins('Rows were read from q99.txt, q99.asc, q99.h5, q99.npy and q99.parquet.'), None, 'extensions not in FORBIDDEN_EXT')]
    # ---------- new: T2 unit spellings (value 778 is listed, so T4 cannot backstop)
    for cid, unit, note in [('U01_latex_dollar', 'km s$^{-1}$', 'astro LaTeX standard'), ('U02_latex_thin_space', 'km\\,s$^{-1}$', 'LaTeX'),
                            ('U03_caret_braces', 'km s^{-1}', ''), ('U04_html_sup', 'km s<sup>-1</sup>', 'HTML'),
                            ('U05_en_dash', 'km s–1', 'U+2013'), ('U06_hyphen_2010', 'km s‐1', 'U+2010'),
                            ('U07_fraction_slash', 'km⁄s', 'U+2044'), ('U08_parenthesised', '(km/s)', ''),
                            ('U09_m_per_s', 'm/s', ''), ('U10_kpc_per_Gyr', 'kpc/Gyr', 'about 0.98 km/s'), ('U11_kilometers_slash_second', 'kilometers/second', ''),
                            ('U12_kmps', 'kmps', ''), ('U13_caret_paren', 'km s^(-1)', ''), ('U14_mathrm', '\\mathrm{km\\,s^{-1}}', 'LaTeX')]:
        c.append((cid, TF, ins('The quoted value at %s is 778 %s.' % (Q, unit)), None, note))
    c.append(('U15_unit_in_table_header', TF, ins('| id | v (km/s) |\n|---|---|\n| %s | 778 |' % Q), None, 'unit in a header cell'))
    # ---------- new: T3 symbol forms (value listed)
    for cid, s, note in [('S01_braced_subscript', 'v_{q} = 778', ''), ('S02_walrus', 'v_q := 778', ''), ('S03_identical_to', 'v_q ≡ 778', ''),
                         ('S04_tilde_operator', 'v_q ∼ 778', 'U+223C'), ('S05_eq_tilde', 'v_q = ~778', ''), ('S06_eq_paren', 'v_q = (778', ''),
                         ('S07_is', 'v_q is 778', ''), ('S08_vflat_no_underscore', 'Vflat = 778', ''), ('S09_v_c', 'V_c = 778', ''),
                         ('S10_v_circ', 'v_circ = 778', ''), ('S11_sigma_braced', 'σ_{q} = 93.6', ''), ('S12_e_v', 'e_v = 93.6', ''),
                         ('S13_observed_rotation_speed', 'the observed rotation speed = 778', ''), ('S14_less_than', 'v_q < 778', 'a bound'),
                         ('S15_leq', 'v_q ≤ 778', 'a bound')]:
        c.append((cid, TF, ins('For %s, %s.' % (Q, s)), None, note))
    # ---------- new: numbers hidden by the v002 stripping rules (value 987.6 / 9876 is NOT listed; T4 should fail)
    c += [('H01_hex_with_letter', TF, ins('The quoted value at %s is 9876e5.' % Q), None, 'HEXL strips 6+ hex chars with a letter'),
          ('H02_iso_Z_suffix', TF, ins('The quoted value at %s is 9876Z.' % Q), None, 'ISO strips \\d{4}Z'),
          ('H03_iso_time_Z', TF, ins('The quoted value at %s is 98:76Z.' % Q), None, 'ISO strips \\d{2}:\\d{2}Z'),
          ('H04_tag_free_text', TF, ins('[C-quoted value at %s is 987.6]' % Q), None, '[C-...] stripping takes any bracket text'),
          ('H05_tag_multiline_span', TF, ins('Note [C-\nThe quoted value at %s is 987.6.\nend]' % Q), None, '[^\\]]+ spans newlines'),
          ('H06_ident_chain_hyphen', TF, ins('The quoted value-987.6 is recorded.'), None, 'IDENT_CHAIN'),
          ('H07_ident_digit', TF, ins('The quoted value is v987 at %s.' % Q), None, 'IDENT_DIGIT'),
          ('H08_greek_glued', TF, ins('The quoted value is σ987.6 at %s.' % Q), None, 'NUM lookbehind excludes any word char'),
          ('H09_exponent_listed_mantissa', TF, ins('The quoted value at %s is 1.48e9.' % Q), None, 'exponent dropped; mantissa 1.48 is listed'),
          ('H10_html_comment_digits', TF, ins('The quoted value at %s is 9<!-- -->8<!-- -->7.' % Q), None, 'each digit is a listed token'),
          ('H11_html_ncr_digits_unit', TF, ins('The quoted value at %s is &#x39;&#x38;&#x37; km/s.' % Q), None, 'renders as 987 km/s'),
          ('H12_hex_literal', TF, ins('The quoted value at %s is 0x3DB.' % Q), None, '0x3DB = 987; only token 0 is seen'),
          ('H13_url_path', TF, ins('See [the row](https://example.invalid/q99/987.6).'), None, 'numbers in URLs and paths are stripped')]
    # ---------- new: files outside TEXT_FILES
    c += [('F01_index_unscanned', TF, app(I, 'Rows were read from the rotmod table; v_q = 987.6 km/s.'), None, 'INDEX_R2.md is in the bundle'),
          ('F02_provenance_uses_unscanned', TF, prov(lambda d: d['numbers']['43']['uses'].append('v_q = 987.6 km/s at %s' % Q)), None, 'provenance text'),
          ('F03_provenance_unused_key', TF, prov(lambda d: d['numbers'].update({'987.6': {'category': 'MODEL_DIAGNOSTIC', 'uses': ['quoted v_q at %s' % Q]}})), None, 'listed_but_absent does not fail T4'),
          ('F04_new_bundle_file', TF, newfile('APPENDIX_R2.md', 'Rows were read from the rotmod table; v_q = 987.6 km/s.\n'), None, 'any added file')]
    # ---------- new: T5 per-entry pins
    c += [('E01_early_end_marker', TF, e01, v005_copy(a66_edit), 'A66 pin re-stated to end before **Fact (%d bytes kept); A66 ruling then edited' % e01_len),
          ('E02_pin_dropped_listed_no_change', TF, both(drop_pin_row(66), sub(P, 'A61, A67–A69', 'A61, A66–A69'), sub(P, NC_OLD, NC_98)), v005_copy(a66_edit), 'A66 pin row removed, A66 put in the no-change list, A66 edited'),
          ('E03_malformed_pin_row_skipped', TF, both(trailing_space_pin_row(66), sub(P, NC_OLD, NC_98)), v005_copy(a66_edit), 'trailing space: row silently not parsed')]
    # ---------- new: T7 currency
    c += [('T00_reviewed_A97_A98', CU, sub(P, NC_OLD, NC_98), None, 'baseline (should PASS): A97-A98 put in the no-change list'),
          ('T01_open_ended_range', CU, sub(P, NC_OLD, 'A91–A199. From V005'), None, 'a range past the last heading covers future entries'),
          ('T03_generator_complement', CU, t03, None, 'the generator complement labels A97 and A98 "read with no change": ' + t03_text)]
    for cid, h in [('T02a_suffix_letter', '## A99a: synthetic'), ('T02b_level3', '### A99: synthetic'), ('T02c_space', '## A 99: synthetic'),
                   ('T02d_no_space', '##A99: synthetic'), ('T02e_lower', '## a99: synthetic'), ('T02f_prefix_word', '## Entry A99: synthetic'),
                   ('T02g_bold_entry', '**A99: synthetic**')]:
        c.append((cid, CU, sub(P, NC_OLD, NC_98), v005_copy(insert_heading(h)), 'heading form: %r' % h))
    return c


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--object', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    assert hashlib.sha256(open(SNAP, 'rb').read()).hexdigest() == SNAP_SHA
    sys.path.insert(0, os.path.join(a.object, 'tools'))
    import check_target_free_c4v002 as T
    orig = T.sources_from_section11

    def patched(text):
        return [(l, (CUR['v005'] if l == 'decisions V005' else p), h) for l, p, h in orig(text)]
    T.sources_from_section11 = patched
    os.makedirs(a.work)
    synth = os.path.join(os.path.abspath(a.work), 'SYNTH_NGC3198_OBSERVED_VELOCITY_TABLE_NOT_DATA.json')
    with open(synth, 'x', encoding='utf-8') as f:
        f.write('{"synthetic": "lens R2-C canary; holds no data of any kind"}\n')

    def run_check(d):
        class A:
            pass
        x = A()
        x.dir, x.provenance, x.slots, x.expect_slots_sha = d, os.path.join(d, N), SLOTS, SLOTS_SHA
        x.nodes, x.expect_nodes_sha = NODES, NODES_SHA
        return T.run(x)

    CUR['v005'] = SNAP
    base = run_check(a.object)
    out = {'schema': 'R2C_ADVERSARIAL_TARGET_FREE_CHECK_V001', 'object': os.path.abspath(a.object),
           'check_sha256': hashlib.sha256(open(os.path.join(a.object, 'tools', 'check_target_free_c4v002.py'), 'rb').read()).hexdigest(),
           'v005_snapshot': {'path': SNAP, 'sha256': SNAP_SHA},
           'baseline': {'target_free': base['verdict_target_free'], 'currency': base['verdict_currency'],
                        'T7_later': base['checks']['T7_V005_CURRENCY'].get('later_entries_needing_a_revision_or_no_change_note')},
           'cases': []}
    for cid, kind, fn, vfn, note in cases(T, synth):
        d = os.path.join(a.work, cid)
        os.makedirs(d)
        for n in (P, M, R, N, I):
            shutil.copyfile(os.path.join(a.object, n), os.path.join(d, n))
        if cid == 'R1_D01_targetlike_named_pin':
            def fn(dd, synth=synth):
                p = os.path.join(dd, P)
                t = rd(p)
                h = hashlib.sha256(open(synth, 'rb').read()).hexdigest()
                last = '| `claude_artifacts/review_freeze_v003g_c4/REVIEW_FREEZE_V003G_C4V001.md` |'
                i = t.index(last)
                j = t.index('\n', i)
                wr(p, t[:j + 1] + '| `%s` | `%s` |' % (synth, h) + '\n' + t[j + 1:])
        if fn:
            fn(d)
        CUR['v005'] = vfn(d) if vfn else SNAP
        role = ('control' if (cid.startswith('K0') or '(control)' in note) else 'baseline' if 'baseline (should PASS)' in note
                else 'limit' if 'stated limit' in note else 'attack')
        changed = [n for n in (P, M, R, N, I) if open(os.path.join(d, n), 'rb').read() != open(os.path.join(a.object, n), 'rb').read()]
        extra = sorted(set(os.listdir(d)) - {P, M, R, N, I})
        r = run_check(d)
        CUR['v005'] = SNAP
        failed = sorted(k for k, v in r['checks'].items() if not v['pass'])
        verdict = r['verdict_target_free'] if kind == 'target_free' else r['verdict_currency']
        rec = {'case': cid, 'kind': kind, 'note': note, 'files_changed': changed, 'extra_files': extra, 'verdict_target_free': r['verdict_target_free'],
               'verdict_currency': r['verdict_currency'], 'failed_checks': failed,
               'role': role,
               'false_negative': (verdict == 'PASS') if role in ('attack', 'limit') else None,
               'control_ok': (verdict == 'FAIL') if role == 'control' else ((verdict == 'PASS') if role == 'baseline' else None)}
        if kind == 'currency':
            rec['T7_later'] = r['checks']['T7_V005_CURRENCY'].get('later_entries_needing_a_revision_or_no_change_note')
        for k in ('T1_FORBIDDEN_TERMS', 'T2_NO_VELOCITY_VALUE', 'T3_NO_TARGET_SYMBOL_VALUE'):
            if r['checks'][k]['hits']:
                rec.setdefault('hits', {})[k] = r['checks'][k]['hits']
        t4 = r['checks']['T4_NUMBER_PROVENANCE']
        if t4['missing_from_provenance']:
            rec['T4_missing'] = t4['missing_from_provenance']
        if t4['listed_but_absent']:
            rec['T4_listed_but_absent'] = t4['listed_but_absent']
        t5 = r['checks']['T5_SOURCES_TARGET_FREE_AND_PINNED']
        if t5['problems']:
            rec['T5_problems'] = t5['problems']
        rec['T5_entries_checked'] = [e['entry'] for e in t5['v005_entries']]
        out['cases'].append(rec)
    out['n_cases'] = len(out['cases'])
    out['n_attack'] = sum(1 for x in out['cases'] if x['role'] == 'attack')
    out['n_false_negative'] = sum(1 for x in out['cases'] if x['role'] == 'attack' and x['false_negative'])
    out['n_limit_cases_passing'] = sum(1 for x in out['cases'] if x['role'] == 'limit' and x['false_negative'])
    out['controls_ok'] = all(x['control_ok'] for x in out['cases'] if x['control_ok'] is not None)
    with open(a.out, 'x', encoding='utf-8') as f:
        f.write(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
    for x in out['cases']:
        print('%-36s %-8s %-11s tf=%-4s cur=%-4s FN=%-5s ok=%-5s %s' % (x['case'], x['role'], x['kind'], x['verdict_target_free'], x['verdict_currency'],
                                                        x['false_negative'], x['control_ok'], ','.join(f.split('_')[0] for f in x['failed_checks'])))
    print('baseline', out['baseline'], '| attack false negatives', out['n_false_negative'], 'of', out['n_attack'], '| stated-limit cases passing',
          out['n_limit_cases_passing'], '| controls/baselines ok', out['controls_ok'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
