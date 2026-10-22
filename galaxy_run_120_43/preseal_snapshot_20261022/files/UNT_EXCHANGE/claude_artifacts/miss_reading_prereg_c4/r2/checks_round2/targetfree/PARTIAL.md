# R2-C target-free and tools lens: PARTIAL

Started: 2026-10-18T19:56:47Z

## Status
- Folder created.
- HASHES_R2.txt verified from bytes: all 10 listed files match (shasum -a 256). HASHES_R2.txt itself = 2e3cf0c60088f23a9530a3ab5b8d8ec1a2d8c5184a7eeff11f726fafa964c6fd.
- Next: read every round-2 file fully, then the tools; then mutation tests.

## Findings so far
(none yet)

## Update 2026-10-18T20:06:35Z
- Read fully: INDEX_R2, PREREG_R2 (621 lines), CLAUSE_SOURCE_MAP_R2, ROOT_ITEMS_R2, NUMBER_PROVENANCE_R2, TARGET_FREE_CHECK_R2 (with census), TARGET_FREE_MUTATION_TEST_R2, the three tools.
- Round-1 lens B REVIEW and verify_targetfree_1/2 VERIFY read.
- V005 now cf9bbf19eae3d2fb0262c31c3a0af43ecc2f100b9295c4075a591716b6ebb9dc (snapshot snapshots/V005_AT_R2C.md, 20:05:18Z); assembly was 991cc242. New: A97 (20:02Z) and A98 (20:04Z; "miss-reading prereg r2 needs r3", Codex2 0490 FAIL). No V006 file exists. V004 487d4449 and V003 5bef6552 match.
- Check CLI rerun (hooked): target-free PASS, currency FAIL (A97, A98); exit code 0 despite currency FAIL. runs/CHECK_RERUN_R2C.json.
- Mutation test rerun: 26/26 cases ok individually, all_ok False (baseline currency FAIL), so later_entry_uncovered is now vacuous. runs/MUTATION_RERUN_R2C.json.
- Next: fenced adversarial harness (round-1 lens-B cases re-run on v002 + new round-2 cases), provenance verification from bytes.

## Update 2026-10-18T20:22:00Z
- Provenance: all 23 NEW entries (and post 0071) verified from bytes: runs/PROVENANCE_VERIFY_R2C.json. N1 rings == GL4 nodes bitwise (100); ordinal 15 == node index 15; derived rule flags Q25 only; metre form same; zones 24/11/8.
- Cited but unpinned V005 entries: A47, A71, A80 (listed as "read with no change").
- Adversarial harness (tools/adversarial_r2c.py -> runs/ADVERSARIAL_R2C.json): controls 6/6 + baseline OK; 92 of 105 attack mutations pass; round-1 lens-B replays: 13 fixed, 23 still pass (21 attack + 2 stated limits).
- Stripped inventory on real bytes (runs/STRIPPED_INVENTORY_R2C.json): nothing hidden that is a quantity; PASS on actual bytes stands.
- Bundled TARGET_FREE_CHECK_R2.json == rerun except T5 V005 note and T7 (A97, A98).
- Assembly V005 991cc242 (closure lens copy, read-only) had headings to A96; only A97/A98 added since.
- Draft findings: B1 T7 currency FAIL (A97/A98; A98 = r2 needs r3). SF: INDEX overclaims; closure B-8/B-9 'FIXED' inaccurate; T4 stripping holes; T1-T3 deny-list gaps; T5 pin coverage (A47/A71/A80; silent skip); T7 mechanism (complement list, open ranges, heading forms, V006). NOTEs: end-marker, mutation test, exit code, provenance labels, Status wording, M-6 curve-shape sentence, hygiene.
- Next: write REVIEW.md and HASHES.txt.

## Final 2026-10-18T20:26:57Z
- V005 moved again: 7f552858be77888ff1e3abc4d490e7e88ca5a16374bad84ad8ae043686b39fa2 at 20:25:33Z (adds A99 20:20Z, A100 20:24Z); snapshot snapshots/V005_AT_R2C_2.md; check rerun runs/CHECK_RERUN_R2C_2.json: T7 later A97-A100, 14/14 pins match, target-free PASS.
- REVIEW.md written: FAIL (1 BLOCKING, 6 SHOULD_FIX, 7 NOTE). Target-free on its bytes: yes. Seal-ready: no.
- HASHES.txt written last (sha256 of every other file in this folder).
