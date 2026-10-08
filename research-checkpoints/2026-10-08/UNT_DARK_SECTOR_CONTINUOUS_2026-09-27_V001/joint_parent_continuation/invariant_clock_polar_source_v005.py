"""Mixed-p discretization of the SAME polar source continuum equations.

V004's failed160/320 clock/current grid comparison is retained. On the
same saved states, the numerical q_R chain-rule defect decreases by15.29
under doubled spatial resolution but is substantial relative to the small
p response. This targets that specific numerical defect, not a new law.

Evolve physical p=sigma*q+c*w instead of phi_R. With Q=sqrt(X²+p²),
q=cQ-sigma*p,w=c*p-sigma*Q, solve M=mq/X+sigmaD at fixed p using M_X.
The coupled time update uses the separate fixed-w Schur. Its exact lapse
gradient cancellation is independently reviewed. No clock clipping, new
phase choice, fitted tolerance or charge/ordinary-source alteration.
Primitive integrability is independently reconstructed and compared with
the original canonical equation. All previous numerical gates remain.
This representation does not itself establish regularity or convergence.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import time
import numpy as np
import invariant_clock_polar_source_v004 as src

prev=src.prev
BASE=Path(__file__).resolve().parent


class Polar(src.Polar):
    canonical_mode=False

    def initial(self):
        self.canonical_mode=True
        z=super().initial()
        self.canonical_mode=False
        # Exact declared initial p=0, rather than subtraction roundoff.
        z[1]=0.
        self.initial_z=z.copy()
        return z

    def fields(self,z,A):
        if self.canonical_mode:return prev.Polar.fields(self,z,A)
        u,p,Z,cp,ns,ps,ell,nb,pb=z;ls2=ell*ell;r=self.r
        sig=u/A;c=np.sqrt(1+sig*sig);target=cp/A
        rt=np.sqrt(p*p+self.bs*self.bs);j=self.lam*abs(p)/rt
        jt=self.lam*abs(p)*(p*p+2*self.bs*self.bs)/rt**3
        e=(Z-self.C*p)/self.KB;DD=self.C*(e-(1+j)*p)
        if np.any(target-sig*DD<=0):raise ValueError('nonpositive mixed clock charge')
        s=(target-sig*DD)/(self.mpref*c)
        for it in range(12):
            if np.any(s<0) or not np.all(np.isfinite(s)):raise ValueError('mixed positive clock branch lost')
            X,m,d,K,dm,qr=self.constitutive(s)
            Q=np.sqrt(X*X+p*p);q=c*Q-sig*p;w=c*p-sig*Q
            Mx=d*q/X+m*(c/Q-q/X**2)
            if np.any(Mx<=0):raise ValueError('nonpositive fixed-p algebraic inverse')
            res=m*q/X+sig*DD-target;err=float(np.max(abs(res)/np.maximum(abs(target),1e-30)))
            if err<1e-15 or it==11:break
            s-=res/(Mx*self.Q0*self.eps/(2*qr*(1+s)**2))
        if err>2e-12:raise ValueError('mixed inverse residual')
        inverse=(q/X)*(d-(m/X)*w*w/(q*q)-self.C*sig*sig*X*X/(q*q)*(2/self.KB+jt))
        if np.any(inverse<=0):raise ValueError('nonpositive mixed time Schur')
        self.max_inverse=max(self.max_inverse,err);self.min_inverse=min(self.min_inverse,float(np.min(inverse/d)))
        jj=abs(p)/self.bs;J=self.lam*self.bs**2*(jj*np.sqrt(1+jj*jj)-np.arcsinh(jj))
        small=jj<.01;ss=jj[small]
        J[small]=self.lam*self.bs**2*(2*ss**3/3-ss**5/5+3*ss**7/28-5*ss**9/72)
        cur=c*DD-(m/X)*w;divZ=self.divergence(Z)
        Ecal=self.KB*e*e+self.C*p*p+self.C*J-2*K
        rhoC=Ecal/2+target*q+c*divZ/A
        PC=-Ecal/2-sig*Q*DD/c-w*cur+sig*sig*divZ/(A*c)
        es=np.sqrt(1+ps*ps/A**2+ls2/r**2);eb=np.sqrt(1+pb*pb/A**2)
        rhoB=(ns*es+nb*eb)/A;PrB=(ns*ps*ps/es+nb*pb*pb/eb)/A**3
        PtB=ns*ls2/(2*A*r*r*es);phir=A*w
        return locals()

    def rhs(self,t,z,return_g=False):
        if self.canonical_mode:
            gg=self.geometry(t,z);mixed=z.copy();mixed[1]=gg['p']
            self.canonical_mode=False
            out,g=self.rhs(t,mixed,True)
            self.canonical_mode=True
            out[1]=g['A']*(g['q']/g['Q']*out[1]-g['sig']*g['X']/g['Q']*g['Xt']-g['q']/g['c']*g['sigt'])+g['phir']*g['adot']
            return (out,g) if return_g else out
        if not np.all(np.isfinite(z)):raise ValueError('nonfinite mixed state')
        g=self.geometry(t,z);r=self.r;A=g['A'];N=g['N'];ar=g['ar'];gg=g['g']
        u,p,Z,cp,ns,ps,ell,nb,pb=z;sig=g['sig'];c=g['c'];X=g['X'];Q=g['Q'];q=g['q'];w=g['w']
        sr=(self.derivative(u,-1)-u*ar)/A
        adot=N*r*(-u*g['divZ']+cp*g['phir']-ns*ps-nb*pb)/(2*A)
        out=np.zeros_like(z)
        out[0]=N*(A*g['e']-gg*c-sig*sr/c)
        sigt=out[0]/A-sig*adot
        out[2]=N*(Q*g['DD']/c-sig*g['divZ']/(A*c))
        out[3]=-N*(self.divergence(g['cur'])+gg*g['cur'])
        Xdiff=self.Q0*self.eps*g['s']/((1+g['s'])*(g['qr']+1))
        xr=self.derivative(Xdiff);pr=self.derivative(p,-1)
        FF=N*c*X*xr/(A*q)+N*w*pr/(A*q)-N*Q*p*sr/(A*q*c*c)+N*Q*g['e']/c-Q*p*adot/(q*c)
        Mp=g['m']*w/(X*Q)-sig*self.C*(2/self.KB+g['jt'])
        Ms=g['DD']-g['m']*w/(c*X)
        Xt=(out[3]/A-g['target']*adot-Mp*FF-Ms*sigt-sig*(self.C/self.KB)*out[2])/g['inverse']
        out[1]=FF+sig*X/q*Xt
        for ni,pi,ei,li in ((4,5,g['es'],ell*ell),(7,8,g['eb'],np.zeros(self.n))):
            nn=z[ni];pp=z[pi];vel=N*pp/(A*A*ei)
            out[ni]=self.rest_flux(nn,vel)[0]
            out[pi]=-vel*self.derivative(pp,-1)-N*gg*ei+N/ei*(pp*pp*ar/(A*A)+li/r**3)
            if ni==4:out[6]=-vel*self.derivative(ell)
        g.update(adot=adot,sigt=sigt,Xt=Xt)
        return (out,g) if return_g else out

    def diagnose(self,t,z):
        dz,g=self.rhs(t,z,True);canonical=z.copy();canonical[1]=g['phir']
        wdot=g['q']/g['Q']*dz[1]-g['sig']*g['X']/g['Q']*g['Xt']-g['q']/g['c']*g['sigt']
        phirdot=g['A']*wdot+g['phir']*g['adot']
        Xdiff=self.Q0*self.eps*g['s']/((1+g['s'])*(g['qr']+1))
        direct=g['N']*(g['q']*g['g']+self.derivative(Xdiff+g['w']**2/(g['q']+g['X'])))
        scale=max(float(np.max(abs(direct[self.mask]))),1e-12)
        self.canonical_mode=True
        result=super().diagnose(t,canonical)
        self.canonical_mode=False
        result['canonical_integrability_error']=float(np.max(abs(phirdot[self.mask]-direct[self.mask])))/scale
        result['representation']='states in receipt canonical phi_R; checkpoint mixed p'
        return result
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--nodes',type=int,default=160)
    ap.add_argument('--duration',type=float,default=.25)
    ap.add_argument('--dt-factor',type=float,default=.5)
    ap.add_argument('--extent',type=float,default=.012)
    ap.add_argument('--tag',required=True);ap.add_argument('--wall-seconds',type=float,default=120.)
    ap.add_argument('--resume')
    args=ap.parse_args()
    output=BASE/('INVARIANT_CLOCK_POLAR_SOURCE_'+args.tag+'_RESULT.json')
    checkpoint=BASE/('INVARIANT_CLOCK_POLAR_SOURCE_'+args.tag+'_CHECKPOINT.json')
    if output.exists():raise FileExistsError(output)
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    identity=dict(source=sha(Path(__file__)),driver=sha(Path(src.__file__)),dependency=sha(Path(prev.__file__)),
                  inherited=sha(Path(prev.inherited.__file__)),input=sha(prev.inherited.SOURCE))
    np.seterr(over='raise',invalid='raise',divide='raise')
    beg=time.monotonic();model=Polar(json.loads(prev.inherited.SOURCE.read_text()),args.nodes,args.extent)
    z=model.initial();snaps=[];error=None;why='completed_requested_interval';step=0
    final=args.duration*model.tdyn;steps=math.ceil(final/(args.dt_factor*(model.r[1]-model.r[0])))
    dt=final/steps;start=0;flux_integral=np.zeros(2)
    if args.resume:
        earlier=json.loads((BASE/args.resume).read_text())
        if earlier['identity']!=identity:raise ValueError('resume identity mismatch')
        for key in ('nodes','duration','dt_factor','extent'):
            if earlier['args'][key]!=getattr(args,key):raise ValueError('resume protocol mismatch')
        z=np.array(earlier['state']);start=earlier['step'];snaps=earlier['snapshots']
        flux_integral=np.array(earlier['ordinary_flux_integral'])
    def flux(y,g):
        r=model.r;A=g['A'];N=g['N']
        return np.array([2*model.rest_flux(y[4],N*y[5]/(A*A*g['es']))[1][-1],
                         2*model.rest_flux(y[7],N*y[8]/(A*A*g['eb']))[1][-1]])
    def save(cpstep):
        data=dict(identity=identity,args=vars(args),step=cpstep,dt=dt,state=z.tolist(),
                  snapshots=snaps,ordinary_flux_integral=flux_integral.tolist())
        checkpoint.write_text(json.dumps(data,allow_nan=False))
    try:
        if not snaps:snaps.append(model.diagnose(start*dt,z))
        for step in range(start+1,steps+1):
            t=(step-1)*dt
            aa,ga=model.rhs(t,z,True);ya=z+aa*dt/2
            bb,gb=model.rhs(t+dt/2,ya,True);yb=z+bb*dt/2
            cc,gc=model.rhs(t+dt/2,yb,True);yc=z+cc*dt
            dd,gd=model.rhs(t+dt,yc,True)
            flux_integral+=dt*(flux(z,ga)+2*flux(ya,gb)+2*flux(yb,gc)+flux(yc,gd))/6
            z+=dt*(aa+2*bb+2*cc+dd)/6
            if np.min(z[[4,7]])<0:raise ValueError('negative ordinary restweight')
            if step%max(1,steps//16)==0 or step==steps:
                snap=model.diagnose(step*dt,z);snaps.append(snap)
                print(json.dumps({k:snap[k] for k in ('t_over_tdyn','central_expansion_estimate','max_JY','min_clock_s','angular_constraint_reduced_error')}),flush=True)
            if step%4096==0:
                save(step)
                if time.monotonic()-beg>args.wall_seconds:
                    why='bounded_checkpoint';break
        if snaps[-1]['t']!=step*dt:snaps.append(model.diagnose(step*dt,z))
    except (ValueError,FloatingPointError,OverflowError) as exc:
        error=f'{type(exc).__name__}: {exc}';why='failure'
    save(step)
    last=snaps[-1];first=snaps[0]
    mass0=np.array([first['supported_discrete_restweight'],first['background_discrete_restweight']])
    mass1=np.array([2*np.dot(model.volumes,z[4]),2*np.dot(model.volumes,z[7])])
    checks=dict(Hamiltonian=max(s['Hamiltonian_source_normalized'] for s in snaps)<=1e-3,
        flux=max(s['flux_tangent_normalized'] for s in snaps)<=1e-3,
        flux_step=max(s['flux_tangent_step_control'] for s in snaps)<=1e-3,
        angular_reduced=max(s['angular_constraint_reduced_error'] for s in snaps)<=1e-3,
        angular_step=max(s['angular_tangent_step_control'] for s in snaps)<=1e-3,
        inverse=model.max_inverse<=2e-12,positive_inverse=model.min_inverse>0,
        positive_ordinary=float(np.min(z[[4,7]]))>=0)
    checks['canonical_integrability']=max(s['canonical_integrability_error'] for s in snaps)<=1e-3
    result=dict(protocol=__doc__,identity=identity,args=vars(args),reason=why,error=error,
        step=step,steps=steps,dt=dt,t_over_tdyn=step*dt/model.tdyn,elapsed_seconds=time.monotonic()-beg,
        max_inverse=model.max_inverse,min_inverse=model.min_inverse,checks=checks,
        snapshots=snaps,ordinary_rest_budget_relative=((mass1-mass0+flux_integral)/mass0).tolist(),
        checkpoint=checkpoint.name,scope='trajectory only; time/grid/domain acceptance pending')
    with output.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps({k:v for k,v in result.items() if k not in ('protocol','snapshots')},allow_nan=False),flush=True)


if __name__=='__main__':main()

