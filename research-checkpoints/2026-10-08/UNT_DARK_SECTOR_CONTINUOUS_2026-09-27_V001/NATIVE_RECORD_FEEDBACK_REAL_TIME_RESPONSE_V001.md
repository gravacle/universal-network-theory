# Native record feedback: static interaction versus real-time response

2026-09-27. Exact single-link analysis within a declared BS restriction. No
new force law, physical metric, relaxation mechanism or formation protocol.

Source: recovered `BS_MICRO_ACTION.md`, BS06/BS09/BS11, SHA256
`00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
All formulas below concern finite native operators. The Hamiltonian clock is
the supplied microscopic clock, not a derived spacetime coordinate.

## 1. One native link and two fixed record occupations

Set N=1, no carriers or graph-dependent ports, all formation couplings off,
and fixed record occupations q_L,q_R in {0,1}. Write s=q_L+q_R. Since the
two node degrees equal the same link projector n=(I-Z)/2,

    H_s = C + epsilon_r s + beta_s n - h X,
    C = 2U d_star^2 + E_other,
    beta_s = Delta + 2U(1-2d_star) - lambda_R s,
    R_s = sqrt(h^2 + beta_s^2/4),       h>0.

The two graph eigenvalues, including the complete common offset, are

    E_(s,±) = C + epsilon_r s + beta_s/2 ± R_s.

Conditional ground energies can therefore have nonzero binary cross-cost
`E_(2,-)-2E_(1,-)+E_(0,-)`. That static comparison does not specify a common
initial graph state, a write operation, or relaxation into the respective
ground states. Different s-ground states cannot be silently substituted for
one actual initial graph state during an abrupt record-history comparison.

## 2. Exact common-state evolution

Declare the same initial graph state in every branch: the normalized graph
ground state |g_0> at s=0. Then evolve branch s with the fixed H_s above.
This is a mathematically explicit comparison of preparations. It is not a
demonstrated native protocol that creates s records instantaneously.

Let delta_s=beta_0-beta_s=lambda_R s and
`n_0=(1-beta_0/(2R_0))/2`. Bloch-vector rotation under the exact two-level
Hamiltonian gives, for arbitrary fixed parameters and time,

    <n>(t;s) = n_0
      + [h^2 delta_s/(4 R_0 R_s^2)] [1-cos(2R_s t/hbar)].

For example, the initial Bloch vector is
`(h/R_0,0,beta_0/(2R_0))`. The rotation axis is proportional to
`(-h,0,-beta_s/2)`. Its z-component changes by
`-h^2 delta_s[1-cos(2R_s t/hbar)]/(2R_0 R_s^2)`, proving the formula.

Thus native incidence responds without graph cooling, but it oscillates.
At fixed finite size, this calculation supplies no convergence to the new
conditional ground expectation `(1-beta_s/(2R_s))/2`.

The branch's complete conserved energy in this common initial state is

    <H_s> = E_(0,-) + epsilon_r s - lambda_R s n_0.

It differs from E_(s,-) by its explicitly retained excitation energy. If a
physical write or control change is used to prepare the comparison, its energy
must come from the completed internal donor/source/controller ledger. The
formula does not declare a free write or an arbitrary reset of energy zero.

## 3. The retarded response is a graph response, not record motion

Around a fixed ground state with coefficient beta and
`R=sqrt(h^2+beta^2/4)`, perturb the graph by `-f(t)n`, where f has energy
units. With the response convention

    chi_nn(t) = (i/hbar) theta(t) <[n(t),n(0)]>,
    delta<n>(t) = integral chi_nn(t-t') f(t') dt',

the exact transition matrix element and causal kernel are

    |<excited|n|ground>|^2 = h^2/(4R^2),
    chi_nn(t) = theta(t) h^2/(2 hbar R^2) sin(2Rt/hbar),
    chi_nn(omega) = (h^2/R)/[4R^2-(hbar omega+i0^+)^2].

The Fourier convention is `integral_0^infinity dt exp(i omega t) chi(t)`.
Consequently

    chi_nn(0) = h^2/(4R^3)
             = -d^2[beta/2-R]/d beta^2 > 0.

This relates the conditional ground-energy curvature to the zero-frequency
graph response. For a small suddenly applied constant f,

    delta<n>(t) = f chi_nn(0)[1-cos(2Rt/hbar)] + O(f^2).

It is not a damped approach to the static answer. An adiabatic or dissipative
physical realization would need its own control/state assumptions and energy
accounting. All q_v remain conserved in this hold; nonzero graph susceptibility
is fully compatible with a zero retarded response of fixed-label record density.

## 4. A shared illustrative coefficient set

Take N=1, U=lambda_R=1, Delta=3, d_star=1, h=1/2,
epsilon_r=2, no carriers or ports, and E_other=0. Energy and time units are
explicitly those of this finite model. The inactive carrier hopping coefficient
can be set to zero, so BS13 has positive margin one, and each local record
insertion has energy operator `2-n >= I`.

Here beta_s=1-s, C=2, and the exact conditional ground energies are

    E_(0,-) = (5-sqrt(2))/2,
    E_(1,-) = 7/2,
    E_(2,-) = (11-sqrt(2))/2.

The binary interaction is `1-sqrt(2)<0` while both record additions still
cost positive energy. The common-state real-time comparison instead has

    n_0 = (1-1/sqrt(2))/2,
    <n>(t;1) = n_0 + [1/(2sqrt(2))][1-cos(t/hbar)],
    <n>(t;2) = n_0 + [1/(2sqrt(2))][1-cos(sqrt(2)t/hbar)].

These expressions were derived analytically; no numerical time evolution or
claim of a measured relaxation time is attached to them. The coefficients
are selected to expose the mechanism, not fitted to a dark-sector target.

## 5. Negative record cross-cost is not yet directional probe attraction

There is also a simple native limitation in this one-link geometry. In the
one-carrier subspace, use tau_x to exchange carrier positions L and R. BS09
and BS11 give `T=tau_x` and `J^2=I` in that subspace, so the complete carrier
addition is

    H_carrier_addition = epsilon_psi I + lambda_J n I - t_hop n tau_x.

The Hamiltonian commutes with tau_x. Moving the single occupied record from
L to R also leaves it unchanged, since feedback depends only on q_L+q_R.
For the same initial graph density rho_g, the full propagator has carrier
blocks `[A B; B A]`; either direction's inclusive transfer probability is
`Tr(B rho_g B^dagger)`. Thus link enhancement alone supplies no preference
for motion toward the occupied endpoint in this one-link example.

This statement retains carrier backreaction; the earlier carrier-free quench
formula is not reused as though the added carrier left the graph unchanged.
For the illustrative Delta and lambda_R, a prospective nonzero carrier hopping
with `|t_hop|<1` retains a positive BS13 margin; no such new run is performed.

Larger, physically anchored network comparisons may have directional responses.
They must compare actual inclusive carrier currents/readouts and own any
relational separation used. Neither conditional binding nor increased link
occupancy alone establishes a force, a physical pressure or a dark component.
