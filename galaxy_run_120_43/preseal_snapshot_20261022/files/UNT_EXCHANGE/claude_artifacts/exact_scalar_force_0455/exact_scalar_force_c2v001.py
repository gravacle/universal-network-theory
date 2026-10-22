"""INERT exact finite-sum lapse scalar + Cartesian gradient evaluator with reusable
geometry and a cached base bound to exact point identity; UNT task 0455, c2v001.

Task 0455 file sha256 b467a0c0c6e2fe3498a44ebdecca110776528dde7b4304d204cd42e64c67062c.
Read-only conventions: fixed-xy line module owned_fixed_xy_fourier_line_v002.py sha256
3a47419d88f24e5f6f0f1c2db1ea85cf4108057a3ddb94db608cd05e94822d18 (phase exp(1j*angle),
angle = kx*x + ky*y then kz*z, derivative multiplier 1j*k, exact-equal kz groups);
0449 nonzero_cached_feedback_c2v001.py sha256
1b4f129ff93698f951a537c1c59011fba93b75d70c6aa7c704a9992aa3f6bf95 (Nb = 1 + Re n_b,
LINEAR deltaPhi = c^2 dn/Nb, grad = c^2 (grad dn/Nb - dn grad nb/Nb^2), elementwise
|Im| <= atol + rtol |Re| reality form).

Finite equations, supplied signed waves k_j (1/m) and supplied complex a_j (already
unit_lapse * deltaJ, once):
    dn(x)      = SUM_j a_j exp(i k_j . x)
    grad dn(x) = SUM_j (i k_j) a_j exp(i k_j . x)
Nothing is added inside the sum: no Fourier weight, boundary term, factor 2, c^2,
reflection, symmetry, mode removal or .real before admission.
Exact regrouping (changes roundoff only):
    exact-equal (kx, ky) pairs p and exact-equal kz values q; dense
    S[q, p] = SUM of a_j with (pair, kz) = (p, q) (np.add.at in supplied order, exact
    duplicate waves summed; a hole is an exact zero = no supplied term);
    exact-equal (x, y) point columns c (z free per point);
    E[c, p] = exp(1j*(kx_p*x_c + ky_p*y_c)), chunked over columns;
    C = E.S, Cx = E.((1j kx) S), Cy = E.((1j ky) S), Cz = C (1j kz)  (np.einsum,
    optimize=False);
    per point: V[q] = exp(1j*(kz_q*z)); dn = SUM_q V C[c, q], grad = SUM_q V (Cx, Cy, Cz)[c, q].
No complete Cartesian product, symmetry, interpolation or binning is assumed.
Admission (separate): finite + elementwise reality |Im| <= atol + rtol |Re| on base and
increment fields and on length-scaled gradients (L * grad), then Nb = 1 + Re n_b > 0,
then the 0449 LINEAR expressions. No Hessian is evaluated. No log replacement, field
solve, source transform, DFT or flow solve.
numpy + stdlib only; no BLAS products (contractions use np.einsum optimize=False); no
floating-point warning suppression (the caller's numpy.errstate governs, a
FloatingPointError fails closed with retention); no I/O; keyword-only arguments without
defaults; fail-closed result dicts; definitions only at import.
"""
import hashlib
import math
import numbers
from collections.abc import Mapping
from types import MappingProxyType

import numpy as np


TASK_0455_SHA256 = 'b467a0c0c6e2fe3498a44ebdecca110776528dde7b4304d204cd42e64c67062c'
LINE_REFERENCE_SHA256 = '3a47419d88f24e5f6f0f1c2db1ea85cf4108057a3ddb94db608cd05e94822d18'
LAPSE_CONVENTION_0449_SHA256 = '1b4f129ff93698f951a537c1c59011fba93b75d70c6aa7c704a9992aa3f6bf95'
GEOMETRY_KIND = 'UNT0455_EXACT_SCALAR_GEOMETRY_C2V001'
BASE_KIND = 'UNT0455_BOUND_BASE_LAPSE_C2V001'
FINITE_SUM_KIND = 'UNT0455_RAW_COMPLEX_FINITE_SUM_C2V001'
HESSIAN = 'NONE EVALUATED (force-only application; no Hessian computed or claimed)'

CONVENTION = MappingProxyType(dict(
    task_sha256=TASK_0455_SHA256,
    line_reference_sha256=LINE_REFERENCE_SHA256,
    lapse_convention_0449_sha256=LAPSE_CONVENTION_0449_SHA256,
    finite_sum=('dn = SUM_j a_j exp(i k_j.x); grad dn = SUM_j (i k_j) a_j exp(i k_j.x); a_j used '
                'as supplied (no weight, boundary, factor 2, c^2, reflection, mode removal, .real)'),
    regrouping=('exact-equal (kx,ky) pairs and exact-equal kz values; dense S[kz, pair] by '
                'np.add.at (duplicates summed, holes exact zero); exact-equal (x,y) columns; '
                'E = exp(1j*(kx*x + ky*y)) per column block; C = E.S, Cx = E.((1j kx) S), '
                'Cy = E.((1j ky) S), Cz = C*(1j kz); per point SUM_q exp(1j*(kz_q*z)) * line; '
                'roundoff grouping changed, finite equation unchanged'),
    identity=('geometry reuse requires byte-identical float64 wavevectors and points (sha256 '
              'of shape, dtype and bytes) and an unchanged geometry digest; the base is bound '
              'to the sha256 of its points; amplitudes, S and collapsed lines are rebuilt on '
              'every call and never cached'),
    reality=('finite, and |Im v| <= atol + rtol |Re v| elementwise with finite bound, for v = '
             'n_b, L*grad n_b (base tolerances) and v = dn, L*grad dn (increment tolerances); L '
             '= caller length scale in m; all four evaluated and reported before any failure'),
    linear=('Nb = 1 + Re n_b > 0 required; deltaPhi = c^2 * (dn / Nb); grad deltaPhi = c^2 * '
            '(grad_dn / Nb - dn * grad_nb / (Nb * Nb)) with dn, grad_dn, grad_nb real parts'),
    units=('k 1/m, x/y/z m, n dimensionless, gradients 1/m, c m/s, deltaPhi m^2 s^-2, grad '
           'deltaPhi m s^-2'),
    hessian=HESSIAN,
    excluded=('Hessian, log replacement, field solve, source transform, DFT, flow solve, '
              'interpolation, symmetry, regularization, clipping, file I/O')))


class _InvalidInput(ValueError):
    """Input contract violation detected before any evaluation."""


class _FailClosed(ValueError):
    """Runtime contract violation; evaluation stopped."""


# ----------------------------------------------------------------------------- helpers

def _real_array(value, name):
    array = np.asarray(value)
    kind = array.dtype.kind
    if kind not in 'fiu' or (kind == 'f' and array.dtype.itemsize > 8):
        raise _InvalidInput(name + ': real float64-representable dtype required, got '
                            + str(array.dtype))
    array = np.array(array, dtype=np.float64, copy=True, order='C')
    if not np.all(np.isfinite(array)):
        raise _InvalidInput(name + ': finite values required')
    return array


def _complex_array(value, name, shape):
    raw = np.asarray(value)
    kind = raw.dtype.kind
    if not ((kind == 'c' and raw.dtype.itemsize <= 16) or (kind == 'f' and raw.dtype.itemsize <= 8)):
        raise _InvalidInput(name + ': complex128/float64-representable dtype required, got '
                            + str(raw.dtype))
    if raw.shape != shape:
        raise _InvalidInput(name + ': shape %s required, got %s' % (shape, raw.shape))
    array = np.array(raw, dtype=np.complex128, copy=True, order='C')
    if not np.all(np.isfinite(array)):
        raise _InvalidInput(name + ': finite values required')
    array.flags.writeable = False
    return array


def _positive_int(value, name):
    if type(value) is not int or value < 1:
        raise _InvalidInput(name + ': positive int required (bool and numpy ints rejected)')
    return value


def _nonnegative(value, name):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, numbers.Real):
        raise _InvalidInput(name + ': real number required')
    value = float(value)
    if not (math.isfinite(value) and value >= 0.0):
        raise _InvalidInput(name + ': finite nonnegative value required')
    return value


def _positive(value, name):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, numbers.Real):
        raise _InvalidInput(name + ': real number required')
    value = float(value)
    if not (math.isfinite(value) and value > 0.0):
        raise _InvalidInput(name + ': finite positive value required')
    return value


def _digest(label, arrays):
    """sha256 over label, then (dtype, shape, C-order bytes) of each array."""
    h = hashlib.sha256()
    h.update(label.encode('ascii'))
    for array in arrays:
        array = np.ascontiguousarray(array)
        h.update(('|%s|%r|' % (array.dtype.str, array.shape)).encode('ascii'))
        h.update(array.reshape(-1).view(np.uint8))
    return h.hexdigest()


def _waves(wavevectors):
    k = _real_array(wavevectors, 'wavevectors')
    if k.ndim != 2 or k.shape[1] != 3 or k.shape[0] < 1:
        raise _InvalidInput('wavevectors: shape (nk, 3), nk >= 1 required, got %s' % (k.shape,))
    k.flags.writeable = False
    return k, _digest('wavevectors', [k])


def _points(x_m, y_m, z_m):
    x = _real_array(x_m, 'x_m')
    y = _real_array(y_m, 'y_m')
    z = _real_array(z_m, 'z_m')
    if x.ndim < 1 or x.size < 1 or y.shape != x.shape or z.shape != x.shape:
        raise _InvalidInput('x_m, y_m, z_m: equal shapes with ndim >= 1 and size >= 1 required, '
                            'got %s %s %s' % (x.shape, y.shape, z.shape))
    for array in (x, y, z):
        array.flags.writeable = False
    return x, y, z, _digest('points_xyz', [x, y, z])


def _group_pairs(a, b):
    """Exact-equal (a, b) groups: (index per entry, sorted unique pairs, sort order, starts)."""
    order = np.lexsort((b, a))
    sa = a[order]
    sb = b[order]
    new = np.empty(order.shape[0], dtype=bool)
    new[0] = True
    new[1:] = (sa[1:] != sa[:-1]) | (sb[1:] != sb[:-1])
    index = np.empty(order.shape[0], dtype=np.intp)
    index[order] = np.cumsum(new) - 1
    unique = np.stack((sa[new], sb[new]), axis=1)
    return index, unique, order, np.flatnonzero(new)


def _group_values(v):
    """Exact-equal value groups: (index per entry, sorted unique values)."""
    order = np.argsort(v, kind='stable')
    sv = v[order]
    new = np.empty(order.shape[0], dtype=bool)
    new[0] = True
    new[1:] = sv[1:] != sv[:-1]
    index = np.empty(order.shape[0], dtype=np.intp)
    index[order] = np.cumsum(new) - 1
    return index, sv[new]


_GEOMETRY_ARRAYS = ('wavevectors', 'transverse_pairs', 'kz_values', 'wave_pair_index',
                    'wave_kz_index', 'x_m', 'y_m', 'z_m', 'column_xy', 'point_column',
                    'point_order', 'column_offsets')
_GEOMETRY_INTS = ('max_dense_entries', 'max_block_entries', 'column_chunk', 'point_chunk',
                  'column_block', 'point_block', 'waves', 'transverse_pairs_count', 'kz_count',
                  'dense_entries', 'filled_cells', 'points', 'columns')


def _geometry_digest(record):
    header = '|'.join([record['kind'], record['wave_sha256'], record['point_sha256'],
                       'shape=%r' % (tuple(record['point_shape']),)]
                      + ['%s=%d' % (key, record['counts'][key]) for key in _GEOMETRY_INTS])
    return _digest('geometry|' + header, [record[key] for key in _GEOMETRY_ARRAYS])


def _check_geometry(geometry):
    if not isinstance(geometry, Mapping) or geometry.get('kind') != GEOMETRY_KIND:
        raise _InvalidInput('geometry: a prepare_geometry(...)["geometry"] record required')
    try:
        digest = _geometry_digest(geometry)
    except Exception as exc:
        raise _InvalidInput('geometry: record incomplete or malformed (%s)' % (exc,))
    if digest != geometry.get('geometry_sha256'):
        raise _InvalidInput('geometry: stored arrays changed since preparation (digest '
                            'mismatch); prepare a new geometry')
    return geometry


def _check_identity(geometry, wavevectors, x_m, y_m, z_m):
    _, wave_sha = _waves(wavevectors)
    if wave_sha != geometry['wave_sha256']:
        raise _InvalidInput('wave identity: supplied wavevectors are not byte-identical (float64, '
                            'same shape and signed order) to the prepared geometry')
    _, _, _, point_sha = _points(x_m, y_m, z_m)
    if point_sha != geometry['point_sha256']:
        raise _InvalidInput('point identity: supplied x_m, y_m, z_m are not byte-identical '
                            '(float64, same shape and order) to the prepared geometry')


def _check_base(base):
    if not isinstance(base, Mapping) or base.get('kind') != BASE_KIND:
        raise _InvalidInput('base: a bind_base(...)["base"] record required')
    try:
        digest = _digest('base_lapse', [base['n_base_complex'], base['grad_n_base_complex']])
    except Exception as exc:
        raise _InvalidInput('base: record incomplete or malformed (%s)' % (exc,))
    if digest != base.get('base_sha256'):
        raise _InvalidInput('base: stored arrays changed since binding (digest mismatch)')
    return base


def _admission_scalars(c_m_s, gradient_length_scale_m, tolerances):
    c = _positive(c_m_s, 'c_m_s')
    c_squared = c * c
    if not (math.isfinite(c_squared) and c_squared > 0.0):
        raise _InvalidInput('c_m_s: finite positive square required')
    length = _positive(gradient_length_scale_m, 'gradient_length_scale_m')
    tol = {name: _nonnegative(value, name) for name, value in tolerances.items()}
    return c, c_squared, length, tol


def _reality(value, atol, rtol):
    """Elementwise finite |Im| <= atol + rtol |Re|; report dict with 'passed'."""
    report = dict(passed=False, max_abs_imag=math.nan, max_excess=math.nan,
                  entries_checked=int(value.size), entries_failing=None)
    if not np.all(np.isfinite(value)):
        report['reason'] = 'nonfinite value'
        return report
    magnitude = np.abs(value.imag)
    bound = atol + rtol * np.abs(value.real)
    if not np.all(np.isfinite(bound)):
        report['reason'] = 'nonfinite bound'
        return report
    failing = magnitude > bound
    report.update(passed=not bool(np.any(failing)), max_abs_imag=float(np.max(magnitude)),
                  max_excess=float(np.max(magnitude - bound)),
                  entries_failing=int(np.count_nonzero(failing)))
    return report


def _invalid(exc, stage, **extra):
    result = dict(status='INVALID_INPUT', complete=False, reason=str(exc), failure_stage=stage,
                  exception_type=type(exc).__name__, convention=CONVENTION, retained=None)
    result.update(extra)
    return result


# ----------------------------------------------------------------------------- geometry

def prepare_geometry(*, wavevectors, x_m, y_m, z_m, max_dense_entries, max_block_entries,
                     column_chunk, point_chunk):
    """Group waves and points once; no source-dependent data is stored.

    wavevectors (nk, 3) real signed 1/m; x_m, y_m, z_m equal-shape real arrays (m).
    Limits (positive int, no defaults): the dense grid n_kz * n_pairs must be <=
    max_dense_entries (evaluation holds three complex128 grids of that size); with
    cb = min(column_chunk, columns) and pb = min(point_chunk, points), each of
    cb * n_pairs, 4 * cb * n_kz and pb * n_kz must be <= max_block_entries.
    A violated limit fails closed BEFORE any dense or block allocation.
    Returns {'status': 'COMPLETE', 'geometry': read-only record, ...} or a fail-closed dict.
    """
    stage = 'validation'
    try:
        limits = dict(max_dense_entries=_positive_int(max_dense_entries, 'max_dense_entries'),
                      max_block_entries=_positive_int(max_block_entries, 'max_block_entries'),
                      column_chunk=_positive_int(column_chunk, 'column_chunk'),
                      point_chunk=_positive_int(point_chunk, 'point_chunk'))
        k, wave_sha = _waves(wavevectors)
        x, y, z, point_sha = _points(x_m, y_m, z_m)
    except Exception as exc:
        return _invalid(exc, stage, geometry=None)
    counts = dict(limits)
    try:
        stage = 'wave_grouping'
        pair_index, pairs, _, _ = _group_pairs(k[:, 0], k[:, 1])
        kz_index, kz_values = _group_values(k[:, 2])
        n_pairs, n_kz = int(pairs.shape[0]), int(kz_values.shape[0])
        dense = n_pairs * n_kz
        counts.update(waves=int(k.shape[0]), transverse_pairs_count=n_pairs, kz_count=n_kz,
                      dense_entries=dense)
        stage = 'dense_limit'
        if dense > limits['max_dense_entries']:
            raise _FailClosed('dense grouping n_kz * n_pairs = %d * %d = %d exceeds '
                              'max_dense_entries = %d; nothing allocated'
                              % (n_kz, n_pairs, dense, limits['max_dense_entries']))
        cell = kz_index * n_pairs + pair_index
        counts['filled_cells'] = int(np.unique(cell).shape[0])
        stage = 'point_grouping'
        flat_x, flat_y = x.reshape(-1), y.reshape(-1)
        point_column, column_xy, point_order, starts = _group_pairs(flat_x, flat_y)
        n_points, n_columns = int(flat_x.shape[0]), int(column_xy.shape[0])
        column_offsets = np.empty(n_columns + 1, dtype=np.intp)
        column_offsets[:-1] = starts
        column_offsets[-1] = n_points
        column_block = min(limits['column_chunk'], n_columns)
        point_block = min(limits['point_chunk'], n_points)
        counts.update(points=n_points, columns=n_columns, column_block=column_block,
                      point_block=point_block)
        stage = 'block_limit'
        blocks = dict(transverse_phase=column_block * n_pairs, collapsed=4 * column_block * n_kz,
                      vertical=point_block * n_kz)
        over = {key: value for key, value in blocks.items() if value > limits['max_block_entries']}
        if over:
            raise _FailClosed('block entries %s exceed max_block_entries = %d; nothing allocated'
                              % (over, limits['max_block_entries']))
        stage = 'record'
        record = dict(kind=GEOMETRY_KIND, task_sha256=TASK_0455_SHA256, wavevectors=k,
                      wave_sha256=wave_sha, transverse_pairs=pairs, kz_values=kz_values,
                      wave_pair_index=pair_index, wave_kz_index=kz_index, x_m=x, y_m=y, z_m=z,
                      point_shape=tuple(x.shape), point_sha256=point_sha, column_xy=column_xy,
                      point_column=point_column, point_order=point_order,
                      column_offsets=column_offsets, block_entries=MappingProxyType(blocks),
                      counts=MappingProxyType(counts))
        for key in _GEOMETRY_ARRAYS:
            record[key].flags.writeable = False
        record['geometry_sha256'] = _geometry_digest(record)
        geometry = MappingProxyType(record)
    except Exception as exc:  # FloatingPointError under caller errstate included
        return dict(status='FAILED_CLOSED', complete=False, reason=str(exc),
                    failure_stage=stage, exception_type=type(exc).__name__, geometry=None,
                    counts=dict(counts), convention=CONVENTION, retained=None)
    return dict(status='COMPLETE', complete=True, reason=None, failure_stage=None,
                exception_type=None, geometry=geometry, counts=dict(counts),
                convention=CONVENTION, retained=None)


def bind_base(*, n_base, grad_n_base, x_m, y_m, z_m):
    """Bind cached complex base lapse n_b (point shape) and grad n_b (point shape + (3,))
    to the exact identity (sha256) of the points they were evaluated on. Copies only."""
    try:
        x, _, _, point_sha = _points(x_m, y_m, z_m)
        shape = tuple(x.shape)
        nb = _complex_array(n_base, 'n_base', shape)
        gnb = _complex_array(grad_n_base, 'grad_n_base', shape + (3,))
    except Exception as exc:
        return _invalid(exc, 'validation', base=None)
    record = dict(kind=BASE_KIND, task_sha256=TASK_0455_SHA256, point_shape=shape,
                  point_sha256=point_sha, n_base_complex=nb, grad_n_base_complex=gnb,
                  base_sha256=_digest('base_lapse', [nb, gnb]))
    return dict(status='COMPLETE', complete=True, reason=None, failure_stage=None,
                exception_type=None, base=MappingProxyType(record), convention=CONVENTION,
                retained=None)


# ----------------------------------------------------------------------------- finite sum

def _finite_sum_core(geometry, amplitudes, amplitude_sha):
    counts = geometry['counts']
    n_pairs, n_kz = counts['transverse_pairs_count'], counts['kz_count']
    n_points, n_columns = counts['points'], counts['columns']
    column_block, point_block = counts['column_block'], counts['point_block']
    shape = geometry['point_shape']
    nan = complex(math.nan, math.nan)
    work = dict(amplitudes=amplitudes, dense_stack=None, last_block=None,
                dn_complex=np.full(n_points, nan, dtype=np.complex128),
                grad_dn_complex=np.full((n_points, 3), nan, dtype=np.complex128),
                point_mask=np.zeros(n_points, dtype=bool),
                column_mask=np.zeros(n_columns, dtype=bool))
    tally = dict(column_blocks=0, point_blocks=0, transverse_phases=0, vertical_phases=0,
                 collapse_complex_mac=0, vertical_complex_mac=0)
    identity = dict(geometry_sha256=geometry['geometry_sha256'],
                    wave_sha256=geometry['wave_sha256'], point_sha256=geometry['point_sha256'],
                    amplitude_sha256=amplitude_sha, result_sha256=None)
    state = dict(stage='scatter', block=None)

    def finish(status, exc):
        complete = status == 'COMPLETE'
        if complete:
            work['dn_complex'].flags.writeable = False
            work['grad_dn_complex'].flags.writeable = False
        dn = work['dn_complex'].reshape(shape)
        grad = work['grad_dn_complex'].reshape(shape + (3,))
        retained = dict(work)
        retained['dn_complex'] = dn
        retained['grad_dn_complex'] = grad
        retained['point_mask'] = work['point_mask'].reshape(shape)
        result = dict(kind=FINITE_SUM_KIND, status=status, complete=complete, reason=None,
                      failure_stage=None, exception_type=None, failure_block=state['block'],
                      dn_complex=None, grad_dn_complex=None, identity=identity,
                      counts=dict(counts, **tally), point_shape=shape, hessian=HESSIAN,
                      convention=CONVENTION, retained=retained)
        if complete:
            identity['result_sha256'] = _digest('finite_sum', [dn, grad])
            result.update(dn_complex=dn, grad_dn_complex=grad)
        else:
            result.update(reason=str(exc), failure_stage=state['stage'],
                          exception_type=type(exc).__name__)
        result['identity'] = MappingProxyType(dict(identity))
        return result

    try:
        pairs, kz = geometry['transverse_pairs'], geometry['kz_values']
        kx, ky = pairs[:, 0], pairs[:, 1]
        # Dense stack [S, (1j kx) S, (1j ky) S], layout (field, kz, pair); fresh per call.
        dense = np.zeros((3, n_kz, n_pairs), dtype=np.complex128)
        np.add.at(dense[0], (geometry['wave_kz_index'], geometry['wave_pair_index']), amplitudes)
        state['stage'] = 'derivative_multipliers'
        np.multiply((1j * kx)[None, :], dense[0], out=dense[1])
        np.multiply((1j * ky)[None, :], dense[0], out=dense[2])
        if not np.all(np.isfinite(dense)):
            raise _FailClosed('nonfinite scattered amplitudes or transverse multipliers')
        dense.flags.writeable = False
        work['dense_stack'] = dense
        mult_z = 1j * kz
        column_xy, offsets = geometry['column_xy'], geometry['column_offsets']
        order, point_column = geometry['point_order'], geometry['point_column']
        flat_z = geometry['z_m'].reshape(-1)
        dn_out, grad_out = work['dn_complex'], work['grad_dn_complex']
        for c0 in range(0, n_columns, column_block):
            c1 = min(c0 + column_block, n_columns)
            state['block'] = dict(columns=(c0, c1), points=None)
            state['stage'] = 'transverse_phase'
            angle = np.multiply.outer(column_xy[c0:c1, 0], kx)
            angle += np.multiply.outer(column_xy[c0:c1, 1], ky)
            if not np.all(np.isfinite(angle)):
                raise _FailClosed('nonfinite transverse phase angle')
            phase = np.exp(1j * angle)
            del angle
            tally['transverse_phases'] += phase.size
            tally['collapse_complex_mac'] += 3 * phase.size * n_kz
            state['stage'] = 'collapse'
            collapsed = np.empty((4, c1 - c0, n_kz), dtype=np.complex128)
            for f in range(3):
                collapsed[f] = np.einsum('cp,qp->cq', phase, dense[f], optimize=False)
            del phase
            np.multiply(collapsed[0], mult_z[None, :], out=collapsed[3])
            if not np.all(np.isfinite(collapsed)):
                raise _FailClosed('nonfinite collapsed line coefficients')
            work['last_block'] = dict(columns=(c0, c1), collapsed_C_Cx_Cy_Cz=collapsed)
            state['stage'] = 'vertical'
            p_start, p_end = int(offsets[c0]), int(offsets[c1])
            for p0 in range(p_start, p_end, point_block):
                p1 = min(p0 + point_block, p_end)
                state['block'] = dict(columns=(c0, c1), points=(p0, p1))
                points = order[p0:p1]
                local = point_column[points] - c0
                vangle = np.multiply.outer(flat_z[points], kz)
                if not np.all(np.isfinite(vangle)):
                    raise _FailClosed('nonfinite vertical phase angle')
                vphase = np.exp(1j * vangle)
                del vangle
                tally['vertical_phases'] += vphase.size
                tally['vertical_complex_mac'] += 4 * vphase.size
                values = np.empty((p1 - p0, 4), dtype=np.complex128)
                for f in range(4):
                    values[:, f] = np.einsum('pq,pq->p', vphase, collapsed[f][local],
                                             optimize=False)
                if not np.all(np.isfinite(values)):
                    raise _FailClosed('nonfinite point read')
                dn_out[points] = values[:, 0]
                grad_out[points] = values[:, 1:]
                work['point_mask'][points] = True
                tally['point_blocks'] += 1
            work['column_mask'][c0:c1] = True
            tally['column_blocks'] += 1
        state['stage'] = 'completeness'
        if not (np.all(work['point_mask']) and np.all(work['column_mask'])):
            raise _FailClosed('not every point/column evaluated')
        state['stage'] = 'complete'
        state['block'] = None
    except Exception as exc:  # FloatingPointError under caller errstate included
        return finish('FAILED_CLOSED', exc)
    except BaseException as exc:
        try:
            exc.unt0455_retained_result = finish('INTERRUPTED', exc)
        except Exception:
            pass
        raise
    return finish('COMPLETE', None)


def exact_finite_sum(*, geometry, wavevectors, amplitudes, x_m, y_m, z_m):
    """Raw complex dn and grad dn at the geometry's points; NO reality admission.

    wavevectors and x_m/y_m/z_m must be byte-identical (as float64) to those prepared;
    amplitudes (nk,) complex in the same signed wave order, used exactly as supplied.
    Returns a fail-closed dict; COMPLETE -> dn_complex (point shape) and
    grad_dn_complex (point shape + (3,), Cartesian x, y, z) read-only, plus
    identity digests and retained intermediates (amplitude copy, dense stack, last
    column block's collapsed lines). Failure -> retained partial arrays and masks.
    """
    try:
        geometry = _check_geometry(geometry)
        _check_identity(geometry, wavevectors, x_m, y_m, z_m)
        amplitudes = _complex_array(amplitudes, 'amplitudes', (geometry['counts']['waves'],))
        amplitude_sha = _digest('amplitudes', [amplitudes])
    except Exception as exc:
        return _invalid(exc, 'validation', kind=FINITE_SUM_KIND, dn_complex=None,
                        grad_dn_complex=None, hessian=HESSIAN)
    return _finite_sum_core(geometry, amplitudes, amplitude_sha)


# ----------------------------------------------------------------------------- admission

def _check_finite_sum(finite_sum):
    if not isinstance(finite_sum, Mapping) or finite_sum.get('kind') != FINITE_SUM_KIND:
        raise _InvalidInput('finite_sum: an exact_finite_sum(...) result required')
    if finite_sum.get('status') != 'COMPLETE' or finite_sum.get('complete') is not True:
        raise _InvalidInput('finite_sum: status COMPLETE required, got %r'
                            % (finite_sum.get('status'),))
    dn, grad = finite_sum.get('dn_complex'), finite_sum.get('grad_dn_complex')
    shape = finite_sum.get('point_shape')
    identity = finite_sum.get('identity')
    if not isinstance(dn, np.ndarray) or not isinstance(grad, np.ndarray) \
            or dn.dtype != np.complex128 or grad.dtype != np.complex128 \
            or dn.shape != shape or grad.shape != tuple(shape) + (3,) \
            or not isinstance(identity, Mapping):
        raise _InvalidInput('finite_sum: complex128 dn_complex/grad_dn_complex of the point '
                            'shape and identity record required')
    if _digest('finite_sum', [dn, grad]) != identity.get('result_sha256'):
        raise _InvalidInput('finite_sum: dn/grad arrays changed since evaluation (digest mismatch)')
    return dn, grad, identity


def _admit(dn_c, grad_dn_c, base, c_squared, length, tol, extra):
    reality = {}
    work = dict(dn_complex=dn_c, grad_dn_complex=grad_dn_c, lapse=None, linear=None)
    checks = dict(reality_all_passed=False, lapse_inputs_finite_Nb_positive=False,
                  linear_finite=False)
    state = dict(stage='reality')

    def finish(status, exc):
        complete = status == 'COMPLETE'
        result = dict(status=status, complete=complete, reason=None, failure_stage=None,
                      exception_type=None, dn_complex=None, grad_dn_complex=None, Nb=None,
                      deltaPhi_m2_s2=None, grad_deltaPhi_cartesian_m_s2=None,
                      reality=reality, checks=dict(checks), hessian=HESSIAN,
                      base_sha256=base['base_sha256'], point_sha256=base['point_sha256'],
                      convention=CONVENTION, retained=None)
        result.update(extra)
        if complete:
            result.update(dn_complex=dn_c, grad_dn_complex=grad_dn_c, Nb=work['lapse']['Nb'],
                          deltaPhi_m2_s2=work['linear']['deltaPhi_m2_s2'],
                          grad_deltaPhi_cartesian_m_s2=work['linear'][
                              'grad_deltaPhi_cartesian_m_s2'],
                          lapse=work['lapse'], linear=work['linear'])
        else:
            result.update(reason=str(exc), failure_stage=state['stage'],
                          exception_type=type(exc).__name__, retained=work)
        return result

    try:
        nb_c, grad_nb_c = base['n_base_complex'], base['grad_n_base_complex']
        for role, field, gradient in (('base', nb_c, grad_nb_c), ('increment', dn_c, grad_dn_c)):
            atol, rtol = tol[role + '_reality_atol'], tol[role + '_reality_rtol']
            reality[role + '_fields'] = _reality(field, atol, rtol)
            reality[role + '_gradient_length_scaled'] = _reality(length * gradient, atol, rtol)
        failed = [key for key, report in reality.items() if not report['passed']]
        if failed:
            raise _FailClosed('nonfinite or nonreal (beyond caller tolerance) %s' % (failed,))
        checks['reality_all_passed'] = True

        state['stage'] = 'lapse_inputs'
        nb = nb_c.real.copy()
        grad_nb = grad_nb_c.real.copy()
        dn = dn_c.real.copy()
        grad_dn = grad_dn_c.real.copy()
        lapse_base = 1.0 + nb
        if not all(np.all(np.isfinite(a)) for a in (nb, grad_nb, dn, grad_dn, lapse_base)):
            raise _FailClosed('nonfinite real lapse inputs')
        work['lapse'] = dict(nb=nb, grad_nb_cartesian=grad_nb, dn=dn, grad_dn_cartesian=grad_dn,
                             Nb=lapse_base)
        if np.any(~(lapse_base > 0.0)):
            raise _FailClosed('Nb = 1 + Re n_b must be > 0 at every point; %d points fail'
                              % int(np.count_nonzero(~(lapse_base > 0.0))))
        checks['lapse_inputs_finite_Nb_positive'] = True

        state['stage'] = 'linear'
        nb3 = lapse_base[..., None]
        delta_phi = c_squared * (dn / lapse_base)
        grad_delta_phi = c_squared * (grad_dn / nb3 - dn[..., None] * grad_nb / (nb3 * nb3))
        if not all(np.all(np.isfinite(a)) for a in (delta_phi, grad_delta_phi)):
            raise _FailClosed('nonfinite linear lapse potential/gradient')
        for array in (nb, grad_nb, dn, grad_dn, lapse_base, delta_phi, grad_delta_phi):
            array.flags.writeable = False
        work['linear'] = dict(
            label='LINEAR deltaPhi = c^2 dn/Nb; grad = c^2 (grad dn/Nb - dn grad nb/Nb^2)',
            deltaPhi_m2_s2=delta_phi, grad_deltaPhi_cartesian_m_s2=grad_delta_phi)
        checks['linear_finite'] = True
        state['stage'] = 'complete'
    except Exception as exc:  # FloatingPointError under caller errstate included
        return finish('FAILED_CLOSED', exc)
    except BaseException as exc:
        try:
            exc.unt0455_retained_result = finish('INTERRUPTED', exc)
        except Exception:
            pass
        raise
    return finish('COMPLETE', None)


def admit_scalar_force(*, finite_sum, base, c_m_s, gradient_length_scale_m, base_reality_atol,
                       base_reality_rtol, increment_reality_atol, increment_reality_rtol):
    """Reality admission and LINEAR lapse potential/gradient for a COMPLETE finite sum.

    base must be a bind_base record bound to the same point sha256 as finite_sum.
    Checks (all four reported): n_b, L*grad n_b with base tolerances; dn, L*grad dn
    with increment tolerances; then Nb = 1 + Re n_b > 0; then 0449 LINEAR forms.
    Complex dn and grad dn are retained in the output. No Hessian.
    """
    try:
        dn_c, grad_dn_c, identity = _check_finite_sum(finite_sum)
        base = _check_base(base)
        if base['point_sha256'] != identity.get('point_sha256'):
            raise _InvalidInput('base point identity: base bound to points sha256 %s, finite '
                                'sum evaluated on %s' % (base['point_sha256'],
                                                         identity.get('point_sha256')))
        _, c_squared, length, tol = _admission_scalars(
            c_m_s, gradient_length_scale_m,
            dict(base_reality_atol=base_reality_atol, base_reality_rtol=base_reality_rtol,
                 increment_reality_atol=increment_reality_atol,
                 increment_reality_rtol=increment_reality_rtol))
    except Exception as exc:
        return _invalid(exc, 'validation', dn_complex=None, grad_dn_complex=None,
                        deltaPhi_m2_s2=None, grad_deltaPhi_cartesian_m_s2=None, hessian=HESSIAN)
    extra = dict(finite_sum_identity=dict(identity), c_m_s=float(c_m_s),
                 gradient_length_scale_m=length, tolerances=tol)
    return _admit(dn_c, grad_dn_c, base, c_squared, length, tol, extra)


def exact_scalar_force(*, geometry, base, wavevectors, amplitudes, x_m, y_m, z_m, c_m_s,
                       gradient_length_scale_m, base_reality_atol, base_reality_rtol,
                       increment_reality_atol, increment_reality_rtol):
    """exact_finite_sum then admit_scalar_force, every input validated before any sum.

    Returns a fail-closed dict with the admission payload at top level when COMPLETE
    and both stage results under 'finite_sum' and 'admission'.
    """
    tolerances = dict(base_reality_atol=base_reality_atol, base_reality_rtol=base_reality_rtol,
                      increment_reality_atol=increment_reality_atol,
                      increment_reality_rtol=increment_reality_rtol)
    try:
        checked = _check_geometry(geometry)
        _check_identity(checked, wavevectors, x_m, y_m, z_m)
        checked_base = _check_base(base)
        if checked_base['point_sha256'] != checked['point_sha256']:
            raise _InvalidInput('base point identity: base bound to points sha256 %s, geometry '
                                'points sha256 %s' % (checked_base['point_sha256'],
                                                      checked['point_sha256']))
        _admission_scalars(c_m_s, gradient_length_scale_m, tolerances)
    except Exception as exc:
        return _invalid(exc, 'validation', finite_sum=None, admission=None, hessian=HESSIAN)
    finite_sum = exact_finite_sum(geometry=geometry, wavevectors=wavevectors,
                                  amplitudes=amplitudes, x_m=x_m, y_m=y_m, z_m=z_m)
    if finite_sum['status'] != 'COMPLETE':
        return dict(status=finite_sum['status'], complete=False, reason=finite_sum['reason'],
                    failure_stage='finite_sum:' + str(finite_sum['failure_stage']),
                    exception_type=finite_sum['exception_type'], finite_sum=finite_sum,
                    admission=None, hessian=HESSIAN, convention=CONVENTION,
                    retained=finite_sum.get('retained'))
    admission = admit_scalar_force(finite_sum=finite_sum, base=base, c_m_s=c_m_s,
                                   gradient_length_scale_m=gradient_length_scale_m, **tolerances)
    result = dict(admission)
    result.update(finite_sum=finite_sum, admission=admission)
    if admission['status'] != 'COMPLETE':
        result['failure_stage'] = 'admission:' + str(admission['failure_stage'])
    return result
