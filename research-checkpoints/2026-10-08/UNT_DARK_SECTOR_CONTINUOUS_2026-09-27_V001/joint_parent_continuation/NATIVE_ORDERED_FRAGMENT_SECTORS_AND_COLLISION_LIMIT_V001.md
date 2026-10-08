# Ordered finite fragments: conserved sectors and the short-collision limit

2026-09-30. Analytical model decision, not an implementation or numerical
packet. All fragment gap nu, copy strength lambda and step delta_tau remain
symbolic. No state, favorable age, Markov bath or reservoir hopping is added
as though derived. This note compares only a finite outgoing native region
with a specified ordered reduced channel, the two continuations already
identified in the formation-limit note.

## 1. What the seed actually supplies

BS07 defines a Hermitian content-preserving transfer T and its current J.
BS09 puts that transfer on the CARRIER registers, gated by quantum incidence.
BS08/10 copies locally from carrier/writer into records and from records into
local reservoir fragments. The copy is reversible; there is no fragment
hopping, outgoing sink or replenishment law in those terms. Energy might
propagate through an enlarged interacting native graph, but neither its
geometry nor a return-error bound follows by calling an edge directed.

BS12 permits an explicitly completed boundary/controller/supply interaction.
It does not supply its matrices or fix its parameters. BS13/13a constrain
stability and port counts; they are not a temperature or rate law. BS05 calls
delta_tau0 an operational boundary-clock calibration, not a derived physical
cosmological step. BS10 permits nonnegative fragment gaps and real couplings,
but does not fix nu, lambda or their ratio to delta_tau0. The current A/B
controller parameters and old diagnostic observation times do not fill these
missing supply parameters.

Literal BS14a traces the OLD BULK layer after a prescribed unitary and retains
the next layer with its independently specified input beta. A repeated
fresh-fragment map that instead retains the entire old 96D cell and traces
only appended fragments is not literally the same retained-space map.
Identifying the two requires an explicit transfer/retained-space adapter and
source/energy assignment. It cannot be inferred from the notation Phi.

Thus the ordered option has the least NEW OPERATOR content for a conditional
diagnostic: use the already defined 384D H'_A/B for a finite interval, two
fresh blank targets, and an explicitly owned discard/decoupling boundary.
This is algebraically cheaper than a larger transport/return problem. It is
not automatically the option with the fewest PHYSICAL boundary assumptions,
nor a derived autonomous universe model.

## 2. The exact carrier-sector obstruction in the retained-cell channel

For this subsection, S means the full retained native 96D cell. Define the
parametric zero-source map

    U_X=exp[-i delta_tau H'_X(nu,lambda)/hbar],
    Phi_X(rho)=Tr_b[U_X(rho tensor |00><00|_b)U_X^dagger]. (1)

Distinct fresh fragments, not reused correlated old fragments, are required
for powers of the same Phi to represent a physical sequence. Equation (1)
defines a mathematical family; it does not close that physical supply.

Let X_c swap the carrier's left/right positions. The current Hamiltonians
contain only I_c and X_c, with identical carrier onsite coefficients. All
record/fragment operations commute with X_c. Therefore exactly, for every
finite nu, lambda and delta_tau in this family,

    [H'_X,X_c]=0,
    Pi_+/-=(I+/-X_c)/2,
    Phi_X^dagger(Pi_+/-)=Pi_+/-,
    p_+/-=Tr(Pi_+/- rho) is conserved.                 (2)

The original carrier-left preparation has p_+=p_-=1/2, including its original
cross-sector coherence. A globally unique attracting native state independent
of the input weights is impossible. Restriction to the actual weights is
legitimate; quietly replacing the initial carrier state or its coherence is
not. Equation (2) does not identify the complete peripheral algebra or prove
mixing within either 48D sector.

Incidence n, record R, Q and Pc are NOT conserved by the full formation-on
Hamiltonian. A simultaneous left/right swap of both records and fragments
gives channel covariance with symmetric blank inputs; covariance alone does
not make native record-swap populations conserved after tracing fragments.
The fixed single-carrier/common-content subspace is an existing preparation
restriction, not newly established universal matter conservation.

Crucially, the physical energy dipole connects the carrier sectors. With
DeltaP=2P_R-I=-Z_c and standard Pauli Y_c,

    [Z_A,X_c]=-2i gamma0(1+n/4)Y_c,
    [Z_B,X_c]=-2i gamma0(s+n/4)Y_c.                    (3)

The volume insertion commutes with X_c, but the mixed B dilation/dipole
contact also has a carrier-crossing term. Zero-source conservation must not
be promoted to conservation during a gravitational probe.

To see what a sector-aware analysis must keep, write the Kraus operators as
K_b=Pi_+ K_b+ +Pi_- K_b-. The four block maps are

    Phi_sigma,tau(A)=sum_b K_b,sigma A K_b,tau^dagger.  (4)

Both diagonal maps and the two off-diagonal maps matter. A source insertion
Pi_sigma Z Pi_-sigma probes cross-sector propagation even when the unforced
state is block diagonal. Replacing Z by its sector-diagonal part removes a
real source channel. The relevant next spectral/contractivity question is
therefore sector-conditioned, with source-visible cross blocks retained,
not a search for one global fixed point.

This X_c theorem applies to retaining this entire two-endpoint cell with
the stated symmetric Hamiltonian. In literal BS14a, X_c can span a discarded
and a retained site; it need not become a retained conserved observable.
That different channel requires its actual adapter and cannot borrow either
this obstruction or an evasion of it without checking the source mapping.

## 3. Exact no-go controls before any channel evaluation

Lambda=0 gives closed native unitary evolution with initially unoccupied
fragments; delta_tau=0 gives the identity channel. Neither gives mixing.
With formation off and the original record blanks, q_v is conserved and
q_v|blank>=0, so copying is inactive. More general held-energy population
claims need care: A's s^-1 q_v coupling does not commute with HQ, so the
earlier scalar-port held-energy theorem cannot silently be applied to the
entire A apparatus for arbitrary occupied records.

At nu=0, each X_bv is an exact constant of the total dynamics. Resolving its
two eigenvalues gives the exact channel

    Phi_X(rho)=1/4 sum_(epsilonL,epsilonR=+/-1)
                      U_epsilon rho U_epsilon^dagger,
    U_epsilon=exp[-i delta_tau
       (H_X+lambda sum_v epsilon_v L_v)/hbar],
    L_v=s^-1 q_v for A,  L_v=q_v for B.               (5)

This remains true with dynamic Q and C. It is unital, but not necessarily
mixing. IF each carrier sector mixes to its normalized identity AND the
cross-sector coherences decay, the original equal weights force I_96/96.
If those hypotheses fail, surviving modes must be retained rather than
asserting a unique state.

For this zero-gap case there is also an exact source qualification: the
OWNED lapse/volume source family is block diagonal in the same two X_b
operators. At native I_96/96 with source-independent blank inputs, each
diagonal bath branch carries the native identity. Every branch trace of a
two-time source commutator is zero. Thus its dynamical commutator response is
null, including the carrier-crossing source, although explicit contacts,
absolute energy, fluctuations and pressure need not vanish. Native identity
alone would not prove a null full system/bath response for a different source;
the common bath-block decomposition is essential here.

## 4. The ordinary short-collision shortcut loses the finite-gap mechanism

Let delta>0 be a newly introduced collision duration. This is a NEW limiting
family, not the fixed BS clock already derived to tend to zero. Write

    H_delta=H_X+nu a_X(Q) sum_v q_bv
                 +lambda(delta) sum_v L_v X_bv,
    a_A=s^-1, a_B=1, L_v=a_X q_v.                    (6)

For fixed lambda, nu and fixed finite native H_X, one independent blank pair
per delta yields only the native unitary generator as delta tends to zero:
the dephasing correction per step is O(lambda^2 delta^2/hbar^2), hence its
per-time contribution vanishes.

The familiar finite-dephasing scaling instead chooses a rate Gamma and

    lambda(delta)=hbar sqrt(Gamma/delta).

Using <X_bv>=0 and <X_bv X_bw>=delta_vw in independent blanks, the reduced
generator on a fixed native time interval is

    L(rho)=-(i/hbar)[H_X,rho]+Gamma sum_v D[L_v](rho),
    D[L](rho)=L rho L-1/2{L^2,rho}
             =-1/2[L,[L,rho]].                        (7)

The finite fragment gap nu, including A's Q-dependent gap term, does not
contribute to this limiting retained generator. Its initial blank mean is
zero and its higher-order cross terms vanish after division by delta. Every
L_v is Hermitian, so (7) is unital and still preserves the carrier weights.
Do not replace A's D[s^-1 q_v] by D[q_v]. Mixing/uniqueness is not established
by deriving (7). If the same sector/cross-sector mixing hypotheses hold,
the original state tends to native identity, not a nontrivial passive native
polarization state. The full driven source channel still requires all source
derivatives; an autonomous Kubo kernel is not automatically inherited from
a collision generator.

This is consistent with, not a contradiction of, the earlier finite-gap
I/2 witness. Its leading nonunital term is proportional to
lambda^2 nu g delta^4/hbar^4. Under the above scaling it becomes
Gamma nu g delta^3/hbar^2 per step, or O(delta^2) per unit time, and disappears.
Finite-duration finite-gap effects cannot be replaced by this limit while
claiming the same formation mechanism. The original blank preparation is
still not the I/2 witness.

The limit is not physically free: lambda diverges and so is not the original
fixed bounded-coupling parent. It requires a new rate, supply, clock and
scaling prescription. Even though nu disappears from (7), outgoing fragment
energy need not disappear: to leading order it is

    Delta E_b=nu Gamma delta sum_v <a_X L_v^2>+o(delta) (8)

in the same adopted zero-source energy partition. Here a_X commutes with L_v;
the first-order collision expansion and blank input fix this term. The energy
per unit time can remain finite. It must be balanced by native, interaction,
controller and switching work, not erased with the discarded fragment.
Equation (8) is a ledger scaling statement, not a positivity or equilibrium
temperature derivation. Source differentiation must also vary L_v, the gap,
the controller clock and any source-dependent incoming state according to
their declared family.

## 5. A specific boundary issue prevents treating Phi as automatic dynamics

For A, turning off just lambda leaves nu*s^-1(Q)*q_b. An occupied old fragment
is STILL coupled to Q. Tracing it and reusing the old 96D map therefore
requires a physical outgoing/decoupling adapter, with its interaction and
volume work counted; it is not the unchanged Hamiltonian's continuation.
For B the zero-source gap becomes fragment-only after copy-off, but its
endpoint dipole gamma0*s(Q)*nu*q_b still belongs to the adopted source family.
Dropping the old fragment under later lapse probes likewise needs an owned
outgoing geometry/source prescription. Discarding it from a reduced state
does not remove its energy from the universe.

The least-new-operator conditional path is consequently a finite-duration,
finite-gap ORDERED channel with an explicit decoupling/retained-space adapter,
all supplied blanks and their work, then a sector-aware formed-state and
complete source-response test. That path is more specific than another
age scan: global unique-attractor and ordinary unital Markov shortcuts are
already excluded as the claimed mechanism. It is not yet a selected physical
model because BS supplies no law for nu, lambda or delta_tau and no adapter.

The alternative remains a larger finite outgoing region using the actually
specified native transport, with a uniform return-error window. No reservoir
hopping is licensed as already present. A literal growing BS14a layer model
can eventually make an outgoing limit meaningful, but must own its retained
state, energy and physical-source mapping first. Neither option permits
independent environmental fit functions or removal of the unresolved absolute
volume/lapse law. No numerical run or higher-order continuation follows from
this decision note; all physical qualification flags remain false.

## Source anchors

- `../recovered_sources/BS_MICRO_ACTION.md`, BS05--14a:
  `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
- `NATIVE_FINITE_FRAGMENT_SOURCE_CURRENT_V001.md`:
  `1116b37f9cbd35a10abc55632f4d21230cdee5a27c5122e0d70d138881b4324b`.
- `NATIVE_FINITE_FRAGMENT_FORMATION_LIMIT_V001.md`:
  `f7d79015b6ed6773bf2c02e611db2b8454bca1ecd5e0ef189633ab6f1cd2cc07`.
- `NATIVE_RESERVOIR_FORMATION_CHANNEL_V001.md`:
  `6db32da99d6d346736e193b34b34cb270c242821051296de1be3bf7d86031a39`.
