# S1 — Codex3 step-5 readiness: filler, templates, dry plans (refute by default)

`date -u`: Sun Oct 18 20:32:09 UTC 2026. Reviewer: Claude3 lane, helper S1 (Claude lineage). The lead posts; S1 posts nowhere.
Scope: READINESS_REPORT_CX3V001.md (c7c72d54293a133df4211805534849d2fe42fadf2ed5286ff7f3f0426e4c2782) and task FROM_CODEX/0594 (19e874ecb927be6ead60e363648d5768b2c1b66d87782ae167e68f5e9d09bd90).
I read Codex3's 0618 carrier successor (FROM_CODEX3/0618 8939c004e4bea1728eed610e4d98b98dffbe4333be1433c539feb16159de60a7) only for the r007/r006 status it records. Carriers and evidence claims belong to the other helper.
No launches. No NGC target or observed velocities, C5H, runs_ext/UVT_* or /.vol were opened or stat-ed. Writes are only below S1_filler/, all exclusive-create; nothing was overwritten or deleted. All Python ran as `-I -B` with single-thread BLAS under `taskpolicy -b`, which was never refused.

## Verdict: PASS_WITH_FINDINGS. BLOCKING 0, SHOULD_FIX 4, NOTE 11

- The filler admits no value that is untraceable to its pinned inputs and no physical override.
- DDO geometry never reaches the NGC fields. Every accepted case has distance 13.8 Mpc and inclination 72 deg, including DDO distance at both box ends (G04, G05).
- Every filler write follows validation and uses exclusive create ('xb', mkdir exist_ok=False). Every receipt has launch_authorized false. v003 differs from v002 only in number().
- The templates meet 0594. The A and B interfaces normalize identically except for the label, so running both would duplicate the calculation.
- The 8 stored dry plans verify from bytes. One re-run reproduces 18 of 18 files with zero fence refusals.
- The findings concern parser robustness, the filler's protected-path guard, and a stale r006 branch after A93.

## Findings

**SF-1 (SHOULD_FIX, low). The typed refusal for oversized integers stops at Python's 4300-digit integer-parse limit.**
- Cases: a 5000-digit JSON integer in u (H02), in theta (H03) or in the handoff log_index (H04). json.loads raises a plain ValueError.
- A 100000-deep array (Z01, RecursionError) and a 0xff byte (Z02, UnicodeDecodeError) fail the same way.
- None of these is in main()'s except tuple (Refusal, OSError, KeyError, TypeError, JSONDecodeError). The in-process CLI exits with an uncaught traceback (H02, H04, Z01, Z02).
- Fail-closed: no output directory exists after any of these cases.
- Fix: in parse(), catch ValueError and RecursionError and raise Refusal.

**SF-2 (SHOULD_FIX). safe_path is a substring deny-list. It misses inode-addressed and differently named protected paths, so the filler went on to open() them.**
- Paths opened: /.vol/16777220/2 (X03); /.resolve/16777220/2 (X08); .../NGC_3198/observed_velocities.json (X04); .../SPARC/MassModels_Lelli2016c.mrt (X05); .../NGC3198_target_free/vobs.dat (X10); .../sparc/Rotmod_LTG/DDO154_rotmod.dat (X11).
- Each open was refused by the S1 fence. The paths were nonexistent fixtures, so nothing was read.
- load_pin reads all the bytes before it compares digests, so a wrong sha256 in the pin does not prevent the read.
- Exploiting this needs a root-approved handoff that names such a path. No delivered input names one, and no tool hardcodes one.
- Fix: refuse /.vol, /.resolve and /.nofollow. Prefer an allow-list of approved roots for the handoff-supplied pins (export, V007 adoption, r007 acceptance, certificates).

**SF-3 (SHOULD_FIX, low). The guard stats a protected path before it refuses it.**
- safe_path builds `(p, p.resolve())` before it checks p. In Python 3.12, resolve() lstat()s every component and then stat()s the result.
- The S1 fence refused 2–3 metadata accesses per case in X01, X02, X06, X07, X09, W11 and W14. Each case still ended in the correct typed refusal.
- Codex3's own tests do the same: the redirected port logged 5, on /Volumes/External1/prohibited/runs_ext/UVT_NEVER_OPEN/result.json and /Users/bgm/NGC3198_observed_velocities.json.
- Only metadata is touched, never content.
- Fix: check p lexically first, resolve only if that passes, then check the resolved path.

**SF-4 (SHOULD_FIX). The driver branch is stale after A93.**
- 0618 records A93: r007 is accepted, the r006 registry is retired (REGISTRY_CX3V001.json r006_fallback_status RETIRED_BY_A93), and the carrier policy accepts only r007.
- The selected filler is still locked to POLICY 4f0d7d03, which lists r006_fallback.
- HANDOFF_CONTRACT_CX3V002 still says to use r006_fallback until acceptance, and HANDOFF_SHAPE_UNFILLED_CX3V001 defaults driver_branch to r006_fallback.
- In production, r006_fallback with a null acceptance pin is accepted, and the receipt binds driver c2930e18 and registry 3c42ca07 (R02, S07).
- Physics is unaffected: the specs are driver-independent (normalized specs identical across drivers). The risk is a receipt bound to a retired driver.
- Fix: a successor policy and filler that admit only r007 with its acceptance pin, plus an updated contract and shape, or an explicit root rule.

**NOTEs**
- N-1. Traceability is to the pinned export, not to the native step-4 record.
  - A theta within rel_tol 1e-12 of its u-image is accepted, and the theta, not the u-image, is written: gamma_over_Eref x(1+5e-13) is accepted (U03); x(1+2e-12) is refused (U04).
  - A self-consistent extra point in the export is accepted when selected (E02).
  - Nearly equal u entries can be swapped inside the tolerance (P02). Permutations of distinct u entries are refused (S01–S04).
  - This is by design and disclosed: root keeps custody of the native record.
- N-2. The production fence is a label check.
  - Relabelled synthetic content passes once its digest is supplied (R02, R03, S07).
  - The V007 adoption, r007 acceptance and certificate pins accept arbitrary bytes; they are byte-pinned and never parsed (R02, R03, R08). An arbitrary certificate pin is copied into numerics.uv_tail (R08).
  - Disclosed. Root preflight must check the content.
- N-3. The receipt does not echo v007_adoption_pin, driver_acceptance_pin or root_admission. They are reachable only through the handoff pin (S07).
- N-4. No type normalization. An integer exactly equal to the fixed Eref trial value is accepted and emitted as a 59-digit JSON integer in physical.Eref_J (H08). The driver's _num() casts it to float, so physics is unaffected, but the same point yields different spec bytes.
- N-5. -0.0 is accepted in u (N05) and for the fixed 0.0-trial native_theta (N06). Neither value is written into any spec, so this is harmless.
- N-6. No output confinement.
  - '..' paths (W05) and symlinked parents (W07) are followed.
  - Two escape probes into the scratchpad ('..' in W06; a symlinked parent in W08) reached mkdir and were blocked only by the S1 fence.
  - No confinement is claimed. Writes stayed after validation and exclusive.
- N-7. load_pin reads the whole file before the digest check, with no size cap and no regular-file check. A FIFO or /dev/zero pin would hang. Static finding only; not executed.
- N-8. The filler parses the driver registry but never consults it. S1 verified that all four template source specs are registered K32 cases in both cd30429c and 3c42ca07.
- N-9. The physical mapping always takes entropy_K_factor from theta (fixed at 64/121). An ORIGINAL_K (K=1.0) template under this mapping would be silently overwritten. Not reachable under the locked policy; a successor must not reuse the mapping for ORIGINAL_K.
- N-10. Codex3's tools/test_filler_cx3v002.py writes into Codex3's tree: it creates synthetic/negative_fixtures_v002, writes FILLER_TESTS_CX3V002.json, and fills into synthetic/must_not_exist_after_refusal. S1 did NOT run it. A redirected port (check logic unchanged, the four write sites moved into S1) passed 55/55.
- N-11. Codex3's review-harness fences (review/bounded_custody_review_cx3v00*.py) omit 'target' from the NGC word list, and they resolve before refusing. Harness only.

## Item 1: filler claims (fill_step5_cx3v003.py 2348974f469ff2d9177a1f3be88296180bb7c614dad7e820438991abac3ddd6c; contract V002 6ae6a0fc, registry V002 85b1e66a, policy 4f0d7d03, selected outputs 77d09781; all verified from bytes)

| Claim | S1 verdict | Evidence |
|---|---|---|
| Refuses any value not traceable to step 4's admitted-point record | HOLDS for the pinned export, not the native record (N-1) | U01, U02, U04-U08, M01, M02, L01-L07, E03, E04 refused; U03, E02, P02 accepted by design |
| No free physical overrides | HOLDS | O01-O05, O08, U08, G06, G07 refused; no CLI flags; POLICY_SHA hard-coded; certificate pins are numerics, byte-pinned (N-2) |
| DDO distance never becomes NGC distance (13.8 Mpc / 72 deg) | HOLDS | code lines 171-177; G01-G03, G06-G08 refused; G04/G05 and every ACCEPT case give 13.8/72 |
| gamma = gamma_over_Eref*Eref_base_J; 29 coordinates and 4 varying u verified | HOLDS | exact float product checked in every ACCEPT case; L03/L04 (28/30 names), L01/L02/L05 (u length), fixed/bounds/mismatch cases |
| Production/default mode refuses the synthetic fixtures | HOLDS for the fixtures as files; label-level only (N-2) | B02, R01, R09 refused; R02, R03, S07 relabelled content accepted |
| All validation precedes output-directory creation; all writes exclusive | HOLDS | 0 output dirs after any refusal; all filler opens 'xb'; mkdir exist_ok=False; W01-W04, W12, W13 |
| Receipt launch_authorized always false | HOLDS | constant; false on disk in every ACCEPT receipt |
| Oversized integer gets a typed refusal | PARTIAL: up to 4300 digits only (SF-1) | H01 typed; H02, H03, H04 untyped ValueError |
| v003 differs from v002 only in number() | HOLDS | `diff`: lines 81-87 only |
| Byte identity of the 4 specs | HOLDS | B01: S1 output equals synthetic/filled_v001 byte for byte |

## Adversarial cases (main run 124: 104 PASS / 20 FAIL; supplement 8/8 PASS)
Fixtures are copies of synthetic/SYNTHETIC_HANDOFF_CX3V001.json (95fa742f...) and SYNTHETIC_EXPORT_CX3V001.json (8969a189...).
- Expected = what the report and contract claims imply. 'TYPED' means main() would turn the error into an exit-2 REFUSED.
- fence# = refusals by the S1 fence during the case.
- 'FENCE_BLOCK' means the filler itself did not refuse, and the S1 fence stopped the OS call.
- All protected-looking paths are nonexistent fixtures.
- Of the 20 FAILs: 16 map to SF-1, SF-2 or SF-3; 4 are NOTE-level (H08 N-4, P02 N-1, W06 and W08 N-6).

| id | case | expected | observed | result | fence# | finding |
|---|---|---|---|---|---|---|
| B01 | Codex3 synthetic handoff, --synthetic-dry-only: exact byte identity with Codex3  | ACCEPT  | ACCEPT SYNTHETIC_DRY_ONLY | PASS | 0 |  |
| B02 | Codex3 synthetic handoff in production/default mode | REFUSAL MODE_FENCE | REFUSAL MODE_FENCE | PASS | 0 |  |
| U01 | varying theta common_scale_s off its u by 1e-9 rel | REFUSAL U_THETA_MISMATCH_common_scale_s | REFUSAL U_THETA_MISMATCH_common_scale_s | PASS | 0 |  |
| U02 | u[1] (gamma_over_Eref) changed, theta kept | REFUSAL U_THETA_MISMATCH_gamma_over_Eref | REFUSAL U_THETA_MISMATCH_gamma_over_Eref | PASS | 0 |  |
| U03 | theta gamma_over_Eref off its u by 5e-13 rel (inside rel_tol 1e-12): theta, not  | ACCEPT  | ACCEPT SYNTHETIC_DRY_ONLY | PASS | 0 |  |
| U04 | theta gamma_over_Eref off by 2e-12 rel (just outside tolerance) | REFUSAL U_THETA_MISMATCH_gamma_over_Eref | REFUSAL U_THETA_MISMATCH_gamma_over_Eref | PASS | 0 |  |
| U05 | fixed Eref_base_J moved by 1 ulp | REFUSAL FIXED_THETA_CHANGED_Eref_base_J | REFUSAL FIXED_THETA_CHANGED_Eref_base_J | PASS | 0 |  |
| U06 | fixed entropy_K_factor set to ORIGINAL_K 1.0 (in box) | REFUSAL FIXED_THETA_CHANGED_entropy_K_factor | REFUSAL FIXED_THETA_CHANGED_entropy_K_factor | PASS | 0 |  |
| U07 | fixed ML_3p6 set to 0.6 (in box) | REFUSAL FIXED_THETA_CHANGED_ML_3p6 | REFUSAL FIXED_THETA_CHANGED_ML_3p6 | PASS | 0 |  |
| U08 | handoff carries a gamma value | REFUSAL EXACT_FIELDS_HANDOFF | REFUSAL EXACT_FIELDS_HANDOFF | PASS | 0 |  |
| G01 | DDO theta distance_Mpc set to the NGC 13.8 | REFUSAL THETA_BOUNDS_distance_Mpc | REFUSAL THETA_BOUNDS_distance_Mpc | PASS | 0 |  |
| G02 | extra theta key ngc3198_distance_Mpc=4.04 (DDO value) | REFUSAL EXACT_ENGINE_COORDINATES | REFUSAL EXACT_ENGINE_COORDINATES | PASS | 0 |  |
| G03 | extra theta key inclination_deg=66 (DDO inclination) | REFUSAL EXACT_ENGINE_COORDINATES | REFUSAL EXACT_ENGINE_COORDINATES | PASS | 0 |  |
| G04 | admitted DDO distance at box low end (u[3]=0): NGC distance must stay 13.8 | ACCEPT  | ACCEPT SYNTHETIC_DRY_ONLY | PASS | 0 |  |
| G05 | admitted DDO distance at box high end (u[3]=1): NGC distance must stay 13.8 | ACCEPT  | ACCEPT SYNTHETIC_DRY_ONLY | PASS | 0 |  |
| G06 | handoff carries distance/inclination | REFUSAL EXACT_FIELDS_HANDOFF | REFUSAL EXACT_FIELDS_HANDOFF | PASS | 0 |  |
| G07 | export carries an NGC slot override | REFUSAL EXACT_FIELDS_EXPORT | REFUSAL EXACT_FIELDS_EXPORT | PASS | 0 |  |
| G08 | export coordinate_pin -> byte-identical copy at another path | REFUSAL EXPORT_COORDINATE_BINDING | REFUSAL EXPORT_COORDINATE_BINDING | PASS | 0 |  |
| O01 | handoff physical_overrides | REFUSAL EXACT_FIELDS_HANDOFF | REFUSAL EXACT_FIELDS_HANDOFF | PASS | 0 |  |
| O02 | handoff numerics override (DDO M_s128) | REFUSAL EXACT_FIELDS_HANDOFF | REFUSAL EXACT_FIELDS_HANDOFF | PASS | 0 |  |
| O03 | export point carries physical block | REFUSAL EXACT_FIELDS_POINT | REFUSAL EXACT_FIELDS_POINT | PASS | 0 |  |
| O04 | certificate_pins carries gamma | REFUSAL EXACT_FIELDS_CERTIFICATES | REFUSAL EXACT_FIELDS_CERTIFICATES | PASS | 0 |  |
| O05 | modified policy copy pinned by its own true sha | REFUSAL POLICY_NOT_REGISTERED | REFUSAL POLICY_NOT_REGISTERED | PASS | 0 |  |
| O06 | byte-identical policy copy at another path (content pin, path free) | ACCEPT  | ACCEPT SYNTHETIC_DRY_ONLY | PASS | 0 |  |
| O07 | production: library TEST_ONLY certificate sentinel injected | REFUSAL EXACT_FIELDS_eps_certificate_PIN | REFUSAL EXACT_FIELDS_eps_certificate_PIN | PASS | 0 |  |
| O08 | production: certificate pin with an extra override field | REFUSAL EXACT_FIELDS_lo_certificate_PIN | REFUSAL EXACT_FIELDS_lo_certificate_PIN | PASS | 0 |  |
| K01 | handoff duplicate top-level key mode | REFUSAL DUPLICATE_JSON_KEY_mode | REFUSAL DUPLICATE_JSON_KEY_mode | PASS | 0 |  |
| K02 | export duplicate theta key gamma_over_Eref | REFUSAL DUPLICATE_JSON_KEY_gamma_over_Eref | REFUSAL DUPLICATE_JSON_KEY_gamma_over_Eref | PASS | 0 |  |
| K03 | handoff duplicate via JSON escape \u006dode | REFUSAL DUPLICATE_JSON_KEY_mode | REFUSAL DUPLICATE_JSON_KEY_mode | PASS | 0 |  |
| K04 | nested duplicate in certificate_pins (same value) | REFUSAL DUPLICATE_JSON_KEY_lo_certificate | REFUSAL DUPLICATE_JSON_KEY_lo_certificate | PASS | 0 |  |
| N01 | theta NaN literal | REFUSAL NONFINITE_JSON_NaN | REFUSAL NONFINITE_JSON_NaN | PASS | 0 |  |
| N02 | u Infinity literal | REFUSAL NONFINITE_JSON_Infinity | REFUSAL NONFINITE_JSON_Infinity | PASS | 0 |  |
| N03 | u -Infinity literal | REFUSAL NONFINITE_JSON_-Infinity | REFUSAL NONFINITE_JSON_-Infinity | PASS | 0 |  |
| N04 | theta 1e999 (parses to inf) | REFUSAL FINITE_REAL_common_scale_s | REFUSAL FINITE_REAL_common_scale_s | PASS | 0 |  |
| N05 | u[0] = -0.0 with consistent theta (u is never written into a spec) | ACCEPT  | ACCEPT SYNTHETIC_DRY_ONLY | PASS | 0 |  |
| N06 | fixed native_theta = -0.0 vs trial 0.0 (== compares equal; not a driver input) | ACCEPT  | ACCEPT SYNTHETIC_DRY_ONLY | PASS | 0 |  |
| N07 | theta common_scale_s = -0.0 (positive box) | REFUSAL THETA_BOUNDS_common_scale_s | REFUSAL THETA_BOUNDS_common_scale_s | PASS | 0 |  |
| N08 | theta gamma_over_Eref 1e-400 (underflows to 0.0) | REFUSAL THETA_BOUNDS_gamma_over_Eref | REFUSAL THETA_BOUNDS_gamma_over_Eref | PASS | 0 |  |
| T01 | u[0] true | REFUSAL FINITE_REAL_U | REFUSAL FINITE_REAL_U | PASS | 0 |  |
| T02 | theta Eref_base_J true | REFUSAL FINITE_REAL_Eref_base_J | REFUSAL FINITE_REAL_Eref_base_J | PASS | 0 |  |
| T03 | handoff log_index true | REFUSAL POINT_SELECTION_INTEGER | REFUSAL POINT_SELECTION_INTEGER | PASS | 0 |  |
| T04 | export log_index false | REFUSAL UNIQUE_NONNEGATIVE_LOG_INDEX | REFUSAL UNIQUE_NONNEGATIVE_LOG_INDEX | PASS | 0 |  |
| T05 | export target_free 1 (not true) | REFUSAL EXPORT_TARGET_FREE_MODE | REFUSAL EXPORT_TARGET_FREE_MODE | PASS | 0 |  |
| T06 | fixed native_beta true (==1.0 trial) | REFUSAL FINITE_REAL_native_beta | REFUSAL FINITE_REAL_native_beta | PASS | 0 |  |
| H01 | u[0] = 10**400 (401-digit JSON integer) | REFUSAL FINITE_REAL_U | REFUSAL FINITE_REAL_U | PASS | 0 |  |
| H02 | u[0] = 5000-digit JSON integer (above int_max_str_digits=4300) | REFUSAL FINITE_REAL_U | EXCEPTION_ValueError Exceeds the limit (4300 digits) for integer string conversion: value h | FAIL | 0 | SF-1 |
| H03 | theta common_scale_s = 5000-digit JSON integer | REFUSAL FINITE_REAL_common_scale_s | EXCEPTION_ValueError Exceeds the limit (4300 digits) for integer string conversion: value h | FAIL | 0 | SF-1 |
| H04 | handoff log_index = 5000-digit JSON integer | REFUSAL POINT_ | EXCEPTION_ValueError Exceeds the limit (4300 digits) for integer string conversion: value h | FAIL | 0 | SF-1 |
| H05 | theta number as a JSON string | REFUSAL FINITE_REAL_common_scale_s | REFUSAL FINITE_REAL_common_scale_s | PASS | 0 |  |
| H06 | u number as a JSON string | REFUSAL FINITE_REAL_U | REFUSAL FINITE_REAL_U | PASS | 0 |  |
| H07 | theta written as an over-long decimal of the same double (lexical-form independe | ACCEPT  | ACCEPT SYNTHETIC_DRY_ONLY | PASS | 0 |  |
| H08 | fixed Eref_base_J as the exactly-equal 59-digit JSON integer: value equal, type/ | ACCEPT  | ACCEPT SYNTHETIC_DRY_ONLY | FAIL | 0 | N-4 |
| H09 | log_index 10**30 in export and handoff (valid integer id) | ACCEPT  | ACCEPT SYNTHETIC_DRY_ONLY | PASS | 0 |  |
| L01 | u with 3 entries | REFUSAL VARYING_U_LENGTH | REFUSAL VARYING_U_LENGTH | PASS | 0 |  |
| L02 | u with 5 entries | REFUSAL VARYING_U_LENGTH | REFUSAL VARYING_U_LENGTH | PASS | 0 |  |
| L03 | theta with 28 coordinates | REFUSAL EXACT_ENGINE_COORDINATES | REFUSAL EXACT_ENGINE_COORDINATES | PASS | 0 |  |
| L04 | theta with 30 coordinates | REFUSAL EXACT_ENGINE_COORDINATES | REFUSAL EXACT_ENGINE_COORDINATES | PASS | 0 |  |
| L05 | u as an object | REFUSAL VARYING_U_LENGTH | REFUSAL VARYING_U_LENGTH | PASS | 0 |  |
| L06 | theta as a list | REFUSAL EXACT_ENGINE_COORDINATES | REFUSAL EXACT_ENGINE_COORDINATES | PASS | 0 |  |
| L07 | admitted_points as an object | REFUSAL NONEMPTY_ADMITTED_POINTS | REFUSAL NONEMPTY_ADMITTED_POINTS | PASS | 0 |  |
| P01 | u reversed | REFUSAL U_THETA_MISMATCH_common_scale_s | REFUSAL U_THETA_MISMATCH_common_scale_s | PASS | 0 |  |
| P02 | u[0]<->u[1] | REFUSAL U_THETA_MISMATCH_common_scale_s | ACCEPT SYNTHETIC_DRY_ONLY | FAIL | 0 | N-1 |
| P03 | u[2]<->u[3] (ell_F_m <-> DDO distance) | REFUSAL U_THETA_MISMATCH_ell_F_m | REFUSAL U_THETA_MISMATCH_ell_F_m | PASS | 0 |  |
| P04 | u and theta of common_scale_s/gamma swapped together | REFUSAL THETA_BOUNDS_ | REFUSAL THETA_BOUNDS_common_scale_s | PASS | 0 |  |
| P05 | theta object keys in reverse order (unsorted bytes) | ACCEPT  | ACCEPT SYNTHETIC_DRY_ONLY | PASS | 0 |  |
| M01 | ell_F_m theta computed with a linear (not log) map | REFUSAL U_THETA_MISMATCH_ell_F_m | REFUSAL U_THETA_MISMATCH_ell_F_m | PASS | 0 |  |
| M02 | DDO distance theta changed inside its box, u kept | REFUSAL U_THETA_MISMATCH_distance_Mpc | REFUSAL U_THETA_MISMATCH_distance_Mpc | PASS | 0 |  |
| E01 | extra valid point (log_index 1), handoff selects 0 | ACCEPT  | ACCEPT SYNTHETIC_DRY_ONLY | PASS | 0 |  |
| E02 | extra self-consistent point selected (indistinguishable from step 4 without the  | ACCEPT  | ACCEPT SYNTHETIC_DRY_ONLY | PASS | 0 |  |
| E03 | extra INVALID point while selecting the valid one | REFUSAL THETA_BOUNDS_common_scale_s | REFUSAL THETA_BOUNDS_common_scale_s | PASS | 0 |  |
| E04 | extra point reusing log_index 0 | REFUSAL UNIQUE_NONNEGATIVE_LOG_INDEX | REFUSAL UNIQUE_NONNEGATIVE_LOG_INDEX | PASS | 0 |  |
| D01 | expected sha of a different file | REFUSAL BYTE_PIN_HANDOFF | REFUSAL BYTE_PIN_HANDOFF | PASS | 0 |  |
| D02 | correct digest in UPPER-case hex | REFUSAL HEX_SHA_HANDOFF | REFUSAL HEX_SHA_HANDOFF | PASS | 0 |  |
| D03 | correct digest with trailing newline | REFUSAL HEX_SHA_HANDOFF | REFUSAL HEX_SHA_HANDOFF | PASS | 0 |  |
| D04 | digest truncated to 63 hex | REFUSAL HEX_SHA_HANDOFF | REFUSAL HEX_SHA_HANDOFF | PASS | 0 |  |
| D05 | export pin sha does not match export bytes | REFUSAL BYTE_PIN_EXPORT | REFUSAL BYTE_PIN_EXPORT | PASS | 0 |  |
| D06 | relative handoff path | REFUSAL ABSOLUTE_PATH_REQUIRED | REFUSAL ABSOLUTE_PATH_REQUIRED | PASS | 0 |  |
| C01 | handoff key mode with Cyrillic o | REFUSAL EXACT_FIELDS_HANDOFF | REFUSAL EXACT_FIELDS_HANDOFF | PASS | 0 |  |
| C02 | theta key gamma_over_Eref with Cyrillic e | REFUSAL EXACT_ENGINE_COORDINATES | REFUSAL EXACT_ENGINE_COORDINATES | PASS | 0 |  |
| C03 | mode value with Cyrillic O | REFUSAL MODE_FENCE | REFUSAL MODE_FENCE | PASS | 0 |  |
| C04 | schema with zero-width space | REFUSAL HANDOFF_SCHEMA | REFUSAL HANDOFF_SCHEMA | PASS | 0 |  |
| C05 | driver_branch with zero-width space | REFUSAL UNREGISTERED_DRIVER_BRANCH | REFUSAL UNREGISTERED_DRIVER_BRANCH | PASS | 0 |  |
| C06 | pending sentinel with Cyrillic E (synthetic) | REFUSAL SYNTHETIC_CERTIFICATE_PROMOTION_REFUSED | REFUSAL SYNTHETIC_CERTIFICATE_PROMOTION_REFUSED | PASS | 0 |  |
| C07 | log_index written with a fullwidth digit | TYPED  | EXCEPTION_JSONDecodeError Expecting value: line 8 column 16 (char 221) | PASS | 0 |  |
| C08 | export key admitted_points with Cyrillic dze | REFUSAL EXACT_FIELDS_EXPORT | REFUSAL EXACT_FIELDS_EXPORT | PASS | 0 |  |
| W01 | pre-existing empty output directory | REFUSAL OUTPUT_DIRECTORY_EXISTS | REFUSAL OUTPUT_DIRECTORY_EXISTS | PASS | 0 |  |
| W02 | pre-existing output directory with a file | REFUSAL OUTPUT_DIRECTORY_EXISTS | REFUSAL OUTPUT_DIRECTORY_EXISTS | PASS | 0 |  |
| W03 | output path is a symlink to an existing directory | REFUSAL OUTPUT_DIRECTORY_EXISTS | REFUSAL OUTPUT_DIRECTORY_EXISTS | PASS | 0 |  |
| W04 | output path is a dangling symlink (target inside S1) | TYPED  | EXCEPTION_FileExistsError [Errno 17] File exists: '/Users/bgm/Research/UNT_EXCHANGE/claude_artif | PASS | 0 |  |
| W05 | output path through '..' that normalises inside S1 | ACCEPT  | ACCEPT SYNTHETIC_DRY_ONLY | PASS | 0 |  |
| W07 | symlinked parent directory (inside S1): files land in the link target | ACCEPT  | ACCEPT SYNTHETIC_DRY_ONLY | PASS | 0 |  |
| W08 | symlinked parent pointing OUTSIDE S1 (scratchpad): no confinement in the filler; | TYPED  | FENCE_BLOCK [Errno 13] S1_FENCE_REFUSED_WRITE_OUTSIDE_S1: '/Users/bgm/Research/UNT | FAIL | 1 | N-6 |
| W06 | '..' path escaping S1 into the scratchpad: no confinement in the filler; S1 fenc | TYPED  | FENCE_BLOCK [Errno 13] S1_FENCE_REFUSED_WRITE_OUTSIDE_S1: '/Users/bgm/Research/UNT | FAIL | 1 | N-6 |
| W09 | relative output path | REFUSAL ABSOLUTE_PATH_REQUIRED | REFUSAL ABSOLUTE_PATH_REQUIRED | PASS | 0 |  |
| W10 | output parent missing | REFUSAL OUTPUT_PARENT_REQUIRED | REFUSAL OUTPUT_PARENT_REQUIRED | PASS | 0 |  |
| W11 | output under an NGC-target-looking name | REFUSAL NGC_TARGET_PATH | REFUSAL NGC_TARGET_PATH | PASS | 2 |  |
| W12 | output path is an existing regular file | REFUSAL OUTPUT_DIRECTORY_EXISTS | REFUSAL OUTPUT_DIRECTORY_EXISTS | PASS | 0 |  |
| W13 | validation failure (bad digest) must create no output directory | REFUSAL BYTE_PIN_HANDOFF | REFUSAL BYTE_PIN_HANDOFF | PASS | 0 |  |
| W14 | output under a runs_ext/UVT_ name | REFUSAL PROTECTED_RUN_PATH | REFUSAL PROTECTED_RUN_PATH | PASS | 2 |  |
| R01 | handoff relabelled ADMITTED, export still SYNTHETIC | REFUSAL EXPORT_TARGET_FREE_MODE | REFUSAL EXPORT_TARGET_FREE_MODE | PASS | 0 |  |
| R02 | relabelled synthetic content + arbitrary bytes as V007 adoption, r006_fallback:  | ACCEPT  | ACCEPT POINT_BOUND_REQUIRES_CLAUDE2_PREFLIGHT | PASS | 0 |  |
| R03 | relabelled synthetic + arbitrary bytes as r007 acceptance | ACCEPT  | ACCEPT POINT_BOUND_REQUIRES_CLAUDE2_PREFLIGHT | PASS | 0 |  |
| R04 | r006_fallback with a non-null acceptance pin | REFUSAL FALLBACK_ACCEPTANCE_FIELD_MUST_BE_NULL | REFUSAL FALLBACK_ACCEPTANCE_FIELD_MUST_BE_NULL | PASS | 0 |  |
| R05 | production without a V007 adoption pin | REFUSAL EXACT_FIELDS_V007_ADOPTION_PIN | REFUSAL EXACT_FIELDS_V007_ADOPTION_PIN | PASS | 0 |  |
| R06 | production with root_admission SYNTHETIC_DRY_ONLY | REFUSAL ROOT_STEP4_ADMISSION_REQUIRED | REFUSAL ROOT_STEP4_ADMISSION_REQUIRED | PASS | 0 |  |
| R07 | r007 without an acceptance pin | REFUSAL EXACT_FIELDS_R007_ACCEPTANCE_PIN | REFUSAL EXACT_FIELDS_R007_ACCEPTANCE_PIN | PASS | 0 |  |
| R08 | production: arbitrary bytes accepted as the EPS certificate (content unchecked;  | ACCEPT  | ACCEPT POINT_BOUND_REQUIRES_CLAUDE2_PREFLIGHT | PASS | 0 |  |
| R09 | ADMITTED-labelled handoff run with --synthetic-dry-only | REFUSAL MODE_FENCE | REFUSAL MODE_FENCE | PASS | 0 |  |
| R10 | synthetic flag passed as int 1 via the API | REFUSAL SYNTHETIC_FLAG_BOOL | REFUSAL SYNTHETIC_FLAG_BOOL | PASS | 0 |  |
| X01 | export pin under runs_ext/UVT_*: refuse with NO protected stat/open | REFUSAL PROTECTED_RUN_PATH | REFUSAL PROTECTED_RUN_PATH | FAIL | 3 | SF-3 |
| X02 | export pin naming NGC3198 observed velocities: refuse with NO protected stat/ope | REFUSAL NGC_TARGET_PATH | REFUSAL NGC_TARGET_PATH | FAIL | 2 | SF-3 |
| X03 | /.vol inode path as export pin: filler should refuse before open | REFUSAL  | FENCE_BLOCK [Errno 13] S1_FENCE_REFUSED_VOLFS_INODE_PATH: '/.vol/16777220/2' | FAIL | 5 | SF-2 |
| X04 | production cert pin, NGC name variant NGC_3198 + observed | REFUSAL  | FENCE_BLOCK [Errno 13] S1_FENCE_REFUSED_NGC_OBSERVED_OR_TARGET: '/nonexistent_s1/N | FAIL | 3 | SF-2 |
| X05 | production cert pin, SPARC all-galaxy mass-model table | REFUSAL  | FENCE_BLOCK [Errno 13] S1_FENCE_REFUSED_SPARC_ROTATION_DATA: '/nonexistent_s1/SPAR | FAIL | 3 | SF-2 |
| X06 | innocent-looking symlink in S1 pointing into runs_ext/UVT_* | REFUSAL PROTECTED_RUN_PATH | REFUSAL PROTECTED_RUN_PATH | FAIL | 3 | SF-3 |
| X07 | production V007 pin inside the C5H run | REFUSAL PROTECTED_RUN_PATH | REFUSAL PROTECTED_RUN_PATH | FAIL | 3 | SF-3 |
| X08 | production cert pin via /.resolve inode path | REFUSAL  | FENCE_BLOCK [Errno 13] S1_FENCE_REFUSED_VOLFS_INODE_PATH: '/.resolve/16777220/2' | FAIL | 5 | SF-2 |
| X09 | mixed-case NGC3198 + Velocity | REFUSAL NGC_TARGET_PATH | REFUSAL NGC_TARGET_PATH | FAIL | 2 | SF-3 |
| X10 | NGC3198 'target_free' directory holding vobs.dat (deny-list words miss 'vobs') | REFUSAL  | FENCE_BLOCK [Errno 13] S1_FENCE_REFUSED_NGC_OBSERVED_OR_TARGET: '/nonexistent_s1/N | FAIL | 3 | SF-2 |
| X11 | SPARC rotmod file of another galaxy (DDO154 observed rotation) | REFUSAL  | FENCE_BLOCK [Errno 13] S1_FENCE_REFUSED_SPARC_ROTATION_DATA: '/nonexistent_s1/spar | FAIL | 4 | SF-2 |
| Z01 | deeply nested JSON array (100000 levels) inside the export | TYPED  | EXCEPTION_RecursionError maximum recursion depth exceeded while decoding a JSON array from a un | FAIL | 0 | SF-1 |
| Z02 | invalid UTF-8 byte inside the export | TYPED  | EXCEPTION_UnicodeDecodeError 'utf-8' codec can't decode byte 0xff in position 1423: invalid start b | FAIL | 0 | SF-1 |
| Z03 | handoff is a JSON array | REFUSAL EXACT_FIELDS_HANDOFF | REFUSAL EXACT_FIELDS_HANDOFF | PASS | 0 |  |
| Z04 | empty handoff file | TYPED  | EXCEPTION_JSONDecodeError Expecting value: line 1 column 1 (char 0) | PASS | 0 |  |
| S00 | distinct-u consistent point (control) | ACCEPT SYNTHETIC_DRY_ONLY | ACCEPT SYNTHETIC_DRY_ONLY | PASS | 0 |  |
| S01 | distinct u permuted (1, 0, 2, 3) | REFUSAL U_THETA_MISMATCH_common_scale_s | REFUSAL U_THETA_MISMATCH_common_scale_s | PASS | 0 |  |
| S02 | distinct u permuted (0, 1, 3, 2) | REFUSAL U_THETA_MISMATCH_ell_F_m | REFUSAL U_THETA_MISMATCH_ell_F_m | PASS | 0 |  |
| S03 | distinct u permuted (3, 2, 1, 0) | REFUSAL U_THETA_MISMATCH_common_scale_s | REFUSAL U_THETA_MISMATCH_common_scale_s | PASS | 0 |  |
| S04 | distinct u permuted (0, 2, 1, 3) | REFUSAL U_THETA_MISMATCH_gamma_over_Eref | REFUSAL U_THETA_MISMATCH_gamma_over_Eref | PASS | 0 |  |
| S05 | u and theta of ell_F_m/distance swapped together | REFUSAL THETA_BOUNDS_ell_F_m | REFUSAL THETA_BOUNDS_ell_F_m | PASS | 0 |  |
| S06 | dangling symlink as output dir | EXCEPTION_FileExistsError  | EXCEPTION_FileExistsError [Errno 17] File exists: '/Users/bgm/Research/UNT_EXCHA | PASS | 0 |  |
| S07 | production r006_fallback (retired by A93) still accepted; receipt contents | ACCEPT POINT_BOUND_REQUIRES_CLAUDE2_PREFLIGHT | ACCEPT POINT_BOUND_REQUIRES_CLAUDE2_PREFLIGHT | PASS | 0 | SF-4 |

## Item 2: templates (logs/TEMPLATES_AND_STORED_DRY_S1.json; 182/182 checks PASS, with the stored-dry checks)
- **Pins.** The four template pins match the policy, registry V002 and bytes: A_HEADLINE f130e6df, A_STAGE0 c0e96a11, B_HEADLINE 4bd4fc14, B_STAGE0 365c0545. The policy pins both r007 (e4f5864a, registry cd30429c) and r006_fallback (c2930e18, registry 3c42ca07), and each source spec is a registered K32 case in both registries.
- **Point slot.** Declared: point_slot = EXTERNALLY_PINNED_STEP4_ADMITTED_POINT_RECORD_REQUIRED. Every physical value is a '$' placeholder, and the label is a slot.
- **Headline and STAGE0.** The headline uses grid 2e3a36d8. STAGE0_GRID_OUTER uses grid bdb9016c, sets coefficient_alternative, and is NOT_EVALUATED_BEFORE_FREEZE. Its outer_query_ids are exactly Q36-Q43, the rows with R >= 30 kpc in the pinned NGC slots (Q35 = 28.16 kpc, Q36 = 30.08 kpc). STAGE0 differs from the headline only in coefficients and coefficient_alternative; normalized, it also adds alternative_registration.
- **K_big and M_s.** uv_tail.outer.K_big_inverse_kpc = 32 and gas.M_s = 96, both integers, in all four templates and all eight normalized specs. No standalone '128' token appears in any template call_spec or normalized spec, so no DDO P128 or M_s128 was imported.
- **A vs B.** The raw A and B call_specs differ only in schema, physical.entropy_K_factor, route_a_inputs (PENDING_ROUTE_A_OUTPUTS) and source_slots. The stored normalized specs of A and B are EQUAL except for the label, for both drivers and both grids, and A normalizes entropy to 64/121. The A and B schemas are therefore one integrated A-to-B calculation, and running both duplicates it.
- **EPS/LO.** eps_certificate and lo_certificate are the explicit sentinel PENDING_UV_TAIL_CERTIFICATE in the templates and the normalized specs. They are not NONE_TEST_ONLY. The dry plans report them only as the PENDING_UV_TAIL_CERTIFICATE class, with readiness PENDING_CERTIFICATES. They are placeholders, not fabricated bindings.

## Item 3: dry plans
**Stored outputs, verified from bytes.**
- DRY_MATRIX_CX3V001.json 103b5170 (TESTED_PASS, 8 plans). Every log and report pin rehashes.
- Each plan: 11 planned / 0 executed (report, matrix and summary agree); binding_blockers, audit blocks, pin_problems, unexplained and static refusals all empty; remaining classes only PENDING_ROUTE_A_OUTPUTS (6 custody fields) and PENDING_UV_TAIL_CERTIFICATE (2 fields).
- Each plan: driver_sha256 e4f5864a or c2930e18 as expected; call_spec_sha256 equals the registered synthetic spec; ctx simulate only; exit 0; writes only inside its own dry/<id>/ directory.
- No stored read in any plan matches the S1 protected patterns.

**One re-run** (dry_rerun_v001/LOG_S1.json): r007 x CALL_B_K32_STAGE0_GRID_OUTER, chosen because it has the widest input set (B schema, source_slots, STAGE0 context, slots file, bdb9016c).
- Preconditions:
  - Code reading confirmed a pure plan: Ctx('simulate'), whose run_stages records executed=False, and every write lands under the report_dir.
  - It ran under `taskpolicy -b` and the S1 fence.
  - A profile guard denied the scientific entries.
  - The spec was S1's own byte-identical filler output.
- Results:
  - exit 0, exception None; ctx ['simulate']; guard denials [].
  - 0 executed / 11 planned; binding_blockers [].
  - 5.9 s; RSS 91914240 bytes.
  - S1 fence refusals: 0. No protected open, stat or listdir was attempted. Writes outside the report dir: [].
  - The driver read nothing outside Codex3's stored read set. The extra paths in the log are S1's post-run comparison reads of the stored outputs.
  - Comparison with Codex3's stored files: {'EQUAL_AFTER_PATH_SHA_SUBSTITUTION': 14, 'RAW_EQUAL': 4}; derived sha pairs 14; residual none.

## Item 4: static protected-read audit (tools/*.py, review/*.py)
- **Imports and path literals.** No network module is imported (no socket, urllib, http or requests). The only absolute path literals are:
  - the deny patterns ('/runs_ext/uvt_', 'kmax_a2f10_c5h_run_v001', the ngc3198 word list);
  - the Python runtime;
  - two NONEXISTENT fixture paths in test_filler_cx3v001/2.py (/Volumes/External1/prohibited/runs_ext/UVT_NEVER_OPEN/result.json, /Users/bgm/NGC3198_observed_velocities.json). These are stat-ed before refusal (SF-3).
- **What the tools read.** Every read comes from the hash-locked policy (coordinates, NGC slots, drivers, registries, templates, then the source specs, both grids and the NGC monotone source.json) or from the handoff. The NGC slots carry radii only (query rows: Rad_text, radius_kpc, validity flags), with no velocities.
- **Dynamic reads.** The union of Codex3's stored dry reads (344 distinct paths) and S1's re-run reads contains no NGC observed or target file, no SPARC rotation file, no runs_ext/UVT_*, no C5H and no /.vol. The 9 uvt_* paths are source modules.
- **Reachable read paths.** The only reachable protected-read paths are the SF-2 gaps, and they require a root-approved handoff to name them.

## S1 fence (scripts/s1_fence_v3.py)
- **Patterns.** The fence uses Codex3's dry-fence pattern, made stricter. NGC names: ngc3198, ngc_3198, ngc-3198, 'ngc 3198', n3198. NGC words: observed, velocit, rotmod, target, vobs, v_obs, rotation_curve, rotcur, vrot, sigma_obs, errv; target_free and target-free are exempt, as in Codex3's fence. It also covers SPARC rotation data for any galaxy, runs_ext/UVT_*, KMAX_A2F10_C5H_RUN_V001, /.vol, /.resolve, /.nofollow and the .codex trees.
- **Operations.** It covers open, os.stat, os.lstat, os.access, listdir, scandir, mkdir, symlink and link. Each path component is checked BEFORE the real lstat, so the fence itself never touches a protected path. Ordinary uvt_* source modules are allowed.
- **Writes and denied events.** Writes are allowed only to new paths under S1. Delete, rename, chmod, subprocess, exec, fork, kill and socket events are denied.
- **Self-test** (logs/FENCE_SELFTEST_S1_V3.json): 0 of the 344 stored dry reads flagged; 11/11 true positives; 0/4 true negatives flagged.
- **Refusal counts.** Every refused path was a nonexistent fixture, an S1-internal output name, or a scratchpad escape probe that the fence blocked.

| Run | Fence refusals |
|---|---|
| Self-test (intentional probes) | {'C5H_RUN': 1, 'DENIED_EVENT': 2, 'NGC_OBSERVED_OR_TARGET': 1, 'RUNS_EXT_UVT_TREE': 4, 'TOTAL': 10, 'VOLFS_INODE_PATH': 1, 'WRITE_OUTSIDE_S1': 1} |
| Adversarial main run | {'C5H_RUN': 3, 'NGC_OBSERVED_OR_TARGET': 14, 'RUNS_EXT_UVT_TREE': 10, 'SPARC_ROTATION_DATA': 7, 'TOTAL': 51, 'VOLFS_INODE_PATH': 15, 'WRITE_OUTSIDE_S1': 2} |
| Supplement | 0 |
| Codex3-test port | {'NGC_OBSERVED_OR_TARGET': 2, 'RUNS_EXT_UVT_TREE': 3, 'TOTAL': 5} |
| Template and stored-dry checks | 0 |
| Dry re-run | 0 |

## Files (SHA256 of every file is in HASHES_S1.txt)
- scripts/: s1_fence_v3.py (in use); s1_fence_v2.py and s1_fence.py (superseded drafts); s1_fence_selftest*.py; s1_adversarial_filler_v2.py (the v1 file was never run); s1_filler_supplement.py; s1_port_codex3_test_filler_v002.py; s1_templates_and_stored_dry.py; s1_dry_rerun_one.py; s1_write_findings.py.
- logs/: ADVERSARIAL_FILLER_RESULTS_S1_V2.json 513688896a69d3b648315603e388df02798937d533c14fe3aff0006669db0e86; FILLER_SUPPLEMENT_S1.json 76c5bd78b13bf7dddc0c67944e10505af141c048cbae6bc44047361dd064aab8; PORTED_CODEX3_FILLER_TESTS_S1.json fdeae42d16bc96f8eb368090a0e23097e859384b414bc3d54e4c417453396cc0; TEMPLATES_AND_STORED_DRY_S1.json 754342ebfa47159c28bee5d25832b750e42578cbfbbc8cef130653d94218d181; FENCE_SELFTEST_S1_V3.json 783ee06244b79b65271c6bc021aa9257b1a1573ae2d9a55841e95a76bce33306; dry_rerun_v001/LOG_S1.json d60f7950862ce09c01d14ece07828dcfc53dc7b8379a4419d7d859914e0e3a44.
- fixtures_v001/, fixtures_supp_v001/, outputs_v001/, outputs_supp_v001/, port_codex3_v002/ and dry_rerun_v001/report/ hold the test inputs and outputs. FINDINGS_S1_PARTIAL.md is the running log.

## Addendum (append-only, 20:35Z)
- **source.json.** The filler (B templates' source_slots) and the B dry plans read the NGC baryonic source ngc_route_impl_c2/reducer/NGC3198_SEGMENT_MONOTONE_SOURCE_TRUNCATED_RUN_V001/source.json (746980f2). S1 classifies it as target-free from its name, its role (route-B source input) and the program record: it is registered in both r006 and r007 spec registries, and it is the reducer_source of the target-free NGC slots. S1 did not inspect its content beyond what the driver re-run read.
- **W11 and W14.** These output-path cases refused with the expected typed code and are counted PASS in the table. They still show the SF-3 stat-before-refuse pattern: 2 fence-refused metadata accesses each.
- **Running log.** FINDINGS_S1_PARTIAL.md is the running log. This file and the logs govern.
