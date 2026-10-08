"""Independent positive-integrand/log-q audit; no producer import or PDE solve."""
import os
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[name] = '1'
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
STEM = 'LINEAR_GRADIENT_EXTERNAL_QUADRUPOLE_V001'
A0, GM = 1.0059833281731022e-10, 1.32712440018e20
GC, PC = 3*math.pi*A0/8, 648000*149597870700/math.pi
checks = []


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def check(name, error, limit):
    error = float(error)
    checks.append(dict(name=name, error=error, limit=limit,
                       passed=math.isfinite(error) and error <= limit))


def identity(name, yes):
    check(name, 0 if yes else 1, 0)


def unit_nodes(n):
    u, w = leggauss(n)
    return (u+1)/2, w/2


def endpoint(ge):
    g = ge/GC
    t = g**(1/3)
    for unused in range(16):
        t -= (t+t**3-g)/(1+3*t*t)
    return g, t


def positive_angular(beta, n):
    # Integration by parts: -I(beta)=2 beta int_0^1 u^2(1-u^2)/(1+beta*u^2)^2 du.
    u, w = unit_nodes(n)
    b = np.atleast_1d(beta)[:, None]
    return 2*b[:, 0]*((u*u*(1-u*u)/(1+b*u*u)**2)@w)


def coefficient(ge, ns, nlog, nangle):
    g, t0 = endpoint(ge)
    z, wz = unit_nodes(ns)
    t = t0/z
    # z=t0/t replaces s integration, removing its fractional-power endpoint.
    density = (1+t0*t0)*z*z*(z*z+3*t0*t0)/(z*z+t0*t0)**2
    weight = wz*density
    ulog, wlog = leggauss(nlog)
    edges = np.arange(-16., 21.)
    logq = (edges[:-1, None]+.5+.5*ulog).reshape(-1)
    qw = np.broadcast_to(.5*wlog, (len(edges)-1, nlog)).reshape(-1)
    q = np.exp(logq)
    qq = q[:, None]**2
    tt = t*t
    kt = 1-(1/(1+tt+qq))@weight
    difference = (2*tt/((1+tt+qq)*(1+3*tt+qq)))@weight
    beta = difference/kt
    aminus = positive_angular(beta, nangle)/kt
    cq = float(np.dot(qw, q**3*aminus)/math.pi)
    # This moment is exact in the continuum, not a finite-node UV check.
    mean_t2 = g*(2*math.atan(1/t0)+t0/(1+t0*t0))
    qmin, qmax = math.exp(-16), math.exp(20)
    lower_kt = t0*t0/(1+t0*t0)
    ir_bound = 4*qmin**3/(45*math.pi*lower_kt**2)
    uv_bound = 8*mean_t2/(15*math.pi)*(1/qmax+2/(3*qmax**3)+1/(5*qmax**5))
    return dict(ge=ge, spectral_nodes=ns, log_cell_order=nlog, angular_nodes=nangle,
                log_q_interval=[-16, 20], Cq_truncated=cq, Cq_upper_with_analytic_tails=cq+ir_bound+uv_bound,
                infrared_tail_bound=ir_bound, ultraviolet_tail_bound=uv_bound,
                spectral_weight_error=abs(float(weight.sum())-1),
                continuum_mean_t2=mean_t2, quadrature_mean_t2=float(np.dot(weight, tt)),
                equilibrium_endpoint_residual=abs(t0+t0**3-g)/g,
                min_KT=float(kt.min()), min_difference=float(difference.min()),
                max_beta=float(beta.max()))


def main():
    start = time.perf_counter()
    result_path = J/(STEM+'_RESULT.json')
    saved = json.loads(result_path.read_text())
    for name, pin in saved['custody'].items():
        identity('custody/'+name, sha(J/name) == pin)
    identity('input_units', saved['inputs']['a0'] == A0 and saved['inputs']['GMsolar'] == GM)
    check('gc', abs(saved['inputs']['gc']/GC-1), 1e-14)
    check('parsec', abs(saved['inputs']['pc']/PC-1), 1e-14)
    for c in saved['controls']:
        identity('saved_control/'+c['name'], c['passed'] and c['error'] <= c['limit'] and math.isfinite(c['error']))
    primary = saved['primary_cases']
    ref = primary[2]['Cq']
    changes = {str(i): abs(primary[i]['Cq']-ref)/ref for i in (1, 3, 4)}
    for key, value in changes.items():
        check('saved_refinement/'+key, abs(value-saved['relative_changes'][key]), 1e-14)
    qualified = all(c['Cq'] > 0 and c['min_KT'] > 0 and c['min_KL_minus_KT'] > 0 and
                    c['max_equilibrium_relative_residual'] < 1e-12 for c in primary)
    qualified = qualified and all(v < saved['inputs']['refinement_tolerance'] for v in changes.values())
    identity('saved_qualification', qualified and saved['qualified_linearized_coefficient'] and saved['all_controls_pass'])
    check('Fourier_prefactor', abs(4*math.pi*2*math.pi/(2*math.pi)**3-1/math.pi), 1e-15)
    beta = np.array([0., 1e-14, 1e-8, 1e-3, .1, 1., 10.])
    angular32, angular64 = positive_angular(beta, 32), positive_angular(beta, 64)
    check('positive_angular_refinement', float(np.max(abs(angular32-angular64)/np.maximum(angular64, 1e-30))), 1e-10)
    identity('angular_isotropy', angular64[0] == 0)
    check('small_anisotropy_normalization', abs(angular64[1]/beta[1]-4/15), 1e-12)
    runs = [coefficient(saved['inputs']['primary_ge'], *spec) for spec in
            [(96, 8, 32), (192, 16, 64), (384, 16, 64)]]
    for i, run in enumerate(runs):
        check('spectral_weight/'+str(i), run['spectral_weight_error'], 1e-12)
        check('continuum_moment/'+str(i), abs(run['quadrature_mean_t2']/run['continuum_mean_t2']-1), 1e-10)
        check('equilibrium/'+str(i), run['equilibrium_endpoint_residual'], 1e-14)
        identity('kernel_positivity/'+str(i), run['min_KT'] > 0 and run['min_difference'] > 0)
    fine = runs[-1]['Cq_truncated']
    check('independent_refinement', abs(runs[1]['Cq_truncated']/fine-1), 1e-7)
    check('combined_independent_refinement', abs(runs[0]['Cq_truncated']/fine-1), 1e-6)
    check('agreement_with_saved_coefficient', abs(fine/ref-1), 1e-6)
    check('analytic_tail_relative_bound', (runs[-1]['ultraviolet_tail_bound']+runs[-1]['infrared_tail_bound'])/fine, 1e-7)
    sensitivity = []
    for i, case in enumerate(saved['external_sensitivities']):
        run = coefficient(case['ge'], 192, 16, 64)
        check('sensitivity_agreement/'+str(i), abs(run['Cq_truncated']/case['Cq']-1), 1e-6)
        identity('sensitivity_scope/'+str(i), case['individual_admissibility'] and case['separately_refined'] is False)
        sensitivity.append(run)
    for item in saved['length_illustrations']:
        length = item['ell_pc']*PC
        check('SI_Q2/'+str(item['ell_pc']), abs(GM*ref/length**3/item['Q2_linear_s_2']-1), 1e-14)
        check('rM_over_ell/'+str(item['ell_pc']), abs(math.sqrt(GM/A0)/length/item['rM_over_ell']-1), 1e-14)
    output = dict(status='LINEAR_GRADIENT_AUDIT_PASSED' if all(c['passed'] for c in checks) else 'LINEAR_GRADIENT_AUDIT_FAILED',
        scope='Independent spectral-variable, positive angular and composite log-q quadrature only; no producer import, PDE solve, parameter fit or nonlinear Solar qualification.',
        pins=dict(audit_source=sha(Path(__file__)), saved_result=sha(result_path), inputs=saved['custody']),
        checks=dict(total=len(checks), passed=sum(c['passed'] for c in checks), failed=[c for c in checks if not c['passed']]),
        primary_runs=runs, sensitivity_checks=sensitivity,
        saved_Cq=ref, independent_to_saved_relative=fine/ref-1,
        tail_scope='Analytic continuum truncation bounds; finite quadrature and floating-point roundoff are separately checked, not rigorously interval-certified.',
        interpretation='Coefficient of linearized external-equilibrium Green response after isotropic-cusp subtraction. Does not prove uniform soft-mode/central validity or a nonlinear Solar pass.',
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
    print(json.dumps(dict(status=output['status'], checks=output['checks'], primary_runs=runs,
                         sensitivity_checks=sensitivity, independent_relative=output['independent_to_saved_relative'],
                         sha256=sha(target), seconds=output['seconds'])))


if __name__ == '__main__':
    main()
