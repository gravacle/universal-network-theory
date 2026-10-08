"""Spatial refinement only of the same constrained nonlinear experiment.

V001 passes all listed gates EXCEPT spatial refinement6.71e-4>1e-4.
Retain it unchanged. Freeze three SERIAL runs:257/8192,257/16384,
513/16384 nodes/steps. No altered physics, mean evolution, seed, field
parity, inverse, constraints, tangent criterion or tolerance. Reuse the
129/8192 V001 row for the coarse spatial trend. Accept only the new fine
sequence if ALL original V001 gates pass. Restore the independently
requested homogeneous RHS and initial shear controls before accepting;
both thresholds are the earlier2e-12 and1e-6 respectively. Record both
finite-difference steps for the eliminated momentum tangent test and gate
both, not merely the finer one. Checkpoint each sampled state in a new
per-resolution run checkpoint; no completed or historical output overwritten.
One NumPy process, <=513 spatial nodes; no external work or fitting.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import resource
import numpy as np
import plane_constrained_evolution_v001 as old
import plane_canonical_evolution_v002 as stable
import plane_canonical_evolution_v001 as base

BASE=Path(__file__).resolve().parent
OUT=BASE/'PLANE_CONSTRAINED_EVOLUTION_V002_RESULT.json'
PRIOR=BASE/'PLANE_CONSTRAINED_EVOLUTION_V001_RESULT.json'


class Model(old.Model):
    def diagnostics(self,x,z):
        result=super().diagnostics(x,z)
        if hasattr(self,'checkpoint'):
            with self.checkpoint.open('w') as f:
                json.dump(dict(a=math.exp(x),x=x,state_reduced=z.tolist(),diagnostics=result,
                               scope='Interrupted-run checkpoint; not an accepted result.'),f,allow_nan=False)
        return result


def preflight(saved,N):
    m=Model(saved,N);x=math.log(.01);z=m.initial();full=m.reconstruct(x,z)
    # Homogeneous dust must also be homogeneous for this constraint solve.
    homog=Model(saved,N);homog.dust_weight=np.ones(N);homog.piT=np.full(N,6*homog.OB)
    homogeneous=float(np.max(abs(homog.rhs(x,homog.initial(True)))))
    g=m.unpack(x,full);flow=stable.Model.rhs(m,x,full)
    dot=2*g['h']**2*(flow[5]-flow[4])/g['ev']
    expected=m.dx(g['bx']/g['A'])/g['A']
    shear=float(np.max(abs(dot-expected)))/max(float(np.max(abs(expected))),1e-300)
    return dict(nodes=N,homogeneous_rhs=homogeneous,initial_shear_relative_error=shear,
                passed=homogeneous<=2e-12 and shear<=1e-6)


def main():
    np.seterr(over='raise',invalid='raise',divide='raise')
    started=time.monotonic();saved=json.loads(base.SOURCE.read_text());prior=json.loads(PRIOR.read_text())
    pre=[preflight(saved,N) for N in (257,513)]
    print(json.dumps(dict(preflight=pre)),flush=True)
    if not all(r['passed'] for r in pre):raise ValueError('restored preflight controls failed')
    old.Model=Model
    rows=[]
    for N,steps in ((257,8192),(257,16384),(513,16384)):
        checkpoint=BASE/f'PLANE_CONSTRAINED_EVOLUTION_V002_N{N}_S{steps}_CHECKPOINT.json'
        with checkpoint.open('x') as f:json.dump(dict(status='starting',nodes=N,steps=steps),f)
        # Class attribute supplies the one currently running, uniquely created checkpoint.
        Model.checkpoint=checkpoint
        row=old.integrate(saved,N,steps);rows.append(row)
        with (BASE/f'PLANE_CONSTRAINED_EVOLUTION_V002_N{N}_S{steps}_ROW.json').open('x') as f:
            json.dump(row,f,allow_nan=False)
    rt=stable.compare(rows[0],rows[1]);rs=stable.compare(rows[1],rows[2])
    coarse=stable.compare(prior['rows'][-1],rows[0])
    samples=[s for r in rows for s in r['snapshots']]
    checks=dict(all_completed=all(r['completed'] for r in rows),preflight=all(r['passed'] for r in pre),
        inverse=max(r['maximum_inverse_error'] for r in rows)<=2e-12,
        time_refinement=rt is not None and rt['maximum']<=1e-4,
        space_refinement=rs is not None and rs['maximum']<=1e-4,
        Hamiltonian_background=max(s['Hamiltonian_background_normalized'] for s in samples)<=1e-9,
        Hamiltonian_perturbation=max(s['Hamiltonian_perturbation_normalized'] for s in samples)<=1e-4,
        momentum=max(s['momentum_normalized'] for s in samples)<=1e-4,
        conserved_charge=max(abs(s['mean_charge_change']) for s in samples)<=2e-12,
        eliminated_momentum_flow=all(max(max(v) for v in t['relative_momentum_defect_by_step'])<=1e-4 for r in rows for t in r['tangent_tests']))
    names=['plane_constrained_evolution_v001.py','plane_canonical_evolution_v001.py','plane_canonical_evolution_v002.py']
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        inputs_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (base.SOURCE,PRIOR)},
        dependencies_sha256={f:hashlib.sha256((BASE/f).read_bytes()).hexdigest() for f in names},
        preflight=pre,rows=rows,time_refinement=rt,space_refinement=rs,coarse_space_refinement=coarse,
        controls=checks,all_controls_passed=all(checks.values()),elapsed_seconds=time.monotonic()-started,
        peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('protocol','rows')},indent=2))
    if not result['all_controls_passed']:raise SystemExit(1)


if __name__=='__main__':main()
