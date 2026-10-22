"""INERT leading-order noncircular displacement action (UNT 0427, Claude2 c2v001).

Implements ONLY sections 3-4 of
  DDO_NONCIRCULAR_DISPLACEMENT_CORRECTION_PROPOSED_V001.txt
  sha256 d97ae766d98a03e14b5eaff39e1b9dcf0395167164eef0e135b5553709980cb4
with the qualifications of
  NONCIRCULAR_DISPLACEMENT_EQUATIONS_REVIEW_V001.json
  sha256 99fca0f60683d0b40e13be4fd9c4b78936d2cc8c07753bead84f8fed863fad4e

Matrix-free BULK action of a stationary displacement xi about a caller-supplied
axisymmetric base (rho0, K0, P0, v0 = R Omega(R,z) e_phi, gamma):
  drho = -div(rho0 xi)   (cylindrical; conservative form (1/R) d_R(R rho0 xi_R))
  dK   = -xi . grad K0
  dP   = cs2 drho + rho0**gamma dK,  cs2 = gamma P0 / rho0
  dv_R = Omega d_phi xi_R,  dv_z = Omega d_phi xi_z,
  dv_phi = Omega d_phi xi_phi - R (Omega_R xi_R + Omega_z xi_z)
  df_n = -c**2 drho  -> caller's complete native response, called exactly once
  dPhi_total = dPhi_angular_forcing + c**2 * (stipulated lapse component)
and the three stationary linearized Euler residuals (spec section 3 signs):
  res_R   = Omega d_phi dv_R - 2 Omega dv_phi + d_R dPhi + d_R dP/rho0
            - drho P0_R/rho0**2 + r0_R
  res_phi = Omega d_phi dv_phi + (2 Omega + R Omega_R) dv_R + R Omega_z dv_z
            + d_phi dPhi/R + d_phi dP/(rho0 R) + r0_phi
  res_z   = Omega d_phi dv_z + d_z dPhi + d_z dP/rho0 - drho P0_z/rho0**2 + r0_z

Physical orthonormal cylindrical components throughout (xi_phi, dv_phi, r0_phi
are physical lengths/speeds/accelerations, NOT angular rates). d_phi is the
derivative per radian; the physical azimuthal gradient is d_phi/R.

Units: SI or any caller-consistent system (declared by `unit_system`). In SI:
R,z,xi [m]; phi [rad]; rho [kg m^-3]; P [Pa]; K [Pa (kg m^-3)^-gamma];
Omega [rad s^-1]; c [m s^-1]; df_n [J m^-3]; dPhi [m^2 s^-2]; dv [m s^-1];
residuals and r0 [m s^-2].

Contract: no I/O, nothing executed at import beyond constant definitions,
numpy + stdlib only, keyword-only public arguments WITHOUT defaults, every
failure returns a fail-closed dict {'ok': False, ...} with no partial fields.
The module never chooses a grid, discretization, Fourier convention, base,
derivative, circulation, boundary value, fit, closure, isotropization, ridge,
pseudoinverse or density clamp; it never drops the induced feedback.

NOT done here: no solve; no boundary realization (boundary rows are caller
callbacks evaluated SEPARATELY by evaluate_boundary_rows and never merged into
the bulk residual); no resonance treatment; no neutral-mode/circulation fixing;
no metric-dependent source-measure corrections; not a stationary state; not an
observation-space prediction.
"""
import math
import types
from collections.abc import Mapping

import numpy as np

MODULE_TAG = 'ddo_noncircular_displacement_action_c2v001'
FORCING_CONVENTION = ('r0=projected_base_residual;'
                      'dPhi_total=angular_forcing+induced_feedback')
LAPSE_WEAK = 'weak_field_delta_n'
LAPSE_EXACT = 'exact_ln_N_first_variation'
BASE_DERIV_CALLBACKS = 'caller_derivative_callbacks'
BASE_DERIV_SUPPLIED = 'supplied'
SUPPLIED_BASE_DERIVATIVE_KEYS = ('rho0_phi', 'K0_R', 'K0_phi', 'K0_z',
                                 'P0_R', 'P0_phi', 'P0_z',
                                 'Omega_R', 'Omega_phi', 'Omega_z')
FORCING_PARTITION_KEYS = ('convention', 'r0_content',
                          'r0_includes_induced_feedback',
                          'angular_forcing_excludes_m0_projection',
                          'angular_forcing_includes_induced_feedback',
                          'r0_provenance', 'angular_forcing_provenance')
NOT_DONE = (
    'no solve or inversion of the action',
    'no boundary realization; boundary rows only via evaluate_boundary_rows',
    'no resonance treatment, ridge, pseudoinverse or mode deletion',
    'no neutral-mode, circulation or annular-mass constraint fixing',
    'no equilibrium base construction; base and r0 are caller-supplied',
    'no metric-dependent quadrature/source-measure corrections (spec s4)',
    'no Fourier transform or kernel solve; the response callback owns both',
    'not a stationary state; no corrected velocities or observation rows',
)


class _Reject(Exception):
    def __init__(self, stage, reason):
        Exception.__init__(self, reason)
        self.stage = stage
        self.reason = reason


def _fail(stage, reason):
    return {'ok': False, 'module': MODULE_TAG, 'stage': stage,
            'reason': reason}


def _readonly(a):
    out = np.array(a, dtype=np.float64, copy=True)
    out.flags.writeable = False
    return out


def _real_array(stage, name, value):
    if isinstance(value, (bool, np.bool_)):
        raise _Reject(stage, name + ': boolean is not a real array')
    try:
        arr = np.asarray(value)
    except Exception as exc:
        raise _Reject(stage, name + ': not array-like (%s)' % type(exc).__name__)
    if arr.dtype.kind not in 'fiu' or (arr.dtype.kind == 'f' and arr.dtype.itemsize > 8):
        raise _Reject(stage, name + ': real float64-representable dtype required, got %s' % arr.dtype)
    arr = arr.astype(np.float64)
    if not np.all(np.isfinite(arr)):
        raise _Reject(stage, name + ': nonfinite values')
    return arr


def _grid_array(name, value, grid_shape):
    arr = _real_array('input_validation', name, value)
    try:
        ok = np.broadcast_shapes(arr.shape, grid_shape) == grid_shape
    except ValueError:
        ok = False
    if not ok:
        raise _Reject('input_validation',
                      '%s: shape %s not broadcast-compatible to grid_shape %s'
                      % (name, arr.shape, grid_shape))
    return _readonly(np.broadcast_to(arr, grid_shape))


def _scalar(name, value, positive):
    if isinstance(value, (bool, np.bool_)) or not isinstance(
            value, (int, float, np.integer, np.floating)):
        raise _Reject('input_validation', name + ': real scalar required')
    v = float(value)
    if not math.isfinite(v):
        raise _Reject('input_validation', name + ': finite value required')
    if positive and not v > 0:
        raise _Reject('input_validation', name + ': strictly positive value required')
    if not positive and v < 0:
        raise _Reject('input_validation', name + ': nonnegative value required')
    return v


def _text(name, value):
    if not isinstance(value, str) or not value.strip():
        raise _Reject('input_validation', name + ': nonempty string required')
    return value


def _triple(name, value, grid_shape):
    if not isinstance(value, tuple) or len(value) != 3:
        raise _Reject('input_validation',
                      name + ': tuple of exactly three components (R, phi, z) required')
    return tuple(_grid_array('%s[%s]' % (name, c), v, grid_shape)
                 for c, v in zip(('R', 'phi', 'z'), value))


def _check_partition(decl):
    stage = 'forcing_partition'
    if not isinstance(decl, Mapping):
        raise _Reject(stage, 'forcing_partition: mapping required')
    keys = set(decl.keys())
    if keys != set(FORCING_PARTITION_KEYS):
        raise _Reject(stage, 'forcing_partition: exact keys %s required; missing %s, unknown %s'
                      % (sorted(FORCING_PARTITION_KEYS),
                         sorted(set(FORCING_PARTITION_KEYS) - keys),
                         sorted(str(k) for k in keys - set(FORCING_PARTITION_KEYS))))
    for k in ('r0_includes_induced_feedback', 'angular_forcing_excludes_m0_projection',
              'angular_forcing_includes_induced_feedback'):
        if type(decl[k]) is not bool:
            raise _Reject(stage, 'forcing_partition[%s]: explicit bool required' % k)
    for k in ('r0_provenance', 'angular_forcing_provenance'):
        if not isinstance(decl[k], str) or not decl[k].strip():
            raise _Reject(stage, 'forcing_partition[%s]: nonempty provenance required' % k)
    if decl['r0_content'] == 'full_saved_field_angular_force':
        raise _Reject(stage, 'DOUBLE COUNT: r0 declared as full saved-field angular force while '
                      'dPhi_total always contains the caller angular forcing under the fixed '
                      'convention ' + FORCING_CONVENTION)
    if decl['r0_content'] != 'projected_base_residual':
        raise _Reject(stage, "forcing_partition[r0_content]: must be 'projected_base_residual'")
    if decl['convention'] != FORCING_CONVENTION:
        raise _Reject(stage, 'forcing_partition[convention]: only the fixed 0427 convention %r '
                      'is accepted' % FORCING_CONVENTION)
    if decl['r0_includes_induced_feedback']:
        raise _Reject(stage, 'DOUBLE COUNT: r0 declared to include induced feedback, which this '
                      'action adds from the response callback')
    if decl['angular_forcing_includes_induced_feedback']:
        raise _Reject(stage, 'DOUBLE COUNT: angular forcing declared to include induced feedback, '
                      'which this action adds from the response callback')
    if not decl['angular_forcing_excludes_m0_projection']:
        raise _Reject(stage, 'DOUBLE COUNT: angular forcing must exclude the m=0 projected base '
                      'potential already balanced in the projected base and its residual r0')
    return dict((k, decl[k]) for k in FORCING_PARTITION_KEYS)


def evaluate_bulk_action(*, grid_shape, R, phi, z, rho0, K0, P0, Omega, gamma,
                         xi, partial_R, partial_phi, partial_z,
                         derivative_rule_description, base_derivative_mode,
                         base_derivatives, base_axisymmetry_rtol,
                         polytrope_consistency_rtol, c_light, unit_system,
                         induced_response, lapse_variation_form,
                         angular_forcing_dPhi, base_residual_r0,
                         forcing_partition):
    """Bulk linear Euler action of displacement xi; see module docstring.

    Returns {'ok': True, ...} or a fail-closed {'ok': False, stage, reason}.
    All arrays are read-only float64 of exactly grid_shape. The response
    callback's full output is retained unmodified as 'induced_response_full'.
    """
    caller_err = np.geterr()
    try:
        with np.errstate(all='ignore'):
            return _bulk(caller_err=caller_err, grid_shape=grid_shape, R=R, phi=phi, z=z,
                         rho0=rho0, K0=K0, P0=P0, Omega=Omega, gamma=gamma, xi=xi,
                         partial_R=partial_R, partial_phi=partial_phi, partial_z=partial_z,
                         derivative_rule_description=derivative_rule_description,
                         base_derivative_mode=base_derivative_mode,
                         base_derivatives=base_derivatives,
                         base_axisymmetry_rtol=base_axisymmetry_rtol,
                         polytrope_consistency_rtol=polytrope_consistency_rtol,
                         c_light=c_light, unit_system=unit_system,
                         induced_response=induced_response,
                         lapse_variation_form=lapse_variation_form,
                         angular_forcing_dPhi=angular_forcing_dPhi,
                         base_residual_r0=base_residual_r0,
                         forcing_partition=forcing_partition)
    except _Reject as rej:
        return _fail(rej.stage, rej.reason)
    except Exception as exc:  # fail closed on anything unforeseen
        return _fail('internal', '%s: %s' % (type(exc).__name__, exc))


def _bulk(*, caller_err, grid_shape, R, phi, z, rho0, K0, P0, Omega, gamma, xi,
          partial_R, partial_phi, partial_z, derivative_rule_description,
          base_derivative_mode, base_derivatives, base_axisymmetry_rtol,
          polytrope_consistency_rtol, c_light, unit_system, induced_response,
          lapse_variation_form, angular_forcing_dPhi, base_residual_r0,
          forcing_partition):
    # ---------------- static validation (no callback is called before this passes)
    if (not isinstance(grid_shape, tuple) or len(grid_shape) == 0
            or any(isinstance(n, (bool, np.bool_)) or not isinstance(n, (int, np.integer))
                   or n < 1 for n in grid_shape)):
        raise _Reject('input_validation', 'grid_shape: nonempty tuple of positive ints required')
    gs = tuple(int(n) for n in grid_shape)
    _text('derivative_rule_description', derivative_rule_description)
    _text('unit_system', unit_system)
    for name, op in (('partial_R', partial_R), ('partial_phi', partial_phi),
                     ('partial_z', partial_z), ('induced_response', induced_response)):
        if not callable(op):
            raise _Reject('input_validation', name + ': callable required')
    Rg = _grid_array('R', R, gs)
    phig = _grid_array('phi', phi, gs)
    zg = _grid_array('z', z, gs)
    rho = _grid_array('rho0', rho0, gs)
    K = _grid_array('K0', K0, gs)
    P = _grid_array('P0', P0, gs)
    W = _grid_array('Omega', Omega, gs)
    gam = _scalar('gamma', gamma, positive=True)
    c = _scalar('c_light', c_light, positive=True)
    ax_rtol = _scalar('base_axisymmetry_rtol', base_axisymmetry_rtol, positive=False)
    pol_rtol = _scalar('polytrope_consistency_rtol', polytrope_consistency_rtol, positive=False)
    if not np.all(Rg > 0):
        raise _Reject('input_validation', 'R: strictly positive radius required everywhere')
    if not np.all(rho > 0):
        raise _Reject('input_validation', 'rho0: strictly positive density required; no clamp')
    if not np.all(P > 0):
        raise _Reject('input_validation', 'P0: strictly positive pressure required; no clamp')
    if not np.all(K > 0):
        raise _Reject('input_validation', 'K0: strictly positive polytropic K required')
    xR, xP, xZ = _triple('xi', xi, gs)
    r0R, r0P, r0Z = _triple('base_residual_r0', base_residual_r0, gs)
    forcing = _grid_array('angular_forcing_dPhi', angular_forcing_dPhi, gs)
    if lapse_variation_form not in (LAPSE_WEAK, LAPSE_EXACT):
        raise _Reject('input_validation', 'lapse_variation_form: %r or %r required'
                      % (LAPSE_WEAK, LAPSE_EXACT))
    partition = _check_partition(forcing_partition)
    if base_derivative_mode == BASE_DERIV_SUPPLIED:
        if not isinstance(base_derivatives, Mapping) or set(base_derivatives.keys()) != set(
                SUPPLIED_BASE_DERIVATIVE_KEYS):
            raise _Reject('input_validation', 'base_derivatives: mapping with exact keys %s '
                          'required in supplied mode' % (SUPPLIED_BASE_DERIVATIVE_KEYS,))
        bd = dict((k, _grid_array('base_derivatives[%s]' % k, base_derivatives[k], gs))
                  for k in SUPPLIED_BASE_DERIVATIVE_KEYS)
    elif base_derivative_mode == BASE_DERIV_CALLBACKS:
        if base_derivatives is not None:
            raise _Reject('input_validation', 'base_derivatives must be None when '
                          'base_derivative_mode is %r (no mixing)' % BASE_DERIV_CALLBACKS)
        bd = None
    else:
        raise _Reject('input_validation', 'base_derivative_mode: %r or %r required'
                      % (BASE_DERIV_CALLBACKS, BASE_DERIV_SUPPLIED))

    # ---------------- base checks (polytrope relation the dP formula relies on)
    pol_mismatch = float(np.max(np.abs(P - K * rho ** gam) / P))
    if not math.isfinite(pol_mismatch) or pol_mismatch > pol_rtol:
        raise _Reject('base_checks', 'P0 != K0 rho0**gamma: max relative mismatch %r exceeds '
                      'polytrope_consistency_rtol %r' % (pol_mismatch, pol_rtol))

    def d(op, opname, field):
        arg = _readonly(field)
        try:
            with np.errstate(**caller_err):
                out = op(arg)
        except Exception as exc:
            raise _Reject('derivative_callback', '%s raised %s: %s'
                          % (opname, type(exc).__name__, exc))
        out = _real_array('derivative_callback', opname + ' output', out)
        if out.shape != gs:
            raise _Reject('derivative_callback', '%s output shape %s != grid_shape %s'
                          % (opname, out.shape, gs))
        return out

    def dR(f):
        return d(partial_R, 'partial_R', f)

    def dphi(f):
        return d(partial_phi, 'partial_phi', f)

    def dz(f):
        return d(partial_z, 'partial_z', f)

    if bd is None:
        bd = {'rho0_phi': dphi(rho), 'K0_R': dR(K), 'K0_phi': dphi(K), 'K0_z': dz(K),
              'P0_R': dR(P), 'P0_phi': dphi(P), 'P0_z': dz(P),
              'Omega_R': dR(W), 'Omega_phi': dphi(W), 'Omega_z': dz(W)}
        bd = dict((k, _readonly(v)) for k, v in bd.items())

    # Base axisymmetry == base stationary continuity/entropy for v0 = R Omega e_phi.
    ax_ratio = {}
    for fname, f, fphi in (('rho0', rho, bd['rho0_phi']), ('K0', K, bd['K0_phi']),
                           ('P0', P, bd['P0_phi']), ('Omega', W, bd['Omega_phi'])):
        num = float(np.max(np.abs(fphi)))
        den = float(np.max(np.abs(f)))
        if num == 0.0:
            ratio = 0.0
        elif den == 0.0:
            ratio = math.inf
        else:
            ratio = num / den
        ax_ratio[fname] = ratio
        if not ratio <= ax_rtol:
            raise _Reject('base_checks', 'base not axisymmetric within base_axisymmetry_rtol: '
                          'max|d_phi %s|/max|%s| = %r > %r; spec s3 equations assume an '
                          'axisymmetric equilibrated base' % (fname, fname, ratio, ax_rtol))
    base_continuity = bd['rho0_phi'] * W + rho * bd['Omega_phi']   # (1/R) d_phi(rho0 R Omega)
    base_entropy = W * bd['K0_phi']                                  # v0 . grad K0

    # ---------------- displacement -> fluid perturbation (spec s3)
    cs2 = gam * P / rho
    flux_R = Rg * rho * xR
    flux_phi = rho * xP
    flux_z = rho * xZ
    div = dR(flux_R) / Rg + dphi(flux_phi) / Rg + dz(flux_z)
    drho = -div
    dK = -(xR * bd['K0_R'] + xP * bd['K0_phi'] / Rg + xZ * bd['K0_z'])
    dP = cs2 * drho + rho ** gam * dK
    xR_phi = dphi(xR)
    xP_phi = dphi(xP)
    xZ_phi = dphi(xZ)
    dvR = W * xR_phi
    dvZ = W * xZ_phi
    dvP = W * xP_phi - Rg * (bd['Omega_R'] * xR + bd['Omega_z'] * xZ)
    lagrangian_dP = dP + xR * bd['P0_R'] + xP * bd['P0_phi'] / Rg + xZ * bd['P0_z']
    for name, arr in (('drho', drho), ('dK', dK), ('dP', dP), ('dv_R', dvR),
                      ('dv_phi', dvP), ('dv_z', dvZ), ('lagrangian_dP', lagrangian_dP)):
        if not np.all(np.isfinite(arr)):
            raise _Reject('perturbation', name + ': nonfinite')

    # ---------------- source feedback (spec s4): exactly one response call
    delta_f_n = -(c * c) * drho
    if not np.all(np.isfinite(delta_f_n)):
        raise _Reject('source_feedback', 'delta_f_n: nonfinite')
    passed = _readonly(delta_f_n)
    try:
        with np.errstate(**caller_err):
            response = induced_response(delta_f_n=passed)
    except Exception as exc:
        raise _Reject('source_feedback', 'induced_response raised %s: %s'
                      % (type(exc).__name__, exc))
    if not np.array_equal(passed, delta_f_n):
        raise _Reject('source_feedback', 'induced_response mutated its delta_f_n input')
    if not isinstance(response, Mapping):
        raise _Reject('source_feedback', 'induced_response must return a mapping')
    if 'native_response' not in response or response['native_response'] is None:
        raise _Reject('source_feedback', "induced_response output lacks 'native_response' "
                      '(complete native response must be returned)')
    lapse = response.get('lapse_component')
    if not isinstance(lapse, Mapping):
        raise _Reject('source_feedback', "induced_response output lacks mapping 'lapse_component'")
    if lapse.get('form') != lapse_variation_form:
        raise _Reject('source_feedback', 'lapse_component form %r != declared '
                      'lapse_variation_form %r; no silent choice' % (lapse.get('form'),
                                                                     lapse_variation_form))

    def lapse_array(key):
        arr = _real_array('source_feedback', 'lapse_component[%s]' % key, lapse[key])
        if arr.shape != gs:
            raise _Reject('source_feedback', 'lapse_component[%s] shape %s != grid_shape %s'
                          % (key, arr.shape, gs))
        return arr

    if lapse_variation_form == LAPSE_WEAK:
        if set(lapse.keys()) != {'form', 'delta_n'}:
            raise _Reject('source_feedback', "weak-field lapse_component keys must be exactly "
                          "{'form','delta_n'}")
        dn = lapse_array('delta_n')
        dPhi_ind = (c * c) * dn                      # weak field: dPhi = c^2 delta n
        lapse_used = {'delta_n': _readonly(dn)}
    else:
        if set(lapse.keys()) != {'form', 'delta_N', 'N0'}:
            raise _Reject('source_feedback', "exact lapse_component keys must be exactly "
                          "{'form','delta_N','N0'}")
        dN = lapse_array('delta_N')
        N0 = lapse_array('N0')
        if not np.all(N0 > 0):
            raise _Reject('source_feedback', 'N0: strictly positive lapse required')
        dPhi_ind = (c * c) * dN / N0                 # exact first variation of c^2 ln N
        lapse_used = {'delta_N': _readonly(dN), 'N0': _readonly(N0)}
    dPhi = forcing + dPhi_ind                        # each contribution exactly once
    if not np.all(np.isfinite(dPhi)):
        raise _Reject('source_feedback', 'dPhi_total: nonfinite')

    # ---------------- stationary linearized Euler residuals (spec s3)
    dPhi_R, dPhi_phi, dPhi_z = dR(dPhi), dphi(dPhi), dz(dPhi)
    dP_R, dP_phi, dP_z = dR(dP), dphi(dP), dz(dP)
    dvR_phi, dvP_phi, dvZ_phi = dphi(dvR), dphi(dvP), dphi(dvZ)
    terms_R = {'Omega_dphi_dv_R': W * dvR_phi, 'minus_2Omega_dv_phi': -2.0 * W * dvP,
               'dR_dPhi': dPhi_R, 'dR_dP_over_rho0': dP_R / rho,
               'minus_drho_P0R_over_rho0sq': -drho * bd['P0_R'] / rho ** 2,
               'r0_R': r0R}
    terms_phi = {'Omega_dphi_dv_phi': W * dvP_phi,
                 'two_Omega_plus_R_OmegaR_dv_R': (2.0 * W + Rg * bd['Omega_R']) * dvR,
                 'R_Omegaz_dv_z': Rg * bd['Omega_z'] * dvZ,
                 'dphi_dPhi_over_R': dPhi_phi / Rg,
                 'dphi_dP_over_rho0_R': dP_phi / (rho * Rg), 'r0_phi': r0P}
    terms_z = {'Omega_dphi_dv_z': W * dvZ_phi, 'dz_dPhi': dPhi_z,
               'dz_dP_over_rho0': dP_z / rho,
               'minus_drho_P0z_over_rho0sq': -drho * bd['P0_z'] / rho ** 2, 'r0_z': r0Z}
    order_R = ('Omega_dphi_dv_R', 'minus_2Omega_dv_phi', 'dR_dPhi', 'dR_dP_over_rho0',
               'minus_drho_P0R_over_rho0sq', 'r0_R')
    order_phi = ('Omega_dphi_dv_phi', 'two_Omega_plus_R_OmegaR_dv_R', 'R_Omegaz_dv_z',
                 'dphi_dPhi_over_R', 'dphi_dP_over_rho0_R', 'r0_phi')
    order_z = ('Omega_dphi_dv_z', 'dz_dPhi', 'dz_dP_over_rho0',
               'minus_drho_P0z_over_rho0sq', 'r0_z')
    residual = {}
    for comp, terms, order in (('R', terms_R, order_R), ('phi', terms_phi, order_phi),
                               ('z', terms_z, order_z)):
        total = np.zeros(gs)
        for key in order:
            total = total + terms[key]
        if not np.all(np.isfinite(total)):
            raise _Reject('euler_residual', 'residual component %s: nonfinite' % comp)
        residual[comp] = _readonly(total)

    # ---------------- diagnostics only (analytically zero about an axisymmetric base)
    lin_cont = (dR(Rg * rho * dvR) / Rg + dphi(rho * dvP + drho * Rg * W) / Rg
                + dz(rho * dvZ))
    lin_ent = W * dphi(dK) + dvR * bd['K0_R'] + dvP * bd['K0_phi'] / Rg + dvZ * bd['K0_z']

    ro = _readonly
    base_state = {'R': Rg, 'phi': phig, 'z': zg, 'rho0': rho, 'K0': K, 'P0': P, 'Omega': W,
                  'gamma': gam, 'c_light': c}
    base_state.update(bd)
    boundary_state = dict(base_state)
    boundary_state.update({'xi_R': xR, 'xi_phi': xP, 'xi_z': xZ, 'drho': ro(drho),
                           'dK': ro(dK), 'dP': ro(dP), 'cs2': ro(cs2), 'dv_R': ro(dvR),
                           'dv_phi': ro(dvP), 'dv_z': ro(dvZ),
                           'lagrangian_dP': ro(lagrangian_dP), 'dPhi_total': ro(dPhi),
                           'partial_R': partial_R, 'partial_phi': partial_phi,
                           'partial_z': partial_z, 'grid_shape': gs,
                           'unit_system': unit_system,
                           'derivative_rule_description': derivative_rule_description})
    return {
        'ok': True, 'module': MODULE_TAG, 'stage': 'bulk_action_evaluated', 'grid_shape': gs,
        'perturbations': {'drho': ro(drho), 'dK': ro(dK), 'dP': ro(dP), 'cs2': ro(cs2),
                          'dv_R': ro(dvR), 'dv_phi': ro(dvP), 'dv_z': ro(dvZ),
                          'lagrangian_dP': ro(lagrangian_dP)},
        'source_feedback': {'delta_f_n': ro(delta_f_n), 'response_call_count': 1,
                            'lapse_variation_form': lapse_variation_form,
                            'lapse_used': lapse_used, 'dPhi_forcing': forcing,
                            'dPhi_induced': ro(dPhi_ind), 'dPhi_total': ro(dPhi)},
        'induced_response_full': response,
        'euler_residual': residual,
        'euler_terms': {'R': dict((k, ro(v)) for k, v in terms_R.items()),
                        'phi': dict((k, ro(v)) for k, v in terms_phi.items()),
                        'z': dict((k, ro(v)) for k, v in terms_z.items())},
        'base_checks': {'polytrope_max_relative_mismatch': pol_mismatch,
                        'axisymmetry_max_ratio': ax_ratio,
                        'base_continuity_residual': ro(base_continuity),
                        'base_entropy_residual': ro(base_entropy),
                        'base_derivative_mode': base_derivative_mode,
                        'base_derivatives': bd},
        'identity_diagnostics': {
            'linearized_continuity': ro(lin_cont), 'linearized_entropy': ro(lin_ent),
            'scope': 'div(rho0 dv + drho v0) and v0.grad dK + dv.grad K0 via the caller '
                     'callbacks; analytically zero about an axisymmetric base; nonzero values '
                     'measure base residual or derivative-rule (non)commutation, not gated'},
        'forcing_partition': partition,
        'conventions': {
            'components': 'physical orthonormal cylindrical (R, phi, z); d_phi per radian',
            'divergence': '(1/R) d_R(R rho0 xi_R) + (1/R) d_phi(rho0 xi_phi) + d_z(rho0 xi_z)',
            'source_sign': 'delta_f_n = -c_light**2 * drho (leading mass-source approximation)',
            'potential': ('dPhi_total = angular_forcing_dPhi + c**2*delta_n (weak field)'
                          if lapse_variation_form == LAPSE_WEAK else
                          'dPhi_total = angular_forcing_dPhi + c**2*delta_N/N0 (exact ln N)'),
            'residual_sign': 'residual = LHS - RHS of spec s3; zero for a solution',
            'forcing_convention': FORCING_CONVENTION,
            'unit_system': unit_system,
            'derivative_rule_description': derivative_rule_description},
        'not_done': NOT_DONE,
        'boundary_rows': 'NOT_EVALUATED: use evaluate_boundary_rows; never merged into '
                         'euler_residual',
        'boundary_state': types.MappingProxyType(boundary_state),
    }


def evaluate_boundary_rows(*, bulk_result, boundary_row_callbacks):
    """Evaluate caller-supplied boundary rows SEPARATELY from the bulk action.

    boundary_row_callbacks: nonempty mapping name -> callable(*, fields) returning a
    real finite array (ndim >= 1, size >= 1). `fields` is the read-only
    bulk_result['boundary_state'] mapping. Rows are returned unweighted and are
    never added to the bulk Euler residual. Fail-closed dict on any failure.
    """
    caller_err = np.geterr()
    try:
        with np.errstate(all='ignore'):
            if (not isinstance(bulk_result, Mapping) or bulk_result.get('ok') is not True
                    or bulk_result.get('module') != MODULE_TAG
                    or not isinstance(bulk_result.get('boundary_state'),
                                      types.MappingProxyType)):
                raise _Reject('input_validation', 'bulk_result: successful %s bulk result '
                              'required' % MODULE_TAG)
            if not isinstance(boundary_row_callbacks, Mapping) or len(boundary_row_callbacks) == 0:
                raise _Reject('input_validation', 'boundary_row_callbacks: nonempty mapping '
                              'required; boundary realization is caller-owned')
            for name, cb in boundary_row_callbacks.items():
                if not isinstance(name, str) or not name.strip() or not callable(cb):
                    raise _Reject('input_validation', 'boundary_row_callbacks: nonempty str '
                                  'names mapped to callables required')
            fields = bulk_result['boundary_state']
            rows = {}
            for name, cb in boundary_row_callbacks.items():
                try:
                    with np.errstate(**caller_err):
                        out = cb(fields=fields)
                except Exception as exc:
                    raise _Reject('boundary_callback', '%s raised %s: %s'
                                  % (name, type(exc).__name__, exc))
                arr = _real_array('boundary_callback', 'boundary row %s' % name, out)
                if arr.ndim < 1 or arr.size < 1:
                    raise _Reject('boundary_callback', 'boundary row %s: nonempty array with '
                                  'ndim >= 1 required' % name)
                rows[name] = _readonly(arr)
            return {'ok': True, 'module': MODULE_TAG, 'stage': 'boundary_rows_evaluated',
                    'boundary_rows': rows,
                    'call_counts': dict((k, 1) for k in rows),
                    'scope': 'caller-realized boundary rows; unweighted; not merged into '
                             'the bulk residual; no boundary values invented'}
    except _Reject as rej:
        return _fail(rej.stage, rej.reason)
    except Exception as exc:
        return _fail('internal', '%s: %s' % (type(exc).__name__, exc))
