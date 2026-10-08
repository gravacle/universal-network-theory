"""Bounded overresolved Galerkin experiment, not a changed physical candidate.

Motivation is the SAVED common-state audit, not a tolerance selected after
this experiment. Represent independent fields on N odd Fourier points;
prolong to M=2N+1 (also4N+1 for padding comparison), reconstruct BOTH
momenta there, evaluate original Hamilton flow there, project only retained
independent-field RHS to N. Mean momentum remains evolved. There is no
dissipative filter or revised source/seed/action. Stable dust excess is used.

Freeze serial (N,M,steps): (129,259,4096),(129,259,8192),
(257,515,8192),(129,517,8192), a=.01 to1. Compare FULL reconstructed
overresolved states, including unmatched tails. Original numerical gates
remain: time/space/padding<=1e-4, Hbackground1e-9,Hperturbation1e-4,
momentum1e-4,charge2e-12,inverse2e-12; homogeneous2e-12,shear1e-6.
Tangent tests use prolongation of the PROJECTED retained-field velocity,
but compare against the unprojected ORIGINAL momentum RHS on M. Thus
constraint satisfaction alone does not certify the Galerkin trajectory.
Both finite-difference steps must pass1e-4, with the original1e-8 floor.
No observable/superiority acceptance if any original gate fails.
"""
from pathlib import Path
import hashlib
import json
import math
import resource
import time
import numpy as np
import plane_source_precision_v001 as precise
import plane_canonical_evolution_v002 as stable
import plane_canonical_evolution_v001 as base
from plane_common_state_audit_v001 import project

BASE=Path(__file__).resolve().parent
OUT=BASE/'PLANE_PROJECTED_EVOLUTION_V001_RESULT.json'


class Model:
    def __init__(self,saved,N,M):
        self.N=N;self.M=M;self.coarse=precise.Model(saved,N)
        self.fine=precise.Model(saved,M)

    def lift(self,z):return stable.prolong(z,self.M)
    def initial(self):return self.coarse.initial()
    def rhs(self,x,z):return project(self.fine.rhs(x,self.lift(z)),self.N)
    def diagnostics(self,x,z):return self.fine.diagnostics(x,self.lift(z))

    def tangent(self,x,z):
        zf=self.lift(z);flow=self.lift(self.rhs(x,z))
        original=stable.Model.rhs(self.fine,x,self.fine.reconstruct(x,zf))[4:6]
        errors=[]
        for step in (1e-3,5e-4):
            states=[self.fine.reconstruct(x+j*step,zf+j*step*flow)[4:6] for j in (-2,-1,1,2)]
            deriv=(states[0]-8*states[1]+8*states[2]-states[3])/(12*step)
            errors.append((np.max(abs(deriv-original),axis=1)/np.maximum(np.max(abs(original),axis=1),1e-8)).tolist())
        return dict(a=math.exp(x),relative_momentum_defect_by_step=errors,
                    passed=max(max(e) for e in errors)<=1e-4)


def preflight(saved,N,M):
    m=Model(saved,N,M);x=math.log(.01);z=m.lift(m.initial());f=m.fine
    full=f.reconstruct(x,z);g=f.unpack(x,full);flow=stable.Model.rhs(f,x,full)
    dot=2*g['h']**2*(flow[5]-flow[4])/g['ev'];expected=f.dx(g['bx']/g['A'])/g['A']
    shear=float(np.max(abs(dot-expected)))/max(float(np.max(abs(expected))),1e-300)
    f.dust_excess=np.zeros(M);f.dust_weight=np.ones(M);f.piT=np.full(M,6*f.OB)
    homog=float(np.max(abs(m.rhs(x,np.zeros((8,N))))))
    return dict(retained_nodes=N,evaluation_nodes=M,homogeneous_rhs=homog,
                initial_shear_relative_error=shear,passed=homog<=2e-12 and shear<=1e-6)


def integrate(saved,N,M,steps):
    m=Model(saved,N,M);z=m.initial();x0=math.log(.01);dx=-x0/steps
    snap=[];tangent=[];failure=None;i=0;beg=time.monotonic()
    checkpoint=BASE/f'PLANE_PROJECTED_EVOLUTION_V001_N{N}_M{M}_S{steps}_CHECKPOINT.json'
    with checkpoint.open('x') as f:json.dump(dict(status='starting',retained_nodes=N,evaluation_nodes=M,steps=steps),f)
    try:
        for i in range(steps+1):
            x=x0+i*dx
            if i%(steps//64)==0:
                snap.append(m.diagnostics(x,z))
                with checkpoint.open('w') as f:json.dump(dict(a=math.exp(x),step=i,state_reduced=z.tolist(),diagnostics=snap[-1]),f,allow_nan=False)
            if i%(steps//4)==0:tangent.append(m.tangent(x,z))
            if i==steps:break
            r1=m.rhs(x,z);r2=m.rhs(x+dx/2,z+dx*r1/2)
            r3=m.rhs(x+dx/2,z+dx*r2/2);r4=m.rhs(x+dx,z+dx*r3)
            z+=dx*(r1+2*r2+2*r3+r4)/6
    except (ValueError,FloatingPointError,OverflowError) as e:failure=f'{type(e).__name__}: {e}'
    row=dict(nodes=M,retained_nodes=N,steps=steps,completed=i==steps and failure is None,
        failure=failure,last_step=i,snapshots=snap,tangent_tests=tangent,
        maximum_inverse_error=m.fine.max_inverse,minimum_schur_fraction=m.fine.min_schur_fraction,
        maximum_Picard_iterations=m.fine.max_picard,minimum_R=m.fine.min_R,
        elapsed_seconds=time.monotonic()-beg)
    with (BASE/f'PLANE_PROJECTED_EVOLUTION_V001_N{N}_M{M}_S{steps}_ROW.json').open('x') as f:json.dump(row,f,allow_nan=False)
    print(json.dumps({k:v for k,v in row.items() if k not in ('snapshots','tangent_tests')}),flush=True)
    return row


def main():
    np.seterr(over='raise',invalid='raise',divide='raise')
    saved=json.loads(base.SOURCE.read_text());beg=time.monotonic()
    pre=[preflight(saved,N,M) for N,M in ((129,259),(257,515),(129,517))]
    print(json.dumps(dict(preflight=pre)),flush=True)
    if not all(r['passed'] for r in pre):raise ValueError('preflight failed')
    rows=[integrate(saved,N,M,s) for N,M,s in ((129,259,4096),(129,259,8192),(257,515,8192),(129,517,8192))]
    rt=stable.compare(rows[0],rows[1]);rs=stable.compare(rows[1],rows[2]);rp=stable.compare(rows[1],rows[3])
    samples=[s for r in rows for s in r['snapshots']]
    checks=dict(all_completed=all(r['completed'] for r in rows),preflight=all(r['passed'] for r in pre),
        inverse=max(r['maximum_inverse_error'] for r in rows)<=2e-12,
        time_refinement=rt is not None and rt['maximum']<=1e-4,
        space_refinement=rs is not None and rs['maximum']<=1e-4,
        padding_refinement=rp is not None and rp['maximum']<=1e-4,
        Hamiltonian_background=max(s['Hamiltonian_background_normalized'] for s in samples)<=1e-9,
        Hamiltonian_perturbation=max(s['Hamiltonian_perturbation_normalized'] for s in samples)<=1e-4,
        momentum=max(s['momentum_normalized'] for s in samples)<=1e-4,
        conserved_charge=max(abs(s['mean_charge_change']) for s in samples)<=2e-12,
        eliminated_momentum_flow=all(t['passed'] for r in rows for t in r['tangent_tests']))
    deps=['plane_source_precision_v001.py','plane_constrained_evolution_v001.py',
          'plane_canonical_evolution_v001.py','plane_canonical_evolution_v002.py','plane_common_state_audit_v001.py']
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        inputs_sha256={base.SOURCE.name:hashlib.sha256(base.SOURCE.read_bytes()).hexdigest()},
        dependencies_sha256={n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in deps},
        preflight=pre,rows=rows,time_refinement=rt,space_refinement=rs,padding_refinement=rp,
        controls=checks,all_controls_passed=all(checks.values()),elapsed_seconds=time.monotonic()-beg,
        peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','protocol')},indent=2))
    if not result['all_controls_passed']:raise SystemExit(1)


if __name__=='__main__':main()
