date -u: Mon Oct 19 19:12:40 UTC 2026

# runbook_v002_c2, build c2v005: root's rulings on the c2v004 re-verify and on G29 (root workflow build; not adopted)

**What this is.** The fifth build of the A142 build-table item "RUNBOOK_V002 and roster builder (A133), root workflow, Claude4 review". It implements two root rulings:
- the cross-call file check covers every call of the build input;
- G29: a cut record is bound to its call by residence.

Nothing here is adopted until root pins it and Claude4 reviews it. Nothing authorizes a launch or target access, and no production build, pass or step 7 was run. The c2v001 to c2v004 files in this folder are unchanged and superseded. Root pins only the c2v005 files and `ROOT_TSR_FLAG_RECORD_V002.json`, which is unchanged since c2v003.

## Files

| file | sha256 | what it is |
|---|---|---|
| `roster_builder_c2v005.py` | `653ced76513d3415d8d4904a73bf1c2dc6d316a053be4f89029611c80ffc9075` | The builder. Commands and input schemas are as in c2v004. Changed: the cross-call file check (below). |
| `RUNBOOK_V002_C2V005.md` | `b34f294a738e7697a0a223651dc9e2bf2956dace7e9ab66001efc84978fe3ac6` | The per-phase runbook. V001 step numbers are kept, so no step map is needed. Changed: the header, §0 (builder and V006 rows), §1 "Call record", §1 "One run file serves one call" (rewritten), the R2 bullet, step 3, §4 rule (a), G10, G29 (now ruled), §8. |
| `test_runbook_v002_c2v005.py` | `90158184fd45f6822cd5e625f729cd2e1361661ff8f14b8b4c82ad97b6aa27ba` | The synthetic MUST_PASS / MUST_FAIL suite: the 137 c2v004 cases ported, two with changed expectations (below), and 12 new cases (J01–J12). |
| `test_records_c2v005/RUN1/TEST_RECORD.json`, `test_records_c2v005/RUN2/TEST_RECORD.json` | `dbabe47228bf45ae43313b46e3cfa16f7e4686365a077f6464319faa0cb1847e` (both; byte-identical) | Two record runs: 149/149 each (38 MUST_PASS, 111 MUST_FAIL); `results_sha256` `dc360aa67eb1175bdcf65c1c3855c3890914cb76acaa467913e978ce43ee2e8d`. |
| `test_records_c2v005/RUN*/work/` | not hashed | The synthetic fixtures each run wrote. By design this includes the hard links made by H01, H03, H04, H05, H07, H13, J02, J03 and J08 inside the work directory. |
| `ROOT_TSR_FLAG_RECORD_V002.json` | `c9d8ab4573278f2d325bc5fe50e396e35e9981f0561cfa20e61e8a215bb5cea0` | Unchanged since c2v003; still the builder constant. |
| `HASHES_C2V005.txt` | — | sha256 of every file above, from bytes. |

## Running it (`python3 -I -B`; every input is a JSON document pinned by sha256)

Run it as in c2v004, with `roster_builder_c2v005.py`.
- The input schemas keep their c2v003 names (`ROSTER_BUILDER_INPUT_C2V003` and the rest), because no schema changed (C39).
- c2v005 refuses a c2v004 BUILD_RECORD (`BUILD_RECORD_OTHER_BUILDER`).
- The suite is `python3 -I -B test_runbook_v002_c2v005.py --record-dir NEW_DIR`.

## The rulings and what the builder now checks

| ruling | c2v004 | c2v005 | tests |
|---|---|---|---|
| **(1) The file identity check covers every file of every call:** realpath and (`st_dev`, `st_ino`) from the fstat of the hashed descriptor, for roster AND OTHER calls (receipts, results, cut records). | Only receipts were compared across all calls. Results and cut records were compared only among roster calls. The re-verify probes built BUILT: Q4b (M001's result pin was F1's receipt), Q4 (a hard link of F1's receipt as M001's result) and Q5 (a hard link of an OTHER call's receipt, which also parses as a cut record, as M001's cut record; pass one read M001 evaluated and valid). | Every run file of every call is identified by realpath and file identity: a roster call's receipts, result and cut record, and an OTHER call's receipts. `other_phase_calls` carry receipts only, since the input has no result or cut record for them. Codes: `RECEIPT_REUSED_ACROSS_CALLS` between receipts (checked first); then `CUT_RECORD_BORROWED` if either file is a cut record, else `FILE_BORROWED`. RUNBOOK §1's claim is now what the builder checks. | MUST_FAIL J01 (Q4b, by realpath), J02 (Q4, by file identity), J03 (Q5, by file identity) |
| **(2) G29: residence.** A cut record's realpath lies inside its own call's registered run directory and inside no other call's, and its file identity is distinct. | A cut record had to lie inside the terminal run directory only. | Unchanged: `CUT_RECORD_NOT_OF_ITS_CALL` when the cut record is outside its call's terminal run directory. New: `CUT_RECORD_IN_OTHER_CALL_RUN_DIR` when it is inside any run directory, of any attempt, of any other roster or OTHER call. The identity check of ruling (1) applies too. The residence check runs after the identity and content checks, so B09 keeps `CUT_RECORD_BORROWED`. | MUST_FAIL J05 (outside its own run directory), J06 (inside another roster call's terminal run directory), J12 (inside another call's non-terminal run directory), J07 (inside an OTHER call's run directory), J08 (hard-linked across calls); H01, H05 kept |
| **(2) G29: the byte-equality refusal for cut records is REMOVED.** | A cut record with the sha256 of another call's cut record or result was refused. | Removed. Two calls may carry byte-identical cut records. | MUST_PASS H02 and H06 (changed, below), J04 (Phase 2: PRIMARY and ORIGINAL_K at one theta with byte-identical cut records; MEMBERS build and pass one) |
| **(2) C38 KEPT:** a FINISHED call's result byte-identical to another call's cut record or result is refused. | Kept, but compared only with the first owner of a sha256. | Kept, and checked over all pairs of calls. `CUT_RECORD_BORROWED` if the other file is a cut record (C40), else `FILE_BORROWED`. | H09, H10, H11 kept; MUST_FAIL J10 (a FINISHED result with another call's cut-record bytes, in both call orders) |
| **(2) FAILED-call failure records may be identical but must reside in their own run directory.** | Allowed; residence checked (`RESULT_NOT_OF_ITS_CALL`, which no test covered). | Unchanged. | H12 kept; MUST_PASS J09 (re-verify probe Q6: a failure record with another call's cut-record bytes; both call orders build, where c2v004 refused one order); MUST_FAIL J11 (a byte-identical failure record in another call's run directory, `RESULT_NOT_OF_ITS_CALL`) |

**Ported tests whose expectation the G29 ruling changes** (the only two; 135 others keep their ids, expectations and observed codes, checked against the c2v004 record):
- `H02_byte_copy_of_M000_cut_record_in_M001_run_dir_refused` (MUST_FAIL `CUT_RECORD_BORROWED` by sha256) is now `H02_byte_copy_of_M000_cut_record_in_M001_run_dir_builds_G29` (MUST_PASS). The copy lies inside M001's own run directory and is a file of no other call. It builds, and both roster contexts carry the same bytes.
- `H06_distinct_calls_with_byte_identical_cut_records_naming_no_call_refused_G29` (MUST_FAIL `CUT_RECORD_BORROWED` by sha256) is now `H06_distinct_calls_with_byte_identical_cut_records_naming_no_call_build_G29` (MUST_PASS). It builds, with all three members EVALUATED.
- Not an expectation change: H08's docstring lost the clause "the sha256 check reads the record's bytes", and its body is unchanged.

**What the residence binding does not see (disclosed; G29 item 4 stays open).** The builder sees where a cut record is and whether it is another call's file. It does not see who wrote it. So these build under c2v005:
- a byte copy or a re-serialized copy of another call's cut record written into a call's own terminal run directory (H02; re-verify probes Q2, Q3, Q3b);
- a hard link of a file that belongs to no call of the build input (probe Q7).

Only a binding key carried in the cut record would close this, a change to the CX3V001 cut-record producer. No honest producer writes such files (A115).

## Development checks (scratchpad `rbv005c2/`, not record runs)

- **The c2v005 suite on the c2v004 builder's bytes: 139/149.** It fails:
  - H02, H06, J04 and J09: the cut-record content rule;
  - J01–J03: OTHER calls are outside the run-file check;
  - J06, J07 and J12: there is no residence rule.

  The suite therefore reproduces the re-verify finding and the G29 changes. J05, J08, J10 and J11 pass on c2v004 too: their rules already existed there.
- **The re-verify probe script** (`rb4verify/probe2_c2v004.py`, run unchanged on the c2v005 builder):
  - refused: Q1, Q4, Q4b, Q5 and Q9;
  - built, as G29 rules: Q2, Q3, Q3b, Q6A, Q6B and Q7, and the Q8 control.
- **10 mutants of the c2v005 changes (`mutate_c2v005.py`), 9 killed** (RUNBOOK §8 lists each with its killing cases).
  - The survivor is the c2v004 first-owner form of the content loop. It is equivalent under c2v005: a call's result precedes its cut record in the file list, and only FINISHED results carry the content rule, so no pair can hide behind a first owner.
  - c2v004's 8 mutants and c2v003's 18 were not re-run.

## Classifier A's records

Unchanged from c2v003 and c2v004. See RUNBOOK §6b and the builder constant `A_INPUTS_NOT_PRODUCED`. OI-A1 to OI-A3 stay open for Claude4.

## CHOICES this build made that the text did not force (root confirms or replaces each)

C1–C40 are carried from c2v004, with C38 now confirmed by root and its scope narrowed by G29 (cut records are no longer content-unique).

- **C41. "Its own registered run directory"** is the terminal attempt's run directory, the directory c2v001–c2v004 already required for the result and the cut record. A cut record inside a non-terminal attempt's run directory of its own call still refuses `CUT_RECORD_NOT_OF_ITS_CALL`.
- **C42. "Any other call's" run directory** means every attempt's run directory of every other call of the build input, roster or OTHER. A roster call is (alternative, exact theta), so a MEMBER and a SENSITIVITY record at one theta are one call.
- **C43. Results keep c2v004's residence rule only:** inside the terminal run directory. The ruling states the "not inside any other call's" clause for cut records. Its extension to results is not made; see the NOTE below.
- **C44. Order and codes.** The checks run in this order:
  1. receipts across calls (R2);
  2. run files by realpath, then file identity;
  3. C38 content;
  4. cut-record residence.

  The new code is `CUT_RECORD_IN_OTHER_CALL_RUN_DIR`. Roster calls are taken in (alternative, theta sha256) order, so the outcome does not depend on the order of the calls in the input.
- **C45. OTHER calls' run files are their receipts.** No input schema changed, so `other_phase_calls` still has no result or cut record field.

## Gaps

**G29 is ruled.** The ruling is implemented above. Its item (4), a file from outside the build input's calls or a copy written by hand into the call's own run directory, stays undetectable without a binding key in the cut record; root decides whether that producer change is wanted.

Root rulings still needed are those carried from c2v004: G1, G2 residual, G3, G7, G8, G9, G10, G13–G21 and G24–G28.

## UNTESTED (deciding tests in RUNBOOK §8)

As in c2v004, with these changes:
- The question "do real cut records of distinct calls differ in bytes" is gone: it no longer matters.
- **New: the production run layout under residence.** Every attempt must have its own run directory, and no call's run directory may lie inside another call's. The deciding test is the first real MEMBERS or FULL build.
- **Still open:** whether real FINISHED results of distinct calls always differ from every other call's cut record and result (C38), and the file identity on the production run root's file system.

## NOTEs (not blocking under A115, recorded)

- **Results inside another call's run directory (C43).** c2v005 does not refuse a result, for example a byte-identical failure record, that lies inside its own terminal run directory when that directory is nested in another call's. Only cut records carry the "no other call's run directory" rule, as ruled. No honest layout nests run directories. If root wants the rule for results too, it is one more check of the same kind.
- **A157 and the gate-status list, carried from c2v004.** V006 A157 pins 15 M-15 gate documents. The builder's list covers only `gate_documents`, which must be REGISTERED_INVALID_ROW_GATE_CX3V001 documents. A production FULL build would therefore write `{"gates": []}`. Root and Claude4 confirm which set classifier A's `gate_status_list` must carry.
- **Carried from c2v003.** A rebuild under a different ledger root gets its own ledger (a V006 event under G28). Deleting the last ledger entry is not detectable by the tool.

## Deviations (disclosed)

- **Drafts in the scratchpad.** The builder, tests, runbook and README were drafted in `/private/tmp/claude-501/-Users-bgm-MB-Work/04dac55c-b963-46a5-9ea4-74afb63af51b/scratchpad/rbv005c2/`. The development runs, the run against the c2v004 bytes, the probe rerun and the mutation check also ran there. Each published file was written once, by exclusive create, from those bytes. The directory `test_records_c2v005/` is new. No existing file in this folder was edited.
- **Beyond the rulings' letter:**
  - J12 (residence against a non-terminal attempt's run directory) and J11 (a test for the existing `RESULT_NOT_OF_ITS_CALL`, which no earlier case covered);
  - the all-pairs C38 loop (equivalent in outcome; C44);
  - id suffixes of H02 and H06 changed with their expectations.
- **Hard links in the record runs** are made with `os.link` inside each run's work directory only.
- **Opened:**
  - the c2v004 README, RUNBOOK, builder, tests, HASHES_V004 and the c2v004 test record;
  - the c2v004 re-verify probe scripts and their outputs in the scratchpad (`rb4verify/`: Q1–Q9);
  - V006 (`96489e9f`, through A160), by its heading list, lines 1-516 and a keyword grep. It has no G29 entry; the rulings implemented here are root's, as dispatched to this build.
  - The suite reads the compare, N1 and node records that the TSR records pin, from bytes.
- **Not opened:**
  - `classifier_a_c4v001.py` and classifier A's README;
  - the slots, the program query manifest and the A133 text;
  - run trees, `/Volumes/External1`, ~/.codex, `c5h_hull_c2/` and `UVT_*`;
  - anything under `v003g/slots`, `runs` or `independent235`;
  - any NGC3198 target, observed or slots file.
