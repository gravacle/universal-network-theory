"""Tests of kmax_tail_compare_c2v007.py (V007 compare, Claude2 root lane).  Synthetic branch tests: one per pre-named
outcome (A47-amended first-applicable order), plus the clause tests the brief and A47 require.  Base rows are the REAL R3
results (C2R3/C3R3/C4R3 forward-model rows, read-only); every other run is synthetic (rows = C4R3 + k*tau_i), with no
observed velocity anywhere (tau and sigma come from the pinned V005 prereg).  End-to-end CLI tests run on real R3 / C5R3
bytes.  Writes only into OUT (must not exist).
usage: python3 -I -B tests_kmax_tail_compare_c2v007.py OUT"""
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
CMP = HERE / 'kmax_tail_compare_c2v007.py'
CT = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'
V010 = 'a' * 64          # placeholder driver sha for synthetic T-runs (the real v010 sha is registered in the case block)
UVT_CFG = 'c' * 64


def load(path, name):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


M = load(CMP, 'cmp7')
CTX = M.build_context()
IDS = CTX['ids']
TAU = CTX['tau']
REAL = {k: CTX['C5M'].adapt_result(M.PIN_R3[k][0]) for k in ('C2R3', 'C3R3', 'C4R3')}
for k in REAL:
    assert REAL[k]['result_sha256'] == M.PIN_R3[k][1]


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def case_block(mode=None):
    cb = {'schema': M.CASE_BLOCK_SCHEMA, 'cases': {}}
    if mode:
        cb['route_a_mode'] = mode
    for lab in M.REGISTERED:
        e = {'grid': M.EXPECTED_GRID[lab], 'truncation': M.EXPECTED_TRUNCATION[lab], 'normalized_spec_equal': {}}
        if lab == M.C5H:
            e.update(tail=False, ro1_required=False, call_spec_sha256=M.PIN_C5H_SPEC[1], drivers_allowed=[M.DRIVER_V009_EXT])
        else:
            e.update(tail=True, ro1_required=True, uv_tail_config_sha256=UVT_CFG, drivers_allowed=[V010],
                     normalized_spec_equal={'/numerics/uv_tail': {'config_sha256': UVT_CFG}})
        cb['cases'][lab] = e
    assert not M.validate_case_block(cb), M.validate_case_block(cb)
    return cb


def numerics_for(lab, cw=8):
    n = copy.deepcopy(CTX['c5h_spec_numerics'])
    n['truncation'] = dict(M.EXPECTED_TRUNCATION[lab])
    n['composite_grid_spec'] = CTX['grids'][M.EXPECTED_GRID[lab]]
    if lab != M.C5H:
        n['uv_tail'] = {'config_sha256': UVT_CFG}
        n['route_a'] = {'column_workers': cw, 'max_iterations': 32}
    return n


def passes_from(final, dlast=0.0005, q=1 / 3.0):
    """three Picard passes ending at final: d_last = -dlast, d_prev = -dlast/q (so the E_i ratio is q)."""
    p3 = dict(final)
    p2 = {i: final[i] + dlast for i in IDS}
    p1 = {i: p2[i] + dlast / q for i in IDS}
    return [p1, p2, p3]


def make_run(lab, rows, *, dlast=0.0005, q=1 / 3.0, ea=0.005, flagged=False, cw=8, driver=None, ro1=None, maxit=32,
             numerics=None, ra_ident='e' * 64, uvt_over=None, present=True, ea_none=False):
    """A synthetic run in exactly the read_run() layout."""
    if not present:
        return {'label': lab, 'present': False, 'absent': 'NOT_IN_MANIFEST'}
    rows = dict(rows)
    num = numerics if numerics is not None else numerics_for(lab, cw)
    if lab != M.C5H:
        num.setdefault('route_a', {})['max_iterations'] = maxit
    ns = {'galaxy': 'DDO154', 'physical': CTX['anchor']['physical'], 'coefficients': CTX['anchor']['coefficients'], 'numerics': num}
    pr = passes_from(rows, dlast, q)
    rsha = sha(json.dumps([lab, rows, dlast, q, ea, flagged, cw, maxit]))
    rao = {'classification': 'CONVERGED', 'converged_iteration': 6, 'result_path': '/synthetic', 'result_sha256': 'f' * 64}
    if lab != M.C5H:
        rao['ro1'] = ro1 if ro1 is not None else {'rule': 'RO1', 'fired': False, 'events': []}
    result = {'schema': M.RESULT_SCHEMA, 'status': 'COMPLETED', 'valid': True, 'normalized_spec': ns,
              'driver_sha256': driver or (M.DRIVER_V009_EXT if lab == M.C5H else V010),
              'call_spec_sha256': M.PIN_C5H_SPEC[1] if lab == M.C5H else sha(lab), 'route_a_outcome': rao}
    adapted = {'schema': M.RESULT_SCHEMA, 'status': 'COMPLETED', 'valid': True, 'rows': rows, 'result_sha256': rsha,
               'last_change_km_s': dlast, 'route_a_identity_sha256': ra_ident, 'm4_row_window': 0.01, 'normalized_spec': ns}
    uvt = None
    if lab != M.C5H:
        uvt = {'schema': M.UVT_RA_RECORD_SCHEMA, 'outcome': 'CONVERGED_FINITE_FIXED_POINT', 'production_admissible': True,
               'admissibility': 'production', 'config_sha256': UVT_CFG, 'flags': [M.FLAG_TSU] if flagged else [],
               'monitor_status': 'FLAGGED' if flagged else 'M_T_WITHIN_THRESHOLD', 'M_T_threshold': 0.25,
               'M_T_accepted': 0.3 if flagged else 0.05, 'accepted_iteration': 6,
               'E_A_rows_km_s_accepted': None if ea_none else [ea * TAU[i] for i in IDS]}
        uvt.update(uvt_over or {})
    return {'label': lab, 'dir': '/synthetic/' + lab, 'present': True, 'result': result, 'result_sha256': rsha, 'adapted': adapted,
            'adapted_sha_equal': True, 'finish': {'result_sha256': rsha}, 'receipt': None, 'spec_for_reading': ns, 'spec_source': 'result',
            'pass_rows': pr, 'route_a_outcome': rao, 'uvt_record': uvt, 'uvt_code': None, 'failure': None,
            'ro1_required': lab != M.C5H}


def identity_run(name, ro1_fired=False):
    rows = REAL['C2R3']['rows']
    rsha = sha('id' + name)
    return {'label': name, 'present': True, 'result': {}, 'result_sha256': rsha, 'adapted_sha_equal': True,
            'adapted': {'status': 'COMPLETED', 'valid': True, 'rows': rows}, 'finish': {'result_sha256': rsha}, 'failure': None,
            'route_a_outcome': {'ro1': {'rule': 'RO1', 'fired': ro1_fired,
                                        'events': [{'code': M.RO1_CODE, 'refusal': M.READOUT_REFUSALS[0], 'query': 3, 'phi_rad': 0.785,
                                                    'R_kpc': 1.48, 'numerator': -0.2, 'denominator': 1.0, 'after_convergence': True}]
                                        if ro1_fired else []}}}


def shift(base, k, rows_k=None):
    """base + k*tau_i (k a number) or + rows_k[i]*tau_i."""
    return {i: base[i] + (rows_k[i] if rows_k else k) * TAU[i] for i in IDS}


C2, C3, C4 = REAL['C2R3']['rows'], REAL['C3R3']['rows'], REAL['C4R3']['rows']
D23 = {i: C3[i] - C2[i] for i in IDS}
D34 = {i: C4[i] - C3[i] for i in IDS}


def t1_rows(d23, d34):
    """C2T = C2R3; C3T = C2T + d23; C4T = C3T + d34 (all km/s)."""
    r2 = dict(C2)
    r3 = {i: r2[i] + d23[i] for i in IDS}
    r4 = {i: r3[i] + d34[i] for i in IDS}
    return r2, r3, r4


GOOD_D23 = {i: 2.0 * TAU[i] * (1 if k % 2 == 0 else -1) for k, i in enumerate(IDS)}
GOOD_D34 = {i: 0.4 * TAU[i] * (1 if k % 2 == 0 else -1) for k, i in enumerate(IDS)}


def base_runs(d23=None, d34=None, **over):
    """A complete set of runs that reads ADOPT_TAIL; 'over' replaces or modifies members."""
    r2, r3, r4 = t1_rows(d23 or GOOD_D23, d34 or GOOD_D34)
    R = {'C2T': make_run('C2T', r2), 'C3T': make_run('C3T', r3), 'C4T': make_run('C4T', r4)}
    R['C6T'] = make_run('C6T', shift(r4, 0.1))
    R['S4T'] = make_run('S4T', shift(r4, 0.5))
    R['C5H'] = make_run('C5H', shift(r4, 0.05))
    R['C4T-D5'] = make_run('C4T-D5', shift(r4, 0.1))
    R['C4T-C5c'] = make_run('C4T-C5c', shift(r4, 0.15))
    R['C4T-K16'] = make_run('C4T-K16', shift(r4, 0.05))
    R['C4T-K64'] = make_run('C4T-K64', shift(r4, -0.05))
    R['C4T-A'] = make_run('C4T-A', shift(r4, 0.5))
    for k, v in over.items():
        R[k] = v(R) if callable(v) else v
    return R


# ---------------------------------------------------------------------------------------------------- gate records
def rec(gate, verdict=None, **fields):
    r = {'schema': M.GATE_SCHEMA, 'gate': gate, 'verdict': verdict or M.GATE_PASS_VERDICTS[gate],
         'producer': {'path': '/synthetic/tool_%s.py' % gate, 'sha256': sha(gate)}}
    r.update(fields)
    return r


def _sh(run):
    return run.get('result_sha256') or '0' * 64


def complete_records(R, IDR, sr_delta=None, srb=None, dV_total=0.5, eps=6e-4):
    t12 = [TAU[i] for i in IDS]
    specs = lambda: {'EXT': [{'label': 'V005', 'sha256': 'd' * 64}], 'GEO': [{'label': '2029f26a', 'sha256': '2029f26a' + '0' * 56},
                     {'label': '4ac5527a', 'sha256': M.B0PRIME_RERUN_SPEC_SHA256}], 'NGC': [{'label': 'T', 'sha256': 'b' * 64}]}
    b3case = {k: (0.0 if op == '==' else t / 10) for k, op, t in M.B3_TOL}
    b3case['hi_v003_L67_pass'] = True
    d = sr_delta or {'2': [0.01 * t for t in t12], '3': [0.012 * t for t in t12], '4': [0.013 * t for t in t12]}
    out = {
        'B0': rec('B0', maps={'EXT': {'a': 'b'}, 'GEO': {'c': 'd'}}, spec_sets=specs()),
        'B0prime_DRY': rec('B0prime_DRY', files_compared=['DRYRUN_REPORT.json', 'DRYRUN_PLAN.txt'], spec_sets=specs()),
        'B0prime_RERUN': rec('B0prime_RERUN', run_result_sha256=_sh(IDR['B0prime_RERUN']),
                             reference_result_sha256=M.GEO_DECIDING_I_RESULT_SHA256, call_spec_sha256=M.B0PRIME_RERUN_SPEC_SHA256,
                             declared_exceptions=['elapsed_seconds'], differences_outside_declared=[], tail='OFF'),
        'B0_FA': rec('B0_FA', cases={c: {'status': 'REFUSED', 'code': 'ROUTE_A_CHECKPOINT_MISSING'} for c in ('A1', 'A2', 'A4')}),
        'B1': rec('B1', run_result_sha256=_sh(IDR['Z2']), reference_result_sha256=M.Z2_REFERENCE_RESULT_SHA256, tail='ON',
                  outer_K_big_equals_K=True, precondition_L={'verdict': 'PASS_BITWISE_EQUAL', 'reference_result_sha256': M.PRECONDITION_L_REFERENCE_SHA256},
                  declared_exceptions=['driver_sha256'], differences_outside_custody=[]),
        'B1_OFF': rec('B1_OFF', run_result_sha256=_sh(IDR['Z2-OFF']), reference_result_sha256=M.Z2_REFERENCE_RESULT_SHA256,
                      tail='OFF', declared_exceptions=['driver_sha256'], differences_outside_custody=[]),
        'B2': rec('B2', O_cube_K_out_inverse_kpc=12, azimuths=16,
                  per_state={s: {'state_result_sha256': M.PIN_R3[s][1], 'max_row_diff_km_s': 1e-6, 'sanity_vs_KB12_km_s': 0.01}
                             for s in ('C2R3', 'C3R3', 'C4R3')}),
        'B3': rec('B3', independent_lane='Claude3', imports_tail_library=False, state_result_sha256=M.PIN_R3['C4R3'][1],
                  cases={'cube_O8': dict(b3case), 'cylinder_O8': dict(b3case)}),
        'B0_RO1': rec('B0_RO1', part_a={'identity_runs': {n: {'result_sha256': _sh(IDR[n]), 'ro1_fired': False} for n in M.IDENTITY_RUNS}},
                      part_b={'checkpoint_source': 'C6 iteration 8', 'recorded_code': M.RO1_CODE, 'query': 3, 'handed_to_route_b': True},
                      part_c={'cases': [{'kind': 'OTHER_EXCEPTION', 'expected': 'CALL_FAILED', 'observed': 'CALL_FAILED'},
                                        {'kind': 'REFUSAL_BEFORE_CONVERGENCE', 'expected': 'CALL_FAILED', 'observed': 'CALL_FAILED'}]}),
        'B0_N3': rec('B0_N3', files_scanned=['driver.py'], constructions=[{'file': 'driver.py', 'line': 10, 'guarded': True}],
                     runtime_checks=['B0prime_RERUN', 'B1_OFF']),
        'EPS': rec('EPS', eps_max=eps, evaluator_sha256=M.QINF_EVALUATOR_PREFIX + '0' * 56,
                   coverage_inverse_kpc={'DDO': [2, 64], 'NGC': [2, 32]},
                   shells=[{'range_inverse_kpc': [4, 5], 'eps_base': 5e-4, 'eps_refined': 5.2e-4, 'refinements': 1}]),
        'DOUBLING': rec('DOUBLING', ddo_state_result_sha256=M.PIN_R3['C4R3'][1], ddo_max_change_over_tau=0.01,
                        ngc_operator_sha256=M.NGC_T120L_OPERATOR_SHA256, ngc_max_change_over_theta=0.01),
        'GQ': rec('GQ', rosters=[{'roster': n, 'k_range_inverse_kpc': [2, kb], 'M_s': 64, 'M_s_doubled': 128, 'nodes': 4096,
                                  'max_abs_diff_over_P0': 1e-14} for n, kb in M.GQ_REQUIRED.items()]),
        'LO': rec('LO', state_result_sha256=M.PIN_R3['C4R3'][1], summed_max_over_tau=0.01,
                  shells=[{'range_inverse_kpc': list(r), 'max_over_tau': 0.001} for r in M.LO_RANGES]),
        'LO_NGC': rec('LO_NGC', operator_sha256=M.NGC_T120L_OPERATOR_SHA256, summed_max_over_theta=0.01,
                      shells=[{'range_inverse_kpc': list(r), 'max_over_theta': 0.001} for r in M.LO_NGC_RANGES]),
        'I1T': rec('I1T', builds=[{'case': c, 'stage': 'route_a', 'max_rel': 1e-15, 'nodes': 4096} for c in M.T_CASES]),
        'T2I': rec('T2I', case='C5H', region='G5\\G4', c5h_result_sha256=R['C5H']['result_sha256'],
                   components={'route_a_updated': 1e-14, 'offset_new_body_fourier_J': 1e-14, 'feedback_gas_source_feedback': 1e-14}, max_rel=1e-14),
        'SRB_ROT': rec('SRB_ROT', case='C4T', c4t_result_sha256=R['C4T']['result_sha256'], srb_rot_km_s=srb or [0.01 * t for t in t12]),
        'RB_FP': rec('RB_FP', case='C4T', c4t_result_sha256=R['C4T']['result_sha256'], eps_max=eps, shells=['4-8', '8-32'],
                     dV_static_shells_km_s={'4-8': [dV_total * 0.7] * 12, '8-32': [dV_total * 0.3] * 12}),
        'SR_K': rec('SR_K', states={s: M.PIN_R3[s][1] for s in ('C2R3', 'C3R3', 'C4R3')}, Delta_km_s=d),
        'EA': rec('EA', per_case={'C5H': {'result_sha256': R['C5H']['result_sha256'], 'E_A_rows_km_s': [0.005 * t for t in t12],
                                          'accepted_iteration': 7}}),
        'HARMONICS': rec('HARMONICS', rows=[{'case': 'C4T', 'source': 'replay', 'query': 3, 'R_kpc': 1.48, 'a0': 2.0, 'a4': 0.2,
                                             'a8': -0.5, 'units': '1e-28/m'}]),
        'MT': rec('MT', per_case={c: {'result_sha256': _sh(R[c]), 'M_T_accepted': ((R[c].get('uvt_record') or {}).get('M_T_accepted') or 0.05),
                                      'flags': list((R[c].get('uvt_record') or {}).get('flags') or [])} for c in M.T_CASES}),
        'FLAG_RULINGS': rec('FLAG_RULINGS', rulings=[])}
    return out


def write_records(out, tag, records):
    d = out / 'gates' / tag
    d.mkdir(parents=True)
    paths = {}
    for g, r in records.items():
        if r is None:
            paths[g] = None
            continue
        p = d / ('%s.json' % g)
        p.write_text(json.dumps(r, indent=1))
        paths[g] = str(p)
    return paths


def run_eval(out, tag, R=None, IDR=None, mutate=None, drop=(), RP=None, mode=None, packets_bad=()):
    ctx = dict(CTX)
    ctx['case_block'] = case_block()
    if mode:
        ctx['route_a_mode'] = mode
    ctx['c4r3_adapted'] = REAL['C4R3']
    R = R if R is not None else base_runs()
    IDR = IDR if IDR is not None else {n: identity_run(n) for n in M.IDENTITY_RUNS}
    records = complete_records(R, IDR)
    if mutate:
        mutate(records)
    for g in drop:
        records[g] = None
    paths = write_records(out, tag, records)
    rsha = M.runs_sha_map(R, IDR, RP)
    gates = M.cross_gate_checks({g: M.evaluate_gate(g, paths.get(g), ctx, rsha) for g in M.ALL_GATES}, R)
    packets = {k: {'V4': k not in packets_bad, 'V5': True} for k in list(R) + ['%s@RPAIR:%s' % (m, p) for p, rp in (RP or {}).items() for m in rp['_runs']]}
    return M.evaluate_v007(ctx, R, IDR, gates, RP or {}, packets)


TESTS = []


def check(name, ev, outcome, extra=None, why=''):
    d = ev['decision']
    ok = d['outcome'] == outcome and (extra is None or bool(extra(ev)))
    TESTS.append({'test': name, 'pass': bool(ok), 'outcome': d['outcome'], 'position': d.get('position'), 'expected': outcome,
                  'reasons': [str(x)[:300] for x in (d['reasons'] if isinstance(d['reasons'], list) else [d['reasons']])][:4],
                  'why': why})


def t(name, cond, **info):
    TESTS.append({'test': name, 'pass': bool(cond), **{k: (str(v)[:400]) for k, v in info.items()}})


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    # ================================================================ one branch test per outcome (first-applicable order)
    check('O16_ADOPT_TAIL', run_eval(out, 'adopt'), 'ADOPT_TAIL',
          extra=lambda e: all(e['decision']['carried_numerical_uncertainty_km_s'][i] is not None for i in IDS)
          and abs(e['decision']['carried_terms']['K34'][IDS[0]] - 0.4 * TAU[IDS[0]]) < 1e-9)

    def b3fail(r):
        r['B3']['cases']['cube_O8']['value_rel'] = 1e-6
    check('O01_NO_RUN_B3_FAIL_IS_IMPLEMENTATION_DEFECT_OF_GATE', run_eval(out, 'b3', mutate=b3fail), 'NO_RUN',
          extra=lambda e: 'B3' in str(e['decision'].get('subtype')))

    def b1off_fail(r):
        r['B1_OFF']['differences_outside_custody'] = ['/passes/0/rows']
    check('O01b_NO_RUN_B1_OFF_FAIL_Z2OFF_MANDATORY_A47_I6', run_eval(out, 'b1off', mutate=b1off_fail), 'NO_RUN')
    check('O02_INCOMPLETE_MISSING_CASE', run_eval(out, 'miss', R=base_runs(**{'C6T': make_run('C6T', {}, present=False)})), 'INCOMPLETE',
          extra=lambda e: any('C6T' in r for r in e['decision']['reasons']) and e['decision']['tests_read'] is False)
    check('O02b_INCOMPLETE_B1_OFF_RECORD_MISSING_A47_I6', run_eval(out, 'b1offmiss', drop=('B1_OFF',)), 'INCOMPLETE',
          extra=lambda e: any('B1_OFF' in r for r in e['decision']['reasons']))
    check('O02c_INCOMPLETE_IDENTITY_RUN_Z2OFF_MISSING_A47_I1', run_eval(out, 'idmiss', IDR={**{n: identity_run(n) for n in M.IDENTITY_RUNS},
                                                                                              'Z2-OFF': {'present': False, 'absent': 'NO_RUN_DIR'}}),
          'INCOMPLETE', extra=lambda e: any('Z2-OFF' in r for r in e['decision']['reasons']))

    def eps_unc(r):
        r['EPS']['verdict'] = 'EPS_UNCERTIFIED'
    check('O03_NUMERICS_UNCERTIFIED_EPS', run_eval(out, 'eps', mutate=eps_unc), 'NUMERICS_UNCERTIFIED')

    def gq_fail(r):
        r['GQ']['rosters'][2]['max_abs_diff_over_P0'] = 2e-12
    check('O03b_NUMERICS_UNCERTIFIED_GQ_RA7', run_eval(out, 'gq', mutate=gq_fail), 'NUMERICS_UNCERTIFIED',
          extra=lambda e: any('UV_TAIL_GAS_QUADRATURE_UNCERTIFIED' in r for r in e['decision']['reasons']))

    def lo_fail(r):
        r['LO']['shells'][3]['max_over_tau'] = 0.006
    check('O03c_NON_LAPSE_TAIL_MATERIAL_LO', run_eval(out, 'lo', mutate=lo_fail), 'NON_LAPSE_TAIL_MATERIAL',
          extra=lambda e: e['decision']['position'] == 3)
    check('O04_UNDECIDABLE_ROUTE_A_TAIL', run_eval(out, 'uta', R=base_runs(**{'C4T-K16': lambda R: dict(make_run('C4T-K16', R['C4T-K16']['adapted']['rows'], flagged=True))})),
          'UNDECIDABLE_ROUTE_A_TAIL')
    # undecidable pair (slow Picard) on T3_K16 with an R-PAIR that is still undecidable -> iteration floor
    slow = dict(dlast=0.001, q=0.95)                       # E_i = 9 * 0.001 km/s per run: > tau_i/8 on rows 06-09

    def undecidable_k16(R):
        return make_run('C4T-K16', R['C4T-K16']['adapted']['rows'], **slow)
    Rf = base_runs(**{'C4T-K16': undecidable_k16})
    ev_pend = run_eval(out, 'pend', R=Rf)
    check('O05a_RPAIR_PENDING_READS_INCOMPLETE_WITH_BRANCH', ev_pend, 'INCOMPLETE',
          extra=lambda e: e['tests']['T3']['pairs']['T3_K16']['status'] == 'RPAIR_PENDING'
          and e['tests']['T3']['pairs']['T3_K16']['rpair_branch'] == 'PICARD')
    RPf = {'T3_K16': {'branch': 'PICARD', '_runs': {'C4T': make_run('C4T', Rf['C4T']['adapted']['rows']),
                                                    'C4T-K16': make_run('C4T-K16', Rf['C4T-K16']['adapted']['rows'], **slow)}}}
    for m in RPf['T3_K16']['_runs'].values():
        m['result']['normalized_spec']['numerics']['picard'] = dict(M.RPAIR_PICARD)
    ev_floor = run_eval(out, 'floor', R=Rf, RP=RPf)
    check('O05_UNDECIDABLE_AT_ITERATION_FLOOR_NEITHER_PASS_NOR_FAIL', ev_floor, 'UNDECIDABLE_AT_ITERATION_FLOOR',
          extra=lambda e: e['tests']['T3']['pairs']['T3_K16']['status'] not in ('PASS', 'FAIL')
          and e['tests']['T3']['status'] == 'UNDECIDABLE_AT_ITERATION_FLOOR')
    RPok = copy.deepcopy(RPf)
    for m, run in RPok['T3_K16']['_runs'].items():
        RPok['T3_K16']['_runs'][m] = make_run(m, run['adapted']['rows'], dlast=0.0002, q=1 / 3.0)
        RPok['T3_K16']['_runs'][m]['result']['normalized_spec']['numerics']['picard'] = dict(M.RPAIR_PICARD)
    check('O05b_RPAIR_PICARD_DECIDED_PASS_THEN_ADOPT', run_eval(out, 'rpok', R=Rf, RP=RPok), 'ADOPT_TAIL',
          extra=lambda e: e['tests']['T3']['pairs']['T3_K16']['source'] == 'RPAIR' and e['rpair_validity']['C4T@RPAIR:T3_K16']['V6'] is True)
    RPbad = copy.deepcopy(RPok)
    RPbad['T3_K16']['branch'] = 'ROUTE_A'
    check('O05c_RPAIR_BRANCH_MISMATCH_INCOMPLETE', run_eval(out, 'rpbad', R=Rf, RP=RPbad), 'INCOMPLETE')
    Rra = base_runs(**{'C4T-K16': lambda R: make_run('C4T-K16', R['C4T-K16']['adapted']['rows'], ea=0.2)})
    ev_ra = run_eval(out, 'rabranch', R=Rra)
    t('O05d_RPAIR_BRANCH_ROUTE_A_WHEN_EA_DOMINATES', ev_ra['tests']['T3']['pairs']['T3_K16'].get('rpair_branch') == 'ROUTE_A',
      branch=ev_ra['tests']['T3']['pairs']['T3_K16'].get('rpair_branch'))
    check('O06_IMPLEMENTATION_DEFECT_T2_DECIDABLE_FAILS', run_eval(out, 't2', R=base_runs(**{'C4T-D5': lambda R: make_run('C4T-D5', shift(R['C5H']['adapted']['rows'], 0.3))})),
          'IMPLEMENTATION_DEFECT')
    check('O07_SOURCE_RULE_MATERIAL_T2c', run_eval(out, 't2c', R=base_runs(**{'C4T-C5c': lambda R: make_run('C4T-C5c', shift(R['C4T-D5']['adapted']['rows'], 0.6))})),
          'SOURCE_RULE_MATERIAL')
    check('O08_KBIG_NOT_CONVERGED_T3', run_eval(out, 't3', R=base_runs(**{'C4T-K64': lambda R: make_run('C4T-K64', shift(R['C4T']['adapted']['rows'], 0.3))})),
          'KBIG_NOT_CONVERGED')
    check('O09_BOUND_INSUFFICIENT_RB_FP', run_eval(out, 'rbfp', R=base_runs(**{'C4T-A': lambda R: make_run('C4T-A', shift(R['C4T']['adapted']['rows'], 10.0))})),
          'BOUND_INSUFFICIENT')

    def srb_fail(r):
        r['SRB_ROT']['srb_rot_km_s'][5] = 0.2 * TAU[IDS[5]]
    check('O09b_BOUND_INSUFFICIENT_SRB_ROT', run_eval(out, 'srb', mutate=srb_fail), 'BOUND_INSUFFICIENT')
    # T1-fail split.  FLOOR_LIKE: increments <= tau but non-contracting (Dhat23 <= 1, Dhat34 <= 1)
    fl23 = {i: 0.5 * TAU[i] for i in IDS}
    fl34 = {i: 0.4 * TAU[i] for i in IDS}
    check('O10_FLOOR_LIKE_BEFORE_T1_FAIL_SPLIT', run_eval(out, 'floorlike', R=base_runs(d23=fl23, d34=fl34)), 'FLOOR_LIKE',
          extra=lambda e: e['tests']['T1']['status'] == 'FAIL' and e['tests']['T1']['floor_like'],
          why='the same T1 failure would otherwise read NOT_UV_RESIDUAL (T2c and SR-K within tau/4): FLOOR_LIKE precedes the split')
    big23 = {i: 4.0 * TAU[i] for i in IDS}
    big34 = {i: 3.0 * TAU[i] for i in IDS}
    check('O11_NOT_UV_RESIDUAL', run_eval(out, 'notuv', R=base_runs(d23=big23, d34=big34)), 'NOT_UV_RESIDUAL')

    def srk_kdep(r):
        r['SR_K']['Delta_km_s']['3'][4] = 0.5 * TAU[IDS[4]]
    check('O12_SOURCE_REPRESENTATION_K_DEPENDENT', run_eval(out, 'srkd', R=base_runs(d23=big23, d34=big34), mutate=srk_kdep),
          'SOURCE_REPRESENTATION_K_DEPENDENT')
    check('O13_HIGHER_K_DISAGREEMENT', run_eval(out, 'hk', R=base_runs(**{'C6T': lambda R: make_run('C6T', shift(R['C4T']['adapted']['rows'], 0.6))})),
          'HIGHER_K_DISAGREEMENT')
    check('O14_SHAPE_DISAGREEMENT', run_eval(out, 'shape', R=base_runs(**{'S4T': lambda R: make_run('S4T', shift(R['C4T']['adapted']['rows'], 2.5))})),
          'SHAPE_DISAGREEMENT')

    def sqm(r):
        r['SR_K']['Delta_km_s']['4'][2] = 1.5 * TAU[IDS[2]]
        r['SR_K']['Delta_km_s']['3'][2] = 1.4 * TAU[IDS[2]]
        r['SR_K']['Delta_km_s']['2'][2] = 1.3 * TAU[IDS[2]]
    check('O15_FLAG_PENDING_RULING_SOURCE_QUADRATURE_MATERIAL', run_eval(out, 'sqm', mutate=sqm), 'FLAG_PENDING_RULING')

    def sqm_ruled(r):
        sqm(r)
        r['FLAG_RULINGS']['rulings'] = [{'flag': M.FLAG_SQM, 'scope': 'C4T', 'ruling': 'RULED', 'root_decision': 'A99 (synthetic)'}]
    check('O15b_FLAG_RULED_THEN_ADOPT', run_eval(out, 'sqmruled', mutate=sqm_ruled), 'ADOPT_TAIL')
    # ================================================================ flagged-run route, A47 I1, per-row clause, TINY
    check('F1_FLAGGED_RUN_UTA_AHEAD_OF_IMPLEMENTATION_DEFECT',
          run_eval(out, 'flagt2', R=base_runs(**{'C4T-D5': lambda R: make_run('C4T-D5', shift(R['C5H']['adapted']['rows'], 0.3), flagged=True)})),
          'UNDECIDABLE_ROUTE_A_TAIL', extra=lambda e: e['tests']['T2']['status'] == 'UNDECIDABLE_ROUTE_A_TAIL')
    check('F2_FLAG_ON_ANY_TEST_PREEMPTS_UNFLAGGED_T2_FAIL_LITERAL_ORDER',
          run_eval(out, 'flagk16', R=base_runs(**{'C4T-D5': lambda R: make_run('C4T-D5', shift(R['C5H']['adapted']['rows'], 0.3)),
                                                  'C4T-K16': lambda R: make_run('C4T-K16', R['C4T-K16']['adapted']['rows'], flagged=True)})),
          'UNDECIDABLE_ROUTE_A_TAIL', extra=lambda e: e['tests']['T2']['status'] == 'FAIL', why='AMB-04')

    def invalid_c3t(R):
        r = make_run('C3T', R['C3T']['adapted']['rows'], maxit=16)
        return r
    check('A47_I1_INVALID_T_CASE_CANNOT_REACH_NOT_UV_RESIDUAL', run_eval(out, 'i1a', R=base_runs(d23=big23, d34=big34, **{'C3T': invalid_c3t})),
          'INCOMPLETE', extra=lambda e: e['decision']['tests_read'] is False)
    check('A47_I1_INVALID_T_CASE_CANNOT_REACH_SOURCE_REPRESENTATION_K_DEPENDENT',
          run_eval(out, 'i1b', R=base_runs(d23=big23, d34=big34, **{'C2T': lambda R: make_run('C2T', R['C2T']['adapted']['rows'], cw=1)}), mutate=srk_kdep),
          'INCOMPLETE')
    check('A47_I1_INVALID_C5H_READS_INCOMPLETE', run_eval(out, 'i1c', R=base_runs(**{'C5H': lambda R: make_run('C5H', R['C5H']['adapted']['rows'], driver=V010)})),
          'INCOMPLETE', extra=lambda e: any(r.startswith('C5H') for r in e['decision']['reasons']))
    check('A47_I1_INVALID_C4T_D5_READS_INCOMPLETE', run_eval(out, 'i1d', R=base_runs(), packets_bad=('C4T-D5',)), 'INCOMPLETE',
          extra=lambda e: any(r.startswith('C4T-D5') for r in e['decision']['reasons']))
    s = 0.99 / max(abs(D34[i]) / TAU[i] for i in IDS)                                                 # G1 (Claude4 0047 / A47)
    ev = run_eval(out, 'g1', R=base_runs(d23={i: s * D23[i] for i in IDS}, d34={i: s * D34[i] for i in IDS}))
    t1 = ev['tests']['T1']
    t('RA6_G1_R3_SCALED_MAX_BASED_PASSES_PER_ROW_FAILS', t1['shape_pass_V005'] and not t1['per_row_clause_pass'] and t1['status'] == 'FAIL'
      and t1['fail_by'] == ['PER_ROW'] and not t1['floor_like'] and ev['decision']['outcome'] in ('NOT_UV_RESIDUAL', 'SOURCE_REPRESENTATION_K_DEPENDENT'),
      outcome=ev['decision']['outcome'], failing_rows=[i[-2:] for i, x in t1['per_row_clause'].items() if x.startswith('FAIL')])
    g2a = {i: (0.3 if i.endswith('_04') else 2.0) * TAU[i] * (1 if k % 2 == 0 else -1) for k, i in enumerate(IDS)}
    g2b = {i: (0.84 if i.endswith('_04') else 0.4) * TAU[i] * (1 if k % 2 == 0 else -1) for k, i in enumerate(IDS)}
    ev = run_eval(out, 'g2', R=base_runs(d23=g2a, d34=g2b))
    t1 = ev['tests']['T1']
    t('RA6_G2_GROWING_ROW04_HIDDEN_UNDER_MAX_CAUGHT', t1['shape_pass_V005'] and t1['status'] == 'FAIL'
      and [i[-2:] for i, x in t1['per_row_clause'].items() if x.startswith('FAIL')] == ['04'], outcome=ev['decision']['outcome'])
    g3b = {i: (-0.05 if i.endswith('_03') else 0.8) * TAU[i] for i in IDS}
    ev = run_eval(out, 'g3', R=base_runs(d23={i: 2.0 * TAU[i] for i in IDS}, d34=g3b))
    t('RA6_G3_SIGN_CHANGE_ROW03_CAUGHT', ev['tests']['T1']['per_row_clause'][IDS[2]] == 'FAIL_SIGN' and ev['tests']['T1']['status'] == 'FAIL')
    g4a = {i: (1e-7 if i.endswith('_07') else 2.0 * TAU[i]) for i in IDS}
    g4b = {i: (1e-6 if i.endswith('_07') else 0.8 * TAU[i]) for i in IDS}
    ev = run_eval(out, 'g4', R=base_runs(d23=g4a, d34=g4b))
    t('RA6_G4_TINY_EXEMPTION_PICARD_NOISE_ROW_PASSES', ev['tests']['T1']['status'] == 'PASS' and ev['tests']['T1']['tiny_rows'] == [IDS[6]]
      and ev['decision']['outcome'] == 'ADOPT_TAIL', outcome=ev['decision']['outcome'])
    g5a, g5b = dict(g2a), dict(g2b)
    g5a[IDS[3]], g5b[IDS[3]] = 0.01 * TAU[IDS[3]], 0.12 * TAU[IDS[3]]
    ev = run_eval(out, 'g5', R=base_runs(d23=g5a, d34=g5b))
    t('RA6_G5_TINY_BLIND_SPOT_T1_PASSES', ev['tests']['T1']['status'] == 'PASS' and IDS[3] in ev['tests']['T1']['tiny_rows'])
    # backstop: the same G5 row keeps growing to K=6 -> T1_H (no TINY) catches it
    r4 = ev['rows_km_s']['C4T']
    c6 = shift(r4, 0.1)
    c6[IDS[3]] = r4[IDS[3]] + 1.44 * TAU[IDS[3]] * (1 if g5b[IDS[3]] > 0 else -1)
    ev = run_eval(out, 'g5b', R=base_runs(d23=g5a, d34=g5b, **{'C6T': make_run('C6T', c6)}))
    check('RA6_G5_BACKSTOP_T1_H_NO_TINY_HIGHER_K_DISAGREEMENT', ev, 'HIGHER_K_DISAGREEMENT')
    tiny23 = {i: 0.10 * TAU[i] for i in IDS}
    tiny34 = {i: 0.09 * TAU[i] for i in IDS}
    ev = run_eval(out, 'tinymax', R=base_runs(d23=tiny23, d34=tiny34))
    t('A47_I2_TINY_DOES_NOT_EXEMPT_MAX_BASED_SHAPE_PASS', ev['tests']['T1']['per_row_clause_pass'] and not ev['tests']['T1']['shape_pass_V005']
      and ev['decision']['outcome'] == 'FLOOR_LIKE', outcome=ev['decision']['outcome'])
    # ================================================================ BRACKET_HULL_MISS / RO1 / missing fields / A47 I4 I5
    for tag, block, want in (('hull', CTX['ra4_block'], 'BRACKET_HULL_MISS'),
                             ('offhull', {'mode': 'rule', 'rule': {**CTX['ra4_block']['rule'], 'fs_absolute_overrides': {'0': [3.025e8, 3.17625e8]}}},
                              'BRACKET_MISS_OFF_RA4_BLOCK')):
        d = out / 'runs' / ('bracket_' + tag)
        sd = d / 'stages' / '05_fs_columns_00'
        (sd / 'columns').mkdir(parents=True)
        (sd / 'columns' / 'finish.json').write_text(json.dumps({'status': 'LAGGED_FREE_SURFACE_COLUMNS_ONLY', 'completed': [],
                                                                 'failures': [{'index': 1, 'type': 'ValueError',
                                                                               'message': 'MASS_ENTHALPY_NOT_BRACKETED: supply a resolved compact-support bracket'}]}))
        res = {'schema': M.RESULT_SCHEMA, 'status': 'FAILED_AT_STAGE', 'valid': False, 'reasons': ["stage(s) exited nonzero: ['fs_rotation']"],
               'driver_sha256': V010, 'call_spec_sha256': 'd' * 64, 'passes': [],
               'stage_records': [{'name': 'fs_columns_00', 'kind': 'columns_v001', 'exit_code': 0, 'stage_dir': str(sd)},
                                 {'name': 'fs_rotation', 'kind': 'rotation_v001', 'exit_code': 1, 'stage_dir': str(d / 'stages' / '09')}]}
        raw = json.dumps(res).encode()
        (d / 'result.json').write_bytes(raw)
        (d / 'finish.json').write_text(json.dumps({'status': 'FAILED_AT_STAGE', 'result_sha256': hashlib.sha256(raw).hexdigest()}))
        ns = {'galaxy': 'DDO154', 'numerics': {'brackets': block}}
        (d / 'start.json').write_text(json.dumps({'normalized_spec': ns}))
        ctx = dict(CTX, case_block=case_block())
        run = M.read_run('C3T', str(d), ctx, True)
        R = base_runs(**{'C3T': run})
        ev = run_eval(out, 'br_' + tag, R=R)
        check('BRACKET_%s_READING' % tag.upper(), ev, 'INCOMPLETE',
              extra=lambda e, want=want: e['validity']['C3T']['reading'] == want
              and (want != 'BRACKET_HULL_MISS' or e['decision']['next_step']['C3T']['V1'] == M.RA4_NEXT))
    ro1 = {'rule': 'RO1', 'fired': True, 'events': [{'code': M.RO1_CODE, 'refusal': 'NO_SUBLUMINAL_CIRCULAR_PRESSURE_BRANCH', 'query': 3,
                                                       'phi_rad': 0.785, 'R_kpc': 1.48, 'numerator': -0.2, 'denominator': 1.1, 'after_convergence': True}]}
    check('RO1_FIRED_IN_T_RUN_RECORDED_NOT_INVALID', run_eval(out, 'ro1', R=base_runs(**{'C6T': lambda R: make_run('C6T', R['C6T']['adapted']['rows'], ro1=ro1)})),
          'ADOPT_TAIL', extra=lambda e: e['validity']['C6T']['valid_all'] and 'C6T' in e['ro1_recorded'])
    bad_ro1 = copy.deepcopy(ro1)
    del bad_ro1['events'][0]['denominator']
    ev = run_eval(out, 'ro1bad', R=base_runs(**{'C6T': lambda R: make_run('C6T', R['C6T']['adapted']['rows'], ro1=bad_ro1)}))
    check('RO1_RECORD_MISSING_FIELD_LOUD', ev, 'INCOMPLETE',
          extra=lambda e: 'FIELD_MISSING:result:route_a_outcome/ro1/events[0]:denominator' in e['validity']['C6T']['V3_mismatch'])
    check('RA5a_RO1_FIRED_IN_IDENTITY_RUN_NO_RUN', run_eval(out, 'ro1id', IDR={**{n: identity_run(n) for n in M.IDENTITY_RUNS}, 'Z2': identity_run('Z2', ro1_fired=True)}),
          'NO_RUN')
    check('A47_I5_MAX_ITERATIONS_16_INVALID', run_eval(out, 'maxit', R=base_runs(**{'C4T-K64': lambda R: make_run('C4T-K64', R['C4T-K64']['adapted']['rows'], maxit=16)})),
          'INCOMPLETE', extra=lambda e: 'route_a.max_iterations!=32' in e['validity']['C4T-K64']['V3_mismatch'])
    ev = run_eval(out, 'iter')
    t('A47_I5_ACCEPTED_ITERATION_REPORTED', all(ev['accepted_route_a_iteration'][c] == 6 for c in M.REGISTERED), it=ev['accepted_route_a_iteration'])
    check('A47_I4_PARALLEL8_SERIAL_T_CASE_INVALID', run_eval(out, 'cw1', R=base_runs(**{'C4T': lambda R: make_run('C4T', R['C4T']['adapted']['rows'], cw=1)})),
          'INCOMPLETE')
    Rser = base_runs()
    for lab in M.T_CASES:
        Rser[lab] = make_run(lab, Rser[lab]['adapted']['rows'], cw=1)
    check('A47_I4_SERIAL_WITH_EXEMPTION_ALTERNATIVE_ADOPTS', run_eval(out, 'serial', R=Rser, mode='serial_with_exemption'), 'ADOPT_TAIL')
    check('A47_I4_PARALLEL8_C4TD5_SERIAL_NOT_EXEMPT', run_eval(out, 'd5ser', R=base_runs(**{'C4T-D5': lambda R: make_run('C4T-D5', R['C4T-D5']['adapted']['rows'], cw=1)})),
          'INCOMPLETE', extra=lambda e: any('numerics_not_byte_equal_to_C5H' in x for x in e['validity']['C4T-D5']['V3_mismatch']))

    def t2i_fail(r):
        r['T2I']['max_rel'] = 1e-9
    check('T2I_FAIL_T2_NOT_READ_INCOMPLETE', run_eval(out, 't2i', mutate=t2i_fail), 'INCOMPLETE',
          extra=lambda e: e['tests']['T2']['status'] == 'NOT_READ')

    def i1t_fail(r):
        r['I1T']['builds'][3]['max_rel'] = 1e-9
    check('I1T_FAIL_CASE_INVALID_INCOMPLETE', run_eval(out, 'i1t', mutate=i1t_fail), 'INCOMPLETE',
          extra=lambda e: 'I1T' in e['validity'][M.T_CASES[3]]['failed'])
    check('UVT_FLAG_INCONSISTENT_INVALID', run_eval(out, 'uvtinc', R=base_runs(**{'C4T': lambda R: make_run('C4T', R['C4T']['adapted']['rows'], uvt_over={'M_T_accepted': 0.4})})),
          'INCOMPLETE', extra=lambda e: 'UVT_FLAG_INCONSISTENT' in e['validity']['C4T']['V3_mismatch'])
    ev = run_eval(out, 'eanone', R=base_runs(**{'C6T': lambda R: make_run('C6T', R['C6T']['adapted']['rows'], ea_none=True)}))
    check('EA_UNAVAILABLE_READS_INCOMPLETE_UNRESOLVED', ev, 'INCOMPLETE', extra=lambda e: e['tests']['T1_H']['status'] == 'INCOMPLETE',
          why='E^A null in the route-A record and C6T absent from the EA record: decidability unknown, never a pass')

    def mt_mismatch(r):
        r['MT']['per_case']['C4T']['flags'] = [M.FLAG_TSU]
    check('MT_CROSSCHECK_MISMATCH_RECORD_DEFECT_NO_RUN', run_eval(out, 'mt', mutate=mt_mismatch), 'NO_RUN')

    def rb_eps(r):
        r['RB_FP']['eps_max'] = 7e-4
    check('RB_FP_EPS_CROSSREF_RECORD_DEFECT_NO_RUN', run_eval(out, 'rbeps', mutate=rb_eps), 'NO_RUN')

    def wrong_ref(r):
        r['B1']['run_result_sha256'] = '9' * 64
    check('GATE_CROSSREF_RUN_SHA_MISMATCH_NO_RUN', run_eval(out, 'xref', mutate=wrong_ref), 'NO_RUN')

    def lo_state(r):
        r['LO']['state_result_sha256'] = '8' * 64
    check('LO_WRONG_STATE_IS_DEFECT_NOT_NON_LAPSE_TAIL_MATERIAL', run_eval(out, 'lostate', mutate=lo_state), 'NO_RUN')
    # ================================================================ missing-field gate failure, every gate, every field (E-SEAL1)
    R0, IDR0 = base_runs(), {n: identity_run(n) for n in M.IDENTITY_RUNS}
    recs = complete_records(R0, IDR0)
    rsha = M.runs_sha_map(R0, IDR0)
    ctx = dict(CTX, case_block=case_block())
    common, G = M.gate_field_contract()
    total = bad = 0
    detail = []
    unread = []
    for g, r in recs.items():
        p = out / 'gates' / 'mf' / ('%s.json' % g)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(r))
        ok0 = M.evaluate_gate(g, str(p), ctx, rsha)
        if ok0['status'] != 'PASS':
            bad += 1
            detail.append('%s complete record not PASS: %s' % (g, ok0['codes']))
        pats = [_pat(x[0]) for x in common + G[g]]
        for fr in ok0['fields_read']:
            if not any(re.fullmatch(pt, fr) for pt in pats):
                unread.append('%s:%s' % (g, fr))
        for path, expect in _leaf_paths(g, r):
            total += 1
            r2 = copy.deepcopy(r)
            _delete(r2, path)
            q = out / 'gates' / 'mf' / ('%s__%d.json' % (g, total))
            q.write_text(json.dumps(r2))
            ev = M.evaluate_gate(g, str(q), ctx, rsha)
            if ev['status'] != 'RECORD_DEFECT' or not any(expect in c for c in ev['codes']):
                bad += 1
                detail.append('%s delete %s -> %s %s (expected %s)' % (g, path, ev['status'], ev['codes'], expect))
    t('E_SEAL1_EVERY_GATE_FIELD_DELETION_FAILS_LOUDLY_NAMING_IT', bad == 0 and total > 150, deletions=total, failures=detail[:10])
    t('E_SEAL1_EVERY_FIELD_READ_IS_DOCUMENTED_IN_FIELDS_MD', not unread, undocumented=unread[:20])
    missing = M.evaluate_gate('EPS', None, ctx, rsha)
    t('GATE_RECORD_ABSENT_READS_MISSING', missing['status'] == 'MISSING' and missing['codes'] == ['GATE_RECORD_MISSING:EPS'])
    v = M.case_validity('C4T', dict(make_run('C4T', C4), uvt_record={k: x for k, x in make_run('C4T', C4)['uvt_record'].items() if k != 'E_A_rows_km_s_accepted'}),
                        ctx, {'V4': True, 'V5': True}, {c: 'PASS' for c in M.T_CASES}, None)
    t('UVT_RECORD_MISSING_FIELD_NAMED', 'FIELD_MISSING:route_a_attempt_result:result/uv_tail:E_A_rows_km_s_accepted' in v['V3_mismatch'],
      codes=v['V3_mismatch'])
    # ================================================================ CLI end-to-end on real bytes (+ A47 I3 blinding)
    cbp = out / 'CASE_BLOCK_PROBE.json'
    cb = case_block()
    cbp.write_text(json.dumps(cb, indent=1))
    man = {'schema': M.MANIFEST_SCHEMA, 'cases': {'C2T': CT + '/runs/KMAX_A2F10_C2R3_D7R3_RUN_V001', 'C3T': CT + '/runs/KMAX_A2F10_C3R3_D7R3_RUN_V001',
                                                  'C4T': CT + '/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001', 'C5H': CT + '/runs_ext/KMAX_A2F10_C5R3_RUN_V001'},
           'identity_runs': {}, 'gates': {}}
    mp = out / 'MANIFEST_REAL_PROBE.json'
    mp.write_text(json.dumps(man, indent=1))

    def cli(name, *extra):
        p = subprocess.run([PY, '-I', '-B', str(CMP), '--prereg', M.PIN_DRAFT_R1[0], '--manifest', str(mp), '--case-block', str(cbp),
                            '--outdir', str(out / name), '--test-allow-unpinned-prereg'] + list(extra), capture_output=True, text=True)
        (out / (name + '.stdout.txt')).write_text(p.stdout + '\n--- stderr ---\n' + p.stderr)
        return p
    p = cli('E2E_REAL_PROBE')
    rep = json.loads((out / 'E2E_REAL_PROBE' / 'KMAX_TAIL_COMPARISON.json').read_text()) if p.returncode == 0 else {}
    t('E2E_REAL_R3_PROBE_READS_INCOMPLETE_NOT_A_SILENT_PASS', p.returncode == 0 and rep['decision']['outcome'] == 'INCOMPLETE' and rep['test_mode']
      and rep['decision']['tests_read'] is False and rep['validity']['C4T']['V4'] and rep['validity']['C4T']['V5'],
      rc=p.returncode, outcome=rep.get('decision', {}).get('outcome'), stderr=p.stderr[-300:])
    speeds = []
    for lab in ('C4R3',):
        speeds += list(REAL[lab]['rows'].values())
    c5r = json.loads(Path(CT + '/runs_ext/KMAX_A2F10_C5R3_RUN_V001/result.json').read_text())
    p = cli('VALIDITY_ONLY_C4T_C5H', '--validity-only', '--case', 'C4T', '--case', 'C5H')
    txt = (out / 'VALIDITY_ONLY_C4T_C5H' / 'VALIDITY_ONLY.json').read_text() if p.returncode == 0 else ''
    body = json.loads(txt) if txt else {}
    leaks = [x for x in speeds for fmt in ('%r', '%.6f', '%.5f', '%.4f', '%.3f', '%.2f', '%.6g', '%.4g') if (fmt % x) in txt or (fmt % x) in p.stdout]
    nums = []
    _find_numbers(body, '$', nums)
    t('A47_I3_VALIDITY_ONLY_HAS_NO_ROW_VALUE_AND_NO_NUMBER', p.returncode == 0 and not leaks and not nums and body.get('blinded') is True
      and body['cases']['C5H']['reading'] == 'BRACKET_MISS_OFF_RA4_BLOCK' and body['cases']['C4T']['V1'] is True,
      leaks=leaks[:5], numbers=nums[:5], rc=p.returncode, stderr=p.stderr[-300:])
    p = cli('GATES_ONLY_REAL_PROBE', '--gates-only', '--no-packets')
    txt = (out / 'GATES_ONLY_REAL_PROBE' / 'GATES_ONLY.json').read_text() if p.returncode == 0 else ''
    nums = []
    _find_numbers(json.loads(txt) if txt else {}, '$', nums)
    t('RA13_GATES_ONLY_BLINDED', p.returncode == 0 and not nums and all(x['status'] == 'MISSING' for x in json.loads(txt)['gates'].values()),
      rc=p.returncode, numbers=nums[:5])
    p = subprocess.run([PY, '-I', '-B', str(CMP), '--prereg', M.PIN_DRAFT_R1[0], '--manifest', str(mp), '--case-block', str(cbp),
                        '--outdir', str(out / 'REFUSE_PIN')], capture_output=True, text=True)
    t('UNPINNED_PREREG_REFUSED_WITHOUT_TEST_FLAG', p.returncode == 2 and 'REFUSED' in p.stderr)
    man2 = dict(man, cases=dict(man['cases'], C9T='/x'))
    (out / 'MANIFEST_BAD.json').write_text(json.dumps(man2))
    p = subprocess.run([PY, '-I', '-B', str(CMP), '--prereg', M.PIN_DRAFT_R1[0], '--manifest', str(out / 'MANIFEST_BAD.json'), '--case-block', str(cbp),
                        '--outdir', str(out / 'REFUSE_LABEL'), '--test-allow-unpinned-prereg'], capture_output=True, text=True)
    t('UNKNOWN_CASE_LABEL_REFUSED', p.returncode == 2 and 'unknown cases' in p.stderr)
    cb3 = case_block('serial_with_exemption')
    (out / 'CB_SERIAL.json').write_text(json.dumps(cb3))
    p = subprocess.run([PY, '-I', '-B', str(CMP), '--prereg', M.PIN_DRAFT_R1[0], '--manifest', str(mp), '--case-block', str(out / 'CB_SERIAL.json'),
                        '--outdir', str(out / 'REFUSE_MODE'), '--route-a-mode', 'parallel8', '--test-allow-unpinned-prereg'], capture_output=True, text=True)
    t('A47_I4_ROUTE_A_MODE_SINGLE_PARAMETER_CONFLICT_REFUSED', p.returncode == 2 and 'route-A mode differs' in p.stderr)
    fp = out / 'FIELDS_TEST.md'
    M.write_field_contract(str(fp))
    t('FIELDS_MD_WRITTEN', fp.is_file() and all(g in fp.read_text() for g in M.ALL_GATES))
    # ================================================================ summary
    n_pass = sum(1 for x in TESTS if x['pass'])
    summary = {'schema': 'UNT_V007_COMPARE_TESTS_C2V001', 'script_sha256': hashlib.sha256(CMP.read_bytes()).hexdigest(),
               'tests_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'n': len(TESTS), 'n_pass': n_pass,
               'n_fail': len(TESTS) - n_pass, 'tests': TESTS}
    (out / 'TEST_SUMMARY.json').write_text(json.dumps(summary, indent=1))
    for x in TESTS:
        print('%s %s %s' % ('PASS' if x['pass'] else 'FAIL', x['test'], '' if x['pass'] else json.dumps(x)[:600]))
    print('%d/%d pass' % (n_pass, len(TESTS)))
    return 0 if n_pass == len(TESTS) else 1


def _pat(doc_path):
    p = doc_path.split('[]')[0]
    p = re.sub(r'\{([^}]*)\}', lambda m: '(' + '|'.join(re.escape(x) for x in m.group(1).split(',')) + ')', p)
    return re.sub(r'<[^>]+>', '[^/]+', p)


def _leaf_paths(g, r):
    """(deletion path, expected code substring) for every key of the record: dict keys recursively; for lists of dicts, every
    key of the first element."""
    out = []

    def walk(o, path, where_list):
        if isinstance(o, dict):
            for k, v in o.items():
                p = path + [k]
                if where_list is None:
                    out.append((p, 'FIELD_MISSING:%s:%s' % (g, '/'.join(p))))
                else:
                    lp, j, inner = where_list
                    out.append((p, 'FIELD_MISSING:%s:%s[%d]:%s' % (g, '/'.join(lp), j, '/'.join(p[len(lp) + 1:]))))
                if isinstance(v, dict) and k not in ('maps',) and where_list is None:
                    walk(v, p, None)
                elif isinstance(v, list) and v and isinstance(v[0], dict) and where_list is None:
                    walk(v[0], p + [0], (p, 0, True))
    walk(r, [], None)
    return out


def _delete(o, path):
    for k in path[:-1]:
        o = o[k]
    del o[path[-1]]


def _find_numbers(o, where, acc):
    if isinstance(o, bool) or o is None or isinstance(o, str):
        return
    if isinstance(o, (int, float)):
        acc.append(where)
        return
    if isinstance(o, dict):
        for k, v in o.items():
            _find_numbers(v, where + '.' + str(k), acc)
    elif isinstance(o, list):
        for j, v in enumerate(o):
            _find_numbers(v, '%s[%d]' % (where, j), acc)


if __name__ == '__main__':
    sys.exit(main())
