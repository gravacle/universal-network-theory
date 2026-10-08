"""Necessary free-fast-mode thermal screens for the CURRENT K(X) model.

Use ONLY the two previously tested widths eps1e-6,6e-6 at Q0/H0=100 and
their unchanged .7/.049/.251 late budgets, KB=.02, lambda_s=98, H0,a0.
Do not fit a photon temperature, occupation or ultraviolet cutoff. One
positive high-k principal boson, local equilibrium, linear dispersion and
a populated WKB band are explicit counterfactual premises, not a derived
photon sector. K(X) principal d phi_dot²-(2eta+mu)gradphi² has canonical
sqrt(P_XX)phi; cL²=(2eta M²+P_X/X)/P_XX, M²=(8pi Gcos)^-1.

The speed derivative differs from the OLD K(Q) calculation. For b=pi²/
(90cL³), b_X/b=1.5[P_XXX/P_XX-(P_XX/X-P_X/X²)/(2eta M²+P_X/X)].
At fixed X, thermal charge=b_X T4 and energy=(3b+Xb_X)T4. At fixed total
charge, deltaX_background=-b_X T4/P_XX; the leading net energy is3bT4
after cold-energy adjustment. Report BOTH, not as interchangeable ensembles.

Freeze inherited .1 perturbative screens: |thermal charge|/cold charge,
fixed-X thermal energy/cold energy, RMS deltaX/nearest positive-branch
margin and spatial J cubic/quadratic. Additionally require fixed-charge
background displacement/nearest margin<=.1. Report all individual limits
and their minimum. These are necessary perturbative diagnostics, NOT a
unitarity cutoff, hard Gaussian support, complete nonlinear thermal state,
photon identification or observational likelihood. The counterfactual
2.7255K evaluation is invalid as a perturbative state if screens fail.

Numerical gates fixed before execution: constitutive speed and adiabatic
identities<=2e-12, complex-step P3/P4 and b_X<=1e-10, Bose Simpson moment
<=1e-9, threshold substitutions<=2e-12. Reuse old physical constants and
present normalization; no dynamics job, parameter sweep or changed action.
"""
from pathlib import Path
import cmath
import hashlib
import json
import math
import invariant_clock_depth_growth_v001 as depth
import invariant_clock_transfer_v001 as core

BASE=Path(__file__).resolve().parent
OUT=BASE/'INVARIANT_CLOCK_THERMAL_WINDOW_V001_RESULT.json'
PRIOR=BASE/'INVARIANT_CLOCK_DEPTH_GROWTH_V001_RESULT.json'
CAL=BASE/'CHARGED_CLOCK_BBN_CALIBRATED_V001_RESULT.json'


def main():
    saved=json.loads(core.base.SOURCE.read_text());prior=json.loads(PRIOR.read_text())
    old=json.loads(CAL.read_text())['adopted']
    if not prior['all_controls_passed']:raise ValueError('unqualified parameter receipt')
    hbar=6.62607015e-34/(2*math.pi);c=299792458.;eV=1.602176634e-19
    GN=6.67430e-11;kb=1.380649e-23;Tph=kb*2.7255/eV
    checks=[]
    def ck(name,error,tol):
        checks.append(dict(name=name,error=float(error),tolerance=tol,passed=bool(error<=tol)))
    rows=[]
    for eps in (1e-6,6e-6):
        m,diag=depth.model(saved,eps);p=m.p
        H0=p['H0_km_s_Mpc']*1000/3.085677581491367e22;H0e=H0*hbar/eV
        Q0=100*H0e;s=diag['s_present'];u=s/(1+s);q=math.sqrt(1+eps*u);X=Q0*q
        D=1/eps-math.log1p(1/eps)
        crit=3*H0**2*c*c/(8*math.pi*GN*old['rG'])*(hbar*c)**3/eV**4
        M2=crit/(3*H0e**2);A=p['omega_A']*crit
        def constit(uu):
            qq=cmath.sqrt(1+eps*uu) if isinstance(uu,complex) else math.sqrt(1+eps*uu)
            dd=eps*(1-uu)
            f2=-2/eps+2/dd+4*qq*qq/dd**2
            f3=12*qq/dd**2+16*qq**3/dd**3
            f4=12/dd**2+96*qq*qq/dd**3+96*qq**4/dd**4
            n=2*A*qq*uu/(D*Q0*eps*(1-uu))
            P2=A*f2/(D*Q0**2);P3=A*f3/(D*Q0**3);P4=A*f4/(D*Q0**4)
            xx=Q0*qq;S=2*m.C/m.KB*M2+n/xx
            c2=S/P2;b=math.pi**2/(90*c2**1.5)
            return n,P2,P3,P4,S,c2,b
        n,P2,P3,P4,S,c2,b=constit(u);v=math.sqrt(c2)
        bX=1.5*b*(P3/P2-(P2/X-n/X**2)/S)
        rho=(p['omega_A']+p['omega_clock_excess'])*crit
        lower=Q0*eps*u/(q+1)
        upper=Q0*eps*(1-u)/(math.sqrt(1+eps)+q)
        margin=min(lower,upper)
        var=math.pi**2/(30*P2*v**3);gradvar=var/c2
        spatial_b=(1+p['lambda_s'])*p['a0']*hbar/(c*eV)
        maxwell=8*math.sqrt(2)/(3*math.sqrt(3*math.pi))
        spatial=2*m.C*p['lambda_s']*M2/(3*spatial_b*S)*maxwell*math.sqrt(gradvar)
        pref=dict(charge_fraction=abs(bX)/n,fixed_X_energy_fraction=(3*b+X*bX)/rho,
            RMS_nearest_margin=math.sqrt(var)/margin,spatial_cubic_fraction=spatial,
            fixed_charge_shift_margin=abs(bX)/(P2*margin))
        powers=dict(charge_fraction=4,fixed_X_energy_fraction=4,RMS_nearest_margin=2,
            spatial_cubic_fraction=2,fixed_charge_shift_margin=4)
        limits={k:(.1/value)**(1/powers[k]) for k,value in pref.items()}
        def evaluate(T):
            result={k:value*T**powers[k] for k,value in pref.items()}
            result.update(T_eV=T,T_K=T*eV/kb,RMS_upper_margin=math.sqrt(var)*T*T/upper,
                fixed_charge_net_energy_fraction=3*b*T**4/rho,
                deltaX_background_eV=-bX*T**4/P2,
                invariant_gradient_mean_shift_margin=gradvar*T**4/(2*X*margin),
                temporal_cubic_power=P3/(6*P2**1.5)*T*T,
                temporal_quartic_power=P4/(24*P2**2)*T**4,
                thermal_pressure_eV4=b*T**4)
            return result
        tag=str(eps)
        ck(tag+'_speed',abs(c2/diag['c_long_squared']-1),2e-12)
        ck(tag+'_adiabatic',abs(n/(X*P2)/diag['c_clock_squared']-1),2e-12)
        ck(tag+'_charge',abs(n/(A*p['d0']/Q0)-1),2e-12)
        hh=1e-24;nc,p2c,p3c,p4c,sc,c2c,bc=constit(u+1j*hh)
        du_dX=2*q/(eps*Q0)
        ck(tag+'_P3',abs(p2c.imag/hh*du_dX/P3-1),1e-10)
        ck(tag+'_P4',abs(p3c.imag/hh*du_dX/P4-1),1e-10)
        ck(tag+'_bX',abs(bc.imag/hh*du_dX/bX-1),1e-10)
        for key,T in limits.items():ck(tag+'_threshold_'+key,abs(evaluate(T)[key]/.1-1),2e-12)
        limiting=min(limits,key=limits.get);Tmax=limits[limiting]
        rows.append(dict(eps=eps,Q0_over_H0=100,background=dict(X_eV=X,Q0_eV=Q0,H0_eV=H0e,
            s=s,d0=p['d0'],A_eV4=A,P1_eV3=n,P2_eV2=P2,P3_eV=P3,P4=P4,
            M2_eV2=M2,c_long_squared=c2,lower_branch_margin_eV=lower,upper_branch_margin_eV=upper,
            rho_clock_eV4=rho),thermal=dict(b=b,b_X=bX,variance_per_T4=var,
            gradient_variance_per_T4=gradvar),diagnostic_limits_eV=limits,
            limiting_diagnostic=limiting,common_screen_T_eV=Tmax,common_screen_T_K=Tmax*eV/kb,
            evaluations=[evaluate(1e-9),evaluate(Tmax),evaluate(Tph)]))
    panels=8192;dx=80/panels
    vals=[0. if i==0 else (i*dx)**3/math.expm1(i*dx) for i in range(panels+1)]
    integral=dx/3*(vals[0]+vals[-1]+4*sum(vals[1:-1:2])+2*sum(vals[2:-1:2]))
    ck('Bose_moment',abs(integral/(math.pi**4/15)-1),1e-9)
    inputs=(PRIOR,CAL,core.base.SOURCE)
    deps=('invariant_clock_depth_growth_v001.py','invariant_clock_transfer_v001.py',
          'plane_canonical_evolution_v001.py','bounded_clock_shared_prediction_v001.py')
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        input_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in inputs},
        dependencies_sha256={name:hashlib.sha256((BASE/name).read_bytes()).hexdigest() for name in deps},
        rows=rows,controls=checks,all_controls_passed=bool(all(x['passed'] for x in checks)))
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(rows=[{k:v for k,v in r.items() if k not in ('background','thermal')} for r in rows],
        controls=checks,all_controls_passed=result['all_controls_passed']),indent=2))
    if not result['all_controls_passed']:raise SystemExit(1)


if __name__=='__main__':main()
