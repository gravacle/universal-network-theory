"""Audit canceled source comparisons and independently implement cubic Euler terms."""
import hashlib
import json
from pathlib import Path
import time
import numpy as np
import dust_clock_second_harmonic_v001 as base
import dust_clock_mean_work_v002_refinement as interpolation

HERE=Path(__file__).resolve().parent
OUTPUT=HERE/'DUST_CLOCK_SECOND_HARMONIC_V002_AUDIT_RESULT.json'
PROTOCOL=HERE/'DUST_CLOCK_SECOND_HARMONIC_V002_AUDIT.md'


def explicit(X,count=16):
    vals,phase=base.fields(X,count)
    h,r,p,q=X[:4]
    z,n,zd,w,d,zx,nx,vx,pp,b,l,bx,lx=vals
    F,BETA,ell,LAM=base.F,base.BETA,base.ELL,base.LAM
    t0=-6*F*h*h;t1=-12*F*h*zd+4*F*h*d
    t2=-6*F*zd*zd+12*F*h*w*zx+4*F*zd*d-BETA*d*d
    m1=3*z-n;m2=4.5*z*z-3*z*n+n*n
    qzd=(12*F*w*zx+m1*(-12*F*zd+4*F*d)-12*F*h*m2)/2
    qd=(-4*F*w*zx+m1*(4*F*zd-2*BETA*d)+4*F*h*m2)/2
    qu=zx*(12*F*zd-4*F*d+12*F*h*m1)/2-2*r*pp*vx
    qzx=w*(12*F*zd-4*F*d+12*F*h*m1)/2
    qn=-(t2+(3*z-2*n)*t1+(4.5*z*z-6*z*n+3*n*n)*t0)/2
    qz=(3*t2+(9*z-3*n)*t1+(13.5*z*z-9*z*n+3*n*n)*t0)/2
    qn+=zx*zx-4.5*LAM*z*z-r*vx*vx
    qnx=2*z*zx
    qz+=zx*zx+2*nx*zx-LAM*(13.5*z*z+9*n*z)+2*r*vx*vx
    qzx+=2*(n+z)*zx+2*z*nx
    qn+=b*b-2*l*b-2*ell*ell*lx*bx
    qnx+=2*z*l
    qz+=b*b-2*l*b+2*l*nx+2*ell*ell*lx*bx
    qzx+=2*ell*ell*(lx*b+l*bx)
    # First-order b,lambda have only frequency p; retain both auxiliary Euler terms.
    qb=2*((n+z)*(b-l)+ell*ell*((nx-zx)*lx-p*p*(n-z)*l+p*p*z*l))
    ql=2*(-(n+z)*b+z*nx+ell*ell*((nx-zx)*bx-p*p*(n-z)*b+p*p*z*b))
    co,si=np.cos(2*phase),np.sin(2*phase)
    f2=1/(1+4*q*q)
    qzd2=2*np.mean(qzd*co)
    sd=2*np.mean(qd*co+qu*si/(2*p))
    rn=2*np.mean(qn*co-2*p*qnx*si-2*p*(f2*qb+f2*f2*ql)*si)
    rz=2*np.mean(qz*co-2*p*qzx*si)
    psi,theta,sigma,dd=X[4:]
    zz,v,pi,ppstar=base.chart(X)
    nn=(1+q*q)**2*(psi+dd)
    vs=-p*p*v*v/4+p*p*sigma*v/2
    ps=p*p*(-(ppstar+nn-2*zz)*v+ppstar*sigma)
    return np.array([qzd2,sd,rn,rz,vs,ps])


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    if OUTPUT.exists():
        raise SystemExit('Refusing to overwrite an audit')
    started=time.perf_counter()
    prior=json.loads(base.OUTPUT.read_text())
    if prior['status']!='FAILED' or prior['source_sha256']!=digest(base.__file__):
        raise SystemExit('Unexpected predecessor or altered source')
    if prior['protocol_sha256']!=digest(base.PROTOCOL) or digest(base.mean.INPUT)!=base.mean.EXPECTED:
        raise SystemExit('Frozen input changed')
    failures=[c for c in prior['controls'] if not c['passed']]
    if len(failures)!=6 or any(not c['name'].startswith(('phase_refinement:','complex_step_refinement:')) for c in failures):
        raise SystemExit('Unexpected failures; audit cannot qualify this predecessor')
    controls=[c for c in prior['controls'] if c['passed']]
    labels=('Qdotz','S_D','Rn','Rz','Vsrc','Psrc')
    details=[]
    original=json.loads(base.mean.INPUT.read_text())
    for case in original['cases']:
        hist=base.QuinticHistory(case);k=hist.k
        v8=[];v16=[];veps=[];analytic=[]
        for x in np.linspace(0.,base.mean.LENGTH,65):
            X,_=hist.at(x)
            v8.append(base.vertices(X))
            v16.append(base.vertices(X,16))
            veps.append(base.vertices(X,eps=1e-25))
            analytic.append(explicit(X))
        v8=np.array(v8);peaks=np.maximum(np.max(abs(v8),axis=0),1e-30)
        for name,other in (('phase_refinement',v16),('complex_step_refinement',veps),
                           ('independent_explicit_vertices',analytic)):
            absolute=np.max(abs(v8-np.array(other)),axis=0)
            error=absolute/peaks
            for i,label in enumerate(labels):
                controls.append(dict(name=f'{name}:k={k}:{label}',error=float(error[i]),
                                     tolerance=2e-10,passed=bool(np.isfinite(error[i]) and error[i]<=2e-10)))
            details.append(dict(k_Mpc_inverse=k,check=name,
                                absolute_error=dict(zip(labels,absolute.tolist())),
                                denominator=dict(zip(labels,peaks.tolist()))))
    dependencies=[Path(base.__file__),Path(base.mean.__file__),Path(interpolation.__file__),
                  Path(base.mean.transient.__file__),Path(base.mean.transient.reference.__file__)]
    result=dict(status='QUALIFIED' if all(c['passed'] for c in controls) else 'FAILED',
                scope='Combined unchanged regular2k evolution plus corrected and independent source audits',
                source_sha256=digest(__file__),protocol_sha256=digest(PROTOCOL),
                predecessor_sha256=digest(base.OUTPUT),linear_input_sha256=base.mean.EXPECTED,
                dependencies={p.name:digest(p) for p in dependencies},
                preserved_predecessor_failures=failures,controls=controls,audit_details=details,
                unchanged_cases=prior['cases'],elapsed_seconds=time.perf_counter()-started)
    encoded=json.dumps(result,indent=2,allow_nan=False)
    with OUTPUT.open('x') as handle:
        handle.write(encoded+'\n')
    print(json.dumps(dict(status=result['status'],controls=len(controls),
                         failed=[c for c in controls if not c['passed']],
                         max_audit_error=max(c['error'] for c in controls if c['name'].startswith(('phase_refinement:','complex_step_refinement:','independent_explicit_vertices:'))),
                         elapsed_seconds=result['elapsed_seconds']),indent=2))


if __name__=='__main__':
    main()
