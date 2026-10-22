#!/bin/bash
# setup_dry_run_c3sa_c3v013.sh: Claude3 (c3v009; c3v012 never ran a dry run: its pin reader expanded $C3 only, so the real c3v020
# ($A/... spellings) failed the gate; c3v013 expands $C3 and $A). c3v012: (c3v009 pre-stage, item (b2); for the WIRED successor ROOT_SEAL_STEPS_c3v020.sh): generator c3v010
# (NO S24/S25: the real tool 4 v004 runs with BOTH --manual-disclosures and --manual-disclosures-sha256, Codex1 0118 (ii)). Before the
# passes it GATES on c3v009_prestage/tools/check_tool4_imports_c3v003.py (tool 4's imports = the T4_RUN modules; pins role-qualified;
# every flag the script passes is a tool-4 flag). The RUN files derive from dry run 11 (20261019T013957Z). After the passes it shows,
# per pass: both flags on the step-10 tool-4 call of the dry-run script, the step-11 STEP_11_DISCLOSURES_VERBATIM verdict, and where
# the disclosures sit in the written SEAL_RECORD (helper locate form). The target script and the dry-run parent folder are arguments.
# c3v011: Claude3 (A110/A111, script c3v018; supersedes c3v010, never run, which kept a no-op copy of the old sed):
# generator c3v009 (S24/S25: v003 tool 4 stands in for the PENDING tool 4 v004); the RUN files derive from dry run 10 (20261019T010953Z)
# minus the four inputs A111 removed (UNT_SEAL_DRIVER_CHECK_RECORD_PATH, _SHA256, UNT_SEAL_RULING_EPS_NGC, UNT_SEAL_RULING_I1T_NGC); the
# fixtures are regenerated exactly as c3v009 does, and the RUN-file check below proves they equal dry run 10's.
# c3v009: Claude3 (seal tools v003; + the three B7 fixtures in v003 C4V002 forms, labelled). Sets up and runs dry-run passes A and B of the root script named by $3.
# Everything it creates lies under a NEW seal_assembly_c3/dry_run_<UTC>/ folder (mkdir / noclobber / open 'x'); it never writes in
# a real seal location. Step 9 is STUBBED by S15; the step-2 output root is a scratch path (S17); r5 and labelled SELECTED fixtures
# stand in for the unpublished prereg r6 and seal tools v003 (S19-S21).
# usage: setup_dry_run_c3sa_c3v013.sh ROOT_SCRIPT_PATH ROOT_SCRIPT_SHA OPEN_V005_SHA DRY_PARENT_DIR
set -uo pipefail; set -o noclobber
C3=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3; A=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ROOTS=$1; ROOTS_SHA=$2; WANT_V005=$3; DRYP=$4; W=$C3/c3v009_prestage
GEN=$W/tools/make_dry_run_c3sa_c3v010.py; SHIM=$C3/tools/dryrun_tool_shim_c3sa_c3v007.py; CHK=$W/tools/check_tool4_imports_c3v003.py
[ "$(shasum -a 256 $GEN | cut -d' ' -f1)" = ab01df672987408cb18954db79698da8051097d1fd6d8ddcc66522e028fedf4c ] || { echo "generator c3v010 bytes differ"; exit 1; }
[ "$(shasum -a 256 $CHK | cut -d' ' -f1)" = 272d9cf58d6cb3f2768745c68425f35db1b161a0c3e39d1df478ab43996ee17a ] || { echo "import check c3v003 bytes differ"; exit 1; }
[ "$(shasum -a 256 $SHIM | cut -d' ' -f1)" = df19ac11401d76593f3b7a03474a31c955a77ec5585475e2a5bc9588027fd135 ] || { echo "shim bytes differ"; exit 1; }
[ "$(shasum -a 256 $ROOTS | cut -d' ' -f1)" = "$ROOTS_SHA" ] || { echo "root script bytes differ"; exit 1; }
pv() { /usr/bin/sed -n "s/.*$1=\"\([^\"]*\)\".*/\1/p" $ROOTS | head -n 1 | /usr/bin/sed -e "s#^\$C3/#$C3/#" -e "s#^\$A/#$A/#"; }   # the script's own pins, $C3 / $A expanded (c3v013)
V4S=$(pv V004_SELECTED); V4H=$(pv V004_SELECTED_SHA); V4C=$(pv V004_SELECTED_SCHEMA); HLP=$(pv HELPER); HLS=$(pv HELPER_SHA)
case "$V4S $V4H $V4C" in *PENDING*) echo "the target is still P13-PENDING: not a wired successor"; exit 1;; esac
GATE=$($PY -I -B $CHK $HLP=$HLS $ROOTS=$ROOTS_SHA $V4S=$V4H $V4C $A/v007_final_prereg_c4/seal_tools_v003/SELECTED_SEAL_TOOLS_V003_C4V001.json=cf7e5b2f1b3daf55c485ada1c869bc7249040a8db8202eb1b1a90bebe1431305 UNT_V007_SELECTED_SEAL_TOOLS_C4V001)
GRC=$?; echo "$GATE" | grep -E '"verdict"|"code"|missing_from|extra_in'; [ $GRC = 0 ] || { echo "GATE: the tool-4 import/CLI check refused; no dry run"; exit 1; }
OPEN="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md"
OS=$(shasum -a 256 "$OPEN" | cut -d' ' -f1); [ "$OS" = "$WANT_V005" ] || { echo "open V005 is $OS, not $WANT_V005"; exit 1; }
UTC=$(date -u +%Y%m%dT%H%M%SZ); DRY=$DRYP/dry_run_$UTC; D9=$C3/dry_run_20261019T002133Z; D10=$C3/dry_run_20261019T010953Z; D11=$C3/dry_run_20261019T013957Z
mkdir $DRY $DRY/fixtures $DRY/fixtures/C5H_STANDIN_REGISTERED_DIR || exit 1
for f in KEY_EQUIVALENCE_MAP_FIXTURE.json NEW_ITEM_LIST_FIXTURE.json SUCCESSOR_CUSTODY_FIXTURE.json CASCADE_MAP_R5_ADDENDUM_FIXTURE.json MANIFEST_GATES_ONLY_STANDIN.json; do
  $PY -I -B -c "import sys; open(sys.argv[2],'xb').write(open(sys.argv[1],'rb').read())" $D9/fixtures/$f $DRY/fixtures/$f || exit 1
done
DSHA=$($PY -I -B - "$OPEN" "$OS" "$DRY" "$A" <<'PYEOF'
import sys, json, hashlib, re
OPEN, OS, DRY, A = sys.argv[1:5]
fb = open(OPEN, 'rb').read(); assert hashlib.sha256(fb).hexdigest() == OS
starts = [0] + [m.end() for m in re.finditer(b'\n', fb)]
heads = [s for s in starts if s < len(fb) and fb.startswith(b'## ', s)]
def sec(e):
    s = [h for h in heads if fb.startswith(('## %s:' % e).encode(), h)][0]; n = [h for h in heads if h > s]
    return fb[s:(n[0] if n else len(fb))]
later = ['A%d' % n for n in sorted({int(m.group(1)) for m in re.finditer(rb'^## A(\d{1,3}):', fb, re.M)}) if n > 106]   # r6's table ends at A106: none
lab = 'DRY-RUN FIXTURE (labelled; not a disposition of record): '
reasons = {'A102': lab + 'A102 rules the r12 review split and orders r13', 'A103': lab + 'A103 reassigns review queues',
           'A104': lab + 'A104 names r13 the compare of record', 'A105': lab + 'A105 rules the BUILD_V007 delta',
           'A106': lab + 'A106 approves prereg r6, rules the seal-tool scope and closes V005'}
d = {'schema': 'UNT_V007_LATER_ENTRY_DISPOSITIONS_C4V001', 'frozen_addendum_sha256': OS,
     'entries': [{'entry': e, 'disposition': 'no_change', 'reason': reasons.get(e, lab + e), 'section_sha256': hashlib.sha256(sec(e)).hexdigest()} for e in later]}
t = json.dumps(d, indent=1) + '\n'
open(DRY + '/fixtures/_DISPOSITIONS_V003_OBJECT.tmp.json', 'x').write(t)
def pinj(p):
    return {'path': p, 'sha256': hashlib.sha256(open(p, 'rb').read()).hexdigest()}
r5 = A + '/v007_final_prereg_c4/r5/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json'
r6f = {'schema': 'DRY_RUN_FIXTURE_NOT_A_SELECTED_FILE', 'fixture': 'Claude3 0643 dry run ONLY: stands in for Claude4 prereg r6 SELECTED file, '
       'which is not published; it names r5. Never use at the real seal.', 'selected_text_of_record': pinj(r5)}
td = A + '/v007_final_prereg_c4/seal_tools/'
v3f = {'schema': 'DRY_RUN_FIXTURE_NOT_A_SELECTED_FILE', 'fixture': 'Claude3 0643 dry run ONLY: stands in for Claude4 seal tools v003 SELECTED '
       'file, which is not published; it names the v001 placeholders. Never use at the real seal.',
       'tools': [pinj(td + n) for n in ('seal_common_c4v001.py', 'check_frozen_addendum_c4v001.py', 'check_sealed_compare_c4v001.py',
                                         'check_slot_fill_c4v001.py', 'build_seal_record_c4v001.py')]}
for n, o in ():   # c3v006: no stand-in fixtures (the real r6 and v003 SELECTED files are wired)
    open(DRY + '/fixtures/' + n, 'x').write(json.dumps(o, indent=1) + '\n')
print(hashlib.sha256(t.encode()).hexdigest())
PYEOF
) || exit 1
echo "dispositions fixture $DSHA"
CSHA=$($PY -I -B -c '
import json, sys, hashlib
cm = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/CASCADE_MAP_R5_C2V001.json"
h = hashlib.sha256(open(cm, "rb").read()).hexdigest(); assert h == "a7281e10a15c7f51eae8b5d5336648c1d0a7d04a8cf932b3860c9eba3636a880"
d = {"fixture": "FIXTURE_DRY_RUN_ONLY (Claude3, v003 dry run): a labelled stand-in for root P7 CASCADE_MAP_R5_ADDENDUM; never use at the real seal",
     "extends_cascade_map": {"path": cm, "sha256": h}, "basis": "A69; RI-32; r5 seal_record_requirements[9]; v003 tool 3 requires the addendum to name the map it extends"}
t = json.dumps(d, indent=1) + "\n"; open(sys.argv[1], "x").write(t); print(hashlib.sha256(t.encode()).hexdigest())' $DRY/fixtures/CASCADE_MAP_R5_ADDENDUM_FIXTURE_V002.json) || exit 1
echo "cascade fixture $CSHA"
B7SHAS=$($PY -I -B -c '
import json, sys, hashlib
F = sys.argv[1]; lab = "FIXTURE_DRY_RUN_ONLY (Claude3, v003 dry run): a labelled stand-in for a root B7 input (GAP-17); never use at the real seal"
impl = "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/COMPARE_V007_IMPL_R13.md"
ih = hashlib.sha256(open(impl, "rb").read()).hexdigest(); assert ih == "274f7049ece71339d39395b434e7e08bfab33067e3e600d17b4a3bde43fb74a3"
docs = [("KEY_EQUIVALENCE_MAP_FIXTURE_V002.json", {"schema": "UNT_V007_SEAL_KEY_EQUIVALENCE_MAP_C4V002", "key_equivalence_map": [],
         "note": lab + "; equals the case block 76309ae3 key_equivalence_map ([])"}),
        ("NEW_ITEM_LIST_FIXTURE_V002.json", {"schema": "UNT_V007_SEAL_NEW_ITEM_DISPOSITIONS_C4V002", "compare_impl": {"path": impl, "sha256": ih}, "items": [],
         "note": lab + "; r13 declares no NEW item (erratum E_R6_1)"}),
        ("SUCCESSOR_CUSTODY_FIXTURE_V002.json", {"schema": "UNT_V007_SEAL_RAW_SUCCESSOR_CUSTODY_C4V002", "identity_run": "Z2",
         "driver_sha256": "b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6", "stages_total": 1, "stages_successor": 1, "verdict": "PASS",
         "method": "DRY-RUN FIXTURE: NOT an observation; the real raw successor-custody record is root input P6 (A59; root UVT read)", "note": lab})]
out = []
for n, d in docs:
    t = json.dumps(d, indent=1) + "\n"; open(F + "/" + n, "x").write(t); out.append(hashlib.sha256(t.encode()).hexdigest())
print(" ".join(out))' $DRY/fixtures) || exit 1
KSHA=${B7SHAS%% *}; rest=${B7SHAS#* }; NSHA=${rest%% *}; USHA=${rest#* }
echo "B7 fixtures $KSHA $NSHA $USHA"
for P in A B; do
  mkdir $DRY/pass$P $DRY/pass$P/scratch_ctrl $DRY/pass$P/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS $DRY/pass$P/scratch_pkt $DRY/pass$P/scratch_pkt/P128 $DRY/pass$P/scratch_internal || exit 1
  $PY -I -B -c "import sys,hashlib; b=open(sys.argv[1],'rb').read(); assert hashlib.sha256(b).hexdigest()=='f3e4e2beeb8f1cb151892fd903b889c471cea58fea1b67c72552137d037575ca'; open(sys.argv[2],'xb').write(b)" $A/v007_launch_packet_cx1/bind_sealed_launch_plan_cx1v001.py $DRY/pass$P/scratch_pkt/bind_sealed_launch_plan_cx1v001.py || exit 1
  $PY -I -B -c "import sys; open(sys.argv[2],'xb').write(open(sys.argv[1],'rb').read())" $DRY/fixtures/_DISPOSITIONS_V003_OBJECT.tmp.json $DRY/pass$P/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS/COVERED_LATER_DISPOSITIONS_V007.json || exit 1
done
MAN=$DRY/fixtures/MANIFEST_GATES_ONLY_STANDIN.json; MS=$(shasum -a 256 $MAN | cut -d' ' -f1)
for P in A B; do
  $PY -I -B $GEN $ROOTS $ROOTS_SHA $DRY/pass$P $P $DRY/fixtures $MAN $MS $SHIM > /dev/null || exit 1
  /usr/bin/diff -u $ROOTS $DRY/pass$P/ROOT_SEAL_STEPS_DRYRUN_$P.sh > $DRY/pass$P/SUBSTITUTION_$P.diff
  /bin/bash -n $DRY/pass$P/ROOT_SEAL_STEPS_DRYRUN_$P.sh || exit 1
  sed -e "s#$D11#$DRY#g" -e "s#ROOT_SEAL_STEPS_c3v019.sh f4843a47#$(basename $ROOTS) ${ROOTS_SHA:0:8}#" $D11/pass$P/RUN_$P.sh > $DRY/pass$P/RUN_$P.sh
  for w in "dry_run_$UTC" "$DSHA" "$(basename $ROOTS)" "$CSHA" "CASCADE_MAP_R5_ADDENDUM_FIXTURE_V002" "$KSHA" "$NSHA" "$USHA" "SUCCESSOR_CUSTODY_FIXTURE_V002"; do grep -q "$w" $DRY/pass$P/RUN_$P.sh || { echo "RUN_$P.sh lacks $w"; exit 1; }; done
  if grep -q "UNT_SEAL_FREEZE_V005_SHA256\|002133Z\|010953Z\|013957Z\|UNT_SEAL_DRIVER_CHECK_RECORD\|UNT_SEAL_RULING_\|c3v019.sh f4843a47" $DRY/pass$P/RUN_$P.sh; then echo "RUN_$P.sh still names removed inputs or dry run 9/10/11 values"; exit 1; fi
  [ "$(grep -cF -- '--manual-disclosures "$DISCLOSURES" --manual-disclosures-sha256 "$DISCLOSURES_SHA"' $DRY/pass$P/ROOT_SEAL_STEPS_DRYRUN_$P.sh)" = 1 ] || { echo "pass $P: the dry-run script does not pass BOTH disclosure flags to tool 4 exactly once"; exit 1; }
done
cd /
for P in A B; do
  taskpolicy -b /bin/bash $DRY/pass$P/RUN_$P.sh > $DRY/pass$P/RUN_$P.stdout.txt 2> $DRY/pass$P/RUN_$P.stderr.txt
  echo "pass $P exit $?: $(grep -c '  PASS  ' $DRY/pass$P/RUN_$P.stdout.txt) PASS lines; $(grep -h -E 'STOPPED|ALL STEPS' $DRY/pass$P/RUN_$P.stdout.txt $DRY/pass$P/RUN_$P.stderr.txt | head -1)"
done
for P in A B; do
  S=$DRY/pass$P/scratch_ctrl/V007_SEAL_ASSEMBLY; R=$DRY/pass$P/scratch_internal/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007
  echo "pass $P prefix entries $(/bin/ls -A $S/NO_PYCACHE_PREFIX_EMPTY | wc -l | tr -d ' '); fence: $(grep -ho '"fence_refused": [0-9]*' $S/logs/STEP_02A_DRIVER_BUILD.json $S/logs/STEP_03B_C04.json $S/logs/STEP_08_GATES_ONLY.json 2>/dev/null | tr '\n' ' '); scratch output root: $( [ -d $R ] && [ ! -L $R ] && echo "real dir, entries $(/bin/ls -A $R | wc -l | tr -d ' ')" || echo absent)"
done
for P in A B; do
  S=$DRY/pass$P/scratch_ctrl/V007_SEAL_ASSEMBLY
  echo "pass $P step 10 both flags: $(grep -cF -- '--manual-disclosures "$DISCLOSURES" --manual-disclosures-sha256 "$DISCLOSURES_SHA"' $DRY/pass$P/ROOT_SEAL_STEPS_DRYRUN_$P.sh); STEP_11_DISCLOSURES_VERBATIM: $( [ -f $S/logs/STEP_11_DISCLOSURES_VERBATIM.json ] && grep -o '"verdict": "[A-Z]*"' $S/logs/STEP_11_DISCLOSURES_VERBATIM.json || echo 'not reached / no log')"
  if [ -f $S/SEAL_RECORD_V007.json ]; then
    $PY -I -B -X pycache_prefix=$S/NO_PYCACHE_PREFIX_EMPTY $HLP check-seal-record-disclosures --seal $S/SEAL_RECORD_V007.json --seal-sha $(shasum -a 256 $S/SEAL_RECORD_V007.json | cut -d' ' -f1) \
      --disclosures $C3/root_inputs/SEAL_MANUAL_DISCLOSURES_V001.json --disclosures-sha b9db6fd1716be1e2fb47b6daf9b1e6e81743d6544f9ec72b589cf50fe0fa4ab6 --key-path NONE --form locate --record-schema ANY 2>&1 | cut -c1-400
  fi
done
shasum -a 256 $DRY/pass*/SUBSTITUTION_*.diff $DRY/pass*/ROOT_SEAL_STEPS_DRYRUN_*.sh $DRY/pass*/SUBSTITUTIONS_*.json $DRY/pass*/RUN_*.sh $DRY/pass*/RUN_*.std*.txt $DRY/fixtures/_DISPOSITIONS_V003_OBJECT.tmp.json $DRY/passB/scratch_ctrl/V007_SEAL_ASSEMBLY/SEAL_RECORD_V007.json 2>/dev/null | sed "s#$DRY/##"
echo $DRY; date -u
