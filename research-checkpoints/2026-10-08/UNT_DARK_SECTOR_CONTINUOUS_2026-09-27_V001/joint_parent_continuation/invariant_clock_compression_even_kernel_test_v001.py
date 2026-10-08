"""Prospective qualification of the parity-regular kernel at cTheta=.01.

Exact R^0,R²,R⁴,R⁶ on128/256/512 midpoint-sinh grids: value and R*chi_R
global1e-11, first-four-cell chi_R/R relative1e-10 for R². Smooth Plummer
plus constant against independent64/128-point finite-range Gauss oracle:
oracle agreement1e-11 and finest-grid value/derivative1e-6. These gates
precede execution. No source evolution, physical parameter fit or clipping.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import invariant_clock_compression_radial_v003 as kernel

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'INVARIANT_CLOCK_COMPRESSION_EVEN_KERNEL_TEST_V001_RESULT.json'
CT=.01;RATE=2/CT
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
maximum=lambda v:float(np.max(np.abs(v)))

def plummer_oracle(r,n):
    nodes,weights=np.polynomial.legendre.leggauss(n)
    top=np.minimum(RATE*np.log(r[-1]/r),50.)
    u=top[:,None]*(nodes+1)/2;t=u/RATE
    rr=r[:,None]*np.exp(t)
    dlogT=-.25*rr*rr/(1+rr*rr)**3.5
    integral=top/2*np.sum(weights*np.exp(-u)*dlogT,axis=1)
    logrder=-CT*integral
    chi=-CT*(3+.05/(1+r*r)**2.5)+logrder/RATE
    return chi,logrder

def main():
    if OUT.exists():raise FileExistsError(OUT)
    started=time.monotonic();checks=[];rows=[]
    def check(name,error,gate):checks.append(dict(name=name,error=float(error),gate=gate,passed=bool(error<=gate)))
    for n in (128,256,512):
        r=np.sinh((np.arange(n)+.5)*math.asinh(1000)/n);lr=np.log(r/r[-1])
        for degree in (0,2,4,6):
            T=(r/r[-1])**degree;part=-CT*T/(1-CT*degree/2)
            hom=.004*np.exp(RATE*lr);exact=part+hom;der=degree*part+RATE*hom
            chi,chir=map(np.array,kernel.kernel(r,T,float(part[-1]+.004),CT))
            err=max(maximum(chi-exact)/max(maximum(exact),CT),
                    maximum(r*chir-der)/max(maximum(der),CT))
            check(f'{n}_Rpower{degree}',err,1e-11)
            if degree==2:
                expected=-2*CT/(1-CT)/r[-1]**2
                check(f'{n}_origin_chi_R_over_R',maximum(chir[:4]/r[:4]/expected-1),1e-10)
        T=3+.05/(1+r*r)**2.5
        chi,chir=map(np.array,kernel.kernel(r,T,float(-CT*T[-1]),CT))
        lo=plummer_oracle(r,64);hi=plummer_oracle(r,128)
        check(f'{n}_independent_quadrature',max(maximum(lo[0]-hi[0]),maximum(lo[1]-hi[1]))/(CT*.05),1e-11)
        err=max(maximum(chi-hi[0]),maximum(r*chir-hi[1]))/(CT*.05)
        rows.append(dict(nodes=n,plummer_error=err,
                         first_four_chi_R_over_R=(chir[:4]/r[:4]).tolist(),
                         oracle_first_four_chi_R_over_R=(hi[1][:4]/r[:4]**2).tolist()))
    check('Plummer_fine',rows[-1]['plummer_error'],1e-6)
    result=dict(protocol=__doc__,rows=rows,controls=checks,
        all_controls_passed=all(row['passed'] for row in checks),
        elapsed_seconds=time.monotonic()-started,
        hashes={str(p):sha(p) for p in (Path(__file__),Path(kernel.__file__))})
    with OUT.open('x') as file:json.dump(result,file,indent=2,allow_nan=False)
    print(json.dumps(dict(rows=rows,checks=len(checks),all_controls_passed=result['all_controls_passed'],
        failures=[r for r in checks if not r['passed']],elapsed_seconds=result['elapsed_seconds'],
        result_sha256=sha(OUT)),indent=2),flush=True)
    if not result['all_controls_passed']:raise SystemExit(1)

if __name__=='__main__':main()
