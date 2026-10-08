"""Central spherical fast-mode RK4 stability at the ACTUAL saved time step.

This tests an unexamined numerical cause of the first-cell charge growth.
The known frozen constrained fast speed is sqrt((2eta+mu)/d). Build the
actual parity-aware derivative/divergence pair on central64/96/128 nodes,
with zero perturbation beyond each test block. Track mode localization
and block dependence so an artificial outer truncation is not confused
with a genuine central mode. No physical parameter, source or trajectory
changes. Evaluate the exact RK4 polynomial at saved dt and dt/2.

Frozen numerical gates: eigen residual1e-10, polynomial derivative1e-10.
The absolute-stability condition |R(dt lambda)|<=1+1e-12 is mathematical,
not an observational fitted tolerance. Frozen-principal results are not
a full evolving-system stability proof.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import invariant_clock_polar_source_v005 as source

BASE=Path(__file__).resolve().parent
OUT=BASE/'INVARIANT_CLOCK_POLAR_CFL_AUDIT_V001_RESULT.json'


def matrices(model,n):
    operators=[]
    for parity in (1,-1):
        matrix=np.zeros((n,n))
        for i in range(n):
            for k,j in enumerate(range(i-2,i+3)):
                index=-j-1 if j<0 else j
                if index<n:matrix[i,index]+=model.weights[i,k]*(parity if j<0 else 1)
        operators.append(matrix)
    return operators[0],operators[1]+np.diag(2/model.r[:n])


def stability(z):
    return 1+z+z*z/2+z**3/6+z**4/24


def main():
    if OUT.exists():raise FileExistsError(OUT)
    start=time.monotonic();saved=json.loads(source.prev.inherited.SOURCE.read_text())
    model=source.Polar(saved,960,.012)
    Q,m=model.bg0[2:4];d=float(model.constitutive(model.bg0[1])[2])
    speed=math.sqrt((2*model.C/model.KB+m/Q)/d)
    runs={};inputs=[]
    for tag in ('MIXED04','MIXED05B','BUFFER01C','BUFFER02D'):
        path=BASE/f'INVARIANT_CLOCK_POLAR_SOURCE_{tag}_RESULT.json'
        receipt=json.loads(path.read_text());inputs.append(path)
        runs[tag]=dict(dt=receipt['dt'],dt_factor=receipt['args']['dt_factor'],
                       quarter_orbit_steps=receipt['steps'])
    checks=[];blocks=[]
    def check(name,error):
        checks.append(dict(name=name,error=float(error),tolerance=1e-10,passed=bool(error<=1e-10)))
    for n in (64,96,128):
        grad,div=matrices(model,n);r=model.r[:n]
        interior=slice(0,n-2)
        check(f'{n}_even_quadratic',np.max(abs((grad@(r*r))[interior]-2*r[interior]))/np.max(2*r[interior]))
        check(f'{n}_odd_linear_div',np.max(abs((div@r)[interior]-3))/3)
        L=div@grad;vals,vecs=np.linalg.eig(L)
        norm=np.linalg.norm(L);modes=[]
        for index,value in enumerate(vals):
            vec=vecs[:,index];res=np.linalg.norm(L@vec-value*vec)/(norm*np.linalg.norm(vec))
            roots=[speed*np.sqrt(complex(value)),-speed*np.sqrt(complex(value))]
            for lam in roots:
                amp={tag:abs(stability(info['dt']*lam)) for tag,info in runs.items()}
                weight=abs(vec)**2;peak=int(np.argmax(weight));cumulative=np.cumsum(weight)/np.sum(weight)
                radius95=int(np.searchsorted(cumulative,.95))
                modes.append(dict(eigenvalue_H0=[lam.real,lam.imag],
                    real_rate_per_tdyn=lam.real*model.tdyn,peak_index=peak,
                    peak_radius_over_L=float(r[peak]/model.L),index95=radius95,
                    residual=float(res),RK4_amplification={tag:float(v) for tag,v in amp.items()},
                    half_step_amplification={tag:float(abs(stability(info['dt']*lam/2))) for tag,info in runs.items()},
                    cumulative_RK4_growth_per_tdyn={tag:float(math.log(max(v,1e-300))*model.tdyn/runs[tag]['dt']) for tag,v in amp.items()},
                    central_localized=peak<n//4 and radius95<n//2))
        check(f'{n}_eigen_residual',max(row['residual'] for row in modes))
        order=sorted(modes,key=lambda row:row['RK4_amplification']['BUFFER02D'],reverse=True)
        centers=[row for row in order if row['central_localized']]
        selected=centers[:4]
        blocks.append(dict(nodes=n,outer_radius_over_L=float(r[-1]/model.L),
            largest_amplification_modes=order[:4],central_modes=selected,
            central_RK4_absolute_stability=all(row['RK4_amplification']['BUFFER02D']<=1+1e-12 for row in centers)))
    inputs+=[Path(__file__),Path(source.__file__),Path(source.prev.__file__),source.prev.inherited.SOURCE]
    result=dict(protocol=__doc__,elapsed_seconds=time.monotonic()-start,
        speed=speed,inner_spacing=float(model.r[1]-model.r[0]),runs=runs,
        checks=checks,all_numerical_controls_passed=all(c['passed'] for c in checks),blocks=blocks,
        identities={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs})
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(result,allow_nan=False),flush=True)


if __name__=='__main__':main()
