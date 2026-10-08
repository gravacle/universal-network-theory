# Exact native joint link/record formation with an owned energy ledger

2026-09-27. Construct `BS_RESONANT_RECORD_PAID_LINK_V001`. Prospective
coefficient family within the existing BS action, derived algebraically
before numerical checking. It is not a replacement of inherited mission
parameters, a cosmological fit, or a completed network-formation theory.

## 1. The formation channel

Use one slab with N=1 and one possible link. Keep carriers and the right
record blank, all other copy couplings zero, and one left writer in a
declared occupied content x. The active left record begins blank. The
native writer-to-record generator restricts to a Pauli X on the record's
blank/content-x subspace. Write n for the link occupation and q for the
left record occupation. The exact invariant four-dimensional Hamiltonian is

    H=C I-a n+epsilon q-lambda n q-h X_link+g X_record,
    C=2U d_*^2+epsilon_w,
    a=4U d_*-Delta-2U,       epsilon=epsilon_r.          (1)

No simultaneous link/record flip has been inserted. The only off-diagonal
terms are the already specified native link flip and local copying. Writer
content is conserved and the same equations hold for both content values.
Nonzero additional spectator constants, if present, must be retained in C.

Choose a>0, epsilon=a+lambda and g=h. The initial state |n=0,q=0> and
the desired final state |1,1> then have the SAME complete diagonal energy C.
The intermediate states |0,1> and |1,0> have relative energies epsilon and
-a. A positive record storage cost is paid by the decrease of graph plus
record-link interaction energy, not by removing a constant from the ledger.

In ordered basis (00,01,10,11), H-CI is exactly

    [[0, h,-h, 0],
     [h, epsilon,0,-h],
     [-h,0,-a,h],
     [0,-h,h,0]].                                      (2)

The symmetric vector D=(|00>+|11>)/sqrt(2) has energy zero. In its orthogonal
subspace (B=(|00>-|11>)/sqrt(2), |01>, |10>) the matrix is

    K=[[0,sqrt(2)h,-sqrt(2)h],
       [sqrt(2)h,epsilon,0],[-sqrt(2)h,0,-a]],
    det(EI-K)=E^3-lambda E^2-[a(a+lambda)+4h^2]E
                                                   +2h^2 lambda. (3)

## 2. An exact solvable transfer family

Let s>=3 be an odd integer and eta>0 an energy unit. Set

    lambda=s eta,
    h^2=g^2=3(s+2)eta^2/(2s),
    a=[sqrt(s^2+4(2s+1-12/s))-s]eta/2,
    epsilon=a+lambda.                                  (4)

Here a>0. Direct substitution factors (3) as

    det(EI-K)=(E+3eta)(E-eta)(E-(s+2)eta).               (5)

At T_*=pi hbar/eta, every eigenvalue in the B subspace acquires phase -1,
whereas D acquires phase +1. Therefore, exactly,

    exp(-i H T_*/hbar)|00>=exp(-i C T_*/hbar)|11>.       (6)

The full active writer/link/record tensor space has dimension 18, and the
four-state reduction is an invariant subspace, not a projection performed
during the calculation. Linearity gives the corresponding content-copy
isometry for an arbitrary writer superposition or entanglement with an
external reference: the link becomes occupied, and each orthogonal writer
content is copied into the formerly blank record with the same phase.
This creates correlation, not independent copies of an arbitrary quantum
state. No outcome selection, bath or measurement is required for (6).

The pulse is an autonomous TIME-INDEPENDENT Hamiltonian evolution on this
interval. Its start and duration are specified preparation/clock inputs;
an autonomous clock/controller producing and stopping that interval has
not been derived here. Without stopping, the evolution is reversible and
returns to the initial state after 2T_*. Permanent monotone accumulation is
not asserted.

## 3. Complete energy transfer and the source-off continuation

Both endpoint means of the link-flip and copying interactions are zero.
The endpoint changes in the other three terms are

    Delta E_graph=-a,
    Delta E_record=+epsilon,
    Delta E_feedback=-lambda,
    total=epsilon-a-lambda=0.                           (7)

The full Hamiltonian mean is C throughout, with energy variance 2h^2 at
both endpoints. Record formation is precisely the degree of freedom absent
from the fixed-record closed-hold obstruction. This example transfers energy
internally rather than relaxing to the full Hamiltonian's ground state.

If the existing copying coefficient is set to zero at the exact endpoint,
its mean instantaneous quench work is -g<X_record>=0. This is zero MEAN
work in the declared Hamiltonian ledger, not a free controller, zero work
fluctuations, or a protocol without timing requirements. After the switch,
q commutes with the hold Hamiltonian and remains one without continued copy
power. All native link flips remain active. Starting from n=1, its exact
hold probability is

    P(n=1;t)=1-L sin^2(sqrt(epsilon^2+4h^2)t/(2hbar)),
    L=4h^2/(epsilon^2+4h^2).                            (8)

Thus the newly formed record persists while the link remains strongly
occupied for suitable members of the family. Graph/interaction energies
can continue exchanging during this hold; record count remains fixed.

Timing sensitivity also has a direct bound. At T_*+delta_t the target
probability is at least 1-2h^2 delta_t^2/hbar^2. Expand the survival
probability in spectral weights and use 1-cos z<=z^2/2 with variance 2h^2.
This is a timing-error bound in native units, not a physical clock design.

## 4. A feedback ablation with an all-time ceiling

Keep the other coefficients and start state fixed, but remove only
-lambda n q. The two active qubits then evolve independently. In particular

    P_ablated(q=1;t)
      <=4g^2/(epsilon^2+4g^2)=L                         (9)

at every time, since g=h. Joint occupied-link/record success is bounded by
the same L. This arm is not claimed to have the same evolved interaction
energy as the target. It isolates a mechanistic distinction: native feedback
allows exact simultaneous formation where copying without that feedback is
off-resonant. Removing copying instead keeps q identically zero.

## 5. Declared numerical fixture and scaling boundary

For a concrete prospective witness take s=25, eta=1/50, U=1, Delta=4,
epsilon_w=0, hbar=1. Then

    lambda=1/2,
    h=g=9sqrt(2)/500,
    a=(sqrt(20677)-125)/500,
    epsilon_r=(sqrt(20677)+125)/500,
    d_*=3/2+a/4,
    Omega=h  (N=1),          T_*=50pi.                  (10)

The native extensive margin and positive bare storage gap hold. The common
degree-one g-gap is a/2>0. U, Delta and lambda match the earlier example;
epsilon_r, d_*, Omega and the formation coupling are explicitly different
prospective coefficients. They were solved for the transfer identity, not
inferred from dark-sector data. In this fixture L<1/100 exactly: substituting
(10) reduces this claim to epsilon_r^2>396h^2, which already follows from
sqrt(20677)>125. Smaller s=3,5 fixtures also check the algebraic family but
are not required to have sub-percent hold leakage.

No inference to a connected many-node graph follows from multiplying
independent cells. The native multi-node flip is Omega/N whereas (4) fixes
a particular relation between copying, flip and detuning. Extending this
route must respect that scaling, overlapping degree costs, writer/record
capacity, and a complete formation/clock/energy ledger. One may not choose
new coefficients separately at each N while claiming the original fixed-
coefficient scaling family. This exact primitive makes an internal energy
transfer pathway available; the collective realization remains to be derived.
