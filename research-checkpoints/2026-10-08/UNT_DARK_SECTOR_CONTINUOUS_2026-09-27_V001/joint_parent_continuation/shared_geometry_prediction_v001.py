"""Small serial physical-prediction screen, not an observational fit."""
import os
import sys

sys.dont_write_bytecode = True
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[name] = '1'

import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import time
import numpy as np

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'joint_parent_dynamics'
EXPECTED = {
    'mechanical_compute.py': 'aa98fe00e9f85ac6502d22232390bb97c3f04f64cbb1b4467255250fdf0b249c',
    'SHAPE_REFERENCE_RESULTS.json': '0ed80105e9b615e5de68594ebf37d25ae42623d7724d4336101ed6966dddb7a9',
}
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
for filename, expected in EXPECTED.items():
    if digest(PARENT / filename) != expected:
        raise RuntimeError('Changed input: ' + filename)
spec = importlib.util.spec_from_file_location('mechanical', PARENT / 'mechanical_compute.py')
mechanical = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mechanical)
A0I, KB = mechanical.A0, mechanical.KB
A0, C, MPC = 1.2e-10, 299792458., 3.085677581491367e22
CENTRAL = json.loads((PARENT / 'SHAPE_REFERENCE_RESULTS.json').read_text())['payload']['cases'][0]['r']
RATIOS = (4., 8., 16., CENTRAL, 32., 64., 128.)
checks = []


def check(name, actual, expected, tolerance):
    error = abs(actual-expected)/max(1., abs(expected))
    checks.append(dict(name=name, error=float(error), tolerance=tolerance,
                       passed=bool(math.isfinite(error) and error <= tolerance)))


class Law:
    def __init__(self, order):
        self.delta, self.weights = mechanical.nodes(order)

    def q(self, r):
        h = A0I*r
        mode = mechanical.root(self.delta, h)
        energy = self.weights @ (.5*self.delta**2*mode**2+.75*mode**4)
        polarization = self.weights @ (self.delta*mode)
        return float(energy/(KB*A0I**2)), float(polarization/(KB*A0I))

    def sample(self, x, r):
        x = np.asarray(x, dtype=float)
        gi = A0I*x
        z = (x/r)**2
        h = gi/np.sqrt(1+z)
        hp, hpp = (1+z)**-1.5, -3*gi/(A0I*r)**2*(1+z)**-2.5
        mode = mechanical.root(self.delta, h[..., None])
        p = (self.delta*mode) @ self.weights
        dp = (self.delta**2/(self.delta**2+3*mode**2)) @ self.weights
        energy = (.5*self.delta**2*mode**2+.75*mode**4) @ self.weights
        # Positive on-shell primitive avoids subtracting two large energies.
        f = 2*energy/(KB*A0I**2)
        fp = p*hp/(KB*gi)
        dflux = 1-(dp*hp**2+p*hpp)/KB
        fpp = (1-dflux-fp)/(2*x*x)
        return f, fp, fpp, dflux

    def eta_threshold(self, r, count):
        lo, hi = math.log(1e-4), math.log(1000*max(1., r))
        grid = np.linspace(lo, hi, count)

        def score(t):
            x = np.exp(t)
            f, fp, _, _ = self.sample(x, r)
            return f/(x*x)-2*fp

        values = score(grid)
        maxima = np.where((values[1:-1] > values[:-2]) &
                          (values[1:-1] >= values[2:]))[0]+1
        if len(maxima) == 0:
            raise RuntimeError('No interior maximum on frozen range')
        refined = []
        for i in maxima:
            a, b = grid[i-1], grid[i+1]
            ratio = (math.sqrt(5)-1)/2
            l, u = b-ratio*(b-a), a+ratio*(b-a)
            fl, fu = float(score(l)), float(score(u))
            for _ in range(70):
                if fl > fu:
                    b, u, fu = u, l, fl
                    l = b-ratio*(b-a)
                    fl = float(score(l))
                else:
                    a, l, fl = l, u, fu
                    u = a+ratio*(b-a)
                    fu = float(score(u))
            t = (a+b)/2
            refined.append((float(score(t)), float(math.exp(t))))
        maximum, x = max(refined)
        return dict(eta_crit_estimate=3/maximum, maximizing_x=x,
                    max_G_over_y=maximum, sampled_local_maxima=len(maxima))


def exact_flux(x, r):
    gi = np.asarray(x)*A0I
    z = (np.asarray(x)/r)**2
    h = gi/np.sqrt(1+z)
    mode = 2/math.sqrt(3)*np.sinh(np.arcsinh(3*math.sqrt(3)*h/2)/3)
    theta = np.arctan2(1., mode)
    fel = h*h/4*(1.5*theta-.5*np.sin(2*theta)-np.sin(4*theta)/8)
    return (2*fel*(1+z)**-1.5+gi*z*(2+z)/(1+z)**2)/A0I


def run():
    started = time.perf_counter()
    low, high = Law(128), Law(256)
    rows = []
    for r in RATIOS:
        q, qp = high.q(r)
        check(f'quadrature_Q:{r}', q, low.q(r)[0], 1e-7)
        eta_lo, eta_hi = low.eta_threshold(r, 513), high.eta_threshold(r, 1025)
        check(f'eta_grid_and_quadrature:{r}', eta_hi['eta_crit_estimate'],
              eta_lo['eta_crit_estimate'], 1e-7)
        b = 2/r**2-64/(9*math.pi**2)
        curvature = lambda x: (float(exact_flux(x, r))/x-x)/x**2
        check(f'low_field_curvature:{r}', 2*curvature(5e-5)-curvature(1e-4), b, 1e-6)
        step = 1e-4*r
        check(f'Q_derivative:{r}', (high.q(r+step)[0]-high.q(r-step)[0])/(2*step), qp, 1e-6)
        for x in (1e-3, .1, 1., r, 10*r):
            f, fp, fpp, dflux = high.sample(x, r)
            flux = x*(1-fp)
            check(f'closed_flux:{r}:{x}', float(flux), float(exact_flux(x, r)), 1e-6)
            step = x*1e-4
            derivative = (float(exact_flux(x+step, r))-float(exact_flux(x-step, r)))/(2*step)
            check(f'flux_derivative:{r}:{x}', float(dflux), derivative, 1e-6)
            derivative_f = (float(high.sample(x+step, r)[0])-float(high.sample(x-step, r)[0]))/(4*x*step)
            check(f'primitive_derivative:{r}:{x}', float(fp), derivative_f, 1e-6)
            check(f'quadrature_F:{r}:{x}', float(f), float(low.sample(x, r)[0]), 1e-7)
        rows.append(dict(r=r, Q=q, Qprime=qp, b=b,
                         Hv_km_s_Mpc=A0/C*math.sqrt(2*q/3)*MPC/1000,
                         dlogHv_db=-r**3*qp/(8*q),
                         **eta_hi))

    bounds = []
    for omega_b in (.02166, .02235):
        h0 = 73.6*1000/MPC
        ordinary_h2 = omega_b*(100*1000/MPC)**2
        required_q = 1.5*(C/A0)**2*(h0*h0-ordinary_h2)
        lo, hi = 1., 256.
        assert high.q(lo)[0] < required_q < high.q(hi)[0]
        for _ in range(80):
            mid = (lo+hi)/2
            if high.q(mid)[0] < required_q:
                lo = mid
            else:
                hi = mid
        r_boundary = (lo+hi)/2
        bounds.append(dict(omega_b=omega_b, required_Q_strictly_greater=required_q,
                           necessary_r_strictly_greater=r_boundary,
                           necessary_b_strictly_less=2/r_boundary**2-64/(9*math.pi**2)))

    result = dict(status='COMPLETE' if all(c['passed'] for c in checks) else 'UNRESOLVED_CONTROLS',
                  meaning='Conditional physical consequences; no new observational score or native derivation',
                  inherited_input_sha256=EXPECTED,
                  script_sha256=digest(Path(__file__)),
                  specification_sha256=digest(ROOT/'SHARED_GEOMETRY_PREDICTION_V001.md'),
                  rows=rows, exposed_reference_necessary_bounds=bounds, checks=checks,
                  seconds=time.perf_counter()-started,
                  peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    target = ROOT/'SHARED_GEOMETRY_PREDICTION_V001_RESULT.json'
    with target.open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False, sort_keys=True)
        stream.write('\n')
    print(json.dumps({key: result[key] for key in ('status', 'rows', 'exposed_reference_necessary_bounds', 'seconds', 'peak_self_rss_bytes')}))
    print(json.dumps({'failures': [c for c in checks if not c['passed']]}))


if __name__ == '__main__':
    run()
