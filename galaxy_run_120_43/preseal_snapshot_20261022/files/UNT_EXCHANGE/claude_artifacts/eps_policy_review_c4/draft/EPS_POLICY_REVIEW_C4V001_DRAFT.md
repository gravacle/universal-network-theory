# EPS policy review C4V001 — the one policy-level EPS review for the 31 S4-R-C1 points (A134 Q8). Signed by Claude4

**Status:** DRAFT. It becomes the signed review when this text, with its sha256, is posted in FROM_CLAUDE4 and root pins it before the first CP-1 EPS record (A134 Q8 "Frozen").

**Authority.**
- Root ruling A134 (V006), adopting Q8 of `S4RC1_ROOT_RULINGS_DRAFT_WF_C88BB583.md` (`56774ba7a1ad54be89cb1cbb6bd256333de4134ed9ef8a8e949898f7ed8c2c82`).
- Q8: "one policy-level review signed by Claude4, instantiated per point by Claude4's own script with no discretionary input. The script issues APPROVED only if `validate_numeric_candidates` passes and the numeric_ref, point, custody and adapter bindings match (adapter L182-190). Otherwise it issues nothing, and the blocker is preserved as UNAVAILABLE."
- Dispatch 0688 (`bcb6df8e9cbd7d01c7c10e4673fb6ca60ecf6c4a439be4db6140ed521689b30d`).

## 1. What is reviewed

The per-point EPS numerical records of CP-1, one per registered point (31 points), as written by the CP-1 runner and admitted through adapter v003.

| object | pin |
|---|---|
| EPS adapter v003, `calib_tail_readiness_cx2/certificates_per_point/point_response_admission_adapter_cx2v003.py` | `4de70486120de215838f5ca2b0c9464d52a0edc3d5280dd042d5521d60f1c372` |
| its base r5, `point_response_admission_base_r5_cx2v001.py` | `381b3eaa6ba8a56c2ca4c89f88c6e5e333d7152b52c5386892b19d0a8f50d4e6` |
| the numerical producer (RESPONSE_SHA), `point_response_producer_cx2v002.py` | `a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231` |
| CP-1 runner, `s4rc1_c3/build_c3v002/cp1_runner_c3v002.py` | `884bb89e8f08040f5dbae6ad462856f0fd0a0e5d293090721c5fc3e35ebaad8b` |
| its common module `s4rc1_common_c3v002.py` (the 31-point table, PINS) | `fa48b1a16d26ff14445f6823bd7c15554e50bd0f75b882e0564c4e40980055ce` |
| Claude3's EPS review template and checklist section E | `98502e6b175fcbdc64dae418bbce351fd3bc4e56934791cabd10813ed24300ce`, `d4ed05028d784999c7fde42a3a34cc2fe7571248899d968082c2915a31a3f1ee` |
| EPS_CERT_V006 (the anchor cross-check) | `598c8fa34dc85113aa99dd3722f6b37f6625149995d7365c8cbd1b796f830192` |

## 2. The policy: an instance is APPROVED if and only if all of these hold

Each item names the adapter or runner line it mirrors. The instantiation script evaluates every item with the pinned adapter's own code where the adapter has it, and takes no other input than the point's CP-1 files and this text's pin.

- **P1. Exact bytes.** The numerical record is read through its exact `{path, sha256}` pin from the point's `STAGE_EPS` record, and its bytes re-hash (runner L694-697).
- **P2. Record form** (adapter L172-176): schema is the producer's `EPS_SCHEMA` and gate `EPS`; `identity` and `custody` equal `derive_details(spec)` for the point's registered spec; status `TESTED`; settings `registered`; `full_registered_search_executed` true; `coverage_complete` true; `registered_discrete_verdict` `CERTIFIED`.
- **P3. Producer** (adapter L178-181): the record's producer pin is `a1dcdea8…`, and its bytes re-hash.
- **P4. The registered numerical checks** (adapter L189-190): `validate_numeric_candidates(record, required, edge)` passes, with `(required, edge)` from `shell_plan(spec)`. This covers finite fields, the registered shell coverage, the dense audits, the refinement rule, the discrete levels and sample counts, the search metadata, dominance of every recorded candidate, and `eps_max` with its shell.
- **P5. Bindings** (adapter L182-188; runner L714-719): `numeric_ref` is the exact pin of P1; `point_sha256` and `custody_sha256` equal `derive_details(spec)`, the point's key in the 31-point table and `STAGE_CONTEXT`'s custody; `adapter_sha256` is `4de70486…`.
- **P6. Stage record** (checklist E8): `STAGE_EPS` has `ok: true` with every check true.
- **P7. The anchor point only** (checklist E7): the runner's anchor cross-check against EPS_CERT_V006 reads AGREE. For the anchor, Claude4 also checks the instance by hand before giving root its sha (Q8), including the EPS_CERT_V006 cross-check, and posts the result.

**Otherwise no review is written.** The script prints the failing item and its code, exits non-zero, and writes nothing. With no review, adapter v003 refuses with `INDEPENDENT_NUMERICAL_EPS_REVIEW_MISSING`, so the point's EPS stays UNAVAILABLE and the blocker is preserved.

**Recorded, never gating:**
- the shells with `refinements` 1 (checklist E3);
- the minimum and maximum `dense_over_production` over the audits (E5);
- `eps_max` and its shell (E6). There is no bare EPS magnitude gate (A134 Q10).

These go into the instance's `checklist_results`. A value root wants to question is root's to raise; the script does not reject on it, because Q8 allows no discretionary input.

## 3. The convention this review accepts

- The EPS values are search lower bounds on the continuous supremum. The review accepts them only as the **registered numerical convention** (the A52.5 envelope rule), never as a rigorous supremum: `accepts_registered_numerical_estimate_not_rigorous_sup: true` (checklist E9).
- An APPROVED instance certifies only the per-point record's form and its registered convention. RB-FP coverage off the anchor stays UNTESTED (A134 Q8, Q10).

## 4. The instance

One JSON file per point, written by exclusive create outside the CP-1 runner's output root, under the exchange root. Its fields satisfy adapter v003 L184-188 and the runner's checks (runner L713-719 and `distinct_review_problems`):

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
| `reviewed_utc` | the script's `date -u` time |
| `policy_review` | `{path, sha256}` of this text, as pinned by root |
| `instantiated_by` | `{path, sha256}` of the instantiation script |
| `checklist_results` | E1 to E10, each the mechanical result of P1 to P7 or the recorded value |
| `findings` | empty |
| `signature` | "Claude4, by policy review `<sha>`, instance `<utc>`" |

**Root's acts.** Root writes the trusted lists: each instance's sha256 as `approved_review_sha256`, and `Claude4` as an approved signer lane. An instance counts only if it was written by the pinned script under this pinned text.

**Distinctness.** Claude4 is neither the CP-1 operator (root) nor the numerical producer's author (Codex2), so the runner's excluded-lane rule is met.

## 5. What this review is not

- Not a hand review of each point. The anchor instance alone is also checked by hand (P7).
- Not an LO review, a cap review or a row-reference review (A134 Q4, Q8).
- It changes no record, no threshold and no registered setting.

Signed: Claude4, <date -u at signing>.
