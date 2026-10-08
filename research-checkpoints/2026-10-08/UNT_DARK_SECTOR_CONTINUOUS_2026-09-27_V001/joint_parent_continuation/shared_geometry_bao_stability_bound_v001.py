"""Ruler-free necessary stability bounds; no expansion/history fit."""
import itertools
import json
import math
import pathlib
import sys
import time
import numpy as np
from disk_solver import sha, save_new

ROOT = pathlib.Path(__file__).resolve().parent
STEM = 'SHARED_GEOMETRY_BAO_STABILITY_BOUND_V001'
DATA = ROOT/'desi_dr2_bao_external_v001'
MEAN = DATA/'desi_gaussian_bao_ALL_GCcomb_mean.txt'
COV = DATA/'desi_gaussian_bao_ALL_GCcomb_cov.txt'
EXPECTED = {MEAN: '9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585',
            COV: '252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509'}


def hashes():
    paths = [pathlib.Path(__file__), ROOT/(STEM+'.md'), MEAN, COV,
             ROOT/'SHARED_GEOMETRY_CONSTANT_SHEAR_REPAIR_V001.md', ROOT/'disk_solver.py']
    return {str(p): sha(p) for p in paths}


def halfspace(y, covariance, i, j, rmax):
    a = np.zeros(len(y))
    a[i], a[j] = 1., -rmax
    resid = float(a@y)
    variance = float(a@covariance@a)
    assert variance > 0
    bound = max(resid, 0.)**2/variance
    projected = y-covariance@a*max(resid, 0.)/variance
    shift = projected-y
    q_direct = float(shift@np.linalg.solve(covariance, shift))
    return {'Rmax': rmax, 'residual_Y1_minus_RmaxY2': resid,
            'variance': variance, 'Q_lower_bound': bound,
            'projection_Q': q_direct, 'projected_boundary_residual': float(a@projected)}


def main():
    if sys.argv[1:] == ['freeze']:
        save_new(ROOT/(STEM+'_FROZEN.json'), {'files': hashes()})
        return
    assert not sys.argv[1:]
    assert json.loads((ROOT/(STEM+'_FROZEN.json')).read_text())['files'] == hashes()
    assert all(sha(p) == expected for p, expected in EXPECTED.items())
    start = time.perf_counter()
    entries = [line.split() for line in MEAN.read_text().splitlines() if line and not line.startswith('#')]
    z = np.array([float(row[0]) for row in entries])
    y = np.array([float(row[1]) for row in entries])
    labels = [row[2] for row in entries]
    c = np.loadtxt(COV)
    radial = [i for i, label in enumerate(labels) if label == 'DH_over_rs']
    assert len(entries) == 13 and c.shape == (13, 13)
    assert radial == [2, 4, 6, 8, 10, 11]
    assert labels[12] == 'DM_over_rs' and z[11] == 2.33 and z[2] == .51
    controls = {}

    def check(name, value, tolerance):
        controls[name] = {'value': float(value), 'tolerance': tolerance, 'pass': bool(value <= tolerance)}

    ch = np.linalg.cholesky(c)
    check('covariance_symmetry', np.max(abs(c-c.T))/np.max(abs(c)), 2e-12)
    check('covariance_cholesky', np.max(abs(ch@ch.T-c))/np.max(abs(c)), 2e-12)
    for s in (.2, .8, 1.2):
        zz = np.array([.51, 2.33])
        b = 100**2*.02235*((1+zz)**3-1)
        hsquared = 70**2+s*b
        increment = hsquared[1]-hsquared[0]
        check(f'synthetic_integral_{s}', abs(increment/(s*(b[1]-b[0]))-1), 1e-12)
        lam = 1/3+2/(3*s)
        assert (lam > 1) == (s < 1)
        assert (increment < b[1]-b[0]) == (s < 1)
        hubble = np.sqrt(hsquared)
        for ruler in (50., 147., 400.):
            yy = 299792.458/(hubble*ruler)
            check(f'ruler_cancellation_{s}_{ruler}', abs((yy[0]/yy[1])/(hubble[1]/hubble[0])-1), 1e-12)
    results = []
    for i, j in itertools.combinations(radial, 2):
        d3, d4 = (float((1+z[j])**power-(1+z[i])**power) for power in (3, 4))
        ratio = float(y[i]/y[j])
        pair = {'indices': [i, j], 'z': [float(z[i]), float(z[j])],
                'Y': [float(y[i]), float(y[j])], 'observed_H_ratio_central': ratio,
                'covariance_pair': c[np.ix_([i,j], [i,j])].tolist(),
                'primary_endpoint_pair': (i == radial[0] and j == radial[-1]),
                'decreasing_branch': halfspace(y, c, i, j, 1.), 'cases': []}
        for wb, wr in itertools.product((.02166, .02235), (0., 4.18e-5)):
            density_change = wb*d3+wr*d4
            h_ceiling = 100*math.sqrt(density_change/(ratio**2-1)) if ratio > 1 else None
            ruler_floor = 299792.458/100*math.sqrt((1/y[j]**2-1/y[i]**2)/density_change) if ratio > 1 else None
            for h0 in (60., 70., 73.6, 80.):
                rmax = math.sqrt(1+density_change/(h0/100)**2)
                case = {'omega_b': wb, 'omega_r': wr, 'H0_benchmark': h0,
                        'delta_H_squared_ceiling': 100**2*density_change,
                        'central_H0_ceiling': h_ceiling,
                        'central_rd_floor_Mpc': ruler_floor,
                        'central_omega_b_minimum': max(0., ((h0/100)**2*(ratio**2-1)-wr*d4)/d3),
                        **halfspace(y, c, i, j, rmax)}
                pair['cases'].append(case)
        for k, case in enumerate([pair['decreasing_branch']]+pair['cases']):
            scale = max(1., case['Q_lower_bound'])
            check(f'pair_{i}_{j}_projection_{k}', abs(case['projection_Q']-case['Q_lower_bound'])/scale, 1e-10)
            if case['residual_Y1_minus_RmaxY2'] > 0:
                check(f'pair_{i}_{j}_boundary_{k}', abs(case['projected_boundary_residual'])/max(abs(y)), 1e-12)
        results.append(pair)
    if not all(v['pass'] for v in controls.values()):
        save_new(ROOT/(STEM+'_CONTROL_FAILURE.json'), {'files': hashes(), 'controls': controls})
        raise RuntimeError('Controls failed; target results withheld.')
    result = {'files': hashes(), 'controls': controls, 'pairs': results, 'new_fit_parameters': 0,
              'assumptions': ['same regular increasing branch from z0 for H0 bound',
                  'conserved common comoving ruler and physical metric distances',
                  'ordinary baryon/radiation density benchmarks, GN-normalized',
                  'valid local principal EFT stability window; no degenerate transition'],
              'limits': ['necessary signs not full stability', 'survey distances not raw photons',
                  'density and H0 benchmarks not fitted or assumption-free measurements',
                  'correlated pair bounds not summed; no sigma interpretation',
                  'central transformed ceilings/floors not confidence limits'],
              'seconds': time.perf_counter()-start}
    save_new(ROOT/(STEM+'_RESULT.json'), result)
    primary = next(pair for pair in results if pair['primary_endpoint_pair'])
    print(json.dumps({'seconds': result['seconds'], 'checks': len(controls), 'primary': primary}, indent=2))


if __name__ == '__main__':
    main()
