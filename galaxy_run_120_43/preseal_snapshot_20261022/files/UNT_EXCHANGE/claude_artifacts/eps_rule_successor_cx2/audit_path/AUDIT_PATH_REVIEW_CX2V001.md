# EPS dense-audit path review CX2V001

Date -u: Wed Oct 21 17:33:59 UTC 2026. Scope ROOT0855/A296, independent Codex2 internal helper. Runtime note: **nice unavailable (sandbox); 0514 waiver**. Only source/metadata/byte inspection and independent JSON identity comparisons were performed. **No project module import, reviewed-function execution, dense search, forward/route/worker launch or actual run-tree/NGC-data access.**

**FORMAL path disposition:** Do not call the original `point_context`. A narrowly extracted numerical route is available from allowed, exact-byte DDO certification inputs. The candidate wrapper is ready for parent review; its numerical behavior remains **UNTESTED** until the parent executes its fail-closed checks/audit.

## Unsafe default path, with ordering

`producer.point_context` lines 73–109 first calls `CU.derive_details`, then `CC.qinf_binder`. Custody lines 103–141 load the driver, coefficient arrays and geometry/prereg inputs and hash broad source pins. That is unnecessary for a fixed-symbol EPS envelope audit and is deliberately omitted here, rather than treating its entire input closure as authorized.

`CC.qinf_binder` lines 203–207 calls `pin('seed_scan_result')` in its dependency comprehension: this hashes an actual `/CLAUDE2/runs/.../result.json`. It next imports `LWR`. **LWR top-level lines 48–62** read an actual NGC run's checkpoint identity and start/seed, then initialize reference modules from those run-derived pins. The code-only inspection did not traverse any of those embedded pointers. The fact that the original producer calls its operation static does not make those input reads allowed in this lane.

Neither `qinf_binder`, `repro_qinf_anchor`, `point_context`, `CU.derive_details`, the original LWR top level, any full driver module, or any forward/column solver is executed by the proposed wrapper. The dense routine uses NumPy 10×10 algebraic symbol solves; those are the authorized static search calculation, not a galaxy/route launch.

## Exact allowed point/input route

The original CP1 POINT_START records identify these exact saved specifications. Independent canonical identity reconstruction (driver SHA, physical, coefficients and whole numerics excluding only EPS/LO slots) equals each saved EPS identity and reproduces its full point key. Row302's point-list binding independently names the same spec/pin. These are certification-input drafts, not newly asserted ROOT_FINAL launch specs.

- Row302: key `6f4604efe6d7fe348d9ca4986d9042234ed54d5df63b254b4e8c3b6c43861ee1`; saved failed shell `[46,47]`.
- Row501: key `421cb796874019be37c7ea90d54f7e55ef1baa0d4d254d70b2f5358f973bcf2c`; saved failed shell `[76,77]`.
- Row504: key `cdc5592d149fa9efd319e4ac1b3e2fc17d5d52ca51b92c24c36709dfed1a10c0`; saved failed shell `[73,74]`.

All three name the same separate A2 coefficient archive under `CRITICAL_PATH_EVALUATION.../sampler_eval`, not under a run tree. Its actual bytes were hashed: 514,382 bytes, SHA256 `2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7`. Lexical component/symlink-target checks found no redirection into a run/data tree. The wrapper selects only `source_hessian_grid`, `background_C`, `background_mu` from this exact archive using `allow_pickle=False`. These are exactly the source arrays against which CC lines 208–214 compare its inventory copy; the wrapper does not read the inventory or any run-derived seed.

Effective point parameters follow the original producer lines 82–86 exactly: `Eref = common_scale_s * Eref_J`, `gam = common_scale_s * gamma`, `ell = ell_F_m`. KPC is obtained from the pinned DDO driver's static literal, without importing the driver. The mandatory saved-discrete reproduction below provides a direct fail-closed check against the original point evaluation; the original NGC-seeded reference check is not claimed rerun.

## Candidate and dependency closure

Selected build: `dense_eps_audit_cx2v002.py`, SHA256 `618ba8fa9db2e7d7747c007d00f0ec64fd30083a164b01ad8ff60195e1b0d341`.

The wrapper parses pinned source and compiles only the following unchanged definition nodes into explicit NumPy/math namespaces:

- Static binding: `_real`, `mandel_matrix`, `mandel_vector`.
- LWR: `root_C`, `Binder`; static `A_BRAVAIS` is checked against its source AST, and `DIRS` is read as literal data.
- CC: `_family`, `direction_sets`, `shell_k`, `q_of`, with literal `PER_DECADE`. `_family` imports only standard-library itertools.
- C2: `Envelope`, `fib_hemi`, `torus_grid_v`, `env_full`, `tangent_basis`, `refine`, `distinct_top`.
- Producer: `finite`, `mandel`, `values_from_x`, `discrete_shell`, `search_envelope`; registered SETTINGS is read as static literal/keyword-dict data.

No selected definition performs file I/O, process launch or network access. Module-level import/load statements are not selected. Input SHA checks are mandatory; source algorithms, seed expression, candidate count and iteration limits are unchanged. The wrapper fences forbidden lexical file/metadata paths, checks symlink targets before traversal, blocks process/network audit events, and rehashes every input plus itself before exclusive publication. This is a bounded execution design, not a claim of generic adversarial sandbox security.

The first wrapper file remains preserved and unexecuted. V002 corrects the static SETTINGS literal reader (the source uses `dict(...)` keyword construction), adds independent grid/background custody reconstruction, and checks self-source stability. Both parse as Python AST; neither was invoked in this slice.

## Required validation and parent execution guide

Default invocation (without `--dense`) performs **cheap numerical validation only**, under the prescribed isolated Python and six single-thread BLAS variables. Parameters: `--row 302 --shell-lo 46 --out <new JSON directly under audit_path>`. No printed command was executed by this helper.

Mandatory checks before any dense search:

1. Exact spec/EPS/point/producer/settings and coefficient-reference identity.
2. Exact pinned A2 bytes and finite arrays; positive-definite background.
3. Recompute the saved `grid_sha256` and `background_sha256` from the arrays, physical spec and original custody encoding; mismatch refuses. Geometry/modules/row-contract custody remains linked to the saved EPS, explicitly **not re-derived**.
4. Reproduce the saved selected-shell discrete levels and full discrete summary **exactly**, including directions/max locations/counts and imaginary diagnostic.
5. At the saved maximizing nodes, require bitwise equality between extracted Binder `q_of` and extracted Envelope `q(t_of(k))`.

For the actual mandatory dense audit, add `--dense`. It executes the unchanged `search_envelope(..., objective='EPS', audit=True, previous=None)`: 20³ torus ×400 hemisphere directions ×5 radial fractions =16,000,000 grid nodes; 16 selected starts, 48 local candidates, 120 maximum iterations, exact original deterministic seed. No smaller audit is substituted. The saved production denominator is exactly the selected shell's `envelope.estimate`.

For full existing-audit reproduction, optional `--reference-audit-lo 45` (row302 has this saved audit) executes that existing dense search first and requires exact equality of its complete `dense_search` result. If omitted, the output explicitly says `existing_dense_reproduction: NOT_RUN`; no claim of that stronger check is made. Parent decides the execution sequence/cost. For rows501/504, use shell-lo76/73 respectively; the same input/identity guards apply.

Dense result schema matches the re-evaluation consumer: `UNT_EPS_NEGLIGIBLE_DENSE_AUDIT_CX2V001`, TESTED, registered, exact source-record pin, point key, original-producer pin, actual audit-wrapper pin, range, production, dense, dense_over_production and complete dense_search. A validation-only result has a different schema and cannot stand in for a dense audit. All results retain `production_admissible:false`, numerical-estimate/not-rigorous-sup scope and explicit custody limitations. No new certification result exists yet in this slice.

## Remaining scope

TESTED: source bytes, AST syntax, safe selected saved-input paths, A2 archive byte identity, and the three independent spec-to-EPS canonical identity joins. FORMAL: forbidden default dependency path and the proposed pure-definition closure. UNTESTED: extracted numerical functions, saved-discrete/bitwise checks, existing-dense reproduction, dense estimates/ratios and A296 acceptance. Parent must review/run the wrapper before using any audit result; no policy constants, search choices or source files were modified by this path review.

## Full byte pins

- `[producer]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/point_response_producer_cx2v002.py` — SHA256 `a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231` (19198 bytes).
- `[custody]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/custody_cx2v002.py` — SHA256 `6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377` (7975 bytes).
- `[C2]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/certs2_common_r5_cx2v001.py` — SHA256 `f8f422f034153b4551e5fd5f89740cb594cb9d877e54b467c617206d2fcd6d8c` (10064 bytes).
- `[CC]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificates_per_point/certs_common_r5_cx2v001.py` — SHA256 `c75aaa5a197efe7bde1014269d74aa37810ccce6f95b7eec1078352f09ffb3b7` (17580 bytes).
- `[LWR]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/long_wavelength_response_c2/tools/lwr_common_v001.py` — SHA256 `758740ebf6caeb80876497674c3ee844f0ec8a9d0fae5d1fb8d491376e3aff48` (9673 bytes).
- `[static_binding]` `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/response_packet_audit/owned_static_action_metric_binding_v002.py` — SHA256 `7130a277ca59b07c8ce788eb20bcb50c996a3575f6fa0e644e971b0d766aee1f` (15174 bytes).
- `[driver]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py` — SHA256 `b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6` (350370 bytes).
- `[A2_grid]` `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz` — SHA256 `2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7` (514382 bytes).
- `[ROOT0855]` `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0855_2026-10-21_codex2_claude3_A296_final_text_build_now_and_F5_gap_proposal.md` — SHA256 `1541dad07b9d14d994fc7f595c8276f2f0555f38b67f1c8fd1142d883fa36b5a` (1511 bytes).
- `[row302_start]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/cp1_run_c3v004b/P302_6f4604efe6d7fe34_W0003_P02_a1/POINT_START_6f4604efe6d7fe34.json` — SHA256 `764ac6260f3c4961a51eaa8be33833b4c7f872dedfdc16c997e3804a2eeffd07` (2485 bytes).
- `[row302_spec]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/future_wave_points_cx1/NOMINAL_W3_MINUS_DRAFT/SPEC_W0003_P02_6f4604efe6d7fe34.json` — SHA256 `7b32dac96337d06c4046c63f967b0a95503e952e88dcc980ae91d474d2b09521` (7002 bytes).
- `[row302_eps]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/cp1_run_c3v004b/P302_6f4604efe6d7fe34_W0003_P02_a1/EPS_NUMERIC_6f4604efe6d7fe34.json` — SHA256 `3babf8f45719220ac161b5e784cb86e2684129e94be5715848088ae61910dc72` (429560 bytes).
- `[row501_start]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/cp1_run_c3v004b/P501_421cb796874019be_W0005_P01_a1/POINT_START_421cb796874019be.json` — SHA256 `26848038817d38e613451478706383b8a1350d98c01db23cbe041391467cffb6` (2492 bytes).
- `[row501_spec]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/future_wave_points_cx1/CONDITIONAL_GLOBAL_POOL_DRAFT/SPEC_W0005_P01_421cb796874019be.json` — SHA256 `35246e7e5ed8602d21013707a00782e28a8a21c917fae7885f16c32fdef19d30` (7003 bytes).
- `[row501_eps]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/cp1_run_c3v004b/P501_421cb796874019be_W0005_P01_a1/EPS_NUMERIC_421cb796874019be.json` — SHA256 `52cc2502b60b53ad14a55fbb94f900e0a7d06e4f256233a9decbb5c48c33ab06` (429728 bytes).
- `[row504_start]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/cp1_run_c3v004b/P504_cdc5592d149fa9ef_W0005_P04_a1/POINT_START_cdc5592d149fa9ef.json` — SHA256 `29601db9275dfd6482aba3f4d4dcaf39c33025849fa94d16dea55d8453ec75c1` (2492 bytes).
- `[row504_spec]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/future_wave_points_cx1/CONDITIONAL_GLOBAL_POOL_DRAFT/SPEC_W0005_P04_cdc5592d149fa9ef.json` — SHA256 `25b9ef8a6458eed2539b866fef2b2cbe7d400e26602905816d8b06b4646acc22` (7005 bytes).
- `[row504_eps]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/cp1_run_c3v004b/P504_cdc5592d149fa9ef_W0005_P04_a1/EPS_NUMERIC_cdc5592d149fa9ef.json` — SHA256 `0005d1615277d4c48ab1c1541e9f7c059bb18d11fc13bb13a9da860202d4a3dd` (427660 bytes).
- `[row302_context]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/cp1_run_c3v004b/P302_6f4604efe6d7fe34_W0003_P02_a1/STAGE_CONTEXT_6f4604efe6d7fe34.json` — SHA256 `e8d0ff09cbfc27543cff258112fe4864299aaf20a64a6a599e362e4e1fb7d168` (7522 bytes).
- `[row302_list_binding]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/cp1_run_c3v004b/P302_6f4604efe6d7fe34_W0003_P02_a1/POINT_LIST_BINDING_6f4604efe6d7fe34.json` — SHA256 `30f9e70be68aa55b0fecb372faef217934d62593034d7a0568efc97df0a21e98` (1246 bytes).
- `[dense_eps_audit_cx2v001.py]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/audit_path/dense_eps_audit_cx2v001.py` — SHA256 `4124b0ef126072a148f4f7874b05aebbe9b18144e9c603262a64bf213e3fd6a0` (16482 bytes).
- `[dense_eps_audit_cx2v002.py]` `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/eps_rule_successor_cx2/audit_path/dense_eps_audit_cx2v002.py` — SHA256 `618ba8fa9db2e7d7747c007d00f0ec64fd30083a164b01ad8ff60195e1b0d341` (17818 bytes).
