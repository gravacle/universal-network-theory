#!/usr/bin/env python3
"""Guarded supplied-metric geodesic and independent material-flow component."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, math, os, sys, traceback
AUTHOR_DRAFT = False
J = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation')
SOURCE = 'cross_u_full_metric_geodesic_and_rotating_material_v001.py'
STEM = 'CROSS_U_FULL_METRIC_GEODESIC_AND_ROTATING_MATERIAL_V001'
PROTOCOL = STEM + '.md'
PROTOCOL_SHA = '971935f5307b660f8b439342f0933537f2e38c4965f02cf24190f3147f2c6bd5'
PINS = {
    'CROSS_U_GENERAL_METRIC_ORBIT_AND_FLRW_TIME_DEPENDENCE_V001.md': 'b3fd1355c03ed78cb702844cb05e34accb9e51d648d89c21db1bafd47dfcef59',
    'NATIVE_ROTATING_MATERIAL_CLOCK_SOURCE_EXTENSION_V001.md': 'e8911d59ae25f9d397a57a6dcd6d0ca5c450df82566935c00f8436568f7484ff',
    'CROSS_U_EPS5_FLRW_GALAXY_JUNCTION_V001.md': 'baa25990f0b2d4ca925e1a74fb65b40c2968890bd552e9f64541e620e07c6965',
    'reviewed_cross_u_full_metric_geodesic_and_rotating_material_v001_306_d3957ded.py': 'd3957ded09f5955bfa91f2bd365608e57aed6092773b543d9df38d08b9ea4be9',
    'REVIEWED_CROSS_U_FULL_METRIC_GEODESIC_AND_ROTATING_MATERIAL_V001_27_26dc2071.md': '26dc20710a1690479757bc34b55adb17464f122cca004ecf81774e64583a3a2e'}
FLAGS = {k: False for k in ('galaxy_metric_supplied', 'material_flow_solved', 'source_history_registered',
    'FLRW_junction_solved', 'galaxy_velocity_qualified', 'observational_success_qualified')}
np = None
CREATED, RAW, CONTROLS = {}, {}, []
EPS = sys.float_info.epsilon
TOL = 2048 * EPS

def floating_refusal(function):
    def checked(*args, **kwargs):
        try:
            with np.errstate(over='raise', divide='raise', invalid='raise'):
                return function(*args, **kwargs)
        except (FloatingPointError, OverflowError, ZeroDivisionError) as exc:
            raise ValueError('Derived floating arithmetic refused in ' + function.__name__) from exc
    return checked

def finite_result(value, name):
    if isinstance(value, dict):
        for key, item in value.items(): finite_result(item, name + '.' + key)
    elif value is not None and not np.isfinite(value).all(): raise ValueError('Nonfinite derived output: ' + name)
    return value

def real(value, shape, name):
    a = np.asarray(value)
    if a.shape != shape or a.dtype.kind not in 'fiu': raise ValueError('Real numeric shape: ' + name)
    a = a.astype(np.float64, copy=True)
    if not np.isfinite(a).all(): raise ValueError('Finite operand: ' + name)
    return a

@floating_refusal
def metric_geometry(g, dg, cp):
    """dg[alpha,mu,nu]=partial_alpha g_mu_nu; x^0=t seconds."""
    if not isinstance(cp, (int, float)) or not math.isfinite(cp) or cp <= 0: raise ValueError('Positive finite cp')
    cp = float(cp); cp2 = cp * cp
    if not math.isfinite(cp2) or cp2 <= 0: raise ValueError('Finite positive derived cp squared')
    g = real(g, (4, 4), 'g'); dg = real(dg, (4, 4, 4), 'dg')
    if not np.array_equal(g, g.T) or not np.array_equal(dg, dg.swapaxes(1, 2)):
        raise ValueError('Symmetric supplied metric/jet; no symmetrization')
    h = g[1:, 1:].copy()
    try: np.linalg.cholesky(h); inv = np.linalg.inv(g)
    except np.linalg.LinAlgError as exc: raise ValueError('Invertible metric with SPD spatial h') from exc
    if not np.isfinite(inv).all() or inv[0, 0] >= 0: raise ValueError('Lorentz metric with timelike t gradient')
    lapse = 1 / math.sqrt(-cp2 * float(inv[0, 0]))
    beta = -inv[0, 1:] / inv[0, 0]
    if not math.isfinite(lapse) or lapse <= 0 or not np.isfinite(beta).all(): raise ValueError('Finite positive lapse and finite shift')
    gamma = np.empty((4, 4, 4), dtype=np.float64)
    for mu in range(4):
        for nu in range(4): gamma[:, mu, nu] = .5 * (inv @ (dg[mu, :, nu] + dg[nu, :, mu] - dg[:, mu, nu]))
    if not np.isfinite(gamma).all(): raise ValueError('Nonfinite Christoffel contraction')
    return finite_result(dict(g=g, dg=dg, inverse=inv, h=h, N=lapse, beta=beta, Gamma=gamma, cp=cp), 'geometry')

@floating_refusal
def normal_observer(geometry, w, causal='timelike', axis=None):
    w = real(w, (3,), 'coordinate velocity'); cp = geometry['cp']
    W = np.concatenate(([1.], w)); norm = float(W @ geometry['g'] @ W)
    v = (w + geometry['beta']) / geometry['N']; v2 = float(v @ geometry['h'] @ v)
    if not math.isfinite(norm) or not math.isfinite(v2) or v2 < 0: raise ValueError('Finite causal norm and nonnegative finite observer speed')
    if causal == 'timelike':
        if norm >= 0 or v2 >= cp * cp: raise ValueError('Strict future timelike coordinate velocity')
        ut = cp / math.sqrt(-norm); lorentz = geometry['N'] * ut
    elif causal == 'null':
        if abs(norm) / max(cp * cp, abs(norm)) > 128 * EPS: raise ValueError('Supplied null normalization')
        ut = lorentz = None
    else: raise ValueError('Causal kind must be timelike or null')
    result = dict(W=W, gWW=norm, normal_velocity=v, normal_speed_squared=v2,
        dt_dproper=ut, normal_Gamma=lorentz)
    if axis is not None:
        axis = real(axis, (3,), 'supplied spatial axis'); length2 = float(axis @ geometry['h'] @ axis)
        if length2 <= 0: raise ValueError('Nonzero supplied spatial axis')
        result['axis_projection'] = float(axis @ geometry['h'] @ v) / math.sqrt(length2)
    return finite_result(result, 'observer')

@floating_refusal
def geodesic_rhs(geometry, w, causal='timelike'):
    """Return dy/dt for y=(x^i,w^i), and the exact nonaffinity row."""
    observed = normal_observer(geometry, w, causal)
    GWW = np.einsum('amn,m,n->a', geometry['Gamma'], observed['W'], observed['W'])
    dw = -GWW[1:] + observed['W'][1:] * GWW[0]
    rhs = np.concatenate((observed['W'][1:], dw))
    if not np.isfinite(rhs).all(): raise ValueError('Nonfinite geodesic RHS')
    return finite_result(dict(rhs=rhs, dw_dt=dw, GammaWW=GWW, dlog_ut_dt=-float(GWW[0]), observer=observed), 'geodesic')

@floating_refusal
def material_kinematics(geometry, u, du):
    """Independent u^mu=dx^mu/dtau_M; du[alpha,mu]=partial_alpha u^mu."""
    u = real(u, (4,), 'independent material u'); du = real(du, (4, 4), 'independent material du')
    cp = geometry['cp']; cov = geometry['g'] @ u; norm = float(u @ cov)
    if not math.isfinite(norm) or u[0] <= 0 or abs(norm + cp * cp) / max(cp * cp, abs(norm)) > 128 * EPS:
        raise ValueError('Future unit material u; no gradient-clock substitution or renormalization')
    covariant = du + np.einsum('bal,l->ab', geometry['Gamma'], u)
    down = covariant @ geometry['g']
    P = np.eye(4) + np.outer(u, cov) / (cp * cp)
    acceleration = u @ covariant
    omega = P.T @ (.5 * (down - down.T)) @ P
    strain = P.T @ (.5 * (down + down.T)) @ P
    Pcontra = geometry['inverse'] + np.outer(u, u) / (cp * cp)
    norm_derivative = np.einsum('amn,m,n->a', geometry['dg'], u, u) + 2 * (du @ cov)
    return finite_result(dict(u=u, du=du, u_cov=cov, covariant_derivative=covariant, acceleration=acceleration,
        projector=P, vorticity_cov=omega, strain_cov=strain,
        expansion=float(np.einsum('ab,ab->', Pcontra, down)), normalization_derivative=norm_derivative), 'material_kinematics')

@floating_refusal
def material_euler_residual(geometry, u, W_cov, reaction_cov, unit_multiplier):
    """Evaluate supplied COMPLETE vertices; this does not solve a flow or invent its force."""
    u = real(u, (4,), 'u'); W = real(W_cov, (4,), 'complete material vertex')
    reaction = real(reaction_cov, (4,), 'actual nonunit reactions')
    cp = geometry['cp']; cov = geometry['g'] @ u
    norm = float(u @ cov)
    if not math.isfinite(norm) or u[0] <= 0 or abs(norm + cp * cp) / max(cp * cp, abs(norm)) > 128 * EPS:
        raise ValueError('Unit material u for Euler projection')
    if not math.isfinite(unit_multiplier): raise ValueError('Finite supplied unit multiplier')
    row = W + reaction + unit_multiplier * cov
    Pcontra = geometry['inverse'] + np.outer(u, u) / (cp * cp)
    return finite_result(dict(full_cov=row, projected_contra=Pcontra @ row,
        required_unit_multiplier=float(u @ (W + reaction)) / (cp * cp)), 'material_Euler')

@floating_refusal
def dynamic_circle_residual(geometry, Omega, Omega_dot, azimuth, meridional):
    """Supplied constant-coordinate circle; no frozen-root selection or orbit integration."""
    if azimuth not in (1, 2, 3) or tuple(meridional) != tuple(i for i in (1, 2, 3) if i != azimuth):
        raise ValueError('Declared circle coordinate ordering')
    if not math.isfinite(Omega) or not math.isfinite(Omega_dot): raise ValueError('Finite supplied circle rates')
    g, dg = geometry['g'], geometry['dg']
    if np.any(dg[azimuth] != 0): raise ValueError('Axisymmetry required for circle interface')
    D = float(g[0, 0] + 2 * Omega * g[0, azimuth] + Omega * Omega * g[azimuth, azimuth])
    if not math.isfinite(D) or D >= 0: raise ValueError('Finite timelike supplied circle')
    Jc = float(g[0, azimuth] + Omega * g[azimuth, azimuth])
    dD = dg[:, 0, 0] + 2 * Omega * dg[:, 0, azimuth] + Omega * Omega * dg[:, azimuth, azimuth]
    f = -float(dD[0] + 2 * Jc * Omega_dot) / (2 * D)
    mer = np.array([dg[0, a, 0] + Omega * dg[0, a, azimuth] + g[a, azimuth] * Omega_dot
        + f * (g[a, 0] + Omega * g[a, azimuth]) - .5 * dD[a] for a in meridional])
    axial = float(dg[0, 0, azimuth] + Omega * dg[0, azimuth, azimuth]
        + g[azimuth, azimuth] * Omega_dot + f * Jc)
    return finite_result(dict(D=D, J=Jc, f=f, meridional=mer, axial=axial), 'circle')

def physical_galaxy_prediction_gate():
    raise ValueError('No registered full same-action galaxy metric/source/history/junction or physical tracer readout in this component')

def check(name, actual, expected):
    a, b = np.asarray(actual), np.asarray(expected)
    if a.shape != b.shape or a.dtype.kind not in 'fiu' or b.dtype.kind not in 'fiu': raise ValueError('Control shape/dtype: ' + name)
    delta = a.astype(float) - b.astype(float)
    scale = max(1., float(np.max(np.abs(a))) if a.size else 0., float(np.max(np.abs(b))) if b.size else 0.)
    error = float(np.max(np.abs(delta))) / scale if delta.size else 0.
    passed = bool(np.isfinite(a).all() and np.isfinite(b).all() and math.isfinite(error) and error <= TOL)
    row = dict(name=name, actual=a.copy(), expected=b.copy(), difference=delta, scale=scale, error=error, tolerance=TOL, passed=passed)
    CONTROLS.append(row); RAW.setdefault('controls', []).append(row)

def cartesian_fixture(cp):
    g = np.diag([-cp * cp, 1., 1., 1.]); dg = np.zeros((4, 4, 4)); w = cp * np.array([.1, -.04, .02])
    RAW.update(g=g, dg=dg, w=w); geo = metric_geometry(g, dg, cp); RAW['geometry'] = geo
    orbit = geodesic_rhs(geo, w); RAW['orbit'] = orbit
    check('minkowski_connection', geo['Gamma'], np.zeros((4, 4, 4)))
    check('minkowski_rhs', orbit['dw_dt'], np.zeros(3))
    check('minkowski_ADM', np.concatenate(([geo['N']], geo['beta'])), [1., 0., 0., 0.])
    check('minkowski_observer', orbit['observer']['normal_velocity'], w)
    u = orbit['observer']['dt_dproper'] * orbit['observer']['W']; kin = material_kinematics(geo, u, np.zeros((4, 4))); RAW['material'] = kin
    check('minkowski_material', np.concatenate((kin['acceleration'], kin['normalization_derivative'], kin['vorticity_cov'].ravel())), np.zeros(24))
    ray = geodesic_rhs(geo, [cp, 0., 0.], 'null'); RAW['null_ray'] = ray
    check('minkowski_null_rhs', ray['dw_dt'], np.zeros(3))

def affine_flat_fixture(cp):
    t = .25; x = np.array([.4, -.2, .3]); w = np.array([.15, -.1, .08]); s = .17
    f = .2 * t + .05 * t * t; fd = .2 + .1 * t; fdd = .1
    R = np.array([[math.cos(f), -math.sin(f), 0.], [math.sin(f), math.cos(f), 0.], [0., 0., 1.]])
    K = np.array([[0., -1., 0.], [1., 0., 0.], [0., 0., 0.]])
    S = np.eye(3); S[0, 1] = s * t; Sd = np.zeros((3, 3)); Sd[0, 1] = s
    Si = np.eye(3); Si[0, 1] = -s * t
    L = R @ S; Ld = fd * K @ R @ S + R @ Sd
    Ldd = (fdd * K @ R + fd * fd * K @ K @ R) @ S + 2 * fd * K @ R @ Sd
    Li = Si @ R.T; bd = np.array([.14 * t, -.09 * t * t, .02]); bdd = np.array([.14, -.18 * t, 0.])
    v0 = Ld @ x + bd; a0 = Ldd @ x + bdd
    g = np.zeros((4, 4)); g[0, 0] = -cp * cp + v0 @ v0; g[1:, 1:] = L.T @ L
    g[0, 1:] = g[1:, 0] = L.T @ v0; dg = np.zeros((4, 4, 4))
    dg[0, 0, 0] = 2 * v0 @ a0; dg[0, 1:, 1:] = Ld.T @ L + L.T @ Ld
    dg[0, 0, 1:] = dg[0, 1:, 0] = Ld.T @ v0 + L.T @ a0
    for k in range(3):
        dg[k + 1, 0, 0] = 2 * v0 @ Ld[:, k]
        dg[k + 1, 0, 1:] = dg[k + 1, 1:, 0] = L.T @ Ld[:, k]
    RAW.update(g=g, dg=dg, L=L, Ld=Ld, Ldd=Ldd, Li=Li, x=x, w=w, bd=bd, bdd=bdd)
    geo = metric_geometry(g, dg, cp); RAW['geometry'] = geo; orbit = geodesic_rhs(geo, w); RAW['orbit'] = orbit
    check('affine_flat_RHS', orbit['dw_dt'], -Li @ (2 * Ld @ w + a0))
    check('affine_flat_ADM', np.concatenate(([geo['N']], geo['beta'])), np.concatenate(([1.], Li @ v0)))
    check('affine_flat_observer_speed', orbit['observer']['normal_speed_squared'], float((L @ w + v0) @ (L @ w + v0)))
    compatible = dg - np.einsum('lam,ln->amn', geo['Gamma'], g) - np.einsum('lan,ml->amn', geo['Gamma'], g)
    RAW['metric_compatibility'] = compatible; check('affine_flat_metric_compatibility', compatible, np.zeros((4, 4, 4)))
    check('affine_flat_inverse', g @ geo['inverse'], np.eye(4))

def flrw_fixture(cp):
    H, Hd = .12, -.015; x = np.array([.4, -.2, .3]); w = H * x
    g = np.eye(4); g[0, 0] = -cp * cp + H * H * (x @ x); g[0, 1:] = g[1:, 0] = -H * x
    dg = np.zeros((4, 4, 4)); dg[0, 0, 0] = 2 * H * Hd * (x @ x); dg[0, 0, 1:] = dg[0, 1:, 0] = -Hd * x
    for k in range(3):
        dg[k + 1, 0, 0] = 2 * H * H * x[k]; dg[k + 1, 0, k + 1] = dg[k + 1, k + 1, 0] = -H
    u = np.concatenate(([1.], w)); du = np.zeros((4, 4)); du[0, 1:] = Hd * x; du[1:, 1:] = H * np.eye(3)
    RAW.update(g=g, dg=dg, H=H, Hdot=Hd, x=x, w=w, u=u, du=du)
    geo = metric_geometry(g, dg, cp); RAW['geometry'] = geo; orbit = geodesic_rhs(geo, w); RAW['orbit'] = orbit
    kin = material_kinematics(geo, u, du); RAW['material'] = kin
    check('FLRW_areal_comoving_RHS', orbit['dw_dt'], (Hd + H * H) * x)
    check('FLRW_areal_observer', orbit['observer']['normal_velocity'], np.zeros(3))
    check('FLRW_comoving_material_acceleration', kin['acceleration'], np.zeros(4))
    check('FLRW_comoving_vorticity', kin['vorticity_cov'], np.zeros((4, 4)))
    check('FLRW_expansion_and_unit_derivative', np.concatenate(([kin['expansion']], kin['normalization_derivative'])), [3 * H, 0., 0., 0., 0.])

def rotating_material_fixture(cp):
    R, Omega = .4, .3; v = np.array([0., Omega * R, 0.]); lorentz = 1 / math.sqrt(1 - float(v @ v) / (cp * cp))
    g = np.diag([-cp * cp, 1., 1., 1.]); dg = np.zeros((4, 4, 4)); u = lorentz * np.concatenate(([1.], v)); du = np.zeros((4, 4))
    gradgamma = np.array([lorentz**3 * Omega * Omega * R / (cp * cp), 0., 0.])
    dv = np.array([[0., Omega, 0.], [-Omega, 0., 0.], [0., 0., 0.]])
    du[1:, 0] = gradgamma; du[1:, 1:] = np.outer(gradgamma, v) + lorentz * dv
    RAW.update(g=g, dg=dg, R=R, Omega=Omega, u=u, du=du, w=v)
    geo = metric_geometry(g, dg, cp); RAW['geometry'] = geo; kin = material_kinematics(geo, u, du); RAW['material'] = kin
    expected = np.array([0., -lorentz * lorentz * Omega * Omega * R, 0., 0.])
    vertex = g @ expected; free = material_euler_residual(geo, u, vertex, np.zeros(4), 0.)
    forced = material_euler_residual(geo, u, vertex, -vertex, 0.); RAW.update(unforced_Euler=free, supported_Euler=forced)
    check('rotation_observer_velocity', normal_observer(geo, v)['normal_velocity'], v)
    check('rotation_requires_centripetal_acceleration', kin['acceleration'], expected)
    check('rotation_nonzero_vorticity', kin['vorticity_cov'][1, 2], lorentz**3 * Omega)
    check('rotation_unforced_Euler_is_not_zero', free['projected_contra'], expected)
    check('rotation_supplied_force_balance_and_unit_derivative', np.concatenate((forced['projected_contra'], kin['normalization_derivative'])), np.zeros(8))

def cylindrical_fixture(cp):
    R, Omega = .4, .3; g = np.diag([-cp * cp, 1., R * R, 1.]); dg = np.zeros((4, 4, 4)); dg[1, 2, 2] = 2 * R
    w = np.array([0., Omega, 0.]); RAW.update(g=g, dg=dg, R=R, Omega=Omega, w=w)
    geo = metric_geometry(g, dg, cp); RAW['geometry'] = geo; orbit = geodesic_rhs(geo, w); RAW['orbit'] = orbit
    circle = dynamic_circle_residual(geo, Omega, 0., 2, (1, 3)); RAW['circle'] = circle
    check('cylindrical_free_RHS_is_outward', orbit['dw_dt'], [R * Omega * Omega, 0., 0.])
    check('cylindrical_circle_is_not_free', circle['meridional'], [-R * Omega * Omega, 0.])
    check('cylindrical_axial_and_clock_rows', [circle['axial'], circle['f']], [0., 0.])
    check('cylindrical_axial_observer_speed', normal_observer(geo, w, axis=[0., 1., 0.])['axis_projection'], R * Omega)

def refusal_fixture(cp):
    g = np.diag([-cp * cp, 1., 1., 1.]); dg = np.zeros((4, 4, 4)); geo = metric_geometry(g, dg, cp)
    wrong_sign = np.diag([cp * cp, 1., 1., 1.]); wrong_h = g.copy(); wrong_h[1, 1] = -1.
    wrong_jet = dg.copy(); wrong_jet[0, 1, 2] = 1.
    huge_w = np.array([1e308, 0., 0.]); huge_u = np.array([1e308, 0., 0., 0.]); huge_du = np.full((4, 4), 1e308)
    extreme_g = g.copy(); extreme_g[0, 0] = -1e-300; extreme_jet = dg.copy(); extreme_jet[0, 0, 0] = 1e308
    tests = [('nonLorentz', lambda: metric_geometry(wrong_sign, dg, cp)), ('nonSPD_h', lambda: metric_geometry(wrong_h, dg, cp)),
        ('nonsymmetric_jet', lambda: metric_geometry(g, wrong_jet, cp)), ('spacelike_velocity', lambda: geodesic_rhs(geo, [2 * cp, 0., 0.])),
        ('nonunit_material_u', lambda: material_kinematics(geo, [2., 0., 0., 0.], np.zeros((4, 4)))),
        ('unregistered_physical_galaxy_prediction', physical_galaxy_prediction_gate),
        ('overflow_cp_squared', lambda: metric_geometry(g, dg, 1e308)),
        ('underflow_cp_squared', lambda: metric_geometry(g, dg, 1e-308)),
        ('overflow_observer_norm', lambda: normal_observer(geo, huge_w)),
        ('overflow_material_norm', lambda: material_kinematics(geo, huge_u, np.zeros((4, 4)))),
        ('overflow_material_derivative', lambda: material_kinematics(geo, [1., 0., 0., 0.], huge_du)),
        ('overflow_Christoffel', lambda: metric_geometry(extreme_g, extreme_jet, cp))]
    RAW.update(g=g, dg=dg, wrong_sign=wrong_sign, wrong_h=wrong_h, wrong_jet=wrong_jet, huge_w=huge_w,
        huge_u=huge_u, huge_du=huge_du, extreme_g=extreme_g, extreme_jet=extreme_jet,
        overflow_cp=1e308, underflow_cp=1e-308, refusals=[])
    for name, callback in tests:
        reason = None
        try: callback()
        except ValueError as exc: reason = str(exc)
        RAW['refusals'].append(dict(name=name, reason=reason)); check('refused_' + name, [int(reason is not None)], [1])

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def encoded(value):
    if np is not None and isinstance(value, np.ndarray):
        return dict(dtype=str(value.dtype), shape=list(value.shape), values=encoded(value.tolist()))
    if np is not None and isinstance(value, np.generic): return encoded(value.item())
    if isinstance(value, dict): return {str(k): encoded(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)): return [encoded(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value): return dict(nonfinite=repr(value))
    if value is None or isinstance(value, (str, bool, int, float)): return value
    raise TypeError('Unregistered serialization type: ' + type(value).__name__)

def publish(suffix, value):
    p = J / (STEM + '_' + suffix + '.json')
    raw = (json.dumps(encoded(value), sort_keys=True, indent=2, allow_nan=False) + '\n').encode()
    with p.open('xb') as f: f.write(raw); f.flush(); os.fsync(f.fileno())
    if p.read_bytes() != raw: raise RuntimeError('Publication byte reread: ' + p.name)
    p.chmod(0o444); CREATED[p.name] = sha(p)
    return CREATED[p.name]

def actual_outputs():
    result = {}
    for p in sorted(J.glob(STEM + '_*.json')):
        if not p.is_file(): raise RuntimeError('Unexpected own output: ' + p.name)
        p.chmod(0o444); result[p.name] = sha(p)
    return result

def verify(inputs):
    for name, expected in inputs.items():
        if sha(J / name) != expected: raise RuntimeError('Input/source changed: ' + name)

def main():
    global np
    ap = argparse.ArgumentParser(description=__doc__); ap.add_argument('--root-execute', action='store_true'); args = ap.parse_args()
    if AUTHOR_DRAFT or not args.root_execute: raise RuntimeError('Guarded author draft/root-only execution')
    if sys.platform != 'darwin' or Path(__file__).resolve() != J / SOURCE or not sys.dont_write_bytecode: raise RuntimeError('Root Mac/source/no-bytecode context')
    if any(p.name != PROTOCOL for p in J.glob(STEM + '*')): raise FileExistsError('Unused exclusive namespace required')
    inputs = {**PINS, PROTOCOL: PROTOCOL_SHA, SOURCE: sha(J / SOURCE)}; verify(inputs)
    owner = dict(owner='root', pid=os.getpid(), started=datetime.now(timezone.utc).isoformat(), source_sha256=inputs[SOURCE])
    try:
        publish('MANIFEST', dict(owner=owner, inputs=inputs, cp_fixture_m_s=5., trajectory_selected=False, physical_flags=FLAGS))
        import numpy as numpy_module
        np = numpy_module
        for name, callback in [('MINKOWSKI', cartesian_fixture), ('AFFINE_FLAT', affine_flat_fixture), ('FLRW', flrw_fixture),
            ('ROTATING_MATERIAL', rotating_material_fixture), ('CYLINDRICAL', cylindrical_fixture), ('REFUSALS', refusal_fixture)]:
            RAW.clear(); start = len(CONTROLS); RAW['fixture'] = name; callback(5.)
            publish('CASE_' + name, dict(owner=owner, fixture=name, available=RAW, controls=CONTROLS[start:], physical_flags=FLAGS))
        if len(CONTROLS) != 37: raise RuntimeError('Prospective thirty-seven-control census')
        passed = all(c['passed'] for c in CONTROLS)
        result = dict(owner=owner, inputs=inputs, status='KINEMATIC_COMPONENT_PASS' if passed else 'ARITHMETIC_FAILURES_RETAINED',
            controls=CONTROLS, count=37, cases=6, physical_flags=FLAGS,
            scope='Supplied full metric/jet and independent rotating material vertices only; no galaxy metric, source extension, flow solve or velocity qualification.')
        rh = publish('RESULT', result); verify(inputs)
        if actual_outputs() != CREATED: raise RuntimeError('Exact successful own output set')
        publish('RECEIPT', dict(status='CLOSED', owner=owner, closed=datetime.now(timezone.utc).isoformat(), input_sha256=inputs,
            output_sha256=dict(CREATED), result_sha256=rh, physical_flags=FLAGS))
        verify(inputs)
        if actual_outputs() != CREATED: raise RuntimeError('Postreceipt exact output set')
        print(json.dumps(dict(status=result['status'], controls=37, cases=6, result_sha256=rh)))
        return 0 if passed else 3
    except BaseException as exc:
        prior = J / (STEM + '_RECEIPT.json'); prior_ref = dict(file=prior.name, sha256=sha(prior)) if prior.exists() else None
        partials = actual_outputs()
        eh = publish('ERROR', dict(owner=owner, exception=repr(exc), traceback=traceback.format_exc(), available=RAW,
            controls=CONTROLS, prior_receipt=prior_ref, preserved_actual_outputs=partials, physical_flags=FLAGS))
        if prior_ref is None: publish('RECEIPT', dict(status='CLOSED_ERROR', owner=owner, closed=datetime.now(timezone.utc).isoformat(),
            input_sha256=inputs, output_sha256=actual_outputs(), error_sha256=eh, physical_flags=FLAGS))
        actual_outputs(); raise

if __name__ == '__main__': sys.exit(main())
