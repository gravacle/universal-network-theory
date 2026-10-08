#!/usr/bin/env python3
"""Guarded supplied-metric null-frequency/tetrad and declared reduction component."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, ast, hashlib, json, math, os, sys, traceback
AUTHOR_DRAFT = True
AUTHORING_IN_PROGRESS = False
J = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation')
SOURCE = 'cross_u_supplied_metric_photon_readout_v001.py'
STEM = 'CROSS_U_SUPPLIED_METRIC_PHOTON_READOUT_V001'
PROTOCOL = STEM + '.md'
PROTOCOL_SHA = '5b1c185b33081ab5c1654dbaac91373531610704a1005ae4c51e41613e92c545'
PINS = {
    'cross_u_full_metric_geodesic_and_rotating_material_v001.py': '53bc39888adeff33fffb13e04182fc9ee23d93233b15e0c533d02e24345137aa',
    'CROSS_U_FULL_METRIC_GEODESIC_AND_ROTATING_MATERIAL_V001.md': '971935f5307b660f8b439342f0933537f2e38c4965f02cf24190f3147f2c6bd5',
    'CROSS_U_FULL_METRIC_GEODESIC_AND_ROTATING_MATERIAL_V001_RESULT.json': 'd863ca31d73aac08ecd9b88b7c2723e197cc564294c5de6b2e5c0feb394105d5',
    'CROSS_U_FULL_METRIC_GEODESIC_AND_ROTATING_MATERIAL_V001_RECEIPT.json': '3a564c9ca721b3cf3ac48313c8d605092e0ed21ed077125b6b0b4f7a0cb245ae',
    'CROSS_U_ORDINARY_GEODESIC_AND_PHOTON_OBSERVATION_BRIDGE_AUDIT_V001.md': 'd5acb4229e79a79b4c394d162d02182973ab12284cf5155158186829a3f2c4bc',
    'CROSS_U_GENERAL_METRIC_ORBIT_AND_FLRW_TIME_DEPENDENCE_V001.md': 'b3fd1355c03ed78cb702844cb05e34accb9e51d648d89c21db1bafd47dfcef59',
    'reviewed_cross_u_supplied_metric_photon_readout_v001_313_287bb785.py': '287bb7850c1dce6c77a664f63e6e7b395fd93479cc22d0aed05c014993ee1d3d',
    'REVIEWED_CROSS_U_SUPPLIED_METRIC_PHOTON_READOUT_V001_25_6d31967e.md': '6d31967e98b9af4ef3334be3b11e8555e133a5a32a023a07f894011cbf926dd9'}
API_NAMES = ('floating_refusal', 'finite_result', 'real', 'metric_geometry', 'normal_observer', 'geodesic_rhs')
np = API = None
RAW, CONTROLS, CREATED = {}, [], {}
EPS = sys.float_info.epsilon
TOL = 2048 * EPS
FLAGS = {name: False for name in ('galaxy_metric_supplied', 'galaxy_null_path_supplied', 'emitter_flow_supplied',
    'physical_rest_line_clock_registered', 'metric_angular_area_map_supplied', 'source_history_registered',
    'FLRW_junction_solved', 'galaxy_velocity_qualified', 'observational_success_qualified')}

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(8 << 20), b''): h.update(block)
    return h.hexdigest()

def admitted_inputs():
    inputs = {**PINS, PROTOCOL: PROTOCOL_SHA, SOURCE: sha(J / SOURCE)}
    receipt = json.loads((J / 'CROSS_U_FULL_METRIC_GEODESIC_AND_ROTATING_MATERIAL_V001_RECEIPT.json').read_text())
    if receipt.get('status') != 'CLOSED' or receipt.get('result_sha256') != PINS['CROSS_U_FULL_METRIC_GEODESIC_AND_ROTATING_MATERIAL_V001_RESULT.json']:
        raise ValueError('Closed protected geometry parent required')
    if any(receipt['physical_flags'].values()): raise ValueError('Parent physical qualifications must remain false')
    for mapping in (receipt['input_sha256'], receipt['output_sha256']):
        for name, digest in mapping.items():
            if name in inputs and inputs[name] != digest: raise ValueError('Conflicting parent binding: ' + name)
            inputs[name] = digest
    if receipt['input_sha256'][PINS_SOURCE] != PINS[PINS_SOURCE]: raise ValueError('Parent executable identity')
    for name, digest in inputs.items():
        if digest is None or sha(J / name) != digest: raise ValueError('Actual complete input binding: ' + name)
    return inputs

def recheck(inputs):
    for name, digest in inputs.items():
        if sha(J / name) != digest: raise ValueError('Changed admitted input: ' + name)
    for name, digest in CREATED.items():
        if sha(J / name) != digest: raise ValueError('Changed actual published output: ' + name)
    if {p.name for p in J.glob(STEM + '_*') if p.is_file()} != set(CREATED):
        raise ValueError('Actual output prefix must equal registered published set')

PINS_SOURCE = 'cross_u_full_metric_geodesic_and_rotating_material_v001.py'

def load_geometry_api():
    """Only protected function definitions; no parent main, imports or old fixtures."""
    parent = J / 'cross_u_full_metric_geodesic_and_rotating_material_v001.py'
    assert sha(parent) == PINS[parent.name]
    tree = ast.parse(parent.read_text()); definitions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    ns = {'np': np, 'math': math, 'EPS': EPS}
    exec(compile(ast.Module(body=[definitions[name] for name in API_NAMES], type_ignores=[]), str(parent), 'exec'), ns)
    return ns

def guarded(function):
    def wrapped(*args, **kwargs):
        try:
            with np.errstate(over='raise', divide='raise', invalid='raise'):
                result = function(*args, **kwargs)
                return API['finite_result'](result, function.__name__)
        except (FloatingPointError, OverflowError, ZeroDivisionError) as exc:
            raise ValueError('Derived photon arithmetic refused in ' + function.__name__) from exc
    return wrapped

def real(value, shape, name):
    return API['real'](value, shape, name)

def clock_registration(clock):
    if not isinstance(clock, dict) or not isinstance(clock.get('identifier'), str) or not clock['identifier']:
        raise ValueError('Explicit source/detector proper-clock registration required')
    rate = clock.get('proper_rate')
    if not isinstance(rate, (int, float)) or not math.isfinite(rate) or rate <= 0:
        raise ValueError('Positive finite d tau_clock / d tau_geom')
    line = clock.get('rest_line_hz')
    if line is not None and (not isinstance(line, (int, float)) or not math.isfinite(line) or line <= 0):
        raise ValueError('Positive finite registered rest-line frequency or unknown None')
    return float(rate), None if line is None else float(line)

@guarded
def observer_frame(geometry, u, tetrad):
    """Supplied independently rotating u; rows of tetrad are spacelike contravariant axes."""
    u = real(u, (4,), 'future observer u'); e = real(tetrad, (3, 4), 'observer spatial tetrad')
    g, cp = geometry['g'], geometry['cp']; cov = g @ u; norm = float(u @ cov)
    if u[0] <= 0 or abs(norm + cp * cp) / max(cp * cp, abs(norm)) > 128 * EPS:
        raise ValueError('Supplied future proper-time unit observer; no normalization repair')
    gram = e @ g @ e.T; orthogonal = e @ cov
    if np.max(np.abs(gram - np.eye(3))) > 128 * EPS or np.max(np.abs(orthogonal)) > 128 * EPS * max(1., cp):
        raise ValueError('Supplied orthonormal spatial observer tetrad; no frame fitting')
    return dict(u=u, u_cov=cov, tetrad=e, tetrad_gram=gram, tetrad_orthogonality=orthogonal)

@guarded
def null_readout(geometry, w, k_t_contravariant, u, tetrad, clock, domain_admitted):
    """One supplied event, seconds t; k^mu=k^t(1,w), with physical phase normalization."""
    if domain_admitted is not True: raise ValueError('Actual caller domain admission required; unknown is not zero')
    if not isinstance(k_t_contravariant, (int, float)) or not math.isfinite(k_t_contravariant) or k_t_contravariant <= 0:
        raise ValueError('Finite positive future k^t required')
    rate, line = clock_registration(clock); frame = observer_frame(geometry, u, tetrad)
    ray = API['geodesic_rhs'](geometry, w, 'null'); k = float(k_t_contravariant) * ray['observer']['W']
    cov = geometry['g'] @ k; omega = -float(frame['u'] @ cov)
    if not math.isfinite(omega) or omega <= 0: raise ValueError('Positive finite -u.k at endpoint')
    nu_geom = omega / (2 * math.pi); nu_clock = nu_geom / rate
    if not math.isfinite(nu_geom) or nu_geom <= 0 or not math.isfinite(nu_clock) or nu_clock <= 0:
        raise ValueError('Finite strictly positive derived geometric and clock frequencies; no underflowed frequency')
    components = frame['tetrad'] @ cov; direction = geometry['cp'] * components / omega
    if abs(float(direction @ direction) - 1.) > 512 * EPS: raise ValueError('Supplied null ray must have unit local direction')
    return dict(k_contra=k, k_cov=cov, omega_geom=omega, nu_geom_hz=nu_geom,
        nu_clock_hz=nu_clock, clock_rate=rate, rest_line_hz=line,
        ray_direction=direction, spatial_wave_components=components, frame=frame,
        dw_dt=ray['dw_dt'], dlog_k_t_dt=ray['dlog_ut_dt'],
        dk_t_dt=float(k_t_contravariant) * ray['dlog_ut_dt'], GammaWW=ray['GammaWW'])

@guarded
def endpoint_ratio(emission, detection):
    """Two endpoints of the SAME caller-provided ray; no endpoint/path fabrication."""
    line = emission['rest_line_hz']
    if line is None: raise ValueError('Emission transition/rest-line Hamiltonian registration missing')
    if abs(emission['nu_clock_hz'] - line) / max(line, emission['nu_clock_hz']) > TOL:
        raise ValueError('Supplied initial phase must actually satisfy registered emitted rest line')
    ratio = emission['omega_geom'] / detection['omega_geom']
    clock_ratio = emission['nu_clock_hz'] / detection['nu_clock_hz']
    return dict(one_plus_z_geometric=ratio, one_plus_z_clock=clock_ratio,
        observed_to_emitted_restline=detection['nu_clock_hz'] / line)

@guarded
def local_doppler_pair(geometry, readout, emitter_u):
    """Independent same-event -u.k and exact local-frame Doppler identity."""
    ue = real(emitter_u, (4,), 'emitter u'); cp, g = geometry['cp'], geometry['g']
    ecov = g @ ue; norm = float(ue @ ecov)
    if ue[0] <= 0 or abs(norm + cp * cp) / max(cp * cp, abs(norm)) > 128 * EPS:
        raise ValueError('Supplied independently normalized future emitter')
    gamma = -float(readout['frame']['u'] @ ecov) / (cp * cp)
    if gamma < 1. - 128 * EPS: raise ValueError('Future observer/emitter Lorentz pairing')
    velocity = (readout['frame']['tetrad'] @ ecov) / gamma
    omega = -float(ue @ readout['k_cov'])
    expected = gamma * readout['omega_geom'] * (1 - float(velocity @ readout['ray_direction']) / cp)
    if omega <= 0 or float(velocity @ velocity) >= cp * cp: raise ValueError('Timelike local emitter and positive frequency')
    return dict(omega_emitter=omega, omega_local_formula=expected, emitter_gamma=gamma, emitter_velocity=velocity)

@guarded
def velocity_convention(observed_to_restline, cp, convention):
    """Declared spectral-reduction convention; this is not a metric orbital velocity."""
    r = float(observed_to_restline)
    if not math.isfinite(r) or r <= 0 or not math.isfinite(cp) or cp <= 0: raise ValueError('Positive finite spectral ratio and cp')
    if convention == 'optical': value = cp * (1 / r - 1)
    elif convention == 'radio': value = cp * (1 - r)
    elif convention == 'relativistic': value = cp * (1 - r * r) / (1 + r * r)
    else: raise ValueError('Explicit optical, radio or relativistic convention required')
    return dict(reduction_velocity=value)

@guarded
def conventional_disk_projection(ray_direction, sky_axes, distance, inclination, disk_velocity):
    """Declared catalogue/tilted-ring geometry ONLY; no metric distance or area derivation."""
    n = real(ray_direction, (3,), 'local propagation direction'); axes = real(sky_axes, (3, 3), 'fixed sky right/up/forward axes')
    if abs(float(n @ n) - 1) > 128 * EPS or np.max(np.abs(axes @ axes.T - np.eye(3))) > 128 * EPS:
        raise ValueError('Supplied unit ray and fixed orthonormal sky axes')
    if not math.isfinite(distance) or distance <= 0 or not math.isfinite(inclination) or not 0 <= inclination < math.pi / 2:
        raise ValueError('Declared positive distance and nonedge-on fixed inclination')
    look = axes @ (-n)
    if look[2] <= 0: raise ValueError('Source must lie in declared forward sky hemisphere')
    X, Y = distance * look[:2] / look[2]; yd = Y / math.cos(inclination)
    radius = math.hypot(X, yd); theta = math.atan2(yd, X)
    vr, vR, vZ = real(disk_velocity, (3,), 'supplied disk rotation/radial/vertical components')
    los = math.sin(inclination) * (vr * math.cos(theta) + vR * math.sin(theta)) + vZ * math.cos(inclination)
    return dict(sky_look=look, projected_X=X, projected_Y=Y, conventional_disk_radius=radius,
        conventional_disk_theta=theta, declared_LOS_velocity=los)

def physical_galaxy_prediction_gate():
    raise ValueError('No supplied full galaxy metric/exterior/ray bundle, emitting flow, rest line, detector clock or raw sky data; no physical prediction')

def check(name, actual, expected):
    a, b = np.asarray(actual), np.asarray(expected)
    if a.shape != b.shape or a.dtype.kind not in 'fiu' or b.dtype.kind not in 'fiu': raise ValueError('Control shape/type: ' + name)
    delta = a.astype(float) - b.astype(float); scale = max(1., float(np.max(np.abs(a))) if a.size else 0., float(np.max(np.abs(b))) if b.size else 0.)
    error = float(np.max(np.abs(delta))) / scale if delta.size else 0.
    passed = bool(np.isfinite(a).all() and np.isfinite(b).all() and math.isfinite(error) and error <= TOL)
    row = dict(name=name, actual=a.copy(), expected=b.copy(), difference=delta, scale=scale, error=error, tolerance=TOL, passed=passed)
    CONTROLS.append(row); RAW.setdefault('controls', []).append(row)

def remember(name, value):
    RAW[name] = value
    return value

def clock(name, rate=1., line=None):
    return dict(identifier='ARTIFICIAL_' + name, proper_rate=rate, rest_line_hz=line)

def flat_fixture(cp):
    g = remember('flat_g', np.diag([-cp * cp, 1., 1., 1.])); dg = remember('flat_dg', np.zeros((4, 4, 4)))
    geo = remember('flat_geometry', API['metric_geometry'](g, dg, cp)); e = np.column_stack((np.zeros(3), np.eye(3)))
    base = remember('flat_readout', null_readout(geo, [cp, 0., 0.], 1., [1., 0., 0., 0.], e, clock('flat'), True))
    speed = cp / 5; gamma = 5 / math.sqrt(24); ue = gamma * np.array([1., speed, 0., 0.])
    dop = remember('flat_doppler', local_doppler_pair(geo, base, ue))
    check('flat_frequency', base['omega_geom'], cp * cp)
    check('flat_ray_direction', base['ray_direction'], [1., 0., 0.])
    check('flat_boosted_emitter', [dop['omega_emitter'], dop['omega_local_formula']], [cp * cp * 4 / math.sqrt(24)] * 2)
    check('flat_frequency_transport', np.concatenate((base['dw_dt'], [base['dlog_k_t_dt']])), np.zeros(4))
    return geo, base, e

def static_lapse_fixture(cp):
    out = []
    for label, N in (('em', 2.), ('obs', 3.)):
        slope, K = .07, 1.5; g = np.diag([-cp * cp * N * N, 1., 1., 1.]); dg = np.zeros((4, 4, 4)); dg[1, 0, 0] = -2 * cp * cp * N * slope
        remember('static_' + label + '_input', dict(g=g, dg=dg, N=N, slope=slope, K=K)); geo = remember('static_' + label + '_geometry', API['metric_geometry'](g, dg, cp))
        rate = 2. if label == 'em' else 3.; line = cp * cp * K / (N * 2 * math.pi * rate) if label == 'em' else None
        out.append(remember('static_' + label + '_readout', null_readout(geo, [cp * N, 0., 0.], K / (N * N), [1 / N, 0., 0., 0.], np.column_stack((np.zeros(3), np.eye(3))), clock(label, rate, line), True)))
    ratios = remember('static_ratios', endpoint_ratio(*out))
    check('static_Killing_frequency', [out[0]['omega_geom'], out[1]['omega_geom']], [cp * cp * 1.5 / 2, cp * cp * 1.5 / 3])
    check('static_gravitational_redshift', ratios['one_plus_z_geometric'], 3 / 2)
    check('registered_clock_ratio', ratios['one_plus_z_clock'], 9 / 4)
    check('static_null_transport', [out[0]['dw_dt'][0], out[0]['dlog_k_t_dt']], [cp * cp * 2 * .07, -2 * cp * .07])

def flrw_fixture(cp):
    out = []
    for label, a, H in (('em', 2., .12), ('obs', 3., .08)):
        g = np.diag([-cp * cp, a * a, a * a, a * a]); dg = np.zeros((4, 4, 4)); dg[0, 1:, 1:] = 2 * a * a * H * np.eye(3)
        remember('FLRW_' + label + '_input', dict(g=g, dg=dg, a=a, H=H)); geo = remember('FLRW_' + label + '_geometry', API['metric_geometry'](g, dg, cp))
        line = cp * cp / (a * 2 * math.pi) if label == 'em' else None
        out.append(remember('FLRW_' + label + '_readout', null_readout(geo, [cp / a, 0., 0.], 1 / a, [1., 0., 0., 0.], np.column_stack((np.zeros(3), np.eye(3) / a)), clock(label, line=line), True)))
    ratio = remember('FLRW_ratio', endpoint_ratio(*out))
    check('FLRW_endpoint_frequency', [r['omega_geom'] for r in out], [cp * cp / 2, cp * cp / 3])
    check('FLRW_redshift', ratio['one_plus_z_geometric'], 3 / 2)
    check('FLRW_frequency_transport', [out[0]['dlog_k_t_dt'], out[1]['dlog_k_t_dt']], [-.12, -.08])
    check('FLRW_coordinate_ray_RHS', out[0]['dw_dt'], [-.12 * cp / 2, 0., 0.])

def rotating_fixture(cp):
    R, Omega = .4, .3; g = np.diag([-cp * cp + R * R * Omega * Omega, 1., R * R, 1.]); g[0, 2] = g[2, 0] = R * R * Omega
    dg = np.zeros((4, 4, 4)); dg[1, 0, 0] = 2 * R * Omega * Omega; dg[1, 0, 2] = dg[1, 2, 0] = 2 * R * Omega; dg[1, 2, 2] = 2 * R
    remember('rotating_input', dict(g=g, dg=dg, R=R, Omega=Omega)); geo = remember('rotating_geometry', API['metric_geometry'](g, dg, cp))
    e = np.array([[0., 1., 0., 0.], [0., 0., 1 / R, 0.], [0., 0., 0., 1.]])
    ray = remember('rotating_readout', null_readout(geo, [3 * cp / 5, 4 * cp / (5 * R) - Omega, 0.], 1., [1., 0., -Omega, 0.], e, clock('rotating'), True))
    gamma = 1 / math.sqrt(1 - 1 / 20); ue = gamma * np.array([1., cp / 5, -cp / (10 * R) - Omega, 0.]); dop = remember('rotating_doppler', local_doppler_pair(geo, ray, ue))
    check('rotating_coordinate_frequency_invariance', ray['omega_geom'], cp * cp)
    check('rotating_coordinate_direction_invariance', ray['ray_direction'], [3 / 5, 4 / 5, 0.])
    check('rotating_coordinate_doppler_invariance', [dop['omega_emitter'], dop['omega_local_formula']], [gamma * cp * cp * 24 / 25] * 2)
    check('rotating_null_RHS_and_frequency', np.concatenate((ray['dw_dt'], [ray['dlog_k_t_dt']])), [16 * cp * cp / (25 * R), -24 * cp * cp / (25 * R * R), 0., 0.])

def reduction_fixture(cp):
    look = np.array([.03, .02, 1.]); n = -look / math.sqrt(float(look @ look))
    projected = remember('reduction_geometry', conventional_disk_projection(n, np.eye(3), 10., math.pi / 3, [.2 * cp, .1 * cp, .05 * cp]))
    check('declared_distance_inclination_projection', [projected['conventional_disk_radius'], projected['conventional_disk_theta']], [.5, math.atan2(.4, .3)])
    check('declared_tilted_ring_LOS', projected['declared_LOS_velocity'], cp * (math.sqrt(3) / 10 + 1 / 40))
    values = [velocity_convention(4 / 5, cp, name)['reduction_velocity'] for name in ('optical', 'radio', 'relativistic')]
    remember('reduction_conventions', values); check('three_explicit_spectral_conventions', values, [cp / 4, cp / 5, 9 * cp / 41])

def refusal_fixture(geo, base, e):
    bad = e.copy(); bad[0, 1] = 2.
    cases = [('negative_future_k_t', lambda: null_readout(geo, [geo['cp'], 0., 0.], -1., [1., 0., 0., 0.], e, clock('bad'), True)),
        ('nonunit_endpoint_u', lambda: observer_frame(geo, [2., 0., 0., 0.], e)),
        ('nonorthonormal_endpoint_tetrad', lambda: observer_frame(geo, [1., 0., 0., 0.], bad)),
        ('missing_clock_registration', lambda: null_readout(geo, [geo['cp'], 0., 0.], 1., [1., 0., 0., 0.], e, None, True)),
        ('physical_galaxy_scope_refusal', physical_galaxy_prediction_gate)]
    for name, fn in cases:
        rejected = False
        try: fn()
        except ValueError as exc: remember('refusal_' + name, str(exc)); rejected = True
        check(name, int(rejected), 1)

def jsonable(value):
    if isinstance(value, dict): return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)): return [jsonable(v) for v in value]
    if np is not None and isinstance(value, np.ndarray): return jsonable(value.tolist())
    if np is not None and isinstance(value, np.generic): return jsonable(value.item())
    if isinstance(value, float) and not math.isfinite(value): return {'unqualified_nonfinite': value.hex()}
    return value

def publish(name, value):
    path = J / name; data = (json.dumps(jsonable(value), sort_keys=True, indent=2, allow_nan=False) + '\n').encode()
    with path.open('xb') as f: f.write(data); f.flush(); os.fsync(f.fileno())
    if path.read_bytes() != data: raise ValueError('Exact publication byte reread failed')
    path.chmod(0o444); CREATED[name] = sha(path)

def freeze_actual():
    for path in J.glob(STEM + '_*'):
        if path.is_file(): path.chmod(0o444); CREATED[path.name] = sha(path)

def main():
    global np, API
    parser = argparse.ArgumentParser(); parser.add_argument('--run-controls', action='store_true'); args = parser.parse_args()
    if AUTHOR_DRAFT or AUTHORING_IN_PROGRESS or not args.run_controls: raise SystemExit('Guarded component; root release and --run-controls required')
    started = datetime.now(timezone.utc).isoformat(); receipt_name = STEM + '_RECEIPT.json'
    try:
        if any(J.glob(STEM + '_*')): raise ValueError('Exclusive unused output namespace required')
        if PROTOCOL_SHA is None: raise ValueError('Unbound reviewed protocol')
        inputs = admitted_inputs()
        import numpy as numpy
        np = numpy; API = load_geometry_api()
        publish(STEM + '_MANIFEST.json', dict(inputs=inputs, flags=FLAGS, owner_pid=os.getpid(), started=started,
            chart='seconds t; supplied g_tt contains cp squared', new_cases=5, expected_controls=24, old_fixture_replay=False))
        geo, base, e = flat_fixture(3.); static_lapse_fixture(3.); flrw_fixture(3.); rotating_fixture(3.); reduction_fixture(3.); refusal_fixture(geo, base, e)
        if len(CONTROLS) != 24 or not all(c['passed'] for c in CONTROLS): raise ValueError('Original finite analytic control gates failed')
        publish(STEM + '_RESULT.json', dict(status='SUPPLIED_METRIC_COMPONENT_ARITHMETIC_PASS', controls=CONTROLS,
            cases=5, raw=RAW, inputs=inputs, flags=FLAGS, metric_angular_area_map=None,
            actual_galaxy_ray_or_velocity=None, source_additions='PAUSED'))
        recheck(inputs)
        publish(receipt_name, dict(status='CLOSED', outcome='SUPPLIED_METRIC_COMPONENT_ARITHMETIC_PASS', owner_pid=os.getpid(),
            started=started, closed=datetime.now(timezone.utc).isoformat(), inputs=inputs, outputs=dict(CREATED), flags=FLAGS))
        recheck(inputs)
        print(json.dumps(dict(status='SUPPLIED_METRIC_COMPONENT_ARITHMETIC_PASS', controls=len(CONTROLS), cases=5, flags=FLAGS)))
    except BaseException as exc:
        error = dict(exception_type=type(exc).__name__, message=str(exc), traceback=traceback.format_exc(), raw=RAW,
            controls=CONTROLS, flags=FLAGS, owner_pid=os.getpid(), started=started, unknown_physical_inputs_remain_unknown=True)
        freeze_actual(); prior = J / receipt_name
        error['prior_receipt_sha256'] = sha(prior) if prior.exists() else None
        try: publish(STEM + '_ERROR_RAW.json', error)
        except BaseException as raw_error:
            freeze_actual(); print(json.dumps(dict(raw_publication_failure=repr(raw_error), actual_files=CREATED)), file=sys.stderr)
        freeze_actual()
        if not prior.exists():
            publish(receipt_name, dict(status='CLOSED_ERROR', outcome='IMPLEMENTATION_FAILURE_RETAINED', owner_pid=os.getpid(),
                started=started, closed=datetime.now(timezone.utc).isoformat(), outputs=dict(CREATED), flags=FLAGS))
        raise

if __name__ == '__main__': main()
