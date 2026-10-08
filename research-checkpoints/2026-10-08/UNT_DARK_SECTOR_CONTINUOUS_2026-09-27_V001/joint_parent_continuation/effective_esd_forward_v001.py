"""One bounded, no-refit forward ESD/covariance screen; see adjacent protocol."""
import hashlib
import io
import json
import math
import pathlib
import resource
import sys
import tarfile
import time

import numpy as np
from numpy.polynomial.legendre import leggauss
import disk_solver as inherited

ROOT = pathlib.Path(__file__).resolve().parent
STEM = 'EFFECTIVE_ESD_FORWARD_V001'
ARCHIVE = ROOT/'external_brouwer2021_v001/brouwer2021_rar.tar'
CALIBRATION = ROOT/'SPARC_EFFECTIVE_TRANSFER_V001_RESULT.json'
PROFILE = 'Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt'
COVARIANCE = 'Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt'
G = 6.67430e-11
PC = 3.085677581491367e16
MSUN = 1.98847e30
SI_TO_ESD = PC**2/MSUN
MODELS = ('baryons', 'inherited_calibrated', 'rar_calibrated')


def hashes():
    return {str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):
            inherited.sha(p) for p in (ROOT/(STEM+'.md'), pathlib.Path(__file__),
                                      ARCHIVE, CALIBRATION, ROOT/'disk_solver.py',
                                      inherited.SHAPE_PATH)}


def flux_derivative(g):
    gi = np.asarray(g)*inherited.A0_INT
    z = (gi/inherited.GS_INT)**2
    w = 1+z
    h = gi/np.sqrt(w)
    q = 2/np.sqrt(3)*np.sinh(np.arcsinh(3*np.sqrt(3)*h/2)/3)
    theta = np.arctan2(1., q)
    bracket = 1.5*theta-.5*np.sin(2*theta)-np.sin(4*theta)/8
    fel = h*h*bracket/4
    fel_h = .5*(h*bracket-q*q/(1+q*q))
    return (2*fel_h/w**3-6*fel*gi/inherited.GS_INT**2/w**2.5
            + z*(2+z)/w**2+4*z/w**3)


def response(x, model):
    if model == 'inherited_calibrated':
        return inherited.inverse(x)
    if model == 'rar_calibrated':
        return x/(-np.expm1(-np.sqrt(x)))
    if model == 'deep':
        return np.sqrt(x)
    return x


def integrand(x, model):
    if model == 'inherited_calibrated':
        return np.sqrt(x)/flux_derivative(inherited.inverse(x))
    if model == 'rar_calibrated':
        s = np.sqrt(x)
        d = -np.expm1(-s)
        return s/d - x*np.exp(-s)/(2*d*d)
    if model == 'deep':
        return np.ones_like(x)/2
    return np.sqrt(x)


def esd(gbar, model, a0, order=64, alternate=False):
    gbar = np.asarray(gbar)
    if model == 'baryons':
        return gbar/(math.pi*G)*SI_TO_ESD
    nodes, weights = leggauss(order)
    theta = (nodes+1)*math.pi/4
    weights = weights*math.pi/4
    y = gbar/a0
    x = y[..., None]*np.cos(theta)**2
    if alternate:
        fy = response(y, model)
        delta = (fy[..., None]-response(x, model))/np.sin(theta)**2
        return a0/(2*math.pi*G)*(fy+np.sum(delta*np.cos(theta)*weights, axis=-1))*SI_TO_ESD
    return np.sqrt(a0*gbar)/(math.pi*G)*np.sum(integrand(x, model)*weights, axis=-1)*SI_TO_ESD


def bin_average(edges, model, a0, mode, shift):
    nodes, weights = leggauss(16)
    lo, hi = np.log(edges[:-1]), np.log(edges[1:])
    logg = lo[:, None]+(hi-lo)[:, None]*(nodes+1)/2
    averaging_weights = np.broadcast_to(weights, logg.shape).copy()
    if mode == 'area_average':
        averaging_weights *= np.exp(-logg)  # dg/g^2 = dlog(g)/g
    values = esd(np.exp(logg)*10**shift, model, a0)
    return np.sum(averaging_weights*values, axis=1)/np.sum(averaging_weights, axis=1)


def load_data():
    with tarfile.open(ARCHIVE) as archive:
        contents = {n: archive.extractfile(n).read() for n in (PROFILE, COVARIANCE, 'README.txt')}
    data = np.loadtxt(io.BytesIO(contents[PROFILE]))
    entries = np.loadtxt(io.BytesIO(contents[COVARIANCE]))
    assert data.shape == (15, 8) and entries.shape == (225, 7)
    coords = np.unique(entries[:, 2])
    assert len(coords) == 15 and np.all(np.diff(coords) > 0)
    assert np.max(abs(data[:, 0]/coords-1)) < 2e-4
    covariance, corr, bias = (np.zeros((15, 15)) for _ in range(3))
    counts = np.zeros((15, 15), dtype=int)
    for row in entries:
        i, j = np.searchsorted(coords, row[2:4])
        assert coords[i] == row[2] and coords[j] == row[3]
        assert row[0] == row[1] == -999
        covariance[i, j] = row[4]/row[6]
        corr[i, j] = row[5]
        bias[i, j] = row[6]
        counts[i, j] += 1
    assert np.all(counts == 1)
    return data, coords, covariance, corr, bias, {n: hashlib.sha256(b).hexdigest() for n, b in contents.items()}


def score(pred, observed, covariance, mask):
    resid = pred[mask]-observed[mask]
    cov = covariance[np.ix_(mask, mask)]
    white = np.linalg.solve(np.linalg.cholesky(cov), resid)
    q = float(white@white)
    return {'n': int(np.sum(mask)), 'Q': q, 'Q_per_bin': q/np.sum(mask),
            'mean_log10_pred_over_data': float(np.mean(np.log10(pred[mask]/observed[mask]))),
            'rms_log10_pred_over_data': float(np.sqrt(np.mean(np.log10(pred[mask]/observed[mask])**2))),
            'residual_esd': resid.tolist(), 'whitened_residual': white.tolist()}


def main():
    if sys.argv[1:] == ['freeze']:
        inherited.save_new(ROOT/(STEM+'_FROZEN.json'), {'files': hashes(), 'r': inherited.RATIO})
        return
    assert not sys.argv[1:]
    assert json.loads((ROOT/(STEM+'_FROZEN.json')).read_text())['files'] == hashes()
    started = time.perf_counter()
    calibration = json.loads(CALIBRATION.read_text())['a0_si']
    a0 = calibration['inherited_calibrated']
    data, gbar, cov, corr, bias, member_hashes = load_data()
    observed = data[:, 1]/data[:, 4]
    errors = data[:, 3]/data[:, 4]
    edges = np.geomspace(1e-15, 5e-12, 16)
    controls = {}
    checks = {}

    def check(name, value, tolerance):
        controls[name] = {'value': float(value), 'tolerance': tolerance}
        checks[name] = bool(value <= tolerance)

    check('coordinate_arithmetic_centres', np.max(abs(gbar/((edges[:-1]+edges[1:])/2)-1)), 2e-4)
    check('covariance_symmetry', np.max(abs(cov-cov.T))/np.max(abs(cov)), 1e-10)
    check('covariance_diagonal_errors', np.max(abs(np.sqrt(np.diag(cov))/errors-1)), 2e-4)
    check('bias_product', np.max(abs(bias/np.outer(data[:, 4], data[:, 4])-1)), 2e-4)
    reconstructed_corr = cov/np.sqrt(np.outer(np.diag(cov), np.diag(cov)))
    check('correlation', np.max(abs(corr-reconstructed_corr)), 1e-10)
    eig = np.linalg.eigvalsh(cov)
    checks['positive_covariance'] = bool(eig[0] > 0)
    x = np.geomspace(1e-12, 1e3, 101)
    check('inverse_flux', np.max(abs(inherited.f(inherited.inverse(x))/x-1)), 1e-10)
    g = np.geomspace(1e-7, 1e4, 101)
    h = g*2e-4
    fd = (-inherited.f(g+2*h)+8*inherited.f(g+h)-8*inherited.f(g-h)+inherited.f(g-2*h))/(12*h)
    check('flux_derivative', np.max(abs(flux_derivative(g)/fd-1)), 1e-6)
    target = np.geomspace(1e-15/10**.2, 5e-12*10**.2, 41)
    for model in ('inherited_calibrated', 'rar_calibrated', 'newton', 'deep'):
        scale = calibration.get(model, a0)
        p64 = esd(target, model, scale, 64)
        p128 = esd(target, model, scale, 128)
        check(model+'_quadrature', np.max(abs(p64/p128-1)), 1e-8)
        alt = esd(target, model, scale, 64, alternate=True)
        check(model+'_alternate_projection', np.max(abs(alt/p64-1)), 1e-6)
        checks[model+'_positive_monotone'] = bool(np.all(p64 > 0) and np.all(np.diff(p64) > 0))
        if model in ('newton', 'deep'):
            exact = target/(math.pi*G) if model == 'newton' else np.sqrt(scale*target)/(4*G)
            check(model+'_analytic', np.max(abs(p64/(exact*SI_TO_ESD)-1)), 1e-11)
    if not all(checks.values()):
        inherited.save_new(ROOT/(STEM+'_CONTROL_FAILURE.json'), {'checks': checks, 'controls': controls})
        raise RuntimeError('Controls failed; target scoring NOT performed; failure preserved.')
    masks = {'primary': gbar >= 1e-13, 'flagged_low': gbar < 1e-13, 'all': np.ones(15, dtype=bool)}
    results = {}
    for model in MODELS:
        scale = calibration[model]
        results[model] = {}
        for shift in (0., -.2, .2):
            cases = {'centre': esd(gbar*10**shift, model, scale),
                     'lower_edge': esd(edges[:-1]*10**shift, model, scale),
                     'upper_edge': esd(edges[1:]*10**shift, model, scale)}
            for mode in ('log_average', 'area_average'):
                cases[mode] = bin_average(edges, model, scale, mode, shift)
            results[model][str(shift)] = {mode: {'prediction_esd': pred.tolist(),
                'scores': {name: score(pred, observed, cov, mask) for name, mask in masks.items()}}
                for mode, pred in cases.items()}
    cross = data[:, 2]/data[:, 4]
    # Descriptive only: assume equal tangential/cross shape covariance, not supplied separately.
    cross_q = {name: float(cross[mask]@np.linalg.solve(cov[np.ix_(mask, mask)], cross[mask]))
               for name, mask in masks.items()}
    result = {'files': hashes(), 'member_sha256': member_hashes, 'checks': checks, 'controls': controls,
              'model': {'a0_si': calibration, 'r': inherited.RATIO, 'new_lensing_fit_parameters': 0,
                        'metric_bridge': 'older stationary Phi=Psi; not current K(X) assembly'},
              'data': {'gbar': gbar.tolist(), 'edges': edges.tolist(), 'esd_corrected': observed.tolist(),
                       'error_corrected': errors.tolist(), 'cross_corrected': cross.tolist(),
                       'covariance_corrected': cov.tolist(), 'covariance_eigenvalues': eig.tolist(),
                       'covariance_condition_number': float(eig[-1]/eig[0]),
                       'max_abs_off_diagonal_correlation': float(np.max(abs(corr-np.eye(15))))},
              'results': results, 'cross_Q_assuming_tangential_covariance': cross_q,
              'limits': ['no exact within-bin source-pair weights', 'statistical covariance excludes full systematics',
                         'fixed imported H0=70, Omega_m=.2793 distance reduction',
                         'compact spherical isolated source and common exterior assumed',
                         'mass shifts are total-baryon fixed-catalogue sensitivities, not full recalibration',
                         'not independent of earlier KiDS reduced-acceleration check',
                         'no standard-model halo comparison and no superiority claim'],
              'seconds': time.perf_counter()-started,
              'peak_self_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    inherited.save_new(ROOT/(STEM+'_RESULT.json'), result)
    print(json.dumps({'checks': checks, 'primary_centre': {m: results[m]['0.0']['centre']['scores']['primary']
          for m in MODELS}, 'seconds': result['seconds'], 'peak_self_rss_bytes': result['peak_self_rss_bytes']}, indent=2))


if __name__ == '__main__':
    main()
