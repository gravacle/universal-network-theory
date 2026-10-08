"""Bounded exact conserved-source periodic evolution, no galaxy claim.

Current action, cTheta=.01,20kpc comoving scale, SAME epoch54 equal-contrast
seed1e-12. Exact constrained initial data from qualified componentsV003.
Fixed interval to a=.6042963902381329 (epoch57). Ordinary restweight is
fixed, density evolves with proper volume; full K(X), J, compression and
all canonical fields are evolved. No filter, equilibrium reset, projection,
halo profile, source holding, new fit, radiation or primordial selection.

Fourth-order two-stage Gauss, exact homogeneous modal tangent as an implicit
preconditioner ONLY; nonlinear stage residual is the entire exact RHS.
Subtract only the analytic-zero homogeneous RHS roundoff (well-balanced
arithmetic), never a physical mode. Fixed point24 iterations,1e-11 relative
per-field stage changes, floor1e-24 in normalized modal variables.
Serial17x512/1024/2048 and33x2048, 150second total bound, checkpoint every
16steps. Gates: time/space state and observables each-prefix1e-4/floor1e-30,
Hamiltonian/background1e-9 and perturbation1e-4, momentum1e-4 normalized to
terms or initial terms; mean scalar charge1e-12. Branch regularity and
positive ordinary volume reported separately. All failed attempts retained.
First compare the analytic modal tangent to central exact-RHS derivatives
at two small amplitudes (1e-5,5e-6), with unchanged1e-4 component gate.
Only proceed if that test passes. This finite development interval cannot
establish permanent saturation, native formation, BTFR or superiority.
"""
from pathlib import Path
import json,math,time
import numpy as np
import invariant_clock_periodic_initial_v002 as initial
import invariant_clock_periodic_exact_v001 as exact
import invariant_clock_periodic_linear_v001 as tangent

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'INVARIANT_CLOCK_PERIODIC_COMPONENTS_V003_RESULT.json'
EXPECTED='c366ac8a6ca2aa8d71ff3d7411e3592d1cd35b52bb96b4fba57957b4c697db39'
OUT=ROOT/'INVARIANT_CLOCK_PERIODIC_EVOLUTION_V001_RESULT.json'
CP=ROOT/'INVARIANT_CLOCK_PERIODIC_EVOLUTION_V001_CHECKPOINT.json'
sha=initial.sha
def clean(v):
    if isinstance(v,np.ndarray):return v.tolist()
    if isinstance(v,np.generic):return v.item()
    raise TypeError(type(v).__name__)

class Integrator:
    def __init__(self,run):
        self.r=run;self.n=run.n;self.M=self.n//2+1;self.scale=tangent.scales(run)
        self.max_stage=0.;self.max_zero=0.;self.max_iterations=0
    def coeff(self,z):return (np.fft.rfft(z/self.scale[:,None],axis=1)/self.n).T
    def grid(self,y):return np.fft.irfft(y.T*self.n,n=self.n,axis=1)*self.scale[:,None]
    def raw_rhs(self,x,y):return self.coeff(self.r.rhs(x,self.grid(y)))
    def step(self,x,y,h):
        off=math.sqrt(3)/6;xa=x+(.5-off)*h;xb=x+(.5+off)*h
        weights=np.array([[.25,.25-off],[.25+off,.25]])
        A=tangent.matrices(self.r,xa);B=tangent.matrices(self.r,xb)
        eye=np.broadcast_to(np.eye(8),(self.M,8,8))
        matrix=np.concatenate([np.concatenate([eye-h*weights[0,0]*A,-h*weights[0,1]*B],axis=2),
            np.concatenate([-h*weights[1,0]*A,eye-h*weights[1,1]*B],axis=2)],axis=1)
        inv=np.linalg.inv(matrix);base=np.concatenate([y,y],axis=1)
        zero=np.zeros_like(y);fzeroa=self.raw_rhs(xa,zero);fzerob=self.raw_rhs(xb,zero)
        self.max_zero=max(self.max_zero,float(np.max(abs(fzeroa))),float(np.max(abs(fzerob))))
        stages=(inv@base[...,None])[...,0]
        for iteration in range(24):
            ya=stages[:,:8];yb=stages[:,8:]
            na=self.raw_rhs(xa,ya)-fzeroa-(A@ya[...,None])[...,0]
            nb=self.raw_rhs(xb,yb)-fzerob-(B@yb[...,None])[...,0]
            right=base+h*np.concatenate([weights[0,0]*na+weights[0,1]*nb,
                weights[1,0]*na+weights[1,1]*nb],axis=1)
            new=(inv@right[...,None])[...,0]
            err=float(np.max(np.max(abs(new-stages),axis=0)/np.maximum(np.max(abs(new),axis=0),1e-24)))
            stages=new
            if err<=1e-11:break
        else:raise ValueError(f'exact nonlinear stage failed fixed iteration bound; relative change {err}')
        self.max_stage=max(self.max_stage,err);self.max_iterations=max(self.max_iterations,iteration+1)
        fa=self.raw_rhs(xa,stages[:,:8])-fzeroa;fb=self.raw_rhs(xb,stages[:,8:])-fzerob
        return y+h*(fa+fb)/2

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
        for N,nstep in ((17,512),(17,1024),(17,2048),(33,2048)):
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
