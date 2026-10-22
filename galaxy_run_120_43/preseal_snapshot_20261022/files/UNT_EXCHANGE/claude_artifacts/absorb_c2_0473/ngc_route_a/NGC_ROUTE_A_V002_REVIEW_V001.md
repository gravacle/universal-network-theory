# NGC_ROUTE_A_V002_REVIEW_V001: distinct review of Claude4's 0471 route-A port and the NGC seed numerics

**Context.** Claude2 lane, absorb 0473. This is the distinct review Claude4 could not finish (dispatch `FROM_CODEX/0471_…`).

**What was written.** Everything is under `claude_artifacts/absorb_c2_0473/ngc_route_a/` and nowhere else.

**What was not done:**
- No NGC route-A calculation.
- No project launch.
- No NGC3198 target velocities opened.
- Nothing deleted.

**How it was run.** Runtime `…/codex-primary-runtime/dependencies/python/bin/python3 -I -B`, numpy only, single thread. Every hash is computed from bytes.

**Claude4's inputs.** `ngc_route_a_0471/` contains only `N1_port/` and `N2_numerics/`. No N3 fixtures and no N4 check exist, so this review supplies both.

## 1. Verdict on the N1 files: PASS (TESTED-POSITIVE, byte level)

| File | sha256 |
|---|---|
| `ngc_route_a_0471/N1_port/ngc_composite_full_coupled_binding_v002.py` | `cc5db369a8e4e50aa3a1fa32ab0713b0c0c3a7be5ead2935554c4b02a438f130` |
| `ngc_route_a_0471/N1_port/ngc43_composite_coupled_root_worker_v002.py` | `42bdd23e3db2b3b00dd9d3b89126ccf92a1e2c9c02bdc6080c4c65c8c40c41bf` |

The sources were verified from bytes:

| Source | sha256 |
|---|---|
| NGC binding v001 | `9e9caf83…1248` |
| NGC worker v001 | `1b95a4ff…0ca4` |
| DDO binding v001 | `23d2b57d…5034` |
| DDO binding v002 | `d81b24b7…b6d5` |
| DDO worker v001 | `0117b2eb…6df25` |
| DDO worker v002 | `c4cb6826…95a4` |

### Method

`n1_verify/verify_n1_v001.py` → `N1_VERIFY_V001.json`, `ALL_PASS: true`. It is independent of Claude4's `chk_port_equivalence` and `patch` checks.

1. **difflib opcode pairing (DDO v001→v002 against NGC v001→v002).**
   - Binding: 1 change on each side. The insertion of 28 lines after NGC v001:45 is byte-identical to DDO's insertion after v001:51.
   - Worker: 3 changes on each side.
     - The seed-coordinate block (NGC v002:59-62) is byte-identical to DDO's.
     - The `caller_identity` fields (NGC v002:102-103) are byte-identical to DDO's.
     - The third change is the `LOCAL['binding']` pin line. It is exactly `ngc_composite_full_coupled_binding_v001.py`/`9e9caf83…` → `…_v002.py`/`cc5db369…`, the sha of the delivered binding's bytes.
2. **Reverse reconstruction.** Undoing the NGC changes on v002 gives the NGC v001 bytes exactly, for both files.
3. **Forward application.** Applying the DDO change texts at the NGC anchors gives the v002 bytes exactly.
4. **Lineage difference preserved.** The DDO-vs-NGC hunk counts are 10/10 for the binding and 9/9 for the worker, the same before and after the port. Both files compile.

**Semantic keys.** I read NGC prep v001 directly. It returns every key the inserted binding block reads:
- `fourier_arguments` with `Eref`, `ell_F`, `gamma`, `Cbar`, `mubar`, `jbar`, `registered_bravais` and `boundary_description` (prep:274-283);
- `c_m_s` (:297);
- `gas_columns[*].hi_options` (:113-118, 178-179);
- `source_pins` and `stellar_quadrature_mass_kg` (:301-302).

This agrees with Claude4's `MAP_DDO_FIX_TO_NGC_PORT.md`.

### Install constraint (root action)

The worker resolves its pins relative to its own directory. `binding` resolves at `H/ngc_composite_full_coupled_binding_v002.py`, and `composite`, `stream` and `prediction` resolve at `H.parent/coefficient_method/`.

The worker therefore runs only when both v002 files are installed in `helpers/recovered_packet_audit/`.
- There, the other 5 LOCAL pins are present with matching bytes (prep `c54c7cc9`, composite `75092cf6`, stream `cbbc4b96`, base `7167a264`, prediction `54136c71`).
- The binding v002 is not installed yet.

Run in place from `N1_port/`, the worker fails with `FileNotFoundError …/ngc_route_a_0471/coefficient_method/…`. My first fixture attempt reproduced this.

## 2. Synthetic fixture: TESTED-POSITIVE (toy scope)

`fixture/run_fixture_v001.py` (`6688dd74…`) and `case_v001.py` (`923085d0…`) produced `FIXTURE_RESULTS_V001.json` (`5bb83611…`), `ALL_PASS: true`. The work tree is `fixture/work_v001/`.

**Real files exercised, all pinned from bytes:**
- NGC worker v001/v002 and binding v001/v002;
- composite adapter `75092cf6`;
- fixed-source solver `44d9c23c`;
- checkpoint c2v003 `069b3935`.

**Toy stand-ins (`fixture/toy/`):**
- prep: the same keyword signature as NGC prep v001:36-44 and the same returned keys, with 3 annuli × 8 azimuths = 24 columns;
- physics: 6 wavevectors and a 3-node HI column;
- stream, base and prediction glue.

**Seed.** The toy seed carries the candidate seed's `numerical_inputs` verbatim (`ff0d70b4…`, all 34 keys) with toy pins.

**Worker pin table.** The worker's LOCAL table is replaced in memory only. The worker bytes are unchanged, and its `sha(__file__)` is the real `42bdd23e`.

| Case | Result |
|---|---|
| S0: v001 worker+binding, new checkpoint | `CheckpointError CALLER_IDENTITY_FIELD_REQUIRED physical_parameters`. This reproduces the dispatch's failure. |
| S1: v002, fresh checkpoint | Returned. The toy converged in 7 iterations. `IDENTITY.json` is written with all 4 mandatory caller fields. |
| S2: v002, fresh, killed (`KeyboardInterrupt`) at iteration 1, column 5 | The process died. The checkpoint was left partial. |
| S4: resume with `pressure_step_kpc` 0.005→0.006 | `IDENTITY_MISMATCH` (`identity.caller.record`). The checkpoint tree is byte-unchanged. |
| S5: resume with `Eref_J` one ulp higher | `IDENTITY_MISMATCH` (`caller.record` and `inputs_sha256.fourier_arguments.Eref`). The checkpoint tree is unchanged. |
| S3: resume with the same seed (after S4/S5) | Resumed from {iteration 1, next column 5} and converged. The reconstructed gas is **bitwise equal** to S1's. The history is equal. The identity sha is the same, `bd469dee…`. |
| S6: prepared `Eref` ≠ caller `Eref_J` (toy prep shift 1e-12) | `ValueError Caller/prepared physical parameter mismatch: Eref_J`, raised before any checkpoint directory exists (binding v002:54-57). |
| S7: seed lacks `gamma` | `KeyError 'gamma'` before the outdir is created (worker v002:59-62). |
| S8: new mode on an existing checkpoint directory | `CHECKPOINT_DIRECTORY_EXISTS`. The tree is unchanged. |

### Decoded identity of the S1 checkpoint

- **`physical_parameters`.**
  - It holds 11 keys: `Eref_J`, `ell_F_m`, `gamma`, `solar_mass_kg`, `kpc_m`, `c_m_s`, `Cbar`, `mubar`, `jbar`, `registered_bravais` and `hi_options_by_column` (24 entries).
  - The 5 seed coordinates are exactly equal to the seed values.
- **`numerical_controls`.** It equals the seed `numerical_inputs` minus `progress_directory` (33 keys).
- **`code_pins`.** It carries the binding v002, adapter, solver and checkpoint shas.
- **`worker`.** It is the v002 path and `42bdd23e`.
- **Fixed source.** The selection is `SUPPLIED`.

### Solver behaviour preserved

On identical toy inputs:
- binding v001 and v002 called with `checkpoint=None` give bitwise-identical reconstructed gas;
- both also equal S1's checkpointed v002 run, with identical residual histories.

### Limitations

- The real NGC prep, Fourier and HI modules are not exercised.
- The availability of real keys is shown by static reading of prep:274-302, the same footing as the DDO PASS_SCOPED review.

### Trial directories (kept, not deleted)

- `work_try1`: fixture path bug (above).
- `work_try2`: the toy diverged.
- `work_try3` and `FIXTURE_RESULTS_TRY3.json`: passed under the pre-final driver.

`work_v001` is the record.

## 3. NGC seed numerics PROPOSAL (Claude2 selects; nothing decided here)

**Sources:**
- Measured DDO analogue: `CODEX1/DDO154_STABLE_CACHED_COUPLED_RUN_V002`, the completed run (`finish.json` RETURNED). Its progress file is `3fe2ba91…` and its result `79855e78…`.
  - Caveat: that run is the stable-cached lineage, not the NGC v001 lineage. DDO timings are indicative only.
- Facts: `numerics/NUMERICS_FACTS_V001.json` (`520b4747…`).
- Claude4 N2: `N2_SYNTHETIC_RESULTS_V001.json` (`f546b172…`, script `9464b357…`), incorporated as cited.

| Numeric (seed) | Reviewed-code constraint | Measured DDO analogue | NGC facts | Proposal | Status / deciding test |
|---|---|---|---|---|---|
| `hi_search_limit_kpc` (32) | **Role:** a failure budget, not a gas edge (hi v002:26-27). **Search:** outward search with `FREE_BOUNDARY_NOT_BRACKETED` (:66-77); call cap (:51-52). **Scope:** one value for all columns (prep v001:113-118). Any column ValueError fails the whole iteration (`FAILED_SOURCE_PREPARATION`, solver:152-179). **Call count:** calls = 67 + ⌈\|z−\|/step⌉ + ⌈z+/step⌉ at step 0.2, ztol 1e-8, 8 panels. Claude4 N2-F checked this against 2880 DDO columns with 0 mismatches. **Bound:** genuine roots are reachable only if \|z−\|+z+ ≤ 191.4 kpc under 1024 calls; a symmetric limit is ≤ 95.7 kpc. | Limit 32. Max \|root\| 22.68 kpc (71 % of the limit) at R=14.05 kpc, the HI edge. The mean root rises steeply near the edge, with z/R ≈ 1.27. The minus side is larger (19.5 vs 12.4 kpc). Calls 73-258 of 1024. | Columns reach R=136.3 kpc (HI support 136.5 kpc). 56 % of columns lie beyond 45.5 kpc and 36 % beyond 66.9 kpc. My calibrated isotropic thin-disk toy (`VERTICAL_ROOT_TOY_V001.json`) is **TESTED-NEGATIVE as a predictor**: it fails DDO (no inner root against 0.6 kpc measured; edge 10 kpc against 17.8 kpc; amplitude spread ×6-12). So there is **no usable NGC root estimate**. | **95** (the largest symmetric limit within the existing 0.2 kpc step and 1024 calls). It costs nothing for bracketed columns and turns would-be failures at 32-95 kpc into roots. Those roots are not resolution-certified (see the grid row). Alternative: 32, which fails loudly. | **UNTESTED.** Deciding test: route-A iteration 0 itself. Columns run inner→outer, so the first `FREE_BOUNDARY_NOT_BRACKETED` (radius and side) appears after the prep plus the inner columns. That is about minutes with DDO-lineage timings. |
| Fourier grid / k-domain (G72: 12×6 panels, kmax 2) | **Required:** composite grid (binding:30). **Integers:** even ≥2 (prep:51-56). **Partition and cap:** exact partition of [−kmax,kmax], Σorders = nk ≤ **80** (prep:140-143). **Symmetry:** reflection (:144). **Zero mode:** no zero node (:153). **Cost:** waves = nk³ (:155-157). **Primitive k:** reduced mod 2π (cardinal v001:91), so kmax=2 samples periodic images (k_prim up to 2.1π, N2-H). This is the same in DDO. | G72 serves DDO separations ≤ ~28 kpc. In N2-A the worst panel error is 4.7e-3 at X0=14.1 and 0.29 at X0=22.7, so DDO is itself only partly resolved at its own outer separations. | Queries reach 44.08 kpc. In-plane separations reach ~272 kpc. N2-A: no ≤80 (or ≤96) grid resolves X ≥ 88 kpc (panel error ≥ 0.56). At 44.08 kpc (N2-B, toyIR\|hi_like), U error falls from 3.0e-2 (G72) to 6.8e-4 (G80B), 8.1e-4 (G80C) and 2.2e-6 (G80D); dU/max falls from 4.7e-2 to 1.3e-2, 3.2e-3 and 4.2e-3. For toyIR\|point, dU/max is 0.31 (G72), 0.014 (G80B), 0.0054 (G80C) and 0.053 (G80D). | **nk = 80 (the cap), G80D:** breaks [−2,−0.3,−0.1,−0.03,−0.01,0,…,2], orders [21,6,5,4,4,4,4,5,6,21]. Alternate: **G80C**, orders [15,10,5,4,3,3,3,3,4,5,10,15]. Keep kmax 2: G80K15 shows no gain, and a cutoff change is a separate counted choice. Both pass the replicated prep checks. Cost is 1.37× G72 per transform. | **UNTESTED** on the program operator, because the toys are isotropic. Structural: the 56 % of columns beyond 45 kpc sit where no admissible grid resolves the large-separation quadrature. Deciding test: route-A iteration-0 column roots and updated gas at R > 45 kpc under G80C and under G80D. If they disagree, the outer columns are grid-dominated. |
| `source_azimuth_count` (8) | **Integer:** ≥4 (prep:51-58). **Columns:** nonzero annuli × gauss × n (:164-179). **Positions:** stellar/H2 provenance positions scale with n (:203-211, 247-249). **Updated gas:** keeps actual φ columns, with no J0 replacement (binding v002:63, solver:186-195). **Limit:** checkpoint ≤ 100000 columns (c2v003:474-475). **Resolution:** the cube resolves the spoke harmonic m=n beyond R = n/kmax (n=8 → 4 kpc). | n=8. DDO queries run to 5.92 kpc, so 4 of 12 queries lie beyond 4 kpc. Columns: 576 per iteration. | Queries run 0.32-44.08 kpc, so spokes are resolved at most query radii. N2-C (spherical Poisson toy, synthetic Σ), gas-v² estimator bias: n_src=8/n_obs=8 up to 79 % (5 kpc); 16/8 ≤ 17 %; 32/8 ≤ 4.3 %; 32/12 ≤ 2.2e-4. N2-D: ring_harmonic passes m ≡ 0, ±2 mod n_obs. Indicative per-iteration cost at nk=80 (DDO-lineage timing): n=8 0.14 h, 32 0.56 h, 88 1.5 h, 272 4.8 h. | **32.** Spokes are unresolved inside 16 kpc. Pair it with an `observation_azimuth_count` that does not divide 32, with 32 ≢ ±2 mod n_obs (e.g. **12**; a counted observation numeric, binding:98-99). Alternatives: 88 (unresolved at every query radius) and 272 (unresolved over the HI support). | **UNTESTED.** Deciding test: n_src 32 vs 64 iteration-0 updated-gas difference and midplane field at the 43 radii. |
| Column count (1248) | Derived: 39 nonzero annuli (of 51; zero annuli are skipped, prep:176) × `source_gauss_order` × n_az. Limit ≤ 100000 (c2v003:474). | 576 (18×4×8). Columns took 0.137 s + 0.26 ms per call (median 0.16 s). The transform took 102 s per iteration (2.8e-8 s per position·wave). | 156 per azimuth at gauss 4 | **4992** (gauss 4 kept, as in DDO; n_az 32) | Derived (FORMAL-RESULT from prep:166-179). |
| `pressure_step_kpc` (0.005) | Requires 0 < d < R (pred v005:107-110). Steps d and d/2 must agree within atol + rtol·\|dp\|, with rtol 0.1 (:118-125). | d/d2 relative difference: max 7.3e-4, median 1.1e-5. | Minimum query 0.32 kpc. Minimum query-to-annulus-edge distance 0.0115 kpc (8.04 kpc), so d = 0.005 keeps R±d inside one annulus. d ≥ 0.0115 would straddle an edge, which matters only if the Bernstein reconstruction is less smooth at edges (UNTESTED). | **0.005** (keep) | TESTED-POSITIVE for DDO. For NGC, UNTESTED; the run's own d/d2 check fails loudly. |
| `azimuth_step_rad` (0.02) | Requires 0 < da < π (pred v005:107-110). da and da/2 central differences are reported only, with no pass/fail check (:159-163). One scalar serves all 43 queries (binding:109). | Arc at the maximum query 0.118 kpc; kmax·R·da = 0.237. Measured da/da2 relative difference: max 4.9 %, median 0.28 %. | At 44.08 kpc, kmax·R·da = 1.76, so (m·da)²/6 reaches 0.52 for band-edge harmonics. Spoke m=32: 6.8 % at 0.02. | **0.0025.** This equals the DDO kmax·R·da at the NGC outer query (0.00269). Band edge 0.8 %; spoke m=32 0.1 %, m=88 0.8 %. | **UNTESTED.** The roundoff floor at 8× smaller da is unmeasured. Deciding test: the run's own `pressure_phi_stencil_difference` at all queries against DDO's 0.28 % median. |
| `h2_tail_mass_rtol` (1e-12, CALL_SPEC; no reviewed value) | Positive, finite, not bool (worker v002:54-56; prep:81-82). The tail masses are normalized to the exact total and then compared (prep:225-240), so the checked error is fsum rounding only. | None: DDO prep has no H2 tail. | N2-E: synthetic maximum 3.0e-16, p99 2.2e-16 over 20000 trials, 62 % exactly 0. Raw unnormalized GL4 error at NGC values is 6.9e-3, which the normalization removes. | **1e-12.** Any value ≳ 1e-14 passes identically. Below ~3e-16 the check could fail spuriously. It has no effect on numerics. | FORMAL-RESULT (normalization argument) plus TESTED-POSITIVE (synthetic). The NGC value is evaluated in the prep within seconds. |

**Coupled numerics.**
- `hi_search_step_kpc` 0.2 and `hi_max_metric_calls` 1024 set the 95.7 kpc ceiling on the limit.
- A larger limit needs either more calls or a coarser step. A coarser step trades crossing resolution (hi v002:27-28).

## 4. Open items, each with its deciding test

1. **Install** both v002 files in `helpers/recovered_packet_audit/`. This is a root action.
2. **NGC vertical roots.** UNTESTED. Decided by the first route-A iteration-0 pass.
3. **Outer-column grid dependence** (56 % of columns beyond 45 kpc). UNTESTED. Decided by G80C against G80D at iteration 0.
4. **Azimuth count and observation aliasing.** UNTESTED on the program operator. Decided by n_src 32 against 64.
5. **NGC v001-lineage timing.** UNTESTED. The DDO numbers come from the stable-cached lineage.
