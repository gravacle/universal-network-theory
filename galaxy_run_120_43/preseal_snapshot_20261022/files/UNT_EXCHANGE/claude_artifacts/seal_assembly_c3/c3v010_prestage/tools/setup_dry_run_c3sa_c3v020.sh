#!/bin/bash
# setup_dry_run_c3sa_c3v020.sh: Claude3 (c3v011, for ROOT_SEAL_STEPS_c3v027.sh; root 0667 A123): generator c3v014; the gates-only stand-in is no
# longer copied from dry run 9 (that copy was the draft e5967bb9 minus identity_runs, so B0_RO1 and B0_N3 stayed null): it is DERIVED from the
# target script's own MANIFEST_GATES pin (bytes checked), with identity_runs emptied and a FIXTURE note; the generator checks it gate for gate.
# c3v019: Claude3 (c3v010 FINAL, for ROOT_SEAL_STEPS_c3v026.sh; root 0664, A121): as c3v018, and the RUN files now carry
# the run inputs root ANSWERED, labelled as such: P8 the /Volumes/External1 C5H spelling (a string only: step 9 stays the published stub,
# which never reads it; step 0 checks its suffix), P9 the ack string, P10 the floor 300 (0659), P5 root's file 6a3fa535. A RUN file that still
# carries a STAND-IN label, or lacks the P8 spelling, stops the setup.
# c3v018: Claude3 (c3v010 FINAL, for ROOT_SEAL_STEPS_c3v024.sh): generator c3v013 (no stand-in); the RUN files carry root's REAL
# run inputs where they exist: the P5 dispositions file (6a3fa535; copied byte-identically into the scratch inputs folder, since S09 moves that
# folder to scratch), the key map KEY_EQUIVALENCE_MAP_V007 (72a21888), the CASCADE_MAP_R5_ADDENDUM_CX3V001 (86c89730; Claude4 0139) and the
# floor 300 GiB (0659). Step 9 stays the published stub; the C5H spelling is a string only.
# c3v017: Claude3 (c3v016, never run, still required the deleted custody env line in its presence check).
# c3v016: Claude3 (c3v010 near-final, for ROOT_SEAL_STEPS_c3v022.sh): generator c3v012 (only S29, the custody stand-in);
# the RUN files drop the four B7 env inputs (c3v022 pins the NEW-item list and refuses those inputs); no NEW-item stand-in is generated.
# c3v015: Claude3 (c3v010 pre-stage; c3v014's dry run 035955Z stopped at step 10, NEW_ITEMS_IMPL_NOT_THE_REVIEWED_SOURCE): the
# labelled B7 NEW-item list stand-in now names IMPL r14 (COMPARE_V007_IMPL_R14_CX1V002 2ba6d12e, from bytes) as compare_impl, since tool 4 v004
# requires the IMPL the list is taken from to name the reviewed source sha (r14) in full (A81 RI-20). Everything else is c3v014.
# c3v014: Claude3 (c3v010 pre-stage, for ROOT_SEAL_STEPS_c3v021.sh): generator c3v011 (stand-ins S26 registry V009, S27
# disclosures V002); the RUN files derive from dry run 12 (20261019T025053Z) with the compare inputs moved to r14 and SELECTED_R14_CX1V002
# (A114/A116); the post-run locate uses the pass's own pinned disclosures file (the S27 stand-in), not a hardcoded one.
# c3v013: Claude3 (c3v009; c3v012 never ran a dry run: its pin reader expanded $C3 only, so the real c3v020
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
# usage: setup_dry_run_c3sa_c3v020.sh ROOT_SCRIPT_PATH ROOT_SCRIPT_SHA OPEN_V005_SHA DRY_PARENT_DIR
set -uo pipefail; set -o noclobber
C3=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3; A=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ROOTS=$1; ROOTS_SHA=$2; WANT_V005=$3; DRYP=$4; W=$C3/c3v009_prestage
GEN=$C3/c3v010_prestage/tools/make_dry_run_c3sa_c3v014.py; SHIM=$C3/tools/dryrun_tool_shim_c3sa_c3v007.py; CHK=$W/tools/check_tool4_imports_c3v003.py
[ "$(shasum -a 256 $GEN | cut -d' ' -f1)" = b49181e2a57367d5fcf2c2bfb4092e9e17d12207c5b1290ce9af81a0adad815c ] || { echo "generator c3v014 bytes differ"; exit 1; }
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
UTC=$(date -u +%Y%m%dT%H%M%SZ); DRY=$DRYP/dry_run_$UTC; D9=$C3/dry_run_20261019T002133Z; D10=$C3/dry_run_20261019T010953Z; D11=$C3/dry_run_20261019T013957Z; D12=$C3/dry_run_20261019T025053Z
mkdir $DRY $DRY/fixtures $DRY/fixtures/C5H_STANDIN_REGISTERED_DIR || exit 1
for f in KEY_EQUIVALENCE_MAP_FIXTURE.json NEW_ITEM_LIST_FIXTURE.json SUCCESSOR_CUSTODY_FIXTURE.json CASCADE_MAP_R5_ADDENDUM_FIXTURE.json; do
  $PY -I -B -c "import sys; open(sys.argv[2],'xb').write(open(sys.argv[1],'rb').read())" $D9/fixtures/$f $DRY/fixtures/$f || exit 1
done
MGP=$(pv MANIFEST_GATES); MGS=$(pv MANIFEST_GATES_SHA)   # c3v020: the stand-in comes from the TARGET's own manifest pin
$PY -I -B - "$MGP" "$MGS" "$DRY/fixtures/MANIFEST_GATES_ONLY_STANDIN.json" <<'PYEOF' || exit 1
import sys, json, hashlib
p, h, out = sys.argv[1:4]
b = open(p, 'rb').read(); assert hashlib.sha256(b).hexdigest() == h, 'target manifest bytes'
m = json.loads(b); assert isinstance(m.get('identity_runs'), dict) and not m.get('cases') and not m.get('rpair')
m['identity_runs'] = {}
m['note'] = ('FIXTURE_DRY_RUN_ONLY (Claude3 0626 dry run): not a record of record; never use at the real seal: the root manifest %s (%s) with identity_runs EMPTIED, '
             'so the dry-run gates-only reads no runs_ext/UVT_* tree; the gate record paths are the real (readable) records.') % (p.rsplit('/', 1)[1], h[:8])
open(out, 'x').write(json.dumps(m, indent=1) + '\n')
PYEOF
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
  $PY -I -B -c "import sys,hashlib; b=open(sys.argv[1],'rb').read(); assert hashlib.sha256(b).hexdigest()=='6a3fa5353e575fbfe617aa497abd4752e8a2c8676d19f6c4c16a69dfeac0c9fe'; open(sys.argv[2],'xb').write(b)" "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/V007_SEAL_ASSEMBLY_INPUTS/COVERED_LATER_DISPOSITIONS_V007.json" $DRY/pass$P/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS/COVERED_LATER_DISPOSITIONS_V007.json || exit 1
done
MAN=$DRY/fixtures/MANIFEST_GATES_ONLY_STANDIN.json; MS=$(shasum -a 256 $MAN | cut -d' ' -f1)
for P in A B; do
  $PY -I -B $GEN $ROOTS $ROOTS_SHA $DRY/pass$P $P $DRY/fixtures $MAN $MS $SHIM > /dev/null || exit 1
  /usr/bin/diff -u $ROOTS $DRY/pass$P/ROOT_SEAL_STEPS_DRYRUN_$P.sh > $DRY/pass$P/SUBSTITUTION_$P.diff
  /bin/bash -n $DRY/pass$P/ROOT_SEAL_STEPS_DRYRUN_$P.sh || exit 1
  sed -e "s#$D12#$DRY#g" -e "s#ROOT_SEAL_STEPS_c3v020.sh 36058df8#$(basename $ROOTS) ${ROOTS_SHA:0:8}#" \
      -e "s#v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py\"     \# r13 frozen; deltas pending#v007_compare_c2/r14/kmax_tail_compare_c2v007_r14_cx1v001.py\"     \# r14, the compare of record (A114/A116)#" \
      -e "s#UNT_SEAL_COMPARE_REVIEWED_SHA256=f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157#UNT_SEAL_COMPARE_REVIEWED_SHA256=f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7#" \
      -e "s#v007_compare_c2/r13/SELECTED_R13_CX3V001.json#v007_compare_c2/r14/SELECTED_R14_CX1V002.json#" \
      -e "s#UNT_SEAL_COMPARE_SELECTION_SHA256=10acd09887bffa5130e2ebbff7d54ab2d70ea7aff0fb2cd696e0cda0fcf6bb5e#UNT_SEAL_COMPARE_SELECTION_SHA256=6b650ececefee673ec3e04849574f9a4b75b977288afd3c9949a4b8d2d3cd49a#" \
      -e '/^export UNT_SEAL_NEW_ITEM_LIST_PATH=/d' -e '/^export UNT_SEAL_NEW_ITEM_LIST_SHA256=/d' -e '/^export UNT_SEAL_SUCCESSOR_CUSTODY_PATH=/d' -e '/^export UNT_SEAL_SUCCESSOR_CUSTODY_SHA256=/d' \
      -e "s#UNT_SEAL_DISPOSITIONS_SHA256=$DSHA#UNT_SEAL_DISPOSITIONS_SHA256=6a3fa5353e575fbfe617aa497abd4752e8a2c8676d19f6c4c16a69dfeac0c9fe#" \
      -e "s#$DRY/fixtures/KEY_EQUIVALENCE_MAP_FIXTURE_V002.json#/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_b7_inputs_c4/KEY_EQUIVALENCE_MAP_V007.json#" \
      -e "s#UNT_SEAL_KEY_EQUIVALENCE_MAP_SHA256=$KSHA#UNT_SEAL_KEY_EQUIVALENCE_MAP_SHA256=72a21888eda617638df38ddd64a0e7981bfb6842a9f7f17b8c1a7d4b93e50ec4#" \
      -e "s#$DRY/fixtures/CASCADE_MAP_R5_ADDENDUM_FIXTURE_V002.json#/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cascade_map_r5_addendum_cx3/CASCADE_MAP_R5_ADDENDUM_CX3V001.json#" \
      -e "s#UNT_SEAL_CASCADE_MAP_R5_ADDENDUM_SHA256=$CSHA#UNT_SEAL_CASCADE_MAP_R5_ADDENDUM_SHA256=86c897304ec5a0971c3ad1552a60cfad90fc3ac809d68fdacee2be1b942caf9e#" \
      -e "s#^export UNT_SEAL_MIN_FREE_GIB=50 #export UNT_SEAL_MIN_FREE_GIB=300 #" \
      -e "s#^export UNT_SEAL_C5H_RUN_DIR=.*#export UNT_SEAL_C5H_RUN_DIR=\"/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext/KMAX_A2F10_C5H_RUN_V001\"  \# P8, root 0664 (A121): a STRING (step 9 stubbed; never read)#" \
      -e "s#\# STAND-IN floor\$#\# P10, root 0659 (300 GiB)#" \
      -e "s#\# STAND-IN ack (dry run only)\$#\# P9, root 0664 (A121)#" \
      -e "s#\# FIXTURE (v003 object on r6: entries .*#\# P5: root file 6a3fa535 (entries [], frozen c01b3c51), copied byte-identically into scratch (S09)#" \
      -e "s#Root-supplied inputs are DRY-RUN\$#Root-supplied inputs are as root#" \
      -e "s#^\# STAND-INS (labelled); nothing here is a root ruling.\$#\# answered them (P5; P7 to P10: 0659, 0664 A121); step 9 is the published stub (no C5H read).#" \
      $D12/pass$P/RUN_$P.sh > $DRY/pass$P/RUN_$P.sh
  for w in r14/kmax_tail_compare_c2v007_r14_cx1v001.py f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7 r14/SELECTED_R14_CX1V002.json 6b650ececefee673ec3e04849574f9a4b75b977288afd3c9949a4b8d2d3cd49a; do grep -q "$w" $DRY/pass$P/RUN_$P.sh || { echo "RUN_$P.sh lacks $w"; exit 1; }; done
  if grep -q "/r13/\|f5adfd11\|10acd098\|025053Z\|UNT_SEAL_NEW_ITEM_LIST\|UNT_SEAL_SUCCESSOR_CUSTODY\|_FIXTURE_V002\|$DSHA\|$KSHA\|$CSHA" $DRY/pass$P/RUN_$P.sh; then echo "RUN_$P.sh still names r13, dry run 12, a B7 env input or a fixture"; exit 1; fi
  for w in "dry_run_$UTC" 6a3fa5353e575fbfe617aa497abd4752e8a2c8676d19f6c4c16a69dfeac0c9fe "$(basename $ROOTS)" 86c897304ec5a0971c3ad1552a60cfad90fc3ac809d68fdacee2be1b942caf9e CASCADE_MAP_R5_ADDENDUM_CX3V001 72a21888eda617638df38ddd64a0e7981bfb6842a9f7f17b8c1a7d4b93e50ec4 KEY_EQUIVALENCE_MAP_V007 UNT_SEAL_MIN_FREE_GIB=300; do grep -q "$w" $DRY/pass$P/RUN_$P.sh || { echo "RUN_$P.sh lacks $w"; exit 1; }; done
  if grep -q "UNT_SEAL_FREEZE_V005_SHA256\|002133Z\|010953Z\|013957Z\|UNT_SEAL_DRIVER_CHECK_RECORD\|UNT_SEAL_RULING_\|c3v020.sh 36058df8" $DRY/pass$P/RUN_$P.sh; then echo "RUN_$P.sh still names removed inputs or older dry-run values"; exit 1; fi
  [ "$(grep -cF -- '--manual-disclosures "$DISCLOSURES" --manual-disclosures-sha256 "$DISCLOSURES_SHA"' $DRY/pass$P/ROOT_SEAL_STEPS_DRYRUN_$P.sh)" = 1 ] || { echo "pass $P: the dry-run script does not pass BOTH disclosure flags to tool 4 exactly once"; exit 1; }
  grep -qF 'export UNT_SEAL_C5H_RUN_DIR="/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext/KMAX_A2F10_C5H_RUN_V001"' $DRY/pass$P/RUN_$P.sh || { echo "RUN_$P.sh lacks the P8 (A121) C5H spelling"; exit 1; }
  if grep -q 'STAND-IN\|FIXTURE (v003\|DRY-RUN$' $DRY/pass$P/RUN_$P.sh; then echo "RUN_$P.sh still carries a stand-in label"; exit 1; fi
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
pvd() { /usr/bin/sed -n "s/^$1=\"\([^\"]*\)\".*/\1/p;s/.*; $1=\"\([^\"]*\)\".*/\1/p" $2 | head -n 1 | /usr/bin/sed -e "s#^\$C3/#$C3/#" -e "s#^\$A/#$A/#"; }
for P in A B; do
  S=$DRY/pass$P/scratch_ctrl/V007_SEAL_ASSEMBLY
  echo "pass $P step 10 both flags: $(grep -cF -- '--manual-disclosures "$DISCLOSURES" --manual-disclosures-sha256 "$DISCLOSURES_SHA"' $DRY/pass$P/ROOT_SEAL_STEPS_DRYRUN_$P.sh); STEP_11_DISCLOSURES_VERBATIM: $( [ -f $S/logs/STEP_11_DISCLOSURES_VERBATIM.json ] && grep -o '"verdict": "[A-Z]*"' $S/logs/STEP_11_DISCLOSURES_VERBATIM.json || echo 'not reached / no log')"
  if [ -f $S/SEAL_RECORD_V007.json ]; then
    $PY -I -B -X pycache_prefix=$S/NO_PYCACHE_PREFIX_EMPTY $HLP check-seal-record-disclosures --seal $S/SEAL_RECORD_V007.json --seal-sha $(shasum -a 256 $S/SEAL_RECORD_V007.json | cut -d' ' -f1) \
      --disclosures $(pvd DISCLOSURES $DRY/pass$P/ROOT_SEAL_STEPS_DRYRUN_$P.sh) --disclosures-sha $(pvd DISCLOSURES_SHA $DRY/pass$P/ROOT_SEAL_STEPS_DRYRUN_$P.sh) --key-path NONE --form locate --record-schema ANY 2>&1 | cut -c1-400
  fi
done
shasum -a 256 $DRY/pass*/SUBSTITUTION_*.diff $DRY/pass*/ROOT_SEAL_STEPS_DRYRUN_*.sh $DRY/pass*/SUBSTITUTIONS_*.json $DRY/pass*/RUN_*.sh $DRY/pass*/RUN_*.std*.txt $DRY/fixtures/_DISPOSITIONS_V003_OBJECT.tmp.json $DRY/passB/scratch_ctrl/V007_SEAL_ASSEMBLY/SEAL_RECORD_V007.json 2>/dev/null | sed "s#$DRY/##"
echo $DRY; date -u
