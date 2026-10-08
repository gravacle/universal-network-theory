"""Time-dependent compact ordinary source in the provisional K(X) action.

Frozen physical preparation: ai=1,Q0/H0=100,kappa=Gcos M/(ai L)=1e-7,
ai L=5 kpc, exact Plummer conformal CMC data, uniform initial clock X,
zero initial tilt/spatial phase/electric field, expanding comoving dust.
Same calibrated cosmological constants and J as the transfer calculation.
No halo, held mass after initialization, imposed force, clock profile fit,
constraint projection, dissipation, or claimed native formation history.

The duration is ten initial material sound crossing times of L. This is
a short source-response experiment, not equilibration/galaxy validation.
Core observations r/L=.5,1,2,5,10. Preserve analytic 1/r initial metric
tail at outer ghosts. Its time development is an approximate boundary:
run 50L and 80L domains, retain a margin to all signals with speed<=1,
and separately monitor material speed; no claim for untested faster cones.

Uniform radial cell centers, fourth-order centered derivatives with even
metric/scalar and odd radial vector parity. RK4 in ln(background a).
Serial rows (N,rmax/L,steps)=(512,50,2048),(1024,50,4096),
(1024,50,8192),(1638,80,6552). Compare interpolated full inner 10L states
with per-field amplitude floors1e-14, not just five selected radii.
Frozen gates: fine temporal/state and spatial/state and domain/state1e-3;
Hamiltonian relative to max initial compact density1e-3; momentum relative
to max canonical-term scale or kappa/L1e-3; homogeneous RHS1e-10;
initial acceleration normalized to max initial inward force1e-3;
inverse relative residual2e-12 and positive inverse derivative; positive
X branch, volume, R_r, finite state. A failed numerical gate is NOT a
physical exclusion. Store every attempted row and halt on branch loss.
Charge flux drift is reported as a control diagnostic; radial centered
derivatives are not a finite-volume scheme, so not an exact discrete
conservation theorem. No parameter fit, observational likelihood, or local
GN recalibration occurs. All output booleans converted before JSON.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import plane_canonical_evolution_v001 as inherited

BASE=Path(__file__).resolve().parent
OUT=BASE/'INVARIANT_CLOCK_SPHERICAL_SOURCE_V001_RESULT.json'


class Model(inherited.Model):
    def __init__(self,saved,N=512,extent=50.,homogeneous=False):
        super().__init__(saved,8)
        self.N=N; self.Q0=100.
        self.mpref=6*self.OA/(self.Q0*self.eps*self.D)
        self.pcbar=6*self.OA*self.p['d0']/self.Q0
        self.L=.005*self.p['H0_km_s_Mpc']/299792.458
        self.kappa=0. if homogeneous else 1e-7
        self.tlam=self.kappa/(1+math.sqrt(1+3*math.pi*self.kappa/8))
        self.extent=extent;self.dr=extent*self.L/N
        self.r=(np.arange(N)+.5)*self.dr
        self.rghost=(N+np.arange(2)+.5)*self.dr
        self.lp=np.log1p(self.tlam/np.sqrt(1+(self.r/self.L)**2))
        self.lpg=np.log1p(self.tlam/np.sqrt(1+(self.rghost/self.L)**2))
        self.tail=np.zeros((8,2));self.tail[0:2]=2*self.lpg
        self.tail[[4,5,7]]=np.expm1(6*self.lpg)
        psi=np.exp(self.lp)
        self.excess=12*self.tlam/self.L**2/(1+(self.r/self.L)**2)**2.5/psi**5
        self.dust_weight=psi**6*(3*self.OB+self.excess)
        self.piT=2*self.r**2*self.dust_weight
        a,s,Q,m,K,h,hx,q=self.bg(0.)
        d=self.constitutive(s)[2]
        self.sound=math.sqrt((2*self.C/self.KB+m/Q)/d)
        self.end_x=10*self.L/self.sound
        self.mask=self.r<=10*self.L
        self.max_inverse=0.;self.min_schur_fraction=1.

    def initial(self,homogeneous=False):
        z=np.zeros((8,self.N));z[0:2]=2*self.lp
        z[[4,5,7]]=np.expm1(6*self.lp)
        return z

    def deriv(self,f,parity=1,outer=None,order=1):
        if outer is None:
            # Polynomial extrapolation is used only for derived fluxes;
            # primitive fields use the explicitly frozen analytic tail.
            outer=np.array([5*f[-1]-10*f[-2]+10*f[-3]-5*f[-4]+f[-5],
                            15*f[-1]-40*f[-2]+45*f[-3]-24*f[-4]+5*f[-5]])
        p=np.concatenate((parity*f[1::-1],f,outer))
        if order==1:return (p[:-4]-8*p[1:-3]+8*p[3:-1]-p[4:])/(12*self.dr)
        return (-p[:-4]+16*p[1:-3]-30*p[2:-2]+16*p[3:-1]-p[4:])/(12*self.dr**2)

    def unpack(self,x,z):
        if not np.all(np.isfinite(z)):raise ValueError('nonfinite state')
        abar,sbar,Xbar,mbar,Kbar,h,hx,qbar=self.bg(x)
        fa,fb,un,phase,pa,pb,pu,pc=z;r=self.r
        v=fa+2*fb;ev=np.exp(v);A=abar*np.exp(fa);R=abar*r*np.exp(fb);V=A*R*R
        pia=-4*abar**3*r*r*h*(1+pa);pib=-8*abar**3*r*r*h*(1+pb)
        piu=2*abar**2*r*r*pu;piph=self.pcbar*r*r*(1+pc)
        ax=self.deriv(fa,outer=self.tail[0]);bx=self.deriv(fb,outer=self.tail[1])
        bxx=self.deriv(fb,outer=self.tail[1],order=2)
        phir=self.deriv(phase,outer=np.zeros(2));w=phir/A
        sig=un*np.exp(-fa);c=np.sqrt(1+sig*sig);Z=pu*np.exp(-2*fb)
        target=piph/(2*V)
        if np.any(target<=0):raise ValueError('nonpositive slice charge')
        s=target/self.mpref
        for it in range(12):
            if np.any(s<0) or np.any(~np.isfinite(s)):raise ValueError('positive X branch lost')
            X,m,d,Kfun,dm,qroot=self.constitutive(s)
            q=np.sqrt(X*X+w*w);Q=c*q+sig*w;p=sig*q+c*w
            e=(Z-self.C*p)/self.KB;root=np.sqrt(p*p+self.bs**2)
            j=self.lam*abs(p)/root
            jt=self.lam*abs(p)*(p*p+2*self.bs**2)/root**3
            Dgeo=self.C*(e-(1+j)*p)
            schur=(q/X)*(d-(m/X)*w*w/(q*q)-self.C*sig*sig*X*X/(q*q)*(2/self.KB+jt))
            if np.any(schur<=0):raise ValueError('nonpositive inverse derivative')
            resid=m*q/X+sig*Dgeo-target
            err=float(np.max(abs(resid)/target))
            if err<8e-16:break
            s-=resid/(schur*self.Q0*self.eps/(2*qroot*(1+s)**2))
        self.max_inverse=max(self.max_inverse,err)
        self.min_schur_fraction=min(self.min_schur_fraction,float(np.min(schur/d)))
        if err>2e-12:raise ValueError('inverse residual gate')
        zz=abs(p)/self.bs
        J=self.lam*self.bs**2*(zz*np.sqrt(1+zz*zz)-np.arcsinh(zz))
        small=zz<.01;t=zz[small]
        J[small]=self.lam*self.bs**2*(2*t**3/3-t**5/5+3*t**7/28-5*t**9/72)
        qdiff=self.Q0*self.eps*(s-sbar)/((1+s)*(1+sbar)*(qroot+qbar))+w*w/(q+X)
        S=Q*Dgeo;cur=c*Dgeo-(m/X)*w
        pur=self.deriv(pu,parity=-1,outer=np.zeros(2));piur=2*abar**2*r*r*(pur+2*pu/r)
        F=np.exp(fb-fa)*(1+r*bx)
        omF2=-np.expm1(2*(fb-fa)+2*np.log1p(r*bx))
        Fr=F*(bx-ax+(bx+r*bxx)/(1+r*bx))
        R3=2*omF2/R**2-4*Fr/(A*R)
        curvA=2*A*omF2;curvB=-4*R*Fr
        Lvec=self.KB*e*e+2*self.C*e*p-self.C*p*p-self.C*J
        kin=pia*(pia-2*pib)/(8*V)
        return locals()

    def rhs(self,x,z,return_g=False):
        g=self.unpack(x,z);a=g['abar'];h=g['h'];V=g['V'];r=self.r
        A=g['A'];sig=g['sig'];c=g['c'];cur=g['cur'];S=g['S']
        pa=z[4];pb=z[5];v=g['v'];ev=g['ev'];inv=np.exp(-v)
        nA=g['curvA']+V*(g['Lvec']-2*g['Z']*g['e']-2*(sig*S/c+g['w']*cur))+sig*sig*g['piur']/c
        nB=g['curvB']+2*V*g['Lvec']
        sd=g['s']-g['sbar'];dK=3*self.OA/self.D*(np.log1p(sd/(1+g['sbar']))-sd/((1+g['s'])*(1+g['sbar'])))
        kA=(g['Kbar']*(pa-np.expm1(v))-ev*dK)/(2*h*h)
        kB=(g['Kbar']*(pb-np.expm1(v))-ev*dK)/(2*h*h)
        shared=1.5*(1+pa)*np.expm1(-v)+.5*inv*(1+pa)*(4*pb-pa)
        out=np.empty_like(z)
        out[0]=np.expm1(-v)+inv*(2*pb-pa)
        out[1]=np.expm1(-v)+inv*pa
        sr=np.exp(-z[0])*(self.deriv(z[2],parity=-1,outer=np.zeros(2))-z[2]*g['ax'])
        out[2]=(A*g['e']-sig*sr/c)/(a*h)-z[2]
        out[3]=g['qdiff']/h
        out[4]=shared+kA+nA/(-4*a**3*r*r*h*h)
        out[5]=shared+1.5*(pa-pb)+kB+nB/(-8*a**3*r*r*h*h)
        out[6]=np.exp(2*z[1])*S/(c*h)-sig*(g['pur']+2*z[6]/r)/(A*c*h)-2*z[6]
        out[7]=-2*a*a*np.exp(2*z[1])/(self.pcbar*h)*(self.deriv(cur,parity=-1)+(2*g['bx']+2/r)*cur)
        return (out,g) if return_g else out

    def diagnose(self,x,z):
        dz,g=self.rhs(x,z,True);h=g['h'];a=g['abar'];r=self.r;V=g['V'];mask=self.mask
        HH=g['kin']/V-g['R3']+self.KB*g['e']**2+self.C*g['p']**2+self.C*g['J']-2*g['Kfun']+g['piph']*g['q']/V+g['c']*g['piur']/V+self.piT/V
        terms=np.array([self.deriv(z[4],outer=self.tail[4]),-(1+z[4])*g['ax'],
            -2*(1+z[5])*g['bx'],2*(z[4]-z[5])/r,
            -z[2]*(g['pur']+2*z[6]/r)/(2*h),self.pcbar*(1+z[7])*g['phir']/(4*a**3*h)])
        DD=terms.sum(axis=0);dscale=max(float(np.max(abs(terms[:,mask]))),max(self.kappa,1e-30)/self.L)
        inv=np.exp(-g['v']);l=h*inv*(1+z[4]);k=h*inv*(1+2*z[5]-z[4])
        piadot=-4*a**3*r*r*h*h*(dz[4]+(1+z[4])*(3+g['hx']))
        acc=(-piadot/(4*V)-l*(k+l))*g['R']
        bgacc=h*h*(1+g['hx'])*g['R'];inward=bgacc-acc
        # Exact log F form avoids subtracting nearly equal metric factors.
        y=r/self.L;u=-2*self.tlam*y*y/(1+y*y)**1.5/np.exp(self.lp)
        initialg=-np.expm1(2*np.log1p(u))/(2*np.exp(2*self.lp)*r)
        sample=[]
        for rr in (.5,1.,2.,5.,10.):
            at=lambda f:float(np.interp(rr*self.L,r,f))
            sample.append(dict(r_over_L=rr,R=at(g['R']),inward=at(inward),initial_inward=at(initialg),
                acceleration_ratio_to_initial=at(inward)/at(initialg),tilt=at(g['sig']),JY=at(g['j']),
                clock_s=at(g['s']),dust_density=at(self.piT/(2*V)),clock_current=at(g['cur'])))
        return dict(x=x,a=a,Hamiltonian_source_normalized=float(np.max(abs(HH[mask]))/max(2*np.max(self.excess),6*h*h)),
            momentum_normalized=float(np.max(abs(DD[mask]))/dscale),
            initial_acceleration_error=float(np.max(abs(inward[mask]-initialg[mask]))/max(np.max(abs(initialg)),1e-30)),
            minimum_inverse_fraction=float(np.min(g['schur']/g['d'])),min_s=float(np.min(g['s'])),
            max_tilt=float(np.max(abs(g['sig'][mask]))),max_JY=float(np.max(g['j'][mask])),
            min_Rr_over_A=float(np.min(g['F'])),samples=sample,
            material_max_speed=float(np.max(np.sqrt((2*self.C/self.KB+g['m']/g['X'])/g['d']))),
            charge_excess_integral=float(self.pcbar*np.sum(r*r*(z[7]-self.initial()[7]))*self.dr),
            outer_charge_flux=float(2*g['R'][-1]**2*g['cur'][-1]),state=z[:,mask].tolist(),radial_centers=r[mask].tolist())


def integrate(saved,N,extent,steps):
    m=Model(saved,N,extent);z=m.initial();dx=m.end_x/steps;snaps=[];err=None
    hom=Model(saved,32,extent,True);homerr=float(np.max(abs(hom.rhs(0.,hom.initial()))))
    last_i=0
    for i in range(steps+1):
        last_i=i;x=i*dx
        try:
            if i%(steps//16)==0 or i==steps:snaps.append(m.diagnose(x,z))
            if i==steps:break
            aa=m.rhs(x,z);bb=m.rhs(x+dx/2,z+dx*aa/2)
            cc=m.rhs(x+dx/2,z+dx*bb/2);dd=m.rhs(x+dx,z+dx*cc)
            z+=dx*(aa+2*bb+2*cc+dd)/6
        except (ValueError,FloatingPointError,OverflowError) as exc:
            err=f'{type(exc).__name__}: {exc}';break
    return dict(N=N,extent=extent,steps=steps,last_step=last_i,completed=err is None,error=err,
        homogeneous_rhs=homerr,snapshots=snaps,max_inverse=m.max_inverse,min_inverse_fraction=m.min_schur_fraction,
        L=m.L,end_x=m.end_x,sound=m.sound,maximum_dt_over_dr=dx/m.dr)


def compare(a,b):
    if not a['completed'] or not b['completed']:return None
    # Last state only; intermediate snapshots need not share exact times.
    sa=a['snapshots'][-1];sb=b['snapshots'][-1]
    ra=np.array(sa['radial_centers']);rb=np.array(sb['radial_centers']);za=np.array(sa['state']);zb=np.array(sb['state'])
    mask=(rb>=ra[1])&(rb<=ra[-2]);rb=rb[mask];zb=zb[:,mask]
    idx=np.clip(np.searchsorted(ra,rb)-1,1,len(ra)-3)
    interp=np.zeros_like(zb)
    for j in range(-1,3):
        w=np.ones(len(rb))
        for k in range(-1,3):
            if k!=j:w*=(rb-ra[idx+k])/(ra[idx+j]-ra[idx+k])
        interp+=za[:,idx+j]*w
    scale=np.maximum(np.max(abs(zb),axis=1),1e-14)
    values=np.max(abs(zb-interp),axis=1)/scale
    return dict(maximum=float(np.max(values)),per_variable=values.tolist())


def main():
    np.seterr(over='raise',invalid='raise',divide='raise');beg=time.monotonic()
    saved=json.loads(inherited.SOURCE.read_text());rows=[]
    for N,extent,steps in ((512,50.,2048),(1024,50.,4096),(1024,50.,8192),(1638,80.,6552)):
        row=integrate(saved,N,extent,steps);rows.append(row)
        print(json.dumps({k:v for k,v in row.items() if k!='snapshots'},default=lambda x:x.item()),flush=True)
    rr=dict(space=compare(rows[0],rows[1]),time=compare(rows[1],rows[2]),domain=compare(rows[1],rows[3]))
    samples=[s for row in rows for s in row['snapshots']]
    checks=dict(completed=all(r['completed'] for r in rows),homogeneous=max(r['homogeneous_rhs'] for r in rows)<=1e-10,
        initial_acceleration=max(r['snapshots'][0]['initial_acceleration_error'] for r in rows)<=1e-3,
        Hamiltonian=max(s['Hamiltonian_source_normalized'] for s in samples)<=1e-3,
        momentum=max(s['momentum_normalized'] for s in samples)<=1e-3,
        inverse=max(r['max_inverse'] for r in rows)<=2e-12,positive_Rr=all(s['min_Rr_over_A']>0 for s in samples),
        refinement=all(v is not None and v['maximum']<=1e-3 for v in rr.values()))
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        dependency_sha256=hashlib.sha256((BASE/'plane_canonical_evolution_v001.py').read_bytes()).hexdigest(),
        input_sha256=hashlib.sha256(inherited.SOURCE.read_bytes()).hexdigest(),rows=rows,refinement=rr,
        controls={k:bool(v) for k,v in checks.items()},all_controls_passed=bool(all(checks.values())),elapsed_seconds=time.monotonic()-beg)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False,default=lambda x:x.item());f.write('\n')
    print(json.dumps(dict(refinement=rr,controls=result['controls'],elapsed_seconds=result['elapsed_seconds'])),flush=True)


if __name__=='__main__':main()
