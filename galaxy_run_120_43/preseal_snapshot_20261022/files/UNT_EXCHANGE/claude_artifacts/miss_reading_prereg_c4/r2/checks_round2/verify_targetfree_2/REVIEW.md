# REVIEW: verify_targetfree_2 (adversarial verification of round-2 lens targetfree finding R2C-S1)

- **Written** 2026-10-18T20:47:51Z (`date -u`) by a Claude4 helper, under dispatches 0585 and 0606, with checks under 0592. I wrote only in this folder and did not edit the object.
- **Full verification:** `VERIFY.md`, sha256 `48d92d5d2a503cf9d81de3db4c523e73ae5e111cfe8d37f928e1e9fcd9654a6d` (re-hashed at 20:49:12Z, after §7 gained the disclosures below).
- **Disclosures:**
  - One `mv -n` rename, inside this folder only (`HASHES.txt.build` → `HASHES.txt`), breached the letter of the "no moves" rule. Nothing outside this folder was moved, and nothing was deleted. HASHES.txt is now written in place.
  - A stray file, `HASHES.txt.new_unused_marker_ignore`, was created by mistake. It now holds a one-line note saying it is unused, and it is left in place.
- **Object:** `r2/round2/`. All 10 HASHES_R2.txt entries match.
- **V005 read:** `7f552858be77888ff1e3abc4d490e7e88ca5a16374bad84ad8ae043686b39fa2` at 20:35:53Z, which is the snapshot the harness used. Then `5a996e97d633cc11a4cb255fe8ba1cdf746d93367621c004aca29382affb6a26` at 20:44:30Z, which adds A101; the 14 pins still match.

## Result

| item | answer |
|---|---|
| finding | R2C-S1: INDEX_R2's "Checked from bytes" (L21–26) claims more than the tools check |
| refuted | **no.** The core is CONFIRMED from bytes; five sub-points are overstated |
| severity assessed | **SHOULD_FIX** (agrees with the lens) |
| fix sufficient | **no, as written.** The literal-scope branch works with six refinements. The "fix the tools (S3–S6) and keep the claims" branch does not |

## Key facts (from bytes)

- **The defect is real at L22 and L23.**
  - **"in any text file" (L22).** T1–T3 scan only PREREG, MAP and ROOT_ITEMS (check L20). Read bundle-wide, the claim is false: the check tool has 15 T1–T3 hits and the test tool 9, by design. INDEX and the provenance JSON are clean (0 hits) but are never scanned. Seven file-scope injections all PASS while the same line FAILs T1–T4 in ROOT_ITEMS or PREREG:
    - F01, INDEX;
    - F02a/b/c, provenance `uses`, `note` and category text;
    - F03, an unused key;
    - F04a/b, a new .md and a new .json file.
  - **"node radii are verified" (L23).** The TSR ring's own radius 10.54 kpc (PREREG L174, L439; node 15 = 10.540847190215317) is declared MODEL_DIAGNOSTIC. Changing it to 10.55 PASSes, while 10.91 → 10.92 (declared NODE_RADIUS) FAILs. The value 10.54 is right.
  - **The deny-list wording (L22).** It is a residual of round-1 B-7. That finding's fix item 6 asked for "checked against a deny-list and a listed-value inventory". The wording was not adopted, but MAP L104 says "INDEX wording narrowed".
  - **The text is boilerplate.** It is fixed text in the generator (L128–138), written whatever the verdict.
- **L24 and L26 hold for round 2.**
  - §11 has 51 sha-bearing lines and all of them parse, including all 14 pin rows.
  - V005 has only standard `## A<n>:` headings, and T7 lists A97–A100 (A101 now).
  - Both claims over-reach only as template text, for later rounds.
- **Overstated sub-points:**
  - "never reads V006" is not an INDEX claim: L26 says V005, and V006 is S6(d).
  - `listed_but_absent` does not contradict L23.
  - NODE_DERIVED 10.22 and 10.73 are not query or node radii.
  - The T5 skip surfaces in T7: the dropped A66 is listed, so currency FAILs.
  - The n ≥ 47 filter is at L350.
  - The F01–F04 summary is imprecise: F02 has no forbidden term, and F03 has no term and no unit.
- **The fix.**
  - Narrow the wording in the generator template, in either branch.
  - Name the three files.
  - Restate T5 and T7 literally (T7 uses `\b`, not ':').
  - Narrow L11 as well.
  - Write the limits abstractly.
  - Add the cheap tool items:
    - scan the provenance strings and keys;
    - fail T4 on `listed_but_absent`;
    - fail on unexpected files;
    - re-declare 10.54 as NODE_RADIUS node 15 (probe: PASS today, catches 10.55);
    - fail T5 on an unparsed A-row.
  - Do not add INDEX to TEXT_FILES. The generator writes INDEX after the check, and INDEX pins the check result, so scan INDEX in the generator before writing it.
