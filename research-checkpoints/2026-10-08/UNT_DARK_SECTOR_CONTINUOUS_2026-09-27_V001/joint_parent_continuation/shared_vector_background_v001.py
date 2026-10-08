"""First absolute shared-scale prediction of the provisional charge-free axes.

U=-A*y/(1+y)^2, kappa=1+1/(1+y), y=(cH/a0)^2, no independentLambda.
Primary A=48 FIXED by the already written existence example. Inherit
physical a0, GN baryon density, photon temperature/Neff from exposed joint
calibration. This reuse is NOT independent observation or native formation.
Solve high-y branch R(y)=6y-A*y*(3y-1)/(1+y)^3=6 Hordinary²/(a0/c)^2.
Predict absolute H(a), cosmic mu floor and principal Sigma, not just shape.
Separate counterfactual A calibrated to the old Htoday reference is counted
as ONE new expansion fit. It is not adopted and does not erase fixed48.
No radiation production, full perturbations, galaxy or likelihood claim.
All roots checked1e-12, derivative identity1e-6, no observational pass gate.
"""
from pathlib import Path
import hashlib,json,math
import invariant_clock_acoustic_v001 as old

ROOT=Path(__file__).resolve().parent
CAL=ROOT/'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json'
OUT=ROOT/'SHARED_VECTOR_BACKGROUND_V001_RESULT.json'
EXPECTED='c92eb0ce131a61009361f2ead3f4db7522d3eabb22f7e3d472f0e4e0c116c24f'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def source(y,A):return A*y*(3*y-1)/(1+y)**3
def sigma(y,A):return A*(-3*y*y+8*y-1)/(1+y)**4
def R(y,A):return 6*y-source(y,A)
def vacuum(A):
    lo=3.;hi=max(6.,math.sqrt(A))
    if A==48:return 3.
    if R(lo,A)>0:raise ValueError('declared high branch bracket')
    while R(hi,A)<0:hi*=2
    for _ in range(100):
        mid=(lo+hi)/2
        if R(mid,A)<0:lo=mid
        else:hi=mid
    return (lo+hi)/2
def root(A,rho):
    lo=vacuum(A);hi=max(2*lo,rho/6+lo)
    while R(hi,A)<rho:hi*=2
    for _ in range(100):
        mid=(lo+hi)/2
        if R(mid,A)<rho:lo=mid
        else:hi=mid
    return (lo+hi)/2

def main():
    if OUT.exists():raise FileExistsError(OUT)
    if sha(CAL)!=EXPECTED:raise ValueError('changed exposed comparison input')
    cal=json.loads(CAL.read_text());p=cal['fixed'];sel=cal['selected']
    c=old.S['c'];mpc=old.S['Mpc'];a0=p['a0'];ha=a0/c*mpc/1000
    ug=8*math.pi**5*old.KBOLTZ**4*old.T0**4/(15*old.HPLANCK**3*c**3)
    H100=100000/mpc
    og=8*math.pi*old.S['GN']*ug/(3*c*c*H100**2)
    orad=og*(1+(7/8)*(4/11)**(4/3)*sel['Neff']);ob=sel['physical_omega_b']
    href=cal['rows'][0]['H_today'];yref=(href/ha)**2;rho0=6*10000*(ob+orad)/ha**2
    Afit=(6*yref-rho0)*(1+yref)**3/(yref*(3*yref-1))
    checks=[];rows=[]
    def check(name,error,gate):checks.append(dict(name=name,error=error,gate=gate,passed=error<=gate))
    for label,A,freedoms in (('fixed_existence_example',48.,0),('counterfactual_Htoday_calibration',Afit,1)):
        yv=vacuum(A);hist=[]
        check(label+'_vacuum',abs(R(yv,A))/(6*yv),1e-12)
        for a in (1e-8,1e-4,1/1101,.01,.1,.25,.5,1.,2.):
            ordinary2=10000*(ob/a**3+orad/a**4);rho=6*ordinary2/ha**2;y=root(A,rho)
            H=ha*math.sqrt(y)
            # Exposed pressureless comparator at the ORIGINAL calibrated Gcos.
            reference2=p['H0_km_s_Mpc']**2*(p['omega_A']+(p['omega_b_cos']+p['omega_clock_excess'])/a**3)+p['rG']*10000*orad/a**4
            check(label+'_root_'+str(a),abs(R(y,A)-rho)/max(rho,6*y),1e-12)
            h=y*1e-4;fd=(R(y-2*h,A)-8*R(y-h,A)+8*R(y+h,A)-R(y+2*h,A))/(12*h)
            check(label+'_derivative_'+str(a),abs(fd-(6-sigma(y,A)))/(6+abs(sigma(y,A))),1e-6)
            hist.append(dict(a=a,y=y,H_km_s_Mpc=H,exposed_reference_H=math.sqrt(reference2),H_ratio_to_reference=H/math.sqrt(reference2),
                Sigma=sigma(y,A),cosmic_held_background_mu_floor=y/(2*(1+y)),
                ordinary_density_response=6-sigma(y,A)))
        rows.append(dict(label=label,A=A,additional_fitted_parameters=freedoms,y_vacuum=yv,H_vacuum_km_s_Mpc=ha*math.sqrt(yv),
            shared_scale_a0=a0,history=hist))
    check('counterfactual_fit_closure',abs(rows[1]['history'][-2]['H_km_s_Mpc']/href-1),1e-12)
    result=dict(protocol=__doc__,producer_sha256=sha(Path(__file__)),calibration_sha256=EXPECTED,
        dependencies={str(Path(old.__file__)):sha(Path(old.__file__))},a0=a0,ordinary_omega_b=ob,ordinary_omega_r=orad,
        exposed_Htoday_reference=href,rows=rows,checks=checks,all_controls_passed=all(c['passed'] for c in checks),
        native_formation=False,galaxy_branch_selected=False,observational_superiority=False)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(dict(rows=rows,all_pass=result['all_controls_passed'],failed=[c for c in checks if not c['passed']],sha256=sha(OUT)),indent=2))

if __name__=='__main__':main()
