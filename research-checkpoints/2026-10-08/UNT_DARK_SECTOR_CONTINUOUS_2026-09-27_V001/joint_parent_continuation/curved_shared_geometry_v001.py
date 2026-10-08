"""Bounded open-curvature/shared-action diagnostic; root must freeze/release first."""
import os
import sys
sys.dont_write_bytecode = True
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
            'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import hashlib
import itertools
import json
import math
from pathlib import Path
import resource
import tempfile
import time
import numpy as np
from numpy.polynomial.legendre import leggauss

ROOT = Path(__file__).resolve().parent
STEM = 'CURVED_SHARED_GEOMETRY_V001'
PARENT = ROOT.parent/'joint_parent_dynamics'
MEAN = ROOT/'desi_dr2_bao_external_v001/desi_gaussian_bao_ALL_GCcomb_mean.txt'
COV = MEAN.with_name('desi_gaussian_bao_ALL_GCcomb_cov.txt')
CAL = ROOT/'SPARC_EFFECTIVE_TRANSFER_V001_RESULT.json'
LAW = ROOT/'shared_geometry_prediction_v001.py'
EXPECTED = {MEAN: '9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585',
    COV: '252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509',
    CAL: 'f8502c04a3f17655172b2f589b48d1eebaa7c46bb64ad9950fd10d34ceb23aa9',
    LAW: '53ca84683a2356a287481d56b8f56250626dc03ba8bd5f71fade09edfd1e4287'}
WB, WR = .02235, 4.18e-5
C, MPC = 299792458., 3.085677581491367e22
CASES = list(itertools.product((60., 70., 73.6), (.5, .75, 1., 1.5), (100., 1000., 10000.)))
DEADLINE = math.inf


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hashes():
    paths = [Path(__file__), ROOT/(STEM+'.md'), *EXPECTED,
             PARENT/'mechanical_compute.py', PARENT/'SHAPE_REFERENCE_RESULTS.json',
             ROOT/'SHARED_GEOMETRY_CONSTANT_SHEAR_REPAIR_V001.md']
    return {str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p): sha(p) for p in paths}


def save(path, obj):
    data = (json.dumps(obj, indent=2, sort_keys=True, allow_nan=False)+'\n').encode()
    with tempfile.NamedTemporaryFile(dir=ROOT, prefix=path.name+'.partial.', delete=False) as f:
        temporary = Path(f.name)
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    try:
        os.link(temporary, path)
    finally:
        temporary.unlink()


def budget():
    if time.perf_counter() > DEADLINE:
        raise TimeoutError('Frozen 55-second calculation budget reached')


def error(a, b, floor=1e-300):
    a, b = np.asarray(a), np.asarray(b)
    return float(np.max(abs(a-b)/np.maximum(floor, np.maximum(abs(a), abs(b)))))


def check(controls, name, value, tolerance):
    controls[name] = dict(value=float(value), tolerance=tolerance,
                          passed=bool(math.isfinite(value) and value <= tolerance))


class Background:
    def __init__(self, law, r, nu0, h0, ok, eta):
        self.law, self.r, self.nu0 = law, r, nu0
        self.h0, self.ok, self.eta = h0, ok, eta
        self.x0 = (h0/nu0)**2
        self.y0 = eta*self.x0
        f, fp, _, _ = law.sample(math.sqrt(self.y0), r)
        self.kappa = (100/h0)**2*(WB+WR)+ok+float(f-2*self.y0*fp)/(3*self.x0)
        self.linear = 3*self.kappa/eta
        self.finf = 2*law.q(r)[0]
        self.max_root_residual = 0.
        self.min_margin, self.min_fp, self.max_fp = math.inf, math.inf, -math.inf
        self.zgrid = np.linspace(0., 2.33, 257)
        self.ygrid = None
        self.root_iterations = 0

    def terms(self, y):
        f, fp, fpp, _ = self.law.sample(np.sqrt(y), self.r)
        g, gy = f-2*y*fp, -fp-2*y*fpp
        return f, fp, g, gy, self.linear*y-g, self.linear-gy

    def source(self, z):
        u = 1+np.asarray(z)
        return 3*(100**2*(WB*u**3+WR*u**4)+self.h0**2*self.ok*u**2)/self.nu0**2

    def inspect(self, y):
        values = self.terms(y)
        fp, ep = values[1], values[5]
        self.min_margin = min(self.min_margin, float(np.min(ep-3/self.eta)))
        self.min_fp = min(self.min_fp, float(np.min(fp)))
        self.max_fp = max(self.max_fp, float(np.max(fp)))
        return values

    def root(self, source, lo, hi):
        lo, hi, source = np.broadcast_arrays(np.asarray(lo, float), np.asarray(hi, float),
                                             np.asarray(source, float))
        lo, hi = lo.copy(), hi.copy()
        elo, ehi = self.terms(lo)[4], self.terms(hi)[4]
        scale = np.maximum(1., abs(source))
        if np.any(elo-source > 1e-11*scale) or np.any(source-ehi > 1e-11*scale):
            raise ArithmeticError('Lost continuation bracket')
        fraction = np.divide(source-elo, ehi-elo, out=np.zeros_like(source), where=ehi != elo)
        y = lo+np.clip(fraction, 0., 1.)*(hi-lo)
        for iteration in range(40):
            budget()
            values = self.terms(y)
            residual, derivative = values[4]-source, values[5]
            active = abs(residual) > 2e-13*scale
            if not np.any(active):
                break
            lo = np.where(active & (residual < 0), y, lo)
            hi = np.where(active & (residual >= 0), y, hi)
            trial = y-np.divide(residual, derivative, out=np.zeros_like(y), where=derivative != 0)
            safe = np.isfinite(trial) & (trial > lo) & (trial < hi) & (derivative > 0)
            y = np.where(active, np.where(safe, trial, (lo+hi)/2), y)
        else:
            raise ArithmeticError('Root iteration cap')
        self.root_iterations += iteration+1
        self.max_root_residual = max(self.max_root_residual, float(np.max(abs(residual)/scale)))
        self.inspect(y)
        return y

    def prepare(self):
        self.inspect(self.y0)
        if not self.kappa > 1 or not self.domain_ok():
            return False
        values = [self.y0]
        for z in self.zgrid[1:]:
            source = self.source(z)
            hi = max(values[-1], float((source+self.finf)/self.linear))*(1+2e-14)
            values.append(float(self.root(source, values[-1], hi)))
        self.ygrid = np.asarray(values)
        self.inspect(np.linspace(self.y0, self.ygrid[-1], 257))
        return self.domain_ok() and bool(np.all(np.diff(self.ygrid) > 0))

    def domain_ok(self):
        return self.min_margin > 0 and self.min_fp > 0 and self.max_fp < 1

    def at(self, z):
        z = np.asarray(z)
        i = np.clip(np.searchsorted(self.zgrid, z, side='right')-1, 0, 255)
        return self.root(self.source(z), self.ygrid[i], self.ygrid[i+1])

    def shape(self, z, labels, order):
        nodes, weights = leggauss(order)
        zz = z[:, None]*(nodes+1)/2
        yh = self.at(zz)
        chi = z*np.sum(weights/np.sqrt(yh/self.y0), axis=1)/2
        dm = np.sinh(math.sqrt(self.ok)*chi)/math.sqrt(self.ok)
        dh = 1/np.sqrt(self.at(z)/self.y0)
        dv = np.cbrt(z*dm*dm*dh)
        lookup = {'DM_over_rs': dm, 'DH_over_rs': dh, 'DV_over_rs': dv}
        return np.asarray([lookup[label][i] for i, label in enumerate(labels)])

    def summary(self):
        out = dict(kappa=self.kappa, lambda_b=(2*self.kappa+1)/3,
                   min_Eprime_minus_3_over_eta=self.min_margin,
                   min_Fprime=self.min_fp, max_Fprime=self.max_fp,
                   max_scaled_root_residual=self.max_root_residual,
                   root_iterations=self.root_iterations)
        if self.ygrid is not None:
            _, fp, g, gy, e, ep = self.terms(self.ygrid)
            u = 1+self.zgrid
            ordinary = 3*100**2*(WB*u**3+2*WR*u**4)/self.nu0**2
            q = (ordinary+2*(self.ygrid*gy-g))/(2*self.ygrid*ep)
            out['history'] = dict(z=self.zgrid.tolist(), y=self.ygrid.tolist(),
                EH=np.sqrt(self.ygrid/self.y0).tolist(), q=q.tolist(),
                lambda_eff=((2*self.kappa+1)/3-2*self.eta*gy/9).tolist(), Fprime=fp.tolist())
            out['q0'] = float(q[0])
        return out


def fit(shape, data, chol, h0):
    dw, yw = np.linalg.solve(chol, shape), np.linalg.solve(chol, data)
    amplitude = max(0., float(dw@yw/(dw@dw)))
    residual = amplitude*shape-data
    wr = np.linalg.solve(chol, residual)
    return dict(A=amplitude, chi2=float(wr@wr), prediction=(amplitude*shape).tolist(),
                residual=residual.tolist(), implied_rd_Mpc=C/1000/h0/amplitude if amplitude else None)


def main():
    global DEADLINE
    if not all(sha(p) == expected for p, expected in EXPECTED.items()):
        raise RuntimeError('Pinned input changed')
    if sys.argv[1:] == ['freeze']:
        save(ROOT/(STEM+'_FROZEN.json'), dict(files=hashes()))
        print(json.dumps({'status': 'FROZEN', 'files': hashes()}))
        return
    if sys.argv[1:]:
        raise ValueError('Only optional argument: freeze')
    if json.loads((ROOT/(STEM+'_FROZEN.json')).read_text())['files'] != hashes():
        raise RuntimeError('Source/protocol/input differs from freeze')
    target = ROOT/(STEM+'_RESULT.json')
    if target.exists() or target.is_symlink():
        raise FileExistsError(target)
    started = time.perf_counter()
    DEADLINE = started+55
    from shared_geometry_prediction_v001 import Law, CENTRAL
    a0 = json.loads(CAL.read_text())['a0_si']['inherited_calibrated']
    nu0 = a0/C*MPC/1000
    entries = [s.split() for s in MEAN.read_text().splitlines() if s and not s.startswith('#')]
    z, data = (np.asarray([float(row[i]) for row in entries]) for i in (0, 1))
    labels = [row[2] for row in entries]
    covariance = np.loadtxt(COV)
    assert len(entries) == 13 and covariance.shape == (13, 13)
    assert labels[11:] == ['DH_over_rs', 'DM_over_rs'] and z[11] == 2.33
    chol = np.linalg.cholesky(covariance)
    controls = {}
    check(controls, 'covariance_symmetry', error(covariance, covariance.T, 1.), 2e-12)
    check(controls, 'covariance_cholesky', error(chol@chol.T, covariance, 1.), 2e-12)
    nodes, weights = leggauss(128)
    chi = z*np.sum(weights/(1+z[:, None]*(nodes+1)/2), axis=1)/2
    check(controls, 'Milne_integral', error(chi, np.log1p(z)), 2e-12)
    check(controls, 'Milne_curved_DM', error(np.sinh(chi), z*(2+z)/(2*(1+z))), 2e-12)
    check(controls, 'flat_limit', error(np.sinh(1e-6*chi)/1e-6, chi), 2e-12)
    synthetic = fit(np.arange(1., 14.), 23*np.arange(1., 14.), chol, 70.)
    check(controls, 'synthetic_amplitude', abs(synthetic['A']/23-1), 2e-12)
    laws = {n: Law(n) for n in (64, 128)}
    rows = []
    for number, (h0, ok, eta) in enumerate(CASES):
        row = dict(index=number, H0=h0, Omega_K0=ok, eta=eta, controls={})
        backgrounds = {}
        try:
            budget()
            admissible = {}
            for n in (64, 128):
                bg = Background(laws[n], CENTRAL, nu0, h0, ok, eta)
                backgrounds[n] = bg
                admissible[n] = bg.prepare()
            if not all(admissible.values()):
                row['status'] = ('INADMISSIBLE_SAMPLED_BRANCH' if not any(admissible.values())
                                 else 'UNRESOLVED_FORCE_ORDER_DOMAIN')
                row['reason'] = 'kappa>1, Fprime or kinetic/monotone screen failed: '+str(admissible)
            else:
                lo, hi = backgrounds[64], backgrounds[128]
                for n, bg in backgrounds.items():
                    check(row['controls'], f'present_constraint_{n}',
                          error(bg.terms(bg.y0)[4], bg.source(0.), 1.), 1e-9)
                check(row['controls'], 'force_kappa', error(lo.kappa, hi.kappa), 1e-7)
                check(row['controls'], 'force_EH', error(np.sqrt(lo.ygrid/lo.y0), np.sqrt(hi.ygrid/hi.y0)), 1e-7)
                lterms, hterms = lo.terms(hi.ygrid), hi.terms(hi.ygrid)
                for index, name in ((0, 'F'), (1, 'Fprime'), (3, 'Gprime')):
                    check(row['controls'], 'force_'+name, error(lterms[index], hterms[index]), 1e-7)
                shape = hi.shape(z, labels, 128)
                distance_low, force_low = hi.shape(z, labels, 64), lo.shape(z, labels, 128)
                check(row['controls'], 'distance_shape', error(shape, distance_low), 1e-7)
                check(row['controls'], 'force_shape', error(shape, force_low), 1e-7)
                for n, bg in backgrounds.items():
                    check(row['controls'], f'root_residual_{n}', bg.max_root_residual, 1e-9)
                if not hi.domain_ok() or not lo.domain_ok():
                    row.update(status='INADMISSIBLE_SAMPLED_BRANCH', reason='Distance-node domain failure')
                else:
                    profiles = [fit(s, data, chol, h0) for s in (shape, distance_low, force_low)]
                    for i in (1, 2):
                        for key in ('A', 'chi2'):
                            check(row['controls'], f'profile_{i}_{key}', error(profiles[0][key], profiles[i][key], 1.), 1e-6)
                    residual = np.asarray(profiles[0]['residual'])
                    direct = float(residual@np.linalg.solve(covariance, residual))
                    check(row['controls'], 'direct_covariance_score', error(direct, profiles[0]['chi2'], 1.), 2e-12)
                    precision_shape = np.linalg.solve(covariance, shape)
                    direct_a = max(0., float(data@precision_shape/(shape@precision_shape)))
                    check(row['controls'], 'direct_amplitude', error(direct_a, profiles[0]['A']), 2e-12)
                    passed = all(c['passed'] for c in row['controls'].values()) and all(c['passed'] for c in controls.values())
                    row['status'] = 'NUMERICALLY_QUALIFIED_SAMPLED_BRANCH' if passed else 'UNRESOLVED_CONTROLS'
                    if passed:
                        row['profile'] = profiles[0]
                        row['refinement_profiles'] = profiles[1:]
                        row['dimensionless_shape'] = shape.tolist()
        except Exception as exc:
            row.update(status='UNEVALUATED_BUDGET' if isinstance(exc, TimeoutError) else 'ERROR',
                       reason=f'{type(exc).__name__}: {exc}')
        row['force_orders'] = {str(n): bg.summary() for n, bg in backgrounds.items()}
        rows.append(row)
    result = dict(files=hashes(), a0_si=a0, r=CENTRAL, omega_b=WB, omega_r=WR,
        nu0_km_s_Mpc=nu0, data=dict(z=z.tolist(), labels=labels, y=data.tolist(), covariance=covariance.tolist()),
        controls=controls, cases=rows, fitted_parameters_per_scored_case=1,
        scope='Exposed discrete curved-action screen; no native derivation, global stability or acoustic ruler prediction',
        seconds=time.perf_counter()-started,
        peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    save(target, result)
    print(json.dumps(dict(path=str(target), sha256=sha(target), bytes=target.stat().st_size,
        seconds=result['seconds'], peak_self_rss_bytes=result['peak_self_rss_bytes'],
        cases=[{k: row[k] for k in ('index', 'H0', 'Omega_K0', 'eta', 'status')}
               | ({k: row['profile'][k] for k in ('A', 'chi2', 'implied_rd_Mpc')}
                  if 'profile' in row else {'reason': row.get('reason')}) for row in rows],
        failures={str(row['index']): {k: v for k, v in row['controls'].items() if not v['passed']}
                  for row in rows if any(not c['passed'] for c in row['controls'].values())})))


if __name__ == '__main__':
    main()
