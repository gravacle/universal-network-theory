# Independent analytic review: conserved-record stress

Reviewed: CONSERVED_RECORD_STRESS_SCREEN_V001.md

SHA-256:
7e4fbb948014c00e0144b980273317749ea574cacd1640fd2ab1a47c957ccc2a

**Accept as a correct conditional screen, with no blocking algebraic finding.**
This review used hand derivation and source reading only: no numerical physics,
coefficient evaluation, empirical fit, source modification or remote work.

## Variations and imported scope

At fixed metric, variation of the defined density gives
partial n/partial J^mu=-u_mu/sqrt(-g). Therefore varying J gives
partial_mu phi=-epsilon' u_mu; varying phi gives partial_mu J^mu=0.
At fixed densitized J, variation with respect to the inverse metric gives
delta n=(n/2)(g_mu_nu+u_mu u_nu) delta g^(mu_nu).
Using T_mu_nu=-2 delta S/[sqrt(-g) delta g^(mu_nu)] then gives exactly

    T_mu_nu = n epsilon' u_mu u_nu + (n epsilon'-epsilon)g_mu_nu.

The signs are correct for -+++ signature. Holding the densitized current,
rather than an ordinary current or velocity, fixed during metric variation
is essential.

I also checked Brown's section 2, equations 2.2–2.8: its densitized-current
definition, action, pressure and current-conservation variation support the
stated specialization. The extra flow/entropy potentials belong to the more
general fluid, so calling the displayed single-potential version irrotational
and isentropic is appropriate. This verifies the mathematical import, not its
applicability to UNT. [Brown (1993)](https://arxiv.org/pdf/gr-qc/9304026)

The adopted WTC metric/source interface is a premise of this review, not a
newly demonstrated microscopic or experimental bridge. The document correctly
does not promote conserved finite register labels to a transported continuum
current.

## Conditional obstruction is correctly limited

Convexity throughout [0,n] gives the supporting-line inequality
epsilon(0)>=epsilon(n)-n epsilon'(n), hence p>=-epsilon(0).
Thus zero background gives nonnegative pressure under those premises.
The smooth integral identity is also correct.

Linearized conservation and momentum balance give
c_s squared=n epsilon''/epsilon'. With epsilon'>0, local gradient stability
requires nonnegative epsilon'' at the tested density. **It implies convexity
throughout [0,n] only if that stability requirement holds throughout the
interval.** The text explicitly includes this crucial condition. No statement
of the result should omit it or replace it by “stable now.”

This sound-speed test is not a proof of global equilibrium, all-mode
stability, nonlinear stability, or absence of Jeans growth. The text's
qualifications and separation of the optional Einstein acceleration inference
from the pressure inequality are adequate.

## Counterexample and bulk-equilibrium warning both check

For f=x-(3/2)x squared+x cubed, direct exact substitution at x=11/20 gives
f=2101/8000, f'=103/400, f''=3/10, p/epsilon_*=-121/1000,
(rho+3p)/epsilon_*=-803/8000, and c_s squared=66/103.
The enthalpy is positive: (rho+p)/epsilon_*=1133/8000.

The global-pressure theorem is avoided because f''<0 for 0<x<1/2,
not because current conservation or its metric variation fails. No polynomial
coefficient has thereby been derived from a network.

The exact identity f-(7/16)x=x(x-3/4) squared verifies the common-tangent
comparison. A permitted bulk vacuum/dense mixture at x=0 and x=3/4 has
the same mean density and lower energy at x=11/20 by 11 epsilon_*/500.
Therefore that homogeneous state is not global bulk equilibrium in the
stated phase-separating setting. Locally acceptable sound speed does not
establish a useful metastable lifetime. The interface, topology and kinetic
barrier caveats are indispensable and correctly retained.

## Constructive implications

The three routes are scientifically distinct:

- Derive a nonzero network background energy and its stress, counted only
  once in the matter/geometric action.
- Derive a selected constrained or metastable phase, with formation,
  perturbations, transition barriers and lifetime.
- Demonstrate that network elasticity, retained internal variables,
  multiple fields or nonlocality invalidate the density-only reduction,
  then derive their actual stress rather than assigning fluid labels.

An ordinary positive gradient-energy term alone would not generally repair
negative compressibility at arbitrarily long wavelengths: it may suppress
short wavelengths while leaving the long-wave instability. Likewise, record
creation adds exchange terms; it does not by itself derive negative pressure.
These are cautions for future realizations, not defects in the present screen.

The proposed first discriminant—whether the chosen parent really supplies a
conserved transported current and a local single-variable energy—is useful.
Only after that is established should density derivatives be interpreted as
compressibility. Changing a coupling is not changing density. This screen
narrows a physical construction without claiming either a blanket no-go for
UNT or a demonstrated network dark-energy mechanism.
