"""Inert consistent-inertia kernel for fixed-mass spherical shells.

This is a discretization repair, not a new force law or a qualified trajectory.
Faces contain the constrained origin followed by N free radii; masses contain
N strictly positive, fixed shell masses. Velocities and momenta contain only
the N free-face entries. Each shell has constant spatial density and the mass
coordinate r(s)^3 = (1-s)L^3 + s R^3. No routine changes its input arrays.

For scale factor A, canonical momentum is p=A^2 M xdot=A M v, where v is the
physical peculiar velocity. Thus xdot=M^-1 p/A^2, K=v^T M v/2, and the kinetic
contribution to pdot is +v^T (partial_x M) v/2. External potential gradients,
pressure, expansion work, and boundary traction are not supplied here.

Only calls perform calculations; there is no runner, file IO, import-time
quadrature, environment mutation, clipping, regularization, or chosen numerical
acceptance tolerance. Root owns numerical execution and prospective controls.
Orders 16/32/64 are the proposed quadrature ladder, not claims of accuracy.
"""

import numpy as np


QUADRATURE_ORDERS = (16, 32, 64)


def _vector(value, name, size=None):
    out = np.asarray(value, dtype=float)
    if out.ndim != 1 or (size is not None and out.size != size):
        raise ValueError(name + " has the wrong vector shape")
    if not np.all(np.isfinite(out)):
        raise ValueError(name + " contains nonfinite entries")
    return out


def _mesh(faces, masses=None):
    x = _vector(faces, "faces")
    if x.size < 2 or x[0] != 0.0 or not np.all(x[1:] > x[:-1]):
        raise ValueError("Faces must start at zero and be strictly increasing")
    if masses is None:
        return x
    m = _vector(masses, "masses", x.size - 1)
    if not np.all(m > 0.0):
        raise ValueError("All fixed shell masses must be positive")
    return x, m


def _finite(value, name):
    if not np.all(np.isfinite(value)):
        raise FloatingPointError(name + " became nonfinite")
    return value


def _tridiagonal(diagonal, off_diagonal):
    diagonal = _vector(diagonal, "diagonal")
    if diagonal.size == 0:
        raise ValueError("The free-face matrix cannot be empty")
    off_diagonal = _vector(off_diagonal, "off_diagonal", diagonal.size - 1)
    return diagonal, off_diagonal


def gauss_rule(order):
    """Return mass-coordinate nodes and weights on (0,1), without caching."""
    if isinstance(order, (bool, np.bool_)) or order not in QUADRATURE_ORDERS:
        raise ValueError("Quadrature order must be 16, 32, or 64")
    nodes, weights = np.polynomial.legendre.leggauss(int(order))
    return (nodes + 1.0) / 2.0, weights / 2.0


def shell_volumes(faces):
    """Physical/comoving volumes in the same length convention as faces.

    Factoring R^3-L^3 avoids subtraction of nearly equal cubes. Overflow or
    underflow to a nonpositive volume is an explicit failure, not a repair.
    """
    x = _mesh(faces)
    left, right = x[:-1], x[1:]
    ratio = left / right
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        volumes = ((4.0 * np.pi / 3.0) * (right - left) * right * right
                   * (1.0 + ratio + ratio * ratio))
    _finite(volumes, "shell volumes")
    if not np.all(volumes > 0.0):
        raise FloatingPointError("A factored shell volume is nonpositive")
    return volumes


def _assemble(faces, masses, order, peculiar_velocity=None):
    """Assemble free-face inertia and optionally its velocity contraction."""
    x, m = _mesh(faces, masses)
    s, weights = gauss_rule(order)
    n = m.size
    velocity = (None if peculiar_velocity is None else
                _vector(peculiar_velocity, "peculiar_velocity", n))
    diagonal = np.zeros(n)
    off_diagonal = np.zeros(n - 1)
    force = None if velocity is None else np.zeros(n)

    # L=0: J_R=s^(1/3), integral J_R^2 ds=3/5. This coefficient is
    # independent of R, so its free-radius derivative and geometric force
    # vanish exactly. No constrained-origin derivative is ever assembled.
    diagonal[0] = (3.0 / 5.0) * m[0]
    if diagonal[0] <= 0.0:
        raise FloatingPointError("The origin inertia underflowed to zero")
    if n == 1:
        return diagonal, off_diagonal, force

    left, right = x[1:-1, None], x[2:, None]
    ratio = left / right
    # 1-(L/R)^3 is evaluated by a factored power difference. Normalizing
    # each shell by R avoids forming dimensional cubes in the Jacobian.
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        delta = ((right - left) / right
                 * (1.0 + ratio + ratio * ratio))
        radius = np.cbrt(ratio * ratio * ratio + s * delta)
        jl = (1.0 - s) * (ratio / radius)**2
        jr = s / (radius * radius)
        cell_mass = m[1:]
        diagonal[:-1] += cell_mass * np.sum(weights * jl * jl, axis=1)
        diagonal[1:] += cell_mass * np.sum(weights * jr * jr, axis=1)
        off_diagonal[:] = cell_mass * np.sum(weights * jl * jr, axis=1)
        if velocity is not None:
            vl, vr = velocity[:-1, None], velocity[1:, None]
            u = jl * vl + jr * vr
            # radius is dimensionless r/R; all derivatives below are with
            # respect to dimensional L,R at fixed mass-coordinate s.
            dljl = 2.0 / right * (ratio * (1.0 - s) / radius**2
                                 - jl * jl / radius)
            drjr = 2.0 / right * (s / radius**2 - jr * jr / radius)
            cross = -2.0 / right * jl * jr / radius
            # (1/2) v^T dM v = sum m integral u (dJ v) ds.
            force[:-1] += cell_mass * np.sum(
                weights * u * (dljl * vl + cross * vr), axis=1)
            force[1:] += cell_mass * np.sum(
                weights * u * (cross * vl + drjr * vr), axis=1)
    _finite(diagonal, "inertia diagonal")
    _finite(off_diagonal, "inertia off-diagonal")
    if force is not None:
        _finite(force, "geometric force")
    if not np.all(diagonal > 0.0):
        raise FloatingPointError("The computed inertia diagonal is nonpositive")
    return diagonal, off_diagonal, force


def mass_matrix(faces, masses, order=32):
    """Return (diagonal, off_diagonal) of the symmetric free-face M."""
    diagonal, off_diagonal, _ = _assemble(faces, masses, order)
    return diagonal, off_diagonal


def geometric_force(faces, masses, peculiar_velocity, order=32):
    """Return +v^T (partial_j M) v/2, the kinetic part of canonical pdot.

    This is not coordinate acceleration, and no Hubble term belongs in pdot
    here. Dividing a force by the old half-adjacent masses is not supported.
    """
    return _assemble(faces, masses, order, peculiar_velocity)[2]


def mass_matrix_and_geometric_force(faces, masses, peculiar_velocity, order=32):
    """Return (diagonal, off_diagonal, geometric_force) in one assembly."""
    return _assemble(faces, masses, order, peculiar_velocity)


def tridiagonal_matvec(diagonal, off_diagonal, vector):
    """Symmetric tridiagonal product in O(N), without forming a dense M."""
    diagonal, off_diagonal = _tridiagonal(diagonal, off_diagonal)
    vector = _vector(vector, "vector", diagonal.size)
    with np.errstate(over="raise", invalid="raise"):
        result = diagonal * vector
        result[:-1] += off_diagonal * vector[1:]
        result[1:] += off_diagonal * vector[:-1]
    return _finite(result, "tridiagonal product")


def solve_spd_tridiagonal(diagonal, off_diagonal, rhs):
    """Solve M x=rhs by an O(N) unpivoted LDL^T factorization.

    Every computed pivot must be finite and strictly positive. No jitter,
    clipping, inversion fallback, or scale-dependent pivot tolerance is used.
    A successful factorization is not a certificate of small solve residual;
    the caller must test residuals and conditioning in the prospective packet.
    """
    diagonal, off_diagonal = _tridiagonal(diagonal, off_diagonal)
    rhs = _vector(rhs, "rhs", diagonal.size)
    pivots = diagonal.copy()
    lower = np.empty_like(off_diagonal)
    result = rhs.copy()
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        for i in range(diagonal.size):
            if not np.isfinite(pivots[i]) or pivots[i] <= 0.0:
                raise np.linalg.LinAlgError("Nonpositive/nonfinite LDL pivot")
            if i < off_diagonal.size:
                lower[i] = off_diagonal[i] / pivots[i]
                pivots[i + 1] -= lower[i] * off_diagonal[i]
                result[i + 1] -= lower[i] * result[i]
        result /= pivots
        for i in range(off_diagonal.size - 1, -1, -1):
            result[i] -= lower[i] * result[i + 1]
    return _finite(result, "SPD solve")


def kinetic_energy(diagonal, off_diagonal, peculiar_velocity):
    """Return K=v^T M v/2 in the caller's mass and velocity units."""
    diagonal, off_diagonal = _tridiagonal(diagonal, off_diagonal)
    velocity = _vector(peculiar_velocity, "peculiar_velocity", diagonal.size)
    with np.errstate(over="raise", invalid="raise"):
        value = 0.5 * np.dot(
            velocity, tridiagonal_matvec(diagonal, off_diagonal, velocity))
    return float(_finite(value, "kinetic energy"))


def canonical_kinematics(faces, masses, momentum, A=1.0, order=32):
    """Return M, velocities, K, and kinetic pdot for a canonical state.

    This convenience function assembles M once for the solve and once again
    with the resulting velocity for its derivative contraction. It remains
    O(N*order) in work and storage and performs no integration or file IO.
    """
    if not np.isscalar(A) or not np.isfinite(A) or A <= 0.0:
        raise ValueError("Scale factor A must be finite and positive")
    diagonal, off_diagonal = mass_matrix(faces, masses, order)
    inverse_p = solve_spd_tridiagonal(diagonal, off_diagonal, momentum)
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        velocity = inverse_p / A
        coordinate_velocity = velocity / A
    _finite(velocity, "peculiar velocity")
    _finite(coordinate_velocity, "coordinate velocity")
    force = geometric_force(faces, masses, velocity, order)
    return dict(diagonal=diagonal, off_diagonal=off_diagonal,
                peculiar_velocity=velocity,
                coordinate_velocity=coordinate_velocity,
                kinetic_energy=kinetic_energy(diagonal, off_diagonal, velocity),
                geometric_force=force)


def harmonic_potential_gradient(faces, masses, kappa=1.0):
    """Independent exact harmonic potential and free-face gradient oracle.

    V=(kappa/2) sum m integral r(s)^2 ds. Uses the factored closed-form
    integral (3/5)(R^5-L^5)/(R^3-L^3), not Jacobians, quadrature, mass_matrix,
    or a call through Mx. Expanded positive polynomials avoid subtracting
    nearly equal powers or quotient-derivative terms for thin shells.

    The exact identity gradient=kappa*M*x applies to the analytic integral;
    the comparison with quadrature M measures a real quadrature defect. At
    rest and A=1 this force gives xddot=-kappa*x, including the first face.
    It says nothing by itself about non-affine continuum accuracy or halos.
    """
    x, m = _mesh(faces, masses)
    if not np.isscalar(kappa) or not np.isfinite(kappa):
        raise ValueError("kappa must be a finite scalar")
    left, right = x[:-1], x[1:]
    q = left / right
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        q2 = q * q
        denominator = 1.0 + q + q2
        numerator = denominator + q2 * q + q2 * q2
        mean_square_radius = (3.0 / 5.0) * right * right * numerator / denominator
        potential = (kappa / 2.0) * np.dot(m, mean_square_radius)
        coefficient = (3.0 / 10.0) * kappa * m * right / denominator**2
        grad_left = coefficient * q2 * (3.0 + 6.0*q + 4.0*q2 + 2.0*q2*q)
        grad_right = coefficient * (2.0 + 4.0*q + 6.0*q2 + 3.0*q2*q)
        gradient = grad_right.copy()
        gradient[:-1] += grad_left[1:]
    return float(_finite(potential, "harmonic potential")), _finite(
        gradient, "harmonic gradient")
