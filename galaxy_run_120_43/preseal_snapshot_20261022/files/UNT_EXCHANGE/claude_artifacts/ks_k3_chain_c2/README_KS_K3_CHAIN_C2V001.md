# KS1–KS6: the S1_UA_C3T (kept K = 3) certificate and acceptance chain, c2v001

**What this is.** The successors that A160 commissions (ks_k3_chain_c2, built 2026-10-19 by a Claude2 root-workflow subagent). Spec of record: V006 A160 and `s1_successors_c2/S1_C3T_CERT_EXTENSION_PROCEDURE_A.md` §1–3.

**Status.**
- **BUILT. NOT ADOPTED.** Root has not ruled and Claude3 has not reviewed.
- Every test is synthetic.
- Nothing was launched. The live CP-1 out-root `s4rc1_c3/cp1_run_c3v004` and pid 18346 were not touched.
- No run tree, `~/.codex`, `c5h_hull_c2`, UVT_* or NGC3198 file was opened. The KS suite fences these with an audit hook, which recorded 0 refused opens.
- No existing file was edited. Every deliverable here was created by exclusive create.

**Bottom line for root.**
- **KS1–KS6 are necessary for S1_UA_C3T, but not sufficient.**
- Inside the built chain, every K=3 allowance sits behind the S1_UA_C3T identity, and every other spec behaves as its predecessor (TESTED, §4).
- Six links outside the A160 list still refuse K=3 (§7, G1–G7, FORMAL from bytes). The first one, the GQ kernel (G3), is TESTED to need more than KS1 (§6).
- **As built, a CP-1 run of row 32 stops at its GQ stage.**

Labels: **TESTED** means shown by a test here or read from bytes. **FORMAL** means it follows from the cited code. **UNTESTED** means the deciding test is named.

## 1. Chain table

All sha256 values below are computed from bytes. Full values are in `HASHES_C2V001.txt`.

| Id | Successor | sha256 | Predecessor (sha) | Change |
|---|---|---|---|---|
| KS1 | `custody_cx2v002_ks1_c2v001.py` | `ad020470` | custody_cx2v002 `6810b7c3` | `derive_details` accepts the ±3 cube for S1_UA_C3T. `grid_sha256` still includes the grid. Every other spec goes to the 6810b7c3 module object (P). |
| KS2 | `point_response_producer_cx2v002_ks2_c2v001.py` | `99c29df6` | response `a1dcdea8` | For S1_UA_C3T, the shells start at the kept K (3), with 179 EPS unit shells, the 10-shell ρ partition and coverage [3,182]. The L347 ρ sample filter uses K. Custody is KS1. Every other spec goes to P = a1dcdea8. |
| KS3 | `s4rc1_common_c3v004_ks3_c2v001.py` | `736d2e7e` | common c3v004 `53f10e6e` | Adds row 32 from a root-written row file. The 31 rows, `POINTS` and all existing PINS are unchanged. New PINS: KS1, KS2, KS5, KS5′ and the case block. |
| KS3 | `cp1_runner_c3v004_ks3_c2v001.py` | `54595c2d` | runner c3v004 `3f5e5c18` | Pins the KS3 common. For row 32 only: KS2, check_eps over [3,182] with 179 shells, check_rho with coverage [3,182] and 10 shells, and F6 source pins mapped KS1/KS2 → 6810b7c3/a1dcdea8. |
| KS4 | `registry_assembler_c3v004_ks4_c2v001.py` | `080ed171` | assembler c3v004 `cb5c61ee` | Pins the KS3 common. For row 32: bundle domain K 3.0, the s1k3 block rule, the deps rule after mapping, and verify against an S1 C1 (custody deriver KS1, guard KS5). |
| KS5 | `certificate_guard_b1_ks5_c2v001.py` | `e394ae94` | guard b1 `9e3fc109` | At L94, the domain K must equal the identity's kept K: 3.0 for the CB C3T grid, 4.0 for every other identity. |
| KS5′ | `calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v002.py` | `66560a6a` | wrapper s1k3 c2v001 `e7f52461` | q5b1's guard G dispatches to KS5 inside a KS5 scope and to b1 otherwise (§3). |
| KS6 | `lo_core_r5_cx2v001_ks6_c2v001.py` | `2cf7c597` | lo_core `12d36305` | For S1_UA_C3T: a kept K=3 state with B1 edges from 3. The response producer is KS2. Every other spec goes to P = 12d36305. |
| KS6 | `lo_config_r5_cx2v001_ks6_c2v001.py` | `510ff07b` | lo_config `6654d93c` | **Deviation, needed.** The adapter runs lo_config's `validate_current_config`, whose L51 kept region is K=4. Here it uses K=3 for S1_UA_C3T, over the KS6 lo_core. |
| KS6 | `lo_state_proof_adapter_c3v003_ks6_c2v001.py` | `8fa371a7` | adapter c3v003 `211a3220` | For S1_UA_C3T: KS1, KS6 lo_config/lo_core, and the ρ contract taken from the identity (coverage [3,182], 10 shells, KS2 producer). The entry point and CLI hand every other spec to 211a3220. |
| KS6 | `acceptance_handoff_c2v004_ks6_c2v001.py` | `6642d209` | handoff v004 `5ff464cc` | S1_UA_C3T uses LO_ADAPTER_KS6. Every other spec goes to P = 5ff464cc. |

**Re-pinning is consistent and TESTED (X-P1).**
- KS2 pins KS1.
- The KS3 common pins KS1, KS2, KS5 and KS5′.
- The KS3 runner and KS4 pin the KS3 common.
- KS5′ pins KS5.
- The KS6 lo_core pins KS2. The KS6 lo_config pins the KS6 lo_core and checks KS2.
- The KS6 adapter pins KS1, the KS6 lo_config, the KS6 lo_core and KS2.
- The KS6 handoff pins the KS6 adapter.

**Diffs.**
- Each successor is its predecessor's bytes with exact-once edits (`build_ks_chain_c2v001.py`).
- The full DIFFs are `diffs/DIFF_<successor>.diff`.

## 2. The S1_UA_C3T identity gate (in every successor)

**Where the spec is in hand** (KS1, KS2, KS3/KS4 row 32, the KS6 lo_core/lo_config/adapter/handoff, and KS5′), S1_UA_C3T means both of:
- the label fully matches `S1 transfer test C3T at u_A theta [0-9a-f]{16}; base [0-9a-f]{8}` (s1k3 L40);
- `composite_grid_spec` equals CB C3T (`76309ae3`) as canonical JSON.

The label is checked first, so no other spec reads the case block.

**Where only the identity is in hand** (KS5 `verify_bundle`, the KS6 adapter `_rho_contract`), the gate is the CB C3T grid alone.
- The identity carries no label.
- Every record of such an identity carries KS1 custody, and KS1 requires the label.
- A grid whose last break is not 3 never reads CB.

**Every gate agrees on a 14-spec battery (TESTED G-P1, G-F1).** The battery covers:
- the C3T label with the K4, C4T, K2, K5 and C6T grids;
- edited C3T grids (a leaf changed, the last break written as 3.0 or as 3.0000000000000004);
- the C4T, campaign, trailing-space, upper-hex and absent labels.

## 3. KS5′: which guard runs

**Scope rules.**
- An S1_UA_C3T `certificate_check` or `prelaunch_check` runs in a KS5 scope. There, q5b1 L73 (`guard_sha256`), L150 and L192 read KS5.
- Every other spec runs in an explicit b1 scope.
- Outside any spec (Context construction, or guard012 L256's direct `certificate_policy_gate()`), the scope is the Context's own: KS5 if its C1's policy review binds KS5's sha, otherwise b1.

**Consequence: S1_UA_C3T needs its own C1.**
- That C1 has custody deriver KS1 and a policy review with `guard_sha256` = KS5.
- Under that C1, every other spec meets b1's sha and reads policy-pending. One C1 never certifies both kinds (TESTED P-P2, P-D1, A-F3).

**Disclosed differences from q5b1 (by design).**
- For a KS5-bound C1 only, the init-time `gates['certificate_policy']` reads OK.
- For the same C1, `cache_id` binds KS5's sha.
- For every C1 that binds b1, behaviour is q5b1's (TESTED P-D1, ported WS-P3).

## 4. "Every other spec byte-identical": mechanism and evidence

**Mechanism.**
- KS1, KS2 and the KS6 modules hand every non-S1_UA_C3T call to the unchanged predecessor module object, loaded by path and sha. Their records, including the self-pins that name the producer file (custody L133, response L102/L282, lo_core L180, the adapter's self-pin, the handoff pin), are the predecessor's.
- KS5 is b1 with kept K 4.0 for every identity except CB C3T.
- KS3 and KS4 are tools whose own self-pins (runner, common, generator) necessarily name this build. Everything else they write for rows 1–31 is c3v004's.

**Evidence (TESTED).**
- **Differentials:**
  - K1-D1: every 31-row dry-plan spec and battery spec, under identical synthetic seams.
  - K2-D1: 1056 shell_plan cases.
  - K2-D2, L-D2, AD-D2, H-P1: delegation sentinels.
  - K5-D1: 252 guard cases equal to b1.
  - P-D1: equal to s1k3 c2v001 and q5b1.
  - R-D1: 130 selection tokens equal to c3v004, with the row file never read.
  - R-D2: the plan.
  - R-D3: check_eps and check_rho.
  - R-D4: run_point records for row 2. GQ_PROOF and EPS_NUMERIC are byte-identical; every other record is equal up to timing, pid and self-pins.
  - A-D1–A-D4: bundle, registry, verify and edge cases.
  - L-D1: recompute_b1 and validate_tail_arrays, plus equal bytecode for the shared functions.
  - AD-D1: K=4 calls equal to 211a3220.
- **Ported predecessor suites** (§5), all passing against the successors.
- **Port differential:** against each suite's run of record, every case has the same id and the same pass flag; the only exception is b1's two static checks, which the port replaces with KS5's two. 711 of the 723 common cases have equal normalized texts; the other 12 are classified as text artefacts in `PORT_DIFFERENTIAL_INPUT_C2V001.json` (truncation windows, argparse wrapping, a live vm_stat reading, a folder file count, left-cut tracebacks). Verdict AGREE (`synthetic/PORT_DIFFERENTIAL_C2V002.json`).

## 5. Tests

| Suite | Successor(s) | Result | Output |
|---|---|---|---|
| `test_ks_k3_chain_c2v001.py` (new) | all | **62/62**: 24 MUST_PASS, 19 MUST_FAIL, 17 DIFFERENTIAL, 2 FINDING | `synthetic/FINAL_KS_TESTS/` |
| CP-1 suite c3v004, ported (`test_s4rc1_c3v004_PORT_ks3_ks4_c2v001.py`) | KS3, KS4 | **295/295** | `synthetic/FINAL_PORT_CP1/` |
| proof-side suite c3v003, ported (`test_proof_side_c3v003_PORT_ks6_c2v001.py`) | KS6 adapter | **222/222** | `synthetic/FINAL_PORT_PS/` |
| acceptance q2 v004, ported (`tests/test_acceptance_q2_c2v004_PORT_ks6_c2v001.py`) | KS6 handoff (and KS6 adapter through it) | **129/129** | `tests/final_port_ks6_run_*/` |
| b1 guard suite, ported (`tests_b1/…_PORT_ks5_c2v001.py`) | KS5 | **54/54** | `tests_b1/FINAL_PORT_GUARD/` |
| s1k3 wrapper suite, ported (`test_wrapper_s1k3_c2v001_PORT_ks5p_c2v002.py`) | KS5′ | **25/25** | `synthetic/FINAL_PORT_S1K3/` |

**New MUST_PASS cases** use an honest S1_UA_C3T synthetic:
- KS1 custody;
- KS2 EPS with 179 shells and ρ with 10 shells (both pass KS3's row-32 checks);
- KS5 domain-3 bundles;
- a KS5′ end-to-end prelaunch certificate_check;
- KS3 row 32: plan and run_point end to end;
- KS4 bundle, registry and verify with an S1 C1;
- KS6 lo_core/lo_config at K3;
- a KS6 adapter C3T call with every state PASS;
- the KS6 handoff C3T path.

**New MUST_FAIL cases:**
- K=3 for non-S1 specs (campaign or C4T label with the C3T grid), and K=2/5/C6T and edited grids;
- a K=4 bundle certifying the K=3 point (K5-F1, P-F2, A-F4);
- mixed cases:
  - one C1 used for both kinds (A-F3);
  - a K=4 ρ or a1dcdea8 ρ for C3T, and a K=3 ρ for a K=4 point (AD-F1, AD-F2);
  - kept-3 states with edges from 4 (L-F1);
  - K=4 source pins or drift for row 32 (R-F3);
  - K=4 EPS or ρ records for row 32 (R-F4);
  - invalid row files (R-F1);
  - row-32 EPS pins (A-F1).

**Port adaptations, disclosed.** The predecessor suites are otherwise unchanged; the substitutions are in `diffs/PORT_*.diff`.
1. q2 H45 patches `HAND.execution_block`. A non-S1 call now runs in the 5ff464cc object, so the port patches that object's seam too.
2. b1's two static checks (diff confinement and literal counts) were written for b1 against v003. The port replaces them with KS5's checks against b1:
   - the diff is confined to the docstring, the import, the block after ART, and L94–95;
   - every threshold literal is unchanged, and `K != 4.0` is replaced once.
3. s1k3 WS-P6's fence source list adds KS5, which KS5′ loads.

**Not ported.**
- The mutation checks (`mutation_check_c3v004/c3v003/c2v004`).
- 6810b7c3, a1dcdea8, 12d36305 and 6654d93c have no runnable suite at a named path. They are covered by the new cases above.

## 6. Findings

1. **GQ kernel (G3), TESTED (GQ-K1).**
   - gq_geometry `c6ffb338` L39 builds `kept_region('route_a', None, 4/KPC_M)`. On the TAIL_REANCHOR uv_tail block, `_grid` gives 20736 kperp nodes at K=4 and 20720 at K=3. Only 480 nodes are shared, and 20240 K=3 nodes are absent at K=4.
   - So a K=4 GQ proof does not test the K=3 production nodes. GQ needs a K-parameterized kernel, not only KS1.
   - Its custody is also 6810b7c3 (L18–26), so the as-built GQ raises "K4 cube required" for row 32.
2. **a1dcdea8 L347, TESTED (K2-F2).** The K=4 filter keeps 0 of 936 (level 1) and 0 of 1768 (level 2) samples of the [3,4] shell, so `argmax` on an empty array would raise. KS2 filters at K=3, which keeps 386 and 716 samples.
3. **The wrapper does not check the ρ partition at prelaunch, TESTED (P-F2 note).**
   - q5b1 L168–172 checks the slot ρ's schema, custody and flags, not its partition.
   - A K=4-partition ρ for the K=3 point passes KS5′'s prelaunch check; the partition is the slot proof's job (G1).
   - The KS6 adapter refuses it at acceptance (AD-F1).

## 7. Open items for root (FORMAL from bytes unless marked)

| # | Link | Why S1_UA_C3T fails there | Needed |
|---|---|---|---|
| G1 | slot proof `lo_slot_proof_c3v003` `cd10cd59` | custody 6810b7c3 (L43, L284); producer must be a1dcdea8 (L44, L212–213); coverage and partition at K=4 (L58–60, L207–210); the anchor pair uses K=4 constants (L297) | a K=3 successor; KS4/C1 must then name it |
| G2 | SRB-ROT adapter `08e9ac0a` | custody 6810b7c3 (L52, L398); `EPS_COVERAGE` (4,182) (L74, L275–291). UNTESTED: whether library 2026f2b6's field_bound/srb_rot work at shells from 3. Deciding test: run both on a synthetic K=3 TailState with an EPS certificate on [3,182] | a successor |
| G3 | GQ: gq_geometry `c6ffb338`, gq_producer `2832ceb9`, gq_producer_b1 `3e668a2b` | custody 6810b7c3; L39 K=4 kept region (TESTED, §6) | a K-parameterized kernel and producer; the KS3 common then pins it for row 32 |
| G4 | EPS adapter `4de70486` (base `381b3eaa`) | L171 custody via a1dcdea8; L189 `shell_plan` 4..182 | a successor that pins KS2 (needed for `adapt-eps` on row 32) |
| G5 | lo_config `6654d93c` | L51 K=4 kept region | **built here** as part of KS6 (deviation) |
| G6 | consumed_states_b1 `4ca7f364`, current_source_evidence_b1 `7044e131`, execution_graph `6d59f1d0` | each derives custody with 6810b7c3 (L149, L290, L67). With the K=3 states, the acceptance inventory reads INCOMPLETE | successors; the KS6 adapter's `ENUMERATOR_SHA` and the handoff's `B1_EVIDENCE` then change |
| G7 | S1 path lib `f961839b` and its 3 CLIs (LIB_SHA) | `WRAPPER_S1K3` pins e7f52461. The plan's `sources_to_add` must also carry KS5 (KS5′ loads it under guard012's fence) and KS1 (the C1 custody deriver) | a lib successor and CLI re-pins |

**Root steps that change from the procedure.**
- **Step 3: the row file.** Root writes `s4rc1_c3/s1_c3t_specs/S1_UA_C3T_CP1_ROW32.json` by exclusive create, instead of editing POINTS.
  - It holds exactly these keys: `{schema: "S4RC1_CP1_S1_UA_C3T_ROW_KS3_C2V001", row: 32, key, label: "S1_UA_C3T", names: ["S1_UA_C3T"], spec_path: "s4rc1_c3/s1_c3t_specs/S1_UA_C3T_<k16>.cp1.spec.json", spec_sha256, distance_Mpc, q_inf}`.
  - The KS3 common verifies it against the spec's bytes. Its pin is recorded in the plan and in POINT_START.
  - The file is not sha-pinned by code (a design choice for root). The alternative is a CLI pin, which is new runner plumbing.
- **Step 6.6: the S1 C1.** Custody deriver KS1; certificate policy review with `guard_sha256` = KS5 `e394ae94…`; approved producers = the G1/G3/G4 successors once built.
- **Step 7.3:** `context_module` = KS5′, which needs G7.
- **The KS6 handoff** checks only its LO adapter pin (as v004). For S1_UA_C3T, root must supply K=3-capable deps: lo_core KS6 and guard KS5 (enumerator and evidence per G6).

## 8. Other deviations and notes

- KS1's CLI `write_new` writes into `certificates_per_point`, as 6810b7c3's does (HERE is kept). Root does not use it.
- The KS6 adapter loads 211a3220 lazily, after F9's root gate.
- On the retired paths (`produce_conditional_lo`, `saved_b1_diagnostic`), S1_UA_C3T is refused, and the predecessor body after the gate is unreachable (minimal diff).
- `compare_port_runs_c2v001.py` is superseded by c2v002. Its only change is the truncation threshold (550 → 390), because the q2 suite cuts texts at 400 characters.
- The probe outputs `synthetic/PROBE_PORT_DIFFERENTIAL*.json` are superseded by `PORT_DIFFERENTIAL_C2V002.json`.
- `dev/` holds the development build and its runs. It is superseded and not for review.

## 9. Reproduce (synthetic only; never `run`/`worker` on real points)

```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3; KS=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2
/usr/sbin/taskpolicy -b $PY -I -B $KS/test_ks_k3_chain_c2v001.py --ks-dir $KS --run-dir $KS/synthetic/<new>
/usr/sbin/taskpolicy -b $PY -I -B $KS/test_s4rc1_c3v004_PORT_ks3_ks4_c2v001.py --build-dir $KS --fixture-root $KS/synthetic/<new>
/usr/sbin/taskpolicy -b $PY -I -B $KS/test_proof_side_c3v003_PORT_ks6_c2v001.py --build-dir $KS --fixture-root $KS/synthetic/<new>/fixtures --results-dir $KS/synthetic/<new>
Q2_RUN_TAG=<tag> /usr/sbin/taskpolicy -b $PY -I -B $KS/tests/test_acceptance_q2_c2v004_PORT_ks6_c2v001.py
$PY -I -B $KS/tests_b1/test_guard_b1_c2v001_PORT_ks5_c2v001.py $KS/tests_b1/<new>
$PY -I -B $KS/test_wrapper_s1k3_c2v001_PORT_ks5p_c2v002.py --run-dir $KS/synthetic/<new>
$PY -I -B $KS/compare_port_runs_c2v002.py --ks-dir $KS --out $KS/synthetic/<new>.json $KS/PORT_DIFFERENTIAL_INPUT_C2V001.json
```
