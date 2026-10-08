"""Prospective DESI DR2 shape census. Stdout only; freeze before run."""
import sys
sys.dont_write_bytecode = True
import functools
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.resolve()
FREEZE = HERE / 'DESI_BAO_SHAPE_V001_FROZEN.json'
DATA = 'desi_dr2_bao_external_v001/'
PINS = {
    DATA + 'desi_gaussian_bao_ALL_GCcomb_mean.txt':
        '9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585',
    DATA + 'desi_gaussian_bao_ALL_GCcomb_cov.txt':
        '252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509',
    DATA + 'README.md':
        '5f21b88b1a6d6264174f7ecd2b1e0baf78a62c9feb467c5fe3865eb3ba9b70f6',
    'DESI_BAO_OUT_OF_CALIBRATION_PRESELECTION_V001.md':
        '6082e4cd11a3b615f5862218455f20482d6548a04ef12a80c0307fd96df08513',
    'COSMOLOGY_CLOSURE_ARITHMETIC.json':
        '258097f5a80c8cfb4891d93e02a1f6224eb54b73014c276683f05c8b3989f153',
    'HARD_LIMIT_NONVACUUM_SCALAR_INTERFACE_V001.md':
        'c501fc2aeebe0cf389ad9c21c5c7fdd3240209a1d9dd0ae710ed45d67bb8003d',
    'HARD_LIMIT_DUST_INTERFACE_WITH_ORDINARY_RADIATION_V001.md':
        '41111a6ed3d0e69114ad36c19d1790e11a57fb2195d395aea88259b67083d522',
    'PAIRED_HARD_MODE_STATE_V001.md':
        '7461324e5c40de23f796c9e438a9d1cbecd88ffcc9bdb2c21c8e05fd54a38c91',
}
ORDER = [(0.295, 'DV_over_rs'), (0.510, 'DM_over_rs'),
    (0.510, 'DH_over_rs'), (0.706, 'DM_over_rs'), (0.706, 'DH_over_rs'),
    (0.934, 'DM_over_rs'), (0.934, 'DH_over_rs'), (1.321, 'DM_over_rs'),
    (1.321, 'DH_over_rs'), (1.484, 'DM_over_rs'), (1.484, 'DH_over_rs'),
    (2.33, 'DH_over_rs'), (2.33, 'DM_over_rs')]
CONFIG = dict(expected_rows=13, expected_references=18,
    gauss_order=96, gauss_check_order=48, simpson_intervals=2048,
    comparator_grids=[257, 513], golden_iterations=80,
    omega_m_bounds=[0., 1.], synthetic_omega_m=.27, synthetic_A=42.,
    quadrature_relative_tolerance=2e-11, gauss_relative_tolerance=2e-12,
    identity_tolerance=2e-12, score_absolute_tolerance=2e-8,
    grid_score_tolerance=2e-8, grid_omega_tolerance=1e-6,
    grid_A_relative_tolerance=1e-6, covariance_tolerance=2e-12,
    temperature_K=2.72548, temperature_error_K=.00057,
    illustrative_Neff=[0., 3.046], c_m_s=299792458.,
    G_SI=6.67430e-11, planck_h_J_s=6.62607015e-34,
    boltzmann_J_K=1.380649e-23, mpc_m=3.085677581491367e22,
    output_target_bytes=1048576)


def encode(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(path):
    path = path.resolve(strict=True)
    path.relative_to(ROOT)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def authenticate():
    files, seen = {}, set()

    def add(path, expected=None):
        path = path.resolve(strict=True)
        value = sha(path)
        if expected is not None and value != expected:
            raise RuntimeError('Input identity differs: ' + str(path))
        files[str(path.relative_to(ROOT))] = value
        return path

    def resolve(name, parent):
        name = Path(name)
        candidates = {name.resolve()} if name.is_absolute() else {
            (base / name).resolve() for base in (parent, ROOT, HERE.parent)}
        valid = []
        for candidate in candidates:
            try:
                candidate.relative_to(ROOT)
            except ValueError:
                continue
            if candidate.is_file():
                valid.append(candidate)
        if len(valid) != 1:
            raise RuntimeError('Missing/ambiguous frozen path: ' + str(name))
        return valid[0]

    def manifest(path):
        path = add(path)
        if path in seen:
            return
        seen.add(path)
        for name, expected in json.loads(path.read_text())['files'].items():
            member = add(resolve(name, path.parent), expected)
            if member.name.endswith('_FROZEN.json'):
                manifest(member)

    for name, expected in PINS.items():
        add(HERE / name, expected)
    closure = json.loads((HERE / 'COSMOLOGY_CLOSURE_ARITHMETIC.json').read_text())
    if closure['status'] != 'AUTHENTICATED_REFERENCE_CLOSURE_DIAGNOSTIC':
        raise RuntimeError('Reference status differs')
    if len(closure['rows']) != CONFIG['expected_references']:
        raise RuntimeError('Reference census differs')
    add(HERE / 'cosmology_closure_arithmetic.py', closure['script_sha256'])
    for name, expected in closure['input_sha256'].items():
        member = add(HERE.parent / name, expected)
        if member.name.endswith('_FROZEN.json'):
            manifest(member)
    add(Path(__file__))
    add(HERE / 'DESI_BAO_SHAPE_PROTOCOL_V001.md')
    return dict(configuration=CONFIG, files=files, expected_data_order=ORDER,
                scope='All18 fixed reference alternatives; not18 independent data sets'), closure


class Checks:
    def __init__(self):
        self.count = 0
        self.failed = []
        self.max_errors = {}

    def test(self, name, ok, error=None, category=None):
        self.count += 1
        if error is not None:
            key = category or name
            self.max_errors[key] = max(self.max_errors.get(key, 0.), float(error))
        if not bool(ok):
            self.failed.append(name)

    def close(self, name, a, b, tol, relative=False, category=None):
        aa, bb = np.asarray(a, float), np.asarray(b, float)
        err = float(np.max(np.abs(aa - bb)))
        if relative:
            err = float(np.max(np.abs(aa - bb) / np.maximum(np.abs(bb), 1e-100)))
        self.test(name, math.isfinite(err) and err <= tol, err, category)

    def payload(self):
        return dict(total=self.count, failed=len(self.failed),
                    failure_names=self.failed, maximum_errors=self.max_errors)


@functools.lru_cache(None)
def gauss(order):
    return np.polynomial.legendre.leggauss(order)


def expansion_squared(z, om, radiation=0., split=None):
    y = 1. + np.asarray(z, float)
    dust = om * y**3 if split is None else split[0] * y**3 + split[1] * y**3
    return dust + (1. - om) + radiation * y**4


def shape(om, z, labels, method='gauss', order=None, radiation=0., split=None):
    z = np.asarray(z, float)
    if method == 'gauss':
        nodes, weights = gauss(order or CONFIG['gauss_order'])
        zz = z[:, None] * (nodes[None, :] + 1.) / 2.
        dm = z * np.sum(weights[None, :] /
            np.sqrt(expansion_squared(zz, om, radiation, split)), axis=1) / 2.
    elif method == 'simpson':
        n = CONFIG['simpson_intervals']
        nodes = np.arange(n + 1, dtype=float) / n
        weights = np.ones(n + 1)
        weights[1:-1:2] = 4.
        weights[2:-1:2] = 2.
        zz = z[:, None] * nodes[None, :]
        dm = z * np.sum(weights[None, :] /
            np.sqrt(expansion_squared(zz, om, radiation, split)), axis=1) / (3. * n)
    else:
        raise ValueError('Unknown method')
    dh = 1. / np.sqrt(expansion_squared(z, om, radiation, split))
    dv = np.cbrt(z * dm * dm * dh)
    lookup = {'DM_over_rs': dm, 'DH_over_rs': dh, 'DV_over_rs': dv}
    return np.array([lookup[label][i] for i, label in enumerate(labels)])


def profile_amplitude(d, y, chol):
    dw, yw = np.linalg.solve(chol, d), np.linalg.solve(chol, y)
    denom, numer = float(dw @ dw), float(dw @ yw)
    if not denom > 0.:
        raise RuntimeError('Nonpositive amplitude denominator')
    raw = numer / denom
    amplitude = max(0., raw)
    residual = y - amplitude * d
    whitened = np.linalg.solve(chol, residual)
    return dict(A=amplitude, A_unconstrained=raw, boundary_active=(raw <= 0.),
        chi2=float(whitened @ whitened), prediction=(amplitude * d).tolist(),
        residual=residual.tolist(), whitened_residual=whitened.tolist(),
        amplitude_gradient=2. * (amplitude * denom - numer),
        amplitude_hessian=2. * denom,
        H0_rd_km_s=CONFIG['c_m_s'] / 1000. / amplitude if amplitude > 0. else None)


def golden(fun, left, right):
    ratio = (math.sqrt(5.) - 1.) / 2.
    a, b = left, right
    c, d = b - ratio * (b - a), a + ratio * (b - a)
    fc, fd = fun(c), fun(d)
    for _ in range(CONFIG['golden_iterations']):
        if fc <= fd:
            b, d, fd = d, c, fc
            c = b - ratio * (b - a)
            fc = fun(c)
        else:
            a, c, fc = c, d, fd
            d = a + ratio * (b - a)
            fd = fun(d)
    choices = [(a, fun(a)), (b, fun(b)), (c, fc), (d, fd)]
    return min(choices, key=lambda pair: (pair[1], pair[0]))[0]


def shape_profile(grid_count, z, labels, y, chol, checks):
    grid = np.linspace(*CONFIG['omega_m_bounds'], grid_count)
    fits = []
    for i, om in enumerate(grid):
        d = shape(float(om), z, labels)
        dc = shape(float(om), z, labels, order=CONFIG['gauss_check_order'])
        checks.close(f'profile_{grid_count}_{i}_gauss', d, dc,
            CONFIG['gauss_relative_tolerance'], True, 'profile_gauss_relative')
        fits.append(profile_amplitude(d, y, chol))
    values = [f['chi2'] for f in fits]
    local = [i for i in range(1, grid_count - 1)
             if values[i] <= values[i-1] and values[i] <= values[i+1]]

    def objective(om):
        return profile_amplitude(shape(om, z, labels), y, chol)['chi2']

    candidates = []
    for label, om in [('finite_left_endpoint', 0.), ('finite_right_endpoint', 1.)]:
        candidates.append(dict(kind=label, Omega_m=om,
            fit=profile_amplitude(shape(om, z, labels), y, chol)))
    imin = int(np.argmin(values))
    candidates.append(dict(kind='best_grid_point', index=imin,
        Omega_m=float(grid[imin]), fit=fits[imin]))
    for i in local:
        om = golden(objective, float(grid[i-1]), float(grid[i+1]))
        candidates.append(dict(kind='refined_sampled_local_minimum', index=i,
            bracket=[float(grid[i-1]), float(grid[i+1])], Omega_m=om,
            fit=profile_amplitude(shape(om, z, labels), y, chol)))
    best_index = min(range(len(candidates)),
        key=lambda i: (candidates[i]['fit']['chi2'], candidates[i]['Omega_m']))
    return dict(grid_count=grid_count, grid_Omega_m=grid.tolist(),
        grid_chi2=values, grid_A=[f['A'] for f in fits],
        sampled_local_minimum_indices=local, candidates=candidates,
        best_candidate_index=best_index, best=candidates[best_index])


def pair_diagnostics(z, labels, y, cov, prediction):
    result = []
    for zz in sorted(set(z)):
        indices = [i for i, value in enumerate(z) if value == zz]
        if len(indices) != 2:
            continue
        im = next(i for i in indices if labels[i] == 'DM_over_rs')
        ih = next(i for i in indices if labels[i] == 'DH_over_rs')
        cc = cov[np.ix_([im, ih], [im, ih])]
        grad = np.array([1. / y[ih], -y[im] / y[ih]**2])
        result.append(dict(z=float(zz), original_indices_DM_DH=[im, ih],
            covariance_DM_DH=cc.tolist(),
            correlation=float(cc[0, 1] / math.sqrt(cc[0, 0] * cc[1, 1])),
            AP_observed=float(y[im] / y[ih]),
            AP_delta_method_sigma=math.sqrt(float(grad @ cc @ grad)),
            AP_prediction=(float(prediction[im] / prediction[ih])
                           if prediction[ih] != 0. else None)))
    return result


def radiation_diagnostic(refs, z, labels, checks):
    cfg = CONFIG
    t0, err = cfg['temperature_K'], cfg['temperature_error_K']
    temperatures = [t0 - err, t0, t0 + err]
    rows = []
    for ref in refs:
        om, h0 = ref['Omega_m'], ref['H0_km_s_Mpc'] * 1000. / cfg['mpc_m']
        baseline = shape(om, z, labels)
        for temperature in temperatures:
            energy = 8. * math.pi**5 * cfg['boltzmann_J_K']**4 * temperature**4 / (
                15. * cfg['planck_h_J_s']**3 * cfg['c_m_s']**3)
            omega_gamma = 8. * math.pi * cfg['G_SI'] * energy / (
                3. * h0**2 * cfg['c_m_s']**2)
            for neff in cfg['illustrative_Neff']:
                factor = 1. + (7. / 8.) * (4. / 11.)**(4. / 3.) * neff
                wr = omega_gamma * factor
                changed = shape(om, z, labels, radiation=wr)
                independent = shape(om, z, labels, method='simpson', radiation=wr)
                checks.close('radiation_method', changed, independent,
                    cfg['quadrature_relative_tolerance'], True, 'radiation_method_relative')
                q = wr * (1. + z)**4 / expansion_squared(z, om)
                qmax = float(np.max(q))
                bound = -math.expm1(-.5 * math.log1p(qmax))
                difference = 1. - changed / baseline
                checks.test('radiation_decrease_bound',
                    bool(np.all(difference >= -cfg['identity_tolerance'])) and
                    float(np.max(difference)) <= bound + cfg['identity_tolerance'])
                rows.append(dict(reference=ref['reference'], temperature_K=temperature,
                    illustrative_Neff=neff, Omega_gamma=omega_gamma, Omega_rad=wr,
                    H_at_zero_over_inherited_H0=math.sqrt(1. + wr),
                    H_fractional_increase=(np.sqrt(1. + q) - 1.).tolist(),
                    distance_fractional_decrease=difference.tolist(),
                    all_z_distance_decrease_upper_bound=bound,
                    all_z_H_increase_upper_bound=math.sqrt(1. + qmax) - 1.))
    return dict(scope='Diagnostic only; no observational score/refit; physical dust and vacuum coefficients fixed',
        convention='E_rad^2=E_dust^2+Omega_rad*(1+z)^4, so inherited H0 is the dust-only normalization',
        neutrino_scope='Neff=3.046 is illustrative if all species massless; not a measured late-time neutrino density or a universal bound',
        temperatures_K=temperatures, rows=rows)


def run(closure):
    started = time.perf_counter()
    checks = Checks()
    raw = [line.split() for line in (HERE / DATA / 'desi_gaussian_bao_ALL_GCcomb_mean.txt').read_text().splitlines()
           if line.strip() and not line.lstrip().startswith('#')]
    order = [(float(row[0]), row[2]) for row in raw]
    if order != ORDER:
        raise RuntimeError('Data ordering differs from complete13-vector preselection')
    z = np.array([r[0] for r in order])
    labels = [r[1] for r in order]
    y = np.array([float(row[1]) for row in raw])
    cov = np.loadtxt(HERE / DATA / 'desi_gaussian_bao_ALL_GCcomb_cov.txt')
    if cov.shape != (13, 13) or not np.isfinite(cov).all() or not np.isfinite(y).all():
        raise RuntimeError('Covariance/data dimensions or finiteness differ')
    checks.close('covariance_symmetry', cov, cov.T, CONFIG['covariance_tolerance'])
    chol = np.linalg.cholesky(cov)
    eig = np.linalg.eigvalsh(cov)
    checks.test('covariance_positive_definite', eig[0] > 0.)
    checks.close('covariance_factorization', chol @ chol.T, cov, CONFIG['covariance_tolerance'])
    checks.test('data_positive', np.all(y > 0.) and np.all(z > 0.))
    checks.test('last_pair_DH_then_DM', labels[-2:] == ['DH_over_rs', 'DM_over_rs'])

    for om in (0., 1.):
        dm = z if om == 0. else 2. * (1. - 1. / np.sqrt(1. + z))
        dh = np.ones_like(z) if om == 0. else (1. + z)**(-1.5)
        dv = np.cbrt(z * dm**2 * dh)
        oracle = np.array([{'DM_over_rs': dm, 'DH_over_rs': dh, 'DV_over_rs': dv}[label][i]
                           for i, label in enumerate(labels)])
        checks.close('analytic_endpoint', shape(om, z, labels), oracle,
                     CONFIG['identity_tolerance'], True, 'endpoint_relative')

    synthetic = shape(CONFIG['synthetic_omega_m'], z, labels)
    fit_synthetic = profile_amplitude(synthetic, CONFIG['synthetic_A'] * synthetic, chol)
    checks.close('synthetic_A_recovery', fit_synthetic['A'], CONFIG['synthetic_A'],
                 CONFIG['identity_tolerance'], True)
    checks.test('synthetic_zero_residual', fit_synthetic['chi2'] < 1e-18)
    boundary = profile_amplitude(synthetic, -synthetic, chol)
    checks.test('synthetic_boundary', boundary['A'] == 0. and boundary['boundary_active']
                and boundary['amplitude_gradient'] > 0.)

    refs, results = [], []
    for index, row in enumerate(closure['rows']):
        inp = row['reference_input']
        h0, ol = float(inp['H0_km_s_Mpc']), float(inp['Omega_Lambda_ref'])
        om = 1. - ol
        ob = float(row['bbn']['omega_b']) / (h0 / 100.)**2
        ox = float(row['reference_H0_missing_Omega'])
        if not (0. < om < 1. and ob > 0. and ox > 0.):
            raise RuntimeError('Inherited density domain differs')
        checks.close('reference_density_closure', ob + ox, om, CONFIG['identity_tolerance'])
        ref = dict(reference=index, reference_case=row['reference_case'],
            bbn=row['bbn'], reference_input=inp, H0_km_s_Mpc=h0,
            Omega_b=ob, Omega_exc=ox, Omega_m=om, Omega_Lambda=ol)
        refs.append(ref)
        d = shape(om, z, labels, split=(ob, ox))
        dc = shape(om, z, labels)
        dg = shape(om, z, labels, order=CONFIG['gauss_check_order'])
        ds = shape(om, z, labels, method='simpson')
        checks.close('same_parameter_network_comparator', d, dc,
                     CONFIG['identity_tolerance'], True, 'same_parameter_relative')
        checks.close('reference_gauss', d, dg, CONFIG['gauss_relative_tolerance'], True,
                     'reference_gauss_relative')
        checks.close('reference_simpson', d, ds, CONFIG['quadrature_relative_tolerance'], True,
                     'reference_simpson_relative')
        fit = profile_amplitude(d, y, chol)
        fit_s = profile_amplitude(ds, y, chol)
        checks.close('reference_score_method', fit['chi2'], fit_s['chi2'],
                     CONFIG['score_absolute_tolerance'], category='score_method_absolute')
        residual = np.array(fit['residual'])
        direct = np.linalg.solve(cov, residual)
        checks.close('direct_covariance_score', float(residual @ direct), fit['chi2'],
                     CONFIG['score_absolute_tolerance'], category='direct_score_absolute')
        direct_A = max(0., float(d @ np.linalg.solve(cov, y)) /
                       float(d @ np.linalg.solve(cov, d)))
        checks.close('direct_amplitude', direct_A, fit['A'],
                     CONFIG['identity_tolerance'], True, 'direct_A_relative')
        stationarity_tol = CONFIG['identity_tolerance'] * max(
            1., fit['amplitude_hessian'] * fit['A'])
        checks.test('amplitude_stationarity',
            fit['amplitude_gradient'] >= -stationarity_tol if fit['boundary_active'] else
            abs(fit['amplitude_gradient']) <= stationarity_tol)
        results.append(dict(reference=index, shape=d.tolist(), fit=fit,
            conditional_rd_Mpc=fit['H0_rd_km_s'] / h0 if fit['A'] > 0. else None,
            precision_controls=dict(gauss48_chi2=profile_amplitude(dg, y, chol)['chi2'],
                                    simpson2048_fit=fit_s),
            covariance_residual_contributions=(residual * direct).tolist(),
            pair_diagnostics=pair_diagnostics(z, labels, y, cov, fit['prediction'])))
    checks.test('complete_reference_census', len(results) == 18 and
                [r['reference'] for r in results] == list(range(18)))
    profiles = [shape_profile(n, z, labels, y, chol, checks)
                for n in CONFIG['comparator_grids']]
    b0, b1 = [p['best'] for p in profiles]
    checks.close('comparator_grid_chi2', b0['fit']['chi2'], b1['fit']['chi2'],
                 CONFIG['grid_score_tolerance'])
    checks.close('comparator_grid_Omega_m', b0['Omega_m'], b1['Omega_m'],
                 CONFIG['grid_omega_tolerance'])
    checks.close('comparator_grid_A', b0['fit']['A'], b1['fit']['A'],
                 CONFIG['grid_A_relative_tolerance'], True)
    for profile in profiles:
        for candidate in profile['candidates']:
            om = candidate['Omega_m']
            d = shape(om, z, labels)
            ds = shape(om, z, labels, method='simpson')
            checks.close('comparator_candidate_simpson', d, ds,
                CONFIG['quadrature_relative_tolerance'], True, 'candidate_simpson_relative')
            sf = profile_amplitude(ds, y, chol)
            checks.close('comparator_candidate_score_method', sf['chi2'], candidate['fit']['chi2'],
                CONFIG['score_absolute_tolerance'], category='candidate_score_absolute')
            candidate['simpson_fit'] = sf
    best = b1
    best['pair_diagnostics'] = pair_diagnostics(z, labels, y, cov, best['fit']['prediction'])
    for result in results:
        result['chi2_minus_extra_shape_fit'] = result['fit']['chi2'] - best['fit']['chi2']
    groups = {}
    for ref in refs:
        groups.setdefault(ref['Omega_m'].hex(), []).append(ref['reference'])
    rad = radiation_diagnostic(refs, z, labels, checks)
    elapsed = time.perf_counter() - started
    return dict(status='COMPLETE' if not checks.failed else 'FAILED_CHECKS',
        checks=checks.payload(), configuration=CONFIG,
        observational_scope='Out-of-calibration, not blinded; covariance-based survey distances, not raw photons; no pass threshold or significance',
        candidate_scope='Ideal balanced hard-limit dust+matched vacuum; acoustic scale profiled, no derived rd or finite-gap CMB claim',
        data=dict(order=[dict(index=i, z=float(z[i]), quantity=labels[i], value=float(y[i]))
                         for i in range(len(y))], covariance=cov.tolist(),
                  covariance_eigenvalues=eig.tolist(), condition_number=float(eig[-1]/eig[0])),
        reference_metadata=refs, duplicate_shape_groups=list(groups.values()), references=results,
        comparator=dict(scope='One extra fitted shape Omega_m; grid/refinement convergence, not analytic global-proof',
            profiles=profiles, selected_grid_count=CONFIG['comparator_grids'][-1]),
        synthetic_controls=dict(amplitude=fit_synthetic, nonpositive_boundary=boundary),
        radiation_omission=rad,
        runtime_seconds=elapsed,
        peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss *
                            (1 if sys.platform == 'darwin' else 1024))


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ('freeze', 'run'):
        raise RuntimeError('Usage: desi_bao_shape_v001.py freeze|run')
    snapshot, closure = authenticate()
    if sys.argv[1] == 'freeze':
        print(encode(snapshot).decode())
        return
    saved = json.loads(FREEZE.read_text())
    if saved != json.loads(encode(snapshot)):
        raise RuntimeError('Freeze/source/configuration differs')
    payload = run(closure)
    result = dict(freeze_sha256=sha(FREEZE), payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),
                  payload=payload)
    output = encode(result)
    if len(output) > CONFIG['output_target_bytes']:
        raise RuntimeError('Prospective output-size bound exceeded')
    print(output.decode())
    if payload['status'] != 'COMPLETE':
        raise SystemExit(2)


if __name__ == '__main__':
    main()
