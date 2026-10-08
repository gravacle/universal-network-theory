# Continuous network radiation: an exact screen and a conditional source

2026-09-29. Analytical Stage 3 diagnostic; no numerical worker, data fit,
new observation, or modification of the native Hamiltonian was performed.
Read in conjunction with the root `UNT_CMB_NETWORK_THERMAL_HYPOTHESIS_V001.md`
and the Stage 3 handoff. This does not interrupt or replace Stages 1 and 2.

## Result

Three precise results narrow the proposed continuous-background mechanism:

1. A grey thermal emitter/absorber cannot continuously inject net radiation
   while preserving an exact blackbody. Its energy and photon-number moments
   already contradict that requirement except at equal bath/radiation
   temperature, where net injection is zero.
2. Pure Planck-shaped emission can satisfy BOTH necessary moments at one
   source temperature, `T_source=4T/3`, yet still fail the full spectral
   equation. Matching those two moments is therefore demonstrably inadequate.
3. A positive, frequency-dependent detailed-balance source can preserve a
   Planck distribution, with an explicitly debited energy reservoir. Its
   required functional shape and angular opacity are derived below. This is
   an **inverse-constructed conditional candidate**, not a photon coupling
   predicted by native UNT. Its new obligations are specific and testable.

No one of these results rejects all network origins of the CMB. The negative
result belongs to the stated simple source, while the constructive result
does not establish an observed CMB origin or a physical network reservoir.

## 1. Adopted physical interface and the exact Planck tangent

Adopt ordinary two-polarization massless photons, ordinary frequency/redshift,
a homogeneous expanding metric, and physical time for this diagnostic. None
has been derived from the finite native record clock here. Let

    D = partial_t - H*nu*partial_nu,
    f_P(x) = 1/(exp(x)-1),       x=h_P*nu/(k_B*T),
    G(x) = -x*f_P'(x) = x*exp(x)/(exp(x)-1)^2 > 0,
    u = T_dot/T+H.

`h_P` is Planck's constant, not the native link-flip coefficient. The
homogeneous occupation equation is `D f=C[f]`. Its exact restriction to the
Planck family is

    C[f_P(T)] = u*G(x).                                   (1)

With the ordinary mode measure, `n_gamma=(8pi/c^3) integral nu^2 f dnu`
and `rho_gamma=(8pi*h_P/c^3) integral nu^3 f dnu`. Integration by parts
gives `integral x^p G dx=(p+1) integral x^p f_P dx` for p=2,3. Thus (1)
implies

    S = n_dot+3H*n = 3u*n,
    Q = rho_dot+4H*rho = 4u*rho,
    Q/rho = (4/3)*S/n.                                   (2)

These equations use energy density, not mass density. Both endpoint terms
in the integrations vanish. Ordinary redshift alone preserves a Planck
spectrum with u=0; it supplies no net continuous photon production.

## 2. Two exact simple-source failures

### A. Grey thermal exchange fails even the moment test

Specify a homogeneous thermal network bath at T_N=rT and a frequency-independent
nonnegative relaxation rate kappa:

    C_grey[f] = kappa*(f_P(x/r)-f).                        (3)

At a Planck radiation state, its moments are

    S/n = kappa*(r^3-1),
    Q/rho = kappa*(r^4-1).

The discrepancy from the necessary condition (2) factorizes exactly:

    Q/rho-(4/3)*S/n
      = (kappa/3)*(r-1)^2*(3r^2+2r+1).                  (4)

For positive finite temperatures and nonzero kappa this vanishes only at
r=1. Then C_grey[f_P]=0 and u=0. A hotter grey bath injects too much energy
relative to photon number to move tangentially through blackbodies. This
is an instantaneous result, independent of a late-time integration, chosen
expansion history, or observational threshold. It does not apply to a
frequency-dependent bath, extra number-changing processes, modified photon
kinematics, or a source claiming only approximate blackbody agreement.

At r=1, ongoing balanced microscopic emission and absorption remain possible.
That is construct B in the root brief, not net-production construct A. Its
angular opacity can still be observable even though its monopole source is
zero.

### B. Pure thermal emission can pass both moments and still fail

Specify instead `C_emit=j*f_P(x/r)` with j>0 independent of frequency and
no absorption. Now `S/n=j*r^3` and `Q/rho=j*r^4`. Both moments require

    r=4/3,             u=(64/81)*j.                       (5)

But the full source is not uG. In the Rayleigh--Jeans limit x->0,

    C_emit/G -> j*r = 4j/3,

which differs from 64j/81. In the Wien limit,

    C_emit/G ~ j*exp[x*(1-1/r)]/x,

which diverges at r=4/3. More generally no fixed finite r and nonzero j
give a constant C_emit/G at all frequencies. Equation (5) is therefore a
clean counterexample to accepting a mechanism merely because it has the
right integrated energy and photon-number rates. No data grid is necessary
to establish this exact failure.

## 3. A positive source family that can preserve the spectrum

For each mode, adopt an effective photon birth/death process. Upward
transition rate A_nu*(n+1) and downward rate B_nu*n imply directly

    d<f>/dt = A_nu*(1+f)-B_nu*f.

If `A_nu/B_nu=exp[-h_P*nu/(k_B*T_N)]`, its stationary number distribution
is geometric and has mean f_N=f_P(h_P nu/k_B T_N). Writing

    A_nu=kappa_nu*f_N,
    B_nu=kappa_nu*(1+f_N),        kappa_nu>=0

gives the collision term `C=kappa_nu*(f_N-f)`. These relations exhibit
nonnegative rates and detailed balance; they do not derive a Markov bath
or its matrix elements from the native unitary record model.

For a prescribed Planck radiation state and r>1,u>0, the **necessary and
sufficient** opacity in this source class is

    kappa_nu = u*G(x)/[f_P(x/r)-f_P(x)].                  (6)

The denominator is positive, so (6) is a mathematically admissible emission/
absorption source. It has the exact limits

    kappa_nu -> u/(r-1)                     (x->0),
    kappa_nu ~ u*x*exp[-x*(1-1/r)]          (x->infinity). (7)

Thus a hotter bath cannot use an arbitrary grey opacity: exact maintenance
requires a strongly frequency-dependent coupling. Formula (6) was solved
**from the desired Planck tangent**. Its algebraic pass must not be reported
as an independent prediction of a blackbody, a native network spectral
function, or a generic consequence of "processing friction."

A minimally specified comparison candidate can use

    u=Gamma*(r-1),       Gamma>0,
    kappa_nu=Gamma*(r-1)*G/[f_P(x/r)-f_P(x)].             (8)

Its r->1 limit is the nonsingular `kappa_nu=Gamma`. Gamma is a separately
owned microscopic rate, not H or a temperature chosen by terminology.
For a general non-Planck state one may define T from its local photon
energy density and use the actual collision integrals for S,Q; then (8)
defines one explicit nonlinear effective law. The Planck manifold is an
exact invariant solution, but its attraction and spectral/inhomogeneous
stability have not been established here. A feedback-dependent opacity is
itself an adopted physical interaction requiring a mechanism.

The constructive native task has consequently become concrete: derive the
positive emission/absorption rates from an owned network state and compare
their ratio and frequency dependence with (6), or predict their actual
spectral residual. Choosing a separate fitted value at each frequency is
not a theory test. A different fixed functional family is another construct,
not an invisible correction to (3).

## 4. The energy source must be debited, including its stress

Whatever its microscopic realization, the homogeneous network sector must
obey the complementary continuity equation

    rho_N_dot + 3H*(rho_N+p_N) = -Q,
    rho_gamma_dot + 4H*rho_gamma = Q.                    (9)

Other owned sectors or mechanical work add their explicit exchanges once.
Inhomogeneous radiation transfer also exchanges momentum; the full source
four-vector must be obtained from the collision moments, not just from Q.
A photon interaction can change the joint expansion/growth solution and
cannot be appended as an independently adjustable heating function.

For a thermally equilibrated donor at T_N>T and a Planck radiation state,
with no omitted chemical work, their local entropy exchange is

    sigma_total = Q*(1/T-1/T_N) >= 0.                    (10)

This follows from the radiation entropy `s_gamma=4rho_gamma/(3T)` and the
reservoir heat debit -Q/T_N. It is a conditional thermodynamic check, not
proof that the native network possesses that thermal bath or entropy law.

### A closed exchange example, not a selected cosmology

To show the energy debit is not merely symbolic, one possible comparison
reservoir has `rho_N=b*T_N^4`, `p_N=rho_N/3`, b>0. This radiation-like
network-mode thermodynamics is **adopted**, not derived from BS; its energy
and gravitational stress may not be omitted or renamed away. Set
`rho_gamma=a_R*T^4`, `B=b/a_R`, and use (8). Equations (9) then give

    T_dot/T = -H+Gamma*(r-1),
    T_N_dot/T_N = -H-Gamma*(r-1)/(B*r^4),
    r_dot/r = -Gamma*(r-1)*[1+1/(B*r^4)],
    a^4*rho_gamma*(1+B*r^4) = constant.                 (11)

For an initially hotter finite donor, its temperature ratio decreases
toward unity while net photons are produced. If equilibration is completed,

    (a*T)_final^4 = (a_i*T_i)^4*(1+B*r_i^4)/(1+B).        (12)

There is no free continuing energy supply: both sectors together retain
their redshift-rescaled radiation energy a^4*(rho_gamma+rho_N), and the source naturally turns off
at r=1. Holding r>1 fixed instead would require additional owned work or
a different donor equation of state. Equation (11) does not generate an
initial Planck state from vacuum, determine b/Gamma/initial temperatures,
or evade early-universe constraints on the total energy. It is a complete
homogeneous **exchange subsystem conditional on H**, not a derived native
cosmology or a new dark component declared invisible to gravity.

More generally, if Q>=0 and the spectrum remains Planckian, define
`L=integral_(t_i)^t u dt`. The net fractions of current radiation
energy and comoving photon number supplied since t_i, after redshifting the
initial contribution to the current epoch, are

    F_E=1-exp(-4L),       F_N=1-exp(-3L).                 (13)

These are net energy/number bookkeeping fractions, not photon identity
tags: absorption and re-emission can replace photons even when F_E=F_N=0.
Explicitly, F_E=1-(a_i^4*rho_i)/(a^4*rho) uses redshift-rescaled energy,
whereas F_N=1-(a_i^3*n_i)/(a^3*n) uses actual comoving photon number.
The former does not assert conservation of the ordinary comoving-volume
energy a^3*rho, which also changes through radiation pressure work.
They connect a claimed substantial continuous contribution to a required
temperature history, rather than silently assuming all production occurs
near the present epoch. Constant physical T would require u=H,Q=4Hrho;
even a putative vacuum-like donor p_N=-rho_N must then deplete by
`rho_N_dot=-Q`, rather than retain an unchanged vacuum energy.

## 5. Preserving the monopole does not preserve the structured sky

For perturbations, the derivative along an unperturbed ray also includes
the ordinary spatial streaming term; the homogeneous equations above are
its monopole restriction. In a spatially homogeneous, isotropic bath, linear
anisotropic occupation
perturbations have collision term

    delta C_(ell m) = -kappa_nu*delta f_(ell m), ell>=1.  (14)

For independent equal-rate polarization channels, the same damping applies
to traceless polarization occupation/Stokes coherences: the bath injects
no correlated polarization. Free streaming and metric terms must still
be retained in a full perturbation equation. Along a ray the inherited
occupation perturbation has a transfer factor

    exp(-tau_nu),     tau_nu=integral kappa_(nu(t))(t) dt. (15)

An isotropic source cannot manufacture the missing coherent angular pattern
by this damping law. Perturbed or correlated network emission could do so,
but its spatial correlations, polarization matrix, transfer phases and
noise are additional predictions, not consequences of a correct monopole.
Equation (14) specifies the source-free anisotropic collision contribution,
not a claim that every possible network perturbation has zero source.

For a constant r>1 while the ray remains in the Rayleigh--Jeans regime,
(7) gives the further exact limiting relation

    tau_RJ = L/(r-1) = -log(1-F_E)/[4(r-1)].             (16)

For variable 1<r<=r_max the same expression with r_max gives a lower bound
in that regime. A near-equilibrium donor therefore needs large optical
depth to supply a substantial net fraction. That erases pre-existing
angular/polarization occupations unless their source is also explained.
No bound uniform over arbitrarily hot donors or non-Rayleigh--Jeans rays
is asserted. Earlier production before a structured sky forms is not
equivalent to production that overwrites an already observed pattern.

There is a second frequency test even for infinitesimal temperature
anisotropies. Write `delta f=G(x)*Theta`, with the background obeying (1).
Along the adopted unperturbed ray `D x=-u*x`. With no bath anisotropy,

    D Theta = [-kappa_nu+u*x*G'(x)/G(x)]*Theta.           (17)

For the inverse source (6), the bracket divided by u tends to
`-r/(r-1)` in the Rayleigh--Jeans limit and to `1-x` in the Wien limit.
It is not frequency independent. Consequently preservation of the mean
blackbody does not automatically preserve the common thermodynamic-
temperature shape of an existing anisotropy. Equivalently, the final
temperature perturbation carries `exp(-tau)*G(x_i)/G(x_f)`, not just
exp(-tau). The same collision model must face multifrequency intensity
and polarization data; a monopole fit alone is insufficient.

## 6. What this permits next

The grey-source and pure-emission failures above are exact and need no
numerical grid. The positive family is a precise comparison target whose
physical derivation remains open. Its first meaningful native test is an
owned photon/source interaction that yields emission, absorption, energy
and momentum debit from one network state, with no frequency-by-frequency
data fitting. A candidate should then predict spectral residuals, T(z),
opacity and angular/polarization transfer with the same parameters/history.

For observational continuation, the root brief already names primary
COBE/FIRAS and Planck products and the required model-assumption audits.
No observed constraint or statistical significance was imported or evaluated
in this note. Blackbody normalization, temperature scale and the origin of
correlations remain separate obligations. A failure of source (3) does not
stop the dark program or exclude balanced maintenance or a network-generated
primordial state under distinct construct IDs.
