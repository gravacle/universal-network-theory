#!/usr/bin/env python3
"""Exit (notifying Claude) when any watched author shows no outbox/PLAN activity for LIMIT seconds.
Usage: idle_watch.py [LIMIT_SECONDS] [Agent ...]   default 1500 Codex2 Codex3"""
import os, sys, time
X = "/Users/bgm/Research/UNT_EXCHANGE"
limit = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
agents = sys.argv[2:] or ["Codex2", "Codex3"]
def sig(a):
    ob = os.path.join(X, "FROM_" + a.upper())
    files = sorted(os.listdir(ob)) if os.path.isdir(ob) else []
    n = sum(1 for line in open(os.path.join(X, "plan/plan_log.tsv")) if f"\t{a}\t" in line)
    return (files[-1] if files else "", n)
last = {a: time.time() for a in agents}; prev = {a: sig(a) for a in agents}
while True:
    if open(os.path.join(X, "STANDING_ORDER.md")).readline().strip() != "PROCEED":
        time.sleep(60); last = {a: time.time() for a in agents}; continue
    for a in agents:
        s = sig(a)
        if s != prev[a]: prev[a] = s; last[a] = time.time()
        if time.time() - last[a] >= limit:
            print(f"IDLE: {a} has no outbox/PLAN activity for {limit//60} min ({time.strftime('%H:%MZ', time.gmtime())})", flush=True)
            sys.exit(0)
    time.sleep(60)
