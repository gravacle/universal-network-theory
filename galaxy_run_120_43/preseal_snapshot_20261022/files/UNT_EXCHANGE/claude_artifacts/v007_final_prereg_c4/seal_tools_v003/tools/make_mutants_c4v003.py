# Claude4 seal tools v003 (BUILD helper): mutation check of the v003 test suite. For each mutant, copy the six dev/ v003 sources and
# dev/tests/test_seal_tools_c4v003.py into mutants/<id>/ (work copies inside this folder) and apply ONE exact replacement that disables a
# v003 check (the old text must occur exactly once). The suite is then run in each folder (by the caller, under the fence); a mutant is
# KILLED when at least one case is NOT_OK. Writes only under <this folder>/mutants/. No process, no network, no delete.
# usage: python3 -I -B make_mutants_c4v003.py
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
DEV = HERE / 'dev'
OUT = HERE / 'mutants'
SRC = ('seal_common_c4v003.py', 'check_frozen_addendum_c4v003.py', 'check_sealed_compare_c4v003.py', 'check_slot_fill_c4v003.py',
       'build_seal_record_c4v003.py', 'print_driver_build_record_c4v003.py')
T1 = 'check_frozen_addendum_c4v003.py'
T3 = 'check_slot_fill_c4v003.py'
T4 = 'build_seal_record_c4v003.py'
SC = 'seal_common_c4v003.py'
MUTANTS = [
    ('M01_t1_api_bare_names_allowed', T1, "    if covered_later:\n        chk.fail('COVERED_LATER_BARE_NAMES_REFUSED', C.COVERED_LATER_REMOVED)\n    later = sorted",
     "    if False:\n        chk.fail('COVERED_LATER_BARE_NAMES_REFUSED', C.COVERED_LATER_REMOVED)\n    later = sorted"),
    ('M02_t1_section_sha_unchecked', T1, "        if 'section_sha256' in r and r['section_sha256'] != want:\n",
     "        if False and 'section_sha256' in r and r['section_sha256'] != want:\n"),
    ('M03_t1_change_from_unchecked', T1, "            if ch['from_section_sha256'] != changed[n]['row_section_sha256']:\n", "            if False:\n"),
    ('M04_t1_file_never_required', T1, "        if need_d:\n            chk.fail('DISPOSITIONS_REQUIRED'", "        if False:\n            chk.fail('DISPOSITIONS_REQUIRED'"),
    ('M05_t1_any_disposition_value', T1, "        if 'disposition' in r and r['disposition'] not in DISPOSITION_VALUES:\n", "        if False:\n"),
    ('M06_t1_tabled_row_allowed', T1, "            if n in table:\n                chk.fail('DISPOSITION_FOR_TABLED_ENTRY'",
     "            if False:\n                chk.fail('DISPOSITION_FOR_TABLED_ENTRY'"),
    ('M07_t1_pin_sha_unchecked', T1, "    if got != h:\n        chk.fail('DISPOSITIONS_PIN_MISMATCH'", "    if False:\n        chk.fail('DISPOSITIONS_PIN_MISMATCH'"),
    ('M08_common_ints_as_strings', SC, "        return strict_json_bytes(text), text, None\n",
     "        return json.loads(text, object_pairs_hook=_pairs, parse_constant=_no_constant, parse_int=str), text, None\n"),
    ('M09_t4_no_reread', T4, "    p, h = disp\n    vp = verified['pin']\n", "    return dict(verified)\n    p, h = disp\n    vp = verified['pin']\n"),
    ('M10_t4_b8_sealed_by_unchecked', T4, "    if seal.get('sealed_by') != C.AUTHORITY:", "    if False:"),
    ('M11_t4_b8_pins_unchecked', T4, "        if sub.pin('seal.' + key, seal[key]):", "        if True or sub.pin('seal.' + key, seal[key]):"),
    ('M12_t3_pin_not_passed_to_t1', T3, "        r1 = T1.run(prereg_path, frozen, fa.get('sha256'), covered_later, False, dispositions)",
     "        r1 = T1.run(prereg_path, frozen, fa.get('sha256'), covered_later, False, None)"),
    ('M13_t4_api_bare_names_unchecked', T4, "    if cov:                                                                     # v003 D-05\n", "    if False:\n"),
    ('M14_t1_cli_flag_unchecked', T1, "    if C.covered_later_flag(argv):                       # v003 D-05: the removed flag is a typed refusal, not a usage error\n"
     "        return C.emit(C.covered_later_refusal('check_frozen_addendum_c4v003'))\n", ''),
    ('M15_t1_later_row_change_allowed', T1, "            if 'change' in r:\n                chk.fail('DISPOSITION_CHANGE_NOT_ALLOWED'",
     "            if False:\n                chk.fail('DISPOSITION_CHANGE_NOT_ALLOWED'"),
    ('M16_t1_frozen_sha_unchecked', T1, "    if 'frozen_addendum_sha256' in obj and obj['frozen_addendum_sha256'] != fsha:", "    if False:"),
    ('M17_t1_reason_unchecked', T1, "        if 'reason' in r and not (isinstance(r['reason'], str) and r['reason'].strip()):", "        if False:"),
    ('M18_t1_duplicate_rows_allowed', T1, "        if n in seen:\n            chk.fail('DISPOSITION_DUPLICATE_ENTRY'", "        if False:\n            chk.fail('DISPOSITION_DUPLICATE_ENTRY'"),
    ('M19_t1_row_keys_unchecked', T1, "        if not (DISPOSITION_ROW_KEYS <= keys <= DISPOSITION_ROW_KEYS | {'change'}):", "        if False:"),
    ('M20_t3_cli_flag_unchecked', T3, "    if C.covered_later_flag(argv):                       # v003 D-05: the removed flag is a typed refusal, not a usage error\n"
     "        return C.emit(C.covered_later_refusal('check_slot_fill_c4v003'))\n", ''),
    ('M21_t4_cli_flag_unchecked', T4, "    if C.covered_later_flag(argv):                       # v003 D-05: the removed flag is a typed refusal (stderr; stdout stays empty)\n"
     "        print(json.dumps(C.covered_later_refusal('build_seal_record_c4v003'), indent=1, sort_keys=True), file=sys.stderr)\n        return 2\n", ''),
    ('M22_t4_b8_missing_key_unchecked', T4, "        if key not in seal:                                                     # guard v008 L39 SEALED_<KEY>_REQUIRED\n"
     "            chk.fail('ADMISSION_SEAL_%s_REQUIRED' % key.upper(), 'the SEAL_RECORD carries no %s pin (guard v008 L39)' % key)\n            continue\n",
     "        if key not in seal:\n            continue\n"),
    ('M23_t1_change_what_unchecked', T1, "            if not (isinstance(ch['what_changed'], str) and ch['what_changed'].strip()):", "            if False:"),
    ('M24_t1_cited_row_allowed', T1, "            if n <= last:\n                chk.fail('DISPOSITION_FOR_CITED_ENTRY'", "            if False:\n                chk.fail('DISPOSITION_FOR_CITED_ENTRY'"),
]


def main():
    OUT.mkdir(exist_ok=True)
    made = []
    for mid, target, old, new in MUTANTS:
        d = OUT / mid
        (d / 'tests').mkdir(parents=True)
        for n in SRC:
            s = (DEV / n).read_text()
            if n == target:
                assert s.count(old) == 1, (mid, s.count(old))
                s = s.replace(old, new)
                compile(s, n, 'exec')
            with open(d / n, 'x') as f:
                f.write(s)
        with open(d / 'tests' / 'test_seal_tools_c4v003.py', 'x') as f:
            f.write((DEV / 'tests' / 'test_seal_tools_c4v003.py').read_text())
        made.append(mid)
    print('\n'.join(made))


if __name__ == '__main__':
    main()
