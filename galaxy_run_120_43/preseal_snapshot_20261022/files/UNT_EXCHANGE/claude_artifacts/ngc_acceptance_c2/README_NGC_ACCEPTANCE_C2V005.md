# NGC acceptance c2v005: recipes c2v002 (A180 R1, R2) and handoff c2v005 (recipes c2v002 + the A179 S2 pins)

**Status.** Root build (Claude2 workflow). Synthetic tests only. Nothing here is adopted until root rules and Claude3 (after its reset) reviews it. No NGC3198 data file was opened. No NGC per-state number, rho, SRB-ROT bound or real-call admission exists, and none was computed.

**Headline.**
- **R1: path (i), `n_recipe_path = RECOMPUTED_GAS`.** `updated_a` is recorded. The checkpoint module writes it into `iteration_NNNN/COMPLETED.json` as `updated_gas_fourier_J`, and it is the same array the solver hands the controller. So the monitor-next state N is rebuilt exactly by the controller L483 expression and admitted on TailState digest equality (TESTED, synthetic). Path (ii) is not used.
- **R2: every c2v001 DECLARED route-B input is now FORMAL.** Each is read from the V011_B_STAGES successor the driver pins, with line citations below. The provenance of every route-B admission carries no DECLARED input (TESTED, R02). The c2v001 readings are refused on a call built with the FORMAL inputs (TESTED, R21).
- **Handoff c2v005** = c2v004 + recipes c2v002 + the S2 module constants (producer `d3d0f3dd`, slot proof `ada31d12`, schema `UNT_NGC_POINT_RHO_NUMERICAL_C3V003`). **No adapter successor is built.** Adapter c2v003a holds no PENDING S2 constant; it receives the approved lists from the handoff.
- Suite: 40/40 MUST_PASS, 59/59 MUST_FAIL, twice. 4 ported tests are BLOCKED by the hard-rule guard, as in c2v004.

## Spec of record (section sha256 from awk bytes: the `## Axxx` line up to the next `## ` line, final newline excluded)

| entry | section sha256 | used for |
|---|---|---|
| A180 | `b2be080a4cbad07f0aa6ed39d8c3fa3aff4dcf9c78cf0d683f83329a9ff82dd9` | the commission (R1 (i)/(ii), R2, handoff c2v005) |
| A179 | `bd320a088c57131dfe6e5a951c8f18b5eee7ce86416fe969d5e4f5435f065bd8` | the S2 pins, adapter L548/L560 |
| A177 | `82b5f691e735ac492c69ba073af6b24a8591561aa076cffd4e1844ab2599a9ec` | the recipe commission (byte-equal to the c2v004 README value) |

V006 was read only through awk, and only these three sections. Its whole-file sha was not taken (the hard rule allows the sections only).

## Files (sha256 from bytes)

| file | sha256 | role |
|---|---|---|
| `ngc_roster_recipes_c2v002.py` | `c700f469314d73e90cd2498cdbea5b7f69fbbd9b61676468ea5e37356939978e` | recipes c2v002; S5 entry `roster_for_state` |
| `ngc_acceptance_handoff_c2v005.py` | `7077ad9337d48b444bb724b3d0dca531e615bbb09656fa00ba453bacf2e634b1` | handoff c2v005 |
| `test_ngc_acceptance_c2v005.py` | `ae045203a3c6bb2b9663ebfb807f0c1208d8177067cca4f83857a7c088802605` | suite (port of c2v004 `fcf7e43f`; c2v003a `e452cec2` loaded by sha) |
| `DIFF_RECIPES_C2V001_TO_C2V002.diff` | `868de8542a8474674692d63b2bae45ffc4a93b03a5cccd08989ccdceb6bf756d` | `diff -u` c2v001 → c2v002 |
| `DIFF_HANDOFF_C2V004_TO_C2V005.diff` | `e9f1111456b91854510bb929779586ddbbbdc5fe98036a5925717df6d00faf60` | `diff -u` c2v004 → c2v005 |
| `synthetic_c2v005/record_run_1/SUITE_RESULTS_C2V005.json` | `f4e96fb421863b72a5d2b11a01176ce3940662ef6236ecbd8df6764aa825eb67` | record run 1 |
| `synthetic_c2v005/record_run_2/SUITE_RESULTS_C2V005.json` | `44fb9b40ddfda65caa47254113dd7a3a69f23f3967bef615cb779c8eb49f741e` | record run 2 |

**Unchanged pins:**
- adapter c2v003a `9c4b6dfc`;
- enumerator `607b7f66`, reader `9335ee42`, S5 `3611e993`, contract `80cbf2f5`;
- library v002 `2026f2b6`, provider `d6c55b55`;
- driver cx3r008 `577f8c94`, controller `c5bdd055`, writer `b9247b1a`, binding `aee7af12`.

`HASHES_C2V005.txt` lists every file of this round, including the synthetic trees.

## R1: the monitor-next state N (FORMAL, from bytes)

**Read (named paths, each sha from bytes):**
- the solvers the driver pins for a tail-ON NGC call: AUX_UVT driver L329-330, chosen at driver L8622-8623. Serial `8ef3079b`, parallel `7667025b`;
- the checkpoint module `069b3935` (driver AUX L253).

**Finding.** Both solvers hand the same `updated` array to the controller and to the checkpoint module, before the convergence return:

| step | serial `8ef3079b` | parallel `7667025b` |
|---|---|---|
| `updated = physical_source_fourier(...)` | L215-216 | L330-333 |
| `uv_tail.complete_iteration(gas=gas, updated=updated, ...)` | L223-224 | L340-341 |
| `cm.complete_iteration(ck, iteration, updated=updated, ...)` | L228-229 | L345-346 |
| convergence return | L234 | L351 |
| `gas = (1-relaxation)*gas + relaxation*updated` | L240 | L357 |

The checkpoint module stores it:
- `complete_iteration`: L576-578, `payload = dict(fields, ..., updated_gas_fourier_J=_put(ck, updated))`, written as `iteration_NNNN/COMPLETED.json`.
- `_put`, L223-234: a content-addressed `.npy` blob `{blob, file_sha256, array_sha256 (typed digest, L108-111), dtype, shape}`.
- On a resumed iteration, the existing COMPLETED record must reproduce `digest(updated)` bitwise (L572-574).

The controller builds N at L481-484:
- L481 appends element a;
- L482-483: `r = self.relaxation; g_next = (1 - r) * gas + r * updated`;
- L484: `_build(a+1, _i1t(a+1, g_next))`.

**Recipe (RECIPE_ROUTE_A).** For the target `(a, next)`, and for a broken-chain `(n, next)` with n < a:
- `gas_{n+1} = (1 - r) * gas_n + r * updated_n`, verbatim and in order, where:
  - `gas_n` = `START(n).gas_fourier_J`;
  - `updated_n` = `COMPLETED(n).updated_gas_fourier_J`, read through the checkpoint module `_get`;
  - `r` = the SIDECAR_IDENTITY relaxation, as in the writer (MW L155);
- START(n) and COMPLETED(n) must be bound to the identity and the iteration, with `converged` True only at a;
- elements 0..n: element a is not loaded by MW `sidecar_elements(sdir, a)`. It is read from `elements_{a}.npz`, which must be in the sidecar finish list (file sha) and match the payload digests (controller `_array_digest` L78-81; code `ROUTE_A_SIDECAR_ELEMENT_DIGEST_MISMATCH`);
- I1-T is recomputed at n+1 and must equal the recorded `payload[n].next_i1t`;
- roster = `roster_route_a(..., elements[:n+1], ...)`.

The admission's `recipe_provenance` carries `n_recipe_path: RECOMPUTED_GAS` and `n_recipe_path_why` (the two citations above). The chain-intact `(n, next)` with n < a still maps to iteration n+1's begun state (START(n+1)), unchanged from c2v001.

**Refusals (TESTED, R15, R22, R23):**

| case | code |
|---|---|
| COMPLETED without `updated_gas_fourier_J` | `ROUTE_A_MONITOR_NEXT_GAS_UNRECORDED` |
| blob bytes not the ref | `ROUTE_A_COMPLETED_UPDATED_GAS_UNREADABLE` |
| consistent forged `updated` | `ROUTE_A_I1T_REFUSED` |
| edited `next_i1t` | `ROUTE_A_I1T_NOT_THE_RECORDED_I1T` |
| edited `elements_a` | `ROUTE_A_SIDECAR_ELEMENT_DIGEST_MISMATCH` |

## R2: the FORMAL route-B sources (V011_B_STAGES, driver L4993; every sha from bytes)

The stages, with the V011_B_STAGES key in brackets:

| kind | stage | sha |
|---|---|---|
| offset | offset | `1ede2384` |
| fs_columns | columns_v001 | `4d4c3467` |
| fs_rotation | rotation_v001 | `9922a919` |
| rfs_columns | columns_v003 | `5657503c` |
| le_columns | columns_v005 | `dd0c759b` |
| le_rotation | rotation_v005 | `e22e79e8` |

Every route-B tail stage is requested with `module_patches = [reuse_patch]` and no stage globals:
- requests: driver L8778 (offset), L8811 (columns), L8868 (fs rotation), L8922 (le rotation); gen_request L8527-8531;
- `reuse_patch`: driver L8727-8732, which sets `SEED_SHA` and `IDENTITY`, plus `PROFILE`/`PROFILE_SHA` only at a per-call geometry. For NGC, geo is None (L8570).
- reuse = `GENERALIZED['reference']['base']` = `ddo_homotopy_reference_root_worker_v001.py` `acda989d` (driver L223, L8487) = every stage's `PINS['reuse']`.
- The shim sets each patched global after the module ran (driver L709-753).

The recipe loads the reuse module by exact bytes and applies the stage request's patch as the shim does (`_stage_reuse`). The module is inert at import: its main is guarded (L129).

| input (c2v001 basis) | c2v002 FORMAL source | stage lines |
|---|---|---|
| gamma_eff, c_m_s (DECLARED: the manifest state record) | `phys = cm.decode(IDENTITY.json identity.caller.record)['physical_parameters']` of `--checkpoint-directory`, with cm = the patched `reuse.PINS['checkpoint']` (`069b3935`). The binding builds with `float(phys['gamma'])`, `float(phys['c_m_s'])`. Checks: the IDENTITY sha = `cm._sha(cm._canonical(identity))` = patched `reuse.IDENTITY` = `identity.route_a.custody`; the caller seed = patched `reuse.SEED_SHA` = `identity.seed`; the checkpoint dir = the route_a stage's. | offset L214-218; fs_columns L199-204; fs_rotation L217-222; rfs_columns L200-205; le_columns L198-203; le_rotation L223-228 |
| profile pin (DECLARED: the route-A sidecar profile) | `(reuse.PROFILE, reuse.PROFILE_SHA)` of the patched reuse module (reuse L24-25). For the production NGC call this is the reuse literal `CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json` `f5becd45`. It must equal the binding's outer-cut profile pin when one is recorded. | bind(profile=...) offset L229; fs_columns L222; fs_rotation L255; rfs_columns L230; le_columns L231; le_rotation L271 |
| offset body arrays (DECLARED: `outputs['body_arrays.npz']` or `<dir>/body_arrays.npz`) | body `finish.json` `array_file` / `array_sha256`. The body finish is bound by `--body-finish-sha256` and the uv_tail stage record. | offset L223, L226-227 |
| fs base arrays (DECLARED: outputs, else `<dir>/name`) | offset `finish.json` `outputs['updated_base_arrays.npz']` `{path, sha256}`, strictly. The offset finish is bound by the uv_tail stage record. | fs_columns L208-214; fs_rotation L228-232; rfs_columns L211-215; le_columns L209-213; le_rotation L234-238 |
| own-roster eval radii (DECLARED: `unique(base radial_nodes_m)`) | **columns kinds:** `[float(base['radial_nodes_m'][i]) for i in controls['radial_indices']]`, with controls = `--controls`, sha-pinned by `--controls-sha256`. **Rotation kinds:** `R` = joined `arrays['radial_nodes_m']`, saved unchanged in the stage's own `rotation_base_arrays.npz` (finish `arrays_path` / `arrays_sha256`). | fs_columns L192, L219-222; rfs_columns L193-195, L228-230; le_columns L190-191, L229-231; fs_rotation L237, L255, L285-286; le_rotation L260, L271, L302-303 |

The digest checks are unchanged: S5 compares the recorded roster digest before any build and admits only on TailState digest equality. New refusal codes (TESTED, R24):

| case | code |
|---|---|
| no reuse patch | `ROUTE_B_REUSE_MODULE_PATCH` |
| IDENTITY not the patched one | `ROUTE_B_CHECKPOINT_IDENTITY` |
| controls sha | `ROUTE_B_EVAL_RADII_UNRECORDED` |
| body array sha | `ROUTE_B_BODY_ARRAYS_UNRECORDED` |

R17 and R18 (an edited base file; the stage run at gamma one ulp off) still refuse, now on FORMAL inputs.

## Handoff c2v005 (the delta from c2v004, and only it)

Generated from the c2v004 bytes by listed exact replacements (dev tool in scratch); the full delta is `DIFF_HANDOFF_C2V004_TO_C2V005.diff`.
- `ROSTER_RECIPES` = `{ngc_roster_recipes_c2v002.py, c700f469…}`.
- The S2 constants:
  - `S2_PINS = {'rho_producer_sha256': 'd3d0f3ddda8be2e3d4b0e0732e5237a602cb3b1fb99d7921e8c10a886420a3c4', 'slot_proof_producer_sha256': 'ada31d121871598aa0cd7db5137691502421c873cc75bdf331706501d3f3310a'}`;
  - `S2_RHO_SCHEMA = 'UNT_NGC_POINT_RHO_NUMERICAL_C3V003'`.
- `_accept` requires `A.RHO_SCHEMA == S2_RHO_SCHEMA` (else `S2_RHO_SCHEMA_NOT_THE_ADAPTER_SCHEMA`, INCOMPLETE), and `rec['pins']` carries `s2_rho_schema`.
- The record and summary schemas move to `*_C2V005`; the loader names and CLI strings move to c2v005.

**Adapter: not rebuilt.**
- Adapter c2v003a's S2 interface reads no constant of its own for the producers. `check_slot_proof` takes `approved_slot` (L548) and `approved_rho` (L560) from the handoff (`_s2_lists`).
- Its `RHO_SCHEMA` (L125) is already `UNT_NGC_POINT_RHO_NUMERICAL_C3V003`.
- So the one-constant adapter c2v003b was not needed.

## Tests

**Record runs** (`python3 -I -B` 3.12.14, run dirs under claude_artifacts, so no ART patch):

| run | must_pass | must_fail | blocked | seconds |
|---|---|---|---|---|
| record_run_1 | 40/40 | 59/59 | P16, P18, P29, F38 | 8.9 |
| record_run_2 | 40/40 | 59/59 | P16, P18, P29, F38 | 9.0 |

The 103 entries have identical ids and ok flags across the two runs. Their details are identical once the run directory, hex digests and floats are normalized.

**Ported.**
- Every c2v003a test, through `e452cec2` loaded by sha against the c2v005 handoff.
- Every c2v004 test: this suite is the c2v004 file with its fixture moved to the FORMAL reading.
- **Re-stated for A179** (the module now holds pins, not PENDING):
  - P33 asserts the module S2 constants;
  - F41's PENDING sub-case passes PENDING explicitly; its other four sub-cases are unchanged.
- **Changed by R1/R2:**
  - R01 and R03 now admit N, and the broken-chain next state;
  - R15 is now the updated_a refusals;
  - R17 and R18 now edit FORMAL inputs.
- **BLOCKED_BY_HARD_RULE:** P16, P18, P29 and F38. They read V006 or the NGC3198 query manifest; the audit hook refuses the open before any byte is read. Those two paths are the run's only refused opens.

**New MUST_PASS:**

| id | what |
|---|---|
| P36 | c2v005 pins recipes c2v002 (sha from bytes): the prepare default, the REGISTERED approvals, the record pin; schemas C2V005 |
| P37 | the S2 module constants = A179; the schema = the adapter's; the adapter receives exactly `[ada31d12]` / `[d3d0f3dd]`; REGISTERED accepts the constants (the next check refuses) |
| R01 | all three route-A targets, N included, ADMITTED; N's digest = `payload[a].next_state_digest`; provenance `n_recipe_path` RECOMPUTED_GAS |
| R02 | all six route-B kinds ADMITTED; no DECLARED in any provenance; gamma = the caller record, profile = reuse.PROFILE, radii as tabled |
| R03 | broken chain: iteration 1's begun state, and the next state of iteration 0 (RECOMPUTED_GAS), both ADMITTED |
| R04 | custody: opens are only own outputs, pinned modules, stand-ins (including the reuse module and its PROFILE); N included |
| R05 | production toolkit: `REUSE_MODULE` = the driver's `GENERALIZED['reference']['base']` (path and sha from the driver text); refuses a synthetic call before loading anything |
| R06 | handoff `prepare_acceptance_inputs` on a recipe-fixture call: 3 route-A admissions (one RECOMPUTED_GAS), the iterate list written, prepare returns (`route_a_iterates`, `rebuild_exports`) |

**New MUST_FAIL:**

| id | what |
|---|---|
| F46 | wrong S2 sha: REGISTERED with either pin changed gives `S2_PINS_NOT_THE_MODULE_CONSTANTS`; a producer that is not the pinned one gives `NGC_RHO_RECORD_MISMATCH` in every state; an adapter `RHO_SCHEMA` C3V001 gives `S2_RHO_SCHEMA_NOT_THE_ADAPTER_SCHEMA` |
| R15 | the updated_a refusals (see R1) |
| R21 | recipes c2v001 (`6c9e8508`, exact bytes) on a FORMAL call: every route-B kind refused (fail-closed) |
| R22 | edited `next_i1t` (see R1) |
| R23 | edited `elements_a` (see R1) |
| R24 | the R2 source refusals (see R2) |

**The fixture** (`RFx`, unchanged otherwise):
- the checkpoint IDENTITY carries an encoded caller record, and its sha is `_sha(_canonical(identity))`;
- COMPLETED carries `updated_gas_fourier_J`;
- every route-B tail stage request carries the reuse patch on a reuse-module stand-in;
- the route-B states are built by the real binding with the FORMAL inputs:
  - gamma = 9·(1+2⁻²⁰), not the accepted state's gamma_eff 9.0;
  - a route-B profile file other than the route-A one, with the same stars and one more record key;
  - the body file named only by `array_file`;
  - controls ids `[2,0,3]`, `[1,3]` and `[3,2,1,0]`;
  - the rotation radii from the stage's own arrays.

These choices make R02 and R21 discriminate the FORMAL readings from the c2v001 ones.

**Dev mutation spot-check** (scratch, not a deliverable). Ten one-line mutants of c2v002, each killed by its intended test:
- N gas without updated: R01;
- relaxation one ulp off: R01;
- the element-n digest check off: R23;
- the missing-updated check off: R15;
- next_i1t not compared: R22;
- gamma from the manifest: R02;
- columns radii = `unique(base)`: R02;
- rotation radii one node short: R02;
- reuse patch not applied: R02;
- patch shape unchecked: R24.

**Observation.** Two order-only mutants survived: sorted column ids, and reversed rotation radii. On the synthetic states, the TailState digest does not depend on the order of `eval_radii_m`, only on the set (TESTED on synthetic, library v002).

## Builder choices (each is root's to overrule)

1. **R1 (i) applies to the broken-chain `(n, next)` too.** Its `updated_n` is equally recorded. The chain-intact `(n, next)` keeps the START(n+1) path.
2. **The recipe executes the reuse module** (`acda989d`, inert at import) by exact bytes to read `PROFILE`/`PINS`/`IDENTITY`/`SEED_SHA` after the patch. That is the stage's own reading. The alternative, an AST literal read, would not follow the shim exactly.
3. **Controls are read as sha-pinned files** (pinned by the stage ctx record's `--controls-sha256`), not only as own outputs. The driver writes generated controls into `<out>/inputs` (L8803) and also accepts a spec-supplied controls path (L8805).
4. **Exactly `[reuse_patch]`.** A stage request with any other module patch, or with stage globals, is refused (`ROUTE_B_REUSE_MODULE_PATCH`).
5. **No adapter c2v003b** (see above).

## Root items

- **R1. Real-call N.** It needs `COMPLETED(a)` with `updated_gas_fourier_J`. That is TESTED from the module bytes (checkpoint L576-578) and on synthetic records. On a real call it is UNTESTED; deciding test: the first call's S5 admission of N.
- **R2. The NGC route-B profile is the reuse literal** `CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json` `f5becd45` (geo None, driver L8570), not the route-A prep profile. They must agree in stars, because the stage's I1-T checks its stars against the route-A fixed source. Whether the two files coincide is UNTESTED; deciding test: the first call's S5 (fail-closed either way).
- **R3. Builder choice 2** (the recipe executes the reuse module at S5 time) is a custody ruling for root.
- **R4. An admitted body** (`adm['body']`, driver L8761-8767) lies outside the call's uv_tail stage records. The recipe then refuses the offset (fail-closed). This is not a case in the NGC plan as read; noted, UNTESTED.
- **R5. P18** (the c2v005 public entry, with the A179 pins) is BLOCKED here; deciding test: P18 run by root. The c2v004 items still stand:
  - R3 STAGE0 writer (deferred, A180);
  - R4 S5 on the run host;
  - the S10 review (Claude3).

## UNTESTED (each with its deciding test)

- **The production toolkit past its first refusal:**
  - the real reuse module load and patch;
  - the real checkpoint `decode` of the caller record;
  - the real CODEX1 profile.
  Deciding test: the first real call's S5.
- **R1, R2, R4 and R5** as above.

## Conduct and deviations

**Read** (by named path, sha from bytes):
- V006 A177, A179 and A180, by awk only;
- the c2v004 README, recipes c2v001, handoff c2v004, adapter c2v003a and suite c2v004;
- the driver `577f8c94` (cited lines);
- the solvers `8ef3079b` and `7667025b`;
- the checkpoint module `069b3935`;
- the controller `c5bdd055`, the writer `b9247b1a` and the binding `aee7af12`;
- the six V011_B_STAGES tail stages listed above;
- the reuse module `acda989d` (lines 1-31 and the line index: its PINS / PROFILE literals and its guarded main).

**Not opened:**
- the CODEX1 profile;
- the roster module;
- the prep;
- the H2 source;
- any NGC3198 target, velocity, sigma, slots or query-manifest file;
- any run tree or `~/.codex`.

**Nothing launched**, and no running process touched.

**Deviations:**
1. **The V006 whole-file sha was not taken.** Only the three section shas were (hard rule).
2. **Test-fixture monkeypatching** (as in c2v004, plus two new hooks):
   - R22: the fixture controller's `_write_new` for `iteration_a.json`;
   - R23: its `_path` for `elements_a.npz`.
3. **Scratch dev.** All dev ran in `scratchpad/ngc_recipes_v2/`. The files here were written by exclusive create, and no existing file was edited.

## Errata in the recipes c2v002 text (bytes unchanged; this README supersedes; no behaviour depends on them)

- **E1.** Docstring line 7, "chosen at driver L8623-8624": read **L8622-8623**.
- **E2.** Docstring line 27 and the `_stage_reuse` docstring (line 634), "L8783, L8810": read **L8778** (offset) and **L8811** (columns). The reuse-patch requests are L8772 body, L8778 offset, L8811 columns, L8868 fs rotation, L8872 fs feedback, L8922 le rotation and L8975 le feedback.
- **E3.** Line 940, the refusal text "driver L8783": read **L8778**.
