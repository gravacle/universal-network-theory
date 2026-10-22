# make_root_script_c3v014.py: Claude3 (0644 follow-up: WIRE r6). Derives ROOT_SEAL_STEPS_c3v014.sh from c3v013 (c1a469e9).
import hashlib, sys
C3, HELPER_SHA = sys.argv[1], sys.argv[2]
src = open(C3 + '/ROOT_SEAL_STEPS_c3v013.sh', 'rb').read()
assert hashlib.sha256(src).hexdigest() == 'c1a469e98c842af37a4c8886459f4f2e2262053ea8848eebdf4a432dc5d641cd'
assert hashlib.sha256(open(C3 + '/tools/seal_steps_c3sa_c3v014.py', 'rb').read()).hexdigest() == HELPER_SHA
s = src.decode('utf-8')
SEL_OLD = '--selected "$R6_SELECTED" --selected-sha "$R6_SELECTED_SHA"'
SEL_NEW = '--selected "$R6_SELECTED" --selected-sha "$R6_SELECTED_SHA" --selected-schema "$R6_SELECTED_SCHEMA" --tor-role "$R6_TOR_ROLE"'
assert s.count(SEL_OLD) == 3, s.count(SEL_OLD)
s = s.replace(SEL_OLD, SEL_NEW)
R = [
 ('# ROOT_SEAL_STEPS_c3v013.sh: the V007 seal assembly in the order of record, for ROOT (Claude2) ONLY. Built by Claude3 (dispatch 0626;\n',
  '# ROOT_SEAL_STEPS_c3v014.sh: the V007 seal assembly in the order of record, for ROOT (Claude2) ONLY. Built by Claude3 (dispatch 0626;\n'),
 ('# c3v013 supersedes ROOT_SEAL_STEPS_c3v012.sh', '''# c3v014 supersedes ROOT_SEAL_STEPS_c3v013.sh (c1a469e9): prereg r6 is WIRED from Claude4's SELECTED_R6_C4V001.json (7200acd9, 00:16Z):
#   PREREG_TOR = its files.text_of_record (d28c95f5), checked role-qualified (helper c3v014); step 0 also checks its roles
#   addendum_at_text_of_record (= the derived TABLE_BYTES, c01b3c51), case_block (76309ae3; r6 binds the same), impl_of_record_r13
#   (274f7049, C-08's IMPL of record per its erratum E_R6_1) and closed_v005_live (c01b3c51). The summary carries E_R6_1's exact
#   text (read from the pinned SELECTED file) for the seal record. Seal tools v003 are still NOT SELECTED: step 0 still refuses (P1).
# c3v013 superseded ROOT_SEAL_STEPS_c3v012.sh'''),
 ('''# |P11| text of record = prereg r6   | C-02 (A106.2): PREREG_TOR must be the r6 that R6_SELECTED stores (path + sha,  | successor: r6 path and |
# |   | (A106.1; 0643 B and C)       | from bytes). NOT PUBLISHED: PREREG_TOR and R6_SELECTED are PENDING (r5 stands  | sha and its SELECTED   |
# |   |                              | in only in the dry run). One pin, used by steps 0, 2, 4, 4a and 10.            | file (two lines)       |
''', '''# |P11| text of record = prereg r6   | DONE: wired from Claude4's SELECTED_R6_C4V001.json (7200acd9; files.text_of_   | done (c3v014)          |
# |   | (A106.1; 0643 B and C)       | record d28c95f5); its addendum copy, case block, IMPL of record (E_R6_1) and   |                        |
# |   |                              | the closed V005 are checked by role in step 0. One pin for steps 0 to 10.      |                        |
'''),
 ('# the r13 IMPL) is a ROOT MANUAL CHECK: README_SEAL_ASSEMBLY_C3_c3v005.md gives the exact instructions, and the seal record says so.\n',
  '# the r13 IMPL of record COMPARE_V007_IMPL_R13.md 274f7049, erratum E_R6_1) is a ROOT MANUAL CHECK: README_SEAL_ASSEMBLY_C3_c3v006.md\n'
  '# gives the exact instructions, and the seal record says so and states E_R6_1.\n'),
 ('''# P11 / C-02 (A106.2): THE text of record = prereg r6 as Claude4's r6 SELECTED file stores it (path + sha, verified from bytes in step 0);
# one pin for steps 0, 2, 4, 4a and 10. NOT PUBLISHED at build: PENDING (step 0 refuses). A successor sets these two lines from it.
PREREG_TOR="PENDING_R6_TEXT_OF_RECORD"; PREREG_TOR_SHA="PENDING_R6_TEXT_OF_RECORD_SHA"
R6_SELECTED="PENDING_R6_SELECTED_FILE"; R6_SELECTED_SHA="PENDING_R6_SELECTED_FILE_SHA"
''', '''# P11 / C-02 (A106.2): THE text of record = prereg r6 exactly as Claude4's SELECTED_R6_C4V001.json (00:16Z) stores it in its role
# files.text_of_record (role-qualified, verified from bytes in step 0); one pin for steps 0, 2, 4, 4a and 10.
PREREG_TOR="$A/v007_final_prereg_c4/r6/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json"; PREREG_TOR_SHA="d28c95f56321f566b444c3e0bfbbe0ecdac564cbc03a8583ecd5f8d0ae40c0a9"
R6_SELECTED="$A/v007_final_prereg_c4/r6/SELECTED_R6_C4V001.json"; R6_SELECTED_SHA="7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0"
R6_SELECTED_SCHEMA="UNT_V007_SELECTED_PREREG_C4V001"; R6_TOR_ROLE="text_of_record"
# also stored by the r6 SELECTED file and checked by role in step 0 (case_block; impl_of_record_r13 = C-08's IMPL of record, erratum E_R6_1)
CASE_BLOCK="$A/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json"; CASE_BLOCK_SHA="76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71"
IMPL_R13="$A/v007_compare_c2/r13/COMPARE_V007_IMPL_R13.md";  IMPL_R13_SHA="274f7049ece71339d39395b434e7e08bfab33067e3e600d17b4a3bde43fb74a3"
'''),
 ('''  echo "  text of record $PREREG_TOR $PREREG_TOR_SHA; its table bytes $TABLE_BYTES $TABLE_BYTES_SHA"
''', '''  echo "  text of record $PREREG_TOR $PREREG_TOR_SHA; its table bytes $TABLE_BYTES $TABLE_BYTES_SHA"
  # the r6 SELECTED file also stores the table bytes, the case block, C-08's IMPL of record (E_R6_1) and the closed V005: each must be
  # exactly its files.<role> (pinned from bytes); and r6 itself must bind that case block
  H selected-roles --selected "$R6_SELECTED" --selected-sha "$R6_SELECTED_SHA" --schema "$R6_SELECTED_SCHEMA" \\
        --role-pin "addendum_at_text_of_record=$TABLE_BYTES=$TABLE_BYTES_SHA" --role-pin "case_block=$CASE_BLOCK=$CASE_BLOCK_SHA" \\
        --role-pin "impl_of_record_r13=$IMPL_R13=$IMPL_R13_SHA" --role-pin "closed_v005_live=$OPEN_V005=$V005_FINAL_SHA"
  [ "$(jf "$PREREG_TOR" binding_inputs.case_block.path)" = "$CASE_BLOCK" ] && [ "$(jf "$PREREG_TOR" binding_inputs.case_block.sha256)" = "$CASE_BLOCK_SHA" ] \\
    || { echo "REFUSE: the text of record does not bind the case block its SELECTED file stores" >&2; false; }
'''),
 ('''                "C-08 is a ROOT MANUAL CHECK (A106.2): every NEW-item id of the NEW-item list is found in r13 as README_SEAL_ASSEMBLY_C3_c3v005.md instructs; the seal record says root checked it by hand",
''', '''                "C-08 is a ROOT MANUAL CHECK (A106.2) against the IMPL of record r13 COMPARE_V007_IMPL_R13.md 274f7049 (erratum E_R6_1: r13 declares no NEW item; its delta evidence of record is A102 V01-V07 as MUST_FAIL tests), as README_SEAL_ASSEMBLY_C3_c3v006.md instructs; the seal record says root checked it by hand",
                "the seal record states erratum E_R6_1 exactly as the r6 SELECTED file gives it (pins.erratum_E_R6_1_for_the_seal_record)",
'''),
 ('''    output_root "$OUTPUT_ROOT_TO_CREATE st_dev=$OR_DEV st_ino=$OR_INO free_gib_at_creation=$OR_FREE"
''', '''    output_root "$OUTPUT_ROOT_TO_CREATE st_dev=$OR_DEV st_ino=$OR_INO free_gib_at_creation=$OR_FREE" \\
    text_of_record "$PREREG_TOR $PREREG_TOR_SHA (SELECTED_R6_C4V001 $R6_SELECTED_SHA)" \\
    erratum_E_R6_1_for_the_seal_record "$(jf "$R6_SELECTED" basis.erratum_E_R6_1)"
'''),
 ('HELPER="$C3/tools/seal_steps_c3sa_c3v013.py";          HELPER_SHA="ad581a06854ad5ce0e337624860cdf07c04181fccb066f71e79128f1d9b05200"',
  'HELPER="$C3/tools/seal_steps_c3sa_c3v014.py";          HELPER_SHA="%s"' % HELPER_SHA),
]
for o, n in R:
    assert s.count(o) == 1, (o[:90], s.count(o))
    s = s.replace(o, n)
assert 'PENDING_R6' not in s
out = s.encode('utf-8')
with open(C3 + '/ROOT_SEAL_STEPS_c3v014.sh', 'xb') as f:
    f.write(out)
print('ROOT_SEAL_STEPS_c3v014.sh', hashlib.sha256(out).hexdigest(), len(out))
