"""Qualification of the proposed compression radial/multiplier components.

One small serial worker, no galaxy evolution or parameter fit. cTheta=.01 is
the previously proposed extra coefficient; it is NOT native-derived. Frozen
current joint calibration supplies unchanged K/J and ordinary budgets. H is
divided by sqrt(1+1.5*cTheta), radiation omitted only for this near-present
oracle. No transfer of the former thermal/observational calibration.

Prospective controls: inward kernel log-polynomials degree0..3, value and
R*derivative1e-11; powersR^2/R^4 fine-grid1e-6; coupled2x2 algebra1e-12;
analytic FLRW radial/stress identities1e-9; background RK refinement1e-11;
sixth-order derivative polynomial1e-9; multiplier FLRW accuracy1e-5 and
128/256 refinement1e-6; cancellation/constraint checks1e-9. No success
threshold for physical force. Failures saved exclusively, never overwritten.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import plane_canonical_evolution_v001 as base
import invariant_clock_compression_radial_v001 as radial
import invariant_clock_compression_multiplier_v001 as multiplier

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'INVARIANT_CLOCK_COMPRESSION_COMPONENTS_V001_RESULT.json'
CAL=ROOT/'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json'
CALSHA='c92eb0ce131a61009361f2ead3f4db7522d3eabb22f7e3d472f0e4e0c116c24f'
CT=.01
F=1+1.5*CT
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
maximum=lambda x:float(np.max(np.abs(x)))

def derivative_factory(r):
    """Seven-node physical-radius polynomial derivative; parity at origin."""
    n=len(r); rows=[]
    for i in range(n):
        ids=np.arange(min(i-3,n-7),min(i-3,n-7)+7)
        rr=np.array([r[j] if j>=0 else -r[-j-1] for j in ids])
        h=max(abs(rr-r[i]));xx=(rr-r[i])/h
        w=np.linalg.solve(np.array([xx**k for k in range(7)]),np.eye(7)[1])/h
        rows.append((ids,w))
    def derivative(v,parity):
        sign=1 if parity=='even' else -1
        return np.array([np.dot(w,[v[j] if j>=0 else sign*v[-j-1] for j in ids])
                         for ids,w in rows])
    return derivative

def background(model,x):
    a,s,X,m,K,H,hx,qr=model.bg(float(x))
    return a,s,X,m,K,H/math.sqrt(F),hx,qr

def polar_slice(model,r,subdivisions):
    def rhs(rr,y):
        H,hx=background(model,y[0])[5:7]; B=1-H*H*rr*rr
        return np.array([-H*H*rr/B,-H*H*hx*rr*(1+H*H*rr*rr)/B**2])
    y=np.zeros(2);last=0.;rows=[]
    for end in r:
        count=max(1,math.ceil((end-last)/(r[-1]/subdivisions)))
        h=(end-last)/count
        for j in range(count):
            rr=last+j*h; aa=rhs(rr,y);bb=rhs(rr+h/2,y+h*aa/2)
            cc=rhs(rr+h/2,y+h*bb/2);dd=rhs(rr+h,y+h*cc)
            y+=h*(aa+2*bb+2*cc+dd)/6
        rows.append(y.copy());last=end
    return np.array(rows).T

def oracle(model,r,slice_state):
    x,lnJ=slice_state
    a,s,X,m,K,H,hx,qr=np.array([background(model,xx) for xx in x]).T
    d=model.constitutive(s)[2]; Hd=H*H*hx; B=1-H*H*r*r
    A=1/np.sqrt(B); N=np.exp(lnJ)/A; sig=H*r*A; c=A; u=H*r/B
    tr=-H*r/B;Hr=Hd*tr;Br=-2*H*H*r-2*H*Hr*r*r
    Ar=-Br*A/(2*B);sr=(H+Hr*r)*A-H*r*Br*A/(2*B)
    Xt=-3*H*m/d;Xr=Xt*tr;q=X*A;w=-X*sig;M=m*A
    qR=Xr*A-X*Br*A/(2*B);cur=m*sig;rb=3*model.OB/a**3
    Pb=rb*u/B;rhoB=rb/B;PrB=rb*H*H*r*r/B
    rho0=(X*m+rb)/B-K;Pr0=K+(X*m+rb)*H*H*r*r/B
    j0=(X*m+rb)*u
    chi=-3*CT*H;chir=-3*CT*Hd*tr;tauN=-3*CT*Hd*A
    rhochi=sig*chir/A-chi*chi/(2*CT)
    Prchi=sig*chir/A+chi*chi/(2*CT)-c*tauN
    rhototal=3*H*H-2*Hd*H*H*r*r/B
    Prtotal=-2*Hd/B-3*H*H
    exactg=-H*H*r/B-Hd*r/B**2
    ur=(Hr*r+H)/B-H*r*Br/B**2
    zero=np.zeros(len(r))
    args=dict(R=r,A=A,Ar=Ar,sigma=sig,sigma_R=sr,w=w,M=M,Z=zero,divZ=zero,
        X=X,m=m,d=d,q=q,Q=X,p=zero,e=zero,D=zero,Jcur=cur,jt=zero,
        rhoB=rhoB,PrB=PrB,PtB=zero,P_b=Pb,Pr0=Pr0,chi=chi,chi_R=chir,
        KB=model.KB,C=model.C,cTheta=CT,q_R=qR)
    return locals()

def main():
    if OUT.exists():raise FileExistsError(OUT)
    started=time.monotonic();checks=[];kernels=[];oracles=[]
    def check(name,error,gate):
        checks.append(dict(name=name,error=float(error),gate=gate,passed=bool(error<=gate)))
    if sha(CAL)!=CALSHA:raise ValueError('changed calibration')
    cal=json.loads(CAL.read_text());saved=json.loads(base.SOURCE.read_text())
    for path in (Path(base.__file__),base.SOURCE):
        if sha(path)!=cal['hashes'][str(path)]:raise ValueError('changed constitutive input')
    saved['inherited']=cal['fixed'];model=base.Model(saved,1)
    rate=2/CT
    for kind in ('log0','log1','log2','log3','power2','power4'):
        errors=[]
        for n in (128,256,512):
            r=np.geomspace(.01,1.,n);lr=np.log(r)
            if kind.startswith('log'):
                degree=int(kind[-1]);T=lr**degree
                part=-CT*sum(math.factorial(degree)/math.factorial(degree-j)*lr**(degree-j)/rate**j
                             for j in range(degree+1))
                partlogr=-CT*sum(math.factorial(degree)/math.factorial(degree-j-1)*lr**(degree-j-1)/rate**j
                                  for j in range(degree)) if degree else np.zeros(n)
            else:
                degree=int(kind[-1]);T=r**degree;part=-CT*T/(1-CT*degree/2)
                partlogr=degree*part
            outer=float(part[-1]+.004);hom=.004*np.exp(rate*(lr-lr[-1]))
            exact=part+hom; exactlogr=partlogr+rate*hom
            chi,chir=map(np.array,radial.kernel(r,T,outer,CT))
            err=max(maximum(chi-exact)/max(maximum(exact),CT),
                    maximum(r*chir-exactlogr)/max(maximum(exactlogr),CT))
            errors.append(dict(nodes=n,error=err))
        gate=1e-11 if kind.startswith('log') else 1e-6
        check(kind+'_kernel_fine',errors[-1]['error'],gate)
        kernels.append(dict(kind=kind,errors=errors))
    manufactured=radial.coupledradial_rhs(.21,1.08,-.032,2.7,.019,.021,.107,.003,CT)
    h=manufactured;s=h['sigma'];c=h['c'];R=.21;A=1.08
    residual=[h['A_R']-A*A*R*s*h['chi_R']/2-h['F_A'],
              s*h['A_R']/(A*A*c*c)+R*h['chi_R']/2-(-.032/CT+h['T_star'])]
    check('coupled_algebra',maximum(residual),1e-12)
    for n in (64,128,256):
        r=(np.arange(n)+.5)*.02/n;dr=derivative_factory(r)
        check(f'{n}_even_derivative',maximum(dr(2+3*r*r+.7*r**6,'even')-(6*r+4.2*r**5)),1e-9)
        check(f'{n}_odd_derivative',maximum(dr(r+.2*r**3+.3*r**5,'odd')-(1+.6*r*r+1.5*r**4)),1e-9)
        lo=polar_slice(model,r,1024);hi=polar_slice(model,r,2048)
        check(f'{n}_background_radial',maximum(lo-hi)/maximum(hi),1e-11)
        g=oracle(model,r,hi)
        check(f'{n}_FLRW_density',maximum(g['rho0']+g['rhochi']-g['rhototal'])/maximum(g['rhototal']),1e-9)
        check(f'{n}_FLRW_pressure',maximum(g['Pr0']+g['Prchi']-g['Prtotal'])/maximum(g['Prtotal']),1e-9)
        coupled=[radial.coupledradial_rhs(rr,aa,ch,ro,jo,uu,uuR,0.,CT)
                 for rr,aa,ch,ro,jo,uu,uuR in zip(r,g['A'],g['chi'],g['rho0'],g['j0'],g['u'],g['ur'])]
        check(f'{n}_FLRW_A_R',maximum(np.array([v['A_R'] for v in coupled])-g['Ar'])/maximum(g['Ar']),1e-9)
        check(f'{n}_FLRW_chi_R',maximum(np.array([v['chi_R'] for v in coupled])-g['chir'])/maximum(g['chir']),1e-9)
        solved=multiplier.multipliers(**g['args'],derivative=dr)
        check(f'{n}_FLRW_chi_time',maximum(solved['chi_dot_over_N']-g['tauN'])/maximum(g['tauN']),1e-5)
        check(f'{n}_FLRW_lapse',maximum(solved['lapse_gradient']-g['exactg'])/maximum(g['exactg']),1e-5)
        dg=solved['diagnostics']
        check(f'{n}_chi_constraint',maximum(dg['state_chi_constraint'])/maximum(g['chi']),1e-9)
        check(f'{n}_tau_R_cancellation',maximum(dg['chi_dot_radial_derivative_coefficient']),1e-9)
        check(f'{n}_Hamiltonian_lapse_identity',maximum(dg['raw_minus_on_hamiltonian_L0'])/maximum(solved['coefficients']['L0']),1e-9)
        oracles.append(dict(nodes=n,chi_time_error=maximum(solved['chi_dot_over_N']-g['tauN'])/maximum(g['tauN']),
            lapse_error=maximum(solved['lapse_gradient']-g['exactg'])/maximum(g['exactg']),
            denominator_range=[float(np.min(solved['denominator'])),float(np.max(solved['denominator']))],
            center_denominator_error=float(solved['denominator'][0]-F),
            scalar_Schur_fraction=dg['minimum_scalar_Schur_fraction'],
            R=r.tolist(),tauN=solved['chi_dot_over_N'].tolist(),tauN_exact=g['tauN'].tolist(),
            lapse=solved['lapse_gradient'].tolist(),lapse_exact=g['exactg'].tolist()))
    # Each mesh is compared to its own exact solution, avoiding interpolation
    # contamination when the midpoint grids do not share nodes.
    check('FLRW_time_refinement_error_bound',sum(row['chi_time_error'] for row in oracles[-2:]),1e-6)
    check('FLRW_lapse_refinement_error_bound',sum(row['lapse_error'] for row in oracles[-2:]),1e-6)
    result=dict(protocol=__doc__,fixed=model.p,cTheta=CT,F=F,kernels=kernels,
        manufactured=manufactured,oracles=oracles,controls=checks,
        all_controls_passed=all(row['passed'] for row in checks),
        elapsed_seconds=time.monotonic()-started,
        hashes={str(p):sha(p) for p in (Path(__file__),Path(base.__file__),base.SOURCE,CAL,
                                     Path(radial.__file__),Path(multiplier.__file__))})
    with OUT.open('x') as file:json.dump(result,file,indent=2,allow_nan=False)
    print(json.dumps(dict(all_controls_passed=result['all_controls_passed'],checks=len(checks),
        failed=[row for row in checks if not row['passed']],kernels=kernels,
        oracles=[{k:v for k,v in row.items() if k not in ('R','tauN','tauN_exact','lapse','lapse_exact')} for row in oracles],
        elapsed_seconds=result['elapsed_seconds'],result_sha256=sha(OUT)),indent=2),flush=True)
    if not result['all_controls_passed']:raise SystemExit(1)

if __name__=='__main__':main()
