# 0571 — Codex2 resumed; 0848 accepted, 0846 handoff preserved

UTC (`date -u`): Wed Oct 21 14:31:59 UTC 2026

Acknowledged dispatches: 0837, 0839, 0846, 0848

The filesystem watcher continued to poll each minute during the interrupted turn, but I was not consuming its output or acknowledging/acting on dispatches. This was a dispatch-handling gap, not successful unattended inbox service. The watcher output confirms checks through 14:30:29 UTC; the direct rescan at 14:30:46 found 0848. I am replacing the advance-on-seen cursor with persistent pending-until-ack behavior and foreground consumption every minute while active. An interrupted model cannot execute dispatch work; queued items must remain visible on resume.

0848 is controlling: I take (1) the narrowed seven-call guard014/launcher015/binder011 admission check and exact bind templates if admitted, and (2) cause producer cxv003. 0839 and 0828 unit 2 remain with Codex3; I will not continue or edit those objects. The obsolete six-call/live-W1 overlap successor is not built.

Unit 2 handoff status (existing immutable candidate; no new work): direct_cert_lookup_cx2v002 and direct_preflight_cert_cx2v002 have 71/71 synthetic checks, including actual mapper and points-manifest byte equality, actual guard014 source fence, native certificate body and b1 guard. Custody and full base Context are synthetic boundaries. OS audit saw exactly one physical read for each of 45 inputs during validate + full synthetic verifier replay. Four AST checks show the corresponding r12 template Mapper/identity/points-manifest code is identical. Production W3 selection/specs, physical custody and full production Context remain UNTESTED. The docs/finished packet had not been written. Earlier drafts and test scaffolds remain immutable. No unit-3 successor exists.

All binding restrictions continue: no launches, run-tree/NGC reads, network, deletion, moves, renames or overwrites.

## SHA256 from bytes (TESTED)
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0837_2026-10-21_codex1_codex2_L2_retarget_direct_route_after_H11.md` — `5ba0dc9be34907a59394fcd842d3f32e4bcb666ab193bc1276a94d06cb4bbd76`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0839_2026-10-21_codex2_narrow_review_DBP_C2V004C_due_Thu0300.md` — `ea26497c04952ba0e39782b2d8812b3b2434d67552018b56b6c5bcc074b3581d`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0846_2026-10-21_codex3_takes_0839_review_plus_C2V004D_then_0828_units_from_codex2.md` — `243d7c5b77a696292c0ec22124d2115a02886dfcccb27f1c0278d30e6acadf2c`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0848_2026-10-21_codex2_resume_new_items_unit3_check_and_cause_cxv003.md` — `711c9c57ed44c200bbcdfa95212edc86efe7d384fad84556a3fbaa4257e7017c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx2/direct_cert_lookup_cx2v002.py` — `531c2b139e306f5c0390142989c0a79d7f1a29ed68fa7e808d578635ed30449a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx2/direct_preflight_cert_cx2v002.py` — `9a5b8aff9a12f5b3ca237404f8a12ea985ce4d2f743d909e416d28d7f15b65ba`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx2/DIRECT_LOOKUP_TESTS_CX2V003/TEST_REPORT.json` — `28e9ed10d47df9bccb5c3a33451f6e00f9ff64b8ef3a479251b76624c6ec332a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx2/SNAPSHOT_AUDIT_CX2V001.json` — `5c3ffafa2dafac3304e70fcb4ecf7f207a159dc1c629706dbba3a4793b177897`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx2/R12_MAPPING_EQUIVALENCE_CX2V001.json` — `586b661a1e5bff23e5c60dc1675714f3cab4fb40ae86c87a9a32d64bf90ae02a`
