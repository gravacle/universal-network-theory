# Campaign certification build c2v003 (V006 A192 "Commissioned"): ledger, F6, CP-1 list, HEADLINE11 evidence, storage

Claude2 for root. Stamp (`date -u` before writing): Tue Oct 20 03:25:40 UTC 2026 (Mon 22:25 CDT). It proposes; root rules.

Nothing real was launched. The only runs used the SYNTHETIC mock driver under the real root monitor, in `test_runs_c2v003/` and `dev_runs_c2v003/`. No run tree, `cp1_run_*` folder, step-2 tree or NGC3198 file was opened; no running process was touched. From V006 only A122, A134, A146, A158, A188, A191 and A192 were read. Labels: TESTED (ran), FORMAL (from code), UNTESTED (forecast or not run). No physics value, threshold or reading changed.

```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ART=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts;  H3=$ART/h3_campaign_path_c2;  CX2=$ART/calib_tail_readiness_cx2
R="<root's H3_AT_VERDICT folder>";  ENTRY="$R/chain/v006r12_c4/h3_campaign_entry_cx2v006r12_c4.py";  CFG="<the W1 config>"
```

## 1. What was built (all new files; nothing existing was edited)

| A192 item | file | sha256 | what |
|---|---|---|---|
| 2, 3 | `calibration_orchestrator_q5b1_ledger_c2v003.py` | `5ea1780a…` | **Wrapper source** for the verdict regeneration: q5b1 `7a6af535` with exactly six q5b1 lines replaced (two lookups, the review binding, the put check) plus two marked blocks. Core untouched. |
| 2, 3 | `h3_campaign_entry_c2v003.py` | `5710e1fa…` | Entry template: c2v002 + `reingest-invalid`, `points-manifest`, `ledger-append`, `ledger-status`. `reingest` (B2) unchanged in behaviour. |
| 2, 3 | `h3_accept_call_c2v003.py` | `ae5ab4a6…` | Acceptance step: the one lookup, the rerun limit, `f6_action` in the step record. |
| 2, 3 | `make_campaign_cascade_c2v003.py` | `d7e6d77a…` | Generator: wrapper source and entry template swapped; policy and core byte-identical to c2v002. |
| 2, 3 | `regenerate_h3_c2v003.py` | `1a17239d…` | Pins that generator; every refusal rule is c2v002's. |
| 2 | `apply_h3_fields_c2v003.py` | `02addc1d…` | Apply c2v001 + one field, `tail_readiness.certificate_ledger`. |
| 2 | `cp1_points_common_c2v001.py`, `cp1_points_runner_c2v001.py`, `cp1_points_assembler_c2v001.py` | `302abdad…`, `3c6a5ba3…`, `951e7203…` | **CP-1 list-of-points successor.** Loads c3v004 runner/common/assembler by path+sha and changes none of their bytes. |
| 4 | `h11_evidence_assembler_c2v001.py` | `2a8df9df…` | HEADLINE11 evidence assembler + the A192 item 4 reuse test (dry). |
| 5 | `storage_check_h3_c2v003.py` | `8eee1f68…` | b = call-dir bytes after acceptance; the threshold recomputation. `move` is c2v001's. |
| tests | `tests/test_campaign_cert_c2v003.py`, `tests/synthetic/syn_h3_c2v003.py`, `tests/synthetic/mock_cp1_c2v003.py` | `6fd12500…`, `6ea2acc9…`, `06fe9b79…` | 77 rows (section 4). |
| chain | `placeholder_chain_c2v003/v006r12_c4/` | policy `93d9c0ac`, core `192d0863`, wrapper `e5aadc02`, entry `4103452c` | Generator output with no tuple. **Do not publish.** Policy and core equal c2v002's. |

Review diffs: `DIFF_q5b1_7a6af535__calibration_orchestrator_q5b1_ledger_c2v003.diff`, `DIFF_h3_campaign_entry_c2v002__c2v003.diff`, `DIFF_h3_accept_call_c2v002__c2v003.diff`, `DIFF_make_campaign_cascade_c2v002__c2v003.diff`, `DIFF_regenerate_h3_c2v002__c2v003.diff`, `DIFF_apply_h3_fields_c2v001__c2v003.diff`, `DIFF_storage_check_h3_c2v001__c2v003.diff`, `DIFF_syn_h3_c2v001__c2v003.diff`, `DIFF_placeholder_chain_{wrapper,entry}_c2v002__c2v003.diff`.

## 2. How each piece works (FORMAL; TESTED in section 4)

**R-C8 ledger (wrapper block L1).**
- Config: `tail_readiness.certificate_ledger = {"schema": "DDO154_CERTIFICATE_LEDGER_C2V003", "path": "<work_dir>/CERTIFICATE_LEDGER.jsonl"}`. No head sha, so the cache id, the gate digest and the adoption binding do not move as the ledger grows (EA11). `certificate_registry` stays the genesis (CP-1's 31-point registry). The policy review must carry `certificate_ledger` equal to that object.
- One lookup, `Context.certificate_record` = genesis, then append-time candidates, then ledger. Used by the re-patched mapper, `certificate_check`, `write_acceptance` and the c2v003 acceptance step.
- Ledger lines are canonical JSON, hash-chained from a genesis digest of {registry pin, ledger policy}; `seq`, `prev_sha256`, `entry_sha256`. A key already in the genesis or earlier in the ledger is refused. On every read each entry's bundle passes the b1 guard's prelaunch check; at append and at every use the full `prelaunch_check` (the check a genesis record gets) runs with the custody derived from the spec. **Any ledger defect closes the certificate policy gate** (F02).
- `Orchestrator.ledger_append`: gates pass; under the work-dir lock (LOCKED if a run holds it); WORK_DIR.json matches; every item is checked (key = identity digest; theta rebuilds the pending spec; guard; full prelaunch with the candidate) before one append of all lines; re-verified from bytes.

**F6 certified MODEL_INVALID (wrapper block F6; A192 item 3).** `reingest-invalid` caches a call MODEL_INVALID only from the adopted handoff's record of **this** call (call dir, FINISHED receipt and result, registered point, the config's enumerator and the wrapper's guard) reading NON_LAPSE_TAIL_MATERIAL or BOUND_INSUFFICIENT with `rows_are_model_output` false, `outputs_are_evidence` false and no step-4 stop. No forward call. Failure class `TAIL_ACCEPTANCE_<reading>`, source `TAIL_ACCEPTANCE_CERTIFIED`, re-verified from bytes at every put, open and reuse. `resolve --decision invalid` stays disabled. The acceptance step never calls it: it records `f6_action`, and root acts call by call. INCOMPLETE "reruns once": the step refuses a third handoff pass on a call (two `ACCEPTANCE_TAILSTATES_*` dirs).

**CP-1 list-of-points successor.** Without `--points-list` the runner and assembler CLIs **are** the c3v004 CLIs (P01: plan of rows 1-31 identical, runner pin included). With `--points-list L --points-list-sha256 H` the rows come from the entry's `points-manifest` (mapper-built specs with pending slots, rows 100·wave + i) and go into the unchanged c3v004 `run_point`, `adapt_point`, `assemble_bundle`, `verify_point`. The only change is that the scheduler spawns the successor's `worker` with the list pin. The anchor is never a list point, and list points wait for the anchor's AGREE and context **in the same out-root** (c3v004 gates). So a list run continues on CP-1's own out-root (design map 3.3). New: `records` (the wave's ledger records, all list points required, EPS source pins equal across points and to the genesis) and list `verify` (c3v004 offline replica, records as the registry).

**HEADLINE11 evidence assembler.** Input is a root-written manifest of HEADLINE11 #0-#10 (`H3_HEADLINE11_RUNS_C2V001`: index, name, call_dir, spec, receipt, result, acceptance_record). `assemble` checks each run's receipt with the pinned monitor, its finish binding, a COMPLETED/valid result, and an ACCEPTED v004 record of this call (with no step-4 stop on #0), and checks that #2-#10 are the candidate's 9 probe specs, one each. It then writes `DECIDING_EVIDENCE_H11.json` and `CAPABILITY_EVIDENCE_H11.json`, runs the chain's own Context on the candidate plus the five fields (in memory), and writes `H3_DELTA_EVIDENCE_H11.json` only if `deciding_test` and `driver_capability` read ok. `reuse-test` (A192 item 4, dry) runs the entry's `status` under the candidate and compares `driver_capability.normalization[].spec_sha256` with the shas HEADLINE11 ran: REUSE_HEADLINE11 (0), RUN_9_CALLS_AT_THESE_SPEC_SHAS (5), UNDECIDED (3).

**Storage c2v003.** b = max(apparent, allocated) bytes of the call dir after acceptance (TAIL_CERTIFICATE_ACCEPTANCE.json or an `ACCEPTANCE_TAILSTATES_*` dir present), metadata only. The receipt value is shown beside it for comparison. With `--threshold-total-free-bytes F --threshold-other-program-bytes H` it also reports R(b), the binding wave, b* and fits; the erratum's inputs reproduce R = 3,385.8 GiB at wave 15 and b* = 17.08 GiB (S02).

## 3. Root steps (exact commands)

**Reviews first:** Claude4 (after Fri 19:00Z): the wrapper diff, entry, acceptance step, CP-1 list successor, assembler, storage and tests. Codex1: `DIFF_make_campaign_cascade_c2v002__c2v003.diff` (A129).

**V1/V2 at the verdict:** README C2V002 §2 with `regenerate_h3_c2v003.py` in place of c2v002 (`fill` and `build`, same arguments). Diff against `$H3/placeholder_chain_c2v003/v006r12_c4/`. Publish and set `$ENTRY` as before.

**V3 candidate config:** `apply_h3_fields_c2v003.py` in place of c2v001. The `set` also carries
`"tail_readiness.certificate_ledger": {"schema": "DDO154_CERTIFICATE_LEDGER_C2V003", "path": "<work_dir>/CERTIFICATE_LEDGER.jsonl"}`,
and the signed policy review carries the same object as `certificate_ledger`. The genesis is CP-1's 31-point registry.

**HEADLINE11 → evidence** (after #0-#10 FINISHED and each accepted by acceptance_q2 v004; root writes `$R/HEADLINE11_RUNS.json`):
```
RUNS="$R/HEADLINE11_RUNS.json"; CAND="$R/RUN_CONFIG_H3_CANDIDATE.json"
cd /tmp && $PY -I -B $H3/h11_evidence_assembler_c2v001.py reuse-test --entry "$ENTRY" --entry-sha256 $(shasum -a 256 "$ENTRY"|cut -c1-64) \
  --config "$CAND" --config-sha256 $(shasum -a 256 "$CAND"|cut -c1-64) --runs "$RUNS" --runs-sha256 $(shasum -a 256 "$RUNS"|cut -c1-64) --out "$R/H11_REUSE_TEST.json"
cd /tmp && $PY -I -B $H3/h11_evidence_assembler_c2v001.py assemble   <same 12 arguments> --out-dir "$R/H11_EVIDENCE"
cd /tmp && $PY -I -B $H3/apply_h3_fields_c2v003.py "$CAND" "$R/H11_EVIDENCE/H3_DELTA_EVIDENCE_H11.json" "$R/RUN_CONFIG_H3_CANDIDATE_EV.json" \
  "$R/APPLY_REPORT_EV.json" --seal-record "$R/SEAL_TUPLE_RECORD_H3_FILLED.json" --seal-record-sha256 $SEAL_SHA
```
Exit 5 from `reuse-test` means 9 real calls at exactly the listed spec shas are still needed.

**V4-V5:** unchanged (builder with `--entry "$ENTRY"`, then `apply_h3_fields_c2v003` for the adoption delta; launch line with `$ENTRY`).

**V6, each finished call:** `h3_accept_call_c2v003.py` with c2v002's arguments. Exit codes: 0, 3, 8, 13. Then act on the step record's `f6_action`:
- `CERTIFIED_MODEL_INVALID_ELIGIBLE` (NON_LAPSE_TAIL_MATERIAL, BOUND_INSUFFICIENT), root's act:
  `cd /tmp && $PY -I -B "$ENTRY" reingest-invalid --config "$CFG" --wave W --call-index I --acceptance-record <abs ACCEPTANCE_RECORD.json> --acceptance-record-sha256 <sha>`
- `RERUN_ACCEPTANCE_ONCE…` (INCOMPLETE): check the deps, then rerun the step once with a new `--records-dir`. A third pass refuses.
- `HALT_ROOT_RULES_PER_CALL`: root rules.

**Each wave whose points lack a record** (from march0; waves 1-2 are genesis rows 28-31):
```
mkdir -p $ART/campaign_points_c2                                      # once
cd /tmp && $PY -I -B "$ENTRY" points-manifest --config "$CFG" --out-dir $ART/campaign_points_c2/W000K   # prints the POINTS_LIST pin
L=$ART/campaign_points_c2/W000K/POINTS_LIST.json; LS=$(shasum -a 256 $L|cut -c1-64)
cd /tmp && taskpolicy -b $PY -I -B $H3/cp1_points_runner_c2v001.py run --points-list $L --points-list-sha256 $LS \
  --out-root <CP-1's own c3v004 out-root> --operator-lane <lane> [--allow-rho --proof-side-review-pin '<pin>' --proof-side-review-sha256 <sha>] [run sheet gates]
# per point: EPS review instance (A134 Q8 script), then
cd /tmp && taskpolicy -b $PY -I -B $H3/cp1_points_runner_c2v001.py adapt-eps --points-list $L --points-list-sha256 $LS --out-root <same> --point <KEY> \
  --review <review> --approved-review-sha256 <sha> --approved-signer-lane <lane>
# root registers rho attempt a and runs the slot proof (proof side c3v003 cd10cd59), as for rows 1-31; then per point
cd /tmp && $PY -I -B $H3/cp1_points_assembler_c2v001.py bundle --points-list $L --points-list-sha256 $LS --out-root $ART/s4rc1_c3/registry_<name> \
  --point <KEY> --eps-proof <EPS_PROOF> --gq-proof <GQ_PROOF> --lo-proof <LO_RHO_SLOT_PROOF> --approved-producers <C1 producers json>
cd /tmp && $PY -I -B $H3/cp1_points_assembler_c2v001.py records --points-list $L --points-list-sha256 $LS --out-root $ART/s4rc1_c3/registry_<name> \
  --bundle <B1> --bundle <B2> ... --approved-producers <C1 producers json> --genesis-registry <genesis> --genesis-registry-sha256 <sha>
cd /tmp && taskpolicy -b $PY -I -B $H3/cp1_points_assembler_c2v001.py verify --points-list $L --points-list-sha256 $LS --records <REC> --records-sha256 <sha> \
  --c1 <C1> --c1-sha256 <sha> --genesis-registry <genesis> --genesis-registry-sha256 <sha> --out-root $ART/s4rc1_c3/registry_<name>   # ok true
cd /tmp && $PY -I -B "$ENTRY" ledger-append --config "$CFG" --records <REC> --records-sha256 <sha>   # 0 OK, 8 LOCKED; prints head_sha256
cd /tmp && $PY -I -B $H3/storage_check_h3_c2v003.py wave --work-dir <work dir> --next-calls N --out "$R/STORAGE_WAVE_<W>.json"
```
The wave record carries the ledger head sha, the POINTS_LIST sha, the records sha and the per-point bundle shas (A192 item 5 / design map ruling 5). Then relaunch without `--new-campaign`. Add each records file to `storage_check move --pins-from`.

**At W1 (A192 item 5):** after W1's acceptance,
`$PY -I -B $H3/storage_check_h3_c2v003.py wave --work-dir <wd> --threshold-total-free-bytes <df both volumes> --threshold-other-program-bytes <HEADLINE11+S0 measured>`
gives b (call-dir bytes after acceptance), R(b), b* and fits. If it reports `fits: false`, root alerts the principal (A147).

## 4. Tests (TESTED)

`tests/test_campaign_cert_c2v003.py` ran twice from this folder. Each run: **77/77** (53 MUST_PASS, 24 MUST_FAIL), 0 audit denials in the test process and in 50 children, and only the pinned python started (74×). Rows are identical by id, expectation and pass across the two runs; wave 3 has 3 calls.
- `test_runs_c2v003/RUN_20261020T032341Z_30918`: TEST_RESULTS `44fed53d3b2c8d08aa14bc947332052b04b51de33c4162b168b56aa2d3c11676`.
- `test_runs_c2v003/RUN_20261020T032426Z_31913`: TEST_RESULTS `d372202aeeba46a63a479178d6b8875c581f30e06156627ad8ac153650e4c5c0`.
- Stdouts: `test_runs_c2v003/TEST_STDOUT_RUN1.txt` (`7d3099cb…`) and `_RUN2.txt` (`6a05a135…`).

**Rows:**
- **G01-G05, R01-R02 (generator, regenerate):** r10_c4 regression; shipped placeholder; policy/core equal to c2v002; diff positions; exactly six q5b1 lines replaced and slot block L145-191 verbatim; EMPTY_TUPLE; synthetic tuple re-pins with diffs 2/1/1/1.
- **K01-K05 (real chain, dry, v004a):** W1 plans the seed `968c915b`/`3958aed3` with six gates pending, and the ledger is inert. New commands refuse. `ledger-status` reads not configured. The acceptance step refuses a c2v002 entry. The HEADLINE11 CLI lists the 9 probe shas and reads RUN_9_CALLS for other bytes (exit 5).
- **P01-P06 (CP-1 list):** table mode = c3v004 (rows 1-31 plan identical, runner pin `3f5e5c18`); the c3v004 bytes are loaded unchanged; list plan verifies keys. MUST_FAIL: sha mismatch, a key that is not the spec's, a 31-table key, row ≤ 31, a table label, and no anchor AGREE in the out-root. The worker command names the successor and the list pin.
- **H01-H04, A01-A03:** reuse-test REUSE; assemble feeds `deciding_test` and `driver_capability` ok (in memory and on T2). MUST_FAIL: other spec bytes; a run not ACCEPTED; #0 with the step-4 stop; swapped receipts; another call's record. The apply rows cover the ledger field and its refusals.
- **World A (genesis = W1 points):** W1 accepted; **unregistered point** (wave 2 refused at preflight, EA05); `points-manifest` (3 points); CP-1 list (mock) certifies them and the offline replica verifies; `ledger-append` refusals (unapproved producer in a bundle, another point's theta, another point's record, sha mismatch: nothing appended); append (3); re-append refused; cache id and gate digest unchanged; **plan via the ledger** (planned spec shas = ledger entries'); run, **accept**, **reuse** (cache reopen, 4 VALID).
- **F01-F03 (forgery):** a faithful re-chained copy verifies. MUST_FAIL, each closing the gate: **forged entry** (unapproved producer), entry hash, **chain break**, genesis key re-registered, key not the identity digest, torn line, a ledger copied from another work dir. A truncated ledger refuses every cache open.
- **World B (genesis = W1 + wave 2):** W1; wave 2 from the genesis; the **march0-style wave 3** refused, then manifest → CP-1 list (mock) → ledger → planned → run (3 calls). Call 0 reads NON_LAPSE_TAIL_MATERIAL (13, eligible), its rerun, and the **rerun limit** (MUST_FAIL). MUST_FAIL: another call's record. **reingest-invalid** caches it MODEL_INVALID (status re-verifies it). MUST_FAIL: re-run on a cached call. Call 1 reads BOUND_INSUFFICIENT and is certified. Call 2: MUST_FAIL on an INCOMPLETE record and **MODEL_INVALID on an ACCEPTED call**, then VALID through the B2 reingest. All 7 cached; the probe moves to new wave-4 points. MUST_FAIL: one byte changed in the certified record refuses every cache open.
- **S01-S04, Z01-Z02, A90-A91:** b after acceptance (69,632 B > receipt 18,274 B, synthetic); threshold regression; HALTED_DISK exit 5; `move` refuses; 25 named inputs unchanged; nothing published; the audits.

**Declared substitutions (TOY_SEPARATION), on top of c2v002's** (mock driver identity in core/wrapper `DRIVER_SHA`, core `BASE`, handoff `LO_ADAPTER`, v004a with work dir, driver, taxonomy and anchor driver replaced):
- `syn_h3_c2v003` (c2v001 + two reading switches driven by `root_ruling_refs`).
- In the c3v004 commons the successor loads: `DRIVER_SHA` = mock; canonical pins custody / response / gq / eps_adapter / lo_slot_proof = synthetic stubs; `background_qos` = True.
- `mock_cp1_c2v003` producers through c3v004's own injection points; in-process scheduler spawn / memory / swap / vm_stat stand-ins; the LO_RHO_SLOT proof written by the mock instead of root's proof-side step; the CP-1 out-root's anchor records synthetic.
- HEADLINE11 accepted in process by the real handoff v004.
- EB20 uses the stubbed-reingest accept step (as c2v002 EB19).

`dev_runs_c2v003/` holds 6 development runs (39/45, 46/49 and 73/75 from test-side bugs: an audit pattern matching `cp1_runner`, a tuple unpack, the variant reviews; then 75/75, 76/76 and 77/77).

## 5. Open items for root

1. **D5 accounting (needs a ruling).** A certified tail-acceptance MODEL_INVALID is recorded with `judgment_call: true`. That is conservative: a NO_ADMITTED_POINT_FOUND run that uses one never meets the D5 TESTED-NEGATIVE condition. Root rules whether that is the intended class.
2. **`run_mode_admitted: true` for HEADLINE11 capability rows** rests on FINISHED + COMPLETED + ACCEPTED at exactly the probe spec. Before the build, this flag came from the driver's dry-run (parent layer 2). Claude4 confirms the reading.
3. **UNTESTED on real artifacts:**
   - the real CP-1 producers in list mode (mock only);
   - the real HEADLINE11 call layout (the receipt location is not assumed; the result must be `<call_dir>/out/result.json`, the handoff's layout);
   - the real custody deriver on list specs.
4. **List runs write into CP-1's own out-root** (the c3v004 anchor gate needs the anchor's AGREE and context there). This build never opened the live out-root; the first list run is root's act after CP-1 finishes. The alternative design-map option (pinning the c3v004 anchor records for a new out-root) was not built.
5. **Ledger truncation** is caught where the point is used (every cache open refuses, F03), not by the ledger alone. The external anchor is the head sha in each wave record.
6. **"Reruns once"** is enforced as at most two handoff passes per call dir. A pass that refuses before the state export creates no `ACCEPTANCE_TAILSTATES` dir, so it does not count.
7. **The storage threshold is recomputed only when root supplies** both volumes' free bytes and the measured HEADLINE11 + S0 bytes at W1. No default is built in.
8. **Not mine:** the ten 0-byte files from 02:21Z (README C2V002 §5) are still in this folder.

## 6. Files

`HASHES_CAMPAIGN_CERT_C2V001.txt` lists every file this build added (sha256 from bytes), this README included, except itself.
