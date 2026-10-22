# REVIEW — Lens A (fidelity and coverage): miss-reading prereg r2, round 1

Reviewer: a helper of lane Claude4, Lens A of the dispatch-0592 independent checks of 0585. Refute by default. Nothing in the object was edited. No NGC3198 target or observed-velocity data was opened, and no launches were made. Python was used only on synthetic data, plus two target-free records. Every sha below comes from bytes, and every time from `date -u`.

**Verdict: FAIL.** 1 BLOCKING, 10 SHOULD_FIX and 7 NOTE findings.
- The BLOCKING item is a mis-citation in a binding invariant (I-6). It contradicts A66.2, 0550 and the actual NGC N-test outcome (A90), so it bears on whether the document applies at all.
- The other fixes are concentrated in four places:
  - the TSR flag rule (M-7), which cannot be applied to the record of record;
  - the meaning of NEAR;
  - the scope of R-MF under A15 E3;
  - coverage of 0550, A90 and 0606.

## 1. What was verified

**The object, verified from bytes** (all 10 match `HASHES_R2.txt` and the task list):

| file | sha256 |
|---|---|
| PREREG_MISS_READING_R2.md | `6437ea33432f50971eef81e549a8e5789d0bd892efaf2d0f423ce4c933f30143` |
| CLAUSE_SOURCE_MAP_R2.md | `b105b55d7f80c5868d936f577ce81e92992999440f5cd85a06decbc62650d24b` |
| ROOT_ITEMS_R2.md | `1d7af792f9b115fc7882254b694d82299217c3ab846d7d26d591f45a5c5eaf7f` |
| NUMBER_PROVENANCE_R2.json | `c81b5a7a579476480a085681ebd6eb8aa445e38b6a7abe2284dba3716b0c2832` |
| TARGET_FREE_CHECK_R2.json (PASS) | `aab683236116bc3562df86f3b9542a54eec3446c44a8f0e5569ff2b305d2180b` |
| TARGET_FREE_MUTATION_TEST_R2.json (14/14) | `2a8202b823beb5cd0bc03c9e1e2b0377d9de59410a698c8d185f39739d66bc41` |
| tools/check_target_free_c4v001.py | `85457a43c654aa13b49fa528b786a615e99a51eaa29b4ba42687a2c0f3396cc7` |
| tools/test_check_target_free_c4v001.py | `fc403648a57b3f0ee30b164e2cde48e3c1889bfee33938c8b23a93c1fd88ea11` |
| tools/make_miss_reading_c4v002.py | `8c0d9fc2fb962f3e72de9e6a7a03cc11aa38efccd59981713fbcc0008b32576a` |
| INDEX_R2.md | `6c1919a900d56fcb7438015db6a6be1d1d28fd07ee17a9bee6e1e007c0045b9b` |

**Sources read** (sha256 from bytes):
- **V005 addendum (open).** Read at 18:49:07Z as `bba6daf53ad07d691d09648801bc113b61718e4be0568a6d870cdb87982d1a17`, newest entry A90. That snapshot is kept as `V005_SNAPSHOT_READ.md`. Re-read at 18:52:42Z and again at 19:11:55Z as `0753f2d8dc437592a4ad70140f309c774837cb07e9c04e2c213c4421eeb8e87e`, newest entry A91. V005 line numbers below refer to `0753f2d8`.
  - All 11 per-entry section pins in §11 MATCH on `0753f2d8`: A48, A56, A60, A62, A63, A64, A65, A66, A70, A81 and A82. This was checked with my own extractor (`tools/entry_pins_lensA_c4.py`), which is independent of T5.
  - **Final read** at 19:16:26Z: `b7a900c4c495b4e9876701918a32ed8e1770da3438a8561e2b18bbd8d0b3ccda`, newest entry A92 ("r5 identity gates PASS under c2v007r2", a V007 matter with no reading change). All 11 pins still MATCH. A92 was inserted above A91, so lines at or after the old L890 shift by 22 in these bytes.
- **Dispatches 0607–0609** (19:14–19:17Z) were also read: c2v007r2 delta, a command-script note and the identity records. None touches the reading.
- **V004** `487d4449…` (A14–A46) and **V003** `5bef6552…` (A10–A13).
- **V001** `6aecf0cb…`.
- **Freeze v003g:**
  - module `48a1e48a…`, with every cited function and constant read;
  - slots V003 `d3859b42…`;
  - RUNBOOK_V001 `9557b5aa…`.
- **Claude4's 0071 review** `575f872c…`.
- **Dispatches 0512–0606** in FROM_CODEX: every dispatch whose title touches NGC, freeze, rosters, N-tests, certificates or readings, and 0585 and 0592 themselves. The relevant shas are quoted in the findings.
- **Codex1 posts** 0031, 0032, 0048, 0049 and 0056.
- **NGC K32 N-test compare output** `claude_artifacts/ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json`, `6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9` (target-free numerics).
- **Codex1's steps 6–7 rehearsal summary** `REHEARSAL_COMPLETE_V001.json`, `19807bb3…`.

**Reproductions.** `tools/repro_lensA_c4.py` imports v003g by path with `-I -B`, so no bytecode is written. It then installs an audit hook that refuses every open, and calls v003g's own helpers on synthetic members. Output: `REPRO_LENSA_OUT.json` (R1–R4) and `REPRO_LENSA_OUT_V2.txt` (R1–R5).
- **R1:** NEAR holds while no member is within error.
- **R2:** a gate reason yields INVALID_AS_MISS, and a gate-listed row reported valid yields a HIT.
- **R3:** the M-7 rule applied to the actual K32 record flags 0 rows.
- **R4:** the zone table and the STAGE0 scope are exact.
- **R5:** an OUTER failure triggers no pattern.

**K-1, consequences beyond the description: none found.** No line of the three text files has an odd number of backticks, so T4's code-span stripping cannot run across prose. The only code spans that contain digits are file names and paths.

## 2. Findings (most severe first)

### A-01 — BLOCKING — PREREG [C-I6] (also CLAUSE_SOURCE_MAP row C-I6 and NUMBER_PROVENANCE "0512")

**Quote (PREREG L56–57).** "Under the 0512 ruling logged in V005, only N_PASS is an input to route A/B. So any other outcome, such as N_INCOMPLETE or N_NO_RUN, also gives no route-A/B run." / "With no route-A/B run there is no score, and this document is not applied."
- Map C-I6: "(N_PASS is the only input to route A/B)".
- Provenance "0512": "the 0512 N-test ruling (N_PASS is the only input to route A/B)".

**Defect.** This inverts 0512. It also contradicts the immediately preceding bullet, which allows N_FAIL_N1 confined to TRUNCATION_SHAPE rings (A66.2), and it contradicts the gate 0550 actually created.
- The real NGC outcome is N_FAIL_N1 with the gate OPEN (A90).
- Read literally, the sentence says that this outcome cannot feed route A/B. The next sentence then says the document is not applied.
- So the sealed text would carry a self-disapplication argument on exactly the case that has occurred.

**Evidence.**
- 0512 (`adac97bb…`) item 2: "`N_PASS` licenses nothing by itself. It is an input to the NGC route-A/B step."
- V005 L1245 (the A65 trailing block): "N_PASS is only an input to NGC route A/B." Here "only" means "merely", as 0512 shows.
- V005 L634 (A66.2): "N_FAIL_N1 confined to TRUNCATION_SHAPE rings does not block NGC route A/B."
- 0550 (`5c686ae8…`): "Add a field `n_route_ab_gate: OPEN|BLOCKED` with the reason codes to the compare output. Do not change the 0512 outcome names."
- V005 L916 (A90): "Under A66 the route A/B gate reads **OPEN**, for the sole reason TRUNCATION_SHAPE_RESIDUAL_ONLY_A66."
- K32 compare `6f095f64`: `outcome` N_FAIL_N1, `n_route_ab_gate` OPEN.
- Codex1's rehearsal (`19807bb3`, rough edge "I6") and dispatch 0606 item 6 flag the same contradiction independently.

**Fix.** Replace the sentence with: "Route A/B runs only when the registered NGC N-test compare reports `n_route_ab_gate` = OPEN (0550; A66.2–A66.3). That happens for N_PASS, or for N_FAIL_N1 confined to TRUNCATION_SHAPE rings (reason TRUNCATION_SHAPE_RESIDUAL_ONLY_A66). N_PASS licenses nothing by itself (0512). Every other outcome, N_INCOMPLETE and N_NO_RUN included, leaves the gate BLOCKED (0512: missing input is never a pass)."
- Record the compare record's sha, outcome, gate and reason codes in the header (D-4).
- Pin 0512 and 0550 in §11.
- Correct the map row and the provenance entry.

### A-02 — SHOULD_FIX — ROOT_ITEMS M-7 (also PREREG [C-1.4] and [C-9])

**Quote.**
- M-7: "the radial support [r_lo, r_hi], exactly as stored in that record"
- M-7: "A query q is flagged if and only if r_lo ≤ R_q ≤ r_hi. This is a closed interval"
- M-7: "A broader flag cannot ease any reading, because R-TSR stays OPEN (DT-TSR is NOT SCHEDULED) and may cite only flagged rows."
- [C-9]: "The definition of a ring's radial support decides which rows are flagged. | Root fixes it before the seal (M-7)."

**Defect.** The record of record that M-7 names, the production-K32 N1 record of the NGC compare, stores no interval. Its support is a single sampled ring. So the recommended rule cannot be applied as written.
- Read as a point interval, it flags no row, which would empty the flag that A66.2 mandates.
- Any cell-width rule is knife-edge. The ring lies 0.00085 kpc above the Q25/Q26 midpoint.
- The reasoning is also unsound. R-TSR can be reported "consistent" for flagged MISS rows ([C-3.2] P10 row), so a broader flag does widen an excuse reading.
- 0550, which created the compare's ring/support listing and the freeze flag requirement, is not cited.

**Evidence.**
- `K32_COMPARE_COMPLETE_V001.json` (`6f095f64`; Codex1 0056 `4b67319d`): `failing_TRUNCATION_SHAPE_rings[0].radial_support = {"kind": "sampled_ring", "R_kpc": 10.540847190215317}`. There are no r_lo or r_hi fields.
- Repro R3: the closed-interval rule flags `[]`. Q25 is at 10.04 and Q26 at 11.04, so the midpoint is 10.54. The ring minus the midpoint is +0.000847 kpc, and the nearest query is Q26.
- 0550: "The compare output must list the failing TRUNCATION_SHAPE rings, with S/θ and radial support. The freeze flags the overlapping rows TRUNCATION_SHAPE_RESIDUAL."
- The rehearsal rough edge "M7" and 0606 item 2 flag the same gap.
- v003g's roster key set is exact (L1658), so the flag record must be a separate pinned input, for example through `write_freeze_manifest` `input_files`.

**Fix.**
- Define, before the seal, the support of a `sampled_ring` record. Examples: the interval between the midpoints to the neighbouring sampled N1 rings of the same record, or the two bracketing query rows.
- Compute the flagged query ids now from target-free data and write them into §1.4. Alternatively, state that no row is flagged and that P10 and R-TSR are vacuous.
- Cite 0550 and A90.
- Restate the reasoning as a trade-off: broader is more disclosure, but it widens R-TSR's "consistent" scope.
- Say that the record is pinned through `input_files` at RUNBOOK step 8.

### A-03 — SHOULD_FIX — PREREG [C-1.1] (also ROOT_ITEMS M-1)

**Quote.**
- [C-1.1]: "**What NEAR means.** Some admitted representative member state reaches the error bar, but the frozen reference member does not." and "It is not counted as a miss in §2."
- M-1: "(c) discards real information: whether some admitted state reaches the error bar."

**Defect.** `band_overlaps_error_bar` tests a pointwise min/max envelope against the error bar. A band that straddles the error bar overlaps it even when no member is within error. So NEAR does not mean what the text says.
- NEAR rows are removed from M(Z), which can switch off miss-dominated patterns (P1–P5).
- That makes the rule more lenient than its own stated rationale.

**Evidence.**
- v003g L2081: the band is the min/max over valid members. L4104: `overlaps = … lo <= obs + sig and hi >= obs - sig`.
- Repro R1: members at v+3σ (the reference), v−2σ and v+2σ. The envelope is [90, 115] against the error bar [95, 105], so `band_overlaps_error_bar` is true while every member's `within_error` is false.
- The label `POINTWISE_ENVELOPE_NOT_A_REALIZABLE_CURVE` says the same.

**Fix.** Take one of two routes.
- (i) Define NEAR as "not INVALID, not HIT, and some PRIMARY member has `members[m].rows[q].within_error` = true". Those are frozen v003g fields, with no new number, and this matches the stated meaning. Add it as option (d) in M-1.
- (ii) Keep band overlap, correct the gloss ("the pointwise envelope overlaps the error bar; no single member need be within error"), and justify the exclusion from M(Z) on that weaker basis, or count straddle-only NEAR rows as MISS.

### A-04 — SHOULD_FIX — PREREG [C-3.2] P1/P2 rows and [C-8], against [C-P]

**Quote.**
- [C-P]: "Under A15 E3 an outer-row failure is TESTED-NEGATIVE for exactly the present-mass-only lapse response of the L = 4 coefficient method, at the A2 grid and the calibrated θ."
- [C-3.2] P1 row: "If P1 holds, this is TESTED-NEGATIVE for exactly this scope."
- [C-3.2] P2 row: "**R-MF**, with the opposite sign: overshoot." No TESTED-NEGATIVE appears there.
- [C-8]: "'TESTED-NEGATIVE' only for R-MF, within its stated scope".

**Defect.** The binding A15 E3 makes any outer-row failure TESTED-NEGATIVE for that scope. r2 applies this only to P1, an outer deficit.
- An outer overshoot (P2) never reads TESTED-NEGATIVE.
- An OUTER zone that is miss-dominated with a CENTERED median (misses on both sides) triggers no pattern from P1 to P9 at all, so the outer failure gets no registered reading.
- This is narrower than [C-P] and A15 E3, and it is easier on the model.

**Evidence.**
- V004 A15 E3 (L44): "An outer-row failure would be TESTED-NEGATIVE for exactly this: the present-mass-only lapse response of the L=4 coefficient method at the A2 grid and the calibrated θ."
- Repro R5, an independent implementation of §2: OUTER r = [−3, −2.5, −2, −0.5, 0.5, 2, 2.5, 3] gives 6 of 8 misses and m = 0 (CENTERED). With INNER and TRANSITION hit-dominated, P1–P9 are all false.

**Fix.**
- Define "outer-row failure" explicitly as OUTER miss-dominated with N_v(OUTER) ≥ 1, whatever the sign.
- Make R-MF read TESTED-NEGATIVE for its stated scope whenever that holds: P1, P2, and a new pattern P11 OUTER_FAILURE_UNSIGNED for the CENTERED case.
- Add P11 to §2, and to §3 with the R-MF, R-REACH, R-HIST, R-UT1 and R-DRIFT readings as for P1.
- Correct [C-8] to match.

### A-05 — SHOULD_FIX — PREREG [C-1.1] and [C-4]

**Quote.**
- [C-1.1]: "In v003g this holds exactly when the root-pinned roster registers q INVALID with one of the three registered reasons (§4)."
- [C-4]: "**The INVALID set** is exactly the set of rows the root-pinned roster registers INVALID"
- [C-4], gate row: "a root-listed gate's own reason | the query ids the gate document lists"
- [C-4]: "So `score_status = INVALID_AS_MISS` can be taken as the roster's statement."

**Defect.** These statements misdescribe v003g in three ways.
- (i) A root-listed gate's own reason also yields INVALID_AS_MISS, so the condition is not "one of the three registered reasons". §4 itself says there are two kinds of reason.
- (ii) Gates authorize but do not require. A gate-listed row that the producer reports valid and finite is scored normally, so the INVALID set is not "the query ids the gate document lists". For gate rows, INVALID_AS_MISS is the producer's statement as authorized by the roster.
- (iii) Under PER_THETA cut contexts, the cut and gap rows can differ by member θ and by alternative. "The INVALID set" is per member; the PRIMARY classification uses the reference member's set.

**Evidence.**
- v003g L1725: `gates[q, reason] = normalized`.
- L1798: `return {'status': 'INVALID', 'reason': reason, 'registration': dict(gate)}`.
- L4042: any registration yields `score_status='INVALID_AS_MISS'` with `registered_reason=reg['reason']`.
- L1872: only built-in `required` rows refuse a finite value.
- L1765: PER_THETA.
- Repro R2: Q02 (gate reason SYNTHETIC_GATE_REASON) reads INVALID_AS_MISS, and that reason is not in REGISTERED_INVALID_REASONS. Q03 (gate-listed, reported valid) reads HIT. `_root_frozen_rows` accepts both.
- 0531 item 1: "INVALID on a row that is not on the roster refuses, unless a root-listed gate in the roster covers that row."

**Fix.** Rewrite as follows.
- INVALID_AS_MISS holds exactly when the reference member's frozen row carries a roster-authorized INVALID registration. That is either a built-in reason derived from its rule, which is always INVALID, or a root-listed gate's reason. A gate row is INVALID only where the producer reported it INVALID and the gate lists that (row, reason) pair.
- Say that I(Z), P0 and P9 use the reference member's set, and that a twin uses its own set.

### A-06 — SHOULD_FIX — coverage: PREREG [C-I6], [C-7] D-4, and CLAUSE_SOURCE_MAP "Dispatch 0585 coverage"

**Quote.**
- [C-I6]: "**Gas M_s.** The NGC gas M_s is 96, or 128 if GQ_NGC at 96 fails anywhere on [2, 91] (A81 RI-23)."
- [C-I6]: "**Certificates.** EPS_NGC, LO_NGC and GQ_NGC are certified to coverage at least √2·64 ≈ 91 /kpc (A64.2)."
- [C-7] D-4: "the values of I-6, together with the gas M_s actually used and the certificate record shas."

**Defect.** The text does not integrate these rulings and records that touch the NGC reading:
- 0550 (14:58Z, before assembly), which created the gate and the ring/support listing;
- Codex1 0032 (14:50Z, before assembly): GQ_NGC at M_s 96 holds on [2, 91], so the RI-23 antecedent is already TESTED false;
- the NGC I1-T requirement (A52.4; 0512's N_INCOMPLETE condition), which is absent from I-6;
- A90 (18:49Z, after assembly): K32 N_FAIL_N1 with tests_read true and the gate OPEN; LO_NGC_K32_CERT_V001 is the NGC N-test record; an LO I1-T precondition is still open and must be ruled before any NGC route A/B launch;
- 0606 (18:59Z): six rehearsal rough edges for r2 to address.

**Evidence.**
- V005 L916–918 (A90): "LO_NGC_K32_CERT_V001 (07745bbf) gives coverage to 91. It is the NGC N-test record." and "**Open for step 5:** the LO I1-T precondition covers only the stored iteration-0 sources … it is ruled before any NGC route A/B launch."
- Codex1 0032: "GQ_NGC at M_s96 versus192 over[2,91]/kpc … M_s96 holds; no128 proposal needed" (record `be148bab…`).
- V005 A52.4 (L218): "NGC I1-T of stars + H₂ against the T120L fixed source must pass before any NGC N-test is read."
- 0606 (`dbb80c77…`) items 1–6.

**Fix.**
- I-6 should state the current state:
  - compare `6f095f64…`: N_FAIL_N1, gate OPEN, TRUNCATION_SHAPE_RESIDUAL_ONLY_A66;
  - LO_NGC_K32_CERT_V001 `07745bbf…`;
  - GQ_NGC_91_MS96 `be148bab…`, so M_s stays 96 and the 128 branch is not triggered unless root rules otherwise;
  - the EPS_NGC and NGC I1-T records.
- Add "the root ruling on the A90 LO I1-T precondition" as an I-6 condition, recorded with its sha in D-4.
- Answer each 0606 item as text or as a root item.
- Add 0550, A90 and 0606 to the map's coverage section.

### A-07 — SHOULD_FIX — PREREG [C-I6] against [C-3.2] (R-GRID; P8)

**Quote.**
- [C-I6]: "No reading attributes a miss to a certified numerical quantity. The only registered numerical reading is R-TSR (§3), which A66 created."
- [C-3.2] P2: "**R-GRID:** k-grid fidelity at outer radii (A17: C3 is the criterion that matters)", whose deciding test is "the A17 C3 record".
- P8: "a mandatory check that ORIGINAL_K and the A17 C3 grid record agree".

**Defect.**
- R-GRID is a registered numerical reading, so I-6's sentence is false, and the two clauses conflict.
- R-GRID's deciding test and P8's check name the A17 tier-1 C3 record. That record is for grids that are not in use: G80C failed with e3 = 0.202.
- The in-use T120L grid passes C3 (A27). That counts against R-GRID, and it is not registered.
- There is no carrier for P8's check (rehearsal rough edge "P8"; 0606 item 4).

**Evidence.**
- V004 L75 (A17): "G80C has C3 max e3 = 0.202 … NOT ADEQUATE".
- V004 L365 and L370 (A27): "T120L | 1.2e-4 …" and "T120L, G120L, T160L and G160L all pass C2, C3, C4 and C1′."
- The NGC route uses T120L (0517; A60 "T120L 14/14 bitwise").

**Fix.**
- Either drop R-GRID, or restate it as a registered numerical reading. In the second case:
  - enter A27's T120L C3 record (e3 = 1.2e-4, pass) as evidence AGAINST it;
  - name a pinned C3 carrier for P8, or mark P8's check NOT_AVAILABLE with that reason;
  - amend the I-6 sentence.

### A-08 — SHOULD_FIX — PREREG [C-7] (D-1, D-2)

**Quote.**
- D-2: "**h_NN(0).** It is −1.899 ± 0.106 against −3.551, a gap of 15.6 SE."
- D-1: "**Outcome.** S0-FAIL-RHAT, TESTED-NEGATIVE as sealed. Analysis v003 completed 8/8. The maximum R-hat is 1.48, and 95 of 778 columns have R-hat above 1.1. The wiring reads WIRING_CHAIN_SPECIFIC."

**Defect.** Every figure quoted is exact, but the disclosure is one-sided.
- D-2 omits A65's qualifier in the same sentence: A2's own single chains bracket the stage-0 value. The 15.6 SE gap uses only the stage-0 SE.
- D-1 omits A63's other outcome lines.
- A65.4 requires disclosure of "the stage-0 outcome".
- Separately, D-1's "which is below A2 − 2 SE" has an ambiguous antecedent.

**Evidence.**
- V005 L1226: "h_NN(0) is −1.899 ± 0.106 against −3.551, a gap of 15.6 SE. A2's own single chains span −5.20 to −1.76."
- V005 L586–587: "R-LIT and R-MA fail." and "The background passes."
- V005 L1240: "disclose the stage-0 outcome, the SUPPORTED k = 0 reading with its untested gloss, and the 0.48 grid difference".

**Fix.**
- Add both A65 and A63 items verbatim.
- Write "stage-0 |h_NN(0)| = 1.90 ± 0.11 lies below A2 − 2 SE" (A63).

### A-09 — SHOULD_FIX — PREREG [C-4] (and CLAUSE_SOURCE_MAP row C-4)

**Quote.**
- [C-4]: "**Reporting.** INVALID rows are listed separately, per reason, with each row's zone."
- V001 §4 had: "the outer-gas cut (A12.5/A14 C3), with its truncation radius and mass fraction".
- The map's C-4 change text does not mention removing this.

**Defect.** r2 silently dropped V001's required report of the cut's truncation radius and the dropped HI mass fraction. Its own change log does not record the drop.

**Evidence.**
- V004 L19–20 (A14 C3): "Truncate the route-A gas roster at the first radius with an unconfined column." and "Record the dropped HI mass fraction."
- V003 L101 (A12.5): "record the mass fraction".
- v003g reads `first_unconfined_R_kpc` from the pinned cut record (L1753).
- 0535 records "the cut wiring, with the dropped-HI fraction recomputed".

**Fix.**
- Restore the report: for QUERY_BEYOND_OUTER_GAS_CUT, give the pinned cut record's sha, `first_unconfined_R_kpc` and the dropped HI mass fraction, per member θ under PER_THETA.
- Put the same in the §8 header.
- Record the change in the map.

### A-10 — SHOULD_FIX — PREREG [C-11], NUMBER_PROVENANCE, CLAUSE_SOURCE_MAP row C-I7, ROOT_ITEMS M-8

**Quote.**
- [C-11]: "Every other V005 entry predates V001 and was used there through V001's citations."
- Provenance "0519": "FROM_CODEX/0519 (section 11 pins it)", and the same for 0521 and 0523.
- M-8: "It follows the PROVISIONAL rule A50 uses for pending steps."

**Defect.**
- V001 cited only "A48 principle, 0518 / A55 log" from V005. Entries such as A50, A52 and A57 were never "used there".
- A50 is cited (map C-I7 and M-8) but not pinned in §11, and not in M-6's seal list.
- 0512, 0519, 0521 and 0523 are cited in the text (L56, L180–182) but not pinned in §11.
- The provenance file asserts pins that do not exist.

**Evidence.**
- V001 §9 V005 row.
- PREREG §11 dispatch table, which lists only 0518, 0522, 0524, 0531, 0535, 0545, 0546, 0548 and 0585.
- `grep` of the text: 0512 at L56; 0519, 0521 and 0523 at L180–182; 0550 absent.

**Fix.**
- Replace the sentence with an explicit list of the V005 entries used.
- Pin A50 by its section sha.
- Pin 0512, 0519, 0521, 0523 and 0550.
- Correct NUMBER_PROVENANCE.

### A-11 — SHOULD_FIX — ROOT_ITEMS M-6

**Quote.**
- Item 2: "the cited entries are A48, A56, A60, A62, A63, A64, A65, A66, A70, A81 and A82".
- Item 3: "Any V006 entry made before target access that touches the reading needs either a revision of this text or an explicit no-change note in the seal entry."

**Defect.**
- Item 3 covers only V006 entries. V005 entries after the last one read (A89) and before the V005 freeze are uncovered. A90 already touches the reading, and A91 exists.
- Item 2 checks only presence. The per-entry section shas would detect an edited entry; presence would not.
- A50 is missing from the list.

**Evidence.**
- V005 now holds A90 (L904 in `0753f2d8`, 18:49Z), A91 (18:54Z) and A92 (19:16Z, in `b7a900c4`). A90 touches the reading; A91 and A92 do not, but they still need the no-change note.
- V005 L1062 (A81 RI-26): "Any entry after A81 that touches the prereg text needs an r4 or an explicit no-change note".
- The seal tool `check_frozen_addendum_c4v001.py` header also checks "any entry after the last cited one that root's no-change list does not cover".

**Fix.**
- Item 3 should cover every V005 entry after A89 up to the V005 freeze, plus every V006 entry before target access.
- Item 2 should verify each cited entry's section sha, as T5 does, and add A50.

### A-12 — NOTE — CLAUSE_SOURCE_MAP, "Entries read with no change to this text"

**Quote.** "A61, A62, A67–A80 (driver, compare, launch packet and certificate work that does not alter how rows are read)" and "A83–A88 (…)".

**Defect.**
- The list contradicts the map's own row C-4, which cites A62.
- It contradicts PREREG §11, which pins A62 and A70.
- It omits A89, which §11 lists.

**Fix.** Make the map list equal to §11's list: A61, A67–A69, A71–A80 and A83–A89.

### A-13 — NOTE — ROOT_ITEMS M-10 and PREREG [C-6.1]

**Quote.** "**This is UNTESTED against real alternative members.** Whether ORIGINAL_K's members share log_index values with the PRIMARY's is known only after the freeze. NO_TWIN handles the case where they do not."

**Defect.** v003g refuses any freeze in which an evaluated alternative's members are not exactly the selected points, in log_index, role and order. So a twin always exists, and only "the twin is not valid" can produce NO_TWIN.

**Evidence.**
- v003g L3644 (`write_freeze_manifest`, "REFUSED (D2)").
- L3164 and L3184 (`_validate_manifest_impl`).

**Fix.** State the D2 guarantee. Keep NO_TWIN only for a twin with `member_valid` false.

### A-14 — NOTE — PREREG [C-I4], [C-3.2] P8 and [C-6.2]

**Quote.**
- I-4 table: "ORIGINAL_K | state | EVALUATED_BEFORE_FREEZE".
- P8: "P8 triggers a mandatory check that ORIGINAL_K and the A17 C3 grid record agree."

**Defect.** The A16.2 contingency is not integrated: root may change ORIGINAL_K to NOT_EVALUATED before step 5. Neither P8's mandatory check nor R-GRID's "against" test is defined when ORIGINAL_K is NOT_EVALUATED or its twin is invalid.

**Evidence.**
- V004 L60 (A16.2): "If its evaluation at the selected members does not fit the budget at freeze time, root records the change to NOT_EVALUATED_BEFORE_FREEZE before step 5."
- Slots V003 `alternatives_note`: "(root records any change before step 5)".

**Fix.** Add the contingency to I-4 and §6.2. Define P8 and R-GRID as NOT_AVAILABLE, with the reason, in that case.

### A-15 — NOTE — PREREG [C-3.1] (DT-S1, DT-GEO) and [C-3.2] (R-GEFF)

**Quote.**
- "Calibration transfer across parameter space (V005 S1)."
- "NOT_EVALUATED_BEFORE_FREEZE (A16.1); the forward refuses with GEOMETRY_NOT_EXPOSED".
- "stellar share about 0.51 (DDO154: about 0.03) (A21, E1)".

**Defect.**
- No calibration-transfer "S1" exists in the V005 addendum. Its S1s are compare and comparator items, at L101 and L690. The UNTESTED transfer question is in A21 (V004).
- GEOMETRY_NOT_EXPOSED is A16.4, not A16.1.
- The 0.51 and 0.03 figures come from A10 (V003 L44), not from A21 or E1.
- All three are carried over from V001.

**Fix.** Re-cite DT-S1 to A21 ("Still UNTESTED: whether γ_eff ≈ 3e41 encodes …"). Cite A16.4 for the refusal, and A10 for 0.51 and 0.03.

### A-16 — NOTE — ROOT_ITEMS M-12 (and PREREG [C-I3])

**Defect.** The sealed classifier should state three things.
- (i) The A71 rule, "no tool may be last-wins anywhere", is satisfied: strict JSON with `object_pairs_hook`, and duplicate rows or ids refused.
- (ii) The envelope label is matched by prefix. In MODE_D_FIXED, v003g emits `POINTWISE_ENVELOPE_NOT_A_REALIZABLE_CURVE; conditional on DDO154 D=4.04 and i=66 (A13/A23)`, at L184 and L932–936.
- (iii) How it relates to Codex1's rehearsal classifier (0603; `steps6_7_rehearsal_cx1/`, 14/14, all 13 readings reachable). That classifier is rehearsal only, which is 0606 item 5.

**Fix.** Add these three points to M-12.

### A-17 — NOTE — PREREG [C-3], [C-6.3] and [C-8]

**Quote.**
- §3: "The 43-row score can make a reading **consistent** or **inconsistent**" and "A reading whose deciding test has not run stays OPEN, whatever the score shows."
- §6.3: "**CONSISTENT** … **AGAINST** … **NOT_DECIDED**".

**Defect.** The status vocabulary has no stated mapping.
- For R-UT1, R-HIST, R-REACH and R-TSR, whose deciding tests are NOT SCHEDULED, both "consistent" (from the score) and "OPEN" (untested) apply.
- §8 allows only one of consistent, inconsistent or OPEN.
- DT-S0G's three outputs are not mapped to those three either.

**Fix.** Report two fields per reading: score bearing (consistent, inconsistent or none) and test status (OPEN or tested). Map CONSISTENT to consistent, AGAINST to inconsistent, and NOT_DECIDED to none.

### A-18 — NOTE — PREREG [C-11] (the A65 section pin)

**Defect.** A65 is the last heading in V005, so its pinned section runs to the end of the file: V005 L1215–1287. That span includes the trailing block: the 0512 N3 ruling, the 0518 contract, Codex2's review, the lane expansion and the withdrawal.
- Any append at the end of the file would break the A65 pin, even though it would not change A65.
- The pin also certifies content unrelated to A65.

**Fix.** Note this in §11. Cite 0512 and 0518 by their own dispatch pins, which 0518 already has.

## 3. Coverage: rulings and dispatches since V001 that touch the NGC reading

| item | integrated in r2? |
|---|---|
| A60, gap rows and cut binding (0535) | yes ([C-4]) |
| A62, two-pass freeze (0545 F5) | yes ([C-4]). The map's no-change list contradicts this (A-12). |
| A63, the stage-0 outcome | partly. D-1 omits R-LIT/R-MA and the background (A-08). |
| A65, STAGE0_GRID_OUTER, check R-3 and the disclosure (0548) | yes, but D-2 omits the A2 chain span (A-08) |
| A64.1, C1′ scope | yes |
| A64.2, K_big 32, N3′, coverage 91 (0546, 0549) | yes |
| A64.3, N1 on production records | yes (M-7) |
| A66 and 0550, the N1 consequence, flag and gate | the flag and R-TSR yes. 0550 is not cited. The gate is mis-stated (A-01). The support rule is not applicable (A-02). |
| v003g INVALID-as-miss (0531/A56, 0545) | yes, but the description is inaccurate (A-05) |
| A70, v003g PASS | yes |
| A81 RI-22 θ/20; RI-23 M_s 96/128 | yes, as conditional. The resolved state (Codex1 0032) is not registered (A-06). |
| A82, V005 closes; V006 | yes (M-6), but the later-entry gap remains (A-11) |
| A52.4 and 0512, NGC I1-T | no (A-06) |
| A71, no last-wins (classifier) | no (A-16) |
| A16.2, ORIGINAL_K contingency | no (A-14) |
| A27, T120L passes C3 (bears on R-GRID and P8) | no (A-07) |
| A90, K32 N-tests: N_FAIL_N1, gate OPEN, LO I1-T open | no; it post-dates assembly (A-06) |
| 0603 and 0606, the rehearsal's rough edges for r2 | no; they post-date assembly (A-06). Items 2, 4 and 6 match A-02, A-07 and A-01. |
| A61, A67–A69, A71–A80, A83–A89, A91, A92; dispatches 0605 and 0607–0609 | no reading change found, apart from A71 (A-16) and A87's LO_NGC V002 being reported only in V007 (correct as stated) |

**The 0585 minimum, item by item:**
- A60 gap rows: integrated.
- A63/A65 stage-0 outcome and STAGE0 with its disclosure: integrated, with disclosure gaps (A-08).
- A64/A66 K_big 32, N3′ and the N1 consequence: integrated, with defects A-01 and A-02.
- The freeze v003g INVALID-as-miss rule: integrated, with a description defect (A-05).
- A81 RI-23: integrated as a conditional, with the resolved state missing (A-06).

**V001's five root items.** All five survive in substance as M-1 to M-5: tiers with σ-multiples rejected; cuts 10/30 with the 2.2 R_d alternative; thresholds; NOT SCHEDULED, with later preregs left to root; inputs bound to the successor through a field map. M-1's reasoning (c) and its NEAR semantics are defective (A-03).

## 4. Root items: are the recommendations consistent and soundly reasoned?

| item | assessment |
|---|---|
| M-1 | Recommending (a) is acceptable only with A-03's fix. Reasoning (c) is false. |
| M-2 | Consistent with A15 and A65.3. A65.3 defines the STAGE0 scope by this OUTER zone, which strengthens the reasoning. |
| M-3 | Sound. The P5 vacuity argument is correct. |
| M-4 | Consistent with 0524 and A63. |
| M-5 | Consistent with A70 and 0071. Every field name exists in v003g. |
| M-6 | Sound in outline, but gaps remain (A-11). |
| M-7 | Not applicable to the actual record, and the reasoning is unsound (A-02). |
| M-8 | Sound. A50 is cited by analogy and should be pinned (A-10). |
| M-9 | Consistent with A65 and check R-3. The vocabulary mapping is missing (A-17). |
| M-10 | The rule is sound, but the UNTESTED claim is wrong (A-13). |
| M-11 | Acceptable. A15 E1's deciding observable is preserved in (a). The change class "CHANGED" has no ruling behind it, by the map's own definition. |
| M-12 | Sound. Add A71 and the rehearsal link (A-16). |
