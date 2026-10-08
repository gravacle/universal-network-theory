"""V002 parity-regularized polar source pilot; NOT galaxy validation.

V001 pilot01 is retained as a NUMERICAL FAILURE: centre mass quadrature
interpolated R²rho across zero without factoring regular volume. V002
integrates even rho with the R² weight, integrates odd lapse gradients,
and tests the Hamiltonian through the regular variable mass/R³. It also
uses the independently reconstructed mass time tangent rather than a
precision-losing derivative of A approximately1. No physical law changes.

Same K(X), J, Q0=100 and eps=1e-6 cosmic calibration. New DECLARED ordinary
preparation: 5 kpc core, Gcos M/L=1e-7, Plummer times (1-(R/20L)^2)^4
inside20L; a Gaussian rest-density compensation of width300L, subtracted
from expanding ordinary background. Orbiting particles start on circular
orbits in the actual initial lapse; angular momentum is subsequently
advected, NOT retuned. Background particles are pressureless and expanding.
Both populations retain kinetic energy, canonical momentum and restweight.
The preparation is a source experiment, not a native galaxy-formation law.

All four canonical field equations, polar mass/lapse constraints, and
ordinary particle Hamiltonian are retained. Fourth-order physical-radius
derivatives on a sinh grid, cubic quadrature, RK4. No viscosity/filter,
charge clipping, fitted phase or held source. The centre has parity; outer
ghosts use polynomial extrapolation. Domain must outrun the measured cones
before this boundary is qualified. Cosmic initial data use the local polar
FLRW time shift through R^2; untested R^4 terms are approximation error.

Initial and trajectory Hamiltonian/momentum-flux/angular checks and
time/space/domain1e-3, inverse2e-12, positive inverse/clock/ordinary weights
are required BEFORE physics acceptance. A bounded pilot records cost and
failures; it is not a replacement for those gates. All tries exclusive.
No new physical coefficient fit; changed preparation freedoms are explicit.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import time
import numpy as np
import plane_canonical_evolution_v001 as inherited

BASE=Path(__file__).resolve().parent


class Polar(inherited.Model):
    def __init__(self, saved, n=160, extent=.012):
        super().__init__(saved,8)
        self.Q0=100.; self.mpref=6*self.OA/(self.Q0*self.eps*self.D)
        self.pcbar=6*self.OA*self.p['d0']/self.Q0
        self.L=.005*self.p['H0_km_s_Mpc']/299792.458
        self.kappa=1e-7; self.n=n; self.extent=extent
        self.dxgrid=math.asinh(extent/self.L)/n
        self.r=self.L*np.sinh((np.arange(n)+.5)*self.dxgrid)
        self.rg=self.L*np.sinh((np.arange(n+2)+.5)*self.dxgrid)
        self.tdyn=self.L/math.sqrt(self.kappa)
        self.mask=self.r<=10*self.L
        self.weights=[]
        for i in range(n):
            rr=np.array([(-self.rg[-j-1] if j<0 else self.rg[j]) for j in range(i-2,i+3)])
            sc=max(abs(rr-self.r[i])); xx=(rr-self.r[i])/sc
            mat=np.array([xx**k for k in range(5)])
            self.weights.append(np.linalg.solve(mat,np.array([0.,1.,0.,0.,0.]))/sc)
        self.weights=np.array(self.weights)
        self.massint=self.quadrature(1,2)
        self.lapseint=self.quadrature(-1,0)
        self.max_inverse=0.; self.min_inverse=1.; self.max_metric_iteration=0.
        self.bg0=self.bg(0.)
        self.Aguess=np.ones(n)

    def quadrature(self,parity,power):
        n=self.n; r=self.r; integ=np.zeros((n,n));running=np.zeros(n)
        gx,gw=np.polynomial.legendre.leggauss(4)
        for end in range(n):
            start=min(end-2,n-4);ids=np.arange(start,start+4)
            nodes=np.array([(-r[-j-1] if j<0 else r[j]) for j in ids])
            lo=0. if end==0 else r[end-1];hi=r[end]
            pts=(lo+hi)/2+(hi-lo)*gx/2
            for j in range(4):
                val=pts**power
                for k in range(4):
                    if k!=j:val=val*(pts-nodes[k])/(nodes[j]-nodes[k])
                idx=ids[j];sgn=parity if idx<0 else 1
                running[-idx-1 if idx<0 else idx]+=sgn*(hi-lo)*np.dot(gw,val)/2
            integ[end]=running
        return integ

    def derivative(self,f,parity=1):
        # Linear polynomial extrapolation operator of degree4, not a clamp.
        xx=self.r[-5:]; outer=[]
        for rt in self.rg[-2:]:
            val=0.
            for j in range(5):
                fac=1.
                for k in range(5):
                    if k!=j:fac*=(rt-xx[k])/(xx[j]-xx[k])
                val+=fac*f[-5+j]
            outer.append(val)
        ff=np.r_[parity*f[1::-1],f,outer]
        return np.sum(self.weights*np.lib.stride_tricks.sliding_window_view(ff,5),axis=1)

    def divergence(self,f):
        return self.derivative(f,-1)+2*f/self.r

    def fields(self,z,A):
        u,phir,Z,cp,ns,ps,ell,nb,pb=z
        ls2=ell*ell
        r=self.r; sig=u/A; c=np.sqrt(1+sig*sig); w=phir/A
        target=cp/A
        if np.any(target<=0):raise ValueError('nonpositive canonical scalar charge')
        s=target/(self.mpref*c)
        for _ in range(12):
            if np.any(s<0) or not np.all(np.isfinite(s)):raise ValueError('positive clock branch lost')
            X,m,d,K,dm,qr=self.constitutive(s)
            q=np.sqrt(X*X+w*w); Q=c*q+sig*w; p=sig*q+c*w
            e=(Z-self.C*p)/self.KB; rt=np.sqrt(p*p+self.bs*self.bs)
            j=self.lam*abs(p)/rt
            jt=self.lam*abs(p)*(p*p+2*self.bs*self.bs)/rt**3
            DD=self.C*(e-(1+j)*p)
            inverse=(q/X)*(d-(m/X)*w*w/(q*q)-self.C*sig*sig*X*X/(q*q)*(2/self.KB+jt))
            if np.any(inverse<=0):raise ValueError('nonpositive scalar inverse')
            res=m*q/X+sig*DD-target
            err=float(np.max(abs(res)/target))
            if err<1e-15:break
            s-=res/(inverse*self.Q0*self.eps/(2*qr*(1+s)**2))
        if err>2e-12:raise ValueError('scalar inverse residual')
        self.max_inverse=max(self.max_inverse,err)
        self.min_inverse=min(self.min_inverse,float(np.min(inverse/d)))
        jj=abs(p)/self.bs
        J=self.lam*self.bs**2*(jj*np.sqrt(1+jj*jj)-np.arcsinh(jj))
        small=jj<.01; ss=jj[small]
        J[small]=self.lam*self.bs**2*(2*ss**3/3-ss**5/5+3*ss**7/28-5*ss**9/72)
        cur=c*DD-(m/X)*w; divZ=self.divergence(Z)
        Ecal=self.KB*e*e+self.C*p*p+self.C*J-2*K
        rhoC=Ecal/2+target*q+c*divZ/A
        PC=-Ecal/2-sig*Q*DD/c-w*cur+sig*sig*divZ/(A*c)
        es=np.sqrt(1+ps*ps/A**2+ls2/r**2); eb=np.sqrt(1+pb*pb/A**2)
        rhoB=(ns*es+nb*eb)/A
        PrB=(ns*ps*ps/es+nb*pb*pb/eb)/A**3
        PtB=ns*ls2/(2*A*r*r*es)
        return locals()

    def geometry(self,t,z):
        A=self.Aguess.copy()
        for _ in range(10):
            g=self.fields(z,A)
            mass=self.massint@((g['rhoC']+g['rhoB'])/2)
            compact=2*mass/self.r
            if np.any(compact>=1):raise ValueError('trapped polar metric')
            newA=1/np.sqrt(1-compact)
            err=float(np.max(abs(newA-A)))
            A=newA
            if err<3e-15:break
        if err>1e-12:raise ValueError('metric iteration residual')
        self.max_metric_iteration=max(self.max_metric_iteration,err)
        g=self.fields(z,A); r=self.r
        ar=A*A*(r*(g['rhoC']+g['rhoB'])/2-mass/r**2)
        lapsegrad=A*A*(mass/r**2+r*(g['PC']+g['PrB'])/2)
        lnN=self.lapseint@lapsegrad
        # Coordinate normalization only: outer local polar cosmic lapse.
        _,_,_,_,_,H,hx,_=self.bg(t)
        lnN+=-.5*H*H*(1+hx)*r[-1]**2-lnN[-1]
        N=np.exp(lnN)
        self.Aguess=A
        g.update(A=A,mass=mass,ar=ar,g=lapsegrad,N=N,lnN=lnN)
        return g

    def initial(self):
        r=self.r; yy=r/self.L; shape=(1+yy*yy)**-2.5*np.maximum(1-(yy/20)**2,0)**4
        peak=2*self.kappa*self.L/(self.massint@shape)[-1]
        source=peak*shape
        comp=np.exp(-(r/(300*self.L))**2)
        comp*=((self.massint@source)[-1]/(self.massint@comp)[-1])
        # FLRW cosmic-time variation on a polar slice, through R^2.
        xc=-.5*r*r
        sb=np.empty(self.n); Xb=sb.copy(); mb=sb.copy(); Hb=sb.copy(); rhob=sb.copy()
        for i,xx in enumerate(xc):
            aa,s,X,m,K,H,hx,qq=self.bg(float(xx));sb[i]=s;Xb[i]=X;mb[i]=m;Hb[i]=H;rhob[i]=3*self.OB/aa**3
        if np.min(rhob-comp)<=0:raise ValueError('ordinary compensation removes too much mass')
        A=1/np.sqrt(1-r*r); ls2=np.zeros(self.n)
        for _ in range(15):
            sig=A*Hb*r; c=np.sqrt(1+sig*sig)
            z=np.array([A*sig,-A*Xb*sig,np.zeros(self.n),A*mb*c,
                        A*source,np.zeros(self.n),np.sqrt(ls2),A*(rhob-comp)*c,A*sig])
            g=self.geometry(0.,z); A=g['A']
            # Only occupied supported cells need circular angular momentum.
            ell=r**3*g['g']/(1-r*g['g'])
            ls2=np.where(source>0,ell,0.)
            if np.any(ls2<0):raise ValueError('unsupported circular initial core')
        self.source=source;self.comp=comp
        self.initial_peak=float(np.max(source));self.initial_z=z.copy()
        self.initial_g=g['g'].copy()
        return z

    def rhs(self,t,z,return_g=False):
        if not np.all(np.isfinite(z)):raise ValueError('nonfinite evolved state')
        g=self.geometry(t,z);r=self.r;A=g['A'];N=g['N'];ar=g['ar'];gg=g['g']
        u,phir,Z,cp,ns,ps,ell,nb,pb=z; ls2=ell*ell; sig=g['sig'];c=g['c']
        sr=(self.derivative(u,-1)-u*ar)/A
        out=np.zeros_like(z)
        out[0]=N*(A*g['e']-gg*c-sig*sr/c)
        # Avoid differentiating a large, almost spatially constant Q0.
        Xminus=self.Q0*self.eps*g['s']/((1+g['s'])*(g['qr']+1))
        qminus=Xminus+g['w']**2/(g['q']+g['X'])
        out[1]=N*(g['q']*gg+self.derivative(qminus))
        out[2]=N*(g['Q']*g['DD']/c-sig*g['divZ']/(A*c))
        out[3]=-N*(self.divergence(g['cur'])+gg*g['cur'])
        for ni,pi,ei,li in ((4,5,g['es'],ls2),(7,8,g['eb'],np.zeros(self.n))):
            nn=z[ni];pp=z[pi];v=N*pp/(A*A*ei)
            out[ni]=-self.divergence(nn*v)
            out[pi]=-v*self.derivative(pp,-1)-N*gg*ei+N/ei*(pp*pp*ar/(A*A)+li/r**3)
            if ni==4:out[6]=-v*self.derivative(ell)
        return (out,g) if return_g else out

    def diagnose(self,t,z):
        dz,g=self.rhs(t,z,True);r=self.r;A=g['A'];N=g['N'];mask=self.mask
        mr3=g['mass']/r**3
        ham=6*mr3+2*r*self.derivative(mr3)-g['rhoC']-g['rhoB']
        # Independent normal-vector expansion: 1/(N A R²)[d_t(A R² c)+d_R(NR²sigma)].
        adot=N*(-z[0]*g['divZ']+z[3]*z[1]-z[4]*z[5]-z[7]*z[8])*r/(2*A)
        sigdot=dz[0]/A-g['sig']*adot
        theta=(adot*g['c']+g['sig']*sigdot/g['c'])/N+(self.divergence(g['sig'])+g['g']*g['sig'])/A
        # Metric flux will be checked against an independent time tangent.
        tt=1e-9*self.tdyn; oldguess=self.Aguess.copy()
        gp=self.geometry(t+tt,z+tt*dz);gm=self.geometry(t-tt,z-tt*dz)
        flux_numeric=A*A*(gp['mass']-gm['mass'])/(2*tt*r)
        self.Aguess=oldguess
        fluxscale=max(float(np.max(abs(adot[mask]))),self.kappa/self.tdyn,1e-12)
        vs=N*z[5]/(A*A*g['es'])
        grav=N*N*g['g']/A**2
        return dict(t=t,t_over_tdyn=t/self.tdyn,
            Hamiltonian_source_normalized=float(np.max(abs(ham[mask]))/self.initial_peak),
            flux_tangent_normalized=float(np.max(abs(flux_numeric[mask]-adot[mask])))/fluxscale,
            max_tilt=float(np.max(abs(g['sig'][mask]))),min_inverse_fraction=float(np.min(g['inverse']/g['d'])),
            min_clock_s=float(np.min(g['s'])),max_JY=float(np.max(g['j'][mask])),
            min_background_restweight=float(np.min(z[7])),min_supported_weight=float(np.min(z[4])),
            max_characteristic_rest_speed=float(np.max(np.sqrt((2*self.C/self.KB+g['m']/g['X'])/g['d']))),
            central_expansion_estimate=float(theta[0]),central_current_slope=float(g['DD'][0]/r[0]),
            supported_radial_speed=float(np.max(abs(vs[mask]))),
            state=z[:,mask].tolist(),r=r[mask].tolist(),gravity=grav[mask].tolist(),
            mass=float(g['mass'][-1]),A_inner=A[mask].tolist(),theta=theta[mask].tolist())


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--nodes',type=int,default=160)
    ap.add_argument('--steps',type=int,default=128);ap.add_argument('--dt-factor',type=float,default=.1)
    ap.add_argument('--extent',type=float,default=.012);ap.add_argument('--tag',required=True)
    ap.add_argument('--wall-seconds',type=float,default=45.)
    args=ap.parse_args();out=BASE/('INVARIANT_CLOCK_POLAR_SOURCE_'+args.tag+'_RESULT.json')
    if out.exists():raise FileExistsError(out)
    np.seterr(over='raise',invalid='raise',divide='raise')
    saved=json.loads(inherited.SOURCE.read_text());beg=time.monotonic()
    m=Polar(saved,args.nodes,args.extent);snaps=[];error=None;step=0;z=None
    dt=args.dt_factor*(m.r[1]-m.r[0]);reason='requested_steps'
    try:
        z=m.initial();snaps.append(m.diagnose(0.,z))
        for step in range(1,args.steps+1):
            t=(step-1)*dt
            aa=m.rhs(t,z);bb=m.rhs(t+dt/2,z+aa*dt/2)
            cc=m.rhs(t+dt/2,z+bb*dt/2);dd=m.rhs(t+dt,z+cc*dt)
            z+=dt*(aa+2*bb+2*cc+dd)/6
            if step%128==0:
                if time.monotonic()-beg>args.wall_seconds:
                    reason='bounded_wall_budget';break
        snaps.append(m.diagnose(step*dt,z))
    except (ValueError,FloatingPointError,OverflowError) as exc:
        error=f'{type(exc).__name__}: {exc}';reason='failure'
    result=dict(protocol=__doc__,args=vars(args),self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        dependency_sha256=hashlib.sha256((BASE/'plane_canonical_evolution_v001.py').read_bytes()).hexdigest(),
        input_sha256=hashlib.sha256(inherited.SOURCE.read_bytes()).hexdigest(),
        reason=reason,error=error,steps=step,dt=dt,t_over_tdyn=step*dt/m.tdyn,
        elapsed_seconds=time.monotonic()-beg,max_inverse=m.max_inverse,min_inverse=m.min_inverse,
        metric_iteration=m.max_metric_iteration,snapshots=snaps,
        scope='pilot only; refinement/angular/domain controls incomplete; no physical acceptance')
    with out.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps({k:v for k,v in result.items() if k not in ('protocol','snapshots')},allow_nan=False),flush=True)


if __name__=='__main__':main()
