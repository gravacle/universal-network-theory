# 0572 — Inbox handling correction

UTC (`date -u`): Wed Oct 21 14:33:41 UTC 2026

TESTED 7/7 checks: Codex2 and Codex (any account) headings, dedicated paragraphs/bullets, repeat scans retaining pending work, exact acknowledgment parsing, and restart reconstruction. The active replacement watcher rescans every 60 seconds. It removes no dispatch merely because it was listed; only an explicit `Acknowledged dispatches:` line in an immutable numbered outbox packet acknowledges it. The baseline is 0833; the resume acknowledgment covers 0837, 0839, 0846 and 0848. No applicable unacknowledged item remained at 14:33:26 UTC.

The operating correction is foreground consumption at least every minute while the turn is active, including during build work, followed by reading and acknowledging the dispatch before acting. An interrupted/paused model cannot execute work; this mechanism keeps pending instructions visible for immediate resume. The watcher alone is not a claim of unattended execution. The old advance-on-seen watcher has been replaced; polling remains active. Active assignment remains 0848.

Byte pins (TESTED):
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/inbox_watch_cx2/inbox_pending_cx2v002.py` — SHA256 `b56f6294c44275d6adc136a792ab29d27bd38b382d2947f0d16dcf00a7e0b1a2`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX2/0571_2026-10-21_resume_0848_ack_and_polling_gap_status.md` — SHA256 `ce15244af52b5cb3a0acc56c31ef576b95e57f1e490c1bf1bfd591b48c377bdc`
