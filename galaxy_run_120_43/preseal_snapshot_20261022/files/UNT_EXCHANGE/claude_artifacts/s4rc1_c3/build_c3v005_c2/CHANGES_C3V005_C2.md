# CHANGES_C3V005_C2: CP-1 offline verifier c3v005, every hunk mapped to A209

**Builder.** Claude2 root workflow (wf_d994f2d3) builder subagent. **Reviewer.** Codex1, as the distinct lineage (A209 item 3): it reviewed the three acceptance producers and wrote none of the c3 tools.
**Ruling.** V006 A209 (2026-10-20 14:32:13Z), items 1-4. Item 3: "Common c3v005 adds the three PINS lines and grows CANONICAL_APPROVED_PRODUCERS to six. Assembler c3v005 changes only COMMON_PATH, COMMON_SHA and its docstring. The registry, bundles and every producer pin stay byte-identical." Root adopts c3v005 in V006 before C1 is frozen.
**Built.** 2026-10-20, 14:41Z to 14:49Z (`date -u`), by exact-once text replacements on the pinned c3v004 bytes. The generator is `synthetic/dev_c3v005_a/gen_c3v005_c2.py` (`12c87bb29a7ff973aea5aa78cc21367b3de18accd375f798c32dbb366acd0422`); it reads each c3v004 file only if its bytes hash to the pin. build_c3v004 was only read (suite case T_C5_12: every file its HASHES list, unchanged in name, size and mtime).

## Files

| c3v004 (build_c3v004, sha256) | c3v005 (this folder, sha256) |
|---|---|
| `s4rc1_common_c3v004.py` `53f10e6eeef62518d7ac9cb21089331b797c5c25efeaa6df3664ff9fbbe51083` | `s4rc1_common_c3v005.py` `2308a47ce3c758b6befa0aa954fa7e2b6ad7f4cb41ed73d4b8cd1d257021e7c5` |
| `registry_assembler_c3v004.py` `cb5c61ee3d515588394c694b115aca733426db670385eddf92ed389894d065b0` | `registry_assembler_c3v005.py` `7df1c4813865b9e1245f5a91d827591a6d87963b6413ab53c50d2a542d211310` |
| `test_s4rc1_c3v004.py` `6f4ce315ff37120d3a555da525955e6f0fe57c7e1f2ae806c9f81cac913ebff4` | `test_s4rc1_c3v005.py` `a18db5b9d56ff8f9ef4458915ec903a263b0fb27389b1d1d0bc650b906089ff7` |
| `mutation_check_c3v004.py` `e758fdc2062cef7c85a48896ecc4e7d0733243633b9f1aea4c00a55b634a86a7` | `mutation_check_c3v005.py` `bbf55b5ce8b4df1a4a559e816e82e29b189f9475a43ba36c2f3e64d05dae7933` |
| `cp1_runner_c3v004.py` `3f5e5c188d4a6967afdb3bfab805d1cc8650e9c26793895096be55ca8f4f1a48` | not part of c3v005 (A209 item 3). It stays the runner of record, with common c3v004. |
| `C1_DRAFT_APPROVED_PRODUCERS_C3V004.json` `8774699ccf5a93bce79e1bb0e4cb1a66bc60d092a55b5a40876b9c8541e06961` | none. The C1 (H1) draft carries the six producers (A209 ruling 1). |

Diffs, by exclusive create: `DIFF_s4rc1_common_c3v004__c3v005.diff` (2 hunks), `DIFF_registry_assembler_c3v004__c3v005.diff` (3 hunks), and for review `DIFF_test_s4rc1_c3v004__c3v005.diff` (16 hunks) and `DIFF_mutation_check_c3v004__c3v005.diff` (6 hunks).

## The three new PINS (sha256 from bytes, 14:41Z)

Each path is absolute, realpath-equal, a regular file with one link, and has no symlink component (also suite case T_C5_01).

| PINS key | path under `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/` | sha256 | A209 |
|---|---|---|---|
| `lo_state_adapter` | `s4rc1_c3/proof_side_c3v003/lo_state_proof_adapter_c3v003.py` | `211a3220f015f8410f81e981f73355d9975d9b738a42a9d1092c28c4ae1c336c` | ruling 1, pin 4 |
| `srb_rot_adapter` | `s4rc1_c3/proof_side_c3v003/srb_rot_adapter_c3v003.py` | `08e9ac0a12cf1829f79f6df8a82c9ec6a7d174fc4bb25be76d3c049525dfae6a` | ruling 1, pin 5 |
| `b1_evidence` | `s4_acceptance_c2/offset_b1/current_source_evidence_b1_c2v001.py` | `7044e1310bb0b8cde08f7839b88b949409d15219fb24756f418224a0e7c0ddce` | ruling 1, pin 6 |

The row producer `67fddd24` is not added (A209 ruling 1: it emits no certificate proof). Suite case T_C5_04 shows that c3v005 refuses it as a seventh pin.

## Module hunks (one row per diff hunk)

| # | File | c3v005 lines | Change | A209 |
|---|---|---|---|---|
| 1 | `s4rc1_common_c3v005.py` | L77-79 (inserted after `lo_slot_proof`, L76) | The three PINS lines above, each with a trailing comment `# c3v005 (A209): C1 producer N`. | item 3 ("adds the three PINS lines"); ruling 1 pins 4-6 |
| 2 | `s4rc1_common_c3v005.py` | L93 (was L90) | `CANONICAL_APPROVED_PRODUCERS = ('eps_adapter', 'gq_producer', 'lo_slot_proof', 'lo_state_adapter', 'srb_rot_adapter', 'b1_evidence')`, with a trailing comment. | item 3 ("grows ... to six"); ruling 1 order |
| 3 | `registry_assembler_c3v005.py` | L1 | Title: c3v005, root workflow, A209, Codex1 reviews. | item 3 (docstring) |
| 4 | `registry_assembler_c3v005.py` | L25-30 | The c3v005 paragraph: common c3v005 only; the six canonical producers in ruling 1 order; only COMMON_PATH, COMMON_SHA and the docstring differ; nothing is rebuilt. | item 3 (docstring) |
| 5 | `registry_assembler_c3v005.py` | L48-49 (were L42-43) | `COMMON_PATH = HERE + '/s4rc1_common_c3v005.py'`, `COMMON_SHA = '2308a47c…'`. | item 3 (COMMON_PATH, COMMON_SHA) |

Nothing else differs. T_C5_00a checks that common c3v005 is byte-equal to c3v004 plus hunks 1-2. T_C5_00b checks that every top-level statement of the assembler after the docstring is AST-equal to c3v004 except the two pin constants.

**Not changed, on purpose (A209 item 3 is exhaustive):**
- The common module docstring. It still ends at the c3v004 paragraph; the provenance is in the trailing comments of hunks 1-2.
- The name under which the assembler registers its common (`spec_from_file_location('s4rc1_common_c3v004', COMMON_PATH)`, L57). It is only a `sys.modules` key. No code in the assembler or the common looks it up. In a process that also loads the runner (the suite), the two commons are separate module objects, and T_V09_02 and T_C5_11 check that. In root's verify run only common c3v005 loads.

**Line map for citations (c3v005 bytes):** common PINS `custody` L60, `state_enumerator` L67, new pins L77-79, CANONICAL L93. Assembler `c1_policy_gate` L349-390: required pins L361, producers L363-366, canonical check L367-371, the review read and the seven bindings L380-388 (`ok is not True` L386), `_out_root` L472-480. The c3v004 lines are 6 lower in the assembler and 3 lower after L76 in the common.

## The registry is not rebuilt, and its logic is unchanged

- Registry `s4rc1_c3/registry_c2v001/REGISTRY_31pts_20261020T140004Z.json` `2dea408ff698e265a41bac1ef2562737ae98ffd4583477632e7a79507a15e319` and manifest `REGISTRY_MANIFEST_31pts_20261020T140004Z.json` `1164bb48d733e613529696c1c6671cb49ad10b0ace2c57a5344e8ad582794eb0` were re-hashed from bytes at 14:41Z and 14:49Z: unchanged. Nothing else in them was read. They were not rebuilt.
- `assemble_bundle`, `assemble_registry`, `verify_point`, `verify_registry` and every other function are AST-equal to c3v004 (T_C5_00b). On the same synthetic inputs, c3v004 and c3v005 write equal bundles, registries and manifests, apart from `generator`, `common` and `utc` (T_C5_10). `REGISTRY_SCHEMA` stays `S4RC1_C1_CERTIFICATE_REGISTRY_C3V003`.
- So the registry 2dea408f is exactly what c3v005 would assemble, except that its `generator`/`common` fields name c3v004, which is correct for when it was built (A207).
- The only behavioural difference: `verify` (F3, L367-371) now admits pins 4-6 as canonical. A C1 holding the three-pin list still passes (T_C5_07), and any pin outside the six is still refused (T_C5_04, T_C5_05, T_F3_09, T103).

## Suite (`test_s4rc1_c3v005.py`), by diff hunk

The c3v004 cases are kept, and what each checks is unchanged: 295 of them, with the same ids. The harness changes:

| Diff hunk (c3v005 lines) | Change | Why (A209) |
|---|---|---|
| L1-20 | The c3v005 description is added above the kept c3v004 description. | item 3 |
| L55, L74 | Usage name; `SYN` text says c3v005. | item 3 (naming) |
| L96-123 | Constants: the runner of record, common, assembler and C1 draft of c3v004 (path, sha); the six A209 pins as literals; row producer 67fddd24; the exact hunk 1-2 lines. | ruling 1; item 3 |
| L146-151 | `exact_file()`: a build_c3v004 file is used only if its bytes hash to the pin. | item 3 (the runner is not rebuilt) |
| L205, L207, L211 | Manifest schema, statement and file name say c3v005. | naming |
| L240-243 | The runner is loaded from build_c3v004 by exact sha (`C` = common c3v004). The assembler is c3v005 (`A.C` = common c3v005). `A_PINS_BEFORE` is taken before the test-only V09 override. | item 3 |
| L270, L277 | A `build_c3v004` snapshot is taken before the cases run; the F11 message says c3v005. | hygiene |
| L432, L442, L447, L453, L591, L1572, L1625 | The 7 runner subprocess probes use the runner of record's path. | item 3 |
| L1404 | T_F7_01 reads the c3v004 C1 draft from build_c3v004 by exact sha. | item 3 (c3v005 ships no draft) |
| L1792-1955 | Section 19, 15 new cases (below). | items 1-3 |
| L1978-1981 | Results schema `S4RC1_C3V005_SYNTHETIC_TEST_RESULTS`; the summary records the c3v004 objects read. | naming |

**Section 19 (A209).**
- T_C5_00a: common bytes = c3v004 + hunks 1-2.
- T_C5_00b: assembler AST.
- T_C5_01: PINS = c3v004 PINS + the three, from bytes.
- T_C5_02: the canonical tuple is the six in ruling 1 order, as whole pins.
- T_C5_03: a six-pin C1 passes verify.
- T_C5_03b: a six-pin C1 passes on the end-to-end registry built from the real slot proof c3v003 (block 4ea218ea and the L30 guard).
- T_C5_04: a seventh pin, 67fddd24, is refused with exactly one blocker.
- T_C5_05: a `/./`-aliased pin 4 is refused with exactly one blocker.
- T_C5_06: a review with `ok: 1` is refused.
- T_C5_07: the three-pin C1 still passes.
- T_C5_08: a six-pin review that lists the producers in another order is refused.
- T_C5_09: c3v004 refuses the six-pin C1 with exactly the three A209 blockers.
- T_C5_10: the same registry logic as c3v004.
- T_C5_11: the runner is the runner of record.
- T_C5_12: build_c3v004 is untouched.

## Mutation check (`mutation_check_c3v005.py`)

It is adapted from c3v004, in 6 diff hunks:
- docstring;
- file set (common, assembler, suite);
- the mutant table;
- the base-file reads, with a check that the assembler pins this folder's common exactly once;
- for an assembler mutant, a byte-identical common c3v004 copy is written beside it;
- the summary schema `S4RC1_VERIFIER_MUTATION_CHECK_C3V005` and its `not_carried` note.

c3v004's MC04 (the runner's rule text) is not carried: the runner is not part of c3v005. c3v004's mutation of record b1cfc73c caught it, and T_V03_01 still runs on the runner of record.

| Mutant | Reverts | Named cases (all must fail) | Other failures |
|---|---|---|---|
| MC01 | carried V09 wrapper pin | T_V09_01, T_C5_00a, T_C5_01 | 0 |
| MC02 | carried V02 enumerator pin | T_V02_02, T_C5_00a, T_C5_01 | 1 (T_C5_10) |
| MC03 | carried slot pin | T94, T_C5_00a, T_C5_01, T_C5_02, T_C5_03, T_C5_07 | 23 |
| MC05 | A209 hunk 1, `lo_state_adapter` line dropped | T94, T_C5_00a, T_C5_01, T_C5_02, T_C5_03 | 31 |
| MC06 | A209 hunk 1, `srb_rot_adapter` line dropped | same | 31 |
| MC07 | A209 hunk 1, `b1_evidence` line dropped | same | 31 |
| MC08 | A209 hunk 2, canonical tuple back to three | T_C5_00a, T_C5_02, T_C5_03 | 5 |
| MC09 | A209 hunk 2, canonical order swapped | T_C5_00a, T_C5_02 | 0 |
| MC10 | A209 hunk 5, assembler common pin back to c3v004 | T_C5_00a, T_C5_00b, T_C5_01, T_C5_02, T_C5_03 | 5 |

MC09 is caught only by the constant and byte cases. verify reads C1 membership, not order. The C1 order is bound by the policy review (T_C5_08; wrapper L72).

## Runs (taskpolicy -b, `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B`, Python 3.12.14)

- **Dev precheck** (`synthetic/dev_c3v005_a/gen_out_1/`, byte-identical copies of the four files):
  - suite 310/310, results `0fa52eb23e3ab503cfd3027ced75060fbeec1dcb162f6d89322c6dffea792184`;
  - mutation 9/9 caught, `fac5ba008451c257d53b96afe11812c192540b9bc6c1fe917675cf1418266158`.
  - The final files were then written by exclusive create, byte-equal to these copies.
- **Suite of record** `synthetic/run_20261020T144729Z/`: **310/310 passed** (81 MUST_PASS, 229 MUST_FAIL; 295 c3v004 cases + 15 new).
  - results `TEST_RESULTS_20261020T144735Z.json` `3a779494c581546584fbccff63dfdc1f605b816aada13a4da10683efe297a404`;
  - outputs manifest `6ce9144a6510a4a9fd91c89e4b279c86a273ac0dea1ae30b2dba704251ceb8fe` (401 files);
  - console `synthetic/RUN_CONSOLE_20261020T144729Z.{stdout,stderr}.txt`.
- **Mutation of record** `synthetic/mutation_20261020T144746Z/MUTATION_RESULTS_C3V005.json` `ee32363d47569f693acaad99f1e1247891fdb7b623a210aa218d41690bbe3dde`: **9/9 caught** by their named cases. Each mutant ran the full 310-case suite.

## UNTESTED, with the deciding test

- **c3v005 `verify` on the real registry 2dea408f with the real frozen C1** (31 points, real custody derivation under taskpolicy -b). The suite uses a stub custody loader and synthetic registries. This is root's real-gate run of record (A209 item 4), after Codex3's policy review and the C1 freeze.
- **The verify CLI end to end.** Argument handling is TESTED (T_F3_21, T_F3_22); `verify_registry` is TESTED in-process. The CLI's real custody loader (`real_custody_fn`) and its output record are first exercised by the run of record.
- **Codex1's distinct-lineage review of c3v005** (A209 item 3) is pending, and so is root's adoption in V006.
