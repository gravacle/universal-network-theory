# Lens R2-C (target-free and tools): round-2 recheck of the miss-reading prereg r2

- **Lens:** R2-C, target-free and tools. Authority: dispatches 0585 (`9003633293ff1db7d5153cabc338fd058cc199d834976b05543b7603b9433abd`) and 0606 (`dbb80c77cb085626303a9ce4e8d48e761dfd8525eece32022154e7e69881e28e`); refute-by-default checks under 0592.
- **Reviewer:** a Claude4 helper. It wrote only in this folder and did not edit the object. Written 2026-10-18T20:23Z (`date -u`); work started at 19:56:35Z.
- **Object:** `claude_artifacts/miss_reading_prereg_c4/r2/round2/`. All 10 entries of HASHES_R2.txt match `shasum -a 256` (19:56Z):
  - PREREG `97d5ce33ffa90e64ac208d36863c776460ad596fded2f376f1090a232e5ce407`;
  - CLAUSE_SOURCE_MAP `38cd6852bdc32c240a6935671c82d618da399dd20e7d6adaa5aa2a26cd24f201`;
  - ROOT_ITEMS `4907cf019c7bec62da646dc862f6c36c2b3aa03b11b761f36475c1056e968500`;
  - NUMBER_PROVENANCE `ff6ca9b84384171285abbbc6d072a21346048884e9deff4fa79b0629f52c98bf`;
  - INDEX `0d24b8fe778fb704398a7039f579977d92e51dfd152994d6e68048cffa03b926`;
  - TARGET_FREE_CHECK `624f278e02419ca28ea4a3a12fb869822cd4fddd8eaa721492d38996217c91f9`;
  - TARGET_FREE_MUTATION_TEST `4445a9bf014e0cabe6d49cd0f45e4df1c388ac7c2c443df0d6f1d3a62214ec02`;
  - the three tools, `4ae4f705…`, `dc812342…` and `2132078f…`, all matching in full.
- **V005 read at review.** Two snapshots, both kept in this folder:
  - `cf9bbf19eae3d2fb0262c31c3a0af43ecc2f100b9295c4075a591716b6ebb9dc` at 20:05:18Z (`snapshots/V005_AT_R2C.md`). The provenance checks and the adversarial harness used this one.
  - `7f552858be77888ff1e3abc4d490e7e88ca5a16374bad84ad8ae043686b39fa2` at 20:25:33Z (`snapshots/V005_AT_R2C_2.md`). It adds A99 (20:20Z) and A100 (20:24Z).
  - Assembly used `991cc242…`. The closure lens's byte copy of it (`checks_round2/closure/V005_SNAPSHOT_991cc242.md`, read-only, sha verified) differs from `cf9bbf19` only by the inserted A98 (L890–901) and A97 (L903–921).
  - V004 `487d4449…` and V003 `5bef6552…` match. No V006 file exists.
- **Rules kept:**
  - No NGC3198 target, observed-velocity, rotmod, Vobs, MassModels or SPARC path was opened, and no NGC3198 data table.
  - `runs_ext/KMAX_A2F10_C5H_RUN_V001` was not read, listed or stat'ed. No `UVT_*` file was read.
  - Nothing was launched, and there was no network use and no recursive content search.
  - All Python ran with `-I -B` and single-thread env, under an audit-hook fence (`tools/fence_r2c.py`).
  - All mutation data is synthetic: non-physical sentinels (987.6, 9876, 1.48e9), listed stand-ins (778, 93.6), and the fake id NGC3198-Q99.
  - `taskpolicy -b` was accepted.

## Verdict: FAIL (1 BLOCKING, 6 SHOULD_FIX, 7 NOTE)

**Target-free on its bytes: yes.** Seal-ready: no.
- The BLOCKING item is currency. The object's own T7 now fails on A97 and A98, and on A97–A100 at 20:25Z. A98 rules this r2 FAIL and orders r3, which root already knows.
- The six SHOULD_FIX items are tool gaps, and claims about the tools that the tools do not support. They do not show any target content in the round-2 bytes. They do show that the mechanical check would pass target-like content in r3 in many forms.

**What holds (checked from bytes):**
- **Content.** No round-2 file names or depends on an NGC3198 observed or target velocity, a target-bearing file or a target data source.
  - The tools name deny-list terms by design. The mutation test uses non-physical sentinels and the fake id Q99, so B-11 is closed.
  - Codex2 0490 independently found "No numeric target content".
- **No rule depends on a target value.**
  - Tiers and NEAR use frozen LADDER fields.
  - Zones use the A15 cuts and are bound by query id.
  - The TSR flag comes from target-free records.
  - DT-S0G uses counts and medians.
  - The one target-shape statement is a reason, not a rule (N6).
- **Number provenance.** All 23 NEW entries, plus post 0071, verify from their stated sources (`runs/PROVENANCE_VERIFY_R2C.json`):
  - **Node radii.** 9.90 and 9.901811 are node 14 (9.901810628740723). 10.540847 is node 15 (10.540847190215317), equal to the compare's `radial_support.R_kpc`. 10.91 and 10.911722 are node 16 (10.911721936765339).
  - **Node-derived.** The midpoints are 10.2213 → 10.22 and 10.7263 → 10.73. The 7-decimal operands in `uses` are right.
  - **Query radius and indices.** 11.04 is Rad_text(Q26). Index 14 is right: Q25 lies between nodes 14 and 15. Index 17 is right: Q26 lies between nodes 16 and 17, and node 17 = 11.656.
  - **Counts.** 100 N1 rings equal the 100 GL4 node radii bitwise, and also as `radii_m/kpc_m`. The 57 round-1 findings parse from the three lens REVIEW.md headings; 32 are serious; 26 remain after the six refuter-checked ones.
  - **Diagnostic.** 1.014818 is the compare's S/θ, 1.01481832531416.
  - **A65 and V001.** 5.20 and 1.76 appear as "−5.20 to −1.76" in V005 A65 L1344. 2.2 appears in V001 as "for example 2.2 R_d".
  - **Posts.** 0032, 0056, 0058, 0618, 0550 and 0606 all exist with the pinned shas.
- **TSR derivation.**
  - The compare's ordinal 15 is node index 15.
  - Only the open interval (r14, r16) = (9.9018, 10.9117) contains a query radius: Q25 at 10.04. The kpc and metre forms agree.
  - Compare: N_FAIL_N1, gate OPEN, reason TRUNCATION_SHAPE_RESIDUAL_ONLY_A66, `failing_non_TRUNCATION_SHAPE_rings` empty.
- **Slots.**
  - Zones are 24/11/8, with edges 0.32–9.04, 10.04–28.16 and 30.08–44.08.
  - STAGE0 `outer_rows` = Q36–Q43; `invalid_primary_GL4` = Q01, Q02.
  - The six alternatives appear in the stated order with the stated statuses, and the observation-rule string matches.
- **Reproduction.**
  - The hooked check CLI reproduces the bundled TARGET_FREE_CHECK_R2.json exactly, apart from T7 and the T5 whole-file note.
  - All 26 mutation cases still behave.
  - On the actual bytes, every digit-bearing substring the stripping rules remove is a tag, section reference, short sha, path or identifier (`runs/STRIPPED_INVENTORY_R2C.json`). So the PASS stands for these bytes.

## Findings (most severe first)

### R2C-B1 — BLOCKING — T7 currency now FAILs: A97 and A98 postdate assembly, and A98 rules this r2 FAIL

**Where:** INDEX_R2.md L12; PREREG [C-11] L584; ROOT_ITEMS M-6 item 4 (L129).

**Quotes:**
- INDEX L12: "TARGET_FREE_CHECK_R2.json | T1–T6 target-free: **PASS**; T7 currency: **PASS**".
- ROOT_ITEMS L129: "Any root entry after the assembly read that touches the reading needs a revision of this text, or an explicit no-change note in the seal entry."

**Defect.**
- V005 now holds A97 (20:02Z) and A98 (20:04Z).
- A98 item 2 (V005 `cf9bbf19`, L898–901): "Miss-reading prereg r2 (Codex2 0490): FAIL, 1 blocking and 1 should-fix … Claude4 builds r3 (0619)".
- A98 touches the reading by definition. So, by the text's own M-6 item 4, round 2 cannot be sealed as it stands.

**Evidence.**
- `runs/CHECK_RERUN_R2C.json` (the hooked CLI, 20:06Z): T1–T6 PASS; T7 FAIL with `later_entries… = ["A97", "A98"]`. The T5 note gives the V005 whole-file sha `cf9bbf19…`. All 14 section pins still match.
- `runs/CHECK_RERUN_R2C_2.json` (20:25:52Z, V005 `7f552858…`): T7 later = A97, A98, A99, A100. All 14 pins match, and target-free still PASSes.
- `runs/MUTATION_RERUN_R2C.json`: all 26 cases ok, but `all_ok` is false because the baseline now fails currency.

**Fix.**
- In r3 (0619), pin A98 by section sha and cite it for the r3 changes.
- Record A97, A99 and A100 (B2 and the V007 seal) in a hand-written no-change note, after reading them.
- Re-run T7 on the V005 bytes read at r3 assembly.
- Do not regenerate the no-change list as a complement (R2C-S6).

### R2C-S1 — SHOULD_FIX — INDEX_R2's "Checked from bytes" claims more than the tools check

**Where:** INDEX_R2.md L21–26.

**Quotes:**
- L22: "no target term, data-source name, data extension, velocity value or target symbol value appears in any text file (T1–T3)".
- L23: "every numeric token is listed with a target-free source, and query and node radii are verified against their bytes (T4)".
- L24: "every pinned source hashes as stated, with the open V005 pinned per entry (T5)".
- L26: "T7 reports V005 entries added after assembly."

**Defect.** Each claim is broader than the code.
- **T1–T3** are fixed deny-lists (check L17–19, L71–73). "Any text file" means the three TEXT_FILES (L20). INDEX_R2.md and NUMBER_PROVENANCE_R2.json are never scanned.
- **T4** sees only the number tokens that survive eight stripping rules (L85–96). For each it checks only value membership and a known category name.
  - Only QUERY_RADIUS and NODE_RADIUS values are verified against bytes. NODE_DERIVED (10.22, 10.73) is not, and neither is the ring radius 10.54, which is declared MODEL_DIAGNOSTIC.
  - `listed_but_absent` never fails T4 (L288).
- **T5** silently skips any pin row its regex does not parse, and it accepts any end-marker (L155–165).
- **T7** reads only `## A<n>` headings with n ≥ 47 in V005 (L151–152). It accepts open-ended ranges (L176–180) and never reads V006.

**Evidence.** `runs/ADVERSARIAL_R2C.json`: 92 of 105 attack mutations pass. The 7 controls fail as they should, and the T7 baseline passes as it should.
- One example: the files outside TEXT_FILES (F01–F04). A forbidden term plus "987.6 km/s" placed in INDEX_R2.md, in a provenance `uses` string, as an unused provenance key, or in a new APPENDIX file: all PASS.
- More examples are under R2C-S3 to S6.

**Fix.** Either state the literal scope or fix the tools (R2C-S3 to S6) and keep the claims. The literal scope would read:
- none of the listed terms, extensions, VEL unit patterns or SYM symbol patterns occurs in PREREG, MAP or ROOT_ITEMS after NFKC and Cf stripping;
- every number token that survives the stated stripping rules has a listed value with a known category;
- values declared QUERY_RADIUS or NODE_RADIUS are verified from bytes;
- T5 checks the pin rows it parses;
- T7 lists `## A<n>:` headings ≥ 47 in V005 only.

If the scope is narrowed, list the residual false-negative classes as stated limits.

### R2C-S2 — SHOULD_FIX — The closure table marks B-8 and B-9 FIXED, yet most of their named items are not implemented; 23 of round 1's 36 adversarial cases still pass

**Where:** CLAUSE_SOURCE_MAP_R2.md, closure rows B-8 (L105), B-9 (L106) and B-7 (L104).

**Quotes:**
- L105: "| B-8 | SHOULD_FIX | FIXED. NFKC and Cf stripping; extended term, extension, unit and symbol lists; every text file scanned. |"
- L106: "| B-9 | NOTE | FIXED. The check runs as its own process with the hook installed; the mutation test installs a hook limited to its work folder. …"

**Defect and evidence.** Round-1 lens B's cases were replayed on v002 (the R1_* rows of `runs/ADVERSARIAL_R2C.json`; Q43 replaced by the fake Q99).
- **Now fixed (13):** A03, A04, A05, B01, B03, B04, B08, B10, B15, B16, C05, C07, C08.
- **Still passing (21 attack cases, plus the 2 stated-limit cases B17 and D01):**
  - A01 and A02, the listed-value forms;
  - A06, km∕s;
  - A07, m/s;
  - B02, "9\*\*8\*\*7";
  - B05, number words;
  - B06 and B07, glued identifiers;
  - B09, §;
  - B11, B12, B13b and B14, the symbol forms;
  - C01, `…/data/NGC3198_observed_curve.txt`;
  - C02, `…/NGC3198_OBSERVED_VELOCITIES.json`;
  - C03, .data, and C04, .dat_v2;
  - C06, "THINGS curve of de Blok et al." and "van Albada";
  - C09, "Mass Models" and "Mass_Models";
  - C10, a term in the provenance JSON;
  - C11, "V obs" and "v-obs".
- **B-8's own fix items not done:**
  - THINGS, de Blok and van Albada (check L17–18);
  - an allow-list for NGC3198-named paths and data-like extensions;
  - the relations "is", "of" and "≃";
  - the m/s and cm/s units;
  - "Also scan the provenance JSON and the INDEX" (L20).
- **B-9's.** The hook (L25–41) still matches only the given path string, with no realpath. It does not refuse truncate, mkdir, symlink, link, chmod, utime, exec, fork or listdir/scandir. B-9's fix asked for all of these.

**Fix.**
- Re-label B-8 and B-9 "FIXED in part".
- List the remaining classes as stated limits in INDEX.
- Add the 23 cases to the mutation test, or implement the missing items.

### R2C-S3 — SHOULD_FIX — T4's stripping rules hide numbers, and T4 is the main numeric guard

**Where:** check v002 L76–96 (`strip_for_numbers`), especially L93; CLAUSE_SOURCE_MAP B-7 (L104): "strips hex only when it contains a letter or is 64 long".

**Quotes:**
- L93: `t = re.sub(r'\[C-[^\]]+\]', ' ', t)`
- L82: `NUM = re.compile(r'(?<![\w.])\d+(?:\.\d+)?')`

**Defect.** An unlisted, non-physical value vanishes from T4 in each of the following forms. Each one gives verdict_target_free PASS.
- **Bracket text.**
  - H04: "[C-quoted value at NGC3198-Q99 is 987.6]".
  - H05: the same, spread over several lines.
  - The [C-…] rule strips any bracketed text, even across newlines, and T6's TAG regex ignores it.
- **Identifiers.** H06 "value-987.6", H07 "v987", B06 "…Q99/987.6", B07 "…Q99_987".
- **Glued Greek letters.** H08 "σ987.6": NUM's lookbehind drops digits that follow any word character.
- **Exponents.** H09 "1.48e9": the exponent is dropped, and the mantissa 1.48 is a listed token.
- **Split digits.** H10 "9<!-- -->8<!-- -->7" and B02 "9\*\*8\*\*7" leave only listed single digits.
- **HTML references.** H11 "&#x39;&#x38;&#x37; km/s" renders as "987 km/s" in Markdown. IDENT_DIGIT strips x39, x38 and x37, and VEL needs a digit right before the unit.
- **Other forms:**
  - H01 "9876e5" (HEXL);
  - H02 "9876Z" and H03 "98:76Z" (ISO);
  - B09 "§987.6" (SECTION);
  - H12 "0x3DB" (= 987; only "0" is seen);
  - H13, a URL path ending "/987.6".

On the actual round-2 bytes nothing quantity-like is stripped (`runs/STRIPPED_INVENTORY_R2C.json`). The rules are unsafe for r3 and later rounds.

**Fix.**
- Strip only the exact T6 tag pattern `\[C-[A-Za-z0-9.]+\]`.
- Strip § only when it is followed by a section number that exists in the text.
- Strip identifiers only against an allow-list of registered shapes, and count their digits otherwise. The shapes: NGC3198-Qnn, A<n>(.<n>), M-<n>, P<n>, DT-…, and the paths named in §11.
- Let NUM capture exponents.
- Fail on HTML entities, comments or markup next to digits.
- Strip hex only for prefixes of shas pinned in §11.
- Add these 17 forms to the mutation test.

### R2C-S4 — SHOULD_FIX — T1, T2 and T3 miss common unit spellings, symbol forms and term evasions, and with a listed value nothing else catches them

**Where:** check v002 L4–5, L17–19, L71–73.

**Quote:** L5: "T2 no number carrying a velocity unit (many spellings); T3 no target symbol set equal to a number".

**Defect.** T4 checks values only, so for any of the 104 listed values only T2 and T3 stand guard. Each of the following PASSes, using the listed stand-in 778 (or 93.6) and the fake id Q99.
- **T2, 15 unit forms (U01–U15):**
  - `km s$^{-1}$`, `km\,s$^{-1}$` and `km s^{-1}`;
  - `km s<sup>-1</sup>`;
  - km s–1 with U+2013, and km s‐1 with U+2010;
  - km⁄s with U+2044;
  - (km/s), m/s, kpc/Gyr, kilometers/second and kmps;
  - km s^(-1) and `\mathrm{km\,s^{-1}}`;
  - a unit in a table header, "| id | v (km/s) |".
  - Also round-1 A06, km∕s with U+2215.
- **T3, 15 forms (S01–S15):**
  - v_{q} =, v_q :=, v_q ≡ and v_q ∼ (U+223C);
  - v_q = ~… and v_q = (…;
  - "v_q is";
  - Vflat =, V_c =, v_circ =, σ_{q} = and e_v =;
  - "the observed rotation speed =";
  - v_q < and v_q ≤.
  - Also round-1 A01, A02, B11 (`` `v_q` = ``), B12 (`v\_q =`), B13b (`v_q(Q) =`) and B14 (`v_q ≃`).
- **T1, 12 forms (N01–N12):**
  - rot+U+034F+mod and rot+U+FE0F+mod. These are Mn characters and invisible, and NFKC plus Cf stripping keeps them.
  - Cyrillic А and о, and the Greek ο homoglyph;
  - `&#x72;otmod`, `rot&shy;mod`, `rot<!-- -->mod` and `rot**mod**`;
  - rot+U+115F+mod;
  - `V_{obs}`;
  - the extensions .txt, .asc, .h5, .npy and .parquet.

**Fix.**
- **T2:** fail on any velocity-unit token, with or without a number; the round-2 texts contain none. Cover km, kms, m/s, cm/s, pc/Myr, kpc/Gyr, and km with s under any exponent markup.
- **T3:** match v, V, σ, sigma or e with any subscript form, within about 20 characters of a number, under any relation: =, ≈, ≃, ~, ∼, :=, ≡, <, ≤, is, of.
- **T1:**
  - after NFKC, also strip Mn and Me;
  - fail on HTML entities and comments, and on non-ASCII letters outside an allow-list;
  - add THINGS, de Blok, van Albada, Gentile, Karukes and "mass models" (spaced or underscored);
  - extend FORBIDDEN_EXT with txt, asc, data, xls, xlsx, h5, hdf5, npy, parquet and pkl, and drop the trailing `\b`.
- Add the N, U and S cases to the mutation test.

### R2C-S5 — SHOULD_FIX — Three relied-on V005 entries are unpinned, and T5 cannot notice a missing pin

**Where:** PREREG [C-S] L19 and L21; [C-11] L584; ROOT_ITEMS M-6 item 3 (L128) and M-12 (L219); check L155–165 and L295–333.

**Quotes:**
- L21: "Until the seal, step-5 outputs are read in validity-only form, the pattern of A47 I3."
- L19: "A80 put step 5 more than a day away."
- ROOT_ITEMS L219: "**Strict parsing (A71).**"
- L128: "The cited entries are A48, A50, A52, A56, A60, A62, A63, A64, A65, A66, A70, A81, A82 and A90."

**Defect.**
- **(a) Three entries are relied on but unpinned.**
  - A47 I3 is the validity-only blinding that the seal-timing rule rests on. A71 is the strictness that M-12 binds. A80 dates step 5.
  - None of the three is pinned or in M-6 item 3. All three are in the generated "Read with no change" list.
  - This repeats round-1 L-C12 (A50 used but unpinned), now for entries that the B-1 and A-16 fixes added. An in-place edit to A47 I3 passes T5.
- **(b) T5 never checks its own completeness.** It never compares its parsed pins with the body citations or with M-6 item 3.
  - E03: a pin row with one trailing space is skipped silently. The result is target-free PASS while V005 A66's ruling is changed to "is not flagged".
  - E02: deleting the A66 row and listing A66 as no-change passes both verdicts.

**Evidence.**
- `runs/PROVENANCE_VERIFY_R2C.json`: `v005_cited_not_pinned` = A47, A71, A80.
- `runs/ADVERSARIAL_R2C.json`, E02 and E03: T5 checked 13 entries, A66 absent, and reported no problem.

**Fix.**
- Pin A47, A71 and A80 and add them to M-6 item 3, or drop those citations.
- In T5, fail when any `| A<n> |` row in §11 fails to parse.
- Also fail when the pinned set differs from either the A≥47 references in the three texts or M-6 item 3's list.
- Add E02 and E03 to the mutation test.

### R2C-S6 — SHOULD_FIX — The "Read with no change" list is computed, not read; T7 accepts open ranges, misses other heading forms and never reads V006

**Where:** PREREG [C-11] L565 and L584; ROOT_ITEMS M-6 item 4 (L129); CLAUSE_SOURCE_MAP A-12 (L91); generator L62–75 and L84; check L151–152, L168–181 and L345–353.

**Quotes:**
- L584: "**Read with no change to this text:** A47, A49, A51, A53–A55, A57–A59, A61, A67–A69, A71–A80, A83–A89, A91–A96."
- MAP L91: "The uncited list is computed at assembly in §11".
- ROOT_ITEMS L129: "This covers entries in V005 until its freeze, and in V006 after it. Check T7 lists them mechanically."

**Defect.**
- **(a) Nothing records a reading.** The list the text calls "read with no change" is the generator's complement of CITED, taken over every heading present at assembly.
  - Re-running that computation on today's V005 gives "…, A91–A98". That labels A98, the ruling that r2 FAILs, as read with no change.
  - With that list, T7 PASSes (T03).
- **(b) Ranges have no upper bound.** "A91–A199" makes T7 PASS today and covers every future entry (T01).
- **(c) Only one heading shape is seen.** T7 matches only `^## A(\d{1,3})\b`.
  - "## A99a:", "### A99:", "## A 99:", "##A99:", "## a99:" and "## Entry A99:" all PASS (T02a–f).
  - "## A99:" FAILs as it should (K06).
- **(d) V006 is never read.** The check has no V006 path, so "Check T7 lists them mechanically" is false for V006.

**Fix.**
- Keep a hand-written no-change record (entry, read time, one-line reason). The generator verifies it but does not write it.
  - Root has just confirmed this pattern for the final prereg. A99 item 3 (V005 `7f552858`): "Prereg r5 lists every entry from A82 to the freeze as either 'revised here' or 'no change, because …', and the seal record quotes the table."
- Reject any range that ends beyond the highest heading at assembly, and record that number in §11.
- Make T7 list every heading-like `A<n>` line and fail on any form it cannot parse.
- Include V006 once it exists.
- Add T01, T02 and T03 to the mutation test.

### R2C-N1 — NOTE — T5 accepts any end-marker

**Where:** PREREG [C-11] L564: "…or up to the end-marker shown."

**Defect.**
- Re-stating A66's pin to end before `**Fact` keeps 71 bytes (the heading). The A66 ruling can then change unseen: E01, T5 PASS.
- The mutation test covers only a nonexistent marker.
- A65's `**Lanes.**` marker is legitimate. It cuts only V005's trailing log (L1360 to EOF), and that log's content is reached through 0512, 0518 and 0524, which are pinned separately.

**Fix:** an allow-list of markers in the check (A65 → `**Lanes.**` only), or report and bound the excluded tail.

### R2C-N2 — NOTE — The mutation test is narrow and not relative to its baseline

**Where:** test L77–102 and L134 (`good = expect <= failed`).

**Defect.**
- None of the 71 new false-negative forms, and none of the 23 round-1 leftovers, is among its 26 cases.
- `later_entry_uncovered` is vacuous whenever the baseline already fails T7, as it does now.
- Its hook (L34) omits os.rename and socket.getaddrinfo, which the check's hook refuses.

**Fix:**
- A case passes only if its failed set exceeds the baseline's and cites the injected token.
- Add the new cases.

### R2C-N3 — NOTE — The CLI exit code ignores currency

**Where:** check L382: `return 0 if res['verdict'] == 'PASS' else 2`, where `verdict` = verdict_target_free.

**Defect.** The check exited 0 at 20:06Z with currency FAIL. The generator does require both verdicts (L155).

**Fix:**
- A distinct non-zero exit code for currency FAIL, or a `--require-currency` flag.
- Any seal script must read `verdict_currency`.

### R2C-N4 — NOTE — Provenance labels

All 23 new entries hold (see "What holds"). Small label defects:
- "2.2" is categorized RULE_CONSTANT, but it is V001's example option ("for example 2.2 R_d").
- The `uses` strings for post numbers say "FROM_CODEX dispatch or a lane post". FROM_CODEX/0618 now exists (the A97 B2 dispatch), so name FROM_CODEX3/0618 explicitly.
- 10.22, 10.73 and 10.54 are verified here by hand, not by T4.

### R2C-N5 — NOTE — The Status list of NGC3198 data read is incomplete

**Where:** PREREG [C-S] L8–10: "The only NGC3198 data read are: query ids and radii from the target-free query block of slots V003; the target-free N-test and node records named in §11."

**Defect.**
- T5 also reads and hashes `NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json`.
- The text uses the slots V003 alternatives list and observation rule.

All of these are target-free. Only the list is incomplete.

**Fix:** name them.

### R2C-N6 — NOTE — The M-6 reasoning asserts the observed curve's shape

**Where:** ROOT_ITEMS L134: "NGC3198's flat outer curve is public (B-1)".

**Defect.** This states a property of the observed target curve. No rule uses it, and it is literature knowledge.

**Fix:** add round-1 B-12's sentence: literature knowledge, not a target read; no classification rule uses it.

### R2C-N7 — NOTE — Hygiene

- ELIDED (L77) is dead code: NFKC turns U+2026 into "...".
- Census contexts are cut from the stripped text, for example "( : about 0.03; )", so reviewers cannot see the identifiers.
- INDEX and HASHES do not record the generator's draft folder, so the assembly cannot be replayed.

## Tested (artifacts in this folder)

| artifact | what it is |
|---|---|
| `runs/CHECK_RERUN_R2C.json` (`4615ba1b…`) | the object's check, hooked CLI, on round2: target-free PASS, currency FAIL (A97, A98), exit 0 |
| `runs/MUTATION_RERUN_R2C.json` (`20e9e80b…`) | the object's mutation test: 26/26 cases ok, all_ok false (baseline currency) |
| `tools/verify_provenance_r2c.py` → `runs/PROVENANCE_VERIFY_R2C.json` (`cdd0fe61…`) | the new provenance entries, the TSR derivation, zones, slots and the A-reference map, from bytes |
| `runs/CHECK_RERUN_R2C_2.json` (`bf622263…`) | the same, against V005 `7f552858`: currency FAIL (A97–A100), all 14 pins match |
| `tools/adversarial_r2c.py` → `runs/ADVERSARIAL_R2C.json` (`215e895e…`) | 115 cases: 7 controls and 1 baseline (all behave), 2 stated-limit cases, and 105 attacks, 92 of which pass |
| `tools/stripped_inventory_r2c.py` → `runs/STRIPPED_INVENTORY_R2C.json` (`6722578d…`) | what the stripping rules remove from the real bytes |
| `tools/fence_r2c.py` | the audit-hook fence used by every script here |
| `snapshots/V005_AT_R2C.md` (`cf9bbf19…`) and `snapshots/V005_AT_R2C_2.md` (`7f552858…`) | the V005 bytes read |

## Outside this lens (no finding here)

- **Codex2 0490, BLOCKING.** Undefined-sign MISS rows break OUTER_FAILURE equivalence and pattern coverage. This is semantics, now ruled in A98.
- **Ring classes.** The compare's S/θ exceeds 1 on rings 15–99, while only ring 15 is listed failing. That matches the record's empty `failing_non_TRUNCATION_SHAPE_rings`, presumably via C1′ on NOT_GRID rings. The fidelity lens may wish to confirm the ring classes.
