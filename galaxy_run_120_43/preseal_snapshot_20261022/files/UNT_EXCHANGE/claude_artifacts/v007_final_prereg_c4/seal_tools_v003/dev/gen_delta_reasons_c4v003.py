# dev helper (work copy, continuation run 3): write tools/delta_reasons_c4v003.py (exclusive create), the module make_delta_c4v003.py reads:
# ROWS = [(v003 file, the hunk's first changed line, tag, why)] for every non-rename hunk of the six dev sources against the r2 bytes, with the
# reason chosen here per (file, hunk number), and HEAD, the delta's opening text. Fails if a non-rename hunk has no reason here or a reason
# names a hunk that does not exist, so a source change after this point cannot slip through unexplained.
# usage: python3 -I -B gen_delta_reasons_c4v003.py OUT.py
import difflib, hashlib, sys
from pathlib import Path
R2 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2')
D = Path(__file__).resolve().parent
OUT = Path(sys.argv[1])
H = 'header: names v003, its dispatches and the r2 predecessor (sha prefix)'
WHY = {
    ('seal_common_c4v003.py', 1): ('header', H),
    ('seal_common_c4v003.py', 2): ('D-05', 'documents the two v003 additions: strict_json_typed and the bare-list refusal helpers'),
    ('seal_common_c4v003.py', 3): ('D-05', 'DISPOSITIONS_SCHEMA (the dispositions file schema, 0633) and COVERED_LATER_REMOVED (the text of the bare-list refusal)'),
    ('seal_common_c4v003.py', 4): ('D-05', 'strict_json_typed: root\'s dispositions bytes as UTF-8 text through r2\'s strict JSON with native integers and no text '
                                   'fallback, one typed code per defect class; covered_later_flag / covered_later_refusal: the removed --covered-later flag '
                                   '(the = form too) is a typed refusal COVERED_LATER_BARE_NAMES_REFUSED, not a usage error'),
    ('check_frozen_addendum_c4v003.py', 1): ('header', H),
    ('check_frozen_addendum_c4v003.py', 2): ('D-05 (0633, 0640, C-01)', 'the v003 rule written out (the read copy, CH, L, the exact row keys of each '
                                             'disposition, changed_text, prereg_revision); the usage gains --addendum-at-text-of-record and '
                                             '--dispositions/--dispositions-sha in place of --covered-later; os is imported for os.PathLike'),
    ('check_frozen_addendum_c4v003.py', 4): ('D-05 (0640)', 'constants: the addendum_read key of the prereg table, the file\'s exact keys, the exact '
                                             'row keys of each disposition, the ASCII-only entry pattern'),
    ('check_frozen_addendum_c4v003.py', 5): ('D-05 (0633, 0640, C-01)', 'new functions: nonblank; read_copy_bytes (the read copy must hash to the '
                                             'prereg\'s addendum_read pin: ADDENDUM_READ_PIN_ABSENT, ADDENDUM_AT_TEXT_OF_RECORD_REQUIRED, _MISMATCH); '
                                             'dispositions_file (root\'s pin, bytes read once); changed_text_codes (the 0640 substring tests on UTF-8 '
                                             'bytes); prereg_revision_codes (an exact verified pin, not the prereg under check); disposition_codes (one '
                                             'row per entry of L u CH, exact keys per disposition, PV-D05-1); _run takes text_of_record_addendum'),
    ('check_frozen_addendum_c4v003.py', 6): ('D-05 (0640)', 'the table keeps each entry\'s row (a dict, not a set) so every row can be compared with the read copy'),
    ('check_frozen_addendum_c4v003.py', 7): ('D-05 (0640)', 'stores the row for that comparison (r2 added the entry to a set)'),
    ('check_frozen_addendum_c4v003.py', 8): ('D-05 (0640)', 'a changed section records the table row sha, the read copy\'s section sha (when the read '
                                             'copy shows the change) and the frozen section sha'),
    ('check_frozen_addendum_c4v003.py', 9): ('D-05', 'the local need becomes need_t, because need now names L u CH; the check and its message are r2\'s'),
    ('check_frozen_addendum_c4v003.py', 10): ('D-05 (0633, 0640, C-01)', 'r2\'s covered-later handling is replaced: a bare list refuses; the read copy '
                                              'is verified; table rows must be its sections; every entry in both copies is compared (CH, C-01); L adds the '
                                              'entries absent from the read copy; no file while L u CH is non-empty refuses DISPOSITIONS_REQUIRED'),
    ('check_frozen_addendum_c4v003.py', 11): ('D-05', 'the dispositions file is verified (pin, strict parse, rows); a CH entry with no row refuses '
                                              'ENTRY_TABLE_SECTION_CHANGED (table row) or ENTRY_SECTION_CHANGED (C-01), an L entry with no row '
                                              'UNCOVERED_LATER_ENTRY; the layer is skipped (a note) without a verified read copy'),
    ('check_frozen_addendum_c4v003.py', 12): ('D-05', 'the result carries dispositions_required, later_entry_dispositions and addendum_at_text_of_record '
                                              'in place of r2\'s covered_later'),
    ('check_frozen_addendum_c4v003.py', 13): ('D-05', 'run() takes dispositions and text_of_record_addendum'),
    ('check_frozen_addendum_c4v003.py', 14): ('D-05', 'main(): a --covered-later flag is refused with the typed code before argparse sees it'),
    ('check_frozen_addendum_c4v003.py', 15): ('D-05 (0640)', 'the --addendum-at-text-of-record flag (optional for argparse, so a missing copy gets the typed code)'),
    ('check_frozen_addendum_c4v003.py', 16): ('D-05', '--dispositions and --dispositions-sha replace --covered-later'),
    ('check_frozen_addendum_c4v003.py', 17): ('D-05', 'the CLI passes the dispositions pin and the read copy to run()'),
    ('check_sealed_compare_c4v003.py', 1): ('header', H + '; tool 2 is otherwise r2 apart from the renames'),
    ('check_slot_fill_c4v003.py', 1): ('header', H),
    ('check_slot_fill_c4v003.py', 2): ('D-05 (0633, 0640)', 'the v003 pass-through documented; the usage gains --addendum-at-text-of-record and the dispositions flags'),
    ('check_slot_fill_c4v003.py', 4): ('D-05', '_run takes dispositions and text_of_record_addendum'),
    ('check_slot_fill_c4v003.py', 5): ('D-05', 'a non-empty covered_later refuses in tool 3 itself'),
    ('check_slot_fill_c4v003.py', 6): ('rename', 'the version name inside a message (tool 3 v002 -> v003)'),
    ('check_slot_fill_c4v003.py', 8): ('D-05', 'tool 1 receives root\'s dispositions pin and the read copy unchanged'),
    ('check_slot_fill_c4v003.py', 9): ('D-05', 'tool 1\'s verified result passes through (dispositions_required, later_entry_dispositions, '
                                       'addendum_at_text_of_record) in place of covered_later'),
    ('check_slot_fill_c4v003.py', 10): ('D-05', 'a dispositions pin or a read copy without --frozen refuses (DISPOSITIONS_WITHOUT_FROZEN, '
                                        'ADDENDUM_AT_TEXT_OF_RECORD_WITHOUT_FROZEN): only tool 1 can check them'),
    ('check_slot_fill_c4v003.py', 12): ('D-05', 'run() takes dispositions and text_of_record_addendum'),
    ('check_slot_fill_c4v003.py', 13): ('D-05', 'main(): a --covered-later flag is refused with the typed code'),
    ('check_slot_fill_c4v003.py', 14): ('D-05', 'the CLI flags --addendum-at-text-of-record, --dispositions, --dispositions-sha replace --covered-later'),
    ('check_slot_fill_c4v003.py', 15): ('D-05', 'the CLI passes the dispositions pin and the read copy to run()'),
    ('build_seal_record_c4v003.py', 1): ('header', H + '; the builder runs tool 3 v003'),
    ('build_seal_record_c4v003.py', 2): ('D-05 / B8', 'the v003 changes documented (D-05 dispositions and read copy; B8 guard v008 mirror)'),
    ('build_seal_record_c4v003.py', 3): ('D-05', 'the usage: --addendum-at-text-of-record and the dispositions flags replace --covered-later (the '
                                         'exclusive-create line is r2\'s with the rename)'),
    ('build_seal_record_c4v003.py', 6): ('D-05', 'the SEAL_RECORD schema becomes C4V003 (its content changed); the NOT_SUPPLIED_NONE_REQUIRED literal'),
    ('build_seal_record_c4v003.py', 7): ('D-05', 'later_entry_dispositions() replaces no_change_note(): the dispositions file is re-read and must still hash '
                                         'to root\'s pin and to what tool 1 verified (DISPOSITIONS_CHANGED_AFTER_CHECK); the record gets {pin, content, raw_text}'),
    ('build_seal_record_c4v003.py', 8): ('D-05', 'build(): a non-empty covered_later refuses; tool 3 receives the dispositions pin and the read copy'),
    ('build_seal_record_c4v003.py', 9): ('D-05 (0640)', 'addendum_at_text_of_record is a required pass-through'),
    ('build_seal_record_c4v003.py', 10): ('D-05', 'the record value of later_entry_dispositions is computed (and checked) before the record is assembled'),
    ('build_seal_record_c4v003.py', 11): ('D-05', 'the record carries later_entry_dispositions and addendum_at_text_of_record in place of no_change_notes'),
    ('build_seal_record_c4v003.py', 13): ('B8 (0634)', 'the admission check refuses every SEAL_RECORD guard v008 admission() refuses on sealed_by (L32), '
                                          'a missing driver or frozen_addendum (L39) and their pins (L40, pin_check L18), by the stricter Checker.pin'),
    ('build_seal_record_c4v003.py', 15): ('D-05', 'main(): a --covered-later flag is refused with the typed code on stderr; stdout stays empty'),
    ('build_seal_record_c4v003.py', 16): ('D-05', 'the CLI flags --addendum-at-text-of-record, --dispositions, --dispositions-sha replace --covered-later'),
    ('build_seal_record_c4v003.py', 17): ('D-05', 'the CLI dispositions pin is (path, sha256) or None; r2 split the covered-later list'),
    ('print_driver_build_record_c4v003.py', 1): ('header', H + '; tool 5 is otherwise r2 apart from the renames'),
}
rows, used = [], set()
for n in ('seal_common', 'check_frozen_addendum', 'check_sealed_compare', 'check_slot_fill', 'build_seal_record', 'print_driver_build_record'):
    a = (R2 / (n + '_c4v002.py')).read_text().splitlines()
    f = n + '_c4v003.py'
    b = (D / f).read_text().splitlines()
    k = 0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == 'equal':
            continue
        k += 1
        al, bl = a[i1:i2], b[j1:j2]
        if len(al) == len(bl) and al and all(x.replace('c4v002', 'c4v003') == y for x, y in zip(al, bl)):
            continue
        if (f, k) not in WHY:
            raise SystemExit('no reason for %s hunk %d: %r' % (f, k, (bl[0] if bl else al[0])[:100]))
        used.add((f, k))
        t, w = WHY[(f, k)]
        rows.append((f, (bl[0] if bl else al[0]).strip(), t, w))
if set(WHY) - used:
    raise SystemExit('unused reasons %r' % sorted(set(WHY) - used))
r2pins = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(R2.glob('*_c4v002.py'))}
head = ('# DELTA: seal tools v002 r2 -> v003 (Claude4; D-05 dispatches 0633 and 0640 with C-01; B8 dispatch 0634; A104-A106)\n\n'
        'Every changed line of the six v003 sources against the r2 bytes of record, hunk by hunk, each with its reason. Generated by '
        '`tools/make_delta_c4v003.py` (difflib SequenceMatcher opcodes over lines, no context) with the reasons of `tools/delta_reasons_c4v003.py`: a hunk '
        'whose + lines are exactly its - lines with c4v002 -> c4v003 is classed rename mechanically; every other hunk carries a reason, and the generator '
        'fails on a hunk without one or a reason without a hunk. The r2 inputs are verified from bytes first:\n\n'
        + ''.join('- r2 `%s` `%s`\n' % (k, v) for k, v in r2pins.items()) +
        '\nNothing outside D-05 (with C-01), B8, the README parser note, the W7-S1 tests and the renames changed (A106.2, option (b)). Tools 2 and 5 change '
        'only in their header and the renames. The README is a new document, README_SEAL_TOOLS_V003.md; its "What v003 changes" table lists its changes '
        'against v002\'s README.\n')
with open(OUT, 'x') as fo:
    fo.write('# Claude4 seal tools v003 (BUILD helper): the reasons make_delta_c4v003.py attaches to each non-rename hunk; generated by\n'
             '# dev/gen_delta_reasons_c4v003.py from the final dev sources (keys: v003 file, the hunk\'s first changed line, stripped).\n'
             'HEAD = %r\nROWS = %r\n' % (head, rows))
print(len(rows), 'reasons')
