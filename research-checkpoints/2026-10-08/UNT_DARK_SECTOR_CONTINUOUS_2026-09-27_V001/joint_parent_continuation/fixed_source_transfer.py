"""Observed-velocity-free transfer helpers for the already qualified field law.

No import-time execution, source choice, observational score or parameter fit.
The caller freezes its source, radii, protocol and this code before running.
"""
import os
import sys
sys.dont_write_bytecode = True
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[name] = '1'
import hashlib
import json
import math
from pathlib import Path
import resource
import tempfile
import time
import numpy as np
import disk_solver as law
import axisymmetric_disk_v002 as disk
import galaxy_density as units
import galaxy_ring_oracle as ring

JOBS = ((256, 255, False), (320, 1023, False),
        (512, 255, False), (512, 255, True))


def authenticated(path, freeze_sha256):
    record = json.loads(Path(path).read_text())
    assert record['freeze_sha256'] == freeze_sha256
    p = record['payload']
    assert record['payload_sha256'] == hashlib.sha256(law.encode(p)).hexdigest()
    return p


def publish(path, payload, freeze_sha256):
    law.save_new(Path(path), {'freeze_sha256': freeze_sha256,
        'payload_sha256': hashlib.sha256(law.encode(payload)).hexdigest(),
        'payload': payload})


def identity(model, n, extent, newtonian):
    assert model and all(c.isalnum() or c in '_-' for c in model)
    return f'{model}_N{n}_L{extent}_Newton{int(newtonian)}'


def validate_radii(radii):
    radii = np.asarray(radii, dtype=float)
    assert radii.shape == (5,) and np.all(np.isfinite(radii))
    assert radii[0] > 0 and np.all(np.diff(radii) > 0)
    return radii


def checkpoint_writer(path, case, freeze_sha256):
    path = Path(path)

    def write(phi, history):
        history_text = law.encode(history).decode()
        metadata = {'case': case, 'freeze_sha256': freeze_sha256,
            'phi_sha256': hashlib.sha256(phi.tobytes(order='C')).hexdigest(),
            'history_sha256': hashlib.sha256(history_text.encode()).hexdigest(),
            'shape': list(phi.shape), 'dtype': str(phi.dtype)}
        with tempfile.NamedTemporaryFile(dir=path.parent,
                prefix=path.name+'.partial.', delete=False) as stream:
            np.savez_compressed(stream, phi=phi, history=history_text,
                                metadata=law.encode(metadata).decode())
            stream.flush()
            os.fsync(stream.fileno())
            temporary = Path(stream.name)
        os.replace(temporary, path)  # Only this identified case's rolling checkpoint.
        print(json.dumps({'checkpoint': case, 'outer': len(history),
            'nonlinear_error': history[-1].get('nonlinear_error'),
            'flux_balance_error': history[-1].get('flux_balance_error')}), flush=True)
    return write


def load_checkpoint(path, case, freeze_sha256, n):
    with np.load(path, allow_pickle=False) as saved:
        phi = saved['phi']
        history_text = str(saved['history'].item())
        metadata = json.loads(str(saved['metadata'].item()))
    assert metadata['case'] == case and metadata['freeze_sha256'] == freeze_sha256
    assert metadata['shape'] == list(phi.shape) == [n, n]
    assert metadata['dtype'] == str(phi.dtype) == 'float64'
    assert metadata['phi_sha256'] == hashlib.sha256(phi.tobytes(order='C')).hexdigest()
    assert metadata['history_sha256'] == hashlib.sha256(history_text.encode()).hexdigest()
    assert np.all(np.isfinite(phi))
    history = json.loads(history_text)
    assert isinstance(history, list) and history
    return phi, history


def compute_oracle(components, radii):
    """Same qualified signed-ring algorithm, fresh source; no observed velocities."""
    started = time.perf_counter()
    radii = validate_radii(radii)
    masses, knots = units.masses(components), ring.source_knots(components)
    assert masses and all(math.isfinite(m) and m > 0 for m in masses.values())
    assert all(r < ring.source_cutoff(components) for r in radii)
    checks, cases = [], []

    def check(name, error, tolerance):
        checks.append({'name': name, 'error': float(error), 'tolerance': float(tolerance),
                       'passed': bool(math.isfinite(error) and error <= tolerance)})

    for radius in radii:
        distance = float(np.min(abs(knots-radius)))
        assert distance > 1e-10, 'Prospective control radius coincides with source knot.'
        heights = [min(.2, distance/4)/2**i for i in range(3)]
        rows = []
        for height in heights:
            values = {str(order): ring.field(radius, height, components, order)
                      for order in ring.ORDERS}
            for key in ('gR_kms2_per_kpc', 'potential_kms2'):
                check(f'quadrature:{radius}:{height}:{key}',
                      ring.relative(values['48'][key], values['96'][key]), 1e-8)
            for name, part in values['96']['components'].items():
                check(f'mass:{radius}:{height}:{name}',
                    abs(part['quadrature_mass_Msun']+part['omitted_mass_Msun']-masses[name])/masses[name], 1e-9)
            rows.append({'z_kpc': height, 'orders': values})
        force = [r['orders']['96']['gR_kms2_per_kpc'] for r in rows]
        extrapolated = [2*force[i+1]-force[i] for i in (0, 1)]
        check(f'height:{radius}', ring.relative(*extrapolated), 1e-3)
        check(f'tail:{radius}', rows[-1]['orders']['96']['force_tail_bound_kms2_per_kpc']
              /max(1., abs(extrapolated[-1])), 1e-10)
        cases.append({'R_kpc': float(radius), 'nearest_knot_distance_kpc': distance,
            'component_masses_Msun': masses, 'heights': rows,
            'extrapolated_gR_kms2_per_kpc': extrapolated})
    return {'status': 'COMPLETE' if all(c['passed'] for c in checks) else 'FAILED',
        'cases': cases, 'checks': checks,
        'seconds': time.perf_counter()-started,
        'role': 'Fresh source-own Newtonian qualification; no observed rotation data.'}


def run_case(components, model, output_dir, freeze_sha256, n, extent,
             newtonian, control_radii, oracle, qualified_masses):
    """Full saved potential and fixed source-only control radii, never Vobs."""
    assert (n, extent, newtonian) in JOBS
    control_radii = validate_radii(control_radii)
    output_dir = Path(output_dir)
    assert output_dir.is_dir()
    case = identity(model, n, extent, newtonian)
    path = output_dir/(case+'.json')
    assert not path.exists(), 'Caller must authenticate existing completed case, never overwrite.'
    assert oracle['status'] == 'COMPLETE' and all(c['passed'] for c in oracle['checks'])
    assert list(control_radii) == [c['R_kpc'] for c in oracle['cases']]
    started = time.perf_counter()
    masses = units.masses(components)
    assert set(masses) == set(qualified_masses)
    assert all(m > 0 and math.isfinite(m) for m in masses.values())
    source_error = max(abs(masses[k]/qualified_masses[k]-1) for k in masses)
    assert source_error <= 1e-13
    mass = math.fsum(masses.values())
    q = units.G_KPC_KMS2_MSUN*mass/units.A0_KMS2_KPC
    geometry = edges, centers, _ = disk.mesh(n, extent)
    assert all(centers[0] <= r <= centers[-1] for r in control_radii)
    sr = np.sqrt(extent**2+centers**2)
    boundary_potential = disk.spherical_potential(sr, q, newtonian=newtonian)
    tangent = (q/sr**2 if newtonian else law.inverse(q/sr**2))*centers/sr
    bottom = units.bottom_flux(edges, components)
    boundary = (boundary_potential, boundary_potential.copy(), tangent, tangent, bottom)
    checkpoint = output_dir/(case+'.checkpoint.npz')
    history = None
    if checkpoint.exists():
        initial, history = load_checkpoint(checkpoint, case, freeze_sha256, n)
        print(json.dumps({'resume_checkpoint': case, 'completed_outer': len(history)}), flush=True)
    else:
        rr, zz = np.meshgrid(centers, centers, indexing='ij')
        s = np.sqrt(rr*rr+(zz+5.)**2)
        initial = q*(1-1/s) if newtonian else math.sqrt(q)*np.log(s)
    phi, radial, history, converged = disk.solve(geometry, boundary, initial, newtonian,
        checkpoint=checkpoint_writer(checkpoint, case, freeze_sha256), history_start=history)
    radii = np.asarray(control_radii, dtype=float)
    force = np.interp(radii, centers, radial)
    controls = []
    for radius, value in zip(radii, force):
        speed2 = float(radius*units.A0_KMS2_KPC*value)
        controls.append({'R_kpc': float(radius), 'radial_force_a0': float(value),
            'velocity_squared_kms2': speed2,
            'circular_speed_kms': math.sqrt(speed2) if speed2 >= 0 else None})
    expected = math.fsum(float(2*math.pi*1e6*p.integral(0., extent)) for p in components.values())
    actual = float(np.sum(bottom))*units.A0_KMS2_KPC/units.G_KPC_KMS2_MSUN
    mass_error = abs(actual-expected)/expected
    checks = {'converged': bool(converged), 'source_mass': mass_error <= 1e-13,
        'qualified_source_identity': source_error <= 1e-13,
        'flux_balance': history[-1].get('flux_balance_error', math.inf) <= 2e-6,
        'unclipped': history[-1].get('clipped_faces', -1) == 0,
        'nonlinear_residual': history[-1].get('nonlinear_error', math.inf) <= 1e-9}
    numerical = {}
    if not newtonian and (n == 512 or extent == 1023):
        old = authenticated(output_dir/(identity(model, 256, 255, False)+'.json'), freeze_sha256)
        assert old['case'] == identity(model, 256, 255, False) and all(old['checks'].values())
        assert [r['R_kpc'] for r in old['source_only_controls']] == list(control_radii)
        previous = np.array([r['radial_force_a0'] for r in old['source_only_controls']])
        change = abs(force-previous)/np.maximum(abs(force), 1e-12)
        name = 'mesh_refinement' if n == 512 else 'remote_domain'
        numerical[name+'_max_control_force_change'] = float(np.max(change))
        numerical[name+'_all_control_force_changes'] = change.tolist()
        checks[name] = bool(np.max(change) < .02)
    ring_comparison = []
    if newtonian:
        for row, value in zip(oracle['cases'], force):
            reference = row['extrapolated_gR_kms2_per_kpc'][-1]
            height_error = abs(reference-row['extrapolated_gR_kms2_per_kpc'][0])
            orders = row['heights'][-1]['orders']
            quadrature_error = abs(orders['96']['gR_kms2_per_kpc']-orders['48']['gR_kms2_per_kpc'])
            calculated = float(value)*units.A0_KMS2_KPC
            allowance = .02*max(1., abs(reference))+height_error+quadrature_error
            discrepancy = abs(calculated-reference)
            ring_comparison.append({'R_kpc': row['R_kpc'],
                'grid_gR_kms2_per_kpc': calculated, 'reference_gR_kms2_per_kpc': reference,
                'height_extrapolation_difference': height_error,
                'quadrature_difference': quadrature_error, 'absolute_discrepancy': discrepancy,
                'numerical_allowance': allowance, 'passed': discrepancy <= allowance})
        checks['independent_newtonian_force'] = all(r['passed'] for r in ring_comparison)
    payload = {'case': case, 'model': model, 'N': n, 'extent': extent,
        'newtonian': newtonian, 'component_masses_Msun': masses,
        'omitted_mass_beyond_boundary_Msun': mass-expected,
        'source_mass_relative_error': mass_error, 'checks': checks, 'history': history,
        'source_only_controls': controls, 'numerical_comparison': numerical,
        'independent_newtonian_force_comparison': ring_comparison,
        'radii': centers.tolist(), 'radial_force_a0': radial.tolist(), 'phi': phi.tolist(),
        'law_parameters': {'a0_kms2_kpc': units.A0_KMS2_KPC, 'ratio': law.RATIO},
        'seconds_this_invocation': time.perf_counter()-started,
        'peak_self_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'role': 'Prospective source-defined field, no target rotation samples read by this code.'}
    publish(path, payload, freeze_sha256)
    print(json.dumps({'completed_transfer_case': case, 'checks': checks,
                     'seconds': payload['seconds_this_invocation']}), flush=True)
    return payload
