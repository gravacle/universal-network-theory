#!/bin/bash
# launch_s0_serial_root_c2v001.sh -- root's launch of one S0 serial call of record (s0_launch_kit_c2, C2V001).
#
# DEFAULT IS DRY: it fills, dry-plans and checks, prints the exact root_monitor command, and launches nothing.
# Only --launch starts root_monitor (root alone launches; A133; A141; A143).
#
# Usage:
#   launch_s0_serial_root_c2v001.sh <seed|j0|j1|j2> --launch-root DIR --run-root /Volumes/External1/NGC_<NAME>
#       [--step2-receipt ABS_PATH] [--launch] [--dry-admission]
#       [--synthetic-pins FILE --synthetic-pins-sha256 H]      (synthetic tests only; refused with real monitor/driver)
#
# Order (each step refuses with exit 3 and launches nothing):
#   1. validate: role, paths (absolute; run root one level under /Volumes/External1, name NGC_*, never runs_ext, no
#      ngc3198/uvt_ component), every pin from bytes, the V006 pin lines.
#   2. M-15 FIRST (A142 item 6): with --launch, if no record exists yet, s0_prelaunch_record_c2v001.py writes it by
#      exclusive create; the script refuses if that write fails.  Only the seed serial may write it, and only while no
#      launch record exists (the record precedes the earliest step-5 NGC launch receipt).  DRY: --check-only.
#   3. fill: fill_step5_c2v001 (ec417e76) from the V006 HANDOFF_PIN (RI45-09: S0 record 1be5ed70 + this point's EPS
#      record + LO 07745bbf; the GQ binding is custody), then fill-check (certificates, pair leaf, V006 SPEC_PIN).
#   4. a FRESH dry plan (RI45-13) with dry_one_c2v001 (aac20dd3); refuse on any blocker (lists, not the label).
#   5. register the spec sha in the per-point launch registry (exclusive create).
#   6. driver sha from bytes = 577f8c94... (and the monitor ba031c23...).
#   7. sched v003 admission (ngc_admission class + pinned gate decide + A133 memory rule); External1 checks and free
#      space >= 136 GiB + 20 GiB; step 2's last receipt; the WATCH_PIN watch is running.
#   8. V006 freeze (first launch): unchanged since the record; wait until the UTC second has advanced past the record.
#   9. launch root_monitor with exactly --driver-sha256 <64 hex>, absolute --spec, absolute --outdir /Volumes/External1/...,
#      caps wall 610324 s, RSS 32 GiB, output 136 GiB; nohup; caffeinate -i -w <monitor pid>.
#  10. wait for <receipt>.launch.json; --hold-check (a serial never holds: expect 0); write the launch record by 'x'.
# Exit: 0 done (DRY: printed), 3 refused, 4 launched with an order flag, 5 launched with an alert, 2 usage.
set -euo pipefail
set -o noclobber
umask 022
export PATH=/usr/bin:/bin:/usr/sbin:/sbin
export LC_ALL=C

KIT_SHA='15d451a6f0a2e8833a7b69a74d91a498ffa299eca85f727ec535c4d4d427ae2b'
RW_SHA='a10965b7a508f106e3d153632d2b1a39a427d9106fa2de3c9e09d92b85bcb59a'
REAL_DRIVER_SHA='577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377'
REAL_MONITOR_SHA='ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107'
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
KIT_DIR=$(cd "$(dirname "$0")" && pwd -P)
KIT="$KIT_DIR/s0_kit_c2v001.py"
RW="$KIT_DIR/s0_prelaunch_record_c2v001.py"

die() { echo "REFUSED: $*" >&2; exit 3; }
note() { echo "[s0-serial $(date -u +%Y-%m-%dT%H:%M:%SZ)] $*"; }
sha() { shasum -a 256 "$1" | awk '{print $1}'; }
need_arg() { [ "$1" -ge 2 ] || die "missing value for $2"; }

[ -f "$KIT" ] && [ "$(sha "$KIT")" = "$KIT_SHA" ] || die "kit helper sha differs from $KIT_SHA"
[ -f "$RW" ] && [ "$(sha "$RW")" = "$RW_SHA" ] || die "record writer sha differs from $RW_SHA"

ROLE="${1:-}"
case "$ROLE" in seed|j0|j1|j2) shift ;; *) echo "usage: $0 <seed|j0|j1|j2> --launch-root DIR --run-root /Volumes/External1/NGC_<NAME> [--step2-receipt F] [--launch]" >&2; exit 2 ;; esac
LAUNCH=0; DRY_ADM=0; LR=""; RR=""; STEP2=""; SP=""; SPH=""
while [ $# -gt 0 ]; do
  case "$1" in
    --launch-root) need_arg $# "$1"; LR="$2"; shift 2 ;;
    --run-root) need_arg $# "$1"; RR="$2"; shift 2 ;;
    --step2-receipt) need_arg $# "$1"; STEP2="$2"; shift 2 ;;
    --synthetic-pins) need_arg $# "$1"; SP="$2"; shift 2 ;;
    --synthetic-pins-sha256) need_arg $# "$1"; SPH="$2"; shift 2 ;;
    --launch) LAUNCH=1; shift ;;
    --dry-admission) DRY_ADM=1; shift ;;
    *) die "unknown argument: $1" ;;
  esac
done
MODE=dry; [ "$LAUNCH" = 1 ] && MODE=launch
[ -n "$LR" ] && [ -n "$RR" ] || die "--launch-root and --run-root are required"
VARGS=(--role "$ROLE" --call serial --mode "$MODE" --launch-root "$LR" --run-root "$RR")
if [ -n "$SP" ] || [ -n "$SPH" ]; then VARGS+=(--synthetic-pins "$SP" --synthetic-pins-sha256 "$SPH"); fi

# ---- 1. validate (no writes)
PLAN_SH=$("$PY" -I -B "$KIT" validate "${VARGS[@]}" --emit shell) || die "validate: $PLAN_SH"
eval "$PLAN_SH"
if [ "$PLAN_SYNTHETIC" = 0 ]; then
  [ "$PLAN_DRIVER_SHA" = "$REAL_DRIVER_SHA" ] && [ "$PLAN_MONITOR_SHA" = "$REAL_MONITOR_SHA" ] || die "real pins differ from 577f8c94/ba031c23"
fi
note "mode=$MODE role=$ROLE outdir=$PLAN_OUTDIR"

# ---- 2. M-15 record FIRST (A142 item 6; M-15 (a)+(1))
if [ ! -e "$PLAN_RECORD" ] && [ "$ROLE" != seed ]; then
  [ "$MODE" = dry ] || die "NO_M15_RECORD: the seed serial launches first and writes the record (A143 D2; r3a L454)"
  note "DRY: no M-15 record yet; the seed serial writes it at its launch"
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
WORK="$WROOT/S0_${RUP}_SERIAL_${STAMP}_$$"
mkdir "$WORK"
"$PY" -I -B "$KIT" validate "${VARGS[@]}" --emit json --out "$WORK/plan.json" > /dev/null || die "plan"
if [ "$MODE" = launch ]; then
  OC=$("$PY" -I -B "$KIT" order-check --plan "$WORK/plan.json") || die "order: $OC"
fi

# ---- 3. fill from the V006-published handoff
[ -n "$PLAN_HANDOFF" ] || die "V006 has no HANDOFF_PIN S0_$RUP (RI45-09)"
[ "$(sha "$PLAN_FILLER")" = "$PLAN_FILLER_SHA" ] || die "filler sha"
"$PLAN_PY" -I -B "$PLAN_FILLER" --handoff "$PLAN_HANDOFF" --expected-sha256 "$PLAN_HANDOFF_SHA" --output-dir "$WORK/fill" \
  > "$WORK/fill.stdout.txt" 2>&1 || die "filler refused: $(cat "$WORK/fill.stdout.txt")"
FC=$("$PY" -I -B "$KIT" fill-check --plan "$WORK/plan.json" --fill-dir "$WORK/fill" --out "$WORK/fill_check.json") || die "fill-check: $FC"
SPEC="$WORK/fill/CALL_A_K32_A2_HEADLINE_C2V001.json"
SPEC_SHA=$(sha "$SPEC")
note "filled spec $SPEC sha256 $SPEC_SHA ($FC)"

# ---- 4. fresh dry plan (RI45-13): read the blocker lists
[ "$(sha "$PLAN_DRY")" = "$PLAN_DRY_SHA" ] || die "dry harness sha"
mkdir "$WORK/dry"
env -i PATH=/usr/bin:/bin HOME="${HOME:-/Users/bgm}" OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  "$PLAN_PY" -I -B "$PLAN_DRY" "$PLAN_DRIVER" "$PLAN_DRIVER_SHA" "$SPEC" "$SPEC_SHA" "$WORK/dry/report" "$WORK/dry/log.json" \
  > "$WORK/dry.stdout.txt" 2>&1 || die "dry harness failed: $(tail -c 2000 "$WORK/dry.stdout.txt")"
DV=$("$PY" -I -B "$KIT" dry-verdict --plan "$WORK/plan.json" --spec "$SPEC" --spec-sha256 "$SPEC_SHA" \
     --log "$WORK/dry/log.json" --report-dir "$WORK/dry/report" --out "$WORK/dry_verdict.json") || die "dry plan: $DV"
note "dry plan: $DV"

# ---- 5. per-point launch registry (exclusive create; DRY prints the entry)
REG=$("$PY" -I -B "$KIT" register --plan "$WORK/plan.json" --fill-check "$WORK/fill_check.json" --dry-verdict "$WORK/dry_verdict.json") || die "register: $REG"
[ "$MODE" = launch ] && note "registry: $REG"

# ---- 6. driver (and monitor) sha from bytes
[ "$(sha "$PLAN_DRIVER")" = "$PLAN_DRIVER_SHA" ] || die "driver sha differs from $PLAN_DRIVER_SHA"
[ "$(sha "$PLAN_MONITOR")" = "$PLAN_MONITOR_SHA" ] || die "monitor sha differs from $PLAN_MONITOR_SHA"

MON_CMD=("$PLAN_PY" -I -B "$PLAN_MONITOR" --driver "$PLAN_DRIVER" --driver-sha256 "$PLAN_DRIVER_SHA" --spec "$SPEC"
         --outdir "$PLAN_OUTDIR" --receipt "$PLAN_RECEIPT" --wall-cap-s "$PLAN_WALL" --rss-cap-bytes "$PLAN_RSS"
         --output-cap-bytes "$PLAN_OUTCAP")
CMDLINE=$("$PY" -I -B "$KIT" monitor-argv --plan "$WORK/plan.json" -- "${MON_CMD[@]}") || die "monitor argv form: $CMDLINE"

# ---- 7. admission and preconditions
if [ "$MODE" = launch ] || [ "$DRY_ADM" = 1 ]; then
  ADM=$("$PY" -I -B "$KIT" admission --plan "$WORK/plan.json" --spec "$SPEC" --spec-sha256 "$SPEC_SHA" --out "$WORK/admission.json") \
    || die "not admitted (sched v003): $ADM"
  note "admission: $ADM"
fi

if [ "$MODE" = dry ]; then
  [ -n "$PLAN_SPEC_PIN_SHA" ] || note "DRY: V006 has no SPEC_PIN S0_${RUP}_SERIAL yet; register $SPEC_SHA (RI45-13) before --launch"
  echo "DRY: nothing launched. The launch command would be:"
  echo "$CMDLINE"
  echo "DRY_SPEC_SHA256=$SPEC_SHA"
  echo "DRY_WORK=$WORK"
  exit 0
fi

E1=$("$PY" -I -B "$KIT" ext1-check --plan "$WORK/plan.json" --out "$WORK/ext1_check.json") || die "External1: $E1"
[ -n "$STEP2" ] || die "--step2-receipt is required with --launch (A135.5)"
S2=$("$PY" -I -B "$KIT" step2-check --plan "$WORK/plan.json" --receipt "$STEP2" --out "$WORK/step2_check.json") || die "step 2: $S2"
WC=$("$PY" -I -B "$KIT" watch-check --plan "$WORK/plan.json" --out "$WORK/watch_check.json") || die "memory watch: $WC"

# ---- 8. V006 freeze; the UTC second must advance past the record's
REC_EPOCH=$("$PY" -I -B "$KIT" record-epoch --plan "$WORK/plan.json") || die "record epoch"
while [ "$(date -u +%s)" -le "$REC_EPOCH" ]; do sleep 0.2; done
FZ=$("$PY" -I -B "$KIT" freeze-check --plan "$WORK/plan.json") || die "V006 write freeze: $FZ"
[ "$(sha "$PLAN_DRIVER")" = "$PLAN_DRIVER_SHA" ] || die "driver sha (immediately before launch)"
[ "$(sha "$PLAN_MONITOR")" = "$PLAN_MONITOR_SHA" ] || die "monitor sha (immediately before launch)"
[ "$(sha "$SPEC")" = "$PLAN_SPEC_PIN_SHA" ] || die "spec sha differs from the V006 SPEC_PIN"

# ---- 9. launch (root only)
cd /
note "LAUNCH: $CMDLINE"
nohup "${MON_CMD[@]}" > "$WORK/monitor.stdout.txt" 2> "$WORK/monitor.stderr.txt" < /dev/null &
MON_PID=$!
caffeinate -i -w "$MON_PID" > /dev/null 2>&1 < /dev/null &
note "monitor pid $MON_PID"

# ---- 10. launch receipt, hold check, launch record
n=0
while [ ! -e "$PLAN_LAUNCH_JSON" ] && [ "$n" -lt 600 ]; do
  kill -0 "$MON_PID" 2> /dev/null || break
  sleep 0.2; n=$((n + 1))
done
if [ ! -e "$PLAN_LAUNCH_JSON" ]; then
  echo "ALERT: no $PLAN_LAUNCH_JSON (monitor refused or failed); see $WORK/monitor.stdout.txt" >&2
  exit 5
fi
HOLD=0
if [ "$PLAN_SYNTHETIC" = 1 ]; then
  "$PY" -I -B "$KIT" gate-cli --plan "$WORK/plan.json" --which hold > "$WORK/hold_check.json" 2>&1 || HOLD=$?
else
  [ "$(sha "$PLAN_GATE")" = "$PLAN_GATE_SHA" ] || die "gate sha (hold check)"
  "$PLAN_PY" -I -B "$PLAN_GATE" --hold-check > "$WORK/hold_check.json" 2>&1 || HOLD=$?
fi
LRC=0
LREC=$("$PY" -I -B "$KIT" launch-record --plan "$WORK/plan.json" --work "$WORK" --spec "$SPEC" --spec-sha256 "$SPEC_SHA" \
       --mon-pid "$MON_PID" --hold-exit "$HOLD") || LRC=$?
note "launch record: $LREC"
if [ "$HOLD" = 3 ]; then
  echo "ALERT: --hold-check exits 3 after a serial launch: the tree is not classed NGC_SERIAL (A143 D3)" >&2
  exit 5
fi
[ "$LRC" = 0 ] || { echo "ALERT: launch record flags (exit $LRC): $LREC" >&2; [ "$LRC" = 4 ] && exit 4; exit 5; }
note "LAUNCHED. D4: alert if the measured route-A peak exceeds 22.4 GB. On the result: driver_sha256 = 577f8c94; reads stay validity-only."
exit 0
