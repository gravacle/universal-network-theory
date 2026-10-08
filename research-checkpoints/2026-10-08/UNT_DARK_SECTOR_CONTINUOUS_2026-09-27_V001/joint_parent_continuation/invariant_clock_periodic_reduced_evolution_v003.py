"""V003 finer explicit steps; preserve failed V001 explicit and V002 implicit.
Bounded exact reduced-action continuation; no physical claim from a solver.

Paired real cosine/sine modal chart; exact H,D reconstruction every RHS.
Evolve mean pi_a, retain fixed dust restweight and every allowed harmonic.
No state, mean shear, or scalar charge projection. The analytically zero
scalar mean RHS is evaluated directly as its flux derivative. Subtract
only the exact homogeneous RHS roundoff, with its magnitude recorded.
Fourth-order Lawson RK4, homogeneous A frozen anew at each step midpoint.
All nonlinear terms AND A(t)-A(midpoint) are in the exact residual.
Same constrained epoch54 equal-contrast1e-12 seed and a=.60429639 endpoint.
Serial17x4096/8192/16384 and33x16384,150s wall bound, checkpoint16 steps.
Unchanged each-prefix1e-4 time/space full-state and observable gates;
H/background1e-9,H/perturbation1e-4,D1e-4,charge1e-12, positive sheet.
The frozen matrix is a numerical split only, not a physical mode selection.
"""
from pathlib import Path
import json, math, time
import numpy as np
import invariant_clock_periodic_initial_v002 as initial
import invariant_clock_periodic_reduced_v003 as reduced
import invariant_clock_periodic_evolution_v007 as diagnostics
from invariant_clock_compression_response_v001 import expm

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'INVARIANT_CLOCK_PERIODIC_REDUCED_COMPONENTS_V003_RESULT.json'
EXPECTED='ec7d78567d50cf486698ea1e57aa17869ce84cd09c29f53971f36ebf3bf6e8ab'
OUT=ROOT/'INVARIANT_CLOCK_PERIODIC_REDUCED_EVOLUTION_V003_RESULT.json'
CP=ROOT/'INVARIANT_CLOCK_PERIODIC_REDUCED_EVOLUTION_V003_CHECKPOINT.json'
sha=initial.sha
clean=diagnostics.clean

class Integrator:
    def __init__(self,run,x):
        self.r=run;self.n=run.n;self.M=self.n//2+1
        self.scale=np.array([1.,1/run.k**2,1/run.k,run.m.Q0/run.k**2,
                             1.,run.core.background(x)['pi_T_bar'],1/run.k,run.pi_phi_bar])
        self.parity=np.array([1,1,-1,1,1,1,-1,1])
        self.T=np.array([1,1,-1j,1,1,1,-1j,1])
        self.max_zero=0.;self.max_rhs_parity=0.
    def coeff(self,z):
        y=np.zeros((self.M,8));v=z/self.scale[:,None]
        for j in range(8):
            if self.parity[j]==1:
                y[0,j]=np.mean(v[j])
                vc=v[j]-y[0,j]
                y[1:,j]=(vc[0]+2*self.r.ch[1:,1:]@vc[1:self.M])/self.n
            else:y[1:,j]=2*self.r.sh[1:,1:]@v[j,1:self.M]/self.n
        return y
    def grid(self,y):
        z=np.zeros((8,self.n))
        for j in range(8):
            if self.parity[j]==1:z[j]=y[0,j]+2*y[1:,j]@self.r.cosine[1:]
            else:z[j]=2*y[1:,j]@self.r.sine
        return z*self.scale[:,None]
    def matrix(self,x):
        complexA=self.r.matrices(x)*self.scale[None,None,:]/self.scale[None,:,None]
        transformed=complexA*self.T[None,None,:]/self.T[None,:,None]
        # Nonzero odd homogeneous coordinate is outside this reflection
        # representation; the zero-mode real matrix acts on its exact zeros.
        if np.max(abs(transformed.imag))>1e-12*max(np.max(abs(transformed.real)),1e-30):
            raise ValueError('real parity matrix mismatch')
        return transformed.real
    def raw_rhs(self,x,y):
        chart=self.grid(y);f,rec=self.r.rhs(x,chart,return_fields=True)
        err=np.max(abs(f-self.parity[:,None]*f[:,self.r.mirror]))/max(np.max(abs(f)),1e-30)
        self.max_rhs_parity=max(self.max_rhs_parity,float(err))
        out=self.coeff(f)
        g=rec['fields'];flux=g['flux_phi']
        flux_sine=2*self.r.sh[1:,1:]@flux[1:self.M]/self.n
        out[0,7]=0.
        out[1:,7]=-self.r.k*np.arange(1,self.M)*flux_sine/(self.scale[7]*g['H'])
        return out
    def step(self,x,y,h):
        A=self.matrix(x+h/2)
        E2=np.array([expm(h*a/2) for a in A]);E=E2@E2
        mul=lambda a,b:(a@b[...,None])[...,0]
        def nonlinear(t,z):
            zero=self.raw_rhs(t,np.zeros_like(z))
            self.max_zero=max(self.max_zero,float(np.max(abs(zero))))
            return self.raw_rhs(t,z)-zero-mul(A,z)
        n1=nonlinear(x,y)
        n2=nonlinear(x+h/2,mul(E2,y+h*n1/2))
        n3=nonlinear(x+h/2,mul(E2,y)+h*n2/2)
        n4=nonlinear(x+h,mul(E,y)+h*mul(E2,n3))
        return mul(E,y)+h*(mul(E,n1)+2*mul(E2,n2+n3)+n4)/6

def main():
    if OUT.exists() or CP.exists():raise FileExistsError('exclusive run already exists')
    if sha(SOURCE)!=EXPECTED:raise ValueError('changed qualified reduced preparation')
    saved=json.loads(SOURCE.read_text())
    if not saved['all_controls_passed']:raise ValueError('components unqualified')
    for p,d in saved['dependencies'].items():
        if sha(p)!=d:raise ValueError('changed component dependency')
    model,parent=initial.load();rows=[];checks=[];error=None;t0=time.monotonic()
    def check(name,e,gate):checks.append(dict(name=name,error=float(e),gate=gate,passed=bool(e<=gate)))
    try:
        xend=math.log(parent['histories'][-1]['snapshots'][57]['a'])
        for N,nstep in ((17,4096),(17,8192),(17,16384),(33,16384)):
            row=next(r for r in saved['rows'] if r['nodes']==N)
            x0=row['x'];chart=np.array(row['chart']);piT=np.array(row['piT'])
            run=reduced.Reduced(model,N,initial.linear.Assembly(model).k)
            integ=Integrator(run,x0);y=integ.coeff(chart)
            check(f'{N}_{nstep}_modal_roundtrip',np.max(np.max(abs(integ.grid(y)-chart),axis=1)/np.maximum(np.max(abs(chart),axis=1),1e-30)),1e-12)
            rec=run.reconstruct(x0,integ.grid(y));dscale=np.max(np.sum(abs(rec['constraints']['momentum_terms']),axis=0))
            snapshots=[];h=(xend-x0)/nstep
            for i in range(nstep+1):
                x=x0+i*h
                if i%(nstep//32)==0:
                    rec=run.reconstruct(x,integ.grid(y))
                    snapshots.append(diagnostics.diagnose(run.core,x,rec['z'],piT,dscale))
                if i%16==0:
                    with CP.open('w') as out:json.dump(dict(producer_sha256=sha(__file__),nodes=N,steps=nstep,accepted_step=i,x=x,chart=integ.grid(y),piT=piT,snapshots=snapshots,completed_rows=rows),out,allow_nan=False,default=clean)
                if i==nstep:break
                y=integ.step(x,y,h)
                if time.monotonic()-t0>150:raise TimeoutError('150s serial bound; accepted checkpoint saved')
            rows.append(dict(nodes=N,steps=nstep,snapshots=snapshots,max_rhs_parity=integ.max_rhs_parity,maximum_homogeneous_subtraction_scaled=integ.max_zero))
            print(json.dumps(dict(nodes=N,steps=nstep,elapsed=time.monotonic()-t0,final={k:v for k,v in snapshots[-1].items() if k not in ('state','observables')})),flush=True)
        for kind,left,right in (('time',rows[1],rows[2]),('space',rows[2],rows[3])):
            for key in ('state','observables'):check(kind+'_'+key,diagnostics.compare(left,right,key)['maximum'],1e-4)
        for key,gate in (('H_background',1e-9),('H_perturbation',1e-4),('momentum',1e-4),('mean_charge',1e-12)):
            check(key,max(s[key] for r in rows for s in r['snapshots']),gate)
    except Exception as exc:error=dict(type=type(exc).__name__,message=str(exc),diagnostics=getattr(exc,'diagnostics',None))
    result=dict(protocol=__doc__,producer_sha256=sha(__file__),source_sha256=EXPECTED,
        dependencies={str(Path(p)):sha(p) for p in (reduced.__file__,initial.__file__,diagnostics.__file__,run.core.__class__.__module__.replace('.', '/')+'.py')},
        rows=rows,checks=checks,error=error,all_controls_passed=error is None and len(rows)==4 and all(c['passed'] for c in checks),
        physical_saturation_established=False,observational_superiority=False,elapsed_seconds=time.monotonic()-t0)
    with OUT.open('x') as out:json.dump(result,out,indent=2,allow_nan=False,default=clean)
    print(json.dumps(dict(error=error,checks=checks,all_pass=result['all_controls_passed'],sha256=sha(OUT)),indent=2),flush=True)
    if not result['all_controls_passed']:raise SystemExit(1)

if __name__=='__main__':main()
