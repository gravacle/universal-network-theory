# Occupied-incidence record memory law V001

2026-10-05 UTC. NEW exact elimination of the empty released-bond sector of
the frozen C8 action. No stiffness, support, fitted potential, parameter or
physical deformation is added. No numerical action, producer import or old
result changes. This is a finite supplied-support interaction law, not yet
a normalized galaxy/expansion law or a new prerequisite for adopted RGRL.

## Complete frozen blocks

Copies are off, all q words and content labels are conserved, and only edge
0--4 is released. Let s=q0+q4, k=sum(q), and a_q=A_R k. In carrier spaces of
dimension 8 (one-probe reference) or 56 (ordered hard-core tagged pairs), set

    H_o0,1=(19/2)I-t T_C8,
    H_e0,1=H_o0,1+2I-j(p0+p4)+t T_04,
    H_o0,2=11I-2j P_adj-t T_2,C8,
    H_e0,2=H_o0,2+2I-j C_04+t T_2,04,
    C_04=p0+p4-2p0*p4.                                  (1)

Here t=1/10, j=1/4, h=1/5 and lambda=1/2. The complete sealed 16D/112D
blocks, in order (empty,occupied), are

    H_q[theta]=[[H_e0+lambda s I, -h exp(-i theta)I],
                [-h exp(+i theta)I, H_o0]]+a_q I.        (2)

The constants include field self-energy and carrier storage/current once.
Tagged direct current, recoil, hard-core exclusion and actual occupied
hopping remain in(1). This law does not assign record occupation a mass.

## Stationary Schur interaction and its sign

For zbar=z-a_q and R_s(zbar)=(zbar-H_e0-lambda s I)^(-1), the exact occupied
block of the full resolvent is

    G_oo(z)=[zbar-H_o0-Sigma_s(zbar)]^(-1),
    Sigma_s=h^2 R_s,
    Sigma_s-Sigma_0=lambda s h^2 R_s R_0.                (3)

The last identity uses only the scalar shift; no commuting assumption about
H_o0 and H_e0 is made. For real zbar<min spec(H_e0), both resolvents are
negative and commute with each other. Thus Sigma_s is negative, while its
record increment is positive. With d=min spec(H_e0)-zbar>0,

    ||Sigma_s-Sigma_0||<=lambda s h^2/[d(d+lambda s)],
    ||Sigma_s||<=h^2/(d+lambda s),
    partial_zbar Sigma_s=-h^2 R_s^2.                    (4)

Raising the empty-sector cost makes the downward virtual shift less negative
at the SAME spectral argument. This is not automatically an attractive
force, a pole comparison at fixed total energy, or a long-range response.
After the explicitly separated a_q shift, H_s-H_0=lambda s P_empty is
positive independently of this subthreshold restriction; ordered block
eigenvalues cannot decrease with s. Absolute comparisons between different
q words must also restore their actual a_q values.

For a resolved pole with occupied vector o, the reconstructed empty vector
is e=-h exp(-i theta)R_s o. Its full normalization is

    <o|[I-partial_zbar Sigma_s]|o>
      =<o|[I+h^2 R_s^2]|o>.                             (5)

Projected norm is not full probability. Physical readouts require e as well
as o. For a differentiable simple pole and a source eta, the physical-energy
derivative is <o|H_o,eta+Sigma_eta|o>/<o|I-Sigma_E|o>, with numerator
derivatives at fixed physical E. Using zbar instead separately retains the
removed a_q derivative and every reference/source/count identity.

## Exact causal memory, including preparation

Write the full amplitudes as (e(t),o(t)). For the frozen diagonal blocks,
U_e(t,t')=exp[-i(H_e0+lambda s+a_q)(t-t')/hbar]. Exact elimination gives

    i hbar o_dot=(H_o0+a_q)o+J_prep(t)
       -(i/hbar) int_t0^t dt' M_theta(t,t') o(t'),
    M_theta=h^2 exp{i[theta(t)-theta(t')]} U_e(t,t'),
    J_prep=-h exp[i theta(t)]U_e(t,t0)e(t0).              (6)

The retarded self-energy is -(i/hbar)Theta(t-t')M_theta. Its Fourier/Laplace
transform gives(3). This is the exact Schur complement of the amplitude
action (or contour action with its initial boundary), not an irreversible
bath, a Markov approximation or an added conservative stiffness.

In the explicitly disclosed q-sector rotating frame exp(+i a_q t/hbar),
the kernel contains the full H_e0 propagator times
exp[-i lambda s(t-t')/hbar]. The scalar a_q is not discarded from physical
energy, cross-q readouts, pulse work, source contacts or count supply.
All original occupied-edge preparations have e(t0)=0. Restarting the exact
equation at a later saved frame generally has e(t0)!=0 and requires J_prep.
Source-dependent preparation also differentiates both initial amplitudes
or the initial density; it cannot be absorbed into a chosen memory kernel.

## Complete source and current contacts

For the dimensionless incidence phase, define delta_u=delta(t-u)-delta(t'-u).
The exact first and second kernel vertices are

    delta M_theta/delta theta(u)=i delta_u M_theta,
    delta^2 M_theta/[delta theta(u)delta theta(v)]
       =-delta_u delta_v M_theta.                       (7)

The preparation forcing has its own endpoint derivative
i delta(t-u)J_prep, plus any owned derivative of e(t0). A constant phase
cancels from the stationary self-energy; a time-dependent prepared response
does not generally vanish. Dropping these endpoint/contact terms would
break the independently owned prepared current identities.

With n=P_occupied, I_theta=-partial_theta H=h Y at theta=0, and the direct
second Hamiltonian contact is partial_theta^2 H=h X. More generally,

    <I_theta>=-2h Im{exp(i theta)<o|e>},
    d<n>/dt=<I_theta>/hbar.                             (8)

Substituting(6)'s reconstruction of e into(8) uses the SAME record-dependent
memory law as matter propagation. A physical transfer charge q_pi gives
I_phys=q_pi<I_theta>/hbar only under its declared faithful charge/path code.
No carrier charge, proper clock or metric is selected by this identity.

For any other owned source, let A=H_o, D=H_e, V=H_oe and R=(z-D)^(-1).
At fixed z and a fixed projection, Sigma=V R V^dagger and

    R_eta=R D_eta R,
    R_eta xi=R D_eta xi R+R D_eta R D_xi R
                               +R D_xi R D_eta R,
    Sigma_eta=V_eta R V^dagger+V R D_eta R V^dagger
                                      +V R V_eta^dagger. (9)

The second Sigma vertex is the full second product derivative, retaining
all ordered insertions, V_eta xi and D_eta xi. Dynamically, the analogous
derivative of U_D is -(i/hbar)int U_D D_eta U_D, with time ordering and
direct second D contacts. Actual lapse/strain/charging/junction sources also
differentiate h, both diagonal blocks, scalar/reference terms, encoding,
query and preparation. A changing encoder/projection adds its actual
derivatives before elimination. Incidence phase alone supplies none of
those unowned physical source identifications or deformation restoration.

## Projection scope and one bounded verification

The projection is the fixed microscopic occupied-edge subspace containing
ALL carrier configurations, not a selected support-conditioned reduced
carrier space. Apply(3)-(9) to every coherent q component and every mixture
column. Replacing s or a_q by an average, tracing q prematurely or retaining
one favorable word destroys actual record/carrier correlations and formed
cross-q clocks. A conditioned, renormalized occupied state is a distinct
measurement; it does not reproduce the unconditioned full preparation.

A minimal NEW verification, if root authorizes it, can read only the two
authenticated saved matrix bundles and perform small linear solves. Freeze
zbar=19/2 for reference and 11 for tagged blocks, all s=0,1,2 retained. Exact
edge positivity j>=t gives H_e0,1>=11.15I and H_e0,2>=12I, so these are safely
subthreshold without another eigensolver. Check(3)-(5), Hermiticity/sign and
the conservative gap bounds and Schur block factorization without a real
full inverse at a possible pole; at zbar+i h independently compare the full
block resolvent to its Schur expression and first/second source contacts.
No baseline propagation, eigenvalue replay, selected reaction or physical
success criterion is needed. This would verify/extract the owned interaction
operator, not establish galaxy-scale range, probe universality or cosmology.

A separately declared equilibrium diagnostic at the SAME clamped q word is
B_s=E_2,min-2E_1,min+E_0,min. The vacuum matrix is the two-edge-state block
with occupied energy 8+a_q and empty increment 2+lambda s, so

    E_0,min=a_q+8+[2+lambda s
                  -sqrt((2+lambda s)^2+4h^2)]/2.        (10)

Field self-energy, a_q and linear carrier storage cancel in B_s but remain
in the physical action. Its derivative in lambda s is
p_empty,2-2p_empty,1+p_empty,0, with no sign theorem. It is clamped-record
spectral addition curvature, not the actual formed-state history, autonomous
record selection, a physical distance-dependent force or a gravity claim.

## Frozen block and source ancestry

Both matrix bundle hashes below match their unique saved journal commits.
The accepted parent audits authenticate the complete states and action; the
present derivation reads text and hashes only, without importing producers.

| Input in this directory | SHA256 |
|---|---|
| FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001.md | 68b4a61ded02e9e6ecdfcf1819680d519f794eb8e3ba08b5b7a1ba329ed1aab9 |
| floating_return_c8_tagged_probe_reaction_v001.py | 778ff1615b0ab38c964ca4feb40b756c0df04771103afc953871c12c890e26c0 |
| FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001_RESULT.json | d7e4e759b357dd8154567a8a103c433f72236d5b0799123a67b6d40c628baae4 |
| FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001_RECEIPT.json | 7896e0b78db294fe3b66886449d088afee4a6a413ee27056d09b6dde5ed05669 |
| FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001_AUDIT.json | bd324e35eaf8bafa7b8686d49f6d1e4add0ad48c8deb6189d21ed2177f5687d7 |
| floating_return_c8_tagged_probe_reaction_v001_checkpoints/reaction_eigensystems.npz | 06432406fd969f8ec3c8d93a606207ff5c4bd1ce0deb0281b87e41e190ebcc1a |
| FLOATING_RETURN_C8_RETAINED_RECORD_GEOMETRY_V001.md | 8f3dc32381e76a4e6badfe23fff6c8bdd4830cb32ed0aff99b1aef57eba5ce5b |
| floating_return_c8_retained_record_geometry_v001.py | 49f2684fe46bce5d46e8e86782f82d73a0293e304d617a46eb5b84e98638396a |
| FLOATING_RETURN_C8_RETAINED_RECORD_GEOMETRY_V001_RESULT.json | 4104ec10a4c0a6a9183e9943743d80ce847dff4bad8b82013c0f2594bc581eac |
| FLOATING_RETURN_C8_RETAINED_RECORD_GEOMETRY_V001_RECEIPT.json | 2151436c1ce895c6fb577c72c673faefed184c1c011b57c98368c33dbf0663d5 |
| FLOATING_RETURN_C8_RETAINED_RECORD_GEOMETRY_V001_AUDIT.json | 5c519d1bef61c0e4b2cdf71424de9df08fa0d7f926b26c6ab9496c986d97e84f |
| floating_return_c8_retained_record_geometry_v001_checkpoints/release_eigensystems.npz | 4dd6c3d1a4d69761e8fb4ecb7755113f81d41473129614a0df9a8f0bcff09ebc |
| FLOATING_RETURN_C8_RETARDED_INCIDENCE_CURRENT_V001.md | 6a4b32a76b16405871ffba37d86b2012862a4f8336ec5c8f34e258a2312fcd44 |
| LOCAL_RECORD_FEEDBACK_GAUGE_COVARIANT_ELECTRIC_SOURCE_V001.md | d67174a454ebe6027f30553b001e64cdabba20112b971a2f35136455ec18e197 |
| LOCAL_PROPER_BOND_CONSERVING_CREATION_SOURCE_CONTACT_V001.md | e28eb807a3df201d46981898f4f85189cca4d54f7723a7946e13dd3cae8f9d43 |
