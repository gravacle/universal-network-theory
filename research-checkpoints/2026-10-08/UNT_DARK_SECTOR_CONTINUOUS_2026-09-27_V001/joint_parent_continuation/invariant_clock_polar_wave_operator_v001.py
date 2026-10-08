"""Principal radial-wave discretization audit; no source evolution.

Inspect L_h=(D_odd+2/r)D_even for the existing derivative and extrapolation,
using coordinates in L units. This is NOT the full physical perturbation
operator. Positive-real sqrt(eigenvalue) indicates growth admitted by this
discrete principal wave/boundary pair, whose localization must be reported.
It cannot alone identify the cause of the full nonlinear discrepancy.
"""
from pathlib import Path
import hashlib
import json
import time
import numpy as np
import invariant_clock_polar_source_v005 as source

BASE=Path(__file__).resolve().parent


def main():
    begin=time.monotonic();rows=[]
    saved=json.loads(source.prev.inherited.SOURCE.read_text())
    for n in (160,320):
        model=source.Polar(saved,n,.012);model.initial()
        basis=np.eye(n)
        even=np.column_stack([model.L*model.derivative(basis[:,i],1) for i in range(n)])
        odd=np.column_stack([model.L*model.derivative(basis[:,i],-1) for i in range(n)])
        lap=(odd+np.diag(2*model.L/model.r))@even
        vals,vecs=np.linalg.eig(lap);roots=np.sqrt(vals.astype(complex))
        order=np.argsort(roots.real)[-5:][::-1];speed=.41169147107929516
        modes=[]
        for i in order:
            weights=abs(vecs[:,i])**2;cdf=np.cumsum(weights)/sum(weights)
            modes.append(dict(eigenvalue=[float(vals[i].real),float(vals[i].imag)],
                growth_per_tdyn=float(roots[i].real*speed*model.tdyn/model.L),
                peak_radius_over_L=float(model.r[np.argmax(weights)]/model.L),
                median_radius_over_L=float(model.r[np.searchsorted(cdf,.5)]/model.L),
                inner10L_weight=float(sum(weights[model.mask])/sum(weights))))
        # Independent exact polynomial tests for this derivative pair.
        x=model.r/model.L;mask=model.mask
        errors={}
        for power in (0,2,4):
            f=x**power;want=np.zeros(n) if power==0 else power*(power+1)*x**(power-2)
            errors[str(power)]=float(np.max(abs((lap@f-want)[mask])))/max(float(np.max(abs(want[mask]))),1.)
        rows.append(dict(nodes=n,modes=modes,polynomial_errors=errors))
    result=dict(protocol=__doc__,rows=rows,elapsed_seconds=time.monotonic()-begin,
        identities={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
            (Path(__file__),Path(source.__file__),Path(source.prev.__file__))})
    with (BASE/'INVARIANT_CLOCK_POLAR_WAVE_OPERATOR_V001_RESULT.json').open('x') as f:
        json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(result,allow_nan=False))


if __name__=='__main__':main()
