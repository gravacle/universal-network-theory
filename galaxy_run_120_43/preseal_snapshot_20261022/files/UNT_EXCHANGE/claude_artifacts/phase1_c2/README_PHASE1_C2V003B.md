# phase1_c2v003b: the A133 Phase-1 tool, values-custody successor of v003a

**Labels.** TESTED = run here on synthetic fixtures, with the result shown. FORMAL = follows from the cited code or text. UNTESTED = not run; the deciding test is named.

**Text of record.**
- Root's v003b commission (one change: AT-0b's values custody). No addendum entry names v003b yet; A149 (V006 addendum) is the latest Phase-1 ruling.
- The v003a verifier's probe `p1v003a_verify/probes/values_unbound_attack.py` (session scratchpad): AT-0b's `--values` file was not bound to the values file the L1 was banded from.
- Base: `phase1_c2v003a.py` (`385b287c`), `test_phase1_c2v003a.py` (`5354d7d8`), `README_PHASE1_C2V003A.md` (`f85eec92`).

**Scope.** v003b changes `phase1_c2v003a.py` at four sites: the docstring (a new header above v003a's, which is kept whole), MODULE, `cmd_at0b` (one statement inserted) and `cmd_at1` (two statements inserted). Everything else is AST-identical to v003a (TESTED, T45). L1 bytes are v003a's except `module` (TESTED, R01 band). v001-v003a files are untouched (T00, T43 and T45 re-hash them in every run). No production run was made. No campaign, cache, run tree, C5H, `UVT_*` path or NGC3198 target was opened.

## Files (all new, created exclusively)

| File | sha256 | Role |
|---|---|---|
| `phase1_c2v003b.py` | `7d891ff7` | The tool. Same commands, arguments, exit codes, schema strings and output file names as v003a. |
| `test_phase1_c2v003b.py` | `c24a7976` | 168 checks: 159 ported from v003a (96 part 1, 9 part 2, 37 part 3, 17 part 4) and 9 new (part 5). 68 MUST_FAIL, 100 MUST_PASS. |
| `DIFF_PHASE1_C2V003A_TO_V003B.diff` | `fd095be9` | Unified diff of the tool (+19 / -2 lines). |
| `DIFF_TEST_PHASE1_C2V003A_TO_V003B.diff` | `d03525a1` | Unified diff of the tests (+350 / -93 lines). |
| `test_runs_v003b/RUN_20261019T175548Z_11222/`, `test_runs_v003b/RUN_20261019T175703Z_18731/` | RESULTS `b6f5a245`, `d30c623f` | The two record runs, each 168/168, with the same ids and results. Each holds `RESULTS.json` and `SHADOW_REGRESSION_V003A_V003B.json` (`5b5aeeba`, `419614ca`). |
| `test_runs_v003b/MUTATION_20261019T175829Z_27393/` | MUTATION_RESULTS `a4ba5da7`; driver `e46f3ccf` | Mutation run: 27/27 killed. Holds `MUTATION_RESULTS.json` and a copy of its driver, `mutation_phase1_c2v003b.py`. |
| `README_PHASE1_C2V003B.md` | in HASHES_V003B | This file. |
| `HASHES_V003B.txt` | not self-listed | sha256 of each object above, from its bytes, plus the v001-v003a objects, unchanged. |

**Pins.** Unchanged from v003a: orchestrator `c75a889f`, engine `6ec8b2d0`, freeze v003g `48a1e48a`, KMAX `dbddc02c`.

**Usage.** As in v003a, with `phase1_c2v003b.py`. No argument was added or removed. One input rule is new: `agree at0b --values` must be the Phase-1 values file that `band` read for the L1 that `agree at1 --l1` names.

## The change

- **V1.** `agree at0b` writes `values_sha256`: the `--values-sha256` it verified against the values bytes, lowercased. It sits beside `members_sha256` (A149 item 2).
- **V2.** `agree at1` refuses VALUES, with no out-dir, unless AT-0b's `values_sha256` equals the L1's `values_sha256`. Both are lowercased before the compare, and both must be strings. The check runs right after the A149 item 2 members check and before `members_values`.
- **Custody.** at1 accepts only an L1 whose module is `phase1_c2v003b`.

What the chain now binds (FORMAL): band writes L1.`values_sha256` = the sha of the values it read (unchanged since v001). AT-0b records the sha of the values it read (V1). at1 requires the two to match (V2), and its `--members` sha to match AT-0b's `members_sha256` (A149 item 2). So AT-0b's u_A re-bind test is made on the values file the L1 was banded from, against the members file at1 reads.

## TESTED (T44, both record runs)

| Case | v003b | v003a on the same inputs |
|---|---|---|
| **The verifier's values-unbound attack.** VALUES_C1 and MEMBERS_C1 with the u_A `result_pin` changed to one other file in both. AT-0b on them reads PASS (rc 0). at1 then runs on the L1 of the unmodified VALUES_C1. | REFUSED VALUES, no out-dir | rc 0, COVERED |
| AT-0b without `values_sha256`: v003a-written, key deleted, or null | REFUSED VALUES, no out-dir (all 3) | not run |
| Control: the same AT-0b (AT0B_C1) with `values_sha256` | rc 0, COVERED | not run |
| An honest AT-0b of another values file (AT0B_C1 on L1_Q1, and AT0B_Q1 on L1_C1), with the members custody satisfied | REFUSED VALUES, no out-dir (both) | not run |
| **Honest chain:** values, band, at0b, at1 (seed, nonlinear toy, ε varying per member and row) | rc 0, SUPERSEDED, 301 pairs | shadowed. band and at1 are identical except `module`; at0b differs only in `module` and `values_sha256` |
| Case: band and at0b given an uppercase `--values-sha256` (the L1 records it uppercase, AT-0b lowercase) | rc 0; AT1 byte-identical to the honest chain's | not run |

Also TESTED (T44 (a)): all 5 part-1 AT-0b files record the sha of the `--values` bytes they read.

## Tests (TESTED; 2 identical record runs: 168/168, MUST_FAIL 68/68, MUST_PASS 100/100, audit denials 0, 64 shadow calls each)

**Ported, 159 checks, in v003a's order.**
- **Ids.** 8 of the 9 R01 ids name the reference, so they now name v003a. `R01.no_other_command...` keeps its id. Every other id is v003a's. Ids that name v003 or v003a as the module under test are kept for continuity, for example T42's "v003a reads 10**400" and T41's "by_ulps" (see the wording corrections below).
- **Port changes:**
  - T00, T33, T37 (a) and T43 read module `phase1_c2v003b`.
  - Part 1 is shadow-run with v003a instead of v003. v003a's at1 reads the L1 that v003a's own band shadow wrote (`<L1 dir>.V003A_SHADOW`). This is the substitution v003a's suite made for v003.
  - **T23.** at1 with the defect AT-0b (AT0B_NOREBIND, which read VALUES_LINEAR) now reads L1_LINEAR, the L1 of that values file, instead of L1_C1. The members file is still MEMBERS_NOREBIND. It reads AGREEMENT_DEFECT, rc 10, with 294 failing pairs. v003a's form is now REFUSED VALUES (T44 (d) covers that refusal).
  - **T37 (b)-(d) and T43.** They read a v003-written L1 and AT-0b. These now come from v003's band and at0b, run directly on the same inputs (`L1_C1_V003`, `L1_Q1_V003`, `AT0B_C1_V003`). Part 1 no longer writes v003 shadow directories.
  - **T42** is still shadowed against v003. Its at0b also declares `values_sha256`.
  - T35's declared node lists against v002 are unchanged, because v003b changes the same nodes.

**New, 9 checks (part 5).**
- T44: six checks (a)-(f), as above.
- T45 (a): v003a's tool, tests, README, HASHES, DIFFs, record RESULTS, SHADOW files, MUTATION_RESULTS and mutation driver are untouched (sha256 from bytes).
- T45 (b): at1 refuses a v003a-written L1 (custody), with no out-dir.
- T45 (c): the AST scope against v003a. Only `<docstring>`, MODULE, `cmd_at0b` and `cmd_at1` changed, and nothing was added or removed. In `cmd_at0b` and `cmd_at1`, the only change is 1 and 2 statements inserted right after the `members_sha256` statement. v003b's docstring ends with v003a's docstring, whole.

## Declared differences against v003a (TESTED, both record runs)

| Command | Calls | Result |
|---|---|---|
| snapshot | 20 | identical up to tool identity and the engine record's volatile fields |
| fdplan | 8 | identical except `module` |
| handoff | 12 | identical except `module` |
| band | 6 | identical except `module` (the L1 bytes) |
| at0a | 9 | identical except `module` |
| at0b | 5 | identical except `module` and the new `values_sha256`, which equals the `--values` file's sha in all 5 |
| at1 | 4 | identical except `module`, including `band_region_box_only_extent`. v003a read its own band-shadow L1 in all 4 |

The four at1 fixtures give the same outcomes and identical failing lists: C1 COVERED (0 pairs), Q1 SUPERSEDED (301), DEFECT AGREEMENT_DEFECT (294, after the T23 port), CORNER SUPERSEDED (320). Nothing else differs.

## Mutation run (TESTED, 27/27 killed)

- **Ported.** v003a's 25 mutants keep their strings unchanged. v003b only inserts lines, so every site is still present exactly once.
- **New:**
  - **B01, the at1 values check disabled.** Killed by T44 (b), (c) and (d).
  - **B02, at0b recording no `values_sha256`.** Every at1 is then refused VALUES. The run recorded 141 of 168 checks, and 21 of them failed.
- **Structural kills.** Every v003a-site mutant also fails T45's AST scope. That kill is structural: each mutant also has at least one behavioural killing check, as listed in `MUTATION_RESULTS.json`.
- **v003's five survivors (X03, X05, X07, X08, X18)** stay killed by T39, T40 and T38.

## Corrections to README_PHASE1_C2V003A.md (wording only; v003a's objects are unchanged)

1. **Ids.** "All v003 ids are kept except the 9 part-2 (R01) ids" should read: **8** of the 9 R01 ids were renamed, the ones that name the reference; `R01.no_other_command...` kept its id.
2. **The T41 tie case.** The nonzero full-region extents (3.96e-15, 4.07e-14, 2.03e-13, 4.05e-13) are **LP feasibility-tolerance vertices**. The engine simplex reaches them through its tolerance E._LP_EPS = 1e-12, which governs the pivot, the reduced cost and the ratio-test ties (engine L181, L1799-1812). This happens near the tiny DDO row. They are not "a few ulps" off 0.0. The same wording appears in three places that this build does not change:
   - FORMAL note 2 of the v003a README;
   - the T41 check id (`..._off_0.0_by_ulps_...`, kept for continuity);
   - the docstring of `band_region_box_only_extent`, kept verbatim for AST identity.
3. **Mutant N03** (at0b without `members_sha256`). Its run **recorded 132 of the 159 checks**, of which 19 failed. The other 27 were not recorded, because their test functions stopped at the first refused at1. In v003b's mutation run, N03 recorded 141 of 168 checks, with 24 failing.

## CHOICES not forced by the commission (for the reviewer)

1. **Where the check sits.** It runs after the A149 members check, so a call with a wrong members file and a wrong values file is refused MEMBERS first. That keeps T37's refusal codes. Before both: the L1 schema, snapshot, fdplan and module checks, all unchanged.
2. **Separate statement.** `res['values_sha256'] = ...` is a new statement. v003a's dict literal is not edited, so its line stays byte-identical and the 25 mutant sites are unchanged. Output files are written with `sort_keys`, so key order does not change the bytes.
3. **Case.** band is AST-frozen and records `--values-sha256` as given. AT-0b records it lowercased, and at1 lowercases both. T44 (f) tests an uppercase L1 value.
4. **Old AT-0b files.** An AT-0b without `values_sha256` (v003a or older), or with a non-string value, is refused by the same check, with no separate code.
5. **Refusal code.** VALUES, the existing code of `check_values`, as the commission names it.
6. **What AT-0b reads is unchanged.** at0b still does not compare its values file with any L1. AT-0b has no L1 input, and the binding is made at at1.
7. **Test ports.** T23 uses the L1 of the defect AT-0b's own values file. The v003-written objects come from v003 run directly. T42 stays against v003.
8. **Mutation driver.** `mutation_phase1_c2v003b.py` is not in the task's file list. It was run from the session scratchpad and copies its own bytes into the MUTATION directory under `test_runs_v003b/`. It is a port of v003a's driver (`2b951584`).

## FORMAL notes

1. **Attack reachability.** The values-unbound case needs an AT-0b run on a values file other than the band's. No forged byte is needed: an operator pairing error between two values files is enough. Root classifies it under A115.
2. **Unchanged custody.** The L1's snapshot and fdplan custody (at1 refuses L1) is unchanged. So is AT-0b's snapshot and Phase-2 record custody: a mismatch reads AGREEMENT_DEFECT through `at0_ok`, not a refusal.
3. **The overflow sites** of v003a's FORMAL note 1 are unchanged. Both still fail closed.

## Process disclosures

- Development and the dev runs were in the session scratchpad: one dev suite run (168/168) and one dev mutation run (27/27). The final tool and tests were copied with exclusive create (`open(..., 'x')`), and their shas were verified against the dev bytes. The record runs and the record mutation run were made from the final location. The DIFFs, this README and HASHES were created exclusively.
- Read beyond the named list:
  - inside `phase1_c2/`: `HASHES_V003A.txt`, v003a's mutation driver and its MUTATION_RESULTS summary;
  - the A149 section of the named V006 addendum, plus a line search on that one file for v003b and `values_sha256` (no hit naming v003b);
  - the verifier probe file.
- Non-recursive `ls` was run on `phase1_c2/`, `test_runs_v003a/` and its MUTATION directory, and on `p1v003a_verify/` and its `probes/`. No recursive grep, find or ls was run.
- Every tool, test and mutation run used `-I -B` with the codex runtime python.

## UNTESTED (deciding test named)

- **M-12.** Classifiers A and B must bind AT0B's new `values_sha256` beside `members_sha256`. Decided by both classifiers on a v003b AT0B/AT1 pair before the seal.
- **Claude3's lean review of v003b.** Nothing here is adopted until it returns.
- **Real ε inputs and the members `eps_km_s` writer** (A148/A152), and **the real campaign and NGC values**, as in v003a.
