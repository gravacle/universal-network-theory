"""Saved-endpoint compression-source comparison; NO trajectory integration.

Rebuild each original constrained preparation only, reconstruct canonical
phi_R from the saved mixed-p state, and call polar_compare_v003.comparison
UNCHANGED. Its complete-state/CHANGE floors, cubic interpolation, interior
edge exclusion, inner10L domain and 1e-3 gate remain exactly those saved.
Gravity is its existing coordinate acceleration N**2*(N_R/N)/A**2;
theta=-chi/cTheta. These are not automatically a rotation curve or a
stationary galaxy. Both initial and endpoint profiles are retained.

The additional Raychaudhuri audit uses complete compression stresses and
kinematic expansion, full material derivative and the prior two tangent
increments (1e-7,5e-8)*tdyn. Its prospective relative numerical gate is
1e-3. It is one additional identity, NOT complete-constraint certification.
No orbit/history is advanced by those algebraic tangent evaluations.

The source is the declared positive ordinary, initially circular 5 kpc
truncated Plummer preparation, kappa=1e-7, with300L ordinary compensation
and evolving cosmic boundary. No native formation, adjusted halo, incoming
phase fit or old cosmological-fit inheritance is claimed. Equal coordinate
compensation does not cancel all canonical rest, kinetic or field energy.

The central early-time Taylor estimate is a diagnostic, never an event
acceptance gate: neglect H, use weak metric and short sound travel. Four
fixed nodes extrapolate in R**2; pointwise branch values remain separate
from that extrapolation. No negative-charge continuation is attempted.
CLI: lefttag righttag outputtag. Output is exclusive; no calibration rerun.
"""

from pathlib import Path
import argparse
import hashlib
import json
import math
import re
import time
import numpy as np
import invariant_clock_compression_source_test_v002 as producer
import invariant_clock_polar_compare_v003 as frozen

ROOT = Path(__file__).resolve().parent
MAXIMUM = lambda x: float(np.max(np.abs(x)))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tag_name(value):
    if not re.fullmatch(r'[A-Za-z0-9_-]+', value):
        raise ValueError('tags must contain only letters, digits, underscore or hyphen')
    return value


def central_even(r, values):
    """Four-point interpolatory R**2 center value, not a fitted physical law."""
    if len(r) < 4:
        raise ValueError('four points required for the fixed central extrapolation')
    x = (r[:4]/r[3])**2
    return math.fsum(float(values[j])*math.prod(-x[k]/(x[j]-x[k])
                     for k in range(4) if k != j) for j in range(4))


def load_pair(tag):
    prefix = 'INVARIANT_CLOCK_COMPRESSION_SOURCE_'+tag_name(tag)
    result_path = ROOT/(prefix+'_RESULT.json')
    checkpoint_path = ROOT/(prefix+'_CHECKPOINT.json')
    result = json.loads(result_path.read_text())
    checkpoint = json.loads(checkpoint_path.read_text())
    if result['hashes'] != checkpoint['hashes'] or result['args'] != checkpoint['args']:
        raise ValueError('result/checkpoint input identity mismatch')
    if result['steps'] != checkpoint['step'] or result['dt'] != checkpoint['dt']:
        raise ValueError('result/checkpoint accepted-time mismatch')
    if 'attempted_step' not in checkpoint:
        raise ValueError('only repaired V002 accepted-step checkpoints are supported')
    if result['ordinary_flux_integral'] != checkpoint['ordinary_flux_integral']:
        raise ValueError('result/checkpoint ordinary-flux mismatch')
    expected_producer = str(Path(producer.__file__).resolve())
    if expected_producer not in result['hashes']:
        raise ValueError('checkpoint is not from the declared parity source producer')
    for name, expected in result['hashes'].items():
        path = Path(name)
        if not path.is_relative_to(ROOT) or sha(path) != expected:
            raise ValueError('changed or out-of-project input: '+name)
    return result, checkpoint, result_path, checkpoint_path


def profile(model, t, z, g):
    mask = model.mask
    canonical = z.copy()
    canonical[1] = g['phir']
    return dict(t=float(t), r=model.r[mask].tolist(),
                state=canonical[:, mask].tolist(),
                gravity=(g['N']**2*g['g']/g['A']**2)[mask].tolist(),
                theta=(-g['chi']/model.cTheta)[mask].tolist())


def invariants(model, t, z):
    dz, g = model.rhs(t, z, True)
    r, A, N, sig, c = model.r, g['A'], g['N'], g['sig'], g['c']
    sigdot = dz[0]/A-sig*g['adot']
    theta = ((g['adot']*c+sig*sigdot/c)/N
             +(model.divergence(sig)+g['g']*sig)/A)
    rho, Pr, Pt, momentum = (g[k] for k in
                            ('rho_total', 'Pr_total', 'Pt_total', 'j_total'))
    ricci = c*c*rho-2*c*sig*momentum+sig*sig*Pr+(-rho+Pr+2*Pt)/2
    shear = 2/3*(theta-3*sig/(A*r))**2
    return dz, g, dict(theta=theta, ricci=ricci, shear=shear)


def ray_check(model, t, z):
    warm = tuple(v.copy() for v in (model.Aguess, model.chiguess, model.chirguess))
    rows = []
    try:
        dz, g, inv = invariants(model, t, z)
        r, A, N, sig, c = model.r, g['A'], g['N'], g['sig'], g['c']
        mask = model.mask
        constraint = inv['theta']+g['chi']/model.cTheta
        theta_scale = max(MAXIMUM(inv['theta'][mask]), 1e-12)
        for factor in (1e-7, 5e-8):
            dt = factor*model.tdyn
            _, gp, vp = invariants(model, t+dt, z+dt*dz)
            _, gm, vm = invariants(model, t-dt, z-dt*dz)
            theta_t = (vp['theta']-vm['theta'])/(2*dt)
            divacc = (dz[0]*g['e']+z[0]*(gp['e']-gm['e'])/(2*dt))/(N*A)
            divacc += (model.divergence(c*g['e'])+g['g']*c*g['e'])/A
            material = c*theta_t/N+sig*model.derivative(inv['theta'])/A
            residual = material+inv['theta']**2/3+inv['shear']+inv['ricci']-divacc
            scale = max(MAXIMUM(inv['ricci'][mask]), MAXIMUM(material[mask]), 1e-12)
            error = MAXIMUM(residual[mask])/scale
            rows.append(dict(tangent_step=dt, relative_ray_error=error,
                prospective_gate=1e-3, passed=bool(error <= 1e-3),
                theta_constraint_relative=MAXIMUM(constraint[mask])/theta_scale,
                central_theta=central_even(r, inv['theta']),
                central_ricci=central_even(r, inv['ricci']),
                central_divacc=central_even(r, divacc),
                central_material_theta_derivative=central_even(r, material)))
        return dict(rows=rows, passed=all(row['passed'] for row in rows),
                    scope='additional identity only; no complete constraint badge')
    except (ValueError, FloatingPointError, OverflowError) as error:
        return dict(rows=rows, passed=False, error=type(error).__name__+': '+str(error),
                    scope='tangent diagnostic undefined; no branch extension attempted')
    finally:
        model.Aguess, model.chiguess, model.chirguess = warm


def rebuild(tag):
    result, checkpoint, result_path, checkpoint_path = load_pair(tag)
    old = producer.old
    cal = json.loads(old.oracle.CAL.read_text())
    saved = json.loads(old.oracle.base.SOURCE.read_text())
    saved['inherited'] = cal['fixed']
    reference = old.oracle.base.Model(saved, 1)
    boundary = old.Boundary(reference)
    model = producer.source.Polar(saved, result['args']['nodes'], result['args']['extent'],
                                  outer_callback=boundary)
    boundary.radius = model.r[-1]
    z0, preparation = old.initial(model, reference)  # Initial solve only.
    g0 = model.geometry(0., z0)
    z = np.asarray(checkpoint['state'], dtype=float)
    t = checkpoint['step']*checkpoint['dt']
    g = model.geometry(t, z)  # Saved state, no advance.
    profiles = dict(snapshots=[profile(model, 0., z0, g0), profile(model, t, z, g)])

    # Reconstruct analytic central profile normalization, NOT first-node peak.
    yy = model.r/model.L
    shape = (1+yy*yy)**-2.5*np.maximum(1-(yy/20)**2, 0)**4
    rho_c = 2*model.kappa*model.L/(model.massint@shape)[-1]
    mbar = model.bg0[3]
    F = model.Fcompression
    laprho = -15.06*rho_c/model.L**2
    lapPhi = rho_c/(2*F)
    cubic = model.C*model.cTheta*laprho/(12*model.KB*F)
    tau_estimate = central_even(model.r, g0['N'])*t
    taylor_quadratic = mbar*lapPhi*tau_estimate**2/2
    taylor_cubic = cubic*tau_estimate**3
    evacuation = (-mbar/cubic)**(1/3)
    central_m0, central_m = central_even(model.r, g0['m']), central_even(model.r, g['m'])
    taylor = dict(central_rho_profile_amplitude=float(rho_c), cosmic_m=float(mbar),
        laplacian_source_density=float(laprho), leading_laplacian_Phi=float(lapPhi),
        central_m_initial=central_m0, central_m_actual=central_m,
        central_delta_m_actual=central_m-central_m0,
        central_proper_time_estimate=tau_estimate,
        proper_time_convention='initial central lapse times coordinate t; no elapsed-time integral claimed',
        delta_m_quadratic=taylor_quadratic, delta_m_cubic=taylor_cubic,
        delta_m_Taylor=taylor_quadratic+taylor_cubic,
        central_m_Taylor=float(mbar+taylor_quadratic+taylor_cubic),
        cubic_evacuation_proper_time_estimate=float(evacuation),
        time_over_Taylor_evacuation=float(tau_estimate/evacuation),
        H_times_tau=float(model.bg0[5]*tau_estimate), tau_over_L=float(tau_estimate/model.L),
        assumptions='weak metric; H neglected locally; short sound travel; leading source-only Taylor terms',
        event_acceptance_gate=False, center_rule='fixed four-point cubic interpolation in R squared')

    rest = []
    for i, (ni, pi, energy) in enumerate(((4, 5, 'es'), (7, 8, 'eb'))):
        initial_rest = float(2*np.dot(model.volumes, z0[ni]))
        final_rest = float(2*np.dot(model.volumes, z[ni]))
        integrated_flux = float(checkpoint['ordinary_flux_integral'][i])
        balance = final_rest-initial_rest+integrated_flux
        rate, flux = model.rest_flux(z[ni], g['N']*z[pi]/(g['A']**2*g[energy]))
        rest.append(dict(population='supported' if i == 0 else 'background',
            initial=initial_rest, final=final_rest, integrated_outward_flux=integrated_flux,
            balance=balance, relative_balance=balance/initial_rest if initial_rest else None,
            instantaneous_flux_algebra=float(2*np.dot(model.volumes, rate)+2*flux[-1]),
            initial_normal_slice_particle_energy=float(2*np.dot(model.volumes, z0[ni]*g0[energy])),
            final_normal_slice_particle_energy=float(2*np.dot(model.volumes, z[ni]*g[energy])),
            energy_scope='ordinary slice energy, not total conserved gravitational/field energy'))

    bg = model.initial_background
    background_total_j = bg['j0']+bg['c']*bg['chir']/bg['A']
    margin = model.Q0*model.eps/((1+g['s'])*(math.sqrt(1+model.eps)+g['qr']))
    available = g['target']-g['sig']*g['DD']
    branch = dict(radius_over_L=(model.r/model.L).tolist(), m=g['m'].tolist(), s=g['s'].tolist(),
        available_positive_charge=available.tolist(),
        fixed_p_inverse=g['Mx'].tolist(), fixed_w_inverse_fraction=(g['inverse']/g['d']).tolist(),
        multiplier_denominator=g['multiplier']['denominator'].tolist(), upper_X_gap=margin.tolist(),
        pointwise_positive_m=bool(np.all(g['m'] > 0)),
        pointwise_nonnegative_s=bool(np.all(g['s'] >= 0)),
        pointwise_positive_available_charge=bool(np.all(available > 0)),
        smallest_m=float(np.min(g['m'])), smallest_m_radius_over_L=float(model.r[np.argmin(g['m'])]/model.L),
        note='extrapolated central m is NOT the pointwise branch criterion')
    record = dict(tag=tag, accepted_time=t, accepted_steps=checkpoint['step'],
        attempted_step=checkpoint['attempted_step'], producer_reason=result['reason'],
        producer_error=result['error'], producer_failed_controls=result.get('failed_numerical_controls', []),
        reconstructed_preparation=preparation, saved_preparation=result['preparation'],
        initial_background_momentum=dict(
            saved_metadata_scope='background_j_outer is OLD-sector j0, not complete compression flux',
            old_sector=float(bg['j0'][-1]), compression=float((bg['c']*bg['chir']/bg['A'])[-1]),
            total=float(background_total_j[-1]), actual_initial_total=float(g0['j_total'][-1]),
            actual_minus_background_total=float(g0['j_total'][-1]-background_total_j[-1])),
        Taylor=taylor, pointwise_branch=branch, ordinary_rest=rest,
        geometry_iteration=g['geometry_iteration'], profiles=profiles,
        ray=ray_check(model, t, z),
        receipt_hashes={str(result_path):sha(result_path), str(checkpoint_path):sha(checkpoint_path)})
    return record, model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('lefttag')
    parser.add_argument('righttag')
    parser.add_argument('outputtag')
    args = parser.parse_args()
    output = ROOT/('INVARIANT_CLOCK_COMPRESSION_COMPARE_'+tag_name(args.outputtag)+'_RESULT.json')
    if output.exists():
        raise FileExistsError(output)
    np.seterr(over='raise', invalid='raise', divide='raise')
    started = time.monotonic()
    left, _ = rebuild(tag_name(args.lefttag))
    right, model = rebuild(tag_name(args.righttag))
    comparison = frozen.comparison(left['profiles'], right['profiles'], model)
    comparison['field_order'] = ['u', 'phi_R', 'Z', 'cp', 'ns', 'ps', 'ell', 'nb', 'pb']
    comparison['definition'] = 'unaltered polar_compare_v003.comparison; complete state and CHANGE floors'
    result = dict(protocol=__doc__, comparison=comparison, left=left, right=right,
        comparison_and_ray_pass=bool(comparison['pass_gate'] and left['ray']['passed'] and right['ray']['passed']),
        trajectory_qualified=False,
        scope='one bounded comparison and extra identity; formation, full constraints, boundary/work and other axes remain distinct',
        elapsed_seconds=time.monotonic()-started,
        hashes={str(p):sha(p) for p in (Path(__file__), Path(producer.__file__),
                                       Path(frozen.__file__), Path(producer.old.__file__))})
    with output.open('x') as file:
        json.dump(result, file, indent=2, allow_nan=False)
    print(json.dumps(dict(comparison=comparison, left_ray=left['ray'], right_ray=right['ray'],
        left_Taylor=left['Taylor'], right_Taylor=right['Taylor'],
        comparison_and_ray_pass=result['comparison_and_ray_pass'],
        elapsed_seconds=result['elapsed_seconds'], result_sha256=sha(output)), allow_nan=False), flush=True)
    if not result['comparison_and_ray_pass']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
