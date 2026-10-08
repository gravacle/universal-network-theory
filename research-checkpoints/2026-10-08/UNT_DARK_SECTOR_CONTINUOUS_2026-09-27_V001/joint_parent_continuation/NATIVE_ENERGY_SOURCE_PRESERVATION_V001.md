# Energy source preservation in the native carrier phase reduction

2026-09-30. Analytic extension of the existing collective carrier candidate,
not a new simulation, formation law, metric derivation or continuum claim.

The carrier conditional-state reduction already preserves carrier-density
source directions. It does **not** thereby preserve the adopted energy-lapse
or volume sources. This distinction is decidable without another response
grid: the energy-dipole source has strictly nonzero complementary-space
leakage at every already specified blank initial state. The exact reduced
memory can retain that leakage; a source-independent local carrier action
cannot simply discard it.

## Existing phase result and exact formation convention

The held-record phase null and constructive carrier/link alternative are
already derived in `NATIVE_COLLECTIVE_CARRIER_PHASE_CANDIDATE_V001.md`
sections 1–4 and `NATIVE_RELATIVE_PHASE_TRANSPORT_TEST_V001.md` section 4.
They are not new findings here. With copying **into** retained records and
noncommuting ports off, BS10–11 give `[H,q_v^r]=0` for each record register.
Copying from a record **into a reservoir** has record projectors as its
control and still commutes with that record's occupation. In contrast,
writer-to-record and carrier-to-record transitions do not commute with it.

For `U_r=exp(-i sum_v theta_v q_v^r)` and `|psi>=U_r|psi_bar>`, a raising
operator with `[q_v^r,A_v]=A_v` has
`<A_v>_psi=exp(i theta_v)<A_v>_bar`. The exact Schrödinger action contains

    i hbar <psi|psi_dot>
       = hbar sum_v <q_v^r> theta_v_dot
                              +i hbar <psi_bar|psi_bar_dot>.       (1)

The chart must fix its redundant split between theta and psi_bar; a vanishing
raising amplitude does not define an operational phase. Static independent
record rotations leave the held energy unchanged for **any** state, including
the actual coherent formed states. This is an operator symmetry, not a claim
of local gauge redundancy. Symmetry-preserving exact elimination retains the
static Ward null. A fixed non-invariant preparation, boundary, reference or
source must be retained as such in an effective functional; omitting its
response is not a derivation of spatial record-phase stiffness. Even such a
preparation does not change the exact fixed-H state-orbit energy null.

For the finite autonomous apparatus, define `R=qL+qR`,
`Aplus=A_L+A_R`, `K=Aplus+Aplus^dagger`, and `s=exp(Q)`. The formation term is

    Hform,X = g eta_X(Q) Pc K,
    eta_A=s^-1,                 eta_B=1.

All other declared terms commute with R. Either the count commutator or the
global-theta Euler variation of (1) therefore gives exactly

    hbar d<R>/d tau
       = -partial_theta <U_r^dagger Hform,X U_r>_bar
       = 2g Im<eta_X(Q) Pc Aplus>.                             (2)

The derivative holds psi_bar fixed; the expectation on the last line uses
the actual full state. In particular,
the A factor cannot be dropped or factorized. Equation (2) describes reversible
controller-referenced transfer, not permanent accumulation, a SEALED verdict,
an attractor, or the spacetime preferred-clock equation. The held local phase
rate can depend on record/incidence correlations without supplying its own
spatial transport action. A composite carrier/link/record clock is not excluded.

## Which sources the existing retained map preserves

At an actual pure-state age with nonzero carrier probabilities, use exactly
the existing isometry

    W|v>=|v>|chi_v>,    P=WW^dagger,    Qperp=1-P,
    Hret=W^dagger H W,  LH=Qperp H W.                         (3)

Unoccupied carrier vertices are excluded from this chart. No conditional
state is invented for them. The full initial vector belongs to P, but that
does not make P invariant under H. For any physical source insertion F,

    LF=Qperp F W.                                           (4)

The necessary and sufficient condition that F preserve the entire retained
subspace is `LF=0`. Each carrier projector P_v preserves it, which explains
the exact chemical-potential source property in the earlier candidate.
There is no analogous general theorem for complete node energy, lapse or
volume sources.

For the **present two-endpoint 96D dipole only**, the symmetrically assigned
hopping cancels from the energy difference, so `[Z,P_v]=0`. Hence

    (LZ^dagger LZ)_uv
       =delta_uv [<chi_v|Z_v^2|chi_v>-<chi_v|Z_v|chi_v>^2]. (5)

This is a conditional variance, not a variance in a substituted ground state.
It need not vanish for a formed conditional state. Equation (5) must not be
generalized to arbitrary spatial energy dipoles: midpoint-weighted hopping
can give off-diagonal carrier blocks on another graph. Equation (4) remains
valid without that restriction.

## An exact source discriminator at the existing blank preparation

Retain `gamma0=ell0/(2c^2)` symbolically; no physical numerical value is set.
Let `Ztilde=Z/gamma0`. At each specified initial state
`|0>=|Q_j,C=1,rL=0,rR=0,n=0,carrier=L>`, W has rank one. Write |Lr> and
|Rr> for the same vector with only its left or right record flipped. The
already owned dipole operators give

    Ztilde_A |0> = -|0>+g|Rr>-g|Lr>,
    Ztilde_B |0> = s_j[-|0>+g|Rr>-g|Lr>].                  (6)

These three vectors are orthogonal. Thus, exactly,

    ||Qperp Ztilde_A |0>||^2=2g^2,
    ||Qperp Ztilde_B |0>||^2=2g^2 s_j^2.                  (7)

At inherited g=1 these are 2 and `2s_j^2`, respectively. A small impulse of
integrated source strength epsilon produces complementary amplitude
`-i epsilon Qperp Z|0>/hbar+O(epsilon^2)`. Initial zero dipole impulse
**moment** `S_Z=<[Z,[H,Z]]>/hbar^2=0` does not contradict this nonzero
source-vector leakage: a commutator moment is not the variance (7).
Because this Z commutes with every carrier projector, the instantaneous
kick itself preserves carrier probabilities. Leakage changes conditional
environmental directions; its subsequent dynamical effect must be retained,
not equated with an immediate carrier transfer.

The owned dilation insertion is `B_eta=-H_eta`. The same rank-one check,
using the frozen h=1 incidence flip, also gives

    ||Qperp B_eta,A |0>||^2=s_j^-2(1+2g^2),
    ||Qperp B_eta,B |0>||^2=0.                            (8)

For A the insertion acts as

    B_eta,A |0>=s_j^-1[3|0>-|incidence flipped>+g|Lr>+g|Rr>].

For B, n annihilates the initial transport term and only
`-3Eb s_j^3|0>` remains. B's initial volume-source preservation is not a
claim about later formed states, the Hamiltonian, or the dipole source.

## The required source terms in the exact memory

Keep W fixed at its declared matching age and take the affine source family
`H(a)=H+aZ`. Define `Zret=W^dagger ZW` and `LZ=Qperp ZW`. The exact projected
equations for `|psi>=W phi+xi`, `xi=Qperp xi`, are

    i hbar phi_dot=(Hret+a Zret)phi+(LH^dagger+a LZ^dagger)xi,
    i hbar xi_dot=(Qperp H Qperp+a Qperp Z Qperp)xi
                                                   +(LH+a LZ)phi. (9)

Although xi initially vanishes, `a LZ phi` is an explicit source forcing.
Elimination must retain both source-dependent end couplings and propagation
inside the complementary subspace. If an initial state outside this owned
P chart is used, its initial xi additionally supplies the retained forcing
`(LH^dagger+a(t)LZ^dagger) U_Q(t,t0) xi(t0)`; it cannot be set to zero by
convention. For a fixed constant source, put
`Rz=(z-Qperp H Qperp)^-1` on Qperp. At a=0 the exact resolvent insertion is

    partial_a Heff(z)=Zret+LZ^dagger Rz LH+LH^dagger Rz LZ
                  +LH^dagger Rz (Qperp Z Qperp) Rz LH.    (10)

This derivative holds at fixed z, with
`Heff(z)=Hret+LH^dagger Rz LH`. An on-shell nondegenerate real eigenbranch
away from complementary poles instead obeys

    dE/da = [phi^dagger (partial_a Heff) phi]
                   /[phi^dagger (1-partial_z Heff) phi]. (11)

The denominator is compulsory. Equation (11) is not an equilibrium replacement
for the actual nonstationary formed states; their evolution uses (9).

The same formula applies with F in place of Z for another affine source,
with its actual sign convention. Nonlinear physical source contacts must
also be retained. Even an affine microscopic source generates higher reduced
source derivatives through the resolvent; these are not an independently
adjustable bare contact. A source-dependent W additionally requires its
derivatives and, in time evolution, its connection.

The constructive decision is therefore exact and limited: use the existing
same-state carrier reduction **with** its energy/volume source-dependent
memory, or establish a controlled approximation that bounds these terms.
No source-independent chemical-potential reduction can be promoted solely
because its hopping phase curvature has a favorable sign. These identities
preserve the full signed response, including negative moments where present;
exact elimination cannot convert them into the rejected positive fixed-inertia
identification by dressing the source. A different controlled frequency/time
window or state requires explicit hypotheses and error bounds. These identities
do not themselves derive a continuum, an action-hardening coefficient,
physical clock/metric mapping, galaxy polarization, a0 or vacuum stress.

## Source identities

- `../recovered_sources/BS_MICRO_ACTION.md`, BS08–12:
  `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
- `NATIVE_COLLECTIVE_CARRIER_PHASE_CANDIDATE_V001.md`:
  `f3dad63532285add3f890b0c15e9fad4c4968226904e66cf43e6e110966eb6fa`.
- `NATIVE_RELATIVE_PHASE_TRANSPORT_TEST_V001.md`:
  `6e9cc504ae81841c55d73c84f91239ce407e84455f11efc10a32ed8724d4b45a`.
- `NATIVE_AUTONOMOUS_VOLUME_FORMATION_V001_PROTOCOL.md`:
  `724f8d8c4a7bbcc7ce4ba9fa37f750e92d96b732db78ef1cc1347fcd52a7a7d5`.
- `NATIVE_ENERGY_DIPOLE_GRAVITY_BRIDGE_V001.md`:
  `81b3c455d761667e2645117699e8986c7030290de8b54bc45879112237d2db96`.
