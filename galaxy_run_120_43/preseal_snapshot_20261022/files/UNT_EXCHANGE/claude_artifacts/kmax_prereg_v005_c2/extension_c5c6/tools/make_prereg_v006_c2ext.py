"""Build the DRAFT prereg V006 (post-extension rule for V005 decision rule 3) from bytes, then pin its sha into the compare
script prereg_v006/kmax_compare_ext_c2v006.py (in place; only its PREREG_SHA256 line changes).
Every sha in the prereg is computed here from the file bytes.  Writes prereg_v006/KMAX_MATRIX_PREREG_V006.json
(refuses to overwrite a different existing file unless --replace-draft is given; a DRAFT is not sealed).
usage: python3 -I -B make_prereg_v006_c2ext.py [--replace-draft]"""
import hashlib
import json
import re
import sys
from pathlib import Path

EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
K5 = EX / 'kmax_prereg_v005_c2'
HERE = K5 / 'extension_c5c6'
CL2 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
RUNS = CL2 / 'runs'
EXT1 = Path('/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def pin(p):
    return {'path': str(p), 'sha256': sha(p)}


def main():
    pre5p = K5 / 'KMAX_MATRIX_PREREG_V005.json'
    pre5 = json.loads(pre5p.read_text())
    if sha(pre5p) != 'dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174':
        raise SystemExit('V005 pin')
    cmpp = K5 / 'verdict_r3/COMPARE_R3_V001/KMAX_COMPARISON.json'
    if sha(cmpp) != '4ea21d902cfb4e8cd3b5aa61d29b8c3bbc05cab9a56c49f3af2913c32ae66433':
        raise SystemExit('R3 verdict pin')
    r3c = json.loads(cmpp.read_text())
    cube = r3c['sequences']['cube']
    inner = r3c['inner_control']
    drv9 = HERE / 'driver_v009/galaxy_m0_forward_c2v009.py'
    prep9 = HERE / 'prep_successor/ddo_actual_initial_source_preparation_v009.py'
    specs = json.loads((HERE / 'specs/SPECS_EXT_M16.json').read_text())
    smoke = {c: HERE / ('analysis/prep_smoke/%s/PREP_V009_SMOKE.json' % c) for c in ('C5', 'C6')}
    repro = {c: HERE / ('analysis/prep_repro/%s/PREP_V009_REPRO.json' % c) for c in ('C2', 'C3', 'C4')}
    for p in list(smoke.values()) + list(repro.values()):
        if not p.is_file():
            raise SystemExit('missing evidence %s' % p)
    g = {gid: pre5['grids'][gid] for gid in ('G2', 'G3', 'G4', 'GR')}
    for case, gid in (('C5', 'G5'), ('C6', 'G6')):
        s = json.loads(Path(specs['specs'][case + '_N8']['path']).read_text())
        g[gid] = {'axis_nodes': s['numerics']['composite_grid_spec']['total_axis_nodes'],
                  'composite_grid_spec': s['numerics']['composite_grid_spec'],
                  'role': '%s plus one more unit outer panel [%d,%d] per side, order 6 (V005 decision rule 3: order-6 unit outer panels)'
                          % ('G4' if gid == 'G5' else 'G5', int(s['numerics']['composite_grid_spec']['breaks_inverse_kpc'][-1]) - 1,
                             int(s['numerics']['composite_grid_spec']['breaks_inverse_kpc'][-1]))}
    ext_out = {c: str(EXT1 / ('KMAX_A2F10_%sR3_RUN_V001' % c)) for c in ('C5', 'C6')}
    R3RUN = {c: RUNS / ('KMAX_A2F10_%s_D7R3_RUN_V001' % c) for c in ('C2R3', 'C3R3', 'C4R3', 'RR3')}
    bound = {}
    for cid, run in (('C4', 'C4R3'), ('C3', 'C3R3'), ('C2', 'C2R3'), ('R', 'RR3')):
        r = R3RUN[run]
        bound[cid] = {'outdir': str(r), 'result': pin(r / 'result.json'), 'finish': pin(r / 'finish.json'),
                      'r3_verdict_input_sha256': r3c['inputs'][cid]['result_sha256']}
        if bound[cid]['result']['sha256'] != bound[cid]['r3_verdict_input_sha256']:
            raise SystemExit('R3 result changed: %s' % cid)
    pre = {
        'schema': 'KMAX_MATRIX_PREREG_V006',
        'status': ('DRAFT_FOR_REVIEW (not sealed).  Written 2026-10-17 after the V005 verdict COMPARE_R3_V001 (NOT_CONVERGED, '
                   'extend_shape cube) was registered and before any C5/C6 call exists (no outdir KMAX_A2F10_C5R3_RUN_V001 / '
                   'KMAX_A2F10_C6R3_RUN_V001 under runs or runs_ext).  The seal (SEAL_RECORD_V006: this file sha + the compare script sha) '
                   'is a separate act after review and before any C5/C6 launch.  Thresholds, statistics and gates are V005\'s unchanged.'),
        'plan_item': 'P-88 (A1-numerics) k_max extension of the cube at the A2 factor-10 anchor: K = 5 and 6 /kpc',
        'extends': {'prereg_v005': pin(pre5p), 'v005_decision_rule_3': pre5['criterion']['decision_rule'][2],
                    'why_v006': ('V005 decision rule 3 names the extension and its resources but no rule that decides after it; a rule '
                                 'chosen after C5/C6 exist would be post hoc.  V006 registers it now with V005\'s statistics.'),
                    'r3_verdict': {'comparison': pin(cmpp), 'stdout': pin(K5 / 'verdict_r3/COMPARE_R3_V001.stdout.txt'),
                                   'table': pin(K5 / 'verdict_r3/COMPARE_R3_V001/KMAX_COMPARISON_TABLE.txt'),
                                   'decision': r3c['decision']}},
        'carried_from_r3': {
            'extend_shape': r3c['decision']['extend_shape'],
            'cube_Dhat_2_3': cube['Dhat_2_3'], 'cube_Dhat_3_4': cube['Dhat_3_4'],
            'sphere_Dhat_3_4': r3c['sequences']['sphere']['Dhat_3_4'], 'cylinder_Dhat_3_4': r3c['sequences']['cylinder']['Dhat_3_4'],
            'inner_control': {'pass': inner['pass_'], 'Dhat_R': inner['Dhat_R'], 'D_R_km_s': inner['D_R'], 'delta': inner['delta'],
                              'cases': inner['cases'], 'scope': 'measured at G2 vs GR (inner panels order 8) in R3; carried, not re-measured at G5/G6'}},
        'unchanged_from_v005': ('row_ids, quoted_sigma_km_s, tau_km_s (tau_i = 0.25 sigma_i), tau_picard 0.0125 km/s, anchor (physical, '
                                'coefficients 2e3a36d8, picard passes 6 / bound 0.01 / observe every pass), statistic Dhat, the contraction '
                                'test q <= 1/2, the per-row tail diagnostic (reported, never adopted), gates V1-V5, the D7 widening rule W1 '
                                'and its later_invocations; all read from the pinned V005 file by the compare script'),
        'binding_inputs': {
            'prereg_v005': pin(pre5p),
            'v005_compare': pin(K5 / 'kmax_compare_c2v005.py'),
            'r3_recovery': pin(K5 / 'd7_recovery_r3/KMAX_D7_RECOVERY_R3.json'),
            'drivers': {'v001': pre5['binding_inputs']['drivers']['v001'], 'v005': pre5['binding_inputs']['drivers']['v005'],
                        'v008': pin(EX / 'driver_v008_c2/galaxy_m0_forward_c2v008.py'), 'v009': pin(drv9)},
            'prep_v009': pin(prep9),
            'v009_admissibility': {
                'driver_sha256': sha(drv9), 'prep_sha256': sha(prep9),
                'review': {'path': str(HERE / 'check/REVIEW_V009_PREP_V009_V001.json'), 'accepted_verdicts': ['PASS', 'PASS_SCOPED'],
                           'required_fields': 'verdict, driver_sha256, prep_sha256 (the separate review writes this file)'},
                'evidence': ([{'name': 'prep_repro_' + c, 'required_verdict': 'PASS_BITWISE', **pin(p)} for c, p in repro.items()]
                             + [{'name': 'prep_smoke_' + c, 'required_verdict': 'PASS', **pin(p)} for c, p in smoke.items()]),
                'condition': ('A case whose driver_sha256 is v009 is admissible (gate V3 driver term) only if, at comparison time, the '
                              'review record exists with an accepted verdict and pins exactly this driver and prep sha, and every '
                              'evidence file has its pinned sha and required verdict.  Otherwise V3 fails with V009_INADMISSIBLE:<reason>.'),
                'inadmissible_next_step': ('V009_INADMISSIBLE: complete the separate review of prep v009 + driver v009 (record at the '
                                           'named path); the comparison is then rerun on the same results (no case rerun is implied).')},
            'driver_equivalence_evidence': {
                'v008_deciding_i': {'result': pin(RUNS / 'DDO154_ROUTE_B_C2V008_DECIDING_ADMIT_PREFIX_RUN_V001/result.json'), 'verdict': 'PASS_BITWISE_EQUAL'},
                'v008_deciding_ii_N8': {'compare': pin(RUNS / 'DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008_DECIDING_RUN_V001.COMPARE_DECIDING_II_C2V008.json'),
                                        'verdict': 'PASS_BITWISE_EQUAL (route-A blobs/records/identity, route-B rows and speeds vs A2_ANCHOR_F10_RUN_V001 under v001)'},
                'v008_vs_v009_dry_byte_identity': pin(HERE / 'dryrun_b2/BYTE_IDENTITY_V008_V009_B2_V001.json'),
                'what_it_shows': ('TESTED-POSITIVE: v008 = v001/v005 chain bitwise at G2 (deciding i, ii incl. N=8 parallel route A); '
                                  'v009 = v008 byte-identical dry-run plans/inputs on 8 registered <=96-node specs (G2, G3, G4, GR; serial '
                                  'and N=8; compute and admitted); prep v009 reproduces the saved route-A IDENTITY inputs and iteration-0 '
                                  'START blobs of the C2, C3, C4 prefixes bitwise.  UNTESTED: v009 (gal_c2v004 stages) vs v005 (gal_c2v003 '
                                  'stages) run-mode equality at G4; deciding test S5 below.')}},
        'grids': g,
        'cases': [
            {'id': 'C4', 'role': 'extension K=4 member (decision)', 'grid': 'G4', 'drivers_allowed': ['v005'], 'prefix': 'bound', 'bound': bound['C4'],
             'note': 'the R3 cube C4R3 (admits KMAX_A2F10_C4_V005_RUN_V001 under v005); under a later D7 R(n) it is rerun as C4R(n) under v005 admitting the same prefix (V005 admission_constraint: same driver as the prefix)'},
            {'id': 'C5', 'role': 'extension K=5 (decision)', 'grid': 'G5', 'drivers_allowed': ['v009'], 'prefix': 'compute',
             'route_a_numerics': {'max_iterations': 16, 'column_workers_allowed': [1, 8]},
             'specs': {'primary_N8': specs['specs']['C5_N8'], 'alternate_N1': specs['specs']['C5_N1']}, 'outdir': ext_out['C5']},
            {'id': 'C6', 'role': 'extension K=6 (decision)', 'grid': 'G6', 'drivers_allowed': ['v009'], 'prefix': 'compute',
             'route_a_numerics': {'max_iterations': 16, 'column_workers_allowed': [1, 8]},
             'specs': {'primary_N8': specs['specs']['C6_N8'], 'alternate_N1': specs['specs']['C6_N1']}, 'outdir': ext_out['C6']},
            {'id': 'C3', 'role': 'diagnostic only (Dhat_3_4 consistency with R3)', 'grid': 'G3', 'drivers_allowed': ['v005'], 'prefix': 'bound', 'bound': bound['C3']},
            {'id': 'C2', 'role': 'diagnostic only (K-sequence table)', 'grid': 'G2', 'drivers_allowed': ['v001'], 'prefix': 'bound', 'bound': bound['C2']},
            {'id': 'R', 'role': 'diagnostic only (inner control carried from R3)', 'grid': 'GR', 'drivers_allowed': ['v005'], 'prefix': 'bound', 'bound': bound['R']}],
        'route_a_expected_inputs': {c: pin(p) for c, p in smoke.items()},
        'fixed_across_extension_cases': {
            'brackets': 'the R3 block 7946b857 (identical to C3R3/C4R3), or as a whole a later cumulative D7 block R(n)',
            'physical_coefficients_picard': 'V005 anchor (unchanged)',
            'route_a_max_iterations': ('16 for C5 and C6 (seed numerical_inputs.max_iterations; base seed 8).  The solvers use it only '
                                       'as the loop bound, so a route A converging at iteration n < 8 computes the same arrays with 8 or 16. '
                                       'Reason: measured prefixes converged at iterations 4/5/6 (K=2/3/4) with the late contraction ratio '
                                       'rising (G4: 0.45 -> 0.66; signed step projection mu 0.45 -> 0.57, cos 0.95: a monotone slow mode, '
                                       'analysis/ROUTE_A_MODE_V001.json); projections for K=6 range from iteration 5 to beyond 12 '
                                       '(analysis/ESTIMATES_V001.json, ROUTE_A_PROJECTION2_V001.json), so the base budget 8 may be exhausted.'),
            'route_a_column_workers': '8 (primary) or 1 (alternate): bitwise-equal by the parallel route-A design, TESTED-POSITIVE at G2 (deciding ii)'},
        'criterion': {
            'statistic': 'Dhat_cube(K1,K2) = max over the 12 rows of |v_i(C_K2) - v_i(C_K1)| / tau_i (V005 statistic, tau_i from V005)',
            'gates': ('V1-V5 exactly as V005 per_case_validity_gates (V3 against the registered block: V005 anchor physical/coefficients/'
                      'picard, the recovery block for every extension case, the registered grid, cube truncation, the case drivers_allowed '
                      'with the v009 admissibility condition, and for C5/C6 numerics.route_a.max_iterations 16 and column_workers in {1, 8}); '
                      'V6 not applicable (no admitted extension case); V7 (C5, C6): the route-A checkpoint IDENTITY.inputs_sha256 entries '
                      'and the iteration_0000/START digests equal route_a_expected_inputs (prep v009 operator evaluation of the registered '
                      'per-call seed).'),
            'decision_rule': [
                'X1. Any of C4, C5, C6 invalid or missing -> INCOMPLETE (name each case and failed gate with its gate_next_steps entry; no threshold or rule change).',
                'X2. The carried R3 inner control (Dhat_R = %.4g, PASS) is not re-decided; if it were not PASS the outcome would be INNER_UNRESOLVED with V005 rule 2 next step.' % inner['Dhat_R'],
                'X3. Dhat_cube(5,6) <= 1 AND Dhat_cube(5,6) <= 0.5 * Dhat_cube(4,5) -> ADOPT cube at k_max = 6 /kpc on grid G6 (driver v009); carried numerical uncertainty per row u_i = |v_i(C6) - v_i(C5)| + |v_i(R) - v_i(C2)| km/s (R3 inner delta), reported with u_i/tau_i and u_i/sigma_i; the V005 shape-spread term is UNTESTED (reported null, not zero).',
                'X4. Otherwise NOT_CONVERGED_EXT with subtype (a) CONTRACTING_ABOVE_TAU if Dhat(5,6) <= 0.5 Dhat(4,5) (so Dhat(5,6) > 1); (c) FLOOR_LIKE if not contracting and Dhat(4,5) <= 1 and Dhat(5,6) <= 1; (b) NOT_CONTRACTING otherwise; each with its pre-named next step below.  Diagnostics always reported: Dhat(3,4) from C3/C4 (must equal the registered %.10g), the K = 2..6 cube rows, per-row q and tail (never adopted), m4 row window of C4-C6, route-A accepted iteration of C5/C6.' % cube['Dhat_3_4']],
            'shape_spread_untested': ('S-shape: only the cube is extended (V005 rule 3).  Deciding test: sphere and cylinder at K = 5, 6 on G5/G6 '
                                      'admitting the C5/C6 prefixes under v009, the V005 shape-agreement test (2 tau_i) at K = 6.'),
            'adopt_next_step': ('Run calibration calls with the cube at K = 6 on G6 (120/axis, driver v009, prep v009); carry u_i; before '
                                'prediction: S-shape (above) and V005 S1 (rerun the adopted grid at K = 5, 6 at the calibrated point).'),
            'next_step_contracting': ('CONTRACTING_ABOVE_TAU: extend the cube to 7 and 8 /kpc with order-6 unit outer panels (132/144 nodes '
                                      'per axis); needs a prep successor with node budget >= 144 and per-call caps from the measured C6 '
                                      'peaks x (144/120)^3 = 1.728, under separate review.  The V005-style geometric tail diagnostic is reported, not adopted.'),
            'next_step_not_contracting': ('NOT_CONTRACTING: separate outer-panel quadrature from the cutoff (V005 scope S3): C4O8 = G4 with its '
                                          'four outer panels at order 8 (104 nodes) and C5O8 = G5 with its six outer panels at order 8 '
                                          '(120 nodes, inside the prep v009 budget), each against C4/C5 with Dhat <= 1; needs a driver '
                                          'successor declaring those two grids and its own prereg version, under separate review.'),
            'next_step_floor_like': ('FLOOR_LIKE: both increments are within tau_i but q > 1/2.  V005 has no floor clause (D14); a floor '
                                     'clause needs a new prereg version with its reason, decided before any further case is run.'),
            'gate_next_steps': {
                'V1': ('(i) monitor stop (wall/RSS/output cap): rerun the same spec in a fresh outdir with the cap raised, separate approval; '
                       '(ii) FAILED_AT_STAGE with a column-pass bracket miss: D7 per V005 later_invocations from the failed call\'s evidence: '
                       'R(n) = previous block + W1 widenings; C5/C6 rerun admitting their own route A, reference and body under v009 with the '
                       'same route_a.max_iterations; C4 rerun as C4R(n) under v005 admitting KMAX_A2F10_C4_V005_RUN_V001; the comparison '
                       'takes --bracket-recovery R(n); (iii) route A without a converged fixed point within 16 iterations '
                       '(ROUTE_A_NO_FIXED_POINT / ITERATION_BUDGET_EXHAUSTED): registered as a measured property of the route-A relaxation at '
                       'that grid; next step: if the saved residual history contracts over its last 3 iterations, rerun with max_iterations 32 '
                       '(v009 ceiling), else a reviewed study of the route-A relaxation (a relaxation change is a new prereg version); '
                       '(iv) BLOCKED admission (C4R(n), admitted reruns): regenerate the admitted spec from the cube outdir under the cube\'s '
                       'driver and rerun; (v) any other FAILED or REFUSED: one rerun of the same spec; a second identical failure is '
                       'reported as a deterministic defect for review.'),
                'V2': ('Picard non-convergence within 6 passes: rerun that case with picard.passes 12 admitting its own route A, reference '
                       'and body (same driver, same route_a.max_iterations); if it still fails, PICARD_NOT_CONVERGED at that grid, stop for review.'),
                'V3': 'Custody mismatch: regenerate the spec with tools/make_ext_specs_c2ext.py from the registered block and rerun that case.',
                'V4': 'Grid/prep defect: stop; review the prep v009 / composite-grid path of driver v009; no rerun before that review.',
                'V5': 'Mask defect: stop; review truncation_mask/apply_mask of the driver that ran the case; no rerun before that review.',
                'V7': ('Route-A prepared inputs differ from the registered expectation: stop; review prep v009, the per-call seed and the '
                       'checkpoint; no rerun before that review.')}},
        'scope_untested': [
            'S-shape: sphere/cylinder at K >= 5 (see criterion.shape_spread_untested).',
            'S1, S2, S4 of V005 unchanged (transfer across parameter space; NGC3198; route-A source azimuths).',
            'S3 of V005 (outer-panel order) unchanged unless X4 (b) runs it.',
            ('S5 cross-driver term: C4 ran under v005 (gal_c2v003 stages), C5/C6 under v009 (gal_c2v004 stages).  TESTED-POSITIVE at G2 '
             '(v008 deciding i and ii, bitwise) and plan-identical v008 = v009 at G3/G4/GR (dry run); UNTESTED in run mode at G4.  Deciding '
             'test: C4V9 = the C4 cube computed under v009 (N8, max_iterations 16) with rows compared bitwise to C4R3; not required by X1-X4 '
             '(a mismatch would be registered as a cross-driver defect for review).'),
            'S6 inner control at G5/G6: carried from G2/GR (R3); deciding test: an inner-order-8 control on G6 (the ten panels inside |k| <= 1/kpc at order 8: 140 nodes per axis, needs prep budget >= 140).'],
        'resources_note': ('V005 rule 3 names a per-call cap >= 6 GiB.  Estimates (analysis/ESTIMATES_V001.json, models stated there, measured '
                           'under load 10-14): route-A serial peak 3.9-4.2 GiB (G5), 5.4-5.9 GiB (G6); route-A N=8 peak about 15 GiB (G5), '
                           '21 GiB (G6); route-B peak 3.8-4.0 / 5.1-5.5 GiB.  Caps are launch parameters (LAUNCH_EXT_V001.json), not part of the rule.'),
        'context_not_used_by_the_decision': ('A21 (qinf_dependence_c2/QINF_DEPENDENCE_V001.md): the lapse response Q(k) = T k^2 c^4/(4 pi G) tends '
                                             'to Qinf = c^4/(16 pi G gamma_eff) with ~1/k^2 corrections (Q(0.3)=7.955, Q(1)=8.053, Q(2)=8.0598, limit '
                                             '8.0623), so above k ~ 2/kpc the response itself is flat to < 0.04%; the K dependence measured here is '
                                             'carried by what the outer panels add to the field, not by a changing response.  Reported for '
                                             'reading the outcome; not used by X1-X4.'),
        'row_ids': pre5['row_ids'], 'tau_km_s': pre5['tau_km_s'], 'quoted_sigma_km_s': pre5['quoted_sigma_km_s'],
    }
    out = HERE / 'prereg_v006/KMAX_MATRIX_PREREG_V006.json'
    b = (json.dumps(pre, indent=1, allow_nan=False) + '\n').encode()
    if out.exists() and out.read_bytes() != b and '--replace-draft' not in sys.argv:
        raise SystemExit('REFUSED: a different V006 draft exists (pass --replace-draft for an unsealed draft)')
    out.write_bytes(b)
    psha = hashlib.sha256(b).hexdigest()
    cs = HERE / 'prereg_v006/kmax_compare_ext_c2v006.py'
    t = cs.read_text()
    t2, n = re.subn(r"^PREREG_SHA256 = '[^']*'$", "PREREG_SHA256 = '%s'" % psha, t, flags=re.M)
    if n != 1:
        raise SystemExit('compare script PREREG line not found exactly once')
    cs.write_text(t2)
    print('V006', psha, 'compare', hashlib.sha256(t2.encode()).hexdigest())


if __name__ == '__main__':
    main()
