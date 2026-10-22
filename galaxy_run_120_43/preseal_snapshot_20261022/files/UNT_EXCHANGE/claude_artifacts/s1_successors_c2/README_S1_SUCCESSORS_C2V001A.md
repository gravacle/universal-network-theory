# s1_successors_c2, A build: the BLK-1 fix (README)

**For root (Claude2), UNT Galaxy Run 120/43.** Built by a root workflow lane on 2026-10-19 (`date -u` 18:27Z at this write). Nothing here is adopted until root rules and a distinct lane reviews. **Nothing was launched**: no solver, monitor, launcher, launcher worker, gate CLI or CP-1 scheduler/worker, and no real machine-gate probe. No run tree, External1 path, `~/.codex`, `c5h_hull_c2/`, `UVT_*` or `v003g/slots` path was opened. The live CP-1 scheduler (pid 18346, out-root `cp1_run_c3v004`) was not touched. **No existing file was edited**: every file below is new, created by exclusive create next to the first versions.

Labels: **TESTED** = shown by a suite here or read from bytes; **FORMAL** = follows from cited code; **UNTESTED** = the deciding test is named.

## BLK-1 and the fix

**The defect (the verifier's probe_adv2, TESTED there and reproduced here as B-P1).** Lib v002's `read_reading` took the manifest's fill record as given: branch, theta_key, physical_u_A and the u_A_point pin were never recomputed or bound to Phase 1.
- An AT_ANCHOR record edited to `branch: OFF_ANCHOR` read PASS instead of PASS_AT_ADOPTION_POINT, which lifts A150's hold on Phase-2 step-5 reads. `guard_replay` also accepted that record.
- A record whose u_A_point names a log-only point read PASS_AT_ADOPTION_POINT, while `guard_replay` refused it.
- **A third instance, found here (B-P1):** three runs one ulp off u_A read INVALID (SV3), but PASS once the record's `physical_u_A` was edited to their bits.

**The fix, by BLK-1 item:**

| Item | Fix in `s1_path_lib_c2v002a.py` | Tests |
|---|---|---|
| (1) read_reading replays | `read_reading` calls `replay_specs(fill_rec)` right after the record's schema check, before the compare or any run is read. That re-binds u_A to the Phase-1 primary anchor (B2), replays both spec byte strings and re-looks up the C3T slots | R-F43, R-F44, R-F48, W-F5 |
| (2) derived fields re-derived | New `check_fill_derived`, called by `replay_specs`. Each must equal its re-derived value as canonical JSON, so floats compare bitwise: `branch` = `branch_record(theta, static, physical)` exactly as `fill` computes it; `theta`; `physical_u_A`; `base_point_key`; `static_pins`; and per case the spec pin (sha = the replayed bytes), `k`, `cb_case`, `label`, `changed_paths`, `sha256` and `point_key`. `theta_key` and `phase1_snapshot` were already checked in `replay_specs` | R-F45, R-F46, R-F47 (13 single-field edits) |
| (3) the same check for guard_replay and launch | It sits in `replay_specs`, which `guard_replay` (guard012's S1_REPLAY_API) and the launch path's S1 checks already call | A-F2, A-F3 (guard012's own `validate`: S1_OVERLAP_REPLAY_REFUSED / FILL_RECORD_BRANCH_NOT_REPLAYED), L-F36 (INACTIVE C4T and overlap C3T, both refused at S1_CHECKS with no probe or spawn) |
| (4) MUST_FAILs | Edited branch and log-only u_A_point at read time, plus the rest above | R-F43, R-F44 |

**New refusal codes:** FILL_RECORD_BRANCH_NOT_REPLAYED, FILL_RECORD_THETA_NOT_REPLAYED, FILL_RECORD_PHYSICAL_U_A_NOT_REPLAYED, FILL_RECORD_BASE_POINT_KEY_NOT_REPLAYED, FILL_RECORD_STATIC_PINS_NOT_REPLAYED, FILL_RECORD_CASES_NOT_REPLAYED, FILL_RECORD_CASE_FIELD_NOT_REPLAYED (the detail names `case.field`). A swapped spec pin keeps S1_TEMPLATE_REPLAY_MISMATCH.

**Not re-derived, named in the code** (`FILL_FIELDS_NOT_REPLAYED`, `CASE_FIELDS_NOT_REPLAYED`): `module`, `module_sha256`, `blockers`, `notes`, and each case's two validate_block strings. No decision reads them (FORMAL). make_plan's sidecar and guard012's controls compute their own validate_block results.

**Small hardening inside `replay_specs`, disclosed:** a non-object base spec and a campaign config without `numerics.block` now refuse with the fill's own codes (BASE_SPEC_OBJECT, CAMPAIGN_CONFIG_NUMERICS_BLOCK) instead of raising a KeyError.

**The verifier's own probe on the A build (TESTED):** `probe_adv2.py` run unchanged against a scratch copy of these files returns RAISED on all four probes:
- forged-branch reading and `guard_replay`: FILL_RECORD_BRANCH_NOT_REPLAYED;
- log-only-u_A reading and `guard_replay`: PHASE1_PRIMARY_ANCHOR_NOT_U_A.

The two genuine readings are unchanged (PASS / OFF_ANCHOR and PASS_AT_ADOPTION_POINT / AT_ANCHOR).

## Files (sha256 from bytes; HASHES_A.txt has every new file)

| File | Role | sha256 |
|---|---|---|
| `s1_path_lib_c2v002a.py` | the library, successor of v002 `e3ca4d80` | `f961839b2dd1ef27c6225badedcc199db3f6515776b5e7e5c08ecede3e769a9e` |
| `s1_fill_c2v002a.py` | fill CLI (library pin and docstring only) | `953e698d8ca87c3894344bef628f048875fe0a2a9a0f3fc873a0720af1499c9d` |
| `s1_launch_root_c2v002a.py` | launch CLI (library pin and docstring only) | `aa49ef4a1a704d17c130d1d16f7028b6556824b4eec259a53f274464d5ae3f71` |
| `s1_read_c2v002a.py` | read CLI (library pin and docstring only) | `4530dd25adc6f1bb361daf31a3d3d3a8c59e1a24d78ac038614342d0cc953378` |
| `test_s1_path_c2v002a.py` | suite | `aa6e35450dcd6f4d5f8dea7acaa6a4727322004d61ed0444230a3db73060a385` |
| `S1_C3T_CERT_EXTENSION_PROCEDURE_A.md` | (4) with the c2v002a CLI names (steps 2 and 7), plus the reading as step 7 item 6 | `4da9ddb5c38f024bb31489da1eb260691870be86ea34c7f9b900cae88bfcf2af` |
| `DIFF_*__c2v002a.diff`, `DIFF_S1_C3T_CERT_EXTENSION_PROCEDURE__A.diff` | unified diffs against each predecessor | HASHES_A.txt |

**Unchanged and still pinned by the A library:** guard012 `f4656fec`, launcher013 `620a44da` and the wrapper successor `e7f52461`. The registration pin `67b4bd78`, the V6 entry-line conventions, every record schema and `S1_REPLAY_API` (`UNT_S1_FILL_REPLAY_C2V002`, guard012's constant) are also unchanged. So guard012 accepts the A library as the overlap replay module (TESTED L-P3, A-F3), and their own suites (G12, WS) do not load the library (FORMAL; not re-run).

## Tests: 148/148 twice

- **Counts:** 27 MUST_PASS and 121 MUST_FAIL.
- **Runs:** `test_runs/S1A_RUN1` and `S1A_RUN2`, 30.9 s and 31.3 s, peak about 249 MB RSS. The real V6 read `41fe5aa2` at test time.
- **Ported:** all 135 c2v002 ids, with the same expected codes. Two details differ:
  - R-P1 now also requires `fill_record_replayed`.
  - L-F15 refuses with the same code and stage, but the refusal now comes from inside the replay, with the case as detail.
- **New MUST_FAIL:**
  - R-F43 to R-F48 at read time (R-F47 has 13 sub-cases);
  - A-F2 (`guard_replay`), A-F3 (guard012 `validate`), L-F36 (launch path), W-F5 (the read CLI unpatched against the real V006).
- **New MUST_PASS:**
  - **B-P1:** the predecessor's bytes reproduce all three BLK-1 instances, so the MUST_FAIL inputs reach the defect.
  - **A-P2:** a fill record written by c2v002 replays under c2v002a and differs from c2v002a's own record only at `module`, `module_sha256` and the spec-file paths.
  - **F-P8:** the procedure's step 2 output (`c3t-cp1-spec`) is byte-identical under both versions.

## For root

1. **Use the c2v002a CLIs** for fill, plan, launch and read, and procedure A. A fill record already written by c2v002 is accepted when it replays (A-P2).
2. **Overlap admission `sources`:** the replay module is the library's own pin, so for an overlap batch it is `s1_path_lib_c2v002a.py@f961839b…`, and root's source review covers it, not v002.
3. **FORMAL limit:** the branch compare is bitwise, and `branch_record` uses `math.log`. The fill and the reading must therefore run on the same platform's libm, which the pinned interpreter on this machine gives. UNTESTED across platforms; deciding test: replay a fill record written here on the other platform.
4. **make_plan is unchanged.** It does not replay, and its `s1.branch` / `theta_key` are labels that no decision reads (FORMAL). A plan from an edited record is refused at launch (L-F36) and by guard012 (A-F3).

## Open root items

1. **BLK-1 review:** distinct-lane review of lib c2v002a, its three CLIs and the suite. guard012, launcher013 and the wrapper successor need the reviews already listed.
2. **Carried unchanged from README_S1_SUCCESSORS_C2V001.md items 1-7:**
   - R-C3T-1 (blocking for S1_UA_C3T; procedure A §1 unchanged);
   - R-C3T-2 (SV7 acceptance tooling);
   - the overlap gate cost;
   - admission content (`sources` now name lib c2v002a for overlap);
   - Phase-1 pointers (phase1_c2v003 `cmd_snapshot`);
   - verifier note 3 (A150 erratum governs).

## Disclosures and deviations

- **Development:** in the session scratchpad (`s1succ_a/`), then assembled here once by exclusive create (`build_a.py`, `final` mode). The final bytes equal the last dev build, compared with `cmp`.
- **Verifier probe:** the verifier's `probe_adv2.py` was read in full and run once, against a scratch copy, with outputs in the scratchpad.
- **Predecessor library:** v002 (`e3ca4d80`) is loaded read-only in-process by B-P1, A-P2 and F-P8. A-P2's c2v002 fill writes its specs and record inside the test run folder.
- **Writes in this folder (all new):**
  - the 6 files above, 6 diffs, this README and HASHES_A.txt;
  - `test_runs/S1A_RUN1` and `S1A_RUN2` (synthetic fixtures, about 13 MB each). As in c2v002's suite, R-F39 makes a symlink inside its run folder to a nonexistent NGC3198-named path; nothing at that target was opened or created.
- **Processes:** the suite (`python -I -B`, twice in this folder, twice in the scratchpad), its CLI subprocesses, and the one probe run.
