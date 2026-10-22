# CHECK_V001: independent check of `ngc_route_impl_c2/binding/` (driver c2v005, gal_c2v003 stages, schema V003)

Claude2 lane, independent checker (not the author). Everything I wrote is in `binding/check_v001/` plus this file; everything else was read-only.

- No project launch. Driver runs were dry runs or run-mode stubs; my own audit-hook guard (`check_v001/xguard.py`) refused every process creation, every write outside `check_v001/`, every velocity-like basename and every open under `CLAUDE2/runs`. Across 22 guarded runs the only denial was the intended `subprocess.Popen` in the deciding-test stub.
- No NGC3198 target velocity was opened. The NGC manifest was read for `Rad_text` only.
- numpy only, single thread, runtime `codex-primary-runtime python3 -I -B`, every hash from bytes.
- Binding authority: `ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V001.md` (sha `06cae881…a905`, re-hashed), read in full. Cited sources: `ngc_options/NGC_CONSTRUCTION_OPTIONS_V001.md` and its CHECK, `stages2/CHECK_V001.md`, `v004_fix/CHECK_V001.md`, `reducer/CHECK_V001.md`, `route_a/CHECK_V001.md`.

## Verdict: PASS_WITH_DEFECTS (1 MAJOR, 1 MEDIUM, 5 LOW, 1 INFO)

- **DDO154 / deciding test: clean.** The v005 binding is a pure binding change for DDO154. The plans are token-identical to c2v004 apart from declared classes, every DDO value equals its old literal, and the run-mode stub reaches the first stage request with no blocker and no refusal. `LAUNCH_DECIDING_TEST_C2V005.json` may go to approval as written.
- **NGC3198 route B: not runnable.** It is correctly refused today: 5 refusals go beyond the pending inputs, because no N-row decides those fields and no row-handling code exists. Separately, **D1 (MAJOR)**: the route-B call path is bound to the provisional-L4 point, so it cannot consume the A2 factor-3 NGC route-A run that the decisions order first. The dry run cannot show this while route A is pending. Fix D1 before route-A outputs are wired in.

## 1. Re-derived claims (own scripts; all results in `check_v001/*.json`)

| Claim | Method (own) | Result | Status |
|---|---|---|---|
| Author manifest `HASHES_BINDING_C2V005.txt` | sha256 of every entry; walk for unlisted files | 1342/1342 match; 0 unlisted; 0 missing | TESTED-POSITIVE |
| Source pins of all generators: 11 stage sources, schema, join successor, decisions, both V002 schemas, profile, DDO seed, kernel v001, main source, DDO template | sha256 of bytes | all match | TESTED-POSITIVE |
| **Byte equality of generated copies** (stages, schema V003, both galaxy configs, NGC solver template) | author builders run in memory, output compared with published bytes (`chk_custody_regen.py`) | all 11 stages, schema `6adbfce5`, DDO `fd47e02b` / NGC `dbf546b5` configs and template `ba5e87eb` are byte-equal | TESTED-POSITIVE |
| Shared blocks | extracted from all 11 stages | ADMISSION: 1 text in 11 stages. READER: 1 text in 10 stages, and its function body equals the v004_fix c2v002 `route_a_final_iteration` verbatim (stages2 CHECK D2 fixed). TRUNCATION: 1 text in 5 stages | TESTED-POSITIVE |
| **AST equivalence of stages** (`chk_ast.py`: flattened statements, difflib on `ast.dump`, DDO rewrite) | every differing statement listed (`AST_V001.json`) | Differences are confined to: admission (V003); the strict reader; N2 truncation (`radial_truncation`, `edges[:J]`, `edges[J]`); the join successor plus `n_columns=NCOL`; and, in the two new successors (fs rotation v001, fs feedback v002), DDO literals mapped to config. Those literals are 72, 16, 32, `iteration_0004`, `OFFSET_SHA`, `SOURCE`, and the producer sha moved into `producer_pins`. The DDO rewrite equals the base at every literal site. All 11 docstrings are byte-equal. No equation, tolerance or base guard was removed. One base guard was replaced by an equivalent: rotation v005 / offset `sqrt(edges[-1])==outer` became `radial_truncation`, which at DDO hits only the last edge. No undefined name; config-derived names are main-local. | TESTED-POSITIVE |
| **DDO invariance of N2** | `radial_truncation` on DDO profile and saved source with the DDO literal 14.102260356114186 | hits = [18] = last edge; 72/72 roster nodes below the edge, so the reference filter is a no-op; mesh coverage = 1.0 | TESTED-POSITIVE |
| **simulate equivalence v004 → v005** (`chk_plans.py`, written independently of `compare_plans_v004_v005.py`; on my own dry runs of both drivers) | per stage: script base identity, argv tokens, generated-file bytes, dropped globals vs per-stage config values, every DDO literal vs schema, producer whitelist, module patches, mask | ADMIT_PREFIX (19 stages), PINNED_FULL (22), RULE_FULL (20) and ADMIT_ROUTE_A (21): **0 failures**. Classes: successor-of-same-base, galaxy-config tail, dry-dir prefix, generated file equal, reference module 81a04b12→1b00add9, globals→config with equal values (SEED_SHA, IDENTITY, REFERENCE, DATA_PINS, OFFSET_SHA). v005 vs the saved-chain launches: stages with identical inputs = c2v004's count in every spec (17, 20, 12, 19); bracket rule bitwise in the pinned specs; `binding_blockers` = []; 0 pin problems; 0 scipy. | TESTED-POSITIVE |
| Run-mode stub, deciding spec | guarded `run` | reaches `stages/01_reference` request with no blocker or refusal; Popen refused | TESTED-POSITIVE |
| Deciding specs and LAUNCH pins | sha256 plus spec field diffs (`chk_specs.py`) | driver, call spec, alternative and source pins all verify. ADMIT_ROUTE_A differs from its source by the label plus the removed `admit.reference` and `admit.body`. ADMIT_PREFIX differs by the label only. Elapsed sum 5247.85 s recomputes. Outdir under `CLAUDE2/runs` not inspected (rule). | TESTED-POSITIVE |
| **Schema V003 = N5** (`chk_schema_values.py`) | field-by-field vs both V002 files | V003 = v004_fix V002 + `custody.fs_feedback_worker_sha256`, whose entry equals stages2's. 0 DDO entries changed, 0 kinds changed, V002 order kept. NGC changes only on N-rows: N1 gauss 4; N2 edge; N1+N2 n_columns 100; N3 slot; N4 ×8. | TESTED-POSITIVE |
| N2 value and S6 | exact profile arithmetic; own GL roster with kernel v001 (skip-zero) | first zero annulus 25. Edge 66.90428799311597 (bitwise, unique hit). Dropped mass 3.8987e-5. Truncated GL4: 100 nodes, coverage Σwr/(hi²/2) = 1.0000000000000002, so mesh v002 accepts (the full domain gives 0.6632 and is refused). Nodes 0.70517–66.7219 kpc; Q01 and Q02 outside (N1 INVALID); Q43 = 44.08 inside. | TESTED-POSITIVE |
| N4 values | recomputed | 1/1.36 and 64/121 bitwise-equal to the DDO literals. Bracket [h0/2, 1.05·h0] = [1.5125e8, 3.17625e8]. Mesh 16/8/32. HI distance 13.8 = main source 13800000 pc. Template mapped from the **actual NGC route-A seed** (`hi_search_limit_kpc` 95 etc.) equals the template bitwise, carried DDO values equal, template bracket = fs bracket. | TESTED-POSITIVE |
| N3 reducer output vs N2 guards | body guard and rotation `radial_truncation` on reducer `source.json` `746980f2` | admitted as the bitwise profile prefix (26 edges / 25 means); rotation J = 25. DDO saved source: full form, J = 18. | TESTED-POSITIVE |
| Admission c2v003 (`chk_admission.py`, 18 probes on the stage's own exec'd text) | synthetic configs | all as expected: the slot is admitted only as PER_CALL with no sentinel; root-decision value or status changes are refused; DDO with non-literal statuses is refused; an unknown galaxy is refused; NONE, missing or extra fields are refused; the **GL10 alternative is refused** (see D2) | TESTED-POSITIVE |
| NGC route-B dry run | my guarded dry run vs author's | refusal classes identical to the author's; beyond pending inputs: N1 invalid-row handling, `brackets.rule_factors`, `driver.fixed_args`, `observation.binding`, `observation.tracer_rule_and_observation_rule`; run-mode stub BLOCKED before any stage | TESTED-POSITIVE |
| Reducer feasibility / DDO bitwise of reducer | not re-derived here: reducer/CHECK_V001 did both (byte-identical CLI reruns; exact feasibility {22},{23}) | its R1 (22-versus-23 rule) still needs a register line before the slot is filled | covered by reducer check |
| Author synthetic tests (31/31) | not re-run (they write under `binding/tests/runs`, outside my area) | replaced by my own probes above | — |

## 2. Defects

| ID | Sev | Where | Defect | Evidence | Fix |
|---|---|---|---|---|---|
| **D1** | **MAJOR** | `galaxy_m0_forward_c2v005.py:231` (`NGC3198.default_coefficients` = fe5a2f06), `:2542-2545`, `:1476`, `:886-890`; `specs/CALL_NGC3198_ROUTE_B_PENDING_C2V005.json:6-9,13-15` | NGC route B is bound to the **provisional-L4 point**, not to the A2 factor-3 anchor of the NGC route-A lane that the decisions run first ("Order of work" 1). The route-A seed uses the A2 pooled grid `2e3a36d8` and the scaled physical point (s = 0.3332538300367979). The route-B normalizer refuses every grid except fe5a2f06; its message calls fe5a2f06 "the NGC route-A grid", which is false. The pending spec copies the DDO saved-chain physical block (Eref 1.4643e58, γ 2.9410e41, s 1). | Probe with the A2 grid: **Refusal** at normalization (`logs/dry_ngc_a2grid.json`). The default grid passes normalization, but `route_a_custody` compares the grid digest with the checkpoint: the two `source_hessian_grid` arrays differ (max \|Δ\| 6.26, `NGC_GRID_V001.json`), so it would **Block**. Pending-spec physical × s ≠ route-A seed (Eref, γ), so `:1476` would **Refuse**; the A2F3 unscaled × s matches bitwise. The dry run cannot show any of this while route A is PENDING. | Accept the call-spec grid when it equals the NGC route-A seed's `coefficients` (the existing digest check at `:890` stays the guard). Set the NGC spec physical to `anchor.physical_unscaled` with its s. Correct the message. Re-run the NGC pending dry run. |
| D2 | MEDIUM | `schema/make_schema_v003.py:155`; schema `radial.n_columns.ngc3198.condition` = {gauss 4} | The N1 **declared GL10 alternative** ("evaluated before freeze… at the reference member") has no binding path. Admission refuses gauss 10 / n_columns 250. Together with route_a CHECK D2 (no GL10 route-A run carried), the alternative has no executable route at all. | `ADMISSION_V001.json` `ngc_gl10_alternative` REFUSE. Own roster: truncated GL10 = 250 nodes, coverage 0.9999999999999999 (mesh accepts), innermost 0.3057 kpc, so all 43 queries are inside. | Add an alternative-labelled NGC entry (gauss 10, n_columns 250 conditional on 10), or carry it as a named open item with its route-A run. |
| D3 | LOW | `stages/ddo_saved_root_body_array_root_v002_gal_c2v003.py:208`; driver slot handling | With J < last edge, the body guard also admits the **full** untruncated source record, and nothing pins the reviewed N3 output: any self-consistent `source.json` fills the slot. N2 and N3 together specify the truncated-domain member (`746980f2`). | Code read; the guard has two admitted forms. | When J < len−1, require the prefix form. Pin the reviewed N3 output sha in the call spec once R1 is recorded. |
| D4 | LOW | `body…_gal_c2v003.py:237` | The added N2 domain-edge guard runs **after** the per-radius evaluation loop. It fails closed, but only after all radius files are written. | Code read | Move it before the loop. |
| D5 | LOW (inherited, extended) | `_producer_refusal` (e.g. `rotation_v001…_gal_c2v003.py:142`), feedback v002, column mean | A stage-level `producer_pins` entry is accepted if it is self-consistent; only the driver whitelists it to {successor, base}. This is v004_fix CHECK N1, now also in the two new successors. | Code read; driver `producer_pin:1326` | Whitelist inside each stage, or record that the driver enforces it. |
| D6 | LOW | `galaxy_m0_forward_c2v005.py:2537` | The NGC route-B spec may override `entropy_K_factor` with any positive value. It is neither labelled as the N4 declared original-K alternative nor restricted. The le_first factors fit only 64/121 (options §2.4). | Code read | Admit only 64/121 or 1.0, and label 1.0 as the N4 alternative. |
| D7 | LOW (inherited) | `compare_npz` (unchanged) | The verdict is named BITWISE but uses value equality (v004_fix N3). This is disclosed in the LAUNCH `pass_condition`. | AST: unchanged | As before. |
| D8 | INFO | driver docstring; `remaining_refusals_v005` | "dry-run lists every remaining refusal" holds only for refusals knowable without route-A bytes. Grid digest, physical-vs-seed and roster-digest checks appear only once `route_a_inputs` exist (D1 is one). | §1 | Reword. Re-run the NGC dry run with real route-A outputs before any NGC launch. |

## 3. NGC route-B open items: refused correctly, not defects

Each item needs a root line or reviewed code; the binding invented none of them.
- `brackets.rule_factors` and `driver.fixed_args`: the options memo §2.4 recommends the DDO values as a counted numerics transfer, but no N-row adopts them.
- `observation.binding` and `observation.tracer_rule_and_observation_rule`: options §2.3 marks the wording ROOT DECISION NEEDED. N4 binds only the HI/(HI+He) ratio inside them.
- N1 INVALID rows: a column-mean successor that emits Q01 and Q02 as INVALID is required. The reviewed adapter refuses the whole call.
- N3 slot: fill it only with the reviewed reducer output after reducer R1 is recorded.

## 4. Status words

| Item | Status |
|---|---|
| DDO154 binding equivalence (static: AST, plans, configs, stub) | TESTED-POSITIVE |
| DDO154 run-mode bitwise equivalence | **UNTESTED**. Deciding test: `specs/LAUNCH_DECIDING_TEST_C2V005.json` (needs launch approval) |
| N2 truncation and S6 coverage | TESTED-POSITIVE |
| N4 / N5 values | TESTED-POSITIVE |
| NGC route B consumes the A2F3 route-A run | **TESTED-NEGATIVE** (D1) |
| NGC GL10 alternative path | TESTED-NEGATIVE (D2) |

## 5. Checker files (sha256 from bytes)

`check_v001/HASHES_CHECK_V001.txt` (254 entries; sha `8bec244964a8a3657daa48d7a662be441efaddbc2789cad499f3eada3c542f7e`) covers every checker file, including the dry-run reports, logs and probes.

| File | sha256 |
|---|---|
| xguard.py | 2abe6408e5f6888f1d8ef4d32cf5c09f3c815310489a489c33db64c4d191fba4 |
| chk_custody_regen.py | da03034c67f73ae41435abf2df6b671e0c9492e7ff348cd27839e5ec6dc02fde |
| chk_schema_values.py | 5967bb746c569407e632178dba61e677660d7d1ac07fc07297ec7155e4185d5c |
| chk_ast.py | 572def0c478607228649989fd6e7a152dfa8b3a88546610c1730481a26fbed2c |
| chk_plans.py | 302b55f8cb42c995dc701b0dfb5906e0c882fbfb3f9ee06c674b26bcdf27b041 |
| chk_admission.py | 77741021427de1179deddc21705e85c1ff7b44d589ef52c1f1a37ae2d07021da |
| chk_specs.py | 5ee789a4554bfd1256e5dbf53d87db333a7a6a4a6f1564cb47e3694f44626e0d |
| chk_ngc_grid.py | 461f1f3042fa1d3d93b42fe210361a11da3a57c081cdfdf91ef63a806cca10e8 |
| CUSTODY_REGEN_V001.json | 5474ffa09ac159313e0854d859c20c10af2b9ec9d833180165fbb1c8d7f9f461 |
| SCHEMA_VALUES_V001.json | 54102723d96925ddd2d8f8a51cdb1d95c47fe307af7adbe9bd2db6623b9a3a99 |
| AST_V001.json | c93c0b94d3f92ee95181bc430e4e0446aa825bae43a1abff889a48ad08daf6b9 |
| PLANS_V001.json | 24c803b7e4a5f07ef07574a195dcc0dd43471a7428ce74dd1145c0d88020bed5 |
| ADMISSION_V001.json | c8ce10a44f3dbe03bc3a0492e251ced9a062565634acd3a305e17fb27f368b88 |
| SPECS_V001.json | bdc036a3c14e009a542928ab5de41651fb7c22f6b36c037dcdbe48fb89029cc5 |
| NGC_GRID_V001.json | b8a6ea03cd4e52020fd558aa7296e6551668d998f730bd9027af1b4bdcb716ba |
