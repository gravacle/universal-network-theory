# 0794 / A240 — minimal KS3/KS4 successor, pending root ruling

FAIL, one blocking item: CX1-KS-SR-01. Do not adopt as satisfying A226 single-read.

Built common s4rc1_common_ks3_cx1v001.py and assembler registry_assembler_ks4_cx1v001.py. Common changes only PINS (+3) and CANONICAL_APPROVED_PRODUCERS_S1 (six); assembler changes only COMMON_PATH and COMMON_SHA. All remaining AST nodes identical, including non-S1 behavior. Added comments identify the predecessor docstrings as historical. Existing published files remain unchanged.

Eight policy cases pass: six, three compatibility, seventh rejection, alias rejection, ok=1 rejection, reversed review rejection, non-S1 baseline and non-S1 rejection of S1 additions. Five in-memory mutations caught. Tests use full imported successor policy-gate/common readers on inert files, with test-only canonical pin tables; they do not execute full registry verify or science.

The required audit-hook single-read test FAILS: c1_policy_gate reads certificate_policy_review in its C1_REQUIRED_PINS loop, then read_json_pinned reads it again. The inherited common hashes both reads, but this still violates the requested one-read contract. Both reads are visible in TEST_RESULT_CX1V001.json. Minimal-function-AST identity and a passing full-gate single-read test cannot both hold without a root ruling.

Recommended next ruling: permit a narrow policy-gate change to retain each validated buffer in a per-invocation map and parse the already-validated review buffer, checking each requested hash before reuse. Audit the complete verify call separately for repeated shared pins; do not claim a one-function fix proves whole-command single-read. This behavior change was not applied.

S1_SOURCE_CLOSURE_DELTA_CX1V001.json gives the exact three path-to-hash additions without editing lib v002c. Actual admission base/fence, row32/real C1, full suites and registry verify remain UNTESTED; root dry launch remains deciding.

Authorship: Codex1 drafted the six-producer list and built this successor. Codex3 provides the S1 policy review; root verifies after reset. No independent-review claim is made for these own-build tests.

Harness note: first mutation probe used an aliased path, which was independently refused by the real path reader even after removing canonical membership. The final probe uses a seventh regular inert producer to isolate membership; no production behavior changed. Both temporary runs were retained; no artifacts overwritten or deleted.
