"""Same-state dense/prefix full-RHS comparison; no trajectory.

Retains the original960 grid and initial/final MIXED04 states. Only the
storage/application of the algebraically identical quadrature changes.
Reports component errors, normalized by original RHS or1e-12, and the
existing1e-3 numerical gate. A pass is not a buffered evolution result.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import invariant_clock_polar_source_v005 as old
from invariant_clock_polar_source_v006 import PrefixQuadrature

BASE=Path(__file__).resolve().parent


def main():
    model=old.Polar(json.loads(old.prev.inherited.SOURCE.read_text()),960,.012)
    initial=model.initial()
    path=BASE/'INVARIANT_CLOCK_POLAR_SOURCE_MIXED04_CHECKPOINT.json'
    cp=json.loads(path.read_text());final=np.array(cp['state'])
    mass=model.massint;lapse=model.lapseint
    pm=PrefixQuadrature(model.r,1,2);pl=PrefixQuadrature(model.r,-1,0)
    rows=[]
    for name,t,z in [('initial',0.,initial),('quarter_orbit',cp['step']*cp['dt'],final)]:
        model.massint=mass;model.lapseint=lapse;model.Aguess=np.ones(model.n)
        dense=model.rhs(t,z)
        model.massint=pm;model.lapseint=pl;model.Aguess=np.ones(model.n)
        prefix=model.rhs(t,z)
        mask=model.mask;scale=np.maximum(np.max(abs(dense[:,mask]),axis=1),1e-12)
        error=np.max(abs(dense[:,mask]-prefix[:,mask]),axis=1)/scale
        rows.append(dict(state=name,relative_error=error.tolist(),pass_gate=bool(np.max(error)<=1e-3)))
    result=dict(protocol=__doc__,rows=rows,identities={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (Path(__file__),path,Path(old.__file__),BASE/'invariant_clock_polar_source_v006.py')})
    with (BASE/'INVARIANT_CLOCK_POLAR_PREFIX_RHS_V001_RESULT.json').open('x') as f:
        json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(result,allow_nan=False))


if __name__=='__main__':main()
