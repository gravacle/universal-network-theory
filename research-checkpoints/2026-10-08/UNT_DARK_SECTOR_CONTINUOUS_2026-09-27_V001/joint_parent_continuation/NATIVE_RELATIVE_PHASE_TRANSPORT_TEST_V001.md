# A relative-phase transport operator: exact test, not an adopted repair

2026-09-29. Analytical only. No new operator has been added to the native BS
Hamiltonian or the retained covariant comparison parent. No fit, propagation,
state selection, physical length assignment or numerical producer is used.

## Result

There is a precise leading spatial operator that can change the problematic
relative-clock branch. Its coefficient-one completion turns the hard phase
sector into an ordinary irrotational fluid, while retaining the separate
clock polarization/contact and soft memory. It has positive local phase
kinetic energy on the occupied positive-hardening branch. This is a
**conditional alternative action**, not a proof that the original action
was stable or that UNT supplies its coefficient.

Native BS carrier hopping supplies a genuinely owned phase-stiffness
observable and its complete source-work formula. It does not yet identify
the hard collective phase with the carrier phase, supply a physical metric,
or force the coefficient-one relation. Those are concrete matching tests,
not reasons to insert a coefficient chosen to stabilize the answer.

## 1. The candidate and its exact quadratic meaning

Use the existing conventions c=1, C=2M2/Kb, hard weight beta, normalized
preferred normal u_mu=-partial_mu T/sqrt(-partial T squared), and
P^{mu nu}=g^{mu nu}+u^mu u^nu. The retained hard scalar action is

    L_H=C beta[I U-e(I,h(a))],   U=u.partial theta,
    omega=e0,I>0,   W=C beta I omega,
    cI2=I e0,II/omega>0.

Around the aligned homogeneous background write
T=t+pi, delta theta=omega(t)V, v=V-pi. To quadratic order,

    P^{mu nu}partial_mu theta partial_nu theta
                            =omega² |grad v|²/a².       (1)

The original hard spatial action, up to the other retained metric terms, is

    L_sp/a³ = W|grad pi|²/(2a²)-W grad pi.grad V/a²
             =W|grad v|²/(2a²)-W|grad V|²/(2a²).         (2)

Consequently the prospective operator

    Delta L_alpha=-C beta alpha I/(2omega)
                          P^{mu nu}partial_mu theta partial_nu theta (3)

changes (2) into

    L_sp/a³ = (1-alpha)W|grad v|²/(2a²)
                                   -W|grad V|²/(2a²). (4)

Here alpha is a dimensionless **unmatched transport coefficient**, not a
parameter selected by a numerical outcome. In (3), omega can be defined as
e0,I(I) for this explicit candidate; only its background value enters (1).
An I-dependent coefficient and its nonlinear completion would need their
own matching. Equation (3) alone specifies the displayed derivative order,
not every higher-gradient or nonlinear operator.

For alpha=1, (3) is exactly the quadratic relative-gradient term in

    L_phase=C beta[I sqrt(-partial theta squared)-e0(I)],

since sqrt(-partial theta squared)=sqrt(U²-|P partial theta|²)
=U-|P partial theta|²/(2U)+higher spatial orders on the positive-U branch.
Replacing U by its background omega is valid in this quadratic term. This
nonlinear square-root completion removes the preferred u from the **phase
and e0 part**, not from the complete action: the owned expansion

    -e(I,h)=-e0(I)+chi_B(I) h²/2+O(h⁴)

still supplies KH=beta chi_B to the preferred-clock acceleration. It must
remain once, alongside the explicit soft modes and DeltaU. Deleting KH or
counting it twice is not the proposed completion.

Eliminating the positive-hardening density perturbation in a local frozen
patch gives the phase kinetic term

    W/(2cI2)*(V_dot-Phi)²,

which is positive for I,omega,e_II>0. At alpha=1 its spatial term is the
ordinary negative Lagrangian gradient -W|grad V|²/2. Equivalently the
Legendre transform P_fluid(mu)=I(mu)mu-e0(I(mu)) obeys
P_fluid,mu=I and P_fluid,mu mu=1/e_II>0. This is a derivation within the
**candidate** action, not importing such a fluid as an established UNT mode.
The strictly harmonic e_II=0 limit instead retains the density constraint;
one must not divide by cI2=0.

Keeping local gravity fixed temporarily also makes the remaining contact/
memory energy explicit. For a nonzero spatial wave number p and Phi=0,

    L_pol/C=xdot^T Ms xdot/2-x^T Ks x/2
                   -p*pi_dot*S+KH*p²*pi_dot²/2,
    H_pol/C=xdot^T Ms xdot/2+x^T Ks x/2
                                      +KH*p²*pi_dot²/2. (5)

The mixed term shifts the canonical momentum of pi; it is not negative
kinetic energy. For positive Ms,Ks,KH this local subsystem has positive
energy. This checks compatibility with the retained memory coordinates,
not full nonlinear metric stability or a general constraint count. The
new spatial operator introduces no new preferred-time derivative at this
order in unitary clock gauge.

### The truncated operator is not its all-orders completion

This distinction also follows from exact variations of (3). Write
`s_mu=P_mu^nu partial_nu theta`, holding I and the scalar fields fixed in
the metric variation. Then `partial(s²)/partial g^{mu nu}=s_mu s_nu`, so

    Delta T_mu nu=alpha C beta (I/omega)
                              [s_mu s_nu-g_mu nu*s²/2].

This extra stress has no first-order term around s=0, but has nonzero
energy and anisotropic stress at quadratic order. The exact truncated
phase equation is

    U=e_I(I,h)+(alpha/2)*partial_I(I/omega)*s².

Its phase-dependent preferred-clock variation has coefficient
`I(1-alpha U/omega)s_mu`, in addition to the separately retained
acceleration/polarization variation. At alpha=1 this term vanishes at the
linear/quadratic-action order discussed above, but generally returns at
cubic order in perturbations. The isolated term (3) does NOT remove the
preferred clock at all orders. The square-root action is a distinct
nonlinear completion whose additional gradient terms must be owned; it is
not an identity for the truncated operator.

## 2. It changes the currents, not just a written gradient sign

Put gamma=1-alpha and keep alpha constant for this diagnostic. The phase
current of (3), to the required order, is

    J_theta^mu=C beta[I u^mu-alpha I/omega
                                      P^{mu nu}partial_nu theta].

Thus its spatial component in Newtonian gauge is proportional to
-I grad[alpha V+gamma pi]/a², not the old -I grad pi/a². With
d=delta I/I=delta rho_H/W, p=k/a and U=Phi-pi_dot, the changed linear
equations are

    d_dot=3Psi_dot-p²[alpha V+gamma pi],
    V_dot=Phi+cI2(d+3H V),
    Pcal_dot+2H Pcal=gamma W p(V-pi),
    Pcal=C[S+KH p U].                                  (6)

The soft-mode equation and its memory are retained. Time dependence of KH
and omega is still kept when differentiating these expressions. Equation
(3) has zero linear density, pressure and momentum stress about the aligned
zero-relative-flow background; in unitary gauge it is a spatial-gradient
quadratic with no lapse/shift linear variation. The hard momentum remains
-W partial_i V, and the polarization density remains -p Pcal.

Combining (6) still gives total stress conservation,

    delta rho_D=Wd-pPcal,    delta p_D=cI2 Wd,
    delta rho_D_dot+3H(delta rho_D+delta p_D)
                                    =W(3Psi_dot-p²V).  (7)

At alpha=1 the clock current has no hard relative-flow source, while the
hard current follows V. Polarization can still carry its own initial data.
At cI2=0 the total metric dust interface is preserved by (7); the internal
clock and hard-current evolution are nevertheless different. At finite
pressure, delta p_D=cI2(delta rho_D+pPcal) still records polarization
entropy unless that independent perturbation is actually absent.

### Local dispersion discriminator

In precisely the frozen, weak-field, subhorizon and slow-hard-source window
of the finite-gap note, set A_G=W/(2M2), y=s², and

    q(y)=[KH+b^T(Ks+y Ms)^(-1)b]/Kb,   0<q(y)<1 for y>=0.

The source/metric constraint and (6) give

    (y-A_G+alpha*cI2*p²)d-p²[gamma-q(y)]U=0,
    [q(y)y-gamma*A_G]U-gamma*A_G*cI2*d=0.

Their determinant is

    (y-A_G)[q(y)y-gamma*A_G]
              +cI2*p²[alpha*q(y)y-gamma*A_G(1-q(y))]=0. (8)

Alpha=0 recovers the original pressure/clock branch; it has not been
reclassified as stable. Alpha=1 gives

    q(y)y[y-A_G+cI2*p²]=0.                             (9)

For positive real y, q(y)>0, so the remaining possible growing root in this
local approximation is the ordinary Jeans root A_G-cI2*p². The internal
neutral/memory factors are still present: multiplying by soft denominators
must not erase their poles or source-dark solutions. Equation (9) is not
a proof of a cosmological transfer function or nonlinear stability. It
demonstrates precisely which missing transport changes this local failure.
No physical wave-number, inertia or averaging cutoff is inferred here.

## 3. What background/static conclusions are unchanged

For homogeneous aligned flow, and also a zero-shift static branch
T=t, theta_j=mu_j t, the projected phase gradient is identically zero.
The new term and its first variation then vanish. The owned homogeneous
e(I), pressure, dilution, endpoint DeltaU, and the static phase condition
N omega=mu are unchanged. The existing central-static coefficients and
finite-spectrum center signs cannot be improved by merely naming (3).

Perturbations with relative flow are different: their current, clock
exchange, propagation and admissible initial conditions must be recomputed.
The old coherent high-gap pulse is not automatically a phase-balanced
state of this alternative action. Rapid averaging, spatial transport and
the physical dictionary still require ownership.

For comparison only, an explicitly added scalar-mode spatial energy
`m c_s² |D y|²/2` would phase-average to
`c_s² I |D theta|²/(2omega)`, since
`m omega <(partial_theta y)²>=I`. It would also generate amplitude/action
gradient terms and source-gradient connections. Keeping only its phase
piece is a slow-gradient approximation, not an exact new parent. This
illustrates a possible coefficient source; that spatial operator is not in
the already tested uncoupled mechanical parent and is not adopted here.

## 4. The owned BS result: phase work and stiffness without a mean link

In the exact held one-carrier sector, BS07/09/11 give

    H=H_inc+epsilon_psi I
                +sum_e n_e[lambda_J(P_u+P_v)-t_hop T_uv]. (10)

For a fixed incidence basis graph G its compression is

    H_car(G)=epsilon_psi I+lambda_J D_G-t_hop A_G
            =epsilon_psi I+t_hop L_G+(lambda_J-t_hop)D_G. (11)

The identity is exact; frozen incidence is a declared control, not a
replacement of native incidence dynamics. For a pure carrier vector psi,

    <H_car>=t_hop sum_edges |psi_u-psi_v|²
                    +sum_v[epsilon_psi+(lambda_J-t_hop)d_v]|psi_v|². (12)

The second term is compulsory. Inherited t_hop=1/2 and lambda_J=1/4 do
not cancel it. Even on a regular graph its uniform band-bottom energy is
part of the source/volume ledger, not free energy to subtract from gravity.

The stronger source identity does NOT require incidence freezing, a pure
carrier or any factorization. Orient e from u to v, set

    A_e=|v><u|,  T_e=A_e+A_e^dagger,
    J_e=i(A_e-A_e^dagger),
    U_phi=exp[i sum_v phi_v P_v],  dphi_e=phi_v-phi_u.

For the actual joint density matrix rho let C_e=<n_e A_e>. A diagnostic
state twist rho_phi=U_phi rho U_phi^dagger gives the exact energy change

    Delta E=t_hop sum_e[<n_e T_e>(1-cos dphi_e)
                                      +<n_e J_e> sin dphi_e],
    Delta E=t_hop sum_e <n_e J_e>dphi_e
                 +(t_hop/2)sum_e <n_e T_e>dphi_e²+O(dphi³). (13)

All diagonal incidence, occupation, record-feedback and current-square
terms commute with these carrier occupation twists in this held sector.
The same formula extends to the native content-preserving transfer with
occupation-phase twists, provided additional noncommuting ports are
included in the ledger rather than omitted.

The exact phase Hessian is a graph Laplacian with edge coefficients

    w_e^phase=t_hop <n_e T_e>=2t_hop Re C_e.              (14)

It has the constant-phase zero direction from total carrier number
symmetry. Its sign is STATE DEPENDENT. A current-carrying state also has
the linear work term in (13). Negative edge weights need not by themselves
make the entire constrained Hessian negative, but there is no automatic
positive-Hessian theorem for an arbitrary formed state. In particular,
`<n_e T_e>` cannot be replaced by `<n_e><T_e>`.

On a fixed graph with phase-aligned pure amplitudes sqrt(p_v), (14) becomes
2t_hop sqrt(p_u p_v)>=0. This is a legitimate comparison state and minimizes
phase energy at fixed amplitudes for positive t_hop. It is not evidence
that the actual network preparation selected or relaxed to that state.

Applying a twist is not free: its endpoint native energy debit is (13).
A real finite-duration phase operation needs a source/controller, its
switching work and recoil. With explicit time-dependent ports the exact
work is integral Tr[rho partial_tau H] d tau. A declared formal U_phi does
not itself construct that port or identify boundary tau with proper time.

### Fixed-state contact is not automatically a relaxed stiffness

There is a particularly sharp null test on the retained single edge. The
formal Hamiltonian source `H(phi)=U_phi H(0) U_phi^dagger` has

    H'(0)=-t_hop nJ,
    H''(0)=+t_hop nT,

where J is the current of (10)-(13). Equivalently,
`H'(0)=i[P_v,H]=-t_hop nJ` and
`H''(0)=-[P_v,[P_v,H]]=t_hop nT`. These source signs are opposite to the
first derivative of the fixed-H state twist (13).

The complete source family is unitarily equivalent: its spectrum and every
covariantly followed state energy are independent of phi. Thus a nonzero
fixed-state contact `<H''>` is compatible with exactly zero *total static
relaxed energy curvature*. For a nondegenerate stationary eigenbranch the
ordinary second derivative identity displays the cancellation explicitly:

    0=E_n''=<n|H''|n>
                        +2 sum_(m!=n) |<m|H'|n>|²/(E_n-E_m). (14a)

Degenerate branches require their full projectors, not singular individual
denominators. The actual formed states need their nonstationary two-time
response; a ground state or dephased stationary density cannot be silently
substituted to apply (14a).

A vertex-gradient hopping phase is similarly pure gauge on a larger graph
when all vertex/boundary states can co-transform. Fixed boundary phase,
nontrivial cycle holonomy, finite-time electric/source forcing or a retained
collective order parameter changes that question and must be specified.
The native endpoint state-twist work (13) is real; calling the Hamiltonian
source pure gauge does not make that fixed-H preparation free. Conversely,
using its contact alone as a persistent macroscopic stiffness omits the
state/current response. These two experiments must not be conflated.

## 5. The missing coefficient is a testable matching, not a convention

The native carrier's canonical phase can be chosen as
theta_car=-arg(psi): its Berry term is +hbar sum_v p_v theta_car_dot.
This fixes the sign and normalization with the owned carrier number. It
does not identify theta_car with the hard collective theta or the native
record phase. Such an identification must reproduce their source/current
responses and must not count the same excitation energy twice.

Given an independently established physical edge displacement ell_e and
volume V_phys, the native quadratic stiffness tensor would be

    rho_s^{ij}=(1/V_phys) sum_e w_e^phase ell_e^i ell_e^j.

If theta=Z theta_car were justified by the canonical/source map, the
leading candidate coefficient would require

    rho_s^{ij}/Z² = C beta alpha I/omega * g_spatial^{ij}. (15)

Neither the isotropic metric/edge displacement, physical volume, clock
normalization, shared hard-phase identification nor alpha=1 follows from
the graph Laplacian identity. Native hopping also contains amplitude-gradient
energy and degree-dependent onsite energy; eliminating these needs its
own controlled reduction. Matching only a spatial sign is insufficient.

For emphasis, in the held copying-off BS sector the LOCAL record occupation
phases commute with H: each q_v^r is conserved. A record-phase twist alone
therefore costs exactly zero held energy, even in a correlated state.
Native carrier hopping supplies carrier-phase transport, not an immediate
stiffness for the record-raising phase clock. A collective emergence/port
mechanism connecting these channels must actually be derived or tested.

## 6. Smallest owned test and decision rule

No larger graph or galaxy refit is needed first. On every already retained
native preparation and age, compute the actual <nT> and <nJ> for the owned
carrier edges. Check (13), continuity and the full phase Hessian under
declared carrier-number twists, while retaining the record-phase null.
This determines whether those states possess positive fixed-state phase curvature,
current-driven linear work, or negative/neutral directions. It introduces
no preferred sign gate or phase-alignment reset.

Also retain the source-conjugacy/current-response null (14a), or its exact
unitary form for the actual states. A positive instantaneous contact is
not a sufficient success criterion for an effective transport term.

If that native channel is proposed as the hard phase, the next necessary
matching is its temporal canonical/source kernel AND its spatial Hessian
in the same state, including eliminated-mode memory, absolute onsite energy
and physical metric/volume calibration. Only then can (15) determine alpha
or show that the candidate operator is absent/inadequate. A successful
alpha=1 conditional fluid completion is a precise route to investigate,
not an authorization to insert a rescuing term into the frozen action.

## Source identities

* `../recovered_sources/BS_MICRO_ACTION.md`:
  `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
* `NATIVE_CARRIER_RULER_PATHWAY_V001.md`:
  `4277871cd49f7e45169f3fd7db0b5d49b9b66651f6b4ac257d794a5230254db8`.
* `NATIVE_RULER_SOURCE_AND_NORMAL_FORM_V001.md`:
  `335044ff025cfd831f92ed34574098fb7fe42841047c2b657d40962f6439568c`.
* `FINITE_GAP_FLRW_PRESSURE_CLOCK_INTERFACE_V001.md`:
  `a8d0c3773eb3f95d5920e3ba7c83822c1af6ae1d0c72b8ec36cb533eb9ba6f94`.
* `HARD_LIMIT_NONVACUUM_SCALAR_INTERFACE_V001.md`:
  `c501fc2aeebe0cf389ad9c21c5c7fdd3240209a1d9dd0ae710ed45d67bb8003d`.
