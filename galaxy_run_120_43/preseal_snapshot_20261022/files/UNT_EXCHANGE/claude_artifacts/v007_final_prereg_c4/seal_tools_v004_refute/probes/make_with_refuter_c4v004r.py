# Claude4 seal tools v004 REFUTE stage (C4V004R; A110, dispatch 0646): writes v004/tests/test_seal_tools_c4v004_with_refuter.py, the v004
# suite (ee237685, copied byte for byte into v004/tests/) with ONE block of refuter probes inserted right before its end-of-run cleanup
# (exact-once anchor), its results file renamed (exact-once), and a header line. The block runs the real builder on the suite's own base
# fixture; every probe is tagged REFUTER and marked v004_new, so the v003/r2 port maps are unchanged. Exclusive create; the text is compiled
# before it is written; any anchor miss refuses (exit 1) before anything is written.
# usage: python3 -I -B make_with_refuter_c4v004r.py
import hashlib, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / 'v004/tests/test_seal_tools_c4v004.py'
DST = HERE.parent / 'v004/tests/test_seal_tools_c4v004_with_refuter.py'
SRC_SHA = 'ee237685e24d6efd799f441a4e7340009e1bc65064f86b62d5be6071dfa417e8'
ANCHOR = "    G.CONFIG = run / 'NO_CONFIG_AFTER_TESTS.json'\n"
RES_OLD = "    with open(run / 'TEST_RESULTS_C4V004.json', 'x') as f:\n"
RES_NEW = "    with open(run / 'TEST_RESULTS_C4V004_WITH_REFUTER_C4V004R.json', 'x') as f:\n"
HEADER = ('# REFUTER COPY (Claude4 seal tools v004 refute stage, C4V004R): test_seal_tools_c4v004.py ee237685 byte for byte, plus one inserted block of\n'
          '# refuter probes (tag REFUTER) before the end-of-run cleanup, and the results file renamed. Written by probes/make_with_refuter_c4v004r.py.\n')
BLOCK = r'''    # ================= REFUTER C4V004R (Claude4 seal tools v004 refute stage): bypass probes through the real builder (tag REFUTER, v004_new)
    # MUST_FAIL: ok means the bypass failed (REFUSE with exactly the expected code and no record printed). CONTROL / OBSERVE / REAL: ok means the
    # stated behaviour holds. Every manual disclosures file here is SYNTHETIC (or root's real file, read only); nothing outside the run folder is written.
    RF = []
    rf_dir = run / 'refuter_c4v004r'
    rf_dir.mkdir()

    def rf(name, ok, detail, expect, kind='MUST_FAIL'):
        results.append({'tool': 'T4', 'tag': 'REFUTER', 'r2': None, 'why': None, 'case': 'REFUTER %s: %s' % (kind, name), 'expect': expect,
                        'verdict': 'PASS' if ok else 'FAIL', 'codes': [str(detail)[:400]], 'notes': [], 'ok': bool(ok), 'v004_new': True})
        RF.append({'kind': kind, 'case': name, 'expect': expect, 'ok': bool(ok), 'detail': str(detail)[:800]})

    def build_md(md, **over):
        b = A()
        b.__dict__.update(a.__dict__)
        b.__dict__.update(over)
        b.manual_disclosures = md
        return T4.safe_build(b)

    def must_refuse(name, md, code, **over):
        r, t = build_md(md, **over)
        codes = [f['code'] for f in r['failures']]
        ok = t is None and r['verdict'] == 'REFUSE' and codes == [code]
        rf(name, ok, 'verdict %s codes %r record_printed %s' % (r['verdict'], codes, t is not None), 'REFUSE %s (only), no record' % code)
        return r, t
    base_rec = jrec(text)

    def must_accept_verbatim(name, md, kind='CONTROL', extra=None):
        r, t = build_md(md)
        rec_ = jrec(t)
        m = rec_.get('manual_disclosures') or {}
        fb = Path(md[0]).read_bytes()
        rt = m.get('raw_text')
        ok = (r['verdict'] == 'PASS' and t is not None and set(m) == {'pin', 'content', 'raw_text'} and m.get('pin') == {'path': md[0], 'sha256': md[1]}
              and isinstance(rt, str) and rt.encode('utf-8') == fb and C.sha_bytes(rt.encode('utf-8')) == md[1] and m.get('content') == C.strict_json_bytes(fb)
              and rec_.get('schema') == 'UNT_V007_SEAL_RECORD_C4V004' and rec_.get('disclosures') == base_rec.get('disclosures')
              and {k: v for k, v in rec_.items() if k != 'manual_disclosures'} == {k: v for k, v in base_rec.items() if k != 'manual_disclosures'}
              and r['pins_verified'].get('manual_disclosures') == {'path': md[0], 'sha256': md[1]} and (extra is None or bool(extra(m))))
        rf(name, ok, 'verdict %s codes %r' % (r['verdict'], [f['code'] for f in r['failures']]), 'PASS; the record carries the file verbatim (pin, strict parse, '
           'raw_text == the bytes) and every other record field equals the genuine record\'s', kind)
        return r, t
    E0 = E_SEL
    assert E0 == T4.E_R6_1
    i_sp, i_e = E0.index(' '), E0.index('e')
    EM, EE = 'MANUAL_DISCLOSURES_E_R6_1_TEXT_MISMATCH', 'MANUAL_DISCLOSURES_E_R6_1_TEXT_EMPTY'
    # ---- R1: e_r6_1_text that is not exactly E_R6_1 (unicode and whitespace variants), through the builder
    variants = [
        ('a trailing LF', E0 + '\n'), ('a trailing CRLF', E0 + '\r\n'), ('a trailing CR', E0 + '\r'), ('a leading U+FEFF inside the string', '\ufeff' + E0),
        ('a trailing U+FEFF', E0 + '\ufeff'), ('U+200B zero-width space after the first word', E0[:i_sp] + '\u200b' + E0[i_sp:]),
        ('U+200D zero-width joiner at the end', E0 + '\u200d'), ('U+00AD soft hyphen inside refuter', E0.replace('refuter', 'ref\u00aduter', 1)),
        ('U+2060 word joiner after the first word', E0[:i_sp] + '\u2060' + E0[i_sp:]), ('U+200E left-to-right mark at the start', '\u200e' + E0),
        ('Cyrillic U+0435 for the first Latin e', E0[:i_e] + '\u0435' + E0[i_e + 1:]), ('Greek U+03A4 for the initial T', '\u03a4' + E0[1:]),
        ('U+0301 combining acute after the first e', E0[:i_e + 1] + '\u0301' + E0[i_e + 1:]), ('U+FF0E fullwidth full stop at the end', E0[:-1] + '\uff0e'),
        ('U+FF34 fullwidth T at the start (NFKC-equal)', '\uff34' + E0[1:]), ('U+2013 en dash in seal-record', E0.replace('seal-record', 'seal\u2013record', 1)),
        ('U+2011 non-breaking hyphen in seal-record', E0.replace('seal-record', 'seal\u2011record', 1)), ('two spaces for the first space', E0.replace(' ', '  ', 1)),
        ('a tab for the first space', E0.replace(' ', '\t', 1)), ('U+3000 ideographic space for the first space', E0.replace(' ', '\u3000', 1)),
        ('U+2009 thin space for the first space', E0.replace(' ', '\u2009', 1)), ('U+2028 line separator at the end', E0 + '\u2028'),
        ('U+00A0 no-break space at the end', E0 + '\u00a0'), ('U+201C/U+201D for the straight quotes', E0.replace('"the IMPL"', '\u201cthe IMPL\u201d', 1)),
        ('a NUL at the end (a \\u0000 escape)', E0 + '\u0000'), ('the last character dropped', E0[:-1]), ('the text twice', E0 + E0),
        ('the text twice with a space', E0 + ' ' + E0), ('... shortened to ..', E0.replace('...', '..', 1)),
        ('the short sha 274f7049... expanded to the full sha', E0.replace('274f7049...', '274f7049ece71339d39395b434e7e08bfab33067e3e600d17b4a3bde43fb74a3', 1)),
        ('upper case', E0.upper()), ('re-issuing r6 changed to re-issuing r7', E0.replace('re-issuing r6', 're-issuing r7', 1)),
        ('one space only', ' '), ('U+3000 only (whitespace)', '\u3000'), ('U+200B only (not whitespace)', '\u200b')]
    for nm_, e2 in variants:
        assert e2 != E0, nm_
        must_refuse('e_r6_1_text is not exactly E_R6_1: %s' % nm_, mdisc(mutate=lambda o, e2=e2: o.update(e_r6_1_text=e2)), EE if not e2.strip() else EM)
    for nm_, e2 in (('a list holding E_R6_1', [E0]), ('an object holding E_R6_1', {'text': E0}), ('the number 0', 0), ('true', True), ('false', False)):
        must_refuse('e_r6_1_text is not a string: %s' % nm_, mdisc(mutate=lambda o, e2=e2: o.update(e_r6_1_text=e2)), EE)
    # ---- R2: JSON spellings of the same text (OBSERVE: the comparison is on the parsed text; raw_text keeps the spelling)
    e_json = json.dumps(E0, ensure_ascii=False)
    assert MD0_TEXT.count(e_json) == 1 and '/' in E0
    esc_all = '"' + ''.join('\\u%04x' % ord(ch) for ch in E0) + '"'
    must_accept_verbatim('e_r6_1_text spelled entirely as \\uXXXX escapes (the same text): accepted by parsed equality; raw_text keeps the escaped bytes',
                         mdisc(raw=MD0_TEXT.replace(e_json, esc_all, 1), name='SEAL_MANUAL_DISCLOSURES_ESCAPED_E_R6_1_C4V004R.json'), kind='OBSERVE',
                         extra=lambda m: m['content']['e_r6_1_text'] == E0 and '\\u0054\\u0068\\u0065' in m['raw_text'])
    must_accept_verbatim('e_r6_1_text with every / written as \\/ (the same text): accepted; raw_text keeps \\/',
                         mdisc(raw=MD0_TEXT.replace(e_json, e_json.replace('/', '\\/'), 1), name='SEAL_MANUAL_DISCLOSURES_ESCAPED_SOLIDUS_C4V004R.json'),
                         kind='OBSERVE', extra=lambda m: m['content']['e_r6_1_text'] == E0 and '\\/' in m['raw_text'])
    # ---- R3: duplicate keys (a last-wins or first-wins parser would carry E_R6_1 or the schema)
    JD = 'MANUAL_DISCLOSURES_JSON_DUPLICATE_KEY'
    ln_e = ' "e_r6_1_text": ' + e_json + ',\n'
    ln_s = ' "schema": "SEAL_MANUAL_DISCLOSURES_V001"\n'
    for nm_, old_, new_ in (
            ('e_r6_1_text twice: a wrong text first, E_R6_1 last', ln_e, ' "e_r6_1_text": "WRONG",\n' + ln_e),
            ('e_r6_1_text twice: E_R6_1 first, a wrong text last', ln_e, ln_e + ' "e_r6_1_text": "WRONG",\n'),
            ('e_r6_1_text twice: E_R6_1 both times', ln_e, ln_e + ln_e),
            ('e_r6_1_text and the escaped spelling e_r6_1_t\\u0065xt of the same key', ln_e, ' "e_r6_1_t\\u0065xt": "WRONG",\n' + ln_e),
            ('schema twice: V002 first, V001 last', ln_s, ' "schema": "SEAL_MANUAL_DISCLOSURES_V002",\n' + ln_s),
            ('schema twice: V001 first, V002 last', ln_s, ' "schema": "SEAL_MANUAL_DISCLOSURES_V001",\n "schema": "SEAL_MANUAL_DISCLOSURES_V002"\n'),
            ('root_disclosures twice: an empty list first', ' "root_disclosures": [', ' "root_disclosures": [],\n "root_disclosures": ['),
            ('c08_table twice: an empty list first', ' "c08_table": [', ' "c08_table": [],\n "c08_table": ['),
            ('new_item_id twice in a C-08 row: NEW-99 first, NEW-71 last', '"new_item_id": "NEW-71"', '"new_item_id": "NEW-99",\n   "new_item_id": "NEW-71"'),
            ('text twice in a root disclosure', '"text": "SYNTHETIC TEST DISCLOSURE (', '"text": "x",\n   "text": "SYNTHETIC TEST DISCLOSURE (')):
        must_refuse('duplicate key: %s' % nm_, mdisc(raw=rep(old_, new_)), JD)
    # ---- R4: extra or look-alike keys
    KS = 'MANUAL_DISCLOSURES_KEYS'
    must_refuse('the key "e_r6_1_text " (trailing space) holding E_R6_1', mdisc(raw=rep('"e_r6_1_text":', '"e_r6_1_text ":')), KS)
    must_refuse('a Cyrillic look-alike key e_r6_1_t\u0435xt holding E_R6_1 in place of e_r6_1_text', mdisc(raw=rep('"e_r6_1_text":', '"e_r6_1_t\u0435xt":')), KS)
    must_refuse('a look-alike key e_r6_1_t\u0435xt (a wrong text) next to the real one', mdisc(raw=rep(ln_e, ' "e_r6_1_t\u0435xt": "WRONG",\n' + ln_e)), KS)
    must_refuse('the key Schema (capital S)', mdisc(raw=rep('"schema":', '"Schema":')), KS)
    must_refuse('an extra key manual_override: true', mdisc(mutate=lambda o: o.update(manual_override=True)), KS)
    must_refuse('an extra key e_r6_1_text_override holding a wrong text', mdisc(mutate=lambda o: o.update(e_r6_1_text_override='WRONG')), KS)
    must_refuse('an extra empty-string key', mdisc(mutate=lambda o: o.update({'': 'x'})), KS)
    SC = 'MANUAL_DISCLOSURES_SCHEMA'
    for nm_, s2 in (('a trailing space', 'SEAL_MANUAL_DISCLOSURES_V001 '), ('a Cyrillic U+041E for the O', 'SEAL_MANUAL_DISCL\u041eSURES_V001'),
                    ('a list holding it', ['SEAL_MANUAL_DISCLOSURES_V001']), ('the v004 record schema', 'UNT_V007_SEAL_RECORD_C4V004'),
                    ('route (b)\'s draft name (Claude4 0120)', 'UNT_V007_MANUAL_DISCLOSURES_C4V001')):
        must_refuse('schema is not exactly SEAL_MANUAL_DISCLOSURES_V001: %s' % nm_, mdisc(mutate=lambda o, s2=s2: o.update(schema=s2)), SC)
    # ---- R5: extra or bad rows
    R8 = 'MANUAL_DISCLOSURES_C08_ROW'
    for nm_, old_, new_ in (('line 1e999 (the JSON layer parses it as float inf; the form must refuse it)', '"line": 7,', '"line": 1e999,'),
                            ('line -1e999', '"line": 7,', '"line": -1e999,'), ('line 1E2 (a float)', '"line": 7,', '"line": 1E2,'),
                            ('line 7.5', '"line": 7,', '"line": 7.5,'), ('line -0', '"line": 7,', '"line": -0,'),
                            ('a key "declared_in_r13 " with a trailing space', '"declared_in_r13": false,', '"declared_in_r13 ": false,'),
                            ('new_item_id "NEW-71 " (trailing space)', '"new_item_id": "NEW-71"', '"new_item_id": "NEW-71 "'),
                            ('new_item_id new-71 (lower case)', '"new_item_id": "NEW-71"', '"new_item_id": "new-71"'),
                            ('new_item_id with Arabic-Indic digits', '"new_item_id": "NEW-71"', '"new_item_id": "NEW-\u0667\u0661"'),
                            ('new_item_id with a trailing U+200B', '"new_item_id": "NEW-71"', '"new_item_id": "NEW-71\u200b"'),
                            ('new_item_id with a Cyrillic U+0415 for E', '"new_item_id": "NEW-71"', '"new_item_id": "N\u0415W-71"')):
        must_refuse('a bad C-08 row: %s' % nm_, mdisc(raw=rep(old_, new_)), R8)
    must_refuse('a JSON syntax error: line 07 (a leading zero)', mdisc(raw=rep('"line": 7,', '"line": 07,')), 'MANUAL_DISCLOSURES_JSON_SYNTAX')
    for nm_, f_ in (('a row that is null', lambda o: o['c08_table'].append(None)), ('a row that is a list', lambda o: o['c08_table'].append(['NEW-9', 'f.py', 9])),
                    ('a row that is an empty object', lambda o: o['c08_table'].append({}))):
        must_refuse('a bad C-08 row: %s' % nm_, mdisc(mutate=f_), R8)
    RR = 'MANUAL_DISCLOSURES_ROOT_DISCLOSURE_ROW'
    for nm_, f_ in (('a row that is null', lambda o: o['root_disclosures'].append(None)), ('a row that is a list', lambda o: o['root_disclosures'].append(['a', 'b', 'c'])),
                    ('an id of U+3000 only (whitespace)', lambda o: o['root_disclosures'][0].update(id='\u3000')),
                    ('text as a list', lambda o: o['root_disclosures'][0].update(text=['x'])), ('source null', lambda o: o['root_disclosures'][0].update(source=None)),
                    ('an extra key Id', lambda o: o['root_disclosures'][0].update(Id='x'))):
        must_refuse('a bad root disclosure: %s' % nm_, mdisc(mutate=f_), RR)
    must_refuse('two root disclosures with the same id and different texts (A71)', mdisc(mutate=lambda o: o['root_disclosures'].append(
        {'id': 'SYNTH_A2', 'source': 'SYNTHETIC', 'text': 'another SYNTHETIC text'})), 'MANUAL_DISCLOSURES_ROOT_DISCLOSURE_DUPLICATE_ID')
    must_refuse('two C-08 rows with the same id, the second a perfect copy of the first', mdisc(mutate=lambda o: o['c08_table'].append(dict(o['c08_table'][0]))),
                'MANUAL_DISCLOSURES_C08_DUPLICATE_ID')
    for nm_, raw_ in (('a // comment', MD0_TEXT.replace('{\n', '{\n // SYNTHETIC comment\n', 1)), ('a trailing comma', rep(ln_s, ' "schema": "SEAL_MANUAL_DISCLOSURES_V001",\n')),
                      ('single-quoted strings', rep('"schema": "SEAL_MANUAL_DISCLOSURES_V001"', "'schema': 'SEAL_MANUAL_DISCLOSURES_V001'")),
                      ('a raw tab inside a string', rep('SYNTHETIC TEST CONFIRMATION', 'SYNTHETIC\tTEST CONFIRMATION')),
                      ('a raw LF inside a string', rep('SYNTHETIC TEST CONFIRMATION', 'SYNTHETIC\nTEST CONFIRMATION'))):
        must_refuse('not strict JSON: %s' % nm_, mdisc(raw=raw_), 'MANUAL_DISCLOSURES_JSON_SYNTAX')
    mdb = MD0_TEXT.encode('utf-8')
    for nm_, raw_ in (('an invalid UTF-8 byte inside a string', mdb.replace(b'SYNTHETIC TEST CONFIRMATION', b'SYNTHETIC \xff CONFIRMATION', 1)),
                      ('CESU-8 surrogate bytes (ED A0 80)', mdb.replace(b'SYNTHETIC TEST CONFIRMATION', b'SYNTHETIC \xed\xa0\x80 CONFIRMATION', 1)),
                      ('an overlong UTF-8 encoding of / (C0 AF)', mdb.replace(b'SYNTHETIC TEST CONFIRMATION', b'SYNTHETIC \xc0\xaf CONFIRMATION', 1)),
                      ('UTF-32 bytes', MD0_TEXT.encode('utf-32'))):
        must_refuse('not UTF-8 text: %s' % nm_, mdisc(raw=raw_), 'MANUAL_DISCLOSURES_JSON_ENCODING')
    # ---- R6: a pin to a different file, near-miss pins
    PM = 'MANUAL_DISCLOSURES_PIN_MISMATCH'
    MDX = mdisc(mutate=lambda o: o['root_disclosures'][0].update(text='SYNTHETIC OTHER FILE X (Claude4 v004 refuter): not root\'s'),
                name='SEAL_MANUAL_DISCLOSURES_OTHER_FILE_X_C4V004R.json')
    mdb0 = Path(MD0[0]).read_bytes()
    for nm_, md_ in (('MD0\'s path with the sha of root\'s real file', (MD0[0], ROOT_MD_SHA)), ('root\'s real path with MD0\'s sha', (str(ROOT_MD), MD0[1])),
                     ('another valid SYNTHETIC file X with MD0\'s sha', (MDX[0], MD0[1])), ('MD0\'s path with X\'s sha', (MD0[0], MDX[1])),
                     ('the sha with a trailing LF', (MD0[0], MD0[1] + '\n')), ('the sha with a leading space', (MD0[0], ' ' + MD0[1])),
                     ('the path with a trailing slash', (MD0[0] + '/', MD0[1])), ('the path with an embedded NUL', (MD0[0] + '\x00', MD0[1])),
                     ('/dev/null with the sha of the empty string', ('/dev/null', C.sha_bytes(b''))), ('the path as bytes', (MD0[0].encode('utf-8'), MD0[1])),
                     ('the path as a pathlib.Path', (Path(MD0[0]), MD0[1])), ('an empty path', ('', MD0[1])),
                     ('the sha of the bytes plus a newline (a near miss)', (MD0[0], C.sha_bytes(mdb0 + b'\n'))),
                     ('the sha of the parsed object re-serialized (not the file bytes)', (MD0[0], C.sha_bytes((json.dumps(json.loads(mdb0), sort_keys=True)).encode('utf-8')))),
                     ('the sha256 of the path string', (MD0[0], C.sha_bytes(MD0[0].encode('utf-8')))), ('a 63-hex sha', (MD0[0], MD0[1][:63])),
                     ('a 65-hex sha', (MD0[0], MD0[1] + '0'))):
        must_refuse('the pin does not verify: %s' % nm_, md_, PM)
    lnk_dir = rf_dir / 'links'
    lnk_dir.mkdir()
    lnk = lnk_dir / 'ROOT_MD_SYMLINK_C4V004R.json'
    os.symlink(str(ROOT_MD), str(lnk))
    must_accept_verbatim('a symlink in the run folder to root\'s real file, with b9db6fd1: accepted (as v003 treats pins); the record pin names the path as given; '
                         'raw_text is root\'s bytes', (str(lnk), ROOT_MD_SHA), kind='OBSERVE')
    must_accept_verbatim('root\'s real file by a path with a .. segment: accepted; the pin keeps the literal path', (str(ROOT_MD.parent) + '/../root_inputs/' + ROOT_MD.name,
                         ROOT_MD_SHA), kind='OBSERVE')
    must_accept_verbatim('the API pin as a list [path, sha256]: accepted', [MD0[0], MD0[1]], kind='OBSERVE')
    # ---- R7: the file swapped between the check and the build (in-process: T4's Path reads other bytes; no file is changed)
    PathT4 = T4.Path

    class _SwapPath(type(Path())):
        plan = {}
        log = []

        def read_bytes(self):
            k = os.path.realpath(str(self))
            q = _SwapPath.plan.get(k, {}).get('read')
            if q:
                beh = q.pop(0)
                _SwapPath.log.append((k, 'read', beh if isinstance(beh, str) else 'bytes'))
                if isinstance(beh, bytes):
                    return beh
            return super().read_bytes()

        def is_file(self):
            k = os.path.realpath(str(self))
            q = _SwapPath.plan.get(k, {}).get('is_file')
            if q:
                beh = q.pop(0)
                _SwapPath.log.append((k, 'is_file', beh))
                if beh == 'gone':
                    return False
            return super().is_file()
    root_raw_ = ROOT_MD.read_bytes()
    for nm_, plan_, expect_ in (
            ('the re-read returns root\'s real file (another valid file) instead of the checked bytes', {'read': ['real', root_raw_]}, 'MANUAL_DISCLOSURES_CHANGED_AFTER_CHECK'),
            ('the re-read returns the checked bytes plus one LF', {'read': ['real', mdb0 + b'\n']}, 'MANUAL_DISCLOSURES_CHANGED_AFTER_CHECK'),
            ('the re-read returns the checked bytes with LF turned into CRLF (same parse)', {'read': ['real', mdb0.replace(b'\n', b'\r\n')]}, 'MANUAL_DISCLOSURES_CHANGED_AFTER_CHECK'),
            ('the re-read returns empty bytes', {'read': ['real', b'']}, 'MANUAL_DISCLOSURES_CHANGED_AFTER_CHECK'),
            ('the file is gone at the re-read', {'is_file': ['real', 'gone']}, 'MANUAL_DISCLOSURES_CHANGED_AFTER_CHECK'),
            ('the checked read itself returns other bytes than the pinned file (swapped before the check)', {'read': [Path(MDX[0]).read_bytes()]}, PM),
            ('the re-read returns identical bytes (control: the genuine record is printed)', {'read': ['real', mdb0]}, None)):
        _SwapPath.plan = {os.path.realpath(MD0[0]): {k: list(v) for k, v in plan_.items()}}
        _SwapPath.log = []
        T4.Path = _SwapPath
        try:
            r_s, t_s = build_md(MD0)
        finally:
            T4.Path = PathT4
        cs = [f['code'] for f in r_s['failures']]
        consumed = not any(_SwapPath.plan[os.path.realpath(MD0[0])].values())
        if expect_ is None:
            ok_s = r_s['verdict'] == 'PASS' and t_s == text and consumed
        else:
            ok_s = t_s is None and r_s['verdict'] == 'REFUSE' and cs == [expect_] and consumed
        rf('swap: %s' % nm_, ok_s, 'verdict %s codes %r consumed %s log %r' % (r_s['verdict'], cs, consumed, [x[1:] for x in _SwapPath.log]),
           'PASS, the genuine record' if expect_ is None else 'REFUSE %s (only), no record' % expect_, 'CONTROL' if expect_ is None else 'MUST_FAIL')
    assert T4.Path is PathT4
    # ---- R8: the record carries the file verbatim (valid files in other spellings)
    big_conf = 'SYNTHETIC caf\u00e9 \u2713 \u2014 \u2264 \U0001d518 [\u2028] [\u2029] [\x7f] confirmation (Claude4 v004 refuter): not root\'s'
    for nm_, md_ in (('CRLF line endings', mdisc(raw=MD0_TEXT.replace('\n', '\r\n'))),
                     ('minified, no trailing newline', mdisc(raw=json.dumps(md_obj(), separators=(',', ':'), ensure_ascii=False))),
                     ('tab indentation', mdisc(raw=json.dumps(md_obj(), indent='\t', ensure_ascii=False) + '\n')),
                     ('keys not sorted (root\'s 0647 file is sorted; the tool does not require it)', mdisc(raw=json.dumps(md_obj(), indent=1, ensure_ascii=False) + '\n')),
                     ('non-ASCII text written as UTF-8 (U+00E9, U+2713, U+2014, U+2264, U+1D518, U+2028, U+2029, DEL)', mdisc(mutate=lambda o: o.update(c08_confirmation=big_conf))),
                     ('the same non-ASCII text written as \\u escapes', mdisc(raw=json.dumps(dict(md_obj(), c08_confirmation=big_conf), indent=1, sort_keys=True, ensure_ascii=True) + '\n')),
                     ('leading and trailing JSON whitespace', mdisc(raw='\n \t\r\n' + MD0_TEXT + '\n\n  ')),
                     ('a \\u0000 escape inside a root disclosure text', mdisc(mutate=lambda o: o['root_disclosures'][0].update(text='SYNTHETIC \u0000 NUL text'))),
                     ('1,000 root disclosure rows', mdisc(mutate=lambda o: o.update(root_disclosures=[{'id': 'SYNTH_%04d' % j, 'source': 'SYNTHETIC', 'text': 'SYNTHETIC %d' % j}
                                                                                                   for j in range(1000)])))):
        must_accept_verbatim('verbatim: %s' % nm_, md_)
    must_accept_verbatim('REAL: root\'s real file b9db6fd1 by the API: accepted, carried verbatim, and every other record field equals the genuine record\'s',
                         (str(ROOT_MD), ROOT_MD_SHA), kind='REAL')
    # ---- R9: extra well-formed rows are accepted (OBSERVE: the tool checks the form; the C-08 lines and texts are root's and the reviewers' checks)
    must_accept_verbatim('an extra well-formed C-08 row (a fabricated NEW-999 at a fabricated file) is accepted and carried verbatim', mdisc(mutate=lambda o: o['c08_table'].append(
        {'new_item_id': 'NEW-999', 'file': 'SYNTHETIC/fabricated.py', 'line': 1, 'declared_in_r13': False})), kind='OBSERVE')
    must_accept_verbatim('an extra well-formed root disclosure is accepted and carried verbatim', mdisc(mutate=lambda o: o['root_disclosures'].append(
        {'id': 'SYNTH_EXTRA', 'source': 'SYNTHETIC', 'text': 'SYNTHETIC EXTRA (Claude4 v004 refuter): not root\'s'})), kind='OBSERVE')
    must_accept_verbatim('NEW-7 and NEW-007 as two C-08 rows: accepted as distinct ids (string comparison, no numeric normalization)', mdisc(mutate=lambda o: o['c08_table'].extend(
        [{'new_item_id': 'NEW-7', 'file': 'SYNTHETIC/a.py', 'line': 1}, {'new_item_id': 'NEW-007', 'file': 'SYNTHETIC/a.py', 'line': 2}])), kind='OBSERVE')
    must_accept_verbatim('root disclosure ids SYNTH_A1 and "SYNTH_A1 " (a trailing space): accepted as distinct ids', mdisc(mutate=lambda o: o['root_disclosures'].append(
        dict(o['root_disclosures'][0], id='SYNTH_A1 '))), kind='OBSERVE')
    must_accept_verbatim('a 4,300-digit C-08 line (Python\'s limit): accepted as a positive integer', mdisc(raw=rep('"line": 7,', '"line": %s,' % ('9' * 4300))), kind='OBSERVE')
    must_accept_verbatim('a root disclosure text of U+200B only (not whitespace to str.strip): accepted', mdisc(mutate=lambda o: o['root_disclosures'][0].update(text='\u200b')),
                         kind='OBSERVE')
    # ---- R10: REAL, the CLI as root runs it, the record written by exclusive create, then re-read from bytes
    rc_r, so_r, se_r = cli(T4.main, base_cli + ['--manual-disclosures', str(ROOT_MD), '--manual-disclosures-sha256', ROOT_MD_SHA])
    cli_dir = rf_dir / 'cli'
    cli_dir.mkdir()
    rec_path = cli_dir / 'SEAL_RECORD_WITH_ROOT_MANUAL_DISCLOSURES_SYNTH_C4V004R.json'
    with open(str(rec_path), 'x') as f_r:
        f_r.write(so_r)
    wb = rec_path.read_bytes()
    wr = jrec(wb.decode('utf-8'))
    wm = wr.get('manual_disclosures') or {}
    ok_cli = (rc_r == 0 and C.sha_bytes(wb) == jget(se_r, 'seal_record_sha256') and wb == so_r.encode('utf-8')
              and wm.get('pin') == {'path': str(ROOT_MD), 'sha256': ROOT_MD_SHA} and isinstance(wm.get('raw_text'), str)
              and wm['raw_text'].encode('utf-8') == root_raw_ and C.sha_bytes(wm['raw_text'].encode('utf-8')) == ROOT_MD_SHA
              and wm.get('content') == C.strict_json_bytes(root_raw_) and wm['content'].get('e_r6_1_text') == T4.E_R6_1 == E_SEL
              and wr.get('schema') == 'UNT_V007_SEAL_RECORD_C4V004' and wr.get('disclosures') == base_rec.get('disclosures')
              and {k: v for k, v in wr.items() if k != 'manual_disclosures'} == {k: v for k, v in base_rec.items() if k != 'manual_disclosures'})
    rf('REAL CLI: --manual-disclosures <root\'s file> --manual-disclosures-sha256 b9db6fd1, stdout written by exclusive create as root does; the written '
       'file\'s sha equals stderr\'s seal_record_sha256, and its manual_disclosures.raw_text encodes to root\'s bytes exactly', ok_cli,
       'rc %r codes %r written %s' % (rc_r, jcodes(se_r), C.sha_bytes(wb)[:8]), 'exit 0, verbatim', 'REAL')
    # ---- R11: OBSERVE, a hand-made record (not built by tool 4) under the v004 admission check and the real guard v008 admission()
    import copy as _copy
    adm = rf_dir / 'admission'
    adm.mkdir()
    q_variants = []
    q = _copy.deepcopy(base_rec)
    q.pop('manual_disclosures')
    q_variants.append(('v004 schema with manual_disclosures removed', 'NO_MD', q))
    q = _copy.deepcopy(base_rec)
    q['manual_disclosures'] = None
    q_variants.append(('v004 schema with manual_disclosures null', 'NULL_MD', q))
    q = _copy.deepcopy(base_rec)
    q['manual_disclosures']['content']['e_r6_1_text'] = 'WRONG'
    q['manual_disclosures']['raw_text'] = q['manual_disclosures']['raw_text'].replace(e_json, '"WRONG"', 1)
    q_variants.append(('v004 schema with e_r6_1_text replaced by a wrong text in content and raw_text', 'WRONG_E', q))
    q = _copy.deepcopy(base_rec)
    q['manual_disclosures']['raw_text'] += ' '
    q_variants.append(('v004 schema with raw_text no longer hashing to the pin', 'RAW_NOT_PIN', q))
    obs = {}
    for nm_, tg_, q in q_variants:
        sp_ = xw(adm / ('SEAL_RECORD_HAND_MADE_%s_SYNTH.json' % tg_), json.dumps(q, indent=1, sort_keys=True, ensure_ascii=False) + '\n')
        cp_ = xw(adm / ('ROOT_SEAL_ADMISSION_HAND_MADE_%s_SYNTH.json' % tg_), dict(cfg, seal=pin(sp_)))
        rq_ = T4.check_admission_config(cp_, sp_)
        G.CONFIG = cp_
        os.environ['UNT_ROOT_ADMISSION_SHA256'] = C.sha(cp_)
        try:
            G.admission(str(PKT / 'route_a_token_launcher_cx1v007.py'))
            og_ = 'ok'
        except BaseException as e:
            og_ = '%s: %s' % (type(e).__name__, str(e)[:160])
        obs[tg_] = {'admission_check': rq_['verdict'], 'codes': [f['code'] for f in rq_['failures']], 'guard_v008': og_}
        rf('a hand-made record (%s): the v004 admission check says %s %r; the real guard v008 admission() says %s' % (nm_, rq_['verdict'],
           [f['code'] for f in rq_['failures']], og_), True, json.dumps(obs[tg_]), 'OBSERVE (no expectation: shows what custody remains after tool 4)', 'OBSERVE')
    G.CONFIG = run / 'NO_CONFIG_AFTER_REFUTER.json'
    os.environ.pop('UNT_ROOT_ADMISSION_SHA256', None)
    # ---- the refuter record
    rf_sum = {'schema': 'UNT_SEAL_TOOLS_V004_REFUTER_PROBES_C4V004R', 'note': 'Claude4 seal tools v004 refute stage: probes run inside the v004 suite copy '
              '(test_seal_tools_c4v004_with_refuter.py) on its base fixture; every manual disclosures file is SYNTHETIC except root\'s real file (read only)',
              'tool4_sha256': C.sha(TOOLS / 'build_seal_record_c4v004.py'), 'e_r6_1_utf8_sha256': C.sha_bytes(T4.E_R6_1.encode('utf-8')),
              'root_md': {'path': str(ROOT_MD), 'sha256': C.sha(ROOT_MD)}, 'python': sys.version, 'stdout_encoding': getattr(sys.__stdout__, 'encoding', None),
              'by_kind': {k: '%d/%d' % (sum(1 for x in RF if x['kind'] == k and x['ok']), sum(1 for x in RF if x['kind'] == k)) for k in sorted({x['kind'] for x in RF})},
              'passed': sum(1 for x in RF if x['ok']), 'total': len(RF), 'admission_observations': obs, 'probes': RF}
    with open(rf_dir / 'REFUTER_PROBES_C4V004R.json', 'x') as f:
        json.dump(rf_sum, f, indent=1)
'''


def main():
    raw = SRC.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SRC_SHA:
        sys.stderr.write('REFUSED: %s is not ee237685\n' % SRC)
        return 1
    s = raw.decode('utf-8')
    for needle in (ANCHOR, RES_OLD):
        if s.count(needle) != 1:
            sys.stderr.write('REFUSED: anchor count %d for %r\n' % (s.count(needle), needle))
            return 1
    s2 = HEADER + s.replace(ANCHOR, BLOCK + ANCHOR, 1).replace(RES_OLD, RES_NEW, 1)
    compile(s2, str(DST), 'exec')
    if s2.count(BLOCK) != 1 or s2.count(RES_NEW) != 1:
        sys.stderr.write('REFUSED: the patched text does not hold the block once\n')
        return 1
    with open(DST, 'x', encoding='utf-8') as f:
        f.write(s2)
    print(hashlib.sha256(DST.read_bytes()).hexdigest(), DST)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
