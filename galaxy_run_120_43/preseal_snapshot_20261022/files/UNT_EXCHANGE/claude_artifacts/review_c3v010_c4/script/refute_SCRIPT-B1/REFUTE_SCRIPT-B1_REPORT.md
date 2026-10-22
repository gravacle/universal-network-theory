# REFUTE_SCRIPT-B1: adversarial refutation of lens SCRIPT finding SCRIPT-B1 (Claude4 delta of SELECTED c3v010)

Helper of UNT lane Claude4. Scope A115. Started 2026-10-19T06:56:19Z; report written 2026-10-19T07:12Z (`date -u`).
Folder: `review_c3v010_c4/script/refute_SCRIPT-B1/` (only `REFUTE_SCRIPT-B1_*` files; the lens's files were not touched).

## Verdict: NOT REFUTED. Final class (b); it is also reachable under (a). BLOCKING for c3v010 as selected.

If root had run SELECTED c3v010 (script c3v026) with the selected env block on the real inputs, the seal would have completed. Its E-SEAL1 would then have carried B0_RO1 and B0_N3 as MISSING, although their registered pre-seal records exist and read PASS. Nothing in c3v026 refuses that.

Every link of the claim is now checked from bytes (TESTED), including the one the lens left FORMAL (that the real ROOT-mode step 8 gives the same MISSING).

**Status after the brief was written:**
- Root upheld the finding as **A123** (06:42Z, V006 addendum, now `0e4d70ef`): "BLOCKING, class (b), and class (a)".
- Root ruled the fix (0667, `92a1aa78`) and **sealed with SELECTED c3v011 / script c3v027 `239a51c3`** at 07:00Z (0669, `9a704b22`).
- c3v010 was therefore never sealed. The finding is moot operationally, but it is correct, and it is the cause of c3v011.

## The claim, link by link (all from bytes this session)
| # | link | evidence | mark |
|---|---|---|---|
| L1 | The selected tuple pins the V009-era manifest | c3v026 `b43cc38b` L258 pins `MANIFEST_GATES_ONLY_DRAFT_C3SA.json` `e5967bb9` (the bytes hash to it). Step 8 uses it at L682 and L686. SELECTED c3v010 `1f62deb4` names it as `selected_tuple.gates_manifest_draft`. README c3v010 `a43c36a7` L16 calls it "step-8 manifest draft (unchanged)". | TESTED |
| L2 | It leaves exactly two V012 pre-seal gates null | V012 `4b8a3c35` has 15 sha-list gates. The manifest names 13 of them; the unnamed ones are exactly `[B0_N3, B0_RO1]`. All 13 named records' bytes are registered. Manifest note: "registry V009 ... null = not built (B0_N3, B0_RO1, I4: fail closed)". | TESTED |
| L3 | The two records are genuine, of record, and pass | `ri33_c3/b0_ro1/B0_RO1_RECORD_C3V001.json` = `332452b7` and `ri33_c3/b0_n3/B0_N3_RECORD_C3V001.json` = `dd1dd912`, both equal to V012 `gate_records`. VALIDATE_R14_C3V012 `a7c80f8e` reads both PASS on r14. | TESTED |
| L4 | r14 reads a null path as MISSING and gates-only exits 0 regardless | r14 `f3f9ba7e` (ast, not run): `evaluate_gate` L3790 starts with an If at L3794, `path is None or not Path(path).is_file()` -> `status='MISSING'`, `GATE_RECORD_MISSING:<g>`. `read_gates` L5528 iterates ALL_GATES. The gates-only branch (L5810) has a single `return 0` and reads no status. `NO_RUN_GATES` L419 contains B0_RO1 and B0_N3. | TESTED (source) |
| L5 | **Real ROOT-mode step 8 on e5967bb9 gives MISSING** (the lens had this FORMAL) | Root's rehearsal (A123, 06:41Z): helper `gates-only --mode root`, sealed compare `83fa73d7` (= c3v010 dry run passA, hashed), real identity trees. stderr: rc 0, fence_refused 0, 10127 entries scanned. GATES_ONLY `4f374bdb` (stdout identical): test_mode false; Z2, Z2-OFF and B0prime_RERUN valid. B0_RO1 and B0_N3 read MISSING with `record_sha256` null. The other 13 pre-seal gates PASS and the 10 after-seal gates are MISSING. Its statuses equal dry run passA's. | TESTED (bytes of root's run) |
| L6 | Nothing later in c3v026 refuses that body | Mirrored checks (c4v002: regex constants read from source by ast, logic copied, originals never executed) on body `4f374bdb`: the step-8 row-value scan passes; step-8 C-03 passes (`C03_SLOT_GATES` covers only EPS, LO, GQ, DOUBLING, LO_NGC, B1, B1_OFF and B0prime_RERUN; the draft c3v007 slot shas equal passA SLOTS_FINAL's); step-10 tool 4 v004 `b6_codes` passes (schema, blinded, test_mode, route mode `parallel8`, number tokens, row rule). Tool 4 `b6_codes`/`build` never read a status, and L539-540 embed the text verbatim. The slot draft has no B0_RO1, B0_N3 or manifest entry. Guard v008 and launcher v007 never mention e_seal1 or gates_only. | TESTED (mirrored) |
| L7 | c3v026 would not refuse earlier on the real inputs | Root's real c3v027 run passed ALL STEPS on those inputs (0669). c3v026 and c3v027 differ in exactly one non-comment line, the MANIFEST_GATES pin. Manifest c3v002 `46dc5310` = e5967bb9 with only B0_RO1 and B0_N3 set to the two record paths (other keys equal), so step-8 `check-manifest gates-root` on e5967bb9 checks a subset of what passed. The dry run of record (c3v026 itself) passed all 13 steps on the same MISSING verdicts. | TESTED + FORMAL (composition) |
| L8 | The verdict sealed instead would have been PASS | The actual sealed E-SEAL1 `e7938c6b` (c3v027 run) shows B0_RO1 PASS `332452b7`, with the 3 identity-run crossrefs present and equal, and B0_N3 PASS `dd1dd912`. All 15 V012 pre-seal gates PASS. The only gates that differ from the e5967bb9 rehearsal are `[B0_N3, B0_RO1]`. | TESTED |
| L9 | The text of record requires them | r6 `d28c95f5` srr[0]: "...the identity-gate records and the RO1 replay; their output goes into the seal record (E-SEAL1)" (A46 RA13). run_list.replays names "B0_RO1 replay (RA5 b)". gates_before_any_T_result lists both. r14 L4542: "RA13: gates on real records before the seal". A113 RI-33: "built before the seal". | TESTED (text) |

## Refutation attempts (all failed)
- **R1. The real ROOT mode differs from the dry run (identity runs present, crossrefs).** Failed: root's own real-mode rehearsal on e5967bb9 reads MISSING for both (L5).
- **R2. A later step refuses the MISSING body, so the defect would be a refusal, not a wrong seal.** Failed (L6). The dry run of record also passed every step with it.
- **R3. c3v026 fails earlier on real inputs, so the defect is unreachable.** Failed (L7).
- **R4. The records are not genuine, or would not PASS in sealed ROOT mode with crossrefs.** Failed (L3, L8).
- **R5. E-SEAL1 need only cover the gates the manifest names.** Failed for B0_RO1 on the letter of srr[0]. For B0_N3, see NOTE R-N1; it is covered by RI-33, RA13 and A123.
- **R6. The omission was disclosed or accepted by root.** Failed. SELECTED c3v010 contains neither gate name. 0665 and A107-A121 are silent. A123 rules the opposite.
- **R7. No physics reading changes, because the post-run full compare re-reads the gates with its own manifest.** Does not refute.
  - E-SEAL1 is sealed irreversibly. It would state MISSING for two NO_RUN gates whose verdict on the genuine records is PASS: a sealed gate verdict that differs from the genuine one (A115 (b)).
  - The RO1-replay output that srr[0] requires would be missing from the seal: failing to seal a required element.
  - If a post-run manifest also omitted them, r14 full mode would read INCOMPLETE (L4539-4542, L4571). That is FORMAL and not needed for the class.

## Class
- **(b):** the sealed E-SEAL1 would carry the wrong verdicts for B0_RO1 and B0_N3 (MISSING instead of PASS), and it would omit the srr[0] RO1-replay evaluation, a required element.
- **(a):** the defect is reached by honest pinned producers (the c3v010 tuple and its pinned manifest), the selected env block and the real records, with no forged input (L5-L7).
- Root's A123 gives the same class.

## NOTEs (non-blocking; on the lens's reasoning, not on the finding)
- **R-N1.** The letter of srr[0] names "the identity-gate records and the RO1 replay". It does not name B0_N3, a static scan of driver r5. B0_N3's place in E-SEAL1 rests on A113 RI-33 (built before the seal), RA13 (r14 L4542) and A123's done-when ("every pre-seal gate registered in V012 reads PASS"). B0_RO1 alone suffices for the finding.
- **R-N2.** The lens's step "the real ROOT-mode run gives the same MISSING verdicts" (FORMAL there) is TESTED here, from root's rehearsal bytes `4f374bdb`.
- **R-N3.** The V006 addendum changed after the brief's reading: A122, A123 and A124 were added, and it is now `0e4d70ef`. The lens's "no ruling A107-A121" stands for those entries; A123 then confirmed the finding.
- **R-N4.** Hardening (the lens's N5), confirmed: no c3v026 step requires every V012 pre-seal gate to read PASS in GATES_ONLY. C-03 covers 8 slotted gates only. Root's A123 register says the same.

## Files written (sha256 from bytes)
- `REFUTE_SCRIPT-B1_check_c4v001.py` `7ebc7b1af3c97d81486d3a2d8e04e7f815dc5b5426c05bf41c5bcbdc1a3d44b7`. Its output is `REFUTE_SCRIPT-B1_CHECK_c4v001.json` `d2843db3ed1cefe2a0f48ff09b7c324368b78e7820f05dfc6935211ae97895cc`: 17 of 17 checks true, 18 of 18 expected shas match.
- `REFUTE_SCRIPT-B1_check_c4v002.py` `0ef97e468383db3602087ea012fd3e666d60a448025d379ced8c7805ec36415a`. Its output is `REFUTE_SCRIPT-B1_CHECK_c4v002.json` `8344b20c4d97982c4906104998fd70a04501fcc8c496a6becb8b86378ca4ff9b`: the mirrored checks pass on the real-mode MISSING body.
- `REFUTE_SCRIPT-B1_PARTIAL.md`: append-only; its final sha is in the structured output. This report's sha is there too.

## Rules and fence
- **Fenced runs.** Both runs went through `tools/run_fenced_c4st2.py` (fence c993d34c, runner fe904509, unmodified). FENCE_C4ST2_SUMMARY for each: selftest 8/8, probes 15/15, `blocked_after_selftest []`.
- **No other Python.** There was no python -c, no heredoc Python and no system python.
- **Nothing launched.** The seal script, the dry-run scripts, the helper, the runner, the compare, tool 4, the guard and the launcher were read as text or ast only.
- **Protected paths never touched.** Nothing under runs_ext (either spelling), UVT_*, UNT_INTERNAL_RUNS, the C5H run or target data was opened, listed or stat'ed. The manifest's identity_runs path strings were read only as JSON text.
- **CLAUDE2 files read.** Only named, unprotected files, all blinded or text:
  - the V005 and V006 addenda;
  - root's rehearsal folder `V007_STEP2_LAUNCH_ROOT/STEP8_ROOT_REHEARSAL_V001/` (listed, with its `out/`; stderr.json, stdout.txt and out/GATES_ONLY.json read);
  - `V007_SEAL_ASSEMBLY/E_SEAL1_GATES_ONLY.stdout.txt`, plus a hash of SEAL_RECORD_V007.json, which equals 0669's `a9646fe3`.
- **Searches.** grep was used only on single named files.
- **Writes.** Only in this folder, by exclusive create (set -C or `open(...,'x')`) or by append to my own PARTIAL.
- **Incidents.** None.
