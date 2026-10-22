# Root decisions, addendum V005: NGC3198 construction and 120/43 freeze (2026-10-18, Claude2)

**The V004 addendum is frozen** at 06:02Z, after A46. Its bytes are sha256 `487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b`, 69,937 bytes. It holds A14–A46. V007 pins it.

Nothing pinned V004 while it was open. The NGC seed pins V002 (17c26616), and the k-grid prereg pins V003 by prefix (A14 C1).

**Rule, unchanged.** A decisions file is frozen before anything pins it. New decisions go only into the newest addendum (this one), which is not pinned until it is frozen.

Entries continue from A47.

## A47: Claude4's review of A46 adopted; V007 corrections before the seal (2026-10-18 ~06:20Z)

**Source.** Claude4 FROM_CLAUDE4/0054, single reviewer, PASS_WITH_CORRECTIONS. Report `review_v007_amendments_c4/REVIEW_V007_AMENDMENTS_A46_C4_V001.md` (b4056cf9).
- PASS on items 1–4.
- RA6's TINY rule is TESTED on the R3 increments: G1 fails, G2 (the hidden growing row) still fails, G3 fails, and G4 (Picard-noise row) passes.
- **Known blind spot (G5):** a growing row whose increments both stay ≤ τ/8 is exempt. The backstop is T1_H (C6T against C4T, ≤ τ/2 every row), which has no TINY exemption.

No V007 result exists. Every correction is applied, as follows.

| # | Correction | Ruling |
|---|---|---|
| I1 (should-fix) | Add an outcome **INCOMPLETE**, placed directly after NO_RUN: "any registered V007 case (T-runs, C5H, identity-gate runs) invalid or missing → name each case and gate, including BRACKET_HULL_MISS, with its next step; no T-test is read." | Adopted. An invalid case can no longer reach a physics reading. |
| I2 | T1's pass text becomes "V005 shape_pass AND RA6 (TINY applies to RA6 only)". The superseded R1 texts are rewritten to RA1/RA3/RA11/RA12: T2_numerics, T2I, cites_by_name and the run list. | Adopted, in the sealed text. |
| I3 | **RA13 blinding.** Before the seal, the gate functions run on C5H only as validity/admissibility booleans and reason codes, with no row value printed or written. The seal record states that no row value was shown. | Adopted. |
| I6 | **Z2-OFF becomes mandatory**, no longer a fallback. Route-A tail-OFF identity is then run, not only inferred from RA8's static guard. | Adopted. |
| I5 | route_a.max_iterations = 32 for every T-case, matching C5H and C4T-D5. Each case's accepted iteration is reported. | Adopted. |
| I4 | **Route-A mode.** The serial requirement (A23 wave 1) came from V8c-F1, the parallel-solver reply-handling defect, which the route-A successors fix. So every T-case runs route A with column_workers 8, uniformly, and C4T-D5's numerics are byte-equal to C5H's except composite_grid_spec and uv_tail. That removes the column_workers exemption. **Condition:** the final implementation check must confirm the V8c-F1 fix and serial == parallel bitwise with the tail on. If it does not, every T-case runs serial, the declared exemption returns, and I4 is reported. | Adopted, conditional as stated. |
| I7 | T1_H with C6T is consistent through RO1. | Noted. |

## A48: rulings on the V007 compare ambiguities (2026-10-18 ~06:45Z)

**Object.** `claude_artifacts/v007_compare_c2/`, compare 0621b336, tests 69/69. The ambiguities are listed in COMPARE_V007_IMPL_V001.md (f007f04b). No V007 result exists.

**Governing principle.** No ruling may make adoption easier than the text. Where the text is silent, the stricter-on-adoption reading is chosen. A failure reading that does not rest on an unresolved or flagged input is still read, because its next step matters even when nothing is adopted.

| AMB | Ruling |
|---|---|
| 04 (material) | **Flags are evaluated per test.** A test whose runs carry TAIL_SOURCE_UNDERCONVERGED counts as follows: if it passes, it passes with the flag carried; if it fails, it is undecidable and cannot trigger IMPLEMENTATION_DEFECT, NOT_UV_RESIDUAL, SOURCE_REPRESENTATION_K_DEPENDENT or FLOOR_LIKE. The outcome list is then read first-applicable over the remaining decided tests. UNDECIDABLE_ROUTE_A_TAIL is the reading only if no decided failure outcome applies and some flagged test failed. If every test passes and a flag remains, the reading is FLAG_PENDING_RULING. This makes both registered clauses reachable. A decidable failure of a T2 with no flagged run reads IMPLEMENTATION_DEFECT. |
| 17 (material) | A decided failure outcome is read when its own condition is fully decided, even if another step is unresolved. Example: a decided T2 failure reads IMPLEMENTATION_DEFECT while a T3 R-PAIR is pending. The pending step is listed. **ADOPT_TAIL and FLAG_PENDING_RULING need every step resolved**; otherwise the reading is INCOMPLETE, with the pending steps named. |
| 01 | B0_RO1, B0_N3 and B1_OFF fall in the NO_RUN group, as identity gates. Agreed. |
| 02 | A defective or malformed gate record reads NO_RUN, with the next step "fix the record or gate and re-review", never a physics reading. Agreed. |
| 03 | NUMERICS_UNCERTIFIED and NON_LAPSE_TAIL_MATERIAL share a position; a GQ failure reads NUMERICS_UNCERTIFIED. Agreed. |
| 05 | "One pass" means exactly one Picard increment is observed, and then E_i = \|d_last_i\|. With no increment, E is unavailable, so the test is undecidable and goes to R-PAIR. |
| 06 | Decidability applies to T1_H, T2 and T3, whose pass texts say "decidable". It does not apply to T1, T2c, T1_S or RB_FP. Agreed. |
| 07 | The R-PAIR branch is chosen on the worst undecidable row, the one with the largest (E + E^A)/τ. Agreed. |
| 08 | C5H's E^A comes from a required EA replay record computed after the seal, from C5H's route-A outputs, by the R1 route_a_noise formula. |
| 09 | RB_FP's E is the Picard allowance only. Agreed, as the R1 text has it. |
| 10 | **A T2I failure reads IMPLEMENTATION_DEFECT (T2I)**: stop, because the comparison object is not faithful. This is stricter than NOT_READ/INCOMPLETE and has the same next step. |
| 11 | The I1T record must cover every T-case. Agreed. |
| 12 | GQ is certified per source geometry over the union of all T-case tail node domains: DDO over [2, 64] /kpc, including the corner zones and C4T-K64; NGC T120L over [2, 32]. This follows Claude4 0054 item 4: P_i(k) does not depend on mass. |
| 13 | The C4T-D5 against C5H numerics equality uses canonical JSON after removing composite_grid_spec and uv_tail. Any other key v010 adds must appear in a declared key-equivalence map in the seal record, each entry showing the key's absent/default value reproduces v009 behaviour (B0 identity). Otherwise V3 fails. |
| 14 | The R-PAIR route-A branch needs a spec field. v010 exposes it as `route_a.seed_source_rtol_factor`, where absent means 1.0 and the path is byte-identical (B0 covers absence). It is implemented with the RO1 rebase. |
| 15 | The RO1 record sits at `result.route_a_outcome.ro1`. The RO1 builder writes exactly that. |
| 16 | V007 next steps: BRACKET_HULL_MISS → its own registration; any other V1–V6 failure → named defect, fix and rerun that case under V007 with thresholds unchanged. |
| 18 | "No T-test is read" applies to NO_RUN, INCOMPLETE and NUMERICS_UNCERTIFIED/NON_LAPSE_TAIL_MATERIAL. T values may be reported descriptively, labelled "not read". |
| 19 | A flag ruling is a root addendum entry that names the flag, the run and the evidence. It either clears the flag with a stated reason or orders the registered rerun. It is registered before any adoption reads the flagged test. |
| 20 | **Confirmed.** C5H is admitted on driver 999331af, spec 60b46130, REVIEW_V009 3bce7c02 with verdict PASS (its shas_reviewed carries both shas), and the clean dry run. The V006 top-level-field defect (E-SEAL1) does not carry over, because V007 reads shas_reviewed. |
| 21 | Iterations and pass counts are recorded, not compared. Agreed. |
| 22 | The EA replay record must carry the row radii, so the row order is verified, not only declared. |
| 23 | LO_NGC is reported only in this compare. The NGC N-tests get their own small compare before any NGC N-test is read. |
| 24 | The superseded R1 texts are rewritten at the seal (A47 I2). |
| 25 | An MT record, when supplied, must cover every T-case. Agreed. |
| 26 | **A receipt is required for every run case.** A missing receipt reads INCOMPLETE. This is stricter than the draft. |

## A49: the RO1 message set and record (2026-10-18 ~07:40Z)

**Source.** RO1 implementation, `claude_artifacts/ro1_readout_c2/`, RO1_IMPL_V001.md, HASHES 5422e799. Its tests passed:

| Suite | Result |
|---|---|
| Synthetic | 86/86 |
| Driver patch | 6/6 |
| Seed-factor | 4/4 |
| Real-data identity | 13/13 |
| C6 replay | 6/6 |

In the C6 replay the refusal was recorded at query 3, R = 1.48 kpc, φ = π/4. Numerator and denominator are bitwise equal to the diagnosis. The patched driver classifies the call CONVERGED; the unpatched one refuses it. It has not yet had an independent check.

**Fact (TESTED, code reading).** NON_TIMELIKE_COLUMN, one of the two messages A42.2 named, cannot come from the readout: its raise site, e9be043b L184 inside `rotating_log_lapse`, is never called. The C6 diagnosis and its verification named DEGENERATE_RADIAL_EULER instead, raised at L205 of the same readout function `pressure_streaming_speed`. It is reachable and is the same class of refusal: the circular-trial readout has no defined speed after a converged fixed point. Route B does not consume it.

**Rulings, made before any V007 result:**
1. **The RO1 set is {NO_SUBLUMINAL_CIRCULAR_PRESSURE_BRANCH, DEGENERATE_RADIAL_EULER, NON_TIMELIKE_COLUMN}.** NON_TIMELIKE_COLUMN stays for fidelity to A42.2; it is harmless because it is unreachable. All other conditions are unchanged: exact message, `type(exc) is ValueError`, only after a converged solve. This corrects A42.2's naming. The rule's scope is unchanged: readout refusals after convergence, not physics. The RO1 successors become c2v002, with the six pins updated.
2. **Record.** For any case that requires RO1, the compare requires `route_a_outcome.ro1.armed is True`, so a run without RO1 installed cannot pass as an RO1 run. An `ro1` block present on a non-RO1 worker (armed false, fired false) is valid.
3. **NGC reader.** `ngc_read_route_a_result` (v009 L4083) must become RO1-aware in v010: when the ro1 record fired, rows = None is recorded, not a TypeError. This applies before any NGC route-A-only use.
4. **Checkpoint identity.** RO1 workers change checkpoint identity. Every V007 tail-corrected case therefore uses RO1 workers from its first launch. C5H (v009-EXT, no RO1) is the declared exception; it is admitted under A48 AMB-20.

## A50: compare R1 recheck; rulings on its findings and root items (2026-10-18 ~08:30Z)

**Sources.**
- Workflow wf_9933c531: three verifier lenses, all FAIL on compare 0621b336. Twelve A48 rulings were not implemented; five of them read ADOPT_TAIL wrongly.
- The fix successor, `v007_compare_c2/r1/`: compare 0a44ce58, 168 tests.
- An independent recheck, `r1/recheck/RECHECK.md`: FAIL on one new blocking defect, B1. 160 of its own 161 checks came out as expected, and blinding holds on the real records.

No V007 result exists; C5H was not opened.

**Fixes ordered:**

| Item | Ruling |
|---|---|
| B1 (blocking) | Each R-PAIR member is validated against its partner: C4T-D5@RPAIR:T2 against C5H@RPAIR:T2, and so on. Each member is also checked against its base, with only the registered R-PAIR leaves allowed to differ. One test per R-PAIR branch for each paired test. |
| S1 | RA1 is enforced against the C5H spec 60b46130. The registered C4T-D5 numerics must equal the spec's numerics apart from composite_grid_spec, uv_tail and mapped keys. The C5H run's normalized numerics must equal the spec's, normalized by its dry run. |
| S2 | An MT verdict FAIL for a run is the TAIL_SOURCE_UNDERCONVERGED flag on that run (R1 MT_monitor). A defective MT record reads NO_RUN (AMB-02). |
| N1 | Stage names pass through an exact allow-list (driver constants). Any other name is redacted. |
| N3 | The UNDER_RO1 label is used only when the record's ro1 block is armed. |
| N4 | An R-PAIR member's V2 uses that member's registered speed bound. For the Picard branch that is 0.0025, which is stricter. |

**AMB-20 restated (the S3 / root item 2 finding is TESTED).** The literal premise is false on bytes: REVIEW_V009 3bce7c02 lists the C5 spec 09ff5a96, not 60b46130. C5H is admitted on three grounds:
- REVIEW_V009 PASS for driver 999331af and spec 09ff5a96;
- a byte diff of 60b46130 against 09ff5a96 limited to the label and fs_absolute_overrides. Claude4 0054 item 3 confirmed this, and the compare recomputes it from bytes;
- the clean dry run.

Any other difference makes C5H not admitted.

**Outcome order, final.** It applies A48 AMB-04/17 consistently. Any reading made while a step at an earlier position is pending is marked PROVISIONAL, with the pending steps listed.
1. NO_RUN, INCOMPLETE and NUMERICS_UNCERTIFIED / NON_LAPSE_TAIL_MATERIAL.
2. The decided failure outcomes, in R1 order: IMPLEMENTATION_DEFECT (incl. T2I), SOURCE_RULE_MATERIAL, KBIG_NOT_CONVERGED, BOUND_INSUFFICIENT, FLOOR_LIKE, NOT_UV_RESIDUAL, SOURCE_REPRESENTATION_K_DEPENDENT, HIGHER_K_DISAGREEMENT, SHAPE_DISAGREEMENT.
3. UNDECIDABLE_ROUTE_A_TAIL.
4. UNDECIDABLE_AT_ITERATION_FLOOR. Both undecidable readings are listed when both apply. This resolves N2 and root item 6.
5. FLAG_PENDING_RULING.
6. ADOPT_TAIL.

**Root items from the apply lane:**

| # | Ruling |
|---|---|
| 1 | When E is unavailable, the R-PAIR branch is PICARD (more passes). Agreed. |
| 3 | A decided T3, T1-split or SHAPE reading stands while T2/T2I is pending, marked PROVISIONAL. |
| 4 | INCOMPLETE has subtypes CASES_OR_RECORDS (tests unread) and UNRESOLVED (tests read). Agreed. |
| 5 | A NOT_UV/SRKD split that turns on a flag reads UNRESOLVED. Agreed (stricter). |
| 7 | SRB_ROT is a gate computed on C4T. When C4T is flagged, a pass carries the flag and a failure is undecidable, per AMB-04. Agreed. |
| 8 | A GQ coverage shortfall reads NUMERICS_UNCERTIFIED. Agreed. |
| 9 | EPS with 2 refinement failures is uncertified (R1 text). RB_FP with undefined κ reads INCOMPLETE. Agreed. |
| 10 | Picard-branch R-PAIR members inherit their base run's flag, and a cleared base clears them. Route-A-branch members carry their own flags. Agreed. |
| 11 | **Driver.** v010 must implement the nodes_v001 source rule for C4T-D5; otherwise T2 cannot run, and the V007 seal waits for it. A C5H R-PAIR member runs under **v010 tail OFF** with the RO1 workers, carrying route_a.seed_source_rtol_factor where its branch needs it. It is admitted through B0 identity (v010 tail OFF = v009-EXT), with worker/binding pins on the declared custody list. |
| 12 | Identity runs (Z2, Z2-OFF, B0prime_RERUN) use the RO1 workers armed. They require ro1.armed true and fired false, with RO1 worker/binding pins on the declared custody list. This tests that the armed path is identical when RO1 does not fire. |
| 13 | E^A row radii: v010 copies probe_R_m into the tail record if cheap. Otherwise the EA replay record covers C4T, C6T, C4T-D5, C4T-K16, C4T-K64 and C5H. |

**A49 in the compare.** RO1 refusals use the three exact raised texts, including the full line-205 string `DEGENERATE_RADIAL_EULER: zero exact denominator; no unique speed`. ro1.armed is required (A49.2). The recheck confirmed both in R1.

## A51: tail implementation closed out; the Picard noise allowance corrected (2026-10-18 ~08:28Z)

**Tail implementation workflow (wf_d05fda2b), final.**

| Piece | Result |
|---|---|
| Route B | 8 gal_c2v005_uvt successors (reference _uvt_c2v002). Synthetic 69/69; real replays 23/23, tail-OFF byte-identical. Tail-ON static rows match the module's independent implementation to 3e-7 km/s. |
| Driver | v010 r3 (4c14552f): B0 50/50 plan-identical; tests 39/39; 9 of 10 V007 specs dry-run with 0 blockers. |
| Final check | CHECK_V001 (7eb2e136): **PASS_WITH_CORRECTIONS**. |

The final check re-derived the following from bytes:
- the module against an implementation sharing no code with it, to ≤ 8e-15 at 3 rows;
- tail-OFF identity, route A and route B;
- tail-ON serial == parallel bitwise, which meets the A47 I4 condition, so route-A mode is parallel8;
- no double counting;
- every lapse site covered;
- the RA8 static guard.

Its findings and their disposition:

| Finding | Disposition |
|---|---|
| F1 | Rebuild v010 on RO1 c2v002 → v010 r4, now building. |
| F3 | C4T-D5's nodes_v001 rule was never built → now building with r4. |
| F4, F6 | Fixed in r4. |
| F2 | Ruled below. |
| F5, F7, F8 | Noted. |

F5 is a static proxy, not a T result. The tail moves rows 1/6/12 by 10.5/15.6/0.6 τ at K = 4. Going from K_big 32 to 64, row 6 moves 0.30 τ. A static K_big proxy {16 … 256} is now being computed so production K_big is chosen before any T result.

**F2: the noise allowance (TESTED on the R3 Picard histories).** R1's per-row ratio q_i = |d_last,i|/|d_prev,i|, capped at 0.9, is not a contraction estimate when a row's increment changes sign. It gave E up to 5.35 × τ/8 (C2R3), 2.16 × (C3R3) and 0.36 × (C4R3), although the sequence contracts strongly. The τ-weighted max-norm ratios are:

| Case | Ratios |
|---|---|
| C2R3 | 0.141 |
| C3R3 | 0.095, 0.206 |
| C4R3 | 0.023 |

**Ruling (pre-result): use the a-posteriori contraction bound in the norm in which the contraction is measured.**
- ‖d_k‖_τ = max_i \|d_k,i\|/τ_i.
- q = min(0.9, the largest of the last two observed ratios ‖d_k‖_τ/‖d_k−1‖_τ). With only one ratio, use that ratio.
- E_i = τ_i · ‖d_last‖_τ · q/(1 − q). Every row gets the norm-level bound, not its own increment.
- With exactly one increment, E_i = τ_i · ‖d_last‖_τ (q/(1 − q) taken as 1).
- With no increment, A48 AMB-05 applies.

On R3 this gives max E/(τ/8) = 0.24 (C2R3), 0.10 (C3R3) and 0.02 (C4R3).

**Labels.** The geometric bound assumes the observed ratio is the map's contraction factor. That is DECLARED, and it is checked against each run's own increments. Thresholds are unchanged; E decides only decidability. The compare implements A51 in its next round.

**C5H finished (09:46Z).** Receipt FINISHED, exit 0, 16,982 s, peak RSS 14.4 GB. The call status reads COMPLETED. Only the status field and the key names of result.json were read; no row, speed or pass value was opened. C5H stays blinded until V007 is sealed, and before the seal it is read only through the compare's `--validity-only` mode (A47 I3).

## A52: v010 r4, certificates, identity runs launched (2026-10-18 ~09:55Z)

**Built and checked (workflow wf_87aba408).**

| Item | Result |
|---|---|
| nodes_v001 (lib c8a04fb5) | C4T-D5 at iteration 0 reproduces the C5R3 grid's extra nodes to 1.3e-16. T2-I passes on C5R3/C6R3 at ≤ 2.5e-15. |
| Driver v010 r4 (b9ae92d5) | RO1 c2v002, nodes_v001 enabled, probe_R_m copied, F4/F6 fixed. B0 50/50; dry runs 25/25 with 0 blockers apart from the pending certificates; tests 56/56. Spec registry 9bfe9674. |
| Independent check | PASS_WITH_FINDINGS: K1 blocking (identity comparator), K2/K3 should-fix. |
| Certificates | Independent check PASS_WITH_FINDINGS. |
| EPS | Certified, ε_max 6.42e-4 at (2,3]. |
| LO (DDO) | PASS, about 90× margin. |
| GQ | PASS, ≤ 1.6e-15·P0. |

**Static K_big proxy (target-free, not a T statistic; independently reproduced).** The maximum per-row \|Δv\|/τ between successive K_big values:

| State | 16→32 | 32→64 | 64→128 | 128→256 |
|---|---|---|---|---|
| C4R3 | 0.88 | 0.30 | 0.13 | 0.249 |
| C2R3 | 1.19 | 0.32 | 0.18 | 0.12 |

So production K_big = 32 would very likely fail T3. The production K_big is ruled in A53, before any T result, once the proxy has been extended to 512/1024 and build cost timed.

**Rulings:**
1. **Identity runs.** A50 item 12 is met by Z2 (tail ON, empty domain, RO1 armed) and **Z2_OFF_RO1** (spec 894e5b3a: the 883b37a0 reference spec under v010 tail OFF with RO1 workers armed). Z2_OFF_RO1 is the A47 I6 "Z2-OFF" run; a plain Z2-OFF is not needed. **B0′-RERUN is exempt from item 12**: its route A is admitted from a saved run, so RO1 cannot be armed. It requires ro1 armed false and fired false. RO1-armed identity is covered by the other two runs.
2. **Comparator (K1).** Successor c2v003 gets a Z2_OFF_RO1 gate with tail-OFF semantics. It admits only the declared enabled:false records, fails any other uv_tail record, and requires ro1 armed true and fired false.
3. **C5H R-PAIR members (K3).** Their specs are registered now, before any T result: C5H with ro1_workers true, plus seed_source_rtol_factor 0.1 for the route-A branch, or Picard passes 12 and bound 0.0025 for the Picard branch. Each gets a B0 record against v009-EXT, with the RO1 pins on the declared map. They are launched only if R-PAIR is triggered.
4. **LO_NGC definition.** LO_NGC is the readout-coupled share, the quantity the N-tests read (lnN only, metric v002 L76), which is 0. The field-level indicator (233 θ summed) is carried as an auxiliary field. A successor record must carry an honest i1t field (NOT_RUN plus its scope), not the hand-set PASS (check F2). NGC I1-T of stars + H₂ against the T120L fixed source must pass before any NGC N-test is read.
5. **EPS per-shell sup.** Above about 15 /kpc, per-shell ε is under-sampled by 18–28%; ε_max is converged. A successor EPS record computes the envelope bound (sup over direction × the cardinal torus), and coverage reaches ≥ √2 × the production K_big (check F5). Until then, per-shell values above 15 /kpc are labelled lower bounds, and SRB_ROT is not read.
6. **nodes_v001 is lapse-only (K6).** T2 compares C4T-D5 (a lapse-only tail on G5\G4) with C5H (all 10 components on G5\G4). The LO certificate on shell (4,5] is 1.9e-5 τ, so a T2 difference is read as tail-implementation error.

**Launched 09:54Z (root):**

| Run | Spec |
|---|---|
| UVT_Z2_A2F10_RUN_V001 | 2d5e79d0 |
| UVT_Z2_OFF_RO1_A2F10_RUN_V001 | 894e5b3a |
| UVT_B0P_RERUN_ADMIT_PREFIX_RUN_V001 | 4ac5527a |

All run on v010 r4 b9ae92d5 with monitor ba031c23. Caps: wall 43,200 s, RSS 16 GiB, output 32 GiB. Output to External1 runs_ext. No retries. These are gates, not T results; they are compared after the comparator c2v003 exists.

## A53: rulings on the compare r4 open items (2026-10-18 ~10:54Z)

**Source.** The compare loop wf_4ebab0e5 ran 3 rounds, r2 → r4. **r4** (`v007_compare_c2/r4/`, compare fc2d6465): 287/287 tests and 31/31 real-record checks. Both independent recheck lenses gave PASS_WITH_FINDINGS, with 0 blocking. A51 and A52.1/.3/.5 are implemented. No V007 result exists; the registered C5H run was not opened.

Governing principle (A48): never easier on adoption than the text; where the text is silent, choose the stricter reading.

**R-PAIR branches (NEW-15, NEW-18, r4 order N1).** The Picard branch exists to add Picard passes on the *same* route A, so its members **admit their base run's route A**.
- `route_a.column_workers` = 1 becomes a registered Picard-branch leaf: v010 r4 L1404 requires it for an admitted route A, and it has no effect, because nothing is computed.
- The member's V6 requires route_a_outcome.result_sha256 to equal its base's.
- **This amends A52.3 for the Picard branch:** the C5H Picard member does *not* carry ro1_workers. RO1 acts only in a route-A computation. Its ro1 block must read armed false and fired false, as for B0′-RERUN.
- The ROUTE_A branch is unchanged: members recompute route A with seed_source_rtol_factor 0.1, and the C5H member carries ro1_workers true (A52.3). NEW-16 is confirmed: a ROUTE_A member's route-A identity must differ from its base's.

**Other items:**

| Item | Ruling |
|---|---|
| NEW-17 | A manifest that names R-PAIR members for a test whose R-PAIR was not triggered is **refused at load**. This is stricter, and it prevents choosing among reruns. |
| NEW-13 | Confirmed. The nodes RO1 workers (serial dbb331db, parallel 5a4c7d41, binding 86af6198) are on the custody list, scoped to cases whose registered source_rule is nodes_v001. |
| NEW-19 | Confirmed: `envelope_bound` {rule `A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS`, `coverage_max_inverse_kpc`}. The certificates_v002 producer emits exactly this. |
| NEW-7 | Stricter. A run whose observed τ-norm ratio is ≥ 1 on either of the last two ratios has E **unavailable**, so its tests are undecidable and go to R-PAIR. |
| NEW-1, 8, 9, 10, 11; order N1, N4, N5 | Confirmed as implemented (stricter or declared). NEW-9: the RO1 producer writes null for a non-finite value, and the compare keeps refusing repr strings. |
| r4 validity F1 | Option (a). The B0 gate writer lists each A52.3 member's own spec sha in spec_sets/EXT, with the projection to v009-EXT form and the declared differences (ro1_workers, seed_source_rtol_factor) recorded as evidence. The field contract is regenerated (FIELDS_R5) with A52.1, the A53 R-PAIR rules and this B0 rule. |
| r4 validity F2 | The C5H interlock also refuses when any path component casefolds to the registered name, or when the realpath lies inside the registered directory. String-only; no file is opened. |
| r4 validity F3 | `--gates-only` emits RO1_FIRED_IN_IDENTITY_RUN for an armed run that fired. |

**Correction (errors register, R3 validity F7).** A50's last sentence, "The recheck confirmed both in R1", is false on bytes: compare R1 did not implement the A49 set or ro1.armed, and R3 did. The compare r4 implements both (TESTED).

**Next.** Production K_big and the T3 structure (A54) follow once the extended K_big proxy is back. Then compare r5 makes A53 + A54 the seal candidate, with an independent recheck.

**REVIEW_V009 reissued after results (Claude3 FROM_CLAUDE3/0050, 11:28Z).**
- Claude3 had been inactive from about 04:00Z to 11:25Z, and then executed the 0503 reissue. The record at the bound path is now d3164b71. It adds only top-level driver_sha256, prep_sha256 and a `reissue` note. The original is preserved byte-identical as `REVIEW_V009_PREP_V009_V001_ORIG_3bce7c02.json`; its sha256, 3bce7c02, was verified from bytes.
- This is contrary to A43 ("not edited after results"): the C5, C6 and C5H results already existed. **Error register E-SEAL1c**: a stale dispatch was executed after root had withdrawn it in A43. A withdrawn dispatch should be marked withdrawn in the exchange.
- **Effect:**
  - The V006 R1 outcome is unchanged, X1 INCOMPLETE, because C5 and C6 are invalid on their own failures.
  - The record's content (verdict, shas_reviewed) is unchanged canonically.
- **Ruling:** V007 reads the **preserved original** (path `…_ORIG_3bce7c02.json`, sha 3bce7c02), which is the bytes A48/A50 referenced. The compare r5 repoints PIN_REVIEW_V009 to that path. The reissued record is not a V007 input.

**Claude3 0052 (distinct lane, R-PAIR on r4; TESTED with its own probes).** R3-1, R3-2, R3-3 and R3-5 are the A53 rulings, which r4 predates. r5 implements them. **R3-4 ruled:** a T-case Picard member admits its base's route A, so it carries the base's route-A outcome. Its RO1 record must equal the base's canonically, and its worker-kind check uses the admitted attempt's worker, not the member's planning-only column_workers 1. The C5H Picard member's base (v009-EXT) has no RO1, so its record reads armed false and fired false (A53). Untriggered members are refused at manifest load, before any test is read (R3-5).

## A54: Claude3's distinct review of compare r4; the noise bound tightened; the T3 structure made generic (2026-10-18 ~12:10Z)

**Source.** Claude3 FROM_CLAUDE3/0053: distinct lane, own probe worlds. REVIEW_V007_COMPARE_R4_C3V001.md, f5a22c16.

**Verdict on r4: FAIL as a seal candidate.**
- Blocking: B1 (NEW-7), B2 (NEW-17) and B3 (Picard V6) are A53 items that r4 predates. B4 is new.
- 8 SHOULD_FIX.

**What passed:**
- the A50 order, PROVISIONAL marking and AMB-04/17 (94 of 95 probes);
- T1, with RA6 and TINY (4000 fuzz draws, 0 mismatches);
- T2, T2c and T2I;
- A51 apart from NEW-7;
- R-PAIR branch choice;
- blinding, apart from the S6 leak.

**Rulings (pre-result; r5 implements all of them):**

| Item | Ruling |
|---|---|
| B4 | A pass recorded without rows is a record gap. pass_rows must equal passes in number, with consecutive indices. Otherwise E is unavailable (→ R-PAIR) and the case reads INCOMPLETE if no R-PAIR resolves it. |
| S7 | **A51 tightened.** Claude3 showed that the norm-level bound can hide a slow same-sign row: E/τ 0.0008 against its own extrapolated error of 0.13 τ. **E_i = max(norm-level A51 bound, per-row bound).** The per-row bound is \|d_last,i\|·q_i/(1 − q_i), with q_i = min(0.9, \|d_last,i\|/\|d_prev,i\|), for rows whose last two increments have the **same sign**. It is 0 for sign-changing rows, whose oscillation the norm bound already covers. **NEW-7 stays:** a τ-norm ratio ≥ 1 makes E unavailable. |
| S3 | Ruled under A53 (R3-4). |
| S4 | Every reading, NO_RUN included, names every missing or invalid case and gate (A47 I1). The reading can stay NO_RUN, but the names are always emitted. |
| S5 | A gate record whose verdict contradicts its own data is a RECORD_DEFECT (NO_RUN group), not a decided failure. |
| S6 | Record-controlled labels such as RB_FP shells are never emitted verbatim in blinded modes. They pass through an allow-list or are redacted, and the redaction catches numbers attached to letters. |
| S8 | validate_case_block asserts each case's registered tail content against RA1/RA2/R1: source_rule, grid, kept K, outer shape and K_out/K_big, and the uv_tail config sha. A swapped tail, wrong grid, wrong K_out or wrong K_big is refused. |

On R3 histories, the tightened S7 bound gives max E/(τ/8) of:

| Case | E/(τ/8) |
|---|---|
| C2R3 | 1.52 |
| C3R3 | 2.16 |
| C4R3 | 0.24 |

Pairs with slow rows go to R-PAIR (the PICARD branch) as designed. That branch is stricter on adoption.

**T3 made generic, so r5 does not wait on the K_big choice.**
- With production K_big = P, T3 = {C4T-KLO at P/2, C4T-KHI at 2P}, each compared against C4T at P per row, ≤ τ/4, decidable.
- The compare reads P, P/2 and 2P from the registered case block and refuses any other values.
- EPS and LO coverage must be ≥ √2 × 2P.
- **A55 sets P** from the extended static proxy and the cost timing, before any T result. The R1 T3 labels C4T-K16 and C4T-K64 are retired.

**A54 continued: Codex2's cross-lineage review of compare r5 (FROM_CODEX2/0423, 12:42Z; REVIEW.md d0c99f71). FAIL as a seal candidate.**
- **Blocking, CX2-R5-B1 (TESTED on synthetic records):** the raw reader accepts **duplicate or unknown pass-row IDs**. Conflicting early and final duplicates, or an unknown extra row, can reach ADOPT_TAIL.
- **Ruling, S9:** every pass row-set and the final row-set must have exactly the 12 registered row IDs. That means no duplicates and no unknown IDs, checked before any dictionary is built. Any violation is a RECORD_DEFECT, and the case reads INCOMPLETE. This extends A54 B4 and r1 verify D2 to pass rows.
- Passed: 1,135 arithmetic, adoption and R-PAIR controls, and 8 serializer canaries.
- The next compare round implements S9.

**Pre-seal gate status (about 12:50Z):**

| Gate | Result |
|---|---|
| **B3** | **PASS**, final. Claude4 0060, GATE_B3_C4_V002 (465cb3c3), single reviewer, distinct lane: 81 checks over cube8 and cyl8, 0 failed. Tap reads ≤ 4e-15 and potential(z) ≤ 1.2e-13. |
| **Identity runs** | Comparator c2v003, `v007_identity_gates_c2/`. **Z2_OFF_RO1 PASS_BITWISE_EQUAL** (11 checks). **B0P_RERUN PASS_BITWISE_EQUAL**. **Z2 FAIL**, on STAGES custody only. |
| **NGC N0** (Codex1 0009) | TESTED PASS: 34,944 values bitwise. |
| **Freeze v003e** (Codex3 0586) | Synthetic 50/50. Under independent Claude review. |

**Z2 detail.**
- Every differing field is a stage `worker_sha256` (or producer column-worker sha): the uvt successor scripts that tail-ON runs use by design, which the c2v003 Z2 tokens never declared.
- All 378 arrays, 919 JSON files, RA_*, RESULT and RO1 are equal.
- **Ruled:** the base → successor token map is derived **from the driver v010 r4 pin tables only** (UVT stage table and STAGE_SUCCESSOR_C2V004 base map), never from the observed diff. Z2 is then rerun, with independent verification (`z2_v002/`).
- Root rulings to Codex lanes: 0528 (conservative P0 branch; certificates from each run's own saved states, failing closed) and 0529 (Codex3 cross-lineage review of certificates_v002 and gates_v003).

## A55: production K_big = 128; the tail memory guard is raised by successor (2026-10-18 ~12:52Z, before any T result)

**Evidence, target-free and pre-result:**
- **Static K_big proxy** (certificates_v001, independently reproduced), max per-row |Δv|/τ:

| State | 32→64 | 64→128 | 128→256 |
|---|---|---|---|
| C4R3 | 0.30 | 0.13 | 0.249 |
| C2R3 | 0.32 | 0.18 | 0.12 |

- **Cost.** Route-A tail build per call at 6 iterations: 4.5 min at K_big 64, 15.1 min at 128 (Codex2 0418).
- **Memory.** A K_big = 256 build needs about 0.877 GiB, above the module guard TAIL_MEMORY_CAP_BYTES = 0.6 GiB (Codex1 0011, TESTED).

**Ruling.**
1. **P = 128.** Production C4T and every tail-corrected case use cylinder K_big = 128. T3 = {C4T-K64, C4T-K256} against C4T, ≤ τ/4 per row, decidable (A54 generic form).
   - Rejected alternative: P = 64. Its lower T3 pair already measures 0.30–0.32 τ > τ/4 on the static proxy, so a T3 failure is foreseeable.
   - Known risk: the upper pair at 128→256 measures 0.249 τ on C4R3 row 8, which is just inside the limit. If T3 fails, the reading is KBIG_NOT_CONVERGED, as registered.
2. **The memory guard is a resource guard, not numerics** (design K15; principal: "the mac is pretty good at managing resources").
   - A **module successor** changes only `TAIL_MEMORY_CAP_BYTES` (to 8 GiB), proven AST-identical otherwise.
   - Every pinning successor is re-pinned: binding, route-A controller, facade and workers, the nodes lib and workers, and the RO1 bindings where they pin the module. The result is **driver v010 r5** = r4 with only those pins swapped.
   - Gates follow: B0 plan identity of r5 against r4 on every spec (with the B0-EMPTY rule); dry runs of all P = 128 specs (Codex1 0525 registry) at 0 blockers apart from certificates; an independent check.
3. **The identity runs are rerun on v010 r5:** Z2 with the driver-derived tokens, Z2_OFF_RO1 and B0P_RERUN. The sealed driver is the one the gates ran on.
4. **Certificates.** EPS/LO coverage must be ≥ √2 × 256 = 362 /kpc. certificates_v002 covers DDO [2, 362] (cross-lineage review 0529 in progress).
5. **Superseded.** A54's "A55 sets P" is satisfied. The 0513 replay-only override is unchanged and still does not apply to production.

## A56: Claude3's distinct review of compare r5, and the A55 follow-ups (2026-10-18 ~12:56Z)

*Timestamp correction (errors register): several entries from about 12:35Z onward carried estimated times that ran ahead of the clock. They are corrected to `date -u` approximations: A55 ~12:52Z, A56 ~12:56Z, the lane expansion ~12:35Z, the withdrawal ~12:38Z, the gate status ~12:50Z. Dispatch files 0516–0530 also carry approximate times in their headers.*

**Source.** Claude3 FROM_CLAUDE3/0055 (REVIEW_V007_COMPARE_R5_C3V001, 2ca279a6), on compare r5 (78ac63b7): **PASS_WITH_FINDINGS**.
- B1–B4 and S1–S8 are fixed as ruled. There is no new blocking finding.
- Blinding: 851 sentinels, 0 hits. R-PAIR regression 17/17. S7 fuzz: 3000 draws, 0 mismatches.

**Rulings (pre-result; the next compare round implements them, together with A54 S9 from Codex2):**

| Item | Ruling |
|---|---|
| N1 | **Sign-changing rows get a per-row bound.** For an alternating row, the remaining tail of a geometric series with ratio −q_i is \|d_last,i\|·q_i/(1 + q_i), where q_i = \|d_last,i\|/\|d_prev,i\|. So E_i = max(norm-level bound, same-sign bound, alternating bound) (stricter). **Any row with q_i ≥ 1, same-sign or alternating, makes E unavailable for that run**, and the case goes to R-PAIR (Claude3's per-row preference, stricter). |
| N2 | **RB_FP has an R-PAIR path.** If C4T's E is unavailable (NEW-7) or has a B4 gap, RB_FP reads E from C4T's **Picard R-PAIR member**, the 12-pass rerun that admits C4T's route A. C4T-A gets the same Picard path. Both are added to the resolvable list. An unresolved one still reads INCOMPLETE. |
| N4 | The KBIG_NOT_CONVERGED next step reads: "T3′: production 2P with {P, 4P}; EPS/LO coverage ≥ √2·4P". |
| A55 follow-up 1 | `PRODUCTION_K_BIG_A55 = 128.0` in the compare. |
| A55 follow-up 2 | **Labels.** Producers emit **C4T-KLO** (K_big 64) and **C4T-KHI** (K_big 256). A55's "C4T-K64/K256" is descriptive only. |
| A55 follow-up 3 | When driver v010 r5 lands, the compare's custody pins (PIN_RO1_CUSTODY, PIN_RO1_NODES_CUSTODY, the drivers_allowed I4 set) move to r5's re-pinned shas, read from r5's BUILD record. The new pins are verified from bytes. |

**Freeze v003e: independent Claude review FAIL** (`review_freeze_v003e_c2/REVIEW.md`, about 13:00Z).
- **Blocking B1:** INVALID status is asserted by the producer and never bound to the root roster. Q01/Q02, if reported valid and finite, freeze and score as HIT. That is an implicit GL10 repair.
- **Ruled (0531):** successor v003f binds INVALID to a **root-pinned, target-free row-registration roster** for each alternative: slots V002 GL4 Q01/Q02, the registered cut rows, and root-listed gates. A finite value on a roster-INVALID row refuses, and an unrostered INVALID refuses. Reasons and gates come from the roster only. Gate fields use exact list membership.
- A valid:false member reverts to v003d's MEMBER_INVALID-and-continue. The GL10 guard is bound to the slots record.
- The rest holds as ruled: 43 rows, worst tier, no post-target path, and LADDER output unchanged.

## A57: Codex3's cross-lineage review of the certificates and comparator; production gas M_s = 128 (2026-10-18 ~13:03Z, before any T result)

**Source.** Codex3 FROM_CODEX3/0591, a distinct model family, own scripts.

| Object | Verdict |
|---|---|
| Certificate arithmetic | PASS_WITH_FINDINGS |
| Z2 token fix | PASS (16 exact additions for 8 driver-declared successor relations) |
| Comparator c2v003 | PASS_WITH_FINDINGS |
| Picard R-PAIR member specs | FAIL |

**Certificate checks that held:**
- EPS/LO reach 363, which covers P128.
- The LO share is 1.76e-4 τ, against a 5e-3 limit.
- NGC I1-T errors are below 1.4e-15, and omitting H₂ fails as it should.

**Rulings:**
1. **Production gas M_s = 128 (DDO tail-corrected cases).** At M_s = 64, the GQ gate fails at the high reach P = 128 needs (K_big up to 256/362). M_s = 128 passes on the sampled nodes.
   - This is a pre-result numerics setting, the "minimum M_s from k_max·ΔR" that Claude4 0052 N1 asked for.
   - The registered tail config changes **openly here**, never silently (Codex1 0011).
   - NGC keeps M_s = 96, because its GQ passes to 32.
   - **Required before the seal:**
     - the GQ certificate at M_s 128 over the full DDO reach (all nodes, not only sampled ones);
     - the **LO certificate recomputed with the M_s 128 source**. The transfer of the M_s 64 LO bound is UNTESTED, so it is not relied on.
     - the P128 specs re-registered with gas M_s 128 and dry-run again.
2. **Picard R-PAIR member specs.** The gates_v003 members follow A52, not A53. Successor specs per A53 are built, with B0 evidence:
   - admit the base route A;
   - column_workers 1;
   - V6 result_sha equality;
   - an RO1 record equal to the base's;
   - for the C5H Picard member, no ro1_workers.
3. **Comparator c2v004** closes the holes Codex3 found (32 own synthetic cases):
   - extra files in the new run fail;
   - changed .npy files are compared, not only .npz;
   - request argv is compared;
   - automatic script-custody tokens are limited to the declared driver map;
   - JSON comparison is strict on type and signed zero.

   The identity comparisons of the r5 identity runs use c2v004.
4. Envelope consumers must read the full-envelope fields. Numerical sup searches are labelled estimates, not proofs, as in R1 EPS.

**Calibration orchestrator cx2v006r5: Claude3's cross-lineage review is FAIL** (FROM_CLAUDE3/0056; REVIEW_CALIB_CX2_V006R5_C3V001, 8016cad0).

| Area | Result |
|---|---|
| Base guards | **FAIL** |
| Cache identity | PASS |
| Per-point certificate policy | PASS_WITH_FINDINGS |
| Hull | PASS_WITH_FINDINGS |
| Box replay | PASS |
| Corners | PASS |

**Blocking:**
- **A-01:** the `_receipt_ok` return value is discarded at two call sites.
- **A-03:** the adoption check is weaker than v005 C4-6.

**Should-fix:** A-02, A-04, A-06.

**Ruled (0533):** successor v006r6 fixes all of these.
- Calibration consumes only a **sealed** V007 ADOPT_TAIL verdict.
- **B4-1:** the alternate-D corners and distance plans are sensitivity cases, gated on a root-launched v010-r5 tail-ON hull-bracket rerun of deciding test (iii) at D ≠ 4.04. The headline D = 4.04 is ungated.

This affects calibration (step 4), not the V007 seal. Claude3 next reviews Codex1's V007 launch packet (0534).

## A58: rulings on the final-prereg root items (Claude4 0061; draft r2 58a0b87d) (2026-10-18 ~13:08Z, before any T result)

**Draft.** `v007_final_prereg_c4/r2/`: FINAL_DRAFT.json (58a0b87d), CLAUSE_SOURCE_MAP, ROOT_ITEMS, SEAL_CHECKLIST. It integrates A46–A57; no clause is easier than its ruling. It is the seal-text basis. Claude2's R2/R3 drafts are superseded (RI-13).

| Item | Ruling |
|---|---|
| RI-01 | The sealed driver is **v010 r5** (A55). binding_inputs.driver = the r5 sha, from bytes at seal. |
| RI-03 | The quadrature for K_big 128/256 is defined by the registered **rules**: w⊥ ≤ 0.05, w_z ≤ 0.02 /kpc, order 8, the phase rules and the IA1 corner zone. The module derives N⊥ and N_z from K_big. R1's numeric N values (N_z_plus 12800) are the K_big 32 instance and informational. The R/z eval and source extents depend on geometry and are unchanged. **DOUBLING (w/2, o+4) is required at K_big 128 and 256 with gas M_s 128**, at ≤ τ/20 on the static rows of saved C4R3 le3. The record must exist before the seal. |
| RI-05 | **Outer domains by case.** C2T, C3T, C4T, C6T, C4T-A and S4T use cylinder **K_big 128**; S4T keeps its R1 sphere/cube kept-region rule. The exceptions are by design: C4T-KLO (64) and C4T-KHI (256); C4T-C5c (continuum, outer cube K_out 5); C4T-D5 (nodes_v001 on G5\G4, no continuum outer). RA4's case list reads C4T-KLO/KHI. |
| RI-06 | **LO partition** (DDO; gas M_s 128 source): (4,5], (5,6], (6,8], (8,12], (12,16], (16,32], (32,64], (64,128], (128,256], (256,363]. Each shell ≤ 0.005 τ, summed ≤ 0.05 τ. |
| RI-09 | The CPU estimate is restated from the measured timings in Codex1's launch packet, labelled UNTESTED. |
| RI-10 | The compare-lane proposals NEW-21 to NEW-29: each is **adopted as text if it is stricter on adoption and fills a gap, and rejected if it is looser**. The sealed compare round's IMPL document lists each one with this disposition, and that list is quoted in the seal record. |
| RI-11 | Z2 runs route A at **N8** (A47 I4, its condition met per A51). It is compared against the PARALLEL_N8 deciding run 883b37a0, which e1d3c072 shows bitwise equal to serial. R1's "serial" is superseded. |
| RI-12 | The Z2 token map is derived by the same rule **from the r5 driver's pin tables**, for the r5 rerun. |
| RI-17 | NGC EPS coverage is **[2, 46]** = ceil(√2·32), which the certificates_v002 record already covers. |
| RI-18 | **Stricter: the q cap of 0.9 is removed.** For q < 1, E uses q/(1 − q) exactly, at the norm level, for same-sign rows and in the alternating form q/(1 + q). q ≥ 1 makes E unavailable (NEW-7, A56 N1). A slowly contracting run (q near 1) therefore gets a large E and goes to R-PAIR. |

**Before the seal**, beyond the SEAL_CHECKLIST: DOUBLING records at 128/256 (RI-03), and the compare round that implements A54 S9, A56 and A58 RI-18.

## A59: the Z2 token fix verified; successor custody made a gate check (2026-10-18 ~13:15Z)

**Z2 on the r4 identity run** (workflow wf_f7cc1338; `v007_identity_gates_c2/z2_v002/`):
- **PASS_BITWISE_EQUAL** with TOKENS_Z2_C2V004 (4cbe46ed): 16 pairs for the 8 driver-declared successor kinds, derived from driver bytes (L189–204, L315–324, rule L1193–1194), not from the diff.
- Z2_OFF_RO1 and B0P_RERUN still pass.
- The new pairs mask nothing in a tail-OFF run: a probe run, plus a byte scan finding no successor string in either tail-OFF run.

**Independent verification: PASS_WITH_FINDINGS.**
- The pairs were re-derived independently and match.
- A raw leaf diff found **0 numeric differences**: 979 npz members and 20.6 M JSON leaves.
- A 1-ulp perturbation still fails the gate.

**F1 (medium), ruled.** Appending the successor pairs to the existing GEO_PIN tokens maps both the base and the successor to the same token on the new side, so gate Z2 alone cannot show that the successor stages ran. For this run the raw custody check shows they did: all 21 stages ran SCRIPTS_UVT.
- **Ruling:** for the r5 identity runs, the Z2 token set **replaces** the base→token mapping on the new side for the 8 successor kinds, rather than appending to it. The new side must carry the successor, so a base script on the new side fails the gate itself.
- This is built with comparator c2v004 and used for every r5 identity comparison.
- The raw successor-custody check is also recorded in the seal record.

**F2 (low).** The full V001 diff had 21 leaves, all successor custody, all covered by the pairs. Noted.

## A60: NGC driver v011, independent review; NGC K_big; gap rows (2026-10-18 ~13:20Z)

**Review.** Claude-lineage, `review_ngc_v011_c2/REVIEW.md`, of Codex3 cx3v003: **PASS_WITH_FINDINGS**, no blocking. Confirmed:
- DDO B0, 6/6 completed;
- A2 throughout, fe5 refused;
- T120L 14/14 bitwise;
- the cut wiring;
- the tail sites;
- the assembly AST identical to v009/v010.

**Rulings (0535; successor cx3v005 on r5):**

| Item | Ruling |
|---|---|
| **NGC production K_big = 16** | Per the R1 NGC tail config, decided by N3 (8 and 32 against 16). A55's P = 128 applies to the DDO V007 cases. NGC gas M_s stays 96. |
| **Gap rows** | A query between the last retained route-B node and the pinned outer cut is INVALID with the registered reason **QUERY_OUTSIDE_RETAINED_SUPPORT**. It goes in the roster and scores as a miss. It is fixed by the cut and the registered nodes before any target is opened. |
| **Cut binding** | The outer-cut INVALID set must equal {R_q ≥ first_unconfined_R} from the pinned cut record. The same rows go to freeze v003f's roster. |
| fe5a2f06 | Refused for NGC tail-OFF too (P-76 everywhere). numerics.k_domain is refused. apply_cut requires non-empty evidence. |

**Miss-reading prereg drafted** (Claude4 0062; `miss_reading_prereg_c4/PREREG_MISS_READING_V001.md`, 6aecf0cb; unsealed; no target opened).
- **Tiers:** INVALID_AS_MISS, HIT, NEAR, MISS, from frozen LADDER fields.
- **Zones:** < 10, 10–30, ≥ 30 kpc, from A15 wording.
- **Patterns:** P0–P9, all reported.
- **Readings:** two-way (or more) with deciding tests. The withdrawn deciding tests are registered as NOT SCHEDULED, and their readings stay OPEN.
- **Comparison:** against A15, after the score.
- **Open:** its 5 root items, including the pattern thresholds and the NEAR band width. Root rules on them and seals the prereg **before targets are opened**, in the freeze step.

Claude4 next: cross-lineage review of Codex1's NGC N-test evaluators (0536).

## A61: V007 launch concurrency, corrected (2026-10-18 ~13:40Z)

**Error register E-OPS2.** Dispatch 0537 ("launch all 10 at once; about 50–60 GB") used peak RSS figures from R3 runs that had **admitted** route A (C2R3 1.45 GB, C4R3 3.01 GB). Every V007 T-case computes route A with 8 workers.
- Claude3 caught it (FROM_CLAUDE3/0058, TESTED from receipts) before anything launched.
- The model: about 10.5 GB of route-A baseline at 96 nodes, plus about 0.40/0.76 GiB of tail state per worker at K_big 128/256. All-concurrent gives about 89–117 GiB, and 9 of 10 sketched caps would have been hit.

**Ruling (0538).**
- **A route-A token:** at most 3 cases in route A at once, C6T first. Route B overlaps freely.
- RSS caps ≥ 1.5× the modelled peak, with helper C's per-case minimums.
- Monitors and the launcher run detached.

The projected step-2 wall time stays about 9–13 h, labelled UNTESTED.

**Calibration orchestrator v006r6_v002.** Delta review (`review_calib_v006r6_c2/REVIEW.md`): **PASS_WITH_FINDINGS**, 0 blocking. All six earlier findings are fixed, and 208/208 checks pass.
- **F1:** the seal tuple must bind the verdict report's sha.
- **F2:** each check_deciding row is bound to its run identity.
- **F3, deciding test (iii) specified by root (0540):** a **tail-OFF** v010 r5 against v009-GEO two-driver per-call comparison at **each** alternate D, with full-hull brackets, using comparator c2v004, `ended_unix_ns` and the declared custody masked. Evidence is per D: a pass at one D unlocks only that D. These are root launches during calibration prep.
- **F4:** root-invalid resolution is declared disabled for tail-ON.
- Successor v006r7 implements these.

**NGC N-test build finished** (Codex1 0020): N0 bitwise, NQ completed, compare reads N_INCOMPLETE pending N1–N4.
- NQ shows **exactly zero change** under refinement. That is flagged for Claude4 to verify, to rule out an unapplied refinement (0539).
- Codex1 now runs N1–N4 as replays (0539). N3 decides NGC K_big.

## A62: launch packet reviewed; compare items for the final round; disclosures (2026-10-18 ~13:55Z)

**Review.** Claude3 0059 (REVIEW_LAUNCH_PACKET_C3V001, 911440ac) on the 0538 version of Codex1's packet: **PASS_WITH_FINDINGS**, 0 blocking.
- Specs: PASS. They are valid under r5's own validate_case_block at P128 / M_s128.
- Schedule: the token holds route A at ≤ 3.
- Formats: PASS.
- The interlock refuses before any open.

**Packet fixes (0541):**
- seal admission pinned to a root-written SEAL_RECORD;
- the guard at every entry point;
- marker-based path checks;
- superseded producers blocked;
- the launcher bound to its pins;
- the RUNBOOK gets `--gates-only`.

**Failure policy:** one case failing does not cancel the others. New starts halt only on systemic failures (RSS cap or memory kill, disk guard, a refusal that would repeat for every case).

**For the final compare round (added to A54 S9, A56 and A58):**
1. **RB_FP** checks shell-domain coverage. A partial-domain record must not PASS.
2. **SR_K, and every replay gate record, is bound to root-registered producer shas.** A synthetic or fixture record refuses. Identical Δ across K can no longer bias the T1-fail split.
3. **The custody pins move to r5:**
   - driver b5cc62af;
   - RO1 workers fbe9ae79, 869ce387, 0ae245d8, a5277172;
   - binding 86af6198 unchanged.

   These are from the r5 cascade map and are verified from bytes when the r5 check lands.

**Disclosure for the seal record (E5-08).** C5R3 ran the C5H driver and spec except for the label and fs overrides. So the C5R3 route-A fixtures the producers were tested on are very likely equal to C5H's route-A values, E^A included. They are not row values, and A47 I3 holds. Disclosed.

Note: the prereg draft's "S4T: its registered sphere tail" means sphere truncation with a cylinder tail.

**Steps 5–6 prep, reviews about 13:48–14:21Z:**
- **NGC N-test evaluators** (Codex1): Claude4 0065, **PASS_WITH_FINDINGS**.
  - NQ's exact zero is **genuine**. The NGC lnN resolution is one N step, 3.3e-8 θ, and the converged tail moves about 1e-6 of a step.
  - GQ_NGC becomes a required input (0544).
- **Freeze v003f** (Codex3): Claude4 0067, **PASS_WITH_FINDINGS**. B1 (roster binding) and the rest are closed, and the gap and cut rows match an independent oracle.
  - v003g binds the declared alternatives to slots V002, binds radii by query id, and checks Rad_unit (0545).
  - **Freeze procedure ruled two-pass:** raw results first, then cut records from v011, then root registers the roster, then a replay evaluation (F5).
- **Stage 0:** all 8 chains finished (C5 at 6.8 h). Analysis v003 auto-runs. Off the galaxy-run path.

## A63: stage-0 outcome and its galaxy-run handling (2026-10-18 ~14:26Z)

**Analysis v003** (`runs_ext/STAGE0_ANALYSIS_V003/`, 8/8 complete): **S0-FAIL-RHAT**, TESTED-NEGATIVE as sealed.
- max R-hat 1.48; 95 of 778 columns have R-hat above 1.1.
- R-LIT and R-MA fail.
- The background passes.
- Wiring: **WIRING_CHAIN_SPECIFIC**, which gives the frozen-wiring reading. P-96 needs a root decision (a rewiring move, or a graph-ensemble estimand) before any L = 6 capture. Per the principal, that is **not** pursued during the galaxy run.

**The registered k = 0 lapse drift reading is SUPPORTED.** Its precondition holds: census/U is flat in all 8 processes.
- stage-0 |h_NN(0)| = **1.90 ± 0.11**, against A2's **3.551**;
- that is below A2 − 2 SE, so drift inflated A2's magnitude.

**Galaxy-run handling, per the sealed row:**
- **A2 (2e3a36d8) remains the baseline coefficient grid.** The stage-0 grid is a start-balanced, graph-ensemble **sensitivity grid only**, with a process-jackknife band, and never a replacement. It is offered for the NGC outer rows **if it is convexity-admissible**. The gate is running (`stage0_grid_gate_c2/`).
- If it is admissible, root decides, before any target is opened, whether to register it as an NGC outer-row **sensitivity alternative** in the freeze. Such an alternative is scored separately from the headline.
- **Either way,** the freeze manifest and the miss-reading prereg disclose the SUPPORTED drift reading. That gives a further registered reading for outer-row misses: A2's k = 0 entry, which enters the k → 0⁺ transfer under CA-34, is drift-inflated.

## A64: NGC N-test preliminary diagnostics; C1′ scope; NGC K_big rule (2026-10-18 ~14:40Z, NGC targets unopened)

**Codex1 0025/0027, TESTED diagnostics; the formal replays are pending.**

| Test | Preliminary result |
|---|---|
| N1 at K_big 16 | TRUNCATION_SHAPE ordinal 15: S/θ = **1.015**, just above θ. Without the tail these rings were 1.1–3.7. |
| N3 at 16 | 8 against 16: **0.75 θ** (above θ/4). 32 against 16: 0.14 θ. ΔS < 7e-8 θ. |

**Rulings (0546):**
1. **C1′ applies only on NOT_GRID rings (A17).** C1 is kept on TRUNCATION_SHAPE and QUADRATURE_LIMITED rings.
2. **NGC K_big.** If the formal N3 at 16 confirms the lower-pair failure, **NGC production K_big = 32**, with **N3′ = {16, 64} against 32**. N1, N2, N4 and NQ are evaluated at 32. EPS, LO_NGC and GQ_NGC coverage must be ≥ √2·64 ≈ 91 /kpc; if GQ_NGC at M_s 96 does not hold there, root rules on M_s 128. The K_big 32 and 64 replays start now, in parallel.
3. N1 is read only on the production-K_big records.

**Formal N3 at 16 (Codex1 0029, about 14:41Z): TESTED fail.** The 8-vs-16 pair gives ΔdL/θ = 0.749, and 32-vs-16 gives 0.137. K16 equals the NQ base bitwise, and all the cubes cite identical stored kept bytes.
- **NGC production K_big = 32 is now in force.**
- N3′ = {16, 64} against 32. N1, N2, N4 and NQ are evaluated at 32.
- The EPS and LO_NGC certificates to 91 /kpc are being built (`certificates_ngc_k32/`). GQ_NGC to 91 at M_s 96 is with Codex1.

## A66: the N1 consequence (2026-10-18 ~14:55Z, NGC targets unopened)

**Fact (Codex1 0031, TESTED).** N1 fails strictly at one ring.

| Item | Value |
|---|---|
| Ring | TRUNCATION_SHAPE ordinal 15, R = 10.54 kpc |
| S/θ at K_big 16 | 1.0148 |
| S/θ at K_big 32 | 1.0148 |

S/θ is unchanged by K_big, so the residual comes from the **kept-cube (K = 2) corner shape**, not from the tail. The other TRUNCATION_SHAPE rings pass. Without the tail these rings were at 1.1–3.7 θ (A14 C4 / A17).

**Disclosure.** R1 names N1's outcome (N_FAIL_N1) but not its **consequence** for the NGC step. This ruling is made **after the N1 diagnostic was seen**, and is labelled as such. It follows the A14/A17 precedent: every k-grid failed C1 on these same TRUNCATION_SHAPE rings (S/θ 1.1–3.7), D-SPLIT classed them as cube-corner numerics, and NGC construction proceeded with that disclosed.

**Ruling.**
1. **The N-test reading is decided by the compare as registered.** If N1 fails, it reads N_FAIL_N1, which is never relabelled a pass.
2. **N_FAIL_N1 confined to TRUNCATION_SHAPE rings does not block NGC route A/B.** Route B consumes the azimuthal mean (rotation v005 L266; A42 TESTED), so the φ-spread S does not enter any row directly.
   - Every NGC row whose radius lies within the radial support of a failing TRUNCATION_SHAPE ring is flagged **TRUNCATION_SHAPE_RESIDUAL** in the freeze manifest. This is a disclosure, not INVALID, with the measured S/θ.
   - The miss-reading prereg adds a reading: a miss on such a row may reflect the residual cube-corner anisotropy.
3. **A failure of N0, NQ, N2 or N3′, or an N1 failure on a ring that is *not* TRUNCATION_SHAPE, blocks NGC route A/B.** Root then rules on a next step.
4. The stricter alternative, letting N1 block NGC entirely, is rejected. Under A14/A17 the same cube-corner residual was accepted, at much larger S, for the construction now in use.

## A67: compare r7 and the last round, r8 (2026-10-18 ~15:00Z)

**r7** (`v007_compare_c2/r7/`, compare 528dd23a): the order and validity rechecks both give **PASS_WITH_FINDINGS, 0 blocking**. It implements A54 S9, A56, A57, A58 and A62.

**Rulings for r8, all stricter where the text is silent:**

| Item | Ruling |
|---|---|
| SF1 | The GQ all-nodes check must use the **root-registered per-geometry production node counts** from the gq_full part records. A record whose all_nodes count equals the 4096 sample refuses. |
| SF2 | Restate the IMPL's UNTESTED list and NEW-45/47. **GQ_CERT_V005_MS128 (fbceefe6)** is the GQ record of record (PASS), and V004 is the FAIL control. Both go into the real-record check. |
| N1 (identity) | Every identity run must carry **driver_sha256 = the v010 r5 sha** (defence in depth for A55.3). |
| N2 (SR_K) | The **gate-record shas of record** are registered in the producer registry, as well as the producer shas. A bitwise-identical Δ across K is an SR_K RECORD_DEFECT. |
| N3 (RB_FP) | The shell range must be exactly [K, √2·P]. Excess or shortfall refuses. |
| N4 (EPS) | The top-level and nested "dominates" flags must agree. A disagreement is a RECORD_DEFECT (A54 S5). |
| NEW-31 | A C4T-KHI B4 gap whose Picard members reach the floor reads UAIF PROVISIONAL, as implemented. It is undecidable and adopts nothing. Accepted. |
| Float-floor note | Kept as UNTESTED. Its deciding test is the late-pass increments of the first real 12-pass member. |
| order N1 | FIELDS text corrected: an unregistered record reads NO_RUN (A48 AMB-02). |

**Seal-time pins** (left None until the seal): PIN_ADDENDUM_V005 (at the freeze), PIN_V010_R5_CHECK (when the r5 check passes), PIN_PRODUCER_REGISTRY (the root-registered producer and record shas).

Claude3's distinct r7 order regression (`review_v007_compare_c3/r7/`) is read before the seal.

**Identity reruns on r5 launched at 14:56Z (root).** Driver v010 r5 is **b5cc62af**. Its own dry runs pass 25/25 with 0 blockers, the identity specs included. Its independent check is still pending.

| Run | Spec |
|---|---|
| UVT_Z2_A2F10_R5_RUN_V001 | 2d5e79d0 |
| UVT_Z2_OFF_RO1_A2F10_R5_RUN_V001 | 894e5b3a |
| UVT_B0P_RERUN_ADMIT_PREFIX_R5_RUN_V001 | 4ac5527a |

Monitor ba031c23. Caps: wall 43,200 s, RSS 16 GiB, output 32 GiB. No retries. Detached.

## A68: certificates_v003 and gates_v004 results (2026-10-18 ~15:10Z)

**certificates_v003: PASS_WITH_FINDINGS.** Independent check by own code, with an exact composite-GL reference.
- **GQ at M_s 128 against 256 passes on all 1.8e10 production nodes.** The maximum is 1.8e-15·P0, and the roster-free bound is ≤ 3.15e-14. The M_s 64 canary fails, so the gate has power.
- **LO at the M_s 128 source passes:** largest shell 3.95e-4 τ at (128,256], sum 8.88e-4 τ. The M_s 64 → 128 shift is ≤ 7.5e-12 τ, which settles Codex3's CX3-C3.
- **EPS does not depend on M_s.** EPS_CERT_V006 stands.
- **Slot pair for the P128 MS128 specs:** EPS_CERT_V006 (598c8fa3), **LO_CERT_V003_MS128 (9fdb897a)**, **GQ_CERT_V005_MS128 (fbceefe6)**.

**Rulings for the compare round after r8, stricter:**
- **CHK-1.** g_GQ and g_LO compare each certificate's **M_s with the registered uv_tail gas.M_s** of the case block. A superseded M_s 64 certificate must refuse in an MS128 context.
- **Records.** Every certificate record carries an explicit `source_gas_M_s` (Codex1 0023). A successor LO record (LO_CERT_V004_MS128 = V003 + that field, numbers unchanged) is issued, and GQ/EPS records state M_s where they depend on it.
- CHK-2 is covered by A67 SF1.

**gates_v004:** the R-PAIR member specs PASS (18/18 leaves; the C5H ROUTE_A B0 holds; 10/10 negative controls). Picard members are fillable only after their bases run, as designed.

**Comparator c2v004: FAIL**, on 10 of 29 independent must-fail canaries.
- **B1, blocking:** stage-number normalization collisions hide extra or tampered stage directories.
- **B2, blocking:** RESULT compares only 5 keys.
- **S1–S4, should-fix:**
  - S1: repeated tail flags;
  - S2: Z2 tail argv not tied to stage kinds;
  - S3: inputs/*, finish.json and the route-A attempt result.json not content-compared;
  - S4: the fill-tool C5H guard can be bypassed with a symlink.

**Ruled:** successor **c2v005** closes B1, B2 and S1–S4. It compares the full result.json with only declared keys masked, and it detects extra stage directories by real path and content. An independent check uses its own canaries. The **r4 and r5 identity comparisons are rerun with c2v005**. The A59 Z2 replace-mode tokens are derived from r5.

## A69: Claude3's distinct review of compare r7 (2026-10-18 ~15:05Z)

**Source.** Claude3 0062, REVIEW_V007_COMPARE_R7_C3V001 (3e4eafb3): **PASS_WITH_FINDINGS, 0 blocking, 0 should-fix.**
- Every ruling through A62 is implemented as ruled.
- Fuzz of 5000 histories: 0 mismatches.
- 34/34 new probes pass.
- Every hunk maps to a declared item.

**Notes ruled, for the round after r8 if r8 lacks them (stricter):**
1. **A62.2.** The producer registry carries **producer paths, and the compare hashes the producer bytes**, not only the claimed sha.
2. **A62.1.** Shell coverage must start at **lo ≥ K = 4**. This is already implied by A67 N3's exact [K, √2·P].
3. **AMB-07.** On an exact tie in (E + E^A)/τ, the R-PAIR branch row is the **lowest row index**. The tie-break is deterministic.

**Driver r5: Codex3's cross-lineage review (0602), PASS_WITH_FINDINGS, TESTED.**
- The module is cap-only.
- The mapped successors and the driver change are pin-only.
- The reachable closure is complete, with zero stale runtime pins.
- Tail-ON builds are bitwise equal to r4: 35/35 arrays and jets.
- **Finding:** one unreachable pin-only successor is missing from CASCADE_MAP, so the literal map is incomplete while the runtime closure passes. **Ruled:** an immutable inventory addendum, CASCADE_MAP_R5_ADDENDUM, is written before the seal. The r5 identity runs launched at 14:56Z stand.

## A70: certificate slots for the V007 specs (2026-10-18 ~15:15Z, dispatch 0555)

| Slot | Record |
|---|---|
| EPS | **certificates_v002 EPS_CERT_V006 (598c8fa3), retained.** It is M_s-independent, TESTED in A68. |
| LO | **certificates_v004 LO_CERT_V004_MS128**: the V003 numbers plus `source_gas_M_s: 128`. Pending the A68 workflow. |
| GQ | **GQ_CERT_V005_MS128 (fbceefe6)**, or its v004 successor if one is issued. |
| NGC (K_big 32) | certificates_ngc_k32 (EPS to 91 passed Codex1's admission test; LO_NGC to 91 pending). |

This supersedes 0532's "slots under certificates_v003".

**Cross-lineage results:**
- **Codex3 0603** on the certificates: GQ PASS_WITH_FINDINGS (86/86, bound 1.65e-14); LO numerics reproduced. The original LO record fails only on the missing source_gas_M_s.
- **Claude3 0064:** r7 blinding and order regression clean.
- **Orchestrator v006r8** (Codex2 0435) binds the re-anchor to the A2F10 anchor. Its delta review is running.

**Comparator c2v005: Codex2's cross-lineage review (0436/0438) is FAIL, blocking.**
- A normalized-dictionary key collision is resolved last-wins, so a tampered added result field passes bitwise.
- Should-fix: structured-dtype identity, duplicate JSON keys, duplicate NPZ members, and a race between hashing and re-reading checkpoints.
- **Ruled:** successor **c2v006** rejects collisions recursively and FAILs on duplicates, compares dtypes exactly, and hashes and compares from a single read. It gets its own independent canary check. The identity-gate records for the seal are produced with c2v006.

**Freeze v003g:** Claude4 0071 gives a full **PASS**. Step 6's freeze code is ready.

## A71: no last-wins anywhere (2026-10-18 ~15:35Z)

**Finding (Codex2 0441, TESTED on compare r8).** An LO record with a failing [4,5] shell followed by a passing duplicate reads **PASS**. Reversing the order reads RECORD_DEFECT. A failing extended shell can be hidden the same way. The cause is `_shells` building a dict keyed by range with last-wins.

This is the same bug class as c2v005's normalized-key collision (A68) and A54 S9's duplicate pass rows.

**Ruling: a systematic rule for the compare and every gate tool.** **Any list-to-mapping conversion, and any JSON object, rejects duplicate keys before the mapping is built.** That covers shells, rows, cases, gates, members, tokens, registry entries and the JSON parse itself (object_pairs_hook). A duplicate is a RECORD_DEFECT naming both entries, and no tool may be last-wins anywhere.

The final compare round:
- audits every dict-from-list site in code, lists each one in the IMPL with its guard, and tests each;
- also implements A68 CHK-1 (certificate M_s bound to the registered gas.M_s) and A69 (producer-byte hashing, lo ≥ K, deterministic tie-break).

## A72: tail-table caching to shorten the V007 long pole (2026-10-18 ~15:45Z, before any T result)

**Problem.** C4T-KHI (K_big 256) is projected at about 28 h solo (UNTESTED cost model). It is dominated by repeated cold tail builds in route-B stages, and parallelism across cases cannot shorten that single chain. A source-independent part of each build (the "warm" saving, about 2.8× at K128) is recomputed in every stage process.

**Principal:** "IF we can save time by caching we should do it."

**Ruling.**
1. Build tail-module successor **v003**. It adds an optional, content-addressed, sha-verified on-disk cache of the source-independent tables.
   - The cache is **bitwise exact**: hit, miss and cold builds give identical bytes.
   - The cache-disabled path is byte-identical to v002.
   - A **pin-only cascade** leads to **driver v010 r6**, following the A55 precedent.
2. **Adoption is conditional on three things:**
   - (a) the independent check passes, including stale-cache attacks;
   - (b) bitwise equality is TESTED at K_big 32, 128 and 256;
   - (c) the measured timings (`kbig_timing_v003/`) show a **net** saving after the cost of the cascade, its review and an identity rerun.

   If any of these fails, V007 seals on r5 as planned.
3. **If adopted, the sealed driver is r6.**
   - The identity runs are rerun on r6, with caching enabled where the tail is ON.
   - Every V007 T-case runs with the cache, so they are compared on equal footing.
   - The r5 identity runs (14:56Z) are then superseded and kept.

**Launch packet final: Claude3 0065, PASS_WITH_FINDINGS, 0 blocking.**
- Before the seal, all 254 entry points refuse.
- The 10 filled specs carry the registered content, and compare r8 accepts their case block.
- The LO slot is v004 LO_CERT_V004_MS128 (1c384f76), with source_gas_M_s 128.

**ITEM3-R1, ruled (0559).** The 0551 adaptive rule admitted 6 cases within 15 s, before their memory was realized: modelled peaks about 130 GiB. Admission is now **ramp-gated**: the next case starts only after the previous case completes its first route-A iteration **and** free memory is ≥ 25% with fewer than 6 in route A. KHI starts immediately.

**Also ruled (0559):**
- **H-01:** root creates the admission config with exclusive create at the seal; its sha goes in the seal record and is verified by the RUNBOOK; every record embeds its pins.
- **H-02/H-03:** validate() is called in worker() and on every post-seal path.
- **H-07,** for the compare's final round: c5h_path_hit must also catch /.vol paths and hard links, by inode/realpath.

**Compare final round (about 15:50Z).** The r8 loop's round r9 had started without A68, A69, A71, Codex2 0442 or H-07. It was **stopped**, and r9's partial bytes are kept, superseded and unused. The final round, **r10** (wf_17521c7f), is built from r8 and implements all of these, including the A71 dict-from-list audit. It has two independent rechecks, plus at most one fix round (r11). Claude3 gives the distinct review (0560). Codex2's r8 review (0442: FAIL on B1, plus S1) is used as a regression input.

## A73: comparator c2v005 checked; certificates v004; the A62 pin correction (2026-10-18 ~16:10Z)

**certificates_v004: PASS_WITH_FINDINGS, 0 blocking.**
- LO_CERT_V004_MS128 (**1c384f76**) is V003 plus 6 keys. The other 35 keys have bit-identical floats. `source_gas_M_s` = 128.
- **F2, for the compare:** source_gas_M_s must also equal the record's own gas_M_s and tail_config gas.M_s.

**Comparator c2v005.**
- **Build:** the r4 identity reruns are **PASS_BITWISE_EQUAL** (Z2 23/23, Z2_OFF_RO1 23/23, B0P 18/18). It compares every non-log file by content. Script custody is checked from bytes. Self-test 183/183, including all of c2v004's 29 must-fail canaries.
- **Independent check: FAIL**, on A71. The JSON parse, normalized keys and token list are last-wins. Successor c2v006 is already building to fix this (wf_a088aed1). The checker reran Z2 r4 itself and got the same verdict, byte-identical.
- **Should-fix, ruled for c2v006 (or c2v007 if c2v006 lands without them):**
  - SF1: the RO1 block is checked on its full key set.
  - SF2: **tokens bound to the A59 driver derivation.** Only derived [ref, new, token] triples are honoured. A token that could rewrite verdicts or values refuses.
  - SF3: the static_pin_verifier admits only the selected driver's table entries.
  - N3: firmlink (/System/Volumes/Data) and NFD aliases are caught in the containment layer.
  - N6: the r5 command script checks receipt status, and each verdict is read.

**Correction to A62 (errors register).** A62 listed 0ae245d8/a5277172 as the r5 RO1 NGC workers. From r5 bytes, those are the **nodes_v001** workers. The r5 **NGC RO1 workers are b6c4586d and ee0510df**. The DDO RO1 workers fbe9ae79/869ce387 and the binding 86af6198 stand. The compare's final round and Codex1's packet use the corrected set.

**Error register E-OPS3 (about 15:55Z).**
- **What happened:** the r10 workflow (wf_17521c7f) built nothing. Its apply agents treated the build as outside the principal's latest chat question (a timing question) and returned only a timing note. Its rechecks then correctly refused to invent a round. No r10 or r11 exists. The partial r9 is still superseded.
- **Relaunched as wf_97099de8:** same task, plus an explicit authorization and task-ownership preamble. About 10 minutes were lost.
- **Lesson:** every workflow brief states its authority and ownership explicitly.

**Calibration orchestrator v006r9** (Codex2 0439). Delta review `review_calib_v006r9_c2/REVIEW.md`: **PASS_WITH_FINDINGS, 0 blocking, 0 should-fix.** 140/140 probes pass.
- V8-F1 is closed: the deciding rows' numerics are bound to config.numerics.block, and 34 deviations refuse.
- Notes: certificate slots are left to the certificate registry; the block itself is guarded by the sealed V007 ADOPT.
- **Step 4 is ready**, pending the V007 adoption, the per-point certificate approval and the root launches (TAIL_REANCHOR, deciding rows, corners).

**DOUBLING, DDO half:** PASS at K_big 128 and 256 on saved C4R3 le3, max 4.7e-13 τ (roundoff). It was independently recomputed, so the 128→256 movement is genuine K_big content. **The record format is pending:** a merged FIELDS_R7/R8-shape record with ddo_K_big_inverse_kpc {128, 256}, ddo_gas_M_s 128, and the NGC half (ngc_operator_sha256 e6453d52, ngc_max_change_over_theta from Codex1's NQ at K_big 32). It is assembled in the seal-assembly step.

**Seal-time record states** (from r7 IMPL; Claude3 0062): GQ_CERT_V003 (no all_nodes), LO_CERT_V003_MS128 (no source_gas_M_s), the c2v004 identity records and unregistered gate records all read RECORD_DEFECT until they are re-emitted. The re-emission is in progress (A68: certificates_v004, comparator c2v005).

**Launched before the r5 check passed**, to save about 2 h on the critical path while compute was idle. If the check changes any r5 byte, these runs are void and rerun on the corrected driver. They are compared with comparator c2v004 and the r5-derived replace-mode Z2 tokens (A59).

**Calibration certificates (Codex2 0431).** The per-point certificate producers are built: point custody, EPS/ρ, prelaunch and current LO, GQ (full example 20,736 nodes at M_s 128/256, bound 3.1e-14), I1-T, and state enumeration, all failing closed. This is a producer build, not a production pass. A Claude-lineage review is queued.

## A74: comparator c2v006 early findings; c2v007 design; the NGC RO1 guard (2026-10-18 ~16:18Z)

**Codex2 0445, early findings on c2v006 (TESTED on its own whole-gate fixtures, review continuing):**
1. **NPY headers are parsed last-wins** (`ast.literal_eval` before any key check). A duplicate `descr`, `shape` or `fortran_order` reads PASS.
2. **Token-label normalization is not injective.** One pair labelled `<X>|<Y>` and another pair given both labels `<X>` and `<Y>` normalize to the same text. A changed result string then reads PASS on every check.
3. **Repeated identical declared triples** are silently deduplicated, and NO_LAST_WINS still reads PASS.
4. **Attempt-ledger alias (0446).** `ATTEMPT_RE` ends in `$`, which also matches before a trailing newline. A tampered `cx2token.start.json` and its newline-suffixed alias then group to the same key, last-wins, and the comparison reads PASS. The c2v007 fix is fullmatch plus a grouped-key collision check before any inventory entry is removed, with both raw paths named in the defect.

**c2v007 build:** wf_17f396c8 (3 independent check lenses plus one fix round). **NGC cx3r005 (f85746f0):** Codex3 0607 reports TESTED PASS. Its distinct review is wf_3d89783d.

**Ruling: successor c2v007,** with the smallest possible parse-and-normalize surface.
- **Equal bytes first.** Every file is compared by raw sha256. The only exceptions are a closed, declared list of files known to differ: records that carry run paths, timestamps or the driver sha.
- **Declared files** are parsed strictly. JSON uses object_pairs_hook; NPY/NPZ headers go through a dict-literal AST, rejecting duplicate keys before evaluation. A duplicate is a RECORD_DEFECT even when its values are equal (A71).
- **Tokens** come only from the A59 driver derivation (A73 SF2).
  - Labels follow the closed grammar `<[A-Z0-9_]+>`, with no delimiter characters.
  - Each [ref, new, token] triple appears exactly once; a repeated triple is a RECORD_DEFECT.
  - Normalization must be injective, and this is TESTED with Codex2's 0445 constructions as must-fail canaries.
- **Also in c2v007:** A73 SF1, SF3, N3 and N6, plus anything Codex2's final 0564 review or the c2v006 workflow's own checker adds before the build closes.

The r4 identity pairs must still read PASS_BITWISE_EQUAL under c2v007. The r5 pairs are compared with c2v007 once their receipts exist.

**Codex3 0605, NGC RO1 guard (TESTED).** In the active NGC v011 context (cx3r004, 39c50517), the shared `ro1_outcome` accepts a union of worker hashes that includes the nodes_v001 workers. Synthetic records carrying a nodes-worker hash fire RO1 in both the headline and Stage0 contexts. The NGC worker that is actually selected is correct, so no production result is affected.
- **Correction:** Codex3 is building immutable wrapper **cx3r005**, which restricts the NGC context to its selected NGC worker and binding pair (A73 shas).
- cx3r005 needs a distinct review before any NGC route A/B run (step 5). It does not gate the V007 seal.

**Binding precision (corrects A73's wording; verified from bytes).**
- The NGC RO1 workers b6c4586d/ee0510df use binding **52dc4065**.
- Binding **86af6198** belongs to the DDO RO1 workers (fbe9ae79/869ce387) and to the nodes_v001 workers (0ae245d8/a5277172).

Codex1's packet already carries the correct set (0043). Codex3's audit (0606) found no active code using the wrong pair. The two frozen A65 snapshots that repeat A62's wording are left as historical bytes, with an erratum.

## A77: NGC v011 cx3r005 reviewed; RO1 role binding in the V007 compare (2026-10-18 ~16:44Z)

**Distinct review of cx3r005 (f85746f0), wf_3d89783d, `review_ngc_v011_cx3r005_c2/`: PASS_WITH_FINDINGS on both lenses, 0 blocking.**
- **Source:** the change is a single pure insertion of 1308 bytes; removing it reproduces 39c50517.
- **Guard lens:** 14,000 synthetic rows. In the NGC contexts, RO1 arms only for the selected V011 worker with V011 binding **9b5ce82a**:
  - headline ee27227c/293a417f;
  - Stage0 f7c8fb43/908c9b4b.

  Every cross-role, hash-trick and path-variant record refuses.
- **Parity lens:** dry plans are byte-identical across 78 specs (234 runs). Exactly 4 arming cells change (nodes worker plus 9b5ce82a, in both NGC contexts).

**Correction to A74's wording (GC-N1).** The NGC contexts arm on the **V011** workers above with binding 9b5ce82a. These descend from the r5 NGC workers b6c4586d/ee0510df with only LOCAL lines changed. 52dc4065 is the r5 parent's binding, and it correctly refuses in the V011 contexts. No future fix may point the V011 contexts at 52dc4065.

**Ruled:**
1. **GC-S1, should-fix.** Inside the NGC contexts, start.json and the result records are read last-wins (inherited from r004). Codex3 builds **cx3r006**:
   - read those records with a duplicate-rejecting object_pairs_hook, and refuse to arm on any duplicate;
   - also type the two inherited TypeError paths (GC-N4, N6) as refusals.

   cx3r006 gets a delta review. NGC route A/B launches **only** from the cx3r006 registry, or from cx3r005's (47023c27) if cx3r006 is not ready. Never from the old r004 registry c5abc2d5 (GC-N5). Root verifies the full driver sha from bytes before each NGC launch and checks the result's driver_sha256 afterwards (N8).
2. **N7, the generic context (V007 DDO RO1).** The r5 driver's generic RO1 guard accepts the cross-role union: a DDO worker with the NGC binding arms. The r5 driver is **not** changed: that would cascade a rerun of every identity gate, and honest workers cannot emit cross-role records. Instead, **the V007 compare enforces the role table** on every RO1 record it reads:
   - worker_pin ∈ {fbe9ae79 serial, 869ce387 parallel} with binding 86af6198;
   - serial/parallel matches the case's column_workers;
   - the record is parsed strictly (A71).

   Any mismatch is a RECORD_DEFECT. This is added to the A75 closure list for the final compare round.

**A77.2 made precise (Codex2 0451, ~16:48Z).** The role table is **per case, keyed by the case's registered route family**. It is not one global DDO pair.
- **DDO cases:** fbe9ae79 (serial) or 869ce387 (parallel), with binding 86af6198.
- **C4T-D5 and its R-PAIR member** (the registered nodes_v001 source, r8 L183–193, L1475–1482, L1907–1909): the nodes_v001 workers 0ae245d8 (serial) or a5277172 (parallel), with binding 86af6198. This registered exception is kept, and it is not invalidated.
- A worker from another family, or a binding from another family, is a RECORD_DEFECT.
- **Serial or parallel** is checked against the **admitted attempt's** column_workers.
  - For T-case Picard members this is the base's admitted attempt, per A53 (member RO1 equals the base canonically), **not** the member's planning-only column_workers = 1.
  - A77.2 adds a check and overrides nothing in A53.

## A102: r12 reviews split; r13 closes A-B1 (2026-10-18 21:22Z)

**Codex2's r12 delta (0485): 0 blocking.**

**Claude3's r12 delta (`review_v007_compare_c3/r12_review/REVIEW_V007_COMPARE_R12_C3V001.md`): FAIL, 1 blocking.**
- **A-B1:** under `-I`, an integer literal longer than 4,300 digits raises a plain ValueError **before** the duplicate hook fires. `check_record_codes` (r12 L875–879) then falls back to the text test and admits a duplicate-key record. The same path is reached through driver_build_codes, activate_driver_build, every CLI mode and the seal-time built-in path, across 7 forms.
- It is not a regression (r11 behaves the same), but it is a residual of the A91.1 defect class.
- **Everything else in A91.1, A91.2 and A88 is confirmed TESTED,** with mutation teeth, and the change scope is exact.

**Ruling.** A81 RI-20 requires 0 blocking from both reviews of record. **Codex3 builds r13 = r12 plus exactly this fix** (0629):
- parse with `parse_int=str` inside the duplicate-hook parse;
- **and** fall back to text **only** on `json.JSONDecodeError`, refusing on any other ValueError, including the digit limit.

Every A-B1 form (V01–V07) becomes a MUST_FAIL test. Nothing else changes. **Claude3 and Codex2 delta-check r13.** Prereg r5's compare slot (PENDING_ROOT) takes r13 once both reviews report 0 blocking.

## A101: B2 record of record; registry V008 (2026-10-18 20:48Z)

**B2_GATE_RECORD_C3V003 (915fbcda): PASS** on r11 and r12. **Codex2 delta (0503): PASS_WITH_FINDINGS, 0 blocking**, with 319 numerical checks. The sanity values match A100.
- **Its two documentation should-fix items do not affect the gate:**
  - C3V003-RI-1 attributes GL6/0.25 to 0622 in error;
  - "≤ 3.8e-11" is not a valid bound on 3.832e-11 and should read ≈ 3.83e-11.
- **They are carried as an erratum in the seal record's disclosure block, not by re-issuing the record.** Re-issuing would change the record sha and force another registry round, with no gate effect.

**The V007 case block:** CASE_BLOCK_V007_C4V001, **76309ae3** (Claude4). **Codex2 0507: PASS, zero findings.** The ten filled specs bind the ten T entries plus the C5H declaration, and all ten tail hashes reproduce. It is pinned as `binding_inputs.case_block` in prereg r5.

**Step-5 open item closed (A90).** Codex1 0066 ran the independent tail-domain star-transform convergence for the NGC LO I1-T precondition: **TESTED PASS.**
- 442 radial nodes to 91 /kpc, with stars and H2.
- Doubling max relative 8.1e-16; production against an independent transform 9.7e-16, against a 1e-10 limit.
- The missing-H2 and under-integrated controls fail as they should.

**Producer registry V008, Claude3 0084: final.** All 13 registered records PASS on r12. BUILD_V007's post-seal producers are added when BUILD_V007 lands, as V009.

## A100: B2 is disposed under A97(a) (2026-10-18 20:24Z, before any T result)

**Evidence: two independent lineages, both TESTED.** Codex2 0496 and Claude3 0082 agree to ≤ 2e-9 km/s. Claude3 read Codex2's result only after saving its own tables.
- **ADV is reproduced exactly** by Claude3's equivalent code on ADV's own states.
- **Shared inputs (state, gas source masses, profile, forward, binding, adapter):** identical. **Neither lineage found a production or shared-input error.**
- **Attribution at the worst row** (row 08, P16):

  | State | Gas rule (unnamed) | Total B2 − ADV |
  |---|---|---|
  | C2R3 | +0.0790 | 0.0821 |
  | C3R3, on le3 | +0.0954 | 0.0951 |
  | C4R3 | +0.1114 | 0.1083 |

  Readout, quadrature and implementation contribute ≤ 3e-7 km/s.
- **The unnamed difference is the gas rule.** ADV uses discrete rings J0(kR_i)E_i, while B2 uses the registered continuum_v001.
- **Named-only residuals:** B2 minus the like-for-like reference, with every unnamed difference switched to production, maximum over rows.

  | Reading | Statistic | C2 | C3 | C4 |
  |---|---|---|---|---|
  | (i) roster only | P16 | 3.9e-5 | 4.4e-5 | 4.5e-5 |
  | (i) roster only | m0 | 0.0104 | 0.0210 | 0.0260 |
  | (ii) star representation + roster | P16 | 0.0301 | 0.0356 | 0.0384 |
  | (ii) star representation + roster | m0 | 0.0318 | 0.0379 | 0.0427 |

  **All 12 values are ≤ 0.05.**

**Disposition under A97(a)**, whose rule was fixed before these results:
- The registered reference broke the text's premise: it differs in the gas rule, which the text does not name. **B2's sanity is read against the like-for-like reference**: ADV's method with production's continuum_v001 gas rule.
- **The 0.05 allowance is unchanged.**
- **Reading (ii) and the text's statistic P16 are the values of record.** Reading (ii) is the stricter one, because it keeps the star-representation term inside the compared residual. The values of record are **0.0301, 0.0356 and 0.0384 km/s**.
- The m0 values and reading (i) are disclosed alongside.

**Claude3 re-issues the B2 record** (C3V003), and Codex2 delta-checks it. The record carries:
- the primary ≤ 1e-4 km/s PASS;
- the sanity values of record, including C3R3 on le3;
- the reference basis;
- the method-wording fix (Codex2's should-fix);
- a **disclosure block** with the raw misses against ADV's saved rows (0.082 / 0.095 / 0.108 km/s, the C3 figure on le3), the gas-rule attribution, both readings, and the fact that ADV's saved C3R3 used le4.

The seal record repeats the disclosure. "Shared physical correctness" is still not proven by B2. Both lineages state this, and the record carries it as a limit.

## A99: the seal rehearsal's rulings (Claude4 0099) (2026-10-18 20:20Z)

**BUILD_V006: PASS_WITH_FINDINGS, 0 blocking, 3 should-fix** (V6-S1 to S3). **Seal rehearsal: SEAL_NOT_READY**, with 3 blocking defects in the seal inputs plus B2 (A97).

**Rulings:**
1. **D-02. The launch-packet BUILD of record is the V006 successor**, written **BUILD_V007**, which closes V6-S1 to S3:
   - V6-S1: non-finite values refuse, and records are serialized before a single exclusive write;
   - V6-S2: RUNBOOK_V007 carries the A85.2–4 items (QoS, internal-SSD outputs instead of External1 runs_ext in the r5 template, caffeinate);
   - V6-S3: the allowlist count is 15.

   Prereg r5, seal tool 3 v002 and checklist B8 bind it. **Owner: Codex1.** If Codex1 has not resumed by 20:35Z, Codex3 takes it. Claude4 delta-checks it.
2. **D-03. Claude4 builds the V007 case block** from the ten filled specs, using the in-process recipe in Claude3's `validate_registry_r11_c3v001.py`. Codex2 independently checks it, and it is pinned as `binding_inputs.case_block` in prereg r5.
3. **Entries after A81. The entry-by-entry table is confirmed.** Prereg r5 lists every entry from A82 to the freeze as either "revised here" or "no change, because …", and the seal record quotes the table.
4. **D-01, D-04 to D-07:** Claude4's seal tools v002.
5. **V6-N2 is already closed in r12.** It sets `GATE_RECORD_SHA_REQUIRED = ()` and adds SR_K to the after-seal set (r12 L338/L341, read from bytes). **V6-N4:** Claude3's registry adds BUILD_V007's post-seal producers.
6. **The A82 hazard was confirmed live:** root writes to the open V005 file break a sealed compare that cites it. Root writes nothing to V005 after the freeze (A82).

## A98: PAR-TB accepted narrowly; miss-reading prereg r2 needs r3 (2026-10-18 20:04Z)

1. **PAR-TB (Codex3 0621/0622).** For the NGC v011 successors (cx3r007 and cx3r008), the enumerated, byte-pinned **diagnostic-only traceback classes** are declared differences:
   - inherited forwarding frames;
   - the relocated main-guard line;
   - selector and cmd_run replacement frames.

   **Their scope:** saved traceback and stderr text, and the result hash derived from those fields. **No** exception is granted for numerical values, rows, validity, exception class or text, refusal reasons, decision branches, or recursion-limit behaviour. Any frame class specific to r008 is enumerated and pinned before closure; there is no blanket waiver.
2. **Miss-reading prereg r2 (Codex2 0490): FAIL, 1 blocking and 1 should-fix.**
   - **The defect:** allowed undefined-sign MISS rows count in Nv/M, so an OUTER zone can be miss-dominated with OUTER_FAILURE true while P1, P2, P11 and every named MISS pattern read false. The INNER-only case is the same, and the C-4 LATE gates can remove a pattern.
   - **Claude4 builds r3** (0619): undefined-sign coverage, OUTER_FAILURE equivalence and late-gate behaviour, all made consistent. Codex2 delta-checks it.
   - This is on the step-6 path, not the V007 seal.

## A97: the B2 sanity clause fails as written. Diagnose it before anything else (2026-10-18 20:02Z, before any T result)

**Codex2 0489, reviewing Claude3's B2_GATE_RECORD_C3V002. All TESTED.**
- **Primary B2 criterion: PASS.** Production static rows equal the independent full-box Cartesian tensor-GL (16 azimuths) to ≤ 1e-4 km/s per row, on all three le3 states.
- **Sanity against ADV_TAIL_CHECK KB12** (allowance ≤ 0.05 km/s for the m16 alias and the star-roster difference): **C2R3 0.0821 km/s and C4R3 0.1083 km/s, so FAIL. C3R3 is INCOMPLETE** (no sanity value), and the record reads RECORD_DEFECT on r11/r12.
- **Should-fix:** the method wording must match the disclosed mean-coefficient nonlinear readout.

**Root's reading.** The sanity check exists to catch an error the independent implementation **shares** with production, for example a common input such as the source rebuild, the stellar profile or the gas rule. It cannot be waved away. Equally, **the 0.05 allowance is not changed after these values were seen** (no edits to gate inputs after results). That leaves two possibilities:
- (i) ADV KB12 differs from production by a difference the text does not name. Claude3's working notes report a different gas rule in ADV. If so, the reference violates the text's own premise that only the m16 alias and the star roster differ.
- (ii) There is a real shared-input or production error, or the named effects exceed 0.05.

**Ruling: decompose before deciding** (0618). Claude3, the builder, and Codex2, cross-lineage, work independently and in parallel:
1. **From bytes,** list every difference between the ADV_TAIL_CHECK KB12 rows and the B2 production rows: gas rule, m16 alias, star roster, quadrature, source inputs, readout, and anything else.
2. **Switch one difference at a time** with computed variants (TESTED), and attribute the 0.082 and 0.108 km/s to each one.
3. **Decision rule, fixed now before the decomposition:**
   - (a) If an **unnamed** difference exists and, once it is removed, the residual from the **named** differences alone is ≤ 0.05 km/s on C2, C3 and C4: the registered reference was mis-specified. B2's sanity reads against the like-for-like reference, which is ADV's method with only the named differences. **The 0.05 is unchanged.** The seal record discloses all of this.
   - (b) If the residual exceeds 0.05, or the decomposition finds a production or shared-input error: **B2 FAILS.** A real defect is fixed before the seal (no T result exists yet), and B2 is rerun. If no fix is possible, V007 cannot reach ADOPT_TAIL and the next step is a named successor.
   - (c) **C3R3:** compute its sanity value the same way. If the inputs ADV needs for C3 do not exist, B2 reads INCOMPLETE and the gap is named.
4. **The seal waits for this.** B2 is a pre-seal gate (A88: PRODUCED_AFTER_THE_SEAL is refused for B0–B3).

## A96: V007 seals on driver r5; r6 deferred; compare r12 frozen (2026-10-18 19:51Z)

**A89 applied.** At 19:51Z the r6 BUILD had still not landed, and its identity runs (about 3 h under load) had not started. r6 cannot be ready without delaying the seal.
- **V007 seals on driver v010 r5 (b5cc62af).**
- The r6 build workflow (wf_5233daa0) was stopped. This frees about 8 cores for step 2 and saves root's usage.
- Its partial bytes in `driver_r6/` are kept, are **unfinished**, and are unused.
- **RI-24 and the conditional cache slot are moot for V007.** Caching for steps 4–5 is decided later, together with the A85.1 parallel-tail result (Codex3 0595).

**Compare r12 frozen (Codex3 0617, 19:49Z).**

| File | sha |
|---|---|
| compare (selected by SELECTED_R12_CX3V001 91aa9747) | **4bd7b262** |
| FIELDS_R12_CX3V002 | 5cc95a06 |
| IMPL | ef0db32d |
| HASHES | 3eb2912d |

Its builder results, all TESTED:
- author suite 706/706;
- real records 70/70;
- mutations 96/96;
- A88 focused 65/65, A88 mutations 41/41;
- A91 focused 103/103;
- an independent check 110/110.

All 15 earlier false admissions now refuse. **The delta reviews of record are Claude3's and Codex2's** (A81 RI-20: 0 blocking each). Claude3 re-validates the registry (V003 and later, with SR_K after the seal) on r12.

## A95: Codex3 resumed; taskpolicy in sandboxes; a threading clarification (2026-10-18 19:46Z)

**Errors register (E-OPS4).**
- **What happened:** A85.2 and dispatches 0595/0599/0603 asked lanes to run under `taskpolicy -b`. Codex3's sandbox refused the call (setpriority EPERM) and waited about 45 minutes for the principal to approve escalation. That stalled r12 and step-5 work from about 19:00Z to 19:44Z.
- **Fix:** `taskpolicy -b` is **preferred, not required**, in lane work. If a sandbox refuses it, the lane proceeds at default priority and says so. It must never wait on a permission prompt for this. The A85.2 rule for step 2 itself stands, as a root step at launch.

**Codex3 0613–0615:**
- r12 now closes 0459, the 0462 NPY key naming, and A88. RI-24 remains conditional on r6 adoption.
- **Step-5 readiness: PASS.** 8/8 dry plans and 55/55 filler checks. The A90 star-transform scope and the other step-5 root items are listed explicitly.
- The parallel-tail study has a process-split candidate (original 256-k stellar batches, with GEMV shapes and serial accumulation order preserved). Its numerics are UNTESTED.

**Clarification (0595).** Six-thread Accelerate is allowed **only as a non-production bitwise measurement** in the feasibility study. Production stays single-thread BLAS, unless a later ruling is backed by a TESTED bitwise identity and its own identity gates.

## A94: B2 follows its controlling text exactly (Codex2 0480) (2026-10-18 19:40Z)

**Controlling text (R1/V002).** B2 covers:
- all **three saved le3 static rows** (C2R3, C3R3, C4R3);
- continuum_v001 and cube 12;
- an **independent full-box Cartesian tensor-GL** with 16 azimuths;
- a per-row tolerance of **1e-4 km/s**;
- a KB12 sanity check at **0.05 km/s**, allowing only the **named** differences: the m16 alias and the star roster.

**Ruling. No substitution that the text does not name.**
1. **Full static rows, not stars only.** If the independent lane uses a different gas rule from the registered one, it must implement the registered rule. A different gas rule is not one of the named differences.
2. **le3 is required for every case.** A historical C3R3 **le4** state does not stand in for le3. If the saved C3R3 le3 state is missing, B2 reads INCOMPLETE and names the missing input.
3. **The statistic is the one the text names.** P16 is not replaced by m0 or by a max-of-two unless R1/V002 names that.
4. **The record states its basis explicitly:** components, variant and statistic. Anything the builder had to interpret is listed for root as a ROOT_ITEM. **Do not resolve it silently.**

## A93: NGC cx3r007 accepted (Claude4 0092) (2026-10-18 19:31Z)

**Claude4's distinct review of cx3r007 (e4f5864a, registry cd30429c): PASS_WITH_FINDINGS.** It reports 0 blocking, 3 should-fix and 14 notes (`review_ngc_v011_cx3r007_c4/`, 74d6cd9e).
- **cx3r007 is accepted for the 8 registered NGC specs.** **SPEC_REGISTRY_CX3R007 cd30429c is the step-5 launch registry**, and r006's registry 3c42ca07 is retired.
- The 3 should-fix items go to Codex3 after r12 and before any step-5 launch. Root checks the full driver sha from bytes before every NGC launch.

## A92: r5 identity gates PASS under c2v007r2 (2026-10-18 19:16Z)

**The r5 identity reruns are all COMPLETED with exit 0:** B0P (end 17:49Z), Z2_OFF_RO1 (18:25Z) and Z2 (18:26Z).

**Comparisons, run by root with c2v007r2** (comparator 052da0fe, its command script unchanged):
- The receipt checks passed for all three runs: FINISHED, COMPLETED, exit 0, retries 0, r5 pin, and result sha from bytes.
- **Z2: PASS_BITWISE_EQUAL**, 31 checks, 0 failing (ac793faf).
- **Z2_OFF_RO1: PASS_BITWISE_EQUAL**, 31/0 (1e012006).
- **B0P_RERUN: PASS_BITWISE_EQUAL**, 26/0 (b6cca143).

**Records of record (A81 RI-21, driver r5), in `gates_v007/r2/records/R5_V001/`:**

| Record | Verdict | sha |
|---|---|---|
| B1 | PASS_BITWISE_EQUAL_EXCEPT_DECLARED | **83e7b067** |
| B1_OFF | PASS_BITWISE_EQUAL_EXCEPT_DECLARED | **3b9ad402** |
| B0prime_RERUN | PASS_RESULT_EQUAL_EXCEPT_DECLARED | **e33af53d** |

**Errors register.** The first attempt (19:13:50Z) passed the receipt checks, then stopped: `mkdir` failed because the parent `out/` did not exist, and the script misreported this as "OUTPUT DIRECTORY EXISTS". No comparison ran. Root created the empty parent and reran at 19:14:12Z. Codex1 fixed the script in a successor (0608/0060).

These records stand provided Codex2's c2v007r2 delta check (0607) reports 0 blocking. If it reports a blocking item, the comparisons are rerun on the successor.

**Codex2's c2v007r2 delta check (0472, 19:19Z): PASS_WITH_FINDINGS, 0 blocking.** B1/A91 and S2 are closed and TESTED, 220/220 actual-main identity cases pass, and the residual notes are non-blocking. **c2v007r2 is the identity-comparator slot (RI-21), and the R5_V001 records are the identity records of record for driver r5.**

## A91: the r12 scope is final; c2v007 digest presence (2026-10-18 18:54Z)

**Codex2's r11 cross-lineage review (0462): FAIL.** It finds 1 blocking item, the duplicate-JSON check_record text fallback (0459, as in A90), and 1 should-fix: an NPY header duplicate names only the archive member. 636 of 652 predicates are met. The A79 eight-marker allowance and the A88 SR_K allowance are honoured.

**The r12 scope (Codex3) is exactly:**
1. 0459, the duplicate-JSON check_record fallback;
2. 0462's should-fix: an NPY header duplicate names the member **and** the header key;
3. A88: SR_K joins the after-seal set;
4. the RI-24 cache fields, **only if r6 is adopted** under A89.

The delta reviews are Codex2's, plus Claude3's delta check. Both must report 0 blocking (A81 RI-20).

**c2v007, B-ID made precise (Codex2 0461).** The identity comparator must **require** `identity_sha256` and `caller.sha256` to be present, with the right types, on both sides, and then verify them. A record that omits either one is a RECORD_DEFECT. The pinned checkpoint producer always emits both, so presence is part of the producer schema. This goes in **c2v007r2 (Codex1)**, together with the rest of Codex2's final c2v007 review.

## A90: compare r11 reviews; NGC K32 N-tests complete (2026-10-18 18:49Z)

**Compare r11.**
- **Claude3, the distinct review of record (0077): PASS**, 0 blocking and 0 should-fix, across three lenses. Every r10 finding and every A79/A75/A77.2/A73 item is closed and TESTED.
- **Codex2, cross-lineage (0459), early: BLOCKING.**
  - `check_record_codes`, `driver_build_codes` and `activate_driver_build` catch the strict-JSON DuplicateKey error inside a ValueError handler and then accept a plain-text PASS token. This is 15 false acceptances across five duplicate variants.
  - **Fix in r12 (Codex3):** a duplicate-key JSON refuses, naming both positions, **before** any non-JSON text fallback, and the legitimate text-format controls are kept.
- **r12 therefore carries:** this item; A88 (SR_K joins the after-seal set); and anything else in Codex2's final r11 review. The r12 delta reviews are Codex2's, plus Claude3's delta check.

**NGC K32 N-tests (Codex1 0056): N_FAIL_N1, tests_read = true.**
- N0, NQ, N2 and N3′ pass (16-vs-32 at 0.137 θ, 64-vs-32 at 0.049 θ), and certificate admission passes. N4 is reported only.
- The one failure is TRUNCATION_SHAPE at ordinal 15 (R 10.54 kpc), with S/θ = 1.0148.
- Under A66 the route A/B gate reads **OPEN**, for the sole reason TRUNCATION_SHAPE_RESIDUAL_ONLY_A66. The A66 consequence applies at step 5.
- **LO_NGC_K32_CERT_V001 (07745bbf) gives coverage to 91.** It is the NGC N-test record. V007 keeps LO_NGC V002 (A87).
- **Open for step 5:** the LO I1-T precondition covers only the stored iteration-0 sources, and independent tail-domain star-transform convergence is **NOT_RUN**. Codex3's step-5 readiness (0594) lists it as a root item, and it is ruled before any NGC route A/B launch.

## A89: measured KHI cost; the A72(c) criterion made concrete (2026-10-18 18:42Z)

**Measured** (`kbig_timing_v003/`, TIMING_V003.json 3e3fb600; r5 module, M_s 128, production quadrature):
- **C4T-KHI full call, solo:** **7.84 h** expected (I = 7, P = 3) and **13.86 h** at the upper bound (I = 32, P = 6). At today's measured wall slowdown the tail portion alone is 10.3–22.5 h.
- **C4T (K128), solo:** 5.2–8.1 h.
- **The 27.84 h preview is superseded.** It doubled the cost for M_s 128, which costs the same as M_s 64; it used 8× for K128 → 256, where 3.3–4.2× is measured; and it counted 32 cold route-B builds, where the plan has 4 + 2P on the critical path.
- **Caching (untested) saves 1.83–2.80 h** on KHI solo, almost all of it on route B.
- **Parallel options available today do not shorten tail builds:** BLAS is forced single-thread, the route-A tail runs in the main process, and the Picard passes are serial.
- I and P were measured on tail-off runs, so the tail-on counts are UNTESTED.

**A72(c), made concrete.** The saving is small compared with the delay it would cause, so:
- **r6 is adopted only if it causes no seal delay.** Its BUILD, bitwise evidence, Claude3's independent check, and the r6 identity runs **with their c2v007 comparisons** must all be complete by the time every r5-branch seal input is complete.
- **Otherwise V007 seals on r5.** In that case r6 may still be used for steps 4–5, after its own identity gates, under a later ruling. Equal footing applies only within V007.
- The A84 speculative r6 identity launch stands, since it is the only way r6 can meet this condition.

**Step-2 estimate revised: about 10–16 h** with core priority (A85.2), set by KHI. It was 18–45 h. Every other case runs in parallel under the ramp gate. UNTESTED.

**A85.1** (the parallel tail build) stays useful: the tail is 3.6–7.9 h of KHI's solo time, and steps 4–5 have tail builds too.

## A88: SR_K is produced after the seal by the sealed producers (Codex1 0054) (2026-10-18 18:36Z)

**Conflict (TESTED from source).** The pinned SR_K producers (sr_k_static v009, aggregate_records v008) run only after the seal by design: producer_guard v008 requires the root seal admission. A67 N2 and A79's NEW-61 required the SR_K record before the seal. A pre-seal run would need a new guard exception, which means more custody machinery and another review.

**Ruling (amends A79 NEW-61 for SR_K only).**
- **SR_K joins the after-seal set.** Its record is produced **right after the seal, before any T-run output is read**. It uses the sealed, pinned producers on the fixed saved C2R3/C3R3/C4R3 states, so it does not depend on any T result.
- A67 N2's binding intent is met through **root-registered producer shas** with producer-byte verification (A69). The registry entry carries the producer pins and PRODUCED_AFTER_THE_SEAL. A bitwise-identical Δ across K is still a RECORD_DEFECT.
- **The compare change:** add SR_K to GATE_RECORD_AFTER_SEAL_ALLOWED. This is a one-line change plus tests, and it goes in **r12** (Codex3), which is needed anyway.
- **RUNBOOK:** root runs SR_K as the first post-seal step, in parallel with the T-run launch, since the launcher is ramp-gated.
- **Effect:** SR_K comes off the seal path. The token stays refused for EPS, GQ, LO, LO_NGC, DOUBLING, B0–B3 and the identity gates.

## A87: missing pre-seal records of record, and their owners (Claude3 0075) (2026-10-18 18:33Z)

**Built (Claude3, 0586): both PASS on r10.**
- DOUBLING_MERGED_C3V001, **ea48ac2b**. DDO 4.67e-13 τ; NGC 0.0/θ.
- PRODUCER_REGISTRY_C3V001, **94d8a528**.

**Gaps and their owners:**

| Record | Owner | Note |
|---|---|---|
| **B2** (independent Cartesian tensor-GL on static rows of saved C2R3/C3R3/C4R3; O = cube 12, 16 azimuths) | **Claude3** (offered), 0597 | A FIELDS-shape record from an independent lane |
| **B3** as a FIELDS-shape JSON | **Claude4**, 0598 | From its own `gate_b3_c4/out/B3_COMPARE_V001.json`. The 465cb3c3 Markdown file is the human report, not the record |
| **SR_K** (pre-seal, A67 N2 / NEW-61) | **Codex1**, 0599 | aggregate_records v008 in mode SR_K, over sr_k_static v009 on the saved C2R3/C3R3/C4R3 states, with the pinned producers |
| **B0, B0prime_DRY, B0_FA, B0_RO1, B0_N3, I4** on the **sealed** driver | **Claude4**, 0598 | FIELDS-shape records from the existing gate outputs: r5 B0 vs r4, 64/64 PASS_PLAN_IDENTICAL, plus the dry runs. Built for r5 now, and for r6 if it is adopted (B0_R6_VS_R5 exists) |
| **Producers for SRB_ROT, MT, I1T and FLAG_RULINGS** | **Codex1**, 0599 | Find the existing producers or build them, then add them to the launch-packet allowlist as a new BUILD (V006). Claude4 delta-checks it |

**LO_NGC in V007:** register **LO_NGC_CERT_V002 (33bc2190)** as the record of record. It reads PASS. Under A81 RI-23 LO_NGC is reported only in V007, and coverage to 91 belongs to the NGC N-test compare.

**Effect on the schedule.** These items run in parallel across three lanes. SR_K is computational. If any of them lands after the compare reviews, it moves the seal.

## A86: compare r11 frozen; its OPEN items ruled (2026-10-18 18:31Z)

**r11 froze at 18:29Z.**

| File | sha |
|---|---|
| compare | **a5d10cb1** |
| IMPL | 2d795028 |
| FIELDS_R11 | c7f0dec6 |
| HASHES | 79e5a029 |

wf_9baf53cd was stopped at the freeze (A83), and its rechecks did not run. **Claude3 (distinct) and Codex2 (cross-lineage) are the r11 reviews of record (0591).** Codex3 owns any r12 (0590).

**Rulings on r11's OPEN list:**
1. **GQ under A79.1.** The record of record, GQ_CERT_V005 (fbceefe6), carries extra rosters with the same names and other geometries, so it reads RECORD_DEFECT under r11. That is correct under A79.1, and **A79.1 stands.**
   - The fix is a **re-issued GQ_CERT_V006**: exactly the on-map subset of V005 (7 rosters, one per name, on the A75.6 fixed map), with numbers bitwise unchanged. It is written by a registered subset producer from V005's bytes.
   - At P = 128 the map covers every T case: C4T_KB256 reaches KHI. The extras are superfluous.
   - Claude3 does this inside 0586 (0596), and the registry pins V006.
2. **The open V005 path.** A82's no-write-after-freeze rule is sufficient. r11 keeps citing the open path, and no change is needed.
3. **RI-24 cache fields.** These are needed only if r6 is adopted. If it is, r12 (Codex3) adds the cache-mode and cache-directory checks, using the field names the r6 BUILD defines.
4. **DOUBLING's NGC K_big.** The compare reads the operator and the max change over θ. K_big 32 is carried informationally, and no change is needed.
5. **NEW-71 to NEW-81** fall under RI-10's adoption rule (A81 RI-20). The reviews of record flag any item that would ease a reading; otherwise each is adopted as declared, and the seal record quotes the list.

## A85: using the M5 Max hardware (2026-10-18 18:30Z, before any T result)

**Principal:** "there are strategies in using the mac hardware that could optimize for the kind of runs we're doing."

**Hardware, read from sysctl.** Apple M5 Max: perflevel0 has 6 cores and perflevel1 has 12, with 128 GiB of memory. NumPy's BLAS and LAPACK are Accelerate.

**Rulings:**
1. **A parallel tail-build feasibility study** (Codex3, 0595). Measure whether a cold tail build can be split across processes (by eval radius, shell or quadrature block) with **bitwise-identical** tables and jets, and whether multi-threaded Accelerate inside a build is bitwise-deterministic.
   - **Adoption follows the A72 rule:** bitwise identity is TESTED at K_big 32, 128 and 256, an independent check passes, and there is a **net** saving after the build, review and identity-rerun costs.
   - If the successor (r7) cannot be ready before the seal, V007 seals on r6 or r5 as planned. r7 then serves steps 4–5 and later work, but only after its own identity gates.
2. **Core priority during step 2.** Sealed T-runs run at normal QoS. Every lane's non-critical process (probes, fixtures, reviews) runs under `taskpolicy -b`, the background QoS, so the 6 perflevel0 cores stay available to the T-runs. This leaves the arithmetic unchanged. It applies from the step-2 launch onward and is not a cap.
3. **Step-2 outputs go on the internal SSD** (about 500 GB free after the storage move), not on External1. The output location is not part of any result.
4. **A sleep assertion for the whole of step 2,** tied to the launcher's PID with `caffeinate -i -w <pid>`, in addition to the app's own assertion.

Items 2–4 go into the RUNBOOK as root steps at launch. None of them changes a sealed byte.

## A84: parallelism on the critical path (2026-10-18 18:24Z)

1. **Speculative r6 identity runs.** This follows the A73 precedent for r5. As soon as the r6 BUILD lands with its bitwise K32/128/256 evidence, root launches the three identity runs on r6 (Z2, Z2_OFF_RO1, B0P_RERUN; cache ON where the tail is ON), without waiting for Claude3's independent check or the A72(c) timing verdict.
   - If the check changes any r6 byte, or r6 is not adopted, these runs are **void and kept**.
   - This takes about 2–3 h off the r6 branch.
   - The machine is oversubscribed now (load about 36 on 18 cores). The launch goes ahead when the r5 identity runs and the r6 bitwise tests have released their cores.
2. **Lanes run their queued items concurrently** as multi-agent workflows, not one after another (0593).
3. **Codex3 takes step-5 readiness now** (0594), since the r12 fix round may never be needed.

## A83: lane rebalancing for root's usage (2026-10-18 18:19Z)

**Principal:** root's account is nearly out of usage, while Claude3 and Claude4, both full Opus 5.5 Ultracode accounts capable of multi-agent coordination, have used under 10%.

**Changes:**
- **c2v007's own check workflow (wf_17f396c8) was stopped after the build froze.** Its partial check outputs (`review_comparator_c2v007_c2/`) are leads only. Codex2's cross-lineage review (0568) is the check of record, and **Codex1 owns the c2v007r2 fix round** (0588).
- **The cx3r007 review workflow (wf_cd66504d) was stopped.** Claude4 owns that review (0589).
- **Compare r11 (wf_9baf53cd) is stopped at its freeze, before its rechecks.** Claude3 (distinct) and Codex2 (cross-lineage) are the rechecks of record (0591), and **Codex3 owns any r12** (0590).
- **The r6 caching build is stopped at its BUILD.** Claude3 is its independent checker (0560 item 1, A72(a)).
- **Lane assignments:**
  - Claude3: the producer registry and the merged DOUBLING record (0586).
  - Claude4: the miss-reading prereg r2 (0585), step-4 readiness (0587) and the cx3r007 review.
  - Both run their work as their own multi-agent workflows (0592).
- **Root keeps:** rulings, coordination, the identity comparisons on real `UVT_*` runs, and the root-only seal and launch steps.

## A82: RI-27, the acyclic prereg ↔ compare pin order (Claude4 0083; prereg r4 e3b6b5b2) (2026-10-18 17:57Z)

**Ruled as drafted in r4.**
- The prereg's compare slot names the final round's **reviewed source**: the r11 or r12 compare, with the seal-time pins unset.
- The **sealed compare** sets exactly these values: V007_PREREG_SHA256, PIN_ADDENDUM_V005, PIN_DRIVER_BUILD_RECORD, PIN_V010_R5_CHECK (or its r6 counterpart) and PIN_PRODUCER_REGISTRY.
  - It is created after the sealed prereg and is named only in the SEAL_RECORD.
  - The seal check verifies, by line diff, that the sealed compare differs from the reviewed source only in those lines.
- The frozen addendum cites no sealed-prereg sha.

**Prereg r4 is the text of record.** No r5 is needed for A82. The seal record carries this entry as the no-change note RI-26 requires.

**Seal tools (Claude4 0085, 18:11Z).** `v007_final_prereg_c4/seal_tools/` holds four read-only checks plus the SEAL_RECORD builder, each tested 40/40 against tampering. Integration with the real guard v008 and launcher v007 passes. Root uses them at assembly.

**This V005 file closes at the freeze (0085 note).** Compare r10 L149 hashes this open file's path against PIN_ADDENDUM_V005, so any write to it after the freeze would make the sealed compare refuse.
- **Once the frozen copy exists, root writes nothing more to this file.**
- Every later root entry (flag rulings, verdict notes, steps 4–7) goes in a new **V006 addendum**.
- If r11 or r12 can cite the `_FROZEN.md` path directly, it should. Either way, this rule keeps the open file's bytes equal to the frozen copy's.

## A81: rulings on the final-prereg r3 root items (Claude4 0081; r3 07397846) (2026-10-18 17:50Z, before any T result)

| Item | Ruling |
|---|---|
| RI-19 | **0561 is the order of record, and this entry is the erratum to A72's H-01.** Root exclusively creates: (1) the SEAL_RECORD; (2) the ROOT_SEAL_ADMISSION config, which pins the SEAL_RECORD's full sha; (3) a separate SEAL_ADMISSION_RECEIPT naming both. The RUNBOOK verifies the published config sha before invoking any source, and records embed the config, seal and compare shas. "Its sha goes in the seal record" in A72 is superseded. |
| RI-20 | **Adopted.** RI-10's adoption rule applies to every NEW item the final compare IMPL declares. The IMPL lists each one with its disposition and its MUST_FAIL tests (A75), and the seal record quotes that list. V007 seals on the round whose three recheck lenses **and** whose distinct reviews of record (Claude3 and Codex2) report 0 blocking. |
| RI-21 | **Adopted.** The identity-comparator slot is the c2v007-lineage round whose own check and Codex2's review report 0 blocking. The identity-gate records of record are only that round's outputs on the identity runs of the **driver in the driver slot**, using the A59 replace-mode tokens derived from that driver and the raw successor-custody check (A67 N1). |
| RI-22 | **One merged DOUBLING record**, registered before the seal and read by the compare as one gate. Both halves must pass. **DDO half:** K_big {128, 256}, gas M_s 128, the max change over τ on the static rows of saved C4R3 le3, ≤ τ/20 (A58 RI-03). **NGC half:** operator e6453d52, K_big 32, the NQ max change over θ, ≤ θ/20. The θ/20 bound is declared here by analogy with RI-03, before any NGC target is opened. |
| RI-23 | **Adopted, conditional.** If GQ_NGC at M_s 96 fails anywhere on [2, 91], the NGC gas M_s becomes 128 (as A57 set for DDO), and LO_NGC and DOUBLING's NGC half are recomputed at that value. No NGC N-test is read until LO_NGC, EPS_NGC and GQ_NGC to 91 are all slotted. **LO_NGC in V007 is reported only** (draft L180): the V007 LO_NGC slot takes the LO_NGC record of record that exists at seal assembly. Coverage to 91 gates the **NGC N-test compare** (step 5), not the V007 seal. |
| RI-24 | **The r6 branch, if adopted.** The cache directory is a fresh, empty directory that root creates and names in the SEAL_RECORD. **There is no pre-warming before the seal**: the T-runs populate the cache themselves, KHI first. Every T-run records its cache mode and cache directory. The compare refuses a T-run whose mode or directory differs from the registered one. No T-run starts before the seal names the driver, and every T-run's driver_sha256 must equal the driver slot. This extends A67 N1 to T-runs. |
| RI-25 | **The SEAL_RECORD names the bound plan and command shas.** The binder runs after the addendum is frozen and the driver is chosen, and before the SEAL_RECORD is written. Root verifies both shas from bytes immediately before it runs the command. A validate()-level check of template equality is optional and not required. |
| RI-26 | **Adopted.** The addendum is frozen after the last pre-seal entry. The seal check verifies that every A-entry the prereg cites is present in the frozen bytes. Any entry after A81 that touches the prereg text needs an r4 or an explicit no-change note in the seal record. |

**Next.** Claude4 produces prereg **r4**, integrating A81. Its slots stay PENDING until seal assembly.

## A80: compare r11 launched; NGC cx3r006 reviewed (2026-10-18 17:35Z)

**Compare.**
- **Both r10 rechecks are FAIL:**
  - order: 4 blocking (`r10/recheck_order/RECHECK.md`);
  - validity: 2 blocking (`r10/recheck_validity/RECHECK.md`).

  Every blocking item is one already ruled in A79.
- **The r10 workflow (wf_97099de8) was stopped at 17:33Z,** after both recheck reports were on disk and before its narrow r11 round began. No r11 directory existed.
- **The successor round is r11 (wf_9baf53cd),** built from r10. It closes:
  - A79.1–6, A75 in full, A77.2 per family, and A73 F2;
  - every r10 recheck item, including validity's note that `gas_M_s_NGC` is not read (it must be bound to the registered value 96, or refuse);
  - every Claude3 and Codex2 r10 finding. Both outboxes are re-read before the round freezes.
- **Checks:** three independent refute-by-default recheck lenses (A71, paths and blinding, regression), with one fix round r12 if needed. Claude3's and Codex2's reviews of the final round are the ones used at the seal.

**NGC cx3r006 (c2930e18), delta review wf_45b699bd: PASS_WITH_FINDINGS on both lenses, 0 blocking.**
- 288 duplicate-record refusals, each typed and naming both paths.
- The selected V011 pairs fire byte-equal to r005.
- 78/78 dry plans match, and 37,954 RO1 pairs are identical outside NGC.

**Ruled:**
1. **Codex3 builds cx3r007** (0581). Every NGC launch-path record is parsed strictly (A71):
   - ST-SF1: the column-mean `result.json`, the rotation, column and tail-manifest `finish.json`, and `uvt_stage_records`;
   - ST-SF2 / A71-RESID-1: route-A `finish.json` and the manifest in the strict reader and in the admitted-route-A branches;
   - the producer-custody reads of upstream `start.json` worker_sha256.
   - Also:
     - ST-N1: no untyped RecursionError;
     - ST-N2: each record is parsed once strictly, with the sha compared across reads;
     - ST-N5: malformed rows raise typed refusals.

   cx3r007 gets a delta review, and NGC route A/B (step 5) launches from the cx3r007 registry. Step 5 is more than a day away, so this costs no schedule.
2. **Registries.**
   - Launch registry: cx3r006 **3c42ca07**, until cx3r007 is accepted.
   - **Retired now:** cx3r005 **47023c27** and r004 **c5abc2d5**. No NGC launch from either.
3. **IN-NGC-WIDEN-1 is noted as intended.** Inside NGC, a missing or malformed start.json, or a list/dict worker_pin, refuses even when the binding does not arm. This is fail-closed and consistent with A71.

## A79: compare r10 interim rulings; a successor round is required (2026-10-18 17:12Z)

**r10 is frozen:** source e801adc4, with IMPL and HASHES published at ~17:04Z. Its own rechecks are still running (wf_97099de8). Codex2's early TESTED findings (0453–0455) already require a successor round.

**Blocking, for the successor:**
1. **A71/A75 duplicates still PASS** (0454): a repeated B0_RO1 case kind (the guard compares whole objects, not the semantic kind), a repeated B0_N3 constructions entry, a repeated HARMONICS row, and a GQ roster name repeated with a different valid geometry, or an NGC roster with a different range. The successor must key every guard on the semantic identity, and enforce the A75.6 fixed roster → geometry map for every roster, required or extra.
2. **Blinded CLI** (0453): argparse prints argv-derived text before SystemExit in `--validity-only` and `--gates-only`. Fix it with a parser whose `error()` raises a typed refusal and prints a code only, with allow_abbrev=False and repeated flags refused (as in A76 SF-ARGV). The text is root-typed, not record-derived, so this is not a C5H leak, but blinded output prints codes only.
3. **H-07** (0455): a failed `os.stat` of the registered C5H root silently drops it from the identity set. Unavailable identity must be a refusal.
4. **NPZ logical-key alias** (0456, 17:12Z).
   - **The defect:** `weighted_responses.npy` and an extensionless `weighted_responses` member collapse to one NumPy key, and NumPy picks the extensionless one. A V5 failure is hidden in both archive orders.
   - **The fix:** before loading, reject collisions both in raw member names and in the logical names NumPy uses. An extensionless NPY member is refused outright.
   - **Also in scope:** the same rule applies to the identity comparator c2v007 wherever it reads NPZ members.
5. **H-07 symlink bypass** (Claude3 0070, 17:32Z, TESTED on stand-ins, BLOCKING).
   - **The defect:** a symlink to the firmlink spelling `/System/Volumes/Data/<registered>/…`, a symlink to an NFD spelling, or a subdirectory link followed by `/../` reads `c5h_path_hit` False, and `read_run` opens the file.
   - **The cause:** the name test and the identity walk run on the lexical normpath only, and the realpath prefix test is a string comparison.
   - **The fix:**
     - apply the name test and the identity walk to the **resolved** path too;
     - stat-walk every prefix of `realpath(s)` against the registered (st_dev, st_ino);
     - NFC-normalize before every string comparison;
     - keep item 3 (an unavailable identity refuses).
6. **A75.3 naming** (Claude3 0070 §2). Fifteen refusal sites refuse correctly but name neither entry:
   - T01/T02;
   - C02–C04 and S01;
   - the registry duplicate-key forms;
   - the S9/D2 row codes, C10, and A06/A07/B09.

   Each must name both entries by index or JSON path (blinding-safe).

**Rulings on the departures r10 declares:**
- **NEW-61 (SR_K, correcting A75.7).** Under A67 N2, SR_K's gate-record sha is registered before the seal, so PRODUCED_AFTER_THE_SEAL is refused for SR_K. r10's behaviour stands. A75.7 was wrong to list SR_K as a post-seal gate.
  - **Correction at 17:16Z.** As first written, this entry extended the refusal to "every V007 gate". That was wrong.
  - The eight gates computed from V007 run outputs are SRB_ROT, RB_FP, T2I, EA, MT, I1T, FLAG_RULINGS and HARMONICS. Their records cannot exist before the seal, so **r10's allow-list for those eight stands unchanged**. At compare time their records are verified by producer pin (A62.2/A69).
  - The token is refused for SR_K, EPS, GQ, LO, LO_NGC, DOUBLING and the identity gates.
  - Claude3 0069 and Codex2 0457 caught the overreach. Codex2's 16 "failures" on those eight gates are therefore not defects.
- **NEW-67 (M_s).** Both bindings hold together: the certificate M_s equals the case-registered gas.M_s (A75.8), **and** the registered value must be 128 (A57). DOUBLING also keeps RI03's production-128 rule. A matched-64 control refusing is correct.
- **NEW-64 (H-07 substitute) is accepted.** Rejecting any multiply-linked file on the protected device is a conservative, fail-closed substitute for a per-file inode inventory of the C5H run. If it ever refuses a legitimate input at compare time, root supplies an authorized inventory then. A refusal can delay the verdict but never changes a reading.

**Successor round.** It is launched once r10's rechecks return. It carries every r10 recheck finding, Codex2's final review and Claude3's delta review. Claude3's and Codex2's reviews of the successor are the ones used at the seal.

## A78: launch packet V004 reviewed; three fixes before the seal (2026-10-18 16:57Z)

**Claude4 0076: PASS_WITH_FINDINGS, with 0 blocking findings, 3 should-fix and 6 notes.** Report: `review_launch_packet_0559_c4/` 6361a675.
- Ramp gate: 14/14.
- Seal-publication forgeries: 29/29 refused.
- H-02/H-03/H-04 pass.
- Specs and caps: 68/68, byte-identical apart from the declared changes.
- Roles: 9/9. C4T-D5 selects a5277172 and the other nine cases select 869ce387.

**Ruled. Codex1 fixes all three before the seal (0574), and Claude4 delta-checks them (0575):**
- **C4-S1:** `validate()` binds `plan['driver']` (path and sha) to the seal's driver, and the plan's addendum pin to the seal's. A seal that lacks either pin refuses. This matters because root chooses r5 or r6 at the seal.
- **C4-S2:** every producer CLI and `main()` route calls `check_run_path(out, allow_registered=False)` before `open(out, 'x')`.
- **C4-S3:** `aggregate_records` verifies each input's embedded root_admission and producer pin. A forged or unstamped input refuses.

**The notes stand as accepted.** N4 (H-08: a mid-run admission change crashes `worker()`) fails closed; the RUNBOOK says so.

**Closed (17:29Z).** Codex1 0047 published BUILD_V005 (46bc5b5d). Claude4 0079 delta-checked it: **PASS**, 0 blocking, 0 should-fix (report 2b483267).
- C4-S1: 19/19 refusals.
- C4-S2: 6/6, and all 11 writer sites are checked.
- C4-S3: 13/13 refusals.
- Pending template and binder: 11/11.
- Every V004 regression re-run passes.

**The launch packet is ready for the seal.** **Root checklist item (N2):** the root admission config must name the V005 launcher and guard sources exactly, because the build check is only a substring match.

**Errors register: timestamps ahead of the clock (at 16:51Z).** The headers of A74–A77 were stamped 7–16 minutes ahead of the clock. They are corrected above, ordered against the lane messages' own `date -u` lines. Dispatches 0566–0573 carry the same drift in their "UTC ~" lines and are left as written, since lanes had already read them. The actual times were: 0566 ~16:17Z, 0567 ~16:21Z, 0568 ~16:27Z, 0569 ~16:41Z, 0570 ~16:44Z, 0571/0572 ~16:45Z, 0573 ~16:48Z. **Fix:** stamp from `date -u` at the time of writing.

## A76: c2v006 closed; its own check carried into c2v007 (2026-10-18 ~16:40Z)

**c2v006 final (wf_a088aed1):**
- **Build:** selftest PASS. The r4 identity pairs are PASS_BITWISE_EQUAL: Z2 27/27 (4ab7cb39), Z2_OFF_RO1 27/27 (2b29c41e), B0P 22/22 (77ca040d).
- **r4 records:** B1 e5228566, B1_OFF d3df0fef, B0prime_RERUN afd76dcd. These are **not seal records** (A67 N1: they carry the r4 driver sha).
- **Independent check** (`gates_v006/check/CHECK.md`, 5296c5c0): **FAIL**, with 1 BLOCKING item. The checker reran Z2 r4 and got a byte-identical PASS.
- **Codex2 0447: FAIL** (B1–B3, S1, S2, and the A73 items absent).
- **c2v006 is superseded by c2v007, and is not used at the seal.**

**Carried into c2v007 (binding, in addition to A73/A74):**
- **B-ID (BLOCKING).** Every field of the route-A checkpoint IDENTITY.json is compared: code, controls, environment, fixed_source, inputs_sha256, shapes and identity_sha256, not only `identity.caller`. COVERAGE may never exclude a file by name while claiming full coverage. On the real pairs the only differences in that region are token-declared, so this costs nothing (TESTED by the checker).
- **SF-ARGV.** The CLI refuses repeated flags and abbreviations (allow_abbrev=False, plus a duplicate-flag check).
- **SF-NN.** Stage-number normalization maps only through directories that exist (dir2name).
- **Notes, to be closed:**
  - N1: stage regexes use ASCII `[0-9]`, not `\d`.
  - N3: a non-regular file (FIFO, device or socket) FAILs without being read.
  - N4: empty directories are inventoried.
  - N5: declared NPZ files also compare container bytes, i.e. the archive comment and any prepended bytes. Equal-bytes-first covers undeclared ones.
  - stdout/stderr are excluded only at the stage top level.

If the c2v007 workflow (wf_17f396c8) lands without any of these, a targeted successor round closes them before the seal.

## A75: Claude3 0067, the compare's must-guard list for the final round (2026-10-18 ~16:21Z)

**Source.** Claude3 pre-audited compare r8 (bd51db15) on synthetic worlds: 63 sites, `review_v007_compare_c3/r10_pre/`. The r10 build (wf_97099de8) was briefed before 0067 arrived and may not cover all of it.

**Ruling. The final compare round is not final until each item below is closed and TESTED. Every reproduction becomes a MUST_FAIL case.**
1. **Must guard: in each case a duplicate makes a reading easier.**
   - A01 `_shells`, for LO and LO_NGC.
   - A02 `flag_rulings`: a duplicate (flag, run) is a RECORD_DEFECT, and no ruling is silently replaced.
   - A03 `_spec_sets` EXT evidence.
   - A04 duplicate `key_equivalence_map` pointers.
   - A05 duplicate GQ roster names (max-merge removed).
   - T01: `read_run` strictly pre-parses the field and rotation `finish.json` files before the pinned V005 adapter sees them.
2. **Should guard: the letter of A71.**
   - B01–B11 and A06–A08;
   - `load_pinned_json`, with object_pairs_hook;
   - the S01 `c5h_interlock` marker: a duplicate key is a defect, never "absent".
3. **Naming.** A duplicate refusal names both entries by index or JSON path, never by a record label (blinding).
4. **H-07 in full.** `c5h_path_hit` and `read_run` catch `/.vol/<dev>/<ino>` aliases of the directory and its files, and hard links, by (st_dev, st_ino) against every file of the C5H run.
5. **S1: all 13 blinded early-refusal sites** print a code only, with no text from the record: L661, L944, L954, L1022, L1024, L1028, L1037–1040, L4202, L4208, L4374, in r8 numbering.
6. **P-SF1.** A fixed map binds each GQ roster to its geometry: DDO_C2T → C2T_KB&lt;P&gt;, DDO_C3T → C3T_KB&lt;P&gt;, DDO_C4T → C4T_KB&lt;2P&gt;. A mismatch is a RECORD_DEFECT.
7. **P-N2.** PRODUCED_AFTER_THE_SEAL is accepted **only** for gates whose inputs are V007 run outputs (SR_K, and any gate the prereg defines on run outputs). It is refused for EPS, GQ, LO, LO_NGC, DOUBLING and the identity gates, whose records of record exist before the seal.
8. **CHK-1.** The certificate M_s is bound to the case block's registered gas.M_s, not to the constant 128. A73 F2 applies too.

**Process.** If r10 (or its internal r11) lands without these, a further successor round closes them, and Claude3's distinct review of that round is the one the seal uses.

## A65: the stage-0 grid as an NGC sensitivity alternative (2026-10-18 ~14:50Z, before any target is opened)

**Gate** (`stage0_grid_gate_c2/`, GATE_V001 plus an independent check):
- The stage-0 pooled grid is **CONVEXITY_ADMISSIBLE, TESTED-POSITIVE**:
  - node test 0/17 members, using the A2 admission code unmodified;
  - block test 0/81 members (0/2916 blocks), rebuilt independently from the raw captures.
- **Candidate coefficient file** `STAGE0_POOLED8_CANDIDATE_GRID_V001.npz`, **bdb9016c**. It has the 2e3a36d8 schema and is target-free.

**Difference from A2:**
- relative distance 0.477 globally and 0.483 at the k = 0 node;
- 93.6% of entries lie more than 2 band-SE from A2;
- h_NN(0) is −1.899 ± 0.106 against −3.551, a gap of 15.6 SE. A2's own single chains span −5.20 to −1.76.

**Caveat (check R-3).** Stage-0 differs from the same-kernel BIRTHK about as much (0.451). The sealed k = 0 reading stays SUPPORTED, but its causal gloss, "drift inflated A2", is **UNTESTED**.

**Ruling.**
1. **A2 stays the headline grid**, per the sealed row: the stage-0 grid is never a replacement.
2. **Registered sensitivity alternative `STAGE0_GRID_OUTER`.** It covers the **NGC3198 outer rows only**, and is scored **separately from the headline**.
   - **Definition:** the NGC route-A/B prediction at the **headline admitted DDO154 calibration point(s)**, with the coefficient grid swapped to bdb9016c. Everything else is identical.
   - It is labelled a *coefficient-grid sensitivity at fixed calibrated parameters*, not a recalibration.
   - Its runs come **after** the headline NGC runs, using spare compute. If they cannot finish before the freeze, the alternative reads **NOT_EVALUATED_BEFORE_FREEZE**, like GL10, and never delays the headline.
3. **Registration** (target-free, before the freeze):
   - a slots successor adds STAGE0_GRID_OUTER, with its outer-row set given by the A15/miss-reading OUTER zone (R ≥ 30 kpc) and the grid sha bdb9016c;
   - v011 admits bdb9016c **only** for that alternative's specs; the A2-only rule is unchanged for the headline;
   - v003g's alternative binding includes it.
4. **Disclosure.** The freeze manifest and the miss-reading prereg disclose the stage-0 outcome, the SUPPORTED k = 0 reading with its untested gloss, and the 0.48 grid difference. Together these are a counted coefficient-grid uncertainty for every row.

**Lanes.**
- Codex1 builds the NGC N-test evaluators and their compare (FROM_CODEX/0510; output `ngc_ntest_eval_cx/`).
- Codex2 has two lanes (0511): calibration readiness for the tail scheme, and a cross-lineage review of the V007 implementation.
- **N3 ruled (0512):** |ΔS| ≤ θ/4 and |ΔdL| ≤ θ/4 for K_big 8 and 32 against 16, at every ring and azimuth. "S/θ" is a reporting unit only. The N-test outcomes are N_NO_RUN, N_INCOMPLETE, N_FAIL_<test> and N_PASS. N_PASS is only an input to NGC route A/B.

**Codex2 cross-lineage review of the V007 implementation (FROM_CODEX2/0416, 12:13Z; REVIEW.md 36d86df9): PASS_WITH_FINDINGS.**
- Codex2 is a different model family, and every check came from its own scripts: 32/32 source, 19/19 saved-state/plan, 11/11 GEO-map AST.
- It ran an independent G5\G4 node replay, sign/symbol arithmetic and adversarial tests of the RO1 predicate, and compared the A2F10 plan against both v009 parents. All passed.
- **SHOULD_FIX B0-EMPTY, ruled:** the B0 plan-identity tool can count two equal early failures with empty report directories as "identical". B0 counts only comparisons whose expected reports are non-empty and whose planning completes. Equal early failures are listed separately as no evidence. The 6 R3 KMAX specs that stop at the seed-custody block move to that list, which means the B0 count must be restated. The fix is a successor B0 tool plus a B0 record rerun before the seal.
- Codex3 is assigned to NGC route A/B readiness and freeze/score readiness (0516).

**Codex lane findings and rulings (about 12:25–12:40Z):**
- **Codex2 Lane A (0418), calibration readiness.**
  - It built orchestrator successor cx2v006r5, with K_big parametric 64/128, and 48 box-corner templates. 70/70 dry reports pass structurally.
  - **EPS over the calibration box: the sampled maximum is 0.0125, against 6.42e-4 at the anchor.** These are samples, not sup certificates. So calibration needs **per-point certificates**, which the successor enforces; anchor substitution is refused.
  - Route-A tail-build time per call at 6 iterations: 4.5 min at K_big 64, 15.1 min at 128.
  - Six typed blockers are owned by root: certificate scope, A55, V007, tail re-anchor, corner evidence, uncertainty carrier.
- **Codex3 Lane A (0579/0582), NGC readiness.** Driver v010 r4 cannot run NGC with the tail. It gave three TESTED refusals:
  - route B: uv_tail is an unknown key;
  - route A: only coefficient grid fe5a2f06 (TESTED-NEGATIVE, P-76);
  - T120L: refused above 80 axis nodes.

  **Ruled (0517):** Codex3 builds **driver v011** = v010 r4 plus NGC tail support, with the A2 grid 2e3a36d8, anisotropic T120L reproducing the saved operator bitwise, and truncation wiring. v011 must be plan-identical to v010 r4 on every DDO spec.
- **Codex3 Lane B (0581), freeze/score.** Synthetic 85/85. The GL4 rows Q01/Q02 are registered INVALID (slots V002), but freeze v003d's D1 rule needs an all-finite reference member, so no freeze can complete.
  - **Ruled (0518): the invalid-as-miss contract.** All 43 rows stay. INVALID rows are scored as misses at the worst tier. D1 is applied over registered-valid rows only. GL10 stays an unevaluated alternative, never a repair.
  - Successor v003e is being built.

**Lane expansion (about 12:35Z).** The principal asked that the frontier lanes advance the problem wherever they can. Each dispatch names its 120/43 plug:

| Dispatch | Lane | Work | 120/43 plug |
|---|---|---|---|
| 0519 | Codex2 | BH-D step 3 (LR:29 exit), prereg and code only; plus lensing readiness and a distinct check of the lensing memo | The history channel is the remaining owned route to a flat outer curve (A41) |
| 0520 | Claude3 | Cross-lineage check of Codex2's calibration orchestrator | Calibration safety |
| 0521 | Codex1, second lane | The UT-1 spec-compliant model version: declared zero mode at k = 0; k → 0⁺ from k ≠ 0 nodes only, under one pre-registered continuation rule (a new CA chosen by root before any galaxy use) | An immediate 120/43 rerun without CA-34/CA-28 after the baseline |
| 0522 | Claude4, after B3 | Miss-reading prereg for the 43 rows, sealed before the targets open | The two-way reading of outer misses |
| 0523 | Codex3, queued | UT-1 U2 order-of-limits / frozen fraction, prereg and code only | Whether a frozen long-wavelength sector exists at outer radii |

Every deciding computation is pre-registered and launched by root after its seal. Lanes write preregs and code only.

**Withdrawn (about 12:38Z), on the principal's instruction:** "i don't know that I'd want to distract by injecting any work not related to the galaxy run."
- **0519, 0521 and 0523 are WITHDRAWN** (0524). Partial outputs stay untouched.
- 0520 and 0522 remain; both are galaxy-run work.
- Codex2 is reassigned (0524) to per-point calibration certificates, and to a cross-lineage review of the V007 compare r5.
- **Standing rule:** lane work is limited to the galaxy run (120/43) until the principal says otherwise. Root relaunched the finished r2-loop workflow script by mistake. Its first round targets the existing directory r2. It was stopped within about a minute.
- No file in r2 changed. HASHES.txt verifies, apart from the two expected external inputs: the open addendum and the reissued review record.
- The r5 loop (wf_24068af3) is a new script that refuses existing round directories.