# NGC acceptance c2v004: the NGC roster recipes (route A, route B) and the handoff that pins them (V006 A177)

**Status.** Root build (Claude2 workflow). Synthetic tests only. Nothing here is adopted until root rules and Claude3 (after its reset) or Claude4 (after Fri) reviews it. No NGC3198 data file was opened. No NGC per-state number, rho, SRB-ROT bound or real-call admission exists, and none was computed.

**Headline.**
- The recipes rebuild every consumed non-accepted state of a synthetic call, and S5 admits each on exact TailState digest equality (TESTED). The one exception is the monitor-next state of the accepted iteration. The recipes are `RECIPE_ROUTE_A` and `RECIPE_ROUTE_B_<kind>` for offset, fs_columns, fs_rotation, rfs_columns, le_columns and le_rotation.
- **The monitor-next state N is refused: `ROUTE_A_MONITOR_NEXT_GAS_UNRECORDED`.** Its gas gas_{a+1} is not recorded by any named code. Builder choice 1 of c2v003 enumerates N, so **every real call still reads INCOMPLETE** (`ROUTE_A_ITERATE_SOURCE_UNESTABLISHED`). This is root item R1.
- Route-B inputs that the binding receives from its stage successor are labelled DECLARED. The successors are not named paths under A177. S5's digest checks make a wrong DECLARED reading a refusal, never an admission (TESTED, R17 and R18). On a real call they are UNTESTED.

## Spec of record (section sha256 from awk bytes: the `## Axxx` line up to the next `## ` line, final newline excluded)

| entry | section sha256 | used for |
|---|---|---|
| A177 | `82b5f691e735ac492c69ba073af6b24a8591561aa076cffd4e1844ab2599a9ec` | the commission (recipes, c2v004, the note-3 tests, the README wording) |
| A162 | `49ef90da0bf2de4237c241aef2dd275ca51f794513c72357d362896dc1fa902d` | S5 rebuild-export (item 2) |
| A167 | `96cb1404cd63b11768bcc546eada8c47b7c46cc8bb3fbb55d74765ad4dd52ae3` | the adopted adapter and handoff c2v003a |
| A153 / A155 | `aa079db7…` / `ed6b144b…` | unchanged (pinned in the adapter) |

The A153, A155, A162 and A167 hashes are byte-equal to the values in the c2v003 README. The V006 file was read only by awk, and only these sections. V006 file sha at build: `a870853426ca96a1f765232f7d4fa399f4aee40a5c9fdf2ca325436942cf771b`.

## Files (sha256 from bytes)

| file | sha256 | role |
|---|---|---|
| `ngc_roster_recipes_c2v001.py` | `6c9e8508cb590e764bda8643caf48c931359bc7318674b1a150ccd43d9ccebce` | the recipes; S5 entry `roster_for_state` (production toolkit) |
| `ngc_acceptance_handoff_c2v004.py` | `2721cfd1d27f6b05b831ba53b02a99125bd49033d235530b911453696bb8f29d` | handoff c2v004: c2v003a plus `ROSTER_RECIPES` = `6c9e8508…` |
| `test_ngc_acceptance_c2v004.py` | `fcf7e43f2cfbf1c4f059e30b48cb07ebbff591bd7e765d4975dc21ac0c4e52f4` | 38 MUST_PASS, 54 MUST_FAIL run; 4 ported tests BLOCKED |
| `synthetic_c2v004/record_run_1/SUITE_RESULTS_C2V004.json` | `997875d3c284e3605d8c735d4048528d48a2f09282e09fa870a66444a8413ce1` | record run 1 |
| `synthetic_c2v004/record_run_2/SUITE_RESULTS_C2V004.json` | `0ae9d20b7acae723691f35fecbbf432ff484004f18febc33dea1ae56beece6c0` | record run 2 |

**Unchanged pins:**
- adapter c2v003a `9c4b6dfc` (adopted, A177);
- enumerator `607b7f66`, reader `9335ee42`, S5 `3611e993`, contract `80cbf2f5`;
- library v002 `2026f2b6`, provider `d6c55b55`;
- driver cx3r008 `577f8c94`, controller `c5bdd055`, manifest writer `b9247b1a`, route-B binding `aee7af12`.

`HASHES_C2V004.txt` lists every file of this round, including the synthetic trees.

## The S5 interface

S5 (`3611e993` L273-309) calls `roster_for_state(call_dir, out_dir, result, target, lib, provider)` and receives `{roster, build{config, kept, gamma_eff, c_m_s, eval_radii_m, i1t, stage_kind}, provenance}`.
- Recorded roster digest: S5 checks `roster.digest()` against it first (route B: `finish.json uv_tail.roster_digest`).
- Build and admission: S5 builds with the pinned library and admits only on TailState digest equality. The recipe never builds.
- Custody: every input comes from the call's own records, with paths resolved inside `<call>/out`, or from a file pinned by sha in those records or in the named code.
- Provenance: the admission records, for each input, its basis (FORMAL or DECLARED) and its citation.
- Toolkit: the production toolkit (recipe L286-307) holds the driver's pins.
  - The writer `b9247b1a` is loaded by exact bytes. Its `LOCAL['prep']` gives prep `8681da84` (MW L43-45), and its `PINS['controller']` gives the controller `c5bdd055` (MW L46-49).
  - Checkpoint module `069b3935` (driver AUX L253), binding `aee7af12`, driver `577f8c94`.
  - The roster module comes through the controller's and the binding's own loaders (controller L99-125, BB L67-75). The H2 component is the binding's (BB L578-593).

### RECIPE_ROUTE_A (recipe L327-513): the manifest writer's rebuild at iteration m

How a target maps to m (reader `s5_targets` L342-351, first occurrence):
- `(n, current)`: m = n.
- `(n, next)` with n < a: m = n+1, only if `payload[n].next_state_digest == payload[n+1].state_digest`.
- `(a, next)`, or a broken chain: refused, `ROUTE_A_MONITOR_NEXT_GAS_UNRECORDED`.

| input | how it is built (named code) | where the call records it | basis |
|---|---|---|---|
| writer | `script_sha256` must be `b9247b1a` | manifest ctx record (driver L8697-8700, L1822-1857) | FORMAL |
| module patches | stage-shim `setattr` after exec, with the decoding at driver L731-739 / L698-707; only the prep may be a target; no mask, no stage globals | the manifest `request.json` (sha = record `request_sha256`, driver L1842-1843); built at L1020-1028 | FORMAL |
| seed | `numerical_inputs`; every seed pin re-hashed (MW L198-203) | manifest argv `--seed/-sha256` = `identity.seed` (L8450, L8464) | FORMAL |
| attempt / checkpoint / sidecar | MW `attempt_tail_record` (MW L98-121); checkpoint `IDENTITY` (MW L213-216) | manifest argv, cross-checked against the route_a stage argv (`--outdir`, `--checkpoint-directory`, `--uv-tail-sidecar-directory`; L8607-8628) and `identity.route_a.custody` (L8682) | FORMAL |
| static parts | `prep.prepare_inputs(**ni)`, then `from_prepared(galaxy='NGC3198', …, sidecar_directory=None)`; must equal `SIDECAR_IDENTITY` (MW L225-231; controller L219-284) | sidecar identity (controller L335, L363) | FORMAL |
| r | `identity.relaxation` (MW L155) | `SIDECAR_IDENTITY.json` | FORMAL |
| elements 0..m-1 | MW `sidecar_elements` (MW L124-148); each file must be in the sidecar finish list | `elements_NNNN.npz` and its payload digests (controller L495-499, L518-519) | FORMAL |
| gas_m | checkpoint `_get(START.gas_fourier_J)`; START/COMPLETED bound to the identity and iteration, `converged` only at a (MW L217-221; driver L7031-7037) | `checkpoint/iteration_m/START.json` | FORMAL |
| i1t | `ctl._i1t(m, gas_m)`; must equal the recorded `payload[m].i1t` (and, for next, `payload[n].next_i1t`) | sidecar payloads (controller L497-498) | FORMAL |
| roster | `rs.roster_route_a(stars, init_rings, elements[:m], r, s_edges, kpc_m, M_s, c_m_s)` | controller L396-397 | FORMAL |
| build | `ctl.config, ctl.kept, ctl.gamma_eff, ctl.c_m_s, ctl.eval_radii, i1t, 'route_a'` | controller L399-401 (kept L190, gamma/c L191, radii L196-197) | FORMAL |

### RECIPE_ROUTE_B_<kind> (recipe L516-791)

Common to every kind:
- The stage is found by its ctx record (name = target stage), with its finish bound by `uv_tail.stage_records` (driver L1155-1172).
- The finish must hold `schema`, `stage_kind` = the binding kind (driver L352-354), `binding_sha256 = aee7af12` (BB L352), the target state digest and the target roster digest.
- **config**: `lib.normalize_config` of argv `--uv-tail-config` must equal the recorded `config`, `config_sha256` and `config_file_sha256` (BB L692-699, L356-357). FORMAL.
- **kept**: the binding's own `_grid_K` and `_truncation`, then `kept_region(kind, tr, K_m)`, must equal the recorded `kept` (BB L235-272). The stage-wave containment check stays the stage's own. FORMAL.
- **i1t**: the recorded `uv_tail.i1t`, which is the dict handed to build (BB L528-531 / L558, L359). FORMAL.
- **stage_kind**: the binding kind (BB L373). FORMAL.
- **gamma_eff, c_m_s**: DECLARED. The binding takes them from the successor's `phys` (BB L372). The recipe takes the accepted route-A state record's values (MW L177-181), the bits A167 C4b requires of every NGC state.
- **Profile pin**: DECLARED. The successor's argument, taken as the route-A prep profile in `SIDECAR_IDENTITY` provenance (controller L235). It is FORMAL when an outer gas cut records it (BB L435), and the two must then agree.
- **Stars**: `rs.stars_registered(profile, 'NGC3198', units, (H2,))` (BB L325-334).

| kind | roster (named code) | own inputs | eval radii |
|---|---|---|---|
| offset | `_DifferenceRoster(body_r, ra_roster, synthetic or i1t verdict != PASS)` (BB L549-552, L559). The manifest is validated by the binding's `_manifest`, and `ra_roster` comes from its `_manifest_gas_roster` (BB L379-427). | argv `--route-a-tail-manifest` = `result.uv_tail.manifest` (L8715-8716); body = `body_arrays.npz` of `--body-directory`, bound by `--body-finish-sha256` (L8778, L3307), **DECLARED** | `unique(body radial_nodes_m)` (BB L560), FORMAL; the body file is DECLARED |
| fs_columns, fs_rotation | `roster_body({pos, J = -c²·rho0·vol}, stars, …)` (BB L489-492) | base = the offset's `updated_base_arrays.npz` (L3310; BB L21), **DECLARED**; `source.new_body` must equal the offset `source_offset.npz` pin (BB L493, L501) | **DECLARED**: `unique(base radial_nodes_m)` (L629-631) |
| rfs_columns, le_columns, le_rotation | `roster_rotation(arr, stars, …)` (BB L514) | `arr` = {rho0, volume_weights_m3, radial_nodes_m, z} from `<--uv-tail-source-rotation-directory>/finish.json arrays_path`, sha-checked, with directory and finish sha = `uv_tail.source.source_rotation` (BB L503-513, L525-526), FORMAL | **DECLARED**: as for fs |
| reference, body | not rebuilt: the accepted manifest state (BB L457-470); refused `ROUTE_B_KIND_NOT_REBUILT` | | |

## The monitor-next state and updated_a (A177 item; FORMAL from bytes)

**Built.** The controller builds N at L483-484: `g_next = (1-r)·gas_a + r·updated_a`, then `_build(a+1, _i1t(a+1, g_next))`.

**Recorded by named code:**
- **updated_a, as an element roster:** `<sidecar>/elements_{a:04d}.npz` (L475-481, L518-519), with digests in `payload.elements` (L499). N's roster is therefore fully recorded.
- **N's I1-T record:** `payload[a].next_i1t` (L497-498).
- **N's digest:** `payload[a].next_state_digest` (L496).

**Not recorded by any named code:**
- **The gas array g_next = gas_{a+1}.** The sidecar write list is L363, L518-520 and L560-561; g_next lives only in `_pending` (L522), and even its digest is not written.
- **No checkpoint START holds it.** The iteration folders stop at a (driver L7024-7038).
- **No Fourier form of updated_a** is written by the controller or the writer.
- **Not read:** the solver `COMPLETED.json` payload and the attempt `result.json` fields beyond `result.uv_tail`. The solver `8ef3079b` / `7667025b` (driver L329-330) and checkpoint module `069b3935` are not named paths here, and the driver reads only `{iteration, identity_sha256, iteration_start_sha256, converged}` from COMPLETED (L7033).

**So N is refused, never approximated.** The writer path recomputes I1-T from the gas array (MW L217-221, L232), and the gas array is missing. The same code refuses an `(n, next)` state, n < a, whose digest is not iteration n+1's begun state (its g_next is equally unrecorded).

## Handoff c2v004 (the delta from c2v003a, and only it)

c2v004 was generated from the c2v003a bytes by listed exact replacements (dev tool kept in scratch). The changes:
- `ROSTER_RECIPES` = `{ngc_roster_recipes_c2v001.py, 6c9e8508…}`, recorded in `rec['pins']['roster_recipes']`.
- `prepare_acceptance_inputs`: `recipe_ref` and `approved_recipe_sha256` default to `ROSTER_RECIPES` and `[its sha]`.
- `_accept`:
  - the approvals carry `recipes`;
  - REGISTERED requires `{reader, s5, recipes}` = the module constants (`READER_S5_OR_RECIPES_NOT_THE_PINNED_MODULES`);
  - each verified export's admission must name the approved recipe, else `REBUILD_EXPORT_REFUSED … S5_ADMISSION_RECIPE_IS_NOT_THE_APPROVED_RECIPE_SOURCE`, and that state reads UNAVAILABLE.
- The record and summary schemas move to `*_C2V004`, the loader names to `c2v004`, and the CLI strings to c2v004.

Everything else is c2v003a. **No adapter successor was built** (builder choice 2).

## Tests

**Record runs** under `python3 -I -B` 3.12.14 (no ART patch):

| run | must_pass | must_fail | blocked | seconds |
|---|---|---|---|---|
| record_run_1 | 38/38 | 54/54 | P16, P18, P29, F38 | 10.1 |
| record_run_2 | 38/38 | 54/54 | P16, P18, P29, F38 | 9.8 |

**Run-to-run agreement.** Ids and ok flags are identical across the 96 entries. Details are identical once the run directory and hex digests are normalized, except P27, which keys its detail by 12-hex digest prefixes that depend on the run directory (as in c2v003).

**Ported: every c2v003a test (P01-P35, F01-F42).**
- The c2v003a suite file (`e452cec2`) is loaded by exact sha and run against the c2v004 handoff, with the same fixture and intent. The one adaptation: the handoff approvals carry the synthetic recipe.
- **BLOCKED_BY_HARD_RULE (4):** P16 and P18 read V006 (the REGISTERED root gate), and P29 and F38 read the NGC3198 query manifest. An audit hook refuses every such open, and a test with a refused open is listed, not counted.
- P16, P29 and F38 exercise only unchanged pinned code, and their c2v003a record results stand.
- P18 is the c2v004 public entry, so its c2v004 result is UNTESTED (root item R5).

**New, MUST_PASS (6):**

| id | what |
|---|---|
| P36 | c2v004 pins `ROSTER_RECIPES` (sha from bytes): the prepare default, the REGISTERED approvals and the record pin; the other pins are c2v003a's |
| R01 | route A: (0,current) and (0,next)→m=1 are ADMITTED via the real recipe; (2,next) is refused `…MONITOR_NEXT_GAS_UNRECORDED` |
| R02 | route B: offset, fs_columns_00, fs_rotation, rfs_columns_00, le1_columns_00 and le1_rotation are each ADMITTED; the recipe roster digest equals the recorded one |
| R03 | broken chain: iteration 1's begun state is rebuilt from START(1) and ADMITTED |
| R04 | custody: every open during S5 + recipe is the call's own output, the S5 out dir, a pinned module, a seed pin or a config certificate; none is refused |
| R05 | production toolkit pins checked against the writer and driver bytes; on a synthetic call it refuses `RECIPE_CALL_NOT_BOUND` before loading any module |

**New, MUST_FAIL (13):**

| id | what | code |
|---|---|---|
| F43 | note 3(a): start.json `driver_sha256` / `call_spec_sha256` not this call's | fresh_call False, `EXECUTION_FACTS_REFUSE` |
| F44 | note 3(b): the finish names the point certificate, but the exported TailState ran with another one | `TAIL_STATE_DID_NOT_RUN_WITH_THE_POINT_CERTIFICATE` (past `STAGE_EPS_PIN_…`, the control) |
| F45 | an export admitted under another recipe; REGISTERED non-constant recipes | `S5_ADMISSION_RECIPE_IS_NOT_THE_APPROVED_RECIPE_SOURCE`, `READER_S5_OR_RECIPES_NOT_THE_PINNED_MODULES` |
| R11 | wrong iteration; iteration out of range | `ROUTE_A_TARGET_NOT_THE_ITERATE_STATE`, `…_OUT_OF_RANGE` |
| R12 | missing sidecar element | `ROUTE_A_SIDECAR_ELEMENT_MISSING` (the reader also refuses) |
| R13 | swapped kind: target kind or state, ctx kind, the recipe of another kind; inherited kinds | `ROUTE_B_STAGE_KIND_MISMATCH`, `ROUTE_B_TARGET_NOT_THE_STAGE_STATE`, `ROUTE_B_KIND_NOT_REBUILT` |
| R14 | edited checkpoint gas: bytes, re-pinned START, consistent forgery, in-tolerance forgery | `…GAS_UNREADABLE`, `…CHECKPOINT_RECORDS_DISAGREE`, `ROUTE_A_I1T_REFUSED`, `ROUTE_A_I1T_NOT_THE_RECORDED_I1T` |
| R15 | missing updated_a: accepted next, broken-chain next, and the handoff prepare chain | `ROUTE_A_MONITOR_NEXT_GAS_UNRECORDED`; prepare raises `ROUTE_A_ITERATE_SOURCE_UNESTABLISHED` (2 admitted, N not) |
| R16 | prep patch dropped from the manifest request | `ROUTE_A_CONTROLLER_IDENTITY_DIFFERS` (init_rings_digest) |
| R17 | DECLARED base arrays not the stage's | `S5_ROSTER_NOT_THE_RECORDED_ROSTER` (before any build) |
| R18 | DECLARED gamma not the stage's (one ulp) | `S5_REBUILD_DIGEST_MISMATCH` (roster equal) |
| R19 / R20 | stage record not written by the pinned binding; manifest stage not run by the recipe-bound writer | `ROUTE_B_BINDING_NOT_THE_PINNED_BINDING`, `ROUTE_A_MANIFEST_WRITER_NOT_RECIPE_BOUND` |

**The recipe fixture.** States come from the named code itself:
- **Route A:** the sidecar is written by the real controller `c5bdd055` (open, begin_iteration, complete_iteration, result_record). The manifest comes from the real writer functions (`rebuild_state`, `write_outputs`).
- **Route B:** every state is built by the real binding `aee7af12` (`bind`, `bind_offset`, `record`). The checkpoint uses the driver's START / COMPLETED form.
- **Test-only stand-ins**, written per run and loaded by exact sha:
  - the roster module (for `4366e3d6`);
  - the prep (for `8681da84`);
  - the checkpoint module (for `069b3935`; `_read` and `_get` only);
  - the H2 component;
  - the toolkit;
  - an S5 wrapper that calls the real recipe's `recipe_for_state` with that toolkit.
- **Where the fixture plays the stage successor, it follows the DECLARED reading.** So R02 shows that the recipe reproduces the binding's own construction, not what the real successors pass (root item R2).

**Dev mutation spot-check** (scratch, not a deliverable). 10 one-line mutants of the recipe, each killed by its intended test:
- next-gas refusal off: R15;
- next mapped to n: R01;
- elements one short: R01;
- prep patches dropped: R01;
- fs J without c²: R02;
- binding-sha check off: R19;
- kind check off: R13;
- I1-T record check off: R14;
- writer check off: R20;
- offset radii changed: R02.

## README wording fixes (verifier notes 1-2)

- **Note 1, the no-recipe outcome.** The c2v003 README said every non-accepted state "reads `NGC_STATE_INPUT_UNAVAILABLE`". In fact:
  1. Without an admitted route-A source, `prepare_acceptance_inputs` raises at the reader's `write_iterate_list`: `ROUTE_A_ITERATE_SOURCE_UNESTABLISHED`.
  2. No iterate list exists, the inventory stays incomplete (`ROUTE_A_ITERATE_LIST_UNAVAILABLE`), and `accept_call_ngc` reads **INCOMPLETE**.
  3. With these recipes the same holds for every real call, because N is refused (R15, TESTED).
- **Note 2, the S10 reviewer.** S10 is **Claude3**'s review (A177, A176). It carries schema `UNT_NGC_LO_ROW_POLICY_REVIEW_C2V002`, verdict APPROVED and `row_contract_sha256` `80cbf2f5…`. It is not Codex1's.
- **Stale wording in pinned files.** The c2v003 S5 docstring ("OPEN INTERFACE: no roster recipe…") and the row-contract builder docstring ("S10 … Codex1's") are unchanged bytes of pinned files. This README supersedes their wording.

## Builder choices (each is root's to overrule)

1. **N refuses, with no fallback.** No variant rebuilds N from the recorded roster and `next_i1t` without recomputing I1-T (R1 below).
2. **No adapter c2v004.** Nothing in the adapter changes: it pins no recipe, and the recipe pin lives in the handoff. A copy would add a sha to review and change nothing. The handoff c2v004 pins the adopted c2v003a adapter.
3. **c2v004 checks recipe provenance at accept.** Each export's admission must name `ROSTER_RECIPES`. Digest equality stays the proof.
4. **Route B uses the binding's own code where it can run without its stage inputs:** `_grid_K` with a zero wave, `_truncation`, `_manifest`, `_manifest_gas_roster` and `_DifferenceRoster`. Stars are built as at BB L334, without the binding's `_stars` (which opens the H2 source) or its I1-T replica rings.
5. **The DECLARED readings are single and cited, never searched.** One reading per input (gamma and c from the manifest state; radii from the base arrays; profile from the sidecar identity; body and base files from the producer `outputs` map, else the named file).
6. **The route-A recipe runs the prep once per route-A state**, as the writer does once per call. There is no cache (U4).

## Root items

- **R1. N (the monitor-next state) is unrecoverable from the named records, so no real call can be ACCEPTED while builder choice 1 enumerates N.**
  - Recorded: N's roster (via elements_a), its I1-T record and its digest. Not recorded: gas_{a+1}.
  - Deciding read: the solver COMPLETED payload (`8ef3079b` / `7667025b`) and the checkpoint module `069b3935`, for whether `updated_a` (Fourier form) is stored. If it is, `g_next` follows exactly from the controller L483 expression.
  - Otherwise root rules whether N may be admitted from the recorded roster and `next_i1t` without recomputing I1-T. That is exact and digest-proved, but it trusts the run's I1-T record.
- **R2. Route-B DECLARED inputs are UNTESTED on a real call.** They are gamma/c, the own-roster eval radii, the profile pin, and the body and base file mapping. They are argument values of the V011_B_STAGES successors (driver L4993), which are not named paths here. Deciding test: a read of those successors, or the first call's S5 admissions (fail-closed either way).
- **R3. STAGE0_GRID_OUTER calls** (writer `443d9fdc`, prep `d5788892`; driver L6145) are refused `ROUTE_A_MANIFEST_WRITER_NOT_RECIPE_BOUND`. That writer is not a named path, so its pins were not read.
- **R4. S5 host custody (observation).** The TailState record carries `provider_custody`: the platform string and the libm path / sha (library L792, provider L62-69). An S5 rebuild on another host or OS build would read `S5_REBUILD_DIGEST_MISMATCH`. Deciding test: the first call's S5 on the run host.
- **R5. Four ported tests are BLOCKED here** (P16, P18, P29, F38: they read V006 or the query manifest). P18 is the c2v004 public entry; deciding test: P18 run by root. Note that with a non-pinned recipe its exports are now dropped at accept.

## UNTESTED (each with its deciding test)

- **The production toolkit beyond its first refusal:** the real prep pass, `load_libraries`, the binding's roster loader and its H2 component. Deciding test: the first real call.
- **U4, the post-run cost.** One prep pass plus one build per route-A state, and one build per route-B state. Deciding test: the first call's S5 timings.
- **R1, R2 and R5** as above.

## Conduct and deviations

**Read** (by named path, sha from bytes):
- V006 A153 / A155 / A162 / A167 / A177, by awk only;
- the c2v003 README and code in this folder;
- the driver `577f8c94` (cited lines);
- the controller `c5bdd055`;
- the writer `b9247b1a`;
- the binding `aee7af12`;
- the library `2026f2b6` and provider `d6c55b55`.

**Not opened:**
- the roster module `4366e3d6`;
- the checkpoint module `069b3935`;
- the solvers;
- the prep `8681da84`;
- the V011_B_STAGES successors;
- the STAGE0 writer;
- the H2 reduction or source;
- any NGC3198 target, velocity, sigma, slots or query-manifest file;
- any run tree or `~/.codex`.

The test suite's audit hook refuses all of these. The two refused opens recorded in both runs are V006 and the query manifest, by the blocked ported tests.

**Deviations:**
1. **The roster module's interface was inferred from its call sites.** Those are in the controller and binding. The synthetic stand-in matches those signatures only.
2. **No adapter successor** (choice 2).
3. **Test-fixture monkeypatching:**
   - the fixture's copy of the binding has `ngc_h2_component` replaced;
   - for R12 only, the fixture's controller instance redirects `elements_0000.npz` out of the sidecar.
4. **Scratch dev.** All dev ran in `scratchpad/ngc_recipes_v1/`. The final files were written here by exclusive create, and no earlier file was edited.
