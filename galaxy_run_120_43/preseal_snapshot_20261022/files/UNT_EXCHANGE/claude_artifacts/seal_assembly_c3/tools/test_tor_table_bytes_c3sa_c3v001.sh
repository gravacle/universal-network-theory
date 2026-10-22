#!/bin/bash
# Claude3 (0644): MUST_FAIL controls for the root script's own tor_table_bytes (its text is extracted from the script by its markers and
# run as-is with the script's own jf): r5's relative byte_copy, r6's absolute one inside its folder, and synthetic bad forms.
# usage: test_tor_table_bytes_c3sa_c3v001.sh SCRIPT SCRIPT_SHA   (writes only under a NEW seal_assembly_c3/tor_table_bytes_test_<UTC>/)
set -u; set -o noclobber
C3=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3; A=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts; SCRIPT=$1
[ "$(shasum -a 256 $SCRIPT | cut -d' ' -f1)" = "$2" ] || { echo "script bytes differ"; exit 1; }
UTC=$(date -u +%Y%m%dT%H%M%SZ); T=$C3/tor_table_bytes_test_$UTC; mkdir $T $T/tor_folder || exit 1; RES=$T/TOR_TABLE_BYTES_RESULTS_C3SA.txt
FN=$T/extracted_functions.sh
sed -n '/^jf() { /,/^print(d if not isinstance/p' $SCRIPT > $FN; sed -n '/^tor_table_bytes() {/,/^}/p' $SCRIPT >> $FN
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
mk() { printf '{"entries_after_A81": {"addendum_read": {"byte_copy": "%s", "sha256_at_generation": "%s"}}}\n' "$2" "$(printf '%064d' 7)" > $T/tor_folder/$1; }
mk TOR_OUTSIDE.json "/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/elsewhere/V005_COPY.md (synthetic)"
mk TOR_DOTDOT.json "addendum_read/../../V005_COPY.md (synthetic)"
mk TOR_EMPTY.json ""
mk TOR_ABS_DOTDOT.json "$T/tor_folder/../tor_folder/V005_COPY.md (synthetic)"
ok=1
run() {   # id, TOR path, want (PASS:expected_path | REFUSE)
  out=$( ( set -Eeuo pipefail; PYX=("$PY" -I -B); source $FN; PREREG_TOR="$2"; tor_table_bytes; echo "TABLE_BYTES=$TABLE_BYTES" ) 2>&1 ); rc=$?
  case "$3" in
    PASS:*) want=${3#PASS:}; if [ $rc = 0 ] && [ "$(echo "$out" | tail -1)" = "TABLE_BYTES=$want" ]; then echo "$1 PASS  $out" >> $RES; else echo "$1 FAIL  rc=$rc $out" >> $RES; ok=0; fi;;
    REFUSE) if [ $rc != 0 ]; then echo "$1 PASS  refused (rc $rc): $(echo "$out" | tail -1)" >> $RES; else echo "$1 FAIL  accepted: $out" >> $RES; ok=0; fi;;
  esac
}
echo "# tor_table_bytes controls (Claude3 0644): script $(basename $SCRIPT) $2" > $RES
run TB-1 $A/v007_final_prereg_c4/r5/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json "PASS:$A/v007_final_prereg_c4/r5/addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md"
run TB-2 $A/v007_final_prereg_c4/r6/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json "PASS:$A/v007_final_prereg_c4/r6/addendum_read/V005_ADDENDUM_READ_AT_R6_GENERATION.md"
run TB-3 $T/tor_folder/TOR_OUTSIDE.json REFUSE
run TB-4 $T/tor_folder/TOR_DOTDOT.json REFUSE
run TB-5 $T/tor_folder/TOR_EMPTY.json REFUSE
run TB-6 $T/tor_folder/TOR_ABS_DOTDOT.json REFUSE
[ $ok = 1 ] && echo "ALL_OK True" >> $RES || echo "ALL_OK False" >> $RES
cat $RES; shasum -a 256 $RES
