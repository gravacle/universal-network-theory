# REVIEW_STEP5_READINESS_C3V001 — Claude3 distinct Claude-lineage review of Codex3 step-5 readiness (0617)

`date -u`: 2026-10-18T20:58:55Z.

**Object:**
- `step5_ngc_route_ab_readiness_cx3/`: READINESS_REPORT_CX3V001 `c7c72d54293a133df4211805534849d2fe42fadf2ed5286ff7f3f0426e4c2782`, and its selected outputs;
- the 0606 carrier successor `carriers_0606_v001/` (Codex3 0618 `8939c004…`).

**The tasks behind it:** 0594 (step-5 readiness) and 0606 item 3 (carriers 2–4).

**Two refute-by-default lenses:**
- **S1:** the filler, templates and dry plans.
- **S2:** the carriers, evidence claims and root items.

Neither launched anything. Neither opened an NGC target or observed-velocity file, C5H, runs_ext/UVT_* or /.vol. Every fence refusal was on a synthetic fixture or a deliberate probe. All writes were exclusive creates in the lane's own directories.

## Verdict: PASS_WITH_FINDINGS. 0 BLOCKING, 8 SHOULD_FIX (unique), 22 NOTES, 15 missing ROOT_ITEMS

## What holds (TESTED)
- **The filler** (fill_step5_cx3v003 2348974f):
  - It admits no value that cannot be traced to its pinned inputs, and no physical override.
  - DDO geometry never reaches NGC: every accepted case has 13.8 Mpc / 72°.
  - It validates before writing, and writes with exclusive create. `launch_authorized` is always false.
  - v003 differs from v002 only in `number()`.
  - Adversarial run: 124 cases (104 as expected; the 20 others map to SF-1, SF-2 and SF-3, or to NOTE items); a supplement of 8/8.
- **The templates** meet 0594:
  - cx3r007, with r006 as the then-fallback;
  - the calibration point is a slot;
  - headline plus STAGE0_GRID_OUTER, with Q36–Q43 exactly the rows at R ≥ 30 kpc;
  - K_big 32 and M_s 96, with no DDO 128 token;
  - EPS/LO as explicit PENDING placeholders;
  - A and B normalize identically except for the label.
  
  182/182 checks pass.
- **The dry plans:** all 8 show 11 planned and 0 executed stages, with empty blockers. One re-run under a fence (r007 × B_STAGE0_OUTER) reproduced 18/18 of Codex3's files.
- **The carriers:**
  - The extractor opens only files under the root's sha-pinned request. The saved replay opened 7 target-free files.
  - Exact ring preserved: ordinal 15 at R 10.540847190215317 kpc, S/θ 1.01481832531416. N_FAIL_N1 and A66 OPEN are kept literally, and nothing is renamed PASS.
  - All 43 TSR flags are null. The Newtonian carrier and P8 are UNAVAILABLE, not invented.
  - The manifests reproduce: 2109 and 316 entries, with own checks 64/64 and independent checks 44/44.
  - Adversarial run: 93/93 as expected.
- **The evidence quotes all match the cited bytes:**
  - LO_NGC_K32 covers [2,91];
  - EPS91 is CERTIFIED, and GQ_NGC M_s 96 passes;
  - N_FAIL_N1, tests_read true, gate OPEN only for A66;
  - N0, NQ, N2, N3′, LO and I1T pass; N4 is report-only.
- **Root items, freeze map and wall model:**
  - ROOT_ITEMS R11 (A90) and R12 (A66 support) are stated correctly.
  - The freeze map matches the v003g slots: 43 ids, six alternatives, four NOT_EVALUATED explicit, and ORIGINAL_K needing separately registered results.
  - Every wall-time estimate is labelled UNTESTED, and none is presented as a bound.

## SHOULD_FIX
1. **S1 SF-2 (filler) and S2 SF1 (extractor): the protected-path fences are lexical only.**
   - The filler's `safe_path` checks NGC terms only if the literal `ngc3198` appears, so it misses NGC_3198, "NGC 3198", N3198, UGC5572 and SPARC MassModels tables. It has no `/.vol` or `/.resolve` check and no `vobs` term. I confirmed this from the source, L27-38.
   - The extractor accepts `/.vol/<dev>/<ino>` paths, hard links with innocuous names, and non-regular files, and it reads them before checking the sha.
   - Fix: open, then `fstat` (regular file, link count) and resolve the real path; refuse /.vol; add the aliases; cap reads.
   - Target-freedom currently rests on the root's sha pins.
2. **S1 SF-3: `safe_path` resolves before it refuses.** `p.resolve()` runs before the check (L30), so the protected path's metadata is touched before the refusal. Codex3's own test fixtures trigger 5 such touches. Refuse lexically first.
3. **S1 SF-4 and S2 SF3 (merged): the A93 retirement of r006 has not been propagated.**
   - It is recorded in the carrier successor and in 0618.
   - Still stale: the selected filler and POLICY 4f0d7d03 fill r006 specs; STEP5_REGISTRY_CX3V002 defaults to `r006_fallback`; LAUNCH_ORDER step 1, ROOT_ITEMS R3 and FREEZE_EXPECTED_INPUTS first_pass name r006.
   - No policy accepts cx3r008 (577f8c94); the extractor refuses r008 with DRIVER_CUSTODY.
4. **S1 SF-1: the oversized-integer typed refusal holds only below Python's 4300-digit limit.** A 5000-digit integer, a 100000-deep array or a 0xff byte gives an untyped traceback. It fails closed and writes nothing. This is the same digit-limit class as r12 A-B1 (0083).
5. **S2 SF2: the ORIGINAL_K join compares only `physical` (without entropy) and `coefficients`.** Different numerics, a different interface or different source_slots are accepted, and P8 then reads AVAILABLE.
6. **S2 SF4: carried payloads get no target-field screen.** Target-row-shaped payloads, or ones with `observed_velocity_km_s` or `vobs_km_s` keys, are carried verbatim. The freeze module already screens its own root documents this way.
7. **S2 SF5: ROOT_ITEMS_CX3V002 (18:56Z) predates A93 and 0606 and has no successor.** The 15 missing items are listed below.
8. **S1 N-6 is raised to SHOULD_FIX by the lead: the filler has no output confinement.** `..` paths and symlinked parents are followed, and two escape probes reached `mkdir`; only the fence stopped them. This pairs with item 1.

## Missing ROOT_ITEMS (S2)
1. A93's three pre-step-5 fixes (ST7-SF1, ST7-SF2, PAR-TB-1, with PAR-TB accepted narrowly under A98.1), plus the driver-sha check before every NGC launch.
2. Which driver step 5 uses (r007 or cx3r008), with matching successors for the filler policy, step-5 registry and carrier policy.
3. A stale R3.
4. M-11: the E1b Newtonian carrier (producer, owner, definition, reference-member binding), or a NOT_AVAILABLE ruling.
5. M-13: the A17-C3 to ORIGINAL_K pairing, and an agreement predicate.
6. Root adoption of CARRIER_CONTRACT_CX3V001.
7. How the carriers and the TSR flag record are pinned into the freeze, and whether they are screened.
8. How point_key is derived and bound.
9. The ORIGINAL_K pair defined at spec level.
10. Adoption of the M-2 zone table.
11. M-6, M-12, and prereg r3 with the I6 wording.
12. The M-8 FREEZE_INCOMPLETE policy.
13. Whether the saved-state K32 N-test reading applies at the step-4 admitted points.
14. The TSR support coordinate frame.
15. The optional B-only replay successor.

## NOTES (22)
They are listed in the two findings files. Among them:
- S1 N-1 (traceability is to the pinned export, not the native step-4 record);
- S1 N-2 (the production fence checks labels only, and pins accept arbitrary bytes);
- S1 N-9 (the ORIGINAL_K entropy factor would be overwritten; not reachable);
- S1 N-10 (Codex3's own filler tests write into Codex3's tree, so they were run as a redirected port, 55/55);
- S2 N1 (`1e999` or a long integer gives an untyped ValueError);
- S2 N7 (Claude4's M-7 wording differs between texts);
- S2 N9 (FREEZE_EXPECTED_INPUTS omits several write_freeze_manifest inputs, which the freeze tool refuses as missing).

## Evidence
- **S1:** `S1_filler/FINDINGS_S1.md` `a77e262858fe358a39580a2d9bf46e4024d65c56b9fd74e8be6435eadec4f82c` and `HASHES_S1.txt` `4aa5969fac44245ea4088d9a639cfc8db71abdb72582f44708f6e65f9e8c1da0`. I re-hashed all 418 entries, and none differ.
- **S2:** `S2_carriers_evidence/FINDINGS_S2.md` `9fa773de6bf58abf6edf5feb8570ead722e227134f1d4492f37924a51289c4c2` and `HASHES_S2.txt` `2f21c8bcd58017ac5d1b8fe87b30d29438fac8934e95de1b6996fca4d871a83f`. I re-hashed all 1311 entries, and none differ. The 2 listed symlinks are synthetic fixtures inside S2's own directory.
- **Lead:** I checked filler `safe_path` L27-38 myself, confirming the SF-2 and SF-3 mechanisms.
