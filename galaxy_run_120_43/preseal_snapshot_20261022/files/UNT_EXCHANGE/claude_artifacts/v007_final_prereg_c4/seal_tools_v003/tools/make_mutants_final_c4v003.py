# Claude4 seal tools v003 (BUILD helper, continuation run 3): the FINAL mutation set. For each mutant, copy the six final dev/ v003 sources
# and dev/tests/test_seal_tools_c4v003.py into mutants/final/<SET>/<id>/ (round 1 wrote mutants/final/<id>/ directly, with the earlier test
# whose harness could stop on a refused genuine build; round 2, SET=round2, is the set of record) (work copies, exclusive create) and apply ONE exact
# replacement that disables or weakens one v003 check (the old text must occur exactly once in its file; the mutant must still compile).
# The caller runs the suite in each folder under the fence; a mutant is KILLED when at least one case is NOT_OK while the ENVIRONMENT
# case (the open V005 did not change during the run) is ok. The manifest MUTANTS_FINAL_C4V003.json (exclusive create) lists every mutant
# with the sha of the dev source it was cut from. Writes only under <this folder>/mutants/final/. No process, no network, no delete.
# usage: python3 -I -B run_fenced_c4st2.py make_mutants_final_c4v003.py SET
import hashlib, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
DEV = HERE / 'dev'
OUT = HERE / 'mutants' / 'final' / sys.argv[1]
SC, T1, T3, T4 = 'seal_common_c4v003.py', 'check_frozen_addendum_c4v003.py', 'check_slot_fill_c4v003.py', 'build_seal_record_c4v003.py'
SRC = (SC, T1, 'check_sealed_compare_c4v003.py', T3, T4, 'print_driver_build_record_c4v003.py')
TEST = 'tests/test_seal_tools_c4v003.py'
MUTANTS = [
    # ---- tool 1: the bare list
    ('M01_t1_api_bare_names_allowed', T1, "    if covered_later:\n        chk.fail('COVERED_LATER_BARE_NAMES_REFUSED'",
     "    if False:\n        chk.fail('COVERED_LATER_BARE_NAMES_REFUSED'"),
    ('M02_t1_cli_flag_unchecked', T1, "    if C.covered_later_flag(argv):                       # v003 D-05: the removed flag is a typed refusal, not a usage error\n"
     "        return C.emit(C.covered_later_refusal('check_frozen_addendum_c4v003'))\n", ''),
    # ---- tool 1: the read copy (0640 old bytes)
    ('M03_t1_read_copy_not_required', T1, "        chk.fail('ADDENDUM_AT_TEXT_OF_RECORD_REQUIRED', 'root gives the V005 copy",
     "        chk.note('ADDENDUM_AT_TEXT_OF_RECORD_REQUIRED', 'root gives the V005 copy"),
    ('M04_t1_read_copy_missing_file_allowed', T1, "        chk.fail('ADDENDUM_AT_TEXT_OF_RECORD_REQUIRED', 'not a regular file: %s' % path)",
     "        chk.note('ADDENDUM_AT_TEXT_OF_RECORD_REQUIRED', 'not a regular file: %s' % path)"),
    ('M05_t1_read_copy_sha_unchecked', T1, "    if got != want:\n", "    if False:\n"),
    ('M06_t1_read_copy_bytes_unchecked', T1, "    if type(n) is int and n != len(raw):", "    if False:"),
    ('M07_t1_addendum_read_pin_unchecked', T1, "    if not (isinstance(want, str) and C.HEX64.fullmatch(want)):", "    if False:"),
    ('M08_t1_read_copy_dup_heading_allowed', T1, "        if rdup:", "        if False:"),
    ('M09_t1_cited_absent_from_read_copy_allowed', T1, "        if miss_r:", "        if False:"),
    ('M10_t1_read_copy_entry_gone_allowed', T1, "        if gone:", "        if False:"),
    ('M11_t1_table_row_missing_from_read_copy_allowed', T1, "                chk.fail('ENTRY_TABLE_ROW_NOT_THE_TEXT_OF_RECORD', 'A%d: the read copy has no such entry' % n)",
     "                chk.note('ENTRY_TABLE_ROW_NOT_THE_TEXT_OF_RECORD', 'A%d: the read copy has no such entry' % n)"),
    ('M12_t1_table_row_sha_vs_read_copy_unchecked', T1, "            if r['section_sha256'] != C.sha_bytes(rs) or", "            if False and r['section_sha256'] != C.sha_bytes(rs) or"),
    ('M13_t1_table_row_bytes_vs_read_copy_unchecked', T1, "(r['section_bytes'] is not None and r['section_bytes'] != len(rs))", "(False)"),
    ('M14_t1_table_row_heading_vs_read_copy_unchecked', T1, "(r['heading'] is not None and r['heading'] != rh)", "(False)"),
    # ---- tool 1: CH and L
    ('M15_t1_ch_read_vs_frozen_skipped', T1, "            if o != nw:", "            if False:"),
    ('M16_t1_ch_only_table_rows_as_r2', T1, "        for n in sorted(set(rsecs) & hset):", "        for n in sorted(set(rsecs) & hset & set(table)):"),
    ('M17_t1_l_absent_from_read_copy_dropped', T1, "        l_set = ({n for n in later if n not in table} | {n for n in hset if n not in rsecs}) - ch",
     "        l_set = {n for n in later if n not in table} - ch"),
    ('M18_t1_dispositions_never_required', T1, "            if need:\n                chk.fail('DISPOSITIONS_REQUIRED'", "            if False:\n                chk.fail('DISPOSITIONS_REQUIRED'"),
    ('M19_t1_uncovered_later_allowed', T1, "        if uncovered:", "        if False:"),
    ('M20_t1_changed_table_row_undisposed_allowed', T1, "                chk.fail('ENTRY_TABLE_SECTION_CHANGED', 'A%d: the frozen section hashes to %s, the table row says %s; a revised or '",
     "                chk.note('ENTRY_TABLE_SECTION_CHANGED', 'A%d: the frozen section hashes to %s, the table row says %s; a revised or '"),
    ('M21_t1_changed_cited_entry_undisposed_allowed', T1, "                chk.fail('ENTRY_SECTION_CHANGED', 'A%d%s:", "                chk.note('ENTRY_SECTION_CHANGED', 'A%d%s:"),
    # ---- tool 1: rows
    ('M22_t1_plain_no_change_on_ch_allowed', T1, "            if d == 'no_change' and n in ch:", "            if False:"),
    ('M23_t1_no_change_after_change_on_l_allowed', T1, "            if d == 'no_change_after_change' and n in l_set:", "            if False:"),
    ('M24_t1_row_keys_unchecked', T1, "            if set(r) != want:", "            if False:"),
    ('M25_t1_row_extra_keys_allowed', T1, "            if set(r) != want:", "            if not want <= set(r):"),
    ('M26_t1_prereg_revision_not_required', T1, "            if d == 'revised' and 'prereg_revision' not in r:", "            if False:"),
    ('M27_t1_value_unchecked', T1, "        if not (isinstance(d, str) and d in DISPOSITION_ROW_KEYS):", "        if not isinstance(d, str):"),
    ('M28_t1_section_sha_unchecked', T1, "        if 'section_sha256' in r and r['section_sha256'] != C.sha_bytes(secs[n][0][1]):", "        if False:"),
    ('M29_t1_reason_unchecked', T1, "        if 'reason' in r and not nonblank(r['reason']):", "        if False:"),
    ('M30_t1_why_no_prereg_effect_unchecked', T1, "        if 'why_no_prereg_effect' in r and not nonblank(r['why_no_prereg_effect']):", "        if False:"),
    ('M31_t1_nonblank_without_strip', T1, "    return isinstance(x, str) and bool(x.strip())", "    return isinstance(x, str) and bool(x)"),
    ('M32_t1_changed_text_skipped', T1, "        if 'changed_text' in r:\n", "        if False:\n"),
    ('M33_t1_changed_text_not_in_new_unchecked', T1, "    if b not in new:", "    if False:"),
    ('M34_t1_changed_text_in_old_unchecked', T1, "    if b in old:", "    if False:"),
    ('M35_t1_changed_text_empty_allowed', T1, "    if not (isinstance(ct, str) and ct):", "    if not isinstance(ct, str):"),
    ('M36_t1_changed_text_old_is_the_frozen_section', T1, "rsecs[n][0][1] if n in rsecs else b'')", "secs[n][0][1])"),
    ('M37_t1_changed_text_surrogatepass', T1, "        b = ct.encode('utf-8')\n", "        b = ct.encode('utf-8', 'surrogatepass')\n"),
    ('M38_t1_prereg_revision_pin_unchecked', T1, "    if not sub.pin('%s.prereg_revision' % w, ref):", "    if False:"),
    ('M39_t1_prereg_revision_may_be_the_prereg', T1, "    if str(Path(ref['path']).resolve()) == prereg_real or ref['sha256'] == prereg_sha:", "    if False:"),
    ('M40_t1_prereg_revision_identity_by_path_only', T1, "    if str(Path(ref['path']).resolve()) == prereg_real or ref['sha256'] == prereg_sha:",
     "    if str(Path(ref['path']).resolve()) == prereg_real:"),
    ('M41_t1_prereg_revision_skipped', T1, "        if 'prereg_revision' in r:\n            prereg_revision_codes(", "        if False:\n            prereg_revision_codes("),
    ('M42_t1_tabled_row_allowed', T1, "            if n in table:\n                chk.fail('DISPOSITION_FOR_TABLED_ENTRY'", "            if False:\n                chk.fail('DISPOSITION_FOR_TABLED_ENTRY'"),
    ('M43_t1_cited_row_allowed', T1, "            if n <= last:\n                chk.fail('DISPOSITION_FOR_CITED_ENTRY'", "            if False:\n                chk.fail('DISPOSITION_FOR_CITED_ENTRY'"),
    ('M44_t1_duplicate_rows_allowed', T1, "        if n in seen:\n            chk.fail('DISPOSITION_DUPLICATE_ENTRY'", "        if False:\n            chk.fail('DISPOSITION_DUPLICATE_ENTRY'"),
    ('M45_t1_dispositions_pin_sha_unchecked', T1, "    if got != h:\n        chk.fail('DISPOSITIONS_PIN_MISMATCH'", "    if False:\n        chk.fail('DISPOSITIONS_PIN_MISMATCH'"),
    ('M46_t1_dispositions_frozen_sha_unchecked', T1, "    if 'frozen_addendum_sha256' in obj and obj['frozen_addendum_sha256'] != fsha:", "    if False:"),
    ('M47_t1_dispositions_schema_unchecked', T1, "    if 'schema' in obj and obj['schema'] != C.DISPOSITIONS_SCHEMA:", "    if False:"),
    ('M48_t1_dispositions_file_keys_unchecked', T1, "    if set(obj) != DISPOSITIONS_KEYS:", "    if False:"),
    ('M49_t1_entry_rx_unicode_digits', T1, "DISPOSITION_ENTRY_RX = re.compile(r'A([1-9][0-9]{0,2})')", r"DISPOSITION_ENTRY_RX = re.compile(r'A([1-9]\d{0,2})')"),
    ('M50_t1_verified_despite_failures', T1, "                    if len(chk.failures) == before and all(n in seen for n in need):", "                    if True:"),
    ('M51_t1_verified_without_every_needed_row', T1, "                    if len(chk.failures) == before and all(n in seen for n in need):",
     "                    if len(chk.failures) == before:"),
    # ---- tool 3
    ('M52_t3_api_bare_names_unchecked', T3, "    if covered_later:                                                           # v003 D-05\n", "    if False:\n"),
    ('M53_t3_cli_flag_unchecked', T3, "    if C.covered_later_flag(argv):                       # v003 D-05: the removed flag is a typed refusal, not a usage error\n"
     "        return C.emit(C.covered_later_refusal('check_slot_fill_c4v003'))\n", ''),
    ('M54_t3_dispositions_not_passed_to_t1', T3, "covered_later, False, dispositions, text_of_record_addendum)", "covered_later, False, None, text_of_record_addendum)"),
    ('M55_t3_read_copy_not_passed_to_t1', T3, "covered_later, False, dispositions, text_of_record_addendum)", "covered_later, False, dispositions, None)"),
    ('M56_t3_read_copy_without_frozen_allowed', T3, "        if text_of_record_addendum is not None:                                 # v003 D-05 (0640): only tool 1 reads the copy",
     "        if False:"),
    ('M57_t3_dispositions_without_frozen_allowed', T3, "        if dispositions is not None:                                            # v003 D-05: only tool 1 can verify the file",
     "        if False:"),
    ('M58_t3_passthrough_read_copy_dropped', T3, "        passthrough['addendum_at_text_of_record'] = r1.get('addendum_at_text_of_record')",
     "        passthrough['addendum_at_text_of_record'] = None"),
    ('M59_t3_passthrough_dispositions_dropped', T3, "        passthrough['later_entry_dispositions'] = r1.get('later_entry_dispositions')",
     "        passthrough['later_entry_dispositions'] = None"),
    ('M60_t3_cli_read_copy_dropped', T3, "a.text_of_record_sha, disp,\n                      a.addendum_at_text_of_record))", "a.text_of_record_sha, disp,\n                      None))"),
    # ---- tool 4 (builder and B8)
    ('M61_t4_api_bare_names_unchecked', T4, "    if cov:                                                                     # v003 D-05\n", "    if False:\n"),
    ('M62_t4_cli_flag_unchecked', T4, "    if C.covered_later_flag(argv):                       # v003 D-05: the removed flag is a typed refusal (stderr; stdout stays empty)\n"
     "        print(json.dumps(C.covered_later_refusal('build_seal_record_c4v003'), indent=1, sort_keys=True), file=sys.stderr)\n        return 2\n", ''),
    ('M63_t4_no_reread', T4, "    p, h = disp\n    vp = verified['pin']\n", "    return dict(verified)\n    p, h = disp\n    vp = verified['pin']\n"),
    ('M64_t4_reread_sha_vs_verified_unchecked', T4, "    if got is None or got != h or got != vp.get('sha256') or p != vp.get('path'):",
     "    if got is None or got != h or p != vp.get('path'):"),
    ('M65_t4_reread_text_unchecked', T4, "    if bad is not None or text != verified.get('raw_text') or json.dumps(", "    if bad is not None or json.dumps("),
    ('M66_t4_read_copy_not_passed', T4, "                 getattr(a, 'addendum_at_text_of_record', None))", "                 None)"),
    ('M67_t4_record_read_copy_dropped', T4, "        'addendum_at_text_of_record': dict(pt['addendum_at_text_of_record']),\n", ''),
    ('M68_t4_none_required_literal_dropped', T4, "        return DISPOSITIONS_NONE_REQUIRED\n", "        return None\n"),
    ('M69_t4_cli_read_copy_flag_dropped', T4, "    p.add_argument('--addendum-at-text-of-record')\n    p.add_argument('--dispositions')\n", "    p.add_argument('--dispositions')\n"),
    ('M70_t4_b8_sealed_by_unchecked', T4, "    if seal.get('sealed_by') != C.AUTHORITY:", "    if False:"),
    ('M71_t4_b8_pins_unchecked', T4, "        if sub.pin('seal.' + key, seal[key]):", "        if True or sub.pin('seal.' + key, seal[key]):"),
    ('M72_t4_b8_missing_key_unchecked', T4, "        if key not in seal:                                                     # guard v008 L39 SEALED_<KEY>_REQUIRED\n"
     "            chk.fail('ADMISSION_SEAL_%s_REQUIRED' % key.upper(), 'the SEAL_RECORD carries no %s pin (guard v008 L39)' % key)\n            continue\n",
     "        if key not in seal:\n            continue\n"),
    ('M73_t4_w7s1_record_allowlist_unchecked', T4, "    if allow != seal.get('admission_allowlist'):", "    if False:"),
    ('M74_t4_w7s1_count_unchecked', T4, "    if len(allow) != C.BUILD_ALLOWLIST_COUNT:", "    if False:"),
    ('M75_t4_w7s1_build_allowlist_unchecked', T4, "        if ballow is not None and allow != ballow:", "        if False:"),
    # ---- seal_common
    ('M76_common_ints_as_strings', SC, "        return strict_json_bytes(text), text, None\n",
     "        return json.loads(text, object_pairs_hook=_pairs, parse_constant=_no_constant, parse_int=str), text, None\n"),
    ('M77_common_utf8_replace', SC, "        text = raw.decode('utf-8')\n", "        text = raw.decode('utf-8', 'replace')\n"),
    ('M78_common_flag_equals_form_missed', SC, "    return any(isinstance(a, str) and a.split('=', 1)[0] == '--covered-later' for a in argv)",
     "    return any(isinstance(a, str) and a == '--covered-later' for a in argv)"),
]


def main():
    OUT.mkdir(parents=True)
    dev = {n: (DEV / n).read_text() for n in SRC + (TEST,)}
    shas = {n: hashlib.sha256((DEV / n).read_bytes()).hexdigest() for n in SRC + (TEST,)}
    ids = [m[0] for m in MUTANTS]
    assert len(ids) == len(set(ids)) and not any('pending' in i.lower() for i in ids)
    made = []
    for mid, target, old, new in MUTANTS:
        d = OUT / mid
        (d / 'tests').mkdir(parents=True)
        for n in SRC + (TEST,):
            s = dev[n]
            if n == target:
                assert s.count(old) == 1, (mid, s.count(old))
                s = s.replace(old, new)
                compile(s, n, 'exec')
            with open(d / n, 'x') as f:
                f.write(s)
        made.append({'id': mid, 'target': target, 'old': old, 'new': new,
                     'mutant_sha256': hashlib.sha256((d / target).read_bytes()).hexdigest()})
    with open(OUT / 'MUTANTS_FINAL_C4V003.json', 'x') as f:
        json.dump({'schema': 'UNT_SEAL_TOOLS_V003_MUTANTS_FINAL_C4V003', 'dev_sha256': shas, 'mutants': made}, f, indent=1)
    print(len(made), 'mutants')


if __name__ == '__main__':
    main()
