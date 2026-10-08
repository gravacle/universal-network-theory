"""Saved-scalar/source audit only: no producer import or spectral-grid rerun."""
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile
import time

J = Path(__file__).resolve().parent
STEM = 'FINITE_SOURCE_GRADIENT_RESIDUAL_BOUND_V001'
checks = []


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name, error, limit=1e-12):
    error = float(error)
    checks.append(dict(name=name, error=error, limit=limit,
                       passed=math.isfinite(error) and error <= limit))


def same(name, yes):
    check(name, 0 if yes else 1, 0)


def rel(name, value, saved):
    check(name, abs(value-saved)/max(abs(value), abs(saved), 1e-300))


def main():
    start = time.perf_counter()
    result_path = J/(STEM+'_RESULT.json')
    source = json.loads(result_path.read_text())
    p = source['inputs']
    for name, pin in source['custody'].items():
        same('custody/'+name, sha(J/name) == pin)
    prior_path = J/'LINEAR_GRADIENT_EXTERNAL_QUADRUPOLE_V001_RESULT.json'
    prior = json.loads(prior_path.read_text())
    same('prior_status', prior['qualified_linearized_coefficient'])
    same('status', source['status'] == 'qualified_bound_evaluation' and source['all_numerical_controls_pass'])
    for c in source['controls']:
        same('saved_control/'+c['name'], c['passed'] and math.isfinite(c['error']) and c['error'] <= c['limit'])
    gm, ge, gc, sigma, eta = (p[k] for k in ('GM', 'ge', 'gc', 'gaussian_sigma_m', 'eta'))
    pc, au = p['pc'], p['AU']
    rel('parsec', 648000*au/math.pi, pc)
    rel('gc', 3*math.pi*p['a0']/8, gc)
    t0 = (ge/gc)**(1/3)
    for unused in range(16):
        t0 -= (t0+t0**3-ge/gc)/(1+3*t0*t0)
    mu = t0*t0/(1+t0*t0)
    rel('mu_lower_bound', mu, source['mu_floor_not_actual_KT0'])
    point = next(c['Cq'] for c in prior['primary_cases'] if c['Ns'] == c['Nx'] == 256)
    rel('point_coefficient', point, source['saved_point_coefficient_nominal'])
    Dinf = 2*gm/(math.pi*mu*sigma**2)
    D2 = 2*math.pi**.25*gm/(mu*math.sqrt(sigma))
    ratio = Dinf/ge
    # Derived directly in dimensional variables, not the producer's t/u expression.
    tail4 = 3/5*(3*ge+Dinf)**(4/3)*Dinf**(2/3)*D2**2/gc**2
    tail4 *= (gc/ge)**(8/3)*eta**(10/3)
    tail2 = (D2*(3*ratio+ratio*ratio))**2*eta**2
    moment2 = ge/gc*(2*math.atan(1/t0)+t0/(1+t0*t0))
    diagnostics = []
    for case in source['cases']:
        ell_pc = case['ell_pc']
        ell = ell_pc*pc
        tag = str(ell_pc)
        rows = case['enclosures']
        same('grids/'+tag, [r['cells'] for r in rows] == p['cells'])
        for r in rows:
            suffix = tag+'/'+str(r['cells'])
            rel('quartic_tail/'+suffix, tail4, r['quartic_tail_upper'])
            rel('quadratic_tail/'+suffix, tail2, r['residual_tail_upper'])
            rel('Gamma_tail/'+suffix, eta**2, r['gamma_tail_upper'])
            for key in ('gamma', 'residual_S', 'quartic_I4'):
                same('positive_enclosure/'+suffix+'/'+key, 0 <= r[key+'_lower'] <= r[key+'_upper'])
            same('saved_endpoint_checks/'+suffix, r['endpoint_ordered'] and r['monotone_t'] and r['monotone_v2'])
        for lo, hi in zip(rows[:-1], rows[1:]):
            for key in ('gamma', 'residual_S', 'quartic_I4'):
                violation = max(0., lo[key+'_lower']-hi[key+'_lower'], hi[key+'_upper']-lo[key+'_upper'])
                check('nesting/'+tag+'/'+str(hi['cells'])+'/'+key, violation/lo[key+'_upper'], p['arithmetic_allowance'])
        fine = rows[-1]
        for key in ('gamma', 'residual_S', 'quartic_I4'):
            diff = abs(rows[-2][key+'_upper']-fine[key+'_upper'])/fine[key+'_upper']
            check('last_refinement/'+tag+'/'+key, diff, p['refinement_gate'])
        gap = 1-fine['gamma_upper']
        rel('gap/'+tag, gap, case['coercivity_gap_lower'])
        same('gap_status/'+tag, gap > 0 and case['coercivity_certificate_available'])
        bulk = math.sqrt(fine['residual_S_upper']/gap)
        rel('bulk_bound/'+tag, bulk, case['bulk_error_bound_g_m_3_2'])
        observed = []
        for obs in case['observables']:
            R = obs['radius_AU']*au
            label = tag+'/'+str(obs['radius_AU'])
            adjoint = math.sqrt((9/(16*math.pi**2))*(4*math.pi/5)*(1/7+1/3)/R**3)
            quadratic = adjoint*bulk/ell
            quartic = adjoint*math.sqrt(.75*fine['quartic_I4_upper'])/ell
            rel('quadratic_Q/'+label, quadratic, obs['coercivity_Q_R_difference_bound_s_2'])
            rel('quartic_Q/'+label, quartic, obs['quartic_Q_R_difference_bound_s_2'])
            best = min(quadratic, quartic)
            rel('minimum_bound/'+label, best, obs['best_analytic_Q_R_difference_bound_s_2'])
            # Exact integrals of min(D q^2,2) times the two positive tail envelopes.
            D = sigma**2/(2*ell**2)+R**2/(14*ell**2)
            qc = math.sqrt(2/D)
            low = D*4/(15*math.pi*mu*mu)/5
            high_prefactor = 8*moment2/(15*math.pi)
            primitive = lambda q: q-2/q-1/(3*q**3)
            middle = D*high_prefactor*(primitive(qc)-primitive(1))
            upper = 2*high_prefactor*(1/qc+2/(3*qc**3)+1/(5*qc**5))
            coefficient = math.fsum((low, middle, upper))
            saved_corr = obs['finite_linear_correction']
            for key, value in [('D', D), ('qc', qc), ('M2_exact', moment2), ('coefficient_bound', coefficient)]:
                rel('linear_correction/'+label+'/'+key, value, saved_corr[key])
            correction = gm*coefficient/ell**3
            rel('linear_correction_Q/'+label, correction, saved_corr['Q_R_linear_minus_exact_point_bound_s_2'])
            nominal = gm*point/ell**3
            rel('nominal_Q/'+label, nominal, obs['inherited_point_Q_nominal_s_2'])
            for i, value in enumerate((nominal-best-correction, nominal+best+correction)):
                rel('nominal_interval/'+label+'/'+str(i), value, obs['nominal_combined_interval_s_2'][i])
            observed.append(dict(radius_AU=obs['radius_AU'], quadratic_bound=quadratic, quartic_bound=quartic,
                quadratic_to_quartic=quadratic/quartic, finite_linear_correction=correction,
                nominal_linear_point_Q=nominal, inherited_point_error_included=False))
        diagnostics.append(dict(ell_pc=ell_pc, coercivity_gap=gap,
            S_tail_fraction=tail2/fine['residual_S_upper'], I4_tail_fraction=tail4/fine['quartic_I4_upper'],
            finite_enclosure_relative_widths={k:(fine[k+'_upper']-fine[k+'_lower'])/fine[k+'_upper']
                                             for k in ('gamma','residual_S','quartic_I4')}, observables=observed))
    output = dict(status='FINITE_SOURCE_SAVED_AUDIT_PASSED' if all(c['passed'] for c in checks) else 'FINITE_SOURCE_SAVED_AUDIT_FAILED',
        scope='Saved scalars plus source-level inequality review. No producer import, spectral-grid rerun, PDE solve or fit. Enclosures are not directed-rounding certificates.',
        pins=dict(audit_source=sha(Path(__file__)), result=sha(result_path), inputs=source['custody']),
        checks=dict(total=len(checks), passed=sum(c['passed'] for c in checks), failed=[c for c in checks if not c['passed']]),
        diagnostics=diagnostics,
        interpretation='Conditional Gaussian-source finite-shell upper error bounds, not realized corrections, a Cassini estimator, existence/formation proof, or full-theory success.',
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
                         sha256=sha(target), seconds=output['seconds'])))


if __name__ == '__main__':
    main()
