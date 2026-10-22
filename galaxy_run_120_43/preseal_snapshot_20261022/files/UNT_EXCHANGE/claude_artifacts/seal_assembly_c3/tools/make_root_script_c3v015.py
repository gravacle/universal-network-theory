# make_root_script_c3v015.py: Claude3 (WIRE v003, the last input). Derives ROOT_SEAL_STEPS_c3v015.sh from c3v014 (0775e5c5).
import hashlib, sys
C3, HELPER_SHA = sys.argv[1], sys.argv[2]
src = open(C3 + '/ROOT_SEAL_STEPS_c3v014.sh', 'rb').read()
assert hashlib.sha256(src).hexdigest() == '0775e5c5002bf3d46874a37338ec1da731211d174939b1a0879a4ed5d2c3e8c7'
assert hashlib.sha256(open(C3 + '/tools/seal_steps_c3sa_c3v015.py', 'rb').read()).hexdigest() == HELPER_SHA
s = src.decode('utf-8')
R = [
 ('# ROOT_SEAL_STEPS_c3v014.sh: the V007 seal assembly', '# ROOT_SEAL_STEPS_c3v015.sh: the V007 seal assembly'),
 ('# c3v014 supersedes ROOT_SEAL_STEPS_c3v013.sh (c1a469e9):', '''# c3v015 supersedes ROOT_SEAL_STEPS_c3v014.sh (0775e5c5): seal tools v003 WIRED from Claude4's SELECTED_SEAL_TOOLS_V003_C4V001.json
#   (cf7e5b2f, 00:51:45Z), role-qualified in step 0 (seal_common, tool_1 .. tool_5, readme, selected_r6). The FINAL pre-stage script:
#   step 0 no longer refuses for P1 or P11; only root's inputs P2-P10 remain. The order is README_SEAL_TOOLS_V003's (L157): tool 1
#   (step 2: --expect-frozen-sha c01b3c51, R-01, and --addendum-at-text-of-record), tool 5 (step 2a: the driver BUILD record is tool 5's
#   bytes, written exclusively, re-checked by the helper), tool 3 (4a), tool 2 (5a), tool 4 build (10: --text-of-record-sha,
#   --addendum-at-text-of-record, --b2-record, the compare's own GATES_ONLY.json / VALIDITY_ONLY.json), tool 4 admission (12, B8).
#   v003 tool 4 has no errata input, so E_R6_1 stays root's manual statement with the SEAL_RECORD publication. Helper c3v015.
# c3v014 superseded ROOT_SEAL_STEPS_c3v013.sh (c1a469e9):'''),
 ('''# | P1| seal tools v003 (Claude4;    | NOT PUBLISHED: T1..T4 below are v001 PLACEHOLDERS (v001 tools 3/4 are pinned  | successor: v003 paths, |
# |   | A106.2: D-05/C-01, B8, the   | to prereg r4 e3b6b5b2 and miss ddo_gas_M_s: they REFUSE r5); V003_SELECTED is  | shas and CLI from its  |
# |   | README fix, the W7-S1 cases) | PENDING (0643 C: the tool paths and shas must be named by its SELECTED file)   | SELECTED file          |
''', '''# | P1| seal tools v003 (Claude4;    | DONE: wired from SELECTED_SEAL_TOOLS_V003_C4V001.json (cf7e5b2f), every tool   | done (c3v015)          |
# |   | A106.2: D-05/C-01, B8, the   | pin role-qualified (tool_1 .. tool_5, seal_common, readme, selected_r6); the   |                        |
# |   | README fix, the W7-S1 cases) | v003 CLI from README_SEAL_TOOLS_V003 (86012117) and each tool's argparse.      |                        |
'''),
 ('''# seal tools: v001 PLACEHOLDERS (P1). A successor script pins v003 here and its exact dispositions flag.
SEAL_TOOLS_STATUS="PENDING_V003__V001_PLACEHOLDERS"
V003_SELECTED="PENDING_V003_SELECTED_FILE"; V003_SELECTED_SHA="PENDING_V003_SELECTED_FILE_SHA"   # 0643 C: it must name every T_* path and sha
# dispositions: tools 1, 3 and 4 take --dispositions D --dispositions-sha H (Claude4 0105; v003 dev CLI); v001 placeholders cannot (P1)
''', '''# seal tools v003 (P1 DONE): Claude4's SELECTED_SEAL_TOOLS_V003_C4V001.json (00:51:45Z), checked role-qualified in step 0
SEAL_TOOLS_STATUS="V003_SELECTED_C4V001"
V003_SELECTED="$A/v007_final_prereg_c4/seal_tools_v003/SELECTED_SEAL_TOOLS_V003_C4V001.json"; V003_SELECTED_SHA="cf7e5b2f1b3daf55c485ada1c869bc7249040a8db8202eb1b1a90bebe1431305"
V003_SELECTED_SCHEMA="UNT_V007_SELECTED_SEAL_TOOLS_C4V001"
# dispositions: tools 1, 3 and 4 take --dispositions D --dispositions-sha H (README_SEAL_TOOLS_V003 section B; optional as a group,
# required when L u CH is not empty; for r6 they are empty, and the pinned entries:[] object is passed)
'''),
 ('''TD="$A/v007_final_prereg_c4/seal_tools"
T_COMMON="$TD/seal_common_c4v001.py";          T_COMMON_SHA="43d8f8eb610106c61be197defba59cff7f357bb31c70ca9c9136a44b5d267c25"
T1="$TD/check_frozen_addendum_c4v001.py";      T1_SHA="c4ebbb5bf69bb8b9c2ea82046c3553897a246cefc417f2d8bc556b10c62381e2"
T2="$TD/check_sealed_compare_c4v001.py";       T2_SHA="b339a8f6051ffe7a596179216ec3ba6e103a14356ed13befa51cf3529110b3ed"
T3="$TD/check_slot_fill_c4v001.py";            T3_SHA="7f3cf07da0d92fef0a1cc592cb644eafca2737e90b917e83ea9ffa5fc367187b"
T4="$TD/build_seal_record_c4v001.py";          T4_SHA="3091fc2afa2e16f74d8c634d8605205c792788924f078b5aae806351a1d18c70"
''', '''TD="$A/v007_final_prereg_c4/seal_tools_v003"
T_COMMON="$TD/seal_common_c4v003.py";          T_COMMON_SHA="101a3aeb9846a21c35993e8e7e4b50a8f1206ed4202b131afd12d7e496c5ab21"
T1="$TD/check_frozen_addendum_c4v003.py";      T1_SHA="a56f8d793750151920b1b47e77b46aebbfadea71fe77730f360beb02af788fb4"
T2="$TD/check_sealed_compare_c4v003.py";       T2_SHA="c2c5dfc5ddba1e44ff82811a38d4c05b0a669f2294b229efe3437623d596f9f1"
T3="$TD/check_slot_fill_c4v003.py";            T3_SHA="316973a1abf5aa2151dc1a517733d970ce1004313395d05fe590f82ed439b0af"
T4="$TD/build_seal_record_c4v003.py";          T4_SHA="de0ceb15ebfb95e04227730bd2785eb46af8cb5980012de91de98f34ea226b96"
T5="$TD/print_driver_build_record_c4v003.py";  T5_SHA="e5bedffe3c91650d5dba7fbd1ed5476e228158679d8959dfea0e2eff436ebdea"
V003_README="$TD/README_SEAL_TOOLS_V003.md";    V003_README_SHA="8601211723b352a9498fa4cb8d3dc4b64d30b7451c400c89230e5d13cd909ea0"
# the B2 record of record (A100; r6 asks the seal record to repeat its disclosure block, so v003 tool 4 needs --b2-record): V009 gate_records.B2
B2_RECORD="$A/gate_b2_c3/out/B2_GATE_RECORD_C3V003.json";   B2_RECORD_SHA="915fbcda4f4a2cb5f61b257ff83494738144e177401c11c94e254c322df2411c"
'''),
 ('TOOL_PINS=("$T_COMMON=$T_COMMON_SHA" "$T1=$T1_SHA" "$T2=$T2_SHA" "$T3=$T3_SHA" "$T4=$T4_SHA")',
  'TOOL_PINS=("$T_COMMON=$T_COMMON_SHA" "$T1=$T1_SHA" "$T2=$T2_SHA" "$T3=$T3_SHA" "$T4=$T4_SHA" "$T5=$T5_SHA")'),
 ('''RUN_MODS_COMMON=(--module "seal_common_c4v001=$T_COMMON=$T_COMMON_SHA")
''', '''RUN_MODS_COMMON=(--module "seal_common_c4v003=$T_COMMON=$T_COMMON_SHA")
'''),
 ('''T3_RUN=("${PYX[@]}" "$RUNNER" "${RUN_MODS_COMMON[@]}" --module "check_frozen_addendum_c4v001=$T1=$T1_SHA" --module "check_sealed_compare_c4v001=$T2=$T2_SHA" --main "$T3=$T3_SHA" --call main --)
T4_RUN=("${PYX[@]}" "$RUNNER" "${RUN_MODS_COMMON[@]}" --module "check_frozen_addendum_c4v001=$T1=$T1_SHA" --module "check_sealed_compare_c4v001=$T2=$T2_SHA" --module "check_slot_fill_c4v001=$T3=$T3_SHA" --main "$T4=$T4_SHA" --call main --)
''', '''T3_RUN=("${PYX[@]}" "$RUNNER" "${RUN_MODS_COMMON[@]}" --module "check_frozen_addendum_c4v003=$T1=$T1_SHA" --module "check_sealed_compare_c4v003=$T2=$T2_SHA" --main "$T3=$T3_SHA" --call main --)
T4_RUN=("${PYX[@]}" "$RUNNER" "${RUN_MODS_COMMON[@]}" --module "check_frozen_addendum_c4v003=$T1=$T1_SHA" --module "check_sealed_compare_c4v003=$T2=$T2_SHA" --module "check_slot_fill_c4v003=$T3=$T3_SHA" --main "$T4=$T4_SHA" --call main --)
T5_RUN=("${PYX[@]}" "$RUNNER" "${RUN_MODS_COMMON[@]}" --main "$T5=$T5_SHA" --call main --)
'''),
 ('''  H selected-names --selected "$V003_SELECTED" --selected-sha "$V003_SELECTED_SHA" $(printf -- '--pin %s ' "${TOOL_PINS[@]}")
''', '''  H selected-roles --selected "$V003_SELECTED" --selected-sha "$V003_SELECTED_SHA" --schema "$V003_SELECTED_SCHEMA" \\
        --role-pin "seal_common=$T_COMMON=$T_COMMON_SHA" --role-pin "tool_1_check_frozen_addendum=$T1=$T1_SHA" \\
        --role-pin "tool_2_check_sealed_compare=$T2=$T2_SHA" --role-pin "tool_3_check_slot_fill=$T3=$T3_SHA" \\
        --role-pin "tool_4_build_seal_record=$T4=$T4_SHA" --role-pin "tool_5_print_driver_build_record=$T5=$T5_SHA" \\
        --role-pin "readme=$V003_README=$V003_README_SHA" --role-pin "selected_r6=$R6_SELECTED=$R6_SELECTED_SHA"
'''),
 ('        --pin "$IDREC_B0P=$IDREC_B0P_SHA" --pin "$B0_RECORD=$B0_RECORD_SHA" \\\n',
  '        --pin "$IDREC_B0P=$IDREC_B0P_SHA" --pin "$B0_RECORD=$B0_RECORD_SHA" --pin "$B2_RECORD=$B2_RECORD_SHA" \\\n'),
 ('''  "${T1_RUN[@]}" --prereg "$PREREG_TOR" --frozen "$FROZEN" --expect-frozen-sha "$FROZEN_SHA" "${COV_ARGS[@]}" > "$LOGS/STEP_02_TOOL1.json"
''', '''  # v003 SELECTED basis R-01 / script_requirement: every direct tool 1 run gets --expect-frozen-sha c01b3c51 (bytes outside the entry
  # sections are compared only through it) and --addendum-at-text-of-record (the read copy r6 pins)
  "${T1_RUN[@]}" --prereg "$PREREG_TOR" --frozen "$FROZEN" --expect-frozen-sha "$V005_FINAL_SHA" --addendum-at-text-of-record "$TABLE_BYTES" \\
        "${COV_ARGS[@]}" > "$LOGS/STEP_02_TOOL1.json"
'''),
 ('''  STEP=2a; echo "STEP 2a driver r5 + exclusive driver BUILD record (SEAL_CHECKLIST_R5 L24-L25 B2/B2a; r5 srr[8]; A72; A96)"
  v005_still_frozen 2a
  run_h STEP_02A_DRIVER_BUILD driver-build-record --compare "$UNT_SEAL_COMPARE_REVIEWED_PATH" --compare-sha "$UNT_SEAL_COMPARE_REVIEWED_SHA256" \\
        --check-record "$UNT_SEAL_DRIVER_CHECK_RECORD_PATH" --check-sha "$UNT_SEAL_DRIVER_CHECK_RECORD_SHA256" --fence "$FENCE" --fence-sha "$FENCE_SHA" \\
        --out "$DRIVER_BUILD_RECORD"
  DBR_SHA="$(jf "$LOGS/STEP_02A_DRIVER_BUILD.json" driver_build_record.sha256)"
''', '''  STEP=2a; echo "STEP 2a v003 tool 5 print_driver_build_record -> exclusive driver BUILD record, re-checked (README_SEAL_TOOLS_V003 B2a; SEAL_CHECKLIST_R5 L24-L25 B2/B2a; r5 srr[8]; A72; A96)"
  v005_still_frozen 2a
  H pin --pin "$UNT_SEAL_COMPARE_REVIEWED_PATH=$UNT_SEAL_COMPARE_REVIEWED_SHA256" --pin "$UNT_SEAL_DRIVER_CHECK_RECORD_PATH=$UNT_SEAL_DRIVER_CHECK_RECORD_SHA256" \\
        --pin "$T5=$T5_SHA" --pin "$T_COMMON=$T_COMMON_SHA" --pin "$RUNNER=$RUNNER_SHA" 2> "$LOGS/STEP_02A_INPUTS.json"
  "${T5_RUN[@]}" --reviewed "$UNT_SEAL_COMPARE_REVIEWED_PATH" --reviewed-sha "$UNT_SEAL_COMPARE_REVIEWED_SHA256" \\
        --check-record "$UNT_SEAL_DRIVER_CHECK_RECORD_PATH" > "$LOGS/STEP_02A_TOOL5.stdout.json" 2> "$LOGS/STEP_02A_TOOL5.json"
  echo "  PASS  STEP_02A_TOOL5.json"
  run_h STEP_02A_COPY copy-exclusive --src "$LOGS/STEP_02A_TOOL5.stdout.json" --src-sha "$(jf "$LOGS/STEP_02A_TOOL5.json" driver_build_record_sha256)" \\
        --dst "$DRIVER_BUILD_RECORD"
  DBR_SHA="$(sha_of "$DRIVER_BUILD_RECORD")"
  run_h STEP_02A_DRIVER_BUILD check-driver-build-record --compare "$UNT_SEAL_COMPARE_REVIEWED_PATH" --compare-sha "$UNT_SEAL_COMPARE_REVIEWED_SHA256" \\
        --record "$DRIVER_BUILD_RECORD" --record-sha "$DBR_SHA" --check-record "$UNT_SEAL_DRIVER_CHECK_RECORD_PATH" \\
        --check-sha "$UNT_SEAL_DRIVER_CHECK_RECORD_SHA256" --fence "$FENCE" --fence-sha "$FENCE_SHA"
'''),
 ('''  "${T3_RUN[@]}" --slots "$SLOTS_FINAL" --prereg "$SEALED_PREREG" --text-of-record "$PREREG_TOR" --frozen "$FROZEN" \\
        "${COV_ARGS[@]}" > "$LOGS/STEP_04A_TOOL3.json"
''', '''  "${T3_RUN[@]}" --slots "$SLOTS_FINAL" --prereg "$SEALED_PREREG" --text-of-record "$PREREG_TOR" --text-of-record-sha "$PREREG_TOR_SHA" \\
        --frozen "$FROZEN" --addendum-at-text-of-record "$TABLE_BYTES" "${COV_ARGS[@]}" > "$LOGS/STEP_04A_TOOL3.json"
'''),
 ('''  local gj gjs; gj="$(jf "$LOGS/STEP_08_GATES_ONLY.json" gates_only_json.path)"; gjs="$(jf "$LOGS/STEP_08_GATES_ONLY.json" gates_only_json.sha256)"
  run_h STEP_08_C03 gates-provenance --gates-json "$gj" --gates-json-sha "$gjs" --slots "$SLOTS_FINAL" --slots-sha "$SLOTS_SHA"
''', '''  GJ_PATH="$(jf "$LOGS/STEP_08_GATES_ONLY.json" gates_only_json.path)"; GJ_SHA="$(jf "$LOGS/STEP_08_GATES_ONLY.json" gates_only_json.sha256)"
  run_h STEP_08_C03 gates-provenance --gates-json "$GJ_PATH" --gates-json-sha "$GJ_SHA" --slots "$SLOTS_FINAL" --slots-sha "$SLOTS_SHA"
'''),
 ('''  VS_SHA="$(jf "$LOGS/STEP_09_ROW_SCAN.json" e_seal1.sha256)"
}
''', '''  VS_SHA="$(jf "$LOGS/STEP_09_ROW_SCAN.json" e_seal1.sha256)"
  VJ_PATH="$VALIDITY_OUTDIR/VALIDITY_ONLY.json"; VJ_SHA="$(sha_of "$VJ_PATH")"   # the compare's own B6 file (v003 tool 4 reads it)
}
'''),
 ('''        --pin "$GATES_STDOUT=$GS_SHA" --pin "$VALIDITY_STDOUT=$VS_SHA" \\
''', '''        --pin "$GATES_STDOUT=$GS_SHA" --pin "$VALIDITY_STDOUT=$VS_SHA" --pin "$GJ_PATH=$GJ_SHA" --pin "$VJ_PATH=$VJ_SHA" --pin "$B2_RECORD=$B2_RECORD_SHA" \\
'''),
 ('''  "${T4_RUN[@]}" --slots "$SLOTS_FINAL" --prereg "$SEALED_PREREG" --text-of-record "$PREREG_TOR" --frozen "$FROZEN" \\
        "${COV_ARGS[@]}" --reviewed "$UNT_SEAL_COMPARE_REVIEWED_PATH" --sealed-compare "$SEALED_COMPARE" \\
        --gates-only-output "$GATES_STDOUT" --validity-only-output "$VALIDITY_STDOUT" --key-equivalence-map "$UNT_SEAL_KEY_EQUIVALENCE_MAP_PATH" \\
        --new-item-list "$UNT_SEAL_NEW_ITEM_LIST_PATH" --successor-custody "$UNT_SEAL_SUCCESSOR_CUSTODY_PATH" > "$T4_STDOUT" 2> "$T4_STDERR"
''', '''  "${T4_RUN[@]}" --slots "$SLOTS_FINAL" --prereg "$SEALED_PREREG" --text-of-record "$PREREG_TOR" --text-of-record-sha "$PREREG_TOR_SHA" \\
        --frozen "$FROZEN" --addendum-at-text-of-record "$TABLE_BYTES" "${COV_ARGS[@]}" --reviewed "$UNT_SEAL_COMPARE_REVIEWED_PATH" \\
        --sealed-compare "$SEALED_COMPARE" --gates-only-output "$GJ_PATH" --validity-only-output "$VJ_PATH" \\
        --key-equivalence-map "$UNT_SEAL_KEY_EQUIVALENCE_MAP_PATH" --new-item-list "$UNT_SEAL_NEW_ITEM_LIST_PATH" \\
        --successor-custody "$UNT_SEAL_SUCCESSOR_CUSTODY_PATH" --b2-record "$B2_RECORD" > "$T4_STDOUT" 2> "$T4_STDERR"
'''),
 ('''  run_h STEP_12_CONFIG_W7_S1 check-config-allowlist --config "$CONFIG" --config-sha "$CFG_SHA" --build "$BUILD" --build-sha "$BUILD_SHA"
''', '''  run_h STEP_12_CONFIG_W7_S1 check-config-allowlist --config "$CONFIG" --config-sha "$CFG_SHA" --build "$BUILD" --build-sha "$BUILD_SHA"
  # B8 (README_SEAL_TOOLS_V003): v003 tool 4 --check-admission-config on the written config and the SEAL_RECORD, before the receipt
  H pin --pin "$CONFIG=$CFG_SHA" --pin "$SEAL_RECORD=$SR_SHA" --pin "$RUNNER=$RUNNER_SHA" $(printf -- '--pin %s ' "${TOOL_PINS[@]}") 2> "$LOGS/STEP_12_ADMISSION_INPUTS.json"
  "${T4_RUN[@]}" --check-admission-config "$CONFIG" --seal-record "$SEAL_RECORD" > "$LOGS/STEP_12_TOOL4_ADMISSION.json"
  echo "  PASS  STEP_12_TOOL4_ADMISSION.json (v003 tool 4, B8)"
'''),
 ('''                "the seal record states erratum E_R6_1 exactly as the r6 SELECTED file gives it (pins.erratum_E_R6_1_for_the_seal_record)",
''', '''                "erratum E_R6_1: v003 tool 4 takes no errata input (its argparse has none), so the SEAL_RECORD cannot carry it; root states it, exactly as the r6 SELECTED file gives it (pins.erratum_E_R6_1_for_the_seal_record), in the numbered root packet that publishes the SEAL_RECORD (a manual seal-record statement)",
'''),
 ('HELPER="$C3/tools/seal_steps_c3sa_c3v014.py";          HELPER_SHA="f41dd02f28ea46f227712fc0774e6a9069eafdc160a98438a3e8bbc6759ec931"',
  'HELPER="$C3/tools/seal_steps_c3sa_c3v015.py";          HELPER_SHA="%s"' % HELPER_SHA),
]
for o, n in R:
    assert s.count(o) == 1, (o[:90], s.count(o))
    s = s.replace(o, n)
assert 'c4v001' not in s.split('# =================================================================================================================== PENDING TABLE')[1].split('step0_preflight() {')[0].replace('UNT_V007_SEAL_SLOTS_C4V001', '').replace('UNT_V007_LATER_ENTRY_DISPOSITIONS_C4V001', '').replace('UNT_V007_SELECTED_PREREG_C4V001', '').replace('UNT_V007_SELECTED_SEAL_TOOLS_C4V001', '').replace('SELECTED_R6_C4V001', '').replace('SELECTED_SEAL_TOOLS_V003_C4V001', '').replace('V003_SELECTED_C4V001', '').replace('B0_R5_RECORD_C4V001', '').replace('CASE_BLOCK_V007_C4V001', ''), 'a v001 tool reference remains'
out = s.encode('utf-8')
with open(C3 + '/ROOT_SEAL_STEPS_c3v015.sh', 'xb') as f:
    f.write(out)
print('ROOT_SEAL_STEPS_c3v015.sh', hashlib.sha256(out).hexdigest(), len(out))
