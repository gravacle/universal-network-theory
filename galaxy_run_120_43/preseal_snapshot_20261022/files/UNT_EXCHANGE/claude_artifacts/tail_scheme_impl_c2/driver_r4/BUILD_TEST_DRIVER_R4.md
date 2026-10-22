# Driver c2v010 r4: build and test record

tail_scheme_impl_c2/driver_r4, 2026-10-18. Claude2 lane. Hashes are in `HASHES.txt`, computed from bytes.

**Pins.**
- The frozen V004 addendum `487d4449`.
- The open V005 addendum is cited by name (A49, and A50 items 11–13).

**Process.**
- No forward, route-A or route-B run was launched.
- C5H was not opened.
- At most 3 compute processes ran at a time.

**Driver.** `galaxy_m0_forward_c2v010.py` **`b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b`** (4,991 lines).

**Build.**
- Built from r3 `4c14552f` by `tools/make_driver_c2v010_r4.py` (`f0ff0a54`), using 37 exact-once edits.
- Record: `BUILD_DRIVER_C2V010_R4.json` (`c081d3b2`).
- Diffs: `DIFF_R3_R4.diff`, `DIFF_V009EXT_R4.diff` and `DIFF_V009GEO_R4.diff`.

## 1. Changes against r3

**R1: RO1 c2v002 (CHECK F1, A49).**
- The c2v001 → c2v002 vehicle diff (`32ab8164`) is applied hunk by hunk. It contains the six pins, the three-message RO1_MESSAGES including the full DEGENERATE_RADIAL_EULER text, and hunk 6, the RO1-aware NGC reader.
- Checked from bytes before the edit: v009-EXT + 1f363113 = vehicle 118c3260, v009-EXT + 90eb7b56 = vehicle db1183bc, and vehicle1 + vehicle diff = vehicle2.
- Test K3: in r4, `ngc_read_route_a_result` and `route_a_outcome_record` equal the c2v002 vehicle's exactly. `ro1_outcome` differs by one declared line: the armed worker set adds the two nodes RO1 workers, which are RO1 c2v002 workers with the nodes controller and the same RO1 binding `86af6198`.

**R2: nodes_v001 is built (A50 item 11).**
- UV_TAIL_NODES_V001_NOT_BUILT is gone. In its place:
  - an ext grid that is not a composite spec object is refused (UV_TAIL_NODES_V001_EXT_GRID_INVALID);
  - NGC is refused (UV_TAIL_NODES_V001_DDO154_ONLY).
- `uvt_plan`, for nodes_v001:
  - the ext grid is checked against the seed grid by the pinned nodes library;
  - every kept region must be a cube;
  - D is the extra-node set G_ext∖G_K (never empty when G_ext ⊋ G_K);
  - the plan records `source_rule` and `nodes_ext_context`.
- Active tables: the scripts, aux files and route-A workers swap to `SCRIPTS_UVT_NODES`, `AUX_UVT_NODES` and `NODES_ROUTE_A` (`uvt_active`). The swap reaches execute_chain, the binding blockers, the static pins, the dry-run scans and the plan records.
- Continuum calls plan exactly the r3 tables, except that the reference is now c2v003 (R4).

**R3: probe radii (A50 item 13).** The route-A tail record gains `probe_R_m`, `probe_phi_rad` and `probe_source`, copied from the request monitor. The plan record carries `monitor_probe_R_m`.

**R4: CHECK F4.**
- `SCRIPTS_UVT['reference']` is now the reference successor uvt_c2v003 (`4778fc73`). Its start.json 'boundary' text is the binding's text only for a non-empty state; for an empty domain the reviewed text is kept byte for byte.
- **Declared, not changed:** the offset `boundary_description`. It is an argument to the reviewed operator call, fixed before the offset tail state exists, and is excluded from the offset's custody comparison (L249). The `uv_tail` start and finish records carry the truth.

**R5: tail OFF on the RO1 workers (A50 items 11–12).**
- New optional key `numerics.route_a.ro1_workers`. It accepts only `true` and needs a computed route A and the tail OFF.
- The RO1 c2v002 worker runs with the v009 solver and a tail-disabled request (`uv_tail.enabled false`, certificates NONE_TEST_ONLY; the sidecar is never created). The RO1 binding then receives `uv_tail=None` and executes the reviewed statements.
- The pins and the scan cover the RO1 worker, the RO1 binding, the facade, the controller module and the library.
- **Absent key:** the r3 / v009-EXT plan, unchanged (B0).

## 2. Gates and tests (TESTED)

| gate / test | tool (sha8) | output | result |
|---|---|---|---|
| B0 / B0′-DRY: all 34 standard specs against both parents, declared maps | gates/b0_plan_identity_c2v002.py (b9aeb78e = c2v001 24108a34 with ≤ 3 workers) | out/B0_RUN_V001/ | **50/50 PASS_PLAN_IDENTICAL; B0′-DRY PASS** |
| B0-FA (A1, A2, A4 → REFUSED ROUTE_A_CHECKPOINT_MISSING) | same | same | **3/3 PASS** |
| Gate records, schemas C2V001 and C2V002 | gates/write_gate_records_v007_c2v003.py (9e9b6bb3) | out/GATE_RECORDS_R4_SCHEMA_C2V001/, out/GATE_RECORDS_R4_SCHEMA_C2V002/ | B0, B0prime_DRY, B0_FA and **B0_N3 PASS** |
| v010 r4 suite: groups A–I from r3 plus J nodes, K RO1 c2v002, L ro1_workers, M probe radii, N F4 | tests/test_v010_r4_c2v001.py (75bc40e0) | out/TEST_V010_R4_C2V003.json | **56/56**, no launch |
| Dry run of every V007 spec, the identity specs and C5H | gates/dryrun_tail_specs_c2v002.py (0ecb7605) | out/DRYRUN_TAIL_SPECS_RUN_V001/DRYRUN_TAIL_SPECS_C2V002.json | **25/25 PASS_ZERO_BLOCKERS** |
| Identity comparator, F6 | gates/run_identity_compare_c2v002.py (f7bb7e7f) | self-test out/COMPARATOR_SELFTEST_R4_V001/ (selftest a0890ad4) | **4/4** |
| T2-I machinery | nodes_v001/gates/t2i_replica_check_c2v001.py | nodes_v001/out/T2I_*.json | **PASS** (C5R3 2.2e-15, C6R3 2.5e-15) |

**B0_N3.** 11 construction and build sites, all guarded:
- the c2v001 sites, now guarded by the RO1 c2v002 binding;
- the nodes controller, binding and manifest writer;
- the tail-OFF RO1 site, where the worker passes `uv_tail=None` for `enabled false`.

The driver itself constructs nothing.

**Dry run.**
- Both C4T-D5 templates (N8, N1) have **zero blockers apart from PENDING_UV_TAIL_CERTIFICATE**. They plan:
  - the nodes RO1 workers (5a4c7d41 parallel);
  - the nodes manifest writer;
  - SCRIPTS_UVT_NODES;
  - cube kept regions;
  - 374,976 extra nodes.
- The other 18 T templates: pending certificates only.
- Z2: clean. It plans the RO1 c2v002 parallel worker d676ecb2, which is in the armed set.
- Z2_OFF_RO1: clean. It plans the RO1 c2v002 worker with the v009 solver aed4dd59 and the tail-disabled request.
- Z2-OFF, B0′-RERUN and C5H: clean.

**F6 comparator.**
- `--gate` is required. Only Z2 masks `uv_tail` and `uv_tail_tap`, drops `numerical_controls.uv_tail` and admits the extra manifest stage.
- New checks: STRAY_UV_TAIL in the tail-OFF gates, and `--require-ro1-armed` (A50 item 12).
- Self-test results:
  - **Real tail-OFF pair** (deciding (i), v008 against v009-GEO), `--gate Z2_OFF`: still PASS_BITWISE_EQUAL.
  - **Synthetic stray tail record:** c2v001 passes it (the defect F6); c2v002 fails it under Z2_OFF and B0PRIME_RERUN and passes it under Z2.
  - **caller_norm:** keeps the stray entry in tail-OFF mode and drops it in tail-ON mode.
  - **RO1 check:** passes only when armed is true and fired is false.

## 3. Spec registry V002

`specs/SPECS_V007_C2V002_R1.json` **`9bfe96741a8aa86a8956f67fab9ebcb62548f228aaaf54dd6c1633754d26e69f`** (tool `make_specs_v007_c2v002.py` `31529b15`). It holds 23 specs plus the registered ones.

**Unchanged from V001** (shas re-verified from bytes):

| spec | sha8 |
|---|---|
| C2T N8 / N1 | 1348aed5 / 2cc67753 |
| C3T N8 / N1 | c2551871 / c8ce736d |
| C4T N8 / N1 | 5aebb6bb / 01c2b15e |
| C6T N8 / N1 | 86c7bdde / 833ea1e3 |
| S4T N8 / N1 | 530d1ac4 / 3adf8015 |
| C4T-C5c N8 / N1 | 092b0128 / 36bb16ab |
| C4T-K16 N8 / N1 | e5064e42 / dd944e2e |
| C4T-K64 N8 / N1 | fb06ff77 / 5e338825 |
| C4T-A N8 / N1 | aa8b101e / 1e4f916a |
| Z2 | 2d5e79d0 |
| NGC N-test request | f230c5b2 |

**Label-only successors.** The old labels said "NOT BUILDABLE". The canonical numerics are checked byte-identical.

| spec | sha |
|---|---|
| C4T-D5 N8 | **1aaa21177776ed81…** (supersedes 2b66c3cc) |
| C4T-D5 N1_FALLBACK | **3b7fc6cf42a9cfd1…** (supersedes 4532941a) |

**New.** Z2_OFF_RO1 `CALL_UVT_Z2_OFF_RO1_A2F10_N8_C2V010R4.json` **`894e5b3ab67d58cd…`**. It is 4978ba17 + `numerics.route_a.ro1_workers` true + a new label.

**Registered, unchanged:**

| spec | sha8 |
|---|---|
| Z2-OFF | 4978ba17 |
| B0′-RERUN | 4ac5527a |
| C5H | 60b46130 |

## 4. Still blocking or open

1. **PENDING_UV_TAIL_CERTIFICATE.** The EPS and LO certificates do not exist, so every T template is planning-only, C4T-D5 included.
2. **A50 item 12 for B0′-RERUN is unsatisfiable as written.** Its route A is admitted (CODEX1 V002), so no RO1 block can be armed, and r4 refuses `ro1_workers` with an admitted route A. Root ruling needed: exempt it, or re-define it with a computed route A, which would no longer be the B0′ object. Z2 and Z2_OFF_RO1 satisfy item 12 at plan level; the armed and not-fired record itself is a runtime result (root launch).
3. **Lanes still on c2v001 (F1 follow-up outside this lane).** The prereg (R3) `binding_inputs.ro1` and `declared_output_maps_of_B0` still cite RO1 c2v001 (1f363113). So do the launch plans `driver/launch*` and the case block. They must move to r4 b9ae92d5, RO1 c2v002, the registry above and the D5 label successors. The V007 compare must also accept the nodes records (`source_rule nodes_v001`, `nodes_ext_context`) and the comparator c2v002 `--gate` interface.
4. **UNTESTED at runtime (root launches):**
   - Z2, Z2_OFF_RO1 and B0′-RERUN identity;
   - C4T-D5 end to end;
   - the `probe_R_m` copy on a returned route A (TESTED at plan level and by code reading);
   - the feedback replica on G5∖G4.
5. **CHECK F2** (the per-row noise allowance) still needs its root prereg ruling; nothing here changes it.

## 5. Errors register

1. A first registry run failed on PosixPath serialization. It left the truncated stub `specs/SPECS_V007_C2V002.json` (288 bytes, invalid JSON). The stub is kept and declared superseded in R1, and the registry is `_R1`. The spec files written by that run are byte-identical to the rerun's (checked).
2. Superseded test-suite attempts, both harness errors:
   - `out/TEST_V010_R4_RUN_V001` (relative outdir);
   - `out/TEST_V010_R4_RUN_V002` (a KeyError in a new test line).
   - The test file was then fixed, and RUN_V003 is the record.
3. `gates/write_gate_records_v007_c2v002.py` (35bab533) is unused. c2v003 cites the B0 tool actually run.
4. Two placeholder hash literals were typed into my own tools: a registry pin and a self-test base pin. Both were caught before any run and replaced by byte hashes or runtime computation. Neither was published.
