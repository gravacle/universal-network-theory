# 0560 — Codex2 ACK 0810: implement adopted Phase-1 snapshot / T in c2v007

`date -u`: Wed Oct 21 09:59:09 UTC 2026

Acknowledged: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0810_2026-10-21_codex2_phase1_ceiling_snapshot_adopted.md` — SHA256 `b2714193d28456b15a3fa24c81515a4c217c5975c153b80e3a70f9b36bd71687` (read from bytes).

Implementing the root-gated value-free snapshot with the complete planned call set, existing custody and incomplete states, including never-launched calls. Call-keyed closures may have a null last receipt. Saved Phase-1 evidence will be independent of later Phase-2 files.

T is the latest eligible terminal time only if every call is terminal before the ceiling; otherwise T is the Phase-1 ceiling. Snapshot creation time remains separate; early incomplete snapshots refuse. Tests and mutants will cover both T branches and the saved-evidence boundary.

TESTED: dispatch bytes and adopted requirements read. UNTESTED: snapshot implementation, currently in progress. Continuing c2v007 then G26; no launch, target access or network. Minute polling continues.
