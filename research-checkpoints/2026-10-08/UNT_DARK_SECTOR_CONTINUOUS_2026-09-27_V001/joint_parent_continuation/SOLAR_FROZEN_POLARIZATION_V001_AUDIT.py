"""Independent saved-field audit: no producer import, solve, fit or iteration."""
import os
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[key] = '1'
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import math
from pathlib import Path
import tempfile
import time
import numpy as np
from numpy.polynomial.legendre import leggauss

J = Path(__file__).resolve().parent
STEM = 'SOLAR_FROZEN_POLARIZATION_V001'
OLD = 'SOLAR_AQUAL_QUADRUPOLE_V001'
A0, GM, RS = 1.0059833281731022e-10, 1.32712440018e20, 25.51664211557329
RM, AI = math.sqrt(GM/A0), 8/(3*math.pi)
checks = []


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(name):
    return json.loads((J/name).read_text())


def check(name, value, gate):
    value = float(value)
    checks.append(dict(name=name, error=value, gate=gate,
                       passed=math.isfinite(value) and value <= gate))


def identity(name, yes):
    check(name, 0 if yes else 1, 0)


def relative(a, b, floor=1.):
    a, b = np.asarray(a), np.asarray(b)
    return float(np.max(abs(a-b))/max(floor, float(np.max(abs(b)))))


def derivative(y, h):
    out = np.empty_like(y)
    out[1:-1] = (y[2:]-y[:-2])/(2*h)
    out[0] = (-3*y[0]+4*y[1]-y[2])/(2*h)
    out[-1] = (3*y[-1]-4*y[-2]+y[-3])/(2*h)
    return out


def legendre(u, order):
    P, D = np.zeros((len(u), order+1)), np.zeros((len(u), order+1))
    P[:, 0] = 1
    P[:, 1], D[:, 1] = u, 1
    for l in range(1, order):
        P[:, l+1] = ((2*l+1)*u*P[:, l]-l*P[:, l-1])/(l+1)
        D[:, l+1] = ((2*l+1)*(P[:, l]+u*D[:, l])-l*D[:, l-1])/(l+1)
    return P, D


def mechanical_b(e, order):
    # Positive equilibrium integral, independent of the producer's closed deficit.
    u, weight = leggauss(order)
    delta, weight = (u+1)/2, weight/2
    h = AI*e/math.sqrt(1+(e/RS)**2)
    z = 2*delta/math.sqrt(3)*np.sinh(np.arcsinh(3*math.sqrt(3)*h/(2*delta**2))/3)
    return float(2*np.dot(weight, delta**2*z)/AI)


def closed_b(e):
    h = AI*e/math.sqrt(1+(e/RS)**2)
    y = 2/math.sqrt(3)*math.sinh(math.asinh(3*math.sqrt(3)*h/2)/3)
    theta = math.atan2(1., y)
    fel = h*h/4*(1.5*theta-.5*math.sin(2*theta)-math.sin(4*theta)/8)
    return (h-2*fel)/AI


def energy(g, b):
    return np.dot(g, g)/2-np.dot(g, b)/np.sqrt(1+np.dot(g, g)/RS**2)


def flux(g, b):
    F = (1+np.dot(g, g)/RS**2)**(-.5)
    return g-F*b+F**3*g*np.dot(b, g)/RS**2


def trap(y, t):
    return float(np.sum((y[1:]+y[:-1])*.5*np.diff(t)))


def main():
    start = time.perf_counter()
    frozen, tests, result = (read(STEM+x+'.json') for x in ('_FROZEN', '_TESTS', '_RESULT'))
    for name, pin in frozen['inputs'].items():
        path = J.parent/'joint_parent_dynamics'/name if name == 'SHAPE_REFERENCE_RESULTS.json' else J/name
        identity('pin/'+name, sha(path) == pin)
    identity('tests_custody', frozen['inputs'] == tests['inputs'] and tests['all_pass'])
    identity('result_custody', frozen['inputs'] == result['inputs'])
    for name, receipt in [('new', tests), ('inherited', read(OLD+'_TESTS.json'))]:
        for k, c in enumerate(receipt['checks']):
            identity('saved_control/'+name+'/'+str(k), c['pass'] and c['error'] <= c['limit'] and math.isfinite(c['error']))
    identity('inherited_control_custody', read(OLD+'_TESTS.json')['inputs'] == read(OLD+'_FROZEN.json')['inputs'])
    cases, diagnostics, pins = [], [], {}
    for index in range(7):
        name = STEM+'_CASE_'+str(index)+'.json'
        case = read(name)
        pins[name] = sha(J/name)
        spec = frozen['specs'][min(index, 4)]
        ext = 2.32e-10 if index < 5 else [2.16e-10, 2.48e-10][index-5]
        identity(name+'/identity', case['inputs'] == frozen['inputs'] and case['index'] == index and
                 case['spec'] == spec and case['external_acceleration'] == ext and case['a0'] == A0 and
                 case['GM'] == GM and case['shape_ratio'] == RS and case['imposed_frozen_polarization'])
        if index < 5:
            identity(name+'/summary_pin', result['receipt_hashes'][name] == pins[name])
        n, order, nq, ri, ro = spec
        t = np.linspace(math.log(ri), math.log(ro), n)
        r, ell, h = np.asarray(case['radii']), np.arange(order+1), t[1]-t[0]
        psi, br_saved, th_saved = (np.asarray(case[k]) for k in ('psi_modes', 'Br_modes', 'Theta_modes'))
        identity(name+'/array_shapes', psi.shape == br_saved.shape == th_saved.shape == (n, order+1))
        identity(name+'/finite_arrays', all(np.all(np.isfinite(v)) for v in (psi, br_saved, th_saved)))
        check(name+'/radial_grid', relative(r, np.exp(t)), 1e-14)
        check(name+'/unit_rM', abs(case['rM']/RM-1), 1e-14)
        e = ext/A0
        b = closed_b(e)
        check(name+'/b_magnitude', abs(b-case['b_magnitude']), 1e-12)
        check(name+'/mechanical_b_256_512', abs(mechanical_b(e, 256)-mechanical_b(e, 512)), 1e-10)
        check(name+'/mechanical_b_closed', abs(b-mechanical_b(e, 512)), 1e-10)
        bv = np.array([0., 0., -b])
        for k, g in enumerate([np.zeros(3), np.array([.3, -.7, 2.]), np.array([30., 1., -60.])]):
            cs = np.array([np.imag(energy(g.astype(complex)+1e-24j*np.eye(3)[a], bv))/1e-24 for a in range(3)])
            check(name+'/contact_energy_gradient/'+str(k), relative(cs, flux(g, bv)), 1e-12)
        fe = (1+(e/RS)**2)**(-.5)
        perp, parallel = 1+b*e*fe**3/RS**2, 1+3*b*e*fe**5/RS**2
        lower_bound = 1-4*b/(math.sqrt(3)*RS)
        for key, value in [('external_C_perp', perp), ('external_C_parallel', parallel), ('global_ellipticity_lower_bound', lower_bound)]:
            check(name+'/'+key, abs(value-case[key]), 1e-12)
        identity(name+'/strict_ellipticity', lower_bound > 0)
        u, weights = leggauss(nq)
        P, Pd = legendre(u, order)
        ss, rr = np.sqrt(1-u*u), r[:, None]
        proj = weights[:, None]*P*(2*ell+1)[None, :]/2
        aproj = (weights*ss)[:, None]*Pd*(2*ell+1)[None, :]/2
        gr = 1/rr**2-e*u+(derivative(psi, h)@P.T)/rr
        gt = e*ss-ss*(psi@Pd.T)/rr
        # Cylindrical Cartesian calculation: b_z=-b, b_cyl=0; then rotate back.
        gz, gc = gr*u-gt*ss, gr*ss+gt*u
        F = (1+(gz*gz+gc*gc)/RS**2)**(-.5)
        Bz_raw, Bc = -b*F+b*F**3*gz*gz/RS**2, b*F**3*gc*gz/RS**2
        Bz = Bz_raw+b*fe**3  # Subtract the uniform external polarization.
        br = (Bz*u+Bc*ss)@proj
        th = (-Bz*ss+Bc*u)@aproj
        check(name+'/Br_cartesian', relative(br, br_saved), 1e-10)
        check(name+'/Theta_cartesian', relative(th, th_saved), 1e-10)
        outer = ((1-1/(math.sqrt(perp*parallel)*np.sqrt(1-u*u+perp/parallel*u*u)))/r[-1])@proj
        src = r[:, None]*(derivative(br, h)+2*br+th)
        aa, cc = math.exp(-h/2)/h**2, math.exp(h/2)/h**2
        bb = -2*np.cosh((ell+.5)*h)/h**2
        residual = aa*psi[:-2]+bb*psi[1:-1]+cc*psi[2:]-src[1:-1]
        inner_error = psi[0]-np.exp(-ell*h)*psi[1]
        outer_error = psi[-1]-outer
        check(name+'/inner_Robin', float(np.max(abs(inner_error))), 1e-12)
        check(name+'/outer_Dirichlet', float(np.max(abs(outer_error))), 1e-8)
        mask = (r >= .003)&(r <= .02)
        plateaux = psi[mask, 2]/r[mask]**2
        c2 = float(np.median(plateaux))
        plateau = float(np.max(abs(plateaux-c2))/max(abs(c2), 1e-5))
        check(name+'/c2', abs(c2-case['c2']), 1e-12)
        check(name+'/plateau', abs(plateau-case['plateau_relative']), 1e-12)
        check(name+'/Q2_sign_units', abs((-3*A0/RM*c2)/case['Q2']-1), 1e-12)
        identity(name+'/convergence_definition', case['converged'] == (case['status'] == 'converged' and case['fixed_point_defect'] < 3e-8))
        j = np.arange(1, n-1)
        green_weights = -np.expm1(-5*h*(n-1-j))/(2*math.sinh(2.5*h)/h**2*r[j]**2)
        green = outer[2]/r[-1]**2-float(green_weights@src[1:-1, 2])
        inner_c2 = float(psi[0, 2]/r[0]**2)
        correction = math.exp(2*h)*inner_error[2]/(r[0]**2*(math.exp(2*h)-math.exp(-3*h)))*(-math.expm1(-5*h*(n-1)))
        weighted_residual = float(green_weights@residual[:, 2])
        green_error = inner_c2-(green-weighted_residual+correction+outer_error[2]/r[-1]**2)
        check(name+'/discrete_Green_identity', abs(green_error), 1e-9)
        integ = trap((3/r+2*r**4/r[-1]**5)*br[:, 2]+(1/r-r**4/r[-1]**5)*th[:, 2], t)
        integ -= (1/r[0]-r[0]**4/r[-1]**5)*br[0, 2]
        continuum = outer[2]/r[-1]**2-integ/5
        mass_flux = r*r/2*((gr-Bz_raw*u-Bc*ss)@weights)
        # Inner contact asymptote, NOT a fit or a replacement extraction rule.
        c1 = float(psi[0, 1]/r[0])
        k3 = RS*b*(e-c1)/3
        radial_factor = ((math.sinh(4*h)/h+2)*2/3+4)/(2*(math.cosh(5.5*h)-math.cosh(2.5*h))/h**2)
        k3_discrete = RS*b*(e-c1)*radial_factor
        contact_change = plateaux-inner_c2
        predicted_change = k3_discrete*r[mask]**3
        diagnostics.append(dict(index=index, Q2_s_minus2=case['Q2'], c2=c2,
            plateau_relative=plateau, inner_c2=inner_c2, inner_Q2_s_minus2=-3*A0/RM*inner_c2,
            inner_vs_median_relative=(inner_c2-c2)/abs(c2), extraction_r_min=float(r[mask][0]),
            extraction_r_max=float(r[mask][-1]), extraction_c2_first=float(plateaux[0]),
            extraction_c2_last=float(plateaux[-1]), inner_regular_dipole=c1,
            leading_contact_c3_continuum=k3, leading_contact_c3_discrete=k3_discrete,
            contact_shape_relative_discrepancy=relative(contact_change, predicted_change, 1e-15),
            discrete_Green_c2=green, discrete_Green_vs_inner_relative=(green-inner_c2)/abs(inner_c2),
            discrete_Green_identity_error=green_error, weighted_modal_residual_c2=weighted_residual,
            continuum_Green_c2=continuum, continuum_Green_vs_inner_relative=(continuum-inner_c2)/abs(inner_c2),
            modal_residual_scaled=float(np.max(abs(residual))/max(1., np.max(abs(src[1:-1])))),
            mass_flux_max_abs_error=float(np.max(abs(mass_flux-1))),
            mass_flux_transition_max_abs_error=float(np.max(abs(mass_flux[(r>.05)&(r<10)]-1))),
            b_magnitude=b, external_C_perp=perp, external_C_parallel=parallel, ellipticity_lower_bound=lower_bound))
        cases.append(case)
    scale = max(abs(cases[4]['c2']), 1e-5)
    diffs = {f'{a}_{b}': abs(cases[a]['c2']-cases[b]['c2'])/scale for a, b in ((1, 2), (2, 3), (3, 4))}
    qualified = all(c['converged'] and c['plateau_relative'] < .01 for c in cases[:5]) and all(v < .05 for v in diffs.values())
    identity('primary_qualification', qualified and qualified == result['qualified_primary'])
    for k, v in diffs.items():
        check('refinement/'+k, abs(v-result['relative_changes'][k]), 1e-14)
    standardized = (cases[4]['Q2']-1.6e-27)/1.8e-27
    check('fixed_mean_residual', abs(standardized-result['cassini_standardized_residual']), 1e-12)
    old_result = read(OLD+'_RESULT.json')
    output = dict(status='SAVED_FROZEN_AUDIT_PASSED' if all(c['passed'] for c in checks) else 'SAVED_FROZEN_AUDIT_FAILED',
        scope='Saved fields only: no producer import, solver, nonlinear iteration or refit. Flux/residual/inner-contact diagnostics are descriptive, not new qualification gates.',
        pins=dict(audit_source=sha(Path(__file__)), frozen=sha(J/(STEM+'_FROZEN.json')), tests=sha(J/(STEM+'_TESTS.json')),
                  result=sha(J/(STEM+'_RESULT.json')), old_result=sha(J/(OLD+'_RESULT.json')), cases=pins),
        checks=dict(total=len(checks), passed=sum(c['passed'] for c in checks), failed=[c for c in checks if not c['passed']]),
        diagnostics=diagnostics, qualified_primary=qualified, relative_changes=diffs,
        Q2_primary_s_minus2=cases[4]['Q2'], sensitivity_Q2_s_minus2=[c['Q2'] for c in cases[5:]],
        frozen_to_relaxed_Q2_ratio=cases[4]['Q2']/old_result['Q2_primary'],
        conditional_fixed_mean_standardized_residual=standardized,
        interpretation='Imposed uniform nonresponding polarization with retained contact. Not native formation, finite response, a monotonic response-time bound or posterior-marginalized exclusion.',
        seconds=time.perf_counter()-start)
    target = J/(STEM+'_AUDIT.json')
    with tempfile.NamedTemporaryFile(dir=J, prefix=target.name+'.partial.', delete=False) as f:
        temporary = Path(f.name)
        f.write((json.dumps(output, indent=2, allow_nan=False)+'\n').encode())
        f.flush()
        os.fsync(f.fileno())
    try:
        os.link(temporary, target)
    finally:
        temporary.unlink()
    print(json.dumps(dict(status=output['status'], checks=output['checks'], diagnostics=diagnostics,
                         ratio=output['frozen_to_relaxed_Q2_ratio'], sha256=sha(target), seconds=output['seconds'])))


if __name__ == '__main__':
    main()
