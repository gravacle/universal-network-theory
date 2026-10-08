# Exact shell inertia and geometric force

2026-09-30. Root analytic derivation during prospective consistent-kinetic
oracle design. No numerical outcome or trajectory is present. This supplements
SPHERICAL_CONSISTENT_KINETIC_REPAIR_V001.md and leaves the old kernel and all
two-current evidence unchanged. Independent symbolic review is requested.

## Closed integrals

For fixed positive shell mass m and 0 <= L < R, put

    r(s)^3 = (1-s)L^3+sR^3,  0 <= s <= 1,
    J_L=(1-s)L^2/r^2,  J_R=sR^2/r^2,
    M_ab=m integral_0^1 J_a J_b ds.

Changing variable to r gives ds=3r^2 dr/(R^3-L^3). The three elementary
antiderivatives needed after extracting the constant prefactors are

    LL: -R^6/r - R^3 r^2 + r^5/5,
    RR: r^5/5 - L^3 r^2 - L^6/r,
    LR: (R^3+L^3)r^2/2 - r^5/5 + R^3 L^3/r.

The L=0 endpoint is taken separately through the original integral, never
by evaluating a singular antiderivative. Set q=L/R and S=1+q+q^2. Factoring
the common (1-q)^3 from each definite integral gives M=m F(q), where

    F_LL = (3/5) q^3 (5+6q+3q^2+q^3)/S^3,
    F_RR = (3/5) (1+3q+6q^2+5q^3)/S^3,
    F_LR = F_RL = (9/10) q^2 (1+3q+q^2)/S^3.

These positive-polynomial expressions avoid subtraction of nearly equal
powers and need no quadrature. At q=0 they give F_RR=3/5 and all constrained
left entries zero. As q approaches one, the limits are 1/3,1/3,1/6. The
zero-width limit is a check only: actual meshes must retain L<R and positive
volumes. Positive definiteness on free faces still follows from the integral
of the squared interpolated velocity, not from positive diagonal entries alone.

## Radius derivatives and canonical geometric force

At fixed mass, d_L M=m F'(q)/R and d_R M=-m q F'(q)/R. Direct differentiation
and cancellation give

    F_LL' = (9/5) q^2 (5+8q+2q^2)/S^4,
    F_RR' = -(9/5) q^2 (2+8q+5q^2)/S^4,
    F_LR' = (9/5) q(1-q)(1+5q+5q^2+q^3)/S^4.

For the shell's physical peculiar face velocities v_L,v_R, the contraction
Q=v^T F' v can equivalently be evaluated as

    Q = (9/5) q/S^4 * (v_L-q v_R)
        * [q(5+8q+2q^2)v_L+(2+8q+5q^2)v_R].

Thus the shell contributions to canonical momentum derivatives are

    g_L = m Q/(2R),  g_R = -q g_L.

For the first shell, the origin is constrained, M_RR=3m/5 is independent
of its radius and its free-radius geometric force is exactly zero. Global
assembly adds adjacent shell contributions to the free-face tridiagonal
matrix and force vector. No half-adjacent-mass division is retained.

The contraction vanishes for affine velocity v_L=q v_R, as required by the
homogeneous radial map. Shellwise L*g_L+R*g_R=0 also follows, and expresses
the degree-zero homogeneity of M. These are analytic identities, not fitted
force corrections or evidence of non-affine continuum accuracy.

The inherited conventions stay p=A M v=A^2 M xdot and
Hkin=p^T M^-1 p/(2A^2). Consequently partial_x Hkin at fixed p is -g, and
partial_ln(A) Hkin at fixed x,p is -2Hkin. Potential/pressure gradients,
expansion work and boundary traction are separate terms; this derivation
does not alter any of them or supply a new gravitational response law.

## Prospective use and safeguards

First use these independently derived closed expressions as an oracle for
the inert 16/32/64 quadrature kernel, retaining every error and the existing
2e-11 arithmetic / 2e-6 derivative controls. Review and freeze the complete
oracle before numerical execution. In particular, qualify SPD solves and
conditioning, first-shell inertia, independent harmonic gradients, fixed-p
kinetic derivatives and nonzero-velocity work cancellation.

An eventual separately versioned exact-inertia runtime could remove the
quadrature expense while representing the same finite-shell kinetic action.
It is not implemented or qualified by this note. Whole-trajectory, spatial,
time/domain, characteristic and crossing controls would still be owed. No
formed halo, lensing, merger, full metric, native source/formation or Stage 3
claim follows from this finite-dimensional identity.
