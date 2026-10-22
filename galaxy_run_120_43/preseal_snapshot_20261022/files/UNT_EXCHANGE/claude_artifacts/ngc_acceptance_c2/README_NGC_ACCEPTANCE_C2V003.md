# NGC acceptance completion, c2v003 and its A167 round c2v003a (root build; V006 A162)

**Status.** Root build (Claude2 workflow). Synthetic tests only. Nothing here is adopted until root rules on it and Claude3 reviews the c2v003 round. No NGC per-state number, rho, SRB-ROT bound or contract review exists for a real call, and none was computed.

**Two rounds, one build.**
- **c2v003** implements V006 A162 items 1-6 as commissioned (the spec of record), on top of A153 and A155 with E_A155_1. Its handoff pins the reviewed adapter c2v002 (`ce33b526`).
- **c2v003a** applies **A167** (root, 19:23:15Z, written after this build was commissioned). A167 changes deliverable 6 ("The NGC acceptance S2 interface (A162) pins the c3v003 schema and shas") and reverses the C4b reading the adapter c2v002 enforces (honest seed and J0 states would read `NGC_GAMMA_ROUTE_BITS_DIFFER`). The c2v003 files were already written by exclusive create, so the A167 change is a new adapter `c2v003a` and a new handoff `c2v003a`; the reader, S5 tool, contract and builder are the c2v003 files, unchanged.
- **Proposed handoff of record: `ngc_acceptance_handoff_c2v003a.py` (`7c54fd6f`), record schema `UNT_NGC_LO_ACCEPTANCE_RECORD_C2V003A`.** Values writer v004 (A159) would pin that schema and sha. Root rules.

## Spec of record (section sha256 from bytes, `## Axxx` line to the next `## ` line)

| entry | section sha256 | used for |
|---|---|---|
| A153 | `aa079db7cc07c2973075514a5d359ff3941b69f414687f12827cc06dab94c51e` | the per-state quantity, S1-S13 (pinned in the adapters) |
| A155 (+E_A155_1, frozen) | `ed6b144b66837069c4febf81a4feaf11c160f9be5f26d914d4c40041b60f3c9d` | rule TI_B_SCALE_R_V001, theta hex, PASS meaning (pinned in the adapters and the builder) |
| A162 | `49ef90da0bf2de4237c241aef2dd275ca51f794513c72357d362896dc1fa902d` | items 1-6 (pinned in the contract builder) |
| A167 | `96cb1404cd63b11768bcc546eada8c47b7c46cc8bb3fbb55d74765ad4dd52ae3` | the c2v003a round |
| A164 | `b904075da454ba93f8fc756e0e88662a8cb1961772dfdbf75e2f453ba1a3104d` | the three DDO Q4 reviews are approved, so the NGC contract's S10 review may start (A162 item 3) |

The V006 file kept growing during the build (A163-A174 appended; file sha `8536ab73` at README time). The A153, A155 and A162 sections were re-hashed after the record runs and are unchanged. A168-A174 do not touch NGC acceptance; A173's "every root-written record carries `schema`" holds for every record written here.

## The NGC acceptance chain, end to end

Per NGC step-5 call, after the driver writes `out/finish.json`:

1. **FINISHED receipt** (root; the c2v002 gate, unchanged).
2. **Sidecar enumeration** (A162 item 1; reader `enumerate_sidecar`): the call's own route-A sidecar, read in the controller's format. For every completed iteration n = 0..a it lists the begun state (`current_begin_inferred_from_completion`) and the monitor-consumed next state (`next_built_and_monitor_consumed`). The last begun state must be the boundary state and the manifest state.
3. **S5 for the iterates** (A162 item 2; S5 `rebuild_admit`): each non-accepted iterate digest is rebuilt from its own roster through the pinned library `build`, and admitted only on TailState digest equality. Wall time is recorded (U4).
4. **Iterate list** (reader `write_iterate_list`): `UNT_NGC_ROUTE_A_ITERATE_STATES_C2V001`, the enumerator's input. Each source digest is established, not asserted: the accepted state's comes from its manifest record (digest re-checked from bytes), and every other state's from its admitted S5 rebuild.
5. **Inventory** (enumerator c2v001, unchanged): Q5 classes ACCEPTED_ROUTE_A / INHERITED_ROUTE_A / ROUTE_B_STAGE / ROUTE_A_PRE_ACCEPTANCE_ITERATE.
6. **S5 for the route-B states**, then a **state input per non-accepted state** (S5 `export_state_input`). The recorded roster digest (`finish.json uv_tail.roster_digest`) must equal the recipe roster's digest before anything is built.
   - Steps 2-6 are one call: handoff `prepare_acceptance_inputs` returns the policy fragment `{route_a_iterates, rebuild_exports}` plus every admission pin.
7. **Handoff `accept_call_ngc`** (REGISTERED registry only):
   1. receipt gate;
   2. **execution facts** (A162 item 4); anything not established, or established and disqualifying, refuses here. The call reads INCOMPLETE, and no inventory or LO is computed;
   3. **iterate list verified** against a fresh sidecar enumeration: no iterate dropped, added, reordered or relabelled, and sources bound to their admissions;
   4. inventory;
   5. **every S5 export verified**: S5 producer pin, an ADMITTED admission for this call and state, and the admitted files are the input's files. An export that fails is dropped with blocker `REBUILD_EXPORT_REFUSED`, and that state reads UNAVAILABLE;
   6. the accepted state's input from the call's own ROUTE_A_TAIL_MANIFEST;
   7. **S2 pins** (A162 item 6, A167); PENDING reads UNAVAILABLE;
   8. **the pinned contract** (A162 item 3);
   9. **the adapter** (c2v003a; A153 S1-S13, the A155 ratio-form gate, C4b per A167);
   10. adoption: every per-state record is re-read and guarded;
   11. the A134 Q5 / 0690 readings;
   12. **SRB-ROT, report-only** (A162 item 5), written to `SRB_ROT_REPORT.json`. It never touches the reading.
8. **member_valid** (values writer v004, A159, not built here): it reads ACCEPTED or LO_UNCERTIFIED_TRANSIENT from this handoff's record.

**NGC acceptance = the A153/A155 LO gate + custody + execution facts** (A162). SRB-ROT is reported beside it and never gates.

## A162 items 1-6: how each is built

| item | where | built as |
|---|---|---|
| 1 route-A iterate list | `ngc_route_a_iterates_c2v003.py` | **Format, from the driver code and the code it pins:**<br>- driver cx3r008 L8628 (`--uv-tail-sidecar-directory <route_a stage>/uv_tail_sidecar`), L8693 (route_a_record), L8706 (manifest digest);<br>- route-A controller `c5bdd055` L29-31, L329-363, L470-565 (SIDECAR_IDENTITY, iteration_NNNN payloads, elements_NNNN rosters, finish_NNN);<br>- NGC manifest writer `b9247b1a` L98-148.<br>**Every file is read from the call's own bytes:**<br>- the sidecar finish pin and every listed file's sha;<br>- iterations and elements exactly 0..a with no gap;<br>- the identity self-sha and its config, request and checkpoint identity;<br>- per-iteration payload, summary and record agreement;<br>- element digests in the controller's `_array_digest` form;<br>- the last begun state = the boundary = the manifest digest. |
| 2 S5 rebuild export | `ngc_s5_rebuild_export_c2v003.py` | **Rebuild:**<br>- a roster recipe in root's approved list returns `{roster, build args}` from the call's own outputs;<br>- `roster.digest()` must equal the recorded roster digest whenever one is recorded;<br>- the state is built by the pinned library `build` (v002 `2026f2b6`, provider `d6c55b55`), never by the recipe.<br>**Admission:**<br>- ADMITTED only if the rebuilt TailState digest equals the recorded `state_digest` (`S5_REBUILD_DIGEST_MISMATCH` otherwise);<br>- the exported npz and JSON are re-loaded with `from_arrays(expected_digest)` before the admission is written;<br>- timing per state (recipe, build, export, total): U4;<br>- every refusal still writes an admission (admitted false, with its code). |
| 3 NGC row contract | `ngc_row_contract_c2v003.py` → `NGC_ROW_CONTRACT_C2V001.json` | **Source:** manifest `a2936517` (the driver's NGC_DATA path), checked for target-free shape (schema, the 5 emitted columns, 43 rows, ids NGC3198-Q01..Q43 in order, kpc).<br>**Fields:**<br>- R_i = `float(Rad_text) * 3.085677581491367e19` (driver L5215, KPC_M L183), with `manifest_radius_scale` 1.0;<br>- rule id `TI_B_SCALE_R_V001`, theta hex `0x1.ce9660bc22098p-29`, c hex `0x1.1de784a000000p+28`, binding null;<br>- **no velocity, no t_i, no sigma.**<br>**Checks:** the adapter's own S8 check on the REGISTERED registry reads BOUND.<br>**sha256 `80cbf2f5be2e9f22a0b751376dcde3e7e779bd89f531a8ffe9d654616490fe32`**, pinned in both handoffs. Build record `39ea4497`. |
| 4 execution facts | handoff `execution_block` | `{fresh_call, resumed, retried, route_a_completed_normally, run_root}`, read by the DDO handoff c2v004 EXECUTION_RULE of record (quoted verbatim in the code), mapped onto the NGC records (`NGC_EXECUTION_RULE`). Acceptance needs fresh, not resumed, not retried and completed normally. A fact that is not established (None) refuses. |
| 5 SRB-ROT for NGC | handoff `srb_rot_report` | **Computation, exactly A152 W-1 as the values writer does it:**<br>- `srb_rot(S, C, rows)['bound_km_s']`;<br>- S = the `le{final_pass}_rotation` TailState from its verified S5 export (digest = the stage finish, `record.eps_certificate` = the point pin);<br>- C = the point certificate, field `eps`, with W-4 checks;<br>- rows = `rotation_rows` (`67fddd24` L171-193) on the call's own rotation arrays and column-mean support radii;<br>- tau inert; `ratio_to_tau` and `pass_tau_over_10` discarded.<br>**Report-only:** labelled **`report-only: no registered NGC tau`**, `gates: false`, values only in `SRB_ROT_REPORT.json`. |
| 6 S2 rho | handoff `S2_PINS`; adapter c2v003a constants | `S2_PINS = {rho_producer_sha256: PENDING, slot_proof_producer_sha256: PENDING}`.<br>PENDING gives blocker `S2_RHO_PINS_PENDING` and empty approved lists, so every state reads `NGC_RHO_RECORD_MISMATCH`. Policy cannot supply S2 approvals, and under REGISTERED the pins must be the module constants.<br>c2v003a: the c3v003 schema strings `UNT_NGC_POINT_LO_SLOT_PROOF_C3V003`, `UNT_NGC_POINT_RHO_NUMERICAL_C3V003` and `UNT_NGC_POINT_RHO_IDENTITY_C3V003` (A167). |

**c2v003a delta (A167), and only it:**
- C4b compares the state's `gamma_eff` with the spec route s·(ge·EB) bit for bit, exactly. The θ route (s·ge)·EB is recorded as `theta_route_bits_equal_diagnostic`.
- The S2 schema strings move to `*_C3V003`.
- The state and call record schemas move to C2V003A.
- Every other adapter line is c2v002's (the diff is in the c2v003a docstring head). The handoff c2v003a differs from c2v003 only in the adapter pin, the record schemas, loader names and the S2 message.

## Files (sha256 from bytes)

| file | sha256 | role |
|---|---|---|
| `ngc_route_a_iterates_c2v003.py` | `9335ee4212719944b6dd45369161de16891ec0ed5dbdd97fed36d68d0b993bdc` | item 1 reader; pins S5 `3611e993` |
| `ngc_s5_rebuild_export_c2v003.py` | `3611e9933b57363ffab8dbdbaae67960751e59d3d34b219f1777e8e2f2a54100` | item 2 S5 tool |
| `ngc_row_contract_c2v003.py` | `f2f54d79cbdbda89113121e1c2068d42f0c8d8460b5ccff963d015ac0f9e73a2` | item 3 builder (self-check pins adapter c2v002) |
| `NGC_ROW_CONTRACT_C2V001.json` | `80cbf2f5be2e9f22a0b751376dcde3e7e779bd89f531a8ffe9d654616490fe32` | item 3, the one contract |
| `NGC_ROW_CONTRACT_C2V001_BUILD_RECORD_C2V003.json` | `39ea44979bc08dbf7b6e001390470bd1da897220f144c5281d8e32975f4def10` | builder record (sources, adapter check BOUND) |
| `ngc_acceptance_handoff_c2v003.py` | `141a87d4c834cd96be9487b9803bac6f7a234b74d9527d1461eb9d09ea6460d4` | items 1-6; pins adapter c2v002 |
| `test_ngc_acceptance_c2v003.py` | `efffa548b7e302a25b110ec0cd8c2e74c32eb99d64a26c0552d51c777d3fe715` | 34 MUST_PASS, 41 MUST_FAIL |
| `mutation_ngc_acceptance_c2v003.py` | `16034f229aafd1886af0a02389e7fab2ce0c8875dd5e758c2c41d4965860f52f` | 72 mutants plus a control |
| `ngc_lo_state_adapter_c2v003a.py` | `9c4b6dfc591cfd5c372416beb936d5d903540e5fc41e4a327b428d7ba5001eb2` | A167 adapter successor |
| `ngc_acceptance_handoff_c2v003a.py` | `7c54fd6fcc3defbc6728a35fd5125eb0d2fba23b735a38af6ac8de2094c04427` | **proposed handoff of record**; pins adapter `9c4b6dfc`, enumerator `607b7f66`, reader `9335ee42`, S5 `3611e993`, contract `80cbf2f5` |
| `test_ngc_acceptance_c2v003a.py` | `e452cec252aeb54c64723c5fc324409bb6e308b0b27f01f3bd43cebeab3a11c0` | 35 MUST_PASS, 42 MUST_FAIL |
| `mutation_ngc_acceptance_c2v003a.py` | `12e98aac4f5868a1b0d8339db42d5b5db792ec17af42ccd819cc3c1ab647eac2` | 75 mutants plus a control |

**Unchanged pins:**
- enumerator c2v001 `607b7f66` and adapter c2v002 `ce33b526` (c2v003 only);
- library v002 `2026f2b6` and provider `d6c55b55`;
- driver cx3r008 `577f8c94`;
- row producer `67fddd24`;
- manifest `a2936517`;
- launch pin `07745bbf` (hash-checked only, never parsed).

`HASHES_C2V003.txt` lists every file of both rounds, including the synthetic trees.

## Tests

**Record runs** under `python3 -I -B` 3.12.14, with no ART patch (`art_patched_for_dev_run` false):

| round | run 1 | run 2 | counts |
|---|---|---|---|
| c2v003 | `synthetic_c2v003/record_run_1/SUITE_RESULTS_C2V003.json` `2233ddca4e878e2e236c874b927c8aebd92283835ed94e6ca43e1e3764863d8a` | `record_run_2/…` `08b7f36d1f177479928ce53dab61f09a7bdeece63109aed1601c0af35812e9ae` | 34/34 MUST_PASS, 41/41 MUST_FAIL |
| c2v003a | `synthetic_c2v003a/record_run_1/SUITE_RESULTS_C2V003A.json` `997083485f1aef7a4eaa9da7638452ce29d152f06cd0ac029f0109179f9b5be5` | `record_run_2/…` `62d2de4f3234deff8ecf5b6416e47af6916b786cff9b1cf34e18c07f4b3685ea` | 35/35 MUST_PASS, 42/42 MUST_FAIL |

**Run-to-run agreement.**
- Ids and ok flags are identical between the two runs of each round.
- Details are identical once two things are normalized: the run-directory name, and the hex digests that embed it. The synthetic configs pin certificate files by path, so state digests and file shas differ by run directory.

**Fixture.**
- Every synthetic state is built by the pinned library's real `build` from a synthetic roster (a test-only recipe file). S5 can therefore genuinely rebuild them.
- Each call has 4 consumed states:
  - A, the accepted route-A state (iteration 1);
  - B, the route-B `le3_rotation`;
  - I, iterate 0;
  - N, the monitor-consumed next state of the accepted iteration.
- The route-A sidecar is written in the controller's format, and the driver layout is followed (`out/stages/NN_name`, ctx records, start.json, finish.json).
- Calibration is through the roster scale, so state A's largest g is 0.001. t_i is never computed.

**Ported.** Every c2v002 test, P01-P24 and F01-F33, is ported with the same intent. Two changes:
- counts move from 3 states to 4, because N is now enumerated;
- the handoff tests run on reader + S5 inputs.

In c2v003a, F06 and P20 follow A167:
- F06: a state 1 ulp off the spec route, and states built at the θ route, are both refused;
- P20: C4b is recorded with the rule text.

**A162 / A167 additions:**

| item | MUST_PASS | MUST_FAIL |
|---|---|---|
| 1 reader | **P25** enumeration (4 occurrences, accepted last, targets I and N, finish index 0).<br>**P26** the list from S5 admissions: enumerator complete, classes right, sources established. | **F34** sidecar gaps refused: gap, file bytes, extra iteration, element digest, identity sha, record differs, boundary, outside the route-A stage dir, outcome, finish sha, last begun state ≠ boundary. Through the handoff, INCOMPLETE with no adapter run.<br>**F35** forged list (dropped iterate, wrong source, other producer); the handoff reads INCOMPLETE.<br>**F36** no list without an ADMITTED, state-bound admission per iterate. |
| 2 S5 | **P27** B, I and N rebuilt from own rosters, digest-equal, timed; S5 exports pass the adapter (all PASS).<br>**P34** the accepted state is never rebuilt; one verified export per other state. | **F37** roster not the recorded one; recipe not approved; target = accepted; recipe raises; unreproducible recorded state (`S5_REBUILD_DIGEST_MISMATCH`, export refused); export identity mismatch; export without admission; at the handoff, a non-S5 export and a swapped admission are dropped, giving INCOMPLETE. |
| 3 contract | **P29** the real contract: pinned sha from bytes, a2936517 ids and order, R bits, rule/θ/c hex, no velocity/t_i/sigma tokens, adapter BOUND, builder reproduces it. | **F38** t_km_s, sigma or velocity key; radius moved; order reversed; another contract at the handoff (REGISTERED and policy); builder refuses a velocity column, other order, other unit, 42 rows, sha mismatch. |
| 4 execution | **P30** facts recorded from own records and carried in the summary.<br>**P28** chain end to end, ACCEPTED. | **F39** retries 1; two route_a records; start-iteration 1; a resume flag; checkpoint-mode resume; exit 1; not converged; `converged_finite_fixed_point` = 1 (not True); admitted route-A lane; COMPLETED_INVALID; no start.json; a result_path elsewhere; argv missing; a reloaded iteration; sidecar finish_001; spec admit. Each refuses before the inventory. |
| 5 SRB-ROT | **P31** equals an independent oracle (1e-12), label exact, gates false, no value in the record or summary.<br>**P32** a 1e12-larger bound and a missing certificate both leave ACCEPTED. | **F40** other point's certificate, bad producer, the state not run with that certificate, anchor role: each UNAVAILABLE with the reading unchanged. The report never holds a tau ratio or pass flag. |
| 6 S2 | **P33** module S2 = PENDING; pinned (synthetic) producers are accepted by sha. | **F41** PENDING reads UNAVAILABLE with the blocker; another rho producer; policy S2 approvals; REGISTERED with non-constant pins; malformed pins. |
| A167 (c2v003a) | **P35** at point 1 (θ route ≠ spec route in the last bit), honest states read PASS; θ bits are a diagnostic. | **F42** c3v001-schema slot proof and rho records are refused, and the constants are the `*_C3V003` strings. |

**Mutation.** Each mutant is one change in a fresh `python3 -I -B` process, with sibling pins re-filled from bytes so that no mutant dies of a stale pin.

| round | results | control | killed | killed by the intended test |
|---|---|---|---|---|
| c2v003 | `synthetic_c2v003/mutation_c2v003/MUTATION_RESULTS_C2V003.json` `bd653c74d839865796a0ba5ff85f94ac31b97bf27ebc324e41b4d555f7e38a64` | clean | 72/72 | 72/72 |
| c2v003a | `synthetic_c2v003a/mutation_c2v003a/MUTATION_RESULTS_C2V003A.json` `824a8ce4910f5297e8f42bbbcfc6b8cba45d741704726fd464a58181753eea93` | clean | 75/75 | 75/75 |

Mutant coverage:
- **M01-M43:** the c2v002 mutants, carried.
- **M44-M50:** reader. Monitor-next dropped, file sha, iteration range, identity sha, list occurrence equality, admission state binding, list source check.
- **M51-M56:** S5. Digest equality, recorded roster, recipe approval, accepted rebuilt, export verification, export identity.
- **M57-M60:** execution. Refusal off, retries ignored, start-iteration ignored, `is True` relaxed.
- **M61-M63:** SRB-ROT. Unavailable gates, bound gates, label changed.
- **M64-M65:** S2. PENDING ignored, REGISTERED pin check off.
- **M66-M68, M72:** contract. Policy check, builder radius rule, builder column check, REGISTERED check.
- **M69-M70:** handoff. Export verification and list verification off.
- **M71:** reader. Last begun state ≠ boundary.
- **M73-M75 (c2v003a):** θ route substituted, all three routes required (the c2v002 behaviour), schema strings back to c3v001.
- One candidate mutant was dropped as untestable: S5's post-write reload check cannot fail between its own write and read. It is disclosed here and not counted.

## Builder choices (disclosed; each is root's to overrule)

1. **The monitor-consumed next state of the accepted iteration is enumerated.** The controller builds it at the accepted completion and M_T reads it (L486). It is classed ROUTE_A_PRE_ACCEPTANCE_ITERATE, the enumerator c2v001's role for it. This is the A48-conservative reading of ALL_CONSUMED_STATES; omitting it would gate one state fewer.
2. **Iterate source digests are established by S5, not asserted.** The sidecar does not record an iterate's roster digest. The accepted state's comes from its manifest record, and every other state's from its admitted rebuild (the TailState digest covers the record's `roster_digest`).
3. **Execution facts: established-but-disqualifying refuses too.** The required values are fresh / not resumed / not retried / completed normally, following A48 and the DDO producer. NGC-specific conjuncts were added from the call's own records:
   - out/start.json binds the same driver and spec;
   - finish.result_path is this out/result.json;
   - the sidecar finish is finish_000, with no reloaded iteration;
   - `identity.route_a.mode` is computed (driver L5083 / L8644: a v011 step-5 spec produces route A in-call).

   A refusal stops before the inventory, so no LO is computed (A162: "Anything not established refuses").
4. **S2 pins and the contract are code pins, not policy.** Policy supplies only the per-point slot-proof and rho-producer files, the row-policy review and its trusted sha, the adapter approval list, the EPS certificate and the high-Q-inf flag. Under REGISTERED, S2, the contract, the reader pin and the S5 pin must all be the module constants.
5. **The handoff re-derives the sidecar enumeration** and re-verifies each export's admission. The enumerator's producer-sha check alone would let a mislabelled list drop an iterate.
6. **The roster recipe is root-approved at run time** (an argument), not a code pin. Digest equality is the proof, and recipe approval is provenance only: a recipe cannot make a different state pass.
7. **SRB-ROT is computed whenever the inventory is complete**, even if the LO reading is INCOMPLETE. It is reported for diagnosis and never read.
8. **c2v003a infers the c3v003 schema strings from A167's text** ("The schema strings move to `*_C3V003`"). Claude3's c3v003 files were not opened (they are not a named path). A mismatch fails closed.
9. The c2v002 verifier NOTE is carried unchanged, as A155 rules it: a row set whose only rows are zero-speed reads PASS with G = 0.

## Open interfaces and UNTESTED items (each with its deciding test)

- **Real roster recipes: OPEN.** None exists. Until root approves recipes, every non-accepted state of a real call reads `NGC_STATE_INPUT_UNAVAILABLE`, the call reads INCOMPLETE, and SRB-ROT reads UNAVAILABLE. That is UNTESTED, not a null.
  - **Route-A recipe:** the manifest writer's rebuild at iteration n: `from_prepared` with the reviewed prep and the driver's prep patches, the sidecar element rosters 0..n-1, and the I1-T gas of iteration n from the checkpoint. The monitor-next state of the last iteration needs gas_{a+1} = (1−r)·gas_a + r·updated_a, and where updated_a is recorded is not yet read.
  - **Route-B recipes:** the route-B binding's (`aee7af12`) per-kind roster:
    - the fs kinds: stars plus body gas;
    - the rfs/le kinds: stars plus the feedback rotation rings;
    - offset: the Δ roster;

    each with the stage's own i1t and kept region.
  - Deciding test: the first real call (and U4).
- **U4, rebuild time.** It is recorded per state in each admission. Deciding test: the first call.
- **S2: PENDING.** Root pins Claude3's NGC rho c3v003 producer and slot-proof shas after its review (A167 R2-R4), in a handoff successor. Whether c3v003's record fields beyond the schema strings match the adapter's S2 checks is UNTESTED. Deciding test: c3v003 records through `check_slot_proof` at that pin.
- **S10 contract review: OPEN.** Codex1, single pass, bound to `80cbf2f5…` (A162 item 3; A164 clears the "after the three DDO Q4 reviews" condition).
  - Interface note: the adapter requires review schema `UNT_NGC_LO_ROW_POLICY_REVIEW_C2V002`, `verdict` APPROVED, and `row_contract_sha256` = the contract sha. Codex1's DDO reviews used `CODEX1_Q4_ROW_POLICY_REVIEW_V001`, which this adapter refuses (`ROW_REFERENCE_POLICY_NOT_REVIEWED`). The review should carry the NGC schema, or root rules.
- **U-b3, whether S7 radii equal the contract bits.** The contract uses the driver's own query-row arithmetic. Deciding test: the first acceptance, through the adapter's bitwise S7 check (a mismatch reads NGC_ROW_CONTRACT_MISMATCH, never a PASS).
- **U-b1** (NGC LO size), **U-b2** (the R·G′ = 1 remainder) and **U1** (the omitted tail through the source) are unchanged from A155.
- **Execution facts on real trees.** The rule is FORMAL from driver bytes and TESTED synthetically. Deciding test: the first call's own records.
- **The c2v003 handoff pins adapter c2v002,** whose C4b A167 reverses. Do not adopt it as the handoff of record if A167 stands; c2v003a is the A167-consistent one.

## Conduct and deviations

**Read, by named path:**
- V006: the A153, A155 and A162 sections and headings; A152 W-1; A156-A161 as context; and, as they appeared, A163-A174 headings with A164 and A167 in full.
- The c2v001 and c2v002 files in this folder.
- The driver cx3r008 at the cited lines (sidecar argv, route_a_record, manifest stage, ctx records, run/finish, the NGC route-A mode, final_rows_check, stage naming).
- The library v002 and the Jn provider.
- The DDO handoff c2v004 (execution_block, EXECUTION_RULE) and row producer c2v003 (`rotation_rows`, named by V006 A152).
- Values writer v003a (W-1/W-4 functions; named by V006 A152/A159).
- The manifest `a2936517`, for ids and radii only.

**Opened beyond the brief's list (disclosed):**
- The route-A controller `c5bdd055`, the NGC manifest writer `b9247b1a` and the route-B binding `aee7af12`. All three are pinned by path and sha inside the driver code, and they define the sidecar format, the rebuild path and the route-B rosters.
- The c2v002 verifier notes. Their path was not named, so they were read from root's own workflow scratch: `c2v002_reverify/probe_v002_out.json` `30c7c41b`.

**Not opened:**
- no run tree, nothing under `~/.codex`, `c5h_hull_c2` or `UVT_*`;
- no NGC3198 target, observed, sigma or slots file;
- the DDO `consumed_states_cx2v005` (its fresh_scope rule is taken from the c2v004 handoff's quoted EXECUTION_RULE);
- Claude3's NGC rho files.

**Deviations:**
1. **A167 applied in a round `a`,** beyond the spec of record A162. A167 redirects item 6 and reverses C4b.
2. **Dev in scratchpad.** Final files were written here by exclusive create from the staged bytes (shas identical). No earlier file was edited.
3. **Tests read real files.** The tests read the real V006 sections, the text of record, manifest `a2936517` and the built contract.
4. **Synthetic fixtures name registered shas as strings.** The synthetic certificates name the real EPS producer sha `8972822b` as a string, and the fabricated public-entry calls name the driver sha.
5. **Synthetic rosters are built through the real pinned library** (the `build` path), never through registered data.
