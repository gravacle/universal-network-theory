"""One-process, target-free build and synthetic/saved-metadata checks; no launches."""
import ast
import copy
import hashlib
import importlib.util
import json
import resource
import sys
import time
from pathlib import Path
from types import SimpleNamespace

OUT = Path(__file__).parent
BASE = OUT.parent
EX = BASE.parent
PROGRAM = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL')
DRIVER = BASE/'tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py'
PARENT = BASE/'stage_successor_gal_c2v005/driver/galaxy_m0_forward_c2v009.py'
SEED = BASE/'ngc_route_a_freeboundary_c2/seed_v002/DEFAULT/seed/NGC3198_ROUTE_A_A2F10_SEED_C2V002_DEFAULT.json'
BT = BASE/'ngc_route_a_freeboundary_c2/seed_v002/DEFAULT/route_b_spec/CALL_NGC3198_ROUTE_B_A2F10_PAR_TEMPLATE_C2V006.json'
NT = BASE/'tail_scheme_impl_c2/driver/specs/NGC3198_T120L_TAIL_ITER0_NTEST_REQUEST_C2V001.TEMPLATE.json'
PREREG = BASE/'ngc_kgrid_fidelity_c2/PREREG_KGRID_FIDELITY_V001.json'
R1 = BASE/'tail_scheme_design_c2/v002/r1/KMAX_TAIL_PREREG_V007_DRAFT_R1.json'
DEC = PROGRAM/'FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'


def module(path, name):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


T = module(OUT/'ngc_readiness_tools_v001.py', 'cx3_readiness')
inputs = {}


def read(path):
    inputs[str(path)] = T.sha(path)
    return json.loads(path.read_text())


def record_input(path):
    inputs[str(path)] = T.sha(path)


def main():
    # Address-space limit 7 GiB; numpy and all BLAS libraries remain single-thread.
    resource.setrlimit(resource.RLIMIT_AS, (7 * 1024**3, 7 * 1024**3))
    for p in (DRIVER, PARENT, OUT/'ngc_readiness_tools_v001.py', Path(__file__)):
        record_input(p)
    if inputs[str(DRIVER)] != 'b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b':
        raise ValueError('DRIVER_PIN_MISMATCH')
    d, parent = module(DRIVER, 'driver_readiness'), module(PARENT, 'parent_readiness')
    seed, bt, nt, prereg, r1 = map(read, (SEED, BT, NT, PREREG, R1))
    for version in ('V002', 'V003', 'V004', 'V005'):
        record_input(DEC/f'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_{version}_ADDENDUM.md')
    for rel in ('tail_scheme_impl_c2/driver_r4/BUILD_TEST_DRIVER_R4.md',
                'tail_scheme_design_c2/v002/TAIL_SCHEME_DESIGN_V002.md',
                'tail_scheme_design_c2/v002/r1/TAIL_SCHEME_DESIGN_V002_R1.md',
                'ngc_kgrid_fidelity_c2/prep_successor/OPTION_B_TRUNCATION_PLAN_V001.md',
                'ngc_freeze_inputs_c3/NGC3198_FREEZE_SLOTS_C3V002.json',
                'ngc_route_a_freeboundary_c2/DIAGNOSIS_V001.json',
                'absorb_c2_0473/ngc_route_a/NGC_ROUTE_A_V002_REVIEW_V001.md'):
        record_input(BASE/rel)
    grid = next(c for c in prereg['candidates'] if c['id'] == 'T120L')
    assert grid['nodes_per_axis'] == [120, 120, 80] and grid['wave_count_W'] == 1152000
    uv = nt['uv_tail']
    assert uv['outer'] == r1['ngc3198_N_tests']['tail']['quadrature']['outer']
    d.normalize_uv_tail(uv, ngc=True)
    results = []
    def check(name, condition):
        results.append({'name': name, 'pass': bool(condition), 'label': 'TESTED'})
        if not condition:
            raise AssertionError(name)

    check('R1_tail_config_normalizes', True)
    # This is a desired interface contract, deliberately not mislabelled an
    # executable driver spec: r4 has no anisotropic grid or truncation hook.
    a_contract = {
        'schema': 'NGC_ROUTE_A_TAIL_READINESS_CONTRACT_CX3V001', 'launch_authority': 'Claude2 only',
        'executable': False, 'status': 'BLOCKED_PRODUCER_SUCCESSOR_REQUIRED',
        'driver': {'path': str(DRIVER), 'sha256': inputs[str(DRIVER)]},
        'base_seed': {'path': str(SEED), 'sha256': inputs[str(SEED)]},
        'physical_example_only_not_admitted': bt['physical'],
        'coefficients': bt['coefficients'], 'grid': grid,
        'kept_region': {'shape': 'cube', 'K_inverse_kpc': 2}, 'uv_tail': uv,
        'ro1': {'armed_required': True, 'worker': [str(d.NGC_CODE_UVT['worker'][0]), d.NGC_CODE_UVT['worker'][1]],
                'binding': [str(d.NGC_CODE_UVT['binding'][0]), d.NGC_CODE_UVT['binding'][1]]},
        'ngc_code_lineage_swap': {k: [str(v[0]), v[1]] for k,v in d.NGC_CODE_UVT.items()},
        'truncation': {'rule': 'A14_C3_A12_5', 'cut': 'PENDING_CURRENT_TAIL_POINT_CONFINEMENT',
                       'implementation': 'ngc_readiness_tools_v001.truncate_roster; standalone, NOT wired to prep',
                       'drop': 'all columns R >= first certified unconfined radius; original weights retained',
                       'invalidate_queries': 'R > first certified unconfined radius; speed=null',
                       'required_rebuild': 'gas source, source transforms and checkpoint identity; then recheck confinement'},
        'certificate_slots': {k: 'PENDING' for k in ('EPS_NGC', 'LO_NGC', 'GQ_NGC', 'I1T_NGC', 'NQ', 'N_PASS', 'V007_ADOPTION')},
        'resource_cap': {'processes_for_this_account': 2, 'rss_bytes_per_process_less_than': 8_000_000_000,
                         'blas_threads': 1, 'no_launch': True},
    }
    T.write_x(OUT/'ROUTE_A_TAIL_CONTRACT_V001.json', a_contract)
    b_tail = copy.deepcopy(bt)
    b_tail['label'] = 'READINESS ONLY: NGC route B v010 tail; r4 expected refusal; no launch'
    b_tail['numerics']['uv_tail'] = uv
    T.write_x(OUT/'ROUTE_B_TAIL_ATTEMPT_V001.json', b_tail)
    attempts = {}
    try:
        d.cmd_dry_run(OUT/'ROUTE_B_TAIL_ATTEMPT_V001.json', OUT/'dryrun_route_b_tail_v001')
        attempts['route_b_tail'] = {'refusal': None}
    except Exception as e:
        attempts['route_b_tail'] = {'exception': type(e).__name__, 'refusal': str(e),
                                    'nonempty_expected_report': (OUT/'dryrun_route_b_tail_v001/DRYRUN_REPORT.json').is_file()}
    check('route_B_actual_dry_run_rejects_tail_key', "uv_tail" in attempts['route_b_tail'].get('refusal', ''))
    a = {'schema': d.NGC_SCHEMA, 'galaxy': 'NGC3198',
         'physical': {k: v for k,v in bt['physical'].items() if k != 'entropy_K_factor'},
         'numerics': {'composite_grid_spec': seed['numerical_inputs']['composite_grid_spec'],
                      'k_domain': {'length_kpc': 300.}, 'h2_tail_mass_rtol': 1e-12, 'uv_tail': uv}}
    for label, update in [('a2_coefficients', {'coefficients': bt['coefficients']}),
                          ('anisotropic_T120L', {})]:
        probe = copy.deepcopy(a); probe.update(update)
        if label == 'anisotropic_T120L':
            # A true anisotropic spec cannot be represented by the r4 single-
            # axis schema. Probe the required transverse axis, which fails even
            # before reaching that missing kz distinction. Do not call it T120L.
            ax = grid['transverse_axis_kx_ky']
            probe['numerics']['composite_grid_spec'] = {
                'version': 'T120L_TRANSVERSE_AXIS_ONLY_NOT_THE_FULL_GRID',
                'breaks_inverse_kpc': ax['breaks_inverse_kpc'], 'panel_orders': ax['panel_orders'],
                'total_axis_nodes': 120, 'scope': 'Refusal probe only; full T120L uses 120x120x80'}
        spath = OUT/f'ROUTE_A_REFUSAL_PROBE_{label}_V001.json'; T.write_x(spath, probe)
        try:
            d.cmd_dry_run(spath, OUT/f'dryrun_{label}_v001')
            attempts[label] = {'refusal': None}
        except Exception as e:
            attempts[label] = {'exception': type(e).__name__, 'refusal': str(e),
                               'nonempty_expected_report': (OUT/f'dryrun_{label}_v001/DRYRUN_REPORT.json').is_file()}
    check('route_A_A2_default_coefficient_refusal', 'default coefficient' in attempts['a2_coefficients']['refusal'])
    check('route_A_transverse_120_axis_refusal', '<=80' in attempts['anisotropic_T120L']['refusal'])
    T.write_x(OUT/'ACTUAL_DRIVER_DRYRUN_REFUSALS_V001.json', {
        'label': 'TESTED', 'driver_sha256': inputs[str(DRIVER)], 'attempts': attempts,
        'stages_executed': 0, 'zero_blocker_dryrun_achieved': False,
        'warning': 'Equal early refusals/empty report directories are not plan identity or readiness evidence.'})
    columns = [{'id': str(i), 'R_kpc': r, 'HI_mass_kg': m,
                'confinement': 'CERTIFIED_UNCONFINED' if i == 3 else 'CONFINED'}
               for i,(r,m) in enumerate([(1.,1.), (1.,1.), (2.,2.), (2.,2.), (3.,4.)])]
    queries = [{'id': f'Q{i}', 'radius_kpc': r, 'valid': True, 'speed_km_s': 10.}
               for i,r in enumerate([1.,2.,2.1,3.])]
    cut = T.truncate_roster(columns, queries)
    check('cut_drops_entire_first_unconfined_ring_and_exterior', [c['id'] for c in cut['kept_columns']] == ['0','1'])
    check('cut_mass_counts_all_dropped_not_only_unconfined', cut['dropped_HI_mass_fraction'] == .8)
    check('beyond_cut_INVALID_null', all(r['valid'] is False and r['speed_km_s'] is None for r in cut['query_rows'][2:]))
    check('cut_equality_follows_literal_beyond_rule', cut['query_rows'][1]['valid'] is True)
    check('cut_order_independent', T.truncate_roster(list(reversed(columns)), queries)['dropped_HI_mass_fraction'] == .8)
    no_cut = copy.deepcopy(columns)
    for c in no_cut: c['confinement'] = 'CONFINED'
    check('all_confined_no_cut', T.truncate_roster(no_cut, queries)['dropped_HI_mass_fraction'] == 0)
    undecided = copy.deepcopy(columns); undecided[0]['confinement'] = 'BRACKET_MISS'
    try: T.truncate_roster(undecided, queries)
    except ValueError: check('numerical_failure_not_unconfinement', True)
    else: check('numerical_failure_not_unconfinement', False)
    T.write_x(OUT/'SYNTHETIC_TRUNCATION_RESULT_V001.json', cut)

    # Replay only the actual result-assembly AST block of each pinned driver on
    # synthetic final-stage output. No driver run or execute_chain invocation.
    def assembly(mod, path, final):
        tree = ast.parse(path.read_text())
        run = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'cmd_run')
        block = next(n for n in ast.walk(run) if isinstance(n, ast.If) and ast.unparse(n.test) == 'final is None')
        nspec = {'physical': {'entropy_K_member': 'N4_PRIMARY_64_OVER_121'}, 'numerics': {'picard': {'speed_change_bound_km_s': .01}}}
        result = {'schema': mod.RESULT_SCHEMA, 'galaxy': 'NGC3198', 'valid': False, 'reasons': [],
                  'normalized_spec': nspec, 'passes': [copy.deepcopy(final)]}
        env = {'result': result, 'final': final, 'nspec': nspec, 'g': {'n_queries': 43},
               'ctx': SimpleNamespace(passes=result['passes']), 'final_rows_check': mod.final_rows_check,
               'harmonic_diagnostic': mod.harmonic_diagnostic}
        exec(compile(ast.Module(body=[block], type_ignores=[]), str(path)+':assembly_only', 'exec'), env)
        result['status'] = 'COMPLETED' if result['valid'] else 'COMPLETED_INVALID'
        return result
    rows = [{'id': f'NGC3198-Q{i:02d}', 'radius_kpc': i * .5, 'speed_km_s': 20.+i, 'valid': True} for i in range(1,44)]
    final = {'pass': 1, 'rows': rows, 'column_failures': [], 'rotation_positive': True,
             'column_mean': {'status': 'CONDITIONAL_PREPARATION_ROWS_NOT_CALIBRATION'},
             'max_abs_change_km_s': .005, 'nonaxisymmetric_residual_maxima': {'synthetic': 0.}, 'residual_units': 'synthetic'}
    old, new = assembly(parent, PARENT, copy.deepcopy(final)), assembly(d, DRIVER, copy.deepcopy(final))
    new['route_a_outcome'] = {'ro1': {'armed': False, 'fired': False}}
    c = T.compare_ngc_results(old, new)
    check('v009_v010_real_AST_synthetic_assembly_equal', c['verdict'] == 'PASS_RESULT_ASSEMBLY_EQUAL')
    T.write_x(OUT/'SYNTHETIC_V009_RESULT_V001.json', old)
    T.write_x(OUT/'SYNTHETIC_V010_RESULT_V001.json', new)
    for name, mutate in [
        ('speed_tamper', lambda x: x['rows'][5].update(speed_km_s=999.)),
        ('missing_row', lambda x: x['rows'].pop()),
        ('row_reorder', lambda x: x['rows'].reverse()),
        ('invalid_with_finite_speed', lambda x: x['rows'][5].update(valid=False)),
        ('stray_tail_off', lambda x: x.update(uv_tail={'domain_empty_all_stages': True})),
        ('ro1_fired', lambda x: x['route_a_outcome']['ro1'].update(fired=True)),
    ]:
        bad = copy.deepcopy(new); mutate(bad)
        check('comparator_refuses_'+name, T.compare_ngc_results(old, bad)['verdict'] == 'FAIL')
    empty = copy.deepcopy(new); empty['uv_tail'] = {'domain_empty_all_stages': True, 'stage_records': [{'empty': True}]}
    check('explicit_empty_tail_identity', T.compare_ngc_results(old, empty, 'EMPTY_TAIL_IDENTITY')['verdict'] == 'PASS_RESULT_ASSEMBLY_EQUAL')
    empty['uv_tail']['stage_records'][0]['empty'] = False
    check('nonempty_tail_cannot_claim_parent_identity', T.compare_ngc_results(old, empty, 'EMPTY_TAIL_IDENTITY')['verdict'] == 'FAIL')
    import numpy as np
    for name, value in [('a', 1.), ('b', 1.), ('tamper', 2.)]:
        with (OUT/f'SYNTHETIC_STAGE_{name}_V001.npz').open('xb') as f:
            np.savez(f, R=np.array([1.,2.]), velocity=np.array([value,3.]))
    check('stage_arrays_equal', T.compare_stage_arrays(OUT/'SYNTHETIC_STAGE_a_V001.npz', OUT/'SYNTHETIC_STAGE_b_V001.npz'))
    check('stage_array_tamper_rejected', not T.compare_stage_arrays(OUT/'SYNTHETIC_STAGE_a_V001.npz', OUT/'SYNTHETIC_STAGE_tamper_V001.npz'))
    T.write_x(OUT/'TEST_RESULTS_V001.json', {'label':'TESTED', 'checks': results,
        'passed': sum(x['pass'] for x in results), 'total': len(results), 'actual_driver_runs': 0,
        'scope': 'Driver early dry-run refusals; real result-assembly AST on synthetic final stage; pure truncation and comparator tests.',
        'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
    T.write_x(OUT/'INPUT_HASHES_V001.json', {'sha256_from_bytes': inputs,
        'V005_note': 'Open addendum hash is an observed snapshot, not a frozen execution pin.'})
    print(json.dumps({'passed':len(results), 'total':len(results), 'refusals':attempts}))


if __name__ == '__main__':
    main()
