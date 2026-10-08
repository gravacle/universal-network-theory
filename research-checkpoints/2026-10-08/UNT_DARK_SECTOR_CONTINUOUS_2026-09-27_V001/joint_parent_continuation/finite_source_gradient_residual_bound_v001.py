"""Prospective finite-source bulk/finite-surface bounds; no work on import."""
import os
for _key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS'):
    os.environ[_key] = '1'
import hashlib
import json
import math
from pathlib import Path
import resource
import sys
import time
import numpy as np

ROOT = Path(__file__).resolve().parent
STEM = 'FINITE_SOURCE_GRADIENT_RESIDUAL_BOUND_V001'
PRIOR = 'LINEAR_GRADIENT_EXTERNAL_QUADRUPOLE_V001_RESULT.json'
PRIOR_SHA = '91557a068666b0079a0ed7ba920a21a6d97cc5dd0ada1b6cf4ba5380b9758163'
A0 = 1.0059833281731022e-10
GC = 3*math.pi*A0/8
GE = 2.32e-10
GM = 1.32712440018e20
AU = 149597870700.
PC = 648000*AU/math.pi
SIGMA = 1e9
ETA = 1e-36
CELLS = (16384, 32768, 65536)
LENGTHS_PC = (1., 10., 100.)
RADII_AU = (1., 10., 30.)
ARITH = 1e-10


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def equilibrium(s):
    h = GE/(GC*np.asarray(s)**2)
    t = 2/math.sqrt(3)*np.sinh(np.arcsinh(3*math.sqrt(3)*h/2)/3)
    return t, h


def quantities(s, ell, mu_floor):
    t, h = equilibrium(s)
    tt = t*t
    a = 1+tt
    g2 = 2*math.pi**.25*GM/(mu_floor*math.sqrt(SIGMA))
    vinf = GM/(math.pi*mu_floor*ell**2)*np.log1p(2*ell**2/(a*SIGMA**2))
    ratio = a*vinf/GE
    v2 = np.minimum(g2/a, math.sqrt(2*math.pi)*GM/
                    (mu_floor*math.sqrt(ell)*a**.75))
    return tt, ratio, v2, float(np.max(abs(t+t**3-h)/h))


def enclosure(n, ell, mu_floor):
    log_s = np.linspace(math.log(ETA), 0., n+1)
    s = np.exp(log_s)
    tt, ratio, v2, cubic_error = quantities(s, ell, mu_floor)
    # Each endpoint combination encloses the ENTIRE cell by monotonicity.
    amin = 1+.75*tt[1:]*np.maximum(1-ratio[:-1], 0.)**2
    amax = 1+.75*tt[:-1]*np.maximum(1-ratio[1:], 0.)**2
    bmax = tt[:-1]*(3*ratio[:-1]+ratio[:-1]**2)*v2[1:]
    bmin = tt[1:]*(3*ratio[1:]+ratio[1:]**2)*v2[:-1]
    i4max = tt[:-1]*(3+ratio[:-1])**(4/3)*ratio[:-1]**(2/3)*v2[1:]**2
    i4min = tt[1:]*(3+ratio[1:])**(4/3)*ratio[1:]**(2/3)*v2[:-1]**2
    weights = s[:-1]**2*np.expm1(2*np.diff(log_s))
    g2 = 2*math.pi**.25*GM/(mu_floor*math.sqrt(SIGMA))
    gstar = 2*GM/(math.pi*mu_floor*SIGMA**2)
    bsoft = g2*(3*gstar/GE+(gstar/GE)**2)
    ustar = gstar/GE
    i4tail = .6*g2*g2*(3+ustar)**(4/3)*ustar**(2/3)*(GC/GE)**(2/3)*ETA**(10/3)
    gamma_lo = float(np.dot(weights, 1/amax))
    gamma_hi = float(np.dot(weights, 1/amin))+ETA**2
    s_lo = float(np.dot(weights, bmin*bmin/amax))
    s_hi = float(np.dot(weights, bmax*bmax/amin))+bsoft*bsoft*ETA**2
    return dict(cells=n, gamma_lower=gamma_lo, gamma_upper=gamma_hi,
                residual_S_lower=s_lo, residual_S_upper=s_hi,
                quartic_I4_lower=float(np.dot(weights,i4min)),
                quartic_I4_upper=float(np.dot(weights,i4max))+i4tail,
                quartic_tail_upper=i4tail,
                gamma_tail_upper=ETA**2,
                residual_tail_upper=bsoft*bsoft*ETA**2,
                cubic_relative_error=cubic_error,
                weight_error=abs(float(weights.sum())-(1-ETA**2)),
                endpoint_ordered=bool(np.all(amin<=amax) and np.all(bmin<=bmax)
                                      and np.all(i4min<=i4max)),
                monotone_t=bool(np.all(np.diff(tt)<=0)),
                monotone_ratio_error=float(max(0., np.max(np.diff(ratio))))/
                                     max(1., float(np.max(ratio))),
                monotone_v2=bool(np.all(np.diff(v2)>=0)))


def finite_linear_correction(ell, radius, t0, mu_floor):
    d = SIGMA**2/(2*ell**2)+radius**2/(14*ell**2)
    qc = math.sqrt(2/d)
    if not qc>1:
        raise ValueError('The declared piecewise envelope requires qc>1')
    m2 = (GE/GC)*(2*math.atan(1/t0)+t0/(1+t0*t0))
    clo = 4/(15*math.pi*mu_floor**2)
    chi = 8*m2/(15*math.pi)
    coef = d*clo/5+d*chi*((qc-1)+2*(1-1/qc)+(1-qc**-3)/3)
    coef += 2*chi*(1/qc+2/(3*qc**3)+1/(5*qc**5))
    return dict(D=d, qc=qc, M2_exact=m2, coefficient_bound=coef,
                Q_R_linear_minus_exact_point_bound_s_2=GM*coef/ell**3)


def rss_bytes():
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value if sys.platform=='darwin' else 1024*value)


def main():
    destination = ROOT/(STEM+'_RESULT.json')
    if destination.exists():
        raise FileExistsError(destination)
    start = time.perf_counter()
    out = dict(status='started', controls=[], cases=[], inputs=dict(
        a0=A0, gc=GC, ge=GE, GM=GM, AU=AU, pc=PC, gaussian_sigma_m=SIGMA,
        eta=ETA, cells=CELLS, lengths_pc=LENGTHS_PC, radii_AU=RADII_AU,
        arithmetic_allowance=ARITH, refinement_gate=.01,
        source='Declared Gaussian control, not measured Solar structure'))
    def check(name, error, limit=ARITH):
        out['controls'].append(dict(name=name, error=float(error), limit=limit,
                                    passed=bool(math.isfinite(error) and error<=limit)))
    try:
        paths = (Path(__file__), ROOT/(STEM+'.md'), ROOT/PRIOR)
        out['custody'] = {p.name:sha(p) for p in paths}
        if out['custody'][PRIOR]!=PRIOR_SHA:
            raise ValueError('Saved point-result hash changed')
        prior = json.loads((ROOT/PRIOR).read_text())
        if not prior['qualified_linearized_coefficient']:
            raise ValueError('Inherited point coefficient is unqualified')
        if prior['inputs']['a0']!=A0 or prior['inputs']['primary_ge']!=GE:
            raise ValueError('Inherited physical inputs differ')
        point_cq = next(c['Cq'] for c in prior['primary_cases']
                        if c['Ns']==256 and c['Nx']==256)
        t0 = float(equilibrium(np.array([1.]))[0][0])
        mu_floor = t0*t0/(1+t0*t0)
        out['mu_floor_not_actual_KT0'] = mu_floor
        out['saved_point_coefficient_nominal'] = point_cq
        check('source_equilibrium', abs(t0+t0**3-GE/GC)/(GE/GC), 1e-12)
        # Exact algebra probes, not a fit or sampled physical state.
        for i, (z,e) in enumerate(((np.array([1.,0.,0.]),np.array([-1.5,0.,0.])),
                                   (np.array([1.,2.,-1.]),np.array([-.2,.3,.7])))):
            lhs = np.dot(np.dot(z+e,z+e)*(z+e)-np.dot(z,z)*z, e)
            rhs = .75*np.dot(z,z)*np.dot(e,e)
            rem = (1.5*np.dot(z,e)+np.dot(e,e))**2
            rem += .25*(np.dot(z,z)*np.dot(e,e)-np.dot(z,e)**2)
            check('secant_identity_'+str(i), abs(lhs-rhs-rem)/max(1.,abs(lhs)))
            center=z+e/2
            quartic=.25*np.dot(e,e)**2+np.dot(center,center)*np.dot(e,e)
            quartic+=2*np.dot(center,e)**2
            check('quartic_identity_'+str(i),abs(lhs-quartic)/max(1.,abs(lhs)))
        check('adjoint_normalization', abs((9/(16*math.pi**2))*(4*math.pi/5)*
                                          (1/7+1/3)-3/(14*math.pi)))
        u,wu = np.polynomial.legendre.leggauss(32)
        check('window_normalization', abs(15/16*np.dot(wu,(1-u*u)**2)-1))
        check('window_variance', abs(15/16*np.dot(wu,u*u*(1-u*u)**2)-1/7))
        x,wx=np.polynomial.legendre.leggauss(256)
        x,wx=(x+1)/2,wx/2
        k=x/(1-x)
        check('gaussian_L2_radial_integral',abs(float(np.dot(wx,np.exp(-k*k)/(1-x)**2))-
                                                math.sqrt(math.pi)/2))
        for ell_pc in LENGTHS_PC:
            ell = ell_pc*PC
            case = dict(ell_pc=ell_pc, enclosures=[], observables=[])
            out['cases'].append(case)
            for n in CELLS:
                row = enclosure(n, ell, mu_floor)
                case['enclosures'].append(row)
                key = str(ell_pc)+'_'+str(n)
                check('cubic_'+key,row['cubic_relative_error'],1e-12)
                check('weight_'+key,row['weight_error'],2e-12)
                check('ordered_'+key,0 if row['endpoint_ordered'] else 1)
                check('t_monotone_'+key,0 if row['monotone_t'] else 1)
                check('u_monotone_'+key,row['monotone_ratio_error'])
                check('V_monotone_'+key,0 if row['monotone_v2'] else 1)
                if time.perf_counter()-start>120 or rss_bytes()>256*1024**2:
                    raise RuntimeError('Declared resource ceiling reached')
            for lo,hi in zip(case['enclosures'][:-1],case['enclosures'][1:]):
                for base in ('gamma','residual_S','quartic_I4'):
                    scale=max(abs(lo[base+'_upper']),1e-300)
                    violation=max(0.,lo[base+'_lower']-hi[base+'_lower'],
                                  hi[base+'_upper']-lo[base+'_upper'])/scale
                    check('nested_'+str(ell_pc)+'_'+base+'_'+str(hi['cells']),violation)
            mid,fine=case['enclosures'][-2:]
            for base in ('gamma','residual_S','quartic_I4'):
                rel=abs(mid[base+'_upper']-fine[base+'_upper'])/fine[base+'_upper']
                check('refinement_'+str(ell_pc)+'_'+base,rel,.01)
            gap=1-fine['gamma_upper']
            case['coercivity_gap_lower']=gap
            case['coercivity_certificate_available']=bool(gap>0)
            case['bulk_error_bound_g_m_3_2']=math.sqrt(fine['residual_S_upper']/gap) if gap>0 else None
            for radius_au in RADII_AU:
                radius=radius_au*AU
                nonlinear=(math.sqrt(3/(14*math.pi))*case['bulk_error_bound_g_m_3_2']/
                           (ell*radius**1.5)) if gap>0 else None
                quartic=3*math.sqrt(fine['quartic_I4_upper'])/(math.sqrt(56*math.pi)*ell*radius**1.5)
                best=min(nonlinear,quartic) if nonlinear is not None else quartic
                correction=finite_linear_correction(ell,radius,t0,mu_floor)
                nominal=GM*point_cq/ell**3
                width=best+correction['Q_R_linear_minus_exact_point_bound_s_2']
                case['observables'].append(dict(radius_AU=radius_au,
                    coercivity_Q_R_difference_bound_s_2=nonlinear,
                    quartic_Q_R_difference_bound_s_2=quartic,
                    best_analytic_Q_R_difference_bound_s_2=best,
                    finite_linear_correction=correction,
                    inherited_point_Q_nominal_s_2=nominal,
                    nominal_combined_interval_s_2=[nominal-width,nominal+width],
                    interval_caveat='Does not include inherited point-quadrature error; not a Cassini likelihood'))
        out['all_numerical_controls_pass']=all(c['passed'] for c in out['controls'])
        out['status']='qualified_bound_evaluation' if out['all_numerical_controls_pass'] else 'numerically_unqualified'
        out['scope']='Analytic finite-source/finite-surface bounds numerically evaluated; not directed-rounding verification, nonlinear field solution, or physical success test.'
    except Exception as exc:
        out['status']='failed'
        out['failure']=repr(exc)
        out['all_numerical_controls_pass']=False
    out['elapsed_seconds']=time.perf_counter()-start
    out['rss_bytes']=rss_bytes()
    with destination.open('x') as stream:
        json.dump(out,stream,indent=2,allow_nan=False)
        stream.write('\n')
    print(json.dumps(dict(status=out['status'], controls=len(out['controls']),
                         elapsed_seconds=out['elapsed_seconds'],result=str(destination))))
    return 0 if out['all_numerical_controls_pass'] else 2


if __name__=='__main__':
    if sys.argv[1:]!=['--run']:
        raise SystemExit('Explicit --run required; imports do not execute the diagnostic.')
    raise SystemExit(main())
