# Clamped common-phase existence and continuation: analytical screen V001

2026-09-29. Analytical only. No producer, orbit quadrature, eigensolve,
numerical result selection, new physical coefficient, or frozen-source edit.
This concerns the already declared clamped Kuzmin patch, not an isolated
galaxy or the selection of its preferred-clock state by cosmological evolution.

## 1. A boundary regularity obstruction, not an equilibrium no-go

The outer wall has u(L,z)=0, whereas the bottom sheet has
D_z(x,0)=j(x)=(1+x^2)^(-3/2), including j(L)>0. A C1 solution with continuous
finite constitutive coefficients cannot extend through their intersection:
the wall condition implies its tangential u_z=0 there, while the bottom
requires nonzero D_z=mu*u_z. Here mu=K_T/Kb. This argument does not exclude a
bounded weak solution, a smooth interior solution, or convergence away from
the prescribed clamp corner.

An independent local constant-coefficient oracle makes the distinction
explicit. Set X=L-x>=0, r=sqrt(X^2+z^2), theta=atan2(z,X), and approximate
the bottom flux by j0>0 and the coefficient by mu0>0. The harmonic function

    u_corner=(2*j0/(pi*mu0))
                *[X*log(r/r0)+z*(pi/2-theta)]                 (1)

vanishes at X=0 and has mu0*u_z=j0 at z=0. The arbitrary r0 only changes
a regular homogeneous X term. Its potential tends to zero at the corner,
but its X derivative diverges logarithmically. The axisymmetric curvature
term is lower order locally at x=L>0. Equation (1) is an oracle, not a
claimed exact nonlinear asymptotic theorem. The bounded source map tends
to Newtonian principal flux at very large gradient, so it does not provide
a reason to assume the incompatible C1 boundary data become compatible.

Keep all prescribed grid points and comparisons. Label the corner when
interpreting maximum gradients, maximum omitted-stress estimates, and
refinement. Do not silently remove it, fit a smoothing width, or call the
result a failure of all network equilibria. An eventually physical matching
surface would need its own compatible source and wall/environment stress.

## 2. Exact finite-field identities for an attractive candidate

Use epsilon=gstar*a/c^2 and T=E+3Pi. The frozen weak-lapse equation is

    div(mu(Phi,g)*grad u)=epsilon*[T(Phi,g)-Tb]/Kb,
    Phi=epsilon*u,  g=|grad u|,  mu=1-F/(Kb*g).               (2)

At g=0 use the exact continuous coefficient. Suppose a candidate is
everywhere attractive: v=-u>=0. Require its constitutive branch to exist
and be uniformly elliptic. In particular 0<mu<=1: the upper bound follows
from the positive source-aligned soft and scalar-hard polarization. This
assumption is not imposed by clipping an ineligible material value.

Define at the SAME local g, not at a newly chosen state profile,

    Tc(g)=T(0,g)-Tb,
    Jsec(v,g)=integral_0^1 J(-s*epsilon*v,g) ds.

Because T_Phi=-J on occupied segments and J=0 on the admissible empty
segment, continuity across the phase boundary gives the exact identity

    T(-epsilon*v,g)-Tb=Tc(g)+epsilon*v*Jsec(v,g).             (3)

No small-density-contrast expansion is used. A positive v can have a very
large I/Ib. Nor may Tc simply be dropped: the clamp state at nonzero field
is different from the homogeneous state even when its lapse is one.

Use the cylindrical measure dV=x dx dz, with the common 2pi factor omitted.
Multiplying (2) by v gives a useful full-state integral check:

    integral mu*|grad v|^2
      =epsilon^2/Kb * integral Jsec*v^2
       +epsilon/Kb * integral Tc*v + integral_bottom j*v*x dx. (4)

This is an identity of the scalar equation, not the full gravitational
energy or a proof of dynamical stability. The original absolute energy,
pressure and DeltaU remain in the material and background accounting.

For a sharper necessary condition, freeze the candidate's actual scalar
mu(x,z) and let phi1>0 be the first eigenfunction of -div(mu*grad), with
zero Dirichlet data at the top/outer wall and homogeneous normal flux at
the bottom/axis. Denote its eigenvalue lambda1(mu). Green's identity gives

    lambda1(mu)*integral phi1*v
       =epsilon^2/Kb * integral phi1*Jsec*v + B_eff,
    B_eff=integral_bottom phi1*j*x dx
                         +epsilon/Kb*integral phi1*Tc.       (5)

If B_eff>0, an everywhere attractive nonzero solution necessarily obeys

    epsilon^2*inf(Jsec)/Kb < lambda1(mu) <= lambda_Lap,
    lambda_Lap=[j_01^2+pi^2/4]/L^2.                          (6)

Here j_01 is the first positive zero of J0. The Laplacian eigenfunction
is J0(j_01*x/L)*cos(pi*z/(2L)), positive inside. Its mixed boundaries
are exactly those of this cylindrical patch. The Rayleigh upper bound
in (6) uses mu<=1. If mu_min>0, the complementary lower bound is
mu_min*lambda_Lap<=lambda1(mu).

The sign B_eff>0 is a hypothesis to establish, not a consequence merely
of positive sheet mass: Tc can contribute with either sign. One may use
the exact identity (5) without assuming that sign. Likewise, a bound on
Jsec must cover the entire intervening phase segment, not just its endpoint.
Failure of the necessary condition excludes this everywhere attractive
elliptic branch on these clamps; it does not exclude sign-changing roots,
different states, nonlinear nonelliptic dynamics, or the geodesic-clock
branch already present in the same macroscopic action.

## 3. An exact solvable branch and what a resonance means

A planar constant-coefficient limit supplies an inexpensive analytical
oracle. Set Tc=0, mu=mu0>0 and J=J0>0, impose -mu0*v'(0)=j0 and v(L)=0.
Writing k^2=epsilon^2*J0/(Kb*mu0), the exact solution is

    v(z)=j0*sin[k*(L-z)]/[mu0*k*cos(k*L)].                   (7)

It is positive and bounded on the first branch 0<=kL<pi/2, with
v=j0*(L-z)/mu0 at k=0. At kL=pi/2 the positive boundary flux violates
Fredholm compatibility: there is no finite solution of this linear
problem. Away from the discrete resonances there is a unique linear
solution, but beyond the first threshold it cannot stay nonnegative.
Thus ellipticity, solvability, and an attractive branch are different
questions. A linear resonance is not itself a nonlinear saddle-node;
the latter requires following the nonlinear branch and its null tangent.

For the finite hard oscillator in the weak-lapse, small-unit-action and
small eta=h/R^2 regime,

    Jsec=(4/3)*beta*R^4*[1+O(ib+|Phi|+eta^2)],
    Tc=-2*Esoft,min(h)-beta*h^2 + higher-order hard terms.    (8)

The leading hard source shift in (8) must be kept. Meanwhile finite-field
soft response can make K_T/Kb order unity even though the cosmic K0/Kb is
tiny. This changes the local cold response length from R^-4 near the
cosmic state to R^-2 at finite field; it does not remove the R^4 growth
of the phase reaction in (8). At fixed otherwise comparable calibration,
the 8192/128 ratio contributes 2^24 to that reaction coefficient, multiplied
by the actual ratio of epsilon^2. This is a scaling statement, not a
numerical existence decision for either declared gap or box.

In particular one must not substitute cosmic K0 for finite-field K_T in
(5), nor suppose arbitrarily increasing the density always restores a
static solution. At much larger action the quartic frequency implies
energy growing as the fourth power of the required frequency, hence an
exponential dependence on -Phi. That regime can make self-gravity stronger,
not automatically regulate it; it is outside a weak-lapse cold expansion
when the corresponding assumptions fail.

## 4. A sufficient local invertibility condition

Let w be a perturbation with zero top/outer value and homogeneous variation
of the prescribed normal flux. The exact continuum Newton map of (2) is

    Kb*Lw=div(Ktensor*grad w)-2*epsilon*F*n.grad w
             +[epsilon^2*J-epsilon*div(F_Phi*n)]*w,          (9)

where n=grad u/g and Ktensor has eigenvalues K_T,K_L. At a zero gradient
the vector expressions use their continuous limits. The apparent F_Phi
gradient drifts cancel to yield the coefficient -2epsilon*F in (9),
but F_Phi remains in the zero-order term and natural boundary variation.
The Jacobian is not generically self-adjoint or positive definite.

Its natural weak form yields

    Kb*integral w*(-Lw)
       =integral grad w.Ktensor.grad w
        -2epsilon*integral(F_Phi-F)*w*n.grad w
        -epsilon^2*integral J*w^2.                          (10)

Therefore, with k_min the minimum principal material eigenvalue,
Bstar=sup|F_Phi-F| and Jmax=sup J on the candidate, the strict inequality

    k_min-2epsilon*Bstar/sqrt(lambda_Lap)
                     -epsilon^2*Jmax/lambda_Lap > 0         (11)

is sufficient for coercivity and local weak invertibility, subject to
the stated regular coefficient/branch hypotheses. Poincare and
Cauchy-Schwarz give (11) directly. It is conservative: failure does not
prove a singular Jacobian, no equilibrium, or instability. If this bound
holds uniformly along the segment between two admissible solutions,
the same difference argument establishes uniqueness on that segment;
checking it only at one solution establishes no global uniqueness theorem.
None of these static tests is a dynamical ghost/growth criterion.

## 5. Prospective continuation if direct Newton seeds fail

Do not change the final material, gap, common chemical potential, clamps,
or numerical success tolerances. A legitimate numerical continuation is
to replace only the sheet flux by lambda*j, following lambda from zero
to one and retaining the complete branch record. It is a family of
externally supported mathematical sources, not a newly claimed formation
history or permission to discard the original two frozen seeds.

At lambda=0, u=0 is the exact occupied cosmic solution. For finite R and
positive Ib the local material is smooth, K0>0, and its linearization is

    (K0/Kb)*Delta w+(epsilon^2*Jb/Kb)*w=0,

with the mixed homogeneous boundaries. Away from its discrete eigenvalue
resonances, the implicit-function theorem supplies a locally unique weak
branch under regularity assumptions appropriate to the mixed corner.
It does not guarantee that this small-source branch is everywhere
attractive; (5)-(7) explain why that additional sign can fail. The ideal
R=infinity limit cannot be substituted into this finite-K0 argument.

At a simple nonlinear turning point, augment the unknowns by lambda and
use an explicit pseudo-arclength equation to retain both sides instead of
requiring du/dlambda to stay finite. Record tangent, smallest singular
value, phase-active set, material ellipticity, full source/flux ledger and
the continuation parameter. Reaching lambda=1 would produce another
declared numerical branch, not retrospectively repair a failed seed or
prove dynamical accessibility. Failure to follow this one path is not
exhaustion of disconnected solution branches. Loss of the constitutive
branch, loss of ellipticity, a proved compatibility violation, and a
failed linear solve must remain distinct outcome classes.

The frozen current census remains unchanged. These identities provide
independent diagnostics and a concrete method for a later prospective
continuation, not outcome-tuned acceptance criteria.

## Sources read in full

- `CLAMPED_COMMON_PHASE_KUZMIN_PATCH_V001.md`, SHA
  `c9df013c7d574e4e240a475a581903ebe921a6751b8dafa5146456c02c8b8285`.
- `FINITE_GAP_CALIBRATION_STATIC_LENGTH_V001.md`, SHA
  `e8c4622d1f86a97f63b24499e21c134100edcad5e30e74208503f4af3cd62d36`.
- `MACROSCOPIC_ALPHA_ONE_GALAXY_BVP_V001.md`, SHA
  `64d98fff0681a81edce675049f6d72bb54c58b1d92f463f69fdd09dff8ed7bb3`.
- `COMMON_ACTION_GALAXY_BOUNDARY_AND_INITIAL_STATE_V001.md`, SHA
  `2eb30bb54416d31a69109b1d48795789a208b2418bfb237cfd81a291ec006c26`.
