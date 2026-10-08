# Which native graph modes couple to the energy source

2026-09-30. Additive source-only derivation. No coefficient adoption, ground
preparation, spectrum computation, producer import, numerical worker or change
to the sealed handoff. The distinction between a soft eigenvalue and a mode
that the physical source can excite is the decision addressed here.

## Decision

The existing degree-constrained BS family gives a concrete answer before a
large spectral calculation. Its degree-one matching modes are invisible to
the complete node-energy lapse source inside their isolated low band, at every
N. Degree-two graphs on at most four nodes per layer are similarly invisible.
The first nonzero leading source response occurs for degree two with five
nodes per layer, provided the source has variation WITHIN a layer. Its entire
leading dipole spectrum is one calculable positive line, not an assumed mode
density. Making that line softer by reducing the native flip strength also
reduces its susceptibility; it does not manufacture a finite soft continuum.

This is a conditional native-family discriminator. It does not assert that
the original blank preparation forms this ground branch. A physical embedding,
source normalization, preparation and source-complete volume law are still
inputs to be owned. In particular the original two-plane source, constant
on each layer, remains dark throughout this degree-two low band for every N.

## The specified family and what the positive cost bound does establish

The inherited held parent satisfies kappa_R=3/4>0, including the actual
carrier current-square term. The previously proved bound is

    <M>_ground <= 4 Omega^2 N^2/(kappa_R^2 N^2+4 Omega^2),
    Prob(connected on all 2N vertices) <= <M>/(2N-1).       (1)

Thus merely adding held carriers or record coherence cannot turn that ground
branch into an extensive connected network. This is NOT by itself a theorem
that every excitation gap is bounded below or every source spectrum is empty.
An excited formed state is not subject to the ground-energy trial assumption.
Those distinctions prevent a connectivity bound from being overstated as a
general spectral no-go.

A minimal allowed change within BS06 is the already specified centered degree
family, not an extra loop interaction. For a fixed uniform record occupancy
q in {0,1}, no carriers, and formation/ports off, put

    a=Delta-2 lambda_R q,
    d_star=k+a/(4U),   h=Omega/N,   U>0,
    H=C_N+U sum_v(d_v-k)^2-h sum_e X_e,
    C_N=N a k+N a^2/(8U)+2N epsilon_r q+C_spectator.       (2)

All native constants remain in C_N. q=0 is available without preparing any
record. Changing d_star relative to the inherited value is a NEW declared
parameter-phase premise; it is not selected by a galaxy residual. k=1 is the
smallest nonempty degree control and k=2 the candidate considered below. The
same coefficients, including Omega, are held fixed as N varies. No arbitrary
edge-gap distribution, cubic energy or reservoir is added.

Let P span every k-regular bipartite incidence graph. Its zero-flip gap to Q
is 2U. The existing uniform regular-degree theorem supplies a sufficient
isolated low band: with beta=min(k,N-k),

    b_N=1+2k(1-k/N),
    r_N=(Omega/U)[sqrt(b_N)+sqrt((beta+1)/N)]<1,
    Q(H-C_N)Q >= 2U(1-r_N) Q.                           (3)

Exactly rank(P) eigenvalues lie below C_N and the remaining ones are above
the displayed positive threshold. For growing N, Omega sqrt(2k+1)<U with a
strict margin is sufficient once N is large. This condition is not certified
for the inherited Omega=U=1. At fixed N the expansions below are the separate
controlled h/U -> 0 limit. A uniform low-band isolation theorem does not make
a fourth-order splitting error uniform at growing N.

For the centered k=0 subfamily, the same sufficient theorem gives rank-one
low-band isolation and a nonzero gap under its small-Omega conditions. It
therefore also supplies a genuine gapped empty-sector control in that stated
domain. The stronger claim at arbitrary inherited Omega is not made.

## Complete local energy and its source representation

For (2), the owned symmetric endpoint partition reduces to

    h_v=c0+U(d_v-k)^2-(h/2) sum_(e incident v) X_e,
    sum_v h_v=H,
    c0=a k/2+a^2/(16U)+epsilon_r q,                      (4)

with any spectator energy separately located and retained. There is no
carrier-current allocation ambiguity in this carrier-free restriction.
Adopt, explicitly rather than deriving a spacetime, fixed externally anchored
node positions x_v and the weak affine lapse source

    H(alpha)=sum_v [1+alpha x_v/c^2] h_v,
    Z=H_alpha=sum_v x_v h_v/c^2,   H_alphaalpha=0.         (5)

alpha is physical acceleration, Z has units of energy/acceleration. All
lapses must remain positive. The common origin is chosen so sum_v x_v=0;
changing the origin adds the complete H/c^2 and does not change ground-state
transition matrix elements. The anchored profile is a BS12 apparatus datum,
NOT an emergent distance inferred from degree or a selected graph. No label
profile is promoted to universal gravity.

The local source operators transform as the two node permutation modules of
G=S_N(left) x S_N(right): two singlets, one left-standard representation and
one right-standard representation. The graph Hamiltonian is G invariant.
For finite h>0 its full incidence ground is unique and strictly positive by
the connected bit-hypercube Perron argument, hence G invariant. The isolated
low-band projector in (3) has the same G representation as P, by continuous
equivariant spectral transport from h=0. These are essential hypotheses,
not assumptions about an arbitrary formed or degenerate excited state.

## Exact dark low bands

For k=1, P is the permutation representation on perfect matchings. Right-node
permutations alone act transitively on those matchings. Its right-invariant
subspace is therefore only the constant vector: it cannot contain a nontrivial
left-standard/right-trivial representation. The left/right statement is
identical, and P has one G singlet. Consequently (5), applied to the invariant
ground, has only a ground-parallel component in the entire low band:

    P_low Z |0> = <0|Z|0> |0>,
    <n_low|Z|0>=0 for every excited low-band state.        (6)

This result is exact throughout the isolated family, not merely through
fourth order. The familiar O(N^-3) matching-switch eigenvalue is thus not
evidence of a source-weighted soft mode. High-band response is not removed.

For k=2 and N<=4, each possible cycle topology has a graph stabilizer
transitive on the vertices in each layer. The same single-layer-standard
representations are absent. Its orbit-constant singlets are even under layer
exchange, whereas a source constant with opposite signs on the two layers is
odd. Thus (6) again holds. More generally every degree-two graph is a union
of even cycles, each isomorphic to its layer transpose. ALL orbit singlets
are layer-even for every N. Therefore a source constant on each layer has
no excited low-band response at any N in this centered degree-two family.
Within-layer variation, not merely a larger graph, is needed to escape this
particular selection rule.

## Leading dressed insertion for the first bright case

The existing fourth-order reduction is

    H_eff=(C_N+E2+D4)P-g4 A_sw+O_N(h^6/U^5),
    g4=5h^4/(2U^3),                                    (7)

where A_sw is the full alternating-square switch adjacency. It is not a
Markov Laplacian with a compensating graph-dependent diagonal.

Source dressing is compulsory. Use a smooth equivariant canonical block
unitary W(alpha) with W(0)=I+O(h/U), mapping fixed P to the isolated band.
The physical fixed-chart insertion is W^dagger Z W. Differentiating H_eff
also produces the commutator with W^dagger partial_alpha W. Its P connection
begins at O_N(h^2/U^2); at zero source the second-order Hamiltonian is scalar.
Its first commutator with a non-scalar term is consequently order h^6.
Thus differentiating (7) gives the leading order-h^4 insertion only; it is
not a license to discard connection terms in a finite-h calculation.

For a four-edge switch involving the vertex set R, insert independent positive
node lapses ell_v into (4). Each flip carries h(ell_u+ell_v)/2, and every
intermediate denominator is U sum_v ell_v(d_v-k)^2. The sum of all 24 path
amplitudes is homogeneous of degree one in the four ell_v. Rectangle symmetry
makes their four first derivatives equal at ell=1. Hence each derivative is
g4/4. The resulting off-diagonal insertion is

    <G'|Z_eff^(4)|G> = -g4/(4c^2) sum_(v in R) x_v.       (8)

All second- and fourth-order diagonal source derivatives are node independent:
their returning paths use at most two edges, and the occupied/empty/shared
pair counts at each vertex depend only on N,k. Their centered dipole is zero.
Their absolute energy, uniform-lapse and volume derivatives are NOT discarded.
Equation (8) is not an undressed incidence-count insertion.

For k=2,N=5 there are exactly

    n_C=5!^2/10=1440 single C10 graphs,
    n_S=binom(5,2)^2 * (3!^2/6)=600 graphs C4+C6.         (9)

A C4+C6 graph has 24 switches merging its components and three within its
C6. A C10 has ten switches to C4+C6 by edge balance, and 15 staying C10;
its total switch count is 25 versus 27 for C4+C6. Thus on normalized orbit
sums,

    A_orbit = [[15,4sqrt(15)],[4sqrt(15),3]],
    lambda0=9+2sqrt(69),
    psi0(G)=u on C10, v on C4+C6,
    r=v/u=(sqrt(69)-3)/5,
    u=(1440+600r^2)^(-1/2).                             (10)

The positive orbit vector is a full adjacency eigenvector at its spectral
radius. The unique full-parent invariant ground selects this unique maximal
eigenvector in its two-dimensional invariant sector as h/U -> 0, independently
of any unproved claim about other representation multiplicities.

Write X4(G)=sum_(v in its C4) x_v for a C4+C6 graph. A vertex of its C4
belongs to 12 merging switches, and a vertex of its C6 to eight. Each C6
vertex belongs to two of its three internal switches. With sum x_v=0, (8)
therefore gives

    (Z_eff^(4) psi0)(G)=0,                              G in C10,
    (Z_eff^(4) psi0)(G)=-g4(u-v/2)X4(G)/c^2,            G in C4+C6. (11)

Each C10 is vertex-transitive, so its sum of X4 over the ten split targets is
zero for a centered profile. The three within-S switches preserve its C4.
Consequently the vector equal to X4 on S and zero on C obeys

    A_sw X4 = 3 X4,   <psi0|X4>=0.                      (12)

Let Q_x=sum_L(x_v-mean_L x)^2+sum_R(x_v-mean_R x)^2.
The two vertices selected for each side of the C4 are uniform independent
two-subsets, giving the exact identity sum_S X4(G)^2=180 Q_x. Thus the ENTIRE
leading low-band source measure is one line:

    Delta_soft = g4[6+2sqrt(69)]+O_N(h^6/U^5),
    W_soft = 180 g4^2(u-v/2)^2 Q_x/c^4 + O_N(h^10),
    chi_soft(0)=2 W_soft/Delta_soft = O_N(h^4).           (13)

Remainder powers in W hold at fixed U, fixed source profile and finite N;
their dimensional coefficients are not suppressed in a numerical error claim.
This is a positive ground-state spectral weight, not an actual formed-state
passivity result. Q_x=0 for the original two-plane profile, restoring the
exact dark control. A new anchored nonconstant profile can be bright, but
its geometry/preparation costs cannot be inferred from this response.

In particular weak native flipping makes the gap and susceptibility vanish
together. Replacing the physical source by an independently normalized edge
probe, or rescaling the clock/source with g4 to keep the response finite,
would change the experiment. A single positive finite line cannot establish
the required source-weighted nu(delta) proportional to delta window.

## Coupled pressure and complete contacts remain part of this family

The raw affine source (5) has zero alpha-alpha contact; its total ground work
curvature is minus the FULL susceptibility, including high states. A low-band
action acquires source contacts from eliminated states and from its source
chart. Those contacts must be retained when computing total work; the one line
(13) alone is neither the complete curvature nor a positive effective inertia.

An explicit conditional extension of the old A/B volume conventions illustrates
the pressure constraint without adding a fitted volume function. Introduce an
external eta and x_v(eta)=exp(eta)x_v(0), with no new quantum Q controller:

    H_A(eta,0)=exp(-eta)H(0),
    H_B(eta,0)=H(0)-E_b+E_b exp(3eta),
    E_b=2N U d_star^2.                                 (14)

This is the carrier-free case T=0; all spectators/controllers and their
physical scaling would have to be specified before adding them. Equation
(14) is an ADOPTED source assignment, not a BS consequence. Centered Z_A is
eta independent and Z_B=exp(eta)Z(0). The ground eigenvectors do not change,
so for the same soft contribution

    chi_A(eta)=exp(eta)chi_A(0),
    chi_B(eta)=exp(2eta)chi_B(0).                         (15)

The same factors hold for its complete stationary susceptibility under these
restricted scalings. The complete ground W, including E_b, must satisfy

    partial_alpha^2(3Vp)=-partial_eta W_alphaalpha.       (16)

This carries the source-dependent pressure and mixed contacts automatically
when derived from the same energy. It does not calibrate V0, a gravitational
field equation, the B absolute baseline or an actual density-dependent state.
Uniform scaling alone leaves the weighted spectral shape unchanged.

## Small exact test and the subsequent decision

No numerical run is needed to state (6) or (9)--(13). The next implementation
check, if authorized, is an exact combinatorial/source oracle, not an age or
parameter scan. Freeze k=2 and N=3,4,5, enumerating all degree-two binary
matrices (6,90,2040 states) and all legal four-edge switches. Freeze one
centered within-left-layer port profile

    x_L/ell=(1-1/N,-1/N,...,-1/N),   x_R=0,

and the separate two-plane null profile. ell/c^2 is symbolic calibration,
not fitted. Use rational arithmetic and Q[sqrt(69)] for the N=5 unnormalized
ground vector (1,r); no eigensolver or chosen finite h is necessary.

The complete census must verify degree preservation, symmetric adjacency,
orbit counts, every row type, the 24-path homogeneity derivative, vanishing
centered lower-order diagonal derivatives, equations (10)--(12), the exact
norm identity 180 Q_x and the two-plane null. N<=4 must give the declared
zero source vector, not be omitted as uninteresting. Fix resource/output
bounds and an independent implementation before any run. A discrepancy is
a failed source derivation, not permission to alter the profile or coefficients.

Passing this oracle would establish a correctly source-matched finite family.
The next REAL scaling question would retain the same degree family, source,
clock and physical-volume convention as N grows, derive the weighted spectral
measure and nonlinear normal form, and bound the error relative to its shrinking
spectral window. Uniform Q-band isolation alone is insufficient. If weight
per calibrated volume vanishes, the family fails this mechanism even when
eigenvalues become dense. Formation must independently supply the tested
state, with conserved sectors and all energy costs; no cooling is assumed.

The finite bright line and exact dark controls are the new information. They
identify which native degree-family change is worth testing and which apparent
soft modes cannot support the claimed source response. They are not a galaxy
fit, a physical normalization or a completed shared dark-sector model.

## Existing evidence and provenance

- `../recovered_sources/BS_MICRO_ACTION.md`: exact degree family, native h_N,
  permutation symmetry, finite preparation and physical port obligations.
- `NATIVE_RECORD_CONNECTIVITY_PATHWAY_V001.md`: inherited full held positive
  cost bound, including carriers; no connected-ground assumption.
- `../NATIVE_UNIFORM_REGULAR_DEGREE_BOUND_V001.md`: uniform isolated-band
  theorem and its distinct error scope.
- `../NATIVE_DEGREE_MANIFOLD_CORRELATION_SELECTION_V001.md` and
  `NATIVE_DEGREE_SWITCH_CHANNEL_V001.md`: fourth-order switch generator and
  complete scalar energy, not claimed new here.
- `NATIVE_SWITCH_GRAPH_RESULT_V001.md`: completed N=4 topology calculation;
  its propagation and eigenvalues are not rerun here.
- `NATIVE_ENERGY_DIPOLE_GRAVITY_BRIDGE_V001.md`: adopted energy-lapse source,
  signs, calibrated length, complete contacts and midpoint ownership.
- `NATIVE_SHARED_WORK_INTEGRABILITY_V001.md`: fixed-state branch and coupled
  force/pressure requirements, not an independent source completion.
