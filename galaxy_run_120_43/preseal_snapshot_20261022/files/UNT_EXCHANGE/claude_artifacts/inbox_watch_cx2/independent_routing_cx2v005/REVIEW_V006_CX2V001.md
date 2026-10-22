# Independent watcher v006 routing review

`date -u`: Thu Oct 22 03:40:28 UTC 2026

**PASS within the tested routing scope: 72/72 checks (45 baseline/extension + 27 actual-dispatch/delta checks).** Candidate v006 bytes were verified before and after testing. This review did not start, replace, scan, or stop any watcher and did not execute any dispatch.

TESTED: all original 16 behaviors remain; direct/shared recipients, comma/and/plus/ampersand/slash groups, separate explicit To lines, ALL LANES, any-account, annotations, quoted/fenced exclusions, Codex20 rejection, ordinary-mention rejection, exact acknowledgment semantics, and restart behavior pass. Actual 0854 comma address and 0859 annotated address select Codex2. Actual 0858 selects no Codex2 task despite its later Codex2 reference. A pending list containing those three selects only 0854 and 0859.

TESTED: v004's actual0858 false positive and v005's actual0854 false negative are reproduced. The unchanged 45-case harness scores v004 28/45 (all original16 pass); v006 scores45/45. The supplemental suite scores27/27. The first supplemental harness stopped before producing a result because the review harness looked up `854_` instead of `0854_`; preserved v002 corrects only this filename formatting error. No candidate source was edited.

FORMAL, supported by AST comparisons: v004-to-v006 changes are confined to the recipient routing function, new ROLE/JOIN expressions, and recipient_label helper. number, acknowledgments, pending, scan, self_test, main, and all remaining module statements are AST-identical. A leading recipient list is collected before task prose: later Codex2 mentions after another recipient's colon do not grant routing. A comma after an already recognized recipient supports the actual0854 vocative; it does not turn later prose into recipient membership. The existing unused ADDRESSEE constant confers no routing authority in v006.

Boundary note: one-line combined `From: Claude2; To: Codex2` metadata is not recognized; a separate leading `To: Codex2` line is recognized. This is an explicitly observed grammar limit, not a claim of universal prose/Markdown interpretation. The tested FROM_CODEX titles and standalone recipient forms pass. No claim is made about every future title or metadata format.

UNTESTED: actual scan I/O, live poll continuity, replacement lifecycle, and execution/completion of dispatched work. Parent owns those operations. Inert module loading used `__name__` other than `__main__`, then only pure routing/ack/pending functions were called; scan was replaced by a tripwire. No run trees, target data, network, session logs, or scientific code were accessed.

Runtime: approved isolated Python with `-I -B`, standard library only, all specified BLAS thread variables set to1; `nice unavailable (sandbox); 0514 waiver`.

Every cited file and its actual byte SHA256 follows. Result files contain the individual expectations, observations, and final byte-stability checks.

| File | SHA256 |
|---|---|
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/inbox_watch_cx2/inbox_pending_cx2v004.py | `352ce2a8752dcc3a39c280b4d572dbb49d6bd13a14db2fe95282f88b2fc52088` |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/inbox_watch_cx2/inbox_pending_cx2v005.py | `c49f7774fba8f9bdef6248dde7d389c04f2d65c1dc7c43abe480715917c08161` |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/inbox_watch_cx2/inbox_pending_cx2v006.py | `a9bd9c5d946676521c8cd432e215a317712583daa99dbe8b11ffd13c7fe56fae` |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/inbox_watch_cx2/independent_routing_cx2v005/probe_routing_cx2v005_v001.py | `1e640cdd0b345f765e9969d71ed3cabb4752383f42574f14c58b30b47fca96c8` |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/inbox_watch_cx2/independent_routing_cx2v005/probe_routing_delta_cx2v006_v001.py | `e5fed13ff7a89f362bd74792ed92c350afa1ed246134c6d99aeea419103fdd18` |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/inbox_watch_cx2/independent_routing_cx2v005/probe_routing_delta_cx2v006_v002.py | `6e41f7bba6e1d573225b2f8b19d6e7af9b682b0ba59231dbf2b501bccda8ef12` |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/inbox_watch_cx2/independent_routing_cx2v005/LEGACY_ROUTING_RESULTS_CX2V001.json | `c032a220b96919f0e5a92120c79eb8c255ea204bd89a1d4408291f73f3320cab` |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/inbox_watch_cx2/independent_routing_cx2v005/ROUTING_V006_RESULTS_CX2V001.json | `3ea6f3c248af0f96f6ceae4128cbb619b3a7bdbb19cc8d0a51d3aa9242f1b1a9` |
| /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/inbox_watch_cx2/independent_routing_cx2v005/ROUTING_V006_DELTA_RESULTS_CX2V001.json | `d6717244c135a892cc05043747516c31ec0738e1c89e1267a15c669374296ca7` |
| /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0854_2026-10-21_codex2_independent_eps_consumption_analysis_then_rule_successor_standby.md | `9669f5d4fa93931ad0d546d2ac9834f962ad946b57f45a3695023a92b234ae5c` |
| /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0858_2026-10-22_codex1_resume_importer_status_and_inbox_fix.md | `4cff96e883191cbfc6402feb26dbb6b3d7d97025f2f34708977ac973c15e18b7` |
| /Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0859_2026-10-22_codex2_prestage_post_C1_pin_successors.md | `e9e51aa7e6b3d7dce35a63b4ba2509da2216fbd135a73e6e73e77917226890da` |
