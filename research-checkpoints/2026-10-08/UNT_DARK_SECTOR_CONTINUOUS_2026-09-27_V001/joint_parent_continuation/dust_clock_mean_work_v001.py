"""Complete regular mean projection, reusing the frozen short linear history."""
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np
import dust_clock_short_transient_v001 as transient

HERE = Path(__file__).resolve().parent
INPUT = HERE/'DUST_CLOCK_SHORT_TRANSIENT_V001_RESULT.json'
OUTPUT = HERE/'DUST_CLOCK_MEAN_WORK_V001_RESULT.json'
PROTOCOL = HERE/'DUST_CLOCK_MEAN_WORK_V001.md'
EXPECTED = '489364c23fca12b5b9bbf3fa10774f4f36b1f574ccfe6a25af14bc6202d2ada7'
BETA = transient.reference.BETA
F = 1+1.5*BETA
LAMBDA = 3*(transient.reference.HVAC/transient.reference.HREF)**2
AMP = transient.AMP
LENGTH = transient.LENGTH


def tangent(X):
    h,r,p,q = X[:4]
    return np.concatenate((np.array([-r/F,-3*h*r,-h*p,-h*q]),
                           transient.apply_matrix(X[4:],h,r,p,q)))


def sources(X):
    h,r,p,q = X[:4]
    psi,theta,sigma,dd = X[4:]
    hd,rd,pd,qd,psid,thd,sgd,ddd = tangent(X)
    f = 1/(1+q*q)
    z = -psi+h*sigma
    zd = -psid+hd*sigma+h*sgd
    n = (psi+dd)/f**2
    v = theta+sigma
    s = p*p*sigma
    t0 = -6*F*h*h
    t1 = -12*F*h*zd+4*F*h*s
    t2 = -3*F*zd*zd-6*F*h*s*z+2*F*zd*s-BETA*s*s/2
    constraint = (p*p*z*z/2-9*LAMBDA*z*z/4
                  -(t2+(3*z-2*n)*t1/2
                    +(9*z*z/4-3*z*n+3*n*n/2)*t0)/2
                  -f*f*p*p*n*n/2-r*p*p*v*v/2)
    qdsource = (-6*F*s*z+(3*z-n)*(-12*F*zd+4*F*s)/2
                -12*F*h*(9*z*z/4-3*z*n/2+n*n/2))/2
    qz = ((3*t2+(9*z-3*n)*t1/2
           +(27*z*z/4-9*z*n/2+3*n*n/2)*t0)/2
          +p*p*(z*z/2+n*z)-LAMBDA*(27*z*z/4+9*z*n/2)
          +(5*f*f-4*f**3)*p*p*n*n/2+r*p*p*v*v)
    shear = -p*p*(2*z*z+4*n*z)+2*p*p*n*n*f*f*(1-2*f)+2*r*p*p*v*v
    cross = (3*z-n)*s
    kinetic = p*p*v*v/4
    # Output uses only analytic polynomials/rational functions: complex step
    # differentiates the complete source along its exact first-order flow.
    return np.array([constraint,qdsource,qz,shear,cross,z,zd,n,v,kinetic])


def evaluate(X):
    val = sources(X)
    derivative = sources(X.astype(complex)+1j*1e-20*tangent(X)).imag/1e-20
    return val,derivative


class History:
    def __init__(self, case, stride=1):
        self.k = case['k_Mpc_inverse']
        samples = case['levels'][-1]['samples'][::stride]
        self.grid = np.linspace(0.,LENGTH,len(samples))
        yy,slopes = [],[]
        for x,entry in zip(self.grid,samples):
            _,h,r,p,q,_ = transient.background(x,self.k)
            psi,de,n,pt,ps = np.array(entry['linear'])/AMP
            y = np.array([psi,pt/p,ps/p,r*de/(p*p)])
            yy.append(y)
            slopes.append(transient.apply_matrix(y,h,r,p,q)/h)
        self.yy = np.array(yy)
        self.slopes = np.array(slopes)
        self.dx = self.grid[1]

    def at(self,x):
        i = min(int(max(x,0.)/self.dx),len(self.grid)-2)
        t = (x-self.grid[i])/self.dx
        ya,yb = self.yy[i:i+2]
        va,vb = self.slopes[i:i+2]
        y = ((2*t**3-3*t*t+1)*ya+(-2*t**3+3*t*t)*yb
             +(t**3-2*t*t+t)*self.dx*va+(t**3-t*t)*self.dx*vb)
        dy = ((6*t*t-6*t)*ya+(-6*t*t+6*t)*yb)/self.dx
        dy += (3*t*t-4*t+1)*va+(3*t*t-2*t)*vb
        _,h,r,p,q,_ = transient.background(x,self.k)
        return np.concatenate(([h,r,p,q],y)),dy


def mean_rhs(x,y,history):
    X,_ = history.at(x)
    (c,qd,qz,j,cross,*_),der = evaluate(X)
    h,r = X[:2]
    z,m,chi,ze,we = y
    wd = (der[1]+3*h*qd-qz)/(6*F)-3*h*we
    return np.array([-(6*r*z+c)/(6*F*h*h),j/h-3*m,
                     (m+cross)/(6*h),we/h,wd/h])


def readout(x,y,history):
    X,_ = history.at(x)
    val,der = evaluate(X)
    c,qd,qz,j,cross,z,zd,n,v,ekin = val
    h,r = X[:2]
    z0,m,chi,ze,we = y
    w = -(6*r*z0+c)/(6*F*h)
    wdot = -(der[0]+3*h*c)/(6*F*h)-3*h*w
    volume = z0+.75*z*z
    dh = w+1.5*z*zd
    dhdot = wdot+1.5*(zd*zd+z*der[6])
    dq = -dhdot/h**2-2*r*dh/(F*h**3)
    return np.array([z0,w,chi,(m+cross)/6,volume,dh/h,dq,ze,we])


def evolve(history,steps):
    X,_ = history.at(0.)
    val,_ = evaluate(X)
    h,r = X[:2]
    z0 = -.75*val[5]**2
    w0 = -(6*r*z0+val[0])/(6*F*h)
    state = np.array([z0,0.,0.,z0,w0])
    dx = LENGTH/steps
    records,states = [],[]
    for i in range(steps+1):
        x = i*dx
        if i % (steps//64)==0:
            records.append(readout(x,state,history))
            states.append(state.copy())
        if i==steps:
            break
        k1=mean_rhs(x,state,history)
        k2=mean_rhs(x+dx/2,state+dx*k1/2,history)
        k3=mean_rhs(x+dx/2,state+dx*k2/2,history)
        k4=mean_rhs(x+dx,state+dx*k3,history)
        state+=dx*(k1+2*k2+2*k3+k4)/6
        if not np.all(np.isfinite(state)):
            raise ArithmeticError('Nonfinite projected mean state')
    return np.array(states),np.array(records)


def main():
    if OUTPUT.exists():
        raise SystemExit('Refusing to overwrite a scientific receipt')
    started=time.perf_counter()
    if hashlib.sha256(INPUT.read_bytes()).hexdigest()!=EXPECTED:
        raise SystemExit('Frozen linear-history receipt changed')
    original=json.loads(INPUT.read_text())
    controls=[]
    def check(name,error,tol):
        controls.append(dict(name=name,error=float(error),tolerance=tol,
                             passed=bool(math.isfinite(error) and error<=tol)))
    labels=('z0','zdot0','chi0','chidot0','log_volume_scale',
            'delta_H_over_H','delta_q','z0_spatial_eq','zdot0_spatial_eq')
    cases=[]
    for case in original['cases']:
        hist=History(case)
        k=hist.k
        ward=[];dust=[];fd=[];defects=[]
        for x in np.linspace(0.,LENGTH,65):
            X,_=hist.at(x)
            val,der=evaluate(X)
            h,r,p,q=X[:4]
            c,qd,qz,j,cross,z,zd,n,v,ek=val
            terms=np.array([der[0],3*h*c,h*der[1],3*h*h*qd,-h*qz])
            ward.append(abs(np.sum(terms))/max(np.sum(abs(terms)),1e-30))
            dt=np.array([der[9],2*h*ek,-p*p*v*n/2])
            dust.append(abs(sum(dt))/max(sum(abs(dt)),1e-30))
            if x>0.:
                eps=1e-5
                centered=(sources(X+eps*tangent(X))-sources(X-eps*tangent(X)))/(2*eps)
                for index in (0,1):
                    fd.append(abs(centered[index]-der[index])/max(abs(der[index]),1e-30))
        for x in (np.arange(64)+.37)*LENGTH/64:
            X,dx=hist.at(x)
            exact=tangent(X)[4:]/X[0]
            # Scale each component by its finite sum of matrix-term sizes.
            h,r,p,q=X[:4]; psi,th,sg,dd=X[4:]
            u=(1+q*q)**2
            scale=np.array([abs(h*psi)+abs(r/F*th)+abs(p*p*sg/(3+2/BETA)),
                            abs(psi),abs((u-1)*psi)+abs(u*dd),
                            abs(h*dd)+abs(r*th)+abs(3*r*sg/(3+2/BETA))])/h
            defects.append(np.max(abs(dx-exact)/np.maximum(scale,1e-30)))
        check(f'work_identity:k={k}',max(ward),2e-10)
        check(f'dust_lapse_work:k={k}',max(dust),2e-10)
        check(f'directional_derivative:k={k}',max(fd),2e-5)
        check(f'history_differential_defect:k={k}',max(defects),2e-5)
        levels=[evolve(hist,n) for n in (256,512,1024)]
        coarse=evolve(History(case,2),1024)
        sf,rf=levels[-1];sm,rm=levels[-2]
        for i,name in enumerate(('z0','shear_momentum','chi0','z0_spatial','zdot0_spatial')):
            scale=max(np.max(abs(sf[:,i])),1e-30)
            check(f'time:k={k}:{name}',np.max(abs(sf[:,i]-sm[:,i]))/scale,2e-5)
            check(f'history_refinement:k={k}:{name}',np.max(abs(sf[:,i]-coarse[0][:,i]))/scale,2e-4)
        for i,name in enumerate(labels):
            scale=max(np.max(abs(rf[:,i])),1e-30)
            check(f'readout_history:k={k}:{name}',np.max(abs(rf[:,i]-coarse[1][:,i]))/scale,2e-4)
        check(f'independent_volume:k={k}',np.max(abs(rf[:,0]-rf[:,7]))/max(np.max(abs(rf[:,0])),1e-30),2e-4)
        check(f'independent_volume_velocity:k={k}',np.max(abs(rf[:,1]-rf[:,8]))/max(np.max(abs(rf[:,1])),1e-30),2e-4)
        check(f'initial_proper_volume:k={k}',abs(rf[0,4]),1e-30)
        zero,_=hist.at(0.);zero[4:]=0.
        check(f'zero_source:k={k}',np.max(abs(sources(zero))),0.)
        physical=rf*AMP**2
        cases.append(dict(k_Mpc_inverse=k,steps=1024,snapshot_count=65,
                          readout_names=labels,final=dict(zip(labels,physical[-1].tolist())),
                          peak_absolute=dict(zip(labels,np.max(abs(physical),axis=0).tolist())),
                          samples=physical.tolist()))
    result=dict(status='QUALIFIED' if all(c['passed'] for c in controls) else 'FAILED',
                scope='Complete regular quadratic mean projection only; 2k and observer optics remain',
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                protocol_sha256=hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
                input_sha256=EXPECTED,physical_amplitude=AMP,
                controls=controls,cases=cases,elapsed_seconds=time.perf_counter()-started)
    encoded=json.dumps(result,indent=2,allow_nan=False)
    with OUTPUT.open('x') as handle:
        handle.write(encoded+'\n')
    print(json.dumps(dict(status=result['status'],controls=len(controls),
                         failed=[c for c in controls if not c['passed']],
                         cases=[dict(k=c['k_Mpc_inverse'],final=c['final'],peak=c['peak_absolute']) for c in cases],
                         elapsed_seconds=result['elapsed_seconds']),indent=2))


if __name__=='__main__':
    main()
