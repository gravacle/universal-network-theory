# NGC serial = parallel identity pair: byte-equality comparison spec (C2V001)

**Purpose.** A132 and A133 §1.4 make the first NGC launch a pair at one theta: the serial call of record and a twin that differs only in `numerics.route_a.column_workers` (1 vs 8). If the pair is byte-equal, the serial = parallel identity is TESTED at that theta. Later calls may then run at 8 workers, and the NGC re-binding key excludes `column_workers`. If the pair differs, every call stays serial, and the twin is recorded and not used.

**Tool.** `tools/compare_identity_pair_c2v001.py`. It follows the idea of the I4 producer (`ri33_c3/i4/write_i4_record_c3v003.py`, `707395ba`), cut to the files one NGC route-A stage writes by iteration k. The checkpoint module c2v003 (`069b3935`) is loaded inert from verified bytes, and its own `_read` (integrity), `_canonical` and `decode` are used unchanged. No driver, stage or solver code is executed.

**Values.** The tool never prints or records a value. The record holds booleans, integer counts, relative file paths and pins only, and test C02 checks that the record contains no float.

## The pair

| | call of record | identity twin |
|---|---|---|
| spec | `CALL_A_K32_A2_HEADLINE_C2V001.json` | `CALL_A_K32_A2_HEADLINE_CW8_TWIN_C2V001.json` |
| `numerics.route_a.column_workers` | 1 | 8 |
| route-A worker (driver-planned, D03) | `ee27227c` | `293a417f` |
| route-A solver | `8ef3079b` | `7667025b` |
| argv | no `--column-workers` | `--column-workers 8` once, right after `--start-iteration 0` |

Both specs come from one `fill_step5_c2v001` run. They carry the same label (`step5 A_K32_A2_HEADLINE theta_key=<key>`). The filler refuses to write either spec unless the two differ only in that leaf. The tool checks this again from the pinned bytes: it strips the leaf and compares the remainder canonically, and it refuses if anything else differs.

## What is compared (route-A stage `stages/NN_route_a/`)

| check | what is compared | declared differences (custody only) |
|---|---|---|
| spec pins | `<run>/inputs/call_spec.json` equals the pinned spec, per side | — |
| C1 custody | `request.json`: script and script_sha256 are the planned worker; `--solver` / `--solver-sha256` are the planned solver; the `--column-workers 8` rule (twin only) | after the flag is removed, the argv lists are equal once each side's run root, worker and solver spellings are replaced by tokens |
| C2 checkpoint identity | `checkpoint/IDENTITY.json`: per side, record integrity and `identity_sha256 = sha256(canonical(identity))`, and `caller.sha256` = the module's `digest` of the decoded caller. Across the two sides these must be equal: `format`, `fixed_source`, `environment`, `inputs_sha256`, `shapes`, `controls`, `code.checkpoint` and `code.modules` | `code.solver`, which must be each side's planned solver. The caller's exact encoded record is compared after the run-root, worker and solver tokens are applied |
| C3 payloads, per compared iteration k | `iteration_k/START.json`, every `column_NNNNN.json` (0 … column_count−1) and `COMPLETED.json`, each read through the module's integrity check; equal across the two sides | removed before comparing: `identity_sha256`, `iteration_start_sha256`, `attempt`, `payload_sha256` (the identity chain and the attempt token). Per side, each column's and COMPLETED's `iteration_start_sha256` must equal that side's START `payload_sha256`, and every record's `identity_sha256` must equal its IDENTITY |
| C3 failure | no `FAILURE.*` record in a compared iteration | — |
| C4 digests | every blob that a compared START or COMPLETED names exists and hashes to its name (`blobs/<sha>.npy`). Content addressing then makes equal references mean byte-equal arrays | — |
| C5 sidecar | `uv_tail_sidecar/SIDECAR_IDENTITY.json`: per side, `identity_sha256 = sha256(canon(identity))` and `identity.checkpoint_identity_sha256` = that side's checkpoint identity; across sides, equal once that field is removed and the run-root tokens are applied. `iteration_k.json`: `payload` equal. `elements_k.npz`: per side, the arrays digest to the payload's `positions_digest` and `J_digest` | `diagnostics` (wall-clock seconds and per-process cache counters; controller c5bdd055 L494–506). The npz zip bytes are not compared, because they carry timestamps; their arrays are |

**Not compared, with the reason:**
- `progress.jsonl` and the worker's `arrays/*.npz`: they repeat the checkpoint arrays, and they carry `elapsed_seconds` and zip timestamps.
- `node_diagnostics/`: logs.
- `attempt_000/start.json`: custody. Its worker pin and paths are covered by C1 and C2.
- Iterations after the last one compared.
- Route B, the readout and `result.json`: the twin is stopped before them.

## Iterations and timing

- **Required.** Iteration 0 always. `--iterations N` compares iterations 0 to N−1; root rules N.
  - N = 1 is the iteration-0 test (A133's minimum).
  - N = 2 also covers the first warm-state transfer to the workers, which is the separate code path Claude4 0174 recommends testing.
- **When it can run.** Once both sides have completed the compared iterations (the serial call of record keeps running). Records are append-only and published atomically, so reading a running serial tree is safe.
- **When the twin stops.** The twin is planned to stop at its wall cap (CAPS: 22,752 s, which is 2 × the U time to the end of iteration 1).

## Verdicts

| verdict | when | exit | reading (A133 §1.4) |
|---|---|---|---|
| `SERIAL_EQUALS_PARALLEL_BITWISE_TAIL_ON` | every check holds | 0 | the identity is TESTED at this theta |
| `DIFFERENT` | a compared file differs, or a custody, digest or integrity-chain check fails | 1 | everything stays serial; the twin is recorded and not used |
| `NOT_READY` | a compared iteration is not complete on both sides | 4 | decides nothing; re-run later |
| refused (no record) | bad pins, specs differing outside the leaf, a protected path (`uvt_` component, C5H marker, an NGC target spelling), a missing route-A stage or IDENTITY, or a record failing its own integrity check | 3 | fix the input |

## Command

```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
$PY -I -B tools/compare_identity_pair_c2v001.py --serial <serial run dir> --twin <twin run dir> \
    --serial-spec <CALL_A_K32_A2_HEADLINE_C2V001.json> --serial-spec-sha256 <sha> \
    --twin-spec <CALL_A_K32_A2_HEADLINE_CW8_TWIN_C2V001.json> --twin-spec-sha256 <sha> \
    --iterations 1 --out <new record path>
```

## Tests (synthetic run trees written with the checkpoint module's own record format; record runs 83/83)

- **MUST_PASS.**
  - C01: an honest pair is EQUAL. Its run roots, attempt tokens, worker and solver custody, diagnostics timings and npz zip bytes all differ.
  - C02: the record contains no float.
  - C03: iterations 0–1 are EQUAL.
- **MUST_FAIL.**

  | test | case | result |
  |---|---|---|
  | C04 | a column result 1 ulp apart | DIFFERENT, naming exactly that column |
  | C05 | a START gas array 1 ulp apart | DIFFERENT |
  | C06 | a COMPLETED residual differs | DIFFERENT |
  | C07 | the sidecar payload differs | DIFFERENT |
  | C08 | elements npz not matching its digests | DIFFERENT |
  | C09 | a missing column | NOT_READY |
  | C10 | iteration 1 absent on the twin | NOT_READY |
  | C11 | the twin ran the serial solver | DIFFERENT |
  | C12 | no `--column-workers 8` | DIFFERENT |
  | C13 | controls differ | DIFFERENT |
  | C14 | the caller differs beyond paths | DIFFERENT |
  | C15 | a record failing integrity | REFUSED |
  | C16 | a FAILURE record | DIFFERENT |
  | C17 | a corrupted blob | DIFFERENT |
  | C18 | a run's call_spec not its pin | DIFFERENT |
  | C19 | a `uvt_` run path | REFUSED |
  | C20 | specs differing outside the leaf | REFUSED |

**UNTESTED.** The first real pair, which the test itself decides. The synthetic trees follow the checkpoint module's record format and the controller's sidecar format, both read from bytes. If a real run tree lacks a file the tool expects, the result is REFUSED or NOT_READY, because every compared file must exist and pass its own integrity check on both sides. The files the tool does not compare are listed above.
