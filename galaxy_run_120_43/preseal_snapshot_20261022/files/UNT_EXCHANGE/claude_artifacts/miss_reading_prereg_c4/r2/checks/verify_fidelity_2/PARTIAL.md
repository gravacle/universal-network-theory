# PARTIAL — verify_fidelity_2 (adversarial verification of fidelity finding A-02)

Started: 2026-10-18T19:19:03Z (date -u)
Lane: Claude4 helper. Authority: dispatch 0585 (sha256 9003633293ff1db7d5153cabc338fd058cc199d834976b05543b7603b9433abd, verified from bytes), 0592.
Object: r2/round1 — all 10 files in HASHES_R2.txt verified from bytes, all match.

## Status
- [x] folder created, object hashes verified
- [ ] read finding A-02 in fidelity REVIEW.md
- [ ] read r2 text: ROOT_ITEMS M-7, PREREG [C-1.4], [C-9], [C-3.2]
- [ ] read evidence: K32_COMPARE_COMPLETE_V001.json, 0550, A66, A90, v003g L1658
- [ ] repro R3 with synthetic/target-free radii only
- [ ] verdict

## Progress at 2026-10-18T19:25:19Z
- Quotes checked: all three M-7 quotes present verbatim in ROOT_ITEMS_R2.md L138, L140, L145; [C-9] quote at PREREG L371 (prefix "Residual risk (not closed)." omitted in finding, no change of meaning).
- K32_COMPARE_COMPLETE_V001.json sha 6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9 (from bytes): radial_support = {kind: sampled_ring, R_kpc: 10.540847190215317}; no r_lo/r_hi. CONFIRMED.
- Producer ntests_compare_k32_cxv003.py (283193be...) L2: "Failing ring support is the sampled radius, not an invented finite radial interval." L26 always emits kind sampled_ring. BUILD_K32_COMPLETE_V001.md L9 says the same. Strengthens the finding.
- N1 record of record K32_RECORDS_COMPLETE_V001_N1.json (8867c376...) stores ring_radii_kpc[100] (points), no per-ring interval either. Ring 14 = 9.901810628740723, ring 16 = 10.911721936765339.
- Core.SHAPE = (1..8,10,13,14,15): ring 15 is the outermost TRUNCATION_SHAPE ring; ring 16 is NOT_GRID (C1').
- 0550 L11 quote verified (sha 5c686ae8...). 0550 absent from all r2 files (grep). CONFIRMED.
- v003g L1658-1660 exact roster key set CONFIRMED; write_freeze_manifest input_files accepts any regular non-empty file (_pin_files L3491).
- V005 read at 19:20:35Z: 50fe0f1c0f3d9d4f9acc8a44677b7d37b2b7c96e682ee2f0c2c270cb8c0a7477 (newest entry A92).
- Early observation: the finding's own fix example (ring-neighbour midpoints) gives support [10.2213, 10.7263], which contains NO query (Q25 10.04, Q26 11.04): it also empties the flag. "Any cell-width alternative is knife-edge" is over-stated for that rule (margins 0.18/0.31 kpc).

## Progress at 2026-10-18T19:33:10Z
- Repro (tools/repro_R3_vf2.zsh, shell+jq+awk, target-free inputs sha-checked): RULE0 point flags none; ring - Q25/Q26 midpoint = +0.000847190 kpc; nearest query Q26. Finding's R3 CONFIRMED.
- Fix example 1 (ring-neighbour midpoints, from the N1 record ring radii) = [10.221328909, 10.726284563], flags none (0.181 kpc margin). Fix example 2 (bracketing rows) flags Q25, Q26 (0.50 kpc margins). Query cell / ring +- half query spacing flag Q26 only (0.000847 kpc: knife-edge).
- tools/repro_R3b_vf2.zsh: the 100 N1 rings are GL4 nodes on 25 panels uniform in R, GL4 in s=R^2 (residual 4e-15). Ring 15 = node 4 of panel 3, R in [8.028514559, 10.704686079]: panel rule flags Q23, Q24, Q25 (0.0115 kpc at Q23). GL4 weight cell [10.2894, 10.7047] flags none.
- Author's own posts after the round-1 freeze (FROM_CLAUDE4 0090 226c1c57, 18:52:44Z; 0091 118fab4b, 18:59:25Z) already state the point support "flags no query row" and recommend the open ring-14..ring-16 interval, which flags Q25 only. Corroborates A-02 as a real defect of round 1.
- Distinct flag sets from plausible rules: none / {Q25} / {Q26} / {Q25,Q26} / {Q23,Q24,Q25}.
- Over-statements found in A-02: "any cell-width alternative is knife-edge" (false for ring-based cells); its fix example 1 also empties the flag; evidence calls the compare output "the N1 record" (N1 record of record is K32_RECORDS_COMPLETE_V001_N1.json 8867c376, also points only).
- Process note: one shell call echoed a string starting with '=' (zsh =cmd expansion error, no effect on files); not repeated.

## Final at 2026-10-18T19:38:50Z
- VERIFY.md and REVIEW.md written. Verdict: A-02 NOT REFUTED; SHOULD_FIX confirmed; fix_sufficient = false (three gaps, refined fix in VERIFY.md §7).
- V005 last read 19:34:37Z: 6145a1f92cbace8d36f86a7c15be4d79ee6992717a5c57438cdd62045e070c7c (newest A93; no ruling on M-7).
