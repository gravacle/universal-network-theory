"""One fixed charged epoch: conditional thermal validity, not a fitted bath.

Before execution: keep the already declared standard-thermal calibration
KB=.02, lambda_s=98, eps=1e-6, a=1, A=.7 rho_crit, clock excess=.251,
Q0/H0=1 and H0=73.6. Read its saved charge normalization. No new history.
For the derived positive fast principal oscillator, calculate the formal
one-boson gapless thermal pressure, charge/energy correction and variances.
This requires a populated WKB band, equilibrium and justified dispersion;
it is not a photon identification or a completed finite-k/cutoff calculation.

Declare diagnostic thresholds before execution: fractional thermal charge
and energy corrections <=.1; thermal RMS phase-rate fluctuation <=.1 of the
NEAREST cold-branch margin; expectation of the leading spatial J cubic term
<=.1 of the reduced quadratic gradient energy. These are perturbative
screens, not hard-support bounds or observational acceptance tolerances.
Report separately their algebraic temperatures and the common minimum.
Evaluate only T=1e-9eV and measured photon kT0 as a COUNTERFACTUAL common
temperature. Do not infer that the clock thermalizes with photons.

Numerical controls: charge and pressure derivative identities <=2e-12;
independent complex-step P''' and P'''' <=1e-10; Simpson Bose moment versus
pi^4/15 <=1e-9 at8192 panels on[0,80]; threshold substitution <=2e-12.
No changed gates after execution. Exclusive output and hashed frozen inputs.
"""
from pathlib import Path
import cmath
import hashlib
import json
import math
import resource
import time
from bounded_clock_shared_prediction_v001 import charge_root, quantities

BASE=Path(__file__).resolve().parent
OUTPUT=BASE/'FAST_MODE_THERMAL_WINDOW_V001_RESULT.json'
INPUT=BASE/'CHARGED_CLOCK_BBN_CALIBRATED_V001_RESULT.json'


def main():
    started=time.monotonic()
    old=json.loads(INPUT.read_text())
    p=old['adopted']; eps=p['eps']; d=p['d0']; KB=p['KB']; C=2-KB
    ss=charge_root(eps,d)
    q,charge,pex,rex,cs2=quantities(eps,ss)
    u=ss/(1+ss); D=1/eps-math.log1p(1/eps)
    gap=eps*(1-u)
    def derivatives(uu):
        qq=cmath.sqrt(1+eps*uu) if isinstance(uu,complex) else math.sqrt(1+eps*uu)
        dd=eps*(1-uu)
        return (-2/eps+2/dd+4*qq*qq/dd**2,
                12*qq/dd**2+16*qq**3/dd**3,
                12/dd**2+96*qq*qq/dd**3+96*qq**4/dd**4)
    f2,f3,f4=derivatives(u)
    hbar=6.62607015e-34/(2*math.pi); c=299792458.; eV=1.602176634e-19
    GN=6.67430e-11; kb=1.380649e-23
    H0=p['H0_km_s_Mpc']*1000/3.085677581491367e22
    H0e=H0*hbar/eV; Q0=H0e*p['Q0_over_H0']; Q=Q0*q
    crit=3*H0**2*c*c/(8*math.pi*GN*p['rG'])*(hbar*c)**3/eV**4
    A=p['omega_A']*crit
    P2=A*f2/(D*Q0**2); P3=A*f3/(D*Q0**3); P4=A*f4/(D*Q0**4)
    n0=A*d/Q0; rho0=A*(1+rex)
    W=p['omega_A']*q*d
    v2=2*C*(Q/H0e)**2*cs2/(3*KB*W); v=math.sqrt(v2)
    b=math.pi**2/(90*v**3); bQ=1.5*b*P3/P2
    t0=kb*2.7255/eV
    qlow=Q0*eps*u/(q+1)
    qhigh=Q0*gap/(math.sqrt(1+eps)+q)
    margin=min(qlow,qhigh)
    rate_var=math.pi**2/(30*P2*v**3)
    grad_var=rate_var/v2
    spatial_b=(1+p['lambda_s'])*p['a0']*hbar/(c*eV)
    maxwell_ratio=8*math.sqrt(2)/(3*math.sqrt(3*math.pi))
    spatial_pref=KB*p['lambda_s']/(3*spatial_b)*maxwell_ratio*math.sqrt(grad_var)
    n_pref=bQ/n0; rho_pref=(3*b+Q*bQ)/rho0
    rate_pref=math.sqrt(rate_var)/margin
    temps=dict(charge=(.1/n_pref)**.25,energy=(.1/rho_pref)**.25,
               rate_RMS=math.sqrt(.1/rate_pref),spatial_cubic=math.sqrt(.1/spatial_pref))
    def screen(T):
        return dict(T_eV=T,thermal_charge_fraction=n_pref*T**4,
                    thermal_energy_fraction=rho_pref*T**4,
                    RMS_rate_over_nearest_margin=rate_pref*T*T,
                    mean_spatial_cubic_over_quadratic=spatial_pref*T*T,
                    pressure_eV4=b*T**4,
                    dimensionless_temporal_cubic=(P3/(6*P2**1.5))*T*T,
                    dimensionless_temporal_quartic=(P4/(24*P2**2))*T**4)
    controls=[]
    def ck(name,value,tol):
        controls.append(dict(name=name,error=value,tolerance=tol,passed=value<=tol))
    ck('charge',abs(charge/d-1),2e-12)
    ck('adiabatic_derivative',abs(n0/(Q*P2)/cs2-1),2e-12)
    ck('speed_curvature',abs((2*C*crit/(3*KB*H0e**2*P2))/v2-1),2e-12)
    hh=1e-24
    fc2,fc3,_=derivatives(u+1j*hh)
    ck('complex_third',abs(fc2.imag/hh*(2*q/eps)/f3-1),1e-10)
    ck('complex_fourth',abs(fc3.imag/hh*(2*q/eps)/f4-1),1e-10)
    panels=8192; dx=80/panels
    vals=[0. if i==0 else (i*dx)**3/math.expm1(i*dx) for i in range(panels+1)]
    integ=dx/3*(vals[0]+vals[-1]+4*sum(vals[1:-1:2])+2*sum(vals[2:-1:2]))
    ck('Bose_moment',abs(integ/(math.pi**4/15)-1),1e-9)
    keys=('thermal_charge_fraction','thermal_energy_fraction','RMS_rate_over_nearest_margin','mean_spatial_cubic_over_quadratic')
    for label,key in zip(temps,keys): ck('threshold_'+label,abs(screen(temps[label])[key]/.1-1),2e-12)
    limiting=min(temps,key=temps.get)
    result=dict(scope=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                input_sha256={INPUT.name:hashlib.sha256(INPUT.read_bytes()).hexdigest()},
                dependency_sha256=hashlib.sha256((BASE/'bounded_clock_shared_prediction_v001.py').read_bytes()).hexdigest(),
                inherited=p,epoch_a=1.,background=dict(s=ss,q=q,Q_eV=Q,Q0_eV=Q0,H0_eV=H0e,A_eV4=A,
                  rho_clock_eV4=rho0,n_eV3=n0,P2_eV2=P2,P3_eV=P3,P4=P4,cs_ad_squared=cs2,
                  fast_speed_over_c=v,lower_rate_margin_eV=qlow,upper_rate_margin_eV=qhigh),
                thermal_coefficients=dict(b=b,bQ_eV_inverse=bQ,rate_variance_per_T4=rate_var,
                  gradient_variance_per_T4=grad_var,spatial_b_eV=spatial_b,Maxwell_moment_ratio=maxwell_ratio),
                diagnostic_temperatures_eV=temps,limiting_diagnostic=limiting,
                common_screen_temperature_eV=temps[limiting],
                evaluations=[screen(1e-9),screen(t0),screen(temps[limiting])],
                controls=controls,all_controls_passed=all(x['passed'] for x in controls),
                elapsed_seconds=time.monotonic()-started,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with OUTPUT.open('x') as f:
        json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(result,indent=2))
    if not result['all_controls_passed']:raise SystemExit(1)


if __name__=='__main__':main()
