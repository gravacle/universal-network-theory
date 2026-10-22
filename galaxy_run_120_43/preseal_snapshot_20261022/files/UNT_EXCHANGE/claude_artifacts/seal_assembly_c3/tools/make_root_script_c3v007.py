# Claude3 (FROM_CODEX/0639 + 0640): derive ROOT_SEAL_STEPS_c3v007.sh from c3v006 by exact, asserted replacements (each occurs once).
import sys, hashlib, re
D = sys.argv[1]
s = open(D + '/ROOT_SEAL_STEPS_c3v006.sh').read()
assert hashlib.sha256(s.encode()).hexdigest() == 'cb3aeb324067910acdd9be5730e70305c819df4327ba00465aeae89249d3ed34'
R = []
R.append(("# ROOT_SEAL_STEPS_c3v006.sh: the V007 seal assembly in the order of record, for ROOT (Claude2) ONLY. Built by Claude3 (dispatch 0626).\n",
"# ROOT_SEAL_STEPS_c3v007.sh: the V007 seal assembly in the order of record, for ROOT (Claude2) ONLY. Built by Claude3 (dispatch 0626;\n"
"# fix round FROM_CODEX/0639 + 0640).\n"
"# c3v007 supersedes ROOT_SEAL_STEPS_c3v006.sh (cb3aeb32):\n"
"#   SA-CX1-B1: helper c3v009 never calls realpath or resolve; every path is a no-follow component walk; a symlink is refused at the link\n"
"#     and its target's metadata is never read.\n"
"#   SA-CX1-B2: every pinned Python program and module is read once, digest-checked and exec'd from that buffer (helper load_pinned for\n"
"#     the fence, the compare and the guard; run_pinned_c3sa_c3v002.py for the seal tools, their sibling modules, the binder and the\n"
"#     step-9 compare); and every Python process runs with -X pycache_prefix=<empty dir>, so no __pycache__ .pyc beside any source is\n"
"#     read, including inside the compare's own importlib load of its pinned V005 compare (r13 L694-L700).\n"
"#   SA-CX1-B3: the dispositions input is only the v003 object; the same pinned file goes to tools 1, 3 and 4; PV-D05-1 is mirrored.\n"
"#   A104 (22:13Z): compare r13 (f5adfd11; SELECTED_R13 10acd098) is the compare of record.\n"
"# TOOL ORDER (README_SEAL_TOOLS of seal tools v002, da29c008, L35-L40: ON DISK, UNPOSTED; v003 has not landed), Claude4's numbers:\n"
"#   tool 1 check_frozen_addendum ...... after B1 -> step 2    tool 5 print_driver_build_record ... B2a -> step 2a (v001 has no tool 5;\n"
"#                                                                                                  the helper builds the same record)\n"
"#   tool 3 check_slot_fill ............ after B4 -> step 4a   tool 2 check_sealed_compare ......... after B5 -> step 5a\n"
"#   tool 4 build_seal_record .......... B7 -> step 10         tool 4 --check-admission-config ..... B8 -> step 12 (v002/v003 only; the\n"
"#                                                                                                  helper's guard self-check stands in)\n"
"#   (0626 listed '6. tool 2, 7. tool 3' after both B4 and B5; this script follows the README order above.)\n"))
R.append(("# |   |                              | for the dispositions JSON is a PLACEHOLDER (T_DISPOSITIONS_FLAG)               | the dispositions flag  |\n",
          "# |   |                              | (v001 cannot take the dispositions file; the v003 dev CLI takes --dispositions) | and the v003 CLI       |\n"))
R.append(("# | P2| compare reviewed source      | r13 FROZEN 21:22Z: kmax_tail_compare_c2v007_r13_cx3v001.py f5adfd11, SELECTED_R13| env (root, invocation) |\n"
          "# |   |                              | 10acd098 (A102); the slot waits for the Claude3 + Codex2 deltas, 0 blocking   |                        |\n",
          "# | P2| compare reviewed source      | A104 (22:13Z): r13 IS the compare of record: kmax_tail_compare_c2v007_r13_cx3v001.py| env (root, invocation) |\n"
          "# |   |                              | f5adfd11, SELECTED_R13 10acd098; both delta reviews of record report 0 blocking|                        |\n"))
R.append(("# | P5| dispositions JSON (0633;     | root writes it at assembly: $CTRL/V007_SEAL_ASSEMBLY_INPUTS/                   | env path + sha (root)  |\n"
          "# |   | RI-34; A81 RI-26)            | COVERED_LATER_DISPOSITIONS_V007.json: {entry, disposition revised|no_change,   |                        |\n"
          "# |   |                              | reason non-empty} for every entry after A101 (now A102) + any changed row      |                        |\n",
          "# | P5| dispositions JSON (0633;     | root writes it at assembly: $CTRL/V007_SEAL_ASSEMBLY_INPUTS/                   | env path + sha (root); |\n"
          "# |   | 0640 SA-CX1-B3, PV-D05-1)    | COVERED_LATER_DISPOSITIONS_V007.json, the v003 OBJECT {schema, frozen_addendum_| the SAME pinned file   |\n"
          "# |   |                              | sha256, entries}: a row for every entry after A101 (now A102-A104) and for any | goes to tools 1, 3, 4  |\n"
          "# |   |                              | changed cited entry (revised + prereg_revision, or no_change_after_change +    |                        |\n"
          "# |   |                              | changed_text + why_no_prereg_effect; key names PENDING v003 final)             |                        |\n"))
R.append(("#   UNT_SEAL_DISPOSITIONS_PATH / _SHA256  the dispositions JSON (under $CTRL/V007_SEAL_ASSEMBLY_INPUTS/), verified before tools 1, 3, 4;\n"
          "#                                         format: Claude4 0105 / the v003 README (frozen_addendum_sha256; rows entry, disposition,\n"
          "#                                         reason, section_sha256 [, change]) for every entry after A101 plus any changed table row\n",
          "#   UNT_SEAL_DISPOSITIONS_PATH / _SHA256  the v003 dispositions OBJECT (under $CTRL/V007_SEAL_ASSEMBLY_INPUTS/), verified from bytes\n"
          "#                                         before tools 1, 3 and 4, which all receive this same pinned file: schema\n"
          "#                                         UNT_V007_LATER_ENTRY_DISPOSITIONS_C4V001 (v003 dev seal_common L24; PENDING v003 final),\n"
          "#                                         keys exactly {schema, frozen_addendum_sha256, entries}; no bare list, 'dispositions' or 'rows'\n"))
R.append(('HELPER="$C3/tools/seal_steps_c3sa_c3v007.py";          HELPER_SHA="2f08fb88c17dbe340fe5f03da10ed510aff384cdb404d8e3d9544664d2d79172"\n'
          'FENCE="$C3/tools/fence_c3sa_c3v003.py";                 FENCE_SHA="9c62ad4902c895f0aeeba3a78976b5944146ee0de153989dbc79470528dd2863"\n',
          'HELPER="$C3/tools/seal_steps_c3sa_c3v009.py";          HELPER_SHA="000798141398d27308d95e7a25fc64d17abe9831c47a2b27457439b7bc7922a3"\n'
          'FENCE="$C3/tools/fence_c3sa_c3v003.py";                 FENCE_SHA="9c62ad4902c895f0aeeba3a78976b5944146ee0de153989dbc79470528dd2863"\n'
          'RUNNER="$C3/tools/run_pinned_c3sa_c3v002.py";          RUNNER_SHA="b57e4859c498bf57e05706dcd83d89db0f14102c33aec7359580c155d924861c"\n'))
R.append(('PREREG_TOR="$A/v007_final_prereg_c4/r5/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json"; PREREG_TOR_SHA="3245899f68081a48928a7242a1d9f1ee3694bb13b3f04913dcb2825104a93393"\n',
          'PREREG_TOR="$A/v007_final_prereg_c4/r5/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json"; PREREG_TOR_SHA="3245899f68081a48928a7242a1d9f1ee3694bb13b3f04913dcb2825104a93393"\n'
          'TABLE_BYTES="$A/v007_final_prereg_c4/r5/addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md"; TABLE_BYTES_SHA="70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e"\n'))
R.append(('SEAL_TOOLS_COVERED_LATER_MODE="v003_dispositions"      # v003 interface (0633): tools 1, 3, 4 take the dispositions JSON\n'
          'T_DISPOSITIONS_FLAG="--dispositions"; T_DISPOSITIONS_SHA_FLAG="--dispositions-sha"   # v003 flags as announced (Claude4 0105)\n'
          'T_DISPOSITIONS_FLAG_STATUS="ANNOUNCED_0105_UNPUBLISHED"  # the successor sets PUBLISHED when the v003 files and README land\n',
          '# dispositions: tools 1, 3 and 4 take --dispositions D --dispositions-sha H (Claude4 0105; v003 dev CLI); v001 placeholders cannot (P1)\n'))
R.append(('T1_RUN=("$PY" -I -B "$T1"); T2_RUN=("$PY" -I -B "$T2"); T3_RUN=("$PY" -I -B "$T3"); T4_RUN=("$PY" -I -B "$T4")\n',
          '# T1_RUN .. T4_RUN: see RUN FORMS below (every seal tool runs from its verified bytes through the pinned-source runner)\n'))
R.append(('SUMMARY="$SEAL_DIR/SEAL_ASSEMBLY_SUMMARY_V007.json"\n',
          'SUMMARY="$SEAL_DIR/SEAL_ASSEMBLY_SUMMARY_V007.json"\n'
          'PYC_PREFIX="$SEAL_DIR/NO_PYCACHE_PREFIX_EMPTY"   # SA-CX1-B2: absent until step 1 creates it empty; -B keeps it empty\n'
          'PYX=("$PY" -I -B -X "pycache_prefix=$PYC_PREFIX") # every Python process: isolated, no bytecode written, no __pycache__ .pyc read\n'
          '# ---------------------------------------------------------------------------------------------------------- RUN FORMS (SA-CX1-B2)\n'
          'RUN_MODS_COMMON=(--module "seal_common_c4v001=$T_COMMON=$T_COMMON_SHA")\n'
          'T1_RUN=("${PYX[@]}" "$RUNNER" "${RUN_MODS_COMMON[@]}" --main "$T1=$T1_SHA" --call main --)\n'
          'T2_RUN=("${PYX[@]}" "$RUNNER" "${RUN_MODS_COMMON[@]}" --main "$T2=$T2_SHA" --call main --)\n'
          'T3_RUN=("${PYX[@]}" "$RUNNER" "${RUN_MODS_COMMON[@]}" --module "check_frozen_addendum_c4v001=$T1=$T1_SHA" --module "check_sealed_compare_c4v001=$T2=$T2_SHA" --main "$T3=$T3_SHA" --call main --)\n'
          'T4_RUN=("${PYX[@]}" "$RUNNER" "${RUN_MODS_COMMON[@]}" --module "check_frozen_addendum_c4v001=$T1=$T1_SHA" --module "check_sealed_compare_c4v001=$T2=$T2_SHA" --module "check_slot_fill_c4v001=$T3=$T3_SHA" --main "$T4=$T4_SHA" --call main --)\n'))
R.append(('H() { "$PY" -I -B "$HELPER" "$@"; }\n', 'H() { "${PYX[@]}" "$HELPER" "$@"; }\n'))
R.append(("jf() { \"$PY\" -I -B -c 'import json,sys\n", "jf() { \"${PYX[@]}\" -c 'import json,sys\n"))
R.append(('v005_still_frozen() { H same-bytes', 'pyc_prefix_empty() { [ ! -e "$PYC_PREFIX" ] || [ -z "$(/bin/ls -A "$PYC_PREFIX")" ] || { echo "REFUSE: the empty pycache prefix gained a file (SA-CX1-B2)" >&2; false; }; }\nv005_still_frozen() { pyc_prefix_empty; H same-bytes'))
R.append(('  STEP=0; echo "STEP 0 preflight (writes nothing)"\n',
          '  STEP=0; echo "STEP 0 preflight (writes nothing)"\n'
          '  # before ANY Python runs: the seal folder (which holds the empty pycache prefix) must not exist yet\n'
          '  { [ ! -e "$SEAL_DIR" ] && [ ! -L "$SEAL_DIR" ]; } || { echo "REFUSE: the seal folder exists already: $SEAL_DIR" >&2; false; }\n'))
R.append(("  [ \"$(sha_of \"$(\"$PY\" -I -B -c 'import os,sys; print(os.path.realpath(sys.executable))')\")\" = \"$PY_REAL_SHA\" ]\n"
          "  [ \"$(\"$PY\" -I -B -c 'import sys; print(sys.stdout.encoding.lower().replace(\"-\",\"\"), sys.version_info[:2])')\" = \"utf8 (3, 12)\" ]\n"
          "  [ \"$(sha_of \"$HELPER\")\" = \"$HELPER_SHA\" ]                       # the helper verifies everything else from bytes\n",
          "  [ \"$(sha_of \"$(\"${PYX[@]}\" -c 'import os,sys; print(os.path.realpath(sys.executable))')\")\" = \"$PY_REAL_SHA\" ]\n"
          "  [ \"$(\"${PYX[@]}\" -c 'import sys; print(sys.stdout.encoding.lower().replace(\"-\",\"\"), sys.version_info[:2], sys.flags.dont_write_bytecode, sys.pycache_prefix is not None)')\" = \"utf8 (3, 12) 1 True\" ]\n"
          "  [ \"$(sha_of \"$HELPER\")\" = \"$HELPER_SHA\" ] && [ \"$(sha_of \"$RUNNER\")\" = \"$RUNNER_SHA\" ]   # these verify everything else from bytes\n"))
R.append(('  case "$SEAL_TOOLS_COVERED_LATER_MODE" in v003_dispositions|v001_names) ;; *) echo "REFUSE: SEAL_TOOLS_COVERED_LATER_MODE" >&2; false;; esac\n'
          '  if [ "$SEAL_TOOLS_COVERED_LATER_MODE" = v003_dispositions ] && [ "$T_DISPOSITIONS_FLAG_STATUS" != PUBLISHED ]; then\n'
          '    echo "REFUSE: the v003 dispositions flag is a placeholder (P1)" >&2; false; fi\n', ''))
R.append(('  H pin --pin "$FENCE=$FENCE_SHA" --pin "$DRAFT=$DRAFT_SHA"', '  H pin --pin "$FENCE=$FENCE_SHA" --pin "$RUNNER=$RUNNER_SHA" --pin "$TABLE_BYTES=$TABLE_BYTES_SHA" --pin "$DRAFT=$DRAFT_SHA"'))
R.append(("  \"$PY\" -I -B -c 'import json,sys\nb=open(sys.argv[1],\"rb\").read(); t=b.decode(\"utf-8\")", "  \"${PYX[@]}\" -c 'import json,sys\nb=open(sys.argv[1],\"rb\").read(); t=b.decode(\"utf-8\")"))
R.append(('  /bin/mkdir "$SEAL_DIR"; /bin/mkdir "$LOGS"\n', '  /bin/mkdir "$SEAL_DIR"; /bin/mkdir "$LOGS"; /bin/mkdir "$PYC_PREFIX"\n'))
R.append(('        --dispositions "$UNT_SEAL_DISPOSITIONS_PATH" --dispositions-sha "$UNT_SEAL_DISPOSITIONS_SHA256"\n'
          '  COVERED_NAMES="$(jf "$LOGS/STEP_02_DISPOSITIONS.json" covered_later_names_for_v001)"\n'
          '  if [ "$SEAL_TOOLS_COVERED_LATER_MODE" = v003_dispositions ]; then\n'
          '    COV_ARGS=("$T_DISPOSITIONS_FLAG" "$UNT_SEAL_DISPOSITIONS_PATH" "$T_DISPOSITIONS_SHA_FLAG" "$UNT_SEAL_DISPOSITIONS_SHA256")\n'
          '  else COV_ARGS=(--covered-later "$COVERED_NAMES"); fi      # v001 placeholders take bare names only (the D-05 defect v003 closes)\n',
          '        --dispositions "$UNT_SEAL_DISPOSITIONS_PATH" --dispositions-sha "$UNT_SEAL_DISPOSITIONS_SHA256" --table-bytes "$TABLE_BYTES" \\\n'
          '        --table-bytes-sha "$TABLE_BYTES_SHA"\n'
          '  COVERED_NAMES="$(jf "$LOGS/STEP_02_DISPOSITIONS.json" covered_later_names_for_v001_placeholders_only)"\n'
          '  COV_ARGS=(--dispositions "$UNT_SEAL_DISPOSITIONS_PATH" --dispositions-sha "$UNT_SEAL_DISPOSITIONS_SHA256")   # SA-CX1-B3: one pinned file, tools 1, 3, 4\n'))
R.append(('  # the dispositions JSON first (0633): no bare name, no empty reason, exactly the entries after the table plus any changed row\n',
          '  # the dispositions OBJECT first (0633; 0640 SA-CX1-B3, PV-D05-1): exactly the later entries plus any changed cited entry\n'))
R.append(('  H pin --pin "$PREREG_TOR=$PREREG_TOR_SHA" --pin "$FROZEN=$FROZEN_SHA" --pin "$T1=$T1_SHA" --pin "$T_COMMON=$T_COMMON_SHA" \\\n'
          '        --pin "$UNT_SEAL_DISPOSITIONS_PATH=$UNT_SEAL_DISPOSITIONS_SHA256" 2> "$LOGS/STEP_02_INPUTS.json"\n',
          '  H pin --pin "$PREREG_TOR=$PREREG_TOR_SHA" --pin "$FROZEN=$FROZEN_SHA" --pin "$T1=$T1_SHA" --pin "$T_COMMON=$T_COMMON_SHA" \\\n'
          '        --pin "$RUNNER=$RUNNER_SHA" --pin "$UNT_SEAL_DISPOSITIONS_PATH=$UNT_SEAL_DISPOSITIONS_SHA256" 2> "$LOGS/STEP_02_INPUTS.json"\n'))
R.append(('  run_h STEP_02_REHASH rehash-entries --prereg "$PREREG_TOR" --prereg-sha "$PREREG_TOR_SHA" --frozen "$FROZEN" --frozen-sha "$FROZEN_SHA" \\\n'
          '        --dispositions "$UNT_SEAL_DISPOSITIONS_PATH" --dispositions-sha "$UNT_SEAL_DISPOSITIONS_SHA256"\n}',
          '  run_h STEP_02_REHASH rehash-entries --prereg "$PREREG_TOR" --prereg-sha "$PREREG_TOR_SHA" --frozen "$FROZEN" --frozen-sha "$FROZEN_SHA" \\\n'
          '        --dispositions "$UNT_SEAL_DISPOSITIONS_PATH" --dispositions-sha "$UNT_SEAL_DISPOSITIONS_SHA256" --table-bytes "$TABLE_BYTES" \\\n'
          '        --table-bytes-sha "$TABLE_BYTES_SHA"\n}'))
R.append(('  STEP=2; echo "STEP 2 tool 1 check_frozen_addendum + r5 entry-table re-hash (README_SEAL_TOOLS L11; SEAL_CHECKLIST_R5 L23; r5 srr[11]; 0633; Claude4 0105)"',
          '  STEP=2; echo "STEP 2 tool 1 check_frozen_addendum + dispositions + entry-table re-hash (README_SEAL_TOOLS v002 L35 / v001 L11; SEAL_CHECKLIST_R5 L23; r5 srr[11]; 0633; 0640)"'))
R.append(('  H pin --pin "$BINDER=$BINDER_SHA" --pin "$TEMPLATE=$TEMPLATE_SHA" --pin "$DRIVER=$DRIVER_SHA" --pin "$FROZEN=$FROZEN_SHA" 2> "$LOGS/STEP_03_INPUTS.json"\n',
          '  H pin --pin "$BINDER=$BINDER_SHA" --pin "$RUNNER=$RUNNER_SHA" --pin "$TEMPLATE=$TEMPLATE_SHA" --pin "$DRIVER=$DRIVER_SHA" --pin "$FROZEN=$FROZEN_SHA" 2> "$LOGS/STEP_03_INPUTS.json"\n'))
R.append(("  \"$PY\" -I -B -c 'import json,os,sys,shutil\n", "  \"${PYX[@]}\" -c 'import json,os,sys,shutil\n"))
R.append(('  "$PY" -I -B "$BINDER" --template "$TEMPLATE" --driver "$DRIVER" --driver-sha256 "$DRIVER_SHA" --frozen-addendum "$FROZEN" \\\n',
          '  "${PYX[@]}" "$RUNNER" --main "$BINDER=$BINDER_SHA" --call argv -- --template "$TEMPLATE" --driver "$DRIVER" --driver-sha256 "$DRIVER_SHA" --frozen-addendum "$FROZEN" \\\n'))
R.append(('# =================================================================================================== STEP 6: tool 3 check_slot_fill\nstep6_tool3() {\n  STEP=6; echo "STEP 6 check_slot_fill (README_SEAL_TOOLS L12, \'after B4\')"\n  v005_still_frozen 6\n',
          '# ======================================================================================== STEP 4a: tool 3 check_slot_fill (after B4)\nstep4a_tool3() {\n  STEP=4a; echo "STEP 4a tool 3 check_slot_fill, after B4 (README_SEAL_TOOLS v002 L37 / v001 L12)"\n  v005_still_frozen 4a\n'))
R.append(('        --pin "$UNT_SEAL_DISPOSITIONS_PATH=$UNT_SEAL_DISPOSITIONS_SHA256" $(printf -- \'--pin %s \' "${TOOL_PINS[@]}") 2> "$LOGS/STEP_06_INPUTS.json"\n'
          '  "${T3_RUN[@]}" --slots "$SLOTS_FINAL" --prereg "$SEALED_PREREG" --text-of-record "$PREREG_TOR" --frozen "$FROZEN" \\\n'
          '        "${COV_ARGS[@]}" > "$LOGS/STEP_06_TOOL3.json"\n  echo "  PASS  STEP_06_TOOL3.json"\n',
          '        --pin "$RUNNER=$RUNNER_SHA" --pin "$UNT_SEAL_DISPOSITIONS_PATH=$UNT_SEAL_DISPOSITIONS_SHA256" $(printf -- \'--pin %s \' "${TOOL_PINS[@]}") 2> "$LOGS/STEP_04A_INPUTS.json"\n'
          '  "${T3_RUN[@]}" --slots "$SLOTS_FINAL" --prereg "$SEALED_PREREG" --text-of-record "$PREREG_TOR" --frozen "$FROZEN" \\\n'
          '        "${COV_ARGS[@]}" > "$LOGS/STEP_04A_TOOL3.json"\n  echo "  PASS  STEP_04A_TOOL3.json"\n'))
R.append(('# ============================================================================================== STEP 7: tool 2 check_sealed_compare\nstep7_tool2() {\n  STEP=7; echo "STEP 7 check_sealed_compare (README_SEAL_TOOLS L13, \'after B5\')"\n  v005_still_frozen 7\n'
          '  H pin --pin "$UNT_SEAL_COMPARE_REVIEWED_PATH=$UNT_SEAL_COMPARE_REVIEWED_SHA256" --pin "$SEALED_COMPARE=$SC_SHA" --pin "$SLOTS_FINAL=$SLOTS_SHA" \\\n'
          '        --pin "$SEALED_PREREG=$SP_SHA" $(printf -- \'--pin %s \' "${TOOL_PINS[@]}") 2> "$LOGS/STEP_07_INPUTS.json"\n'
          '  "${T2_RUN[@]}" --reviewed "$UNT_SEAL_COMPARE_REVIEWED_PATH" --sealed "$SEALED_COMPARE" --slots "$SLOTS_FINAL" --prereg "$SEALED_PREREG" > "$LOGS/STEP_07_TOOL2.json"\n'
          '  echo "  PASS  STEP_07_TOOL2.json"\n',
          '# =================================================================================== STEP 5a: tool 2 check_sealed_compare (after B5)\nstep5a_tool2() {\n  STEP=5a; echo "STEP 5a tool 2 check_sealed_compare, after B5 (README_SEAL_TOOLS v002 L38 / v001 L13)"\n  v005_still_frozen 5a\n'
          '  H pin --pin "$UNT_SEAL_COMPARE_REVIEWED_PATH=$UNT_SEAL_COMPARE_REVIEWED_SHA256" --pin "$SEALED_COMPARE=$SC_SHA" --pin "$SLOTS_FINAL=$SLOTS_SHA" \\\n'
          '        --pin "$SEALED_PREREG=$SP_SHA" --pin "$RUNNER=$RUNNER_SHA" $(printf -- \'--pin %s \' "${TOOL_PINS[@]}") 2> "$LOGS/STEP_05A_INPUTS.json"\n'
          '  "${T2_RUN[@]}" --reviewed "$UNT_SEAL_COMPARE_REVIEWED_PATH" --sealed "$SEALED_COMPARE" --slots "$SLOTS_FINAL" --prereg "$SEALED_PREREG" > "$LOGS/STEP_05A_TOOL2.json"\n'
          '  echo "  PASS  STEP_05A_TOOL2.json"\n'))
R.append(('  H pin --pin "$SEALED_COMPARE=$SC_SHA" --pin "$SEALED_PREREG=$SP_SHA" --pin "$C5H_MANIFEST=$msha" 2> "$LOGS/STEP_09_INPUTS.json"\n'
          '  "$PY" -I -B "$SEALED_COMPARE" --prereg "$SEALED_PREREG" --manifest "$C5H_MANIFEST" --outdir "$VALIDITY_OUTDIR" --validity-only --case C5H \\\n',
          '  H pin --pin "$SEALED_COMPARE=$SC_SHA" --pin "$SEALED_PREREG=$SP_SHA" --pin "$C5H_MANIFEST=$msha" --pin "$RUNNER=$RUNNER_SHA" 2> "$LOGS/STEP_09_INPUTS.json"\n'
          '  "${PYX[@]}" "$RUNNER" --main "$SEALED_COMPARE=$SC_SHA" --call main -- --prereg "$SEALED_PREREG" --manifest "$C5H_MANIFEST" \\\n'
          '        --outdir "$VALIDITY_OUTDIR" --validity-only --case C5H \\\n'))
R.append(('        --pin "$UNT_SEAL_SUCCESSOR_CUSTODY_PATH=$UNT_SEAL_SUCCESSOR_CUSTODY_SHA256" --pin "$UNT_SEAL_DISPOSITIONS_PATH=$UNT_SEAL_DISPOSITIONS_SHA256" \\\n',
          '        --pin "$UNT_SEAL_SUCCESSOR_CUSTODY_PATH=$UNT_SEAL_SUCCESSOR_CUSTODY_SHA256" --pin "$UNT_SEAL_DISPOSITIONS_PATH=$UNT_SEAL_DISPOSITIONS_SHA256" \\\n'
          '        --pin "$RUNNER=$RUNNER_SHA" \\\n'))
R.append(("  \"$PY\" -I -B -c 'import json,sys\nk=sys.argv[2::2]", "  \"${PYX[@]}\" -c 'import json,sys\nk=sys.argv[2::2]"))
R.append(('step4_sealed_prereg\nstep5_sealed_compare\nstep6_tool3\nstep7_tool2\n', 'step4_sealed_prereg\nstep4a_tool3\nstep5_sealed_compare\nstep5a_tool2\n'))
for o, n in R:
    c = s.count(o)
    assert c == 1, ('count %d' % c, o[:90])
    s = s.replace(o, n)
left = [m.start() for m in re.finditer(r'"\$PY" -I -B', s)]
assert len(left) == 1 and 'PYX=("$PY" -I -B -X' in s, ('raw PY invocations left', len(left))
for bad in ('SEAL_TOOLS_COVERED_LATER_MODE', 'T_DISPOSITIONS_FLAG', 'covered_later_names_for_v001)', 'step6_tool3', 'step7_tool2'):
    assert bad not in s, bad
open(D + '/ROOT_SEAL_STEPS_c3v007.sh', 'x').write(s)
print('ROOT_SEAL_STEPS_c3v007.sh', hashlib.sha256(s.encode()).hexdigest())
