# cw8 Phase-1 implementation design — CX3V001

date -u: Wed Oct 21 12:09:01 UTC 2026

Dispatch: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0821_2026-10-21_codex3_build_cw8_phase1_path.md` — SHA256 `132bcc7620604096e33f7def9cf54a6568760cc12d7a2604bfe15779398007b9`.

FORMAL / proposed contract, not root adoption. Implementation and tests are UNTESTED at this revision. No scientific launch or real run read is authorized.

The serial call remains the registered baseline. A new full-call cw8 spec must differ in its raw bytes only at the numeric value of `numerics.route_a.column_workers` (1 to 8), and have a separate `SPEC_PIN <call>_FULL_CW8` in V006. There is no cross-worker result reuse. S0 calls retain their original worker role and history.

A root-pinned `CW8_LICENSE_PIN path=<absolute> sha256=<full>` line under an A-numbered V006 section will identify an immutable metadata-only license. It binds the exact S0 serial/twin comparator record, seed spec pins, cx3r008 driver, existing worker/solver pins, and proposed RSS accounting. Missing or invalid authorization, missing/unequal/not-ready comparison, wrong pins or fewer than two compared iterations selects serial and records the reason. A previously committed cw8 role whose evidence subsequently fails verification refuses reconstruction; it never substitutes serial into old custody.

Proposed RSS ruling: full cw8 uses eleven times the registered host RAM as its monitor process-tree RSS cap, the A177 accounting factor, while keeping the full-call output cap, Phase-2-ceiling wall, ordinary member/F name, and no twin watcher. This factor is explicitly gated by the root-pinned license; its presence in a candidate is not a ruling.

A root-supplied, byte-pinned, value-free forecast gives the cohort of new pending member/F calls, cores already in use, and the remaining S0/other critical-path barrier. The selector uses the 0818 two-stage cost model, compares whole-cohort predicted makespans, and chooses cw8 only for a strict predicted improvement. It reports both expectation and upper scenarios. Unknown/stale inputs or unsupported load scenarios select serial. This is a planning estimate, not a measured speedup or an automatic CPU admission governor.

Selection is an explicit metadata-only operation available before the root's launch. It writes exclusive per-call choice records binding the input forecast, comparator license, original and selected raw spec pins, point/theta identity, and scientific PLAN/fdplan/selection scope. A launch without a choice writes an explicit serial fallback for a new call. Existing history, residuals, registration or an earlier choice prevent a fresh role assignment. Choices survive process restart and are checked on every reconstruction. Selecting a batch has no scientific launch side effect. A partial batch write must be resumed with the same input pins; no existing choice is overwritten.

The P112 successor propagates worker metadata through dry checks, registry entries, plans, launch commits, attempt records/receipts, retries, and assembly. A226 single-buffer reads, A245 cause rules and A244 output escalation remain. The consumer successor accepts the new exact launcher pin, independently binds cw8 receipt metadata back to the selected call, and uses its verified worker role for RSS. G26 changes only if needed to pin that builder. Synthetic tests cover fallback, role persistence, raw-spec mismatch, changed non-worker bytes, false twin/watch classification, RSS, final registry/replay and inherited policy. Each tested claim will name the actual evidence.

S0 analysis remains separate: no restart of an existing serial. The saved forecast includes the existing S0 critical barrier so an apparent per-new-call gain hidden behind S0 does not count as a makespan improvement.
