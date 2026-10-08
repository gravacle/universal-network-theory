# Same-field Maxwell light and charging-source contract V001

2026-10-05 UTC. NEW analytical continuation of the frozen physical plate,
shared-link charge and floating-return candidate. No photon mode, numerical
worker, new light-speed fit, native source replacement or metric adoption is
reported. The conditional RGRL/WTC metric architecture remains unchanged.
The new content is a same-field electrostatic reduction, local transfer-current
and source-contact contract, and an exact conditional TEM compatibility identity.

## 1. One physical field inventory and the electrostatic match

Keep the existing port charges eta_v q_* Z_e, actual fifth-island charge
eta_v q_R q_v and floating return Q_0=-q_R sum_v eta_v q_v. Each original
link is encoded once. The passive circuit is realized by the SAME declared
shielded plates and boundaries, not by a second charge model for light.

The nearest dynamical completion class retains an electromagnetic potential
(phi,A), conductor/junction positions, and their material support. In a fixed
laboratory chart with a homogeneous, nondispersive, positive dielectric and
magnetic constitutive law, its field Lagrangian is

    L_EM=integral_domain [epsilon |E|^2/2-|B|^2/(2mu)] d^3x,
    E=-grad(phi)-A_dot, B=curl(A).

Charge, transfer and support are part of the same full action. This formula
specifies a completion CLASS; the frozen circuit has not fixed mu, the complete
domain/connector shapes, or a constitutive frequency window. Vacuum Maxwell is
a particular physical choice, with epsilon0 mu0 c_vac^2=1, rather than an extra
adjustable propagation-speed coefficient. A material dielectric can instead
have a rest frame and dispersion; its optical propagation is not automatically
the common physical metric cone. The relation between vacuum constants is
tabulated by [NIST/CODATA](https://physics.nist.gov/cuu/pdf/all.pdf).

For fixed conductor potentials, the quasistatic field solution has electric
energy (1/2) Vpot^T C_full(F) Vpot. Solving Gauss' law at fixed neutral island
charges and taking the fixed-charge Legendre transform gives

    H_EM,longitudinal(F,Q)=Q^T C_full(F)^+ Q/2
                         =x^T C_rel(F)^-1 x/2=Jcap(F).       (1)

Here C_rel(F) is the frozen sum of actual ideal-plate branch matrices and
C_full=B C_rel B^T with B=[I;-1^T]. The second equality is the previously
proved neutral quotient. Equation (1) includes the return FIELD energy once.
One may retain Maxwell fields and Gauss constraints, or use their longitudinal
reduction Jcap plus the remaining transverse field; adding Jcap a second time
to the unreduced complete field energy double counts this sector. The circuit
Hamiltonian separation between charge energy and magnetic/flux energy is the
standard one described by [Vool and Devoret, sections 2.1 and 3.2.2](https://arxiv.org/html/1610.03438v1).

In the ideal shielded-plate approximation, area and perpendicular gap both
transported by F give exactly the frozen law

    C_b(F)=epsilon A_b(F)/d_b(F)
          =C_b0 det(F)|F^-T n_b|^2.                          (2)

Real fringing, exterior fields or conducting connections may change (1)--(2).
Their inclusion must be tested against the frozen capacitance, not absorbed
into a newly selected kernel or energy reference. The ideal reduction preserves
the already owned six first strain vertices and all direct second contacts.

## 2. Transfer paths, local gauge covariance and electric current

For a native coded transfer O_pi raising destination charge by q_pi and lowering
source charge by q_pi, choose its actual oriented physical path Gamma_pi from
source to destination. The passive gauge convention is

    A -> A+grad(chi), phi -> phi-chi_dot,
    O_pi -> exp[-i q_pi(chi_dest-chi_source)/hbar] O_pi.

Then the Wilson factor, dressed transfer and complete signed coupling are

    W_pi=exp[i q_pi integral_Gamma A.dl/hbar],
    D_pi=W_pi O_pi, H_pi=tau_pi(D_pi+D_pi^dagger).             (3)

This is a local gauge-invariant construction for the stated operator/path;
tau_pi is the ACTUAL signed native coupling, not a newly chosen amplitude.
The scalar potential couples to the complete charges. Local Gauss constraints,
field canonical variables, boundaries and junction material remain in the same
action. A Wilson factor alone supplies neither junction dynamics nor a proof
that the physical low-energy compression preserves tau_pi.

For the fifth-island record copy, O_pi=R_v,x^+ T_0^-eta_v with the actual
carrier/content gate, q_pi=eta_v q_R, and Gamma goes from return to record
island. For incidence n_e:0->1 on an A--B link, Z=1-2n, so the A port loses
2q_* and the B port gains 2q_*: q_pi=2q_*, Gamma is A->B, tau_pi=-h.
The SAME original incidence bit supplies this transfer; no independent pair
of endpoint spins is introduced. Copy has the actual tau_pi=+gamma.

A tagged carrier's ordinary electric charge has not been selected by its
native label. If charged, its spatial hop needs the corresponding Wilson path
with that independently owned charge. Calling it neutral or assigning it q_R
would each be an additional physical dictionary, not a consequence of the code.
For compact U(1), all admitted transfers and backgrounds must obey one owned
charge lattice; q_R/q_* is not chosen here to force commensurability.

Directly from (3), the oriented charge-transfer current is

    I_pi=Q_dest_dot=(i q_pi tau_pi/hbar)(D_pi^dagger-D_pi),
    partial H_pi/partial a_pi=-I_pi,
    partial^2 H_pi/partial a_pi^2=-(q_pi^2/hbar^2)H_pi,
    a_pi=integral_Gamma A.dl.                               (4)

Thus the fixed-amplitude path source has a compulsory second contact. These
are actual electric currents, with charge/time units; the earlier native
current-square coefficient j is not automatically a physical magnetic
inductance or this current squared.

For fixed endpoint positions the line-current distribution

    j_pi(x)=I_pi integral_0^1 Gamma'_pi(s)
                              delta^3(x-Gamma_pi(s)) ds

has div(j_pi)=I_pi[delta_source-delta_destination]. Together with the endpoint
charge rates this proves local charge continuity. Moving endpoints add their
convective current; moving distributed conductor charges require their actual
surface-current completion. The operator current alone does not specify those
conductors or transfer paths. For a fixed path the gauge-invariant voltage is
phi_dest-phi_source+partial_t a_pi; moving paths also retain motional contacts.

## 3. A concrete same-field light-binding identity

One positive plate branch can be extended as an IDEAL homogeneous two-conductor
TEM segment with the same epsilon, mu, gap and width, neglecting fringing and
internal conductor/kinetic inductance. Supply a longitudinal plate tangent t_b
and length ell_b0. Under the same affine F,

    ell_b(F)=ell_b0|F t_b|,
    C'_b(F)=C_b(F)/ell_b(F), L'_b(F)=epsilon mu/C'_b(F).

The actual total magnetic inductance is L_b=ell_b L'_b. Consequently

    L_b(F) C_b(F)=epsilon mu ell_b(F)^2,
    v_b=ell_b/sqrt(L_b C_b)=1/sqrt(epsilon mu).                (5)

The speed in (5) is an implication of the SAME electric and magnetic field
law and physical geometry. It is not an independently fitted clock/ruler
normalization. Standard transmission-line propagation follows from the paired
electric/magnetic energies; see [Vool and Devoret, equations 3.49--3.52](https://arxiv.org/html/1610.03438v1#S3.SS2.SSS2.Px1).
Native and observer independently checked the conditional algebra before this
note. Branches absent at the passive boundary remain absent; no TEM channel is
claimed for a zero capacitance.

Equation (2) fixes epsilon A/d, not t_b, ell_b0, connector/return paths or mu.
Different longitudinal geometries can have the same static capacitance and
different total inductance/mode frequencies. Supplying those geometries makes
(5) a falsifiable binding test. Arbitrary extra inductors chosen to achieve a
desired native speed would change the completion; kinetic/internal inductance
or dielectric dispersion needs its own material action instead.

At finite frequency the return is a physical conductor with distributed charge,
current and field modes. Its single total-charge register n0 and equipotential
C_full are a low-frequency reduction requiring omega ell_return/v <<1 over
the declared operations and sources. The frozen global charge-code identity
does not remove these finite-frequency modes or enable instantaneous signaling.
Restoring them adds genuine magnetic/transverse/support dynamics, not a second
generic electrostatic return self-energy. Shielded finite cavities or isolated
segments need not furnish a global gapless light channel.

## 4. One source/clock/ruler binding obligation

The SAME physical deformation moves plates, conductors, junctions, paths and
readout apparatus. Full first/mixed/second sources therefore differentiate the
complete field/domain action, tau_pi, paths, physical encoder and readout.
For example (4)'s contact survives a field response; a path deformation also
differentiates a_pi. The existing capacitor contacts are precisely the static
fixed-charge part of these sources, not the whole electromagnetic stress.
A fully covariant vacuum action uses the SAME spacetime metric for Maxwell
and the eventual massive probe; a material completion additionally owns its
constitutive rest frame, stress and support. This does not assign old scalar L
to a lapse or replace its preserved all-record midpoint-source law.

The supported release result earned a logical joint record phase on six held
nonendpoints. A physical charged readout instead contains its actual Wilson
path and electromagnetic dressing. Releasing that field adds [H_EM,W_pi] and
path/source contacts to its derivative. Exact logical frequency A_R is not an
automatic full-field proper clock. Conversely, with copying off, conserved
record charge by itself has no finite-frequency transition/emission channel;
the earlier native photon-source null remains. A phase or measurement pulse
is not unaccounted radiation extracted from static record energy. Actual link
transfers can carry the currents (4) and exchange native/field energy.

The first bounded binding decision is an explicit conductor/junction/return
geometry and constitutive frequency window that passes BOTH (1)--(2) and (5),
using fixed native charges/couplings and their current/source contacts (3)--(4).
This earns a same-field charging/light completion in that domain. It still
requires the tagged massive-particle dispersion/source test and complete
metric Ward conditions before common gravity normalization. Gapped internal
record/coordination response may then modify the EXISTING metric through an
owned mixed Schur kernel; no extra massless scalar or graviton entrance is
required by this construction. The RGRL/WTC conditional closure and full
galaxy/expansion/Stage3 scope remain at their established status.

## Frozen resident ancestry

Paths are relative to joint_parent_continuation except the program paths.
These ten byte streams were verified before creating this exclusive note.

| Input | SHA256 |
|---|---|
| LOCAL_RECORD_FEEDBACK_COMPLETE_STRAIN_SOURCE_CONTRACT_V001.md | cc363bf1885917a9beededadb8d49b5d898c951bd54a1e2d2ad6ce5003ebaf63 |
| LOCAL_RECORD_FEEDBACK_FLOATING_RETURN_COMPLETION_V001.md | 255ea0ca5f86cc711cae2ff5e746d8e9b005c2156b934818ded7789f9461f2a4 |
| LOCAL_RECORD_FEEDBACK_DRESSED_RECORD_CHARGE_V001.md | e1742a5a3f7f68734f91c563fe04696b8d7664522e830ed8e261c708b7c83cb1 |
| LOCAL_RECORD_FEEDBACK_SHARED_LINK_DIPOLE_HOLD_V001.md | f461558f0ddf330cad6758824e9d1efed45697c4bc8ad46bf540251fcde71e70 |
| LOCAL_RECORD_FEEDBACK_FIVE_ISLAND_PASSIVE_COMPLETION_V001.md | 124f68b600130afcb3935e11c43c1f939a804892b2794c25f89c29a0892f8693 |
| NATIVE_PHOTON_SOURCE_PATHWAY_V001.md | e6bdd502ae6e31c1bc318a49aea98f5db2c882e82143ca99d849587919fd4049 |
| LOCAL_RECORD_FEEDBACK_FLOATING_CAP_COUNT_COMPLETION_V001.md | 97562eae265f43cef842a5cfb125aede1d8edce2b7b6e21a0292634b3d3a21c7 |
| program-worktree/GRAVITY_RECORD_FIRST_WORKING_THEORY_CLOSURE_V001.md | cf9229586268f054b473b1641085ebafc3bca01fa0691a191cbda923ae1fa7f2 |
| program-worktree/GRAVITY_RECORD_FIRST_DIRECT_PROOF_PLAN_V001.md | 6e4f6b21db461366546e55ff9b68bd337206148b93d7903f228b34bfe356c758 |
| program-worktree/MODEL.md | 3d7c360a38b09fed8f4051c049e838ca561c32ba5dd105dddd80c6aeb7f65607 |
