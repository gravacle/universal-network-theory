# S2 findings: carriers, evidence and root items (Claude3 lane, helper S2)

Reviewed: Codex3 step-5 readiness `claude_artifacts/step5_ngc_route_ab_readiness_cx3/`: READINESS_REPORT_CX3V001.md c7c72d54, and the 0606 carrier successor `carriers_0606_v001/` (FROM_CODEX3/0618 8939c004). Tasks: FROM_CODEX/0594 19e874ec and 0606 item 3 (dbb80c77). Root dispatch: FROM_CODEX/0617 622f5cc9. Lens: carriers, evidence and root-item claims, refuted by default. S1 covers the filler, templates and dry plans.

Nothing was launched. No NGC3198 target or observed velocity file, no C5H run, no runs_ext/UVT_* tree and nothing under /.vol was opened, except my own synthetic file in the /.vol probe, and the fence blocked that open. Every write was an exclusive create under this directory. `taskpolicy -b` was accepted every time. All Python ran as `python3 -I -B` with single-thread BLAS env.

## VERDICT: PASS_WITH_FINDINGS. 0 BLOCKING, 5 SHOULD_FIX, 11 NOTE

Every evidence quote is faithful to the cited bytes. Every count claim reproduces. The three carriers are honestly UNAVAILABLE in the saved output, and nothing is fabricated or renamed PASS. All 93 main adversarial cases behave as claimed, with 0 fence refusals. The findings are in three areas:
- the extractor's target fence is narrower than claimed;
- some joins are missing;
- the A93 / r006 retirement is recorded in the successor but has not reached the 0594 operational layer, and ROOT_ITEMS is out of date.

**Why SF1 is not BLOCKING:**
- No code path opens anything outside the root's sha-pinned request.
- The actual saved request opened only seven target-free files.
- A mis-pinned file is hashed and refused, never parsed or emitted.

The lead may escalate SF1 if a fence gap alone counts as "a target read path exists".

## 0. Pins (sha256 from bytes): all match
- The lead's pins all match: report c7c72d54; carriers REPORT 50f4278e, DECISION 8762a1b5, REGISTRY 04d8cff3, extractor v005 50c7db5f, CARRIERS_AVAILABLE_SAVED_CX3V005 a0e608c0, independent REVIEW 87eef799, HASHES f587d1ad, carrier POLICY 311ceedd; freeze RUNBOOK 9557b5aa, freeze module 48a1e48a, slots V003 d3859b42.
- The other cited files also match: CARRIER_CONTRACT 252ef9e1, SOURCE_AUDIT 8dbfc2c4, RUNBOOK 1b0e3903, READINESS_DELTA 89aaa8f6, ROOT_ITEMS_V002 3e9e31d4, LATEST_COORDINATOR_EVIDENCE b9566900, FREEZE_EXPECTED_INPUTS_V002 169df91f, LAUNCH_ORDER_V002 829a8cb6, WALL_MODEL cf3c1c29, and all 10 K32 record/certificate pins.

## Findings

### SHOULD_FIX

**S2-SF1. The extractor's target fence is lexical, and it reads before it checks the sha (claim a).**
`safe_path` refuses only these:
- lowercase paths containing `/runs_ext/uvt_`, `kmax_a2f10_c5h_run_v001` or `/.codex/`;
- `ngc3198` plus observed/velocit/rotmod/target (after the token target_free is removed).

`read_pin` then reads the whole file before it compares the sha.

What the probes showed, using my own synthetic files (logs/ATTACK_RESULTS_S2_V001.json):
- **F1.** A `/.vol/<dev>/<ino>` path is accepted, because `resolve()` returns it unchanged. The extractor then tried to open it, and my fence blocked the open (DOTVOL).
- **F2.** A hard link with an innocuous name is opened (DENY_INODE).
- **F3.** These names are all accepted: `NGC_3198_observed.json`, `NGC 3198 rotation.json`, `N3198_vobs.json`, `UGC5572_rotation_curve.json`, `MassModels_Lelli2016c.mrt`, `NGC3198_vrot_obs.dat`, `ngc3198_HI_kinematics.json`, `NGC3198_TARGET_FREEvel.json`.
  - The slots' own provenance says "rotmod header and MassModels D agree", so the program holds a MassModels catalogue. Its name contains no galaxy string.
- **Static reading.** Non-regular files are not refused: a device has st_size 0 and passes the cap, and it is then read without bound.

Consequences:
- Target-freedom rests on the root's request pins, not on the guard.
- RUNBOOK's sentence "Protected run/target paths are rejected before file reads" holds only for lexically recognisable names.
- The independent parent guard (probe v003) uses the same lexical rules, so its "zero audit events" does not test this.

Fix:
- Open the file first. Then call `fstat`, require S_ISREG, and either require `st_nlink == 1` or check an inode allow-list.
- Use `fcntl(F_GETPATH)` to get the canonical path, and re-run the lexical check on it **before** reading.
- Refuse `/.vol`.
- Read at most MAX_BYTES+1.
- Add the aliases and catalogue terms ngc_3198, "ngc 3198", n3198, ugc5572, massmodels, vobs, rotcurve.
- Better: use an allow-list of artifact roots.

**S2-SF2. The ORIGINAL_K join is incomplete (claim b).**
`ORIGINAL_K_SHARED_POINT_GRID` compares only `physical` (without entropy_K_factor) and `coefficients`.
- An ORIGINAL_K call with different `numerics` (uv_tail K_big 16, truncation cube), a different schema/interface, or different `source_slots` is accepted, and P8 reads AVAILABLE (A7i, A7j).
- The slots define ORIGINAL_K as "entropy_K_factor 1.0 instead of 64/121 … at the same selected points".
- Fix: compare the full normalized call spec except physical.entropy_K_factor, label and any interface-specific route_a_inputs, or bind both calls to a root-registered spec pair.

**S2-SF3. The A93 r006 retirement is recorded but not propagated (claim h).**
It is a supersession that is properly recorded, not a silent contradiction. But it has not reached the 0594 operational layer.

Recorded in the 0606 successor:
- REPORT: "A93 supersedes the prior readiness's pending-acceptance statement".
- REGISTRY: `r006_fallback_status: RETIRED_BY_A93`, with the scope "Supersedes old pending r007 acceptance prose, without editing prior files".
- READINESS_DELTA: "Old r006 fallback must not be selected for new launches".
- The carrier POLICY accepts r007 only, and 0618 says the same.

Still stale in the 0594 layer:
- STEP5_REGISTRY_CX3V002, which the report names as "the operational registry", says `"default_until_external_acceptance": "r006_fallback"`.
- The selected filler `fill_step5_cx3v003.py` (2348974f) with POLICY 4f0d7d03 still registers `r006_fallback`. It fills specs for a handoff that names that branch with a null acceptance pin (L149–163).
- LAUNCH_ORDER_V002 step 1, ROOT_ITEMS R3 and FREEZE_EXPECTED_INPUTS first_pass still name the r006 fallback.

Neither tool policy accepts cx3r008 (577f8c94, built in 0624; external delta and root adoption still pending). The extractor refuses an r008 result with DRIVER_CUSTODY (A2j).

Fix: issue a step-5 registry and filler-policy successor that refuses r006 and pins the root-adopted driver, and a carrier-policy successor alongside it.

**S2-SF4. Carried payloads get no target-field content screen (claims a and f).**
- The opaque A17-C3 payload (up to 1 MiB) and the native ring objects are copied verbatim. These are all carried into the pre-freeze carrier (S1–S3, synthetic numbers):
  - a C3 payload with the v003g P46 target-row shape {id, velocity, sigma};
  - a C3 payload with an `observed_velocity_km_s` key;
  - a compare ring with a `vobs_km_s` key.
- v003g already screens root documents (`_scan_forbidden` / `_root_target_screen`).
- Fix: apply the same screen to every parsed input before emitting.

**S2-SF5. ROOT_ITEMS_CX3V002 is incomplete and not superseded (item 6).**
- It is dated 18:56Z, before A93 (19:31Z), the 0606 carriers (19:50Z) and the cx3r008 build (0624).
- The successor's open items sit only in READINESS_DELTA prose.
- 15 open dependencies are missing; they are listed below.
- Fix: issue ROOT_ITEMS_CX3V003.

### NOTE
- **N1. Untyped refusals.** These cases fail closed with no output, but they raise a plain ValueError rather than a typed Refusal. CLI `main` does not catch it, so the run ends with a traceback and exit 1 (A4e, A4e2, A4g, and the CLI log):
  - `1e999` in an unchecked field (ring `criterion_over_theta`) becomes inf, and the error comes late from `encode(allow_nan=False)`;
  - an integer of more than 4300 digits escapes `strict_json`.
  - A missing file is FileNotFoundError, which the CLI catches (REFUSED, exit 2).
  - Fix: add a parse_float hook that rejects non-finite values, and map ValueError to a typed Refusal.
- **N2. point_key is a free root label.** It is never joined to the call spec's physical point. The same model rows under keys 1…1 and 2…2 were both accepted (A7h). The RUNBOOK documents this; root must define how the key is derived.
- **N3. The E1b model readout is not bound to the headline alternative or the reference member.** A readout on the stage-0 grid bdb9016c was accepted as the E1b model (A7k). Prereg M-11(a) specifies "the reference member's parameters".
- **N4. The ntest_compare is not bound to its required context.** It is not tied to production K_big 32 (A64.3) or to an OPEN gate. `failing_non_TRUNCATION_SHAPE_rings` and `checks` are not carried. A K16 compare with a BLOCKED gate gave TSR AVAILABLE (A7n). `ntest_state` still shows the BLOCKED gate.
- **N5. Authenticity rests on the root request sha (a documented trust boundary).** In SAVED mode, a fabricated readout without the synthetic flag is accepted (G1). Newtonian definition text, Newtonian producer identity (even the UNT driver itself) and C3 record identity (even the model's own result.json) are taken on assertion (S5–S7). Contract adoption should say how authenticity is established.
- **N6. The LO_NGC_K32 last shell is a D-cap.** The (64,91] shell is "D cap {|k|>64} of cylinder 64 … not the complete spherical shell". "Covers [2,91]" is the record's own coverage field, so the quote is faithful. The nuance is not carried into the report.
- **N7. Claude4's M-7 framing differs between texts.**
  - The prereg round-1 ROOT_ITEMS_R2 M-7 text says "[r_lo, r_hi] exactly as stored". The stored support is a single point, so that flags nothing.
  - 0090/0091 recommend the ring-14/16 neighbour interval, which flags Q25.
  - R12 quotes the latter faithfully. Root should cite the final (r3) M-7 text.
  - From the N1 ring radii (9.9018, 10.5408, 10.9117) and the slots radii: point → none; midpoint cell → none; open or closed neighbour interval → exactly Q25.
- **N8. Two values are fixed in code rather than read from records.**
  - E1b INNER is hard-coded as `ids[:24]`. That matches the prereg zone table (R_q < 10 kpc at 13.8 Mpc), but M-2 is not adopted.
  - TSR support bounds are compared with manifest radii at the registered 13.8 Mpc geometry. That is moot while geometry sensitivity stays NOT_EVALUATED (A16.1).
- **N9. FREEZE_EXPECTED_INPUTS does not list several `write_freeze_manifest` inputs.**
  - The missing inputs:
    - `parameter_region` (with bounds_semantics);
    - `observation_rule`;
    - the coordinate spec;
    - the DDO154 observation-region file in input_files;
    - the `notes` used by A16.1/A13;
    - `allow_incomplete` (FREEZE_INCOMPLETE, prereg M-8).
  - These are step-4/freeze-owned, and v003g refuses when they are missing, so they are not silently dropped.
  - v003g also has no vehicle for the TSR flag record or the E1b/P8 carriers (M-7 options a/b).
- **N10. A point-in-time pin is labelled "live".** LATEST_COORDINATOR_EVIDENCE `live_root_observed_pin` shows the live V005 path with its build-time sha 0753f2d8. The live file is now 70a48f51 (A91–A101 appended). The snapshot pin is correct.
- **N11. The registry is read but unused.** The extractor reads cd30429c but does not use it. That registry holds 8 dry-readiness fixture specs, so filled step-5 specs are not members. It serves custody only.

## Claim-by-claim (1a–1i, 2–5)

**(a) PARTIAL; see SF1 and SF4.**
- Static AST:
  - the only read site is `read_pin` → `Path.read_bytes()` (L97), plus the extractor's own `__file__` (L273);
  - the only write is `p.open('xb')` (L285);
  - imports are argparse, datetime, hashlib, json, math and pathlib only;
  - there is no listdir, glob, os.walk, subprocess or network call.
- Every file it can open:
  1. the request (CLI);
  2. the POLICY, whose sha is fixed in code (311ceedd);
  3. from the policy:
     - the r007 driver (bytes only);
     - the registry (parsed, unused);
     - slots V003 (ids and radii);
  4. model readout: result, finish and call spec;
  5. ORIGINAL_K readout: result, finish and call spec;
  6. ntest_compare;
  7. tsr_support;
  8. newtonian_reference, plus its second-level `producer_pin` (bytes only);
  9. the A17-C3 registration, plus its second-level `record_pin` (copied verbatim);
  10. its own source;
  11. the output (exclusive create).
- Metadata-only calls: resolve(), stat() and is_dir().
- The actual saved replay (P1) opened exactly these: the request, the carrier POLICY, the r007 driver, the r007 registry, slots V003, the K32 compare, its own source, and the xb output. CX3V005 was opened by my harness for comparison, not by the extractor. Fence refusals: 0.

**(b) Output exclusive-create: CONFIRMED.**
- An existing file, a dangling symlink and a directory each give FileExistsError, with bytes unchanged and no symlink target created.
- A missing parent gives OUTPUT_PARENT_REQUIRED.
- A protected output name gives PROTECTED_RUN_PATH.

Joins that exist are strict:
- driver, call, finish and result shas;
- statuses and validity;
- row id order;
- compare pin path+sha;
- slots pin;
- point label;
- entropy;
- Newtonian ↔ model call, C3 ↔ ORIGINAL_K call.

The missing joins are SF2, N2, N3 and N4.

**(c) CONFIRMED.**
- The saved carriers keep the exact ring: ordinal 15, R 10.540847190215317, S/θ 1.01481832531416, criterion C1, radial_support sampled_ring.
- They keep `outcome: N_FAIL_N1`, `tests_read: true`, `n_route_ab_gate: OPEN` and `reason_codes: [TRUNCATION_SHAPE_RESIDUAL_ONLY_A66]`.
- The only "PASS" token in the file is inside the sentence "Never infer agreement from two PASS strings".

**(d) CONFIRMED.** All 43 rows read `TRUNCATION_SHAPE_RESIDUAL: null` with `ring_evidence: null`. Flags become booleans only when a support record is supplied. Note that "adopted" is not verified beyond the request sha (N5).

**(e) CONFIRMED.**
- Saved reasons: NO_SAVED_ROUTE_B_READOUT, NO_PRE_FREEZE_BARYONIC_NEWTONIAN_CARRIER, NO_ROOT_PINNED_A17_C3_RECORD, and UNAVAILABLE_NO_REGISTERED_AGREEMENT_PREDICATE.
- A scoped grep of the pinned r007 driver and the four pinned sources (9b5ce82a, 51ab097c, 7ae28901, aee7af12) finds no Newtonian, v_bar/gbar, A17/C3 or TSR-flag emission. The only hits are hex digests, "pc3", and QUERY_OUTSIDE_SUPPLIED_RADIAL_SUPPORT.

**(f) CONFIRMED.**
- P2: with all three carriers, only Q25 is flagged under a closed [R14,R16], and E1b has 24 rows.
- P4: comparisons give [None, None, False, False, None, True] for invalid / Newtonian-above / invalid-Newtonian / normal rows.
- P5: a COMPLETED_INVALID model keeps its rows and reasons, and E1b is UNAVAILABLE.
- P6: PASS strings in the C3 payload infer no agreement.

**(g) CONFIRMED.**
- Boolean entropy is refused for both headline and ORIGINAL_K (A5g, A5l).
- A support that excludes its ring is refused, for a closed interval and for an open endpoint at the ring (A6b, A6c).
- Point and neighbour supports are accepted (P2, P3).

**(h) RECORDED SUPERSESSION, NOT PROPAGATED; see SF3.**

**(i) CONFIRMED from bytes.**
- Carriers HASHES: 2109 entries, all matching, with 0 unlisted and 0 missing files.
- Prior 0594 HASHES: 316 entries, all matching, with 0 unlisted and 0 missing files, and no edits after 0618.
- TESTS_CX3V004: 64/64.
- Independent out_v003: 44/44, guard [].

**2. Evidence: FAITHFUL.**
- LO_NGC_K32 07745bbf: PASS, coverage [2.0, 91.0]. The nuance is N6.
- EPS_NGC91 1d5eef1b: CERTIFIED, NGC [2,91].
- GQ_NGC_91_MS96 be148bab: PASS, M_s 96, k [2,91].
- K32 compare 6f095f64:
  - N_FAIL_N1 with tests_read=true;
  - gate OPEN, with the sole reason TRUNCATION_SHAPE_RESIDUAL_ONLY_A66;
  - one failing TRUNCATION_SHAPE ring at ordinal 15 (R 10.540847190215317, S/θ 1.01481832531416), and no non-TSR failures;
  - N0, NQ, N2, N3 (N3′ cutoffs 16/64), LO_NGC and I1T_NGC all true, and N4 REPORTED_ONLY.
- In the evidence JSON:
  - lo scopes are byte-equal (parsed) to LO cert i1t.scope / i1t.not_run;
  - failing_rings and the record pins equal the compare and its manifest.
- Root A66 and A90 text (snapshot 0753f2d8) agree.

**3. Root items R11 (A90) and R12 (A66): stated correctly and present.**
- I1T 3ae7981a is iteration_0 only, at nodes |k| up to 3.374.
- The NOT_RUN item is tail-domain (2,91] star-transform convergence. Its deciding test is quoted verbatim in the evidence JSON.
- For R12, see N7.

**4. Freeze inputs vs v003g: CONSISTENT.**
- The 43 ids equal the slots.
- The six-alternative declaration equals the slots (parsed).
- The 4 NOT_EVALUATED names are explicit: ML_3p6_0.4, ML_3p6_0.6, GL10_SOURCE_GAUSS_ORDER and STAGE0_GRID_OUTER.
- OUTER Q36–Q43 equals:
  - the rows with R ≥ 30;
  - the stage-0 scoring_scope;
  - stage0_registration.outer_rows.
- Denominators: OUTER 8, headline and ordinary alternatives 43, and null INVALID counts as a miss.
- ORIGINAL_K is EVALUATED_BEFORE_FREEZE and "needs separately registered results".
- The A66 disclosure is present and ROOT_UNRESOLVED.
- The query manifest and route-B config pins equal the slots.
- See also SF3 (stale r006) and N9.

**5. WALL_MODEL: PASS.**
- Status is UNTESTED_SCIENTIFIC_WALL_TIME.
- 15.07 and 25.07 h equal the source's 1-worker `hours_16_iterations_UNTESTED` at 2496 and 4992 columns (ADMITTED_POINT_RESOURCE_PLAN 4de87df9; logs/VERIFY_EVIDENCE_S2_V001_SUPPLEMENT.txt).
- The file says this is "not a valid K32 lower/upper bound", and the integrated bound is "UNTESTED/unavailable".
- KHI 7.84 h / 13.86 h is labelled "C4T-KHI only".
- The file says "Never use these projections as failure/admission thresholds".
- Nothing in it is presented as a bound.

## Missing from ROOT_ITEMS_CX3V002

1. **A93 pre-step-5 closures.** ST7-SF1, ST7-SF2 and PAR-TB-1. Per 0624, cx3r008 577f8c94 is built and PAR-TB-1 is accepted narrowly under A98.1, but the external delta review and root adoption are pending. Also A93's rule that root checks the full driver sha from bytes before every NGC launch.
2. **Step-5 driver adoption, r007 or cx3r008, with matching successors.** The filler policy, the STEP5 registry and the carrier policy all need successors, because both current tool policies refuse or mislabel r008. Claude4 says r008 is needed whenever a step-5 spec declares an outer-gas cut.
3. **R3 itself is stale.** It must become "r006 retired (A93)".
4. **M-11 (E1b Newtonian carrier).** It needs a producer, an owner, a baryonic definition and a reference-member binding, or a NOT_AVAILABLE ruling.
5. **M-13 (P8).** It needs the A17-C3 record selection and its pairing with ORIGINAL_K member(s). No agreement predicate is registered.
6. **Root adoption of CARRIER_CONTRACT_CX3V001.** That covers the request and the three optional root-record schemas, plus the authenticity statement (N5).
7. **Vehicle for carriers and the TSR flag record in the freeze.** v003g has no field: M-7 option (a), a separate pinned record, or (b), v003h. The ruling must say whether they go into input_files or notes, and whether the target-field screen applies (SF4).
8. **The point_key derivation and binding rule** (N2).
9. **The ORIGINAL_K pair definition at the spec level.** Same numerics, source and interface as the headline (SF2).
10. **M-2 zone-table adoption.** The INNER Q01–Q24 used by E1b depends on it (N8).
11. **Prereg items.** M-6 and M-12 (seal vehicle and sealed classifier, 0606 item 5) and the r2→r3 prereg under A98.2, including the I6 wording (0606 item 6).
12. **M-8: the FREEZE_INCOMPLETE scoring policy** (`allow_incomplete`).
13. **Per-point applicability of the saved-state K32 N-test.** That N-test was run on the saved T120L operator at θ 3.366e-9. A90's "The A66 consequence applies at step 5" implies reuse at the step-4 admitted points; confirm it explicitly.
14. **The TSR support coordinate frame.** It is kpc at the registered 13.8 Mpc manifest radii, which is moot while geometry sensitivity is NOT_EVALUATED (N8).
15. **The optional B-only replay policy successor** (LAUNCH_ORDER step 3), needed only if a saved route-A replay is wanted.

## Adversarial totals and fence counts
**Main suite** (scripts/attack_extractor_s2_v002.py, logs/ATTACK_RESULTS_S2_V001.json): 93 cases, 93 as expected, **S2 fence refusals 0**.

| Group | Cases |
|---|---|
| Positive controls (P) | 6 |
| A1 missing pin | 10 |
| A2 sha mismatch | 11 |
| A3 duplicate JSON keys | 6 |
| A4 NaN / Infinity / 1e999 / big integers | 9 |
| A5 bool where a number belongs | 12 |
| A6 ring absent from the support | 9 |
| A7 join-key collision | 16 |
| A8 output exists | 7 |
| G contract | 7 |

**Fence probes:** 4 cases, **S2 fence refusals 2**, which is the expected evidence of the gap.
- F1: /.vol path, refused as DOTVOL.
- F2: hard link, refused as DENY_INODE.
- F3: lexical-only, no open (results above).
- F4: symlink control, refused by the extractor itself, 0 fence refusals.

**Supplementary** (scripts/attack_extractor_s2_supp_v001.py, logs/ATTACK_SUPP_RESULTS_S2_V001.json): 8 cases, all accepted, which is the expected evidence for SF4 and N5. Fence refusals 0.

**Evidence and manifest verification** (scripts/verify_evidence_s2.py, logs/VERIFY_EVIDENCE_S2_V001.json): 69/70. The 1 failure was a parser bug in my own harness, re-checked as PASS in the supplement. Fence refusals 0.

**Fence:** scripts/fence_s2.py. It refuses:
- /.vol;
- runs_ext/UVT_* and C5H;
- NGC3198 aliases together with observed, target or velocity terms, and rotmod/MassModels catalogues;
- inodes on a deny list;
- writes outside S2 or without exclusive create;
- deletes, renames, subprocess and network calls.

It is a strict superset of Codex3's definition. The step-5 and carrier POLICY files themselves define no target paths; the definition lives in `safe_path`. Ordinary uvt_* source modules are not refused.

**Script history:** scripts/attack_extractor_s2.py (v001) was never run. v002 removes two dead or duplicate blocks from it.

**Files:** all are under this directory; HASHES_S2.txt lists them all.
