"""INERT nonzero-mode (m=1..6) density Fourier source contraction; UNT task 0445.

Binding equation (task 0445 file sha256
29ebcffdf8dca98212b859e0a07f041608afe32d2ed19a9e28df9f5870720835), implemented verbatim:

  deltaJ0(k) = -c^2 * 2pi * (-i)^m * sum_q [ w_q * J_m(k_perp R_q) * exp(-i k_z z_q)
               * ( rho_m(q) exp(+i m alpha_k) + conj(rho_m(q)) exp(-i m alpha_k) ) ]

  k_perp = hypot(k_x, k_y), alpha_k = atan2(k_y, k_x), w_q = R dR dz WITHOUT 2pi.

Real perturbation rho_m e^{+i m phi} + conj(rho_m) e^{-i m phi}; source Fourier
e^{-i k.x}; existing scalar rest-energy convention J_0(x) = -c^2 rho(x). One
(-i)^m multiplies both harmonics (J_{-m} = (-1)^m J_m). No extra factor 2, no
conjugated vertical exponential, no Fourier integration weights, no native
inversion, normalization, mass adjustment, pressure source or acceptance.
Only source coordinate 0 is represented: the scalar increment, in joules:
  c^2 [m^2 s^-2] x w_q [m^3] x rho_m [kg m^-3]; 2pi, (-i)^m, J_m and phases
  dimensionless  ->  kg m^2 s^-2 = J.
k_perp = 0: alpha_k is numpy.arctan2 of signed zeros (finite: 0, -0, pi or -pi);
nothing is divided by k_perp; J_m(0) = 0 for m >= 1 makes every term exactly
zero. The injected provider must return exactly 0.0 at argument 0.0, otherwise
the call fails closed.
Dependencies: numpy + stdlib only. No BLAS products, no floating-point warning
suppression (the caller's numpy.errstate governs), no I/O, nothing executed at
import beyond these definitions.
"""
import math
import numbers

import numpy as np


EQUATION_0445 = (
    'deltaJ0(k) = -c^2 * 2pi * (-i)^m * sum_q [ w_q J_m(k_perp R_q) exp(-i k_z z_q) '
    '* ( rho_m(q) exp(+i m alpha_k) + conj(rho_m(q)) exp(-i m alpha_k) ) ], '
    'alpha_k = atan2(k_y, k_x), w_q = R dR dz WITHOUT 2pi')
UNIT_CHAIN = ('c^2 [m^2 s^-2] x w_q [m^3] x rho_m [kg m^-3] (2pi, (-i)^m, J_m, '
              'exp factors dimensionless) = kg m^2 s^-2 = J')
ACCUMULATION_ORDER = (
    'Per wave: complex128 accumulator starts at 0; position blocks [u, u+position_chunk) '
    'are added in ascending u by in-place +=; inside a block the q-reduction is '
    "numpy.einsum('q,kq,kq,kq->k', w, J_m, exp(-i kz z), bracket, optimize=False) "
    '(numpy internal uncompensated sum-of-products order, operands multiplied in the '
    'listed order); after the last block (-i)^m (exact unit) multiplies the sum, then '
    'the real scale -(c*c)*(2*pi). Results for different position_chunk agree to '
    'rounding only.')
ALPHA_AT_K_PERP_ZERO = (
    'alpha_k = numpy.arctan2(k_y, k_x) everywhere, also at k_perp = 0 where it is finite '
    '(0, -0, pi or -pi by signed zeros); never divided by k_perp; J_m(0) = 0 (m >= 1, '
    'provider-enforced exactly) zeroes every term, and k_perp = 0 outputs are checked '
    'to equal 0 exactly.')

# (-i)^m for m mod 4 = 0, 1, 2, 3; exact unit values, no complex power evaluation.
_MINUS_I_POWER = (complex(1.0, 0.0), complex(0.0, -1.0),
                  complex(-1.0, 0.0), complex(0.0, 1.0))


class _InvalidInput(ValueError):
    """Input contract violation detected before any contraction."""


class _FailClosed(ValueError):
    """Runtime contract violation during the contraction."""


def _real_vector(value, name):
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


def _validate(radius_m, z_m, weights_RdRdz_m3, rho_mode_kg_m3, k_physical_inverse_m,
              c_m_s, mode, bessel_jn, wave_chunk, position_chunk):
    if type(mode) is not int or not 1 <= mode <= 6:
        raise _InvalidInput('mode: int in 1..6 required (bool and other types rejected)')
    for name, chunk in (('wave_chunk', wave_chunk), ('position_chunk', position_chunk)):
        if type(chunk) is not int or chunk < 1:
            raise _InvalidInput(name + ': positive int required (bool rejected)')
    if not callable(bessel_jn):
        raise _InvalidInput('bessel_jn: callable (n, x_array) -> float64 array required')
    if (isinstance(c_m_s, (bool, np.bool_)) or not isinstance(c_m_s, numbers.Real)):
        raise _InvalidInput('c_m_s: real number required')
    c = float(c_m_s)
    c_squared = c * c
    if not (math.isfinite(c) and c > 0.0 and math.isfinite(c_squared) and c_squared > 0.0):
        raise _InvalidInput('c_m_s: finite positive value with finite positive square required')
    radius = _real_vector(radius_m, 'radius_m')
    height = _real_vector(z_m, 'z_m')
    weight = _real_vector(weights_RdRdz_m3, 'weights_RdRdz_m3')
    count = radius.shape[0]
    if count < 1:
        raise _InvalidInput('radius_m: at least one position required')
    if height.shape != radius.shape or weight.shape != radius.shape:
        raise _InvalidInput('radius_m, z_m, weights_RdRdz_m3: identical length required')
    if np.any(radius <= 0.0):
        raise _InvalidInput('radius_m: strictly positive radii required')
    if np.any(weight <= 0.0):
        raise _InvalidInput('weights_RdRdz_m3: strictly positive weights required')
    rho = np.asarray(rho_mode_kg_m3)
    if rho.dtype.kind != 'c' or rho.dtype.itemsize > 16:
        raise _InvalidInput('rho_mode_kg_m3: complex64/complex128 dtype required, got '
                            + str(rho.dtype))
    if rho.shape != radius.shape:
        raise _InvalidInput('rho_mode_kg_m3: shape (q,) matching radius_m required')
    rho = np.array(rho, dtype=np.complex128, copy=True)
    if not np.all(np.isfinite(rho)):
        raise _InvalidInput('rho_mode_kg_m3: finite values required')
    waves = np.asarray(k_physical_inverse_m)
    kind = waves.dtype.kind
    if kind not in 'fiu' or (kind == 'f' and waves.dtype.itemsize > 8):
        raise _InvalidInput('k_physical_inverse_m: real dtype required, got ' + str(waves.dtype))
    if waves.ndim != 2 or waves.shape[1] != 3 or waves.shape[0] < 1:
        raise _InvalidInput('k_physical_inverse_m: shape (nk, 3) with nk >= 1 required')
    waves = np.array(waves, dtype=np.float64, copy=True)
    if not np.all(np.isfinite(waves)):
        raise _InvalidInput('k_physical_inverse_m: finite values required')
    return radius, height, weight, rho, waves, c_squared


def _provider_values(bessel_jn, mode, argument, zero_argument):
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


def _base_result(status, nk, count, mode, wave_chunk, position_chunk):
    return dict(
        status=status, complete=False, deltaJ0_J=None, units='J',
        reason=None, failure_stage=None, exception_type=None,
        retained_deltaJ0_J=None, retained_wave_mask=None, completed_wave_chunks=(),
        counts=dict(waves=nk, positions=count, mode=mode),
        chunking=dict(wave_chunk=wave_chunk, position_chunk=position_chunk),
        convention=dict(equation=EQUATION_0445, unit_chain=UNIT_CHAIN,
                        accumulation_order=ACCUMULATION_ORDER,
                        alpha_at_k_perp_zero=ALPHA_AT_K_PERP_ZERO,
                        source_coordinate=0, weights='w_q = R dR dz WITHOUT 2pi',
                        fourier_sign='source Fourier exp(-i k.x)',
                        excluded='native inversion, normalization, mass adjustment, '
                                 'pressure source, acceptance'))


def nonzero_mode_density_fourier(*, radius_m, z_m, weights_RdRdz_m3, rho_mode_kg_m3,
                                 k_physical_inverse_m, c_m_s, mode, bessel_jn,
                                 wave_chunk, position_chunk):
    """Scalar Fourier increment deltaJ0(k) [J] of one nonzero density harmonic.

    Returns a fail-closed dict. status 'COMPLETE' -> deltaJ0_J complex128 (nk,)
    in the caller's wave order. 'INVALID_INPUT' -> nothing evaluated.
    'FAILED_CLOSED' -> deltaJ0_J None; retained_deltaJ0_J holds every completed
    wave chunk (other rows NaN), retained_wave_mask marks them. A non-Exception
    interruption (KeyboardInterrupt, SystemExit) is re-raised after the same
    retained dict (status 'INTERRUPTED') is attached to it as attribute
    unt0445_retained_result. No (wave, position) array exceeds
    wave_chunk x position_chunk elements.
    """
    try:
        radius, height, weight, rho, waves, c_squared = _validate(
            radius_m, z_m, weights_RdRdz_m3, rho_mode_kg_m3, k_physical_inverse_m,
            c_m_s, mode, bessel_jn, wave_chunk, position_chunk)
    except Exception as exc:  # fail closed: nothing evaluated
        nk = None
        result = _base_result('INVALID_INPUT', nk, None,
                              mode if type(mode) is int else None,
                              wave_chunk if type(wave_chunk) is int else None,
                              position_chunk if type(position_chunk) is int else None)
        result['reason'] = str(exc)
        result['failure_stage'] = 'validation'
        result['exception_type'] = type(exc).__name__
        return result

    nk = waves.shape[0]
    count = radius.shape[0]
    rho_conj = np.conj(rho)                                   # conj(rho_m(q))
    unit = _MINUS_I_POWER[mode % 4]                           # (-i)^m, exact
    scale = -c_squared * (2.0 * math.pi)                      # -c^2 * 2pi
    wave_chunks_total = -(-nk // wave_chunk)
    position_chunks_per_wave_chunk = -(-count // position_chunk)

    retained = np.full(nk, complex(math.nan, math.nan), dtype=np.complex128)
    mask = np.zeros(nk, dtype=bool)
    completed = []
    tally = dict(blocks_evaluated=0, provider_calls=0, provider_elements=0,
                 k_perp_zero_waves=0, zero_argument_elements=0,
                 realized_max_block_elements=0)
    stage = 'start'

    def finish(status, exc):
        result = _base_result(status, nk, count, mode, wave_chunk, position_chunk)
        result['counts'].update(
            wave_chunks_total=wave_chunks_total,
            wave_chunks_completed=len(completed),
            position_chunks_per_wave_chunk=position_chunks_per_wave_chunk,
            waves_completed=int(np.count_nonzero(mask)), **tally)
        result['chunking'].update(
            block_element_bound=wave_chunk * position_chunk,
            realized_max_block_elements=tally['realized_max_block_elements'],
            order='wave chunks ascending; position chunks ascending within each wave chunk; '
                  'a wave chunk is committed only after all its position chunks')
        result['completed_wave_chunks'] = tuple(completed)
        result['retained_wave_mask'] = mask
        if status == 'COMPLETE':
            result['complete'] = True
            result['deltaJ0_J'] = retained
        else:
            result['retained_deltaJ0_J'] = retained
            result['reason'] = str(exc)
            result['failure_stage'] = stage
            result['exception_type'] = type(exc).__name__
        return result

    try:
        for a in range(0, nk, wave_chunk):
            b = min(a + wave_chunk, nk)
            stage = 'wave_geometry'
            k_x = waves[a:b, 0]
            k_y = waves[a:b, 1]
            k_z = waves[a:b, 2]
            k_perp = np.hypot(k_x, k_y)                       # k_perp
            alpha = np.arctan2(k_y, k_x)                      # alpha_k = atan2(k_y, k_x)
            if not (np.all(np.isfinite(k_perp)) and np.all(np.isfinite(alpha))):
                raise _FailClosed('nonfinite k_perp or alpha_k')
            plus = np.exp(1j * (float(mode) * alpha))         # exp(+i m alpha_k)
            minus = np.conj(plus)                             # exp(-i m alpha_k)
            perp_zero = k_perp == 0.0
            accumulator = np.zeros(b - a, dtype=np.complex128)
            for u in range(0, count, position_chunk):
                v = min(u + position_chunk, count)
                stage = 'bessel_argument'
                argument = k_perp[:, None] * radius[None, u:v]  # k_perp R_q
                if not np.all(np.isfinite(argument)):
                    raise _FailClosed('nonfinite Bessel argument k_perp R')
                argument.flags.writeable = False
                zero_argument = argument == 0.0
                tally['realized_max_block_elements'] = max(
                    tally['realized_max_block_elements'], argument.size)
                stage = 'bessel_provider'
                tally['provider_calls'] += 1
                tally['provider_elements'] += argument.size
                bessel = _provider_values(bessel_jn, mode, argument, zero_argument)  # J_m
                tally['zero_argument_elements'] += int(np.count_nonzero(zero_argument))
                stage = 'vertical_phase'
                phase = k_z[:, None] * height[None, u:v]      # k_z z_q
                if not np.all(np.isfinite(phase)):
                    raise _FailClosed('nonfinite vertical phase k_z z')
                vertical = np.exp(-1j * phase)                # exp(-i k_z z_q)
                stage = 'azimuthal_bracket'
                bracket = (rho[None, u:v] * plus[:, None]     # rho_m exp(+i m alpha_k)
                           + rho_conj[None, u:v] * minus[:, None])  # + conj(rho_m) exp(-i m alpha_k)
                stage = 'position_sum'
                partial = np.einsum('q,kq,kq,kq->k', weight[u:v], bessel, vertical,
                                    bracket, optimize=False)  # sum_q w_q J_m exp [..]
                if not np.all(np.isfinite(partial)):
                    raise _FailClosed('nonfinite position-block partial sum')
                accumulator += partial
                tally['blocks_evaluated'] += 1
            stage = 'prefactor'
            values = scale * (unit * accumulator)             # -c^2 2pi (-i)^m sum_q
            if not np.all(np.isfinite(values)):
                raise _FailClosed('nonfinite deltaJ0 for wave chunk ' + str((a, b)))
            if np.any(values[perp_zero] != 0.0):
                raise _FailClosed('k_perp = 0 wave not exactly zero')
            stage = 'commit'
            retained[a:b] = values
            mask[a:b] = True
            completed.append((a, b))
            tally['k_perp_zero_waves'] += int(np.count_nonzero(perp_zero))
        stage = 'complete'
    except Exception as exc:  # FloatingPointError under caller errstate included
        return finish('FAILED_CLOSED', exc)
    except BaseException as exc:
        try:
            exc.unt0445_retained_result = finish('INTERRUPTED', exc)
        except Exception:
            pass
        raise
    return finish('COMPLETE', None)
