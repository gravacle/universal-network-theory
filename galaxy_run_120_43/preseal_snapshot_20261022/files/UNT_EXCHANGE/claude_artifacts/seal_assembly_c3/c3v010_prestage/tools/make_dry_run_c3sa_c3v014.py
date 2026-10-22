# Claude3 seal-assembly builder (0626), c3v014 (c3v011, for ROOT_SEAL_STEPS_c3v027.sh; root 0667 A123): S10 is keyed to the TARGET's own
# MANIFEST_GATES line (c3v013 matched the draft e5967bb9 literally), and the stand-in MAN must equal the target's manifest with identity_runs emptied
# and a FIXTURE note (same schema, cases, rpair and gates, key for key), so the dry-run gates-only evaluates exactly the seal's gate records.
# c3v013 (c3v010 FINAL, for ROOT_SEAL_STEPS_c3v024.sh): S29 is REMOVED; no stand-in of any kind remains
# (only the published scratch substitutions S01-S18, the step-9 stub S15, the D-10 allowance S16/S16b and, in pass B, S23).
# c3v012 (c3v010 near-final, for ROOT_SEAL_STEPS_c3v022.sh): S26 and S27 are REMOVED (registry V010 and
# disclosures V003 are real); + S29 (both passes: the B7 successor-custody record is PENDING; the dry run's labelled fixture stands in).
# c3v011 (c3v010 pre-stage, for ROOT_SEAL_STEPS_c3v021.sh): + S26 (both passes: the registry V010 is
# PENDING, so V009 stands in, labelled; V009 loads on r14) and S27 (both passes: root disclosures V003 is PENDING, so V002 stands in, labelled).
# Both are STAND-INS that exist only so the dry run can execute; the real script refuses both placeholders in step 0.
# c3v010 (c3v009 pre-stage; for the WIRED successor ROOT_SEAL_STEPS_c3v020.sh): S24 and S25 are
# REMOVED, so the dry run runs the real tool 4 v004 with both manual-disclosure flags; everything else is c3v009's substitution set.
# c3v009 (for ROOT_SEAL_STEPS_c3v018.sh, A110/A111): + S24 (both passes: v003 tool 4 and its
# SELECTED file stand in for the PENDING tool 4 v004, P13, so step 0 does not refuse) and S25 (both passes: step 10 drops
# --manual-disclosures, which v003 tool 4 does not take). The disclosures file itself is the REAL root file, pre-checked in step 0.
# c3v008 (for ROOT_SEAL_STEPS_c3v015.sh, seal tools v003): S07, S08 and S21 are removed (the real
# v003 tools and SELECTED file are wired); S15 also writes a labelled B6-form VALIDITY_ONLY.json; S16 and S16b (both passes) apply only
# the D-10 allowance; S23 (pass B) gives the tools no dispositions file.
# c3v007 (for ROOT_SEAL_STEPS_c3v014.sh): S19 and S20 are removed: the root script now wires the
# REAL prereg r6 and its SELECTED file (Claude4 SELECTED_R6_C4V001 7200acd9); only the v003 stand-in (S21) remains.
# c3v006 (for ROOT_SEAL_STEPS_c3v012.sh, FROM_CODEX/0644): S22 is removed (A107 rules the C-04
# exclusions, so pass B needs no C-04 exception).
# Claude3 seal-assembly builder (0626), c3v005 (for ROOT_SEAL_STEPS_c3v011.sh, FROM_CODEX/0643): adds S19-S21 (r5 and labelled
# SELECTED fixtures stand in for the unpublished r6 and v003) and S22 (pass B: a C-04 REFUSE is logged, not fatal).
# c3v004 (for ROOT_SEAL_STEPS_c3v009.sh, FROM_CODEX/0642): adds S17 (the step-2 output root
# to create -> scratch; the REAL root is never created by a dry run) and S18 (that scratch root is not the template output root).
# c3v003 (for ROOT_SEAL_STEPS_c3v007.sh: S08 is the single dispositions line; S16 targets the
# runner-based T3_RUN / T4_RUN lines). c3v002 (for c3v003-c3v006): the step-9 stub also sets VS_SHA from its row scan:
# derive a DRY-RUN script from the root script by an explicit substitution set
# (each old string must occur exactly once). Writes ROOT_SEAL_STEPS_DRYRUN_<PASS>.sh and SUBSTITUTIONS_<PASS>.json (exclusive).
import hashlib, json, sys
ROOT, ROOT_SHA, PASSDIR, PASS, FIXT, MAN, MAN_SHA, SHIM = sys.argv[1:9]
src = open(ROOT).read()
assert hashlib.sha256(src.encode()).hexdigest() == ROOT_SHA, 'root script bytes changed'
import re as _re
_MGM = _re.search(r'^MANIFEST_GATES="([^"]*)"; MANIFEST_GATES_SHA="([0-9a-f]{64})"$', src, _re.M); assert _MGM, 'MANIFEST_GATES line'
_MGL = _MGM.group(0); _TMP = _MGM.group(1).replace('$C3', '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3', 1)
_tb = open(_TMP, 'rb').read(); assert hashlib.sha256(_tb).hexdigest() == _MGM.group(2), 'target manifest bytes'
_sb = open(MAN, 'rb').read(); assert hashlib.sha256(_sb).hexdigest() == MAN_SHA, 'stand-in bytes'
_tm, _sm = json.loads(_tb), json.loads(_sb)
assert set(_sm) == set(_tm) and all(_sm[k] == _tm[k] for k in ('schema', 'cases', 'rpair')) and list(_sm['gates'].items()) == list(_tm['gates'].items()), 'STANDIN_GATES_ARE_NOT_THE_TARGET_MANIFEST_GATES'
assert _sm['identity_runs'] == {} and _sm['note'].startswith('FIXTURE_DRY_RUN_ONLY'), 'STANDIN_NOT_A_LABELLED_FIXTURE_WITHOUT_RUN_TREES'
S = [
 ('S01 frozen copy -> scratch', 'FROZEN="$CTRL/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md"',
  'FROZEN="%s/scratch_ctrl/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md"' % PASSDIR),
 ('S02 seal folder -> scratch', 'SEAL_DIR="$CTRL/V007_SEAL_ASSEMBLY$SFX"', 'SEAL_DIR="%s/scratch_ctrl/V007_SEAL_ASSEMBLY$SFX"' % PASSDIR),
 ('S03 bound plan -> scratch binder folder', 'BOUND_PLAN="$PKT/P128/LAUNCH_PLAN_V011_CX3V001_BOUND_R5_V007_SEAL$SFX.json"',
  'BOUND_PLAN="%s/scratch_pkt/P128/LAUNCH_PLAN_V011_CX3V001_BOUND_R5_V007_SEAL$SFX.json"' % PASSDIR),
 ('S04 bound command -> scratch binder folder', 'BOUND_COMMAND="$PKT/P128/LAUNCH_COMMAND_V011_CX3V001_BOUND_R5_V007_SEAL$SFX.txt"',
  'BOUND_COMMAND="%s/scratch_pkt/P128/LAUNCH_COMMAND_V011_CX3V001_BOUND_R5_V007_SEAL$SFX.txt"' % PASSDIR),
 ('S05 admission config -> scratch', 'CONFIG="$PKT/ROOT_SEAL_ADMISSION_V001.json"', 'CONFIG="%s/scratch_pkt/ROOT_SEAL_ADMISSION_V001.json"' % PASSDIR),
 ('S06 binder -> byte-identical scratch copy (HERE = scratch_pkt; same sha)', 'BINDER="$PKT/bind_sealed_launch_plan_cx1v001.py";',
  'BINDER="%s/scratch_pkt/bind_sealed_launch_plan_cx1v001.py";' % PASSDIR),
 ('S09 seal inputs folder -> scratch', 'SEAL_INPUTS_DIR="$CTRL/V007_SEAL_ASSEMBLY_INPUTS"', 'SEAL_INPUTS_DIR="%s/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS"' % PASSDIR),
 ('S10 gates-only manifest -> stand-in (no identity-run tree, no case)',
  _MGL,
  'MANIFEST_GATES="%s"; MANIFEST_GATES_SHA="%s"' % (MAN, MAN_SHA)),
 ('S11 draft documents the real paths, the dry run uses scratch', 'DRAFT_PATHS_MUST_MATCH=1 ', 'DRAFT_PATHS_MUST_MATCH=0 '),
 ('S12 the scratch config is not the guard CONFIG path', 'EXPECT_CONFIG_IS_GUARD_CONFIG=True ', 'EXPECT_CONFIG_IS_GUARD_CONFIG=False '),
 ('S13 step 8 fence mode dryrun (refuses all runs_ext/UVT_*; C5H dirs redirected to a stand-in)', 'STEP8_MODE=root ', 'STEP8_MODE=dryrun '),
 ('S14 step 8 stand-in for C5H_REGISTERED_RUN_DIRS', 'STEP8_STANDIN=""', 'STEP8_STANDIN="%s/C5H_STANDIN_REGISTERED_DIR"' % FIXT),
]
S.append(('S17 the step-2 output root to create -> scratch (RP-S1; the REAL root is never created by a dry run); its parent UNT_INTERNAL_RUNS is absent at setup, as it is on disk', 'OUTPUT_ROOT_TO_CREATE="$INTERNAL_OUTPUT_ROOT"', 'OUTPUT_ROOT_TO_CREATE="%s/scratch_internal/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007"' % PASSDIR))
S.append(('S18 the scratch root is not the template output root (the template outputs stay the real strings and are only checked absent; nothing is created there)', 'OUTPUT_ROOT_IS_TEMPLATE_ROOT=1 ', 'OUTPUT_ROOT_IS_TEMPLATE_ROOT=0 '))
old9 = src[src.index('step9_validity_c5h() {'):src.index('# =========================================================================== STEP 10')]
assert 'RUNNER' in old9 and 'validity-only' in old9
new9 = '''step9_validity_c5h() {
  STEP=9; echo "STEP 9 STUBBED (dry run): the sealed compare is NOT executed; no C5H path is opened, stat'ed or resolved"
  v005_still_frozen 9
  cat > "$VALIDITY_STDOUT" <<'STUBEOF'
{"schema": "DRY_RUN_FIXTURE_NOT_A_COMPARE_OUTPUT", "fixture": "STUB for ROOT_SEAL_STEPS step 9 (Claude3 0626 dry run): --validity-only --case C5H was NOT run", "cases": {"C5H": {"valid": false, "codes": ["DRY_RUN_STUB_NOT_EXECUTED"]}}, "no_row_value_shown": true}
STUBEOF
  echo "  STUB  E_SEAL1_VALIDITY_ONLY_C5H.stdout.txt = booleans fixture"
  run_h STEP_09_ROW_SCAN row-value-scan --path "$VALIDITY_STDOUT"
  VS_SHA="$(jf "$LOGS/STEP_09_ROW_SCAN.json" e_seal1.sha256)"
  /bin/mkdir "$VALIDITY_OUTDIR"   # the B6 body v003 tool 4 reads: a labelled fixture in the compare's own form (schema, blinded, test_mode, sha, mode, cases)
  "${PYX[@]}" -c 'import json,sys
g=json.loads(open(sys.argv[1],"rb").read()); assert g["schema"].endswith("_GATES_ONLY")
d={"schema": g["schema"][:-len("_GATES_ONLY")] + "_VALIDITY_ONLY", "blinded": True, "test_mode": False, "script_sha256": sys.argv[2],
   "route_a_mode": g["route_a_mode"], "cases": {"C5H": {"valid": False, "codes": ["DRY_RUN_STUB_NOT_EXECUTED"]}},
   "fixture": "DRY-RUN FIXTURE (Claude3): ROOT_SEAL_STEPS step 9 was NOT executed; no C5H path was opened, stat-ed or resolved"}
open(sys.argv[3], "x").write(json.dumps(d, indent=1) + "\\n")' "$GJ_PATH" "$SC_SHA" "$VALIDITY_OUTDIR/VALIDITY_ONLY.json"
  echo "  STUB  VALIDITY_ONLY.json = labelled B6-form fixture (cases C5H, valid false)"
  VJ_PATH="$VALIDITY_OUTDIR/VALIDITY_ONLY.json"; VJ_SHA="$(sha_of "$VJ_PATH")"
}

'''
S.append(('S15 step 9 STUBBED: booleans stdout fixture plus a labelled B6-form VALIDITY_ONLY.json; the compare and the C5H run are never touched', old9, new9))
t3 = 'T3_RUN=("${PYX[@]}" "$RUNNER" "${RUN_MODS_COMMON[@]}" --module "check_frozen_addendum_c4v003=$T1=$T1_SHA" --module "check_sealed_compare_c4v003=$T2=$T2_SHA" --main "$T3=$T3_SHA" --call main --)'
t4 = 'T4_RUN=("${PYX[@]}" "$RUNNER" "${RUN_MODS_COMMON[@]}" --module "check_frozen_addendum_c4v003=$T1=$T1_SHA" --module "check_sealed_compare_c4v003=$T2=$T2_SHA" --module "check_slot_fill_c4v003=$T3=$T3_SHA" --main "$T4=$T4_SHA" --call main --)'
S.append(('S16 (both passes) tools 3 and 4 run through the DRY-RUN SHIM: the pinned runner plus ONE patch, the D-10 allowance for the tool 1 '
          'runs inside them (the FROZEN copy is in scratch, never at path_to_be); NOT a seal tool', t3 + '\n' + t4, (t3 + '\n' + t4).replace('"$RUNNER"', '"%s"' % SHIM)))
t1 = '  "${T1_RUN[@]}" --prereg "$PREREG_TOR" --frozen "$FROZEN" --expect-frozen-sha "$V005_FINAL_SHA" --addendum-at-text-of-record "$TABLE_BYTES" \\'
S.append(('S16b (both passes) the direct tool 1 run gets its own --allow-open-copy-for-dry-run (D-10 -> its DRY_RUN note); --expect-frozen-sha stays',
          t1, t1[:-1] + '--allow-open-copy-for-dry-run \\'))
# c3v010: NO S24 / S25. The target is the WIRED successor (script c3v020): tool 4 v004 is pinned from Claude4's SELECTED file, and step 10
# passes BOTH --manual-disclosures and --manual-disclosures-sha256 to it unchanged (Codex1 0118 (ii): a dry run on v003 without the
# flags cannot establish embedding). Refuse a target that still carries the P13 PENDING block or lacks the two flags.
assert 'V004_SELECTED="PENDING' not in src and 'T4_SHA="PENDING"' not in src, 'TARGET_STILL_P13_PENDING (use generator c3v009 for c3v019)'
assert src.count('--manual-disclosures "$DISCLOSURES" --manual-disclosures-sha256 "$DISCLOSURES_SHA"') == 1, 'TARGET_STEP10_LACKS_BOTH_DISCLOSURE_FLAGS'
# c3v013: NO stand-in is left. The target (c3v024) pins every value itself; refuse a target that still has a PENDING pin.
_pins = src[src.index('# ============================================================================================================ PINS'):src.index('# ---------------------------------------------------------------------------------------------------- OUTPUTS')]
assert '="PENDING' not in _pins and '_SHA="PENDING"' not in _pins, 'TARGET_HAS_A_PENDING_PIN'
if PASS == 'B':
    S.append(('S23 (pass B only) the tools get NO dispositions file (README_SEAL_TOOLS_V003: optional when L u CH is empty, as for r6); the helper still checks the pinned entries:[] object',
              '  COV_ARGS=(--dispositions "$UNT_SEAL_DISPOSITIONS_PATH" --dispositions-sha "$UNT_SEAL_DISPOSITIONS_SHA256")   # SA-CX1-B3: one pinned file, tools 1, 3, 4',
              '  COV_ARGS=()   # DRY RUN pass B (S23): no dispositions file to the tools'))
out = src
for sid, o, n in S:
    assert out.count(o) == 1, (sid, out.count(o))
    out = out.replace(o, n)
dst = '%s/ROOT_SEAL_STEPS_DRYRUN_%s.sh' % (PASSDIR, PASS)
with open(dst, 'x') as f:
    f.write(out)
subs = {'schema': 'C3SA_DRY_RUN_SUBSTITUTIONS_V001', 'root_script': {'path': ROOT, 'sha256': ROOT_SHA},
        'dry_run_script': {'path': dst, 'sha256': hashlib.sha256(out.encode()).hexdigest()},
        'substitutions': [{'id': sid, 'old': o if len(o) < 400 else o[:400] + '...(function body; see the diff)', 'new': n if len(n) < 400 else n[:400] + '...'} for sid, o, n in S]}
with open('%s/SUBSTITUTIONS_%s.json' % (PASSDIR, PASS), 'x') as f:
    f.write(json.dumps(subs, indent=1) + '\n')
print(json.dumps({'dry_run_script': subs['dry_run_script'], 'n_substitutions': len(S)}))
