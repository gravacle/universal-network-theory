# Prospective consistent shell kinetic energy

Additive analytical repair proposal, not an executed trajectory. V001's twelve
qualified semidiscrete runs, origin inconsistency and false continuum flags
remain unchanged. No force multiplier, central mask or new physical pressure
is introduced. Independent reviewer has checked the homogeneity argument below.

## Mass map and inertia

Retain each shell's exact positive fixed mass m and constant spatial density
between its two moving radii L,R. Its fixed mass coordinate s in [0,1] is

    r(s)^3 = (1-s)L^3+sR^3,
    J_L = (1-s)L^2/r^2,   J_R=sR^2/r^2,
    u(s)=J_L dot L+J_R dot R.

The consistent kinetic energy is T=(A^2/2) sum m integral u(s)^2 ds.
Assemble M=sum m integral J^T J ds on free faces, keeping r=0 fixed.
M is symmetric positive definite for strictly ordered positive volumes and
masses: a zero quadratic form implies zero interpolated velocity in every
shell and hence zero free-face velocity. Its support is tridiagonal. In the
first shell L=0, J_R=s^(1/3), so M_RR=3m/5 exactly; all constrained-L terms
vanish. This replaces the inconsistent half-adjacent-mass kinetic lumping,
not the already energy-derived gravity or internal-pressure force.

M depends on radii; merely replacing the velocity division by a linear solve
would not be a complete repair. With canonical p=A^2 M dot x,

    Hkin=p^T M^-1 p/(2A^2),
    dot x=M^-1 p/A^2,
    dot p_j=(A^2/2) dot x^T (partial_j M) dot x
              - partial_j U - (partial_j W0)/A + boundary traction.

For a physical peculiar velocity v=A dot x, the geometric term is
(1/2)v^T(partial_j M)v. K=(1/2)v^T Mv. Explicit expansion still supplies
-2H K in the energy ledger; the geometric term cancels the coordinate
dependence of kinetic energy. All pressure/gravity work uses dot x, as before.

At fixed s the exact derivatives are

    partial_L J_L = 2L(1-s)/r^2-2J_L^2/r,
    partial_R J_R = 2Rs/r^2-2J_R^2/r,
    partial_R J_L = partial_L J_R = -2J_L J_R/r.

Thus derivatives of M follow under the same finite-shell integral. The origin
block is treated analytically, not by quadrature through a singular endpoint.
Away from the first shell, fixed Gauss-Legendre orders16/32/64 are a prospective
small implementation ladder; all orders and defects must be reported before
any trajectory qualification. Thin shells require cancellation-safe volume
arithmetic and explicit order checks, not an assumed exact numerical integral.

## Exact regular-origin oracle

The mass map is homogeneous of degree one: J x=r and (partial_j J)x=0.
Consequently Mx=sum m integral J^T r ds. The derivative of a harmonic potential
V=(kappa/2) sum m integral r^2 ds is kappa Mx, exactly. Starting at rest gives
ddot x=-kappa x, including the first face. For affine velocity dot x=h x,
the geometric contraction also vanishes, because (partial_j J)x=0.
This is the required local regularity identity missing from V001. It does not
prove finite-resolution accuracy for non-affine collapse or a continuum limit.

The harmonic derivative can also be evaluated independently from
integral r^2 ds=(3/5)(R^5-L^5)/(R^3-L^3). Quotients should be evaluated using
factored power differences. Compare against Mx, not a potential formula that
calls the very same matrix routine. Affine motion, kinetic derivatives at
fixed canonical p, and nonzero-velocity work must all be tested.

## Next implementation and unchanged debts

An inert reusable kernel and prospective oracle packet should precede the
next full solver. Qualify SPD solves, symmetry, first-shell3m/5, homogeneity,
harmonic forcing, fixed-p kinetic finite differences and quadrature refinement
using the existing arithmetic2e-11 and derivative2e-6 controls, retaining raw
failures. No numerical acceptance target is inferred from V001's observed
central error. Afterwards create an additive two-current version with the
consistent canonical equations, same source/background/pressure/energy terms,
same mass/current, grids/domain/time ladder and immutable failures.

Recheck physical characteristic and guard interpretation under the new
semidiscrete operator before assuming the earlier CFL bound applies. Root
alone executes, with one bounded worker. Independent source review and a
prospectively specified continuum/readout error budget remain necessary.
Passing this oracle alone would not establish full Einstein gravity, observed
lensing, formed halos, multistream transport or merger morphology.
