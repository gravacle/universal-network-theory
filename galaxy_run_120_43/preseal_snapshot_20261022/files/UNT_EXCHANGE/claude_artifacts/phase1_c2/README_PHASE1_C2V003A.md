# phase1_c2v003a: the A133 Phase-1 tool, A149 successor of v003

**Labels.** TESTED = run here on synthetic fixtures, with the result shown. FORMAL = follows from the cited code or text. UNTESTED = not run; the deciding test is named.

**Text of record.**
- A149 items 1-4 (on top of A144), in `CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md`.
- The two root verifiers of v003 (scratchpad `p1v003_verify_adv/`, including `out/EXTRA_MUTANTS_58693` and `out/AT1_ATTACKS_32483`, and `p1v003_verify_math/`).
- Base: `phase1_c2v003.py` (`149ed4cb`), `test_phase1_c2v003.py` (`331d0212`), `README_PHASE1_C2V003.md` (`52432afe`).

**Scope.** v003a changes `phase1_c2v003.py` at these sites only: the docstring, MODULE, `member_eps` (item 1), `cmd_at0b` (item 2), `cmd_at1` (item 2), `at1_rows` (item 3, one call and one key), and one new helper, `band_region_box_only_extent` (item 3). Everything else is AST-identical to v003, including `band_rows`, `cmd_band`, `linear_model`, `band_region`, `band_region_extent`, `region_violation`, `check_member_eps`, `certificate_maps`, `cmd_handoff`, `members_values` and E_Q_READING (TESTED, T43). L1 bytes are v003's except `module` (TESTED, R01 band). v001-v003 files are untouched (T00 and T43 re-hash them in every run). No production run was made. No campaign, cache, run tree, C5H, `UVT_*` path or NGC3198 target was opened.

## Files (all new, created exclusively)

| File | sha256 | Role |
|---|---|---|
| `phase1_c2v003a.py` | `385b287c` | The tool. Same commands, arguments, exit codes, schema strings and output file names as v003. |
| `test_phase1_c2v003a.py` | `5354d7d8` | 159 checks: 142 ported from v003 (96 part 1, 9 part 2, 37 part 3) and 17 new (part 4, A149). 64 MUST_FAIL, 95 MUST_PASS. |
| `DIFF_PHASE1_C2V003_TO_V003A.diff` | `1870f43b` | Unified diff of the tool (+49 / -7 lines). |
| `DIFF_TEST_PHASE1_C2V003_TO_V003A.diff` | `4d61c6af` | Unified diff of the tests (+524 / -99 lines). |
| `test_runs_v003a/RUN_20261019T170742Z_30680/`, `test_runs_v003a/RUN_20261019T170900Z_36696/` | RESULTS `67222cf6`, `1548dcf8` | The two record runs, each 159/159, with the same ids and results. Each holds `RESULTS.json` and `SHADOW_REGRESSION_V003_V003A.json` (`4f4371cb`, `97b4c63a`). |
| `test_runs_v003a/MUTATION_20261019T171025Z_44245/` | MUTATION_RESULTS `e90b7129`; driver `2b951584` | Mutation run: 25/25 killed. Holds `MUTATION_RESULTS.json` and a copy of its driver, `mutation_phase1_c2v003a.py`. |
| `README_PHASE1_C2V003A.md` | in HASHES_V003A | This file. |
| `HASHES_V003A.txt` | not self-listed | sha256 of each object above, from its bytes, plus the v001-v003 objects, unchanged. |

**Pins.** Unchanged from v003: orchestrator `c75a889f`, engine `6ec8b2d0`, freeze v003g `48a1e48a`, KMAX `dbddc02c`.

**Usage.** As in v003, with `phase1_c2v003a.py`. No argument was added or removed. One input rule is new: `agree at1 --members` must be the file `agree at0b` read (its sha is now recorded in AT0B).

## A149 item 1: the overflow entry

- `member_eps` wraps `math.isfinite(e)` in `try/except OverflowError`. An int entry beyond the float range (10**400, -10**400, 2**1024) reads MEMBER_EPS_NON_FINITE. That pair is flagged MEMBER_POINT_NOISE_NOT_BOUNDED with every bounded term kept, as for inf.
- TESTED (T42): in process (10**400, -10**400, 2**1024 → NON_FINITE; 2**1023 and 10**300 stay finite). Through the CLI, a members file holding the 401-digit int at one (member, row) gives rc 0 with exactly that pair flagged; v003 on the same inputs refused the whole at1 (`INTERNAL_ERROR: OverflowError`, no out-dir). v003a's AT1 file for 10**400 is byte-identical to its AT1 file for an `Infinity` entry at the same pair.

## A149 item 2: the members file custody

- `agree at0b` writes `members_sha256`: the `--members-sha256` it verified against the members bytes (lowercase hex).
- `agree at1` refuses MEMBERS, with no out-dir, unless its `--members-sha256` equals that value. The check runs right after the members file is read and pinned, before `members_values` and the eps contract.
- TESTED (T37): every at0b file records the sha of the members bytes it read (5 files). Refused, with no out-dir: v003's T23 form (the defect AT-0b with another members file), the adversarial verifier's case (the Q1 members file with only the u_A `result_pin` changed after AT-0b), and an AT-0b written by v003 (no `members_sha256`). v003 accepted the first two (rc 10 and rc 0).

## A149 item 3: the box-only extent (print only)

- `reported.band_region_box_only_extent`: per identified c_j, `{direction, extent: [min, max], lp_status: [min, max]}` over the band region's BOX rows alone, by E._lp_max. These are the same rows, objectives and programs the single-point reason reads.
- `band_region_extent`, `band_region_single_point` (still exact, no new tolerance), its reason and every row are unchanged.
- TESTED (T41):
  - The CLI at1 files (corner, seed Q1, CM2, seed R3) print it, equal to an independent box-only computation within 1e-12, and it contains the full-region extent. Corner: `[[0.0, 0.0]]`.
  - **The exact-corner LP-tie case** (the adversarial verifier's A5 construction: u_A = (1, 0, 0.5), V_I ≈ (1, 1, 0)/√2, one DDO row with b_band = tiny). For tiny = 1e-14, 1e-13, 5e-13 and 1e-12, the full-region extent is [0.0, 3.96e-15], [0.0, 4.07e-14], [0.0, 2.03e-13] and [0.0, 4.05e-13] (OPTIMAL), so `band_region_single_point` reads false and the reason null. The box-only extent is exactly [0.0, 0.0] (OPTIMAL) in every case. At tiny = 0 the region is a single point, BOX_CORNER.
  - Injected non-OPTIMAL programs print NOT_AVAILABLE with their status and change no row (MUST_FAIL).
  - On 12 fixtures (T30's six, T31's OTHER_ROWS fixture and the five tie cases), wherever the region is a single point, the reason is BOX_CORNER iff the printed box-only extents are OPTIMAL [0.0, 0.0].

## A149 item 4: the five surviving mutants

| v003 survivor | Killing test (TESTED) |
|---|---|
| region tolerance 1e-9 | T38: an exact-geometry fixture (V = I, DDO row 0 at zero slack, u_A,0 = 0) puts members at violations exactly 5e-13, 1e-12, 1e-12 + 1 ulp, 2e-12 and 1e-10, all computed exactly in floating point. The first two read [] (NGC_NONLINEAR) and the last three LINEAR_DDO. The 1e-10 member kills tolerance 1e-9. |
| region tolerance 1e-13 | T38: the 5e-13 member. |
| `>=` in place of `>` | T38: the member at exactly 1e-12 = E._LP_EPS. |
| eps contract on member_valid = true only | T39: a member_valid false point without `eps_km_s`, or with 42 entries, is refused MEMBERS with no out-dir (at0b PASS on the same file). Control: with a full list it is accepted. |
| scope check by spec sha only | T40: a map pin naming another member by its theta key alone (no spec sha anywhere in it) is refused CERTIFICATE_MAP. So is one naming another member's spec sha alone. Control: a pin naming only its own member's key is accepted. |

**Mutation run (TESTED, 25/25 killed):** v003's 12 mutants, the 8 extra mutants of the v003 adversarial verifier (the 5 survivors plus X01, X10, X19) and 5 mutants of the A149 code (overflow not caught, no members_sha256 check at at1, at0b without members_sha256, box-only over all rows, box-only ignoring LP status). Each of v003's 5 survivors is killed by a behavioural check: X07, X08 and X18 by T38, X03 by T39, X05 by T40. Mutants whose site lies inside a node that is AST-identical to v003 (`band_region`, `region_violation`, `check_member_eps`, `certificate_maps`) also fail T43's scope check; that is a structural kill, and no mutant relies on it alone. N01 is killed by T42 (3 checks), N02 by T37 (3), N03 by 19 checks, N04 by T41 (3) and N05 by T41's non-OPTIMAL check.

## Tests (TESTED; 2 identical record runs: 159/159, MUST_FAIL 64/64, MUST_PASS 95/95, audit denials 0, 64 shadow calls each)

**Ported, 142 checks, in v003's order.** All v003 ids are kept except the 9 part-2 (R01) ids, which now name v003 as the reference. Port changes:
- T00 and T33: the module is `phase1_c2v003a`.
- T23: at1 with the defect AT-0b now passes that AT-0b's own members file (NOREBIND). v003's form is now REFUSED (A149 item 2) and is tested as such in T37.
- T30 (c): v002's corner at1 is run directly (`AT1_CORNER_V002`) instead of being read from v002's part-1 shadow directory.
- T35: the declared AST nodes against v002 add `cmd_at0b` (changed) and `band_region_box_only_extent` (added).
- T36 keeps v002 as its reference (S0, the shared-map handoff and L1 byte-identical to v002 except `module`).

**Part 2 (R01, 9 checks): regression against v003.** Every part-1 CLI call also runs v003 (`149ed4cb`) on the same inputs into the same out-dir path. v003's directory is moved aside to `<out>.V003_SHADOW`.
- **One input substitution, at1 only.** v003's A144 custody reads only a v003-written L1, so v003's at1 reads the L1 that v003's own band shadow wrote (`<L1 dir>.V003_SHADOW`). The band comparison shows those bytes equal to v003a's except `module`.

**Part 4 (17 checks, new): T37-T43** as above. T43 also checks that v003's tool, tests, mutation script, README and HASHES are untouched, that at1 refuses a v003-written L1 (custody `phase1_c2v003a`), and the AST scope against v003.

## Declared differences against v003 (TESTED, both record runs)

| Command | Calls | Result |
|---|---|---|
| snapshot | 20 | identical up to tool identity and the engine record's volatile fields |
| fdplan | 8 | identical except `module` |
| handoff | 12 | identical except `module` |
| band | 6 | identical except `module` (the L1 bytes) |
| at0a | 9 | identical except `module` |
| at0b | 5 | identical except `module` and the new `members_sha256`, which equals the `--members` file's sha in all 5 |
| at1 | 4 | identical except `module` and the new `reported.band_region_box_only_extent`; v003 read its own band-shadow L1 in all 4 |

The four at1 fixtures read the same outcomes and identical failing lists, field by field: C1 COVERED (0 pairs), Q1 SUPERSEDED (301), DEFECT AGREEMENT_DEFECT (516, NOREBIND members after the T23 port), CORNER SUPERSEDED (320).

**The overflow case (T42, shadowed against v003).** v003 refuses `INTERNAL_ERROR: OverflowError`, with no out-dir. v003a writes AT1 with one flagged pair. The band and at0b of the same chain differ only in `module` and `members_sha256`.

Nothing else differs.

## CHOICES not forced by A149 (for the reviewer)

1. **Separate helper.** `band_region_box_only_extent` is a new function. `band_region_extent` is not changed to return the box-only extents, which keeps it AST-identical to v003 and T31's calls unchanged. Its programs are the ones the reason reads; the LP is deterministic, and T41 (d) checks that the two agree. When the region is a single point, the box-only programs run twice (2·m_id extra LPs).
2. **Where the members check sits.** It runs after the members file is read and pinned, and before `members_values` and the A144 eps contract. So a mismatched file is refused for the sha first. The refusal code is MEMBERS.
3. **Case.** at0b records the lowercase `--members-sha256` (`read_pinned` has verified that it equals the bytes' sha), and at1 compares lowercase.
4. **Old AT-0b files.** An AT-0b without `members_sha256` (v003 or older) is refused by the same check (None ≠ sha), with no separate code.
5. **Sign.** -10**400 also reads MEMBER_EPS_NON_FINITE, because the non-finite test comes before the negative test, as for -inf in v003.
6. **E_Q_READING is unchanged.** Its "non-finite" covers ints beyond the float range, which keeps `e_q_reading` byte-identical to v003.
7. **Shadow harness.** v003's at1 shadow reads v003's own band-shadow L1 (above). Without it, v003's at1 cannot run on any v003a input.
8. **Mutation driver.** `mutation_phase1_c2v003a.py` is not in the task's file list. It was run from the session scratchpad and copies its own bytes into the MUTATION directory under `test_runs_v003a/`. It pins nothing.

## FORMAL notes

1. **Other overflow sites, out of A149's scope; both fail closed.** A huge int in a member's `speeds_km_s` (`at1_rows`' validity check), or in the Phase-1 values' speeds or eps (`band_rows`, which is AST-frozen), still raises OverflowError in `math.isfinite`. The CLI turns that into `REFUSED INTERNAL_ERROR` with no out-dir.
2. **The box-only extent says nothing about whether the band is a point.** The single-point rule is exact (A144 R2, A149 item 3): a full-region extent a few ulps off 0.0 reads false, whatever the box-only extent shows.
3. **ε provenance (A149).** at1 still cannot verify where `eps_km_s` came from. That custody is the values writer's (A148).

## Process disclosures

- Development and dev runs were in the session scratchpad. The final files were copied with exclusive create (`open(..., 'x')`), and their shas were verified against the dev bytes. The record runs and the mutation run were made from the final location.
- Read beyond the named list, all inside `phase1_c2/` or the named evidence: `HASHES_V003.txt`, `mutation_phase1_c2v003.py`, and v003's record RESULTS summary. One non-recursive `ls` listed `phase1_c2/` and one level of `test_runs_v003/`.
- No recursive grep, find or ls was run on the artifact tree.
- This README was corrected once in place after its exclusive create and before any hash of it was taken: the fixture count in item 3 read 10; it is 12.
- One dev inspection command ran a non-isolated `python3` with the session scratchpad as its working directory, and it imported an unrelated `enum.py` from there. That file failed on its first statement (AttributeError, before its `open` call), so nothing was read. Every tool, test and mutation run used `-I -B`.

## UNTESTED (deciding test named)

- **M-12.** Classifiers A and B must bind `members_sha256` (AT0B), `band_region_box_only_extent`, and the print-only `e_q_per_member_row` fields. Decided by both classifiers on a v003a AT0B/AT1 pair before the seal.
- **Claude3's lean review of v003a** (A149).
- **Real ε inputs.** The members `eps_km_s` writer (A148). Decided by the first real at1 on its output.
- **The real campaign and NGC values.** As in v003.
