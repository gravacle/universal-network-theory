# A296 EPS successor — downstream admission impact

`date -u`: Wed Oct 21 17:30:42 UTC 2026

**FORMAL: the truthful A296 successor is intentionally rejected by the existing admission chain.** A rule producer and re-evaluator alone cannot make row 302 launch-admissible. At least an explicit new EPS validation/proof path, a compatible prelaunch/acceptance guard path, and root-approved provenance/policy bindings are required. **The SRB-ROT adapter can remain byte-identical**, as A296 directs. This report proposes the necessary scope; it implements nothing and grants no approval.

## Contract under review

Keep the original failed shell's `certified=False`, `refinements=2`, level values, and the record's `registered_discrete_verdict=EPS_UNCERTIFIED`. Add the A296 acceptance fields, a measured-ε disclosure and the 10× substituted `eps`. The overall verdict is exactly `NUMERICAL_RULE_PASSED_NEGLIGIBLE_SHELLS_NOTED_REVIEW_REQUIRED`, with `successor_rule_verdict=ACCEPTED_NEGLIGIBLE` and an explicit accepted-shell list. The actual re-evaluator is the new producer; preserve predecessor bytes and original producer as provenance rather than impersonating the old producer.

R1(d) requires **at most one original discrete-failed shell per record**: for any accepted shell, every other shell must pass the original rule. Zero failures keep the old path unchanged; two failures cannot be accepted merely because each separately meets the magnitude/floor/audit bounds.

## Concrete existing blockers

| Boundary | Source location | Why the A296 record fails |
|---|---|---|
| CP1 EPS stage | CP1_RUNNER lines 296–309 | Requires original `CERTIFIED`, exact old top-level verdict, old canonical producer, and exactly 14 original audit entries. An additional audit embedded in that list also breaks the count. |
| EPS proof adapter | EPS_ADAPTER 109–115, 176–188 | Rejects refinements=2, `certified=False`, and refined/base>1.1; requires original discrete CERTIFIED and pinned old producer. Even an approved new review does not bypass these checks. |
| Proof shell guard | B1_GUARD 133–140; BASE_GUARD same lines | Rejects any proof row with `refinement_failures=2`. Relabelling the proof history as 0/1 would conceal the old failure; use an explicit new accepted branch instead. |
| Distinct review | CP1_RUNNER 898–925; COMMON 480–496 | Existing failed STAGE_EPS is not OK. Review must bind the exact new numeric bytes and adapter SHA, be root hash-approved, outside the runner output root, and signed by an approved lane distinct from producer/operator. Old reviews cannot cover changed bytes. |
| Approved proof producers | C1 `/tail_readiness/approved_certificate_producers`; REGISTRY_ASSEMBLER 259–265 | Frozen C1 lists the old EPS adapter `4de70486…`. A successor proof producer is not on that list. |
| Source provenance | LIST_ASSEMBLER 79–100; DIRECT_LOOKUP 306–307 and 363–365 | The digest of `{dependencies, producer}` must equal genesis. A truthful new producer changes it. Mixed old/new records also fail the single-digest-per-list requirement. |
| Direct admission | DIRECT_LOOKUP 284–310; DIRECT_PREFLIGHT 34–40, 144–148 | Pins exact frozen C1/genesis, six approved producers, existing assembler/verifier, and exact configuration policy. Appending an adapter to an otherwise unchanged supplied allowlist is rejected. |

The old failure is correct fail-closed behavior, not a reason to remove the checks. The review and producer bindings must be extended under a specifically reviewed A296 path.

## Smallest necessary successor scope

1. **A296-aware EPS validation and proof adapter.** Keep every old numeric/coverage/custody/search check for normal records. For the new exact R3 verdict, independently replay the rule against pinned predecessor and audit evidence, require exactly one original failure, exact R1 constants and TESTED registered full coverage, exact 10× substitution, all other values/history unchanged, and unchanged governing max/max-shell. Keep raw discrete history in the proof and label acceptance separately. A boolean `accepted_negligible` alone is not proof. The producer/re-evaluator pin and new adapter pin must both be independently approved.
2. **New re-evaluation admission/stage entry or CP1 runner successor.** The old runner cannot consume a failed STAGE_EPS or the new verdict. A separate immutable import/adapt path can validate saved context and new numeric/review pins without recomputing or overwriting the failed attempt. If the normal CP1 route is retained, its common/runner/list-runner pins need successors. Put the extra dense-audit evidence in a named successor field, or explicitly extend the audited-set contract; do not silently defeat the original exact-14 check.
3. **A296-aware certificate guard and callers.** The EPS proof may remain TESTED/PASS only after the new independent review, while carrying original `refinement_failures=2` and verified A296 acceptance. New guard logic must allow that one precise branch and reject unknown flags, multiple original failures, missing evidence and out-of-bound substitutions. The current b1 guard rejects it during both prelaunch and acceptance; its wrapper/preflight/policy bindings must name the reviewed successor. No mathematical SRB transformation is needed.
4. **Root-approved policy/provenance bridge.** The immutable frozen C1/genesis records and the 31 original certificate bytes should stay intact. The new list/direct admission needs an explicit reviewed, root-bound compatibility policy for original producer lineage plus A296 transformation lineage, and a new approved EPS proof producer/guard binding. Whether this is a separate compatible policy extension or an explicit C1 successor is a root decision; the present frozen chain supports neither implicitly. Every affected assembler/direct-lookup/native-preflight source pin, policy review `checked_gate`, source review, generated verification record, manifest and bound input must be renewed under new names. Do not preserve the old `producer` value as a shortcut around digest equality.
5. **Fresh approved-signer review and downstream artifacts.** The new review binds the exact substituted numeric record, the new adapter and scope, and explicitly approves the numerical convention and accepted-shell evidence. Then create a new EPS proof, bundle, list record/verification and final spec pins. Existing GQ and rho records can remain reusable only if their point/custody bindings still agree; they require their own existing registration/proof checks. The admission work does not imply that the missing rho or slot proof has been completed.

This is an integration dependency report, not a request to change all listed modules blindly. A reviewed narrow alternate admission path can consolidate successors; it must cover each currently enforced predicate and pin boundary above. Parent/root should approve a concrete integration design before implementation to avoid collisions with other active lanes.

## Why SRB-ROT remains unchanged

SRB_ADAPTER `format_eps` lines 265–292 requires the existing EPS schema/gate, exact point/custody, registered full search, complete [4,182] unit-shell coverage, finite nonnegative values and `eps >= eps_envelope`. It copies the per-shell `eps`; it never reads the numeric record's discrete verdict, refinements or accepted-negligible flag. The substituted 10× value fits that same format. Its outer adapter lines 418–427 requires a TESTED/PASS approved EPS slot proof, which the new admission path must supply legitimately. Thus the existing SRB mathematical and formatting code can consume the conservative number once the proof/policy chain admits it; changing this adapter would violate the explicit scope instruction and is unnecessary.

## Verification limits

Eight source-text/custody comparisons passed (TESTED). All integration consequences above are FORMAL from source. No project module was imported or executed, no fixture or scientific command ran, and no admission was attempted. No actual run-tree, NGC data, postseal records, session logs or network were accessed. Only selected control heading A296 and C1 policy metadata were inspected. Numerical re-evaluation and end-to-end admission remain UNTESTED. No reviewed file was changed; no implementation was created.

## Sources — SHA256 from bytes

- **EPS_ADAPTER**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/point_response_admission_adapter_cx2v003.py`
  SHA256 `4de70486120de215838f5ca2b0c9464d52a0edc3d5280dd042d5521d60f1c372`
- **CP1_RUNNER**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/build_c3v004/cp1_runner_c3v004.py`
  SHA256 `3f5e5c188d4a6967afdb3bfab805d1cc8650e9c26793895096be55ca8f4f1a48`
- **COMMON**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/build_c3v005_c2/s4rc1_common_c3v005.py`
  SHA256 `2308a47ce3c758b6befa0aa954fa7e2b6ad7f4cb41ed73d4b8cd1d257021e7c5`
- **B1_GUARD**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py`
  SHA256 `9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677`
- **BASE_GUARD**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/certificate_guard_cx2v003.py`
  SHA256 `5f1e49e689a859c003b137c45c07f887423443ef2c726182616b41bf290c9c2f`
- **SRB_ADAPTER**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/proof_side_c3v003/srb_rot_adapter_c3v003.py`
  SHA256 `08e9ac0a12cf1829f79f6df8a82c9ec6a7d174fc4bb25be76d3c049525dfae6a`
- **REGISTRY_ASSEMBLER**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/build_c3v005_c2/registry_assembler_c3v005.py`
  SHA256 `7df1c4813865b9e1245f5a91d827591a6d87963b6413ab53c50d2a542d211310`
- **LIST_ASSEMBLER**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx2/cp1_points_assembler_cx2v002.py`
  SHA256 `1b701591714c11856d525631f946d19a64f76f28041da21c6e9f1a62863b0e88`
- **LIST_COMMON**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx2/cp1_points_common_cx2v002.py`
  SHA256 `658593278f428a1937daa0a40837cd3d8e10e6ad7acf0e479508bdbb04362934`
- **DIRECT_LOOKUP**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx3/direct_cert_lookup_cx3v001.py`
  SHA256 `1cb5039ef380f7472191f40d1293f45b98cbc4e301efb06d9ea9ccc5b59de7e5`
- **DIRECT_PREFLIGHT**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/direct_cert_lookup_cx3/direct_preflight_cert_cx3v001.py`
  SHA256 `586391ecd15453608956347ecafd4f61f6dea77a33ec71a61435a7a714e39a8f`
- **C1**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/c1_h1_c2/C1_H1_C2V001.json`
  SHA256 `4015932226dcfbf9783b96de1daa512ef5c7a397ac4ca093d701ead362ed92c1`
- **ROOT_A296**: `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md`
  SHA256 `1655124f7605a791c39ab0450a3096dabd9cde0447e9e5259d421f6a6a3a41a9`
- **DISPATCH_0855**: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0855_2026-10-21_codex2_claude3_A296_final_text_build_now_and_F5_gap_proposal.md`
  SHA256 `1541dad07b9d14d994fc7f595c8276f2f0555f38b67f1c8fd1142d883fa36b5a`
- **Selected-source evidence and checks**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/integration/ADMISSION_IMPACT_EVIDENCE_CXV001.json`
  SHA256 `5b9031535c625cbe8a35d43955694f92e94d1220997771a52f1c51aaec7a91f8`
