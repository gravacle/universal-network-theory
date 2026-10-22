# Driver EPS consumption — independent source analysis CX2V001

Date -u: Wed Oct 21 17:25:04 UTC 2026. ROOT0854 source-only slice. Runtime note: **nice unavailable (sandbox); 0514 waiver**. Exact prescribed Python `-I -B`, stdlib only, six BLAS thread environment variables set to 1. No project import, reviewed-function execution, scientific computation/launch, run-tree access, NGC data, target velocity, or further Claude3 analysis was used.

**FORMAL conclusion:** Neither requested driver feeds numerical EPS values into the continuum tail/lapse kernel. Both carry the byte-pinned EPS reference through configuration, worker checks, TailState custody and admission checks. The shared library separately exposes a **per-shell weighted bound API**, which is not called by the reviewed native route-A/route-B paths. Both route-B bindings explicitly record `NOT_EVALUATED_IN_STAGE` for SRB-ROT. This distinction prevents mistaking an external certificate/gate computation for a driver numerical correction.

**TESTED mechanics:** 189/189 byte-pin, source/AST and final-stability checks passed over 36 source files. These are static checks, not scientific or runtime acceptance tests. The source facts below are FORMAL interpretations of those exact bytes. Full path/byte SHA/size/start-end pins are in SOURCE_PINS_CX2V001.json and repeated in the source appendix; detailed EPS sites and checks are in STATIC_SOURCE_RESULTS_CX2V003.json. No admission or rule successor is authorized by this report.

## Exact consumption paths

1. **DDO driver.** `[ddo]` lines 884–937 load the pinned common library and normalize a strict configuration. `eps_certificate` is a `{path,sha256}` reference, a pending planning sentinel, or the restricted test-only sentinel. `uvt_plan` lines 1076–1105 checks certificate bytes and propagates the same references into request/argv. The active continuum tables are selected at lines 946–950; the worker, controller, binding and library lineage is checked at lines 1176–1212. The driver never reads shell `eps`, `eps_max`, or `certified` values to alter a physical quantity.
2. **Route A, DDO and NGC.** The six reviewed serial/parallel workers (ordinary DDO, ordinary NGC, STAGE0 NGC) pin the same `[controller]` and `[lib]`; EPS CLI reference must equal the request and the bytes must match its SHA. `[ddo_a]` lines 113–125 and `[ngc_a]` lines 110–117 create `RouteATailController.from_prepared`, install its boundary and bind the solver. The controller's `_build` lines 395–406 calls `lib.build` with source roster, physical constants, quadrature/config and I1-T; `begin_iteration` lines 409–427 sets the resulting state as the boundary. Its completion/monitor path lines 429–525 uses actual state jets and source differences. `[serial_solver]` and `[parallel_solver]` call these hooks and consume boundary jets; they do not consume EPS values. `[facade]` obtains actual tail jets/lapse differences, not an EPS-based numerical correction.
3. **Route B, DDO and NGC.** `[ddo_b]` `_build` lines 336–341 and `[ngc_b]` lines 371–376 call the same `lib.build` and install a TailBoundary. Manifest/inherited paths recover the recorded TailState and enforce state/config custody; they do not insert EPS coefficients into the tail arrays. The eight selected DDO stage wrappers and eleven selected NGC stage sources have no bound-API call or direct EPS numeric reader. `[ddo_b]` lines 215–216 and `[ngc_b]` lines 220–221 explicitly defer SRB-ROT to external gates computed from the state digest. Actual proof-side adapter/gate semantics belong to the parent's complementary analysis; this report does not claim either driver itself evaluates SRB-ROT.
4. **NGC final overrides, not merely its inherited prefix.** `[ngc]` lines 5117–5131 swap the selected NGC stage/worker/binding tables, while retaining the common controller/library. Lines 6523–6526 wrap that context in strict record operations. Strict normalizer/info clones at 6602–6628 still call common `uvt_info`/`uvt_config`; the strict chain at 8405 onward still invokes `_uvt_ngc_v011_plan` at 8586. The strict dispatch replacement table at 9183–9191, final selected-record dispatch at 9194–9216 and final CX3R008 helper overrides do not add an EPS numerical reader or replace the shared bound/kernel routines. Both ordinary and STAGE0 serial/parallel worker byte pins point to the same common library/controller. The NGC nodes branch is refused; the DDO T2-only `nodes_v001` alternate numerical implementation is outside this production-continuum analysis.

## What the shared library actually does

`[lib]` `normalize_config` lines 115–130 validates certificate reference shape/hex SHA and includes that reference in the normalized configuration digest. In `build` lines 664–674, the certificate is **opened as bytes and hashed**, without JSON parsing or any numerical shell lookup. Lines 685–688 record EPS/LO references, config SHA and the `production_admissible` flag. That flag here reflects non-test certificate references and I1-T conditions; it is not a parser's scientific certification of EPS shell contents.

The numerical tail construction uses physical/source/quadrature inputs: prefactor at 684; grid at 694; roster factors P/F at 725–728; source/quadrature products and ring tables at 738–756; source-weighted shell integrals at 757 onward. `TailState.cyl_jets` 480–517, `jet` 520–537 and `lapse_pair` 557–582 evaluate those arrays. None reads numerical EPS values. `TailState._digest` 353–358 includes both the record and arrays, so changing a certificate pin **does change custody identity**, even when physical arrays are unchanged.

The separate `_eps_per_shell` function at 830–844 reads `eps_certificate['shells']`. For each state shell it selects the **maximum among overlapping certificate rows**, not the global certificate maximum. `field_bound` at 847–857 computes, for derivative order a=0,1,2:

`F_a = sum_i e_i * B_i^(a)`

where `e_i` is that overlap maximum and `B_i^(a)` is the state's source-dependent shell integral. This bound API consumes neither `certified` flags nor a global `eps_max`. `srb_rot` at 860–871 uses `F_1` and returns the maximum column bound for each row, with a `tau/10` acceptance comparison. Its own label is a necessary, not sufficient, static rotation-law channel. The function labels EPS and the node-assigned integrals as estimates and explicitly says **not a proven sup**. `monitor_MT` 874–885 is instead based on differences of actual tail jets and does not read EPS.

## Consequences for a local certification-rule change

**FORMAL, conditional on fixed physical/source/numerical inputs and consistent references:** Changing only a certification status/rule field in an EPS document, while leaving every shell EPS value/interval unchanged, cannot change the shared kernel's numerical tail/lapse construction or the separate estimated field/SRB bound. It can change upstream admission, availability, certificate SHA, normalized config SHA, state digest and downstream custody. If the pin is not rebound consistently, the runtime rejects the bytes; this is not an unchanged successful result. This report does not claim output-file byte identity, reuse/resume permission, or a successful preflight.

**FORMAL sensitivity if an EPS estimate is changed:** In general,

`Delta F_a = sum_i (e_i_new - e_i_old) * B_i^(a)`.

For a single exactly matching certificate/state shell j, with no competing overlapping row changing the maximum, this reduces to `Delta F_a = Delta eps_j * B_j^(a)`. Overlapping certificates require recomputing each affected maximum. For fixed positive row inputs, define `beta_row = max_columns[R*c^2/(2*N_min*v_c*1000)]`; then `Delta SRB_row = beta_row * Delta F_1`. Thus a numerical EPS revision can change the estimated bound and its threshold decision without changing the physical tail kernel.

**FORMAL limitation:** A small `eps_j / eps_max` alone does not bound that shell's share of `F_a`; its source-dependent `B_j^(a)` can dominate. Conversely, if one deliberately constructs a global-max envelope and all estimated EPS values remain below the same maximum, that particular envelope stays unchanged. The reviewed library's actual bound API retains per-shell weights. No row-specific numerical bound change can be supplied here without the applicable source-state shell integrals and row factors, which were not read or computed.

**UNTESTED true-error claim:** The underconverged shell's finite-refinement samples and ratio do not establish a rigorous supremum on its unknown true error. Therefore no finite actual-physics worst-case ceiling follows from this source analysis or from the supplied small EPS estimate alone. ROOT0854's row302 values are the dispatch's stated case, not independently reproduced numerical measurements in this slice. No conclusion here recommends loosening the rule; final constants and adoption remain root decisions.

## Verification history and boundaries

`inspect_eps_source_cx2v001.py` stopped on a static selector assumption because both `_DifferenceRoster` and `Binding` define `record`; `v002` stopped because its selector used the incorrect class name `TailBinding`. Both files are preserved, and neither wrote a results file or executed scientific code. The final immutable `v003` selects exact `Binding.record` and produces 189/189 passing static checks. All 36 source hashes matched their declared pins at first read and remained unchanged at final rehash. No candidate source file was edited.

TESTED covers source bytes, AST/text mechanics and pin lineage. FORMAL covers the explicitly scoped dataflow/equations and conditional invariance. UNTESTED covers actual run acceptance, saved or future physical output values, actual row302 state integrals, rigorously bounded true EPS error, policy registration/rationale and any downstream proof adapter not in this driver slice. No actual run/evidence/seed/profile paths embedded in source were followed.

## Source appendix: byte identities

- `[ddo]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py`
  SHA256 `b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6`; 350370 bytes; identical end SHA.
- `[ngc]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py`
  SHA256 `577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377`; 669113 bytes; identical end SHA.
- `[lib]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py`
  SHA256 `2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54`; 47830 bytes; identical end SHA.
- `[controller]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_a/route_a_uv_tail_controller_c2v001_r5.py`
  SHA256 `c5bdd0553968e3f00b61db89f7944cebe51166006f58b727a7aed2a9b6a434fc`; 35085 bytes; identical end SHA.
- `[ddo_b]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/uvt_route_b_binding_c2v001_r5.py`
  SHA256 `1e27430c12cc84195b7642fe925bc6f9916a55158ecc02c9fbff9b8564506329`; 33672 bytes; identical end SHA.
- `[ngc_b]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_uvt_route_b_binding_cx3v006_r5cx3v001_cx3v005.py`
  SHA256 `aee7af1286f2d3d9d52117d6b4d4ae82e31d8776af4a4b0a6da7cee96be12fb3`; 46896 bytes; identical end SHA.
- `[ddo_a]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_readout_c2/ddo_composite_stable_cached_binding_v002_uvtail_ro1_c2v002.py`
  SHA256 `86af6198045ee6995daa7b57e78570643ddbd9edcc0eba42e2fdc816897ca885`; 16104 bytes; identical end SHA.
- `[ngc_a]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/route_a/ngc_composite_full_coupled_binding_uvtail_ro1_cx3v011.py`
  SHA256 `9b5ce82adea46c8e660f44b0fc91e8dbe5d0616cc1de1fd4467878ef3b5c0668`; 15785 bytes; identical end SHA.
- `[ddo_worker]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/ro1_readout_c2/ddo_composite_stable_cached_root_worker_v002_uvtail_ro1_c2v002_r5.py`
  SHA256 `fbe9ae79ac113aab76109ece785d8030729ce62890dc76ff58144a75af6c17b3`; 12177 bytes; identical end SHA.
- `[ddo_parallel]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/ro1_readout_c2/ddo_composite_stable_cached_root_worker_v002_parallel_uvtail_ro1_c2v002_r5.py`
  SHA256 `869ce3870a13fdc94a014cdb0b34eab867c05e59ab7d8abfb15f7db382fd52da`; 12576 bytes; identical end SHA.
- `[ngc_worker]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/prep_loader_fix/ngc43_coupled_root_worker_uvtail_ro1_cx3v011_r5cx3v001_cx3v005.py`
  SHA256 `ee27227c2cee3093589ae6b6546a0d88a1bbe20c47ba4dacff497ad7cc80189f`; 12512 bytes; identical end SHA.
- `[ngc_parallel]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/prep_loader_fix/ngc43_coupled_root_worker_parallel_uvtail_ro1_cx3v011_r5cx3v001_cx3v005.py`
  SHA256 `293a417f493fee2b59176bc60873fa3cdea5e586f375efbe51cbd10651e045b1`; 12911 bytes; identical end SHA.
- `[ngc_stage0_worker]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/stage0_alternative/sources/ngc43_coupled_root_worker_uvtail_ro1_cx3v011_r5cx3v001_cx3v005.py`
  SHA256 `f7c8fb43852eece4cddf4aac769aab7f91eab4445575296fb19a4e5454677f9e`; 12523 bytes; identical end SHA.
- `[ngc_stage0_parallel]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/stage0_alternative/sources/ngc43_coupled_root_worker_parallel_uvtail_ro1_cx3v011_r5cx3v001_cx3v005.py`
  SHA256 `908c9b4b0898136e00ea253be60be3f0e5763237234385cb76e8b3158b7f4a9b`; 12922 bytes; identical end SHA.
- `[facade]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/route_a/owned_stable_lapse_hi_facade_uvtail_c2v001.py`
  SHA256 `191fb7bd91708b6aae9fdc21d1bf81c01482374ae5b6f80cbaad5a9a8438af9c`; 3695 bytes; identical end SHA.
- `[serial_solver]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/route_a/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_uvtail_c2v001.py`
  SHA256 `8ef3079b0a23c32c688605e96eb5b79beb79768578cc7aef22ea087c7ae12469`; 18956 bytes; identical end SHA.
- `[parallel_solver]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/route_a/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_parallel_uvtail_c2v001.py`
  SHA256 `7667025bd9382a58688153fde98bf90f2b67d27baa39a939982631c305c229db`; 60584 bytes; identical end SHA.
- `[ddo_stage_reference]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/driver_r4/route_b/ddo_homotopy_reference_root_worker_v001_gal_c2v005_uvt_c2v003_r5.py`
  SHA256 `022f257066032865a8c068009fea7618844a993e38d9eb19cc82f303fa637642`; 29540 bytes; identical end SHA.
- `[ddo_stage_body]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/stages/ddo_saved_root_body_array_root_v002_gal_c2v005_uvt_c2v001_r5.py`
  SHA256 `4b0f28fa0539c4ebb2413b91dddc4f93cc74f147000dccb2926177e1da16a42a`; 30641 bytes; identical end SHA.
- `[ddo_stage_offset]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/stages/ddo_body_source_offset_root_v003_gal_c2v005_uvt_c2v001_r5.py`
  SHA256 `693686352af3020734530b5e896364e58037926c659c23d3e514c88cb5cccbe6`; 30462 bytes; identical end SHA.
- `[ddo_stage_columns_v001]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/stages/ddo_fixed_K_free_surface_root_v001_gal_c2v005_uvt_c2v001_r5.py`
  SHA256 `a129b3d8ed5e9ededd9d854ae4ef971f8150dbd9ed79d697331d2e7e8b1f0a7b`; 24240 bytes; identical end SHA.
- `[ddo_stage_rotation_v001]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/stages/ddo_free_surface_rotation_root_v001_gal_c2v005_uvt_c2v001_r5.py`
  SHA256 `139643c01d3be53e34df8ececccea69d4a2a7377486498c4d1035e5cb4433242`; 28954 bytes; identical end SHA.
- `[ddo_stage_columns_v003]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/stages/ddo_fixed_K_free_surface_root_v003_gal_c2v005_uvt_c2v001_r5.py`
  SHA256 `a1a8a4bdc7bd928e664b2cd595171d4e4fd5a72a61825bc24bfb7a689cc8b3ff`; 26377 bytes; identical end SHA.
- `[ddo_stage_columns_v005]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/stages/ddo_fixed_K_free_surface_root_v005_gal_c2v005_uvt_c2v001_r5.py`
  SHA256 `e0d3132e82dc2b5c2557b85a846233c4ea3cddfe885795fc4605af3f78d683ff`; 27400 bytes; identical end SHA.
- `[ddo_stage_rotation_v005]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/stages/ddo_free_surface_rotation_root_v005_gal_c2v005_uvt_c2v001_r5.py`
  SHA256 `8459ce3cbccb47e3b59f7cf08f33ce8565efae9dd6df8d79d35aa27782b24601`; 32921 bytes; identical end SHA.
- `[ngc_stage_reference]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_homotopy_reference_root_worker_v001_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py`
  SHA256 `69db1fe41adf2bf610acd801a2ffb6f605701b890bef45ab90c99a45c8c8483b`; 29692 bytes; identical end SHA.
- `[ngc_stage_body]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_saved_root_body_array_root_v002_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py`
  SHA256 `d1d70e11d3464d9081e38c6eec560104769e95a3f30e166ac54eac618bea3ad9`; 30947 bytes; identical end SHA.
- `[ngc_stage_offset]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_body_source_offset_root_v003_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py`
  SHA256 `1ede2384637bfacaa52944b2aebb70fb82bfe1ede7ec08da3c9691e929df68e3`; 30366 bytes; identical end SHA.
- `[ngc_stage_columns_v001]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_fixed_K_free_surface_root_v001_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py`
  SHA256 `4d4c34674d45a3832f28591ac53b88c6f343ce194b1c75d2fced608f55dcd60a`; 24503 bytes; identical end SHA.
- `[ngc_stage_rotation_v001]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_free_surface_rotation_root_v001_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py`
  SHA256 `9922a919ebadfc1ba17508f42ee553918d50ad29e36fdfa2bc3677bcbc1767c4`; 29112 bytes; identical end SHA.
- `[ngc_stage_columns_v003]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_fixed_K_free_surface_root_v003_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py`
  SHA256 `5657503c4d5c9c7db203c1de09f3ceb6cbd9a5a70aa4e680a56227f20e03b58b`; 26640 bytes; identical end SHA.
- `[ngc_stage_columns_v005]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_fixed_K_free_surface_root_v005_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py`
  SHA256 `dd0c759be8b85b107828b1db8d7e453134176ac32a68544f6f6d6a8f1f92eee0`; 27663 bytes; identical end SHA.
- `[ngc_stage_rotation_v005]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_free_surface_rotation_root_v005_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py`
  SHA256 `e22e79e80a63825458ca659dd32c81bef473e170ba81486ef9db86929007249f`; 33079 bytes; identical end SHA.
- `[ngc_stage_column_mean_v004]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_lower_entropy_column_mean_root_v004_gal_c2v005_cx3v006_r5cx3v001_cx3v005.py`
  SHA256 `51ab097c15ff4e30f4001ec0989cbaaac479b11c8c8956eef30b44253092e4dd`; 26123 bytes; identical end SHA.
- `[ngc_stage_feedback_v002]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_free_surface_native_feedback_root_v002_gal_c2v005_r5cx3v001_cx3v005.py`
  SHA256 `fb8eaae6a5202f5eeae5f38a6573b9a0c8cd8ddbbad1ebcbc7c93a1104996ac8`; 27043 bytes; identical end SHA.
- `[ngc_stage_feedback_v004]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_free_surface_native_feedback_root_v004_gal_c2v005_r5cx3v001_cx3v005.py`
  SHA256 `abbc62f53b3d44d776357a2d598844ce96a7b503d3dceb403f79bcd9204fc593`; 29483 bytes; identical end SHA.

Dispatch/runtime authority bytes (read only):

- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0854_2026-10-21_codex2_independent_eps_consumption_analysis_then_rule_successor_standby.md` — SHA256 `9669f5d4fa93931ad0d546d2ac9834f962ad946b57f45a3695023a92b234ae5c`.
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0514_2026-10-18_codex_any_nice_waiver.md` — SHA256 `50d4ab43ba3b2dbdc91330d5d3846010661871b654ac4c5a03b836cbb48ccd55`.
