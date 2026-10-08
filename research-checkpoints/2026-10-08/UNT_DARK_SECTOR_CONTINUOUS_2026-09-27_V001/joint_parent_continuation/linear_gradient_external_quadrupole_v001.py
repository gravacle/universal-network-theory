"""Linearized gradient-parent observable, not a nonlinear Solar solution."""
import os
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
            'VECLIB_MAXIMUM_THREADS'):
    os.environ[key] = '1'
import hashlib
import json
import math
from pathlib import Path
import time
import numpy as np

ROOT = Path(__file__).resolve().parent
STEM = 'LINEAR_GRADIENT_EXTERNAL_QUADRUPOLE_V001'
A0 = 1.0059833281731022e-10
GC = 3*math.pi/8*A0
GM = 1.32712440018e20
PC = 648000*149597870700/math.pi
PRIMARY_GE = 2.32e-10
SPECS = [(64,64), (128,128), (256,256), (128,256), (256,128)]


def nodes(n):
    x, w = np.polynomial.legendre.leggauss(n)
    return (x+1)/2, w/2


def modes(n, ge):
    s, w = nodes(n)
    w = 2*s*w
    h = ge/(GC*s*s)
    t = 2/math.sqrt(3)*np.sinh(np.arcsinh(3*math.sqrt(3)*h/2)/3)
    return s, w, t, h


def kernels(q, w, t):
    a = 1+t*t
    b = 1+3*t*t
    qq = np.asarray(q)[...,None]**2
    kt = np.sum(w*(t*t+qq)/(a+qq), axis=-1)
    diff = np.sum(w*(2*t*t)/((a+qq)*(b+qq)), axis=-1)
    return kt, diff


def angular(beta):
    beta = np.asarray(beta, dtype=float)
    ans = np.empty_like(beta)
    small = beta <= .125
    bs = beta[small]
    term = np.ones_like(bs)
    result = np.zeros_like(bs)
    for n in range(1,40):
        term *= -bs
        result += term*(4*n/((2*n+1)*(2*n+3)))
    ans[small] = result
    bl = beta[~small]
    root = np.sqrt(bl)
    ans[~small] = 3/bl-(3/bl+1)*np.arctan(root)/root
    return ans


def coefficient(ns, nx, ge):
    start = time.perf_counter()
    s, w, t, h = modes(ns,ge)
    x, wx = nodes(nx)
    q = x/(1-x)
    kt, diff = kernels(q,w,t)
    i2 = angular(diff/kt)/kt
    cq = -float(np.dot(wx, q*q*i2/(1-x)**2))/math.pi
    return dict(Ns=ns,Nx=nx,ge=ge,Cq=cq,min_KT=float(kt.min()),
                min_KL_minus_KT=float(diff.min()),
                max_equilibrium_relative_residual=float(np.max(abs(t+t**3-h)/h)),
                elapsed_seconds=time.perf_counter()-start)


def main():
    started = time.perf_counter()
    source = [Path(__file__),ROOT/(STEM+'.md')]
    custody = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source}
    def save(output):
        with (ROOT/(STEM+'_RESULT.json')).open('x') as f:
            json.dump(output,f,indent=2,allow_nan=False)
            f.write('\n')
        print(json.dumps(output,indent=2))
    checks = []
    def check(name, error, limit):
        checks.append(dict(name=name,error=float(error),limit=limit,
                           passed=bool(error <= limit)))
    s,w,t,h = modes(256,PRIMARY_GE)
    check('spectral_weight',abs(w.sum()-1),1e-13)
    check('equilibrium',np.max(abs(t+t**3-h)/h),1e-12)
    betas = np.array([1e-12,1e-6,.01,.125,.5,2.,10.])
    u,wu = np.polynomial.legendre.leggauss(256)
    # Subtract the angularly constant term before integration, not after it.
    ref = np.array([-b*np.dot(wu,((3*u*u-1)/2)*u*u/(1+b*u*u)) for b in betas])
    values = angular(betas)
    for i,b in enumerate(betas):
        check('angular_'+str(b),abs(values[i]-ref[i])/abs(ref[i]),1e-10)
    check('isotropic_zero',abs(float(angular(np.array([0.]))[0])),0.)
    q = 1e6
    kt, diff = kernels(np.array([q]),w,t)
    check('anisotropic_high_q',abs(float(diff[0])*q**4/np.dot(w,2*t*t)-1),1e-5)
    # Evaluate 1-KT without subtracting nearly equal floats.
    one_minus_kt = np.dot(w,1/(1+t*t+q*q))
    check('isotropic_high_q',abs(q*q*one_minus_kt-1),1e-5)
    if not all(c['passed'] for c in checks):
        save(dict(custody=custody,controls=checks,all_controls_pass=False,
                  qualified_linearized_coefficient=False,
                  scope='Control failure; physical quadratures not run.'))
        return
    cases = [coefficient(ns,nx,PRIMARY_GE) for ns,nx in SPECS]
    reference = cases[2]['Cq']
    changes = {str(i):abs(cases[i]['Cq']-reference)/reference for i in (1,3,4)}
    qualified = bool(all(c['Cq']>0 and c['min_KT']>0 and
                         c['min_KL_minus_KT']>0 and
                         c['max_equilibrium_relative_residual']<1e-12 for c in cases)
                     and all(v<1e-3 for v in changes.values()))
    sensitivity = [coefficient(256,256,ge) for ge in (2.16e-10,2.48e-10)] if qualified else []
    for case in sensitivity:
        case['individual_admissibility'] = bool(case['Cq'] > 0 and case['min_KT'] > 0
            and case['min_KL_minus_KT'] > 0 and case['max_equilibrium_relative_residual'] < 1e-12)
        case['separately_refined'] = False
    illustrations = [dict(ell_pc=pc, Q2_linear_s_2=GM/(pc*PC)**3*reference,
                          rM_over_ell=math.sqrt(GM/A0)/(pc*PC))
                     for pc in (1,10,100)] if qualified else []
    output = dict(custody=custody,
                  inputs=dict(a0=A0,gc=GC,GMsolar=GM,pc=PC,primary_ge=PRIMARY_GE,
                              specs=SPECS,refinement_tolerance=1e-3),
                  controls=checks,all_controls_pass=all(c['passed'] for c in checks),
                  primary_cases=cases,relative_changes=changes,
                  qualified_linearized_coefficient=qualified,
                  external_sensitivities=sensitivity,length_illustrations=illustrations,
                  scope='Linearized equilibrium only; full nonlinear Solar prediction and shared cosmology unresolved.',
                  elapsed_seconds=time.perf_counter()-started)
    save(output)


if __name__ == '__main__':
    main()
