# INTERFACE_V008: route-B driver `galaxy_m0_forward_c2v008.py` (Claude2 lane `driver_v008_c2`)

## Status

READY_FOR_CHECK, with one part BLOCKED by the reviewed stage binding (not by the driver):

- (a) distance. Ported and tested. At D = 4.04 every request and input is byte-identical to v007. At D != 4.04 the driver produces exactly the inputs v003c produces. **BLOCKED in run mode:** the gal_c2v004 stages' own admission refuses the per-call geometry fields for DDO154, so run mode stops before any stage with `BLOCKED GEOMETRY_NOT_ADMITTED_BY_STAGE_BINDING`. Unblocking needs a stage/schema successor (new reviewed bytes), which is outside this task.
- (b) comparator C1 fix: done.
- (c) LE parallelism: not added; the reason is below.
- (d) CHECK D1: ported (DDO154).

Nothing real was launched. Every test is synthetic, a guarded dry run, or a run-mode call that ends or is captured before any stage executes.

## Files (sha256 from bytes; the full list is in HASHES.txt)

| File | sha256 |
|---|---|
| `galaxy_m0_forward_c2v008.py` | `f8e4770106abb83df5e658e91edc5593198fe87f0600ee5d1946f22415902f28` |
| `DIFF_V007_V008.diff` (`diff -u` from v007 `0338584b`; 22 hunks) | `f26b3aaaee3865dc0c60de9846ff3df7105c4ef8411542613096ea58a035b8b8` |
| `deciding/compare_deciding_ii_c2v008.py` | `b122b8e691b46d5fc83149d5b9454f79b560e49dc600f07d8a11b140d174a467` |
| `deciding/CALL_A2_ANCHOR_F10_ROUTE_A_PARALLEL_N8_C2V008.json` | `4978ba17fb05fb3fb096440d9a8a20e1d2d4d657d0b4b8f7007dc457d37c73eb` |
| `deciding/LAUNCH_DECIDING_I_C2V008.json` | `b32b7b63dac78542f5b6f630543541930813baa545af6c9732f8878a6dac0e18` |
| `deciding/LAUNCH_DECIDING_II_C2V008.json` | `3109111f81c289d3434e99aa7c59ebd5720f13c7fb1de2586ca8213e5901b3cb` |

## (a) Distance

### What is ported, and from where

From v003c `ed326130`; v003b is the same code:

- **Verbatim** (byte check `tests/runs/final/VERBATIM_CHECK_C2V008.json`, all true):
  - the 172-line block `geometry_active` .. `geometry_inputs` (v003c L717-888);
  - `GEOMETRY_PINS` and `PROFILE_NAME`;
  - the inclination refusal text;
  - the custody source-profile check.
- The annotation literal `'driver': 'galaxy_m0_forward_c2v003b'` in the per-call files is kept on purpose. With it, v008 writes the same per-call files as v003c.

### Wiring onto the v007 galaxy-config structure

Everything below is DDO154 only, and only when D != 4.04.

| Consumer | v003c | v008 |
|---|---|---|
| route A (reviewed or parallel worker) | prep module patch `C = <inputs>/geometry_C` | the same patch, merged into the one prep patch with the same key order |
| route-A custody | profile pin `ROUTE_A_GEOMETRY_MISMATCH` | the same; also applied at 4.04 (see the custody notes below) |
| reference | stage globals `PROFILE`, `PROFILE_SHA` | the same stage globals (the successor still has them), plus config `source.profile` and `radial.outer_edge_kpc` PER_CALL |
| body / offset / columns / rotations / feedback | reuse-module patch `PROFILE`, `PROFILE_SHA` | the same patch |
| body | global `SOURCE` | config `source.monotone_source` and `source.profile` PER_CALL (plus outer edge) |
| rotations v001/v005 | globals `SOURCE`, `SOURCE_SHA` | config `source.monotone_source` (plus outer edge) PER_CALL |
| column mean | `PINS[0]` = per-call binding | `custody.column_mean_input_pins[0]` and config `observation.binding` and `observation.query_rows` PER_CALL |
| admitted reference / body | `REFERENCE_GEOMETRY_MISMATCH` / `BODY_GEOMETRY_MISMATCH` | the same (DDO154) |

Notes on the per-call values:
- `radial.outer_edge_kpc` = `sqrt(last per-call s_edge)`. This is the expression the DDO154 literal check uses at 4.04, and at 4.04 it gives 14.102260356114186. At D it equals 14.102260356114186 × D/4.04, to 1e-14.
- Inclination stays registered-only.
- NGC3198: both NGC normalizers are unchanged and still refuse any distance other than 13.8 Mpc. This was tested on the route-B template and on the route-A seed spec. The NGC binding gives no distance support: the NGC radii and projection are baked into the profile and binding v001.
- The accepted DDO154 distance range is v003c's, i.e. any finite positive value. The calibration box [3.98107, 4.11150] is a spec-side choice and is not enforced by the driver.

### Why run mode blocks at D != 4.04

The probe is `geometry_admission_probe`. For each stage, it runs that stage's own admission (`galaxy_config()`) on two configs:
- the stage's config with the per-call geometry fields;
- a control copy at the registered geometry.

The rule it hits is the gal_c2v004 shared admission (`admit_config`):
- A DDO154 field is admitted only as `DDO154_EXACT_LITERAL`, which must equal the schema V004 ddo154 value, i.e. the 4.04 Mpc files.
- `PER_CALL` is admitted only on these kinds: `PER_CALL_CUSTODY`, `ROUTE_A_RUN_OUTCOME`, `STAGE_CODE_IDENTITY`, a call input (`source.coefficients`), or a declared input slot.

**Refused (TESTED-NEGATIVE, from stage bytes, at all 3 distances)**, every refusal naming exactly these fields:

| Stage | Refused fields |
|---|---|
| reference | `source.profile` (SHARED_SAME_VALUE), `radial.outer_edge_kpc` (GALAXY_DERIVED_SHAPE) |
| body | `source.profile`, `source.monotone_source` (GALAXY_SOURCE_RECONSTRUCTION), `radial.outer_edge_kpc` |
| offset | `source.profile`, `radial.outer_edge_kpc` |
| rotation_v001, rotation_v005 | `source.monotone_source`, `radial.outer_edge_kpc` |
| column_mean_v004 | `observation.binding`, `observation.query_rows` (OBSERVATION_BINDING) |

- All 6 registered-geometry controls are accepted.
- The literal values cannot simply be kept. `radial_truncation` requires `outer_edge_kpc` to equal one per-call edge, so a 4.04 literal refuses. The column mean would also observe the 4.04 query radii.

**What run mode does:** `refuse('geometry', 'GEOMETRY_NOT_ADMITTED_BY_STAGE_BINDING', …)` raises Blocked before route A.
- `result.json` carries `geometry`: the derivation record, the config fields and the probe.
- The per-call files and the probe files are kept in `inputs/`.
- Simulate mode records the refusal, and planning continues.

**Deciding fix (UNTESTED; another lane):** a gal_c2v005 stage set plus a schema V005 that admits these 5 DDO154 fields as PER_CALL when `physical.distance_Mpc` is a call input. A distance-varied call becomes runnable only once v008's `SCRIPTS`/`GC_SCHEMA` are re-pinned to those bytes. The driver side is complete and needs no other change: the probe then accepts, and the requests are the ones listed in G6.

### Custody notes

These change no request.

- **Profile pin at 4.04.** The `ROUTE_A_GEOMETRY_MISMATCH` check now also runs at 4.04, with the registered profile `f5becd45`, as in v003c. The seed does not depend on D, so without this check a route A prepared at another distance would be admitted into a 4.04 call. The saved V002 checkpoint and the A2F10 checkpoint pass; a different profile is Blocked (GC_*).
- **Admitted reference and body.** These are now checked against the registered profile and monotone source: the reference against `source_custody`, the body against `input_pins`. The deciding (i) spec 4ac5527a passes in dry run (exit 0, 17/17 stage inputs identical to the saved launches).

## (b) Comparator C1 fix

`compare_deciding_ii_c2v008.py` is v007's `aee8b7a6` with only these changes:
- `identity_check()`: for each side it requires `caller.sha256 == cm.digest(cm.decode(caller.record))`. Only then does it replace `caller.sha256` by `<CALLER_SHA>` and compare the identities after the Side substitutions. The decoded caller itself stays compared.
- The docstring and the schema name.
- The diff hunk list is in VERBATIM_CHECK.

**Real-caller fixtures** (`tests/test_comparator_c2v008.py`), on the A2F10 IDENTITY bytes:

| Fixture | v008 RA_IDENTITY | v007 rule |
|---|---|---|
| RC_correct_parallel_identity | PASS | FAIL, remaining exactly `identity.caller.sha256` (reproduces C1) |
| RC_stale_caller_sha256 | FAIL | **would PASS** (a false PASS that v007 also had) |
| RC_caller_numerical_control_changed | FAIL | — |

- The A2F10 reference `caller.sha256` equals the digest of its decoded caller.
- The synthetic fixtures now carry the real `digest(caller)`. Three mutations were added (`caller_sha_wrong`, `caller_sha_absent`, `caller_seed_other`), and each fails at RA_IDENTITY.
- Fixtures: 17/17 PASS. Self-test A2F10 vs A2F10: PASS_BITWISE_EQUAL, with `caller_sha256_is_digest_of_decoded_caller` true on both sides.

## (c) LE-pass and reference parallelism

Not changed. The facts below are pinned as text from the bytes by test `LE_code_facts_pinned`.

### Why the LE passes run serially when a bound is set

The cause is not a data dependence between columns. It is the consumer contract.

**What the driver does:**
- `serial = last or bound is not None` leads to `generated_runs(..., split=not serial)`, which makes one run of all 72 columns.
- A pass is observed only when `len(cols) == 1`.
- With a bound, every pass must be observed, because `max_abs_change_km_s` comes from the column-mean speeds. The last pass is always observed.

**Why the column mean forces one run:** `ddo12_lower_entropy_column_mean_root_v004_gal_c2v004.py` (`11d6f8b8`) requires all of:
- exactly 5 input pins: binding, rotation start, rotation finish, and ONE columns run's start and finish;
- `len(cf['completed']) == NC` (72) in that single run;
- `rs['producer_sha_inputs']['column-worker-sha256'] == cs['worker_sha256']`;
- the same entropy and field keys across rotation and columns.

**Columns within a pass are independent:**
- In `ddo_fixed_K_free_surface_root_v005_gal_c2v004.py` (`0fdf435a`), `for i in ids:` each column prepares its own lines at R_i and calls `solve_column`.
- It shares only read-only inputs (prepared field, base arrays, controls). A failure is isolated to its column.
- That independence is why fs/rfs can be split. Their consumers (rotation v001/v005, rfs → H) take a manifest of several runs.
- Unobserved LE passes are already split by `column_workers` today: with no bound, `observe_every_pass` false, and every pass except the last.

**Why `le_column_workers` was not added:**
- The fs mechanism (several stage processes, several runs) would produce more than one LE run per observed pass.
- The column mean v004 refuses that, so the option could never apply to the anchor profile.
- Adding it would therefore be dead code. No option was added, and the default behaviour is unchanged.

**What would enable it (UNTESTED, new reviewed bytes, outside this task).** Either:
1. A column-mean successor that accepts a manifest of column runs, checking `failures`, `completed`, worker and entropy/field per run. It already reads every column file through `rs['column_custody']`, so its rows would be bitwise equal by construction. Deciding test: A2F10 with LE split N=4, with the 12 speeds bitwise equal to A2_ANCHOR_F10_RUN_V001.
2. An in-stage pool successor of columns v005 that writes one 72-column run, like the parallel route-A solver.

**Size of the prize, from A2F10 `stage_records`:**
- LE columns: 742.0 + 677.9 + 702.5 = 2122 s of the 6724 s call.
- With N=4: about 1590 s saved (about 26 min).
- Route A (1619 s) is already covered by `route_a.column_workers`.

### Reference stage (947 s), report only

- **Radii are independent by code:** `for i,R in enumerate(radii): ref.evaluate_radius(...)`, and the module's `cache` is local to each `evaluate_radius` call.
- **Why it cannot be split today:** the stage writes ONE run, whose `finish.json` lists all radii, and body consumes `custody.reference_run` = {directory, start_sha256, finish_sha256}, which is a single run. Splitting therefore needs an in-stage pool successor of the reference stage, or a body successor that takes a manifest (new bytes).
- **Status:** UNTESTED. The deciding test would be reference radii bitwise equal and the body arrays equal.

## (d) CHECK D1

`route_a_attempt_link` runs inside `route_a_custody`, right after the IDENTITY self-hash and before any outcome verdict. It requires:
- `result.result.source_fixed_point.checkpoint.identity_sha256 == IDENTITY.identity_sha256`;
- an attempt token that names `attempts/<token>.end.json` (no `/`) whose record carries that identity.

Otherwise it raises `Refusal ROUTE_A_ATTEMPT_NOT_OF_THIS_CHECKPOINT`; an unreadable layout raises `StageFailed`.

- It applies to DDO154 only (admitted, computed, and simulate on saved bytes).
- NGC3198 is left as in v007, because NGC route-A result bytes may not be read in this lane, so the layout is UNTESTED on NGC.
  - Deciding test: the v007 M1 NGC dry run on real bytes; extending D1 to NGC needs it to show `checkpoint.attempt` present.

**Results:**
- The A2F10 attempt with the V002 checkpoint is Refused, and so is the reverse pairing. v007 admits the mismatched pairing.
- Matching pairs pass on both real runs.
- Run mode, unlinked or other-checkpoint attempt: `REFUSED`. The v007 baseline on the same input gives `ROUTE_A_NO_FIXED_POINT`, the mislabel D1 described.

## Hunk-by-hunk justification (`DIFF_V007_V008.diff`, 22 hunks)

| # | Hunk | Content | Part |
|---|---|---|---|
| 1 | `-1,4 +1,25` | docstring c2v008 section | doc |
| 2 | `-222,6 +243,20` | `GEOMETRY_PINS`, `PROFILE_NAME` (verbatim v003c), `GEOMETRY_CONFIG_FIELDS` | (a) |
| 3 | `-685,11 +720,19` | normalize: DDO154 distance accepted; inclination refusal verbatim v003c; explicit non-DDO distance refusal (unreachable) | (a) |
| 4 | `-880,6 +923,244` | verbatim geometry block; `geometry_config_fields`; `geometry_admission_probe` | (a) |
| 5 | `-946,6 +1227,7` | `Ctx.geometry` | (a) record |
| 6 | `-1104,7 +1386,29` | `route_a_attempt_link`; custody signature (+`profile_sha`, `attempt_result`) | (d), (a) |
| 7 | `-1113,13 +1417,23` | custody docstring; link call; profile check (verbatim v003c) | (d), (a) |
| 8 | `-1157,7 +1471,8` | custody returns `attempt_link`, `source_profile_sha256` | record |
| 9 | `-1773,6 +2088,7` | `gfields = {}` | (a) |
| 10 | `-1784,6 +2100,8` | per-call geometry fields to consumers only | (a) |
| 11 | `-1804,10 +2122,11` | `gen_request(stage_globals=None)` (empty → v007 `{}`) | (a) |
| 12 | `-1850,6 +2169,26` | geometry inputs, config fields, probe, run-mode gate | (a) |
| 13 | `-1877,9 +2216,13` | prep patch built as `prep_set` (+`C`) | (a) |
| 14 | `-1917,7 +2260,10` | custody call with `profile_sha`, `attempt_result` (DDO only) | (a), (d) |
| 15 | `-1933,12 +2279,19` | `route_a_rows_scope`; reuse/reference `PROFILE` globals (verbatim v003c) | (a) |
| 16 | `-1961,11 +2314,13` | admitted-reference geometry check; reference `stage_globals` | (a) |
| 17 | `-1974,6 +2329,8` | admitted-body geometry check | (a) |
| 18 | `-2183,6 +2540,8` | column-mean binding pin from the per-call binding | (a) |
| 19 | `-2359,6 +2718,9` | static pins + `GEOMETRY_PINS` when active | (a) |
| 20 | `-2519,6 +2881,8` | `result['geometry']` | (a) record |
| 21 | `-2641,7 +3005,8` | dry run: `repro_like` false at a per-call geometry (v003c) | (a) |
| 22 | `-2777,6 +3142,17` | dry-run summary and plan lines for geometry (only when active) | (a) |

## Tests

Run by `tests/run_all_c2v008.sh` into `tests/runs/final`:
- `nice -n 10`, single-thread BLAS, at most 4 processes;
- every script runs under `tests/guard_c2v008.py`, except the shim test (it spawns workers);
- the guard refuses process creation, writes outside the lane, CLAUDE2/runs except A2_ANCHOR_F10_RUN_V001, velocity-like paths, and any `result.json` under a KMAX_/D7R1/V005/V006/V007/DECIDING path; it now exits with the script's code (v007 L3);
- across 54 guard logs: 0 denials, and the only CLAUDE2/runs entry read is A2_ANCHOR_F10_RUN_V001.

| Suite | Result | Count |
|---|---|---|
| dry runs v003c / v007 / v008 (48 jobs: 41 exit 0, 7 expected refusals) + `compare_dry_c2v008.py` | `COMPARE_DRY_C2V008.json` | 54/54 PASS |
| v008 unit / run mode / capture (`test_c2v008.py`) | `unit/TEST_RESULTS.json` | 45/45 PASS |
| v007 suite on v008 (verbatim copy, 4 path literals) | `v7suite/TEST_RESULTS.json` | 50/56. The 6 failures are the intended (d) change, see below |
| v006 suite on v008 (verbatim copy) | `tests/runs/v006_suite_on_v008_20261017T190349Z` | 27/27 PASS |
| comparator fixtures (v007's 11 + 3 caller mutations + 3 real-caller) | `comparator/FIXTURE_RESULTS.json` | 17/17 PASS |
| comparator self-test A2F10 vs A2F10 | `SELFTEST_A2F10_VS_A2F10.json` | PASS_BITWISE_EQUAL (12 checks) |
| shim + spawn N = 1, 2, 3 | `shim/SHIM_RESULTS.json` | 5/5 PASS |
| verbatim byte check vs v003c | `VERBATIM_CHECK_C2V008.json` | all true |

**The 6 v007-suite failures:** `RUN_v007_{NFP_IDONLY, HIFAIL_IDONLY, NFP_SAVEDCKPT, CONV3_SAVEDCKPT, INCONSISTENT_SAVEDCKPT, F2_relative_outdir}` all end `REFUSED ROUTE_A_ATTEMPT_NOT_OF_THIS_CHECKPOINT`. Their synthetic attempts carry no attempt token, and the IDENTITY-only checkpoint has no `attempts/`. The same six cases with LINKED fixtures (`RUNL_*`) give exactly the v007 statuses.

### Results

**At D = 4.04, requests and inputs are byte-identical to v007: TESTED-POSITIVE.** This is D1, on 15 specs:
- the deciding (i) spec `4ac5527a`, ADMIT_ROUTE_A, ADMIT_PREFIX_C2V001, PINNED_FULL, RULE_FULL, A2F10, both NGC templates and the NGC route-A seed spec;
- the v007 deciding (ii) spec `038c4398`, A2F10_RA1/2/8/64 and ADMIT_ROUTE_A_RA1.

For every spec:
- every planned request is byte-identical after `<RD>` normalization, and so is every generated input;
- the normalized spec and the remaining refusals are identical;
- the identity record differs only by the two added custody keys.

Run-mode capture gives the same result: the first requests are byte-identical v007 vs v008 for A2F10 (route_a), the v007 and v008 deciding (ii) specs (parallel route_a), and 4ac5527a (offset). Inputs are identical (CAP_*).

**At D != 4.04, the changed inputs equal v003c's: TESTED-POSITIVE** at 3.98107, 4.1115 and 4.07:
- **G1:** the 4 per-call files (profile, source-binding copy, monotone source, column-mean binding) are byte-identical to v003c's after `<RD>`. The profile at 4.1115 is `177e2fd0`.
- **G2:** the route-A delta against 4.04 is identical in v003c and v008: only `module_patches[0].set.C`.
- **G3:** v003c's `PROFILE`/`PROFILE_SHA`/`SOURCE`/`SOURCE_SHA` values equal v008's stage globals, reuse patch and config fields. The per-call fields travel exactly to their consumers.
- **G4:** the outer edge and the query rows (radius ratio D/4.04).
- **G5:** the stage refusals listed above.
- **G6:** v008 at D vs v008 at 4.04 has no difference outside the geometry ones (route_a `C`; reference globals; `PROFILE` in the reuse patch of body/offset/columns/rotation/feedback; galaxy-config tokens and meta).
- **GD:** `derive_geometry` returns equal canonical JSON v008 vs v003c in-process.
- **G9:** inclination 64, NGC 14 Mpc, and an admitted 4.04 route A at 4.1115 (`ROUTE_A_GEOMETRY_MISMATCH`) are all refused or blocked. v007 refuses any distance.
- **One lineage difference, not introduced by v008:** the v003c and v008 seeds differ only in their annotation literal (`c2v003` vs `c2v006`), at every D.

**Run mode at D != 4.04 is BLOCKED before any stage: TESTED-POSITIVE** (RUNG_*, 4 specs incl. parallel and admitted):
- 0 stage records, no `stages/` directory;
- geometry files and probe files kept;
- all 6 stages refuse, and all 6 controls are accepted.

## Deciding tests for root (real runs)

The exact command arrays are in `deciding/LAUNCH_DECIDING_I_C2V008.json` and `deciding/LAUNCH_DECIDING_II_C2V008.json`. Every run uses the environment `OMP/OPENBLAS/MKL/NUMEXPR/VECLIB/BLIS_NUM_THREADS=1`.

### (i) ADMIT_PREFIX bitwise, spec 4ac5527a, under v008

```
/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py \
  --driver /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/driver_v008_c2/galaxy_m0_forward_c2v008.py \
  --driver-sha256 f8e4770106abb83df5e658e91edc5593198fe87f0600ee5d1946f22415902f28 \
  --spec /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_impl_c2/binding/specs/CALL_REPRO_PINNED_ADMIT_PREFIX_C2V005.json \
  --outdir "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/DDO154_ROUTE_B_C2V008_DECIDING_ADMIT_PREFIX_RUN_V001" \
  --receipt "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/DDO154_ROUTE_B_C2V008_DECIDING_ADMIT_PREFIX_RUN_V001.receipt.json" \
  --wall-cap-s 14400 --rss-cap-bytes 3221225472 --output-cap-bytes 8589934592 --poll-s 2.0
```

**PASS requires all of:**
- finish COMPLETED;
- `deciding_test.verdict` PASS_BITWISE_EQUAL;
- `route_a_outcome` CONVERGED at 4;
- custody iteration 4, solver `44d9c23c`, `attempt_link` {98816902…, 01792161909921426000-19994-831a3fbc}, `source_profile_sha256` f5becd45…;
- no `geometry` key.

### (ii) Full A2F10 anchor call, route_a.column_workers=8, fs/rfs column_workers=2, under v008

The spec is `4978ba17`: the content of `a93c95b9` plus `numerics.route_a.column_workers = 8`, with only the label changed.

```
/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py \
  --driver /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/driver_v008_c2/galaxy_m0_forward_c2v008.py \
  --driver-sha256 f8e4770106abb83df5e658e91edc5593198fe87f0600ee5d1946f22415902f28 \
  --spec /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/driver_v008_c2/deciding/CALL_A2_ANCHOR_F10_ROUTE_A_PARALLEL_N8_C2V008.json \
  --outdir "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008_DECIDING_RUN_V001" \
  --receipt "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008_DECIDING_RUN_V001.receipt.json" \
  --wall-cap-s 14400 --rss-cap-bytes 8589934592 --output-cap-bytes 8589934592 --poll-s 2.0
```

Then compare with the fixed comparator:

```
/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B \
  /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/driver_v008_c2/deciding/compare_deciding_ii_c2v008.py \
  --reference "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/A2_ANCHOR_F10_RUN_V001" \
  --new "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008_DECIDING_RUN_V001" \
  --column-workers 8 \
  --out "/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008_DECIDING_RUN_V001.COMPARE_DECIDING_II_C2V008.json"
```

**PASS requires** verdict PASS_BITWISE_EQUAL, with all 13 checks passing. The checks are as in v007; RA_IDENTITY now uses the C1 caller-digest rule.

**How to read the outcome:**
- RA_* pass but SPEEDS fails: the cause is route-B lineage (c2v001→c2v008), not the parallel route A.
- Any RA_* fails: TESTED-NEGATIVE for the option.

There is no (iii), because no LE option exists. If a v007 deciding (ii) run already exists, its compare must be re-run with the c2v008 comparator: the rule is driver-independent.

## Open items

- **UNTESTED:** a DDO154 distance call in run mode. It needs the stage/schema successor described in (a); the deciding test is A2F10 at 3.98107 / 4.1115 with the 12 rows produced.
- **UNTESTED:** D1 on NGC route-A bytes, as described in (d).
- **UNTESTED:** LE and reference parallel successors, as described in (c).
- **Rule note.** Superseded outputs of my own try runs stay in place under new names (`tests/runs/*_try*`, `smoke`, the first `v006_suite_on_v008_*` stamp). Nothing was moved or deleted. `tests/specs/` holds only the `c2v008/` subdirectory, because the empty `specs/` existed before the generator ran.
