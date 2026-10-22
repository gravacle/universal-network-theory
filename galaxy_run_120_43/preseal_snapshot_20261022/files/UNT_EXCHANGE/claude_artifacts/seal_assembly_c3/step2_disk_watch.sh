#!/bin/bash
# step2_disk_watch.sh: a CONVENIENCE disk watchdog for the V007 step-2 launch (A105.3; FROM_CODEX/0642 item 3). Claude3, 2026-10-18.
# NOT part of the seal: it is outside ROOT_SEAL_STEPS and outside the SELECTED seal tuple's hash chain. Root starts it at launch.
#
# What it does: about every 60 s it reads the internal Data volume's free space with `df -Pk /System/Volumes/Data` (a statfs of the
# volume's mount point; it opens, stats or lists no run tree and no run file), appends ONE line to its own log, and, while free space
# is below the threshold, raises a macOS notification with a sound (osascript: display notification ... sound name "Glass").
# Threshold: 80 GiB by default (= 85.90 GB). That is the stricter reading of A105's "below 80 GB": the alert can only come earlier,
# never later. --threshold-gib sets another integer.
# It writes NOTHING except its log, which it creates exclusively at the absolute path root chooses (refused if the file exists, if
# its folder does not exist, or if the path lies in a run tree: under the step-2 output root, under runs_ext, a UVT_* or C5H name).
#
# Usage (root, at launch; stop it with kill <pid>):
#   nohup /bin/bash step2_disk_watch.sh --log /ABS/PATH/STEP2_DISK_WATCH_V007.log > /dev/null 2>&1 &
# Options:  --threshold-gib N (default 80)   --interval-s S (default 60)   --max-polls K (default 0 = until killed)
# Test-only options (not for the launch):
#   --df-stub FILE    read `df -Pk` output from FILE instead of running df (simulated free space)
#   --notify-stub     write "NOTIFY_STUB ..." to the log instead of calling osascript (no real notification)
#   --test-notify     send ONE real notification now (to check sound and permissions), log it, and exit
set -u
set -o noclobber
export PATH=/usr/bin:/bin:/usr/sbin:/sbin
cd /
VOL=/System/Volumes/Data
RUN_ROOT=/Users/bgm/Research/UNT_INTERNAL_RUNS/V007_STEP2_R5_BUILD_V007
LOG=""; THRESH_GIB=80; INTERVAL=60; MAX_POLLS=0; DF_STUB=""; NOTIFY_STUB=0; TEST_NOTIFY=0
die() { echo "step2_disk_watch: REFUSE: $*" >&2; exit 2; }
while [ $# -gt 0 ]; do
  case "$1" in
    --log) LOG="${2-}"; shift 2;;
    --threshold-gib) THRESH_GIB="${2-}"; shift 2;;
    --interval-s) INTERVAL="${2-}"; shift 2;;
    --max-polls) MAX_POLLS="${2-}"; shift 2;;
    --df-stub) DF_STUB="${2-}"; shift 2;;
    --notify-stub) NOTIFY_STUB=1; shift;;
    --test-notify) TEST_NOTIFY=1; shift;;
    *) die "unknown argument: $1";;
  esac
done
for n in "$THRESH_GIB" "$INTERVAL" "$MAX_POLLS"; do case "$n" in ''|*[!0-9]*) die "not a non-negative integer: '$n'";; esac; done
case "$LOG" in /*) ;; *) die "--log must be an absolute path";; esac
case "$LOG" in *"/../"*|*"/./"*|*/..|*/.|*//*) die "--log must be a plain absolute path";; esac
lc="$(printf '%s' "$LOG" | tr '[:upper:]' '[:lower:]')"
case "$lc" in "$(printf '%s' "$RUN_ROOT" | tr '[:upper:]' '[:lower:]')"|"$(printf '%s' "$RUN_ROOT" | tr '[:upper:]' '[:lower:]')"/*|*/runs_ext/*|*/runs_ext|*/uvt_*|*kmax_a2f10_c5h_run_v001*|/.vol*|/system/volumes/data/*)
  die "the log must not lie in a run tree (or use a /.vol or firmlink spelling): $LOG";; esac
[ -d "$(dirname "$LOG")" ] || die "the log's folder does not exist: $(dirname "$LOG")"
: > "$LOG" 2>/dev/null || die "the log exists already or cannot be created (exclusive): $LOG"
utc() { date -u +%Y-%m-%dT%H:%M:%SZ; }
notify() {   # $1 = message (digits and fixed text only)
  if [ "$NOTIFY_STUB" = 1 ]; then echo "$(utc) NOTIFY_STUB title='UNT step-2 disk watchdog' message='$1' sound=Glass" >> "$LOG"; return 0; fi
  osascript -e "display notification \"$1\" with title \"UNT step-2 disk watchdog\" sound name \"Glass\"" > /dev/null 2>&1
  echo "$(utc) NOTIFIED rc=$? message='$1'" >> "$LOG"
}
echo "$(utc) START pid=$$ volume=$VOL threshold_gib=$THRESH_GIB interval_s=$INTERVAL max_polls=$MAX_POLLS df=$([ -n "$DF_STUB" ] && echo "STUB:$DF_STUB" || echo 'df -Pk') notify=$([ "$NOTIFY_STUB" = 1 ] && echo stub || echo osascript)" >> "$LOG"
trap 'echo "$(utc) STOP (signal) pid=$$" >> "$LOG"; exit 0' TERM INT HUP
if [ "$TEST_NOTIFY" = 1 ]; then notify "Test notification from step2_disk_watch.sh (no disk alarm)"; echo "$(utc) END test-notify" >> "$LOG"; exit 0; fi
poll=0
while :; do
  poll=$((poll + 1))
  if [ -n "$DF_STUB" ]; then out="$(cat "$DF_STUB" 2>&1)"; rc=$?; else out="$(df -Pk "$VOL" 2>&1)"; rc=$?; fi
  avail_kb="$(printf '%s\n' "$out" | awk -v v="$VOL" 'NR==2 && $NF==v && $4 ~ /^[0-9]+$/ {print $4}')"
  if [ "$rc" -ne 0 ] || [ -z "$avail_kb" ]; then
    echo "$(utc) poll=$poll DF_ERROR rc=$rc (no reading this poll; the watchdog keeps running)" >> "$LOG"
  else
    line="$(awk -v kb="$avail_kb" -v th="$THRESH_GIB" 'BEGIN { printf "free_gib=%.2f free_gb=%.2f threshold_gib=%d", kb/1048576, kb*1024/1e9, th }')"
    if [ "$avail_kb" -lt $((THRESH_GIB * 1048576)) ]; then
      echo "$(utc) poll=$poll LOW $line" >> "$LOG"
      gib="$(awk -v kb="$avail_kb" 'BEGIN { printf "%.1f", kb/1048576 }')"
      notify "Step-2 disk: ${gib} GiB free on ${VOL}, below ${THRESH_GIB} GiB. Root rules: relocate unstarted cases or pause admission (A105.3)."
    else
      echo "$(utc) poll=$poll OK $line" >> "$LOG"
    fi
  fi
  if [ "$MAX_POLLS" -gt 0 ] && [ "$poll" -ge "$MAX_POLLS" ]; then echo "$(utc) END max_polls=$MAX_POLLS" >> "$LOG"; exit 0; fi
  sleep "$INTERVAL"
done
