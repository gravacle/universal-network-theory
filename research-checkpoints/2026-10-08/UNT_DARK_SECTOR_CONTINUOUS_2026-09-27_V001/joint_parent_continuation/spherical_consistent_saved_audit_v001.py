"""Inert saved-state audit; no trajectory, RHS, old main or producer rerun.

Dense quotient-rule reconstruction is distinct arithmetic from the producer's
tridiagonal/factored kernel. This auditor shares the producer's author; it is
not an independently authored replication and still needs independent review.
Fixed execution pins bind the completed V002 receipts and fail on changes.
"""
import base64
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import resource
import signal
import struct
import sys
import tempfile
import time

ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J = ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
THIS = J/'spherical_consistent_saved_audit_v001.py'
PROTOCOL = J/'SPHERICAL_CONSISTENT_SAVED_AUDIT_PROTOCOL_V001.md'
INTENT = J/'SPHERICAL_CONSISTENT_SAVED_AUDIT_V001_INTENT.json'
OUT = J/'SPHERICAL_CONSISTENT_SAVED_AUDIT_V001_RESULTS.json'
FROZEN = J/'SPHERICAL_CONSISTENT_TWO_CURRENT_V002_FROZEN.json'
PINS = {
    FROZEN.name: '319322787bda24ca11b842c35f74d65a5dbca15f0d0b5eb351e0d71955f0d9d5',
    'SPHERICAL_CONSISTENT_TWO_CURRENT_SUPERVISOR_V002_FROZEN.json': '1591736f2714a63d2f082a90d5b447f1b1da88ccd9ef5c47b44f36bdbfce6c5d',
    'SPHERICAL_CONSISTENT_TWO_CURRENT_V002_FREEZE_RUN.json': '31d54e2c77167b12929bfd03e0ba7f3c3c83657b06d7e840cec84c898046e3e0',
    'SPHERICAL_CONSISTENT_TWO_CURRENT_V002_CASE_000.json': '5c77c9463ca5e2bff408bf71197d4ce19ca7fc3e931bec498a70b869e429c607',
    'SPHERICAL_CONSISTENT_TWO_CURRENT_V002_CASE_001.json': '5904e43e52c20663b4013821372a058e72a888fcdce60db1a1380e0c50f1acbd',
    'SPHERICAL_CONSISTENT_TWO_CURRENT_V002_CASE_000_RUN.json': '2bf68d2670ba89c5cbf80c8c485bb52dbde683a9ab068244b2346e471095894b',
    'SPHERICAL_CONSISTENT_TWO_CURRENT_V002_CASE_001_RUN.json': 'eb810e99c90c393b03dea67746717002a6c7a95c10a2698ba3cf593a57b3cd9b',
    'SPHERICAL_CONSISTENT_TWO_CURRENT_V002_SERIAL_RESULT.json': 'e4e0c44e73c0dd10f6d80b8946391dc3a97d50e308c973a52666c654b303c559',
    'spherical_consistent_two_current_v002.py': 'add34988868ec848d14350a63fc1b6061f62b99fb4042508cdf6415b840cfed5',
    'spherical_exact_kinetic_v001.py': '78765ef0e2d29c044642b1d944682a81ff5d48b22de9d0cb16b7bc47b9c7e11a',
    'spherical_consistent_state_maps_v001.py': '483ebdcb7fc66532911d6a9eac0eece4e29c3fff2eef063dd397ea31193e2dc4',
    'spherical_two_current_v001.py': '0349740de7d0b4173f634eaf8fd52c7e5eb4ea9ea196f95a5b882024f6dd95df',
}
CASES = [dict(case_index=i, gap=gap, L=8., dx=1/16, cells=128) for i, gap in enumerate((128, 8192))]
METHODS = ('RK4_h', 'RK4_h2', 'RK4_h4', 'DOPRI54', 'PRESSURE_OFF_RK4_h4')
TIMES = [0., 1/64, 1/32, 1/16]
CONFIG = dict(arithmetic=2e-11, material=2e-10, state=2e-8, readout=2e-7,
              compare_reference='RK4_h4', expected_complete_states=40,
              expected_fine_snapshots=8, same_author_as_producer=True)
LIMITS = dict(wall_seconds=90, cpu_soft_seconds=85, cpu_hard_seconds=90,
              self_rss_bytes=536870912, input_file_bytes=67108864,
              output_bytes=16777216, maximum_inputs=220)
THREAD_KEYS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
               'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS')


class Stop(RuntimeError):
    pass


def need(condition, message):
    if not condition:
        raise Stop(message)


def safe(value):
    if isinstance(value, float) and not math.isfinite(value):
        return dict(nonfinite=repr(value), binary64_hex=struct.pack('>d', value).hex())
    if isinstance(value, dict):
        return {str(k):safe(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [safe(v) for v in value]
    return value


def enc(value):
    return json.dumps(safe(value), sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    path.relative_to(ROOT)
    need('..' not in path.parts, 'Parent traversal refused')
    for p in (path, *path.parents):
        if p == ROOT.parent:
            break
        need(not p.is_symlink(), 'Linked input refused')
    need(path.resolve(strict=True) == path, 'Input ancestry differs')
    need(path.stat().st_size <= LIMITS['input_file_bytes'], 'Input size limit')
    return path.read_bytes()


def pin(path, expected=None):
    raw = read(path)
    need(expected is None or sha(raw) == expected, 'Changed input '+str(path))
    inputs[str(path)] = dict(sha256=sha(raw), bytes=len(raw))
    need(len(inputs) <= LIMITS['maximum_inputs'], 'Input census bound')
    return raw


def publish(path, value):
    need(path in (INTENT, OUT) and not path.exists() and not path.is_symlink(), 'Exclusive fixed output required')
    need(J.resolve(strict=True) == J, 'Output ancestry differs')
    raw = enc(value)+b'\n'
    need(len(raw) <= LIMITS['output_bytes'], 'Output byte bound')
    fd, name = tempfile.mkstemp(prefix=path.name+'.pending.', dir=J)
    with os.fdopen(fd, 'wb') as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    os.link(name, path)
    fd = os.open(J, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    Path(name).unlink()


def guard():
    need(time.monotonic()-started < LIMITS['wall_seconds'], 'Wall resource bound')
    need(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss <= LIMITS['self_rss_bytes'], 'RSS resource bound')


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check(name, actual, expected=0., tolerance=None, scale=None):
    a, b = np.asarray(actual), np.asarray(expected)
    if scale is None:
        scale = np.maximum(1., np.maximum(abs(a), abs(b)))
    error = abs(a-b)/np.maximum(abs(scale), 1e-300)
    finite = np.isfinite(error); maximum = float(np.max(error[finite])) if np.any(finite) else None
    tolerance = CONFIG['arithmetic'] if tolerance is None else tolerance
    passed = bool(np.all(finite) and maximum is not None and maximum <= tolerance)
    row = dict(name=name, count=int(error.size), maximum_normalized_error=maximum,
               nonfinite_entries=int(np.count_nonzero(~finite)), tolerance=tolerance, passed=passed)
    checks.append(row)
    return row


def dense_inertia_and_derivative(x, mass, direction=None):
    """Independent polynomial quotient assembly, no kernel/maps call.

    Use N' S - 3N S' rather than the producer's simplified derivative or
    factored quadratic force. Origin has one constant 3m/5 free entry.
    """
    x = np.asarray(x, dtype=float); mass = np.asarray(mass, dtype=float); n = len(mass)
    need(x.shape == (n+1,) and x[0] == 0. and np.all(np.diff(x) > 0.) and np.all(mass > 0.), 'Invalid audit mesh/masses')
    M = np.zeros((n, n)); M[0, 0] = 3*mass[0]/5
    Md = np.zeros_like(M); blocks = []
    if direction is not None:
        direction = np.r_[0., np.asarray(direction, dtype=float)]
        need(direction.shape == x.shape, 'Invalid directional vector')
    for j in range(1, n):
        q = x[j]/x[j+1]; S = 1+q+q*q; Sp = 1+2*q
        Ns = (5*q**3+6*q**4+3*q**5+q**6, q*q+3*q**3+q**4, 1+3*q+6*q*q+5*q**3)
        Ds = (15*q*q+24*q**3+15*q**4+6*q**5, 2*q+9*q*q+4*q**3, 3+12*q+15*q*q)
        coefficients = (3/5, 9/10, 3/5)
        F = [c*N/S**3 for c, N in zip(coefficients, Ns)]
        D = [c*(Np*S-3*N*Sp)/S**4 for c, N, Np in zip(coefficients, Ns, Ds)]
        block = np.array([[F[0], F[1]], [F[1], F[2]]])*mass[j]
        deriv = np.array([[D[0], D[1]], [D[1], D[2]]])*mass[j]
        M[j-1:j+1, j-1:j+1] += block
        blocks.append((j, q, deriv))
        if direction is not None:
            dq = (direction[j]-q*direction[j+1])/x[j+1]
            Md[j-1:j+1, j-1:j+1] += deriv*dq
    need(np.all(np.isfinite(M)) and np.all(np.isfinite(Md)), 'Nonfinite dense reconstruction')
    return M, Md, blocks


def reconstruct(model, tau, y, pressure):
    """Reuse authenticated material/force read; reconstruct inertia independently."""
    guard(); y = np.asarray(y, dtype=float)
    need(y.shape == (model.nstate,) and np.all(np.isfinite(y)), 'Invalid raw canonical state')
    o = model.read(tau, y); A = float(y[0]); n = model.N; items = []; chart = y.copy()
    pk = 4*math.pi*o['meshes'][1][1:]**2*(o['P']-np.r_[o['P'][1:], o['Pbar']])
    for s in range(2):
        offset = 1+2*n*s; x = np.r_[0., y[offset:offset+n]]; p = y[offset+n:offset+2*n]
        M, _, blocks = dense_inertia_and_derivative(x, model.masses[s])
        v = np.linalg.solve(M, p/A); xd = v/A; g = np.zeros(n)
        for j, q, deriv in blocks:
            local = v[j-1:j+1]
            left = .5*float(local@deriv@local)/x[j+1]
            g[j-1] += left; g[j] -= q*left
        _, Mdot, _ = dense_inertia_and_derivative(x, model.masses[s], xd)
        fg = -o['gradW0'][s]/A
        fp = pk if s == 1 and pressure else np.zeros(n)
        a_gravity = np.linalg.solve(M, fg)/A
        a_pressure = np.linalg.solve(M, fp)/A
        a_geometry = np.linalg.solve(M, g)/A
        a_motion = -np.linalg.solve(M, Mdot@v)
        a_hubble = -o['Ht']*v
        a_full = a_gravity+a_pressure+a_geometry+a_motion+a_hubble
        K = .5*float(v@M@v); mt = float(np.sum(model.masses[s]))
        chart[offset+n:offset+2*n] = v
        half_dot = .5*float(v@Mdot@v)
        kinetic_chain = float(xd@(fg+fp+g))-half_dot-2*o['Ht']*K
        physical_work = float(xd@(fg+fp))-2*o['Ht']*K
        items.append(dict(M=M, Mdot=Mdot, v=v, xd=xd, p=p, g=g, K=K, mass=model.masses[s],
            acceleration=dict(gravity=a_gravity, pressure=a_pressure, geometry=a_geometry,
                              motion=a_motion, hubble=a_hubble, full=a_full),
            kinetic_chain=kinetic_chain, physical_work=physical_work, total_mass=mt,
            half_Mdot=half_dot, geometric_work=float(xd@g)))
    chart[1+4*n+7:] /= float(np.sum(model.masses[1]))
    return dict(raw=y, read=o, species=items, chart=chart)


def check_reconstruction(label, reconstruction):
    o = reconstruction['read']
    for s, item in enumerate(reconstruction['species']):
        tag = label+'/species'+str(s); mt = item['total_mass']; live = o['kinematics'][s]
        check(tag+'/dense_vs_tridiagonal_diagonal', np.diag(item['M'])/mt, live['diagonal']/mt)
        check(tag+'/dense_vs_tridiagonal_off', np.diag(item['M'], 1)/mt, live['off_diagonal']/mt)
        check(tag+'/velocity', item['v'], o['velocities'][s])
        check(tag+'/geometric_force_per_mass', item['g']/mt, live['geometric_force']/mt)
        check(tag+'/kinetic_per_mass', item['K']/mt, o['K_species'][s]/mt)
        check(tag+'/geometric_work_per_mass', item['half_Mdot']/mt, item['geometric_work']/mt)
        check(tag+'/kinetic_work_per_mass', item['kinetic_chain']/mt, item['physical_work']/mt)


def check_fine_snapshot(label, row, saved):
    o = row['read']; check(label+'/A', saved['A'], o['A'])
    for key in ('K', 'U', 'Ubar', 'W'):
        expected = sum(s['K'] for s in row['species']) if key == 'K' else o[key]
        check(label+'/'+key, saved[key], expected)
    check(label+'/action_ratio', saved['action_ratio'], o['action_ratio'])
    check(label+'/ledger', saved['ledger'], row['raw'][-10:])
    check(label+'/hard_pressure', saved['hard_pressure_dimensionless'], o['P'])
    check(label+'/background_pressure', saved['background_pressure'], o['Pbar'])
    for key in ('e', 'p', 'omega', 'cI2', 'dE', 'dW'):
        expected = o['hard'][key]
        check(label+'/material_'+key, saved['hard_material'][key], expected, CONFIG['material'],
              np.maximum(abs(expected), 1e-300))
    for s, name in enumerate(('baryon', 'hard')):
        item = row['species'][s]; saved_species = saved['species'][name]; tag = label+'/'+name
        check(tag+'/faces', saved_species['faces'], o['meshes'][s])
        check(tag+'/velocity', saved_species['peculiar_v_over_vdyn'], item['v'])
        check(tag+'/momentum', saved_species['canonical_momentum'], item['p'])
        check(tag+'/mass', np.asarray(saved_species['cell_masses_over_M'])/item['total_mass'],
              item['mass']/item['total_mass'])
        check(tag+'/saved_inertia_diagonal', np.asarray(saved_species['inertia_diagonal'])/item['total_mass'], np.diag(item['M'])/item['total_mass'])
        check(tag+'/saved_inertia_off', np.asarray(saved_species['inertia_off_diagonal'])/item['total_mass'], np.diag(item['M'], 1)/item['total_mass'])
        check(tag+'/saved_kinetic', saved['K_species'][s]/item['total_mass'], item['K']/item['total_mass'])
        check(tag+'/volume_ratio', saved_species['volume_ratio'], o['volume_ratios'][s])
        check(tag+'/density', saved_species['comoving_density'], o['q'][s], scale=np.maximum(abs(o['q'][s]), 1e-300))
        check(tag+'/geometric_kick', np.asarray(saved_species['geometric_canonical_kick'])/item['total_mass'], item['g']/item['total_mass'])
        acc = saved_species['acceleration_decomposition']; independent = item['acceleration']
        check(tag+'/gravity', saved_species['gravity_acceleration_over_gstar'], independent['gravity'])
        check(tag+'/gravity_component', acc['physical_force_responses']['gravity'], independent['gravity'])
        check(tag+'/geometry_response', acc['geometric_kick_response'], independent['geometry'])
        check(tag+'/inertia_motion', acc['inertia_motion_response'], independent['motion'])
        check(tag+'/hubble', acc['hubble_response'], independent['hubble'])
        check(tag+'/full_peculiar_vdot', acc['full_peculiar_acceleration'], independent['full'])
        check(tag+'/Mdot_diagonal', np.asarray(acc['inertia_time_derivative_diagonal'])/item['total_mass'], np.diag(item['Mdot'])/item['total_mass'])
        check(tag+'/Mdot_off', np.asarray(acc['inertia_time_derivative_off_diagonal'])/item['total_mass'], np.diag(item['Mdot'], 1)/item['total_mass'])
        if s == 1:
            check(tag+'/pressure', acc['physical_force_responses']['pressure'], independent['pressure'])


def work_checks(label, row, initial):
    o = row['read']; oi = initial['read']; L = row['raw'][-10:]
    K = [s['K'] for s in row['species']]; Ki = [s['K'] for s in initial['species']]
    check(label+'/total_energy', sum(K)+o['U']+o['W']-sum(Ki)-oi['U']-oi['W'], L[4], CONFIG['readout'])
    check(label+'/mechanical_energy', sum(K)+o['U']-sum(Ki)-oi['U'], sum(L[:3]), CONFIG['readout'])
    mt = row['species'][1]['total_mass']
    check(label+'/hard_energy_per_mass', (K[1]+o['U']-Ki[1]-oi['U'])/mt, L[9]/mt, CONFIG['readout'])
    check(label+'/ordinary_energy', K[0]-Ki[0], L[0]-L[7]+L[2]-L[8], CONFIG['readout'])


def audit_case(index, frozen):
    path = J/('SPHERICAL_CONSISTENT_TWO_CURRENT_V002_CASE_'+format(index, '03d')+'.json')
    raw = read(path); wrapper = json.loads(raw); payload = wrapper['payload']
    need(wrapper['freeze_sha256'] == PINS[FROZEN.name] and wrapper['payload_sha256'] == sha(enc(payload)), 'Saved case binding differs')
    need(payload['case'] == CASES[index], 'Saved case census differs')
    receipt_path = path.with_name(path.stem+'_RUN.json')
    receipt = json.loads(read(receipt_path)); invocation = receipt['payload']['invocation']
    need(receipt['freeze_sha256'] == PINS['SPHERICAL_CONSISTENT_TWO_CURRENT_SUPERVISOR_V002_FROZEN.json']
         and receipt['payload_sha256'] == sha(enc(receipt['payload']))
         and receipt['payload']['case'] == CASES[index], 'Invocation receipt binding differs')
    need(invocation['stdout_sha256'] == sha(raw) and invocation['stdout_bytes'] == len(raw)
         and base64.b64decode(invocation['stdout_base64'], validate=True) == raw, 'Raw capture binding differs')
    invocation_complete = (invocation['returncode'] == 0 and invocation['exception'] is None
                           and invocation['stop_reason'] is None and not invocation['resource_monitor_errors'])
    report = dict(case=CASES[index], producer_status=payload['status'], producer_failures=payload.get('failures'),
                  producer_complete=(payload['status'] == 'COMPLETE_EXPLORATORY_NUMERICAL_CASE'
                                     and not payload.get('failures') and payload.get('custody_end_verified') is True
                                     and invocation_complete),
                  invocation_complete=invocation_complete,
                  invocation_stop_reason=invocation['stop_reason'],
                  producer_failure_snapshot=payload.get('failure_snapshot'), methods={}, snapshots_checked=0,
                  signed_pressure_on_off=[], incomplete_methods=[], errors=[])
    reports.append(report)
    need(payload['scope'] == frozen['scope'] and all(value is False for value in payload['scope'].values())
         and payload['mandatory_lanes_open'] == 11,
         'Saved qualification scope differs')
    Model = producer.make_model_class(old, kernel, maps)
    model = Model(CASES[index], shadow, certificate); rows = {}
    for name in METHODS:
        journal = payload.get('journals', {}).get(name)
        if journal is None:
            report['incomplete_methods'].append(dict(method=name, reason='ABSENT')); continue
        saved = journal.get('samples', [])
        report['methods'][name] = dict(producer_status=journal['status'], saved_sample_count=len(saved), reconstructed=0)
        if journal['status'] != 'COMPLETED' or len(saved) != 4:
            report['incomplete_methods'].append(dict(method=name, reason='PARTIAL', saved_times=[r['tau'] for r in saved],
                                                      last_accepted=journal.get('last_accepted')))
        vectors = payload.get('method_vectors', {}).get(name)
        if name != METHODS[-1] and journal['status'] == 'COMPLETED' and (vectors is None or len(vectors) != 4):
            report['incomplete_methods'].append(dict(method=name, reason='MISSING_COMPLETE_METHOD_VECTOR_BINDING'))
        rows[name] = []
        for it, sample in enumerate(saved):
            need(it < len(TIMES) and sample['tau'] == TIMES[it], 'Readout prefix/time differs')
            label = 'case'+str(index)+'/'+name+'/t'+str(it)
            row = reconstruct(model, sample['tau'], sample['state'], name != METHODS[-1])
            rows[name].append(row); report['methods'][name]['reconstructed'] += 1
            check_reconstruction(label, row)
            if it == 0:
                check(label+'/fixed_initial_state', sample['state'], model.initial(), 0.)
            if name != METHODS[-1]:
                if vectors is not None:
                    check(label+'/journal_binding', vectors[it], sample['state'], 0.)
                work_checks(label, row, rows[name][0])
    reference = rows.get('RK4_h4', [])
    for name in METHODS[:3]+('DOPRI54',):
        if name == 'RK4_h4':
            continue
        for it, row in enumerate(rows.get(name, [])):
            if it >= len(reference):
                continue
            ref = reference[it]; label = 'case'+str(index)+'/chart/'+name+'/t'+str(it)
            check(label, row['chart'], ref['chart'], CONFIG['state'])
            for s in range(2):
                check(label+'/velocity'+str(s), row['species'][s]['v'], ref['species'][s]['v'], CONFIG['readout'])
                check(label+'/volume'+str(s), row['read']['volume_ratios'][s], ref['read']['volume_ratios'][s], CONFIG['readout'])
            check(label+'/action', row['read']['action_ratio'], ref['read']['action_ratio'], CONFIG['readout'])
    for it, saved in enumerate(payload.get('samples', [])):
        need(it < len(reference) and saved['tau'] == TIMES[it], 'Fine snapshot census differs')
        check_fine_snapshot('case'+str(index)+'/snapshot'+str(it), reference[it], saved)
        report['snapshots_checked'] += 1
    off_rows = rows.get(METHODS[-1], [])
    if len(off_rows) == 4 and len(payload.get('pressure_off_control', {}).get('comparisons', [])) != 4:
        report['incomplete_methods'].append(dict(method=METHODS[-1], reason='MISSING_COMPLETE_DIFFERENCE_BINDING'))
    for it in range(min(len(reference), len(off_rows))):
        on, off = reference[it], off_rows[it]; signed = dict(tau=TIMES[it], species={})
        for s, name in enumerate(('baryon', 'hard')):
            dface = on['read']['meshes'][s]-off['read']['meshes'][s]
            dv = on['species'][s]['v']-off['species'][s]['v']; dq = on['read']['q'][s]-off['read']['q'][s]
            signed['species'][name] = dict(face_displacement=dface.tolist(), peculiar_velocity=dv.tolist(), density=dq.tolist(),
                fixed_origin_displacement=float(dface[0]), first_free_face_displacement=float(dface[1]),
                first_free_face_velocity=float(dv[0]), central_cell_density=float(dq[0]),
                seed_edge_face_displacement=float(dface[16]), seed_edge_face_velocity=float(dv[15]),
                seed_edge_inside_density=float(dq[15]), seed_edge_outside_density=float(dq[16]))
            saved = payload.get('pressure_off_control', {}).get('comparisons', [])
            if it < len(saved):
                label = 'case'+str(index)+'/on_off/t'+str(it)+'/species'+str(s)
                check(label+'/faces', saved[it]['pressure_on_minus_off_faces'][s], dface)
                check(label+'/velocity', saved[it]['pressure_on_minus_off_velocity'][s], dv)
                check(label+'/density', saved[it]['pressure_on_minus_off_density'][s], dq,
                      scale=np.maximum(np.maximum(abs(on['read']['q'][s]), abs(off['read']['q'][s])), 1e-300))
        report['signed_pressure_on_off'].append(signed)
    report['complete_saved_census'] = (not report['incomplete_methods'] and report['snapshots_checked'] == 4
                                       and len(report['signed_pressure_on_off']) == 4)


def run(frozen):
    global np, producer, old, kernel, maps, shadow, certificate
    import numpy as np
    old = load('saved_audit_old_read_dependencies', J/'spherical_two_current_v001.py')
    kernel = load('saved_audit_checked_kernel_dependency', J/'spherical_exact_kinetic_v001.py')
    maps = load('saved_audit_checked_map_dependency', J/'spherical_consistent_state_maps_v001.py')
    producer = load('saved_audit_producer_definitions_only', J/'spherical_consistent_two_current_v002.py')
    producer.np = np; producer.guard = guard
    # Only initialization and read are called. No producer main, RHS, controls,
    # run_case, snapshot, integrator or input-discovery entry point is invoked.
    shadow = json.loads(read(J/'SPHERICAL_DUST_SHADOW_V001_RESULTS.json'))['payload']
    certificate = json.loads(read(J/'SMOOTH_DISK_RELEASE_CERTIFICATE_V001_RESULTS.json'))['payload']
    need(old.CONFIG == frozen['inherited_configuration'], 'Inherited read configuration differs')
    for index in range(2):
        try:
            audit_case(index, frozen)
        except BaseException as exc:
            failures.append(dict(case_index=index, type=type(exc).__name__, message=str(exc)))
            if isinstance(exc, Stop) and ('resource' in str(exc).lower() or 'rss' in str(exc).lower()):
                raise


def main():
    global started, inputs, reports, checks, failures
    need(Path.cwd().resolve() == ROOT and Path(__file__).resolve() == THIS and sys.platform == 'darwin', 'Fixed Mac root/source required')
    need(sys.argv[1:] == ['--run'] and not INTENT.exists() and not OUT.exists(), 'One exclusive audit invocation required')
    need(all(len(v) == 64 and all(c in '0123456789abcdef' for c in v) for v in PINS.values()), 'Execution pins incomplete; no audit authorized yet')
    need(all(os.environ.get(k) == '1' for k in THREAD_KEYS), 'Single-thread environment required before NumPy import')
    inputs, reports, checks, failures = {}, [], [], []; started = time.monotonic(); sys.dont_write_bytecode = True
    resource.setrlimit(resource.RLIMIT_CPU, (LIMITS['cpu_soft_seconds'], LIMITS['cpu_hard_seconds']))
    def halt(signum, frame):
        raise Stop('Wall/CPU resource signal')
    signal.signal(signal.SIGALRM, halt); signal.signal(signal.SIGXCPU, halt)
    for name, digest in PINS.items():
        pin(J/name, digest)
    frozen = json.loads(read(FROZEN))
    need(frozen['schema'] == 'SPHERICAL_CONSISTENT_TWO_CURRENT_FREEZE_V002' and frozen['cases'] == CASES,
         'Wrong prospective freeze schema or case census')
    control = json.loads(read(J/'SPHERICAL_CONSISTENT_TWO_CURRENT_SUPERVISOR_V002_FROZEN.json'))
    need(control['producer_freeze_sha256'] == PINS[FROZEN.name]
         and control['freeze_receipt_sha256'] == PINS['SPHERICAL_CONSISTENT_TWO_CURRENT_V002_FREEZE_RUN.json'],
         'Controller/science freeze lineage differs')
    for name, digest in frozen['files'].items():
        relative = Path(name)
        need(not relative.is_absolute() and '..' not in relative.parts, 'Invalid freeze path')
        pin(ROOT/relative, digest)
    source_sha = sha(pin(THIS)); protocol_sha = sha(pin(PROTOCOL))
    publish(INTENT, dict(schema='SPHERICAL_CONSISTENT_SAVED_AUDIT_INTENT_V001', source_sha256=source_sha,
        protocol_sha256=protocol_sha, config=CONFIG, limits=LIMITS, pins=PINS, inputs=inputs,
        thread_environment={k:os.environ[k] for k in THREAD_KEYS}, argv=sys.argv))
    pin(INTENT); signal.alarm(LIMITS['wall_seconds'])
    try:
        run(frozen)
    except BaseException as exc:
        failures.append(dict(type=type(exc).__name__, message=str(exc)))
    finally:
        signal.alarm(0)
    custody = True
    try:
        for path, meta in inputs.items():
            raw = read(Path(path)); need(sha(raw) == meta['sha256'] and len(raw) == meta['bytes'], 'End custody changed')
    except BaseException as exc:
        custody = False; failures.append(dict(type=type(exc).__name__, message=str(exc)))
    complete = len(reports) == 2 and all(r.get('complete_saved_census', False) for r in reports)
    reconstructed = complete and custody and not failures and all(c['passed'] for c in checks)
    passed = reconstructed and all(r['producer_complete'] for r in reports)
    payload = dict(schema='SPHERICAL_CONSISTENT_SAVED_AUDIT_V001',
        status='SAVED_ARITHMETIC_CHECKS_PASSED' if passed else 'SAVED_FAILURES_OR_INCOMPLETE_RETAINED',
        source_sha256=source_sha, protocol_sha256=protocol_sha, inputs=inputs, config=CONFIG, limits=LIMITS,
        reports=reports, checks=checks, failures=failures, custody_end_verified=custody,
        complete_saved_census=complete, all_saved_arithmetic_checks_passed=passed,
        reconstruction_checks_passed=reconstructed, inherited_failed_producer_not_waived=True,
        numerical_entry_count=sum(c['count'] for c in checks), failed_check_groups=sum(not c['passed'] for c in checks),
        resources_analysis_phase=dict(seconds=time.monotonic()-started,
            maximum_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        independently_authored_reproduction=False, trajectory_rerun=False,
        qualification=dict(trajectory=False, continuum=False, physical_source=False, formation=False,
                           full_metric=False, observations=False, Stage3_complete=False), mandatory_lanes_open=11)
    publish(OUT, dict(payload_sha256=sha(enc(payload)), payload=payload))
    print(enc(dict(path=str(OUT), sha256=sha(read(OUT)), status=payload['status'])).decode())
    if not passed:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
