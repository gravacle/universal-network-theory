"""INERT modal-candidate full-grid join (UNT 0431, Claude2 c2v001).

Joins seven caller-supplied modal displacement candidates (m = 0..6) to the
root binding's single full-grid action evaluation. Two public functions:

  assemble_real_displacement(*, mesh, mode_results, nphi, imag_atol, imag_rtol)
  evaluate_modal_candidate(*, binding_module, action_module, mesh, base_fields,
                           c_light, gamma, tolerances, provenance, mode_results,
                           nphi, imag_atol, imag_rtol, induced_response)

Layout and conventions (see INTERFACE_0431_V001.md):
  * mesh is the root make_mesh output: grid_shape = (nr, nphi, neta) with
    nr = len(radial nodes), neta = len(eta nodes); axis order (R, phi, eta).
  * phi nodes: phi_j = 2*pi*j/nphi, j = 0..nphi-1, read from mesh['phi'] and
    required to equal that root expression bitwise and to be constant along
    the R and eta axes.
  * xi_cylindrical_m has shape (3, nr*neta); axis 0 = (R, phi, z) physical
    orthonormal components [m]; column k = iR*neta + ieta (R-major /
    eta-minor, numpy C order).
  * FFT/nphi: xi_m = (1/nphi) sum_j f(phi_j) exp(-i m phi_j)  (np.fft.fft/nphi).
    Real field: f = Re(xi_0) + 2*Re(sum_{m=1..6} xi_m exp(i m phi)).
  * Output xi is the tuple (xi_R, xi_phi, xi_z) of read-only float64 arrays of
    exactly grid_shape, which root evaluate_action passes unchanged to
    c2v002 evaluate_bulk_action(xi=...).

Contract: no I/O, nothing executed at import beyond constant and function
definitions, numpy + stdlib only, keyword-only public arguments WITHOUT
defaults, fail-closed result dicts. No solve, QR, transform, kernel, source
offset, clipping, forced positivity, boundary lid, threshold, convergence
decision, or physical/calibration acceptance. ok=True is never acceptance.
"""
import inspect
import math
import types
from collections.abc import Mapping

import numpy as np

MODULE_TAG = 'modal_full_grid_join_c2v001'
ACTION_MODULE_TAG = 'ddo_noncircular_displacement_action_c2v002'
ACCEPTANCE = 'NOT_ASSESSED_BY_THIS_WRAPPER'
RETAINED_MODES = (0, 1, 2, 3, 4, 5, 6)
MAX_RETAINED_MODE = 6
# Mode-result dict fields. 'xi_cylindrical_m' and 'accepted_inner' are named by
# 0431; 'm' and 'solve_failed' are NOT named by 0431 (missing interface facts,
# INTERFACE section 6) and are required explicitly, never defaulted.
MODE_INDEX_KEY = 'm'
FAILED_SOLVE_FLAG = 'solve_failed'
INNER_FLAG = 'accepted_inner'
CANDIDATE_KEY = 'xi_cylindrical_m'
COMPONENTS = ('R', 'phi', 'z')
# Exact keyword-only parameter set of root evaluate_action (binding v002 text).
EVALUATE_ACTION_PARAMETERS = frozenset((
    'action_module', 'mesh', 'base_fields', 'xi', 'induced_response', 'gamma',
    'c_light', 'base_axisymmetry_rtol', 'polytrope_consistency_rtol',
    'base_provenance'))
TOLERANCE_KEYS = ('base_axisymmetry_rtol', 'polytrope_consistency_rtol')
_ERRSTATE = {'divide': 'raise', 'over': 'raise', 'invalid': 'raise', 'under': 'ignore'}
CONVENTIONS = {
    'mesh_layout': 'grid_shape=(nr, nphi, neta) from root make_mesh; axes (R, phi, eta)',
    'phi_nodes': 'phi_j = 2*pi*j/nphi, j=0..nphi-1 (bitwise root expression), from mesh[phi]',
    'candidate_layout': ('xi_cylindrical_m shape (3, nr*neta); rows (R, phi, z) physical '
                         'orthonormal [m]; column k = iR*neta + ieta (R-major/eta-minor, C order)'),
    'fourier': 'FFT/nphi: xi_m = (1/nphi) sum_j f(phi_j) exp(-i m phi_j)',
    'reconstruction': 'f = Re(xi_0) + 2*Re(sum_{m=1..6} xi_m exp(i m phi_j)); Im(xi_0) tested then discarded',
    'output_xi': 'tuple (xi_R, xi_phi, xi_z), read-only float64, exactly grid_shape',
}
NOT_DONE = (
    'no modal solve, matrix assembly or QR (owned elsewhere); candidates used as supplied',
    'no zero mode invented; each m=0..6 required exactly once',
    'no native feedback call during assembly; induced_response is passed unchanged to the '
    'single evaluate_action call',
    'no base-source offset added; base_fields passed unchanged (offset already in Phi0, '
    'angular forcing and r0)',
    'no clipping, forced positivity, boundary lid, threshold, convergence decision, '
    'physical or calibration acceptance',
    'no acceptance on retained modes; residual reported in all nphi angular slots',
    'no promotion of accepted_inner flags',
)


class _Reject(Exception):
    def __init__(self, stage, reason):
        Exception.__init__(self, reason)
        self.stage = stage
        self.reason = reason


def _fail(stage, reason):
    return {'ok': False, 'module': MODULE_TAG, 'stage': stage, 'reason': reason,
            'acceptance': ACCEPTANCE}


def _readonly(a, dtype=np.float64):
    out = np.array(a, dtype=dtype, copy=True)
    out.flags.writeable = False
    return out


def _is_int(v):
    return isinstance(v, (int, np.integer)) and not isinstance(v, (bool, np.bool_))


def _flag(stage, name, v):
    if not isinstance(v, (bool, np.bool_)):
        raise _Reject(stage, '%s: explicit bool required, got %s' % (name, type(v).__name__))
    return bool(v)


def _tolerance(name, v):
    if isinstance(v, (bool, np.bool_)) or not isinstance(v, (int, float, np.integer, np.floating)):
        raise _Reject('input_validation', name + ': real scalar required')
    x = float(v)
    if not math.isfinite(x) or x < 0:
        raise _Reject('input_validation', name + ': finite nonnegative value required')
    return x


# --------------------------------------------------------------------------- assembly

def _mesh_layout(mesh, nphi):
    stage = 'mesh'
    if not isinstance(mesh, Mapping):
        raise _Reject(stage, 'mesh: mapping (root make_mesh output) required')
    for key in ('grid_shape', 'phi'):
        if key not in mesh:
            raise _Reject(stage, 'mesh: key %r required' % key)
    gs = mesh['grid_shape']
    if not isinstance(gs, tuple) or len(gs) != 3 or not all(_is_int(n) and n >= 1 for n in gs):
        raise _Reject(stage, 'mesh[grid_shape]: tuple (nr, nphi, neta) of positive ints required')
    nr, n_phi_mesh, neta = (int(n) for n in gs)
    if not _is_int(nphi):
        raise _Reject(stage, 'nphi: int required')
    if int(nphi) != n_phi_mesh:
        raise _Reject(stage, 'nphi %d != mesh grid_shape[1] %d' % (int(nphi), n_phi_mesh))
    nphi = int(nphi)
    if not 2 * MAX_RETAINED_MODE < nphi:
        raise _Reject(stage, 'nphi %d cannot represent m=0..%d without aliasing (need nphi > %d)'
                      % (nphi, MAX_RETAINED_MODE, 2 * MAX_RETAINED_MODE))
    phi = mesh['phi']
    if not isinstance(phi, np.ndarray) or phi.dtype != np.float64 or phi.shape != (nr, nphi, neta):
        raise _Reject(stage, 'mesh[phi]: float64 array of exactly grid_shape required')
    if not np.all(np.isfinite(phi)):
        raise _Reject(stage, 'mesh[phi]: nonfinite')
    line = phi[0, :, 0]
    if not np.array_equal(phi, np.broadcast_to(line[None, :, None], phi.shape)):
        raise _Reject(stage, 'mesh[phi]: must depend on the phi axis only')
    expected = 2 * np.pi * np.arange(nphi) / nphi
    if not np.array_equal(line, expected):
        raise _Reject(stage, 'mesh[phi]: nodes must equal 2*pi*arange(nphi)/nphi bitwise '
                      '(root make_mesh convention; required by the FFT/nphi convention)')
    return nr, nphi, neta, _readonly(line)


def _mode_table(mode_results, nr, neta):
    stage = 'mode_results'
    if not isinstance(mode_results, (list, tuple)):
        raise _Reject(stage, 'mode_results: list or tuple of mode-result mappings required')
    ms = []
    for i, entry in enumerate(mode_results):
        if not isinstance(entry, Mapping):
            raise _Reject(stage, 'mode_results[%d]: mapping required' % i)
        if MODE_INDEX_KEY not in entry or not _is_int(entry[MODE_INDEX_KEY]):
            raise _Reject(stage, 'mode_results[%d]: explicit int %r required'
                          % (i, MODE_INDEX_KEY))
        ms.append(int(entry[MODE_INDEX_KEY]))
    duplicate = sorted(m for m in set(ms) if ms.count(m) > 1)
    extra = sorted(m for m in set(ms) if m not in RETAINED_MODES)
    missing = [m for m in RETAINED_MODES if m not in ms]
    if duplicate or extra or missing:
        raise _Reject(stage, 'each m in %s required exactly once; duplicate %s, extra %s, '
                      'missing %s; no zero mode is invented' % (RETAINED_MODES, duplicate,
                                                                 extra, missing))
    by_m = dict(zip(ms, mode_results))
    coeffs, inner = {}, {}
    for m in RETAINED_MODES:
        entry = by_m[m]
        if FAILED_SOLVE_FLAG not in entry:
            raise _Reject(stage, 'm=%d: explicit %r flag required (0431 names no failed-solve '
                          'field; missing interface fact)' % (m, FAILED_SOLVE_FLAG))
        if _flag(stage, 'm=%d %s' % (m, FAILED_SOLVE_FLAG), entry[FAILED_SOLVE_FLAG]):
            raise _Reject(stage, 'm=%d: failed solve (%s=True); no candidate is invented'
                          % (m, FAILED_SOLVE_FLAG))
        if INNER_FLAG not in entry:
            raise _Reject(stage, 'm=%d: %r flag required' % (m, INNER_FLAG))
        inner[m] = _flag(stage, 'm=%d %s' % (m, INNER_FLAG), entry[INNER_FLAG])
        arr = entry.get(CANDIDATE_KEY)
        if arr is None:
            raise _Reject(stage, 'm=%d: missing candidate array %r' % (m, CANDIDATE_KEY))
        if not isinstance(arr, np.ndarray) or isinstance(arr, np.ma.MaskedArray):
            raise _Reject(stage, 'm=%d: %s must be a plain numpy array' % (m, CANDIDATE_KEY))
        k = arr.dtype.kind
        if k not in 'fc' or (k == 'f' and arr.dtype.itemsize > 8) or (k == 'c' and arr.dtype.itemsize > 16):
            raise _Reject(stage, 'm=%d: %s dtype %s not complex128/float64-representable'
                          % (m, CANDIDATE_KEY, arr.dtype))
        if arr.shape != (3, nr * neta):
            raise _Reject(stage, 'm=%d: %s shape %s != (3, nr*neta) = (3, %d)'
                          % (m, CANDIDATE_KEY, arr.shape, nr * neta))
        c = np.array(arr, dtype=np.complex128, copy=True)
        if not np.all(np.isfinite(c)):
            raise _Reject(stage, 'm=%d: %s has nonfinite real or imaginary parts' % (m, CANDIDATE_KEY))
        coeffs[m] = c
    return by_m, coeffs, inner


def _assemble(*, mesh, mode_results, nphi, imag_atol, imag_rtol):
    atol = _tolerance('imag_atol', imag_atol)
    rtol = _tolerance('imag_rtol', imag_rtol)
    nr, nphi, neta, phi = _mesh_layout(mesh, nphi)
    by_m, coeffs, inner = _mode_table(mode_results, nr, neta)

    x0 = coeffs[0]
    imag_max = float(np.max(np.abs(x0.imag)))
    real_max = float(np.max(np.abs(x0.real)))
    per_comp = dict((c, {'imag_max_abs': float(np.max(np.abs(x0[i].imag))),
                         'real_max_abs': float(np.max(np.abs(x0[i].real)))})
                    for i, c in enumerate(COMPONENTS))
    if not (imag_max <= atol and imag_max <= rtol * real_max):
        raise _Reject('m0_imaginary', 'm=0 imaginary part: max|Im xi_0| = %r must satisfy both '
                      '<= imag_atol %r and <= imag_rtol %r * max|Re xi_0| (%r); per component %r'
                      % (imag_max, atol, rtol, real_max, per_comp))

    gs = (nr, nphi, neta)
    phase = dict((m, np.exp(1j * m * phi)) for m in RETAINED_MODES[1:])
    xi = []
    for i, c in enumerate(COMPONENTS):
        acc = np.zeros(gs, dtype=np.complex128)
        for m in RETAINED_MODES[1:]:
            acc = acc + coeffs[m][i].reshape(nr, neta)[:, None, :] * phase[m][None, :, None]
        field = x0[i].real.reshape(nr, neta)[:, None, :] + 2.0 * acc.real
        if field.shape != gs or not np.all(np.isfinite(field)):
            raise _Reject('reconstruction', 'xi_%s: nonfinite or misshaped reconstruction' % c)
        xi.append(_readonly(field))

    false_modes = tuple(m for m in RETAINED_MODES if not inner[m])
    return {
        'ok': True, 'module': MODULE_TAG, 'stage': 'assembled', 'acceptance': ACCEPTANCE,
        'xi': tuple(xi), 'grid_shape': gs, 'nphi': nphi, 'phi_nodes': phi,
        'inner_accepted_by_m': types.MappingProxyType(dict(inner)),
        'modes_with_accepted_inner_false': false_modes,
        'm0_imaginary_check': {
            'test': 'max|Im xi_0| <= imag_atol AND max|Im xi_0| <= imag_rtol * max|Re xi_0|, '
                    'max over all three components and all nr*neta columns',
            'imag_max_abs': imag_max, 'real_max_abs': real_max,
            'imag_atol': atol, 'imag_rtol': rtol, 'per_component': per_comp,
            'imaginary_part': 'discarded after the test (Re xi_0 used)'},
        'mode_results_by_m': tuple(by_m[m] for m in RETAINED_MODES),
        'conventions': dict(CONVENTIONS),
    }


def assemble_real_displacement(*, mesh, mode_results, nphi, imag_atol, imag_rtol):
    """Reconstruct the real cylindrical displacement on (nr, nphi, neta).

    Returns {'ok': True, 'xi': (xi_R, xi_phi, xi_z), ...} or a fail-closed
    {'ok': False, 'module', 'stage', 'reason', 'acceptance'}. Calls no callback.
    """
    try:
        with np.errstate(**_ERRSTATE):
            return _assemble(mesh=mesh, mode_results=mode_results, nphi=nphi,
                             imag_atol=imag_atol, imag_rtol=imag_rtol)
    except _Reject as rej:
        return _fail(rej.stage, rej.reason)
    except FloatingPointError as exc:
        return _fail('floating_point', 'assembly arithmetic raised FloatingPointError (%s)' % exc)
    except Exception as exc:
        return _fail('internal', '%s: %s' % (type(exc).__name__, exc))


# --------------------------------------------------------------------------- join

def _check_join(binding_module, action_module, induced_response, tolerances):
    stage = 'join_validation'
    if not isinstance(binding_module, types.ModuleType):
        raise _Reject(stage, 'binding_module: caller-supplied module object required')
    if not isinstance(action_module, types.ModuleType):
        raise _Reject(stage, 'action_module: caller-supplied module object required')
    fn = getattr(binding_module, 'evaluate_action', None)
    if not callable(fn):
        raise _Reject(stage, 'binding_module.evaluate_action: callable required')
    try:
        params = inspect.signature(fn).parameters
    except (TypeError, ValueError) as exc:
        raise _Reject(stage, 'binding_module.evaluate_action: signature unreadable (%s)' % exc)
    if (set(params) != EVALUATE_ACTION_PARAMETERS
            or any(p.kind is not inspect.Parameter.KEYWORD_ONLY
                   or p.default is not inspect.Parameter.empty for p in params.values())):
        raise _Reject(stage, 'binding_module.evaluate_action: keyword-only parameters %s without '
                      'defaults required (root binding v002); got %s'
                      % (sorted(EVALUATE_ACTION_PARAMETERS), list(params)))
    if getattr(action_module, 'MODULE_TAG', None) != ACTION_MODULE_TAG:
        raise _Reject(stage, 'action_module.MODULE_TAG must be %r' % ACTION_MODULE_TAG)
    if not callable(getattr(action_module, 'evaluate_bulk_action', None)):
        raise _Reject(stage, 'action_module.evaluate_bulk_action: callable required')
    if not callable(induced_response):
        raise _Reject(stage, 'induced_response: callable required')
    if not isinstance(tolerances, Mapping) or set(tolerances.keys()) != set(TOLERANCE_KEYS):
        raise _Reject(stage, 'tolerances: mapping with exact keys %s required' % (TOLERANCE_KEYS,))
    return fn, dict((k, tolerances[k]) for k in TOLERANCE_KEYS)


def _fourier_report(result, gs, nphi):
    stage = 'euler_residual_report'
    res = result.get('euler_residual')
    if not isinstance(res, Mapping) or set(res.keys()) != set(COMPONENTS):
        raise _Reject(stage, "returned 'euler_residual' must be a mapping with exactly keys R, phi, z")
    k = np.arange(nphi)
    signed = np.where(k <= nphi // 2, k, k - nphi)
    retained = np.abs(signed) <= MAX_RETAINED_MODE
    comps = {}
    for c in COMPONENTS:
        a = res[c]
        if (not isinstance(a, np.ndarray) or a.dtype.kind != 'f' or a.shape != gs
                or not np.all(np.isfinite(a))):
            raise _Reject(stage, 'euler_residual[%s]: real finite array of grid_shape %s required'
                          % (c, gs))
        a = np.asarray(a, dtype=np.float64)
        F = np.fft.fft(a, axis=1) / nphi
        p2 = np.sum(F.real ** 2 + F.imag ** 2, axis=(0, 2))
        l2 = np.sqrt(p2)
        mx = np.max(np.abs(F), axis=(0, 2))
        entry = {
            'slot_l2_over_R_eta': _readonly(l2), 'slot_max_abs': _readonly(mx),
            'all_slots_l2': float(np.sqrt(np.sum(p2))),
            'retained_slots_l2': float(np.sqrt(np.sum(p2[retained]))),
            'omitted_slots_l2': float(np.sqrt(np.sum(p2[~retained]))),
            'omitted_slots_max_abs': float(np.max(mx[~retained])),
            'nodal_l2_over_sqrt_nphi': float(np.sqrt(np.sum(a * a)) / math.sqrt(nphi)),
        }
        for key, val in entry.items():
            if not np.all(np.isfinite(val)):
                raise _Reject(stage, 'euler_residual[%s] report %s: nonfinite' % (c, key))
        comps[c] = entry
    return {
        'slot_index': _readonly(k, np.int64),
        'signed_m': _readonly(signed, np.int64),
        'retained_slot': _readonly(retained, bool),
        'omitted_slot_indices': tuple(int(i) for i in k[~retained]),
        'nyquist_slot_index': nphi // 2,
        'components': comps,
        'convention': ('F[:, s, :] = np.fft.fft(residual, axis=1)[:, s, :] / nphi for every slot '
                       's=0..nphi-1; signed m = s for s <= nphi/2 (s = nphi/2 is Nyquist), '
                       's - nphi otherwise; retained slot means |m| <= 6. Norms are unweighted '
                       'over (R, eta) nodes. nodal_l2_over_sqrt_nphi equals all_slots_l2 by '
                       'Parseval (reported, not gated).'),
        'acceptance': ACCEPTANCE,
    }


def _array_status(obj):
    if isinstance(obj, np.ndarray):
        if obj.dtype.kind not in 'fiuc':
            return 'PRESENT_NOT_NUMERIC'
        return 'AVAILABLE_FINITE' if np.all(np.isfinite(obj)) else 'PRESENT_NONFINITE'
    return 'PRESENT_NOT_ARRAY'


def _availability(result):
    out = {}
    for path in (('euler_residual',), ('euler_terms',), ('perturbations',), ('source_feedback',),
                 ('identity_diagnostics', 'linearized_continuity'),
                 ('identity_diagnostics', 'linearized_entropy'),
                 ('base_checks', 'base_continuity_residual'),
                 ('base_checks', 'base_entropy_residual'), ('mesh_scope',)):
        node, ok = result, True
        for p in path:
            if isinstance(node, Mapping) and p in node:
                node = node[p]
            else:
                ok = False
                break
        name = '.'.join(path)
        if not ok:
            out[name] = 'ABSENT'
        elif len(path) == 2:
            out[name] = _array_status(node)
        else:
            out[name] = 'PRESENT'
    out['induced_response_full'] = ('PRESENT_NOT_TRAVERSED' if 'induced_response_full' in result
                                    else 'ABSENT')
    mc = result.get('mesh_constraints')
    if not isinstance(mc, Mapping):
        out['mesh_constraints'] = 'ABSENT'
    else:
        out['mesh_constraints'] = dict(
            (str(k), 'TEXT' if isinstance(v, str) else _array_status(v)) for k, v in mc.items())
    return out


def _density_pressure(result, gs):
    try:
        bs, pert = result['boundary_state'], result['perturbations']
        arrays = {'rho0': bs['rho0'], 'P0': bs['P0'], 'drho': pert['drho'], 'dP': pert['dP']}
    except (KeyError, TypeError) as exc:
        return {'status': 'UNAVAILABLE', 'reason': 'returned fields absent (%s: %s)'
                % (type(exc).__name__, exc)}
    for name, a in arrays.items():
        if (not isinstance(a, np.ndarray) or a.dtype.kind != 'f' or a.shape != gs
                or not np.all(np.isfinite(a))):
            return {'status': 'UNAVAILABLE',
                    'reason': '%s: not a real finite array of grid_shape %s' % (name, gs)}
    try:
        with np.errstate(**_ERRSTATE):
            rho = arrays['rho0'] + arrays['drho']
            pres = arrays['P0'] + arrays['dP']
            ratio = np.abs(arrays['drho'] / arrays['rho0'])
    except FloatingPointError as exc:
        return {'status': 'UNAVAILABLE', 'reason': 'FloatingPointError (%s)' % exc}
    if not (np.all(np.isfinite(rho)) and np.all(np.isfinite(pres)) and np.all(np.isfinite(ratio))):
        return {'status': 'UNAVAILABLE', 'reason': 'nonfinite combination'}

    def idx(i):
        return tuple(int(n) for n in np.unravel_index(int(i), gs))

    return {'status': 'AVAILABLE',
            'min_rho0_plus_drho': float(np.min(rho)), 'argmin_rho0_plus_drho': idx(np.argmin(rho)),
            'min_P0_plus_dP': float(np.min(pres)), 'argmin_P0_plus_dP': idx(np.argmin(pres)),
            'max_abs_drho_over_rho0': float(np.max(ratio)),
            'argmax_abs_drho_over_rho0': idx(np.argmax(ratio)),
            'sources': 'boundary_state[rho0], boundary_state[P0], perturbations[drho], '
                       'perturbations[dP] of the returned result',
            'scope': 'first-order sums as returned; diagnostics only; no clipping, forced '
                     'positivity, threshold or acceptance; index order (R, phi, eta)'}


def _xi_roundtrip(result, xi):
    bs = result.get('boundary_state')
    keys = ('xi_R', 'xi_phi', 'xi_z')
    if not isinstance(bs, Mapping) or any(k not in bs for k in keys):
        return 'UNAVAILABLE'
    return all(isinstance(bs[k], np.ndarray) and np.array_equal(bs[k], a)
               for k, a in zip(keys, xi))


def evaluate_modal_candidate(*, binding_module, action_module, mesh, base_fields, c_light,
                             gamma, tolerances, provenance, mode_results, nphi, imag_atol,
                             imag_rtol, induced_response):
    """Assemble once, call binding_module.evaluate_action exactly once, report.

    ok=True means only: assembly passed, the single evaluate_action call returned
    ok=True, and the all-slot residual report was computed. 'acceptance' is
    always 'NOT_ASSESSED_BY_THIS_WRAPPER'.
    """
    state = {'calls': 0, 'assembly': None, 'result': None, 'returned': False}

    def fail(stage, reason):
        out = _fail(stage, reason)
        out['evaluate_action_call_count'] = state['calls']
        if state['assembly'] is not None:
            out['assembly'] = state['assembly']
        if state['returned']:
            out['action_result'] = state['result']      # preserved by identity, unmodified
        return out

    try:
        try:
            fn, tol = _check_join(binding_module, action_module, induced_response, tolerances)
        except _Reject as rej:
            return fail(rej.stage, rej.reason)
        assembly = assemble_real_displacement(mesh=mesh, mode_results=mode_results, nphi=nphi,
                                              imag_atol=imag_atol, imag_rtol=imag_rtol)
        state['assembly'] = assembly
        if assembly.get('ok') is not True:
            return fail('assembly', 'assembly stage %s: %s' % (assembly.get('stage'),
                                                               assembly.get('reason')))
        xi = assembly['xi']
        state['calls'] = 1
        try:
            result = fn(action_module=action_module, mesh=mesh, base_fields=base_fields, xi=xi,
                        induced_response=induced_response, gamma=gamma, c_light=c_light,
                        base_axisymmetry_rtol=tol['base_axisymmetry_rtol'],
                        polytrope_consistency_rtol=tol['polytrope_consistency_rtol'],
                        base_provenance=provenance)
        except Exception as exc:
            return fail('evaluate_action_raised', '%s: %s' % (type(exc).__name__, exc))
        state['result'], state['returned'] = result, True
        if not isinstance(result, Mapping):
            return fail('evaluate_action_output', 'evaluate_action returned %s, not a mapping'
                        % type(result).__name__)
        if result.get('ok') is not True:
            return fail('evaluate_action_not_ok', 'evaluate_action returned ok=%r, stage %r: %r'
                        % (result.get('ok'), result.get('stage'), result.get('reason')))
        gs = assembly['grid_shape']
        try:
            with np.errstate(**_ERRSTATE):
                report = _fourier_report(result, gs, assembly['nphi'])
        except _Reject as rej:
            return fail(rej.stage, rej.reason)
        except FloatingPointError as exc:
            return fail('euler_residual_report', 'FloatingPointError (%s)' % exc)
        sf = result.get('source_feedback')
        return {
            'ok': True, 'module': MODULE_TAG, 'stage': 'modal_candidate_evaluated',
            'acceptance': ACCEPTANCE,
            'acceptance_scope': ('ok=True means only that assembly passed, evaluate_action was '
                                 'called once and returned ok=True, and the all-slot residual '
                                 'report was computed; no convergence, threshold, retained-mode, '
                                 'physical or calibration acceptance is made'),
            'evaluate_action_call_count': state['calls'],
            'action_result': result,                    # complete output, by identity
            'action_result_module': result.get('module'),
            'response_call_count_reported': (sf.get('response_call_count')
                                             if isinstance(sf, Mapping) else 'UNAVAILABLE'),
            'assembly': assembly,
            'inner_accepted_by_m': assembly['inner_accepted_by_m'],
            'modes_with_accepted_inner_false': assembly['modes_with_accepted_inner_false'],
            'euler_residual_angular_fourier': report,
            'density_pressure_diagnostics': _density_pressure(result, gs),
            'diagnostic_availability': _availability(result),
            'xi_bitwise_equal_in_returned_boundary_state': _xi_roundtrip(result, xi),
            'not_done': NOT_DONE,
        }
    except Exception as exc:
        return fail('internal', '%s: %s' % (type(exc).__name__, exc))
