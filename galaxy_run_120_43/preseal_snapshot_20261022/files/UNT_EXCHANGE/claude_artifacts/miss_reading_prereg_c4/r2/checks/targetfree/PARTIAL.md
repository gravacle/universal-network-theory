# Lens B (target-free and blinding) review of miss-reading prereg r2 round1 -- PARTIAL

Started: 2026-10-18T18:48:30Z (date -u)
Status: in progress. Object hashes verified from bytes (all 10 entries of HASHES_R2.txt match shasum -a 256).

## Findings so far
(none yet)

## Progress log
- 2026-10-18T18:56:49Z: read all r2 files (prereg, map, root items, provenance, check JSON, mutation JSON, INDEX, HASHES, 3 tools). V005 read at review: sha256 0753f2d8dc437592a4ad70140f309c774837cb07e9c04e2c213c4421eeb8e87e (snapshot in snapshots/V005_AT_REVIEW.md); it now holds A90 and A91, added after r2 assembly (assembly sha 17cb4fd4..., last entry A89).
- Leads being tested: T4 checks token values not occurrences (listed small integers pass anywhere); superscript/zero-width/number-word evasions; hook not installed in generator/test runs; T5 per-entry pins blind to later amending entries; A90 (NGC K32 N-tests complete) not reflected.
- 2026-10-18T19:01:29Z: reran the check CLI (with its hook) on round1: PASS, identical to TARGET_FREE_CHECK_R2.json apart from the T5 note that V005 is now 0753f2d8 (runs/CHECK_RERUN_AT_REVIEW.json). Reran the mutation test: 14/14 (runs/MUTATION_RERUN_AT_REVIEW.json).
- 2026-10-18T19:01:29Z: adversarial harness tools_lensb/adversarial_check_lensb.py: 37 of 38 target-like mutations PASS the check (runs/ADVERSARIAL_RESULTS.json). Only the control (indexed symbol with an unlisted value) FAILs.

## Findings so far (draft ids)
- F-T4-VALUE (SHOULD_FIX): T4 checks token values, not occurrences; any listed number (all digits 0-9, 778, 93.6, 96, 128 ...) can carry a target value; plus superscript/zero-width/bold-split/number-word/sci-notation/glued-identifier/8-digit/section-sign evasions; T4 scans the prereg only (not ROOT_ITEMS or the map); provenance categories are self-declared.
- F-T1-DENYLIST (SHOULD_FIX): T1 is a 7-substring, 7-extension deny-list on 3 files; .txt/.json/.tsv/.data/.dat_v2, THINGS/de Blok, fullwidth/soft-hyphen spellings, the provenance JSON and the INDEX are not covered.
- F-T2T3 (part of the above): T2 misses Unicode minus, middle dot, division slash, words, m/s, cm/s; T3 misses code-span or escaped symbols, indexed symbols, approx-sign variants and 'is/of' phrasing.
- F-T5-NAME (NOTE/SHOULD_FIX): T5 judges a pinned source target-free by its path string only (a synthetic target-named JSON pinned in section 11 passes).
- F-HOOK-NOT-INSTALLED (NOTE): the generator and the mutation test call T.run() with no audit hook; the bundled PASS was produced unhooked (CLI rerun matches).
- 2026-10-18T19:11:32Z: T5 probe (tools_lensb/t5_v005_amendment_lensb.py, runs/T5_V005_AMENDMENT_RESULTS.json): T5 PASSes when a later V005 entry amends A81 RI-23 (E01), when an uncited entry withdraws A66.2 (E02), and with headings 'A81a:' / 'A66 amendment' (E07, E08). In-place edits, duplicate headings and EOF appends FAIL as they should. The real V005 at review (0753f2d8, with A90/A91) PASSes silently.
- 2026-10-18T19:11:32Z: hook probe (tools_lensb/hook_probe_lensb.py, runs/HOOK_PROBE_RESULTS.json, runs/HOOK_PROBE_PART3.json): refuses deny-listed opens and write-mode opens; allows os.truncate (canary truncated 17 -> 0 bytes under the hook), mkdir, symlink, hard link, chmod, exec/posix_spawn/fork, listdir/scandir of deny-listed dirs, C5H/UVT_ paths, other source names, fullwidth spellings, and an open through an innocently named symlink. T.run() as called by the generator and the mutation test runs with no hook.
- 2026-10-18T19:11:32Z: K32 N-test record of record (K32_COMPARE_COMPLETE_V001.json 6f095f64...) stores the failing ring's radial_support as {kind: sampled_ring, R_kpc: 10.5408...}: a point, not [r_lo, r_hi]. M-7's 'exactly as stored' rule flags no row; neighbouring N-test rings are 9.9018 and 10.9117 kpc; Q25 10.04, Q26 11.04. Flag set depends on an unfixed definition.
- 2026-10-18T19:11:32Z: semantic leads: seal and M-item rulings may come after NGC predictions (public knowledge of the observed curve); STAGE0 adoption and root-listed gates are discretionary after predictions; non-mechanical 'against' conditions (ORIGINAL_K same excess, DT-T1a move by the miss, onset radius, P8 agree, post-freeze DT-GEO); single-status report ambiguity; no first-score-final rule (I-7, CLASSIFICATION_INPUT_DEFECT); later deciding tests may reuse opened rows.
- 2026-10-18T19:14:58Z: provenance located in sources (runs/PROVENANCE_LOCATE.json): every value found in a target-free source; 0.03 and 0.51 occur only in V003 A10 L44 (cited as 'V001 3, A21/E1'); 0519/0521/0523 claimed 'section 11 pins it' but section 11 does not pin them. Naming sweep of all 11 r2 files: text files name no target file, source or value; tools carry deny-list names and realistic-magnitude synthetic velocities (150.2 km/s; v_q = 151 for Q40; 147.3).
- 2026-10-18T19:14:58Z: TSR flag set by candidate support definition (runs/TSR_FLAG_SET_BY_DEFINITION.json): point as stored -> none; neighbour midpoints -> none; neighbour rings -> Q25; two rings each side -> Q24,Q25,Q26; +-0.5 kpc -> Q26 only (Q25 misses by 0.0008 kpc).
- Next: write REVIEW.md and HASHES.txt.
- 2026-10-18T19:18:03Z: REVIEW.md written. Verdict PASS_WITH_FINDINGS: 0 BLOCKING, 8 SHOULD_FIX (B-1 to B-8), 4 NOTE (B-9 to B-12). Status: complete; HASHES.txt follows.
