"""Regular quadratic 2k response from direct canonical action vertices."""
import hashlib
import json
import math
from pathlib import Path
import time
import numpy as np
import dust_clock_mean_work_v001 as mean
from dust_clock_mean_work_v002_refinement import QuinticHistory

HERE=Path(__file__).resolve().parent
OUTPUT=HERE/'DUST_CLOCK_SECOND_HARMONIC_V001_RESULT.json'
PROTOCOL=HERE/'DUST_CLOCK_SECOND_HARMONIC_V001.md'
F,BETA,LAM=mean.F,mean.BETA,mean.LAMBDA
A=3+2/BETA
ELL=mean.transient.reference.ELL_MPC*mean.transient.reference.HREF/mean.transient.reference.C_KMS


def fields(X,count):
    h,r,p,q=X[:4];psi,th,sg,dd=X[4:]
    phase=2*np.pi*np.arange(count)/count
    co,si=np.cos(phase),np.sin(phase)
    f=1/(1+q*q)
    z=-psi+h*sg;n=(psi+dd)/f**2;v=th+sg;s=p*p*sg
    pp=p*p*dd/r-3*h*th-3*psi
    zd=h*n+s/A-r*v/F
    vals=np.array([z*co,n*co,zd*co,p*sg*si,s*co,-p*z*si,
                   -p*n*si,-p*v*si,pp*co,-f*p*n*si,
                   -f*f*p*n*si,-f*p*p*n*co,-f*f*p*p*n*co])
    return vals,phase


def cubic(vals,h,r):
    z,n,zd,w,d,zx,nx,vx,pp,b,lam,bx,lx=vals
    t0=-6*F*h*h
    t1=-12*F*h*zd+4*F*h*d
    t2=-6*F*zd*zd+12*F*h*w*zx+4*F*zd*d-BETA*d*d
    t3=12*F*zd*w*zx-4*F*w*zx*d
    m1=3*z-n;m2=4.5*z*z-3*z*n+n*n
    m3=4.5*z**3-4.5*z*z*n+3*z*n*n-n**3
    kinetic=(t3+m1*t2+m2*t1+m3*t0)/2
    curvature=(n+z)*zx*zx+2*z*nx*zx
    endpoint=-LAM*(4.5*z**3+4.5*n*z*z)
    dust=-2*r*((n+pp-2*z)*vx*vx/2+pp*w*vx)
    acc=(n+z)*(b*b-2*lam*b)+2*z*lam*nx
    acc+=-2*ELL**2*(n-z)*lx*bx+2*ELL**2*zx*(lx*b+lam*bx)
    return kinetic+curvature+endpoint+dust+acc


def vertices(X,count=8,eps=1e-20,target=2):
    vals,phase=fields(X,count)
    h,r,p,q=X[:4]
    co=np.cos(target*phase);si=np.sin(target*phase)
    fp=1/(1+(target*q)**2)
    variations=np.zeros((6,13,count))
    # Qdotz, S_D, Rn, Rz, Q_P, Q_v. The shift test includes D=W_r.
    variations[0,2]=co
    if target:
        variations[1,3]=si/(target*p)
        variations[1,4]=co
    variations[2,1]=co
    variations[2,6]=-target*p*si
    variations[2,9]=-fp*target*p*si
    variations[2,10]=-fp*fp*target*p*si
    variations[2,11]=-fp*(target*p)**2*co
    variations[2,12]=-fp*fp*(target*p)**2*co
    variations[3,0]=co
    variations[3,5]=-target*p*si
    variations[4,8]=co
    variations[5,7]=-target*p*si
    norm=2 if target else 1
    result=[]
    for variation in variations:
        result.append(norm*np.mean(cubic(vals.astype(complex)+1j*eps*variation,h,r)).imag/eps)
    result=np.array(result)
    result[4]/=-2*r
    result[5]/=2*r
    return result


def auxiliary(y,h,r,p,q,source):
    z,v,pi,pp=y
    qd,sd,rn,rz,vs,ps=source
    e=(pi-qd-A*sd)/(2*A)-r*v
    g=p*p/(1+q*q)**2
    n=(h*(pi-qd)-2*(p*p+3*r)*z+2*r*pp-rn)/(2*g)
    d=A*e+2*r/BETA*v+sd/BETA
    return e,n,d


def canonical(y,h,r,p,q,source):
    z,v,pi,pp=y;qd,sd,rn,rz,vs,ps=source
    e,n,d=auxiliary(y,h,r,p,q,source)
    return np.array([e+h*n,n+vs,-3*h*pi+2*p*p*z+2*(p*p+3*r)*n+rz,
                     d-p*p*v+ps])


def chart(X):
    h,r,p,q=X[:4];psi,th,sg,dd=X[4:]
    return np.array([-psi+h*sg,th+sg,2*p*p*sg+6*r*(th+sg),
                     p*p*dd/r-3*h*th-3*psi])


def rhs(x,y,hist):
    X,_=hist.at(x);h,r,p,q=X[:4]
    return canonical(y,h,r,2*p,2*q,vertices(X))/h


def readout(x,y,hist):
    X,_=hist.at(x);h,r,p,q=X[:4]
    vv=vertices(X);e,n,d=auxiliary(y,h,r,2*p,2*q,vv)
    z,v,pi,pp=y
    zz,vv1,pipi,pp1=chart(X)
    density=pp-3*z+2.25*zz*zz-1.5*pp1*zz-p*p*vv1*vv1/4
    return np.array([z,n,pp,2*p*v,d/h,density])


def evolve(hist,steps):
    X,_=hist.at(0.);h,r,p,q=X[:4]
    zi=chart(X)[0]
    z=-3*(p*p+3*r)*zi*zi/(4*(4*p*p+3*r))
    y=np.array([z,0.,-13.5*F*h*zi*zi,0.])
    dx=mean.LENGTH/steps
    states=[];records=[]
    for i in range(steps+1):
        x=i*dx
        if i%(steps//64)==0:
            states.append(y.copy());records.append(readout(x,y,hist))
        if i==steps:
            break
        k1=rhs(x,y,hist);k2=rhs(x+dx/2,y+dx*k1/2,hist)
        k3=rhs(x+dx/2,y+dx*k2/2,hist);k4=rhs(x+dx,y+dx*k3,hist)
        y+=dx*(k1+2*k2+2*k3+k4)/6
        if not np.all(np.isfinite(y)):
            raise ArithmeticError('Nonfinite second harmonic')
    return np.array(states),np.array(records)


def main():
    if OUTPUT.exists():
        raise SystemExit('Refusing to overwrite evidence')
    started=time.perf_counter()
    if hashlib.sha256(mean.INPUT.read_bytes()).hexdigest()!=mean.EXPECTED:
        raise SystemExit('Saved first-order evidence changed')
    original=json.loads(mean.INPUT.read_text())
    controls=[];cases=[]
    def check(name,error,tol):
        controls.append(dict(name=name,error=float(error),tolerance=tol,
                             passed=bool(math.isfinite(error) and error<=tol)))
    names=('z2','n2','canonical_P2','p2_v2','D2_over_H','normal_dust_density2')
    for case in original['cases']:
        hist=QuinticHistory(case);k=hist.k
        errors={s:[] for s in ('linear_chart','mean_vertices','phase_refinement',
                              'complex_step_refinement','dust_sources')}
        linear_peaks=np.zeros(6)
        for x in np.linspace(0.,mean.LENGTH,65):
            X,_=hist.at(x);h,r,p,q=X[:4];psi,th,sg,dd=X[4:]
            flow=mean.tangent(X);hd,rd,pd,qd=flow[:4];psid,thd,sgd,ddd=flow[4:]
            c=chart(X);z,v,pi,pp=c
            actual=canonical(c,h,r,p,q,np.zeros(6))
            expected=chart(X.astype(complex)+1j*1e-20*flow).imag/1e-20
            scale=np.array([abs(psid)+abs(hd*sg)+abs(h*sgd),abs(thd)+abs(sgd),
                            abs(4*p*pd*sg)+abs(2*p*p*sgd)+abs(6*rd*v)+abs(6*r*(thd+sgd)),
                            abs(p*p*ddd/r)+abs((2*pd/p-rd/r)*p*p*dd/r)
                            +abs(3*hd*th)+abs(3*h*thd)+abs(3*psid)])
            errors['linear_chart'].append(np.max(abs(actual-expected)/np.maximum(scale,1e-30)))
            vert=vertices(X);v16=vertices(X,16);veps=vertices(X,eps=1e-25)
            vscl=np.maximum(abs(vert),1e-30)
            errors['phase_refinement'].append(np.max(abs(vert-v16)/vscl))
            errors['complex_step_refinement'].append(np.max(abs(vert-veps)/vscl))
            vm=vertices(X,target=0);ms=mean.sources(X)
            lhs=np.array([vm[0],vm[2],vm[3]]);ref=np.array([ms[1],ms[0],ms[2]])
            errors['mean_vertices'].append(np.max(abs(lhs-ref)/np.maximum(abs(ref),1e-30)))
            n=(1+q*q)**2*(psi+dd)
            dust=np.array([-p*p*v*v/4+p*p*sg*v/2,
                           p*p*(-(pp+n-2*z)*v+pp*sg)])
            # Exactly zero initial dust sources are checked absolutely.
            errors['dust_sources'].append(np.max(abs(vert[4:]-dust)/np.maximum(abs(dust),1e-30)))
            den1=pp-3*z
            linear_peaks=np.maximum(linear_peaks,abs(np.array([z,n,pp,p*v,p*p*sg/h,den1])))
        for name,values in errors.items():
            check(f'{name}:k={k}',max(values),2e-10)
        X,_=hist.at(0.);h,r,p,q=X[:4];zi=chart(X)[0]
        init=np.array([-3*(p*p+3*r)*zi*zi/(4*(4*p*p+3*r)),0.,-13.5*F*h*zi*zi,0.])
        src=vertices(X);ee,nn,dd=auxiliary(init,h,r,2*p,2*q,src)
        scale=max(abs(h*init[2]),abs(2*(4*p*p+3*r)*init[0]),abs(src[2]),1e-30)
        check(f'initial_lapse_constraint:k={k}',abs(nn*2*(4*p*p)/(1+4*q*q)**2)/scale,2e-10)
        check(f'initial_shift_constraint:k={k}',max(abs(ee),abs(dd),abs(src[1]))/max(abs(init[2]),1e-30),2e-10)
        levels=[evolve(hist,nsteps) for nsteps in (256,512,1024)]
        coarse=evolve(QuinticHistory(case,2),1024)
        sf,rf=levels[-1];sm,rm=levels[-2]
        for i,name in enumerate(('z2','v2','pi2','P2')):
            scale=max(np.max(abs(sf[:,i])),1e-30)
            check(f'time_state:k={k}:{name}',np.max(abs(sf[:,i]-sm[:,i]))/scale,2e-5)
            check(f'history_state:k={k}:{name}',np.max(abs(sf[:,i]-coarse[0][:,i]))/scale,2e-4)
        ratios=mean.AMP*np.max(abs(rf),axis=0)/np.maximum(linear_peaks,1e-30)
        for i,name in enumerate(names):
            scale=max(np.max(abs(rf[:,i])),1e-30)
            check(f'time_readout:k={k}:{name}',np.max(abs(rf[:,i]-rm[:,i]))/scale,2e-5)
            check(f'history_readout:k={k}:{name}',np.max(abs(rf[:,i]-coarse[1][:,i]))/scale,2e-4)
            check(f'working_quadratic_fraction:k={k}:{name}',ratios[i],.01)
        cases.append(dict(k_Mpc_inverse=k,readout_names=names,
                          final=dict(zip(names,(rf[-1]*mean.AMP**2).tolist())),
                          peak_absolute=dict(zip(names,(np.max(abs(rf),axis=0)*mean.AMP**2).tolist())),
                          correction_fraction=dict(zip(names,ratios.tolist())),
                          samples=(rf*mean.AMP**2).tolist()))
    result=dict(status='QUALIFIED' if all(c['passed'] for c in controls) else 'FAILED',
                scope='Regular2k canonical response only; not nonlinear Newtonian-gauge observables',
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                protocol_sha256=hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
                linear_input_sha256=mean.EXPECTED,amplitude=mean.AMP,
                controls=controls,cases=cases,elapsed_seconds=time.perf_counter()-started)
    encoded=json.dumps(result,indent=2,allow_nan=False)
    with OUTPUT.open('x') as handle:
        handle.write(encoded+'\n')
    print(json.dumps(dict(status=result['status'],controls=len(controls),
                         failed=[c for c in controls if not c['passed']],
                         cases=[dict(k=c['k_Mpc_inverse'],final=c['final'],fractions=c['correction_fraction']) for c in cases],
                         elapsed_seconds=result['elapsed_seconds']),indent=2))


if __name__=='__main__':
    main()
