"""Necessary dynamic/symmetry-breaking escape scales, not a stellar solution.

Fixed spherical lapse and finite proper matching length, regular phase at
center, positive timelike branch and actual prescribed outer phase rate.
If deltaq=q_outer-exp(-depth)*Xcap>0, phase difference grows at least
deltaq*T and max|w(T)-w(0)| >= deltaq*T/ell. This does not bound total
energy, force charge inflow, locate the gradient, or prove metric drift.
Illustrative lengths and elapsed times are NOT fitted matching radii/ages.
For a stationary NONspherical phase, w_center²>=q_outer² exp(2depth)-Xcap².
The associated phase-normal velocity is not ordinary matter or U velocity.

Solar redshift638+-6m/s from arxiv2009.10558 uses3D convective modeling;
adopt minimal photon coupling/attractive center for this lower lapse proxy.
No raw-observable reinterpretation, stellar interior or whole-UNT verdict.
Freeze analytic identity/independent formula gate1e-9 (cancellation-limited
direct subtraction), scale-unit roundtrip1e-12. No observational pass gate.
"""
from pathlib import Path
import hashlib
import json
import math
import invariant_clock_recombination_transfer_v002 as rec

BASE=Path(__file__).resolve().parent
OUT=BASE/'INVARIANT_CLOCK_STELLAR_WINDING_V001_RESULT.json'


def main():
    if OUT.exists():raise FileExistsError(OUT)
    cal=json.loads(rec.pilot.CAL.read_text());seed=json.loads(rec.plasma.prior.old.base.SOURCE.read_text())
    seed['inherited']['Q0_over_H0']=100.;seed['inherited']['H0_km_s_Mpc']=cal['selected_Hunit']
    m=rec.plasma.prior.old.base.Model(seed,1);_,s,X,charge,_,_,_,qr=m.bg(0.)
    c=299792458.;yr=365.25*86400.;pc=3.0856775814913673e16
    dcap=.5*math.log1p(m.eps/(1+s)/(1+m.eps*s/(1+s)))
    controls=[];rows=[]
    def check(name,value,tol):controls.append(dict(name=name,error=float(value),tolerance=tol,passed=bool(value<=tol)))
    for velocity in (620.,632.,638.,644.,656.):
        depth=math.log1p(velocity/c)
        # q_outer=Xbar: deltaq/Q0 = qr*[1-exp(dcap-depth)].
        margin=-qr*math.expm1(dcap-depth)
        direct=qr-math.exp(-depth)*math.sqrt(1+m.eps)
        check('margin_'+str(velocity),abs(margin-direct)/abs(margin),1e-9)
        # Lower positive margin for ANY zero-gradient outer X>=Q0.
        universal=-math.expm1(.5*math.log1p(m.eps)-depth)
        gradient2=qr*qr*math.expm1(2*depth)-m.eps/(1+s)
        grad=math.sqrt(max(gradient2,0.))
        beta=grad/(qr*math.exp(depth))
        check('gradient_identity_'+str(velocity),abs((grad/qr/math.exp(depth))**2+((math.sqrt(1+m.eps)/qr)*math.exp(-depth))**2-1),1e-12)
        rows.append(dict(velocity_proxy_m_s=velocity,depth=depth,stationary_spherical_headroom=dcap,
            deficit=depth-dcap,deltaq_over_Q0_current_outer=margin,deltaq_over_Q0_any_unboosted_outer=universal,
            minimum_stationary_nonspherical_gradient_over_Q0=grad,
            minimum_phase_normal_speed_over_c=beta,phase_speed_scale_m_s=beta*c))
    nominal=next(r for r in rows if r['velocity_proxy_m_s']==638.)
    scales=[]
    for label,length in (('1_AU',149597870700.),('1_pc',pc),('1_kpc',1000*pc),('100_kpc',1e5*pc),('1_Mpc',1e6*pc)):
        crossing=length/c;rate=nominal['deltaq_over_Q0_current_outer']
        for years in (1.,1e6,1e9):
            increment=rate*years*yr/crossing
            check(label+'_'+str(years)+'_units',abs(increment*crossing/(years*yr)/rate-1),1e-12)
            scales.append(dict(illustrative_matching_length=label,length_m=length,elapsed_years=years,
                minimum_max_gradient_change_over_Q0=increment,
                time_to_gradient_change_1e_minus3_years=1e-3*crossing/(rate*yr)))
    result=dict(protocol=__doc__,fixed=m.p,s_present=s,charge_present=charge,
        inherited_calibration_source='INVARIANT_CLOCK_CMB_CALIBRATION_V001_RESULT.json',
        solar_primary_source='https://arxiv.org/abs/2009.10558',
        observations_are_development_exposed=True,additional_fitted_freedoms=0,
        rows=rows,illustrative_scales=scales,controls=controls,
        all_numerical_controls_passed=all(r['passed'] for r in controls),
        hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),rec.pilot.CAL,rec.plasma.prior.old.base.SOURCE)})
    with OUT.open('x') as stream:json.dump(result,stream,indent=2,allow_nan=False)
    print(json.dumps(dict(all_numerical_controls_passed=result['all_numerical_controls_passed'],nominal=nominal,illustrative_scales=scales)),flush=True)


if __name__=='__main__':main()
