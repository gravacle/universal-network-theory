"""Additive numerical repair: original disk operator, verified-residual PCG."""
import os
import sys

sys.dont_write_bytecode = True
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
            'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'

import copy
import math
import numpy as np
import axisymmetric_disk as original

# All mesh, boundary integration and physical face coefficients are unchanged.
mesh = original.mesh
spherical_potential = original.spherical_potential
operator = original.operator


def pcg(apply, diagonal, rhs, initial):
    """Same diagonal preconditioner; larger cap and true residual acceptance.

    Restart only when the recurrence claims convergence but the explicitly
    recomputed residual does not. No field/source/tolerance is changed.
    """
    x = initial.copy()
    norm_rhs = float(np.linalg.norm(rhs))
    if not math.isfinite(norm_rhs) or norm_rhs <= 0:
        raise ValueError('This benchmark requires a finite nonzero RHS norm')
    if not np.all(np.isfinite(diagonal)) or not np.all(diagonal > 0):
        raise ValueError('PCG requires a finite positive diagonal')
    cap = 32 * len(x) + 100
    residual = rhs - apply(x)
    recurrence_error = float(np.linalg.norm(residual)) / norm_rhs
    true_checks, restarts = 1, 0

    def finish(iterations, reason):
        nonlocal true_checks
        true_residual = rhs - apply(x)
        true_error = float(np.linalg.norm(true_residual)) / norm_rhs
        true_checks += 1
        ok = math.isfinite(true_error) and true_error <= 1e-12
        details = dict(maximum_iterations=cap,
                       recurrence_error=recurrence_error if math.isfinite(recurrence_error) else None,
                       true_residual_checks=true_checks, residual_restarts=restarts,
                       exit_reason=reason)
        return x, iterations, true_error if math.isfinite(true_error) else None, ok, details

    if recurrence_error <= 1e-12:
        return finish(0, 'initial_residual')
    z = residual / diagonal
    direction = z.copy()
    rz = float(np.sum(residual * z))
    for iteration in range(1, cap + 1):
        ad = apply(direction)
        denominator = float(np.sum(direction * ad))
        if (not math.isfinite(denominator) or denominator <= 0
                or not math.isfinite(rz) or rz <= 0):
            return finish(iteration - 1, 'nonpositive_or_nonfinite_pcg_scalar')
        alpha = rz / denominator
        x += alpha * direction
        residual -= alpha * ad
        recurrence_error = float(np.linalg.norm(residual)) / norm_rhs
        if not math.isfinite(recurrence_error):
            return finish(iteration, 'nonfinite_recurrence')
        if recurrence_error <= 1e-12:
            true_residual = rhs - apply(x)
            true_error = float(np.linalg.norm(true_residual)) / norm_rhs
            true_checks += 1
            if math.isfinite(true_error) and true_error <= 1e-12:
                return finish(iteration, 'verified_convergence')
            if not math.isfinite(true_error):
                return finish(iteration, 'nonfinite_true_residual')
            # Rebuild the Krylov direction; never continue with a replaced
            # residual and a stale conjugacy coefficient.
            residual = true_residual
            recurrence_error = true_error
            z = residual / diagonal
            direction = z.copy()
            rz = float(np.sum(residual * z))
            restarts += 1
            continue
        z = residual / diagonal
        next_rz = float(np.sum(residual * z))
        direction = z + (next_rz / rz) * direction
        rz = next_rz
    return finish(cap, 'iteration_allowance_exhausted')


def solve(geometry, boundary, initial, newtonian=False, checkpoint=None,
          history_start=None):
    """Original Picard procedure with the V002 linear solver.

    Optional checkpoint(phi_copy, history_copy) is called after
    completed nonlinear updates only. Caller owns source validation and
    durable publication; the benchmark supplies no callback or new writes.
    A caller can restart from validated saved phi/history as `initial` and
    `history_start`; the 300-outer-iteration allowance includes that history.
    """
    phi = initial.copy()
    pr, pz, tr, tz, bottom = boundary
    mass = float(np.sum(bottom))
    history = copy.deepcopy(history_start) if history_start is not None else []
    if len(history) > 300 or any(row.get('outer') != index or row.get('linear_failed', False)
                                 for index, row in enumerate(history)):
        raise ValueError('Resume history must contain sequential completed outer updates')
    success = False
    if history:
        # Authentication belongs to the caller; convergence is recomputed
        # from the actual supplied field, not inherited from a stored flag.
        apply, diagonal, rhs, clipped, kr, kz = operator(phi, geometry, boundary, newtonian)
        residual = float(np.linalg.norm(apply(phi) - rhs) / np.linalg.norm(rhs))
        outgoing = float(np.sum(kr[-1] * (pr - phi[-1]))
                         + np.sum(kz[:, -1] * (pz - phi[:, -1])))
        balance = abs(outgoing - mass) / mass
        success = residual <= 1e-9 and clipped == 0 and balance <= 2e-6
    for outer in range(len(history), 300):
        if success:
            break
        apply, diagonal, rhs, _, _, _ = operator(phi, geometry, boundary, newtonian)
        candidate, inner, inner_error, ok, details = pcg(apply, diagonal, rhs, phi)
        if not ok:
            history.append(dict(outer=outer, inner=inner, inner_error=inner_error,
                                linear_failed=True, pcg=details))
            break
        phi = candidate if newtonian else .4 * phi + .6 * candidate
        apply, diagonal, rhs, clipped, kr, kz = operator(phi, geometry, boundary, newtonian)
        residual = float(np.linalg.norm(apply(phi) - rhs) / np.linalg.norm(rhs))
        outgoing = float(np.sum(kr[-1] * (pr - phi[-1]))
                         + np.sum(kz[:, -1] * (pz - phi[:, -1])))
        balance = abs(outgoing - mass) / mass
        history.append(dict(outer=outer, inner=inner, inner_error=inner_error,
                            nonlinear_error=residual, flux_balance_error=balance,
                            clipped_faces=clipped, pcg=details))
        if checkpoint is not None:
            checkpoint(phi.copy(), copy.deepcopy(history))
        if residual <= 1e-9 and clipped == 0 and balance <= 2e-6:
            success = True
            break
    _, c, _ = geometry
    disk_phi = phi[:, 0] - c[0] * (phi[:, 1] - phi[:, 0]) / (c[1] - c[0])
    radial = np.gradient(disk_phi, c, edge_order=2)
    return phi, radial, history, success
