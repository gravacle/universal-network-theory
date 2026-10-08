# Can a local probe distinguish network expansion from refinement?

2026-09-29. New analytical operational test for the connected-subdivision
candidate. No numerical worker, cosmological fit, native coefficient change
or assertion that the BS composition layers are physical space.

## Result

Yes, once the probe coupling, inertia and clock standard are independently
calibrated. A local gapless probe distinguishes three physically different
operations on the SAME subdivided graph:

1. Adding identical physical segments increases static resistance and
   low-frequency propagation time.
2. Rescaling only segment conductance can preserve static response while
   still changing timing and inertia.
3. Refining the representation of a fixed physical interval must also
   repartition its kinetic measure. Its long-wavelength continuum response
   can then converge without increasing the calibrated interval length.

None of these physical assignments follows from the topological subdivision
alone. An exact finite-frequency boundary response additionally detects the
internal degrees of freedom even when static conductance matches. This is a
small operational discriminator, not a proof that a sequence of subdivisions
is a cosmological scale factor or supplies a spacetime metric.

## 1. Explicit local probe and standards

Declare a weak classical scalar readout field on an undirected incidence
graph, with independent positive calibrated inertias mu_v and link stiffnesses
c_e. Its action and energy are

    S_probe=(1/2)*integral dt [sum_v mu_v*phi_dot_v²
                            -sum_(uv) c_uv*(phi_u-phi_v)²],
    H_probe=sum_v pi_v²/(2mu_v)
                         +(1/2)*sum_(uv) c_uv*(phi_u-phi_v)². (1)

There is no onsite mass term: uniform phi has zero restoring force. On an
infinite regular chain this gives an acoustic gapless branch. A finite
Dirichlet resonance is a boundary/size gap, not an inserted mass. This is a
declared local probe port, NOT the BS qutrit carrier Hamiltonian or a proof
of photons, Lorentz invariance or the physical speed of light. Its classical
weak-amplitude approximation neglects graph backreaction only at leading
probe order; a closed implementation must include its work and energy.

Time t is measured against a specified external/controller clock or a
separately qualified relational reference. Meaningful comparisons use
dimensionless ratios such as omega_res/omega_ref, c_eff/c_ref and
omega_ref*t_delay. If the reference clock changes with N, its measured rate
must be retained; rescaling both clock and ruler does not by itself establish
observable expansion. The finite native record-phase result supplies a
candidate reference to test, not an already calibrated universal standard.

The equation mu_v*phi_ddot_v+sum_u c_vu*(phi_v-phi_u)=0 follows from (1).
All couplings are local on the graph. A narrow-band acoustic propagation
time is meaningful below; no exact relativistic causal cone is inferred
from a finite system of coupled ordinary differential equations.

## 2. Static series matching is exact but only static

For a three-segment path between retained endpoints 0,3, minimizing its
potential energy over phi_1,phi_2 gives a common flux F and

    phi_0-phi_3=F*(1/c_1+1/c_2+1/c_3),
    c_eff=(1/c_1+1/c_2+1/c_3)^(-1).                       (2)

This is the Laplacian Schur-complement boundary reduction. Its general
weighted-graph form is the standard Kron reduction described by
[Dorfler and Bullo](https://arxiv.org/abs/1102.2950). The dynamic extensions
and physical-calibration comparison below are derived directly from (1);
the cited static result does not supply a native distance assignment.

Three conductances equal to the old c give c_eff=c/3. Three equal to 3c
give c_eff=c. The latter matches old endpoint potential energy after
minimization but does not remove the kinetic energy of new coordinates.
No minimization is asserted to occur spontaneously: preparing or relaxing
the probe into its static solution requires its own source/work protocol.

## 3. Exact dynamic boundary map exposes the new inertia

At a harmonic frequency omega, partition the weighted graph Laplacian K
into boundary B and new internal I coordinates. Let M_I be their positive
diagonal inertia matrix. Away from its Dirichlet poles, eliminating the
internal amplitudes gives the boundary stiffness map

    Lambda(omega)=K_BB
           -K_BI*(K_II-omega² M_I)^(-1)*K_IB.             (3)

The total boundary force also includes -omega² M_B*phi_B. Boundary inertias
must be included or explicitly held fixed in any comparison.

For three equal new segment stiffnesses c_s and two equal internal inertias
mu, equation (3) is explicitly

    D=(2c_s-mu*omega²)²-c_s²,
    Lambda=c_s I_2-(c_s²/D)*
                    [[2c_s-mu*omega², c_s],
                     [c_s, 2c_s-mu*omega²]].             (4)

The two internal Dirichlet resonances are

    omega_1²=c_s/mu,       omega_2²=3c_s/mu.

The first is visible in the symmetric boundary channel, the second in the
antisymmetric channel. Both couple to the boundary. Setting c_s=3c makes
Lambda(0)=c[[1,-1],[-1,1]], but (4) is still frequency dependent and has
these poles. It is not the old massless spring at nonzero frequency.

The low-frequency expansion is particularly diagnostic:

    Lambda(omega)=c_eff*[[1,-1],[-1,1]]
                         -omega² M_added+O(omega^4),
    M_added=(mu/9)*[[5,4],[4,5]].                         (5)

This positive added inertia is independent of the common c_s. It is obtained
by inserting the static profiles phi_1=(2phi_0+phi_3)/3 and
phi_2=(phi_0+2phi_3)/3 into their kinetic energy. Its eigenvalues are mu and
mu/9. Changing only the two endpoint diagonal inertias cannot cancel its
off-diagonal entry. Even a separately adopted compensating kinetic matrix
would at most match a finite number of low-frequency terms, not remove the
two accessible poles of this finite positive-inertia path.

More generally, put S=K_II^(-1/2) M_I K_II^(-1/2) and
A=K_II^(-1/2) K_IB. Then M_added=A^dagger S A and the remainder in (5) is

    -omega^4 A^dagger S²*(I-omega² S)^(-1)*A.

If omega²<omega_D²=1/||S||, its norm is at most

    omega^4*||M_added||/(omega_D²-omega²).                 (6)

This supplies a declared accuracy window for a static approximation. It
does not justify eliminating the new coordinates near their resonances.
The internal Dirichlet stiffness is positive for a connected positive path
with fixed boundary; no inverse of a whole-graph zero mode was used.

## 4. Repeated subdivision separates two operational limits

Let q be the number of equal segments along an originally anchored route.
Repeated three-way subdivisions give q=3^k if every segment is subdivided at
each stage. For a uniform chain with segment stiffness c_q, interior inertia
mu_q, and fixed endpoint amplitudes, the exact interior frequencies are

    omega_j²=4(c_q/mu_q)*sin²[j*pi/(2q)],
    j=1,...,q-1,
    c_eff=c_q/q.                                         (7)

This is obtained by substituting the discrete sine eigenvectors into the
equation from (1). In the long-route/long-wavelength limit,

    omega_1 approximately (pi/q)*sqrt(c_q/mu_q),
    t_acoustic approximately q*sqrt(mu_q/c_q).            (8)

The time is a low-frequency travel scale or packet delay, not an exact
first-arrival time on a discrete graph.

For an independently calibrated segment length a_q, the infinite-chain
dispersion and group velocity are

    omega²=4(c_q/mu_q)*sin²(k*a_q/2),
    v_group=a_q*sqrt(c_q/mu_q)*cos(k*a_q/2).               (9)

These lead to three distinct, testable choices:

| Declared operation | Segment calibration | Static route stiffness | Long-wave route time |
|---|---|---|---|
| Add identical physical cells | c_q=c_0, mu_q=mu_0, a_q=a_0 | c_0/q | q sqrt(mu_0/c_0) |
| Match static response only | c_q=q c_0, mu_q=mu_0 | c_0 | sqrt(q) sqrt(mu_0/c_0) |
| Refine a fixed calibrated interval | c_q=q c_0, mu_q=mu_0/q, a_q=a_0/q | c_0 | sqrt(mu_0/c_0) |

The third row is the discretization of a fixed continuum interval of length
a_0, tension T and inertial density rho, with c_q=T/a_q and mu_q=rho*a_q.
Endpoint half-cell weights and any other boundary mass must be repartitioned
consistently. Keeping old endpoint weights while simply adding positive
interior mass is NOT that refinement prescription. For fixed physical k,
(9) then converges to omega²=(T/rho)k², with errors O(k² a_q²) relative to
the continuum dispersion. It is convergence under a declared calibration,
not exact dynamic equality of every finite q.

The first row instead keeps physical local cell calibration unchanged. Its
route length, resistance and packet time grow relative to the unchanged
clock/ruler standards. It is operational stretching of this route. That
does not alone prove homogeneous expansion of a volume, isotropic geometry,
a redshift law, an acceleration equation or a cosmological formation rate.

For an arbitrary scaling c_q=c_0*q^alpha, mu_q=mu_0*q^beta, the two
independently measurable scalings are

    c_eff/c_0=q^(alpha-1),
    t_acoustic/sqrt(mu_0/c_0)=q^[1+(beta-alpha)/2].         (10)

Thus preserving the static boundary response fixes alpha=1 but does not fix
beta or the clock response. Preserving both of these low-frequency measures
requires beta=-1 within this particular chain family. It still does not
identify the complete finite-frequency theory or a unique physical metric.

## 5. The probe is part of the growth/work completion

The existing native subdivision map appends finite blank native registers;
it does not specify phi,pi on newly introduced probe coordinates. The port
must separately prescribe their state, coupling and switching. A classical
calibrated change of coefficients has explicit probe work

    partial_t H_probe|canonical
       =-(1/2)*sum_v mu_dot_v*phi_dot_v²
         +(1/2)*sum_e c_dot_e*(phi_u-phi_v)².             (11)

At a discrete insertion, compare complete before/after Hamiltonian energies
and include the new-coordinate preparation and source work. Calling the new
values the harmonic interpolation does not make that operation costless or
unitary. A quantum probe would additionally require its actual state and
absolute energy bookkeeping; zero-point or volume terms are not derived
from the classical static Schur complement.

Likewise, changing native h_N to h_(N+1) during growth changes the native
Hamiltonian and may affect a native clock. The subdivision candidate already
retains that work. It must not be removed by silently assigning a compensating
probe clock rate. A proposed relational calibration can be tested using its
owned clock response, but is an additional calculation, not a consequence of
unchanged topological cycle rank.

## 6. Minimal exact discriminator, without cosmological fitting

The four-node path is already sufficient. Choose the probe constants and
boundary clock/source calibration before applying the growth port. At the
same old endpoints, compare:

* Static boundary force per imposed field difference, giving c_eff.
* The frequency-dependent two-channel boundary map (4), including its added
  inertia and the two internal resonances. No time-propagation worker is
  required to establish those exact formulas.
* The retained supply/controller/probe work, and any measured change of the
  clock standard between the two size sectors.

A fit to a galaxy or Hubble history is not needed: the competing calibrated
assignments make different laboratory-style network predictions. If the
goal is true refinement, compare against the fixed-continuum target within
the controlled low-frequency error (6), not against an asserted exact
equality of finite graphs. If the goal is physical stretching, preserve the
local standards and measure its route ratios, then separately derive whether
the network growth is spatially coherent and obeys a gravitational volume law.

This is a substantive same-port next interface: connected growth can now be
paired with a falsifiable ruler/clock experiment. Topology plus node count
alone cannot settle its physical interpretation, while a locally coupled,
independently calibrated probe can distinguish the proposed interpretations.
