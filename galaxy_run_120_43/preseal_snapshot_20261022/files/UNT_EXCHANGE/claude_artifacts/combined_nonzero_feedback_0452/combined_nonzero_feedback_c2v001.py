"""INERT combined binding of several supplied nonzero-mode density harmonics through ONE
cached native full-ten response evaluation, then the lagged lapse feedback; UNT task
0452, c2v001.

Task 0452 file sha256 2cb7cc47429d14803a71cf0acb0ec57407c4aed414998e08ee71fac967efe3e3.
Successor of the reviewed 0449 binding nonzero_cached_feedback_c2v001.py (sha256
1b4f129ff93698f951a537c1c59011fba93b75d70c6aa7c704a9992aa3f6bf95; distinct review
REVIEW_0449_V001.md sha256 68327d2bc23cb2e7e76d861b4d5533f1f3a75fb0346f491bf23efb8238b9a274).
0449 is neither modified nor imported. Its reviewed source-to-field stage is COPIED
here. Every region is marked: '[0449 Lx-Ly verbatim]' (byte-identical to those 0449
lines), '[0449 Lx-Ly adapted: ...]' (the stated edit only), or '[0452 new: ...]' (the
mode mapping, the per-mode loop and the single summation; no new force law).
Binding operations, in order:
  1. Modes: an explicit nonempty mapping {m: rho_m}; keys unique Python int m in 1..6
     (bool, numpy integer, float and other types rejected); every rho_m a complex (q,)
     coefficient array on the ONE common R, z, RdRdz roster. Modes are processed in
     ascending m whatever the mapping order. No m = 0 entry, no m0 source correction.
     Output metadata lists modes_included and modes_omitted (of 1..6); no single-mode
     tag is attached to the combined source.
  2. Per included m: deltaJ0_m = supplied, unchanged 0445 contraction(rho_m on R, z,
     RdRdz; m; the same validated read-only signed waves; READY J_n provider).
     COMPLETE, complete True, counts.waves == nk, counts.mode == m, full wave mask,
     complex128 (nk,), finite, and the wave array bitwise unchanged are required for
     EVERY mode. The first mode that fails stops the call before any summation; no
     partial total is formed; every per-mode result obtained (the failing one included)
     is retained.
  3. deltaJ0_total = left fold in ascending m: copy(deltaJ0_{m_1}); then for k = 2.. :
     total = total + deltaJ0_{m_k} (complex128 elementwise IEEE adds). Each per-mode
     array enters exactly once. One mode -> a copy of that mode's array (bitwise).
  4. [0449 step 2] delta_prepared = weighted_unit_response * deltaJ0_total[:, None, None],
     exactly once. Root layout (nk, 10, 1): axis 1 = ten field components (index 0 =
     lapse perturbation n); axis 2 = the single unit lapse source column e_n (source
     coordinate 0). No extra minus, c^2, 2pi, R, volume or dk weight. Increment around
     the supplied F2 base: nothing subtracted, nothing re-added, no base accumulation.
  5. [0449 step 3] Supplied fixed-xy prepare_line/evaluate_line for base and the TOTAL
     increment, ONCE per (R_i, phi_j) and per z_ijl (not per mode); x = R cos(phi),
     y = R sin(phi); zero boundary perturbations. Complex full-ten fields and Cartesian
     jets; finite and caller-tolerance reality checks at every point, all BEFORE any
     real lapse quantity is derived.
  6. [0449 step 4] Nb = 1 + Re n_base. LINEAR (the physical-iteration branch):
     dPhi = c^2 dn / Nb, grad dPhi = c^2 (grad dn / Nb - dn grad nb / Nb^2), Nb > 0.
     Optional, SEPARATELY labelled FINITE LOG DIFFERENCE only when the caller passes
     include_log_difference=True: c^2 log1p(dn / Nb), c^2 (Nb grad dn - dn grad nb) /
     (Nb (Nb + dn)), Nb + dn > 0; never substituted into the linear operator.
  7. [0449 steps 5-6] Every supplied angle evaluated, full angular arrays returned, no
     DFT or modal projection. Completeness and finite checks, provenance, per-mode and
     total source increments, field increment. No solve, regularization, clipping,
     renormalization or acceptance.
numpy + stdlib only; no BLAS products and no einsum in this file (the reused line
module uses einsum optimize=False); no floating-point warning suppression (the
caller's numpy.errstate governs); no I/O; fail-closed dicts; definitions only at import.
"""
# [0449 L32-36 verbatim]
import math
import numbers
from collections.abc import Mapping

import numpy as np


# [0452 new: pins and the accepted mode range]
TASK_0452_SHA256 = '2cb7cc47429d14803a71cf0acb0ec57407c4aed414998e08ee71fac967efe3e3'
SOURCE_0449_SHA256 = '1b4f129ff93698f951a537c1c59011fba93b75d70c6aa7c704a9992aa3f6bf95'
SOURCE_0449_REVIEW_SHA256 = '68327d2bc23cb2e7e76d861b4d5533f1f3a75fb0346f491bf23efb8238b9a274'
ALLOWED_MODES = (1, 2, 3, 4, 5, 6)
# [0449 L40-42 verbatim]
FIELD_COMPONENTS = 10
LAPSE_FIELD_INDEX = 0       # field axis 1: lapse perturbation n (root v005: N = 1 + f[0].real)
LAPSE_SOURCE_COLUMN = 0     # source coordinate 0 = the single stored unit column e_n (root v004)

# [0452 new: summation order statement]
SUMMATION_ORDER = ('deltaJ0_total = left fold over modes in ascending m: copy of '
                   'deltaJ0_{m_1}; then total = total + deltaJ0_{m_k}, k = 2.. (complex128 '
                   'elementwise IEEE adds, no compensation, no reordering); each per-mode '
                   'array enters exactly once; one mode -> bitwise copy of that array')

# [0449 L44-70 adapted: task pin; combined-source entries added; source_increment and base
#  name the total increment; text of every other entry unchanged]
CONVENTION = dict(
    task_sha256=TASK_0452_SHA256,
    reused_source=('0449 nonzero_cached_feedback_c2v001.py sha256 ' + SOURCE_0449_SHA256
                   + ' (review ' + SOURCE_0449_REVIEW_SHA256 + '): source-to-field stage '
                   'copied with per-region provenance markers; 0449 neither modified nor '
                   'imported'),
    modes=('explicit nonempty mapping {m: rho_m}, unique Python int m in 1..6 (bool and other '
           'types rejected), each rho_m complex (q,) on the one common R, z, RdRdz roster; '
           'processed in ascending m; modes_included and modes_omitted (of 1..6) reported; '
           'no single-mode tag for the combined source'),
    per_mode_gate=('unchanged 0445 contraction per mode with the same validated read-only '
                   'signed waves; COMPLETE, complete True, counts.waves == nk, counts.mode == '
                   'm, full retained_wave_mask, complex128 (nk,), finite, wave array bitwise '
                   'unchanged; first failing mode stops the call, no total formed, every '
                   'per-mode result retained'),
    summation=SUMMATION_ORDER,
    mode_zero='m = 0 not accepted; no m0 source correction in this operation',
    unit_layout=('weighted_responses (nk, 10, 1): axis 1 ten field components, index 0 = '
                 'lapse perturbation n; axis 2 length 1 = response to the unit lapse source '
                 'e_n in source coordinate 0 (root v004 stores and multiplies it this way)'),
    source_increment=('delta_prepared = weighted_unit_response * deltaJ0_total_J[:, None, '
                      'None], once for the combined source (not per mode); equal to root v004 '
                      'unit * delta[:, 0:1, :] with delta[:, 0, 0] = deltaJ0_total_J; no extra '
                      'minus, c^2, 2pi, R, volume or dk weight'),
    base=('supplied base prepared response (root F2 refreshed total), read once per point '
          '(not per mode); the total increment is added around it by linearity of the line '
          'read; no m0 gas subtracted, no reference re-added, no base accumulation'),
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
    branch=('the LINEAR result is the physical-iteration branch; the finite log difference is '
            'computed only when include_log_difference is True and is returned under its own '
            'label; a combined source does not select it'),
    cylindrical=('from Cartesian (gx, gy, gz): R = gx cos(phi) + gy sin(phi), phi = -gx sin(phi) '
                 '+ gy cos(phi) (physical, (1/R) d/dphi), z = gz; component order (R, phi, z)'),
    units=('fields dimensionless, gradient 1/m, hessian 1/m^2, deltaJ0 J, deltaPhi m^2 s^-2, '
           'grad deltaPhi m s^-2'),
    angles='every supplied angle evaluated; no DFT, modal projection or angular average',
    excluded=('solve, regularization, clipping, renormalization, acceptance, file I/O, m0 source '
              'correction, F2 source subtraction, base accumulation'))


# [0449 L73-78 verbatim]
class _InvalidInput(ValueError):
    """Input contract violation detected before any evaluation."""


class _FailClosed(ValueError):
    """Runtime contract violation during the binding."""


# [0449 L81-92 verbatim]
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


# [0449 L95-115 verbatim]
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


# [0449 L118-124 verbatim]
def _tolerance(value, name):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, numbers.Real):
        raise _InvalidInput(name + ': real number required')
    value = float(value)
    if not (math.isfinite(value) and value >= 0.0):
        raise _InvalidInput(name + ': finite nonnegative value required')
    return value


# [0452 new: mode mapping validation; mirrors the 0445 rho checks so that no mode is
#  contracted when any supplied coefficient array is malformed (0445 still validates)]
def _rho_modes(rho_modes_kg_m3, radius_m):
    if not isinstance(rho_modes_kg_m3, Mapping):
        raise _InvalidInput('rho_modes_kg_m3: mapping {m: complex (q,) coefficients} required')
    items = list(rho_modes_kg_m3.items())
    if not items:
        raise _InvalidInput('rho_modes_kg_m3: nonempty mapping required')
    keys = [key for key, _ in items]
    for key in keys:
        if type(key) is not int or not 1 <= key <= 6:
            raise _InvalidInput('rho_modes_kg_m3: keys must be Python int m in 1..6 (bool, '
                                'numpy integer, float and other types rejected); got %r'
                                % (key,))
    if len(set(keys)) != len(keys):
        raise _InvalidInput('rho_modes_kg_m3: unique modes required')
    roster_shape = np.asarray(radius_m).shape
    coefficients = {}
    dtypes = {}
    for key, value in sorted(items, key=lambda item: item[0]):
        name = 'rho_modes_kg_m3[%d]' % key
        raw = np.asarray(value)
        if raw.dtype.kind != 'c' or raw.dtype.itemsize > 16:
            raise _InvalidInput(name + ': complex64/complex128 dtype required, got '
                                + str(raw.dtype))
        if raw.ndim != 1 or raw.shape != roster_shape:
            raise _InvalidInput(name + ': shape (q,) of the one common radius_m roster '
                                       'required, got ' + str(raw.shape))
        rho = np.array(raw, dtype=np.complex128, copy=True)
        if not np.all(np.isfinite(rho)):
            raise _InvalidInput(name + ': finite values required')
        rho.flags.writeable = False
        coefficients[key] = rho
        dtypes[key] = str(raw.dtype)
    return coefficients, dtypes


# [0449 L127-130 adapted: radius_m and rho_modes_kg_m3 replace the single-mode arguments]
def _validate(density_fourier, jn_provider, radius_m, rho_modes_kg_m3, k_physical_inverse_m,
              unit_response, base_prepared, prepare_line, evaluate_line, eval_radius_m,
              eval_phi_rad, eval_z_m, c_m_s, tolerances, wave_chunk, position_chunk,
              include_log_difference, provenance):
    # [0449 L131-167 verbatim]
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
    # [0452 new: mode mapping after the 0449 checks; adapted return of 0449 L168-170]
    rho_modes, rho_dtypes = _rho_modes(rho_modes_kg_m3, radius_m)
    return dict(c_squared=c_squared, tol=tol, waves=waves, unit=unit, base=base,
                unit_dtype=unit_dtype, base_dtype=base_dtype, radius=radius, phi=phi,
                height=height, rho_modes=rho_modes, rho_dtypes=rho_dtypes)


# [0449 L173-204 verbatim]
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


# [0449 L207-222 adapted: rho_modes_kg_m3 mapping replaces rho_mode_kg_m3 and mode;
#  docstring; interruption attribute unt0452_retained_result]
def combined_nonzero_feedback(*, density_fourier, jn_provider, radius_m, z_m, weights_RdRdz_m3,
                              rho_modes_kg_m3, k_physical_inverse_m, unit_response,
                              base_prepared, prepare_line, evaluate_line, eval_radius_m,
                              eval_phi_rad, eval_z_m, c_m_s, base_reality_atol,
                              base_reality_rtol, increment_reality_atol,
                              increment_reality_rtol, wave_chunk, position_chunk,
                              include_log_difference, provenance):
    """Bind several supplied density harmonics through ONE cached full-ten evaluation.

    Returns a fail-closed dict. status 'COMPLETE' -> every payload key is set.
    'INVALID_INPUT' -> nothing evaluated at 'validation'; at
    'density_fourier_validation' a 0445 call reported INVALID_INPUT (failure_mode
    names the mode; earlier per-mode results retained). 'FAILED_CLOSED' -> payload
    keys None; 'retained' holds everything computed so far (per-mode 0445 results
    and deltaJ0, total, line reads; point_mask marks evaluated points). A
    non-Exception interruption is re-raised after the same retained dict (status
    'INTERRUPTED') is attached to it as attribute unt0452_retained_result.
    """
    # [0449 L223-225 verbatim]
    tolerances = dict(base_reality_atol=base_reality_atol, base_reality_rtol=base_reality_rtol,
                      increment_reality_atol=increment_reality_atol,
                      increment_reality_rtol=increment_reality_rtol)
    # [0449 L226-234 adapted: new validation arguments; mode metadata keys None]
    try:
        v = _validate(density_fourier, jn_provider, radius_m, rho_modes_kg_m3,
                      k_physical_inverse_m, unit_response, base_prepared, prepare_line,
                      evaluate_line, eval_radius_m, eval_phi_rad, eval_z_m, c_m_s, tolerances,
                      wave_chunk, position_chunk, include_log_difference, provenance)
    except Exception as exc:  # fail closed: nothing evaluated
        return dict(status='INVALID_INPUT', complete=False, reason=str(exc),
                    failure_stage='validation', failure_mode=None,
                    exception_type=type(exc).__name__, modes_included=None,
                    modes_omitted=None, convention=CONVENTION, retained=None)

    # [0449 L236-241 verbatim]
    waves, unit, base, tol = v['waves'], v['unit'], v['base'], v['tol']
    radius, phi, height, c_squared = v['radius'], v['phi'], v['height'], v['c_squared']
    nk = waves.shape[0]
    n_radius, n_phi, n_z = height.shape
    grid = (n_radius, n_phi, n_z)
    uniform = [2 * math.pi * j / n_phi for j in range(n_phi)]
    # [0452 new: included/omitted modes; wave snapshot for the per-mode order check]
    rho_modes = v['rho_modes']
    modes = tuple(rho_modes)
    omitted = tuple(m for m in ALLOWED_MODES if m not in rho_modes)
    wave_snapshot = waves.copy()
    # [0449 L242-250 adapted: mode -> modes_included / modes_omitted / mode_count,
    #  coefficient dtypes, summation order]
    summary = dict(
        modes_included=modes, modes_omitted=omitted, mode_count=len(modes),
        rho_modes_dtypes=v['rho_dtypes'], positions=int(np.asarray(radius_m).shape[0]),
        waves=nk, summation_order=SUMMATION_ORDER,
        unit_weighted_responses_dtype=v['unit_dtype'], base_weighted_responses_dtype=v['base_dtype'],
        layout='(nk, 10, 1) for unit, base and delta_prepared',
        eval_grid=grid, eval_radius_m=radius, eval_phi_rad=phi, eval_z_m=height,
        angles_equal_2pi_j_over_n=bool(np.array_equal(phi, np.asarray(uniform))),
        c_m_s=float(c_m_s), tolerances=tol, wave_chunk=wave_chunk,
        position_chunk=position_chunk, include_log_difference=include_log_difference,
        boundary='zero perturbations for base and increment')
    # [0449 L251 verbatim]
    provenance_copy = dict(provenance)

    # [0449 L253-260 adapted: per-mode results and deltaJ0, total deltaJ0; per-mode checks;
    #  density_fourier call tally]
    work = dict(density_fourier_results={}, deltaJ0_J_by_mode={}, deltaJ0_J_total=None,
                delta_prepared=None, base_line=None, increment_line=None,
                point_mask=np.zeros(grid, dtype=bool), lapse=None, linear=None,
                log_difference=None)
    checks = dict(all_modes_complete=False, all_mode_deltaJ0_finite=False,
                  deltaJ0_total_finite=False, delta_prepared_finite=False,
                  all_points_finite_and_real=False, lapse_inputs_finite_Nb_positive=False,
                  linear_finite=False,
                  log_difference_finite=(None if not include_log_difference else False))
    tally = dict(density_fourier_calls=0, line_prepare_calls=0, line_evaluate_calls=0)
    # [0449 L261-264 verbatim]
    reality = {role + '_' + kind: dict(max_abs_imag=None, max_excess=None, points_checked=0)
               for role in ('base', 'increment') for kind in ('fields', 'gradient', 'hessian')}
    failure = dict(point=None, check=None)
    stage = 'density_fourier'
    # [0452 new: in-flight mode record for failure_mode and interruption retention]
    current = dict(mode=None)

    # [0449 L266-295 adapted: per-mode statuses, call tallies, failure_mode,
    #  modes_included / modes_omitted]
    def finish(status, exc):
        mask = work['point_mask']
        payload = {key: value for key, value in work.items()}
        complete = status == 'COMPLETE'
        results = work['density_fourier_results']
        result = dict(
            status=status, complete=complete, reason=None, failure_stage=None,
            failure_mode=None, exception_type=None, failure_point=failure['point'],
            failure_check=failure['check'], modes_included=modes, modes_omitted=omitted,
            provenance=provenance_copy, inputs=summary,
            jn_provider_metadata=(dict(jn_provider['metadata']) if isinstance(
                jn_provider.get('metadata'), Mapping) else None),
            completeness=dict(
                density_fourier_status_by_mode={
                    m: (results[m].get('status') if isinstance(results.get(m), Mapping)
                        else None) for m in modes},
                modes_complete=tuple(work['deltaJ0_J_by_mode']),
                density_fourier_calls_expected=len(modes),
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
            result['failure_mode'] = current['mode']
            result['exception_type'] = type(exc).__name__
        return result

    # [0449 L297-329 adapted: one unchanged 0445 call per included mode, ascending m, the
    #  same validated waves; per-mode gate as 0449 plus the wave-array check]
    try:
        # Step 1: 0445 contraction per mode with the READY provider; COMPLETE only.
        for m in modes:
            current['mode'] = m
            stage = 'density_fourier'
            tally['density_fourier_calls'] += 1
            density = density_fourier(radius_m=radius_m, z_m=z_m,
                                      weights_RdRdz_m3=weights_RdRdz_m3,
                                      rho_mode_kg_m3=rho_modes[m], k_physical_inverse_m=waves,
                                      c_m_s=c_m_s, mode=m, bessel_jn=jn_provider['bessel_jn'],
                                      wave_chunk=wave_chunk, position_chunk=position_chunk)
            work['density_fourier_results'][m] = density
            if isinstance(density, Mapping) and density.get('status') == 'INVALID_INPUT':
                result = finish('INVALID_INPUT', _InvalidInput(
                    '0445 contraction INVALID_INPUT for mode %d: %s'
                    % (m, density.get('reason'))))
                result['failure_stage'] = 'density_fourier_validation'
                return result
            if not isinstance(density, Mapping) or density.get('status') != 'COMPLETE' \
                    or density.get('complete') is not True:
                raise _FailClosed('0445 contraction for mode %d not COMPLETE (status %r); '
                                  'partial deltaJ0 never consumed, no total formed'
                                  % (m, density.get('status')
                                     if isinstance(density, Mapping) else None))
            counts = density.get('counts') or {}
            mask0445 = np.asarray(density.get('retained_wave_mask'))
            if counts.get('waves') != nk or counts.get('mode') != m \
                    or mask0445.shape != (nk,) or not np.all(mask0445):
                raise _FailClosed('0445 result counts/mode/wave mask do not match mode %d' % m)
            if waves.shape != wave_snapshot.shape or not np.array_equal(waves, wave_snapshot):
                raise _FailClosed('signed wave array changed during the mode %d call' % m)
            delta_j = density.get('deltaJ0_J')
            if not isinstance(delta_j, np.ndarray) or delta_j.dtype != np.complex128 \
                    or delta_j.shape != (nk,):
                raise _FailClosed('0445 deltaJ0_J for mode %d must be complex128 (nk,)' % m)
            delta_j = delta_j.copy()
            if not np.all(np.isfinite(delta_j)):
                raise _FailClosed('nonfinite deltaJ0_J for mode %d' % m)
            delta_j.flags.writeable = False
            work['deltaJ0_J_by_mode'][m] = delta_j
        checks['all_modes_complete'] = True
        checks['all_mode_deltaJ0_finite'] = True
        current['mode'] = None

        # [0452 new: the single summation, ascending-m left fold, each mode once]
        stage = 'deltaJ0_sum'
        combined = work['deltaJ0_J_by_mode'][modes[0]].copy()
        for m in modes[1:]:
            combined = combined + work['deltaJ0_J_by_mode'][m]
        if not np.all(np.isfinite(combined)):
            raise _FailClosed('nonfinite deltaJ0_total')
        combined.flags.writeable = False
        work['deltaJ0_J_total'] = combined
        checks['deltaJ0_total_finite'] = True
        delta_j = combined

        # [0449 L331-338 verbatim]
        # Step 2: the single multiplication by the cached weighted unit response.
        stage = 'delta_prepared'
        delta_prepared = unit * delta_j[:, None, None]
        if not np.all(np.isfinite(delta_prepared)):
            raise _FailClosed('nonfinite delta_prepared')
        delta_prepared.flags.writeable = False
        work['delta_prepared'] = dict(wavevectors=waves, weighted_responses=delta_prepared)
        checks['delta_prepared_finite'] = True

        # [0449 L340-394 verbatim]
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

        # [0449 L396-449 verbatim]
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
    # [0449 L450-455 adapted: attribute unt0452_retained_result; an in-flight mode's
    #  0445 interruption record (unt0445_retained_result) is kept under that mode]
    except BaseException as exc:
        try:
            pending = current['mode']
            record = getattr(exc, 'unt0445_retained_result', None)
            if pending is not None and pending not in work['density_fourier_results'] \
                    and isinstance(record, Mapping):
                work['density_fourier_results'][pending] = record
        except Exception:
            pass
        try:
            exc.unt0452_retained_result = finish('INTERRUPTED', exc)
        except Exception:
            pass
        raise
    # [0449 L456 verbatim]
    return finish('COMPLETE', None)
