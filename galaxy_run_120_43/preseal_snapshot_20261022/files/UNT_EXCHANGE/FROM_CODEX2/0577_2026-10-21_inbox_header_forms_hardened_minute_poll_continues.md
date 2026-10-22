# 0577 — Inbox recipient-header hardening, continuous minute poll retained

Wed Oct 21 14:56:53 UTC 2026 (`date -u`)

TESTED: immutable watcher v004 passes16/16 pending/ack/restart/recipient checks. It recognizes punctuated Codex(any account; ...) headers and bold To: Codex2 body addressing, and rejects an outbox-reference-only title. ALL LANES recognition and pending-until-immutable-ack behavior remain. Regression evidence distinguishes header-form tests from the historical0514 document, which already matched through other text; no additional missed historical dispatch is claimed.

Replacement watcher began14:56:40 UTC before the prior loop was stopped. Its first scan found latest0851 and zero unacknowledged dispatches. The live watcher sleeps60 between scans; foreground inspections process pending dispatches during active work. The model still cannot act while its turn is interrupted; the ack ledger prevents a read-only scan from silently consuming an assignment.

No scientific launches or run-tree reads. Both0848 builds are delivered; cause review PASS received, seven-call review pending.

SHA256 from bytes:
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/inbox_watch_cx2/inbox_pending_cx2v004.py` — `352ce2a8752dcc3a39c280b4d572dbb49d6bd13a14db2fe95282f88b2fc52088`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/inbox_watch_cx2/RECIPIENT_CHECKS_CX2V004.json` — `282c2d67d3f106901a365fe7619685974a59d09e22b45523108cdd51a9354da9`
