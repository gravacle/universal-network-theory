# Classifier B c2v005 — Codex2 distinct-lane review

date -u: Tue Oct 20 15:15:22 UTC 2026

**PASS for classification; zero blocking findings.** One nonblocking contract ambiguity (CA1) requires a reporting ruling. B_DEFECT count 0; CONTRACT_AMBIGUITY count 1; A_DEFECT count 0. This record makes no adoption or launch decision.

Object: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/classifier_b_c2/build_c2v005/classifier_b_c2v005.py` — sha256 `cec5bfe9582899437aa715d78e1dfdb36089ebead04f840d4d68893b3d1251c7`. Dispatch: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0767_2026-10-20_codex2_A205_queue_P106_classifierB_launcher_v004_G26.md` — sha256 `47531f2671f30ba3966b0ddc896686b354f3d67d2e3304ad95c1e12978205025`.

## Evidence

- TESTED: B suite 327/327 twice. The suite retains its declared 311 seamed and 16 as-shipped cases. The wrapper only redirects the compare input to byte-identical permitted suite bytes; both parent read logs have zero refused opens.
- TESTED: shared unmodified CLI runs agree on 364/368 cases; four differences are forged-only A115 NOTEs. Independent hand-built classifier-form cases agree on 14/14; zero honest-form disagreements. All per-case comparisons and all A outputs remain in A_SIDE.
- TESTED: 158/158 independent B clause checks across 14 own cases: thresholds, null-ratio unsigned misses, per-row registration, global/mixed patterns, L1 availability/noise/inclusive overlap, eight-row STAGE0 comparison, invalid twin, no successor and AT1 failure consequences.
- TESTED static: 15/15 Codex1 kernels match their V089 pins and current upstream bytes. The supplied 894-entry B read log records zero forbidden A-code/suite-code/output reads. This is an audit of the supplied record, not historical process telemetry.

## Focused code review

FORMAL: reviewed B against the contract and pinned producer bytes, with attention to score alternatives[]/NON_PRIMARY, full-length frozen row_registration, scoped STAGE0 score arrays, exact successor block/member keys, receipt-time equality, L1 source/full-hash binding and column-only failures, and AT1 record forms/Phase-2 precedence. Source producer code was read, never imported or executed. B reads the frozen registered reason and gate status per member; null ratios remain unsigned misses; a twin gets neither NEAR nor TSR. STAGE0 comparison uses only jointly valid signed rows and does not alter the headline. The below reporting ambiguity is the sole unresolved item identified.

## CA1 — nonblocking reporting contract ambiguity

C-6.1 requires the scored member distribution when the twin is invalid. C-6.3 final sentence asks for the STAGE0 member within-error distribution. The adopted output schema instead defines stage0_within_error_distribution as n=8 and the reference twin HIT count, and omits it on TWIN_INVALID.

score.alternatives[] carries member_within_error_counts from the distribution over all scored members (v003g L4289-L4294).

TESTED: Two member counts [8,3] give producer-form n=2,min=3,median=5.5,max=8; B reports only n=8,within_error=8. For an invalid reference twin with member counts [0,3], B reports TWIN_INVALID and no member distribution. Both are classified without stops; R-DRIFT remains OPEN in the invalid-twin case.

B locations: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/classifier_b_c2/build_c2v005/classifier_b_c2v005.py:2222` — sha256 `cec5bfe9582899437aa715d78e1dfdb36089ebead04f840d4d68893b3d1251c7`; invalid-twin early return at line 2208. Contract basis: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/classifier_a_c4/build_c4v001/basis/PREREG_MISS_READING_R3A.md:521` — sha256 `1e17eb459c43d40205e7ed913da16de8b67e2762fa5e1a440699de796d9216a5` and line 581; fixed form: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/classifier_a_c4/schema_c4v003/OUTPUT_SCHEMA_C4V003.json:6832` — sha256 `36d8a1dc079e58a0667517504cc9acf3d445766a4fffda52e38a5af25063f541`. The seal-candidate text also retains the member-distribution wording: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/miss_reading_prereg_c4/r3a_sc2/PREREG_MISS_READING_R3A.md:579` — sha256 `9a2f177f52345a875dff5e7a13d931fbfbbaf2a2dda36028b6c3977cc66c9b55`.

Clarify whether C-6 requires echoing the all-member distribution, with a synchronized text/schema correction or report field if so. The existing twin-row count may remain separately named. Nonblocking reporting ambiguity: no wrong classification, reason, row reading, physics/gate/blinding effect demonstrated.

B-only reproductions and expected input counts: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2/OWN_BUNDLE_INDEX_CX2V002.json` — sha256 `a8f41deff7eef55c1eee4b38e0644316d26fdd5b8ce611673124c8d22fcb86a0`; `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2/OWN_CONTRACT_CHECKS_CX2V001.json` — sha256 `34e3c6a18530c096a27d6b4dbd40745a0f87c6b39264d66047e25cde2dba8ac5`. All input and output hashes are in the evidence manifest below.

## Barrier and limits

A_DEFECT count: **0**. Claude4-only note: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2/A_SIDE/A_DEFECTS_FOR_CLAUDE4_CX2V001.md` — sha256 `430d4b9524d17d534cbd57bb3e9f5af1611c13e281b446b6b5110c6ddffdb66e`. Root and any B successor builder must not open A_SIDE.

Disclosures: Codex2 is a different lane but the same model family as Codex1, who wrote the kernels. v003g L188 depends on the FORBIDDEN name set from prior Codex2 P46 work. Neither dependency is claimed independent lineage. The own cases reuse permitted root-record scaffolding; their member, score, band and AT1 records were independently authored from source forms. Full production freeze custody is UNTESTED. No producer execution or real scientific data access occurred. Exact isolated Python with six thread variables set to one was used; nice was attempted but the sandbox denied setpriority.

The root-facing artifacts contain only comparison counts; forged-only details and every per-bundle comparison are confined to A_SIDE. No reviewed file was edited. Builder drafts v001/v002 remain unexecuted and immutable; v003 generated the final case set. Suite parent guards logged zero refusals; child CLI opens were not independently traced.

## Hash-linked records

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2/RESULT_CX2V001.json` — sha256 `939e53445e000eb7350cd3800b4183b345044896bbab87d50c7837ea854b2930`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2/B_EVIDENCE_MANIFEST_CX2V001.json` — sha256 `9f11273a3b198f5fb4744a8be037616967e008b23c4bed92277f6996b5f62978`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2/READ_LOG_AND_KERNEL_AUDIT_CX2V001.json` — sha256 `4527508a6f21da680673edb90265638021dcf08faa3d098051b600b04edf137c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2/AUTHORIZED_RULINGS_CX2V001.json` — sha256 `1bdd220bb054e64b12fd8e2e8e161f6f45316d26b16fb0ed58a4a2422a8362e0`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2/OWN_BUNDLE_INDEX_CX2V001.json` — sha256 `87b28d46a70e7d8ad9ed7a901cbbb706327822a1cf66683f7fc76f7b1df234eb`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2/OWN_BUNDLE_INDEX_CX2V002.json` — sha256 `a8f41deff7eef55c1eee4b38e0644316d26fdd5b8ce611673124c8d22fcb86a0`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2/OWN_CONTRACT_CHECKS_CX2V001.json` — sha256 `34e3c6a18530c096a27d6b4dbd40745a0f87c6b39264d66047e25cde2dba8ac5`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2/B_suite_run_1_cx2v001/SUITE_RESULTS_CX2V001.json` — sha256 `ed2e29d739125c1ff5e5d6f07f28f0b50b16e00aa0705d2ab894ccb53dc522c1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2/B_suite_run_1_cx2v001/READ_LOG_CX2V001.json` — sha256 `a49b33538dd7e6bf7777034c81d54fc838c219418eabb013580dc02b579bc3f4`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2/B_suite_run_2_cx2v001/SUITE_RESULTS_CX2V001.json` — sha256 `ed2e29d739125c1ff5e5d6f07f28f0b50b16e00aa0705d2ab894ccb53dc522c1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_classifier_b_cx2/B_suite_run_2_cx2v001/READ_LOG_CX2V001.json` — sha256 `a49b33538dd7e6bf7777034c81d54fc838c219418eabb013580dc02b579bc3f4`
