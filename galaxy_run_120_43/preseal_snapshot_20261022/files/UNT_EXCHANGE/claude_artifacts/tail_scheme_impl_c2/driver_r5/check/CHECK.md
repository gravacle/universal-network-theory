# Independent check of driver v010 r5 (A55): PASS_WITH_FINDINGS

driver_r5/check, 2026-10-18. Claude refute-by-default check. I wrote my own scripts and imported none of the builder's tools. Every sha below was computed from bytes.

**Scope.**
- Nothing was launched. The only programs run were dry runs, guard probes and one library build on a saved state.
- Nothing was written outside `check/`, and no existing file was edited.
- I did not read C5H (`runs_ext/KMAX_A2F10_C5H_RUN_V001`) or any NGC target. The only saved state I read is DDO154 C4R3 (`CLAUDE2/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001`).

**Builder shas re-verified from bytes:**

| file | sha256 |
|---|---|
| driver r5 | b5cc62af… |
| module v002 | 2026f2b6… |
| cascade map | a7281e10… |
| spec registry | 8186a16f… |
| BUILD.md | 0c188312… |
| HASHES.txt | afaa1e24… |
| PROOF_CASCADE_R5_V002 | 07ec8e0d… |
| COMPARE_ALL_R5_V004 | a27f226d… |
| COMPARE_NODES_R5_V003 | 4b459ec8… |

All match the build return.

## Results

| item | verdict | evidence |
|---|---|---|
| (a) module successor | **PASS** (TESTED) | See (a) below. |
| (b) cascade is pin-only, and the map is complete | **PASS** (TESTED) | See (b) below. |
| (c) r5 against r4 differs only in pins | **PASS** (TESTED) | 58 changed STRING tokens on 29 lines (294–297, 311, 316–323, 326, 327, 331, 363–370, 373, 374, 376, 379, 380). The line diff equals the token lines, and the token count and types are otherwise identical. |
| (d) B0 reproduction on 3+1 specs | **PASS** (TESTED) | See (d) below. |
| (e) C4T-K256 P128 passes the memory guard | **PASS** (TESTED) | See (e) below. |
| (f) tail-ON numerics are bitwise equal between the r4 and r5 cascades | **PASS** (TESTED) | See (f) below. |

### (a) Module successor

- The two files differ only on line 37: `int(0.6 * 2 ** 30)` becomes `int(8 * 2 ** 30)`, which is 644,245,094 → 8,589,934,592 bytes.
- The byte prefix and suffix around that line are identical, and both files have 897 lines.
- The two AST dumps are identical once the single `TAIL_MEMORY_CAP_BYTES` value is set to a placeholder.
- The guard still reads the name (2 references).

### (b) Cascade proof and map completeness

**Per record, 36 of 36 pass.** For each one:
- The parent and successor token streams have the same length and types.
- Every differing token is a STRING:
  - a sha, which must equal `declared_sha_map[old]`; or
  - a path in the same 2-tuple pin, where the old literal resolves to the map key whose bytes hash to the tuple's old sha, and the new absolute path hashes to the tuple's new sha. This covers the `Path('…')` and `X / '…'` forms.
- The changed lines are exactly the token lines.

**Completeness (own closure over CODE string tokens).**
- I indexed 9,354+ `.py` files under claude_artifacts and FIRST_CONSTRUCTION_REVIEW by sha, with forbidden directories pruned, and followed every 64-hex code string transitively from each driver.
- The r4 closure has 119 distinct shas and the r5 closure has 119.
- The set of r4 files that reach c28d4209 through code pins has 30 distinct shas: the module, the driver and 28 cascade files. Every one is in the map. None is missing, and the map has no extra r4-graph file beyond the 4 declared lane-only route_a uvtail workers.
- The r5 closure contains **no** code pin of any changed old sha, and no old file.
- The r5 closure's sha set **equals** the r4 closure's sha set mapped through the declared map.
- The unchanged files confirm what BUILD says:
  - the facade `191fb7bd`, both RO1 c2v002 bindings, the nodes lib and both solvers pin no re-pinned file;
  - the 46 unresolved shas are all JSON/npz data pins in the driver and stage bases, with none on a `.py` path.
- Code-string mentions of old names are of three kinds, and none loads anything:
  - the `sys.modules` name `unt_owned_uv_tail_lapse_v001_c2`;
  - the module name `uvt_route_b_binding_c2v001` passed to spec_from_file_location, whose path is pinned;
  - a refusal message.

Records: `out/CHK_STATIC_R5_C2V003.json` (8d811141). V001 and V002 are kept as superseded, see the errors register.

### (d) B0 reproduction

**Specs:**
- C4T-K256 FILLED `957e4f56`
- C4T-D5 FILLED `e57ab0ec` (nodes)
- Z2_OFF_RO1 `894e5b3a`
- Z2 `2d5e79d0` (extra)

**Comparator, my own:**
- It canonicalizes **both** sides symmetrically, labelling each declared old/new sha (including the 16- and 12-character prefixes), each path and basename, and the report directory.
- It adds a derived file-hash pair only when the two canonical files are equal (fixpoint).
- Directional guards: the r5 output must contain 0 old tokens, and the r4 output 0 new tokens.

**Result:**
- 4 of 4 counted under B0-EMPTY: both sides exit 0 and both reports are non-empty.
- All 4 are **PASS_PLAN_IDENTICAL**: 14/14/15/16 files, 0 canonical diffs, 0 directional hits.
- The r5 C4T-K256 report has binding_blockers [], pending_certificates [] and executed_stages 0. It pins `2026f2b6` and never `c28d4209`.

Record: `out/CHK_B0_R5_C2V001.json` (32fb7d68).

### (e) Memory guard

**Method.**
- The library is loaded **only through each variant's route-A controller** `load_libraries()`: r4 `51d32e7b` → v001; r5 `c5bdd055` → v002.
- I used the **real C4R3 saved-state roster**, not a synthetic duck, with 72 gas columns.
- A sentinel provider raises at L725, the first statement after the guard.
- The estimate is read by temporarily setting the cap to 0, then restored and checked.

**C4T-K256 (V002 FILLED):**

| eval radii | v001 | v002 |
|---|---|---|
| 72 | REFUSED UV_TAIL_MEMORY_CAP, 0.603 GiB | **PAST_MEMORY_GUARD** |
| 132 | REFUSED, 0.877 GiB | PAST |
| 264 | REFUSED, 1.482 GiB | PAST |

- These estimates reproduce the builder's and Codex1's 0.877 / 0.603 GiB independently.
- C4T K128 and KLO K64: v002 passes on every row.
- K_big 4096: v002 still **REFUSES** (8.63 / 13.03 / 22.69 GiB).

Record: `out/tail_V001/CHK_TAIL_COMPARE_R5_C2V001.json` (04fe2ead).

### (f) Bitwise numerics

**Build.** One real build on the C4R3 saved state:
- the P = 128 C4T FILLED uv_tail block (K_big 128, production certificates EPS_V006 / LO_V002);
- route-A kept cube 4, eval radii = the 72 radial nodes;
- i1t declared 'PASS' by this check, so it is a check build and not a production state;
- about 487 s each, memory estimate 398,567,424 B.

**Comparison:**
- TailState arrays: 12/12 members bitwise equal. `F_ARRAYS.npz` is **byte-identical** (9b801b29 on both sides).
- Jets and lapse pairs at 48 points: 5/5 members bitwise equal.
- Digest 8d4ade2b… equal.
- Record and diagnostics: 221 leaves equal (floats compared by hex), apart from `build_seconds`.

## Findings (none blocking for this lane)

- **N1, BUILD §2 miscount.** It says the closure scan found "26 files". The independent closure finds **28** cascade files plus the driver and the module. The map itself is complete and exact, so this is prose only.
- **N2, M_s 128 specs (A57).** The builder's dry runs used Codex1 registry V002 (M_s 64), as the task asked. Codex1 already has `SPEC_REGISTRY_R5_MS128_CX1V004` and the `*_MS128_R5_CX1V004.FILLED` specs targeting r5 `b5cc62af`.
  - TESTED here: the guard passes for C4T-K256 MS128 V004 under v002, and the estimate does not change with M_s.
  - UNTESTED here: B0 and dry runs of the V004 set. Codex1's `DRY_R5_MS128_V004.json` claims PASS; I did not verify it.
- **N3, compare r6 stale pins (confirmed, outside this lane, already declared).** `v007_compare_c2/r6/kmax_tail_compare_c2v007_r6.py` L126/128/139/141 pin 9f74d465 / d676ecb2 / dbb331db / 5a4c7d41, and L150 pins c28d4209. This blocks comparing r5 runs until a compare successor re-pins them (A56 follow-up 3).
- **N4.** Codex1's `R5_RUNTIME_PINS_V001.json` names the roster and provider at the `driver_r5/module/` sibling copies, while every cascade consumer pins `module/`. They are byte-identical (4366e3d6 / d6c55b55), so this has no effect beyond a path-label difference in custody records.
- **N5, not a defect.** The r5 controllers keep `LIB_MODULE_NAME = 'unt_owned_uv_tail_lapse_v001_c2'`. The registry-conflict check compares realpaths, so v001 and v002 cannot silently co-load in one process.
- **N6, headroom (TESTED as estimates only).** Every P = 128 configuration probed is at most 1.48 GiB at up to 264 radii, under the 8 GiB cap. Under v001, C4T K128 at 264 radii would also have refused (0.811 GiB).
  - Actual production RSS and time at K_big 256 are UNTESTED.
  - So is r5 end to end, and so are the A55 identity reruns on r5, which are root launches.

## Errors register (this check)

1. `chk_static_c2v001.py` read two path-pin forms wrongly:
   - It did not recognise `Path('…')` tuple pins, so it flagged path tokens "not in a pin tuple" on 25 records.
   - It compared closures as multisets, so a duplicate path with the same sha made it read unequal.
   - Successor `chk_static_c2v002.py` fixes both. `c2v003` resolves the should-change set by sha: the review copy `review_tail_module_c4/copies/owned_uv_tail_lapse_v001.py` shares c28d4209's bytes and had shown up as "not in map".
   - The V001 and V002 records are superseded. V003 is the record.
2. A first ad hoc listing of unresolved shas failed on a path-prefix strip bug. It was rerun with full paths and wrote nothing.

## Files (check/)

**Scripts:**

| script | sha256 |
|---|---|
| `chk_static_c2v003.py` | e2aea19f |
| `chk_static_c2v001.py` (superseded) | a04002e6 |
| `chk_static_c2v002.py` (superseded) | 04348c59 |
| `chk_b0_c2v001.py` | 7e813240 |
| `chk_tail_worker_c2v001.py` | 4a4abe77 |
| `chk_tail_compare_c2v001.py` | cbb2d402 |

**Records:**

| record | sha256 |
|---|---|
| `out/CHK_STATIC_R5_C2V003.json` | 8d811141 |
| `out/CHK_B0_R5_C2V001.json` | 32fb7d68 |
| `out/b0_V001/` | dry-run report dirs |
| `out/tail_V001/CHK_TAIL_COMPARE_R5_C2V001.json` | 04fe2ead |
| `out/tail_V001/r4/WORKER.json` | 1d7ef8a9 |
| `out/tail_V001/r5/WORKER.json` | bbcd8a76 |
| `out/tail_V001/{r4,r5}/F_ARRAYS.npz` | 9b801b29 |
| `out/tail_V001/{r4,r5}/F_EVALS.npz` | — |
