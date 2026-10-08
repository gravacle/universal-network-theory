"""Restricted stationary through-flow in a PRESCRIBED planar lapse well.

Not an Einstein solution, star, native preparation or preferred-frame test.
Same calibrated action; fixed Gaussian log lapse -depth exp(-xi²), A=1,
xi=z/ell in [-8,8]. Depth=log(1+638/c); ell=695700km Hunit/c is an
ILLUSTRATIVE length, not a solar potential profile. Gaussian plane is not
claimed to be a positive ordinary-density solution. Two prescribed incident
tilts -.001 and -.0001 are extra preparation choices, NOT fitted velocities.
Start at xi=8, integrate toward -8 along the negative flow; phi=omega t+psi.
omega=Xbar cinf and NJ=mbar sigma_inf fixed. No downstream reset.

Evolve E=Nc-cinf and Z, retaining tiny E explicitly. E_xi=ell N e,
Z_xi=ell Q D/sigma, exact algebraic current determines p. Stable X²-Xbar²
prevents cancellation of a ~1e-10 displacement beneath Xbar~100.
RK4 512/1024 steps; save129 common points. Frozen gates: current1e-11,
algebra1e-12, inverse analytic-vs-finite derivative1e-6, common-point
refinement1e-5 per field amplitude with stated floors, integrated
derivative residual1e-3 (fourth-order sample derivative, interior only).
Positive branch/cap/current inverse are necessary screens, not stability.
Field stress/flux relative to imposed curvature are approximation screens,
not solved gravitational constraints. Nonzero downstream Z is retained.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import plane_canonical_evolution_v001 as base

BASE=Path(__file__).resolve().parent
CAL=BASE/'INVARIANT_CLOCK_CMB_CALIBRATION_V001_RESULT.json'
OUT=BASE/'INVARIANT_CLOCK_PLANAR_THROUGHFLOW_V001_RESULT.json'


class Flow:
    def __init__(self,model,tilt):
        self.m=model;self.tilt=tilt;self.cinf=math.sqrt(1+tilt*tilt)
        _,self.sb,self.Xb,self.mb,self.Kb,*_=model.bg(0.)
        self.fb=self.sb/(1+self.sb);self.Jinf=self.mb*tilt
        self.depth=math.log1p(638./299792458.)
        self.ell=695700.*model.p['H0_km_s_Mpc']/3.085677581491367e19/299792.458
        self.max_current=0.;self.max_algebra=0.;self.min_inverse=math.inf
        self.min_f=math.inf;self.max_f=-math.inf

    def algebra(self,xi,state,p,track=False):
        m=self.m;E,Z=state;lnN=-self.depth*math.exp(-xi*xi);N=math.exp(lnN)
        cc=(self.cinf+E)/N;v=E/self.cinf
        sig=-math.sqrt(self.tilt*self.tilt-math.expm1(2*lnN)+2*self.cinf*E+E*E)/N
        qc=self.Xb/(1+v);q=qc*cc
        dx2=-self.Xb**2*v*(2+v)/(1+v)**2+2*sig*qc*p/cc-p*p/(cc*cc)
        ff=self.fb+dx2/(m.Q0*m.Q0*m.eps)
        if not 0<ff<1:raise ValueError('clock branch left')
        ss=ff/(1-ff);X,charge,dd,K,dm,qr=m.constitutive(ss)
        w=p/cc-sig*qc;Q=(q+sig*p)/cc
        rt=math.sqrt(p*p+m.bs*m.bs);jj=m.lam*abs(p)/rt
        jt=m.lam*abs(p)*(p*p+2*m.bs*m.bs)/rt**3
        ee=(Z-m.C*p)/m.KB;D=m.C*(ee-(1+jj)*p)
        F=cc*D-charge*w/X-self.Jinf/N
        dfdp=2*(sig*qc/cc-p/cc**2)/(m.Q0*m.Q0*m.eps)
        dXdp=(sig*qc/cc-p/cc**2)/X
        dmdp=dm*dfdp/(1-ff)**2
        Fp=-cc*m.C*(2/m.KB+jt)-dmdp*w/X-charge/(cc*X)+charge*w*dXdp/X**2
        if Fp>=0:raise ValueError('current inverse lost')
        # Stable cubic J for the tiny p/bs regime used here.
        zz=abs(p)/m.bs
        if zz>.01:raise ValueError('series regime left')
        Jfun=m.lam*m.bs**2*(2*zz**3/3-zz**5/5+3*zz**7/28-5*zz**9/72)
        Ecal=m.KB*ee*ee+m.C*p*p+m.C*Jfun-2*K
        M=charge*q/X+sig*D;Zprime=Q*D/sig
        rho=Ecal/2+M*q+cc*Zprime
        P=-Ecal/2-sig*Q*D/cc-w*(self.Jinf/N)+sig*sig*Zprime/cc
        flux=sig*Zprime-M*w;expected_flux=q*self.Jinf/N
        identity=max(abs(cc*cc-sig*sig-1),abs((q*q-w*w-X*X)/(X*X)),
                     abs(flux-expected_flux)/max(abs(expected_flux),1e-30))
        if track:
            self.max_current=max(self.max_current,abs(F)/abs(self.Jinf/N))
            self.max_algebra=max(self.max_algebra,identity)
            self.min_inverse=min(self.min_inverse,-Fp)
            self.min_f=min(self.min_f,ff);self.max_f=max(self.max_f,ff)
        return dict(N=N,c=cc,sigma=sig,p=p,X=X,X_minus_Xbar=dx2/(X+self.Xb),
            s=ss,m=charge,Q=Q,w=w,q=q,e=ee,D=D,F=F,Fp=Fp,Zprime=Zprime,
            rho=rho,P=P,flux=flux,E=E,Z=Z,branch_fraction=ff,identity=identity)

    def solve(self,xi,state):
        p=0.
        for _ in range(10):
            a=self.algebra(xi,state,p)
            if abs(a['F'])<1e-14*abs(self.Jinf):break
            p-=a['F']/a['Fp']
        a=self.algebra(xi,state,p,True)
        if abs(a['F'])>1e-11*abs(self.Jinf):raise ValueError('current inverse residual')
        return a

    def rhs(self,xi,state):
        a=self.solve(xi,state)
        return self.ell*np.array([a['N']*a['e'],a['Zprime']])

    def integrate(self,n):
        y=np.zeros(2);h=-16/n;snaps=[]
        for i in range(n+1):
            x=8+i*h
            if i%(n//128)==0:
                a=self.solve(x,y);a['xi']=x;snaps.append(a)
            if i==n:break
            k1=self.rhs(x,y);k2=self.rhs(x+h/2,y+h*k1/2)
            k3=self.rhs(x+h/2,y+h*k2/2);k4=self.rhs(x+h,y+h*k3)
            y+=h*(k1+2*k2+2*k3+k4)/6
        return dict(steps=n,snapshots=snaps)


def main():
    if OUT.exists():raise FileExistsError(OUT)
    t=time.monotonic();cal=json.loads(CAL.read_text());seed=json.loads(base.SOURCE.read_text())
    seed['inherited']['Q0_over_H0']=100.;seed['inherited']['H0_km_s_Mpc']=cal['selected_Hunit']
    m=base.Model(seed,1);rows=[];controls=[]
    def gate(name,value,tol):controls.append(dict(name=name,error=float(value),tolerance=tol,passed=bool(value<=tol)))
    for tilt in (-.001,-.0001):
        flow=Flow(m,tilt);coarse=flow.integrate(512);fine=flow.integrate(1024)
        z=fine['snapshots'];prefix=str(tilt)
        for key,floor in (('E',1e-40),('Z',1e-40),('p',1e-24),('X_minus_Xbar',1e-30),('D',1e-24)):
            aa=np.array([v[key] for v in coarse['snapshots']]);bb=np.array([v[key] for v in z])
            gate(prefix+'_refinement_'+key,max(abs(aa-bb))/max(max(abs(bb)),floor),1e-5)
        gate(prefix+'_current',flow.max_current,1e-11)
        gate(prefix+'_algebra',flow.max_algebra,1e-12)
        for i in (32,64,96):
            a=z[i];hh=1e-9;state=[a['E'],a['Z']]
            fd=(flow.algebra(a['xi'],state,a['p']+hh)['F']-flow.algebra(a['xi'],state,a['p']-hh)['F'])/(2*hh)
            gate(prefix+'_inverse_derivative_'+str(i),abs(fd/a['Fp']-1),1e-6)
        # Independent sampled differentiation of accumulated states.
        dx=z[1]['xi']-z[0]['xi']
        for key,which in (('E',0),('Z',1)):
            ar=np.array([a[key] for a in z]);der=(ar[:-4]-8*ar[1:-3]+8*ar[3:-1]-ar[4:])/(12*dx)
            rr=np.array([flow.rhs(a['xi'],[a['E'],a['Z']])[which] for a in z[2:-2]])
            gate(prefix+'_ode_sample_'+key,max(abs(der-rr))/max(max(abs(rr)),1e-40),1e-3)
        mid=z[64];rho0=z[0]['rho'];p0=z[0]['P']
        summary=dict(tilt=tilt,ell_Hunit=flow.ell,depth=flow.depth,
            max_X_displacement=max(abs(a['X_minus_Xbar']) for a in z),
            min_current_inverse=flow.min_inverse,branch_fraction_range=[flow.min_f,flow.max_f],
            max_E=max(abs(a['E']) for a in z),max_Z=max(abs(a['Z']) for a in z),
            downstream_E=z[-1]['E'],downstream_Z=z[-1]['Z'],center=mid,
            local_stress_to_imposed_curvature=max(max(abs(a['rho']-rho0),abs(a['P']-p0)) for a in z)*flow.ell**2/flow.depth,
            total_flux_to_imposed_curvature=max(abs(a['flux']) for a in z)*flow.ell**2/flow.depth,
            uniform_E_bound=16*flow.ell*max(abs(a['N']*a['e']) for a in z),
            uniform_Z_bound=16*flow.ell*max(abs(a['Zprime']) for a in z))
        rows.append(dict(summary=summary,coarse=coarse,fine=fine))
    result=dict(protocol=__doc__,fixed=m.p,additional_fitted_freedoms=0,
        extra_prescribed_preparation='one incoming tilt, two illustrative values; not selected by network',
        rows=rows,controls=controls,all_numerical_controls_passed=all(c['passed'] for c in controls),
        hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),CAL,base.SOURCE,Path(base.__file__))},
        elapsed_seconds=time.monotonic()-t)
    with OUT.open('x') as stream:json.dump(result,stream,indent=2,allow_nan=False)
    print(json.dumps(dict(all_numerical_controls_passed=result['all_numerical_controls_passed'],
        summaries=[r['summary'] for r in rows],controls=controls,elapsed_seconds=result['elapsed_seconds'])),flush=True)


if __name__=='__main__':main()
