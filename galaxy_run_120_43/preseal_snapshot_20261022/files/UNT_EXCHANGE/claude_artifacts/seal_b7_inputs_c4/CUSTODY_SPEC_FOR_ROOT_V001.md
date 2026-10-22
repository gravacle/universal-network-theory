# Raw successor-custody record for seal tool 4 (B7 input 3): what root runs

From: Claude4 helper (dispatch 0650, V006 A113 P6). Written 2026-10-19T04:01:08Z (`date -u`). Status: a specification for root. Nothing here was run on a real run output. The converter was tested on synthetic fixtures only.

Labels: **TESTED** means run on bytes in this folder. **FORMAL** means read from source. **UNTESTED** means neither.

## 1. What tool 4 needs, and the rule behind it

- Tool 4 (`build_seal_record_c4v004.py`, sha256 `9787cf587ca3e9a92c24587a9c5ea56568b808f53c48acf739eea71b997ceb41`) reads `--successor-custody Z.json` with strict JSON. It calls `custody_codes(chk, obj, slots['driver']['sha256'])` (FORMAL, L486; TESTED that the call text occurs once).
- The form tool 4 accepts (FORMAL, L230-252):
  - `schema` = `UNT_V007_SEAL_RAW_SUCCESSOR_CUSTODY_C4V002`;
  - `identity_run` = `"Z2"`;
  - `driver_sha256` = the driver slot sha;
  - `stages_total` = `stages_successor`, an integer greater than 0;
  - `verdict` = `"PASS"`;
  - `method`, a non-empty string;
  - `evidence`, an optional list of `{path, sha256}`; each pin is verified from bytes when the record is built;
  - `note`, optional.
- **The driver slot.** Prereg r6 (`d28c95f5…0c0a9`) names one candidate for `seal_slots.driver`: r5, `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py`, sha256 `b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6` (TESTED from the prereg bytes and the driver bytes). Root's slots file sets `driver.sha256`. Tool 3 requires that value to equal the sealed prereg's slot value.
- **Rules.**
  - V005 A59: Z2 replace mode; the raw successor-custody check is recorded in the seal record.
  - A67 N1: every identity run is on the driver slot.
  - A81 RI-21: the records of record are the c2v007-lineage round's outputs on the driver slot's identity runs, with the raw successor-custody check.
  - Prereg r6 `seal_record_requirements`: "The raw successor-custody check of the Z2 run is recorded (A59)."
  - V006 A113 P6: "produced by c2v007r2's own tool from the R5_V001 identity runs. Root runs it, since it reads `UVT_*`."

## 2. The pinned objects (from the prereg and record bytes)

| Object | Path | sha256 | How known |
|---|---|---|---|
| Identity comparator slot c2v007r2 | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/run_identity_compare_c2v007.py` | `052da0fe378b7927f35be28f9eda6f03313aef32bae7d5c9a301d276de21b12e` | prereg r6 `seal_slots.identity_comparator.named_candidates_verified_from_bytes.c2v007r2`; TESTED from bytes |
| Z2 identity gate record of record (B1, R5_V001) | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/records/R5_V001/B1_R5_C2V007.json` | `83e7b0673159156832995a1d7caae401a430918cbd110975bac8e18335aedc72` | prereg r6 `seal_slots.identity_gate_records` Z2; TESTED from bytes |
| Its report of record (the c2v007r2 output on the Z2 run) | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/out/IDENTITY_C2V007_R5_V001/Z2.json` | `ac793faff46adb26c71effe880dfb3e92642a36dec8c33e57d83f350d8f49795` | the record's `identity_comparison.report` (TESTED from the record bytes). **This helper did not open the report** (UNTESTED here). |
| Z2 tokens | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/tokens/TOKENS_Z2_R5_C2V007.json` | `0773782b6ce323a6e5bec3241791e6daf9188050f7296483ccaed6d98b9dcbb0` | the record's `tokens`; TESTED from bytes |
| The R5_V001 Z2 run (new side) | `/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext/UVT_Z2_A2F10_R5_RUN_V001` | (a directory) | the record's `run.path`, with `driver_sha256` = b5cc62af and receipt FINISHED. V005 A67 lists the run with spec 2d5e79d0. Path only: **not opened, listed or stat-ed here** |
| The reference run | `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008_DECIDING_RUN_V001` | (a directory) | the record's `reference_run.path`. Path only: **not opened** |
| c2v007r2's own gate-check tool | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2/tools/r5_gate_check_c2v007.py` | `5dcd51422409f3354b480e67bd59c28f1b3412b756ea3228d834d133a673d745` | pinned by `R5_IDENTITY_COMPARE_COMMANDS_C2V007_R2_V002.sh` (`283cfde4e9da72b07300e2c92b0a16f19f6d41adf1fb79287302779829a43dc7`), the script that ran the R5_V001 comparisons; TESTED from bytes |
| The converter (this folder) | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_b7_inputs_c4/tools/make_custody_record_c4v001.py` | `1b097cbaf75d4bc1931218d943c6f247f99291a233ca46c2c0a6933d061ca841` | TESTED from bytes; synthetic tests below |

The B1 record's own fields:
- `identity_comparison`: gate Z2, driver_selected r5, verdict PASS_BITWISE_EQUAL, `failing` [], and `checks.SCRIPT_CUSTODY` true and `NEW_DRIVER_PIN` true;
- `a67_n1.identity_run_driver_sha256` = b5cc62af;
- `verdict` PASS_BITWISE_EQUAL_EXCEPT_DECLARED.

(TESTED from the record bytes.) The record carries the custody check's pass bit, but not its stage counts. The counts are only in the comparator report.

## 3. How c2v007r2 computes the raw successor custody (FORMAL, comparator source 052da0fe)

- **`SCRIPT_CUSTODY` (L2327-2347, "A59 raw").** For every stage directory of the new run that has a `request.json`, the comparator computes `planned_script(gate, name, request, driver)` (L1580-1595). For gate Z2 that is:
  - `SCRIPTS_UVT[kind]` for the eight `UVT_TAIL_KINDS`;
  - `RO1_ROUTE_A['worker' | 'worker_parallel']` for `route_a`;
  - `AUX_UVT['manifest_writer']` for `route_a_tail_manifest`;
  - otherwise the base `SCRIPTS[kind]`.

  It then requires the request's `(script, script_sha256)` to equal that plan, with the plan's bytes hashing to its sha. Each stage gets a row `stages[name] = {kind, script_sha256, planned_sha256, ok}`, and the check passes iff no row fails. The rule text is `A59: every new stage runs the driver-planned script for gate Z2, hashed from bytes`.
- **`NEW_DRIVER_PIN` (L2331-2335, A67 N1).** The new run's `start.json` driver and `driver_sha256` and its `result.json` `driver_sha256` must be the selected driver pin (`--driver r5` = b5cc62af).
- **`STAGE_SET` (L2229-2231).** Its detail carries `order_new`, the new run's full stage list.
- **Output.** The comparator writes ONE report, by exclusive create, to `--out`. Its head holds `schema RUN_IDENTITY_COMPARE_C2V007`, `gate`, `driver_selected`, `driver_pin`, `comparator {path, sha256}`, `reference`, `new` and `tokens {path, sha256}`. It also holds `checks {name: {pass, detail}}`, `verdict` (PASS_BITWISE_EQUAL or FAIL), `failing` and `comparator_sha256_at_end`. On stdout it prints `{"verdict", "failing"}`. Its exit code is 0 iff PASS_BITWISE_EQUAL (L2097-2107).
- **The gap the converter closes.** `SCRIPT_CUSTODY` alone does not prove that every stage ran a successor, for two reasons:
  - (a) a stage without `request.json` gets no row (L2337);
  - (b) a stage of a kind outside the UVT kinds is planned on its base script and still passes.

  The converter therefore requires one row per stage of `STAGE_SET.order_new`. From the driver slot's own tables (read as AST from its bytes; no driver code executed), it requires that every stage ran its Z2 successor: `SCRIPTS_UVT[kind]` (never the base), an RO1 tail route-A worker for route_a, or the manifest writer. **Any other kind refuses** (`STAGE_KIND_HAS_NO_SUCCESSOR`).

## 4. The commands root runs

Shared settings (zsh):

```sh
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
G7=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v007/r2
C4=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_b7_inputs_c4
R5=b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6      # = root's slots driver.sha256 (check it)
CMP_SHA=052da0fe378b7927f35be28f9eda6f03313aef32bae7d5c9a301d276de21b12e
B1=$G7/records/R5_V001/B1_R5_C2V007.json
B1_SHA=83e7b0673159156832995a1d7caae401a430918cbd110975bac8e18335aedc72
OUTDIR=$C4/root_run        # or any root-owned folder outside both compared runs; it must not exist yet
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
pin() { [ "$(shasum -a 256 "$1" | cut -d' ' -f1)" = "$2" ] || { echo "PIN MISMATCH: $1"; return 1; } }
```

### Option A (recommended): convert the report of record. No run is touched again.

The report of record is c2v007r2's own output on the R5_V001 Z2 run (A92). It sits under `gates_v007/r2/out/`, not under `runs_ext`. The converter reads only:
- the report;
- the B1 record;
- the comparator, tokens and driver sources;
- tool 4.

It never opens, lists or stats a run directory.

```sh
pin $G7/run_identity_compare_c2v007.py $CMP_SHA && pin $B1 $B1_SHA && \
pin $C4/tools/make_custody_record_c4v001.py 1b097cbaf75d4bc1931218d943c6f247f99291a233ca46c2c0a6933d061ca841 && \
REP=$G7/out/IDENTITY_C2V007_R5_V001/Z2.json && \
REP_SHA=ac793faff46adb26c71effe880dfb3e92642a36dec8c33e57d83f350d8f49795 && pin $REP $REP_SHA && \
mkdir "$OUTDIR" && \
$PY -I -B $C4/tools/make_custody_record_c4v001.py --report $REP --report-sha256 $REP_SHA \
  --identity-record $B1 --identity-record-sha256 $B1_SHA --driver-sha256 $R5 \
  --out $OUTDIR/RAW_SUCCESSOR_CUSTODY_Z2_R5_V001.json --dry-run > $OUTDIR/dry_run.stdout.json && \
$PY -I -B $C4/tools/make_custody_record_c4v001.py --report $REP --report-sha256 $REP_SHA \
  --identity-record $B1 --identity-record-sha256 $B1_SHA --driver-sha256 $R5 \
  --out $OUTDIR/RAW_SUCCESSOR_CUSTODY_Z2_R5_V001.json
```

### Option B (A113 taken literally): re-run c2v007r2 on the Z2 run, then convert the fresh report

**Read this first.** The comparator's containment guard (`registered_identity`, L312-323, FORMAL) stats `runs_ext` and **lists it** (`os.scandir`) to read the inode of the registered C5H directory `KMAX_A2F10_C5H_RUN_V001` from the listing. The C5H directory itself is not stat-ed or opened. Root's manual disclosure A105_E_OPS5 (SEAL_MANUAL_DISCLOSURES_V002) says "No further C5H metadata access before the seal". A re-run touches the C5H directory entry in that listing. Root decides whether that is acceptable before running it. The receipt check also reads the run's receipt and `result.json` under `runs_ext`.

```sh
REF="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs"
EXT="/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext"
pin $G7/run_identity_compare_c2v007.py $CMP_SHA && pin $G7/tokens/TOKENS_Z2_R5_C2V007.json 0773782b6ce323a6e5bec3241791e6daf9188050f7296483ccaed6d98b9dcbb0 && \
pin $G7/tools/r5_gate_check_c2v007.py 5dcd51422409f3354b480e67bd59c28f1b3412b756ea3228d834d133a673d745 && pin $B1 $B1_SHA && \
pin $C4/tools/make_custody_record_c4v001.py 1b097cbaf75d4bc1931218d943c6f247f99291a233ca46c2c0a6933d061ca841 && \
$PY -I -B $G7/tools/r5_gate_check_c2v007.py receipts --ext "$EXT" --driver-sha $R5 UVT_Z2_A2F10_R5_RUN_V001 && \
mkdir "$OUTDIR" && \
taskpolicy -b $PY -I -B $G7/run_identity_compare_c2v007.py --gate Z2 --driver r5 \
  --reference "$REF/DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008_DECIDING_RUN_V001" --new "$EXT/UVT_Z2_A2F10_R5_RUN_V001" \
  --tokens $G7/tokens/TOKENS_Z2_R5_C2V007.json --out $OUTDIR/Z2_CUSTODY_RERUN.json > $OUTDIR/z2_rerun.stdout.txt 2> $OUTDIR/z2_rerun.stderr.txt; C=$?
$PY -I -B $G7/tools/r5_gate_check_c2v007.py verdicts --comparator-sha $CMP_SHA --driver r5 Z2=$OUTDIR/Z2_CUSTODY_RERUN.json=$C && \
REP_SHA=$(shasum -a 256 $OUTDIR/Z2_CUSTODY_RERUN.json | cut -d' ' -f1) && \
$PY -I -B $C4/tools/make_custody_record_c4v001.py --report $OUTDIR/Z2_CUSTODY_RERUN.json --report-sha256 $REP_SHA \
  --identity-record $B1 --identity-record-sha256 $B1_SHA --driver-sha256 $R5 \
  --out $OUTDIR/RAW_SUCCESSOR_CUSTODY_Z2_R5_V001.json --dry-run > $OUTDIR/dry_run.stdout.json && \
$PY -I -B $C4/tools/make_custody_record_c4v001.py --report $OUTDIR/Z2_CUSTODY_RERUN.json --report-sha256 $REP_SHA \
  --identity-record $B1 --identity-record-sha256 $B1_SHA --driver-sha256 $R5 \
  --out $OUTDIR/RAW_SUCCESSOR_CUSTODY_Z2_R5_V001.json
```

In Option B the converter also re-reads the report of record (`ac793faf…`) and refuses `RERUN_DIFFERS_FROM_THE_REPORT_OF_RECORD` unless all of the following equal it:
- gate, driver, comparator, runs, tokens, verdict and failing;
- the `SCRIPT_CUSTODY`, `NEW_DRIVER_PIN` and `STAGE_SET` checks.

## 5. What the output must show

- **Comparator (Option B only):**
  - stdout `{"verdict": "PASS_BITWISE_EQUAL", "failing": []}`, with exit code 0;
  - `r5_gate_check_c2v007.py verdicts` prints `"ok": true`;
  - `receipts` prints `"ok": true` for `UVT_Z2_A2F10_R5_RUN_V001`.
- **Converter:**
  - the dry run prints the record on stdout, and `{"verdict": "DRY_RUN_PASS", "sha256": H, ...}` on stderr;
  - the real run prints `{"verdict": "PASS", "out": ..., "sha256": H}` on stderr, with exit code 0, and the same H;
  - on any defect it prints `{"verdict": "REFUSE", "code": ...}`, exits 2 and writes nothing.
- **The record**, `RAW_SUCCESSOR_CUSTODY_Z2_R5_V001.json`, exactly tool 4's form:
  - `"schema": "UNT_V007_SEAL_RAW_SUCCESSOR_CUSTODY_C4V002"`, `"identity_run": "Z2"`, `"driver_sha256": "b5cc62af…"` (= `slots.driver.sha256`);
  - `"stages_total": n`, `"stages_successor": n`, `"verdict": "PASS"`;
  - `method`, quoting the comparator, report, runs, tokens and driver with their shas and the successor rule;
  - `evidence`: report, B1 record, report of record (Option B only), comparator, tokens, driver and converter, each as `{path, sha256}`;
  - `note`, with the stages by successor class.
- **The expected n (UNTESTED).** The B1 record lists 17 stages that received the tail argv block: 16 UVT-kind stages and route_a. With the `route_a_tail_manifest` stage, which Z2 requires, n = 18 if the run has no stage of another kind. If the run has a stage of a kind with no successor (for example `feedback_v002` or `column_mean_v004`, which are in the driver's SCRIPTS), the converter refuses with `STAGE_KIND_HAS_NO_SUCCESSOR` and root must rule.
- **Then tool 4:** `--successor-custody $OUTDIR/RAW_SUCCESSOR_CUSTODY_Z2_R5_V001.json`. `custody_codes` must report no failure against `slots.driver.sha256`. TESTED on the converter's synthetic output: no failure. The must-fails return `CUSTODY_DRIVER_NOT_THE_SLOT` (r4 sha), `CUSTODY_STAGES` and `CUSTODY_RUN`; see `VALIDATION_TOOL4_B7_C4V001.json`.

## 6. Converter refusals, TESTED on synthetic fixtures

`TEST_CUSTODY_CONVERTER_SYNTHETIC_C4V002.json`: 31 of 31 cases behave as expected, 2 PASS and 29 refusals. Each refusal exits 2 and writes no output.

- **Successor rule.**
  - a stage without its custody row;
  - a UVT stage on its base script;
  - a stage not on its planned script;
  - a stage kind with no successor;
  - route_a on the base parallel worker;
  - no stages.
- **Run and driver.**
  - gate Z2_OFF_RO1;
  - a report on driver r4;
  - a `--driver-sha256` that is not the report's driver;
  - NEW_DRIVER_PIN on another driver;
  - a record on another driver.
- **Comparison and record.**
  - a FAIL verdict;
  - SCRIPT_CUSTODY false;
  - comparator not c2v007r2;
  - a record naming another run;
  - a re-run that differs from the report of record;
  - a SCRIPT_CUSTODY rule of another gate.
- **Malformed input.** A duplicate JSON key, a NaN, a non-object report, SCRIPT_CUSTODY absent, an extra key in a stage row.
- **Pins and output.**
  - a wrong report sha;
  - a wrong record sha;
  - `--out` existing (the existing file is left unchanged);
  - `--out` inside a compared run.
- **Command line.** A repeated flag, `--flag=value`, an abbreviated flag.

The driver tables the converter reads by AST equal an independent regex extraction from the same bytes, for all 6 tables (TESTED). The superseded v001 run (`…_C4V001.json`) also passed 31 of 31 cases. Its regex missed one entry, whose source line ends in a comment, so its cross-check read false. The run is kept, not deleted.

The CLI was TESTED through the fence runner (`fixtures/custody_cli_v002/`):
- a dry run, then a real write, with the same sha `d9ad6da8…`, exit code 0;
- an r4 `--driver-sha256`, exit code 2 with `DRIVER_NOT_THE_SLOT` and no output.
