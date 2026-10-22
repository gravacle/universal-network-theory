# values_writer_c2v003: the values / members writer (V006 A152)

Root build (Claude2 workflow), written 2026-10-19T17:52:08Z (`date -u` immediately before writing). **Nothing here is adopted.** Claude4 reviews it (lean, per A152). Labels: **TESTED**, **FORMAL**, **UNTESTED** (with its deciding test).

## 1. What v003 changes against v002 (`38ac8c93`), and only this

1. **ROOT_RULING is pinned to A152**: `{path: V006 addendum, section: 'A152', sha256: 5aee4cc0f3ae64e5ea630d5a6459fdccc4cf2e3d55061d57e9214b1f002b074f}`.
   - The sha covers the section bytes only: from the line `## A152` to the byte before the next line starting `## ` (3,628 bytes). The whole file is not pinned because root appends to it.
   - `check_root_ruling()` re-reads the bytes before every `attach_eps`, `assemble` and CLI run. A changed section, a missing file, or a duplicate heading refuses.
   - TESTED: the V006 file sha changed during this build (`ee99b4bf` at the start, `182b2e88` at 17:50:59Z), and the A152 pin still verifies.
2. **The W-3 assembler**, `assemble(kind, query_ids, points)` and CLI `assemble`. Per point, it reads the call's own `out/result.json` and `out/finish.json`, the acceptance record, and the query ids. It then builds the `PHASE1_NGC_VALUES_C2V001` document and attaches `eps_km_s` through `attach_eps`, one W-1 point record per point.
   - Phase 1: roles `u_A`, `F0`, `F1`, `F2`.
   - Phase 2: members with `log_index`.
3. **W-3 eps rows.** A row with speed None, or with v ≤ 0, gets eps None and keeps the call's reason. A call with no final rows gets 43 None, with its status and reasons.

Unchanged from v002: W-1 (srb_rot on the own state, certificate and `rotation_rows`), C-1 to C-10, W-2, and W-4/C-8.

## 2. W-3 as built

| Field | Rule | Source |
|---|---|---|
| `speeds_km_s` | `result.rows` in `query_ids` order. It must equal the call's row order; nothing is reordered. `result.speeds_km_s` (driver L6074) must agree with the rows. | C-7 |
| `valid[q]` | row valid ∧ `result.valid` ∧ status COMPLETED | W-3 |
| `member_valid` | `result.valid` ∧ COMPLETED ∧ acceptance reading ∈ {ACCEPTED, LO_UNCERTIFIED_TRANSIENT} | W-3 |
| `result_pin` | `{resolved out/result.json, finish.result_sha256}`. `finish.result_sha256` must equal the sha of the bytes read, and `finish.result_path` must resolve to the same file. | A138 V01(b) |

Each point also carries print-only custody: `call` (status, `result_valid`, finish pin, spec sha, driver sha) and `acceptance` (record pin, reading, handoff pin). The document carries `assembly` (writer pin, ruling, manifest cross-check, record shas). The consumer ignores extra keys (TESTED: T31a, T32a).

## 3. Builder choices (new in v003; C-1 to C-10 as adopted)

| # | Choice | Note |
|---|---|---|
| C-11 | **The acceptance record** is the `acceptance_handoff_c2v004` record. Its schema is `DDO154_TAIL_ACCEPTANCE_RECORD_C2V001` (L50), and its `handoff` pin must be `5ff464cc` (A151). It is bound to the call by `result` == this result pin (L368-369) and `call_dir` (L344). The reading must be one of the 7 handoff READINGS (L78-85). | The NGC acceptance record has not been built (A136 G1-G5). A successor handoff or an NGC record schema needs a writer successor. |
| C-12 | `member_valid` counts **only** ACCEPTED and LO_UNCERTIFIED_TRANSIENT. ACCEPTED_PASS_FLAGGED reads false. | W-3 literal, the stricter reading (A48). **O-1** |
| C-13 | **Phase-1 points:** acceptance is optional and printed only. `valid[q]` is not gated by it. | W-3 names acceptance only in `member_valid`. **O-2** |
| C-14 | **Final rows** = `result.rows`, for any status. If the call has no rows: speeds 43 None, `valid` 43 false, eps 43 None (`CALL_HAS_NO_FINAL_ROWS`, with status and reasons). COMPLETED without rows is refused. | Driver L6073: rows are written only when the final column mean is complete. |
| C-15 | **v ≤ 0** has two cases. (a) A valid row with speed ≤ 0 gets eps None (`ROW_SPEED_NONPOSITIVE_IN_CALL`); its `valid[q]` stays per W-3. (b) If the call records a nonpositive rotation square (COMPLETED_INVALID, driver L5939/L6082), all 43 eps are None with the call's reason. If the record and the arrays disagree, it is refused. | This replaces v002's refusal (v002 T16). |
| C-16 | **Status invariant:** COMPLETED ⇒ valid true, and COMPLETED_INVALID ⇒ valid false (driver L6099); otherwise refused. Any status outside the driver's 7 is refused. Finish and result must agree on status and valid. | |
| C-17 | **Manifest cross-check** (`a2936517`, ids and `Rad_text` only): the order must be exact. Radii must agree within a relative 1e-9, for every row `radius_m` present and every support radius. | Radius rule `float(Rad_text) * KPC_M` (driver L5215, L183). The tolerance is a cross-check only; the radii fed are the call's own (C-1). |
| C-18 | **Phase 1** is exactly `u_A`, `F0`, `F1`, `F2` with no `log_index`. **Members** have role `member`, a distinct int `log_index` ≥ 0, and distinct θ keys. | The θ-key uniqueness is inherited from v002 `attach_eps`. |
| C-19 | A row without a `valid` key but with a finite speed counts as row-valid. | Driver c2v005 rule, as in v002. |
| C-20 | CLI `assemble` writes each point record, then the values document, all by exclusive create. | |

## 4. Open items for root (each is a reading, not a computation)

- **O-1.** ACCEPTED_PASS_FLAGGED in `member_valid`. Built as false.
- **O-2.** A134 Q2 says "before any value is used". Should Phase-1 `valid[q]` also require an accepted reading? Built as no, the W-3 literal.
- **O-3.** A-4, the sin(i_phys)/sin(i_released) factor. A152 does not name it (TESTED: `A-4` is absent from the section). W-1 "adds no new knob", so the factor stays printed and not applied.

## 5. Dependencies (UNTESTED; each with its deciding test)

- **D-1** (from v002): the reconstructed `le{final_pass}_rotation` TailState must reproduce `finish.uv_tail.state_digest`. Deciding test: the first real S0 call.
- **D-2** (from v002): certificates for every point other than the 4 S0 θ. Deciding test: each one passes C-8.
- **D-3** (from v002): a driver successor needs a writer successor.
- **D-4**: the NGC acceptance record must be in the C-11 form. Deciding test: the first real NGC `accept_call` record passes `check_acceptance`.
- **D-5**: if a call was launched with a relative `--outdir`, `finish.result_path` is relative, and v003 refuses it (FINISH_RESULT_PATH; fail-closed). Deciding test: the first real S0 `finish.json`.
- **D-6**: the real column-mean `radius_m` must match the manifest within 1e-9. Deciding test: the first real S0 assemble.

## 6. Tests (synthetic values only)

- **Record runs.** `test_values_writer_c2v003.py` under `python3 -I -B` (codex runtime 3.12.14, numpy 2.3.5): **226/226 in both record runs** (`test_runs_v003/run1`, `run2`), with identical outcome lists. Consumers: phase1_c2v003 (`149ed4cb`) and v003a (`385b287c`).
- **Ported from v002: 123.** 120 keep their v002 names; the fixtures now also write the driver's `out/finish.json`. 3 were renamed:
  - T16, a W-3 change: nonpositive rotation now gives 43 None instead of a refusal;
  - T17, which sets ROOT_RULING to None in-process;
  - T20, which runs the CLI gate on a module copy with the pin removed.
- **New: 103.**
  - T30: the A152 pin, an independent extraction, 9 synthetic ruling cases and 9 A152 text checks.
  - T31: Phase-1 MUST_PASS through `check_values` on v003 and v003a.
  - T32: Phase-2 MUST_PASS through `members_values` and `check_member_eps` on both; all 7 readings plus no record; at0b re-bind.
  - T33: order MUST_FAIL.
  - T34: status and call-valid flags and refusals.
  - T35: acceptance MUST_FAIL.
  - T36: finish MUST_FAIL.
  - T37: speed None and v ≤ 0.
  - T38: rotation positivity.
  - T39: manifest, including the real manifest's sha and order.
  - T40: assemble inputs.
  - T41: the post-attach guard.
  - T42: CLI end-to-end.
  - T43: driver and handoff line evidence.
  - T44: consumer AST identity v003 = v003a.
- **Mutation** (`mutation_values_writer_c2v003.py`): **44/44 killed**. These are v002's 16, re-targeted, plus 28 new. Three equivalent mutants survive, as expected, and are reported:
  - E01, E02: the `result.valid` conjunct is implied by the C-16 invariant;
  - E03: the call_outputs order check duplicates the check in `final_rows`.

## 7. Reads and deviations (disclosed)

- **Real reads, all read-only:**
  - V006: the A152 pin and line evidence;
  - the 4 S0 EPS and 6 refused records (v002 tests);
  - the target-free query manifest: sha, query ids and `Rad_text` only, never printed;
  - the driver, the SRB adapter, the library v002/v003, the rotation stage and the row producer: line evidence, as in v002;
  - phase1_c2v003 and v003a (consumers), plus the orchestrator they pin (`ORCH_PIN`, loaded through `mod('O')` for `theta_key` only).
- **One file found by listing.** `acceptance_handoff_c2v004.py` (`5ff464cc`) was found by a non-recursive `ls` of `s4_acceptance_c2/acceptance_q2/`, the directory named in A145 and A151. It is identified by its A151 sha and read for its record schema, READINGS and the result/call_dir binding.
- No run tree, `~/.codex`, `c5h_hull_c2/`, UVT_* or NGC3198 target/observed/slots file was opened. No recursive grep or find was run.
- Drafts and development runs were made in the session scratchpad. The published files were created here by exclusive create, with shas verified after the copy. v002 files were not touched (v002 `38ac8c93` re-verified).
- HASHES_V003 lists the published files and the three results records. The synthetic fixture trees under `test_runs_v003/` can be regenerated from the test file.

## 8. Files

See `HASHES_V003.txt`.
- `values_writer_c2v003.py` `dd9456bc`
- tests `70001d1f`
- mutation `5f1ccb9f`
- results: run1 `5634dd2a`, run2 `93d0ba96`, mutation `e498a3e3`
