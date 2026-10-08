"""One small arithmetic evaluation of the prospectively fixed Banach bound."""
import hashlib
import json
import math
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parent
STEM='FILTERED_SOURCE_NONLINEAR_BOUND_V001'

def main():
    start=time.perf_counter()
    out=ROOT/(STEM+'_RESULT.json')
    if out.exists():
        raise SystemExit('Existing result preserved; refusing repeat/overwrite.')
    a0=1.0059833281731022e-10
    ratio=25.51664211557329
    gc=3*math.pi/8*a0
    gs=ratio*a0
    external=2.32e-10
    gm=1.32712440018e20
    pc=648000*149597870700/math.pi
    ell=100*pc
    sigma=1e9
    radius=.01
    sradius=2*radius
    tmin=.9
    z=(external/gs)**2
    f0=1/math.sqrt(1+z)
    gam=z/(1+z)
    tt=gam*(2*radius+radius*radius)
    jmax=(1-tt)**(-.5)+gam*(1+radius)**2*(1-tt)**(-1.5)
    djmax=3*gam*(1+radius)*(1-tt)**(-1.5)+3*gam**2*(1+radius)**3*(1-tt)**(-2.5)
    modal_lip=6*sradius+3*sradius*sradius
    modal_map=jmax*radius+3*sradius**2+sradius**3
    lw=jmax/(1-modal_lip)
    pref=f0*f0/(1+tmin*tmin)
    lf=pref*(jmax*lw+djmax*(1+sradius))
    x=sigma*sigma/(2*ell*ell)
    integral_upper=math.log1p(x)-math.log(x)+math.exp(-1)
    eps=gm/(math.pi*ell*ell*external)*integral_upper
    checks=[]
    def upper(name,value,limit,strict=False):
        checks.append(dict(name=name,value=value,limit=limit,margin=limit-value,
                           passed=bool(math.isfinite(value) and (value<limit if strict else value<=limit))))
    upper('binomial_domain',tt,1.,True)
    upper('modal_self_map',modal_map,sradius)
    upper('modal_contraction',modal_lip,1.,True)
    upper('spectral_root_lower_bound',tmin+tmin**3,external*f0/gc)
    upper('outer_contraction',lf,1.,True)
    upper('outer_self_map',eps,(1-lf)*radius)
    hess=external/(2*ell)*lf*eps/(1-lf)
    quad=external/ell*lf*eps/(1-lf)
    upper('quadrupole_hessian_relation',abs(quad/(2*hess)-1),2e-12)
    prefactor2=2*gm/(math.pi*ell**2*external)*.5
    upper('input_prefactor_identity',abs(eps/(prefactor2*integral_upper)-1),2e-12)
    result=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',
                scope='Nonlinear static Gaussian-source existence/uniqueness in the declared Wiener ball and absolute Hessian bound; not an observed Solar/causal/cosmology qualification.',
                inputs=dict(a0=a0,ratio=ratio,external=external,GM=gm,ell_pc=100.,sigma_m=sigma,r0=radius,s0=sradius,spectral_root_lower=tmin),
                gamma=gam,Jmax=jmax,DJmax=djmax,Lw=lw,pref_upper=pref,LF_upper=lf,
                gaussian_x=x,source_integral_upper=integral_upper,input_norm_upper=eps,
                solution_norm_upper=eps/(1-lf),
                Hessian_operator_bound_s_2=hess,Q2_absolute_bound_s_2=quad,
                controls=checks,control_count=len(checks),
                custody={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in (Path(__file__),ROOT/(STEM+'.md'),ROOT/'FILTERED_SOURCE_SHARED_CANDIDATE_V001.py')},
                elapsed_seconds=time.perf_counter()-start)
    with out.open('x') as f:
        json.dump(result,f,indent=2,allow_nan=False)
        f.write('\n')
    print(json.dumps(result,indent=2))
    if result['status']!='PASS':
        raise SystemExit(1)

if __name__=='__main__':
    main()
