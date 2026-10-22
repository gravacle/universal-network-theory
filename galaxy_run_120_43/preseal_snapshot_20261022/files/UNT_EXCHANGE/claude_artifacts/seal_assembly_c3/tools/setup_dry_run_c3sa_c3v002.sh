#!/bin/bash
# setup_dry_run_c3sa_c3v002.sh: Claude3 (FROM_CODEX/0642). Sets up and runs dry-run passes A and B of the root script named by $3.
# Everything it creates lies under a NEW seal_assembly_c3/dry_run_<UTC>/ folder (mkdir / noclobber / open 'x'); it never writes in
# a real seal location. Step 9 is STUBBED by S15 and never executed; the step-2 output root is a scratch path (S17).
# usage: setup_dry_run_c3sa_c3v002.sh ROOT_SCRIPT_SHA OPEN_V005_SHA ROOT_SCRIPT_NAME (c3v002: the script name is an argument)
set -uo pipefail; set -o noclobber
C3=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ROOTS=$C3/$3; ROOTS_SHA=$1; WANT_V005=$2
GEN=$C3/tools/make_dry_run_c3sa_c3v004.py; SHIM=$C3/tools/dryrun_tool_shim_c3sa_c3v004.py
[ "$(shasum -a 256 $ROOTS | cut -d' ' -f1)" = "$ROOTS_SHA" ] || { echo "root script bytes differ"; exit 1; }
OPEN="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md"
OS=$(shasum -a 256 "$OPEN" | cut -d' ' -f1); [ "$OS" = "$WANT_V005" ] || { echo "open V005 is $OS, not $WANT_V005"; exit 1; }
UTC=$(date -u +%Y%m%dT%H%M%SZ); DRY=$C3/dry_run_$UTC; D7=$C3/dry_run_20261018T222835Z
mkdir $DRY $DRY/fixtures $DRY/fixtures/C5H_STANDIN_REGISTERED_DIR || exit 1
for f in KEY_EQUIVALENCE_MAP_FIXTURE.json NEW_ITEM_LIST_FIXTURE.json SUCCESSOR_CUSTODY_FIXTURE.json CASCADE_MAP_R5_ADDENDUM_FIXTURE.json MANIFEST_GATES_ONLY_STANDIN.json; do
  $PY -I -B -c "import sys; open(sys.argv[2],'xb').write(open(sys.argv[1],'rb').read())" $D7/fixtures/$f $DRY/fixtures/$f || exit 1
done
DSHA=$($PY -I -B - "$OPEN" "$OS" "$DRY" <<'PYEOF'
import sys, json, hashlib, re
OPEN, OS, DRY = sys.argv[1:4]
fb = open(OPEN, 'rb').read(); assert hashlib.sha256(fb).hexdigest() == OS
starts = [0] + [m.end() for m in re.finditer(b'\n', fb)]
heads = [s for s in starts if s < len(fb) and fb.startswith(b'## ', s)]
def sec(e):
    s = [h for h in heads if fb.startswith(('## %s:' % e).encode(), h)][0]; n = [h for h in heads if h > s]
    return fb[s:(n[0] if n else len(fb))]
later = ['A%d' % n for n in sorted({int(m.group(1)) for m in re.finditer(rb'^## A(\d{1,3}):', fb, re.M)}) if n > 101]
lab = 'DRY-RUN FIXTURE (labelled; not a disposition of record): '
reasons = {'A102': lab + 'A102 rules the r12 review split and orders r13; it fills seal_slots.compare at assembly',
           'A103': lab + 'A103 reassigns review queues and accepts cx3r008 for step 5',
           'A104': lab + 'A104 names r13 the compare of record and restates the mechanical D-05 rule',
           'A105': lab + 'A105 rules the BUILD_V007 delta (RP-S1 and W7-S1 in the seal script; a disk watchdog; E-OPS5)'}
d = {'schema': 'UNT_V007_LATER_ENTRY_DISPOSITIONS_C4V001', 'frozen_addendum_sha256': OS,
     'entries': [{'entry': e, 'disposition': 'no_change', 'reason': reasons.get(e, lab + e), 'section_sha256': hashlib.sha256(sec(e)).hexdigest()} for e in later]}
t = json.dumps(d, indent=1) + '\n'
open(DRY + '/fixtures/_DISPOSITIONS_V003_OBJECT.tmp.json', 'x').write(t)
print(hashlib.sha256(t.encode()).hexdigest())
PYEOF
) || exit 1
echo "dispositions fixture $DSHA"
for P in A B; do
  mkdir $DRY/pass$P $DRY/pass$P/scratch_ctrl $DRY/pass$P/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS $DRY/pass$P/scratch_pkt $DRY/pass$P/scratch_pkt/P128 $DRY/pass$P/scratch_internal || exit 1
  $PY -I -B -c "import sys,hashlib; b=open(sys.argv[1],'rb').read(); assert hashlib.sha256(b).hexdigest()=='f3e4e2beeb8f1cb151892fd903b889c471cea58fea1b67c72552137d037575ca'; open(sys.argv[2],'xb').write(b)" /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/bind_sealed_launch_plan_cx1v001.py $DRY/pass$P/scratch_pkt/bind_sealed_launch_plan_cx1v001.py || exit 1
  $PY -I -B -c "import sys; open(sys.argv[2],'xb').write(open(sys.argv[1],'rb').read())" $DRY/fixtures/_DISPOSITIONS_V003_OBJECT.tmp.json $DRY/pass$P/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS/COVERED_LATER_DISPOSITIONS_V007.json || exit 1
done
MAN=$DRY/fixtures/MANIFEST_GATES_ONLY_STANDIN.json; MS=$(shasum -a 256 $MAN | cut -d' ' -f1)
for P in A B; do
  $PY -I -B $GEN $ROOTS $ROOTS_SHA $DRY/pass$P $P $DRY/fixtures $MAN $MS $SHIM > /dev/null || exit 1
  /usr/bin/diff -u $ROOTS $DRY/pass$P/ROOT_SEAL_STEPS_DRYRUN_$P.sh > $DRY/pass$P/SUBSTITUTION_$P.diff
  /bin/bash -n $DRY/pass$P/ROOT_SEAL_STEPS_DRYRUN_$P.sh || exit 1
  sed -e "s#dry_run_20261018T222835Z#dry_run_$UTC#g" -e "s#ROOT_SEAL_STEPS_c3v008.sh 023b2bbf#$3 ${ROOTS_SHA:0:8}#" \
      -e "s#acb7f44a3f7c68289571a3b83add4101fb4f6d5185781c03627946489a21a8ab   \# the open V005 at dry-run setup (A104 newest)#$OS   \# the open V005 at dry-run setup (A105 newest)#" \
      -e "s#UNT_SEAL_DISPOSITIONS_SHA256=1250e0fb22b8638268e9a76586ed700d7a25a34673f25d8349862ff2418fb3ab      \# FIXTURE (v003 object: A102, A103, A104 no_change)#UNT_SEAL_DISPOSITIONS_SHA256=$DSHA      \# FIXTURE (v003 object: A102-A105 no_change; labelled)#" \
      $D7/pass$P/RUN_$P.sh > $DRY/pass$P/RUN_$P.sh
  for w in "dry_run_$UTC" "$OS" "$DSHA" "$3"; do grep -q "$w" $DRY/pass$P/RUN_$P.sh || { echo "RUN_$P.sh lacks $w"; exit 1; }; done
  if grep -q "acb7f44a\|1250e0fb\|222835Z" $DRY/pass$P/RUN_$P.sh; then echo "RUN_$P.sh still names dry run 7 values"; exit 1; fi
done
cd /
for P in A B; do
  taskpolicy -b /bin/bash $DRY/pass$P/RUN_$P.sh > $DRY/pass$P/RUN_$P.stdout.txt 2> $DRY/pass$P/RUN_$P.stderr.txt
  echo "pass $P exit $?: $(grep -c '  PASS  ' $DRY/pass$P/RUN_$P.stdout.txt) PASS lines; $(grep -h -E 'STOPPED|ALL STEPS' $DRY/pass$P/RUN_$P.stdout.txt $DRY/pass$P/RUN_$P.stderr.txt | head -1)"
done
for P in A B; do
  S=$DRY/pass$P/scratch_ctrl/V007_SEAL_ASSEMBLY; R=$DRY/pass$P/scratch_internal/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007
  echo "pass $P prefix entries $(/bin/ls -A $S/NO_PYCACHE_PREFIX_EMPTY | wc -l | tr -d ' '); fence: $(grep -ho '"fence_refused": [0-9]*' $S/logs/STEP_02A_DRIVER_BUILD.json $S/logs/STEP_08_GATES_ONLY.json 2>/dev/null | tr '\n' ' '); scratch output root: $( [ -d $R ] && [ ! -L $R ] && echo "real dir, entries $(/bin/ls -A $R | wc -l | tr -d ' ')" || echo absent)"
done
shasum -a 256 $DRY/pass*/SUBSTITUTION_*.diff $DRY/pass*/ROOT_SEAL_STEPS_DRYRUN_*.sh $DRY/pass*/SUBSTITUTIONS_*.json $DRY/pass*/RUN_*.sh $DRY/pass*/RUN_*.std*.txt $DRY/fixtures/_DISPOSITIONS_V003_OBJECT.tmp.json $DRY/passB/scratch_ctrl/V007_SEAL_ASSEMBLY/SEAL_RECORD_V007.json 2>/dev/null | sed "s#$DRY/##"
echo $DRY; date -u
