"""Conservation-complete bounded polar source continuation of V003.

No new physical parameter/width/phase fit. V001-003 pilot results remain
separate. The literal angular spatial-derivative check remains reported;
its leading Newtonian cancellation is also evaluated using the already
solved radial constraints, as a stress/evolution consistency check:
 pib_dot/R³=2NA[(Lvec+2K-2Pc+2PtB-2PrB)/R-P_R-g(rho+P)].
The pressure derivative uses cancellation-free K-Kref. This is NOT an
independent test of the radial constraints; their Hamiltonian check stays.

All gates remain1e-3; inverse2e-12 and positive clock/inverse/restweights.
Actual runs are one small CPU worker, bounded/checkpointed. A returned
trajectory without completed time/grid/domain comparisons is UNQUALIFIED.
Source normalization kappa fixes the coordinate rest-density profile
integral, not exact total gravitating mass including orbital/metric energy.
Cosmic initialization and boundary restrictions inherited from V003 apply.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import time
import numpy as np
import invariant_clock_polar_source_v003 as prev

BASE=Path(__file__).resolve().parent


class Polar(prev.Polar):
    def diagnose(self,t,z):
        out=super().diagnose(t,z)
        dz,g=self.rhs(t,z,True);r=self.r;mask=self.mask
        N=g['N'];A=g['A'];sig=g['sig'];c=g['c'];Z=z[2]
        sb=self.bg0[1];ds=g['s']-sb
        dK=3*self.OA/self.D*(np.log1p(ds/(1+sb))-ds/((1+g['s'])*(1+sb)))
        Ps=dK-.5*(self.KB*g['e']**2+self.C*g['p']**2+self.C*g['J'])
        Ps+=-sig*g['Q']*g['DD']/c-g['w']*g['cur']+sig**2*g['divZ']/(A*c)+g['PrB']
        anis=2*(Z*g['e']+sig*g['Q']*g['DD']/c+g['w']*g['cur']
                -sig**2*g['divZ']/(A*c)+g['PtB']-g['PrB'])
        pr=self.derivative(Ps)
        angular=2*N*A*(anis/r-pr-g['g']*(g['rhoC']+g['rhoB']+g['PC']+g['PrB']))
        def pbreg(zz,gg):
            return 2*(zz[0]*gg['divZ']-zz[3]*zz[1]+zz[4]*zz[5]+zz[7]*zz[8])
        old=self.Aguess.copy();tangent=[]
        for fac in (1e-6,5e-7):
            dt=fac*self.tdyn
            ggplus=self.geometry(t+dt,z+dt*dz);ggminus=self.geometry(t-dt,z-dt*dz)
            tangent.append((pbreg(z+dt*dz,ggplus)-pbreg(z-dt*dz,ggminus))/(2*dt))
        self.Aguess=old
        sc=max(float(np.max(abs(angular[mask]))),float(np.max(abs(tangent[-1][mask]))),self.initial_peak*self.kappa,1e-12)
        out['angular_constraint_reduced_error']=float(np.max(abs(angular[mask]-tangent[-1][mask])))/sc
        out['angular_tangent_step_control']=float(np.max(abs(tangent[0][mask]-tangent[1][mask])))/sc
        out['angular_equation_scale']=sc
        out['maximum_nonrelativistic_core_velocity']=float(np.max(abs(g['sig'][mask])))
        return out


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
    identity=dict(source=sha(Path(__file__)),dependency=sha(Path(prev.__file__)),
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
    result=dict(protocol=__doc__,identity=identity,args=vars(args),reason=why,error=error,
        step=step,steps=steps,dt=dt,t_over_tdyn=step*dt/model.tdyn,elapsed_seconds=time.monotonic()-beg,
        max_inverse=model.max_inverse,min_inverse=model.min_inverse,checks=checks,
        snapshots=snaps,ordinary_rest_budget_relative=((mass1-mass0+flux_integral)/mass0).tolist(),
        checkpoint=checkpoint.name,scope='trajectory only; time/grid/domain acceptance pending')
    with output.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps({k:v for k,v in result.items() if k not in ('protocol','snapshots')},allow_nan=False),flush=True)


if __name__=='__main__':main()
