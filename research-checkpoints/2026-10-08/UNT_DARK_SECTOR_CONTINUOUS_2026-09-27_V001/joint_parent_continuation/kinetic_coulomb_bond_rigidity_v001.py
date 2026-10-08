"""Exclusive, tiny local constitutive check; no old driver imports."""
from pathlib import Path
import hashlib
import json
import math
import os
import resource
import sys
import time
import traceback
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / 'KINETIC_COULOMB_BOND_RIGIDITY_V001_RESULT.json'
PROTOCOL = HERE / 'KINETIC_COULOMB_BOND_RIGIDITY_V001.md'
if OUT.exists():
    raise SystemExit('Refusing to overwrite any prior attempt')
START = time.monotonic()
T0, V0, EREF = 1., 1., 2.
S_VALUES = [.4, .5, .75, 1., 1.2, 1.25, 1.5, 1.75, 2.]
STEPS = [.01, .005, .0025]
checks, rows = [], []
anchors = ['POLARIZATION_GENERATED_RIGIDITY_V001.md',
           'GALACTIC_SMOOTHNESS_AND_COLD_HISTORY_CONSTRAINT_V001.md',
           'NATIVE_SINGLE_LINK_STRAIN_COMPLETION_PROPOSAL_V001.md',
           'HOMOTHETY_COMPRESSION_RESPONSE_V001.md']
inputs = {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
          for name in anchors}

def normalized_error(x, y):
    x, y = np.asarray(x), np.asarray(y)
    return float(np.max(abs(x-y)) / max(1., float(np.max(abs(x))),
                                       float(np.max(abs(y)))))

def check(name, value, limit=1e-11):
    value = float(value)
    checks.append(dict(name=name, value=value, limit=limit,
                       passed=bool(math.isfinite(value) and value <= limit)))

def grid(order, azimuth):
    mu, weights = np.polynomial.legendre.leggauss(order)
    phi = 2*math.pi*np.arange(azimuth)/azimuth
    n = np.stack(np.broadcast_arrays(
        np.sqrt(1-mu[:, None]**2)*np.cos(phi),
        np.sqrt(1-mu[:, None]**2)*np.sin(phi), mu[:, None]), axis=-1)
    w = np.broadcast_to(weights[:, None]/(2*azimuth), (order, azimuth))
    return n.reshape(-1, 3), w.reshape(-1)

GRIDS = [grid(12, 24), grid(24, 48)]
I = np.eye(3)

def energy(F, n, w):
    v = n @ F.T
    r2 = np.sum(v*v, axis=1)
    if np.min(r2) <= 0 or np.linalg.det(F) <= 0:
        raise ValueError('Nonpositive bond length or determinant')
    return EREF + T0*float(np.dot(w, 1/r2-2/np.sqrt(r2)))

def derivatives(F, n, w):
    v = n @ F.T
    r2 = np.sum(v*v, axis=1)
    hp = -r2**-2+r2**-1.5
    hpp = 2*r2**-3-1.5*r2**-2.5
    P = 2*T0*np.einsum('n,ni,na->ia', w*hp, v, n)
    born = 4*T0*np.einsum('n,ni,nj,na,nb->iajb', w*hpp, v, v, n, n)
    prestress = 2*T0*np.einsum('ij,ab->iajb', I,
                              np.einsum('n,na,nb->ab', w*hp, n, n))
    return P, born+prestress, born, prestress

def analytic_hessian(s):
    hp = (s-1)/s**4
    hpp = (4-3*s)/(2*s**6)
    pair = np.einsum('ij,ab->iajb', I, I)
    isotropic = pair+np.einsum('ia,jb->iajb', I, I)+np.einsum('ib,ja->iajb', I, I)
    born = 4*T0*s*s*hpp*isotropic/15
    prestress = 2*T0*hp*pair/3
    return born+prestress, born, prestress

def rank_value(A, a, m):
    return float(np.einsum('iajb,i,a,j,b', A, a, m, a, m))

def rank_exact(s, a, m):
    return T0/s**4*(2*(2*s-1)*np.dot(a,a)*np.dot(m,m)/15
                   +4*(4-3*s)*np.dot(a,m)**2/15)

def extrapolations(values):
    return [(4*values[1]-values[0])/3, (4*values[2]-values[1])/3]

m_random = np.array([.2, -.5, .7]); m_random /= np.linalg.norm(m_random)
perp = np.cross(m_random, I[2]); perp /= np.linalg.norm(perp)
a_mixed = m_random+perp; a_mixed /= np.linalg.norm(a_mixed)
DIRECTIONS = [(I[0], I[2]), (I[2], I[2]), (I[1], I[0]),
              (I[0], I[0]), (m_random, m_random), (a_mixed, m_random)]
axis = np.array([1., 2., 3.]); axis /= np.linalg.norm(axis)
cross = np.array([[0., -axis[2], axis[1]], [axis[2], 0., -axis[0]],
                  [-axis[1], axis[0], 0.]])
ROTATION = I+math.sin(.37)*cross+(1-math.cos(.37))*(cross@cross)

failure = None
try:
    check('rotation_orthogonal', normalized_error(ROTATION.T@ROTATION, I))
    check('rotation_proper', abs(float(np.linalg.det(ROTATION))-1))
    for ig, (n, w) in enumerate(GRIDS):
        check(f'grid{ig}_normalization', abs(float(sum(w))-1))
        for i in range(3):
            check(f'grid{ig}_second{i}', abs(float(np.dot(w,n[:,i]**2))-1/3))
            check(f'grid{ig}_fourth{i}', abs(float(np.dot(w,n[:,i]**4))-1/5))
            for j in range(i):
                check(f'grid{ig}_mixed{i}{j}', abs(float(np.dot(w,n[:,i]**2*n[:,j]**2))-1/15))
    for s in S_VALUES:
        F = s*I; volume = V0*s**3
        analytic_energy = EREF+T0*(s**-2-2/s)
        pressure = 2*T0*(1-s)/(3*V0*s**5)
        bulk = 2*T0*(5-4*s)/(9*V0*s**5)
        shear = 2*T0*(2*s-1)/(15*V0*s**5)
        longitudinal = 2*T0*(7-4*s)/(15*V0*s**5)
        Ae, Be, Pe = analytic_hessian(s)
        outputs = []
        for ig, (n,w) in enumerate(GRIDS):
            P, A, born, prestress = derivatives(F,n,w)
            E = energy(F,n,w)
            stress = P@F.T/volume
            check(f's{s}_grid{ig}_energy', normalized_error(E,analytic_energy))
            check(f's{s}_grid{ig}_stress', normalized_error(stress,-pressure*I))
            check(f's{s}_grid{ig}_full_hessian', normalized_error(A,Ae))
            check(f's{s}_grid{ig}_born_block', normalized_error(born,Be))
            check(f's{s}_grid{ig}_prestress_block', normalized_error(prestress,Pe))
            for idir,(a,m) in enumerate(DIRECTIONS):
                check(f's{s}_grid{ig}_rank{idir}',normalized_error(rank_value(A,a,m),rank_exact(s,a,m)))
            check(f's{s}_grid{ig}_physical_G',normalized_error(s*s*rank_value(A,I[0],I[2])/volume,shear))
            check(f's{s}_grid{ig}_physical_M',normalized_error(s*s*rank_value(A,I[2],I[2])/volume,longitudinal))
            check(f's{s}_grid{ig}_objectivity',normalized_error(energy(ROTATION@F,n,w),E))
            outputs.append(dict(energy=E,full_hessian_max=float(np.max(abs(A))),
                                prestress_max=float(np.max(abs(prestress)))))
        check(f's{s}_M_B_G_identity',normalized_error(longitudinal,bulk+4*shear/3))
        n,w = GRIDS[1]; base = energy(F,n,w)
        fd_rows = []
        for idir,(a,m) in enumerate(DIRECTIONS):
            dyad = np.outer(a,m); fd = []; determinants = []
            for step in STEPS:
                epsilon = s*step
                plus,minus = F+epsilon*dyad,F-epsilon*dyad
                determinants.extend([float(np.linalg.det(plus)),float(np.linalg.det(minus))])
                fd.append((energy(plus,n,w)+energy(minus,n,w)-2*base)/epsilon**2)
            rich = extrapolations(fd); exact = rank_exact(s,a,m)
            check(f's{s}_fd_rank{idir}',normalized_error(rich[-1],exact),2e-7)
            check(f's{s}_fd_rank{idir}_det_positive',max(0.,-min(determinants)))
            fd_rows.append(dict(direction=idir,a=a.tolist(),m=m.tolist(),
                                exact=exact,finite_differences=fd,richardson=rich,
                                minimum_determinant=min(determinants)))
        simple_fd = []; simple_determinants = []
        bulk_fd = []
        for step in STEPS:
            plus = s*(I+step*np.outer(I[0],I[1]))
            minus = s*(I-step*np.outer(I[0],I[1]))
            simple_determinants.extend([float(np.linalg.det(plus)),float(np.linalg.det(minus))])
            simple_fd.append((energy(plus,n,w)+energy(minus,n,w)-2*base)/step**2)
            ep = energy(s*math.exp(step/3)*I,n,w)
            em = energy(s*math.exp(-step/3)*I,n,w)
            first = (ep-em)/(2*step)
            second = (ep+em-2*base)/step**2
            bulk_fd.append((second-first)/volume)
        simple_rich,bulk_rich = extrapolations(simple_fd),extrapolations(bulk_fd)
        check(f's{s}_fd_exact_simple_shear',normalized_error(simple_rich[-1]/volume,shear),2e-7)
        check(f's{s}_simple_shear_constant_volume',normalized_error(simple_determinants,[s**3]*6))
        check(f's{s}_fd_log_volume_bulk',normalized_error(bulk_rich[-1],bulk),2e-7)
        classification = ('STRONGLY_ELLIPTIC' if .5<s<1.75 else
                          'MARGINAL_ACOUSTIC' if s in [.5,1.75] else 'NOT_STRONGLY_ELLIPTIC')
        rows.append(dict(s=s,complete_energy=analytic_energy,pressure=pressure,
                         bulk=bulk,shear_G=shear,longitudinal_M=longitudinal,
                         acoustic_classification=classification,
                         bulk_classification='POSITIVE' if s<1.25 else ('ZERO' if s==1.25 else 'NEGATIVE'),
                         quadrature_outputs=outputs,rank_finite_difference_rows=fd_rows,
                         simple_shear_finite_differences=simple_fd,simple_shear_richardson=simple_rich,
                         bulk_finite_differences=bulk_fd,bulk_richardson=bulk_rich))
except Exception:
    failure = traceback.format_exc()

passed = sum(c['passed'] for c in checks)
payload = dict(status=('ARITHMETIC_QUALIFIED_PENDING_ROOT_REVIEW'
                       if failure is None and passed==len(checks) else 'FAILED'),
               scope='new isotropic fixed-material bond deformation; no gravity or history qualification',
               worker_owner='observer_cosmography',pid=os.getpid(),ppid=os.getppid(),
               thread_environment={k:os.environ.get(k) for k in
                                   ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS']},
               inputs=inputs,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               protocol_sha256=hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
               arithmetic_parameters=dict(T0=T0,V0=V0,Eref=EREF),
               s_values=S_VALUES,grids=[[12,24],[24,48]],finite_difference_steps=STEPS,
               exact_strong_ellipticity_open_interval=[.5,1.75],
               exact_positive_bulk_upper_boundary=1.25,rows=rows,checks=checks,
               passed=passed,total=len(checks),failure=failure,
               peak_resident_memory_bytes=(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                                           * (1 if sys.platform=='darwin' else 1024)),
               elapsed_seconds=time.monotonic()-START,
               resumable_next_action=('root source/interpretation review before qualification'
                                      if failure is None and passed==len(checks) else
                                      'inspect sealed errors; preserve this receipt and use a new version for any repair'))
canonical=json.dumps(payload,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
with OUT.open('x') as stream:
    json.dump(dict(payload=payload,payload_sha256=hashlib.sha256(canonical).hexdigest()),stream,indent=2,allow_nan=False)
print(json.dumps(dict(status=payload['status'],pid=payload['pid'],passed=passed,total=len(checks),
                      elapsed_seconds=payload['elapsed_seconds'],
                      failed=[c for c in checks if not c['passed']],failure=failure),indent=2))
