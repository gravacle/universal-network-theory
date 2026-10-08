# Structured network averaging and expansion work

2026-10-04. This tests whether spatial structure discarded by the homogeneous
reduction can supply the missing cosmological contribution without another
state law. The new result concerns the existing filtered static action and
a declared quasistatic cell approximation. It is not a full averaged metric
equation or an exclusion of dynamical network geometry.

## An exact bound for the filtered static action

Use a periodic flat cell of volume V with nonnegative ordinary mass density
rho, total mass M, contrast delta_rho=rho-M/V and mean-zero Phi. Define
g=grad Phi and b=Sg, with the same self-adjoint contractive Helmholtz filter
S=(1-ell^2 Laplacian)^(-1). Subtract the already matched constant vacuum
term, which is not generated afresh by structure. The remaining functional is

    E[Phi]=Ffield[g]+integral delta_rho Phi,
    Ffield=(4 pi G)^(-1) integral [g^2/2+U(b)/Kb].

Completing the square in the quadratic modal energy, retaining its positive
quartic term, gives U(b)>=-Kb h(b)^2/2>=-Kb b^2/2. Consequently Ffield>=0,
because ||Sg||_2<=||g||_2. For a global relaxed minimizer Phi_star, the zero
trial field gives E_min<=0, while

    -M osc(Phi_star) <= integral rho Phi_star <= E_min <= 0,
    |E_min|/(M c^2) <= osc(Phi_star)/c^2.

This does not require uniqueness. Existence/regularity, where needed, are
assumptions of this statement; the inequality holds for any attained global
minimum. It does not apply to arbitrary excited states. The field-only term
is not the total binding energy: the ordinary source work must be included.
The filter and all source derivative/contact terms remain unchanged.

This rules out adding the relaxed static binding energy as a positive
rest-mass-like cosmological budget. It does NOT bound the separately varied
clock stress, a full covariant averaged Einstein equation, arbitrary lapse
histories, nonadiabatic modes or strong-field structure. The existing
K0_FLRW_SCALAR_DECISION section 6 already computes a positive clock-only
weak-gradient stress; that is a different quantity and is not contradicted.
No general-relativistic backreaction theorem is imported as a theorem about
UNT. Independent analytical review by handoff_plan_review_v005 checked the
bound and its signs before execution of the illustration below.

## One explicit cell reduction with conserved ordinary mass

To derive a pressure as well as an energy, adopt a quasistatic physical-cell
coarse graining in which the relaxed binding energy E(R) is an additive
correction to M c^2. Its work pressure is p=-dE/dV at fixed M. This is a NEW
approximation to be tested, not a stress tensor inherited from the as-yet
unprovided covariant filtered action. Time derivatives and cell interactions
are not thereby solved. No independent dust amplitude is inserted.

An analytically soluble illustration uses the exact deep-field local limit
W(g)=g^3/(12 pi G a0), not the complete finite-ell bounded-source model.
The ordinary source is a uniform positive sphere of radius b and mass M,
inside a spherical cell of radius R>b. Subtract the cell mean only in the
peculiar gravitational source. The compensating term is a density contrast,
not physical negative matter. At R the peculiar flux vanishes.

Set L=R/b, B=sqrt(G M a0), s=sqrt(1-L^(-3)). In x=r/b coordinates the
enclosed contrast fraction is m(x)=x^3(1-L^(-3)) for x<=1, and
m(x)=1-(x/L)^3 for 1<x<=L. Then

    g=(B/b) sqrt(m(x))/x,
    osc Phi=B A(L),       A=(2/3) atanh(s),
    I(L)=integral_0^L m(x)^(3/2) dx/x
        =(2/3)[atanh(s)-s],
    E=-2 M B I/3,         dI/dlnL=s.

The energy follows from the field equation and its zero-flux surface term:
integral delta_rho Phi=-3 integral W, hence E=-2 integral W. Integrating
the inner and outer regions separately gives the closed forms above. These
are conditional deep-limit formulas, not new measured galaxy results.

For a comoving source shape, b/R is fixed: E is constant and this negative
binding correction dilutes as a^(-3), with zero work pressure. For a fixed
physical core b while R expands,

    rho_E=E/V,       p_E=2 M B s/(9 V),
    (rho_E+3p_E)/(M c^2/V)=(2/3)(B/c^2)(s-I).

Both satisfy d(rho_E V)=-p_E dV along their stated path. The complete matter
acceleration source includes the positive M c^2/V baseline. A small negative
binding term is not a positive dark matter replacement, nor automatically
a negative-pressure fluid. The fixed-core profile is maintained here; its
actual formation and virial dynamics are not derived by this toy reduction.

## Fixed arithmetic test before execution

Use the already exposed a0=1.0059833281731022e-10 m/s^2 and nominal solar
GM=1.32712440018e20 m^3/s^2. Take the prior illustrative masses 10^7,10^9,
10^11 nominal solar masses and L=10,100,1000. Set b=100 sqrt(GM/a0), so
g_max<=.01 a0 within the deep-limit illustration. These generous geometric
ratios are not measured galaxy cell sizes or a claim of quasistatic validity
at arbitrary H R/c. They are not used to fit any parameter.

Check A and I with independent split quadrature, compare 128 and 256 nodes,
and use the substitution u=sqrt(1-(r/R)^3) outside the core to remove endpoint
fractional powers. Relative/scaled errors against the closed forms must be
<=1e-7. Check dI/dlnL=s with symmetric step1e-4, scaled error<=1e-7; check
the pressure by a central volume derivative, same allowance. Numerical
gates cannot be changed after seeing results. Report the potential, binding
and acceleration-source fractions and all failed checks. The static energy
bound must hold in every case; the total rest-plus-binding acceleration
source is reported, not fitted to an observational threshold.

The calculation supplies an explicit homogeneous correction only under the
declared cell-work approximation. A successful implementation is not a
successful cosmology. If the correction is insufficient or of the wrong sign,
retain that result and test a genuinely dynamical volume/clock law next.
Do not rerun old galaxy fits or the already failed homogeneous zero state.

## Relation to earlier theory

Deep-MOND scale and virial identities have established antecedents in
[Milgrom's general virial theorem](https://arxiv.org/abs/1311.2579). This
note claims no novelty for that framework. The filtered-action energy bound,
the chosen compensated profile and its work comparison are the calculations
specified here. They do not derive their continuum mapping from UNT Gates.

## Completed arithmetic result

All 45 fixed controls pass. The nine cases took 0.0319 s internally. The
largest potential range is 2.9961852e-6 c^2 and the most negative binding
correction is -1.8167696e-6 M c^2. For the fixed-core work path the smallest
rest-plus-binding acceleration-source ratio is 0.9999984543. Thus this
declared correction cannot replace an order-one positive missing-matter
budget or make the ordinary cell source accelerate by itself. The matched
vacuum term remains separate. These are conditional weak-field examples,
not observed cell sizes or a covariant cosmological likelihood.

Result SHA256:
21933e846b5349166e0d56ace6045236f3b0ec3ce8fb98d2171c588f6bb41fa1.
Source SHA256:
80381bd3c23fc9e748aa56cf2572857f7ae90555433fe40f5793541eb4051fae.
The result records the pre-execution note hash and every control. No gate or
physical input changed after execution. The numerical worker has exited.

The independent reviewer also verified a general conserved-profile dilation
identity for the finite-ell action. At fixed physical ell, x=a xi gives
db/dln a=b-2Sb at fixed comoving Phi. Envelope differentiation gives

    dE/dln a=(4 pi G)^(-1){ ||g||^2/2
          +integral [3U/Kb-F(b).(b-2Sb)] },
    F(b)=-grad_b U/Kb.

The source term has no explicit scale dependence under conserved-profile
dilation. This relation retains the filter variation; omitting that variation
would produce an incorrect work pressure. It is still quasistatic work, not
a derivation of the missing covariant averaged stress.
