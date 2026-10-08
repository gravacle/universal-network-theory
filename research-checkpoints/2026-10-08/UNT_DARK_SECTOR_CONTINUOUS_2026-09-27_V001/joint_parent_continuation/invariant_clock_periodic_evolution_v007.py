"""V007 independent Lawson integrating-factor RK4, exact nonlinear action.

Prior implicit Gauss attempts remain failed numerical controls, not physical
trajectories. This explicit transformed RK4 has no iterative-stage gate; it
does NOT relax one or accept the old failed stages. Linear oscillations are
exponentiated, all nonlinear terms/physical Fourier modes are retained.
Freeze A at each of32block midpoints; N=entire exact RHS−A*y, so no term is
discarded by freezing. Fixed same .4869675→.6042964 interval and constrained
epoch54 equal-contrast1e-12 preparation. Current K(X)/J/cTheta=.01 unchanged.
17x4096/8192/16384 and33x16384 serial,150second bound; checkpoint16steps.
UNCHANGED1e-4 full-state/observable prefix time/grid gates, Hamiltonian
background1e-9/perturbation1e-4,momentum1e-4,charge1e-12,positive sheet.
No filtering, state projection, source holding, fit or galaxy claim.
"""
from pathlib import Path
import json,math,time
import numpy as np
import invariant_clock_periodic_initial_v002 as initial
import invariant_clock_periodic_exact_v002 as exact
import invariant_clock_periodic_linear_v001 as tangent
from invariant_clock_compression_response_v001 import expm

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'INVARIANT_CLOCK_PERIODIC_COMPONENTS_V004_RESULT.json'
EXPECTED='f4bc4d6c9b5ace57b9d6848fd0b27a299e429eb3a5c4c1f8d3f5b2c99295e831'
OUT=ROOT/'INVARIANT_CLOCK_PERIODIC_EVOLUTION_V007_RESULT.json'
CP=ROOT/'INVARIANT_CLOCK_PERIODIC_EVOLUTION_V007_CHECKPOINT.json'
sha=initial.sha
def clean(v):
    if isinstance(v,np.ndarray):return v.tolist()
    if isinstance(v,np.generic):return v.item()
    raise TypeError(type(v).__name__)

class Integrator:
    def __init__(self,run):
        self.r=run;self.n=run.n;self.M=self.n//2+1;self.scale=tangent.scales(run)
        self.max_stage=0.;self.max_zero=0.;self.max_iterations=0;self.frozen=None;self.E=None;self.E2=None
    def coeff(self,z):return (np.fft.rfft(z/self.scale[:,None],axis=1)/self.n).T
    def grid(self,y):return np.fft.irfft(y.T*self.n,n=self.n,axis=1)*self.scale[:,None]
    def raw_rhs(self,x,y):
        f,g=self.r.rhs(x,self.grid(y),return_fields=True)
        out=self.coeff(f)
        # Exactly the same periodic derivative as the field equation; avoid
        # derivative->grid->Fourier roundtrip, especially its identically
        # zero n=0 entry. No state projection or physical filter.
        ik=1j*self.r.k*np.arange(self.M)
        out[:,7]=-ik*(np.fft.rfft(g['flux_phi'])/self.n)/(self.scale[7]*g['H'])
        return out
    def freeze(self,x,h):
        self.frozen=tangent.matrices(self.r,x)
        self.E2=np.array([expm(h*A/2) for A in self.frozen])
        self.E=self.E2@self.E2
    def step(self,x,y,h):
        mul=lambda a,b:(a@b[...,None])[...,0]
        def nonlinear(t,z):
            fzero=self.raw_rhs(t,np.zeros_like(z))
            self.max_zero=max(self.max_zero,float(np.max(abs(fzero))))
            return self.raw_rhs(t,z)-fzero-mul(self.frozen,z)
        n1=nonlinear(x,y)
        ya=mul(self.E2,y+h*n1/2);n2=nonlinear(x+h/2,ya)
        yb=mul(self.E2,y)+h*n2/2;n3=nonlinear(x+h/2,yb)
        yc=mul(self.E,y)+h*mul(self.E2,n3);n4=nonlinear(x+h,yc)
        return mul(self.E,y)+h*(mul(self.E,n1)+2*mul(self.E2,n2+n3)+n4)/6

def diagnose(run,x,z,piT,initial_momentum_scale):
    f,g=run.rhs_proper(x,z,return_fields=True);cc=run.constraints(x,z,piT,fields=g)
    rb=3*run.m.OB/g['abar']**3;db=piT/(2*g['V'])/rb-1
    hbg=6*g['Vbar']*g['H']**2
    hpert=max(np.max(abs(piT-g['pi_T_bar'])),np.max(abs(run.dx(cc['boundary']))),1e-30)
    dscale=max(np.max(np.sum(abs(cc['momentum_terms']),axis=0)),initial_momentum_scale,1e-30)
    obs=np.array([db,g['mdiff']/g['mbar'],g['p'],g['e'],g['delta_chi'],g['delta_adot'],g['delta_bdot'],g['qdiff']])
    Jcharge=2*run.C*run.dx(g['B']**2*g['c']*g['j']*g['p'])
    deltaT=g['delta_adot']+2*g['delta_bdot']
    return dict(a=g['abar'],state=z,observables=obs,
        H_background=float(np.max(abs(cc['Hamiltonian']))/hbg),H_perturbation=float(np.max(abs(cc['Hamiltonian']))/hpert),
        momentum=float(np.max(abs(cc['momentum']))/dscale),mean_charge=float(abs(np.mean(z[7]))/run.pi_phi_bar),
        inverse_error=g['inverse_error'],min_s=float(np.min(g['s'])),min_schur_fraction=float(np.min(g['schur']/g['d'])),
        minimum_volume_ratio=float(np.min(g['V']/g['Vbar'])),
        peak_ordinary_contrast=float(np.max(abs(db))),ordinary_fundamental=float(2*np.real(np.fft.rfft(db)[1])/run.n),
        max_Cj_over_mu=float(np.max(run.C*g['j']/(g['m']/g['X']))),
        max_Cjt_over_mu=float(np.max(run.C*g['jt']/(g['m']/g['X']))),
        ordinary_advection_ratio=float(np.max(abs(db*deltaT))/max(np.max(abs((1+db)*deltaT)),1e-30)),
        explicit_J_charge_source_ratio=float(np.max(abs(Jcharge))/max(np.max(abs(f[7])),1e-30)),
        canonical_geometric_difference=float(np.max(abs(cc['canonical_minus_geometric']))/hpert))

def compare(left,right,key):
    a=np.array([s[key] for s in left['snapshots']]);b=np.array([s[key] for s in right['snapshots']])
    if a.shape[-1]!=b.shape[-1]:
        N=b.shape[-1];ff=np.fft.rfft(a,axis=-1)/a.shape[-1];pad=np.zeros(b.shape[:-1]+(N//2+1,),complex)
        pad[...,:ff.shape[-1]]=ff;a=np.fft.irfft(pad*N,n=N,axis=-1)
    errors=[]
    for i in range(1,len(a)):
        errors.append(float(np.max(np.max(abs(a[:i+1]-b[:i+1]),axis=(0,2))/np.maximum(np.max(abs(b[:i+1]),axis=(0,2)),1e-30))))
    return dict(maximum=max(errors),prefix=errors)

def main():
    if OUT.exists() or CP.exists():raise FileExistsError('exclusive evolution already exists')
    if sha(SOURCE)!=EXPECTED:raise ValueError('changed initial qualification')
    source=json.loads(SOURCE.read_text())
    if not source['all_controls_passed']:raise ValueError('initial component controls failed')
    for p,d in source['dependencies'].items():
        if sha(p)!=d:raise ValueError('changed component dependency')
    model,parent=initial.load();checks=[];rows=[];error=None;t0=time.monotonic()
    def check(name,e,gate):checks.append(dict(name=name,error=float(e),gate=gate,passed=bool(e<=gate)))
    try:
        run=exact.PeriodicExact(model,17,initial.linear.Assembly(model).k)
        integ=Integrator(run);x=source['rows'][0]['x'];A=tangent.matrices(run,x)
        for eps in (1e-5,5e-6):
            yy=np.zeros((integ.M,8),complex);yy[1]=eps*np.array([.7,.3,.2j,.5,-.4,.8,-.3j,.6])/2
            actual=(integ.raw_rhs(x,yy)-integ.raw_rhs(x,-yy))/2
            predicted=(A@yy[...,None])[...,0]
            e=np.max(np.max(abs(actual-predicted),axis=0)/np.maximum(np.max(abs(predicted),axis=0),1e-30))
            check(f'modal_tangent_{eps}',e,1e-4)
        if not all(c['passed'] for c in checks):raise ValueError('analytic modal tangent control failed')
        xend=math.log(parent['histories'][-1]['snapshots'][57]['a'])
        for N,nstep in ((17,4096),(17,8192),(17,16384),(33,16384)):
            row=next(r for r in source['rows'] if r['nodes']==N);x0=row['x'];z=np.array(row['state']);piT=np.array(row['piT'])
            run=exact.PeriodicExact(model,N,initial.linear.Assembly(model).k);integ=Integrator(run);y=integ.coeff(z)
            cc=run.constraints(x0,z,piT);dscale=float(np.max(np.sum(abs(cc['momentum_terms']),axis=0)))
            snaps=[];h=(xend-x0)/nstep
            for i in range(nstep+1):
                x=x0+i*h
                if i%(nstep//32)==0:snaps.append(diagnose(run,x,integ.grid(y),piT,dscale))
                if i%16==0:
                    with CP.open('w') as out:json.dump(dict(producer_sha256=sha(__file__),nodes=N,steps=nstep,accepted_step=i,x=x,
                        state=integ.grid(y),piT=piT,completed_rows=rows,snapshots=snaps),out,allow_nan=False,default=clean)
                if i==nstep:break
                if i%(nstep//32)==0:integ.freeze(x+h*(nstep//32)/2,h)
                y=integ.step(x,y,h)
                if time.monotonic()-t0>150:raise TimeoutError('150 second serial bound; checkpoint retained')
            rows.append(dict(nodes=N,steps=nstep,snapshots=snaps,max_stage=integ.max_stage,
                max_iterations=integ.max_iterations,maximum_homogeneous_subtraction_scaled=integ.max_zero))
            print(json.dumps(dict(nodes=N,steps=nstep,elapsed=time.monotonic()-t0,
                final={k:v for k,v in snaps[-1].items() if k not in ('state','observables')})),flush=True)
        for kind,l,r in (('time',rows[1],rows[2]),('space',rows[2],rows[3])):
            for key in ('state','observables'):check(kind+'_'+key,compare(l,r,key)['maximum'],1e-4)
        for key,gate in (('H_background',1e-9),('H_perturbation',1e-4),('momentum',1e-4),('mean_charge',1e-12)):
            check(key,max(s[key] for r in rows for s in r['snapshots']),gate)
    except Exception as exc:error=dict(type=type(exc).__name__,message=str(exc),diagnostics=getattr(exc,'diagnostics',None))
    result=dict(protocol=__doc__,producer_sha256=sha(__file__),source_sha256=EXPECTED,
        dependencies={str(Path(p)):sha(p) for p in (exact.__file__,initial.__file__,tangent.__file__)},fixed=model.p,
        rows=rows,checks=checks,error=error,all_controls_passed=error is None and len(rows)==4 and all(c['passed'] for c in checks),
        physical_saturation_established=False,galaxy_prediction=False,observational_superiority=False,elapsed_seconds=time.monotonic()-t0)
    with OUT.open('x') as out:json.dump(result,out,indent=2,allow_nan=False,default=clean)
    print(json.dumps(dict(checks=checks,error=error,all_pass=result['all_controls_passed'],sha256=sha(OUT)),indent=2),flush=True)
    if not result['all_controls_passed']:raise SystemExit(1)

if __name__=='__main__':main()






