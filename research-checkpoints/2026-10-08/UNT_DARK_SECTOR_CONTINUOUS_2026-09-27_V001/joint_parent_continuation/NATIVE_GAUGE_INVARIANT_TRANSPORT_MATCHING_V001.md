# Native transport beyond a single-edge contact: invariant sources and matching

2026-09-29. Analytical only. No numerical producer, new state preparation,
alteration of a frozen source, physical-length assignment or fitted coefficient.

## Result

Two exact native experiments distinguish transport from instantaneous contact:
a time-dependent voltage/link-phase drive, and a nonremovable four-cycle phase.
The first is available even on the existing single edge. The second already
has an owned N=2 carrier preparation and an exact short-time interference
coefficient. Neither requires adding a new graph or assuming a ground state.

The native symmetries constrain the complete source response, including its
contacts and boundary state, but do not fix the ratio of temporal and spatial
coefficients called alpha in the conditional phase action. That ratio becomes
identifiable only after a SAME retained phase, state, temporal response and
operational spatial/clock calibration have been matched. A loop response alone
is not that matching.

## 1. Exact source covariance on the actual quantum incidence

Use the invariant one-carrier, copying-off native sector. For each possible
edge e oriented u to v put Aop_e=|v><u| and introduce the explicitly declared
diagnostic source family

    H0[A]=H_inc+epsilon_psi I
       +sum_e n_e {lambda_J(P_u+P_v)
          -t_hop[exp(i A_e) Aop_e+exp(-i A_e) Aop_e^dagger]},
    H[A,V]=H0[A]+sum_v V_v P_v.                         (1)

Record feedback, if present in an owned held state, is retained in the
phase-independent diagonal terms; it does not change the following identities.
A_e is dimensionless and V_v is an energy. Equation (1) names a source, not a
claim that native electromagnetic gauge fields or physical space have emerged.
A realized finite port would need its own controller and work ledger.

For U_chi=exp(i sum_v chi_v P_v), the time-dependent change of representation
psi'=U_chi psi gives

    A_e' = A_e+chi_v-chi_u,
    V_v' = V_v-hbar*chi_v_dot,
    H[A',V']=U_chi H[A,V] U_chi^dagger
                                  +i hbar U_chi_dot U_chi^dagger. (2)

This covariance is exact with the n_e operators and native incidence flips
retained. It is not obtained by replacing links with mean occupations.
The initial density must also transform by U_chi(t0), unless chi(t0)=0 or
the specified state is invariant. Omitting that boundary change creates a
different preparation; the nonstationary Ward comparison must keep it.

The invariant edge drive is

    E_e=hbar*A_e_dot+V_v-V_u.                          (3)

Here E_e has energy units and denotes an oriented source-energy difference,
not a claimed electric field per metre. A static vertex-gradient A with
covariantly followed boundaries is pure gauge. A changing A with V=0 has
nonzero E and is not the same experiment as a static phase twist. On a tree
it can be represented by A'=0 and nonzero scalar V' without removing its
physical source history.

Define the PARTICLE-RATE current

    j_e=(t_hop/hbar)<n_e J_e(A)>,
    J_e(A)=i[exp(i A_e)Aop_e-exp(-i A_e)Aop_e^dagger].

It enters exact continuity with +j_e at v and -j_e at u. Differentiating the
internal native energy, excluding the scalar source term sum V_v P_v, gives

    d<H0[A]>/dt = -sum_e j_e E_e.                      (4)

Indeed partial_A H0=-t_hop*nJ=-hbar*j, while the scalar-source commutator
contributes -sum_v V_v d<P_v>/dt=-sum_e j_e(V_v-V_u).
Equation (4) is gauge invariant when state and source transform together.
If instead j_energy=t_hop<nJ> is used, its right side is
-sum(j_energy/hbar)*E. Explicit switching, source-storage and recoil terms
remain necessary for a complete physical port.

Thus the minimal one-edge follow-on is a SAME initial-state comparison of
two representations of the SAME E(t), retaining boundary phases, carrier
probabilities, current and (4). It checks actual dynamical transport and its
work, rather than interpreting <H_AA> alone as a relaxed spatial stiffness.
The separate nonstationary Ward derivation supplies the exact response-kernel
and initial-boundary cancellation; no new one-edge run is required here.

## 2. A nontrivial loop already exists in the owned input inventory

Use the previous native carrier-ruler N=2 preparation: blank noncarrier
registers, all four incidence links occupied (mask 15), and one carrier at
L0. This is an existing declared preparation, not a new phase-aligned or
ground-state replacement. The comparison tree (mask 11) is also already
owned. Both used t_hop=1/2, lambda_J=1/4, epsilon_psi=1 and unchanged native
incidence coefficients.

Orient all four possible links from L_i to R_j. The phase

    Theta=A00-A10+A11-A01                              (5)

is unchanged by (2). Unlike a phase on a lone edge, nonzero Theta cannot be
removed by vertex rephasing. One may represent it by a phase on one edge or
distribute it around the loop; all source contacts and the initial-state
representation must transform consistently. These are diagnostic coupling
phases, not unearned geometric angles or magnetic flux units.

There are two length-two carrier routes from L0 to L1. At the first nonzero
amplitude order their unchanged-incidence contribution is

    <15,L1|U(tau)|15,L0>
      =-t_hop^2*tau^2/(2 hbar^2)
           [exp(i(A00-A10))+exp(i(A01-A11))]+O(tau^3).

Therefore the unconditional arrival probability has the exact leading term

    Pr(L1;tau,Theta)
       =t_hop^4*tau^4/(2 hbar^4)*(1+cos Theta)+O(tau^5). (6)

Native incidence flips remain present. They cannot contribute a carrier
arrival at L1 before two hops, and a changed final incidence sector needs
an additional flip, so they cannot change the displayed fourth-order
coefficient. The conservative remainder notation does not assume more
time-reversal structure than needed. At Theta=pi that coefficient vanishes;
this is destructive two-route interference, not a universal zero at every
finite time with quantum links. The initially missing edge of the owned
tree removes the two-route fourth-order interference. It is not an all-time
tree null because native flips can create the missing route.

There is also an exact state-independent spectral discriminator on the
FULL 64-dimensional N=2 incidence/carrier space:

    Tr H0(Theta)^4-Tr H0(0)^4
                         =8 t_hop^4*(cos Theta-1).     (7)

Only four-hop closed walks can carry this loop phase at order four. There
are four starting vertices and two orientations; their incidence factor
is the product of the four n_e, whose trace is one. Terms containing onsite
energies or incidence flips cannot complete a phase-sensitive carrier loop
at that order. Equation (7) therefore does not freeze the incidence or
discard its diagonal/source energy.

The separately FROZEN cycle control has the elementary spectrum

    E_m=epsilon_psi+2lambda_J
                 -2t_hop*cos[(2pi*m+Theta)/4], m=0,1,2,3. (8)

For example its nondegenerate lower branch near zero phase has curvature
t_hop/8. This is a spectral oracle, not the state occupied by the actual
localized-carrier preparation, and is not the spectrum of the full quantum
incidence system. Equations (6)-(7) already settle the immediate analytical
question: this native system has a gauge-invariant transport/source readout
that is not just the pure-gradient single-edge contact. No new finite toy
simulation is necessary to establish that fact.

## 3. What symmetry constrains and what could identify alpha

For an anchored possible-edge incidence matrix B, source covariance acts as
A->A+B^T chi. Its invariant channels are the history (3), and cycle phases
Z^T A with B Z=0. A uniform V multiplies the conserved carrier count and
does not produce relative transport. Temporal response must therefore use
specified nonuniform charge sources or the relevant collective phase, not
confuse a uniform identity-energy shift with compressibility.

Number conservation gives continuity and Ward identities for the COMPLETE
temporal/current response, including diamagnetic contacts and initial-state
terms. It does not independently choose the finite response function.
Relabeling and content symmetry enforce covariance; they do not supply
boost symmetry, physical isotropy, a length scale or a universal velocity.

There is a direct symmetry counterexample to a coefficient-one claim:
t_hop can vary continuously within the allowed native family, keeping the
same carrier U(1), content and permutation symmetries. At a fixed declared
state, the phase Hessian scales with t_hop while the Berry/charge normalization
hbar sum p_v theta_car_dot is unchanged. The required onsite/current-square
energy and state response must still be counted, but no Ward identity forbids
this change. Consequently those symmetries alone cannot impose alpha=1 or
any particular temporal/spatial ratio.

A meaningful SAME-PHASE effective matching would instead measure/derive
both quadratic coefficients after a specified source quotient and controlled
elimination of other modes. For the candidate hard phase, writing its small
phase perturbation as delta theta rather than V, these are

    K_time = C beta/e_II,
    K_space = C beta*alpha*I/omega,
    K_space/K_time = alpha*cI2.                        (9)

Equation (9) assumes positive occupied e_II and the same action/state used
to define cI2=I e_II/omega. It is not valid by dividing through the exact
single-link affine action e_II=0; that sector retains a density constraint.
A common phase rescaling changes both coefficients together, so their ratio
is independent of that rescaling once the SAME phase is actually identified.
It is nevertheless a physical speed-squared comparison only after spatial
and temporal units and the metric dictionary are owned. Without that mapping
one obtains graph/clock response coefficients, not the dimensionless alpha
relative to a physical relativistic cone.

For an actual nonstationary preparation the primary object is the two-time
kernel, not an assumed frequency-local derivative expansion. A static flux
curvature, an endpoint state-twist Hessian, and a dynamical long-wavelength
coefficient are different limits. A finite native cell's discrete poles do
not by themselves establish a hydrodynamic or spatial continuum limit.

The smallest constructive next matching is therefore sharply specified:
use the same already owned native states and anchored source operators for
the full temporal kernel, continuity/current kernel and nontrivial cycle
response, retaining contacts, absolute onsite energy and source work. Test
whether one controlled retained phase explains them together. Do not select
a new favorable state or insert the coefficient needed for stability. A
successful matched reduction would make (9) an inference; failure would
identify the missing collective/state or physical dictionary, not erase the
exact transport demonstrated by (6).

## Read-source identities

* `NATIVE_RELATIVE_PHASE_TRANSPORT_TEST_V001.md`:
  `6e9cc504ae81841c55d73c84f91239ce407e84455f11efc10a32ed8724d4b45a`.
* `NATIVE_CARRIER_RULER_PATHWAY_V001.md`:
  `4277871cd49f7e45169f3fd7db0b5d49b9b66651f6b4ac257d794a5230254db8`.
* `NATIVE_RULER_SOURCE_AND_NORMAL_FORM_V001.md`:
  `335044ff025cfd831f92ed34574098fb7fe42841047c2b657d40962f6439568c`.
* `../recovered_sources/BS_MICRO_ACTION.md`:
  `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.

These identities specify the mathematical/input provenance. They do not
authenticate a physical source implementation or identify native carrier
phase with the conditional cosmological mode phase.
