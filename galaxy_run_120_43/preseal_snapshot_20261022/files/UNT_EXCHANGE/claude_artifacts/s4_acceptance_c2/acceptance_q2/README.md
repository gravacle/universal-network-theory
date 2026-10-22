# acceptance_q2: the A134 Q2 acceptance input side

**Builder.** Claude2 root workflow, 2026-10-19, 11:15Z to 11:31Z (`date -u`). **Reviewer of record:** Claude3 (A134 build table).
**Basis.** A134 (V006 addendum `c7a1cd04` at build time) adopts `S4RC1_ROOT_RULINGS_DRAFT_WF_C88BB583.md` (`56774ba7`, checked from bytes): Q2, Q3, Q4, the Q5 readings and Q10. A115 applies: make the smallest correct change and fail closed.
**Status.** Built and synthetic-tested. Not reviewed. Not run on any real call.

## Files (sha256 from bytes)

| File | sha256 | Role |
|---|---|---|
| `replay_inputs_writer_c2v001.py` | `ffa36e8db1b736b8077e90989ac97e8d994e491827dfda7e7f4b970beb3d4bad` | Replay-plan, descriptor and I1-T packet writer. |
| `row_reference_producer_c2v001.py` | `f483af8e50fa903dcba79a910a82898e1d82090df3e70861cf7163eb62712041` | Per-state row-reference records (`UNT_POINT_LO_ROWS_CX2V001`). |
| `acceptance_handoff_c2v001.py` | `02f438e1c1d841e661ba916e61fa420f8996cd14c6d250e1b516571a2a54d3fb` | The acceptance handoff root runs per call. |
| `tests/test_acceptance_q2_c2v001.py` | `b4c9c34230d0ccfb5c4fb643acf0c05dbd692a97f6f39696c6ca4363c505360a` | Synthetic MUST_PASS / MUST_FAIL suite. |
| `tests/record_run_20261019T113112Z/TEST_RESULTS.json` | `76f12fc0be2ec829b3059e3081cd24c352035d1cb7bfe1e0030ba015c77499cb` | Run of record. |

All three modules are new, so they have no predecessor. `diffs/NEW_*.diff` are unified diffs from `/dev/null`. **No existing file was modified, and no pinned sha changes.**

## What root runs, and in what order

`accept_call()` runs once per tail-ON direct call (HEADLINE11, SENS_LO9, SENS_HI9). It runs after the call's FINISHED receipt and before any value from the call is used.

1. **Receipt.** It checks the same fields as wrapper r10_c4 L109-113: `status` FINISHED, `driver_status` COMPLETED, and the result sha.
2. **Discovery and writer.** It runs the pinned v005 discovery, reached through the enumerator's `D`. Then the writer maps every real occurrence, in discovery order, to the call's own records:
   - route-A current and next states: rebuild from the sidecar elements, with the payload's `i1t` or `next_i1t`;
   - the boundary and the inherited reference and body states: `accepted_manifest`;
   - offset: the body finish `array_file` plus the accepted manifest;
   - `fs_columns` and `fs_rotation`: the offset `updated_base_arrays`;
   - `rfs_columns`, `le_columns` and `le_rotation`: the source-rotation finish `arrays_path`;
   - recipes: `kept`, `i1t` and `config_sha256` come from each stage finish's `uv_tail`, and `gamma_eff` from the accepted state record;
   - eval radii: taken exactly as the stage scripts pass them;
   - packets: the checkpoint blobs (gas, fixed stars, waves), `source_offset.npz`, `refreshed_prepared.npz` and `gas_source_feedback.npz`, with the Gauss order taken from the route-A attempt's `start.json`.

   It writes `<call>/ACCEPTANCE_INPUTS_C2V001/` and `<call>/TAIL_REPLAY_PLAN.json` by exclusive create. If any occurrence cannot be resolved, it writes typed gaps and **no plan**.
3. **Inventory.** It runs the C1 enumerator unchanged: v010 `e48cca3c`, or the b1 successor.
4. **Per consumed state:**
   - the TailState export: the accepted state reuses the manifest arrays, and every other state is a pinned reconstruction replay;
   - `export_lo_source` (evidence v004, or b1), which gives the GQ premises for nonnegative states and GQ_SIGNED for the offset state;
   - the row reference;
   - `produce_current_lo` (`12d36305`), unchanged;
   - the ρ check: ρ must equal the slot bitwise, over the same key set as the wrapper_q5 successor;
   - Claude3's per-state LO proof adapter.
5. **Accepted state only:** Claude3's SRB-ROT adapter (Q10), with the call's `TAIL_SOURCE_UNDERCONVERGED` flag passed in.
6. **Post-state bundle** (the prelaunch bundle, plus `parent_prelaunch_bundle` and `states`). It is checked by the guard acceptance phase (L155-219) directly, or by the wrapper successor's `write_acceptance` (Q3).
7. **Reading and record.** The reading is applied mechanically, and `ACCEPTANCE_RECORD.json` is written. The record carries:
   - every per-state result;
   - the summed LO for each state and the maximum over states (Q4(c));
   - the time of each stage (the Q2 deciding test);
   - `step4_stop_for_root_ruling` for an anchor failure (Q5).

**Reading precedence:** NON_LAPSE_TAIL_MATERIAL > BOUND_INSUFFICIENT > UNDECIDABLE_FLAGGED > LO_UNCERTIFIED_TRANSIENT > INCOMPLETE > ACCEPTED_PASS_FLAGGED > ACCEPTED.
- A threshold number recorded while any other LO blocker is open is not a failure reading. The state reads UNAVAILABLE, and the number is preserved.
- LO_UNCERTIFIED_TRANSIENT needs every other state's LO to have been read. Otherwise the call reads INCOMPLETE and records the iterate failure as `transient_candidate_unconfirmed`.

**The handoff never writes a proof and never approves anything** (test H04). The only proof producers are the evidence module and Claude3's adapters.

## Findings (A115)

**(a) BLOCKING. Every real call reads UNAVAILABLE under the pinned v010.** FORMAL, from code. The synthetic deciding case is test W17. Two inputs that v010 requires as own-call files under `<call>/out` are never written by r5:

- **G1: route-A initial rings.**
  - `from_prepared` (controller L220-285; prep v007 L155-165 and L201-211) keeps the rings (R, z, m) in memory. Only `identity.init_rings_digest` is archived (controller L213, written at L363).
  - Every route-A source selector needs the rings file (reconstruction L207-224; evidence L51-55, L64-65). So every call needs it: boundary, inherited, offset, and every iterate.
  - v010 L182 refuses any I1-T source file outside `<call>/out` (`SOURCE_PACKET_OUTSIDE_OWN_CALL`).
- **G2: the final route-A next state's gas packet.**
  - g_N = (1−r)·gas_{N−1} + r·updated_{N−1} (controller L483). The solver returns at L234 before relaxing, so g_N is never written.
  - It is re-derivable bitwise from checkpoint blobs START_{N−1} and COMPLETED_{N−1} (test W09).

**What the writer does now.**
- It takes both as root-supplied refs and checks them against own-call bytes: G1 against the archived digest, G2 by bitwise re-derivation (`derive_final_next_gas`).
- Without them, it writes gaps and no plan (W12, W14).
- The init-rings materializer is **not built**. It would replicate the prep v007 arithmetic under the call's module patches and is checked against the archived digest.

**Root must rule where the derived inputs live. The options:**
1. Under `<call>/out/` in a new subfolder that the driver never writes. This needs no pinned successor, but it departs from the replay-plan contract's phrase "original archives".
2. A v010 successor that admits these two derived inputs with the same checks.

**(a) BLOCKING. Per-occurrence packet-binding reviews have no owner.** TESTED in code: evidence `_approved` (L269-278) requires one distinct-lane `DDO154_CURRENT_SOURCE_REVIEW_CX2V001` per state occurrence, which is tens per call across 29 calls. No ruling assigns them.
- The handoff writes `PACKET_BINDING_REVIEW_REQUESTS.json` with the exact bound fields for each state (H20).
- A Q8-style ruling is needed: a policy-level review, instantiated per occurrence by a script.

**(b) b1 dependency.** TESTED, synthetic. Under guard v003 and the 0528 branch, an equal-mass offset is refused (H23). The same bundle passes the unreviewed b1 guard `9e3fc109` (H24). The handoff passes GQ_SIGNED through without reading it.

**Notes:**
- **N1. Readout set for |v_i| (DECLARED).** It is `rows`, `passes[*].rows` and `identity.route_a.route_a_rows`; null N1 entries are skipped.
  - Including the route-A rows follows Q4(a)'s "every readout … the call itself recorded". It can only raise |v_i|.
  - The three Q4 row-policy reviews (Codex1) bind this text through `speed_policy`.
- **N2. Adapter interface (proposed).**
  - LO adapter: `(spec, state, lo_record, lo_record_ref, uniform_gq_ref, details) -> proof`. The proof must carry `numeric_evidence` for wrapper_q5.
  - SRB-ROT adapter: `(spec, state, tail_state, row_reference_ref, eps_certificate, flagged, flags) -> {reading}`.
  - If Claude3's adapters differ, a handoff successor maps them. The handoff is unpinned.
- **N3. Cost (UNTESTED).**
  - Each non-accepted state is replayed three times: by v010, by the TailState export and by `export_lo_source`.
  - `produce_current_lo` recomputes the point-level ρ for every state.
  - TailState exports are written per state under `<call>/ACCEPTANCE_TAILSTATES_C2V001/` (disk use unmeasured; A124 applies).
  - Deciding test: TAIL_REANCHOR's acceptance timing, which the record captures.
- **N4. Layout prerequisites.**
  - Wrapper mode needs `<call>/spec.json` and `RECEIPT.json` (wrapper L96-113).
  - Whether launcher011's receipt matches is UNTESTED (Q3).
  - The records folder must be under `claude_artifacts`, because the guard reads the bundle and proofs only there (guard L37-55). `Store` refuses anything else (H25).

## Tests: 66/66 PASS (26 MUST_PASS, 40 MUST_FAIL)

Run of record: `tests/record_run_20261019T113112Z/`, Python 3.12.14 and numpy 2.3.5, run with `-I -B`.

**What runs for real:**
- v010 `e48cca3c`: plan validation, lineage, descriptor checks, the L182 location rule, and the final rehash;
- guard v003 `5f1e49e6`;
- the b1 guard `9e3fc109`;
- lo_core `row_values`;
- `load_deps` on the real pinned modules.

**What is stubbed:** v010's science seams (as in `test_consumed_join_cx2v003.py`). The `compute_i1t` stub is a shape oracle transcribed from reconstruction L354-381 and evidence L120-161. It returns the exact source-file list, so v010 L182 runs on the writer's real refs. Evidence `export_lo_source`, `produce_current_lo` and both adapters are also synthetic.

An audit-hook fence refuses any open under `runs`, `runs_ext`, `uvt_*`, `ngc3198` or C5H, and any write outside this folder. It refused 0 opens.

| Suite | Count | Covers |
|---|---|---|
| W, writer | 25 | **Pass:** v010 completes on the writer's output; radii, recipes and packet mapping by stage kind; G2 re-derivation; registered and geometry profiles. **Fail:** G1/G2 missing, digest or bitwise mismatch; derived inputs outside `out` (refused by real v010); result drift; missing element; unknown kind; exclusive create; tampered plan. |
| R, rows | 11 | **Pass:** max over all recorded readouts, null entries skipped, accepted by real lo_core. **Fail:** a missing or all-null row; non-finite values; contract digest; state identity; lo_core refuses a tau or row contract that was not derived from custody. |
| H, handoff | 28 | **Pass:** ACCEPTED under real guard v003; ACCEPTED_PASS_FLAGGED; b1 pass-through; wrapper mode. **Fail:** each reading (NON_LAPSE, TRANSIENT, the unconfirmed transient, anchor stop, BOUND_INSUFFICIENT, UNDECIDABLE_FLAGGED); ρ off by one ulp; threshold with an open blocker; missing reviews; offset without GQ_SIGNED; adapter not in C1; equal mass under 0528; bad receipt; incomplete inventory; wrapper refusal; a bundle missing a state. |
| L, loader | 2 | Real modules load by path and sha; a wrong sha is refused. |

**Dev runs.** `tests/dev_run_*` are earlier iterations, disclosed:
- `112838Z` failed 4 checks on a fixture bug: the attempt result lacked `boundary_state_digest_at_return`;
- `112848Z` and `113036Z` passed with earlier test and handoff bytes.

## Labels

- **TESTED (synthetic):** the suites above.
- **FORMAL:** the r5 layout mapping (driver, binding, stage scripts, controller, checkpoint, cited at each resolver); G1 and G2; the reading classes.
- **UNTESTED:** the writer on a real r5 tree; compute, disk and time per call; launcher011's receipt layout. **Deciding test:** TAIL_REANCHOR's acceptance, after the G1/G2 and review rulings.

## Downstream successors

**This item changes no pinned sha.** So none are required by the item itself. Adoption needs only caller-side inputs and the reviews already ruled:
- the row producer's sha goes into `trusted_source_producers`;
- the Q4 reviews bind `speed_policy`.

C1, the wrapper, guard010/PRELAUNCH004 and G7-SCOPE-1 do not change for this item. These files emit no guard proof and run after the PRELAUNCH fence.

**If root resolves G1/G2 through a v010 successor:**
- the C1 `state_enumerator` pin changes;
- `certificate_policy_review` is re-signed, because it binds `state_enumerator` (wrapper L70-75);
- the G7-SCOPE-1 fence allowlist changes at `sources[19]`, because guard007-lineage L205 requires the enumerator to be allowlisted (brief §1.5);
- compose all of these with the b1 enumerator successor (`4ca7f364`) in one generator run.

The wrapper and the guard owner contract are keyed by the wrapper sha, so they do not change.

The placement ruling (option 1) needs none of these.
