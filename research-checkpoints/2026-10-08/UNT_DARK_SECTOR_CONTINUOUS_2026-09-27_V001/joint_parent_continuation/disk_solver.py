"""Small finite-volume AQUAL benchmark with restartable completed cases."""
import os
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[name] = '1'
import hashlib
import json
import math
import pathlib
import resource
import sys
import tempfile
import time
import numpy as np
from numpy.polynomial.legendre import leggauss

ROOT = pathlib.Path(__file__).resolve().parent
PREV = ROOT.parent/'joint_parent_dynamics'
A0_INT = 8/(3*math.pi)
SHAPE_PATH = PREV/'SHAPE_REFERENCE_RESULTS.json'
RATIO = json.loads(SHAPE_PATH.read_text())['payload']['cases'][0]['r']
GS_INT = RATIO*A0_INT


def encode(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_new(path, obj):
    content = json.dumps(obj, indent=2, sort_keys=True, allow_nan=False)+'\n'
    with tempfile.NamedTemporaryFile(mode='w', dir=path.parent,
                                     prefix=path.name+'.partial.', delete=False) as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())
        temporary = pathlib.Path(stream.name)
    os.link(temporary, path)  # Atomic publication that refuses an existing result.
    temporary.unlink()


def f(g):
    """Scalar flux magnitude in physical a0 units; vectorized exact law."""
    gi = np.asarray(g)*A0_INT
    z = (gi/GS_INT)**2
    h = gi/np.sqrt(1+z)
    y = 2/math.sqrt(3)*np.sinh(np.arcsinh(3*math.sqrt(3)*h/2)/3)
    theta = np.arctan2(1., y)
    fel = h*h/4*(1.5*theta-.5*np.sin(2*theta)-np.sin(4*theta)/8)
    return (2*fel*(1+z)**(-1.5)+gi*z*(2+z)/(1+z)**2)/A0_INT


def inverse(d):
    d = np.asarray(d)
    lo = np.zeros_like(d)
    hi = 2*(d+np.sqrt(d)+RATIO)
    for _ in range(70):
        mid = (lo+hi)/2
        below = f(mid) < d
        lo = np.where(below, mid, lo)
        hi = np.where(below, hi, mid)
    return (lo+hi)/2


def potential(s, eta, order):
    nodes, weights = leggauss(order)
    u = 1+(np.asarray(s)[..., None]-1)*(nodes+1)/2
    return (np.asarray(s)-1)/2*np.sum(inverse(eta/u**2)*weights, axis=-1)


def boundaries(n, eta):
    width = 8/n
    c = (np.arange(n)+.5)*width
    sr = np.sqrt(8**2+(c+1)**2)
    sz = np.sqrt(c*c+9**2)
    pr, pz = potential(sr, eta, 48), potential(sz, eta, 48)
    error = max(np.max(abs(pr-potential(sr, eta, 96))),
                np.max(abs(pz-potential(sz, eta, 96))))/max(1., float(np.max(pr)), float(np.max(pz)))
    tangent_r = inverse(eta/sr**2)*(c+1)/sr
    tangent_z = inverse(eta/sz**2)*c/sz
    edges = np.arange(n+1)*width
    bottom_flux = eta*(1/np.sqrt(edges[:-1]**2+1)-1/np.sqrt(edges[1:]**2+1))
    return c, width, pr, pz, tangent_r, tangent_z, bottom_flux, float(error)


def system(phi, boundary):
    c, h, pr, pz, tr, tz, bottom, _ = boundary
    n = len(c)
    gr, gz = np.gradient(phi, h, h, edge_order=2)
    mu_r = np.ones((n+1, n))
    mu_z = np.ones((n, n+1))
    clipped = 0

    def mu(normal, transverse):
        nonlocal clipped
        norm = np.hypot(normal, transverse)
        value = np.divide(f(norm), norm, out=np.zeros_like(norm), where=norm>0)
        clipped += int(np.sum(value < 1e-12))
        return np.maximum(value, 1e-12)

    mu_r[1:n] = mu(np.diff(phi, axis=0)/h, (gz[1:]+gz[:-1])/2)
    mu_r[n] = mu(2*(pr-phi[-1])/h, tr)
    mu_z[:, 1:n] = mu(np.diff(phi, axis=1)/h, (gr[:, 1:]+gr[:, :-1])/2)
    mu_z[:, n] = mu(2*(pz-phi[:, -1])/h, tz)
    kr = np.arange(n+1)[:, None]*h*mu_r
    kz = c[:, None]*mu_z
    kr[-1] *= 2
    kz[:, -1] *= 2
    kz[:, 0] = 0
    diag = kr[:-1]+kr[1:]+kz[:, :-1]+kz[:, 1:]
    rhs = np.zeros_like(phi)
    rhs[-1] += kr[-1]*pr
    rhs[:, -1] += kz[:, -1]*pz
    rhs[:, 0] -= bottom

    def apply(v):
        out = diag*v
        out[1:] -= kr[1:-1]*v[:-1]
        out[:-1] -= kr[1:-1]*v[1:]
        out[:, 1:] -= kz[:, 1:-1]*v[:, :-1]
        out[:, :-1] -= kz[:, 1:-1]*v[:, 1:]
        return out

    return apply, diag, rhs, clipped, kr, kz


def pcg(apply, diag, rhs, initial):
    x = initial.copy()
    residual = rhs-apply(x)
    norm_rhs = float(np.linalg.norm(rhs))
    z = residual/diag
    direction = z.copy()
    rz = float(np.sum(residual*z))
    error = float(np.linalg.norm(residual))/norm_rhs
    for iteration in range(8*len(x)+100):
        if error <= 1e-12:
            return x, iteration, error, True
        ad = apply(direction)
        denominator = float(np.sum(direction*ad))
        if denominator <= 0 or not math.isfinite(denominator):
            return x, iteration, error, False
        alpha = rz/denominator
        x += alpha*direction
        residual -= alpha*ad
        error = float(np.linalg.norm(residual))/norm_rhs
        z = residual/diag
        next_rz = float(np.sum(residual*z))
        direction = z+(next_rz/rz)*direction
        rz = next_rz
    return x, iteration+1, error, False


def solve(n, eta):
    start = time.perf_counter()
    b = boundaries(n, eta)
    c, h, pr, pz, _, _, bottom, boundary_error = b
    rr, zz = np.meshgrid(c, c, indexing='ij')
    s = np.sqrt(rr*rr+(zz+1)**2)
    scale = float(inverse(eta/4))/(eta/4)
    phi = scale*eta*(1-1/s)
    history = []
    converged = False
    for outer in range(300):
        apply, diag, rhs, _, _, _ = system(phi, b)
        candidate, inner, inner_error, ok = pcg(apply, diag, rhs, phi)
        if not ok:
            history.append({'outer': outer, 'inner': inner, 'inner_error': inner_error, 'linear_failed': True})
            break
        phi = .4*phi+.6*candidate
        apply, diag, rhs, clipped, kr, kz = system(phi, b)
        error = float(np.linalg.norm(apply(phi)-rhs)/np.linalg.norm(rhs))
        outgoing = float(np.sum(kr[-1]*(pr-phi[-1]))+np.sum(kz[:, -1]*(pz-phi[:, -1])))
        balance = abs(outgoing-float(np.sum(bottom)))/float(np.sum(bottom))
        history.append({'outer': outer, 'inner': inner, 'inner_error': inner_error,
                        'nonlinear_error': error, 'clipped_faces': clipped,
                        'flux_balance_error': balance})
        if error <= 1e-9 and clipped == 0 and balance <= 2e-6:
            converged = True
            break
    apply, diag, rhs, clipped, kr, kz = system(phi, b)
    nonlinear_error = float(np.linalg.norm(apply(phi)-rhs)/np.linalg.norm(rhs))
    disk_phi = (3*phi[:, 0]-phi[:, 1])/2
    numerical = np.gradient(disk_phi, h, edge_order=2)
    s0 = np.sqrt(c*c+1)
    exact = c/s0*inverse(eta/s0**2)
    selection = (c >= .5)&(c <= 4)
    max_error = float(np.max(abs(numerical[selection]/exact[selection]-1)))
    outgoing = float(np.sum(kr[-1]*(pr-phi[-1]))+np.sum(kz[:, -1]*(pz-phi[:, -1])))
    mass = float(np.sum(bottom))
    balance = abs(outgoing-mass)/mass
    mass_error = abs(mass-eta*(1-1/math.sqrt(65)))/mass
    checks = {'converged': bool(converged), 'boundary_quadrature': boundary_error<=1e-9,
              'unclipped': clipped==0, 'positive_curve': bool(np.all(numerical[selection]>0)),
              'flux_balance': balance<=2e-6, 'annular_mass': mass_error<=1e-13}
    if n == 128:
        checks['finest_curve_accuracy'] = max_error < .02
    return {'N': n, 'eta': eta, 'checks': checks, 'history': history,
            'nonlinear_error': nonlinear_error, 'boundary_quadrature_error': boundary_error,
            'flux_balance_error': balance, 'mass_error': mass_error,
            'max_curve_relative_error': max_error, 'radii': c.tolist(),
            'numerical_radial_force': numerical.tolist(), 'exact_radial_force': exact.tolist(),
            'phi': phi.tolist(), 'seconds': time.perf_counter()-start,
            'peak_self_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


def main():
    freeze_path = ROOT/'DISK_SOLVER_FROZEN.json'
    sources = {'DISK_SOLVER_PROTOCOL.md': sha(ROOT/'DISK_SOLVER_PROTOCOL.md'),
               'disk_solver.py': sha(ROOT/'disk_solver.py'),
               '../joint_parent_dynamics/SHAPE_REFERENCE_RESULTS.json': sha(SHAPE_PATH)}
    if sys.argv[1:] == ['freeze']:
        save_new(freeze_path, {'files': sources, 'r': RATIO})
        return
    assert not sys.argv[1:]
    assert json.loads(freeze_path.read_text())['files'] == sources
    previous = {}
    for n in (32, 64, 128):
        for eta in (.01, 1., 100.):
            path = ROOT/f'disk_case_N{n}_eta{eta:g}.json'
            if path.exists():
                record = json.loads(path.read_text())
                assert record['freeze_sha256'] == sha(freeze_path)
                assert record['payload_sha256'] == hashlib.sha256(encode(record['payload'])).hexdigest()
                payload = record['payload']
                assert payload['N'] == n and payload['eta'] == eta
                assert all(payload['checks'].values()), 'Preserved failed case; requires diagnosis.'
                if eta in previous:
                    assert payload['max_curve_relative_error'] < previous[eta]
                print(json.dumps({'resumed_verified_case': path.name}), flush=True)
            else:
                payload = solve(n, eta)
                if eta in previous:
                    payload['checks']['refinement_improves'] = payload['max_curve_relative_error'] < previous[eta]
                save_new(path, {'freeze_sha256': sha(freeze_path),
                                'payload_sha256': hashlib.sha256(encode(payload)).hexdigest(), 'payload': payload})
                print(json.dumps({k: payload[k] for k in ('N','eta','checks','max_curve_relative_error','nonlinear_error','flux_balance_error','seconds')}), flush=True)
                if not all(payload['checks'].values()):
                    raise SystemExit('Saved failed numerical benchmark case; no further cases executed.')
            previous[eta] = payload['max_curve_relative_error']


if __name__ == '__main__':
    main()
