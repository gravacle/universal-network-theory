#!/bin/bash
# launch_s0_serial_root_c2v003.sh -- root's launch of one S0 serial call of record (s0_launch_kit_c2, C2V003).
#
# DEFAULT IS DRY: it fills, dry-plans and checks, prints the exact root_monitor command, and launches nothing.
# Only --launch starts root_monitor (root alone launches; A133; A141).
# C2V003 (V006 A166): no memory gating.  No machine-gate admission, no A133 103 GB rule, no post-launch gate reading;
# the RSS cap is physical RAM (137438953472 B); wall and output caps unchanged.  macOS schedules memory.
#
# Usage:
#   launch_s0_serial_root_c2v003.sh <seed|j0|j1|j2> --launch-root DIR --run-root /Volumes/External1/NGC_<NAME>
#       [--attempt K] [--step2-receipt ABS_PATH] [--launch]
#       [--synthetic-pins FILE --synthetic-pins-sha256 H]      (synthetic tests only; refused with real monitor/driver)
#
# Attempts (relaunch path): attempt 1 is the default.  A procedural mis-launch of attempt k is relaunched as
# --attempt k+1 in the same launch root, under the same M-15 record; the outdir is <run root>/NGC_P1_S0_<ROLE>_SERIAL_RUN_
# C2V003_A<k>.  order-check admits attempt k+1 only after attempt k's MISLAUNCH record and its monitor receipt exist.
#
# Order (each step refuses with exit 3 and launches nothing):
#   1. validate: role, attempt, paths (absolute; run root one level under /Volumes/External1, name NGC_*, never runs_ext,
#      no ngc3198/uvt_ component), every pin from bytes, the V006 pin lines.
#   2. M-15 FIRST (A142 item 6): with --launch, if no record exists yet, s0_prelaunch_record_c2v001.py writes it by
#      exclusive create; the script refuses if that write fails.  Only the seed serial's attempt 1 may write it, and only
#      while no launch record exists (the record precedes the earliest step-5 NGC launch receipt).  DRY: --check-only.
#   3. order-check (launch): seed first, one confirmed launch per name, the attempt rule above.
#   4. fill: fill_step5_c2v001 (ec417e76) from the V006 HANDOFF_PIN (RI45-09), then fill-check (certificates, pair leaf,
#      V006 SPEC_PIN).
#   5. a FRESH dry plan (RI45-13) with dry_one_c2v001 (aac20dd3); refuse on any blocker (lists, not the label).
#   6. register the spec sha in the per-point launch registry (exclusive create; reused for the same spec).
#   7. driver sha from bytes = 577f8c94... (and the monitor ba031c23...); the exact monitor argv (D3 form).
#   8. External1 checks and free space >= 136 GiB + 20 GiB (disk guard); step 2's last receipt; the WATCH_PIN watch
#      (passive) is running.
#   9. V006 freeze (first launch in the launch root): unchanged since the record; wait until the UTC second has advanced.
#  10. launch root_monitor with exactly --driver-sha256 <64 hex>, absolute --spec, absolute --outdir /Volumes/External1/...,
#      caps wall 610324 s, RSS 137438953472 B (RAM), output 136 GiB; nohup; caffeinate -i -w <monitor pid>.
#  11. wait for <receipt>.launch.json; launch-check: the launch record must match the plan (command, pins, caps,
#      retries 0, launch after the M-15 record).  CONFIRMED -> launch record (exit 0, or 4 with a flag).  Otherwise ->
#      stop the driver process group at once (kill-target checks), write the MISLAUNCH record, exit 5; relaunch with
#      --attempt k+1.
# Exit: 0 done (DRY: printed), 3 refused, 4 launched with an order flag, 5 alert (mis-launch stopped, or no launch
#       record from the monitor), 2 usage.
set -euo pipefail
set -o noclobber
umask 022
export PATH=/usr/bin:/bin:/usr/sbin:/sbin
export LC_ALL=C

KIT_SHA='e58c8605fd35d8894d214ee3e06fa83d9577b14efdaa960938bf2bb330676e73'
RW_SHA='a10965b7a508f106e3d153632d2b1a39a427d9106fa2de3c9e09d92b85bcb59a'
REAL_DRIVER_SHA='577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377'
REAL_MONITOR_SHA='ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107'
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
KIT_DIR=$(cd "$(dirname "$0")" && pwd -P)
KIT="$KIT_DIR/s0_kit_c2v003.py"
RW="$KIT_DIR/s0_prelaunch_record_c2v001.py"

die() { echo "REFUSED: $*" >&2; exit 3; }
note() { echo "[s0-serial $(date -u +%Y-%m-%dT%H:%M:%SZ)] $*"; }
sha() { shasum -a 256 "$1" | awk '{print $1}'; }
need_arg() { [ "$1" -ge 2 ] || die "missing value for $2"; }

[ -f "$KIT" ] && [ "$(sha "$KIT")" = "$KIT_SHA" ] || die "kit helper sha differs from $KIT_SHA"
[ -f "$RW" ] && [ "$(sha "$RW")" = "$RW_SHA" ] || die "record writer sha differs from $RW_SHA"

ROLE="${1:-}"
case "$ROLE" in seed|j0|j1|j2) shift ;; *) echo "usage: $0 <seed|j0|j1|j2> --launch-root DIR --run-root /Volumes/External1/NGC_<NAME> [--attempt K] [--step2-receipt F] [--launch]" >&2; exit 2 ;; esac
LAUNCH=0; LR=""; RR=""; STEP2=""; SP=""; SPH=""; ATTEMPT=1
while [ $# -gt 0 ]; do
  case "$1" in
    --launch-root) need_arg $# "$1"; LR="$2"; shift 2 ;;
    --run-root) need_arg $# "$1"; RR="$2"; shift 2 ;;
    --attempt) need_arg $# "$1"; ATTEMPT="$2"; shift 2 ;;
    --step2-receipt) need_arg $# "$1"; STEP2="$2"; shift 2 ;;
    --synthetic-pins) need_arg $# "$1"; SP="$2"; shift 2 ;;
    --synthetic-pins-sha256) need_arg $# "$1"; SPH="$2"; shift 2 ;;
    --launch) LAUNCH=1; shift ;;
    *) die "unknown argument: $1" ;;
  esac
done
case "$ATTEMPT" in [1-9]|[1-9][0-9]) ;; *) die "--attempt must be an integer 1..99" ;; esac
MODE=dry; [ "$LAUNCH" = 1 ] && MODE=launch
[ -n "$LR" ] && [ -n "$RR" ] || die "--launch-root and --run-root are required"
VARGS=(--role "$ROLE" --call serial --mode "$MODE" --launch-root "$LR" --run-root "$RR" --attempt "$ATTEMPT")
if [ -n "$SP" ] || [ -n "$SPH" ]; then VARGS+=(--synthetic-pins "$SP" --synthetic-pins-sha256 "$SPH"); fi

# ---- 1. validate (no writes)
PLAN_SH=$("$PY" -I -B "$KIT" validate "${VARGS[@]}" --emit shell) || die "validate: $PLAN_SH"
eval "$PLAN_SH"
if [ "$PLAN_SYNTHETIC" = 0 ]; then
  [ "$PLAN_DRIVER_SHA" = "$REAL_DRIVER_SHA" ] && [ "$PLAN_MONITOR_SHA" = "$REAL_MONITOR_SHA" ] || die "real pins differ from 577f8c94/ba031c23"
fi
note "mode=$MODE role=$ROLE attempt=$PLAN_ATTEMPT outdir=$PLAN_OUTDIR"

# ---- 2. M-15 record FIRST (A142 item 6; M-15 (a)+(1))
if [ ! -e "$PLAN_RECORD" ] && [ "$ROLE" != seed ]; then
  [ "$MODE" = dry ] || die "NO_M15_RECORD: the seed serial launches first and writes the record (M-15; r3a L454)"
  note "DRY: no M-15 record yet; the seed serial writes it at its launch"
elif [ ! -e "$PLAN_RECORD" ] && [ "$PLAN_ATTEMPT" != 1 ]; then
  [ "$MODE" = dry ] || die "NO_M15_RECORD: a relaunch (attempt $PLAN_ATTEMPT) runs under the existing M-15 record of its launch root"
  note "DRY: no M-15 record yet; a relaunch (attempt $PLAN_ATTEMPT) needs the existing record of its launch root"
elif [ ! -e "$PLAN_RECORD" ]; then
  if [ -d "$PLAN_LAUNCHES_DIR" ] && [ -n "$(ls -A "$PLAN_LAUNCHES_DIR")" ]; then
    die "LAUNCH_RECORDS_EXIST_WITHOUT_M15_RECORD in $PLAN_LAUNCHES_DIR"
  fi
  RARGS=(--v006 "$PLAN_V006" --out "$PLAN_RECORD" --require-pins "$PLAN_GATE_PINS" --require-pins-sha256 "$PLAN_GATE_PINS_SHA"
         --first-call "$PLAN_FIRST_CALL" --driver-sha256 "$PLAN_DRIVER_SHA" --monitor-sha256 "$PLAN_MONITOR_SHA"
         --outdir "$PLAN_OUTDIR" --receipt "$PLAN_RECEIPT")
  if [ "$MODE" = launch ]; then
    REC_OUT=$("$PY" -I -B "$RW" "${RARGS[@]}") || die "M-15 record NOT written, no launch: $REC_OUT"
    note "M-15 record written: $REC_OUT"
  else
    REC_OUT=$("$PY" -I -B "$RW" "${RARGS[@]}" --check-only --allow-pending-first-spec) || die "M-15 record check (dry): $REC_OUT"
    note "DRY: M-15 record check passes (nothing written)"
  fi
else
  note "M-15 record exists: $PLAN_RECORD"
fi

# ---- work directory (new) and plan
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
RUP=$(echo "$ROLE" | tr 'a-z' 'A-Z')
if [ "$MODE" = launch ]; then WROOT="$LR/work"; else WROOT="$LR/dry"; fi
[ -d "$WROOT" ] || mkdir "$WROOT"
WORK="$WROOT/S0_${RUP}_SERIAL_A${PLAN_ATTEMPT}_${STAMP}_$$"
mkdir "$WORK"
"$PY" -I -B "$KIT" validate "${VARGS[@]}" --emit json --out "$WORK/plan.json" > /dev/null || die "plan"

# ---- 3. order (launch)
if [ "$MODE" = launch ]; then
  OC=$("$PY" -I -B "$KIT" order-check --plan "$WORK/plan.json") || die "order: $OC"
fi

# ---- 4. fill from the V006-published handoff
[ -n "$PLAN_HANDOFF" ] || die "V006 has no HANDOFF_PIN S0_$RUP (RI45-09)"
[ "$(sha "$PLAN_FILLER")" = "$PLAN_FILLER_SHA" ] || die "filler sha"
"$PLAN_PY" -I -B "$PLAN_FILLER" --handoff "$PLAN_HANDOFF" --expected-sha256 "$PLAN_HANDOFF_SHA" --output-dir "$WORK/fill" \
  > "$WORK/fill.stdout.txt" 2>&1 || die "filler refused: $(cat "$WORK/fill.stdout.txt")"
FC=$("$PY" -I -B "$KIT" fill-check --plan "$WORK/plan.json" --fill-dir "$WORK/fill" --out "$WORK/fill_check.json") || die "fill-check: $FC"
SPEC="$WORK/fill/CALL_A_K32_A2_HEADLINE_C2V001.json"
SPEC_SHA=$(sha "$SPEC")
note "filled spec $SPEC sha256 $SPEC_SHA ($FC)"

# ---- 5. fresh dry plan (RI45-13): read the blocker lists
[ "$(sha "$PLAN_DRY")" = "$PLAN_DRY_SHA" ] || die "dry harness sha"
mkdir "$WORK/dry"
env -i PATH=/usr/bin:/bin HOME="${HOME:-/Users/bgm}" OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  "$PLAN_PY" -I -B "$PLAN_DRY" "$PLAN_DRIVER" "$PLAN_DRIVER_SHA" "$SPEC" "$SPEC_SHA" "$WORK/dry/report" "$WORK/dry/log.json" \
  > "$WORK/dry.stdout.txt" 2>&1 || die "dry harness failed: $(tail -c 2000 "$WORK/dry.stdout.txt")"
DV=$("$PY" -I -B "$KIT" dry-verdict --plan "$WORK/plan.json" --spec "$SPEC" --spec-sha256 "$SPEC_SHA" \
     --log "$WORK/dry/log.json" --report-dir "$WORK/dry/report" --out "$WORK/dry_verdict.json") || die "dry plan: $DV"
note "dry plan: $DV"

# ---- 6. per-point launch registry (exclusive create; DRY prints the entry)
REG=$("$PY" -I -B "$KIT" register --plan "$WORK/plan.json" --fill-check "$WORK/fill_check.json" --dry-verdict "$WORK/dry_verdict.json") || die "register: $REG"
[ "$MODE" = launch ] && note "registry: $REG"

# ---- 7. driver (and monitor) sha from bytes; the exact monitor argv
[ "$(sha "$PLAN_DRIVER")" = "$PLAN_DRIVER_SHA" ] || die "driver sha differs from $PLAN_DRIVER_SHA"
[ "$(sha "$PLAN_MONITOR")" = "$PLAN_MONITOR_SHA" ] || die "monitor sha differs from $PLAN_MONITOR_SHA"
MON_CMD=("$PLAN_PY" -I -B "$PLAN_MONITOR" --driver "$PLAN_DRIVER" --driver-sha256 "$PLAN_DRIVER_SHA" --spec "$SPEC"
         --outdir "$PLAN_OUTDIR" --receipt "$PLAN_RECEIPT" --wall-cap-s "$PLAN_WALL" --rss-cap-bytes "$PLAN_RSS"
         --output-cap-bytes "$PLAN_OUTCAP")
CMDLINE=$("$PY" -I -B "$KIT" monitor-argv --plan "$WORK/plan.json" -- "${MON_CMD[@]}") || die "monitor argv form: $CMDLINE"

# ---- 8. preconditions (no memory admission: V006 A166)
if [ "$MODE" = dry ]; then
  [ -n "$PLAN_SPEC_PIN_SHA" ] || note "DRY: V006 has no SPEC_PIN S0_${RUP}_SERIAL yet; register $SPEC_SHA (RI45-13) before --launch"
  echo "DRY: nothing launched. The launch command would be:"
  echo "$CMDLINE"
  echo "After the launch: the launch-record check (<receipt>.launch.json against the plan; RSS cap = RAM); no gate reading (A166)."
  echo "DRY_SPEC_SHA256=$SPEC_SHA"
  echo "DRY_WORK=$WORK"
  exit 0
fi

E1=$("$PY" -I -B "$KIT" ext1-check --plan "$WORK/plan.json" --out "$WORK/ext1_check.json") || die "External1: $E1"
[ -n "$STEP2" ] || die "--step2-receipt is required with --launch (A135.5)"
S2=$("$PY" -I -B "$KIT" step2-check --plan "$WORK/plan.json" --receipt "$STEP2" --out "$WORK/step2_check.json") || die "step 2: $S2"
WC=$("$PY" -I -B "$KIT" watch-check --plan "$WORK/plan.json" --out "$WORK/watch_check.json") || die "memory watch: $WC"

# ---- 9. V006 freeze; the UTC second must advance past the record's
REC_EPOCH=$("$PY" -I -B "$KIT" record-epoch --plan "$WORK/plan.json") || die "record epoch"
while [ "$(date -u +%s)" -le "$REC_EPOCH" ]; do sleep 0.2; done
FZ=$("$PY" -I -B "$KIT" freeze-check --plan "$WORK/plan.json") || die "V006 write freeze: $FZ"
[ "$(sha "$PLAN_DRIVER")" = "$PLAN_DRIVER_SHA" ] || die "driver sha (immediately before launch)"
[ "$(sha "$PLAN_MONITOR")" = "$PLAN_MONITOR_SHA" ] || die "monitor sha (immediately before launch)"
[ "$(sha "$SPEC")" = "$PLAN_SPEC_PIN_SHA" ] || die "spec sha differs from the V006 SPEC_PIN"

# ---- 10. launch (root only)
cd /
note "LAUNCH (attempt $PLAN_ATTEMPT): $CMDLINE"
nohup "${MON_CMD[@]}" > "$WORK/monitor.stdout.txt" 2> "$WORK/monitor.stderr.txt" < /dev/null &
MON_PID=$!
caffeinate -i -w "$MON_PID" > /dev/null 2>&1 < /dev/null &
note "monitor pid $MON_PID"

# ---- 11. launch receipt, then the launch-record check
n=0
while [ ! -e "$PLAN_LAUNCH_JSON" ] && [ "$n" -lt 600 ]; do
  kill -0 "$MON_PID" 2> /dev/null || break
  sleep 0.2; n=$((n + 1))
done
if [ ! -e "$PLAN_LAUNCH_JSON" ]; then
  echo "ALERT: no $PLAN_LAUNCH_JSON (monitor refused or failed); see $WORK/monitor.stdout.txt" >&2
  exit 5
fi
KC=0
KV=$("$PY" -I -B "$KIT" launch-check --plan "$WORK/plan.json" --mon-pid "$MON_PID" --spec "$SPEC" --spec-sha256 "$SPEC_SHA" \
     --out "$WORK/launch_verdict.json") || KC=$?
note "launch check: $KV"
RARGS2=(--plan "$WORK/plan.json" --work "$WORK" --spec "$SPEC" --spec-sha256 "$SPEC_SHA" --mon-pid "$MON_PID"
        --launch-verdict "$WORK/launch_verdict.json")
if [ "$KC" != 0 ]; then
  # procedural mis-launch (or no verdict): stop the driver process group at once, with the kill-target checks
  KT=0
  PGID=$("$PY" -I -B "$KIT" kill-target --launch-json "$PLAN_LAUNCH_JSON" --spec-sha256 "$SPEC_SHA" \
         --expect-leaf "$PLAN_EXPECTED_LEAF" --mon-pid "$MON_PID" 2> "$WORK/kill_target.json") || KT=$?
  RES=NOT_KILLED_TARGET_REFUSED
  if [ "$KT" = 0 ] && [ -n "$PGID" ]; then
    kill -TERM -- "-$PGID" 2> /dev/null || true
    k=0; while kill -0 -- "-$PGID" 2> /dev/null && [ "$k" -lt 75 ]; do sleep 0.2; k=$((k + 1)); done
    RES=KILLED_TERM
    if kill -0 -- "-$PGID" 2> /dev/null; then kill -KILL -- "-$PGID" 2> /dev/null || true; RES=KILLED_KILL; fi
  elif [ "$KT" = 1 ]; then
    RES=ALREADY_ENDED
  fi
  m=0; while [ ! -e "$PLAN_RECEIPT" ] && [ "$m" -lt 300 ]; do sleep 0.2; m=$((m + 1)); done
  PG_ARG=(); [ -n "${PGID:-}" ] && [ "$KT" = 0 ] && PG_ARG=(--pgid "$PGID")
  "$PY" -I -B "$KIT" launch-record --outcome MISLAUNCH "${RARGS2[@]}" --stop-result "$RES" \
    --kill-target-out "$WORK/kill_target.json" ${PG_ARG[@]+"${PG_ARG[@]}"} > "$WORK/mislaunch_record.out" 2>&1 || true
  echo "MISLAUNCH_STOPPED (procedural, not a scientific failure): launch check exit $KC, stop $RES; $(cat "$WORK/mislaunch_record.out")" >&2
  echo "Relaunch: the same command with --attempt $((PLAN_ATTEMPT + 1)) in this launch root (same M-15 record), once root has recorded the mis-launch." >&2
  exit 5
fi
LRC=0
LREC=$("$PY" -I -B "$KIT" launch-record --outcome LAUNCH "${RARGS2[@]}") || LRC=$?
note "launch record: $LREC"
[ "$LRC" = 0 ] || { echo "ALERT: launch record flags (exit $LRC): $LREC" >&2; [ "$LRC" = 4 ] && exit 4; exit 5; }
note "LAUNCHED (launch record matches the plan; RSS cap = RAM). On the result: driver_sha256 = 577f8c94; reads stay validity-only."
exit 0
