# Verdict-day command sheet — CX1V001 (0801)

DRAFT, root-operated only. PASS for the read-only command-sheet scope, 0 blocking drafting findings. Production prerequisites remain (below); this is not launch approval. The command interfaces and listed existing input pins were checked from source bytes. No command below was executed; no receipt, result, target velocity, C5H run, or V007_POSTSEAL_RECORDS content was opened. Future artifact pins are intentionally runtime variables, never guessed or replaced with fixture hashes.

## Root inputs and hard stops

1. **Verdict-time data:** root must supply the actual S4T R3 receipt/run path, complete all-case manifests, gate records/rulings, sealed ADOPT_TAIL verdict, final configs/admissions and their published hashes. This draft cannot precompute their hashes. Any missing or changed pin stops the dependent step.
2. **A248 exceptions, superseding the audit-era launch hold:** HEADLINE11 first attempts retain DBP wall100800; S0 first attempts retain serial610324 and twin22752. Root expressly defers a pre-verdict DBP/kit successor. Cap reruns use reviewed P112 cx2v004. The Phase-1 reporting boundary is 2026-11-06T05:59:00Z (Thu Nov5 23:59 CST), with unfinished calls FREEZE_INCOMPLETE and continuing for Phase2. P112 monitor walls use time remaining to Phase2, 2026-12-01T05:59:00Z (Mon Nov30 23:59 CST), per A249; do not stop at Phase1.
3. **Interruption accounting:** P112 cx2v004 and builder c2v007 must carry reviewed cause records; unauthenticated FAILED reruns are uncounted, and two consecutive identical solo raw failures become HELD_FOR_CAUSE (not terminal or automatically rerun). Root must have its alert-only CPU/stage-mtime stall watch before first launch. Nonphysics acceptance passes do not consume H3 MAX_PASSES under root's recorded fresh-pass procedure. Counted list is A248's ROUTE_A_NO_FIXED_POINT / clean ITERATION_BUDGET_EXHAUSTED; FAILED_SOURCE_PREPARATION stays uncounted. Cause producer0805 is commissioned, not adopted.

A218 already resolves PRELAUNCH005/guard014 compatibility: use the guard011 candidate only for emission, then the guard014/launcher015 plan for binding. This is an authorized bridge, not an additional missing-code blocker. A216 already freezes H1 C1; do not repeat the historical C1 creation steps in C1_ROOT_STEPS §0–4.

Run blocks under `/bin/bash`. All new paths must be unused. Use the existing verified runtime:

```bash
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ART=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts
CTRL='/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'
PKT="$ART/v007_launch_packet_cx1"
H3="$ART/h3_campaign_path_c2"
C4="$ART/b1_policy_successor_c4"
C1="$ART/c1_h1_c2/C1_H1_C2V001.json"
REG="$ART/s4rc1_c3/registry_c2v001/REGISTRY_31pts_20261020T140004Z.json"
COMPARE="$CTRL/V007_SEAL_ASSEMBLY/kmax_tail_compare_c2v007_r14_cx1v001_SEALED_V007.py"
PREREG="$CTRL/V007_SEAL_ASSEMBLY/KMAX_TAIL_PREREG_V007_SEALED.json"
# R is a new root-owned record folder outside run trees; PS is root's new postseal output folder.
# Set R, PS and all other uppercase runtime variables from root's registered artifacts before use.
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1
```

`producer_guard_cx1v008` reads its fixed `$PKT/ROOT_SEAL_ADMISSION_V001.json`; export `UNT_ROOT_ADMISSION_SHA256` from the independent root publication (there is no path environment override); verify the source list and seal, never trust a fresh self-hash as publication. The producer guard's exact environment names are checked in the source annex. STOP on any refusal; preserve partial outputs and choose new paths after root's ruling.

## 1. S4T R3 receipt check — root at completion

Root sets `S4T_R3_RECEIPT` from the registered R3 launch record (A197/A198), not the R2 receipt. The registered outdir ends `KMAX_V007_P128_S4T_MS128_CX1_RUN_V011_CX3V001_R3`. No receipt was opened for this draft.

```bash
"$PY" -I -B - "$S4T_R3_RECEIPT" <<'CHECK'
from pathlib import Path
import json,hashlib,sys
p=Path(sys.argv[1]); raw=p.read_bytes(); r=json.loads(raw)
print('receipt_sha256',hashlib.sha256(raw).hexdigest())
for k in ('schema','utc_start','utc_end','status','driver_status','exit_code','stop_reason','command','pins','caps','result'):
    print(k,json.dumps(r.get(k),sort_keys=True))
assert r.get('status')=='FINISHED' and type(r.get('exit_code')) is int and r['exit_code']==0
assert r.get('stop_reason') is None and r.get('driver_status')=='COMPLETED'
CHECK
```

Expected exit 0. Root compares top-level command/pins/caps/result reference with R3 launch publication: driver b5cc62af…, spec8e71be9b…, wall792000, RSS137438953472, output103079215104. Do not dereference result in this receipt-only step. A non-success pauses the verdict path for root classification; no retry or scientific invalidation is inferred by this sheet.

## 2. Cases manifest — A197

Root exclusively writes `CASES` from the registered cases manifest schema. `cases.S4T` must name R3; all other case paths and bindings stay registered. The comparator uses `--manifest "$CASES"` and resolves the sealed case block itself. The separate postseal producer manifest `RESULT_MANIFEST` is an object with `runs` mapping each exact T label to `{path,sha256}` for its `result.json`.

Exact base labels: C2T, C3T, C4T, C6T, S4T, C4T-D5, C4T-C5c, C4T-KLO, C4T-KHI, C4T-A. Root hashes actual result bytes only when authorized to produce the gates. FLAG_RULINGS additionally needs a byte pin `root_rulings` to root's explicit request, per FLAG_RULINGS_REQUEST_SCHEMA_V001.json. Do not use a cases directory map as the pinned-result manifest. Preserve the manifests by exclusive create; publish both hashes. Expected complete exact labels, unique run paths, S4T R3. STOP on absent, alias, stale-R2 or mismatched input.

## 3. Postseal gates — root only

Use the admitted source hashes in the annex; these commands consume saved outputs. For each registered case selected by the gate contract, root supplies `CASE_RUN` and its exact `CASE_LABEL`; use R3 for S4T.

```bash
/usr/sbin/taskpolicy -b /usr/bin/nice -n 10 "$PY" -I -B "$PKT/ea_replay_cx1v012.py" "$CASE_RUN" "$CASE_LABEL" "$PS/EA_${CASE_LABEL}.json"
/usr/sbin/taskpolicy -b /usr/bin/nice -n 10 "$PY" -I -B "$PKT/ra10_checkpoint_cx1v012.py" "$CASE_RUN" "$CASE_LABEL" "$PS/HARMONICS_${CASE_LABEL}.json"
/usr/sbin/taskpolicy -b /usr/bin/nice -n 10 "$PY" -I -B "$PKT/aggregate_records_cx1v008.py" EA "$EA_COMPONENT_MANIFEST" "$PS/EA.json"
/usr/sbin/taskpolicy -b /usr/bin/nice -n 10 "$PY" -I -B "$PKT/postseal_records_cx1v006_cx3v001.py" MT "$RESULT_MANIFEST" "$PS/MT.json"
/usr/sbin/taskpolicy -b /usr/bin/nice -n 10 "$PY" -I -B "$PKT/postseal_records_cx1v006_cx3v001.py" I1T "$RESULT_MANIFEST" "$PS/I1T.json"
/usr/sbin/taskpolicy -b /usr/bin/nice -n 10 "$PY" -I -B "$PKT/postseal_records_cx1v006_cx3v001.py" FLAG_RULINGS "$RESULT_MANIFEST" "$PS/FLAG_RULINGS.json"
```

Expected exit0 and new stamped gate records. `EA_COMPONENT_MANIFEST` is label→component-byte-pin, not `runs`; aggregate EA requires the registered C5H component as well. That component is solely root's existing blinded procedure; this draft neither opens it nor grants this lane access. I1T exports actual runtime checks, not a new independent replay. FLAG_RULINGS exports root decisions and creates none. HARMONICS uses ra10 checkpoint readout with route_a_tail_replay v005 for tail-ON (the old module docstring is stale; lines65–68 implement reconstruction). It reports saved-state harmonics, not a convergence acceptance. Bind each returned HARMONICS record as required by the sealed manifest contract; do not fabricate a combined record with an unadmitted writer.

The five named gate families are not a replacement for the sealed manifest's full registry: preserve all other required identity/SR/T2I/shell/etc records. In particular A88's SR_K timing is a prior obligation; do not silently redo it after T outputs are read. Any missing gate, partial record, producer refusal or unresolved root flag stops comparison.

## 4. Sealed compare r14

```bash
/usr/sbin/taskpolicy -b /usr/bin/nice -n 10 "$PY" -I -B "$COMPARE" --prereg "$PREREG" --manifest "$CASES" --outdir "$VERDICT_DIR"
VERDICT="$VERDICT_DIR/KMAX_TAIL_COMPARISON.json"
VERDICT_SHA=$(shasum -a 256 "$VERDICT" | cut -c1-64)
```

Use full decision, no test/validity-only/gates-only/no-packets override. Expected new report; exit code alone never authorizes adoption. Root checks schema UNT_KMAX_TAIL_COMPARISON_C2V007_R11, script_sha256 a99105a1…, prereg.sha256 b2989012…, pins_verified.V005_addendum c01b3c51…, decision.outcome ADOPT_TAIL, decision.tests_read true, test_mode false (0770). STOP if any differs; publish verdict path and byte SHA. No verdict contents were read for this draft.

## 5. A129 r11 policy finalization — Claude4 0166, root-run

```bash
cd "$C4"
/usr/sbin/taskpolicy -b "$PY" -I -B tools/run_fenced_c4st2.py tools/make_b1_cascade_c4v002.py "$C4/final" v006r11_c4 --dry-run --policy-only --seal-tuple a99105a19b582c68d961e0ee12be3a2efa79dbd1e65d63682c3d2d8daa55f0ab b2989012c92161a7da3dd10d0148e1607422416d369fc4ebe164217758b5c695 c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1 UNT_KMAX_TAIL_COMPARISON_C2V007_R11 "$VERDICT_SHA"
# Only after dry success:
/usr/sbin/taskpolicy -b "$PY" -I -B tools/run_fenced_c4st2.py tools/make_b1_cascade_c4v002.py "$C4/final" v006r11_c4 --write --policy-only --seal-tuple a99105a19b582c68d961e0ee12be3a2efa79dbd1e65d63682c3d2d8daa55f0ab b2989012c92161a7da3dd10d0148e1607422416d369fc4ebe164217758b5c695 c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1 UNT_KMAX_TAIL_COMPARISON_C2V007_R11 "$VERDICT_SHA"
```

Expected dry exit0 then exclusive policy write; not the test `build_f1` output. Copy only the produced policy:

```bash
SRC="$C4/final/v006r11_c4/adoption_policy_cx2v006r11_c4.py"
DST="$ART/calib_tail_readiness_cx2/v006r11_c4/adoption_policy_cx2v006r11_c4.py"
cp -n "$SRC" "$DST"
"$PY" -I -B - "$SRC" "$DST" <<'CHECK'
from pathlib import Path
import hashlib,sys
a,b=(Path(x).read_bytes() for x in sys.argv[1:]); assert a==b
print(hashlib.sha256(b).hexdigest())
CHECK
```

Root ensures destination parent exists and destination absent first; cp-n may silently skip. Publish the computed policy digest. Codex3's gating review checks exactly the tuple/comment change; Codex1's second look is nongating under A208. STOP on changed method, base pins, or tuple mismatch; no update of open V005.

## 6. H3 r12 chain and review dispatch

```bash
"$PY" -I -B "$H3/regenerate_h3_c2v004.py" fill --report "$VERDICT" --filled-by 'root (Claude2)' --ruling "$VERDICT_RULING" --out "$R/SEAL_TUPLE_RECORD_H3_FILLED.json"
SEAL_RECORD="$R/SEAL_TUPLE_RECORD_H3_FILLED.json"
SEAL_SHA=$(shasum -a 256 "$SEAL_RECORD" | cut -c1-64)
"$PY" -I -B "$H3/regenerate_h3_c2v004.py" build --seal-record "$SEAL_RECORD" --seal-record-sha256 "$SEAL_SHA" --out-dir "$R/chain"
```

Expected exit0, chain/v006r12_c4 and REGENERATE_RECORD_v006r12_c4.json; exit2 refuses. Diff against `h3_campaign_path_c2/placeholder_chain_c2v004/v006r12_c4`, not older placeholder/wrapper. Root follows README publication cp-n and byte-equality checks for policy/core/wrapper; entry remains at generated path as registered. Post a fresh numbered FROM_CODEX review request with verdict path/hash, seven allowed verdict fields (0770), r11 policy, seal tuple record, r12 four files, regenerate record and byte hashes. Codex3 is gating; Codex1 second lens nongating. No message was sent by this draft.

## 7. T0 registrations and RI45-13

After actual fill/review, root records whole-line HANDOFF_PIN S0_SEED, SPEC_PIN S0_SEED_SERIAL, WATCH_PIN MEMORY_WATCH, and V007 adoption pin to the verdict report. Full syntax and exact paths are the kit's parsed V006 contract; do not fill these from a historical hash. Register twin spec as required by its own call. HANDOFF proves the registered theta; SPEC binds the fresh filled bytes; WATCH names the extended live watch script. Paths must be canonical and ngc3198-free per A179; no /tmp or runs_ext symlink spelling for fill_dir.

For **each** final launched spec, including twin, root runs the corresponding pinned driver dry plan:

```bash
/usr/sbin/taskpolicy -b "$PY" -I -B "$DRIVER" dry-run --spec "$FILLED_SPEC" --report-dir "$NEW_DRY_REPORT_DIR"
```

Driver is the exact registered NGC r008 or DDO r5 pin in the annex, according to the call. Hash driver and filled spec before it; root reads blocker lists, requires RI45-13 success, and pins the spec and dry report. No scientific stage may execute. STOP on any blocker or stale spec; no inferred success from exit alone. The kit's own dry-verdict/check performs additional handoff/fill/watch/geometry gates. All T0 hashes await real root inputs and are UNTESTED here.

## 8. H1 config and FINAL specs — A216/A227

Root prepares H1 predecessor/delta from the frozen C1 tail_readiness and adopted r11 bindings. Use only C1.tail_readiness, not C1's extra top-level document keys. A248 retains the current DBP first-attempt walls; preserve those exact cap/config bindings. Reruns move to the reviewed P112 ceiling interface.

```bash
BLOCK_SOURCE="$PKT/P128/specs/C4T_P128_MS128_R5_CX1V004.FILLED.json"
"$PY" -I -B "$H3/apply_fields_c2v006/apply_h3_fields_c2v006.py" "$H1_PREDECESSOR" "$H1_DELTA" "$H1_CONFIG" "$R/H1_APPLY_REPORT.json" --seal-record "$SEAL_RECORD" --seal-record-sha256 "$SEAL_SHA" --block-source "$BLOCK_SOURCE" --block-source-sha256 de6d7d77d053d9c983f15eca11468fe8520d025ff2ad1f643b2a517a915b1738
"$PY" -I -B "$ART/step4_launch_readiness_c4/handoff_v004/tools/produce_final_step4_specs_c4v004.py" final --config "$H1_CONFIG" --config-sha "$H1_CONFIG_SHA" --seal "$STEP4_SEAL" --seal-sha "$STEP4_SEAL_SHA" --adoption-policy "$DST" --adoption-policy-sha "$R11_POLICY_SHA" --cases "$HEADLINE_CASES" --outdir "$FINAL_SPECS_DIR" --utc "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

Compute H1_CONFIG_SHA from the newly written bytes before the producer call. `HEADLINE_CASES` is the comma-separated string `TAIL_REANCHOR,WORKERS_8_CANDIDATE_ANCHOR,HEADLINE_TRIAL,HEADLINE_CORNER_000,HEADLINE_CORNER_001,HEADLINE_CORNER_010,HEADLINE_CORNER_011,HEADLINE_CORNER_100,HEADLINE_CORNER_101,HEADLINE_CORNER_110,HEADLINE_CORNER_111`. FINAL mode reads the registry exclusively from C1 tail_readiness; passing --registry would refuse (FINAL_REGISTRY_OVERRIDE_REFUSED). Expected apply exit0 and verified verdict/prereg association; producer exit0 and complete FINAL output/manifest. Exit3 undecided/refused or5 write failure stops binding, including any partial folder. Compare final `binder_pins` against all nine 0778 table-D values reproduced below; do not bind provisional or test specs. The frozen registry/C1 pins remain unchanged. The same block-source correction applies to W1 candidate before V4, but W1 is not launched by this sheet.

## 9–10. PRELAUNCH/bind, then integrity START, then launch

This dependency ordering refines the requested numbering: START snapshots the **final** configs/plans/admissions, so PRELAUNCH and binding precede START, and scientific launch follows it.

```bash
"$PY" -I -B "$ART/step4_prelaunch_cx1/v005/step4_prelaunch_c2v005.py" --admission "$ADMISSION_CANDIDATE" --admission-sha256 "$ADMISSION_CANDIDATE_SHA" --plan "$GUARD011_CANDIDATE" --plan-sha256 "$GUARD011_CANDIDATE_SHA" --output-dir "$PRELAUNCH_OUT"
"$PY" -I -B "$ART/s1_successors_c2/step4_bind_c2v011.py" --final-plan "$GUARD014_FINAL_PLAN" --admission-candidate "$FINAL_ADMISSION_CANDIDATE" --plan-out "$BOUND_PLAN" --admission-out "$BOUND_ADMISSION" --command-out "$BOUND_COMMAND"
```

Expected PRELAUNCH records and successful binder validation. Candidate names guard011 with null prelaunch; final plan names guard014 and launcher015 with actual PRELAUNCH pins and the A248 first-attempt caps. Admission `sources` and source review's `approved_sources` exactly agree; retain guard011 and add guard014/launcher015, native imports, C1 producers and adopted r11 policy (C1_ROOT_STEPS §5 + A218). No missing transitive dependency may be waived.

Under bash, for each phase (S0_SEED and HEADLINE11 separately):

```bash
T="$ART/pinned_input_envelope_c2v003/pinned_input_envelope_c2v003.py"
V006="$CTRL/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md"
"$PY" -I -B "$T" collect --phase "$PHASE" --max-depth 0 "${PHASE_SOURCE_ARGS[@]}" --v006 "$V006" --out "$E/PINSET.json"
PINSET_SHA=$(shasum -a 256 "$E/PINSET.json" | cut -c1-64)
"$PY" -I -B "$T" snapshot --pins "$E/PINSET.json" --pins-sha256 "$PINSET_SHA" --label start --out "$E/START.json"
```

`PHASE_SOURCE_ARGS` is a bash array of `--doc-pin SHA PATH` arguments for final run configs, plans, admission records, and registered inputs. HEADLINE11 includes C1 pin with `--scope "$C1" /tail_readiness` and registry pin; S0 includes gate document `GATE_DOCUMENT_PINS_V002.json` SHA5e688882451824931f964e610cf17597d82ee0eb246fb0dce528ec0c6e148042 and its final config/spec/admission; add scoped C1/registry only if its config carries tail_readiness. Root must fill the complete array from final artifacts; an empty array is not a phase envelope. Expected both exit0; exit3 INVALIDATE stops phase. Preserve this same pinset for END; no re-collect. No chmod/hardlink/GUI mutation of inputs during phase.

Root independently publishes `UNT_STEP4_ADMISSION_PATH`/SHA256, verifies the generated command and launches **that** command after START. Its actual executor is launcher015 `PLAN --execute-root-only`; do not bypass the generated single-thread/nice/taskpolicy/lock environment. The launcher detaches: launcher return0 is not completion. Monitor child receipts and root non-content stall watch; all retries require new root ruling. HEADLINE11 max_active counts route-A only (A247), not total jobs.

## 11. S0 serial seed then twin — A248 retains first-attempt kit

Current adopted exact interfaces; run dry first:

```bash
/bin/bash "$ART/s0_launch_kit_c2/launch_s0_serial_root_c2v003a.sh" seed --launch-root "$S0_LAUNCH_ROOT" --run-root /Volumes/External1/NGC_S0_PHASE1_V001 --attempt 1 --step2-receipt "$STEP2_LAST_RECEIPT"
/bin/bash "$ART/s0_launch_kit_c2/launch_twin_root_c2v003a.sh" --launch-root "$S0_LAUNCH_ROOT" --run-root /Volumes/External1/NGC_S0_PHASE1_V001 --attempt 1 --step2-receipt "$STEP2_LAST_RECEIPT" --dry-fill-dir "$SEED_DRY_FILL_DIR" --watch-poll-s 30
```

Default is dry, no launch. After every T0/START gate passes and root installs the alert-only stall watch, A248 authorizes these current first-attempt commands with `--launch`; omit dry-fill-dir for live twin, which uses serial's registered fill. Seed must have a confirmed LAUNCH before twin (A166); both wait until step2's last receipt. Keep M-15 ordering, watch, volume/D9 checks and twin iteration1 planned stop. Exit5/parse timeout means reconcile/stop qualified child under root rule, never assume it died. Any cap/signal/root stop is nonphysics, never a completed twin without explicit bound planned-stop evidence. A248 expressly authorizes these first-attempt fixed walls; subsequent retries need reviewed P112 cx2v004 and A249 cause/hold handling. This sheet grants no independent launch authority.

## Validation and future pins

TESTED: existing named code/docs/config bytes hashed, sealed tuple constants checked by AST without import, CLI signatures inspected. UNTESTED: all production invocations, future report pins, final admissions/source closure, actual dry plans, envelopes, launch settings, final spec equality, and success under contention. Deciding tests are the root steps above after prerequisites. No science/seal/launch was performed. This sheet is a draft command interface with explicitly required future inputs, not an executable all-in-one script.

## 0778 table D — expected FINAL binder pins

| # | Case | Registry row | Predicted spec sha256 |
|---|---|---|---|
| 2 | TRIAL | P01 | `f4ae15461f669979e8648e6686f093c6a909988f9cfb122de71b42c073327aff` |
| 3 | CORNER_000 | P02 | `14e943baa68acceec5dfd600efa8b7b536d7c76adb5239d900a597d4e0c24cec` |
| 4 | CORNER_001 | P03 | `eed3be9b19b6941ba30ab4ac09e8787f6aaf331ba2e6d81317dea51cc597bf40` |
| 5 | CORNER_010 | P04 | `e6c0e3cda12276c3fb830906c0ee30c9a20912015225418755145182e3a81031` |
| 6 | CORNER_011 | P05 | `bb7014113d66c38b634d07e4ff59a730c3762812c10e9bace78c0280bd12505b` |
| 7 | CORNER_100 | P06 | `fac5b8a11754ecc5b4665c2f640f8bce56d5c614c52e42b39ceb3a9ea469ed7c` |
| 8 | CORNER_101 | P07 | `d6a63c4bcb47f0b05b5d08c740d1ea67bf5a4ad2240313ce087410e9f804a290` |
| 9 | CORNER_110 | P08 | `44fee9a4e247d810d508b440c9dc07e67aa5abf7dac312704bc2e2df92b9112e` |
| 10 | CORNER_111 | P09 | `ca46f232cd9d18601c218f895ec490679df85fae710057f2edea9cf71265a510` |


## Existing input hashes computed from bytes

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/PRODUCER_INDEX_V009_CX3V001.json` — `7a61747efeee8ff27e8e5b3c2213a0aa2f3e8ed888e871ac1df193a6a64b6a97`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/producer_guard_cx1v008.py` — `294cb7760679b883a62fb3117dc75e91231b2f173bcec65983e6762371ea0731`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/ea_replay_cx1v012.py` — `380e2d81027eba4c86843b904ccb79f5f27e6c917b5f3f5a71f286c01be32156`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/aggregate_records_cx1v008.py` — `9794123d20d6617428a7e6445af5a831885946f0178e9a58edee5801ba01b28f`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/postseal_records_cx1v006_cx3v001.py` — `4024d82a8ec59ba339f00214066798ea905d1234466d29db2e8bb5e5869de366`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/ra10_checkpoint_cx1v012.py` — `b66dd9c083dda5bd4218baf12583c842ce8548ecbeb11df5ada4d953cbfa8b98`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/route_a_tail_replay_cx1v005.py` — `9e49aad93ed85f1ade6f620836fa2ab14d38010633b4a6bf0ed9a03de7691465`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/POSTSEAL_PRODUCER_CONTRACT_V001.md` — `34aa2897fd06ea2cb19642bc914edc2ea170fbb3658d3ca41fa975672b898778`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/CASES_MANIFEST_TEMPLATE_V011_CX3V001.json` — `df4cad82f947edf85741ce97d5902c9b926daa1401448c5daac4ad461a2b1726`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/b1_policy_successor_c4/tools/make_b1_cascade_c4v002.py` — `a7a5fe58d509b99f14cb000305633c6f192ac71f5093f4ec5fa1a2fa6f1a1f35`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/b1_policy_successor_c4/tools/run_fenced_c4st2.py` — `fe904509c7d2d6300042589aaa02d839e82b436680d293b65c5c7d4cf69f6d25`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/regenerate_h3_c2v004.py` — `ad5cee08650b78d3e012a874dcde6afdad39a9cfd17146a35422802ac8db346e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/make_campaign_cascade_c2v004.py` — `5014b04f0de3cf2fc0289dcabe519e0056f9395302cfd1b9b4082b4d045b228a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/apply_fields_c2v006/apply_h3_fields_c2v006.py` — `0ed72837684f345b311401ea90b9889cd46b8431753a4e0697225e9849aff951`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/handoff_v004/tools/produce_final_step4_specs_c4v004.py` — `fcbf1c3ed175e1cfb3519c33324622a3b0ed190769e71b199687bd46dd1cb7ba`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/handoff_v004/tools/fence_c4v003.py` — `5851f42f259ab5b967c89ec0c66e7e1573353f1076bb498e5aae60ad04b42940`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_prelaunch_cx1/v005/step4_prelaunch_c2v005.py` — `117b35209cc57d8eda730bed94a772e3b29c4ee25bc33a4fcf4628ef70bc6f27`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/step4_guard_c2v014.py` — `6efdca016416a919b25a1e23d46a415b75fe2b5e60145ba098f864730975165d`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/step4_launcher_c2v015.py` — `cd987edd097323999847208d7b5fdfd93dadecb8a10beb6feaf91a0c53b68e0b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/step4_bind_c2v011.py` — `d3d9702eb8096d11b98461f1c62c67931b9ecf74957cee95fbc3a60f60deaea0`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/pinned_input_envelope_c2v003/pinned_input_envelope_c2v003.py` — `9d531381615f7b68f2f33bfc19f0aa2bcfe97a4e6f5c0e93187ea8eb35ce8d9a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/pinned_input_envelope_c2v003/README_PINNED_INPUT_ENVELOPE_C2V003.md` — `3f0a63f9a79cb3bd572a2d84e417e56d32b5200aa7ebe2d96cf5047f27de7ccb`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/pinned_input_envelope_c2v002/README_PINNED_INPUT_ENVELOPE_C2V002.md` — `bcf34ecb4b64793cdcfc14dd45ba5ad469593949fafbb82736ae3c2c73c26b8b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/c1_h1_c2/C1_ROOT_STEPS_C2V002.md` — `7f173b9136bb9e6c4607a1af5efd44ccb205ec91a55d4178b4d99ef1c27b2f3c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/launch_s0_serial_root_c2v003a.sh` — `621263a21b813e8c71762cea57b0efc6ba36aecb1cf9023cc788f9133c3a96c2`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/launch_twin_root_c2v003a.sh` — `f199544db9fe40a4fedbe7647d52ad4bd8dacb13a9aa9c1b9ab4ad0198e7769f`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/s0_kit_c2v003a.py` — `fdc0ee6c833072b40991750f8df1122a1b51910986f01af3480a73cccfbed550`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py` — `577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py` — `b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/V007_SEAL_ASSEMBLY/kmax_tail_compare_c2v007_r14_cx1v001_SEALED_V007.py` — `a99105a19b582c68d961e0ee12be3a2efa79dbd1e65d63682c3d2d8daa55f0ab`
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/V007_SEAL_ASSEMBLY/KMAX_TAIL_PREREG_V007_SEALED.json` — `b2989012c92161a7da3dd10d0148e1607422416d369fc4ebe164217758b5c695`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/c1_h1_c2/C1_H1_C2V001.json` — `4015932226dcfbf9783b96de1daa512ef5c7a397ac4ca093d701ead362ed92c1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/registry_c2v001/REGISTRY_31pts_20261020T140004Z.json` — `2dea408ff698e265a41bac1ef2562737ae98ffd4583477632e7a79507a15e319`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_launch_packet_cx1/P128/specs/C4T_P128_MS128_R5_CX1V004.FILLED.json` — `de6d7d77d053d9c983f15eca11468fe8520d025ff2ad1f643b2a517a915b1738`
