# apply_h3_fields_c2v006: README and CHANGES (V006 A222 under E_A220_1)

Claude2 builder for root (V006 A222, being written). Stamp (`date -u` before writing): Tue Oct 20 17:34:27 UTC 2026 (12:34 CDT).
Folder: `h3_campaign_path_c2/apply_fields_c2v006/`. It is new (created by `mkdir`, which fails if it exists); nothing outside it was edited.
Labels: TESTED (a recorded run, rows cited) and FORMAL (from the code, lines cited).

## Files

| File | sha256 |
|---|---|
| `apply_h3_fields_c2v006.py` (the tool) | `0ed72837684f345b311401ea90b9889cd46b8431753a4e0697225e9849aff951` |
| `tests/test_apply_h3_fields_c2v006.py` | `8ed6f753400173931e41b91d1ae22837eb1eaeaffe43a3f93e0f3d75affc4103` |
| `tests/mutation_check_c2v006.py` | `c60a0b1a20591476b3c2e97d62be4c48725871023142f5de4c0f42a531659ec3` |
| `DIFF_apply_h3_fields_c2v005__c2v006.diff` | `b1902093c94947e2cd61a00cfaa0fab3ed215e584e81092f74fb45d22092eda9` |
| `DIFF_test_apply_h3_fields_c2v005__c2v006.diff` | `2315d82bd751b612158baaa97598404d84909cd6f43f545c419190002501ad35` |
| `DIFF_mutation_check_c2v005__c2v006.diff` | `df0f9673ea27cb621048d469f98dbaa819a112d8b2bb7cdd33cd7a81be6baafc` |
| test run 1 `test_runs/RUN_20261020T172857Z_4860/TEST_RESULTS.json` | `1152d3167efc407ec25da898d033c7ea6e518969854de837239529a20efb0f8e` |
| test run 2 `test_runs/RUN_20261020T173040Z_5661/TEST_RESULTS.json` | `852881030fa5f6b137debab0eea1855c7f5b26e9319c97700778289a69265941` |
| mutation `mutation_runs/RUN_20261020T173226Z_6462/MUTATION_RESULTS.json` | `932e49a6ab55ff26f77fb7f34976a4b06b3e6c386b607183f963e44fd5bfc566` |

`HASHES_APPLY_FIELDS_C2V006.txt` lists every other file in the folder, computed from bytes.
Base: c2v005 `apply_h3_fields_c2v005.py` `6c6c6d085a3b58dcb6933f50f5ebff279509e8e09b49833cf783516200b5fa3a` (pinned in the tests; Z01 re-hashes it).

## The sweep of c2v005 (every place a pinned file is hashed and read again)

Line numbers are c2v005's. The module reads files at only three places:
- `pin_problem` L146 (one read; it hashes and returns a message, never a buffer);
- `block_derived` L230;
- `main` L360-361 (the predecessor, the delta and the seal record).

Pin checks are made at L157 (every `PIN_PATHS` field), L162 (approved producers), L170-171 (`source_results`), L197 (report and compare) and L204 (prereg).

| # | Path | Reads | Class | c2v006 |
|---|---|---|---|---|
| D1 | `seal_derived`: L197 `pin_problem(rp)` hashes report read 1. L202 `json.loads(Path(rp['path']).read_bytes())` parses report read 2. Its `prereg` (L203) is written into `numerics.sealed_prereg` (L208). | report ×3 (L197; L202; then L282→L157, the `verdict_artifact` re-check) | **hash, then parse another read** | **FIXED** |
| D2 | `value_problems`, `numerics.source_results`: L170 `pin_problem(x['result'])` decides. When it fails, L171 calls `pin_problem(x['result'])` again for the refusal text. | result pin ×2 when failing | **hash, then hash again for the output text** (nothing parsed; the refusal stands, but its text can come from a read that did not decide, e.g. `... .result: None`) | **FIXED** |
| K1 | `numerics.block_source` set by the delta: L282→L157 field check (hash only), then L289→L230 `block_derived` (hash L233 and parse L239 of the same buffer). This is the double read c2v005 disclosed. | ×2 | hash-only re-check | KEPT (below) |
| K2 | The report, after D1's fix: `seal_derived`'s one read (hashed and parsed), then L282→L157 re-checks `numerics.verdict_artifact` (hash only). | ×2 | hash-only re-check | KEPT |
| K3 | The compare file: L197 `pin_problem(cp)`, then L282→L157 `numerics.compare`. Both hash only; the file is never parsed. | ×2 | hash-only re-check | KEPT |
| K4 | The prereg file: L204 `pin_problem(pre, extra_keys_ok=True)`, then L282→L157 `numerics.sealed_prereg`. Both hash only; the file is never parsed. | ×2 | hash-only re-check | KEPT |

These were already compliant:
- **The seal record:** one read (L361), hashed (L191) and parsed (L193) from the same buffer.
- **`block_derived`:** fixed by c2v005, L230/L233/L239.
- **Every other pin field, and each approved producer:** one hash-only read per field (L157, L162); nothing is parsed.
- **Not pins:** the predecessor is read once (L360), parsed (L261) and its sha reported (L319) from the same bytes. The delta is not pinned.
- **One file pinned by two fields:** each field's check is its own hash-only read. This is K-class.

X07 runs this sweep as a static detector over the whole module (TESTED). It flags D1 and D2 on c2v003 and c2v005. On c2v004 it also flags `block_derived`. On c2v006 it flags nothing.

## The change (`DIFF_apply_h3_fields_c2v005__c2v006.diff`; c2v006 line numbers)

- **New `pin_read(v, extra_keys_ok=False)` (L169-184):** it applies `pin_problem`'s checks and messages, in `pin_problem`'s order, to ONE read (L179). It returns `(None, raw)` when `sha_b(raw)` equals the pin (L182), and otherwise `(problem, None)`.
- **D1, `seal_derived`:** L233 `rp_bad, rp_raw = pin_read(rp)` is the one read of the report. L234 `reasons = [x for x in (rp_bad, pin_problem(cp)) if x]` keeps the same order and the same messages. L239 `rep = json.loads(rp_raw)` parses the buffer that was hashed. The `prereg` written at L245 comes from that buffer.
- **D2, `value_problems`:** L204-205 `elif (bad := pin_problem(x['result'])): out.append('%s[%d].result: %s' % (p, i, bad))`. One read decides and gives the text.

Everything else is AST-identical to c2v005:
- `pin_problem`, `block_derived`, `strip_slots`, `apply`, `main` and every constant are unchanged (X06).
- Only `<docstring>`, `value_problems` (its `source_results` branch only) and `seal_derived` (exactly two edited statements plus the `pin_read` assignment) differ (X06).
- Against c2v003, `value_problems` and `seal_derived` are the only changed functions, and their c2v005 forms equal c2v003's (X01).

Refusal texts are identical whenever no file changes between reads. TESTED by:
- X02: c2v003 on 66 inputs, now including 22 seal-record branch records and 13 `source_results` branches;
- X08: c2v005 on all 92 apply calls (66 plain and 26 with `--block-source`; 31 written, 61 refused);
- X05: c2v004 on the 26 block calls;
- X09: the 5 branches that raise (a pinned report that is not JSON or is a list, a tuple that is not an object, a seal record that is not an object or not JSON) raise the same exception and message in c2v003, c2v005 and c2v006.

## K1-K4: kept, with the reasons

FORMAL and TESTED:
- **Each is one read, hashed against the pin, with nothing parsed from it or written from it.** That is the A222 pattern with no parse step.
- **A change on either read refuses; none can accept unhashed bytes:**
  - K1: R4b, both orders, exact reasons;
  - K2: S2;
  - K3 and K4: S4b. Read 1 changed gives the `seal_derived` text; read 2 changed gives `numerics.compare` / `numerics.sealed_prereg: sha256 differs from the file bytes`.
- **They are never parsed (by identity):**
  - K1: R4a `parsed_read_indices == [2]` (only the derivation's buffer);
  - K2: S1 `[1]` (only `pin_read`'s buffer);
  - K3 and K4: S4a `[]`.
- **They are `value_problems`' c2v003 contract for any pin field set by a delta or derived from the seal record.** The check runs the same with or without `--block-source` / `--seal-record`, and it independently checks the field value that is written into the config. Folding it into the derivation's read would change `value_problems` / `apply` for every path, including the no-flag path that X02 holds byte-equal to c2v003. It would remove a check and fix no gap.
- **The only buffers of a pinned file that c2v006 parses** are `block_derived`'s one read and `seal_derived`'s one report read (X06, X07, R2a, S1).

## Tests and checks (record runs, cwd = this folder, the codex python `-I -B`)

**Suite, two record runs:**
- Both 64/64 (MUST_PASS 38, MUST_FAIL 25, INFO 1), with 0 audit denials. The only subprocess was the pinned python (2). Wall 99 s and 102 s.
- All 50 c2v005 rows are carried with the same ids and expectations. X01 and X04 now also name the A222 sites as the only other AST differences.
- 14 rows are new: S0-S3, S4a, S4b, V0-V2, Y01, X06-X09.

**C rows (the c2v003 suites with c2v006 swapped in):**
- `test_campaign_cert_c2v004` `52d04202`: 90/90.
- `test_campaign_cert_c2v003` `6fd12500`: 77/77.
- In both runs every row (id, expectation, pass) equals its record run. The suites' inputs name `apply_h3_fields_c2v006.py` `0ed72837` and none of c2v003, c2v004 or c2v005.

**Mutation (`--skip-suites`): 18/18 caught.**
- M1-M12 are c2v005's, with byte-identical anchors.
- New:

| Mutant | Reintroduces / removes | Caught by |
|---|---|---|
| M13 | D1: `seal_derived` parses a second `Path(rp['path']).read_bytes()` | S1, S2, X06, X07 |
| M14 | D1 through builtin `open()` (not seen by the fixture's Path) | S1, S2, X06, X07 |
| M18 | D1 shape with c2v006 names (`pin_problem(rp)`, then read) | S1, S2, X06, X07 |
| M15 | D2: second `pin_problem(x['result'])` for the text | X01, V1, X04, X06, X07 |
| M16 | `pin_read` without its sha comparison | S3, Y01, X02, X06, X08 |
| M17 | `pin_read` hashes one read and returns a second | S1, S2, Y01, X06 |

**New rows:** each runs on the REAL v004a. The seal world (report, prereg, compare) is synthetic and written in the run dir. The read-changing fixture is a `Path` subclass in the tool instance that counts reads and swaps bytes. The audit hook keeps an independent `open` count.

| Row | Expect | What it shows |
|---|---|---|
| S0 | MUST_PASS (control) | On c2v005, 3 report reads. Read 2 is the one parsed. Its unhashed `prereg`, an extra key or the same bytes at another path, is written into `numerics.sealed_prereg` under the original `verdict_artifact` pin. |
| S1 | MUST_PASS | c2v006 honest, two deltas and the CLI. 2 report reads on both counters. Read 1 is the only report buffer parsed (the same object). The bytes and report equal c2v005's. `sealed_prereg` is read 1's `prereg`. |
| S2 | MUST_FAIL | Read 2 (or every read after read 1) returns the unhashed key, another path, another field, non-JSON or OSError. c2v006 refuses with `numerics.verdict_artifact: sha256 differs from the file bytes` (or `unreadable: …`) and parses only read 1. The CLI exits 2 and writes nothing. |
| S3 | MUST_FAIL | If the one read already differs or fails, c2v006 refuses with c2v005's exact text, after 1 read, and parses nothing. |
| S4a / S4b | MUST_PASS / MUST_FAIL | K3 and K4: compare and prereg are read twice, hash only, never parsed. A change on either read refuses with the exact reason. |
| V0 | MUST_PASS (control) | On c2v005, a failing result pin is read twice and the text comes from read 2 (`... .result: None`). |
| V1 | MUST_FAIL | c2v006 reads it once, and the text comes from the deciding read. |
| V2 | MUST_PASS | Honest, 2 pins: one read each. Bytes equal c2v005's. A changed later read cannot matter, because none occurs. |
| Y01 | MUST_PASS | `pin_read(v,k)[0] == pin_problem(v,k)` on 15 cases × 2 values of `extra_keys_ok`. On success the buffer is the file's bytes, from exactly one read. |
| X06 | MUST_PASS | AST against c2v005, as described in "The change". |
| X07 | MUST_PASS | The sweep detector, as described in "The sweep". |
| X08 | MUST_PASS | Parity with c2v005 on all 92 apply calls. |
| X09 | MUST_PASS | Parity on the 5 seal branches that raise. |

## Use (unchanged except the tool name)

Wherever c2v005 is named (README V3, V4, the H1 §5 block line), read `$H3/apply_fields_c2v006/apply_h3_fields_c2v006.py`. The arguments and the expected report values are c2v005's.

## Disclosures

- **Working directory:** the record runs and every mutant's suite ran with cwd = this folder (under `claude_artifacts`). c2v005 used `/tmp`. Writes stay inside each run dir; the audit hook enforces this and Z90 checks it.
- **`dev_runs/`:**
  - one suite run without the suites (62/62);
  - `MUT_DEV1`, a copy of the package run through the mutation check (18/18).
  - Both used the published bytes (`0ed72837` / `8ed6f753` / `c60a0b1a`). They are not the record.
- **Unchanged, not in scope:** a pinned report that is not JSON or not an object still raises instead of refusing (c2v003 behavior; X09). On the CLI this means a traceback, exit 1 and nothing written. It is not a provenance gap: nothing is accepted.
- **Not opened:** no NGC3198 file, step-2 run output, `V007_POSTSEAL_RECORDS` or `~/.codex`, as the audit checks. There was no network use. Reads outside this folder were read-only: the c2v005 folder (tool, tests, README, probe, and a grep of its verifier's check script), the pinned inputs through the tests, and `test_campaign_cert_c2v004.py`, viewed for its APPLY use.
- **UNTESTED:** everything A220 and c2v005 list (real r5 `prelaunch_check` on the FILLED base, the final W1/H1 configs, production bind/launch). Also untested here is the real root-filled seal record: only synthetic seal records were used. The deciding test is the first real `--seal-record` apply at the verdict. The written `numerics.verdict_artifact.sha256` must equal sha256 of the root-filled report's bytes, and `numerics.sealed_prereg` must equal that report's `prereg` object.
