"""INERT parameterized clean m=0 ("route B") forward driver, Claude2 lane, galaxy-config binding c2v006.
c2v010 (Claude2 lane tail_scheme_impl_c2/driver): the merge of the two drivers both called "c2v009" (root V004 addendum A29),
plus the R-A F-A fix, readout rule RO1 and the optional UV-tail block.  Cite this file by sha256, never as "v010" alone.
  r4 (tail_scheme_impl_c2/driver_r4; successor of r3 4c14552f): RO1 c2v002 (CHECK_V001 F1, A49); nodes_v001 built (A50 item 11);
  probe_R_m in the route-A tail record (A50 item 13); reference successor uvt_c2v003 (CHECK F4); optional
  numerics.route_a.ro1_workers for tail-OFF calls (A50 items 11-12).  See C2V010 r4 comments.
  base bytes: v009-EXT = kmax_prereg_v005_c2/extension_c5c6/driver_v009/galaxy_m0_forward_c2v009.py (999331af).
  (m1) every v008 -> v009-GEO hunk (stage_successor_gal_c2v005/driver/DIFF_V008_V009.diff; v009-GEO 237ef3d4), re-applied
       at the EXT lines: BIND7, the eleven gal_c2v005 stage pins, schema V005, the three schema-V005 galaxy-config files,
       ADMISSION_HEAD and the two record texts.  v009-EXT's G5/G6 prep-v009 selection and numerics.route_a.max_iterations
       are kept.  At 4.04 Mpc a tail-OFF call equals v009-EXT after the GEO pin map and v009-GEO after the EXT map (gate B0).
  (m2) the R-A F-A fix verbatim from REVIEW_DRIVER_V008_C4_V001 sec 6 (f0987f41; gal_c2v005 CHECK_V001 F1): an admitted
       DDO154 route A paired with a checkpoint without IDENTITY.json is REFUSED (ROUTE_A_CHECKPOINT_MISSING) before any
       outcome verdict; a route A computed in run mode that returned a result without a checkpoint IDENTITY is
       FAILED_AT_STAGE (ROUTE_A_RESULT_WITHOUT_CHECKPOINT).
  (m3) readout rule RO1 (V004 addendum A42.2, A46 RA5; V005 A49): the ro1_readout_c2 driver hunks applied verbatim
       (r4: ro1_readout_c2/driver_patch/c2v002/DRIVER_V009EXT_RO1_c2v002.diff 90eb7b56, incl. hunk 6, the RO1-aware NGC reader).  A converged route-A result whose circular-trial readout
       was refused and recorded by a pinned RO1 binding/worker is CONVERGED; route B proceeds on the checkpoint.
  (u)  OPTIONAL numerics.uv_tail (DDO154 only): the tail-corrected lapse (TAIL_SCHEME_DESIGN_V002 sec 2.5/3.7 with the
       V002_R1 record; root A45-A47).  ABSENT: nothing of the C2V010 uv_tail block is normalized, pinned, scanned, loaded or
       launched and the call is the v009 call.  PRESENT: route A = the RO1 successors of the uvtail_c2v001 workers with the
       uvtail solvers and the tail request; a route-A tail manifest stage (route_a_tail_manifest_c2v001.py) rebuilds the
       accepted-iteration tail state from the route-A sidecar and checks its digest; the gal_c2v005_uvt route-B successors run
       the eight stage kinds that read the lapse (feedback v002/v004 and the column mean stay gal_c2v005).  See C2V010 comments.
v009-EXT (999331af) text follows.
c2v009 (Claude2 lane kmax_prereg_v005_c2/extension_c5c6): successor of driver_v008_c2/galaxy_m0_forward_c2v008.py (f8e47701).
Changes ONLY (see the C2V009 comments):
  (a) route-A prep node budget: DDO154 grids of 97..120 nodes/axis run prep v009 (extension_c5c6/prep_successor,
      b4b27a1d = prep v008 except line 130: nk>96 -> nk>120), and only the declared kmax-extension grids G5 (108 nodes,
      kmax 5/kpc) and G6 (120 nodes, kmax 6/kpc) are accepted above 96.  Grids <= 96 nodes/axis select prep v007/v008
      exactly as c2v008, so their requests, inputs and reports are byte-identical to c2v008.  Prep v009 has no review
      pin in this driver (its review is the separate review named by prereg V006); prep_info records that.
  (b) OPTIONAL numerics.route_a.max_iterations M (int 1..32): the per-call seed numerical_inputs.max_iterations, the
      route-A outer-iteration budget.  The serial and parallel solvers use it only as the loop bound
      (for iteration in range(start_iteration, max_iterations)) and record it in the checkpoint identity controls, so
      a route A that converges at iteration < min(8, M) computes the same arrays with M as with the base value 8.
      Absent: the per-call seed is exactly the c2v008 seed.  With an admitted route A it is allowed and must equal the
      value the admitted checkpoint was computed with: it enters the per-call seed, and route_a_custody blocks a seed sha
      that differs from the checkpoint's caller seed (an admitted rerun of a C5/C6 prefix carries the same value).
v009-GEO (237ef3d4) text follows.
c2v009 (Claude2 lane stage_successor_gal_c2v005): driver_v008_c2/galaxy_m0_forward_c2v008.py (f8e47701) with ONLY the
route-B stage binding moved to the gal_c2v005 successors (stage_successor_gal_c2v005/stages; the shared admission also
admits the five DDO154 per-call geometry fields PER_CALL, schema V005 per_call_geometry), the schema V005 pin, the three
galaxy-config files re-pinned to their schema V005 copies, the shared-admission head the binding check locates, and two
record texts (geometry probe rule, GEOMETRY_NOT_ADMITTED refusal).  At 4.04 Mpc every request and input equals c2v008
after the pin substitution; at D != 4.04 the probe now admits and run mode is no longer BLOCKED before any stage.
c2v008 text follows.
c2v008 (Claude2 lane driver_v008_c2): successor of driver_v007_c2/galaxy_m0_forward_c2v007.py (0338584b).
Changes ONLY (see the C2V008 comments):
  (a) DDO154 physical.distance_Mpc is a call input again: the c2v003b/c2v003c per-call geometry path (derive_geometry,
      geometry_inputs, GEOMETRY_PINS; absorb_c2_0473/driver_f/galaxy_m0_forward_c2v003c.py ed326130) is ported VERBATIM and
      wired into the galaxy-config structure: route-A prep module patch C (as c2v003c), route-A custody source-profile pin
      (ROUTE_A_GEOMETRY_MISMATCH, as c2v003c), the reference PROFILE/PROFILE_SHA stage globals and reuse-module patch (as
      c2v003c), and the per-call config fields source.profile, source.monotone_source, radial.outer_edge_kpc,
      observation.binding, observation.query_rows (to the stages that consume them).  Inclination stays registered-only;
      NGC3198 keeps its registered geometry (both NGC normalizers unchanged).  At the registered 4.04 Mpc nothing new is
      planned or written (requests byte-identical to c2v007).  At D != 4.04 the gal_c2v004 stages' OWN shared admission
      (schema V004) refuses those PER_CALL fields for DDO154 (only DDO154_EXACT_LITERAL or PER_CALL on per-call kinds), so
      run mode is BLOCKED (GEOMETRY_NOT_ADMITTED_BY_STAGE_BINDING) before any stage, from a probe that runs each stage's
      own admission function on the per-call config (and on a registered-geometry control copy).  Also ported from
      c2v003c: the admitted reference/body geometry custody (reference start.json source_custody, body input_pins).
  (b) is the deciding-(ii) comparator (deciding/compare_deciding_ii_c2v008.py); no driver change.
  (d) c2v003c CHECK D1 (DDO154): a route-A attempt must belong to the checkpoint it is paired with (result.json
      source_fixed_point.checkpoint.identity_sha256 == IDENTITY, and its attempt token has an attempts/<token>.end.json of
      that identity); else Refusal ROUTE_A_ATTEMPT_NOT_OF_THIS_CHECKPOINT, checked before the F1 outcome.
  Not changed (INTERFACE_V008 (c)): LE and reference column parallelism (the column mean v004 consumes exactly one 72-column
  run; the reference stage writes one run of all radii).
c2v007 text follows.
c2v007 (Claude2 lane driver_v007_c2): successor of ngc_f10_c2/route_b_v006/galaxy_m0_forward_c2v006.py (c53997b4).
Changes ONLY (see the C2V007 comments):
  (a) the four RD1 driver fixes of absorb_c2_0473/driver_f/galaxy_m0_forward_c2v003c.py (ed326130; hunks in
      DIFF_V003B_V003C.txt), ported onto the v006 structure:
      F1 the route-A outcome is classified from the attempt's own result.json; no finite fixed point -> run status
         ROUTE_A_NO_FIXED_POINT (a model outcome, not BLOCKED); v006 has no iteration-4 lock, so v003c's
         "converged at k != 4" verdict becomes "converged iteration in result.json != the strict reader's iteration";
      F2 run outdir / dry-run report dir made absolute (os.path.abspath: lexical, no symlink resolution) and every
         path a stage request hands to its child refused if relative;
      F3 bracket-override keys must be canonical ASCII decimal ('0' or [1-9][0-9]*), the form str(i) lookups use;
      F4 route-A custody checks the background mu/C (the check offset v003 makes) before any route-B stage.
  (b) OPTIONAL DDO154 parallel route A: numerics.route_a.column_workers N (int 1..64).  Absent or 1: the reviewed serial
      worker c4cb6826 + reviewed solver 44d9c23c, request byte-identical to c2v006.  N > 1: the parallel worker successor
      9dbdaf11 + parallel solver aed4dd59 with --column-workers N (parallel_route_a_c2, CHECK_V001 PASS).  The checkpoint
      IDENTITY then differs only in code.solver.{path,sha256}; custody records the solver from IDENTITY bytes
      (custody.solver_code) and, for a route A computed by this call, requires it to be the requested solver.
c2v006 text follows.
c2v006 (Claude2 lane ngc_f10_c2/route_b_v006): successor of ngc_route_impl_c2/binding/galaxy_m0_forward_c2v005.py
(2aef51c4), from ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V002_ADDENDUM (A0, A2-A5) and the binding/reducer CHECK_V001
defects D1-D4, D6, D8.  Changes (see the C2V006 comments):
  * stages: the eleven gal_c2v004 successors (route_b_v006/stages): schema V004 pin + shared c2v004 admission (optional
    config 'member', A2 / CHECK D2); body D3 (prefix-form source when truncated) and D4 (N2 edge guard before the loop);
    column mean A4/N1 (binding invalid_row_rule: rows below the innermost radial node are emitted valid=false
    QUERY_INSIDE_INNERMOST_NODE, the call stays valid).  DDO154 runs exactly the c2v003 code paths.
  * schema V004 (A4): NGC3198 observation.binding = the 43-row column-mean binding (route_b_v006/inputs), tracer and
    observation rule, brackets.rule_factors and driver.fixed_args = the DDO154 values; member NGC3198/GL10_ALTERNATIVE.
  * NGC3198 route B (A5, CHECK D1 MAJOR): the call-spec coefficient grid is accepted when it is a decided grid
    (fe5a2f06 V004 provisional = NGC prep v001 default, or 2e3a36d8 A2 pooled) AND equals the coefficients the NGC
    route-A seed records (no record: prep v001 default fe5a2f06); the checkpoint grid digest check stays the guard.
    The physical block is the anchor's unscaled block with its s (checked against the route-A seed x s).
  * NGC3198 call spec: entropy_K_factor only 64/121 (primary) or 1.0 (labelled N4 original-K alternative) (D6);
    brackets: the galaxy-config rule factors only, no overrides (A4: DDO manual corrections not carried);
    source.monotone_source only the reviewed N3 output 746980f2 (D3, A3); route_a_inputs may name the route-A run
    directories with PENDING sentinels (template; nothing under them is opened while pending); member GL10_ALTERNATIVE.
  * dry run (D8): lists every refusal knowable without route-A bytes, plus the checks that need route-A bytes as
    class PENDING_ROUTE_A_OUTPUTS items (grid digest, seed coefficients/physical, iteration, roster, template mapping).
c2v005 text follows.
Successor of ngc_route_construction_c2/v004_fix/galaxy_m0_forward_c2v004.py (e2141e5d), written in
ngc_route_impl_c2/binding from ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V001 (N1, N2, N4, N5; N3 as a declared
input slot).  c2v005 changes ONLY the stage binding and the galaxy-config contract (see the C2V005 sections):
  * every route-B stage runs a gal_c2v003 successor (binding/stages): the stages2 successors of reference, body,
    fs columns v001 and rfs columns v003, the v004_fix successors of offset, le columns v005, le rotation v005,
    le feedback v004 and column mean v004, and new successors of fs rotation v001 and fs native feedback v002 (needed
    once fs columns run as a successor: their reviewed bases hard-code the producer shas of the reviewed stage before).
    All share ONE admission (admit_config on GALAXY_CONFIG_SCHEMA_V003, N5) and the strict route-A reader
    route_a_final_iteration verbatim (stages2 CHECK D2), and receive --galaxy-config/--galaxy-config-sha256
    (column mean: --galaxy-config PATH SHA).  No stage globals are patched any more (dropped: SEED_SHA, IDENTITY,
    REFERENCE, DATA_PINS, OFFSET_SHA, PINS, COEFF/COEFF_SHA); the reuse_patch of the reviewed reference worker module
    (SEED_SHA/IDENTITY) is kept exactly as c2v004 (body, offset, columns, rotations, feedback read reuse.SEED_SHA).
  * reference runs with the stages2 reference module successor 1b00add9 (n_phi keyword); le/fs rotation pin the stages2
    join successor 0a7f5314 (n_columns keyword); body pins the stages2 body base successor d540fd7c.
  * producer identities: custody.body_worker_sha256 and custody.fs_feedback_worker_sha256 are per-call config fields;
    the fs rotation (column worker), fs feedback (rotation worker) and column mean (rotation worker) take their producer
    from config producer_pins; flags keep the c2v004 producer rule (run: SCRIPTS sha; simulate on SAVED outputs: the
    worker recorded in that output's start.json).  Every producer is whitelisted to {successor, reviewed base}.
  * route-A iteration: no driver literal 4 any more; the converged final iteration is read by the strict rule and passed
    as route_a.accepted_iteration (every stage re-derives it).
  * N2: radial.outer_edge_kpc is consumed by reference/body/offset/rotations (radial_truncation); DDO154 = last edge.
  * NGC3198 route B: call spec schema UNT_GALAXY_M0_FORWARD_CALL_C2V001 with galaxy NGC3198, route_a_inputs (outputs of
    the NGC route-A lane, or PENDING_ROUTE_A_OUTPUTS) and source_slots (the N3 monotone source, or PENDING); values
    from the galaxy config (N1 GL4, N2 66.904 kpc, N4); dry-run lists every remaining refusal by class; run mode is
    BLOCKED before any stage while any refusal remains.
  Run-mode equivalence to the saved DDO154 chain is UNTESTED until the deciding test (REPRO_PINNED_ADMIT_PREFIX with
  reference_compare; deciding_test_verdict).

One call = one parameter point, read from a single JSON call spec.  Runs the full chain that
produced the saved DDO154 axisymmetric reference, reusing every reviewed stage script by
executing its exact pinned bytes (SHA256 verified from bytes) in a child process:

  route_a     ddo_composite_stable_cached_root_worker_v002 (+solver/checkpoint 0422)  -> G4 fixed point
  reference   ddo_homotopy_reference_root_worker_v001 (reference module V003)        -> 72-radius reference
  body        ddo_saved_root_body_array_root_v002                                    -> 72x16x8 body arrays
  offset      ddo_body_source_offset_root_v003                                       -> unit response, offset
  fs_*        ddo_fixed_K_free_surface_root_v001 / rotation_root_v001 / feedback_root_v002 (original K)
  rfs_columns ddo_fixed_K_free_surface_root_v003 (original K, refreshed field; bracket source only)
  le{p}_*     ddo_fixed_K_free_surface_root_v005 / rotation_root_v005 / feedback_root_v004 (scaled K)
  le{P}_column_mean  ddo12_lower_entropy_column_mean_root_v004                         -> 12 rows

No equation, tolerance or guard of any stage is changed.  The ONLY substitutions are module
globals that hard-code the identity of one historical run (seed SHA, checkpoint identity,
offset finish SHA, reference-run pins, column-mean input pins, coefficient-grid pin).  They
are replaced by per-call values computed from bytes of this call's own (or explicitly
admitted, re-verified) upstream outputs.  Optional truncation shapes 'sphere'/'cylinder'
are a declared NUMERICAL CHOICE implemented only as a 0/1 weight mask on the existing
composite grid (see truncation_mask and INTERFACE_C2_0466_V001.md).

Importing this module does nothing.  CLI:
  run      --spec SPEC.json --outdir NEW_DIR      (outdir must be absent; never retries)
  dry-run  --spec SPEC.json --report-dir NEW_DIR  (pins, JSON/NPZ headers, planned stage calls;
                                                   no stage is executed)
  _stage   REQUEST.json                           (internal: one stage in this process)
"""
import hashlib
import json
import math
import os
import sys
import time
from pathlib import Path

SCHEMA = 'UNT_GALAXY_M0_FORWARD_CALL_C2V001'
RESULT_SCHEMA = 'UNT_GALAXY_M0_FORWARD_RESULT_C2V001'
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
ROOT = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
HC = ROOT / 'helpers/coefficient_method'
HR = ROOT / 'helpers/recovered_packet_audit'
C1 = ROOT / 'CODEX1'
HP = ROOT / 'helpers/response_packet_audit'
EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
V4FIX = EX / 'ngc_route_construction_c2/v004_fix'  # c2v004: successors gal_c2v002, schema V002, galaxy configs (history)
S2MOD = EX / 'ngc_route_construction_c2/stages2/modules'  # c2v005: stages2 module successors
BIND = EX / 'ngc_route_impl_c2/binding'  # c2v005: gal_c2v003 stage successors, schema V003, galaxy configs
BIND6 = EX / 'ngc_f10_c2/route_b_v006'  # c2v006: gal_c2v004 stage successors, schema V004, galaxy configs, NGC binding
BIND7 = EX / 'stage_successor_gal_c2v005'  # c2v009: gal_c2v005 stage successors, schema V005, galaxy configs
KPC_M = 3.085677581491367e19  # identical to seed numerical_inputs.kpc_m (checked at run time)
THREAD_ENV = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS',
              'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS')

# Stage scripts.  c2v005: every route-B stage is a gal_c2v003 successor (GENERALIZED holds each reviewed base, the
# script the saved DDO154 chain launched).  Route A is the reviewed worker, unchanged.
SCRIPTS = {
    'route_a': (HR / 'ddo_composite_stable_cached_root_worker_v002.py', 'c4cb682669993afbad3c623a010244cc8a31b9fcbacfe44e6bc692bf2d5895a4'),
    # c2v006: the gal_c2v004 successors of the c2v005 gal_c2v003 stages (route_b_v006/stages/build_stages_c2v004.py)
    # c2v009: their gal_c2v005 successors (stage_successor_gal_c2v005/stages/build_stages_c2v005.py; admission only)
    'reference': (BIND7 / 'stages/ddo_homotopy_reference_root_worker_v001_gal_c2v005.py', 'cdf155e8161a89fd78518bbe048fae2b8114a5fb04b0fb770c30a8502308eb7f'),
    'body': (BIND7 / 'stages/ddo_saved_root_body_array_root_v002_gal_c2v005.py', '7387493b6e2e153afd0e2352cf630edd32944d641dc563a706381983add0b1e3'),
    'offset': (BIND7 / 'stages/ddo_body_source_offset_root_v003_gal_c2v005.py', '1ee18dcdcc42fc2465cebcc120297f262839fc4506249416b4d71d6a00be3dd4'),
    'columns_v001': (BIND7 / 'stages/ddo_fixed_K_free_surface_root_v001_gal_c2v005.py', '2699cc76777621aea33398acb394ec880189399623a24dd0fb6d76e9ed0a0011'),
    'rotation_v001': (BIND7 / 'stages/ddo_free_surface_rotation_root_v001_gal_c2v005.py', 'a49085e96e8b5f241b45e72682140b4b6892fa6171ca8c8d42fc28b0eaa61e85'),
    'feedback_v002': (BIND7 / 'stages/ddo_free_surface_native_feedback_root_v002_gal_c2v005.py', '77ac558786dbe8dc932ff1d902200f85d570f058b903e7253acb31d40a2cb99b'),
    'columns_v003': (BIND7 / 'stages/ddo_fixed_K_free_surface_root_v003_gal_c2v005.py', '1f473e39a7634e86bc49edfd1a409ca787c92a7031b761b734933e7401d31ba0'),
    'columns_v005': (BIND7 / 'stages/ddo_fixed_K_free_surface_root_v005_gal_c2v005.py', '99fab2857b3f18e1f05c78da81c9d1dc2b4206e65aaadb4ed0fd78b8a639bea1'),
    'rotation_v005': (BIND7 / 'stages/ddo_free_surface_rotation_root_v005_gal_c2v005.py', 'be1c913f4cfe3f6ccafd5d48bd2fb68856fa080ad8da016091ec237c652bef25'),
    'feedback_v004': (BIND7 / 'stages/ddo_free_surface_native_feedback_root_v004_gal_c2v005.py', 'b3a8424e15343bbf3dc80430d3170f385718eb96d5cc5789fa66e3be5b30b02e'),
    'column_mean_v004': (BIND7 / 'stages/ddo12_lower_entropy_column_mean_root_v004_gal_c2v005.py', 'ae78b012d079ceffd62af1dbc8c59c4aaf97cbc30e697eca8b58cd03fb732d38'),
}
# c2v006: the c2v005 script each successor was built from (declared plan-difference class STAGE_SUCCESSOR_C2V004).
C2V005_SCRIPTS = {
    'reference': (BIND / 'stages/ddo_homotopy_reference_root_worker_v001_gal_c2v003.py', '406dda4412ba1a87624908689a4a804ff7e07a140574e6e823a254d544dd66f1'),
    'body': (BIND / 'stages/ddo_saved_root_body_array_root_v002_gal_c2v003.py', '5eb33018e2ce7fbc52caea897651169cf3d0b310f140b98f99136fa9540e6d63'),
    'offset': (BIND / 'stages/ddo_body_source_offset_root_v003_gal_c2v003.py', '5fb1660f4fe55599073c8756010a0b6af3254a181f876d1928dedf899686d7f2'),
    'columns_v001': (BIND / 'stages/ddo_fixed_K_free_surface_root_v001_gal_c2v003.py', '529320ee8cff0ca90ca32f69e3f6c9f7e3d3678da5be801941071a3dc2f2d66a'),
    'rotation_v001': (BIND / 'stages/ddo_free_surface_rotation_root_v001_gal_c2v003.py', '4c2ddad8e8eed82ab3ea9959e68a12c4f84891a223099c2030d10a20bfc66881'),
    'feedback_v002': (BIND / 'stages/ddo_free_surface_native_feedback_root_v002_gal_c2v003.py', '0816b3416fdfb7ee599125d2a6393f6e1ed1986d239986ac75cfd8e0d79c6561'),
    'columns_v003': (BIND / 'stages/ddo_fixed_K_free_surface_root_v003_gal_c2v003.py', 'b76b0dcaaa3cb918de0993d1bfb52380a2f33633e44f9f7d4a144ecc406f4f0e'),
    'columns_v005': (BIND / 'stages/ddo_fixed_K_free_surface_root_v005_gal_c2v003.py', 'a72664a6e509801af313e6f616af05ea2ad4caa4661bfcead94922862c2ac07b'),
    'rotation_v005': (BIND / 'stages/ddo_free_surface_rotation_root_v005_gal_c2v003.py', '2eec8f5cf55464dc8eb130f76e8cc65dfc94157ab7865ec3e97d39c170dad896'),
    'feedback_v004': (BIND / 'stages/ddo_free_surface_native_feedback_root_v004_gal_c2v003.py', '796e50ec874ef9c4b15ee03f5aed44dc08ab01c9b657da57a434c11551d21f9c'),
    'column_mean_v004': (BIND / 'stages/ddo12_lower_entropy_column_mean_root_v004_gal_c2v003.py', '3d076998a09c2c72da279ab86fcf6fc5f7002dde906ba4b3b12acc4d1ba0de2e'),
}
# c2v005: reviewed DDO-literal base of each successor (the script the saved chain launched), its config format, the flag
# style, the stage globals c2v003/c2v004 patched that the successor no longer has, and the producer pins it reads.
_OFF = {'OFFSET_SHA': 'custody.offset_finish_sha256'}
GENERALIZED = {
    'reference': {'base': (HR / 'ddo_homotopy_reference_root_worker_v001.py', 'acda989d375925bf9a8163d8d8a3a22c3f183b6b253c8137312bccc0cefbbe36'),
                  'format': 'UNT_ROUTE_B_STAGE_CONFIG_REFERENCE_C2V003', 'flags': 'pair',
                  'dropped_globals': {'SEED_SHA': 'custody.seed_sha256', 'IDENTITY': 'custody.checkpoint_identity_sha256'}},
    'body': {'base': (HC / 'ddo_saved_root_body_array_root_v002.py', '271e5612caf00cbde3a154d6deb4c7c4d5c7ec342b9ede893e0bf820d044a8f6'),
             'format': 'UNT_ROUTE_B_STAGE_CONFIG_BODY_C2V003', 'flags': 'pair',
             'dropped_globals': {'REFERENCE': 'custody.reference_run', 'DATA_PINS': 'custody.reference_run + source.monotone_source'}},
    'offset': {'base': (HC / 'ddo_body_source_offset_root_v003.py', 'c5faed578e8e9b6e60b2c0309049232ed11c634347cf80570f939764df6620b1'),
               'format': 'UNT_ROUTE_B_STAGE_CONFIG_OFFSET_C2V003', 'flags': 'pair', 'dropped_globals': {'COEFF': 'source.coefficients', 'COEFF_SHA': 'source.coefficients'}},
    'columns_v001': {'base': (HC / 'ddo_fixed_K_free_surface_root_v001.py', '399720adc6eb1836a15e147ccd395a5a9346e9fc2a49db8f2c41bb1c2f5dc347'),
                     'format': 'UNT_ROUTE_B_STAGE_CONFIG_FS_COLUMNS_C2V003', 'flags': 'pair', 'dropped_globals': _OFF},
    'rotation_v001': {'base': (HC / 'ddo_free_surface_rotation_root_v001.py', '3df32880972a4cd94cac6072a106ef94cacaa8a1a1de52f7f3872692e7efbfc2'),
                      'format': 'UNT_ROUTE_B_STAGE_CONFIG_FS_ROTATION_C2V003', 'flags': 'pair', 'dropped_globals': _OFF,
                      'producer_pins': {'column_worker': 'columns_v001'}},
    'feedback_v002': {'base': (HC / 'ddo_free_surface_native_feedback_root_v002.py', '44376116d64825ce5319e402a47c138e5e69303a6482d3ebc54abee8291ae1fd'),
                      'format': 'UNT_ROUTE_B_STAGE_CONFIG_FS_FEEDBACK_C2V003', 'flags': 'pair', 'dropped_globals': _OFF,
                      'producer_pins': {'rotation_worker': 'rotation_v001'}},
    'columns_v003': {'base': (HC / 'ddo_fixed_K_free_surface_root_v003.py', 'c9e2c2ecb6dd7d388cb9cb8658f5330d0d7cab48abde8de1c82b91f326dde1f9'),
                     'format': 'UNT_ROUTE_B_STAGE_CONFIG_RFS_COLUMNS_C2V003', 'flags': 'pair', 'dropped_globals': _OFF},
    'columns_v005': {'base': (HC / 'ddo_fixed_K_free_surface_root_v005.py', '8a9b2ec1eaba3661b8e5d11cca66b7761efcb0bd0dab4a53987b222b242cda96'),
                     'format': 'UNT_ROUTE_B_STAGE_CONFIG_COLUMNS_C2V003', 'flags': 'pair', 'dropped_globals': _OFF},
    'rotation_v005': {'base': (HC / 'ddo_free_surface_rotation_root_v005.py', '1b42990556ee34d30a7a12eb5b5605aa1e43aa8322e03d73bbab86e5c38497b7'),
                      'format': 'UNT_ROUTE_B_STAGE_CONFIG_ROTATION_C2V003', 'flags': 'pair', 'dropped_globals': _OFF},
    'feedback_v004': {'base': (HC / 'ddo_free_surface_native_feedback_root_v004.py', '6da11133734e65fe31b6408d4f64d0e50df9f453c8872308b960678d80ec02ed'),
                      'format': 'UNT_ROUTE_B_STAGE_CONFIG_FEEDBACK_C2V003', 'flags': 'pair', 'dropped_globals': _OFF},
    'column_mean_v004': {'base': (HC / 'ddo12_lower_entropy_column_mean_root_v004.py', '12504c4b86c31e20d0e019868c406f22c35a568e3ad25ee39a9db8ddabfda3c2'),
                         'format': 'UNT_ROUTE_B_STAGE_CONFIG_COLMEAN_C2V003', 'flags': 'nargs2', 'dropped_globals': {'PINS': 'custody.column_mean_input_pins'},
                         'producer_pins': {'rotation_worker': 'rotation_v005'}},
}
AUX = {
    'solver': (EX / 'resumable_coupled_gas_0422/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_c2v001.py', '44d9c23c47d6beb52b7539802fcf0f284c1a2c7eea7662536f04b184523e3644'),
    'checkpoint_module': (EX / 'resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v003.py', '069b393560003fc200932e2d17fa84ee750043fa2132f2cadd459915fb99b114'),
    # c2v005: the stages2 n_phi successor of the reviewed reference module v003 (81a04b12); the reference successor binds only it.
    'reference_module': (S2MOD / 'owned_axisymmetric_homotopy_reference_v003_gal_c2v001.py', '1b00add9fb6b7ee563fe4ab86e971345d45123a6a10beccebae4b93b7558383b'),
    'prep': (HC / 'ddo_actual_initial_source_preparation_v007.py', 'ac905597b1aa06da3a0178bfa629f6256b78cc87e8b1b05fcea22b3f6df25a42'),
    'cache': (HR / 'owned_scalar_lapse_inverse_cache_v001.py', '7b9816aea218d638c2eece184df22e29ca18b68547f3d04193780c2eff96a529'),
    # c2v003: ddo_actual_initial_source_preparation_v008.py bb05f97452cec43e215fa0853b0674262eb54c75de524b5a640cd984cd137e62
    # differs from V007 only at line 130 (node budget nk>80 -> nk>96); reviewed PASS_SCOPED in
    # CURRENT_SOURCE_ALL_PANEL_DERIVATIVE_AUDIT_REVIEW_V001.json (PREP_V008_REVIEW).  Used ONLY for grids > 80 nodes/axis.
    'prep_v008': (HC / 'ddo_actual_initial_source_preparation_v008.py', 'bb05f97452cec43e215fa0853b0674262eb54c75de524b5a640cd984cd137e62'),
    # C2V009 (a): prep v009 = v008 except line 130 (nk>96 -> nk>120).  Used ONLY for grids of 97..120 nodes/axis (G5, G6).
    'prep_v009': (EX / 'kmax_prereg_v005_c2/extension_c5c6/prep_successor/ddo_actual_initial_source_preparation_v009.py',
                  'b4b27a1deb68a2ec24e9bd3700de3a23537fd14b7029e124aab0f7b50bcac8bc'),
}
# C2V007 (b): OPTIONAL DDO154 parallel route A (parallel_route_a_c2, INTERFACE_PARALLEL_ROUTE_A_C2V001, CHECK_V001 PASS).
# Used ONLY when numerics.route_a.column_workers > 1; never pinned, scanned or launched otherwise.  The worker is the
# successor of SCRIPTS['route_a'] (c4cb6826; same LOCAL keys and pins, absolute H, required --column-workers N); the
# solver is the successor of AUX['solver'] (44d9c23c).  The checkpoint module AUX['checkpoint_module'] is unchanged.
PAR = EX / 'parallel_route_a_c2'
PARALLEL_ROUTE_A = {
    'worker': (PAR / 'ddo_composite_stable_cached_root_worker_v002_parallel_c2v001.py', '9dbdaf11eb80fd4fa8d47e8c0827eae51d06e87f05efdd6e5c11d422ecbd197a'),
    'solver': (PAR / 'coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_parallel_c2v001.py', 'aed4dd59b38bfe1043e0c38ad4592e4b6bb74c8c4bbee969a707a310926e6f58'),
}
ROUTE_A_COLUMN_WORKERS_MAX = 64  # the worker and solver refuse anything outside 1..64 (INTERFACE "API")
ROUTE_A_MAX_ITERATIONS_MAX = 32  # C2V009 (b): declared ceiling for numerics.route_a.max_iterations (base seed value 8)
# RO1 (ro1_readout_c2/RO1_IMPL_V002.md; ROOT_DECISIONS V004 ADDENDUM A42.2, V005 ADDENDUM A48 AMB-14/AMB-15, A49).
# c2v002 (A49): RO1_MESSAGES adds DEGENERATE_RADIAL_EULER (A49.1), the pins name the RO1 c2v002 successors, and the NGC
# route-A-only reader ngc_read_route_a_result records rows None when route_a_outcome.ro1 fired (A49.3).
# (1) Readout rule RO1.  Every route-A outcome record carries route_a_outcome.ro1 = {rule 'RO1', fired, events, armed, ...}
# (the V007 compare path, AMB-15).  An attempt written through a pinned RO1 binding (result.json input_pins) by a pinned RO1
# worker (attempt start.json worker_pin) is ARMED.  If an armed attempt's prediction slot carries an admissible
# route_a_readout_refusal record (code RO1_CODE, refusal in RO1_MESSAGES, after_convergence True, readout_status RO1_CODE,
# predictions_available False, rows None) and the solver outcome is converged, it is classified CONVERGED, fired is True
# and events = [the record]: route B proceeds on the checkpoint.  Every other classification is exactly v009-EXT's.
# The workers are the RO1 successors of the uvtail_c2v001 route-A workers (same CLI); this driver launches none of them
# (v010 wires them in place of its uvtail_c2v001 workers).
# (2) AMB-14: OPTIONAL numerics.route_a.seed_source_rtol_factor f (finite, 0 < f <= 1): the per-call seed
# numerical_inputs.source_rtol becomes base source_rtol * f (the route-A source-convergence rtol: binding controls ->
# composite adapter -> solver bound source_atol_J + source_rtol*scale).  Absent: normalization, seed and requests are
# byte-identical to v009-EXT.  Nothing else changes.
RO1_DIR = EX / 'ro1_readout_c2'
RO1_ROUTE_A = {
    'worker': (RO1_DIR / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/ro1_readout_c2/ddo_composite_stable_cached_root_worker_v002_uvtail_ro1_c2v002_r5.py', 'fbe9ae79ac113aab76109ece785d8030729ce62890dc76ff58144a75af6c17b3'),
    'worker_parallel': (RO1_DIR / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/ro1_readout_c2/ddo_composite_stable_cached_root_worker_v002_parallel_uvtail_ro1_c2v002_r5.py', '869ce3870a13fdc94a014cdb0b34eab867c05e59ab7d8abfb15f7db382fd52da'),
    'ngc_worker': (RO1_DIR / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/ro1_readout_c2/ngc43_composite_coupled_root_worker_v002_uvtail_ro1_c2v002_r5.py', 'b6c4586d2236a4cb14cc3d334adb0c8bb0aa729a3c23b33af8f71f807777370d'),
    'ngc_worker_parallel': (RO1_DIR / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/ro1_readout_c2/ngc43_composite_coupled_root_worker_v002_parallel_uvtail_ro1_c2v002_r5.py', 'ee0510dface33bf97b55d51e31941c635b365f386054bf96b9dd218a490e3a3e'),
    'binding': (RO1_DIR / 'ddo_composite_stable_cached_binding_v002_uvtail_ro1_c2v002.py', '86af6198045ee6995daa7b57e78570643ddbd9edcc0eba42e2fdc816897ca885'),
    'ngc_binding': (RO1_DIR / 'ngc_composite_full_coupled_binding_v002_uvtail_ro1_c2v002.py', '52dc4065da6b0307d1a37bb63bf22921edd08709a763b0ed5a114e8c2b0f2226'),
}
RO1_CODE = 'ROUTE_A_READOUT_NO_CIRCULAR_BRANCH'
RO1_MESSAGES = ('NO_SUBLUMINAL_CIRCULAR_PRESSURE_BRANCH',  # V005 ADDENDUM A49.1: exact raised texts (e9be043b L208, L205, L184)
                'DEGENERATE_RADIAL_EULER: zero exact denominator; no unique speed', 'NON_TIMELIKE_COLUMN')
# ---- C2V010 (u) uv_tail (tail_scheme_impl_c2/driver; TAIL_SCHEME_DESIGN_V002 sec 2.5/3.7, V002_R1; root V004 A42/A45/A46,
# V005 A47).  Used ONLY when a DDO154 call spec declares numerics.uv_tail; absent, no table below is pinned, scanned, loaded or
# launched.  Tail ON: route A = RO1_ROUTE_A worker / worker_parallel (RO1 successors of the uvtail_c2v001 workers d223ad61 /
# dac9efcb) with AUX_UVT solver / solver_parallel; then the manifest stage AUX_UVT manifest_writer; route-B kinds in
# SCRIPTS_UVT run their gal_c2v005_uvt successors (tail_scheme_impl_c2/route_b BUILD_ROUTE_B_UVT_C2V002 8379a92d).
UVT = EX / 'tail_scheme_impl_c2'
UVT_LIB = {
    'lib': (UVT / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py', '2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54'),
    'roster': (UVT / 'module/uv_tail_source_roster_c2v001.py', '4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2'),
    'provider': (UVT / 'module/posix_libm_bessel_jn_provider_c2v001.py', 'd6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171'),
}
SCRIPTS_UVT = {
    'reference': (UVT / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/driver_r4/route_b/ddo_homotopy_reference_root_worker_v001_gal_c2v005_uvt_c2v003_r5.py', '022f257066032865a8c068009fea7618844a993e38d9eb19cc82f303fa637642'),  # r4 F4: successor of uvt_c2v002 6775599e
    'body': (UVT / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/stages/ddo_saved_root_body_array_root_v002_gal_c2v005_uvt_c2v001_r5.py', '4b0f28fa0539c4ebb2413b91dddc4f93cc74f147000dccb2926177e1da16a42a'),
    'offset': (UVT / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/stages/ddo_body_source_offset_root_v003_gal_c2v005_uvt_c2v001_r5.py', '693686352af3020734530b5e896364e58037926c659c23d3e514c88cb5cccbe6'),
    'columns_v001': (UVT / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/stages/ddo_fixed_K_free_surface_root_v001_gal_c2v005_uvt_c2v001_r5.py', 'a129b3d8ed5e9ededd9d854ae4ef971f8150dbd9ed79d697331d2e7e8b1f0a7b'),
    'rotation_v001': (UVT / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/stages/ddo_free_surface_rotation_root_v001_gal_c2v005_uvt_c2v001_r5.py', '139643c01d3be53e34df8ececccea69d4a2a7377486498c4d1035e5cb4433242'),
    'columns_v003': (UVT / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/stages/ddo_fixed_K_free_surface_root_v003_gal_c2v005_uvt_c2v001_r5.py', 'a1a8a4bdc7bd928e664b2cd595171d4e4fd5a72a61825bc24bfb7a689cc8b3ff'),
    'columns_v005': (UVT / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/stages/ddo_fixed_K_free_surface_root_v005_gal_c2v005_uvt_c2v001_r5.py', 'e0d3132e82dc2b5c2557b85a846233c4ea3cddfe885795fc4605af3f78d683ff'),
    'rotation_v005': (UVT / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/stages/ddo_free_surface_rotation_root_v005_gal_c2v005_uvt_c2v001_r5.py', '8459ce3cbccb47e3b59f7cf08f33ce8565efae9dd6df8d79d35aa27782b24601'),
}
AUX_UVT = {
    'route_b_binding': (UVT / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/uvt_route_b_binding_c2v001_r5.py', '1e27430c12cc84195b7642fe925bc6f9916a55158ecc02c9fbff9b8564506329'),
    'controller': (UVT / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_a/route_a_uv_tail_controller_c2v001_r5.py', 'c5bdd0553968e3f00b61db89f7944cebe51166006f58b727a7aed2a9b6a434fc'),
    'facade': (UVT / 'route_a/owned_stable_lapse_hi_facade_uvtail_c2v001.py', '191fb7bd91708b6aae9fdc21d1bf81c01482374ae5b6f80cbaad5a9a8438af9c'),
    'solver': (UVT / 'route_a/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_uvtail_c2v001.py', '8ef3079b0a23c32c688605e96eb5b79beb79768578cc7aef22ea087c7ae12469'),
    'solver_parallel': (UVT / 'route_a/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_parallel_uvtail_c2v001.py', '7667025bd9382a58688153fde98bf90f2b67d27baa39a939982631c305c229db'),
    'manifest_writer': (UVT / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/driver/route_a_tail_manifest_c2v001_r5.py', '44b31a8b8a91bf7ff67426a1def0b441f4e6d6dc69d00474892883f68ca93b33'),
}
# K16 (planning only): the v002-lineage NGC route-A code the tail-ON NGC configuration plans (route_a_f10/LAUNCH.json d70cbcfe).
NGC_CODE_UVT = {
    'worker': RO1_ROUTE_A['ngc_worker'], 'worker_parallel': RO1_ROUTE_A['ngc_worker_parallel'], 'binding': RO1_ROUTE_A['ngc_binding'],
    'uvtail_binding_base': (UVT / 'route_a/ngc_composite_full_coupled_binding_v002_uvtail_c2v001.py', 'e666bede787aac37424faec70d0fb8abc9bc68f9db3d7408a1a59fa507b30ff7'),
    'solver': AUX_UVT['solver'], 'solver_parallel': AUX_UVT['solver_parallel'],
    'lineage_evidence': (EX / 'ngc_f10_c2/route_a_f10/LAUNCH.json', 'd70cbcfe061ba357a0f8cfc8624468b4d00569b01b99bae6a268585846c3f1e7'),
}
# The route-A monitor (design sec 1.7, K13) is composed from bytes, never supplied by the caller.
UVT_MONITOR_PINS = {
    'binding': (C1 / 'DDO154_COLUMN_MEAN_REFERENCE_BINDING_V001.json', 'f42c7c657cd9b8bcef6b88e980918ff2570b1fc0a5480784d8bf3b8bb2a3c600'),
    'a2f10_result': (ROOT / 'CLAUDE2/runs/A2_ANCHOR_F10_RUN_V001/result.json', 'bcd2f64ec6c858a51718b2badb85b9e35121b6a3575227a4c9e4b8b5c673836e'),
    'prereg_v005': (EX / 'kmax_prereg_v005_c2/KMAX_MATRIX_PREREG_V005.json', 'dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174'),
}
UVT_REQUEST_SCHEMA = 'UNT_UV_TAIL_ROUTE_A_REQUEST_C2V001'
UVT_RECORD_SCHEMA = 'UNT_GALAXY_M0_FORWARD_UV_TAIL_C2V010'
UVT_PENDING_CERTIFICATE = 'PENDING_UV_TAIL_CERTIFICATE'  # template sentinel for an EPS/LO certificate not yet produced
UVT_TEST_ONLY = 'NONE_TEST_ONLY'  # the library's TEST_ONLY_CERT (checked against the library at normalization)
UVT_MT_THRESHOLD = 0.25  # design sec 1.7 (pre-named); the controller refuses any other value
UVT_TAIL_KINDS = ('reference', 'body', 'offset', 'columns_v001', 'rotation_v001', 'columns_v003', 'columns_v005', 'rotation_v005')
UVT_BINDING_KIND = {'reference': 'reference', 'body': 'body', 'offset': 'offset', 'columns_v001': 'fs_columns',
                    'rotation_v001': 'fs_rotation', 'columns_v003': 'rfs_columns', 'columns_v005': 'le_columns',
                    'rotation_v005': 'le_rotation'}
UVT_ARGV_NON_PATH = ('--uv-tail-truncation',)  # JSON-valued flag (route-B binding add_argv); never a path
# ---- C2V010 r4 (driver_r4): nodes_v001 (T2 only; TAIL_SCHEME_DESIGN_V002 sec 1.3 table; root V005 A50 item 11; C4T-D5).  Used
# ONLY when numerics.uv_tail.source_rule is nodes_v001 (tail_scheme_impl_c2/nodes_v001, BUILD_NODES_SUCCESSORS_C2V001 aad641c3db4dee18):
# route A = the nodes RO1 workers (RO1 c2v002 workers with the nodes controller), the nodes manifest writer, and the nodes
# successors of the eight route-B stage kinds (they refuse continuum_v001, which keeps SCRIPTS_UVT / AUX_UVT / RO1_ROUTE_A).
UVT_NODES = UVT / 'nodes_v001'
UVT_NODES_LIB = (UVT_NODES / 'lib/owned_uv_tail_nodes_v001.py', 'c8a04fb55f6c388c7cc5b735cb0e19222836c49acfce46d846198951593be551')
SCRIPTS_UVT_NODES = {
    'reference': (UVT_NODES / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/nodes_v001/route_b/stages/ddo_homotopy_reference_root_worker_v001_gal_c2v005_uvt_nodes_c2v001_r5.py', 'fba1576fe8d36a680d7a0a1019ba88a07a50c392a1e0f50b2f9e5ff3538f0ce0'),
    'body': (UVT_NODES / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/nodes_v001/route_b/stages/ddo_saved_root_body_array_root_v002_gal_c2v005_uvt_nodes_c2v001_r5.py', '1b289491a1d13d5e736d8f6640ca6fa548b883fc60511d1cfed1e11dfedba2dd'),
    'offset': (UVT_NODES / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/nodes_v001/route_b/stages/ddo_body_source_offset_root_v003_gal_c2v005_uvt_nodes_c2v001_r5.py', '2fc1337c0dacbdf4e30839f882623481f010794fde947ed08c6bc19798abe9ea'),
    'columns_v001': (UVT_NODES / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/nodes_v001/route_b/stages/ddo_fixed_K_free_surface_root_v001_gal_c2v005_uvt_nodes_c2v001_r5.py', '558c724a06b17c5c5968a9e9a7764e88baceda6e0f91556672e7bd160409496e'),
    'rotation_v001': (UVT_NODES / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/nodes_v001/route_b/stages/ddo_free_surface_rotation_root_v001_gal_c2v005_uvt_nodes_c2v001_r5.py', 'd5c144cd64fcd1c1a43c96d91fa3acac4b640b44a85c0959fcacd2216f0780fd'),
    'columns_v003': (UVT_NODES / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/nodes_v001/route_b/stages/ddo_fixed_K_free_surface_root_v003_gal_c2v005_uvt_nodes_c2v001_r5.py', '13f7e3255ce10e5b33d10461aa6c04d9fb34a9534663ff04769b4b49ea3a6a8a'),
    'columns_v005': (UVT_NODES / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/nodes_v001/route_b/stages/ddo_fixed_K_free_surface_root_v005_gal_c2v005_uvt_nodes_c2v001_r5.py', 'ccc5682f2599614df30a191336053ac5fe13c876924d31474769483c256243a9'),
    'rotation_v005': (UVT_NODES / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/nodes_v001/route_b/stages/ddo_free_surface_rotation_root_v005_gal_c2v005_uvt_nodes_c2v001_r5.py', '0e5f4723664bcfbaeadca24f85ea3d5250d2c13331aa326064f8f8211e1caf38'),
}
AUX_UVT_NODES = {
    'route_b_binding': (UVT_NODES / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/nodes_v001/route_b/uvt_route_b_binding_nodes_c2v001_r5.py', '1b5f3b4f961bedbf2f79e750989cdf79d44552ac1363f0e78639234d634df40b'),
    'controller': (UVT_NODES / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/nodes_v001/route_a/route_a_uv_tail_controller_nodes_c2v001_r5.py', 'e5a29a6773b2caff75c9494230b88de63dea7b58dab547cbc282d76b881b792b'),
    'facade': AUX_UVT['facade'], 'solver': AUX_UVT['solver'], 'solver_parallel': AUX_UVT['solver_parallel'],
    'manifest_writer': (UVT_NODES / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/nodes_v001/route_a/route_a_tail_manifest_nodes_c2v001_r5.py', 'e003fcb5c821defaa880414cb965043019c44c3076fa532da20c56b9bf8bcf62'),
}
NODES_ROUTE_A = {
    'worker': (UVT_NODES / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/nodes_v001/route_a/ddo_composite_stable_cached_root_worker_v002_uvtail_ro1_nodes_c2v001_r5.py', '0ae245d86ef4f28c9a348094cedca14e5b2f4e704a9c90905a167084ac88af15'),
    'worker_parallel': (UVT_NODES / '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/nodes_v001/route_a/ddo_composite_stable_cached_root_worker_v002_parallel_uvtail_ro1_nodes_c2v001_r5.py', 'a527717283f8234df6a562eae6a4f28d5c9d34abfbc08cd7cf3f18d7d5f903f2'),
    'binding': RO1_ROUTE_A['binding'],
}
# r4 (R5; root V005 A50 items 11-12): tail-OFF route A on the RO1 c2v002 workers (numerics.route_a.ro1_workers true).
UVT_RO1_OFF_REQUEST_SCHEMA = 'UNT_UV_TAIL_ROUTE_A_REQUEST_TAIL_OFF_RO1_C2V010R4'

# c2v005 wiring (stages2 report): module successors and the pin each consumer must carry (checked by binding_blockers).
MODULE_SUCCESSORS = {
    'reference_module': {'successor': AUX['reference_module'],
                         'base': (HC / 'owned_axisymmetric_homotopy_reference_v003.py', '81a04b1241c1004f8766f68d22f9c586824ae3b3cbe32ca36243a2d3da387128')},
    'body_base': {'successor': (S2MOD / 'owned_saved_root_body_base_v003_gal_c2v001.py', 'd540fd7c1a943e94355d273f4329e1f0d350dbcf8be5a2db22b82577d6d87329'),
                  'base': (HR / 'owned_saved_root_body_base_v003.py', 'c525ec711b7ebd1fc776299669fe9c2ed3e369a55f562f350a9e05ef6c5a0675')},
    'join': {'successor': (S2MOD / 'owned_free_surface_column_packet_join_v001_gal_c2v001.py', '0a7f53147365db21618a116c300f0bb87850024eb3cf15e1ac8bbd89786d2c25'),
             'base': (HC / 'owned_free_surface_column_packet_join_v001.py', 'c3d4e08bf108d4fff908d8c34af9c20b7f50d38d678a6d7f999df71c78c7d62b')},
}
PREP_V008_REVIEW = (ROOT / 'helpers/response_packet_audit/CURRENT_SOURCE_ALL_PANEL_DERIVATIVE_AUDIT_REVIEW_V001.json',
                    'aa12d69f4119983fdcfceb4809971ec08c596aeaf5630c85a51823b36332182e')
PREP_V007_MAX_AXIS_NODES = 80  # v007.py:130
PREP_V008_MAX_AXIS_NODES = 96  # v008.py:130
PREP_V009_MAX_AXIS_NODES = 120  # C2V009 (a): v009.py:130
# Grids > 80 nodes/axis are accepted ONLY if (breaks, panel_orders, total) equal one of the declared P-88 grids
# (KMAX_MATRIX_PREREG_V001.json d5acfc2f..., grids G3/G4/GR; specs/wave1 of calibration_prep_c2_0470/kmax_convergence).
_G2_BREAKS = [-2, -1, -0.3, -0.1, -0.03, -0.01, 0, 0.01, 0.03, 0.1, 0.3, 1, 2]
DECLARED_LARGE_GRIDS = {
    'G3': ([-3] + _G2_BREAKS + [3], [6] * 14, 84),
    'G4': ([-4, -3] + _G2_BREAKS + [3, 4], [6] * 16, 96),
    'GR': (list(_G2_BREAKS), [6] + [8] * 10 + [6], 92),
    # C2V009 (a): kmax-extension grids (prereg V005 decision rule 3 next step; prereg V006 grids G5/G6): G4 plus unit
    # outer panels of order 6 per side.
    'G5': ([-5, -4, -3] + _G2_BREAKS + [3, 4, 5], [6] * 18, 108),
    'G6': ([-6, -5, -4, -3] + _G2_BREAKS + [3, 4, 5, 6], [6] * 20, 120),
}
# C2V008 (a), verbatim from c2v003b/c2v003c: pinned inputs of the per-call DDO154 geometry derivation (read only when
# distance != registered).
GEOMETRY_PINS = {
    'calibration_input': (HR / 'DDO154_CURRENT_MODEL_CALIBRATION_INPUT_POPULATED_V001.json', '8fff3e433f932947c2725ac7fb769126abb87814e11eeb19723974485e98e5e7'),
    'stellar_3d': (C1 / 'GALAXY_STELLAR_3D_REFERENCE_SOURCE_V001.json', '612dc36529835e233fdda5810636ab8b99924fba9d0117b168aeeb9d1e2c449f'),
    'photometric': (HR / 'STELLAR_PHOTOMETRIC_REFERENCE_MEAN_PROFILE_V001.json', '2f31122d9f2a1e3a3a63560fcd20541e4dfcf235eefca966b2fed644702b8b6a'),
    'source_binding_v003': (C1 / 'GALAXY_PHYSICAL_SOURCE_STATE_BINDING_V003.json', '7cadac8b66096a9d9942e9861289a1d41bad084e13cd7ba655341eb06e6afae9'),
    'monotone_reducer': (HR / 'ddo_monotone_bernstein_source_controls_v002.py', '50edaba79af30cbc3582685861b55bb3eefdbe6fcb002ec1a4187b6913b4f83c'),
}
PROFILE_NAME = 'GALAXY_RADIAL_SOURCE_REFERENCE_V001.json'  # literal file name read by prep V007/V008 as C/PROFILE_NAME
# C2V008 (a): galaxy-config fields whose DDO154 value depends on the call distance, in the order derive_geometry produces
# them.  Each travels (PER_CALL) only to the stages that consume it (consumed_fields); none is consumed by columns/feedback.
GEOMETRY_CONFIG_FIELDS = ('source.profile', 'source.monotone_source', 'radial.outer_edge_kpc', 'observation.binding',
                          'observation.query_rows')
# Reviewed fixed stage arguments (not parameters).
FIXED_ARGS = {'wave_batch': '256', 'position_batch': '512', 'bessel_cache_entries': '500000',
              'mass_relative_tolerance': '1.1e-8'}

_ORIG = 'DDO154_'
GALAXIES = {
    'DDO154': {
        'supported': True,
        'base_seed': (C1 / 'DDO154_STABLE_CACHED_COUPLED_TRIAL_SEED_V002.json', '694eaaaab38547a369ac85c3c3d0b5550d8878753ccafe7bc0e5cdcb79be6680'),
        'profile': (C1 / 'GALAXY_RADIAL_SOURCE_REFERENCE_V001.json', 'f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b'),
        'monotone_source': (C1 / 'DDO154_MONOTONE_SOURCE_RECONSTRUCTION_RUN_V001/source.json', '1dbf2b687b8ef2747091557f3a92ebd4995409f326ec21df816f6c7397c11be2'),
        'column_mean_binding': (C1 / 'DDO154_COLUMN_MEAN_REFERENCE_BINDING_V001.json', 'f42c7c657cd9b8bcef6b88e980918ff2570b1fc0a5480784d8bf3b8bb2a3c600'),
        'solver_template': (C1 / 'DDO154_REMAINING_FREE_SURFACE_CONTROLS_V001.json', '5d69360f24fc1c943bdec1b24b2a1dd6e22670375118f344c4e66231df002d16'),
        'default_coefficients': (C1 / 'PROVISIONAL_L4_COEFFICIENT_FREEZE_V001/coefficients.npz', 'fe5a2f065dec8f120c573eeeb6edc0a24a945d2a0fd70e3f29a66cb986e53e4f'),
        'registered_geometry': {'distance_Mpc': 4.04, 'inclination_deg': 66.0, 'released_inclination_deg': 64.0,
                                'HI_original_distance_Mpc': 4.3},
        'n_columns': 72, 'n_queries': 12,
        'default_entropy_K_factor': 64 / 121,
        # Controls used by the saved chain, in the saved run order (reproduction, mode pinned_controls).
        'saved_controls': {
            'fs': [(C1 / 'DDO154_OUTER_FREE_SURFACE_CONTROLS_V001.json', 'f9f07c0ef0709c226b3346ecf38aedb3e3342ae7a4ed71d7f4018f40ff994dae'),
                   (C1 / 'DDO154_REMAINING_FREE_SURFACE_CONTROLS_V001.json', '5d69360f24fc1c943bdec1b24b2a1dd6e22670375118f344c4e66231df002d16'),
                   (C1 / 'DDO154_FREE_SURFACE_BRACKET_CORRECTION_CONTROLS_V001.json', '7719e7d8e35501fb1277973ddc53b3d75655646aaa60fc0705d32e891bc00f31')],
            'rfs': [(C1 / 'DDO154_REFRESHED_FREE_SURFACE_CONTROLS_V001.json', 'db835b143f735d9ebae74d28c99bfbd7e2f392b1554f78ed2e60a73989bb03ef'),
                    (C1 / 'DDO154_REFRESHED_OUTER_BRACKET_CORRECTION_CONTROLS_V001.json', '87eef1fd7454879e13ef05eb96ea9d727f8b3daa2a736efc1bae15132189c5ad')],
            'le': [[(C1 / 'DDO154_LOWER_ENTROPY_FREE_SURFACE_CONTROLS_V001.json', 'c2f8b434c0de06cf8bfeef0f202e8a8140c33a4b140dbf1a75ebffc4e83b4938')],
                   [(C1 / 'DDO154_LOWER_ENTROPY_REFRESHED_CONTROLS_V001.json', '24f404e64b4c514c9bd331ba711426faa53d5d77e3dfa3bf222a4d88262ff4b0')],
                   [(C1 / 'DDO154_LOWER_ENTROPY_REFRESHED_CONTROLS_V002.json', '7a4ac8e216ea71f3aee2db774a09fcc13089535f7206ffbf0d4ba41d2a73e54c')]]},
        # Saved run outputs of the chain (reproduction map; read-only).
        'saved_runs': {
            'route_a': {'attempt': C1 / 'DDO154_STABLE_CACHED_COUPLED_RUN_V002/attempt_000', 'checkpoint': C1 / 'DDO154_STABLE_CACHED_COUPLED_RUN_V002/checkpoint'},
            'reference': C1 / 'DDO154_NONCIRCULAR_REFERENCE_RUN_V001/reference',
            'body': C1 / 'DDO154_NORMALIZED_BODY_ARRAY_RUN_V001/body',
            'offset': C1 / 'DDO154_BODY_SOURCE_OFFSET_RUN_V001/offset',
            'fs_columns': [C1 / 'DDO154_OUTER_FREE_SURFACE_RUN_V001/columns', C1 / 'DDO154_REMAINING_FREE_SURFACE_RUN_V001/columns', C1 / 'DDO154_FREE_SURFACE_BRACKET_CORRECTION_RUN_V001/columns'],
            'fs_rotation': C1 / 'DDO154_FREE_SURFACE_ROTATION_RUN_V001/rotation',
            'fs_feedback': C1 / 'DDO154_FREE_SURFACE_NATIVE_FEEDBACK_RUN_V001/feedback',
            'rfs_columns': [C1 / 'DDO154_REFRESHED_FREE_SURFACE_RUN_V001/columns', C1 / 'DDO154_REFRESHED_OUTER_BRACKET_CORRECTION_RUN_V001/columns'],
            'le1_columns': [C1 / 'DDO154_LOWER_ENTROPY_FREE_SURFACE_RUN_V001/columns'],
            'le1_rotation': C1 / 'DDO154_LOWER_ENTROPY_ROTATION_RUN_V001/rotation',
            'le1_feedback': C1 / 'DDO154_LOWER_ENTROPY_NATIVE_FEEDBACK_RUN_V001/feedback',
            'le2_columns': [C1 / 'DDO154_LOWER_ENTROPY_REFRESHED_COLUMNS_RUN_V001/columns'],
            'le2_rotation': C1 / 'DDO154_LOWER_ENTROPY_REFRESHED_ROTATION_RUN_V001/rotation',
            'le2_feedback': C1 / 'DDO154_LOWER_ENTROPY_NATIVE_FEEDBACK_RUN_V002/feedback',
            'le3_columns': [C1 / 'DDO154_LOWER_ENTROPY_REFRESHED_COLUMNS_RUN_V002/columns'],
            'le3_rotation': C1 / 'DDO154_LOWER_ENTROPY_REFRESHED_ROTATION_RUN_V002/rotation',
            'le3_column_mean': C1 / 'DDO154_LOWER_ENTROPY_REFRESHED_COLUMN_MEAN_RUN_V002/observation',
        },
        # The two manual bracket corrections of the saved chain, written as declared rule overrides.
        'repro_rule_overrides': {
            'fs_absolute_overrides': {str(i): [302500000.0, 317625000.0] for i in (5, 6, 7, 8, 9, 45, 46, 47, 48, 49, 50)},
            'rfs_factor_overrides': {'71': [0.8, 1.01]}},
        'saved_reference_speeds_km_s': [11.582165247926024, 21.882993578802893, 29.132298352542904, 34.53811554072339,
                                        38.18655701048106, 41.43604462412697, 44.62663756340822, 47.756836739826575,
                                        49.19289920475613, 49.39790797958474, 50.909676339988216, 48.65527268393767],
    },
    'NGC3198': {
        # c2v002: route-A configuration via normalize_ngc_spec (NGC section).  c2v005: route B is configured from the
        # galaxy config (schema V003 NGC3198 entry; ROOT_DECISIONS N1/N2/N4, N3 slot) with route-A outputs admitted
        # from the NGC route-A lane (normalize_ngc_route_b_spec).  The values below are checked against the galaxy config.
        'supported': True,
        'route_b_mode': 'ADMITTED_ROUTE_A_OUTPUTS',
        'config': 'NGC3198_C2V002',
        'profile': (C1 / 'GALAXY_RADIAL_SOURCE_REFERENCE_V001.json', 'f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b'),
        'solver_template': (BIND / 'inputs/NGC3198_SOLVER_TEMPLATE_C2V005.json', 'ba5e87eb134d1c0b4edf85ca7c9653904dd2c16751e51283114e485d3acbfa13'),
        'registered_geometry': {'distance_Mpc': 13.8, 'inclination_deg': 72.0, 'released_inclination_deg': 73.0,
                                'HI_original_distance_Mpc': 13.8},
        'n_columns': 100, 'n_queries': 43,
        'n_columns_by_member': {None: 100, 'GL10_ALTERNATIVE': 250},  # c2v006: schema V004 ngc3198 / ngc3198_gl10_alternative
        'default_entropy_K_factor': 64 / 121,
        # c2v006 (D6): the NGC entropy factor is the N4 primary 64/121 or the declared N4 original-K alternative 1.0 only.
        'entropy_K_members': {64 / 121: 'N4_PRIMARY_64_OVER_121', 1.0: 'N4_DECLARED_ALTERNATIVE_ORIGINAL_K_NOT_HEADLINE'},
        # c2v006 (D1 message): fe5a2f06 is the V004 provisional L4 grid, hard-coded as NGC prep v001's default (prep:19-20);
        # it is NOT "the NGC route-A grid".  The route-A lane injects the A2 grid by a module patch on the prep.
        'default_coefficients': (C1 / 'PROVISIONAL_L4_COEFFICIENT_FREEZE_V001/coefficients.npz', 'fe5a2f065dec8f120c573eeeb6edc0a24a945d2a0fd70e3f29a66cb986e53e4f'),
        # c2v006 (A5): decided coefficient grids a route-B call may name; the call grid must ALSO equal the route-A seed's.
        'decided_coefficient_grids': {
            'fe5a2f065dec8f120c573eeeb6edc0a24a945d2a0fd70e3f29a66cb986e53e4f': (C1 / 'PROVISIONAL_L4_COEFFICIENT_FREEZE_V001/coefficients.npz',
                                                                                  'V004 provisional L4 grid; NGC prep v001 default (prep:19-20)'),
            '2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7': (ROOT / 'CLAUDE2/CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz',
                                                                                  'ROOT_DECISIONS_A1_A2 A2 4-chain pooled grid (provisional)')},
        # c2v006 (D3, A3): the only admissible N3 monotone source: the reviewed reducer V003 output, exceptions {23}.
        'monotone_source_pin': (EX / 'ngc_route_impl_c2/reducer/NGC3198_SEGMENT_MONOTONE_SOURCE_TRUNCATED_RUN_V001/source.json',
                                '746980f2b602ddbc17d862a815f0213ee0c4efea9f4cbf027ef0b0a1b0fd31e1'),
        'column_mean_binding': (BIND6 / 'inputs/NGC3198_COLUMN_MEAN_REFERENCE_BINDING_C2V006.json', '83dda7757aa5ebc81ff193fe220992f5659d1cfe59dda1483574c17bf43c9096'),
        'saved_controls': {}, 'saved_runs': {}, 'repro_rule_overrides': {},
        'blockers': [
            'c2v006: route B is bound (gal_c2v004 successors, schema V004, A4 fields decided). The only remaining refusals are '
            'those that need the NGC route-A run bytes (listed by the route-B dry run as PENDING_ROUTE_A_OUTPUTS).',
        ],
    },
}
LE_RULE_DEFAULTS = {'fs_absolute_overrides': {}, 'rfs_factors': [0.8, 1.2], 'rfs_factor_overrides': {},
                    'le_first_factors': [0.4, 0.9], 'le_next_factors': [0.8, 1.1], 'le_factor_overrides': {}}


# ----------------------------------------------------------------------------- small helpers
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)


def _is_hex64(s):
    return isinstance(s, str) and len(s) == 64 and all(c in '0123456789abcdef' for c in s)


class Refusal(ValueError):
    pass


class StageFailed(RuntimeError):
    pass


class Blocked(RuntimeError):
    pass


class RouteANoFixedPoint(RuntimeError):
    """C2V007 (a) F1, from c2v003c (RD1 F1): the route-A stage returned normally (exit 0, RETURNED_ACTUAL_RESULT) but its own
    result.json records no finite source fixed point (FAILED_SOURCE_PREPARATION, ITERATION_BUDGET_EXHAUSTED, ...).
    A model outcome at this parameter point, NOT a tooling gap; carries the classification record.  (Solver/prediction
    errors that RAISE instead of returning end in the worker's failure.json with a nonzero exit, i.e. FAILED_AT_STAGE;
    so do parallel-pool failures, ColumnPoolError.)"""

    def __init__(self, message, record):
        RuntimeError.__init__(self, message)
        self.record = record


def verify_pin(path, sha, label):
    p = Path(path)
    if not p.is_file():
        raise Refusal('%s missing: %s' % (label, p))
    actual = sha256_file(p)
    if actual != sha:
        raise Refusal('%s pin mismatch: %s expected %s actual %s' % (label, p, sha, actual))
    return actual


def exec_verified(path, sha, name):
    """Execute a pinned module from the exact bytes that were hashed (no reread)."""
    import types
    raw = Path(path).read_bytes()
    if sha256_bytes(raw) != sha:
        raise Refusal('Pin mismatch on load: %s' % path)
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), module.__dict__)
    return module


def _jsonable(v):
    if isinstance(v, Path):
        return str(v)
    if isinstance(v, dict):
        return {str(k): _jsonable(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_jsonable(x) for x in v]
    if hasattr(v, 'tolist'):
        return _jsonable(v.tolist())
    if isinstance(v, float) and not math.isfinite(v):
        return repr(v)
    return v


def _write_x(path, obj):
    with open(path, 'x') as f:
        json.dump(_jsonable(obj), f, indent=1, allow_nan=False)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())
    return sha256_file(path)


def single_thread_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
    for k in THREAD_ENV:
        env[k] = '1'
    return env


# ----------------------------------------------------------------------------- truncation mask
def truncation_mask(k_physical, shape, kmax_inverse_m):
    """0/1 weight mask on the EXISTING composite grid nodes (numerical choice, not physics).
    cube: all ones (identity; the driver then installs no hook at all).
    sphere: keep |k| <= kmax.  cylinder: keep k_perp = sqrt(kx^2+ky^2) <= kmax (disk axis = chart z),
    all k_z of the cube kept.  Both masks are invariant under k -> -k, so real fields stay real.
    Zeroing a node's weight is exactly zeroing its weighted response row, because the reviewed
    prepare() forms weighted_response = dk_weight/(2pi)^3 * x_tilde node by node.
    Scope (CHECK_V001 s3 corr. 1): route A, reference and body run UNMASKED (cube G4), so under
    sphere/cylinder the offset stage's real-space total (body full_fields + inverse(masked offset)),
    its reality/lapse/C-eigenvalue guards and the stored updated_base_arrays full_fields_complex,
    Phi0, angular_forcing_dPhi, base_residual_r0 are a MIXED field (cube G4 + masked offset).
    Downstream stages read only radial_nodes_m, K0, Sigma, RdR weights from that file; every
    Fourier packet they consume is masked consistently.  Constraint (s3 corr. 3): the cache
    module's evaluate() calls its closure-local prepare, bypassing the wrapper; only prepare()
    may be relied on (true for offset V003)."""
    import numpy as np
    k = np.asarray(k_physical, dtype=float)
    if k.ndim != 2 or k.shape[1] != 3 or not np.isfinite(k).all():
        raise ValueError('k nodes (n,3) finite required')
    if shape == 'cube':
        return np.ones(len(k))
    if not (isinstance(kmax_inverse_m, float) and math.isfinite(kmax_inverse_m) and kmax_inverse_m > 0):
        raise ValueError('positive finite kmax required for a non-cube mask')
    if shape == 'sphere':
        r = np.sqrt(k[:, 0] * k[:, 0] + k[:, 1] * k[:, 1] + k[:, 2] * k[:, 2])
    elif shape == 'cylinder':
        r = np.sqrt(k[:, 0] * k[:, 0] + k[:, 1] * k[:, 1])
    else:
        raise ValueError('shape must be cube, sphere or cylinder')
    return (r <= kmax_inverse_m).astype(float)


def apply_mask(weighted_responses, mask):
    import numpy as np
    a = np.asarray(weighted_responses)
    if a.ndim < 1 or a.shape[0] != len(mask):
        raise ValueError('mask/packet length mismatch')
    return a * np.asarray(mask, dtype=float).reshape((len(mask),) + (1,) * (a.ndim - 1))


def mask_fired_check(offset_dir, shape, kmax_inverse_m):
    """c2v003 (CHECK_V001 s3 corr. 2): evidence that the mask fired.  Recompute the mask from the
    stored wavevectors of unit_response.npz and offset_prepared.npz and require every row outside
    it to be exactly 0.  Raises StageFailed('MASK_NOT_FIRED ...') otherwise; returns the record."""
    import numpy as np
    rec = {'shape': shape, 'kmax_inverse_m': kmax_inverse_m, 'files': {}}
    axis_waves = None
    for name in ('unit_response.npz', 'offset_prepared.npz'):
        p = Path(offset_dir) / name
        if not p.is_file():
            raise StageFailed('MASK_NOT_FIRED: %s missing' % p)
        with np.load(p, allow_pickle=False) as f:
            w = f['wavevectors'].copy()
            r = f['weighted_responses'].copy()
        if r.ndim < 1 or r.shape[0] != len(w):
            raise StageFailed('MASK_NOT_FIRED: %s rows %s != nodes %d' % (name, r.shape, len(w)))
        if axis_waves is None:
            axis_waves = w
        elif not np.array_equal(axis_waves, w):
            raise StageFailed('MASK_NOT_FIRED: wavevectors differ between offset npz files')
        m = truncation_mask(w, shape, kmax_inverse_m)
        out = m == 0
        flat = r.reshape(len(r), -1)
        bad = int(np.count_nonzero(np.any(flat[out] != 0, axis=1)))
        kept_zero = int(np.count_nonzero(~np.any(flat[~out] != 0, axis=1)))
        rec['files'][name] = {'sha256': sha256_file(p), 'total_nodes': int(len(m)), 'kept_nodes': int(m.sum()),
                              'outside_rows': int(out.sum()), 'outside_rows_nonzero': bad, 'kept_rows_all_zero': kept_zero}
        if bad:
            raise StageFailed('MASK_NOT_FIRED: %s has %d nonzero rows outside the %s mask (kept %d of %d nodes)'
                              % (name, bad, shape, int(m.sum()), len(m)))
    rec['kept_nodes'] = rec['files']['unit_response.npz']['kept_nodes']
    rec['total_nodes'] = rec['files']['unit_response.npz']['total_nodes']
    rec['vacuous'] = rec['kept_nodes'] == rec['total_nodes']
    rec['status'] = 'MASK_FIRED_OUTSIDE_ROWS_EXACTLY_ZERO'
    return rec


# ----------------------------------------------------------------------------- _stage shim
def _decode_value(v):
    if isinstance(v, dict) and len(v) == 1:
        (key, val), = v.items()
        if key == '__path__':
            return Path(val)
        if key == '__pathdict__':
            return {Path(p): s for p, s in val}
        if key == '__ordered__':
            return {p: s for p, s in val}
    return v


def _install_hooks(request):
    """Wrap importlib.util.spec_from_file_location so that the listed dependency modules get
    their identity globals replaced (after their own code ran) and, for a non-cube truncation,
    the mask wrappers.  Every patched file is re-verified from bytes."""
    import importlib.util
    patches = {str(Path(p['path']).resolve()): p for p in request.get('module_patches', [])}
    mask = request.get('mask')
    targets = dict(patches)
    if mask:
        for key in ('checkpoint_module', 'cache_module'):
            targets.setdefault(str(Path(mask[key][0]).resolve()), {'path': mask[key][0], 'sha256': mask[key][1], 'set': {}})
    original = importlib.util.spec_from_file_location

    class PatchedLoader:
        def __init__(self, inner, key):
            self.inner = inner
            self.key = key

        def create_module(self, spec):
            return self.inner.create_module(spec)

        def exec_module(self, module):
            patch = targets[self.key]
            if sha256_file(self.key) != patch['sha256']:
                raise ValueError('Patched dependency pin mismatch: ' + self.key)
            self.inner.exec_module(module)
            for name, value in patch.get('set', {}).items():
                if not hasattr(module, name):
                    raise ValueError('Override target absent: %s.%s' % (self.key, name))
                setattr(module, name, _decode_value(value))
            if mask and self.key == str(Path(mask['checkpoint_module'][0]).resolve()):
                _wrap_checkpoint_get(module, mask)
            if mask and self.key == str(Path(mask['cache_module'][0]).resolve()):
                _wrap_cache(module, mask)

    def hooked(name, location=None, *args, **kwargs):
        spec = original(name, location, *args, **kwargs)
        if spec is not None and location is not None:
            key = str(Path(location).resolve())
            if key in targets:
                spec.loader = PatchedLoader(spec.loader, key)
        return spec

    importlib.util.spec_from_file_location = hooked


def _wrap_checkpoint_get(module, mask):
    orig = module._get
    state = {}

    def _get(directory, ref):
        a = orig(directory, ref)
        if isinstance(ref, dict) and ref.get('file_sha256') == mask['g4_file_sha256']:
            if directory not in state:
                waves = orig(directory, mask['waves_ref'])
                state[directory] = truncation_mask(waves, mask['shape'], mask['kmax_inverse_m'])
            a = apply_mask(a, state[directory])
        return a
    module._get = _get


def _wrap_cache(module, mask):
    orig_make = module.make_fourier_module

    def make_fourier_module(**kw):
        inner = orig_make(**kw)
        orig_prepare = inner.prepare

        def prepare(**arguments):
            out = orig_prepare(**arguments)
            m = truncation_mask(arguments['k_physical'], mask['shape'], mask['kmax_inverse_m'])
            out = dict(out)
            out['weighted_responses'] = apply_mask(out['weighted_responses'], m)
            out['truncation_mask'] = {'shape': mask['shape'], 'kmax_inverse_m': mask['kmax_inverse_m'],
                                      'kept_nodes': int(m.sum()), 'total_nodes': int(len(m))}
            return out
        inner.prepare = prepare
        return inner
    module.make_fourier_module = make_fourier_module


def stage_main(request_path):
    request = json.loads(Path(request_path).read_text())
    script, sha = request['script'], request['script_sha256']
    _install_hooks(request)
    module = exec_verified(script, sha, 'c2v001_stage_' + Path(script).stem)
    for name, value in request.get('stage_globals', {}).items():
        if name not in module.__dict__:
            raise ValueError('Stage override target absent: ' + name)
        module.__dict__[name] = _decode_value(value)
    # c2v003: replace single (path, sha) entries of a dict global (route-A LOCAL['prep'] only).
    for gname, items in request.get('stage_dict_items', {}).items():
        target = module.__dict__.get(gname)
        if not isinstance(target, dict):
            raise ValueError('Stage dict override target absent: ' + gname)
        for key, pin in items.items():
            old = target.get(key)
            if not (isinstance(old, tuple) and len(old) == 2):
                raise ValueError('Stage dict override entry absent: %s[%s]' % (gname, key))
            if sha256_file(pin['path']) != pin['sha256']:
                raise ValueError('Stage dict override pin mismatch: ' + pin['path'])
            target[key] = (Path(pin['path']), pin['sha256'])
    sys.argv = [script] + list(request['argv'])
    module.main()
    return 0


# ----------------------------------------------------------------------------- call spec
def _num(x, label, positive=True):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(float(x)):
        raise Refusal(label + ' must be a finite number')
    x = float(x)
    if positive and x <= 0:
        raise Refusal(label + ' must be > 0')
    return x


def _strict(d, allowed, label):
    if not isinstance(d, dict):
        raise Refusal(label + ' must be an object')
    extra = set(d) - set(allowed)
    if extra:
        raise Refusal('%s: unknown keys %s' % (label, sorted(extra)))


def _abs(path, label):
    """c2v003 (CHECK_V001 further defect 3): spec paths must be absolute (stages run with cwd=stage dir)."""
    if not isinstance(path, str) or not Path(path).is_absolute():
        raise Refusal('%s must be an absolute path: %r' % (label, path))
    return path


def _canon_key(key):
    """C2V007 (a) F3, from c2v003c (RD1 F3): an override key is accepted only in the exact form the lookups use (str(int)):
    ASCII '0' or [1-9][0-9]*.  str.isdigit() also accepted '05', '071', Arabic-Indic and superscript digits,
    which were then silently not applied (or raised a bare ValueError)."""
    import re
    return isinstance(key, str) and re.fullmatch('0|[1-9][0-9]*', key) is not None


def normalize_route_a_numerics(ra):
    """C2V007 (b): numerics.route_a = {column_workers: N}, N an int (not bool) in 1..ROUTE_A_COLUMN_WORKERS_MAX.
    N = 1 is the reviewed serial worker + reviewed solver (exactly the c2v006 request); N > 1 the parallel successors."""
    _strict(ra, ('column_workers', 'max_iterations', 'seed_source_rtol_factor', 'ro1_workers'), 'numerics.route_a')  # C2V009 (b), RO1 AMB-14, r4 R5
    n = ra.get('column_workers', 1)
    if type(n) is not int or not 1 <= n <= ROUTE_A_COLUMN_WORKERS_MAX:
        raise Refusal('numerics.route_a.column_workers must be an int in 1..%d, not %r' % (ROUTE_A_COLUMN_WORKERS_MAX, n))
    out = {'column_workers': n}
    if 'max_iterations' in ra:  # C2V009 (b): present only when declared (absent -> exactly the c2v008 normalization)
        m = ra['max_iterations']
        if type(m) is not int or not 1 <= m <= ROUTE_A_MAX_ITERATIONS_MAX:
            raise Refusal('numerics.route_a.max_iterations must be an int in 1..%d, not %r' % (ROUTE_A_MAX_ITERATIONS_MAX, m))
        out['max_iterations'] = m
    if 'seed_source_rtol_factor' in ra:  # RO1 AMB-14: present only when declared (absent -> exactly the v009-EXT normalization)
        f = ra['seed_source_rtol_factor']
        if isinstance(f, bool) or not isinstance(f, (int, float)) or not math.isfinite(f) or not 0 < f <= 1:
            raise Refusal('numerics.route_a.seed_source_rtol_factor must be a finite number in (0, 1], not %r' % (f,))
        out['seed_source_rtol_factor'] = float(f)
    if 'ro1_workers' in ra:  # C2V010 r4 (R5; A50 items 11-12): present only when declared; only true is meaningful
        if ra['ro1_workers'] is not True:
            raise Refusal('numerics.route_a.ro1_workers must be true when declared (absent = the v009 workers), not %r' % (ra['ro1_workers'],))
        out['ro1_workers'] = True
    return out


def route_a_column_workers(nspec):
    """C2V007 (b): the route-A column worker count of a normalized spec (absent -> 1, the reviewed serial path)."""
    return ((nspec.get('numerics') or {}).get('route_a') or {}).get('column_workers', 1)


# ----------------------------------------------------------------------------- C2V010 (u) uv_tail helpers
_UVT_LOADED = {}


def uvt_library():
    """C2V010: the pinned tail library, executed from its verified bytes (inert: definitions only)."""
    if 'lib' not in _UVT_LOADED:
        lib = exec_verified(UVT_LIB['lib'][0], UVT_LIB['lib'][1], 'c2v010_uvt_lib')
        if lib.TEST_ONLY_CERT != UVT_TEST_ONLY or lib.KPC_M != KPC_M or lib.PROVIDER_SHA256 != UVT_LIB['provider'][1]:
            raise Refusal('UV_TAIL_LIBRARY_CONSTANTS differ from the driver (TEST_ONLY_CERT, KPC_M, provider pin)')
        _UVT_LOADED['lib'] = lib
    return _UVT_LOADED['lib']


def normalize_uv_tail(raw, ngc=False):
    """C2V010: numerics.uv_tail = the tail library's configuration object (UNT_UV_TAIL_CONFIG_C2V001; strict keys, checked by
    the pinned library's own normalize_config).  enabled must be true: a tail-OFF call omits the block (root A45 N3: in tail-OFF
    mode v010 constructs no TailBoundary).  source_rule continuum_v001, or (r4) nodes_v001 with a composite ext_grid object (T2 only;
    DDO154; the nodes successors; ext grid checked at planning).  eps_/lo_certificate: {path, sha256} (verified from
    bytes at planning and at every build), NONE_TEST_ONLY (admitted only when every stage domain is empty, uvt_plan), or the
    template sentinel PENDING_UV_TAIL_CERTIFICATE (planning only; run mode BLOCKED, class PENDING_UV_TAIL_CERTIFICATE)."""
    if not isinstance(raw, dict):
        raise Refusal('numerics.uv_tail must be an object (the tail library configuration)')
    if raw.get('enabled') is not True:
        raise Refusal('numerics.uv_tail.enabled must be true; omit numerics.uv_tail for a tail-OFF call (A45 N3)')
    info = uvt_info(raw)
    sr = uvt_config(info)['source_rule']
    if sr != 'continuum_v001':  # C2V010 r4 (R2): nodes_v001 is built (T2 only); its ext grid is checked at planning (uvt_plan)
        if not isinstance(sr.get('ext_grid'), dict):
            raise Refusal('UV_TAIL_NODES_V001_EXT_GRID_INVALID: source_rule.ext_grid must be a composite grid spec object, not %r'
                          % (sr.get('ext_grid'),))
        if ngc:
            raise Refusal('UV_TAIL_NODES_V001_DDO154_ONLY: the nodes_v001 successors bind DDO154 (T2 C4T-D5)')
    # the normalized spec carries the library configuration itself (canonical JSON), the object the V007 compare registers
    # and normalizes with the pinned library (v007_compare_c2 FIELDS: normalized_spec/numerics/uv_tail)
    return json.loads(canonical(raw))


def uvt_info(raw):
    """C2V010: the planning record of a normalized numerics.uv_tail: {config (the library config), config_sha256 (the
    library-normalized sha; None while a certificate is the pending sentinel), pending_certificates, test_only_certificates}."""
    pending = sorted(k for k in ('eps_certificate', 'lo_certificate') if raw.get(k) == UVT_PENDING_CERTIFICATE)
    cfg = uvt_config({'config': raw, 'pending_certificates': pending})
    test_only = sorted(k for k in ('eps_certificate', 'lo_certificate') if k not in pending and cfg[k] == UVT_TEST_ONLY)
    return {'config': json.loads(canonical(raw)), 'config_sha256': None if pending else cfg['sha256'],
            'pending_certificates': pending, 'test_only_certificates': test_only}


def uvt_config(nuv):
    """C2V010: the library-normalized config (a pending certificate sentinel replaced by NONE_TEST_ONLY for validation only)."""
    lib = uvt_library()
    probe = dict(nuv['config'])
    for k in nuv['pending_certificates']:
        probe[k] = UVT_TEST_ONLY
    try:
        return lib.normalize_config(probe)
    except ValueError as exc:
        raise Refusal('numerics.uv_tail: %s' % exc)


def uvt_is_nodes(raw):
    """C2V010 r4: True when a numerics.uv_tail block (raw or normalized) declares source_rule nodes_v001."""
    sr = (raw or {}).get('source_rule') if isinstance(raw, dict) else None
    return isinstance(sr, dict) and sr.get('rule') == 'nodes_v001'


def uvt_active(nodes):
    """C2V010 r4: the active tail-ON tables (scripts, aux, route-A workers): nodes_v001 -> the nodes successors; else r3's."""
    if nodes:
        return {'scripts': SCRIPTS_UVT_NODES, 'aux': AUX_UVT_NODES, 'route_a': NODES_ROUTE_A, 'lib_extra': {'nodes': UVT_NODES_LIB}}
    return {'scripts': SCRIPTS_UVT, 'aux': AUX_UVT, 'route_a': RO1_ROUTE_A, 'lib_extra': {}}


def uvt_nodes_library():
    """C2V010 r4: the pinned nodes_v001 library (inert: definitions only), for the planning-time ext-grid check."""
    if 'nodes' not in _UVT_LOADED:
        _UVT_LOADED['nodes'] = exec_verified(UVT_NODES_LIB[0], UVT_NODES_LIB[1], 'c2v010r4_uvt_nodes_lib')
    return _UVT_LOADED['nodes']


def ro1_off_request():
    """C2V010 r4 (R5): the tail-disabled route-A request of a ro1_workers call (the RO1 worker CLI requires one; enabled false ->
    the RO1 binding receives uv_tail=None and executes the reviewed statements; the controller is never constructed)."""
    return {'schema': UVT_RO1_OFF_REQUEST_SCHEMA, 'uv_tail': {'enabled': False, 'eps_certificate': UVT_TEST_ONLY, 'lo_certificate': UVT_TEST_ONLY},
            'note': 'tail OFF on the RO1 c2v002 workers (root V005 A50 items 11-12): RO1 armed, no UV-tail arithmetic'}


def ro1_off_pins():
    """C2V010 r4 (R5): the code a ro1_workers tail-OFF route A loads (RO1 workers + binding, the uvtail facade, the controller module the
    RO1 worker loads and pin-checks, the module-lane library it pins), verified from bytes."""
    pins = {}
    for label, (path, s) in (('RO1 worker', RO1_ROUTE_A['worker']), ('RO1 worker_parallel', RO1_ROUTE_A['worker_parallel']),
                             ('RO1 binding', RO1_ROUTE_A['binding']), ('uvt facade', AUX_UVT['facade']), ('uvt controller', AUX_UVT['controller']),
                             ('uvt lib', UVT_LIB['lib']), ('uvt roster', UVT_LIB['roster']), ('uvt provider', UVT_LIB['provider'])):
        pins[str(path)] = verify_pin(path, s, 'ro1_workers ' + label)
    return pins


def ro1_off_blockers():
    """C2V010 r4 (R5): the RO1 workers pin the RO1 c2v002 binding, the uvtail facade and the controller (bytes)."""
    out = []
    for key in ('worker', 'worker_parallel'):
        try:
            verify_pin(RO1_ROUTE_A[key][0], RO1_ROUTE_A[key][1], 'RO1 ' + key)
        except Refusal as exc:
            out.append('RO1_OFF_PIN: %s' % exc); continue
        t = Path(RO1_ROUTE_A[key][0]).read_text()
        for need in (RO1_ROUTE_A['binding'][1], AUX_UVT['facade'][1], AUX_UVT['controller'][1]):
            if need not in t:
                out.append('RO1_OFF_WORKER_PIN: %s does not pin %s' % (Path(RO1_ROUTE_A[key][0]).name, need[:16]))
    return out


def route_a_ro1_workers(nspec):
    """C2V010 r4 (R5): numerics.route_a.ro1_workers of a normalized spec (absent -> False, the v009 workers)."""
    return bool(((nspec.get('numerics') or {}).get('route_a') or {}).get('ro1_workers', False))


def uvt_route_a_monitor(ni):
    """C2V010: the route-A tail-source monitor M_T (design sec 1.7, K13; R1 L1 E^A): the 12 column-mean binding row radii,
    the seed's source azimuths, v_ref = the A2F10 route-A row speeds (a forward-model output) and tau_i of prereg V005,
    threshold 1/4 -- composed from pinned bytes."""
    b = _pinned_json(UVT_MONITOR_PINS['binding'][0], UVT_MONITOR_PINS['binding'][1], 'uv_tail monitor binding')
    a2 = _pinned_json(UVT_MONITOR_PINS['a2f10_result'][0], UVT_MONITOR_PINS['a2f10_result'][1], 'uv_tail monitor A2F10 result')
    v5 = _pinned_json(UVT_MONITOR_PINS['prereg_v005'][0], UVT_MONITOR_PINS['prereg_v005'][1], 'uv_tail monitor prereg V005')
    R = [q['radius_m'] for q in b['query_rows']]
    v = [x['speed_km_s'] for x in a2['identity']['route_a']['route_a_rows']]
    tau = [float(t) for t in v5['tau_km_s']]
    n = ni['source_azimuth_count']
    if not (len(R) == len(v) == len(tau) == 12) or type(n) is not int or n < 4:
        raise Refusal('UV_TAIL_MONITOR_INPUTS: %d radii, %d v_ref, %d tau, azimuths %r' % (len(R), len(v), len(tau), n))
    return {'probe_R_m': R, 'probe_phi_rad': [2 * math.pi * j / n for j in range(n)], 'v_ref_km_s': v, 'tau_km_s': tau,
            'threshold': UVT_MT_THRESHOLD,
            'provenance': {'probe_R_m': {'path': str(UVT_MONITOR_PINS['binding'][0]), 'sha256': UVT_MONITOR_PINS['binding'][1], 'field': 'query_rows[].radius_m'},
                           'v_ref_km_s': {'path': str(UVT_MONITOR_PINS['a2f10_result'][0]), 'sha256': UVT_MONITOR_PINS['a2f10_result'][1],
                                          'field': 'identity.route_a.route_a_rows[].speed_km_s'},
                           'tau_km_s': {'path': str(UVT_MONITOR_PINS['prereg_v005'][0]), 'sha256': UVT_MONITOR_PINS['prereg_v005'][1], 'field': 'tau_km_s'},
                           'probe_phi_rad': 'the %d route-A column azimuths 2 pi j / %d (seed source_azimuth_count)' % (n, n)}}


def uvt_prep_patches(coeff_default, coeff_path, coeff_sha, geo, prep_path, prep_sha):
    """C2V010: the route-A prep module patch exactly as execute_chain builds it for a computed route A (the manifest stage
    re-runs the same prep, so it receives the same patch and the same LOCAL['prep'] dict item)."""
    prep_set = {}
    if not coeff_default:
        prep_set.update({'COEFFICIENT': {'__path__': coeff_path}, 'COEFFICIENT_SHA': coeff_sha})
    if geo is not None:
        prep_set['C'] = {'__path__': geo['C_dir']}
    return [{'path': str(prep_path), 'sha256': prep_sha, 'set': prep_set}] if prep_set else []


def uvt_plan(ctx, sp, ni, refuse, prep_patches):
    """C2V010: tail-ON planning, before route A.  Per-stage kept regions C (design sec 1.1, the library's kept_region; route A,
    reference, body: cube K; offset, columns, rotations: the call truncation) and whether each omitted domain D = O \\ C is
    empty; certificate custody (rule UVT_TEST_ONLY_EMPTY_DOMAIN: NONE_TEST_ONLY certificates only when EVERY stage domain is
    empty -- the identity gate B1 -- and then route A runs with admissibility test_only and the route-B successors receive
    --uv-tail-admit-test-only, recorded); the route-B config file (the spec's library config) and the route-A request
    (UNT_UV_TAIL_ROUTE_A_REQUEST_C2V001: config, admissibility, monitor).  Pending certificates: nothing is written."""
    lib = uvt_library()
    nuv = uvt_info(sp['numerics']['uv_tail'])
    if ni['kpc_m'] != lib.KPC_M:
        raise Refusal('UV_TAIL_UNITS: seed kpc_m differs from the tail library KPC_M')
    K_m = float(ni['composite_grid_spec']['breaks_inverse_kpc'][-1]) / KPC_M
    cfg = uvt_config(nuv)
    tr = sp['numerics']['truncation']
    trunc = None if tr['shape'] == 'cube' else {'shape': tr['shape'], 'kmax_inverse_kpc': tr['kmax_inverse_kpc']}
    kept = {}
    for kind in ('route_a',) + UVT_TAIL_KINDS:
        bk = 'route_a' if kind == 'route_a' else UVT_BINDING_KIND[kind]
        try:
            k = lib.kept_region(bk, trunc, K_m)
        except ValueError as exc:
            raise Refusal('numerics.uv_tail kept region (%s): %s' % (bk, exc))
        kept[kind] = {'binding_kind': bk, 'kept': k, 'domain_empty': bool(lib.domain_is_empty(k, cfg['outer']))}
    nodes = uvt_is_nodes(nuv['config'])  # C2V010 r4 (R2): nodes_v001 -- D = G_ext \\ G_K for every stage (never empty), cubes only
    nodes_ctx = None
    if nodes:
        bad = sorted(k for k, v in kept.items() if v['kept'].get('shape') != 'cube')
        if bad:
            raise Refusal('UV_TAIL_NODES_V001_REQUIRES_CUBE_KEPT: stage kept regions %s are not the cube (truncation %r)' % (bad, tr))
        try:
            nodes_ctx = uvt_nodes_library().ext_context(ext_spec=nuv['config']['source_rule']['ext_grid'],
                                                        kept_spec=ni.get('composite_grid_spec'), kpc_m=ni['kpc_m'])['record']
        except ValueError as exc:
            raise Refusal('UV_TAIL_NODES_V001_EXT_GRID_INVALID: %s' % exc)
        for v in kept.values():
            v['domain_empty'] = nodes_ctx['n_ext_nodes'] == 0
            v['domain_rule'] = 'nodes_v001: D = G_ext \\ G_K (%d extra nodes)' % nodes_ctx['n_ext_nodes']
    act = uvt_active(nodes)
    empty_all = all(v['domain_empty'] for v in kept.values())
    if nuv['test_only_certificates'] and not empty_all:
        raise Refusal('UVT_TEST_ONLY_REQUIRES_EMPTY_DOMAIN: NONE_TEST_ONLY certificates %s are admitted only when every stage '
                      'domain D = O \\ C is empty (identity gate B1); non-empty: %s'
                      % (nuv['test_only_certificates'], sorted(k for k, v in kept.items() if not v['domain_empty'])))
    admissibility = 'test_only' if nuv['test_only_certificates'] else 'production'
    certs = {}
    for k in ('eps_certificate', 'lo_certificate'):
        c = nuv['config'][k]
        if k in nuv['pending_certificates']:
            certs[k] = ['%s(%s.path)' % (UVT_PENDING_CERTIFICATE, k), '%s(%s.sha256)' % (UVT_PENDING_CERTIFICATE, k)]
            refuse('uv_tail.' + k, 'PENDING_UV_TAIL_CERTIFICATE',
                   '%s is the template sentinel %s: gate %s (design sec 1.5/1.6) has not produced its certificate; the filled '
                   'spec replaces exactly this entry by {path, sha256}' % (k, UVT_PENDING_CERTIFICATE, 'EPS' if k.startswith('eps') else 'LO'))
        elif c == UVT_TEST_ONLY:
            certs[k] = [UVT_TEST_ONLY, UVT_TEST_ONLY]
        else:
            certs[k] = [str(c['path']), verify_pin(c['path'], c['sha256'], 'uv_tail ' + k)]
    monitor = uvt_route_a_monitor(ni)
    request = {'schema': UVT_REQUEST_SCHEMA, 'uv_tail': nuv['config'], 'admissibility': admissibility, 'monitor': monitor}
    written = not nuv['pending_certificates']
    if written:
        cfg_p, cfg_s = ctx.write_input('uv_tail_config.json', nuv['config'])
        req_p, req_s = ctx.write_input('uv_tail_route_a_request.json', request)
    else:
        cfg_p = ctx.out / 'inputs' / 'uv_tail_config.json'
        req_p = ctx.out / 'inputs' / 'uv_tail_route_a_request.json'
        cfg_s, req_s = 'PENDING_SHA256(%s)' % cfg_p, 'PENDING_SHA256(%s)' % req_p
    return {'schema': UVT_RECORD_SCHEMA, 'enabled': True,
            'config': {'path': str(cfg_p), 'sha256': cfg_s, 'written': written, 'normalized_sha256': nuv['config_sha256']},
            'request': {'path': str(req_p), 'sha256': req_s, 'written': written, 'schema': UVT_REQUEST_SCHEMA},
            'admissibility': admissibility, 'certificates': certs, 'pending_certificates': list(nuv['pending_certificates']),
            'kept_regions': kept, 'domain_empty_all_stages': empty_all, 'outer': cfg['outer'], 'K_inverse_kpc': K_m * KPC_M,
            'monitor_provenance': monitor['provenance'], 'prep_patches': prep_patches,
            'route_a_argv': ['--uv-tail-config', req_p, '--uv-tail-config-sha256', req_s,
                             '--eps-certificate', certs['eps_certificate'][0], '--eps-certificate-sha256', certs['eps_certificate'][1],
                             '--lo-certificate', certs['lo_certificate'][0], '--lo-certificate-sha256', certs['lo_certificate'][1]],
            'truncation_argv': None if trunc is None else canonical(trunc),
            'test_only_flag': ['--uv-tail-admit-test-only'] if admissibility == 'test_only' else [],
            'rules': {'kept_region': 'design sec 1.1: route A, reference, body cube K; offset, columns, rotations the call truncation',
                      'test_only': 'UVT_TEST_ONLY_EMPTY_DOMAIN (NONE_TEST_ONLY certificates only with every stage domain empty)',
                      'admission': 'UVT_ADMISSION_MISMATCH (an admitted route A / reference / body must carry this config sha; tail OFF: none)'},
            'source_rule': 'nodes_v001' if nodes else 'continuum_v001', 'nodes_ext_context': nodes_ctx,  # C2V010 r4 (R2)
            'monitor_probe_R_m': monitor['probe_R_m'], 'monitor_probe_phi_rad': monitor['probe_phi_rad'],  # C2V010 r4 (R3)
            'code': {'route_a_workers': {k: [str(act['route_a'][k][0]), act['route_a'][k][1]] for k in ('worker', 'worker_parallel')},
                     'route_a_solvers': {k: [str(act['aux'][k][0]), act['aux'][k][1]] for k in ('solver', 'solver_parallel')},
                     'route_a_controller': [str(act['aux']['controller'][0]), act['aux']['controller'][1]],
                     'manifest_writer': [str(act['aux']['manifest_writer'][0]), act['aux']['manifest_writer'][1]],
                     'route_b': {k: [str(p), s] for k, (p, s) in act['scripts'].items()},
                     'route_b_binding': [str(act['aux']['route_b_binding'][0]), act['aux']['route_b_binding'][1]],
                     'library': {k: [str(p), s] for k, (p, s) in dict(UVT_LIB, **act['lib_extra']).items()}}}


def uvt_route_a_identity_check(cp, want_config_sha256):
    """C2V010: the uv_tail entry of a route-A checkpoint's caller numerical_controls (the uvtail binding writes
    controller.identity() there).  want None (a tail-OFF call): the checkpoint must carry none; otherwise its config_sha256
    must be this call's.  Refusal UVT_ADMISSION_MISMATCH.  Returns the entry summary (None when absent)."""
    cm = exec_verified(AUX['checkpoint_module'][0], AUX['checkpoint_module'][1], 'c2v010_uvt_ckpt')
    ident = _read_checkpoint_identity(cm, cp)
    caller = cm.decode(ident['identity']['caller']['record'])
    got = (caller.get('numerical_controls') or {}).get('uv_tail')
    if want_config_sha256 is None:
        if got is not None:
            raise Refusal('UVT_ADMISSION_MISMATCH: route-A checkpoint %s carries a UV-tail entry (config %s); this call is tail OFF'
                          % (cp, (got or {}).get('config_sha256') if isinstance(got, dict) else got))
        return None
    if not isinstance(got, dict) or got.get('config_sha256') != want_config_sha256:
        raise Refusal('UVT_ADMISSION_MISMATCH: route-A checkpoint %s tail config %r is not this call config %s'
                      % (cp, got.get('config_sha256') if isinstance(got, dict) else got, want_config_sha256))
    return {k: got.get(k) for k in ('config_sha256', 'request_sha256', 'admissibility', 'kept', 'static_identity_sha256')}


def uvt_admitted_record_check(path, uvt, label):
    """C2V010: an admitted reference (start.json) / body (finish.json) output and this call's tail mode must agree:
    tail OFF -> no enabled uv_tail record; tail ON -> a record with this call's config sha (UVT_ADMISSION_MISMATCH)."""
    rec = json.loads(Path(path).read_text()).get('uv_tail')
    if uvt is None:
        if isinstance(rec, dict) and rec.get('enabled'):
            raise Refusal('UVT_ADMISSION_MISMATCH: admitted %s %s carries an enabled UV-tail record; this call is tail OFF' % (label, path))
        return None
    if not isinstance(rec, dict) or (uvt['config_sha256'] is not None and rec.get('config_sha256') != uvt['config_sha256']):
        raise Refusal('UVT_ADMISSION_MISMATCH: admitted %s %s tail record %r is not this call config %s'
                      % (label, path, None if not isinstance(rec, dict) else rec.get('config_sha256'), uvt['config_sha256']))
    return {'config_sha256': rec.get('config_sha256'), 'state_digest': rec.get('state_digest')}


def uvt_stage_records(records):
    """C2V010: the uv_tail record each executed tail stage wrote into its finish.json (state digest, empty, I1-T verdict)."""
    out = []
    for rec in records:
        if not rec.get('executed') or rec.get('kind') not in UVT_TAIL_KINDS + ('route_a_tail_manifest',):
            continue
        od = _argv_map(rec['argv']).get('--outdir')
        fin = Path(od) / 'finish.json' if od else None
        if fin is None or not fin.is_file():
            out.append({'stage': rec['name'], 'kind': rec['kind'], 'finish': 'ABSENT'})
            continue
        f = json.loads(fin.read_text())
        u = f.get('uv_tail') if rec['kind'] != 'route_a_tail_manifest' else {k: f.get(k) for k in ('state_digest', 'empty', 'production_admissible', 'manifest', 'manifest_sha256')}
        u = u if isinstance(u, dict) else {}
        out.append({'stage': rec['name'], 'kind': rec['kind'], 'finish_sha256': sha256_file(fin), 'state_digest': u.get('state_digest'),
                    'empty': u.get('empty'), 'production_admissible': u.get('production_admissible'),
                    'test_only_admitted': u.get('test_only_admitted'), 'i1t_verdict': (u.get('i1t') or {}).get('verdict') if isinstance(u.get('i1t'), dict) else None,
                    'srb_rot': u.get('srb_rot')})
    return out


def uvt_binding_blockers(nodes=False):
    """C2V010: blockers of the tail-ON binding found from bytes: every route-B uvt successor names its gal_c2v005 base sha (the
    SCRIPTS pin) and loads the pinned route-B binding; the binding, the route-A controller and the RO1 workers pin the
    library / controller / facade bytes this driver pins; the manifest writer pins the controller."""
    out = []

    def text(path, sha, label):
        try:
            verify_pin(path, sha, label)
        except Refusal as exc:
            out.append('UVT_PIN: %s' % exc)
            return ''
        return Path(path).read_text()
    act = uvt_active(nodes)  # C2V010 r4 (R2): the nodes tables for a nodes_v001 call
    bpath, bsha = act['aux']['route_b_binding']
    for kind, (path, sha) in act['scripts'].items():
        t = text(path, sha, 'uvt successor ' + kind)
        base_path, base_sha = SCRIPTS[kind]
        if ('successor of %s (sha256 %s)' % (Path(base_path).name, base_sha)) not in t:
            out.append('UVT_BASE: %s does not name its gal_c2v005 base %s %s' % (Path(path).name, Path(base_path).name, base_sha[:16]))
        if ("UVT_BINDING=(Path('%s'),'%s')" % (bpath, bsha)) not in t:
            out.append('UVT_BINDING_PIN: %s does not load the pinned route-B binding %s' % (Path(path).name, bsha[:16]))
    bt = text(bpath, bsha, 'uvt route-B binding')
    ct = text(act['aux']['controller'][0], act['aux']['controller'][1], 'uvt controller')
    for key, (p, s) in dict(UVT_LIB, **act['lib_extra']).items():
        for name, t in (('route-B binding', bt), ('route-A controller', ct)):
            if s not in t:
                out.append('UVT_LIBRARY_PIN: %s does not pin %s %s' % (name, key, s[:16]))
    for key in ('worker', 'worker_parallel'):
        t = text(act['route_a'][key][0], act['route_a'][key][1], 'route-A ' + key)
        for need in (act['aux']['controller'][1], act['aux']['facade'][1], RO1_ROUTE_A['binding'][1]) + tuple(s for _, s in act['lib_extra'].values()):
            if need not in t:
                out.append('UVT_ROUTE_A_WORKER_PIN: %s does not pin %s' % (Path(act['route_a'][key][0]).name, need[:16]))
    wt = text(act['aux']['manifest_writer'][0], act['aux']['manifest_writer'][1], 'manifest writer')
    if act['aux']['controller'][1] not in wt:
        out.append('UVT_MANIFEST_WRITER_PIN: the manifest writer does not pin the route-A controller')
    return out


def uvt_static_pins(nodes=False):
    """C2V010: every tail-ON code/data pin, verified from bytes (only when numerics.uv_tail is declared).  r4: the active tables."""
    pins = {}
    act = uvt_active(nodes)
    for label, table in (('lib', dict(UVT_LIB, **act['lib_extra'])), ('route_b', act['scripts']), ('aux', act['aux']), ('route_a', act['route_a']),
                         ('ro1', RO1_ROUTE_A), ('monitor', UVT_MONITOR_PINS)):
        for key, (path, sha) in table.items():
            pins[str(path)] = verify_pin(path, sha, 'uv_tail %s %s' % (label, key))
    return pins


def uvt_scan_roots(scripts, nodes=False):
    """C2V010: transitive-scan roots of a tail-ON call: the active stage scripts, AUX, and every tail-ON code pin (r4: active)."""
    roots = list(scripts.values()) + list(AUX.values())
    act = uvt_active(nodes)
    for table in (dict(UVT_LIB, **act['lib_extra']), act['aux'], act['route_a']):
        roots += list(table.values())
    return roots


def normalize_spec(spec):
    if isinstance(spec, dict) and spec.get('schema') == NGC_SCHEMA:
        return normalize_ngc_spec(spec)  # c2v002 NGC3198 configuration (route A only; see NGC section)
    if isinstance(spec, dict) and spec.get('schema') == SCHEMA and spec.get('galaxy') == 'NGC3198':
        return normalize_ngc_route_b_spec(spec)  # c2v005 NGC3198 route B (see the C2V005 NGC route-B section)
    _strict(spec, ('schema', 'galaxy', 'label', 'physical', 'coefficients', 'numerics', 'admit', 'reference_compare'), 'spec')
    if spec.get('schema') != SCHEMA:
        raise Refusal('schema must be ' + SCHEMA)
    gname = spec.get('galaxy')
    if gname not in GALAXIES:
        raise Refusal('unknown galaxy %r' % gname)
    g = GALAXIES[gname]
    if not g['supported']:
        raise Refusal('galaxy %s UNSUPPORTED by the reused route-B stages: %s' % (gname, ' | '.join(g['blockers'])))
    phys = spec.get('physical', {})
    _strict(phys, ('Eref_J', 'ell_F_m', 'gamma', 'common_scale_s', 'entropy_K_factor', 'distance_Mpc', 'inclination_deg'), 'physical')
    out = {'schema': SCHEMA, 'galaxy': gname, 'label': spec.get('label', '')}
    p = {'Eref_J': _num(phys.get('Eref_J'), 'Eref_J'), 'ell_F_m': _num(phys.get('ell_F_m'), 'ell_F_m'),
         'gamma': _num(phys.get('gamma'), 'gamma'),  # static EH block requires net gamma > 0
         'common_scale_s': _num(phys.get('common_scale_s', 1.0), 'common_scale_s'),
         'entropy_K_factor': _num(phys.get('entropy_K_factor', g['default_entropy_K_factor']), 'entropy_K_factor'),
         'distance_Mpc': _num(phys.get('distance_Mpc', g['registered_geometry']['distance_Mpc']), 'distance_Mpc'),
         'inclination_deg': _num(phys.get('inclination_deg', g['registered_geometry']['inclination_deg']), 'inclination_deg')}
    geo = g['registered_geometry']
    # C2V008 (a), from c2v003b/c2v003c: any finite positive DDO154 distance is accepted (derive_geometry).  Inclination stays
    # registered-only (c2v003c text verbatim).  This branch is reached only for DDO154 (NGC3198 has its own normalizers, which
    # keep refusing any non-registered geometry); the galaxy test below keeps that explicit.
    if gname != 'DDO154' and p['distance_Mpc'] != geo['distance_Mpc']:
        raise Refusal('UNSUPPORTED geometry: only the registered distance %.2f Mpc is supported for %s' % (geo['distance_Mpc'], gname))
    if p['inclination_deg'] != geo['inclination_deg']:
        raise Refusal('UNSUPPORTED inclination %r: only the registered %.0f deg is supported (BLOCKED_GAS_REDEPROJECTION). '
                      'The DDO154 gas annuli are extracted IN the %.0f deg plane: extract_source.py bins every sky pixel by '
                      'deprojected radius with y/cos(i) before the annular masses/means exist, so another inclination '
                      'changes the pixel-to-annulus assignment, not a factor on the pinned arrays. No pinned formula or '
                      'route-B stage re-extracts the gas; the stellar cos(i)/cos64 re-facing and the sin(i)/sin64 '
                      'observation map alone would give a mixed-plane source. Distance is supported.'
                      % (p['inclination_deg'], geo['inclination_deg'], geo['inclination_deg']))
    out['physical'] = p
    coeff = spec.get('coefficients', None)
    if coeff is None:
        coeff = {'path': str(g['default_coefficients'][0]), 'sha256': g['default_coefficients'][1]}
    _strict(coeff, ('path', 'sha256'), 'coefficients')
    if not _is_hex64(coeff.get('sha256')) or not isinstance(coeff.get('path'), str):
        raise Refusal('coefficients {path, sha256(64 lowercase hex)} required')
    _abs(coeff['path'], 'coefficients.path')
    out['coefficients'] = {'path': str(Path(coeff['path'])), 'sha256': coeff['sha256']}
    num = spec.get('numerics', {})
    _strict(num, ('composite_grid_spec', 'truncation', 'picard', 'brackets', 'column_workers', 'k_domain', 'route_a', 'uv_tail'), 'numerics')  # C2V007 (b): + route_a; C2V010 (u): + uv_tail
    grid = num.get('composite_grid_spec', None)
    if grid is not None:
        _strict(grid, ('version', 'breaks_inverse_kpc', 'panel_orders', 'total_axis_nodes', 'scope'), 'composite_grid_spec')
        br, po = grid.get('breaks_inverse_kpc'), grid.get('panel_orders')
        if not (isinstance(br, list) and isinstance(po, list) and len(br) == len(po) + 1 and len(po) >= 1):
            raise Refusal('composite_grid_spec breaks/panel_orders malformed')
        if any(type(n) is not int or n < 2 for n in po) or grid.get('total_axis_nodes') != sum(po):
            raise Refusal('panel orders must be ints >=2 summing to total_axis_nodes')
        if br[0] != -br[-1] or br[-1] <= 0:
            raise Refusal('breaks must partition [-kmax,kmax]')
        # c2v003: > 80 nodes/axis only for the declared P-88 grids (route-A prep V008, budget 96).
        if grid['total_axis_nodes'] > PREP_V007_MAX_AXIS_NODES:
            hit = [gid for gid, (b, o, t) in DECLARED_LARGE_GRIDS.items()
                   if br == b and po == o and grid['total_axis_nodes'] == t]
            if not hit or grid['total_axis_nodes'] > PREP_V009_MAX_AXIS_NODES:  # C2V009 (a): budget 120
                raise Refusal('composite grid with %d nodes/axis > %d is accepted only as a declared P-88 grid %s'
                              % (grid['total_axis_nodes'], PREP_V007_MAX_AXIS_NODES, sorted(DECLARED_LARGE_GRIDS)))
    out_num = {'composite_grid_spec': grid}
    if num.get('k_domain') is not None:  # c2v002 OPTIONAL check; absent => exactly the c2v001 behaviour
        kd = normalize_k_domain(num['k_domain'])
        k_domain_report(grid if grid is not None else _base_seed_grid(g), kd['length_kpc'], refuse=True)
        out_num['k_domain'] = kd
    tr = num.get('truncation', {'shape': 'cube'})
    _strict(tr, ('shape', 'kmax_inverse_kpc'), 'truncation')
    shape = tr.get('shape', 'cube')
    if shape not in ('cube', 'sphere', 'cylinder'):
        raise Refusal('truncation.shape must be cube, sphere or cylinder')
    kmask = tr.get('kmax_inverse_kpc', None)
    if shape == 'cube' and kmask is not None:
        raise Refusal('cube truncation takes no kmax_inverse_kpc (the grid edge is the cube)')
    if kmask is not None:
        kmask = _num(kmask, 'truncation.kmax_inverse_kpc')
    out_num['truncation'] = {'shape': shape, 'kmax_inverse_kpc': kmask}
    pc = num.get('picard', {})
    _strict(pc, ('passes', 'speed_change_bound_km_s', 'observe_every_pass'), 'picard')
    passes = pc.get('passes', 3)
    if type(passes) is not int or not 1 <= passes <= 12:
        raise Refusal('picard.passes must be an int in 1..12')
    bound = pc.get('speed_change_bound_km_s', None)
    if bound is not None:
        bound = _num(bound, 'speed_change_bound_km_s')
    obs = pc.get('observe_every_pass', True)
    if type(obs) is not bool:
        raise Refusal('observe_every_pass must be bool')
    out_num['picard'] = {'passes': passes, 'speed_change_bound_km_s': bound, 'observe_every_pass': obs}
    bk = num.get('brackets', {'mode': 'rule'})
    _strict(bk, ('mode', 'rule', 'pinned_controls'), 'brackets')
    mode = bk.get('mode', 'rule')
    if mode == 'rule':
        rule = dict(LE_RULE_DEFAULTS)
        r_in = bk.get('rule', {})
        _strict(r_in, tuple(LE_RULE_DEFAULTS), 'brackets.rule')
        rule.update(r_in)
        for key in ('rfs_factors', 'le_first_factors', 'le_next_factors'):
            f = rule[key]
            if not (isinstance(f, list) and len(f) == 2 and 0 < _num(f[0], key) < _num(f[1], key)):
                raise Refusal(key + ' must be [lo, hi] with 0<lo<hi')
        for key, absolute in (('fs_absolute_overrides', True), ('rfs_factor_overrides', False)):
            for idx, pair in rule[key].items():  # C2V007 (a) F3: _canon_key replaces str.isdigit (c2v003c hunk @@ -577)
                if not (_canon_key(idx) and 0 <= int(idx) < g['n_columns'] and isinstance(pair, list) and len(pair) == 2
                        and 0 < _num(pair[0], key) < _num(pair[1], key)):
                    raise Refusal('%s entries must be "index": [lo, hi] (canonical ASCII index, no leading zeros): %r' % (key, idx))
        for ps, table in rule['le_factor_overrides'].items():
            if not (_canon_key(ps) and 1 <= int(ps) <= passes) or not isinstance(table, dict):
                raise Refusal('le_factor_overrides keys must be pass numbers 1..passes (canonical ASCII, no leading zeros): %r' % (ps,))
            for idx, pair in table.items():
                if not (_canon_key(idx) and 0 <= int(idx) < g['n_columns'] and isinstance(pair, list) and len(pair) == 2
                        and 0 < _num(pair[0], 'le override') < _num(pair[1], 'le override')):
                    raise Refusal('le_factor_overrides entries must be "index": [lo, hi] (canonical ASCII index, no leading zeros): %r' % (idx,))
        out_num['brackets'] = {'mode': 'rule', 'rule': rule}
    elif mode == 'pinned_controls':
        pcs = bk.get('pinned_controls')
        _strict(pcs, ('fs', 'rfs', 'le'), 'pinned_controls')

        def runs(lst, label):
            if not isinstance(lst, list) or not lst:
                raise Refusal(label + ' must be a non-empty list of {path, sha256}')
            res = []
            for item in lst:
                _strict(item, ('path', 'sha256'), label)
                if not _is_hex64(item.get('sha256')):
                    raise Refusal(label + ' sha256 must be 64 lowercase hex')
                _abs(item.get('path'), label + ' path')
                res.append({'path': str(item['path']), 'sha256': item['sha256']})
            return res
        le = pcs.get('le')
        if not isinstance(le, list) or len(le) != passes:
            raise Refusal('pinned_controls.le must list one run list per Picard pass')
        out_num['brackets'] = {'mode': 'pinned_controls', 'pinned_controls': {
            'fs': runs(pcs.get('fs'), 'pinned fs'), 'rfs': runs(pcs.get('rfs'), 'pinned rfs'),
            'le': [runs(x, 'pinned le') for x in le]}}
        if any(len(x) != 1 for x in out_num['brackets']['pinned_controls']['le']):
            raise Refusal('each LE pass must be a single column run (column-mean V004 requires one 72-column run)')
    else:
        raise Refusal('brackets.mode must be rule or pinned_controls')
    workers = num.get('column_workers', 1)
    if type(workers) is not int or not 1 <= workers <= 12:
        raise Refusal('column_workers must be int 1..12')
    if workers > 1 and mode != 'rule':
        raise Refusal('column_workers>1 requires brackets.mode rule (pinned controls cannot be split without new bytes)')
    out_num['column_workers'] = workers
    if 'route_a' in num:  # C2V007 (b): present only when declared, so a default spec normalizes exactly as in c2v006
        out_num['route_a'] = normalize_route_a_numerics(num['route_a'])
    if 'uv_tail' in num:  # C2V010 (u): present only when declared (absent -> exactly the v009 normalization)
        if gname != 'DDO154':
            raise Refusal('numerics.uv_tail: the route-B tail successors bind DDO154 only (UV_TAIL_ROUTE_B_GALAXY_NOT_BOUND_C2V001)')
        out_num['uv_tail'] = normalize_uv_tail(num['uv_tail'])
        if out_num.get('route_a', {}).get('ro1_workers'):  # C2V010 r4 (R5): tail ON always runs the RO1 workers
            raise Refusal('numerics.route_a.ro1_workers is for tail-OFF calls (a tail-ON call always runs the RO1 workers)')
    out['numerics'] = out_num
    adm = spec.get('admit', {}) or {}
    _strict(adm, ('route_a', 'reference', 'body'), 'admit')
    norm_adm = {}
    if adm.get('route_a') is not None:
        a = adm['route_a']
        _strict(a, ('attempt_directory', 'checkpoint_directory', 'identity_sha256', 'result_sha256'), 'admit.route_a')
        if not (_is_hex64(a.get('identity_sha256')) and _is_hex64(a.get('result_sha256'))):
            raise Refusal('admit.route_a needs identity_sha256 and result_sha256')
        _abs(a.get('attempt_directory'), 'admit.route_a.attempt_directory')
        _abs(a.get('checkpoint_directory'), 'admit.route_a.checkpoint_directory')
        norm_adm['route_a'] = {k: str(a[k]) for k in ('attempt_directory', 'checkpoint_directory', 'identity_sha256', 'result_sha256')}
        if out_num.get('route_a', {}).get('column_workers', 1) > 1:  # C2V007 (b): a parallel route A that would never run
            raise Refusal('numerics.route_a.column_workers > 1 requires route A to be computed by this call (admit.route_a absent)')
        if out_num.get('route_a', {}).get('ro1_workers'):  # C2V010 r4 (R5): an admitted route A cannot be RO1-armed
            raise Refusal('numerics.route_a.ro1_workers requires route A to be computed by this call (an admitted attempt keeps its own worker)')
    if adm.get('reference') is not None:
        if 'route_a' not in norm_adm:
            raise Refusal('admit.reference requires admit.route_a')
        a = adm['reference']
        _strict(a, ('directory', 'start_sha256', 'finish_sha256'), 'admit.reference')
        _abs(a.get('directory'), 'admit.reference.directory')
        norm_adm['reference'] = {k: str(a[k]) for k in ('directory', 'start_sha256', 'finish_sha256')}
    if adm.get('body') is not None:
        if 'reference' not in norm_adm:
            raise Refusal('admit.body requires admit.reference')
        a = adm['body']
        _strict(a, ('directory', 'finish_sha256'), 'admit.body')
        _abs(a.get('directory'), 'admit.body.directory')
        norm_adm['body'] = {k: str(a[k]) for k in ('directory', 'finish_sha256')}
    out['admit'] = norm_adm
    rc = spec.get('reference_compare', False)
    if type(rc) is not bool:
        raise Refusal('reference_compare must be bool')
    out['reference_compare'] = rc
    return out


def per_call_seed(nspec):
    """Return (seed_object, changed_fields, base_seed_reusable).  Only numerical_inputs Eref_J,
    gamma (both times s), ell_F_m and the composite grid (with kmax/fourier_points) change;
    the 'physical' annotation mirrors follow.  Every other field is copied unchanged."""
    g = GALAXIES[nspec['galaxy']]
    path, sha = g['base_seed']
    raw = Path(path).read_bytes()
    if sha256_bytes(raw) != sha:
        raise Refusal('base seed pin mismatch')
    base = json.loads(raw)
    seed = json.loads(raw)
    ni = seed['numerical_inputs']
    p = nspec['physical']
    s = p['common_scale_s']
    new = {'Eref_J': s * p['Eref_J'], 'gamma': s * p['gamma'], 'ell_F_m': p['ell_F_m']}
    grid = nspec['numerics']['composite_grid_spec']
    if grid is not None:
        new['composite_grid_spec'] = grid
        new['kmax_inverse_kpc'] = float(grid['breaks_inverse_kpc'][-1])
        new['fourier_points_per_axis'] = int(grid['total_axis_nodes'])
    ra_num = nspec['numerics'].get('route_a') or {}
    if 'max_iterations' in ra_num:  # C2V009 (b): route-A outer-iteration budget (absent: base seed value, c2v008 seed)
        new['max_iterations'] = ra_num['max_iterations']
    if 'seed_source_rtol_factor' in ra_num:  # RO1 AMB-14: route-A source rtol x f (absent: base seed value, v009-EXT seed)
        new['source_rtol'] = ni['source_rtol'] * ra_num['seed_source_rtol_factor']
    changed = []
    for k, v in new.items():
        if canonical(ni.get(k)) != canonical(v):
            changed.append({'field': 'numerical_inputs.' + k, 'old': ni.get(k), 'new': v})
        ni[k] = v
    for k in ('Eref_J', 'ell_F_m', 'gamma'):
        seed['physical'][k] = ni[k]
    reusable = canonical(seed) == canonical(base)
    if not reusable:
        # c2v003 annotation (CHECK_V001 s2 minor): no stage reads it; only numerical_inputs is consumed.
        # C2V007: the literal stays 'galaxy_m0_forward_c2v006' (the seed composition code is unchanged since c2v006), so a
        # c2v007 call writes the byte-identical seed and the byte-identical route-A request (--seed-sha256) of c2v006.
        seed['c2_changed_fields'] = {
            'driver': 'galaxy_m0_forward_c2v006', 'base_seed_sha256': sha, 'changed': changed,
            'note': ('scale_seed, seed_method, scope, pins, parent_seed and quadrature_selection_evidence are copied '
                     'unchanged from the base seed and describe ITS normalization and grid, not this call; '
                     'numerical_inputs (and the physical mirrors) are the values of this call.')}
    return seed, changed, reusable


# ----------------------------------------------------------------------------- c2v003b per-call geometry
# C2V008 (a): the block below (geometry_active .. geometry_inputs) is VERBATIM c2v003c ed326130 L717-888 (= c2v003b).
# The annotation literal 'galaxy_m0_forward_c2v003b' in the per-call files is kept on purpose: c2v008 writes the
# byte-identical per-call profile, monotone source and column-mean binding that c2v003c writes for the same distance.
def geometry_active(nspec):
    """True when the call geometry differs from the registered one (then per-call source files are derived)."""
    reg = GALAXIES[nspec['galaxy']]['registered_geometry']
    p = nspec['physical']
    return p['distance_Mpc'] != reg['distance_Mpc'] or p['inclination_deg'] != reg['inclination_deg']


def _pinned_json(path, sha, label):
    raw = Path(path).read_bytes()
    if sha256_bytes(raw) != sha:
        raise Refusal('%s pin mismatch: %s' % (label, path))
    return json.loads(raw)


def derive_geometry(gname, D, inc):
    """Per-call DDO154 inputs at distance D [Mpc] (inclination: registered value only, see normalize_spec).
    No producer script of the pinned profile exists on disk; each formula below is the documented rule and is
    GUARDED to reproduce the pinned registered records bitwise before it is applied at D:
      HI (calibration input source_conversion.distance; extract_source.py radii = angle*D, mass ~ D^2):
        lambda = D/4.3 (HI extraction distance); s_edges = (r_4.3*lambda)^2; annular means/controls unchanged;
        integrated mass = fsum(pi*1e6*ds*mean); original mass = fsum(annulus HI mass)*helium*lambda^2.
      stars (STELLAR_PHOTOMETRIC_REFERENCE_MEAN_PROFILE_V001, reference distance 4.04, face-on cos(i)):
        radius = arcsec*(D*1e3)/(arcsec per rad); Sigma = Sigma_64*cos(i)/cos(64) (distance-free);
        Rd and h = Rd/7.3 are angular scales converted with D: x D/4.04; masses x (D/4.04)^2; midplane x 1/(D/4.04).
      observation (column-mean binding): radius_m = r_catalogue*(D/4.04)*kpc_m; physical inclination radians(i).
      monotone source: the pinned reviewed reducer V002 re-run on the per-call HI record (saved sweeps/KKT).
    Returns (profile_obj, monotone_result, binding_obj_without_source_profile, record)."""
    if gname != 'DDO154':
        raise Refusal('per-call geometry is implemented for DDO154 only')
    g = GALAXIES[gname]
    reg = g['registered_geometry']
    if inc != reg['inclination_deg']:
        raise Refusal('inclination %r: BLOCKED_GAS_REDEPROJECTION (see normalize_spec)' % (inc,))
    if not (isinstance(D, float) and math.isfinite(D) and D > 0):
        raise Refusal('distance_Mpc must be a finite positive float')
    prof = _pinned_json(g['profile'][0], g['profile'][1], 'profile')
    cal = _pinned_json(*GEOMETRY_PINS['calibration_input'], 'calibration input')
    s3 = _pinned_json(*GEOMETRY_PINS['stellar_3d'], 'stellar 3D source')['galaxies']['DDO154']
    ph = _pinned_json(*GEOMETRY_PINS['photometric'], 'photometric reference')
    base_bind = _pinned_json(g['column_mean_binding'][0], g['column_mean_binding'][1], 'column-mean binding')
    base_mono = _pinned_json(g['monotone_source'][0], g['monotone_source'][1], 'monotone source')
    old = prof['galaxies']['DDO154']
    na = cal['source_HI']['NA']
    pg = ph['galaxies']['DDO154']
    nodes = [x for x in pg['nodes'] if x['reference_included']]
    D_hi = float(cal['geometry']['source_distance_Mpc'])       # HI extraction distance (4.3)
    D_st = float(pg['distance_Mpc_reference'])                  # photometric reference distance (4.04)
    i_st = float(pg['inclination_deg_reference'])               # photometric face-on reduction inclination (64)
    D_rows = {float(x['reference_distance_Mpc']) for x in cal['response_rows']}
    n = int(na['complete_prefix']['bin_count'])
    if (D_hi != reg['HI_original_distance_Mpc'] or float(na['reference_geometry']['distance_pc']) != D_hi * 1e6
            or D_st != reg['distance_Mpc'] or D_rows != {reg['distance_Mpc']} or i_st != reg['released_inclination_deg']
            or old['geometry']['distance_Mpc'] != reg['distance_Mpc'] or n != len(old['HI_plus_He']['annular_means_Msun_pc2'])
            or len(nodes) != len(s3['radius_kpc'])):
        raise Refusal('geometry source reference values differ from the registered geometry')
    he = float(na['reference_geometry']['helium_factor'])
    r_hi = [float(na['r_lo_kpc'][0])] + [float(x) for x in na['r_hi_kpc'][:n]]
    arcsec_rad = float(ph['normalization']['angular_arcsec_per_radian'])

    def hi_edges(Dx):
        lam = Dx / D_hi
        return lam, [(x * lam) ** 2 for x in r_hi]

    def star_radius(Dx):
        return [float(x['radius_literal']) * (Dx * 1e3) / arcsec_rad for x in nodes]

    def faceon(ix):
        return math.cos(math.radians(ix)) / math.cos(math.radians(i_st))

    def query_rows(Dx):
        return [{'id': x['id'], 'radius_m': float(x['radius_reference_kpc']) * (Dx / float(x['reference_distance_Mpc'])) * KPC_M}
                for x in cal['response_rows']]
    # Guards: the formulas reproduce the pinned registered records bitwise.
    f_reg = faceon(reg['inclination_deg'])
    guards = {
        'hi_edges': hi_edges(reg['distance_Mpc'])[1] == old['HI_plus_He']['s_edges_kpc2'],
        'hi_means': [float(x) * he for x in na['full_annulus']['effective_retained_HI_Msun_pc2'][:n]] == old['HI_plus_He']['annular_means_Msun_pc2'],
        'star_radius': star_radius(D_st) == s3['radius_kpc'] == old['stellar_reference']['radius_kpc'],
        'star_sigma': [s * f_reg for s in s3['surface_density_Msun_pc2']] == old['stellar_reference']['surface_density_Msun_pc2'],
        'star_scales': (s3['outer_scale_kpc'], s3['height_kpc']) == (old['stellar_reference']['outer_scale_kpc'], old['stellar_reference']['height_kpc']),
        'faceon_factor': f_reg == old['geometry']['stellar_faceon_factor_from_64deg'],
        'query_rows': query_rows(reg['distance_Mpc']) == base_bind['query_rows'],
        'binding_inclinations': (base_bind['physical_inclination_rad'], base_bind['released_inclination_rad'])
        == (math.radians(reg['inclination_deg']), math.radians(reg['released_inclination_deg'])),
    }
    if not all(guards.values()):
        raise Refusal('geometry formulas do not reproduce the pinned registered files: %s' % sorted(k for k, v in guards.items() if not v))
    lam, edges = hi_edges(D)
    mu = D / D_st
    f = faceon(inc)
    gas = dict(old['HI_plus_He'])
    gas['s_edges_kpc2'] = edges
    gas['integrated_mass_Msun'] = math.fsum(math.pi * 1e6 * (b - a) * m for a, b, m in zip(edges, edges[1:], gas['annular_means_Msun_pc2']))
    gas['original_retained_mass_scaled_Msun'] = math.fsum(na['full_annulus']['mass_Msun'][:n]) * he * lam ** 2
    gas['relative_mass_pairing_difference'] = (abs(gas['integrated_mass_Msun'] - gas['original_retained_mass_scaled_Msun'])
                                               / gas['original_retained_mass_scaled_Msun'])
    gas['support_radius_kpc'] = r_hi[-1] * lam
    star = dict(old['stellar_reference'])
    star['radius_kpc'] = star_radius(D)
    star['surface_density_Msun_pc2'] = [s * f for s in s3['surface_density_Msun_pc2']]
    star['midplane_density_Msun_pc3'] = [x * f / mu for x in s3['midplane_density_Msun_pc3']]
    star['outer_scale_kpc'] = s3['outer_scale_kpc'] * mu
    star['height_kpc'] = s3['height_kpc'] * mu
    for k in ('mass_within_last_node_Msun', 'assumed_exponential_tail_mass_Msun', 'total_reference_stellar_mass_Msun'):
        star[k] = s3[k] * f * mu ** 2
    geom = dict(old['geometry'])
    geom.update(distance_Mpc=D, inclination_deg=inc, radial_distance_scale=lam, stellar_faceon_factor_from_64deg=f,
                released_velocity_reference_factor=math.sin(math.radians(inc)) / math.sin(math.radians(reg['released_inclination_deg'])))
    note = {'driver': 'galaxy_m0_forward_c2v003b', 'distance_Mpc': D, 'inclination_deg': inc,
            'note': 'Per-call copy; only the DDO154 geometry-dependent fields are re-derived (derive_geometry docstring).'}
    profile = dict(prof)
    profile['galaxies'] = dict(prof['galaxies'], DDO154=dict(old, geometry=geom, HI_plus_He=gas, stellar_reference=star))
    profile['c2_geometry'] = dict(note, base={'path': str(g['profile'][0]), 'sha256': g['profile'][1]})
    red = exec_verified(GEOMETRY_PINS['monotone_reducer'][0], GEOMETRY_PINS['monotone_reducer'][1], 'c2v003b_monotone_reducer')
    mono = red.reduce_source(record=gas, max_sweeps=base_mono['diagnostics']['max_sweeps'],
                             kkt_tolerance=base_mono['diagnostics']['normalized_kkt_tolerance'])
    if mono.get('status') != base_mono['status']:
        raise Refusal('GEOMETRY_MONOTONE_SOURCE_NOT_ADMITTED: reviewed reducer returned %s' % mono.get('status'))
    mono['worker_sha256'] = GEOMETRY_PINS['monotone_reducer'][1]
    mono['model_choice'] = base_mono['model_choice']
    mono['c2_geometry'] = dict(note, base={'path': str(g['monotone_source'][0]), 'sha256': g['monotone_source'][1]})
    binding = dict(base_bind, query_rows=query_rows(D), distance_Mpc=D, physical_inclination_rad=math.radians(inc))
    binding['c2_geometry'] = dict(note, base={'path': str(g['column_mean_binding'][0]), 'sha256': g['column_mean_binding'][1]})
    ctrl = all(mono['source_record'][k] == base_mono['source_record'][k] for k in ('boundary_controls_Msun_pc2', 'middle_controls_Msun_pc2'))
    record = {'distance_Mpc': D, 'inclination_deg': inc, 'hi_lambda_D_over_4p3': lam, 'length_scale_D_over_4p04': mu,
              'stellar_faceon_factor': f, 'registered_formula_guards': guards,
              'monotone_controls_bitwise_equal_to_registered': ctrl,
              'unchanged_numerics': 'seed numerical controls (kpc-valued search/step/limits), composite k grid and column '
                                    'solver template are numerical choices and are NOT rescaled with D',
              'route_a_rows': ('NOT AT CALL GEOMETRY: prep V007/V008 reads the 12 query radii at %.2f Mpc from the calibration '
                               'input and the route-A binding hard-codes radians(66)/radians(64); route-A rows are a '
                               'diagnostic only. The route-B rows use the per-call binding.' % reg['distance_Mpc'])}
    return profile, mono, binding, record


def _write_bytes_x(ctx, path, raw):
    if ctx.mode == 'run':
        with open(path, 'xb') as f:
            f.write(raw)
            f.flush()
            os.fsync(f.fileno())
    else:
        if Path(path).exists():
            raise Refusal('dry-run input exists: %s' % path)
        Path(path).write_bytes(raw)
    return sha256_file(path)


def geometry_inputs(ctx, nspec):
    """c2v003b: None at the registered geometry (pinned files; plan unchanged).  Otherwise write the per-call
    inputs under <out>/inputs: geometry_C/{PROFILE_NAME, byte copy of source binding V003} (the prep reads both
    as C/<name>), geometry_monotone_source.json and geometry_column_mean_binding.json."""
    if not geometry_active(nspec):
        return None
    p = nspec['physical']
    profile, mono, binding, record = derive_geometry(nspec['galaxy'], p['distance_Mpc'], p['inclination_deg'])
    gdir = ctx.out / 'inputs' / 'geometry_C'
    gdir.mkdir(parents=True, exist_ok=False)
    ppath, psha = ctx.write_input('geometry_C/' + PROFILE_NAME, profile)
    bpath, bsha = GEOMETRY_PINS['source_binding_v003']
    raw = Path(bpath).read_bytes()
    if sha256_bytes(raw) != bsha or _write_bytes_x(ctx, gdir / Path(bpath).name, raw) != bsha:
        raise Refusal('source binding V003 copy pin mismatch')
    mono['input'] = {'path': str(ppath), 'sha256': psha, 'record': 'galaxies.DDO154.HI_plus_He'}
    mpath, msha = ctx.write_input('geometry_monotone_source.json', mono)
    binding['source_profile'] = {'path': str(ppath), 'sha256': psha}
    cpath, csha = ctx.write_input('geometry_column_mean_binding.json', binding)
    record['files'] = {'C_directory': str(gdir), 'profile': [str(ppath), psha], 'source_binding_v003_copy': [str(gdir / Path(bpath).name), bsha],
                       'monotone_source': [str(mpath), msha], 'column_mean_binding': [str(cpath), csha]}
    return {'C_dir': str(gdir), 'profile': (str(ppath), psha), 'monotone': (str(mpath), msha),
            'binding': (str(cpath), csha), 'record': record}


def geometry_config_fields(geo):
    """C2V008 (a): the galaxy-config values of GEOMETRY_CONFIG_FIELDS at the call geometry, read back from the per-call
    files geometry_inputs wrote (sha256 re-verified from bytes).  geo None (registered geometry) -> {}: nothing changes.
    radial.outer_edge_kpc = sqrt(last per-call s_edge), the expression the DDO154 literal check uses at 4.04 Mpc (and the
    stages' radial_truncation compares with IEEE sqrt); observation.query_rows = the per-call binding rows {id, radius_m}."""
    if geo is None:
        return {}
    raws = {}
    for key in ('profile', 'binding'):
        raw = Path(geo[key][0]).read_bytes()
        if sha256_bytes(raw) != geo[key][1]:
            raise Refusal('per-call geometry file pin mismatch: %s' % geo[key][0])
        raws[key] = json.loads(raw)
    edges = raws['profile']['galaxies']['DDO154']['HI_plus_He']['s_edges_kpc2']
    return {'source.profile': {'path': str(geo['profile'][0]), 'sha256': geo['profile'][1]},
            'source.monotone_source': {'path': str(geo['monotone'][0]), 'sha256': geo['monotone'][1]},
            'radial.outer_edge_kpc': float(math.sqrt(edges[-1])),
            'observation.binding': {'path': str(geo['binding'][0]), 'sha256': geo['binding'][1]},
            'observation.query_rows': [{'id': q['id'], 'radius_m': q['radius_m']} for q in raws['binding']['query_rows']]}


def geometry_admission_probe(ctx, gc, gfields):
    """C2V008 (a): does the reviewed stage binding admit this call's geometry?  For every successor that consumes a
    GEOMETRY_CONFIG_FIELDS field, write a probe config = the stage config with those fields PER_CALL at the call geometry
    and every other field the galaxy-config entry (DDO154_EXACT_LITERAL; column mean: custody.column_mean_input_pins = the
    5-pin list the driver passes, built from the saved chain with the probe's binding first; producer pins = the successor
    scripts), and run the SUCCESSOR'S OWN admission (probe_stage_admission) on it; plus a control copy at the registered
    geometry, which must be accepted (else the probe proves nothing).  Writes only probe files under <out>/inputs.
    Returns {stages: {kind: {geometry_fields, call_geometry, registered_control}}, refused, controls_accepted, admitted}."""
    rows = {}
    lit = gc['cfg']['fields']['custody.column_mean_input_pins']['value']
    for kind in GENERALIZED:
        consumed = set(consumed_fields(kind))
        gf = {k: v for k, v in gfields.items() if k in consumed}
        if not gf:
            continue
        row = {'geometry_fields': sorted(gf)}
        for tag, pc in (('call_geometry', dict(gf)), ('registered_control', {})):
            if kind == 'column_mean_v004':
                b = pc.get('observation.binding') or gc['cfg']['fields']['observation.binding']['value']
                pins = [[str(b['path']), b['sha256']]]
                for run_key in ('rotation_run', 'columns_run'):
                    for name in ('start.json', 'finish.json'):
                        f = Path(lit[run_key]) / name
                        pins.append([str(f), sha256_file(f)])
                pc['custody.column_mean_input_pins'] = pins
            producers = {n: producer_pin(k, SCRIPTS[k][1]) for n, k in GENERALIZED[kind].get('producer_pins', {}).items()} or None
            obj, _ = stage_config_object(kind, gc, pc, omit_missing_per_call=False, producers=producers)
            p, s = ctx.write_input('geometry_admission_probe_%s_%s.json' % (kind, tag), obj)
            row[tag] = dict(probe_stage_admission(kind, p, s), path=str(p), sha256=s, per_call_fields=sorted(pc))
        rows[kind] = row
    refused = {k: r['call_geometry'].get('refusal') for k, r in rows.items() if not r['call_geometry']['accepted']}
    controls = all(r['registered_control']['accepted'] for r in rows.values())
    return {'stages': rows, 'refused': refused, 'controls_accepted': controls, 'admitted': bool(rows) and not refused and controls,
            'rule': ('gal_c2v005 shared admission (schema V005 admission_rules; c2v009): a DDO154 config field is admitted only as '
                     'DDO154_EXACT_LITERAL (== the schema ddo154 value, i.e. the 4.04 Mpc files) or PER_CALL on a per-call kind '
                     '(PER_CALL_CUSTODY, ROUTE_A_RUN_OUTCOME, STAGE_CODE_IDENTITY), a call input (source.coefficients) or a '
                     'declared input slot, or (c2v005) PER_CALL on a field of PER_CALL_GEOMETRY[galaxy] that the schema V005 '
                     'per_call_geometry entry lists (DDO154: the five distance-dependent fields)')}


def _relative_request_paths(req):
    """C2V007 (a) F2, from c2v003c (RD1 F2; hunk @@ -865): every path a stage request hands to the child that is not
    absolute.  Paths are the script, argv values (any value that is not a number, a 64-hex digest or a simulate-mode
    sentinel), __path__/__pathdict__/__ordered__ path entries of stage globals and module patches, module-patch and
    dict-item paths, and the mask's module paths.  Adapted to c2v006: a sentinel is any value _has_pending accepts
    (PENDING... or NONE_IN_REVIEWED_CODE..., the c2v005/c2v006 placeholder for an undecided field); c2v003c knew only
    PENDING."""
    found = []

    def chk(v):
        if isinstance(v, (str, Path)) and not _has_pending(str(v)) and not Path(str(v)).is_absolute():
            found.append(str(v))

    def val(v):
        if isinstance(v, dict) and len(v) == 1:
            (k, x), = v.items()
            if k == '__path__':
                chk(x)
            elif k in ('__pathdict__', '__ordered__'):
                for item in x:
                    chk(item[0])
    chk(req.get('script'))
    argv = [str(a) for a in req.get('argv', [])]
    for i, a in enumerate(argv):
        if a.startswith('--') or i == 0 or not argv[i - 1].startswith('--'):
            continue
        if argv[i - 1] in UVT_ARGV_NON_PATH or a == UVT_TEST_ONLY:  # C2V010 (u): JSON value / certificate sentinel, not paths
            continue
        try:
            float(a)
            continue
        except ValueError:
            pass
        if not _is_hex64(a):
            chk(a)
    for v in (req.get('stage_globals') or {}).values():
        val(v)
    for p in req.get('module_patches') or []:
        chk(p.get('path'))
        for v in (p.get('set') or {}).values():
            val(v)
    for items in (req.get('stage_dict_items') or {}).values():
        for pin in items.values():
            chk(pin.get('path'))
    for key in ('checkpoint_module', 'cache_module'):
        if req.get('mask'):
            chk(req['mask'][key][0])
    return found


# ----------------------------------------------------------------------------- execution context
class Ctx:
    """mode 'run': executes stages.  mode 'simulate': executes nothing; a stage's outputs are
    the SAVED chain's outputs (reproduction map) when they exist, else symbolic placeholders."""

    def __init__(self, mode, nspec, outdir, saved_runs=None):
        self.mode = mode
        self.spec = nspec
        self.out = Path(outdir)
        self.saved = saved_runs or {}
        self.counter = 0
        self.records = []
        self.passes = []
        self.compare = []
        self.t0 = time.monotonic()
        self.log = None
        self.driver = str(Path(__file__).resolve())
        self.route_a_outcome = None  # C2V007 (a) F1: classification of the route-A result.json (c2v003c hunk @@ -882)
        self.geometry = None  # C2V008 (a): per-call geometry record + stage-admission probe (None at the registered geometry)
        self.scripts = SCRIPTS  # C2V010 (u): the stage-script table (tail ON: SCRIPTS + SCRIPTS_UVT + the manifest writer)
        self.uv_tail = None  # C2V010 (u): tail-ON planning/custody record (None: tail OFF)

    # -- paths / hashes ------------------------------------------------------------------
    def stage_dir(self, name):
        self.counter += 1
        d = self.out / 'stages' / ('%02d_%s' % (self.counter, name))
        if self.mode == 'run':
            d.mkdir(parents=True, exist_ok=False)
        return d

    def finish_sha(self, d, name='finish.json'):
        p = Path(d) / name
        if p.is_file():
            return sha256_file(p)
        return 'PENDING_SHA256(%s)' % p

    def event(self, **kw):
        kw['elapsed_seconds'] = time.monotonic() - self.t0
        if self.log is not None:
            self.log.write(json.dumps(_jsonable(kw), allow_nan=False) + '\n')
            self.log.flush()

    def write_input(self, name, obj):
        d = self.out / 'inputs'
        if self.mode == 'run':
            d.mkdir(parents=True, exist_ok=True)
        p = d / name
        if self.mode == 'run':
            return p, _write_x(p, obj)
        raw = (json.dumps(_jsonable(obj), indent=1, allow_nan=False) + '\n').encode()
        d.mkdir(parents=True, exist_ok=True)
        if p.exists():
            raise Refusal('dry-run input exists: %s' % p)
        p.write_bytes(raw)
        return p, sha256_bytes(raw)

    # -- stage execution -------------------------------------------------------------------
    def request(self, name, key, argv, stage_globals=None, module_patches=None, mask=None):
        script, sha = self.scripts[key]  # C2V010 (u): SCRIPTS unless tail ON
        return {'name': name, 'kind': key, 'script': str(script), 'script_sha256': sha, 'argv': [str(a) for a in argv],
                'stage_globals': stage_globals or {}, 'module_patches': module_patches or [], 'mask': mask}

    def run_stages(self, requests, stage_dirs):
        """Run one or more independent stage requests concurrently (single-thread each)."""
        import subprocess
        for req, d in zip(requests, stage_dirs):  # C2V007 (a) F2 (c2v003c hunk @@ -926): every mode, before anything is launched
            bad = _relative_request_paths(req) + ([str(d)] if not Path(d).is_absolute() else [])
            if bad:
                raise Refusal('RELATIVE_PATH_IN_REQUEST %s: stages run with cwd=<stage dir>, so relative paths %s '
                              'would not resolve (use an absolute outdir/report dir and absolute spec paths)' % (req['name'], bad[:5]))
        recs = []
        if self.mode != 'run':
            for req, d in zip(requests, stage_dirs):
                rec = dict(req, stage_dir=str(d), executed=False)
                self.records.append(rec)
                recs.append(rec)
            return recs
        procs = []
        for req, d in zip(requests, stage_dirs):
            rp = d / 'request.json'
            rsha = _write_x(rp, req)
            fo = open(d / 'stdout.txt', 'x')
            fe = open(d / 'stderr.txt', 'x')
            t = time.monotonic()
            pr = subprocess.Popen([PY, '-I', '-B', self.driver, '_stage', str(rp)], stdout=fo, stderr=fe,
                                  env=single_thread_env(), cwd=str(d))
            self.event(stage=req['name'], event='started', pid=pr.pid, request_sha256=rsha)
            procs.append((req, d, rp, rsha, pr, fo, fe, t))
        failed = []
        for req, d, rp, rsha, pr, fo, fe, t in procs:
            code = pr.wait()
            fo.close()
            fe.close()
            rec = dict(req, request_path=str(rp), request_sha256=rsha, stage_dir=str(d), exit_code=code,
                       elapsed_seconds=time.monotonic() - t, executed=True)
            self.records.append(rec)
            recs.append(rec)
            self.event(stage=req['name'], event='finished', exit_code=code, elapsed=rec['elapsed_seconds'])
            if code != 0:
                failed.append(req['name'])
        if failed:
            raise StageFailed('stage(s) exited nonzero: %s' % failed)
        return recs

    def saved_or(self, key, default):
        v = self.saved.get(key)
        return Path(v) if isinstance(v, (str, Path)) else default


# ----------------------------------------------------------------------------- chain helpers
def _read_checkpoint_identity(cm, cp):
    ident = cm._read(str(Path(cp) / 'IDENTITY.json'), 'identity')
    if ident['identity_sha256'] != cm._sha(cm._canonical(ident['identity'])):
        raise Blocked('checkpoint identity self-hash mismatch')
    return ident


ROUTE_A_CONVERGED = 'CONVERGED_FINITE_FIXED_POINT'


def route_a_outcome_record(ra, result_path):
    """C2V007 (a) F1, verbatim from c2v003c (RD1 F1; hunk @@ -973): classify a route-A attempt from ITS OWN result.json
    (the route-A worker v002 writes it, exit 0, for every solver outcome the solver RETURNS).  Layout: result.result =
    prediction v005 return; its source_fixed_point = the solver return, whose checkpoint.outcome is the solver outcome
    token and whose history[-1].iteration is the last completed iteration.  Pure: returns the record, raises nothing
    except StageFailed on an unreadable layout.  The parallel worker successor writes the same layout (same binding,
    prediction and solver return; CHECK_V001 s1-s3)."""
    try:
        pred = ra['result']['result']
        sfp = pred.get('source_fixed_point')
        if not isinstance(sfp, dict):
            raise TypeError('source_fixed_point absent')
        hist = sfp.get('history') or []
        outcome = (sfp.get('checkpoint') or {}).get('outcome')
        conv_flag = sfp.get('converged_finite_fixed_point')
        rec = {'result_path': str(result_path), 'result_sha256': sha256_file(result_path), 'outcome': outcome,
               'converged_finite_fixed_point': conv_flag, 'predictions_available': pred.get('predictions_available'),
               'iterations_completed': [h.get('iteration') for h in hist],
               'last_completed_iteration': hist[-1].get('iteration') if hist else None,
               'reason': pred.get('reason'), 'solver_scope': sfp.get('scope')}
    except (KeyError, TypeError, AttributeError, IndexError) as exc:
        raise StageFailed('ROUTE_A_RESULT_UNREADABLE %s: %s: %s' % (result_path, type(exc).__name__, exc))
    f = sfp.get('failure')
    if isinstance(f, dict):
        rec['failure'] = {k: f.get(k) for k in ('type', 'message', 'iteration', 'column_index', 'stage')}
    ro1, ro1_fired = ro1_outcome(ra, pred, result_path, conv_flag is True and outcome == ROUTE_A_CONVERGED)  # RO1
    if conv_flag is True and outcome == ROUTE_A_CONVERGED and rec['predictions_available'] is True:
        rec['classification'] = 'CONVERGED'
        rec['converged_iteration'] = rec['last_completed_iteration']
    elif ro1_fired:  # RO1: converged fixed point, circular-trial readout refused and recorded; route B proceeds
        rec['classification'] = 'CONVERGED'
        rec['converged_iteration'] = rec['last_completed_iteration']
    elif conv_flag is not True:
        rec['classification'] = 'ROUTE_A_NO_FIXED_POINT'
        rec['converged_iteration'] = None
    else:
        rec['classification'] = 'INCONSISTENT'
        rec['converged_iteration'] = None
    rec['ro1'] = ro1  # RO1 (AMB-15): result.route_a_outcome.ro1 in every outcome record
    return rec


def ro1_outcome(ra, pred, result_path, converged):
    """RO1: (ro1 block, fired).  Block = {'rule': 'RO1', 'fired', 'events', 'armed', 'worker_sha256', 'binding_sha256'}.
    armed: result.json input_pins name a pinned RO1 binding AND the attempt start.json worker_pin is a pinned RO1 worker
    (else the shas are None; a non-armed attempt that returned a result had no readout refusal).  fired (events = [the
    record]) only for an armed attempt with an admissible route_a_readout_refusal record on a converged outcome; a present but
    inadmissible record is kept under 'inadmissible_record' with fired False.  Raises nothing."""
    bind, worker = [], None
    try:
        pins = ra.get('input_pins') or {}
        bind = [s for p, s in (RO1_ROUTE_A['binding'], RO1_ROUTE_A['ngc_binding']) if pins.get(str(Path(p).resolve())) == s]
        if bind:
            worker = json.loads((Path(result_path).parent / 'start.json').read_text()).get('worker_pin')
    except (OSError, ValueError, TypeError, AttributeError):
        bind, worker = [], None
    armed = bool(bind) and worker in ({RO1_ROUTE_A[k][1] for k in ('worker', 'worker_parallel', 'ngc_worker', 'ngc_worker_parallel')}
                                      | {NODES_ROUTE_A[k][1] for k in ('worker', 'worker_parallel')})  # C2V010 r4: + the nodes RO1 workers
    block = {'rule': 'RO1', 'fired': False, 'events': [], 'armed': armed,
             'worker_sha256': worker if armed else None, 'binding_sha256': bind[0] if armed else None}
    rec = pred.get('route_a_readout_refusal')
    if rec is None:
        return block, False
    ok = (armed and converged is True and isinstance(rec, dict) and rec.get('code') == RO1_CODE and rec.get('refusal') in RO1_MESSAGES
          and rec.get('after_convergence') is True and pred.get('readout_status') == RO1_CODE
          and pred.get('predictions_available') is False and 'rows' in pred and pred.get('rows') is None)
    if ok:
        block.update(fired=True, events=[dict(rec)])
    else:
        block['inadmissible_record'] = rec
    return block, ok


def require_route_a_fixed_point(rec, reported_iteration=None):
    """C2V007 (a) F1, from c2v003c require_route_a_fixed_point: no fixed point -> RouteANoFixedPoint (its own status);
    inconsistent record -> StageFailed.  Adapted to c2v006 (no iteration-4 lock; the stages accept the strict reader's
    iteration): c2v003c's 'converged at k != 4 -> Blocked ROUTE_A_ITERATION_NOT_4' becomes 'converged at k != the
    iteration the strict reader reports from the checkpoint records -> Blocked ROUTE_A_ITERATION_MISMATCH' (checked
    only when the reader ran, i.e. reported_iteration is given)."""
    if rec['classification'] == 'ROUTE_A_NO_FIXED_POINT':
        f = rec.get('failure') or {}
        raise RouteANoFixedPoint('ROUTE_A_NO_FIXED_POINT: route-A outcome %s after iterations %s%s (a result at this '
                                 'parameter point, not a tooling gap)' % (
                                     rec['outcome'], rec['iterations_completed'],
                                     '; failure %s: %s (iteration %s, column %s, stage %s)' % (
                                         f.get('type'), f.get('message'), f.get('iteration'), f.get('column_index'), f.get('stage'))
                                     if f else ''), rec)
    if rec['classification'] != 'CONVERGED':
        raise StageFailed('ROUTE_A_RESULT_INCONSISTENT: converged flag %r, outcome %r, predictions_available %r'
                          % (rec['converged_finite_fixed_point'], rec['outcome'], rec['predictions_available']))
    if reported_iteration is not None and rec['converged_iteration'] != reported_iteration:
        raise Blocked('ROUTE_A_ITERATION_MISMATCH: route-A result.json converged at iteration %r; the checkpoint records '
                      'report %r (strict reader)' % (rec['converged_iteration'], reported_iteration))


def route_a_attempt_link(cm, ra, identity_sha, cp):
    """C2V008 (d), v003c CHECK D1 (RD1 F6): the route-A attempt (its own result.json `ra`) must belong to the checkpoint it
    is paired with: result.result.source_fixed_point.checkpoint.identity_sha256 == the checkpoint IDENTITY identity_sha256,
    and its attempt token names an attempts/<token>.end.json of that identity.  Else Refusal (a pairing error in the call
    spec or tooling, never a model outcome).  A computed route A always passes (attempt and checkpoint of one run)."""
    try:
        ck = ra['result']['result']['source_fixed_point']['checkpoint']
        got, tok = ck.get('identity_sha256'), ck.get('attempt')
    except (KeyError, TypeError, AttributeError) as exc:
        raise StageFailed('ROUTE_A_RESULT_UNREADABLE (attempt/checkpoint link): %s: %s' % (type(exc).__name__, exc))
    if got != identity_sha:
        raise Refusal('ROUTE_A_ATTEMPT_NOT_OF_THIS_CHECKPOINT: attempt result.json names checkpoint identity %r, the paired '
                      'checkpoint IDENTITY is %s' % (got, identity_sha))
    end = Path(cp) / 'attempts' / ('%s.end.json' % tok) if isinstance(tok, str) and tok and '/' not in tok else None
    if end is None or not end.is_file():
        raise Refusal('ROUTE_A_ATTEMPT_NOT_OF_THIS_CHECKPOINT: attempt token %r has no %s/attempts/<token>.end.json' % (tok, cp))
    rec = cm._read(str(end), 'attempt_end')
    if rec.get('identity_sha256') != identity_sha:
        raise Refusal('ROUTE_A_ATTEMPT_NOT_OF_THIS_CHECKPOINT: %s carries identity %r' % (end.name, rec.get('identity_sha256')))
    return {'identity_sha256': got, 'attempt': tok, 'end_record': str(end), 'end_outcome': rec.get('outcome')}


def route_a_custody(cp, seed_sha, coeff_path, call_physical, outcome=None, expected_solver=None, profile_sha=None, attempt_result=None):
    """Verify a route-A checkpoint (computed in this call or admitted) from bytes and return
    the per-call identity the route-B stages need.  c2v005: the route-B stages are generalized, so the converged final
    iteration is the one the checkpoint's own records report under the strict rule (route_a_reported_iteration); the
    c2v004 iteration_0004 literal is gone.  Any ambiguity is a BLOCKER.
    C2V007: (a) F4 background mu/C custody (c2v003c hunk @@ -993); (a) F1 `outcome` (route_a_outcome_record) enforced after
    the identity/parameter/coefficient/background checks and BEFORE the strict reader, so a no-fixed-point attempt ends
    ROUTE_A_NO_FIXED_POINT instead of ROUTE_A_ITERATION_AMBIGUOUS; its converged iteration must equal the reader's.
    (b) custody.solver_code = IDENTITY code.solver {path, sha256} from bytes (the one IDENTITY field the parallel solver
    changes); `expected_solver` (path, sha) given -> it must match (route A computed by this call), else recorded only.
    C2V008: (d) `attempt_result` (the attempt's result.json) must belong to this checkpoint (route_a_attempt_link), checked
    right after the identity self-hash, before any outcome verdict; (a) `profile_sha` (DDO154: the call's source profile,
    per-call or registered) must be the one PROFILE_NAME pin the checkpoint caller recorded (c2v003b verbatim:
    ROUTE_A_GEOMETRY_MISMATCH).  The seed does not depend on the distance, so without this check a route A prepared at
    another distance would be admitted."""
    import numpy as np
    cm = exec_verified(AUX['checkpoint_module'][0], AUX['checkpoint_module'][1], 'c2v001_ckpt')
    ident = _read_checkpoint_identity(cm, cp)
    link = route_a_attempt_link(cm, attempt_result, ident['identity_sha256'], cp) if attempt_result is not None else None
    caller = cm.decode(ident['identity']['caller']['record'])
    if caller['seed']['sha256'] != seed_sha:
        raise Blocked('checkpoint caller seed %s is not this call seed %s' % (caller['seed']['sha256'], seed_sha))
    if profile_sha is not None:  # c2v003b: the checkpoint must have been prepared from this call's source profile
        got = sorted(s for p, s in (caller.get('code_pins') or {}).items() if Path(p).name == PROFILE_NAME)
        if got != [profile_sha]:
            raise Blocked('ROUTE_A_GEOMETRY_MISMATCH: checkpoint source profile pins %s, call profile %s' % (got, profile_sha))
    phys = caller['physical_parameters']
    for k in ('Eref_J', 'ell_F_m', 'gamma'):
        if phys.get(k) != call_physical[k]:
            raise Blocked('checkpoint %s differs from call' % k)
    with np.load(coeff_path, allow_pickle=False) as f:
        grid = f['source_hessian_grid'].copy()
        mu = f['background_mu'].copy()  # C2V007 (a) F4
        Cb = f['background_C'].copy()
    dig = ident['identity']['inputs_sha256']['fourier_arguments']
    if cm.digest(grid) != dig['source_hessian_grid']:
        raise Blocked('checkpoint coefficient grid differs from call coefficient grid')
    # C2V007 (a) F4: the same two checks offset v003 makes (array equality with the caller mubar/Cbar and the
    # operator-argument digests), made here so a mismatch blocks before the reference and body stages run.
    if not (cm.digest(mu) == dig.get('mubar') and cm.digest(Cb) == dig.get('Cbar')
            and np.array_equal(mu, phys.get('mubar')) and np.array_equal(Cb, phys.get('Cbar'))):
        raise Blocked('ROUTE_A_BACKGROUND_MISMATCH: checkpoint background mu/C differs from call coefficients '
                      '(offset v003 would refuse with Frozen background mismatch)')
    if outcome is not None:  # C2V007 (a) F1: model outcome first (no fixed point / inconsistent record)
        require_route_a_fixed_point(outcome)
    solver_code = (ident['identity'].get('code') or {}).get('solver')  # C2V007 (b)
    solver_code = {'path': solver_code.get('path'), 'sha256': solver_code.get('sha256')} if isinstance(solver_code, dict) else None
    if expected_solver is not None and solver_code != {'path': str(expected_solver[0]), 'sha256': expected_solver[1]}:
        raise Blocked('ROUTE_A_SOLVER_MISMATCH: checkpoint IDENTITY code.solver %r is not the solver this call ran %s %s'
                      % (solver_code, expected_solver[0], expected_solver[1]))
    it = route_a_reported_iteration(cp, ident['identity_sha256'], cm)
    if outcome is not None:  # C2V007 (a) F1 adapted: result.json converged iteration == the strict reader's
        require_route_a_fixed_point(outcome, reported_iteration=it)
    folder = Path(cp) / ('iteration_%04d' % it)
    start = cm._read(str(folder / 'START.json'), 'iteration_start')
    done = cm._read(str(folder / 'COMPLETED.json'), 'iteration_completed')
    if start['iteration'] != it or done['converged'] is not True or done['iteration_start_sha256'] != start['payload_sha256']:
        raise Blocked('ROUTE_A_NOT_CONVERGED_AT_REPORTED_ITERATION_%d' % it)
    return {'identity_sha256': ident['identity_sha256'], 'iteration': it, 'start_payload_sha256': start['payload_sha256'],
            'g4_ref': start['prepared_weighted_responses'], 'waves_ref': start['prepared_wavevectors'],
            'caller_seed': caller['seed'], 'physical': {k: phys.get(k) for k in ('Eref_J', 'ell_F_m', 'gamma')},
            'prep_code_pins': {p: s for p, s in (caller.get('code_pins') or {}).items()
                               if 'actual_initial_source_preparation' in p},  # c2v003: record which prep built route A (c2v005: DDO or NGC)
            'solver_code': solver_code,  # C2V007 (b)
            'attempt_link': link, 'source_profile_sha256': profile_sha}  # C2V008 (d), (a)


def column_H(run_dirs):
    """Solved central enthalpies of completed columns (file pins from the run finish.json)."""
    H = {}
    for d in run_dirs:
        fin = Path(d) / 'finish.json'
        if not fin.is_file():
            return None
        f = json.loads(fin.read_text())
        for item in f['completed']:
            if sha256_file(item['path']) != item['sha256']:
                raise StageFailed('column file pin mismatch ' + item['path'])
            col = json.loads(Path(item['path']).read_text())
            if col['radial_index'] in H:
                raise StageFailed('duplicate column %d' % col['radial_index'])
            H[col['radial_index']] = col['Hc_m2_s2']
    return H


def rule_brackets(H, factors, overrides, indices):
    lo, hi = factors
    out = {}
    for i in indices:
        f = overrides.get(str(i), [lo, hi])
        out[str(i)] = [f[0] * H[i], f[1] * H[i]]
    return out


def require_bracket_source(H, n, tag):
    """c2v003 (CHECK_V001 further defect 1): a missing column is a stage failure, not a bare KeyError."""
    missing = sorted(set(range(n)) - set(H))
    if missing:
        raise StageFailed('%s column(s) %s failed; no bracket source' % (tag, missing[:20]))


def merged_brackets(paths):
    """index -> bracket actually supplied by a list of controls files (later runs win)."""
    out = {}
    for p in paths:
        c = json.loads(Path(p).read_text())
        b = c.get('column_enthalpy_brackets', {})
        for i in c['radial_indices']:
            out[str(i)] = list(b.get(str(i), c['solver']['enthalpy_bracket']))
    return out


def rule_vs_saved(g, key, table):
    """DIAGNOSTIC: rule-generated bracket table versus the saved chain's controls for that pass."""
    sc = g.get('saved_controls', {})
    if key == 'fs':
        paths = [p for p, _ in sc.get('fs', [])]
    elif key == 'rfs':
        paths = [p for p, _ in sc.get('rfs', [])]
    else:
        k = int(key[2:]) - 1
        paths = [p for p, _ in sc['le'][k]] if 'le' in sc and k < len(sc['le']) else []
    if not paths:
        return {'checked': False}
    saved = merged_brackets(paths)
    diff = [i for i in saved if saved[i] != list(table.get(i, []))]
    return {'checked': True, 'n': len(saved), 'bitwise_equal_to_saved_controls': not diff, 'differing_indices': diff[:20]}


def bracket_check(pinned_paths, H, factors, overrides):
    """Diagnostic: do the pinned controls equal rule(H) bitwise?"""
    if H is None:
        return {'checked': False, 'reason': 'previous columns not available'}
    pinned = {}
    for p in pinned_paths:
        c = json.loads(Path(p).read_text())
        b = c.get('column_enthalpy_brackets', {})
        for i in c['radial_indices']:
            pinned[str(i)] = b.get(str(i), c['solver']['enthalpy_bracket'])
    rule = rule_brackets(H, factors, overrides, sorted(int(i) for i in pinned))
    diff = [i for i in pinned if pinned[i] != rule[i]]
    return {'checked': True, 'n': len(pinned), 'bitwise_equal': not diff, 'differing_indices': diff[:20]}


def _chunks(seq, n):
    n = max(1, min(n, len(seq)))
    size, rem = divmod(len(seq), n)
    out, i = [], 0
    for c in range(n):
        j = i + size + (1 if c < rem else 0)
        out.append(seq[i:j])
        i = j
    return out


def array_digests(npz_path, keys=None):
    import numpy as np
    out = {}
    with np.load(npz_path, allow_pickle=False) as f:
        for k in (keys or f.files):
            a = np.ascontiguousarray(f[k])
            h = hashlib.sha256((a.dtype.str + str(a.shape)).encode())
            h.update(a.tobytes())
            out[k] = h.hexdigest()
    return out


def compare_npz(new, old, keys=None):
    import numpy as np
    res = {}
    with np.load(new, allow_pickle=False) as a, np.load(old, allow_pickle=False) as b:
        for k in (keys or b.files):
            if k not in a.files:
                res[k] = 'MISSING'
                continue
            x, y = a[k], b[k]
            if x.shape != y.shape or x.dtype != y.dtype:
                res[k] = 'SHAPE_OR_DTYPE_DIFFERS'
            elif np.array_equal(x, y):
                res[k] = 'BITWISE_EQUAL'
            else:
                res[k] = 'DIFFERS max_abs=%r' % float(np.max(np.abs(x - y)))
    return res


def harmonic_diagnostic(rotation_npz):
    """Driver-side DIAGNOSTIC (not a stage output): azimuthal Fourier amplitude ratios of the
    stored full radial force Phi_R_full over the 16 azimuths, |F_m|/|F_0|, m=1..8."""
    import numpy as np
    with np.load(rotation_npz, allow_pickle=False) as f:
        pr = f['Phi_R_full'].copy()
        R = f['radial_nodes_m'].copy()
    F = np.abs(np.fft.rfft(pr, axis=1))
    with np.errstate(divide='ignore', invalid='ignore'):
        ratio = F[:, 1:, :] / F[:, :1, :]
    ratio = np.where(np.isfinite(ratio), ratio, np.nan)
    per_m = {('m%d' % (m + 1)): float(np.nanmax(ratio[:, m, :])) for m in range(ratio.shape[1])}
    per_radius = [{('m%d' % (m + 1)): float(np.nanmax(ratio[i, m, :])) for m in range(ratio.shape[1])} for i in range(len(R))]
    return {'quantity': '|FFT_m(Phi_R_full)|/|FFT_0(Phi_R_full)| over 16 azimuths, max over z', 'global_max': per_m,
            'per_radius_max': per_radius, 'radial_nodes_m': R.tolist(), 'status': 'DIAGNOSTIC_ONLY'}


# ============================================================================= C2V005 galaxy-config binding
# One driver-level galaxy-config file per galaxy (a copy of the pinned schema V003 for that galaxy, made by
# binding/configs/make_galaxy_config_c2v005.py).  Per stage call the driver writes the config in the successor's
# format {format, schema{name,path,sha256}, galaxy, fields[, producer_pins]}: galaxy fields from that file, PER_CALL
# fields from bytes of this call, a DECLARED_INPUT_SLOT from the call spec.  One shared admission reads it (N5).
GC_SCHEMA = (BIND7 / 'schema/GALAXY_CONFIG_SCHEMA_V005.json', 'f9b8d48eca10e5c8f2299c23dc1ac69c60c9f87bc24486024e675f7927bc042a')  # c2v009
GC_SCHEMA_NAME = 'UNT_ROUTE_B_GALAXY_CONFIG_SCHEMA_V005'  # c2v009
GC_FORMAT = 'UNT_ROUTE_B_DRIVER_GALAXY_CONFIG_C2V006'
GC_ENTRY = {'DDO154': 'ddo154', 'NGC3198': 'ngc3198'}
GC_MEMBER_ENTRY = {('NGC3198', 'GL10_ALTERNATIVE'): 'ngc3198_gl10_alternative'}  # c2v006 (A2, CHECK D2)
# c2v006: keyed by (galaxy, member); member None = the primary entry.
GALAXY_CONFIG_FILES = {
    'DDO154': (BIND7 / 'configs/GALAXY_CONFIG_DDO154_GAL_C2V005.json', 'c21f1272f94026dcd4d38b5a8d89e8af2c76e85fbdff2d28f517c366c80f7c45'),  # c2v009
    'NGC3198': (BIND7 / 'configs/GALAXY_CONFIG_NGC3198_GAL_C2V005.json', '299ce971fab0ad6557754066d39ec5a0a664d09dfddcff7650f91b059cd82559'),  # c2v009
    ('NGC3198', 'GL10_ALTERNATIVE'): (BIND7 / 'configs/GALAXY_CONFIG_NGC3198_GL10_ALTERNATIVE_GAL_C2V005.json',  # c2v009
                                      '0873b6a4ffde696243f842c656fdc64c519d40aaad7a04f4beda5d47b0f1335a'),
}
ADMITTED_STATUS = ('DDO154_EXACT_LITERAL', 'PER_CALL', 'SUPPLIED_REVIEWED_CODE', 'SUPPLIED_REVIEWED_DATA', 'SUPPLIED_REVIEWED_CODE_AND_DATA',
                   'SUPPLIED_TARGET_FREE_MANIFEST', 'SHARED_SAME_VALUE', 'SUPPLIED_ROOT_DECISION')
SLOT_STATUS = 'DECLARED_INPUT_SLOT'
# Per-call fields in the order they become known along the chain.
PER_CALL_FIELDS = ('custody.seed_sha256', 'source.coefficients', 'custody.checkpoint_identity_sha256', 'route_a.accepted_iteration',
                   'custody.reference_run', 'custody.body_worker_sha256', 'custody.offset_finish_sha256',
                   'custody.fs_feedback_worker_sha256', 'custody.column_mean_input_pins')
# Per-call fields each successor's config carries when it is written (the later ones do not exist yet and are OMITTED;
# dry-run checks statically that no omitted field is one the successor consumes).
STAGE_PER_CALL = {'reference': PER_CALL_FIELDS[:4], 'body': PER_CALL_FIELDS[:5], 'offset': PER_CALL_FIELDS[:6],
                  'columns_v001': PER_CALL_FIELDS[:7], 'rotation_v001': PER_CALL_FIELDS[:7], 'feedback_v002': PER_CALL_FIELDS[:7],
                  'columns_v003': PER_CALL_FIELDS[:8], 'columns_v005': PER_CALL_FIELDS[:8], 'rotation_v005': PER_CALL_FIELDS[:8],
                  'feedback_v004': PER_CALL_FIELDS[:8], 'column_mean_v004': PER_CALL_FIELDS}
PRODUCER_FLAGS = ('--column-worker-sha256', '--feedback-worker-sha256', '--rotation-worker-sha256', '--current-feedback-worker-sha256')
B1_NEEDLE = "('ddo_free_surface_rotation_root_v005.py',rs['worker_sha256'])"
COLMEAN_PRODUCER_PINS = ('rotation_worker',)
ROUTE_A_CONVERGED_OUTCOME = 'CONVERGED_FINITE_FIXED_POINT'
READER_HEAD = '# ---- c2v002 shared strict route-A reader (verbatim; stages2 CHECK D2)'
ADMISSION_HEAD = '# ---- c2v005 shared stage-config admission (schema V005, members, DDO154 per-call geometry; ROOT_DECISIONS V003 A13)'  # c2v009
TRUNCATION_HEAD = '# ---- c2v003 shared N2 radial truncation'
TRUNCATION_KINDS = ('reference', 'body', 'offset', 'rotation_v001', 'rotation_v005')


def _has_pending(v):
    if isinstance(v, str):
        return v.startswith('PENDING') or v.startswith('NONE_IN_REVIEWED_CODE')
    if isinstance(v, dict):
        return any(_has_pending(x) for x in v.values())
    if isinstance(v, (list, tuple)):
        return any(_has_pending(x) for x in v)
    return False


def load_galaxy_config(gname, member=None):
    """Verify the pinned galaxy-config file from bytes and that it IS the schema copy for gname (c2v006: and member):
    same field set, every value equal to the schema value for that galaxy member, statuses as the schema."""
    key = gname if member is None else (gname, member)
    if key not in GALAXY_CONFIG_FILES:
        raise Refusal('no galaxy-config file for %r' % (key,))
    path, sha = GALAXY_CONFIG_FILES[key]
    raw = Path(path).read_bytes()
    if sha256_bytes(raw) != sha:
        raise Refusal('galaxy-config pin mismatch: %s' % path)
    sraw = Path(GC_SCHEMA[0]).read_bytes()
    if sha256_bytes(sraw) != GC_SCHEMA[1]:
        raise Refusal('galaxy-config schema pin mismatch')
    cfg, schema = json.loads(raw), json.loads(sraw)
    if cfg.get('format') != GC_FORMAT or cfg.get('galaxy') != gname or schema.get('schema') != GC_SCHEMA_NAME or \
            cfg.get('schema') != {'name': GC_SCHEMA_NAME, 'path': str(GC_SCHEMA[0]), 'sha256': GC_SCHEMA[1]} or cfg.get('member') != member:
        raise Refusal('galaxy-config format/galaxy/member/schema identity')
    entry = GC_ENTRY[gname] if member is None else GC_MEMBER_ENTRY[(gname, member)]
    if member is not None and (schema.get('members') or {}).get(gname, {}).get(member, {}).get('entry') != entry:
        raise Refusal('galaxy-config member %r not declared by the schema' % member)
    sf = {f['field']: f for f in schema['fields']}
    if set(cfg['fields']) != set(sf) or len(sf) != len(schema['fields']):
        raise Refusal('galaxy-config field set differs from schema')
    if set(cfg.get('per_call_fields', {})) != set(PER_CALL_FIELDS):
        raise Refusal('galaxy-config per_call_fields differ from driver PER_CALL_FIELDS')
    bad = []
    for n, e in cfg['fields'].items():
        se = sf[n][entry]
        want = 'DDO154_EXACT_LITERAL' if gname == 'DDO154' else se.get('status')
        if canonical(e.get('value')) != canonical(se.get('value')) or e.get('status') != want or e.get('kind') != sf[n]['kind']:
            bad.append(n)
        if gname != 'DDO154' and canonical(e.get('condition')) != canonical(se.get('condition')):
            bad.append(n + ' (condition)')
    slots = sorted(n for n, e in cfg['fields'].items() if e.get('status') == SLOT_STATUS)
    if sorted(cfg.get('declared_input_slots', [])) != slots:
        bad.append('declared_input_slots')
    if bad:
        raise Refusal('galaxy-config fields differ from the schema %s entry: %s' % (entry, bad))
    return {'path': str(path), 'sha256': sha, 'galaxy': gname, 'member': member, 'entry': entry, 'cfg': cfg, 'schema': schema, 'slots': slots}


def gc_value(gc, name):
    """(value, admitted, status) of a galaxy-config field as the driver may use it: admitted means a whitelisted
    non-PER_CALL status and no sentinel value (NONE_IN_REVIEWED_CODE / PENDING...)."""
    e = gc['cfg']['fields'][name]
    st = e['status']
    ok = st in ADMITTED_STATUS and st != 'PER_CALL' and not _has_pending(e['value'])
    if st == 'DERIVED_FROM_BYTES_CONDITIONAL':
        c = e.get('condition') or {}
        ok = c.get('field') in gc['cfg']['fields'] and canonical(gc['cfg']['fields'][c['field']]['value']) == canonical(c.get('equals')) \
            and gc_value(gc, c['field'])[1] and not _has_pending(e['value'])
    return e['value'], ok, st


def ddo_driver_literal_check(g, gc):
    """Every DDO154 driver literal the map lists equals the galaxy-config value (no behaviour change)."""
    f = {n: e['value'] for n, e in gc['cfg']['fields'].items()}
    tpl = json.loads(Path(g['solver_template'][0]).read_text())
    pin = lambda t: {'path': str(t[0]), 'sha256': t[1]}
    prof = json.loads(Path(g['profile'][0]).read_bytes())['galaxies']['DDO154']['HI_plus_He']['s_edges_kpc2']
    pairs = [('galaxy.key', 'DDO154'), ('custody.seed_sha256', g['base_seed'][1]), ('source.profile', pin(g['profile'])),
             ('source.monotone_source', pin(g['monotone_source'])), ('source.coefficients', pin(g['default_coefficients'])),
             ('observation.binding', pin(g['column_mean_binding'])), ('radial.n_columns', g['n_columns']),
             ('output.n_queries', g['n_queries']), ('geometry.registered', g['registered_geometry']),
             ('entropy.K_factor', g['default_entropy_K_factor']), ('driver.fixed_args', FIXED_ARGS),
             ('brackets.repro_overrides', g['repro_rule_overrides']),
             ('brackets.rule_factors', {k: LE_RULE_DEFAULTS[k] for k in ('rfs_factors', 'le_first_factors', 'le_next_factors')}),
             ('brackets.solver_template', dict(pin(g['solver_template']), solver=tpl['solver'])),
             ('brackets.fs_nominal_absolute_bracket_m2_s2', tpl['solver']['enthalpy_bracket']),
             # c2v005: the saved chain's producers (the reviewed bases) are the DDO literals of the producer fields
             ('custody.body_worker_sha256', GENERALIZED['body']['base'][1]),
             ('custody.fs_feedback_worker_sha256', GENERALIZED['feedback_v002']['base'][1]),
             ('radial.outer_edge_kpc', float(math.sqrt(prof[-1])))]
    rows = [{'field': n, 'driver_literal': v, 'equal': canonical(f[n]) == canonical(_jsonable(v))} for n, v in pairs]
    bad = [r['field'] for r in rows if not r['equal']]
    if bad:
        raise Refusal('DDO154 driver literals differ from the galaxy config: %s' % bad)
    return rows


def ngc_driver_value_check(g, gc):
    """c2v005: NGC3198 driver values equal the galaxy-config (schema V003 NGC entry) values; undecided fields are reported."""
    f = {n: e['value'] for n, e in gc['cfg']['fields'].items()}
    tpl = json.loads(Path(g['solver_template'][0]).read_text())
    geo = f['geometry.registered']
    rows = [{'field': 'geometry.registered', 'equal': isinstance(geo, dict) and set(geo) == set(g['registered_geometry'])
             and all(isinstance(geo[k], (int, float)) and float(geo[k]) == float(v) for k, v in g['registered_geometry'].items())},
            {'field': 'radial.n_columns', 'equal': f['radial.n_columns'] == g['n_columns_by_member'][gc.get('member')]},
            {'field': 'observation.binding', 'equal': f['observation.binding'] == {'path': str(g['column_mean_binding'][0]), 'sha256': g['column_mean_binding'][1]}},
            {'field': 'output.n_queries', 'equal': f['output.n_queries'] == g['n_queries']},
            {'field': 'entropy.K_factor', 'equal': f['entropy.K_factor'] == g['default_entropy_K_factor']},
            {'field': 'source.profile', 'equal': f['source.profile'] == {'path': str(g['profile'][0]), 'sha256': g['profile'][1]}},
            {'field': 'source.coefficients', 'equal': f['source.coefficients'] == {'path': str(g['default_coefficients'][0]), 'sha256': g['default_coefficients'][1]}},
            {'field': 'brackets.solver_template', 'equal': f['brackets.solver_template'] == {'path': str(g['solver_template'][0]), 'sha256': g['solver_template'][1], 'solver': tpl['solver']}},
            {'field': 'brackets.fs_nominal_absolute_bracket_m2_s2', 'equal': f['brackets.fs_nominal_absolute_bracket_m2_s2'] == tpl['solver']['enthalpy_bracket']}]
    bad = [r['field'] for r in rows if not r['equal']]
    if bad:
        raise Refusal('NGC3198 driver values differ from the galaxy config: %s' % bad)
    return rows


def _gc_entry(e):
    return {k: e[k] for k in ('value', 'status', 'condition') if k in e}


def stage_config_object(kind, gc, per_call, omit_missing_per_call=True, producers=None):
    """The config of successor `kind`.  per_call: {field: value from bytes or the call spec} (status PER_CALL).  A
    per-call field absent from per_call is omitted (call mode) or kept as the galaxy-config entry (probe mode).
    producers: {name: {path, sha256}} for the successor's PRODUCER_PINS; absent -> the sentinel NONE_IN_REVIEWED_CODE
    (probe mode), which the successor refuses."""
    gname = gc['galaxy']
    fields, omitted = {}, []
    for n, e in gc['cfg']['fields'].items():
        if n in per_call:
            fields[n] = {'value': per_call[n], 'status': 'PER_CALL'}
        elif n in PER_CALL_FIELDS and omit_missing_per_call:
            omitted.append(n)
        else:
            fields[n] = _gc_entry(e)
    obj = {'format': GENERALIZED[kind]['format'], 'schema': {'name': GC_SCHEMA_NAME, 'path': str(GC_SCHEMA[0]), 'sha256': GC_SCHEMA[1]},
           'galaxy': gname, 'fields': fields}
    if gc.get('member') is not None:  # c2v006 (A2): declared alternative member; the c2v004 admission checks its entry
        obj['member'] = gc['member']
    names = tuple(GENERALIZED[kind].get('producer_pins', {}))
    if names:
        obj['producer_pins'] = producers if producers is not None else {k: 'NONE_IN_REVIEWED_CODE' for k in names}
    elif producers is not None:
        raise Refusal('c2v005 internal: %s takes no producer pins' % kind)
    return obj, omitted


def galaxy_config_argv(kind, path, sha):
    if GENERALIZED[kind]['flags'] == 'nargs2':
        return ['--galaxy-config', str(path), sha]
    return ['--galaxy-config', str(path), '--galaxy-config-sha256', sha]


def split_galaxy_config_argv(argv):
    """(argv without the galaxy-config tokens, the galaxy-config tokens)."""
    argv = [str(a) for a in argv]
    if '--galaxy-config' not in argv:
        return argv, []
    i = argv.index('--galaxy-config')
    j = i + 2
    if j < len(argv) and not argv[j].startswith('--'):
        j += 1  # nargs=2 form
    if j < len(argv) and argv[j] == '--galaxy-config-sha256':
        j += 2
    return argv[:i] + argv[j:], argv[i:j]


def route_a_reported_iteration(cp, identity, cm=None):
    """Final converged iteration reported by the route-A checkpoint's own records: the SAME rule as the
    successors' shared route_a_final_iteration (CHECK_V001 D2/D3), without a declared value (this driver is
    what supplies route_a.accepted_iteration).  Every entry named iteration_* is a directory iteration_NNNN
    with exactly four ASCII digits; contiguous from 0; START.json and COMPLETED.json bound to this identity,
    to their iteration and to each other; converged a bool, True only at the last; every attempts/*.end.json
    of this identity and exactly one CONVERGED_FINITE_FIXED_POINT.  Blocked on any ambiguity."""
    if cm is None:
        cm = exec_verified(AUX['checkpoint_module'][0], AUX['checkpoint_module'][1], 'c2v004_ckpt_iter')
    cp = Path(cp)
    its = []
    for x in sorted(cp.iterdir(), key=lambda q: q.name):
        if not x.name.startswith('iteration_'):
            continue
        d = x.name[len('iteration_'):]
        if len(d) != 4 or any(ch not in '0123456789' for ch in d) or not x.is_dir():
            raise Blocked('ROUTE_A_ITERATION_AMBIGUOUS: unexpected checkpoint entry ' + x.name)
        its.append(int(d))
    if not its or its != list(range(len(its))):
        raise Blocked('ROUTE_A_ITERATION_AMBIGUOUS: iterations %s are not contiguous from 0' % (its,))
    converged = []
    for i in its:
        folder = cp / ('iteration_%04d' % i)
        if not (folder / 'START.json').is_file() or not (folder / 'COMPLETED.json').is_file():
            raise Blocked('ROUTE_A_ITERATION_AMBIGUOUS: iteration %d lacks START or COMPLETED' % i)
        s = cm._read(str(folder / 'START.json'), 'iteration_start')
        c = cm._read(str(folder / 'COMPLETED.json'), 'iteration_completed')
        if s['iteration'] != i or c['iteration'] != i or s['identity_sha256'] != identity or c['identity_sha256'] != identity \
                or c['iteration_start_sha256'] != s['payload_sha256'] or type(c['converged']) is not bool:
            raise Blocked('ROUTE_A_ITERATION_AMBIGUOUS: records of iteration %d not bound to this identity/iteration' % i)
        if c['converged']:
            converged.append(i)
    if converged != [its[-1]]:
        raise Blocked('ROUTE_A_ITERATION_AMBIGUOUS: converged %s of present %s; exactly the last must be converged' % (converged, its))
    ad = cp / 'attempts'
    if not ad.is_dir():
        raise Blocked('ROUTE_A_ITERATION_AMBIGUOUS: no attempts directory')
    ends = []
    for x in sorted(ad.glob('*.end.json'), key=lambda q: q.name):
        rec = cm._read(str(x), 'attempt_end')
        if rec['identity_sha256'] != identity:
            raise Blocked('ROUTE_A_ITERATION_AMBIGUOUS: attempt_end of another identity ' + x.name)
        if rec['outcome'] == ROUTE_A_CONVERGED_OUTCOME:
            ends.append(x.name)
    if len(ends) != 1:
        raise Blocked('ROUTE_A_ITERATION_AMBIGUOUS: %d attempt_end records report %s (exactly one required)'
                      % (len(ends), ROUTE_A_CONVERGED_OUTCOME))
    return its[-1]


def _block(text, head, end):
    if text.count(head) != 1:
        return None
    i = text.index(head)
    return text[i:text.index(end, i) + len(end)]


def binding_blockers(scripts=None):
    """Blockers of the c2v005 binding, found from the successors' bytes (independent of the galaxy).  The stages2 wiring:
    every successor pins schema V003 and its own format; the shared admission, the strict route-A reader and the N2
    truncation blocks are byte-identical where present; the reference successor binds only the reference module
    successor; body pins the body base successor; both rotations pin the join successor; producer pins are exactly the
    driver's; B1 (column mean never verifies against the fixed reviewed rotation v005 file)."""
    out = []
    blocks = {'admission': {}, 'reader': {}, 'truncation': {}}
    for kind, (path, sha) in (SCRIPTS if scripts is None else scripts).items():  # C2V010 (u): tail ON passes the active table
        if kind not in GENERALIZED:
            continue
        text = Path(path).read_text()
        m = exec_verified(path, sha, 'c2v005_bind_' + kind)
        gen = GENERALIZED[kind]
        if tuple(getattr(m, 'SCHEMA', ())) != (GC_SCHEMA[0], GC_SCHEMA[1]):
            out.append('SCHEMA_PIN: %s pins %r, not schema V003 %s' % (Path(path).name, getattr(m, 'SCHEMA', None), GC_SCHEMA[1][:16]))
        if getattr(m, 'CONFIG_FORMAT', None) != gen['format']:
            out.append('CONFIG_FORMAT: %s declares %r; the driver writes %r' % (Path(path).name, getattr(m, 'CONFIG_FORMAT', None), gen['format']))
        if tuple(getattr(m, 'PRODUCER_PINS', ())) != tuple(gen.get('producer_pins', {})):
            out.append('PRODUCER_PINS: %s declares %r; the driver writes %r' % (Path(path).name, getattr(m, 'PRODUCER_PINS', ()), tuple(gen.get('producer_pins', {}))))
        blocks['admission'][kind] = _block(text, ADMISSION_HEAD, " return galaxy,{n:F[n]['value'] for n in used},cfg\n")
        if kind != 'column_mean_v004':
            blocks['reader'][kind] = _block(text, READER_HEAD, ' return its[-1]\n')
        if kind in TRUNCATION_KINDS:
            blocks['truncation'][kind] = _block(text, TRUNCATION_HEAD, ' return hits[0]\n')
        if kind in ('rotation_v001', 'rotation_v005') and tuple(m.PINS.get('join', ())) != MODULE_SUCCESSORS['join']['successor']:
            out.append('JOIN_PIN: %s pins join %r, not the join successor' % (Path(path).name, m.PINS.get('join')))
        if kind == 'body' and tuple(m.PINS.get('base', ())) != MODULE_SUCCESSORS['body_base']['successor']:
            out.append('BODY_BASE_PIN: %s pins base %r, not the body base successor' % (Path(path).name, m.PINS.get('base')))
        if kind == 'reference' and ("a.reference_sha256!='%s'" % AUX['reference_module'][1]) not in text:
            out.append('REFERENCE_MODULE: %s does not bind the reference module successor %s' % (Path(path).name, AUX['reference_module'][1][:16]))
        if kind == 'column_mean_v004' and B1_NEEDLE in text:
            out.append('B1_COLMEAN_PINS_REVIEWED_ROTATION_FILE: %s still verifies against the fixed reviewed rotation v005 file' % Path(path).name)
    for name, per in blocks.items():
        vals = set(per.values())
        if None in vals or len(vals) != 1:
            out.append('SHARED_BLOCK_%s not byte-identical in %s' % (name.upper(), sorted(per)))
    return out


def producer_pin(kind, sha, extra=None):
    """{path, sha256} of the script with this sha among {the successor of `kind`, its reviewed base}; else refuse.
    C2V010 (u): extra = SCRIPTS_UVT in a tail-ON call only (its uvt successor is then also a whitelisted producer)."""
    for path, s in (SCRIPTS[kind], GENERALIZED[kind]['base']) + ((extra[kind],) if extra and kind in extra else ()):
        if sha == s:
            return {'path': str(path), 'sha256': s}
    raise Refusal('c2v005: producer %s of %s is neither the successor nor its reviewed base' % (sha, kind))


def rotation_producer_pin(sha, extra=None):
    return producer_pin('rotation_v005', sha, extra)


def probe_stage_admission(kind, path, sha, scripts=None):
    """DRY-RUN ONLY: the successor's own config-admission function on the written config file (C2V010: of the active script)."""
    scripts = SCRIPTS if scripts is None else scripts
    m = exec_verified(scripts[kind][0], scripts[kind][1], 'c2v005_probe_' + kind)
    try:
        if kind == 'column_mean_v004':
            pins, nc, nphi, nz, obsv, rotw = m.galaxy_config((str(path), sha))
            vals = {'PINS': [[p, s] for p, s in pins.items()], 'radial.n_columns': nc, 'mesh.n_phi': nphi, 'column.n_z': nz,
                    'observation': obsv, 'producer_pins.rotation_worker': rotw}
        else:
            vals = m.galaxy_config(str(path), sha)
            if isinstance(vals, tuple):
                vals = {'fields': vals[0], 'producer_pins.' + tuple(GENERALIZED[kind]['producer_pins'])[0]: vals[1]}
        return {'accepted': True, 'values': _jsonable(vals)}
    except Exception as exc:
        return {'accepted': False, 'refusal': '%s: %s' % (type(exc).__name__, exc)}


def probe_route_a_iteration(kind, cp, identity, declared):
    """DRY-RUN ONLY: the successor's own (shared) route-A iteration function on the (saved) checkpoint records."""
    m = exec_verified(SCRIPTS[kind][0], SCRIPTS[kind][1], 'c2v005_iter_' + kind)
    if not hasattr(m, 'route_a_final_iteration'):
        return {'applicable': False}
    cm = exec_verified(AUX['checkpoint_module'][0], AUX['checkpoint_module'][1], 'c2v005_iter_ckpt')
    try:
        it = m.route_a_final_iteration(cm, Path(cp), identity, declared)
        return {'applicable': True, 'iteration': it, 'equals_config': it == declared}
    except Exception as exc:
        return {'applicable': True, 'refusal': '%s: %s' % (type(exc).__name__, exc)}


_CONSUMED = {}


def consumed_fields(kind):
    """Field names the successor consumes, read from its own module constants (inert load; cached per process)."""
    if kind not in _CONSUMED:
        m = exec_verified(SCRIPTS[kind][0], SCRIPTS[kind][1], 'c2v005_consumed_' + kind)
        for name in ('USED', 'NEEDED', 'CONSUMED'):
            if hasattr(m, name):
                _CONSUMED[kind] = sorted(getattr(m, name))
                break
        else:
            raise Refusal('c2v005 internal: %s declares no consumed-field constant' % kind)
    return list(_CONSUMED[kind])


def pending_probe(kind, gc, per_call, producers, inputs_dir, tag=''):
    """DRY-RUN ONLY (c2v005): when a stage config cannot be written because per-call values are pending, write a PROBE
    copy whose pending values are the PENDING placeholders themselves and run the successor's own admission on it.
    Evidence that the stage refuses ONLY on pending values (and on any NONE field it consumes)."""
    obj, _ = stage_config_object(kind, gc, per_call, omit_missing_per_call=False, producers=producers)
    p = Path(inputs_dir) / ('galaxy_config_%s%s_PENDING_PROBE.json' % (kind, ('_' + tag) if tag else ''))
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        raise Refusal('dry-run probe exists: %s' % p)
    raw = (json.dumps(_jsonable(obj), indent=1, allow_nan=False) + '\n').encode()
    p.write_bytes(raw)
    s = sha256_bytes(raw)
    adm = probe_stage_admission(kind, p, s)
    consumed = set(consumed_fields(kind))
    pend = sorted(n for n, e in obj['fields'].items() if n in consumed and _has_pending(e['value']))
    if 'producer_pins' in obj and _has_pending(obj['producer_pins']):
        pend.append('producer_pins')
    return {'path': str(p), 'sha256': s, 'admission': adm, 'consumed_fields_pending_or_none': pend}


# ----------------------------------------------------------------------------- the chain
PENDING_ROUTE_A = 'PENDING_ROUTE_A_OUTPUTS'
PENDING_SLOT = 'PENDING_N3_MONOTONE_SOURCE_REDUCER_STREAM'


def template_mapping_check(ni, solver):
    """c2v005 (N4): the NGC solver template must be the DDO mapping applied to THIS call's seed HI controls
    (binding/inputs/make_ngc_solver_template_c2v005.py); refuse on any difference."""
    kpc = ni['kpc_m']
    want = {'search_step': ni['hi_search_step_kpc'] * kpc, 'search_limit': ni['hi_search_limit_kpc'] * kpc,
            'root_tolerance': ni['hi_root_tolerance_kpc'] * kpc, 'enthalpy_root_tolerance': 299792458.0 ** 2 * ni['hi_log_lapse_tolerance']}
    bad = [k for k, v in want.items() if solver.get(k) != v]
    if bad:
        raise Refusal('NGC solver template is not the N4 mapping of this call seed HI controls: %s' % bad)
    return {'checked': sorted(want), 'equal': True}


def execute_chain(ctx):
    sp = ctx.spec
    gname = sp['galaxy']
    g = GALAXIES[gname]
    ngc = gname != 'DDO154'
    sv = ctx.saved
    uvt = uvt_info(sp['numerics']['uv_tail']) if 'uv_tail' in sp['numerics'] else None  # C2V010 (u): None = tail OFF (every statement of the chain is then the v009 one)
    uvt_act = uvt_active(uvt_is_nodes(sp['numerics'].get('uv_tail')))  # C2V010 r4 (R2): nodes_v001 -> the nodes tables
    uvt_extra = uvt_act['scripts'] if uvt is not None else None
    uvx = None
    ro1_off = uvt is None and route_a_ro1_workers(sp)  # C2V010 r4 (R5): tail OFF on the RO1 c2v002 workers (declared)
    if uvt is not None:
        ctx.scripts = dict(SCRIPTS, **uvt_act['scripts'], route_a_tail_manifest=uvt_act['aux']['manifest_writer'])
    P = sp['numerics']['picard']['passes']
    bound = sp['numerics']['picard']['speed_change_bound_km_s']
    workers = sp['numerics']['column_workers']
    brackets = sp['numerics']['brackets']
    ef = sp['physical']['entropy_K_factor']
    efs = repr(ef)
    coeff_path, coeff_sha = sp['coefficients']['path'], sp['coefficients']['sha256']
    verify_pin(coeff_path, coeff_sha, 'coefficient grid')
    gc = load_galaxy_config(gname, sp.get('member'))  # c2v006: pinned file = schema V004 copy (member: A2 alternative)
    refusals = []

    def refuse(where, cls, msg):
        """c2v005: a remaining refusal.  Run mode: BLOCKED before any further stage.  Simulate: recorded, planning goes on."""
        refusals.append({'where': where, 'class': cls, 'refusal': msg})
        if ctx.mode == 'run':
            raise Blocked('%s [%s]: %s' % (where, cls, msg))

    info = {}
    if not ngc:
        seed_obj, changed, reusable = per_call_seed(sp)
        if reusable:
            seed_path, seed_sha = g['base_seed']
        else:
            seed_path, seed_sha = ctx.write_input('seed_c2v001.json', seed_obj)
        seed_path = Path(seed_path)
        ni = seed_obj['numerical_inputs']
        info['seed'] = {'path': str(seed_path), 'sha256': seed_sha, 'base_seed_reused': reusable, 'changed_fields': changed}
        literal_rows = ddo_driver_literal_check(g, gc)
    else:
        literal_rows = ngc_driver_value_check(g, gc)
        ra_in = sp['route_a_inputs']
        if route_a_inputs_pending(ra_in):
            # c2v006: nothing under a declared (pending) route-A directory is opened; placeholders only.
            seed_path, seed_sha, ni = Path('%s(seed path)' % PENDING_ROUTE_A), '%s(custody.seed_sha256)' % PENDING_ROUTE_A, None
            refuse('route_a', 'PENDING_ROUTE_A_OUTPUTS', 'NGC3198 route-A outputs (seed, attempt, checkpoint) are not supplied yet; '
                   'route B consumes them from the NGC route-A lane (route A is not run by this driver)')
            for where, what in NGC_DEFERRED_ROUTE_A_CHECKS:  # c2v006 (D8): checks that need route-A bytes, listed by name
                refuse(where, 'PENDING_ROUTE_A_OUTPUTS', 'needs route-A bytes: ' + what)
            info['route_a_inputs_declared'] = ra_in
        else:
            seed_path = Path(ra_in['seed']['path'])
            seed_sha = verify_pin(seed_path, ra_in['seed']['sha256'], 'NGC route-A seed')
            seed_doc = json.loads(seed_path.read_bytes())
            ni = seed_doc['numerical_inputs']
            info['route_a_seed_coefficients'] = ngc_seed_coefficient_check(seed_doc, sp['coefficients'], g)  # c2v006 (A5, D1)
        info['seed'] = {'path': str(seed_path), 'sha256': seed_sha, 'source': 'route_a_inputs.seed (NGC route-A lane)'}
        info['member'] = {'member': sp.get('member'), 'label': ('PRIMARY' if sp.get('member') is None else
                          gc['schema']['members']['NGC3198'][sp['member']]['label']),
                          'entropy_K_member': sp['physical'].get('entropy_K_member')}
    info['galaxy_config'] = {'path': gc['path'], 'sha256': gc['sha256'], 'driver_literal_check': literal_rows}
    if ni is not None:
        if ni['kpc_m'] != KPC_M:
            raise Refusal('seed kpc_m differs from driver constant')
        call_phys = {k: ni[k] for k in ('Eref_J', 'ell_F_m', 'gamma')}
        if ngc:
            s = sp['physical']['common_scale_s']
            want = {'Eref_J': s * sp['physical']['Eref_J'], 'gamma': s * sp['physical']['gamma'], 'ell_F_m': sp['physical']['ell_F_m']}
            if any(call_phys[k] != want[k] for k in want):
                raise Refusal('NGC3198: call physical parameters (times s) differ from the route-A seed numerical_inputs')
    else:
        call_phys = None
    tr = sp['numerics']['truncation']
    if ni is not None:
        kgrid = float(ni['composite_grid_spec']['breaks_inverse_kpc'][-1])
        if tr['kmax_inverse_kpc'] is not None and tr['kmax_inverse_kpc'] > kgrid:
            raise Refusal('mask kmax exceeds the composite grid edge %.6g/kpc' % kgrid)
        kmask_m = (tr['kmax_inverse_kpc'] if tr['kmax_inverse_kpc'] is not None else kgrid) / KPC_M
    else:
        kmask_m = None
    coeff_default = (coeff_path == str(g['default_coefficients'][0]) and coeff_sha == g['default_coefficients'][1])
    reuse_path, reuse_sha = GENERALIZED['reference']['base']  # c2v005: the REVIEWED reference worker is the reuse module
    percall = {'custody.seed_sha256': seed_sha, 'source.coefficients': {'path': str(coeff_path), 'sha256': coeff_sha}}
    # c2v005: declared input slots (NGC3198 source.monotone_source, N3) come from the call spec only
    for k in gc['slots']:
        v = (sp.get('source_slots') or {}).get(k, PENDING_SLOT)
        percall[k] = v
        if _has_pending(v):
            refuse(k, 'PENDING_N3_MONOTONE_SOURCE', '%s is a DECLARED_INPUT_SLOT (N3) not yet filled by the reviewed reducer output' % k)
    gc_written = {}
    gfields = {}  # C2V008 (a): per-call geometry config fields; stays empty at the registered geometry and for NGC3198

    def stage_gc(kind, tag='', producers=None):
        """Write (once per name) the per-stage config of successor `kind`; returns (path, sha, meta)."""
        name = 'galaxy_config_%s%s.json' % (kind, ('_' + tag) if tag else '')
        if name in gc_written:
            return gc_written[name]
        missing = [k for k in STAGE_PER_CALL[kind] if k not in percall]
        if missing:
            raise Refusal('c2v005 internal: per-call fields %s not yet computed for %s' % (missing, kind))
        pc = {k: percall[k] for k in STAGE_PER_CALL[kind]}
        pc.update({k: percall[k] for k in gc['slots'] if k in consumed_fields(kind)})  # a slot travels only to its consumers
        # C2V008 (a): per-call geometry fields (empty at the registered geometry) travel only to their consumers too
        pc.update({k: v for k, v in gfields.items() if k in consumed_fields(kind)})
        obj, omitted = stage_config_object(kind, gc, pc, omit_missing_per_call=True, producers=producers)
        pending = sorted(k for k, v in pc.items() if _has_pending(v))
        if producers is not None and _has_pending(producers):
            pending.append('producer_pins')
        meta = {'format': GENERALIZED[kind]['format'], 'galaxy_config_file': {'path': gc['path'], 'sha256': gc['sha256']},
                'per_call_fields': sorted(pc), 'omitted_per_call_fields': omitted}
        if producers is not None:
            meta['producer_pins'] = producers
        if pending:  # simulate only: never hash a placeholder; the file is not written
            p = ctx.out / 'inputs' / name
            s = 'PENDING_SHA256(%s)' % p
            meta.update(path=str(p), sha256=s, written=False, pending_fields=pending)
            if ctx.mode != 'run':
                meta['pending_probe'] = pending_probe(kind, gc, pc, producers, ctx.out / 'inputs', tag)
        else:
            p, s = ctx.write_input(name, obj)
            meta.update(path=str(p), sha256=s, written=True)
        gc_written[name] = (p, s, meta)
        return gc_written[name]

    def gen_request(name, key, argv, tag='', module_patches=None, mask=None, producers=None, stage_globals=None):
        """Request for a gal_c2v003 successor: c2v003 argv + galaxy-config tokens appended; no stage globals (C2V008 (a):
        except the reference PROFILE/PROFILE_SHA at a per-call geometry, as c2v003c)."""
        p, s, meta = stage_gc(key, tag, producers)
        req = ctx.request(name, key, list(argv) + galaxy_config_argv(key, p, s), stage_globals=stage_globals or {},
                          module_patches=module_patches, mask=mask)
        req['galaxy_config'] = meta
        return req

    producer_log = []

    def producer(dirs, key, flag, stage, admitted=False):
        """c2v004 rule: sha of the script that produced the upstream output(s).  run: SCRIPTS[key] (this call ran it);
        simulate on SAVED outputs, or an ADMITTED upstream in any mode (c2v005): the worker_sha256 recorded in their
        start.json, which must be the successor or its reviewed base."""
        run_value = ctx.scripts[key][1]  # C2V010 (u): the active script (SCRIPTS unless tail ON)
        val, src = run_value, 'SCRIPTS[%s] (this call runs it)' % key
        if ctx.mode != 'run' or admitted:
            recs = [Path(x) / 'start.json' for x in dirs]
            have = [p for p in recs if p.is_file()]
            if have:
                vals = {json.loads(p.read_text())['worker_sha256'] for p in have}
                if len(have) != len(recs) or len(vals) != 1:
                    raise Refusal('c2v005: mixed upstream producers for %s %s' % (stage, flag))
                val, src = vals.pop(), 'worker_sha256 recorded in the %s upstream start.json' % ('admitted' if admitted else 'saved')
                producer_pin(key, val, uvt_extra)
            elif admitted:
                raise Refusal('c2v005: admitted %s output has no start.json to name its producer' % key)
        producer_log.append({'stage': stage, 'flag': flag, 'value': val, 'source': src, 'run_mode_value': run_value,
                             'run_mode_differs': val != run_value})
        return val

    # c2v003: route-A prep by node count (DDO154 only; NGC3198 route A is run by the NGC route-A lane).
    if not ngc:
        nk = int(ni['fourier_points_per_axis'])
        if nk <= PREP_V007_MAX_AXIS_NODES:
            prep_key = 'prep'
        elif nk <= PREP_V008_MAX_AXIS_NODES:
            prep_key = 'prep_v008'
            verify_pin(PREP_V008_REVIEW[0], PREP_V008_REVIEW[1], 'prep V008 review')
        elif nk <= PREP_V009_MAX_AXIS_NODES:  # C2V009 (a)
            prep_key = 'prep_v009'
        else:
            raise Refusal('%d nodes/axis exceeds every route-A prep budget (%d)' % (nk, PREP_V009_MAX_AXIS_NODES))
        prep_path, prep_sha = AUX[prep_key]
        prep_info = {'path': str(prep_path), 'sha256': prep_sha, 'axis_nodes': nk,
                     'rule': 'V007 for <=%d nodes/axis (unchanged); V008 for %d..%d (review %s)'
                             % (PREP_V007_MAX_AXIS_NODES, PREP_V007_MAX_AXIS_NODES + 1, PREP_V008_MAX_AXIS_NODES, PREP_V008_REVIEW[1][:16])}
        if prep_key == 'prep_v009':  # C2V009 (a): only here does the record differ from c2v008
            prep_info['rule'] += '; V009 for %d..%d (declared G5/G6 only; review: separate, named by prereg V006)' % (
                PREP_V008_MAX_AXIS_NODES + 1, PREP_V009_MAX_AXIS_NODES)

    # C2V008 (a), from c2v003b (c2v003c @L1338): per-call geometry inputs (DDO154 only; None at the registered geometry:
    # pinned files, plan unchanged).  Then the stage-admission probe: run mode is BLOCKED here, before any stage, when a
    # successor's own admission refuses the per-call geometry fields (simulate: recorded, planning goes on).
    geo = geometry_inputs(ctx, sp) if not ngc else None
    profile_sha = None if ngc else (geo['profile'][1] if geo is not None else g['profile'][1])
    if not ngc:
        src_path, src_sha = geo['monotone'] if geo is not None else g['monotone_source']
    if geo is not None:
        gfields.update(geometry_config_fields(geo))
        probe = geometry_admission_probe(ctx, gc, gfields)
        info['geometry'] = dict(geo['record'], config_fields=gfields, stage_admission_probe=probe)
        ctx.geometry = info['geometry']
        if not probe['admitted']:
            refuse('geometry', 'GEOMETRY_NOT_ADMITTED_BY_STAGE_BINDING',
                   'distance_Mpc %r != registered %r: the pinned gal_c2v005 stages refuse the per-call geometry config fields '
                   '(their own admission, schema V005): %s%s. No stage is run.' % (sp['physical']['distance_Mpc'], g['registered_geometry']['distance_Mpc'],
                                               '; '.join('%s: %s' % kv for kv in sorted(probe['refused'].items())),
                                               '' if probe['controls_accepted'] else ' (registered-geometry control copies also refused)'))

    if uvt is not None:  # C2V010 (u): tail-ON planning (kept regions, certificates, route-B config, route-A request)
        uvx = uvt_plan(ctx, sp, ni, refuse, uvt_prep_patches(coeff_default, coeff_path, coeff_sha, geo, prep_path, prep_sha))
        ctx.uv_tail = uvx

    # ---------------- route A
    adm = sp.get('admit') or {}
    if ngc:
        ra_in = sp['route_a_inputs']
        if route_a_inputs_pending(ra_in):
            att, cp = Path('%s(attempt_directory)' % PENDING_ROUTE_A), Path('%s(checkpoint_directory)' % PENDING_ROUTE_A)
            info['route_a'] = {'mode': 'pending_ngc_route_a_lane', 'attempt': str(att), 'checkpoint': str(cp),
                               'declared': ra_in if isinstance(ra_in, dict) else None}
        else:
            att, cp = Path(ra_in['attempt_directory']), Path(ra_in['checkpoint_directory'])
            fin = json.loads((att / 'finish.json').read_text())
            if fin['status'] != 'RETURNED_ACTUAL_RESULT' or sha256_file(att / 'result.json') != ra_in['result_sha256'] or fin['result_sha256'] != ra_in['result_sha256']:
                raise Refusal('NGC route-A attempt does not verify')
            info['route_a'] = {'mode': 'admitted_ngc_route_a_lane', 'attempt': str(att), 'checkpoint': str(cp)}
    elif 'route_a' in adm:
        a = adm['route_a']
        att, cp = Path(a['attempt_directory']), Path(a['checkpoint_directory'])
        fin = json.loads((att / 'finish.json').read_text())
        if fin['status'] != 'RETURNED_ACTUAL_RESULT' or sha256_file(att / 'result.json') != a['result_sha256'] or fin['result_sha256'] != a['result_sha256']:
            raise Refusal('admitted route-A attempt does not verify')
        info['route_a'] = {'mode': 'admitted', 'attempt': str(att), 'checkpoint': str(cp)}
    else:
        d = ctx.stage_dir('route_a')
        sa = (sv.get('route_a') or {}) if ctx.mode != 'run' else {}
        att = Path(sa['attempt']) if 'attempt' in sa else d / 'attempt_000'
        cp = Path(sa['checkpoint']) if 'checkpoint' in sa else d / 'checkpoint'
        patches = []
        prep_set = {}  # C2V008 (a): one prep module patch as c2v003c (same key order; identical to c2v007 without geometry)
        if not coeff_default:
            prep_set.update({'COEFFICIENT': {'__path__': coeff_path}, 'COEFFICIENT_SHA': coeff_sha})
        if geo is not None:
            prep_set['C'] = {'__path__': geo['C_dir']}  # c2v003b: prep reads C/PROFILE_NAME and C/<binding V003>
        if prep_set:
            patches.append({'path': str(prep_path), 'sha256': prep_sha, 'set': prep_set})
        # C2V007 (b): N = 1 -> exactly the c2v006 request (reviewed worker c4cb6826 + reviewed solver 44d9c23c);
        # N > 1 -> the parallel worker successor with the parallel solver and --column-workers N.  Same LOCAL keys and
        # pins, so the prep COEFFICIENT module patch and the prep V008 LOCAL['prep'] dict item apply unchanged.
        ra_workers = route_a_column_workers(sp)
        solver_pin = AUX['solver'] if ra_workers == 1 else PARALLEL_ROUTE_A['solver']
        if uvt is not None:  # C2V010 (u): the uvtail solvers (route_a/; serial 8ef3079b, parallel 7667025b)
            solver_pin = uvt_act['aux']['solver'] if ra_workers == 1 else uvt_act['aux']['solver_parallel']
        ra_argv = ['--seed', seed_path, '--seed-sha256', seed_sha, '--solver', solver_pin[0], '--solver-sha256', solver_pin[1],
                   '--checkpoint-module', AUX['checkpoint_module'][0], '--checkpoint-module-sha256', AUX['checkpoint_module'][1],
                   '--outdir', att, '--checkpoint-directory', cp, '--start-iteration', '0']
        if ra_workers > 1:
            ra_argv += ['--column-workers', str(ra_workers)]
        if uvt is not None:  # C2V010 (u): tail request, certificates, new sidecar directory (the controller creates it)
            ra_argv += uvx['route_a_argv'] + ['--uv-tail-sidecar-directory', d / 'uv_tail_sidecar']
        if ro1_off:  # C2V010 r4 (R5): the RO1 worker CLI with a tail-disabled request (sidecar never created)
            off_p, off_s = ctx.write_input('uv_tail_route_a_request_tail_off_ro1.json', ro1_off_request())
            ra_argv += ['--uv-tail-config', off_p, '--uv-tail-config-sha256', off_s, '--eps-certificate', UVT_TEST_ONLY,
                        '--eps-certificate-sha256', UVT_TEST_ONLY, '--lo-certificate', UVT_TEST_ONLY, '--lo-certificate-sha256', UVT_TEST_ONLY,
                        '--uv-tail-sidecar-directory', d / 'uv_tail_sidecar']
        req = ctx.request('route_a', 'route_a', ra_argv, module_patches=patches)
        if ra_workers > 1:
            req['script'], req['script_sha256'] = str(PARALLEL_ROUTE_A['worker'][0]), PARALLEL_ROUTE_A['worker'][1]
        if uvt is not None:  # C2V010 (u): the RO1 successors of the uvtail workers (same CLI and LOCAL keys); r4: nodes -> nodes workers
            w = uvt_act['route_a']['worker'] if ra_workers == 1 else uvt_act['route_a']['worker_parallel']
            req['script'], req['script_sha256'] = str(w[0]), w[1]
        if ro1_off:  # C2V010 r4 (R5): tail OFF on the RO1 c2v002 workers, the v009 solvers
            w = RO1_ROUTE_A['worker'] if ra_workers == 1 else RO1_ROUTE_A['worker_parallel']
            req['script'], req['script_sha256'] = str(w[0]), w[1]
        if prep_key in ('prep_v008', 'prep_v009'):  # C2V009 (a): v009 is injected the same way as v008
            req['stage_dict_items'] = {'LOCAL': {'prep': {'path': str(prep_path), 'sha256': prep_sha}}}
        ctx.run_stages([req], [d])
        info['route_a'] = {'mode': 'computed', 'attempt': str(att), 'checkpoint': str(cp)}
        info['route_a']['implementation'] = {  # C2V007 (b)
            'column_workers': ra_workers, 'kind': 'REVIEWED_SERIAL' if ra_workers == 1 else 'PARALLEL_C2V001',
            'worker': {'path': req['script'], 'sha256': req['script_sha256']},
            'solver': {'path': str(solver_pin[0]), 'sha256': solver_pin[1]}}
        if uvt is not None:  # C2V010 (u)
            info['route_a']['implementation']['kind'] = (('UVTAIL_NODES_RO1_SERIAL_C2V001' if ra_workers == 1 else 'UVTAIL_NODES_RO1_PARALLEL_C2V001')
                                                         if uvt_is_nodes(sp['numerics'].get('uv_tail')) else
                                                         ('UVTAIL_RO1_SERIAL_C2V001' if ra_workers == 1 else 'UVTAIL_RO1_PARALLEL_C2V001'))
        if ro1_off:  # C2V010 r4 (R5)
            info['route_a']['implementation']['kind'] = 'TAIL_OFF_RO1_SERIAL_C2V010R4' if ra_workers == 1 else 'TAIL_OFF_RO1_PARALLEL_C2V010R4'
            info['route_a']['implementation']['ro1_workers'] = True
    if not ngc:
        info['route_a']['prep'] = dict(prep_info, role=('used by this call' if info['route_a']['mode'] == 'computed' else
                                                        'expected for this grid; the admitted checkpoint records its own (custody.prep_code_pins)'))
    # C2V007 (a) F1 (c2v003c hunk @@ -1229): classify the route-A outcome from its own result.json before any iteration verdict.
    # (A pending NGC attempt path is a PENDING placeholder, never a file: nothing is opened.)
    att_res = Path(att) / 'result.json'
    ra = json.loads(att_res.read_text()) if att_res.is_file() else None
    ra_outcome = route_a_outcome_record(ra, att_res) if ra is not None else None
    ctx.route_a_outcome = ra_outcome
    if ra_outcome is not None:
        info['route_a']['outcome'] = ra_outcome
    # C2V007 (b): a route A computed by this call (run mode) must carry the solver it was launched with in its IDENTITY.
    # Simulate on saved outputs and admitted route A: the solver is recorded (custody.solver_code), not required.
    expected_solver = solver_pin if (info['route_a']['mode'] == 'computed' and ctx.mode == 'run') else None
    if (Path(cp) / 'IDENTITY.json').is_file():
        # c2v005: route_a_custody reads the converged final iteration by the strict rule (no literal 4)
        # C2V008: (a) the call source profile (DDO154; c2v003b); (d) the attempt must belong to this checkpoint (CHECK D1;
        # DDO154 only, as in c2v003c: the NGC route-A result bytes may not be read in this lane, so NGC is left as c2v007)
        cust = route_a_custody(cp, seed_sha, coeff_path, call_phys, outcome=ra_outcome, expected_solver=expected_solver,
                               profile_sha=profile_sha, attempt_result=None if ngc else ra)
        if 'route_a' in adm and cust['identity_sha256'] != adm['route_a']['identity_sha256']:
            raise Refusal('admitted checkpoint identity differs from declared')
        if ngc and cust['identity_sha256'] != sp['route_a_inputs']['identity_sha256']:
            raise Refusal('NGC route-A checkpoint identity differs from route_a_inputs.identity_sha256')
        if uvt is None:  # C2V010 (u): a tail-OFF call never admits a tail-ON route A (never fires on v009 checkpoints)
            uvt_route_a_identity_check(cp, None)
        elif uvt['config_sha256'] is not None:
            uvx['route_a_checkpoint_tail'] = uvt_route_a_identity_check(cp, uvt['config_sha256'])
        else:
            uvx['route_a_checkpoint_tail'] = 'PENDING (certificate sentinel: config sha unknown)'
    else:
        # C2V010 (m2): the R-A F-A fix (REVIEW_DRIVER_V008_C4_V001 sec 6, f0987f41), before any outcome verdict.
        if not ngc and info['route_a']['mode'] == 'admitted':
            raise Refusal('ROUTE_A_CHECKPOINT_MISSING: %s/IDENTITY.json absent; admitted attempt cannot be paired (D1)' % cp)
        if info['route_a']['mode'] == 'computed' and ctx.mode == 'run' and ra_outcome is not None:
            raise StageFailed('ROUTE_A_RESULT_WITHOUT_CHECKPOINT: %s' % cp)
        if ra_outcome is not None:  # C2V007 (a) F1 (c2v003c): no checkpoint but a returned result -> outcome first
            require_route_a_fixed_point(ra_outcome)
        if ngc and not route_a_inputs_pending(sp['route_a_inputs']):  # c2v006: a supplied NGC route A must have its checkpoint
            raise Refusal('NGC route-A checkpoint IDENTITY.json missing under %s' % cp)
        cust = {'identity_sha256': '%s(custody.checkpoint_identity_sha256)' % PENDING_ROUTE_A if ngc else 'PENDING(route_a identity)',
                'iteration': '%s(route_a.accepted_iteration)' % PENDING_ROUTE_A if ngc else 'PENDING(route_a iteration)',
                'start_payload_sha256': 'PENDING', 'g4_ref': {'file_sha256': 'PENDING'}, 'waves_ref': None}
    info['route_a']['custody'] = cust
    if ra is not None:
        info['route_a']['route_a_rows'] = ra['result']['result']['rows']
        if geo is not None:
            info['route_a']['route_a_rows_scope'] = geo['record']['route_a_rows']  # c2v003b
    if uvt is not None:  # C2V010 (u): the route-A tail record, then the manifest stage (reference, body, offset read it)
        u = ((ra or {}).get('result') or {}).get('uv_tail') if ra is not None else None
        if ra is not None and not isinstance(u, dict):
            raise StageFailed('UV_TAIL_ROUTE_A_RECORD_MISSING: %s has no result.uv_tail (a tail-OFF route A in a tail-ON call?)' % att_res)
        if isinstance(u, dict) and uvt['config_sha256'] is not None and u.get('config_sha256') != uvt['config_sha256']:
            raise Refusal('UVT_ADMISSION_MISMATCH: route-A result tail config %r is not this call config %s' % (u.get('config_sha256'), uvt['config_sha256']))
        uvx['route_a_record'] = None if not isinstance(u, dict) else {k: u.get(k) for k in (
            'outcome', 'accepted_iteration', 'M_T_accepted', 'M_T_threshold', 'monitor_status', 'flags', 'production_admissible',
            'boundary_state_digest_at_return', 'config_sha256', 'request_sha256', 'admissibility', 'E_A_rows_km_s_accepted', 'sidecar')}
        if uvx['route_a_record'] is not None:  # C2V010 r4 (R3; A50 item 13): the E^A row radii, in the request's probe order
            uvx['route_a_record'].update(probe_R_m=list(uvx['monitor_probe_R_m']), probe_phi_rad=list(uvx['monitor_probe_phi_rad']),
                                         probe_source='uv_tail request monitor (binding f42c7c65 query_rows[].radius_m; seed azimuths)')
        d = ctx.stage_dir('route_a_tail_manifest')
        mdir = d / 'manifest'
        margv = ['--seed', seed_path, '--seed-sha256', seed_sha, '--attempt-directory', att, '--checkpoint-directory', cp,
                 '--checkpoint-module', AUX['checkpoint_module'][0], '--checkpoint-module-sha256', AUX['checkpoint_module'][1],
                 '--uv-tail-request', uvx['request']['path'], '--uv-tail-request-sha256', uvx['request']['sha256'], '--outdir', mdir]
        mreq = ctx.request('route_a_tail_manifest', 'route_a_tail_manifest', margv, module_patches=uvx['prep_patches'])
        if prep_key in ('prep_v008', 'prep_v009'):  # the same prep the route-A worker ran (LOCAL['prep'] dict item)
            mreq['stage_dict_items'] = {'LOCAL': {'prep': {'path': str(prep_path), 'sha256': prep_sha}}}
        ctx.run_stages([mreq], [d])
        uvx['manifest'] = {'path': str(mdir / 'ROUTE_A_TAIL_MANIFEST.json'), 'sha256': ctx.finish_sha(mdir, 'ROUTE_A_TAIL_MANIFEST.json')}
        if (mdir / 'finish.json').is_file():
            mf = json.loads((mdir / 'finish.json').read_text())
            uvx['manifest'].update(state_digest=mf.get('state_digest'), empty=mf.get('empty'), production_admissible=mf.get('production_admissible'))

    def uvt_argv(kind, source_rotation=None):
        """C2V010 (u): the tail argv of a route-B uvt successor ([] when tail OFF): config, manifest (reference, body,
        offset), the call truncation for the masked kinds, the source rotation (rfs/le columns, le rotation)."""
        if uvt is None:
            return []
        bk = UVT_BINDING_KIND[kind]
        a = ['--uv-tail-config', uvx['config']['path'], '--uv-tail-config-sha256', uvx['config']['sha256']] + uvx['test_only_flag']
        if bk in ('reference', 'body', 'offset'):
            a += ['--route-a-tail-manifest', uvx['manifest']['path'], '--route-a-tail-manifest-sha256', uvx['manifest']['sha256']]
        if bk not in ('reference', 'body') and uvx['truncation_argv'] is not None:
            a += ['--uv-tail-truncation', uvx['truncation_argv']]
        if bk in ('rfs_columns', 'le_columns', 'le_rotation'):
            a += ['--uv-tail-source-rotation-directory', source_rotation]
        return a
    ident = cust['identity_sha256']
    it = cust['iteration']
    info['route_a']['reported_final_iteration'] = it
    percall['custody.checkpoint_identity_sha256'] = ident
    percall['route_a.accepted_iteration'] = it
    reuse_patch = {'path': str(reuse_path), 'sha256': reuse_sha, 'set': {'SEED_SHA': seed_sha, 'IDENTITY': ident}}
    ref_globals = None
    if geo is not None:  # C2V008 (a), c2v003b: homotopy worker PROFILE (reference stage itself; body/offset read it as reuse.PROFILE)
        ref_globals = {}
        for target in (reuse_patch['set'], ref_globals):
            target.update(PROFILE={'__path__': geo['profile'][0]}, PROFILE_SHA=geo['profile'][1])
    mask = None
    if tr['shape'] != 'cube':
        mask = {'shape': tr['shape'], 'kmax_inverse_m': kmask_m, 'g4_file_sha256': cust['g4_ref']['file_sha256'],
                'waves_ref': cust['waves_ref'], 'checkpoint_module': [str(AUX['checkpoint_module'][0]), AUX['checkpoint_module'][1]],
                'cache_module': [str(AUX['cache'][0]), AUX['cache'][1]]}
    common = ['--seed', seed_path, '--checkpoint-directory', cp]
    # c2v005 driver-level galaxy values (NGC3198: from the galaxy config; an undecided field is a refusal)
    if ngc:
        fa, fa_ok, _ = gc_value(gc, 'driver.fixed_args')
        if fa_ok:
            FA = dict(fa)
        else:
            FA = {k: 'NONE_IN_REVIEWED_CODE(driver.fixed_args.%s)' % k for k in FIXED_ARGS}
            refuse('driver.fixed_args', 'UNDECIDED_NGC_FIELD', 'driver.fixed_args is NONE_IN_REVIEWED_CODE for NGC3198 (no ROOT_DECISIONS row)')
    else:
        FA = FIXED_ARGS

    # ---------------- reference (c2v005: generalized successor + reference module successor 1b00add9)
    if 'reference' in adm:
        ref = Path(adm['reference']['directory'])
        verify_pin(ref / 'start.json', adm['reference']['start_sha256'], 'admitted reference start')
        verify_pin(ref / 'finish.json', adm['reference']['finish_sha256'], 'admitted reference finish')
        if not ngc and json.loads((ref / 'start.json').read_text())['source_custody']['sha256'] != profile_sha:  # C2V008 (a), c2v003b
            raise Blocked('REFERENCE_GEOMETRY_MISMATCH: admitted reference was not built from this call source profile')
        r_t = uvt_admitted_record_check(ref / 'start.json', uvt, 'reference')  # C2V010 (u)
        if uvt is not None:
            uvx['admitted_reference_tail'] = r_t
    else:
        d = ctx.stage_dir('reference')
        ref = d / 'reference' if ctx.mode == 'run' else ctx.saved_or('reference', d / 'reference')
        req = gen_request('reference', 'reference', common + ['--reference-module', AUX['reference_module'][0],
                          '--reference-sha256', AUX['reference_module'][1], '--outdir', ref] + uvt_argv('reference'), stage_globals=ref_globals)
        ctx.run_stages([req], [d])
    percall['custody.reference_run'] = {'directory': str(ref), 'start_sha256': ctx.finish_sha(ref, 'start.json'),
                                        'finish_sha256': ctx.finish_sha(ref)}

    # ---------------- body (c2v005: generalized successor; REFERENCE/DATA_PINS travel as custody.reference_run/source.monotone_source)
    if 'body' in adm:
        body = Path(adm['body']['directory'])
        verify_pin(body / 'finish.json', adm['body']['finish_sha256'], 'admitted body finish')
        if not ngc and src_sha not in json.loads((body / 'start.json').read_text())['input_pins'].values():  # C2V008 (a), c2v003b
            raise Blocked('BODY_GEOMETRY_MISMATCH: admitted body was not built from this call monotone source')
        b_t = uvt_admitted_record_check(body / 'finish.json', uvt, 'body')  # C2V010 (u)
        if uvt is not None:
            uvx['admitted_body_tail'] = b_t
    else:
        d = ctx.stage_dir('body')
        body = d / 'body' if ctx.mode == 'run' else ctx.saved_or('body', d / 'body')
        req = gen_request('body', 'body', common + ['--outdir', body] + uvt_argv('body'), module_patches=[reuse_patch])
        ctx.run_stages([req], [d])
    body_fin = ctx.finish_sha(body)
    percall['custody.body_worker_sha256'] = producer([body], 'body', 'config custody.body_worker_sha256', 'offset', admitted='body' in adm)

    # ---------------- offset (generalized successor; COEFF/COEFF_SHA travel as source.coefficients)
    d = ctx.stage_dir('offset')
    off = d / 'offset' if ctx.mode == 'run' else ctx.saved_or('offset', d / 'offset')
    req = gen_request('offset', 'offset', common + ['--body-directory', body, '--body-finish-sha256', body_fin,
                      '--wave-batch', FA['wave_batch'], '--position-batch', FA['position_batch'], '--outdir', off] + uvt_argv('offset'),
                      module_patches=[reuse_patch], mask=mask)
    ctx.run_stages([req], [d])
    if mask is not None:
        # c2v003 (CHECK_V001 s3 corr. 2): refuse to continue unless the mask demonstrably fired.
        tinfo = {'shape': tr['shape'], 'kmax_inverse_m': kmask_m,
                 'scope': 'route A, reference and body unmasked (cube G4); offset real-space total and '
                          'updated_base_arrays full_fields/Phi0/angular_forcing/r0 are a MIXED field (see truncation_mask)'}
        if ctx.mode == 'run' or ((Path(off) / 'unit_response.npz').is_file() and (Path(off) / 'offset_prepared.npz').is_file()):
            tinfo['mask_check'] = mask_fired_check(off, tr['shape'], kmask_m)
            ctx.event(stage='offset', event='mask_check', kept_nodes=tinfo['mask_check']['kept_nodes'],
                      total_nodes=tinfo['mask_check']['total_nodes'])
        else:
            tinfo['mask_check'] = 'PENDING (offset outputs not present in simulate mode)'
        info['truncation'] = tinfo
    off_fin = ctx.finish_sha(off)
    percall['custody.offset_finish_sha256'] = off_fin  # c2v005: no stage global OFFSET_SHA is patched any more
    base = common + ['--offset-directory', off]

    verify_pin(g['solver_template'][0], g['solver_template'][1], 'solver template')
    template = json.loads(Path(g['solver_template'][0]).read_text())['solver']
    if ngc and ni is not None:
        info['solver_template_mapping'] = template_mapping_check(ni, template)
    n = g['n_columns_by_member'][sp.get('member')] if ngc else g['n_columns']  # c2v006: GL10 member = 250 (checked == config)

    def column_pass(tag, key, extra_args, plan_runs):
        """plan_runs: list of (controls_path, controls_sha) or ('GENERATE', controls_obj).  Returns run dirs."""
        dirs, reqs, sdirs = [], [], []
        saved_dirs = sv.get(tag + '_columns') if ctx.mode != 'run' else None
        for j, item in enumerate(plan_runs):
            if item[0] == 'GENERATE':
                cpath, csha = ctx.write_input('%s_controls_%02d.json' % (tag, j), item[1])
            else:
                cpath, csha = item
            dd = ctx.stage_dir('%s_columns_%02d' % (tag, j))
            outc = dd / 'columns'
            if saved_dirs is not None and len(saved_dirs) == len(plan_runs):
                outc = Path(saved_dirs[j])
            cargv = base + ['--controls', cpath, '--controls-sha256', csha] + extra_args + ['--outdir', outc]
            reqs.append(gen_request('%s_columns_%02d' % (tag, j), key, cargv, module_patches=[reuse_patch], mask=mask))  # c2v005: all generalized
            sdirs.append(dd)
            dirs.append(outc)
        # run in waves of `workers` processes (rule mode only; otherwise len==sequential)
        for k in range(0, len(reqs), max(1, workers)):
            ctx.run_stages(reqs[k:k + workers], sdirs[k:k + workers])
        if ctx.mode != 'run' and saved_dirs is not None and len(saved_dirs) != len(plan_runs):
            dirs = [Path(x) for x in saved_dirs]
        return dirs

    def manifest(tag, run_dirs):
        obj = {'runs': [{'directory': str(x), 'finish_sha256': ctx.finish_sha(x)} for x in run_dirs],
               'scope': 'c2v001 generated manifest for %s; complete %d columns required by the stage itself' % (tag, n)}
        return ctx.write_input('%s_manifest.json' % tag, obj)

    def generated_runs(tag, bracket_table, v001=False, split=True):
        """Group indices into column runs.  v001 supports only one global bracket per run."""
        runs = []
        if v001:
            groups = {}
            for i in range(n):
                groups.setdefault(tuple(bracket_table[str(i)]), []).append(i)
            for br, ids in sorted(groups.items(), key=lambda kv: kv[1][0]):
                for ch in (_chunks(ids, workers) if split else [ids]):
                    sol = dict(template)
                    sol['enthalpy_bracket'] = list(br)
                    runs.append(('GENERATE', {'radial_indices': ch, 'solver': sol, 'selection': '%s c2v001 rule' % tag}))
        else:
            for ch in (_chunks(list(range(n)), workers) if split else [list(range(n))]):
                runs.append(('GENERATE', {'radial_indices': ch, 'solver': dict(template),
                                          'column_enthalpy_brackets': {str(i): bracket_table[str(i)] for i in ch},
                                          'selection': '%s c2v001 rule' % tag}))
        return runs

    rule = brackets.get('rule')
    pinned = brackets.get('pinned_controls')
    checks = {}
    if rule:
        undecided = [k for k in ('rfs_factors', 'le_first_factors', 'le_next_factors') if _has_pending(rule[k])]
        if undecided:
            refuse('brackets.rule_factors', 'UNDECIDED_NGC_FIELD', 'brackets.rule_factors is NONE_IN_REVIEWED_CODE for %s (no ROOT_DECISIONS '
                   'row) and the call spec supplies none: %s' % (gname, undecided))

    # ---------------- FS pass, original K (columns v001 / rotation v001 / feedback v002, all gal_c2v003)
    if pinned:
        fs_plan = [(x['path'], verify_pin(x['path'], x['sha256'], 'pinned fs controls')) for x in pinned['fs']]
        merged = {}
        for x in pinned['fs']:
            c = json.loads(Path(x['path']).read_text())
            for i in c['radial_indices']:
                merged[str(i)] = c['solver']['enthalpy_bracket']
            if any(c['solver'][k] != template[k] for k in template if k != 'enthalpy_bracket'):
                checks.setdefault('fs_solver_block_differs', []).append(x['path'])
        ro = g.get('repro_rule_overrides', {}).get('fs_absolute_overrides', {})
        expect = {str(i): list(ro.get(str(i), template['enthalpy_bracket'])) for i in range(n)}
        checks['fs'] = {'checked': True, 'n': len(merged), 'bitwise_equal': merged == expect,
                        'rule': 'nominal template bracket + repro_rule_overrides.fs_absolute_overrides (last successful run wins)'}
    else:
        table = {str(i): list(rule['fs_absolute_overrides'].get(str(i), template['enthalpy_bracket'])) for i in range(n)}
        fs_plan = generated_runs('fs', table, v001=True)
        checks['fs'] = rule_vs_saved(g, 'fs', table)
    fs_dirs = column_pass('fs', 'columns_v001', [] + uvt_argv('columns_v001'), fs_plan)
    mpath, msha = manifest('fs', fs_dirs)
    d = ctx.stage_dir('fs_rotation')
    fs_rot = d / 'rotation' if ctx.mode == 'run' else ctx.saved_or('fs_rotation', d / 'rotation')
    fs_col_producer = producer_pin('columns_v001', producer(fs_dirs, 'columns_v001', 'config producer_pins.column_worker', 'fs_rotation'), uvt_extra)
    ctx.run_stages([gen_request('fs_rotation', 'rotation_v001', base + ['--column-manifest', mpath, '--column-manifest-sha256', msha,
                    '--mass-relative-tolerance', FA['mass_relative_tolerance'], '--outdir', fs_rot] + uvt_argv('rotation_v001'),
                    module_patches=[reuse_patch], mask=mask, producers={'column_worker': fs_col_producer})], [d])
    d = ctx.stage_dir('fs_feedback')
    fs_fb = d / 'feedback' if ctx.mode == 'run' else ctx.saved_or('fs_feedback', d / 'feedback')
    fs_rot_producer = producer_pin('rotation_v001', producer([fs_rot], 'rotation_v001', 'config producer_pins.rotation_worker', 'fs_feedback'), uvt_extra)
    ctx.run_stages([gen_request('fs_feedback', 'feedback_v002', base + ['--rotation-directory', fs_rot,
                    '--rotation-finish-sha256', ctx.finish_sha(fs_rot), '--wave-batch', FA['wave_batch'],
                    '--position-batch', FA['position_batch'], '--bessel-cache-entries', FA['bessel_cache_entries'],
                    '--outdir', fs_fb], module_patches=[reuse_patch], mask=mask, producers={'rotation_worker': fs_rot_producer})], [d])
    fs_fb_sha = ctx.finish_sha(fs_fb)
    percall['custody.fs_feedback_worker_sha256'] = producer([fs_fb], 'feedback_v002', 'config custody.fs_feedback_worker_sha256', 'rfs_columns')

    # ---------------- RFS columns, original K, refreshed field (columns v003 gal_c2v003): source of LE1 brackets
    H_fs = column_H(fs_dirs)
    rfs_args = ['--feedback-directory', fs_fb, '--feedback-finish-sha256', fs_fb_sha]
    if pinned:
        rfs_plan = [(x['path'], verify_pin(x['path'], x['sha256'], 'pinned rfs controls')) for x in pinned['rfs']]
        checks['rfs'] = bracket_check([x['path'] for x in pinned['rfs']], H_fs, LE_RULE_DEFAULTS['rfs_factors'],
                                      g.get('repro_rule_overrides', {}).get('rfs_factor_overrides', {}))
    else:
        if H_fs is None:
            rfs_plan = 'PENDING'
        else:
            require_bracket_source(H_fs, n, 'fs')
            table = rule_brackets(H_fs, rule['rfs_factors'], rule['rfs_factor_overrides'], range(n))
            checks['rfs'] = rule_vs_saved(g, 'rfs', table)
            rfs_plan = generated_runs('rfs', table)
    if rfs_plan == 'PENDING':
        rfs_dirs = ['PENDING(rfs columns)']
        ctx.records.append({'name': 'rfs_columns', 'executed': False, 'note': 'controls depend on fs column enthalpies (rule mode)'})
    else:
        rfs_dirs = column_pass('rfs', 'columns_v003', rfs_args + uvt_argv('columns_v003', fs_rot), rfs_plan)

    # ---------------- LE Picard passes (v005 / v005 / v004 + column mean v004, all gal_c2v003)
    field_dir, field_sha = fs_fb, fs_fb_sha
    field_rot = fs_rot  # C2V010 (u): the rotation the current field's feedback transformed
    field_worker = producer([fs_fb], 'feedback_v002', '--feedback-worker-sha256', 'le1 field')  # c2v004 (run: c2v003 value)
    prev_dirs = rfs_dirs
    prev_speeds = None
    final = None
    for p in range(1, P + 1):
        tag = 'le%d' % p
        last = (p == P)
        serial = last or bound is not None
        H_prev = column_H(prev_dirs) if all(isinstance(x, Path) for x in prev_dirs) else None
        factors = rule['le_first_factors'] if (rule and p == 1) else (rule['le_next_factors'] if rule else None)
        if pinned:
            plan = [(x['path'], verify_pin(x['path'], x['sha256'], 'pinned le controls')) for x in pinned['le'][p - 1]]
            checks[tag] = bracket_check([x['path'] for x in pinned['le'][p - 1]], H_prev,
                                        LE_RULE_DEFAULTS['le_first_factors'] if p == 1 else LE_RULE_DEFAULTS['le_next_factors'], {})
        elif H_prev is None:
            plan = 'PENDING'
        else:
            ov = rule['le_factor_overrides'].get(str(p), {})
            require_bracket_source(H_prev, n, 'rfs' if p == 1 else 'le%d' % (p - 1))
            table = rule_brackets(H_prev, factors, ov, range(n))
            checks[tag] = rule_vs_saved(g, tag, table)
            plan = generated_runs(tag, table, split=not serial)
        if plan == 'PENDING':
            ctx.records.append({'name': tag + '_columns', 'executed': False, 'note': 'controls depend on previous column enthalpies'})
            break
        cols = column_pass(tag, 'columns_v005', ['--feedback-directory', field_dir, '--feedback-finish-sha256', field_sha,
                           '--feedback-worker-sha256', field_worker, '--entropy-scale', efs] + uvt_argv('columns_v005', field_rot), plan)
        mpath, msha = manifest(tag, cols)
        d = ctx.stage_dir(tag + '_rotation')
        rot = d / 'rotation' if ctx.mode == 'run' else ctx.saved_or(tag + '_rotation', d / 'rotation')
        ctx.run_stages([gen_request(tag + '_rotation', 'rotation_v005', base + ['--column-manifest', mpath, '--column-manifest-sha256', msha,
                        '--feedback-directory', field_dir, '--feedback-finish-sha256', field_sha,
                        '--column-worker-sha256', producer(cols, 'columns_v005', '--column-worker-sha256', tag + '_rotation'),
                        '--feedback-worker-sha256', field_worker,
                        '--mass-relative-tolerance', FA['mass_relative_tolerance'], '--outdir', rot, '--entropy-scale', efs] + uvt_argv('rotation_v005', field_rot),
                        module_patches=[reuse_patch], mask=mask)], [d])
        pass_rec = {'pass': p, 'columns': [str(x) for x in cols], 'rotation': str(rot), 'field': str(field_dir)}
        rf = Path(rot) / 'finish.json'
        if rf.is_file():
            rfj = json.loads(rf.read_text())
            pass_rec.update(rotation_positive=rfj['positive_rotation_square'], minimum_rotation_square=rfj['minimum_rotation_square'],
                            nonpositive_indices=rfj['nonpositive_indices'], rotation_arrays={'path': rfj['arrays_path'], 'sha256': rfj['arrays_sha256']})
            if ctx.mode == 'run':
                pass_rec['rotation_array_content_digests'] = array_digests(rfj['arrays_path'])
        failures = []
        for x in cols:
            fx = Path(x) / 'finish.json'
            if fx.is_file():
                failures += json.loads(fx.read_text())['failures']
        pass_rec['column_failures'] = failures
        observe = len(cols) == 1 and (last or bound is not None or sp['numerics']['picard']['observe_every_pass'])
        speeds = None
        if observe:
            d = ctx.stage_dir(tag + '_column_mean')
            obsd = d / 'observation' if ctx.mode == 'run' else ctx.saved_or(tag + '_column_mean', d / 'observation')
            b, b_ok, b_st = gc_value(gc, 'observation.binding')  # c2v005: DDO154 == g['column_mean_binding'] (checked)
            if 'observation.binding' in gfields:  # C2V008 (a), c2v003b: the per-call column-mean binding
                b, b_ok = gfields['observation.binding'], True
            bpin = [str(b['path']), b['sha256']] if b_ok else ['NONE_IN_REVIEWED_CODE(observation.binding)', 'NONE_IN_REVIEWED_CODE']
            pins = [bpin, [str(Path(rot) / 'start.json'), ctx.finish_sha(rot, 'start.json')],
                    [str(Path(rot) / 'finish.json'), ctx.finish_sha(rot)],
                    [str(Path(cols[0]) / 'start.json'), ctx.finish_sha(cols[0], 'start.json')],
                    [str(Path(cols[0]) / 'finish.json'), ctx.finish_sha(cols[0])]]
            percall['custody.column_mean_input_pins'] = pins  # c2v004: was stage global PINS
            rot_worker = rotation_producer_pin(producer([rot], 'rotation_v005', 'config producer_pins.rotation_worker',
                                                        tag + '_column_mean'), uvt_extra)
            ctx.run_stages([gen_request(tag + '_column_mean', 'column_mean_v004', ['--outdir', obsd], tag=tag,
                                        producers={'rotation_worker': rot_worker})], [d])
            rp = Path(obsd) / 'result.json'
            if rp.is_file():
                res = json.loads(rp.read_text())
                pass_rec['column_mean'] = {'path': str(rp), 'sha256': sha256_file(rp), 'status': res['status']}
                if res['status'] == 'CONDITIONAL_PREPARATION_ROWS_NOT_CALIBRATION':
                    speeds = [r['speed_km_s'] for r in res['prediction']['rows']]  # c2v006: None on an N1 invalid row
                    pass_rec['rows'] = res['prediction']['rows']
                    if res['prediction'].get('invalid_rows') is not None:  # c2v006 (A4): only with the binding invalid_row_rule
                        pass_rec['invalid_rows'] = res['prediction']['invalid_rows']
                    pass_rec['nonaxisymmetric_residual_maxima'] = res['nonaxisymmetric_residual_maxima']
                    pass_rec['residual_units'] = res.get('residual_units')
                else:
                    pass_rec['column_mean_failure'] = res.get('failure')
        else:
            pass_rec['column_mean'] = 'NOT_OBSERVED (multi-run parallel pass or observe_every_pass false)'
        if speeds is not None and prev_speeds is not None:
            # c2v006: N1 invalid rows (speed None) are skipped; with no invalid row this is the c2v005 expression
            pass_rec['max_abs_change_km_s'] = max(abs(a - b) for a, b in zip(speeds, prev_speeds) if a is not None and b is not None)
        ctx.passes.append(pass_rec)
        ctx.event(event='pass_done', **{k: v for k, v in pass_rec.items() if k in ('pass', 'max_abs_change_km_s', 'rotation_positive')})
        stop = last or (bound is not None and pass_rec.get('max_abs_change_km_s') is not None and pass_rec['max_abs_change_km_s'] <= bound)
        if stop:
            final = pass_rec
            break
        prev_speeds = speeds
        d = ctx.stage_dir(tag + '_feedback')
        fb = d / 'feedback' if ctx.mode == 'run' else ctx.saved_or(tag + '_feedback', d / 'feedback')
        ctx.run_stages([gen_request(tag + '_feedback', 'feedback_v004', base + ['--rotation-directory', rot,
                        '--rotation-finish-sha256', ctx.finish_sha(rot), '--wave-batch', FA['wave_batch'],
                        '--position-batch', FA['position_batch'], '--bessel-cache-entries', FA['bessel_cache_entries'],
                        '--outdir', fb, '--current-feedback-directory', field_dir, '--current-feedback-finish-sha256', field_sha,
                        '--rotation-worker-sha256', producer([rot], 'rotation_v005', '--rotation-worker-sha256', tag + '_feedback'),
                        '--current-feedback-worker-sha256', field_worker],
                        module_patches=[reuse_patch], mask=mask)], [d])
        field_dir, field_sha = fb, ctx.finish_sha(fb)
        field_rot = rot  # C2V010 (u)
        field_worker = producer([fb], 'feedback_v004', '--feedback-worker-sha256', 'le%d field' % (p + 1))
        prev_dirs = cols
    info['bracket_rule_checks'] = checks
    info['producer_identity'] = producer_log
    info['galaxy_config']['stage_configs'] = [m for _, _, m in gc_written.values()]
    info['refusals'] = refusals
    info['percall_known'] = {k: v for k, v in percall.items()}
    if uvx is not None:  # C2V010 (u): tail-ON record (absent for tail OFF)
        info['uv_tail'] = uvx
    return info, final


def reference_comparison(records, saved):
    """DIAGNOSTIC ONLY (never alters the flow): compare this call's stage outputs with the saved
    chain's outputs by array content.  NPZ file bytes are not deterministic (zip timestamps), so
    arrays are compared, not file hashes."""
    rows = []
    for rec in records:
        if not rec.get('executed') or rec.get('exit_code') != 0:
            continue
        name = rec['name']
        am = _argv_map(rec['argv'])
        new = Path(am.get('--outdir', ''))
        try:
            if name == 'route_a' and 'route_a' in saved:
                a = json.loads((Path(am['--checkpoint-directory']) / 'iteration_0004/START.json').read_text())
                b = json.loads((Path(saved['route_a']['checkpoint']) / 'iteration_0004/START.json').read_text())
                res = {k: ('BITWISE_EQUAL' if a[k]['array_sha256'] == b[k]['array_sha256'] else 'DIFFERS')
                       for k in ('prepared_wavevectors', 'prepared_weighted_responses', 'gas_fourier_J', 'fixed_source_fourier_J')}
            elif name == 'body' and 'body' in saved:
                res = compare_npz(new / 'body_arrays.npz', Path(saved['body']) / 'body_arrays.npz')
            elif name == 'offset' and 'offset' in saved:
                res = {f: compare_npz(new / f, Path(saved['offset']) / f) for f in
                       ('unit_response.npz', 'source_offset.npz', 'offset_prepared.npz', 'updated_base_arrays.npz')}
            elif name.endswith('_rotation') and name in saved:
                res = compare_npz(new / 'rotation_base_arrays.npz', Path(saved[name]) / 'rotation_base_arrays.npz')
            elif name.endswith('_feedback') and name in saved:
                res = {f: compare_npz(new / f, Path(saved[name]) / f) for f in ('gas_source_feedback.npz', 'refreshed_prepared.npz')}
            elif '_columns_' in name:
                tag = name.split('_columns_')[0]
                old_paths = {}
                for od in saved.get(tag + '_columns') or []:
                    for y in json.loads((Path(od) / 'finish.json').read_text())['completed']:
                        old_paths[y['index']] = y['path']
                if not old_paths:
                    continue
                fa = json.loads((new / 'finish.json').read_text())
                keys = ('Hc_m2_s2', 'z_m', 'weights_m', 'rho_kg_m3', 'enthalpy_m2_s2', 'roots_m', 'K_SI')
                res = {'failures_new': [x['index'] for x in fa['failures']]}
                for x in fa['completed']:
                    if x['index'] not in old_paths:
                        res[str(x['index'])] = 'NO_SAVED_COUNTERPART'
                        continue
                    ca, cb = json.loads(Path(x['path']).read_text()), json.loads(Path(old_paths[x['index']]).read_text())
                    res[str(x['index'])] = 'BITWISE_EQUAL' if all(ca[k] == cb[k] for k in keys) else 'DIFFERS'
            elif name.endswith('_column_mean') and name in saved:
                a = json.loads((new / 'result.json').read_text())['prediction']['rows']
                b = json.loads((Path(saved[name]) / 'result.json').read_text())['prediction']['rows']
                res = {'bitwise_equal': a == b, 'max_relative_difference': max(abs(x['speed_km_s'] - y['speed_km_s']) / abs(y['speed_km_s'])
                                                                              for x, y in zip(a, b))}
            else:
                continue
        except Exception as exc:
            res = 'COMPARISON_ERROR %s: %s' % (type(exc).__name__, exc)
        rows.append({'stage': name, 'result': res})
    return rows


def deciding_test_verdict(rows, passes):
    """c2v004 DIAGNOSTIC ONLY (never alters the flow): the run-mode equivalence pass condition of the DRAFT plan
    (BINDING_NOTES_AND_V004_PLAN_C2V004 s7 item 2): the offset arrays, every rotation and feedback array set that has
    a saved counterpart, and the final column-mean rows are BITWISE_EQUAL to the saved chain.  Column comparisons are
    reported, not required.  PASS needs the offset row and the final pass's column-mean row to be present."""
    def flat(v):
        if isinstance(v, dict):
            if not v:
                return ['EMPTY_COMPARISON']  # c2v005 (v004_fix CHECK N2): an empty per-file result fails
            return [x for y in v.values() for x in flat(y)]
        return [v]
    required, failing, columns = [], [], {'bitwise_equal': 0, 'other': []}
    final = ('le%d_column_mean' % passes[-1]['pass']) if passes else None
    for r in rows:
        name, res = r['stage'], r['result']
        if '_columns_' in name:
            for k, v in (res.items() if isinstance(res, dict) else []):
                if k == 'failures_new':
                    continue
                if v == 'BITWISE_EQUAL':
                    columns['bitwise_equal'] += 1
                else:
                    columns['other'].append('%s[%s]=%s' % (name, k, v))
            continue
        if name in ('offset', 'body') or name.endswith('_rotation') or name.endswith('_feedback'):  # c2v005: body when recomputed
            required.append(name)
            vals = flat(res) if isinstance(res, dict) else [res]
            if not vals or any(v != 'BITWISE_EQUAL' for v in vals):
                failing.append(name)
        elif name.endswith('_column_mean'):
            required.append(name)
            if not (isinstance(res, dict) and res.get('bitwise_equal') is True):
                failing.append(name)
    missing = [n for n in ('offset', final) if n is None or n not in required]
    return {'verdict': 'PASS_BITWISE_EQUAL' if not failing and not missing else 'FAIL',
            'compared': required, 'failing': failing, 'missing_required': missing, 'columns': columns,
            'condition': 'offset (and body when recomputed), rotation and feedback arrays and the final column-mean rows BITWISE_EQUAL to the saved chain',
            'status': 'DIAGNOSTIC_ONLY'}


# ----------------------------------------------------------------------------- run command
def all_static_pins(nspec):
    pins = {}
    for path, sha in list(SCRIPTS.values()) + list(AUX.values()):
        pins[str(path)] = verify_pin(path, sha, 'code')
    pins[str(PREP_V008_REVIEW[0])] = verify_pin(PREP_V008_REVIEW[0], PREP_V008_REVIEW[1], 'prep V008 review')  # c2v003
    if route_a_column_workers(nspec) > 1:  # C2V007 (b): the parallel route-A worker and solver, only when used
        for key, (path, sha) in PARALLEL_ROUTE_A.items():
            pins[str(path)] = verify_pin(path, sha, 'parallel route-A ' + key)
    g = GALAXIES[nspec['galaxy']]
    for key in ('base_seed', 'profile', 'monotone_source', 'column_mean_binding', 'solver_template', 'monotone_source_pin'):
        if g.get(key) is None:  # c2v006: NGC3198 has no base seed; its slot pin (D3) and A4 binding are pinned here
            continue
        path, sha = g[key]
        pins[str(path)] = verify_pin(path, sha, key)
    for key, ms in MODULE_SUCCESSORS.items():  # c2v005: module successors and the reviewed modules they replace
        for role in ('successor', 'base'):
            pins[str(ms[role][0])] = verify_pin(ms[role][0], ms[role][1], '%s %s' % (key, role))
    pins[nspec['coefficients']['path']] = verify_pin(nspec['coefficients']['path'], nspec['coefficients']['sha256'], 'coefficients')
    # c2v004: the reviewed base of each generalized successor, the galaxy-config file and the shared schema
    for key, gen in GENERALIZED.items():
        pins[str(gen['base'][0])] = verify_pin(gen['base'][0], gen['base'][1], 'generalized base ' + key)
    gpath, gsha = GALAXY_CONFIG_FILES[nspec['galaxy'] if nspec.get('member') is None else (nspec['galaxy'], nspec['member'])]
    pins[str(gpath)] = verify_pin(gpath, gsha, 'galaxy config')
    pins[str(GC_SCHEMA[0])] = verify_pin(GC_SCHEMA[0], GC_SCHEMA[1], 'galaxy-config schema')
    if nspec['galaxy'] == 'DDO154' and geometry_active(nspec):  # C2V008 (a), c2v003b: inputs of the per-call geometry derivation
        for key, (path, sha) in GEOMETRY_PINS.items():
            pins[str(path)] = verify_pin(path, sha, 'geometry ' + key)
    if 'uv_tail' in (nspec.get('numerics') or {}):  # C2V010 (u): tail-ON code and data pins, only when declared
        pins.update(uvt_static_pins(uvt_is_nodes(nspec['numerics']['uv_tail'])))
    elif route_a_ro1_workers(nspec):  # C2V010 r4 (R5): tail OFF on the RO1 workers
        pins.update(ro1_off_pins())
    return pins


def transitive_pins_and_scipy(roots=None):
    """Load each stage script from verified bytes (inert) and verify every (path, sha) it pins;
    scan every pinned .py for a top-level scipy import.  c2v002: `roots` (default = the DDO
    SCRIPTS+AUX, i.e. exactly c2v001) lets the NGC configuration scan its own files."""
    import re
    seen, problems, scipy_hits = {}, [], []
    if roots is None:
        roots = list(SCRIPTS.values()) + list(AUX.values())
    queue = [(str(p), s) for p, s in roots]
    pat = re.compile(r'^\s*(import\s+scipy|from\s+scipy)', re.M)

    def collect(obj, acc):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, str) and _is_hex64(v) and isinstance(k, (str, Path)):
                    acc.append((str(k), v))
                else:
                    collect(v, acc)
        elif isinstance(obj, (list, tuple)):
            if len(obj) == 2 and isinstance(obj[1], str) and _is_hex64(obj[1]) and isinstance(obj[0], (str, Path)):
                acc.append((str(obj[0]), obj[1]))
            else:
                for v in obj:
                    collect(v, acc)
    while queue:
        path, sha = queue.pop()
        if path in seen:
            if seen[path] != sha:
                problems.append('conflicting pins for %s' % path)
            continue
        seen[path] = sha
        p = Path(path)
        if not p.is_file():
            problems.append('missing %s' % path)
            continue
        if sha256_file(p) != sha:
            problems.append('pin mismatch %s' % path)
            continue
        if p.suffix == '.py':
            text = p.read_text()
            if pat.search(text):
                scipy_hits.append(path)
            try:
                m = exec_verified(p, sha, 'c2v001_scan_' + p.stem)
            except Exception as exc:  # inert modules only define names
                problems.append('could not load %s: %s' % (path, exc))
                continue
            acc = []
            for name in dir(m):
                if name.isupper():
                    collect(getattr(m, name), acc)
            for path2, sha2 in acc:
                if Path(path2).suffix in ('.py', '.json', '.npz'):
                    queue.append((path2, sha2))
    return {'verified_files': len(seen), 'files': seen, 'problems': problems, 'scipy_imports': scipy_hits}


def cmd_run(spec_path, outdir):
    # C2V007 (a) F2 (c2v003c hunk @@ -1653): absolute outdir (stage children run with cwd=<stage dir>).  os.path.abspath
    # is lexical: it normalizes '.', '..', '//' and a trailing '/', and resolves no symlink.  A relative monitor/campaign
    # outdir resolves against the driver's inherited cwd, which is the monitor's.
    out = Path(os.path.abspath(outdir))
    if out.exists():
        print('REFUSED: outdir exists', file=sys.stderr)
        return 2
    out.mkdir(parents=True)
    t0 = time.monotonic()
    raw = Path(spec_path).read_bytes()
    spec_sha = sha256_bytes(raw)
    (out / 'inputs').mkdir()
    with open(out / 'inputs' / 'call_spec.json', 'xb') as f:
        f.write(raw)
    result = {'schema': RESULT_SCHEMA, 'call_spec_sha256': spec_sha, 'driver_sha256': sha256_file(__file__),
              'accepted_for_calibration': False, 'scored': False, 'valid': False, 'reasons': []}
    status = 'FAILED'
    ctx = None
    try:
        nspec = normalize_spec(json.loads(raw))
        if nspec.get('config') == 'NGC3198_C2V002':
            ngc_run_blocked(out, nspec, spec_sha, result)  # writes start/inputs, executes 0 stages, raises Blocked
        pins = all_static_pins(nspec)
        g = GALAXIES[nspec['galaxy']]
        _write_x(out / 'start.json', {'schema': RESULT_SCHEMA, 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                 'pid': os.getpid(), 'driver': str(Path(__file__).resolve()), 'driver_sha256': result['driver_sha256'],
                 'call_spec_sha256': spec_sha, 'normalized_spec': nspec, 'static_pins': pins,
                 'scope': 'Route-B m0 forward call; no observed velocity read, no score, no calibration admission.'})
        # c2v004/c2v005: fail closed before any stage on a binding blocker found from bytes (see binding_blockers);
        # NGC3198: execute_chain raises Blocked at the first remaining refusal, before any stage it would feed.
        _nodes = uvt_is_nodes(nspec['numerics'].get('uv_tail'))  # C2V010 r4
        bb = (binding_blockers() + (ro1_off_blockers() if route_a_ro1_workers(nspec) else [])) if 'uv_tail' not in nspec['numerics'] else (
            binding_blockers(dict(SCRIPTS, **uvt_active(_nodes)['scripts'])) + uvt_binding_blockers(_nodes))  # C2V010 (u): tail ON, active tables
        if bb:
            result['binding_blockers'] = bb
            raise Blocked(' | '.join(bb))
        sr = route_b_static_refusals(nspec, load_galaxy_config(nspec['galaxy'], nspec.get('member')))  # c2v005: empty for DDO154
        if sr:
            result['remaining_refusals'] = sr
            raise Blocked('REMAINING_REFUSALS: ' + ' | '.join('%s [%s] %s' % (r['where'], r['class'], r['refusal']) for r in sr))
        ctx = Ctx('run', nspec, out)
        ctx.log = open(out / 'progress.jsonl', 'x')
        info, final = execute_chain(ctx)
        result.update(galaxy=nspec['galaxy'], normalized_spec=nspec, identity=info, passes=ctx.passes)
        if final is None:
            result['reasons'].append('no final pass')
        else:
            result['final_pass'] = final['pass']
            # c2v003 (CHECK_V001 further defect 2): explicit convergence-bound outcome.
            bnd = nspec['numerics']['picard']['speed_change_bound_km_s']
            chg = final.get('max_abs_change_km_s')
            result['picard_bound_met'] = None if bnd is None or chg is None else bool(chg <= bnd)
            rows_ok, invalid_rows = final_rows_check(final, g['n_queries'])  # c2v006 (A4/N1)
            if rows_ok:
                result['rows'] = final['rows']
                result['speeds_km_s'] = {r['id']: r['speed_km_s'] for r in final['rows']}
                if invalid_rows is not None:
                    result['invalid_rows'] = invalid_rows
                    result['headline_rule'] = ('N1/A4: rows valid=false (QUERY_INSIDE_INNERMOST_NODE) count as misses; invalid entries '
                                               'never pass; they do not invalidate the call')
                if nspec.get('member') is not None or nspec['physical'].get('entropy_K_member', 'N4_PRIMARY_64_OVER_121') != 'N4_PRIMARY_64_OVER_121':
                    result['alternative_label'] = {'member': nspec.get('member'), 'entropy_K_member': nspec['physical'].get('entropy_K_member'),
                                                   'status': 'DECLARED_ALTERNATIVE_NOT_HEADLINE'}
                result['valid'] = (not final['column_failures']) and final.get('rotation_positive') is True
                if not result['valid']:
                    result['reasons'].append('final pass column failures or nonpositive rotation')
            else:
                result['reasons'].append('final column mean did not return %d rows: %s' % (g['n_queries'], final.get('column_mean')))
            diag = {'nonaxisymmetric_residual_maxima': final.get('nonaxisymmetric_residual_maxima'),
                    'residual_units': final.get('residual_units'),
                    'stored_residual_arrays': {'rotation_arrays': final.get('rotation_arrays'),
                                               'keys': ['angular_radial_residual', 'angular_vertical_residual', 'angular_azimuthal_residual',
                                                        'Phi_R_full', 'Phi_z_full', 'base_residual_r0']},
                    'per_pass_maxima': [{'pass': x['pass'], 'maxima': x.get('nonaxisymmetric_residual_maxima')} for x in ctx.passes]}
            if final.get('rotation_arrays'):
                try:
                    diag['azimuthal_harmonics'] = harmonic_diagnostic(final['rotation_arrays']['path'])
                except Exception as exc:
                    diag['azimuthal_harmonics'] = 'unavailable: %s' % exc
            result['residual_diagnostics'] = diag
        status = 'COMPLETED' if result['valid'] else 'COMPLETED_INVALID'
    except Refusal as exc:
        status = 'REFUSED'
        result['reasons'].append(str(exc))
    except Blocked as exc:
        status = 'BLOCKED'
        result['reasons'].append(str(exc))
    except RouteANoFixedPoint as exc:  # C2V007 (a) F1 (c2v003c hunk @@ -1715): a model outcome, not BLOCKED
        status = 'ROUTE_A_NO_FIXED_POINT'
        result['reasons'].append(str(exc))
    except StageFailed as exc:
        status = 'FAILED_AT_STAGE'
        result['reasons'].append(str(exc))
    except Exception as exc:
        import traceback
        status = 'FAILED'
        result['reasons'].append('%s: %s' % (type(exc).__name__, exc))
        result['traceback'] = traceback.format_exc()
    if ctx is not None:
        if ctx.route_a_outcome is not None:  # C2V007 (a) F1 (c2v003c hunk @@ -1724): outcome + converged iteration, every status
            result['route_a_outcome'] = ctx.route_a_outcome
        if ctx.geometry is not None:  # C2V008 (a): per-call geometry record and the stage-admission probe, every status
            result['geometry'] = ctx.geometry
        result['stage_records'] = ctx.records
        if ctx.uv_tail is not None:  # C2V010 (u): tail record + each tail stage's finish.json tail record, every status
            result['uv_tail'] = dict(ctx.uv_tail, stage_records=uvt_stage_records(ctx.records))
        if ctx.spec.get('reference_compare'):
            result['reference_comparison'] = reference_comparison(ctx.records, GALAXIES[ctx.spec['galaxy']].get('saved_runs', {}))
            result['deciding_test'] = deciding_test_verdict(result['reference_comparison'], ctx.passes)  # c2v004
        if result.get('passes') is None:
            result['passes'] = ctx.passes
        if ctx.log is not None:
            ctx.log.close()
    result['status'] = status
    result['elapsed_seconds'] = time.monotonic() - t0
    rsha = _write_x(out / 'result.json', result)
    _write_x(out / 'finish.json', {'status': status, 'valid': result['valid'], 'result_path': str(out / 'result.json'),
             'result_sha256': rsha, 'elapsed_seconds': result['elapsed_seconds'], 'reasons': result['reasons'],
             'retries': 0, 'partial_outputs_preserved': True})
    return 0 if status in ('COMPLETED', 'COMPLETED_INVALID') else 3


# ----------------------------------------------------------------------------- dry-run command
def _argv_map(argv):
    out, i = {}, 0
    while i < len(argv):
        k = argv[i]
        if i + 1 < len(argv) and not str(argv[i + 1]).startswith('--'):
            out[k] = str(argv[i + 1])
            i += 2
        else:
            out[k] = None
            i += 1
    return out


UPSTREAM_FLAGS = ('--checkpoint-directory', '--body-directory', '--body-finish-sha256', '--offset-directory',
                  '--rotation-directory', '--rotation-finish-sha256', '--feedback-directory', '--feedback-finish-sha256',
                  '--current-feedback-directory', '--current-feedback-finish-sha256', '--column-manifest', '--column-manifest-sha256')


def _compare_argv(kind, planned, original):
    """Per-flag comparison of the planned argv (upstream outputs resolved to the SAVED chain's
    outputs) with the saved launch argv: identical literal / identical file bytes / identical
    manifest content / output location / different.  'role' says whether the value is an
    upstream output (in a real call it is this call's own output with the same role)."""
    # c2v004: the appended galaxy-config tokens are compared separately (GALAXY_CONFIG_ADDED).
    planned_wo, gc_tokens = split_galaxy_config_argv(planned[1:])
    pm, om = _argv_map(planned_wo), _argv_map(original[4:])
    rows = []
    outputs = ('--outdir', '--checkpoint-directory') if kind == 'route_a' else ('--outdir',)
    for k in sorted(set(pm) | set(om)):
        a, b = pm.get(k, '<absent>'), om.get(k, '<absent>')
        role = 'output' if k in outputs else ('upstream-output' if k in UPSTREAM_FLAGS else
                                              ('upstream-producer-identity' if k in PRODUCER_FLAGS else 'static'))
        ms = MODULE_SUCCESSORS['reference_module']
        if k in outputs:
            verdict = 'OUTPUT_LOCATION (fresh per call in a real run)'
        elif kind == 'reference' and (k, a, b) in (('--reference-module', str(ms['successor'][0]), str(ms['base'][0])),
                                                    ('--reference-sha256', ms['successor'][1], ms['base'][1])):
            role = 'module-identity'
            verdict = 'MODULE_SUCCESSOR (c2v005: stages2 n_phi successor of the module the saved launch used)'
        elif a == b:
            verdict = 'IDENTICAL_VALUE'
            if a and Path(a).is_file():
                verdict = 'IDENTICAL_VALUE_FILE_SHA256=' + sha256_file(a)
        elif k == '--column-manifest' and Path(a).is_file() and Path(b).is_file() and \
                json.loads(Path(a).read_text())['runs'] == json.loads(Path(b).read_text())['runs']:
            verdict = 'IDENTICAL_MANIFEST_RUNS (generated file; bytes differ)'
        elif k == '--column-manifest-sha256' and Path(pm['--column-manifest']).is_file() and \
                sha256_file(pm['--column-manifest']) == a and sha256_file(om['--column-manifest']) == b:
            verdict = 'IDENTICAL_ROLE (sha256 of the respective manifest file)'
        elif a and b and Path(a).is_file() and Path(b).is_file() and sha256_file(a) == sha256_file(b):
            verdict = 'IDENTICAL_FILE_BYTES'
        else:
            verdict = 'DIFFERENT'
        rows.append({'flag': k, 'role': role, 'planned': a, 'original': b, 'verdict': verdict})
    if gc_tokens:
        rows.append({'flag': ' '.join(t for t in gc_tokens if t.startswith('--')), 'role': 'galaxy-config',
                     'planned': gc_tokens, 'original': '<absent>', 'verdict': 'GALAXY_CONFIG_ADDED'})
    return rows


def _orig_launch(stage_outdir):
    lp = Path(stage_outdir).parent / 'launch.json'
    if lp.is_file():
        return json.loads(lp.read_text())['command']
    return None


def _npz_headers(path):
    import zipfile
    import numpy as np
    heads = {}
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            with z.open(name) as f:
                ver = np.lib.format.read_magic(f)
                shape, fortran, dtype = (np.lib.format.read_array_header_1_0(f) if ver == (1, 0)
                                         else np.lib.format.read_array_header_2_0(f))
                heads[name[:-4] if name.endswith('.npy') else name] = {'shape': list(shape), 'dtype': dtype.str}
    return heads


def cmd_dry_run(spec_path, report_dir):
    rd = Path(os.path.abspath(report_dir))  # C2V007 (a) F2 (c2v003c hunk @@ -1812): planned paths absolute, as in a run
    if rd.exists():
        print('REFUSED: report dir exists', file=sys.stderr)
        return 2
    rd.mkdir(parents=True)
    raw = Path(spec_path).read_bytes()
    nspec = normalize_spec(json.loads(raw))
    if nspec.get('config') == 'NGC3198_C2V002':
        return ngc_dry_run(spec_path, raw, nspec, rd)
    g = GALAXIES[nspec['galaxy']]
    report = {'schema': 'UNT_GALAXY_M0_FORWARD_DRYRUN_C2V001', 'call_spec': str(spec_path), 'call_spec_sha256': sha256_bytes(raw),
              'driver_sha256': sha256_file(__file__), 'normalized_spec': nspec, 'executed_stages': 0}
    report['static_pins'] = all_static_pins(nspec)
    # C2V007 (b): with a parallel route A the scan also covers the parallel worker (its LOCAL pins) and solver.
    report['transitive_pins'] = (transitive_pins_and_scipy() if route_a_column_workers(nspec) == 1 else
                                 transitive_pins_and_scipy(list(SCRIPTS.values()) + list(AUX.values()) + list(PARALLEL_ROUTE_A.values())))
    if 'uv_tail' in nspec['numerics']:  # C2V010 (u): tail ON scans the active scripts and every tail-ON code pin
        _nodes = uvt_is_nodes(nspec['numerics']['uv_tail'])  # C2V010 r4
        report['transitive_pins'] = transitive_pins_and_scipy(uvt_scan_roots(dict(SCRIPTS, **uvt_active(_nodes)['scripts']), _nodes) + list(PARALLEL_ROUTE_A.values()))
    elif route_a_ro1_workers(nspec):  # C2V010 r4 (R5): tail OFF on the RO1 workers
        report['transitive_pins'] = transitive_pins_and_scipy(list(SCRIPTS.values()) + list(AUX.values()) + list(PARALLEL_ROUTE_A.values())
                                                              + [RO1_ROUTE_A[k] for k in ('worker', 'worker_parallel', 'binding')]
                                                              + [AUX_UVT['facade'], AUX_UVT['controller']] + list(UVT_LIB.values()))
    report['coefficient_npz_headers'] = _npz_headers(nspec['coefficients']['path'])
    if nspec['galaxy'] == 'DDO154':
        seed_obj, changed, reusable = per_call_seed(nspec)
        report['seed'] = {'base_seed_reused_bitwise': reusable, 'changed_fields': changed}
        repro_like = reusable and nspec['numerics']['truncation']['shape'] == 'cube' and \
            nspec['physical']['entropy_K_factor'] == g['default_entropy_K_factor'] and \
            nspec['coefficients']['sha256'] == g['default_coefficients'][1] and nspec['numerics']['picard']['passes'] == 3 and \
            not geometry_active(nspec) and 'uv_tail' not in nspec['numerics']  # C2V008 (a), c2v003b; C2V010 (u): saved outputs are tail OFF
    else:  # c2v005 NGC3198 route B: the seed is the route-A lane's (route_a_inputs), never composed here
        report['seed'] = {'source': 'route_a_inputs.seed', 'route_a_inputs': nspec['route_a_inputs']}
        repro_like = False
    saved = dict(g['saved_runs']) if repro_like else {}
    ctx = Ctx('simulate', nspec, rd / 'simulated_call', saved_runs=saved)
    info, final = execute_chain(ctx)
    report['identity'] = info
    # c2v004: binding blockers and the fields each successor consumes (from its own module constants)
    report['binding_blockers'] = ((binding_blockers() + (ro1_off_blockers() if route_a_ro1_workers(nspec) else [])) if ctx.uv_tail is None else
                                  binding_blockers(ctx.scripts) + uvt_binding_blockers(ctx.uv_tail.get('source_rule') == 'nodes_v001'))  # C2V010 (u); r4
    consumed = {k: consumed_fields(k) for k in GENERALIZED}
    cp_ra = Path(info['route_a']['checkpoint'])
    ident_ra = info['route_a']['custody']['identity_sha256']
    it_ra = info['route_a'].get('reported_final_iteration')
    stages = []
    for rec in ctx.records:
        row = {k: rec.get(k) for k in ('name', 'kind', 'script', 'script_sha256', 'argv', 'stage_globals', 'module_patches', 'mask', 'note')}
        if rec.get('stage_dict_items'):
            row['stage_dict_items'] = rec['stage_dict_items']  # c2v003 (route-A prep V008 only)
        gen = GENERALIZED.get(rec.get('kind')) if rec.get('argv') else None
        if gen:  # c2v004 rows for a generalized successor
            gm = rec['galaxy_config']
            row['generalized_base'] = {'path': str(gen['base'][0]), 'sha256': gen['base'][1]}
            row['argv_without_galaxy_config'], row['galaxy_config_argv'] = split_galaxy_config_argv(rec['argv'])
            row['galaxy_config'] = gm
            row['dropped_stage_globals'] = gen['dropped_globals']
            row['omitted_fields_consumed'] = sorted(set(gm['omitted_per_call_fields']) & set(consumed[rec['kind']]))
            if gm['written']:
                row['stage_admission'] = probe_stage_admission(rec['kind'], gm['path'], gm['sha256'], ctx.scripts)  # C2V010: active script
            else:
                row['stage_admission'] = 'PENDING (config not written: per-call fields %s pending in simulate)' % gm['pending_fields']
                row['pending_probe'] = gm.get('pending_probe')  # c2v005: the successor's own admission on a placeholder copy
            if rec['kind'] != 'column_mean_v004' and isinstance(it_ra, int) and (cp_ra / 'IDENTITY.json').is_file():
                row['route_a_iteration_probe'] = probe_route_a_iteration(rec['kind'], cp_ra, ident_ra, it_ra)
        if rec.get('argv') and repro_like:
            outdir = _argv_map(rec['argv']).get('--outdir')
            orig = _orig_launch(outdir) if outdir else None
            if orig is not None:
                row['original_launch'] = str(Path(outdir).parent / 'launch.json')
                row['original_launch_script_identical'] = (orig[3] == rec['script'] and sha256_file(orig[3]) == rec['script_sha256'])
                if gen:  # c2v004: the saved launch ran the reviewed base of this successor
                    row['original_launch_script_is_generalized_base'] = (orig[3] == str(gen['base'][0]) and sha256_file(orig[3]) == gen['base'][1])
                row['argv_comparison'] = _compare_argv(rec['kind'], [rec['script']] + rec['argv'], orig)
                row['all_inputs_identical'] = (row['original_launch_script_identical'] or row.get('original_launch_script_is_generalized_base', False)) and all(
                    x['verdict'].startswith('IDENTICAL') or x['verdict'].startswith('OUTPUT_LOCATION') or x['verdict'] == 'GALAXY_CONFIG_ADDED'
                    or x['verdict'].startswith('MODULE_SUCCESSOR')
                    for x in row['argv_comparison'])
            else:
                row['original_launch'] = None
                row['note'] = (row.get('note') or '') + ' no saved launch for this stage (extra observation or new stage)'
        if rec.get('argv'):
            # override values versus the values hard-coded in the stage / dependency files
            ov = []
            if rec.get('stage_globals') or rec.get('module_patches') or rec.get('stage_dict_items'):
                m = exec_verified(rec['script'], rec['script_sha256'], 'c2v001_dry_' + rec['kind'])
                for name, val in (rec.get('stage_globals') or {}).items():
                    ov.append(_override_row(rec['kind'], name, m.__dict__.get(name, _ABSENT), _decode_value(val)))
                for gname, items in (rec.get('stage_dict_items') or {}).items():
                    for key, pin in items.items():
                        hard = (m.__dict__.get(gname) or {}).get(key, _ABSENT)
                        ov.append(_override_row(rec['kind'], '%s[%s]' % (gname, key), hard, (Path(pin['path']), pin['sha256'])))
                for patch in rec.get('module_patches') or []:
                    dm = exec_verified(patch['path'], patch['sha256'], 'c2v001_dry_dep')
                    for name, val in patch['set'].items():
                        ov.append(_override_row(Path(patch['path']).name, name, getattr(dm, name, _ABSENT), _decode_value(val)))
            row['override_comparison'] = ov
        stages.append(row)
    report['stages'] = stages
    report['passes_simulated'] = ctx.passes
    # c2v005: every remaining refusal, classified from the successors' own admission results and the driver
    gc_all = load_galaxy_config(nspec['galaxy'], nspec.get('member'))
    route_a_pending = route_a_inputs_pending(nspec.get('route_a_inputs'))  # c2v006: a template with PENDING sentinels is pending
    if nspec['galaxy'] != 'DDO154':
        report['n1_query_rows'] = n1_query_rows(nspec, gc_all)  # c2v006 (N1/A4)
        planned = {x['kind'] for x in stages if x.get('generalized_base')}
        pk = info['percall_known']
        unplanned = {}
        for kind in GENERALIZED:
            if kind in planned:
                continue
            pc = {k: pk.get(k, '%s(%s)' % (PENDING_ROUTE_A if route_a_pending else 'PENDING_RUN_OUTPUT', k)) for k in STAGE_PER_CALL[kind]}
            pc.update({k: pk[k] for k in gc_all['slots'] if k in pk and k in consumed_fields(kind)})
            prods = {nm: '%s(producer_pins.%s)' % (PENDING_ROUTE_A if route_a_pending else 'PENDING_RUN_OUTPUT', nm)
                     for nm in GENERALIZED[kind].get('producer_pins', {})} or None
            unplanned[kind] = pending_probe(kind, gc_all, pc, prods, rd / 'simulated_call' / 'inputs', 'unplanned')
        report['admission_probes_unplanned_stages'] = unplanned
    report['remaining_refusals'] = remaining_refusals_v006(report, info, gc_all, route_a_pending)
    if final is not None and final.get('rows'):
        report['final_rows_from_saved_chain'] = final['rows']
    sp = [ctx_row for ctx_row in stages if ctx_row.get('argv_comparison') is not None]
    report['summary'] = {
        'repro_like': repro_like,
        'stages_planned': len(stages),
        'stages_compared_with_original_launch': len(sp),
        'stages_all_inputs_identical': sum(1 for x in sp if x.get('all_inputs_identical')),
        'overrides_total': sum(len(x.get('override_comparison') or []) for x in stages),
        'overrides_noop_identical': sum(1 for x in stages for o in (x.get('override_comparison') or []) if o['verdict'] == 'NO_OP_IDENTICAL_VALUE'),
        # c2v003 (CHECK_V001 s1 doc correction): state the count as "n of total" and name the others.
        'overrides_not_noop': ['%s %s.%s: %s' % (x['name'], o['where'], o['name'], o['verdict']) for x in stages
                               for o in (x.get('override_comparison') or []) if o['verdict'] != 'NO_OP_IDENTICAL_VALUE'],
        'bracket_rule_checks': info.get('bracket_rule_checks'),
        'scipy_imports': report['transitive_pins']['scipy_imports'],
        'pin_problems': report['transitive_pins']['problems'],
        # c2v004
        'galaxy_config': {k: info['galaxy_config'][k] for k in ('path', 'sha256')},
        'driver_literals_equal_galaxy_config': all(r['equal'] for r in info['galaxy_config']['driver_literal_check']),
        'generalized_stage_calls': sum(1 for x in stages if x.get('generalized_base')),
        'stage_admission_accepted': sum(1 for x in stages if isinstance(x.get('stage_admission'), dict) and x['stage_admission'].get('accepted')),
        'stage_admission_refused': ['%s: %s' % (x['name'], x['stage_admission']['refusal']) for x in stages
                                    if isinstance(x.get('stage_admission'), dict) and not x['stage_admission'].get('accepted')],
        'stage_admission_pending': [x['name'] for x in stages if isinstance(x.get('stage_admission'), str)],
        'route_a_iteration_probes': {x['name']: x['route_a_iteration_probe'].get('iteration', x['route_a_iteration_probe'].get('refusal'))
                                     for x in stages if x.get('route_a_iteration_probe')},
        'omitted_fields_consumed': {x['name']: x['omitted_fields_consumed'] for x in stages if x.get('omitted_fields_consumed')},
        'producer_identity_run_mode_differs': [p for p in info.get('producer_identity', []) if p['run_mode_differs']],
        'binding_blockers': report['binding_blockers'],
        # c2v005
        'remaining_refusals_by_class': report['remaining_refusals']['by_class'],
        'refusals_beyond_pending_inputs': report['remaining_refusals']['beyond_pending_inputs'],
        'unexplained_refusals': report['remaining_refusals']['unexplained'],
        # c2v006
        'only_refusals_needing_route_a_bytes': report['remaining_refusals']['only_refusals_needing_route_a_bytes'],
        'deferred_route_a_checks': [x['where'] for x in report['remaining_refusals']['deferred_route_a_checks']],
        'n1_query_rows': report.get('n1_query_rows'),
    }
    ra = info.get('route_a', {})
    rp = Path(ra.get('attempt', '')) / 'result.json'
    if rp.is_file():
        src = json.loads(rp.read_text())['result'].get('source_pins', {})
        bad = [p for p, s in src.items() if not Path(p).is_file() or sha256_file(p) != s]
        report['route_a_recorded_source_pins'] = {'n': len(src), 'all_current_files_match': not bad, 'mismatch': bad,
            'note': 'prep V007/V008 loads these helper modules by path and RECORDS (does not verify) their SHA256; checked here from bytes'}
    report['summary']['overrides_wording'] = '%d of %d identity overrides are no-ops' % (
        report['summary']['overrides_noop_identical'], report['summary']['overrides_total'])
    report['summary']['route_a_prep'] = info.get('route_a', {}).get('prep')
    if ctx.uv_tail is not None:  # C2V010 (u): tail-ON plan record and summary (absent for tail OFF)
        report['uv_tail'] = ctx.uv_tail
        report['summary']['uv_tail'] = {
            'admissibility': ctx.uv_tail['admissibility'], 'pending_certificates': ctx.uv_tail['pending_certificates'],
            'source_rule': ctx.uv_tail.get('source_rule'), 'nodes_ext_context': ctx.uv_tail.get('nodes_ext_context'),  # C2V010 r4
            'domain_empty_all_stages': ctx.uv_tail['domain_empty_all_stages'], 'outer': ctx.uv_tail['outer'],
            'kept_regions': {k: v['kept'] for k, v in ctx.uv_tail['kept_regions'].items()},
            'route_a_worker': [x['script_sha256'] for x in stages if x['kind'] == 'route_a'],
            'tail_stage_scripts': {x['name']: x['script_sha256'] for x in stages if x['kind'] in UVT_TAIL_KINDS + ('route_a_tail_manifest',)},
            'refusal_classes_beyond_pending': sorted({it['class'] for it in report['remaining_refusals']['items']
                                                      if it['class'] not in EXPECTED_PENDING_CLASSES})}
    lines = ['DRY-RUN PLAN %s  (spec %s)' % (nspec.get('label', ''), report['call_spec_sha256']), '']
    if info.get('geometry'):  # C2V008 (a): only at a per-call geometry (the registered-geometry report is unchanged)
        gp = info['geometry']['stage_admission_probe']
        report['summary']['geometry'] = {'distance_Mpc': info['geometry']['distance_Mpc'], 'files': info['geometry']['files'],
                                         'config_fields': sorted(info['geometry']['config_fields']),
                                         'stage_binding_admits_geometry': gp['admitted'], 'refused_by': gp['refused'],
                                         'registered_controls_accepted': gp['controls_accepted']}
        lines.append('GEOMETRY distance %r Mpc (per-call files %s); stage binding admits it: %s; registered controls accepted: %s'
                     % (info['geometry']['distance_Mpc'], sorted(info['geometry']['files']), gp['admitted'], gp['controls_accepted']))
        for kind, msg in sorted(gp['refused'].items()):
            lines.append('  REFUSED by %s own admission: %s' % (kind, msg))
        lines.append('')
    if ctx.uv_tail is not None:  # C2V010 (u)
        u = ctx.uv_tail
        lines.append('UV TAIL (C2V010): admissibility %s; outer %s; K %.6g/kpc; all stage domains empty: %s; pending certificates: %s'
                     % (u['admissibility'], u['outer'], u['K_inverse_kpc'], u['domain_empty_all_stages'], u['pending_certificates'] or 'none'))
        lines.append('UV TAIL source rule (r4): %s%s' % (u.get('source_rule'), '' if not u.get('nodes_ext_context') else
                     '; ext grid %s (%d extra nodes)' % (u['nodes_ext_context']['ext_spec']['version'] if 'version' in u['nodes_ext_context']['ext_spec'] else '?',
                                                      u['nodes_ext_context']['n_ext_nodes'])))
        for k, v in u['kept_regions'].items():
            lines.append('  kept %-14s %-12s %s empty=%s' % (k, v['binding_kind'], v['kept'], v['domain_empty']))
        lines.append('')
    for b in report['binding_blockers']:  # c2v004
        lines.append('BINDING BLOCKER (run mode refuses before any stage): ' + b)
    if report['binding_blockers']:
        lines.append('')
    rr = report['remaining_refusals']  # c2v005
    lines.append('REMAINING REFUSALS (c2v006, from the successors\' own admission and the driver; only route-A bytes missing: %s):'
                 % rr['only_refusals_needing_route_a_bytes'])
    for cls, items in rr['by_class'].items():
        lines.append('  %-30s %s' % (cls, ', '.join(items)))
    if rr['beyond_pending_inputs']:
        lines.append('  beyond pending inputs: ' + '; '.join(rr['beyond_pending_inputs']))
    lines.append('')
    for i, s in enumerate(stages, 1):
        verdict = s.get('all_inputs_identical')
        lines.append('%02d %-22s %-18s %s  inputs_identical_to_saved_launch=%s' % (i, s['name'], s['kind'] or '', (s['script_sha256'] or '')[:12], verdict))
        for x in s.get('argv_comparison') or []:
            lines.append('      %-34s %-15s %s' % (x['flag'], x['role'], x['verdict']))
        if s.get('argv') and not s.get('argv_comparison'):
            lines.append('      argv: ' + ' '.join(str(a).replace(str(ROOT), '$ROOT').replace(str(rd), '$DRY') for a in s['argv']))
        if s.get('mask'):
            lines.append('      mask: shape=%s kmax=%.6g/m g4_blob=%s (weight mask on existing grid)' % (s['mask']['shape'], s['mask']['kmax_inverse_m'], s['mask']['g4_file_sha256'][:16]))
        for gname, items in (s.get('stage_dict_items') or {}).items():
            for key, pin in items.items():
                lines.append('      dict item %s[%s] := %s %s' % (gname, key, Path(pin['path']).name, pin['sha256'][:12]))
        for o in s.get('override_comparison') or []:
            lines.append('      override %s.%s: %s' % (o['where'], o['name'], o['verdict']))
        if s.get('galaxy_config'):  # c2v004
            gm = s['galaxy_config']
            lines.append('      galaxy-config %s %s (%s; per-call %s)' % (Path(gm['path']).name, gm['sha256'][:16] if gm['written'] else gm['sha256'],
                                                                      gm['format'], ','.join(gm['per_call_fields'])))
            adm = s['stage_admission']
            lines.append('      stage admission: ' + (('ACCEPTED' if adm['accepted'] else 'REFUSED ' + adm['refusal']) if isinstance(adm, dict) else adm))
            if s.get('pending_probe'):
                pa = s['pending_probe']['admission']
                lines.append('      placeholder-copy admission: ' + ('ACCEPTED' if pa['accepted'] else 'REFUSED ' + pa['refusal']))
            if s.get('route_a_iteration_probe'):
                lines.append('      route-A iteration (stage rule on checkpoint records): %s' % s['route_a_iteration_probe'])
            lines.append('      dropped stage globals -> config: %s' % s['dropped_stage_globals'])
        if s.get('note'):
            lines.append('      note: ' + s['note'].strip())
    for kind, pr in (report.get('admission_probes_unplanned_stages') or {}).items():  # c2v005 (NGC3198)
        pa = pr['admission']
        lines.append('-- %-20s (not reached in simulate) placeholder-copy admission: %s' % (kind, 'ACCEPTED' if pa['accepted'] else 'REFUSED ' + pa['refusal']))
    with open(rd / 'DRYRUN_PLAN.txt', 'x') as f:
        f.write('\n'.join(lines) + '\n')
    _write_x(rd / 'DRYRUN_REPORT.json', report)
    print(json.dumps(_jsonable(report['summary']), indent=1))
    return 0


_ABSENT = object()


def _override_row(where, name, hard, new):
    if hard is _ABSENT:
        return {'where': where, 'name': name, 'hard_coded': None, 'per_call': str(new), 'verdict': 'OVERRIDE_TARGET_ABSENT'}
    def norm(v):
        if isinstance(v, dict):
            return {str(k): norm(x) for k, x in v.items()}
        if isinstance(v, (list, tuple)):
            return [norm(x) for x in v]
        return str(v) if isinstance(v, Path) else v
    a, b = norm(hard), norm(new)
    if a == b:
        verdict = 'NO_OP_IDENTICAL_VALUE'
    elif isinstance(b, str) and b.startswith('PENDING'):
        verdict = 'PER_CALL_VALUE_PENDING'
    else:
        verdict = 'PER_CALL_VALUE_DIFFERS_FROM_HARDCODED'
    return {'where': where, 'name': name, 'hard_coded': a, 'per_call': b, 'verdict': verdict}


# ============================================================================= C2V006 NGC3198 route B
# Route B for NGC3198 consumes the outputs of the NGC route-A lane (it does not run route A) and the N3 monotone source
# (a declared input slot, admitted only as the reviewed reducer output 746980f2, D3/A3).  Every galaxy value comes from the
# galaxy config (schema V004 NGC entry: N1 GL4, N2 66.904 kpc, N4 rows, A4 rows; member GL10_ALTERNATIVE: A2).  Nothing
# undecided is filled: an undecided field is a remaining refusal, listed by the dry run and BLOCKING run mode before any stage.
EXPECTED_PENDING_CLASSES = ('PENDING_ROUTE_A_OUTPUTS', 'PENDING_N3_MONOTONE_SOURCE', 'PRODUCED_BY_THIS_CALL')
ROUTE_A_INPUT_KEYS = ('seed', 'attempt_directory', 'checkpoint_directory', 'identity_sha256', 'result_sha256')
# c2v006 (CHECK D8): the checks that need the NGC route-A bytes.  While route A is pending each is listed by the dry run as
# a PENDING_ROUTE_A_OUTPUTS item; with route-A bytes each runs (execute_chain / route_a_custody / the stages) and fails closed.
NGC_DEFERRED_ROUTE_A_CHECKS = (
    ('route_a.seed', 'route_a_inputs.seed {path, sha256} verified from bytes and equal to the checkpoint caller seed (route_a_custody)'),
    ('route_a.seed_coefficients', 'the call coefficient grid equals the coefficients the route-A seed records (A5, ngc_seed_coefficient_check)'),
    ('route_a.seed_physical', 'call physical Eref_J*s, gamma*s, ell_F_m equal the route-A seed numerical_inputs bitwise (A5)'),
    ('route_a.attempt', 'route-A attempt finish.json RETURNED_ACTUAL_RESULT; result.json sha256 == route_a_inputs.result_sha256'),
    ('route_a.checkpoint_identity', 'checkpoint IDENTITY self-hash == route_a_inputs.identity_sha256; caller physical_parameters == call (route_a_custody)'),
    ('route_a.coefficient_grid_digest', 'checkpoint inputs_sha256.fourier_arguments.source_hessian_grid == digest of the call grid (the kept D1 guard)'),
    ('route_a.accepted_iteration', 'final converged iteration by the strict reader (route_a_reported_iteration; every stage re-derives it)'),
    ('route_a.solver_template_mapping', 'NGC solver template == the N4 mapping of the route-A seed HI controls (template_mapping_check)'),
    ('reference.roster_digest', 'reference stage: route-A roster digest and N2-truncated roster against the checkpoint records'),
    ('per_call_fields', 'custody.* per-call fields and stage producer pins (exist only once route A and the earlier stages exist)'),
)
INVALID_ROW_REASON = 'QUERY_INSIDE_INNERMOST_NODE'
NGC_ROSTER_BY_MEMBER = {None: 'NGC3198_truncated_N2', 'GL10_ALTERNATIVE': 'NGC3198_truncated_N2_GL10_alternative'}


def route_a_inputs_pending(ra):
    """c2v006: route_a_inputs is pending when it is the PENDING_ROUTE_A_OUTPUTS string or an object holding any PENDING sentinel
    (a template naming the future run directories).  Pending inputs are never opened."""
    if ra == PENDING_ROUTE_A:
        return True
    return isinstance(ra, dict) and _has_pending(ra)


def ngc_seed_coefficient_check(seed_doc, call_coeff, g):
    """c2v006 (A5, CHECK D1): the call coefficient grid must equal the grid the NGC route-A seed records ({path, sha256}).  A seed
    without a record ran NGC prep v001's own default (fe5a2f06, prep:19-20).  The checkpoint grid digest (route_a_custody) stays
    the guard.  Returns the record; Refusal otherwise."""
    rec = seed_doc.get('coefficients')
    if rec is None:
        seed_grid = {'path': str(g['default_coefficients'][0]), 'sha256': g['default_coefficients'][1]}
        source = 'NGC prep v001 default (prep:19-20); the route-A seed records no coefficients'
    else:
        if not isinstance(rec, dict) or not isinstance(rec.get('path'), str) or not _is_hex64(rec.get('sha256')):
            raise Refusal('NGC route-A seed coefficients record must be {path, sha256, ...}')
        seed_grid = {'path': str(Path(rec['path'])), 'sha256': rec['sha256']}
        source = 'route-A seed coefficients record'
    call = {'path': str(Path(call_coeff['path'])), 'sha256': call_coeff['sha256']}
    if seed_grid != call:
        raise Refusal('NGC3198 route B (A5): call coefficient grid %s differs from the NGC route-A seed grid %s (%s)'
                      % (call['sha256'][:16], seed_grid['sha256'][:16], source))
    return {'call': call, 'route_a_seed': seed_grid, 'source': source, 'equal': True,
            'guard_kept': 'route_a_custody: checkpoint source_hessian_grid digest == digest of the call grid'}


def final_rows_check(final, n_queries):
    """(rows_ok, invalid_row_ids or None).  Rows without a 'valid' key (DDO154; any binding without invalid_row_rule): the
    c2v005 rule, n_queries rows all finite.  Rows with 'valid' (c2v006 column mean, A4/N1): valid rows finite, invalid rows
    valid=false with reason QUERY_INSIDE_INNERMOST_NODE and speed null; at least one valid row."""
    rows = final.get('rows')
    if not isinstance(rows, list) or len(rows) != n_queries:
        return False, None
    if not any('valid' in r for r in rows):
        return all(math.isfinite(r['speed_km_s']) for r in rows), None
    invalid = []
    for r in rows:
        if r.get('valid') is True:
            if isinstance(r.get('speed_km_s'), bool) or not isinstance(r.get('speed_km_s'), (int, float)) or not math.isfinite(r['speed_km_s']):
                return False, None
        elif r.get('valid') is False and r.get('reason') == INVALID_ROW_REASON and r.get('speed_km_s') is None:
            invalid.append(r['id'])
        else:
            return False, None
    if len(invalid) == len(rows):
        return False, None
    return True, invalid


def _sentinel_or(v, check, label):
    if isinstance(v, str) and v.startswith('PENDING'):
        return v
    return check(v, label)


def _hex_or_refuse(v, label):
    if not _is_hex64(v):
        raise Refusal(label + ' must be 64 lowercase hex or a PENDING sentinel')
    return v


def normalize_ngc_route_b_spec(spec):
    _strict(spec, ('schema', 'galaxy', 'label', 'member', 'physical', 'coefficients', 'numerics', 'route_a_inputs', 'source_slots',
                   'reference_compare'), 'spec')
    g = GALAXIES['NGC3198']
    member = spec.get('member')
    if member is not None and ('NGC3198', member) not in GC_MEMBER_ENTRY:
        raise Refusal('member must be absent (primary) or one of %s' % sorted(m for _, m in GC_MEMBER_ENTRY))
    gc = load_galaxy_config('NGC3198', member)
    phys = spec.get('physical', {})
    _strict(phys, ('Eref_J', 'ell_F_m', 'gamma', 'common_scale_s', 'entropy_K_factor', 'distance_Mpc', 'inclination_deg'), 'physical')
    kf, kf_ok, kf_st = gc_value(gc, 'entropy.K_factor')
    if not kf_ok or g['entropy_K_members'].get(kf) != 'N4_PRIMARY_64_OVER_121':
        raise Refusal('NGC3198 entropy.K_factor is %s / %r in the galaxy config' % (kf_st, kf))
    geo = g['registered_geometry']
    p = {'Eref_J': _num(phys.get('Eref_J'), 'Eref_J'), 'ell_F_m': _num(phys.get('ell_F_m'), 'ell_F_m'),
         'gamma': _num(phys.get('gamma'), 'gamma'), 'common_scale_s': _num(phys.get('common_scale_s', 1.0), 'common_scale_s'),
         'entropy_K_factor': _num(phys.get('entropy_K_factor', kf), 'entropy_K_factor'),
         'distance_Mpc': _num(phys.get('distance_Mpc', geo['distance_Mpc']), 'distance_Mpc'),
         'inclination_deg': _num(phys.get('inclination_deg', geo['inclination_deg']), 'inclination_deg')}
    if p['distance_Mpc'] != geo['distance_Mpc'] or p['inclination_deg'] != geo['inclination_deg']:
        raise Refusal('UNSUPPORTED NGC geometry: only the registered 13.8 Mpc / 72 deg (profile NGC3198.geometry) is supported')
    # c2v006 (CHECK D6): only the N4 primary 64/121 or the declared N4 original-K alternative 1.0, labelled.
    if p['entropy_K_factor'] not in g['entropy_K_members']:
        raise Refusal('NGC3198 entropy_K_factor must be 64/121 (N4 primary) or 1.0 (N4 declared original-K alternative), not %r'
                      % p['entropy_K_factor'])
    p['entropy_K_member'] = g['entropy_K_members'][p['entropy_K_factor']]
    # c2v006 (A5, CHECK D1 MAJOR): a decided grid; it must ALSO equal the NGC route-A seed's grid (checked with route-A bytes).
    coeff = spec.get('coefficients', None) or {'path': str(g['default_coefficients'][0]), 'sha256': g['default_coefficients'][1]}
    _strict(coeff, ('path', 'sha256'), 'coefficients')
    if not _is_hex64(coeff.get('sha256')) or not isinstance(coeff.get('path'), str):
        raise Refusal('coefficients {path, sha256(64 lowercase hex)} required')
    _abs(coeff['path'], 'coefficients.path')
    dg = g['decided_coefficient_grids'].get(coeff['sha256'])
    if dg is None or str(Path(coeff['path'])) != str(dg[0]):
        raise Refusal('NGC3198 route B (A5): the coefficient grid must be a decided grid %s, and it must equal the grid the NGC '
                      'route-A seed records (fe5a2f06 is the V004 provisional grid = NGC prep v001 default, not a route-A grid)'
                      % {k[:16]: v[1] for k, v in g['decided_coefficient_grids'].items()})
    num = spec.get('numerics', {})
    _strict(num, ('picard', 'brackets', 'column_workers', 'truncation'), 'numerics')
    tr = num.get('truncation', {'shape': 'cube'})
    _strict(tr, ('shape',), 'truncation')
    if tr.get('shape', 'cube') != 'cube':
        raise Refusal('NGC3198 route B: only the cube grid (no k-space mask) is supported; route A has no mask hook')
    out_num = {'composite_grid_spec': None, 'truncation': {'shape': 'cube', 'kmax_inverse_kpc': None}}
    pc = num.get('picard', {})
    _strict(pc, ('passes', 'speed_change_bound_km_s', 'observe_every_pass'), 'picard')
    passes = pc.get('passes', 3)
    if type(passes) is not int or not 1 <= passes <= 12:
        raise Refusal('picard.passes must be an int in 1..12')
    bound = pc.get('speed_change_bound_km_s', None)
    if bound is not None:
        bound = _num(bound, 'speed_change_bound_km_s')
    obs = pc.get('observe_every_pass', True)
    if type(obs) is not bool:
        raise Refusal('observe_every_pass must be bool')
    out_num['picard'] = {'passes': passes, 'speed_change_bound_km_s': bound, 'observe_every_pass': obs}
    # c2v006 (A4): the galaxy-config rule factors (= DDO154 values); no overrides (the DDO154 manual corrections are not carried).
    bk = num.get('brackets', {'mode': 'rule'})
    _strict(bk, ('mode', 'rule'), 'brackets')
    if bk.get('mode', 'rule') != 'rule':
        raise Refusal('NGC3198 route B: brackets.mode must be rule (pinned controls exist only for the saved DDO154 chain)')
    rf, rf_ok, rf_st = gc_value(gc, 'brackets.rule_factors')
    if not rf_ok:
        raise Refusal('NGC3198 brackets.rule_factors is %s in the galaxy config' % rf_st)
    rule = {'fs_absolute_overrides': {}, 'rfs_factor_overrides': {}, 'le_factor_overrides': {}}
    for k in ('rfs_factors', 'le_first_factors', 'le_next_factors'):
        rule[k] = list(rf[k])
    r_in = bk.get('rule', {})
    _strict(r_in, tuple(LE_RULE_DEFAULTS), 'brackets.rule')
    for k, v in r_in.items():
        if k.endswith('_overrides'):
            if v != {}:
                raise Refusal('NGC3198 route B (A4): %s must be empty; the DDO154 manual corrections are not carried and any NGC '
                              'column failure is a recorded result' % k)
        elif v != rule[k]:
            raise Refusal('NGC3198 route B (A4): %s must equal the galaxy-config rule factors %r' % (k, rule[k]))
    out_num['brackets'] = {'mode': 'rule', 'rule': rule, 'rule_factors_source': 'galaxy config brackets.rule_factors (A4: = DDO154)'}
    workers = num.get('column_workers', 1)
    if type(workers) is not int or not 1 <= workers <= 12:
        raise Refusal('column_workers must be int 1..12')
    out_num['column_workers'] = workers
    # c2v006: route_a_inputs = PENDING string, or {seed, attempt_directory, checkpoint_directory, identity_sha256, result_sha256}
    # where (template) any value may be a PENDING sentinel; directories are absolute and never opened while pending.
    ra = spec.get('route_a_inputs', PENDING_ROUTE_A)
    if ra != PENDING_ROUTE_A:
        _strict(ra, ROUTE_A_INPUT_KEYS, 'route_a_inputs')
        if set(ra) != set(ROUTE_A_INPUT_KEYS):
            raise Refusal('route_a_inputs needs %s' % (ROUTE_A_INPUT_KEYS,))
        seed = ra['seed']
        if not (isinstance(seed, str) and seed.startswith('PENDING')):
            if not (isinstance(seed, dict) and set(seed) == {'path', 'sha256'}):
                raise Refusal('route_a_inputs.seed must be {path, sha256} or a PENDING sentinel')
            seed = {'path': _sentinel_or(seed['path'], _abs, 'route_a_inputs.seed.path'),
                    'sha256': _sentinel_or(seed['sha256'], _hex_or_refuse, 'route_a_inputs.seed.sha256')}
        norm_ra = {'seed': seed}
        for k in ('attempt_directory', 'checkpoint_directory'):
            norm_ra[k] = str(_abs(ra[k], 'route_a_inputs.' + k))
        for k in ('identity_sha256', 'result_sha256'):
            norm_ra[k] = _sentinel_or(ra[k], _hex_or_refuse, 'route_a_inputs.' + k)
        ra = norm_ra
    # c2v006 (D3, A3): the slot admits only the reviewed N3 output (exceptions {23}), 746980f2.
    slots_in = spec.get('source_slots', {}) or {}
    _strict(slots_in, tuple(gc['slots']), 'source_slots')
    slots = {}
    for k in gc['slots']:
        v = slots_in.get(k, PENDING_SLOT)
        if v != PENDING_SLOT:
            _strict(v, ('path', 'sha256'), 'source_slots.' + k)
            if not _is_hex64(v.get('sha256')):
                raise Refusal('source_slots.%s sha256 must be 64 lowercase hex' % k)
            _abs(v.get('path'), 'source_slots.%s.path' % k)
            pin = g['monotone_source_pin'] if k == 'source.monotone_source' else None
            if pin is None or (str(Path(v['path'])), v['sha256']) != (str(pin[0]), pin[1]):
                raise Refusal('source_slots.%s (CHECK D3, A3): only the reviewed N3 output %s (%s) is admissible' % (k, pin[1][:16] if pin else None, pin[0] if pin else None))
            verify_pin(pin[0], pin[1], 'N3 monotone source')
            v = {'path': str(v['path']), 'sha256': v['sha256']}
        slots[k] = v
    if spec.get('reference_compare', False) is not False:
        raise Refusal('NGC3198 route B has no saved chain to compare against')
    return {'schema': SCHEMA, 'galaxy': 'NGC3198', 'member': member, 'label': spec.get('label', ''), 'physical': p,
            'coefficients': {'path': str(coeff['path']), 'sha256': coeff['sha256']}, 'numerics': out_num, 'admit': {},
            'reference_compare': False, 'route_a_inputs': ra, 'source_slots': slots}


def n1_query_rows(nspec, gc):
    """c2v006 (N1/A4): the query rows below the innermost / beyond the outermost route-B radial node of this member's roster
    (schema derived rosters), and whether the pinned observation binding carries the invalid_row_rule."""
    rows, rows_ok, _ = gc_value(gc, 'observation.query_rows')
    rosters = gc['schema'].get('derived_rosters', {})
    ros = rosters.get(NGC_ROSTER_BY_MEMBER[nspec.get('member')]) if nspec['galaxy'] == 'NGC3198' else rosters.get(nspec['galaxy'])
    if not rows_ok or not ros:
        return None
    lo = ros.get('innermost_node_kpc', ros.get('smallest_node_kpc'))
    hi = ros.get('outermost_node_kpc', ros.get('largest_node_kpc'))
    b, b_ok, _ = gc_value(gc, 'observation.binding')
    rule = json.loads(Path(b['path']).read_bytes()).get('invalid_row_rule') if b_ok and sha256_file(b['path']) == b['sha256'] else None
    return {'roster': {'innermost_node_kpc': lo, 'outermost_node_kpc': hi},
            'below_innermost': [q['id'] for q in rows if q['radius_m'] / KPC_M < lo],
            'beyond_outermost': [q['id'] for q in rows if q['radius_m'] / KPC_M > hi],
            'binding_invalid_row_rule': rule}


def route_b_static_refusals(nspec, gc):
    """c2v006: refusals known before any stage, from the call spec and the galaxy config: route-A outputs pending, declared input
    slots unfilled, consumed galaxy fields that are not admissible for this galaxy, driver-level fields, query rows the column
    mean cannot handle.  DDO154: always empty (every consumed field is the exact literal)."""
    out = []
    if route_a_inputs_pending(nspec.get('route_a_inputs')):
        out.append({'where': 'route_a', 'class': 'PENDING_ROUTE_A_OUTPUTS', 'field': 'route_a_inputs',
                    'refusal': 'NGC route-A outputs (seed, attempt, checkpoint) not supplied'})
    for k in gc['slots']:
        if _has_pending((nspec.get('source_slots') or {}).get(k, PENDING_SLOT)):
            out.append({'where': k, 'class': 'PENDING_N3_MONOTONE_SOURCE', 'field': k, 'refusal': 'DECLARED_INPUT_SLOT not filled'})
    for kind in GENERALIZED:
        for n in consumed_fields(kind):
            if n in PER_CALL_FIELDS or n in gc['slots']:
                continue
            v, ok, st = gc_value(gc, n)
            if not ok:
                out.append({'where': kind, 'class': 'UNDECIDED_NGC_FIELD' if st == 'NONE_IN_REVIEWED_CODE' else 'NOT_ADMISSIBLE',
                            'field': n, 'refusal': '%s is %s' % (n, st)})
    for n in ('driver.fixed_args',):
        v, ok, st = gc_value(gc, n)
        if not ok:
            out.append({'where': 'driver', 'class': 'UNDECIDED_NGC_FIELD' if st == 'NONE_IN_REVIEWED_CODE' else 'NOT_ADMISSIBLE',
                        'field': n, 'refusal': '%s is %s' % (n, st)})
    # N1 (A4): rows below the innermost node are emitted valid=false by the c2v004 column mean when the binding carries the
    # invalid_row_rule; without it (or for rows beyond the outermost node, which no decision covers) the reviewed adapter refuses
    # the whole call, a certain final-stage failure listed here.
    n1 = n1_query_rows(nspec, gc)
    if n1:
        lo, hi = n1['roster']['innermost_node_kpc'], n1['roster']['outermost_node_kpc']
        if n1['below_innermost'] and (n1['binding_invalid_row_rule'] or {}).get('reason') != INVALID_ROW_REASON:
            out.append({'where': 'column_mean_v004', 'class': 'N1_INVALID_ROW_HANDLING_ABSENT', 'field': 'observation.binding',
                        'refusal': '%s lie below the innermost radial node %.6g kpc and the binding has no invalid_row_rule; the reviewed '
                                   'adapter refuses the whole call (QUERY_OUTSIDE_SUPPLIED_RADIAL_SUPPORT)' % (n1['below_innermost'], lo)})
        if n1['beyond_outermost']:
            out.append({'where': 'column_mean_v004', 'class': 'N1_QUERY_BEYOND_OUTERMOST_NODE', 'field': 'observation.query_rows',
                        'refusal': '%s lie beyond the outermost radial node %.6g kpc; no decision covers them and the reviewed adapter '
                                   'refuses the whole call' % (n1['beyond_outermost'], hi)})
    rule = (nspec['numerics'].get('brackets') or {}).get('rule') or {}
    bad = [k for k in ('rfs_factors', 'le_first_factors', 'le_next_factors') if _has_pending(rule.get(k))]
    if bad:
        out.append({'where': 'driver', 'class': 'UNDECIDED_NGC_FIELD', 'field': 'brackets.rule_factors',
                    'refusal': 'brackets.rule_factors is NONE_IN_REVIEWED_CODE and the call spec supplies none: %s' % bad})
    return out


def remaining_refusals_v006(report, info, gc, route_a_pending):
    """Every refusal of the dry run, classified.  Sources: the driver (info.refusals, including the c2v006 deferred route-A
    checks), every successor's own admission on its written config or on a placeholder copy (pending per-call values are the
    placeholders themselves), and the static scan.  A refusal part that cannot be attributed to a field is UNEXPLAINED."""
    items = []

    def cls_of(field):
        if field == 'producer_pins' or field in PER_CALL_FIELDS:
            return 'PENDING_ROUTE_A_OUTPUTS' if route_a_pending else 'PRODUCED_BY_THIS_CALL'
        if field in gc['slots']:
            return 'PENDING_N3_MONOTONE_SOURCE'
        e = gc['cfg']['fields'].get(field)
        if e is not None and e['status'] == 'NONE_IN_REVIEWED_CODE':
            return 'UNDECIDED_NGC_FIELD'
        return 'OTHER'

    def from_admission(where, adm):
        if not isinstance(adm, dict) or adm.get('accepted'):
            return
        msg = adm['refusal']
        if 'nothing guessed: ' not in msg:
            items.append({'class': 'UNEXPLAINED', 'where': where, 'field': None, 'text': msg})
            return
        for part in msg.split('nothing guessed: ', 1)[1].split('; '):
            field = part.split(' ')[0].rstrip(':')
            items.append({'class': cls_of(field), 'where': where, 'field': field, 'text': part})
    for r in info.get('refusals', []):
        items.append({'class': r['class'], 'where': r['where'], 'field': r['where'], 'text': r['refusal']})
    for s in report['stages']:
        from_admission(s['name'], s.get('stage_admission'))
        if s.get('pending_probe'):
            from_admission(s['name'] + ' (placeholder copy)', s['pending_probe']['admission'])
    for kind, pr in (report.get('admission_probes_unplanned_stages') or {}).items():
        from_admission(kind + ' (not reached in simulate; placeholder copy)', pr['admission'])
    static = route_b_static_refusals(report['normalized_spec'], gc)
    for r in static:
        items.append({'class': r['class'], 'where': r['where'], 'field': r['field'], 'text': r['refusal']})
    by_class = {}
    for it in items:
        by_class.setdefault(it['class'], set()).add(it['field'] or it['where'])
    beyond = sorted({'%s: %s' % (it['class'], it['field'] or it['where']) for it in items if it['class'] not in EXPECTED_PENDING_CLASSES})
    only_route_a = sorted({it['class'] for it in items}) in ([], ['PENDING_ROUTE_A_OUTPUTS'])
    return {'by_class': {k: sorted(v) for k, v in sorted(by_class.items())}, 'beyond_pending_inputs': beyond,
            'unexplained': [it for it in items if it['class'] in ('UNEXPLAINED', 'OTHER')], 'static': static, 'items': items,
            'expected_pending_classes': list(EXPECTED_PENDING_CLASSES),
            'only_refusals_needing_route_a_bytes': only_route_a,
            'deferred_route_a_checks': [{'where': w, 'check': c} for w, c in NGC_DEFERRED_ROUTE_A_CHECKS] if route_a_pending else []}


# ============================================================================= NGC3198 (c2v002)
# Configuration only.  No NGC physics is implemented here: the NGC route-A chain is the reviewed
# ngc43 worker -> NGC prep v001 -> NGC binding v001 -> composite adapter -> 0424 solver, executed
# (when a reviewed successor unblocks it) from exact pinned bytes like every DDO stage.
NGC_SCHEMA = 'UNT_GALAXY_M0_FORWARD_CALL_NGC_C2V002'
NGC_RESULT_SCHEMA = 'UNT_GALAXY_M0_FORWARD_RESULT_NGC_C2V002'
NGC_CODE = {
    'worker': (HR / 'ngc43_composite_coupled_root_worker_v001.py', '1b95a4ff333f17cf7bc6ab56b76c4e615e982a298ee1a95fd80f07c8ab6c0ca4'),
    'prep': (HR / 'ngc_actual_initial_source_preparation_v001.py', 'c54c7cc995f0bb59bb5d81a3f1267dba5dae48d116302c9c0438fe7e5a53710f'),
    'binding': (HR / 'ngc_composite_full_coupled_binding_v001.py', '9e9caf83bcbbe259d371e923242cddc9011aa7f9f9830d63479138756d9b1248'),
    'composite': (HC / 'owned_composite_prepared_coupled_gas_adapter_v001.py', '75092cf64cf5293d9e1a5b28b2c909d875c1f5a1b3e9d185f71f065ccff49ec3'),
    'stream': (HC / 'owned_streamed_fourier_per_run_adapter_v001.py', 'cbbc4b968fc189440ddd4f516fb53f07d04a97b638fdf90fd90f50422afb928e'),
    'base': (HR / 'owned_physical_fourier_metric_quadrature_v005.py', '7167a264aace95b0dd0732799534a39e9a271dbd9bf09abec16d02e6f647d491'),
    'prediction': (HC / 'galaxy_coupled_fourier_hi_prediction_v005.py', '54136c71403c90b82f5b150672bf218577bf837c345798ec5f770adf31ba8c72'),
}
NGC_DATA = {
    'profile': (C1 / 'GALAXY_RADIAL_SOURCE_REFERENCE_V001.json', 'f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b'),
    'manifest': (C1 / 'NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json', 'a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494'),
    'h2_tail_reduction': (C1 / 'NGC3198_H2_SOURCE_TAIL_REDUCTION_RUN_V001/stdout.txt', '157ede0487beed6658a413ae4db34cae2e819efc58efd292ccc56794ae5917d2'),
    'h2_source': (HR / 'NGC3198_MAIN_SOURCE_ANNULAR_INPUT_V001.json', '84e20bc022a088f7223319638091b65044983412cec09ac1cb0fb21d205aed61'),
    'physical_source_state_binding': (C1 / 'GALAXY_PHYSICAL_SOURCE_STATE_BINDING_V003.json', '7cadac8b66096a9d9942e9861289a1d41bad084e13cd7ba655341eb06e6afae9'),
    'stellar_photometry_nodes': (HR / 'NGC3198_DDO154_STELLAR_PHOTOMETRY_NODES_V001.json', '90657540e9d730c0af4d7a1b7fe66ec827f2c0bbb82f921df1398f23d6ab6935'),
    'source_only_bundle': (C1 / 'NGC3198_SOURCE_ONLY_BUNDLE_CANDIDATE_V001.json', '62abc88f12cb9da99ea1f1ba27c7eab2454553391984a65e2aa87a155fcc1fc1'),
    'review_worker': (HP / 'NGC43_COMPOSITE_ROOT_WORKER_DISTINCT_REVIEW_V001.json', '32736643ff32472c5a00ebab4eb91881be5332508f7f39b31a9e31e5f489c1ca'),
    'review_binding': (HP / 'NGC43_COMPOSITE_H2_BINDING_DISTINCT_REVIEW_V001.json', '23d1d395cf124bb4f71474aca35bff49abeca3f813a6fc46ee35732f3c85c39f'),
    # numerical controls of the candidate NGC seed are carried from the current DDO seed (V002)
    'parameter_seed': (C1 / 'DDO154_STABLE_CACHED_COUPLED_TRIAL_SEED_V002.json', '694eaaaab38547a369ac85c3c3d0b5550d8878753ccafe7bc0e5cdcb79be6680'),
}
# Evidence for the route-A blocker (read-only; nothing here is executed except inert definitions).
NGC_EVIDENCE = {
    'checkpoint_c2v001': (EX / 'resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v001.py', 'a831fe81ef25a065201f0c5d7e2cb4447a7d8cf3712507b1462a09ff4e0d2dd3'),
    'checkpoint_c2v002': (EX / 'resumable_coupled_gas_0422/coupled_gas_checkpoint_c2v002.py', '0bb955ed86c6e71884152c1dd97c41e2d086a4cd2e135f78e9b2716d2e4803c1'),
    'solver_nonfixedsrc': (EX / 'resumable_coupled_gas_0422/coupled_hi_fourier_source_iteration_v005_resume_c2v001.py', 'c91c5051ad7fea477a51dc9fbdaae2cdc755cc8186a318aa27627cf9d21651e6'),
    'ddo_stable_binding_v002': (HR / 'ddo_composite_stable_cached_binding_v002.py', 'd81b24b7150c846a5b70c82a8668daaaef53335ced062763980a33cdbc90b6d5'),
    'ddo_precedent_failure': (C1 / 'DDO154_STABLE_CACHED_COUPLED_RUN_V001/attempt_000/failure.json', '3743adff8ba446310e28e074089a1080ba0cabc9d18fa2ba2eae555a7df6f301'),
}
NGC_PREP_MAX_AXIS_NODES = 80  # NGC prep v001 guard (nk>80 refused); not a driver choice

# Every DDO-specific hard-coding of the route-B chain and what the NGC configuration supplies.
# (stage, file key in SCRIPTS/AUX or None for the driver itself, needles located at dry-run, ...)
NGC_ROUTE_B_HARDCODING = [
    ('route_a', 'route_a', ["ddo_actual_initial_source_preparation_v007.py"],
     'Route-A preparation = DDO prep V007: galaxies["DDO154"] profile, 12-row DDO roster, DDO H2/stars.',
     'NGC prep v001 c54c7cc9 (reviewed PASS_SCOPED_CONDITIONAL_SOLVER): galaxies["NGC3198"], 43-row manifest roster, '
     'HI sigma0=11 km/s and Gamma=5/3 (prep line 113), H2 = 10 detected centres + constant core + matched exponential tail '
     '(Rd=1.806 kpc from the pinned tail reduction) at the stellar sech^2 height (counted proxy), analytic stellar rings; '
     'profile geometry 13.8 Mpc / 72 deg.', 'SUPPLIED_FROM_REVIEWED_CODE'),
    ('route_a', 'route_a', ["ddo_composite_stable_cached_binding_v002.py", "'stable_adapter'", "owned_scalar_lapse_inverse_cache_v001.py"],
     'Route-A binding = DDO stable-cached V002: stable lapse HI facade, stable line v002, HI v003, scalar lapse inverse cache, '
     'and the c2v003 checkpoint caller contract (physical_parameters, numerical_controls); observation 66/64 deg.',
     'NGC binding v001 9e9caf83 + worker v001 1b95a4ff exist (72/73 deg, 43 rows) but are clones of the PRE-stable DDO '
     'composite binding/worker v001: no stable HI/line/cache modules and no c2v003 caller contract. They cannot open any '
     'existing checkpoint (see caller_contract_check). The same defect failed DDO154_STABLE_CACHED_COUPLED_RUN_V001.',
     'BLOCKER_NO_REVIEWED_NGC_SUCCESSOR'),
    ('route_a', None, ['DDO154_STABLE_CACHED_COUPLED_TRIAL_SEED_V002.json'],
     'Base seed = DDO seed V002 (694eaaaa): numerical controls + DDO-selected Eref/ell_F/gamma.',
     'No NGC seed exists. c2v002 composes a CANDIDATE seed: DDO V002 numerical controls unchanged, call-spec Eref/ell_F/gamma/s, '
     'call-spec composite grid, call-spec h2_tail_mass_rtol (worker requires it explicitly; no reviewed value exists).',
     'CANDIDATE_COMPOSED_REQUIRES_ROOT_SELECTION'),
    ('reference', 'reference', ["['galaxies']['DDO154']", "'iteration_0004'", "start['iteration']!=4"],
     'Homotopy reference reads galaxies["DDO154"] inline and accepts only route-A iteration 4.',
     'None. Needs a reviewed successor reading galaxies["NGC3198"] (the same profile file holds it) and the converged iteration.',
     'BLOCKER_NO_REVIEWED_NGC_SUCCESSOR'),
    ('reference', 'reference_module', ['sigma=11000.;gamma=5/3', 'range(16)'],
     'Reference module: HI sigma0=11 km/s, Gamma=5/3, 16 angles inline.',
     'Same adopted values as NGC prep v001 (11 km/s, 5/3); 16 angles are numerics. Not galaxy-specific.',
     'COMPATIBLE_SAME_ADOPTED_VALUES'),
    ('body', 'body', ["DDO154_MONOTONE_SOURCE_RECONSTRUCTION_RUN_V001/source.json", "['galaxies']['DDO154']", 'len(R)!=72', '(72,16,8)'],
     'Body: DDO monotone source, galaxies["DDO154"], exactly 72 radii, shape (72,16,8) inline.',
     'None. No NGC monotone-source reconstruction exists; the NGC HI radial roster is 51 annuli x GL order (204 at order 4), not 72.',
     'BLOCKER_NO_REVIEWED_NGC_SUCCESSOR'),
    ('offset', 'offset', ["['galaxies']['DDO154']", 'reshape((72,16,8,10))', '(72,16,8)'],
     'Offset: galaxies["DDO154"] radial domain and (72,16,8) reshapes inline.', 'None.', 'BLOCKER_NO_REVIEWED_NGC_SUCCESSOR'),
    ('fs/rfs/le columns', 'columns_v005', ['0<=i<72', 'iteration_0004'],
     'Column stages v001/v003/v005: radial index range 0..71 inline; iteration 4.', 'None.', 'BLOCKER_NO_REVIEWED_NGC_SUCCESSOR'),
    ('fs/le rotation', 'rotation_v005', ["DDO154_MONOTONE_SOURCE_RECONSTRUCTION_RUN_V001/source.json", 'set(range(72))', '(72,16,nz,10)'],
     'Rotation v001/v005: DDO monotone source pin, complete-72 roster inline.', 'None.', 'BLOCKER_NO_REVIEWED_NGC_SUCCESSOR'),
    ('fs/le feedback', 'feedback_v004', ['(72,16,32)', 'radius.shape!=(72,)'],
     'Native feedback v002/v004: complete 72x16x32 measure inline.', 'None.', 'BLOCKER_NO_REVIEWED_NGC_SUCCESSOR'),
    ('column mean', 'column_mean_v004', ['DDO154_COLUMN_MEAN_REFERENCE_BINDING_V001.json', 'R.shape!=(72,)', 'list(range(72))'],
     'Column mean V004: DDO 12-row binding (4.04 Mpc radii, sin66/sin64) and 72 columns inline.',
     'None. No NGC 43-row column-mean binding exists (the 43 radii and 72/73 deg exist only in the route-A binding).',
     'BLOCKER_NO_REVIEWED_NGC_SUCCESSOR'),
    ('brackets', None, ['DDO154_REMAINING_FREE_SURFACE_CONTROLS_V001.json', '302500000.0'],
     'Column solver template and FS absolute enthalpy brackets [1.5125e8, 3.025e8] m^2/s^2 are DDO values.',
     'None. NGC column enthalpy scale is unknown until an NGC route-A fixed point exists.', 'BLOCKER_NO_NGC_VALUES'),
    ('entropy', None, ['64 / 121'],
     'Entropy K factor 64/121 was selected on the DDO chain.', 'None (route-B only).', 'NOT_APPLICABLE_ROUTE_B_BLOCKED'),
    ('geometry', None, ["'distance_Mpc': 4.04", "'inclination_deg': 66.0"],
     'Registered geometry 4.04 Mpc / 66 deg (released 64).',
     'Profile NGC3198 geometry 13.8 Mpc / 72 deg (stellar face-on factor 1.0) and NGC binding v001 72/73 deg projection.',
     'SUPPLIED_FROM_REVIEWED_CODE'),
    ('queries', None, ["'n_queries': 12"],
     'Output = 12 DDO rows from the column-mean binding.',
     'Output = 43 rows NGC3198-Q01..Q43 in manifest order from route A (prediction v005 rows); route-B rows unavailable.',
     'SUPPLIED_ROUTE_A_ONLY'),
]


def normalize_k_domain(kd):
    _strict(kd, ('length_kpc', 'scope'), 'k_domain')
    return {'length_kpc': _num(kd.get('length_kpc'), 'k_domain.length_kpc')}


def _base_seed_grid(g):
    path, sha = g['base_seed']
    raw = Path(path).read_bytes()
    if sha256_bytes(raw) != sha:
        raise Refusal('base seed pin mismatch')
    return json.loads(raw)['numerical_inputs']['composite_grid_spec']


def _grid_axis(grid):
    import numpy as np
    parts = []
    for lo, hi, n in zip(grid['breaks_inverse_kpc'][:-1], grid['breaks_inverse_kpc'][1:], grid['panel_orders']):
        x, _ = np.polynomial.legendre.leggauss(n)
        parts.append((lo + hi) / 2 + (hi - lo) * x / 2)
    return np.concatenate(parts)


def k_domain_report(grid, length_kpc, refuse=False):
    """k-domain coverage of a composite Gauss grid for a real-space extent L (kpc).
    CHECK (refusable): the smallest positive axis node k_min must satisfy k_min <= 2*pi/L.
    DIAGNOSTIC only (no acceptance threshold, no accuracy certificate): per positive panel,
    the phase L*dk swept across the panel and that phase per node, i.e. how many radians of
    exp(i k x) at |x| = L each Gauss node must carry."""
    import numpy as np
    ax = _grid_axis(grid)
    pos = np.sort(ax[ax > 0])
    need = 2 * math.pi / length_kpc
    ok = bool(len(pos) and pos[0] <= need)
    panels = []
    br, po = grid['breaks_inverse_kpc'], grid['panel_orders']
    for lo, hi, n in zip(br[:-1], br[1:], po):
        if lo < 0:
            continue
        x, _ = np.polynomial.legendre.leggauss(n)
        nodes = (lo + hi) / 2 + (hi - lo) * x / 2
        panels.append({'panel_inverse_kpc': [lo, hi], 'order': n, 'max_node_spacing_inverse_kpc': float(np.max(np.diff(nodes))) if n > 1 else None,
                       'phase_across_panel_rad_at_L': length_kpc * (hi - lo), 'phase_per_node_rad_at_L': length_kpc * (hi - lo) / n})
    rep = {'length_kpc': length_kpc, 'required_kmin_inverse_kpc': need, 'grid_kmin_node_inverse_kpc': float(pos[0]) if len(pos) else None,
           'grid_kmax_inverse_kpc': float(br[-1]), 'nodes_per_axis': int(sum(po)), 'positive_nodes_below_required_kmin': int(np.sum(pos <= need)),
           'kmin_covered': ok, 'positive_panels_DIAGNOSTIC': panels,
           'scope': 'kmin check only; per-panel phase is a DIAGNOSTIC with no accuracy threshold (nonperiodic Gauss cube, '
                    'no cutoff/quadrature error certificate)'}
    if refuse and not ok:
        raise Refusal('k-domain: smallest positive grid node %.6g/kpc exceeds 2pi/L = %.6g/kpc for L = %.6g kpc'
                      % (rep['grid_kmin_node_inverse_kpc'], need, length_kpc))
    return rep


def normalize_ngc_spec(spec):
    _strict(spec, ('schema', 'galaxy', 'label', 'physical', 'coefficients', 'numerics'), 'spec')
    if spec.get('galaxy') != 'NGC3198':
        raise Refusal('schema %s is the NGC3198 configuration only' % NGC_SCHEMA)
    g = GALAXIES['NGC3198']
    phys = spec.get('physical', {})
    _strict(phys, ('Eref_J', 'ell_F_m', 'gamma', 'common_scale_s', 'distance_Mpc', 'inclination_deg'), 'physical')
    geo = g['registered_geometry']
    p = {'Eref_J': _num(phys.get('Eref_J'), 'Eref_J'), 'ell_F_m': _num(phys.get('ell_F_m'), 'ell_F_m'),
         'gamma': _num(phys.get('gamma'), 'gamma'),
         'common_scale_s': _num(phys.get('common_scale_s', 1.0), 'common_scale_s'),
         'distance_Mpc': _num(phys.get('distance_Mpc', geo['distance_Mpc']), 'distance_Mpc'),
         'inclination_deg': _num(phys.get('inclination_deg', geo['inclination_deg']), 'inclination_deg')}
    if p['distance_Mpc'] != geo['distance_Mpc'] or p['inclination_deg'] != geo['inclination_deg']:
        raise Refusal('UNSUPPORTED NGC geometry: only the profile reference 13.8 Mpc / 72 deg is supported. The source radii '
                      'and stellar face-on factor are baked into GALAXY_RADIAL_SOURCE_REFERENCE_V001 (NGC3198 geometry) and '
                      'NGC binding v001 hard-codes the 72/73 deg projection; no reviewed code rescales either.')
    coeff = spec.get('coefficients', None) or {'path': str(g['default_coefficients'][0]), 'sha256': g['default_coefficients'][1]}
    _strict(coeff, ('path', 'sha256'), 'coefficients')
    if (str(coeff.get('path')), coeff.get('sha256')) != (str(g['default_coefficients'][0]), g['default_coefficients'][1]):
        raise Refusal('NGC c2v002: only the default coefficient grid fe5a2f06 (hard-coded in NGC prep v001) is supported')
    num = spec.get('numerics', {})
    _strict(num, ('composite_grid_spec', 'k_domain', 'h2_tail_mass_rtol', 'truncation', 'uv_tail'), 'numerics')  # C2V010 (K16): + uv_tail
    tr = num.get('truncation', {'shape': 'cube'})
    _strict(tr, ('shape',), 'truncation')
    if tr.get('shape', 'cube') != 'cube':
        raise Refusal('NGC: route A has no truncation-mask hook; only cube is supported')
    grid = num.get('composite_grid_spec', None)
    if grid is not None:
        _strict(grid, ('version', 'breaks_inverse_kpc', 'panel_orders', 'total_axis_nodes', 'scope'), 'composite_grid_spec')
        br, po = grid.get('breaks_inverse_kpc'), grid.get('panel_orders')
        if not (isinstance(br, list) and isinstance(po, list) and len(br) == len(po) + 1 and len(po) >= 1):
            raise Refusal('composite_grid_spec breaks/panel_orders malformed')
        if any(type(n) is not int or n < 2 for n in po) or grid.get('total_axis_nodes') != sum(po):
            raise Refusal('panel orders must be ints >=2 summing to total_axis_nodes')
        if br[0] != -br[-1] or br[-1] <= 0 or any(b <= a for a, b in zip(br, br[1:])):
            raise Refusal('breaks must strictly partition [-kmax,kmax]')
        # NGC prep v001 guards, checked early (the prep re-checks them itself)
        if sum(po) > NGC_PREP_MAX_AXIS_NODES or sum(po) % 2 or br != [-b for b in br[::-1]] or po != po[::-1]:
            raise Refusal('NGC prep v001 requires <=80 even axis nodes and reflection-symmetric breaks/orders')
    if num.get('k_domain') is None:
        raise Refusal('NGC: numerics.k_domain {length_kpc} is required (the 43 queries reach 44.08 kpc)')
    kd = normalize_k_domain(num['k_domain'])
    k_domain_report(grid if grid is not None else _base_seed_grid({'base_seed': NGC_DATA['parameter_seed']}), kd['length_kpc'], refuse=True)
    tol = num.get('h2_tail_mass_rtol')
    if isinstance(tol, bool) or not isinstance(tol, (int, float)) or not math.isfinite(float(tol)) or tol <= 0:
        raise Refusal('NGC: numerics.h2_tail_mass_rtol (positive finite) is required by the reviewed worker; no reviewed value exists')
    return {'schema': NGC_SCHEMA, 'config': 'NGC3198_C2V002', 'galaxy': 'NGC3198', 'label': spec.get('label', ''), 'physical': p,
            'coefficients': {'path': str(coeff['path']), 'sha256': coeff['sha256']},
            'numerics': dict({'composite_grid_spec': grid, 'k_domain': kd, 'h2_tail_mass_rtol': float(tol), 'truncation': {'shape': 'cube'}},
                             **({'uv_tail': normalize_uv_tail(num['uv_tail'], ngc=True)} if 'uv_tail' in num else {}))}  # C2V010 (K16); r4: nodes refused


def ngc_seed(nspec):
    """Candidate per-call NGC worker seed: DDO seed V002 numerical controls carried unchanged,
    plus the call's Eref/gamma (times s), ell_F, composite grid and h2_tail_mass_rtol.  Checked
    against the NGC prep v001 signature (exact keyword set).  Not root-selected."""
    import inspect
    path, sha = NGC_DATA['parameter_seed']
    raw = Path(path).read_bytes()
    if sha256_bytes(raw) != sha:
        raise Refusal('parameter seed pin mismatch')
    base = json.loads(raw)
    ni = json.loads(json.dumps(base['numerical_inputs']))
    p, s = nspec['physical'], nspec['physical']['common_scale_s']
    grid = nspec['numerics']['composite_grid_spec']
    set_fields = {'Eref_J': s * p['Eref_J'], 'gamma': s * p['gamma'], 'ell_F_m': p['ell_F_m'],
                  'h2_tail_mass_rtol': nspec['numerics']['h2_tail_mass_rtol']}
    if grid is not None:
        set_fields.update(composite_grid_spec=grid, kmax_inverse_kpc=float(grid['breaks_inverse_kpc'][-1]),
                          fourier_points_per_axis=int(grid['total_axis_nodes']))
    provenance = {}
    for k in sorted(set(ni) | set(set_fields)):
        if k in set_fields:
            old = ni.get(k)
            ni[k] = set_fields[k]
            provenance[k] = 'CALL_SPEC' + ('' if canonical(old) != canonical(ni[k]) else ' (equal to DDO seed V002 value)')
        else:
            provenance[k] = 'CARRIED_FROM_DDO_SEED_V002 (numerical control; not NGC-reviewed)'
    if ni['kpc_m'] != KPC_M:
        raise Refusal('seed kpc_m differs from driver constant')
    prep = exec_verified(NGC_CODE['prep'][0], NGC_CODE['prep'][1], 'c2v002_ngc_prep_sig')
    params = set(inspect.signature(prep.prepare_inputs).parameters)
    if set(ni) != params:
        raise Refusal('candidate seed keys differ from NGC prep v001 signature: missing %s extra %s'
                      % (sorted(params - set(ni)), sorted(set(ni) - params)))
    if ni.get('analytic_initial_azimuth') is not True or ni.get('composite_grid_spec') is None:
        raise Refusal('NGC binding v001 requires analytic_initial_azimuth True and a composite grid')
    pins = {str(NGC_DATA[k][0]): NGC_DATA[k][1] for k in ('manifest', 'profile', 'h2_tail_reduction', 'h2_source', 'parameter_seed')}
    seed = {'status': 'C2V002_CANDIDATE_NGC3198_TARGET_FREE_SEED_NOT_ROOT_SELECTED',
            'numerical_inputs': ni,
            'physical': {'Eref_J': ni['Eref_J'], 'ell_F_m': ni['ell_F_m'], 'gamma': ni['gamma'], 'common_scale_s': s,
                         'distance_Mpc': p['distance_Mpc'], 'inclination_deg': p['inclination_deg'],
                         'released_inclination_deg': GALAXIES['NGC3198']['registered_geometry']['released_inclination_deg']},
            'pins': pins,
            'parameter_provenance': provenance,
            'parent_seed': {'path': str(path), 'sha256': sha, 'scale_seed': base.get('scale_seed')},
            'scope': 'Target-free NGC43 provisional circular trial seed. Physical point = DDO seed parameters unless the call '
                     'spec says otherwise; numerical controls carried from DDO seed V002 are DDO-selected, not NGC-reviewed. '
                     'No velocity read; not calibration.'}
    return seed


def ngc_static_pins(nspec):
    pins = {}
    for table in (NGC_CODE, NGC_DATA, NGC_EVIDENCE):
        for key, (path, sha) in table.items():
            pins[str(path)] = verify_pin(path, sha, 'NGC ' + key)
    for key in ('solver', 'checkpoint_module'):
        pins[str(AUX[key][0])] = verify_pin(AUX[key][0], AUX[key][1], key)
    pins[nspec['coefficients']['path']] = verify_pin(nspec['coefficients']['path'], nspec['coefficients']['sha256'], 'coefficients')
    # reviews name exactly these code pins
    rw = json.loads(Path(NGC_DATA['review_worker'][0]).read_text())
    rb = json.loads(Path(NGC_DATA['review_binding'][0]).read_text())
    rb_pins = {x['path']: x['sha256'] for x in rb['sources']}
    review = {'worker_review_verdict': rw['verdict'], 'worker_review_sha_matches': rw['sha256'] == NGC_CODE['worker'][1],
              'binding_review_verdict': rb['verdict'],
              'binding_review_pins_match': all(rb_pins.get(str(NGC_CODE[k][0])) == NGC_CODE[k][1] for k in ('prep', 'binding'))
              and rb_pins.get(str(NGC_DATA['manifest'][0])) == NGC_DATA['manifest'][1]
              and rb_pins.get(str(NGC_DATA['h2_tail_reduction'][0])) == NGC_DATA['h2_tail_reduction'][1],
              'blocking_corrections': rw['blocking_corrections'] + rb['blocking_corrections']}
    w = exec_verified(NGC_CODE['worker'][0], NGC_CODE['worker'][1], 'c2v002_ngc_worker_local')
    local = {k: (str(pth), s) for k, (pth, s) in w.LOCAL.items()}
    review['worker_LOCAL_equals_config'] = all(local.get(k) == (str(NGC_CODE[k][0]), NGC_CODE[k][1]) for k in local) and \
        set(local) == {'prep', 'binding', 'composite', 'stream', 'base', 'prediction'}
    return pins, review


_VELOCITY_KEY_HINTS = ('velocit', 'vobs', 'v_obs', 'vrot', 'v_rot', 'vgas', 'vdisk', 'vbul', 'errv', 'vflat')


def _key_scan(obj, prefix='', hits=None):
    """Key NAMES only (never values) that look like velocity fields."""
    hits = [] if hits is None else hits
    if isinstance(obj, dict):
        for k, v in obj.items():
            kl = str(k).lower()
            if any(h in kl for h in _VELOCITY_KEY_HINTS):
                hits.append(prefix + '/' + str(k))
            _key_scan(v, prefix + '/' + str(k), hits)
    elif isinstance(obj, list):
        for v in obj[:3]:
            _key_scan(v, prefix + '/[]', hits)
    return hits


def ngc_sources_summary():
    """Load the NGC source JSONs (source-only files; no target velocity file is opened) and
    return headers and counts.  The rotmod .dat named in the manifest provenance is NOT opened."""
    out = {}
    load = {k: json.loads(Path(NGC_DATA[k][0]).read_bytes()) for k in
            ('profile', 'manifest', 'h2_source', 'physical_source_state_binding', 'stellar_photometry_nodes', 'source_only_bundle')}
    tail = json.loads(Path(NGC_DATA['h2_tail_reduction'][0]).read_bytes())
    prof = load['profile']['galaxies']['NGC3198']
    gas, st = prof['HI_plus_He'], prof['stellar_reference']
    out['profile_NGC3198'] = {'geometry': prof['geometry'], 'HI_annuli': len(gas['annular_means_Msun_pc2']),
                              'HI_s_edges': len(gas['s_edges_kpc2']), 'HI_support_radius_kpc': gas['support_radius_kpc'],
                              'HI_integrated_mass_Msun': gas['integrated_mass_Msun'], 'HI_helium': gas['helium'],
                              'stellar_nodes': st['node_count'], 'stellar_last_radius_kpc': float(st['radius_kpc'][-1]),
                              'stellar_height_kpc': st['height_kpc'], 'stellar_outer_scale_kpc': st['outer_scale_kpc']}
    m = load['manifest']
    out['manifest'] = {'n_rows': len(m['rows']), 'query_ids': [r['query_id'] for r in m['rows']],
                       'Rad_text': [r['Rad_text'] for r in m['rows']], 'units': sorted({r['Rad_unit'] for r in m['rows']}),
                       'emitted_columns': m['emitted_columns'], 'no_other_columns_emitted': m['no_other_columns_emitted'],
                       'reference_distance_Mpc_text': m['reference_distance']['rotmod_header']['value_text'],
                       'not_included': m['not_included'],
                       'ids_are_Q01_Q43_in_order': [r['query_id'] for r in m['rows']] == ['NGC3198-Q%02d' % i for i in range(1, 44)]}
    src_ok = Path(tail['source']['path']) == Path(NGC_DATA['h2_source'][0]) and tail['source']['sha256'] == NGC_DATA['h2_source'][1]
    rows = load['h2_source']['S1_alternative_and_stellar_median_rows']['rows'][:10]
    out['h2'] = {'tail_source_pin_matches_config': src_ok, 'outer_scale_kpc': tail['outer_scale_kpc'], 'tail_rule': tail['tail'],
                 'detected_centres_used': len(rows),
                 'radius_literals_kpc': [r['radius_kpc_literal']['value'] for r in rows],
                 'helium_already_included': all(r['conventions']['gas_helium']['value'] == 'ALREADY_INCLUDED' for r in rows)}
    for k in ('physical_source_state_binding', 'stellar_photometry_nodes', 'source_only_bundle', 'h2_source'):
        o = load[k]
        out.setdefault('headers', {})[k] = {'schema': o.get('schema'), 'status': o.get('status'), 'top_keys': sorted(o)[:20]}
    out['velocity_like_key_names'] = {k: _key_scan(v) for k, v in load.items()}
    out['not_opened'] = [m['source']['path']]
    return out


def ngc_prep_local_modules():
    """Modules NGC prep v001 loads by path INSIDE prepare_inputs (not module-global pins): it records
    their sha at load and the composite adapter re-verifies that record from bytes; neither checks
    them against a reviewed list.  Reported here with sha from bytes and a scipy scan."""
    import re
    text = Path(NGC_CODE['prep'][0]).read_text()
    prep = exec_verified(NGC_CODE['prep'][0], NGC_CODE['prep'][1], 'c2v002_ngc_prep_locals')
    base = {'HERE': prep.HERE, 'HC': prep.HC, 'HP': prep.HP}
    paths = [base[a] / b for a, b in re.findall(r"\b(HERE|HC|HP)/'([^']+\.py)'", text)] + [prep.KERNEL]
    pat = re.compile(r'^\s*(import\s+scipy|from\s+scipy)', re.M)
    out = []
    for pth in dict.fromkeys(paths):
        ok = Path(pth).is_file()
        out.append({'path': str(pth), 'exists': ok, 'sha256': sha256_file(pth) if ok else None,
                    'scipy_import': bool(ok and pat.search(Path(pth).read_text()))})
    return out


def ngc_caller_contract_check():
    """Deciding evidence for the route-A blocker, using only inert definitions of the real modules
    and a synthetic caller dict (no solver, no checkpoint directory, no project data)."""
    import inspect
    res = {}
    texts = {k: Path(NGC_CODE[k][0]).read_bytes() for k in ('worker', 'binding', 'composite')}
    res['physical_parameters_or_numerical_controls_written_by'] = {
        k: (b'physical_parameters' in t or b'numerical_controls' in t) for k, t in texts.items()}
    res['ddo_stable_binding_v002_writes_them'] = b"identity['physical_parameters']" in Path(NGC_EVIDENCE['ddo_stable_binding_v002'][0]).read_bytes()
    # caller identity keys exactly as the NGC worker builds them, plus binding/adapter additions
    w = texts['worker'].decode()
    built = all(s in w for s in ("caller_identity=dict(", "seed={'path'", "code_pins=pins", "worker={'path'", "boundary_prescription="))
    caller = {'seed': {'path': 'SYNTHETIC', 'sha256': '0' * 64}, 'code_pins': {'/synthetic.py': '0' * 64},
              'worker': {'path': 'SYNTHETIC', 'sha256': '0' * 64}, 'boundary_prescription': 'synthetic',
              'composite_full_driver': {}, 'composite_source_binding': {}}
    cm = exec_verified(AUX['checkpoint_module'][0], AUX['checkpoint_module'][1], 'c2v002_ngc_ckpt_c2v003')
    try:
        cm._identity(solver_file=str(AUX['solver'][0]), inputs={}, caller=caller, fixed=None)
        verdict = 'NO_ERROR (unexpected)'
    except Exception as exc:
        verdict = '%s: %s' % (type(exc).__name__, exc)
    res['c2v003_identity_on_ngc_caller_keys'] = {'worker_builds_these_keys': built, 'caller_keys': sorted(caller), 'result': verdict}
    for k in ('checkpoint_c2v001', 'checkpoint_c2v002'):
        m = exec_verified(NGC_EVIDENCE[k][0], NGC_EVIDENCE[k][1], 'c2v002_ngc_' + k)
        res[k + '_FIXED_SOURCE_SELECTION_IDENTITY'] = getattr(m, 'FIXED_SOURCE_SELECTION_IDENTITY', None)
    s = exec_verified(NGC_EVIDENCE['solver_nonfixedsrc'][0], NGC_EVIDENCE['solver_nonfixedsrc'][1], 'c2v002_ngc_solver_nf')
    res['nonfixedsrc_solver_accepts_fixed_source_fourier_J'] = 'fixed_source_fourier_J' in inspect.signature(s.solve).parameters
    res['adapter_always_passes_fixed_source_fourier_J'] = b"fixed_source_fourier_J=prepared['fixed_source_fourier_J']" in texts['composite']
    prec = json.loads(Path(NGC_EVIDENCE['ddo_precedent_failure'][0]).read_text())
    res['precedent'] = {'run': str(NGC_EVIDENCE['ddo_precedent_failure'][0]), 'type': prec['type'], 'message': prec['message'],
                        'elapsed_seconds': prec['elapsed_seconds'],
                        'note': 'DDO stable-cached binding v001 lacked the same contract; v002 added it and then ran (RUN_V002)'}
    blocked = (verdict.startswith('CheckpointError') and 'physical_parameters' in verdict
               and not any(res['physical_parameters_or_numerical_controls_written_by'].values())
               and res['checkpoint_c2v001_FIXED_SOURCE_SELECTION_IDENTITY'] is not True
               and res['checkpoint_c2v002_FIXED_SOURCE_SELECTION_IDENTITY'] is not True
               and not res['nonfixedsrc_solver_accepts_fixed_source_fourier_J'] and res['adapter_always_passes_fixed_source_fourier_J'])
    res['verdict'] = ('ROUTE_A_BLOCKED: every existing solver/checkpoint pairing fails before any column work '
                      '(fixedsrc+c2v003: caller contract; fixedsrc+c2v001/2: no fixed-source identity; '
                      'non-fixedsrc solver: no fixed_source_fourier_J parameter)') if blocked else 'NOT_DEMONSTRATED'
    res['blocked'] = blocked
    return res


def ngc_route_b_table(admission=None):
    """c2v004: rows of the five generalized stages locate the DDO literals in the reviewed BASE file (the
    successor reads them from the galaxy config) and carry the successor's own NGC admission result."""
    rows = []
    driver_text = Path(__file__).read_text()
    adm = {a['stage']: a for a in (admission or {}).get('stages', [])}
    for stage, key, needles, hard, ngc, status in NGC_ROUTE_B_HARDCODING:
        gen = GENERALIZED.get(key) if key else None
        if key is None:  # the driver's own DDO configuration (lines above the NGC section)
            path, text = Path(__file__), driver_text.split('# ' + '=' * 77 + ' NGC3198 (c2v002)')[0]
        else:
            path = gen['base'][0] if gen else (SCRIPTS.get(key) or AUX.get(key))[0]
            text = Path(path).read_text()
        lines = text.splitlines()
        loc = {n: [i + 1 for i, ln in enumerate(lines) if n in ln][:6] for n in needles}
        row = {'stage': stage, 'file': str(path), 'needle_lines': loc, 'ddo_hard_coding': hard,
               'ngc_equivalent': ngc, 'status': status, 'key_is_driver': key is None}
        if gen:
            row['generalized_successor'] = {'path': str(SCRIPTS[key][0]), 'sha256': SCRIPTS[key][1]}
            row['successor_admission_ngc'] = adm[key]['admission'] if key in adm else 'NOT_PROBED'
            row['status'] = ('C2V005_SUCCESSOR_ADMITS_NGC' if isinstance(row['successor_admission_ngc'], dict) and row['successor_admission_ngc'].get('accepted')
                             else 'C2V005_SUCCESSOR_REFUSES_NGC_IN_THIS_ROUTE_A_CONFIG (route-B call: see the c2v005 route-B dry run)')
        rows.append(row)
    return rows


NGC_PLAN_KIND = {'reference': 'reference', 'body': 'body', 'offset': 'offset', 'fs_columns': 'columns_v001', 'fs_rotation': 'rotation_v001',
                 'fs_feedback': 'feedback_v002', 'rfs_columns': 'columns_v003', 'le_columns': 'columns_v005', 'le_rotation': 'rotation_v005',
                 'le_feedback': 'feedback_v004', 'le_column_mean': 'column_mean_v004'}
NGC_NOT_GENERALIZED = {}  # c2v005: every route-B stage has a gal_c2v003 successor


def ngc_route_b_admission(inputs_dir, writer):
    """c2v004: write each generalized successor's config for NGC3198 (galaxy-config values; the per-call
    fields hold the NGC galaxy-config value NONE_IN_REVIEWED_CODE because no NGC route A exists) and run the
    successor's OWN admission function on it.  Nothing is executed beyond inert module definitions."""
    gc = load_galaxy_config('NGC3198')
    out = []
    for kind in GENERALIZED:
        obj, _ = stage_config_object(kind, gc, {}, omit_missing_per_call=False)
        p, s = writer(Path(inputs_dir) / ('galaxy_config_%s_ngc3198_probe.json' % kind), obj)
        out.append({'stage': kind, 'script': {'path': str(SCRIPTS[kind][0]), 'sha256': SCRIPTS[kind][1]},
                    'config': {'path': str(p), 'sha256': s, 'format': GENERALIZED[kind]['format']},
                    'galaxy_config_argv': galaxy_config_argv(kind, p, s), 'admission': probe_stage_admission(kind, p, s)})
    return {'galaxy_config': {'path': gc['path'], 'sha256': gc['sha256']}, 'stages': out}


def ngc_stage_plan(seed_path, seed_sha, stages_dir, admission=None, uvt=None):
    d = Path(stages_dir) / '01_route_a_ngc43'
    script, sha = NGC_CODE['worker']
    if uvt is not None:  # C2V010 (K16): tail ON plans the v002-lineage RO1 uvtail NGC worker, never NGC_CODE v001
        script, sha = NGC_CODE_UVT['worker']
    argv = ['--seed', str(seed_path), '--seed-sha256', seed_sha, '--solver', str(AUX['solver'][0]), '--solver-sha256', AUX['solver'][1],
            '--checkpoint-module', str(AUX['checkpoint_module'][0]), '--checkpoint-module-sha256', AUX['checkpoint_module'][1],
            '--outdir', str(d / 'attempt_000'), '--checkpoint-directory', str(d / 'checkpoint'), '--start-iteration', '0']
    if uvt is not None:  # C2V010 (K16): the uvtail solver and the tail argv (request not composed here: NGC route A is the NGC lane's)
        argv[argv.index('--solver') + 1] = str(AUX_UVT['solver'][0])
        argv[argv.index('--solver-sha256') + 1] = AUX_UVT['solver'][1]
        argv += ['--uv-tail-config', 'PENDING_NGC_UV_TAIL_REQUEST(route-A request composed by the NGC route-A lane)',
                 '--uv-tail-config-sha256', 'PENDING_NGC_UV_TAIL_REQUEST_SHA256', '--eps-certificate', 'PENDING', '--eps-certificate-sha256',
                 'PENDING', '--lo-certificate', 'PENDING', '--lo-certificate-sha256', 'PENDING', '--uv-tail-sidecar-directory', str(d / 'uv_tail_sidecar')]
    plan = [{'name': 'route_a_ngc43', 'kind': 'route_a_ngc43', 'script': str(script), 'script_sha256': sha, 'argv': argv,
             'command': [PY, '-I', '-B', str(script)] + argv, 'executed': False,
             'status': 'PLANNED_BLOCKED (see caller_contract_check)',
             'cost_estimate': 'ESTIMATE_NOT_MEASURED: DDO route A = 1594 s for 72x8 = 576 gas columns, 12 queries; NGC has up to '
                              '51x4x8 = 1632 gas columns and 43 queries, so roughly 1.3-1.5 h serial if column work dominates'}]
    if uvt is not None:  # C2V010 (K16): the declared plan difference
        plan[0]['ngc_code_lineage_swap'] = {
            'from': {k: [str(p), s] for k, (p, s) in NGC_CODE.items() if k in ('worker', 'binding')},
            'to': {k: [str(p), s] for k, (p, s) in NGC_CODE_UVT.items()},
            'evidence': [str(NGC_CODE_UVT['lineage_evidence'][0]), NGC_CODE_UVT['lineage_evidence'][1]],
            'uv_tail_config_sha256': uvt_info(uvt)['config_sha256'],
            'status': 'PLANNED_ONLY: tail-ON NGC route A runs on the v002-lineage code of the live NGC route-A packet; this '
                      'configuration plans and never launches it; NGC route B with the tail is not bound (DDO154 only)'}
    adm = {a['stage']: a for a in ((admission or {}).get('stages') or [])}
    for name in ('reference', 'body', 'offset', 'fs_columns', 'fs_rotation', 'fs_feedback', 'rfs_columns',
                 'le_columns', 'le_rotation', 'le_feedback', 'le_column_mean'):
        kind = NGC_PLAN_KIND.get(name)
        if kind and kind in adm:
            a = adm[kind]
            res = a['admission']
            plan.append({'name': name, 'kind': kind, 'executed': False, 'script': a['script']['path'], 'script_sha256': a['script']['sha256'],
                         'galaxy_config': a['config'], 'galaxy_config_argv': a['galaxy_config_argv'],
                         'status': ('ADMITTED (unexpected for NGC3198)' if res['accepted'] else
                                    'REFUSED_AT_ADMISSION_BY_SUCCESSOR_CODE: ' + res['refusal'])})
        elif kind:
            plan.append({'name': name, 'kind': kind, 'executed': False, 'status': 'NOT_PROBED'})
        else:
            plan.append({'name': name, 'kind': name, 'executed': False,
                         'status': 'BLOCKED_NOT_GENERALIZED: ' + NGC_NOT_GENERALIZED[name]})
    return plan


def ngc_remaining_refusals(contract, admission, hard):
    """c2v004: every refusal that stands between the NGC3198 seed call and 43 route-B rows, from bytes."""
    out = [{'where': 'route_a', 'refusal': contract['verdict'], 'source': 'ngc_caller_contract_check (real modules, synthetic caller)'}]
    for name, why in NGC_NOT_GENERALIZED.items():
        out.append({'where': name, 'refusal': 'NOT_GENERALIZED: ' + why, 'source': 'route_b_hardcoding'})
    for a in (admission or {}).get('stages', []):
        if not a['admission']['accepted']:
            out.append({'where': a['stage'], 'refusal': a['admission']['refusal'], 'source': 'successor admission function on '
                        + Path(a['config']['path']).name})
    for r in hard:
        if r['key_is_driver'] and r['status'].startswith('BLOCKER'):
            out.append({'where': 'driver ' + r['stage'], 'refusal': r['status'] + ': ' + r['ngc_equivalent'], 'source': 'route_b_hardcoding'})
    for b in binding_blockers():
        out.append({'where': 'binding', 'refusal': b, 'source': 'binding_blockers (applies to every galaxy)'})
    schema = json.loads(Path(GC_SCHEMA[0]).read_bytes())
    for s in schema.get('structural_findings', []):
        out.append({'where': 'structural ' + s['id'], 'refusal': s['title'], 'source': 'GALAXY_CONFIG_SCHEMA_V002 structural_findings (= V001)'})
    return out


def ngc_read_route_a_result(result_path, finish_path, manifest_path=None):
    """Read a (future) NGC43 route-A result: 43 speeds keyed NGC3198-Q01..Q43 in manifest order,
    validity, and DIAGNOSTIC m>=1 content of the azimuth-resolved trial (no acceptance threshold).
    Reads only the worker's own outputs and the target-free manifest."""
    import numpy as np
    manifest_path = manifest_path or NGC_DATA['manifest'][0]
    man = json.loads(Path(manifest_path).read_text())
    ids = [r['query_id'] for r in man['rows']]
    rad = {r['query_id']: r['Rad_text'] for r in man['rows']}
    reasons = []
    fin = json.loads(Path(finish_path).read_text())
    if fin.get('status') != 'RETURNED_ACTUAL_RESULT':
        reasons.append('worker status %s' % fin.get('status'))
    if sha256_file(result_path) != fin.get('result_sha256'):
        reasons.append('result sha256 differs from worker finish.json')
    ra = json.loads(Path(result_path).read_text())  # RO1 (A49.3): the whole result, for the ro1 record
    x = ra['result']['result']
    sfp = x.get('source_fixed_point') if isinstance(x.get('source_fixed_point'), dict) else {}
    ro1, ro1_fired = ro1_outcome(ra, x, result_path, sfp.get('converged_finite_fixed_point') is True
                                 and (sfp.get('checkpoint') or {}).get('outcome') == ROUTE_A_CONVERGED)
    if ro1_fired:  # RO1 (A49.3): converged fixed point, readout refused: rows None recorded (no TypeError), not valid
        reasons.append('RO1: route-A circular-trial readout refused after a converged fixed point (%s); no route-A rows'
                       % ro1['events'][0].get('refusal'))
        return {'rows': None, 'speeds_km_s': None, 'valid': False, 'reasons': reasons, 'ro1': ro1,
                'validity_definition': 'worker RETURNED_ACTUAL_RESULT, result sha matches, 43 manifest ids in order, finite speeds, '
                                       'converged source fixed point, predictions_available',
                'm_ge_1_diagnostics': None, 'dynamics_status': x.get('dynamics_status'), 'accepted_for_calibration': False,
                'route': 'ROUTE_A_ONLY (route B blocked)'}
    rows = x['rows']
    if [r['id'] for r in rows] != ids:
        reasons.append('row ids are not the 43 manifest ids in order')
    speeds = [r['speed_km_s'] for r in rows]
    if not all(isinstance(v, (int, float)) and math.isfinite(v) for v in speeds):
        reasons.append('nonfinite speed')
    if x.get('source_fixed_point', {}).get('converged_finite_fixed_point') is not True:
        reasons.append('route-A source fixed point not converged')
    if x.get('predictions_available') is not True:
        reasons.append('predictions_available is not True')
    per_q, gmax = [], {}
    for q in x.get('query_physics', []):
        nodes = q['nodes']
        n = len(nodes)
        phi = np.array([nd['phi_rad'] for nd in nodes])
        v = np.array([nd['v'] for nd in nodes], dtype=float)
        equal = bool(np.allclose(phi, 2 * np.pi * np.arange(n) / n, rtol=0, atol=1e-12))
        F = np.abs(np.fft.rfft(v))
        ratios = {'m%d' % m: (float(F[m] / F[0]) if F[0] > 0 else None) for m in range(1, len(F))}
        for k, val in ratios.items():
            if val is not None:
                gmax[k] = max(gmax.get(k, 0.0), val)
        eul = np.array([nd['Euler_covector_residual_R_phi_z'] for nd in nodes], dtype=float)
        cont = [abs(r) for nd in nodes for r in nd['mass_continuity']['fractional_density_rate_per_s']]
        per_q.append({'id': q['id'], 'n_azimuths': n, 'equal_angle_nodes': equal,
                      'speed_m_s_azimuth_harmonic_ratio': ratios,
                      'speed_m_s_azimuth_range': float(v.max() - v.min()),
                      'Euler_residual_abs_max_R_phi_z': [float(a) for a in np.max(np.abs(eul), axis=0)],
                      'continuity_fractional_rate_abs_max_per_s': float(max(cont)) if cont else None})
    valid = not reasons and len(rows) == 43
    return {'rows': [{'id': r['id'], 'Rad_text_kpc': rad.get(r['id']), 'speed_km_s': r['speed_km_s']} for r in rows],
            'speeds_km_s': {r['id']: r['speed_km_s'] for r in rows}, 'valid': valid, 'reasons': reasons,
            'validity_definition': 'worker RETURNED_ACTUAL_RESULT, result sha matches, 43 manifest ids in order, finite speeds, '
                                   'converged source fixed point, predictions_available',
            'm_ge_1_diagnostics': {'quantity': '|FFT_m(v)|/|FFT_0(v)| of the circular trial speed over the observation azimuths; '
                                               'max |Euler residual| (R,phi,z) and |continuity rate| per query',
                                   'global_max_harmonic_ratio': gmax, 'per_query': per_q, 'status': 'DIAGNOSTIC_ONLY'},
            'dynamics_status': x.get('dynamics_status'), 'accepted_for_calibration': False, 'route': 'ROUTE_A_ONLY (route B blocked)'}


def _ngc_collect(nspec, inputs_dir, writer):
    pins, review = ngc_static_pins(nspec)
    sources = ngc_sources_summary()
    seed = ngc_seed(nspec)
    seed_path, seed_sha = writer(Path(inputs_dir) / 'seed_ngc_c2v002.json', seed)
    grid = nspec['numerics']['composite_grid_spec'] or seed['numerical_inputs']['composite_grid_spec']
    kd = {'call_length_kpc': k_domain_report(grid, nspec['numerics']['k_domain']['length_kpc']),
          'queries_44_08_kpc': k_domain_report(grid, 44.08),
          'HI_support_%.2f_kpc' % sources['profile_NGC3198']['HI_support_radius_kpc']:
              k_domain_report(grid, sources['profile_NGC3198']['HI_support_radius_kpc'])}
    return pins, review, sources, seed, seed_path, seed_sha, kd


def _ngc_blockers(contract, admission=None):
    refused = [a['stage'] for a in (admission or {}).get('stages', []) if not a['admission']['accepted']]
    return ['NGC3198_ROUTE_A_BLOCKED: ' + contract['verdict'] + '. Needs a reviewed NGC successor of binding/worker v001 '
            '(the NGC analogue of ddo_composite_stable_cached_binding/root_worker_v002).',
            'NGC3198_ROUTE_B (c2v005): every route-B stage has a gal_c2v003 successor; route B is called with schema %s, galaxy '
            'NGC3198 and the route-A outputs of the NGC route-A lane; in this route-A seed configuration the successors %s refuse '
            '(per-call values do not exist here).' % (SCHEMA, refused)]


def ngc_run_blocked(out, nspec, spec_sha, result):
    def writer(p, obj):
        p.parent.mkdir(parents=True, exist_ok=True)
        return p, _write_x(p, obj)
    pins, review, sources, seed, seed_path, seed_sha, kd = _ngc_collect(nspec, out / 'inputs', writer)
    contract = ngc_caller_contract_check()
    admission = ngc_route_b_admission(out / 'inputs', writer)  # c2v004
    plan = ngc_stage_plan(seed_path, seed_sha, out / 'stages', admission, nspec['numerics'].get('uv_tail'))  # C2V010 (K16)
    _write_x(out / 'start.json', {'schema': NGC_RESULT_SCHEMA, 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
             'pid': os.getpid(), 'driver': str(Path(__file__).resolve()), 'driver_sha256': result['driver_sha256'],
             'call_spec_sha256': spec_sha, 'normalized_spec': nspec, 'static_pins': pins,
             'scope': 'NGC3198 configuration; no stage executed; no velocity read; no score or calibration admission.'})
    result.update(schema=NGC_RESULT_SCHEMA, galaxy='NGC3198', normalized_spec=nspec, executed_stages=0,
                  identity={'seed': {'path': str(seed_path), 'sha256': seed_sha, 'status': seed['status']}},
                  ngc={'review': review, 'sources': sources, 'k_domain': kd, 'caller_contract_check': contract,
                       'stage_plan': plan, 'route_b_hardcoding': ngc_route_b_table(admission), 'route_b_admission': admission,
                       'output_schema': 'ngc_read_route_a_result(): 43 rows NGC3198-Q01..Q43, valid, m_ge_1_diagnostics'})
    raise Blocked(' | '.join(_ngc_blockers(contract, admission)))


def ngc_dry_run(spec_path, raw, nspec, rd):
    rd = Path(rd).resolve()
    def writer(p, obj):
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.exists():
            raise Refusal('dry-run input exists: %s' % p)
        b = (json.dumps(_jsonable(obj), indent=1, allow_nan=False) + '\n').encode()
        p.write_bytes(b)
        return p, sha256_bytes(b)
    pins, review, sources, seed, seed_path, seed_sha, kd = _ngc_collect(nspec, rd / 'simulated_call' / 'inputs', writer)
    contract = ngc_caller_contract_check()
    admission = ngc_route_b_admission(rd / 'simulated_call' / 'inputs', writer)  # c2v004
    plan = ngc_stage_plan(seed_path, seed_sha, rd / 'simulated_call' / 'stages', admission, nspec['numerics'].get('uv_tail'))  # C2V010 (K16)
    locals_ = ngc_prep_local_modules()
    roots = [v for v in NGC_CODE.values()] + [AUX['solver'], AUX['checkpoint_module']] + \
        [(x['path'], x['sha256']) for x in locals_ if x['exists']]
    trans = transitive_pins_and_scipy(roots)
    hard = ngc_route_b_table(admission)
    remaining = ngc_remaining_refusals(contract, admission, hard)
    report = {'schema': 'UNT_GALAXY_M0_FORWARD_DRYRUN_NGC_C2V002', 'call_spec': str(spec_path), 'call_spec_sha256': sha256_bytes(raw),
              'driver_sha256': sha256_file(__file__), 'normalized_spec': nspec, 'executed_stages': 0,
              'static_pins': pins, 'review_custody': review, 'transitive_pins': trans, 'prep_local_modules': locals_,
              'coefficient_npz_headers': _npz_headers(nspec['coefficients']['path']), 'sources': sources,
              'seed': {'path': str(seed_path), 'sha256': seed_sha, 'status': seed['status'],
                       'parameter_provenance': seed['parameter_provenance']},
              'k_domain': kd, 'caller_contract_check': contract, 'stage_plan': plan, 'route_b_hardcoding': hard,
              'route_b_admission': admission, 'remaining_refusals': remaining, 'binding_blockers': binding_blockers(),
              'blockers': _ngc_blockers(contract, admission)}
    report['summary'] = {
        'executed_stages': 0, 'static_pins_verified': len(pins), 'transitive_files_verified': trans['verified_files'],
        'pin_problems': trans['problems'], 'scipy_imports': trans['scipy_imports'] + [x['path'] for x in locals_ if x['scipy_import']],
        'prep_local_modules_missing': [x['path'] for x in locals_ if not x['exists']],
        'reviews': [review['worker_review_verdict'], review['binding_review_verdict']],
        'review_pins_match': review['worker_review_sha_matches'] and review['binding_review_pins_match'] and review['worker_LOCAL_equals_config'],
        'manifest_ids_Q01_Q43_in_order': sources['manifest']['ids_are_Q01_Q43_in_order'],
        'velocity_like_key_names': {k: v for k, v in sources['velocity_like_key_names'].items() if v},
        'k_domain_kmin_covered': {k: v['kmin_covered'] for k, v in kd.items()},
        'route_a_blocked': contract['blocked'], 'route_b_blocked_rows': sum(1 for r in hard if r['status'].startswith('BLOCKER')),
        'seed_sha256': seed_sha,
        # c2v004
        'galaxy_config': admission['galaxy_config'],
        'generalized_successors_refusing_ngc': [a['stage'] for a in admission['stages'] if not a['admission']['accepted']],
        'generalized_successors_admitting_ngc': [a['stage'] for a in admission['stages'] if a['admission']['accepted']],
        'remaining_refusals': len(remaining)}
    lines = ['NGC3198 DRY-RUN PLAN %s  (spec %s)' % (nspec.get('label', ''), report['call_spec_sha256']), '',
             'seed (candidate, not root-selected): %s  sha256 %s' % (seed_path, seed_sha), '']
    for i, s in enumerate(plan, 1):
        lines.append('%02d %-16s %s' % (i, s['name'], s['status']))
        if s.get('galaxy_config'):  # c2v004
            lines.append('      successor %s  galaxy-config %s %s' % (Path(s['script']).name, Path(s['galaxy_config']['path']).name,
                                                                     s['galaxy_config']['sha256'][:16]))
        if s.get('command'):
            lines.append('      ' + ' '.join(str(a).replace(str(ROOT), '$ROOT').replace(str(rd), '$DRY') for a in s['command']))
            lines.append('      ' + s['cost_estimate'])
    lines += ['', 'caller contract: ' + contract['verdict'], '      c2v003 on NGC caller keys -> ' + contract['c2v003_identity_on_ngc_caller_keys']['result'],
              '      precedent: %s -> %s' % (contract['precedent']['run'].replace(str(ROOT), '$ROOT'), contract['precedent']['message']), '',
              'k-domain (kmin check; per-panel phase is diagnostic only):']
    for k, v in kd.items():
        lines.append('      %-28s L=%-8.4g need kmin<=%.4g/kpc  grid kmin=%.4g/kpc  covered=%s' % (
            k, v['length_kpc'], v['required_kmin_inverse_kpc'], v['grid_kmin_node_inverse_kpc'], v['kmin_covered']))
    lines += ['', 'remaining refusals (c2v004, from bytes):']
    for r in remaining:
        lines.append('      %-22s %s' % (r['where'], r['refusal']))
    lines += ['', 'route-B DDO hard-coding -> NGC equivalent:']
    for r in hard:
        lines.append('      %-18s %-40s %s' % (r['stage'], r['status'], {n: l for n, l in r['needle_lines'].items()}))
    with open(rd / 'DRYRUN_PLAN.txt', 'x') as f:
        f.write('\n'.join(lines) + '\n')
    _write_x(rd / 'DRYRUN_REPORT.json', report)
    print(json.dumps(_jsonable(report['summary']), indent=1))
    return 0


def main(argv=None):
    import argparse
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == '_stage':
        return stage_main(argv[1])
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    r = sub.add_parser('run')
    r.add_argument('--spec', required=True)
    r.add_argument('--outdir', required=True)
    dr = sub.add_parser('dry-run')
    dr.add_argument('--spec', required=True)
    dr.add_argument('--report-dir', required=True)
    a = ap.parse_args(argv)
    if a.cmd == 'run':
        return cmd_run(a.spec, a.outdir)
    return cmd_dry_run(a.spec, a.report_dir)



# NGC-only successor source. The original DDO call paths above remain unchanged.
V011_PINS={'prep': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/prep_loader_fix/ngc_actual_initial_source_preparation_cx3v011_cx3v005.py', '8681da84bbd2b6858f5334d724b4e22e10c191e68f305b6e29df841571bf712b'), 'prediction': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/route_a/ngc_coupled_fourier_hi_prediction_cx3v011.py', '7ae28901023974005fac9a5dc4126941371b1522837b02c81cdb5811573c1e98'), 'binding': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/route_a/ngc_composite_full_coupled_binding_uvtail_ro1_cx3v011.py', '9b5ce82adea46c8e660f44b0fc91e8dbe5d0616cc1de1fd4467878ef3b5c0668'), 'worker': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/prep_loader_fix/ngc43_coupled_root_worker_uvtail_ro1_cx3v011_r5cx3v001_cx3v005.py', 'ee27227c2cee3093589ae6b6546a0d88a1bbe20c47ba4dacff497ad7cc80189f'), 'worker_parallel': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/prep_loader_fix/ngc43_coupled_root_worker_parallel_uvtail_ro1_cx3v011_r5cx3v001_cx3v005.py', '293a417f493fee2b59176bc60873fa3cdea5e586f375efbe51cbd10651e045b1'), 'grid_cut': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_grid_cut_cx3v001_cx3v005.py', '5d037291c8d683d7921f38365640bf41502216a67a5ed6ca84986aa671faf353'), 'seed_v002': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_a_freeboundary_c2/seed_v002/DEFAULT/seed/NGC3198_ROUTE_A_A2F10_SEED_C2V002_DEFAULT.json', '88ef386d2bd4e14be23709d21b23fd3b7b57a2cc85adcc09d6a0459bcbc108da'), 'a2_coefficients': ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz', '2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7'), 'route_b_binding': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_uvt_route_b_binding_cx3v006_r5cx3v001_cx3v005.py', 'aee7af1286f2d3d9d52117d6b4d4ae82e31d8776af4a4b0a6da7cee96be12fb3'), 'manifest_writer': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/prep_loader_fix/ngc_route_a_tail_manifest_cx3v011_r5cx3v001_cx3v005.py', 'b9247b1aef0d9c3c05757bd27d68a9964a22d078ce8189311f11e0e2ad6b4c7c')}
V011_B_STAGES={'reference': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_homotopy_reference_root_worker_v001_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py', '69db1fe41adf2bf610acd801a2ffb6f605701b890bef45ab90c99a45c8c8483b'), 'body': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_saved_root_body_array_root_v002_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py', 'd1d70e11d3464d9081e38c6eec560104769e95a3f30e166ac54eac618bea3ad9'), 'offset': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_body_source_offset_root_v003_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py', '1ede2384637bfacaa52944b2aebb70fb82bfe1ede7ec08da3c9691e929df68e3'), 'columns_v001': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_fixed_K_free_surface_root_v001_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py', '4d4c34674d45a3832f28591ac53b88c6f343ce194b1c75d2fced608f55dcd60a'), 'rotation_v001': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_free_surface_rotation_root_v001_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py', '9922a919ebadfc1ba17508f42ee553918d50ad29e36fdfa2bc3677bcbc1767c4'), 'columns_v003': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_fixed_K_free_surface_root_v003_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py', '5657503c4d5c9c7db203c1de09f3ceb6cbd9a5a70aa4e680a56227f20e03b58b'), 'columns_v005': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_fixed_K_free_surface_root_v005_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py', 'dd0c759be8b85b107828b1db8d7e453134176ac32a68544f6f6d6a8f1f92eee0'), 'rotation_v005': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_free_surface_rotation_root_v005_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py', 'e22e79e80a63825458ca659dd32c81bef473e170ba81486ef9db86929007249f'), 'column_mean_v004': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_lower_entropy_column_mean_root_v004_gal_c2v005_cx3v006_r5cx3v001_cx3v005.py', '51ab097c15ff4e30f4001ec0989cbaaac479b11c8c8956eef30b44253092e4dd'), 'feedback_v002': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_free_surface_native_feedback_root_v002_gal_c2v005_r5cx3v001_cx3v005.py', 'fb8eaae6a5202f5eeae5f38a6573b9a0c8cd8ddbbad1ebcbc7c93a1104996ac8'), 'feedback_v004': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_free_surface_native_feedback_root_v004_gal_c2v005_r5cx3v001_cx3v005.py', 'abbc62f53b3d44d776357a2d598844ce96a7b503d3dceb403f79bcd9204fc593')}
# Appended to the exact v010-r4 source by build_driver_cx3v001.py.
# Definitions are inert. The scoped tables apply only to NGC3198 tail calls.
import contextlib
import copy

_V010_NORMALIZE=normalize_spec
_V010_DRY=cmd_dry_run
_V010_RUN=cmd_run
_V010_EXECUTE=execute_chain
_V010_MONITOR=uvt_route_a_monitor
_V010_UVT_BLOCKERS=uvt_binding_blockers
_V010_BINDING_BLOCKERS=binding_blockers
_V010_STATIC_REFUSALS=route_b_static_refusals
_V010_FINAL_ROWS=final_rows_check
_NGC_V011_ACTIVE=False


def _ngc_v011_pin(name):
    p,s=V011_PINS[name]
    verify_pin(p,s,'NGC v011 '+name)
    return Path(p),s


def _ngc_v011_helper():
    return exec_verified(*_ngc_v011_pin('grid_cut'),'ngc_v011_grid_cut')


def _ngc_v011_grid_edge(ni):
    a=ni.get('composite_grid_spec_anisotropic')
    return float(a['axes']['x']['breaks_inverse_kpc'][-1] if a else ni['composite_grid_spec']['breaks_inverse_kpc'][-1])


def _ngc_v011_t120l():
    br=[-2,-1,-.3,-.1,-.03,-.01,0,.01,.03,.1,.3,1,2]
    return {'version':'NGC_T120L_CX3V011','axes':{k:{'breaks_inverse_kpc':br,'panel_orders':o,'total_axis_nodes':sum(o)}
      for k,o in zip('xyz',([22,16,8,5,6,3,3,6,5,8,16,22],[22,16,8,5,6,3,3,6,5,8,16,22],[14,10,5,3,6,2,2,6,3,5,10,14]))},
      'scope':'Registered T120L; 120x120x80; dispatch 0517'}


def normalize_spec(spec):
    if not isinstance(spec,dict):raise Refusal('SPEC_OBJECT_REQUIRED')
    stage0=_ngc_v011_stage0_flag(spec)
    if spec.get('galaxy')=='NGC3198':
        num0=spec.get('numerics',{})
        if not isinstance(num0,dict):raise Refusal('NGC_NUMERICS_OBJECT_REQUIRED')
        if 'k_domain' in num0:raise Refusal('NGC_V011_K_DOMAIN_UNSUPPORTED')
        cf=spec.get('coefficients');oldpath,oldsha=GALAXIES['NGC3198']['default_coefficients']
        if not isinstance(cf,dict) or cf.get('sha256')==oldsha or cf.get('path')==str(oldpath):
            raise Refusal('NGC_P76_FE5_GRID_REFUSED_ALL_TAIL_MODES')
    if not (isinstance(spec,dict) and spec.get('galaxy')=='NGC3198' and 'uv_tail' in spec.get('numerics',{})):
        return _V010_NORMALIZE(spec)
    sp=copy.deepcopy(spec);sp.pop('coefficient_alternative',None);num=sp.get('numerics',{})
    _strict(num,('uv_tail','composite_grid_spec_anisotropic','composite_grid_spec','ngc_outer_gas_cut','h2_tail_mass_rtol','route_a','picard','brackets','column_workers','truncation'),'NGC v011 numerics')
    uv=normalize_uv_tail(num['uv_tail'],ngc=True)
    if not uv.get('enabled',False):raise Refusal('NGC_V011_TAIL_ON_REQUIRED: omit the block for the v010 tail-off path')
    coeff=sp.get('coefficients')
    expected_coeff=STAGE0_GRID_PIN if stage0 else V011_PINS['a2_coefficients']
    if not isinstance(coeff,dict) or (coeff.get('path'),coeff.get('sha256'))!=tuple(expected_coeff):
        raise Refusal('NGC_V011_REQUIRES_A2_GRID_2e3a36d8: fe5a2f06 must not feed further solves')
    verify_pin(coeff['path'],coeff['sha256'],'NGC registered coefficients')
    grid=num.get('composite_grid_spec_anisotropic') or _ngc_v011_t120l()
    if num.get('composite_grid_spec') is not None:raise Refusal('NGC_V011_REQUIRES_ANISOTROPIC_T120L')
    try:_ngc_v011_helper().validate_anisotropic(grid,2.)
    except ValueError as e:raise Refusal(str(e))
    ra=num.get('route_a',{})
    _strict(ra,('column_workers','max_iterations'),'NGC route_a')
    for k,default,hi in (('column_workers',1,8),('max_iterations',16,32)):
        if type(ra.get(k,default)) is not int or not 1<=ra.get(k,default)<=hi:raise Refusal('NGC route_a.'+k)
    cut=num.get('ngc_outer_gas_cut')
    if cut is not None:
        if not isinstance(cut,dict) or set(cut)!={'path','sha256'}:raise Refusal('NGC_CUT_PIN_SCHEMA')
        _abs(cut['path'],'ngc_outer_gas_cut.path');verify_pin(cut['path'],cut['sha256'],'NGC cut')
        try:_ngc_v011_helper().read_cut_record(cut)
        except (ValueError,TypeError,KeyError) as exc:raise Refusal(str(exc))
    is_a=sp.get('schema')==NGC_SCHEMA
    if is_a:
        _strict(sp,('schema','galaxy','label','physical','coefficients','numerics'),'NGC route-A spec')
        sp['schema']=SCHEMA
        sp['source_slots']={'source.monotone_source':{'path':str(GALAXIES['NGC3198']['monotone_source_pin'][0]),'sha256':GALAXIES['NGC3198']['monotone_source_pin'][1]}}
    sp['numerics']={k:v for k,v in num.items() if k in ('picard','brackets','column_workers','truncation')}
    with _ngc_v011_stage0_context(stage0):out=normalize_ngc_route_b_spec(sp)
    if stage0:
        if out.get('member') is not None or out['physical']['entropy_K_factor']!=64/121:raise Refusal('STAGE0_GRID_OUTER_HEADLINE_GEOMETRY_ONLY')
        out['coefficient_alternative']='STAGE0_GRID_OUTER'
        out['alternative_registration']={'path':str(STAGE0_SLOTS_PIN[0]),'sha256':STAGE0_SLOTS_PIN[1]}
    out['numerics'].update(uv_tail=uv,composite_grid_spec=None,composite_grid_spec_anisotropic=grid,ngc_outer_gas_cut=cut,
        route_a=dict(column_workers=ra.get('column_workers',1),max_iterations=ra.get('max_iterations',16)),
        h2_tail_mass_rtol=float(num.get('h2_tail_mass_rtol',1e-12)))
    if out['numerics']['h2_tail_mass_rtol']!=1e-12:raise Refusal('NGC_V011_REGISTERED_H2_ARITHMETIC_TOLERANCE_REQUIRED')
    out['_ngc_produces_route_a']=route_a_inputs_pending(out['route_a_inputs'])
    return out


def _ngc_v011_seed(nspec):
    p,s=_ngc_v011_pin('seed_v002');base=json.loads(p.read_bytes());ni=copy.deepcopy(base['numerical_inputs'])
    phys=nspec['physical'];scale=phys['common_scale_s'];num=nspec['numerics']
    ni.update(Eref_J=scale*phys['Eref_J'],ell_F_m=phys['ell_F_m'],gamma=scale*phys['gamma'],
        composite_grid_spec=None,composite_grid_spec_anisotropic=num['composite_grid_spec_anisotropic'],fourier_points_per_axis=120,
        ngc_outer_gas_cut=num.get('ngc_outer_gas_cut'),max_iterations=num['route_a']['max_iterations'],
        source_gauss_order=10 if nspec.get('member')=='GL10_ALTERNATIVE' else 4)
    # Old decision documents remain provenance; pin only the immutable base seed plus actual source bytes here.
    pins={str(p):s}
    for k in ('manifest','profile','h2_tail_reduction','h2_source'):
        q,t=NGC_DATA[k];verify_pin(q,t,k);pins[str(q)]=t
    q,t=nspec['coefficients']['path'],nspec['coefficients']['sha256'];verify_pin(q,t,'NGC seed actual coefficients');pins[str(q)]=t
    if ni['ngc_outer_gas_cut'] is not None:pins[ni['ngc_outer_gas_cut']['path']]=ni['ngc_outer_gas_cut']['sha256']
    return {'status':'NGC_V011_SOURCE_BUILD_TARGET_FREE_SEED','numerical_inputs':ni,'pins':pins,
        'coefficients':dict(nspec['coefficients']),'parent_seed':{'path':str(p),'sha256':s},
        'parameter_provenance':{'base':'NGC v002 A2F10','changes':'call physical parameters; T120L; registered GL member; optional certified cut'},
        'scope':'No target velocities; new checkpoint required for changed numerical inputs'}


def uvt_route_a_monitor(ni):
    if not _NGC_V011_ACTIVE:return _V010_MONITOR(ni)
    p,s=NGC_DATA['manifest'];m=_pinned_json(p,s,'NGC target-free manifest');n=ni['source_azimuth_count']
    return {'probe_R_m':[float(r['Rad_text'])*ni['kpc_m'] for r in m['rows']],
        'probe_phi_rad':[2*math.pi*j/n for j in range(n)],'v_ref_km_s':None,'tau_km_s':None,'threshold':UVT_MT_THRESHOLD,
        'provenance':{'probe_R_m':{'path':str(p),'sha256':s,'field':'rows[].Rad_text'},
            'v_ref_km_s':'NOT_SUPPLIED: no NGC velocity baseline invented','tau_km_s':'NOT_SUPPLIED: raw source monitor only',
            'probe_phi_rad':'seed source azimuths; M_T remains explicitly NOT_NORMALIZED'}}


@contextlib.contextmanager
def _ngc_v011_context():
    global SCRIPTS_UVT,AUX_UVT,RO1_ROUTE_A,UVT_MONITOR_PINS,SCRIPTS,_NGC_V011_ACTIVE
    names=('SCRIPTS_UVT','AUX_UVT','RO1_ROUTE_A','UVT_MONITOR_PINS','SCRIPTS','_NGC_V011_ACTIVE')
    old={k:globals()[k] for k in names}
    try:
        _NGC_V011_ACTIVE=True
        SCRIPTS_UVT={k:(Path(p),s) for k,(p,s) in V011_B_STAGES.items() if k!='column_mean_v004'}
        SCRIPTS=dict(SCRIPTS,column_mean_v004=(Path(V011_B_STAGES['column_mean_v004'][0]),V011_B_STAGES['column_mean_v004'][1]))
        AUX_UVT=dict(AUX_UVT,route_b_binding=_ngc_v011_pin('route_b_binding'),manifest_writer=_ngc_v011_pin('manifest_writer'))
        RO1_ROUTE_A=dict(RO1_ROUTE_A,worker=_ngc_v011_pin('worker'),worker_parallel=_ngc_v011_pin('worker_parallel'),
            binding=_ngc_v011_pin('binding'),ngc_worker=_ngc_v011_pin('worker'),ngc_worker_parallel=_ngc_v011_pin('worker_parallel'),ngc_binding=_ngc_v011_pin('binding'))
        UVT_MONITOR_PINS={'manifest':NGC_DATA['manifest']}
        yield
    finally:
        for k,v in old.items():globals()[k]=v


def _ngc_v011_dispatch(fn,spec_path,*args):
    raw=json.loads(Path(spec_path).read_bytes())
    if not isinstance(raw,dict):raise Refusal('SPEC_OBJECT_REQUIRED')
    if not isinstance(raw.get('numerics',{}),dict):raise Refusal('NUMERICS_OBJECT_REQUIRED')
    if raw.get('galaxy')=='NGC3198' and 'uv_tail' in raw.get('numerics',{}):
        with _ngc_v011_stage0_context(_ngc_v011_stage0_flag(raw)):
            with _ngc_v011_context():return fn(spec_path,*args)
    return fn(spec_path,*args)


def cmd_dry_run(spec_path,report_dir):
    code=_ngc_v011_dispatch(_V010_DRY,spec_path,report_dir)
    rp=Path(report_dir)/'DRYRUN_REPORT.json'
    if code==0 and rp.is_file():
        report=json.loads(rp.read_bytes());sp=report['normalized_spec']
        if sp.get('galaxy')=='NGC3198' and 'uv_tail' in sp.get('numerics',{}):
            items=report['remaining_refusals']['items'];produces=sp.get('_ngc_produces_route_a')
            expected=[r for r in items if produces and r['class']=='PENDING_ROUTE_A_OUTPUTS']
            blockers=[r for r in items if r not in expected]
            record={'status':'SOURCE_BUILD_DRY_RUN_ONLY','executed_stages':0,
                'report':{'path':str(rp),'sha256':sha256_file(rp)},
                'binding_blockers':report['binding_blockers'],'source_build_blockers':blockers,
                'future_stage_dependencies':expected,
                'dependency_rule':'Only custody outputs of the planned route-A and route-B stages are deferred; stage pin/schema/physical refusals remain blockers.',
                'planned_route_a':any(r['kind']=='route_a' for r in report['stages']),
                'monitor':'NGC M_T_NOT_NORMALIZED; raw source monitor only. No NGC forward v_ref or tau supplied; no convergence claim.',
                'readiness':'PENDING_CERTIFICATES' if not report['binding_blockers'] and all(r['class']=='PENDING_UV_TAIL_CERTIFICATE' for r in blockers) else 'BLOCKED'}
            _write_x(Path(report_dir)/'NGC_SOURCE_BUILD_READINESS.json',record)
    return code
def cmd_run(spec_path,outdir):
    raw=json.loads(Path(spec_path).read_bytes())
    if not isinstance(raw,dict):raise Refusal('SPEC_OBJECT_REQUIRED')
    if raw.get('galaxy')=='NGC3198' and isinstance(raw.get('numerics'),dict) and 'uv_tail' in raw['numerics']:
        return _ngc_v011_dispatch(_cmd_run_ngc_cx3v005,spec_path,outdir)
    return _V010_RUN(spec_path,outdir)


def execute_chain(ctx):
    if ctx.spec.get('galaxy')=='NGC3198' and 'uv_tail' in ctx.spec.get('numerics',{}):return _execute_ngc_v011_chain(ctx)
    return _V010_EXECUTE(ctx)


def route_b_static_refusals(nspec,gc):
    rows=_V010_STATIC_REFUSALS(nspec,gc)
    if nspec.get('_ngc_produces_route_a'):
        rows=[r for r in rows if not (r['where']=='route_a' and r['class']=='PENDING_ROUTE_A_OUTPUTS')]
    return rows


def uvt_binding_blockers(nodes=False):
    if not _NGC_V011_ACTIVE:return _V010_UVT_BLOCKERS(nodes)
    out=[];bp,bs=_ngc_v011_pin('route_b_binding')
    for k,(p,s) in V011_B_STAGES.items():
        try:
            verify_pin(p,s,'NGC stage '+k);t=Path(p).read_text()
            if k!='column_mean_v004' and bs not in t:out.append('NGC_STAGE_BINDING_PIN '+k)
            if k=='column_mean_v004' and ('ngc_outer_gas_cut_custody' not in t or 'QUERY_BEYOND_OUTER_GAS_CUT' not in t):out.append('NGC_COLUMN_MEAN_CUT_CUSTODY_ABSENT')
        except Refusal as e:out.append(str(e))
    for k in ('worker','worker_parallel'):
        p,s=_ngc_v011_pin(k);t=p.read_text()
        for dep in ('prep','binding','prediction'):
            if V011_PINS[dep][1] not in t:out.append('NGC_WORKER_PIN '+k+' '+dep)
        if AUX_UVT['controller'][1] not in t:out.append('NGC_WORKER_CONTROLLER_PIN '+k)
    for k in ('route_b_binding','manifest_writer'):
        p,s=_ngc_v011_pin(k)
        if k=='manifest_writer' and AUX_UVT['controller'][1] not in p.read_text():out.append('NGC_MANIFEST_CONTROLLER_PIN')
    return out


def final_rows_check(final,n_queries,normalized_spec=None):
    rows=final.get('rows')
    special=('QUERY_BEYOND_OUTER_GAS_CUT','QUERY_OUTSIDE_RETAINED_SUPPORT')
    if not (isinstance(rows,list) and rows and all(isinstance(r,dict) and str(r.get('id','')).startswith('NGC3198-Q') for r in rows)):
        return _V010_FINAL_ROWS(final,n_queries)
    actual={r['id']:r.get('reason') for r in rows if r.get('reason') in special}
    cut=(normalized_spec.get('numerics') or {}).get('ngc_outer_gas_cut') if isinstance(normalized_spec,dict) else None
    if cut is None:
        return (False,None) if actual else _V010_FINAL_ROWS(final,n_queries)
    if normalized_spec.get('galaxy')!='NGC3198' or 'uv_tail' not in normalized_spec.get('numerics',{}):return False,None
    try:
        p,s=NGC_DATA['manifest'];manifest=_pinned_json(p,s,'NGC target-free manifest')
        query_rows=[{'id':r['query_id'],'radius_m':float(r['Rad_text'])*KPC_M} for r in manifest['rows']]
        expected=_ngc_v011_helper().registered_cut_rows(cut,query_rows,10 if normalized_spec.get('member')=='GL10_ALTERNATIVE' else 4,KPC_M)
        if [r['id'] for r in rows]!=[r['id'] for r in query_rows] or actual!=expected:return False,None
        if any(r.get('valid') is not False or r.get('speed_km_s') is not None for r in rows if r['id'] in expected):return False,None
    except (ValueError,TypeError,KeyError,OSError):return False,None
    cloned=copy.deepcopy(final)
    for r in cloned['rows']:
        if r.get('reason') in special:r['reason']=INVALID_ROW_REASON
    return _V010_FINAL_ROWS(cloned,n_queries)

def _uvt_ngc_v011_plan(ctx, sp, ni, refuse, prep_patches):
    """C2V010: tail-ON planning, before route A.  Per-stage kept regions C (design sec 1.1, the library's kept_region; route A,
    reference, body: cube K; offset, columns, rotations: the call truncation) and whether each omitted domain D = O \\ C is
    empty; certificate custody (rule UVT_TEST_ONLY_EMPTY_DOMAIN: NONE_TEST_ONLY certificates only when EVERY stage domain is
    empty -- the identity gate B1 -- and then route A runs with admissibility test_only and the route-B successors receive
    --uv-tail-admit-test-only, recorded); the route-B config file (the spec's library config) and the route-A request
    (UNT_UV_TAIL_ROUTE_A_REQUEST_C2V001: config, admissibility, monitor).  Pending certificates: nothing is written."""
    lib = uvt_library()
    nuv = uvt_info(sp['numerics']['uv_tail'])
    if ni['kpc_m'] != lib.KPC_M:
        raise Refusal('UV_TAIL_UNITS: seed kpc_m differs from the tail library KPC_M')
    K_m = _ngc_v011_grid_edge(ni) / KPC_M
    cfg = uvt_config(nuv)
    tr = sp['numerics']['truncation']
    trunc = None if tr['shape'] == 'cube' else {'shape': tr['shape'], 'kmax_inverse_kpc': tr['kmax_inverse_kpc']}
    kept = {}
    for kind in ('route_a',) + UVT_TAIL_KINDS:
        bk = 'route_a' if kind == 'route_a' else UVT_BINDING_KIND[kind]
        try:
            k = lib.kept_region(bk, trunc, K_m)
        except ValueError as exc:
            raise Refusal('numerics.uv_tail kept region (%s): %s' % (bk, exc))
        kept[kind] = {'binding_kind': bk, 'kept': k, 'domain_empty': bool(lib.domain_is_empty(k, cfg['outer']))}
    nodes = uvt_is_nodes(nuv['config'])  # C2V010 r4 (R2): nodes_v001 -- D = G_ext \\ G_K for every stage (never empty), cubes only
    nodes_ctx = None
    if nodes:
        bad = sorted(k for k, v in kept.items() if v['kept'].get('shape') != 'cube')
        if bad:
            raise Refusal('UV_TAIL_NODES_V001_REQUIRES_CUBE_KEPT: stage kept regions %s are not the cube (truncation %r)' % (bad, tr))
        try:
            nodes_ctx = uvt_nodes_library().ext_context(ext_spec=nuv['config']['source_rule']['ext_grid'],
                                                        kept_spec=ni.get('composite_grid_spec'), kpc_m=ni['kpc_m'])['record']
        except ValueError as exc:
            raise Refusal('UV_TAIL_NODES_V001_EXT_GRID_INVALID: %s' % exc)
        for v in kept.values():
            v['domain_empty'] = nodes_ctx['n_ext_nodes'] == 0
            v['domain_rule'] = 'nodes_v001: D = G_ext \\ G_K (%d extra nodes)' % nodes_ctx['n_ext_nodes']
    act = uvt_active(nodes)
    empty_all = all(v['domain_empty'] for v in kept.values())
    if nuv['test_only_certificates'] and not empty_all:
        raise Refusal('UVT_TEST_ONLY_REQUIRES_EMPTY_DOMAIN: NONE_TEST_ONLY certificates %s are admitted only when every stage '
                      'domain D = O \\ C is empty (identity gate B1); non-empty: %s'
                      % (nuv['test_only_certificates'], sorted(k for k, v in kept.items() if not v['domain_empty'])))
    admissibility = 'test_only' if nuv['test_only_certificates'] else 'production'
    certs = {}
    for k in ('eps_certificate', 'lo_certificate'):
        c = nuv['config'][k]
        if k in nuv['pending_certificates']:
            certs[k] = ['%s(%s.path)' % (UVT_PENDING_CERTIFICATE, k), '%s(%s.sha256)' % (UVT_PENDING_CERTIFICATE, k)]
            refuse('uv_tail.' + k, 'PENDING_UV_TAIL_CERTIFICATE',
                   '%s is the template sentinel %s: gate %s (design sec 1.5/1.6) has not produced its certificate; the filled '
                   'spec replaces exactly this entry by {path, sha256}' % (k, UVT_PENDING_CERTIFICATE, 'EPS' if k.startswith('eps') else 'LO'))
        elif c == UVT_TEST_ONLY:
            certs[k] = [UVT_TEST_ONLY, UVT_TEST_ONLY]
        else:
            certs[k] = [str(c['path']), verify_pin(c['path'], c['sha256'], 'uv_tail ' + k)]
    monitor = uvt_route_a_monitor(ni)
    request = {'schema': UVT_REQUEST_SCHEMA, 'uv_tail': nuv['config'], 'admissibility': admissibility, 'monitor': monitor}
    written = not nuv['pending_certificates']
    if written:
        cfg_p, cfg_s = ctx.write_input('uv_tail_config.json', nuv['config'])
        req_p, req_s = ctx.write_input('uv_tail_route_a_request.json', request)
    else:
        cfg_p = ctx.out / 'inputs' / 'uv_tail_config.json'
        req_p = ctx.out / 'inputs' / 'uv_tail_route_a_request.json'
        cfg_s, req_s = 'PENDING_SHA256(%s)' % cfg_p, 'PENDING_SHA256(%s)' % req_p
    return {'schema': UVT_RECORD_SCHEMA, 'enabled': True,
            'config': {'path': str(cfg_p), 'sha256': cfg_s, 'written': written, 'normalized_sha256': nuv['config_sha256']},
            'request': {'path': str(req_p), 'sha256': req_s, 'written': written, 'schema': UVT_REQUEST_SCHEMA},
            'admissibility': admissibility, 'certificates': certs, 'pending_certificates': list(nuv['pending_certificates']),
            'kept_regions': kept, 'domain_empty_all_stages': empty_all, 'outer': cfg['outer'], 'K_inverse_kpc': K_m * KPC_M,
            'monitor_provenance': monitor['provenance'], 'prep_patches': prep_patches,
            'route_a_argv': ['--uv-tail-config', req_p, '--uv-tail-config-sha256', req_s,
                             '--eps-certificate', certs['eps_certificate'][0], '--eps-certificate-sha256', certs['eps_certificate'][1],
                             '--lo-certificate', certs['lo_certificate'][0], '--lo-certificate-sha256', certs['lo_certificate'][1]],
            'truncation_argv': None if trunc is None else canonical(trunc),
            'test_only_flag': ['--uv-tail-admit-test-only'] if admissibility == 'test_only' else [],
            'rules': {'kept_region': 'design sec 1.1: route A, reference, body cube K; offset, columns, rotations the call truncation',
                      'test_only': 'UVT_TEST_ONLY_EMPTY_DOMAIN (NONE_TEST_ONLY certificates only with every stage domain empty)',
                      'admission': 'UVT_ADMISSION_MISMATCH (an admitted route A / reference / body must carry this config sha; tail OFF: none)'},
            'source_rule': 'nodes_v001' if nodes else 'continuum_v001', 'nodes_ext_context': nodes_ctx,  # C2V010 r4 (R2)
            'monitor_probe_R_m': monitor['probe_R_m'], 'monitor_probe_phi_rad': monitor['probe_phi_rad'],  # C2V010 r4 (R3)
            'code': {'route_a_workers': {k: [str(act['route_a'][k][0]), act['route_a'][k][1]] for k in ('worker', 'worker_parallel')},
                     'route_a_solvers': {k: [str(act['aux'][k][0]), act['aux'][k][1]] for k in ('solver', 'solver_parallel')},
                     'route_a_controller': [str(act['aux']['controller'][0]), act['aux']['controller'][1]],
                     'manifest_writer': [str(act['aux']['manifest_writer'][0]), act['aux']['manifest_writer'][1]],
                     'route_b': {k: [str(p), s] for k, (p, s) in act['scripts'].items()},
                     'route_b_binding': [str(act['aux']['route_b_binding'][0]), act['aux']['route_b_binding'][1]],
                     'library': {k: [str(p), s] for k, (p, s) in dict(UVT_LIB, **act['lib_extra']).items()}}}

def _execute_ngc_v011_chain(ctx):
    sp = ctx.spec
    gname = sp['galaxy']
    g = GALAXIES[gname]
    ngc = gname != 'DDO154'
    sv = ctx.saved
    uvt = uvt_info(sp['numerics']['uv_tail']) if 'uv_tail' in sp['numerics'] else None  # C2V010 (u): None = tail OFF (every statement of the chain is then the v009 one)
    uvt_act = uvt_active(uvt_is_nodes(sp['numerics'].get('uv_tail')))  # C2V010 r4 (R2): nodes_v001 -> the nodes tables
    uvt_extra = uvt_act['scripts'] if uvt is not None else None
    uvx = None
    ro1_off = uvt is None and route_a_ro1_workers(sp)  # C2V010 r4 (R5): tail OFF on the RO1 c2v002 workers (declared)
    if uvt is not None:
        ctx.scripts = dict(SCRIPTS, **uvt_act['scripts'], route_a_tail_manifest=uvt_act['aux']['manifest_writer'])
    P = sp['numerics']['picard']['passes']
    bound = sp['numerics']['picard']['speed_change_bound_km_s']
    workers = sp['numerics']['column_workers']
    brackets = sp['numerics']['brackets']
    ef = sp['physical']['entropy_K_factor']
    efs = repr(ef)
    coeff_path, coeff_sha = sp['coefficients']['path'], sp['coefficients']['sha256']
    verify_pin(coeff_path, coeff_sha, 'coefficient grid')
    gc = load_galaxy_config(gname, sp.get('member'))  # c2v006: pinned file = schema V004 copy (member: A2 alternative)
    refusals = []

    def refuse(where, cls, msg):
        """c2v005: a remaining refusal.  Run mode: BLOCKED before any further stage.  Simulate: recorded, planning goes on."""
        refusals.append({'where': where, 'class': cls, 'refusal': msg})
        if ctx.mode == 'run':
            raise Blocked('%s [%s]: %s' % (where, cls, msg))

    info = {}
    if not ngc:
        seed_obj, changed, reusable = per_call_seed(sp)
        if reusable:
            seed_path, seed_sha = g['base_seed']
        else:
            seed_path, seed_sha = ctx.write_input('seed_c2v001.json', seed_obj)
        seed_path = Path(seed_path)
        ni = seed_obj['numerical_inputs']
        info['seed'] = {'path': str(seed_path), 'sha256': seed_sha, 'base_seed_reused': reusable, 'changed_fields': changed}
        literal_rows = ddo_driver_literal_check(g, gc)
    else:
        literal_rows = ngc_driver_value_check(g, gc)
        ra_in = sp['route_a_inputs']
        if sp.get('_ngc_produces_route_a'):
            seed_doc=_ngc_v011_seed(sp)
            seed_path,seed_sha=ctx.write_input('ngc_seed_v011.json',seed_doc)
            ni=seed_doc['numerical_inputs']
        elif route_a_inputs_pending(ra_in):
            # c2v006: nothing under a declared (pending) route-A directory is opened; placeholders only.
            seed_path, seed_sha, ni = Path('%s(seed path)' % PENDING_ROUTE_A), '%s(custody.seed_sha256)' % PENDING_ROUTE_A, None
            refuse('route_a', 'PENDING_ROUTE_A_OUTPUTS', 'NGC3198 route-A outputs (seed, attempt, checkpoint) are not supplied yet; '
                   'route B consumes them from the NGC route-A lane (route A is not run by this driver)')
            for where, what in NGC_DEFERRED_ROUTE_A_CHECKS:  # c2v006 (D8): checks that need route-A bytes, listed by name
                refuse(where, 'PENDING_ROUTE_A_OUTPUTS', 'needs route-A bytes: ' + what)
            info['route_a_inputs_declared'] = ra_in
        else:
            seed_path = Path(ra_in['seed']['path'])
            seed_sha = verify_pin(seed_path, ra_in['seed']['sha256'], 'NGC route-A seed')
            seed_doc = json.loads(seed_path.read_bytes())
            ni = seed_doc['numerical_inputs']
            info['route_a_seed_coefficients'] = ngc_seed_coefficient_check(seed_doc, sp['coefficients'], g)  # c2v006 (A5, D1)
        info['seed'] = {'path': str(seed_path), 'sha256': seed_sha, 'source': 'route_a_inputs.seed (NGC route-A lane)'}
        info['member'] = {'member': sp.get('member'), 'label': ('PRIMARY' if sp.get('member') is None else
                          gc['schema']['members']['NGC3198'][sp['member']]['label']),
                          'entropy_K_member': sp['physical'].get('entropy_K_member')}
    info['galaxy_config'] = {'path': gc['path'], 'sha256': gc['sha256'], 'driver_literal_check': literal_rows}
    if ni is not None:
        if ni['kpc_m'] != KPC_M:
            raise Refusal('seed kpc_m differs from driver constant')
        call_phys = {k: ni[k] for k in ('Eref_J', 'ell_F_m', 'gamma')}
        if ngc:
            s = sp['physical']['common_scale_s']
            want = {'Eref_J': s * sp['physical']['Eref_J'], 'gamma': s * sp['physical']['gamma'], 'ell_F_m': sp['physical']['ell_F_m']}
            if any(call_phys[k] != want[k] for k in want):
                raise Refusal('NGC3198: call physical parameters (times s) differ from the route-A seed numerical_inputs')
    else:
        call_phys = None
    tr = sp['numerics']['truncation']
    if ni is not None:
        kgrid = _ngc_v011_grid_edge(ni)
        if tr['kmax_inverse_kpc'] is not None and tr['kmax_inverse_kpc'] > kgrid:
            raise Refusal('mask kmax exceeds the composite grid edge %.6g/kpc' % kgrid)
        kmask_m = (tr['kmax_inverse_kpc'] if tr['kmax_inverse_kpc'] is not None else kgrid) / KPC_M
    else:
        kmask_m = None
    coeff_default = (coeff_path == str(g['default_coefficients'][0]) and coeff_sha == g['default_coefficients'][1])
    reuse_path, reuse_sha = GENERALIZED['reference']['base']  # c2v005: the REVIEWED reference worker is the reuse module
    percall = {'custody.seed_sha256': seed_sha, 'source.coefficients': {'path': str(coeff_path), 'sha256': coeff_sha}}
    # c2v005: declared input slots (NGC3198 source.monotone_source, N3) come from the call spec only
    for k in gc['slots']:
        v = (sp.get('source_slots') or {}).get(k, PENDING_SLOT)
        percall[k] = v
        if _has_pending(v):
            refuse(k, 'PENDING_N3_MONOTONE_SOURCE', '%s is a DECLARED_INPUT_SLOT (N3) not yet filled by the reviewed reducer output' % k)
    gc_written = {}
    gfields = {}  # C2V008 (a): per-call geometry config fields; stays empty at the registered geometry and for NGC3198

    def stage_gc(kind, tag='', producers=None):
        """Write (once per name) the per-stage config of successor `kind`; returns (path, sha, meta)."""
        name = 'galaxy_config_%s%s.json' % (kind, ('_' + tag) if tag else '')
        if name in gc_written:
            return gc_written[name]
        missing = [k for k in STAGE_PER_CALL[kind] if k not in percall]
        if missing:
            raise Refusal('c2v005 internal: per-call fields %s not yet computed for %s' % (missing, kind))
        pc = {k: percall[k] for k in STAGE_PER_CALL[kind]}
        pc.update({k: percall[k] for k in gc['slots'] if k in consumed_fields(kind)})  # a slot travels only to its consumers
        # C2V008 (a): per-call geometry fields (empty at the registered geometry) travel only to their consumers too
        pc.update({k: v for k, v in gfields.items() if k in consumed_fields(kind)})
        obj, omitted = stage_config_object(kind, gc, pc, omit_missing_per_call=True, producers=producers)
        pending = sorted(k for k, v in pc.items() if _has_pending(v))
        if producers is not None and _has_pending(producers):
            pending.append('producer_pins')
        meta = {'format': GENERALIZED[kind]['format'], 'galaxy_config_file': {'path': gc['path'], 'sha256': gc['sha256']},
                'per_call_fields': sorted(pc), 'omitted_per_call_fields': omitted}
        if producers is not None:
            meta['producer_pins'] = producers
        if pending:  # simulate only: never hash a placeholder; the file is not written
            p = ctx.out / 'inputs' / name
            s = 'PENDING_SHA256(%s)' % p
            meta.update(path=str(p), sha256=s, written=False, pending_fields=pending)
            if ctx.mode != 'run':
                meta['pending_probe'] = pending_probe(kind, gc, pc, producers, ctx.out / 'inputs', tag)
        else:
            p, s = ctx.write_input(name, obj)
            meta.update(path=str(p), sha256=s, written=True)
        gc_written[name] = (p, s, meta)
        return gc_written[name]

    def gen_request(name, key, argv, tag='', module_patches=None, mask=None, producers=None, stage_globals=None):
        """Request for a gal_c2v003 successor: c2v003 argv + galaxy-config tokens appended; no stage globals (C2V008 (a):
        except the reference PROFILE/PROFILE_SHA at a per-call geometry, as c2v003c)."""
        p, s, meta = stage_gc(key, tag, producers)
        req = ctx.request(name, key, list(argv) + galaxy_config_argv(key, p, s), stage_globals=stage_globals or {},
                          module_patches=module_patches, mask=mask)
        req['galaxy_config'] = meta
        return req

    producer_log = []

    def producer(dirs, key, flag, stage, admitted=False):
        """c2v004 rule: sha of the script that produced the upstream output(s).  run: SCRIPTS[key] (this call ran it);
        simulate on SAVED outputs, or an ADMITTED upstream in any mode (c2v005): the worker_sha256 recorded in their
        start.json, which must be the successor or its reviewed base."""
        run_value = ctx.scripts[key][1]  # C2V010 (u): the active script (SCRIPTS unless tail ON)
        val, src = run_value, 'SCRIPTS[%s] (this call runs it)' % key
        if ctx.mode != 'run' or admitted:
            recs = [Path(x) / 'start.json' for x in dirs]
            have = [p for p in recs if p.is_file()]
            if have:
                vals = {json.loads(p.read_text())['worker_sha256'] for p in have}
                if len(have) != len(recs) or len(vals) != 1:
                    raise Refusal('c2v005: mixed upstream producers for %s %s' % (stage, flag))
                val, src = vals.pop(), 'worker_sha256 recorded in the %s upstream start.json' % ('admitted' if admitted else 'saved')
                producer_pin(key, val, uvt_extra)
            elif admitted:
                raise Refusal('c2v005: admitted %s output has no start.json to name its producer' % key)
        producer_log.append({'stage': stage, 'flag': flag, 'value': val, 'source': src, 'run_mode_value': run_value,
                             'run_mode_differs': val != run_value})
        return val

    # c2v003: route-A prep by node count (DDO154 only; NGC3198 route A is run by the NGC route-A lane).
    if not ngc:
        nk = int(ni['fourier_points_per_axis'])
        if nk <= PREP_V007_MAX_AXIS_NODES:
            prep_key = 'prep'
        elif nk <= PREP_V008_MAX_AXIS_NODES:
            prep_key = 'prep_v008'
            verify_pin(PREP_V008_REVIEW[0], PREP_V008_REVIEW[1], 'prep V008 review')
        elif nk <= PREP_V009_MAX_AXIS_NODES:  # C2V009 (a)
            prep_key = 'prep_v009'
        else:
            raise Refusal('%d nodes/axis exceeds every route-A prep budget (%d)' % (nk, PREP_V009_MAX_AXIS_NODES))
        prep_path, prep_sha = AUX[prep_key]
        prep_info = {'path': str(prep_path), 'sha256': prep_sha, 'axis_nodes': nk,
                     'rule': 'V007 for <=%d nodes/axis (unchanged); V008 for %d..%d (review %s)'
                             % (PREP_V007_MAX_AXIS_NODES, PREP_V007_MAX_AXIS_NODES + 1, PREP_V008_MAX_AXIS_NODES, PREP_V008_REVIEW[1][:16])}
        if prep_key == 'prep_v009':  # C2V009 (a): only here does the record differ from c2v008
            prep_info['rule'] += '; V009 for %d..%d (declared G5/G6 only; review: separate, named by prereg V006)' % (
                PREP_V008_MAX_AXIS_NODES + 1, PREP_V009_MAX_AXIS_NODES)

    # C2V008 (a), from c2v003b (c2v003c @L1338): per-call geometry inputs (DDO154 only; None at the registered geometry:
    # pinned files, plan unchanged).  Then the stage-admission probe: run mode is BLOCKED here, before any stage, when a
    # successor's own admission refuses the per-call geometry fields (simulate: recorded, planning goes on).
    geo = geometry_inputs(ctx, sp) if not ngc else None
    profile_sha = None if ngc else (geo['profile'][1] if geo is not None else g['profile'][1])
    if not ngc:
        src_path, src_sha = geo['monotone'] if geo is not None else g['monotone_source']
    if geo is not None:
        gfields.update(geometry_config_fields(geo))
        probe = geometry_admission_probe(ctx, gc, gfields)
        info['geometry'] = dict(geo['record'], config_fields=gfields, stage_admission_probe=probe)
        ctx.geometry = info['geometry']
        if not probe['admitted']:
            refuse('geometry', 'GEOMETRY_NOT_ADMITTED_BY_STAGE_BINDING',
                   'distance_Mpc %r != registered %r: the pinned gal_c2v005 stages refuse the per-call geometry config fields '
                   '(their own admission, schema V005): %s%s. No stage is run.' % (sp['physical']['distance_Mpc'], g['registered_geometry']['distance_Mpc'],
                                               '; '.join('%s: %s' % kv for kv in sorted(probe['refused'].items())),
                                               '' if probe['controls_accepted'] else ' (registered-geometry control copies also refused)'))

    if ngc:
        prep_key='ngc_v011'
        prep_path,prep_sha=_ngc_v011_pin('prep')
        prep_info={'path':str(prep_path),'sha256':prep_sha,'axis_nodes':[120,120,80],'rule':'NGC registered T120L successor'}
    if uvt is not None:  # C2V010 (u): tail-ON planning (kept regions, certificates, route-B config, route-A request)
        uvx = _uvt_ngc_v011_plan(ctx, sp, ni, refuse, uvt_prep_patches(coeff_default, coeff_path, coeff_sha, geo, prep_path, prep_sha))
        ctx.uv_tail = uvx

    # ---------------- route A
    adm = sp.get('admit') or {}
    if ngc and not sp.get('_ngc_produces_route_a'):
        ra_in = sp['route_a_inputs']
        if route_a_inputs_pending(ra_in):
            att, cp = Path('%s(attempt_directory)' % PENDING_ROUTE_A), Path('%s(checkpoint_directory)' % PENDING_ROUTE_A)
            info['route_a'] = {'mode': 'pending_ngc_route_a_lane', 'attempt': str(att), 'checkpoint': str(cp),
                               'declared': ra_in if isinstance(ra_in, dict) else None}
        else:
            att, cp = Path(ra_in['attempt_directory']), Path(ra_in['checkpoint_directory'])
            fin = json.loads((att / 'finish.json').read_text())
            if fin['status'] != 'RETURNED_ACTUAL_RESULT' or sha256_file(att / 'result.json') != ra_in['result_sha256'] or fin['result_sha256'] != ra_in['result_sha256']:
                raise Refusal('NGC route-A attempt does not verify')
            info['route_a'] = {'mode': 'admitted_ngc_route_a_lane', 'attempt': str(att), 'checkpoint': str(cp)}
    elif 'route_a' in adm:
        a = adm['route_a']
        att, cp = Path(a['attempt_directory']), Path(a['checkpoint_directory'])
        fin = json.loads((att / 'finish.json').read_text())
        if fin['status'] != 'RETURNED_ACTUAL_RESULT' or sha256_file(att / 'result.json') != a['result_sha256'] or fin['result_sha256'] != a['result_sha256']:
            raise Refusal('admitted route-A attempt does not verify')
        info['route_a'] = {'mode': 'admitted', 'attempt': str(att), 'checkpoint': str(cp)}
    else:
        d = ctx.stage_dir('route_a')
        sa = (sv.get('route_a') or {}) if ctx.mode != 'run' else {}
        att = Path(sa['attempt']) if 'attempt' in sa else d / 'attempt_000'
        cp = Path(sa['checkpoint']) if 'checkpoint' in sa else d / 'checkpoint'
        patches = []
        prep_set = {}  # C2V008 (a): one prep module patch as c2v003c (same key order; identical to c2v007 without geometry)
        if not coeff_default:
            prep_set.update({'COEFFICIENT': {'__path__': coeff_path}, 'COEFFICIENT_SHA': coeff_sha})
        if geo is not None:
            prep_set['C'] = {'__path__': geo['C_dir']}  # c2v003b: prep reads C/PROFILE_NAME and C/<binding V003>
        if prep_set:
            patches.append({'path': str(prep_path), 'sha256': prep_sha, 'set': prep_set})
        # C2V007 (b): N = 1 -> exactly the c2v006 request (reviewed worker c4cb6826 + reviewed solver 44d9c23c);
        # N > 1 -> the parallel worker successor with the parallel solver and --column-workers N.  Same LOCAL keys and
        # pins, so the prep COEFFICIENT module patch and the prep V008 LOCAL['prep'] dict item apply unchanged.
        ra_workers = route_a_column_workers(sp)
        solver_pin = AUX['solver'] if ra_workers == 1 else PARALLEL_ROUTE_A['solver']
        if uvt is not None:  # C2V010 (u): the uvtail solvers (route_a/; serial 8ef3079b, parallel 7667025b)
            solver_pin = uvt_act['aux']['solver'] if ra_workers == 1 else uvt_act['aux']['solver_parallel']
        ra_argv = ['--seed', seed_path, '--seed-sha256', seed_sha, '--solver', solver_pin[0], '--solver-sha256', solver_pin[1],
                   '--checkpoint-module', AUX['checkpoint_module'][0], '--checkpoint-module-sha256', AUX['checkpoint_module'][1],
                   '--outdir', att, '--checkpoint-directory', cp, '--start-iteration', '0']
        if ra_workers > 1:
            ra_argv += ['--column-workers', str(ra_workers)]
        if uvt is not None:  # C2V010 (u): tail request, certificates, new sidecar directory (the controller creates it)
            ra_argv += uvx['route_a_argv'] + ['--uv-tail-sidecar-directory', d / 'uv_tail_sidecar']
        if ro1_off:  # C2V010 r4 (R5): the RO1 worker CLI with a tail-disabled request (sidecar never created)
            off_p, off_s = ctx.write_input('uv_tail_route_a_request_tail_off_ro1.json', ro1_off_request())
            ra_argv += ['--uv-tail-config', off_p, '--uv-tail-config-sha256', off_s, '--eps-certificate', UVT_TEST_ONLY,
                        '--eps-certificate-sha256', UVT_TEST_ONLY, '--lo-certificate', UVT_TEST_ONLY, '--lo-certificate-sha256', UVT_TEST_ONLY,
                        '--uv-tail-sidecar-directory', d / 'uv_tail_sidecar']
        req = ctx.request('route_a', 'route_a', ra_argv, module_patches=patches)
        if ra_workers > 1:
            req['script'], req['script_sha256'] = str(PARALLEL_ROUTE_A['worker'][0]), PARALLEL_ROUTE_A['worker'][1]
        if uvt is not None:  # C2V010 (u): the RO1 successors of the uvtail workers (same CLI and LOCAL keys); r4: nodes -> nodes workers
            w = uvt_act['route_a']['worker'] if ra_workers == 1 else uvt_act['route_a']['worker_parallel']
            req['script'], req['script_sha256'] = str(w[0]), w[1]
        if ro1_off:  # C2V010 r4 (R5): tail OFF on the RO1 c2v002 workers, the v009 solvers
            w = RO1_ROUTE_A['worker'] if ra_workers == 1 else RO1_ROUTE_A['worker_parallel']
            req['script'], req['script_sha256'] = str(w[0]), w[1]
        if prep_key in ('prep_v008', 'prep_v009'):  # C2V009 (a): v009 is injected the same way as v008
            req['stage_dict_items'] = {'LOCAL': {'prep': {'path': str(prep_path), 'sha256': prep_sha}}}
        ctx.run_stages([req], [d])
        info['route_a'] = {'mode': 'computed', 'attempt': str(att), 'checkpoint': str(cp)}
        info['route_a']['implementation'] = {  # C2V007 (b)
            'column_workers': ra_workers, 'kind': 'REVIEWED_SERIAL' if ra_workers == 1 else 'PARALLEL_C2V001',
            'worker': {'path': req['script'], 'sha256': req['script_sha256']},
            'solver': {'path': str(solver_pin[0]), 'sha256': solver_pin[1]}}
        if uvt is not None:  # C2V010 (u)
            info['route_a']['implementation']['kind'] = (('UVTAIL_NODES_RO1_SERIAL_C2V001' if ra_workers == 1 else 'UVTAIL_NODES_RO1_PARALLEL_C2V001')
                                                         if uvt_is_nodes(sp['numerics'].get('uv_tail')) else
                                                         ('UVTAIL_RO1_SERIAL_C2V001' if ra_workers == 1 else 'UVTAIL_RO1_PARALLEL_C2V001'))
        if ro1_off:  # C2V010 r4 (R5)
            info['route_a']['implementation']['kind'] = 'TAIL_OFF_RO1_SERIAL_C2V010R4' if ra_workers == 1 else 'TAIL_OFF_RO1_PARALLEL_C2V010R4'
            info['route_a']['implementation']['ro1_workers'] = True
    if not ngc:
        info['route_a']['prep'] = dict(prep_info, role=('used by this call' if info['route_a']['mode'] == 'computed' else
                                                        'expected for this grid; the admitted checkpoint records its own (custody.prep_code_pins)'))
    # C2V007 (a) F1 (c2v003c hunk @@ -1229): classify the route-A outcome from its own result.json before any iteration verdict.
    # (A pending NGC attempt path is a PENDING placeholder, never a file: nothing is opened.)
    att_res = Path(att) / 'result.json'
    ra = json.loads(att_res.read_text()) if att_res.is_file() else None
    ra_outcome = route_a_outcome_record(ra, att_res) if ra is not None else None
    ctx.route_a_outcome = ra_outcome
    if ra_outcome is not None:
        info['route_a']['outcome'] = ra_outcome
    # C2V007 (b): a route A computed by this call (run mode) must carry the solver it was launched with in its IDENTITY.
    # Simulate on saved outputs and admitted route A: the solver is recorded (custody.solver_code), not required.
    expected_solver = solver_pin if (info['route_a']['mode'] == 'computed' and ctx.mode == 'run') else None
    if (Path(cp) / 'IDENTITY.json').is_file():
        # c2v005: route_a_custody reads the converged final iteration by the strict rule (no literal 4)
        # C2V008: (a) the call source profile (DDO154; c2v003b); (d) the attempt must belong to this checkpoint (CHECK D1;
        # DDO154 only, as in c2v003c: the NGC route-A result bytes may not be read in this lane, so NGC is left as c2v007)
        cust = route_a_custody(cp, seed_sha, coeff_path, call_phys, outcome=ra_outcome, expected_solver=expected_solver,
                               profile_sha=profile_sha, attempt_result=ra)
        if 'route_a' in adm and cust['identity_sha256'] != adm['route_a']['identity_sha256']:
            raise Refusal('admitted checkpoint identity differs from declared')
        if ngc and not sp.get('_ngc_produces_route_a') and cust['identity_sha256'] != sp['route_a_inputs']['identity_sha256']:
            raise Refusal('NGC route-A checkpoint identity differs from route_a_inputs.identity_sha256')
        if uvt is None:  # C2V010 (u): a tail-OFF call never admits a tail-ON route A (never fires on v009 checkpoints)
            uvt_route_a_identity_check(cp, None)
        elif uvt['config_sha256'] is not None:
            uvx['route_a_checkpoint_tail'] = uvt_route_a_identity_check(cp, uvt['config_sha256'])
        else:
            uvx['route_a_checkpoint_tail'] = 'PENDING (certificate sentinel: config sha unknown)'
    else:
        # C2V010 (m2): the R-A F-A fix (REVIEW_DRIVER_V008_C4_V001 sec 6, f0987f41), before any outcome verdict.
        if not ngc and info['route_a']['mode'] == 'admitted':
            raise Refusal('ROUTE_A_CHECKPOINT_MISSING: %s/IDENTITY.json absent; admitted attempt cannot be paired (D1)' % cp)
        if info['route_a']['mode'] == 'computed' and ctx.mode == 'run' and ra_outcome is not None:
            raise StageFailed('ROUTE_A_RESULT_WITHOUT_CHECKPOINT: %s' % cp)
        if ra_outcome is not None:  # C2V007 (a) F1 (c2v003c): no checkpoint but a returned result -> outcome first
            require_route_a_fixed_point(ra_outcome)
        if ngc and not route_a_inputs_pending(sp['route_a_inputs']):  # c2v006: a supplied NGC route A must have its checkpoint
            raise Refusal('NGC route-A checkpoint IDENTITY.json missing under %s' % cp)
        cust = {'identity_sha256': '%s(custody.checkpoint_identity_sha256)' % PENDING_ROUTE_A if ngc else 'PENDING(route_a identity)',
                'iteration': '%s(route_a.accepted_iteration)' % PENDING_ROUTE_A if ngc else 'PENDING(route_a iteration)',
                'start_payload_sha256': 'PENDING', 'g4_ref': {'file_sha256': 'PENDING'}, 'waves_ref': None}
    info['route_a']['custody'] = cust
    if ra is not None:
        info['route_a']['route_a_rows'] = ra['result']['result']['rows']
        if geo is not None:
            info['route_a']['route_a_rows_scope'] = geo['record']['route_a_rows']  # c2v003b
    if uvt is not None:  # C2V010 (u): the route-A tail record, then the manifest stage (reference, body, offset read it)
        u = ((ra or {}).get('result') or {}).get('uv_tail') if ra is not None else None
        if ra is not None and not isinstance(u, dict):
            raise StageFailed('UV_TAIL_ROUTE_A_RECORD_MISSING: %s has no result.uv_tail (a tail-OFF route A in a tail-ON call?)' % att_res)
        if isinstance(u, dict) and uvt['config_sha256'] is not None and u.get('config_sha256') != uvt['config_sha256']:
            raise Refusal('UVT_ADMISSION_MISMATCH: route-A result tail config %r is not this call config %s' % (u.get('config_sha256'), uvt['config_sha256']))
        uvx['route_a_record'] = None if not isinstance(u, dict) else {k: u.get(k) for k in (
            'outcome', 'accepted_iteration', 'M_T_accepted', 'M_T_threshold', 'monitor_status', 'flags', 'production_admissible',
            'boundary_state_digest_at_return', 'config_sha256', 'request_sha256', 'admissibility', 'E_A_rows_km_s_accepted', 'sidecar')}
        if uvx['route_a_record'] is not None:  # C2V010 r4 (R3; A50 item 13): the E^A row radii, in the request's probe order
            uvx['route_a_record'].update(probe_R_m=list(uvx['monitor_probe_R_m']), probe_phi_rad=list(uvx['monitor_probe_phi_rad']),
                                         probe_source='uv_tail request monitor (binding f42c7c65 query_rows[].radius_m; seed azimuths)')
        d = ctx.stage_dir('route_a_tail_manifest')
        mdir = d / 'manifest'
        margv = ['--seed', seed_path, '--seed-sha256', seed_sha, '--attempt-directory', att, '--checkpoint-directory', cp,
                 '--checkpoint-module', AUX['checkpoint_module'][0], '--checkpoint-module-sha256', AUX['checkpoint_module'][1],
                 '--uv-tail-request', uvx['request']['path'], '--uv-tail-request-sha256', uvx['request']['sha256'], '--outdir', mdir]
        mreq = ctx.request('route_a_tail_manifest', 'route_a_tail_manifest', margv, module_patches=uvx['prep_patches'])
        if prep_key in ('prep_v008', 'prep_v009'):  # the same prep the route-A worker ran (LOCAL['prep'] dict item)
            mreq['stage_dict_items'] = {'LOCAL': {'prep': {'path': str(prep_path), 'sha256': prep_sha}}}
        ctx.run_stages([mreq], [d])
        uvx['manifest'] = {'path': str(mdir / 'ROUTE_A_TAIL_MANIFEST.json'), 'sha256': ctx.finish_sha(mdir, 'ROUTE_A_TAIL_MANIFEST.json')}
        if (mdir / 'finish.json').is_file():
            mf = json.loads((mdir / 'finish.json').read_text())
            uvx['manifest'].update(state_digest=mf.get('state_digest'), empty=mf.get('empty'), production_admissible=mf.get('production_admissible'))

    def uvt_argv(kind, source_rotation=None):
        """C2V010 (u): the tail argv of a route-B uvt successor ([] when tail OFF): config, manifest (reference, body,
        offset), the call truncation for the masked kinds, the source rotation (rfs/le columns, le rotation)."""
        if uvt is None:
            return []
        bk = UVT_BINDING_KIND[kind]
        a = ['--uv-tail-config', uvx['config']['path'], '--uv-tail-config-sha256', uvx['config']['sha256']] + uvx['test_only_flag']
        if bk in ('reference', 'body', 'offset'):
            a += ['--route-a-tail-manifest', uvx['manifest']['path'], '--route-a-tail-manifest-sha256', uvx['manifest']['sha256']]
        if bk not in ('reference', 'body') and uvx['truncation_argv'] is not None:
            a += ['--uv-tail-truncation', uvx['truncation_argv']]
        if bk in ('rfs_columns', 'le_columns', 'le_rotation'):
            a += ['--uv-tail-source-rotation-directory', source_rotation]
        return a
    ident = cust['identity_sha256']
    it = cust['iteration']
    info['route_a']['reported_final_iteration'] = it
    percall['custody.checkpoint_identity_sha256'] = ident
    percall['route_a.accepted_iteration'] = it
    reuse_patch = {'path': str(reuse_path), 'sha256': reuse_sha, 'set': {'SEED_SHA': seed_sha, 'IDENTITY': ident}}
    ref_globals = None
    if geo is not None:  # C2V008 (a), c2v003b: homotopy worker PROFILE (reference stage itself; body/offset read it as reuse.PROFILE)
        ref_globals = {}
        for target in (reuse_patch['set'], ref_globals):
            target.update(PROFILE={'__path__': geo['profile'][0]}, PROFILE_SHA=geo['profile'][1])
    mask = None
    if tr['shape'] != 'cube':
        mask = {'shape': tr['shape'], 'kmax_inverse_m': kmask_m, 'g4_file_sha256': cust['g4_ref']['file_sha256'],
                'waves_ref': cust['waves_ref'], 'checkpoint_module': [str(AUX['checkpoint_module'][0]), AUX['checkpoint_module'][1]],
                'cache_module': [str(AUX['cache'][0]), AUX['cache'][1]]}
    common = ['--seed', seed_path, '--checkpoint-directory', cp]
    # c2v005 driver-level galaxy values (NGC3198: from the galaxy config; an undecided field is a refusal)
    if ngc:
        fa, fa_ok, _ = gc_value(gc, 'driver.fixed_args')
        if fa_ok:
            FA = dict(fa)
        else:
            FA = {k: 'NONE_IN_REVIEWED_CODE(driver.fixed_args.%s)' % k for k in FIXED_ARGS}
            refuse('driver.fixed_args', 'UNDECIDED_NGC_FIELD', 'driver.fixed_args is NONE_IN_REVIEWED_CODE for NGC3198 (no ROOT_DECISIONS row)')
    else:
        FA = FIXED_ARGS

    # ---------------- reference (c2v005: generalized successor + reference module successor 1b00add9)
    if 'reference' in adm:
        ref = Path(adm['reference']['directory'])
        verify_pin(ref / 'start.json', adm['reference']['start_sha256'], 'admitted reference start')
        verify_pin(ref / 'finish.json', adm['reference']['finish_sha256'], 'admitted reference finish')
        if not ngc and json.loads((ref / 'start.json').read_text())['source_custody']['sha256'] != profile_sha:  # C2V008 (a), c2v003b
            raise Blocked('REFERENCE_GEOMETRY_MISMATCH: admitted reference was not built from this call source profile')
        r_t = uvt_admitted_record_check(ref / 'start.json', uvt, 'reference')  # C2V010 (u)
        if uvt is not None:
            uvx['admitted_reference_tail'] = r_t
    else:
        d = ctx.stage_dir('reference')
        ref = d / 'reference' if ctx.mode == 'run' else ctx.saved_or('reference', d / 'reference')
        req = gen_request('reference', 'reference', common + ['--reference-module', AUX['reference_module'][0],
                          '--reference-sha256', AUX['reference_module'][1], '--outdir', ref] + uvt_argv('reference'), stage_globals=ref_globals)
        ctx.run_stages([req], [d])
    percall['custody.reference_run'] = {'directory': str(ref), 'start_sha256': ctx.finish_sha(ref, 'start.json'),
                                        'finish_sha256': ctx.finish_sha(ref)}

    # ---------------- body (c2v005: generalized successor; REFERENCE/DATA_PINS travel as custody.reference_run/source.monotone_source)
    if 'body' in adm:
        body = Path(adm['body']['directory'])
        verify_pin(body / 'finish.json', adm['body']['finish_sha256'], 'admitted body finish')
        if not ngc and src_sha not in json.loads((body / 'start.json').read_text())['input_pins'].values():  # C2V008 (a), c2v003b
            raise Blocked('BODY_GEOMETRY_MISMATCH: admitted body was not built from this call monotone source')
        b_t = uvt_admitted_record_check(body / 'finish.json', uvt, 'body')  # C2V010 (u)
        if uvt is not None:
            uvx['admitted_body_tail'] = b_t
    else:
        d = ctx.stage_dir('body')
        body = d / 'body' if ctx.mode == 'run' else ctx.saved_or('body', d / 'body')
        req = gen_request('body', 'body', common + ['--outdir', body] + uvt_argv('body'), module_patches=[reuse_patch])
        ctx.run_stages([req], [d])
    body_fin = ctx.finish_sha(body)
    percall['custody.body_worker_sha256'] = producer([body], 'body', 'config custody.body_worker_sha256', 'offset', admitted='body' in adm)

    # ---------------- offset (generalized successor; COEFF/COEFF_SHA travel as source.coefficients)
    d = ctx.stage_dir('offset')
    off = d / 'offset' if ctx.mode == 'run' else ctx.saved_or('offset', d / 'offset')
    req = gen_request('offset', 'offset', common + ['--body-directory', body, '--body-finish-sha256', body_fin,
                      '--wave-batch', FA['wave_batch'], '--position-batch', FA['position_batch'], '--outdir', off] + uvt_argv('offset'),
                      module_patches=[reuse_patch], mask=mask)
    ctx.run_stages([req], [d])
    if mask is not None:
        # c2v003 (CHECK_V001 s3 corr. 2): refuse to continue unless the mask demonstrably fired.
        tinfo = {'shape': tr['shape'], 'kmax_inverse_m': kmask_m,
                 'scope': 'route A, reference and body unmasked (cube G4); offset real-space total and '
                          'updated_base_arrays full_fields/Phi0/angular_forcing/r0 are a MIXED field (see truncation_mask)'}
        if ctx.mode == 'run' or ((Path(off) / 'unit_response.npz').is_file() and (Path(off) / 'offset_prepared.npz').is_file()):
            tinfo['mask_check'] = mask_fired_check(off, tr['shape'], kmask_m)
            ctx.event(stage='offset', event='mask_check', kept_nodes=tinfo['mask_check']['kept_nodes'],
                      total_nodes=tinfo['mask_check']['total_nodes'])
        else:
            tinfo['mask_check'] = 'PENDING (offset outputs not present in simulate mode)'
        info['truncation'] = tinfo
    off_fin = ctx.finish_sha(off)
    percall['custody.offset_finish_sha256'] = off_fin  # c2v005: no stage global OFFSET_SHA is patched any more
    base = common + ['--offset-directory', off]

    verify_pin(g['solver_template'][0], g['solver_template'][1], 'solver template')
    template = json.loads(Path(g['solver_template'][0]).read_text())['solver']
    if ngc and ni is not None:
        info['solver_template_mapping'] = template_mapping_check(ni, template)
    n = g['n_columns_by_member'][sp.get('member')] if ngc else g['n_columns']  # c2v006: GL10 member = 250 (checked == config)

    def column_pass(tag, key, extra_args, plan_runs):
        """plan_runs: list of (controls_path, controls_sha) or ('GENERATE', controls_obj).  Returns run dirs."""
        dirs, reqs, sdirs = [], [], []
        saved_dirs = sv.get(tag + '_columns') if ctx.mode != 'run' else None
        for j, item in enumerate(plan_runs):
            if item[0] == 'GENERATE':
                cpath, csha = ctx.write_input('%s_controls_%02d.json' % (tag, j), item[1])
            else:
                cpath, csha = item
            dd = ctx.stage_dir('%s_columns_%02d' % (tag, j))
            outc = dd / 'columns'
            if saved_dirs is not None and len(saved_dirs) == len(plan_runs):
                outc = Path(saved_dirs[j])
            cargv = base + ['--controls', cpath, '--controls-sha256', csha] + extra_args + ['--outdir', outc]
            reqs.append(gen_request('%s_columns_%02d' % (tag, j), key, cargv, module_patches=[reuse_patch], mask=mask))  # c2v005: all generalized
            sdirs.append(dd)
            dirs.append(outc)
        # run in waves of `workers` processes (rule mode only; otherwise len==sequential)
        for k in range(0, len(reqs), max(1, workers)):
            ctx.run_stages(reqs[k:k + workers], sdirs[k:k + workers])
        if ctx.mode != 'run' and saved_dirs is not None and len(saved_dirs) != len(plan_runs):
            dirs = [Path(x) for x in saved_dirs]
        return dirs

    def manifest(tag, run_dirs):
        obj = {'runs': [{'directory': str(x), 'finish_sha256': ctx.finish_sha(x)} for x in run_dirs],
               'scope': 'c2v001 generated manifest for %s; complete %d columns required by the stage itself' % (tag, n)}
        return ctx.write_input('%s_manifest.json' % tag, obj)

    def generated_runs(tag, bracket_table, v001=False, split=True):
        """Group indices into column runs.  v001 supports only one global bracket per run."""
        runs = []
        if v001:
            groups = {}
            for i in range(n):
                groups.setdefault(tuple(bracket_table[str(i)]), []).append(i)
            for br, ids in sorted(groups.items(), key=lambda kv: kv[1][0]):
                for ch in (_chunks(ids, workers) if split else [ids]):
                    sol = dict(template)
                    sol['enthalpy_bracket'] = list(br)
                    runs.append(('GENERATE', {'radial_indices': ch, 'solver': sol, 'selection': '%s c2v001 rule' % tag}))
        else:
            for ch in (_chunks(list(range(n)), workers) if split else [list(range(n))]):
                runs.append(('GENERATE', {'radial_indices': ch, 'solver': dict(template),
                                          'column_enthalpy_brackets': {str(i): bracket_table[str(i)] for i in ch},
                                          'selection': '%s c2v001 rule' % tag}))
        return runs

    rule = brackets.get('rule')
    pinned = brackets.get('pinned_controls')
    checks = {}
    if rule:
        undecided = [k for k in ('rfs_factors', 'le_first_factors', 'le_next_factors') if _has_pending(rule[k])]
        if undecided:
            refuse('brackets.rule_factors', 'UNDECIDED_NGC_FIELD', 'brackets.rule_factors is NONE_IN_REVIEWED_CODE for %s (no ROOT_DECISIONS '
                   'row) and the call spec supplies none: %s' % (gname, undecided))

    # ---------------- FS pass, original K (columns v001 / rotation v001 / feedback v002, all gal_c2v003)
    if pinned:
        fs_plan = [(x['path'], verify_pin(x['path'], x['sha256'], 'pinned fs controls')) for x in pinned['fs']]
        merged = {}
        for x in pinned['fs']:
            c = json.loads(Path(x['path']).read_text())
            for i in c['radial_indices']:
                merged[str(i)] = c['solver']['enthalpy_bracket']
            if any(c['solver'][k] != template[k] for k in template if k != 'enthalpy_bracket'):
                checks.setdefault('fs_solver_block_differs', []).append(x['path'])
        ro = g.get('repro_rule_overrides', {}).get('fs_absolute_overrides', {})
        expect = {str(i): list(ro.get(str(i), template['enthalpy_bracket'])) for i in range(n)}
        checks['fs'] = {'checked': True, 'n': len(merged), 'bitwise_equal': merged == expect,
                        'rule': 'nominal template bracket + repro_rule_overrides.fs_absolute_overrides (last successful run wins)'}
    else:
        table = {str(i): list(rule['fs_absolute_overrides'].get(str(i), template['enthalpy_bracket'])) for i in range(n)}
        fs_plan = generated_runs('fs', table, v001=True)
        checks['fs'] = rule_vs_saved(g, 'fs', table)
    fs_dirs = column_pass('fs', 'columns_v001', [] + uvt_argv('columns_v001'), fs_plan)
    mpath, msha = manifest('fs', fs_dirs)
    d = ctx.stage_dir('fs_rotation')
    fs_rot = d / 'rotation' if ctx.mode == 'run' else ctx.saved_or('fs_rotation', d / 'rotation')
    fs_col_producer = producer_pin('columns_v001', producer(fs_dirs, 'columns_v001', 'config producer_pins.column_worker', 'fs_rotation'), uvt_extra)
    ctx.run_stages([gen_request('fs_rotation', 'rotation_v001', base + ['--column-manifest', mpath, '--column-manifest-sha256', msha,
                    '--mass-relative-tolerance', FA['mass_relative_tolerance'], '--outdir', fs_rot] + uvt_argv('rotation_v001'),
                    module_patches=[reuse_patch], mask=mask, producers={'column_worker': fs_col_producer})], [d])
    d = ctx.stage_dir('fs_feedback')
    fs_fb = d / 'feedback' if ctx.mode == 'run' else ctx.saved_or('fs_feedback', d / 'feedback')
    fs_rot_producer = producer_pin('rotation_v001', producer([fs_rot], 'rotation_v001', 'config producer_pins.rotation_worker', 'fs_feedback'), uvt_extra)
    ctx.run_stages([gen_request('fs_feedback', 'feedback_v002', base + ['--rotation-directory', fs_rot,
                    '--rotation-finish-sha256', ctx.finish_sha(fs_rot), '--wave-batch', FA['wave_batch'],
                    '--position-batch', FA['position_batch'], '--bessel-cache-entries', FA['bessel_cache_entries'],
                    '--outdir', fs_fb], module_patches=[reuse_patch], mask=mask, producers={'rotation_worker': fs_rot_producer})], [d])
    fs_fb_sha = ctx.finish_sha(fs_fb)
    percall['custody.fs_feedback_worker_sha256'] = producer([fs_fb], 'feedback_v002', 'config custody.fs_feedback_worker_sha256', 'rfs_columns')

    # ---------------- RFS columns, original K, refreshed field (columns v003 gal_c2v003): source of LE1 brackets
    H_fs = column_H(fs_dirs)
    rfs_args = ['--feedback-directory', fs_fb, '--feedback-finish-sha256', fs_fb_sha]
    if pinned:
        rfs_plan = [(x['path'], verify_pin(x['path'], x['sha256'], 'pinned rfs controls')) for x in pinned['rfs']]
        checks['rfs'] = bracket_check([x['path'] for x in pinned['rfs']], H_fs, LE_RULE_DEFAULTS['rfs_factors'],
                                      g.get('repro_rule_overrides', {}).get('rfs_factor_overrides', {}))
    else:
        if H_fs is None:
            rfs_plan = 'PENDING'
        else:
            require_bracket_source(H_fs, n, 'fs')
            table = rule_brackets(H_fs, rule['rfs_factors'], rule['rfs_factor_overrides'], range(n))
            checks['rfs'] = rule_vs_saved(g, 'rfs', table)
            rfs_plan = generated_runs('rfs', table)
    if rfs_plan == 'PENDING':
        rfs_dirs = ['PENDING(rfs columns)']
        ctx.records.append({'name': 'rfs_columns', 'executed': False, 'note': 'controls depend on fs column enthalpies (rule mode)'})
    else:
        rfs_dirs = column_pass('rfs', 'columns_v003', rfs_args + uvt_argv('columns_v003', fs_rot), rfs_plan)

    # ---------------- LE Picard passes (v005 / v005 / v004 + column mean v004, all gal_c2v003)
    field_dir, field_sha = fs_fb, fs_fb_sha
    field_rot = fs_rot  # C2V010 (u): the rotation the current field's feedback transformed
    field_worker = producer([fs_fb], 'feedback_v002', '--feedback-worker-sha256', 'le1 field')  # c2v004 (run: c2v003 value)
    prev_dirs = rfs_dirs
    prev_speeds = None
    final = None
    for p in range(1, P + 1):
        tag = 'le%d' % p
        last = (p == P)
        serial = last or bound is not None
        H_prev = column_H(prev_dirs) if all(isinstance(x, Path) for x in prev_dirs) else None
        factors = rule['le_first_factors'] if (rule and p == 1) else (rule['le_next_factors'] if rule else None)
        if pinned:
            plan = [(x['path'], verify_pin(x['path'], x['sha256'], 'pinned le controls')) for x in pinned['le'][p - 1]]
            checks[tag] = bracket_check([x['path'] for x in pinned['le'][p - 1]], H_prev,
                                        LE_RULE_DEFAULTS['le_first_factors'] if p == 1 else LE_RULE_DEFAULTS['le_next_factors'], {})
        elif H_prev is None:
            plan = 'PENDING'
        else:
            ov = rule['le_factor_overrides'].get(str(p), {})
            require_bracket_source(H_prev, n, 'rfs' if p == 1 else 'le%d' % (p - 1))
            table = rule_brackets(H_prev, factors, ov, range(n))
            checks[tag] = rule_vs_saved(g, tag, table)
            plan = generated_runs(tag, table, split=not serial)
        if plan == 'PENDING':
            ctx.records.append({'name': tag + '_columns', 'executed': False, 'note': 'controls depend on previous column enthalpies'})
            break
        cols = column_pass(tag, 'columns_v005', ['--feedback-directory', field_dir, '--feedback-finish-sha256', field_sha,
                           '--feedback-worker-sha256', field_worker, '--entropy-scale', efs] + uvt_argv('columns_v005', field_rot), plan)
        mpath, msha = manifest(tag, cols)
        d = ctx.stage_dir(tag + '_rotation')
        rot = d / 'rotation' if ctx.mode == 'run' else ctx.saved_or(tag + '_rotation', d / 'rotation')
        ctx.run_stages([gen_request(tag + '_rotation', 'rotation_v005', base + ['--column-manifest', mpath, '--column-manifest-sha256', msha,
                        '--feedback-directory', field_dir, '--feedback-finish-sha256', field_sha,
                        '--column-worker-sha256', producer(cols, 'columns_v005', '--column-worker-sha256', tag + '_rotation'),
                        '--feedback-worker-sha256', field_worker,
                        '--mass-relative-tolerance', FA['mass_relative_tolerance'], '--outdir', rot, '--entropy-scale', efs] + uvt_argv('rotation_v005', field_rot),
                        module_patches=[reuse_patch], mask=mask)], [d])
        pass_rec = {'pass': p, 'columns': [str(x) for x in cols], 'rotation': str(rot), 'field': str(field_dir)}
        rf = Path(rot) / 'finish.json'
        if rf.is_file():
            rfj = json.loads(rf.read_text())
            pass_rec.update(rotation_positive=rfj['positive_rotation_square'], minimum_rotation_square=rfj['minimum_rotation_square'],
                            nonpositive_indices=rfj['nonpositive_indices'], rotation_arrays={'path': rfj['arrays_path'], 'sha256': rfj['arrays_sha256']})
            if ctx.mode == 'run':
                pass_rec['rotation_array_content_digests'] = array_digests(rfj['arrays_path'])
        failures = []
        for x in cols:
            fx = Path(x) / 'finish.json'
            if fx.is_file():
                failures += json.loads(fx.read_text())['failures']
        pass_rec['column_failures'] = failures
        observe = len(cols) == 1 and (last or bound is not None or sp['numerics']['picard']['observe_every_pass'])
        speeds = None
        if observe:
            d = ctx.stage_dir(tag + '_column_mean')
            obsd = d / 'observation' if ctx.mode == 'run' else ctx.saved_or(tag + '_column_mean', d / 'observation')
            b, b_ok, b_st = gc_value(gc, 'observation.binding')  # c2v005: DDO154 == g['column_mean_binding'] (checked)
            if 'observation.binding' in gfields:  # C2V008 (a), c2v003b: the per-call column-mean binding
                b, b_ok = gfields['observation.binding'], True
            bpin = [str(b['path']), b['sha256']] if b_ok else ['NONE_IN_REVIEWED_CODE(observation.binding)', 'NONE_IN_REVIEWED_CODE']
            pins = [bpin, [str(Path(rot) / 'start.json'), ctx.finish_sha(rot, 'start.json')],
                    [str(Path(rot) / 'finish.json'), ctx.finish_sha(rot)],
                    [str(Path(cols[0]) / 'start.json'), ctx.finish_sha(cols[0], 'start.json')],
                    [str(Path(cols[0]) / 'finish.json'), ctx.finish_sha(cols[0])]]
            percall['custody.column_mean_input_pins'] = pins  # c2v004: was stage global PINS
            rot_worker = rotation_producer_pin(producer([rot], 'rotation_v005', 'config producer_pins.rotation_worker',
                                                        tag + '_column_mean'), uvt_extra)
            ctx.run_stages([gen_request(tag + '_column_mean', 'column_mean_v004', ['--outdir', obsd], tag=tag,
                                        producers={'rotation_worker': rot_worker})], [d])
            rp = Path(obsd) / 'result.json'
            if rp.is_file():
                res = json.loads(rp.read_text())
                pass_rec['column_mean'] = {'path': str(rp), 'sha256': sha256_file(rp), 'status': res['status']}
                if res['status'] == 'CONDITIONAL_PREPARATION_ROWS_NOT_CALIBRATION':
                    speeds = [r['speed_km_s'] for r in res['prediction']['rows']]  # c2v006: None on an N1 invalid row
                    pass_rec['rows'] = res['prediction']['rows']
                    if res['prediction'].get('invalid_rows') is not None:  # c2v006 (A4): only with the binding invalid_row_rule
                        pass_rec['invalid_rows'] = res['prediction']['invalid_rows']
                    pass_rec['nonaxisymmetric_residual_maxima'] = res['nonaxisymmetric_residual_maxima']
                    pass_rec['residual_units'] = res.get('residual_units')
                else:
                    pass_rec['column_mean_failure'] = res.get('failure')
        else:
            pass_rec['column_mean'] = 'NOT_OBSERVED (multi-run parallel pass or observe_every_pass false)'
        if speeds is not None and prev_speeds is not None:
            # c2v006: N1 invalid rows (speed None) are skipped; with no invalid row this is the c2v005 expression
            pass_rec['max_abs_change_km_s'] = max(abs(a - b) for a, b in zip(speeds, prev_speeds) if a is not None and b is not None)
        ctx.passes.append(pass_rec)
        ctx.event(event='pass_done', **{k: v for k, v in pass_rec.items() if k in ('pass', 'max_abs_change_km_s', 'rotation_positive')})
        stop = last or (bound is not None and pass_rec.get('max_abs_change_km_s') is not None and pass_rec['max_abs_change_km_s'] <= bound)
        if stop:
            final = pass_rec
            break
        prev_speeds = speeds
        d = ctx.stage_dir(tag + '_feedback')
        fb = d / 'feedback' if ctx.mode == 'run' else ctx.saved_or(tag + '_feedback', d / 'feedback')
        ctx.run_stages([gen_request(tag + '_feedback', 'feedback_v004', base + ['--rotation-directory', rot,
                        '--rotation-finish-sha256', ctx.finish_sha(rot), '--wave-batch', FA['wave_batch'],
                        '--position-batch', FA['position_batch'], '--bessel-cache-entries', FA['bessel_cache_entries'],
                        '--outdir', fb, '--current-feedback-directory', field_dir, '--current-feedback-finish-sha256', field_sha,
                        '--rotation-worker-sha256', producer([rot], 'rotation_v005', '--rotation-worker-sha256', tag + '_feedback'),
                        '--current-feedback-worker-sha256', field_worker],
                        module_patches=[reuse_patch], mask=mask)], [d])
        field_dir, field_sha = fb, ctx.finish_sha(fb)
        field_rot = rot  # C2V010 (u)
        field_worker = producer([fb], 'feedback_v004', '--feedback-worker-sha256', 'le%d field' % (p + 1))
        prev_dirs = cols
    info['bracket_rule_checks'] = checks
    info['producer_identity'] = producer_log
    info['galaxy_config']['stage_configs'] = [m for _, _, m in gc_written.values()]
    info['refusals'] = refusals
    info['percall_known'] = {k: v for k, v in percall.items()}
    if uvx is not None:  # C2V010 (u): tail-ON record (absent for tail OFF)
        info['uv_tail'] = uvx
    return info, final

def _cmd_run_ngc_cx3v005(spec_path, outdir):
    # C2V007 (a) F2 (c2v003c hunk @@ -1653): absolute outdir (stage children run with cwd=<stage dir>).  os.path.abspath
    # is lexical: it normalizes '.', '..', '//' and a trailing '/', and resolves no symlink.  A relative monitor/campaign
    # outdir resolves against the driver's inherited cwd, which is the monitor's.
    out = Path(os.path.abspath(outdir))
    if out.exists():
        print('REFUSED: outdir exists', file=sys.stderr)
        return 2
    out.mkdir(parents=True)
    t0 = time.monotonic()
    raw = Path(spec_path).read_bytes()
    spec_sha = sha256_bytes(raw)
    (out / 'inputs').mkdir()
    with open(out / 'inputs' / 'call_spec.json', 'xb') as f:
        f.write(raw)
    result = {'schema': RESULT_SCHEMA, 'call_spec_sha256': spec_sha, 'driver_sha256': sha256_file(__file__),
              'accepted_for_calibration': False, 'scored': False, 'valid': False, 'reasons': []}
    status = 'FAILED'
    ctx = None
    try:
        nspec = normalize_spec(json.loads(raw))
        if nspec.get('config') == 'NGC3198_C2V002':
            ngc_run_blocked(out, nspec, spec_sha, result)  # writes start/inputs, executes 0 stages, raises Blocked
        pins = all_static_pins(nspec)
        g = GALAXIES[nspec['galaxy']]
        _write_x(out / 'start.json', {'schema': RESULT_SCHEMA, 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                 'pid': os.getpid(), 'driver': str(Path(__file__).resolve()), 'driver_sha256': result['driver_sha256'],
                 'call_spec_sha256': spec_sha, 'normalized_spec': nspec, 'static_pins': pins,
                 'scope': 'Route-B m0 forward call; no observed velocity read, no score, no calibration admission.'})
        # c2v004/c2v005: fail closed before any stage on a binding blocker found from bytes (see binding_blockers);
        # NGC3198: execute_chain raises Blocked at the first remaining refusal, before any stage it would feed.
        _nodes = uvt_is_nodes(nspec['numerics'].get('uv_tail'))  # C2V010 r4
        bb = (binding_blockers() + (ro1_off_blockers() if route_a_ro1_workers(nspec) else [])) if 'uv_tail' not in nspec['numerics'] else (
            binding_blockers(dict(SCRIPTS, **uvt_active(_nodes)['scripts'])) + uvt_binding_blockers(_nodes))  # C2V010 (u): tail ON, active tables
        if bb:
            result['binding_blockers'] = bb
            raise Blocked(' | '.join(bb))
        sr = route_b_static_refusals(nspec, load_galaxy_config(nspec['galaxy'], nspec.get('member')))  # c2v005: empty for DDO154
        if sr:
            result['remaining_refusals'] = sr
            raise Blocked('REMAINING_REFUSALS: ' + ' | '.join('%s [%s] %s' % (r['where'], r['class'], r['refusal']) for r in sr))
        ctx = Ctx('run', nspec, out)
        ctx.log = open(out / 'progress.jsonl', 'x')
        info, final = execute_chain(ctx)
        result.update(galaxy=nspec['galaxy'], normalized_spec=nspec, identity=info, passes=ctx.passes)
        if final is None:
            result['reasons'].append('no final pass')
        else:
            result['final_pass'] = final['pass']
            # c2v003 (CHECK_V001 further defect 2): explicit convergence-bound outcome.
            bnd = nspec['numerics']['picard']['speed_change_bound_km_s']
            chg = final.get('max_abs_change_km_s')
            result['picard_bound_met'] = None if bnd is None or chg is None else bool(chg <= bnd)
            rows_ok, invalid_rows = final_rows_check(final, g['n_queries'], nspec)  # c2v006 (A4/N1)
            if rows_ok:
                if nspec.get('coefficient_alternative')=='STAGE0_GRID_OUTER':
                    reg=_pinned_json(STAGE0_SLOTS_PIN[0],STAGE0_SLOTS_PIN[1],'STAGE0 alternative registration')
                    alt=next(a for a in reg['alternatives']['declared'] if a['name']=='STAGE0_GRID_OUTER')
                    result['alternative_label']={'name':'STAGE0_GRID_OUTER','status':'DECLARED_ALTERNATIVE_NOT_HEADLINE','scoring_scope':alt['scoring_scope']}
                result['rows'] = final['rows']
                result['speeds_km_s'] = {r['id']: r['speed_km_s'] for r in final['rows']}
                if invalid_rows is not None:
                    result['invalid_rows'] = invalid_rows
                    result['headline_rule'] = ('N1/A4: rows valid=false (QUERY_INSIDE_INNERMOST_NODE, QUERY_BEYOND_OUTER_GAS_CUT, QUERY_OUTSIDE_RETAINED_SUPPORT) count as misses; invalid entries '
                                               'never pass; they do not invalidate the call')
                if nspec.get('member') is not None or nspec['physical'].get('entropy_K_member', 'N4_PRIMARY_64_OVER_121') != 'N4_PRIMARY_64_OVER_121':
                    result['alternative_label'] = {'member': nspec.get('member'), 'entropy_K_member': nspec['physical'].get('entropy_K_member'),
                                                   'status': 'DECLARED_ALTERNATIVE_NOT_HEADLINE'}
                result['valid'] = (not final['column_failures']) and final.get('rotation_positive') is True
                if not result['valid']:
                    result['reasons'].append('final pass column failures or nonpositive rotation')
            else:
                result['reasons'].append('final column mean did not return %d rows: %s' % (g['n_queries'], final.get('column_mean')))
            diag = {'nonaxisymmetric_residual_maxima': final.get('nonaxisymmetric_residual_maxima'),
                    'residual_units': final.get('residual_units'),
                    'stored_residual_arrays': {'rotation_arrays': final.get('rotation_arrays'),
                                               'keys': ['angular_radial_residual', 'angular_vertical_residual', 'angular_azimuthal_residual',
                                                        'Phi_R_full', 'Phi_z_full', 'base_residual_r0']},
                    'per_pass_maxima': [{'pass': x['pass'], 'maxima': x.get('nonaxisymmetric_residual_maxima')} for x in ctx.passes]}
            if final.get('rotation_arrays'):
                try:
                    diag['azimuthal_harmonics'] = harmonic_diagnostic(final['rotation_arrays']['path'])
                except Exception as exc:
                    diag['azimuthal_harmonics'] = 'unavailable: %s' % exc
            result['residual_diagnostics'] = diag
        status = 'COMPLETED' if result['valid'] else 'COMPLETED_INVALID'
    except Refusal as exc:
        status = 'REFUSED'
        result['reasons'].append(str(exc))
    except Blocked as exc:
        status = 'BLOCKED'
        result['reasons'].append(str(exc))
    except RouteANoFixedPoint as exc:  # C2V007 (a) F1 (c2v003c hunk @@ -1715): a model outcome, not BLOCKED
        status = 'ROUTE_A_NO_FIXED_POINT'
        result['reasons'].append(str(exc))
    except StageFailed as exc:
        status = 'FAILED_AT_STAGE'
        result['reasons'].append(str(exc))
    except Exception as exc:
        import traceback
        status = 'FAILED'
        result['reasons'].append('%s: %s' % (type(exc).__name__, exc))
        result['traceback'] = traceback.format_exc()
    if ctx is not None:
        if ctx.route_a_outcome is not None:  # C2V007 (a) F1 (c2v003c hunk @@ -1724): outcome + converged iteration, every status
            result['route_a_outcome'] = ctx.route_a_outcome
        if ctx.geometry is not None:  # C2V008 (a): per-call geometry record and the stage-admission probe, every status
            result['geometry'] = ctx.geometry
        result['stage_records'] = ctx.records
        if ctx.uv_tail is not None:  # C2V010 (u): tail record + each tail stage's finish.json tail record, every status
            result['uv_tail'] = dict(ctx.uv_tail, stage_records=uvt_stage_records(ctx.records))
        if ctx.spec.get('reference_compare'):
            result['reference_comparison'] = reference_comparison(ctx.records, GALAXIES[ctx.spec['galaxy']].get('saved_runs', {}))
            result['deciding_test'] = deciding_test_verdict(result['reference_comparison'], ctx.passes)  # c2v004
        if result.get('passes') is None:
            result['passes'] = ctx.passes
        if ctx.log is not None:
            ctx.log.close()
    result['status'] = status
    result['elapsed_seconds'] = time.monotonic() - t0
    rsha = _write_x(out / 'result.json', result)
    _write_x(out / 'finish.json', {'status': status, 'valid': result['valid'], 'result_path': str(out / 'result.json'),
             'result_sha256': rsha, 'elapsed_seconds': result['elapsed_seconds'], 'reasons': result['reasons'],
             'retries': 0, 'partial_outputs_preserved': True})
    return 0 if status in ('COMPLETED', 'COMPLETED_INVALID') else 3



# Dispatch0548: registered coefficient sensitivity, isolated from the headline.
STAGE0_GRID_PIN = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage0_grid_gate_c2/candidate/STAGE0_POOLED8_CANDIDATE_GRID_V001.npz', 'bdb9016c97685d72de8fb93d43cb6ce5baff42b64e59f99af14fb310c8317ca5')
STAGE0_SLOTS_PIN = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json', 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969')
V011_STAGE0_PINS = {'prep': ['/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/stage0_alternative/sources/ngc_actual_initial_source_preparation_cx3v011_cx3v005.py', 'd578889248f0e2f7a40ded8c6645a14811ac8ba59c192e4e6ef243dde06db5f8'], 'prediction': ['/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/route_a/ngc_coupled_fourier_hi_prediction_cx3v011.py', '7ae28901023974005fac9a5dc4126941371b1522837b02c81cdb5811573c1e98'], 'binding': ['/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/route_a/ngc_composite_full_coupled_binding_uvtail_ro1_cx3v011.py', '9b5ce82adea46c8e660f44b0fc91e8dbe5d0616cc1de1fd4467878ef3b5c0668'], 'worker': ['/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/stage0_alternative/sources/ngc43_coupled_root_worker_uvtail_ro1_cx3v011_r5cx3v001_cx3v005.py', 'f7c8fb43852eece4cddf4aac769aab7f91eab4445575296fb19a4e5454677f9e'], 'worker_parallel': ['/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/stage0_alternative/sources/ngc43_coupled_root_worker_parallel_uvtail_ro1_cx3v011_r5cx3v001_cx3v005.py', '908c9b4b0898136e00ea253be60be3f0e5763237234385cb76e8b3158b7f4a9b'], 'grid_cut': ['/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_grid_cut_cx3v001_cx3v005.py', '5d037291c8d683d7921f38365640bf41502216a67a5ed6ca84986aa671faf353'], 'seed_v002': ['/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_a_freeboundary_c2/seed_v002/DEFAULT/seed/NGC3198_ROUTE_A_A2F10_SEED_C2V002_DEFAULT.json', '88ef386d2bd4e14be23709d21b23fd3b7b57a2cc85adcc09d6a0459bcbc108da'], 'a2_coefficients': ['/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz', '2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7'], 'route_b_binding': ['/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/ngc_uvt_route_b_binding_cx3v006_r5cx3v001_cx3v005.py', 'aee7af1286f2d3d9d52117d6b4d4ae82e31d8776af4a4b0a6da7cee96be12fb3'], 'manifest_writer': ['/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/stage0_alternative/sources/ngc_route_a_tail_manifest_cx3v011_r5cx3v001_cx3v005.py', '443d9fdca2cd28e6e49a2b55f9e60d27bddf4b4a8170740ce2b1bb2b5e99eca8'], 'stage0_coefficients': ['/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage0_grid_gate_c2/candidate/STAGE0_POOLED8_CANDIDATE_GRID_V001.npz', 'bdb9016c97685d72de8fb93d43cb6ce5baff42b64e59f99af14fb310c8317ca5']}

def _ngc_v011_stage0_flag(spec):
    if 'coefficient_alternative' not in spec:return False
    if spec.get('coefficient_alternative')!='STAGE0_GRID_OUTER':raise Refusal('UNKNOWN_COEFFICIENT_ALTERNATIVE')
    if spec.get('galaxy')!='NGC3198' or not isinstance(spec.get('numerics'),dict) or 'uv_tail' not in spec['numerics']:
        raise Refusal('STAGE0_GRID_OUTER_NGC_TAIL_ON_ONLY')
    if spec.get('member') is not None:raise Refusal('STAGE0_GRID_OUTER_HEADLINE_GEOMETRY_ONLY')
    doc=_pinned_json(STAGE0_SLOTS_PIN[0],STAGE0_SLOTS_PIN[1],'STAGE0 alternative registration')
    alt=next((a for a in doc['alternatives']['declared'] if a['name']=='STAGE0_GRID_OUTER'),None)
    if not isinstance(alt,dict) or alt.get('coefficient_grid_pin')!={'path':str(STAGE0_GRID_PIN[0]),'sha256':STAGE0_GRID_PIN[1]} or alt.get('headline') is not False:
        raise Refusal('STAGE0_GRID_OUTER_REGISTRATION_MISMATCH')
    return True

@contextlib.contextmanager
def _ngc_v011_stage0_context(enabled):
    global V011_PINS,GALAXIES
    if not enabled:
        yield
        return
    prior_pins,prior_galaxies=V011_PINS,GALAXIES
    try:
        V011_PINS=V011_STAGE0_PINS
        ngc=dict(GALAXIES['NGC3198'])
        grids=dict(ngc['decided_coefficient_grids']);grids[STAGE0_GRID_PIN[1]]=(Path(STAGE0_GRID_PIN[0]),'STAGE0_GRID_OUTER explicit alternative only')
        ngc['decided_coefficient_grids']=grids;GALAXIES=dict(GALAXIES,NGC3198=ngc)
        yield
    finally:V011_PINS,GALAXIES=prior_pins,prior_galaxies


# Dispatch0563/A73: NGC RO1 admission uses the selected NGC worker/binding
# pair. The inherited r5/DDO RO1 implementation and all original source text
# remain unchanged; outside this scoped context delegation is exact.
_V010_RO1_OUTCOME_CX3R005 = ro1_outcome

def ro1_outcome(ra, pred, result_path, converged):
    if not _NGC_V011_ACTIVE:
        return _V010_RO1_OUTCOME_CX3R005(ra, pred, result_path, converged)
    block, fired = _V010_RO1_OUTCOME_CX3R005(ra, pred, result_path, converged)
    # V011_PINS is already selected by the headline/Stage0 context and its
    # worker and binding bytes are checked on context entry. The parent gate
    # still checks binding-path custody and all convergence/event conditions.
    allowed_workers = (V011_PINS['worker'][1], V011_PINS['worker_parallel'][1])
    expected_binding = V011_PINS['binding'][1]
    if block['armed'] and (block['worker_sha256'] not in allowed_workers
                           or block['binding_sha256'] != expected_binding):
        block = dict(block, armed=False, fired=False, events=[],
                     worker_sha256=None, binding_sha256=None)
        rec = pred.get('route_a_readout_refusal')
        if rec is not None:
            block['inadmissible_record'] = rec
        return block, False
    return block, fired


# Dispatch0570/A77: strict records only inside headline/Stage0 NGC contexts.
# Every original r005 byte is retained. All inactive calls delegate unchanged.
_CX3R005_RO1_OUTCOME = ro1_outcome
_CX3R005_ROUTE_A_OUTCOME_RECORD = route_a_outcome_record
_CX3R005_NGC_READ_ROUTE_A_RESULT = ngc_read_route_a_result

class _NGCObjectPairsCX3R006(list):
    """Keep every decoded object member until full root-to-leaf paths exist."""

def _ngc_ro1_record_load_cx3r006(path, label):
    try:
        tree = json.loads(Path(path).read_text(), object_pairs_hook=_NGCObjectPairsCX3R006)
    except (OSError, ValueError, TypeError) as exc:
        raise Refusal('NGC_RO1_RECORD_UNREADABLE: %s file=%s (%s)' %
                      (label, json.dumps(str(path)), type(exc).__name__)) from exc
    def unpack(value, at):
        if isinstance(value, _NGCObjectPairsCX3R006):
            result, seen = {}, {}
            for index, (key, child) in enumerate(value):
                # JSON-escaped keys plus zero-based object-member indexes
                # distinguish duplicate occurrences even under duplicate parents.
                here = at + '[' + json.dumps(key, ensure_ascii=True) + ']@member[' + str(index) + ']'
                if key in seen:
                    raise Refusal('NGC_JSON_DUPLICATE_KEY: %s file=%s first_path=%s second_path=%s' %
                                  (label, json.dumps(str(path)), seen[key], here))
                seen[key] = here
                result[key] = unpack(child, here)
            return result
        if isinstance(value, list):
            return [unpack(child, at + '[' + str(index) + ']') for index, child in enumerate(value)]
        return value
    result = unpack(tree, '$')
    if not isinstance(result, dict):
        raise Refusal('NGC_RO1_RECORD_OBJECT_REQUIRED: %s file=%s path=$' % (label, json.dumps(str(path))))
    return result

def _ngc_ro1_prediction_cx3r006(ra, result_path):
    outer = ra.get('result')
    pred = outer.get('result') if isinstance(outer, dict) else None
    if not isinstance(pred, dict):
        raise Refusal('NGC_ROUTE_A_PREDICTION_OBJECT_REQUIRED: file=%s path=$["result"]["result"]' % json.dumps(str(result_path)))
    return pred

def ro1_outcome(ra, pred, result_path, converged):
    if not _NGC_V011_ACTIVE:
        return _CX3R005_RO1_OUTCOME(ra, pred, result_path, converged)
    # Re-read original bytes even if a caller already permissively decoded them.
    # The parsed record, not that lossy dictionary, supplies the admitted inputs.
    ra = _ngc_ro1_record_load_cx3r006(result_path, 'route-A result')
    pred = _ngc_ro1_prediction_cx3r006(ra, result_path)
    start_path = Path(result_path).parent / 'start.json'
    start = _ngc_ro1_record_load_cx3r006(start_path, 'route-A start')
    worker = start.get('worker_pin')
    if isinstance(worker, (list, dict)):
        raise Refusal('NGC_RO1_WORKER_PIN_TYPE: file=%s path=$["worker_pin"]; expected string, got %s' %
                      (json.dumps(str(start_path)), type(worker).__name__))
    pins = ra.get('input_pins') or {}
    bind_path, bind_sha = V011_PINS['binding']
    armed = (isinstance(pins, dict) and pins.get(str(Path(bind_path).resolve())) == bind_sha
             and isinstance(worker, str) and worker in (V011_PINS['worker'][1], V011_PINS['worker_parallel'][1]))
    block = {'rule': 'RO1', 'fired': False, 'events': [], 'armed': armed,
             'worker_sha256': worker if armed else None, 'binding_sha256': bind_sha if armed else None}
    rec = pred.get('route_a_readout_refusal')
    if rec is None:
        return block, False
    ok = (armed and converged is True and isinstance(rec, dict) and rec.get('code') == RO1_CODE and rec.get('refusal') in RO1_MESSAGES
          and rec.get('after_convergence') is True and pred.get('readout_status') == RO1_CODE
          and pred.get('predictions_available') is False and 'rows' in pred and pred.get('rows') is None)
    if ok:
        block.update(fired=True, events=[dict(rec)])
    else:
        block['inadmissible_record'] = rec
    return block, ok

def route_a_outcome_record(ra, result_path):
    if not _NGC_V011_ACTIVE:
        return _CX3R005_ROUTE_A_OUTCOME_RECORD(ra, result_path)
    ra = _ngc_ro1_record_load_cx3r006(result_path, 'route-A result')
    return _CX3R005_ROUTE_A_OUTCOME_RECORD(ra, result_path)

def _ngc_read_route_a_result_strict_cx3r006(result_path, finish_path, manifest_path=None):
    """Read a (future) NGC43 route-A result: 43 speeds keyed NGC3198-Q01..Q43 in manifest order,
    validity, and DIAGNOSTIC m>=1 content of the azimuth-resolved trial (no acceptance threshold).
    Reads only the worker's own outputs and the target-free manifest."""
    import numpy as np
    manifest_path = manifest_path or NGC_DATA['manifest'][0]
    man = json.loads(Path(manifest_path).read_text())
    ids = [r['query_id'] for r in man['rows']]
    rad = {r['query_id']: r['Rad_text'] for r in man['rows']}
    reasons = []
    fin = json.loads(Path(finish_path).read_text())
    if fin.get('status') != 'RETURNED_ACTUAL_RESULT':
        reasons.append('worker status %s' % fin.get('status'))
    if sha256_file(result_path) != fin.get('result_sha256'):
        reasons.append('result sha256 differs from worker finish.json')
    ra = _ngc_ro1_record_load_cx3r006(result_path, 'route-A result')
    x = _ngc_ro1_prediction_cx3r006(ra, result_path)
    sfp = x.get('source_fixed_point') if isinstance(x.get('source_fixed_point'), dict) else {}
    ro1, ro1_fired = ro1_outcome(ra, x, result_path, sfp.get('converged_finite_fixed_point') is True
                                 and (sfp.get('checkpoint') or {}).get('outcome') == ROUTE_A_CONVERGED)
    if ro1_fired:  # RO1 (A49.3): converged fixed point, readout refused: rows None recorded (no TypeError), not valid
        reasons.append('RO1: route-A circular-trial readout refused after a converged fixed point (%s); no route-A rows'
                       % ro1['events'][0].get('refusal'))
        return {'rows': None, 'speeds_km_s': None, 'valid': False, 'reasons': reasons, 'ro1': ro1,
                'validity_definition': 'worker RETURNED_ACTUAL_RESULT, result sha matches, 43 manifest ids in order, finite speeds, '
                                       'converged source fixed point, predictions_available',
                'm_ge_1_diagnostics': None, 'dynamics_status': x.get('dynamics_status'), 'accepted_for_calibration': False,
                'route': 'ROUTE_A_ONLY (route B blocked)'}
    if not isinstance(x.get('rows'), list):
        raise Refusal('NGC_ROUTE_A_ROWS_REQUIRED: file=%s path=$["result"]["result"]["rows"]; RO1 did not fire' % json.dumps(str(result_path)))
    rows = x['rows']
    if [r['id'] for r in rows] != ids:
        reasons.append('row ids are not the 43 manifest ids in order')
    speeds = [r['speed_km_s'] for r in rows]
    if not all(isinstance(v, (int, float)) and math.isfinite(v) for v in speeds):
        reasons.append('nonfinite speed')
    if x.get('source_fixed_point', {}).get('converged_finite_fixed_point') is not True:
        reasons.append('route-A source fixed point not converged')
    if x.get('predictions_available') is not True:
        reasons.append('predictions_available is not True')
    per_q, gmax = [], {}
    for q in x.get('query_physics', []):
        nodes = q['nodes']
        n = len(nodes)
        phi = np.array([nd['phi_rad'] for nd in nodes])
        v = np.array([nd['v'] for nd in nodes], dtype=float)
        equal = bool(np.allclose(phi, 2 * np.pi * np.arange(n) / n, rtol=0, atol=1e-12))
        F = np.abs(np.fft.rfft(v))
        ratios = {'m%d' % m: (float(F[m] / F[0]) if F[0] > 0 else None) for m in range(1, len(F))}
        for k, val in ratios.items():
            if val is not None:
                gmax[k] = max(gmax.get(k, 0.0), val)
        eul = np.array([nd['Euler_covector_residual_R_phi_z'] for nd in nodes], dtype=float)
        cont = [abs(r) for nd in nodes for r in nd['mass_continuity']['fractional_density_rate_per_s']]
        per_q.append({'id': q['id'], 'n_azimuths': n, 'equal_angle_nodes': equal,
                      'speed_m_s_azimuth_harmonic_ratio': ratios,
                      'speed_m_s_azimuth_range': float(v.max() - v.min()),
                      'Euler_residual_abs_max_R_phi_z': [float(a) for a in np.max(np.abs(eul), axis=0)],
                      'continuity_fractional_rate_abs_max_per_s': float(max(cont)) if cont else None})
    valid = not reasons and len(rows) == 43
    return {'rows': [{'id': r['id'], 'Rad_text_kpc': rad.get(r['id']), 'speed_km_s': r['speed_km_s']} for r in rows],
            'speeds_km_s': {r['id']: r['speed_km_s'] for r in rows}, 'valid': valid, 'reasons': reasons,
            'validity_definition': 'worker RETURNED_ACTUAL_RESULT, result sha matches, 43 manifest ids in order, finite speeds, '
                                   'converged source fixed point, predictions_available',
            'm_ge_1_diagnostics': {'quantity': '|FFT_m(v)|/|FFT_0(v)| of the circular trial speed over the observation azimuths; '
                                               'max |Euler residual| (R,phi,z) and |continuity rate| per query',
                                   'global_max_harmonic_ratio': gmax, 'per_query': per_q, 'status': 'DIAGNOSTIC_ONLY'},
            'dynamics_status': x.get('dynamics_status'), 'accepted_for_calibration': False, 'route': 'ROUTE_A_ONLY (route B blocked)'}

def ngc_read_route_a_result(result_path, finish_path, manifest_path=None):
    if not _NGC_V011_ACTIVE:
        return _CX3R005_NGC_READ_ROUTE_A_RESULT(result_path, finish_path, manifest_path)
    return _ngc_read_route_a_result_strict_cx3r006(result_path, finish_path, manifest_path)



# BEGIN DISPATCH0581 CX3R007 SCOPED RECORD SUCCESSOR
# Dispatch0581/A80: operation-scoped strict records, no shared-module patch.
import functools as _cx3r007_functools

_NGC_RECORD_DIGESTS_CX3R007 = None
_NGC_RECORD_SELECTION_CX3R007 = False
_NGC_RECORD_DIGEST_CAP_CX3R007 = 64 * 1024 * 1024
_CX3R006_SHA256_FILE = sha256_file
_CX3R006_NGC_CONTEXT = _ngc_v011_context

def _ngc_records_active_cx3r007():
    return _NGC_V011_ACTIVE or _NGC_RECORD_SELECTION_CX3R007

@contextlib.contextmanager
def _ngc_record_operation_cx3r007():
    global _NGC_RECORD_DIGESTS_CX3R007
    owned = _NGC_RECORD_DIGESTS_CX3R007 is None
    if owned:
        _NGC_RECORD_DIGESTS_CX3R007 = {'lexical': {}, 'resolved': {}, 'bytes': 0}
    try:
        yield
    finally:
        if owned:
            _NGC_RECORD_DIGESTS_CX3R007 = None

def _ngc_record_identity_cx3r007(path):
    return os.path.abspath(os.fspath(path)), str(Path(path).resolve())

def _ngc_note_record_cx3r007(identity, digest):
    state = _NGC_RECORD_DIGESTS_CX3R007
    if state is None:
        raise Refusal('NGC_RECORD_OPERATION_REQUIRED')
    lexical, resolved = identity
    old = state['lexical'].get(lexical)
    if old is not None and old != (resolved, digest):
        raise Refusal('NGC_RECORD_CHANGED: file=%s; lexical identity or bytes changed' % json.dumps(lexical))
    if resolved in state['resolved'] and state['resolved'][resolved] != digest:
        raise Refusal('NGC_RECORD_CHANGED: file=%s; resolved bytes changed' % json.dumps(resolved))
    if old is None:
        charge = len(lexical.encode('utf-8')) + len(resolved.encode('utf-8')) + 256
        if state['bytes'] + charge > _NGC_RECORD_DIGEST_CAP_CX3R007:
            raise Refusal('NGC_RECORD_DIGEST_CAP: 64 MiB operation metadata limit')
        state['bytes'] += charge
        state['lexical'][lexical] = (resolved, digest)
        state['resolved'][resolved] = digest

class _NGCRecordBytesCX3R007(bytes):
    pass

class _NGCRecordTextCX3R007(str):
    pass

def _ngc_record_bytes_cx3r007(path):
    before = _ngc_record_identity_cx3r007(path)
    raw = Path(path).read_bytes()
    if _ngc_record_identity_cx3r007(path) != before:
        raise Refusal('NGC_RECORD_CHANGED_DURING_READ: file=%s' % json.dumps(before[0]))
    digest = hashlib.sha256(raw).hexdigest()
    _ngc_note_record_cx3r007(before, digest)
    out = _NGCRecordBytesCX3R007(raw)
    out.record_path, out.record_sha256 = before[0], digest
    return out

def _ngc_record_text_cx3r007(path, encoding=None, errors=None):
    raw = _ngc_record_bytes_cx3r007(path)
    import io
    with io.TextIOWrapper(io.BytesIO(raw), encoding=encoding, errors=errors) as stream:
        value = stream.read()
    out = _NGCRecordTextCX3R007(value)
    out.record_path, out.record_sha256 = raw.record_path, raw.record_sha256
    return out

class _NGCPairsCX3R007(list):
    pass

def _ngc_validate_row_elements_cx3r007(rows, source, at):
    if rows is None:
        return
    if not isinstance(rows, list):
        raise Refusal('NGC_ROW_LIST_REQUIRED: file=%s path=%s' % (json.dumps(source), at))
    for index, row in enumerate(rows):
        where = at + '[' + str(index) + ']'
        if not isinstance(row, dict):
            raise Refusal('NGC_ROW_OBJECT_REQUIRED: file=%s path=%s' % (json.dumps(source), where))
        for key in ('id', 'speed_km_s'):
            if key not in row:
                raise Refusal('NGC_ROW_FIELD_REQUIRED: file=%s path=%s[%s]' % (json.dumps(source), where, json.dumps(key)))
        if not isinstance(row['id'], str) or not row['id']:
            raise Refusal('NGC_ROW_ID_TYPE: file=%s path=%s["id"]' % (json.dumps(source), where))
        speed = row['speed_km_s']
        if speed is not None and (isinstance(speed, bool) or not isinstance(speed, (int, float))):
            raise Refusal('NGC_ROW_SPEED_TYPE: file=%s path=%s["speed_km_s"]' % (json.dumps(source), where))
    # Nonfinite numbers/null retain the caller's registered validity rule.

def _ngc_validate_record_rows_cx3r007(value, source):
    if not isinstance(value, dict):
        return
    outer = value.get('result')
    pred = outer.get('result') if isinstance(outer, dict) else None
    if isinstance(pred, dict) and 'rows' in pred:
        _ngc_validate_row_elements_cx3r007(pred['rows'], source, '$["result"]["result"]["rows"]')
    pred = value.get('prediction')
    if value.get('status') == 'CONDITIONAL_PREPARATION_ROWS_NOT_CALIBRATION':
        if not isinstance(pred, dict):
            raise Refusal('NGC_COLUMN_MEAN_PREDICTION_REQUIRED: file=%s path=$["prediction"]' % json.dumps(source))
        if not isinstance(pred.get('rows'), list):
            raise Refusal('NGC_COLUMN_MEAN_ROWS_REQUIRED: file=%s path=$["prediction"]["rows"]' % json.dumps(source))
    if isinstance(pred, dict) and 'rows' in pred:
        _ngc_validate_row_elements_cx3r007(pred['rows'], source, '$["prediction"]["rows"]')

def _ngc_json_loads_cx3r007(data, *args, **kwargs):
    source = getattr(data, 'record_path', '<in-memory JSON>')
    options = dict(kwargs)
    options['object_pairs_hook'] = _NGCPairsCX3R007
    try:
        tree = json.loads(data, *args, **options)
        # Iterative reconstruction retains full paths without Python recursion.
        holder = [None]
        stack = [(tree, '$', holder, 0)]
        while stack:
            value, at, parent, slot = stack.pop()
            if isinstance(value, _NGCPairsCX3R007):
                result, seen, children = {}, {}, []
                parent[slot] = result
                for index, (key, child) in enumerate(value):
                    here = at + '[' + json.dumps(key, ensure_ascii=True) + ']@member[' + str(index) + ']'
                    if key in seen:
                        raise Refusal('NGC_JSON_DUPLICATE_KEY: file=%s first_path=%s second_path=%s' % (json.dumps(source), seen[key], here))
                    seen[key] = here
                    children.append((child, here, result, key))
                stack.extend(reversed(children))
            elif isinstance(value, list):
                result = [None] * len(value)
                parent[slot] = result
                stack.extend((child, at + '[' + str(index) + ']', result, index) for index, child in reversed(list(enumerate(value))))
            else:
                parent[slot] = value
        value = holder[0]
        _ngc_validate_record_rows_cx3r007(value, source)
        return value
    except json.JSONDecodeError as exc:
        raise Refusal('NGC_JSON_PARSE_REFUSED: file=%s line=%s column=%s' % (json.dumps(source), exc.lineno, exc.colno)) from exc
    except RecursionError as exc:
        raise Refusal('NGC_JSON_DEPTH_REFUSED: file=%s path=$' % json.dumps(source)) from exc

def _ngc_checkpoint_read_cx3r007(reader, path, *args, **kwargs):
    raw = _ngc_record_bytes_cx3r007(path)
    snapshot = _ngc_json_loads_cx3r007(raw)
    result = reader(path, *args, **kwargs)
    _ngc_record_bytes_cx3r007(path)
    canonical = json.dumps(result, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('ascii') + b'\n'
    if hashlib.sha256(canonical).hexdigest() != raw.record_sha256 or result != snapshot:
        raise Refusal('NGC_CHECKPOINT_READER_SNAPSHOT_MISMATCH: file=%s' % json.dumps(str(path)))
    return result

def sha256_file(path):
    if not _ngc_records_active_cx3r007():
        return _CX3R006_SHA256_FILE(path)
    with _ngc_record_operation_cx3r007():
        before = _ngc_record_identity_cx3r007(path)
        digest = _CX3R006_SHA256_FILE(path)
        if _ngc_record_identity_cx3r007(path) != before:
            raise Refusal('NGC_RECORD_CHANGED_DURING_HASH: file=%s' % json.dumps(before[0]))
        _ngc_note_record_cx3r007(before, digest)
        return digest

@contextlib.contextmanager
def _ngc_v011_context():
    with _ngc_record_operation_cx3r007():
        with _CX3R006_NGC_CONTEXT():
            yield

@contextlib.contextmanager
def _ngc_selected_record_scope_cx3r007(path, raw):
    global _NGC_RECORD_SELECTION_CX3R007
    prior = _NGC_RECORD_SELECTION_CX3R007
    with _ngc_record_operation_cx3r007():
        _NGC_RECORD_SELECTION_CX3R007 = True
        try:
            identity = _ngc_record_identity_cx3r007(path)
            _ngc_note_record_cx3r007(identity, hashlib.sha256(raw).hexdigest())
            data = _NGCRecordBytesCX3R007(raw)
            data.record_path = identity[0]
            _ngc_json_loads_cx3r007(data)
            yield
        finally:
            _NGC_RECORD_SELECTION_CX3R007 = prior

def _ngc_scoped_callable_cx3r007(original, strict):
    @_cx3r007_functools.wraps(original)
    def scoped(*args, **kwargs):
        if not _ngc_records_active_cx3r007():
            return original(*args, **kwargs)
        with _ngc_record_operation_cx3r007():
            return strict(*args, **kwargs)
    scoped._cx3r007_original = original
    scoped._cx3r007_strict = strict
    return scoped

def _ngc_validate_manifest_rows_cx3r007(man, source):
    if not isinstance(man, dict) or not isinstance(man.get('rows'), list):
        raise Refusal('NGC_MANIFEST_ROWS_REQUIRED: file=%s path=$["rows"]' % json.dumps(str(source)))
    for index, row in enumerate(man['rows']):
        at = '$["rows"][%d]' % index
        if not isinstance(row, dict):
            raise Refusal('NGC_MANIFEST_ROW_OBJECT_REQUIRED: file=%s path=%s' % (json.dumps(str(source)), at))
        for key in ('query_id', 'Rad_text'):
            if key not in row or not isinstance(row[key], str) or not row[key]:
                raise Refusal('NGC_MANIFEST_ROW_FIELD_REQUIRED: file=%s path=%s[%s]' % (json.dumps(str(source)), at, json.dumps(key)))


def _cx3r007_strict_exec_verified_L577(path, sha, name):
    """Execute a pinned module from the exact bytes that were hashed (no reread)."""
    import types
    raw = _ngc_record_bytes_cx3r007(Path(path))
    if sha256_bytes(raw) != sha:
        raise Refusal('Pin mismatch on load: %s' % path)
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), module.__dict__)
    return module

def _cx3r007_strict_stage_main_L791(request_path):
    request = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(request_path)))
    script, sha = (request['script'], request['script_sha256'])
    _install_hooks(request)
    module = exec_verified(script, sha, 'c2v001_stage_' + Path(script).stem)
    for name, value in request.get('stage_globals', {}).items():
        if name not in module.__dict__:
            raise ValueError('Stage override target absent: ' + name)
        module.__dict__[name] = _decode_value(value)
    for gname, items in request.get('stage_dict_items', {}).items():
        target = module.__dict__.get(gname)
        if not isinstance(target, dict):
            raise ValueError('Stage dict override target absent: ' + gname)
        for key, pin in items.items():
            old = target.get(key)
            if not (isinstance(old, tuple) and len(old) == 2):
                raise ValueError('Stage dict override entry absent: %s[%s]' % (gname, key))
            if sha256_file(pin['path']) != pin['sha256']:
                raise ValueError('Stage dict override pin mismatch: ' + pin['path'])
            target[key] = (Path(pin['path']), pin['sha256'])
    sys.argv = [script] + list(request['argv'])
    module.main()
    return 0

def _cx3r007_strict_normalize_uv_tail_L894(raw, ngc=False):
    """C2V010: numerics.uv_tail = the tail library's configuration object (UNT_UV_TAIL_CONFIG_C2V001; strict keys, checked by
    the pinned library's own normalize_config).  enabled must be true: a tail-OFF call omits the block (root A45 N3: in tail-OFF
    mode v010 constructs no TailBoundary).  source_rule continuum_v001, or (r4) nodes_v001 with a composite ext_grid object (T2 only;
    DDO154; the nodes successors; ext grid checked at planning).  eps_/lo_certificate: {path, sha256} (verified from
    bytes at planning and at every build), NONE_TEST_ONLY (admitted only when every stage domain is empty, uvt_plan), or the
    template sentinel PENDING_UV_TAIL_CERTIFICATE (planning only; run mode BLOCKED, class PENDING_UV_TAIL_CERTIFICATE)."""
    if not isinstance(raw, dict):
        raise Refusal('numerics.uv_tail must be an object (the tail library configuration)')
    if raw.get('enabled') is not True:
        raise Refusal('numerics.uv_tail.enabled must be true; omit numerics.uv_tail for a tail-OFF call (A45 N3)')
    info = uvt_info(raw)
    sr = uvt_config(info)['source_rule']
    if sr != 'continuum_v001':
        if not isinstance(sr.get('ext_grid'), dict):
            raise Refusal('UV_TAIL_NODES_V001_EXT_GRID_INVALID: source_rule.ext_grid must be a composite grid spec object, not %r' % (sr.get('ext_grid'),))
        if ngc:
            raise Refusal('UV_TAIL_NODES_V001_DDO154_ONLY: the nodes_v001 successors bind DDO154 (T2 C4T-D5)')
    return _ngc_json_loads_cx3r007(canonical(raw))

def _cx3r007_strict_uvt_info_L918(raw):
    """C2V010: the planning record of a normalized numerics.uv_tail: {config (the library config), config_sha256 (the
    library-normalized sha; None while a certificate is the pending sentinel), pending_certificates, test_only_certificates}."""
    pending = sorted((k for k in ('eps_certificate', 'lo_certificate') if raw.get(k) == UVT_PENDING_CERTIFICATE))
    cfg = uvt_config({'config': raw, 'pending_certificates': pending})
    test_only = sorted((k for k in ('eps_certificate', 'lo_certificate') if k not in pending and cfg[k] == UVT_TEST_ONLY))
    return {'config': _ngc_json_loads_cx3r007(canonical(raw)), 'config_sha256': None if pending else cfg['sha256'], 'pending_certificates': pending, 'test_only_certificates': test_only}

def _cx3r007_strict_ro1_off_blockers_L978():
    """C2V010 r4 (R5): the RO1 workers pin the RO1 c2v002 binding, the uvtail facade and the controller (bytes)."""
    out = []
    for key in ('worker', 'worker_parallel'):
        try:
            verify_pin(RO1_ROUTE_A[key][0], RO1_ROUTE_A[key][1], 'RO1 ' + key)
        except Refusal as exc:
            out.append('RO1_OFF_PIN: %s' % exc)
            continue
        t = _ngc_record_text_cx3r007(Path(RO1_ROUTE_A[key][0]))
        for need in (RO1_ROUTE_A['binding'][1], AUX_UVT['facade'][1], AUX_UVT['controller'][1]):
            if need not in t:
                out.append('RO1_OFF_WORKER_PIN: %s does not pin %s' % (Path(RO1_ROUTE_A[key][0]).name, need[:16]))
    return out

def _cx3r007_strict_uvt_admitted_record_check_L1141(path, uvt, label):
    """C2V010: an admitted reference (start.json) / body (finish.json) output and this call's tail mode must agree:
    tail OFF -> no enabled uv_tail record; tail ON -> a record with this call's config sha (UVT_ADMISSION_MISMATCH)."""
    rec = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(path))).get('uv_tail')
    if uvt is None:
        if isinstance(rec, dict) and rec.get('enabled'):
            raise Refusal('UVT_ADMISSION_MISMATCH: admitted %s %s carries an enabled UV-tail record; this call is tail OFF' % (label, path))
        return None
    if not isinstance(rec, dict) or (uvt['config_sha256'] is not None and rec.get('config_sha256') != uvt['config_sha256']):
        raise Refusal('UVT_ADMISSION_MISMATCH: admitted %s %s tail record %r is not this call config %s' % (label, path, None if not isinstance(rec, dict) else rec.get('config_sha256'), uvt['config_sha256']))
    return {'config_sha256': rec.get('config_sha256'), 'state_digest': rec.get('state_digest')}

def _cx3r007_strict_uvt_stage_records_L1155(records):
    """C2V010: the uv_tail record each executed tail stage wrote into its finish.json (state digest, empty, I1-T verdict)."""
    out = []
    for rec in records:
        if not rec.get('executed') or rec.get('kind') not in UVT_TAIL_KINDS + ('route_a_tail_manifest',):
            continue
        od = _argv_map(rec['argv']).get('--outdir')
        fin = Path(od) / 'finish.json' if od else None
        if fin is None or not fin.is_file():
            out.append({'stage': rec['name'], 'kind': rec['kind'], 'finish': 'ABSENT'})
            continue
        f = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(fin))
        u = f.get('uv_tail') if rec['kind'] != 'route_a_tail_manifest' else {k: f.get(k) for k in ('state_digest', 'empty', 'production_admissible', 'manifest', 'manifest_sha256')}
        u = u if isinstance(u, dict) else {}
        out.append({'stage': rec['name'], 'kind': rec['kind'], 'finish_sha256': sha256_file(fin), 'state_digest': u.get('state_digest'), 'empty': u.get('empty'), 'production_admissible': u.get('production_admissible'), 'test_only_admitted': u.get('test_only_admitted'), 'i1t_verdict': (u.get('i1t') or {}).get('verdict') if isinstance(u.get('i1t'), dict) else None, 'srb_rot': u.get('srb_rot')})
    return out

def _cx3r007_strict_uvt_binding_blockers_L1176(nodes=False):
    """C2V010: blockers of the tail-ON binding found from bytes: every route-B uvt successor names its gal_c2v005 base sha (the
    SCRIPTS pin) and loads the pinned route-B binding; the binding, the route-A controller and the RO1 workers pin the
    library / controller / facade bytes this driver pins; the manifest writer pins the controller."""
    out = []

    def text(path, sha, label):
        try:
            verify_pin(path, sha, label)
        except Refusal as exc:
            out.append('UVT_PIN: %s' % exc)
            return ''
        return _ngc_record_text_cx3r007(Path(path))
    act = uvt_active(nodes)
    bpath, bsha = act['aux']['route_b_binding']
    for kind, (path, sha) in act['scripts'].items():
        t = text(path, sha, 'uvt successor ' + kind)
        base_path, base_sha = SCRIPTS[kind]
        if 'successor of %s (sha256 %s)' % (Path(base_path).name, base_sha) not in t:
            out.append('UVT_BASE: %s does not name its gal_c2v005 base %s %s' % (Path(path).name, Path(base_path).name, base_sha[:16]))
        if "UVT_BINDING=(Path('%s'),'%s')" % (bpath, bsha) not in t:
            out.append('UVT_BINDING_PIN: %s does not load the pinned route-B binding %s' % (Path(path).name, bsha[:16]))
    bt = text(bpath, bsha, 'uvt route-B binding')
    ct = text(act['aux']['controller'][0], act['aux']['controller'][1], 'uvt controller')
    for key, (p, s) in dict(UVT_LIB, **act['lib_extra']).items():
        for name, t in (('route-B binding', bt), ('route-A controller', ct)):
            if s not in t:
                out.append('UVT_LIBRARY_PIN: %s does not pin %s %s' % (name, key, s[:16]))
    for key in ('worker', 'worker_parallel'):
        t = text(act['route_a'][key][0], act['route_a'][key][1], 'route-A ' + key)
        for need in (act['aux']['controller'][1], act['aux']['facade'][1], RO1_ROUTE_A['binding'][1]) + tuple((s for _, s in act['lib_extra'].values())):
            if need not in t:
                out.append('UVT_ROUTE_A_WORKER_PIN: %s does not pin %s' % (Path(act['route_a'][key][0]).name, need[:16]))
    wt = text(act['aux']['manifest_writer'][0], act['aux']['manifest_writer'][1], 'manifest writer')
    if act['aux']['controller'][1] not in wt:
        out.append('UVT_MANIFEST_WRITER_PIN: the manifest writer does not pin the route-A controller')
    return out

def _cx3r007_strict_per_call_seed_L1430(nspec):
    """Return (seed_object, changed_fields, base_seed_reusable).  Only numerical_inputs Eref_J,
    gamma (both times s), ell_F_m and the composite grid (with kmax/fourier_points) change;
    the 'physical' annotation mirrors follow.  Every other field is copied unchanged."""
    g = GALAXIES[nspec['galaxy']]
    path, sha = g['base_seed']
    raw = _ngc_record_bytes_cx3r007(Path(path))
    if sha256_bytes(raw) != sha:
        raise Refusal('base seed pin mismatch')
    base = _ngc_json_loads_cx3r007(raw)
    seed = _ngc_json_loads_cx3r007(raw)
    ni = seed['numerical_inputs']
    p = nspec['physical']
    s = p['common_scale_s']
    new = {'Eref_J': s * p['Eref_J'], 'gamma': s * p['gamma'], 'ell_F_m': p['ell_F_m']}
    grid = nspec['numerics']['composite_grid_spec']
    if grid is not None:
        new['composite_grid_spec'] = grid
        new['kmax_inverse_kpc'] = float(grid['breaks_inverse_kpc'][-1])
        new['fourier_points_per_axis'] = int(grid['total_axis_nodes'])
    ra_num = nspec['numerics'].get('route_a') or {}
    if 'max_iterations' in ra_num:
        new['max_iterations'] = ra_num['max_iterations']
    if 'seed_source_rtol_factor' in ra_num:
        new['source_rtol'] = ni['source_rtol'] * ra_num['seed_source_rtol_factor']
    changed = []
    for k, v in new.items():
        if canonical(ni.get(k)) != canonical(v):
            changed.append({'field': 'numerical_inputs.' + k, 'old': ni.get(k), 'new': v})
        ni[k] = v
    for k in ('Eref_J', 'ell_F_m', 'gamma'):
        seed['physical'][k] = ni[k]
    reusable = canonical(seed) == canonical(base)
    if not reusable:
        seed['c2_changed_fields'] = {'driver': 'galaxy_m0_forward_c2v006', 'base_seed_sha256': sha, 'changed': changed, 'note': 'scale_seed, seed_method, scope, pins, parent_seed and quadrature_selection_evidence are copied unchanged from the base seed and describe ITS normalization and grid, not this call; numerical_inputs (and the physical mirrors) are the values of this call.'}
    return (seed, changed, reusable)

def _cx3r007_strict__pinned_json_L1486(path, sha, label):
    raw = _ngc_record_bytes_cx3r007(Path(path))
    if sha256_bytes(raw) != sha:
        raise Refusal('%s pin mismatch: %s' % (label, path))
    return _ngc_json_loads_cx3r007(raw)

def _cx3r007_strict_geometry_inputs_L1627(ctx, nspec):
    """c2v003b: None at the registered geometry (pinned files; plan unchanged).  Otherwise write the per-call
    inputs under <out>/inputs: geometry_C/{PROFILE_NAME, byte copy of source binding V003} (the prep reads both
    as C/<name>), geometry_monotone_source.json and geometry_column_mean_binding.json."""
    if not geometry_active(nspec):
        return None
    p = nspec['physical']
    profile, mono, binding, record = derive_geometry(nspec['galaxy'], p['distance_Mpc'], p['inclination_deg'])
    gdir = ctx.out / 'inputs' / 'geometry_C'
    gdir.mkdir(parents=True, exist_ok=False)
    ppath, psha = ctx.write_input('geometry_C/' + PROFILE_NAME, profile)
    bpath, bsha = GEOMETRY_PINS['source_binding_v003']
    raw = _ngc_record_bytes_cx3r007(Path(bpath))
    if sha256_bytes(raw) != bsha or _write_bytes_x(ctx, gdir / Path(bpath).name, raw) != bsha:
        raise Refusal('source binding V003 copy pin mismatch')
    mono['input'] = {'path': str(ppath), 'sha256': psha, 'record': 'galaxies.DDO154.HI_plus_He'}
    mpath, msha = ctx.write_input('geometry_monotone_source.json', mono)
    binding['source_profile'] = {'path': str(ppath), 'sha256': psha}
    cpath, csha = ctx.write_input('geometry_column_mean_binding.json', binding)
    record['files'] = {'C_directory': str(gdir), 'profile': [str(ppath), psha], 'source_binding_v003_copy': [str(gdir / Path(bpath).name), bsha], 'monotone_source': [str(mpath), msha], 'column_mean_binding': [str(cpath), csha]}
    return {'C_dir': str(gdir), 'profile': (str(ppath), psha), 'monotone': (str(mpath), msha), 'binding': (str(cpath), csha), 'record': record}

def _cx3r007_strict_geometry_config_fields_L1652(geo):
    """C2V008 (a): the galaxy-config values of GEOMETRY_CONFIG_FIELDS at the call geometry, read back from the per-call
    files geometry_inputs wrote (sha256 re-verified from bytes).  geo None (registered geometry) -> {}: nothing changes.
    radial.outer_edge_kpc = sqrt(last per-call s_edge), the expression the DDO154 literal check uses at 4.04 Mpc (and the
    stages' radial_truncation compares with IEEE sqrt); observation.query_rows = the per-call binding rows {id, radius_m}."""
    if geo is None:
        return {}
    raws = {}
    for key in ('profile', 'binding'):
        raw = _ngc_record_bytes_cx3r007(Path(geo[key][0]))
        if sha256_bytes(raw) != geo[key][1]:
            raise Refusal('per-call geometry file pin mismatch: %s' % geo[key][0])
        raws[key] = _ngc_json_loads_cx3r007(raw)
    edges = raws['profile']['galaxies']['DDO154']['HI_plus_He']['s_edges_kpc2']
    return {'source.profile': {'path': str(geo['profile'][0]), 'sha256': geo['profile'][1]}, 'source.monotone_source': {'path': str(geo['monotone'][0]), 'sha256': geo['monotone'][1]}, 'radial.outer_edge_kpc': float(math.sqrt(edges[-1])), 'observation.binding': {'path': str(geo['binding'][0]), 'sha256': geo['binding'][1]}, 'observation.query_rows': [{'id': q['id'], 'radius_m': q['radius_m']} for q in raws['binding']['query_rows']]}

def _cx3r007_strict__read_checkpoint_identity_L1873(cm, cp):
    ident = _ngc_checkpoint_read_cx3r007(cm._read, str(Path(cp) / 'IDENTITY.json'), 'identity')
    if ident['identity_sha256'] != cm._sha(cm._canonical(ident['identity'])):
        raise Blocked('checkpoint identity self-hash mismatch')
    return ident

def _cx3r007_strict_ro1_outcome_L1925(ra, pred, result_path, converged):
    """RO1: (ro1 block, fired).  Block = {'rule': 'RO1', 'fired', 'events', 'armed', 'worker_sha256', 'binding_sha256'}.
    armed: result.json input_pins name a pinned RO1 binding AND the attempt start.json worker_pin is a pinned RO1 worker
    (else the shas are None; a non-armed attempt that returned a result had no readout refusal).  fired (events = [the
    record]) only for an armed attempt with an admissible route_a_readout_refusal record on a converged outcome; a present but
    inadmissible record is kept under 'inadmissible_record' with fired False.  Raises nothing."""
    bind, worker = ([], None)
    try:
        pins = ra.get('input_pins') or {}
        bind = [s for p, s in (RO1_ROUTE_A['binding'], RO1_ROUTE_A['ngc_binding']) if pins.get(str(Path(p).resolve())) == s]
        if bind:
            worker = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(result_path).parent / 'start.json')).get('worker_pin')
    except Refusal:
        raise
    except (OSError, ValueError, TypeError, AttributeError):
        bind, worker = ([], None)
    armed = bool(bind) and worker in {RO1_ROUTE_A[k][1] for k in ('worker', 'worker_parallel', 'ngc_worker', 'ngc_worker_parallel')} | {NODES_ROUTE_A[k][1] for k in ('worker', 'worker_parallel')}
    block = {'rule': 'RO1', 'fired': False, 'events': [], 'armed': armed, 'worker_sha256': worker if armed else None, 'binding_sha256': bind[0] if armed else None}
    rec = pred.get('route_a_readout_refusal')
    if rec is None:
        return (block, False)
    ok = armed and converged is True and isinstance(rec, dict) and (rec.get('code') == RO1_CODE) and (rec.get('refusal') in RO1_MESSAGES) and (rec.get('after_convergence') is True) and (pred.get('readout_status') == RO1_CODE) and (pred.get('predictions_available') is False) and ('rows' in pred) and (pred.get('rows') is None)
    if ok:
        block.update(fired=True, events=[dict(rec)])
    else:
        block['inadmissible_record'] = rec
    return (block, ok)

def _cx3r007_strict_route_a_attempt_link_L1978(cm, ra, identity_sha, cp):
    """C2V008 (d), v003c CHECK D1 (RD1 F6): the route-A attempt (its own result.json `ra`) must belong to the checkpoint it
    is paired with: result.result.source_fixed_point.checkpoint.identity_sha256 == the checkpoint IDENTITY identity_sha256,
    and its attempt token names an attempts/<token>.end.json of that identity.  Else Refusal (a pairing error in the call
    spec or tooling, never a model outcome).  A computed route A always passes (attempt and checkpoint of one run)."""
    try:
        ck = ra['result']['result']['source_fixed_point']['checkpoint']
        got, tok = (ck.get('identity_sha256'), ck.get('attempt'))
    except (KeyError, TypeError, AttributeError) as exc:
        raise StageFailed('ROUTE_A_RESULT_UNREADABLE (attempt/checkpoint link): %s: %s' % (type(exc).__name__, exc))
    if got != identity_sha:
        raise Refusal('ROUTE_A_ATTEMPT_NOT_OF_THIS_CHECKPOINT: attempt result.json names checkpoint identity %r, the paired checkpoint IDENTITY is %s' % (got, identity_sha))
    end = Path(cp) / 'attempts' / ('%s.end.json' % tok) if isinstance(tok, str) and tok and ('/' not in tok) else None
    if end is None or not end.is_file():
        raise Refusal('ROUTE_A_ATTEMPT_NOT_OF_THIS_CHECKPOINT: attempt token %r has no %s/attempts/<token>.end.json' % (tok, cp))
    rec = _ngc_checkpoint_read_cx3r007(cm._read, str(end), 'attempt_end')
    if rec.get('identity_sha256') != identity_sha:
        raise Refusal('ROUTE_A_ATTEMPT_NOT_OF_THIS_CHECKPOINT: %s carries identity %r' % (end.name, rec.get('identity_sha256')))
    return {'identity_sha256': got, 'attempt': tok, 'end_record': str(end), 'end_outcome': rec.get('outcome')}

def _cx3r007_strict_route_a_custody_L2000(cp, seed_sha, coeff_path, call_physical, outcome=None, expected_solver=None, profile_sha=None, attempt_result=None):
    """Verify a route-A checkpoint (computed in this call or admitted) from bytes and return
    the per-call identity the route-B stages need.  c2v005: the route-B stages are generalized, so the converged final
    iteration is the one the checkpoint's own records report under the strict rule (route_a_reported_iteration); the
    c2v004 iteration_0004 literal is gone.  Any ambiguity is a BLOCKER.
    C2V007: (a) F4 background mu/C custody (c2v003c hunk @@ -993); (a) F1 `outcome` (route_a_outcome_record) enforced after
    the identity/parameter/coefficient/background checks and BEFORE the strict reader, so a no-fixed-point attempt ends
    ROUTE_A_NO_FIXED_POINT instead of ROUTE_A_ITERATION_AMBIGUOUS; its converged iteration must equal the reader's.
    (b) custody.solver_code = IDENTITY code.solver {path, sha256} from bytes (the one IDENTITY field the parallel solver
    changes); `expected_solver` (path, sha) given -> it must match (route A computed by this call), else recorded only.
    C2V008: (d) `attempt_result` (the attempt's result.json) must belong to this checkpoint (route_a_attempt_link), checked
    right after the identity self-hash, before any outcome verdict; (a) `profile_sha` (DDO154: the call's source profile,
    per-call or registered) must be the one PROFILE_NAME pin the checkpoint caller recorded (c2v003b verbatim:
    ROUTE_A_GEOMETRY_MISMATCH).  The seed does not depend on the distance, so without this check a route A prepared at
    another distance would be admitted."""
    import numpy as np
    cm = exec_verified(AUX['checkpoint_module'][0], AUX['checkpoint_module'][1], 'c2v001_ckpt')
    ident = _read_checkpoint_identity(cm, cp)
    link = route_a_attempt_link(cm, attempt_result, ident['identity_sha256'], cp) if attempt_result is not None else None
    caller = cm.decode(ident['identity']['caller']['record'])
    if caller['seed']['sha256'] != seed_sha:
        raise Blocked('checkpoint caller seed %s is not this call seed %s' % (caller['seed']['sha256'], seed_sha))
    if profile_sha is not None:
        got = sorted((s for p, s in (caller.get('code_pins') or {}).items() if Path(p).name == PROFILE_NAME))
        if got != [profile_sha]:
            raise Blocked('ROUTE_A_GEOMETRY_MISMATCH: checkpoint source profile pins %s, call profile %s' % (got, profile_sha))
    phys = caller['physical_parameters']
    for k in ('Eref_J', 'ell_F_m', 'gamma'):
        if phys.get(k) != call_physical[k]:
            raise Blocked('checkpoint %s differs from call' % k)
    with np.load(coeff_path, allow_pickle=False) as f:
        grid = f['source_hessian_grid'].copy()
        mu = f['background_mu'].copy()
        Cb = f['background_C'].copy()
    dig = ident['identity']['inputs_sha256']['fourier_arguments']
    if cm.digest(grid) != dig['source_hessian_grid']:
        raise Blocked('checkpoint coefficient grid differs from call coefficient grid')
    if not (cm.digest(mu) == dig.get('mubar') and cm.digest(Cb) == dig.get('Cbar') and np.array_equal(mu, phys.get('mubar')) and np.array_equal(Cb, phys.get('Cbar'))):
        raise Blocked('ROUTE_A_BACKGROUND_MISMATCH: checkpoint background mu/C differs from call coefficients (offset v003 would refuse with Frozen background mismatch)')
    if outcome is not None:
        require_route_a_fixed_point(outcome)
    solver_code = (ident['identity'].get('code') or {}).get('solver')
    solver_code = {'path': solver_code.get('path'), 'sha256': solver_code.get('sha256')} if isinstance(solver_code, dict) else None
    if expected_solver is not None and solver_code != {'path': str(expected_solver[0]), 'sha256': expected_solver[1]}:
        raise Blocked('ROUTE_A_SOLVER_MISMATCH: checkpoint IDENTITY code.solver %r is not the solver this call ran %s %s' % (solver_code, expected_solver[0], expected_solver[1]))
    it = route_a_reported_iteration(cp, ident['identity_sha256'], cm)
    if outcome is not None:
        require_route_a_fixed_point(outcome, reported_iteration=it)
    folder = Path(cp) / ('iteration_%04d' % it)
    start = _ngc_checkpoint_read_cx3r007(cm._read, str(folder / 'START.json'), 'iteration_start')
    done = _ngc_checkpoint_read_cx3r007(cm._read, str(folder / 'COMPLETED.json'), 'iteration_completed')
    if start['iteration'] != it or done['converged'] is not True or done['iteration_start_sha256'] != start['payload_sha256']:
        raise Blocked('ROUTE_A_NOT_CONVERGED_AT_REPORTED_ITERATION_%d' % it)
    return {'identity_sha256': ident['identity_sha256'], 'iteration': it, 'start_payload_sha256': start['payload_sha256'], 'g4_ref': start['prepared_weighted_responses'], 'waves_ref': start['prepared_wavevectors'], 'caller_seed': caller['seed'], 'physical': {k: phys.get(k) for k in ('Eref_J', 'ell_F_m', 'gamma')}, 'prep_code_pins': {p: s for p, s in (caller.get('code_pins') or {}).items() if 'actual_initial_source_preparation' in p}, 'solver_code': solver_code, 'attempt_link': link, 'source_profile_sha256': profile_sha}

def _cx3r007_strict_column_H_L2067(run_dirs):
    """Solved central enthalpies of completed columns (file pins from the run finish.json)."""
    H = {}
    for d in run_dirs:
        fin = Path(d) / 'finish.json'
        if not fin.is_file():
            return None
        f = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(fin))
        for item in f['completed']:
            if sha256_file(item['path']) != item['sha256']:
                raise StageFailed('column file pin mismatch ' + item['path'])
            col = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(item['path'])))
            if col['radial_index'] in H:
                raise StageFailed('duplicate column %d' % col['radial_index'])
            H[col['radial_index']] = col['Hc_m2_s2']
    return H

def _cx3r007_strict_merged_brackets_L2101(paths):
    """index -> bracket actually supplied by a list of controls files (later runs win)."""
    out = {}
    for p in paths:
        c = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(p)))
        b = c.get('column_enthalpy_brackets', {})
        for i in c['radial_indices']:
            out[str(i)] = list(b.get(str(i), c['solver']['enthalpy_bracket']))
    return out

def _cx3r007_strict_bracket_check_L2129(pinned_paths, H, factors, overrides):
    """Diagnostic: do the pinned controls equal rule(H) bitwise?"""
    if H is None:
        return {'checked': False, 'reason': 'previous columns not available'}
    pinned = {}
    for p in pinned_paths:
        c = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(p)))
        b = c.get('column_enthalpy_brackets', {})
        for i in c['radial_indices']:
            pinned[str(i)] = b.get(str(i), c['solver']['enthalpy_bracket'])
    rule = rule_brackets(H, factors, overrides, sorted((int(i) for i in pinned)))
    diff = [i for i in pinned if pinned[i] != rule[i]]
    return {'checked': True, 'n': len(pinned), 'bitwise_equal': not diff, 'differing_indices': diff[:20]}

def _cx3r007_strict_load_galaxy_config_L2252(gname, member=None):
    """Verify the pinned galaxy-config file from bytes and that it IS the schema copy for gname (c2v006: and member):
    same field set, every value equal to the schema value for that galaxy member, statuses as the schema."""
    key = gname if member is None else (gname, member)
    if key not in GALAXY_CONFIG_FILES:
        raise Refusal('no galaxy-config file for %r' % (key,))
    path, sha = GALAXY_CONFIG_FILES[key]
    raw = _ngc_record_bytes_cx3r007(Path(path))
    if sha256_bytes(raw) != sha:
        raise Refusal('galaxy-config pin mismatch: %s' % path)
    sraw = _ngc_record_bytes_cx3r007(Path(GC_SCHEMA[0]))
    if sha256_bytes(sraw) != GC_SCHEMA[1]:
        raise Refusal('galaxy-config schema pin mismatch')
    cfg, schema = (_ngc_json_loads_cx3r007(raw), _ngc_json_loads_cx3r007(sraw))
    if cfg.get('format') != GC_FORMAT or cfg.get('galaxy') != gname or schema.get('schema') != GC_SCHEMA_NAME or (cfg.get('schema') != {'name': GC_SCHEMA_NAME, 'path': str(GC_SCHEMA[0]), 'sha256': GC_SCHEMA[1]}) or (cfg.get('member') != member):
        raise Refusal('galaxy-config format/galaxy/member/schema identity')
    entry = GC_ENTRY[gname] if member is None else GC_MEMBER_ENTRY[gname, member]
    if member is not None and (schema.get('members') or {}).get(gname, {}).get(member, {}).get('entry') != entry:
        raise Refusal('galaxy-config member %r not declared by the schema' % member)
    sf = {f['field']: f for f in schema['fields']}
    if set(cfg['fields']) != set(sf) or len(sf) != len(schema['fields']):
        raise Refusal('galaxy-config field set differs from schema')
    if set(cfg.get('per_call_fields', {})) != set(PER_CALL_FIELDS):
        raise Refusal('galaxy-config per_call_fields differ from driver PER_CALL_FIELDS')
    bad = []
    for n, e in cfg['fields'].items():
        se = sf[n][entry]
        want = 'DDO154_EXACT_LITERAL' if gname == 'DDO154' else se.get('status')
        if canonical(e.get('value')) != canonical(se.get('value')) or e.get('status') != want or e.get('kind') != sf[n]['kind']:
            bad.append(n)
        if gname != 'DDO154' and canonical(e.get('condition')) != canonical(se.get('condition')):
            bad.append(n + ' (condition)')
    slots = sorted((n for n, e in cfg['fields'].items() if e.get('status') == SLOT_STATUS))
    if sorted(cfg.get('declared_input_slots', [])) != slots:
        bad.append('declared_input_slots')
    if bad:
        raise Refusal('galaxy-config fields differ from the schema %s entry: %s' % (entry, bad))
    return {'path': str(path), 'sha256': sha, 'galaxy': gname, 'member': member, 'entry': entry, 'cfg': cfg, 'schema': schema, 'slots': slots}

def _cx3r007_strict_ddo_driver_literal_check_L2306(g, gc):
    """Every DDO154 driver literal the map lists equals the galaxy-config value (no behaviour change)."""
    f = {n: e['value'] for n, e in gc['cfg']['fields'].items()}
    tpl = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(g['solver_template'][0])))
    pin = lambda t: {'path': str(t[0]), 'sha256': t[1]}
    prof = _ngc_json_loads_cx3r007(_ngc_record_bytes_cx3r007(Path(g['profile'][0])))['galaxies']['DDO154']['HI_plus_He']['s_edges_kpc2']
    pairs = [('galaxy.key', 'DDO154'), ('custody.seed_sha256', g['base_seed'][1]), ('source.profile', pin(g['profile'])), ('source.monotone_source', pin(g['monotone_source'])), ('source.coefficients', pin(g['default_coefficients'])), ('observation.binding', pin(g['column_mean_binding'])), ('radial.n_columns', g['n_columns']), ('output.n_queries', g['n_queries']), ('geometry.registered', g['registered_geometry']), ('entropy.K_factor', g['default_entropy_K_factor']), ('driver.fixed_args', FIXED_ARGS), ('brackets.repro_overrides', g['repro_rule_overrides']), ('brackets.rule_factors', {k: LE_RULE_DEFAULTS[k] for k in ('rfs_factors', 'le_first_factors', 'le_next_factors')}), ('brackets.solver_template', dict(pin(g['solver_template']), solver=tpl['solver'])), ('brackets.fs_nominal_absolute_bracket_m2_s2', tpl['solver']['enthalpy_bracket']), ('custody.body_worker_sha256', GENERALIZED['body']['base'][1]), ('custody.fs_feedback_worker_sha256', GENERALIZED['feedback_v002']['base'][1]), ('radial.outer_edge_kpc', float(math.sqrt(prof[-1])))]
    rows = [{'field': n, 'driver_literal': v, 'equal': canonical(f[n]) == canonical(_jsonable(v))} for n, v in pairs]
    bad = [r['field'] for r in rows if not r['equal']]
    if bad:
        raise Refusal('DDO154 driver literals differ from the galaxy config: %s' % bad)
    return rows

def _cx3r007_strict_ngc_driver_value_check_L2332(g, gc):
    """c2v005: NGC3198 driver values equal the galaxy-config (schema V003 NGC entry) values; undecided fields are reported."""
    f = {n: e['value'] for n, e in gc['cfg']['fields'].items()}
    tpl = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(g['solver_template'][0])))
    geo = f['geometry.registered']
    rows = [{'field': 'geometry.registered', 'equal': isinstance(geo, dict) and set(geo) == set(g['registered_geometry']) and all((isinstance(geo[k], (int, float)) and float(geo[k]) == float(v) for k, v in g['registered_geometry'].items()))}, {'field': 'radial.n_columns', 'equal': f['radial.n_columns'] == g['n_columns_by_member'][gc.get('member')]}, {'field': 'observation.binding', 'equal': f['observation.binding'] == {'path': str(g['column_mean_binding'][0]), 'sha256': g['column_mean_binding'][1]}}, {'field': 'output.n_queries', 'equal': f['output.n_queries'] == g['n_queries']}, {'field': 'entropy.K_factor', 'equal': f['entropy.K_factor'] == g['default_entropy_K_factor']}, {'field': 'source.profile', 'equal': f['source.profile'] == {'path': str(g['profile'][0]), 'sha256': g['profile'][1]}}, {'field': 'source.coefficients', 'equal': f['source.coefficients'] == {'path': str(g['default_coefficients'][0]), 'sha256': g['default_coefficients'][1]}}, {'field': 'brackets.solver_template', 'equal': f['brackets.solver_template'] == {'path': str(g['solver_template'][0]), 'sha256': g['solver_template'][1], 'solver': tpl['solver']}}, {'field': 'brackets.fs_nominal_absolute_bracket_m2_s2', 'equal': f['brackets.fs_nominal_absolute_bracket_m2_s2'] == tpl['solver']['enthalpy_bracket']}]
    bad = [r['field'] for r in rows if not r['equal']]
    if bad:
        raise Refusal('NGC3198 driver values differ from the galaxy config: %s' % bad)
    return rows

def _cx3r007_strict_route_a_reported_iteration_L2403(cp, identity, cm=None):
    """Final converged iteration reported by the route-A checkpoint's own records: the SAME rule as the
    successors' shared route_a_final_iteration (CHECK_V001 D2/D3), without a declared value (this driver is
    what supplies route_a.accepted_iteration).  Every entry named iteration_* is a directory iteration_NNNN
    with exactly four ASCII digits; contiguous from 0; START.json and COMPLETED.json bound to this identity,
    to their iteration and to each other; converged a bool, True only at the last; every attempts/*.end.json
    of this identity and exactly one CONVERGED_FINITE_FIXED_POINT.  Blocked on any ambiguity."""
    if cm is None:
        cm = exec_verified(AUX['checkpoint_module'][0], AUX['checkpoint_module'][1], 'c2v004_ckpt_iter')
    cp = Path(cp)
    its = []
    for x in sorted(cp.iterdir(), key=lambda q: q.name):
        if not x.name.startswith('iteration_'):
            continue
        d = x.name[len('iteration_'):]
        if len(d) != 4 or any((ch not in '0123456789' for ch in d)) or (not x.is_dir()):
            raise Blocked('ROUTE_A_ITERATION_AMBIGUOUS: unexpected checkpoint entry ' + x.name)
        its.append(int(d))
    if not its or its != list(range(len(its))):
        raise Blocked('ROUTE_A_ITERATION_AMBIGUOUS: iterations %s are not contiguous from 0' % (its,))
    converged = []
    for i in its:
        folder = cp / ('iteration_%04d' % i)
        if not (folder / 'START.json').is_file() or not (folder / 'COMPLETED.json').is_file():
            raise Blocked('ROUTE_A_ITERATION_AMBIGUOUS: iteration %d lacks START or COMPLETED' % i)
        s = _ngc_checkpoint_read_cx3r007(cm._read, str(folder / 'START.json'), 'iteration_start')
        c = _ngc_checkpoint_read_cx3r007(cm._read, str(folder / 'COMPLETED.json'), 'iteration_completed')
        if s['iteration'] != i or c['iteration'] != i or s['identity_sha256'] != identity or (c['identity_sha256'] != identity) or (c['iteration_start_sha256'] != s['payload_sha256']) or (type(c['converged']) is not bool):
            raise Blocked('ROUTE_A_ITERATION_AMBIGUOUS: records of iteration %d not bound to this identity/iteration' % i)
        if c['converged']:
            converged.append(i)
    if converged != [its[-1]]:
        raise Blocked('ROUTE_A_ITERATION_AMBIGUOUS: converged %s of present %s; exactly the last must be converged' % (converged, its))
    ad = cp / 'attempts'
    if not ad.is_dir():
        raise Blocked('ROUTE_A_ITERATION_AMBIGUOUS: no attempts directory')
    ends = []
    for x in sorted(ad.glob('*.end.json'), key=lambda q: q.name):
        rec = _ngc_checkpoint_read_cx3r007(cm._read, str(x), 'attempt_end')
        if rec['identity_sha256'] != identity:
            raise Blocked('ROUTE_A_ITERATION_AMBIGUOUS: attempt_end of another identity ' + x.name)
        if rec['outcome'] == ROUTE_A_CONVERGED_OUTCOME:
            ends.append(x.name)
    if len(ends) != 1:
        raise Blocked('ROUTE_A_ITERATION_AMBIGUOUS: %d attempt_end records report %s (exactly one required)' % (len(ends), ROUTE_A_CONVERGED_OUTCOME))
    return its[-1]

def _cx3r007_strict_binding_blockers_L2460(scripts=None):
    """Blockers of the c2v005 binding, found from the successors' bytes (independent of the galaxy).  The stages2 wiring:
    every successor pins schema V003 and its own format; the shared admission, the strict route-A reader and the N2
    truncation blocks are byte-identical where present; the reference successor binds only the reference module
    successor; body pins the body base successor; both rotations pin the join successor; producer pins are exactly the
    driver's; B1 (column mean never verifies against the fixed reviewed rotation v005 file)."""
    out = []
    blocks = {'admission': {}, 'reader': {}, 'truncation': {}}
    for kind, (path, sha) in (SCRIPTS if scripts is None else scripts).items():
        if kind not in GENERALIZED:
            continue
        text = _ngc_record_text_cx3r007(Path(path))
        m = exec_verified(path, sha, 'c2v005_bind_' + kind)
        gen = GENERALIZED[kind]
        if tuple(getattr(m, 'SCHEMA', ())) != (GC_SCHEMA[0], GC_SCHEMA[1]):
            out.append('SCHEMA_PIN: %s pins %r, not schema V003 %s' % (Path(path).name, getattr(m, 'SCHEMA', None), GC_SCHEMA[1][:16]))
        if getattr(m, 'CONFIG_FORMAT', None) != gen['format']:
            out.append('CONFIG_FORMAT: %s declares %r; the driver writes %r' % (Path(path).name, getattr(m, 'CONFIG_FORMAT', None), gen['format']))
        if tuple(getattr(m, 'PRODUCER_PINS', ())) != tuple(gen.get('producer_pins', {})):
            out.append('PRODUCER_PINS: %s declares %r; the driver writes %r' % (Path(path).name, getattr(m, 'PRODUCER_PINS', ()), tuple(gen.get('producer_pins', {}))))
        blocks['admission'][kind] = _block(text, ADMISSION_HEAD, " return galaxy,{n:F[n]['value'] for n in used},cfg\n")
        if kind != 'column_mean_v004':
            blocks['reader'][kind] = _block(text, READER_HEAD, ' return its[-1]\n')
        if kind in TRUNCATION_KINDS:
            blocks['truncation'][kind] = _block(text, TRUNCATION_HEAD, ' return hits[0]\n')
        if kind in ('rotation_v001', 'rotation_v005') and tuple(m.PINS.get('join', ())) != MODULE_SUCCESSORS['join']['successor']:
            out.append('JOIN_PIN: %s pins join %r, not the join successor' % (Path(path).name, m.PINS.get('join')))
        if kind == 'body' and tuple(m.PINS.get('base', ())) != MODULE_SUCCESSORS['body_base']['successor']:
            out.append('BODY_BASE_PIN: %s pins base %r, not the body base successor' % (Path(path).name, m.PINS.get('base')))
        if kind == 'reference' and "a.reference_sha256!='%s'" % AUX['reference_module'][1] not in text:
            out.append('REFERENCE_MODULE: %s does not bind the reference module successor %s' % (Path(path).name, AUX['reference_module'][1][:16]))
        if kind == 'column_mean_v004' and B1_NEEDLE in text:
            out.append('B1_COLMEAN_PINS_REVIEWED_ROTATION_FILE: %s still verifies against the fixed reviewed rotation v005 file' % Path(path).name)
    for name, per in blocks.items():
        vals = set(per.values())
        if None in vals or len(vals) != 1:
            out.append('SHARED_BLOCK_%s not byte-identical in %s' % (name.upper(), sorted(per)))
    return out

def _cx3r007_strict_execute_chain_L2597(ctx):
    sp = ctx.spec
    gname = sp['galaxy']
    g = GALAXIES[gname]
    ngc = gname != 'DDO154'
    sv = ctx.saved
    uvt = uvt_info(sp['numerics']['uv_tail']) if 'uv_tail' in sp['numerics'] else None
    uvt_act = uvt_active(uvt_is_nodes(sp['numerics'].get('uv_tail')))
    uvt_extra = uvt_act['scripts'] if uvt is not None else None
    uvx = None
    ro1_off = uvt is None and route_a_ro1_workers(sp)
    if uvt is not None:
        ctx.scripts = dict(SCRIPTS, **uvt_act['scripts'], route_a_tail_manifest=uvt_act['aux']['manifest_writer'])
    P = sp['numerics']['picard']['passes']
    bound = sp['numerics']['picard']['speed_change_bound_km_s']
    workers = sp['numerics']['column_workers']
    brackets = sp['numerics']['brackets']
    ef = sp['physical']['entropy_K_factor']
    efs = repr(ef)
    coeff_path, coeff_sha = (sp['coefficients']['path'], sp['coefficients']['sha256'])
    verify_pin(coeff_path, coeff_sha, 'coefficient grid')
    gc = load_galaxy_config(gname, sp.get('member'))
    refusals = []

    def refuse(where, cls, msg):
        """c2v005: a remaining refusal.  Run mode: BLOCKED before any further stage.  Simulate: recorded, planning goes on."""
        refusals.append({'where': where, 'class': cls, 'refusal': msg})
        if ctx.mode == 'run':
            raise Blocked('%s [%s]: %s' % (where, cls, msg))
    info = {}
    if not ngc:
        seed_obj, changed, reusable = per_call_seed(sp)
        if reusable:
            seed_path, seed_sha = g['base_seed']
        else:
            seed_path, seed_sha = ctx.write_input('seed_c2v001.json', seed_obj)
        seed_path = Path(seed_path)
        ni = seed_obj['numerical_inputs']
        info['seed'] = {'path': str(seed_path), 'sha256': seed_sha, 'base_seed_reused': reusable, 'changed_fields': changed}
        literal_rows = ddo_driver_literal_check(g, gc)
    else:
        literal_rows = ngc_driver_value_check(g, gc)
        ra_in = sp['route_a_inputs']
        if route_a_inputs_pending(ra_in):
            seed_path, seed_sha, ni = (Path('%s(seed path)' % PENDING_ROUTE_A), '%s(custody.seed_sha256)' % PENDING_ROUTE_A, None)
            refuse('route_a', 'PENDING_ROUTE_A_OUTPUTS', 'NGC3198 route-A outputs (seed, attempt, checkpoint) are not supplied yet; route B consumes them from the NGC route-A lane (route A is not run by this driver)')
            for where, what in NGC_DEFERRED_ROUTE_A_CHECKS:
                refuse(where, 'PENDING_ROUTE_A_OUTPUTS', 'needs route-A bytes: ' + what)
            info['route_a_inputs_declared'] = ra_in
        else:
            seed_path = Path(ra_in['seed']['path'])
            seed_sha = verify_pin(seed_path, ra_in['seed']['sha256'], 'NGC route-A seed')
            seed_doc = _ngc_json_loads_cx3r007(_ngc_record_bytes_cx3r007(seed_path))
            ni = seed_doc['numerical_inputs']
            info['route_a_seed_coefficients'] = ngc_seed_coefficient_check(seed_doc, sp['coefficients'], g)
        info['seed'] = {'path': str(seed_path), 'sha256': seed_sha, 'source': 'route_a_inputs.seed (NGC route-A lane)'}
        info['member'] = {'member': sp.get('member'), 'label': 'PRIMARY' if sp.get('member') is None else gc['schema']['members']['NGC3198'][sp['member']]['label'], 'entropy_K_member': sp['physical'].get('entropy_K_member')}
    info['galaxy_config'] = {'path': gc['path'], 'sha256': gc['sha256'], 'driver_literal_check': literal_rows}
    if ni is not None:
        if ni['kpc_m'] != KPC_M:
            raise Refusal('seed kpc_m differs from driver constant')
        call_phys = {k: ni[k] for k in ('Eref_J', 'ell_F_m', 'gamma')}
        if ngc:
            s = sp['physical']['common_scale_s']
            want = {'Eref_J': s * sp['physical']['Eref_J'], 'gamma': s * sp['physical']['gamma'], 'ell_F_m': sp['physical']['ell_F_m']}
            if any((call_phys[k] != want[k] for k in want)):
                raise Refusal('NGC3198: call physical parameters (times s) differ from the route-A seed numerical_inputs')
    else:
        call_phys = None
    tr = sp['numerics']['truncation']
    if ni is not None:
        kgrid = float(ni['composite_grid_spec']['breaks_inverse_kpc'][-1])
        if tr['kmax_inverse_kpc'] is not None and tr['kmax_inverse_kpc'] > kgrid:
            raise Refusal('mask kmax exceeds the composite grid edge %.6g/kpc' % kgrid)
        kmask_m = (tr['kmax_inverse_kpc'] if tr['kmax_inverse_kpc'] is not None else kgrid) / KPC_M
    else:
        kmask_m = None
    coeff_default = coeff_path == str(g['default_coefficients'][0]) and coeff_sha == g['default_coefficients'][1]
    reuse_path, reuse_sha = GENERALIZED['reference']['base']
    percall = {'custody.seed_sha256': seed_sha, 'source.coefficients': {'path': str(coeff_path), 'sha256': coeff_sha}}
    for k in gc['slots']:
        v = (sp.get('source_slots') or {}).get(k, PENDING_SLOT)
        percall[k] = v
        if _has_pending(v):
            refuse(k, 'PENDING_N3_MONOTONE_SOURCE', '%s is a DECLARED_INPUT_SLOT (N3) not yet filled by the reviewed reducer output' % k)
    gc_written = {}
    gfields = {}

    def stage_gc(kind, tag='', producers=None):
        """Write (once per name) the per-stage config of successor `kind`; returns (path, sha, meta)."""
        name = 'galaxy_config_%s%s.json' % (kind, '_' + tag if tag else '')
        if name in gc_written:
            return gc_written[name]
        missing = [k for k in STAGE_PER_CALL[kind] if k not in percall]
        if missing:
            raise Refusal('c2v005 internal: per-call fields %s not yet computed for %s' % (missing, kind))
        pc = {k: percall[k] for k in STAGE_PER_CALL[kind]}
        pc.update({k: percall[k] for k in gc['slots'] if k in consumed_fields(kind)})
        pc.update({k: v for k, v in gfields.items() if k in consumed_fields(kind)})
        obj, omitted = stage_config_object(kind, gc, pc, omit_missing_per_call=True, producers=producers)
        pending = sorted((k for k, v in pc.items() if _has_pending(v)))
        if producers is not None and _has_pending(producers):
            pending.append('producer_pins')
        meta = {'format': GENERALIZED[kind]['format'], 'galaxy_config_file': {'path': gc['path'], 'sha256': gc['sha256']}, 'per_call_fields': sorted(pc), 'omitted_per_call_fields': omitted}
        if producers is not None:
            meta['producer_pins'] = producers
        if pending:
            p = ctx.out / 'inputs' / name
            s = 'PENDING_SHA256(%s)' % p
            meta.update(path=str(p), sha256=s, written=False, pending_fields=pending)
            if ctx.mode != 'run':
                meta['pending_probe'] = pending_probe(kind, gc, pc, producers, ctx.out / 'inputs', tag)
        else:
            p, s = ctx.write_input(name, obj)
            meta.update(path=str(p), sha256=s, written=True)
        gc_written[name] = (p, s, meta)
        return gc_written[name]

    def gen_request(name, key, argv, tag='', module_patches=None, mask=None, producers=None, stage_globals=None):
        """Request for a gal_c2v003 successor: c2v003 argv + galaxy-config tokens appended; no stage globals (C2V008 (a):
        except the reference PROFILE/PROFILE_SHA at a per-call geometry, as c2v003c)."""
        p, s, meta = stage_gc(key, tag, producers)
        req = ctx.request(name, key, list(argv) + galaxy_config_argv(key, p, s), stage_globals=stage_globals or {}, module_patches=module_patches, mask=mask)
        req['galaxy_config'] = meta
        return req
    producer_log = []

    def producer(dirs, key, flag, stage, admitted=False):
        """c2v004 rule: sha of the script that produced the upstream output(s).  run: SCRIPTS[key] (this call ran it);
        simulate on SAVED outputs, or an ADMITTED upstream in any mode (c2v005): the worker_sha256 recorded in their
        start.json, which must be the successor or its reviewed base."""
        run_value = ctx.scripts[key][1]
        val, src = (run_value, 'SCRIPTS[%s] (this call runs it)' % key)
        if ctx.mode != 'run' or admitted:
            recs = [Path(x) / 'start.json' for x in dirs]
            have = [p for p in recs if p.is_file()]
            if have:
                vals = {_ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(p))['worker_sha256'] for p in have}
                if len(have) != len(recs) or len(vals) != 1:
                    raise Refusal('c2v005: mixed upstream producers for %s %s' % (stage, flag))
                val, src = (vals.pop(), 'worker_sha256 recorded in the %s upstream start.json' % ('admitted' if admitted else 'saved'))
                producer_pin(key, val, uvt_extra)
            elif admitted:
                raise Refusal('c2v005: admitted %s output has no start.json to name its producer' % key)
        producer_log.append({'stage': stage, 'flag': flag, 'value': val, 'source': src, 'run_mode_value': run_value, 'run_mode_differs': val != run_value})
        return val
    if not ngc:
        nk = int(ni['fourier_points_per_axis'])
        if nk <= PREP_V007_MAX_AXIS_NODES:
            prep_key = 'prep'
        elif nk <= PREP_V008_MAX_AXIS_NODES:
            prep_key = 'prep_v008'
            verify_pin(PREP_V008_REVIEW[0], PREP_V008_REVIEW[1], 'prep V008 review')
        elif nk <= PREP_V009_MAX_AXIS_NODES:
            prep_key = 'prep_v009'
        else:
            raise Refusal('%d nodes/axis exceeds every route-A prep budget (%d)' % (nk, PREP_V009_MAX_AXIS_NODES))
        prep_path, prep_sha = AUX[prep_key]
        prep_info = {'path': str(prep_path), 'sha256': prep_sha, 'axis_nodes': nk, 'rule': 'V007 for <=%d nodes/axis (unchanged); V008 for %d..%d (review %s)' % (PREP_V007_MAX_AXIS_NODES, PREP_V007_MAX_AXIS_NODES + 1, PREP_V008_MAX_AXIS_NODES, PREP_V008_REVIEW[1][:16])}
        if prep_key == 'prep_v009':
            prep_info['rule'] += '; V009 for %d..%d (declared G5/G6 only; review: separate, named by prereg V006)' % (PREP_V008_MAX_AXIS_NODES + 1, PREP_V009_MAX_AXIS_NODES)
    geo = geometry_inputs(ctx, sp) if not ngc else None
    profile_sha = None if ngc else geo['profile'][1] if geo is not None else g['profile'][1]
    if not ngc:
        src_path, src_sha = geo['monotone'] if geo is not None else g['monotone_source']
    if geo is not None:
        gfields.update(geometry_config_fields(geo))
        probe = geometry_admission_probe(ctx, gc, gfields)
        info['geometry'] = dict(geo['record'], config_fields=gfields, stage_admission_probe=probe)
        ctx.geometry = info['geometry']
        if not probe['admitted']:
            refuse('geometry', 'GEOMETRY_NOT_ADMITTED_BY_STAGE_BINDING', 'distance_Mpc %r != registered %r: the pinned gal_c2v005 stages refuse the per-call geometry config fields (their own admission, schema V005): %s%s. No stage is run.' % (sp['physical']['distance_Mpc'], g['registered_geometry']['distance_Mpc'], '; '.join(('%s: %s' % kv for kv in sorted(probe['refused'].items()))), '' if probe['controls_accepted'] else ' (registered-geometry control copies also refused)'))
    if uvt is not None:
        uvx = uvt_plan(ctx, sp, ni, refuse, uvt_prep_patches(coeff_default, coeff_path, coeff_sha, geo, prep_path, prep_sha))
        ctx.uv_tail = uvx
    adm = sp.get('admit') or {}
    if ngc:
        ra_in = sp['route_a_inputs']
        if route_a_inputs_pending(ra_in):
            att, cp = (Path('%s(attempt_directory)' % PENDING_ROUTE_A), Path('%s(checkpoint_directory)' % PENDING_ROUTE_A))
            info['route_a'] = {'mode': 'pending_ngc_route_a_lane', 'attempt': str(att), 'checkpoint': str(cp), 'declared': ra_in if isinstance(ra_in, dict) else None}
        else:
            att, cp = (Path(ra_in['attempt_directory']), Path(ra_in['checkpoint_directory']))
            fin = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(att / 'finish.json'))
            if fin['status'] != 'RETURNED_ACTUAL_RESULT' or sha256_file(att / 'result.json') != ra_in['result_sha256'] or fin['result_sha256'] != ra_in['result_sha256']:
                raise Refusal('NGC route-A attempt does not verify')
            info['route_a'] = {'mode': 'admitted_ngc_route_a_lane', 'attempt': str(att), 'checkpoint': str(cp)}
    elif 'route_a' in adm:
        a = adm['route_a']
        att, cp = (Path(a['attempt_directory']), Path(a['checkpoint_directory']))
        fin = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(att / 'finish.json'))
        if fin['status'] != 'RETURNED_ACTUAL_RESULT' or sha256_file(att / 'result.json') != a['result_sha256'] or fin['result_sha256'] != a['result_sha256']:
            raise Refusal('admitted route-A attempt does not verify')
        info['route_a'] = {'mode': 'admitted', 'attempt': str(att), 'checkpoint': str(cp)}
    else:
        d = ctx.stage_dir('route_a')
        sa = sv.get('route_a') or {} if ctx.mode != 'run' else {}
        att = Path(sa['attempt']) if 'attempt' in sa else d / 'attempt_000'
        cp = Path(sa['checkpoint']) if 'checkpoint' in sa else d / 'checkpoint'
        patches = []
        prep_set = {}
        if not coeff_default:
            prep_set.update({'COEFFICIENT': {'__path__': coeff_path}, 'COEFFICIENT_SHA': coeff_sha})
        if geo is not None:
            prep_set['C'] = {'__path__': geo['C_dir']}
        if prep_set:
            patches.append({'path': str(prep_path), 'sha256': prep_sha, 'set': prep_set})
        ra_workers = route_a_column_workers(sp)
        solver_pin = AUX['solver'] if ra_workers == 1 else PARALLEL_ROUTE_A['solver']
        if uvt is not None:
            solver_pin = uvt_act['aux']['solver'] if ra_workers == 1 else uvt_act['aux']['solver_parallel']
        ra_argv = ['--seed', seed_path, '--seed-sha256', seed_sha, '--solver', solver_pin[0], '--solver-sha256', solver_pin[1], '--checkpoint-module', AUX['checkpoint_module'][0], '--checkpoint-module-sha256', AUX['checkpoint_module'][1], '--outdir', att, '--checkpoint-directory', cp, '--start-iteration', '0']
        if ra_workers > 1:
            ra_argv += ['--column-workers', str(ra_workers)]
        if uvt is not None:
            ra_argv += uvx['route_a_argv'] + ['--uv-tail-sidecar-directory', d / 'uv_tail_sidecar']
        if ro1_off:
            off_p, off_s = ctx.write_input('uv_tail_route_a_request_tail_off_ro1.json', ro1_off_request())
            ra_argv += ['--uv-tail-config', off_p, '--uv-tail-config-sha256', off_s, '--eps-certificate', UVT_TEST_ONLY, '--eps-certificate-sha256', UVT_TEST_ONLY, '--lo-certificate', UVT_TEST_ONLY, '--lo-certificate-sha256', UVT_TEST_ONLY, '--uv-tail-sidecar-directory', d / 'uv_tail_sidecar']
        req = ctx.request('route_a', 'route_a', ra_argv, module_patches=patches)
        if ra_workers > 1:
            req['script'], req['script_sha256'] = (str(PARALLEL_ROUTE_A['worker'][0]), PARALLEL_ROUTE_A['worker'][1])
        if uvt is not None:
            w = uvt_act['route_a']['worker'] if ra_workers == 1 else uvt_act['route_a']['worker_parallel']
            req['script'], req['script_sha256'] = (str(w[0]), w[1])
        if ro1_off:
            w = RO1_ROUTE_A['worker'] if ra_workers == 1 else RO1_ROUTE_A['worker_parallel']
            req['script'], req['script_sha256'] = (str(w[0]), w[1])
        if prep_key in ('prep_v008', 'prep_v009'):
            req['stage_dict_items'] = {'LOCAL': {'prep': {'path': str(prep_path), 'sha256': prep_sha}}}
        ctx.run_stages([req], [d])
        info['route_a'] = {'mode': 'computed', 'attempt': str(att), 'checkpoint': str(cp)}
        info['route_a']['implementation'] = {'column_workers': ra_workers, 'kind': 'REVIEWED_SERIAL' if ra_workers == 1 else 'PARALLEL_C2V001', 'worker': {'path': req['script'], 'sha256': req['script_sha256']}, 'solver': {'path': str(solver_pin[0]), 'sha256': solver_pin[1]}}
        if uvt is not None:
            info['route_a']['implementation']['kind'] = ('UVTAIL_NODES_RO1_SERIAL_C2V001' if ra_workers == 1 else 'UVTAIL_NODES_RO1_PARALLEL_C2V001') if uvt_is_nodes(sp['numerics'].get('uv_tail')) else 'UVTAIL_RO1_SERIAL_C2V001' if ra_workers == 1 else 'UVTAIL_RO1_PARALLEL_C2V001'
        if ro1_off:
            info['route_a']['implementation']['kind'] = 'TAIL_OFF_RO1_SERIAL_C2V010R4' if ra_workers == 1 else 'TAIL_OFF_RO1_PARALLEL_C2V010R4'
            info['route_a']['implementation']['ro1_workers'] = True
    if not ngc:
        info['route_a']['prep'] = dict(prep_info, role='used by this call' if info['route_a']['mode'] == 'computed' else 'expected for this grid; the admitted checkpoint records its own (custody.prep_code_pins)')
    att_res = Path(att) / 'result.json'
    ra = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(att_res)) if att_res.is_file() else None
    ra_outcome = route_a_outcome_record(ra, att_res) if ra is not None else None
    ctx.route_a_outcome = ra_outcome
    if ra_outcome is not None:
        info['route_a']['outcome'] = ra_outcome
    expected_solver = solver_pin if info['route_a']['mode'] == 'computed' and ctx.mode == 'run' else None
    if (Path(cp) / 'IDENTITY.json').is_file():
        cust = route_a_custody(cp, seed_sha, coeff_path, call_phys, outcome=ra_outcome, expected_solver=expected_solver, profile_sha=profile_sha, attempt_result=None if ngc else ra)
        if 'route_a' in adm and cust['identity_sha256'] != adm['route_a']['identity_sha256']:
            raise Refusal('admitted checkpoint identity differs from declared')
        if ngc and cust['identity_sha256'] != sp['route_a_inputs']['identity_sha256']:
            raise Refusal('NGC route-A checkpoint identity differs from route_a_inputs.identity_sha256')
        if uvt is None:
            uvt_route_a_identity_check(cp, None)
        elif uvt['config_sha256'] is not None:
            uvx['route_a_checkpoint_tail'] = uvt_route_a_identity_check(cp, uvt['config_sha256'])
        else:
            uvx['route_a_checkpoint_tail'] = 'PENDING (certificate sentinel: config sha unknown)'
    else:
        if not ngc and info['route_a']['mode'] == 'admitted':
            raise Refusal('ROUTE_A_CHECKPOINT_MISSING: %s/IDENTITY.json absent; admitted attempt cannot be paired (D1)' % cp)
        if info['route_a']['mode'] == 'computed' and ctx.mode == 'run' and (ra_outcome is not None):
            raise StageFailed('ROUTE_A_RESULT_WITHOUT_CHECKPOINT: %s' % cp)
        if ra_outcome is not None:
            require_route_a_fixed_point(ra_outcome)
        if ngc and (not route_a_inputs_pending(sp['route_a_inputs'])):
            raise Refusal('NGC route-A checkpoint IDENTITY.json missing under %s' % cp)
        cust = {'identity_sha256': '%s(custody.checkpoint_identity_sha256)' % PENDING_ROUTE_A if ngc else 'PENDING(route_a identity)', 'iteration': '%s(route_a.accepted_iteration)' % PENDING_ROUTE_A if ngc else 'PENDING(route_a iteration)', 'start_payload_sha256': 'PENDING', 'g4_ref': {'file_sha256': 'PENDING'}, 'waves_ref': None}
    info['route_a']['custody'] = cust
    if ra is not None:
        info['route_a']['route_a_rows'] = ra['result']['result']['rows']
        if geo is not None:
            info['route_a']['route_a_rows_scope'] = geo['record']['route_a_rows']
    if uvt is not None:
        u = ((ra or {}).get('result') or {}).get('uv_tail') if ra is not None else None
        if ra is not None and (not isinstance(u, dict)):
            raise StageFailed('UV_TAIL_ROUTE_A_RECORD_MISSING: %s has no result.uv_tail (a tail-OFF route A in a tail-ON call?)' % att_res)
        if isinstance(u, dict) and uvt['config_sha256'] is not None and (u.get('config_sha256') != uvt['config_sha256']):
            raise Refusal('UVT_ADMISSION_MISMATCH: route-A result tail config %r is not this call config %s' % (u.get('config_sha256'), uvt['config_sha256']))
        uvx['route_a_record'] = None if not isinstance(u, dict) else {k: u.get(k) for k in ('outcome', 'accepted_iteration', 'M_T_accepted', 'M_T_threshold', 'monitor_status', 'flags', 'production_admissible', 'boundary_state_digest_at_return', 'config_sha256', 'request_sha256', 'admissibility', 'E_A_rows_km_s_accepted', 'sidecar')}
        if uvx['route_a_record'] is not None:
            uvx['route_a_record'].update(probe_R_m=list(uvx['monitor_probe_R_m']), probe_phi_rad=list(uvx['monitor_probe_phi_rad']), probe_source='uv_tail request monitor (binding f42c7c65 query_rows[].radius_m; seed azimuths)')
        d = ctx.stage_dir('route_a_tail_manifest')
        mdir = d / 'manifest'
        margv = ['--seed', seed_path, '--seed-sha256', seed_sha, '--attempt-directory', att, '--checkpoint-directory', cp, '--checkpoint-module', AUX['checkpoint_module'][0], '--checkpoint-module-sha256', AUX['checkpoint_module'][1], '--uv-tail-request', uvx['request']['path'], '--uv-tail-request-sha256', uvx['request']['sha256'], '--outdir', mdir]
        mreq = ctx.request('route_a_tail_manifest', 'route_a_tail_manifest', margv, module_patches=uvx['prep_patches'])
        if prep_key in ('prep_v008', 'prep_v009'):
            mreq['stage_dict_items'] = {'LOCAL': {'prep': {'path': str(prep_path), 'sha256': prep_sha}}}
        ctx.run_stages([mreq], [d])
        uvx['manifest'] = {'path': str(mdir / 'ROUTE_A_TAIL_MANIFEST.json'), 'sha256': ctx.finish_sha(mdir, 'ROUTE_A_TAIL_MANIFEST.json')}
        if (mdir / 'finish.json').is_file():
            mf = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(mdir / 'finish.json'))
            uvx['manifest'].update(state_digest=mf.get('state_digest'), empty=mf.get('empty'), production_admissible=mf.get('production_admissible'))

    def uvt_argv(kind, source_rotation=None):
        """C2V010 (u): the tail argv of a route-B uvt successor ([] when tail OFF): config, manifest (reference, body,
        offset), the call truncation for the masked kinds, the source rotation (rfs/le columns, le rotation)."""
        if uvt is None:
            return []
        bk = UVT_BINDING_KIND[kind]
        a = ['--uv-tail-config', uvx['config']['path'], '--uv-tail-config-sha256', uvx['config']['sha256']] + uvx['test_only_flag']
        if bk in ('reference', 'body', 'offset'):
            a += ['--route-a-tail-manifest', uvx['manifest']['path'], '--route-a-tail-manifest-sha256', uvx['manifest']['sha256']]
        if bk not in ('reference', 'body') and uvx['truncation_argv'] is not None:
            a += ['--uv-tail-truncation', uvx['truncation_argv']]
        if bk in ('rfs_columns', 'le_columns', 'le_rotation'):
            a += ['--uv-tail-source-rotation-directory', source_rotation]
        return a
    ident = cust['identity_sha256']
    it = cust['iteration']
    info['route_a']['reported_final_iteration'] = it
    percall['custody.checkpoint_identity_sha256'] = ident
    percall['route_a.accepted_iteration'] = it
    reuse_patch = {'path': str(reuse_path), 'sha256': reuse_sha, 'set': {'SEED_SHA': seed_sha, 'IDENTITY': ident}}
    ref_globals = None
    if geo is not None:
        ref_globals = {}
        for target in (reuse_patch['set'], ref_globals):
            target.update(PROFILE={'__path__': geo['profile'][0]}, PROFILE_SHA=geo['profile'][1])
    mask = None
    if tr['shape'] != 'cube':
        mask = {'shape': tr['shape'], 'kmax_inverse_m': kmask_m, 'g4_file_sha256': cust['g4_ref']['file_sha256'], 'waves_ref': cust['waves_ref'], 'checkpoint_module': [str(AUX['checkpoint_module'][0]), AUX['checkpoint_module'][1]], 'cache_module': [str(AUX['cache'][0]), AUX['cache'][1]]}
    common = ['--seed', seed_path, '--checkpoint-directory', cp]
    if ngc:
        fa, fa_ok, _ = gc_value(gc, 'driver.fixed_args')
        if fa_ok:
            FA = dict(fa)
        else:
            FA = {k: 'NONE_IN_REVIEWED_CODE(driver.fixed_args.%s)' % k for k in FIXED_ARGS}
            refuse('driver.fixed_args', 'UNDECIDED_NGC_FIELD', 'driver.fixed_args is NONE_IN_REVIEWED_CODE for NGC3198 (no ROOT_DECISIONS row)')
    else:
        FA = FIXED_ARGS
    if 'reference' in adm:
        ref = Path(adm['reference']['directory'])
        verify_pin(ref / 'start.json', adm['reference']['start_sha256'], 'admitted reference start')
        verify_pin(ref / 'finish.json', adm['reference']['finish_sha256'], 'admitted reference finish')
        if not ngc and _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(ref / 'start.json'))['source_custody']['sha256'] != profile_sha:
            raise Blocked('REFERENCE_GEOMETRY_MISMATCH: admitted reference was not built from this call source profile')
        r_t = uvt_admitted_record_check(ref / 'start.json', uvt, 'reference')
        if uvt is not None:
            uvx['admitted_reference_tail'] = r_t
    else:
        d = ctx.stage_dir('reference')
        ref = d / 'reference' if ctx.mode == 'run' else ctx.saved_or('reference', d / 'reference')
        req = gen_request('reference', 'reference', common + ['--reference-module', AUX['reference_module'][0], '--reference-sha256', AUX['reference_module'][1], '--outdir', ref] + uvt_argv('reference'), stage_globals=ref_globals)
        ctx.run_stages([req], [d])
    percall['custody.reference_run'] = {'directory': str(ref), 'start_sha256': ctx.finish_sha(ref, 'start.json'), 'finish_sha256': ctx.finish_sha(ref)}
    if 'body' in adm:
        body = Path(adm['body']['directory'])
        verify_pin(body / 'finish.json', adm['body']['finish_sha256'], 'admitted body finish')
        if not ngc and src_sha not in _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(body / 'start.json'))['input_pins'].values():
            raise Blocked('BODY_GEOMETRY_MISMATCH: admitted body was not built from this call monotone source')
        b_t = uvt_admitted_record_check(body / 'finish.json', uvt, 'body')
        if uvt is not None:
            uvx['admitted_body_tail'] = b_t
    else:
        d = ctx.stage_dir('body')
        body = d / 'body' if ctx.mode == 'run' else ctx.saved_or('body', d / 'body')
        req = gen_request('body', 'body', common + ['--outdir', body] + uvt_argv('body'), module_patches=[reuse_patch])
        ctx.run_stages([req], [d])
    body_fin = ctx.finish_sha(body)
    percall['custody.body_worker_sha256'] = producer([body], 'body', 'config custody.body_worker_sha256', 'offset', admitted='body' in adm)
    d = ctx.stage_dir('offset')
    off = d / 'offset' if ctx.mode == 'run' else ctx.saved_or('offset', d / 'offset')
    req = gen_request('offset', 'offset', common + ['--body-directory', body, '--body-finish-sha256', body_fin, '--wave-batch', FA['wave_batch'], '--position-batch', FA['position_batch'], '--outdir', off] + uvt_argv('offset'), module_patches=[reuse_patch], mask=mask)
    ctx.run_stages([req], [d])
    if mask is not None:
        tinfo = {'shape': tr['shape'], 'kmax_inverse_m': kmask_m, 'scope': 'route A, reference and body unmasked (cube G4); offset real-space total and updated_base_arrays full_fields/Phi0/angular_forcing/r0 are a MIXED field (see truncation_mask)'}
        if ctx.mode == 'run' or ((Path(off) / 'unit_response.npz').is_file() and (Path(off) / 'offset_prepared.npz').is_file()):
            tinfo['mask_check'] = mask_fired_check(off, tr['shape'], kmask_m)
            ctx.event(stage='offset', event='mask_check', kept_nodes=tinfo['mask_check']['kept_nodes'], total_nodes=tinfo['mask_check']['total_nodes'])
        else:
            tinfo['mask_check'] = 'PENDING (offset outputs not present in simulate mode)'
        info['truncation'] = tinfo
    off_fin = ctx.finish_sha(off)
    percall['custody.offset_finish_sha256'] = off_fin
    base = common + ['--offset-directory', off]
    verify_pin(g['solver_template'][0], g['solver_template'][1], 'solver template')
    template = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(g['solver_template'][0])))['solver']
    if ngc and ni is not None:
        info['solver_template_mapping'] = template_mapping_check(ni, template)
    n = g['n_columns_by_member'][sp.get('member')] if ngc else g['n_columns']

    def column_pass(tag, key, extra_args, plan_runs):
        """plan_runs: list of (controls_path, controls_sha) or ('GENERATE', controls_obj).  Returns run dirs."""
        dirs, reqs, sdirs = ([], [], [])
        saved_dirs = sv.get(tag + '_columns') if ctx.mode != 'run' else None
        for j, item in enumerate(plan_runs):
            if item[0] == 'GENERATE':
                cpath, csha = ctx.write_input('%s_controls_%02d.json' % (tag, j), item[1])
            else:
                cpath, csha = item
            dd = ctx.stage_dir('%s_columns_%02d' % (tag, j))
            outc = dd / 'columns'
            if saved_dirs is not None and len(saved_dirs) == len(plan_runs):
                outc = Path(saved_dirs[j])
            cargv = base + ['--controls', cpath, '--controls-sha256', csha] + extra_args + ['--outdir', outc]
            reqs.append(gen_request('%s_columns_%02d' % (tag, j), key, cargv, module_patches=[reuse_patch], mask=mask))
            sdirs.append(dd)
            dirs.append(outc)
        for k in range(0, len(reqs), max(1, workers)):
            ctx.run_stages(reqs[k:k + workers], sdirs[k:k + workers])
        if ctx.mode != 'run' and saved_dirs is not None and (len(saved_dirs) != len(plan_runs)):
            dirs = [Path(x) for x in saved_dirs]
        return dirs

    def manifest(tag, run_dirs):
        obj = {'runs': [{'directory': str(x), 'finish_sha256': ctx.finish_sha(x)} for x in run_dirs], 'scope': 'c2v001 generated manifest for %s; complete %d columns required by the stage itself' % (tag, n)}
        return ctx.write_input('%s_manifest.json' % tag, obj)

    def generated_runs(tag, bracket_table, v001=False, split=True):
        """Group indices into column runs.  v001 supports only one global bracket per run."""
        runs = []
        if v001:
            groups = {}
            for i in range(n):
                groups.setdefault(tuple(bracket_table[str(i)]), []).append(i)
            for br, ids in sorted(groups.items(), key=lambda kv: kv[1][0]):
                for ch in _chunks(ids, workers) if split else [ids]:
                    sol = dict(template)
                    sol['enthalpy_bracket'] = list(br)
                    runs.append(('GENERATE', {'radial_indices': ch, 'solver': sol, 'selection': '%s c2v001 rule' % tag}))
        else:
            for ch in _chunks(list(range(n)), workers) if split else [list(range(n))]:
                runs.append(('GENERATE', {'radial_indices': ch, 'solver': dict(template), 'column_enthalpy_brackets': {str(i): bracket_table[str(i)] for i in ch}, 'selection': '%s c2v001 rule' % tag}))
        return runs
    rule = brackets.get('rule')
    pinned = brackets.get('pinned_controls')
    checks = {}
    if rule:
        undecided = [k for k in ('rfs_factors', 'le_first_factors', 'le_next_factors') if _has_pending(rule[k])]
        if undecided:
            refuse('brackets.rule_factors', 'UNDECIDED_NGC_FIELD', 'brackets.rule_factors is NONE_IN_REVIEWED_CODE for %s (no ROOT_DECISIONS row) and the call spec supplies none: %s' % (gname, undecided))
    if pinned:
        fs_plan = [(x['path'], verify_pin(x['path'], x['sha256'], 'pinned fs controls')) for x in pinned['fs']]
        merged = {}
        for x in pinned['fs']:
            c = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(x['path'])))
            for i in c['radial_indices']:
                merged[str(i)] = c['solver']['enthalpy_bracket']
            if any((c['solver'][k] != template[k] for k in template if k != 'enthalpy_bracket')):
                checks.setdefault('fs_solver_block_differs', []).append(x['path'])
        ro = g.get('repro_rule_overrides', {}).get('fs_absolute_overrides', {})
        expect = {str(i): list(ro.get(str(i), template['enthalpy_bracket'])) for i in range(n)}
        checks['fs'] = {'checked': True, 'n': len(merged), 'bitwise_equal': merged == expect, 'rule': 'nominal template bracket + repro_rule_overrides.fs_absolute_overrides (last successful run wins)'}
    else:
        table = {str(i): list(rule['fs_absolute_overrides'].get(str(i), template['enthalpy_bracket'])) for i in range(n)}
        fs_plan = generated_runs('fs', table, v001=True)
        checks['fs'] = rule_vs_saved(g, 'fs', table)
    fs_dirs = column_pass('fs', 'columns_v001', [] + uvt_argv('columns_v001'), fs_plan)
    mpath, msha = manifest('fs', fs_dirs)
    d = ctx.stage_dir('fs_rotation')
    fs_rot = d / 'rotation' if ctx.mode == 'run' else ctx.saved_or('fs_rotation', d / 'rotation')
    fs_col_producer = producer_pin('columns_v001', producer(fs_dirs, 'columns_v001', 'config producer_pins.column_worker', 'fs_rotation'), uvt_extra)
    ctx.run_stages([gen_request('fs_rotation', 'rotation_v001', base + ['--column-manifest', mpath, '--column-manifest-sha256', msha, '--mass-relative-tolerance', FA['mass_relative_tolerance'], '--outdir', fs_rot] + uvt_argv('rotation_v001'), module_patches=[reuse_patch], mask=mask, producers={'column_worker': fs_col_producer})], [d])
    d = ctx.stage_dir('fs_feedback')
    fs_fb = d / 'feedback' if ctx.mode == 'run' else ctx.saved_or('fs_feedback', d / 'feedback')
    fs_rot_producer = producer_pin('rotation_v001', producer([fs_rot], 'rotation_v001', 'config producer_pins.rotation_worker', 'fs_feedback'), uvt_extra)
    ctx.run_stages([gen_request('fs_feedback', 'feedback_v002', base + ['--rotation-directory', fs_rot, '--rotation-finish-sha256', ctx.finish_sha(fs_rot), '--wave-batch', FA['wave_batch'], '--position-batch', FA['position_batch'], '--bessel-cache-entries', FA['bessel_cache_entries'], '--outdir', fs_fb], module_patches=[reuse_patch], mask=mask, producers={'rotation_worker': fs_rot_producer})], [d])
    fs_fb_sha = ctx.finish_sha(fs_fb)
    percall['custody.fs_feedback_worker_sha256'] = producer([fs_fb], 'feedback_v002', 'config custody.fs_feedback_worker_sha256', 'rfs_columns')
    H_fs = column_H(fs_dirs)
    rfs_args = ['--feedback-directory', fs_fb, '--feedback-finish-sha256', fs_fb_sha]
    if pinned:
        rfs_plan = [(x['path'], verify_pin(x['path'], x['sha256'], 'pinned rfs controls')) for x in pinned['rfs']]
        checks['rfs'] = bracket_check([x['path'] for x in pinned['rfs']], H_fs, LE_RULE_DEFAULTS['rfs_factors'], g.get('repro_rule_overrides', {}).get('rfs_factor_overrides', {}))
    elif H_fs is None:
        rfs_plan = 'PENDING'
    else:
        require_bracket_source(H_fs, n, 'fs')
        table = rule_brackets(H_fs, rule['rfs_factors'], rule['rfs_factor_overrides'], range(n))
        checks['rfs'] = rule_vs_saved(g, 'rfs', table)
        rfs_plan = generated_runs('rfs', table)
    if rfs_plan == 'PENDING':
        rfs_dirs = ['PENDING(rfs columns)']
        ctx.records.append({'name': 'rfs_columns', 'executed': False, 'note': 'controls depend on fs column enthalpies (rule mode)'})
    else:
        rfs_dirs = column_pass('rfs', 'columns_v003', rfs_args + uvt_argv('columns_v003', fs_rot), rfs_plan)
    field_dir, field_sha = (fs_fb, fs_fb_sha)
    field_rot = fs_rot
    field_worker = producer([fs_fb], 'feedback_v002', '--feedback-worker-sha256', 'le1 field')
    prev_dirs = rfs_dirs
    prev_speeds = None
    final = None
    for p in range(1, P + 1):
        tag = 'le%d' % p
        last = p == P
        serial = last or bound is not None
        H_prev = column_H(prev_dirs) if all((isinstance(x, Path) for x in prev_dirs)) else None
        factors = rule['le_first_factors'] if rule and p == 1 else rule['le_next_factors'] if rule else None
        if pinned:
            plan = [(x['path'], verify_pin(x['path'], x['sha256'], 'pinned le controls')) for x in pinned['le'][p - 1]]
            checks[tag] = bracket_check([x['path'] for x in pinned['le'][p - 1]], H_prev, LE_RULE_DEFAULTS['le_first_factors'] if p == 1 else LE_RULE_DEFAULTS['le_next_factors'], {})
        elif H_prev is None:
            plan = 'PENDING'
        else:
            ov = rule['le_factor_overrides'].get(str(p), {})
            require_bracket_source(H_prev, n, 'rfs' if p == 1 else 'le%d' % (p - 1))
            table = rule_brackets(H_prev, factors, ov, range(n))
            checks[tag] = rule_vs_saved(g, tag, table)
            plan = generated_runs(tag, table, split=not serial)
        if plan == 'PENDING':
            ctx.records.append({'name': tag + '_columns', 'executed': False, 'note': 'controls depend on previous column enthalpies'})
            break
        cols = column_pass(tag, 'columns_v005', ['--feedback-directory', field_dir, '--feedback-finish-sha256', field_sha, '--feedback-worker-sha256', field_worker, '--entropy-scale', efs] + uvt_argv('columns_v005', field_rot), plan)
        mpath, msha = manifest(tag, cols)
        d = ctx.stage_dir(tag + '_rotation')
        rot = d / 'rotation' if ctx.mode == 'run' else ctx.saved_or(tag + '_rotation', d / 'rotation')
        ctx.run_stages([gen_request(tag + '_rotation', 'rotation_v005', base + ['--column-manifest', mpath, '--column-manifest-sha256', msha, '--feedback-directory', field_dir, '--feedback-finish-sha256', field_sha, '--column-worker-sha256', producer(cols, 'columns_v005', '--column-worker-sha256', tag + '_rotation'), '--feedback-worker-sha256', field_worker, '--mass-relative-tolerance', FA['mass_relative_tolerance'], '--outdir', rot, '--entropy-scale', efs] + uvt_argv('rotation_v005', field_rot), module_patches=[reuse_patch], mask=mask)], [d])
        pass_rec = {'pass': p, 'columns': [str(x) for x in cols], 'rotation': str(rot), 'field': str(field_dir)}
        rf = Path(rot) / 'finish.json'
        if rf.is_file():
            rfj = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(rf))
            pass_rec.update(rotation_positive=rfj['positive_rotation_square'], minimum_rotation_square=rfj['minimum_rotation_square'], nonpositive_indices=rfj['nonpositive_indices'], rotation_arrays={'path': rfj['arrays_path'], 'sha256': rfj['arrays_sha256']})
            if ctx.mode == 'run':
                pass_rec['rotation_array_content_digests'] = array_digests(rfj['arrays_path'])
        failures = []
        for x in cols:
            fx = Path(x) / 'finish.json'
            if fx.is_file():
                failures += _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(fx))['failures']
        pass_rec['column_failures'] = failures
        observe = len(cols) == 1 and (last or bound is not None or sp['numerics']['picard']['observe_every_pass'])
        speeds = None
        if observe:
            d = ctx.stage_dir(tag + '_column_mean')
            obsd = d / 'observation' if ctx.mode == 'run' else ctx.saved_or(tag + '_column_mean', d / 'observation')
            b, b_ok, b_st = gc_value(gc, 'observation.binding')
            if 'observation.binding' in gfields:
                b, b_ok = (gfields['observation.binding'], True)
            bpin = [str(b['path']), b['sha256']] if b_ok else ['NONE_IN_REVIEWED_CODE(observation.binding)', 'NONE_IN_REVIEWED_CODE']
            pins = [bpin, [str(Path(rot) / 'start.json'), ctx.finish_sha(rot, 'start.json')], [str(Path(rot) / 'finish.json'), ctx.finish_sha(rot)], [str(Path(cols[0]) / 'start.json'), ctx.finish_sha(cols[0], 'start.json')], [str(Path(cols[0]) / 'finish.json'), ctx.finish_sha(cols[0])]]
            percall['custody.column_mean_input_pins'] = pins
            rot_worker = rotation_producer_pin(producer([rot], 'rotation_v005', 'config producer_pins.rotation_worker', tag + '_column_mean'), uvt_extra)
            ctx.run_stages([gen_request(tag + '_column_mean', 'column_mean_v004', ['--outdir', obsd], tag=tag, producers={'rotation_worker': rot_worker})], [d])
            rp = Path(obsd) / 'result.json'
            if rp.is_file():
                res = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(rp))
                pass_rec['column_mean'] = {'path': str(rp), 'sha256': sha256_file(rp), 'status': res['status']}
                if res['status'] == 'CONDITIONAL_PREPARATION_ROWS_NOT_CALIBRATION':
                    speeds = [r['speed_km_s'] for r in res['prediction']['rows']]
                    pass_rec['rows'] = res['prediction']['rows']
                    if res['prediction'].get('invalid_rows') is not None:
                        pass_rec['invalid_rows'] = res['prediction']['invalid_rows']
                    pass_rec['nonaxisymmetric_residual_maxima'] = res['nonaxisymmetric_residual_maxima']
                    pass_rec['residual_units'] = res.get('residual_units')
                else:
                    pass_rec['column_mean_failure'] = res.get('failure')
        else:
            pass_rec['column_mean'] = 'NOT_OBSERVED (multi-run parallel pass or observe_every_pass false)'
        if speeds is not None and prev_speeds is not None:
            pass_rec['max_abs_change_km_s'] = max((abs(a - b) for a, b in zip(speeds, prev_speeds) if a is not None and b is not None))
        ctx.passes.append(pass_rec)
        ctx.event(event='pass_done', **{k: v for k, v in pass_rec.items() if k in ('pass', 'max_abs_change_km_s', 'rotation_positive')})
        stop = last or (bound is not None and pass_rec.get('max_abs_change_km_s') is not None and (pass_rec['max_abs_change_km_s'] <= bound))
        if stop:
            final = pass_rec
            break
        prev_speeds = speeds
        d = ctx.stage_dir(tag + '_feedback')
        fb = d / 'feedback' if ctx.mode == 'run' else ctx.saved_or(tag + '_feedback', d / 'feedback')
        ctx.run_stages([gen_request(tag + '_feedback', 'feedback_v004', base + ['--rotation-directory', rot, '--rotation-finish-sha256', ctx.finish_sha(rot), '--wave-batch', FA['wave_batch'], '--position-batch', FA['position_batch'], '--bessel-cache-entries', FA['bessel_cache_entries'], '--outdir', fb, '--current-feedback-directory', field_dir, '--current-feedback-finish-sha256', field_sha, '--rotation-worker-sha256', producer([rot], 'rotation_v005', '--rotation-worker-sha256', tag + '_feedback'), '--current-feedback-worker-sha256', field_worker], module_patches=[reuse_patch], mask=mask)], [d])
        field_dir, field_sha = (fb, ctx.finish_sha(fb))
        field_rot = rot
        field_worker = producer([fb], 'feedback_v004', '--feedback-worker-sha256', 'le%d field' % (p + 1))
        prev_dirs = cols
    info['bracket_rule_checks'] = checks
    info['producer_identity'] = producer_log
    info['galaxy_config']['stage_configs'] = [m for _, _, m in gc_written.values()]
    info['refusals'] = refusals
    info['percall_known'] = {k: v for k, v in percall.items()}
    if uvx is not None:
        info['uv_tail'] = uvx
    return (info, final)

def _cx3r007_strict_reference_comparison_L3289(records, saved):
    """DIAGNOSTIC ONLY (never alters the flow): compare this call's stage outputs with the saved
    chain's outputs by array content.  NPZ file bytes are not deterministic (zip timestamps), so
    arrays are compared, not file hashes."""
    rows = []
    for rec in records:
        if not rec.get('executed') or rec.get('exit_code') != 0:
            continue
        name = rec['name']
        am = _argv_map(rec['argv'])
        new = Path(am.get('--outdir', ''))
        try:
            if name == 'route_a' and 'route_a' in saved:
                a = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(am['--checkpoint-directory']) / 'iteration_0004/START.json'))
                b = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(saved['route_a']['checkpoint']) / 'iteration_0004/START.json'))
                res = {k: 'BITWISE_EQUAL' if a[k]['array_sha256'] == b[k]['array_sha256'] else 'DIFFERS' for k in ('prepared_wavevectors', 'prepared_weighted_responses', 'gas_fourier_J', 'fixed_source_fourier_J')}
            elif name == 'body' and 'body' in saved:
                res = compare_npz(new / 'body_arrays.npz', Path(saved['body']) / 'body_arrays.npz')
            elif name == 'offset' and 'offset' in saved:
                res = {f: compare_npz(new / f, Path(saved['offset']) / f) for f in ('unit_response.npz', 'source_offset.npz', 'offset_prepared.npz', 'updated_base_arrays.npz')}
            elif name.endswith('_rotation') and name in saved:
                res = compare_npz(new / 'rotation_base_arrays.npz', Path(saved[name]) / 'rotation_base_arrays.npz')
            elif name.endswith('_feedback') and name in saved:
                res = {f: compare_npz(new / f, Path(saved[name]) / f) for f in ('gas_source_feedback.npz', 'refreshed_prepared.npz')}
            elif '_columns_' in name:
                tag = name.split('_columns_')[0]
                old_paths = {}
                for od in saved.get(tag + '_columns') or []:
                    for y in _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(od) / 'finish.json'))['completed']:
                        old_paths[y['index']] = y['path']
                if not old_paths:
                    continue
                fa = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(new / 'finish.json'))
                keys = ('Hc_m2_s2', 'z_m', 'weights_m', 'rho_kg_m3', 'enthalpy_m2_s2', 'roots_m', 'K_SI')
                res = {'failures_new': [x['index'] for x in fa['failures']]}
                for x in fa['completed']:
                    if x['index'] not in old_paths:
                        res[str(x['index'])] = 'NO_SAVED_COUNTERPART'
                        continue
                    ca, cb = (_ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(x['path']))), _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(old_paths[x['index']]))))
                    res[str(x['index'])] = 'BITWISE_EQUAL' if all((ca[k] == cb[k] for k in keys)) else 'DIFFERS'
            elif name.endswith('_column_mean') and name in saved:
                a = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(new / 'result.json'))['prediction']['rows']
                b = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(saved[name]) / 'result.json'))['prediction']['rows']
                res = {'bitwise_equal': a == b, 'max_relative_difference': max((abs(x['speed_km_s'] - y['speed_km_s']) / abs(y['speed_km_s']) for x, y in zip(a, b)))}
            else:
                continue
        except Refusal:
            raise
        except Exception as exc:
            res = 'COMPARISON_ERROR %s: %s' % (type(exc).__name__, exc)
        rows.append({'stage': name, 'result': res})
    return rows

def _cx3r007_strict_transitive_pins_and_scipy_L3420(roots=None):
    """Load each stage script from verified bytes (inert) and verify every (path, sha) it pins;
    scan every pinned .py for a top-level scipy import.  c2v002: `roots` (default = the DDO
    SCRIPTS+AUX, i.e. exactly c2v001) lets the NGC configuration scan its own files."""
    import re
    seen, problems, scipy_hits = ({}, [], [])
    if roots is None:
        roots = list(SCRIPTS.values()) + list(AUX.values())
    queue = [(str(p), s) for p, s in roots]
    pat = re.compile('^\\s*(import\\s+scipy|from\\s+scipy)', re.M)

    def collect(obj, acc):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, str) and _is_hex64(v) and isinstance(k, (str, Path)):
                    acc.append((str(k), v))
                else:
                    collect(v, acc)
        elif isinstance(obj, (list, tuple)):
            if len(obj) == 2 and isinstance(obj[1], str) and _is_hex64(obj[1]) and isinstance(obj[0], (str, Path)):
                acc.append((str(obj[0]), obj[1]))
            else:
                for v in obj:
                    collect(v, acc)
    while queue:
        path, sha = queue.pop()
        if path in seen:
            if seen[path] != sha:
                problems.append('conflicting pins for %s' % path)
            continue
        seen[path] = sha
        p = Path(path)
        if not p.is_file():
            problems.append('missing %s' % path)
            continue
        if sha256_file(p) != sha:
            problems.append('pin mismatch %s' % path)
            continue
        if p.suffix == '.py':
            text = _ngc_record_text_cx3r007(p)
            if pat.search(text):
                scipy_hits.append(path)
            try:
                m = exec_verified(p, sha, 'c2v001_scan_' + p.stem)
            except Refusal:
                raise
            except Exception as exc:
                problems.append('could not load %s: %s' % (path, exc))
                continue
            acc = []
            for name in dir(m):
                if name.isupper():
                    collect(getattr(m, name), acc)
            for path2, sha2 in acc:
                if Path(path2).suffix in ('.py', '.json', '.npz'):
                    queue.append((path2, sha2))
    return {'verified_files': len(seen), 'files': seen, 'problems': problems, 'scipy_imports': scipy_hits}

def _cx3r007_strict_cmd_run_L3477(spec_path, outdir):
    out = Path(os.path.abspath(outdir))
    if out.exists():
        print('REFUSED: outdir exists', file=sys.stderr)
        return 2
    out.mkdir(parents=True)
    t0 = time.monotonic()
    raw = _ngc_record_bytes_cx3r007(Path(spec_path))
    spec_sha = sha256_bytes(raw)
    (out / 'inputs').mkdir()
    with open(out / 'inputs' / 'call_spec.json', 'xb') as f:
        f.write(raw)
    result = {'schema': RESULT_SCHEMA, 'call_spec_sha256': spec_sha, 'driver_sha256': sha256_file(__file__), 'accepted_for_calibration': False, 'scored': False, 'valid': False, 'reasons': []}
    status = 'FAILED'
    ctx = None
    try:
        nspec = normalize_spec(_ngc_json_loads_cx3r007(raw))
        if nspec.get('config') == 'NGC3198_C2V002':
            ngc_run_blocked(out, nspec, spec_sha, result)
        pins = all_static_pins(nspec)
        g = GALAXIES[nspec['galaxy']]
        _write_x(out / 'start.json', {'schema': RESULT_SCHEMA, 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'pid': os.getpid(), 'driver': str(Path(__file__).resolve()), 'driver_sha256': result['driver_sha256'], 'call_spec_sha256': spec_sha, 'normalized_spec': nspec, 'static_pins': pins, 'scope': 'Route-B m0 forward call; no observed velocity read, no score, no calibration admission.'})
        _nodes = uvt_is_nodes(nspec['numerics'].get('uv_tail'))
        bb = binding_blockers() + (ro1_off_blockers() if route_a_ro1_workers(nspec) else []) if 'uv_tail' not in nspec['numerics'] else binding_blockers(dict(SCRIPTS, **uvt_active(_nodes)['scripts'])) + uvt_binding_blockers(_nodes)
        if bb:
            result['binding_blockers'] = bb
            raise Blocked(' | '.join(bb))
        sr = route_b_static_refusals(nspec, load_galaxy_config(nspec['galaxy'], nspec.get('member')))
        if sr:
            result['remaining_refusals'] = sr
            raise Blocked('REMAINING_REFUSALS: ' + ' | '.join(('%s [%s] %s' % (r['where'], r['class'], r['refusal']) for r in sr)))
        ctx = Ctx('run', nspec, out)
        ctx.log = open(out / 'progress.jsonl', 'x')
        info, final = execute_chain(ctx)
        result.update(galaxy=nspec['galaxy'], normalized_spec=nspec, identity=info, passes=ctx.passes)
        if final is None:
            result['reasons'].append('no final pass')
        else:
            result['final_pass'] = final['pass']
            bnd = nspec['numerics']['picard']['speed_change_bound_km_s']
            chg = final.get('max_abs_change_km_s')
            result['picard_bound_met'] = None if bnd is None or chg is None else bool(chg <= bnd)
            rows_ok, invalid_rows = final_rows_check(final, g['n_queries'])
            if rows_ok:
                result['rows'] = final['rows']
                result['speeds_km_s'] = {r['id']: r['speed_km_s'] for r in final['rows']}
                if invalid_rows is not None:
                    result['invalid_rows'] = invalid_rows
                    result['headline_rule'] = 'N1/A4: rows valid=false (QUERY_INSIDE_INNERMOST_NODE) count as misses; invalid entries never pass; they do not invalidate the call'
                if nspec.get('member') is not None or nspec['physical'].get('entropy_K_member', 'N4_PRIMARY_64_OVER_121') != 'N4_PRIMARY_64_OVER_121':
                    result['alternative_label'] = {'member': nspec.get('member'), 'entropy_K_member': nspec['physical'].get('entropy_K_member'), 'status': 'DECLARED_ALTERNATIVE_NOT_HEADLINE'}
                result['valid'] = not final['column_failures'] and final.get('rotation_positive') is True
                if not result['valid']:
                    result['reasons'].append('final pass column failures or nonpositive rotation')
            else:
                result['reasons'].append('final column mean did not return %d rows: %s' % (g['n_queries'], final.get('column_mean')))
            diag = {'nonaxisymmetric_residual_maxima': final.get('nonaxisymmetric_residual_maxima'), 'residual_units': final.get('residual_units'), 'stored_residual_arrays': {'rotation_arrays': final.get('rotation_arrays'), 'keys': ['angular_radial_residual', 'angular_vertical_residual', 'angular_azimuthal_residual', 'Phi_R_full', 'Phi_z_full', 'base_residual_r0']}, 'per_pass_maxima': [{'pass': x['pass'], 'maxima': x.get('nonaxisymmetric_residual_maxima')} for x in ctx.passes]}
            if final.get('rotation_arrays'):
                try:
                    diag['azimuthal_harmonics'] = harmonic_diagnostic(final['rotation_arrays']['path'])
                except Refusal:
                    raise
                except Exception as exc:
                    diag['azimuthal_harmonics'] = 'unavailable: %s' % exc
            result['residual_diagnostics'] = diag
        status = 'COMPLETED' if result['valid'] else 'COMPLETED_INVALID'
    except Refusal as exc:
        status = 'REFUSED'
        result['reasons'].append(str(exc))
    except Blocked as exc:
        status = 'BLOCKED'
        result['reasons'].append(str(exc))
    except RouteANoFixedPoint as exc:
        status = 'ROUTE_A_NO_FIXED_POINT'
        result['reasons'].append(str(exc))
    except StageFailed as exc:
        status = 'FAILED_AT_STAGE'
        result['reasons'].append(str(exc))
    except Exception as exc:
        import traceback
        status = 'FAILED'
        result['reasons'].append('%s: %s' % (type(exc).__name__, exc))
        result['traceback'] = traceback.format_exc()
    if ctx is not None:
        if ctx.route_a_outcome is not None:
            result['route_a_outcome'] = ctx.route_a_outcome
        if ctx.geometry is not None:
            result['geometry'] = ctx.geometry
        result['stage_records'] = ctx.records
        if ctx.uv_tail is not None:
            result['uv_tail'] = dict(ctx.uv_tail, stage_records=uvt_stage_records(ctx.records))
        if ctx.spec.get('reference_compare'):
            result['reference_comparison'] = reference_comparison(ctx.records, GALAXIES[ctx.spec['galaxy']].get('saved_runs', {}))
            result['deciding_test'] = deciding_test_verdict(result['reference_comparison'], ctx.passes)
        if result.get('passes') is None:
            result['passes'] = ctx.passes
        if ctx.log is not None:
            ctx.log.close()
    result['status'] = status
    result['elapsed_seconds'] = time.monotonic() - t0
    rsha = _write_x(out / 'result.json', result)
    _write_x(out / 'finish.json', {'status': status, 'valid': result['valid'], 'result_path': str(out / 'result.json'), 'result_sha256': rsha, 'elapsed_seconds': result['elapsed_seconds'], 'reasons': result['reasons'], 'retries': 0, 'partial_outputs_preserved': True})
    return 0 if status in ('COMPLETED', 'COMPLETED_INVALID') else 3

def _cx3r007_strict__compare_argv_L3619(kind, planned, original):
    """Per-flag comparison of the planned argv (upstream outputs resolved to the SAVED chain's
    outputs) with the saved launch argv: identical literal / identical file bytes / identical
    manifest content / output location / different.  'role' says whether the value is an
    upstream output (in a real call it is this call's own output with the same role)."""
    planned_wo, gc_tokens = split_galaxy_config_argv(planned[1:])
    pm, om = (_argv_map(planned_wo), _argv_map(original[4:]))
    rows = []
    outputs = ('--outdir', '--checkpoint-directory') if kind == 'route_a' else ('--outdir',)
    for k in sorted(set(pm) | set(om)):
        a, b = (pm.get(k, '<absent>'), om.get(k, '<absent>'))
        role = 'output' if k in outputs else 'upstream-output' if k in UPSTREAM_FLAGS else 'upstream-producer-identity' if k in PRODUCER_FLAGS else 'static'
        ms = MODULE_SUCCESSORS['reference_module']
        if k in outputs:
            verdict = 'OUTPUT_LOCATION (fresh per call in a real run)'
        elif kind == 'reference' and (k, a, b) in (('--reference-module', str(ms['successor'][0]), str(ms['base'][0])), ('--reference-sha256', ms['successor'][1], ms['base'][1])):
            role = 'module-identity'
            verdict = 'MODULE_SUCCESSOR (c2v005: stages2 n_phi successor of the module the saved launch used)'
        elif a == b:
            verdict = 'IDENTICAL_VALUE'
            if a and Path(a).is_file():
                verdict = 'IDENTICAL_VALUE_FILE_SHA256=' + sha256_file(a)
        elif k == '--column-manifest' and Path(a).is_file() and Path(b).is_file() and (_ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(a)))['runs'] == _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(b)))['runs']):
            verdict = 'IDENTICAL_MANIFEST_RUNS (generated file; bytes differ)'
        elif k == '--column-manifest-sha256' and Path(pm['--column-manifest']).is_file() and (sha256_file(pm['--column-manifest']) == a) and (sha256_file(om['--column-manifest']) == b):
            verdict = 'IDENTICAL_ROLE (sha256 of the respective manifest file)'
        elif a and b and Path(a).is_file() and Path(b).is_file() and (sha256_file(a) == sha256_file(b)):
            verdict = 'IDENTICAL_FILE_BYTES'
        else:
            verdict = 'DIFFERENT'
        rows.append({'flag': k, 'role': role, 'planned': a, 'original': b, 'verdict': verdict})
    if gc_tokens:
        rows.append({'flag': ' '.join((t for t in gc_tokens if t.startswith('--'))), 'role': 'galaxy-config', 'planned': gc_tokens, 'original': '<absent>', 'verdict': 'GALAXY_CONFIG_ADDED'})
    return rows

def _cx3r007_strict__orig_launch_L3661(stage_outdir):
    lp = Path(stage_outdir).parent / 'launch.json'
    if lp.is_file():
        return _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(lp))['command']
    return None

def _cx3r007_strict_cmd_dry_run_L3682(spec_path, report_dir):
    rd = Path(os.path.abspath(report_dir))
    if rd.exists():
        print('REFUSED: report dir exists', file=sys.stderr)
        return 2
    rd.mkdir(parents=True)
    raw = _ngc_record_bytes_cx3r007(Path(spec_path))
    nspec = normalize_spec(_ngc_json_loads_cx3r007(raw))
    if nspec.get('config') == 'NGC3198_C2V002':
        return ngc_dry_run(spec_path, raw, nspec, rd)
    g = GALAXIES[nspec['galaxy']]
    report = {'schema': 'UNT_GALAXY_M0_FORWARD_DRYRUN_C2V001', 'call_spec': str(spec_path), 'call_spec_sha256': sha256_bytes(raw), 'driver_sha256': sha256_file(__file__), 'normalized_spec': nspec, 'executed_stages': 0}
    report['static_pins'] = all_static_pins(nspec)
    report['transitive_pins'] = transitive_pins_and_scipy() if route_a_column_workers(nspec) == 1 else transitive_pins_and_scipy(list(SCRIPTS.values()) + list(AUX.values()) + list(PARALLEL_ROUTE_A.values()))
    if 'uv_tail' in nspec['numerics']:
        _nodes = uvt_is_nodes(nspec['numerics']['uv_tail'])
        report['transitive_pins'] = transitive_pins_and_scipy(uvt_scan_roots(dict(SCRIPTS, **uvt_active(_nodes)['scripts']), _nodes) + list(PARALLEL_ROUTE_A.values()))
    elif route_a_ro1_workers(nspec):
        report['transitive_pins'] = transitive_pins_and_scipy(list(SCRIPTS.values()) + list(AUX.values()) + list(PARALLEL_ROUTE_A.values()) + [RO1_ROUTE_A[k] for k in ('worker', 'worker_parallel', 'binding')] + [AUX_UVT['facade'], AUX_UVT['controller']] + list(UVT_LIB.values()))
    report['coefficient_npz_headers'] = _npz_headers(nspec['coefficients']['path'])
    if nspec['galaxy'] == 'DDO154':
        seed_obj, changed, reusable = per_call_seed(nspec)
        report['seed'] = {'base_seed_reused_bitwise': reusable, 'changed_fields': changed}
        repro_like = reusable and nspec['numerics']['truncation']['shape'] == 'cube' and (nspec['physical']['entropy_K_factor'] == g['default_entropy_K_factor']) and (nspec['coefficients']['sha256'] == g['default_coefficients'][1]) and (nspec['numerics']['picard']['passes'] == 3) and (not geometry_active(nspec)) and ('uv_tail' not in nspec['numerics'])
    else:
        report['seed'] = {'source': 'route_a_inputs.seed', 'route_a_inputs': nspec['route_a_inputs']}
        repro_like = False
    saved = dict(g['saved_runs']) if repro_like else {}
    ctx = Ctx('simulate', nspec, rd / 'simulated_call', saved_runs=saved)
    info, final = execute_chain(ctx)
    report['identity'] = info
    report['binding_blockers'] = binding_blockers() + (ro1_off_blockers() if route_a_ro1_workers(nspec) else []) if ctx.uv_tail is None else binding_blockers(ctx.scripts) + uvt_binding_blockers(ctx.uv_tail.get('source_rule') == 'nodes_v001')
    consumed = {k: consumed_fields(k) for k in GENERALIZED}
    cp_ra = Path(info['route_a']['checkpoint'])
    ident_ra = info['route_a']['custody']['identity_sha256']
    it_ra = info['route_a'].get('reported_final_iteration')
    stages = []
    for rec in ctx.records:
        row = {k: rec.get(k) for k in ('name', 'kind', 'script', 'script_sha256', 'argv', 'stage_globals', 'module_patches', 'mask', 'note')}
        if rec.get('stage_dict_items'):
            row['stage_dict_items'] = rec['stage_dict_items']
        gen = GENERALIZED.get(rec.get('kind')) if rec.get('argv') else None
        if gen:
            gm = rec['galaxy_config']
            row['generalized_base'] = {'path': str(gen['base'][0]), 'sha256': gen['base'][1]}
            row['argv_without_galaxy_config'], row['galaxy_config_argv'] = split_galaxy_config_argv(rec['argv'])
            row['galaxy_config'] = gm
            row['dropped_stage_globals'] = gen['dropped_globals']
            row['omitted_fields_consumed'] = sorted(set(gm['omitted_per_call_fields']) & set(consumed[rec['kind']]))
            if gm['written']:
                row['stage_admission'] = probe_stage_admission(rec['kind'], gm['path'], gm['sha256'], ctx.scripts)
            else:
                row['stage_admission'] = 'PENDING (config not written: per-call fields %s pending in simulate)' % gm['pending_fields']
                row['pending_probe'] = gm.get('pending_probe')
            if rec['kind'] != 'column_mean_v004' and isinstance(it_ra, int) and (cp_ra / 'IDENTITY.json').is_file():
                row['route_a_iteration_probe'] = probe_route_a_iteration(rec['kind'], cp_ra, ident_ra, it_ra)
        if rec.get('argv') and repro_like:
            outdir = _argv_map(rec['argv']).get('--outdir')
            orig = _orig_launch(outdir) if outdir else None
            if orig is not None:
                row['original_launch'] = str(Path(outdir).parent / 'launch.json')
                row['original_launch_script_identical'] = orig[3] == rec['script'] and sha256_file(orig[3]) == rec['script_sha256']
                if gen:
                    row['original_launch_script_is_generalized_base'] = orig[3] == str(gen['base'][0]) and sha256_file(orig[3]) == gen['base'][1]
                row['argv_comparison'] = _compare_argv(rec['kind'], [rec['script']] + rec['argv'], orig)
                row['all_inputs_identical'] = (row['original_launch_script_identical'] or row.get('original_launch_script_is_generalized_base', False)) and all((x['verdict'].startswith('IDENTICAL') or x['verdict'].startswith('OUTPUT_LOCATION') or x['verdict'] == 'GALAXY_CONFIG_ADDED' or x['verdict'].startswith('MODULE_SUCCESSOR') for x in row['argv_comparison']))
            else:
                row['original_launch'] = None
                row['note'] = (row.get('note') or '') + ' no saved launch for this stage (extra observation or new stage)'
        if rec.get('argv'):
            ov = []
            if rec.get('stage_globals') or rec.get('module_patches') or rec.get('stage_dict_items'):
                m = exec_verified(rec['script'], rec['script_sha256'], 'c2v001_dry_' + rec['kind'])
                for name, val in (rec.get('stage_globals') or {}).items():
                    ov.append(_override_row(rec['kind'], name, m.__dict__.get(name, _ABSENT), _decode_value(val)))
                for gname, items in (rec.get('stage_dict_items') or {}).items():
                    for key, pin in items.items():
                        hard = (m.__dict__.get(gname) or {}).get(key, _ABSENT)
                        ov.append(_override_row(rec['kind'], '%s[%s]' % (gname, key), hard, (Path(pin['path']), pin['sha256'])))
                for patch in rec.get('module_patches') or []:
                    dm = exec_verified(patch['path'], patch['sha256'], 'c2v001_dry_dep')
                    for name, val in patch['set'].items():
                        ov.append(_override_row(Path(patch['path']).name, name, getattr(dm, name, _ABSENT), _decode_value(val)))
            row['override_comparison'] = ov
        stages.append(row)
    report['stages'] = stages
    report['passes_simulated'] = ctx.passes
    gc_all = load_galaxy_config(nspec['galaxy'], nspec.get('member'))
    route_a_pending = route_a_inputs_pending(nspec.get('route_a_inputs'))
    if nspec['galaxy'] != 'DDO154':
        report['n1_query_rows'] = n1_query_rows(nspec, gc_all)
        planned = {x['kind'] for x in stages if x.get('generalized_base')}
        pk = info['percall_known']
        unplanned = {}
        for kind in GENERALIZED:
            if kind in planned:
                continue
            pc = {k: pk.get(k, '%s(%s)' % (PENDING_ROUTE_A if route_a_pending else 'PENDING_RUN_OUTPUT', k)) for k in STAGE_PER_CALL[kind]}
            pc.update({k: pk[k] for k in gc_all['slots'] if k in pk and k in consumed_fields(kind)})
            prods = {nm: '%s(producer_pins.%s)' % (PENDING_ROUTE_A if route_a_pending else 'PENDING_RUN_OUTPUT', nm) for nm in GENERALIZED[kind].get('producer_pins', {})} or None
            unplanned[kind] = pending_probe(kind, gc_all, pc, prods, rd / 'simulated_call' / 'inputs', 'unplanned')
        report['admission_probes_unplanned_stages'] = unplanned
    report['remaining_refusals'] = remaining_refusals_v006(report, info, gc_all, route_a_pending)
    if final is not None and final.get('rows'):
        report['final_rows_from_saved_chain'] = final['rows']
    sp = [ctx_row for ctx_row in stages if ctx_row.get('argv_comparison') is not None]
    report['summary'] = {'repro_like': repro_like, 'stages_planned': len(stages), 'stages_compared_with_original_launch': len(sp), 'stages_all_inputs_identical': sum((1 for x in sp if x.get('all_inputs_identical'))), 'overrides_total': sum((len(x.get('override_comparison') or []) for x in stages)), 'overrides_noop_identical': sum((1 for x in stages for o in x.get('override_comparison') or [] if o['verdict'] == 'NO_OP_IDENTICAL_VALUE')), 'overrides_not_noop': ['%s %s.%s: %s' % (x['name'], o['where'], o['name'], o['verdict']) for x in stages for o in x.get('override_comparison') or [] if o['verdict'] != 'NO_OP_IDENTICAL_VALUE'], 'bracket_rule_checks': info.get('bracket_rule_checks'), 'scipy_imports': report['transitive_pins']['scipy_imports'], 'pin_problems': report['transitive_pins']['problems'], 'galaxy_config': {k: info['galaxy_config'][k] for k in ('path', 'sha256')}, 'driver_literals_equal_galaxy_config': all((r['equal'] for r in info['galaxy_config']['driver_literal_check'])), 'generalized_stage_calls': sum((1 for x in stages if x.get('generalized_base'))), 'stage_admission_accepted': sum((1 for x in stages if isinstance(x.get('stage_admission'), dict) and x['stage_admission'].get('accepted'))), 'stage_admission_refused': ['%s: %s' % (x['name'], x['stage_admission']['refusal']) for x in stages if isinstance(x.get('stage_admission'), dict) and (not x['stage_admission'].get('accepted'))], 'stage_admission_pending': [x['name'] for x in stages if isinstance(x.get('stage_admission'), str)], 'route_a_iteration_probes': {x['name']: x['route_a_iteration_probe'].get('iteration', x['route_a_iteration_probe'].get('refusal')) for x in stages if x.get('route_a_iteration_probe')}, 'omitted_fields_consumed': {x['name']: x['omitted_fields_consumed'] for x in stages if x.get('omitted_fields_consumed')}, 'producer_identity_run_mode_differs': [p for p in info.get('producer_identity', []) if p['run_mode_differs']], 'binding_blockers': report['binding_blockers'], 'remaining_refusals_by_class': report['remaining_refusals']['by_class'], 'refusals_beyond_pending_inputs': report['remaining_refusals']['beyond_pending_inputs'], 'unexplained_refusals': report['remaining_refusals']['unexplained'], 'only_refusals_needing_route_a_bytes': report['remaining_refusals']['only_refusals_needing_route_a_bytes'], 'deferred_route_a_checks': [x['where'] for x in report['remaining_refusals']['deferred_route_a_checks']], 'n1_query_rows': report.get('n1_query_rows')}
    ra = info.get('route_a', {})
    rp = Path(ra.get('attempt', '')) / 'result.json'
    if rp.is_file():
        src = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(rp))['result'].get('source_pins', {})
        bad = [p for p, s in src.items() if not Path(p).is_file() or sha256_file(p) != s]
        report['route_a_recorded_source_pins'] = {'n': len(src), 'all_current_files_match': not bad, 'mismatch': bad, 'note': 'prep V007/V008 loads these helper modules by path and RECORDS (does not verify) their SHA256; checked here from bytes'}
    report['summary']['overrides_wording'] = '%d of %d identity overrides are no-ops' % (report['summary']['overrides_noop_identical'], report['summary']['overrides_total'])
    report['summary']['route_a_prep'] = info.get('route_a', {}).get('prep')
    if ctx.uv_tail is not None:
        report['uv_tail'] = ctx.uv_tail
        report['summary']['uv_tail'] = {'admissibility': ctx.uv_tail['admissibility'], 'pending_certificates': ctx.uv_tail['pending_certificates'], 'source_rule': ctx.uv_tail.get('source_rule'), 'nodes_ext_context': ctx.uv_tail.get('nodes_ext_context'), 'domain_empty_all_stages': ctx.uv_tail['domain_empty_all_stages'], 'outer': ctx.uv_tail['outer'], 'kept_regions': {k: v['kept'] for k, v in ctx.uv_tail['kept_regions'].items()}, 'route_a_worker': [x['script_sha256'] for x in stages if x['kind'] == 'route_a'], 'tail_stage_scripts': {x['name']: x['script_sha256'] for x in stages if x['kind'] in UVT_TAIL_KINDS + ('route_a_tail_manifest',)}, 'refusal_classes_beyond_pending': sorted({it['class'] for it in report['remaining_refusals']['items'] if it['class'] not in EXPECTED_PENDING_CLASSES})}
    lines = ['DRY-RUN PLAN %s  (spec %s)' % (nspec.get('label', ''), report['call_spec_sha256']), '']
    if info.get('geometry'):
        gp = info['geometry']['stage_admission_probe']
        report['summary']['geometry'] = {'distance_Mpc': info['geometry']['distance_Mpc'], 'files': info['geometry']['files'], 'config_fields': sorted(info['geometry']['config_fields']), 'stage_binding_admits_geometry': gp['admitted'], 'refused_by': gp['refused'], 'registered_controls_accepted': gp['controls_accepted']}
        lines.append('GEOMETRY distance %r Mpc (per-call files %s); stage binding admits it: %s; registered controls accepted: %s' % (info['geometry']['distance_Mpc'], sorted(info['geometry']['files']), gp['admitted'], gp['controls_accepted']))
        for kind, msg in sorted(gp['refused'].items()):
            lines.append('  REFUSED by %s own admission: %s' % (kind, msg))
        lines.append('')
    if ctx.uv_tail is not None:
        u = ctx.uv_tail
        lines.append('UV TAIL (C2V010): admissibility %s; outer %s; K %.6g/kpc; all stage domains empty: %s; pending certificates: %s' % (u['admissibility'], u['outer'], u['K_inverse_kpc'], u['domain_empty_all_stages'], u['pending_certificates'] or 'none'))
        lines.append('UV TAIL source rule (r4): %s%s' % (u.get('source_rule'), '' if not u.get('nodes_ext_context') else '; ext grid %s (%d extra nodes)' % (u['nodes_ext_context']['ext_spec']['version'] if 'version' in u['nodes_ext_context']['ext_spec'] else '?', u['nodes_ext_context']['n_ext_nodes'])))
        for k, v in u['kept_regions'].items():
            lines.append('  kept %-14s %-12s %s empty=%s' % (k, v['binding_kind'], v['kept'], v['domain_empty']))
        lines.append('')
    for b in report['binding_blockers']:
        lines.append('BINDING BLOCKER (run mode refuses before any stage): ' + b)
    if report['binding_blockers']:
        lines.append('')
    rr = report['remaining_refusals']
    lines.append("REMAINING REFUSALS (c2v006, from the successors' own admission and the driver; only route-A bytes missing: %s):" % rr['only_refusals_needing_route_a_bytes'])
    for cls, items in rr['by_class'].items():
        lines.append('  %-30s %s' % (cls, ', '.join(items)))
    if rr['beyond_pending_inputs']:
        lines.append('  beyond pending inputs: ' + '; '.join(rr['beyond_pending_inputs']))
    lines.append('')
    for i, s in enumerate(stages, 1):
        verdict = s.get('all_inputs_identical')
        lines.append('%02d %-22s %-18s %s  inputs_identical_to_saved_launch=%s' % (i, s['name'], s['kind'] or '', (s['script_sha256'] or '')[:12], verdict))
        for x in s.get('argv_comparison') or []:
            lines.append('      %-34s %-15s %s' % (x['flag'], x['role'], x['verdict']))
        if s.get('argv') and (not s.get('argv_comparison')):
            lines.append('      argv: ' + ' '.join((str(a).replace(str(ROOT), '$ROOT').replace(str(rd), '$DRY') for a in s['argv'])))
        if s.get('mask'):
            lines.append('      mask: shape=%s kmax=%.6g/m g4_blob=%s (weight mask on existing grid)' % (s['mask']['shape'], s['mask']['kmax_inverse_m'], s['mask']['g4_file_sha256'][:16]))
        for gname, items in (s.get('stage_dict_items') or {}).items():
            for key, pin in items.items():
                lines.append('      dict item %s[%s] := %s %s' % (gname, key, Path(pin['path']).name, pin['sha256'][:12]))
        for o in s.get('override_comparison') or []:
            lines.append('      override %s.%s: %s' % (o['where'], o['name'], o['verdict']))
        if s.get('galaxy_config'):
            gm = s['galaxy_config']
            lines.append('      galaxy-config %s %s (%s; per-call %s)' % (Path(gm['path']).name, gm['sha256'][:16] if gm['written'] else gm['sha256'], gm['format'], ','.join(gm['per_call_fields'])))
            adm = s['stage_admission']
            lines.append('      stage admission: ' + (('ACCEPTED' if adm['accepted'] else 'REFUSED ' + adm['refusal']) if isinstance(adm, dict) else adm))
            if s.get('pending_probe'):
                pa = s['pending_probe']['admission']
                lines.append('      placeholder-copy admission: ' + ('ACCEPTED' if pa['accepted'] else 'REFUSED ' + pa['refusal']))
            if s.get('route_a_iteration_probe'):
                lines.append('      route-A iteration (stage rule on checkpoint records): %s' % s['route_a_iteration_probe'])
            lines.append('      dropped stage globals -> config: %s' % s['dropped_stage_globals'])
        if s.get('note'):
            lines.append('      note: ' + s['note'].strip())
    for kind, pr in (report.get('admission_probes_unplanned_stages') or {}).items():
        pa = pr['admission']
        lines.append('-- %-20s (not reached in simulate) placeholder-copy admission: %s' % (kind, 'ACCEPTED' if pa['accepted'] else 'REFUSED ' + pa['refusal']))
    with open(rd / 'DRYRUN_PLAN.txt', 'x') as f:
        f.write('\n'.join(lines) + '\n')
    _write_x(rd / 'DRYRUN_REPORT.json', report)
    print(json.dumps(_jsonable(report['summary']), indent=1))
    return 0

def _cx3r007_strict_n1_query_rows_L4167(nspec, gc):
    """c2v006 (N1/A4): the query rows below the innermost / beyond the outermost route-B radial node of this member's roster
    (schema derived rosters), and whether the pinned observation binding carries the invalid_row_rule."""
    rows, rows_ok, _ = gc_value(gc, 'observation.query_rows')
    rosters = gc['schema'].get('derived_rosters', {})
    ros = rosters.get(NGC_ROSTER_BY_MEMBER[nspec.get('member')]) if nspec['galaxy'] == 'NGC3198' else rosters.get(nspec['galaxy'])
    if not rows_ok or not ros:
        return None
    lo = ros.get('innermost_node_kpc', ros.get('smallest_node_kpc'))
    hi = ros.get('outermost_node_kpc', ros.get('largest_node_kpc'))
    b, b_ok, _ = gc_value(gc, 'observation.binding')
    rule = _ngc_json_loads_cx3r007(_ngc_record_bytes_cx3r007(Path(b['path']))).get('invalid_row_rule') if b_ok and sha256_file(b['path']) == b['sha256'] else None
    return {'roster': {'innermost_node_kpc': lo, 'outermost_node_kpc': hi}, 'below_innermost': [q['id'] for q in rows if q['radius_m'] / KPC_M < lo], 'beyond_outermost': [q['id'] for q in rows if q['radius_m'] / KPC_M > hi], 'binding_invalid_row_rule': rule}

def _cx3r007_strict__base_seed_grid_L4384(g):
    path, sha = g['base_seed']
    raw = _ngc_record_bytes_cx3r007(Path(path))
    if sha256_bytes(raw) != sha:
        raise Refusal('base seed pin mismatch')
    return _ngc_json_loads_cx3r007(raw)['numerical_inputs']['composite_grid_spec']

def _cx3r007_strict_ngc_seed_L4485(nspec):
    """Candidate per-call NGC worker seed: DDO seed V002 numerical controls carried unchanged,
    plus the call's Eref/gamma (times s), ell_F, composite grid and h2_tail_mass_rtol.  Checked
    against the NGC prep v001 signature (exact keyword set).  Not root-selected."""
    import inspect
    path, sha = NGC_DATA['parameter_seed']
    raw = _ngc_record_bytes_cx3r007(Path(path))
    if sha256_bytes(raw) != sha:
        raise Refusal('parameter seed pin mismatch')
    base = _ngc_json_loads_cx3r007(raw)
    ni = _ngc_json_loads_cx3r007(json.dumps(base['numerical_inputs']))
    p, s = (nspec['physical'], nspec['physical']['common_scale_s'])
    grid = nspec['numerics']['composite_grid_spec']
    set_fields = {'Eref_J': s * p['Eref_J'], 'gamma': s * p['gamma'], 'ell_F_m': p['ell_F_m'], 'h2_tail_mass_rtol': nspec['numerics']['h2_tail_mass_rtol']}
    if grid is not None:
        set_fields.update(composite_grid_spec=grid, kmax_inverse_kpc=float(grid['breaks_inverse_kpc'][-1]), fourier_points_per_axis=int(grid['total_axis_nodes']))
    provenance = {}
    for k in sorted(set(ni) | set(set_fields)):
        if k in set_fields:
            old = ni.get(k)
            ni[k] = set_fields[k]
            provenance[k] = 'CALL_SPEC' + ('' if canonical(old) != canonical(ni[k]) else ' (equal to DDO seed V002 value)')
        else:
            provenance[k] = 'CARRIED_FROM_DDO_SEED_V002 (numerical control; not NGC-reviewed)'
    if ni['kpc_m'] != KPC_M:
        raise Refusal('seed kpc_m differs from driver constant')
    prep = exec_verified(NGC_CODE['prep'][0], NGC_CODE['prep'][1], 'c2v002_ngc_prep_sig')
    params = set(inspect.signature(prep.prepare_inputs).parameters)
    if set(ni) != params:
        raise Refusal('candidate seed keys differ from NGC prep v001 signature: missing %s extra %s' % (sorted(params - set(ni)), sorted(set(ni) - params)))
    if ni.get('analytic_initial_azimuth') is not True or ni.get('composite_grid_spec') is None:
        raise Refusal('NGC binding v001 requires analytic_initial_azimuth True and a composite grid')
    pins = {str(NGC_DATA[k][0]): NGC_DATA[k][1] for k in ('manifest', 'profile', 'h2_tail_reduction', 'h2_source', 'parameter_seed')}
    seed = {'status': 'C2V002_CANDIDATE_NGC3198_TARGET_FREE_SEED_NOT_ROOT_SELECTED', 'numerical_inputs': ni, 'physical': {'Eref_J': ni['Eref_J'], 'ell_F_m': ni['ell_F_m'], 'gamma': ni['gamma'], 'common_scale_s': s, 'distance_Mpc': p['distance_Mpc'], 'inclination_deg': p['inclination_deg'], 'released_inclination_deg': GALAXIES['NGC3198']['registered_geometry']['released_inclination_deg']}, 'pins': pins, 'parameter_provenance': provenance, 'parent_seed': {'path': str(path), 'sha256': sha, 'scale_seed': base.get('scale_seed')}, 'scope': 'Target-free NGC43 provisional circular trial seed. Physical point = DDO seed parameters unless the call spec says otherwise; numerical controls carried from DDO seed V002 are DDO-selected, not NGC-reviewed. No velocity read; not calibration.'}
    return seed

def _cx3r007_strict_ngc_static_pins_L4535(nspec):
    pins = {}
    for table in (NGC_CODE, NGC_DATA, NGC_EVIDENCE):
        for key, (path, sha) in table.items():
            pins[str(path)] = verify_pin(path, sha, 'NGC ' + key)
    for key in ('solver', 'checkpoint_module'):
        pins[str(AUX[key][0])] = verify_pin(AUX[key][0], AUX[key][1], key)
    pins[nspec['coefficients']['path']] = verify_pin(nspec['coefficients']['path'], nspec['coefficients']['sha256'], 'coefficients')
    rw = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(NGC_DATA['review_worker'][0])))
    rb = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(NGC_DATA['review_binding'][0])))
    rb_pins = {x['path']: x['sha256'] for x in rb['sources']}
    review = {'worker_review_verdict': rw['verdict'], 'worker_review_sha_matches': rw['sha256'] == NGC_CODE['worker'][1], 'binding_review_verdict': rb['verdict'], 'binding_review_pins_match': all((rb_pins.get(str(NGC_CODE[k][0])) == NGC_CODE[k][1] for k in ('prep', 'binding'))) and rb_pins.get(str(NGC_DATA['manifest'][0])) == NGC_DATA['manifest'][1] and (rb_pins.get(str(NGC_DATA['h2_tail_reduction'][0])) == NGC_DATA['h2_tail_reduction'][1]), 'blocking_corrections': rw['blocking_corrections'] + rb['blocking_corrections']}
    w = exec_verified(NGC_CODE['worker'][0], NGC_CODE['worker'][1], 'c2v002_ngc_worker_local')
    local = {k: (str(pth), s) for k, (pth, s) in w.LOCAL.items()}
    review['worker_LOCAL_equals_config'] = all((local.get(k) == (str(NGC_CODE[k][0]), NGC_CODE[k][1]) for k in local)) and set(local) == {'prep', 'binding', 'composite', 'stream', 'base', 'prediction'}
    return (pins, review)

def _cx3r007_strict_ngc_sources_summary_L4578():
    """Load the NGC source JSONs (source-only files; no target velocity file is opened) and
    return headers and counts.  The rotmod .dat named in the manifest provenance is NOT opened."""
    out = {}
    load = {k: _ngc_json_loads_cx3r007(_ngc_record_bytes_cx3r007(Path(NGC_DATA[k][0]))) for k in ('profile', 'manifest', 'h2_source', 'physical_source_state_binding', 'stellar_photometry_nodes', 'source_only_bundle')}
    tail = _ngc_json_loads_cx3r007(_ngc_record_bytes_cx3r007(Path(NGC_DATA['h2_tail_reduction'][0])))
    prof = load['profile']['galaxies']['NGC3198']
    gas, st = (prof['HI_plus_He'], prof['stellar_reference'])
    out['profile_NGC3198'] = {'geometry': prof['geometry'], 'HI_annuli': len(gas['annular_means_Msun_pc2']), 'HI_s_edges': len(gas['s_edges_kpc2']), 'HI_support_radius_kpc': gas['support_radius_kpc'], 'HI_integrated_mass_Msun': gas['integrated_mass_Msun'], 'HI_helium': gas['helium'], 'stellar_nodes': st['node_count'], 'stellar_last_radius_kpc': float(st['radius_kpc'][-1]), 'stellar_height_kpc': st['height_kpc'], 'stellar_outer_scale_kpc': st['outer_scale_kpc']}
    m = load['manifest']
    out['manifest'] = {'n_rows': len(m['rows']), 'query_ids': [r['query_id'] for r in m['rows']], 'Rad_text': [r['Rad_text'] for r in m['rows']], 'units': sorted({r['Rad_unit'] for r in m['rows']}), 'emitted_columns': m['emitted_columns'], 'no_other_columns_emitted': m['no_other_columns_emitted'], 'reference_distance_Mpc_text': m['reference_distance']['rotmod_header']['value_text'], 'not_included': m['not_included'], 'ids_are_Q01_Q43_in_order': [r['query_id'] for r in m['rows']] == ['NGC3198-Q%02d' % i for i in range(1, 44)]}
    src_ok = Path(tail['source']['path']) == Path(NGC_DATA['h2_source'][0]) and tail['source']['sha256'] == NGC_DATA['h2_source'][1]
    rows = load['h2_source']['S1_alternative_and_stellar_median_rows']['rows'][:10]
    out['h2'] = {'tail_source_pin_matches_config': src_ok, 'outer_scale_kpc': tail['outer_scale_kpc'], 'tail_rule': tail['tail'], 'detected_centres_used': len(rows), 'radius_literals_kpc': [r['radius_kpc_literal']['value'] for r in rows], 'helium_already_included': all((r['conventions']['gas_helium']['value'] == 'ALREADY_INCLUDED' for r in rows))}
    for k in ('physical_source_state_binding', 'stellar_photometry_nodes', 'source_only_bundle', 'h2_source'):
        o = load[k]
        out.setdefault('headers', {})[k] = {'schema': o.get('schema'), 'status': o.get('status'), 'top_keys': sorted(o)[:20]}
    out['velocity_like_key_names'] = {k: _key_scan(v) for k, v in load.items()}
    out['not_opened'] = [m['source']['path']]
    return out

def _cx3r007_strict_ngc_prep_local_modules_L4613():
    """Modules NGC prep v001 loads by path INSIDE prepare_inputs (not module-global pins): it records
    their sha at load and the composite adapter re-verifies that record from bytes; neither checks
    them against a reviewed list.  Reported here with sha from bytes and a scipy scan."""
    import re
    text = _ngc_record_text_cx3r007(Path(NGC_CODE['prep'][0]))
    prep = exec_verified(NGC_CODE['prep'][0], NGC_CODE['prep'][1], 'c2v002_ngc_prep_locals')
    base = {'HERE': prep.HERE, 'HC': prep.HC, 'HP': prep.HP}
    paths = [base[a] / b for a, b in re.findall("\\b(HERE|HC|HP)/'([^']+\\.py)'", text)] + [prep.KERNEL]
    pat = re.compile('^\\s*(import\\s+scipy|from\\s+scipy)', re.M)
    out = []
    for pth in dict.fromkeys(paths):
        ok = Path(pth).is_file()
        out.append({'path': str(pth), 'exists': ok, 'sha256': sha256_file(pth) if ok else None, 'scipy_import': bool(ok and pat.search(_ngc_record_text_cx3r007(Path(pth))))})
    return out

def _cx3r007_strict_ngc_caller_contract_check_L4631():
    """Deciding evidence for the route-A blocker, using only inert definitions of the real modules
    and a synthetic caller dict (no solver, no checkpoint directory, no project data)."""
    import inspect
    res = {}
    texts = {k: _ngc_record_bytes_cx3r007(Path(NGC_CODE[k][0])) for k in ('worker', 'binding', 'composite')}
    res['physical_parameters_or_numerical_controls_written_by'] = {k: b'physical_parameters' in t or b'numerical_controls' in t for k, t in texts.items()}
    res['ddo_stable_binding_v002_writes_them'] = b"identity['physical_parameters']" in _ngc_record_bytes_cx3r007(Path(NGC_EVIDENCE['ddo_stable_binding_v002'][0]))
    w = texts['worker'].decode()
    built = all((s in w for s in ('caller_identity=dict(', "seed={'path'", 'code_pins=pins', "worker={'path'", 'boundary_prescription=')))
    caller = {'seed': {'path': 'SYNTHETIC', 'sha256': '0' * 64}, 'code_pins': {'/synthetic.py': '0' * 64}, 'worker': {'path': 'SYNTHETIC', 'sha256': '0' * 64}, 'boundary_prescription': 'synthetic', 'composite_full_driver': {}, 'composite_source_binding': {}}
    cm = exec_verified(AUX['checkpoint_module'][0], AUX['checkpoint_module'][1], 'c2v002_ngc_ckpt_c2v003')
    try:
        cm._identity(solver_file=str(AUX['solver'][0]), inputs={}, caller=caller, fixed=None)
        verdict = 'NO_ERROR (unexpected)'
    except Refusal:
        raise
    except Exception as exc:
        verdict = '%s: %s' % (type(exc).__name__, exc)
    res['c2v003_identity_on_ngc_caller_keys'] = {'worker_builds_these_keys': built, 'caller_keys': sorted(caller), 'result': verdict}
    for k in ('checkpoint_c2v001', 'checkpoint_c2v002'):
        m = exec_verified(NGC_EVIDENCE[k][0], NGC_EVIDENCE[k][1], 'c2v002_ngc_' + k)
        res[k + '_FIXED_SOURCE_SELECTION_IDENTITY'] = getattr(m, 'FIXED_SOURCE_SELECTION_IDENTITY', None)
    s = exec_verified(NGC_EVIDENCE['solver_nonfixedsrc'][0], NGC_EVIDENCE['solver_nonfixedsrc'][1], 'c2v002_ngc_solver_nf')
    res['nonfixedsrc_solver_accepts_fixed_source_fourier_J'] = 'fixed_source_fourier_J' in inspect.signature(s.solve).parameters
    res['adapter_always_passes_fixed_source_fourier_J'] = b"fixed_source_fourier_J=prepared['fixed_source_fourier_J']" in texts['composite']
    prec = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(NGC_EVIDENCE['ddo_precedent_failure'][0])))
    res['precedent'] = {'run': str(NGC_EVIDENCE['ddo_precedent_failure'][0]), 'type': prec['type'], 'message': prec['message'], 'elapsed_seconds': prec['elapsed_seconds'], 'note': 'DDO stable-cached binding v001 lacked the same contract; v002 added it and then ran (RUN_V002)'}
    blocked = verdict.startswith('CheckpointError') and 'physical_parameters' in verdict and (not any(res['physical_parameters_or_numerical_controls_written_by'].values())) and (res['checkpoint_c2v001_FIXED_SOURCE_SELECTION_IDENTITY'] is not True) and (res['checkpoint_c2v002_FIXED_SOURCE_SELECTION_IDENTITY'] is not True) and (not res['nonfixedsrc_solver_accepts_fixed_source_fourier_J']) and res['adapter_always_passes_fixed_source_fourier_J']
    res['verdict'] = 'ROUTE_A_BLOCKED: every existing solver/checkpoint pairing fails before any column work (fixedsrc+c2v003: caller contract; fixedsrc+c2v001/2: no fixed-source identity; non-fixedsrc solver: no fixed_source_fourier_J parameter)' if blocked else 'NOT_DEMONSTRATED'
    res['blocked'] = blocked
    return res

def _cx3r007_strict_ngc_route_b_table_L4675(admission=None):
    """c2v004: rows of the five generalized stages locate the DDO literals in the reviewed BASE file (the
    successor reads them from the galaxy config) and carry the successor's own NGC admission result."""
    rows = []
    driver_text = _ngc_record_text_cx3r007(Path(__file__))
    adm = {a['stage']: a for a in (admission or {}).get('stages', [])}
    for stage, key, needles, hard, ngc, status in NGC_ROUTE_B_HARDCODING:
        gen = GENERALIZED.get(key) if key else None
        if key is None:
            path, text = (Path(__file__), driver_text.split('# ' + '=' * 77 + ' NGC3198 (c2v002)')[0])
        else:
            path = gen['base'][0] if gen else (SCRIPTS.get(key) or AUX.get(key))[0]
            text = _ngc_record_text_cx3r007(Path(path))
        lines = text.splitlines()
        loc = {n: [i + 1 for i, ln in enumerate(lines) if n in ln][:6] for n in needles}
        row = {'stage': stage, 'file': str(path), 'needle_lines': loc, 'ddo_hard_coding': hard, 'ngc_equivalent': ngc, 'status': status, 'key_is_driver': key is None}
        if gen:
            row['generalized_successor'] = {'path': str(SCRIPTS[key][0]), 'sha256': SCRIPTS[key][1]}
            row['successor_admission_ngc'] = adm[key]['admission'] if key in adm else 'NOT_PROBED'
            row['status'] = 'C2V005_SUCCESSOR_ADMITS_NGC' if isinstance(row['successor_admission_ngc'], dict) and row['successor_admission_ngc'].get('accepted') else 'C2V005_SUCCESSOR_REFUSES_NGC_IN_THIS_ROUTE_A_CONFIG (route-B call: see the c2v005 route-B dry run)'
        rows.append(row)
    return rows

def _cx3r007_strict_ngc_remaining_refusals_L4768(contract, admission, hard):
    """c2v004: every refusal that stands between the NGC3198 seed call and 43 route-B rows, from bytes."""
    out = [{'where': 'route_a', 'refusal': contract['verdict'], 'source': 'ngc_caller_contract_check (real modules, synthetic caller)'}]
    for name, why in NGC_NOT_GENERALIZED.items():
        out.append({'where': name, 'refusal': 'NOT_GENERALIZED: ' + why, 'source': 'route_b_hardcoding'})
    for a in (admission or {}).get('stages', []):
        if not a['admission']['accepted']:
            out.append({'where': a['stage'], 'refusal': a['admission']['refusal'], 'source': 'successor admission function on ' + Path(a['config']['path']).name})
    for r in hard:
        if r['key_is_driver'] and r['status'].startswith('BLOCKER'):
            out.append({'where': 'driver ' + r['stage'], 'refusal': r['status'] + ': ' + r['ngc_equivalent'], 'source': 'route_b_hardcoding'})
    for b in binding_blockers():
        out.append({'where': 'binding', 'refusal': b, 'source': 'binding_blockers (applies to every galaxy)'})
    schema = _ngc_json_loads_cx3r007(_ngc_record_bytes_cx3r007(Path(GC_SCHEMA[0])))
    for s in schema.get('structural_findings', []):
        out.append({'where': 'structural ' + s['id'], 'refusal': s['title'], 'source': 'GALAXY_CONFIG_SCHEMA_V002 structural_findings (= V001)'})
    return out

def _cx3r007_strict_ngc_read_route_a_result_L4788(result_path, finish_path, manifest_path=None):
    """Read a (future) NGC43 route-A result: 43 speeds keyed NGC3198-Q01..Q43 in manifest order,
    validity, and DIAGNOSTIC m>=1 content of the azimuth-resolved trial (no acceptance threshold).
    Reads only the worker's own outputs and the target-free manifest."""
    import numpy as np
    manifest_path = manifest_path or NGC_DATA['manifest'][0]
    man = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(manifest_path)))
    _ngc_validate_manifest_rows_cx3r007(man, manifest_path)
    ids = [r['query_id'] for r in man['rows']]
    rad = {r['query_id']: r['Rad_text'] for r in man['rows']}
    reasons = []
    fin = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(finish_path)))
    if fin.get('status') != 'RETURNED_ACTUAL_RESULT':
        reasons.append('worker status %s' % fin.get('status'))
    if sha256_file(result_path) != fin.get('result_sha256'):
        reasons.append('result sha256 differs from worker finish.json')
    ra = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(result_path)))
    x = ra['result']['result']
    sfp = x.get('source_fixed_point') if isinstance(x.get('source_fixed_point'), dict) else {}
    ro1, ro1_fired = ro1_outcome(ra, x, result_path, sfp.get('converged_finite_fixed_point') is True and (sfp.get('checkpoint') or {}).get('outcome') == ROUTE_A_CONVERGED)
    if ro1_fired:
        reasons.append('RO1: route-A circular-trial readout refused after a converged fixed point (%s); no route-A rows' % ro1['events'][0].get('refusal'))
        return {'rows': None, 'speeds_km_s': None, 'valid': False, 'reasons': reasons, 'ro1': ro1, 'validity_definition': 'worker RETURNED_ACTUAL_RESULT, result sha matches, 43 manifest ids in order, finite speeds, converged source fixed point, predictions_available', 'm_ge_1_diagnostics': None, 'dynamics_status': x.get('dynamics_status'), 'accepted_for_calibration': False, 'route': 'ROUTE_A_ONLY (route B blocked)'}
    rows = x['rows']
    if [r['id'] for r in rows] != ids:
        reasons.append('row ids are not the 43 manifest ids in order')
    speeds = [r['speed_km_s'] for r in rows]
    if not all((isinstance(v, (int, float)) and math.isfinite(v) for v in speeds)):
        reasons.append('nonfinite speed')
    if x.get('source_fixed_point', {}).get('converged_finite_fixed_point') is not True:
        reasons.append('route-A source fixed point not converged')
    if x.get('predictions_available') is not True:
        reasons.append('predictions_available is not True')
    per_q, gmax = ([], {})
    for q in x.get('query_physics', []):
        nodes = q['nodes']
        n = len(nodes)
        phi = np.array([nd['phi_rad'] for nd in nodes])
        v = np.array([nd['v'] for nd in nodes], dtype=float)
        equal = bool(np.allclose(phi, 2 * np.pi * np.arange(n) / n, rtol=0, atol=1e-12))
        F = np.abs(np.fft.rfft(v))
        ratios = {'m%d' % m: float(F[m] / F[0]) if F[0] > 0 else None for m in range(1, len(F))}
        for k, val in ratios.items():
            if val is not None:
                gmax[k] = max(gmax.get(k, 0.0), val)
        eul = np.array([nd['Euler_covector_residual_R_phi_z'] for nd in nodes], dtype=float)
        cont = [abs(r) for nd in nodes for r in nd['mass_continuity']['fractional_density_rate_per_s']]
        per_q.append({'id': q['id'], 'n_azimuths': n, 'equal_angle_nodes': equal, 'speed_m_s_azimuth_harmonic_ratio': ratios, 'speed_m_s_azimuth_range': float(v.max() - v.min()), 'Euler_residual_abs_max_R_phi_z': [float(a) for a in np.max(np.abs(eul), axis=0)], 'continuity_fractional_rate_abs_max_per_s': float(max(cont)) if cont else None})
    valid = not reasons and len(rows) == 43
    return {'rows': [{'id': r['id'], 'Rad_text_kpc': rad.get(r['id']), 'speed_km_s': r['speed_km_s']} for r in rows], 'speeds_km_s': {r['id']: r['speed_km_s'] for r in rows}, 'valid': valid, 'reasons': reasons, 'validity_definition': 'worker RETURNED_ACTUAL_RESULT, result sha matches, 43 manifest ids in order, finite speeds, converged source fixed point, predictions_available', 'm_ge_1_diagnostics': {'quantity': '|FFT_m(v)|/|FFT_0(v)| of the circular trial speed over the observation azimuths; max |Euler residual| (R,phi,z) and |continuity rate| per query', 'global_max_harmonic_ratio': gmax, 'per_query': per_q, 'status': 'DIAGNOSTIC_ONLY'}, 'dynamics_status': x.get('dynamics_status'), 'accepted_for_calibration': False, 'route': 'ROUTE_A_ONLY (route B blocked)'}

def _cx3r007_strict__ngc_v011_seed_L5087(nspec):
    p, s = _ngc_v011_pin('seed_v002')
    base = _ngc_json_loads_cx3r007(_ngc_record_bytes_cx3r007(p))
    ni = copy.deepcopy(base['numerical_inputs'])
    phys = nspec['physical']
    scale = phys['common_scale_s']
    num = nspec['numerics']
    ni.update(Eref_J=scale * phys['Eref_J'], ell_F_m=phys['ell_F_m'], gamma=scale * phys['gamma'], composite_grid_spec=None, composite_grid_spec_anisotropic=num['composite_grid_spec_anisotropic'], fourier_points_per_axis=120, ngc_outer_gas_cut=num.get('ngc_outer_gas_cut'), max_iterations=num['route_a']['max_iterations'], source_gauss_order=10 if nspec.get('member') == 'GL10_ALTERNATIVE' else 4)
    pins = {str(p): s}
    for k in ('manifest', 'profile', 'h2_tail_reduction', 'h2_source'):
        q, t = NGC_DATA[k]
        verify_pin(q, t, k)
        pins[str(q)] = t
    q, t = (nspec['coefficients']['path'], nspec['coefficients']['sha256'])
    verify_pin(q, t, 'NGC seed actual coefficients')
    pins[str(q)] = t
    if ni['ngc_outer_gas_cut'] is not None:
        pins[ni['ngc_outer_gas_cut']['path']] = ni['ngc_outer_gas_cut']['sha256']
    return {'status': 'NGC_V011_SOURCE_BUILD_TARGET_FREE_SEED', 'numerical_inputs': ni, 'pins': pins, 'coefficients': dict(nspec['coefficients']), 'parent_seed': {'path': str(p), 'sha256': s}, 'parameter_provenance': {'base': 'NGC v002 A2F10', 'changes': 'call physical parameters; T120L; registered GL member; optional certified cut'}, 'scope': 'No target velocities; new checkpoint required for changed numerical inputs'}

def _cx3r007_strict_cmd_dry_run_L5144(spec_path, report_dir):
    code = _ngc_v011_dispatch(_V010_DRY, spec_path, report_dir)
    rp = Path(report_dir) / 'DRYRUN_REPORT.json'
    if code == 0 and rp.is_file():
        report = _ngc_json_loads_cx3r007(_ngc_record_bytes_cx3r007(rp))
        sp = report['normalized_spec']
        if sp.get('galaxy') == 'NGC3198' and 'uv_tail' in sp.get('numerics', {}):
            items = report['remaining_refusals']['items']
            produces = sp.get('_ngc_produces_route_a')
            expected = [r for r in items if produces and r['class'] == 'PENDING_ROUTE_A_OUTPUTS']
            blockers = [r for r in items if r not in expected]
            record = {'status': 'SOURCE_BUILD_DRY_RUN_ONLY', 'executed_stages': 0, 'report': {'path': str(rp), 'sha256': sha256_file(rp)}, 'binding_blockers': report['binding_blockers'], 'source_build_blockers': blockers, 'future_stage_dependencies': expected, 'dependency_rule': 'Only custody outputs of the planned route-A and route-B stages are deferred; stage pin/schema/physical refusals remain blockers.', 'planned_route_a': any((r['kind'] == 'route_a' for r in report['stages'])), 'monitor': 'NGC M_T_NOT_NORMALIZED; raw source monitor only. No NGC forward v_ref or tau supplied; no convergence claim.', 'readiness': 'PENDING_CERTIFICATES' if not report['binding_blockers'] and all((r['class'] == 'PENDING_UV_TAIL_CERTIFICATE' for r in blockers)) else 'BLOCKED'}
            _write_x(Path(report_dir) / 'NGC_SOURCE_BUILD_READINESS.json', record)
    return code

def _cx3r007_strict_uvt_binding_blockers_L5183(nodes=False):
    if not _NGC_V011_ACTIVE:
        return _V010_UVT_BLOCKERS(nodes)
    out = []
    bp, bs = _ngc_v011_pin('route_b_binding')
    for k, (p, s) in V011_B_STAGES.items():
        try:
            verify_pin(p, s, 'NGC stage ' + k)
            t = _ngc_record_text_cx3r007(Path(p))
            if k != 'column_mean_v004' and bs not in t:
                out.append('NGC_STAGE_BINDING_PIN ' + k)
            if k == 'column_mean_v004' and ('ngc_outer_gas_cut_custody' not in t or 'QUERY_BEYOND_OUTER_GAS_CUT' not in t):
                out.append('NGC_COLUMN_MEAN_CUT_CUSTODY_ABSENT')
        except Refusal as e:
            out.append(str(e))
    for k in ('worker', 'worker_parallel'):
        p, s = _ngc_v011_pin(k)
        t = _ngc_record_text_cx3r007(p)
        for dep in ('prep', 'binding', 'prediction'):
            if V011_PINS[dep][1] not in t:
                out.append('NGC_WORKER_PIN ' + k + ' ' + dep)
        if AUX_UVT['controller'][1] not in t:
            out.append('NGC_WORKER_CONTROLLER_PIN ' + k)
    for k in ('route_b_binding', 'manifest_writer'):
        p, s = _ngc_v011_pin(k)
        if k == 'manifest_writer' and AUX_UVT['controller'][1] not in _ngc_record_text_cx3r007(p):
            out.append('NGC_MANIFEST_CONTROLLER_PIN')
    return out

def _cx3r007_strict__execute_ngc_v011_chain_L5315(ctx):
    sp = ctx.spec
    gname = sp['galaxy']
    g = GALAXIES[gname]
    ngc = gname != 'DDO154'
    sv = ctx.saved
    uvt = uvt_info(sp['numerics']['uv_tail']) if 'uv_tail' in sp['numerics'] else None
    uvt_act = uvt_active(uvt_is_nodes(sp['numerics'].get('uv_tail')))
    uvt_extra = uvt_act['scripts'] if uvt is not None else None
    uvx = None
    ro1_off = uvt is None and route_a_ro1_workers(sp)
    if uvt is not None:
        ctx.scripts = dict(SCRIPTS, **uvt_act['scripts'], route_a_tail_manifest=uvt_act['aux']['manifest_writer'])
    P = sp['numerics']['picard']['passes']
    bound = sp['numerics']['picard']['speed_change_bound_km_s']
    workers = sp['numerics']['column_workers']
    brackets = sp['numerics']['brackets']
    ef = sp['physical']['entropy_K_factor']
    efs = repr(ef)
    coeff_path, coeff_sha = (sp['coefficients']['path'], sp['coefficients']['sha256'])
    verify_pin(coeff_path, coeff_sha, 'coefficient grid')
    gc = load_galaxy_config(gname, sp.get('member'))
    refusals = []

    def refuse(where, cls, msg):
        """c2v005: a remaining refusal.  Run mode: BLOCKED before any further stage.  Simulate: recorded, planning goes on."""
        refusals.append({'where': where, 'class': cls, 'refusal': msg})
        if ctx.mode == 'run':
            raise Blocked('%s [%s]: %s' % (where, cls, msg))
    info = {}
    if not ngc:
        seed_obj, changed, reusable = per_call_seed(sp)
        if reusable:
            seed_path, seed_sha = g['base_seed']
        else:
            seed_path, seed_sha = ctx.write_input('seed_c2v001.json', seed_obj)
        seed_path = Path(seed_path)
        ni = seed_obj['numerical_inputs']
        info['seed'] = {'path': str(seed_path), 'sha256': seed_sha, 'base_seed_reused': reusable, 'changed_fields': changed}
        literal_rows = ddo_driver_literal_check(g, gc)
    else:
        literal_rows = ngc_driver_value_check(g, gc)
        ra_in = sp['route_a_inputs']
        if sp.get('_ngc_produces_route_a'):
            seed_doc = _ngc_v011_seed(sp)
            seed_path, seed_sha = ctx.write_input('ngc_seed_v011.json', seed_doc)
            ni = seed_doc['numerical_inputs']
        elif route_a_inputs_pending(ra_in):
            seed_path, seed_sha, ni = (Path('%s(seed path)' % PENDING_ROUTE_A), '%s(custody.seed_sha256)' % PENDING_ROUTE_A, None)
            refuse('route_a', 'PENDING_ROUTE_A_OUTPUTS', 'NGC3198 route-A outputs (seed, attempt, checkpoint) are not supplied yet; route B consumes them from the NGC route-A lane (route A is not run by this driver)')
            for where, what in NGC_DEFERRED_ROUTE_A_CHECKS:
                refuse(where, 'PENDING_ROUTE_A_OUTPUTS', 'needs route-A bytes: ' + what)
            info['route_a_inputs_declared'] = ra_in
        else:
            seed_path = Path(ra_in['seed']['path'])
            seed_sha = verify_pin(seed_path, ra_in['seed']['sha256'], 'NGC route-A seed')
            seed_doc = _ngc_json_loads_cx3r007(_ngc_record_bytes_cx3r007(seed_path))
            ni = seed_doc['numerical_inputs']
            info['route_a_seed_coefficients'] = ngc_seed_coefficient_check(seed_doc, sp['coefficients'], g)
        info['seed'] = {'path': str(seed_path), 'sha256': seed_sha, 'source': 'route_a_inputs.seed (NGC route-A lane)'}
        info['member'] = {'member': sp.get('member'), 'label': 'PRIMARY' if sp.get('member') is None else gc['schema']['members']['NGC3198'][sp['member']]['label'], 'entropy_K_member': sp['physical'].get('entropy_K_member')}
    info['galaxy_config'] = {'path': gc['path'], 'sha256': gc['sha256'], 'driver_literal_check': literal_rows}
    if ni is not None:
        if ni['kpc_m'] != KPC_M:
            raise Refusal('seed kpc_m differs from driver constant')
        call_phys = {k: ni[k] for k in ('Eref_J', 'ell_F_m', 'gamma')}
        if ngc:
            s = sp['physical']['common_scale_s']
            want = {'Eref_J': s * sp['physical']['Eref_J'], 'gamma': s * sp['physical']['gamma'], 'ell_F_m': sp['physical']['ell_F_m']}
            if any((call_phys[k] != want[k] for k in want)):
                raise Refusal('NGC3198: call physical parameters (times s) differ from the route-A seed numerical_inputs')
    else:
        call_phys = None
    tr = sp['numerics']['truncation']
    if ni is not None:
        kgrid = _ngc_v011_grid_edge(ni)
        if tr['kmax_inverse_kpc'] is not None and tr['kmax_inverse_kpc'] > kgrid:
            raise Refusal('mask kmax exceeds the composite grid edge %.6g/kpc' % kgrid)
        kmask_m = (tr['kmax_inverse_kpc'] if tr['kmax_inverse_kpc'] is not None else kgrid) / KPC_M
    else:
        kmask_m = None
    coeff_default = coeff_path == str(g['default_coefficients'][0]) and coeff_sha == g['default_coefficients'][1]
    reuse_path, reuse_sha = GENERALIZED['reference']['base']
    percall = {'custody.seed_sha256': seed_sha, 'source.coefficients': {'path': str(coeff_path), 'sha256': coeff_sha}}
    for k in gc['slots']:
        v = (sp.get('source_slots') or {}).get(k, PENDING_SLOT)
        percall[k] = v
        if _has_pending(v):
            refuse(k, 'PENDING_N3_MONOTONE_SOURCE', '%s is a DECLARED_INPUT_SLOT (N3) not yet filled by the reviewed reducer output' % k)
    gc_written = {}
    gfields = {}

    def stage_gc(kind, tag='', producers=None):
        """Write (once per name) the per-stage config of successor `kind`; returns (path, sha, meta)."""
        name = 'galaxy_config_%s%s.json' % (kind, '_' + tag if tag else '')
        if name in gc_written:
            return gc_written[name]
        missing = [k for k in STAGE_PER_CALL[kind] if k not in percall]
        if missing:
            raise Refusal('c2v005 internal: per-call fields %s not yet computed for %s' % (missing, kind))
        pc = {k: percall[k] for k in STAGE_PER_CALL[kind]}
        pc.update({k: percall[k] for k in gc['slots'] if k in consumed_fields(kind)})
        pc.update({k: v for k, v in gfields.items() if k in consumed_fields(kind)})
        obj, omitted = stage_config_object(kind, gc, pc, omit_missing_per_call=True, producers=producers)
        pending = sorted((k for k, v in pc.items() if _has_pending(v)))
        if producers is not None and _has_pending(producers):
            pending.append('producer_pins')
        meta = {'format': GENERALIZED[kind]['format'], 'galaxy_config_file': {'path': gc['path'], 'sha256': gc['sha256']}, 'per_call_fields': sorted(pc), 'omitted_per_call_fields': omitted}
        if producers is not None:
            meta['producer_pins'] = producers
        if pending:
            p = ctx.out / 'inputs' / name
            s = 'PENDING_SHA256(%s)' % p
            meta.update(path=str(p), sha256=s, written=False, pending_fields=pending)
            if ctx.mode != 'run':
                meta['pending_probe'] = pending_probe(kind, gc, pc, producers, ctx.out / 'inputs', tag)
        else:
            p, s = ctx.write_input(name, obj)
            meta.update(path=str(p), sha256=s, written=True)
        gc_written[name] = (p, s, meta)
        return gc_written[name]

    def gen_request(name, key, argv, tag='', module_patches=None, mask=None, producers=None, stage_globals=None):
        """Request for a gal_c2v003 successor: c2v003 argv + galaxy-config tokens appended; no stage globals (C2V008 (a):
        except the reference PROFILE/PROFILE_SHA at a per-call geometry, as c2v003c)."""
        p, s, meta = stage_gc(key, tag, producers)
        req = ctx.request(name, key, list(argv) + galaxy_config_argv(key, p, s), stage_globals=stage_globals or {}, module_patches=module_patches, mask=mask)
        req['galaxy_config'] = meta
        return req
    producer_log = []

    def producer(dirs, key, flag, stage, admitted=False):
        """c2v004 rule: sha of the script that produced the upstream output(s).  run: SCRIPTS[key] (this call ran it);
        simulate on SAVED outputs, or an ADMITTED upstream in any mode (c2v005): the worker_sha256 recorded in their
        start.json, which must be the successor or its reviewed base."""
        run_value = ctx.scripts[key][1]
        val, src = (run_value, 'SCRIPTS[%s] (this call runs it)' % key)
        if ctx.mode != 'run' or admitted:
            recs = [Path(x) / 'start.json' for x in dirs]
            have = [p for p in recs if p.is_file()]
            if have:
                vals = {_ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(p))['worker_sha256'] for p in have}
                if len(have) != len(recs) or len(vals) != 1:
                    raise Refusal('c2v005: mixed upstream producers for %s %s' % (stage, flag))
                val, src = (vals.pop(), 'worker_sha256 recorded in the %s upstream start.json' % ('admitted' if admitted else 'saved'))
                producer_pin(key, val, uvt_extra)
            elif admitted:
                raise Refusal('c2v005: admitted %s output has no start.json to name its producer' % key)
        producer_log.append({'stage': stage, 'flag': flag, 'value': val, 'source': src, 'run_mode_value': run_value, 'run_mode_differs': val != run_value})
        return val
    if not ngc:
        nk = int(ni['fourier_points_per_axis'])
        if nk <= PREP_V007_MAX_AXIS_NODES:
            prep_key = 'prep'
        elif nk <= PREP_V008_MAX_AXIS_NODES:
            prep_key = 'prep_v008'
            verify_pin(PREP_V008_REVIEW[0], PREP_V008_REVIEW[1], 'prep V008 review')
        elif nk <= PREP_V009_MAX_AXIS_NODES:
            prep_key = 'prep_v009'
        else:
            raise Refusal('%d nodes/axis exceeds every route-A prep budget (%d)' % (nk, PREP_V009_MAX_AXIS_NODES))
        prep_path, prep_sha = AUX[prep_key]
        prep_info = {'path': str(prep_path), 'sha256': prep_sha, 'axis_nodes': nk, 'rule': 'V007 for <=%d nodes/axis (unchanged); V008 for %d..%d (review %s)' % (PREP_V007_MAX_AXIS_NODES, PREP_V007_MAX_AXIS_NODES + 1, PREP_V008_MAX_AXIS_NODES, PREP_V008_REVIEW[1][:16])}
        if prep_key == 'prep_v009':
            prep_info['rule'] += '; V009 for %d..%d (declared G5/G6 only; review: separate, named by prereg V006)' % (PREP_V008_MAX_AXIS_NODES + 1, PREP_V009_MAX_AXIS_NODES)
    geo = geometry_inputs(ctx, sp) if not ngc else None
    profile_sha = None if ngc else geo['profile'][1] if geo is not None else g['profile'][1]
    if not ngc:
        src_path, src_sha = geo['monotone'] if geo is not None else g['monotone_source']
    if geo is not None:
        gfields.update(geometry_config_fields(geo))
        probe = geometry_admission_probe(ctx, gc, gfields)
        info['geometry'] = dict(geo['record'], config_fields=gfields, stage_admission_probe=probe)
        ctx.geometry = info['geometry']
        if not probe['admitted']:
            refuse('geometry', 'GEOMETRY_NOT_ADMITTED_BY_STAGE_BINDING', 'distance_Mpc %r != registered %r: the pinned gal_c2v005 stages refuse the per-call geometry config fields (their own admission, schema V005): %s%s. No stage is run.' % (sp['physical']['distance_Mpc'], g['registered_geometry']['distance_Mpc'], '; '.join(('%s: %s' % kv for kv in sorted(probe['refused'].items()))), '' if probe['controls_accepted'] else ' (registered-geometry control copies also refused)'))
    if ngc:
        prep_key = 'ngc_v011'
        prep_path, prep_sha = _ngc_v011_pin('prep')
        prep_info = {'path': str(prep_path), 'sha256': prep_sha, 'axis_nodes': [120, 120, 80], 'rule': 'NGC registered T120L successor'}
    if uvt is not None:
        uvx = _uvt_ngc_v011_plan(ctx, sp, ni, refuse, uvt_prep_patches(coeff_default, coeff_path, coeff_sha, geo, prep_path, prep_sha))
        ctx.uv_tail = uvx
    adm = sp.get('admit') or {}
    if ngc and (not sp.get('_ngc_produces_route_a')):
        ra_in = sp['route_a_inputs']
        if route_a_inputs_pending(ra_in):
            att, cp = (Path('%s(attempt_directory)' % PENDING_ROUTE_A), Path('%s(checkpoint_directory)' % PENDING_ROUTE_A))
            info['route_a'] = {'mode': 'pending_ngc_route_a_lane', 'attempt': str(att), 'checkpoint': str(cp), 'declared': ra_in if isinstance(ra_in, dict) else None}
        else:
            att, cp = (Path(ra_in['attempt_directory']), Path(ra_in['checkpoint_directory']))
            fin = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(att / 'finish.json'))
            if fin['status'] != 'RETURNED_ACTUAL_RESULT' or sha256_file(att / 'result.json') != ra_in['result_sha256'] or fin['result_sha256'] != ra_in['result_sha256']:
                raise Refusal('NGC route-A attempt does not verify')
            info['route_a'] = {'mode': 'admitted_ngc_route_a_lane', 'attempt': str(att), 'checkpoint': str(cp)}
    elif 'route_a' in adm:
        a = adm['route_a']
        att, cp = (Path(a['attempt_directory']), Path(a['checkpoint_directory']))
        fin = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(att / 'finish.json'))
        if fin['status'] != 'RETURNED_ACTUAL_RESULT' or sha256_file(att / 'result.json') != a['result_sha256'] or fin['result_sha256'] != a['result_sha256']:
            raise Refusal('admitted route-A attempt does not verify')
        info['route_a'] = {'mode': 'admitted', 'attempt': str(att), 'checkpoint': str(cp)}
    else:
        d = ctx.stage_dir('route_a')
        sa = sv.get('route_a') or {} if ctx.mode != 'run' else {}
        att = Path(sa['attempt']) if 'attempt' in sa else d / 'attempt_000'
        cp = Path(sa['checkpoint']) if 'checkpoint' in sa else d / 'checkpoint'
        patches = []
        prep_set = {}
        if not coeff_default:
            prep_set.update({'COEFFICIENT': {'__path__': coeff_path}, 'COEFFICIENT_SHA': coeff_sha})
        if geo is not None:
            prep_set['C'] = {'__path__': geo['C_dir']}
        if prep_set:
            patches.append({'path': str(prep_path), 'sha256': prep_sha, 'set': prep_set})
        ra_workers = route_a_column_workers(sp)
        solver_pin = AUX['solver'] if ra_workers == 1 else PARALLEL_ROUTE_A['solver']
        if uvt is not None:
            solver_pin = uvt_act['aux']['solver'] if ra_workers == 1 else uvt_act['aux']['solver_parallel']
        ra_argv = ['--seed', seed_path, '--seed-sha256', seed_sha, '--solver', solver_pin[0], '--solver-sha256', solver_pin[1], '--checkpoint-module', AUX['checkpoint_module'][0], '--checkpoint-module-sha256', AUX['checkpoint_module'][1], '--outdir', att, '--checkpoint-directory', cp, '--start-iteration', '0']
        if ra_workers > 1:
            ra_argv += ['--column-workers', str(ra_workers)]
        if uvt is not None:
            ra_argv += uvx['route_a_argv'] + ['--uv-tail-sidecar-directory', d / 'uv_tail_sidecar']
        if ro1_off:
            off_p, off_s = ctx.write_input('uv_tail_route_a_request_tail_off_ro1.json', ro1_off_request())
            ra_argv += ['--uv-tail-config', off_p, '--uv-tail-config-sha256', off_s, '--eps-certificate', UVT_TEST_ONLY, '--eps-certificate-sha256', UVT_TEST_ONLY, '--lo-certificate', UVT_TEST_ONLY, '--lo-certificate-sha256', UVT_TEST_ONLY, '--uv-tail-sidecar-directory', d / 'uv_tail_sidecar']
        req = ctx.request('route_a', 'route_a', ra_argv, module_patches=patches)
        if ra_workers > 1:
            req['script'], req['script_sha256'] = (str(PARALLEL_ROUTE_A['worker'][0]), PARALLEL_ROUTE_A['worker'][1])
        if uvt is not None:
            w = uvt_act['route_a']['worker'] if ra_workers == 1 else uvt_act['route_a']['worker_parallel']
            req['script'], req['script_sha256'] = (str(w[0]), w[1])
        if ro1_off:
            w = RO1_ROUTE_A['worker'] if ra_workers == 1 else RO1_ROUTE_A['worker_parallel']
            req['script'], req['script_sha256'] = (str(w[0]), w[1])
        if prep_key in ('prep_v008', 'prep_v009'):
            req['stage_dict_items'] = {'LOCAL': {'prep': {'path': str(prep_path), 'sha256': prep_sha}}}
        ctx.run_stages([req], [d])
        info['route_a'] = {'mode': 'computed', 'attempt': str(att), 'checkpoint': str(cp)}
        info['route_a']['implementation'] = {'column_workers': ra_workers, 'kind': 'REVIEWED_SERIAL' if ra_workers == 1 else 'PARALLEL_C2V001', 'worker': {'path': req['script'], 'sha256': req['script_sha256']}, 'solver': {'path': str(solver_pin[0]), 'sha256': solver_pin[1]}}
        if uvt is not None:
            info['route_a']['implementation']['kind'] = ('UVTAIL_NODES_RO1_SERIAL_C2V001' if ra_workers == 1 else 'UVTAIL_NODES_RO1_PARALLEL_C2V001') if uvt_is_nodes(sp['numerics'].get('uv_tail')) else 'UVTAIL_RO1_SERIAL_C2V001' if ra_workers == 1 else 'UVTAIL_RO1_PARALLEL_C2V001'
        if ro1_off:
            info['route_a']['implementation']['kind'] = 'TAIL_OFF_RO1_SERIAL_C2V010R4' if ra_workers == 1 else 'TAIL_OFF_RO1_PARALLEL_C2V010R4'
            info['route_a']['implementation']['ro1_workers'] = True
    if not ngc:
        info['route_a']['prep'] = dict(prep_info, role='used by this call' if info['route_a']['mode'] == 'computed' else 'expected for this grid; the admitted checkpoint records its own (custody.prep_code_pins)')
    att_res = Path(att) / 'result.json'
    ra = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(att_res)) if att_res.is_file() else None
    ra_outcome = route_a_outcome_record(ra, att_res) if ra is not None else None
    ctx.route_a_outcome = ra_outcome
    if ra_outcome is not None:
        info['route_a']['outcome'] = ra_outcome
    expected_solver = solver_pin if info['route_a']['mode'] == 'computed' and ctx.mode == 'run' else None
    if (Path(cp) / 'IDENTITY.json').is_file():
        cust = route_a_custody(cp, seed_sha, coeff_path, call_phys, outcome=ra_outcome, expected_solver=expected_solver, profile_sha=profile_sha, attempt_result=ra)
        if 'route_a' in adm and cust['identity_sha256'] != adm['route_a']['identity_sha256']:
            raise Refusal('admitted checkpoint identity differs from declared')
        if ngc and (not sp.get('_ngc_produces_route_a')) and (cust['identity_sha256'] != sp['route_a_inputs']['identity_sha256']):
            raise Refusal('NGC route-A checkpoint identity differs from route_a_inputs.identity_sha256')
        if uvt is None:
            uvt_route_a_identity_check(cp, None)
        elif uvt['config_sha256'] is not None:
            uvx['route_a_checkpoint_tail'] = uvt_route_a_identity_check(cp, uvt['config_sha256'])
        else:
            uvx['route_a_checkpoint_tail'] = 'PENDING (certificate sentinel: config sha unknown)'
    else:
        if not ngc and info['route_a']['mode'] == 'admitted':
            raise Refusal('ROUTE_A_CHECKPOINT_MISSING: %s/IDENTITY.json absent; admitted attempt cannot be paired (D1)' % cp)
        if info['route_a']['mode'] == 'computed' and ctx.mode == 'run' and (ra_outcome is not None):
            raise StageFailed('ROUTE_A_RESULT_WITHOUT_CHECKPOINT: %s' % cp)
        if ra_outcome is not None:
            require_route_a_fixed_point(ra_outcome)
        if ngc and (not route_a_inputs_pending(sp['route_a_inputs'])):
            raise Refusal('NGC route-A checkpoint IDENTITY.json missing under %s' % cp)
        cust = {'identity_sha256': '%s(custody.checkpoint_identity_sha256)' % PENDING_ROUTE_A if ngc else 'PENDING(route_a identity)', 'iteration': '%s(route_a.accepted_iteration)' % PENDING_ROUTE_A if ngc else 'PENDING(route_a iteration)', 'start_payload_sha256': 'PENDING', 'g4_ref': {'file_sha256': 'PENDING'}, 'waves_ref': None}
    info['route_a']['custody'] = cust
    if ra is not None:
        info['route_a']['route_a_rows'] = ra['result']['result']['rows']
        if geo is not None:
            info['route_a']['route_a_rows_scope'] = geo['record']['route_a_rows']
    if uvt is not None:
        u = ((ra or {}).get('result') or {}).get('uv_tail') if ra is not None else None
        if ra is not None and (not isinstance(u, dict)):
            raise StageFailed('UV_TAIL_ROUTE_A_RECORD_MISSING: %s has no result.uv_tail (a tail-OFF route A in a tail-ON call?)' % att_res)
        if isinstance(u, dict) and uvt['config_sha256'] is not None and (u.get('config_sha256') != uvt['config_sha256']):
            raise Refusal('UVT_ADMISSION_MISMATCH: route-A result tail config %r is not this call config %s' % (u.get('config_sha256'), uvt['config_sha256']))
        uvx['route_a_record'] = None if not isinstance(u, dict) else {k: u.get(k) for k in ('outcome', 'accepted_iteration', 'M_T_accepted', 'M_T_threshold', 'monitor_status', 'flags', 'production_admissible', 'boundary_state_digest_at_return', 'config_sha256', 'request_sha256', 'admissibility', 'E_A_rows_km_s_accepted', 'sidecar')}
        if uvx['route_a_record'] is not None:
            uvx['route_a_record'].update(probe_R_m=list(uvx['monitor_probe_R_m']), probe_phi_rad=list(uvx['monitor_probe_phi_rad']), probe_source='uv_tail request monitor (binding f42c7c65 query_rows[].radius_m; seed azimuths)')
        d = ctx.stage_dir('route_a_tail_manifest')
        mdir = d / 'manifest'
        margv = ['--seed', seed_path, '--seed-sha256', seed_sha, '--attempt-directory', att, '--checkpoint-directory', cp, '--checkpoint-module', AUX['checkpoint_module'][0], '--checkpoint-module-sha256', AUX['checkpoint_module'][1], '--uv-tail-request', uvx['request']['path'], '--uv-tail-request-sha256', uvx['request']['sha256'], '--outdir', mdir]
        mreq = ctx.request('route_a_tail_manifest', 'route_a_tail_manifest', margv, module_patches=uvx['prep_patches'])
        if prep_key in ('prep_v008', 'prep_v009'):
            mreq['stage_dict_items'] = {'LOCAL': {'prep': {'path': str(prep_path), 'sha256': prep_sha}}}
        ctx.run_stages([mreq], [d])
        uvx['manifest'] = {'path': str(mdir / 'ROUTE_A_TAIL_MANIFEST.json'), 'sha256': ctx.finish_sha(mdir, 'ROUTE_A_TAIL_MANIFEST.json')}
        if (mdir / 'finish.json').is_file():
            mf = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(mdir / 'finish.json'))
            uvx['manifest'].update(state_digest=mf.get('state_digest'), empty=mf.get('empty'), production_admissible=mf.get('production_admissible'))

    def uvt_argv(kind, source_rotation=None):
        """C2V010 (u): the tail argv of a route-B uvt successor ([] when tail OFF): config, manifest (reference, body,
        offset), the call truncation for the masked kinds, the source rotation (rfs/le columns, le rotation)."""
        if uvt is None:
            return []
        bk = UVT_BINDING_KIND[kind]
        a = ['--uv-tail-config', uvx['config']['path'], '--uv-tail-config-sha256', uvx['config']['sha256']] + uvx['test_only_flag']
        if bk in ('reference', 'body', 'offset'):
            a += ['--route-a-tail-manifest', uvx['manifest']['path'], '--route-a-tail-manifest-sha256', uvx['manifest']['sha256']]
        if bk not in ('reference', 'body') and uvx['truncation_argv'] is not None:
            a += ['--uv-tail-truncation', uvx['truncation_argv']]
        if bk in ('rfs_columns', 'le_columns', 'le_rotation'):
            a += ['--uv-tail-source-rotation-directory', source_rotation]
        return a
    ident = cust['identity_sha256']
    it = cust['iteration']
    info['route_a']['reported_final_iteration'] = it
    percall['custody.checkpoint_identity_sha256'] = ident
    percall['route_a.accepted_iteration'] = it
    reuse_patch = {'path': str(reuse_path), 'sha256': reuse_sha, 'set': {'SEED_SHA': seed_sha, 'IDENTITY': ident}}
    ref_globals = None
    if geo is not None:
        ref_globals = {}
        for target in (reuse_patch['set'], ref_globals):
            target.update(PROFILE={'__path__': geo['profile'][0]}, PROFILE_SHA=geo['profile'][1])
    mask = None
    if tr['shape'] != 'cube':
        mask = {'shape': tr['shape'], 'kmax_inverse_m': kmask_m, 'g4_file_sha256': cust['g4_ref']['file_sha256'], 'waves_ref': cust['waves_ref'], 'checkpoint_module': [str(AUX['checkpoint_module'][0]), AUX['checkpoint_module'][1]], 'cache_module': [str(AUX['cache'][0]), AUX['cache'][1]]}
    common = ['--seed', seed_path, '--checkpoint-directory', cp]
    if ngc:
        fa, fa_ok, _ = gc_value(gc, 'driver.fixed_args')
        if fa_ok:
            FA = dict(fa)
        else:
            FA = {k: 'NONE_IN_REVIEWED_CODE(driver.fixed_args.%s)' % k for k in FIXED_ARGS}
            refuse('driver.fixed_args', 'UNDECIDED_NGC_FIELD', 'driver.fixed_args is NONE_IN_REVIEWED_CODE for NGC3198 (no ROOT_DECISIONS row)')
    else:
        FA = FIXED_ARGS
    if 'reference' in adm:
        ref = Path(adm['reference']['directory'])
        verify_pin(ref / 'start.json', adm['reference']['start_sha256'], 'admitted reference start')
        verify_pin(ref / 'finish.json', adm['reference']['finish_sha256'], 'admitted reference finish')
        if not ngc and _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(ref / 'start.json'))['source_custody']['sha256'] != profile_sha:
            raise Blocked('REFERENCE_GEOMETRY_MISMATCH: admitted reference was not built from this call source profile')
        r_t = uvt_admitted_record_check(ref / 'start.json', uvt, 'reference')
        if uvt is not None:
            uvx['admitted_reference_tail'] = r_t
    else:
        d = ctx.stage_dir('reference')
        ref = d / 'reference' if ctx.mode == 'run' else ctx.saved_or('reference', d / 'reference')
        req = gen_request('reference', 'reference', common + ['--reference-module', AUX['reference_module'][0], '--reference-sha256', AUX['reference_module'][1], '--outdir', ref] + uvt_argv('reference'), stage_globals=ref_globals)
        ctx.run_stages([req], [d])
    percall['custody.reference_run'] = {'directory': str(ref), 'start_sha256': ctx.finish_sha(ref, 'start.json'), 'finish_sha256': ctx.finish_sha(ref)}
    if 'body' in adm:
        body = Path(adm['body']['directory'])
        verify_pin(body / 'finish.json', adm['body']['finish_sha256'], 'admitted body finish')
        if not ngc and src_sha not in _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(body / 'start.json'))['input_pins'].values():
            raise Blocked('BODY_GEOMETRY_MISMATCH: admitted body was not built from this call monotone source')
        b_t = uvt_admitted_record_check(body / 'finish.json', uvt, 'body')
        if uvt is not None:
            uvx['admitted_body_tail'] = b_t
    else:
        d = ctx.stage_dir('body')
        body = d / 'body' if ctx.mode == 'run' else ctx.saved_or('body', d / 'body')
        req = gen_request('body', 'body', common + ['--outdir', body] + uvt_argv('body'), module_patches=[reuse_patch])
        ctx.run_stages([req], [d])
    body_fin = ctx.finish_sha(body)
    percall['custody.body_worker_sha256'] = producer([body], 'body', 'config custody.body_worker_sha256', 'offset', admitted='body' in adm)
    d = ctx.stage_dir('offset')
    off = d / 'offset' if ctx.mode == 'run' else ctx.saved_or('offset', d / 'offset')
    req = gen_request('offset', 'offset', common + ['--body-directory', body, '--body-finish-sha256', body_fin, '--wave-batch', FA['wave_batch'], '--position-batch', FA['position_batch'], '--outdir', off] + uvt_argv('offset'), module_patches=[reuse_patch], mask=mask)
    ctx.run_stages([req], [d])
    if mask is not None:
        tinfo = {'shape': tr['shape'], 'kmax_inverse_m': kmask_m, 'scope': 'route A, reference and body unmasked (cube G4); offset real-space total and updated_base_arrays full_fields/Phi0/angular_forcing/r0 are a MIXED field (see truncation_mask)'}
        if ctx.mode == 'run' or ((Path(off) / 'unit_response.npz').is_file() and (Path(off) / 'offset_prepared.npz').is_file()):
            tinfo['mask_check'] = mask_fired_check(off, tr['shape'], kmask_m)
            ctx.event(stage='offset', event='mask_check', kept_nodes=tinfo['mask_check']['kept_nodes'], total_nodes=tinfo['mask_check']['total_nodes'])
        else:
            tinfo['mask_check'] = 'PENDING (offset outputs not present in simulate mode)'
        info['truncation'] = tinfo
    off_fin = ctx.finish_sha(off)
    percall['custody.offset_finish_sha256'] = off_fin
    base = common + ['--offset-directory', off]
    verify_pin(g['solver_template'][0], g['solver_template'][1], 'solver template')
    template = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(g['solver_template'][0])))['solver']
    if ngc and ni is not None:
        info['solver_template_mapping'] = template_mapping_check(ni, template)
    n = g['n_columns_by_member'][sp.get('member')] if ngc else g['n_columns']

    def column_pass(tag, key, extra_args, plan_runs):
        """plan_runs: list of (controls_path, controls_sha) or ('GENERATE', controls_obj).  Returns run dirs."""
        dirs, reqs, sdirs = ([], [], [])
        saved_dirs = sv.get(tag + '_columns') if ctx.mode != 'run' else None
        for j, item in enumerate(plan_runs):
            if item[0] == 'GENERATE':
                cpath, csha = ctx.write_input('%s_controls_%02d.json' % (tag, j), item[1])
            else:
                cpath, csha = item
            dd = ctx.stage_dir('%s_columns_%02d' % (tag, j))
            outc = dd / 'columns'
            if saved_dirs is not None and len(saved_dirs) == len(plan_runs):
                outc = Path(saved_dirs[j])
            cargv = base + ['--controls', cpath, '--controls-sha256', csha] + extra_args + ['--outdir', outc]
            reqs.append(gen_request('%s_columns_%02d' % (tag, j), key, cargv, module_patches=[reuse_patch], mask=mask))
            sdirs.append(dd)
            dirs.append(outc)
        for k in range(0, len(reqs), max(1, workers)):
            ctx.run_stages(reqs[k:k + workers], sdirs[k:k + workers])
        if ctx.mode != 'run' and saved_dirs is not None and (len(saved_dirs) != len(plan_runs)):
            dirs = [Path(x) for x in saved_dirs]
        return dirs

    def manifest(tag, run_dirs):
        obj = {'runs': [{'directory': str(x), 'finish_sha256': ctx.finish_sha(x)} for x in run_dirs], 'scope': 'c2v001 generated manifest for %s; complete %d columns required by the stage itself' % (tag, n)}
        return ctx.write_input('%s_manifest.json' % tag, obj)

    def generated_runs(tag, bracket_table, v001=False, split=True):
        """Group indices into column runs.  v001 supports only one global bracket per run."""
        runs = []
        if v001:
            groups = {}
            for i in range(n):
                groups.setdefault(tuple(bracket_table[str(i)]), []).append(i)
            for br, ids in sorted(groups.items(), key=lambda kv: kv[1][0]):
                for ch in _chunks(ids, workers) if split else [ids]:
                    sol = dict(template)
                    sol['enthalpy_bracket'] = list(br)
                    runs.append(('GENERATE', {'radial_indices': ch, 'solver': sol, 'selection': '%s c2v001 rule' % tag}))
        else:
            for ch in _chunks(list(range(n)), workers) if split else [list(range(n))]:
                runs.append(('GENERATE', {'radial_indices': ch, 'solver': dict(template), 'column_enthalpy_brackets': {str(i): bracket_table[str(i)] for i in ch}, 'selection': '%s c2v001 rule' % tag}))
        return runs
    rule = brackets.get('rule')
    pinned = brackets.get('pinned_controls')
    checks = {}
    if rule:
        undecided = [k for k in ('rfs_factors', 'le_first_factors', 'le_next_factors') if _has_pending(rule[k])]
        if undecided:
            refuse('brackets.rule_factors', 'UNDECIDED_NGC_FIELD', 'brackets.rule_factors is NONE_IN_REVIEWED_CODE for %s (no ROOT_DECISIONS row) and the call spec supplies none: %s' % (gname, undecided))
    if pinned:
        fs_plan = [(x['path'], verify_pin(x['path'], x['sha256'], 'pinned fs controls')) for x in pinned['fs']]
        merged = {}
        for x in pinned['fs']:
            c = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(x['path'])))
            for i in c['radial_indices']:
                merged[str(i)] = c['solver']['enthalpy_bracket']
            if any((c['solver'][k] != template[k] for k in template if k != 'enthalpy_bracket')):
                checks.setdefault('fs_solver_block_differs', []).append(x['path'])
        ro = g.get('repro_rule_overrides', {}).get('fs_absolute_overrides', {})
        expect = {str(i): list(ro.get(str(i), template['enthalpy_bracket'])) for i in range(n)}
        checks['fs'] = {'checked': True, 'n': len(merged), 'bitwise_equal': merged == expect, 'rule': 'nominal template bracket + repro_rule_overrides.fs_absolute_overrides (last successful run wins)'}
    else:
        table = {str(i): list(rule['fs_absolute_overrides'].get(str(i), template['enthalpy_bracket'])) for i in range(n)}
        fs_plan = generated_runs('fs', table, v001=True)
        checks['fs'] = rule_vs_saved(g, 'fs', table)
    fs_dirs = column_pass('fs', 'columns_v001', [] + uvt_argv('columns_v001'), fs_plan)
    mpath, msha = manifest('fs', fs_dirs)
    d = ctx.stage_dir('fs_rotation')
    fs_rot = d / 'rotation' if ctx.mode == 'run' else ctx.saved_or('fs_rotation', d / 'rotation')
    fs_col_producer = producer_pin('columns_v001', producer(fs_dirs, 'columns_v001', 'config producer_pins.column_worker', 'fs_rotation'), uvt_extra)
    ctx.run_stages([gen_request('fs_rotation', 'rotation_v001', base + ['--column-manifest', mpath, '--column-manifest-sha256', msha, '--mass-relative-tolerance', FA['mass_relative_tolerance'], '--outdir', fs_rot] + uvt_argv('rotation_v001'), module_patches=[reuse_patch], mask=mask, producers={'column_worker': fs_col_producer})], [d])
    d = ctx.stage_dir('fs_feedback')
    fs_fb = d / 'feedback' if ctx.mode == 'run' else ctx.saved_or('fs_feedback', d / 'feedback')
    fs_rot_producer = producer_pin('rotation_v001', producer([fs_rot], 'rotation_v001', 'config producer_pins.rotation_worker', 'fs_feedback'), uvt_extra)
    ctx.run_stages([gen_request('fs_feedback', 'feedback_v002', base + ['--rotation-directory', fs_rot, '--rotation-finish-sha256', ctx.finish_sha(fs_rot), '--wave-batch', FA['wave_batch'], '--position-batch', FA['position_batch'], '--bessel-cache-entries', FA['bessel_cache_entries'], '--outdir', fs_fb], module_patches=[reuse_patch], mask=mask, producers={'rotation_worker': fs_rot_producer})], [d])
    fs_fb_sha = ctx.finish_sha(fs_fb)
    percall['custody.fs_feedback_worker_sha256'] = producer([fs_fb], 'feedback_v002', 'config custody.fs_feedback_worker_sha256', 'rfs_columns')
    H_fs = column_H(fs_dirs)
    rfs_args = ['--feedback-directory', fs_fb, '--feedback-finish-sha256', fs_fb_sha]
    if pinned:
        rfs_plan = [(x['path'], verify_pin(x['path'], x['sha256'], 'pinned rfs controls')) for x in pinned['rfs']]
        checks['rfs'] = bracket_check([x['path'] for x in pinned['rfs']], H_fs, LE_RULE_DEFAULTS['rfs_factors'], g.get('repro_rule_overrides', {}).get('rfs_factor_overrides', {}))
    elif H_fs is None:
        rfs_plan = 'PENDING'
    else:
        require_bracket_source(H_fs, n, 'fs')
        table = rule_brackets(H_fs, rule['rfs_factors'], rule['rfs_factor_overrides'], range(n))
        checks['rfs'] = rule_vs_saved(g, 'rfs', table)
        rfs_plan = generated_runs('rfs', table)
    if rfs_plan == 'PENDING':
        rfs_dirs = ['PENDING(rfs columns)']
        ctx.records.append({'name': 'rfs_columns', 'executed': False, 'note': 'controls depend on fs column enthalpies (rule mode)'})
    else:
        rfs_dirs = column_pass('rfs', 'columns_v003', rfs_args + uvt_argv('columns_v003', fs_rot), rfs_plan)
    field_dir, field_sha = (fs_fb, fs_fb_sha)
    field_rot = fs_rot
    field_worker = producer([fs_fb], 'feedback_v002', '--feedback-worker-sha256', 'le1 field')
    prev_dirs = rfs_dirs
    prev_speeds = None
    final = None
    for p in range(1, P + 1):
        tag = 'le%d' % p
        last = p == P
        serial = last or bound is not None
        H_prev = column_H(prev_dirs) if all((isinstance(x, Path) for x in prev_dirs)) else None
        factors = rule['le_first_factors'] if rule and p == 1 else rule['le_next_factors'] if rule else None
        if pinned:
            plan = [(x['path'], verify_pin(x['path'], x['sha256'], 'pinned le controls')) for x in pinned['le'][p - 1]]
            checks[tag] = bracket_check([x['path'] for x in pinned['le'][p - 1]], H_prev, LE_RULE_DEFAULTS['le_first_factors'] if p == 1 else LE_RULE_DEFAULTS['le_next_factors'], {})
        elif H_prev is None:
            plan = 'PENDING'
        else:
            ov = rule['le_factor_overrides'].get(str(p), {})
            require_bracket_source(H_prev, n, 'rfs' if p == 1 else 'le%d' % (p - 1))
            table = rule_brackets(H_prev, factors, ov, range(n))
            checks[tag] = rule_vs_saved(g, tag, table)
            plan = generated_runs(tag, table, split=not serial)
        if plan == 'PENDING':
            ctx.records.append({'name': tag + '_columns', 'executed': False, 'note': 'controls depend on previous column enthalpies'})
            break
        cols = column_pass(tag, 'columns_v005', ['--feedback-directory', field_dir, '--feedback-finish-sha256', field_sha, '--feedback-worker-sha256', field_worker, '--entropy-scale', efs] + uvt_argv('columns_v005', field_rot), plan)
        mpath, msha = manifest(tag, cols)
        d = ctx.stage_dir(tag + '_rotation')
        rot = d / 'rotation' if ctx.mode == 'run' else ctx.saved_or(tag + '_rotation', d / 'rotation')
        ctx.run_stages([gen_request(tag + '_rotation', 'rotation_v005', base + ['--column-manifest', mpath, '--column-manifest-sha256', msha, '--feedback-directory', field_dir, '--feedback-finish-sha256', field_sha, '--column-worker-sha256', producer(cols, 'columns_v005', '--column-worker-sha256', tag + '_rotation'), '--feedback-worker-sha256', field_worker, '--mass-relative-tolerance', FA['mass_relative_tolerance'], '--outdir', rot, '--entropy-scale', efs] + uvt_argv('rotation_v005', field_rot), module_patches=[reuse_patch], mask=mask)], [d])
        pass_rec = {'pass': p, 'columns': [str(x) for x in cols], 'rotation': str(rot), 'field': str(field_dir)}
        rf = Path(rot) / 'finish.json'
        if rf.is_file():
            rfj = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(rf))
            pass_rec.update(rotation_positive=rfj['positive_rotation_square'], minimum_rotation_square=rfj['minimum_rotation_square'], nonpositive_indices=rfj['nonpositive_indices'], rotation_arrays={'path': rfj['arrays_path'], 'sha256': rfj['arrays_sha256']})
            if ctx.mode == 'run':
                pass_rec['rotation_array_content_digests'] = array_digests(rfj['arrays_path'])
        failures = []
        for x in cols:
            fx = Path(x) / 'finish.json'
            if fx.is_file():
                failures += _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(fx))['failures']
        pass_rec['column_failures'] = failures
        observe = len(cols) == 1 and (last or bound is not None or sp['numerics']['picard']['observe_every_pass'])
        speeds = None
        if observe:
            d = ctx.stage_dir(tag + '_column_mean')
            obsd = d / 'observation' if ctx.mode == 'run' else ctx.saved_or(tag + '_column_mean', d / 'observation')
            b, b_ok, b_st = gc_value(gc, 'observation.binding')
            if 'observation.binding' in gfields:
                b, b_ok = (gfields['observation.binding'], True)
            bpin = [str(b['path']), b['sha256']] if b_ok else ['NONE_IN_REVIEWED_CODE(observation.binding)', 'NONE_IN_REVIEWED_CODE']
            pins = [bpin, [str(Path(rot) / 'start.json'), ctx.finish_sha(rot, 'start.json')], [str(Path(rot) / 'finish.json'), ctx.finish_sha(rot)], [str(Path(cols[0]) / 'start.json'), ctx.finish_sha(cols[0], 'start.json')], [str(Path(cols[0]) / 'finish.json'), ctx.finish_sha(cols[0])]]
            percall['custody.column_mean_input_pins'] = pins
            rot_worker = rotation_producer_pin(producer([rot], 'rotation_v005', 'config producer_pins.rotation_worker', tag + '_column_mean'), uvt_extra)
            ctx.run_stages([gen_request(tag + '_column_mean', 'column_mean_v004', ['--outdir', obsd], tag=tag, producers={'rotation_worker': rot_worker})], [d])
            rp = Path(obsd) / 'result.json'
            if rp.is_file():
                res = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(rp))
                pass_rec['column_mean'] = {'path': str(rp), 'sha256': sha256_file(rp), 'status': res['status']}
                if res['status'] == 'CONDITIONAL_PREPARATION_ROWS_NOT_CALIBRATION':
                    speeds = [r['speed_km_s'] for r in res['prediction']['rows']]
                    pass_rec['rows'] = res['prediction']['rows']
                    if res['prediction'].get('invalid_rows') is not None:
                        pass_rec['invalid_rows'] = res['prediction']['invalid_rows']
                    pass_rec['nonaxisymmetric_residual_maxima'] = res['nonaxisymmetric_residual_maxima']
                    pass_rec['residual_units'] = res.get('residual_units')
                else:
                    pass_rec['column_mean_failure'] = res.get('failure')
        else:
            pass_rec['column_mean'] = 'NOT_OBSERVED (multi-run parallel pass or observe_every_pass false)'
        if speeds is not None and prev_speeds is not None:
            pass_rec['max_abs_change_km_s'] = max((abs(a - b) for a, b in zip(speeds, prev_speeds) if a is not None and b is not None))
        ctx.passes.append(pass_rec)
        ctx.event(event='pass_done', **{k: v for k, v in pass_rec.items() if k in ('pass', 'max_abs_change_km_s', 'rotation_positive')})
        stop = last or (bound is not None and pass_rec.get('max_abs_change_km_s') is not None and (pass_rec['max_abs_change_km_s'] <= bound))
        if stop:
            final = pass_rec
            break
        prev_speeds = speeds
        d = ctx.stage_dir(tag + '_feedback')
        fb = d / 'feedback' if ctx.mode == 'run' else ctx.saved_or(tag + '_feedback', d / 'feedback')
        ctx.run_stages([gen_request(tag + '_feedback', 'feedback_v004', base + ['--rotation-directory', rot, '--rotation-finish-sha256', ctx.finish_sha(rot), '--wave-batch', FA['wave_batch'], '--position-batch', FA['position_batch'], '--bessel-cache-entries', FA['bessel_cache_entries'], '--outdir', fb, '--current-feedback-directory', field_dir, '--current-feedback-finish-sha256', field_sha, '--rotation-worker-sha256', producer([rot], 'rotation_v005', '--rotation-worker-sha256', tag + '_feedback'), '--current-feedback-worker-sha256', field_worker], module_patches=[reuse_patch], mask=mask)], [d])
        field_dir, field_sha = (fb, ctx.finish_sha(fb))
        field_rot = rot
        field_worker = producer([fb], 'feedback_v004', '--feedback-worker-sha256', 'le%d field' % (p + 1))
        prev_dirs = cols
    info['bracket_rule_checks'] = checks
    info['producer_identity'] = producer_log
    info['galaxy_config']['stage_configs'] = [m for _, _, m in gc_written.values()]
    info['refusals'] = refusals
    info['percall_known'] = {k: v for k, v in percall.items()}
    if uvx is not None:
        info['uv_tail'] = uvx
    return (info, final)

def _cx3r007_strict__cmd_run_ngc_cx3v005_L6014(spec_path, outdir):
    out = Path(os.path.abspath(outdir))
    if out.exists():
        print('REFUSED: outdir exists', file=sys.stderr)
        return 2
    out.mkdir(parents=True)
    t0 = time.monotonic()
    raw = _ngc_record_bytes_cx3r007(Path(spec_path))
    spec_sha = sha256_bytes(raw)
    (out / 'inputs').mkdir()
    with open(out / 'inputs' / 'call_spec.json', 'xb') as f:
        f.write(raw)
    result = {'schema': RESULT_SCHEMA, 'call_spec_sha256': spec_sha, 'driver_sha256': sha256_file(__file__), 'accepted_for_calibration': False, 'scored': False, 'valid': False, 'reasons': []}
    status = 'FAILED'
    ctx = None
    try:
        nspec = normalize_spec(_ngc_json_loads_cx3r007(raw))
        if nspec.get('config') == 'NGC3198_C2V002':
            ngc_run_blocked(out, nspec, spec_sha, result)
        pins = all_static_pins(nspec)
        g = GALAXIES[nspec['galaxy']]
        _write_x(out / 'start.json', {'schema': RESULT_SCHEMA, 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'pid': os.getpid(), 'driver': str(Path(__file__).resolve()), 'driver_sha256': result['driver_sha256'], 'call_spec_sha256': spec_sha, 'normalized_spec': nspec, 'static_pins': pins, 'scope': 'Route-B m0 forward call; no observed velocity read, no score, no calibration admission.'})
        _nodes = uvt_is_nodes(nspec['numerics'].get('uv_tail'))
        bb = binding_blockers() + (ro1_off_blockers() if route_a_ro1_workers(nspec) else []) if 'uv_tail' not in nspec['numerics'] else binding_blockers(dict(SCRIPTS, **uvt_active(_nodes)['scripts'])) + uvt_binding_blockers(_nodes)
        if bb:
            result['binding_blockers'] = bb
            raise Blocked(' | '.join(bb))
        sr = route_b_static_refusals(nspec, load_galaxy_config(nspec['galaxy'], nspec.get('member')))
        if sr:
            result['remaining_refusals'] = sr
            raise Blocked('REMAINING_REFUSALS: ' + ' | '.join(('%s [%s] %s' % (r['where'], r['class'], r['refusal']) for r in sr)))
        ctx = Ctx('run', nspec, out)
        ctx.log = open(out / 'progress.jsonl', 'x')
        info, final = execute_chain(ctx)
        result.update(galaxy=nspec['galaxy'], normalized_spec=nspec, identity=info, passes=ctx.passes)
        if final is None:
            result['reasons'].append('no final pass')
        else:
            result['final_pass'] = final['pass']
            bnd = nspec['numerics']['picard']['speed_change_bound_km_s']
            chg = final.get('max_abs_change_km_s')
            result['picard_bound_met'] = None if bnd is None or chg is None else bool(chg <= bnd)
            rows_ok, invalid_rows = final_rows_check(final, g['n_queries'], nspec)
            if rows_ok:
                if nspec.get('coefficient_alternative') == 'STAGE0_GRID_OUTER':
                    reg = _pinned_json(STAGE0_SLOTS_PIN[0], STAGE0_SLOTS_PIN[1], 'STAGE0 alternative registration')
                    alt = next((a for a in reg['alternatives']['declared'] if a['name'] == 'STAGE0_GRID_OUTER'))
                    result['alternative_label'] = {'name': 'STAGE0_GRID_OUTER', 'status': 'DECLARED_ALTERNATIVE_NOT_HEADLINE', 'scoring_scope': alt['scoring_scope']}
                result['rows'] = final['rows']
                result['speeds_km_s'] = {r['id']: r['speed_km_s'] for r in final['rows']}
                if invalid_rows is not None:
                    result['invalid_rows'] = invalid_rows
                    result['headline_rule'] = 'N1/A4: rows valid=false (QUERY_INSIDE_INNERMOST_NODE, QUERY_BEYOND_OUTER_GAS_CUT, QUERY_OUTSIDE_RETAINED_SUPPORT) count as misses; invalid entries never pass; they do not invalidate the call'
                if nspec.get('member') is not None or nspec['physical'].get('entropy_K_member', 'N4_PRIMARY_64_OVER_121') != 'N4_PRIMARY_64_OVER_121':
                    result['alternative_label'] = {'member': nspec.get('member'), 'entropy_K_member': nspec['physical'].get('entropy_K_member'), 'status': 'DECLARED_ALTERNATIVE_NOT_HEADLINE'}
                result['valid'] = not final['column_failures'] and final.get('rotation_positive') is True
                if not result['valid']:
                    result['reasons'].append('final pass column failures or nonpositive rotation')
            else:
                result['reasons'].append('final column mean did not return %d rows: %s' % (g['n_queries'], final.get('column_mean')))
            diag = {'nonaxisymmetric_residual_maxima': final.get('nonaxisymmetric_residual_maxima'), 'residual_units': final.get('residual_units'), 'stored_residual_arrays': {'rotation_arrays': final.get('rotation_arrays'), 'keys': ['angular_radial_residual', 'angular_vertical_residual', 'angular_azimuthal_residual', 'Phi_R_full', 'Phi_z_full', 'base_residual_r0']}, 'per_pass_maxima': [{'pass': x['pass'], 'maxima': x.get('nonaxisymmetric_residual_maxima')} for x in ctx.passes]}
            if final.get('rotation_arrays'):
                try:
                    diag['azimuthal_harmonics'] = harmonic_diagnostic(final['rotation_arrays']['path'])
                except Refusal:
                    raise
                except Exception as exc:
                    diag['azimuthal_harmonics'] = 'unavailable: %s' % exc
            result['residual_diagnostics'] = diag
        status = 'COMPLETED' if result['valid'] else 'COMPLETED_INVALID'
    except Refusal as exc:
        status = 'REFUSED'
        result['reasons'].append(str(exc))
    except Blocked as exc:
        status = 'BLOCKED'
        result['reasons'].append(str(exc))
    except RouteANoFixedPoint as exc:
        status = 'ROUTE_A_NO_FIXED_POINT'
        result['reasons'].append(str(exc))
    except StageFailed as exc:
        status = 'FAILED_AT_STAGE'
        result['reasons'].append(str(exc))
    except Exception as exc:
        import traceback
        status = 'FAILED'
        result['reasons'].append('%s: %s' % (type(exc).__name__, exc))
        result['traceback'] = traceback.format_exc()
    try:
        if ctx is not None:
            if ctx.route_a_outcome is not None:
                result['route_a_outcome'] = ctx.route_a_outcome
            if ctx.geometry is not None:
                result['geometry'] = ctx.geometry
            result['stage_records'] = ctx.records
            if ctx.uv_tail is not None:
                result['uv_tail'] = dict(ctx.uv_tail, stage_records=uvt_stage_records(ctx.records))
            if ctx.spec.get('reference_compare'):
                result['reference_comparison'] = reference_comparison(ctx.records, GALAXIES[ctx.spec['galaxy']].get('saved_runs', {}))
                result['deciding_test'] = deciding_test_verdict(result['reference_comparison'], ctx.passes)
            if result.get('passes') is None:
                result['passes'] = ctx.passes
            if ctx.log is not None:
                ctx.log.close()
    except Refusal as exc:
        status = 'REFUSED'
        result['valid'] = False
        result['reasons'].append(str(exc))
        if ctx.log is not None:
            ctx.log.close()
    result['status'] = status
    result['elapsed_seconds'] = time.monotonic() - t0
    rsha = _write_x(out / 'result.json', result)
    _write_x(out / 'finish.json', {'status': status, 'valid': result['valid'], 'result_path': str(out / 'result.json'), 'result_sha256': rsha, 'elapsed_seconds': result['elapsed_seconds'], 'reasons': result['reasons'], 'retries': 0, 'partial_outputs_preserved': True})
    return 0 if status in ('COMPLETED', 'COMPLETED_INVALID') else 3

def _cx3r007_strict__ngc_ro1_record_load_cx3r006_L6209(path, label):
    try:
        tree = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(path)), object_pairs_hook=_NGCObjectPairsCX3R006)
    except Refusal:
        raise
    except (OSError, ValueError, TypeError) as exc:
        raise Refusal('NGC_RO1_RECORD_UNREADABLE: %s file=%s (%s)' % (label, json.dumps(str(path)), type(exc).__name__)) from exc

    def unpack(value, at):
        if isinstance(value, _NGCObjectPairsCX3R006):
            result, seen = ({}, {})
            for index, (key, child) in enumerate(value):
                here = at + '[' + json.dumps(key, ensure_ascii=True) + ']@member[' + str(index) + ']'
                if key in seen:
                    raise Refusal('NGC_JSON_DUPLICATE_KEY: %s file=%s first_path=%s second_path=%s' % (label, json.dumps(str(path)), seen[key], here))
                seen[key] = here
                result[key] = unpack(child, here)
            return result
        if isinstance(value, list):
            return [unpack(child, at + '[' + str(index) + ']') for index, child in enumerate(value)]
        return value
    result = unpack(tree, '$')
    if not isinstance(result, dict):
        raise Refusal('NGC_RO1_RECORD_OBJECT_REQUIRED: %s file=%s path=$' % (label, json.dumps(str(path))))
    return result

def _cx3r007_strict__ngc_read_route_a_result_strict_cx3r006_L6280(result_path, finish_path, manifest_path=None):
    """Read a (future) NGC43 route-A result: 43 speeds keyed NGC3198-Q01..Q43 in manifest order,
    validity, and DIAGNOSTIC m>=1 content of the azimuth-resolved trial (no acceptance threshold).
    Reads only the worker's own outputs and the target-free manifest."""
    import numpy as np
    manifest_path = manifest_path or NGC_DATA['manifest'][0]
    man = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(manifest_path)))
    _ngc_validate_manifest_rows_cx3r007(man, manifest_path)
    ids = [r['query_id'] for r in man['rows']]
    rad = {r['query_id']: r['Rad_text'] for r in man['rows']}
    reasons = []
    fin = _ngc_json_loads_cx3r007(_ngc_record_text_cx3r007(Path(finish_path)))
    if fin.get('status') != 'RETURNED_ACTUAL_RESULT':
        reasons.append('worker status %s' % fin.get('status'))
    if sha256_file(result_path) != fin.get('result_sha256'):
        reasons.append('result sha256 differs from worker finish.json')
    ra = _ngc_ro1_record_load_cx3r006(result_path, 'route-A result')
    x = _ngc_ro1_prediction_cx3r006(ra, result_path)
    sfp = x.get('source_fixed_point') if isinstance(x.get('source_fixed_point'), dict) else {}
    ro1, ro1_fired = ro1_outcome(ra, x, result_path, sfp.get('converged_finite_fixed_point') is True and (sfp.get('checkpoint') or {}).get('outcome') == ROUTE_A_CONVERGED)
    if ro1_fired:
        reasons.append('RO1: route-A circular-trial readout refused after a converged fixed point (%s); no route-A rows' % ro1['events'][0].get('refusal'))
        return {'rows': None, 'speeds_km_s': None, 'valid': False, 'reasons': reasons, 'ro1': ro1, 'validity_definition': 'worker RETURNED_ACTUAL_RESULT, result sha matches, 43 manifest ids in order, finite speeds, converged source fixed point, predictions_available', 'm_ge_1_diagnostics': None, 'dynamics_status': x.get('dynamics_status'), 'accepted_for_calibration': False, 'route': 'ROUTE_A_ONLY (route B blocked)'}
    if not isinstance(x.get('rows'), list):
        raise Refusal('NGC_ROUTE_A_ROWS_REQUIRED: file=%s path=$["result"]["result"]["rows"]; RO1 did not fire' % json.dumps(str(result_path)))
    rows = x['rows']
    if [r['id'] for r in rows] != ids:
        reasons.append('row ids are not the 43 manifest ids in order')
    speeds = [r['speed_km_s'] for r in rows]
    if not all((isinstance(v, (int, float)) and math.isfinite(v) for v in speeds)):
        reasons.append('nonfinite speed')
    if x.get('source_fixed_point', {}).get('converged_finite_fixed_point') is not True:
        reasons.append('route-A source fixed point not converged')
    if x.get('predictions_available') is not True:
        reasons.append('predictions_available is not True')
    per_q, gmax = ([], {})
    for q in x.get('query_physics', []):
        nodes = q['nodes']
        n = len(nodes)
        phi = np.array([nd['phi_rad'] for nd in nodes])
        v = np.array([nd['v'] for nd in nodes], dtype=float)
        equal = bool(np.allclose(phi, 2 * np.pi * np.arange(n) / n, rtol=0, atol=1e-12))
        F = np.abs(np.fft.rfft(v))
        ratios = {'m%d' % m: float(F[m] / F[0]) if F[0] > 0 else None for m in range(1, len(F))}
        for k, val in ratios.items():
            if val is not None:
                gmax[k] = max(gmax.get(k, 0.0), val)
        eul = np.array([nd['Euler_covector_residual_R_phi_z'] for nd in nodes], dtype=float)
        cont = [abs(r) for nd in nodes for r in nd['mass_continuity']['fractional_density_rate_per_s']]
        per_q.append({'id': q['id'], 'n_azimuths': n, 'equal_angle_nodes': equal, 'speed_m_s_azimuth_harmonic_ratio': ratios, 'speed_m_s_azimuth_range': float(v.max() - v.min()), 'Euler_residual_abs_max_R_phi_z': [float(a) for a in np.max(np.abs(eul), axis=0)], 'continuity_fractional_rate_abs_max_per_s': float(max(cont)) if cont else None})
    valid = not reasons and len(rows) == 43
    return {'rows': [{'id': r['id'], 'Rad_text_kpc': rad.get(r['id']), 'speed_km_s': r['speed_km_s']} for r in rows], 'speeds_km_s': {r['id']: r['speed_km_s'] for r in rows}, 'valid': valid, 'reasons': reasons, 'validity_definition': 'worker RETURNED_ACTUAL_RESULT, result sha matches, 43 manifest ids in order, finite speeds, converged source fixed point, predictions_available', 'm_ge_1_diagnostics': {'quantity': '|FFT_m(v)|/|FFT_0(v)| of the circular trial speed over the observation azimuths; max |Euler residual| (R,phi,z) and |continuity rate| per query', 'global_max_harmonic_ratio': gmax, 'per_query': per_q, 'status': 'DIAGNOSTIC_ONLY'}, 'dynamics_status': x.get('dynamics_status'), 'accepted_for_calibration': False, 'route': 'ROUTE_A_ONLY (route B blocked)'}

_CX3R007_STRICT_BY_LINE = {577: '_cx3r007_strict_exec_verified_L577', 791: '_cx3r007_strict_stage_main_L791', 894: '_cx3r007_strict_normalize_uv_tail_L894', 918: '_cx3r007_strict_uvt_info_L918', 978: '_cx3r007_strict_ro1_off_blockers_L978', 1141: '_cx3r007_strict_uvt_admitted_record_check_L1141', 1155: '_cx3r007_strict_uvt_stage_records_L1155', 1176: '_cx3r007_strict_uvt_binding_blockers_L1176', 1430: '_cx3r007_strict_per_call_seed_L1430', 1486: '_cx3r007_strict__pinned_json_L1486', 1627: '_cx3r007_strict_geometry_inputs_L1627', 1652: '_cx3r007_strict_geometry_config_fields_L1652', 1873: '_cx3r007_strict__read_checkpoint_identity_L1873', 1925: '_cx3r007_strict_ro1_outcome_L1925', 1978: '_cx3r007_strict_route_a_attempt_link_L1978', 2000: '_cx3r007_strict_route_a_custody_L2000', 2067: '_cx3r007_strict_column_H_L2067', 2101: '_cx3r007_strict_merged_brackets_L2101', 2129: '_cx3r007_strict_bracket_check_L2129', 2252: '_cx3r007_strict_load_galaxy_config_L2252', 2306: '_cx3r007_strict_ddo_driver_literal_check_L2306', 2332: '_cx3r007_strict_ngc_driver_value_check_L2332', 2403: '_cx3r007_strict_route_a_reported_iteration_L2403', 2460: '_cx3r007_strict_binding_blockers_L2460', 2597: '_cx3r007_strict_execute_chain_L2597', 3289: '_cx3r007_strict_reference_comparison_L3289', 3420: '_cx3r007_strict_transitive_pins_and_scipy_L3420', 3477: '_cx3r007_strict_cmd_run_L3477', 3619: '_cx3r007_strict__compare_argv_L3619', 3661: '_cx3r007_strict__orig_launch_L3661', 3682: '_cx3r007_strict_cmd_dry_run_L3682', 4167: '_cx3r007_strict_n1_query_rows_L4167', 4384: '_cx3r007_strict__base_seed_grid_L4384', 4485: '_cx3r007_strict_ngc_seed_L4485', 4535: '_cx3r007_strict_ngc_static_pins_L4535', 4578: '_cx3r007_strict_ngc_sources_summary_L4578', 4613: '_cx3r007_strict_ngc_prep_local_modules_L4613', 4631: '_cx3r007_strict_ngc_caller_contract_check_L4631', 4675: '_cx3r007_strict_ngc_route_b_table_L4675', 4768: '_cx3r007_strict_ngc_remaining_refusals_L4768', 4788: '_cx3r007_strict_ngc_read_route_a_result_L4788', 5087: '_cx3r007_strict__ngc_v011_seed_L5087', 5144: '_cx3r007_strict_cmd_dry_run_L5144', 5183: '_cx3r007_strict_uvt_binding_blockers_L5183', 5315: '_cx3r007_strict__execute_ngc_v011_chain_L5315', 6014: '_cx3r007_strict__cmd_run_ngc_cx3v005_L6014', 6209: '_cx3r007_strict__ngc_ro1_record_load_cx3r006_L6209', 6280: '_cx3r007_strict__ngc_read_route_a_result_strict_cx3r006_L6280'}
_CX3R007_WRAPPED_OBJECTS = {}
for _cx3_name, _cx3_value in list(globals().items()):
    _cx3_code = getattr(_cx3_value, '__code__', None)
    if _cx3_code is not None and _cx3_code.co_filename == __file__ and _cx3_code.co_firstlineno in _CX3R007_STRICT_BY_LINE:
        _cx3_key = id(_cx3_value)
        if _cx3_key not in _CX3R007_WRAPPED_OBJECTS:
            _CX3R007_WRAPPED_OBJECTS[_cx3_key] = _ngc_scoped_callable_cx3r007(_cx3_value, globals()[_CX3R007_STRICT_BY_LINE[_cx3_code.co_firstlineno]])
        globals()[_cx3_name] = _CX3R007_WRAPPED_OBJECTS[_cx3_key]


def _ngc_v011_dispatch(fn, spec_path, *args):
    _cx3r007_spec_snapshot = Path(spec_path).read_bytes()
    raw = json.loads(_cx3r007_spec_snapshot)
    if not isinstance(raw, dict):
        raise Refusal('SPEC_OBJECT_REQUIRED')
    if not isinstance(raw.get('numerics', {}), dict):
        raise Refusal('NUMERICS_OBJECT_REQUIRED')
    if raw.get('galaxy') == 'NGC3198' and 'uv_tail' in raw.get('numerics', {}):
        with _ngc_selected_record_scope_cx3r007(spec_path, _cx3r007_spec_snapshot):
            with _ngc_v011_stage0_context(_ngc_v011_stage0_flag(raw)):
                with _ngc_v011_context():
                    return fn(spec_path, *args)
    return fn(spec_path, *args)

def cmd_run(spec_path, outdir):
    _cx3r007_spec_snapshot = Path(spec_path).read_bytes()
    raw = json.loads(_cx3r007_spec_snapshot)
    if not isinstance(raw, dict):
        raise Refusal('SPEC_OBJECT_REQUIRED')
    if raw.get('galaxy') == 'NGC3198' and isinstance(raw.get('numerics'), dict) and ('uv_tail' in raw['numerics']):
        with _ngc_selected_record_scope_cx3r007(spec_path, _cx3r007_spec_snapshot):
            return _ngc_v011_dispatch(_cmd_run_ngc_cx3v005, spec_path, outdir)
    return _V010_RUN(spec_path, outdir)
# END DISPATCH0581 CX3R007 SCOPED RECORD SUCCESSOR

if __name__ == '__main__':
    sys.exit(main())
