"""One constrained charged-background response; no fit or nonlinear galaxy claim."""
from pathlib import Path
import hashlib
import json
import math
import resource
import time

import numpy as np

from bounded_clock_shared_prediction_v001 import charge_root, quantities

BASE = Path(__file__).resolve().parent
PROTOCOL = BASE / 'CHARGED_CLOCK_RESPONSE_V001.md'
OUTPUT = BASE / 'CHARGED_CLOCK_RESPONSE_V001_RESULT.json'
EPS = 1e-6
KB, C, LAMBDA_S = 1., 1., 1.
OA, OB, OC = .7, .0125, .2875
Q0, WAVENUMBER = 1., 30000.
AI, SEED = .01, 1e-5
H0_KMS_MPC, C_KMS = 73.6, 299792.458
H0_SI = H0_KMS_MPC * 1000 / 3.085677581491367e22
A0 = 1.2e-10
X0 = math.log(AI)
EYE = np.eye(7)
NAMES = ['Phi', 'delta_b', 'H0_theta_b', 'clock_delta_rho_over_enthalpy',
         'H0_theta_clock', 'Z', 'H0_alpha']
SCALE = np.array([1/WAVENUMBER**2, 1., 1/WAVENUMBER**2, 1.,
                  1/WAVENUMBER**2, 1/WAVENUMBER**2, 1/WAVENUMBER**2])


def calibrated_charge():
    lo, hi = 0., 2*OC/OA
    for _ in range(80):
        d = (lo+hi)/2
        if OA*quantities(EPS, charge_root(EPS, d))[3] > OC:
            hi = d
        else:
            lo = d
    return (lo+hi)/2


D0 = calibrated_charge()


def background(x, dust=False):
    a = math.exp(x)
    rb = OB/a**3
    if dust:
        return dict(a=a, rb=rb, W=OC/a**3, h=math.sqrt(OA+(OB+OC)/a**3),
                    Q=Q0, cs2=0., s=0., q=1., charge=OC/OA/a**3)
    d = D0/a**3
    ss = charge_root(EPS, d)
    q, _, pex, rex, cs2 = quantities(EPS, ss)
    W = OA*q*d
    h = math.sqrt(rb+OA*(1+rex))
    return dict(a=a, rb=rb, W=W, h=h, Q=Q0*q, cs2=cs2, s=ss, q=q, charge=d)


def matrix(x, dust=False):
    b = background(x, dust)
    h, rb, W, Q, cs = (b[z] for z in ('h', 'rb', 'W', 'Q', 'cs2'))
    kp = WAVENUMBER**2/b['a']**2
    phi, db, vb, F, vc, Z, alpha = EYE
    chi = Q*(vc+alpha)
    E = (Z-C*chi)/KB
    pressure = cs*(W*F+kp*Z/3)
    m = np.empty((7, 7))
    m[0] = -phi+1.5*(W*vc+rb*vb)/h
    m[1] = 3*m[0]-kp*vb/h
    m[2] = phi/h
    m[3] = 3*m[0]-kp*vc/h-cs*kp*Z/W
    m[4] = 3*cs*vc+(phi+pressure/W)/h
    m[5] = -Z+3*W*chi/(Q*h)+C*Q*(E-chi)/h
    m[6] = (E-phi)/h
    return m, b


def initial(b, basis=True):
    h, W, rb = b['h'], b['W'], b['rb']
    kp = WAVENUMBER**2/b['a']**2
    y = np.zeros((7, 8 if basis else 2))
    offset = 6 if basis else 0
    if basis:
        for col, row in enumerate(range(1, 7)):
            y[row, col] = SCALE[row]
            y[0, col] = -1.5*(W*y[3, col]+rb*y[1, col]
                                   +3*h*(W*y[4, col]+rb*y[2, col]))/kp
    # Declared ordinary-matter density perturbation, initially at rest.
    y[1, offset] = SEED
    y[0, offset] = -1.5*rb*SEED/kp
    # Declared adiabatic development case, initial Phi_dot=0, chi=Z=0.
    j = offset+1
    ph = -1.5*(W+rb)*SEED/(kp+3*h*h)
    v = 2*h*ph/(3*(W+rb))
    y[:, j] = [ph, SEED, v, SEED, v, 0., -v]
    return y/SCALE[:, None]


def gauss_step(y, x, dx, rhs_matrix):
    z = math.sqrt(3)/6
    a11, a12, a21, a22 = .25, .25-z, .25+z, .25
    m1 = rhs_matrix(x+(.5-z)*dx)
    m2 = rhs_matrix(x+(.5+z)*dx)
    n = len(y)
    eye = np.eye(n)
    lhs = np.block([[eye-dx*a11*m1, -dx*a12*m1],
                    [-dx*a21*m2, eye-dx*a22*m2]])
    rhs = np.vstack((m1@y, m2@y))
    stages = np.linalg.solve(lhs, rhs)
    return y+.5*dx*(stages[:n]+stages[n:])


def integrate(nstep, dust=False):
    # In the dust comparator only its five metric/matter rows are needed.
    keep = np.array([0, 1, 2, 3, 4]) if dust else np.arange(7)
    scales = SCALE[keep]
    y = initial(background(X0, dust), basis=not dust)[keep]
    dx = -X0/nstep
    saved = [y.copy()]

    def mm(x):
        m, _ = matrix(x, dust)
        m = m[np.ix_(keep, keep)]
        return m*scales[None, :]/scales[:, None]

    for i in range(nstep):
        y = gauss_step(y, X0+i*dx, dx, mm)
        if (i+1) % (nstep//64) == 0:
            saved.append(y.copy())
    return np.array(saved)


def max_relative(lhs, rhs):
    norm = max(float(np.max(np.abs(lhs))), float(np.max(np.abs(rhs))), 1e-300)
    return float(np.max(np.abs(lhs-rhs)))/norm


def identities():
    errors = dict(constraint_propagation=0., phase_current=0., einstein_trace=0.,
                  original_E_equation=0., background_charge=0.)
    for x in np.linspace(X0, 0., 33):
        m, b = matrix(float(x))
        h, W, rb, Q, cs = (b[z] for z in ('h', 'W', 'rb', 'Q', 'cs2'))
        hp = -1.5*(W+rb)/h
        wp, rp = -3*(1+cs)*W, -3*rb
        kp = WAVENUMBER**2/b['a']**2
        ph, db, vb, F, vc, Z, al = EYE
        chi = Q*(vc+al)
        erow = (Z-C*chi)/KB
        pr = cs*(W*F+kp*Z/3)
        crow = 2*kp*ph+3*(W*F+rb*db)+9*h*(W*vc+rb*vb)
        cp = -4*kp*ph+3*(wp*F+rp*db)+9*hp*(W*vc+rb*vb)+9*h*(wp*vc+rp*vb)
        err = max_relative(cp+crow@m, -3*crow)
        errors['constraint_propagation'] = max(errors['constraint_propagation'], err)
        urow = W*F+kp*Z/3
        up = wp*F-2*kp*Z/3
        urhs = -3*(1+cs)*urow+3*W*m[0]+C*Q*kp*(erow-chi)/(3*h)+W*kp*al/h
        errors['phase_current'] = max(errors['phase_current'], max_relative(up+urow@m, urhs))
        pdot = h*m[0]
        pddot = -h*hp*ph-h*pdot+1.5*(h*wp*vc+W*h*m[4]+h*rp*vb+rb*h*m[2])
        # Compare before subtracting large terms, with shared term scale.
        trace_lhs = pddot+4*h*pdot+(2*h*hp+3*h*h)*ph
        norm = max(np.max(abs(pddot)), np.max(abs(4*h*pdot)),
                   np.max(abs((2*h*hp+3*h*h)*ph)), np.max(abs(1.5*pr)))
        errors['einstein_trace'] = max(errors['einstein_trace'], float(np.max(abs(trace_lhs-1.5*pr))/norm))
        chip = -3*cs*chi+Q*(m[4]+m[6])
        ep = (m[5]-C*chip)/KB
        erhs = -h*erow+(3*W/Q*chi-C*(Q*pr/W+(h+Q)*chi-3*cs*h*Q*al))/KB
        errors['original_E_equation'] = max(errors['original_E_equation'], max_relative(h*ep, erhs))
        errors['background_charge'] = max(errors['background_charge'], abs(b['a']**3*b['charge']/D0-1))
    return errors


def eds_control(nstep=2048):
    kval = 30.
    phi = -1e-5

    def exact(x):
        a = math.exp(x)
        h = a**-1.5
        return np.array([phi, -2*phi-2*kval*kval*a*phi/3, 2*phi/(3*h)])[:, None]

    def mm(x):
        a = math.exp(x)
        h, kp = a**-1.5, kval*kval/a**2
        p = np.array([-1., 0., 1.5*h])
        return np.array([p, 3*p-np.array([0., 0., kp/h]), [1/h, 0., 0.]])

    y, dx = exact(X0), -X0/nstep
    largest = 0.
    for i in range(nstep):
        y = gauss_step(y, X0+i*dx, dx, mm)
        if (i+1) % 32 == 0:
            yy = exact(X0+(i+1)*dx)
            largest = max(largest, float(np.max(np.abs((y-yy)/yy))))
    return largest


def convergence(coarse, fine):
    peak = np.max(abs(fine), axis=0)
    floor = 1e-10*np.max(peak, axis=0)[None, :]
    norm = np.maximum(peak, floor)
    diff = np.max(abs(coarse-fine), axis=0)
    return dict(max_normalized=float(np.max(diff/norm)), per_component_column=(diff/norm).tolist(),
                max_absolute_scaled=float(np.max(diff)))


def diagnostics(history):
    xs = np.linspace(X0, 0., len(history))
    raw = history*SCALE[None, :, None]
    constraint_peak = 0.
    series = {key: [] for key in ('a', 'Zdot', 'HZ', 'KQchi', 'CQEminuschi',
                                    'actual_rate_fraction', 'frozen_rate_fraction',
                                    'rate_margin_fraction', 'spatial_nonlinearity',
                                    'peculiar_baryon', 'peculiar_vector', 'phi_dot_over_Q')}
    for j, x in enumerate(xs):
        m, b = matrix(float(x))
        y = raw[j]
        h, W, rb, Q, cs = (b[z] for z in ('h', 'W', 'rb', 'Q', 'cs2'))
        kp = WAVENUMBER**2/b['a']**2
        terms = np.array([2*kp*y[0], 3*W*y[3], 3*rb*y[1], 9*h*W*y[4], 9*h*rb*y[2]])
        residual = abs(np.sum(terms, axis=0))/np.maximum(np.sum(abs(terms), axis=0), 1e-200)
        constraint_peak = max(constraint_peak, float(np.max(residual)))
        yp = y[:, 6:]
        chi = Q*(yp[4]+yp[6])
        E = (yp[5]-C*chi)/KB
        rate = cs*(yp[3]+kp*yp[5]/(3*W))
        ss, q = b['s'], b['q']
        low = EPS*ss/((1+ss)*q*(q+1))
        high = EPS/((1+ss)*q*(math.sqrt(1+EPS)+q))
        margin = min(low, high)
        values = dict(a=b['a'], Zdot=h*(m@yp)[5], HZ=h*yp[5],
                      KQchi=3*W/Q*chi, CQEminuschi=C*Q*(E-chi),
                      actual_rate_fraction=rate, frozen_rate_fraction=-yp[0],
                      rate_margin_fraction=margin,
                      spatial_nonlinearity=np.sqrt(kp)*abs(chi)*H0_SI*299792458./((1+LAMBDA_S)*A0),
                      peculiar_baryon=np.sqrt(kp)*abs(yp[2]),
                      peculiar_vector=np.sqrt(kp)*abs(yp[6]),
                      phi_dot_over_Q=rate+yp[0])
        for key, value in values.items():
            series[key].append(np.asarray(value).tolist())
    rows = []
    late = xs >= math.log(.1)-1e-12
    for col, name in enumerate(('baryon_isocurvature', 'adiabatic_development')):
        zt = np.array(series['Zdot'])[:, col]
        retained = sum(np.array(series[key])[:, col]**2 for key in ('HZ', 'KQchi', 'CQEminuschi'))
        time_norm = math.sqrt(float(np.trapezoid(zt[late]**2, xs[late])/np.trapezoid(retained[late], xs[late])))
        rate = np.array(series['actual_rate_fraction'])[:, col]
        frozen = np.array(series['frozen_rate_fraction'])[:, col]
        margin = np.array(series['rate_margin_fraction'])
        peak_rate = float(np.max(abs(rate)/margin))
        validity = dict(delta_b=float(np.max(abs(raw[:, 1, col+6]))),
                        clock_enthalpy_contrast=float(np.max(abs(raw[:, 3, col+6]))),
                        metric=float(np.max(abs(raw[:, 0, col+6]))), rate_to_nearest_margin=peak_rate,
                        spatial_nonlinearity=float(np.max(np.array(series['spatial_nonlinearity'])[:, col])),
                        peculiar_baryon=float(np.max(np.array(series['peculiar_baryon'])[:, col])),
                        peculiar_vector=float(np.max(np.array(series['peculiar_vector'])[:, col])))
        rows.append(dict(preparation=name, final_state=dict(zip(NAMES, raw[-1, :, col+6].tolist())),
                         frozen_Z_time_term_L2_ratio=time_norm, frozen_Z_10percent_screen=time_norm <= .1,
                         max_actual_rate_to_nearest_margin=peak_rate,
                         max_frozen_phase_rate_to_nearest_margin=float(np.max(abs(frozen)/margin)),
                         validity_maxima=validity, within_conservative_linear_window=max(validity.values()) <= .1,
                         initial_amplitude_upper_for_linear_window=SEED*.1/max(validity.values())))
    return dict(max_normalized_constraint=constraint_peak, selected_preparations=rows, series=series)


def main():
    started = time.monotonic()
    errors = identities()
    print(json.dumps(dict(identity_errors=errors)), flush=True)
    eds = eds_control()
    histories = {}
    for n in (512, 1024, 2048):
        histories[n] = integrate(n)
        print(json.dumps(dict(completed_steps=n, elapsed_seconds=time.monotonic()-started)), flush=True)
    ref = integrate(2048, dust=True)
    conv = convergence(histories[1024], histories[2048])
    dg = diagnostics(histories[2048])
    fine = histories[2048]*SCALE[None, :, None]
    reference = ref*SCALE[None, :5, None]
    comparisons = []
    for j, label in enumerate(('baryon_isocurvature', 'adiabatic_development')):
        comparisons.append(dict(preparation=label, candidate_final_delta_b=float(fine[-1, 1, j+6]),
                                reference_final_delta_b=float(reference[-1, 1, j]),
                                candidate_over_reference_delta_b=float(fine[-1, 1, j+6]/reference[-1, 1, j]),
                                candidate_over_reference_Phi=float(fine[-1, 0, j+6]/reference[-1, 0, j]),
                                candidate_final_clock_F_over_delta_b=float(fine[-1, 3, j+6]/fine[-1, 1, j+6])))
    controls = dict(matrix_identities=max(errors.values()) <= 1e-10, eds=eds <= 1e-7,
                    constraint=dg['max_normalized_constraint'] <= 1e-6,
                    trajectory_convergence=conv['max_normalized'] <= 1e-4)
    result = dict(protocol_sha256=hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  scope='Constrained linear response on one specified background and scale; no observed or nonlinear galaxy score.',
                  fixed=dict(eps=EPS, KB=KB, lambda_s=LAMBDA_S, Q0_over_H0=Q0, K=WAVENUMBER,
                             H0_km_s_Mpc=H0_KMS_MPC, a0_SI=A0, omega_A=OA, omega_b_cos=OB,
                             omega_clock_excess_today=OC, conserved_charge_d0=D0, initial_a=AI, initial_amplitude=SEED,
                             inverse_k_kpc=C_KMS/H0_KMS_MPC/WAVENUMBER*1000),
                  identity_errors=errors, eds_max_relative_error=eds,
                  convergence_512_1024=convergence(histories[512], histories[1024]),
                  convergence_1024_2048=conv, controls=controls, all_controls_passed=all(controls.values()),
                  diagnostics=dg, comparisons=comparisons, x_checkpoints=np.linspace(X0, 0., 65).tolist(),
                  state_names=NAMES, state_scalings=SCALE.tolist(),
                  final_six_column_response_scaled=histories[2048][-1, :, :6].tolist(),
                  trajectories_scaled={str(n): y.tolist() for n, y in histories.items()},
                  comparator_trajectory_scaled=ref.tolist(), elapsed_seconds=time.monotonic()-started,
                  peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with OUTPUT.open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps({key: result[key] for key in ('controls', 'eds_max_relative_error', 'comparisons', 'elapsed_seconds', 'peak_RSS_bytes')}, indent=2))
    print(json.dumps(dg['selected_preparations'], indent=2))
    if not result['all_controls_passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
