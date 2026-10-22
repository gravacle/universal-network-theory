# Campaign certification build c2v004: verifier B1 fix (ADV rows C03, C04; V006 A192 item 3)

Claude2 for root. Stamp (`date -u` before writing): Tue Oct 20 04:08:34 UTC 2026 (Mon 23:08 CDT). It proposes; root rules.

This is a delta on README_CAMPAIGN_CERT_C2V001.md (build c2v003). Nothing real was launched. No running process, run tree or NGC3198 file was touched, and no existing file was edited. No physics value, threshold or reading changed. Labels: TESTED (ran), FORMAL (from code), UNTESTED.

**The defect (verifier evidence `adv_verify_runs_c2v003/ADV_20261020T034243Z_81516/ADV_RESULTS.json`):**
- C03: a call whose first pass read ACCEPTED (not yet cached) got a second pass reading NON_LAPSE and was certified MODEL_INVALID.
- C04: a second pass after a NON_LAPSE first pass ran, read ACCEPTED, and cached VALID.

c2v003 counted passes but never checked the first pass's reading. A192 item 3 allows a rerun only after INCOMPLETE and freezes failure readings.

## 1. Files (all new, exclusive create)

| file | sha256 | against |
|---|---|---|
| `h3_accept_call_c2v004.py` | `eb895263…` | c2v003 `ae5ab4a6` |
| `calibration_orchestrator_q5b1_ledger_c2v004.py` (wrapper source) | `7c9b4248…` | c2v003 `5ea1780a` |
| `h3_campaign_entry_c2v004.py` | `cbdf0d49…` | c2v003 `5710e1fa` |
| `make_campaign_cascade_c2v004.py` | `5014b04f…` | c2v003 `d7e6d77a` |
| `regenerate_h3_c2v004.py` | `ad5cee08…` | c2v003 `1a17239d` |
| `tests/test_campaign_cert_c2v004.py` | `52d04202…` | c2v003 `6fd12500` |
| `placeholder_chain_c2v004/v006r12_c4/` | policy `93d9c0ac`, core `192d0863` (both equal to c2v003's), wrapper `381fa295`, entry `dd9c951b` | **Do not publish.** |

Review diffs: `DIFF_{calibration_orchestrator_q5b1_ledger,h3_campaign_entry,h3_accept_call,make_campaign_cascade,regenerate_h3,test_campaign_cert}_c2v003__c2v004.diff` and `DIFF_placeholder_chain_{wrapper,entry}_c2v003__c2v004.diff`.

## 2. Rules (FORMAL; TESTED in section 4)

- **Pass.** A pass is one `ACCEPTANCE_TAILSTATES_C2V002_A<nnn>` directory made by handoff v004, which takes the first free number. The wrapper's `acceptance_passes` lists A001..A<n> oldest first. It refuses on a gap, or on any other `ACCEPTANCE_TAILSTATES_*` entry (another name, or a file instead of a directory), because the highest number is the newest only when there are no gaps. A record is **of the latest pass** when its `tailstate_dir` is A<n> of its own call dir.
- **Acceptance step (item 1).**
  - With one pass in the call dir, the step refuses unless root pins that pass's record with `--first-pass-record ABS --first-pass-record-sha256 H`. The record must be the A158 handoff's record of this call dir and of that pass, and it must read INCOMPLETE. Otherwise it refuses with `ACCEPTANCE_RERUN_FIRST_PASS_RECORD_REQUIRED` or `ACCEPTANCE_RERUN_NOT_AFTER_INCOMPLETE` (`FIRST_PASS_READING_STANDS`, `_OTHER_CALL`, `_NOT_THE_FIRST_PASS`, sha mismatch). Nothing is written.
  - With two passes it refuses with `ACCEPTANCE_RERUN_LIMIT`.
  - A pin given when no pass exists refuses.
  - The pass list is read again under the work-dir lock (`ACCEPTANCE_PASSES_CHANGED`).
  - An INCOMPLETE second pass gets `f6_action` HALT.
  - The step record (schema `..._C2V004`) adds `acceptance_passes_after`, `acceptance_pass` and `first_pass_record`.
- **Wrapper (item 2).** `reingest_invalid` refuses when the call dir holds `TAIL_CERTIFICATE_ACCEPTANCE.json` (`TAIL_INVALID_CALL_HOLDS_TAIL_CERTIFICATE_ACCEPTANCE`) or when the record is not of the latest pass (`TAIL_INVALID_RECORD_NOT_THE_LATEST_PASS`). Both checks are part of `tail_invalid_problems`, so they are also re-checked at every put, open and reuse of the cache entry.
- **VALID reingest.** It now takes the record: `reingest(..., acceptance_ref)`, the one extra q5b1 line replaced. Under the work-dir lock, before `write_acceptance`, it refuses a record that is not of the latest pass (`REINGEST_RECORD_NOT_THE_LATEST_PASS`). The entry passes on its `--acceptance-record`, and the step passes on the record of the pass it just ran.
- **Item 3.** The entry, generator and regenerate successors re-pin. The generator's policy and core outputs are byte-equal to c2v003's.

## 3. Root steps (changes only)

- **V1/V2:** use `regenerate_h3_c2v004.py` in place of c2v003 (same arguments), then diff against `$H3/placeholder_chain_c2v004/v006r12_c4/`.
- **V6:** use `h3_accept_call_c2v004.py` with c2v003's arguments. After an INCOMPLETE first pass (`f6_action` RERUN…), rerun it once with a new `--records-dir`, adding `--first-pass-record <that ACCEPTANCE_RECORD.json> --first-pass-record-sha256 <sha>`.
- **Reingest:** `reingest` and `reingest-invalid` take the record of the call's **latest** pass. The commands are unchanged.

## 4. Tests (TESTED)

`tests/test_campaign_cert_c2v004.py` ran twice from H3. Each run passed **90/90**: 58 MUST_PASS, 31 MUST_FAIL and 1 INFO.
- Audit: 0 denials. Only the pinned python was started (89×), across 65 children.
- Rows were identical across the two runs. Wave 3 had 3 calls and wave 4 had 2.
- `test_runs_c2v004/RUN_20261020T040626Z_44162`: TEST_RESULTS `03b5943dcb59565f6e6fcbf4e327d81ae1ab145a5a1ffd2d45b13b752accaac7`.
- `test_runs_c2v004/RUN_20261020T040714Z_45619`: TEST_RESULTS `324e770505340edda5979f49b61e566a7b32388fa9ecd6c6beeabb3418d32300`.
- Stdouts: `TEST_STDOUT_RUN1.txt` (`63194d7c…`) and `_RUN2.txt` (`6845267c…`).

All 77 c2v003 rows are ported. EB14's meaning changed: c2v003 let a second pass after a NON_LAPSE first pass run. New or changed rows:
- **EB14 (C04, MUST_FAIL):** after a NON_LAPSE first pass, a second pass refuses both without a pin (FIRST_PASS_RECORD_REQUIRED) and with the NON_LAPSE record pinned and good deps, as in the verifier (READING_STANDS). Nothing is written, there is still one pass, and nothing is cached.
- **EB26 (MUST_FAIL):** the rerun after INCOMPLETE refuses with no pin, with another call's record, or with a sha mismatch.
- **EB27 (MUST_PASS):** with the call's own INCOMPLETE record pinned, pass 2 runs (ACCEPTED). EB21 then caches it VALID from the latest pass.
- **EB28 (MUST_FAIL, third pass):** refuses with ACCEPTANCE_RERUN_LIMIT, even with the pin.
- **EB29a-c:** wave 4 is certified through the CP-1 list successor and the ledger, then run (2 calls).
- **EB30 (C03, MUST_FAIL, rerun after ACCEPTED):** after a first pass read ACCEPTED and was not cached, a second pass refuses both without a pin and with the ACCEPTED record pinned.
- **EB31 (C03, MUST_FAIL):** `reingest_invalid` refuses a NON_LAPSE record of the latest pass while `TAIL_CERTIFICATE_ACCEPTANCE.json` is present.
- **EB32 / EB33 (MUST_FAIL, stale records):** a VALID reingest with the first pass's ACCEPTED record refuses, and so does `reingest_invalid` with the first pass's NON_LAPSE record, once a later pass exists.
- **U01 (MUST_FAIL):** the pass rule refuses a gap, a missing A001, another `ACCEPTANCE_TAILSTATES_*` name, and a file with the handoff's name.
- **G05/G06:** seven q5b1 lines are replaced (c2v003's six plus the reingest signature). Against c2v003, the wrapper replaces exactly that one line. The entry changes exactly its first docstring line, WRAPPER, WRAPPER_SHA, ENTRY_NAME and the reingest call.
- **K04:** the step refuses a c2v003-line entry.
- **G03:** the generator matches c2v003 for policy and core.

**Declared substitutions (TOY_SEPARATION), added to c2v003's:**
- EB31 writes `TAIL_CERTIFICATE_ACCEPTANCE.json` in process with the wrapper's own `write_acceptance`. This stands for a VALID reingest that stopped before its cache put.
- EB31 and EB33-EB34 make a second pass by calling handoff v004 directly, in process, outside the step.

`dev_runs_c2v004/` holds 2 development runs of a staged copy in scratch: 84/85 and 85/86. In both, the only failure was the G block, because the staged copy of the c2v003 generator looks for its template in its own folder. A harness then ran G01-G06 and R01 with G03 pointing at the H3 generator: 7/7. The H3 runs above have no such substitution.

## 5. Open items for root

1. **Residual R1 (TESTED, EB34 INFO):** a second pass made by **calling the handoff directly, outside the step**, is not seen as a rerun. After a NON_LAPSE first pass, a direct pass reading ACCEPTED was cached VALID through the B2 reingest (rc 0). The wrapper sees only the latest pass, so the rerun rule holds only while campaign calls go through the step.
   - Next step (not built; it is outside this spec and changes root's commands): both reingest paths would require `--first-pass-record` when the record is of pass A002. They would check that it reads INCOMPLETE, and keep it in the MODEL_INVALID provenance so it is re-checked at every open.
   - Until then, root runs the handoff on campaign calls only through `h3_accept_call_c2v004`.
2. The entry's record-content checks (ACCEPTED, this call, receipt, bundle) still run before the lock, as in c2v003. The records are sha-pinned. The latest-pass check runs under the lock.
3. An attempt that refuses before its state export makes no pass directory and does not count (c2v003 item 6). `f6_action` says so.
4. c2v003 README §5 items 1-5 and 7 stand unchanged.

## 6. Files

`HASHES_CAMPAIGN_CERT_C2V004.txt` lists every file this build added, with sha256 computed from the bytes. It includes this README and leaves out only itself.
