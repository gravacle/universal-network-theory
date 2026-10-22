# 0859 / 0330 post-C1 metadata pre-stage

`date -u`: **Thu Oct 22 03:46:21 UTC 2026**.

**TESTED: author finalizer controls 72/72; separate bound-C1 AST controls 23/23. FORMAL: zero existing integration executable successors are needed for the new C1. UNTESTED: real binding, full F1 replay, custody, native preflight, source review, root adoption and production execution.**

The current A296 v003 lookup, preflight and registry verifier select C1 through the validated ROOT_BOUND binding. The frozen C1 constant is legacy/baseline lineage. This build changes no reviewed source, C1, root binding, proof, acceptance deps or policy. Draft finalizers v001-v003 are retained and superseded by v004. Parent review caught an incorrect F1 output root in the earlier drafts; v004 requires the caller's explicit `replay_out_dir` under the actual final-F1 lookup directory. The tests project the exact final-F1 publish predicate and kill that former wrong-root case.

## Required explicit inputs

Root must first freeze its real successor C1 and write its own validated ROOT_BOUND binding. This tool consumes the binding's byte pin; it cannot manufacture root authority. The exact input-plan schema is `A296_POST_C1_INPUTS_CX2V001` with only these fields:

- `lookup_request_predecessor`: byte pin of the selected existing request.
- `records`: byte pin of genuinely assembled records already carrying the new binding.
- `verification`: byte pin of the genuine current-assembler verification report carrying those records, the new binding and C1, and a passing policy gate.
- `admission_predecessor`: byte pin of the selected candidate containing the predecessor request, known A296 direct_context and source-map slots.
- `replay_out_dir`: explicit, new absolute child path under the final F1 source directory `integration/lookup`; its parent must already exist.

The unbound template contains null values and intentionally refuses. No actual root request, records/verification successor, admission candidate or output selection was supplied in 0859/0330/checklist3d. These inputs must be named and pinned before real finalization. Unknown/missing or ambiguous source slots refuse. This is an explicit readiness dependency, not an invented choice of production inputs.

The admission source map must have exactly one known v001/v002/v003 selection for each A296 lookup, preflight and registry-verifier role. The helper may be absent or have exactly one known version. Only those role entries are replaced or added; unrelated entries remain identical. This does not prove a complete runtime source closure. Root and the distinct source reviewer must check that full closure and the native config. In particular, direct preflight requires its config's certificate-policy pin equal the bound C1 policy; the separate campaign policy cannot silently replace it.

## One-command root finalization (prepared, not executed here)

Set all five parameter variables to the explicitly supplied real values: ROOT_BINDING_PATH, ROOT_BINDING_SHA256, ROOT_INPUTS_PATH, ROOT_INPUTS_SHA256, and NEW_PRESTAGE_OUT. NEW_PRESTAGE_OUT must be a new child under this build directory. The replay output directory is separately required in the pinned input plan. Claude2 uses its registered normal root session; the command attempts nice 10 and single-thread settings, and the F1 child inherits them. It changes no QoS itself. The existing 0514 nice-unavailable waiver applies where required.

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 nice -n 10 /Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/post_c1_prestage_cx2v001/build/finalize_post_c1_cx2v004.py finalize-root-only --actor Claude2 --ack-root-only-custody-replay --binding "$ROOT_BINDING_PATH" --binding-sha256 "$ROOT_BINDING_SHA256" --inputs "$ROOT_INPUTS_PATH" --inputs-sha256 "$ROOT_INPUTS_SHA256" --out-dir "$NEW_PRESTAGE_OUT"
```

`--actor Claude2` and the explicit acknowledgment prevent accidental CLI selection; they are declarations, not identity authentication or new authority. Codex2 must not invoke this mode. It executes only pinned F1 static replay, which is root-only because it reads custody. It never invokes a scientific launcher, monitor, Step4 binder or native context directly. Nonzero replay exit refuses; there is no automatic retry or cleanup. Earlier exclusive outputs remain as evidence if a later phase fails.

For metadata preparation alone, use subcommand `prepare` with the same five input/output arguments and omit the two root-only declarations. This prepares a request, producer-list bytes, candidate admission with a null manifest and null source_review, static F1 command entry, and PREPARED.json. It neither runs F1 nor writes a verification claim. A previously prepared package can later be consumed by `execute-root-only --actor Claude2 --ack-root-only-custody-replay --prepared PATH --prepared-sha256 SHA` after the same root authorization.

## Exact finalization boundary

Before publication, inputs are hash-checked and the pinned binding helper validates the exact old-six-plus-bridge and policy contract. Extra hardening refuses non-successor schema, missing frozen metadata, synthetic_test other than false, or a draft placeholder. Every other C1/root-authentication requirement remains root's responsibility. The finalizer does not infer authority from a hash alone.

The request successor changes only C1/binding, the explicit records/verification references and the producer-list pin. Its genesis and request schema are preserved. Admission changes only direct_context, direct_certificate_lookup, the four reviewed source roles, and clears source_review so a predecessor approval cannot be reused.

Root replay must return success and a real manifest at the declared output path. Its generator must be exact final F1, request must be the generated request byte pin, and verification_replayed must be true; wave/points-list and spec byte pins are checked before an admission candidate is written. The finalizer never invents or sets that replay flag. Merely supplying a prior manifest is not an execution path.

After successful replay, outputs remain **production_admissible=false**. The candidate has `source_review=null`; a separate review request contains requested_sources and the old review pin only as predecessor evidence. A genuine distinct review must bind the exact final source map, and root must publish the admission/source bindings. The emitted F1_REPLAY_COMMAND is explicitly a static-replay command entry, **not a final Step4 launcher entry**. Actual Step4 command binding remains root-owned and was not supplied or tested here.

## Evidence limits

The 72 author checks use physical owned synthetic metadata and output files, a test-only binding seam, and an injected synthetic replay executor. They check exact allowed deltas, unchanged predecessor bytes, wrong/malformed hashes, protected paths before I/O, missing/ambiguous/stale source roles, malformed/unbound inputs, upstream-verification mismatch, genuine-output requirements, replay failures, exclusive outputs, root CLI declarations, and one-command dispatch. The actual pinned F1 output-directory predicate ran independently of the injected executor.

The separate 23 checks execute the exact binding helper and source-derived C1-selection projections from lookup, preflight and registry verifier. They demonstrate non-v001 C1 routing plus refusal of unbound/old-C1/mismatched-policy cases. They are bounded AST tests with RAM stubs, not full native or custody replay. Synthetic replay fixtures are conspicuously marked and do not provide production authority.

No production run-tree/volume, NGC observed target, postseal record, session log, network, actual replay or launch was accessed. All generated files are new and immutable. Prescribed Python 3.12.14 -I -B and six single-thread variables were used; nice reported its known sandbox limitation.

## Byte pins

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/post_c1_prestage_cx2v001/build/finalize_post_c1_cx2v004.py` — SHA256 `5743cfefeb423da01e69024d51b92fca1c4c4a30b603662629b8a4d4569e4baf`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/post_c1_prestage_cx2v001/build/SOURCE_PINS_CX2V001.json` — SHA256 `76ffd4a204bbc5d9c9be10deab8cd9cbbb2c6218323782c4eb36b9df1ab3fab6`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/post_c1_prestage_cx2v001/build/INPUTS_UNBOUND_TEMPLATE_CX2V001.json` — SHA256 `42b19b1797975d341ec16f99c11df2e094358fa37fc7e7cde4141bdc0499990d`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/post_c1_prestage_cx2v001/build/test_finalize_post_c1_cx2v001.py` — SHA256 `8ecfb67cab2b724c2ea72b62d522cec77aac275a6f0a5df85c628c1085a158d4`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/post_c1_prestage_cx2v001/build/FINALIZER_TEST_RESULTS_CX2V001.json` — SHA256 `c85edf80b81fc88d5196c369296de3e461f3350eec66395b723174d6f8aab3cd`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/post_c1_prestage_cx2v001/trace/BOUND_MODE_AST_TESTS_CX2V001.json` — SHA256 `b15b49769eef5e2c36689dde487659ad2a46dc91e3128f752d2985148150e2a3`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/post_c1_prestage_cx2v001/trace/C1_PIN_TRACE_CX2V001.json` — SHA256 `81899629c69c0d240d7eae902031e3defea6dc8c6f8203f0d515c17be1969b89`.
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0859_2026-10-22_codex2_prestage_post_C1_pin_successors.md` — SHA256 `e9e51aa7e6b3d7dce35a63b4ba2509da2216fbd135a73e6e73e77917226890da`.
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE3/0330_2026-10-22_ack-0858-0861-deputy-no-C1-pin-successor-needed-on-A296-bound-path-two-re-signs-C1-tail-first-importer-rule-logged.md` — SHA256 `077663a0194a8ab67cfa68f50fce8ab0be4837f58a19fc7f9da425133475d0a9`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/root_thu_checklist_c3/A296_CHAIN_CHECKLIST_C3V002.md` — SHA256 `81e24b585dcb6d32faff65e32c01ab4b8ae6522ca83b2d2fd3d11b14c2b9e2b9`.
