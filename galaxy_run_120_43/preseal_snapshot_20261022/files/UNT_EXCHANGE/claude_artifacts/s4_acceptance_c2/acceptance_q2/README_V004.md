# acceptance_q2 v004: the LO route pins Claude3's published c3v003 adapter (A145)

**Builder.** Claude2 root workflow, 2026-10-19, 15:56Z to 16:52Z (`date -u`). **Reviewer of record:** Claude3, v004 only, lean (A145).

**Basis.**
- A145 in the V006 addendum (`## A145`, lines 842-857).
- Claude3 0208 (proof side c3v003 published; notes N4 and N5).
- The v003 verifier's non-blocking notes in `NO_FIX_NEEDED_V003.txt` (`c97c0195`): N2, N3, N4, N5.
- offset_b1 `README.md`, Downstream item 5 (the b1 evidence module `7044e131` in `trusted_source_producers`).
- A115: make the smallest correct change and fail closed.

**Scope.** Only these changes to the handoff:
- **(a)** `LO_ADAPTER` pins Claude3's published c3v003 adapter;
- **(b)** `adopt_lo` adopts an adapter PASS only with an exact `core_record` pin (verify N2);
- **(c)** `route_a_completed_normally` needs `converged_finite_fixed_point is True` (verify N4);
- **(d)** root's `trusted_source_producers` must name the b1 evidence module `7044e131` (0208 N5).

The README errata of v003 (verify N3 and N5) are fixed below. The row producer, the writer and every reading rule are unchanged; no row producer v004 was needed.

**Status.** Built and synthetic-tested. Not reviewed. Not run on any real call. No v001, v002 or v003 file changed: every entry of `HASHES.txt` (12258/12258), `HASHES_V002.txt` (18348/18348) and `HASHES_V003.txt` (236112/236112, `0821d05f`) re-verifies from bytes.

## Files (sha256 from bytes)

| File | sha256 | Predecessor |
|---|---|---|
| `acceptance_handoff_c2v004.py` | `5ff464cc866d3e69ef83ab7542701b211afaae29d7be14e69b10fb09f16692d8` | v003 `887c8ba0` |
| `tests/test_acceptance_q2_c2v004.py` | `085cafbe8c7abebe15a0364eefa53dccb80214cd58c2d51e974b02c3d85ce4d4` | v003 `2d1dbe67` |
| `tests/mutation_check_c2v004.py` | `c2a74413e6dc47e9b61beb76ce3bcaefc4cbb46bcd39ddaec157fbf22763810a` | v003 `8cc33658` |
| `tests/record_v004_run_20261019T162648Z/TEST_RESULTS.json` | `c02f664388f79b34ed4870d2b0f0e5d932a33863b2fa5a6b4c9f8fca0751ba2f` | run of record 1 |
| `tests/record_v004_run_20261019T162648Z/RUN_FILE_MANIFEST.json` | `4446971aebe8d34bb6e8c9c7e009e74cde7678873c95211d45ca27b824e181df` | run of record 1, file manifest |
| `tests/record_v004_run_20261019T162744Z/TEST_RESULTS.json` | `db86232218a906f7a01a5ad66237f8ea9c3ad76a59527c800e3d4e8ff351441a` | run of record 2 |
| `tests/record_v004_run_20261019T162744Z/RUN_FILE_MANIFEST.json` | `de1ca777abb1af9acb1b35e2f619c4ba313fe2790d7ae19f3e787d31b4913c9b` | run of record 2, file manifest |
| `tests/mutation_v004_20261019T162832Z/MUTATION_RESULTS_C2V004.json` | `20d53e4630b33274abdcba1802c8c3f7e0960448e14a88a9bdb09917920b8b9d` | mutation run of record |
| `diffs/V003_TO_V004_acceptance_handoff.diff` | `d587ed69dce9fd880ed09883e12d53652f186efde2b9ffed7f89362f976210f8` |  |
| `diffs/V003_TO_V004_test_acceptance_q2.diff` | `a8dd8a2cba1011f3796e6b95e747e76ae90a6f499f703281668e1e358ecf60fb` |  |
| `diffs/V003_TO_V004_mutation_check.diff` | `fe8e71fc41d78264f1e12daf297cb499655f9c28c5a6c6192c92d4cbdd5e1b50` |  |
| `tests/hash_check_v001_v003_by_v004_20261019T164420Z.json` | `2f10e276a6e9a41bdd8edbd6b7086edf9423842f3c1b1520fe7eec788403bd15` | v001-v003 hash re-check |

- Unchanged and still pinned by the tests: row producer v003 `67fddd24`, writer v002 `808cfe6a`.
- Each diff was re-applied with `patch` to its v003 file in scratch and rebuilds the v004 file byte for byte.
- `HASHES_V004.txt` covers the v004 files, both runs of record, the mutation run and the dev folder (see Deviations, item 3).

## Pins (each sha256 hashed from bytes at build and again by L07 in every run)

| Role | File | sha256 |
|---|---|---|
| LO adapter (`LO_ADAPTER`, entry `adapt_call_lo`) | `s4rc1_c3/proof_side_c3v003/lo_state_proof_adapter_c3v003.py` | `211a3220f015f8410f81e981f73355d9975d9b738a42a9d1092c28c4ae1c336c` |
| SRB-ROT adapter (root's `pins['srb_adapter']`; tests) | `s4rc1_c3/proof_side_c3v003/srb_rot_adapter_c3v003.py` | `08e9ac0a12cf1829f79f6df8a82c9ec6a7d174fc4bb25be76d3c049525dfae6a` |
| LO slot proof (prelaunch `LO_RHO_SLOT`; tests) | `s4rc1_c3/proof_side_c3v003/lo_slot_proof_c3v003.py` | `cd10cd59df44d7b79f3c3aa7ba88998d94c7292c4c2656e09bbbe16ded01bca3` |
| b1 evidence (`B1_EVIDENCE`) | `s4_acceptance_c2/offset_b1/current_source_evidence_b1_c2v001.py` | `7044e1310bb0b8cde08f7839b88b949409d15219fb24756f418224a0e7c0ddce` |
| b1 enumerator (both adapters' `ENUMERATOR_SHA`) | `s4_acceptance_c2/offset_b1/consumed_states_b1_c2v001.py` | `4ca7f3640bff6adc13d181a8045bec750681362595a9a9e71e643fa521af60f0` |

v003 pinned c3v002 in all three Claude3 roles: the LO adapter `8cae0b1a` (handoff constant), and the SRB adapter `d69e5449` and slot proof `398d988e` (suite, as the LO adapter's siblings). v004 replaces all three. The handoff constrains only the LO adapter; the SRB adapter remains root's `pins['srb_adapter']`, as in v003.

## What changed

**(a) The pin.** `LO_ADAPTER = {path: …/proof_side_c3v003/lo_state_proof_adapter_c3v003.py, sha256: 211a3220…, entry: adapt_call_lo}`. `load_deps` and `lo_adapter_problem` are unchanged, so the genuine c3v002 adapter (v003's pin) is now refused like any other (`LO_ADAPTER_PIN_NOT_A138`; H50c, L04b). c3v003 carries A138 V02 (b1 enumerator), V03 (10-key rho) and B3 (the 0690 OPEN-6 call reading). This addresses verify N1 (under c3v002 every b1 inventory read INCOMPLETE): TESTED on synthetic b1 calls (H01, H55); real calls UNTESTED.

**(b) `adopt_lo` (verify N2).** If the adapter reports PASS but its `core_record` is not an exact `{path, sha256}` pin, the state gets the blocker `LO_ADAPTER_PASS_WITHOUT_EXACT_CORE_RECORD_PIN` and stays UNAVAILABLE. Every adopted PASS has therefore passed the handoff's own 10-key rho check. FAIL adoption already needed the core record and is unchanged.

**(c) `execution_block` (verify N4).** One added line: `outcome.get('converged_finite_fixed_point') is True`, as `consumed_states_cx2v005` L237 requires. The integer 1 and the float 1.0 no longer read as completed normally. The `EXECUTION_RULE` text says `is True`.

**(d) The b1 evidence module in `trusted_source_producers` (0208 N5).**
- The handoff checks that root's list is a list or tuple containing `7044e131`. If not, it records `TRUSTED_SOURCE_PRODUCERS_WITHOUT_B1_EVIDENCE_7044E131 (…)` and the call reads INCOMPLETE. The NON_LAPSE_TAIL_MATERIAL, BOUND_INSUFFICIENT and UNDECIDABLE_FLAGGED readings keep their precedence.
- The handoff never adds to the list. Root's list goes to both adapters unchanged; H55 and H58 check what each adapter received.
- The reason: with b1 inventories `export_lo_source` is the b1 module, which stamps its own pin on every source reconstruction. lo_core L248-249 refuses an untrusted source producer, so without `7044e131` every state reads UNAVAILABLE (H58).

**N4 (refusal text).** The handoff matches no refusal text. The suite and this README use c3v003's `INVENTORY_PRODUCER_NOT_B1_4CA7F364` (H56); the c3v002 string `INVENTORY_PRODUCER_NOT_V010_E48CCA3C` appears in no v004 record.

**Observable differences from v003 (no reading rule changes).**
- A call that v003 read ACCEPTED reads INCOMPLETE in v004 when root's list lacks `7044e131` (H58b). v003's test policy had exactly that shape.
- An adapter PASS without an exact core-record pin is no longer adopted (H53, U01). With c3v003's real writer this cannot happen; H53 forces it at the adapter's write seam.
- A call whose route-A converged flag is a non-bool truthy value no longer has `route_a_completed_normally` True (H54, U02).
- On the c3v003 adapter, a rho with an equal projection but another shell record (V03) is refused by the adapter as well as by the handoff (H52b).

## README_V003 errata (verify N3 and N5)

1. **N3, note 5 of README_V003.** It said the adapter's and the handoff's readings "agreed in every synthetic case". Under c3v002 that was false in two cases:
   - H35: the handoff read LO_UNCERTIFIED_TRANSIENT and adapter c3v002 read INCOMPLETE (the B3 corner);
   - H52: adapter c3v002 read PASS and the handoff refused (the V03 gap).

   The returned reading was the handoff's in both, as 0690 requires, so no reading was affected. **Under c3v003 (v004, measured in each run of record):** in the 49 handoff cases run through `accept()`, the adapter ran in 42. In 41 of those its LO reading equals the LO part of the handoff's reading, H35 and H52 included. The one difference is H53_CORE_RECORD_NOT_AN_EXACT_PIN, by design: the adapter reads PASS, and the handoff refuses to adopt the PASS because the core-record pin is not exact. The handoff's reading is still the one returned. Both runs give the same pairs (`reading_pairs` in TEST_RESULTS).
2. **N3, line 120 of README_V003.** It said the readings agree "including `step4_stop`". That holds only for LO-driven stops. The adapter's `step4_stop` covers LO only; the handoff also stops on an SRB-ROT reading at the anchor (the v001 rule, kept). Measured in v004: `step4_stop` differs only in H38_ANCHOR_SRB_FAIL (an SRB-ROT failure at the anchor: the handoff stops, and the adapter's LO-only `step4_stop` is False).
3. **N5, observable differences of README_V003.** Missing from the list: `summed_lo_max_over_states` is the maximum over the states whose adapter result carried a readable core record. On an ACCEPTED call that is every state, so the value is unchanged from v002. On an INCOMPLETE call it can differ from v002's, which summed every state the handoff's own core call reached. v004 does not change this.

## Tests: 129/129 PASS (43 MUST_PASS, 86 MUST_FAIL) in both runs of record; mutation check 14/14 caught

**Runs of record:** `tests/record_v004_run_20261019T162648Z/` and `tests/record_v004_run_20261019T162744Z/`.
- Interpreter: the program runtime (`~/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`), Python 3.12.14 and numpy 2.3.5, with `-I -B`, under `taskpolicy -b` and with BLAS threads set to 1, as v003.
- The fence refused 0 opens in each run. Each run's `RUN_FILE_MANIFEST.json` pins every file the process wrote (8179 files per run).
- Both runs pass the same 129 cases with the same names and kinds; their reading pairs are identical.

**Carried from v003: all 115 cases, unchanged in name and kind.** They now run through the c3v003 set. Port changes:
- The pins are explicit (path and sha, bytes checked at load), not read from the handoff constant. L07 checks the constant.
- The enumerator is the b1 enumerator by explicit sha; L06 checks that both adapters accept exactly it.
- The default policy's `trusted_source_producers` gains `7044e131`, which change (d) requires. H43's list gains it too.
- H04 hashes the v004 handoff.

**The required v004 cases:**

| Requirement | Case | Kind |
|---|---|---|
| An honest b1 inventory call is ACCEPTED end to end through the real c3v003 adapter | H55: b1 inventory `4ca7f364` (the adapter's `inventory_digest` equals it), evidence records stamped with the real `7044e131` pin, b1 GQ_SIGNED and b1 guard, C1-shaped lists, LO and SRB-ROT through c3v003 | MUST_PASS |
| A v010 inventory is refused with the new string | H56: the handoff run on a v010 inventory; both adapters refuse with `INVENTORY_PRODUCER_NOT_B1_4CA7F364`; the old string appears nowhere | MUST_FAIL |
| H35 reads LO_UNCERTIFIED_TRANSIENT in both the handoff and the adapter | H35 (carried) and H35b | MUST_FAIL |
| H52 is refused by the adapter | H52 (carried) and H52b: every adapter state refused `RHO_RECOMPUTE_NOT_BITWISE_EQUAL_TO_SLOT`, with the projection still equal (diagnostic) | MUST_FAIL |
| Missing `7044e131` in the trusted list makes every state UNAVAILABLE | H58 (documented MUST_FAIL): every adapter state `SOURCE_RECONSTRUCTION_PRODUCER_NOT_APPROVED`, the handoff's blocker, INCOMPLETE. H58b: v003's list shape reads INCOMPLETE even though every adapter state passes | MUST_FAIL |
| A PASS with a non-pin core record is not adopted | U01 (None, an extra key, no sha); H53 (end to end: the adapter's real write with one key added to the returned core pin) | MUST_FAIL |
| The route-A flag as the integer 1 is refused | H54 (end to end; every state refused `FRESH_COMPLETED_NO_RESUME_NO_RETRY_CALL_NOT_ESTABLISHED`); U02 (1, 1.0 and "True"); U02b control | MUST_FAIL / MUST_PASS |
| The pins | L07 (the constant equals the c3v003 pin; all four shas from bytes; the b1 enumerator's evidence pin is `7044e131`); H50c and L04b (the genuine c3v002 adapter refused) | MUST_PASS / MUST_FAIL |

**Mutation check of record:** `tests/mutation_v004_20261019T162832Z/`. Each change is reverted alone, in memory, by one exact-once replacement, and every named test must fail.

| Mutant | What it reverts | Caught by |
|---|---|---|
| M01 | no `execution` | H01, H01c |
| M02 | no `state_files` | H01, R20 |
| M03 | no pin check in `accept_call` | H50, H50b, H50c, H51 |
| M04 | `resumed` never set | H47 |
| M05 | retries not read | H48 |
| M06 | route-A outcome not read (both lines) | H49 |
| M07 | no 10-key check | H52, H18 |
| M08 | FAIL not adopted | H12, H13 |
| M09 | `load_deps` takes any pin | L03, L04, L04b, L05 |
| M10 | any adapter record adopted as PASS | H43 |
| M11 | `LO_ADAPTER` back to c3v002 `8cae0b1a` (a) | H01, H55, L04b, L07 |
| M12 | PASS adopted without an exact core-record pin (b) | U01, H53 |
| M13 | the converged flag compared with `==` (c) | U02, H54 |
| M14 | trusted list not checked for `7044e131` (d) | H58, H58b |

M01-M10 are v003's mutants on the v004 handoff. M06 now removes both route-A outcome lines, because otherwise the `is True` line would still read the outcome.

**Superseded, not of record:** `dev_v004_20261019T155644Z/`, the dev copy of this item. The handoff was `5ff464cc` in every dev run.
- Its files are now byte-identical to the v004 handoff, test and mutation check, plus copies of the v002 writer and the v002 and v003 row producers.
- `tests/dev_v004_run_20261019T160357Z`: 129/129, on earlier test bytes (`2b869a49`).
- `tests/mutation_v004_20261019T160729Z`: 13/14 on those bytes. M11 failed H01, L04b and L07, but the H suite then aborted at H05 before H55 ran, so M11 counted as not caught. Fix (test only): the v002, v003 and v004 handoff groups now run as separate suites, and three new checks read optional keys with `.get`.
- `tests/dev_v004_M11_run_20261019T162534Z`: M11 alone on the final test bytes `085cafbe`. H01, H55, L04b and L07 all fail.
- `tests/dev_v004_run_20261019T162534Z`: 129/129 on `085cafbe`.

## C1 consequences (caller-side inputs that change from v003)
- `pins['lo_adapter']` must equal the new `LO_ADAPTER`.
- `pins['enumerator']` is the b1 enumerator `4ca7f364`; both c3v003 adapters refuse any other.
- `pins['srb_adapter']` is `srb_rot_adapter_c3v003.py` `08e9ac0a`, entry `adapt_call_srb_rot`.
- `pins['evidence']` is the b1 evidence `7044e131`, the enumerator's own evidence pin.
- `policy['approved_certificate_producers']` must contain:
  - the LO adapter `211a3220`;
  - the SRB adapter `08e9ac0a`;
  - **the LO slot-proof producer `cd10cd59`** (A145: it joins the approved list). The adapter refuses `LO_SLOT_PROOF_PRODUCER_NOT_APPROVED` without it;
  - the b1 evidence `7044e131`, in place of v004 `7289f2ba` (offset_b1 item 4), plus the EPS and uniform-GQ producers.
- `policy['trusted_source_producers']` must contain:
  - **row producer v003 `67fddd24`** (unchanged in v004; no row producer v004 exists);
  - **the b1 evidence `7044e131`** (0208 N5; checked by the handoff).
- `policy['approved_evidence_producer_sha256']` is `[7044e131]`.
- `pins['guard']` (or the wrapper successor's guard) is the b1 guard `9e3fc109`, as offset_b1 items 1 and 4 already require.

## Notes for root and the reviewer
1. **Real calls are UNTESTED.** H55 is the honest b1 call on synthetic records, and four seams of the adapter are doubles, as in v003 (`derive_details`, `point_context`, `produce_current_lo`, `validate_config`). **Deciding test:** the first real acceptance (TAIL_REANCHOR) under the published set (v003 N6 carried).
2. **0208 N2 bears on acceptance.** c3v003's per-state rho check is the 10-key form, so every shell diagnostic must reproduce bitwise across processes. The handoff already applied that form. UNTESTED on real inputs; **deciding test:** the CP-1 anchor pair (Claude3's).
3. **H54 uses the synthetic discovery stub,** which reports FRESH_COMPLETED. The real `consumed_states_cx2v005` discovery would also refuse such a call (L237), so `fresh_call` would be False there too. v004 makes `route_a_completed_normally` an independent second reading of that fact.
4. **H58b is a fail-closed check, not a gap.** In production `export_lo_source` is the b1 module, so a list without `7044e131` already makes every state UNAVAILABLE (H58). The handoff check names the cause at call level.
5. **Carried unchanged from v003:** README_V003 notes 3, 4, 6 and 7 (the null-readout strictness, `execution` on real r5 trees, `point_context` twice per call, F1, G1/G2 placement, the packet-binding review owner, the AnyReview stand-in, disk and the launcher011 receipt layout).

## Deviations (disclosed)
1. **The handoff checks (d) instead of only documenting it.** A145 lists four v004 items; this build's task adds (d). It is implemented as a check that never edits root's list, and it fails closed. It adds one pinned constant (`B1_EVIDENCE`).
2. **The suite no longer follows the handoff constant.** v003's suite read the adapter pin from `LO_ADAPTER` and found the SRB adapter and slot proof as its siblings. v004 pins all three explicitly, so that reverting the constant is caught (M11).
3. **`HASHES_V004.txt` is built without a directory walk.** This build may not list directories recursively. The file therefore covers: the named v004 files; each run's `TEST_RESULTS.json` and `RUN_FILE_MANIFEST.json`, plus every file that manifest names, re-hashed from bytes and compared with it (0 mismatches among 236,680 manifest entries over 33 runs); the mutation results; the dev folder; and the v001-v003 re-check output. Directories with no files are not listed.
4. **Interpreter flags.** `taskpolicy -b` and BLAS threads set to 1 were kept to match v003's record runs. They are not required by the suite.

## Labels
- **TESTED (synthetic):** the suite and the mutation check above; the v001-v003 hash re-check.
- **FORMAL:** that every adopted PASS has passed the 10-key check (by (b) and the code path); the mapping of (c) onto v005 L237.
- **UNTESTED:** every module on a real r5 tree; c3v003 on real inputs (0208 N2).
