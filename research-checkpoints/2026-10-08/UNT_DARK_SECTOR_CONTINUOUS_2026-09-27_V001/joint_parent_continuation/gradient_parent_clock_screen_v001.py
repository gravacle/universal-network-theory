"""Arithmetic for a declared slow-curvature energy bound, not cosmology fitting."""
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parent
STEM='GRADIENT_PARENT_CLOCK_SCREEN_V001'
PC=648000*149597870700/math.pi
H=70000/(1e6*PC)
LIGHT=299792458.
CHI=3.
YEAR=365.25*86400


def bound(alpha):
    if alpha<=1:
        return alpha**6/27
    # Algebraically identical finite-cutoff expression without small-b powers.
    return alpha**4/36+alpha**2/18-5/108


def main():
    cases=[]
    for ell_pc,speed in [(1,LIGHT),(10,LIGHT),(100,LIGHT),(10,1.)]:
        ell=ell_pc*PC
        omega=speed/ell
        alpha=CHI*H/omega
        cases.append(dict(ell_pc=ell_pc,assumed_fastest_mode_speed_m_s=speed,
            omega_max_s_inverse=omega,inverse_omega_years=1/(omega*YEAR),
            H_times_ell_m_s=H*ell,alpha=alpha,
            slow_potential_bound_over_Kb_gc2=bound(alpha),
            independently_calibrated=False))
    checks=[]
    def check(name,value):
        checks.append(dict(name=name,passed=bool(value)))
        assert value,name
    check('bound_continuous_at_one',math.isclose(1/36+1/18-5/108,1/27,rel_tol=1e-14))
    for i,case in enumerate(cases):
        ell=case['ell_pc']*PC
        check('speed_clock_identity_'+str(i),math.isclose(ell*case['omega_max_s_inverse'],
            case['assumed_fastest_mode_speed_m_s'],rel_tol=1e-14))
        alpha=case['alpha']
        b=min(1.,alpha**-2)
        integrated=alpha**6*(b+2*b*b-5*b**3/3)/36
        check('integral_backsubstitution_'+str(i),math.isclose(integrated,bound(alpha),rel_tol=1e-14))
    sources=[Path(__file__),ROOT/(STEM+'.md')]
    result=dict(custody={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
        inputs=dict(H_illustration_s_inverse=H,H_illustration_km_s_Mpc=70.,
                    chi=CHI,pc=PC,c_light_m_s=LIGHT),
        checks=checks,all_pass=all(c['passed'] for c in checks),cases=cases,
        scope='Defined slow-curvature subset, constant inertia; illustrative clock choices, no measured expansion fit.')
    with (ROOT/(STEM+'_RESULT.json')).open('x') as f:
        json.dump(result,f,indent=2,allow_nan=False)
        f.write('\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
