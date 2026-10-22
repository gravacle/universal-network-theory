# COMPARE_V007_IMPL_V001: the V007 tail-scheme compare (Claude2 root lane)

`claude_artifacts/v007_compare_c2/`, 2026-10-18.  Not sealed.  Shas are in `HASHES.txt` (from bytes).

## Status

- **TESTED:**
  - The decision code passes **69/69** branch and clause tests (`out/tests_V002/TEST_SUMMARY.json`).
  - The field readers match real driver and controller output (`out/REAL_RECORD_CHECK.json`, all 12 expectations met).
- **UNTESTED:** the compare on real V007 records. No v010 run, gate record or RO1 record exists yet. The field names that v010, RO1 and the gate tools must produce are fixed in `FIELDS.md`.
- **Pins verified from bytes on every start, REFUSED on mismatch:**
  - V004 addendum 487d4449;
  - V005 prereg dbddc02c and its compare 49404bc4 (loaded pinned; supplies adapt_result, packet_checks, diffs and canon);
  - V006 R1 807fc5bf (G5/G6 grids);
  - draft R1 c691cab6;
  - C5H spec 60b46130 (RA4 block, RA1 numerics);
  - the R3 results C2R3 1f6b32a4, C3R3 c9c802f4 and C4R3 aac01962.
- **Not pinned:** A47 is cited by name (V005 addendum, open file). `V007_PREREG_SHA256 = None` stays PENDING until the seal sets it, so until then every run is TEST mode.

## Modes

| mode | what it writes | use |
|---|---|---|
| full | `KMAX_TAIL_COMPARISON.json` + table | the decision |
| `--validity-only --case X` | `VALIDITY_ONLY.json`: booleans and reason codes, and **no number of any kind** (asserted) | A47 I3. The pre-seal check on C5H uses this mode |
| `--gates-only` | `GATES_ONLY.json`: gate statuses, codes and cross-reference booleans; no record numbers | RA13 |
| `--write-field-contract FIELDS.md` | the field contract | producers |

**Route-A mode (A47 I4)** is one declared parameter:
- `parallel8` (the default): every T-case uses route_a.column_workers 8, and C4T-D5 is byte-equal to C5H except composite_grid_spec and uv_tail.
- `serial_with_exemption`: column_workers 1, and the RA1 exemption returns.

The value is read from the prereg `route_a_mode`, the case-block `route_a_mode` or `--route-a-mode`. Any disagreement between them is REFUSED.

## Clause → code (`kmax_tail_compare_c2v007.py`, line numbers at sha 0621b336)

| clause | implementation |
|---|---|
| V005 V1 (status, valid, 12 finite rows) + finish/receipt custody | `case_validity` L588-612 |
| V005 V2 (final change ≤ 0.0125) | L613-614 |
| V005 V3 against the registered V007 case block | L615-712. Anchor physical/coefficients/picard L622-634; RA4 block L635; grid/truncation L637-642; **A47 I5** max_iterations 32 L644; **A47 I4** column_workers L646-648; drivers L649-653; case-block pointers L664-671; **RA1** C4T-D5 vs C5H numerics L672-678; route_a_outcome L679-691; uv_tail record L692-703; **RA5** RO1 record L704-710 |
| V005 V4/V5 (packet) | L713-717 (packet_checks of the pinned V005 compare, in `read_all` L1901) |
| V005 V6 (R-PAIR Picard reruns admit their own prefix) | L719-724 |
| I1T coverage per case | L725-730; gate `g_I1T` L1043 |
| **RA4** BRACKET_HULL_MISS reading | `classify_failure` L373-397; next step `next_steps_for_case` L739 (RA4 text) |
| RA5 (c) / A42 readout refusal reading | L398-414 |
| **RA5** RO1 record (recorded, not an invalidity) | `check_ro1_record` L510; RA5 (a), RO1 in an identity run → NO_RUN, L1488-1494; gate B0_RO1 `g_B0_RO1` L915 |
| R1 MT_monitor / TAIL_SOURCE_UNDERCONVERGED flag; IA6 admissibility | `check_uvt_record` L469 |
| R1 noise_allowance E_i | `picard_noise` L1217 |
| R1 route_a_noise E^A_i | `route_a_noise` L1242 (route-A record, else EA replay record) |
| R1 decidable_iff and R-PAIR branch | `pair_noise` L1256 |
| R1 R-PAIR once, UNDECIDABLE_AT_ITERATION_FLOOR | `evaluate_pair_test` L1390-1445 |
| **T1** = V005 shape_pass AND RA6 per-row, with TINY only inside RA6 (**A47 I2**); FLOOR_LIKE wording (RA6) | `t1_test` L1287-1318 |
| T1_H ≤ ½ decidable; T1_S max ≤ 2; T2 (RA1) ≤ ¼ decidable, read only after T2I (RA3); T2c (RA2) ≤ ½ pass/fail; T3 ≤ ¼ per pair, decidable | L1528-1537 |
| RB_FP (R1 L9) | `rb_fp` L1326 |
| SR_K, SR term, SOURCE_QUADRATURE_MATERIAL (R1 L6) | `sr_k` L1366 |
| u_i | `carried_uncertainty` L1654 |
| D_m4 and the RA10 harmonics (reported, not deciding); LO_NGC status | `reported_items` L1667 |
| Outcome 1 NO_RUN | L1488-1495 |
| Outcome 2 INCOMPLETE (**A47 I1**) | L1496-1511 |
| Outcome 3 NUMERICS_UNCERTIFIED / NON_LAPSE_TAIL_MATERIAL (RA7 GQ) | L1512-1519 |
| Outcomes 4-16, first-applicable, three-valued | L1558-1624 |
| Gate records: B0, B0prime_DRY/RERUN, B0_FA, B1, **B1_OFF (A47 I6)**, B2, B3, B0_RO1 (RA5), B0_N3 (RA8), EPS, DOUBLING, GQ (RA7), LO, LO_NGC, I1T, T2I (RA3), SRB_ROT, RB_FP, SR_K, EA, MT, HARMONICS (RA10), FLAG_RULINGS | `g_*` L810-1160; `evaluate_gate` L1165 |
| **A47 I3** blinding | `blinded_case` L1685, `blinded_gate` L1700, `assert_no_numbers` L1709; CLI L2020-2056 |
| RA12 pins / RA13 gates on real records | `build_context` L256; `--gates-only` L2044 |

## Outcome order as implemented

| position | outcome | condition |
|---|---|---|
| 1 | **NO_RUN** | A gate in {B0, B0prime_DRY, B0prime_RERUN, B0_FA, B1, B1_OFF, B2, B3, B0_RO1, B0_N3} FAILs; or any gate record is defective; or RO1 fires in Z2, Z2-OFF or B0prime_RERUN. A B2/B3 failure is subtyped IMPLEMENTATION_DEFECT_OF_GATE |
| 2 | **INCOMPLETE** (A47 I1) | Any registered case (T-runs, C5H) or identity-gate run (Z2, Z2-OFF, B0prime_RERUN) is invalid or missing (named, with its reading, e.g. BRACKET_HULL_MISS, and next step); or a required gate record is missing. **No T-test is read** |
| 3 | NUMERICS_UNCERTIFIED / NON_LAPSE_TAIL_MATERIAL | EPS, DOUBLING or GQ fails; or LO fails. T-tests are not read |
| 4-16 | UNDECIDABLE_ROUTE_A_TAIL, UNDECIDABLE_AT_ITERATION_FLOOR, IMPLEMENTATION_DEFECT, SOURCE_RULE_MATERIAL, KBIG_NOT_CONVERGED, BOUND_INSUFFICIENT, FLOOR_LIKE, NOT_UV_RESIDUAL, SOURCE_REPRESENTATION_K_DEPENDENT, HIGHER_K_DISAGREEMENT, SHAPE_DISAGREEMENT, FLAG_PENDING_RULING, ADOPT_TAIL | The R1 order, applied first-applicable |

If a condition earlier in the order cannot be resolved (an R-PAIR still pending, E^A unavailable, or T2 not read), the reading is INCOMPLETE (subtype UNRESOLVED), never a later outcome and never a pass.

## Tests (69/69 pass; `tests_kmax_tail_compare_c2v007.py`; real R3 rows as base, synthetic runs otherwise; no observation read)

**One branch test per outcome:**
- ADOPT_TAIL.
- NO_RUN, twice: B3 FAIL, which is the gate's IMPLEMENTATION_DEFECT; and B1_OFF FAIL.
- INCOMPLETE, three times: a missing case, a missing B1_OFF record, and a missing Z2-OFF run.
- NUMERICS_UNCERTIFIED, twice: EPS and GQ.
- NON_LAPSE_TAIL_MATERIAL.
- UNDECIDABLE_ROUTE_A_TAIL.
- UNDECIDABLE_AT_ITERATION_FLOOR: neither PASS nor FAIL.
- R-PAIR: pending, Picard-branch decided, branch mismatch, and route-A branch selection.
- IMPLEMENTATION_DEFECT, SOURCE_RULE_MATERIAL, KBIG_NOT_CONVERGED.
- BOUND_INSUFFICIENT, twice: RB_FP and SRB_ROT.
- FLOOR_LIKE ahead of the T1-fail split.
- NOT_UV_RESIDUAL, SOURCE_REPRESENTATION_K_DEPENDENT, HIGHER_K_DISAGREEMENT, SHAPE_DISAGREEMENT.
- FLAG_PENDING_RULING, and the same case after a ruling, which then adopts.

**Clause tests:**
- **Flagged-run route.** A flagged run sends T2 to UNDECIDABLE_ROUTE_A_TAIL ahead of IMPLEMENTATION_DEFECT.
- **A47 I1.** An invalid T-case cannot reach NOT_UV_RESIDUAL or SOURCE_REPRESENTATION_K_DEPENDENT. An invalid C5H, and an invalid C4T-D5, each read INCOMPLETE.
- **RA6 cases G1-G5** (Claude4 0047/0054). G1 is the R3 increments scaled so that D̂34 = 0.99: the max-based test passes and the per-row test fails. G2, the growing row 04 hidden under the max, is caught. G3, the sign change, is caught. G4, a TINY Picard-noise row, passes. G5 sits in the TINY blind spot and passes, and the T1_H backstop then reads HIGHER_K_DISAGREEMENT. Under A47 I2, TINY does not exempt the max-based clause.
- **Brackets.** BRACKET_HULL_MISS, with the RA4 next step, and BRACKET_MISS_OFF_RA4_BLOCK, both from on-disk failure records.
- **RO1.** RO1 firing in a T-run is recorded and is not an invalidity. A missing RO1 field is loud. RO1 firing in an identity run reads NO_RUN.
- **A47 I5.** max_iterations 16 is invalid, and the accepted iteration is reported.
- **A47 I4.** In parallel8 mode, a serial T-case is invalid and C4T-D5 is not exempt. The serial_with_exemption alternative adopts.
- **Other gates and cross-checks.** T2I FAIL leaves T2 NOT_READ. An I1T failure makes the case invalid. An inconsistent UVT flag is invalid. Unavailable E^A reads INCOMPLETE. MT, RB_FP-eps and run-sha cross-reference defects each read NO_RUN. An LO record on the wrong state is a defect (NO_RUN), not NON_LAPSE_TAIL_MATERIAL.
- **E-SEAL1.** Every gate's complete record PASSes. Each of the 348 single-field deletions makes that gate RECORD_DEFECT with the deleted field named. Every field read is documented in FIELDS.md.
- **CLI.** The real R3 probe reads INCOMPLETE. `--validity-only` on real C4R3 and C5R3 bytes contains no row value and no number. `--gates-only` is blinded. An unpinned prereg, an unknown label and a route-A mode conflict are each REFUSED.

## Real-record check (TESTED; `out/REAL_RECORD_CHECK.json`; C5H not opened)

- **R3 runs (10).** All COMPLETED and valid, with 12 finite rows, V2 met, and finish and receipt custody equal. Packets give V4 and V5 true with mask counts equal, final rows equal last-pass rows, and E_i is computable.
- **R3 runs probed as V007 cases.** V1 is true. V3 fails loudly, naming `FIELD_MISSING:result:route_a_outcome`, `/numerics/uv_tail`, the brackets (not RA4), max_iterations and driver.
- **C5R3.** Invalid: BRACKET_MISS_OFF_RA4_BLOCK, `fs_columns_00:col0001:MASS_ENTHALPY_NOT_BRACKETED`. Its normalized_spec came from start.json, because the failed result lacks it.
- **C6R3.** Invalid: `ROUTE_A_READOUT_REFUSAL_NO_RO1:NO_SUBLUMINAL_CIRCULAR_PRESSURE_BRANCH`.
- **v009-GEO distance run.** The misses read as columns 44 (fs_columns_01) and 50 (fs_columns_03), matching A32.
- **v009-GEO deciding (i).** route_a_outcome reads (classification CONVERGED, converged_iteration). The attempt result is sha-verified, and its missing `result/uv_tail` is named.
- **Route-A controller records** (13 real `UNT_UV_TAIL_ROUTE_A_RECORD_C2V001` records from the route-A lane's runs).
  - They carry every field the reader reads: 0 FIELD_MISSING codes.
  - As test-only records they read inadmissible as expected.
  - Their 4-probe E_A rows are refused as not 12.
  - A record without v_ref reads `UVT_MONITOR_STATUS:M_T_NOT_NORMALIZED`, which is loud. So production monitor requests must carry v_ref and τ for the 12 row radii.
- **Finding (TESTED, relevant to R-PAIR load).**
  - On the R3 Picard trajectories, the single-run allowance max_i E_i/τ_i is: C4R3 0.045, S3R3 0.016, Y3R3 0.15, C3R3 0.27, S4R3 0.32, C2R3 0.67, Y4R3 0.65.
  - The pair rule needs E(a) + E(b) + E^A ≤ τ/8 = 0.125·τ on every row.
  - So pairs with R3-like trajectories (stopping at pass 3 with q near 0.9) are likely to need R-PAIR (Picard branch, 12 passes, bound 0.0025). This is a projection from R3, UNTESTED for T-runs.

## Ambiguities in the draft + RA + A47 text, and the resolution implemented (for root ruling)

- **AMB-01.** RA5's B0_RO1, RA8's B0_N3 and A47 I6's B1_OFF have no named outcome. They are placed in the NO_RUN group, as identity and implementation gates.
- **AMB-02.** A gate record that lacks a field, or names the wrong state, reference, configuration or coverage, is a *record defect*. This applies to any gate, including optional ones when supplied.
  - Resolution: NO_RUN (GATE_RECORD_DEFECT). It is never read as a numerics or physics outcome; for example, a malformed LO record does not read NON_LAPSE_TAIL_MATERIAL.
  - A *missing* record reads INCOMPLETE (A47 I1).
- **AMB-03.** NUMERICS_UNCERTIFIED and NON_LAPSE_TAIL_MATERIAL share position 3.
  - If both apply, the outcome is NUMERICS_UNCERTIFIED with NON_LAPSE_TAIL_MATERIAL also named.
  - GQ maps to NUMERICS_UNCERTIFIED (RA7).
- **AMB-04 (material).** "A test using any flagged run is read only as undecidable" is applied literally.
  - Position 4 pre-empts later readings even when they come from unflagged tests. In test F2, an unflagged, decidable T2 failure reads UNDECIDABLE_ROUTE_A_TAIL.
  - Consequence: FLAG_PENDING_RULING's clause "TAIL_SOURCE_UNDERCONVERGED on an adoption run" is unreachable for DDO, because every T-run is read by some test.
  - The alternative reading is not implemented: the flag would block only failing readings, and passing flagged tests would flow on to FLAG_PENDING_RULING.
- **AMB-05.** E_i edge cases:
  - "one pass: E_i = |d_last_i|" is read as two passes, i.e. one change.
  - One pass (no change) means E is unavailable, which reads INCOMPLETE.
  - d_prev = 0 with d_last ≠ 0 gives q = 0.9. d_last = 0 gives E = 0.
  - E needs the final rows to equal the last pass rows.
- **AMB-06.** Scope of the decidability rule:
  - applied to T1_H, T2 and T3, whose texts say "decidable";
  - not to T1 (R1 T1_status), T2c (CHECK K1 made it pass/fail), T1_S (its text has no "decidable"), or RB_FP (E is already inside its bound).
- **AMB-07.** R-PAIR "on the failing row", when several rows are undecidable:
  - The branch is chosen on the worst row, max (E+E^A)/τ.
  - R-PAIR members are keyed per pair (`<label>@RPAIR:<pair>`). A shared member (C4T in T1_H and both T3 pairs) is supplied per pair. The cap of ≤ 4 pairs equals the 4 decidability pairs.
- **AMB-08.** E^A for C5H, a direct run with no tail controller, has no named source.
  - Resolution: a required EA replay record with per_case C5H.
  - The EA record is also the fallback when a tail record's E_A rows are null (M_K unavailable). With neither, decidability is unknown and the reading is INCOMPLETE.
- **AMB-09.** RB_FP's "E_i(C4T-A, C4T)" is read literally as the Picard allowance only, without E^A.
- **AMB-10.** A T2I FAIL has no named outcome.
  - Resolution: T2 is NOT_READ, which gives INCOMPLETE (UNRESOLVED) with the T2I codes.
  - It could arguably be IMPLEMENTATION_DEFECT.
- **AMB-11.** I1T is a build-time refusal.
  - The I1T record must cover every T-case.
  - An uncovered or failing case is invalid, which reads INCOMPLETE.
- **AMB-12.** RA7 names the DDO C2T–C4T rosters (C4T to 64 /kpc) and NGC T120L.
  - Required reach: C2T and C3T to 32, C4T to 64, T120L to 32 /kpc.
  - The rosters of C6T, S4T, C4T-D5, C4T-C5c, C4T-K16, C4T-K64 and C4T-A are not named. They are accepted if supplied, and must then pass.
- **AMB-13.** "C4T-D5 numerics byte-equal to C5H's" is compared on the canonical JSON of the two results' `normalized_spec.numerics`.
  - Any key that v010's normalization adds, other than uv_tail, breaks equality loudly.
- **AMB-14.** R-PAIR's route-A branch ("seed source_rtol/10") has no spec field in v009 or v010.
  - The field is DECLARED as `numerics.route_a.seed_source_rtol_factor` = 0.1.
  - The driver lane must implement it, or root must name the field.
- **AMB-15.** The location of the RO1 record is unspecified.
  - It is DECLARED as `result.route_a_outcome.ro1` in every v010 result: T-runs and identity runs, admitted or computed.
  - A missing record is a loud code, because RA5 puts RO1 in every V007 run.
- **AMB-16.** V005's next-step texts:
  - V3 names C2'/F3, so its first sentence is used.
  - V1 (ii), the D7 recovery, is replaced by RA4.
  - V1 (iii) cites the obsolete iteration-4 lock. It is passed through verbatim, and root may want a V007 text for ROUTE_A_NO_FIXED_POINT.
- **AMB-17 (material).** First-applicable evaluation is three-valued.
  - If an earlier condition is unresolved, the reading is INCOMPLETE even when a later condition holds. For example, a pending T3 R-PAIR with a decidable failing T2 gives INCOMPLETE, not IMPLEMENTATION_DEFECT.
  - Root may prefer that a decided IMPLEMENTATION_DEFECT stands.
- **AMB-18.** A47 I1's "no T-test is read" is extended to NO_RUN and to position 3, consistent with R1's "no T run starts" and "blocks all T runs".
- **AMB-19.** What a flag ruling must contain is unspecified.
  - A FLAG_RULINGS entry {flag, scope, ruling, root_decision} marks the flag as ruled, whatever its text says.
- **AMB-20.** No text carries V006 R1's v009 admissibility condition (REVIEW_V009, E-SEAL1) into V007.
  - Resolution: C5H is admitted on driver 999331af, spec 60b46130, V1-V5 and RA4.
  - Root to confirm.
- **AMB-21.** Accepted route-A iterations and Picard pass counts are recorded but not compared (R1 L1). They are reported per case (A47 I5).
- **AMB-22.** The row order of E_A is not verifiable from the controller record, which lacks probe_R.
  - It is DECLARED to be the 12 row radii in row_ids order.
- **AMB-23.** LO_NGC is reported but not required for the DDO decision ("for NGC readings").
  - The NGC N-tests are outside this compare, because they are not in the decision rule.
- **AMB-24.** Some R1 texts are superseded but still present, and the sealed text needs rewriting (A47 I2):
  - fixed_across_all_cases.brackets ("D7 R3 block, W1 widening");
  - T2_numerics (C6);
  - T2I (G6\G4);
  - the C4T-D6 / C4T-C6c run list;
  - the "external: direct C6" entry.
  - The compare implements RA1, RA3, RA4 and RA11.
- **AMB-25.** An MT record is optional. If supplied, it must cover every T-case and is cross-checked against each run's tail record.
- **AMB-26.** Receipts are not a V005 gate.
  - When a receipt is present, a result-sha mismatch fails V1.
  - When it is absent, that is noted only.

## Seal-time steps (RA13, A47 I3)

1. Write the V007 case block: the v010 sha in drivers_allowed, uv_tail_config_sha256 and `/numerics/uv_tail` for each T-case, and route_a_mode. Pin it as `binding_inputs.case_block` in the prereg.
2. Set `V007_PREREG_SHA256`. The seal record then pins this script's new sha.
3. Run `--gates-only` on the real gate records, and `--validity-only --case C5H` on the C5H receipt and result. Both modes print and write no row value. The seal record states that no row value was shown.
