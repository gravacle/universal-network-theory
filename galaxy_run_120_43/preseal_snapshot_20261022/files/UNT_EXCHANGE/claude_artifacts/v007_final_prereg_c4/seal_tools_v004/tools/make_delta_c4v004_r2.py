# Claude4 seal tools v004 (BUILD helper; A110, dispatch 0646): DELTA_V003_TO_V004.md, every changed line of the v004 sources and tests against
# the v003 bytes of record, hunk by hunk, each with its reason. The diff is difflib.SequenceMatcher opcodes over lines (no context). A hunk whose
# '+' lines are exactly its '-' lines with c4v003 -> c4v004 (lower case, as in v003) is classed 'rename' mechanically; every other hunk takes its reason
# from REASONS below, keyed by (file, the hunk's first changed line, stripped), and the run fails if any hunk has no reason or any reason is
# unused. The v003 inputs are verified from bytes first; the five unchanged sources must be byte-identical. OUT is created exclusively.
# r2 (successor of tools/make_delta_c4v004.py, which refused (UNUSED REASONS: its either-case rename rule classed the two schema
# hunks of the tests as renames) and wrote nothing): the rename rule is lower-case only, as in v003, and the TEST_RESULTS hunk has a reason.
# usage: python3 -I -B make_delta_c4v004_r2.py V004_DIR OUT.md
import difflib, hashlib, sys
from pathlib import Path

V3 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v003')
V3_PINS = {'seal_common_c4v003.py': '101a3aeb9846a21c35993e8e7e4b50a8f1206ed4202b131afd12d7e496c5ab21',
           'check_frozen_addendum_c4v003.py': 'a56f8d793750151920b1b47e77b46aebbfadea71fe77730f360beb02af788fb4',
           'check_sealed_compare_c4v003.py': 'c2c5dfc5ddba1e44ff82811a38d4c05b0a669f2294b229efe3437623d596f9f1',
           'check_slot_fill_c4v003.py': '316973a1abf5aa2151dc1a517733d970ce1004313395d05fe590f82ed439b0af',
           'print_driver_build_record_c4v003.py': 'e5bedffe3c91650d5dba7fbd1ed5476e228158679d8959dfea0e2eff436ebdea',
           'build_seal_record_c4v003.py': 'de0ceb15ebfb95e04227730bd2785eb46af8cb5980012de91de98f34ea226b96',
           'tests/test_seal_tools_c4v003.py': '67dd8a0085436639ef85650ca966b6b9ae045cc9413f01fc943b7003f142099a',
           'tools/fence_c4v002.py': 'c993d34c185d785d77c443a00033e8efeea10cd02f1a547a99af458c0f698eb5',
           'tools/run_fenced_c4st2.py': 'fe904509c7d2d6300042589aaa02d839e82b436680d293b65c5c7d4cf69f6d25'}
SAME = ['seal_common_c4v003.py', 'check_frozen_addendum_c4v003.py', 'check_sealed_compare_c4v003.py', 'check_slot_fill_c4v003.py',
        'print_driver_build_record_c4v003.py', 'tools/fence_c4v002.py', 'tools/run_fenced_c4st2.py']
CHANGED = [('build_seal_record_c4v003.py', 'build_seal_record_c4v004.py'), ('tests/test_seal_tools_c4v003.py', 'tests/test_seal_tools_c4v004.py')]
T4 = 'build_seal_record_c4v004.py'
TT = 'tests/test_seal_tools_c4v004.py'
ROWS = [
    (T4, '# Claude4 seal tools v004, tool 4 (successor of v003 build_seal_record_c4v003.py de0ceb15; v003 succeeded r2 build_seal_record_c4v002.py',
     'header', 'names v004, its predecessor v003 build_seal_record_c4v003.py (de0ceb15) and v003\'s predecessor r2 (4192983d)'),
    (T4, '# New in v004 (A110; dispatches 0646 and 0647; Codex1 0114 C3V007-DISCLOSURE-01). Nothing else changes: tools 1, 2, 3 and 5 and',
     'A110 (doc)', 'the v004 change written out: the one new input, its pin, read once, the strict parse, the exact form, the re-read, the record '
     'field and the record schema; tools 1, 2, 3, 5 and seal_common are v003\'s bytes'),
    (T4, "#        --manual-disclosures M.json --manual-disclosures-sha256 H   (v004 A110: root's SEAL_MANUAL_DISCLOSURES_V001 file; required)",
     'A110 (doc)', 'the usage names the two new flags; the admission-mode usage line that follows is v003\'s with the c4v004 file name'),
    (T4, "SCHEMA = 'UNT_V007_SEAL_RECORD_C4V004'                       # v004 A110: the record content changed (manual_disclosures); v003 C4V003",
     'A110', 'the SEAL_RECORD content changed (the manual_disclosures field), so the record schema becomes UNT_V007_SEAL_RECORD_C4V004, as v003 '
     'renamed it for D-05 (README_SEAL_TOOLS_V003, row "rename"); the v004 admission check then refuses a v003 record, which carries no manual '
     'disclosures (ADMISSION_SEAL_RECORD_SCHEMA, TESTED). Guard v008, launcher v007 and Claude3\'s c3v017 helper do not read the record schema '
     '(source reading); the real guard and launcher accept the v004 record (TESTED)'),
    (T4, "MANUAL_DISCLOSURES_SCHEMA = 'SEAL_MANUAL_DISCLOSURES_V001'    # v004 A110: root's file (seal_assembly_c3/root_inputs, 0647)",
     'A110', 'constants: the disclosures file\'s schema, its exact key set, the C-08 row keys (declared_in_r13 optional: 0646 names three keys, root\'s '
     'file four), the NEW-item id form (ASCII digits), the root-disclosure row keys, and E_R6_1, generated from the bytes of SELECTED_R6_C4V001.json '
     '(7200acd9) basis.erratum_E_R6_1 by tools/make_tool4_c4v004.py (469 ASCII characters, UTF-8 sha256 c28202b0; checked by AST after the write, '
     'and by the suite against the SELECTED file re-read)'),
    (T4, "def strings_of(obj, where='$'):",
     'A110', 'new functions: strings_of and has_utf8_form (a lone surrogate refuses with a typed code, not INTERNAL_EXCEPTION); manual_disclosures_form_codes '
     '(the exact form, e_r6_1_text non-empty and equal to E_R6_1, the C-08 rows, root_disclosures, unique ids); manual_disclosures_codes (the pin: '
     'given, a (path, sha256) pair of strings, an absolute path, a regular file, bytes that hash to the pin, read once; those bytes through v003\'s '
     'strict_json_typed with the MANUAL_DISCLOSURES prefix; then the form; on PASS the pin is listed and MANUAL_DISCLOSURES_VERIFIED noted); '
     'manual_disclosures_record (the re-read; the record value {pin, content, raw_text})'),
    (T4, "chk = C.Checker('build_seal_record_c4v004')",
     'A110', 'build(): the checker is created before tools 1-3 run, so root\'s file is checked (and read once) first and every later step lies '
     'between the check and the re-read; its name follows the file (c4v004)'),
    (T4, "chk = C.Checker('build_seal_record_c4v003')",
     'A110', 'the v003 checker line, moved above tools 1-3 (previous hunk)'),
    (T4, 'mdr = manual_disclosures_record(chk, md)                                    # v004 A110: re-read just before the record is built',
     'A110', 'the re-read, right before the record is assembled; its refusal (MANUAL_DISCLOSURES_CHANGED_AFTER_CHECK) joins v003\'s last refusal check'),
    (T4, "'manual_disclosures': mdr,                                              # v004 A110: root's file verbatim, next to the prereg disclosures",
     'A110', 'the record carries root\'s file verbatim, {pin {path, sha256}, content, raw_text}, next to the derived prereg disclosures (v003\'s '
     '"disclosures" list is unchanged)'),
    (T4, "p.add_argument('--manual-disclosures')                                      # v004 A110",
     'A110', 'the two CLI flags; optional for argparse, so an omitted pin is the typed MANUAL_DISCLOSURES_REQUIRED, not a usage error'),
    (T4, 'a.manual_disclosures = (None if a.manual_disclosures is None and a.manual_disclosures_sha256 is None',
     'A110', 'the CLI pin is (path, sha256) when either flag is given (a half pin refuses MANUAL_DISCLOSURES_PIN_MISMATCH) and None when neither is '
     '(MANUAL_DISCLOSURES_REQUIRED), as v003 forms the dispositions pin'),
    (TT, '# Claude4 seal tools v004: tamper tests for the five seal tools with tool 4 v004 (A110, dispatches 0646 and 0647: root\'s manual disclosures',
     'header', 'the v003 header is replaced by the v004 one: the port, its tags, its port map and the new cases'),
    (TT, '', 'port bookkeeping', 'tool 4\'s two entry points (safe_build, main) are wrapped to count builder calls, so a ported case that called the builder '
     'is tagged PORT_CHANGED; a results list that stamps the count; an audit hook that counts opens of one path (the read-once control)'),
    (TT, '# v004 (A110): the v003 suite of record (the port map), the v003 sources (the five unchanged copies must be their bytes), prereg r6\'s SELECTED',
     'v004 constants', 'the v003 results of record (26bb912f), the v003 source pins, prereg r6\'s SELECTED file, root\'s disclosures file, the four '
     'case-text renames and the PORT_CHANGED reasons'),
    (TT, 'results = _Results()                              # v004: stamped with the builder-call count (port tags)',
     'port bookkeeping', 'the results list stamps the builder-call count'),
    (TT, 'assert C.sha(p) == h, p',
     'v004 inputs', 'the v003 results (the port map) and prereg r6\'s SELECTED file (the E_R6_1 source) are verified from bytes before any case, as v003 '
     'verifies its own inputs'),
    (TT, '# ---------------- v004 (A110): the manual disclosures fixtures, in root\'s SEAL_MANUAL_DISCLOSURES_V001 form with SYNTHETIC rows and texts;',
     'A110', 'the SYNTHETIC manual disclosures fixtures (md_obj, mdisc) and the base fixture MD0; its e_r6_1_text is read from SELECTED_R6_C4V001\'s '
     'bytes, not taken from tool 4'),
    (TT, 'a.manual_disclosures = MD0                        # v004 (A110): the SYNTHETIC manual disclosures fixture',
     'A110', 'the builder\'s base arguments carry MD0, so every ported tool 4 case (and every copy of its arguments) still tests only what it tested'),
    (TT, "and rec.get('later_entry_dispositions') == LED0 and 'no_change_notes' not in rec and rec.get('schema') == 'UNT_V007_SEAL_RECORD_C4V004'",
     'A110', 'the genuine record\'s expected schema is UNT_V007_SEAL_RECORD_C4V004 (the one changed expectation of the port)'),
    (TT, "'(schema C4V004)',", 'A110', 'the genuine case\'s text names the v004 schema (V4_RENAMES)'),
    (TT, "'--new-item-list', str(newl), '--successor-custody', str(cust), '--b2-record', str(B2_REC),",
     'A110', 'the builder\'s base CLI argv carries MD0 (--manual-disclosures, --manual-disclosures-sha256)'),
    (TT, "results.append({'tool': 'integration', 'tag': 'PORT', 'r2': 130, 'why': None, 'case': 'real guard v008 admits the v004 SEAL_RECORD (via the checked config); real launcher '",
     'case text', 'the record named is v004\'s (V4_RENAMES); call and expectation unchanged'),
    (TT, "check('integration', 'B8 control: the genuine v004 record and its config still pass the v004 admission check and the real guard v008 admission()',",
     'case text', 'the record and the admission check named are v004\'s (V4_RENAMES); call and expectation unchanged'),
    (TT, "'v004 SEAL_RECORD', 'expect': 'PASS', 'verdict': 'PASS' if oR == 'ok' else 'REFUSE', 'codes': [oR], 'notes': [], 'ok': oR == 'ok'})",
     'case text', 'the record named is v004\'s (V4_RENAMES); call and expectation unchanged'),
    (TT, "# ================= v004 (A110): tool 4 v004's manual disclosures input (new cases, each marked v004_new)",
     'A110', 'the 115 new v004 cases (before the guard reset): the unchanged files and E_R6_1, root\'s real file by API and CLI (and its record under the '
     'v004 admission check and the real guard), a v003-form record under the v004 admission check, the read-once control, every refusal of the new '
     'input, the change after the check at two points, layered reporting, the CLI forms'),
    (TT, "# ================= the port maps: every v003 case once, in v003's order (TEST_RESULTS_C4V003.json 26bb912f); every r2 case once, by index (v003's)",
     'summary', 'the v003 port map: every v003 case once, in order, with its tool, tag, r2 index, expectation and text (or its listed rename); a ported '
     'case is PORT, or PORT_CHANGED when it called the builder; then v003\'s own r2 port map'),
    (TT, "r2ported = sorted(r['r2'] for r in results if r.get('r2') is not None)",
     'summary', 'v003\'s r2 port map, unchanged, on a renamed variable (ported now names the v003 port list)'),
    (TT, "bad_tags = [r['case'] for r in ported if r['v003_tag'] == 'PORT_CHANGED' and not r.get('v003_why')]",
     'summary', 'v003\'s check that each of its PORT_CHANGED cases gives a reason, now read from the v003 fields of the ported results'),
    (TT, "'check_slot_fill_c4v003.py', 'build_seal_record_c4v004.py', 'print_driver_build_record_c4v003.py')},",
     'summary', 'the summary hashes build_seal_record_c4v004.py'),
    (TT, 'CX1_PV[0], CX1_PV[1], CX1_PV[2], CX1_OLD_A90, R5_READ, V3_RESULTS, R6_SELECTED, ROOT_MD]',
     'summary', 'the summary lists the v004 inputs read (the v003 results, prereg r6\'s SELECTED file, root\'s file, the v003 sources)'),
    (TT, "'frozen_A62_edited': pin(f_62), 'frozen_A90_edited': pin(f_90), 'cx1_pv_d05_1_read_copy': pin(rc_cx),",
     'summary', 'the summary lists MD0 and the v003 port record'),
    (TT, "with open(run / 'TEST_RESULTS_C4V004.json', 'x') as f:", 'summary', 'the results record is TEST_RESULTS_C4V004.json (exclusive create, as in v003)'),
    (TT, "print('%-11s %-12s %-4s %-96s %-7s %s' % (r['tool'], r['tag'], '' if r.get('v003') is None else r['v003'], r['case'][:96], 'ok' if r['ok'] else 'NOT_OK',",
     'summary', 'the printed table shows the v003 index in place of the r2 index'),
    (TT, "print('passed', summary['passed'], '/', summary['total'], summary['by_tag'], 'port_v003', {k: v for k, v in summary['port_v003'].items() if k != 'renamed'},",
     'summary', 'the run passes only if every case passes and both port maps hold (each with every PORT_CHANGED case giving its reason)'),
]
HEAD = ('# DELTA: seal tools v003 -> v004 (Claude4; A110, dispatches 0646 and 0647; Codex1 0114 C3V007-DISCLOSURE-01)\n\n'
        'Every changed line of the v004 sources and tests against the v003 bytes of record (SELECTED_SEAL_TOOLS_V003_C4V001 cf7e5b2f), hunk by hunk, '
        'each with its reason. Generated by `tools/make_delta_c4v004.py` (difflib SequenceMatcher opcodes over lines, no context): a hunk whose + lines '
        'are exactly its - lines with c4v003 -> c4v004 is classed rename mechanically; every other hunk carries a reason, and the '
        'generator fails on a hunk without one or a reason without a hunk. The v003 inputs are verified from bytes first.\n\n'
        '**Unchanged, byte-identical to v003 (sha256 from bytes, same names):**\n\n%s\n'
        '**Changed:** tool 4 only, as the new file `build_seal_record_c4v004.py` (v003 `build_seal_record_c4v003.py` `de0ceb15`), and the tests, as '
        '`tests/test_seal_tools_c4v004.py` (v003 `tests/test_seal_tools_c4v003.py` `67dd8a00`). Nothing outside A110 changed in tool 4: the hunks are '
        'the header and usage, the record schema, the new constants and functions, the check before tools 1-3, the re-read, the record field, the CLI '
        'flags, and the c4v004 renames of the tool\'s own names. The README of the change is README_SEAL_TOOLS_V004_DELTA.md.\n')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def hunks(a, b):
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag != 'equal':
            out.append((i1, a[i1:i2], j1, b[j1:j2]))
    return out


def renamed(x):
    return x.replace('c4v003', 'c4v004')


def main():
    v4, out = Path(sys.argv[1]), Path(sys.argv[2])
    for rel, h in V3_PINS.items():
        assert sha((V3 / rel).read_bytes()) == h, rel
    same_lines = []
    for rel in SAME:
        b = (v4 / rel).read_bytes()
        assert sha(b) == V3_PINS[rel], 'not byte-identical: %s' % rel
        same_lines.append('- `%s` `%s` (v003 `%s`, identical)' % (rel, sha(b), V3_PINS[rel][:8]))
    reasons = {}
    for f, first, tag, why in ROWS:
        key = (f, first.strip())
        assert key not in reasons, key
        reasons[key] = (tag, why)
    used, totals, body = set(), {}, []
    for v3name, v4name in CHANGED:
        ra, rb = (V3 / v3name).read_bytes(), (v4 / v4name).read_bytes()
        a, b = ra.decode('utf-8').splitlines(), rb.decode('utf-8').splitlines()
        hs = hunks(a, b)
        body.append('\n## `%s`\n\nv003 `%s` `%s` (%d lines) -> v004 `%s` `%s` (%d lines), %d hunks.\n' % (v4name, v3name, V3_PINS[v3name][:8], len(a), v4name,
                                                                                                   sha(rb)[:8], len(b), len(hs)))
        for k, (i1, al, j1, bl) in enumerate(hs, 1):
            if len(al) == len(bl) and al and all(renamed(x) == y for x, y in zip(al, bl)):
                tag, why = 'rename', 'v003 -> v004 file, check-name, usage or record-name rename only'
            else:
                key = (v4name, (bl[0] if bl else al[0]).strip())
                if key not in reasons:
                    raise SystemExit('NO REASON for %s hunk %d, first changed line: %r' % (v4name, k, key[1]))
                used.add(key)
                tag, why = reasons[key]
            totals[tag] = totals.get(tag, 0) + 1
            span_a = 'v003 L%d-%d' % (i1 + 1, i1 + len(al)) if al else 'v003 after L%d' % i1
            span_b = 'v004 L%d-%d' % (j1 + 1, j1 + len(bl)) if bl else 'v004 after L%d' % j1
            body.append('### %s hunk %d: %s, %s -- **%s**\n\n%s\n\n```diff\n%s\n```\n' % (
                v4name, k, span_a, span_b, tag, why, '\n'.join(['-' + x for x in al] + ['+' + x for x in bl])))
    unused = sorted(set(reasons) - used)
    if unused:
        raise SystemExit('UNUSED REASONS %r' % unused)
    head = HEAD % '\n'.join(same_lines) + '\nHunks by reason: %s.\n' % ', '.join('%s %d' % (t, n) for t, n in sorted(totals.items()))
    with open(out, 'x') as f:
        f.write(head + '\n'.join(body))
    print('hunks', totals)


if __name__ == '__main__':
    main()
