"""Operator evaluation of prep v009 at the extension grids (no route-A iteration, no column solve, no stage launch):
prepare_inputs(**seed.numerical_inputs) on the per-call seed the c2v009 dry run wrote for C5/C6 (dryrun_m16/.../seed_c2v001.json),
with the A2 pooled coefficient patch the driver applies, then ONE iteration-0 prepare through the pinned lapse-inverse cache
facade (the base unit solve), exactly the solver's first prepare.  Records: wall time and process peak RSS of each phase;
axis checks (unique axis values equal the composite Gauss-Legendre formula; every G4 axis value is present bitwise;
weight sum vs (2 kmax)^3); and the digests (checkpoint-module digest) of every IDENTITY.inputs_sha256 entry and of the
iteration-0 START arrays, i.e. the values the C5/C6 route-A checkpoint must carry (post-run check).
usage: python3 -I -B prep_v009_smoke_c2ext.py SEED_JSON OUT_DIR"""
import hashlib
import importlib.util
import json
import resource
import sys
import time
from pathlib import Path

HERE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6')
sys.path.insert(0, str(HERE / 'tools'))
import prep_v009_repro_c2ext as RP  # noqa: E402  (same pins and loaders)

COEFF = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/'
         'CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz',
         '2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7')
KPC = 3.085677581491367e19
G4B = [-4, -3, -2, -1, -0.3, -0.1, -0.03, -0.01, 0, 0.01, 0.03, 0.1, 0.3, 1, 2, 3, 4]


def rss_gib():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 ** 3  # macOS: bytes


def axis_of(breaks, orders, np):
    parts = []
    for lo, hi, n in zip(breaks[:-1], breaks[1:], orders):
        x, _ = np.polynomial.legendre.leggauss(n)
        parts.append(((lo + hi) / 2 + (hi - lo) * x / 2) / KPC)
    return np.concatenate(parts)


def main():
    seed_p, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=False)
    t0 = time.time()
    seed = json.loads(seed_p.read_text())
    ni = seed['numerical_inputs']
    cm = RP.load('checkpoint', *RP.PINS['checkpoint'])
    solver = RP.load('solver', *RP.PINS['solver'])
    stream = RP.load('stream', *RP.PINS['stream'])
    base = RP.load('base', *RP.PINS['base'])
    prep = RP.load('prep_v009', RP.PREP_V009, RP.PREP_V009_SHA)
    if RP.sha_file(COEFF[0]) != COEFF[1]:
        raise SystemExit('coefficient pin')
    prep.COEFFICIENT, prep.COEFFICIENT_SHA = Path(COEFF[0]), COEFF[1]
    np = solver.np
    rep = {'schema': 'UNT_PREP_V009_SMOKE_C2EXT_V001', 'seed': {'path': str(seed_p), 'sha256': RP.sha_file(seed_p)},
           'grid': ni['composite_grid_spec'], 'fourier_points_per_axis': ni['fourier_points_per_axis'], 'max_iterations': ni['max_iterations'],
           'prep_v009_sha256': RP.PREP_V009_SHA}
    data = prep.prepare_inputs(**ni)
    rep['t_prepare_inputs_s'] = round(time.time() - t0, 1)
    rep['peak_rss_after_prepare_inputs_GiB'] = round(rss_gib(), 3)
    fa = data['fourier_arguments']
    k = fa['k_physical']
    g = ni['composite_grid_spec']
    ax = axis_of(g['breaks_inverse_kpc'], g['panel_orders'], np)
    uniq = [np.unique(k[:, i]) for i in range(3)]
    ax4 = axis_of(G4B, [6] * 16, np)
    rep['axis_checks'] = {'nodes': int(len(k)), 'expected_nodes': int(len(ax) ** 3),
                          'unique_axis_equals_formula': all(len(u) == len(ax) and np.array_equal(u, np.sort(ax)) for u in uniq),
                          'G4_axis_values_present_bitwise': bool(np.all(np.isin(ax4, ax))),
                          'weight_sum_rel_error': float(abs(data['quadrature_weight_sum'] / data['quadrature_weight_sum_expected'] - 1))}
    fixed = solver._supplied_fixed_source(data['fixed_source_fourier_J'], len(k))
    gas = np.asarray(data['initial_gas_fourier_J'], dtype=complex)
    rep['expected_identity_inputs_sha256'] = {
        'fixed_positions_m': cm.digest(data['fixed_positions_m']), 'fixed_integrated_columns_J': cm.digest(data['fixed_integrated_columns_J']),
        'initial_gas_fourier_J': cm.digest(gas), 'fixed_source_fourier_J': cm.digest(fixed), 'gas_columns': cm.digest(data['gas_columns']),
        'fourier_arguments': {kk: cm.digest(v) for kk, v in sorted(fa.items())}}
    t1 = time.time()
    facade = stream.make_fourier_module(base_module=base, log_directory=out / 'node_diagnostics', start_iteration=0)
    current = fixed + gas
    prepared = facade.prepare(**dict(fa), source_density_fourier=current)
    rep['t_iteration0_prepare_s'] = round(time.time() - t1, 1)
    rep['peak_rss_after_iteration0_prepare_GiB'] = round(rss_gib(), 3)
    rep['expected_start_iteration_0000'] = {
        'gas_fourier_J': cm.digest(gas), 'current_source_fourier_J': cm.digest(current), 'fixed_source_fourier_J': cm.digest(fixed),
        'prepared_wavevectors': cm.digest(prepared['wavevectors']), 'prepared_weighted_responses': cm.digest(prepared['weighted_responses']),
        'prepared_metric_response_sha256': cm.digest(prepared)}
    rep['node_diagnostics_iteration0_sha256'] = {nm: RP.sha_file(out / 'node_diagnostics' / nm)
                                                 for nm in ('iteration_000000_nodes.jsonl', 'iteration_000000_scaled_nodes.jsonl')}
    rep['elapsed_s'] = round(time.time() - t0, 1)
    rep['verdict'] = 'PASS' if (rep['axis_checks']['unique_axis_equals_formula'] and rep['axis_checks']['G4_axis_values_present_bitwise']
                                and rep['axis_checks']['nodes'] == rep['axis_checks']['expected_nodes']
                                and rep['axis_checks']['weight_sum_rel_error'] < 1e-12) else 'FAIL'
    with open(out / 'PREP_V009_SMOKE.json', 'x') as f:
        json.dump(rep, f, indent=1, sort_keys=True)
    print(json.dumps({k_: rep[k_] for k_ in ('verdict', 'axis_checks', 't_prepare_inputs_s', 't_iteration0_prepare_s',
                                             'peak_rss_after_prepare_inputs_GiB', 'peak_rss_after_iteration0_prepare_GiB', 'elapsed_s')}))


if __name__ == '__main__':
    main()
