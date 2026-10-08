"""Local stationary-center diagnostic, NOT a galaxy solution or fit.

Same K(X), cTheta=.01 and inherited source central density. Independently
derived regular, zero-current, no-ordinary-radial-flux center identities:
w1=q*(rho+q*m+2*K+6*F*sigma1**2)/(3*m),
g1=(1+mu/C)*w1+q*sigma1-sigma1**2,
X**2=q**2-(q**2*g1+w1**2)*R**2+O(R**4).
Circular-source radial pressure is zero. These are a LOCAL stationary
necessary screen; exact FLRW has nonzero current and cannot be attached
to this solution without time terms. The initial density is a diagnostic
reference, not a fixed-density/retuned-angular-momentum equilibrium.

Vary the central charge to the prospectively stated LOCAL q*m/rho ratios
1e-4,1e-3,.01,.03,.1,1 plus inherited cosmic m. This is not a halo fit:
none is selected as a physical initial condition. Minimize the local
X-squared curvature over sigma1 analytically via its unique cubic root.
The resulting Taylor radius is NOT a true branch radius or stability gate.
No observational comparison, theory promotion, or coefficient tuning.
Numerical gates frozen here: center identities and cubic stationarity1e-10;
finite-difference curvature1e-5. No integration or long worker.
"""
from pathlib import Path
import hashlib
import json
import math

ROOT=Path(__file__).resolve().parent
INPUT=ROOT/'INVARIANT_CLOCK_COMPRESSION_COMPARE_grid256_512_v001_RESULT.json'
INPUT_SHA='8c12ff88ca86ccd0dbb92c1f38933c598c2754fbabee2ec9da41df8959c591f0'
OUTPUT=ROOT/'INVARIANT_CLOCK_STATIONARY_CENTER_V001_RESULT.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
Q0=100.;EPS=1e-6;OA=.7;KB=.02;C=2-KB;CT=.01;F=1+1.5*CT
DEN=1/EPS-math.log1p(1/EPS);MP=6*OA/(Q0*EPS*DEN)

def state(s):
    q=Q0*math.sqrt(1+EPS*s/(1+s))
    m=MP*(q/Q0)*s
    K=3*OA*(-1+(math.log1p(s)-s/(1+s))/DEN)
    return q,m,K

def bisect(fun,lo,hi):
    flo,fhi=fun(lo),fun(hi)
    if flo>0 or fhi<0:raise ValueError('root not bracketed')
    for _ in range(120):
        mid=(lo+hi)/2
        if mid==lo or mid==hi:break
        if fun(mid)<0:lo=mid
        else:hi=mid
    return (lo+hi)/2

def main():
    if OUTPUT.exists():raise FileExistsError(OUTPUT)
    if sha(INPUT)!=INPUT_SHA:raise ValueError('changed numerical input')
    evidence=json.loads(INPUT.read_text())['right']['Taylor']
    rho=evidence['central_rho_profile_amplitude'];mbar=evidence['cosmic_m']
    # Saved 5 kpc scale and calibrated Hunit; no recalibration.
    L=.005*67.49711988577813/299792.458
    targets=[('cosmic_m',None)]+[(str(v),v) for v in (1e-4,1e-3,.01,.03,.1,1.)]
    rows=[];checks=[]
    def check(name,error,gate):
        checks.append(dict(name=name,error=error,gate=gate,passed=error<=gate))
    for label,ratio in targets:
        target=mbar if ratio is None else ratio*rho
        fun=(lambda s:state(s)[1]-target) if ratio is None else (lambda s:state(s)[0]*state(s)[1]-target)
        hi=1.
        while fun(hi)<0:hi*=2
        s=bisect(fun,0.,hi);q,m,K=state(s);mu=m/q
        a=q*(rho+q*m+2*K)/(3*m);b=2*F*q/m;d=1+mu/C
        quadratic=q*q*(d*b-1)+2*a*b
        if quadratic<=0:raise ValueError('minimum cubic uniqueness condition failed')
        deriv=lambda sig:q**3+2*quadratic*sig+4*b*b*sig**3
        lo=-max(1.,q**3/(2*quadratic))
        while deriv(lo)>0:lo*=2
        sig=bisect(deriv,lo,0.);w=a+b*sig*sig
        g=d*w+q*sig-sig*sig;p=w+q*sig;e=g+sig*sig
        curvature=lambda v:q*q*(d*(a+b*v*v)+q*v-v*v)+(a+b*v*v)**2
        kx=curvature(sig);margin=Q0*Q0*EPS*s/(1+s)
        if kx<=0 or margin<=0:raise ValueError('unexpected nonpositive local curvature or margin')
        radius=math.sqrt(margin/kx)
        check(label+':center_Einstein',abs(3*mu*w-(rho+q*m+2*K+6*F*sig*sig))/rho,1e-10)
        check(label+':center_current',abs(C*e-((C+mu)*p-mu*q*sig))/max(abs(C*e),1e-30),1e-10)
        check(label+':minimum',abs(deriv(sig))/q**3,1e-10)
        h=max(1.,abs(sig))*1e-2
        second=(curvature(sig+h)-2*kx+curvature(sig-h))/(h*h)
        exact_second=2*quadratic+12*b*b*sig*sig
        # The quartic centered stencil has known +2*b^2*h^2 truncation.
        check(label+':curvature',abs(second-(exact_second+2*b*b*h*h))/exact_second,1e-5)
        rows.append(dict(label=label,s=s,q=q,m=m,K=K,mu=mu,
            local_qm_over_ordinary_density=q*m/rho,local_clock_rho_over_ordinary=(q*m-K)/rho,
            minimizing_sigma1=sig,w1=w,g1=g,chi0=-3*CT*sig,
            minimum_X_squared_curvature=kx,initial_X_squared_floor_margin=margin,
            Taylor_floor_radius_over_L=radius/L,Taylor_floor_radius_parsec=5000*radius/L,
            central_charge_over_cosmic=m/mbar,
            uniform_reservoir_radius_over_L=(m/mbar)**(1/3),
            reservoir_scope='uniform-volume order estimate only, not actual charge integral or formation',
            phi_curvature_over_bare=g/(rho/6),
            physical_branch_selected=False))
    result=dict(protocol=__doc__,producer_sha256=sha(Path(__file__)),input_sha256=INPUT_SHA,
        constants=dict(Q0=Q0,eps=EPS,omega_A=OA,K_B=KB,cTheta=CT),
        reference_source=dict(rho_center=rho,L=L,m_cosmic=mbar),rows=rows,checks=checks,
        all_numerical_checks_pass=all(x['passed'] for x in checks),
        galaxy_solution=False,cosmic_matching=False,native_assembly=False)
    with OUTPUT.open('x') as out:json.dump(result,out,indent=2,allow_nan=False)
    print(json.dumps(dict(all_checks_pass=result['all_numerical_checks_pass'],rows=rows,
                         failed=[x for x in checks if not x['passed']],sha256=sha(OUTPUT)),indent=2))
    if not result['all_numerical_checks_pass']:raise SystemExit(1)

if __name__=='__main__':main()
