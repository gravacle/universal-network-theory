# Claude3 seal-assembly builder (FROM_CODEX/0646 + 0647, rulings A110 and A111): derive ROOT_SEAL_STEPS_c3v017.sh from
# ROOT_SEAL_STEPS_c3v016.sh (dcdb746c) by an explicit replacement set; each old string must occur exactly once (the two global
# DRIVER_CHECK_RECORD renames state their counts). Writes the new script exclusively and prints its sha.
# usage: python3 -I -B make_root_script_c3v017.py SEAL_ASSEMBLY_C3_DIR
import hashlib, sys
C3 = sys.argv[1]
src = open(C3 + '/ROOT_SEAL_STEPS_c3v016.sh', 'rb').read()
assert hashlib.sha256(src).hexdigest() == 'dcdb746c76546169bc0b4702c832265b59115c552480f248bdd5c3f354f0a6e8'
s = src.decode('utf-8')
R = []
R.append(('header', '''# ROOT_SEAL_STEPS_c3v016.sh: the V007 seal assembly in the order of record, for ROOT (Claude2) ONLY. Built by Claude3 (dispatch 0626;
# fix round FROM_CODEX/0639 + 0640; FROM_CODEX/0642, ruling A105; FROM_CODEX/0643, ruling A106; FROM_CODEX/0644, ruling A107).
# c3v016 supersedes ROOT_SEAL_STEPS_c3v015.sh (e209ca60;''', '''# ROOT_SEAL_STEPS_c3v017.sh: the V007 seal assembly in the order of record, for ROOT (Claude2) ONLY. Built by Claude3 (dispatch 0626;
# fix round FROM_CODEX/0639 + 0640; FROM_CODEX/0642, ruling A105; FROM_CODEX/0643, ruling A106; FROM_CODEX/0644, ruling A107;
# FROM_CODEX/0646 + 0647, rulings A110 and A111).
# c3v017 supersedes ROOT_SEAL_STEPS_c3v016.sh (dcdb746c, the c3v007 pre-stage tuple). The last seal-path change (A110, A111):
#   A110: root's manual disclosures file root_inputs/SEAL_MANUAL_DISCLOSURES_V001.json (b9db6fd1: E_R6_1's text, the C-08 table and
#     confirmation, root's disclosures) is the pinned constant DISCLOSURES. Step 0 pre-checks it (helper c3v017 check-disclosures: read
#     once, the c3v013 SELECTED-strictness rules, the exact key set, e_r6_1_text non-empty and byte-equal to the r6 SELECTED file's
#     basis.erratum_E_R6_1). Step 10 passes it to tool 4 v004 (--manual-disclosures / --manual-disclosures-sha256), which embeds it
#     verbatim INSIDE the SEAL_RECORD. The separate-packet substitute for E_R6_1 and C-08 is gone (root_next).
#   P13 (NEW): tool 4 v004 and Claude4's seal-tools SELECTED file naming it are NOT PUBLISHED: PENDING, step 0 refuses. Tools 1, 2,
#     3, 5 and seal_common stay v003 (cf7e5b2f, role-qualified); tool 4's role is checked against the v004 SELECTED file.
#   A111: P3 and P4 are RULED. The driver check record is the pinned constant DRIVER_CHECK_RECORD (CHECK.md 89a6de88); EPS_NGC
#     (1d5eef1b) and I1T_NGC (3ae7981a) are plain pins in SLOT_VALUES_DRAFT_c3v003.json, which has no PENDING_ROOT_RULING marker.
#     The inputs UNT_SEAL_DRIVER_CHECK_RECORD_PATH / _SHA256 and UNT_SEAL_RULING_EPS_NGC / _I1T_NGC are gone; step 0 refuses if any of
#     them is still set, and checks that the draft pins exactly the ruled records. Nothing else changes.
# c3v016 superseded ROOT_SEAL_STEPS_c3v015.sh (e209ca60;'''))
R.append(('pending status', '# Status at build (2026-10-18 ~22:50Z). The script REFUSES in step 0 while any item P1-P10 below is unresolved (P11 is a note).',
          '# Status at build (2026-10-19 ~01:40Z). The script REFUSES in step 0 while P13 or any root input (P2, P5-P10) is unresolved.'))
R.append(('pending P3 P4', '''# | P3| driver check record (RI-36)  | CHECK.md 89a6de88 | Codex3 0602 R5_REVIEW_FINAL_V001.md 6758bd24               | env (root ruling)      |
# | P4| EPS_NGC, I1T_NGC (GAP-12)    | EPS_CERT_NGC91_V001 1d5eef1b; I1T_NGC_T120L_V001 3ae7981a (single candidates) | env (root ruling)      |''',
          '''# | P3| driver check record (RI-36)  | RULED A111 (0647): CHECK.md 89a6de88, the pinned constant DRIVER_CHECK_RECORD; | done (c3v017)          |
# |   |                              | the slot draft c3v003 pins the same record (R5_REVIEW_FINAL 6758bd24: not used)|                        |
# | P4| EPS_NGC, I1T_NGC (GAP-12)    | RULED A111 (0647): EPS_CERT_NGC91_V001 1d5eef1b; I1T_NGC_T120L_V001 3ae7981a,  | done (c3v017)          |
# |   |                              | plain pins in SLOT_VALUES_DRAFT_c3v003.json (= the two C04_EXCLUSIONS pins)    |                        |'''))
R.append(('pending P13', '''# |   |                              | must PASS, with its gate's pass verdict. No registry V010.                     |                        |''',
          '''# |   |                              | must PASS, with its gate's pass verdict. No registry V010.                     |                        |
# |P13| tool 4 v004 (A110, 0646;     | PENDING (NOT PUBLISHED): build_seal_record + --manual-disclosures <path>        | Claude4's seal-tools   |
# |   | Claude4)                     | --manual-disclosures-sha256 <hex>, root's disclosures file verbatim in the     | SELECTED file (v004 or |
# |   |                              | SEAL_RECORD. Step 0 REFUSES until V004_SELECTED and T4 are wired from it.      | v003 r2)               |'''))
R.append(('A106.2 C-08 note', '''# the r13 IMPL of record COMPARE_V007_IMPL_R13.md 274f7049, erratum E_R6_1) is a ROOT MANUAL CHECK: README_SEAL_ASSEMBLY_C3_c3v006.md
# gives the exact instructions, and the seal record says so and states E_R6_1.''',
          '''# the r13 IMPL of record COMPARE_V007_IMPL_R13.md 274f7049, erratum E_R6_1) is a ROOT MANUAL CHECK: root has done it and recorded it
# in the disclosures file's c08_table and c08_confirmation (A110; 0647). Tool 4 v004 carries that file, with E_R6_1's text, verbatim
# INSIDE the SEAL_RECORD (step 10); nothing about E_R6_1 or C-08 is published separately.'''))
R.append(('root inputs', '''#   UNT_SEAL_DRIVER_CHECK_RECORD_PATH / _SHA256   RI-36 ruling (one of the two candidates)
#   UNT_SEAL_RULING_EPS_NGC, UNT_SEAL_RULING_I1T_NGC   full sha of the ruled record (must equal the draft's single candidate)
''', '''#   (no driver-check-record or ruling input: A111 rules P3 and P4, so DRIVER_CHECK_RECORD and the slot draft c3v003 fix them; step 0
#   REFUSES if UNT_SEAL_DRIVER_CHECK_RECORD_PATH, UNT_SEAL_DRIVER_CHECK_RECORD_SHA256, UNT_SEAL_RULING_EPS_NGC or
#   UNT_SEAL_RULING_I1T_NGC is still set)
#   (no disclosures input: A110 / 0647 fix root's file, DISCLOSURES below, pinned by sha in step 0)
'''))
R.append(('helper pin', 'HELPER="$C3/tools/seal_steps_c3sa_c3v016.py";          HELPER_SHA="21f0eb09e927722237459d65cf60eae79d92acf4c6a25bb4340f1519e66d28c0"',
          'HELPER="$C3/tools/seal_steps_c3sa_c3v017.py";          HELPER_SHA="3c642d1a8be8bdac12d3472add602065c6d86cc47c7f3d96c297f534056a047b"'))
R.append(('draft pin', 'DRAFT="$C3/SLOT_VALUES_DRAFT_c3v002.json";              DRAFT_SHA="02d97c376ddf231ec9e9643e21b88e57669719e9bb3687c2e8b6f30eec711e7f"   # schema UNT_V007_SEAL_SLOTS_C4V002 (v003)',
          'DRAFT="$C3/SLOT_VALUES_DRAFT_c3v003.json";              DRAFT_SHA="e12292a27e58aacdebfde5dfc4d1a3f7ccb0c5b3ca4b756ef2a6d8468a5311c5"   # schema UNT_V007_SEAL_SLOTS_C4V002 (v003); P3, P4 ruled (A111)'))
R.append(('disclosures pin', 'IMPL_R13="$A/v007_compare_c2/r13/COMPARE_V007_IMPL_R13.md";  IMPL_R13_SHA="274f7049ece71339d39395b434e7e08bfab33067e3e600d17b4a3bde43fb74a3"\n',
          '''IMPL_R13="$A/v007_compare_c2/r13/COMPARE_V007_IMPL_R13.md";  IMPL_R13_SHA="274f7049ece71339d39395b434e7e08bfab33067e3e600d17b4a3bde43fb74a3"
# A110 (0646, 0647): root's manual disclosures (E_R6_1's text, the C-08 table and confirmation, root's disclosures), carried verbatim
# INSIDE the SEAL_RECORD by tool 4 v004 (step 10); step 0 pins and pre-checks them (helper check-disclosures)
DISCLOSURES="$C3/root_inputs/SEAL_MANUAL_DISCLOSURES_V001.json"; DISCLOSURES_SHA="b9db6fd1716be1e2fb47b6daf9b1e6e81743d6544f9ec72b589cf50fe0fa4ab6"
'''))
R.append(('tool 4 v004 PENDING', 'T4="$TD/build_seal_record_c4v003.py";          T4_SHA="de0ceb15ebfb95e04227730bd2785eb46af8cb5980012de91de98f34ea226b96"\n',
          '''# P13 (A110): tool 4 is v004 (build_seal_record + --manual-disclosures), as Claude4's seal-tools SELECTED file (v004 or v003 r2) names
# it: PENDING, NOT PUBLISHED, so step 0 refuses. v003's tool 4 (de0ceb15) is no longer the seal's tool 4.
V004_SELECTED="PENDING_SEAL_TOOLS_V004_SELECTED_FILE (Claude4, A110)"; V004_SELECTED_SHA="PENDING"; V004_SELECTED_SCHEMA="PENDING"
T4="PENDING_TOOL4_V004 (Claude4, A110)";        T4_SHA="PENDING"
'''))
R.append(('driver check record constant', '''# RI-36 admissible candidates (path|sha)
DRIVER_CHECK_CANDIDATES="$A/tail_scheme_impl_c2/driver_r5/check/CHECK.md|89a6de88739e1c4b76c39dc11d7417d7e243b7235511d8ea0951e1493865b632
$A/review_r5_certs_cx3/R5_REVIEW_FINAL_V001.md|6758bd24784ec514d73054a30a8fdd673c3d0c571521a62514ba4260f3ad7ba9"
''', '''# P3 RULED (A111, 0647): the driver check record of record (RI-36); the slot draft c3v003 pins the same path and sha
DRIVER_CHECK_RECORD="$A/tail_scheme_impl_c2/driver_r5/check/CHECK.md"; DRIVER_CHECK_RECORD_SHA="89a6de88739e1c4b76c39dc11d7417d7e243b7235511d8ea0951e1493865b632"
'''))
R.append(('step 0 PENDING', '''  case "$SEAL_TOOLS_STATUS $V003_SELECTED $V003_SELECTED_SHA $PREREG_TOR $PREREG_TOR_SHA $R6_SELECTED $R6_SELECTED_SHA $PY $A $CTRL $PKT $HELPER $DRAFT $FROZEN $SEAL_DIR $BOUND_PLAN $BOUND_COMMAND $CONFIG" in
    *PENDING*) echo "REFUSE: a PINS value is still PENDING (P1: seal tools v003 and its SELECTED file; P11: prereg r6 and its SELECTED file)" >&2; false;; esac''',
          '''  case "$SEAL_TOOLS_STATUS $V003_SELECTED $V003_SELECTED_SHA $V004_SELECTED $V004_SELECTED_SHA $V004_SELECTED_SCHEMA $T4 $T4_SHA $DISCLOSURES $DISCLOSURES_SHA $PREREG_TOR $PREREG_TOR_SHA $R6_SELECTED $R6_SELECTED_SHA $PY $A $CTRL $PKT $HELPER $DRAFT $FROZEN $SEAL_DIR $BOUND_PLAN $BOUND_COMMAND $CONFIG" in
    *PENDING*) echo "REFUSE: a PINS value is still PENDING (P13: tool 4 v004 and Claude4's seal-tools SELECTED file naming it, A110)" >&2; false;; esac'''))
R.append(('step 0 need', '''       UNT_SEAL_COMPARE_SELECTION_PATH UNT_SEAL_COMPARE_SELECTION_SHA256 UNT_SEAL_DRIVER_CHECK_RECORD_PATH \\
       UNT_SEAL_DRIVER_CHECK_RECORD_SHA256 UNT_SEAL_RULING_EPS_NGC UNT_SEAL_RULING_I1T_NGC UNT_SEAL_KEY_EQUIVALENCE_MAP_PATH \\
''', '''       UNT_SEAL_COMPARE_SELECTION_PATH UNT_SEAL_COMPARE_SELECTION_SHA256 UNT_SEAL_KEY_EQUIVALENCE_MAP_PATH \\
'''))
R.append(('step 0 stale inputs', '''       UNT_SEAL_C5H_RUN_DIR UNT_SEAL_MIN_FREE_GIB UNT_SEAL_ROOT_ACK
''', '''       UNT_SEAL_C5H_RUN_DIR UNT_SEAL_MIN_FREE_GIB UNT_SEAL_ROOT_ACK
  # A111: P3 and P4 are ruled; the old ruling inputs must not be given (a stale invocation would otherwise look like a choice)
  local v; for v in UNT_SEAL_DRIVER_CHECK_RECORD_PATH UNT_SEAL_DRIVER_CHECK_RECORD_SHA256 UNT_SEAL_RULING_EPS_NGC UNT_SEAL_RULING_I1T_NGC; do
    if [ -n "${!v+x}" ]; then echo "REFUSE: $v is no longer an input (A111 ruled P3 and P4; the slot draft c3v003 fixes them): unset it" >&2; false; fi; done
'''))
R.append(('step 0 RI-36 grep removed', '''  printf '%s\\n' "$DRIVER_CHECK_CANDIDATES" | /usr/bin/grep -qxF "$UNT_SEAL_DRIVER_CHECK_RECORD_PATH|$UNT_SEAL_DRIVER_CHECK_RECORD_SHA256" \\
    || { echo "REFUSE: the driver check record is not an RI-36 candidate (a different record needs a successor draft)" >&2; false; }
''', ''))
R.append(('step 0 disclosures', '''    || { echo "REFUSE: the text of record does not bind the case block its SELECTED file stores" >&2; false; }
''', '''    || { echo "REFUSE: the text of record does not bind the case block its SELECTED file stores" >&2; false; }
  # A110 (0646, 0647): root's manual disclosures, read ONCE from bytes and parsed strictly (the SELECTED-strictness rules): the exact key
  # set, e_r6_1_text non-empty and byte-equal to the r6 SELECTED file's basis.erratum_E_R6_1 (tool 4 v004 embeds the file at step 10)
  H check-disclosures --disclosures "$DISCLOSURES" --disclosures-sha "$DISCLOSURES_SHA" --r6-selected "$R6_SELECTED" \\
        --r6-selected-sha "$R6_SELECTED_SHA" --r6-schema "$R6_SELECTED_SCHEMA"
'''))
R.append(('step 0 v003 roles without tool 4', '''        --role-pin "tool_4_build_seal_record=$T4=$T4_SHA" --role-pin "tool_5_print_driver_build_record=$T5=$T5_SHA" \\
        --role-pin "readme=$V003_README=$V003_README_SHA" --role-pin "selected_r6=$R6_SELECTED=$R6_SELECTED_SHA"
''', '''        --role-pin "tool_5_print_driver_build_record=$T5=$T5_SHA" \\
        --role-pin "readme=$V003_README=$V003_README_SHA" --role-pin "selected_r6=$R6_SELECTED=$R6_SELECTED_SHA"
  # P13 (A110): tool 4 v004 exactly as Claude4's seal-tools SELECTED file names it (role tool_4_build_seal_record)
  H selected-roles --selected "$V004_SELECTED" --selected-sha "$V004_SELECTED_SHA" --schema "$V004_SELECTED_SCHEMA" \\
        --role-pin "tool_4_build_seal_record=$T4=$T4_SHA"
'''))
R.append(('step 0 pins', '''        --pin "$UNT_SEAL_DRIVER_CHECK_RECORD_PATH=$UNT_SEAL_DRIVER_CHECK_RECORD_SHA256" \\
        --pin "$UNT_SEAL_KEY_EQUIVALENCE_MAP_PATH=$UNT_SEAL_KEY_EQUIVALENCE_MAP_SHA256"''',
          '''        --pin "$DRIVER_CHECK_RECORD=$DRIVER_CHECK_RECORD_SHA" --pin "$DISCLOSURES=$DISCLOSURES_SHA" \\
        --pin "$UNT_SEAL_KEY_EQUIVALENCE_MAP_PATH=$UNT_SEAL_KEY_EQUIVALENCE_MAP_SHA256"'''))
R.append(('step 0 draft A111 checks', '''    && [ "$(jf "$DRAFT" identity_gate_records.B0prime_RERUN.sha256)" = "$IDREC_B0P_SHA" ]
''', '''    && [ "$(jf "$DRAFT" identity_gate_records.B0prime_RERUN.sha256)" = "$IDREC_B0P_SHA" ]
  # A111 (P3, P4): the draft pins exactly the ruled records: its driver_check_record is DRIVER_CHECK_RECORD, and its EPS_NGC and I1T_NGC
  # are the two C04_EXCLUSIONS pins (path and sha)
  [ "$(jf "$DRAFT" driver_check_record.path)" = "$DRIVER_CHECK_RECORD" ] && [ "$(jf "$DRAFT" driver_check_record.sha256)" = "$DRIVER_CHECK_RECORD_SHA" ] \\
    || { echo "REFUSE: the slot draft's driver_check_record is not the A111 record" >&2; false; }
  local x; for x in "${C04_EXCLUSIONS[@]}"; do
    [ "$(jf "$DRAFT" "${x%%=*}.path")=$(jf "$DRAFT" "${x%%=*}.sha256")" = "${x#*=}" ] || { echo "REFUSE: the slot draft's ${x%%=*} is not the A111 record" >&2; false; }; done
'''))
R.append(('step 3a echo', 'STEP 3a fill SLOT_VALUES_FINAL from the draft + run-time pins + root rulings (README_SEAL_TOOLS L27 mapping, L33 \'Slot JSON\')',
          'STEP 3a fill SLOT_VALUES_FINAL from the draft (P3, P4 ruled in it, A111) + run-time pins (README_SEAL_TOOLS L27 mapping, L33 \'Slot JSON\')'))
R.append(('step 3a runtime DRIVER_CHECK_RECORD removed', '''        --runtime "DRIVER_CHECK_RECORD=$UNT_SEAL_DRIVER_CHECK_RECORD_PATH=$UNT_SEAL_DRIVER_CHECK_RECORD_SHA256" \\
''', ''))
R.append(('step 3a rulings removed', '''        --expect "CASCADE_MAP_R5_ADDENDUM=$UNT_SEAL_CASCADE_MAP_R5_ADDENDUM_PATH" \\
        --ruling "EPS_NGC=$UNT_SEAL_RULING_EPS_NGC" --ruling "I1T_NGC=$UNT_SEAL_RULING_I1T_NGC"
''', '''        --expect "CASCADE_MAP_R5_ADDENDUM=$UNT_SEAL_CASCADE_MAP_R5_ADDENDUM_PATH"
'''))
R.append(('step 10 echo', 'STEP 10 build_seal_record: record bytes to stdout, sha to stderr (README_SEAL_TOOLS L14, L16-L22; SEAL_CHECKLIST_R5 L30 B7)',
          'STEP 10 build_seal_record v004: record bytes to stdout, sha to stderr; root\'s manual disclosures INSIDE the record (A110; README_SEAL_TOOLS L14, L16-L22; SEAL_CHECKLIST_R5 L30 B7)'))
R.append(('step 10 pin', '''        --pin "$UNT_SEAL_SUCCESSOR_CUSTODY_PATH=$UNT_SEAL_SUCCESSOR_CUSTODY_SHA256" --pin "$UNT_SEAL_DISPOSITIONS_PATH=$UNT_SEAL_DISPOSITIONS_SHA256" \\
        --pin "$RUNNER=$RUNNER_SHA" \\''', '''        --pin "$UNT_SEAL_SUCCESSOR_CUSTODY_PATH=$UNT_SEAL_SUCCESSOR_CUSTODY_SHA256" --pin "$UNT_SEAL_DISPOSITIONS_PATH=$UNT_SEAL_DISPOSITIONS_SHA256" \\
        --pin "$DISCLOSURES=$DISCLOSURES_SHA" --pin "$RUNNER=$RUNNER_SHA" \\'''))
R.append(('step 10 tool 4 v004 disclosures', '''        --successor-custody "$UNT_SEAL_SUCCESSOR_CUSTODY_PATH" --b2-record "$B2_RECORD" > "$T4_STDOUT" 2> "$T4_STDERR"''',
          '''        --successor-custody "$UNT_SEAL_SUCCESSOR_CUSTODY_PATH" --b2-record "$B2_RECORD" \\
        --manual-disclosures "$DISCLOSURES" --manual-disclosures-sha256 "$DISCLOSURES_SHA" > "$T4_STDOUT" 2> "$T4_STDERR"'''))
R.append(('root_next C-08 and E_R6_1', '''                "C-08 is a ROOT MANUAL CHECK (A106.2) against the IMPL of record r13 COMPARE_V007_IMPL_R13.md 274f7049 (erratum E_R6_1: r13 declares no NEW item; its delta evidence of record is A102 V01-V07 as MUST_FAIL tests), as README_SEAL_ASSEMBLY_C3_c3v006.md instructs; the seal record says root checked it by hand",
                "erratum E_R6_1: v003 tool 4 takes no errata input (its argparse has none), so the SEAL_RECORD cannot carry it; root states it, exactly as the r6 SELECTED file gives it (pins.erratum_E_R6_1_for_the_seal_record), in the numbered root packet that publishes the SEAL_RECORD (a manual seal-record statement)",''',
          '''                "C-08 (A106.2, A110): root's manual check against the IMPL of record r13 COMPARE_V007_IMPL_R13.md 274f7049 is recorded in the disclosures file's c08_table and c08_confirmation (SEAL_MANUAL_DISCLOSURES_V001.json b9db6fd1), which tool 4 v004 carried verbatim INSIDE the SEAL_RECORD: nothing to publish separately",
                "erratum E_R6_1 (A110): INSIDE the SEAL_RECORD (the disclosures file's e_r6_1_text, byte-equal to the r6 SELECTED file's basis.erratum_E_R6_1, checked in step 0): no separate statement",'''))
R.append(('summary pins', '''    erratum_E_R6_1_for_the_seal_record "$(jf "$R6_SELECTED" basis.erratum_E_R6_1)"''',
          '''    manual_disclosures "$DISCLOSURES $DISCLOSURES_SHA (verbatim inside the SEAL_RECORD through tool 4 v004; A110)"'''))
out = s
for rid, o, n in R:
    assert out.count(o) == 1, (rid, out.count(o))
    out = out.replace(o, n)
for o, n, k in (('$UNT_SEAL_DRIVER_CHECK_RECORD_PATH', '$DRIVER_CHECK_RECORD', 3), ('$UNT_SEAL_DRIVER_CHECK_RECORD_SHA256', '$DRIVER_CHECK_RECORD_SHA', 2)):
    assert out.count(o) == k, (o, out.count(o))
    out = out.replace(o, n)
assert 'UNT_SEAL_RULING_EPS_NGC=' not in out and 'DRIVER_CHECK_CANDIDATES' not in out and '--ruling' not in out
dst = C3 + '/ROOT_SEAL_STEPS_c3v017.sh'
with open(dst, 'x') as f:
    f.write(out)
print('ROOT_SEAL_STEPS_c3v017.sh', hashlib.sha256(out.encode()).hexdigest(), 'replacements', len(R) + 2)
