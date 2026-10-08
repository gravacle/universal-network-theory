"""Refine failed numerical audits; frozen mean action and physical inputs."""
import hashlib
import json
import math
from pathlib import Path
import time
import numpy as np
import dust_clock_mean_work_v001 as base

HERE=Path(__file__).resolve().parent
OUTPUT=HERE/'DUST_CLOCK_MEAN_WORK_V002_RESULT.json'
PROTOCOL=HERE/'DUST_CLOCK_MEAN_WORK_V002_REFINEMENT.md'


class QuinticHistory(base.History):
    def __init__(self,case,stride=1):
        super().__init__(case,stride)
        self.coefficients=[]
        second=[]
        for x,y in zip(self.grid,self.yy):
            _,h,r,p,q,_=base.transient.background(x,self.k)
            X=np.concatenate(([h,r,p,q],y))
            xt=base.tangent(X)
            xdd=base.tangent(X.astype(complex)+1j*1e-20*xt).imag/1e-20
            second.append(xdd[4:]/h**2-xt[4:]*xt[0]/h**3)
        for i in range(len(self.grid)-1):
            c0=self.yy[i];c1=self.dx*self.slopes[i]
            c2=.5*self.dx**2*second[i]
            r0=self.yy[i+1]-c0-c1-c2
            r1=self.dx*self.slopes[i+1]-c1-2*c2
            r2=self.dx**2*second[i+1]-2*c2
            self.coefficients.append(np.array([c0,c1,c2,10*r0-4*r1+.5*r2,
                                               -15*r0+7*r1-r2,6*r0-3*r1+.5*r2]))

    def at(self,x):
        i=min(int(max(x,0.)/self.dx),len(self.grid)-2)
        t=(x-self.grid[i])/self.dx
        cc=self.coefficients[i]
        y=cc[0]+t*(cc[1]+t*(cc[2]+t*(cc[3]+t*(cc[4]+t*cc[5]))))
        dy=(cc[1]+t*(2*cc[2]+t*(3*cc[3]+t*(4*cc[4]+t*5*cc[5]))))/self.dx
        _,h,r,p,q,_=base.transient.background(x,self.k)
        return np.concatenate(([h,r,p,q],y)),dy


ORIGINAL_READOUT=base.readout
def consistent_readout(x,y,history):
    result=ORIGINAL_READOUT(x,y,history)
    X,_=history.at(x)
    z=base.sources(X)[5]
    result[4]=y[0]+.75*z**2
    return result


def main():
    if OUTPUT.exists():
        raise SystemExit('Refusing to overwrite result')
    started=time.perf_counter()
    if hashlib.sha256(base.INPUT.read_bytes()).hexdigest()!=base.EXPECTED:
        raise SystemExit('Original linear receipt changed')
    original=json.loads(base.INPUT.read_text())
    prior=json.loads(base.OUTPUT.read_text())
    if prior['status']!='FAILED':
        raise SystemExit('Expected preserved failed predecessor')
    base.readout=consistent_readout
    controls=[]
    def check(name,error,tol):
        controls.append(dict(name=name,error=float(error),tolerance=tol,
                             passed=bool(math.isfinite(error) and error<=tol)))
    labels=('z0','zdot0','chi0','chidot0','log_volume_scale',
            'delta_H_over_H','delta_q','z0_spatial_eq','zdot0_spatial_eq')
    cases=[]
    for case in original['cases']:
        hist=QuinticHistory(case);k=hist.k
        ward=[];dust=[];fd1=[];fd2=[];fdcompare=[];defects=[]
        for x in np.linspace(0.,base.LENGTH,65):
            X,_=hist.at(x);val,der=base.evaluate(X)
            h,r,p,q=X[:4]
            c,qd,qz,j,cross,z,zd,n,v,ek=val
            terms=np.array([der[0],3*h*c,h*der[1],3*h*h*qd,-h*qz])
            ward.append(abs(sum(terms))/max(sum(abs(terms)),1e-30))
            dt=np.array([der[9],2*h*ek,-p*p*v*n/2])
            dust.append(abs(sum(dt))/max(sum(abs(dt)),1e-30))
            if x>0.:
                estimates=[]
                for eps,errors in ((1e-6,fd1),(5e-7,fd2)):
                    vv=base.tangent(X)
                    center=(base.sources(X+eps*vv)-base.sources(X-eps*vv))/(2*eps)
                    estimates.append(center)
                    for index in (0,1):
                        errors.append(abs(center[index]-der[index])/max(abs(der[index]),1e-30))
                for index in (0,1):
                    fdcompare.append(abs(estimates[0][index]-estimates[1][index])/max(abs(der[index]),1e-30))
        for x in (np.arange(64)+.37)*base.LENGTH/64:
            X,dx=hist.at(x);h,r,p,q=X[:4];psi,th,sg,dd=X[4:]
            exact=base.tangent(X)[4:]/h;u=(1+q*q)**2
            scale=np.array([abs(h*psi)+abs(r/base.F*th)+abs(p*p*sg/(3+2/base.BETA)),
                            abs(psi),abs((u-1)*psi)+abs(u*dd),
                            abs(h*dd)+abs(r*th)+abs(3*r*sg/(3+2/base.BETA))])/h
            defects.append(np.max(abs(dx-exact)/np.maximum(scale,1e-30)))
        for name,errors,tol in (('work_identity',ward,2e-10),('dust_lapse_work',dust,2e-10),
                                ('directional_derivative_1e-6',fd1,2e-5),
                                ('directional_derivative_5e-7',fd2,2e-5),
                                ('directional_derivative_refinement',fdcompare,2e-5),
                                ('history_differential_defect',defects,2e-5)):
            check(f'{name}:k={k}',max(errors),tol)
        levels=[base.evolve(hist,n) for n in (256,512,1024)]
        coarse=base.evolve(QuinticHistory(case,2),1024)
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
        check(f'zero_source:k={k}',np.max(abs(base.sources(zero))),0.)
        physical=rf*base.AMP**2
        cases.append(dict(k_Mpc_inverse=k,steps=1024,snapshot_count=65,
                          readout_names=labels,final=dict(zip(labels,physical[-1].tolist())),
                          peak_absolute=dict(zip(labels,np.max(abs(physical),axis=0).tolist())),
                          samples=physical.tolist()))
    result=dict(status='QUALIFIED' if all(c['passed'] for c in controls) else 'FAILED',
                scope='Regular quadratic mean sector only; 2k and observer optics remain',
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                frozen_engine_sha256=hashlib.sha256(Path(base.__file__).read_bytes()).hexdigest(),
                predecessor_sha256=hashlib.sha256(base.OUTPUT.read_bytes()).hexdigest(),
                protocol_sha256=hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
                input_sha256=base.EXPECTED,physical_amplitude=base.AMP,
                controls=controls,cases=cases,elapsed_seconds=time.perf_counter()-started,
                time_unit='1/Href; zdot0,chidot0 are normalized to Href')
    encoded=json.dumps(result,indent=2,allow_nan=False)
    with OUTPUT.open('x') as handle:
        handle.write(encoded+'\n')
    print(json.dumps(dict(status=result['status'],controls=len(controls),
                         failed=[c for c in controls if not c['passed']],
                         cases=[dict(k=c['k_Mpc_inverse'],final=c['final'],peak=c['peak_absolute']) for c in cases],
                         elapsed_seconds=result['elapsed_seconds']),indent=2))


if __name__=='__main__':
    main()
