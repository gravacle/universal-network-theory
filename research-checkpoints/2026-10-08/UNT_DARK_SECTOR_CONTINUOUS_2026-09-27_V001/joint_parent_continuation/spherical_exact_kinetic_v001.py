"""Closed-form consistent inertia for fixed-mass spherical shells.

This separately versioned kernel evaluates exact finite-shell integrals as
rational polynomials in binary64; floating-point results still require tests.
It neither repairs the old quadrature evidence nor qualifies a trajectory.

Faces include the constrained origin and N strictly ordered free radii. Shell
masses are fixed and positive. p=A M v=A^2 M xdot, K=v^T M v/2, and the
kinetic contribution to pdot is +v^T (partial_x M) v/2. Pressure, gravity,
expansion work, boundary traction and evolution are not provided here.

There is no quadrature, order knob, clipping, regularization, mesh mask,
fallback, file IO, import-time numerical work or input-array mutation.
"""
import numpy as np


INERTIA_METHOD = 'closed_form_rational_polynomial_binary64_v001'


def _vector(value, name, size=None):
    out = np.asarray(value, dtype=float)
    if out.ndim != 1 or (size is not None and out.size != size):
        raise ValueError(name + ' has the wrong vector shape')
    if not np.all(np.isfinite(out)):
        raise ValueError(name + ' contains nonfinite entries')
    return out


def _mesh(faces, masses=None):
    x = _vector(faces, 'faces')
    if x.size < 2 or x[0] != 0.0 or not np.all(x[1:] > x[:-1]):
        raise ValueError('Faces must start at zero and be strictly increasing')
    if masses is None:
        return x
    m = _vector(masses, 'masses', x.size-1)
    if not np.all(m > 0.0):
        raise ValueError('All fixed shell masses must be positive')
    return x, m


def _finite(value, name):
    if not np.all(np.isfinite(value)):
        raise FloatingPointError(name + ' became nonfinite')
    return value


def _tridiagonal(diagonal, off_diagonal):
    diagonal = _vector(diagonal, 'diagonal')
    if diagonal.size == 0:
        raise ValueError('The free-face matrix cannot be empty')
    off_diagonal = _vector(off_diagonal, 'off_diagonal', diagonal.size-1)
    return diagonal, off_diagonal


def shell_volumes(faces):
    """Cancellation-safe positive volumes; same convention as the old kernel."""
    x = _mesh(faces)
    left, right = x[:-1], x[1:]
    ratio = left/right
    with np.errstate(over='raise', invalid='raise', divide='raise'):
        volumes = ((4.0*np.pi/3.0)*(right-left)*right*right
                   * (1.0+ratio+ratio*ratio))
    _finite(volumes, 'shell volumes')
    if not np.all(volumes > 0.0):
        raise FloatingPointError('A factored shell volume is nonpositive')
    return volumes


def _assemble(faces, masses, peculiar_velocity=None):
    """Exact integral formulas, evaluated without a quadrature parameter."""
    x, m = _mesh(faces, masses)
    n = m.size
    velocity = (None if peculiar_velocity is None else
                _vector(peculiar_velocity, 'peculiar_velocity', n))
    diagonal = np.zeros(n)
    off_diagonal = np.zeros(n-1)
    force = None if velocity is None else np.zeros(n)
    diagonal[0] = (3.0/5.0)*m[0]
    if diagonal[0] <= 0.0:
        raise FloatingPointError('The origin inertia underflowed to zero')
    if n == 1:
        return diagonal, off_diagonal, force

    left, right = x[1:-1], x[2:]
    with np.errstate(over='raise', invalid='raise', divide='raise'):
        q = left/right
        q2, q3 = q*q, q*q*q
        s = 1.0+q+q2
        denominator = s*s*s
        cell_mass = m[1:]
        ll = (3.0/5.0)*cell_mass*q3*(5.0+6.0*q+3.0*q2+q3)/denominator
        rr = (3.0/5.0)*cell_mass*(1.0+3.0*q+6.0*q2+5.0*q3)/denominator
        lr = (9.0/10.0)*cell_mass*q2*(1.0+3.0*q+q2)/denominator
        diagonal[:-1] += ll
        diagonal[1:] += rr
        off_diagonal[:] = lr
        if velocity is not None:
            vl, vr = velocity[:-1], velocity[1:]
            # Q=v^T F'(q)v, with M_shell=m F(q). The factored form
            # retains the affine null vl=q*vr without subtracting three
            # independent large quadratic contractions.
            contraction = ((9.0/5.0)*q/(denominator*s)*(vl-q*vr)
                           * (q*(5.0+8.0*q+2.0*q2)*vl
                              +(2.0+8.0*q+5.0*q2)*vr))
            g_left = (0.5*cell_mass/right)*contraction
            force[:-1] += g_left
            force[1:] -= q*g_left
    _finite(diagonal, 'inertia diagonal')
    _finite(off_diagonal, 'inertia off-diagonal')
    if force is not None:
        _finite(force, 'geometric force')
    if not np.all(diagonal > 0.0):
        raise FloatingPointError('The computed inertia diagonal is nonpositive')
    return diagonal, off_diagonal, force


def mass_matrix(faces, masses):
    """Return the free-face symmetric tridiagonal matrix, without order knobs."""
    diagonal, off_diagonal, _ = _assemble(faces, masses)
    return diagonal, off_diagonal


def geometric_force(faces, masses, peculiar_velocity):
    """Return the kinetic contribution +v^T(partial_j M)v/2 to pdot."""
    return _assemble(faces, masses, peculiar_velocity)[2]


def mass_matrix_and_geometric_force(faces, masses, peculiar_velocity):
    return _assemble(faces, masses, peculiar_velocity)


def tridiagonal_matvec(diagonal, off_diagonal, vector):
    diagonal, off_diagonal = _tridiagonal(diagonal, off_diagonal)
    vector = _vector(vector, 'vector', diagonal.size)
    with np.errstate(over='raise', invalid='raise'):
        result = diagonal*vector
        result[:-1] += off_diagonal*vector[1:]
        result[1:] += off_diagonal*vector[:-1]
    return _finite(result, 'tridiagonal product')


def solve_spd_tridiagonal(diagonal, off_diagonal, rhs):
    """Same unpivoted LDL equations; nonpositive/nonfinite pivots fail closed."""
    diagonal, off_diagonal = _tridiagonal(diagonal, off_diagonal)
    rhs = _vector(rhs, 'rhs', diagonal.size)
    pivots = diagonal.copy()
    lower = np.empty_like(off_diagonal)
    result = rhs.copy()
    with np.errstate(over='raise', invalid='raise', divide='raise'):
        for i in range(diagonal.size):
            if not np.isfinite(pivots[i]) or pivots[i] <= 0.0:
                raise np.linalg.LinAlgError('Nonpositive/nonfinite LDL pivot')
            if i < off_diagonal.size:
                lower[i] = off_diagonal[i]/pivots[i]
                pivots[i+1] -= lower[i]*off_diagonal[i]
                result[i+1] -= lower[i]*result[i]
        result /= pivots
        for i in range(off_diagonal.size-1, -1, -1):
            result[i] -= lower[i]*result[i+1]
    return _finite(result, 'SPD solve')


def kinetic_energy(diagonal, off_diagonal, peculiar_velocity):
    diagonal, off_diagonal = _tridiagonal(diagonal, off_diagonal)
    velocity = _vector(peculiar_velocity, 'peculiar_velocity', diagonal.size)
    with np.errstate(over='raise', invalid='raise'):
        value = 0.5*np.dot(velocity, tridiagonal_matvec(diagonal, off_diagonal, velocity))
    return float(_finite(value, 'kinetic energy'))


def canonical_kinematics(faces, masses, momentum, A=1.0):
    """Return unchanged canonical equations with the new closed-form M and g."""
    if not np.isscalar(A) or not np.isfinite(A) or A <= 0.0:
        raise ValueError('Scale factor A must be finite and positive')
    diagonal, off_diagonal = mass_matrix(faces, masses)
    inverse_p = solve_spd_tridiagonal(diagonal, off_diagonal, momentum)
    with np.errstate(over='raise', invalid='raise', divide='raise'):
        velocity = inverse_p/A
        coordinate_velocity = velocity/A
    _finite(velocity, 'peculiar velocity')
    _finite(coordinate_velocity, 'coordinate velocity')
    force = geometric_force(faces, masses, velocity)
    return dict(diagonal=diagonal, off_diagonal=off_diagonal,
                peculiar_velocity=velocity, coordinate_velocity=coordinate_velocity,
                kinetic_energy=kinetic_energy(diagonal, off_diagonal, velocity),
                geometric_force=force)


def harmonic_potential_gradient(faces, masses, kappa=1.0):
    """Unchanged harmonic potential oracle API, independent of inertia assembly."""
    x, m = _mesh(faces, masses)
    if not np.isscalar(kappa) or not np.isfinite(kappa):
        raise ValueError('kappa must be a finite scalar')
    left, right = x[:-1], x[1:]
    q = left/right
    with np.errstate(over='raise', invalid='raise', divide='raise'):
        q2 = q*q
        denominator = 1.0+q+q2
        numerator = denominator+q2*q+q2*q2
        mean_square_radius = (3.0/5.0)*right*right*numerator/denominator
        potential = (kappa/2.0)*np.dot(m, mean_square_radius)
        coefficient = (3.0/10.0)*kappa*m*right/denominator**2
        grad_left = coefficient*q2*(3.0+6.0*q+4.0*q2+2.0*q2*q)
        grad_right = coefficient*(2.0+4.0*q+6.0*q2+3.0*q2*q)
        gradient = grad_right.copy()
        gradient[:-1] += grad_left[1:]
    return float(_finite(potential, 'harmonic potential')), _finite(gradient, 'harmonic gradient')
