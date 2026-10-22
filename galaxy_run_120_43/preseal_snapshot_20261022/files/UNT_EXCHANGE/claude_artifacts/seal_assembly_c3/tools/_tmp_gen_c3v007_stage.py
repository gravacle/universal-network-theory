# Claude3 seal-assembly builder (0626), c3v006 (for ROOT_SEAL_STEPS_c3v012.sh, FROM_CODEX/0644): S22 is removed (A107 rules the C-04
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
 ('S07 seal tools status (v001 placeholders are what exists)', 'SEAL_TOOLS_STATUS="PENDING_V003__V001_PLACEHOLDERS"', 'SEAL_TOOLS_STATUS="DRYRUN__V001_PLACEHOLDERS"'),
 ('S08 dispositions -> the v001 bare-name form (DRY RUN ONLY: the v001 placeholders cannot take the pinned dispositions file)',
  '  COV_ARGS=(--dispositions "$UNT_SEAL_DISPOSITIONS_PATH" --dispositions-sha "$UNT_SEAL_DISPOSITIONS_SHA256")   # SA-CX1-B3: one pinned file, tools 1, 3, 4',
  '  COV_ARGS=(--covered-later "$COVERED_NAMES")   # DRY RUN: v001 placeholders take bare names only; the root script passes the pinned dispositions file'),
 ('S09 seal inputs folder -> scratch', 'SEAL_INPUTS_DIR="$CTRL/V007_SEAL_ASSEMBLY_INPUTS"', 'SEAL_INPUTS_DIR="%s/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS"' % PASSDIR),
 ('S10 gates-only manifest -> stand-in (no identity-run tree, no case)',
  'MANIFEST_GATES="$C3/MANIFEST_GATES_ONLY_DRAFT_C3SA.json"; MANIFEST_GATES_SHA="e5967bb9901fda39703553c5c02b4d11a580ef8456f6c0b7d315ee4c750f09da"',
  'MANIFEST_GATES="%s"; MANIFEST_GATES_SHA="%s"' % (MAN, MAN_SHA)),
 ('S11 draft documents the real paths, the dry run uses scratch', 'DRAFT_PATHS_MUST_MATCH=1 ', 'DRAFT_PATHS_MUST_MATCH=0 '),
 ('S12 the scratch config is not the guard CONFIG path', 'EXPECT_CONFIG_IS_GUARD_CONFIG=True ', 'EXPECT_CONFIG_IS_GUARD_CONFIG=False '),
 ('S13 step 8 fence mode dryrun (refuses all runs_ext/UVT_*; C5H dirs redirected to a stand-in)', 'STEP8_MODE=root ', 'STEP8_MODE=dryrun '),
 ('S14 step 8 stand-in for C5H_REGISTERED_RUN_DIRS', 'STEP8_STANDIN=""', 'STEP8_STANDIN="%s/C5H_STANDIN_REGISTERED_DIR"' % FIXT),
]
S.append(('S17 the step-2 output root to create -> scratch (RP-S1; the REAL root is never created by a dry run); its parent UNT_INTERNAL_RUNS is absent at setup, as it is on disk', 'OUTPUT_ROOT_TO_CREATE="$INTERNAL_OUTPUT_ROOT"', 'OUTPUT_ROOT_TO_CREATE="%s/scratch_internal/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007"' % PASSDIR))
S.append(('S18 the scratch root is not the template output root (the template outputs stay the real strings and are only checked absent; nothing is created there)', 'OUTPUT_ROOT_IS_TEMPLATE_ROOT=1 ', 'OUTPUT_ROOT_IS_TEMPLATE_ROOT=0 '))
import os
def _fx(name):
    p = FIXT + '/' + name; b = open(p, 'rb').read(); return p, hashlib.sha256(b).hexdigest()
R6F, R6S = _fx('R6_SELECTED_DRYRUN_FIXTURE.json'); V3F, V3S = _fx('V003_SELECTED_DRYRUN_FIXTURE.json')
S.append(('S21 DRY RUN ONLY: the v003 SELECTED file -> a labelled fixture naming the v001 placeholders (exercises selected-names)',
          'V003_SELECTED="PENDING_V003_SELECTED_FILE"; V003_SELECTED_SHA="PENDING_V003_SELECTED_FILE_SHA"',
          'V003_SELECTED="%s"; V003_SELECTED_SHA="%s"   # DRY RUN (S21): labelled fixture' % (V3F, V3S)))
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
}

'''
S.append(('S15 step 9 STUBBED: booleans fixture; the compare and the C5H run are never touched', old9, new9))
if PASS == 'B':
    t3 = 'T3_RUN=("${PYX[@]}" "$RUNNER" "${RUN_MODS_COMMON[@]}" --module "check_frozen_addendum_c4v001=$T1=$T1_SHA" --module "check_sealed_compare_c4v001=$T2=$T2_SHA" --main "$T3=$T3_SHA" --call main --)'
    t4 = 'T4_RUN=("${PYX[@]}" "$RUNNER" "${RUN_MODS_COMMON[@]}" --module "check_frozen_addendum_c4v001=$T1=$T1_SHA" --module "check_sealed_compare_c4v001=$T2=$T2_SHA" --module "check_slot_fill_c4v001=$T3=$T3_SHA" --main "$T4=$T4_SHA" --call main --)'
    S.append(('S16 (pass B only) tools 3 and 4 run through the DRY-RUN SHIM (the pinned runner plus two in-process constant patches: text '
              'of record r5; ddo_gas_M_s), so steps 4a-13 run; NOT a seal tool', t3 + '\n' + t4,
              (t3 + '\n' + t4).replace('"$RUNNER"', '"%s"' % SHIM)))
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
