# PARTIAL - text_c4 (r3 TEXT BUILDER helper of lane Claude4)

Log is append-only; newest entry last. Labels: TESTED / FORMAL / UNTESTED.

## 2026-10-18T20:58:55Z start
- Folder created. Inputs re-hashed from bytes: 0619, 0585, 0606, 0490, REVIEW_CX2V001.md, FINDINGS_CX2V001.json, HASHES_DRAFT_START.txt and all files it lists, HASHES_R2.txt and all 10 files it lists: all match the shas given in the task (TESTED).
- Next: copy V005 addendum, read rulings, read the four draft text files and all recheck REVIEW.md files.

## "$TS" sources read
- V005 byte copy V005_ADDENDUM_COPY.md = 70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e (copied 20:59:14Z; re-hashed equal, TESTED). 55 heading lines starting '## ' (A47..A77 in order, then A101 down to A78, then A76, A75, A65). Read in full.
- V003 5bef6552 and V004 487d4449 re-hashed equal to the r2 pins (TESTED); A10, A12, A15, A20, A21, A27, A41, A42 read.
- Draft r3 four text files, generator v004 and check v003 read. Round-2 lens REVIEW.md x3 and six refuter REVIEW.md read; refuter VERIFY.md sections read where they carry better fixes. Codex2 0490 + REVIEW_CX2V001 + FINDINGS read. Round-1 extract read for the 21 PARTLY rows.
- Also read (target-free): RUNBOOK_V001 9557b5aa; slots V003 d3859b42 (observation rule, alternatives, STAGE0 registration, SA notes; no query values beyond ids/radii); K32 compare 6f095f64 gate fields; GL4 nodes ec1dcca5 (r14, r15, r16 exact); Codex3 extractor 50c7db5f support schema (L200-250); Codex1 0066 f2d94655; Codex2 CHECKLIST_CX2V001 020ef3f1; 0512, 0550.
- Parallel stage seen: r3_work/tools_c4 (TOOLS builder). Tool-only findings will be routed there, not fixed here.
- Plan: S(Z) rule M-U<N_v/2 (qualified by miss-dominated); P14/P15; reading-centric table with one tuple rule per reading; R-UT1/R-REACH deficit-type (NOT_ADDRESSED with reason under EXCESS/UNSIGNED), R-HIST sign-free; A10 two-way rule; LATE = not pinned before first step-5 launch receipt; truthful LATE lemma (to be TESTED by a synthetic enumeration in tools/).

## 2026-10-18T21:19:36Z self-test and work copies
- tools/verify_r3_rules_c4.py (written with the Write tool on a new path; no overwrite) encodes the planned r3 §2/§4 rules. Run 21:19:18Z: 200000 random + 265716 exhaustive synthetic outcomes, all checks pass (TESTED, synthetic only): OUTER_FAILURE <=> exactly one of P1/P2/P11/P14; coverage; |m|>1 => miss-dominated; P5 <=> INNER hit-dom & OUTER_FAILURE & P13; P6 => zone patterns; no sign class from a minority of signed misses; LATE vs on-time lemma (removals only within {P0,P1,P1g,P2,P3,P4,P5,P6,P7,P8,P9,P11,P11g,P12}, additions only within {P5,P7,P13,P14,P15}, every listed change witnessed; P10 unchanged; E3 only toward TESTED-NEGATIVE; deficit-type readings never become CONSISTENT). Output R3_RULES_SELFTEST.json sha256 f303af667b7f6f50489f6450ff57ad519733cfe0e115034963bd4039785f21f7.
- Four draft text files copied with exclusive create (shas equal to HASHES_DRAFT_START). They are the work copies to be revised.
- Self-reported slip: one earlier command used echo with a string starting with =; zsh refused it ('== not found'); nothing else ran or changed. Later separators use printf.

## 2026-10-18T21:26:32Z V005 moved
- Live V005 re-read at 21:25:59Z: 27b62183a4c2f4a992d30cfee56e58e395dc2b6e74c85fe73290a26478b9469f (137698 bytes). Byte copy V005_ADDENDUM_COPY_27b62183.md made at 21:26:06Z (re-hashed equal, TESTED). Diff against the first copy: one pure insertion, A102 (r12 reviews split; r13 closes A-B1), between A77 and A101; nothing else changed (TESTED by diff). A102 is V007-compare only: NO_CHANGE.
- The entry table will be built last, from the newest bytes, with a final live re-check.

## 2026-10-18T21:36:20Z text revised
- PREREG_MISS_READING_R3.md and ROOT_ITEMS_R3.md rewritten in the work copies (r3 content: S(Z) rule, U(Z), P14/P15, P11g/CROSSING, OUTER_FAILURE equivalence, reading-centric table with one tuple rule per reading, A10 and A15 E3 rules, deficit-type sign rule, LATE definition and truthful lemma, NOT_READ trigger, TSR stop and support record, STAGE0 identical rule, fallback versions and attestation, A101 for the LO I1-T item; M-15 new).
- Baseline run of the draft check v003 on the work folder: T1, T2, T3, T5, T6 PASS; T4 missing 9.901810628740723, 10.911721936765339, 0066, 99 (to add); T7 FAIL expected (placeholders not rendered). (TESTED)
- Next: CLOSURE_R3.json builder, CSM rewrite, provenance, entry table.

## 2026-10-18T21:49:23Z slip disclosed; V005 moved again
- Self-reported slip (rule 2): at about 21:33Z one stdout redirect wrote the draft check's JSON output to the session scratchpad (scratchpad/chk1.json), outside this folder. It holds only the check result on this folder's work copies (no target content). Nothing else was written outside this folder. Later check outputs go to this folder's work/ subfolder.
- V005 re-read 21:46:18Z: 643ef6efee21df4875b5e2cffc2f6aefe40ee479052b313fed479fd89a73d343 (138581 bytes); byte copy V005_ADDENDUM_COPY_643ef6ef.md at 21:46:26Z; diff against 27b62183: one pure insertion, A103 (Codex2 out of usage; the miss-reading r3 delta moves to Codex1; cx3r008 accepted). A103: NO_CHANGE (a review assignment and launch custody, no clause). 57 heading lines.
- Entry-table builder dry run on 643ef6ef: 57 headings, 57 rows, 19 CITED_PINNED (= M-6 item 3 list), 38 NO_CHANGE, both section extractors agree (TESTED).
- Closure builder dry run: 94 rows (85 FIXED, 2 NOT_ADOPTED, 7 ROUTED_TO_TOOLS_STAGE); every lens id (16 + 13 + 14), both Codex2 ids and all 21 round-1 PARTLY rows covered (TESTED).
- Targeted deny-list scan of the three texts, the provenance JSON, the closure strings and the entry-table reasons: one hit fixed ('things' in a PREREG sentence; 'observed curve' in a closure finding); Greek option labels in ROOT_ITEMS replaced by ASCII words (TESTED).

## 2026-10-18T21:52:31Z deliverables written; dry checks
- CLOSURE_R3.json written 21:49:28Z (exclusive create): e21dfe8a66881be8b7c01f5e85b868867b663a6c2aa17ab7c79f0effaa84007b (94 rows: 85 FIXED, 2 NOT_ADOPTED, 7 ROUTED_TO_TOOLS_STAGE).
- V005_ENTRY_TABLE_R3.json written 21:51:21Z (exclusive create) from V005_ADDENDUM_COPY_643ef6ef.md (live V005 re-hashed equal at 21:50:57Z and at the build): d9d0d70288746f8e5b24e1db122937a73fc1e729da5bfaece8602d84d53b1a77 (57 rows; 19 CITED_PINNED; 38 NO_CHANGE).
- CSM closure tables rebuilt from CLOSURE_R3.json (with a finding column); ROOT_ITEMS wording fixes (120/43 phrase; Greek labels; no flat-curve wording).
- Draft check v003 on the unrendered work copies: T1-T6 PASS, T7 FAIL only because the placeholders are unrendered (TESTED, work/CHECK_V003_ON_TEXT_UNRENDERED_2.json).
- Rendered simulation (work/render_sim: placeholders filled from V005_ENTRY_TABLE_R3.json in the r2 row format, NO_CHANGE ids as the comma list; dispatch shas from bytes): check v003 target-free PASS and currency PASS, 19/19 section pins match the live V005 (TESTED, work/CHECK_V003_ON_RENDER_SIM.json).
- Draft mutation test v003 on the simulation: its v005_end_marker_changed case cannot apply (r3 has no end-marker; assertion in the test, work/mutation_scratch left partial). With that case removed (tools/run_mutation_minus_endmarker_c4.py): 25/25 ok, baseline PASS/PASS (TESTED). The tools stage must replace that case.

## 2026-10-18T21:56:05Z final
- Final edits after the JSON files: M-12 adds C16d as a P1 control; M-14 made verbatim identical to the PREREG 6.3 rule (8/8 operative sentences equal, TESTED); the PREREG's stray A55 mention rephrased. PREREG and ROOT_ITEMS together reference exactly the 19 CITED_PINNED V005 entries; M-6 item 3 lists the same 19 (TESTED). The clause map's closure rows name two NO_CHANGE entries (A80, A97) as context.
- Final render simulation (work/render_sim_3) against live V005 643ef6ef at 21:55Z: check v003 T1-T7 PASS (target-free PASS, currency PASS); mutation v003 minus the end-marker case 25/25 ok (TESTED). Extended deny-list scan of the four files clean (TESTED).
- HASHES_TEXT_C4.txt written (exclusive). work/CLOSURE_TABLES_R3_FRAGMENT.md is the first fragment (no finding column); the clause map carries the rebuilt tables generated from CLOSURE_R3.json.
- For the tools stage / lead (not done here): (1) render V005_ENTRY_TABLE_R3.json into the PREREG placeholders @@V005_ENTRY_ROWS@@ (CITED rows) and @@V005_UNCITED@@ (NO_CHANGE rows, with reasons); (2) T5/T7 verify the table against V005 bytes; T7 over every '## ' line; (3) replace the mutation case v005_end_marker_changed (r3 has no end-marker); (4) if heading lines are rendered, their numeric tokens need provenance rows (the reasons need none beyond those listed); (5) the 7 ROUTED_TO_TOOLS_STAGE rows and every tools_stage note in CLOSURE_R3.json.
- Open: V005 keeps growing (A102, A103 appeared during this stage); any heading after 643ef6ef needs a hand-written row in a successor table. A103 moves the r3 delta check to Codex1. R2B-08 module paths not pinned (not in inputs). The self-test is synthetic and checks the text's rules only; the M-12 classifier is not built.
- No target, observed-velocity or protected-run path was opened, listed or stat'ed; nothing launched; no network; no deletes or moves. One write outside this folder (scratchpad/chk1.json), disclosed above.
