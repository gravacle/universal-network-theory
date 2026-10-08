# Native nonstationary transport Ward identity V001

2026-09-29. Additive exact analysis of the owned 16D held cell. No new
preparation, numerical producer, continuum transport term or physical clock
identification. The full finite-time response, not the instantaneous contact
alone, is the microscopic quantity available for a proposed phase matching.

## 1. Source, current and units

Use the basis and all original energy terms of the authenticated transport
test. Let P be carrier-right occupation, n the incidence projector,
A=|R><L|, T=A+A† and J=i(A−A†), the conventional carrier Pauli Y. The older
saved operator named YC has the opposite sign. In the inherited units,

    H = 3I + R − X_a + n(9/4 − lambda_R R − t_hop T),
    j = t_hop nJ = i[H,P],       D = t_hop nT = [P,[H,P]].       (1)

Here t_hop=1/2; lambda_R=1/2 or zero in the feedback-off control. The symbol
j is an operator with **energy units**; the particle transfer rate is j/ℏ.
In particular [P,j]=iD and Pdot=j/ℏ. The numerical sources used ℏ=1.

For a dimensionless diagnostic edge phase phi and a scalar source V with
energy units, set

    G(phi)=exp(i phi P),
    H_phi=G H G†=H+t_hop n[T(1−cos phi)−J sin phi],
    H_src(t)=H_phi(t)+V(t)P,
    j_phi=−∂_phi H_phi=t_hop n[J cos phi−T sin phi],
    D_phi=∂_phi² H_phi=t_hop n[T cos phi+J sin phi].              (2)

The original current-square term is unchanged by this consistent twist.
There is no independent loop flux on this single edge. For a fixed state,
the exact source work is <D>(1−cos phi)−<j>sin phi. A state-only twist
rho→G rho G† at fixed H has the opposite sine sign. These are distinct
experiments; neither may be substituted for the other.

## 2. Exact time-dependent frame and initial-state term

Writing psi(t)=G(phi(t)) chi(t) gives, without an approximation,

    iℏ chi_dot = [H+F(t)P] chi,
    F(t)=V(t)+ℏ phi_dot(t).                                    (3)

Thus the physical driving combination for this declared source is F, not
phi by itself. A genuinely pure-gauge change of the original evolution is
H_phi−ℏ phi_dot P, for which F=0. If the original initial density matrix is
rho_w (the actual formed state held to age w), keeping that same physical
initial state while phi(t0)=phi0 produces the frame initial state
G(phi0)† rho_w G(phi0). Alternatively, covariantly transforming the physical
initial state to G(phi0)rho_w G(phi0)† leaves the frame initial state rho_w.
The two choices have different boundary responses. Pure-gauge invariance
applies to the second choice, not to an unmatched initial-state quench.

This also fixes the complete energy ledger. For arbitrary exact evolution,

    d<H_src>/dt = −phi_dot <j_phi> + V_dot <P>,
    d<H_phi>/dt = −F <j_phi>/ℏ.                                (4)

The second equation is the intrinsic, gauge-covariant energy transfer; the
first retains the scalar-source energy. A time-dependent frame generator is
not an additional matter-energy component, and source work is not discarded.

## 3. Nonstationary retarded kernel and Ward identity

Use held-H Heisenberg operators with origin t0 and the actual rho_w. Define

    chi_AB(t,s) = (i/ℏ) theta(t−s) Tr rho_w [A(t),B(s)].          (5)

A perturbation −f(s)B gives delta<A(t)>=∫chi_AB(t,s)f(s)ds for an unchanged
initial state. No commutation of rho_w with H is assumed. In general the
kernel depends on both times, not only their difference.

For the strict interior t>s,

    chi_Pj = ℏ ∂_s chi_PP,
    chi_jP = ℏ ∂_t chi_PP,
    chi_jj = ℏ² ∂_t∂_s chi_PP.                                 (6)

The right-sided coincident limits of the commutator factors are
chi_PP=0, chi_jP=<D(s)>/ℏ and chi_Pj=−<D(s)>/ℏ. Consequently the complete
retarded current response to phi, including its explicit source derivative,
is the distribution

    K_jphi(t,s)=chi_jj(t,s)−<D(t)> delta(t−s)
              =ℏ² ∂_t∂_s chi_PP(t,s).                          (7)

The delta term is essential. Equation (7) can be read through the following
Volterra identities, which avoid any ambiguous convention for theta(0).
For differentiable phi,V and a fixed physical initial state,

    delta P(t)
      = ∫ chi_Pj(t,s)phi(s) ds − ∫ chi_PP(t,s)V(s) ds
      = −ℏ chi_PP(t,t0)phi0 − ∫ chi_PP(t,s)F(s) ds,

    delta j(t)
      = −<D(t)>phi(t)+∫chi_jj(t,s)phi(s)ds−∫chi_jP(t,s)V(s)ds
      = −ℏ chi_jP(t,t0)phi0 − ∫ chi_jP(t,s)F(s) ds.             (8)

All integrals in (8) are from t0 to t. For example, integration by parts
gives ∫chi_jj phi=<D(t)>phi(t)−ℏ chi_jP(t,t0)phi0−ℏ∫chi_jP phi_dot:
the upper endpoint cancels the explicit contact, not the initial boundary.
The continuity response is exactly ∂_t delta P=delta j/ℏ.

An initial state-only infinitesimal twist by eta, with eta dimensionless,
adds delta rho_w=i eta[P,rho_w] and hence

    delta P_initial=+ℏ eta chi_PP(t,t0),
    delta j_initial=+ℏ eta chi_jP(t,t0).                        (9)

Taking eta=phi0 cancels the boundary in (8). With F=0 this proves the exact
linear gauge-null response of both covariant observables. Conversely, a
constant phase switched on at t0 with unchanged state has the nonzero
boundary response in (8); isospectrality does not erase a source quench.
Impulses require the corresponding finite kick or a specified limiting
smooth source, not omission of this boundary term.

Two useful exact consequences are

    chi_PP(s+tau,s)=<D(s)> tau/ℏ²+O(tau²),
    ∫[t0,t] chi_jj(t,s)ds=<D(t)>−ℏ chi_jP(t,t0).                (10)

The second is the finite-time current sum rule with its initial-state term.
It is not a stationary infinite-time cancellation assumption. In a separately
specified stationary state, with a causal/adiabatic Fourier prescription,
(7) reduces to K_jphi(omega)=ℏ² omega² chi_PP(omega). A finite isolated cell
can retain oscillatory transients, so taking its long-time or zero-frequency
limit needs that prescription. This stationary comparison is not used to
replace the actual coherent held states.

## 4. Entire kernel is determined by retained evidence

The three original formed vectors, their own held Hamiltonians and the
twelve analytical projectors already determine (5). No formation replay or
eigensolver is needed. For labels a=(R,s,beta), with s,beta=±1,

    x_Rs=9/4−lambda_R R−t_hop s,  d_Rs=sqrt(x_Rs²+4),
    E_a=3+R+(x_Rs+beta d_Rs)/2,
    Pi_a=P_R (I+sT)/2 [I−beta(2X_a+x_Rs Z_a)/d_Rs]/2.           (11)

The symbol X_a in (11) denotes the incidence Pauli matrix, not the spectral
label. The R=1 multiplicity is kept in its full projector. The sum of these
orthogonal projectors is I. Exact degeneracies cause no division by a gap;
coincident energies can be grouped without changing any expression.

For t0=0, rho_w=exp(−iHw/ℏ)rho_formed exp(+iHw/ℏ), and

    P(t)=Σ_ab exp[i(E_a−E_b)t/ℏ] Pi_a P Pi_b,
    W_abc=Tr(rho_w Pi_a P Pi_b P Pi_c),
    chi_PP(t,s)=(i/ℏ)theta(t−s) Σ_abc W_abc
       {exp[i((E_a−E_b)t+(E_b−E_c)s)/ℏ]
        −exp[i((E_a−E_b)s+(E_b−E_c)t)/ℏ]}.                    (12)

All initial cross-energy coherences in W_abc are retained. Replacing them
with diagonal populations is a different state and generally changes the
kernel. Total-record dephasing, by contrast, leaves this particular complete
channel unchanged: H,P,j,D commute with total R, so every operator product
in (12) is R-preserving. This exact channel-null statement does not apply to
the distinct writer or record-phase readouts.

Equations (6)–(12) give the complete phase/current/density linear response
and an independent nested-commutator check from the same 16D evidence. The
three preparations and all five inherited ages remain eligible; no positive
contact, special age or passive branch is selected. A new sampling grid is
unnecessary for proving the Ward identity. If a future effective kernel is
specified, these finite sums provide its direct, small, same-state test.

## 5. What the saved result establishes, and the matching it enables

The independently reviewed native contacts at ages 0,.25,.5,1,2 are
approximately .0460068,.0772616,.1015156,.0847068,−.0567654. The factorized
t_hop<n><T> is numerically zero at every retained age, while the actual
correlated contact is not. Those results fix the initial slope in (10).
The last negative value is a signed source moment about an actual
current-carrying state, not by itself a negative kinetic norm, unstable
equilibrium, or negative relaxed modulus. Controls also have correlated
transport response; the effect is not uniquely attributable to record
feedback from this census.

A proposed hard-phase/transport description must match, under an explicit
physical source and phase normalization:

- the same particle/current conservation law and the actual two-time
  chi_PP, equivalently the **complete** K_jphi including its contact;
- the retained state and source-switch prescription, including (9), and
  the source work in (4), rather than an equilibrium state selected later;
- a genuine spatial/boundary response if it claims a phase-gradient
  coefficient. A one-edge pure-gauge source has no independent loop modulus.

In particular, the continuum coefficient alpha cannot be equated to <D>,
nor can an extra contact be added to a native response that already includes
it. Current/contact Ward identities constrain a proposed mapping but do not
provide physical length, volume, photon propagation or the record-clock
dictionary. The constructive next comparison is a specified effective
temporal kernel against (12), supplemented by a separately owned loop or
spatial source; it is not another fit of a single effective mass.

## Evidence identities

All paths below are resident packet files. This note does not alter them.

- `RECORD_ADDITION_RESULTS.json`: SHA-256
  `2b9b19954f137aaf0b60173481fdb9059cda3892ee3c71bd9a6884cbb4b6350a`.
- `native_transport_twist_v001.py`:
  `7defe0dea2425aee64a8f490d79d4c14f83fb284f4f97da03f27f7a3bdcbad75`.
- `NATIVE_TRANSPORT_TWIST_PROTOCOL_V001.md`:
  `247b9227c7ef9ab731f56759a8dd741481a0efbaf03f54fc1316bbe8c5f4e0c6`.
- `NATIVE_TRANSPORT_TWIST_V001_RESULTS.json`:
  `9f29e3d5083d5a03b2e02dca62c2dd90041fa1303a573c55e5a73ed5545775d3`.
- `NATIVE_TRANSPORT_TWIST_V001_FROZEN.json`:
  `1f511788e25dbdf203355f1f0b3de0861d09c4a7e07fe80eab544d15f55a5330`.
- `NATIVE_TRANSPORT_TWIST_V001_RESULTS_REVIEW.md`:
  `4991e72c2b30f5b864ef38d522ae93ddabb3f2952f7551e23aa61b7b917a955a`.
- `../recovered_sources/BS_MICRO_ACTION.md`:
  `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.

The cited numerical result and its audit are inherited evidence. Everything
new here is finite-dimensional operator algebra; no new numerical outcome
is claimed.
