# A connected subdivision growth port with owned work

2026-09-29. New analytical port candidate; no numerical worker or change to
the native Hamiltonians. This follows V038's connectivity and controller
results. It is an explicitly adopted incidence-changing source, not a proof
that the ports-off native dynamics spontaneously performs this growth.

## Result

One occupied, physically anchored bipartite edge can be replaced coherently
by a three-edge path containing one new vertex on each side. This preserves
connected components and cycle rank, gives an exact finite native-energy
increment, and has a well-defined Hermitian reverse channel. The resulting
port itself cannot disconnect a connected graph. Native flips still can;
their leakage and the complete source/supply work are retained below.

The smallest direct test is N=2 to N=3 in the invariant blank-register
sector: link dimensions 16 and 512, with a rank-eight partial isometry.
No record/carrier Hilbert-space enlargement is needed to check that claim.
An additional exact compressed-work correction for retained record/carrier
states is supplied separately, without claiming it has been simulated.

## 1. Partial isometry, not an unconditional node isometry

Work in one BS bipartite slab. A physical port anchors an old occupied edge
`a=(u_L,v_R)`. Add vertices `b_L,b_R` and the path

    u_L — b_R — b_L — v_R.

Its three allowed left-to-right incidence qubits are
`e1=(u_L,b_R)`, `e2=(b_L,b_R)`, `e3=(b_L,v_R)`.
Define J on incidence basis states by:

- if n_a=1, set the old a qubit to zero, set e1,e2,e3 to one, put every
  other new incidence qubit in zero, and retain all other old qubits;
- append every new carrier, record, writer and reservoir register in its
  unique blank, retaining every old register and correlation;
- if n_a=0, J annihilates the state.

Thus, with P=n_a,

    J^dagger J=P,             J J^dagger=Q.                (1)

Q requires old a absent, all three path links present, all other new links
absent, and all new physical registers blank. J^dagger acts only on that
image; it does not erase new records, remove a populated carrier, or silently
delete extra new links. A state outside Q needs additional owned operations
before this particular reverse channel can act.

An arbitrary old density matrix has eligible weight Tr(P rho). The normalized
conditional image is `J rho J^dagger/Tr(P rho)` when that weight is positive;
calling J an unconditional unitary or omitting that success weight is wrong.
The autonomous realization below has no postselected normalization.

For an eligible basis graph, the old degrees of u and v are unchanged, the
two new vertices each have degree two, and

    vertex count increases by 2;  edge count increases by 2.

Replacing an edge by this path preserves connected components and every
cycle's topological subdivision. In particular the cycle rank M-|V|+c is
unchanged. Conversely contracting the exact Q path recovers the same old
components. This port cannot join two previously separate old components.
On the composition schedule the path alternates arrow orientation; it is
not a new directed three-step causal route. Only underlying **undirected**
connectivity is proved.

## 2. Exact native work in the blank-register sector

Use the original BS06 incidence Hamiltonian, with `h_N=Omega/N`, and all
other registers blank. This is an invariant sector of the ports-off seed.
Let `S_rest=sum_(old e!=a) X_e`, `h'=Omega/(N+1)`, and

    c0=2Delta+2U_d(2-d_*)^2,
    D_B=c0+(h_N-h')*S_rest.

All old vertex degrees are unchanged by J; only the two degree-two new
vertices add degree energy. The bias counts two extra occupied links.
Compression therefore gives the exact operator identity

    J^dagger H_(N+1)^B J - P H_N^B P = P D_B P.          (2)

The old anchor flip has zero compression on either side; it must not be
included as an old coherent X contribution. Every other old flip changes
from h_N to h', not to a held fixed coefficient. Hence for normalized rho
supported in P,

    Delta E=c0+[Omega/(N(N+1))]*<S_rest>,
    |Delta E-c0| <= Omega*(N-1)/N.                       (3)

At the unchanged inherited Delta=4,U_d=d_*=Omega=1, c0=10. For N=2 to 3,
`D_B=10+(1/6)S_rest`, with possible mean costs between 9.5 and 10.5.
The occupied four-cycle maps to the occupied six-cycle and costs exactly
10 because its old incidence basis state has zero X coherence. Its original
and enlarged full diagonal energies are respectively 20 and 30. These are
analytical values, not reported numerical outcomes. This positive work must
be supplied; connected growth is not energetically free.

## 3. Both sides leak; keep the complete intertwining defect

Only the anchor flip leaves the old source domain:

    (1-P)H_N^B P=-h_N X_a P,       norm=h_N.              (4)

In the target, flipping old a or any of the 2N+1 new edges leaves Q. Their
images are mutually orthogonal, whether the flipped new edge began at zero
or one. Define

    L_B=-h'*(X_a+sum_new X_e)*J,
    J^dagger L_B=0,
    L_B^dagger L_B=h'^2*(2N+2)*P.                        (5)

On the full old Hilbert space, not just its eligible part, the identity is

    H_(N+1)^B J-J H_N^B
      = J D_B+L_B+h_N J X_a(1-P).                       (6)

The last term matters: native flips can feed eligibility from an initially
unoccupied anchor. Removing it would incorrectly treat P as an invariant
native sector. On a P-supported input it vanishes at that instant, but
subsequent native evolution need not remain in P.

For a normalized pure input psi in P, the target energy variance is exactly

    Var_(J psi)(H_(N+1)^B)
       = Var_psi(P H_N^B P+D_B)+h'^2*(2N+2).             (7)

The source variance itself is `Var_psi(P H_N^B P)+h_N^2`. Thus the old
blank-inclusion leakage formula cannot be reused unchanged. For N=2 to 3,
the target off-image squared norm is 2/3 and the source squared norm is 1/4.

### Retaining old records and carriers

The same J retains old register states and appends blank new registers.
Old record-feedback energy cancels exactly: each old endpoint still has
one occupied path edge, and the new records are blank. Old onsite and local
formation terms are retained; new onsite/copy terms annihilate their blanks.
For BS07 define `q_u,q_v` as **carrier** occupation and `T_uv` as the old
carrier transfer. Since `J_uv^2=q_u+q_v-2q_u q_v`, the exact compressed
correction becomes

    D_full=D_B+t_hop*T_uv+2lambda_J*q_u*q_v.             (8)

The removed direct hopping explains the plus sign before T_uv. New hopping
has zero compression but can move an old carrier into a new vertex, adding

    L_car=-t_hop*(T_(u,b_R)+T_(b_L,v))*J,
    L=L_B+L_car,
    L^dagger L=[h'^2*(2N+2)+t_hop^2*(q_u+q_v)]P.        (9)

The two new carrier destinations and the incidence-flip leakage sectors
are orthogonal. Equation (6) then holds with D_full and L. These formulas
assume exactly the displayed BS bulk terms and the declared new blanks;
extra ports or a populated new register require their explicit corrections.
The first small proposed numerical check uses (2)-(7), not an unqualified
large full-register calculation.

## 4. Source weights change, unless explicitly made additive

For the frozen occupation insertion `B_N=sum b_e n_e`, retain old weights
and declare the three new weights. Put

    delta_b=b_e1+b_e2+b_e3-b_a.

Then

    B_(N+1)J-JB_N=delta_b*J.                             (10)

Uniform incidence count has delta_b=2. A separately calibrated path-additive
source could have delta_b=0, but assigning each new weight b_a/3 is a new
source/ruler prescription, not a consequence of subdivision. Choose the
insertion before testing; do not switch it to remove an unwanted work term.

Use the previous autonomous controller, with

    U_N(g,V)=K_g*g^2/2+C*g*(V-2Nv_cell)
                       +K_V*(V-2Nv_cell)^2/2,
    p_N=-[C*g+K_V*(V-2Nv_cell)],         d=2v_cell.

At fixed instantaneous g,V its preferred-volume change still costs
`U_(N+1)-U_N=d*p_N+K_V*d^2/2`. Including source `-gamma*g*B`, the complete
compressed transition detuning from a supply excitation Delta_s is

    D_tot=D_full-gamma*g*delta_b
                     +d*p_N+K_V*d^2/2-Delta_s.          (11)

All terms have one owner. Neither the native coherence work nor the source
jump nor finite elastic energy may be renamed vacuum pressure. The controller
contact derivatives remain K_g,C,K_V for this g,V-independent J; making
its coupling geometry-dependent would add new derivative/contact terms.

## 5. Autonomous finite supply, exact reverse support and response

Let b=|0><1| lower a two-state supply and set T=J tensor b on the two size
sectors. Add `epsilon*(T+T^dagger)` to the original block-diagonal native,
source/controller and supply Hamiltonian. Then

    T^dagger T=P tensor |1><1|,
    TT^dagger=Q tensor |0><0|,
    [H_tot,n_size+b^dagger b]=0,
    d<n_size>/dt=(2epsilon/hbar)*Im<T>.                  (12)

The full Hamiltonian is Hermitian and time independent. Native, supply,
interaction and controller energy are conserved together. For an initial
old-sector state and excited supply, target probability begins
`epsilon^2*t^2*<P>/hbar^2+O(t^3)`. If the input is entirely in P, its cubic
term vanishes and the remainder is O(t^4). No projector measurement or
postselected success is silently applied during this evolution.

Unlike the old blank-pair port, this source generally does not commute with
creation. Equation (10) gives `[B,T]=delta_b*T`, and therefore

    (B_dot)_creation=delta_b*(n_size_dot)_creation,
    [B,[H_tot,B]]
       = direct_sum_n [(Omega/n) sum_e b_e^2 X_e]
                         -epsilon*delta_b^2*(T+T^dagger). (13)

The extra term is part of the actual incidence response. Reusing the old
source-preserving sum rule would miss it. A source impulse also rotates the
creation coherence by its delta_b phase; its interaction-energy work belongs
in the ledger rather than only in the old native flips.

### Creation itself preserves connectedness, even at finite strength

Let C_conn be the two-sector projector onto connected incidence graphs.
Subdivision and its supported inverse preserve the component count, hence
`[C_conn,T]=0`. The port is not a new channel for disconnection; native
incidence flips still are.

More quantitatively choose an old connected backbone G0 containing a, with
M0 edges, and its subdivided backbone G1 with M0+2 edges. Let Pi_back be the
two-sector projector requiring the respective backbone edges to be occupied,
without constraining extra edges or record states. Then
`[Pi_back,T]=0`, as do the diagonal source/controller terms. The existing
orthogonal-flip and Duhamel proof gives, for an initially supported state,

    Pr(outside Pi_back at readout time t)
       <= min(1, t^2/hbar^2 * max[Omega^2*M0/N^2,
                         Omega^2*(M0+2)/(N+1)^2]).       (14)

This is a readout leakage probability, not a classical first-passage claim.
It bounds disconnection independently of epsilon. In the target, losing the
exact Q pattern need not lose the backbone: an extra link can block reversal
without breaking connectivity.

The native-from-blank formation bound is not contradicted. Its premise was
that only `-Omega sum X/N` changes incidence; this port explicitly changes
four link values and the size sector. Its physical realization, blank supply,
energy and control are new premises that cannot be credited to the native
record-copy term.

## 6. A controlled fast-transfer limit exists in this declared port

There is a useful constructive bound without a time-propagation calculation.
Restrict this paragraph to blank registers and fixed clamped g,V. Choose
the supply gap from known operator constants, not a state's fitted mean:

    Delta_s=c0-gamma*g*delta_b+d*p_N+K_V*d^2/2.

Assume this is a positive available excitation gap. Inside the paired
P-source/Q-target subspace, identify target vectors using J. The Hamiltonian
is a common old compressed Hamiltonian plus epsilon times the branch Pauli X
and a target-only detuning `(h_N-h') S_rest`. The latter has norm at most

    delta_N=Omega*(N-1)/N.

The norm coupling the paired subspace to its complement is

    ell_N=max[Omega/N, Omega*sqrt(2N+2)/(N+1)].

Compare with the exactly swapping reference that drops only that detuning
and off-subspace block, keeping the actual complementary Hamiltonian. At
`t_swap=pi*hbar/(2|epsilon|)`, Duhamel's inequality gives

    Pr(target exact Q at t_swap)
       >= max(0, 1-[pi*(delta_N+ell_N)/(2|epsilon|)]^2).  (15)

This state-uniform bound uses no selected native response or transition
frequency. It proves that a sufficiently strong **added port** can transfer
an eligible connected state with controlled error at finite N. It does not
prove that the BS seed supplies that strength, gap or controller, nor that
the same bound applies to a moving quantum piston or full carrier states.
The bound is allowed to be uninformative at smaller epsilon; that is not a
reason to retune a frozen experiment after seeing its output.

## 7. Physical anchors and geometry are separate questions

Under old-node permutations pi, extend the permutation to the enlarged
space while retaining the newly supplied port labels. The family obeys
`U_pi,new J_a U_pi,old^dagger=J_(pi a)`. An explicit anchor register with
controlled map `sum_a |a><a| tensor J_a` is covariant when the anchor
transforms as well. Its norm is one and its eligibility projector retains
the anchor. One must not replace it by an unnormalized coherent sum over
all N^2 edges and accidentally introduce a size-enhanced creation amplitude.
An uncorrelated uniform anchor has eligibility `<M>/N^2`; reliably locating
an occupied edge in a sparse graph requires its own preparation/control.

Topological subdivision by itself supplies no physical distance. With each
edge assigned the same probe length, the chosen endpoint route changes
from one segment to three. With new segment lengths summing to the old one,
it can instead be a metric refinement. These are distinct calibrations.

For an explicit static diagnostic, take positive edge conductances c_i and
the quadratic energy `sum_i c_i(phi_i-phi_(i+1))^2/2`. Minimizing over the
two intermediate vertices fixes a common flux and gives

    c_effective=(1/c_1+1/c_2+1/c_3)^(-1).

Three unchanged conductances c give c/3; three conductances 3c reproduce c
at the old boundary vertices. This exact static series identity is not
invariance of all finite-frequency carrier dynamics or new-node probes.
The native seed does not assign those conductances, lengths, physical
clock rates or a spatial volume solely by creating the vertices.

## 8. Small falsifier to run next

Use the inherited N=2 and N=3 blank-register incidence matrices, a fixed
anchored edge, and explicit J. Check all of (1)-(7), (10)-(14) as operator
identities or independently bounded readouts. Enumerate the eight eligible
N=2 basis graphs: J must preserve component count, while the connected
four-cycle becomes the six-cycle. Use a finite supply with its values and
source weights fixed before propagation; retain both eligible and ineligible
inputs and the full native flips. The conserved-charge block has dimension
16+512=528, not a growing many-body simulation.

The scientific output is the actual transfer, connection/reverse-support
probabilities and energy ledger, including failures of complete transfer.
Check the strong-port bound only in its clamped blank-register domain.
No galaxy, CMB or desired Hubble history enters parameter selection. A
failure of this declared controller is evidence about this port, not an
excuse to delete leakage, reverse support, or the source jump.

This provides a finite, falsifiable route to **already-connected growth**
with an explicit supply. It neither proves native spontaneous growth nor
turns topological refinement into cosmological expansion, three-dimensional
geometry or gravity.
