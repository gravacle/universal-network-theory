# Complete charging strain and the remaining native source contract

2026-10-05 UTC. NEW bounded physical-placement candidate and exact analytical
contacts. Root proposed the plate geometry before the following algebra;
native and observer independently checked the complete first jet. This note
does not adopt a universe, select capacitor values, fit an energy function,
modify a sealed parent, or report a new numerical calculation. Final text
review remains a separate boundary.

## 1. Declared physical geometry, charges and reference

Retain the faithful shared-link dipole and floating-return code on a supplied
simple balanced bipartite q4 support. Each original incidence spin is encoded
once. The actual star charges are x_a=eta q_* Z_a and x_R=eta q_R q, with
q^2=q, c=-sum_a Z_a/2, and the same total neutral return charge as in the
floating-return note. No independent endpoint bits or omitted return energy
are introduced. The unstrained five-island elastance is

    E5=[[ed I4+em 11T, gcap 1],[gcap 1T,eR]],
    U=2 q_*^2 em, lambda=2 q_* q_R gcap, AR=q_R^2 eR/2,
    Jcap=sum_v[U c_v^2-lambda q_v c_v+AR q_v+2 q_*^2 ed I].       (1)

The passive capacitor weights C_m,C_pr,C_gp,C_gR are exactly those in the
five-island note. Values and charge units remain unselected. The q-dependent
AR cost and absolute self term are retained. A common fixed-q1 reference
comparison cannot remove them from deformation or count work.

The NEW geometry premise is an ideal shielded parallel-plate realization of
every positive capacitor branch, with fixed dielectric, negligible fringing,
and area and separation both transported by one orientation-preserving affine
F. It is a declared apparatus/reference chart, not an emergent 3D phase or a
calibrated network ruler. Use tetrahedral unit directions

    u1=(1,1,1)/sqrt3, u2=(1,-1,-1)/sqrt3,
    u3=(-1,1,-1)/sqrt3, u4=(-1,-1,1)/sqrt3.

Mutual port branches have normal n_ab=(u_a-u_b)/|u_a-u_b|. BOTH the port-record
and port-return branches have normal u_a. The record-return capacitance is
three separate equal branches C_gR/3 with normals ex,ey,ez. These assignments
are supplied physical premises; they were not inferred from a desired pair
response. They do not specify the physical connectors, support stresses,
Maxwell dynamics, local gauge paths, ordinary probes or copying junctions.

## 2. Finite deformation law and full electrostatic work

An initial plate area A and gap d become

    A(F)=A det(F)|F^-T n|,  d(F)=d/|F^-T n|,
    C_b(F)=C_b0 det(F)|F^-T n_b|^2.                             (2)

This is the exact ideal-plate approximation just declared. For F=aI it gives
C_b(a)=a C_b0, rather than a chosen volume-energy interpolation. The three
record-return branches sum to C_gR det(F)tr(F^-1 F^-T)/3.

Build each relative Maxwell capacitance C_v(F) by its actual branch incidence
vectors b_b: C_v=sum_b C_b(F)b_b b_b^T. All positive weights stay positive for
finite F in GL+(3); zero baseline branches stay absent. The baseline connected
passive capacitor graph therefore remains positive definite. With
C_rel=directsum_v C_v and B=[I;-1T], the floating matrix is B C_rel B^T. Its
single gauge kernel and neutral charge quotient give, exactly,

    Hcap(F)=1/2 x^T E(F)x,  E(F)=C_rel(F)^-1,
    1/2 Q_full^T C_full(F)^+ Q_full=1/2 x^T E(F)x.              (3)

Return-field energy is already in (3). Additional physical junction, chemical,
support or field terms are distinct obligations, not a second generic return
self term. Electrical passivity alone is not mechanical equilibrium or
positive mechanical stiffness.

For a fixed charge code, let Vpot=E x. A geometrical variation obeys

    E_A=-E C_A E,
    Hcap,A=-1/2 Vpot^T C_A Vpot.

Thus every capacitor branch, including record and return branches, participates
in the work. No branch or charge-independent contact is removed by comparing
carrier addition with a matched background.

## 3. Six complete first jets, not isolated mutual sources

At F=I+epsilon with epsilon symmetric, set tau=tr(epsilon),
epsilonT=epsilon-tau I/3 and mu=q_*^2 ed^2 C_m. Write Y_ab=Z_a Z_b for the
actual local pair primitive, without identifying its expectation with a
qualified retained physical metric. The branch logarithmic first derivative is

    s_b(epsilon)=tr(epsilon)-2 n_b^T epsilon n_b.

The six mutual branch derivatives are xx-2yz (12), xx+2yz (34),
yy-2xz (13), yy+2xz (24), zz-2xy (14), zz+2xy (23). Their map has rank6
when C_m>0. The FULL charging jet, after the other branches are included, is

    Hcap,epsilon=-(tau/3)Jcap
      +mu[epsilonT_xx(Y12+Y34)+epsilonT_yy(Y13+Y24)
          +epsilonT_zz(Y14+Y23)
          +(2/3)epsilon_yz(Y12-Y34)
          +(2/3)epsilon_xz(Y13-Y24)
          +(2/3)epsilon_xy(Y14-Y23)],                         (4)

summed over stars for a common deformation. It holds for both record
occupancies and every incidence word, not only degree2. B-star normals may
all be reversed without changing the plate law.

To check the complete coefficient, at a star put

    Vp,a=eta[q_* ed Z_a+q_* em sum Z+gcap q_R q],
    VR=eta[gcap q_* sum Z+eR q_R q].

The identities C_gp em+C_pr(em-gcap)=ed C_m and
C_gp gcap+C_pr(gcap-eR)=0 show both the extra pair contribution and the
cancellation of every traceless qZ term. For pair12 the port branches add
8mu epsilon_yz/3 to the mutual -2mu epsilon_yz coefficient. The complete
coefficient is therefore +2mu epsilon_yz/3, not the isolated mutual result.
The trace is exactly -tau Jcap/3 and keeps AR/self/return work.

Equation (4) has five independent traceless pair directions plus the trace
direction, whose pair coefficient is -U/2. At the allowed passive equality
C_m=0 all five traceless first jets vanish; no rank6 claim transfers to that
boundary. Rank6 of these charging vertices proves neither mechanical stability
nor six independently unconstrained global displacement fields.

## 4. Exact second contacts and the owned response contraction

For the linear chart F=I+sA+tB with symmetric A,B, each plate branch obeys

    C_b,AB/C_b=s_b(A)s_b(B)-tr(AB)
      +3 n_b^T(AB+BA)n_b-4(n_b^T A n_b)(n_b^T B n_b).

Use the three actual record-return branches separately in this formula. Then

    Hcap,AB=1/2 Vpot^T[C_A E C_B+C_B E C_A-C_AB]Vpot.           (5)

This includes every direct strain contact. Uniform A=B=I gives Hcap,aa=2Jcap
at a=1. For an actually owned canonical ensemble at fixed physical beta,

    Phi_beta,AB=<Htotal,AB>-chi_beta(Htotal,A,Htotal,B).         (6)

Equation (6) is a free-energy curvature, not the second derivative of thermal
internal energy. Its ground-branch limit requires a justified ground state.
Full cross responses with other Hamiltonian strain tangents must be retained.

At fixed q1 on the sampled current parent, each nonidentity charging first jet
is sqrt27 a_A dot Q14,0 plus an owned identity. Consequently its connected
uniform susceptibility per native vertex is a_A chi14(k0) a_B^dagger/2.
The identity still supplies direct stress/work. This contracts a prescribed
geometric source with the existing pair/coordination block; it does not choose
u(F),f(F), promote an unqualified sample inverse, or erase finite-beta/mixing
restrictions. Physical-volume normalization remains separate. Second contacts,
port means and physical query/coframe derivatives must also be owned.

## 5. Complete-parent contacts still needed

In a fixed logical chart the whole strain law must have the form

    Htotal(F)=Hcap(F)+Rraw(F)I+sum_mu c_mu(F)O_mu(F)+Hextra(F).

The signed coefficients include actual -h,-t,+lambda_J,+gamma, any independent
bare storage, and all other canonical terms not already in Hcap. Hextra includes
genuine connector/gauge, support, donor and count-port energies. No term is
counted twice. Uniformly,

    H_a=-Jcap/a^2+Rraw'+sum(c_mu' O_mu+c_mu O_mu,a)+Hextra,a,
    H_aa=2Jcap/a^3+Rraw''
      +sum(c_mu'' O_mu+2c_mu' O_mu,a+c_mu O_mu,aa)+Hextra,aa.

The plate law does not determine these other derivatives. If the physical code
W(F) changes, d(W^dagger H W) includes W_A^dagger H W+W^dagger H W_A. Exactly,

    Hlogical,AB=W^dagger H_AB W+W_A^dagger H_B W+W_B^dagger H_A W
      +W^dagger H_A W_B+W^dagger H_B W_A+W_AB^dagger H W
      +W^dagger H W_AB+W_A^dagger H W_B+W_B^dagger H W_A.

Fixed logical charge labels alone do not justify discarding those terms,
the complementary forcing or a dressed readout tangent.

The current physical candidate fixes compound charging feedback scaling1/a.
If no independent bare storage remains, its degree2 detuning is AR/a.
Adding independently fixed proper epsilon_r=2lambda instead gives
delta(a)=epsilon_r-2lambda/a+AR/a. These agree at reference but have slopes
-AR and 2lambda-AR, a genuine record-operator difference already exposed by
the conserving-clock note. Selecting the physical storage inventory is a
required decision, not an identity subtraction to preserve old resonance.

## 6. Nonuniform source and count boundaries; next obligation

The prescribed old L source remains an operational benchmark. With the current
intrinsic epsilon_r-2lambda=0, node-owned charging minus the native midpoint
degree/record source is exactly AR sum_v L_v q_v+self sum_v L_v-G_mid, where
G_mid=lambda/2 sum_e n_e(L_u-L_v)(q_u-q_v). G_mid vanishes for uniform L or
the held all-q1 sector, not for dynamic records. Equation (2) supplies its own
mechanical source and does not make old L a lapse or require engineering
capacitances to reproduce L.
The separately demonstrated L-compatible circuit realizer remains a different
unearned source-control premise. Uniform agreement transfers no gradient Ward
identity, record-clock source or physical gravity kernel.

Local-proper h on UNDISTORTED count growth does not imply h_A=0 on stretched
bonds. Count changes must use an explicit q4 support/capacitor inclusion with
supplies and the existing D/Lambda/source contacts; fixed-count F is not N
and no physical volume is supplied by graph labels alone.

One conditional minimal-class screen is already decisive: if ONLY the complete
positive charging block deforms, all other terms and raw reference have zero
explicit a derivative, and an independent physical V=Vref a^3 is supplied,
the justified mechanical branch gives p=<Jcap>/(3Vref a^4)>=0. Relaxation does
not reverse this Hellmann--Feynman sign. With positive full density and an
independently justified Einstein/perfect-fluid matching, that minimal dilation
cannot supply accelerated expansion. This is not a no-go for counted creation,
other owned strain terms, conditional RGRL closure or UNT as a whole. The older
whole-homothety galaxy failure also remains unchanged.

The concrete next obligation is to specify the actual junction/support/storage
strain inventory BEFORE contracting (4)--(6) as a full material law. The plate
geometry already supplies a falsifiable six-source charging law; no further
finite-cell response scan is needed to define it. A physical common ruler,
dynamic-source/Ward completion, conserving q4 incorporation, ordinary probes,
and the shared galaxy/expansion tests then use that same complete inventory.

## Frozen resident inputs

Paths are relative to joint_parent_continuation except the two program paths.
All nine byte streams were rehashed before this NEW note; none was changed.

| Input | SHA256 |
|---|---|
| LOCAL_RECORD_FEEDBACK_FLOATING_RETURN_COMPLETION_V001.md | 255ea0ca5f86cc711cae2ff5e746d8e9b005c2156b934818ded7789f9461f2a4 |
| LOCAL_RECORD_FEEDBACK_FIVE_ISLAND_PASSIVE_COMPLETION_V001.md | 124f68b600130afcb3935e11c43c1f939a804892b2794c25f89c29a0892f8693 |
| LOCAL_RECORD_FEEDBACK_CONSERVING_CLOCK_DOMAIN_V001.md | 4e2619089b00e432eb2a6800b5cf77774e5f8b673b83b8e1a66154b279a617e4 |
| LOCAL_PROPER_BOND_NORMALIZATION_V001.md | 9b4cc5e1942ac7373e210efa46bfa74e03bbcfb8130c01232373b02e8a622a5b |
| LOCAL_PROPER_BOND_CONSERVING_CREATION_SOURCE_CONTACT_V001.md | e28eb807a3df201d46981898f4f85189cca4d54f7723a7946e13dd3cae8f9d43 |
| NATIVE_MIDPOINT_SOURCE_CLOCK_CONSTRAINT_V001.md | 1c0cf577cbc9124b8c3f28fa6d639c8e06dfea25426bf015c9340215f571723a |
| HOMOTHETY_COMPRESSION_RESPONSE_V001.md | e5d7539eca899c7f8b949d817fd2acf8e5f68a8c9064587bbe66c7d892d8d84e |
| program-worktree/LANE_GRA_FU_F3_Q4_PAIR_RESOLVED_MAXWELL_DPAR_DERIVATION_V001/THEOREM.md | f088346f72861b3b11ae737fe6b882d43da9e747fc1d1d1f6bd446a7fd2b6272 |
| program-worktree/MODEL.md | 3d7c360a38b09fed8f4051c049e838ca561c32ba5dd105dddd80c6aeb7f65607 |
