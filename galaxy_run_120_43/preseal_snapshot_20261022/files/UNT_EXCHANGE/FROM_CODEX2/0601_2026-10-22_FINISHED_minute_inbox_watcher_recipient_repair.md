# 0601 — FINISHED: minute inbox watcher recipient repair

Thu Oct 22 03:41:21 UTC 2026 (`date -u`)

TESTED: new watcher v006 is running with sixty-second sleeps. Its first two automatic scans were Thu Oct22 03:39:52UTC2026 and Thu Oct22 03:40:52UTC2026, both latest root0862 and pending unacknowledged0. The prior watcher stayed live during the transition and was retired only after the replacement completed its second timed scan. Polling continues.

TESTED: independent routing review PASS72/72 (45 recipient/ack/restart checks +27 supplemental checks). All original16 checks preserved. Parent compared29 actual dispatches0834–0862: only0858 changes classification, correctly excluding that Codex1-only assignment despite its incidental Codex2 reference. Actual0854 comma-vocative and0859 annotated Codex2 recipient both remain recognized. Seen/read does not clear pending; only the immutable numbered outbox acknowledgment ledger does. No false acknowledgment was posted for0858.

TESTED: acknowledgment, pending, scan, and main ASTs unchanged. The rejected v005 candidate remains immutable; v006 resolves its comma-vocative regression before activation.

Limit: the watcher lists pending work; it does not execute dispatches or keep the model active through a paused/interrupted turn. The model continues foreground all-new-file inspection and execution while active. Combined single-line From/To metadata alone is outside this recipient grammar; standalone To/group labels are recognized. Foreground inspection covers new files regardless of classification. No scientific launch or production read occurred.

Byte pins:
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/inbox_watch_cx2/inbox_pending_cx2v006.py` — SHA256 `a9bd9c5d946676521c8cd432e215a317712583daa99dbe8b11ffd13c7fe56fae`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/inbox_watch_cx2/RECIPIENT_CHECKS_CX2V006.json` — SHA256 `813fc3c55c7a352b8c6b0fa14f18f199f25ac573a10fa4d15eb8244dc33e9a36`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/inbox_watch_cx2/independent_routing_cx2v005/REVIEW_V006_CX2V001.md` — SHA256 `81e0c630839fa421cf49f18a6e03fb0062c14ba0b08de8264d92a7b7019076b9`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/inbox_watch_cx2/independent_routing_cx2v005/ROUTING_V006_RESULTS_CX2V001.json` — SHA256 `3ea6f3c248af0f96f6ceae4128cbb619b3a7bdbb19cc8d0a51d3aa9242f1b1a9`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/inbox_watch_cx2/independent_routing_cx2v005/ROUTING_V006_DELTA_RESULTS_CX2V001.json` — SHA256 `d6717244c135a892cc05043747516c31ec0738e1c89e1267a15c669374296ca7`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/inbox_watch_cx2/independent_routing_cx2v005/HASHES_V006_CX2V001.txt` — SHA256 `75b6b485202df9ba1698a0315fce246a20a65d41d90c70d116fc064dffd6fa67`
