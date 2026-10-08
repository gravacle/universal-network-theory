"""Inert state maps for a prospective consistent-inertia two-current solver.

No integration, step choice, EOS, gravity, source fitting or numerical tests
run here. The caller must authenticate the exact kernel below before importing
it and pass that module explicitly. Checking INERTIA_METHOD is an API guard,
not a replacement for file custody. There is no import-time numerical work,
file IO, fallback, clipping, mesh mask, quadrature or input-array mutation.

State convention: [A, xb, pb, xh, ph, ten work ledgers], with only free faces
stored. Species have the same number of fixed, positive mass cells. This is
the old state layout; its momentum slots now obey p=A M(x) v, not lumping.
"""
import numpy as np


EXPECTED_KERNEL_SHA256 = '78765ef0e2d29c044642b1d944682a81ff5d48b22de9d0cb16b7bc47b9c7e11a'
EXPECTED_INERTIA_METHOD = 'closed_form_rational_polynomial_binary64_v001'
DP_RTOL = 2e-11
DP_ATOL = 2e-13
SCOPE_FLAGS = dict(trajectory_qualified=False, certified_cfl=False,
                   certified_no_crossing=False, spatial_continuum_qualified=False,
                   physical_state_formation=False, physical_source_qualified=False,
                   observational_fit=False)


def _vector(value, name, size=None):
    value = np.asarray(value, dtype=float)
    if value.ndim != 1 or (size is not None and value.size != size):
        raise ValueError(name + ' has the wrong vector shape')
    if not np.all(np.isfinite(value)):
        raise ValueError(name + ' contains nonfinite entries')
    return value


def _scalar(value, name, positive=False):
    if not np.isscalar(value) or not np.isfinite(value):
        raise ValueError(name + ' must be a finite scalar')
    if positive and value <= 0.0:
        raise ValueError(name + ' must be positive')
    return float(value)


def _finite(value, name):
    if not np.all(np.isfinite(value)):
        raise FloatingPointError(name + ' became nonfinite')
    return value


def _kernel(kernel):
    if getattr(kernel, 'INERTIA_METHOD', None) != EXPECTED_INERTIA_METHOD:
        raise ValueError('Wrong exact-inertia API; source authentication is also required')


def mass_matrix_directional_derivative(faces, masses, free_face_direction):
    """Return dM[x][direction] as diagonal/off-diagonal, without differencing.

    The constrained origin has direction zero. Each non-origin shell has
    M_shell=m F(q), q=L/R, so dM_shell=m F'(q)(dL-q*dR)/R. The origin's
    single free entry is 3m/5 and has exactly zero directional derivative.
    """
    x = _vector(faces, 'faces')
    if x.size < 2 or x[0] != 0.0 or not np.all(x[1:] > x[:-1]):
        raise ValueError('Faces must start at zero and be strictly increasing')
    m = _vector(masses, 'masses', x.size-1)
    if not np.all(m > 0.0):
        raise ValueError('All fixed shell masses must be positive')
    direction = _vector(free_face_direction, 'free_face_direction', m.size)
    diagonal = np.zeros(m.size)
    off_diagonal = np.zeros(m.size-1)
    if m.size == 1:
        return diagonal, off_diagonal
    with np.errstate(over='raise', invalid='raise', divide='raise'):
        q = x[1:-1]/x[2:]
        q2 = q*q
        s = 1.0+q+q2
        common = (9.0/5.0)*m[1:]/(s*s*s*s)
        dq = (direction[:-1]-q*direction[1:])/x[2:]
        ll = common*q2*(5.0+8.0*q+2.0*q2)*dq
        rr = -common*q2*(2.0+8.0*q+5.0*q2)*dq
        lr = common*q*(1.0-q)*(1.0+5.0*q+5.0*q2+q*q2)*dq
        diagonal[:-1] += ll
        diagonal[1:] += rr
        off_diagonal[:] = lr
    return (_finite(diagonal, 'directional inertia diagonal'),
            _finite(off_diagonal, 'directional inertia off-diagonal'))


def canonical_species_rhs(kernel, faces, masses, momentum, A, physical_kick):
    """Map an already assembled physical canonical kick to xdot and pdot.

    Gravity's input is -grad(W0)/A; hard pressure's input is its full face
    kick including outer traction. Neither is an acceleration. No Hubble
    drag is added to pdot: it enters the p=A M v conversion instead.
    """
    _kernel(kernel)
    A = _scalar(A, 'A', positive=True)
    state = kernel.canonical_kinematics(faces, masses, momentum, A)
    kick = _vector(physical_kick, 'physical_kick', state['peculiar_velocity'].size)
    with np.errstate(over='raise', invalid='raise'):
        pdot = state['geometric_force']+kick
    return dict(kinematics=state,
                coordinate_velocity=state['coordinate_velocity'],
                canonical_momentum_derivative=_finite(pdot, 'canonical momentum derivative'))


def peculiar_acceleration_decomposition(kernel, faces, masses, momentum, A,
                                        Ht, physical_kicks):
    """Return force responses separately from geometry and Hubble terms.

    physical_kicks maps descriptive names to canonical force vectors. The
    complete peculiar acceleration is M^-1(sum f+g)/A - M^-1(Mdot v)-Ht*v.
    It is not the isolated gravity response, nor g divided by a lumped mass.
    Mdot is evaluated along xdot=v/A, at fixed shell masses.
    """
    _kernel(kernel)
    A = _scalar(A, 'A', positive=True)
    Ht = _scalar(Ht, 'Ht')
    if not isinstance(physical_kicks, dict):
        raise ValueError('physical_kicks must be a dictionary of named canonical kicks')
    state = kernel.canonical_kinematics(faces, masses, momentum, A)
    diagonal, off = state['diagonal'], state['off_diagonal']
    velocity = state['peculiar_velocity']
    physical = {}
    total_kick = np.zeros(velocity.size)
    for name, raw in physical_kicks.items():
        if not isinstance(name, str) or not name:
            raise ValueError('Each canonical kick needs a nonempty string label')
        kick = _vector(raw, 'physical kick '+name, velocity.size)
        with np.errstate(over='raise', invalid='raise', divide='raise'):
            physical[name] = kernel.solve_spd_tridiagonal(diagonal, off, kick)/A
            total_kick += kick
        _finite(physical[name], 'physical acceleration '+name)
    mdot_diag, mdot_off = mass_matrix_directional_derivative(
        faces, masses, state['coordinate_velocity'])
    mdot_v = kernel.tridiagonal_matvec(mdot_diag, mdot_off, velocity)
    with np.errstate(over='raise', invalid='raise', divide='raise'):
        geometric_kick_response = kernel.solve_spd_tridiagonal(
            diagonal, off, state['geometric_force'])/A
        inertia_motion = -kernel.solve_spd_tridiagonal(diagonal, off, mdot_v)
        hubble = -Ht*velocity
        total = kernel.solve_spd_tridiagonal(
            diagonal, off, total_kick+state['geometric_force'])/A+inertia_motion+hubble
    for name, value in [('geometric kick response', geometric_kick_response),
                        ('inertia motion', inertia_motion), ('Hubble term', hubble),
                        ('full peculiar acceleration', total)]:
        _finite(value, name)
    return dict(physical_force_responses=physical,
                geometric_kick_response=geometric_kick_response,
                inertia_motion_response=inertia_motion,
                hubble_response=hubble, full_peculiar_acceleration=total,
                inertia_time_derivative_diagonal=mdot_diag,
                inertia_time_derivative_off_diagonal=mdot_off)


def physical_error_chart(kernel, state_vector, masses):
    """Nonlinear chart [A,xb,vb,xh,vh,scaled ledgers] of the old state layout.

    Every call uses that vector's own A and both meshes in M(x). Only the
    last three ledgers are divided by total hard mass, as in the old protocol.
    This chart validates kinematics, not EOS/action or prospective run guards.
    The caller must apply those guards to every evaluated stage and endpoint.
    """
    _kernel(kernel)
    if len(masses) != 2:
        raise ValueError('Exactly two fixed species mass vectors are required')
    mb = _vector(masses[0], 'ordinary masses')
    mh = _vector(masses[1], 'hard masses', mb.size)
    if mb.size == 0 or not np.all(mb > 0.0) or not np.all(mh > 0.0):
        raise ValueError('Both species need positive fixed cell masses')
    n = mb.size
    y = _vector(state_vector, 'state_vector', 1+4*n+10)
    A = _scalar(y[0], 'A', positive=True)
    chart = y.copy()
    for offset, mass in [(1, mb), (1+2*n, mh)]:
        faces = np.r_[0.0, y[offset:offset+n]]
        momentum = y[offset+n:offset+2*n]
        # Use the kernel's exact matrix and solve, without requiring geometric
        # force assembly merely to evaluate an error norm.
        diagonal, off = kernel.mass_matrix(faces, mass)
        with np.errstate(over='raise', invalid='raise', divide='raise'):
            chart[offset+n:offset+2*n] = kernel.solve_spd_tridiagonal(
                diagonal, off, momentum)/A
    with np.errstate(over='raise', invalid='raise', divide='raise'):
        hard_total = _scalar(np.sum(mh), 'total hard mass', positive=True)
        chart[1+4*n+7:] /= hard_total
    return _finite(chart, 'physical error chart')


def embedded_error_norm(kernel, current, high_order, low_order, masses):
    """Use complete high/low nonlinear charts and the unchanged DOPRI tolerances.

    low_order must be the actual embedded solution, not a linearly scaled
    momentum error. Invalid kinematics raises; the caller retains the failed
    attempted state rather than silently converting it to an accuracy retry.
    """
    old = physical_error_chart(kernel, current, masses)
    high = physical_error_chart(kernel, high_order, masses)
    low = physical_error_chart(kernel, low_order, masses)
    with np.errstate(over='raise', invalid='raise', divide='raise'):
        denominator = DP_ATOL+DP_RTOL*np.maximum(np.abs(old), np.abs(high))
        normalized = np.abs(high-low)/denominator
    return float(np.max(_finite(normalized, 'embedded physical state error')))
