#!/bin/bash
# Claude3 (0642): tests of step2_disk_watch.sh with a SIMULATED threshold or a df STUB only (never by filling the disk), and with the
# notification STUBBED (no real notification is raised; the AppleScript line is only compiled by osacompile, never run).
# Everything it writes lies under a NEW folder seal_assembly_c3/watchdog_test_<UTC>/. usage: test_step2_disk_watch_c3sa_c3v001.sh WATCH_SHA
set -u; set -o noclobber
C3=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3; W=$C3/step2_disk_watch.sh
[ "$(shasum -a 256 $W | cut -d' ' -f1)" = "$1" ] || { echo "watchdog bytes differ"; exit 1; }
UTC=$(date -u +%Y%m%dT%H%M%SZ); T=$C3/watchdog_test_$UTC; mkdir $T || exit 1; RES=$T/WATCHDOG_TEST_RESULTS_C3SA.txt
ok_all=1
rec() { echo "$1" >> $RES; case "$1" in *" FAIL "*) ok_all=0;; esac; }
stub() { printf 'Filesystem   1024-blocks      Used Available Capacity  Mounted on\n/dev/disk3s5   971350180 400000000 %s    50%%    %s\n' "$1" "$2" > "$T/$3"; }
echo "# step2_disk_watch.sh tests (Claude3, $UTC); watchdog sha $1; all simulated (stub df or a high threshold); notifications stubbed" > $RES
# T1 simulated threshold with the real df
/bin/bash $W --log $T/T1.log --threshold-gib 100000 --max-polls 1 --notify-stub; rc=$?
grep -q ' poll=1 LOW free_gib=' $T/T1.log && grep -q 'NOTIFY_STUB' $T/T1.log && [ $rc = 0 ] && rec "T1  PASS  simulated threshold 100000 GiB, real df: LOW + NOTIFY_STUB (rc $rc)" || rec "T1  FAIL  (rc $rc)"
# T2 default threshold with the real df (about 450 GiB free now)
/bin/bash $W --log $T/T2.log --max-polls 1 --notify-stub; rc=$?
grep -q ' poll=1 OK free_gib=' $T/T2.log && ! grep -q 'NOTIFY' $T/T2.log && [ $rc = 0 ] && rec "T2  PASS  default 80 GiB, real df: OK, no notification ($(grep -o 'free_gib=[0-9.]*' $T/T2.log))" || rec "T2  FAIL  (rc $rc)"
# T3 df stub: 50 GiB free
stub 52428800 /System/Volumes/Data df_50gib.txt
/bin/bash $W --log $T/T3.log --df-stub $T/df_50gib.txt --max-polls 1 --notify-stub; rc=$?
grep -q 'LOW free_gib=50.00' $T/T3.log && grep -q 'NOTIFY_STUB' $T/T3.log && rec "T3  PASS  df stub 50 GiB: LOW + NOTIFY_STUB" || rec "T3  FAIL  (rc $rc)"
# T4 the boundary: exactly 80 GiB is not below; 1 KiB less is
stub 83886080 /System/Volumes/Data df_80gib.txt; stub 83886079 /System/Volumes/Data df_80gib_minus_1k.txt
/bin/bash $W --log $T/T4a.log --df-stub $T/df_80gib.txt --max-polls 1 --notify-stub
/bin/bash $W --log $T/T4b.log --df-stub $T/df_80gib_minus_1k.txt --max-polls 1 --notify-stub
grep -q ' OK free_gib=80.00' $T/T4a.log && grep -q ' LOW free_gib=80.00' $T/T4b.log && grep -q NOTIFY_STUB $T/T4b.log && ! grep -q NOTIFY $T/T4a.log && rec "T4  PASS  boundary: 80 GiB exactly -> OK; 80 GiB - 1 KiB -> LOW" || rec "T4  FAIL"
# T5 a df reading it cannot parse (another mount point): logged, and the watchdog keeps polling (2 polls, 1 s apart)
stub 52428800 /Volumes/Other df_wrong_mount.txt
/bin/bash $W --log $T/T5.log --df-stub $T/df_wrong_mount.txt --max-polls 2 --interval-s 1 --notify-stub; rc=$?
[ "$(grep -c DF_ERROR $T/T5.log)" = 2 ] && grep -q 'END max_polls=2' $T/T5.log && ! grep -q NOTIFY $T/T5.log && rec "T5  PASS  unparseable df: DF_ERROR on both polls, no alert, keeps running" || rec "T5  FAIL  (rc $rc)"
# T6 the log exists already: refused, and the file is unchanged
printf 'SYNTHETIC existing log\n' > $T/T6_existing.log; h0=$(shasum -a 256 $T/T6_existing.log | cut -d' ' -f1)
/bin/bash $W --log $T/T6_existing.log --max-polls 1 --notify-stub 2> $T/T6.stderr; rc=$?
[ $rc = 2 ] && [ "$(shasum -a 256 $T/T6_existing.log | cut -d' ' -f1)" = "$h0" ] && rec "T6  PASS  existing log: REFUSE (rc 2), file unchanged" || rec "T6  FAIL  (rc $rc)"
# T7 a log path inside the step-2 run tree, under runs_ext, and with a firmlink spelling: refused lexically, nothing created
for p in /Users/bgm/Research/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007/watch.log $T/runs_ext/watch.log /System/Volumes/Data$T/T7.log; do
  /bin/bash $W --log "$p" --max-polls 1 --notify-stub 2>> $T/T7.stderr; rc=$?
  [ $rc = 2 ] && rec "T7  PASS  run-tree / firmlink log path refused (rc 2): $p" || rec "T7  FAIL  (rc $rc) $p"
done
[ ! -e /Users/bgm/Research/UNT_INTERNAL_RUNS ] && rec "T7  PASS  /Users/bgm/Research/UNT_INTERNAL_RUNS still absent" || rec "T7  FAIL  UNT_INTERNAL_RUNS exists"
# T8 relative path, missing folder, unknown option, non-integer threshold
/bin/bash $W --log rel.log --max-polls 1 2>> $T/T8.stderr; r1=$?
/bin/bash $W --log $T/no_such_folder/x.log --max-polls 1 2>> $T/T8.stderr; r2=$?
/bin/bash $W --log $T/T8c.log --bogus 2>> $T/T8.stderr; r3=$?
/bin/bash $W --log $T/T8d.log --threshold-gib 8O 2>> $T/T8.stderr; r4=$?
[ "$r1$r2$r3$r4" = 2222 ] && [ ! -e $T/T8c.log ] && [ ! -e $T/T8d.log ] && [ ! -e /rel.log ] && rec "T8  PASS  relative path, missing folder, unknown option, non-integer threshold: all REFUSE (rc 2), nothing created" || rec "T8  FAIL  ($r1$r2$r3$r4)"
# T9 SIGTERM: started in the background (stub df), stopped with kill; the STOP line is logged
stub 104857600 /System/Volumes/Data df_100gib.txt
/bin/bash $W --log $T/T9.log --df-stub $T/df_100gib.txt --interval-s 1 --notify-stub & pid=$!
sleep 3; kill -TERM $pid; wait $pid; rc=$?
grep -q 'STOP (signal)' $T/T9.log && [ "$(grep -c ' OK free_gib=100.00' $T/T9.log)" -ge 2 ] && rec "T9  PASS  background run, $(grep -c ' OK ' $T/T9.log) OK polls, SIGTERM -> STOP line (rc $rc)" || rec "T9  FAIL  (rc $rc)"
# T10 the AppleScript line compiles (osacompile into this folder; NOT executed; no notification is raised)
osacompile -o $T/notify_syntax_check.scpt -e 'display notification "Step-2 disk: 79.9 GiB free on /System/Volumes/Data, below 80 GiB. Root rules: relocate unstarted cases or pause admission (A105.3)." with title "UNT step-2 disk watchdog" sound name "Glass"' 2> $T/T10.stderr; rc=$?
[ $rc = 0 ] && rec "T10 PASS  osacompile accepts the notification line (compiled only, not run)" || rec "T10 FAIL  osacompile rc $rc"
# T11 static: the only commands are date, df, awk, cat (stub only), osascript, tr, dirname, sleep; the only fixed paths are the volume and the run-root name it refuses
rec "T11 INFO  fixed paths in the script: $(grep -o '/[A-Za-z][A-Za-z0-9_/.]*' $W | grep -v '^/bin/bash$\|^/usr/bin\|^/bin\|^/usr/sbin\|^/sbin\|^/dev/null$' | sort -u | tr '\n' ' ')"
rec "UNTESTED: a real notification with sound (run once by root: step2_disk_watch.sh --log ABS_PATH --test-notify)"
[ $ok_all = 1 ] && rec "ALL PASS" || rec "SOME FAIL"
cat $RES; echo $T
