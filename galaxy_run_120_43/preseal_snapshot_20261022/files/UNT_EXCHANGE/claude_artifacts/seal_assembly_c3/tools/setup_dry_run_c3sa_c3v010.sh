#!/bin/bash
# setup_dry_run_c3sa_c3v010.sh: Claude3 (A110/A111, script c3v018: generator c3v009 (S24/S25: v003 tool 4 stands in for the PENDING
# tool 4 v004); the RUN files derive from dry run 10 (20261019T010953Z) minus the four inputs A111 removed: UNT_SEAL_DRIVER_CHECK_RECORD_PATH,
# _SHA256, UNT_SEAL_RULING_EPS_NGC, UNT_SEAL_RULING_I1T_NGC; the fixtures are regenerated exactly as c3v009 does and must equal dry run 10's).
# c3v009: Claude3 (seal tools v003; + the three B7 fixtures in v003 C4V002 forms, labelled). Sets up and runs dry-run passes A and B of the root script named by $3.
# Everything it creates lies under a NEW seal_assembly_c3/dry_run_<UTC>/ folder (mkdir / noclobber / open 'x'); it never writes in
# a real seal location. Step 9 is STUBBED by S15; the step-2 output root is a scratch path (S17); r5 and labelled SELECTED fixtures
# stand in for the unpublished prereg r6 and seal tools v003 (S19-S21).
# usage: setup_dry_run_c3sa_c3v010.sh ROOT_SCRIPT_SHA OPEN_V005_SHA ROOT_SCRIPT_NAME
set -uo pipefail; set -o noclobber
C3=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3; A=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ROOTS=$C3/$3; ROOTS_SHA=$1; WANT_V005=$2
GEN=$C3/tools/make_dry_run_c3sa_c3v009.py; SHIM=$C3/tools/dryrun_tool_shim_c3sa_c3v007.py
[ "$(shasum -a 256 $ROOTS | cut -d' ' -f1)" = "$ROOTS_SHA" ] || { echo "root script bytes differ"; exit 1; }
OPEN="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md"
OS=$(shasum -a 256 "$OPEN" | cut -d' ' -f1); [ "$OS" = "$WANT_V005" ] || { echo "open V005 is $OS, not $WANT_V005"; exit 1; }
UTC=$(date -u +%Y%m%dT%H%M%SZ); DRY=$C3/dry_run_$UTC; D9=$C3/dry_run_20261019T002133Z; D10=$C3/dry_run_20261019T010953Z
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
  sed -e '/^export UNT_SEAL_DRIVER_CHECK_RECORD_PATH=/d' -e '/^export UNT_SEAL_DRIVER_CHECK_RECORD_SHA256=/d' -e '/^export UNT_SEAL_RULING_EPS_NGC=/d' \
      -e '/^export UNT_SEAL_RULING_I1T_NGC=/d' -e "s#dry_run_20261019T010953Z#dry_run_$UTC#g" -e "s#ROOT_SEAL_STEPS_c3v016.sh dcdb746c#$3 ${ROOTS_SHA:0:8}#" \
      $D10/pass$P/RUN_$P.sh > $DRY/pass$P/RUN_$P.sh
  : sed of dry run 9 kept for the record, not run: \
      -e "s#UNT_SEAL_DISPOSITIONS_SHA256=ed7aa568233f1e4a5250dbff2d41907b617045a4faa967ef27cb1c2998f9a9be#UNT_SEAL_DISPOSITIONS_SHA256=$DSHA#" -e "s#fixtures/CASCADE_MAP_R5_ADDENDUM_FIXTURE.json#fixtures/CASCADE_MAP_R5_ADDENDUM_FIXTURE_V002.json#" -e "s#fixtures/KEY_EQUIVALENCE_MAP_FIXTURE.json#fixtures/KEY_EQUIVALENCE_MAP_FIXTURE_V002.json#" -e "s#UNT_SEAL_KEY_EQUIVALENCE_MAP_SHA256=e060670ac70dd5ce42ad96bb8b62ef20c01bbcf0ac971658100a213c1e4a8d60#UNT_SEAL_KEY_EQUIVALENCE_MAP_SHA256=$KSHA#" -e "s#fixtures/NEW_ITEM_LIST_FIXTURE.json#fixtures/NEW_ITEM_LIST_FIXTURE_V002.json#" -e "s#UNT_SEAL_NEW_ITEM_LIST_SHA256=79b7408314673215c9f2bf948fc810bdaf534f35762c409a40d6b1dd1822120a#UNT_SEAL_NEW_ITEM_LIST_SHA256=$NSHA#" -e "s#fixtures/SUCCESSOR_CUSTODY_FIXTURE.json#fixtures/SUCCESSOR_CUSTODY_FIXTURE_V002.json#" -e "s#UNT_SEAL_SUCCESSOR_CUSTODY_SHA256=d57c75385b96ad91645ac3d9de2e1e35baf66da2d18644c2aa353829b3824304#UNT_SEAL_SUCCESSOR_CUSTODY_SHA256=$USHA#" -e "s#UNT_SEAL_CASCADE_MAP_R5_ADDENDUM_SHA256=ec962aaa966ec991ded4807902f33bde8f8c4e50f58a945c3e5e06d09467fc71#UNT_SEAL_CASCADE_MAP_R5_ADDENDUM_SHA256=$CSHA#" \
      $D9/pass$P/RUN_$P.sh > /dev/null
  for w in "dry_run_$UTC" "$DSHA" "$3" "$CSHA" "CASCADE_MAP_R5_ADDENDUM_FIXTURE_V002" "$KSHA" "$NSHA" "$USHA" "SUCCESSOR_CUSTODY_FIXTURE_V002"; do grep -q "$w" $DRY/pass$P/RUN_$P.sh || { echo "RUN_$P.sh lacks $w"; exit 1; }; done
  if grep -q "UNT_SEAL_FREEZE_V005_SHA256\|002133Z\|010953Z\|UNT_SEAL_DRIVER_CHECK_RECORD\|UNT_SEAL_RULING_\|c3v016" $DRY/pass$P/RUN_$P.sh; then echo "RUN_$P.sh still names removed inputs or dry run 9/10 values"; exit 1; fi
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
shasum -a 256 $DRY/pass*/SUBSTITUTION_*.diff $DRY/pass*/ROOT_SEAL_STEPS_DRYRUN_*.sh $DRY/pass*/SUBSTITUTIONS_*.json $DRY/pass*/RUN_*.sh $DRY/pass*/RUN_*.std*.txt $DRY/fixtures/_DISPOSITIONS_V003_OBJECT.tmp.json $DRY/passB/scratch_ctrl/V007_SEAL_ASSEMBLY/SEAL_RECORD_V007.json 2>/dev/null | sed "s#$DRY/##"
echo $DRY; date -u
