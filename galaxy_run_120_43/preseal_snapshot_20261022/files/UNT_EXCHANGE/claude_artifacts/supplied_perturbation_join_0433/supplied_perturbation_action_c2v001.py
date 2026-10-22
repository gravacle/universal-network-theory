"""INERT supplied-perturbation action join (UNT 0433, Claude2 c2v001).

One public function:

  evaluate_supplied_perturbations(*, mesh, base_fields, delta_rho, deltaP, deltaK,
                                  delta_v, c_light, gamma, induced_response,
                                  provenance)

Every physical perturbation is SUPPLIED by the caller (root) as a finite real
array of exactly mesh['grid_shape']; delta_v = (w_R, w_phi, w_z) holds physical
orthonormal cylindrical velocity components. Nothing is reconstructed: no
density from a displacement, no pressure from entropy, no velocity from a
displacement ansatz, and no missing value becomes zero.

Exactly ONE native callback:  induced_response(delta_f_n=-c_light**2*delta_rho).
Its complete output (native_response with all 10 fields, and lapse_component)
is retained by identity. Weak-field contract (0427 c2v002):
  induced potential = c_light**2 * lapse_component['delta_n']
  dPhi = base_fields['angular_forcing_dPhi'] + induced potential
Phi0 already contains the base-source offset; it enters only r0, never dPhi.

  r0 = (dR(Phi0) + dR(P0)/rho0 - R*Omega**2, 0, dz(Phi0) + dz(P0)/rho0)

Supplied-state STRONG residual diagnostics (0433, verbatim, w = delta_v):
  R    r0_R + Omega*dphi(w_R) - 2*Omega*w_phi + dR(deltaP)/rho0
       - delta_rho*dR(P0)/rho0**2 + dR(dPhi)
  phi  Omega*dphi(w_phi) + (2*Omega + R*dR(Omega))*w_R + R*dz(Omega)*w_z
       + dphi(deltaP)/(rho0*R) + dphi(dPhi)/R
  z    r0_z + Omega*dphi(w_z) + dz(deltaP)/rho0 - delta_rho*dz(P0)/rho0**2
       + dz(dPhi)
  continuity  dR(R*rho0*w_R)/R + dphi(rho0*w_phi)/R + dz(rho0*w_z)
              + Omega*dphi(delta_rho)
  entropy     Omega*dphi(deltaK) + w_R*dR(K0) + w_z*dz(K0)
  EOS         deltaP - gamma*P0*delta_rho/rho0 - rho0**gamma*deltaK
dR, dphi, dz are ONLY mesh['partial_R'], mesh['partial_phi'], mesh['partial_z']
(root make_mesh callables; dphi is per radian). These residuals are not an
assertion that a weak discretization makes them zero and are not a nonlinear
acceptance test.

Contract: numpy + stdlib only; nothing executed at import beyond constant,
class and function definitions; no I/O; keyword-only arguments without
defaults; fail-closed result dicts. Module arithmetic raises on
divide/overflow/invalid (underflow ignored); callbacks run under the caller's
errstate. No threshold, clipping, correction, iteration, calibration, solve or
acceptance: 'status' is always 'not_assessed'.
"""
import math
from collections.abc import Mapping

import numpy as np

MODULE_TAG = 'supplied_perturbation_action_c2v001'
STATUS = 'not_assessed'
LAPSE_FORM = 'weak_field_delta_n'
N_NATIVE_FIELDS = 10
# Exact key sets of the root bind_full_response callback output (binding v002 L166-168).
RESPONSE_KEYS = frozenset(('native_response', 'lapse_component'))
NATIVE_RESPONSE_KEYS = frozenset(('fields_complex', 'imaginary_norms', 'reality_bounds',
                                  'unit_response_custody', 'scope'))
LAPSE_KEYS = frozenset(('form', 'delta_n'))
UNIT_SOURCE_CONVENTION = 'unit_positive_lapse_e_n_full_signed'   # binding v002 L138
MESH_ARRAY_KEYS = ('R', 'phi', 'volume_weights_m3')
MESH_CALLABLE_KEYS = ('partial_R', 'partial_phi', 'partial_z')
BASE_ARRAY_KEYS = ('rho0', 'K0', 'P0', 'Omega', 'Phi0', 'angular_forcing_dPhi')
AXISYMMETRIC_BASE_KEYS = ('rho0', 'K0', 'P0', 'Omega', 'Phi0')
# NOT named by 0433 (missing interface fact 1): explicit caller tolerance in base_fields.
AXISYMMETRY_TOL_KEY = 'axisymmetry_phi_variation_rtol'
COMPONENTS = ('R', 'phi', 'z')
RESIDUAL_KEYS = ('euler_R', 'euler_phi', 'euler_z', 'continuity', 'entropy', 'eos_discrepancy')
_ERRSTATE = {'divide': 'raise', 'over': 'raise', 'invalid': 'raise', 'under': 'ignore'}
AXISYMMETRY_TEST = ('for f in (rho0, K0, P0, Omega, Phi0): dev = max|f[i,j,k] - f[i,0,k]| over all '
                    'nodes; ratio = 0 if dev == 0 else dev / max|f|; require ratio <= '
                    "base_fields['%s'] (caller value; 0433 gives no tolerance)" % AXISYMMETRY_TOL_KEY)
CONVENTIONS = {
    'mesh_layout': 'grid_shape = (nr, nphi, neta) from root make_mesh; axes (R, phi, eta)',
    'phi_nodes': 'mesh[phi] line equals 2*pi*arange(nphi)/nphi bitwise; nphi even',
    'velocity': 'delta_v = (w_R, w_phi, w_z) physical orthonormal components; w_phi is a speed',
    'derivatives': "only mesh['partial_R'], mesh['partial_phi'], mesh['partial_z']; dphi per radian",
    'source': 'delta_f_n = -c_light**2 * delta_rho (supplied delta_rho; never recomputed)',
    'potential': ("induced = c_light**2 * lapse_component['delta_n'] (weak_field_delta_n); "
                  'dPhi = angular_forcing_dPhi + induced; Phi0 never added to dPhi'),
    'r0': 'r0 = (dR(Phi0) + dR(P0)/rho0 - R*Omega**2, 0, dz(Phi0) + dz(P0)/rho0)',
    'residual_label': 'supplied-state STRONG residual diagnostics (0433 formulas verbatim)',
    'angular_norms': ('F = np.fft.fft(a, axis=1)/nphi (0431 FFT/nphi); every slot s = 0..nphi-1; '
                      'signed m = s for s <= nphi/2, s - nphi otherwise; unweighted l2 over '
                      '(R, eta) nodes, evaluated with max-abs scaling'),
    'mass': "float(np.sum(mesh['volume_weights_m3'] * delta_rho)) (root constraint_rows form)",
}
NOT_DONE = (
    'no reconstruction of density, pressure, entropy or velocity from any other field',
    'no missing value set to zero (r0_phi = 0 is the 0433 formula, not a fill)',
    'no second native callback; no Fourier transform or kernel solve here',
    'no base-source offset added; Phi0 enters r0 only',
    'no threshold, clipping, forced positivity, correction, iteration, calibration or acceptance',
    'no weak-form residual, boundary row, tail or continuum-derivative certificate',
    'no target or model selection',
)


class _Reject(Exception):
    def __init__(self, stage, reason):
        Exception.__init__(self, reason)
        self.stage = stage
        self.reason = reason


def _readonly(a, dtype=np.float64):
    out = np.array(a, dtype=dtype, copy=True)
    out.flags.writeable = False
    return out


def _is_int(v):
    return isinstance(v, (int, np.integer)) and not isinstance(v, (bool, np.bool_))


def _text(stage, name, value):
    if not isinstance(value, str) or not value.strip():
        raise _Reject(stage, name + ': nonempty string required')
    return value


def _scalar(stage, name, value, positive):
    if isinstance(value, (bool, np.bool_)) or not isinstance(
            value, (int, float, np.integer, np.floating)):
        raise _Reject(stage, name + ': real scalar required')
    v = float(value)
    if not math.isfinite(v):
        raise _Reject(stage, name + ': finite value required')
    if positive and not v > 0:
        raise _Reject(stage, name + ': strictly positive value required')
    if not positive and v < 0:
        raise _Reject(stage, name + ': nonnegative value required')
    return v


def _real_array(stage, name, value, shape):
    """Plain numpy real array of exactly `shape`, finite; returned as a float64 copy."""
    if not isinstance(value, np.ndarray) or isinstance(value, np.ma.MaskedArray):
        raise _Reject(stage, '%s: plain numpy array required, got %s' % (name, type(value).__name__))
    k = value.dtype.kind
    if k not in 'fiu' or (k == 'f' and value.dtype.itemsize > 8):
        raise _Reject(stage, '%s: real float64-representable dtype required, got %s (complex '
                      'inputs are rejected, never truncated)' % (name, value.dtype))
    if value.shape != shape:
        raise _Reject(stage, '%s: shape %s != required %s (no broadcasting)'
                      % (name, value.shape, shape))
    out = np.array(value, dtype=np.float64, copy=True)
    if not np.all(np.isfinite(out)):
        raise _Reject(stage, name + ': nonfinite values')
    return out


def _require_finite_outputs(obj, path):
    if isinstance(obj, np.ndarray):
        if obj.dtype.kind not in 'fiub' or not np.all(np.isfinite(obj)):
            raise _Reject('output_validation', '%s: non-finite or non-real returned array' % path)
    elif isinstance(obj, (float, np.floating)):
        if not math.isfinite(float(obj)):
            raise _Reject('output_validation', '%s: non-finite returned value' % path)
    elif isinstance(obj, Mapping):
        for k, v in obj.items():
            _require_finite_outputs(v, '%s[%r]' % (path, k))
    elif isinstance(obj, (tuple, list)):
        for i, v in enumerate(obj):
            _require_finite_outputs(v, '%s[%d]' % (path, i))


# --------------------------------------------------------------------------- validation

def _mesh(mesh):
    stage = 'input_validation'
    if not isinstance(mesh, Mapping):
        raise _Reject(stage, 'mesh: mapping (root make_mesh output) required')
    for key in ('grid_shape',) + MESH_ARRAY_KEYS + MESH_CALLABLE_KEYS + ('derivative_rule_description',):
        if key not in mesh:
            raise _Reject(stage, 'mesh: key %r required' % key)
    gs = mesh['grid_shape']
    if not isinstance(gs, tuple) or len(gs) != 3 or not all(_is_int(n) and n >= 1 for n in gs):
        raise _Reject(stage, 'mesh[grid_shape]: tuple (nr, nphi, neta) of positive ints required')
    gs = tuple(int(n) for n in gs)
    nphi = gs[1]
    if nphi % 2 or nphi < 2:
        raise _Reject(stage, 'mesh[grid_shape][1] = nphi must be even (root make_mesh)')
    for key in MESH_CALLABLE_KEYS:
        if not callable(mesh[key]):
            raise _Reject(stage, 'mesh[%s]: callable required' % key)
    desc = _text(stage, 'mesh[derivative_rule_description]', mesh['derivative_rule_description'])
    R = _real_array(stage, 'mesh[R]', mesh['R'], gs)
    if not np.all(R > 0):
        raise _Reject(stage, 'mesh[R]: strictly positive interior radius required at every node')
    if not np.array_equal(R, np.broadcast_to(R[:, :1, :1], gs)):
        raise _Reject(stage, 'mesh[R]: must depend on the radial axis only (root layout)')
    phi = _real_array(stage, 'mesh[phi]', mesh['phi'], gs)
    line = phi[0, :, 0]
    if not np.array_equal(phi, np.broadcast_to(line[None, :, None], gs)):
        raise _Reject(stage, 'mesh[phi]: must depend on the phi axis only')
    if not np.array_equal(line, 2 * np.pi * np.arange(nphi) / nphi):
        raise _Reject(stage, 'mesh[phi]: nodes must equal 2*pi*arange(nphi)/nphi bitwise '
                      '(root make_mesh; required by the FFT/nphi slot convention)')
    w = _real_array(stage, 'mesh[volume_weights_m3]', mesh['volume_weights_m3'], gs)
    if not np.all(w > 0):
        raise _Reject(stage, 'mesh[volume_weights_m3]: strictly positive quadrature weights '
                      'required (root make_mesh guarantees them)')
    ops = dict((key, mesh[key]) for key in MESH_CALLABLE_KEYS)   # captured once
    return gs, R, w, desc, ops


def _base(base_fields, gs):
    stage = 'input_validation'
    if not isinstance(base_fields, Mapping):
        raise _Reject(stage, 'base_fields: mapping required')
    for key in BASE_ARRAY_KEYS + (AXISYMMETRY_TOL_KEY,):
        if key not in base_fields:
            raise _Reject(stage, 'base_fields: key %r required%s' % (
                key, ' (0433 gives no axisymmetry tolerance; explicit caller value required, '
                     'never a module constant)' if key == AXISYMMETRY_TOL_KEY else ''))
    tol = _scalar(stage, 'base_fields[%s]' % AXISYMMETRY_TOL_KEY, base_fields[AXISYMMETRY_TOL_KEY],
                  positive=False)
    arrays = dict((k, _real_array(stage, 'base_fields[%s]' % k, base_fields[k], gs))
                  for k in BASE_ARRAY_KEYS)
    for k in ('rho0', 'K0', 'P0'):
        if not np.all(arrays[k] > 0):
            raise _Reject(stage, 'base_fields[%s]: strictly positive finite value required at every '
                          'interior node; no clamp' % k)
    ignored = tuple(sorted(str(k) for k in base_fields.keys()
                           if k not in BASE_ARRAY_KEYS and k != AXISYMMETRY_TOL_KEY))
    return arrays, tol, ignored


def _axisymmetry(arrays, tol):
    out = {}
    for k in AXISYMMETRIC_BASE_KEYS:
        f = arrays[k]
        dev = float(np.max(np.abs(f - f[:, :1, :])))
        ratio = 0.0 if dev == 0.0 else dev / float(np.max(np.abs(f)))
        out[k] = ratio
        if not ratio <= tol:
            raise _Reject('base_checks', 'base_fields[%s] not axisymmetric: max|f - f[:,0,:]| / '
                          'max|f| = %r > %s = %r' % (k, ratio, AXISYMMETRY_TOL_KEY, tol))
    return out


# --------------------------------------------------------------------------- response schema

def _validate_response(response, gs):
    stage = 'response_schema'
    if not isinstance(response, Mapping):
        raise _Reject(stage, 'induced_response returned %s, not a mapping' % type(response).__name__)
    if set(response.keys()) != RESPONSE_KEYS:
        raise _Reject(stage, 'induced_response output keys %s != root keys %s'
                      % (sorted(map(str, response.keys())), sorted(RESPONSE_KEYS)))
    native, lapse = response['native_response'], response['lapse_component']
    if not isinstance(native, Mapping) or set(native.keys()) != NATIVE_RESPONSE_KEYS:
        raise _Reject(stage, 'native_response: mapping with exactly root keys %s required'
                      % sorted(NATIVE_RESPONSE_KEYS))
    fields = native['fields_complex']
    if not isinstance(fields, np.ndarray) or isinstance(fields, np.ma.MaskedArray):
        raise _Reject(stage, 'native_response[fields_complex]: plain numpy array required')
    if fields.dtype != np.complex128:
        raise _Reject(stage, 'native_response[fields_complex]: complex128 required (root '
                      'dtype=complex), got %s; imaginary parts are never dropped' % fields.dtype)
    want = gs + (N_NATIVE_FIELDS,)
    if fields.shape != want:
        raise _Reject(stage, 'native_response[fields_complex]: shape %s != grid_shape+(10,) = %s'
                      % (fields.shape, want))
    bad = []
    for a in range(N_NATIVE_FIELDS):
        if not np.all(np.isfinite(fields[..., a].real)):
            bad.append('field %d real' % a)
        if not np.all(np.isfinite(fields[..., a].imag)):
            bad.append('field %d imaginary' % a)
    if bad:
        raise _Reject(stage, 'native_response[fields_complex]: nonfinite parts in %s (all 10 '
                      'fields are validated, not only the lapse)' % ', '.join(bad))
    declared = {}
    for key in ('imaginary_norms', 'reality_bounds'):
        v = native[key]
        if (not isinstance(v, np.ndarray) or v.dtype.kind != 'f' or v.shape != (N_NATIVE_FIELDS,)
                or not np.all(np.isfinite(v)) or np.any(v < 0)):
            raise _Reject(stage, 'native_response[%s]: finite nonnegative float array of shape '
                          '(10,) required (root L163)' % key)
        declared[key] = _readonly(v)
    custody = native['unit_response_custody']
    if not isinstance(custody, Mapping) or custody.get('source_convention') != UNIT_SOURCE_CONVENTION:
        raise _Reject(stage, 'native_response[unit_response_custody]: mapping with '
                      'source_convention %r required (root L138)' % UNIT_SOURCE_CONVENTION)
    _text(stage, 'native_response[scope]', native['scope'])
    if not isinstance(lapse, Mapping) or set(lapse.keys()) != LAPSE_KEYS:
        raise _Reject(stage, "lapse_component: mapping with exactly keys {'form','delta_n'} required")
    if lapse['form'] != LAPSE_FORM:
        raise _Reject(stage, 'lapse_component[form] %r != %r; no silent choice'
                      % (lapse['form'], LAPSE_FORM))
    dn = lapse['delta_n']
    if (not isinstance(dn, np.ndarray) or dn.dtype != np.float64 or dn.shape != gs
            or not np.all(np.isfinite(dn))):
        raise _Reject(stage, 'lapse_component[delta_n]: finite float64 array of grid_shape required')
    if not np.array_equal(dn, fields[..., 0].real):
        raise _Reject(stage, 'lapse_component[delta_n] != fields_complex[..., 0].real bitwise '
                      '(root L168 definition)')
    # Root's reality rule (L163-164) on the declared values AND on the actual returned fields.
    stage = 'response_reality'
    recomputed = np.linalg.norm(fields.reshape(-1, N_NATIVE_FIELDS).imag, axis=0)
    if not np.all(np.isfinite(recomputed)):
        raise _Reject(stage, 'recomputed imaginary norms nonfinite')
    if not np.array_equal(recomputed, declared['imaginary_norms']):
        raise _Reject(stage, 'declared imaginary_norms != np.linalg.norm(fields_complex.reshape(-1,10)'
                      '.imag, axis=0) (root L163 on the returned fields)')
    bound = declared['reality_bounds']
    over = [a for a in range(N_NATIVE_FIELDS) if not recomputed[a] <= bound[a]]
    if over:
        raise _Reject(stage, 'imaginary norms exceed root-declared reality_bounds in fields %s' % over)
    checks = {
        'fields_complex_shape': want, 'fields_complex_dtype': 'complex128',
        'all_10_fields_finite_real_and_imaginary': True,
        'declared_imaginary_norms': declared['imaginary_norms'],
        'recomputed_imaginary_norms': _readonly(recomputed),
        'declared_reality_bounds': bound,
        'declared_equals_recomputed_imaginary_norms': True,
        'root_reality_rule': ('imag_a <= reality_bounds_a for a = 0..9, applied to declared and to '
                              'recomputed norms (root L163-164); bounds taken as declared'),
        'lapse_form': LAPSE_FORM,
        'lapse_delta_n_equals_field0_real_bitwise': True,
        'field0_imaginary_norm': float(recomputed[0]),
        'imaginary_parts': ('retained unmodified in native_response; the potential uses root '
                            'lapse_component[delta_n] = Re(field 0) as root defines it'),
        'unit_response_custody_source_convention': UNIT_SOURCE_CONVENTION,
    }
    return dn, checks


# --------------------------------------------------------------------------- diagnostics

def _scaled_l2(a, axis):
    """sqrt(sum |a|**2) with max-abs scaling (no overflow for finite large values)."""
    absa = np.abs(a)
    s = float(np.max(absa))
    if s == 0.0:
        return np.zeros(absa.shape[1]) if axis is not None else 0.0
    g = absa / s
    if axis is None:
        return s * math.sqrt(float(np.sum(g * g)))
    return s * np.sqrt(np.sum(g * g, axis=axis))


def _angular_report(residuals, nphi):
    k = np.arange(nphi)
    signed = np.where(k <= nphi // 2, k, k - nphi)
    comps = {}
    for name in RESIDUAL_KEYS:
        a = residuals[name]
        F = np.fft.fft(a, axis=1) / nphi
        if not np.all(np.isfinite(F)):
            raise _Reject('angular_norms', '%s: nonfinite angular transform' % name)
        comps[name] = {
            'slot_l2_over_R_eta': _readonly(_scaled_l2(F, (0, 2))),
            'slot_max_abs': _readonly(np.max(np.abs(F), axis=(0, 2))),
            'all_slots_l2': _scaled_l2(F, None),
            'nodal_l2_over_sqrt_nphi': _scaled_l2(a, None) / math.sqrt(nphi),
        }
    return {
        'slot_index': _readonly(k, np.int64), 'signed_m': _readonly(signed, np.int64),
        'nyquist_slot_index': nphi // 2,
        'euler_components': ('euler_R', 'euler_phi', 'euler_z'),
        'components': comps,
        'convention': CONVENTIONS['angular_norms'] + '; nodal_l2_over_sqrt_nphi equals '
                      'all_slots_l2 by Parseval (reported, not gated)',
        'status': STATUS,
    }


def _idx(i, gs):
    return tuple(int(n) for n in np.unravel_index(int(i), gs))


# --------------------------------------------------------------------------- evaluation

def _evaluate(*, state, caller_err, mesh, base_fields, delta_rho, deltaP, deltaK, delta_v,
              c_light, gamma, induced_response, provenance):
    stage = 'input_validation'
    prov = _text(stage, 'provenance', provenance)
    if not callable(induced_response):
        raise _Reject(stage, 'induced_response: callable required')
    gs, R, weights, desc, ops = _mesh(mesh)
    nphi = gs[1]
    base, ax_tol, ignored = _base(base_fields, gs)
    drho = _real_array(stage, 'delta_rho', delta_rho, gs)
    dP = _real_array(stage, 'deltaP', deltaP, gs)
    dK = _real_array(stage, 'deltaK', deltaK, gs)
    if not isinstance(delta_v, tuple) or len(delta_v) != 3:
        raise _Reject(stage, 'delta_v: tuple of exactly three physical components (R, phi, z) required')
    w_R, w_phi, w_z = (_real_array(stage, 'delta_v[%s]' % c, v, gs)
                       for c, v in zip(COMPONENTS, delta_v))
    c_light = _scalar(stage, 'c_light', c_light, positive=True)
    gamma = _scalar(stage, 'gamma', gamma, positive=True)
    rho0, K0, P0 = base['rho0'], base['K0'], base['P0']
    Omega, Phi0, forcing = base['Omega'], base['Phi0'], base['angular_forcing_dPhi']

    state['trace'].append('base_checks')
    ax_ratio = _axisymmetry(base, ax_tol)
    rho0_gamma = rho0 ** gamma
    polytrope = float(np.max(np.abs(P0 - K0 * rho0_gamma) / P0))

    counts = {'partial_R': 0, 'partial_phi': 0, 'partial_z': 0}

    def d(key, field):
        arg = _readonly(field)
        counts[key] += 1
        try:
            with np.errstate(**caller_err):
                out = ops[key](arg)
        except Exception as exc:
            raise _Reject('derivative_callback', 'mesh[%s] raised %s: %s'
                          % (key, type(exc).__name__, exc))
        return _real_array('derivative_callback', 'mesh[%s] output' % key,
                           np.asarray(out) if not isinstance(out, np.ndarray) else out, gs)

    def dR(f):
        return d('partial_R', f)

    def dphi(f):
        return d('partial_phi', f)

    def dz(f):
        return d('partial_z', f)

    # ---- everything independent of the native response, before the single call
    state['trace'].append('pre_response_derivatives')
    dphi_ratio = {}
    for k in AXISYMMETRIC_BASE_KEYS:
        num = float(np.max(np.abs(dphi(base[k]))))
        den = float(np.max(np.abs(base[k])))
        dphi_ratio[k] = (0.0 if num == 0.0 else num / den if den > 0.0
                         else 'UNDEFINED: zero field with nonzero partial_phi output')
    dR_P0, dz_P0 = dR(P0), dz(P0)
    r0_R = dR(Phi0) + dR_P0 / rho0 - R * Omega ** 2
    r0_phi = np.zeros(gs)
    r0_z = dz(Phi0) + dz_P0 / rho0
    continuity = (dR(R * rho0 * w_R) / R + dphi(rho0 * w_phi) / R + dz(rho0 * w_z)
                  + Omega * dphi(drho))
    entropy = Omega * dphi(dK) + w_R * dR(K0) + w_z * dz(K0)
    eos = dP - gamma * P0 * drho / rho0 - rho0_gamma * dK
    # Euler pieces not involving dPhi (same 0433 expressions, evaluated left to right below)
    Om_dphi_wR, Om_dphi_wphi, Om_dphi_wz = Omega * dphi(w_R), Omega * dphi(w_phi), Omega * dphi(w_z)
    dR_dP, dphi_dP, dz_dP = dR(dP), dphi(dP), dz(dP)
    dR_Om, dz_Om = dR(Omega), dz(Omega)

    # ---- exactly one native callback with the supplied density
    state['trace'].append('source_feedback')
    delta_f_n = -c_light ** 2 * drho
    if not np.all(np.isfinite(delta_f_n)):
        raise _Reject('source_feedback', 'delta_f_n: nonfinite')
    passed = _readonly(delta_f_n)
    state['calls'] += 1
    try:
        with np.errstate(**caller_err):
            response = induced_response(delta_f_n=passed)
    except Exception as exc:
        raise _Reject('induced_response_raised', '%s: %s' % (type(exc).__name__, exc))
    state['response'], state['returned'] = response, True
    if not np.array_equal(passed, delta_f_n):
        raise _Reject('source_feedback', 'induced_response mutated its delta_f_n input')

    state['trace'].append('response_validation')
    delta_n, response_checks = _validate_response(response, gs)
    state['validated'] = True

    # ---- potential and Euler residuals (0433 verbatim)
    state['trace'].append('potential')
    induced = c_light ** 2 * np.array(delta_n, dtype=np.float64, copy=True)
    dPhi = forcing + induced
    state['trace'].append('euler_residual')
    euler_R = (r0_R + Om_dphi_wR - 2 * Omega * w_phi + dR_dP / rho0
               - drho * dR_P0 / rho0 ** 2 + dR(dPhi))
    euler_phi = (Om_dphi_wphi + (2 * Omega + R * dR_Om) * w_R + R * dz_Om * w_z
                 + dphi_dP / (rho0 * R) + dphi(dPhi) / R)
    euler_z = (r0_z + Om_dphi_wz + dz_dP / rho0 - drho * dz_P0 / rho0 ** 2 + dz(dPhi))
    residuals = {'euler_R': euler_R, 'euler_phi': euler_phi, 'euler_z': euler_z,
                 'continuity': continuity, 'entropy': entropy, 'eos_discrepancy': eos}
    for name in RESIDUAL_KEYS:
        if not np.all(np.isfinite(residuals[name])):
            raise _Reject('euler_residual', '%s: nonfinite' % name)

    # ---- diagnostics (reported, never gated)
    state['trace'].append('diagnostics')
    angular = _angular_report(residuals, nphi)
    rho_tot = rho0 + drho
    P_tot = P0 + dP
    ratio = np.abs(drho / rho0)
    mass = float(np.sum(weights * drho))
    ro = _readonly
    result = {
        'ok': True, 'module': MODULE_TAG, 'stage': 'supplied_perturbations_evaluated',
        'status': STATUS,
        'status_scope': ('ok=True means only: inputs validated, the single native callback returned '
                         'a schema- and reality-valid response, and all arrays below are finite. '
                         'No threshold, convergence, physical or calibration acceptance.'),
        'response_call_count': state['calls'],
        'grid_shape': gs, 'provenance': prov, 'derivative_rule_description': desc,
        'inputs': {'delta_rho': ro(drho), 'deltaP': ro(dP), 'deltaK': ro(dK),
                   'delta_v': (ro(w_R), ro(w_phi), ro(w_z)), 'c_light': c_light, 'gamma': gamma},
        'base_fields_used': dict((k, ro(v)) for k, v in base.items()),
        'ignored_base_field_keys': ignored,
        'source': {'delta_f_n': ro(delta_f_n),
                   'formula': 'delta_f_n = -c_light**2 * delta_rho (supplied delta_rho)'},
        'induced_response_output': response,                      # complete, by identity
        'native_response': response['native_response'],          # all 10 fields, by identity
        'lapse_component': response['lapse_component'],          # by identity
        'response_checks': response_checks,
        'potential': {'angular_forcing_dPhi': ro(forcing), 'induced_potential': ro(induced),
                      'dPhi': ro(dPhi),
                      'formula': 'dPhi = angular_forcing_dPhi + c_light**2 * delta_n; Phi0 not added'},
        'r0': {'R': ro(r0_R), 'phi': ro(r0_phi), 'z': ro(r0_z)},
        'residuals': dict((k, ro(residuals[k])) for k in RESIDUAL_KEYS),
        'residual_label': 'supplied-state STRONG residual diagnostics',
        'residual_scope': ('strong pointwise residuals of the supplied state through the mesh '
                           'derivative callables; not an assertion that a weak discretization '
                           'makes them zero; not a nonlinear acceptance test'),
        'angular_slot_norms': angular,
        'positivity_diagnostics': {
            'min_rho0_plus_delta_rho': float(np.min(rho_tot)),
            'argmin_rho0_plus_delta_rho': _idx(np.argmin(rho_tot), gs),
            'min_P0_plus_deltaP': float(np.min(P_tot)),
            'argmin_P0_plus_deltaP': _idx(np.argmin(P_tot), gs),
            'max_abs_delta_rho_over_rho0': float(np.max(ratio)),
            'argmax_abs_delta_rho_over_rho0': _idx(np.argmax(ratio), gs),
            'scope': 'unclipped first-order sums; index order (R, phi, eta); not gated'},
        'mass_perturbation': {
            'total_quadrature_mass_perturbation': mass,
            'weights': ("mesh['volume_weights_m3'] = wr[:,None,None]*(2*pi/n_phi)*H[:,None,None]"
                        '*we[None,None,:] (root make_mesh L70-71: supplied R dR radial weights, '
                        'uniform angle, half-thickness H, eta Gauss weights)'),
            'formula': CONVENTIONS['mass']},
        'base_checks': {'axisymmetry_test': AXISYMMETRY_TEST,
                        'axisymmetry_phi_variation_rtol': ax_tol,
                        'axisymmetry_phi_variation_ratio': ax_ratio,
                        'dphi_ratio_reported_not_gated': dphi_ratio,
                        'polytrope_max_relative_mismatch_reported_not_gated': polytrope},
        'derivative_call_counts': dict(counts),
        'conventions': dict(CONVENTIONS),
        'not_done': NOT_DONE,
    }
    state['trace'].append('output_validation')
    for key, val in result.items():
        if key not in ('induced_response_output', 'native_response', 'lapse_component'):
            _require_finite_outputs(val, key)
    return result


def evaluate_supplied_perturbations(*, mesh, base_fields, delta_rho, deltaP, deltaK, delta_v,
                                    c_light, gamma, induced_response, provenance):
    """Evaluate supplied-state strong residual diagnostics; see module docstring.

    Returns {'ok': True, ...} or a fail-closed {'ok': False, 'module', 'stage',
    'reason', 'status', 'response_call_count'} which, once the native callback
    has returned, also carries 'induced_response_output' (by identity) and
    'induced_response_validated'. 'status' is always 'not_assessed'.
    """
    caller_err = np.geterr()
    state = {'calls': 0, 'returned': False, 'response': None, 'validated': False,
             'trace': ['input_validation']}

    def fail(stage, reason):
        out = {'ok': False, 'module': MODULE_TAG, 'stage': stage, 'reason': reason,
               'status': STATUS, 'response_call_count': state['calls']}
        if state['returned']:
            out['induced_response_output'] = state['response']   # retained, unmodified
            out['induced_response_validated'] = state['validated']
        return out

    try:
        with np.errstate(**_ERRSTATE):
            return _evaluate(state=state, caller_err=caller_err, mesh=mesh, base_fields=base_fields,
                             delta_rho=delta_rho, deltaP=deltaP, deltaK=deltaK, delta_v=delta_v,
                             c_light=c_light, gamma=gamma, induced_response=induced_response,
                             provenance=provenance)
    except _Reject as rej:
        return fail(rej.stage, rej.reason)
    except FloatingPointError as exc:
        return fail('floating_point', 'module arithmetic during %s raised FloatingPointError (%s); '
                    'no value is returned' % (state['trace'][-1], exc))
    except Exception as exc:
        return fail('internal', '%s: %s' % (type(exc).__name__, exc))
