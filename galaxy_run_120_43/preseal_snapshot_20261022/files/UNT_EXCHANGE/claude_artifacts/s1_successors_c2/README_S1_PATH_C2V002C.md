# S1 launch-path follow-up (V006 A182): lib c2v002c, CLI wrappers c2v002c, binder step4_bind_c2v011

Written 2026-10-19T23:36:10Z (date -u). Claude2 root workflow item, V006 A182 "Commissioned: the S1 launch-path
follow-up" (A177 builder items (1)-(3) and README_KS_K3_GWAVE_C2V001b.md section 7 G7).

**Status: BUILT. NOT ADOPTED.** Nothing launched, no process or run tree touched, no NGC3198 data file opened. Every
test is synthetic. No existing file was edited; every deliverable was created by exclusive create. Every sha256 below
is from bytes; HASHES_S1_PATH_C2V002C.txt has the full list.

Labels: **TESTED** (a test here, or read from bytes), **FORMAL** (follows from the cited code), **UNTESTED** (the
deciding test is named).

## 1. Files

| File | sha256 | Base |
|---|---|---|
| s1_path_lib_c2v002c.py | `99e2be175e546992c70984435bc480e1eddb90b052fda65ddcbfe8780bdbd27e` | lib c2v002b `65d69cf4` |
| s1_launch_root_c2v002c.py | `d4e310138c3c2a068d6a963d32c230a52cdca4467ece8e60de39fce3b5955684` | c2v002a `aa49ef4a` |
| s1_fill_c2v002c.py | `2b120b89c7b9aa95e585ff95ac21d27abd83497049bc78a81aa594019b4877c5` | c2v002a `953e698d` |
| s1_read_c2v002c.py | `4716bb696cfa6bc163f18d8602ad2aa7326317868ccaf4152dfb323b8baa8d5d` | c2v002a `4530dd25` |
| step4_bind_c2v011.py | `d3d9702eb8096d11b98461f1c62c67931b9ecf74957cee95fbc3a60f60deaea0` | step4_bind_c2v010 `4d07dca3` |
| test_s1_path_c2v002c.py | `e6a5782912f920776aad3e479027688868c8f3b12766f3a7ca37bcbb59f9ec8c` | test_s1_path_c2v002b `a4923e43` |

DIFFs (each against its base): `DIFF_s1_path_lib_c2v002b__c2v002c.diff`, `DIFF_s1_launch_root_c2v002a__c2v002c.diff`,
`DIFF_s1_fill_c2v002a__c2v002c.diff`, `DIFF_s1_read_c2v002a__c2v002c.diff`, `DIFF_step4_bind_c2v010__c2v011.diff`,
`DIFF_test_s1_path_c2v002b__c2v002c.diff`.

## 2. lib c2v002c (three changes, nothing else; TESTED L-P0)

1. **Wrapper pin** `WRAPPER_S1K3` = KS5'' `ks_k3_chain_c2/calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v003.py`
   `51a6fb27` (was e7f52461). This is the plan sidecar's `context_module`.
2. **`sources_to_add`** = `s1_sources_to_add(overlap)`: guard014, launcher015, then `S1_FENCE_SOURCES` in A182's order,
   then (overlap only) the library itself, as before. Eight pins were added to PINS for it.
3. **Default params** `DBP` = `sched_s45_c2/v004b/DIRECT_BATCH_PARAMS_S45_C2V004B.json` `e239d21e` (was C2V003A).

Against c2v002b: only MODULE, PINS and make_plan differ; S1_FENCE_SOURCES and s1_sources_to_add are added; make_plan
differs only in its sources_to_add expression; imports are unchanged (TESTED L-P0).

### The exact sources_to_add list and its basis

guard014's fence (L126-127, L161-168, L182-187): inside `fence()`, every `.py` opened under `/Research/` must be a
listed source, and every module compiled from such a path must match its listed sha. native_preflight (L248-253) also
requires each C1 producer, custody deriver and state enumerator to be allowlisted. The S1 prelaunch on the canonical S1
C1 (A182: custody KS1, enumerator G6c, producers G4 / G3 producer / G1, policy review `guard_sha256` KS5) opens:

| # | Source | sha256 | Opened by (FORMAL from bytes) | Left out (TESTED, DEC-F1) |
|---|---|---|---|---|
| 1 | s1_successors_c2/step4_guard_c2v014.py | `6efdca01` | validate L369 `admitted_source(plan['guard'])` | SOURCE_NOT_ALLOWLISTED |
| 2 | s1_successors_c2/step4_launcher_c2v015.py | `cd987edd` | validate L369 `admitted_source(plan['launcher'])` | SOURCE_NOT_ALLOWLISTED |
| 3 | KS5'' ks_k3_chain_c2/calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v003.py | `51a6fb27` | guard014 L239 `load(context_module)` (L195 allowlist, L198 verified exec) | UNPINNED_PREFLIGHT_SOURCE |
| 4 | KS5 ks_k3_chain_c2/certificate_guard_b1_ks5_c2v001.py | `e394ae94` | KS5'' import (`_load(GUARD_KS5)`); q5b1 L73 hashes it | UNPINNED_PREFLIGHT_SOURCE |
| 5 | KS1 ks_k3_chain_c2/custody_cx2v002_ks1_c2v001.py | `ad020470` | guard014 L249, L253; q5b1 L68 (read), L92 (load) | UNPINNED_PREFLIGHT_SOURCE |
| 6 | calib_tail_readiness_cx2/certificates_per_point/custody_cx2v002.py | `6810b7c3` | KS1 L81-82: loaded at KS1's import | NATIVE_GATE_REFUSED (inner UNPINNED_PREFLIGHT_SOURCE) |
| 7 | KS2 ks_k3_chain_c2/point_response_producer_cx2v002_ks2_c2v001.py | `99c29df6` | KS5'' `s1_rho_slot_problems` reads it | NATIVE_GATE_REFUSED (inner UNPINNED_PREFLIGHT_SOURCE) |
| 8 | G4 ks_k3_chain_c2/point_response_admission_adapter_cx2v003_g4_c2v001.py | `e00ab71d` | guard014 L252; q5b1 L69, L157 (EPS proof producer) | UNPINNED_PREFLIGHT_SOURCE |
| 9 | G3 producer ks_k3_chain_c2/gq_producer_cx2v005_g3_c2v001.py | `c3699c78` | guard014 L252; q5b1 L69; KS5 verify_bundle L154 (GQ proof producer) | UNPINNED_PREFLIGHT_SOURCE |
| 10 | G1 ks_k3_chain_c2/lo_slot_proof_c3v003_g1_c2v001.py | `6af9ed6c` | guard014 L252; q5b1 L69, L157 (LO_RHO_SLOT proof producer) | UNPINNED_PREFLIGHT_SOURCE |
| 11 | G6c ks_k3_chain_c2/consumed_states_b1_c2v001_g6_c2v001.py | `4ea0c2ca` | guard014 L249, L253; q5b1 L68 (read) | UNPINNED_PREFLIGHT_SOURCE |

Items 3-11 are `S1_FENCE_SOURCES`. With overlap, the library itself is appended (the replay module), unchanged from
c2v002b.

- **Not added: the G3 geometry `572c86c6`.** It was named in the commissioning text "if the G3 producer loads it". At
  prelaunch the G3 producer is only read: q5b1 L69 and KS5 L154 read its bytes, and nothing executes it. So the G3
  geometry is never opened. TESTED: DEC-P1 records no open of it. G6a `ba58fb18` and G6b `65834e9b` are not opened
  either: at prelaunch G6c is only read, and q5b1 L114 runs it at acceptance only.
- **The q5b1 base stays root's.** The S1 README C2V001 says, for the admission content, "q5b1, core, ORC, sensitivity
  v002 and guard b1 must be listed, as for q5b1". The same base also holds the r5 driver closure, the monitor, the
  packet's direct adapter and its adoption policy.
  - DEC-P1 opened these five base sources: q5b1 `7a6af535`, core `dc895f8a`, ORC `c75a889f`, sensitivity v002
    `8fb06600` and guard b1 `9e3fc109`.
  - KS1's S1 custody derivation (KS1 L153-192) opens the r5 driver and its closure, `certs_common_r5_cx2v001.py`
    `c75aaa5a`, the driver's GEOMETRY_PINS files, the coefficient file and the prereg pin. 6810b7c3's K=4 derivation
    opens the same set (L103-142), and the campaign C1 runs that derivation for every tail-ON prelaunch (FORMAL). So
    these belong to the base. They are seamed in the tests and are **UNTESTED** here (section 6).

## 3. CLI wrappers c2v002c

s1_launch_root, s1_fill and s1_read are their c2v002a code with only the library pin changed:
- `LIB` = `s1_path_lib_c2v002c.py`;
- `LIB_SHA` = `99e2be17...`;
- the module name.

The docstrings now describe lib c2v002c (guard014 / launcher015, no gate, and plan without `--params` using C2V004B).
TESTED W-P4: the code after the docstring is AST-identical to c2v002a's once the library name and sha are substituted.
There were no c2v002b wrappers, so the base is c2v002a.

## 4. binder step4_bind_c2v011

c2v010 with three changes:
- `GUARD_PATH` / `GUARD_SHA256` load guard014 `6efdca01` instead of guard011;
- the command drops `nice -n 10`. It keeps `env` with single-thread BLAS, then `python -I -B <launcher> <plan>
  --execute-root-only`;
- `check_command` refuses an argv carrying `nice` or `renice` (NICE_IN_COMMAND_REFUSED) before any output is written.

The binder now lives in s1_successors_c2, so the output folder c2v010 derived as `HERE.parent` is named explicitly:
`PACKET` = `step4_launch_packet_cx1`. Every other check is c2v010's. TESTED BIND-P2: only GUARD_PATH, GUARD_SHA256 and
bind differ; HERE is removed; PACKET, NICE_PROGRAMS and check_command are added; bind differs only in those two lines.

## 5. Deciding test (DEC-P1, DECIDING): PASS in both runs (TESTED, synthetic)

**Setup.**
- The S1_UA_C3T spec is the one lib c2v002c fills at the synthetic u_A "off" point, against a synthetic registry.
- The admission's `sources` are the q5b1 base plus lib c2v002c's `sources_to_add`.
- The C1 is the canonical S1 C1. Its custody deriver, enumerator and producers are the real files, read under the
  fence. Its policy review binds KS5.
- The certificate world (registry, bundle, EPS / GQ / LO_RHO_SLOT proofs, EPS record, rho record) is synthetic JSON.

**(1) guard014 `native_preflight`: PASS.**
- adoption passes, and every gate passes: certificate_policy_gate under KS5, certificate_check (prelaunch: KS5
  verify_bundle, then the KS5'' domain-K and rho-slot checks), sensitivity_gate and prelaunch_check.
- KS1 ran as the custody deriver twice and saw the S1_UA_C3T identity (`s1_c3t_spec` True) both times.
- Opened `.py` under `/Research/`: the nine fence sources and the five base sources above. 0 unlisted opens. The G3
  geometry, G6a and G6b were not opened. No process event.

**(2) The library's own dry launch: ADMITTED, all four controls PASS.**
- make_plan used the default params C2V004B. The admission sources came from the plan sidecar's `sources_to_add`,
  which equals `s1_sources_to_add()`.
- validate replays (1). The synthetic process table was read once. Nothing was spawned.

**Companion tests (TESTED):**
- **DEC-P2, non-S1 specs unchanged.** guard014's preflight under KS5'' and under the as-built q5b1 gives the same
  outcome.
  - On a b1-bound K=4 C1, the campaign-labelled and the S1_UA_C4T-labelled K=4 specs PASS under both, with byte-equal
    prelaunch records.
  - A campaign label on the CB C3T grid is refused by both ("kept K must be 4").
  - Under the S1 C1, the S1_UA_C4T spec is refused by both (NATIVE_GATE_REFUSED, "binding mismatch: guard_sha256"). The
    refusing gate differs by the KS5' design: KS5'' reads KS5 at Context level and the C4T spec's own check meets b1;
    q5b1 meets b1 at the first gate.
- **DEC-F1, a source missing from sources_to_add is refused by the fence.** All 11 leave-one-out cases are refused,
  with the codes in section 2.
- **DEC-F2, the old wrapper e7f52461 is refused**, in three ways:
  - (a) named as the context module on lib c2v002c's sources: control C1 refuses UNPINNED_PREFLIGHT_SOURCE;
  - (b) with e7f52461 added to the sources, the S1 C1 refuses it (NATIVE_GATE_REFUSED, "binding mismatch: guard_sha256");
  - (c) a fill record written by lib c2v002b (static_pins e7f52461) is refused by guard_replay and at the launch path's
    S1_CHECKS (FILL_RECORD_STATIC_PINS_NOT_REPLAYED).
- **BIND-F1, nice in the binder command is refused.** c2v010's argv form, `/usr/bin/nice` and `renice` are each refused
  NICE_IN_COMMAND_REFUSED.
- **Mutation check** (dev, not a deliverable; `test_runs/S1C_DEV_MUT_001`): a lib with G1 removed from S1_FENCE_SOURCES
  reads 151/163. DEC-P1 fails with "Refusal: UNPINNED_PREFLIGHT_SOURCE", and F-P9 and L-P0 fail too.

## 6. Tests

`test_s1_path_c2v002c.py`: **163/163 in `test_runs/S1C_RUN1` and `test_runs/S1C_RUN2`**.
- By kind: 37 MUST_PASS, 125 MUST_FAIL, 1 DECIDING. Each run took about 26 s.
- Ids, kinds and results are identical across the two runs.
- The logs differ only in shas that depend on the run folder (R-P3, A-P1, F-P8, DEC-P2), as in c2v002b's S1B runs.

**Ported from c2v002b: 142 of 143.**
- L-P0, A-P2 and F-P8 are retargeted to c2v002b as the predecessor. A-P2: the records now also differ at
  `static_pins.WRAPPER_S1K3`, and the spec bytes are identical.
- L-P4 is not ported. It reads the real V006, and this build reads V006 only through awk.

**New: 21 tests.**
- F-P9: the exact list, checked against an independent list from bytes.
- L-P10: the default params plan is admitted by guard014.
- L-F39: an explicit C2V003A plan is refused MEMORY_ADMISSION_FIELD_REFUSED.
- CLI: W-P2, W-P3, W-P4, W-F2 (all three CLIs), W-F3, W-F6 and W-F7. The real-V006 W-P1, W-F1, W-F4 and W-F5 are
  replaced by the non-root-V006 refusals W-F6 and W-F7.
- Binder: BIND-P1, BIND-P2 and BIND-F1 to BIND-F5. No binder suite existed among the named files.
- DEC-P1, DEC-P2, DEC-F1 and DEC-F2.

**Seams (disclosed):**
- As in c2v002b: `V6_PATH` points at a synthetic V006, dry-mode `process_table`, and `subprocess.run` fakes.
- DEC-*:
  - a synthetic direct-preflight adapter stands in for the packet's adapter (not opened). It builds the context
    module's real Context in direct form, with an identity driver normalization.
  - It replaces only `derive_custody` of the custody deriver, after the deriver was read and executed for real inside
    the fence.
- BIND-*: the binder's `PACKET` is a folder in the run directory, and its guard instance's `disk_admission` is stubbed,
  because it stats /Volumes/External1.

**UNTESTED, with the deciding test named:**
- The real r5 normalization, the real custody derivation (the base opens in section 2) and the packet's direct adapter
  inside the fence. Deciding test: root's dry launch (`s1_launch_root_c2v002c.py` without `--launch`) on the real
  S1_UA_C3T admission.
- The real V006 entry-line read through the c2v002c CLIs. Deciding test: the same dry launch.
- The binder on a real direct batch. Deciding test: root's first c2v011 bind.

## 7. Root items

1. **Base list.** Root's S1 admission `sources` = the q5b1 base + the sidecar's `sources_to_add` (11, or 12 with
   overlap). Root confirms the base carries `certs_common_r5_cx2v001.py` `c75aaa5a` and the r5 driver closure. KS1's S1
   derivation opens them as 6810b7c3's does for every campaign call (FORMAL; UNTESTED here).
2. **Two C1s.** The S1_UA_C3T admission takes the S1 C1 (KS5 review). The S1_UA_C4T admission must take the campaign
   (b1) C1: under the S1 C1 the C4T call is refused (TESTED DEC-P2 (b)).
3. **context_module.** As in c2v002b, the launch path does not itself compare the admission's `context_module` with
   its wrapper pin. Root copies it from the sidecar. e7f52461 is refused by the fence and by the S1 C1 (TESTED DEC-F2).
4. **Re-fill.** Any fill record written by c2v002b must be re-filled with c2v002c (FILL_RECORD_STATIC_PINS_NOT_REPLAYED).
   No real S1 fill exists (A172: no S1 call was planned).
5. **Binder.**
   - Root rules c2v011 for direct batches. DBP C2V004B `packet_read.binder` still names c2v010 `4d07dca3` (unchanged
     here). Nothing in the lib reads it. The A177 (6) re-derivation can carry the c2v011 entry.
   - c2v011, like c2v010, does not pin the launcher. A guard014 plan naming launcher014 would bind, then fail closed at
     launcher014's own guard013 validation (FORMAL from A170 / A172).
6. **Wall cap.** The default DBP's wall cap is PROVISIONAL (A140 N4). After the W1 rebuild, root passes `--params`
   or commissions a one-constant re-pin.
7. **Stale texts (no decision reads them; changing them would be a code change).**
   - `C3T_CHAIN_NOTE` (fill and sidecar notes) still says the chain is K=4-only.
   - make_plan's docstring still says "passes the machine gate" (C14 erratum, A177 (5)).
8. **Review:** Claude3 after the G-wave if its credit allows, otherwise Claude4 at Fri 19:00Z (A182).

## 8. Disclosures

- **Reads beyond the named folders**, all by explicit path and sha:
  - q5b1 `7a6af535` (pinned by KS5'') and 6810b7c3 (pinned by KS1);
  - ORC and CORE helper definitions, lib PINS (grep only);
  - sensitivity v002 `sensitivity_gate` (pinned by q5b1);
  - guard011 `eb97e303` (pinned by binder c2v010 and lib PINS GUARD011);
  - binder c2v010 `4d07dca3` (DBP packet_read).
- **V006** was read only through awk, sections A170, A172, A177 and A182. The tests never open it. G-P1 lstat-walks its
  path only.
- **Dev work in scratch** `s1_path_v002c_dev/`: exact-once edit scripts and dev copies. The dev runs are in
  `test_runs/`:
  - `S1C_DEV_001` and `S1C_DEV_002`, each 163/163, superseded;
  - `S1C_DEV_MUT_001`, the mutation check.

  The dev test file of `S1C_DEV_001` (`b757837b`) differed from the final only in DEC-F1's detail text.
- `wrapper_successor()` still registers its module as `_s1_wrapper_s1k3_c2v001`. The code is unchanged, and the name is
  a sys.modules label only.
- **No resource gates.** No nice and no taskpolicy were added. Single-thread BLAS was set for the runs.

## 9. Reproduce (synthetic only)

```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
S=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  $PY -I -B $S/test_s1_path_c2v002c.py --run-dir $S/test_runs/<new>
```
