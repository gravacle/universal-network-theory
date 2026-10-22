"""INERT binding of one supplied nonzero-mode density increment through the cached
native full-ten response, then the lagged lapse feedback; UNT task 0449, c2v001.

Task 0449 file sha256 b7e1cdc3cd4a45d6c4dd36136ff9f720c7a5362adc683560f4f0775dda675cc4.
Binding operations, in order:
  1. deltaJ0 = supplied 0445 contraction(rho_m on R, z, RdRdz; mode; signed waves;
     READY J_n provider). Status COMPLETE is required; a partial deltaJ0 is never used.
  2. delta_prepared = weighted_unit_response * deltaJ0[:, None, None], exactly once.
     Root layout (nk, 10, 1): axis 1 = ten field components (index 0 = lapse
     perturbation n); axis 2 = the single source column, the response to the unit
     lapse source e_n (source coordinate 0). No extra minus, c^2, 2pi, R, volume
     or dk weight. Increment around the supplied base (F2): nothing subtracted,
     nothing re-added.
  3. Supplied fixed-xy prepare_line/evaluate_line for base and increment at every
     (R_i, phi_j, z_ijl); x = R cos(phi), y = R sin(phi); zero boundary
     perturbations (increment: binding; base: root v005 convention). Complex
     full-ten fields and Cartesian jets; finite and caller-tolerance reality
     checks at every point, all BEFORE any real lapse quantity is derived.
  4. Nb = 1 + Re n_base. LINEAR: dPhi = c^2 dn / Nb,
     grad dPhi = c^2 (grad dn / Nb - dn grad nb / Nb^2), Nb > 0 required.
     Optional, SEPARATELY labelled FINITE LOG DIFFERENCE: c^2 log1p(dn / Nb),
     c^2 (Nb grad dn - dn grad nb) / (Nb (Nb + dn)), Nb + dn > 0 required;
     never substituted into the linear operator.
  5. Every supplied angle is evaluated; full angular arrays are returned. No DFT
     or modal projection is made here (root chooses the modal interpretation).
  6. Completeness and finite checks, supplied provenance, source and field
     increments. No solve, regularization, clipping, renormalization or acceptance.
numpy + stdlib only; no BLAS products and no einsum in this file (the reused line
module uses einsum optimize=False); no floating-point warning suppression (the
caller's numpy.errstate governs); no I/O; fail-closed dicts; definitions only at import.
"""
import math
import numbers
from collections.abc import Mapping

import numpy as np


TASK_0449_SHA256 = 'b7e1cdc3cd4a45d6c4dd36136ff9f720c7a5362adc683560f4f0775dda675cc4'
FIELD_COMPONENTS = 10
LAPSE_FIELD_INDEX = 0       # field axis 1: lapse perturbation n (root v005: N = 1 + f[0].real)
LAPSE_SOURCE_COLUMN = 0     # source coordinate 0 = the single stored unit column e_n (root v004)

CONVENTION = dict(
    task_sha256=TASK_0449_SHA256,
    unit_layout=('weighted_responses (nk, 10, 1): axis 1 ten field components, index 0 = '
                 'lapse perturbation n; axis 2 length 1 = response to the unit lapse source '
                 'e_n in source coordinate 0 (root v004 stores and multiplies it this way)'),
    source_increment=('delta_prepared = weighted_unit_response * deltaJ0_J[:, None, None], '
                      'once; equal to root v004 unit * delta[:, 0:1, :] with delta[:, 0, 0] = '
                      'deltaJ0_J; no extra minus, c^2, 2pi, R, volume or dk weight'),
    base=('supplied base prepared response (root F2 refreshed total); the increment is added '
          'around it by linearity of the line read; no m0 gas subtracted, no reference re-added'),
    line_points=('x = R cos(phi), y = R sin(phi) per (R_i, phi_j); prepare_line once per point '
                 'and field; evaluate_line at each z_ijl; zero boundary perturbations, shapes '
                 '(1,10,1), (1,10,1,3), (1,10,1,3,3)'),
    reality=('per point and per field/gradient/hessian: finite, and |Im| <= atol + rtol |Re| '
             'elementwise with finite bound (root v005 form); base and increment use their own '
             'caller tolerances; a failure stops the call, nothing is averaged'),
    linear=('LINEAR: Nb = 1 + nb, deltaPhi = c^2 * (dn / Nb), grad = c^2 * (grad_dn / Nb - '
            'dn * grad_nb / (Nb * Nb)); Nb > 0 required'),
    log_difference=('FINITE LOG DIFFERENCE (separate, optional): c^2 * log1p(dn / Nb), '
                    'c^2 * (Nb * grad_dn - dn * grad_nb) / (Nb * (Nb + dn)); Nb + dn > 0 and '
                    'dn / Nb > -1 required; never used in the linear result'),
    cylindrical=('from Cartesian (gx, gy, gz): R = gx cos(phi) + gy sin(phi), phi = -gx sin(phi) '
                 '+ gy cos(phi) (physical, (1/R) d/dphi), z = gz; component order (R, phi, z)'),
    units=('fields dimensionless, gradient 1/m, hessian 1/m^2, deltaJ0 J, deltaPhi m^2 s^-2, '
           'grad deltaPhi m s^-2'),
    angles='every supplied angle evaluated; no DFT, modal projection or angular average',
    excluded='solve, regularization, clipping, renormalization, acceptance, file I/O')


class _InvalidInput(ValueError):
    """Input contract violation detected before any evaluation."""


class _FailClosed(ValueError):
    """Runtime contract violation during the binding."""


def _real_array(value, name, ndim):
    array = np.asarray(value)
    kind = array.dtype.kind
    if kind not in 'fiu' or (kind == 'f' and array.dtype.itemsize > 8):
        raise _InvalidInput(name + ': real float64-representable dtype required, got '
                            + str(array.dtype))
    if array.ndim != ndim:
        raise _InvalidInput(name + ': %d-D array required, got shape %s' % (ndim, array.shape))
    array = np.array(array, dtype=np.float64, copy=True)
    if not np.all(np.isfinite(array)):
        raise _InvalidInput(name + ': finite values required')
    return array


def _response_packet(packet, name, waves):
    if not isinstance(packet, Mapping) or 'wavevectors' not in packet \
            or 'weighted_responses' not in packet:
        raise _InvalidInput(name + ': mapping with wavevectors and weighted_responses required')
    stored = _real_array(packet['wavevectors'], name + "['wavevectors']", 2)
    if stored.shape != waves.shape or not np.array_equal(stored, waves):
        raise _InvalidInput(name + ': wavevectors must equal k_physical_inverse_m exactly, '
                                   'same signed order')
    raw = np.asarray(packet['weighted_responses'])
    kind = raw.dtype.kind
    if not ((kind == 'c' and raw.dtype.itemsize <= 16) or (kind == 'f' and raw.dtype.itemsize <= 8)):
        raise _InvalidInput(name + ': complex128/float64-representable weighted_responses '
                                   'required, got ' + str(raw.dtype))
    if raw.shape != (waves.shape[0], FIELD_COMPONENTS, 1):
        raise _InvalidInput(name + ': weighted_responses shape (nk, 10, 1) required (root '
                                   'layout), got ' + str(raw.shape))
    array = np.array(raw, dtype=np.complex128, copy=True)
    if not np.all(np.isfinite(array)):
        raise _InvalidInput(name + ': finite weighted_responses required')
    array.flags.writeable = False
    return array, str(raw.dtype)


def _tolerance(value, name):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, numbers.Real):
        raise _InvalidInput(name + ': real number required')
    value = float(value)
    if not (math.isfinite(value) and value >= 0.0):
        raise _InvalidInput(name + ': finite nonnegative value required')
    return value


def _validate(density_fourier, jn_provider, k_physical_inverse_m, unit_response,
              base_prepared, prepare_line, evaluate_line, eval_radius_m, eval_phi_rad,
              eval_z_m, c_m_s, tolerances, wave_chunk, position_chunk,
              include_log_difference, provenance):
    for name, item in (('density_fourier', density_fourier), ('prepare_line', prepare_line),
                       ('evaluate_line', evaluate_line)):
        if not callable(item):
            raise _InvalidInput(name + ': callable required')
    if not isinstance(jn_provider, Mapping) or jn_provider.get('status') != 'READY' \
            or not callable(jn_provider.get('bessel_jn')):
        raise _InvalidInput("jn_provider: provider dict with status 'READY' and callable "
                            'bessel_jn required')
    if type(include_log_difference) is not bool:
        raise _InvalidInput('include_log_difference: bool required')
    if not isinstance(provenance, Mapping):
        raise _InvalidInput('provenance: mapping required')
    for name, chunk in (('wave_chunk', wave_chunk), ('position_chunk', position_chunk)):
        if type(chunk) is not int or chunk < 1:
            raise _InvalidInput(name + ': positive int required (bool rejected)')
    if isinstance(c_m_s, (bool, np.bool_)) or not isinstance(c_m_s, numbers.Real):
        raise _InvalidInput('c_m_s: real number required')
    c = float(c_m_s)
    c_squared = c * c
    if not (math.isfinite(c) and c > 0.0 and math.isfinite(c_squared) and c_squared > 0.0):
        raise _InvalidInput('c_m_s: finite positive value with finite positive square required')
    tol = {name: _tolerance(value, name) for name, value in tolerances.items()}
    waves = _real_array(k_physical_inverse_m, 'k_physical_inverse_m', 2)
    if waves.shape[1:] != (3,) or waves.shape[0] < 1:
        raise _InvalidInput('k_physical_inverse_m: shape (nk, 3), nk >= 1 required')
    waves.flags.writeable = False
    unit, unit_dtype = _response_packet(unit_response, 'unit_response', waves)
    base, base_dtype = _response_packet(base_prepared, 'base_prepared', waves)
    radius = _real_array(eval_radius_m, 'eval_radius_m', 1)
    phi = _real_array(eval_phi_rad, 'eval_phi_rad', 1)
    height = _real_array(eval_z_m, 'eval_z_m', 3)
    if radius.shape[0] < 1 or np.any(radius <= 0.0):
        raise _InvalidInput('eval_radius_m: at least one strictly positive radius required')
    if phi.shape[0] < 1:
        raise _InvalidInput('eval_phi_rad: at least one angle required')
    if height.shape[:2] != (radius.shape[0], phi.shape[0]) or height.shape[2] < 1:
        raise _InvalidInput('eval_z_m: shape (n_radius, n_phi, n_z), n_z >= 1 required')
    return dict(c_squared=c_squared, tol=tol, waves=waves, unit=unit, base=base,
                unit_dtype=unit_dtype, base_dtype=base_dtype, radius=radius, phi=phi,
                height=height)


def _point_packet(packet, role):
    """(fields (10,), gradient (10,3), hessian (10,3,3)) complex of one line read."""
    if not isinstance(packet, Mapping):
        raise _FailClosed(role + ': evaluate_line must return a mapping')
    out = []
    for key, shape in (('fields', (1, 10, 1)), ('gradient', (1, 10, 1, 3)),
                       ('hessian', (1, 10, 1, 3, 3))):
        value = np.asarray(packet.get(key))
        if value.shape != shape or value.dtype != np.complex128:
            raise _FailClosed(role + ': evaluate_line ' + key + ' must be complex128 '
                              + str(shape) + ', got ' + str(value.dtype) + ' ' + str(value.shape))
        out.append(value[0, :, 0])
    return out


def _reality(value, atol, rtol):
    """(passed, max |Im|, max(|Im| - bound)); passed requires finite value and bound."""
    if not np.all(np.isfinite(value)):
        return False, math.nan, math.nan
    magnitude = np.abs(value.imag)
    bound = atol + rtol * np.abs(value.real)
    if not np.all(np.isfinite(bound)):
        return False, math.nan, math.nan
    excess = magnitude - bound
    return (not np.any(magnitude > bound)), float(np.max(magnitude)), float(np.max(excess))


def _cylindrical(gradient, cos_phi, sin_phi):
    gx = gradient[..., 0]
    gy = gradient[..., 1]
    return np.stack((gx * cos_phi + gy * sin_phi, -gx * sin_phi + gy * cos_phi,
                     gradient[..., 2]), axis=-1)


def nonzero_cached_feedback(*, density_fourier, jn_provider, radius_m, z_m, weights_RdRdz_m3,
                            rho_mode_kg_m3, mode, k_physical_inverse_m, unit_response,
                            base_prepared, prepare_line, evaluate_line, eval_radius_m,
                            eval_phi_rad, eval_z_m, c_m_s, base_reality_atol,
                            base_reality_rtol, increment_reality_atol,
                            increment_reality_rtol, wave_chunk, position_chunk,
                            include_log_difference, provenance):
    """Bind one supplied density harmonic through the cached full-ten response.

    Returns a fail-closed dict. status 'COMPLETE' -> every payload key is set.
    'INVALID_INPUT' -> nothing evaluated (also when the 0445 callable reports
    INVALID_INPUT). 'FAILED_CLOSED' -> payload keys None; 'retained' holds
    everything computed so far (point_mask marks evaluated points). A
    non-Exception interruption is re-raised after the same retained dict (status
    'INTERRUPTED') is attached to it as attribute unt0449_retained_result.
    """
    tolerances = dict(base_reality_atol=base_reality_atol, base_reality_rtol=base_reality_rtol,
                      increment_reality_atol=increment_reality_atol,
                      increment_reality_rtol=increment_reality_rtol)
    try:
        v = _validate(density_fourier, jn_provider, k_physical_inverse_m, unit_response,
                      base_prepared, prepare_line, evaluate_line, eval_radius_m, eval_phi_rad,
                      eval_z_m, c_m_s, tolerances, wave_chunk, position_chunk,
                      include_log_difference, provenance)
    except Exception as exc:  # fail closed: nothing evaluated
        return dict(status='INVALID_INPUT', complete=False, reason=str(exc),
                    failure_stage='validation', exception_type=type(exc).__name__,
                    convention=CONVENTION, retained=None)

    waves, unit, base, tol = v['waves'], v['unit'], v['base'], v['tol']
    radius, phi, height, c_squared = v['radius'], v['phi'], v['height'], v['c_squared']
    nk = waves.shape[0]
    n_radius, n_phi, n_z = height.shape
    grid = (n_radius, n_phi, n_z)
    uniform = [2 * math.pi * j / n_phi for j in range(n_phi)]
    summary = dict(
        mode=mode, waves=nk,
        unit_weighted_responses_dtype=v['unit_dtype'], base_weighted_responses_dtype=v['base_dtype'],
        layout='(nk, 10, 1) for unit, base and delta_prepared',
        eval_grid=grid, eval_radius_m=radius, eval_phi_rad=phi, eval_z_m=height,
        angles_equal_2pi_j_over_n=bool(np.array_equal(phi, np.asarray(uniform))),
        c_m_s=float(c_m_s), tolerances=tol, wave_chunk=wave_chunk,
        position_chunk=position_chunk, include_log_difference=include_log_difference,
        boundary='zero perturbations for base and increment')
    provenance_copy = dict(provenance)

    work = dict(density_fourier_result=None, deltaJ0_J=None, delta_prepared=None,
                base_line=None, increment_line=None, point_mask=np.zeros(grid, dtype=bool),
                lapse=None, linear=None, log_difference=None)
    checks = dict(density_fourier_complete=False, deltaJ0_finite=False,
                  delta_prepared_finite=False, all_points_finite_and_real=False,
                  lapse_inputs_finite_Nb_positive=False, linear_finite=False,
                  log_difference_finite=(None if not include_log_difference else False))
    tally = dict(line_prepare_calls=0, line_evaluate_calls=0)
    reality = {role + '_' + kind: dict(max_abs_imag=None, max_excess=None, points_checked=0)
               for role in ('base', 'increment') for kind in ('fields', 'gradient', 'hessian')}
    failure = dict(point=None, check=None)
    stage = 'density_fourier'

    def finish(status, exc):
        mask = work['point_mask']
        payload = {key: value for key, value in work.items()}
        complete = status == 'COMPLETE'
        density = work['density_fourier_result']
        result = dict(
            status=status, complete=complete, reason=None, failure_stage=None,
            exception_type=None, failure_point=failure['point'], failure_check=failure['check'],
            provenance=provenance_copy, inputs=summary,
            jn_provider_metadata=(dict(jn_provider['metadata']) if isinstance(
                jn_provider.get('metadata'), Mapping) else None),
            completeness=dict(
                density_fourier_status=(density.get('status') if isinstance(density, Mapping)
                                        else None),
                points_expected=n_radius * n_phi * n_z,
                points_evaluated=int(np.count_nonzero(mask)),
                all_points_evaluated=bool(np.all(mask)),
                line_prepare_calls_expected=2 * n_radius * n_phi,
                line_evaluate_calls_expected=2 * n_radius * n_phi * n_z,
                checks=dict(checks), **tally),
            reality=reality, convention=CONVENTION, retained=None)
        if complete:
            result.update(payload)
        else:
            result.update({key: None for key in payload})
            result['retained'] = payload
            result['reason'] = str(exc)
            result['failure_stage'] = stage
            result['exception_type'] = type(exc).__name__
        return result

    try:
        # Step 1: 0445 contraction with the READY provider; COMPLETE only.
        density = density_fourier(radius_m=radius_m, z_m=z_m, weights_RdRdz_m3=weights_RdRdz_m3,
                                  rho_mode_kg_m3=rho_mode_kg_m3, k_physical_inverse_m=waves,
                                  c_m_s=c_m_s, mode=mode, bessel_jn=jn_provider['bessel_jn'],
                                  wave_chunk=wave_chunk, position_chunk=position_chunk)
        work['density_fourier_result'] = density
        if isinstance(density, Mapping) and density.get('status') == 'INVALID_INPUT':
            result = finish('INVALID_INPUT', _InvalidInput(
                '0445 contraction INVALID_INPUT: ' + str(density.get('reason'))))
            result['failure_stage'] = 'density_fourier_validation'
            return result
        if not isinstance(density, Mapping) or density.get('status') != 'COMPLETE' \
                or density.get('complete') is not True:
            raise _FailClosed('0445 contraction not COMPLETE (status %r); partial deltaJ0 '
                              'never consumed' % (density.get('status')
                                                  if isinstance(density, Mapping) else None,))
        counts = density.get('counts') or {}
        mask0445 = np.asarray(density.get('retained_wave_mask'))
        if counts.get('waves') != nk or counts.get('mode') != mode \
                or mask0445.shape != (nk,) or not np.all(mask0445):
            raise _FailClosed('0445 result counts/mode/wave mask do not match this call')
        delta_j = density.get('deltaJ0_J')
        if not isinstance(delta_j, np.ndarray) or delta_j.dtype != np.complex128 \
                or delta_j.shape != (nk,):
            raise _FailClosed('0445 deltaJ0_J must be complex128 (nk,)')
        checks['density_fourier_complete'] = True
        delta_j = delta_j.copy()
        if not np.all(np.isfinite(delta_j)):
            raise _FailClosed('nonfinite deltaJ0_J')
        delta_j.flags.writeable = False
        work['deltaJ0_J'] = delta_j
        checks['deltaJ0_finite'] = True

        # Step 2: the single multiplication by the cached weighted unit response.
        stage = 'delta_prepared'
        delta_prepared = unit * delta_j[:, None, None]
        if not np.all(np.isfinite(delta_prepared)):
            raise _FailClosed('nonfinite delta_prepared')
        delta_prepared.flags.writeable = False
        work['delta_prepared'] = dict(wavevectors=waves, weighted_responses=delta_prepared)
        checks['delta_prepared_finite'] = True

        # Step 3: reused fixed-xy line read for base and increment, zero boundary.
        stage = 'line_allocation'
        prepared = dict(base=dict(wavevectors=waves, weighted_responses=base),
                        increment=dict(wavevectors=waves, weighted_responses=delta_prepared))
        nan = complex(math.nan, math.nan)
        lines = {}
        for role in ('base', 'increment'):
            lines[role] = dict(
                fields=np.full(grid + (FIELD_COMPONENTS,), nan, dtype=np.complex128),
                gradient=np.full(grid + (FIELD_COMPONENTS, 3), nan, dtype=np.complex128),
                hessian=np.full(grid + (FIELD_COMPONENTS, 3, 3), nan, dtype=np.complex128))
            work[role + '_line'] = lines[role]
        zero = dict(boundary_fields=np.zeros((1, 10, 1), dtype=np.complex128),
                    boundary_gradient=np.zeros((1, 10, 1, 3), dtype=np.complex128),
                    boundary_hessian=np.zeros((1, 10, 1, 3, 3), dtype=np.complex128))
        for array in zero.values():
            array.flags.writeable = False
        for i in range(n_radius):
            for j in range(n_phi):
                stage = 'line_prepare'
                x_m = float(radius[i] * np.cos(phi[j]))
                y_m = float(radius[i] * np.sin(phi[j]))
                line = {}
                for role in ('base', 'increment'):
                    tally['line_prepare_calls'] += 1
                    line[role] = prepare_line(prepared=prepared[role], x_m=x_m, y_m=y_m)
                for l in range(n_z):
                    read = {}
                    for role in ('base', 'increment'):
                        stage = 'line_evaluate'
                        tally['line_evaluate_calls'] += 1
                        packet = evaluate_line(line=line[role], z_m=float(height[i, j, l]), **zero)
                        stage = 'point_checks'
                        read[role] = _point_packet(packet, role)
                        for kind, value in zip(('fields', 'gradient', 'hessian'), read[role]):
                            passed, imag, excess = _reality(
                                value, tol[role + '_reality_atol'], tol[role + '_reality_rtol'])
                            entry = reality[role + '_' + kind]
                            if not passed:
                                failure['point'] = (i, j, l)
                                failure['check'] = dict(role=role, kind=kind, max_abs_imag=imag,
                                                        max_excess=excess)
                                raise _FailClosed('nonfinite or nonreal %s %s at point %s'
                                                  % (role, kind, (i, j, l)))
                            if entry['points_checked'] == 0:
                                entry['max_abs_imag'], entry['max_excess'] = imag, excess
                            else:
                                entry['max_abs_imag'] = max(entry['max_abs_imag'], imag)
                                entry['max_excess'] = max(entry['max_excess'], excess)
                            entry['points_checked'] += 1
                    for role in ('base', 'increment'):
                        for kind, value in zip(('fields', 'gradient', 'hessian'), read[role]):
                            lines[role][kind][i, j, l] = value
                    work['point_mask'][i, j, l] = True
        checks['all_points_finite_and_real'] = True

        # Step 4: real lapse quantities, derived only after every point passed.
        stage = 'lapse_inputs'
        nb = lines['base']['fields'][..., LAPSE_FIELD_INDEX].real.copy()
        grad_nb = lines['base']['gradient'][..., LAPSE_FIELD_INDEX, :].real.copy()
        dn = lines['increment']['fields'][..., LAPSE_FIELD_INDEX].real.copy()
        grad_dn = lines['increment']['gradient'][..., LAPSE_FIELD_INDEX, :].real.copy()
        lapse_base = 1.0 + nb
        if not all(np.all(np.isfinite(a)) for a in (nb, grad_nb, dn, grad_dn, lapse_base)):
            raise _FailClosed('nonfinite real lapse inputs')
        work['lapse'] = dict(nb=nb, grad_nb_cartesian=grad_nb, dn=dn, grad_dn_cartesian=grad_dn,
                             Nb=lapse_base)
        if np.any(~(lapse_base > 0.0)):
            raise _FailClosed('Nb = 1 + nb must be > 0 at every point; %d points fail'
                              % int(np.count_nonzero(~(lapse_base > 0.0))))
        checks['lapse_inputs_finite_Nb_positive'] = True
        cos_phi = np.cos(phi)[None, :, None]
        sin_phi = np.sin(phi)[None, :, None]
        nb3 = lapse_base[..., None]

        stage = 'linear_feedback'
        delta_phi = c_squared * (dn / lapse_base)
        grad_delta_phi = c_squared * (grad_dn / nb3 - dn[..., None] * grad_nb / (nb3 * nb3))
        cylindrical = _cylindrical(grad_delta_phi, cos_phi, sin_phi)
        if not all(np.all(np.isfinite(a)) for a in (delta_phi, grad_delta_phi, cylindrical)):
            raise _FailClosed('nonfinite linear lapse feedback')
        work['linear'] = dict(
            label='LINEAR deltaPhi = c^2 dn/Nb; grad = c^2 (grad dn/Nb - dn grad nb/Nb^2)',
            deltaPhi_m2_s2=delta_phi, grad_deltaPhi_cartesian_m_s2=grad_delta_phi,
            grad_deltaPhi_cylindrical_R_phi_z_m_s2=cylindrical)
        checks['linear_finite'] = True

        if include_log_difference:
            stage = 'log_difference'
            total = lapse_base + dn
            ratio = dn / lapse_base
            if np.any(~(total > 0.0)) or np.any(~(ratio > -1.0)):
                raise _FailClosed('finite log difference needs Nb + dn > 0 and dn/Nb > -1; '
                                  '%d points fail' % int(np.count_nonzero(
                                      ~(total > 0.0) | ~(ratio > -1.0))))
            log_phi = c_squared * np.log1p(ratio)
            grad_log = c_squared * (nb3 * grad_dn - dn[..., None] * grad_nb) / (nb3 * total[..., None])
            cylindrical_log = _cylindrical(grad_log, cos_phi, sin_phi)
            if not all(np.all(np.isfinite(a)) for a in (log_phi, grad_log, cylindrical_log)):
                raise _FailClosed('nonfinite finite log difference')
            work['log_difference'] = dict(
                label=('FINITE LOG DIFFERENCE, separate from and never substituted into the '
                       'linear operator: c^2 log1p(dn/Nb); c^2 (Nb grad dn - dn grad nb)/'
                       '(Nb (Nb + dn))'),
                deltaPhi_m2_s2=log_phi, grad_deltaPhi_cartesian_m_s2=grad_log,
                grad_deltaPhi_cylindrical_R_phi_z_m_s2=cylindrical_log)
            checks['log_difference_finite'] = True
        stage = 'complete'
    except Exception as exc:  # FloatingPointError under caller errstate included
        return finish('FAILED_CLOSED', exc)
    except BaseException as exc:
        try:
            exc.unt0449_retained_result = finish('INTERRUPTED', exc)
        except Exception:
            pass
        raise
    return finish('COMPLETE', None)
