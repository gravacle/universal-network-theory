#!/bin/bash
# twin_kill_watch_c2v002.sh -- A141 L4 kill trigger for the cw8 identity twin (s0_launch_kit_c2, C2V002).
#
# The twin's planned stop: once <outdir>/stages/NN_route_a/checkpoint/iteration_0001/COMPLETED.json AND
# <outdir>/stages/NN_route_a/uv_tail_sidecar/iteration_0001.json both exist, stop the twin's driver process group
# (SIGTERM, then SIGKILL after 15 s).  root_monitor then writes its receipt.  The stop is planned, not a failure
# (A135 item 3; A133 section 3(c)); the twin is never a member and its values are never read.
# Existence checks only; no record content is read.  Before any kill, the target is verified: the launch record's
# child is alive, leads its own group, runs exactly the launch record's command, its parent is the twin's monitor
# (--mon-pid, when given), and that command's spec is the registered twin (sha256, column_workers 8).
# C2V002: kill-target takes --spec-sha256/--expect-leaf/--mon-pid; the kill record is named after the outdir (attempts).
#
# DEFAULT IS DRY: reports WOULD_KILL and exits.  --kill sends the signals and writes the kill record (exclusive create).
# Usage:
#   twin_kill_watch_c2v002.sh --launch-root DIR --launch-json <receipt>.launch.json --outdir <twin outdir>
#       --twin-spec-sha256 H [--mon-pid PID] [--kill] [--poll-s 30] [--once] [--max-wait-s 30000]
# Exit: 0 trigger handled (or the twin ended by itself, or max wait reached), 1 not met (--once), 3 refused.
set -euo pipefail
set -o noclobber
umask 022
export PATH=/usr/bin:/bin:/usr/sbin:/sbin
export LC_ALL=C

KIT_SHA='0ba823f3fbd11e80547bcf43e8db0538594f5c3c1e21b4014016a40a7f66d109'
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
KIT_DIR=$(cd "$(dirname "$0")" && pwd -P)
KIT="$KIT_DIR/s0_kit_c2v002.py"

die() { echo "REFUSED: $*" >&2; exit 3; }
note() { echo "[twin-watch $(date -u +%Y-%m-%dT%H:%M:%SZ)] $*"; }
sha() { shasum -a 256 "$1" | awk '{print $1}'; }
need_arg() { [ "$1" -ge 2 ] || die "missing value for $2"; }

[ -f "$KIT" ] && [ "$(sha "$KIT")" = "$KIT_SHA" ] || die "kit helper sha differs from $KIT_SHA"

LR=""; LJ=""; OUT=""; TSHA=""; KILL=0; POLL=30; ONCE=0; MAXW=30000; MPID=""
while [ $# -gt 0 ]; do
  case "$1" in
    --launch-root) need_arg $# "$1"; LR="$2"; shift 2 ;;
    --launch-json) need_arg $# "$1"; LJ="$2"; shift 2 ;;
    --outdir) need_arg $# "$1"; OUT="$2"; shift 2 ;;
    --twin-spec-sha256) need_arg $# "$1"; TSHA="$2"; shift 2 ;;
    --mon-pid) need_arg $# "$1"; MPID="$2"; shift 2 ;;
    --poll-s) need_arg $# "$1"; POLL="$2"; shift 2 ;;
    --max-wait-s) need_arg $# "$1"; MAXW="$2"; shift 2 ;;
    --kill) KILL=1; shift ;;
    --once) ONCE=1; shift ;;
    *) die "unknown argument: $1" ;;
  esac
done
case "$POLL$MAXW$MPID" in *[!0-9]*) die "--poll-s, --max-wait-s and --mon-pid must be integers" ;; esac
[ -n "$LR" ] && [ -n "$LJ" ] && [ -n "$OUT" ] && [ -n "$TSHA" ] || die "--launch-root, --launch-json, --outdir, --twin-spec-sha256 are required"
case "$LJ" in /*.receipt.json.launch.json) ;; *) die "--launch-json must be an absolute <receipt>.launch.json" ;; esac
case "$OUT" in /*) ;; *) die "--outdir must be absolute" ;; esac
[ "${LJ%.receipt.json.launch.json}" = "$OUT" ] || die "--launch-json does not belong to --outdir"
RECEIPT="${LJ%.launch.json}"
[ -e "$LJ" ] || die "no launch record $LJ"
MP_ARG=(); [ -n "$MPID" ] && MP_ARG=(--mon-pid "$MPID")

waited=0
while :; do
  if [ -e "$RECEIPT" ]; then
    note "the twin's monitor receipt exists (the twin ended by itself: wall cap or exit); nothing to stop"
    exit 0
  fi
  TR=0
  TJ=$("$PY" -I -B "$KIT" twin-trigger --outdir "$OUT") || TR=$?
  if [ "$TR" = 3 ]; then die "trigger check: $TJ"; fi
  if [ "$TR" = 0 ]; then
    note "TRIGGER MET (A141 L4): $TJ"
    PGID=$("$PY" -I -B "$KIT" kill-target --launch-json "$LJ" --spec-sha256 "$TSHA" --expect-leaf 8 ${MP_ARG[@]+"${MP_ARG[@]}"}) \
      || die "kill target not verified; NOT killing"
    if [ "$KILL" != 1 ]; then
      echo "DRY: WOULD_KILL process group $PGID (kill -TERM -- -$PGID; KILL after 15 s)"
      exit 0
    fi
    kill -TERM -- "-$PGID" 2> /dev/null || true
    k=0; while kill -0 -- "-$PGID" 2> /dev/null && [ "$k" -lt 75 ]; do sleep 0.2; k=$((k + 1)); done
    RES=KILLED_TERM
    if kill -0 -- "-$PGID" 2> /dev/null; then kill -KILL -- "-$PGID" 2> /dev/null || true; RES=KILLED_KILL; fi
    KR=$("$PY" -I -B "$KIT" kill-record --launch-root "$LR" --launch-json "$LJ" --outdir "$OUT" --pgid "$PGID" \
         --result "$RES" --reason ITERATION_0001_COMPLETED_AND_SIDECAR) || die "kill record: $KR"
    note "twin stopped ($RES): $KR"
    exit 0
  fi
  [ "$ONCE" = 1 ] && { note "not met: $TJ"; exit 1; }
  [ "$waited" -ge "$MAXW" ] && { note "max wait ${MAXW}s reached; the monitor's wall cap governs"; exit 0; }
  sleep "$POLL"; waited=$((waited + POLL))
done
