# EPS policy review C4V001 — the one policy-level EPS review for the 31 S4-R-C1 points (A134 Q8). Signed by Claude4

**Status:** SIGNED (line at the end). Root pins this text by its sha256 before the first CP-1 EPS record (A134 Q8 "Frozen"). The order was: the script was finalized; its sha256 was entered in §1; this text was signed; root pins it. Any edit to the script needs a new policy text.

**Authority.**
- Root ruling A134 (V006), adopting Q8 of `S4RC1_ROOT_RULINGS_DRAFT_WF_C88BB583.md` (`56774ba7a1ad54be89cb1cbb6bd256333de4134ed9ef8a8e949898f7ed8c2c82`).
- Q8: "one policy-level review signed by Claude4, instantiated per point by Claude4's own script with no discretionary input. The script issues APPROVED only if `validate_numeric_candidates` passes and the numeric_ref, point, custody and adapter bindings match (adapter L182-190). Otherwise it issues nothing, and the blocker is preserved as UNAVAILABLE. Claude4 checks the anchor instance by hand first, including the cross-check against EPS_CERT_V006."
- Dispatches 0688 (`bcb6df8e9cbd7d01c7c10e4673fb6ca60ecf6c4a439be4db6140ed521689b30d`) and 0691 (`934bdbd6d0f9e66985a5f57f38a453bb33e78c8724d0d215dce1db8685f26d64`).

## 1. What is reviewed, and the code that does it

| object | pin |
|---|---|
| **the instantiation script**, `claude_artifacts/eps_policy_review_c4/build_c4v001/tools/eps_review_instance_c4v001.py` | `e352458665223560b7d8895d57c40f8faed2ec240d393955c53efe5f2345bc15` |
| EPS adapter v003, `calib_tail_readiness_cx2/certificates_per_point/point_response_admission_adapter_cx2v003.py` | `4de70486120de215838f5ca2b0c9464d52a0edc3d5280dd042d5521d60f1c372` |
| its base r5, `point_response_admission_base_r5_cx2v001.py` | `381b3eaa6ba8a56c2ca4c89f88c6e5e333d7152b52c5386892b19d0a8f50d4e6` |
| the numerical producer (RESPONSE_SHA), `point_response_producer_cx2v002.py` | `a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231` |
| the custody deriver that defines `derive_details` for P2 and P5 (custody_cx2v002) | `6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377` (`calib_tail_readiness_cx2/certificates_per_point/custody_cx2v002.py`; s4rc1_common_c3v002 PINS) |
| the forward driver that `derive_details` reads (r5) | `b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6` (s4rc1_common_c3v002 `DRIVER_SHA`) |
| CP-1 runner, `s4rc1_c3/build_c3v002/cp1_runner_c3v002.py` | `884bb89e8f08040f5dbae6ad462856f0fd0a0e5d293090721c5fc3e35ebaad8b` |
| its common module `s4rc1_common_c3v002.py` (the 31-point table, PINS) | `fa48b1a16d26ff14445f6823bd7c15554e50bd0f75b882e0564c4e40980055ce` |
| Claude3's EPS review template and checklist section E | `98502e6b175fcbdc64dae418bbce351fd3bc4e56934791cabd10813ed24300ce`, `d4ed05028d784999c7fde42a3a34cc2fe7571248899d968082c2915a31a3f1ee` |
| EPS_CERT_V006 (the anchor cross-check) | `598c8fa34dc85113aa99dd3722f6b37f6625149995d7365c8cbd1b796f830192` |

Build and verification of the script (synthetic only): `build_c4v001/out/TEST_RESULTS_C4V001.json` (`c459a1897d2f27c067278d7185118742de19ded64972c7a296f979d652649f4a`), 110/110, and the adversarial verifier's `verify_c4v001/VERIFY_C4V001.md` (`c3ec58111a4ad6bad5b487b9b6bc3ec8b27b3697ae6e65dafdba05b264f1d9d7`), with no blocking finding. End to end, adapter v003 `adapt_eps` returned READY_FOR_MANIFEST and the runner's `adapt_point` wrote EPS_PROOF for every instance written. The real custody `derive_details` is UNTESTED here (§5).

## 2. The policy: an instance is APPROVED only if all of these hold

**The inputs.** The script takes exactly six inputs and no other option: `--point-dir` (one point attempt's CP-1 directory), `--out-root` (the CP-1 runner output root it lies in), `--point-key`, `--policy`, `--policy-sha256` and `--output-dir`. None of them can turn a refusal into an approval.

**Identification checks (fail closed).** Before P1 to P7, the script requires:
- the six inputs (ARGS);
- the key is one of the 31 rows of the pinned common module (POINT_KEY_NOT_IN_TABLE);
- the policy path, its sha and that it names this script's sha (POLICY_PATH_INVALID, POLICY_SHA_MISMATCH, POLICY_DOES_NOT_NAME_THIS_SCRIPT);
- the out-root and output directory (OUT_ROOT_INVALID, OUTPUT_DIR_INVALID, OUTPUT_DIR_INSIDE_RUNNER_OUT_ROOT, OUTPUT_DIR_OUTSIDE_EXCHANGE_ROOT);
- the point directory's name (POINT_DIR_NOT_THIS_POINT);
- the four runner records POINT_START, STAGE_CONTEXT, STAGE_EPS and POINT_DONE (RECORD_MISSING_OR_UNREADABLE, RECORD_NOT_THIS_POINT, RECORDS_INCONSISTENT);
- the spec pin agreeing across the table, POINT_START and POINT_DONE, with the runner's load_spec checks (SPEC_PIN_DISAGREES, SPEC_INVALID);
- the pinned code (PINNED_CODE_MISMATCH);
- the adapter's own `adapt_eps` with no review stopping exactly at L182 (P2_P3_ADAPTER_OWN_CODE);
- the inputs unchanged during the run (INPUT_CHANGED_DURING_RUN).

A worker that dies after STAGE_EPS ok but before POINT_DONE leaves a record that the adapter would admit; the script refuses it. That is fail-closed by design.

**P1 to P7.** Each mirrors the adapter or runner line named, and the script evaluates each with the pinned adapter's own code where the adapter has it.
- **P1. Exact bytes.** The numerical record is read through its exact `{path, sha256}` pin from the point's `STAGE_EPS` record, and its bytes re-hash (runner L694-697).
- **P2. Record form** (adapter L172-176): schema is the producer's `EPS_SCHEMA` and gate `EPS`; `identity` and `custody` equal `derive_details(spec)` for the point's registered spec; status `TESTED`; settings `registered`; `full_registered_search_executed` true; `coverage_complete` true; `registered_discrete_verdict` `CERTIFIED`.
- **P3. Producer** (adapter L177-181): the producer sha and the adapter's own sha are in the approved set (a1dcdea8, 4de70486); the producer bytes re-hash; the producer sha is RESPONSE_SHA `a1dcdea8…`. The canonical producer path (the runner's R4 condition) is checked through P6.
- **P4. The registered numerical checks** (adapter L189-190): `validate_numeric_candidates(record, required, edge)` passes, with `(required, edge)` from `shell_plan(spec)`. This covers finite fields, the registered shell coverage, the dense audits, the refinement rule, the discrete levels and sample counts, the search metadata, dominance of every recorded candidate, and `eps_max` with its shell.
- **P5. Bindings** (adapter L182-188; runner L714-719): `numeric_ref` is the exact pin of P1; `point_sha256` and `custody_sha256` equal `derive_details(spec)`, the point's key in the 31-point table and `STAGE_CONTEXT`'s custody; `adapter_sha256` is `4de70486…`.
- **P6. Stage record:** `STAGE_EPS` has `ok: true`, and its checks are exactly the nine runner c3v002 `check_eps` names (L272-282), each true. The `STAGE_CONTEXT` checks of checklist E8 (`source_pins_match_anchor`, `anchor_context_record_present`) are recorded, not gating; Claude4's anchor hand check (P7) covers them for the anchor.
- **P7. The anchor point only** (checklist E7): every `ANCHOR_EPS_CROSSCHECK_*` record in this anchor attempt's folder counts, and at least one must exist. Each must have schema `S4RC1_ANCHOR_EPS_CROSSCHECK_C3V002`, bind `anchor_eps` to the P1 pin and `eps_cert_v006` to the canonical `598c8fa3…` pin, and read AGREE. Other anchor attempts are not consulted.

**Otherwise no review is written.** The script prints one JSON line with the item code and the reason, exits 3, and writes nothing. With no review, adapter v003 refuses with `INDEPENDENT_NUMERICAL_EPS_REVIEW_MISSING`, so the point's EPS stays UNAVAILABLE and the blocker is preserved. If the exclusive write succeeded but its re-hash then failed (INSTANCE_WRITE_CHECK), a file may exist; **only exit 0 with the printed sha256 is an instance.**

**Recorded, never gating:**
- the shells with `refinements` 1 (checklist E3);
- the minimum and maximum `dense_over_production` over the audits, excluding null ratios (zero production), whose count is recorded (E5). Checklist E5's "reject, or flag for root" is not open to the script;
- `eps_max` and its shell (E6). There is no bare EPS magnitude gate (A134 Q10).

These go into the instance's `checklist_results`. A value root wants to question is root's to raise; the script does not reject on it, because Q8 allows no discretionary input.

## 3. The convention this review accepts

- The EPS values are search lower bounds on the continuous supremum. The review accepts them only as the **registered numerical convention** (the A52.5 envelope rule), never as a rigorous supremum: `accepts_registered_numerical_estimate_not_rigorous_sup: true` (checklist E9). This is the policy's acceptance, not a test from bytes.
- An APPROVED instance certifies only the per-point record's form and its registered convention. RB-FP coverage off the anchor stays UNTESTED (A134 Q8, Q10).

## 4. The instance

One JSON file per point attempt and numerical record, named `EPS_REVIEW_INSTANCE_C4V001_<point dir>_n<numeric sha12>.json`, written by exclusive create in **`claude_artifacts/eps_policy_review_c4/instances/`**, outside the CP-1 runner's output root. Its 15 fields satisfy adapter v003 L184-188 and the runner's checks (runner L714-719 and `distinct_review_problems`):

| field | value |
|---|---|
| `schema` | `UNT_POINT_EPS_REVIEW_CX2V001` |
| `verdict` | `APPROVED` (the only verdict the script writes) |
| `numeric_ref` | the exact pin of P1 |
| `point_sha256`, `custody_sha256` | from P5 |
| `adapter_sha256` | `4de70486120de215838f5ca2b0c9464d52a0edc3d5280dd042d5521d60f1c372` |
| `accepts_registered_numerical_estimate_not_rigorous_sup` | `true` |
| `reviewer_lane` | `Claude4` |
| `distinct_from_producer_lane` | `true` |
| `reviewed_utc` | the system UTC clock at writing, `YYYY-MM-DDTHH:MM:SSZ` |
| `policy_review` | `{path, sha256}` as given by `--policy` and `--policy-sha256`; the script checks only that the bytes hash to the sha and that the text names the script's sha |
| `instantiated_by` | `{path, sha256}` of the script |
| `checklist_results` | E1 to E10: the mechanical results of the identification checks and P1 to P7, and the recorded values. E9 is the §3 acceptance; E10 rests on P5 and distinctness |
| `findings` | empty |
| `signature` | exactly `Claude4, by policy review <policy sha256>, instance <reviewed_utc>` |

**Who runs the script.** Root, the CP-1 operator, runs it. Root holds the read set that `derive_details` needs, the same as adapter v003 `adapt_eps`: the A2 anchor run's result.json and the uv-tail modules through the static pins, the A2 coefficient grid, the DDO154 geometry inputs and prereg V005. Claude4 does not read run trees. Root runs it with `-I -B` under `taskpolicy -b`, as the run sheet does for adapt-eps.

**The order (Q8 "first").**
- Root runs the script for the anchor point first. Claude4 then checks the anchor instance by hand: the runner's anchor cross-check against EPS_CERT_V006, its `tolerance_relative` (at most the anchor tolerance root fixes in the CP-1 run sheet), `overlap_shells` = 178, and the STAGE_CONTEXT checks. Claude4 posts the result.
- **No non-anchor instance is issued before that post reads PASS.** The script would issue one, so this rule is root's to apply.

**Root's acts.**
- Root passes `--out-root` as the CP-1 out-root (`s4rc1_c3/cp1_*`) and `--output-dir` as the instances folder above.
- Before adding an instance's sha256 to `approved_review_sha256`, root checks that its `policy_review` is this pinned text and its `instantiated_by` is the pinned script `e3524586…`. Any text that quotes the script's sha would otherwise pass the script's own check.
- Root passes `--approved-signer-lane Claude4` to adapt-eps.
- Only root writes the trusted lists.

**Distinctness.** Claude4 is neither the CP-1 operator (root) nor the numerical producer's author (Codex2). The script checks this mechanically from POINT_START's `operator_lane`, refusing Claude4 or a blank lane, case-sensitively as the runner does (DISTINCTNESS). It also self-checks the instance against the adapter and runner fields (INSTANCE_SELF_CHECK).

## 5. Limits

- **The real custody path is UNTESTED.** Every test stubbed `derive_details`, with real identity and point key and synthetic custody. The deciding test is the anchor round trip in the CP-1 window, run by root.
- P6 and P7 read the values the runner recorded; they do not recompute `check_eps` or `compare_anchor_records`.
- The other verifier notes (VC4-07 to VC4-10, and VC4-12) are NOTE class under A115 and change nothing here.

## 6. What this review is not

- Not a hand review of each point. The anchor instance alone is also checked by hand (§4).
- Not an LO review, a cap review or a row-reference review (A134 Q4, Q8).
- It changes no record, no threshold and no registered setting.

Signed: Claude4, 2026-10-19T12:50:30Z.
