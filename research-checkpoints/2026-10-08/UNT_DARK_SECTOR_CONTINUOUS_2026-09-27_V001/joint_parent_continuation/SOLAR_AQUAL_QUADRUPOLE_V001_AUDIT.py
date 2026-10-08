"""Saved-array AQUAL audit; no producer import or nonlinear/linear solve."""
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
STEM = 'SOLAR_AQUAL_QUADRUPOLE_V001'
AI = 8/(3*math.pi)
RATIO = 25.51664211557329
A0, GM = 1.0059833281731022e-10, 1.32712440018e20
RM = math.sqrt(GM/A0)
checks = []


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(name):
    return json.loads((J/name).read_text())


def check(name, value, gate):
    value = float(value)
    checks.append({'name': name, 'error': value, 'gate': gate,
        'passed': bool(math.isfinite(value) and value <= gate)})


def identity(name, flag):
    check(name, 0 if flag else 1, 0)


def relative(a, b, floor=1.):
    a, b = np.asarray(a), np.asarray(b)
    return float(np.max(abs(a-b))/max(floor, float(np.max(abs(b)))))


def derivative(y, h):
    out = np.empty_like(y)
    out[1:-1] = (y[2:]-y[:-2])/(2*h)
    out[0] = (-3*y[0]+4*y[1]-y[2])/(2*h)
    out[-1] = (3*y[-1]-4*y[-2]+y[-3])/(2*h)
    return out


def polynomials(u, L):
    # Independent recurrence, not the producer's legvander/legder evaluation.
    P, D = np.zeros((len(u), L+1)), np.zeros((len(u), L+1))
    P[:, 0] = 1
    if L:
        P[:, 1], D[:, 1] = u, 1
    for l in range(1, L):
        P[:, l+1] = ((2*l+1)*u*P[:, l]-l*P[:, l-1])/(l+1)
        D[:, l+1] = ((2*l+1)*(P[:, l]+u*D[:, l])-l*D[:, l-1])/(l+1)
    return P, D


def deficit(g):
    g = np.asarray(g)
    gi, w = AI*g, 1+(g/RATIO)**2
    h = gi/np.sqrt(w)
    y = 2/math.sqrt(3)*np.sinh(np.arcsinh(3*math.sqrt(3)*h/2)/3)
    theta = np.arctan2(1., y)
    fel = h*h/4*(1.5*theta-.5*np.sin(2*theta)-np.sin(4*theta)/8)
    ratio = np.divide(h-2*fel, gi, out=np.ones_like(gi), where=gi != 0)
    return ratio*w**(-1.5)


def polarization(h, order):
    nodes, weights = leggauss(order)
    delta, weights = (nodes+1)/2, weights/2
    h = np.atleast_1d(h)
    z = 2*delta[None, :]/math.sqrt(3)*np.sinh(np.arcsinh(3*math.sqrt(3)*h[:, None]/(2*delta[None, :]**2))/3)
    P = (z*delta[None, :]**2)@weights
    Pd = (delta[None, :]**3/(delta[None, :]**2+3*z*z))@weights
    return P, Pd


def trap(y, t):
    return float(np.sum((y[1:]+y[:-1])*.5*np.diff(t)))


def main():
    start = time.perf_counter()
    frozen, tests, result = (read(STEM+x+'.json') for x in ('_FROZEN', '_TESTS', '_RESULT'))
    for name, h in frozen['inputs'].items():
        path = J.parent/'joint_parent_dynamics'/name if name == 'SHAPE_REFERENCE_RESULTS.json' else J/name
        identity('pin/'+name, sha(path) == h)
    identity('tests_custody', tests['inputs'] == frozen['inputs'] and tests['all_pass'])
    for i, c in enumerate(tests['checks']):
        identity('saved_control/'+str(i), c['pass'] and math.isfinite(c['error']) and c['error'] <= c['limit'])
    identity('result_custody', result['inputs'] == frozen['inputs'])
    gg = np.geomspace(1e-8, 1e8, 101)
    gi, ww = AI*gg, 1+(gg/RATIO)**2
    PP, _ = polarization(gi/np.sqrt(ww), 512)
    PP2, _ = polarization(gi/np.sqrt(ww), 256)
    dq = 2*PP/gi*ww**(-1.5)
    check('deficit_mechanical_positive_integral', relative(deficit(gg), dq), 1e-8)
    check('polarization_256_512', relative(2*PP2/gi*ww**(-1.5), dq), 1e-8)
    cases, diagnostics, pins = [], [], {}
    for index in range(7):
        name = STEM+'_CASE_'+str(index)+'.json'
        case = read(name)
        pins[name] = sha(J/name)
        spec = frozen['specs'][index] if index < 5 else frozen['specs'][-1]
        ext = frozen['external_accelerations'][0 if index < 5 else index-4]
        identity(name+'/identity', case['index'] == index and case['inputs'] == frozen['inputs'] and case['spec'] == spec and case['external_acceleration'] == ext and case['a0'] == A0 and case['GM'] == GM and case['shape_ratio'] == RATIO)
        if index < 5:
            identity(name+'/result_pin', result['receipt_hashes'][name] == pins[name])
        n, L, nq, ri, ro = spec
        radii = np.asarray(case['radii'])
        t = np.linspace(math.log(ri), math.log(ro), n)
        h, ell = t[1]-t[0], np.arange(L+1)
        check(name+'/radial_grid', relative(radii, np.exp(t)), 1e-14)
        check(name+'/units', abs(case['rM']/RM-1), 1e-14)
        psi, storedbr, storedth = (np.asarray(case[k]) for k in ('psi_modes', 'Br_modes', 'Theta_modes'))
        identity(name+'/array_shapes', psi.shape == storedbr.shape == storedth.shape == (n, L+1))
        u, wq = leggauss(nq)
        P, D = polynomials(u, L)
        sintheta = np.sqrt(1-u*u)
        projection = (wq[:, None]*P)*(2*ell+1)[None, :]/2
        aprojection = (wq*sintheta)[:, None]*D*(2*ell+1)[None, :]/2
        e = ext/A0
        rr = radii[:, None]
        internalr = 1/rr**2+(derivative(psi, h)@P.T)/rr
        internalt = -sintheta*(psi@D.T)/rr
        gr, gt = internalr-e*u, internalt+e*sintheta
        dm, de = deficit(np.hypot(gr, gt)), float(deficit(e))
        # Algebraically cancel the uniform external polarization before projecting.
        br = (dm*internalr-(dm-de)*e*u)@projection
        th = (dm*internalt+(dm-de)*e*sintheta)@aprojection
        check(name+'/Br_reconstruction', relative(br, storedbr), 1e-10)
        check(name+'/Theta_reconstruction', relative(th, storedth), 1e-10)
        check(name+'/mu_min', abs(float(np.min(1-dm))-case['mu_min']), 1e-10)
        mu = 1-de
        step = 1e-4
        Le = (math.log(1-float(deficit(e*math.exp(step))))-math.log(1-float(deficit(e*math.exp(-step)))))/(2*step)
        check(name+'/mu_external', abs(mu-case['mu_external']), 1e-12)
        check(name+'/L_external', abs(Le-case['L_external']), 1e-10)
        hv = AI*e/math.sqrt(1+(e/RATIO)**2)
        PP, Pd = polarization([hv], 512)
        z = (e/RATIO)**2
        logD = AI*e*Pd[0]*(1+z)**(-1.5)/PP[0]-1-3*z/(1+z)
        analyticLe = -de*logD/mu
        check(name+'/analytic_external_derivative', abs(Le-analyticLe), 1e-7)
        outer = ((1-1/(mu*np.sqrt(1+Le*(1-u*u))))/radii[-1])@projection
        src = radii[:, None]*(derivative(br, h)+2*br+th)
        lower, upper = math.exp(-h/2)/h**2, math.exp(h/2)/h**2
        diagonal = -2*np.cosh((ell+.5)*h)/h**2
        residual = lower*psi[:-2]+diagonal*psi[1:-1]+upper*psi[2:]-src[1:-1]
        inner_residual = psi[0]-np.exp(-ell*h)*psi[1]
        outer_residual = psi[-1]-outer
        check(name+'/inner_Robin', float(np.max(abs(inner_residual))), 1e-12)
        check(name+'/outer_Dirichlet', float(np.max(abs(outer_residual))), 1e-8)
        mask = (radii >= .003)&(radii <= .02)
        plateaux = psi[mask, 2]/radii[mask]**2
        c2 = float(np.median(plateaux))
        plateau_error = float(np.max(abs(plateaux-c2))/max(abs(c2), 1e-5))
        check(name+'/c2', abs(c2-case['c2']), 1e-12)
        check(name+'/plateau', abs(plateau_error-case['plateau_relative']), 1e-12)
        q2 = -3*A0/RM*c2
        check(name+'/Q2_conversion', abs(q2/case['Q2']-1), 1e-12)
        identity(name+'/declared_convergence', case['converged'] == (case['status'] == 'converged' and case['fixed_point_defect'] < 3e-8))
        # Exact discrete Green weights for the fitted radial recurrence; no solve.
        j = np.arange(1, n-1)
        weights = -np.expm1(-5*h*(n-1-j))/(2*math.sinh(2.5*h)/h**2*radii[j]**2)
        discrete = outer[2]/radii[-1]**2-float(weights@src[1:-1, 2])
        inner_c2 = psi[0, 2]/radii[0]**2
        eps0 = inner_residual[2]
        inner_correction = math.exp(2*h)*eps0/(radii[0]**2*(math.exp(2*h)-math.exp(-3*h)))*(-math.expm1(-5*h*(n-1)))
        identity_defect = inner_c2-(discrete-float(weights@residual[:, 2])+inner_correction+outer_residual[2]/radii[-1]**2)
        check(name+'/discrete_Green_identity', abs(identity_defect), 1e-9)
        # Continuum finite-bound Green formula, integrated by parts (no Br derivative).
        R = radii[-1]
        weight_a = 1/radii[0]-radii[0]**4/R**5
        integ = trap((3/radii+2*radii**4/R**5)*br[:, 2]+(1/radii-radii**4/R**5)*th[:, 2], t)-weight_a*br[0, 2]
        finitegreen = outer[2]/R**2-integ/5
        raw = -(br[-1, 2]/R-br[0, 2]/radii[0]+trap((3*br[:, 2]+th[:, 2])/radii, t))/5
        check(name+'/stored_raw_Green', abs(raw-case['finite_domain_green_c2_uncorrected']), 1e-10)
        flux = radii**2/2*(((1-dm)*gr)@wq)
        diagnostics.append({'index': index, 'Q2_s_minus2': q2, 'c2': c2, 'plateau_relative': plateau_error,
            'discrete_modal_residual_scaled': float(np.max(abs(residual))/max(1., np.max(abs(src[1:-1])))),
            'quadrupole_modal_residual_max': float(np.max(abs(residual[:, 2]))),
            'discrete_Green_c2': discrete, 'discrete_Green_relative_to_plateau': (discrete-c2)/max(abs(c2),1e-5),
            'inner_c2': inner_c2, 'weighted_residual_c2': float(weights@residual[:, 2]),
            'finite_continuum_Green_c2': finitegreen, 'finite_continuum_Green_relative_to_plateau': (finitegreen-c2)/max(abs(c2),1e-5),
            'raw_continuum_Green_c2': raw, 'raw_continuum_Green_relative_to_plateau': (raw-c2)/max(abs(c2),1e-5),
            'flux_max_abs_deviation_from_unit_mass': float(np.max(abs(flux-1))),
            'flux_transition_max_abs_deviation': float(np.max(abs(flux[(radii>.05)&(radii<10)]-1))),
            'analytic_L_external': float(analyticLe), 'highest_mode_max_abs': float(np.max(abs(psi[:, -1])))})
        cases.append(case)
    scale = max(abs(cases[4]['c2']), 1e-5)
    diffs = {f'{a}_{b}': abs(cases[a]['c2']-cases[b]['c2'])/scale for a,b in ((1,2),(2,3),(3,4))}
    qualified = all(c['converged'] and c['plateau_relative'] < .01 for c in cases[:5]) and all(x < .05 for x in diffs.values())
    identity('primary_qualification', qualified == result['qualified_primary'] and qualified)
    for key, value in diffs.items():
        check('refinement/'+key, abs(value-result['relative_changes'][key]), 1e-14)
    residual = (cases[4]['Q2']-1.6e-27)/1.8e-27
    check('Cassini_standardized_residual', abs(residual-result['cassini_standardized_residual']), 1e-12)
    output = {'status': 'SAVED_SOLAR_AUDIT_PASSED' if all(c['passed'] for c in checks) else 'SAVED_SOLAR_AUDIT_FAILED',
        'scope': 'No producer import, refit, Poisson solve or nonlinear iteration. Independent recurrence source/Green checks on saved fields. Added residual, flux and continuum Green values are descriptive, not retroactive gates.',
        'pins': {'audit_source': sha(Path(__file__)), 'freeze': sha(J/(STEM+'_FROZEN.json')), 'result': sha(J/(STEM+'_RESULT.json')), 'tests': sha(J/(STEM+'_TESTS.json')), 'cases': pins},
        'checks': {'total': len(checks), 'passed': sum(c['passed'] for c in checks), 'failed': [c for c in checks if not c['passed']]},
        'diagnostics': diagnostics, 'qualified_primary': qualified, 'relative_changes': diffs,
        'Q2_primary_s_minus2': cases[4]['Q2'], 'sensitivity_Q2_s_minus2': [c['Q2'] for c in cases[5:]],
        'conditional_fixed_prediction_standardized_residual': residual,
        'interpretation': 'Qualified fixed-calibration mean prediction under uniform-external-field static AQUAL; not posterior-marginalized exclusion. Galaxy source/calibration uncertainties and completion uncertainty not propagated; not all UNT.',
        'seconds': time.perf_counter()-start}
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
    print(json.dumps({'status': output['status'], 'checks': output['checks'], 'diagnostics': diagnostics,
        'Q2': output['Q2_primary_s_minus2'], 'fixed_prediction_residual': residual, 'sha256': sha(target), 'seconds': output['seconds']}))


if __name__ == '__main__':
    main()
