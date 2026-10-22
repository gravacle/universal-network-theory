# Claude4 seal tools v004 (BUILD helper; A110, dispatch 0646): write tests/test_seal_tools_c4v004.py = v003's test bytes (67dd8a00) with
# exactly the replacements below (each old text must occur exactly once, else the run fails and nothing is written): the header, the tool 4
# import, the port bookkeeping (a results list stamped with the builder-call count), the v004 constants, the SYNTHETIC manual disclosures
# fixture MD0 in the builder's base arguments and CLI, the genuine record's schema, four case texts that named the v003 record, the new v004
# cases (before the guard reset at the end) and the summary with both port maps. The output is created exclusively and compiled.
# r2 (successor of tools/make_tests_c4v004.py, which refused on an anchor that occurred twice and wrote nothing): the B8-control rename
# anchor carries its check( prefix. usage: python3 -I -B make_tests_c4v004_r2.py OUT.py
import hashlib, sys
from pathlib import Path

V3_TESTS = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v003/tests/test_seal_tools_c4v003.py')
V3_TESTS_SHA = '67dd8a0085436639ef85650ca966b6b9ae045cc9413f01fc943b7003f142099a'

HEADER = r'''# Claude4 seal tools v004: tamper tests for the five seal tools with tool 4 v004 (A110, dispatches 0646 and 0647: root's manual disclosures
# bound into the SEAL_RECORD). Successor of v003 test_seal_tools_c4v003.py (67dd8a00; 352/352 in run_20261019T000810Z, TEST_RESULTS_C4V003.json
# 26bb912f). The v003 suite is PORTED UNCHANGED: its code, fixtures, case texts and order are v003's, run against this folder, where
# seal_common and tools 1, 2, 3 and 5 are v003's bytes and tool 4 is build_seal_record_c4v004.py. The changes to the v003 code are: tool 4 is
# imported as build_seal_record_c4v004; the builder's base arguments (args_for, hence every copy of them) and its base CLI argv also carry
# the SYNTHETIC manual disclosures fixture MD0 (root's SEAL_MANUAL_DISCLOSURES_V001 form, with prereg r6's E_R6_1 read from
# SELECTED_R6_C4V001's bytes), so every v003 tool 4 case still tests only what it tested; the genuine record's expected schema is
# UNT_V007_SEAL_RECORD_C4V004; and four case texts that named the v003 record or admission check say v004 (V4_RENAMES).
# Port tags (against v003): every ported result carries its v003 index and v003 tag. It is PORT when the call and the expectation are
# v003's, and PORT_CHANGED when its case invoked the builder (counted by wrapping T4.safe_build and T4.main), whose call now carries MD0;
# 'why4' gives the reason. The port map is checked against TEST_RESULTS_C4V003.json: every v003 case once, in v003's order, with v003's
# tool, tag, r2 index, expectation and text (or its listed rename). v003's own r2 port map is kept and checked as in v003. The v003 fixture
# labels ("Claude4 seal tools v003 tests") are kept verbatim.
# New v004 cases (tags NEW, NEW_CONTROL, REAL_NEW; marked v004_new): every refusal of the new input, by API and CLI:
# MANUAL_DISCLOSURES_REQUIRED (no pin; the v003 argument form; no flags); _PIN_MISMATCH (a missing file, a wrong, capital, foreign or short
# sha, a relative path, a directory, a bare-path, dict, half or three-element pin, a half CLI pin); the typed _JSON_* codes (duplicate keys,
# NaN, -Infinity, a 5,000-digit integer, a duplicate key behind one, a syntax error, trailing data, UTF-16, a BOM, deep nesting); _SHAPE,
# _KEYS, _SCHEMA; _E_R6_1_TEXT_EMPTY and _MISMATCH (another text and one-character differences); the C-08 table and row rules and a
# duplicate NEW id; _C08_CONFIRMATION_EMPTY; the root_disclosures rules and a duplicate id; _TEXT_ENCODING (lone surrogates);
# _CHANGED_AFTER_CHECK at two points of the build; a repeated or abbreviated flag. Positives: the five unchanged files are v003's bytes and
# are the ones imported; E_R6_1 equals SELECTED_R6_C4V001 basis.erratum_E_R6_1 re-read from bytes; the genuine record carries MD0 verbatim
# next to the derived prereg disclosures; root's real SEAL_MANUAL_DISCLOSURES_V001.json (b9db6fd1, read only) is accepted and carried
# verbatim (raw_text is the file's bytes) by API and CLI, and that record passes the v004 admission check and the real guard v008
# admission(); one build opens the file exactly twice (the checked read and the re-read); a v003-form record refuses the v004 admission check.
# Fixtures are built under tests/run_<UTC>/ as in v003; every manual disclosures file there is SYNTHETIC (or a SYNTHETIC copy of root's file
# with one change) and root's file is never written.
# Run inside tools/run_fenced_c4st2.py (fence_c4v002). A local audit hook also refuses process creation, network, deletes and any
# write outside the run folder.
# usage: python3 -I -B ../tools/run_fenced_c4st2.py test_seal_tools_c4v004.py
'''

BOOKKEEPING = r'''import seal_common_c4v003 as C
import check_frozen_addendum_c4v003 as T1
import check_sealed_compare_c4v003 as T2
import check_slot_fill_c4v003 as T3
import build_seal_record_c4v004 as T4
import print_driver_build_record_c4v003 as T5

BUILDER_CALLS = [0]       # v004: builder invocations so far; a ported case that invoked the builder is PORT_CHANGED (its call carries MD0)


def _counted(fn):
    def call(*a, **k):
        BUILDER_CALLS[0] += 1
        return fn(*a, **k)
    call.__wrapped__ = fn
    return call


T4.safe_build, T4.main = _counted(T4.safe_build), _counted(T4.main)


class _Results(list):
    """v004: every appended result is stamped with the builder-call count at that moment (the port classification reads the change)"""
    def append(self, r):
        r['_builder_calls'] = BUILDER_CALLS[0]
        super().append(r)


OPEN_COUNT = {'path': None, 'n': 0}       # v004: opens of one path, counted only while 'path' is set


def _count_hook(event, args):
    if event == 'open' and OPEN_COUNT['path'] is not None and args and isinstance(args[0], (str, bytes, os.PathLike)):
        if os.path.realpath(os.path.abspath(os.fsdecode(args[0]))) == OPEN_COUNT['path']:
            OPEN_COUNT['n'] += 1


sys.addaudithook(_count_hook)
'''

CONSTANTS = r'''EDIT90 = 'SYNTHETIC EDIT INSIDE A90 (Claude4 seal tools v003 tests): not root text.\n'
# v004 (A110): the v003 suite of record (the port map), the v003 sources (the five unchanged copies must be their bytes), prereg r6's SELECTED
# file (E_R6_1) and root's manual disclosures file (read only; only SYNTHETIC copies of it are ever written, in the run folder)
V3 = CA / 'v007_final_prereg_c4/seal_tools_v003'
V3_RESULTS = V3 / 'tests/run_20261019T000810Z/TEST_RESULTS_C4V003.json'
V3_RESULTS_SHA = '26bb912f58fbd2f912c3ca162b4a8f0971fbc2cf556d8a80b87c5a99b188f8df'
V3_SOURCES = {'seal_common_c4v003.py': '101a3aeb9846a21c35993e8e7e4b50a8f1206ed4202b131afd12d7e496c5ab21',
              'check_frozen_addendum_c4v003.py': 'a56f8d793750151920b1b47e77b46aebbfadea71fe77730f360beb02af788fb4',
              'check_sealed_compare_c4v003.py': 'c2c5dfc5ddba1e44ff82811a38d4c05b0a669f2294b229efe3437623d596f9f1',
              'check_slot_fill_c4v003.py': '316973a1abf5aa2151dc1a517733d970ce1004313395d05fe590f82ed439b0af',
              'print_driver_build_record_c4v003.py': 'e5bedffe3c91650d5dba7fbd1ed5476e228158679d8959dfea0e2eff436ebdea',
              'build_seal_record_c4v003.py': 'de0ceb15ebfb95e04227730bd2785eb46af8cb5980012de91de98f34ea226b96'}
R6_SELECTED = CA / 'v007_final_prereg_c4/r6/SELECTED_R6_C4V001.json'
R6_SELECTED_SHA = '7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0'
ROOT_MD = CA / 'seal_assembly_c3/root_inputs/SEAL_MANUAL_DISCLOSURES_V001.json'
ROOT_MD_SHA = 'b9db6fd1716be1e2fb47b6daf9b1e6e81743d6544f9ec72b589cf50fe0fa4ab6'
V4_RENAMES = {
    'genuine: record built, nothing written, guard-shaped pins, pass-through fields, B2 disclosure (real C3V003), later_entry_dispositions = {pin, '
    'content, raw_text} in place of the generic no_change_notes, and the read copy\'s pin (schema C4V003)':
    'genuine: record built, nothing written, guard-shaped pins, pass-through fields, B2 disclosure (real C3V003), later_entry_dispositions = {pin, '
    'content, raw_text} in place of the generic no_change_notes, and the read copy\'s pin (schema C4V004)',
    'real guard v008 admits the v003 SEAL_RECORD (via the checked config); real launcher v007 validate() accepts the bound plan':
    'real guard v008 admits the v004 SEAL_RECORD (via the checked config); real launcher v007 validate() accepts the bound plan',
    'B8 control: the genuine v003 record and its config still pass the v003 admission check and the real guard v008 admission()':
    'B8 control: the genuine v004 record and its config still pass the v004 admission check and the real guard v008 admission()',
    'REAL BUILD_V007: the real guard v008 admission() accepts the config built from the v003 SEAL_RECORD':
    'REAL BUILD_V007: the real guard v008 admission() accepts the config built from the v004 SEAL_RECORD'}
WHY4_MD = ('v004 (A110): the builder call now also carries the SYNTHETIC manual disclosures fixture MD0 (API manual_disclosures=(path, sha256); '
           'CLI --manual-disclosures/--manual-disclosures-sha256), which tool 4 v004 requires; the expectation is v003\'s')
WHY4_EXTRA = {list(V4_RENAMES)[0]: WHY4_MD + ', apart from the record schema, now UNT_V007_SEAL_RECORD_C4V004 (A110: the record content changed)'}
'''

FIXTURE = r'''    D0_TEXT = Path(D0[0]).read_bytes().decode('utf-8')
    # ---------------- v004 (A110): the manual disclosures fixtures, in root's SEAL_MANUAL_DISCLOSURES_V001 form with SYNTHETIC rows and texts;
    # e_r6_1_text is prereg r6's E_R6_1 read from SELECTED_R6_C4V001's bytes (verified above), not taken from tool 4
    E_SEL = C.strict_json_bytes(R6_SELECTED.read_bytes())['basis']['erratum_E_R6_1']
    nmd = [0]

    def md_obj():
        return {'schema': 'SEAL_MANUAL_DISCLOSURES_V001', 'e_r6_1_text': E_SEL,
                'c08_table': [{'new_item_id': 'NEW-71', 'file': 'SYNTHETIC/v004_test_fixture.py', 'line': 7, 'declared_in_r13': False},
                              {'new_item_id': 'NEW-72', 'file': 'SYNTHETIC/v004_test_fixture.py', 'line': 72}],
                'c08_confirmation': 'SYNTHETIC TEST CONFIRMATION (Claude4 seal tools v004 tests): not root\'s C-08 check',
                'root_disclosures': [{'id': 'SYNTH_A1', 'source': 'SYNTHETIC', 'text': 'SYNTHETIC TEST DISCLOSURE (Claude4 seal tools v004 tests): not root\'s'},
                                     {'id': 'SYNTH_A2', 'source': 'SYNTHETIC', 'text': 'SYNTHETIC TEST DISCLOSURE 2 (Claude4 seal tools v004 tests): not root\'s'}]}

    def mdisc(mutate=None, raw=None, name='SEAL_MANUAL_DISCLOSURES_SYNTH_C4V004.json'):
        """a manual disclosures file in the run folder; returns root's pin (path, sha256). mutate(obj) edits the fixture object; raw: the
        exact text or bytes"""
        nmd[0] += 1
        if raw is None:
            obj = md_obj()
            if mutate:
                mutate(obj)
            raw = json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=False) + '\n'
            try:
                raw.encode('utf-8')
            except UnicodeEncodeError:                  # a lone surrogate under test: written as a JSON escape, so the file stays UTF-8 text
                raw = json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=True) + '\n'
        p = xwb(run / ('manual_disclosures_%03d' % nmd[0]) / name, raw if isinstance(raw, bytes) else raw.encode('utf-8'))
        return (str(p), C.sha(p))
    MD0 = mdisc()                                      # the builder's base fixture (args_for, t4_argv)
    MD0_TEXT = Path(MD0[0]).read_bytes().decode('utf-8')
'''

NEW_CASES = r'''    # ================= v004 (A110): tool 4 v004's manual disclosures input (new cases, each marked v004_new)
    use(TOR)

    def rec4(tool, name, res, expect_pass, code=None, tag='NEW', **kw):
        r_ = record(tool, name, res, expect_pass, code, tag=tag, **kw)
        results[-1]['v004_new'] = True
        return r_

    def chk4(tool, name, ok, detail, tag='NEW'):
        check(tool, name, ok, detail, tag=tag)
        results[-1]['v004_new'] = True

    def md4(name, expect_code, md, tag='NEW', exact=True, base=None, **over):
        """a builder run on the base arguments (or base) with manual_disclosures=md: REFUSE with expect_code (exact: the only code), no
        record printed, no INTERNAL_EXCEPTION"""
        b = A()
        b.__dict__.update((base or a).__dict__)
        b.__dict__.update(over)
        b.manual_disclosures = md
        r, t = T4.safe_build(b)
        codes = [f['code'] for f in r['failures']]
        ok = (t is None and r['verdict'] == 'REFUSE' and any(expect_code in c for c in codes) and not any(c.startswith('INTERNAL_EXCEPTION') for c in codes)
              and (not exact or codes == [expect_code]))
        results.append({'tool': 'T4', 'tag': tag, 'r2': None, 'why': None, 'case': 'A110: ' + name, 'expect': 'REFUSE ' + expect_code + (' (only)' if exact else ''),
                        'verdict': r['verdict'], 'codes': codes, 'notes': [], 'ok': ok, 'v004_new': True})
        return r

    def rep(old, new, src=None):
        s = MD0_TEXT if src is None else src
        assert s.count(old) == 1, old
        return s.replace(old, new, 1)

    def jrec(s):
        try:
            return json.loads(s) if s else {}
        except ValueError:
            return {}
    # ---- the five unchanged files, the E_R6_1 constant, root's file
    v3ok = {n: C.sha(V3 / n) == h for n, h in V3_SOURCES.items()}
    v4same = {n: C.sha(TOOLS / n) == h for n, h in V3_SOURCES.items() if n != 'build_seal_record_c4v003.py'}
    mods = ((C, 'seal_common_c4v003.py'), (T1, 'check_frozen_addendum_c4v003.py'), (T2, 'check_sealed_compare_c4v003.py'), (T3, 'check_slot_fill_c4v003.py'),
            (T5, 'print_driver_build_record_c4v003.py'), (T4, 'build_seal_record_c4v004.py'))
    from_v4 = {n: Path(m.__file__).resolve() == (TOOLS / n).resolve() for m, n in mods}
    chk4('T4', 'v004: seal_common and tools 1, 2, 3 and 5 here are v003\'s bytes (the v003 SELECTED cf7e5b2f pins, from bytes), tool 4 is '
         'build_seal_record_c4v004.py, no v003 tool 4 is in this folder, and the suite imported exactly these files', all(v3ok.values()) and all(v4same.values())
         and all(from_v4.values()) and not (TOOLS / 'build_seal_record_c4v003.py').exists(), repr((v3ok, v4same, from_v4))[:400], tag='NEW_CONTROL')
    sel_raw = R6_SELECTED.read_bytes()
    sel = C.strict_json_bytes(sel_raw)
    e_sel = (sel.get('basis') or {}).get('erratum_E_R6_1')
    chk4('T4', 'v004: tool 4\'s E_R6_1 constant equals prereg r6\'s E_R6_1, re-read now from SELECTED_R6_C4V001.json (7200acd9, schema '
         'UNT_V007_SELECTED_PREREG_C4V001, strict parse) basis.erratum_E_R6_1, byte for byte', C.sha_bytes(sel_raw) == R6_SELECTED_SHA
         and sel.get('schema') == 'UNT_V007_SELECTED_PREREG_C4V001' and isinstance(e_sel, str) and e_sel.strip() != '' and T4.E_R6_1 == e_sel
         and T4.E_R6_1.encode('utf-8') == e_sel.encode('utf-8') and E_SEL == e_sel,
         'constant %s, SELECTED %s' % (C.sha_bytes(T4.E_R6_1.encode('utf-8'))[:8], C.sha_bytes(str(e_sel).encode('utf-8'))[:8]), tag='NEW_CONTROL')
    root_raw = ROOT_MD.read_bytes()
    root_text = root_raw.decode('utf-8')
    chk4('T4', 'REAL: root\'s SEAL_MANUAL_DISCLOSURES_V001.json hashes to b9db6fd1 (read only; this suite never writes it)', C.sha_bytes(root_raw) == ROOT_MD_SHA,
         C.sha_bytes(root_raw)[:8], tag='REAL_NEW')
    # ---- positives
    derived = [r['text'] for r in json.loads(sp.read_bytes())['seal_record_requirements'] if isinstance(r, dict) and isinstance(r.get('text'), str)
               and r['text'].startswith('Disclosure')]
    rg, tg = T4.safe_build(a_with())
    recg = jrec(tg)
    mdr0 = recg.get('manual_disclosures') or {}
    chk4('T4', 'v004 control: the base build passes, prints the genuine record bytes, and that record carries manual_disclosures = {pin, content, '
         'raw_text} of MD0 exactly (raw_text hashes to the pin), next to the derived prereg disclosures (the E5-08 list, as in v003); the verdict lists '
         'the pin and notes MANUAL_DISCLOSURES_VERIFIED', rg['verdict'] == 'PASS' and tg == text and set(mdr0) == {'pin', 'content', 'raw_text'}
         and mdr0 == {'pin': {'path': MD0[0], 'sha256': MD0[1]}, 'content': json.loads(MD0_TEXT), 'raw_text': MD0_TEXT}
         and C.sha_bytes(mdr0.get('raw_text', '').encode('utf-8')) == MD0[1] and recg.get('disclosures') == derived and len(derived) == 1
         and derived[0].startswith('Disclosure E5-08') and rg['pins_verified'].get('manual_disclosures') == {'path': MD0[0], 'sha256': MD0[1]}
         and 'MANUAL_DISCLOSURES_VERIFIED' in [n['code'] for n in rg['notes']] and recg.get('schema') == 'UNT_V007_SEAL_RECORD_C4V004',
         repr([f['code'] for f in rg['failures']]) + repr(sorted(mdr0))[:200], tag='NEW_CONTROL')
    rr_, tr_ = T4.safe_build(a_with(manual_disclosures=(str(ROOT_MD), ROOT_MD_SHA)))
    recr = jrec(tr_)
    mdr = recr.get('manual_disclosures') or {}
    root_obj = C.strict_json_bytes(root_raw)
    chk4('T4', 'REAL: root\'s real file b9db6fd1 (API manual_disclosures=(path, sha256)) is accepted, and the SEAL_RECORD carries it verbatim: the pin, '
         'the parsed content, and raw_text equal to the file\'s exact text (its UTF-8 bytes are the file\'s bytes and hash to b9db6fd1)',
         rr_['verdict'] == 'PASS' and tr_ is not None and set(mdr) == {'pin', 'content', 'raw_text'} and mdr.get('pin') == {'path': str(ROOT_MD), 'sha256': ROOT_MD_SHA}
         and mdr.get('content') == root_obj and mdr.get('raw_text') == root_text and mdr.get('raw_text', '').encode('utf-8') == root_raw
         and C.sha_bytes(mdr.get('raw_text', '').encode('utf-8')) == ROOT_MD_SHA and recr.get('disclosures') == derived,
         repr([f['code'] for f in rr_['failures']]), tag='REAL_NEW')
    mc = mdr.get('content') or {}
    chk4('T4', 'REAL: ... the content tool 4 carried from root\'s file: e_r6_1_text is E_R6_1, 19 C-08 rows from NEW-4 to NEW-73 (each declared_in_r13 '
         'false), and the five root disclosures A100_B2_SANITY, A101_B2_DOC_ERRATUM, A105_E_OPS5, A107_P12, A111_P3_P4', mc.get('e_r6_1_text') == e_sel
         and len(mc.get('c08_table') or []) == 19 and [x.get('new_item_id') for x in mc.get('c08_table') or []][::18] == ['NEW-4', 'NEW-73']
         and all(x.get('declared_in_r13') is False for x in mc.get('c08_table') or [])
         and [x.get('id') for x in mc.get('root_disclosures') or []] == ['A100_B2_SANITY', 'A101_B2_DOC_ERRATUM', 'A105_E_OPS5', 'A107_P12', 'A111_P3_P4'],
         repr(sorted(mc))[:200], tag='REAL_NEW')
    i_md = t4_argv.index('--manual-disclosures')
    t4_argv_nomd = t4_argv[:i_md] + t4_argv[i_md + 4:]
    base_cli = t4_argv_nomd + ['--addendum-at-text-of-record', RC0s, '--dispositions', D0[0], '--dispositions-sha', D0[1]]
    rc, so, se = cli(T4.main, base_cli + ['--manual-disclosures', str(ROOT_MD), '--manual-disclosures-sha256', ROOT_MD_SHA])
    chk4('T4', 'REAL: the builder CLI with --manual-disclosures <root\'s file> --manual-disclosures-sha256 b9db6fd1 exits 0 and prints the same record '
         'bytes as the API run, whose sha stderr names; their raw_text is the file\'s bytes', rc == 0 and tr_ is not None and so == tr_
         and jget(se, 'seal_record_sha256') == C.sha_bytes(so.encode('utf-8'))
         and (jrec(so).get('manual_disclosures') or {}).get('raw_text', '').encode('utf-8') == root_raw, 'rc %r codes %r' % (rc, jcodes(se)), tag='REAL_NEW')
    if tr_:
        seal_r = xw(run / 'v004_admission' / 'SEAL_RECORD_WITH_ROOT_MANUAL_DISCLOSURES_SYNTH.json', tr_)
        cfg_r = xw(run / 'v004_admission' / 'ROOT_SEAL_ADMISSION_WITH_ROOT_MANUAL_DISCLOSURES_SYNTH.json', dict(cfg, seal=pin(seal_r)))
        rq = T4.check_admission_config(cfg_r, seal_r)
        G.CONFIG = cfg_r
        os.environ['UNT_ROOT_ADMISSION_SHA256'] = C.sha(cfg_r)
        try:
            G.admission(str(PKT / 'route_a_token_launcher_cx1v007.py'))
            og = 'ok'
        except BaseException as e:
            og = '%s: %s' % (type(e).__name__, e)
    else:
        rq, og = {'verdict': 'NOT_BUILT', 'failures': []}, 'not built'
    chk4('integration', 'REAL: the SEAL_RECORD carrying root\'s real disclosures passes the v004 admission check (B8) and the real guard v008 '
         'admission() (CONFIG patched to a synthetic config pinning it; nothing is started)', rq['verdict'] == 'PASS' and og == 'ok',
         repr([f['code'] for f in rq['failures']]) + ' ' + og, tag='REAL_NEW')
    q3 = copy.deepcopy(rec)
    q3['schema'] = 'UNT_V007_SEAL_RECORD_C4V003'
    q3.pop('manual_disclosures', None)
    s3_p = xw(run / 'v004_admission' / 'SEAL_RECORD_IN_THE_V003_FORM_SYNTH.json', json.dumps(q3, indent=1, sort_keys=True) + '\n')
    c3_p = xw(run / 'v004_admission' / 'ROOT_SEAL_ADMISSION_V003_FORM_SYNTH.json', dict(cfg, seal=pin(s3_p)))
    rec4('T4', 'A110: the v004 admission check refuses a SEAL_RECORD in v003\'s form (schema UNT_V007_SEAL_RECORD_C4V003, no manual_disclosures): '
         'ADMISSION_SEAL_RECORD_SCHEMA', T4.check_admission_config(c3_p, s3_p), False, 'ADMISSION_SEAL_RECORD_SCHEMA')
    r_, t_ = T4.safe_build(a_with(manual_disclosures=mdisc(mutate=lambda o: [x.pop('declared_in_r13', None) for x in o['c08_table']])))
    rec4('T4', 'v004 control: C-08 rows without declared_in_r13 (0646 names three keys) pass', r_, True, tag='NEW_CONTROL')
    r_, t_ = T4.safe_build(a_with(manual_disclosures=mdisc(mutate=lambda o: o['c08_table'][0].update(declared_in_r13=True))))
    rec4('T4', 'v004 control: declared_in_r13 true on a row passes', r_, True, tag='NEW_CONTROL')
    MDc = mdisc(name='SEAL_MANUAL_DISCLOSURES_OPEN_COUNT_C4V004.json')
    OPEN_COUNT['path'], OPEN_COUNT['n'] = os.path.realpath(MDc[0]), 0
    try:
        rc_b, tc_b = T4.safe_build(a_with(manual_disclosures=MDc))
    finally:
        n_open, OPEN_COUNT['path'] = OPEN_COUNT['n'], None
    chk4('T4', 'v004 control: one build opens the disclosures file exactly twice: the checked read (whose bytes are hashed, then parsed) and the '
         're-read just before the record', rc_b['verdict'] == 'PASS' and n_open == 2, 'opens %d, verdict %s' % (n_open, rc_b['verdict']), tag='NEW_CONTROL')
    # ---- MUST_FAIL: the pin
    md4('no manual disclosures (API manual_disclosures=None): MANUAL_DISCLOSURES_REQUIRED, and no record', 'MANUAL_DISCLOSURES_REQUIRED', None)
    b_nomd = A()
    b_nomd.__dict__.update({k: v for k, v in a.__dict__.items() if k != 'manual_disclosures'})
    r_n4, t_n4 = T4.safe_build(b_nomd)
    chk4('T4', 'A110: an argument object with no manual_disclosures attribute (v003\'s form): MANUAL_DISCLOSURES_REQUIRED only, and no record',
         t_n4 is None and [f['code'] for f in r_n4['failures']] == ['MANUAL_DISCLOSURES_REQUIRED'], repr([f['code'] for f in r_n4['failures']]))
    PM = 'MANUAL_DISCLOSURES_PIN_MISMATCH'
    md4('a missing file (the pinned path does not exist)', PM, (MD0[0] + '.missing', MD0[1]))
    md4('a wrong sha (64 zeros)', PM, (MD0[0], '0' * 64))
    md4('the sha in capitals (not the hexdigest of the bytes)', PM, (MD0[0], MD0[1].upper()))
    md4('the sha of another file (the dispositions fixture D0)', PM, (MD0[0], D0[1]))
    md4('an 8-hex sha prefix', PM, (MD0[0], MD0[1][:8]))
    md4('a relative path', PM, (os.path.relpath(MD0[0]), MD0[1]))
    md4('the path is a directory', PM, (str(Path(MD0[0]).parent), MD0[1]))
    md4('the API pin is a bare path, not (path, sha256)', PM, MD0[0])
    md4('the API pin is a {path, sha256} dict, not (path, sha256)', PM, {'path': MD0[0], 'sha256': MD0[1]})
    md4('a half pin (path, None)', PM, (MD0[0], None))
    md4('a half pin (None, sha256)', PM, (None, MD0[1]))
    md4('a three-element pin', PM, (MD0[0], MD0[1], MD0[1]))
    # ---- MUST_FAIL: the strict parse (v003's strict JSON, typed codes)
    J = 'MANUAL_DISCLOSURES_JSON_'
    md4('a duplicate top-level key (strict JSON, A71)', J + 'DUPLICATE_KEY', mdisc(raw=rep('{\n "c08_confirmation"', '{\n "c08_confirmation": "x",\n "c08_confirmation"')))
    md4('a duplicate key inside a C-08 row', J + 'DUPLICATE_KEY', mdisc(raw=rep('"line": 7,', '"line": 7,\n   "line": 8,')))
    md4('a duplicate key inside a root disclosure', J + 'DUPLICATE_KEY', mdisc(raw=rep('"id": "SYNTH_A1",', '"id": "SYNTH_A1",\n   "id": "SYNTH_A9",')))
    md4('a NaN constant (as a C-08 line)', J + 'NON_FINITE_CONSTANT', mdisc(raw=rep('"line": 7,', '"line": NaN,')))
    md4('a -Infinity constant (as a C-08 line)', J + 'NON_FINITE_CONSTANT', mdisc(raw=rep('"line": 7,', '"line": -Infinity,')))
    md4('a 5,000-digit integer as a C-08 line (Python\'s 4,300-digit limit)', J + 'INTEGER_TOO_LONG', mdisc(raw=rep('"line": 7,', '"line": %s,' % big)))
    md4('a duplicate key behind a 5,000-digit integer (A-B1 class; no text fallback)', J, mdisc(raw='{"n": %s, "schema": "SEAL_MANUAL_DISCLOSURES_V001", '
        '"schema": "x"}\n' % big), exact=False)
    md4('a JSON syntax error (the file truncated)', J + 'SYNTAX', mdisc(raw=MD0_TEXT[:-3]))
    md4('a second JSON value after the object', J + 'SYNTAX', mdisc(raw=MD0_TEXT + '{}\n'))
    md4('UTF-16 bytes (the file must be UTF-8 text)', J + 'ENCODING', mdisc(raw=MD0_TEXT.encode('utf-16')))
    md4('a UTF-8 byte-order mark', J + 'SYNTAX', mdisc(raw=b'\xef\xbb\xbf' + MD0_TEXT.encode('utf-8')))
    md4('nesting deep enough to exhaust the parser (a typed code, not a traceback)', J + 'DEFECT', mdisc(raw='[' * 100000))
    # ---- MUST_FAIL: the form
    md4('the file is a JSON list, not an object', 'MANUAL_DISCLOSURES_SHAPE', mdisc(raw=json.dumps([json.loads(MD0_TEXT)]) + '\n'))
    md4('the file is a JSON string', 'MANUAL_DISCLOSURES_SHAPE', mdisc(raw='"SEAL_MANUAL_DISCLOSURES_V001"\n'))
    md4('an extra top-level key', 'MANUAL_DISCLOSURES_KEYS', mdisc(mutate=lambda o: o.update(note='x')))
    md4('a missing top-level key (root_disclosures)', 'MANUAL_DISCLOSURES_KEYS', mdisc(mutate=lambda o: o.pop('root_disclosures')))
    md4('a missing top-level key (e_r6_1_text)', 'MANUAL_DISCLOSURES_KEYS', mdisc(mutate=lambda o: o.pop('e_r6_1_text')))
    md4('an empty object', 'MANUAL_DISCLOSURES_KEYS', mdisc(raw='{}\n'))
    md4('a wrong schema (SEAL_MANUAL_DISCLOSURES_V002)', 'MANUAL_DISCLOSURES_SCHEMA', mdisc(mutate=lambda o: o.update(schema='SEAL_MANUAL_DISCLOSURES_V002')))
    md4('the schema in lower case', 'MANUAL_DISCLOSURES_SCHEMA', mdisc(mutate=lambda o: o.update(schema=o['schema'].lower())))
    md4('the schema null', 'MANUAL_DISCLOSURES_SCHEMA', mdisc(mutate=lambda o: o.update(schema=None)))
    E = 'MANUAL_DISCLOSURES_E_R6_1_TEXT_'
    md4('an empty e_r6_1_text', E + 'EMPTY', mdisc(mutate=lambda o: o.update(e_r6_1_text='')))
    md4('a whitespace-only e_r6_1_text', E + 'EMPTY', mdisc(mutate=lambda o: o.update(e_r6_1_text=' \n\t ')))
    md4('an e_r6_1_text that is not a string (null)', E + 'EMPTY', mdisc(mutate=lambda o: o.update(e_r6_1_text=None)))
    md4('another text as e_r6_1_text (r6 SELECTED basis.own_refuter)', E + 'MISMATCH', mdisc(mutate=lambda o: o.update(e_r6_1_text=sel['basis']['own_refuter'])))
    one = (('the last character changed (. to !)', lambda s: s[:-1] + '!'),
           ('one digit changed (the first r13 to r14)', lambda s: s.replace('r13', 'r14', 1)),
           ('one character deleted (the first comma)', lambda s: s.replace(',', '', 1)),
           ('one character added (a trailing space)', lambda s: s + ' '),
           ('one character added (a leading space)', lambda s: ' ' + s),
           ('a straight double quote replaced by U+201C', lambda s: s.replace('"', '“', 1)),
           ('the first letter in lower case', lambda s: s[0].lower() + s[1:]),
           ('a non-breaking space for the first space', lambda s: s.replace(' ', ' ', 1)),
           ('the ASCII ... replaced by U+2026 (visually alike)', lambda s: s.replace('...', '…', 1)))
    for nm_, f_ in one:
        e2 = f_(e_sel)
        assert e2 != e_sel, nm_
        md4('e_r6_1_text differs from E_R6_1: %s' % nm_, E + 'MISMATCH', mdisc(mutate=lambda o, e2=e2: o.update(e_r6_1_text=e2)))
    T8 = 'MANUAL_DISCLOSURES_C08_'
    md4('c08_table an empty list', T8 + 'TABLE_SHAPE', mdisc(mutate=lambda o: o.update(c08_table=[])))
    md4('c08_table an object, not a list', T8 + 'TABLE_SHAPE', mdisc(mutate=lambda o: o.update(c08_table={'NEW-71': 7})))
    md4('c08_table null', T8 + 'TABLE_SHAPE', mdisc(mutate=lambda o: o.update(c08_table=None)))
    rows_bad = (('a row that is a string', lambda r: 'NEW-71'),
                ('a row with an extra key', lambda r: dict(r, note='x')),
                ('a row without line', lambda r: {k: v for k, v in r.items() if k != 'line'}),
                ('a row without new_item_id', lambda r: {k: v for k, v in r.items() if k != 'new_item_id'}),
                ('a row without file', lambda r: {k: v for k, v in r.items() if k != 'file'}),
                ('line 0', lambda r: dict(r, line=0)),
                ('a negative line', lambda r: dict(r, line=-3)),
                ('line as a string ("7")', lambda r: dict(r, line='7')),
                ('line true (a bool is not an integer)', lambda r: dict(r, line=True)),
                ('line 7.0 (a float)', lambda r: dict(r, line=7.0)),
                ('line null', lambda r: dict(r, line=None)),
                ('new_item_id not a string (71)', lambda r: dict(r, new_item_id=71)),
                ('new_item_id not of the form NEW-<n> (NEW71)', lambda r: dict(r, new_item_id='NEW71')),
                ('new_item_id with a trailing newline', lambda r: dict(r, new_item_id='NEW-71\n')),
                ('new_item_id with fullwidth digits', lambda r: dict(r, new_item_id='NEW-７１')),
                ('new_item_id with four digits', lambda r: dict(r, new_item_id='NEW-1071')),
                ('an empty file', lambda r: dict(r, file='')),
                ('a whitespace-only file', lambda r: dict(r, file='  ')),
                ('file not a string (a list)', lambda r: dict(r, file=['x'])),
                ('declared_in_r13 "false" (a string)', lambda r: dict(r, declared_in_r13='false')),
                ('declared_in_r13 0 (an integer)', lambda r: dict(r, declared_in_r13=0)),
                ('declared_in_r13 null', lambda r: dict(r, declared_in_r13=None)))
    for nm_, f_ in rows_bad:
        md4('a bad C-08 row: %s' % nm_, T8 + 'ROW', mdisc(mutate=lambda o, f_=f_: o['c08_table'].__setitem__(0, f_(o['c08_table'][0]))))
    md4('one NEW id twice in c08_table', T8 + 'DUPLICATE_ID', mdisc(mutate=lambda o: o['c08_table'].append(dict(o['c08_table'][0], line=8))))
    md4('an empty c08_confirmation', T8 + 'CONFIRMATION_EMPTY', mdisc(mutate=lambda o: o.update(c08_confirmation='')))
    md4('a whitespace-only c08_confirmation', T8 + 'CONFIRMATION_EMPTY', mdisc(mutate=lambda o: o.update(c08_confirmation='\n ')))
    md4('a c08_confirmation that is a list', T8 + 'CONFIRMATION_EMPTY', mdisc(mutate=lambda o: o.update(c08_confirmation=['checked'])))
    RD = 'MANUAL_DISCLOSURES_ROOT_DISCLOSURE'
    md4('root_disclosures an object, not a list', RD + 'S_SHAPE', mdisc(mutate=lambda o: o.update(root_disclosures={'SYNTH_A1': 'x'})))
    md4('root_disclosures an empty list (A110.3 names the disclosures root carries)', RD + 'S_SHAPE', mdisc(mutate=lambda o: o.update(root_disclosures=[])))
    rd_bad = (('a row that is a string', lambda x: 'SYNTH_A1'),
              ('a row with an extra key', lambda x: dict(x, note='x')),
              ('a row without source', lambda x: {k: v for k, v in x.items() if k != 'source'}),
              ('a row without text', lambda x: {k: v for k, v in x.items() if k != 'text'}),
              ('an empty text', lambda x: dict(x, text='')),
              ('a whitespace-only source', lambda x: dict(x, source=' ')),
              ('an id that is not a string', lambda x: dict(x, id=1)),
              ('an empty id', lambda x: dict(x, id='')))
    for nm_, f_ in rd_bad:
        md4('a bad root disclosure: %s' % nm_, RD + '_ROW', mdisc(mutate=lambda o, f_=f_: o['root_disclosures'].__setitem__(0, f_(o['root_disclosures'][0]))))
    md4('two root disclosures with one id', RD + '_DUPLICATE_ID', mdisc(mutate=lambda o: o['root_disclosures'].append(dict(o['root_disclosures'][0], text='another text'))))
    md4('a lone surrogate in c08_confirmation (a JSON escape; no UTF-8 form): a typed code, not INTERNAL_EXCEPTION', 'MANUAL_DISCLOSURES_TEXT_ENCODING',
        mdisc(mutate=lambda o: o.update(c08_confirmation='SYNTHETIC \ud800 confirmation')))
    md4('a lone surrogate in a root disclosure text', 'MANUAL_DISCLOSURES_TEXT_ENCODING', mdisc(mutate=lambda o: o['root_disclosures'][0].update(text='SYNTHETIC \udc00 text')))
    md4('a lone surrogate in a C-08 file', 'MANUAL_DISCLOSURES_TEXT_ENCODING', mdisc(mutate=lambda o: o['c08_table'][0].update(file='SYNTHETIC/\ud83d.py')))
    assert root_text.count('states this erratum.') == 1
    md4('REAL: a SYNTHETIC copy of root\'s file whose e_r6_1_text ends "erratum!" instead of "erratum." refuses MANUAL_DISCLOSURES_E_R6_1_TEXT_MISMATCH',
        E + 'MISMATCH', mdisc(raw=root_text.replace('states this erratum.', 'states this erratum!', 1), name='SEAL_MANUAL_DISCLOSURES_ROOT_COPY_ONE_CHAR_C4V004.json'),
        tag='REAL_NEW')
    # ---- MUST_FAIL: the file changes after the check (SYNTHETIC work copies in the run folder; root's file is never written)
    MDm = mdisc(name='SEAL_MANUAL_DISCLOSURES_CHANGED_DURING_TOOLS_1_3_C4V004.json')
    MDm2 = mdisc(name='SEAL_MANUAL_DISCLOSURES_CHANGED_BEFORE_THE_REREAD_C4V004.json')
    orig_t3_run, orig_led = T3.run, T4.later_entry_dispositions

    def t3_then_append(*args_, **kw_):
        r = orig_t3_run(*args_, **kw_)
        with open(MDm[0], 'a') as f:
            f.write(' ')
        return r

    def append_then_led(*args_, **kw_):
        with open(MDm2[0], 'a') as f:
            f.write('\n')
        return orig_led(*args_, **kw_)
    for nm_, where_, fn_, mm in (('bytes appended while tools 1-3 run (after the checked read)', 'T3', t3_then_append, MDm),
                                 ('bytes appended during the last step before the re-read (the dispositions re-read)', 'LED', append_then_led, MDm2)):
        if where_ == 'T3':
            T3.run = fn_
        else:
            T4.later_entry_dispositions = fn_
        try:
            r_m, t_m = T4.safe_build(a_with(manual_disclosures=mm))
        finally:
            T3.run, T4.later_entry_dispositions = orig_t3_run, orig_led
        cm = [f['code'] for f in r_m['failures']]
        results.append({'tool': 'T4', 'tag': 'NEW', 'r2': None, 'why': None, 'case': 'A110: the disclosures file changes after the check: %s: '
                        'MANUAL_DISCLOSURES_CHANGED_AFTER_CHECK only, and no record' % nm_, 'expect': 'REFUSE MANUAL_DISCLOSURES_CHANGED_AFTER_CHECK (only)',
                        'verdict': r_m['verdict'], 'codes': cm, 'notes': [], 'ok': t_m is None and cm == ['MANUAL_DISCLOSURES_CHANGED_AFTER_CHECK']
                        and C.sha(mm[0]) != mm[1], 'v004_new': True})
    r_c4, t_c4 = T4.safe_build(a_with())
    chk4('T4', 'v004 control: with both patches removed the base build passes again and prints the genuine record bytes', r_c4['verdict'] == 'PASS'
         and t_c4 == text and T3.run is orig_t3_run and T4.later_entry_dispositions is orig_led, repr([f['code'] for f in r_c4['failures']]), tag='NEW_CONTROL')
    p_l, sp_l = variant('v004_layered_pending', lambda s: s.update(producer_registry={'path': str(preg), 'sha256': 'PENDING_ROOT_AT_SEAL_ASSEMBLY'}))
    r_l, t_l = T4.safe_build(a_with(slots=str(p_l), prereg=str(sp_l), manual_disclosures=(MD0[0], '0' * 64)))
    cl = [f['code'] for f in r_l['failures']]
    chk4('T4', 'A110 (D-08 class): a bad disclosures pin and a slot-fill refusal are reported together (MANUAL_DISCLOSURES_PIN_MISMATCH and T3: codes), '
         'and no record', t_l is None and 'MANUAL_DISCLOSURES_PIN_MISMATCH' in cl and any(c.startswith('T3:') for c in cl), repr(cl)[:300])
    # ---- the CLI
    rc, so, se = cli(T4.main, base_cli)
    chk4('T4', 'A110: the builder CLI without --manual-disclosures exits 2, prints no record bytes, and refuses MANUAL_DISCLOSURES_REQUIRED on stderr',
         rc == 2 and so == '' and jcodes(se) == ['MANUAL_DISCLOSURES_REQUIRED'], 'rc %r stdout %r codes %r' % (rc, so[:60], jcodes(se)))
    rc, so, se = cli(T4.main, base_cli + ['--manual-disclosures', MD0[0]])
    chk4('T4', 'A110: --manual-disclosures without --manual-disclosures-sha256 exits 2, prints no record bytes, MANUAL_DISCLOSURES_PIN_MISMATCH',
         rc == 2 and so == '' and jcodes(se) == [PM], 'rc %r stdout %r codes %r' % (rc, so[:60], jcodes(se)))
    rc, so, se = cli(T4.main, base_cli + ['--manual-disclosures-sha256', MD0[1]])
    chk4('T4', 'A110: --manual-disclosures-sha256 without --manual-disclosures exits 2, prints no record bytes, MANUAL_DISCLOSURES_PIN_MISMATCH',
         rc == 2 and so == '' and jcodes(se) == [PM], 'rc %r stdout %r codes %r' % (rc, so[:60], jcodes(se)))
    rc, so, se = cli(T4.main, base_cli + ['--manual-disclosures', MD0[0], '--manual-disclosures-sha256', MD0[1], '--manual-disclosures', MD0[0]])
    chk4('T4', 'A110: --manual-disclosures given twice exits 2 with CLI_REPEATED_FLAG (no record)', rc == 2 and jcodes(so) == ['CLI_REPEATED_FLAG']
         and jget(so, 'seal_record_sha256') is None, 'rc %r codes %r' % (rc, jcodes(so)))
    rc, so, se = cli(T4.main, base_cli + ['--manual-disc', MD0[0], '--manual-disclosures-sha256', MD0[1]])
    chk4('T4', 'A110: an abbreviated flag (--manual-disc) is refused (no abbreviations): exit 2, CLI_ARGUMENTS', rc == 2 and jcodes(so) == ['CLI_ARGUMENTS'],
         'rc %r codes %r' % (rc, jcodes(so)))
    MDx = mdisc(mutate=lambda o: o.update(e_r6_1_text=o['e_r6_1_text'][:-1] + '!'))
    rc, so, se = cli(T4.main, base_cli + ['--manual-disclosures', MDx[0], '--manual-disclosures-sha256', MDx[1]])
    chk4('T4', 'A110: through the CLI, a one-character e_r6_1_text difference exits 2, prints no record bytes, MANUAL_DISCLOSURES_E_R6_1_TEXT_MISMATCH',
         rc == 2 and so == '' and jcodes(se) == [E + 'MISMATCH'], 'rc %r stdout %r codes %r' % (rc, so[:60], jcodes(se)))
    rc, so, se = cli(T4.main, base_cli + ['--manual-disclosures=' + MD0[0], '--manual-disclosures-sha256=' + MD0[1]])
    chk4('T4', 'v004 control: the = forms --manual-disclosures=P --manual-disclosures-sha256=H print the genuine record bytes', rc == 0 and so == text,
         'rc %r codes %r' % (rc, jcodes(se)), tag='NEW_CONTROL')
'''

SUMMARY = r'''    # ================= the port maps: every v003 case once, in v003's order (TEST_RESULTS_C4V003.json 26bb912f); every r2 case once, by index (v003's)
    v3res = json.loads(V3_RESULTS.read_bytes())['results']
    last = 0
    for r in results:
        cnt = r.pop('_builder_calls')
        r['builder_called'] = cnt > last
        last = cnt
    ported = [r for r in results if not r.get('v004_new')]
    port4_problems = [] if len(ported) == len(v3res) == 352 else ['%d ported results; v003 has %d' % (len(ported), len(v3res))]
    for i, (r, v) in enumerate(zip(ported, v3res)):
        r['v003'], r['v003_case'] = i, v['case']
        r['v003_tag'], r['v003_why'] = r.pop('tag'), r.pop('why', None)
        if (r['case'] != V4_RENAMES.get(v['case'], v['case']) or r['tool'] != v['tool'] or r['v003_tag'] != v['tag'] or r.get('r2') != v.get('r2')
                or r['expect'] != v['expect']):
            port4_problems.append('v003[%d] %s' % (i, v['case'][:100]))
        r['tag'], r['why4'] = ('PORT_CHANGED', WHY4_EXTRA.get(v['case'], WHY4_MD)) if r['builder_called'] else ('PORT', None)
    used_renames = sorted(v['case'] for v in v3res if v['case'] in V4_RENAMES)
    if used_renames != sorted(V4_RENAMES):
        port4_problems.append('renames not all used: %r' % sorted(set(V4_RENAMES) - set(used_renames)))
    bad_tags4 = [r['case'] for r in ported if r['tag'] == 'PORT_CHANGED' and not r.get('why4')]
    port4_ok = not port4_problems
    r2res = json.loads(R2_RESULTS.read_bytes())['results']
    r2ported = sorted(r['r2'] for r in results if r.get('r2') is not None)
    port_ok = r2ported == list(range(len(r2res))) and len(r2res) == 148
    for r in results:
        if r.get('r2') is not None:
            r['r2_tag'], r['r2_case'] = r2res[r['r2']]['tag'], r2res[r['r2']]['case']
    bad_tags = [r['case'] for r in ported if r['v003_tag'] == 'PORT_CHANGED' and not r.get('v003_why')]
    summary = {'tool': 'test_seal_tools_c4v004.py', 'tool_sha256': C.sha(__file__), 'run_dir': str(run), 'utc': stamp,
               'tools': {n: C.sha(TOOLS / n) for n in ('seal_common_c4v003.py', 'check_frozen_addendum_c4v003.py', 'check_sealed_compare_c4v003.py',
                                                        'check_slot_fill_c4v003.py', 'build_seal_record_c4v004.py', 'print_driver_build_record_c4v003.py')},
               'inputs_read': {str(p): C.sha(p) for p in [R4, R12, R12_IMPL, R13, R13_IMPL, DRIVER, CHECK_MD, COMPARATOR, REGISTRY, REGISTRY_V007, DRAFT_CASE_BLOCK, B2_REC,
                                                          B2_REC_V002, BUILD_V007, TEMPLATE_V011, PKT / 'BUILD_V005.md', BUILD_V006, PKT / 'P128/LAUNCH_PLAN_V010.json',
                                                          PKT / 'DRY_R5_MS128_V004.json', PKT / 'bind_sealed_launch_plan_cx1v001.py', PKT / 'producer_guard_cx1v008.py',
                                                          PKT / 'route_a_token_launcher_cx1v007.py', PKT / 'route_a_token_launcher_cx1v006.py', R2 / 'seal_common_c4v002.py',
                                                          R2 / 'check_frozen_addendum_c4v002.py', R2_RESULTS, CX3_LATER[0], CX3_LATER[1], CX3_CHANGED[0], CX3_CHANGED[1],
                                                          CX1_PV[0], CX1_PV[1], CX1_PV[2], CX1_OLD_A90, R5_READ, V3_RESULTS, R6_SELECTED, ROOT_MD]
                               + [R5] + list(CERTS.values()) + list(IDENTITY_FILES.values()) + [V3 / n for n in V3_SOURCES]},
               'frozen_copy_of_the_open_V005': {'path': str(frozen), 'sha256': C.sha(frozen), 'entries': 'A47-A%d' % NMAX, 'later_entries_for_prereg_r5': cov5},
               'fixtures': {'text_of_record_standin': pin(TOR), 'read_copy_RC0': pin(RC0), 'read_copy_full': pin(RCF), 'case_block': pin(cbf),
                            'driver_build_record': rpin(dbr), 'build_v007_standin': pin(b7), 'template': pin(template), 'bound_plan': rpin(plan_p),
                            'bound_plan_real_build_v007': rpin(plan_r), 'bound_plan_A90_edited': rpin(plan_90p), 'cascade_addendum_standin': rpin(cma),
                            'seal_record': pin(seal_p), 'prereg_revision_standin': REV, 'dispositions_D0': {'path': D0[0], 'sha256': D0[1]},
                            'dispositions_D5_prereg_r5': {'path': D5[0], 'sha256': D5[1]}, 'dispositions_D_90': {'path': D_90[0], 'sha256': D_90[1]},
                            'frozen_A62_edited': pin(f_62), 'frozen_A90_edited': pin(f_90), 'cx1_pv_d05_1_read_copy': pin(rc_cx),
                            'manual_disclosures_MD0': {'path': MD0[0], 'sha256': MD0[1]}},
               'port_v003': {'v003_results': {'path': str(V3_RESULTS), 'sha256': V3_RESULTS_SHA}, 'v003_cases': len(v3res), 'ported': len(ported),
                             'each_once_in_order': port4_ok, 'problems': port4_problems, 'renamed': V4_RENAMES,
                             'port_changed_v003_indexes': [r['v003'] for r in ported if r['tag'] == 'PORT_CHANGED'],
                             'port_changed_without_reason': bad_tags4, 'new_v004_cases': sum(1 for r in results if r.get('v004_new'))},
               'port': {'r2_cases': len(r2res), 'ported': len(r2ported), 'each_once': port_ok, 'port_changed_without_reason': bad_tags},
               'results': results, 'passed': sum(r['ok'] for r in results), 'total': len(results),
               'by_tag': {t: '%d/%d' % (sum(r['ok'] for r in results if r['tag'] == t), sum(1 for r in results if r['tag'] == t)) for t in sorted({r['tag'] for r in results})}}
    with open(run / 'TEST_RESULTS_C4V004.json', 'x') as f:
        json.dump(summary, f, indent=1)
    for r in results:
        print('%-11s %-12s %-4s %-96s %-7s %s' % (r['tool'], r['tag'], '' if r.get('v003') is None else r['v003'], r['case'][:96], 'ok' if r['ok'] else 'NOT_OK',
                                               '' if r['ok'] else r['codes']))
    print('passed', summary['passed'], '/', summary['total'], summary['by_tag'], 'port_v003', {k: v for k, v in summary['port_v003'].items() if k != 'renamed'},
          'port', summary['port'])
    return 0 if summary['passed'] == summary['total'] and port_ok and not bad_tags and port4_ok and not bad_tags4 else 1
'''


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    out = Path(sys.argv[1])
    src = V3_TESTS.read_bytes()
    assert sha(src) == V3_TESTS_SHA, 'v003 tests are not 67dd8a00'
    text = src.decode('utf-8')
    lines = text.splitlines(keepends=True)
    old_header = ''.join(lines[:36])
    assert old_header.startswith('# Claude4 seal tools v003: tamper tests') and old_header.endswith('test_seal_tools_c4v003.py\n'), old_header[-80:]
    i0 = text.index('    # ================= the port map: every r2 case once, by index (r2 TEST_RESULTS_C4V002.json 6de5ab43)\n')
    end = "    return 0 if summary['passed'] == summary['total'] and port_ok and not bad_tags else 1\n"
    i1 = text.index(end) + len(end)
    old_summary = text[i0:i1]
    R = [(old_header, HEADER),
         ('import seal_common_c4v003 as C\nimport check_frozen_addendum_c4v003 as T1\nimport check_sealed_compare_c4v003 as T2\nimport check_slot_fill_c4v003 as T3\n'
          'import build_seal_record_c4v003 as T4\nimport print_driver_build_record_c4v003 as T5\n', BOOKKEEPING),
         ("EDIT90 = 'SYNTHETIC EDIT INSIDE A90 (Claude4 seal tools v003 tests): not root text.\\n'\n", CONSTANTS),
         ('    for p, h in REAL_SHAS.items():\n        assert C.sha(p) == h, p\n',
          '    for p, h in REAL_SHAS.items():\n        assert C.sha(p) == h, p\n'
          '    for p, h in ((V3_RESULTS, V3_RESULTS_SHA), (R6_SELECTED, R6_SELECTED_SHA)):          # v004: the port map and the E_R6_1 source\n'
          '        assert C.sha(p) == h, p\n'),
         ('    results = []\n', '    results = _Results()                              # v004: stamped with the builder-call count (port tags)\n'),
         ("    D0_TEXT = Path(D0[0]).read_bytes().decode('utf-8')\n", FIXTURE),
         ('        a.addendum_at_text_of_record = RC0s\n',
          '        a.addendum_at_text_of_record = RC0s\n'
          '        a.manual_disclosures = MD0                        # v004 (A110): the SYNTHETIC manual disclosures fixture\n'),
         ("rec.get('schema') == 'UNT_V007_SEAL_RECORD_C4V003'\n", "rec.get('schema') == 'UNT_V007_SEAL_RECORD_C4V004'\n"),
         ("                    '(schema C4V003)',\n", "                    '(schema C4V004)',\n"),
         ("               '--new-item-list', str(newl), '--successor-custody', str(cust), '--b2-record', str(B2_REC)]\n",
          "               '--new-item-list', str(newl), '--successor-custody', str(cust), '--b2-record', str(B2_REC),\n"
          "               '--manual-disclosures', MD0[0], '--manual-disclosures-sha256', MD0[1]]          # v004 (A110): MD0\n"),
         ("'case': 'real guard v008 admits the v003 SEAL_RECORD (via", "'case': 'real guard v008 admits the v004 SEAL_RECORD (via"),
         ("    check('integration', 'B8 control: the genuine v003 record and its config still pass the v003 admission check and the real guard v008 admission()',\n",
          "    check('integration', 'B8 control: the genuine v004 record and its config still pass the v004 admission check and the real guard v008 admission()',\n"),
         ("                        'v003 SEAL_RECORD', 'expect': 'PASS'", "                        'v004 SEAL_RECORD', 'expect': 'PASS'"),
         ("    G.CONFIG = run / 'NO_CONFIG_AFTER_TESTS.json'\n", NEW_CASES + "    G.CONFIG = run / 'NO_CONFIG_AFTER_TESTS.json'\n"),
         (old_summary, SUMMARY)]
    for old, new in R:
        k = text.count(old)
        if k != 1:
            raise SystemExit('REFUSED: an old text occurs %d times (not once): %r' % (k, old[:120]))
        text = text.replace(old, new, 1)
    compile(text, str(out), 'exec')
    b = text.encode('utf-8')
    with open(out, 'xb') as f:
        f.write(b)
    if sha(out.read_bytes()) != sha(b):
        raise SystemExit('REFUSED: the written bytes re-read differently')
    print(sha(b), out, '%d replacements' % len(R))


if __name__ == '__main__':
    main()
