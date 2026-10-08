"""Source-free coupled matter/clock assembly-response diagnostic.

Reuse the independently checked six finite-k FLRW equations of compression
response V003, with prescribed test stress identically zero. The ordinary
dust evolves by its continuity/Euler equations; no held galaxy profile,
central charge fit, new coefficient, or imposed halo. cTheta=.01, width20kpc
(k=1/width, not2pi/width), current shared calibration inputs unchanged.
This near-matter-era DEVELOPMENT calculation omits radiation from a=.01
to1, so it is NOT a primordial/CMB prediction or new cosmological fit.

Two declared tangent seeds: ordinary-only isocurvature at rest, and equal
clock-charge/dust contrasts with common velocity, p=Z=0 and Phi_dot=0.
The latter is NOT certified to be the unique adiabatic growing mode and
can include fast/decaying fields. No mode is removed or damped. Unit
contrast defines a linear transfer, NOT a finite physical perturbation;
finite-seed domain bounds are reported separately, no nonlinear claim.

One serial worker, inherited two-stage fourth-order Gauss solver,
1024/2048/4096 steps and65 retained epochs. Unchanged relative full-history
component gates1e-4 and floor1e-30 for all six physical fields and all
observables. Einstein derivative1e-9; exact seed and representation checks
1e-12. A-stability is NOT phase accuracy; failed fast-mode refinement is
preserved and forbids a physical conclusion. No scientific score threshold.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import invariant_clock_compression_response_v003 as linear
import charged_clock_response_v001 as gauss

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'INVARIANT_CLOCK_COMPRESSION_ASSEMBLY_V001_RESULT.json'
OLD=ROOT/'INVARIANT_CLOCK_COMPRESSION_RESPONSE_V003_RESULT.json'
OLDSHA='57039f275d2a7d21d98d90da4e9910bc66bbd546929a4140e6cec242eae71c35'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

class Assembly(linear.Response):
    def __init__(self,model):
        super().__init__(model,20.,.01)
        mbar=self.bg(0.)[2]
        self.scale=np.array([mbar,model.Q0/self.k**2,1/self.k**2,
                             model.Q0/self.k**2,1.,1/self.k**2])
    def source(self,x,bg):return (0.,0.,0.,0.,0.)
    def matrix(self,x):
        return self.rhs(x,np.eye(7))[:6,:6]
    def values(self,x,y):
        a,Q,m,d,H,Hd,Hdx,rb,k2=self.bg(x)
        dm,rel,alpha,Z,db,theta=y*self.scale[:,None]
        phi=rel-Q*alpha;qb=m*phi+rb*theta
        chi=self.cT/self.F*(1.5*qb+k2*alpha)
        Phi=Z/2-(Q*dm+rb*db+3*H*qb)/(2*k2)
        Phidot=(qb-chi)/2-H*Phi
        E=(Z-self.m.C*rel)/self.m.KB
        state=np.array([dm,phi,alpha,Z,db,theta])
        obs=np.array([Phi,db,theta,dm/m,dm/m-db,np.sqrt(k2)*rel,E,chi])
        # Stable exact headroom rather than subtracting nearly equal clocks.
        s=self.bg_s(x);qr=Q/self.m.Q0;capr=math.sqrt(1+self.m.eps)
        upper=self.m.Q0*self.m.eps/((1+s)*(capr+qr))
        lower=self.m.Q0*self.m.eps*s/((1+s)*(qr+1))
        dx=dm/d
        return dict(a=a,state=state.tolist(),observables=obs.tolist(),
            Phi_dot=Phidot.tolist(),clock_energy_piece=(Q*dm).tolist(),
            ordinary_energy_piece=(rb*db).tolist(),metric_Z_piece=(Z/2).tolist(),
            linear_unit_seed_domain=dict(deltaX_over_nearest_margin=(abs(dx)/min(upper,lower)).tolist(),
                relative_gradient_over_bs=(np.sqrt(k2)*abs(rel)/self.m.bs).tolist(),
                ordinary_contrast=abs(db).tolist(),clock_charge_contrast=abs(dm/m).tolist(),
                vector_tilt=(np.sqrt(k2)*abs(alpha)).tolist()))
    def bg_s(self,x):return self.m.bg(x)[1]
    def initial(self,x):
        a,Q,m,d,H,Hd,Hdx,rb,k2=self.bg(x);W=Q*m+rb
        phys=np.zeros((6,2));phys[4,:]=1.
        # Second column only: common velocity, equal charge/dust contrast.
        Phi=-W/(2*k2+6*self.F*H*H*W/(W+self.cT*k2))
        theta=2*self.F*H*Phi/(W+self.cT*k2)
        phys[0,1]=m;phys[2,1]=-theta;phys[5,1]=theta
        return phys/self.scale[:,None]

def discrepancy(left,right,key):
    a=np.array([s[key] for s in left['snapshots']]);b=np.array([s[key] for s in right['snapshots']])
    errs=np.max(abs(a-b),axis=0)/np.maximum(np.max(abs(b),axis=0),1e-30)
    return dict(maximum=float(np.max(errs)),by_component=errs.tolist())

def main():
    if OUT.exists():raise FileExistsError(OUT)
    if sha(OLD)!=OLDSHA:raise ValueError('changed response evidence')
    prior=json.loads(OLD.read_text());base=linear.old.base
    if not prior['all_controls_passed']:raise ValueError('unqualified inherited response')
    if sha(Path(linear.__file__))!=prior['coordinate_repair_source_sha256']:
        raise ValueError('changed relative phase equations')
    if sha(Path(linear.old.__file__))!=prior['source_sha256']:raise ValueError('changed parent')
    for p,digest in prior['dependencies'].items():
        if sha(Path(p))!=digest:raise ValueError('changed constitutive dependency')
    saved=json.loads(base.SOURCE.read_text());saved['inherited']=prior['fixed'];model=base.Model(saved,1)
    checks=[];histories=[];started=time.monotonic();error=None
    def check(name,err,gate):checks.append(dict(name=name,error=float(err),gate=gate,passed=bool(err<=gate)))
    run=Assembly(model);x0=math.log(.01);seed=run.initial(x0);s0=run.values(x0,seed)
    a,Q,m,d,H,*_=run.bg(x0);Phi=s0['observables'][0][1]
    check('equal_contrast_seed_Phi_dot',abs(s0['Phi_dot'][1])/(abs(H*Phi)+1e-100),1e-12)
    check('equal_contrast_seed_relative_density',abs(s0['observables'][4][1]),1e-12)
    # Compare actual unforced original/relative equations including Qdot.
    old=linear.old.Response(model,20.,.01)
    old.source=lambda x,bg:(0.,0.,0.,0.,0.)
    representation_error=0.
    for x in (x0,math.log(.1),0.):
        a,Q,m,d,H,*_=run.bg(x)
        T=np.eye(7);T[:6,:6]=np.diag(run.scale/old.scale)
        T[1,2]=-Q*run.scale[2]/old.scale[1]
        Tx=np.zeros((7,7));Tx[1,2]=3*m/d*run.scale[2]/old.scale[1]
        lhs=old.rhs(x,np.eye(7))@T;rhs=T@run.rhs(x,np.eye(7))+Tx
        representation_error=max(representation_error,float(np.max(abs(lhs-rhs))/np.max(abs(lhs))))
    check('exact_time_dependent_representation',representation_error,1e-12)
    try:
        for n in (1024,2048,4096):
            run=Assembly(model);y=run.initial(x0);h=-x0/n;snaps=[]
            for i in range(n+1):
                x=x0+i*h
                if i%(n//64)==0:snaps.append(run.values(x,y))
                if i==n:break
                y=gauss.gauss_step(y,x,h,run.matrix)
                if not np.all(np.isfinite(y)):raise ValueError('nonfinite linear transfer')
                if time.monotonic()-started>45:raise TimeoutError('45 second serial diagnostic limit')
            histories.append(dict(steps=n,snapshots=snaps,Einstein_derivative=run.max_constraint))
            print(json.dumps(dict(steps=n,elapsed_seconds=time.monotonic()-started,
                final_observables=snaps[-1]['observables'],Einstein_derivative=run.max_constraint)),flush=True)
    except Exception as exc:error=dict(type=type(exc).__name__,message=str(exc))
    comparisons={}
    if len(histories)==3:
        for key in ('state','observables'):
            comparisons[key]=discrepancy(histories[-2],histories[-1],key)
            check('fine_'+key,comparisons[key]['maximum'],1e-4)
    if histories:check('Einstein_derivative',max(v['Einstein_derivative'] for v in histories),1e-9)
    result=dict(protocol=__doc__,producer_sha256=sha(Path(__file__)),inherited_receipt_sha256=OLDSHA,
        dependencies={str(p):sha(p) for p in (Path(linear.__file__),Path(linear.old.__file__),Path(gauss.__file__),Path(base.__file__),base.SOURCE)},
        calibration_sha256=prior['calibration_sha256'],fixed=model.p,cTheta=.01,width_kpc=20.,
        preparations=['ordinary_only_at_rest','equal_contrast_common_velocity_Phi_dot_zero'],
        state_order=['delta_m','varphi','alpha','Z','ordinary_delta','ordinary_theta'],
        observable_order=['Phi','delta_b','theta_b','delta_m_over_m','relative_charge_contrast','k_relative_phase','E','chi'],
        histories=histories,comparisons=comparisons,checks=checks,error=error,
        all_numerical_controls_passed=error is None and len(histories)==3 and all(c['passed'] for c in checks),
        selected_native_growing_mode=False,nonlinear_formation=False,observational_superiority=False,
        elapsed_seconds=time.monotonic()-started)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(dict(all_pass=result['all_numerical_controls_passed'],error=error,
        comparisons=comparisons,failed=[r for r in checks if not r['passed']],sha256=sha(OUT)),indent=2),flush=True)
    if not result['all_numerical_controls_passed']:raise SystemExit(1)

if __name__=='__main__':main()
