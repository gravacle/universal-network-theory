# Frontier V014: native size scaling, record energy and formation time

2026-09-27. New analytical progress; no numerical execution, production retry,
remote dispatch, physical-parameter replacement or infrastructure change.
The prior goal turn was progress: it verified the transport return, identified
its remaining numerical stop and preserved the local pre-execution failure.
Neither stopped branch has been resumed. The overall dark-sector goal remains
active and incomplete; no blocked-goal condition is claimed.

## 1. The native normalization matters

The full recovered BS microscopic source and joint plan V002 were read.
BS06 already specifies h_N=Omega/N, with Omega fixed. It is an owned part of
the candidate, not a normalization added to rescue scaling. N is the number
of nodes in each of two adjacent layers, with N^2 possible links. It is not
the remote L6 label, physical volume, cosmological scale factor or elapsed age.

Previous fixed-size examples with h=1 remain valid at those sizes. Extending
the N=2 example while preserving the native parameter means Omega=2 and
h_N=2/N, not h_N=1 for every N. Nor can the previous finite-N weak-flip
expansion be used uniformly when its own smallness bound grows with N.

## 2. A derived energy decomposition, not a guessed dark-fluid split

Take the source-off, carrier-free conditional graph sector, with fixed actual
binary record occupations q_v. Its complete relevant energy includes record
storage, link storage, degree penalty and record-link binding:

    H = epsilon_r D + sum_v f_(q_v)(d_v) - (Omega/N) sum_e X_e,
    f_q(d) = U(d-d_star)^2 + (Delta/2-lambda_R q)d,
    D = sum_v q_v.

Under the source's positive edge margin and fixed U>0, define the integer
minimum m_q=min_(d>=0) f_q(d), and a minimizing degree d_q. For equal numbers
of occupied records in the two layers, the two preferred degree lists have
the same sum. They are jointly realizable when M_*>=K^2, K=max(d_0,d_1),
or when M_*=0. The proof uses integral network flow, not a mean-degree ansatz.
Its mathematical input is the row/column-sum criterion in [Gale's original
paper](https://msp.org/pjm/1957/7-2/pjm-v7-n2-p04-s.pdf); the K^2 sufficient
condition is derived explicitly in the note.

For these populations the exact classical minimum and bounded quantum
correction give

    E_cl = 2N m_0 + D mu,     mu = epsilon_r + m_1 - m_0,
    E_cl - 2 Omega sqrt(C N) <= E_0 <= E_cl,
    C = (2U d_star^2 + Omega)/delta,

where Delta-2lambda_R>=delta>0. Thus the leading extensive energy separates
into a network baseline and a record-associated excess with binding included.
The bound holds for the true conditional quantum ground state, not a presumed
product state, and allows surviving correlations inside degenerate manifolds.

The coefficient obeys

    epsilon_r-lambda_R d_1 <= mu <= epsilon_r-lambda_R d_0.

Positive bare storage energy alone therefore does not prove positive complete
record excess. The error controls an extensive population comparison, not a
single-record insertion. This is not a formation, SEALED-record, gravitational
mass or pressure result. Increasing N cannot silently stand in for mechanical
volume deformation. Even if one later adopts a volume map, its complete
stress and composition work must be varied independently.

Likewise the formula does not choose D. At leading order, unconstrained
minimization over these record sectors favors the boundary of the allowed
population range according to the sign of mu, or is indifferent when mu=0.
The actual source-off dynamics conserves record occupation; it does not
perform this cross-sector minimization. A nontrivial population/formation law
is still required for abundance predictions.

Detailed proof: [balanced-record energy](NATIVE_BALANCED_RECORD_LEADING_ENERGY_V001.md).

## 3. The inherited benchmark is in a dilute-incidence ground regime

There is a sharper uniform bound that requires no balanced-record assumption.
Let

    G_min = Delta-2lambda_R + 2U - 4U d_star > 0,
    E_base = 2N U d_star^2 + epsilon_r D.

Use d_v^2=d_v+d_v(d_v-1). The exact diagonal Hamiltonian satisfies
H_diag-E_base>=G_min M, where M=sum_e n_e. For any joint state with
m=<M>, positivity of each reduced link qubit gives

    |<(Omega/N) sum_e X_e>| <= 2 Omega sqrt(m).

The empty-graph trial and completing the square imply

    E_base-Omega^2/G_min <= E_0 <= E_base,
    <M>_ground <= 4 Omega^2/G_min^2.

The second inequality is independent of N: this plateau does not provide
nonzero limiting mean degree. For the inherited U=1, Delta=4, lambda_R=1/2,
d_star=1, G_min=1. With Omega=2 (the N=2, h=1 calibration), <M>_ground<=16
and mean degree <=16/N, for every fixed binary record pattern. A basis-graph
connectivity claim also cannot survive unchanged: its probability is at most
<M>/(2N-1), since a connected graph on2N vertices needs at least2N-1 links.
This is a statement about the native incidence observable and conditional
ground state, not a universal no-go for all possible emergent observables.

This does not falsify the finite formed-state results, the separate L6 parent,
or UNT. It does rule out presenting this parameter point's ground-state
large-N limit as an already extensive connected network.

For uniform records the bound can be sharpened to an exact asymptotic result.
With G_q=Delta-2lambda_R q+2U-4U d_star>0, a product trial supplies a matching
upper bound to the all-state lower bound, proving

    E_0-E_base -> -Omega^2/G_q,
    <M>_ground -> (Omega/G_q)^2.

At the inherited coefficients the graph-blank-record sector tends to1 expected
link and the uniformly occupied-record sector to4, while their complete
energies are2N-2+o(1) and4N-4+o(1), respectively. The product state is only
a variational trial, not an assumption about the true ground state. The
proof also bounds the probability of a degree-two-or-higher incidence vertex
by O(1/N) in this strict empty-degree plateau. See the [native sparse-limit
and empty-phase theorem](NATIVE_SPARSE_THERMODYNAMIC_BOUND_V001.md).

The exact integer-degree screen identifies the next relevant parameter domain:
uniform occupied records prefer a positive degree only after

    d_star > 1/2 + (Delta-2lambda_R)/(4U)

(equality permits a degenerate zero/one-degree minimum). At the inherited
coefficients the threshold is1.25, above the current d_star=1. This is a
prospective condition, not a silently changed parameter. Nonzero degree is
only a first screen: degree-one graphs are matchings, and higher degree alone
does not prove local three-dimensional geometry or universal gravity.

## 4. Stable energy does not supply a preparation protocol

The native formation, carrier and record-feedback terms commute with every
link occupation. They can change the state and link energetics, but only the
declared X flips change the total incidence in the absence of link-changing
ports. For arbitrary entangled or mixed states, including time-dependent
record formation, the exact commutator and reduced-qubit positivity yield

    |d<M>/dt| <= (2 Omega/hbar) sqrt(<M>),
    |sqrt(<M(t)>)-sqrt(<M(0)>)| <= Omega |t|/hbar.

Therefore a graph-blank start satisfies

    <M(t)> <= (Omega t/hbar)^2.

To form a target mean degree d>0, so that <M> >= N d, requires at least

    t >= (hbar/Omega) sqrt(N d).

This is a necessary bound, not a guaranteed sufficient formation time. It
does not assume cooling, a ground state or a mean-link Hamiltonian. A stronger
sine bound and separate local-degree bound are in the proof. The global bound
requires rest-Hamiltonian commutation with M; the local version additionally
requires commutation with each d_v. Unspecified incidence-changing ports are
not included. A pre-existing sparse graph remains allowed, but its preparation
and energy must be owned rather than substituted for a blank start.

Detailed proof: [incidence formation-speed bound](NATIVE_INCIDENCE_FORMATION_SPEED_BOUND_V001.md).

## 5. What changes in the research sequence

These exact screens remove a misleading extrapolation before spending on
larger BS runs. The useful native next step is a prospectively specified
nonempty degree regime plus a formation/initial-state route that meets the
clock bound, followed by correlation-sensitive locality/response tests.
There is no reason to enlarge the inherited dilute ground-state benchmark
and call the enlargement a gravity test.

The primary active/maintenance allocation remains a separate required
derivation. The new energy coefficient constrains a supporting parent but
does not supply capacity allocation, physical stress, initial record abundance,
or a verified map into the already adopted working-gravity action. No dust/DE
identification, abundance ratio or observational pass follows from this turn.
Continue the analytical physical mapping; preserve all numerical stop boundaries.

## Review and custody

Three same-family analytical agents worked on native scaling, balanced
populations and the real-time bound. Root read the saved energy and speed
proofs in full, checked the commutators, flow cut, coefficients and empty-phase
bounds independently, and read the primary flow theorem. Independent review
specifically caught the need to keep h_N=Omega/N, the local-versus-global
commutator distinction and the degree-gap factor of two. Shared source and
assumptions remain; these are mathematical checks, not independent empirical
confirmation. No new numerical values were generated by executing the model.

- BS source SHA256:00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec.
- Balanced-energy note SHA256:2fffe1a190b1e25b96703485c6ee8170fc14345b56b511e53604fa6eca1b2865.
- Speed-bound note SHA256:8118207e2da4bdae41143f6a90d48dd3be9f450371c688f508eabe776ccc6229.
- Sparse-limit note SHA256:76d3a1b3c6ae511066777889f4a47cc70d987bba31dcd160c79698e44b78eedc; root read and checked the complete proof, including its matching product-trial bounds and actual-ground-state conclusions.
