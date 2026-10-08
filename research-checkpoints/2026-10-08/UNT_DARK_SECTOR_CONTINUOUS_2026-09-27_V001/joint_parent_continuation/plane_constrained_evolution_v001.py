"""Same physical IVP, independently derived fully constrained formulation.

Preserve both failed free-ADM runs. On the exact reflection-symmetric
initial sector, reconstruct pi_a,pi_b from H=D=0 and the evolved coordinate
mean pi_a. Evolve all other fields with ORIGINAL Hamilton RHS and evolve
mean pi_a with mean(original pi_a_dot). This is not continued CMC/isotropy:
both momenta are spatially varying. The tangent-defect proof establishes
continuum equivalence while pi_a<0 and the local constitutive map is regular.
Do not use a zero constraint-substituted Hamiltonian with original brackets.

Let R=pi_a/(-4 abar³ h), W=exp(fa+fb/2), R/W=1+g.
The momentum constraint is g_x=alpha/(1+g)+beta, with
alpha=exp(-fa+fb) E b_x/(4 abar³h²),
beta=exp(-fa-fb/2)(-u*piu_x+piph*phi_x)/(-4 abar³h).
An odd RHS has a zero-mean periodic primitive. Its integration constant is
set by mean(R), not a fitted homogeneous expansion. Picard at most20 steps,
change<=2e-13*max(|g|,1e-8). Report failure, never clip. Reflection symmetry
is explicitly represented by parity projection at RHS evaluations (an
exact invariant sector, not smoothing high modes). Odd grids, no filter.

Frozen: same a=.01→1, k=.01/Mpc, seed1e-5 and parameters;65/4096,
65/8192,129/8192 nodes/steps. Same1e-4 trajectory gates (full fine grid),
H background1e-9/perturbation1e-4, momentum1e-4, charge2e-12.
In addition, verify the eliminated momentum evolution at five fixed
epochs by fourth-order directional finite differences, steps1e-3 and5e-4
in ln a. Its relative defect must be<=1e-4 with1e-8 denominator floor.
Constraint satisfaction alone is not an acceptance criterion. A failure
stays failed. No changed action, branch, seed, photon model or thermal bath.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import resource
import numpy as np
import plane_canonical_evolution_v001 as base
import plane_canonical_evolution_v002 as stable

BASE=Path(__file__).resolve().parent
OUT=BASE/'PLANE_CONSTRAINED_EVOLUTION_V001_RESULT.json'


class Model(stable.Model):
    def __init__(self,saved,N):
        super().__init__(saved,N)
        self.mirror=(-np.arange(N))%N
        self.sign=np.array([1,1,-1,1,1,1,-1,1])[:,None]
        self.max_picard=0;self.max_odd_mean=0.;self.min_R=1.

    def symmetric(self,z):
        return (z+self.sign*z[:,self.mirror])/2

    def initial(self,homogeneous=False):
        z=super().initial(homogeneous)
        z[4]=np.mean(z[4]);z[5]=0.
        return self.symmetric(z)

    def primitive(self,f):
        hats=np.fft.fft(f);result=np.zeros_like(hats)
        result[1:]=hats[1:]/(1j*self.K*self.modes[1:])
        return np.fft.ifft(result).real

    def reconstruct(self,x,z):
        z=self.symmetric(z);g=self.unpack(x,z)
        a=g['abar'];h=g['h'];V=g['V'];ev=g['ev'];v=z[0]+2*z[1]
        R3=-(4*self.dx(g['bx'])+6*g['bx']**2-4*g['ax']*g['bx'])/g['A']**2
        ds=g['s']-g['sbar']
        dK=3*self.OA/self.D*(np.log1p(ds/(1+g['sbar']))-ds/((1+g['s'])*(1+g['sbar'])))
        vec=self.KB*g['e']**2+self.C*g['p']**2+self.C*g['J']
        # Exact E-background subtraction; E excludes BOTH gravitational momenta.
        ed=ev*(-R3+vec)/(6*h*h)-(g['Kbar']*np.expm1(v)+ev*dK)/(3*h*h)
        ed+=self.pcbar*(g['Qbar']*z[7]+(1+z[7])*g['qdiff'])/(6*a**3*h*h)
        ed+=g['c']*g['piux']/(6*a**3*h*h)+self.OB*(self.dust_weight-1)/(a**3*h*h)
        ed=(ed+ed[self.mirror])/2
        alpha=1.5*np.exp(-z[0]+z[1])*(1+ed)*g['bx']
        Jmom=-a*z[2]*g['piux']+g['piph']*self.dx(z[3])
        beta=np.exp(-z[0]-z[1]/2)*Jmom/(-4*a**3*h)
        wm1=np.expm1(z[0]+z[1]/2);W=1+wm1;meanpa=float(np.mean(z[4]))
        gg=np.zeros(self.N)
        for iteration in range(20):
            if np.any(1+gg<=0):raise ValueError('constrained pi_a chart approached zero')
            rhs=alpha/(1+gg)+beta
            self.max_odd_mean=max(self.max_odd_mean,abs(float(np.mean(rhs))))
            gv=self.primitive(rhs)
            constant=(meanpa-np.mean(wm1)-np.mean(W*gv))/np.mean(W)
            new=gv+constant
            change=float(np.max(abs(new-gg)))
            gg=new
            if change<=2e-13*max(float(np.max(abs(gg))),1e-8):break
        else:raise ValueError('periodic constraint Picard failed')
        self.max_picard=max(self.max_picard,iteration+1)
        pa=wm1+W*gg;R=1+pa
        self.min_R=min(self.min_R,float(np.min(R)))
        if np.any(R<=0):raise ValueError('pi_a crossed chart boundary')
        pb=pa/4+.75*(np.expm1(v)+ev*ed-pa)/R
        full=z.copy();full[4]=pa;full[5]=pb
        return full

    def rhs(self,x,z):
        full=self.reconstruct(x,z)
        out=stable.Model.rhs(self,x,full)
        out[4]=np.mean(out[4]);out[5]=0.
        return self.symmetric(out)

    def diagnostics(self,x,z):
        full=self.reconstruct(x,z)
        out=stable.Model.diagnostics(self,x,full)
        out['mean_pi_a_normalized_minus_one']=float(np.mean(full[4]))
        return out

    def tangent_test(self,x,z):
        flow=self.rhs(x,z);full=self.reconstruct(x,z)
        original=stable.Model.rhs(self,x,full)[4:6]
        errors=[]
        for step in (1e-3,5e-4):
            mm=self.reconstruct(x-2*step,z-2*step*flow)[4:6]
            m=self.reconstruct(x-step,z-step*flow)[4:6]
            p=self.reconstruct(x+step,z+step*flow)[4:6]
            pp=self.reconstruct(x+2*step,z+2*step*flow)[4:6]
            deriv=(mm-8*m+8*p-pp)/(12*step)
            denom=np.maximum(np.max(abs(original),axis=1),1e-8)
            errors.append((np.max(abs(deriv-original),axis=1)/denom).tolist())
        return dict(a=math.exp(x),relative_momentum_defect_by_step=errors,
                    passed=max(errors[-1])<=1e-4)


def integrate(saved,N,steps):
    m=Model(saved,N);x0=math.log(.01);dx=-x0/steps;z=m.initial()
    snapshots=[];tangents=[];failure=None;beg=time.monotonic();last_step=0
    try:
        for i in range(steps+1):
            x=x0+i*dx;last_step=i
            if i%(steps//64)==0:snapshots.append(m.diagnostics(x,z))
            if i%(steps//4)==0:tangents.append(m.tangent_test(x,z))
            if i==steps:break
            r1=m.rhs(x,z);r2=m.rhs(x+dx/2,z+dx*r1/2)
            r3=m.rhs(x+dx/2,z+dx*r2/2);r4=m.rhs(x+dx,z+dx*r3)
            z+=dx*(r1+2*r2+2*r3+r4)/6
    except (ValueError,FloatingPointError,OverflowError) as e:
        failure=f'{type(e).__name__}: {e}'
    result=dict(nodes=N,steps=steps,completed=last_step==steps and failure is None,
        failure=failure,last_step=last_step,last_attempted_a=math.exp(x0+last_step*dx),
        maximum_inverse_error=m.max_inverse,minimum_schur_fraction=m.min_schur_fraction,
        maximum_Picard_iterations=m.max_picard,maximum_odd_flux_mean=m.max_odd_mean,
        minimum_R=m.min_R,snapshots=snapshots,tangent_tests=tangents,
        elapsed_seconds=time.monotonic()-beg)
    print(json.dumps({k:v for k,v in result.items() if k not in ('snapshots','tangent_tests')}),flush=True)
    return result


def main():
    np.seterr(over='raise',invalid='raise',divide='raise')
    started=time.monotonic();saved=json.loads(base.SOURCE.read_text())
    rows=[integrate(saved,N,steps) for N,steps in ((65,4096),(65,8192),(129,8192))]
    rt=stable.compare(rows[0],rows[1]);rs=stable.compare(rows[1],rows[2])
    samples=[s for r in rows for s in r['snapshots']]
    checks=dict(all_completed=all(r['completed'] for r in rows),
        inverse=max(r['maximum_inverse_error'] for r in rows)<=2e-12,
        time_refinement=rt is not None and rt['maximum']<=1e-4,
        space_refinement=rs is not None and rs['maximum']<=1e-4,
        Hamiltonian_background=max(s['Hamiltonian_background_normalized'] for s in samples)<=1e-9,
        Hamiltonian_perturbation=max(s['Hamiltonian_perturbation_normalized'] for s in samples)<=1e-4,
        momentum=max(s['momentum_normalized'] for s in samples)<=1e-4,
        conserved_charge=max(abs(s['mean_charge_change']) for s in samples)<=2e-12,
        eliminated_momentum_flow=all(t['passed'] for r in rows for t in r['tangent_tests']))
    names=['plane_canonical_evolution_v001.py','plane_canonical_evolution_v002.py','PLANE_CANONICAL_EVOLUTION_V002_RESULT.json']
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        input_sha256={base.SOURCE.name:hashlib.sha256(base.SOURCE.read_bytes()).hexdigest()},
        dependencies_sha256={f:hashlib.sha256((BASE/f).read_bytes()).hexdigest() for f in names},
        rows=rows,time_refinement=rt,space_refinement=rs,controls=checks,
        all_controls_passed=all(checks.values()),elapsed_seconds=time.monotonic()-started,
        peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('protocol','rows')},indent=2))
    if not result['all_controls_passed']:raise SystemExit(1)


if __name__=='__main__':main()
