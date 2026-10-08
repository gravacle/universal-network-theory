"""Inert two-case consistent-inertia experiment; root alone executes after review.

Reuse only authenticated old definitions, never ancestral main/inputs/run_case.
Physical inputs, forces and EOS are unchanged. All qualification flags stay false.
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
import sys
import time
import traceback

ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J = ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
THIS = J/'spherical_consistent_two_current_v001.py'
PROTOCOL = J/'SPHERICAL_CONSISTENT_TWO_CURRENT_PROTOCOL_V001.md'
SUPERVISOR = J/'spherical_consistent_two_current_supervisor_v001.py'
FREEZE = J/'SPHERICAL_CONSISTENT_TWO_CURRENT_V001_FROZEN.json'
PINS = {
    'spherical_two_current_v001.py': '0349740de7d0b4173f634eaf8fd52c7e5eb4ea9ea196f95a5b882024f6dd95df',
    'SPHERICAL_TWO_CURRENT_V001_FROZEN.json': '0c698bc6c9867d7afdb32f2dc51f9b776a14f6512a5e302ec8b28aa0c9057c82',
    'spherical_exact_kinetic_v001.py': '78765ef0e2d29c044642b1d944682a81ff5d48b22de9d0cb16b7bc47b9c7e11a',
    'spherical_consistent_state_maps_v001.py': '483ebdcb7fc66532911d6a9eac0eece4e29c3fff2eef063dd397ea31193e2dc4',
    'SPHERICAL_CONSISTENT_SOLVER_INTEGRATION_DESIGN_V001.md': 'a3fc53447b520650b44c5ad16e135745c1c14aefcbf78bf592cfc3d98e135413',
    'SPHERICAL_EXACT_INERTIA_DERIVATION_V001.md': '3a60f43ea5e666e23bac8e478df74f38aeaac77f0cc4a86c15cae593a622a431',
    'SPHERICAL_EXACT_KINETIC_ORACLE_V001_RESULTS.json': '738dd1f841cfa1648f178c4dcbc556f5333b0e560ab3daae82908cd3f715250b',
    'SPHERICAL_EXACT_KINETIC_ORACLE_V001_INTENT.json': '519974b2736eb77abe8d41dfabd062c1c4f18f97c9874014a46b960563abee1d',
}
CASES = [dict(case_index=i, gap=gap, L=8., dx=1/16, cells=128)
         for i, gap in enumerate((128, 8192))]
METHODS = ('RK4_h', 'RK4_h2', 'RK4_h4', 'DOPRI54')
LIMITS = dict(wall_seconds=165, cpu_soft_seconds=150, cpu_hard_seconds=155,
              self_rss_bytes=536870912, output_bytes=16777216,
              input_file_bytes=67108864, maximum_frozen_members=200)
THREAD_KEYS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
               'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS')
SCOPE = dict(trajectory_qualified=False, spatial_continuum_qualified=False,
             certified_cfl=False, certified_no_crossing=False,
             full_relativistic_metric_qualified=False, observational_fit=False,
             physical_state_formation=False, physical_source_qualified=False,
             Stage3_complete=False)


def enc(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def bound(path):
    path = Path(path)
    path.relative_to(ROOT)
    if '..' in path.parts:
        raise RuntimeError('Parent traversal refused')
    for p in (path, *path.parents):
        if p == ROOT.parent:
            break
        if p.is_symlink():
            raise RuntimeError('Linked input refused')
    if path.resolve(strict=True) != path:
        raise RuntimeError('Input ancestry differs')
    if path.stat().st_size > LIMITS['input_file_bytes']:
        raise RuntimeError('Input size bound')
    return path


def read(path):
    return bound(path).read_bytes()


def snapshot_inputs():
    if Path.cwd().resolve() != ROOT or Path(__file__).resolve() != THIS:
        raise RuntimeError('Fixed project/source required')
    files = {}
    def add(path, expected=None):
        data = read(path)
        digest = sha(data)
        if expected is not None and digest != expected:
            raise RuntimeError('Changed input '+str(path))
        files[str(path.relative_to(ROOT))] = digest
        return data
    for name, digest in PINS.items():
        add(J/name, digest)
    prior = json.loads(read(J/'SPHERICAL_TWO_CURRENT_V001_FROZEN.json'))
    if len(prior['files']) > LIMITS['maximum_frozen_members']:
        raise RuntimeError('Unexpected inherited custody census')
    for name, digest in prior['files'].items():
        rel = Path(name)
        if rel.is_absolute() or '..' in rel.parts:
            raise RuntimeError('Invalid inherited freeze member')
        add(ROOT/rel, digest)
    for path in (THIS, PROTOCOL, SUPERVISOR):
        add(path)
    return dict(schema='SPHERICAL_CONSISTENT_TWO_CURRENT_FREEZE_V001', files=files,
                cases=CASES, limits=LIMITS, inherited_configuration=prior['configuration'],
                methods=list(METHODS), fixed_step_factors=[1., .5, .25],
                pressure_off_factor=.25, test_velocity_coefficients=[.17, -.11],
                state_error_chart='A_xb_vb_xh_vh_hard_specific_last_three_ledgers',
                ceiling_interpretation='legacy_work_ceiling_not_certified_CFL',
                scope=SCOPE, mandatory_lanes_open=11)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ResourceStop(RuntimeError):
    pass


def guard():
    if time.monotonic()-started > LIMITS['wall_seconds']:
        raise ResourceStop('COOPERATIVE_WALL_LIMIT')
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss > LIMITS['self_rss_bytes']:
        raise ResourceStop('COOPERATIVE_SELF_RSS_LIMIT')


def make_model_class(old, kernel, maps):
    class Model(old.Model):
        def __init__(self, case, shadow, certificate, pressure=True):
            # Do not call the old initializer: no hidden lumping or domain gate.
            self.case = case; self.N = case['cells']; self.R = case['gap']; self.pressure = pressure
            self.old = next(c for c in shadow['cases'] if c['gap'] == self.R)
            self.ref = self.old['background_reference']; self.s = self.old['source_state']
            self.Kb = next(c['Kb'] for c in certificate['cases'] if c['gap'] == self.R)
            self.ell = self.old['ell_m']; self.td = self.old['t_dyn_s']; self.eps = self.old['epsilon']; self.M = self.old['seed_mass_kg']
            self.rho_unit = self.M/self.ell**3; self.v2 = self.s['gstar']*self.ell
            self.S = self.s['gstar']**2/(4*math.pi*old.CONFIG['G_SI']*self.Kb)
            self.qh = self.old['rho0_H1_kg_m3']/self.rho_unit
            self.qb = 3*self.ref['H0_s_inverse']**2*self.ref['Omega_b']/(8*math.pi*old.CONFIG['G_SI']*self.rho_unit)
            self.qbar = self.qh+self.qb; self.x0 = np.linspace(0, case['L'], self.N+1)
            self.V0 = 4*math.pi*np.diff(self.x0**3)/3
            self.masses = [np.diff(old.seed_mass(self.x0))+self.qb*self.V0, self.qh*self.V0]
            self.eos = old.EOS(self.R, old.CONFIG['primary_order']); self.I1 = self.s['I']; self.e1 = self.s['E']/old.CONFIG['beta']
            self.speed_cap = old.CONFIG['velocity_cap']+math.sqrt(4*self.I1/(self.R**3*self.eps))
            self.step = min(old.CONFIG['max_step'], old.CONFIG['cfl']*case['dx']/self.speed_cap)
            self.nstate = 1+4*self.N+10; self.last = None; self.maxima = {}; self.minimum_volume_ratio = 1.
            self.cache = None

        def read(self, t, y, guard=True):
            globals()['guard']()
            if len(y) != self.nstate or not np.all(np.isfinite(y)):
                raise old.Stop(t, y, 'NONFINITE_STATE')
            A = y[0]; n = self.N
            meshes = [np.r_[0., y[1:1+n]], np.r_[0., y[1+2*n:1+3*n]]]
            ps = [y[1+n:1+2*n], y[1+3*n:1+4*n]]
            vols = [4*math.pi*np.diff(x**3)/3 for x in meshes]
            if A < 1-2e-14 or any(np.any(v <= 0) for v in vols):
                raise old.Stop(t, y, 'NONPOSITIVE_ORDERED_VOLUME_OR_BACKGROUND')
            states = [kernel.canonical_kinematics(x, m, p, A) for x, m, p in zip(meshes, self.masses, ps)]
            velocities = [s['peculiar_velocity'] for s in states]
            ratios = [v/self.V0 for v in vols]; qs = [m/v for m, v in zip(self.masses, vols)]
            action_ratio = qs[1]/self.qh
            if guard and (max(float(np.max(abs(v))) for v in velocities) > old.CONFIG['velocity_cap'] or
                          min(float(np.min(r)) for r in ratios) < .25 or max(float(np.max(r)) for r in ratios) > 4 or
                          float(np.min(action_ratio)) < .25 or float(np.max(action_ratio)) > 4):
                raise old.Stop(t, y, 'PROSPECTIVE_VELOCITY_ACTION_OR_VOLUME_GUARD')
            mat = self.eos.at(np.r_[self.I1*action_ratio/A**3, self.I1/A**3])
            bg = {k: float(v[-1]) for k, v in mat.items()}; hard = {k: v[:-1] for k, v in mat.items()}
            Ht = self.ref['H0_s_inverse']*self.td*math.sqrt(self.ref['Omega_b']/A**3+self.ref['Omega_exc']*bg['e']/self.e1+self.ref['Omega_Lambda'])
            P = A**3*self.S*old.CONFIG['beta']*hard['p']/(self.rho_unit*self.v2)
            Pbar = A**3*self.S*old.CONFIG['beta']*bg['p']/(self.rho_unit*self.v2)
            grad, W0, span, phi = old.gravity(meshes, self.masses, self.qbar)
            Ts = [s['kinetic_energy'] for s in states]
            o = dict(A=A, meshes=meshes, ps=ps, volumes=vols, q=qs, velocities=velocities,
                     hard=hard, background_material=bg, Ht=Ht, P=P, Pbar=Pbar, gradW0=grad,
                     K=sum(Ts), K_species=Ts, U=float(np.dot(self.masses[1], hard['dE']))/self.eps,
                     Ubar=float(np.sum(self.masses[1]))*bg['dE']/self.eps, W=float(W0/A),
                     potential_span_over_c2=span/A*self.eps, action_ratio=action_ratio,
                     volume_ratios=ratios, kinematics=states)
            self.cache = o
            return o

        def rhs(self, t, y):
            globals()['guard']()
            # The ancestral method uses self.read and the same physical force/work
            # formulas. It has no face-mass access and no geometric kick.
            out = old.Model.rhs(self, t, y)
            o = self.cache; n = self.N
            out[1+n:1+2*n] += o['kinematics'][0]['geometric_force']
            out[1+3*n:1+4*n] += o['kinematics'][1]['geometric_force']
            if not np.all(np.isfinite(out)):
                raise old.Stop(t, y, 'NONFINITE_RHS')
            return out
    return Model


def journal_start(model, name):
    y = model.initial()
    row = dict(method=name, status='STARTED', samples=[dict(tau=0., state=y.tolist())],
               last_accepted=dict(tau=0., state=y.tolist()), rhs_evaluations=0,
               accepted=0, rejected=0)
    return row, y


def accept(row, t, y):
    row['accepted'] += 1
    row['last_accepted'] = dict(tau=float(t), state=y.tolist())


def rk4(model, row, step):
    y = model.initial(); t = 0.; samples = [y.copy()]
    row['maximum_step'] = step
    for target in old.CONFIG['times'][1:]:
        count = math.ceil((target-t)/step); h = (target-t)/count
        for _ in range(count):
            guard()
            k1 = model.rhs(t, y); k2 = model.rhs(t+h/2, y+h*k1/2)
            k3 = model.rhs(t+h/2, y+h*k2/2); k4 = model.rhs(t+h, y+h*k3)
            row['rhs_evaluations'] += 4
            y = y+h*(k1+2*k2+2*k3+k4)/6; t += h
            model.read(t, y); accept(row, t, y)
        t = target; samples.append(y.copy()); row['samples'].append(dict(tau=t, state=y.tolist()))
    row['status'] = 'COMPLETED'
    return samples


def dopri(model, row):
    y = model.initial(); t = 0.; h = model.step; samples = [y.copy()]
    aa = [[], [1/5], [3/40, 9/40], [44/45, -56/15, 32/9], [19372/6561, -25360/2187, 64448/6561, -212/729],
          [9017/3168, -355/33, 46732/5247, 49/176, -5103/18656], [35/384, 0, 500/1113, 125/192, -2187/6784, 11/84]]
    cc = [0, 1/5, 3/10, 4/5, 8/9, 1, 1]
    b5 = np.array([35/384, 0, 500/1113, 125/192, -2187/6784, 11/84, 0])
    b4 = np.array([5179/57600, 0, 7571/16695, 393/640, -92097/339200, 187/2100, 1/40])
    for target in old.CONFIG['times'][1:]:
        while t < target:
            guard(); h = min(h, target-t, model.step)
            if t+h == t:
                raise old.Stop(t, y, 'TIME_STEP_UNDERFLOW')
            ks = []
            for i in range(7):
                yy = y.copy()
                for j, a in enumerate(aa[i]):
                    yy += h*a*ks[j]
                ks.append(model.rhs(t+cc[i]*h, yy)); row['rhs_evaluations'] += 1
            K = np.asarray(ks); high = y+h*np.dot(b5, K); low = y+h*np.dot(b4, K)
            # Retain domain failures at either embedded endpoint; no hidden retry.
            model.read(t+h, high); model.read(t+h, low)
            norm = maps.embedded_error_norm(kernel, y, high, low, model.masses)
            row['last_attempt'] = dict(tau=t, step=h, error_norm=norm,
                                       high=high.tolist(), low=low.tolist())
            if norm <= 1:
                y = high; t += h; accept(row, t, y)
            else:
                row['rejected'] += 1
            h *= min(5., max(.2, .9*norm**-.2)) if norm else 5.
        samples.append(y.copy()); row['samples'].append(dict(tau=t, state=y.tolist()))
    row['status'] = 'COMPLETED'
    return samples


def pressure_kick(o):
    return 4*math.pi*o['meshes'][1][1:]**2*(o['P']-np.r_[o['P'][1:], o['Pbar']])


def plain(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, dict):
        return {k: plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    if isinstance(value, np.generic):
        return value.item()
    return value


def snapshot(model, t, y):
    o = model.read(t, y); A = o['A']; data = {}; pk = pressure_kick(o)
    for i, name in enumerate(('baryon', 'hard')):
        x = o['meshes'][i]; mass = model.masses[i]; state = o['kinematics'][i]
        kicks = dict(gravity=-o['gradW0'][i]/A)
        if i == 1 and model.pressure:
            kicks['pressure'] = pk
        acc = maps.peculiar_acceleration_decomposition(kernel, x, mass, o['ps'][i], A, o['Ht'], kicks)
        residual = kernel.tridiagonal_matvec(state['diagonal'], state['off_diagonal'], o['velocities'][i])-o['ps'][i]/A
        residual_scale = max(float(np.max(abs(o['ps'][i]/A))), float(np.max(abs(state['diagonal']*o['velocities'][i]))), np.finfo(float).tiny)
        centers = (x[:-1]+x[1:])/2
        data[name] = dict(faces=x, peculiar_v_over_vdyn=o['velocities'][i], canonical_momentum=o['ps'][i],
            cell_masses_over_M=mass, comoving_density=o['q'][i], volume_ratio=o['volume_ratios'][i],
            enclosed_mass_over_M=np.r_[0., np.cumsum(mass)],
            gravity_acceleration_over_gstar=acc['physical_force_responses']['gravity'],
            acceleration_interpretation='peculiar_velocity_derivative_not_physical_radius_acceleration',
            acceleration_decomposition=acc, geometric_canonical_kick=state['geometric_force'],
            inertia_diagonal=state['diagonal'], inertia_off_diagonal=state['off_diagonal'],
            solve_residual=residual, normalized_solve_residual=float(np.max(abs(residual)))/residual_scale,
            log_density_radial_gradient=np.diff(np.log(o['q'][i]))/np.diff(centers),
            face_velocity_radial_gradient=np.diff(np.r_[0., o['velocities'][i]])/np.diff(x))
    return plain(dict(tau=t, seconds=t*model.td, A=A, H_s_inverse=o['Ht']/model.td, species=data,
        hard_material=o['hard'], action_ratio=o['action_ratio'], hard_pressure_dimensionless=o['P'],
        background_pressure=o['Pbar'], K=o['K'], K_species=o['K_species'], U=o['U'], Ubar=o['Ubar'],
        U_excess=o['U']-o['Ubar'], W=o['W'], potential_span_over_c2=o['potential_span_over_c2'],
        hard_gravity_omission_internal_over_rest=o['hard']['dE'],
        hard_gravity_omission_active_over_rest=o['hard']['dE']+3*o['hard']['p']/(model.R*o['hard']['I']),
        ledger=y[1+4*model.N:])))


def actual_mesh_controls(model, ck, records):
    y = model.initial(); n = model.N
    for i, coefficient in enumerate((.17, -.11)):
        offset = 1+2*n*i; x = np.r_[0., y[offset:offset+n]]
        v = coefficient*x[1:]/(1+x[1:]); d, e = kernel.mass_matrix(x, model.masses[i])
        y[offset+n:offset+2*n] = y[0]*kernel.tridiagonal_matvec(d, e, v)
    o = model.read(0., y); dy = model.rhs(0., y)
    for i in range(2):
        state = o['kinematics'][i]; mass = model.masses[i]; mt = float(np.sum(mass))
        x = o['meshes'][i]; p = o['ps'][i]; v = o['velocities'][i]; xd = v/o['A']
        direction = .1*np.sin(math.pi*x[1:]/model.case['L'])
        md, me = maps.mass_matrix_directional_derivative(x, mass, direction)
        kin_fd = []; matrix_fd = []
        for h in old.CONFIG['gradient_steps']:
            matrices = []; energies = []
            for sign in (-1, 1):
                xx = np.r_[0., x[1:]+sign*h*direction]
                ss = kernel.canonical_kinematics(xx, mass, p, o['A'])
                matrices.append(np.r_[ss['diagonal'], ss['off_diagonal']]); energies.append(ss['kinetic_energy'])
            kin_fd.append((energies[1]-energies[0])/(2*h))
            matrix_fd.append((matrices[1]-matrices[0])/(2*h))
            ck.test('actual_mesh_kinetic_centered_'+str(i)+'_'+str(h), kin_fd[-1]/mt,
                    -np.dot(state['geometric_force'], direction)/mt, old.CONFIG['gradient_tolerance'])
            ck.test('actual_mesh_matrix_centered_'+str(i)+'_'+str(h), matrix_fd[-1]/mt,
                    np.r_[md, me]/mt, old.CONFIG['gradient_tolerance'])
        ck.test('actual_mesh_kinetic_Richardson_'+str(i), (4*kin_fd[1]-kin_fd[0])/(3*mt),
                -np.dot(state['geometric_force'], direction)/mt, old.CONFIG['gradient_tolerance'])
        ck.test('actual_mesh_matrix_Richardson_'+str(i), (4*matrix_fd[1]-matrix_fd[0])/(3*mt),
                np.r_[md, me]/mt, old.CONFIG['gradient_tolerance'])
        # Independent Mdot contraction versus assembled g in canonical work.
        td, te = maps.mass_matrix_directional_derivative(x, mass, xd)
        half_mdot = .5*np.dot(v, kernel.tridiagonal_matvec(td, te, v))
        ck.test('actual_mesh_geometric_work_cancellation_'+str(i), half_mdot/mt,
                np.dot(xd, state['geometric_force'])/mt)
        offset = 1+2*n*i
        pdot = dy[offset+n:offset+2*n]
        chain = np.dot(xd, pdot)-half_mdot-2*o['Ht']*state['kinetic_energy']
        physical = -np.dot(xd, o['gradW0'][i])/o['A']-2*o['Ht']*state['kinetic_energy']
        if i == 1:
            physical += np.dot(xd, pressure_kick(o))
        ck.test('actual_mesh_kinetic_work_chain_'+str(i), chain/mt, physical/mt)
        records.append(dict(species=i, total_mass=mt, direction=direction.tolist(),
            test_velocity=v.tolist(), kinetic_centered=plain(kin_fd), matrix_centered=plain(matrix_fd),
            kinetic_analytic=float(-np.dot(state['geometric_force'], direction)),
            half_v_Mdot_v=float(half_mdot), geometric_work=float(np.dot(xd, state['geometric_force'])),
            kinetic_chain=float(chain), physical_work=float(physical)))


def verify_samples(model, runs, samples, ck):
    fine = runs['RK4_h4']; initial = samples[0]; checkmat = old.EOS(model.R, old.CONFIG['check_order'])
    for it, (t, y, snap) in enumerate(zip(old.CONFIG['times'], fine, samples)):
        own = model.read(t, y)
        for name in ('RK4_h', 'RK4_h2', 'DOPRI54'):
            yy = runs[name][it]
            ck.test('time_state_'+name, maps.physical_error_chart(kernel, yy, model.masses),
                    maps.physical_error_chart(kernel, y, model.masses), old.CONFIG['state_tolerance'])
            other = model.read(t, yy)
            for sp in range(2):
                ck.test('time_velocity_'+name, other['velocities'][sp], own['velocities'][sp], old.CONFIG['readout_tolerance'])
                ck.test('time_volume_ratio_'+name, other['volume_ratios'][sp], own['volume_ratios'][sp], old.CONFIG['readout_tolerance'])
            ck.test('time_action_ratio_'+name, other['action_ratio'], own['action_ratio'], old.CONFIG['readout_tolerance'])
        hmat = snap['hard_material']; q = checkmat.at(np.asarray(hmat['I']))
        for key in ('e', 'p', 'omega', 'cI2', 'dE', 'dW'):
            a = np.asarray(hmat[key]); ck.test('material_'+key, a, q[key], old.CONFIG['material_tolerance'], np.maximum(abs(a), 1e-300))
        Is = np.asarray(hmat['I']); es = np.asarray(hmat['e']); ps = np.asarray(hmat['p']); ws = np.asarray(hmat['omega'])
        ck.test('virial_enthalpy', Is*ws, es+ps, old.CONFIG['material_tolerance'], abs(es+ps))
        ck.test('mass_action', np.asarray(hmat['action_recovered']), Is, old.CONFIG['material_tolerance'], abs(Is))
        ck.test('sound_upper_bound', np.maximum(0., np.asarray(hmat['cN_c2'])*model.R**3/Is-1.), 0.)
        ck.test('total_action_energy_ledger', snap['K']+snap['U']+snap['W']-initial['K']-initial['U']-initial['W'], snap['ledger'][4], old.CONFIG['readout_tolerance'])
        ck.test('mechanical_work_ledger', snap['K']+snap['U']-initial['K']-initial['U'], sum(snap['ledger'][:3]), old.CONFIG['readout_tolerance'])
        mh = float(np.sum(model.masses[1]))
        ck.test('hard_mechanical_work_per_rest_mass', (snap['K_species'][1]+snap['U']-initial['K_species'][1]-initial['U'])/mh,
                snap['ledger'][9]/mh, old.CONFIG['readout_tolerance'])
        ck.test('baryon_mechanical_work', snap['K_species'][0]-initial['K_species'][0],
                snap['ledger'][0]-snap['ledger'][7]+snap['ledger'][2]-snap['ledger'][8], old.CONFIG['readout_tolerance'])
        for species in ('baryon', 'hard'):
            ck.test('fixed_mass_'+species, sum(snap['species'][species]['cell_masses_over_M']), sum(initial['species'][species]['cell_masses_over_M']))
            ck.test('snapshot_solve_residual_'+species, snap['species'][species]['normalized_solve_residual'], 0.)


def run_case(case, shadow, certificate):
    ck = old.Checks(); out = dict(case=case, status='STARTED', journals={}, actual_mesh_controls=[],
                                samples=[], method_vectors={}, scope=SCOPE, mandatory_lanes_open=11)
    model = None; active_model = None; active_row = None
    try:
        Model = make_model_class(old, kernel, maps); model = Model(case, shadow, certificate); active_model = model
        old.controls(model, ck); actual_mesh_controls(model, ck, out['actual_mesh_controls'])
        if ck.failures:
            raise RuntimeError('Prerequisite actual-mesh/material controls failed')
        out['prerequisite_diagnostics'] = dict(maxima=model.maxima.copy(),
            minimum_volume_ratio=model.minimum_volume_ratio, max_action_root_error=model.eos.max_action_error)
        model.maxima = {}; model.minimum_volume_ratio = 1.; model.eos.max_action_error = 0.
        runs = {}
        for name, factor in zip(METHODS, (1., .5, .25, None)):
            active_row, _ = journal_start(model, name); out['journals'][name] = active_row
            runs[name] = dopri(model, active_row) if factor is None else rk4(model, active_row, model.step*factor)
            out['method_vectors'][name] = [v.tolist() for v in runs[name]]
        for t, y in zip(old.CONFIG['times'], runs['RK4_h4']):
            out['samples'].append(snapshot(model, t, y))
        verify_samples(model, runs, out['samples'], ck)
        dust = Model(case, shadow, certificate, pressure=False)
        active_model = dust
        active_row, _ = journal_start(dust, 'PRESSURE_OFF_RK4_h4'); out['journals']['PRESSURE_OFF_RK4_h4'] = active_row
        dust_rows = rk4(dust, active_row, dust.step*.25)
        differences = []
        for i, (t, yy) in enumerate(zip(old.CONFIG['times'], dust_rows)):
            o = dust.read(t, yy); on = model.read(t, runs['RK4_h4'][i])
            saved = dust.old['samples'][i]['fields']['f']; labels = dust.x0
            expected = labels*np.interp(labels, np.arange(257)/16, saved)
            differences.append(plain(dict(tau=t, labels=labels, shadow_faces=expected,
                baryon_minus_shadow=o['meshes'][0]-expected, hard_minus_shadow=o['meshes'][1]-expected,
                pressure_on_minus_off_faces=[on['meshes'][s]-o['meshes'][s] for s in range(2)],
                pressure_on_minus_off_velocity=[on['velocities'][s]-o['velocities'][s] for s in range(2)],
                pressure_on_minus_off_density=[on['q'][s]-o['q'][s] for s in range(2)])))
        out['pressure_off_control'] = dict(comparisons=differences, energy_qualified=False,
                                           same_consistent_inertia=True, geometry_retained=True)
        out['status'] = 'COMPLETE_EXPLORATORY_NUMERICAL_CASE' if not ck.failures else 'FAILED_NUMERICAL_CHECKS_RETAINED'
    except BaseException as exc:
        out.update(status='FAILED_OR_INCOMPLETE_RETAINED', exception=dict(type=type(exc).__name__, message=str(exc)),
                   traceback=traceback.format_exc()[-8192:])
        if active_row is not None and active_row['status'] == 'STARTED':
            active_row['status'] = 'FAILED_OR_INCOMPLETE_RETAINED'
        t, state = ((exc.t, exc.y) if isinstance(exc, old.Stop) else
                    (active_model.last if active_model is not None and active_model.last is not None else (None, None)))
        if state is not None:
            state = np.asarray(state, dtype='<f8')
            out['failure_snapshot'] = dict(tau=t, state=[float(v) if math.isfinite(v) else None for v in state],
                state_ieee754_little_endian_base64=base64.b64encode(state.tobytes()).decode(),
                reason=exc.why if isinstance(exc, old.Stop) else str(exc))
    if model is not None:
        out.update(source_state=model.s, background_reference=model.ref, legacy_work_ceiling=model.step,
                   formal_continuum_travel_bound=model.speed_cap*old.CONFIG['times'][-1],
                   discrete_domain_of_dependence_proved=False, sampled_stage_maxima=model.maxima,
                   minimum_sampled_stage_volume_ratio=model.minimum_volume_ratio,
                   max_action_root_error=model.eos.max_action_error,
                   units=dict(ell_m=model.ell, t_dyn_s=model.td, seed_mass_kg=model.M, epsilon=model.eps,
                              rho_unit=model.rho_unit, v_dyn_m_s=math.sqrt(model.v2),
                              q_baryon_background=model.qb, q_hard_background=model.qh),
                   inherited_omissions={key:model.old[key] for key in ('ordinary_radiation_H2_omission_fraction_today',
                       'radiation_active_mass_per_unit_brightness_kg_m3', 'complete_radiation_brightness_envelope')})
    out.update(checks=ck.counts, worst_errors=ck.maxima, failures=ck.failures,
               numerical_entry_count=sum(ck.counts.values()), failed_check_groups=len(ck.failures))
    return out


def main():
    global started, np, old, kernel, maps
    started = time.monotonic()
    if sys.platform != 'darwin' or not all(os.environ.get(k) == '1' for k in THREAD_KEYS):
        raise RuntimeError('This Mac and one-thread environment required before NumPy import')
    resource.setrlimit(resource.RLIMIT_CPU, (LIMITS['cpu_soft_seconds'], LIMITS['cpu_hard_seconds']))
    def stop(signum, frame):
        raise ResourceStop('CPU_OR_WALL_SIGNAL_LIMIT')
    signal.signal(signal.SIGXCPU, stop); signal.signal(signal.SIGALRM, stop)
    sys.dont_write_bytecode = True
    frozen = snapshot_inputs(); args = sys.argv[1:]
    if args == ['freeze']:
        print(enc(frozen).decode()); return
    if len(args) != 2 or args[0] != 'run-case' or args[1] not in ('0', '1'):
        raise RuntimeError('Use freeze or run-case 0|1')
    raw_freeze = read(FREEZE)
    if json.loads(raw_freeze) != frozen:
        raise RuntimeError('Absent or changed experiment freeze')
    index = int(args[1]); signal.alarm(LIMITS['wall_seconds'])
    import numpy as np
    old = load('owned_two_current_definitions_only', J/'spherical_two_current_v001.py')
    kernel = load('owned_exact_inertia_definitions_only', J/'spherical_exact_kinetic_v001.py')
    maps = load('owned_consistent_state_maps_only', J/'spherical_consistent_state_maps_v001.py')
    if old.CONFIG != frozen['inherited_configuration'] or maps.EXPECTED_KERNEL_SHA256 != PINS['spherical_exact_kinetic_v001.py']:
        raise RuntimeError('Inherited configuration or kernel identity differs')
    witness = json.loads(read(J/'SPHERICAL_EXACT_KINETIC_ORACLE_V001_RESULTS.json'))
    if sha(enc(witness['payload'])) != witness['payload_sha256'] or not witness['payload']['all_numerical_controls_passed']:
        raise RuntimeError('Exact kernel prerequisite receipt differs')
    shadow_wrapper = json.loads(read(J/'SPHERICAL_DUST_SHADOW_V001_RESULTS.json'))
    if sha(enc(shadow_wrapper['payload'])) != shadow_wrapper['payload_sha256']:
        raise RuntimeError('Inherited physical input payload differs')
    shadow = shadow_wrapper['payload']
    certificate = json.loads(read(J/'SMOOTH_DISK_RELEASE_CERTIFICATE_V001_RESULTS.json'))['payload']
    payload = run_case(CASES[index], shadow, certificate)
    signal.alarm(0)
    try:
        if snapshot_inputs() != frozen or read(FREEZE) != raw_freeze:
            raise RuntimeError('Input custody changed during experiment')
        payload['custody_end_verified'] = True
    except BaseException as exc:
        payload.update(custody_end_verified=False, custody_error=str(exc), status='CUSTODY_FAILURE_RETAINED')
    payload['resources_analysis_phase'] = dict(seconds=time.monotonic()-started,
        maximum_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    raw = enc(dict(freeze_sha256=sha(raw_freeze), payload_sha256=sha(enc(payload)), payload=payload))
    if len(raw) > LIMITS['output_bytes']:
        raise RuntimeError('Result size exceeds frozen limit; supervisor retains attempt')
    print(raw.decode(), flush=True)
    if payload['status'] != 'COMPLETE_EXPLORATORY_NUMERICAL_CASE':
        raise SystemExit(2)


if __name__ == '__main__':
    main()
