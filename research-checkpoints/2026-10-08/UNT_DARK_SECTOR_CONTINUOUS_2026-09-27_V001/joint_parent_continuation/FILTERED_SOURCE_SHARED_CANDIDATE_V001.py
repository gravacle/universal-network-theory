"""One new filtered-source linear test; no historical driver import or fit."""
import hashlib
import json
import math
from pathlib import Path
import time
import numpy as np

ROOT = Path(__file__).resolve().parent
STEM = "FILTERED_SOURCE_SHARED_CANDIDATE_V001"
A0 = 1.0059833281731022e-10
RATIO = 25.51664211557329
GC = 3*math.pi/8*A0
GS = RATIO*A0
GE = 2.32e-10
GM = 1.32712440018e20
PC = 648000*149597870700/math.pi
ELL = 100*PC
SPECS = [(64,64),(128,128),(256,256),(128,256),(256,128)]

def gauss(n):
    x,w = np.polynomial.legendre.leggauss(n)
    return (x+1)/2, w/2

def state(n, g):
    s,w=gauss(n)
    weights=2*s*w
    fac=1/math.sqrt(1+(g/GS)**2)
    h=g*fac
    t=2/math.sqrt(3)*np.sinh(np.arcsinh(3*math.sqrt(3)/2*h/(GC*s*s))/3)
    pol=GC*float(np.dot(weights,s*s*t))
    polprime=float(np.dot(weights,1/(1+3*t*t)))
    hp=fac**3
    hpp=-3*g/GS**2*fac**5
    qt=hp*pol/g
    ql=hpp*pol+hp*hp*polprime
    return dict(Qperp=qt,Qparallel=ql,epsilon_perp=1-qt,epsilon_parallel=1-ql,
                flux=g-hp*pol)

def closed_flux(g):
    ai=8/(3*math.pi)
    gi=g/A0*ai
    z=(g/GS)**2
    h=gi/math.sqrt(1+z)
    y=2/math.sqrt(3)*math.sinh(math.asinh(3*math.sqrt(3)*h/2)/3)
    th=math.atan2(1.,y)
    fel=h*h/4*(1.5*th-.5*math.sin(2*th)-math.sin(4*th)/8)
    return A0/ai*(2*fel*(1+z)**(-1.5)+gi*z*(2+z)/(1+z)**2)

def angular(n,qt,ql):
    u,w=np.polynomial.legendre.leggauss(n)
    d=qt+(ql-qt)*u*u
    kernel=d/np.sqrt(2+2*np.sqrt(1-d))
    return -.5*float(np.dot(w,(3*u*u-1)/2*kernel)), .5*float(np.dot(w,kernel))

def main():
    start=time.perf_counter()
    out=ROOT/(STEM+"_RESULT.json")
    if out.exists():
        raise SystemExit("Existing result preserved; refusing repeat/overwrite.")
    checks=[]
    def check(name,error,tolerance):
        checks.append(dict(name=name,error=float(error),tolerance=tolerance,
                           passed=bool(math.isfinite(error) and error<=tolerance)))
    t,w=gauss(256)
    q=t/(1-t)
    for d in (-.5,.2,.8,.98):
        radial=float(np.dot(w,q*q*d/((1+q*q)**2-d)/(1-t)**2))
        exact=math.pi*d/(2*math.sqrt(2+2*math.sqrt(1-d)))
        check(f"radial_{d}",abs(radial-exact)/max(1.,abs(exact)),2e-9)
    check("zero_Q",abs(angular(64,0.,0.)[0]),2e-12)
    check("isotropic_Q",abs(angular(64,.4,.4)[0]),2e-12)
    st=state(256,GE)
    check("static_force",abs(st['flux']/closed_flux(GE)-1),2e-6)
    step=GE*1e-4
    deriv=(closed_flux(GE+step)-closed_flux(GE-step))/(2*step)
    check("static_derivative",abs(st['epsilon_parallel']/deriv-1),2e-6)
    cases=[]
    for ns,nu in SPECS:
        row=state(ns,GE)
        cq,lap=angular(nu,row['Qperp'],row['Qparallel'])
        row.update(Ns=ns,Nu=nu,Cq=cq,laplacian_coefficient=lap)
        cases.append(row)
    ref=cases[2]
    for i,row in enumerate(cases):
        check(f"positive_static_{i}",0. if min(row['epsilon_perp'],row['epsilon_parallel'])>0 else 1.,0.)
        for key in ('Cq','epsilon_perp','epsilon_parallel'):
            check(f"refinement_{i}_{key}",abs(row[key]/ref[key]-1),1e-6)
    eps=min(1.,ref['epsilon_perp'],ref['epsilon_parallel'])
    dmax=max(abs(ref['Qperp']),abs(ref['Qparallel']))
    bound=GM/(2*ELL*ELL)*(1+dmax/(math.pi*eps))
    shape_path=ROOT.parent/'joint_parent_dynamics/SHAPE_REFERENCE_RESULTS.json'
    old=json.loads(shape_path.read_text())['payload']['cases'][0]
    check("inherited_shape_ratio",abs(old['r']/RATIO-1),2e-12)
    hvac=old['H_vac_reference_s_inverse']*A0/old['input']['a0_m_s2']
    output=dict(status="PASS" if all(c['passed'] for c in checks) else "FAIL",
                scope="New nonlocal effective action; linear static prediction only, not a Solar or cosmology likelihood.",
                inputs=dict(a0=A0,r=RATIO,ell_pc=100.,g_external=GE,GM_sun=GM),
                controls=checks,control_count=len(checks),cases=cases,
                Q2_linear_s_2=ref['Cq']*GM/ELL**3,
                laplacian_linear_s_2=ref['laplacian_coefficient']*GM/ELL**3,
                linear_filtered_input_bound_m_s2=bound,
                linear_input_bound_fraction_of_external=bound/GE,
                retained_matched_Hvac_km_s_Mpc=hvac*(1e6*PC)/1000.,
                retained_endpoint_is_previously_calibrated=True,
                Hvac_is_not_Htoday=True,
                custody={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in (Path(__file__),ROOT/(STEM+'.md'),shape_path)},
                elapsed_seconds=time.perf_counter()-start)
    with out.open('x') as f:
        json.dump(output,f,indent=2,allow_nan=False)
        f.write('\n')
    print(json.dumps(output,indent=2))
    if output['status']!='PASS':
        raise SystemExit(1)

if __name__=='__main__':
    main()
