#!/bin/bash
# launch_twin_root_c2v003.sh -- root's launch of the cw8 identity twin at the seed theta (s0_launch_kit_c2, C2V003).
#
# DEFAULT IS DRY: checks, prints the monitor and kill-watch commands, launches nothing.  Only --launch starts root_monitor.
# V006 A166: the twin may start any time after the seed serial's LAUNCH record.  No gate admission (--twin-start-check),
#          no wave-state attestation, no post-launch gate reading; the RSS cap is physical RAM (137438953472 B); wall
#          22752 s and output 32 GiB unchanged.
# D3 form: exact --driver-sha256 <64 hex>, absolute --spec.  After the start, the launch record (<receipt>.launch.json)
#          must match the plan; otherwise the twin is stopped at once: a procedural mis-launch, recorded, relaunched as
#          --attempt k+1 in the same launch root.
# A141 L4: twin_kill_watch_c2v003.sh stops the twin once iteration_0001 COMPLETED.json and the sidecar iteration record
#          exist (a planned stop to save compute, never a failure; the twin is never a member).
#
# Usage:
#   launch_twin_root_c2v003.sh --launch-root DIR --run-root /Volumes/External1/NGC_<NAME>
#       [--attempt K] [--step2-receipt ABS_PATH] [--launch] [--dry-fill-dir DIR] [--watch-poll-s 30]
#       [--synthetic-pins FILE --synthetic-pins-sha256 H]
# Exit: 0 done (DRY: printed), 3 refused, 4 launched with an order flag, 5 alert (mis-launch stopped, or no launch record
#       from the monitor), 2 usage.
set -euo pipefail
set -o noclobber
umask 022
export PATH=/usr/bin:/bin:/usr/sbin:/sbin
export LC_ALL=C

KIT_SHA='e58c8605fd35d8894d214ee3e06fa83d9577b14efdaa960938bf2bb330676e73'
WATCH_SHA='88e7c8981959036fccc45fdb60ff551555ea66c15a137d74025414ee864f9a14'
REAL_DRIVER_SHA='577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377'
REAL_MONITOR_SHA='ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107'
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
KIT_DIR=$(cd "$(dirname "$0")" && pwd -P)
KIT="$KIT_DIR/s0_kit_c2v003.py"
WATCH="$KIT_DIR/twin_kill_watch_c2v003.sh"

die() { echo "REFUSED: $*" >&2; exit 3; }
note() { echo "[s0-twin $(date -u +%Y-%m-%dT%H:%M:%SZ)] $*"; }
sha() { shasum -a 256 "$1" | awk '{print $1}'; }
need_arg() { [ "$1" -ge 2 ] || die "missing value for $2"; }

[ -f "$KIT" ] && [ "$(sha "$KIT")" = "$KIT_SHA" ] || die "kit helper sha differs from $KIT_SHA"
[ -f "$WATCH" ] && [ "$(sha "$WATCH")" = "$WATCH_SHA" ] || die "kill-watch sha differs from $WATCH_SHA"

LAUNCH=0; LR=""; RR=""; STEP2=""; SP=""; SPH=""; DRY_FILL=""; ATTEMPT=1
WPOLL=30
while [ $# -gt 0 ]; do
  case "$1" in
    --launch-root) need_arg $# "$1"; LR="$2"; shift 2 ;;
    --run-root) need_arg $# "$1"; RR="$2"; shift 2 ;;
    --attempt) need_arg $# "$1"; ATTEMPT="$2"; shift 2 ;;
    --step2-receipt) need_arg $# "$1"; STEP2="$2"; shift 2 ;;
    --dry-fill-dir) need_arg $# "$1"; DRY_FILL="$2"; shift 2 ;;
    --watch-poll-s) need_arg $# "$1"; WPOLL="$2"; shift 2 ;;
    --synthetic-pins) need_arg $# "$1"; SP="$2"; shift 2 ;;
    --synthetic-pins-sha256) need_arg $# "$1"; SPH="$2"; shift 2 ;;
    --launch) LAUNCH=1; shift ;;
    *) die "unknown argument: $1" ;;
  esac
done
case "$ATTEMPT" in [1-9]|[1-9][0-9]) ;; *) die "--attempt must be an integer 1..99" ;; esac
case "$WPOLL" in ''|*[!0-9]*) die "--watch-poll-s must be an integer" ;; esac
MODE=dry; [ "$LAUNCH" = 1 ] && MODE=launch
[ -n "$LR" ] && [ -n "$RR" ] || die "--launch-root and --run-root are required"
VARGS=(--role seed --call twin --mode "$MODE" --launch-root "$LR" --run-root "$RR" --attempt "$ATTEMPT")
if [ -n "$SP" ] || [ -n "$SPH" ]; then VARGS+=(--synthetic-pins "$SP" --synthetic-pins-sha256 "$SPH"); fi

# ---- 1. validate (no writes)
PLAN_SH=$("$PY" -I -B "$KIT" validate "${VARGS[@]}" --emit shell) || die "validate: $PLAN_SH"
eval "$PLAN_SH"
if [ "$PLAN_SYNTHETIC" = 0 ]; then
  [ "$PLAN_DRIVER_SHA" = "$REAL_DRIVER_SHA" ] && [ "$PLAN_MONITOR_SHA" = "$REAL_MONITOR_SHA" ] || die "real pins differ from 577f8c94/ba031c23"
fi
note "mode=$MODE attempt=$PLAN_ATTEMPT outdir=$PLAN_OUTDIR"

# ---- 2. order: the M-15 record and the seed serial's confirmed launch record exist (seed first; then any time, A166)
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
if [ "$MODE" = launch ]; then WROOT="$LR/work"; else WROOT="$LR/dry"; fi
[ -d "$WROOT" ] || mkdir "$WROOT"
WORK="$WROOT/S0_SEED_CW8_TWIN_A${PLAN_ATTEMPT}_${STAMP}_$$"
mkdir "$WORK"
"$PY" -I -B "$KIT" validate "${VARGS[@]}" --emit json --out "$WORK/plan.json" > /dev/null || die "plan"
if [ "$MODE" = launch ]; then
  OC=$("$PY" -I -B "$KIT" order-check --plan "$WORK/plan.json") || die "order: $OC"
fi

# ---- 3. the twin spec of the seed's fill (the same filler run as the serial call of record)
if [ -e "$PLAN_SEED_REGISTRY" ]; then
  FILL_DIR=$("$PY" -I -B -c 'import json,sys; print(json.load(open(sys.argv[1]))["fill_dir"])' "$PLAN_SEED_REGISTRY")
  [ -z "$DRY_FILL" ] || [ "$MODE" = dry ] || die "--dry-fill-dir is DRY only"
elif [ "$MODE" = dry ] && [ -n "$DRY_FILL" ]; then
  FILL_DIR="$DRY_FILL"
else
  die "no seed registry entry ($PLAN_SEED_REGISTRY); DRY may pass --dry-fill-dir of a seed DRY run"
fi
FC=$("$PY" -I -B "$KIT" fill-check --plan "$WORK/plan.json" --fill-dir "$FILL_DIR" --out "$WORK/fill_check.json") || die "fill-check (twin): $FC"
SPEC="$FILL_DIR/CALL_A_K32_A2_HEADLINE_CW8_TWIN_C2V001.json"
SPEC_SHA=$(sha "$SPEC")
note "twin spec $SPEC sha256 $SPEC_SHA"

# ---- 4. fresh dry plan of the twin spec (RI45-13)
[ "$(sha "$PLAN_DRY")" = "$PLAN_DRY_SHA" ] || die "dry harness sha"
mkdir "$WORK/dry"
env -i PATH=/usr/bin:/bin HOME="${HOME:-/Users/bgm}" OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  "$PLAN_PY" -I -B "$PLAN_DRY" "$PLAN_DRIVER" "$PLAN_DRIVER_SHA" "$SPEC" "$SPEC_SHA" "$WORK/dry/report" "$WORK/dry/log.json" \
  > "$WORK/dry.stdout.txt" 2>&1 || die "dry harness failed: $(tail -c 2000 "$WORK/dry.stdout.txt")"
DV=$("$PY" -I -B "$KIT" dry-verdict --plan "$WORK/plan.json" --spec "$SPEC" --spec-sha256 "$SPEC_SHA" \
     --log "$WORK/dry/log.json" --report-dir "$WORK/dry/report" --out "$WORK/dry_verdict.json") || die "dry plan: $DV"

# ---- 5. registry
REG=$("$PY" -I -B "$KIT" register --plan "$WORK/plan.json" --fill-check "$WORK/fill_check.json" --dry-verdict "$WORK/dry_verdict.json") || die "register: $REG"

# ---- 6. driver / monitor sha; exact argv (twin caps 22752 / 137438953472 (RAM) / 34359738368)
[ "$(sha "$PLAN_DRIVER")" = "$PLAN_DRIVER_SHA" ] || die "driver sha"
[ "$(sha "$PLAN_MONITOR")" = "$PLAN_MONITOR_SHA" ] || die "monitor sha"
MON_CMD=("$PLAN_PY" -I -B "$PLAN_MONITOR" --driver "$PLAN_DRIVER" --driver-sha256 "$PLAN_DRIVER_SHA" --spec "$SPEC"
         --outdir "$PLAN_OUTDIR" --receipt "$PLAN_RECEIPT" --wall-cap-s "$PLAN_WALL" --rss-cap-bytes "$PLAN_RSS"
         --output-cap-bytes "$PLAN_OUTCAP")
CMDLINE=$("$PY" -I -B "$KIT" monitor-argv --plan "$WORK/plan.json" -- "${MON_CMD[@]}") || die "monitor argv form: $CMDLINE"
WATCH_BASE=(/bin/bash "$WATCH" --launch-root "$LR" --launch-json "$PLAN_LAUNCH_JSON" --outdir "$PLAN_OUTDIR"
            --twin-spec-sha256 "$SPEC_SHA" --poll-s "$WPOLL" --kill)

# ---- 7. (V006 A166: no wave-state attestation and no gate admission; the twin starts any time after the seed's LAUNCH)
if [ "$MODE" = dry ]; then
  echo "DRY: nothing launched. The twin launch command would be:"
  echo "$CMDLINE"
  echo "After the launch: the launch-record check (<receipt>.launch.json against the plan; RSS cap = RAM); no gate reading (A166)."
  echo "Then the kill watch (A141 L4), with the twin's monitor pid:"
  printf '%q ' "${WATCH_BASE[@]}"; echo "--mon-pid <monitor pid>"
  echo "DRY_TWIN_SPEC_SHA256=$SPEC_SHA"
  exit 0
fi

E1=$("$PY" -I -B "$KIT" ext1-check --plan "$WORK/plan.json" --out "$WORK/ext1_check.json") || die "External1: $E1"
[ -n "$STEP2" ] || die "--step2-receipt is required with --launch (A135.5)"
S2=$("$PY" -I -B "$KIT" step2-check --plan "$WORK/plan.json" --receipt "$STEP2" --out "$WORK/step2_check.json") || die "step 2: $S2"
WC=$("$PY" -I -B "$KIT" watch-check --plan "$WORK/plan.json" --out "$WORK/watch_check.json") || die "memory watch: $WC"
[ "$(sha "$PLAN_DRIVER")" = "$PLAN_DRIVER_SHA" ] || die "driver sha (immediately before launch)"
[ "$(sha "$PLAN_MONITOR")" = "$PLAN_MONITOR_SHA" ] || die "monitor sha (immediately before launch)"
[ "$(sha "$SPEC")" = "$PLAN_SPEC_PIN_SHA" ] || die "twin spec sha differs from the V006 SPEC_PIN S0_SEED_CW8_TWIN"

# ---- 8. launch (root only)
cd /
note "LAUNCH TWIN (attempt $PLAN_ATTEMPT): $CMDLINE"
nohup "${MON_CMD[@]}" > "$WORK/monitor.stdout.txt" 2> "$WORK/monitor.stderr.txt" < /dev/null &
MON_PID=$!
caffeinate -i -w "$MON_PID" > /dev/null 2>&1 < /dev/null &
n=0
while [ ! -e "$PLAN_LAUNCH_JSON" ] && [ "$n" -lt 600 ]; do
  kill -0 "$MON_PID" 2> /dev/null || break
  sleep 0.2; n=$((n + 1))
done
[ -e "$PLAN_LAUNCH_JSON" ] || { echo "ALERT: no $PLAN_LAUNCH_JSON; see $WORK/monitor.stdout.txt" >&2; exit 5; }

# ---- 9. launch-record check: the twin's launch record matches the plan; otherwise stop it at once
KC=0
KV=$("$PY" -I -B "$KIT" launch-check --plan "$WORK/plan.json" --mon-pid "$MON_PID" --spec "$SPEC" --spec-sha256 "$SPEC_SHA" \
     --out "$WORK/launch_verdict.json") || KC=$?
note "launch check: $KV"
RARGS2=(--plan "$WORK/plan.json" --work "$WORK" --spec "$SPEC" --spec-sha256 "$SPEC_SHA" --mon-pid "$MON_PID"
        --launch-verdict "$WORK/launch_verdict.json")
if [ "$KC" != 0 ]; then
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
  echo "MISLAUNCH_STOPPED (procedural, not a scientific failure): twin launch check exit $KC, stop $RES; $(cat "$WORK/mislaunch_record.out")" >&2
  echo "Relaunch: the same command with --attempt $((PLAN_ATTEMPT + 1)) in this launch root (same M-15 record), once root has recorded the mis-launch." >&2
  exit 5
fi

# ---- 10. the A141 L4 kill watch, then the launch record
nohup "${WATCH_BASE[@]}" --mon-pid "$MON_PID" > "$WORK/kill_watch.out.txt" 2>&1 < /dev/null &
WATCH_PID=$!
LRC=0
LREC=$("$PY" -I -B "$KIT" launch-record --outcome LAUNCH "${RARGS2[@]}" --watch-pid "$WATCH_PID") || LRC=$?
note "launch record: $LREC; kill watch pid $WATCH_PID"
[ "$LRC" = 0 ] || { echo "ALERT: launch record flags (exit $LRC): $LREC" >&2; [ "$LRC" = 4 ] && exit 4; exit 5; }
note "TWIN LAUNCHED; launch record matches the plan (RSS cap = RAM); the kill watch stops it after iteration 1 COMPLETED + sidecar (A141 L4)."
exit 0
