#!/usr/bin/env bash
# ONE COMMAND THAT REPRODUCES THE WHOLE CORPUS.
#   ./replicate/reproduce.sh          re-run every lane script, diff against the SEALED output
#   ./replicate/reproduce.sh --seals  verify SHA-256 seals only (fast)
#   ./replicate/reproduce.sh --quick  skip the scripts known to take minutes
# Exits non-zero if any seal fails or any script's output differs from its sealed .txt.
set -uo pipefail
# ROOT must NOT be derived from $BASH_SOURCE: a snapshot copy in /tmp resolved it to "/" and the
# whole run silently found nothing. Set UNT_ROOT to override; WAC_ROOT remains a compatibility
# alias for existing automation. Otherwise use the script's location only when it actually looks
# like the repo.
ROOT="${UNT_ROOT:-${WAC_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}}"
if [ ! -f "$ROOT/CORE_FRAMEWORK_V001.md" ]; then
  echo "not a universal-network-theory checkout: $ROOT"
  echo "run from the repo, or set UNT_ROOT=/path/to/universal-network-theory"
  exit 2
fi
cd "$ROOT"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
FAIL=0

hdr(){ printf '\n\033[1m%s\033[0m\n%s\n' "$1" "$(printf '=%.0s' $(seq 1 78))"; }

hdr "0. ENVIRONMENT"
printf "  python  %s\n  numpy   %s\n" "$(python3 -V 2>&1)" "$(python3 -c 'import numpy;print(numpy.__version__)' 2>/dev/null || echo MISSING)"
python3 -c 'import numpy' 2>/dev/null || { echo "  numpy is required"; exit 2; }

hdr "1. SEALS  (SHA-256 over every registered document and lane)"
bad=0
for f in *.sha256; do
  case "$f" in *.seal.sha256) continue;; esac
  if ! shasum -a 256 -c "$f" >/dev/null 2>&1; then echo "  FAIL  $f"; bad=$((bad+1)); fi
done
[ "$bad" -eq 0 ] && echo "  all $(ls *.sha256 | grep -vc '\.seal\.' ) manifests verify" || FAIL=1

if [ "${1:-}" = "--seals" ]; then
  hdr "RESULT"; [ "$FAIL" -eq 0 ] && echo "  SEALS OK" || echo "  SEAL FAILURE"; exit "$FAIL"
fi

SLOW="o1_gap_a_compatibility.py o1_converse_theorem.py o4_L3.py o4_toric.py verify_o4.py o10_arbitrary_coupling.py"
hdr "2. RE-RUN EVERY LANE SCRIPT AND DIFF AGAINST ITS SEALED OUTPUT"
printf "  %-30s %-26s %s\n" "lane" "script" "result"
printf "  %-30s %-26s %s\n" "------------------------------" "--------------------------" "------"
# DATED RECORDS: some sealed outputs are deliberate dated records (corpus audits; discard-verdict
# annotations) and can NEVER byte-match a fresh run BY DESIGN. They are listed, with reasons, in
# replicate/dated_records.txt — printed on every run, counted separately, never as DIFFERS and
# never silently skipped. Adding to that list is a registrar act.
DATED=0
for py in LANE_*/*.py; do
  lane="${py%%/*}"; base="$(basename "$py")"; txt="${py%.py}.txt"
  if [ -f replicate/dated_records.txt ] && grep -q "^$py	" replicate/dated_records.txt; then
    reason=$(grep "^$py	" replicate/dated_records.txt | cut -f2 | cut -c1-40)
    printf "  %-30s %-26s \033[36m%s\033[0m\n" "$lane" "$base" "DATED-RECORD ($reason)"
    DATED=$((DATED+1)); continue
  fi
  [ -f "$txt" ] || txt="${py%.py}.OUT.txt"
  if [ ! -f "$txt" ]; then printf "  %-30s %-26s %s\n" "$lane" "$base" "no sealed output — SKIP"; continue; fi
  if [ "${1:-}" = "--quick" ] && [[ " $SLOW " == *" $base "* ]]; then
    printf "  %-30s %-26s %s\n" "$lane" "$base" "skipped (--quick)"; continue; fi
  out="$TMP/$lane.$base.out"
  ( cd "$lane" && python3 -u "$base" ) >"$out" 2>&1
  # Normalize BOTH sides identically before diffing -- never the results, only presentation:
  #   wall-clock timings ("(84s)", "elapsed 241.6s") vary run to run, and scripts that write
  #   their own .txt then print "[written]" leave that marker in captured stdout but not the file.
  # Wall-clock durations vary run to run and are presentation, never physics. Every rule below is
  # ANCHORED TO END OF LINE: an unanchored "(Ns)" rule once matched "(2s)" inside a probability
  # expression, (1-s)/(2s) -- a physics line. The anchor is what keeps this normalisation honest.
  norm(){ sed -E \
    -e 's/\(([0-9]+(\.[0-9]+)?)s\)[[:space:]]*$/(Ts)/' \
    -e 's/: [0-9]+(\.[0-9]+)?s\)[[:space:]]*$/: Ts)/' \
    -e 's/elapsed [0-9]+(\.[0-9]+)?s[[:space:]]*$/elapsed Ts/' \
    -e 's/runtime [0-9]+(\.[0-9]+)?s[[:space:]]*$/runtime Ts/' \
    -e 's/t=[0-9]+(\.[0-9]+)?s[[:space:]]*$/t=Ts/' \
    -e 's/numeric block: [0-9]+(\.[0-9]+)?s[[:space:]]*$/numeric block: Ts/' \
    -e 's/, [0-9]+(\.[0-9]+)?s[[:space:]]*$/, Ts/' \
    -e 's/time: [0-9]+(\.[0-9]+)? s[[:space:]]*$/time: T s/' \
    -e 's/started [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}[[:space:]]*$/started DATETIME/' \
    "$1" | grep -vx '\[written\]' | sed -e :a -e '/^[[:space:]]*$/{$d;N;ba' -e '}'; }
  norm "$txt" >"$out.a"; norm "$out" >"$out.b"
  if diff -q "$out.a" "$out.b" >/dev/null 2>&1; then
    printf "  %-30s %-26s \033[32m%s\033[0m\n" "$lane" "$base" "IDENTICAL"
  else
    n=$(diff "$out.a" "$out.b" | grep -c '^[<>]' || true)
    printf "  %-30s %-26s \033[31m%s\033[0m\n" "$lane" "$base" "DIFFERS ($n lines)"
    FAIL=1
  fi
done

[ "${DATED:-0}" -gt 0 ] && printf "\n  %d dated-record seals not re-diffed (replicate/dated_records.txt — corpus audits and deliberate lane records)\n" "$DATED"

hdr "3. THE STATUS LEDGER IS GENERATED, NOT TYPED"
before=$(shasum -a 256 STATUS_LEDGER_V001.md 2>/dev/null | cut -d' ' -f1)
./ledger/status.py >/dev/null 2>&1
after=$(shasum -a 256 STATUS_LEDGER_V001.md 2>/dev/null | cut -d' ' -f1)
# D-8: an empty hash must NOT compare equal to an empty hash and report PASS. The first snapshot
# run did exactly that -- the file was missing, both sides were "", and the check announced success.
if [ -z "$before" ] || [ -z "$after" ]; then
  echo "  FAIL — the grid could not be hashed (missing file or status.py did not run)"; FAIL=1
elif [ "$before" = "$after" ]; then
  echo "  regenerating the grid from ledger/status_ledger.tsv reproduces it byte-for-byte"
else echo "  FAIL — the committed grid does not match what the ledger generates"; FAIL=1; fi

hdr "RESULT"
[ "$FAIL" -eq 0 ] && echo "  EVERYTHING REPRODUCES" || echo "  REPRODUCTION FAILED — see above"
exit "$FAIL"
# NOTE: bash reads a script incrementally as it executes. NEVER edit this file while a run
# is in flight -- the running shell will mis-parse the shifted bytes. Run long jobs from a
# snapshot copy:  cp replicate/reproduce.sh /tmp/r.sh && /tmp/r.sh
