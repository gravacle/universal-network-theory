# Codex3 r007 strict NGC launch records — implementation lane

date -u: `Sun Oct 18 17:48:10 UTC 2026`

**PASS (TESTED within the synthetic scope below).** No scientific run or worker main was launched. No targets or prohibited saved runs were read.

The immutable successor preserves every r006 byte and adds NGC-only strict variants of 48 functions, including saved aliases. Inactive calls delegate to the original functions. The initial NGC spec selector validates the exact byte snapshot it used to select the context.

All direct JSON loads and delegated checkpoint reads in the covered launch helpers pass through strict duplicate detection. Both decoded-key occurrences are reported with full JSON paths and member indices. Iterative reconstruction avoids recursive tree walking; decoder depth failure is a typed Refusal. Route-A and column-mean row elements are checked before indexed use; target-free manifests use their own query_id/Rad_text role. Speeds must be numeric (excluding bool) or null; NaN/Inf retain the existing numerical-invalid classification. Conditional column-mean preparation records require a prediction object and rows list. Failure-status records may omit prediction; legitimate route-A RO1 rows:null and individual N1 speed:null remain legal.

A nested operation shares bounded digest metadata (64 MiB accounting cap, typed refusal on exhaustion), retaining both absolute lexical paths and resolved identities. Every subsequent read or hash must match the first byte digest. This covers both hash-before-parse and parse-before-hash. Checkpoint reads retain the unchanged pinned integrity validator and compare the exact canonical returned-byte SHA to the first strictly parsed snapshot; before/after fencing alone is not relied upon. No shared json or checkpoint module was patched.

Finalization catches strict Refusal, marks the result REFUSED/valid=false and preserves the existing result/finish sealing path. Active text reads use a local io.TextIOWrapper over the tracked raw bytes, preserving default encoding and newline semantics without adding an inactive locale import.

TESTED: 241/241 focused checks; peak macOS RSS 121,389,056 bytes; zero audit denials. Tests use synthetic records, fake changing byte streams, actual shared helper entry points, the unchanged checkpoint validator and the extracted actual finalization block. The 48 clone checks are source-coverage assertions, not scientific-stage executions.

Earlier immutable candidates and harness retries are retained. Review corrections added canonical checkpoint byte custody, removed top-level manifest/result row inference, removed eager locale import, and added typed malformed-speed/conditional-column-mean structure refusals after independent v003 probes exposed downstream TypeError/KeyError paths. Initial harness failures involved missing explicit read allowlisting and a negative checkpoint fixture passing Path where the existing validator expects str; final results below supersede those attempts.

UNTESTED: numerical/scientific execution and large production-record resource use. Parent combines separate independent semantic review and 78-spec dry-plan evidence, and owns final registration. This report does not grant launch authority.

| Evidence | Path | SHA256 from bytes |
|---|---|---|
| dispatch | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0581_2026-10-18_codex3_cx3r007_strict_launch_path.md` | `3e6ea8a721e32546cc88703486edbca5b871bbffdc7cd66f1d3fa7d394371132` |
| parent | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ro1_strict_records_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r006.py` | `c2930e18eb2ba6f691dcaffffd56658143490ab366552cf90b27506a2357be49` |
| candidate | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r007_cx3v004.py` | `e4f5864aee796febf133aa03e2bf3236a9fc566971c5d2f0f5d3e2d6b226ea69` |
| build | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/implementation/BUILD_CX3R007_V004.json` | `4d5685d181f29a7a63081ffe0f1b0d103ce20fb2b9d23be3fb94b78c2b007c2b` |
| tests | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/implementation/focused_v006/RESULTS_CX3V001.json` | `56d9a84a5d553bfaecc1196a6debdc5e77ee5c81883433f50cc415096e036d3b` |
| checkpoint_validator | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py` | `069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114` |
| typed status | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_launch_record_strictness_cx3/implementation/TYPED_STATUS_CX3V001.json` | `6c49cf03b6ca0a59e13f45012c98ab5239a0f98e5165d0049c1858f1ac671c4e` |
