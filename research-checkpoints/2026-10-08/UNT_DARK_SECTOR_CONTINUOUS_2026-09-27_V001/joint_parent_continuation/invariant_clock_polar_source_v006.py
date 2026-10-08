"""Wave-buffered mesh for the SAME mixed-p polar equations.

The saved charge audit found split/combined current derivative differences
below 5e-14, and integral defects below 5e-7, not the observed .0015 error.
The local fourth-order derivative symbol turns a k~1/L outgoing wave on
the original sinh mesh near133L (N960), with a return time ~.20 t_dyn.
This is a hypothesis about numerical backscatter, not a physical failure.

Keep the exact original core nodes while adjacent spacing <= cap*L,
then cap spacing to cap*L through buffer*L before stretching again to the
SAME outer extent. Defaults cap=.125, buffer=600 resolve k~1/L and defer
the low-k numerical turning region past the .25 t_dyn interval.
No absorbing boundary, damping, physical coupling or source change.
All old numerical gates remain. Actual number of nodes is recorded.

Cubic quadrature uses exactly the same four-node interval polynomials,
stored as local weights plus a prefix sum instead of a dense cumulative
matrix. It is still point-value quadrature, not a finite-volume scalar
reinterpretation. Algebraic equivalence must be checked separately.
Accepted state/step and RK flux updates are transactional on failures.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import time
import numpy as np
import invariant_clock_polar_source_v005 as mixed
src=mixed.src
prev=mixed.prev
BASE=Path(__file__).resolve().parent


class PrefixQuadrature:
    def __init__(self,r,parity,power):
        n=len(r); self.indices=np.zeros((n,4),dtype=int)
        self.values=np.zeros((n,4))
        gx,gw=np.polynomial.legendre.leggauss(4)
        for end in range(n):
            ids=np.arange(min(end-2,n-4),min(end-2,n-4)+4)
            nodes=np.array([(-r[-j-1] if j<0 else r[j]) for j in ids])
            lo=0. if end==0 else r[end-1];hi=r[end]
            pts=(lo+hi)/2+(hi-lo)*gx/2
            for j in range(4):
                val=pts**power
                for k in range(4):
                    if k!=j:val=val*(pts-nodes[k])/(nodes[j]-nodes[k])
                index=ids[j];sgn=parity if index<0 else 1
                self.indices[end,j]=-index-1 if index<0 else index
                self.values[end,j]=sgn*(hi-lo)*np.dot(gw,val)/2

    def __matmul__(self,f):
        return np.cumsum(np.sum(self.values*f[self.indices],axis=1))


class Polar(mixed.Polar):
    def __init__(self,saved,n=960,extent=.012,cap=.125,buffer=600.):
        super().__init__(saved,32,extent)
        self.base_nodes=n;self.cap=cap;self.buffer=buffer
        self.dxgrid=math.asinh(extent/self.L)/n
        radius=[self.L*math.sinh(.5*self.dxgrid)];i=1
        while True:
            next_r=self.L*math.sinh((i+.5)*self.dxgrid)
            if next_r-radius[-1]>cap*self.L:break
            radius.append(next_r);i+=1
        while radius[-1]<extent:
            h=cap*self.L+self.dxgrid*max(radius[-1]-buffer*self.L,0.)
            radius.append(radius[-1]+h)
        actual_n=len(radius)-1
        while len(radius)<actual_n+2:
            h=cap*self.L+self.dxgrid*max(radius[-1]-buffer*self.L,0.)
            radius.append(radius[-1]+h)
        self.n=actual_n;self.rg=np.array(radius);self.r=self.rg[:self.n]
        self.mask=self.r<=10*self.L;self.weights=[]
        for i in range(self.n):
            rr=np.array([(-self.rg[-j-1] if j<0 else self.rg[j]) for j in range(i-2,i+3)])
            sc=max(abs(rr-self.r[i]));xx=(rr-self.r[i])/sc
            mat=np.array([xx**k for k in range(5)])
            self.weights.append(np.linalg.solve(mat,np.array([0.,1.,0.,0.,0.]))/sc)
        self.weights=np.array(self.weights)
        self.massint=PrefixQuadrature(self.r,1,2)
        self.lapseint=PrefixQuadrature(self.r,-1,0)
        self.edges=np.r_[0.,(self.r[:-1]+self.r[1:])/2,extent]
        self.volumes=np.diff(self.edges**3)/3
        self.Aguess=np.ones(self.n)
        if np.min(self.volumes)<=0:raise ValueError('nonpositive mesh volume')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--nodes',type=int,default=160)
    ap.add_argument('--duration',type=float,default=.25)
    ap.add_argument('--dt-factor',type=float,default=.5)
    ap.add_argument('--extent',type=float,default=.012)
    ap.add_argument('--tag',required=True);ap.add_argument('--wall-seconds',type=float,default=120.)
    ap.add_argument('--resume')
    ap.add_argument('--cap',type=float,default=.125)
    ap.add_argument('--buffer',type=float,default=600.)
    args=ap.parse_args()
    output=BASE/('INVARIANT_CLOCK_POLAR_SOURCE_'+args.tag+'_RESULT.json')
    checkpoint=BASE/('INVARIANT_CLOCK_POLAR_SOURCE_'+args.tag+'_CHECKPOINT.json')
    if output.exists():raise FileExistsError(output)
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    identity=dict(source=sha(Path(__file__)),mixed=sha(Path(mixed.__file__)),driver=sha(Path(src.__file__)),dependency=sha(Path(prev.__file__)),
                  inherited=sha(Path(prev.inherited.__file__)),input=sha(prev.inherited.SOURCE))
    np.seterr(over='raise',invalid='raise',divide='raise')
    beg=time.monotonic();model=Polar(json.loads(prev.inherited.SOURCE.read_text()),args.nodes,args.extent,args.cap,args.buffer)
    z=model.initial();snaps=[];error=None;why='completed_requested_interval';step=0
    final=args.duration*model.tdyn;steps=math.ceil(final/(args.dt_factor*(model.r[1]-model.r[0])))
    dt=final/steps;start=0;flux_integral=np.zeros(2)
    if args.resume:
        earlier=json.loads((BASE/args.resume).read_text())
        if earlier['identity']!=identity:raise ValueError('resume identity mismatch')
        for key in ('nodes','duration','dt_factor','extent','cap','buffer'):
            if earlier['args'][key]!=getattr(args,key):raise ValueError('resume protocol mismatch')
        z=np.array(earlier['state']);start=earlier['step'];snaps=earlier['snapshots']
        flux_integral=np.array(earlier['ordinary_flux_integral'])
        model.max_inverse=earlier['max_inverse'];model.min_inverse=earlier['min_inverse']
    step=start;last_good_step=start;trial_step=None
    def flux(y,g):
        r=model.r;A=g['A'];N=g['N']
        return np.array([2*model.rest_flux(y[4],N*y[5]/(A*A*g['es']))[1][-1],
                         2*model.rest_flux(y[7],N*y[8]/(A*A*g['eb']))[1][-1]])
    def save(cpstep):
        data=dict(identity=identity,args=vars(args),step=cpstep,dt=dt,state=z.tolist(),
                  snapshots=snaps,ordinary_flux_integral=flux_integral.tolist(),
                  max_inverse=model.max_inverse,min_inverse=model.min_inverse)
        checkpoint.write_text(json.dumps(data,allow_nan=False))
    try:
        if not snaps:snaps.append(model.diagnose(start*dt,z))
        for step in range(start+1,steps+1):
            trial_step=step;t=(step-1)*dt
            aa,ga=model.rhs(t,z,True);ya=z+aa*dt/2
            bb,gb=model.rhs(t+dt/2,ya,True);yb=z+bb*dt/2
            cc,gc=model.rhs(t+dt/2,yb,True);yc=z+cc*dt
            dd,gd=model.rhs(t+dt,yc,True)
            candidate=z+dt*(aa+2*bb+2*cc+dd)/6
            if not np.all(np.isfinite(candidate)):raise ValueError('nonfinite candidate')
            if np.min(candidate[[4,7]])<0:raise ValueError('negative ordinary restweight')
            # Validate the full candidate before committing its state/time.
            model.geometry(step*dt,candidate)
            flux_integral+=dt*(flux(z,ga)+2*flux(ya,gb)+2*flux(yb,gc)+flux(yc,gd))/6
            z=candidate;last_good_step=step
            if step%max(1,steps//16)==0 or step==steps:
                snap=model.diagnose(step*dt,z);snaps.append(snap)
                print(json.dumps({k:snap[k] for k in ('t_over_tdyn','central_expansion_estimate','max_JY','min_clock_s','angular_constraint_reduced_error')}),flush=True)
            if step%4096==0:
                save(step)
                if time.monotonic()-beg>args.wall_seconds:
                    why='bounded_checkpoint';break
        if snaps[-1]['t']!=step*dt:snaps.append(model.diagnose(step*dt,z))
    except (ValueError,FloatingPointError,OverflowError) as exc:
        error=f'{type(exc).__name__}: {exc}';why='failure';step=last_good_step
    save(last_good_step)
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
        step=last_good_step,trial_step=trial_step,actual_nodes=model.n,steps=steps,dt=dt,t_over_tdyn=step*dt/model.tdyn,elapsed_seconds=time.monotonic()-beg,
        max_inverse=model.max_inverse,min_inverse=model.min_inverse,checks=checks,
        snapshots=snaps,ordinary_rest_budget_relative=((mass1-mass0+flux_integral)/mass0).tolist(),
        checkpoint=checkpoint.name,scope='trajectory only; time/grid/domain acceptance pending')
    with output.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps({k:v for k,v in result.items() if k not in ('protocol','snapshots')},allow_nan=False),flush=True)


if __name__=='__main__':main()


