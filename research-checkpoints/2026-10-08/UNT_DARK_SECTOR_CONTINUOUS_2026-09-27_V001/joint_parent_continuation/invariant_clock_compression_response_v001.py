"""Retarded finite-k source response of one PROPOSED compression operator.

Add -cTheta*(div U)^2 with cTheta=.01, versus unchanged cTheta=0 control.
One new universal coefficient/operator, prospectively chosen, NOT fitted,
adopted or native-derived. Full independently checked linear FLRW equations
retain Q mixing, charge, lapse/shift constraints and cosmic normalization.
Use current joint-calibration K(X), baryons and Hunit, but omit radiation
consistently in this near-present dust-background diagnostic. No new cosmic
calibration/BBN/observational comparison is made. H is divided by sqrt(F),
F=1+1.5cTheta. The former Gcos/GN dictionary becomes .98/F conditionally.

Conserved prescribed isotropic Fourier TEST STRESS, not a positive matter
assembly model: R=a^3(rho_s+3H q_s)=Rfinal*f(log a), with quintic ramp over
one nominal formation time L/sqrt(kappa). q_s=-Rfinal*H*f_x/[a^3(kp^2-3Hdot)],
P_s=q_s_dot+3H q_s. It is signed, need not obey matter energy conditions,
and expands after the ramp. It measures a retarded Green response, not a
formed/supported galaxy. Initially all fields/forcing vanish; no incoming
vector, phase or fitted halo. Fixed widths5/20kpc and kappa=(200km/s/c)^2
come from the prior source test. Actual forcing is 1e-12 times that depth.
Report, do not certify, extrapolated finite-amplitude validity diagnostics.

One serial worker: CF4 Magnus with Pade13 matrix exponentials, 128/256/512
steps per formation interval, four intervals, fixed breakpoints. Frozen
state/observable refinement1e-4 with full-history component scale; matrix
exponential controls1e-10, Einstein derivative/source continuity1e-9.
No scientific success threshold. All failed attempts remain separate.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import plane_canonical_evolution_v001 as base

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'INVARIANT_CLOCK_COMPRESSION_RESPONSE_V001_RESULT.json'
CAL=ROOT/'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json'
CALSHA='c92eb0ce131a61009361f2ead3f4db7522d3eabb22f7e3d472f0e4e0c116c24f'
DEPTH=(200./299792.458)**2
PROBE=DEPTH*1e-12

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def expm(a):
    """Degree13 Pade, norm-based scaling/squaring, no added dependency."""
    b=(64764752532480000.,32382376266240000.,7771770303897600.,
       1187353796428800.,129060195264000.,10559470521600.,
       670442572800.,33522128640.,1323241920.,40840800.,960960.,
       16380.,182.,1.)
    norm=float(np.linalg.norm(a,1))
    s=max(0,int(math.ceil(math.log2(norm/5.371920351148152)))) if norm else 0
    a=a/(2.**s);eye=np.eye(a.shape[0]);a2=a@a;a4=a2@a2;a6=a4@a2
    u=a@(a6@(b[13]*a6+b[11]*a4+b[9]*a2)+b[7]*a6+b[5]*a4+b[3]*a2+b[1]*eye)
    v=a6@(b[12]*a6+b[10]*a4+b[8]*a2)+b[6]*a6+b[4]*a4+b[2]*a2+b[0]*eye
    e=np.linalg.solve(v-u,v+u)
    for _ in range(s):e=e@e
    return e

class Response:
    def __init__(self,m,width,cTheta):
        self.m=m;self.cT=cTheta;self.F=1+1.5*cTheta
        self.L=width/1000*m.p['H0_km_s_Mpc']/299792.458;self.k=1/self.L
        self.tf=self.L/math.sqrt(DEPTH)
        _,_,Q,charge,_,H,_,_=m.bg(0.);d=m.constitutive(m.bg(0.)[1])[2]
        self.xf=H/math.sqrt(self.F)*self.tf
        self.rf=2*self.k**2*PROBE
        self.scale=PROBE*np.array([d*Q,Q*self.tf,self.tf,1.,1/DEPTH,self.tf])
        self.max_constraint=0.;self.max_source=0.
    def bg(self,x):
        a,s,Q,charge,K,H,hx,qr=self.m.bg(x)
        d=self.m.constitutive(s)[2];H/=math.sqrt(self.F)
        rb=3*self.m.OB/a**3;Hd=-(rb+Q*charge)/(2*self.F)
        Hdx=3*(rb+Q*charge+charge**2/d)/(2*self.F)
        return a,Q,charge,d,H,Hd,Hdx,rb,self.k**2/a**2
    def source(self,x,bg):
        a,Q,m,d,H,Hd,Hdx,rb,k2=bg;z=x/self.xf
        if z<=0:f=fx=fxx=0.
        elif z>=1:f=1.;fx=fxx=0.
        else:
            f=z**3*(10+z*(-15+6*z))
            fx=30*z*z*(1-z)**2/self.xf
            fxx=60*z*(1-z)*(1-2*z)/self.xf**2
        r=self.rf/a**3;W=k2-3*Hd;Wx=-2*k2-3*Hdx
        q=-r*H*fx/W
        qdot=-r*H*H*(fxx+fx*(Hd/H**2-3-Wx/W))/W
        p=qdot+3*H*q;rho=r*f-3*H*q
        rhodot=r*H*(fx-3*f)-3*Hd*q-3*H*qdot
        terms=(rhodot,3*H*(rho+p),k2*q)
        defect=abs(sum(terms))/max(sum(abs(v) for v in terms),1e-80)
        self.max_source=max(self.max_source,defect)
        return r*f,r*H*(fx-3*f),q,p,rho
    def rhs(self,x,y,diagnostic=False):
        # The last row is an affine constant; columns may hold basis vectors.
        bg=self.bg(x);a,Q,m,d,H,Hd,Hdx,rb,k2=bg
        rt,rtdot,qs,ps,rhos=self.source(x,bg)
        dm,phi,alpha,Z,db,theta=y[:6]*self.scale.reshape((-1,)+(1,)*(y.ndim-1))
        one=y[6];qs=qs*one;rt=rt*one;rtdot=rtdot*one
        qbase=m*phi+rb*theta+qs
        chi=self.cT/self.F*(1.5*qbase+k2*alpha)
        potential=Z/2-(Q*dm+rb*db+3*H*(m*phi+rb*theta)+rt)/(2*k2)
        pdot=(qbase-chi)/2-H*potential
        rel=phi+Q*alpha;E=(Z-self.m.C*rel)/self.m.KB
        D=self.m.C*(E-rel)
        dmdot=-3*H*dm+3*m*pdot+k2*(D-m*phi/Q)
        phidot=dm/d+Q*potential
        adot=E-potential
        zdot=-H*Z+Q*D-chi+3*self.cT*Hd*alpha
        dbdot=3*pdot-k2*theta;tdot=potential
        qdot=-3*H*(m*phi+rb*theta)+m*phidot+rb*tdot
        u=Q*dm+rb*db+3*H*(m*phi+rb*theta)+rt
        udot=(-3*H*m/d)*dm+Q*dmdot-3*H*rb*db+rb*dbdot+3*Hd*(m*phi+rb*theta)+3*H*qdot+rtdot
        constraint=zdot/2-(udot+2*H*u)/(2*k2)-pdot
        cscale=np.abs(zdot/2)+np.abs(udot/(2*k2))+np.abs(H*u/k2)+np.abs(pdot)
        self.max_constraint=max(self.max_constraint,float(np.max(np.abs(constraint)/np.maximum(cscale,1e-80))))
        ret=np.array([dmdot,phidot,adot,zdot,dbdot,tdot])/self.scale.reshape((-1,)+(1,)*(y.ndim-1))/H
        ret=np.concatenate([ret,np.zeros_like(y[6:7])],axis=0)
        if not diagnostic:return ret
        cap=self.m.Q0*math.sqrt(1+self.m.eps)-Q
        return dict(a=a,log_a=x,log_a_formation_intervals=x/self.xf,
            state=y[:6].tolist(),observables=[float(potential/PROBE),float(E/PROBE),float(rel/PROBE),float(chi/(H*PROBE))],
            physical_depth_linear_extrapolation=dict(
                phase_gradient_over_bs=float(math.sqrt(k2)*abs(rel)*1e12/self.m.bs),
                deltaX_over_upper_margin=float(abs(dm/d)*1e12/cap),
                ordinary_contrast=float(abs(db)*1e12),
                vector_tilt=float(math.sqrt(k2)*abs(alpha)*1e12)),
            infinitesimal_probe_domain=dict(deltaX_over_upper_margin=float(abs(dm/d)/cap),
                                           phase_gradient_over_bs=float(math.sqrt(k2)*abs(rel)/self.m.bs)))
    def integrate(self,n):
        h=self.xf/n;y=np.zeros(7);y[6]=1.;snaps=[]
        cm=.5-math.sqrt(3)/6;cp=.5+math.sqrt(3)/6
        am=(3-2*math.sqrt(3))/12;ap=(3+2*math.sqrt(3))/12
        for i in range(4*n+1):
            x=i*h
            if i%(n//32)==0:snaps.append(self.rhs(x,y,True))
            if i==4*n:break
            a1=self.rhs(x+cm*h,np.eye(7));a2=self.rhs(x+cp*h,np.eye(7))
            y=expm(h*(am*a1+ap*a2))@expm(h*(ap*a1+am*a2))@y
            if not np.all(np.isfinite(y)):raise FloatingPointError('nonfinite retained state')
        return dict(steps_per_formation=n,snapshots=snaps,
                    constraint_defect=self.max_constraint,source_defect=self.max_source)

def discrepancy(a,b,key):
    aa=np.array([r[key] for r in a['snapshots']]);bb=np.array([r[key] for r in b['snapshots']])
    return float(np.max(np.max(abs(aa-bb),axis=0)/np.maximum(np.max(abs(bb),axis=0),1e-20)))

def main():
    started=time.monotonic()
    if OUT.exists():raise RuntimeError('no overwrite/duplicate worker')
    if sha(CAL)!=CALSHA:raise ValueError('changed calibration')
    cal=json.loads(CAL.read_text());saved=json.loads(base.SOURCE.read_text())
    for path in (Path(base.__file__),base.SOURCE):
        if sha(path)!=cal['hashes'][str(path)]:raise ValueError('changed constitutive source')
    saved['inherited']=cal['fixed'];model=base.Model(saved,1)
    checks=[];rows=[]
    def check(name,error,gate):checks.append(dict(name=name,error=float(error),gate=gate,passed=bool(error<=gate)))
    rot=np.array([[0.,-81.3],[81.3,0.]])
    exact=np.array([[math.cos(81.3),-math.sin(81.3)],[math.sin(81.3),math.cos(81.3)]])
    check('exponential_rotation',np.max(abs(expm(rot)-exact)),1e-10)
    nil=np.zeros((3,3));nil[0,1]=1.7;nil[1,2]=-.3
    check('exponential_nilpotent',np.max(abs(expm(nil)-(np.eye(3)+nil+nil@nil/2))),1e-10)
    rng=np.random.default_rng(179);mat=rng.normal(size=(7,7))*.01
    check('exponential_semigroup',np.max(abs(expm(mat)@expm(mat)-expm(2*mat))),1e-10)
    for width in (5.,20.):
        for cT in (0.,.01):
            histories=[]
            for n in (128,256,512):
                run=Response(model,width,cT);histories.append(run.integrate(n))
            label=f'{width}kpc_cT{cT}'
            check(label+'_state_refinement',discrepancy(histories[-2],histories[-1],'state'),1e-4)
            # chi is identically zero in cT=0; other near-zero histories retain a fixed floor.
            check(label+'_observable_refinement',discrepancy(histories[-2],histories[-1],'observables'),1e-4)
            check(label+'_Einstein_derivative',max(r['constraint_defect'] for r in histories),1e-9)
            check(label+'_source_conservation',max(r['source_defect'] for r in histories),1e-9)
            fine=histories[-1]['snapshots'];obs=np.array([r['observables'] for r in fine])
            row=dict(width_kpc=width,cTheta=cT,F=run.F,L_Hunit=run.L,k_Hunit=run.k,
                formation_time_Hunit=run.tf,ramp_delta_log_a=run.xf,
                state_scales=run.scale.tolist(),
                conditional_Gcos_over_GN=.98/run.F,background_H_ratio=1/math.sqrt(run.F),
                final=fine[-1],one_formation=fine[32],peak_abs_observables=np.max(abs(obs),axis=0).tolist(),
                maximum_physical_extrapolation={key:max(r['physical_depth_linear_extrapolation'][key] for r in fine)
                    for key in fine[0]['physical_depth_linear_extrapolation']},
                histories=histories)
            rows.append(row)
            print(json.dumps({k:v for k,v in row.items() if k not in ('histories','final','one_formation')}),flush=True)
    result=dict(protocol=__doc__,source_sha256=sha(Path(__file__)),calibration_sha256=CALSHA,
        dependencies={str(p):sha(p) for p in (Path(base.__file__),base.SOURCE)},
        fixed=model.p,proposed_cTheta=.01,source_physical_depth=DEPTH,actual_probe_depth=PROBE,
        observable_order=['Phi_over_probe','E_over_probe','relative_phase_over_probe','compression_chi_over_Hprobe'],
        scaled_state_order=['delta_m','varphi','alpha','Z','ordinary_delta','ordinary_theta'],
        time_label='log(a)/ramp_delta_log_a; not exact elapsed proper time/formation_time',
        rows=rows,controls=checks,all_controls_passed=all(r['passed'] for r in checks),
        elapsed_seconds=time.monotonic()-started)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(dict(all_controls_passed=result['all_controls_passed'],
        failed=[r for r in checks if not r['passed']],checks=len(checks),
        elapsed_seconds=result['elapsed_seconds'],result_sha256=sha(OUT)),indent=2))
    if not result['all_controls_passed']:raise SystemExit(1)

if __name__=='__main__':main()
