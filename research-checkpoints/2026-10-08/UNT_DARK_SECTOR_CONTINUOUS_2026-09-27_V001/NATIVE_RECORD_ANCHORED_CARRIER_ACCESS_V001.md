# Native record-anchored carrier access V001

2026-09-27. Exact short-time word expansion; no numerical run, edge pinning,
mean-link replacement, formation claim or physical-force interpretation.

**Result:** a prepared occupied record can either increase or decrease early
carrier access to its node in the same BS action family. The leading bias is
sixth order in the microscopic hold time and its sign is fixed by a native
detuning, including the current-squared feedback. All four incidence qubits
remain dynamical and all final graph states are included.

Source: [recovered BS microscopic action](recovered_sources/BS_MICRO_ACTION.md),
SHA256 `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`,
BS01 and BS06-BS13. The finite restriction is specified below; it is not the
actual post-write state of the earlier formation experiments.

## 1. Full four-link, one-carrier hold

Use nodes (L0,L1 | R0,R1) and edges

    a=(L0,R0), b=(L0,R1), c=(L1,R0), d=(L1,R1).

Each edge has its original incidence qubit n_e=(I-Z_e)/2 and flip X_e.
There is one carrier of fixed content, with N_v=|v><v| and
T_e=|u><v|+|v><u|. In this one-carrier sector BS07 gives

    J_e^2=N_u+N_v.

All formation/copy couplings are off; ports are zero; writer/reservoir
spectators are blank. Initially q_R0=1 and all other record occupations are
zero. The occupied symbol is fixed but does not enter the feedback. These
record sectors are invariant during the hold, so suppressing their fixed
factors is exact, not a postselected approximation. Write lambda=lambda_R,
kappa=lambda_J, t=t_hop>0 and h=h_N=Omega/2>0. On all 16 graph masks and
four carrier positions the Hamiltonian is

    H=-h sum_e X_e + Delta sum_e n_e + U sum_v(d_v-d_star)^2
      -t sum_(e=u v)n_e T_e
      -lambda sum_(e=u v)n_e(q_u+q_v)
      +kappa sum_(e=u v)n_e(N_u+N_v)
      +epsilon_psi I+epsilon_r I.

Here d_v=sum_(e incident v)n_e, U>=0, lambda,kappa>=0. The initial state is

    |psi>=|empty graph> tensor |L0>.

The complete initial energy is

    C=4U d_star^2+epsilon_psi+epsilon_r.

Subtracting C I below only removes a common propagation phase; this energy
is retained in the comparison ledger. Put H'=H-CI. Define

    A=Delta+2U-4U d_star+kappa,
    A_j=A-lambda q_Rj,       j=0,1.

For the direct edge e_j=(L0,Rj), the state with that edge alone occupied has
diagonal H' energy A_j whether the carrier is at L0 or Rj. The term kappa
is essential: J_e^2 is not the identity on the four-position carrier space,
but equals one on either endpoint of this particular one-edge configuration.

## 2. Native word enumeration through H'^4

Let P_j=I_graph tensor |Rj><Rj|. Both P_j|psi> and P_jH'|psi> vanish.
To arrive at Rj requires an incidence flip followed by a hop. Write a graph
mask by its set of occupied edges, always with final carrier at Rj.

| Power | Final graph | Matrix element from psi |
| --- | --- | --- |
| H'^2 | {e_j} | ht |
| H'^3 | {e_j} | 2ht A_j |
| H'^3 | empty | -h^2 t |
| H'^3 | {e_j,f}, each of the three f != e_j | -3h^2 t |
| H'^4 | {e_j} | ht(3A_j^2+20h^2+t^2) |

The table lists every P_jH'^2 and P_jH'^3 output. For H'^4 only the
one-edge output can overlap the second-order arrival and affect the sixth-
order probability; other fourth-order outputs are not being discarded from
the dynamics.

The counts can be checked directly:

- At order three, a diagonal factor can occur between the first flip and
  hop or after the hop, giving 2A_j. Two flips of e_j, with the hop between,
  give the empty final graph. For two distinct flips e_j,f, three orders
  place the e_j flip before the hop, giving the coefficient -3.
- At order four with two diagonal factors, their three allowed placements
  after the first flip give 3A_j^2. A diagonal factor before any flip acts
  as zero on the initial state of H'.
- With three flips and one hop, three flips of e_j give two allowed words.
  For each other edge f, the multiset (e_j,f,f,hop) has six words with e_j
  before the hop. The total is 2+3*6=20. No incidence qubit is frozen.
- One flip and three hops give one word: flip e_j, then traverse it three
  times. Its contribution is ht^3.

Intermediate two-edge degree penalties and other current diagonal values do
not enter these sixth-order overlaps: words carrying those diagonals end in
graph sectors whose first arrival has order three or higher.

## 3. Inclusive probabilities and their leading difference

Set x=tau/hbar, where tau is hold time. The expansion is

    P_j exp(-iH'tau/hbar)|psi>
      =-(x^2/2)P_jH'^2|psi>+(i x^3/6)P_jH'^3|psi>
        +(x^4/24)P_jH'^4|psi>+... .

H' and the preparation are real in this basis, and the readout is real and
diagonal. Hence the probabilities are even in tau. The necessary overlaps
from the complete table are

    ||P_j H'^2 psi||^2=h^2 t^2,
    ||P_j H'^3 psi||^2=4h^2 t^2 A_j^2+28h^4 t^2,
    <H'^2 psi|P_j H'^4 psi>
      =h^2 t^2(3A_j^2+20h^2+t^2).

The coefficient of x^6 is the second norm divided by 36 minus the final
overlap divided by 24. Therefore the full, unconditioned position probability
is

    p_Rj(tau)=(h^2 t^2/4)x^4
       -[h^2 t^2 A_j^2/72+h^4 t^2/18+h^2 t^4/24]x^6+O(x^8).

All coefficients have the required energy powers: x has inverse-energy
units. The remainder means fixed-H Taylor coefficients, not an assigned
finite-time tolerance. With q_R0=1 and q_R1=0, the fixed readout
B=N_R0-N_R1 consequently obeys

    <B>(tau)=h^2 t^2 lambda(2A-lambda)/72 * (tau/hbar)^6
             +O((tau/hbar)^8).

Thus A>lambda/2 gives leading sourceward bias, and A<lambda/2 gives leading
bias away from the source. At A=lambda/2 only this sixth-order coefficient
vanishes; no all-time equality is inferred. Lambda=0, h=0 or t=0 does give
an exact zero-bias control in the specified initial preparation.

The leading fourth-order arrivals are identical. The sixth-order asymmetry
comes from changing the squared detuning from A^2 to (A-lambda)^2. Lowering
the source-side energy can move it closer to or farther from resonance.
This is an interference/access statement, not a universal force sign.

## 4. Admissible opposite signs and an energy-matched source control

For explicit examples set, in one energy unit,

    h=t=lambda=kappa=1, Delta=4, d_star=1,
    epsilon_r=3, epsilon_psi=1, Omega=2.

Both U=1 and U=3 obey the sufficient BS13 domain with delta_E=1:
Delta=2lambda+|t|+delta_E, U>=0, kappa>=0. Record insertion also retains
the operator floor epsilon_r-lambda N=1. Their different U values are two
distinct fixed parameter examples, not retunings within one source contrast.

- U=1 gives A=3 and sixth-order bias coefficient +5/72.
- U=3 gives A=-1 and coefficient -1/24.

These signs follow from exact coefficients, not numerical evolution. They
hold for sufficiently small nonzero tau; no particular finite-time window
or all-time monotonic bias is asserted.

For an exact control within either fixed parameter choice, move the sole
prepared occupied record from R0 to R1, leaving the initial graph and carrier
unchanged. Let S exchange the right-node labels, their incidence factors and
carrier positions. It maps the two conditional Hamiltonians into one another,
fixes |empty graph,L0>, and sends B to -B. Therefore

    <B>(tau;source R1)=-<B>(tau;source R0)

at every time, including all link fluctuations. Both initial energies equal
C because there is still exactly one record and every link is initially off.
The readout B is held fixed; relabeling it with the source would erase the
contrast rather than test it. No graph-state measurement or branch selection
is required by these inclusive expectations.

## What this advances, and what it does not

The existing native carrier supplies a mobile readout of record-conditioned
incidence dynamics even though record occupations themselves do not hop.
The same allowed action supports either sign of short-time access bias, so
record feedback or a negative conditional insertion interaction alone cannot
establish universal attraction.

This calculation begins with a prepared occupied record, an empty graph and
a carrier at L0. It neither reconstructs an actual writing history nor resets
the previously formed state for free. Preparation and readout implementation
would need their own declared ports and work. Node labels and the microscopic
clock have not become a physical distance, acceleration, force law or metric.
The result is a finite native dynamical response, not evidence of gravity or
dark matter/energy.
