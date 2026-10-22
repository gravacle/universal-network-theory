#!/bin/bash
# Supervisor: re-runs a Codex author agent whenever it stops, while STANDING_ORDER.md says PROCEED.
# Usage (in the terminal/account where that Codex is logged in):  keep_working.sh Codex2   (or Codex3)
# Stop: Ctrl-C, or set the first line of STANDING_ORDER.md to PAUSE.
NAME="${1:?usage: keep_working.sh <AgentName e.g. Codex2>}"
X=/Users/bgm/Research/UNT_EXCHANGE
CODEX=${CODEX_BIN:-/opt/homebrew/bin/codex}
LOG="$X/logs/${NAME}_supervisor.log"
OUTBOX="FROM_$(echo "$NAME" | tr '[:lower:]' '[:upper:]')"
PROMPT="You are ${NAME} on the UNT program (same Mac, existing project; no restart).
Read /Users/bgm/Research/UNT_EXCHANGE/STANDING_ORDER.md and README.md, then the newest messages in TO_CODEX/ and FROM_CODEX/, and run python3 /Users/bgm/Research/UNT_EXCHANGE/plan/plan.py.
Under principal decision D11 (TO_CODEX/0169) Codex root orchestrates: take your assignments from root's newest FROM_CODEX messages and your ACTIVE PLAN tasks (--by ${NAME}). If root has assigned nothing eligible, post one blocker notice and wait; do not invent work.
Do a full work block: post starts and finished packets as numbered immutable files in /Users/bgm/Research/UNT_EXCHANGE/${OUTBOX}/ and keep the PLAN current.
Rules: source and theory only; Codex root is the sole numerical launcher; no self-review; no deletion, moves, overwrites or network; work only in your assigned folders."
echo "$(date -u +%FT%TZ) supervisor start for $NAME" >> "$LOG"
while true; do
  if [ "$(head -1 "$X/STANDING_ORDER.md" | tr -d '[:space:]')" != "PROCEED" ]; then
    echo "$(date -u +%FT%TZ) switch not PROCEED; waiting" >> "$LOG"; sleep 300; continue
  fi
  echo "$(date -u +%FT%TZ) launching work block" >> "$LOG"
  "$CODEX" exec --skip-git-repo-check -C /Users/bgm/Research --sandbox workspace-write \
      -o "$X/logs/${NAME}_last_message.txt" "$PROMPT" >> "$X/logs/${NAME}_exec.log" 2>&1
  echo "$(date -u +%FT%TZ) work block ended (exit $?); next check in 5 min" >> "$LOG"
  sleep 300
done
