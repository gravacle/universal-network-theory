# acceptance_q2 v002: fixes for the four blocking defects

**Builder.** Claude2 root workflow, 2026-10-19, 12:04Z to 12:25Z (`date -u`). **Reviewer of record:** Claude3 (A134 build table).
**Basis.**
- A134 in the V006 addendum `92b01d76` (checked from bytes); rulings text `56774ba7`.
- The reading points frozen in `FROM_CODEX/0690` (`e45c9a6d`): OPEN-1, OPEN-3, OPEN-4, OPEN-5, OPEN-6 and OPEN-9.
- A115: make the smallest correct change and fail closed.
- The adversarial verification of v001 found 4 blocking defects. v002 fixes those 4 and changes nothing else.

**Status.** Built and synthetic-tested. Not reviewed. Not run on any real call. The v001 files are unchanged, and `README.md` and `HASHES.txt` still describe v001.

## Files (sha256 from bytes)

| File | sha256 | Predecessor |
|---|---|---|
| `replay_inputs_writer_c2v002.py` | `808cfe6a98f8e89a17d8b54e0f8d36b40c8445b121ce2efe2008b82b3a4592d9` | v001 `ffa36e8d` |
| `row_reference_producer_c2v002.py` | `e9190f5e3e852eb540a3300ed98c79bc0a4d55d0525eca41095f3881d2e121b6` | v001 `f483af8e` |
| `acceptance_handoff_c2v002.py` | `ccdbec2b831a1ee5b7feadc68156f7329b9490ee21dc0820589b6760757e5c08` | v001 `02f438e1` |
| `tests/test_acceptance_q2_c2v002.py` | `6aacc1a324d58924324cd56711c389006434a8e8dd1112ebc5773ba85a9a622a` | v001 `b4c9c342` |
| `tests/record_v002_run_20261019T121719Z/TEST_RESULTS.json` | `6440a4c9500d972cbb03a48c576a65709e11bd2a2bd0eb150e4b84d5f4da8349` | (run of record) |

`diffs/V001_TO_V002_*.diff` are unified diffs from each predecessor. Each one was re-applied to its v001 file in scratch and rebuilds the v002 file byte for byte.

## What changed, by defect

**1. The Q4a readout set** (row producer).
- The readout set is now `passes[*].rows[i].speed_km_s` only (OPEN-1).
- `identity.route_a.route_a_rows` is no longer read: driver L1608 marks it "not at call geometry". Nor is `result.rows`, which is the final pass's rows copied (L3532).
- The record now carries `speed_reference_policy = A134_Q4A_OWN_CALL_MAX_ABS_OVER_EVERY_RECORDED_READOUT` (OPEN-9). That is the field Claude3's adapter checks.
- Tests: R01 and R03 are corrected. R12 is probe P1: a route-A row of 99 no longer enters, and v reads 15. R13 is new.

**2. The SRB-ROT target and its inputs** (row producer and handoff).
- **Target.** `final_rotation_target` selects the unique `own_source_state` at `le{final_pass}_rotation`, with stage_kind `le_rotation`, from the v010 inventory (OPEN-3).
  - The rule is the same as srb_rot_adapter_c3v001 L183-200.
  - It adds one check: `passes[-1].pass == final_pass`.
- **Rows input.** `srb_rot_rows_input` writes `S4RC1_SRB_ROT_ROWS_INPUT_C3V001` (OPEN-10/11).
  - It reads only the stage's own records: the `finish.json` that the discovery evidence pins, and that finish's `rotation_base_arrays.npz`.
  - Both files must be inside `<call>/out`. The arrays must equal `passes[-1].rotation_arrays` (driver L3214).
  - `column_R_m`, `v_c_m_s`, `N_min` and `row_columns` follow the V007 SRB_ROT rule (`srb_rot_record_cx1v008_cx3v001` L43-63, `2757847a`). Row radii come from the row contract (custody L120).
- **The adapter call.** The handoff now calls the SRB adapter with the `adapt_call_srb_rot` signature.
  - The arguments are: the call dir, the result, the inventory, the registered bundle, the target's LO state input, the rows input, `root_ruling_refs`, the approved shas and the trusted source producers.
  - The state input now carries `call_result` (adapter L360-362).
- **Reading a PASS.** A PASS is read only together with its SRB_ROT proof. The handoff writes that proof as `SRB_ROT_PROOF.json`, so that root can read it beside the guard (OPEN-2).
- **Tests.** The SRB step runs these real modules:
  - Claude3's real `_adapt` (`e74c6f5e`);
  - the real library `srb_rot`/`field_bound` (`2026f2b6`), on a real synthetic TailState;
  - r14's `apply_flag`, taken from the `f3f9ba7e` bytes.

  Only the I/O and `derive_details` are test doubles. H28 is probe P2; H29-H32 are new.

**3. The readings** (handoff).
- **OPEN-5 (anchor).** `step4_stop_for_root_ruling` is now true at the anchor when any state reads LO_ABOVE_THRESHOLD, or when the call reading is one of v001's stop readings.
  - `step4_stop_basis` records which condition applied.
  - The class reading stays in `reading`.
  - Tests: H33 (probe P3), H34, H37.
- **OPEN-6 (mixed outcomes).** The call reads TRANSIENT when the failures are confined to route-A iterates and every non-iterate state reads PASS. Another iterate may be UNAVAILABLE.
  - Tests: H35 (probe P4) and H36.
  - H13b is unchanged: an unread non-iterate state gives INCOMPLETE.
- **Kept.** An SRB-ROT failure at the anchor still stops step 4. This is conservative, per the verifier's note. Test: H38 (probe P5).

**4. A repeated acceptance pass** (writer and handoff).
- **Writer, when the plan exists.** Once `<call>/TAIL_REPLAY_PLAN.json` exists, the writer writes nothing. It returns REUSED only if every check below holds:
  - the plan is in canonical form;
  - the plan is bound to this call's own result and spec bytes;
  - its ordinals equal the real occurrences;
  - its input set is one `<call>/ACCEPTANCE_INPUTS_*` directory;
  - that directory's WRITER_REPORT reads WRITTEN, carries this plan's pin, has no gaps and the same entry count;
  - every recorded file still matches its sha;
  - every plan ref is in the recorded set;
  - any G1/G2 refs supplied now equal the recorded ones;
  - the recorded G1/G2 pass the digest and re-derivation checks again.

  Otherwise it reads UNAVAILABLE with a typed gap.
- **Writer, when no plan exists.** Each attempt writes a fresh `ACCEPTANCE_INPUTS_C2V002_A<nnn>`.
- **Handoff.** Each pass writes its TailState exports to a fresh `ACCEPTANCE_TAILSTATES_C2V002_A<nnn>`, or to the caller's directory. That directory is created inside the try, so a refusal is recorded in `ACCEPTANCE_RECORD.json`.
- **Tests:**
  - W21, W25-W28;
  - H39 (probe P7): pass 1 has no reviews; pass 2 reads REUSED, the 8 review requests bind the plan it reuses, and the call reads ACCEPTED;
  - H40: a pass before the G1 ruling, then WRITTEN in A002, then ACCEPTED;
  - H41 and H42.

**What did not change:** every other byte (see the diffs). No pinned file changed. These shas were checked from bytes after the build: ef3d3d69, e48cca3c, 7b7400f3, 7289f2ba, 5f1e49e6, 12d36305, 6d59f1d0, b8471197, 6810b7c3, a1dcdea8, 9e3fc109, e74c6f5e, 2026f2b6 and f3f9ba7e, plus all v001 files of this item.

## Tests: 93/93 PASS (34 MUST_PASS, 59 MUST_FAIL)

- **Run of record:** `tests/record_v002_run_20261019T121719Z/`, Python 3.12.14 and numpy 2.3.5, run with `-I -B` and BLAS threads set to 1. The fence refused 0 opens.
- **Dev runs:** all in scratch, on a copy of the item, with the same root-prefix widening the verifier used. No dev run was written to this folder.
- **Negative control (scratch):** the same suite run against the v001 modules.
  - Failed: R03, R05, R06, R12; H01, H07, H08 and H09 (the SRB signature); L01.
  - W01b fails on the directory name only.
  - The W, R and H suites each abort: W at W21's second write (FileExistsError), R at R13 (v001 reads the copied rows), and H at H14 (v001 has no `step4_stop_basis`).

## Caller-side inputs the handoff now needs
- `policy['root_ruling_refs']`: the two A134 pins that srb_rot_adapter_c3v001 requires, `56774ba7` then `bcb6df8e`.
- `policy['approved_certificate_producers']` must include srb_rot_adapter_c3v001 (Q9(a)).
- `trusted_source_producers` must include row producer v002 `e9190f5e`. That module now emits both the row references and the SRB-ROT rows input.
- `pins['srb_adapter']`: `{path, sha256 e74c6f5e…, entry 'adapt_call_srb_rot'}`.

## Remaining notes

**New findings for root**
- **F1. Inclination factor (proof side; FORMAL from code; can change an SRB-ROT verdict, A115(b)).**
  - V007's SRB_ROT producer multiplied the library bound by sin(i_physical)/sin(i_released) before its τ/10 test (`srb_rot_record_cx1v008_cx3v001` L60-61, L106-107).
  - The column-mean stage reads row speeds through both inclinations (`ddo12_lower_entropy_column_mean_root_v004_gal_c2v003` L183).
  - srb_rot_adapter_c3v001 applies the library's `pass_tau_over_10` with no factor (L392-395).
  - Custody fixes i_physical at 66° for every calibration point (custody L96), and the registered released inclination is 64° (driver L440). The factor is therefore sin 66°/sin 64° = 1.0164 at every point.
  - Without it, a bound in (τ_i/10)/1.0164 < b ≤ τ_i/10 reads PASS where V007's rule reads FAIL.
  - The rows input applies no factor, and says so in its `provenance`.
  - **Deciding step:** a ruling by root or Codex1 on whether acceptance applies the factor. Not built here.
- **F2. The LO adapter interface is still v001's proposal.** This is the verifier's non-blocking note. It fails closed, but on real calls it is reachable: every state would read UNAVAILABLE.
  - Claude3's c3v001 LO adapter is the call-level `adapt_call_lo`. It runs `produce_current_lo` itself and needs `execution` on the state input.
  - Before TAIL_REANCHOR's acceptance, one of these is needed:
    - (a) a handoff v003 that hands the state inputs to `adapt_call_lo` and adopts its per-state verdicts;
    - (b) a per-state entry in Claude3's next version.
  - Not built: it decides which layer owns the readings.
- **F3. N1 invalid rows.** If every Picard-pass speed of a row is null, every state's row reference is UNAVAILABLE (Q4a: nothing is substituted), so that call reads INCOMPLETE. This was already true in v001.
  - Whether any of the 29 calls has such a row is UNTESTED.
  - **Deciding test:** each call's `result.invalid_rows`.

**Carried, unchanged**
- The G1/G2 placement ruling (option 1, a subfolder under `<call>/out`).
- An owner for the packet-binding reviews: a Q8-style ruling, one review per state. SRB-ROT also waits on these reviews, because it needs the target's LO state input.
- Two "bitwise ρ" definitions. **Deciding test:** the (a)4 anchor pair compared under the handoff's key set.
- The AnyReview stand-in never exercises the real `_approved` binding.
- Compute and disk are UNTESTED. **Deciding test:** TAIL_REANCHOR's acceptance timing.
- launcher011's receipt layout is UNTESTED.

## Downstream successors
**None required.** No pinned sha changes.
- The writer and the handoff are unpinned.
- Row producer v002 `e9190f5e` is not pinned anywhere yet. It enters `trusted_source_producers` at adoption, as v001's sha would have.
- C1, the wrapper, guard010/PRELAUNCH004, G7-SCOPE-1 and the generator do not change.

## Labels
- **TESTED (synthetic):** the suites above.
- **FORMAL:** the mapping of the rows input onto r5's own outputs (rotation_v005 stage L293-301; driver L3209-3214); the reuse checks; F1.
- **UNTESTED:** every module on a real r5 tree.
