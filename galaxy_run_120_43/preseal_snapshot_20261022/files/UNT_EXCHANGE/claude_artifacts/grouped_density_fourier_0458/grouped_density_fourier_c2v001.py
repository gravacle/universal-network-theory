"""INERT exact grouped regrouping of the 0445 nonzero-mode density Fourier source sum;
UNT task 0458, c2v001.

Task 0458 file sha256 18eb2dba463378903a952fd408d1f3b8a5cff9fc9be1b580921cbab9c1e51fdf.
Read-only references (never imported here): 0445 contraction nonzero_density_fourier_c2v001.py
sha256 255e09f4889b6ed470e3424d3a3c41f3a21c433f3095e04ea12af7a96bc5aaf4; 0445 Jn provider
posix_libm_bessel_jn_provider_c2v001.py sha256
9ec3f1c9fb8afe1ffa4a2bb24df5daf4d2695aa51574984658cb753cfc304f67 (the caller injects its
READY dict unchanged); cache/custody pattern exact_scalar_force_c2v001.py sha256
0dab62be91cfd793949ef251aa3e731b4544e7131606599784762cb4101175ea.

Finite law, identical to 0445 (unchanged):
  deltaJ0(k) = -c^2 * 2pi * (-i)^m * sum_q [ w_q J_m(k_perp R_q) exp(-i k_z z_q)
               * ( rho_m(q) exp(+i m alpha_k) + conj(rho_m(q)) exp(-i m alpha_k) ) ]
  k_perp = numpy.hypot(k_x, k_y), alpha_k = numpy.arctan2(k_y, k_x) on the signed inputs,
  w_q = R dR dz WITHOUT 2pi, m in 1..6.
No extra factor 2, no conjugated vertical exponential on the negative branch, no angle
symmetry, interpolation, mode dropping, Fourier weight or native inverse.

Exact regrouping (changes floating-point summation order only):
  waves      bitwise-equal k_z groups z and bitwise-equal computed k_perp groups p; the
             filled cells c = (z, p) that actual waves occupy; every wave keeps its own
             alpha_k and its position in the output (duplicates and holes retained).
  positions  bitwise-equal R groups r with arbitrary z_q and w_q inside a group; slots s
             list q by group (stable: ascending q inside a group); no Cartesian
             completeness or equal-z assumption.
  cached     (source independent, bound to the actual inputs by sha256):
             E[s, z]       = exp(-1j*(k_z[z]*z_q)), q = position_order[s]
             J[mode, p, r] = J_m(k_perp[p]*R[r]) from the injected provider
             P[mode, k]    = exp(1j*(m*alpha_k)); group maps.
  per call   (never cached): A[s, 0] = w_q*rho_q, A[s, 1] = w_q*conj(rho_q)
             V[r, b, z] = SUM_{s in r} A[s, b] E[s, z]  (both branches use the SAME E)
             T[b, c]    = SUM_r V[r, b, z_c] J[mode, p_c, r]
             deltaJ0(k) = (-(c*c)*(2*pi)) * ((-i)^m * (T[0, c_k] P[k] + T[1, c_k] conj(P[k])))
Every q enters exactly one R group once. No (wave, position) table is formed.
numpy + stdlib only; no BLAS products (contractions are np.einsum(optimize=False)); no
floating-point warning suppression (the caller's numpy.errstate governs; a
FloatingPointError fails closed with retention; numpy.einsum itself raises no
floating-point flags, so every stage also checks finiteness explicitly); no file I/O;
keyword-only arguments without defaults; fail-closed result dicts; definitions only at
import.
"""
import hashlib
import math
import numbers
import time
from collections.abc import Mapping
from types import MappingProxyType

import numpy as np


TASK_0458_SHA256 = '18eb2dba463378903a952fd408d1f3b8a5cff9fc9be1b580921cbab9c1e51fdf'
REFERENCE_0445_SHA256 = '255e09f4889b6ed470e3424d3a3c41f3a21c433f3095e04ea12af7a96bc5aaf4'
PROVIDER_0445_SHA256 = '9ec3f1c9fb8afe1ffa4a2bb24df5daf4d2695aa51574984658cb753cfc304f67'
PATTERN_0455_SHA256 = '0dab62be91cfd793949ef251aa3e731b4544e7131606599784762cb4101175ea'
MODULE_VERSION = 'c2v001'
GEOMETRY_KIND = 'UNT0458_GROUPED_DENSITY_GEOMETRY_C2V001'
PREPARE_KIND = 'UNT0458_PREPARE_RESULT_C2V001'
RESULT_KIND = 'UNT0458_GROUPED_DENSITY_FOURIER_RESULT_C2V001'
ADAPTER_KIND = 'UNT0458_0445_KEYWORD_ADAPTER_C2V001'
INTERRUPT_ATTRIBUTE = 'unt0458_retained_result'
INTERRUPT_ATTRIBUTE_0445 = 'unt0445_retained_result'

EQUATION_0445 = (
    'deltaJ0(k) = -c^2 * 2pi * (-i)^m * sum_q [ w_q J_m(k_perp R_q) exp(-i k_z z_q) '
    '* ( rho_m(q) exp(+i m alpha_k) + conj(rho_m(q)) exp(-i m alpha_k) ) ], '
    'alpha_k = atan2(k_y, k_x), w_q = R dR dz WITHOUT 2pi')
UNIT_CHAIN = ('c^2 [m^2 s^-2] x w_q [m^3] x rho_m [kg m^-3] (2pi, (-i)^m, J_m, '
              'exp factors dimensionless) = kg m^2 s^-2 = J')
ACCUMULATION_ORDER = (
    'A[s,0] = w*rho, A[s,1] = w*conj(rho) (numpy.multiply, slots s in R-group order); '
    "V[r] = numpy.einsum('sb,sz->bz', A[group r], E[group r], optimize=False) "
    '(sequential over s ascending inside the group, as observed); '
    "T[:, cells] = numpy.einsum('rb,cr->bc', V[:, :, z], J[mode][cell perps], "
    'optimize=False) per k_z group (sequential over r ascending, as observed); per wave '
    'acc = T[0,c]*P + T[1,c]*conj(P), then (-i)^m (exact unit) multiplies acc, then the '
    'real scale -(c*c)*(2*pi). Output observed bitwise independent of wave_chunk, '
    'position_chunk, cell_chunk and perp_chunk; differs from 0445 by summation order only.')
ALPHA_AT_K_PERP_ZERO = (
    'alpha_k = numpy.arctan2(k_y, k_x) per wave, also at k_perp = 0 where it is finite '
    '(0, -0, pi or -pi by signed zeros); never divided by k_perp; the provider must return '
    'J_m(0) = 0 exactly (m >= 1) wherever k_perp*R == 0, so the k_perp = 0 Bessel row is '
    'exactly zero, and k_perp = 0 outputs are checked to equal 0 exactly.')

CONVENTION = MappingProxyType(dict(
    task_sha256=TASK_0458_SHA256,
    reference_0445_sha256=REFERENCE_0445_SHA256,
    provider_0445_sha256=PROVIDER_0445_SHA256,
    pattern_0455_sha256=PATTERN_0455_SHA256,
    module_version=MODULE_VERSION,
    equation=EQUATION_0445,
    unit_chain=UNIT_CHAIN,
    accumulation_order=ACCUMULATION_ORDER,
    alpha_at_k_perp_zero=ALPHA_AT_K_PERP_ZERO,
    source_coordinate=0,
    weights='w_q = R dR dz WITHOUT 2pi',
    fourier_sign='source Fourier exp(-i k.x)',
    grouping=('waves: bitwise-equal float64 k_z (so +0.0 and -0.0 are separate groups) and '
              'bitwise-equal computed k_perp = numpy.hypot(k_x, k_y); filled (k_z, k_perp) '
              'cells only; original wave order, alpha, duplicates and holes kept. positions: '
              'bitwise-equal float64 R, arbitrary z and w per group'),
    caching=('E = exp(-1j*(k_z*z_q)) per (slot, k_z group); J_m(k_perp*R) per (mode, '
             'k_perp group, R group); exp(1j*(m*alpha)) per (mode, wave); group maps. No '
             'rho-dependent quantity is cached'),
    identity=('geometry reuse requires sha256-identical float64 waves (nk,3), radius, z and '
              'weights (dtype, shape, bytes), a bound mode, the identical bessel_jn object, '
              'an unchanged geometry digest and an unchanged convention digest'),
    excluded=('native inversion, normalization, mass adjustment, pressure source, '
              'acceptance, interpolation, symmetry, mode dropping, file I/O')))

# (-i)^m for m mod 4 = 0, 1, 2, 3; exact unit values, no complex power evaluation (0445).
_MINUS_I_POWER = (complex(1.0, 0.0), complex(0.0, -1.0),
                  complex(-1.0, 0.0), complex(0.0, 1.0))
_PROVIDER_COUNTERS = ('calls', 'evaluations', 'cache_hits', 'cache_evictions', 'cache_entries')


class _InvalidInput(ValueError):
    """Input contract violation detected before any evaluation."""


class _FailClosed(ValueError):
    """Runtime contract violation; evaluation stopped."""


# ----------------------------------------------------------------------------- helpers

def _real_vector(value, name):
    # 0445 rule, verbatim semantics.
    array = np.asarray(value)
    kind = array.dtype.kind
    if kind not in 'fiu' or (kind == 'f' and array.dtype.itemsize > 8):
        raise _InvalidInput(name + ': real float64-representable dtype required, got '
                            + str(array.dtype))
    if array.ndim != 1:
        raise _InvalidInput(name + ': 1-D array required, got shape ' + str(array.shape))
    array = np.array(array, dtype=np.float64, copy=True)
    if not np.all(np.isfinite(array)):
        raise _InvalidInput(name + ': finite values required')
    return array


def _positions(radius_m, z_m, weights_RdRdz_m3):
    radius = _real_vector(radius_m, 'radius_m')
    height = _real_vector(z_m, 'z_m')
    weight = _real_vector(weights_RdRdz_m3, 'weights_RdRdz_m3')
    if radius.shape[0] < 1:
        raise _InvalidInput('radius_m: at least one position required')
    if height.shape != radius.shape or weight.shape != radius.shape:
        raise _InvalidInput('radius_m, z_m, weights_RdRdz_m3: identical length required')
    if np.any(radius <= 0.0):
        raise _InvalidInput('radius_m: strictly positive radii required')
    if np.any(weight <= 0.0):
        raise _InvalidInput('weights_RdRdz_m3: strictly positive weights required')
    return radius, height, weight


def _waves(k_physical_inverse_m):
    waves = np.asarray(k_physical_inverse_m)
    kind = waves.dtype.kind
    if kind not in 'fiu' or (kind == 'f' and waves.dtype.itemsize > 8):
        raise _InvalidInput('k_physical_inverse_m: real dtype required, got ' + str(waves.dtype))
    if waves.ndim != 2 or waves.shape[1] != 3 or waves.shape[0] < 1:
        raise _InvalidInput('k_physical_inverse_m: shape (nk, 3) with nk >= 1 required')
    waves = np.array(waves, dtype=np.float64, copy=True, order='C')
    if not np.all(np.isfinite(waves)):
        raise _InvalidInput('k_physical_inverse_m: finite values required')
    return waves


def _rho(rho_mode_kg_m3, count):
    rho = np.asarray(rho_mode_kg_m3)
    if rho.dtype.kind != 'c' or rho.dtype.itemsize > 16:
        raise _InvalidInput('rho_mode_kg_m3: complex64/complex128 dtype required, got '
                            + str(rho.dtype))
    if rho.shape != (count,):
        raise _InvalidInput('rho_mode_kg_m3: shape (q,) matching radius_m required')
    rho = np.array(rho, dtype=np.complex128, copy=True)
    if not np.all(np.isfinite(rho)):
        raise _InvalidInput('rho_mode_kg_m3: finite values required')
    return rho


def _c_squared(c_m_s):
    if isinstance(c_m_s, (bool, np.bool_)) or not isinstance(c_m_s, numbers.Real):
        raise _InvalidInput('c_m_s: real number required')
    c = float(c_m_s)
    c_squared = c * c
    if not (math.isfinite(c) and c > 0.0 and math.isfinite(c_squared) and c_squared > 0.0):
        raise _InvalidInput('c_m_s: finite positive value with finite positive square required')
    return c_squared


def _positive_int(value, name):
    if type(value) is not int or value < 1:
        raise _InvalidInput(name + ': positive int required (bool and numpy ints rejected)')
    return value


def _modes(modes):
    if not isinstance(modes, (tuple, list)) or len(modes) < 1:
        raise _InvalidInput('modes: nonempty tuple or list of int in 1..6 required')
    for m in modes:
        if type(m) is not int or not 1 <= m <= 6:
            raise _InvalidInput('modes: every mode must be a Python int in 1..6 (bool, numpy '
                                'ints and floats rejected)')
    if len(set(modes)) != len(modes):
        raise _InvalidInput('modes: duplicate modes rejected')
    return tuple(sorted(modes))


def _digest(label, arrays):
    """sha256 over label, then (dtype, shape, C-order bytes) of each array (0455 pattern)."""
    h = hashlib.sha256()
    h.update(label.encode('ascii'))
    for array in arrays:
        array = np.ascontiguousarray(array)
        h.update(('|%s|%r|' % (array.dtype.str, array.shape)).encode('ascii'))
        h.update(array.reshape(-1).view(np.uint8))
    return h.hexdigest()


def _text_digest(label, mapping):
    h = hashlib.sha256()
    h.update(label.encode('ascii'))
    for key in sorted(mapping):
        h.update(('\n%s=%r' % (key, mapping[key])).encode('utf-8'))
    return h.hexdigest()


def _convention_sha256():
    return _text_digest('convention', dict(CONVENTION))


def _provider(jn_provider):
    """READY gate (0449/0452 pattern) and static provenance snapshot."""
    if not isinstance(jn_provider, Mapping) or jn_provider.get('status') != 'READY' \
            or not callable(jn_provider.get('bessel_jn')):
        raise _InvalidInput("jn_provider: provider dict with status 'READY' and callable "
                            'bessel_jn required')
    metadata = jn_provider.get('metadata')
    if not isinstance(metadata, Mapping):
        raise _InvalidInput('jn_provider: metadata mapping required for provenance')
    bessel_jn = jn_provider['bessel_jn']
    static = {str(key): repr(value) for key, value in metadata.items()
              if key not in _PROVIDER_COUNTERS}
    static['callable_qualname'] = repr(getattr(bessel_jn, '__qualname__', type(bessel_jn).__name__))
    static['callable_module'] = repr(getattr(bessel_jn, '__module__', None))
    provenance = MappingProxyType(static)
    return bessel_jn, provenance, _text_digest('provider_provenance', static)


def _provider_values(bessel_jn, mode, argument, zero_argument):
    # 0445 provider checks, verbatim semantics.
    values = np.asarray(bessel_jn(mode, argument))
    if values.shape != argument.shape:
        raise _FailClosed('bessel_jn returned shape ' + str(values.shape)
                          + ' for argument shape ' + str(argument.shape))
    if values.dtype != np.float64:
        raise _FailClosed('bessel_jn must return real float64, got ' + str(values.dtype))
    if not np.all(np.isfinite(values)):
        raise _FailClosed('bessel_jn returned nonfinite values')
    if np.any(np.abs(values) > 1.0):
        raise _FailClosed('bessel_jn violated |J_m(x)| <= 1 for real x')
    if np.any(values[zero_argument] != 0.0):
        raise _FailClosed('bessel_jn violated J_m(0) = 0 for m >= 1 (J0 substitution?)')
    return values


def _group_exact(values):
    """Bitwise-exact groups of a finite float64 vector.

    Returns (group index per entry, group values). Groups are ordered numerically, with
    +0.0 before -0.0 when both occur; members of a group share identical float64 bits.
    """
    bits = np.ascontiguousarray(values, dtype=np.float64).view(np.uint64)
    unique_bits, inverse = np.unique(bits, return_inverse=True)
    unique_values = unique_bits.view(np.float64)
    order = np.lexsort((unique_bits, unique_values))
    rank = np.empty(order.shape[0], dtype=np.intp)
    rank[order] = np.arange(order.shape[0], dtype=np.intp)
    index = rank[inverse.reshape(-1)]
    return index, unique_values[order].copy()


# ----------------------------------------------------------------------------- scaling

def scaling(*, nq, nk, n_kz_unique, n_perp_unique, n_R_unique, n_cells, n_modes,
            max_cells_per_kz, position_chunk, perp_chunk, cell_chunk):
    """Exact element, byte and operation counts for one geometry (pure arithmetic).

    Element counts are what prepare_geometry checks against the caller limits before any
    cache allocation. Returns dict(status 'COMPLETE', entries, bytes, operations) or
    dict(status 'INVALID_INPUT', reason) when an argument is not a positive Python int.
    """
    try:
        plan = _scaling(nq, nk, n_kz_unique, n_perp_unique, n_R_unique, n_cells, n_modes,
                        max_cells_per_kz, position_chunk, perp_chunk, cell_chunk)
    except Exception as exc:
        return dict(status='INVALID_INPUT', complete=False, reason=str(exc),
                    exception_type=type(exc).__name__, entries=None, bytes=None,
                    operations=None)
    return dict(status='COMPLETE', complete=True, reason=None, exception_type=None, **plan)


def _scaling(nq, nk, n_kz_unique, n_perp_unique, n_R_unique, n_cells, n_modes,
             max_cells_per_kz, position_chunk, perp_chunk, cell_chunk):
    names = dict(nq=nq, nk=nk, n_kz_unique=n_kz_unique, n_perp_unique=n_perp_unique,
                 n_R_unique=n_R_unique, n_cells=n_cells, n_modes=n_modes,
                 max_cells_per_kz=max_cells_per_kz, position_chunk=position_chunk,
                 perp_chunk=perp_chunk, cell_chunk=cell_chunk)
    for name, value in names.items():
        _positive_int(value, name)
    nz, npp, nr = n_kz_unique, n_perp_unique, n_R_unique
    entries = dict(
        vertical_cache=nz * nq,                                   # complex128
        bessel_cache=n_modes * npp * nr,                          # float64
        angular_cache=n_modes * nk,                               # complex128
        work_per_evaluation=4 * nq + 2 * nr * nz + 2 * n_cells + nk,   # complex128
        prepare_phase_block=min(position_chunk, nq) * nz,         # float64 + complex128
        provider_block=min(perp_chunk, npp) * nr,                 # float64 argument
        cell_gather_block=min(cell_chunk, max_cells_per_kz) * nr)  # float64 J rows
    map_bytes = (8 * (3 * nk + 2 * n_cells + (nz + 1) + 2 * nq + (nr + 1))
                 + 8 * (nz + npp + nr) + 8 * nq + 16 * nk + nk)
    nbytes = dict(
        vertical_cache=16 * entries['vertical_cache'],
        bessel_cache=8 * entries['bessel_cache'],
        angular_cache=16 * entries['angular_cache'],
        group_maps_and_vectors=map_bytes,
        work_per_evaluation=16 * entries['work_per_evaluation'],
        prepare_phase_block=24 * entries['prepare_phase_block'],
        provider_block_excluding_provider_internals=17 * entries['provider_block'],
        cell_gather_block=8 * entries['cell_gather_block'],
        validation_copies_per_call=8 * (3 * nq + 3 * nk))
    nbytes['geometry_digest_bytes'] = (nbytes['vertical_cache'] + nbytes['bessel_cache']
                                       + nbytes['angular_cache'] + map_bytes)
    operations = dict(
        prepare=dict(hypot=nk, arctan2=nk, vertical_real_products=nz * nq,
                     vertical_complex_exp=nz * nq, bessel_argument_products=n_modes * npp * nr,
                     provider_elements=n_modes * npp * nr, angular_complex_exp=n_modes * nk,
                     provider_calls=n_modes * (-(-npp // perp_chunk))),
        evaluate_per_mode=dict(source_weighting_real_by_complex=2 * nq,
                               scatter_complex_mac=2 * nq * nz,
                               cell_complex_by_real_mac=2 * n_cells * nr,
                               cell_gather_float_copies=n_cells * nr,
                               gather_complex_products=2 * nk, gather_complex_adds=nk,
                               prefactor_complex_products=2 * nk,
                               scatter_einsum_calls=nr,
                               cell_einsum_calls_upper_bound=nz + n_cells // cell_chunk,
                               digest_bytes_hashed=nbytes['geometry_digest_bytes']
                               + 8 * (3 * nq + 3 * nk)),
        direct_0445_equivalent_terms=nk * nq)
    return dict(entries=entries, bytes=nbytes, operations=operations)


# ----------------------------------------------------------------------------- geometry

_GEOMETRY_ARRAYS = ('kz_unique', 'kperp_unique', 'R_unique', 'wave_kz_index', 'wave_perp_index',
                    'wave_cell_index', 'cell_kz_index', 'cell_perp_index', 'kz_cell_offsets',
                    'position_r_index', 'position_order', 'r_offsets', 'weights_sorted',
                    'k_perp', 'alpha', 'perp_zero', 'angular_plus', 'vertical_phase', 'bessel')
_GEOMETRY_TEXT = ('kind', 'module_version', 'task_sha256', 'convention_sha256', 'wave_sha256',
                  'radius_sha256', 'z_sha256', 'weight_sha256', 'provider_provenance_sha256')


def _geometry_digest(record):
    header = '|'.join([str(record[key]) for key in _GEOMETRY_TEXT]
                      + ['modes=%r' % (tuple(record['modes']),)]
                      + ['%s=%r' % (key, record['counts'][key]) for key in sorted(record['counts'])]
                      + ['%s=%r' % (key, record['controls'][key])
                         for key in sorted(record['controls'])])
    return _digest('geometry|' + header, [record[key] for key in _GEOMETRY_ARRAYS])


def _check_geometry(geometry):
    if not isinstance(geometry, Mapping) or geometry.get('kind') != GEOMETRY_KIND:
        raise _InvalidInput('geometry: a prepare_geometry(...)["geometry"] record required')
    if geometry.get('convention_sha256') != _convention_sha256():
        raise _InvalidInput('geometry: convention digest differs from this module (stale '
                            'convention or module version); prepare a new geometry')
    try:
        digest = _geometry_digest(geometry)
    except Exception as exc:
        raise _InvalidInput('geometry: record incomplete or malformed (%s)' % (exc,))
    if digest != geometry.get('geometry_sha256'):
        raise _InvalidInput('geometry: stored arrays or counts changed since preparation '
                            '(digest mismatch); prepare a new geometry')
    if not callable(geometry.get('provider_bessel_jn')):
        raise _InvalidInput('geometry: bound provider callable missing')
    provenance = geometry.get('provider_provenance')
    if not isinstance(provenance, Mapping) or _text_digest(
            'provider_provenance', dict(provenance)) != geometry.get('provider_provenance_sha256'):
        raise _InvalidInput('geometry: provider provenance changed since preparation')
    return geometry


def _prepare_invalid(exc, stage, timing):
    return dict(kind=PREPARE_KIND, status='INVALID_INPUT', complete=False, geometry=None,
                geometry_sha256=None, reason=str(exc), failure_stage=stage,
                exception_type=type(exc).__name__, counts=None, scaling=None, limits=None,
                timing=timing, retained=None, convention=CONVENTION)


def prepare_geometry(*, radius_m, z_m, weights_RdRdz_m3, k_physical_inverse_m, modes,
                     jn_provider, position_chunk, perp_chunk, cell_chunk,
                     max_vertical_entries, max_bessel_entries, max_angular_entries,
                     max_work_entries, max_block_entries):
    """Group waves and positions once and cache the source-independent factors.

    Inputs follow the 0445 contract (radius > 0, weights > 0, finite real, k (nk, 3)
    signed). modes: tuple/list of distinct Python ints in 1..6. jn_provider: the READY
    dict of the unchanged 0445 provider (status 'READY', callable bessel_jn, metadata).
    position_chunk (slots per vertical-phase block), perp_chunk (k_perp groups per
    provider call) and cell_chunk (cells per J-row gather at evaluation) are positive
    ints. Every limit is a positive int element count checked BEFORE the corresponding
    allocation (see scaling()): max_vertical_entries >= n_kz*nq, max_bessel_entries >=
    n_modes*n_perp*n_R, max_angular_entries >= n_modes*nk, max_work_entries >= the
    per-evaluation work, max_block_entries >= every block transient. Returns a fail-closed
    dict; COMPLETE -> 'geometry' (read-only record). Interrupts are re-raised with the
    retained dict attached as attribute unt0458_retained_result.
    """
    t0 = time.perf_counter()
    timing = dict(validation_s=None, grouping_s=None, angular_s=None, vertical_s=None,
                  bessel_s=None, digest_s=None, total_s=None)
    try:
        controls = dict(position_chunk=_positive_int(position_chunk, 'position_chunk'),
                        perp_chunk=_positive_int(perp_chunk, 'perp_chunk'),
                        cell_chunk=_positive_int(cell_chunk, 'cell_chunk'),
                        max_vertical_entries=_positive_int(max_vertical_entries,
                                                           'max_vertical_entries'),
                        max_bessel_entries=_positive_int(max_bessel_entries, 'max_bessel_entries'),
                        max_angular_entries=_positive_int(max_angular_entries,
                                                          'max_angular_entries'),
                        max_work_entries=_positive_int(max_work_entries, 'max_work_entries'),
                        max_block_entries=_positive_int(max_block_entries, 'max_block_entries'))
        mode_tuple = _modes(modes)
        bessel_jn, provenance, provenance_sha = _provider(jn_provider)
        radius, height, weight = _positions(radius_m, z_m, weights_RdRdz_m3)
        waves = _waves(k_physical_inverse_m)
    except Exception as exc:
        timing['total_s'] = time.perf_counter() - t0
        return _prepare_invalid(exc, 'validation', timing)
    except BaseException as exc:
        try:
            timing['total_s'] = time.perf_counter() - t0
            record = _prepare_invalid(exc, 'validation', timing)
            record['status'] = 'INTERRUPTED'
            setattr(exc, INTERRUPT_ATTRIBUTE, record)
        except Exception:
            pass
        raise
    timing['validation_s'] = time.perf_counter() - t0

    nk, nq, n_modes = int(waves.shape[0]), int(radius.shape[0]), len(mode_tuple)
    identity = dict(wave_sha256=_digest('k_physical_inverse_m', [waves]),
                    radius_sha256=_digest('radius_m', [radius]),
                    z_sha256=_digest('z_m', [height]),
                    weight_sha256=_digest('weights_RdRdz_m3', [weight]),
                    provider_provenance_sha256=provenance_sha)
    counts = dict(nk=nk, nq=nq, n_modes=n_modes)
    work = dict(vertical_phase=None, vertical_slot_mask=None, bessel=None, bessel_row_mask=None,
                angular_plus=None)
    tally = dict(provider_calls=0, provider_elements=0, zero_argument_elements=0,
                 vertical_blocks=0, realized_max_block_entries=0)
    state = dict(stage='wave_geometry', block=None)
    holder = dict(scaling=None)

    def finish(status, exc, geometry=None):
        timing['total_s'] = time.perf_counter() - t0
        result = dict(kind=PREPARE_KIND, status=status, complete=status == 'COMPLETE',
                      geometry=geometry, reason=None, failure_stage=None, exception_type=None,
                      failure_block=state['block'], counts=dict(counts, **tally),
                      scaling=holder['scaling'], limits=dict(controls), identity=dict(identity),
                      timing=dict(timing), retained=None, convention=CONVENTION)
        if status == 'COMPLETE':
            result['geometry_sha256'] = geometry['geometry_sha256']
        else:
            result.update(reason=str(exc), failure_stage=state['stage'],
                          exception_type=type(exc).__name__, retained=dict(work),
                          geometry_sha256=None)
        return result

    try:
        t1 = time.perf_counter()
        k_x, k_y, k_z = waves[:, 0], waves[:, 1], waves[:, 2]
        k_perp = np.hypot(k_x, k_y)                                # k_perp (0445 L236)
        alpha = np.arctan2(k_y, k_x)                               # alpha_k (0445 L237)
        if not (np.all(np.isfinite(k_perp)) and np.all(np.isfinite(alpha))):
            raise _FailClosed('nonfinite k_perp or alpha_k')
        perp_zero = k_perp == 0.0

        state['stage'] = 'grouping'
        wave_kz_index, kz_unique = _group_exact(k_z)
        wave_perp_index, kperp_unique = _group_exact(k_perp)
        position_r_index, R_unique = _group_exact(radius)
        n_kz, n_perp = int(kz_unique.shape[0]), int(kperp_unique.shape[0])
        n_R = int(R_unique.shape[0])
        cell_key = wave_kz_index.astype(np.int64) * n_perp + wave_perp_index.astype(np.int64)
        cell_keys, wave_cell_index = np.unique(cell_key, return_inverse=True)
        wave_cell_index = wave_cell_index.reshape(-1).astype(np.intp)
        cell_kz_index = (cell_keys // n_perp).astype(np.intp)
        cell_perp_index = (cell_keys % n_perp).astype(np.intp)
        n_cells = int(cell_keys.shape[0])
        kz_cell_offsets = np.searchsorted(cell_kz_index, np.arange(n_kz + 1), side='left')
        kz_cell_offsets = kz_cell_offsets.astype(np.intp)
        position_order = np.argsort(position_r_index, kind='stable').astype(np.intp)
        group_sizes = np.bincount(position_r_index, minlength=n_R)
        r_offsets = np.zeros(n_R + 1, dtype=np.intp)
        np.cumsum(group_sizes, out=r_offsets[1:])
        cells_per_kz = np.diff(kz_cell_offsets)
        if not (r_offsets[-1] == nq and np.all(group_sizes >= 1) and np.all(cells_per_kz >= 1)
                and np.array_equal(np.sort(position_order), np.arange(nq))
                and np.array_equal(position_r_index[position_order],
                                   np.repeat(np.arange(n_R), group_sizes))):
            raise _FailClosed('grouping invariant violated (partition of q or cells)')
        weights_sorted = weight[position_order]
        counts.update(n_kz_unique=n_kz, n_perp_unique=n_perp, n_R_unique=n_R, n_cells=n_cells,
                      dense_cells=n_kz * n_perp, max_cells_per_kz=int(np.max(cells_per_kz)),
                      max_positions_per_R=int(np.max(group_sizes)),
                      k_perp_zero_waves=int(np.count_nonzero(perp_zero)),
                      distinct_wave_rows=int(np.unique(waves.view(np.uint64), axis=0).shape[0]))
        timing['grouping_s'] = time.perf_counter() - t1

        state['stage'] = 'cache_limit'
        plan = _scaling(nq, nk, n_kz, n_perp, n_R, n_cells, n_modes, counts['max_cells_per_kz'],
                        controls['position_chunk'], controls['perp_chunk'], controls['cell_chunk'])
        holder['scaling'] = plan
        entries = plan['entries']
        over = {}
        for key, limit in (('vertical_cache', 'max_vertical_entries'),
                           ('bessel_cache', 'max_bessel_entries'),
                           ('angular_cache', 'max_angular_entries'),
                           ('work_per_evaluation', 'max_work_entries'),
                           ('prepare_phase_block', 'max_block_entries'),
                           ('provider_block', 'max_block_entries'),
                           ('cell_gather_block', 'max_block_entries')):
            if entries[key] > controls[limit]:
                over[key] = (entries[key], limit, controls[limit])
        if over:
            raise _FailClosed('entry limits exceeded %s; no cache allocated' % (over,))

        state['stage'] = 'angular_phase'
        t1 = time.perf_counter()
        angular_plus = np.empty((n_modes, nk), dtype=np.complex128)
        work['angular_plus'] = angular_plus
        for slot, m in enumerate(mode_tuple):
            angular_plus[slot] = np.exp(1j * (float(m) * alpha))  # exp(+i m alpha_k) (0445 L240)
        if not np.all(np.isfinite(angular_plus)):
            raise _FailClosed('nonfinite exp(i m alpha_k)')
        timing['angular_s'] = time.perf_counter() - t1

        state['stage'] = 'vertical_phase'
        t1 = time.perf_counter()
        vertical = np.empty((nq, n_kz), dtype=np.complex128)
        vertical_mask = np.zeros(nq, dtype=bool)
        work['vertical_phase'] = vertical
        work['vertical_slot_mask'] = vertical_mask
        chunk = controls['position_chunk']
        for u in range(0, nq, chunk):
            v = min(u + chunk, nq)
            state['block'] = dict(slots=(u, v))
            heights = height[position_order[u:v]]
            phase = kz_unique[None, :] * heights[:, None]           # k_z z_q (0445 L260)
            if not np.all(np.isfinite(phase)):
                raise _FailClosed('nonfinite vertical phase k_z z')
            np.exp(-1j * phase, out=vertical[u:v])                  # exp(-i k_z z_q) (0445 L263)
            vertical_mask[u:v] = True
            tally['vertical_blocks'] += 1
            tally['realized_max_block_entries'] = max(tally['realized_max_block_entries'],
                                                      phase.size)
        timing['vertical_s'] = time.perf_counter() - t1

        state['stage'] = 'bessel_argument'
        t1 = time.perf_counter()
        bessel = np.empty((n_modes, n_perp, n_R), dtype=np.float64)
        bessel_mask = np.zeros((n_modes, n_perp), dtype=bool)
        work['bessel'] = bessel
        work['bessel_row_mask'] = bessel_mask
        chunk = controls['perp_chunk']
        for slot, m in enumerate(mode_tuple):
            for p0 in range(0, n_perp, chunk):
                p1 = min(p0 + chunk, n_perp)
                state['block'] = dict(mode=m, perp_groups=(p0, p1))
                state['stage'] = 'bessel_argument'
                argument = kperp_unique[p0:p1, None] * R_unique[None, :]  # k_perp R (0445 L247)
                if not np.all(np.isfinite(argument)):
                    raise _FailClosed('nonfinite Bessel argument k_perp R')
                argument.flags.writeable = False
                zero_argument = argument == 0.0
                tally['realized_max_block_entries'] = max(tally['realized_max_block_entries'],
                                                          argument.size)
                state['stage'] = 'bessel_provider'
                tally['provider_calls'] += 1
                tally['provider_elements'] += argument.size
                bessel[slot, p0:p1] = _provider_values(bessel_jn, m, argument, zero_argument)
                tally['zero_argument_elements'] += int(np.count_nonzero(zero_argument))
                bessel_mask[slot, p0:p1] = True
        timing['bessel_s'] = time.perf_counter() - t1

        state['stage'] = 'record'
        state['block'] = None
        t1 = time.perf_counter()
        counts.update(zero_argument_elements=tally['zero_argument_elements'],
                      provider_calls=tally['provider_calls'],
                      provider_elements=tally['provider_elements'])
        record = dict(kind=GEOMETRY_KIND, module_version=MODULE_VERSION,
                      task_sha256=TASK_0458_SHA256, convention_sha256=_convention_sha256(),
                      modes=mode_tuple,
                      provider_bessel_jn=bessel_jn, provider_provenance=provenance,
                      kz_unique=kz_unique, kperp_unique=kperp_unique, R_unique=R_unique,
                      wave_kz_index=wave_kz_index, wave_perp_index=wave_perp_index,
                      wave_cell_index=wave_cell_index, cell_kz_index=cell_kz_index,
                      cell_perp_index=cell_perp_index, kz_cell_offsets=kz_cell_offsets,
                      position_r_index=position_r_index, position_order=position_order,
                      r_offsets=r_offsets, weights_sorted=weights_sorted, k_perp=k_perp,
                      alpha=alpha, perp_zero=perp_zero, angular_plus=angular_plus,
                      vertical_phase=vertical, bessel=bessel,
                      counts=MappingProxyType(dict(counts)),
                      controls=MappingProxyType(dict(controls)), **identity)
        for key in _GEOMETRY_ARRAYS:
            record[key] = np.ascontiguousarray(record[key])
            record[key].flags.writeable = False
        record['geometry_sha256'] = _geometry_digest(record)
        geometry = MappingProxyType(record)
        timing['digest_s'] = time.perf_counter() - t1
        state['stage'] = 'complete'
    except Exception as exc:  # FloatingPointError under caller errstate included
        return finish('FAILED_CLOSED', exc)
    except BaseException as exc:
        try:
            setattr(exc, INTERRUPT_ATTRIBUTE, finish('INTERRUPTED', exc))
        except Exception:
            pass
        raise
    return finish('COMPLETE', None, geometry)


# ----------------------------------------------------------------------------- evaluation

def _base_result(status, nk, count, mode, wave_chunk, position_chunk):
    # 0445 result keys (consumer contract) plus 0458 provenance keys.
    return dict(
        kind=RESULT_KIND, status=status, complete=False, deltaJ0_J=None, units='J',
        reason=None, failure_stage=None, exception_type=None, failure_block=None,
        retained_deltaJ0_J=None, retained_wave_mask=None, completed_wave_chunks=(),
        counts=dict(waves=nk, positions=count, mode=mode),
        chunking=dict(wave_chunk=wave_chunk, position_chunk=position_chunk),
        convention=dict(CONVENTION), provenance=None, timing=None, retained_work=None)


def _evaluate_validate(geometry, radius_m, z_m, weights_RdRdz_m3, rho_mode_kg_m3,
                       k_physical_inverse_m, c_m_s, mode, bessel_jn, wave_chunk, position_chunk):
    if type(mode) is not int or not 1 <= mode <= 6:
        raise _InvalidInput('mode: int in 1..6 required (bool and other types rejected)')
    for name, chunk in (('wave_chunk', wave_chunk), ('position_chunk', position_chunk)):
        if type(chunk) is not int or chunk < 1:
            raise _InvalidInput(name + ': positive int required (bool rejected)')
    if not callable(bessel_jn):
        raise _InvalidInput('bessel_jn: callable (n, x_array) -> float64 array required')
    c_squared = _c_squared(c_m_s)
    geometry = _check_geometry(geometry)
    radius, height, weight = _positions(radius_m, z_m, weights_RdRdz_m3)
    rho = _rho(rho_mode_kg_m3, radius.shape[0])
    waves = _waves(k_physical_inverse_m)
    if _digest('k_physical_inverse_m', [waves]) != geometry['wave_sha256']:
        raise _InvalidInput('wave identity: k_physical_inverse_m is not sha256-identical '
                            '(float64, shape, signed order) to the prepared geometry')
    for label, array, key in (('radius_m', radius, 'radius_sha256'), ('z_m', height, 'z_sha256'),
                              ('weights_RdRdz_m3', weight, 'weight_sha256')):
        if _digest(label, [array]) != geometry[key]:
            raise _InvalidInput('position identity: %s is not sha256-identical to the '
                                'prepared geometry' % label)
    if mode not in tuple(geometry['modes']):
        raise _InvalidInput('mode %d is not bound in this geometry (modes %r)'
                            % (mode, tuple(geometry['modes'])))
    if bessel_jn is not geometry['provider_bessel_jn']:
        raise _InvalidInput('provider identity: bessel_jn is not the provider object bound '
                            'at prepare_geometry')
    return dict(geometry=geometry, rho=rho, c_squared=c_squared, mode=mode,
                wave_chunk=wave_chunk, position_chunk=position_chunk,
                rho_sha256=_digest('rho_mode_kg_m3', [rho]))


def evaluate_mode(*, geometry, radius_m, z_m, weights_RdRdz_m3, rho_mode_kg_m3,
                  k_physical_inverse_m, c_m_s, mode, bessel_jn, wave_chunk, position_chunk):
    """Scalar Fourier increment deltaJ0(k) [J] of one nonzero density harmonic, regrouped.

    The 0445 keyword contract plus a bound geometry. radius_m, z_m, weights_RdRdz_m3 and
    k_physical_inverse_m must be sha256-identical (as validated float64 copies) to the
    prepared geometry, mode must be bound in it, and bessel_jn must be the provider object
    bound at preparation (it is not called: J is cached). wave_chunk = waves gathered and
    committed per block (retention granularity); position_chunk = minimum positions per
    scatter retention batch (whole R groups). Neither changes the arithmetic.
    Returns a fail-closed dict with the 0445 keys: 'COMPLETE' -> deltaJ0_J complex128 (nk,)
    in the caller's wave order; 'INVALID_INPUT' -> nothing evaluated; 'FAILED_CLOSED' ->
    deltaJ0_J None, retained_deltaJ0_J/retained_wave_mask hold committed wave chunks and
    retained_work holds the partial V/T with masks. A non-Exception interruption is
    re-raised with the same dict (status 'INTERRUPTED') attached as unt0458_retained_result.
    """
    t0 = time.perf_counter()
    try:
        ctx = _evaluate_validate(geometry, radius_m, z_m, weights_RdRdz_m3, rho_mode_kg_m3,
                                 k_physical_inverse_m, c_m_s, mode, bessel_jn, wave_chunk,
                                 position_chunk)
    except Exception as exc:  # fail closed: nothing evaluated
        result = _base_result('INVALID_INPUT', None, None, mode if type(mode) is int else None,
                              wave_chunk if type(wave_chunk) is int else None,
                              position_chunk if type(position_chunk) is int else None)
        result.update(reason=str(exc), failure_stage='validation',
                      exception_type=type(exc).__name__,
                      timing=dict(validation_s=time.perf_counter() - t0))
        return result
    except BaseException as exc:
        try:
            result = _base_result('INTERRUPTED', None, None, None, None, None)
            result.update(reason=str(exc), failure_stage='validation',
                          exception_type=type(exc).__name__)
            setattr(exc, INTERRUPT_ATTRIBUTE, result)
        except Exception:
            pass
        raise
    ctx['validation_s'] = time.perf_counter() - t0
    return _evaluate_core(ctx, t0)


def _evaluate_core(ctx, t0):
    geometry, rho, mode = ctx['geometry'], ctx['rho'], ctx['mode']
    wave_chunk, position_chunk = ctx['wave_chunk'], ctx['position_chunk']
    gcounts, controls = geometry['counts'], geometry['controls']
    nk, nq = gcounts['nk'], gcounts['nq']
    n_kz, n_R, n_cells = gcounts['n_kz_unique'], gcounts['n_R_unique'], gcounts['n_cells']
    cell_chunk = controls['cell_chunk']
    slot = tuple(geometry['modes']).index(mode)                  # modes are digest-bound
    unit = _MINUS_I_POWER[mode % 4]                               # (-i)^m, exact (0445 L192)
    scale = -ctx['c_squared'] * (2.0 * math.pi)                   # -c^2 * 2pi (0445 L193)
    nan = complex(math.nan, math.nan)

    retained = np.full(nk, nan, dtype=np.complex128)
    mask = np.zeros(nk, dtype=bool)
    completed = []
    work = dict(source_weighted=None, scatter_V=None, r_group_mask=np.zeros(n_R, dtype=bool),
                cell_T=None, cell_mask=np.zeros(n_cells, dtype=bool))
    tally = dict(scatter_batches=0, r_groups_scattered=0, positions_scattered=0,
                 cell_blocks=0, cells_summed=0, k_perp_zero_waves=0)
    timing = dict(validation_s=ctx['validation_s'], source_weighting_s=None, scatter_s=None,
                  cell_sum_s=None, gather_s=None, total_s=None)
    state = dict(stage='block_limit', block=None)
    provenance = dict(geometry_sha256=geometry['geometry_sha256'],
                      convention_sha256=geometry['convention_sha256'],
                      wave_sha256=geometry['wave_sha256'], radius_sha256=geometry['radius_sha256'],
                      z_sha256=geometry['z_sha256'], weight_sha256=geometry['weight_sha256'],
                      provider_provenance_sha256=geometry['provider_provenance_sha256'],
                      rho_sha256=ctx['rho_sha256'], mode=mode, modes_bound=tuple(geometry['modes']),
                      c_squared=ctx['c_squared'], result_sha256=None)

    def finish(status, exc):
        timing['total_s'] = time.perf_counter() - t0
        result = _base_result(status, nk, nq, mode, wave_chunk, position_chunk)
        result['counts'].update(
            wave_chunks_total=-(-nk // wave_chunk), wave_chunks_completed=len(completed),
            waves_completed=int(np.count_nonzero(mask)), provider_calls=0, provider_elements=0,
            n_kz_unique=n_kz, n_perp_unique=gcounts['n_perp_unique'], n_R_unique=n_R,
            n_cells=n_cells, **tally)
        result['chunking'].update(
            cell_chunk=cell_chunk,
            order=('scatter batches of whole R groups (>= position_chunk positions each, >= 1 '
                   'group) ascending; cells per k_z group in blocks of cell_chunk ascending; '
                   'wave chunks ascending, a wave chunk committed after its prefactor and '
                   'zero checks'))
        result['completed_wave_chunks'] = tuple(completed)
        result['retained_wave_mask'] = mask
        result['provenance'] = provenance
        result['timing'] = dict(timing)
        if status == 'COMPLETE':
            retained.flags.writeable = False
            provenance['result_sha256'] = _digest('deltaJ0_J', [retained])
            result['complete'] = True
            result['deltaJ0_J'] = retained
        else:
            result['retained_deltaJ0_J'] = retained
            result['retained_work'] = work
            result['reason'] = str(exc)
            result['failure_stage'] = state['stage']
            result['failure_block'] = state['block']
            result['exception_type'] = type(exc).__name__
        return result

    try:
        if min(wave_chunk, nk) > controls['max_block_entries']:
            raise _FailClosed('wave block min(wave_chunk, nk) = %d exceeds max_block_entries = '
                              '%d; nothing allocated' % (min(wave_chunk, nk),
                                                          controls['max_block_entries']))
        state['stage'] = 'source_weighting'
        t1 = time.perf_counter()
        order = geometry['position_order']
        weights_sorted = geometry['weights_sorted']
        rho_sorted = rho[order]
        source = np.empty((nq, 2), dtype=np.complex128)
        np.multiply(weights_sorted, rho_sorted, out=source[:, 0])           # w_q rho_q
        np.conjugate(rho_sorted, out=source[:, 1])                          # conj(rho_q)
        np.multiply(weights_sorted, source[:, 1], out=source[:, 1])         # w_q conj(rho_q)
        del rho_sorted
        if not np.all(np.isfinite(source)):
            raise _FailClosed('nonfinite weighted source w*rho')
        source.flags.writeable = False
        work['source_weighted'] = source
        timing['source_weighting_s'] = time.perf_counter() - t1

        state['stage'] = 'scatter'
        t1 = time.perf_counter()
        vertical = geometry['vertical_phase']
        offsets = geometry['r_offsets']
        V = np.zeros((n_R, 2, n_kz), dtype=np.complex128)
        work['scatter_V'] = V
        r_mask = work['r_group_mask']
        r = 0
        while r < n_R:
            r_end = r
            batch_positions = 0
            while r_end < n_R and batch_positions < position_chunk:
                batch_positions += int(offsets[r_end + 1] - offsets[r_end])
                r_end += 1
            state['block'] = dict(r_groups=(r, r_end))
            for g in range(r, r_end):
                s0, s1 = int(offsets[g]), int(offsets[g + 1])
                # SUM_{q at R_g} w_q rho_q E[q, z] and w_q conj(rho_q) E[q, z]; the SAME E.
                V[g] = np.einsum('sb,sz->bz', source[s0:s1], vertical[s0:s1], optimize=False)
            if not np.all(np.isfinite(V[r:r_end])):
                raise _FailClosed('nonfinite grouped vertical sum V')
            r_mask[r:r_end] = True
            tally['scatter_batches'] += 1
            tally['r_groups_scattered'] += r_end - r
            tally['positions_scattered'] += int(offsets[r_end] - offsets[r])
            r = r_end
        if tally['positions_scattered'] != nq or not np.all(r_mask):
            raise _FailClosed('not every position scattered exactly once')
        V.flags.writeable = False
        timing['scatter_s'] = time.perf_counter() - t1

        state['stage'] = 'cell_sum'
        t1 = time.perf_counter()
        bessel = geometry['bessel'][slot]
        cell_perp = geometry['cell_perp_index']
        kz_offsets = geometry['kz_cell_offsets']
        T = np.full((2, n_cells), nan, dtype=np.complex128)
        work['cell_T'] = T
        c_mask = work['cell_mask']
        for z in range(n_kz):
            c_lo, c_hi = int(kz_offsets[z]), int(kz_offsets[z + 1])
            for c0 in range(c_lo, c_hi, cell_chunk):
                c1 = min(c0 + cell_chunk, c_hi)
                state['block'] = dict(kz_group=z, cells=(c0, c1))
                rows = bessel[cell_perp[c0:c1]]                    # J_m(k_perp_p R_r), cached
                # SUM_r V[r, b, z] J[p_c, r] for b = +, - branches
                T[:, c0:c1] = np.einsum('rb,cr->bc', V[:, :, z], rows, optimize=False)
                if not np.all(np.isfinite(T[:, c0:c1])):
                    raise _FailClosed('nonfinite cell sum T')
                c_mask[c0:c1] = True
                tally['cell_blocks'] += 1
                tally['cells_summed'] += c1 - c0
        if tally['cells_summed'] != n_cells or not np.all(c_mask):
            raise _FailClosed('not every filled cell summed exactly once')
        T.flags.writeable = False
        timing['cell_sum_s'] = time.perf_counter() - t1

        t1 = time.perf_counter()
        wave_cell = geometry['wave_cell_index']
        angular = geometry['angular_plus'][slot]
        perp_zero_all = geometry['perp_zero']
        for a in range(0, nk, wave_chunk):
            b = min(a + wave_chunk, nk)
            state['block'] = dict(waves=(a, b))
            state['stage'] = 'gather'
            cells = wave_cell[a:b]
            plus = angular[a:b]                                     # exp(+i m alpha_k)
            minus = np.conj(plus)                                   # exp(-i m alpha_k) (0445 L241)
            acc = T[0, cells] * plus + T[1, cells] * minus
            state['stage'] = 'prefactor'
            values = scale * (unit * acc)                   # -c^2 2pi (-i)^m sum (0445 L275)
            if not np.all(np.isfinite(values)):
                raise _FailClosed('nonfinite deltaJ0 for wave chunk ' + str((a, b)))
            perp_zero = perp_zero_all[a:b]
            if np.any(values[perp_zero] != 0.0):
                raise _FailClosed('k_perp = 0 wave not exactly zero')
            state['stage'] = 'commit'
            retained[a:b] = values
            mask[a:b] = True
            completed.append((a, b))
            tally['k_perp_zero_waves'] += int(np.count_nonzero(perp_zero))
        timing['gather_s'] = time.perf_counter() - t1
        state['stage'] = 'complete'
        state['block'] = None
    except Exception as exc:  # FloatingPointError under caller errstate included
        return finish('FAILED_CLOSED', exc)
    except BaseException as exc:
        try:
            setattr(exc, INTERRUPT_ATTRIBUTE, finish('INTERRUPTED', exc))
        except Exception:
            pass
        raise
    return finish('COMPLETE', None)


# ----------------------------------------------------------------------------- 0445 adapter

def bind_0445_adapter(*, geometry):
    """Bind a prepared geometry; return a callable with the exact 0445 keyword contract.

    Returns dict(kind, status 'READY' | 'INVALID_INPUT', density_fourier, geometry_sha256,
    reason). density_fourier(*, radius_m, z_m, weights_RdRdz_m3, rho_mode_kg_m3,
    k_physical_inverse_m, c_m_s, mode, bessel_jn, wave_chunk, position_chunk) -> the
    evaluate_mode result (all 0445 result keys present). On a non-Exception interruption
    the retained dict is also attached as unt0445_retained_result (0452 consumer contract).
    """
    try:
        bound = _check_geometry(geometry)
    except Exception as exc:
        return dict(kind=ADAPTER_KIND, status='INVALID_INPUT', density_fourier=None,
                    geometry_sha256=None, reason=str(exc), exception_type=type(exc).__name__)

    def density_fourier(*, radius_m, z_m, weights_RdRdz_m3, rho_mode_kg_m3,
                        k_physical_inverse_m, c_m_s, mode, bessel_jn, wave_chunk,
                        position_chunk):
        try:
            return evaluate_mode(geometry=bound, radius_m=radius_m, z_m=z_m,
                                 weights_RdRdz_m3=weights_RdRdz_m3,
                                 rho_mode_kg_m3=rho_mode_kg_m3,
                                 k_physical_inverse_m=k_physical_inverse_m, c_m_s=c_m_s,
                                 mode=mode, bessel_jn=bessel_jn, wave_chunk=wave_chunk,
                                 position_chunk=position_chunk)
        except BaseException as exc:
            try:
                record = getattr(exc, INTERRUPT_ATTRIBUTE, None)
                if record is not None:
                    setattr(exc, INTERRUPT_ATTRIBUTE_0445, record)
            except Exception:
                pass
            raise

    density_fourier.unt0458_geometry_sha256 = bound['geometry_sha256']
    return dict(kind=ADAPTER_KIND, status='READY', density_fourier=density_fourier,
                geometry_sha256=bound['geometry_sha256'], reason=None, exception_type=None)
