"""Bounded first-constitutive-nonlinearity assembly test, NOT a galaxy model.

Same current K(X)/J/cTheta=.01,20kpc comoving wavelength convention. Start
from qualified assemblyV004 epoch54 (a=.4869675), equal-contrast seed times
1e-12. This is an ILLUSTRATIVE diagnostic amplitude, not fitted primordial
power. Evolve to epoch57 (a=.6042964). Retain ordinary/field velocities,
phases and all J-generated harmonics; no held source or equilibrium reset.

Reviewed semilinear insertion: p=grad(rel), NJ=-C*j*p, nJ=grad^-1 NJ.
Add -div NJ to dm_dot and Q*nJ to Z_dot. Other six-field equations unchanged.
This preserves retained-order charge/Phi_dot, NOT exact nonlinear gravity.
Report omitted ordinary advection/Euler, norm/Bernoulli, charge-current and
stress estimates against surviving equation terms. Separate1% asymptotic
ceiling; crossing is an approximation limit, not a physical exclusion or
permission to relax it. No Stage3/observational claim from this diagnostic.

Periodic reflection-symmetric cosine prep, zero means. Spectral Galerkin
J evaluated on3N points; grids33/65. Implicit2-stage order4 Gauss with
full stage fixed-point solve (1e-11,16iterations); no fast-mode filter.
Serial33x512/1024/2048 and65x2048. Full physical fields/observables all
PREFIX refinement1e-4/floor1e-30; retained identities1e-10. 160s wall bound,
checkpoint every64 steps, exclusive result. Failed controls preserved.
"""
from pathlib import Path
import hashlib,json,math,time
import numpy as np
import invariant_clock_compression_assembly_v001 as linear

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'INVARIANT_CLOCK_COMPRESSION_ASSEMBLY_V004_RESULT.json'
OUT=ROOT/'INVARIANT_CLOCK_SEMILINEAR_ASSEMBLY_V001_RESULT.json'
CP=ROOT/'INVARIANT_CLOCK_SEMILINEAR_ASSEMBLY_V001_CHECKPOINT.json'
EXPECTED='7ed429224a93aaef44c97dc2bdaedce5c2f3fc7b685ceb863ae99c91fc9f304b'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

class Periodic:
    def __init__(self,model,N):
        self.m=model;self.N=N;self.M=N//2+1;self.n=np.arange(self.M)
        self.runs=[linear.Assembly(model) for _ in range(self.M)]
        for n,run in enumerate(self.runs[1:],1):
            run.k*=n;run.scale[[1,2,3,5]]/=n*n
        self.scale=np.array([r.scale for r in self.runs]);self.max_stage=0.;self.max_nl_identity=0.
    def bg(self,x):return self.runs[0].bg(x)
    def grid(self,f,N=None):
        N=N or self.N;pad=np.zeros((N//2+1,)+f.shape[1:],complex);pad[:len(f)]=f
        return np.fft.irfft(pad*N,n=N,axis=0)
    def coeff(self,f):return np.fft.rfft(f,axis=0)/len(f)
    def matrices(self,x):return np.array([r.matrix(x) for r in self.runs[1:]])
    def nonlinear(self,x,y):
        a,Q,m,d,H,Hd,Hdx,rb,k2=self.bg(x);wave=np.sqrt(k2)*self.n
        rel=y[:,1]*self.scale[:,1];p=self.grid(1j*wave*rel,3*self.N)
        j=self.m.lam*abs(p)/np.sqrt(p*p+self.m.bs**2)
        nj=self.coeff(-self.m.C*j*p)[:self.M]
        out=np.zeros_like(y);dm=-1j*wave[1:]*nj[1:];Z=Q*nj[1:]/(1j*wave[1:])
        out[1:,0]=dm/self.scale[1:,0]/H;out[1:,3]=Z/self.scale[1:,3]/H
        defect=Z/2-Q*dm/(2*wave[1:]**2)
        den=abs(Z/2)+abs(Q*dm/(2*wave[1:]**2))
        self.max_nl_identity=max(self.max_nl_identity,float(np.max(abs(defect)/np.maximum(den,1e-100))))
        return out
    def step(self,x,y,h):
        q=math.sqrt(3)/6;c1=.5-q;c2=.5+q
        aa=np.array([[.25,.25-q],[.25+q,.25]])
        A1=self.matrices(x+c1*h);A2=self.matrices(x+c2*h)
        eye=np.broadcast_to(np.eye(6),(self.M-1,6,6))
        K=np.concatenate((np.concatenate((eye-h*aa[0,0]*A1,-h*aa[0,1]*A2),axis=2),
                          np.concatenate((-h*aa[1,0]*A1,eye-h*aa[1,1]*A2),axis=2)),axis=1)
        inv=np.linalg.inv(K);base=np.concatenate((y[1:],y[1:]),axis=1)
        stages=(inv@base[...,None])[...,0]
        for iteration in range(16):
            Y1=np.zeros_like(y);Y2=np.zeros_like(y);Y1[1:]=stages[:,:6];Y2[1:]=stages[:,6:]
            N1=self.nonlinear(x+c1*h,Y1)[1:];N2=self.nonlinear(x+c2*h,Y2)[1:]
            right=base+h*np.concatenate((aa[0,0]*N1+aa[0,1]*N2,aa[1,0]*N1+aa[1,1]*N2),axis=1)
            nextst=(inv@right[...,None])[...,0]
            err=float(np.max(np.max(abs(nextst-stages),axis=0)/np.maximum(np.max(abs(nextst),axis=0),1e-30)))
            stages=nextst
            if err<=1e-11:break
        else:raise ValueError('implicit nonlinear stage did not converge')
        self.max_stage=max(self.max_stage,err)
        Y1[1:]=stages[:,:6];Y2[1:]=stages[:,6:]
        f1=(A1@Y1[1:,:,None])[...,0]+self.nonlinear(x+c1*h,Y1)[1:]
        f2=(A2@Y2[1:,:,None])[...,0]+self.nonlinear(x+c2*h,Y2)[1:]
        result=y.copy();result[1:]+=h*(f1+f2)/2
        if not np.all(np.isfinite(result)):raise ValueError('nonfinite state')
        return result
    def diagnose(self,x,y):
        a,Q,m,d,H,Hd,Hdx,rb,k2=self.bg(x);wave=np.sqrt(k2)*self.n
        dm,rel,alpha,Z,db,theta=(y*self.scale).T;phi=rel-Q*alpha
        qb=m*phi+rb*theta;Phi=np.zeros(self.M,complex)
        Phi[1:]=Z[1:]/2-(Q*dm[1:]+rb*db[1:]+3*H*qb[1:])/(2*wave[1:]**2)
        chi=.01/1.015*(1.5*qb+wave**2*alpha);E=(Z-self.m.C*rel)/self.m.KB
        NP=3*self.N;g=lambda f:self.grid(f,NP);der=lambda f:g(1j*wave*f)
        w=der(phi);v=der(alpha);p=der(rel);ee=der(E);vb=-der(theta)
        j=self.m.lam*abs(p)/np.sqrt(p*p+self.m.bs**2)
        D=self.m.C*(ee-(1+j)*p);current=D-m/Q*w
        dmgrid=g(dm);dbgrid=g(db);Phigrid=g(Phi);mx=lambda f:float(np.max(abs(f)))
        # Omitted equation-term estimates, not hidden inside numerical accuracy.
        fluxcoef=self.coeff(dbgrid*vb)[:self.M]
        adv=der(fluxcoef);pdot=(qb-chi)/2-H*Phi
        dbdot=3*pdot-wave**2*theta
        norm=mx(d*w*w/(2*Q))/max(mx(dmgrid),1e-100)
        advratio=mx(adv)/max(mx(g(dbdot)),1e-100)
        eulerratio=mx(vb*vb/2)/max(mx(Phigrid),1e-100)
        missing_current=-dmgrid*w/Q+(v*v/2)*D
        currratio=mx(missing_current)/max(mx(current),1e-100)
        zz=abs(p)/self.m.bs
        JJ=self.m.lam*self.m.bs**2*(zz*np.sqrt(1+zz*zz)-np.arcsinh(zz))
        small=zz<.01;JJ[small]=self.m.lam*self.m.bs**2*(2*zz[small]**3/3-zz[small]**5/5+3*zz[small]**7/28)
        stress=self.m.KB*ee*ee+self.m.C*p*p+self.m.C*JJ+d*(dmgrid/d)**2+rb*vb*vb
        stressratio=mx(stress)/max(mx(g(-2*wave**2*Phi)),1e-100)
        s=self.m.bg(x)[1];qr=Q/self.m.Q0;cap=math.sqrt(1+self.m.eps)
        upper=self.m.Q0*self.m.eps/((1+s)*(cap+qr));lower=self.m.Q0*self.m.eps*s/((1+s)*(qr+1))
        validity=dict(ordinary_contrast=mx(dbgrid),clock_contrast=mx(dmgrid/m),
            norm_correction=norm,ordinary_advection=advratio,ordinary_Euler=eulerratio,
            omitted_current=currratio,omitted_stress=stressratio,
            branch_shift=mx(dmgrid/d-w*w/(2*Q))/min(upper,lower),vector_tilt=mx(v))
        jt=self.m.lam*abs(p)*(p*p+2*self.m.bs**2)/(p*p+self.m.bs**2)**1.5
        stiffness=(m/Q+self.m.C*jt)*k2/(d*Q*Q)
        state=np.array([self.grid(f) for f in (dm,phi,alpha,Z,db,theta)])
        obs=np.array([self.grid(f) for f in (Phi,db,theta,dm/m,dm/m-db,1j*wave*rel,E,chi)])
        return dict(a=a,state=state.tolist(),observables=obs.tolist(),validity=validity,
            within_declared_asymptotic_ceiling=max(validity.values())<=.01,
            potential_fundamental=float(2*Phi[1].real),density_fundamental=float(2*db[1].real),
            max_Cj_over_mu=mx(self.m.C*j/(m/Q)),soft_stiffness_ratio_range=[float(stiffness.min()),float(stiffness.max())],
            retained_charge_mean=float((a**3*(dm[0]-3*m*Phi[0])).real),
            max_J=float(np.max(JJ)),max_abs_p=mx(p))

def compare(left,right,key):
    a=np.array([s[key] for s in left['snapshots']]);b=np.array([s[key] for s in right['snapshots']])
    if a.shape[-1]!=b.shape[-1]:
        n=a.shape[-1];N=b.shape[-1];f=np.fft.rfft(a,axis=-1)/n
        p=np.zeros(a.shape[:-1]+(N//2+1,),complex);p[...,:len(f[0,0])]=f
        a=np.fft.irfft(p*N,n=N,axis=-1)
    errors=[]
    for i in range(1,len(a)):
        num=np.max(abs(a[:i+1]-b[:i+1]),axis=(0,2));den=np.maximum(np.max(abs(b[:i+1]),axis=(0,2)),1e-30)
        errors.append(float(np.max(num/den)))
    return dict(maximum=max(errors),prefix=errors)

def main():
    if OUT.exists() or CP.exists():raise FileExistsError('exclusive result/checkpoint exists')
    if sha(SOURCE)!=EXPECTED:raise ValueError('changed phase evidence')
    parent=json.loads(SOURCE.read_text())
    if not parent['all_controls_passed']:raise ValueError('unqualified initial history')
    for path,digest in parent['dependencies'].items():
        if sha(Path(path))!=digest:raise ValueError('changed equations')
    saved=json.loads(linear.linear.old.base.SOURCE.read_text());saved['inherited']=parent['fixed']
    model=linear.linear.old.base.Model(saved,1);ss=parent['histories'][-1]['snapshots']
    first=ss[54];x0=math.log(first['a']);end=math.log(ss[57]['a']);rows=[];error=None;started=time.monotonic()
    try:
        for N,nstep in ((33,512),(33,1024),(33,2048),(65,2048)):
            run=Periodic(model,N);y=np.zeros((run.M,6),complex)
            dm,phi,alpha,Z,db,theta=np.array(first['state'])[:,1]*1e-12
            Q=run.bg(x0)[1];y[1]=np.array([dm,phi+Q*alpha,alpha,Z,db,theta])/run.scale[1]/2
            snaps=[];h=(end-x0)/nstep
            for i in range(nstep+1):
                x=x0+i*h
                if i%(nstep//32)==0:snaps.append(run.diagnose(x,y))
                if i%64==0:
                    with CP.open('w') as f:json.dump(dict(producer_sha256=sha(Path(__file__)),N=N,nstep=nstep,
                        accepted_step=i,x=x,state_real=y.real.tolist(),state_imag=y.imag.tolist(),completed_rows=rows,snapshots=snaps),f,allow_nan=False)
                if i==nstep:break
                y=run.step(x,y,h)
                if time.monotonic()-started>160:raise TimeoutError('160s serial bound; checkpoint retained')
            row=dict(nodes=N,steps=nstep,snapshots=snaps,max_stage=run.max_stage,nonlinear_constraint_identity=run.max_nl_identity,
                Einstein_derivative=max(r.max_constraint for r in run.runs));rows.append(row)
            print(json.dumps(dict(nodes=N,steps=nstep,elapsed=time.monotonic()-started,
                final={k:v for k,v in snaps[-1].items() if k not in ('state','observables')})),flush=True)
    except Exception as exc:error=dict(type=type(exc).__name__,message=str(exc))
    checks=[];comparisons={}
    if len(rows)==4:
        for label,left,right in (('time',rows[1],rows[2]),('space',rows[2],rows[3])):
            for key in ('state','observables'):
                val=compare(left,right,key);comparisons[label+'_'+key]=val
                checks.append(dict(name=label+'_'+key,error=val['maximum'],gate=1e-4,passed=val['maximum']<=1e-4))
        for key in ('nonlinear_constraint_identity','Einstein_derivative'):
            e=max(r[key] for r in rows);checks.append(dict(name=key,error=e,gate=1e-10,passed=e<=1e-10))
    result=dict(protocol=__doc__,producer_sha256=sha(Path(__file__)),source_sha256=EXPECTED,
        dependencies={str(Path(linear.__file__)):sha(Path(linear.__file__))},fixed=parent['fixed'],cTheta=.01,width_kpc=20.,
        initial_epoch=54,end_epoch=57,illustrative_amplitude=1e-12,rows=rows,error=error,comparisons=comparisons,checks=checks,
        all_numerical_controls_passed=error is None and len(rows)==4 and all(c['passed'] for c in checks),
        exact_nonlinear_model=False,galaxy_prediction=False,observational_superiority=False,elapsed_seconds=time.monotonic()-started)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(dict(checks=checks,error=error,all_pass=result['all_numerical_controls_passed'],sha256=sha(OUT)),indent=2),flush=True)
    if not result['all_numerical_controls_passed']:raise SystemExit(1)

if __name__=='__main__':main()
