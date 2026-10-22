# The G-wave of the S1_UA_C3T (kept K = 3) chain, c2v001

**What this is.** The G-wave successors that V006 A175 lists and A176 commissions now (G1, G2, G3, G4, G6, plus KS3′, KS4′, KS5″ and KS6′). They were built 2026-10-19 by a Claude2 root-workflow subagent in `ks_k3_chain_c2/`, beside wave 1 (`README_KS_K3_CHAIN_C2V001.md`).

**Status.**
- **BUILT. NOT ADOPTED.** Root has not ruled and Claude3 has not reviewed.
- Every test is synthetic. Nothing was launched: no CP-1 `run`/`worker`/`rho-repeat`/`adapt-eps` on a real point, no process touched, and the live out-roots `cp1_run_c3v004*` are fenced in every new suite.
- No existing file was edited. Every deliverable here was created by exclusive create. The fences refused 0 opens.

**Bottom line for root.**
- **Row 32 is now certified and accepted end to end in synthetic tests.** The flow is: plan, then `run_point`, then adapt-eps, then the slot proof, then bundle and registry, then verify against the canonical S1 C1, then the KS5″ prelaunch check, then acceptance.
  - `run_point` runs the real G3 GQ on synthetic geometry: 20720 production nodes, TESTED PASS.
  - adapt-eps goes through G4 with 179 shells from [3,4]. The slot proof is the real G1.
  - Acceptance reads **ACCEPTED** through the KS6′ handoff and adapter, G2 SRB-ROT, the G6c inventory and guard KS5.
- **G3 equivalence: TESTED.** The K=3 GQ certificate is c6ffb338's computation with only the kept K substituted (§4).
- **G2 deciding test: TESTED.** Library 2026f2b6 works at shells from 3, so the library needs no change. The adapter successor was built (§3).
- **Every other spec runs the unchanged predecessor object.** This is TESTED by DIFFERENTIAL cases and by ten ported predecessor suites whose case outcomes equal their runs of record (§5, §6).
- **G7 (S1 lib v002c) is open, as A175 scopes it.** §7 lists what it must carry, including the fence sources.

Labels: **TESTED** means shown by a test here or read from bytes. **FORMAL** means it follows from the cited code. **UNTESTED** means the deciding test is named.

## 1. Chain table

All sha256 values are computed from bytes. Full values are in `HASHES_GWAVE_C2V001.txt`.

### G-wave (this build; `build_gwave_c2v001.py`, every edit exact-once, DIFFs in `diffs/DIFF_<successor>.diff`)

| Id | Successor | sha256 | Predecessor | Change (S1_UA_C3T only; every other spec goes to the predecessor object) |
|---|---|---|---|---|
| G3 geometry | `gq_geometry_r5_cx2v001_g3_c2v001.py` | `572c86c6` | c6ffb338 | Custody KS1. L39 kept region at the spec's kept K (3). |
| G3 producer | `gq_producer_cx2v005_g3_c2v001.py` | `c3699c78` | 2832ceb9 | Kernel is the G3 geometry, under its own module name (MAP H7). |
| G3 producer b1 | `gq_producer_b1_c2v001_g3_c2v001.py` | `8893213e` | 3e668a2b | Same, for `produce()`. `signed_bound` and `policy` are 3e668a2b's text. |
| G4 | `point_response_admission_adapter_cx2v003_g4_c2v001.py` | `e00ab71d` | 4de70486 (base 381b3eaa) | PR is KS2, CU is KS1, RESPONSE_SHA is KS2. The shell plan is 3..182 (179 shells). |
| G1 | `lo_slot_proof_c3v003_g1_c2v001.py` | `6af9ed6c` | cd10cd59 | Custody KS1. The slot ρ uses the K=3 contract: [3,182], 10 shells, KS2 producer (sha and bytes). The anchor pair stays K=4. |
| G6a | `execution_graph_cx2v002_g6_c2v001.py` | `ba58fb18` | 6d59f1d0 | Custody KS1. |
| G6b | `current_source_evidence_b1_c2v001_g6_c2v001.py` | `65834e9b` | 7044e131 | L is the KS6 lo_config 510ff07b (MAP H1 (a)), G is the G3 b1 producer, and C is KS1. |
| G6c | `consumed_states_b1_c2v001_g6_c2v001.py` | `4ea0c2ca` | 4ca7f364 | A is G6b and X is G6a. The inventory producer pin names G6c. |
| G2 | `srb_rot_adapter_c3v003_g2_c2v001.py` | `7eb456cd` | 08e9ac0a | Custody KS1, EPS coverage [3,182], and the inventory producer is G6c (MAP H3). |
| KS5″ | `calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v003.py` | `51a6fb27` | KS5′ 66560a6a | Adds the S1-only ρ slot check in `certificate_check` (A175, ADV-D1/D2). |
| KS3′ common | `s4rc1_common_c3v004_ks3_c2v002.py` | `fcd63a73` | KS3 736d2e7e | New PINS: G3 (2), G4, G1, G6c, KS5″. Adds `CANONICAL_APPROVED_PRODUCERS_S1` = (G4, G3, G1) and `s1_rho_slot_problems`. |
| KS3′ runner | `cp1_runner_c3v004_ks3_c2v002.py` | `da08d725` | KS3 54595c2d | Row 32: GQ is G3 (`check_gq` wants it). The EPS review request and adapt-eps bind G4. |
| KS4′ | `registry_assembler_c3v004_ks4_c2v002.py` | `85c3343d` | KS4 080ed171 | The S1 C1 has the canonical list (G4, G3, G1) and the enumerator G6c. The manifest draft names G6c and KS5″. Verify adds the S1 ρ check. |
| KS6′ adapter | `lo_state_proof_adapter_c3v003_ks6_c2v002.py` | `c8dc59a1` | KS6 8fa371a7 | The inventory producer is chosen by identity: G6c for the CB C3T grid, 4ca7f364 otherwise. |
| KS6′ handoff | `acceptance_handoff_c2v004_ks6_c2v002.py` | `7bb37957` | KS6 6642d209 | On the S1 path: `LO_ADAPTER_KS6` is KS6′, and `trusted_source_producers` must name G6b. |

### Wave 1 (unchanged; pinned by the G-wave)

| Id | File | sha256 |
|---|---|---|
| KS1 | `custody_cx2v002_ks1_c2v001.py` | `ad020470` |
| KS2 | `point_response_producer_cx2v002_ks2_c2v001.py` | `99c29df6` |
| KS3 | `s4rc1_common_c3v004_ks3_c2v001.py`, `cp1_runner_c3v004_ks3_c2v001.py` | `736d2e7e`, `54595c2d` (superseded by KS3′) |
| KS4 | `registry_assembler_c3v004_ks4_c2v001.py` | `080ed171` (superseded by KS4′) |
| KS5 | `certificate_guard_b1_ks5_c2v001.py` | `e394ae94` (unchanged; the S1 guard) |
| KS5′ | `calibration_orchestrator_cx2v006r10_c4_q5b1_s1k3_c2v002.py` | `66560a6a` (superseded by KS5″) |
| KS6 | `lo_core_r5_cx2v001_ks6_c2v001.py`, `lo_config_r5_cx2v001_ks6_c2v001.py` | `2cf7c597`, `510ff07b` (unchanged) |
| KS6 | `lo_state_proof_adapter_c3v003_ks6_c2v001.py`, `acceptance_handoff_c2v004_ks6_c2v001.py` | `8fa371a7`, `6642d209` (superseded by KS6′) |

**Re-pinning is consistent: TESTED (X-P1, X-P2 from bytes).**
- G3 producer and G3 producer b1 pin the G3 geometry. G3 geometry pins KS1.
- G4 pins KS2 (and through it KS1).
- G1, G2 and G6a pin KS1. G6b pins the KS6 lo_config and the G3 producer b1. G6c pins G6b and G6a.
- G2, KS6′ adapter and the KS3′ common pin G6c.
- The KS3′ common pins G3, G4, G1, G6c and KS5″, and keeps every wave-1 and c3v004 pin.
- The KS3′ runner and KS4′ pin the KS3′ common. KS5″ pins KS5 and the KS2 pin.
- The KS6′ handoff pins the KS6′ adapter and G6b.

## 2. The S1_UA_C3T gate (unchanged from wave 1)

**Where the spec is in hand,** S1_UA_C3T means both of:
- the label fully matches `S1 transfer test C3T at u_A theta [0-9a-f]{16}; base [0-9a-f]{8}`;
- `composite_grid_spec` equals CB C3T (`76309ae3`) as canonical JSON.

The G-wave spec gates are KS1's `s1_c3t_spec` (G3, G4, G6a/b/c), G1's and G2's own copies, and those of KS3′, KS5″ and KS6′.

**Identity-only sites** (G1 `check_rho_record`, G2 `format_eps`/`check_inventory`, KS6′ `check_inventory`) decide by the CB C3T grid alone, as KS5 does.

**Every gate agrees on the wave-1 14-spec battery: TESTED (G-P1, G-F1).**

## 3. G2 deciding test (run first: `g2_deciding_test_c2v001.py`, 2026-10-19 21:17Z in dev; final run 22:04Z, `synthetic/FINAL_GWAVE_G2_DECIDING/`)

**Result, TESTED: library 2026f2b6's `field_bound` and `srb_rot` work at shells from 3.**
- The library's own `build()` gives a K=3 le_rotation TailState (kept cube 3, synthetic source and quadrature) with unit shell edges from 3.0, and its [3,4) shell is nonzero.
- Both functions run with an EPS certificate on [3,182].
- With a certificate on [4,182] (08e9ac0a's coverage), both refuse `UV_TAIL_EPS_COVERAGE` at [3,4).
- So the library needs no change. The adapter does: EPS coverage from the kept K, KS1 and the G6c enumerator.
- The same test runs again as case G2-T in the suite. Then G2-P1 runs the successor end to end to PASS on a real K=3 TailState with the KS2 EPS record of the end-to-end run.

## 4. G3 equivalence evidence (TESTED, synthetic)

- **GQ-E1, the code-object diff.** The successor's `produce` AST, with its first statement (the S1 gate) removed and `kept_k(spec)` replaced by the constant 4, is identical to c6ffb338's.
  - `co_names` adds only `P`, `kept_k`, `produce` and `s1_c3t_spec`.
  - `co_consts` loses only `4` and gains only the call's kwnames tuple.
  - The G3 producer and producer b1 `produce` functions equal their predecessors' once the gate is removed. `policy` and `signed_bound` are AST-identical.
- **GQ-E2, the same computation.** The successor's record is identical, field for field, to c6ffb338 with exactly one in-memory substitution (L39, `4/` to `3/`), apart from the producer and custody_deriver pins and the seconds.
  - Both runs used the same synthetic geometry and the real roster and library.
  - The kperp node arrays are bitwise equal.
  - A K=4 control on the same spec gives 20736 nodes.
- **GQ-E3, independent recomputation.** The suite re-implements the kept region and the kperp node grid from the library's documented definition (B = {0, K, √2K, K_big}, uniform GL panels, alpha-phase marching from the cube corner) without calling it.
  - The successor used the kept region {cube, K 3.0} on stage `route_a`.
  - Its 20720 nodes are bitwise equal to the recomputation. The K=4 control's 20736 nodes equal the K=4 recomputation.
  - 20240 K=3 nodes are absent at K=4. This matches wave-1 GQ-K1.
- **GQ-P1.** The S1 GQ through the G3 producer reads TESTED PASS, with production_nodes = nodes_tested = 20720.
  - The pins are: producer G3 producer, numeric_producer G3 geometry, custody_deriver KS1.
  - KS3′ `check_gq(s1=True)` passes every check. The rows 1-31 rule refuses its producer pin.

## 5. Tests

| Suite | Successor(s) | Result | Output |
|---|---|---|---|
| `test_gwave_c2v001.py` (new) | all | **43/43: 18 MUST_PASS, 12 MUST_FAIL, 3 EQUIVALENCE, 9 DIFFERENTIAL, 1 DECIDING** | `synthetic/FINAL_GWAVE_TESTS/` |
| wave-1 KS suite, ported (`test_ks_k3_chain_c2v001_PORT_gwave_c2v001.py`) | KS3′, KS4′, KS5″, KS6′ | **62/62** | `synthetic/FINAL_GWAVE_PORT_KS/` |
| CP-1 suite c3v004, ported (`test_s4rc1_c3v004_PORT_gwave_c2v001.py`) | KS3′, KS4′ | **295/295** | `synthetic/FINAL_GWAVE_PORT_CP1/` |
| proof-side suite c3v003, ported (`test_proof_side_c3v003_PORT_gwave_c2v001.py`) | G1, G2, KS6′ adapter | **222/222** | `synthetic/FINAL_GWAVE_PORT_PS/` |
| acceptance q2 v004, ported, plus 8 new S1 cases (`tests_gwave/…`) | KS6′ handoff (and KS6′, G2, G6c, G1 through it) | **137/137 (129 ported + 8 new)** | `tests_gwave/final_gwave_run_*/` |
| s1k3 wrapper suite, ported (`test_wrapper_s1k3_c2v001_PORT_gwave_c2v003.py`) | KS5″ | **25/25** | `synthetic/FINAL_GWAVE_PORT_S1K3/` |
| b1 GQ suite, ported (`tests_b1_gwave/test_gq_b1_…`) | G3 producer b1 | **21/21** | `tests_b1_gwave/FINAL_GQ/` |
| b1 evidence suite, ported, DELEGATED / S1 modes | G6b | **33/33 / 34/34** | `tests_b1_gwave/FINAL_EVIDENCE_*/` |
| b1 enumerator suite, ported, DELEGATED / S1 modes | G6c | **40/40 / 40/40** | `tests_b1_gwave/FINAL_ENUMERATOR_*/` |
| r5 closure, ported (`tests_r5_gwave/…`) | G3 producer, G4, G6a | **28/28** | `tests_r5_gwave/FINAL_R5/` |

**New suite** (`test_gwave_c2v001.py`).
- **MUST_PASS:**
  - pins (X-P1/2) and gates (G-P1);
  - GQ-P1;
  - the end-to-end chain E-P1 to E-P7: plan; `run_point` of row 32 with the real G3 GQ and the real KS2 `produce_eps`/`produce_rho` (schema-valid numeric doubles); `adapt_point` through G4; the G1 slot proof; KS4′ bundle and registry; KS4′ verify against the canonical S1 C1 (`canonical_producers=None`); the KS5″ prelaunch `certificate_check`;
  - G4-P1, G2-P1 (SRB-ROT PASS);
  - G6-P1 (graph), G6-P2 (evidence `verify_point` against the real K=3 production grid, 20720 kperp), G6-P3;
  - K6-P1/P2.
- **MUST_FAIL:**
  - K=3 for non-S1 specs, K=2/5/C6T and edited grids (G-F1, GQ-F1);
  - K=4 artefacts at the K=3 point:
    - GQ-F2, a K=4-node or 2832ceb9-pinned GQ record;
    - G4-F1: an a1dcdea8 or shells-from-4 EPS record, a review binding 4de70486, G4 unapproved, and 4de70486 itself;
    - G1-F2/F3: a K=3 anchor pair, a K=3 ρ for a K=4 point, cd10cd59 itself;
    - G2-F1: a 4ca7f364 inventory, the [4,182] EPS, 08e9ac0a;
  - mixed cases: E-F1 (a 4de70486 review for row 32), E-F2 (an S1 C1 with the K=4 producers, 4ca7f364 or 6810b7c3), K6-F1 (crossed inventories);
  - the three A175 ADV-D cases (G1-F1, and KF-ADV-D at KS4′ verify and KS5″ prelaunch):
    - K=4 partition from [4,5], with coverage [4,182] and with [3,182];
    - merged [3,5];
    - producer a1dcdea8.

    KF-ADV-D also shows that wave-1 KS5′ accepted all four.
- **EQUIVALENCE:** GQ-E1/E2/E3. **DECIDING:** G2-T.
- **DIFFERENTIAL:** GQ-D1/D2/D3, G4-D1, G1-D1, G2-D1, G6-D1, K6-D1, R-D1 (§6).

**New acceptance cases** (q2 port, GW00-GW07). An S1_UA_C3T call reads ACCEPTED end to end (GW01), with:
- 8 states, all PASS;
- the KS6′ adapter's call reading PASS;
- the G6c inventory and G2 SRB-ROT PASS;
- guard KS5 ok;
- LO proofs from [3,4].

MUST_FAIL:
- the 4ca7f364 inventory (INCOMPLETE);
- a trusted list without G6b;
- 08e9ac0a SRB;
- the 211a3220 or wave-1 KS6 adapter pin (refused before anything is read);
- guard b1 (domain K 3 refused);
- a K=4 or a1dcdea8 ρ slot, which never gets a G1 proof.

**Port adaptations, disclosed.** All are marked `PORT (G-wave)` in the ports, and the diffs are in `diffs/PORT_*_gwave_*.diff`.
1. **KS suite.**
   - The six superseded modules load from the G-wave names.
   - X-P1 checks the `wrapper_s1k3_ks5pp` pin.
   - The row-32 GQ stub carries the G3 producer pin.
   - P-F2's K=4 ρ slot now reads refused (A175; wave 1 read ok).
   - An S1 C1 names G6c.
   - C3T inventories name G6c.
2. **CP-1, proof-side and q2.** File names only, plus the q2 run folder `tests_gwave/`. The q2 port also has the GW section appended (new cases, not ported ones).
3. **Wrapper.**
   - The module name is c2v003.
   - KS5 is read from the wave-1 folder.
   - The synthetic lo slot carries the K=3 contract, because KS5″ now reads it.
4. **b1 suites.**
   - The module under test is the G-wave successor.
   - The b1-vs-v0xx diff-scope checks become "successor = predecessor plus exactly the listed build edits" (re-rendered from the build).
   - MP10 checks the G3 kernel. MP09 removes the S1 gate before comparing ASTs.
   - **Evidence and enumerator run twice.**
     - DELEGATED: the suite's non-S1 spec, with seams on the delegated b1 object. Every check must hold with the b1 module's own records.
     - S1: the same spec with the C3T label and grid, with seams on the successor. Every check must hold with the successor's self-pins, and the mutants run here.
     - In DELEGATED mode the two mutant checks are replaced by one delegation sentinel.
5. **r5 closure.**
   - G, P and X are the successors. Their custody is KS1 over 6810b7c3, and P's producer is KS2 over a1dcdea8.
   - The GQ library check reads certs common c75aaa5a directly, so the driver is not imported.
   - The three checks that derive custody from real template inputs are not run, under the synthetic-only rule. 6810b7c3 is unchanged.
   - Writes go to the port's own folder.

**Port differential at case level (`compare_gwave_port_ids_c2v001.py`, `synthetic/FINAL_GWAVE_PORT_DIFFERENTIAL.json`): AGREE on all 11 suite runs.**
- For every ported suite, each common case id has the same pass flag in the run of record and in the G-wave run.
- The only ids in just one run are the G-wave additions (q2 GW*, evidence `MF_delegated_mode_*`) and the disclosed removals (the 2 DELEGATED-mode mutants, and the 3 real-input r5 checks).

**Not ported.**
- The mutation checks (`mutation_check_c3v004/c3v003/c2v004`).
- The wave-1 port-text differential tool (case-level only here).
- There is no runnable suite at a named path for c6ffb338 alone. It is covered by the r5 port (through G3) and by GQ-E1 to E3.

## 6. Non-S1 identity evidence (TESTED)

- **Mechanism.** Every G-wave entry that takes a spec hands any non-S1_UA_C3T spec to the unchanged predecessor module object, loaded by path and sha, so its records, self-pins included, are the predecessor's. The entries are:
  - G3 `produce` (×3), G4 `adapt_eps`, G1 `prove_lo_slot`/`main`, G2 `adapt_call_srb_rot`/`main`;
  - G6a `expected_stages`/`validate_graph`;
  - G6b `assemble_current`/`export_lo_source`/`verify_point`/`verify_occurrence`;
  - G6c `consumed_states`.

  KS3′, KS4′, KS5″ and KS6′ change only S1 branches (as wave 1 did).
- **Sentinels:** GQ-D1, G4-D1, G1-D1, G2-D1, G6-D1 and K6-D1 confirm the delegation on rows 1, 2 and 29 and on every non-S1 battery spec.
- **Byte-identical K=4 outputs:**
  - GQ-D2: the full K=4 GQ record, 20736 nodes, against a separately loaded 2832ceb9;
  - G4-D1: the full K=4 adapt_eps result against 4de70486, on a real a1dcdea8 record;
  - G6-D1: the K=4 graph against 6d59f1d0;
  - G1-D1: `check_rho_record` against cd10cd59 on 12 records and identities;
  - G2-D1: `format_eps` and `check_inventory` against 08e9ac0a;
  - K6-D1: KS6′ `check_inventory` against KS6;
  - R-D1: `check_gq` against KS3.
- **Spec-free functions.** G3 `policy`/`signed_bound` and G6b `compute_i1t`/`verify_gas`/`verify_product`/`_approved` are AST-identical to the predecessors'. GQ-D3 shows equal outputs apart from the self-pin.
- **Ported suites.** The predecessors' own suites pass unchanged on K=4/non-S1 inputs. The case-level differential is in §5.

## 7. Open items and root steps (FORMAL from bytes unless marked)

| # | Item | Needed |
|---|---|---|
| G7 | S1 path lib v002c (follows lib v002b, A172) | Re-pin the wrapper to **KS5″** (`51a6fb27`), not e7f52461. Under guard012/013's fence (L159-169: every `.py` opened under `/Research/` must be a pinned source), the S1 prelaunch reads: q5b1 L68-69 (every C1 pin: KS1, G6c, the review and registry), L157 (the EPS and slot-proof producers: G4, G1), KS5's `verify_bundle` (`_read(producer)`: G3 producer), KS5″'s ρ check (the KS2 bytes), and the modules KS5″ loads (q5b1's set plus KS5). So `sources_to_add` must carry KS5″, KS5, KS1 (and 6810b7c3, which KS1 loads), KS2, G4, G3 producer, G1 and G6c. UNTESTED. Deciding test: the guard's adoption plus prelaunch of an S1_UA_C3T spec inside the fence with lib v002c's sources. |
| C1 | The S1 C1 (procedure step 6.6) | Custody deriver KS1; `state_enumerator` G6c (`4ea0c2ca`; KS4′ refuses anything else for row 32); `approved_certificate_producers` = [G4 `e00ab71d`, G3 producer `c3699c78`, G1 `6af9ed6c`]; certificate policy review `guard_sha256` = KS5 `e394ae94`. |
| HO | Handoff deps for the S1 call | enumerator G6c, evidence G6b (`65834e9b`), lo_core KS6 `2cf7c597`, guard KS5, `srb_adapter` G2 (`7eb456cd`, entry `adapt_call_srb_rot`), `lo_adapter` = KS6′ (`c8dc59a1`). Root's `trusted_source_producers` must name G6b. The handoff still checks only its LO adapter pin (as v004 and KS6), so root supplies the rest. Writer `808cfe6a` and row producer `67fddd24` are K-free (MAP H5 resolved from bytes: neither loads custody, and `kept` is copied from the call's own records). |
| R32 | Row file (step 3) | As A175: root writes it once u_A is fixed and records its sha in V006 before any row-32 run. |
| RUN | Real GQ, EPS and ρ at row 32 | UNTESTED on real inputs. The G3 node count (20720) matches K=4's cost (20736). Deciding test: the CP-1 row-32 run itself (after G7 and root's rulings). |

## 8. Deviations and notes

- **G2 order.** The deciding test was run first (dev, 21:17Z). The successor was then built, and the final run order was deciding test, then build (22:04Z).
- **Spec-free functions stay the successor's text.** This is wave 1's convention. MAP H8 offered "keep the predecessor's objects". The outputs are equal up to the self-pin (GQ-D3, AST checks).
- **G6b binds the KS6 lo_config directly** (MAP H1 (a)). There is no lo_producer v004 successor.
- **G6b pins the G3 producer b1** (its only uses are `signed_bound`/`policy`). The signed-GQ records are unchanged in content.
- **G3 producer b1 has no other consumer in the chain.** Its `produce()` is not the uniform producer of record (offset_b1 README).
- **Stricter-only additions on the S1 path:**
  - KS4′ requires the S1 C1's `state_enumerator` to be G6c.
  - KS5″ runs the ρ check at both phases of an S1 `certificate_check` (prelaunch, so `prelaunch_check`, and acceptance).
- **Identity-only decisions.** G1's contract is chosen by the expected identity it is given: none (the anchor pair) means K=4. G2's EPS coverage for S1 is (3, 182), the kept K of the CB C3T grid (FORMAL: the S1 identity implies K = 3).
- **Reads beyond named paths** (all code or record files, none forbidden):
  - offset_b1 `README.md` and its `tests/` suites;
  - CERT `test_r5_closure_cx2v002.py` (ported), plus the heads of four other CERT test files, used to locate suites;
  - the library's sibling roster `4366e3d6` and provider `d6c55b55` (cited by reconstruction b8471197);
  - r14 `f3f9ba7e` (G2's apply_flag);
  - guard012 `f4656fec` (fence semantics; cited by the wrapper port);
  - the writer and row producer (cited by the q2 port).
- **V006.** Its sha is now `01497680`, because A177 was appended after the MAP's read of `8322c9f0`. Only the A160, A170, A172, A175 and A176 sections were read.
- **CP-1 port probes.** As in wave 1, the CP-1 port's CLI probes call the runner with `run`/`worker`/`rho-repeat` in ways that are refused at setup (exit 2, nothing created; asserted by T23-T26 and T_A10). Its F4 probe runs `run_point` on synthetic producer doubles. No point is computed.
- **The first final proof-side port run read 221/222** (). Its H02_F11 check snapshots the suite's own folder outside  before and after the run, and the other suites, launched in parallel in the same folder, wrote ,  and  while it ran. Run alone (), it read 222/222. The dev run also read 222/222. Both runs are kept.
- **Walks inside ported suites.** The ported proof-side and CP-1 suites (the predecessors' own code, as wave 1 ran them) walk their own folder and the build folders their hygiene checks name. They read names, sizes and mtimes only, under the suites' own fences. No walk was added here.
- **The dev folder holds superseded work, not for review:** `dev/gwave_dev_001`-`003`, `dev/gw_test_*`, `dev/port_*`, `dev/g2_deciding_dev_001` and `dev/probe_coeff.npz`.
- **The build run's JSON output** was saved as `synthetic/FINAL_GWAVE_BUILD_OUTPUT.json.tmp_not_used` (a redirect name). It is the record of the final build; the name is cosmetic.

## 9. Reproduce (synthetic only; never `run`/`worker` on real points)

```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3; KS=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_c2
$PY -I -B $KS/g2_deciding_test_c2v001.py --out-dir $KS/synthetic/<new>
/usr/sbin/taskpolicy -b $PY -I -B $KS/test_gwave_c2v001.py --gw-dir $KS --run-dir $KS/synthetic/<new>
/usr/sbin/taskpolicy -b $PY -I -B $KS/test_ks_k3_chain_c2v001_PORT_gwave_c2v001.py --ks-dir $KS --gw-dir $KS --run-dir $KS/synthetic/<new>
/usr/sbin/taskpolicy -b $PY -I -B $KS/test_s4rc1_c3v004_PORT_gwave_c2v001.py --build-dir $KS --fixture-root $KS/synthetic/<new>
/usr/sbin/taskpolicy -b $PY -I -B $KS/test_proof_side_c3v003_PORT_gwave_c2v001.py --build-dir $KS --fixture-root $KS/synthetic/<new>/fixtures --results-dir $KS/synthetic/<new>
Q2_RUN_TAG=<tag> /usr/sbin/taskpolicy -b $PY -I -B $KS/tests_gwave/test_acceptance_q2_c2v004_PORT_gwave_c2v001.py
$PY -I -B $KS/test_wrapper_s1k3_c2v001_PORT_gwave_c2v003.py --run-dir $KS/synthetic/<new>
$PY -I -B $KS/tests_b1_gwave/test_gq_b1_c2v001_PORT_gwave_c2v001.py $KS/tests_b1_gwave/<new>
GW_PORT_MODE=DELEGATED|S1 $PY -I -B $KS/tests_b1_gwave/test_evidence_b1_c2v001_PORT_gwave_c2v001.py $KS/tests_b1_gwave/<new>
GW_PORT_MODE=DELEGATED|S1 $PY -I -B $KS/tests_b1_gwave/test_enumerator_b1_c2v001_PORT_gwave_c2v001.py $KS/tests_b1_gwave/<new>
$PY -I -B $KS/tests_r5_gwave/test_r5_closure_cx2v002_PORT_gwave_c2v001.py $KS/tests_r5_gwave/<new>
$PY -I -B $KS/compare_gwave_port_ids_c2v001.py $KS/synthetic/FINAL_GWAVE_PORT_DIFFERENTIAL_INPUT.json $KS/synthetic/<new>.json
```
