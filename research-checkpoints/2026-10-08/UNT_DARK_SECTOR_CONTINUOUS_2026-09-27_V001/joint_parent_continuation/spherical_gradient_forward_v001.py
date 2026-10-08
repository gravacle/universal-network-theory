"""Declared full-mode spherical states; source-only until root release."""
import os
for _key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_key]='1'
import hashlib
import json
import math
from pathlib import Path
import resource
import sys
import time
import numpy as np

ROOT=Path(__file__).resolve().parent
STEM='SPHERICAL_GRADIENT_FORWARD_V001'
A0=1.0059833281731022e-10
GMSUN=1.32712440018e20
PC=648000*149597870700/math.pi
ELL=100*PC
CG=3*math.pi/8
MASSES=(1e7,1e9,1e11)
SPECS=((129,32,200.),(257,32,200.),(257,64,200.),(257,64,400.))
READ=np.array([5.,10.,20.,50.])
DEADLINE=math.inf
CUSTODY={}


def budget():
    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss=rss if sys.platform=='darwin' else 1024*rss
    if time.perf_counter()>DEADLINE or rss>256*1024**2:
        raise RuntimeError('Declared total120s/256MiB ceiling')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def publish(path,obj):
    with path.open('x') as stream:
        json.dump(obj,stream,indent=2,allow_nan=False)
        stream.write('\n')


def spectrum(n):
    x,w=np.polynomial.legendre.leggauss(n)
    s=(x+1)/2
    weights=s*w
    return s,weights,1/(CG**2*s**4)


def modes(g,alpha):
    root=np.sqrt(alpha)[:,None]
    h=root*np.asarray(g)[None,:]
    t=2/math.sqrt(3)*np.sinh(np.arcsinh(3*math.sqrt(3)*h/2)/3)
    return t/root


def local(d,alpha,w):
    d=np.asarray(d,dtype=float)
    lo=np.zeros_like(d)
    hi=4*(d+np.sqrt(d)+1)
    def f(g):
        q=modes(g,alpha)
        return (1-w.sum())*g+np.sum(w[:,None]*alpha[:,None]*q**3,axis=0)
    if np.any(f(hi)<d) or np.any(d<0):
        raise ValueError('Local inverse bracket/source')
    for _ in range(80):
        mid=(lo+hi)/2
        below=f(mid)<d
        lo=np.where(below,mid,lo)
        hi=np.where(below,hi,mid)
    g=np.where(d==0,0.,(lo+hi)/2)
    q=modes(g,alpha)
    return g,q,float(np.max(abs(f(g)-d)/np.maximum(d,1e-30)))


def closed_flux(x):
    # Positive angular integral avoids cancellation of the closed sine formula.
    h=np.asarray(x)/CG
    t=2/math.sqrt(3)*np.sinh(np.arcsinh(3*math.sqrt(3)*h/2)/3)
    th=np.arctan2(1.,t)
    z,w=np.polynomial.legendre.leggauss(32)
    a=th[:,None]*(z+1)/2
    si=np.sin(a)**2
    bracket=th/2*np.sum(w*2*si*(3-2*si),axis=1)
    return CG*h*h*bracket/2


def closed_inverse(d):
    lo=np.zeros_like(d); hi=4*(d+np.sqrt(d)+1)
    for _ in range(80):
        mid=(lo+hi)/2
        below=closed_flux(mid)<d
        lo=np.where(below,mid,lo); hi=np.where(below,hi,mid)
    return (lo+hi)/2


class Grid:
    def __init__(self,n,outer=200.):
        self.h=math.log(2001.)/n
        faces=.1*np.expm1(np.arange(n+1)*self.h)
        faces[-1]=200.
        if outer>200:
            extra=[]; j=n+1
            while .1*math.expm1(j*self.h)<outer:
                extra.append(.1*math.expm1(j*self.h)); j+=1
            faces=np.concatenate((faces,np.array(extra+[outer])))
        self.faces=faces
        self.r=(faces[1:]+faces[:-1])/2
        # Stable exact cell volume in the r^4 measure.
        a,b=faces[:-1],faces[1:]
        self.vol=(b-a)*(b**4+b**3*a+b*b*a*a+b*a**3+a**4)/5
        self.root=np.sqrt(self.vol)
        self.c=faces[1:-1]**4/np.diff(self.r)
        self.co=faces[-1]**4/(faces[-1]-self.r[-1])
        self.diag=np.zeros_like(self.r)
        self.diag[:-1]+=self.c/self.vol[:-1]
        self.diag[1:]+=self.c/self.vol[1:]
        self.diag[-1]+=self.co/self.vol[-1]
        self.off=-self.c/(self.root[:-1]*self.root[1:])

    def minus_lap(self,u,boundary):
        f=self.diag*u
        f[...,1:]-=self.c*u[...,:-1]/self.vol[1:]
        f[...,:-1]-=self.c*u[...,1:]/self.vol[:-1]
        f[...,-1]-=self.co*np.asarray(boundary)/self.vol[-1]
        return f


def factor(diag,off):
    den=diag.copy(); cp=np.empty(len(off))
    for i in range(len(off)):
        if not den[i]>0:
            raise ValueError('Nonpositive tridiagonal pivot')
        cp[i]=off[i]/den[i]
        den[i+1]-=off[i]*cp[i]
    if not den[-1]>0 or np.any(~np.isfinite(den)):
        raise ValueError('Invalid final tridiagonal pivot')
    return den,cp


def solve_tri(fac,off,rhs):
    den,cp=fac
    out=rhs.copy()
    out[0]/=den[0]
    for i in range(1,len(den)):
        out[i]=(out[i]-off[i-1]*out[i-1])/den[i]
    for i in range(len(den)-2,-1,-1):
        out[i]-=cp[i]*out[i+1]
    return out


def schur(diagonals,off,weights,residual):
    n=residual.shape[1]
    ss=np.eye(n); right=np.zeros(n); factors=[]
    for j,(diag,w) in enumerate(zip(diagonals,weights)):
        if j%8==0: budget()
        fac=factor(diag,off); factors.append(fac)
        inv=solve_tri(fac,off,np.eye(n))
        ss-=w*inv
        right-=w*(inv@residual[j])
    symmetry=float(np.max(abs(ss-ss.T))/max(float(np.max(abs(ss))),1e-30))
    if symmetry>1e-10:
        raise ValueError('Schur symmetry control')
    mean=np.linalg.solve((ss+ss.T)/2,right)
    delta=np.stack([solve_tri(fac,off,mean-residual[j]) for j,fac in enumerate(factors)])
    return delta,mean,symmetry


class Problem:
    def __init__(self,n,ns,outer,mass,coefficient=None,zero=False):
        self.grid=Grid(n,outer)
        self.s,self.w,self.alpha=spectrum(ns)
        self.rm=math.sqrt(GMSUN*mass/A0)
        self.lam2=(ELL/self.rm)**2 if coefficient is None else coefficient
        r=self.grid.r
        self.source=np.zeros_like(r) if zero else (r*r+.01)**-1.5
        self.newtonian=r*self.source
        gl,q,err=local(self.newtonian,self.alpha,self.w)
        self.cubic_error=float(np.max(abs(q+self.alpha[:,None]*q**3-gl)/np.maximum(abs(gl),1e-30)))
        self.local=q/r
        self.local_g=self.newtonian+r*np.sum(self.w[:,None]*self.local,axis=0)
        ro=np.array([outer]); do=np.zeros(1) if zero else ro/(ro*ro+.01)**1.5
        go,qo,eo=local(do,self.alpha,self.w)
        self.cubic_error=max(self.cubic_error,float(np.max(abs(qo+self.alpha[:,None]*qo**3-go)/np.maximum(abs(go),1e-30))))
        self.boundary=qo[:,0]/outer
        self.local_inverse_error=max(err,eo)

    def residual(self,u):
        mean=np.sum(self.w[:,None]*u,axis=0)
        diffusion=self.lam2*self.grid.minus_lap(u,self.boundary)
        cubic=self.alpha[:,None]*self.grid.r**2*u**3
        value=diffusion+u+cubic-self.source-mean
        scale=abs(diffusion)+abs(u)+abs(cubic)+abs(self.source)+abs(mean)+1e-30
        return value,scale,float(np.max(abs(value)/scale))

    def direction(self,u,value):
        diag=self.lam2*self.grid.diag+1+3*self.alpha[:,None]*self.grid.r**2*u**2
        d,mean,sym=schur(diag,self.lam2*self.grid.off,self.w,value*self.grid.root)
        return d/self.grid.root,mean/self.grid.root,sym

    def sample(self,arr):
        return np.interp(np.log(READ),np.log(self.grid.r),arr)

    def solve(self):
        u=self.local.copy(); history=[]; status='iteration_limit'; step_a=math.inf
        self.last_u=u; self.last_history=history
        failure=None
        try:
            for iteration in range(32):
                budget()
                value,scale,error=self.residual(u)
                if np.max(abs(value))==0:
                    step_a=0.; status='converged'; break
                du,dmean,sym=self.direction(u,value)
                step_a=float(np.max(abs(self.sample(self.grid.r*dmean))*READ**2/max(self.lam2,1e-300)))
                history.append(dict(iteration=iteration,true_relative_residual=error,
                                    proposed_A_correction=step_a,schur_symmetry=sym))
                if error<=1e-12 and step_a<=1e-4:
                    status='converged'; break
                accepted=False
                for backtrack in range(20):
                    step=2.**(-backtrack)
                    trial=u+step*du
                    _,_,next_error=self.residual(trial)
                    if next_error<error*(1-1e-4*step) or next_error<=1e-12:
                        u=trial; self.last_u=u
                        history[-1]['step']=step; accepted=True; break
                if not accepted:
                    status='line_search_failed'; break
        except Exception as exc:
            # Preserve the last accepted physical vector, including a resource stop.
            status='failed_with_saved_state'; failure=repr(exc)
        value,scale,error=self.residual(u)
        difference=self.grid.r*np.sum(self.w[:,None]*(u-self.local),axis=0)
        delta=self.sample(difference)
        gl=self.sample(self.local_g)
        target_local,_q,_er=local(READ/(READ*READ+.01)**1.5,self.alpha,self.w)
        exact_local=closed_inverse(READ/(READ*READ+.01)**1.5)
        first=self.first_gradient()
        return dict(status=status,failure=failure,
            qualified_newton=bool(status=='converged' and error<=1e-9 and step_a<=1e-4
                                 and self.local_inverse_error<=1e-11 and self.cubic_error<=1e-11),
            true_relative_residual=error,proposed_A_correction=step_a if math.isfinite(step_a) else None,
            history=history,r=self.grid.r.tolist(),faces=self.grid.faces.tolist(),
            spectral_s=self.s.tolist(),spectral_weights=self.w.tolist(),
            source_over_r=self.source.tolist(),outer_mode_u=self.boundary.tolist(),
            local_u=self.local.tolist(),mode_u=u.tolist(),
            normalized_residual=(value/scale).tolist(),raw_residual_max=float(np.max(abs(value))),
            local_scale_max_over_modes=np.max(scale,axis=0).tolist(),local_scale_min=float(np.min(scale)),
            local_inverse_error=self.local_inverse_error,
            local_cubic_forward_error=self.cubic_error,
            readouts=dict(r=READ.tolist(),delta_g_over_a0=delta.tolist(),
                A=(-READ**2*delta/self.lam2).tolist(),
                g_local_same_interpolation_over_a0=gl.tolist(),
                g_full_over_a0=(gl+delta).tolist(),
                g_local_at_exact_readout_over_a0=target_local.tolist(),
                g_local_continuum_over_a0=exact_local.tolist(),
                finite_spectrum_local_relative_difference=(target_local/exact_local-1).tolist(),
                first_gradient_A=first.tolist(),rM_over_R=(1/READ).tolist(),
                gradient_parameter=(self.lam2/READ).tolist()))

    def first_gradient(self):
        r=READ; b2=.01
        d=r/(r*r+b2)**1.5
        dp=(b2-2*r*r)/(r*r+b2)**2.5
        dpp=3*r*(2*r*r-3*b2)/(r*r+b2)**3.5
        g,z,_=local(d,self.alpha,self.w)
        al=1+3*self.alpha[:,None]*z*z
        kl=1-np.sum(self.w[:,None]/al,axis=0)
        klp=np.sum(self.w[:,None]*6*self.alpha[:,None]*z/al**3,axis=0)
        gp=dp/kl; gpp=(dpp-klp*gp*gp)/kl
        bb=np.sum(self.w[:,None]*((gpp+2*gp/r)/al**2-
                  6*self.alpha[:,None]*z*gp*gp/al**4-2*z/(al*r*r)),axis=0)
        return -r*r*bb/kl


def controls():
    out=[]
    def check(name,error,limit):
        out.append(dict(name=name,error=float(error),limit=limit,
                        passed=bool(math.isfinite(error) and error<=limit)))
    p=Problem(17,4,200.,1e9,zero=True)
    v,sc,er=p.residual(np.zeros_like(p.local))
    check('zero_source',np.max(abs(v)),0.)
    p=Problem(17,8,200.,1e9,coefficient=0.)
    check('zero_gradient_matched_local',p.residual(p.local)[2],1e-11)
    check('local_inverse',p.local_inverse_error,1e-11)
    gg=np.array([1e-8,1e-4,1.,1e4])
    zz=modes(gg,p.alpha)
    check('cubic_forward_identity',np.max(abs(zz+p.alpha[:,None]*zz**3-gg)/gg),1e-11)
    rr=np.array([.001,.1,1.,200.])
    enclosed=rr**3/(rr*rr+.01)**1.5
    check('Plummer_enclosed_source_identity',np.max(abs(enclosed/rr**2-rr/(rr*rr+.01)**1.5)),1e-11)
    errors=[]
    for n in (129,257):
        gg=Grid(n)
        r=gg.r
        truth=1/(1+r*r)
        target=(10+2*r*r)/(1+r*r)**3
        got=gg.minus_lap(truth,1/(1+200.**2))
        mask=(r>.2)&(r<5.)
        errors.append(float(np.max(abs(got[mask]-target[mask]))/np.max(abs(target[mask]))))
    check('manufactured_fine',errors[-1],.02)
    check('manufactured_ratio',errors[1]/errors[0],.4)
    n=7; ns=3
    diag=np.array([np.full(n,2.+j*.2) for j in range(ns)])
    off=np.full(n-1,-.2); weights=np.array([.2,.3,.5])
    residual=np.arange(ns*n,dtype=float).reshape(ns,n)/17-0.4
    delta,mean,sym=schur(diag,off,weights,residual)
    full=np.zeros((ns*n,ns*n))
    for j in range(ns):
        h=np.diag(diag[j])+np.diag(off,1)+np.diag(off,-1)
        full[j*n:(j+1)*n,j*n:(j+1)*n]=h
        for k in range(ns):
            full[j*n:(j+1)*n,k*n:(k+1)*n]-=weights[k]*np.eye(n)
    direct=np.linalg.solve(full,-residual.ravel()).reshape(ns,n)
    check('tiny_block_schur',np.max(abs(delta-direct))/max(1.,np.max(abs(direct))),1e-10)
    check('tiny_schur_mean',np.max(abs(np.sum(weights[:,None]*delta,axis=0)-mean)),1e-10)
    check('tiny_schur_symmetry',sym,1e-10)
    check('tiny_unreduced_Newton_residual',np.max(abs(full@delta.ravel()+residual.ravel())),1e-10)
    return out


def main():
    global DEADLINE,CUSTODY
    destination=ROOT/(STEM+'_RESULT.json')
    if destination.exists(): raise FileExistsError(destination)
    existing=list(ROOT.glob(STEM+'_M*_CASE_*.json'))
    if existing: raise FileExistsError('Existing case receipts: '+str(existing))
    started=time.perf_counter(); DEADLINE=started+120
    CUSTODY={p.name:sha(p) for p in (Path(__file__),ROOT/(STEM+'.md'))}
    out=dict(status='started',custody=CUSTODY,inputs=dict(a0=A0,GM_sun=GMSUN,
        ell_pc=100.,masses_Msun=MASSES,specs=SPECS,source_b_over_rM=.1,
        readout_R_over_rM=READ.tolist()),controls=[],cases=[])
    try:
        out['controls']=controls()
        if not all(c['passed'] for c in out['controls']):
            raise RuntimeError('Frozen preflight controls failed; no physical case started')
        for mass in MASSES:
            mass_cases=[]
            for index,(n,ns,outer) in enumerate(SPECS):
                budget()
                p=None
                try:
                    p=Problem(n,ns,outer,mass)
                    case=p.solve()
                except Exception as exc:
                    case=dict(status='failed_before_complete_readout',failure=repr(exc),
                        qualified_newton=False,true_relative_residual=None,readouts=None)
                    if p is not None:
                        case.update(r=p.grid.r.tolist(),faces=p.grid.faces.tolist(),
                            local_u=p.local.tolist(),
                            last_accepted_mode_u=getattr(p,'last_u',p.local).tolist(),
                            history=getattr(p,'last_history',[]))
                case.update(custody=CUSTODY,mass_Msun=mass,spec=[n,ns,outer],
                            rM_metres=math.sqrt(GMSUN*mass/A0),lambda_squared=ELL**2*A0/(GMSUN*mass))
                filename=STEM+'_M'+str(int(mass))+'_CASE_'+str(index)+'.json'
                publish(ROOT/filename,case)
                mass_cases.append(case)
                out['cases'].append(dict(mass_Msun=mass,index=index,filename=filename,
                    sha256=sha(ROOT/filename),status=case['status'],
                    qualified_newton=case['qualified_newton'],true_relative_residual=case['true_relative_residual'],
                    readouts=case['readouts']))
                if case['failure'] is not None:
                    raise RuntimeError('Case state preserved: '+case['failure'])
            for name,left,right in (('mesh',0,1),('spectral',1,2),('domain',2,3)):
                error=float(np.max(abs(np.asarray(mass_cases[left]['readouts']['A'])-
                                       np.asarray(mass_cases[right]['readouts']['A']))))
                out['controls'].append(dict(name=str(mass)+'_'+name+'_A',error=error,limit=.02,passed=bool(error<=.02)))
            r2=np.asarray(mass_cases[2]['r']); r3=np.asarray(mass_cases[3]['r'])
            identical=bool(np.array_equal(r2,r3[:len(r2)]))
            out['controls'].append(dict(name=str(mass)+'_identical_domain_interior',error=0 if identical else 1,limit=0,passed=identical))
        out['all_numerical_controls_pass']=all(c['passed'] for c in out['controls']) and all(c['qualified_newton'] for c in out['cases'])
        out['status']='QUALIFIED_DECLARED_SPHERICAL_STATES' if out['all_numerical_controls_pass'] else 'UNRESOLVED_NUMERICS'
    except Exception as exc:
        out['status']='failed_or_partial'; out['failure']=repr(exc)
        out['all_numerical_controls_pass']=False
    out['elapsed_seconds']=time.perf_counter()-started
    publish(destination,out)
    print(json.dumps(dict(status=out['status'],cases=len(out['cases']),elapsed_seconds=out['elapsed_seconds'],result=str(destination))))
    return 0 if out['all_numerical_controls_pass'] else 2


if __name__=='__main__':
    if sys.argv[1:]!=['--run']:
        raise SystemExit('Explicit --run required; no producer imports or pilot execution.')
    raise SystemExit(main())
