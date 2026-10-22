# VERIFY: adversarial check of round-2 targetfree finding R2C-B1 (miss-reading prereg r2, round 2)

- **Written:** 2026-10-18T20:42Z, updated at 20:48Z after V005 changed twice more (`date -u`). Work started at 20:28:45Z. V005 was still `70a48f51…` at 20:48:01Z.
- **Verifier:** a Claude4 helper, under dispatches 0585 (`9003633293ff1db7d5153cabc338fd058cc199d834976b05543b7603b9433abd`) and 0606 (`dbb80c77cb085626303a9ce4e8d48e761dfd8525eece32022154e7e69881e28e`), with the 0592 refute-by-default checks.
  - I wrote only in this folder and did not edit the object.
- **Object:** `claude_artifacts/miss_reading_prereg_c4/r2/round2/`. All 10 entries of HASHES_R2.txt match `shasum -a 256` (20:28Z), for example:
  - PREREG `97d5ce33ffa90e64ac208d36863c776460ad596fded2f376f1090a232e5ce407`;
  - ROOT_ITEMS `4907cf019c7bec62da646dc862f6c36c2b3aa03b11b761f36475c1056e968500`;
  - INDEX `0d24b8fe778fb704398a7039f579977d92e51dfd152994d6e68048cffa03b926`;
  - TARGET_FREE_CHECK `624f278e02419ca28ea4a3a12fb869822cd4fddd8eaa721492d38996217c91f9`.
- **Finding checked:** R2C-B1 (BLOCKING) in `checks_round2/targetfree/REVIEW.md` (`8443cb1e76d1dc24b0d29ea3be1eb0d38b32aba1eb70dcaeec9fc57644119ec6`): "T7 currency now FAILs: A97 and A98 postdate assembly, and A98 rules this r2 FAIL".
- **Root decisions read:**
  - V005 (open) at 20:29:39Z: `7f552858be77888ff1e3abc4d490e7e88ca5a16374bad84ad8ae043686b39fa2`. A copy is in `snapshots/V005_AT_VERIFY.md`.
    - It was unchanged at 20:39:54Z, and no V006 file exists.
    - V005 line numbers below refer to `7f552858` unless a sha is named.
  - V005 again at 20:44:14Z: `5a996e97d633cc11a4cb255fe8ba1cdf746d93367621c004aca29382affb6a26` (copy in `snapshots/V005_AT_VERIFY_2.md`).
    - The only change is a 10-line insert at L890: "## A101: B2 record of record; registry V008 (2026-10-18 20:48Z)". In this first form it is on the V007 path only.
    - Still no V006.
  - V005 a third time at 20:45:25Z: `70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e` (copy in `snapshots/V005_AT_VERIFY_3.md`).
    - **A101 was amended in place** by a 7-line insert at L898–904. One part is the V007 case block. The other is "**Step-5 open item closed (A90).** Codex1 0066 ran the independent tail-domain star-transform convergence for the NGC LO I1-T precondition: **TESTED PASS.**" (L900).
    - That second part does touch this text (§3c).
  - Also used: the closure lens's byte copies `991cc242…` (the assembly read), `cf9bbf19…` and `ff7980e8…`. Each was re-hashed from bytes and matches its name.
  - V004 `487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b` and V003 `5bef6552b92b0939405ae6d6cefd12c1df95f2d57097589439fa37aa78b9b468` both match the PREREG pins.
- **Other sources read** (sha256 from bytes):
  - FROM_CODEX2/0490 `3a922168f800de5ae9fff2ba1cb55af2f55d7ae4290a75b14a0ca2daa36a2649`, and its `review_miss_reading_r2_cx2/round2/REVIEW_CX2V001.md` `7e3b6211ded52e4212c8534b7dad04bc9334ea5c458cdc8de6c8545c19e5af71`;
  - FROM_CODEX dispatches 0619 `238858d12823a153b14dd980d2e2c0a4a71da5c320be054c1fe14832d667ee99`, 0621 `7ab78e6a0aa4c3d11d6c4dd9887ea2fc8b65e40a84bc75de387a319534b99504` and 0622 `e6ae0c32632bfd77c8898d4bf598336941f237dfb22324bfbae0291d4bdd0509`;
  - the round-2 closure lens `REVIEW.md` `566cf50f5613161c6d1316911a44f2555004144c3e17c62a4c0dce91197f0d48` and newdefects lens `REVIEW.md` `5b7c8b488f85bff551b47df5d83ed4904d86936cd51188c32dd5840bf4e4b3f3`;
  - the round-1 lens reports: targetfree `2eab55194d7ec2d7783ebed259d8afb2794de45bd9d383cefc3dc5fd3c7537b6`, consistency `a586fb877a54a34c82ed5767877fa7ac94825741dce44ceb96c91facbbf9450e` and fidelity `41cbea3bb48839fa384b9878a247b6e53adbaeba216dd7d76b5b469e59bc3ed0`.
- **Rules kept:**
  - No NGC3198 target, observed-velocity, rotmod, Vobs, MassModels or SPARC path was opened, and no NGC3198 data table.
  - `runs_ext/KMAX_A2F10_C5H_RUN_V001` was not read, listed or stat'ed. No `UVT_*` file was read.
  - Nothing was launched. There was no network use and no recursive content search; `grep` ran only on files named here.
  - Python ran as `python3 -I -B` with single-thread env, under the audit-hook fence `tools/fence_vtf1.py`.
  - The object's own check was not re-run. The T7 and pin results below come from independent code in `tools/`. The lens's runs were read as files.

## Verdict

| question | answer |
|---|---|
| Refuted? | **No, on the facts.** Every factual claim is confirmed from bytes (§2). Two things do not survive: the claim that the quoted text is defective (§1), and the BLOCKING severity (§3). |
| Is the quoted text there and defective? | **There, verbatim. Not defective.** INDEX L12 correctly describes the bundled check, which was computed against the V005 sha that INDEX L18 names. ROOT_ITEMS L129 is the rule being applied, and it works as written. |
| Does the evidence say what is claimed? | **Yes, every item** (§2). One step of the argument is loose: M-6 item 4 alone would allow a no-change note. What bars sealing r2 is the content of A98.2. |
| Severity | **NOTE, not BLOCKING** (§3). Round 2 is wrong to seal, but only because of A98.2, root's adoption of Codex2 0490's blocker. That blocker is already BLOCKING in this round as closure F2 and newdefects R2B-01. A T7 FAIL after assembly is the check's designed signal. The newdefects lens rates the same fact NOTE (R2B-13). |
| Would the fix work? | **Partly** (§4). The dispositions are right, and an A98 section pin is stable. But "re-run T7 at r3 assembly" passes by construction while the no-change list is generated: in a replay, A98 lands in the list and T7 passes. Nothing re-checks at the seal, so r3 would recreate the same stale PASS. Its closed list (A97, A99, A100) is already outdated by A101, which touches PREREG L79. |

## 1. The quoted text is present, but not defective

- **INDEX_R2.md L12**, verbatim: "| TARGET_FREE_CHECK_R2.json | T1–T6 target-free: **PASS**; T7 currency: **PASS**; with the occurrence census | `624f278e…` |".
  - The row describes the bundled `TARGET_FREE_CHECK_R2.json`. That file's sha matches, it was written at 19:55:19Z, and its T7 reads `pass: true` with `later_entries…: []`.
  - Generator L122 fills the row from that run's `verdict_currency`. Generator L127 writes L18: "V005 at assembly: `991cc242…` (headings up to A96)."
  - INDEX L4 says the pins and the uncited list "were read from the addendum bytes at assembly". L26 says: "T7 reports V005 entries added after assembly. That is currency, not target-freeness."
  - My independent T7 on the `991cc242` bytes gives `later = []` (`runs/T7_RECHECK_VTF1.json`). So the row was true when written, and the INDEX ties it to that sha.
- **ROOT_ITEMS_R2.md L129** (M-6 item 4), verbatim: "Any root entry after the assembly read that touches the reading needs a revision of this text, or an explicit no-change note in the seal entry."
  - This is the rule the finding applies, not a defect. T7 now lists A97–A101, exactly as L129 says it will ("Check T7 lists them mechanically").
- **PREREG [C-11] L584** is cited but not quoted. It holds the no-change list "A47, A49, A51, A53–A55, A57–A59, A61, A67–A69, A71–A80, A83–A89, A91–A96".
  - It is accurate for `991cc242`. My replay of the generator's complement (L62–75) on those bytes reproduces it exactly (`runs/COMPLEMENT_REPLAY_VTF1.json`).
  - That the list is computed rather than read is a real defect. But it is R2C-S6(a) and closure F3, not B1.
- **So the "defect" is a change in the world after assembly, not an error in the bytes.**
  - The text was built to stay fixed while V005 grows. PREREG L564–565: "root keeps adding entries… Check T7 lists every heading in the file that is neither cited here nor in the read-with-no-change list."
  - Check L353 gives the meaning of the result: "currency only: a FAIL here means root added an entry after assembly (M-6 item 4)".

## 2. The evidence, claim by claim

| claim in R2C-B1 | what the bytes say | status |
|---|---|---|
| V005 holds A97 (20:02Z) and A98 (20:04Z) | `7f552858` L961 "## A97: … (2026-10-18 20:02Z, …)" and L948 "## A98: … (2026-10-18 20:04Z)". In `cf9bbf19` they are at L903 and L890. | CONFIRMED |
| at 20:25Z also A99 and A100 | L931 "## A99: … (2026-10-18 20:20Z)" and L890 "## A100: … (2026-10-18 20:24Z…)". The lens snapshot `7f552858` was taken at 20:25:33Z. My reads at 20:29:39Z and 20:39:54Z found the same sha and no V006. | CONFIRMED |
| A98 item 2 quote | `cf9bbf19` L898 and `7f552858` L956: "2. **Miss-reading prereg r2 (Codex2 0490): FAIL, 1 blocking and 1 should-fix.**". L900/L958: "**Claude4 builds r3** (0619)". The ellipsis is fair. | CONFIRMED |
| A98 touches this reading (round 2, not round 1) | Codex2 0490 (20:01:30Z) L6: "Exact round2 candidate remains unchanged and unsealed". Its REVIEW_CX2V001.md pins PREREG `97d5ce33…`. 0619 L5–7 orders r3 from it. | CONFIRMED |
| `runs/CHECK_RERUN_R2C.json` (20:06Z): T1–T6 PASS, T7 later [A97, A98], T5 note `cf9bbf19` | mtime 20:06:05Z, sha `4615ba1b…`, which equals the stdout capture. T7 `pass: false`, later ["A97", "A98"]. T5 note: "V005 whole-file sha is now cf9bbf19…". 14 entries match. | CONFIRMED |
| `runs/CHECK_RERUN_R2C_2.json` (20:25:52Z): later A97–A100; 14/14 pins | mtime 20:25:52Z. later ["A97", "A98", "A99", "A100"]. 14 entries, all `match: true`. verdict_target_free PASS. | CONFIRMED |
| `991cc242` differs from `cf9bbf19` only by inserted A98 (L890–901) and A97 (L903–921) | `diff` gives a single 33-line insert after L889, with no deleted or changed line. A98 is at L890–901 and A97 at L903–921. The later snapshots are also pure inserts at L890: A99 (17 lines), then A100 (41 lines). | CONFIRMED |
| mutation rerun all_ok False because the baseline fails currency | Test L125: `ok = base['verdict_target_free'] == 'PASS' and base['verdict_currency'] == 'PASS'`. The rerun has baseline_currency FAIL and all 26 cases ok. | CONFIRMED |
| (my own check) pins and T7, from independent code | `tools/recheck_t7_vtf1.py` uses byte slicing and does not import the object. Results: 14/14 pins match on all four snapshots. T7 later is [] on `991cc242`, [A97, A98] on `cf9bbf19`, [A97–A99] on `ff7980e8` and [A97–A100] on `7f552858`. No heading-like line falls outside the strict pattern in any snapshot. On `5a996e97` (20:44:14Z) and `70a48f51` (20:45:25Z) the pins still match 14/14, A90 included, and later is [A97–A101] (`runs/T7_RECHECK_VTF1_2.json`, `_3.json`). | CONFIRMED |

**One loose step.** The finding says that "by the text's own M-6 item 4 round 2 cannot be sealed". But L129 offers "a revision of this text, **or** an explicit no-change note in the seal entry". So item 4 alone does not bar the seal.
- What bars it is A98.2's content. No honest no-change note can be written for a ruling that orders a revision.
- M-6 is also still a root item, listed in PREREG [C-10] L514, not a ruling.
- The conclusion stands, by A98.

**Trivial.** The lens header says "Written 2026-10-18T20:23Z", but it cites a 20:25:52Z run. Its file was last written at 20:26:44Z.

## 3. Severity: NOTE, not BLOCKING

- **(a) It counts one blocker again.** A98.2 adopts Codex2's CX2-MR2-REACH-B1. In this same round, closure F2 (closure REVIEW L204, BLOCKING) and newdefects R2B-01 (newdefects REVIEW L82, BLOCKING) state the same defect: undefined-sign MISS rows break OUTER_FAILURE, coverage and the late-gate claim.
  - The targetfree lens itself lists 0490 under "Outside this lens (no finding here)".
  - B1 takes all its force from A98.2. Root ruled and dispatched r3 (0619) at 20:04Z, before the lens wrote its report.
  - Listing B1 as a target-free BLOCKING counts that one blocker twice in this round, and four times across reviewers.
- **(b) The FAIL is the designed behaviour.** Check L10/L353, INDEX L26, PREREG L565 and ROOT_ITEMS L129 all define a T7 FAIL after assembly as "root added an entry", to be dispositioned. The tool did its job: it is the intended alarm, not a defect.
- **(c) A T7 FAIL does not by itself make a text wrong to seal.** Every later entry trips T7, but they differ in what they need.
  - **A97, A99, A100 and A98.1 do not touch the text.**
    - The three texts mention V007 only at PREREG L561 ("it closes at the V007 freeze, A82"). They mention no B2, BUILD_V007, case block or "prereg r5": `grep -c` gives 0 in ROOT_ITEMS and MAP, and PREREG's one hit is L561.
    - "Prereg r5" in A99.3 is the V007 final prereg: 0621 L6 binds BUILD_V007 and the case block to it.
    - A99.6 ("Root writes nothing to V005 after the freeze (A82)") restates A82, which M-6 item 2 (L127) and PREREG L561 already follow.
    - A98.1 (PAR-TB) is about NGC v011 traceback text. It grants "**No** exception … for numerical values, rows, validity" (L955).
  - **A101, in its amended form (20:45Z), does touch the text, without making anything unsafe.**
    - A101 L900 closes "the step-5 open item (A90)": the LO I1-T precondition is TESTED PASS (Codex1 0066).
    - PREREG [C-I6] L79 records that precondition as "NOT_RUN", "ruled by root before any NGC route-A/B launch (A90). That ruling is recorded in D-4 with its sha". D-4 L451 lists "the root ruling on the A90 LO I1-T precondition".
    - So A101 needs a reasoned disposition. It can be "revised here", updating L79, or "no change, because D-4 already records the ruling", since "NOT_RUN" was the status at writing.
    - A90's pin still matches, so T5 cannot see this. Only T7 plus a human reading can (round-1 B-6; closure F4).
    - The text already provides for the ruling, so nothing here is unsafe. It is the routine M-6 item 4 work.
  - **Only A98.2 makes r2 unsealable**, and it does so through its content.
- **(d) Calibration with earlier rounds and with the other round-2 lenses.**
  - Round 1 rated this exact class SHOULD_FIX: V005 had grown after assembly with A90, which touched the reading. Those findings were B-6 (round-1 targetfree L168), L-C11 (consistency L272) and A-11 (fidelity L298), with closure rows at MAP L90, L103 and L120.
  - In round 1 the tooling could *not* see the new entries (T5 passed with a note). Round 2's T7 sees them.
  - In round 2, the newdefects lens rates this same observation NOTE (R2B-13, newdefects REVIEW L363), with the same fix: "r3 cites A98 and lists A97, A99 and A100 as no-change, per M-6 item 4."
- **(e) The work left for r3 is already SHOULD_FIX elsewhere.** It consists of citing and pinning A98, and writing the dispositions by hand. R2C-S6(a) and closure F3 both name this very case ("…, A91–A98", labelling A98 as read with no change).
- **Result: NOTE, cross-referenced to A98.2.** The round-2 aggregate should still read FAIL. Its blocker of record is A98.2 (= Codex2 REACH-B1 = closure F2 = newdefects R2B-01), counted once.

## 4. The fix: works in part

**What works:**
- **An A98 section pin is stable under the way root inserts entries.** A98's section sha is the same on `cf9bbf19`, `ff7980e8`, `7f552858`, `5a996e97` and `70a48f51`: `181248d91db1437786cc8654c4dc82bb3983ea36a069f702f6dfd2acadfd8aa9` (`runs/NEW_ENTRY_SECTIONS_VTF1.json`, `_2.json`, `_3.json`). Root inserts new entries at L890, above A98. A77's and A96's sections are also unchanged across all six snapshots.
- **The no-change notes for A97, A99 and A100 are right in substance** (§3c).

**Gaps:**
1. **"Re-run T7 on the V005 bytes read at r3 assembly" proves nothing while the list is generated.**
   - Generator v003 hard-codes CITED (L16–31). It writes every other heading ≥ A47 into the no-change list (L62–75), so T7 at assembly passes by construction.
   - Replay (`runs/COMPLEMENT_REPLAY_VTF1.json`): on `991cc242` it reproduces L584 exactly. On `7f552858` it gives "…, A83–A89, A91–A100", with A98 inside, and T7 PASS. On `5a996e97` and `70a48f51` it gives "…, A91–A101" and T7 PASS (`runs/COMPLEMENT_REPLAY_VTF1_2.json`, `_3.json`). So it also labels A101 "read with no change", although A101 closes the item that L79 calls NOT_RUN.
   - The fix's last item points at R2C-S6, but it has to state the generator change itself: A98 goes into CITED, and the list is read from a hand-written record, which the generator only verifies.
2. **Nothing checks at the seal.**
   - V005 gained four entries in 22 minutes (heading times 20:02Z to 20:24Z), and a fifth, A101, while this verification ran (between 20:39:54Z and 20:44:14Z). A PASS at r3 assembly will be stale by r3's review and seal, exactly as r2's was.
   - The CLI exits 0 on a currency FAIL (check L382; R2C-N3). So a seal script that trusts the exit code would not notice.
3. **The INDEX wording would repeat the problem.**
   - Generator L122 writes "T7 currency: **PASS**" with no basis on the same line.
   - The mutation test's all_ok includes baseline currency (test L125), so it goes stale the same way.
4. **A new, minor problem: A98's section also holds A98.1 (PAR-TB), which expects follow-up.** L955 reads: "Any frame class specific to r008 is enumerated and pinned before closure".
   - Root has amended an entry in place before: "**A77.2 made precise (Codex2 0451, ~16:48Z).**" (L882) sits inside A77, whose heading says ~16:44Z.
   - It happened again during this verification: A101 gained L898–904 between 20:44:14Z and 20:45:25Z. A disposition of A101 made from the 20:44Z bytes would have missed its A90 item.
   - An in-place PAR-TB amendment would make r3's T5 fail, although the reading is untouched. That is fail-closed and acceptable.
   - r3 should still say how such a failure is cleared: re-read A98.2, re-pin and note it. A silent re-pin is not enough.
5. **The fix names a closed list (A97, A99, A100), and that list is already out of date.** A101 arrived after the lens wrote, and its amended A90 item needs its own reasoned disposition (§3c). The fix should say "every entry after the assembly read", each one read from hashed bytes.

**Better fix:**
1. Re-label R2C-B1 NOTE and merge it with newdefects R2B-13. The round-2 aggregate names A98.2 (= Codex2 REACH-B1 = closure F2 = newdefects R2B-01) as its one blocker of record.
2. **In the r3 generator (v004):**
   - Add A98 to CITED, with the use "A98.2: r2 FAIL; undefined-sign coverage, OUTER_FAILURE equivalence and late-gate behaviour (0619)".
   - Compute its section sha from bytes at assembly. Do not copy one from a review.
   - Cite A98 at each clause r3 changes.
3. **Replace the computed list with a hand-written table**: entry, time read, and "revised here" or "no change, because …".
   - It covers at least: A97 (the V007 B2 gate); A98.1 (PAR-TB, NGC v011 traceback text only); A99 ("prereg r5" is the final prereg, and item 6 restates A82, which M-6 item 2 already follows); A100 (B2 disposed); A101; and every later entry.
     - For A101 the B2, case-block and registry parts need no change. Its A90 LO I1-T closure needs the L79/D-4 disposition described in §3c.
     - Each entry is read and dispositioned from bytes hashed at a stated time, and the table records that sha.
   - The generator verifies coverage and refuses any range that runs past the highest heading (R2C-S6).
4. **In the INDEX,** write "T7 currency: PASS against V005 `<sha>` read at `<date -u>`; re-checked at the seal". Report the mutation all_ok for the target-free cases separately from baseline currency.
5. **At the seal step:**
   - Re-run T7 on the V005 bytes at the seal, and on V006 if it exists.
   - Read `verdict_currency` from the JSON, not the exit code.
   - Put a disposition for every entry after r3's assembly read into the seal entry (M-6 item 4).

## 5. Artifacts in this folder

| artifact | what it is |
|---|---|
| `snapshots/V005_AT_VERIFY.md` | V005 bytes read at 20:29:39Z (`7f552858…`) |
| `snapshots/V005_AT_VERIFY_2.md` | V005 bytes read at 20:44:14Z (`5a996e97…`, adds A101) |
| `runs/T7_RECHECK_VTF1_2.json`, `runs/NEW_ENTRY_SECTIONS_VTF1_2.json`, `runs/COMPLEMENT_REPLAY_VTF1_2.json` | the same three rechecks, on `5a996e97` |
| `snapshots/V005_AT_VERIFY_3.md` | V005 bytes read at 20:45:25Z (`70a48f51…`; A101 amended in place) |
| `runs/T7_RECHECK_VTF1_3.json`, `runs/NEW_ENTRY_SECTIONS_VTF1_3.json`, `runs/COMPLEMENT_REPLAY_VTF1_3.json` | the same three rechecks, on `70a48f51` |
| `tools/fence_vtf1.py` | audit-hook fence. It refuses target-like and protected paths, any write outside this folder, and process, network, delete and rename events. |
| `tools/recheck_t7_vtf1.py` → `runs/T7_RECHECK_VTF1.json` | independent T7 and 14-pin recheck on `991cc242`, `cf9bbf19`, `ff7980e8` and `7f552858` |
| `tools/a98_section_vtf1.py` → `runs/NEW_ENTRY_SECTIONS_VTF1.json` | section shas of A77 and A96–A100 in each snapshot (pin stability) |
| `tools/complement_replay_vtf1.py` → `runs/COMPLEMENT_REPLAY_VTF1.json` | generator v003's no-change complement, replayed on three snapshots, with T7 on the result |
| `PARTIAL.md`, `REVIEW.md`, `HASHES.txt` | progress log, short summary, and sha256 of every file here |
