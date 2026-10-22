# P-112 cx2v004 — immutable review candidate

`date -u`: Wed Oct 21 09:55:29 UTC 2026

TESTED: 221 functional/static checks and 21 killed mutations. UNTESTED: real launches, production inputs, root adoption, scientific classification and the subsequent incomplete-freeze integration.

Source: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2v004/phase1_ngc_launch_cx2v004.py` — SHA256 `8cec1b56fc682f638fee57329eefc9b3cddfa47959d175e7095fc0c5fe0342c9`
Evidence and all test/source pins: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2v004/REVIEW_EVIDENCE_CX2V004_V001.json` — SHA256 `e72288a03c3de8e6744321caaa0499d8064ca2fe9c08da1f8165678d2af29089`
Parent: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2v003/phase1_ngc_launch_cx2v003.py` — SHA256 `af0210715f658c43f73f37a5e6e733f7a48dc374caa1b8af5a0defe3987854d7`

## Changed behavior

CAP and nonphysics ends do not terminate the call by attempt count. Repeated identical REFUSED/BLOCKED is HELD_FOR_FIX. Two consecutive identical solo FAILED statuses without authenticated cause evidence are HELD_FOR_CAUSE. Unknown causes remain uncounted. Matching root-pinned model causes require the same spec, driver, status, stage, code, exception class/site set and two distinct monitor receipts, with solo evidence; only ROUTE_A_NO_FIXED_POINT and clean ITERATION_BUDGET_EXHAUSTED are admitted. The unchanged spec pin carries the unchanged scientific iteration budget. No new numeric iteration budget is invented.

Retries are solo, with RSS at RAM (twin: 11×RAM). OUTPUT_CAP doubles the previous output cap. There is no doubled-wall condition and no attempt-count cap. Raw status and the exact 54-entry map remain unchanged; policy independently excludes nonphysics and explicit root stops.

A twin STOPPED_* alone is a cap/interruption. A planned twin stop needs the watch record's schema, reason, complete launch pin, outdir, child PGID, successful kill result and date. An explicit bound root stop preempts it.

Phase-1 ceiling is 2026-11-06T05:59:00Z; Phase-2 ceiling is 2026-12-01T05:59:00Z. Config must state both exactly. Phase 1 is a reporting/freeze boundary, with no process stop. `status` reports UNEVALUATED_SCHEDULE_CEILING for unfinished calls, including active calls or missing receipts, while preserving mount failures. New Phase-1 admissions stop at that boundary. A finish after it cannot retroactively count for Phase 1. Monitor wall uses remaining Phase 2.

After dry checks and sampler lead-in, launch writes an exclusive successor launch plan and commit. Sampler, resume and residual recovery bind to that final argv. Historical residual wall values come from the saved plan, never today's clock. Final filesystem/scheduler delay and monitor poll delay are not eliminated by this change.

## Config and root-controlled interfaces

Use schema `P112_CONFIG_CX2V004`. All parent config fields remain; add:

- `phase1_ceiling_utc`: `2026-11-06T05:59:00Z`.
- `phase2_ceiling_utc`: `2026-12-01T05:59:00Z`.
- `cause_records`: a list of exact path/SHA256 pins to reviewed, root-trusted, value-free cause records; initially `[]` is valid.
- `root_stop_records`: a list of exact path/SHA256 pins; initially `[]` is valid.

Cause records use the producer's exact eight top-level fields. A252 SITE_SET/CLASS_SET strings are compared exactly and are never followed as paths. P112 verifies association to the independently rederived monitor/result/spec/driver pins and requires the finish SHA in a positive record. It does not read result, finish or stage files; it does not cryptographically establish who produced the cause file. Producer review and root custody are prerequisites. Contract inspected: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/CAUSE_PROTOCOL_CXV002.txt` — SHA256 `dcd08ad11f23b12a0bbb38d6baceff54e878b02f7864c1940d7fdea6f701098e`. Producer candidate inspected, not executed or adopted: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/cause_record_cxv002.py` — SHA256 `4271da4422c40faf1afbd115af836091e765f64e902809432b55af69036606f3`. Vocabulary metadata byte pin: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002/CAUSE_VOCABULARY_CXV002.json` — SHA256 `839c75774c28c6c8213180df7e204ba5b9d0fbc63531591d22d9912149f8df37`.

The proposed value-free root-stop record shape is exact keys `schema`, `date_u`, `call`, `launch_json`, `registration`: schema `ROOT_NONPHYSICS_STOP_C2V001`; `date_u` is ISO UTC within the attempt; `call` is the closed receipt's four-field call object; `launch_json` is the complete launch pin; `registration` is a pinned root declaration. This is a review interface, not a claim of a preexisting root registration. Repeated REFUSED/BLOCKED has no automatic release override in public launch; root must resolve the hold through a separately reviewed procedure.

Proposed adoption line (not written to V006):

```text
TOOL_PIN P112_LAUNCHER_CX2V004 8cec1b56fc682f638fee57329eefc9b3cddfa47959d175e7095fc0c5fe0342c9 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/phase1_ngc_launch_kit_cx2v004/phase1_ngc_launch_cx2v004.py
```

Runtime custody filenames and receipt schema names stay compatible with the parent. Existing source and runtime records are never rewritten. A changed config is a new immutable file. A partially started launch must resume against its original pinned config and final committed plan; adding later cause inputs does not rewrite earlier receipts.

## Boundary and validation scope

The public status boundary is implemented. Registry assembly still requires its registered entries and closed receipts; it does not fabricate a receipt for a running or never-launched call. The c2v007/G26 work that follows must supply the Phase-1 incomplete-call freeze integration. This is explicitly not yet an end-to-end freeze claim.

The 221 checks comprise 101 status/gate/core checks, 75 saved-state integration checks, 16 committed-plan checks and 29 process-row/static contract checks. Three status mutations, fourteen policy mutations and four committed-plan mutations were detected. Mutation sources were evaluated in memory; no reviewed file was edited. The evidence manifest pins every test and result, including the initial corrected harness-only failure. The older full suite's subprocess fixtures were not run. No forward, route-A, route-B, real sampler or monitor run was launched; no NGC target or run content was opened. Tests reject rename/delete/existing-file writes, scientific child processes and forbidden reads.
