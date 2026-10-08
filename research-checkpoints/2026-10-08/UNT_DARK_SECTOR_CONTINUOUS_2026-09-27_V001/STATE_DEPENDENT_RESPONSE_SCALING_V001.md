# One response law across different density backgrounds

2026-09-27. Analytical extension of `JOINT_RESPONSE_INVERSE_SOLVER_V001.md`
using the resident `RECORD_GRAVITY_CONSTRUCTIVE_SOLVER_V001.md`, read in full.
No new interaction, numerical run, physical density map or galaxy claim.

**Result.** Changing the background can change the response without changing
the universal mechanics. The native one-link model already supplies an
exact example: its static susceptibility scales as the inverse cube of its
response frequency. This permits a constrained scaling hypothesis, not
independent response functions for galaxies and cosmology.

## One energy, evaluated on different states

For the conditional continuum closure retain one universal epsilon(n,chi)
and its same-parent dynamical coefficients Z_t(n,chi), Z_s(n,chi). Static
energy alone does not determine these dynamical coefficients. On a stable
stationary internal branch epsilon_chi=0, let chi=chi_*(n), D>0. Then

    dchi_*/dn = -B/D,             dmu/dn = A-B^2/D,
    h(n)=B^2/D,   ell^2(n)=Z_s/D,   tau^2(n)=Z_t/D.          (1)

Every quantity is evaluated at (n,chi_*(n)). These state-dependent
coefficients come from the common law; constants in a locally frozen
calculation need not be constant across different backgrounds. Define the
branch derivative L=partial_n-(B/D)partial_chi. Where B is nonzero,

    d ln h/dn     = 2(LB)/B-(LD)/D,
    d ln ell^2/dn = (LZ_s)/Z_s-(LD)/D,
    d ln tau^2/dn = (LZ_t)/Z_t-(LD)/D.                       (2)

For example LB=epsilon_nnchi-(B/D)epsilon_nchichi and
LD=epsilon_nchichi-(B/D)epsilon_chichichi. Thus a proposed density scaling
must satisfy shared-derivative relations. A power law is not implied; a
crossover or nonmonotonic response is equally possible.

In a locally uniform patch the conditional induced response is

    T(k,omega;n)=h(n)/[1+ell^2(n)k^2-tau^2(n)(omega+i0)^2]. (3)

Comparisons use the same function at the measured state and retain its
static/dynamic cross predictions. Strong spatial background variation
requires the variable-coefficient equations and boundary data; substituting
n(r) into a translation-invariant Yukawa kernel is not an exact solution.

## An exact native scaling relation already available

For the source-off one-link conditional ground family, the existing native
Hamiltonian gives

    z_s=a-lambda_R s,    R_s=sqrt(z_s^2+4Omega^2),
    D_s=R_s^3/(2Omega^2),  Z_t,s=hbar^2 R_s/(2Omega^2),
    B_s=-lambda_R,
    X_s:=chi_link(0;s)=2Omega^2/R_s^3,
    omega_gap,s=R_s/hbar,    tau_s=hbar/R_s.                (4)

Here s is the record sum 0,1,2; the link occupation probed by chi_link is
not a continuum physical density. Smooth s expressions use the declared
external-bias interpolation. With ONE set of Omega,lambda_R,a,

    X_s omega_gap,s^3 = 2Omega^2/hbar^3,
    h_s:=B_s^2/D_s=lambda_R^2 X_s,
    h_s/tau_s^3=2lambda_R^2 Omega^2/hbar^3.                 (5)

Consequently measuring the gap ratio between two native source settings
predicts the susceptibility ratio:

    X_s2/X_s1=(omega_gap,s1/omega_gap,s2)^3.                (6)

This is a test with no further fitted scaling exponent or amplitude. Its
ratio form survives a common rescaling of the internal coordinate/source.
The SAME response also gives e''(s)=-h_s on the interpolation branch.

The dependence need not increase monotonically with record occupation:
d ln X_s/ds=3lambda_R z_s/R_s^2 changes sign at zero detuning. At z_s=0,
X_s=1/(4Omega) and tau_s=hbar/(2Omega), their finite maxima. At large
|z_s|/Omega, X_s approaches 2Omega^2/|z_s|^3 and tau_s approaches
hbar/|z_s|. These are detuning limits, not a claim of arbitrarily large
physical s in one link. Spatial range, volume conversion, and a map from
record populations to physical n remain unearned. Equation (5) establishes
native state dependence, not yet a galactic scaling law.

## Three distinct changes must be tracked

Changing mean density or preparation changes the background and therefore
the coefficients. Changing probe wavelength or frequency at fixed state
instead samples different parts of (3). Coarse-graining changes what
variables and distributions are retained; it may generate extra frequency
dependence even if every microscopic sector has one oscillator.

For example, an incoherent mixture of the conditional native grounds, with
fixed sector weights p_s under the weak link probe, has exactly

    chi_mix(omega)=sum_s p_s chi_link(omega;s).              (7)

Generally sum_s p_s X_s is not X evaluated at sum_s p_s s. Distinct gaps
also produce several poles in (7); replacing them by the response at the
mean density loses information. The prior inverse note's spectral-moment
inequality diagnoses this failure of a single-oscillator closure. This
ground-sector example does not assume actual formation prepares those
grounds; formed states require their own measured response and history.

A nearly static galactic probe samples small omega and finite spatial k.
Homogeneous cosmological evolution samples k=0 while the background changes
in time. If a conserved physical current and a homogeneous expanding volume
have been earned, its mean density obeys n_bar proportional to a_cos^(-3);
following chi_*(n_bar) additionally requires sufficiently slow evolution
and a justified preparation or relaxation mechanism. The undamped native
oscillator alone does not provide that relaxation. Cosmological perturbations
have physical k=k_com/a_cos and must include expansion in their dynamics.

Thus a galactic outskirts state and a cosmological average need not share
density, response frequency, external fields, fluctuations or history. The
constructive next inference is to constrain ONE state-dependent response
law against several such states, while retaining their source distributions
and preparation. Relations (1)-(6) give testable restrictions on that law;
the necessary physical source and spatial maps still have to be derived.
