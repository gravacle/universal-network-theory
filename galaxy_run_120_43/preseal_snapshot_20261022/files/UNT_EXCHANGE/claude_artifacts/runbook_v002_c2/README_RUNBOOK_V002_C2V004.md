date -u: Mon Oct 19 18:43:51 UTC 2026

# runbook_v002_c2, build c2v004: one run file serves one call (the blocking finding against c2v003 fixed; root workflow build; not adopted)

**What this is.** The fourth build of the A142 build-table item "RUNBOOK_V002 and roster builder (A133), root workflow, Claude4 review". It fixes the blocking finding against c2v003: one cut-record file could serve two calls. Nothing here is adopted until root pins it and Claude4 reviews it. Nothing authorizes a launch or target access. No production build, pass or step 7 was run. The c2v001, c2v002 and c2v003 files in this folder are unchanged and are superseded by these; root pins only the c2v004 files and `ROOT_TSR_FLAG_RECORD_V002.json` (unchanged since c2v003).

## Files

| file | sha256 | what it is |
|---|---|---|
| `roster_builder_c2v004.py` | `8e8022e2978c605e299e66032dfbd63ede8288244d309aa5194f933c9f3dfeea` | The builder. Commands as in c2v003 (`build`, `pass`, `step7`, `sens-budget`, `check-gate-list`, `seal-check`, `tsr-record`, `tsr-check`). Changed: the cross-call file check (below). |
| `RUNBOOK_V002_C2V004.md` | `06ca537f1683a6c01f611ab95717e2a964d3bca81cd84bd1567160b0a075d4af` | The per-phase runbook (V001 step numbers kept; no step map). Changed: §1 "One run file serves one call" (replaces c2v003's one-sentence claim), the R2 bullet, step 3, §4 rule (a), G10, new G29, §8. |
| `test_runbook_v002_c2v004.py` | `98d0293f19f2d3466c344d46d53c7e771871c447d99d6da8d96ef1ffd2bd3d39` | The synthetic MUST_PASS / MUST_FAIL suite: the 124 c2v003 cases ported, 13 new (H01–H13). |
| `test_records_c2v004/RUN1/TEST_RECORD.json`, `test_records_c2v004/RUN2/TEST_RECORD.json` | `8b0def0e4cd68e5bb4d04cc2be0b3d1cec9665a91cf711442e2f611d08b681bf` (both; byte-identical) | Two record runs: 137/137 each (34 MUST_PASS, 103 MUST_FAIL); `results_sha256` `488a79c3add4010f8a722283735fcefc8b343316ced49b5b62b89d9e1aa9a563`. |
| `test_records_c2v004/RUN*/work/` | not hashed | The synthetic fixtures each run wrote, including (by design) the hard links H01, H03, H04, H05, H07 and H13 made inside the work directory, and the c2v003 cases' forged ledger entries, symlink and renamed ledger directories. |
| `ROOT_TSR_FLAG_RECORD_V002.json` | `c9d8ab4573278f2d325bc5fe50e396e35e9981f0561cfa20e61e8a215bb5cea0` | Unchanged (c2v003); still the builder constant. |
| `HASHES_V004.txt` | — | sha256 of every file above, from bytes. |

## Running it (`python3 -I -B`; every input is a JSON document pinned by sha256)

As in c2v003 with `roster_builder_c2v004.py`; the input schemas keep their c2v003 names (`ROSTER_BUILDER_INPUT_C2V003` and the rest), because no schema changed (C39). A c2v003 BUILD_RECORD is refused by c2v004 (`BUILD_RECORD_OTHER_BUILDER`). Suite: `python3 -I -B test_runbook_v002_c2v004.py --record-dir NEW_DIR`.

## The finding and the fix

| finding | fix | tests |
|---|---|---|
| **One cut-record file could serve two calls.** c2v003's RUNBOOK §1 (L50) said a cut record or result file serving two calls refuses (`CUT_RECORD_BORROWED`, RI45-11), but the builder compared realpaths only (c2v003 L978-988). M000's cut record hard-linked into M001's terminal run directory, with a result consistent with that cut, built BUILT and pass one read M001 evaluated and valid (c2v001 probe A2e, open since c2v001); a byte copy built BUILT too; so did a hard-linked or copied result | Every receipt, result and cut record is identified by realpath **and by file identity** (`st_dev`, `st_ino`, from the fstat of the descriptor whose bytes the builder hashed); one file serves one call. Cut records **and the results of FINISHED calls** are also identified by sha256: one content serves one call (a byte copy refuses). Receipts keep R2's realpath and sha256 checks and add the file identity. Codes: `CUT_RECORD_BORROWED` when either file is a cut record, else `FILE_BORROWED`; `RECEIPT_REUSED_ACROSS_CALLS` between receipts. The identity is never written to an output, so builds stay byte-deterministic | H01 (A2e), H02 (byte copy, the finding's REUSE1), H03 (hard-linked result), H04 (hard-linked receipt), H05 (across alternatives at one theta), H06 (cut records naming no call: refused, G29), H07 (a cut record as another call's result), H09–H11 (byte-copied results), H13 (hard-linked failure record); controls H08 (equal radius, own record: BUILT and passes), H12 (byte-identical failure records of two FAILED calls: BUILT); B09 kept |

**Beyond the stated fix (CHOICE C38, root confirms or replaces).** The finding asked for the file identity on all three roles and sha256 on cut records, and left byte-copied results to v003g. A development probe showed v003g does not catch every copy: a byte copy of PRIMARY M000's result saved as ORIGINAL_K M000's result (distinct calls at one theta) built BUILT under c2v003 and pass one read ORIGINAL_K M000 evaluated, forward_valid and member_valid true. c2v004 therefore applies the sha256 rule to results too, but only when either side is a FINISHED call's result: two FAILED calls may save byte-identical failure records, as the four Phase-2 geometry sensitivity calls do in every Phase-2 fixture (a mutant that makes every result unique fails 18 Phase-2 cases and H12).

**Still not detected (G29, disclosed).** (1) A byte copy of one FAILED call's failure record as another FAILED call's (allowed by design; the call is EVALUATED_FAILED by its own bound receipts either way). (2) A file taken from a run that is not one of the build input's calls: no path, identity or content check can see it. Closing (2) needs the cut record and result to carry their call's binding keys (`theta_sha256`, `spec_sha256`, as receipts do under G27), a change to the CX3V001 cut-record producer; `st_nlink` 1 per run file would catch hard links from anywhere but not copies.

**Development checks (scratchpad `rbv004c2/`, not record runs).**
- The c2v004 suite run against the c2v003 builder's bytes: 126/137, failing H01–H07, H09–H11 and H13 (H04 only by its detail: c2v003's sha256 check already caught the hard-linked receipt). The suite reproduces the finding against c2v003.
- Probe on the c2v003 builder: the A2e construction BUILT, pass one M001 evaluated / forward_valid / member_valid true; the ORIGINAL_K result copy as above. Under c2v004 both refuse (`CUT_RECORD_BORROWED` by file identity; `FILE_BORROWED` by sha256).
- 8 mutants of the c2v004 check, all killed: no file identity for run files (H01, H03, H05, H07, H13); no content rule (H02, H06, H09–H11); content for cut records only (H09–H11); content for every result (18 Phase-2 cases, H12); cut-record code only for the later file (H07); no file identity for receipts (H04); content rule only when the later file is unique (H11); c2v003's realpath-only loop (H01–H03, H05–H07, H09–H11, H13). c2v003's 18 mutants were not re-run; the 124 ported cases keep c2v003's observed codes.

## Classifier A's records

Unchanged from c2v003: the builder writes `GATE_STATUS_LIST.json` (`GATE_STATUS_LIST_C4V001`) and `ROOT_TSR_FLAG_RECORD_V002.json` (`TSR_FLAG_RECORD_C4V001`) in A's schemas exactly; the 15 other inputs A expects, and their writers, are listed in RUNBOOK §6b and the builder constant `A_INPUTS_NOT_PRODUCED` (root: `phase_inputs`, `stage0_status`, `commitment_status`, `fallback`, `field_map`, `root_disclosures`; other producers: `freeze_manifest`, `score`, `slots`, `tsr_support_record`, `ntest_compare`, `agree_record`, `phase1_classification`, `l1_record`, `c3_record`). OI-A1 to OI-A3 stay open for Claude4. Classifier A's README was not reopened by c2v004.

## CHOICES this build made that the text did not force (root confirms or replaces each)

C1–C36 are carried from c2v003 unchanged.

- **C37. File identity.** `(st_dev, st_ino)` from `os.fstat` on the descriptor whose bytes are hashed, for every receipt, result and cut record of a roster call (receipts of OTHER calls too, in the R2 receipt check). Call identity as in C33. The identity is held in memory only.
- **C38. Content rule scope.** sha256 uniqueness across calls for cut records (the finding's fix) and for the result of a FINISHED call against any other call's cut record or result (beyond the finding); not for failure records between FAILED calls. Receipts keep R2's sha256 rule.
- **C39. Schema names.** No input or output schema changed, so the c2v003 schema names are kept; the BUILD_RECORD's builder sha separates the versions.
- **C40. Codes.** `CUT_RECORD_BORROWED` when either of the two files is a cut record (c2v003 decided by the later file's role); `FILE_BORROWED` otherwise; details name how the file was recognised (realpath, file identity or sha256).

## Gaps

Root rulings needed (detail in RUNBOOK §7): those carried from c2v003 (G1, G2 residual, G3, G7, G8, G9, G10, G13–G21, G24–G28) and new **G29**: whether distinct calls may carry byte-identical cut records or FINISHED results (c2v004 refuses both, fail-closed), whether byte-identical failure records are allowed (c2v004 allows them), and whether cut records and results must carry their call's binding keys so that a file from a run outside the build input can be refused.

## UNTESTED (deciding tests in RUNBOOK §8)

As in c2v003, plus: whether real cut records and FINISHED results of distinct calls always differ in bytes (the first real MEMBERS or FULL build decides; a "by sha256" refusal there goes to G29); the file identity on the production run root's file system (A157's `/Volumes/External1/NGC_S0_PHASE1_V001`, not opened).

## NOTEs (not blocking, recorded)

- **A157 and the gate-status list (A157 read at L1243-1250 and L1262-1280 only; nothing changed here).** V006 A157 pins 15 M-15 gate documents (GATE_PIN rows: the N-test compare, N1, the GL4 nodes, the S0 binding and others) and records "Root-listed row gates known at launch: none". The builder's gate-status list covers only its `gate_documents` input, which must be REGISTERED_INVALID_ROW_GATE_CX3V001 documents (`GATE_REGISTRATION_REQUIRED` otherwise), so a production FULL build would write `{"gates": []}`. Root and Claude4: confirm which set classifier A's `gate_status_list` must carry. If it is A157's 15 pins, a successor needs a separate gate-pin input for the list.
- Carried from c2v003: a rebuild under a different ledger root gets its own ledger (a V006 event under G28); deleting the last ledger entry is not detectable by the tool.

## Deviations (disclosed)

- **Drafts in the scratchpad.** The builder, tests, runbook and README were drafted in `/private/tmp/claude-501/-Users-bgm-MB-Work/04dac55c-b963-46a5-9ea4-74afb63af51b/scratchpad/rbv004c2/`, where four development runs, the run against the c2v003 bytes, the probes (`probe_residuals.py`) and the mutation check (`mutate_c2v004.py`) ran. Each published file was written once, by exclusive create, from those bytes. No existing file in this folder was edited.
- **Beyond the finding's fix:** C38 (FINISHED results by content); C40 (the code when either file is a cut record).
- **Fixture change in the ported cases.** A synthetic cut record now names its call in `classification_evidence` (`synthetic_call`). Under the c2v003 form, PRIMARY's and ORIGINAL_K's cut records at one theta were byte-identical in every Phase-2 case, and c2v004's content rule would refuse them. The change assumes real cut records differ between calls; H06 keeps the c2v003 form and shows the refusal. All 124 ported cases keep their ids, expectations and observed codes (checked against the c2v003 record).
- **Hard links in the record runs** are made with `os.link` inside each run's work directory only.
- **Opened:** the c2v003 README, RUNBOOK, builder and tests, HASHES_C2V003 and the c2v003 test record; V006 (`41fe5aa2`, through A159) by its heading list, a keyword grep (hard link, inode, BORROWED, RI45-11, cut record, c2v003, c2v004, runbook_v002_c2, G27–G29, launch registry; no ruling on file reuse) and A157 at L1243-1250 and L1262-1280. The suite reads the compare, N1 and node records that the TSR records pin, from bytes.
- **Not opened.** `classifier_a_c4v001.py` and classifier A's README (not reopened), the slots, the program query manifest, the A133 text, run trees, `/Volumes/External1`, ~/.codex, `c5h_hull_c2/`, `UVT_*`, anything under `v003g/slots`, `runs` or `independent235`, and any NGC3198 target or observed-velocity file.
