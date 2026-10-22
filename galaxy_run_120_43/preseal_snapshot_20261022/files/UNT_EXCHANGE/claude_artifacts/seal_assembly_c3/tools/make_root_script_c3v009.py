# make_root_script_c3v009.py: Claude3 (FROM_CODEX/0642, A105; heads-up Claude4 0109). Derives ROOT_SEAL_STEPS_c3v009.sh from c3v008
# (023b2bbf) by exact replacements (each old string occurs exactly once; the step-3 pre-binding region is replaced whole).
import hashlib, sys
C3, HELPER_SHA = sys.argv[1], sys.argv[2]
src = open(C3 + '/ROOT_SEAL_STEPS_c3v008.sh', 'rb').read()
assert hashlib.sha256(src).hexdigest() == '023b2bbf63007ce2ce9e91f053313a40af4c69d57136633c88e8aed4c449b8c9'
h = open(C3 + '/tools/seal_steps_c3sa_c3v010.py', 'rb').read()
assert hashlib.sha256(h).hexdigest() == HELPER_SHA
s = src.decode('utf-8')
R = []
R.append(('''# ROOT_SEAL_STEPS_c3v008.sh: the V007 seal assembly in the order of record, for ROOT (Claude2) ONLY. Built by Claude3 (dispatch 0626;
# fix round FROM_CODEX/0639 + 0640).
''', '''# ROOT_SEAL_STEPS_c3v009.sh: the V007 seal assembly in the order of record, for ROOT (Claude2) ONLY. Built by Claude3 (dispatch 0626;
# fix round FROM_CODEX/0639 + 0640; FROM_CODEX/0642, ruling A105).
# c3v009 supersedes ROOT_SEAL_STEPS_c3v008.sh (023b2bbf; FROM_CODEX/0642, A105, from Claude4 0108; heads-up Claude4 0109):
#   RP-S1 (A105.2): STEP 3 creates the step-2 output root /Users/bgm/Research/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007 BEFORE the
#     binder, as a NEW, EMPTY, real directory, EXCLUSIVELY; step 0 already refuses if it exists in any form (directory, file or
#     symlink). Helper c3v010 'output-root': no-follow walk of every parent component (the one missing level, UNT_INTERNAL_RUNS, is
#     created); realpath = literal; st_dev = /System/Volumes/Data; empty. Device, realpath and free space go to the run log
#     (logs/STEP_03_OUTPUT_ROOT.json, a RECORD line, the summary); the summary re-verifies it is still the same empty directory.
#   W7-S1 (A105.1, A78 N2): STEP 12 builds producer_allowlist from BUILD_V007's 15-row table EXACTLY (strict section parse; any other
#     count, any row not byte-equal in path and sha, a reordered or duplicated row refuses), checked on the bytes before the exclusive
#     write and re-checked on the written file (check-config-allowlist).
#   P11 (Claude4 0109): PREREG_TOR is the ONE text-of-record pin (path + sha), used by steps 0, 2, 4, 4a and 10; the bytes its entry
#     table was read from (TABLE_BYTES) are now derived from it in step 0, so r5 -> r6 is a one-line change.
#   The disk watchdog step2_disk_watch.sh (A105.3) is a convenience: NOT part of this script, the seal or the tuple's hash chain.
#   Otherwise only the helper pin, the PENDING table (P10 note, P11, the 0109 C-02..C-06 note) and the summary's root_next change.
'''))
R.append(('# Status at build (2026-10-18 ~21:40Z). The script REFUSES in step 0 while any item below is unresolved.\n',
          '# Status at build (2026-10-18 ~22:50Z). The script REFUSES in step 0 while any item P1-P10 below is unresolved (P11 is a note).\n'))
R.append(('''# |P10| free-space floor (RUNBOOK_V008 L37) | root's GiB floor for the internal output root                          | env UNT_SEAL_MIN_FREE_GIB |
''', '''# |P10| free-space floor (RUNBOOK_V008 L37) | root's GiB floor at the output root; 0 = record only (A105.3 rules an 80 GB | env UNT_SEAL_MIN_FREE_GIB |
# |   |                              | watchdog, not a refusal). Free space is always logged (RP-S1).                 |                        |
# |P11| text of record (Claude4 0109)| r5 now: PREREG_TOR, ONE line (path + sha) used by steps 0, 2, 4, 4a and 10;    | a successor changes    |
# |   |                              | its table bytes derive from it. r6 expected (Claude4 0109 F-01: r5's text is   | that one line          |
# |   |                              | stale after A102-A105).                                                        |                        |
# Claude4 0109 section 2, C-02..C-06: possible script-encoded checks pending root's ruling on 0109 section 2 (NOT implemented here;
# listed in README_SEAL_ASSEMBLY_C3_c3v003.md).
'''))
R.append(('''#   ROOT_SEAL_ADMISSION config $PKT/ROOT_SEAL_ADMISSION_V001.json                                              FIXED (guard v008 L8; FORMAT_V005 L7)
''', '''#   ROOT_SEAL_ADMISSION config $PKT/ROOT_SEAL_ADMISSION_V001.json                                              FIXED (guard v008 L8; FORMAT_V005 L7)
#   step-2 output root ..... /Users/bgm/Research/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007, new and empty (its parent too if absent)
#                                                                                                            FIXED (RUNBOOK_V008 L37; A105.2)
'''))
R.append(('''#                                         only if it exists with exactly the stated bytes)
''', '''#                                         only if it exists with exactly the stated bytes). The step-2 output root is never
#                                         reused: if a run stopped after step 3 created it, root removes that EMPTY directory by
#                                         hand (rmdir refuses a non-empty one) before the next attempt. This script never deletes.
'''))
R.append(('HELPER="$C3/tools/seal_steps_c3sa_c3v009.py";          HELPER_SHA="000798141398d27308d95e7a25fc64d17abe9831c47a2b27457439b7bc7922a3"',
          'HELPER="$C3/tools/seal_steps_c3sa_c3v010.py";          HELPER_SHA="%s"' % HELPER_SHA))
R.append(('''PREREG_TOR="$A/v007_final_prereg_c4/r5/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json"; PREREG_TOR_SHA="3245899f68081a48928a7242a1d9f1ee3694bb13b3f04913dcb2825104a93393"
TABLE_BYTES="$A/v007_final_prereg_c4/r5/addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md"; TABLE_BYTES_SHA="70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e"
''', '''# P11: THE text of record, ONE pin (path + sha) for steps 0, 2, 4, 4a and 10. r5 now; r6 expected (Claude4 0109): change this line only.
PREREG_TOR="$A/v007_final_prereg_c4/r5/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json"; PREREG_TOR_SHA="3245899f68081a48928a7242a1d9f1ee3694bb13b3f04913dcb2825104a93393"
# TABLE_BYTES / TABLE_BYTES_SHA (the V005 bytes the text of record's entry table was read from) are DERIVED in step 0 from the text of
# record's own entries_after_A81.addendum_read (byte_copy, sha256_at_generation). For r5 they are $A/v007_final_prereg_c4/r5/
# addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md and 70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e.
TABLE_BYTES=""; TABLE_BYTES_SHA=""
'''))
R.append(('INTERNAL_OUTPUT_ROOT="/Users/bgm/Research/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007"     # RUNBOOK_V008 L37 / template outputs\n',
          'INTERNAL_OUTPUT_ROOT="/Users/bgm/Research/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007"     # RUNBOOK_V008 L37; the template\'s 41 outputs lie under it (RP-N6)\n'))
R.append(('CONFIG="$PKT/ROOT_SEAL_ADMISSION_V001.json"\n',
          'CONFIG="$PKT/ROOT_SEAL_ADMISSION_V001.json"\nOUTPUT_ROOT_TO_CREATE="$INTERNAL_OUTPUT_ROOT"   # RP-S1 (A105.2): step 3 creates exactly this directory, new and empty\n'))
R.append(('EXPECT_CONFIG_IS_GUARD_CONFIG=True    # the config is the guard\'s own CONFIG path\n',
          'EXPECT_CONFIG_IS_GUARD_CONFIG=True    # the config is the guard\'s own CONFIG path\n'
          'OUTPUT_ROOT_IS_TEMPLATE_ROOT=1        # the root created is the template\'s output root (step 0 checks that the two strings are equal)\n'))
R.append(('''need() { local v; for v in "$@"; do if [ -z "${!v+x}" ]; then echo "REFUSE: root input $v is not set" >&2; false; fi; done; }
''', '''need() { local v; for v in "$@"; do if [ -z "${!v+x}" ]; then echo "REFUSE: root input $v is not set" >&2; false; fi; done; }
# P11: the bytes the text of record's entry table was read from, derived from the text of record itself (step 0 pins it first)
tor_table_bytes() {
  local bc; bc="$(jf "$PREREG_TOR" entries_after_A81.addendum_read.byte_copy)"; bc="${bc%% *}"
  case "$bc" in ''|/*|*..*) echo "REFUSE: the text of record's entries_after_A81.addendum_read.byte_copy: '$bc'" >&2; false;; esac
  TABLE_BYTES="$(/usr/bin/dirname "$PREREG_TOR")/$bc"
  TABLE_BYTES_SHA="$(jf "$PREREG_TOR" entries_after_A81.addendum_read.sha256_at_generation)"
}
'''))
R.append(('''  # every input from bytes (the helper also refuses non-canonical, firmlink, /private, /.vol and protected spellings)
''', '''  # P11: the ONE text-of-record pin first; the bytes its entry table was read from are derived from it
  H pin --pin "$PREREG_TOR=$PREREG_TOR_SHA"
  tor_table_bytes
  echo "  text of record $PREREG_TOR $PREREG_TOR_SHA; its table bytes $TABLE_BYTES $TABLE_BYTES_SHA"
  # every input from bytes (the helper also refuses non-canonical, firmlink, /private, /.vol and protected spellings)
'''))
R.append(('''  if [ "$ATTEMPT" = 1 ]; then H absent --path "$FROZEN"; fi
  echo "  PASS  preflight"
''', '''  if [ "$ATTEMPT" = 1 ]; then H absent --path "$FROZEN"; fi
  # RP-S1 (A105.2): the step-2 output root does not exist yet in any form (step 3 creates it); its parent chain is real directories
  if [ "$OUTPUT_ROOT_IS_TEMPLATE_ROOT" = 1 ]; then
    [ "$OUTPUT_ROOT_TO_CREATE" = "$INTERNAL_OUTPUT_ROOT" ] || { echo "REFUSE: the output root to create is not the template's output root" >&2; false; }
  fi
  H output-root --path "$OUTPUT_ROOT_TO_CREATE" --mode check --min-free-gib "$UNT_SEAL_MIN_FREE_GIB"
  echo "  PASS  preflight"
'''))
a0 = s.index('# ============================================================================ STEP 3 (B3): pre-binding output-root check + binder')
a1 = s.index('  "${PYX[@]}" "$RUNNER" --main "$BINDER=$BINDER_SHA" --call argv')
R.append((s[a0:a1], '''# ================================================= STEP 3 (B3): template outputs, the step-2 output root (RP-S1, A105.2), the binder
step3_bind() {
  STEP=3; echo "STEP 3 the step-2 output root (RP-S1, A105.2) + build-only binder: bound plan and command (SEAL_CHECKLIST_R5 L26 B3; A81 RI-25 V005@27b62183 L1269; RUNBOOK_V008 L19, L37)"
  v005_still_frozen 3
  H pin --pin "$BINDER=$BINDER_SHA" --pin "$RUNNER=$RUNNER_SHA" --pin "$TEMPLATE=$TEMPLATE_SHA" --pin "$DRIVER=$DRIVER_SHA" --pin "$FROZEN=$FROZEN_SHA" 2> "$LOGS/STEP_03_INPUTS.json"
  # RUNBOOK_V008 L37 (before binding): fresh exclusive output paths, all under the template's output root (the binder copies them, RP-N6)
  "${PYX[@]}" -c 'import json,os,sys
t=json.loads(open(sys.argv[1],"rb").read()); root=sys.argv[2]
outs=[t["launcher_log"]]+[p for c in t["calls"] for p in (c["outdir"],c["receipt"],c["receipt"]+".launch.json",c["monitor_log"])]
assert len(outs)==41==len(set(outs)) and all(o.startswith(root+"/") for o in outs), "TEMPLATE_OUTPUTS"
assert not any(os.path.lexists(o) for o in outs), "TEMPLATE_OUTPUT_EXISTS"
print(json.dumps({"template_output_root":root,"outputs_fresh":41}))' "$TEMPLATE" "$INTERNAL_OUTPUT_ROOT" > "$LOGS/STEP_03_PREBIND_TEMPLATE_OUTPUTS.json"
  # RP-S1 (A105.2): the output root, created EXCLUSIVELY as a new, empty, real directory on /System/Volumes/Data, and recorded
  run_h STEP_03_OUTPUT_ROOT output-root --path "$OUTPUT_ROOT_TO_CREATE" --mode create --min-free-gib "$UNT_SEAL_MIN_FREE_GIB"
  OR_DEV="$(jf "$LOGS/STEP_03_OUTPUT_ROOT.json" output_root.st_dev)"; OR_INO="$(jf "$LOGS/STEP_03_OUTPUT_ROOT.json" output_root.st_ino)"
  OR_REAL="$(jf "$LOGS/STEP_03_OUTPUT_ROOT.json" output_root.realpath)"; OR_FREE="$(jf "$LOGS/STEP_03_OUTPUT_ROOT.json" output_root.free.free_gib)"
  [ "$OR_REAL" = "$OUTPUT_ROOT_TO_CREATE" ]
  echo "  RECORD output root $OR_REAL: st_dev $OR_DEV (= /System/Volumes/Data), st_ino $OR_INO, empty, free $OR_FREE GiB (copy into the root launch record)"
'''))
R.append(('''  STEP=12; echo "STEP 12 exclusive-create the ROOT_SEAL_ADMISSION config (0561 1.2; A81 RI-19; FORMAT_V005 L7; SEAL_CHECKLIST_R5 L31 B8; r5 srr[10])"
''', '''  STEP=12; echo "STEP 12 exclusive-create the ROOT_SEAL_ADMISSION config; producer_allowlist = BUILD_V007's 15 rows exactly (W7-S1, A105.1; 0561 1.2; A81 RI-19; FORMAT_V005 L7; SEAL_CHECKLIST_R5 L31 B8; r5 srr[10])"
'''))
R.append(('''        --guard-sha "$GUARD_SHA" --launcher "$LAUNCHER" --launcher-sha "$LAUNCHER_SHA" --out "$CONFIG" --n-sources 15
  CFG_SHA="$(jf "$LOGS/STEP_12_CONFIG.json" config.sha256)"
  [ "$(jf "$LOGS/STEP_12_CONFIG.json" config_is_guard_CONFIG)" = "$EXPECT_CONFIG_IS_GUARD_CONFIG" ]
''', '''        --guard-sha "$GUARD_SHA" --launcher "$LAUNCHER" --launcher-sha "$LAUNCHER_SHA" --out "$CONFIG"
  CFG_SHA="$(jf "$LOGS/STEP_12_CONFIG.json" config.sha256)"
  [ "$(jf "$LOGS/STEP_12_CONFIG.json" config_is_guard_CONFIG)" = "$EXPECT_CONFIG_IS_GUARD_CONFIG" ]
  # W7-S1 (A105.1, A78 N2): the WRITTEN config, re-read from its bytes: exactly BUILD_V007's 15 rows, byte-equal, in table order
  run_h STEP_12_CONFIG_W7_S1 check-config-allowlist --config "$CONFIG" --config-sha "$CFG_SHA" --build "$BUILD" --build-sha "$BUILD_SHA"
'''))
R.append(('''summary() {
  STEP=summary
''', '''summary() {
  STEP=summary
  # RP-S1: at the end of the assembly the output root is still the recorded, empty directory
  H output-root --path "$OUTPUT_ROOT_TO_CREATE" --mode verify --expect-dev "$OR_DEV" --expect-ino "$OR_INO" 2> "$LOGS/FINAL_OUTPUT_ROOT_STILL_EMPTY.json"
'''))
R.append(('"schema":"C3SA_ROOT_SEAL_ASSEMBLY_SUMMARY_V001"', '"schema":"C3SA_ROOT_SEAL_ASSEMBLY_SUMMARY_V002"'))
R.append(('''                "verify the bound plan and command shas from bytes immediately before running the command (A81 RI-25; SEAL_CHECKLIST_R5 C2)",
''', '''                "verify the bound plan and command shas from bytes immediately before running the command (A81 RI-25; SEAL_CHECKLIST_R5 C2)",
                "copy the output-root record (logs/STEP_03_OUTPUT_ROOT.json: st_dev, realpath, free space) into the root launch record and re-check that the root is still empty just before the launch (RP-S1, A105.2)",
                "start step2_disk_watch.sh at the launch (A105.3; a convenience, not part of the seal)",
'''))
R.append(('''    config "$CONFIG $CFG_SHA" receipt "$RECEIPT $RC_SHA"
}
''', '''    config "$CONFIG $CFG_SHA" receipt "$RECEIPT $RC_SHA" \\
    output_root "$OUTPUT_ROOT_TO_CREATE st_dev=$OR_DEV st_ino=$OR_INO free_gib_at_creation=$OR_FREE"
}
'''))
for o, n in R:
    assert s.count(o) == 1, (o[:90], s.count(o))
    s = s.replace(o, n)
assert '--n-sources' not in s and 'STEP_03_PREBIND_OUTPUT_ROOT' not in s
out = s.encode('utf-8')
with open(C3 + '/ROOT_SEAL_STEPS_c3v009.sh', 'xb') as f:
    f.write(out)
print('ROOT_SEAL_STEPS_c3v009.sh', hashlib.sha256(out).hexdigest(), len(out))
