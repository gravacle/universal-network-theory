"""A dimensionless Hamiltonian prediction, not a fit to galaxy data."""
import os
for _name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
              'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_name] = '1'
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT/'QUENCH_MEAN_COEFFICIENT_V001.json'


def mean_z3(c, order):
    x,w = leggauss(order)
    theta = (x+1)*math.pi/2
    z = (1-np.cos(theta))/2
    weight = w/np.sqrt(1+np.asarray(c)[...,None]*(z+z*z))
    return np.sum(weight*z**3,axis=-1)/np.sum(weight,axis=-1)


def compact(order):
    x,w = leggauss(order)
    phi = (x+1)*math.pi/4
    z = np.sin(phi)**2
    return float(2*math.sqrt(2)*np.sum(w*math.pi/4*(3-2*z)*z*mean_z3(1-z,order)))


def direct(order):
    x,w = leggauss(order)
    phi = (x+1)*math.pi/4
    s = np.tan(phi)
    b = 2*math.sqrt(2/3)*s*np.sinh(np.arcsinh(3*math.sqrt(3/2)/(s*s))/3)
    c = b**3/(4*s)
    root_residual = float(np.max(abs(b**3+2*s*s*b-4*s)/(4*s)))
    coefficient = float(np.sum(w*math.pi/4*b**3*mean_z3(c,order)/(np.cos(phi)**2)))
    return coefficient, root_residual


def main():
    assert not OUTPUT.exists(), 'Preserve earlier coefficient.'
    rows=[]
    for n in (32,64,128,256):
        c=compact(n)
        d,err=direct(n)
        rows.append({'order':n,'compact_coefficient':c,'direct_s_coefficient':d,
                     'relative_difference':abs(c/d-1),'root_residual':err})
    cref=3*math.pi/16
    cq=rows[-1]['compact_coefficient']
    ratio=cq/cref
    endpoints=mean_z3(np.array([1.,0.]),256).tolist()
    checks={'independent_variable_changes':max(r['relative_difference'] for r in rows)<2e-8,
        'final_refinement':abs(rows[-1]['compact_coefficient']/rows[-2]['compact_coefficient']-1)<1e-11,
        'positive_cubic_root':max(r['root_residual'] for r in rows)<1e-12,
        'soft_beta_moment':abs(endpoints[0]-.25)<1e-13,
        'hard_harmonic_moment':abs(endpoints[1]-5/16)<1e-13,
        'analytical_ratio_bounds':math.sqrt(2)<ratio<5*math.sqrt(2)/4}
    result={'role':'Original conditional mechanical calculation, no observed inputs or source-history fit.',
        'definition':'Cq=integral_0^infinity orbit_mean(Y^3) ds; V_s=.5s^2Y^2+.25Y^4-sY, energy0.',
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'rows':rows,'C_relaxed':cref,'C_quench':cq,'C_quench_over_relaxed':ratio,
        'a0_mean_over_a0_relaxed':1/ratio,'endpoint_z3_moments':endpoints,
        'checks':checks,
        'scope':'Infinite-time mean in a scalar uncoupled conservative continuum window; not finite-age gravity, native state, or observed galaxy correction.'}
    result['payload_sha256']=hashlib.sha256(json.dumps(result,sort_keys=True,
        separators=(',',':'),allow_nan=False).encode()).hexdigest()
    with OUTPUT.open('x') as out:
        json.dump(result,out,sort_keys=True,indent=2,allow_nan=False)
        out.write('\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
