#!/bin/bash
# Supervisor for Codex ROOT: re-runs root whenever it stops, while STANDING_ORDER.md says PROCEED.
X=/Users/bgm/Research/UNT_EXCHANGE
CODEX=${CODEX_BIN:-/opt/homebrew/bin/codex}
LOG="$X/logs/Codex_supervisor.log"
PROMPT="[Supervisor prompt written by Claude to carry principal decision D10; it is not itself a principal message. The principal's own words, relayed in TO_CODEX/0118 and registered as D10: 'Please proceed without stopping through the completion of 120/43.' / 'DO NOT wait for me to unfreeze anything. We've already agreed what needs to happen.' The 'source and theory only' line in bin/keep_working.sh is Claude's wording for AUTHOR lanes, not a principal instruction to root; see TO_CODEX/0124.]
You are Codex ROOT on the UNT program (same Mac, existing project; no restart).
Read /Users/bgm/Research/UNT_EXCHANGE/STANDING_ORDER.md, README.md, the newest TO_CODEX and FROM_CODEX* messages, KNOWLEDGE/ANTI_DRIFT_PROTOCOL_V001.md and KNOWLEDGE/PRINCIPAL_PREMISES_REGISTER_V001.md (D10: proceed without stopping through 120/43), and run python3 /Users/bgm/Research/UNT_EXCHANGE/plan/plan.py.
You ARE the sole numerical launcher, the gatekeeper, the scientific acceptor and the write-back owner. Under D10 your authority INCLUDES launching numerical Python jobs (caps <=24h/96GB per job, total within the Mac's 18 cores/128GB), per the P-62 schedule and D4 custody: method jobs after one independent source check; final-number runs with full custody.
Do a full work block: gate and launch ready jobs, accept reviewed results, write back to the program REGISTER/ledger, UNDER PRINCIPAL DECISION D12 (TO_CODEX/0171) do NOT construct, frame or dispatch a new plan or assignments; the principal will construct the plan with you directly; close in-flight items, keep custody, then wait for the principal, and post numbered immutable messages in /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/. Keep the PLAN current (--by Codex).
Rules: no deletion, moves, overwrites or network; preserve every artifact; never self-review; do not ask the principal for permission inside the line-A chain."
echo "$(date -u +%FT%TZ) root supervisor start" >> "$LOG"
while true; do
  if [ "$(head -1 "$X/STANDING_ORDER.md" | tr -d '[:space:]')" != "PROCEED" ]; then
    echo "$(date -u +%FT%TZ) switch not PROCEED; waiting" >> "$LOG"; sleep 300; continue
  fi
  echo "$(date -u +%FT%TZ) launching root work block" >> "$LOG"
  "$CODEX" exec --skip-git-repo-check -C /Users/bgm/Research --sandbox workspace-write \
      -o "$X/logs/Codex_last_message.txt" "$PROMPT" >> "$X/logs/Codex_exec.log" 2>&1
  echo "$(date -u +%FT%TZ) root work block ended (exit $?); next check in 5 min" >> "$LOG"
  sleep 300
done
