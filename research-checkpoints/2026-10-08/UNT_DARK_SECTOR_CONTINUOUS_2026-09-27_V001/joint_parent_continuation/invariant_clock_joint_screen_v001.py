"""Provisional K(X) clock, X=sqrt(Q^2-Y), not an adopted UNT derivation.

Retain the SAME K, J, constants, ordinary coupling and conserved totals.
Change one explicit physical premise: clock norm X rather than U.grad phi.
In homogeneous phi, X=q, Q=cq,p=sigma q. M=m(X)+sigma Dp_geo;
Dp_geo=C[e-(1+j)p], S=Q Dp_geo. The K-part cancels from vector force.
All metric/vector/phase momenta still follow the full Hamilton equations.
The original calibrated K(Q) failures remain independent preserved evidence.

Test the original sigma_i=1e-12 and an explicitly additional1e-3 stress
preparation, same Z_i=KB H(p_old+1)sigma_i, not a formation/population fit.
Three serial1024/2048/4096 steps per seed, ai=.01 to1. Freeze time gate1e-4,
Hamilton1e-9, charge2e-12, inverse2e-12, homogeneous2e-12, eliminated
momentum tangent1e-4 (existing two finite-difference steps/floor1e-8).
Time errors: metric/phase normalized-state floor1e-8, vector channels floor
seed*1e-4. This avoids accepting erased tiny tilt through an absolute floor.

Joint consequence: at fixed local charged state the conditional static
coefficient becomes j+zeta, zeta=m/(C X), not j alone. Report its algebraic
force curve and exact X-domain at the frozen background phase rate; these
are conditional diagnostics, NOT a stationary galaxy solution or data fit.
No new parameter/function is fitted; K,J,charge and absolute normalization
remain inherited adopted freedoms. No full-spectrum stability/CMB closure.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import homogeneous_tilt_saturation_v001 as prior

BASE=Path(__file__).resolve().parent
OUT=BASE/'INVARIANT_CLOCK_JOINT_SCREEN_V001_RESULT.json'


class Model(prior.Model):
    def unpack(self,x,z):
        if not np.all(np.isfinite(z)):raise ValueError('nonfinite state')
        abar,sbar,Qbar,mbar,Kbar,h,hx,qbar=self.bg(x)
        fa,fb,un,phase,pa,pb,pu,pc=z
        ev=np.exp(fa+2*fb);A=abar*np.exp(fa);B=abar*np.exp(fb);V=abar**3*ev
        pia=-4*abar**3*h*(1+pa);pib=-8*abar**3*h*(1+pb)
        piu=2*abar**2*pu;piph=self.pcbar*(1+pc)
        sig=un*np.exp(-fa);c=np.sqrt(1+sig*sig);w=np.zeros(1);Z=pu*np.exp(-2*fb)
        target=piph/(2*V);s=target/self.mpref
        for _ in range(12):
            q,mX,d,Kfun,dm,qroot=self.constitutive(s);Q=c*q;p=sig*q
            e=(Z-self.C*p)/self.KB;root=np.sqrt(p*p+self.bs*self.bs)
            j=self.lam*abs(p)/root;jt=self.lam*abs(p)*(p*p+2*self.bs*self.bs)/root**3
            Dp_geo=self.C*(e-(1+j)*p)
            schur=d-self.C*sig*sig*(2/self.KB+jt)
            resid=mX+sig*Dp_geo-target
            if np.any(schur<=0) or np.any(s<0):raise ValueError('invariant-clock original X branch lost')
            if np.max(abs(resid)/target)<1e-14:break
            s-=resid/(schur*(self.Q0*self.eps/(2*qroot*(1+s)**2)))
        else:raise ValueError('invariant-clock inverse failed')
        err=float(np.max(abs(resid)/target));self.max_inverse=max(self.max_inverse,err)
        self.min_schur_fraction=min(self.min_schur_fraction,float(np.min(schur/d)))
        if err>2e-12:raise ValueError('inverse gate failed')
        zz=abs(p)/self.bs
        J=self.lam*self.bs**2*(zz*np.sqrt(1+zz*zz)-np.arcsinh(zz))
        small=zz<.01
        J[small]=self.lam*self.bs**2*(2*zz[small]**3/3-zz[small]**5/5+3*zz[small]**7/28-5*zz[small]**9/72)
        qdiff=self.Q0*self.eps*(s-sbar)/((1+s)*(1+sbar)*(qroot+qbar))
        ax=bx=piux=np.zeros(1)
        Lx=self.KB*e*e+2*self.C*e*p-self.C*p*p-self.C*J+2*Kfun
        # Full partial derivatives of K(sqrt(Q^2-p^2)), not K(Q).
        m=c*mX;Dp=Dp_geo-sig*mX;S=Q*Dp_geo;cur=c*Dp_geo
        kin=pia*(pia-2*pib)/(8*V)
        return locals()

    def diagnostics(self,x,z):
        full=self.reconstruct(x,z);g=self.unpack(x,full);h=g['h']
        E=g['V']*(self.KB*g['e']**2+self.C*g['p']**2+self.C*g['J']-2*g['Kfun'])+g['piph']*g['q']+self.piT
        k=(g['pia']-g['pib'])/(4*g['V']);l=-g['pia']/(4*g['V'])
        return dict(a=math.exp(x),state=full.tolist(),physical_tilt=float(g['sig'][0]),
            mean_expansion_over_reference=float(((k+2*l)/(3*h))[0]),
            shear_over_reference=float(((k-l)/h)[0]),proper_volume_ratio=float(g['ev'][0]),
            Hamiltonian_background_normalized=float(np.max(abs(g['kin']+E)/(6*g['V']*h*h))),
            X_over_X0=float(g['q'][0]/self.Q0),vector_Q_over_X0=float(g['Q'][0]/self.Q0),
            s=float(g['s'][0]),schur_fraction=float((g['schur']/g['d'])[0]),
            charge_error=float(z[7,0]),JY=float(g['j'][0]))


def integrate(saved,seed,steps):
    m=Model(saved);m.seed=seed;x0=math.log(.01);dx=-x0/steps;z=m.initial()
    pre=float(np.max(abs(m.rhs(x0,m.initial(True)))));snaps=[];tangent=[]
    for i in range(steps+1):
        x=x0+i*dx
        if i%(steps//64)==0:snaps.append(m.diagnostics(x,z))
        if i%(steps//4)==0:tangent.append(m.tangent(x,z))
        if i==steps:break
        a=m.rhs(x,z);b=m.rhs(x+dx/2,z+dx*a/2)
        c=m.rhs(x+dx/2,z+dx*b/2);d=m.rhs(x+dx,z+dx*c)
        z+=dx*(a+2*b+2*c+d)/6
    return dict(seed=seed,steps=steps,homogeneous_rhs=pre,snapshots=snaps,
        tangent_tests=tangent,maximum_inverse_error=m.max_inverse,
        minimum_schur_fraction=m.min_schur_fraction)


def compare(a,b):
    za=np.array([s['state'] for s in a['snapshots']]);zb=np.array([s['state'] for s in b['snapshots']])
    floor=np.full(8,1e-8);floor[[2,6]]=b['seed']*1e-4
    scale=np.maximum(np.max(abs(zb),axis=(0,2)),floor)
    return float(np.max(np.max(abs(za-zb),axis=(0,2))/scale))


def main():
    beg=time.monotonic();saved=json.loads(prior.base.SOURCE.read_text());rows=[];ref=[]
    for seed in (1e-12,1e-3):
        rr=[integrate(saved,seed,n) for n in (1024,2048,4096)];rows+=rr
        ref.append(dict(seed=seed,coarse=compare(rr[0],rr[1]),fine=compare(rr[1],rr[2])))
        print(json.dumps(dict(seed=seed,refinement=ref[-1],max_sampled_tilt=max(abs(s['physical_tilt']) for s in rr[-1]['snapshots']),last=rr[-1]['snapshots'][-1])),flush=True)
    m=Model(saved);bg=m.bg(0.);X=bg[2];charge=bg[3];zeta=charge/(m.C*X)
    aa0=m.bs/(1+m.lam);static=[]
    for gn in (1e-4,1e-3,1e-2,.1,1.,10.,100.):
        target=gn*aa0;lo=0.;hi=max(target/zeta,aa0)
        for _ in range(64):
            mid=(lo+hi)/2;j=m.lam*mid/math.sqrt(mid*mid+m.bs*m.bs)
            if (j+zeta)*mid>target:hi=mid
            else:lo=mid
        grad=(lo+hi)/2;norm2=X*X-grad*grad
        static.append(dict(gNhat_over_a0=gn,gphi_over_a0=grad/aa0,
            fixed_charge_zeta=zeta,X_squared_if_same_phase_rate=norm2,
            positive_clock_branch_if_same_phase_rate=bool(norm2>=m.Q0**2),
            algebraic_residual=((m.lam*grad/math.sqrt(grad*grad+m.bs*m.bs)+zeta)*grad-target)/target))
    samples=[s for r in rows for s in r['snapshots']]
    checks=dict(homogeneous=max(r['homogeneous_rhs'] for r in rows)<=2e-12,
        inverse=max(r['maximum_inverse_error'] for r in rows)<=2e-12,
        refinement=max(r['fine'] for r in ref)<=1e-4,
        Hamiltonian=max(s['Hamiltonian_background_normalized'] for s in samples)<=1e-9,
        charge=max(abs(s['charge_error']) for s in samples)<=2e-12,
        tangent=all(t['passed'] for r in rows for t in r['tangent_tests']),
        static_algebra=max(abs(s['algebraic_residual']) for s in static)<=1e-12)
    deps=['homogeneous_tilt_saturation_v001.py','plane_canonical_evolution_v001.py','plane_canonical_evolution_v002.py']
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        input_sha256=hashlib.sha256(prior.base.SOURCE.read_bytes()).hexdigest(),
        dependencies_sha256={n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in deps},
        rows=rows,refinement=ref,conditional_static=static,present_zeta=zeta,
        controls=checks,all_controls_passed=bool(all(checks.values())),elapsed_seconds=time.monotonic()-beg)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False,default=lambda x:x.item());f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','protocol')},indent=2))
    if not all(checks.values()):raise SystemExit(1)

if __name__=='__main__':main()
