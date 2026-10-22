# FIXLOG_V002: the fix stage of ROOT_ITEMS_STEP45 (dispatch 0637)

**Who and when.** A helper of lane Claude4 (coordinator Claude2), fix stage of dispatch 0637 (`e6163c64eaf2193e7730a1819ae0e1cea87420c8a4fa9ddb2678583e460ade01`, re-hashed from bytes). Written 2026-10-19T02:56:51Z (`date -u`).

**Object.** ROOT_ITEMS_STEP45_V001.md `33d09696d105062f8a8dc0cd15256b412d2db6eeadd7d8e693a0489bbee07e46` and .json `8a20c3342e2e3abe7a3560b07e4cfda5957aebbe044885e585373a3a5dc46fb2` (unchanged), and the refuter's report REFUTE_ROOT_ITEMS_STEP45.md `0a75e6d86ecb57fd1a04dfafbd47ed17273ac4d015231032729bcb1499d9468d` (8 SHOULD_FIX, 13 NOTE).

**Output (exclusive create, this folder).** ROOT_ITEMS_STEP45_V002.md `417de6fef408082695e4e3f68530351a0b71a7c1415d784a29199a8a9ec42ee8` and .json `f6eb430eaf13b1fa8543ff8b14d74e61c3f57da649615a8dd0ddd0315919c910`, built at 2026-10-19T02:55:14Z by BUILDER_ROOT_ITEMS_STEP45_C4V002.py `c74d41f9fa1db5587496f96161d10e74c1e38bbb1f9ac5b999c23d32bdbe4bf3` (the V001 builder `5ee4978811cb4842603e8f303bbdb9750c6db6ef8a816ce91199bf7c5da35c65`, copied and patched). CHECK_ROOT_ITEMS_STEP45_V002.py `8980c60bde8d1db605f19e8f34345afcea994de8d9ff0c0f0ca38c72604f3611` is the self-check that ran on the staged pair before publication. V001 and every other build-stage file are unchanged.

**Labels.** TESTED = recomputed from bytes in this stage. FORMAL = read from a named record. UNTESTED = projections and models. RECOMMENDATION = a proposal for root. Nothing here rules, launches or adopts anything.

## Summary

- **All 8 SHOULD_FIX findings are CONFIRMED from the source bytes, and each is fixed in V002.** None was refuted; one fix is wider than the finding asked (SF-4 also adds the contract's third missing obligation), and SF-1's evidence is stronger than the refuter cited (the launcher's own replay check).
- **All 13 notes were checked.** N-1 is a state update and is applied with the newer state; N-2 to N-13 are confirmed and applied as wording changes.
- **State that landed after the refuter (02:04Z) is folded in:** Claude4 0124 (the first SEAL CANDIDATE) and 0125, Codex1 0119 and 0120 (the r3 delta), V006 `b22bd18a` (A112), the ROOT_ITEMS_FINAL_C4V005 candidate and dispatch 0648.
- **Counts (TESTED, CHECK_ROOT_ITEMS_STEP45_V002.py, 175 of 175 checks pass):** 55 items (V001's 53 plus S4-R-B4a and S4-R-B7; every RI45 id unchanged); 68 summary rows (25 `BLOCKS_START`, 43 `BEFORE_FIRST_RESULT`; V001 had 62: 27 and 35); 12 step-4 start items.

## The findings

### SF-1: CONFIRMED, fixed

**Finding.** R-B4's prelaunch-check part blocks step 4's start but was filed as campaign-only.

**Reason.**
- FORMAL, ROOT_ITEMS_FINAL_C4V004 (`97a762e1`): R-B4's Blocks line (L183) reads 'The campaign launch; the PRELAUNCH records the 0616 plans pin'; its What (L182) says 'Root also needs a one-call prelaunch check for standalone specs' and that PRELAUNCH 'must include the actual certificate-policy and per-spec checks'; its owner (L58, L184) is 'builder any lane; distinct review'. R-B6's disposition (L202) binds 'the PRELAUNCH records (R-B4)'.
- FORMAL, LAUNCH_ORDER_C4V002 (`52027098`): L110 puts 'PRELAUNCH per spec on those bytes (R-B4)' on the path to HEADLINE11; L133 (H1) has root run PRELAUNCH with the certificate-policy and per-spec checks.
- Stronger than cited (FORMAL, read in this stage): guard007 (`42bf0ce9`) validate refuses any call whose pinned PRELAUNCH is not equal to a fresh native_preflight replay (L266, PRELAUNCH_REPLAY_MISMATCH); IMPLEMENTATION_INTERFACE_CX1V003 (`dc73cd94`) has root obtain the record 'by a controlled in-process, read-only call'; RUNBOOK_CX1V003 (`2eda3ebf`) step 4 says to generate it through guarded native_preflight. TESTED (grep of the named files): binder v006 (`3db8c72a`) and launcher v008 (`bf2d535f`) contain no PRELAUNCH writer, and guard007 has no command-line entry. So HEADLINE11 cannot be admitted without a tool that nobody is assigned to build.

**Change.** R-B4 is split. New in-full item **S4-R-B4a** (`BLOCKS_START`, step 4; 'During step 2, before T0'): the one-call PRELAUNCH tool, calling guard007's native_preflight unchanged and writing each record by exclusive create, with MUST_FAIL controls; builder unassigned, Codex1 recommended (Claude4 if Codex1 lacks capacity), reviewer Claude3. The by-reference R-B4 row stays `BEFORE_FIRST_RESULT` as **S4-R-B4b** (the campaign entry). Flags item 1 counts 12 start items, two without a builder; S4-R-B6 and S4-R-A1 point to S4-R-B4a.

### SF-2: CONFIRMED, fixed

**Finding.** Five AFTER_HEADLINE items gate campaign wave 1 but were marked LATER.

**Reason.**
- FORMAL, ROOT_ITEMS_FINAL_C4V004: Blocks lines of R-A4 (L133, 'adoption_regeneration gate, hence the campaign'), R-A5 (L141, 'adoption_regeneration'), R-C2 (L217, 'u_i_carrier gate, hence the campaign'), R-D3 (L291, 'driver_capability and adoption_regeneration') and R-D4 (L299, 'deciding_test and numerics_verdict'). AFTER_HEADLINE is 'H3, from the headline receipts' (legend, L93), and R-B4's disposition (L186) lists these as the campaign's gates.
- TESTED (V001 JSON): step4_by_reference marked all five LATER, and section 9 had none of them, against V001's own legend ('for step 4: before campaign wave 1').

**Change.** The five rows are `BEFORE_FIRST_RESULT` (step 4). Section 9 has a new block, 'At H3, from the headline receipts, before campaign wave 1' (phase 5; the later phases are renumbered by one). R-A4's note says its generator is written and reviewed before H3 (its disposition, L136) and that the record names no builder.

### SF-3: CONFIRMED, fixed

**Finding.** The step-4 producer and package state was stale at build time.

**Reason.**
- FORMAL: Claude3 0105 (`c0378a32`, born 01:19:16Z, before the V001 build at 01:37:51Z): PASS_WITH_FINDINGS, 0 BLOCKING, 7 SHOULD_FIX; PR-SF1 an escalation candidate; PKG-S1 (A105.3 not folded in; the disk guard has no implementer), PKG-S2 (the DIII tail_off_policy is missing), PKG-S3 (no item carries the route-A cap). Claude4 0119 (`4ee6044b`, 01:20:04Z) started producer v003 and package V003.
- TESTED (V001 bytes): S4-R-A1 said the review had been 'running since 00:25Z' and named 8e835ce3 as the T0 producer.

**Change.** S4-R-A1: the review is done; T0 uses producer v003 (`28921808...`, TESTED sha) once Claude3's delta check reports 0 blocking with PR-SF1 closed, and root may escalate PR-SF1 meanwhile. New **S4-R-B7** (the DIII tail_off_policy; `LATER`, because guard007 reads it only on the tail-OFF branch, L196-221). S4-R-D17: Codex1 implements the disk guard in the 0616 packet, Claude3 reviews, root records a df reading at admission until then, and A105.3 is folded in (DECIDED in part). The route-A cap stays in S4-R-D8 (SF-5). The ROOT_ITEMS_FINAL_C4V005 candidate is noted as V004's coming successor and compared (see 'State').

### SF-4: CONFIRMED, fixed

**Finding.** RI45-01 (a) dropped two producer obligations.

**Reason.**
- FORMAL: H5 in ROOT_ITEMS_CX1V002 (`47c6f836`) and V003 (`98a45bbb`) requires '... double replay, and guarded plan/admission hashes'. HANDOFF_CONTRACT_CX1V002 (`8eb07459`) L15: the producer 'must independently retain and verify native record/registry custody, actual rectangle membership, complete deterministic replay, guarded plan/admission provenance, post-state acceptance and point-scoped certificate validity'. Codex1 0074 (`4a0236d1`) blocker (3) and BUILD_CX1V001 (`c305a3b0`) L13 name post-state acceptance.
- TESTED (V001 bytes): RI45-01 (a) carried neither obligation.

**Change.** RI45-01 (a) now verifies all six obligations of the contract sentence: it adds the guarded plan and admission provenance (H5), post-state acceptance (step-4 R-B5) and point-scoped certificate validity (step-4 R-C1 and R-C8; the third obligation, beyond the two the refuter named, is in the same sentence). New MUST_FAIL controls: a missing or refused post-state acceptance; a plan or admission hash mismatch. The group-1 map has rows for 0074's blockers (1) to (4).

### SF-5: CONFIRMED, fixed

**Finding.** S4-R-D8's route-A cap rule misread its source and left the record's defaults without saying so.

**Reason.**
- FORMAL, LAUNCH_ORDER_C4V002 section 6.4: cap 3 for the 9- to 11-call batches, or cap 2 if root wants modelled free memory at or above 25% after admission; cap 3 models 17.1% in HEADLINE11. Section 6.5: cap 2 keeps 25% only while the increment over 2.805 GiB is at most 1.80 GiB (1.7972 GiB exactly); the H1 rule reads the C4T after-route-A tree RSS first. R-D8 (L334): the C4T plan caps (28 GiB), or 29 GiB for the 1.5x margin exactly.
- TESTED (V001 bytes): the rule was '2, unless that reading shows 3 keeps modelled free memory at or above 25%', with no branch for an increment above 1.80 GiB, and both defaults (28 GiB; cap 3) were replaced silently.
- TESTED here (exact arithmetic on the record's UNTESTED model, 11 calls, 17 GiB background, 128 GiB): 17.09%, 28.57%, 19.89% and 1.7972 GiB reproduce; cap 3 keeps 25% only while the after-route-A term is at most 2.829 GiB; cap 1 keeps 25% up to an increment of 3.216 GiB.

**Change.** S4-R-D8 (now 'Caps for the direct tail-ON runs, and the route-A concurrency cap'): RSS 29 GiB. The cap rule reads the C4T record first: cap 2 up to an increment of 1.80 GiB; above it, or with no RSS record, cap 1 (good to 3.22 GiB) unless root records that it accepts a dip, in which case cap 2; beyond 3.22 GiB, root accepts the dip or re-plans; cap 3 only if root accepts the modelled 17.1% dip. Both departures from the record are stated, and the V005 candidate's R-D18 (cap 3 by default) is named as option (c).

### SF-6: CONFIRMED, fixed

**Finding.** RI45-14's flag contradicted its own text.

**Reason.**
- TESTED (V001 bytes): flag 'BLOCKS_START (step 6). LATER for step 5', against the title 'one complete list before any value is read', the recommendation 'now' and the reasoning 'fixed before any step-5 value is read'.
- TESTED (strict JSON): FREEZE_EXPECTED_INPUTS_CX3V002 (`169df91f`) first_pass.root_inputs still lists 'registered driver branch acceptance or r006 fallback' (Claude3 0088 SF3).

**Change.** RI45-14 is `BEFORE_FIRST_RESULT` (step 5) and still blocks step 6; its row moves to section 9's step-5-read block; option (a) drops the r006 input and names cx3r008. N-5 is applied with it (RI45-27, RI45-28).

### SF-7: CONFIRMED, fixed

**Finding.** RI45-20's JSON rule imported a text fallback that JSON-only readers must not have.

**Reason.**
- FORMAL, V005 (`c01b3c51`): A102 orders parse_int=str and a text fallback only on JSONDecodeError for r13's check_record_codes; A90 keeps that path's 'legitimate text-format controls'; A71 makes duplicate keys refuse inside the parse.
- FORMAL: the writer, the filler and the extractor parse only JSON; HANDOFF_CONTRACT_CX3V002 (`6ae6a0fc`) L11 requires an integer, nonnegative selected log_index and finite, non-boolean u entries, which parse_int=str would break.

**Change.** RI45-20 (a): strict UTF-8 with no BOM; a JSONDecodeError is a typed refusal; no text fallback; a bounded parse_int inside the duplicate-refusing hook; parse_constant and parse_float refuse non-finite values; a nesting-depth cap; MUST_FAIL cases for each. A71 and A102 are cited for the principle only.

### SF-8: CONFIRMED, fixed

**Finding.** RI45-12 capped the first NGC point by a rule with no model to apply it to.

**Reason.**
- FORMAL: ADMITTED_POINT_RESOURCE_PLAN_V001 (`4de87df9`, read in full) is a K15 design estimate: K15_tail_memory cap_GiB_per_process 0.6 (DESIGN_ESTIMATE_UNTESTED_ON_NGC_FIXED_POINT); serial_peak_estimate_bytes_UNTESTED 3170424422.4; proposed caps 5 GiB serial and 45 GiB for parallel8; and its own sequence measures the first point before setting caps. A64.2 fixed NGC K_big 32 after it, and A55 raised the tail module's 0.6 GiB guard to 8 GiB. READINESS_REPORT_CX3V001 (`c7c72d54`) has only dry-process RSS (at most 89,751,552 B). A61 records the E-OPS2 error class.

**Change.** RI45-12: the first point's caps rest on a named model, either a commissioned target-free K32/T120L estimate (then A61's 1.5x rule) or an explicit first-point cap with stated headroom, labelled UNTESTED; the first point runs solo under monitoring with no automatic retry, and later caps come from its measurement.

## State folded in (N-1, and what landed after the refuter)

- **r3 final (TESTED, ls and sha256).** `r3/` was born 01:56:31Z; PREREG `b0fba984` (unsealed); ROOT_ITEMS_R3 `b33270fe`, byte-equal to the draft V001 read. Line 598 still carries the unqualified C-9 row (C-2, line 242, is qualified by miss-domination), as do line 598 of the draft `fb40156a` and of the dry build `bdcf6aff`.
- **Claude4 0124** (`73f5faab`, 02:16:45Z): the first SEAL CANDIDATE post, with 'classifier: none' and no STAGE0 successor. **Claude4 0125** (`a58d1804`, 02:19:34Z): CX1-MR3-P1 confirmed from bytes, a two-sentence fix proposed and batched into one re-render; FB-3 (every V006 heading before the seal entry needs a row and a re-render).
- **Codex1 0119** (`ae2374c4`) and its record `ee375b8d`: the A98.2 delta reads PASS with 0 blocking in its scope. **Codex1 0120** (`27d2bd75`): CX1-MR3-P1 an OPEN SHOULD_FIX, CX1-MR3-P2 CLOSED, the M-12 pair still needed.
- **V006 (TESTED).** `b22bd18ae4c3142be54db0e965b2a2fff4264e787fa29963bd637b6ae2ddc6a4` since 02:42:32Z: `43d4562b` plus one inserted section, A112 (seal tool 4 v004 SELECTED; the disclosures file V002; R-02), placed before the 'A108 continued' heading (diff of the byte copies). Copied to V006_ADDENDUM_COPY_AT_FIX.md (`b22bd18ae4c3142be54db0e965b2a2fff4264e787fa29963bd637b6ae2ddc6a4`, equal to the live file now). A112 decides no item here; r3's re-render needs its row.
- **Step 4 (TESTED, ls and sha256; FORMAL, the work log).** The ROOT_ITEMS_FINAL_C4V005 candidate is in `v003_work/order/` (`753e7e25`), its build stage complete at 02:39:38Z, not reviewed or published; producer v003 is `28921808`. Its R-B7 and R-D17 agree with S4-R-B7 and S4-R-D17 here; its R-D18 defaults the route-A cap to 3, where S4-R-D8 defaults to keeping 25% free.
- **Dispatch 0648** (`101f671f`): seal-path wiring (A112); it assigns no step-4 builder, so S4-R-C1 and S4-R-B4a still have none.
- **Where.** Flags 1 and 4; S4-R-A1, S4-R-B7, S4-R-C1, S4-R-D8, S4-R-D17; RI45-16, RI45-27 to RI45-30, RI45-32 and RI45-40; the group-6 and group-7 introductions; section 8.

## The notes

| note | confirmed from | change in V002 |
|---|---|---|
| N-1 | TESTED (the r3 folder, its files and line 598) | the state update above |
| N-2 | FORMAL: A98.1 ('enumerated, byte-pinned'; 'enumerated and pinned before closure'); dispatch 0619 L15; the review's own fix is a disposition successor | RI45-24: issue quotes both texts; the V006 entry is quoted verbatim and pinned by its section sha; (b) named as the review's fix; flags 3 and the group-5 intro say 'recommended' |
| N-3 | no source tests that the N-tests are independent of the calibrated point; Claude3 0088 missing item 13 asks root to confirm it | RI45-06: option (b) and the recommendation label the premise UNTESTED and state its basis |
| N-4 | r3 M-3 (`b33270fe`) first asks to adopt the §2 rule set as written | RI45-31: title, issue, options and recommendation |
| N-5 | V001 flags of RI45-27 and RI45-28 against their own notes | both `BEFORE_FIRST_RESULT` (step 5), with SF-6 |
| N-6 | CARRIER_CONTRACT_CX3V001 (`252ef9e1`) role A17_C3, schema UNT_ROOT_A17_C3_REGISTRATION_CX3V001; READINESS_DELTA and FINDINGS_S2 L246 | RI45-34: the seal entry states that the A17_C3 role carries A27's T120L record, or names a contract successor |
| N-7 | PAR8-N6 text in REVIEW_NGC_V011_CX3R008_C4V001 | RI45-20's module covers any dry harness root uses for RI45-13; group-5 map |
| N-8 | RI45-09 and RI45-20 are both needed before the first real handoff | RI45-10 (a) lists them |
| N-9 | LAUNCH_ORDER_CX3V002 (`829a8cb6`) L5: 'choose r006 fallback unless Claude4's r007 review is accepted' | RI45-08 (a) replaces it in the same round |
| N-10 | slots V003 register ORIGINAL_K EVALUATED_BEFORE_FREEZE; FREEZE_EXPECTED_INPUTS: 'not silently omit it' | RI45-15 (b) needs a root-approved slots successor first |
| N-11 | TESTED: H7 and H8 statuses differ between CX1V002 and V003; ROOT_ITEMS_CX3V001 (`446f3406`) R1-R3 and R6-R10 equal V002's, R4 and R5 are earlier wordings | group-1 map shows both statuses; group-2 intro cites CX3V001 |
| N-12 | H6 (CX1V003); READINESS_DELTA rough edges; REVIEW_STEP4_HANDOFF_C3V001 notes CX-N3, ADM-N4, ADM-N6, ADM-N7 | RI45-06 (H6's validity replay); RI45-11 and the group-2 map (refused geometry stays INVALID); RI45-20 and the group-4 map (CX-N3, ADM-N4); RI45-09 (ADM-N6); RI45-01 and RI45-10 (ADM-N7) |
| N-13 | A85.2: 'It applies from the step-2 launch onward' | S4-R-D11's issue |

## Checks (TESTED)

- Builder dry runs 1 to 4 (02:43:55Z to 02:53:43Z) and the final build (2026-10-19T02:55:14Z) exited 0; every non-volatile source re-hashed equal (a mismatch refuses the build); volatile changes are recorded in V002 section 10.
- CHECK_ROOT_ITEMS_STEP45_V002.py on the staged pair: 175 of 175, including: the only new ids are S4-R-B4a and S4-R-B7, no V001 id is dropped, and only RI45-14, RI45-27 and RI45-28 change flag among V001's items; the phases shift consistently; exactly the five H3 rows change in the by-reference table; the summary counts, order and phases; the MD headings, Blocks lines and section-9 rows equal the JSON; 55 recommendation lines; each fix's key phrases are present and the stale V001 phrases are gone; strict JSON with no duplicate keys or non-finite values.
- The published bytes equal the staged bytes (compared in the publishing step).

## Conduct

- No launch; no driver, orchestrator, writer, filler, extractor, producer, guard, launcher, binder or compare was imported or run. No NGC3198 target or observed-velocity file, rotmod, Vobs, MassModels or SPARC file was opened. Nothing under runs_ext, KMAX_A2F10_C5H_RUN_V001 or any UVT_* path was read, listed or stat'ed. No network, delete, move or overwrite.
- Reads: the named sources only (V002 section 10 lists each with its sha); greps of named files only; ls of named folders; `df -k` on two volumes. The V005 and V006 decisions files carry NGC3198 in their names; they are rulings, not target data.
- Writes, all in this folder by exclusive create: PARTIAL_FIX_V002.md (created once, then appended), V006_ADDENDUM_COPY_AT_FIX.md, the V002 pair, BUILDER_ROOT_ITEMS_STEP45_C4V002.py, CHECK_ROOT_ITEMS_STEP45_V002.py, this file and HASHES_ROOT_ITEMS_STEP45_V002.txt (written last). Python ran as `python3 -I -B` with single-thread BLAS variables.
- Disclosures: the scratchpad copy of the builder was edited in place (Edit tool, and one Python patch for the phase renumbering and the r3 source keys) before it ran; staging, logs and this file's generator are in the session scratchpad. One shell command failed before printing (a sed range built from a grep that matched two lines), with no effect on any file.

