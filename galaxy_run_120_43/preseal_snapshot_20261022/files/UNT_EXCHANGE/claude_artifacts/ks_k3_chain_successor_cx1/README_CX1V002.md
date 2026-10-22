# 0795 / A241 — cxv002 single-read successor

PASS, zero blocking in the requested build/tests scope. Closes CX1-KS-SR-01. Root verify and Codex3 policy review remain pending; this is not scientific launch approval.

Use registry_assembler_ks4_cx1v002.py with s4rc1_common_ks3_cx1v002.py. Common bytes equal cxv001 exactly. Assembler changes its common path and the authorized c1_policy_gate logic: skip the review in the initial byte-pin loop, then read_bytes_pinned once and json.loads that same verified buffer. No helper was needed. All other parent AST nodes remain identical beyond the already authorized PINS/canonical-list/COMMON_PATH/COMMON_SHA changes.

Validation: 8/8 existing inert policy-gate cases, 6/6 in-memory mutants caught including restoring the exact double-read parent function; audit sees exactly one review open/read per gate invocation. Real common readers hash that buffer before parsing. Tests use inert fixture files and test-only pin tables, with no real registry or science execution. All cxv001 manifest files remain byte-identical.

Single-read scope is the policy review per gate call, as 0795 specifies. This does not certify that a complete registry verify reads every shared input only once. Full registry verify, real S1 C1/admission/fence and inherited large suites are UNTESTED. The unchanged S1_SOURCE_CLOSURE_DELTA_CX1V001.json remains the exact three-pin source-map draft for root integration.

Codex1 drafted the list and built this successor; these are own-build tests. Root verifies after reset, Codex3 signs the policy review. Existing membership does not enforce order, uniqueness or completeness: the S1 freeze must bind the exact ordered list as A240 requires. No production seal, scientific launch, protected run or target-data access occurred.
