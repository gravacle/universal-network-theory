# REVIEW_V007_COMPARE_R13_C3V001 — Claude3 delta review of compare r13 (A102; 0632)

`date -u`: 2026-10-18T22:09:22Z.

**Object:**
- kmax_tail_compare_c2v007_r13_cx3v001.py `f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157`, selected by SELECTED_R13_CX3V001 `10acd098…`;
- HASHES_R13_CX3V001.json `d4509325…`; FIELDS_R13 `7b116b01…`; tests `71c7b516…`, module `cmp7r12`.

The base is r12 `4bd7b262…`.

## Verdict: PASS_WITH_FINDINGS. 0 BLOCKING, 2 SHOULD_FIX, notes listed below

## How it was run
The workflow `wf_8056bcc9-a65` (ultracode) ran three refute-by-default lenses: AB1 regression, SCOPE and NEWCODE. Every SHOULD_FIX went to its own adversarial verifier (3). The lead also ran its own L probes. Every exec of the compare went through `r12_loader_c3.py` (`2ef8bc5f…`), with r12 and r13 always in separate processes. **The guard refused 0 in every run** across all lenses, verifiers and lead runs. Nothing was launched, no protected path was touched, and the author's cli()-child suite was not run. All 91 files the helpers claimed, I re-hashed: none differ.

## Confirmed (TESTED)
- **A-B1 is closed.** V01–V07 now REFUSE on every leg: check_record_codes, driver_build_codes r5/r6, activate_driver_build r5/r6, in-process main in all three CLI modes, and the seal-time built-in path. On r12 the same forms are admitted on 113 of 113 legs. The lead's own reproduction agrees: the 4301-digit duplicate refuses with both positions named.
- **Scope.** The r12 → r13 diff is one hunk, L875-881. 439 of 440 top-level AST nodes are identical; the only change is check_record_codes. HASHES 202/202 and SELECTED 6/6 match.
- **Regression.** These read exactly as on r12:
  - helper A's v4 suite ported to r13 (99 check-record probes, 489 leg calls, 27 CLI rows, 75 NPY rows that differ only in zip timestamps, and the x-path entries);
  - the T01–T19 text controls, G01 and the real r5 CHECK.md (89a6de88).
  
  The lead's L probes, 58/58 and 14/14, give result bytes **identical to r12's** (`c52a94b9…` and `929f413e…`).
- **New branches.** The only exception json.loads(bytes, …, parse_int=str) can raise that is a ValueError but not a JSONDecodeError is UnicodeDecodeError (118-fixture audit; 3000 fuzz records). The L878-879 NEW-73 fallback remains the only admitting JSON-parse site in the file. Blinded output is clean.
- **Registry.** V009 on r13, against the case block of record: all 13 registered records PASS (`VALIDATE_R13_C3V009_CASEBLOCK_OF_RECORD.json` `f14dd9a6…`).

## SHOULD_FIX
1. **R13-SF1, the A102 item-3 tests are missing.** A102 says "V01–V07 become MUST_FAIL tests", but the selected author suite adds 0 tests. As shipped it cannot tell the defective r12 from the fixed r13.
   - Lenses: SCOPE-SF1 and NC-N7. The verifier reproduced it.
   - Fix: add V01–V07 (and the controls) as MUST_FAIL tests in a successor suite. The source needs no change.
2. **R13-SF2, the documentation of undecodable text records.** UnicodeDecodeError, which json.loads(bytes) raises before parsing, now falls under the new `except ValueError` and gives DRIVER_BUILD_CHECK_RECORD_UNREADABLE.
   - Text check records that are not decodable under json's encoding detection used to receive the NEW-73 lexical test on r12. They now refuse; examples are Latin-1 or cp1252 text, a stray 0xff, and NUL-led bytes.
   - The behaviour follows A102 word for word ("any other ValueError refuses with a typed code"), it fails closed, and no registered record is affected (the real CHECK.md is strict UTF-8).
   - **But FIELDS_R13 L113**, inherited from r12, still says "Legitimate text-format PASS controls retain NEW-73 behavior". That is now inaccurate for this class.
   - **Fix: option (a).** Document in FIELDS that check records must decode as JSON-detected text, and that undecodable ones refuse with UNREADABLE.
   - **Do NOT take option (b),** catching UnicodeDecodeError into the text fallback. The SCOPE verifier showed it would reopen a second A-B1-class admission that r12 had: a duplicate-key JSON record with an invalid UTF-8 byte reached the text fallback and was admitted (SCOPE-N2). r13 closes it.
   - Lenses: AB1-S1, SCOPE-SF2 and NC-N1. The verifiers split: AB1-S1's kept SHOULD_FIX, and SCOPE-SF2's ruled NOTE. I set SHOULD_FIX for the documentation only.

## NOTES (highlighted)
- **SCOPE-N1:** FIELDS_R13 (7b116b01) cannot be regenerated from the selected source.
  - r13's `--write-field-contract` emits 5cc95a06, which is r12's FIELDS under r12's header. FIELDS_R13 is a 25-line A102 preamble followed by those bytes verbatim.
  - The byte-for-byte regeneration test was re-pointed at r12's file.
  - This is consistent with "nothing else changes", and the content is accurate apart from R13-SF2. But SELECTED_R13 names a field contract that the source does not generate.
- **SCOPE-N2:** r12 had the second admission class described under R13-SF2. r13 closes it, though without naming both positions.
- **SCOPE-N3:** the r13 suite loads its fixture producers from r12/tools/fixture_producers by absolute path, and HASHES_R13 does not pin those 29 files.
- **AB1-N3 and SCOPE-N5:** the other strict-parse sites fail closed but drop the both-position naming when a long integer precedes the close. Pre-existing.
- **NC-N3:** RecursionError escapes, as on r12. Pre-existing.
- **NC-N5 and SCOPE-N6:** malformed near-JSON still takes the NEW-73 fallback. This is the registered policy.
- **AB1-N5, SCOPE-N7 and NC-N6:** "unreadable" is spelled two ways. Cosmetic.
- **AB1-N1 and AB1-N2:** harness-instrumentation and zip-timestamp artifacts, not behaviour.
- **AB1-N6:** helper process disclosure. The lens edited its own unrun script once; it is superseded and kept.

## Evidence
- **Lens AB1** (`AB1_regression/`): `HASHES_AB1_R13.txt` `13e1da5417372479…` (full sha in the hashes file); RESULTS_A_r13 `92e1fd36…`; the port diff `056c5f0d…`.
- **Lens SCOPE** (`scope/`): `HASHES_VERIFY_C3H_v001.json` `124d456a…`; AST_SCOPE `c79f3c2f…`; FIELDS regenerations (5cc95a06).
- **Lens NEWCODE** (`newcode/`): `HASHES_NEWCODE_R13_001.txt` `524ac17a…`; CMP_NEWCODE_003 `b67d744e…`.
- **Verifiers** (`verify/`): AB1-S1 `verify_ab1s1_c3v002.py` `c3092505…`; SCOPE-SF1 `verify_scope_sf1_c3v001.py` `7de32334…`; SCOPE-SF2 `probe_sf2_c3v001.py` `93c58574…`.
- **Lead** (`c3/`): r13_probes `e24281d1…`, r13_driver_build_probes `ea13784d…`, r13_verify_ab1 `882fa59a…` (output R13_VERIFY_AB1 `90289dbc…`).
