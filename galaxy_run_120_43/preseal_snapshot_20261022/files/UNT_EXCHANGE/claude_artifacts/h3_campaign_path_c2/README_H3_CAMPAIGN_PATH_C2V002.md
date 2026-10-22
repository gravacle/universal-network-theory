# H3 campaign launch path, c2v002 (V006 A191 B2 and B1): delta to README C2V001

Claude2 for root. Stamp (`date -u` before writing): Tue Oct 20 02:22:24 UTC 2026 (Mon 21:22 CDT).

Nothing real was launched. The only runs used the SYNTHETIC mock driver under the real root monitor, in `test_runs_c2v002/` and `dev_runs_c2v002/`. No run tree was opened and no NGC3198 file was opened. From V006 (`b1c63b6f`), only A143, A147, A158 and A191 were read. Labels: TESTED (ran), FORMAL (from code), UNTESTED (forecast or not run).

**What this supersedes in README C2V001 (`6d2b4ee2`):** the §1 rows for the entry, generator, regenerate, acceptance step, placeholder chain and tests; the §3 V2 and V6 commands; §5 step 6; §6 Plan items 1-2 (superseded by `STORAGE_PLAN_ERRATUM_C2V001.md`); §8; and §9. Everything else holds as written.

**Unchanged and reused by path:** the apply tool, the adoption derivation builder, the storage check, the three record templates and the synthetic modules. The builder takes any entry by `--entry` and its sha, and it only loads the wrapper, so the c2v002 entry needs no builder successor (FORMAL, `build_adoption_derivation_c2v001` L46-51).

## 1. B2: reingest needs the handoff's record (TESTED)

`h3_campaign_entry_c2v002.py` (`75b4cafa`) is c2v001 plus `--acceptance-record PATH --acceptance-record-sha256 H` on `reingest`. Every check below runs before the wrapper is called, and every refusal exits 3.

1. `--bundle` and `--acceptance-record` are absolute paths.
2. The gates pass, and the wave plan has this config and gate digest and holds the call index. The bundle verifies from its bytes.
3. The record's bytes hash to its sha.
4. The record is the adopted handoff's: schema `DDO154_TAIL_ACCEPTANCE_RECORD_C2V001`, and handoff = {acceptance_q2 v004 path, `5ff464cc`}.
5. The record reads ACCEPTED or ACCEPTED_PASS_FLAGGED, with `outputs_are_evidence` true, guard ok, and `step4_stop_for_root_ruling` false.
6. `record.call_dir` is this call's directory, resolved.
7. **The same receipt.** v004's record pins the result, not the receipt: v004 checks `policy.receipt` against the result (L253-257, L370) and records `result` (L368-369) (FORMAL). So the call's `RECEIPT.json` must verify with the pinned monitor for the planned spec and the config driver, read FINISHED/COMPLETED, and pin the same result that `record.result` pins.
8. `record.bundle` equals `{--bundle, --bundle-sha256}` exactly.

In process, `reingest(..., acceptance_ref=None)` refuses `REINGEST_ACCEPTANCE_RECORD_REQUIRED`. On the CLI both new flags are required, so argparse exits 2 without them.

**Residual (FORMAL).** These are content checks on a byte-pinned record. A record written by hand with these fields would pass. Its custody is root's: the records dir is under `claude_artifacts`, created new, with exclusive-create files (v004 Store L205-242).

**Successors that embed the entry:**
- `h3_accept_call_c2v002.py` (`c9058dd5`) passes its own record pin to `reingest`. It refuses a c2v001-line entry before the wrapper loads (`ENTRY_NOT_C2V002_LINE`), and its step record schema is `..._C2V002`.
- `make_campaign_cascade_c2v002.py` (`bbb9d656`) pins the c2v002 entry template. Its policy, core and wrapper outputs are c2v001's, byte for byte (G08).
- `regenerate_h3_c2v002.py` (`0fc614f5`) pins that generator. The seal tuple record schema and every refusal rule are unchanged.

**Placeholder chain** `placeholder_chain_c2v002/v006r12_c4/`: policy `93d9c0ac`, core `192d0863` and wrapper `7ac07851` are the same as c2v001's. The entry is `b6aada8e`. **Do not publish it.**

## 2. Commands that change (README C2V001 §3)

**V2.** Use `regenerate_h3_c2v002.py` in place of `regenerate_h3_c2v001.py` in both `fill` and `build`. The arguments are unchanged.
- The `diff -u` loop compares against `$H3/placeholder_chain_c2v002/v006r12_c4/`.
- `ENTRY` is `$R/chain/v006r12_c4/h3_campaign_entry_cx2v006r12_c4.py`, as before.

**V6.**
```
cd /tmp && $PY -I -B $H3/h3_accept_call_c2v002.py --entry "$ENTRY" --entry-sha256 $ENTRY_SHA --config "$CFG" \
    --wave 1 --call-index 0 --deps "$DEPS" --deps-sha256 $(shasum -a 256 "$DEPS" | cut -c1-64) \
    --records-dir "$ART/campaign_acceptance_records_c2/W0001_C0000_A01"
```
The exit codes are unchanged: 0, 3, 8 and 13. Root needs a manual reingest only if the step's reingest returned LOCKED. In that case, use the record and bundle that the step printed:
```
cd /tmp && $PY -I -B "$ENTRY" reingest --config "$CFG" --wave W --call-index I --bundle <abs POST_STATE_BUNDLE.json> \
    --bundle-sha256 <sha> --acceptance-record <abs ACCEPTANCE_RECORD.json> --acceptance-record-sha256 <sha>
```

## 3. B1: storage

See `STORAGE_PLAN_ERRATUM_C2V001.md`. In short, with HEADLINE11 + S0 ×4 at 370.5 GiB:
- **At the measured 16.24 GiB per call, both volumes hold the program with 74.1 GiB to spare.** That needs HEADLINE11/S0 on the internal disk and 508.3-582.4 GiB moved off External1 before wave 15.
- **At the 57.19 GiB projection they do not.** The campaign volume needs 7,043.0 GiB, against External1's 3,725.8 GiB.
- The break-even is 17.08 GiB per call. W1's measured output decides which case holds.

## 4. Tests (TESTED)

`tests/test_h3_campaign_path_c2v002.py` (`6705c949`) is the c2v001 suite ported, plus the B2 rows. It ran twice from this folder, 94/94 each time: 45 MUST_PASS, 49 MUST_FAIL, 0 audit denials, 36 children, only the pinned python started. The rows are identical across the two runs.
- `test_runs_c2v002/RUN_20261020T022025Z_60511`: TEST_RESULTS `28e11397a1c58b7a3306912ce436c937a68407d90ef325c8668c09d09b506167`.
- `test_runs_c2v002/RUN_20261020T022053Z_61639`: TEST_RESULTS `76c2925caae62939ca5796e508a76bfb537645b048bbbdd443abd4810022fbbe`.

**New and changed rows:**
- **G08:** generator c2v002 equals c2v001 except the entry, for SUB r10_c4 and r12_c4.
- **K06:** the entry CLI with the new flags still refuses on the gates first.
- **K15:** the acceptance step refuses a c2v001-line entry, and nothing is written.
- **EB07:** the wrong-producer bundle now runs through the c2v001 function, to keep the wrapper's own refusal in the suite.
- **EB10:** the step record is `_C2V002`. Reingest gets the record and caches the call VALID.
- **EB17 (MUST_FAIL):** a guard-valid post-state bundle built without the handoff, on wave-2 call 1, with no record. The CLI exits 2; in process it refuses `ACCEPTANCE_RECORD_REQUIRED`.
- **EB18 (MUST_FAIL):** W1's ACCEPTED record offered for wave-2 call 1 refuses `OTHER_CALL` and `OTHER_RECEIPT`, with either bundle.
- **EB18C (contrast, B2 as found):** the c2v001 entry caches that handoff-less bundle VALID.
- **EB19:** the handoff alone reads ACCEPTED for wave-2 call 0. This uses the declared stub for the step's reingest, so the call stays uncached.
- **EB20 (MUST_FAIL):** a record reading INCOMPLETE refuses `NOT_ACCEPTED` as the only reason. The genuine EB09 INCOMPLETE record refuses as well, and W1's acceptance file is unchanged.
- **EB21 (MUST_FAIL):** a relative `--bundle` or a relative `--acceptance-record` refuses.
- **EB22 (MUST_FAIL):** a record whose sha does not match its bytes refuses, and so does a bundle other than the record's.
- **EB23 (MUST_PASS):** the CLI reingest with the call's own record and bundle caches it VALID, giving n_cached 3.
- **EC03:** reingest of the non-finished call now refuses `RECEIPT_NOT_FINISHED`.

**Declared substitution added (TOY_SEPARATION):** in EB19 the acceptance step's `E.reingest` is replaced by a stub that returns `TEST_STUB_REINGEST_NOT_CALLED`. Everything else is c2v001's declared synthetic world.

## 5. Files

`HASHES_H3_CAMPAIGN_PATH_C2V002.txt` lists every file this task added (sha256 from bytes), except itself.

| file | sha256 |
|---|---|
| h3_campaign_entry_c2v002.py | 75b4cafa8563e31879ab1d70a74fe64dba9f4d61f496c3bc28479668c1e61c10 |
| h3_accept_call_c2v002.py | c9058dd5b2868b40660d9b39103939a9b5fad9967fa70bcacd6f19af16d9b89f |
| make_campaign_cascade_c2v002.py | bbb9d6568894f615ab798003ddd285defed10c5ef9dc95d4dd5444f55ac1ab28 |
| regenerate_h3_c2v002.py | 0fc614f5a1fe7a7c8fc5bba9aa3cf783888dc1b00c3cddd14f2a1bc7625ca1f1 |
| tests/test_h3_campaign_path_c2v002.py | 6705c949b504aac4cfd994710c0beea8abd2775ef347ede2dff986035f2caa1d |
| placeholder_chain_c2v002/v006r12_c4/h3_campaign_entry_cx2v006r12_c4.py | b6aada8e3bdaade21674a66bcfc333f59350ed11c8c14068e7294b5b19bcd0ac |
| STORAGE_PLAN_ERRATUM_C2V001.md | 5ce908d0e3eb732a4ea07d9a8a24ecf7557b0d62321f3003c202776505c6eb3c |
| DIFF_h3_campaign_entry_c2v001__c2v002.diff | 691cbd48f59bbbaadd5679f059974ef7620d2f53346bdf542c2704487e638923 |
| DIFF_h3_accept_call_c2v001__c2v002.diff | cc92ab86c8f8197112b65922ba435c6b64b4c481382dd29fa700fc6305d5bded |
| DIFF_make_campaign_cascade_c2v001__c2v002.diff | 3e50ff70e7404cafd4d7ea2710ab0d83b8757ff99c1b9c79b68737b92858da78 |
| DIFF_regenerate_h3_c2v001__c2v002.diff | 4d63eb3ebbf6d10cd5edf0ef3d0e82278fc0e10942c6b1840138b0adef90fb37 |
| DIFF_test_h3_campaign_path_c2v001__c2v002.diff | b17414b7b0e2d196ea37086898942d739d0a8967a7c96227938056ba2bfb04c9 |
| DIFF_placeholder_chain_entry_c2v001__c2v002.diff | c9e311f99b8930bade9e6a95acb7a7ab2b10270eb374c1c2b116945984a6ad57 |

**Ten empty files, not artifacts.** A shell quoting error at 02:21Z created ten 0-byte files in this folder. Their sha256 is `e3b0c442…`. They were left in place, because no file is deleted here, and root may remove them:
- `DIFF_h3_accept_call_c2v001.py`
- `DIFF_h3_campaign_entry_c2v001.py`
- `DIFF_make_campaign_cascade_c2v001.py`
- `DIFF_regenerate_h3_c2v001.py`
- `DIFF_placeholder_entry_c2v001__c2v002.diff`
- `DIFF_test_h3_campaign_path_c2v002__.py.diff`
- `h3_accept_call_c2v002__.py.diff`
- `h3_campaign_entry_c2v002__.py.diff`
- `make_campaign_cascade_c2v002__.py.diff`
- `regenerate_h3_c2v002__.py.diff`

The real diffs are the `DIFF_*__c2v002.diff` files listed above.
