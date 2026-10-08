"""Frozen full-constraint field-Jacobian diagnostic, not source evolution.

Linearize u,p,Z,cp on the saved160-cell quarter-orbit state, retaining
metric constraints but holding ordinary particle variables fixed. Two
central-difference increments reveal derivative sensitivity. Eigenvalues
belong to this semidiscrete frozen subsystem, not a continuum stability
certificate. No physical fit, trajectory acceptance or gate change.
"""
from pathlib import Path
import hashlib
import json
import time
import numpy as np
import invariant_clock_polar_source_v005 as source

BASE=Path(__file__).resolve().parent


def main():
    begin=time.monotonic();path=BASE/'INVARIANT_CLOCK_POLAR_SOURCE_MIXED01_CHECKPOINT.json'
    cp=json.loads(path.read_text());model=source.Polar(json.loads(source.prev.inherited.SOURCE.read_text()),160,.012)
    model.initial();z=np.array(cp['state']);t=cp['step']*cp['dt'];g=model.geometry(t,z)
    guess=g['A'].copy();sc=np.array([1e-4,1e-8,1e-8,.01])[:,None]
    rows=[];matrix_previous=None
    for eps in (1e-4,5e-5):
        matrix=np.empty((4*model.n,4*model.n))
        for i in range(4*model.n):
            component,index=divmod(i,model.n);plus=z.copy();minus=z.copy()
            plus[component,index]+=eps*sc[component,0];minus[component,index]-=eps*sc[component,0]
            model.Aguess=guess.copy();fp=model.rhs(t,plus)[:4]/sc
            model.Aguess=guess.copy();fm=model.rhs(t,minus)[:4]/sc
            matrix[:,i]=((fp-fm)/(2*eps)).ravel()*model.tdyn
        vals,vecs=np.linalg.eig(matrix);order=np.argsort(vals.real)[-8:][::-1]
        modes=[]
        for i in order:
            weights=np.sum(abs(vecs[:,i].reshape(4,model.n))**2,axis=0)
            modes.append(dict(eigenvalue_per_tdyn=[float(vals[i].real),float(vals[i].imag)],
                scaled_component_norm=np.sum(abs(vecs[:,i].reshape(4,model.n))**2,axis=1).tolist(),
                peak_radius_over_L=float(model.r[np.argmax(weights)]/model.L),
                inner10L_scaled_weight=float(sum(weights[model.mask])/sum(weights))))
        row=dict(increment=eps,modes=modes)
        if matrix_previous is not None:
            row['matrix_relative_frobenius_change']=float(np.linalg.norm(matrix-matrix_previous)/np.linalg.norm(matrix))
        rows.append(row);matrix_previous=matrix
    result=dict(protocol=__doc__,rows=rows,elapsed_seconds=time.monotonic()-begin,
        identities={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),path,Path(source.__file__))})
    with (BASE/'INVARIANT_CLOCK_POLAR_FIELD_JACOBIAN_V001_RESULT.json').open('x') as f:
        json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(result,allow_nan=False))


if __name__=='__main__':main()
