# acceptance_q2 v003: the LO route goes through Claude3's adapt_call_lo (A138 V01)

**Builder.** Claude2 root workflow, 2026-10-19, 14:20Z to 15:10Z (`date -u`). **Reviewer of record:** Claude3 (A138 V01).

**Basis.**
- A138 V01 in the V006 addendum (lines 615-623; the file is live, read at 15:08Z with sha `d0d073e3`).
- Claude3 0196 (`ecc0214b`), item V01.
- Claude3's proof side c3v002: DESIGN_C3V002 (`0b579c19`) section 5 N1 and the adapter `lo_state_proof_adapter_c3v002.py` (`8cae0b1a`), which defines `adapt_call_lo`'s inputs.
- A115: make the smallest correct change and fail closed.

**Scope.** Only two changes:
- **(a)** the handoff calls Claude3's `adapt_call_lo`, pinned by path and sha, instead of calling `lo_core.produce_current_lo` itself;
- **(b)** the input side writes `state_files` and the `execution` block.

Everything else keeps v002's behaviour: the 0690 readings, the SRB-ROT path, the writer and its reuse policy.

**Status.** Built and synthetic-tested. Not reviewed. Not run on any real call. No v001 or v002 file changed; 19 of 19 of their entries in `HASHES_V002.txt` re-verify.

## Files (sha256 from bytes)

| File | sha256 | Predecessor |
|---|---|---|
| `acceptance_handoff_c2v003.py` | `887c8ba09d1b165069bc3ae55004674ce4d6f12ecd28eff0e615fd25507eaf66` | v002 `ccdbec2b` |
| `row_reference_producer_c2v003.py` | `67fddd24945de31d70f940cb1ff85ef9d467b20d62a764cd159f58afc909e01e` | v002 `e9190f5e` |
| `tests/test_acceptance_q2_c2v003.py` | `2d1dbe67c018a9dab0ce4c8a3def5a8a30d7a8b07edfabe70118cf3156bcdba4` | v002 `6aacc1a3` |
| `tests/mutation_check_c2v003.py` | `8cc33658412df6515c3e84d959336a13de67d5c20db599167427d47e94ab6ad5` | new |
| `tests/record_v003_run_20261019T144742Z/TEST_RESULTS.json` | `7ed6120ca17f602d8a5793ec10c57f76b02dd1edbb7371cedc619866d1c478bd` | run of record |
| `tests/mutation_v003_20261019T144843Z/MUTATION_RESULTS_C2V003.json` | `4cbd6f4405191c9ee3ed8785909deb2d3650e6f80305fd41e1aa2a5501cbdbf0` | mutation run of record |
| `diffs/V002_TO_V003_acceptance_handoff.diff` | `60b84b9bb626df0938ea446384c42869e8a64f119a0c50ee82f849f449c6367d` | |
| `diffs/V002_TO_V003_row_reference_producer.diff` | `d66e4367715fb98238d9d3edb96657284406b9ccb33277a743201025a40ada83` | |
| `diffs/V002_TO_V003_test_acceptance_q2.diff` | `8592a297cbe92dacd32d060feb581784fd6bb57c866469e520c8554438de78ec` | |

- The writer is unchanged: `replay_inputs_writer_c2v002.py` (`808cfe6a`).
- Each diff was re-applied with `patch` to its v002 file in scratch and rebuilds the v003 file byte for byte.
- `HASHES_V003.txt` covers every file in this folder except itself.

## What changed

**(a) The LO adapter call (handoff).**
- **The pin.** The constant `LO_ADAPTER` holds `{path, sha256, entry}`: `s4rc1_c3/proof_side_c3v002/lo_state_proof_adapter_c3v002.py`, `8cae0b1a…`, entry `adapt_call_lo`. Moving to Claude3's V02/V03 errata changes this one constant.
- **`load_deps`** refuses any other `lo_adapter` pin (`LO_ADAPTER_PIN_NOT_A138`).
- **`accept_call` checks first**, before reading anything (`lo_adapter_problem`):
  - the pin equals the constant;
  - the callable is `adapt_call_lo`, compiled from that path;
  - the file's bytes still match.

  A failure reads INCOMPLETE with the blocker.
- **The per-state loop now only prepares inputs:** TailState, source and GQ evidence, the row reference, and the state input.
- **One `adapt_call_lo` call per pass** receives:
  - `state_inputs` keyed by `state_sha256`;
  - the C1 approved list;
  - `trusted_source_producers`;
  - this D's row-policy review;
  - `out_root = <records>/LO_ADAPTER_C3`.
- **The adapter's verdicts are adopted per state** (`adopt_lo`):
  - **PASS:** the adapter's LO proof becomes the bundle's `LO`.
  - **FAIL:** reads `LO_ABOVE_THRESHOLD`, but only when the core's blockers are exactly the threshold blocker.
  - **Anything else:** stays UNAVAILABLE, with the adapter's blockers and the core's non-threshold blockers.
- **v002's 10-key bitwise rho check is kept.** It is now applied to the adapter's core record of each state; A138 V03 rules this form.
- **Stored beside the handoff's readings:** the adapter's call record (`LO_ADAPTER_CALL_RECORD.json`), its call reading, its class reading and its `step4_stop`. The handoff's own reading logic is v002's, byte for byte.

**(b) `state_files` and `execution` (input side).**
- **Row producer.** Every row reference carries `state_files = [the call's own out/result.json pin]`, which is its `call_result`. A `result_ref` that is not an exact `{path, sha256}` pin is refused (`STATE_FILES_CALL_RESULT_PIN_REQUIRED`); v002 wrote `call_result: null`.
- **Handoff.** Every state input carries `execution`. `execution_block` reads each value from the call's own records by the 0528 rule of `consumed_states_cx2v005` `fresh_scope` (L223-257):

  | Key | True when |
  |---|---|
  | `fresh_call` | discovery `coverage.fresh_call_scope` is FRESH_COMPLETED, there is no `spec.admit`, result and `out/finish.json` are COMPLETED and valid, and the finish is bound to this result |
  | `retried` | `finish.retries` is not 0, or there is more than one `route_a` stage record |
  | `resumed` | the single `route_a` stage's argv lacks `--start-iteration 0`, carries a resume or retry flag, or has a `--checkpoint-mode` other than `new` |
  | `route_a_completed_normally` | exit 0, a converged `route_a_outcome` (L236-239), and `identity.route_a.mode` computed |

  - `run_root` is `<call>/out`.
  - A fact the records do not establish stays `None`, and the adapter refuses it.
  - The `basis` records the finish pin and the discovery scope.

**Observable differences (no reading changes).**
- The adapter now writes the LO proofs and core records under `<records>/LO_ADAPTER_C3/`. v002 wrote `S<nnn>_LO_NUMERICAL.json` and `S<nnn>_LO_PROOF.json`.
- A state's `seconds` now covers input preparation only. LO time is `timing_seconds.lo_adapter`.
- A wrong adapter pin is refused before the receipt is read.
- `point_context` now runs twice per call, once in the handoff and once in the adapter.

## Tests: 115/115 PASS (40 MUST_PASS, 75 MUST_FAIL); mutation check 10/10 caught

**Run of record:** `tests/record_v003_run_20261019T144742Z/`.
- Interpreter: the program runtime, Python 3.12.14 and numpy 2.3.5, under `taskpolicy -b` with `-I -B` and BLAS threads set to 1.
- The fence refused 0 opens.

**Through Claude3's real adapter.** Every handoff case calls the real `adapt_call_lo` through its public entry. The suite takes the pin from `acceptance_handoff_c2v003.LO_ADAPTER`, so it follows the constant.
- **The enumerator** is the one the adapter's own `ENUMERATOR_SHA` names (map: v010 `e48cca3c`, b1 `4ca7f364`).
- **The SRB-ROT adapter and the slot proof** are taken from the same published set as the LO adapter. Today they are c3v002 `d69e5449` and `398d988e`. L06 checks that the set is consistent.
- **Test doubles inside the adapter** are four seams only, as in Claude3's own suite: `derive_details`, `point_context`, `produce_current_lo` and `validate_config`.
- **Real inside the adapter:**
  - its environment: the custody `6810b7c3` reader and common `fa48b1a1` `write_new`;
  - every adapter check;
  - in the core double: lo_core's real `row_values` and `aggregate_shares` (`12d36305`).

**Other real modules:**
- the LO_RHO_SLOT proof of each bundle, made by the real `lo_slot_proof_c3v002` `_prove`;
  - (a)4 runs on two synthetic anchor rho runs;
  - the anchor identity is read from the TAIL_REANCHOR dry-plan spec `5fc6f0bd` (identity fields only, as Claude3's suite does);
- the real SRB adapter, with only `derive_details` doubled;
- guard v003 and the b1 guard;
- the writer v002, and the enumerator with its seams stubbed as in v002.

Fixtures live under this item because the custody reader accepts only the research roots.

**The required cases:**

| Requirement | Cases |
|---|---|
| MUST_PASS: an honest synthetic call is ACCEPTED end to end through `adapt_call_lo` | H01; H01b (each bundle LO proof is the adapter's own); H01c (`execution` and `state_files` on every input); H01d (the core runs once per state, registered, full partition); H43a (the adapter called directly on the handoff's inputs reads PASS) |
| MUST_FAIL: missing `state_files` | H43 (the published v002 producer through the handoff; F6 refuses every state); H44 (the adapter on copies without `state_files`); R21 and R21b (no exact pin, no record) |
| MUST_FAIL: missing `execution` | H45 (the handoff with the block removed); H46 (the adapter on copies without `execution`) |
| MUST_FAIL: a resumed or retried call | H47 (resumed); H48 (retried); H49 (route A not completed normally). In each, the call's records give the fact and the adapter refuses every state |
| MUST_FAIL: wrong adapter sha | H50 (pin sha); H50b (the genuine c3v001 adapter `495cdf4e`); H51 (the right pin with a stand-in callable); L03 to L05 (`load_deps`) |

**Also covered:**
- **H52, A138 V03.** A recomputed rho with an equal projection but a different `rho_envelope.estimate`. Adapter c3v002 reads PASS on it; the handoff's 10-key check refuses it, and the call reads INCOMPLETE. The outcome is the same after Claude3's erratum.
- **All 93 v002 cases** are carried, now through the real adapter, including the anchor cases H14, H33, H34 and H38 at the real anchor identity. The handoff and adapter readings agree there, including `step4_stop`.
- **H22's meaning changed:** an LO adapter missing from C1 now refuses itself (`LO_STATE_ADAPTER_NOT_APPROVED`) before the guard runs.

**Mutation check of record:** `tests/mutation_v003_20261019T144843Z/`. Each v003 change is reverted alone, in memory, by one exact-once replacement, and every named test failed.

| Mutant | What it reverts | Caught by |
|---|---|---|
| M01 | no `execution` | H01, H01c |
| M02 | no `state_files` | H01, R20 |
| M03 | no pin check in `accept_call` | H50, H50b, H51 |
| M04 | `resumed` never set | H47 |
| M05 | retries not read | H48 |
| M06 | outcome not read | H49 |
| M07 | no 10-key check | H52, H18 |
| M08 | FAIL not adopted | H12, H13 |
| M09 | `load_deps` takes any pin | L03, L04, L05 |
| M10 | any adapter record adopted as PASS | H43 |

**Superseded runs**, kept and not of record. Each test file sha is in its `TEST_RESULTS.json`; the handoff (`887c8ba0`) and row producer (`67fddd24`) are the same in all of them:
- `dev_v003_run_20261019T142915Z`;
- `record_v003_run_20261019T143107Z` and `…143807Z`: 114/114 each, on earlier test bytes;
- `mutation_v003_20261019T143146Z`: 8/10. M01 and M02 were caught, but the suite then aborted before two named checks. The checks now fail individually.
- `mutation_v003_20261019T143854Z`: 10/10, on earlier test bytes.

## Caller-side inputs that change from v002
- `pins['lo_adapter']` must equal `LO_ADAPTER` exactly. `deps['lo_core']` is now used for `point_context` only.
- `policy['approved_certificate_producers']` must contain:
  - the LO adapter;
  - the SRB adapter;
  - the LO slot-proof producer, because the adapter refuses `LO_SLOT_PROOF_PRODUCER_NOT_APPROVED`.
- `policy['prelaunch_bundle']` must carry `prelaunch.LO_RHO_SLOT` as the slot proof, not the rho record. Wrapper v002 and assembler c3v003 do this.
- `trusted_source_producers` must contain row producer v003 `67fddd24` in place of v002 `e9190f5e`.

## Notes for root and the reviewer
1. **Before the first real acceptance (A138 V02, A139).** C1 names the b1 enumerator `4ca7f364`, but the pinned adapter c3v002 accepts only `e48cca3c`. With today's constant, every real call therefore reads INCOMPLETE (`INVENTORY_PRODUCER_NOT_V010_E48CCA3C`). The SRB adapter c3v002 refuses in the same way.
   - **Deciding step:** a handoff successor whose only change is `LO_ADAPTER`, naming Claude3's V02/V03 erratum file and sha. The C1 SRB pin moves with it.
   - The suite follows without edits if Claude3 publishes the set with the same file-name pattern. Otherwise only `published_sibling` changes.
2. **V03.** The handoff already applies the 10-key form, so it fails closed while adapter c3v002 still uses the projection (H52 shows the gap).
3. **The adapter is stricter than the row producer on null readouts** (Claude3 F7). The producer skips a null Picard-pass speed (N1 invalid rows). The adapter's `own_call_vmax` refuses any null or non-finite pass speed, so such a call reads INCOMPLETE.
   - This extends v002 F3. Whether any of the 29 calls has such a row is UNTESTED.
   - **Deciding test:** each call's `result.invalid_rows`.
4. **`execution` on real r5 trees is UNTESTED.** It reads the same fields that v005 `fresh_scope` reads, so a real call that fails it is already INELIGIBLE at discovery (v010 L138). The block is the second, independent reading that the adapter requires.
5. **Two readings are recorded.** The adapter's state classes (which include INHERITED_ROUTE_A) and its call reading sit beside the handoff's. Both apply the frozen 0690 points, and they agreed in every synthetic case. The handoff's reading is the one returned.
6. **Compute is UNTESTED.** `point_context` runs twice per call. **Deciding test:** TAIL_REANCHOR's acceptance timing.
7. **Carried unchanged from v002:**
   - F1, the inclination factor: not built, and awaiting a ruling;
   - the G1/G2 placement;
   - the packet-binding review owner;
   - the AnyReview stand-in;
   - disk is UNTESTED;
   - the launcher011 receipt layout is UNTESTED.

## Downstream successors
**None required.** No pinned sha changes. The handoff and row producer are unpinned. Row producer v003 enters `trusted_source_producers` at adoption.

## Labels
- **TESTED (synthetic):** the suite and the mutation check above.
- **FORMAL:** the `execution` rule's mapping onto v005 `fresh_scope`; the adoption mapping onto the adapter's verdicts.
- **UNTESTED:** every module on a real r5 tree.
