# Claude4 seal tools v004 (BUILD helper; A110, dispatch 0646): write build_seal_record_c4v004.py = v003's tool 4 bytes (de0ceb15) with
# exactly the replacements below (each old text must occur exactly once, else the run fails and nothing is written), and the E_R6_1
# constant generated from the bytes of SELECTED_R6_C4V001.json basis.erratum_E_R6_1 (sha-verified; the literal is checked by AST after
# the write). The output is created exclusively. No process, no network, no delete.
# usage: python3 -I -B make_tool4_c4v004.py OUT.py
import ast, hashlib, json, sys
from pathlib import Path

V3_TOOL4 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v003/build_seal_record_c4v003.py')
V3_TOOL4_SHA = 'de0ceb15ebfb95e04227730bd2785eb46af8cb5980012de91de98f34ea226b96'
R6_SELECTED = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r6/SELECTED_R6_C4V001.json')
R6_SELECTED_SHA = '7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def _pairs(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError('DUPLICATE_JSON_KEY %r' % k)
        out[k] = v
    return out


def literal(s, width=112, indent=10):
    """s as implicitly concatenated string literals, split after spaces; ''.join of the pieces is s exactly"""
    words = s.split(' ')
    chunks, cur = [], ''
    for w in words:
        nxt = (cur + ' ' + w) if cur else w
        if len(nxt) > width and cur:
            chunks.append(cur + ' ')
            cur = w
        else:
            cur = nxt
    chunks.append(cur)
    assert ''.join(chunks) == s
    return '(' + ('\n' + ' ' * indent).join(repr(c) for c in chunks) + ')'


def main():
    out = Path(sys.argv[1])
    src = V3_TOOL4.read_bytes()
    assert sha(src) == V3_TOOL4_SHA, 'v003 tool 4 is not de0ceb15'
    sel = R6_SELECTED.read_bytes()
    assert sha(sel) == R6_SELECTED_SHA, 'SELECTED_R6_C4V001 is not 7200acd9'
    e = json.loads(sel, object_pairs_hook=_pairs)['basis']['erratum_E_R6_1']
    assert isinstance(e, str) and e.strip()
    e_sha = sha(e.encode('utf-8'))
    ascii_note = '%d ASCII characters' % len(e) if all(ord(c) < 128 for c in e) else '%d characters' % len(e)
    text = src.decode('utf-8')

    R = []          # (old, new): each old occurs exactly once in the v003 bytes
    R.append(("# Claude4 seal tools v003, tool 4 (successor of r2 build_seal_record_c4v002.py 4192983d; v002 succeeded build_seal_record_c4v001.py\n"
              "# 3091fc2a): build the exact SEAL_RECORD bytes for root to create exclusively, and check root's admission config against them. It writes nothing.\n",
              "# Claude4 seal tools v004, tool 4 (successor of v003 build_seal_record_c4v003.py de0ceb15; v003 succeeded r2 build_seal_record_c4v002.py\n"
              "# 4192983d): build the exact SEAL_RECORD bytes for root to create exclusively, and check root's admission config against them. It writes nothing.\n"))
    R.append(("#        be present (L39) and exact {path, sha256} pins whose bytes verify (L40, pin_check L18), here by the stricter Checker.pin.\n"
              "# Root creates the record with exclusive create, e.g.\n",
              "#        be present (L39) and exact {path, sha256} pins whose bytes verify (L40, pin_check L18), here by the stricter Checker.pin.\n"
              "# New in v004 (A110; dispatches 0646 and 0647; Codex1 0114 C3V007-DISCLOSURE-01). Nothing else changes: tools 1, 2, 3 and 5 and\n"
              "# seal_common are v003's bytes, and this tool imports them under their v003 names.\n"
              "#  A110  one new input, root's SEAL_MANUAL_DISCLOSURES_V001 file: --manual-disclosures M.json --manual-disclosures-sha256 H (API\n"
              "#        manual_disclosures=(path, sha256)). It is required for the V007 seal (not given: MANUAL_DISCLOSURES_REQUIRED). It must be an\n"
              "#        absolute path to a regular file whose bytes hash to H (else MANUAL_DISCLOSURES_PIN_MISMATCH), read once, before tools 1-3\n"
              "#        run; those bytes are parsed by v003's strict JSON (typed MANUAL_DISCLOSURES_JSON_* codes: a duplicate key, a non-finite\n"
              "#        constant, a 4,300+ digit integer, ...) and checked against the exact form: keys {schema, e_r6_1_text, c08_table,\n"
              "#        c08_confirmation, root_disclosures}; schema SEAL_MANUAL_DISCLOSURES_V001; e_r6_1_text non-empty and equal to E_R6_1 below;\n"
              "#        c08_table a non-empty list of {new_item_id NEW-<n>, file, line > 0} rows (declared_in_r13, a bool, optional), ids unique;\n"
              "#        c08_confirmation non-empty; root_disclosures a non-empty list of {id, source, text} rows of non-empty strings, ids unique;\n"
              "#        every string has a UTF-8 form. Just before the record is built the file is re-read, and the build refuses\n"
              "#        MANUAL_DISCLOSURES_CHANGED_AFTER_CHECK unless its bytes still hash to H. The record carries it verbatim, next to the\n"
              "#        derived prereg disclosures: manual_disclosures = {pin {path, sha256}, content (the parsed file), raw_text (its exact text)}.\n"
              "#        The record schema becomes UNT_V007_SEAL_RECORD_C4V004 (its content changed), so the v004 admission check refuses a v003\n"
              "#        record, which has no manual disclosures. The tool checks the form and E_R6_1 only; the C-08 table and the disclosure texts\n"
              "#        are root's (its manual C-08 check), cross-checked by Claude3 and Codex1.\n"
              "# Root creates the record with exclusive create, e.g.\n"))
    R.append(("#   python3 -I -B build_seal_record_c4v003.py ... | python3",
              "#   python3 -I -B build_seal_record_c4v004.py ... | python3"))
    R.append(("# usage: python3 -I -B build_seal_record_c4v003.py --slots S.json",
              "# usage: python3 -I -B build_seal_record_c4v004.py --slots S.json"))
    R.append(("#        [--text-of-record-sha H]            (root states the r5 sha while tool 3's pin is PENDING; see tool 3)\n",
              "#        [--text-of-record-sha H]            (root states the r5 sha while tool 3's pin is PENDING; see tool 3)\n"
              "#        --manual-disclosures M.json --manual-disclosures-sha256 H   (v004 A110: root's SEAL_MANUAL_DISCLOSURES_V001 file; required)\n"))
    R.append(("#        python3 -I -B build_seal_record_c4v003.py --check-admission-config",
              "#        python3 -I -B build_seal_record_c4v004.py --check-admission-config"))
    R.append(("SCHEMA = 'UNT_V007_SEAL_RECORD_C4V003'                       # v003 D-05: the record content changed (later_entry_dispositions)\n",
              "SCHEMA = 'UNT_V007_SEAL_RECORD_C4V004'                       # v004 A110: the record content changed (manual_disclosures); v003 C4V003\n"))
    R.append(("                    'text of record byte for byte, so it keeps that text\\'s draft status line and the PENDING strings listed here.')\n",
              "                    'text of record byte for byte, so it keeps that text\\'s draft status line and the PENDING strings listed here.')\n"
              "MANUAL_DISCLOSURES_SCHEMA = 'SEAL_MANUAL_DISCLOSURES_V001'    # v004 A110: root's file (seal_assembly_c3/root_inputs, 0647)\n"
              "MANUAL_DISCLOSURES_KEYS = {'schema', 'e_r6_1_text', 'c08_table', 'c08_confirmation', 'root_disclosures'}\n"
              "C08_ROW_KEYS = {'new_item_id', 'file', 'line'}                # and declared_in_r13 (a bool), optional: 0646 names three keys, root's file four\n"
              "C08_ID_RX = re.compile(r'NEW-[0-9]{1,3}')                     # a NEW-item id, ASCII digits only\n"
              "ROOT_DISCLOSURE_KEYS = {'id', 'source', 'text'}\n"
              "# E_R6_1 (v004 A110): prereg r6's erratum E-R6-1, copied byte for byte from basis.erratum_E_R6_1 of\n"
              "# " + str(R6_SELECTED) + "\n"
              "# (sha256 " + R6_SELECTED_SHA + "): " + ascii_note + ", the sha256 of their UTF-8 bytes\n"
              "# " + e_sha + ". The tests re-read that file and assert that this constant equals it.\n"
              "E_R6_1 = " + literal(e) + "\n"))
    R.append(("def build(a):\n"
              "    cov = getattr(a, 'covered_later', None)\n"
              "    disp = getattr(a, 'dispositions', None)\n"
              "    res = T3.run(a.slots, a.prereg, a.text_of_record, a.frozen, cov or (), a.reviewed, a.sealed_compare, getattr(a, 'text_of_record_sha', None), disp,\n"
              "                 getattr(a, 'addendum_at_text_of_record', None))\n"
              "    chk = C.Checker('build_seal_record_c4v003')\n",
              "def strings_of(obj, where='$'):\n"
              "    \"\"\"v004 A110: every (JSON path, string) of a parsed JSON value, keys included\"\"\"\n"
              "    if isinstance(obj, str):\n"
              "        return [(where, obj)]\n"
              "    out = []\n"
              "    if isinstance(obj, dict):\n"
              "        for k, v in obj.items():\n"
              "            out += strings_of(k, where + '.<key>') + strings_of(v, '%s.%s' % (where, k))\n"
              "    elif isinstance(obj, list):\n"
              "        for j, v in enumerate(obj):\n"
              "            out += strings_of(v, '%s[%d]' % (where, j))\n"
              "    return out\n"
              "\n"
              "\n"
              "def has_utf8_form(s):\n"
              "    try:\n"
              "        s.encode('utf-8')\n"
              "        return True\n"
              "    except UnicodeEncodeError:\n"
              "        return False\n"
              "\n"
              "\n"
              "def manual_disclosures_form_codes(chk, d):\n"
              "    \"\"\"v004 A110: the exact form of root's SEAL_MANUAL_DISCLOSURES_V001 file (0646, 0647). The tool checks the form and E_R6_1; it does\n"
              "    not judge the C-08 table or the disclosure texts, which are root's (its manual C-08 check), cross-checked by Claude3 and Codex1.\"\"\"\n"
              "    if not isinstance(d, dict):\n"
              "        chk.fail('MANUAL_DISCLOSURES_SHAPE', 'the file is a JSON object')\n"
              "        return\n"
              "    if set(d) != MANUAL_DISCLOSURES_KEYS:\n"
              "        chk.fail('MANUAL_DISCLOSURES_KEYS', 'exactly %s; the file has %s' % (sorted(MANUAL_DISCLOSURES_KEYS), sorted(d)[:20]))\n"
              "        return\n"
              "    n = len(chk.failures)\n"
              "    if d['schema'] != MANUAL_DISCLOSURES_SCHEMA:\n"
              "        chk.fail('MANUAL_DISCLOSURES_SCHEMA', '%s, not %s' % (repr(d['schema'])[:120], MANUAL_DISCLOSURES_SCHEMA))\n"
              "    e = d['e_r6_1_text']\n"
              "    if not (isinstance(e, str) and e.strip()):\n"
              "        chk.fail('MANUAL_DISCLOSURES_E_R6_1_TEXT_EMPTY', 'e_r6_1_text is a non-empty string: prereg r6\\'s E_R6_1 exactly')\n"
              "    elif e != E_R6_1:\n"
              "        i = next((k for k, (x, y) in enumerate(zip(e, E_R6_1)) if x != y), min(len(e), len(E_R6_1)))\n"
              "        chk.fail('MANUAL_DISCLOSURES_E_R6_1_TEXT_MISMATCH', 'e_r6_1_text is not prereg r6\\'s E_R6_1 (SELECTED_R6_C4V001 basis.erratum_E_R6_1) '\n"
              "                 'exactly: %d characters against %d, first difference at character %d' % (len(e), len(E_R6_1), i))\n"
              "    rows = d['c08_table']\n"
              "    if not (isinstance(rows, list) and rows):\n"
              "        chk.fail('MANUAL_DISCLOSURES_C08_TABLE_SHAPE', 'c08_table is a non-empty list of rows')\n"
              "    else:\n"
              "        seen = {}\n"
              "        for j, r in enumerate(rows):\n"
              "            if not (isinstance(r, dict) and C08_ROW_KEYS <= set(r) <= C08_ROW_KEYS | {'declared_in_r13'} and isinstance(r['new_item_id'], str)\n"
              "                    and C08_ID_RX.fullmatch(r['new_item_id']) and isinstance(r['file'], str) and r['file'].strip()\n"
              "                    and type(r['line']) is int and r['line'] > 0 and type(r.get('declared_in_r13', False)) is bool):\n"
              "                chk.fail('MANUAL_DISCLOSURES_C08_ROW', 'c08_table[%d]: exactly {new_item_id NEW-<n>, file (non-empty), line (an integer > 0)}, '\n"
              "                         'plus declared_in_r13 (true or false) if given' % j)\n"
              "                continue\n"
              "            if r['new_item_id'] in seen:\n"
              "                chk.fail('MANUAL_DISCLOSURES_C08_DUPLICATE_ID', 'c08_table[%d] and c08_table[%d] carry %s (A71)' % (seen[r['new_item_id']], j, r['new_item_id']))\n"
              "            seen.setdefault(r['new_item_id'], j)\n"
              "    c = d['c08_confirmation']\n"
              "    if not (isinstance(c, str) and c.strip()):\n"
              "        chk.fail('MANUAL_DISCLOSURES_C08_CONFIRMATION_EMPTY', 'c08_confirmation is root\\'s non-empty confirmation text (A107.4)')\n"
              "    rd = d['root_disclosures']\n"
              "    if not (isinstance(rd, list) and rd):\n"
              "        chk.fail('MANUAL_DISCLOSURES_ROOT_DISCLOSURES_SHAPE', 'root_disclosures is a non-empty list of rows (A110.3)')\n"
              "    else:\n"
              "        ids = {}\n"
              "        for j, x in enumerate(rd):\n"
              "            if not (isinstance(x, dict) and set(x) == ROOT_DISCLOSURE_KEYS and all(isinstance(x[k], str) and x[k].strip() for k in sorted(ROOT_DISCLOSURE_KEYS))):\n"
              "                chk.fail('MANUAL_DISCLOSURES_ROOT_DISCLOSURE_ROW', 'root_disclosures[%d]: exactly {id, source, text}, each a non-empty string' % j)\n"
              "                continue\n"
              "            if x['id'] in ids:\n"
              "                chk.fail('MANUAL_DISCLOSURES_ROOT_DISCLOSURE_DUPLICATE_ID', 'root_disclosures[%d] and root_disclosures[%d] carry %s (A71)'\n"
              "                         % (ids[x['id']], j, repr(x['id'])[:120]))\n"
              "            ids.setdefault(x['id'], j)\n"
              "    if len(chk.failures) == n:                                  # the form holds, so every string is a flat field value or key\n"
              "        bad = [w for w, s in strings_of(d) if not has_utf8_form(s)]\n"
              "        if bad:\n"
              "            chk.fail('MANUAL_DISCLOSURES_TEXT_ENCODING', '%d string(s) with no UTF-8 form (a lone surrogate), the first at %s' % (len(bad), bad[0]))\n"
              "\n"
              "\n"
              "def manual_disclosures_codes(chk, md):\n"
              "    \"\"\"v004 A110: root's manual disclosures pin (path, sha256): an absolute path to a regular file whose bytes hash to sha256 (else\n"
              "    MANUAL_DISCLOSURES_PIN_MISMATCH; no pin given: MANUAL_DISCLOSURES_REQUIRED). The bytes are read once and are the ones parsed, by\n"
              "    v003's strict JSON (typed MANUAL_DISCLOSURES_JSON_* codes), then checked for the exact form. Returns (path, sha256, content, text)\n"
              "    or None after a failure.\"\"\"\n"
              "    if md is None:\n"
              "        chk.fail('MANUAL_DISCLOSURES_REQUIRED', 'A110: the V007 SEAL_RECORD carries root\\'s manual disclosures: give --manual-disclosures M.json '\n"
              "                 '--manual-disclosures-sha256 H (API manual_disclosures=(path, sha256))')\n"
              "        return None\n"
              "    if not (isinstance(md, (tuple, list)) and len(md) == 2 and all(isinstance(x, str) for x in md)):\n"
              "        chk.fail('MANUAL_DISCLOSURES_PIN_MISMATCH', 'the manual disclosures pin is (path, sha256), both given: %s' % repr(md)[:200])\n"
              "        return None\n"
              "    p, h = md\n"
              "    if not Path(p).is_absolute():\n"
              "        chk.fail('MANUAL_DISCLOSURES_PIN_MISMATCH', 'not an absolute path: %s' % repr(p)[:200])\n"
              "        return None\n"
              "    if not Path(p).is_file():\n"
              "        chk.fail('MANUAL_DISCLOSURES_PIN_MISMATCH', 'not a regular file: %s' % p)\n"
              "        return None\n"
              "    raw = Path(p).read_bytes()\n"
              "    got = C.sha_bytes(raw)\n"
              "    if got != h:\n"
              "        chk.fail('MANUAL_DISCLOSURES_PIN_MISMATCH', '%s has %s; root pinned %s' % (p, got, repr(h)[:80]))\n"
              "        return None\n"
              "    obj, text, bad = C.strict_json_typed(raw, 'MANUAL_DISCLOSURES')\n"
              "    if bad is not None:\n"
              "        chk.fail(*bad)\n"
              "        return None\n"
              "    n = len(chk.failures)\n"
              "    manual_disclosures_form_codes(chk, obj)\n"
              "    if len(chk.failures) > n:\n"
              "        return None\n"
              "    chk.pins['manual_disclosures'] = {'path': p, 'sha256': h}\n"
              "    chk.note('MANUAL_DISCLOSURES_VERIFIED', '%d C-08 rows and %d root disclosures; e_r6_1_text equals prereg r6\\'s E_R6_1'\n"
              "             % (len(obj['c08_table']), len(obj['root_disclosures'])))\n"
              "    return p, h, obj, text\n"
              "\n"
              "\n"
              "def manual_disclosures_record(chk, md):\n"
              "    \"\"\"v004 A110: root's manual disclosures file is re-read just before the record is built; its bytes must still hash to root's pin\n"
              "    (the pin the bytes checked at the start of this build hashed to), else MANUAL_DISCLOSURES_CHANGED_AFTER_CHECK. Returns the record\n"
              "    value {pin {path, sha256}, content (the parsed file), raw_text (its exact text)}, or None.\"\"\"\n"
              "    p, h, obj, text = md\n"
              "    now = Path(p).read_bytes() if Path(p).is_file() else None\n"
              "    if now is None or C.sha_bytes(now) != h:\n"
              "        chk.fail('MANUAL_DISCLOSURES_CHANGED_AFTER_CHECK', '%s now hashes to %s; root pinned %s, the sha of the bytes checked at the start of '\n"
              "                 'this build' % (p, None if now is None else C.sha_bytes(now), h))\n"
              "        return None\n"
              "    return {'pin': {'path': p, 'sha256': h}, 'content': obj, 'raw_text': text}\n"
              "\n"
              "\n"
              "def build(a):\n"
              "    cov = getattr(a, 'covered_later', None)\n"
              "    disp = getattr(a, 'dispositions', None)\n"
              "    chk = C.Checker('build_seal_record_c4v004')\n"
              "    md = manual_disclosures_codes(chk, getattr(a, 'manual_disclosures', None))     # v004 A110: root's file, read once, before tools 1-3 run\n"
              "    res = T3.run(a.slots, a.prereg, a.text_of_record, a.frozen, cov or (), a.reviewed, a.sealed_compare, getattr(a, 'text_of_record_sha', None), disp,\n"
              "                 getattr(a, 'addendum_at_text_of_record', None))\n"))
    R.append(("    led = later_entry_dispositions(chk, disp, pt.get('later_entry_dispositions'), pt.get('dispositions_required'))    # v003 D-05\n",
              "    led = later_entry_dispositions(chk, disp, pt.get('later_entry_dispositions'), pt.get('dispositions_required'))    # v003 D-05\n"
              "    mdr = manual_disclosures_record(chk, md)                                    # v004 A110: re-read just before the record is built\n"))
    R.append(("        'disclosures': disclosures,\n",
              "        'disclosures': disclosures,\n"
              "        'manual_disclosures': mdr,                                              # v004 A110: root's file verbatim, next to the prereg disclosures\n"))
    R.append(("    chk = C.Checker('check_admission_config_c4v003')\n", "    chk = C.Checker('check_admission_config_c4v004')\n"))
    R.append(("    return C.guarded_run('check_admission_config_c4v003', _check_admission_config, config_path, seal_record_path)\n",
              "    return C.guarded_run('check_admission_config_c4v004', _check_admission_config, config_path, seal_record_path)\n"))
    R.append(("        print(json.dumps(C.covered_later_refusal('build_seal_record_c4v003'), indent=1, sort_keys=True), file=sys.stderr)\n",
              "        print(json.dumps(C.covered_later_refusal('build_seal_record_c4v004'), indent=1, sort_keys=True), file=sys.stderr)\n"))
    R.append(("    p.add_argument('--text-of-record-sha')\n"
              "    a = C.parse_args(p, argv)\n"
              "    a.dispositions = None if a.dispositions is None and a.dispositions_sha is None else (a.dispositions, a.dispositions_sha)\n",
              "    p.add_argument('--text-of-record-sha')\n"
              "    p.add_argument('--manual-disclosures')                                      # v004 A110\n"
              "    p.add_argument('--manual-disclosures-sha256')\n"
              "    a = C.parse_args(p, argv)\n"
              "    a.dispositions = None if a.dispositions is None and a.dispositions_sha is None else (a.dispositions, a.dispositions_sha)\n"
              "    a.manual_disclosures = (None if a.manual_disclosures is None and a.manual_disclosures_sha256 is None\n"
              "                            else (a.manual_disclosures, a.manual_disclosures_sha256))\n"))
    R.append(("        return ({'check': 'build_seal_record_c4v003', 'verdict': 'REFUSE',",
              "        return ({'check': 'build_seal_record_c4v004', 'verdict': 'REFUSE',"))
    for old, new in R:
        k = text.count(old)
        if k != 1:
            raise SystemExit('REFUSED: an old text occurs %d times (not once): %r' % (k, old[:120]))
        text = text.replace(old, new, 1)
    # the only c4v003 left: the three imports of v003's unchanged modules, and the header's predecessor name
    left = [ln for ln in text.splitlines() if 'c4v003' in ln]
    want = ["# Claude4 seal tools v004, tool 4 (successor of v003 build_seal_record_c4v003.py de0ceb15; v003 succeeded r2 build_seal_record_c4v002.py",
            'import seal_common_c4v003 as C', 'import check_slot_fill_c4v003 as T3', 'import check_sealed_compare_c4v003 as T2']
    if left != want:
        raise SystemExit('REFUSED: unexpected c4v003 lines %r' % left)
    tree = ast.parse(text)
    got = [ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and [getattr(t, 'id', None) for t in n.targets] == ['E_R6_1']]
    if got != [e]:
        raise SystemExit('REFUSED: the generated E_R6_1 literal is not the SELECTED text')
    compile(text, str(out), 'exec')
    b = text.encode('utf-8')
    with open(out, 'xb') as f:
        f.write(b)
    if sha(out.read_bytes()) != sha(b):
        raise SystemExit('REFUSED: the written bytes re-read differently')
    print(sha(b), out, '%d replacements; E_R6_1 %s, sha256 %s' % (len(R), ascii_note, e_sha))


if __name__ == '__main__':
    main()
