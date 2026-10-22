# make_root_script_c3v011.py: Claude3 (FROM_CODEX/0643, A106). Derives ROOT_SEAL_STEPS_c3v011.sh from c3v010 (2b9d02fa) by exact
# replacements (each old string occurs exactly once).
import hashlib, sys
C3, HELPER_SHA = sys.argv[1], sys.argv[2]
src = open(C3 + '/ROOT_SEAL_STEPS_c3v010.sh', 'rb').read()
assert hashlib.sha256(src).hexdigest() == '2b9d02fa34b06c4c672c58617a9e93e5bacca26924405106e462d2af397cecef'
assert hashlib.sha256(open(C3 + '/tools/seal_steps_c3sa_c3v012.py', 'rb').read()).hexdigest() == HELPER_SHA
s = src.decode('utf-8')
C02 = '''  # C-02 (A106.2): the text of record is r6 as its SELECTED file stores it, unsealed; the sealed prereg is exactly it plus the slot values
  run_h STEP_%s_C02 check-tor --text-of-record "$PREREG_TOR" --tor-sha "$PREREG_TOR_SHA" --selected "$R6_SELECTED" --selected-sha "$R6_SELECTED_SHA" \\
        --sealed-prereg "$SEALED_PREREG" --sealed-prereg-sha "$SP_SHA" --slots "$SLOTS_FINAL" --slots-sha "$SLOTS_SHA"
'''
R = [
 ('''# ROOT_SEAL_STEPS_c3v010.sh: the V007 seal assembly in the order of record, for ROOT (Claude2) ONLY. Built by Claude3 (dispatch 0626;
# fix round FROM_CODEX/0639 + 0640; FROM_CODEX/0642, ruling A105).
''', '''# ROOT_SEAL_STEPS_c3v011.sh: the V007 seal assembly in the order of record, for ROOT (Claude2) ONLY. Built by Claude3 (dispatch 0626;
# fix round FROM_CODEX/0639 + 0640; FROM_CODEX/0642, ruling A105; FROM_CODEX/0643, ruling A106).
# c3v011 supersedes ROOT_SEAL_STEPS_c3v010.sh (2b9d02fa; FROM_CODEX/0643, A106; helper c3v012):
#   A (A106.3): the V005 addendum is FINAL: V005_FINAL_SHA c01b3c51 / V005_FINAL_BYTES 143081 are pinned constants (no root freeze
#     input). Step 1 verifies the open bytes' sha AND length BEFORE copying, creates the copy exclusively and re-hashes it; the same
#     sha is the frozen_addendum slot sha and the frozen sha the dispositions JSON's frozen_addendum_sha256 must equal.
#   C-02: PREREG_TOR must be prereg r6 as Claude4's r6 SELECTED file stores it (step 0), an UNSEALED text; at steps 4a and 10 the
#     sealed prereg must be a different file, byte-equal to it plus the slot values. r6 is NOT PUBLISHED: PENDING, step 0 refuses.
#   C-04 (step 3b): every slot record through r13's own load_producer_registry against V009 (r13 read once, fenced); every slot
#     must PASS. Finding: V009 registers neither EPS_NGC nor I1T_NGC, so the current draft refuses here (P12, root ruling).
#   C-05 + C-06 (step 3, after the binder): launcher and guard by EXACT BUILD_V007 name and sha; the WHOLE bound command is
#     byte-equal to the binder's output. C-03 (step 8): the GATES_ONLY body evaluated the slotted gate records. C-08: ROOT MANUAL CHECK.
#   0643 C: the seal tools must be exactly what Claude4's v003 SELECTED file names (step 0); v003 is NOT PUBLISHED: PENDING, refuses.
'''),
 ('''# | P1| seal tools v003 (Claude4;    | NOT LANDED: T1..T4 below are v001 PLACEHOLDERS (v001 tools 3/4 are pinned to   | successor script pins  |
# |   | 0633/0634: v002 + D-05 + B8) | prereg r4 e3b6b5b2 and miss ddo_gas_M_s, D-01: they REFUSE r5); the v003 flag  | v003 paths, shas and   |
# |   |                              | (v001 cannot take the dispositions file; the v003 dev CLI takes --dispositions) | and the v003 CLI       |
''', '''# | P1| seal tools v003 (Claude4;    | NOT PUBLISHED: T1..T4 below are v001 PLACEHOLDERS (v001 tools 3/4 are pinned  | successor: v003 paths, |
# |   | A106.2: D-05/C-01, B8, the   | to prereg r4 e3b6b5b2 and miss ddo_gas_M_s: they REFUSE r5); V003_SELECTED is  | shas and CLI from its  |
# |   | README fix, the W7-S1 cases) | PENDING (0643 C: the tool paths and shas must be named by its SELECTED file)   | SELECTED file          |
'''),
 ('''# |P11| text of record (Claude4 0109)| r5 now: PREREG_TOR, ONE line (path + sha) used by steps 0, 2, 4, 4a and 10;    | a successor changes    |
# |   |                              | its table bytes derive from it. r6 expected (Claude4 0109 F-01: r5's text is   | that one line          |
# |   |                              | stale after A102-A105).                                                        |                        |
# Claude4 0109 section 2, C-02..C-06: possible script-encoded checks pending root's ruling on 0109 section 2 (NOT implemented here;
# listed in README_SEAL_ASSEMBLY_C3_c3v003.md).
''', '''# |P11| text of record = prereg r6   | C-02 (A106.2): PREREG_TOR must be the r6 that R6_SELECTED stores (path + sha,  | successor: r6 path and |
# |   | (A106.1; 0643 B and C)       | from bytes). NOT PUBLISHED: PREREG_TOR and R6_SELECTED are PENDING (r5 stands  | sha and its SELECTED   |
# |   |                              | in only in the dry run). One pin, used by steps 0, 2, 4, 4a and 10.            | file (two lines)       |
# |P12| C-04 scope for EPS_NGC and   | V009 registers neither EPS_NGC (1d5eef1b: gate EPS, producer eps_ngc91_        | root ruling            |
# |   | I1T_NGC (0643 finding)       | assemble 04bba30b) nor I1T_NGC (3ae7981a: I1T_NGC is no registry gate). Strict | (PENDING_ROOT_RULING)  |
# |   |                              | C-04 ('every slot must PASS') refuses the current draft at step 3b.            |                        |
# A106.2 (option (b)): C-02, C-03, C-04, C-05 and C-06 are encoded here (steps 0, 3, 3b, 4a, 8 and 10). C-08 (NEW-item ids against
# the r13 IMPL) is a ROOT MANUAL CHECK: README_SEAL_ASSEMBLY_C3_c3v004.md gives the exact instructions, and the seal record says so.
'''),
 ('#   UNT_SEAL_FREEZE_V005_SHA256           the open V005 sha root has read and freezes (step 1 refuses any other bytes)\n',
  '#   (no freeze-sha input: A106 fixes the FINAL V005 bytes, V005_FINAL_SHA and V005_FINAL_BYTES below; step 1 refuses other bytes)\n'),
 ('''# P11: THE text of record, ONE pin (path + sha) for steps 0, 2, 4, 4a and 10. r5 now; r6 expected (Claude4 0109): change this line only.
PREREG_TOR="$A/v007_final_prereg_c4/r5/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json"; PREREG_TOR_SHA="3245899f68081a48928a7242a1d9f1ee3694bb13b3f04913dcb2825104a93393"
''', '''# P11 / C-02 (A106.2): THE text of record = prereg r6 as Claude4's r6 SELECTED file stores it (path + sha, verified from bytes in step 0);
# one pin for steps 0, 2, 4, 4a and 10. NOT PUBLISHED at build: PENDING (step 0 refuses). A successor sets these two lines from it.
PREREG_TOR="PENDING_R6_TEXT_OF_RECORD"; PREREG_TOR_SHA="PENDING_R6_TEXT_OF_RECORD_SHA"
R6_SELECTED="PENDING_R6_SELECTED_FILE"; R6_SELECTED_SHA="PENDING_R6_SELECTED_FILE_SHA"
'''),
 ('OPEN_V005="$CTRL/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md"\n',
  'OPEN_V005="$CTRL/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md"\n'
  'V005_FINAL_SHA="c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1"; V005_FINAL_BYTES=143081   # A106.3 / 0643 A: FINAL (A106 is its last entry)\n'),
 ('SEAL_TOOLS_STATUS="PENDING_V003__V001_PLACEHOLDERS"\n',
  'SEAL_TOOLS_STATUS="PENDING_V003__V001_PLACEHOLDERS"\n'
  'V003_SELECTED="PENDING_V003_SELECTED_FILE"; V003_SELECTED_SHA="PENDING_V003_SELECTED_FILE_SHA"   # 0643 C: it must name every T_* path and sha\n'),
 ('# RI-36 admissible candidates (path|sha)\n',
  'COMPARE_R13_SHA="f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157"   # A104: the compare of record; C-04 loads its load_producer_registry\n'
  '# RI-36 admissible candidates (path|sha)\n'),
 ('''  case "$SEAL_TOOLS_STATUS $PY $A $CTRL $PKT $HELPER $DRAFT $FROZEN $SEAL_DIR $BOUND_PLAN $BOUND_COMMAND $CONFIG" in
    *PENDING*) echo "REFUSE: a PINS value is still PENDING (P1: seal tools v002 not pinned)" >&2; false;; esac
''', '''  case "$SEAL_TOOLS_STATUS $V003_SELECTED $V003_SELECTED_SHA $PREREG_TOR $PREREG_TOR_SHA $R6_SELECTED $R6_SELECTED_SHA $PY $A $CTRL $PKT $HELPER $DRAFT $FROZEN $SEAL_DIR $BOUND_PLAN $BOUND_COMMAND $CONFIG" in
    *PENDING*) echo "REFUSE: a PINS value is still PENDING (P1: seal tools v003 and its SELECTED file; P11: prereg r6 and its SELECTED file)" >&2; false;; esac
'''),
 ('  need UNT_SEAL_FREEZE_V005_SHA256 UNT_SEAL_DISPOSITIONS_PATH ', '  need UNT_SEAL_DISPOSITIONS_PATH '),
 ('''  case " $COMPARE_SUPERSEDED_SHAS " in *" $UNT_SEAL_COMPARE_REVIEWED_SHA256 "*) echo "REFUSE: the compare source is a superseded round (A102)" >&2; false;; esac
''', '''  case " $COMPARE_SUPERSEDED_SHAS " in *" $UNT_SEAL_COMPARE_REVIEWED_SHA256 "*) echo "REFUSE: the compare source is a superseded round (A102)" >&2; false;; esac
  [ "$UNT_SEAL_COMPARE_REVIEWED_SHA256" = "$COMPARE_R13_SHA" ] || { echo "REFUSE: the reviewed compare must be r13 f5adfd11 (A104; C-04 uses its loader)" >&2; false; }
'''),
 ('''  # P11: the ONE text-of-record pin first; the bytes its entry table was read from are derived from it
  H pin --pin "$PREREG_TOR=$PREREG_TOR_SHA"
  tor_table_bytes
  echo "  text of record $PREREG_TOR $PREREG_TOR_SHA; its table bytes $TABLE_BYTES $TABLE_BYTES_SHA"
''', '''  # P11 / C-02 (A106.2): the ONE text-of-record pin is exactly what the r6 SELECTED file stores, and it is an UNSEALED text; the bytes
  # its entry table was read from are derived from it
  H check-tor --text-of-record "$PREREG_TOR" --tor-sha "$PREREG_TOR_SHA" --selected "$R6_SELECTED" --selected-sha "$R6_SELECTED_SHA"
  tor_table_bytes
  echo "  text of record $PREREG_TOR $PREREG_TOR_SHA; its table bytes $TABLE_BYTES $TABLE_BYTES_SHA"
  # 0643 C: the seal tools are exactly what Claude4's v003 SELECTED file names (paths and shas, from bytes)
  H selected-names --selected "$V003_SELECTED" --selected-sha "$V003_SELECTED_SHA" $(printf -- '--pin %s ' "${TOOL_PINS[@]}")
'''),
 ('--pin "$OPEN_V005=$UNT_SEAL_FREEZE_V005_SHA256"', '--pin "$OPEN_V005=$V005_FINAL_SHA"'),
 ('  STEP=1; echo "STEP 1 freeze the V005 addendum (', '  STEP=1; echo "STEP 1 freeze the FINAL V005 addendum c01b3c51, 143081 bytes (A106.3; 0643 A; '),
 ('    H pin --pin "$FROZEN=$UNT_SEAL_FREEZE_V005_SHA256" 2> "$LOGS/STEP_01_FROZEN_REUSED.json"; FROZEN_SHA="$UNT_SEAL_FREEZE_V005_SHA256"\n',
  '    H pin --pin "$FROZEN=$V005_FINAL_SHA" 2> "$LOGS/STEP_01_FROZEN_REUSED.json"; FROZEN_SHA="$V005_FINAL_SHA"\n'),
 ('''    run_h STEP_01_FREEZE freeze --open "$OPEN_V005" --open-sha "$UNT_SEAL_FREEZE_V005_SHA256" --out "$FROZEN"
    FROZEN_SHA="$(jf "$LOGS/STEP_01_FREEZE.json" frozen.sha256)"
  fi
''', '''    run_h STEP_01_FREEZE freeze --open "$OPEN_V005" --open-sha "$V005_FINAL_SHA" --open-bytes "$V005_FINAL_BYTES" --out "$FROZEN"
    FROZEN_SHA="$(jf "$LOGS/STEP_01_FREEZE.json" frozen.sha256)"
  fi
  [ "$FROZEN_SHA" = "$V005_FINAL_SHA" ] || { echo "REFUSE: the FROZEN copy is not the final V005 bytes (A106.3)" >&2; false; }
'''),
 ('  echo "  PASS  STEP_03_BINDER.json"\n', '''  echo "  PASS  STEP_03_BINDER.json"
  # C-05 + C-06 (A106.2): the launcher and guard by EXACT BUILD_V007 name and sha; the WHOLE bound command = the binder's output
  run_h STEP_03_C05_C06 bound-check --build "$BUILD" --build-sha "$BUILD_SHA" --plan "$BOUND_PLAN" --plan-sha "$BP_SHA" \\
        --command "$BOUND_COMMAND" --command-sha "$BC_SHA" --binder "$BINDER" --binder-sha "$BINDER_SHA" --launcher "$LAUNCHER" \\
        --launcher-sha "$LAUNCHER_SHA" --guard "$GUARD" --guard-sha "$GUARD_SHA"
'''),
 ('--runtime "FROZEN_ADDENDUM=$FROZEN=$FROZEN_SHA"', '--runtime "FROZEN_ADDENDUM=$FROZEN=$V005_FINAL_SHA"'),
 ('step4_sealed_prereg() {\n', '''step3b_c04() {
  STEP=3b; echo "STEP 3b C-04 (A106.2): every slot record through r13's own load_producer_registry against registry V009; every slot must PASS"
  v005_still_frozen 3b
  run_h STEP_03B_C04 slot-registry --compare "$UNT_SEAL_COMPARE_REVIEWED_PATH" --compare-sha "$UNT_SEAL_COMPARE_REVIEWED_SHA256" \\
        --registry "$REGISTRY" --registry-sha "$REGISTRY_SHA" --slots "$SLOTS_FINAL" --slots-sha "$SLOTS_SHA" --fence "$FENCE" --fence-sha "$FENCE_SHA"
}

step4_sealed_prereg() {
'''),
 ('  "${T3_RUN[@]}" --slots "$SLOTS_FINAL" --prereg "$SEALED_PREREG" --text-of-record "$PREREG_TOR" --frozen "$FROZEN" \\\n',
  C02 % '04A' + '  "${T3_RUN[@]}" --slots "$SLOTS_FINAL" --prereg "$SEALED_PREREG" --text-of-record "$PREREG_TOR" --frozen "$FROZEN" \\\n'),
 ('  GS_SHA="$(jf "$LOGS/STEP_08_ROW_SCAN.json" e_seal1.sha256)"\n', '''  GS_SHA="$(jf "$LOGS/STEP_08_ROW_SCAN.json" e_seal1.sha256)"
  # C-03 (B6 provenance; A106.2): the sealed-mode GATES_ONLY body evaluated the slotted gate records (record sha equal, status PASS)
  local gj gjs; gj="$(jf "$LOGS/STEP_08_GATES_ONLY.json" gates_only_json.path)"; gjs="$(jf "$LOGS/STEP_08_GATES_ONLY.json" gates_only_json.sha256)"
  run_h STEP_08_C03 gates-provenance --gates-json "$gj" --gates-json-sha "$gjs" --slots "$SLOTS_FINAL" --slots-sha "$SLOTS_SHA"
'''),
 ('  "${T4_RUN[@]}" --slots "$SLOTS_FINAL" --prereg "$SEALED_PREREG" --text-of-record "$PREREG_TOR" --frozen "$FROZEN" \\\n',
  C02 % '10' + '  "${T4_RUN[@]}" --slots "$SLOTS_FINAL" --prereg "$SEALED_PREREG" --text-of-record "$PREREG_TOR" --frozen "$FROZEN" \\\n'),
 ('step3a_fill\nstep4_sealed_prereg\n', 'step3a_fill\nstep3b_c04\nstep4_sealed_prereg\n'),
 ('''                "start step2_disk_watch.sh at the launch (A105.3; a convenience, not part of the seal)",
''', '''                "start step2_disk_watch.sh at the launch (A105.3; a convenience, not part of the seal)",
                "C-08 is a ROOT MANUAL CHECK (A106.2): every NEW-item id of the NEW-item list is found in r13 as README_SEAL_ASSEMBLY_C3_c3v004.md instructs; the seal record says root checked it by hand",
'''),
 ('HELPER="$C3/tools/seal_steps_c3sa_c3v011.py";          HELPER_SHA="7caad125be19160c6e431dcf6be8f038cb9bba172c95f1f8059ebcdd938a0aff"',
  'HELPER="$C3/tools/seal_steps_c3sa_c3v012.py";          HELPER_SHA="%s"' % HELPER_SHA),
]
for o, n in R:
    assert s.count(o) == 1, (o[:90], s.count(o))
    s = s.replace(o, n)
assert 'UNT_SEAL_FREEZE_V005_SHA256' not in s
out = s.encode('utf-8')
with open(C3 + '/ROOT_SEAL_STEPS_c3v011.sh', 'xb') as f:
    f.write(out)
print('ROOT_SEAL_STEPS_c3v011.sh', hashlib.sha256(out).hexdigest(), len(out))
