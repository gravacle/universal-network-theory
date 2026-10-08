# An operational subdivision test using the native BS carrier

2026-09-29. Analytical derivation and prospective small test only. No worker,
new carrier preparation, physical-length fit or edit of a frozen source.
The parent is the resident `../recovered_sources/BS_MICRO_ACTION.md`,
BS06–BS11, and the declared held, copying-off setting. The subdivision map
and its work/leakage identities are those in
`CONNECTED_SUBDIVISION_GROWTH_CANDIDATE_V001.md`.

## Result

The native carrier already supplies an owned, finite transfer observable
across the old endpoints. It is not the scalar Laplacian probe previously
adopted for the operational-ruler comparison. Its current-square term adds
an essential degree-dependent onsite energy. A three-link subdivision has
an energy-dependent endpoint self-energy and additional resonances, and is
not equivalent to the removed direct hopping under the unchanged coefficients.

The fully quantum incidence is scientifically important: it can reopen the
removed direct edge and thereby create a short-time carrier route absent
from a frozen graph. The next informative calculation is therefore the
same prepared carrier on both full native systems, with frozen-incidence
transfer as a separately labeled control. No physical photon, light cone,
three-dimensional metric or cosmological expansion follows merely from
different transfer curves.

## 1. Exact invariant one-carrier held sector

Set all record, writer and reservoir registers blank, and all copying
couplings to zero as in the inherited held calculation. Put exactly one
carrier of a fixed content, say 0, among the 2N vertices. Its content-1
counterpart is related by the exact native content symmetry. This sector
has dimension `2^(N²)*(2N)`; it is invariant under the displayed held action.
Nonzero carrier-to-record copying would not preserve its blank-record
restriction and must not be silently retained.

For a carrier position v let P_v=|v><v|. In this sector BS07 gives

    T_uv=|u><v|+|v><u|,
    J_uv=i(|v><u|-|u><v|),
    J_uv²=P_u+P_v.                                           (1)

In particular the current-square energy is NOT a velocity expectation
squared, and it is not zero for a localized carrier with zero mean current.
The complete exact generator is

    H_N=H_inc tensor I + epsilon_psi I
        +sum_e n_e tensor [lambda_J(P_u+P_v)-t_hop T_uv],

    H_inc=-Omega/N sum_e X_e
          +Delta sum_e n_e+U_d sum_v(d_v-d_*)².               (2)

The record-feedback term vanishes because the actual records are blank.
Carrier count remains one; the onsite epsilon_psi term is retained in all
absolute energies. There is no additional matter species or source fit.
Replacing the operator n_e by its mean is not an exact closure: incidence
and carrier become correlated under (2).

The native current also provides a continuity check. For an edge oriented
u to v in the notation of (1), its contribution is

    d<P_v>/d tau=(t_hop/hbar)<n_e J_uv>,
    d<P_u>/d tau=-(t_hop/hbar)<n_e J_uv>.                     (3)

Sum over incident edges with the corresponding signs. Incidence flips
commute with every P_v, so (3) remains exact in the full quantum system.
Hermitian transfer is bidirectional; the bipartite composition orientation
does not turn a subdivided path into an irreversible directed signal.

## 2. Frozen incidence is a control, not a replacement Hamiltonian

For a specified incidence basis graph G, let
P_G=|G><G| tensor I_carrier. Its compression is

    P_G H_N P_G = E_inc(G) I + H_car(G),
    H_car(G)=epsilon_psi I+lambda_J D_G-t_hop A_G.             (4)

D_G is the diagonal degree matrix and A_G the undirected adjacency matrix.
Although

    H_car=epsilon_psi I+t_hop L_G+(lambda_J-t_hop)D_G,

this is a Laplacian plus a uniform offset only if lambda_J=t_hop, or on a
fixed regular graph where D_G is itself uniform. Inherited values are
`epsilon_psi=1, t_hop=1/2, lambda_J=1/4`, not lambda_J=t_hop.
Changing site energies or hopping weights to force a Laplacian is an
additional port/parent choice, not a consequence of BS07.

There is a rigorous finite-window control without suppressing native flips.
Every one of the N² flips maps P_G into a different incidence pattern; all
other terms preserve the pattern. Therefore

    ||(1-P_G) H_N P_G||=(Omega/N)*sqrt(N²)=Omega,
    Pr(not G at tau) <= min(1,Omega²*tau²/hbar²).              (5)

For the block-diagonal reference `P_G H P_G+(1-P_G)H(1-P_G)`, Duhamel also
gives state-vector error at most Omega*|tau|/hbar on an initial P_G state.
For a norm-one readout the elementary expectation-error bound is twice
this value, capped by its possible range. These are absolute, not relative,
error bounds for a small arrival probability. They apply with the carrier
terms included, since those do not themselves change the incidence bits.

The bound does not improve merely by increasing N: all N² possible flips
are being constrained. It becomes uninformative at an inherited one-edge
transfer time `pi*hbar/(2*t_hop)=pi` in units hbar=Omega=1. That does NOT
show that an actual graph fails to persist then. Native degree/bias energy
detuning can suppress real transitions, and the full finite test will
measure survival and transfer rather than infer failure from this bound.
Requiring only backbone survival is a weaker condition; added links can
alter transfer even when the backbone remains intact.

## 3. Native endpoint elimination retains the onsite and spectral terms

Consider the anchored replacement `u--v` by `u--b_R--b_L--v`, with no other
links incident on the two new vertices. Keep all other old carrier sites
in the boundary space. Old endpoint degrees are unchanged; both new
vertices have degree two. Denote the boundary generator without the old
direct hopping by H_B^0. The old and new boundary descriptions are

    H_old,B = H_B^0-t_hop(|u><v|+|v><u|),
    H_II=(epsilon_psi+2lambda_J)I-t_hop sigma_x,
    H_BI=-t_hop (|u><b_R|+|v><b_L|).                         (6)

E is the carrier spectral energy, with the branch's incidence baseline
handled separately. For E away from the two internal poles, the exact
Schur complement of `E-H_car` is `E-H_B^0-Sigma(E)`, where on (u,v)

    z=E-epsilon_psi-2lambda_J,
    Sigma(E)=t_hop²/(z²-t_hop²)
                      [[z,-t_hop],[-t_hop,z]].              (7)

The poles are `E=epsilon_psi+2lambda_J +/- t_hop`; they are internal
Dirichlet resonances, not automatically poles of every full boundary
readout. The diagonal self-energy and the off-diagonal transfer are both
compulsory. Dropping the diagonal part would change the carrier source
response and its energy accounting.

Even at a single nonsingular energy, matching the old off-diagonal entry
requires `z²=2t_hop²`. The diagonal correction then equals z, not zero.
Thus unchanged coefficients cannot reproduce the original endpoint matrix
at that energy, much less at every energy. A compensating endpoint potential
would be an explicitly added source; matching one frequency would still
not remove the other frequency dependence.

An expansion about E_0 is allowed only inside its distance to these poles:

    Sigma'(E_0)=-H_BI(E_0-H_II)^(-2)H_IB,
    -Sigma'(E_0) is positive semidefinite.                    (8)

The first correction carries additional retained carrier amplitude and
frequency dependence. It is not the scalar-probe added inertia with a new
name: (7) is a first-order quantum Schrödinger resolvent with the native
adjacency and current-energy terms. In particular, at inherited parameters
one internal pole is `E=epsilon_psi`; a putative low-frequency expansion
around that onsite reference is singular. One must specify the source's
energy/clock reference instead of calling E=0 a universal low-energy limit.

For an isolated old edge the carrier eigenvalues are
`epsilon_psi+lambda_J +/- t_hop`. For its isolated four-vertex path,
reflection parity p=+1 or -1 reduces the matrix to

    [[epsilon_psi+lambda_J, -t_hop],
     [-t_hop, epsilon_psi+2lambda_J-p*t_hop]],

    E_(p,+/-)=epsilon_psi+(3lambda_J-p*t_hop)/2
              +/- sqrt((lambda_J-p*t_hop)²+4t_hop²)/2.       (9)

These are directly testable frequencies. At the inherited values they are
`(9-sqrt(17))/8, 1, (9+sqrt(17))/8, 9/4`, versus `3/4,7/4`
for the isolated edge. These formulas are controls, not the spectra of an
embedded old tree after ignoring its other edges.

On a long regular degree-two graph, native dispersion relative to the
onsite reference is `epsilon_psi+2lambda_J-2t_hop cos k`. Relative to its
band bottom the small-k energy is quadratic, not a massless linear photon
dispersion. Population transfer can nevertheless supply a native operational
comparison with a fixed clock calibration; photon identification is not
needed for that narrower question and has not been established.

## 4. Exact short-time effect of quantum-incidence shortcuts

Initially put the carrier at u and the target incidence exactly in the
subdivided pattern G'. The removed old edge a is absent but still has a
native link qubit. A flip can create it and the carrier can then hop directly
to v. The leading amplitude, in the incidence sector G' with a toggled, is

    <G' xor a,v|U(tau)|G',u>
       =-h_(N+1)*t_hop*tau²/(2hbar²)+O(tau³).

Hence the UNCONDITIONAL arrival probability has the exact leading term

    Pr(carrier at v)=h_(N+1)²*t_hop²*tau^4/(4hbar^4)
                                                        +O(tau^6). (10)

For the real held generator and these real basis preparations, probabilities
are even in tau. On the frozen graph, if q_3 is the number of length-three
paths between u and v, arrival instead begins

    Pr_frozen(v)=q_3²*t_hop^6*tau^6/(36hbar^6)+O(tau^8).

Even postselecting exact G' at the endpoint is NOT frozen evolution. The
virtual sequence flip-a, hop-a, flip-a contributes at the same amplitude
order as the length-three routes:

    <G',v|U(tau)|G',u>
       =-i*t_hop*(q_3*t_hop²+h_(N+1)²)*tau³/(6hbar³)
                                                        +O(tau^4). (11)

Equations (10)–(11) assume this bipartite subdivision, hence no direct
occupied edge and no two-hop path between opposite-side endpoints. They
apply to the two concrete target graphs below, with q_3=2 for the six-cycle
and q_3=1 for the six-vertex tree. They are not a claim that a quantum
shortcut dominates at every finite time or carries a relativistic signal.
The control demonstrates exactly why hop count and measured native transfer
cannot be equated without testing the incidence dynamics.

## 5. Preparation and work are part of the comparison

The completed subdivision experiment began with ALL physical registers
blank. It did not contain the carrier used here and does not already test
(1)–(11). A new test must prepare the single carrier explicitly, retaining
its injection energy and the chosen port labels. No carrier-source pulse
needs to be invented for the first propagation test: its prepared state
can simply be specified and its absolute native expectation reported.

For an eligible old state with one carrier, the existing exact subdivision
formula simplifies because q_u*q_v=0 in this entire sector:

    Delta E = c0+(h_N-h_(N+1))<S_rest>+t_hop<T_uv>,
    c0=2Delta+2U_d(2-d_*)².                                 (12)

The positive hopping correction removes the old direct transfer. Old
current-square energy is retained at the endpoints; the new hopping leaves
the exact blank-new-carrier image and cannot be discarded in subsequent
evolution. Its extra off-image norm is the t_hop²(q_u+q_v) term of subdivision
Eq9. A real implementation of J also needs the already declared source/supply
ledger; (12) does not make J a free unitary or manufacture its controller.

Localizing the carrier at u on an incidence basis graph gives both
<S_rest>=0 and <T_uv>=0, so the exact mean increment is c0=10. A coherent
old carrier would generally have a different increment. Inserting a carrier
into a blank graph at u itself costs `epsilon_psi+lambda_J*d_u`, not just
epsilon_psi. If preparation uses nonzero copying or other ports beforehand,
their actual switching work is `Tr rho(H_after-H_before)`; no zero-work
assertion follows merely from naming the subsequent calculation a hold.

## 6. Small prospective full-incidence census, without a new growth port

Use `hbar=1`, and the inherited constants

    Omega=U_d=d_*=1, Delta=4,
    epsilon_psi=1, t_hop=1/2, lambda_J=1/4,
    all copying couplings=0; all noncarrier registers blank.

The physical anchor is `a=(L0,R0)` and the initially populated old vertex
is L0. These source/reader labels transform with relabelings; they are not
an inferred background geometry. No adjustable hopping or endpoint onsite
compensation is introduced. Compare BOTH original graph types:

| Old N=2 graph | Occupied old edges | Subdivided N=3 graph |
|---|---|---|
| Four-cycle | all four | six-cycle |
| Spanning tree | (L0,R0),(L0,R1),(L1,R1) | six-vertex path |

With edge bit index `i*N+j`, old masks are respectively 15 and 11; target
masks are 350 and 342. The new occupied path is `(L0,R2),(L2,R2),(L2,R0)`;
old (L0,R0) is removed, other old edges are kept, and all other new links
are blank. Old carrier positions `(L0,L1,R0,R1)` embed into target indices
`(0,1,3,4)`; new vertices L2,R2 begin carrier-blank. The prepared carrier
stays at old L0, not at an optimized source vertex.

The prior blank-register growth control used tree mask 7 and image 334.
Masks 7 and 11 are isomorphic as UNANCHORED paths, but their fixed edge
`a=(L0,R0)` has different roles: middle edge for 7, end edge for 11.
Swapping old R0 and R1 maps 7 to 11 but also moves that original anchor
to (L0,R1). Keeping anchor a here is consequently a new declared port
placement, not the same anchored experiment renamed. In tree 11 the
prepared source L0 has degree two and reader R0 degree one; their degrees
are preserved by its subdivision. This choice is prospective and not
selected by an observed transfer result.

The two old diagonal incidence energies are 20 and 14, and the target
energies are 30 and 24. L0 has degree two in every preparation, so the
full initial mean energies are respectively `21.5 -> 31.5` and
`15.5 -> 25.5`. These are algebraic expectations of (2), NOT worker results.
The full initial energy variance is `Omega²+t_hop²*d_L0=1.5` in all four
cases; this supplies a further exact generator check.

Prospective readout times, fixed in microscopic hbar/Omega units, are

    0, 1/32, 1/16, 1/8, 1/4, 1/2, 1, pi/2, 2, pi, 4.

The short subset tests (10)–(11); the later times test transfer/survival
where the uniform bound (5) need not be useful. No time is selected by a
galaxy residual or by an observed favorable peak. Each full state should
retain all carrier populations, source return, old-v arrival, occupation
of the two new vertices, exact-graph and connected-backbone survival, and
the joint edge currents (3), including the removed direct edge a. Record
unconditional and joint `(G',v)` probabilities separately, never silently
renormalizing by a successful graph projection. Norm, mean energy, carrier
count and continuity provide independent checks.

For each of the four preparations also evolve the explicitly FROZEN graph
compression (4), with all onsite terms retained. These 4x4 and 6x6 controls
can be independently diagonalized. In particular the cycle controls admit
exact population amplitudes. With `s=t_hop*tau/hbar`, ignoring their common
phase `exp[-i(epsilon_psi+2lambda_J)tau/hbar]`, they are

    C4: old-v amplitude=(i/2)sin(2s), return=cos²(s),
    C6: old-v amplitude=(i/3)[sin(2s)-2sin(s)],
        return=[cos(2s)+2cos(s)]/3.                           (13)

The carrier spectra of these regular controls are
`{1/2,3/2,3/2,5/2}` and `{1/2,1,1,2,2,5/2}`. Shared band edges do not
make the transfer spectra or old-endpoint response equal.

### Runnable operator and resource scale

Represent the state as `psi[mask,vertex]`. The diagonal is

    Delta*M(mask)+U_d*sum(d(mask)-d_*)²
                     +epsilon_psi+lambda_J*d_vertex(mask).

For each possible edge add `-(Omega/N)*psi[mask xor edge,vertex]` and
`-t_hop*n_edge(mask)*psi[mask,opposite_endpoint]` for its two carrier
endpoint entries. This is the exact invariant-sector Hamiltonian, with no
mean-incidence approximation or omitted current square.

Dimensions are 64 (N=2) and 3072 (N=3); their complex128 state vectors use
1 KiB and 48 KiB. A few dozen matrix-free work vectors, bit/degree tables
and output arrays are small; a dense 3072-square matrix would alone occupy
144 MiB and is unnecessary. Independent time-action algorithms can use the
same prospectively authenticated operator, with separate truncation/error
controls; tiny frozen graph diagonalization and (3),(10)–(13) supply external
checks. This note authorizes no execution and fixes no numerical tolerance
after outcomes: a short code/protocol preflight precedes any worker.

## 7. What this would establish

The test can establish whether connected node addition changes a carrier's
transfer/return spectrum under the already owned microscopic clock and
bulk coefficients, and whether quantum-incidence shortcuts materially alter
the frozen-graph comparison. That is a native operational discriminator
between refinement-like equivalence and a measurable change, not merely
a change in graph labels or storage count.

It does not alone convert the measured change into meters, seconds, a
massless photon, a universal ruler shared by all probes, three-dimensional
volume, or an autonomous expansion history. Those require calibrated ports
and further owned comparisons. The specific advance is narrower and useful:
the next ruler test can use the native current and carrier Hamiltonian,
with its full work and incidence response, instead of borrowing a separate
scalar-probe action and assuming the two are the same.
