# Prepared connected graphs: carrier, clock and source-work probes

2026-09-27. Analytical continuation; no numerical run, new interaction,
parameter adoption, graph preparation or physical metric assignment. The
resident prepared-graph persistence, correlation/preparation and frontier
V019 notes were read. The connected local-comparison companion was also
read and its propagation factors and cycle witness independently checked.

**Result.** On prepared incidence the native carrier sees adjacency PLUS a
degree-dependent onsite energy. Local transport, collective survival, mode
gaps and edge-work response test different parts of this same operator.
There is an additional O(N^(-1/2)) full-native comparison for ANY rank-one
carrier readout at fixed time, so global coherent probes need not be justified
by silently freezing graph flips. None of these results prepares the graph.

## 1. The exact one-carrier comparison Hamiltonian

Take a specified computational graph G on the 2N vertices of one bipartite
slab, preferably connected with bounded maximum degree. Turn formation off,
fix record occupations, and retain one carrier of fixed content. Let A_G,D_G
be graph adjacency and degree matrices. Native BS07 gives, in this sector,

    T_e=|u><v|+|v><u|,
    J_e^2=|u><u|+|v><v|.

Thus the comparison replacing incidence by its prepared bits has carrier
Hamiltonian

    K_G=epsilon_psi I+lambda_J D_G-t_hop A_G
       =epsilon_psi I+t_hop L_G+(lambda_J-t_hop)D_G,
    L_G=D_G-A_G.                                        (1)

The complete graph/record energy is retained as a carrier-scalar term.
In particular -lambda_R sum_e g_e(q_u+q_v) does NOT become a carrier
potential proportional to q_u. At fixed G the frozen carrier gaps and
position probabilities are exactly independent of record occupation.
Record-dependent carrier effects must enter through actual incidence
evolution, quantum dressing or another included native sector.

For t_hop>0, (1) is a positive-Laplacian kinetic operator up to a constant
if G is regular, or if lambda_J=t_hop. On an irregular graph, equality to
a scalar plus t_hop L_G requires lambda_J=t_hop. Otherwise the degree
potential is a specified native term, not an independently adjustable
gravitational field. The inherited lambda_J=1/4,t_hop=1/2 do not meet that
equality. Regularity hides the potential from fixed-number transport because
D_G=d I, but does not erase its energy or source derivatives.

## 2. Two independent finite-time carrier diagnostics

For a carrier initially at vertex u, under the fixed comparison hold,

    Pr_G(u;T)=1-t_hop^2 d_u T^2/hbar^2+O(T^4),
    Pr_G(v;T)=t_hop^2 T^2/hbar^2+O(T^4) if v neighbors u.  (2)

These follow from the off-diagonal matrix elements of K_G. Onsite degree
energy cancels from the return variance. For the separately specified
uniform coherent preparation |s>=(2N)^(-1/2)sum_v|v>, however,

    Var_s(K_G)=(lambda_J-t_hop)^2 Var_vertices(d_v),
    |<s|exp(-iK_G T/hbar)|s>|^2
      =1-(lambda_J-t_hop)^2 Var_vertices(d_v)T^2/hbar^2
                                                        +O(T^4). (3)

Indeed A_G|s>=D_G|s>, so K_G|s>=epsilon_psi|s>
+(lambda_J-t_hop)D_G|s>. Real Hamiltonians and these real preparations
make the survival probabilities even in T. Equations (2),(3) distinguish
degree-sensitive hopping from the degree potential. Preparing and reading
|s> is a distinct prospective protocol, not a free operation inferred from
the existence of the vector.

The quadratic coefficients in (2),(3) are in fact EXACT full-native
short-time coefficients for the stated graph-basis preparations, at any
native flip strength h. For P_a=I_graph tensor |a><a| and initial |G,a>,

    1-<P_a>(T)=T^2 <G,a|H(I-P_a)H|G,a>/hbar^2+O(T^4).

Graph-only terms and flips cannot leave the carrier state at first order;
the remaining vector is |G> tensor (I-|a><a|)K_G|a>. This gives precisely
Var_a(K_G). An initially empty target-site projector gives the analogous
transfer coefficient t_hop^2 g_uv. The real native hold and these real
preparations make the probabilities even in T. Formation remains off for
this test; conditional copying could otherwise entangle a coherent carrier
with newly written local records and add another survival-loss channel.

For a minimal connected irregular fixture, take the prospectively prepared
P4=K_(2,2) minus one edge. Its degree list is (2,1;2,1), so degree variance
is 1/4. With inherited t_hop=1/2, lambda_J=1/4 and hbar=1,

    Pr_full(uniform carrier survives;T)=1-T^2/64+O(T^4),
    Pr_full(site survives;T)=1-(d_u/4)T^2+O(T^4).

This distinguishes endpoint coefficient 1/4 from internal coefficient 1/2
and supplies a collective degree-potential test. For lambda_J=t_hop,
every carrier edge term annihilates the uniform vector, for ANY incidence
configuration; with formation off its survival is identically one even in
the full model with graph flips. Graph flips can affect the P4 fourth and
higher coefficients, but cannot erase its displayed quadratic distinction.
P4 and the coherent probe are specified preparations, not graphs or states
claimed to have formed or to be energetically preferred. No numerical run
is required for these identities.

The full native comparison can retain every flip. For any normalized
rank-one carrier readout A=|a><a|, its backward comparison is
|phi><phi|. Put b_c=|t_hop|+lambda_J and P_e=|u><u|+|v><v|. The
nonscalar edge operator obeys B_e=P_e B_e P_e and B_e^2<=b_c^2 P_e. Hence

    ||[B_e,|phi><phi|]||=sqrt(Var_phi B_e)
                              <=b_c sqrt(<P_e>_phi),
    sum_e P_e=N I,
    sum_e ||[B_e,|phi><phi|]||<=b_c N^(3/2).               (4)

Insert (4) into the already-proved exact readout identity, with wrong-bit
population y_e(s)<=Omega^2 s^2/(N^2 hbar^2). The NEW global-probe bound is

    |<A>_full(T)-<A>_G(T)|
       <=min{1,b_c Omega^2 T^3/(3 sqrt(N) hbar^3)}.        (5)

It applies to an arbitrary initial one-carrier density matrix on the
prepared graph, without factorizing its subsequent entanglement with
incidence. Fixed-record scalar terms commute with the carrier readout.
The companion's local site-readout bound is sharper, O(1/N), on bounded
degree graphs. Equation (5) instead controls the collective probe (3).
Both are fixed-time comparisons, not an unrestricted spectroscopy limit.

## 3. A calibration-free clock-only test on regular connected graphs

If G is d-regular and connected, the uniform carrier mode is the unique
lowest mode for t_hop>0. Its energy is epsilon_psi+(lambda_J-t_hop)d.
The gaps above it are

    omega_j=(t_hop/hbar) ell_j,
    sum_j ell_j=2N d,
    sum_j ell_j^2=2N d(d+1),                              (6)

where ell_j are all eigenvalues of L_G, including its one zero. The second
identity uses Tr A_G^2=2Nd; no embedding or continuum wavelength is assumed.
The dimensionless gap-shape statistic is therefore

    [(1/(2N))sum_j omega_j^2]
      /[(1/(2N))sum_j omega_j]^2=1+1/d.                  (7)

Suppose two simple connected regular graphs on the SAME 2N vertices, with
the same native hopping, had every gap multiplied by one factor a>0.
The first moment forces a=d'/d. The second then forces d'=d and a=1.
Thus changing unweighted prepared incidence cannot yield a nontrivial
pure common rescaling of ALL these carrier gaps. Equal-degree cospectral
graphs can still share the spectrum; their spatial readouts may differ.

This tests a clock-only interpretation with fixed intrinsic probe law,
not all common geometries: changing spatial geometry also changes standing
wave spectra. Independent carrier contents are symmetry copies, not two
independent clock calibrations. A universal physical lapse still needs
separately specified accessible composites and their source responses.
Resolving a very small finite-size gap may require T growing with N;
(5) and the local bound must be checked at that T before assigning full
native operational significance to the frozen spectral diagnostic.

## 4. Edge-work response distinguishes equal transport from equal stress

A prospective control multiplying an EXISTING carrier edge term gives the
Hellmann--Feynman work derivative for a normalized isolated mode phi_j:

    dE_j/deta_e = g_e {lambda_J(|phi_j(u)|^2+|phi_j(v)|^2)
                       -2t_hop Re[phi_j(u)* phi_j(v)]}.   (8)

This is a diagnostic differentiation, not an installed new interaction.
At lambda_J=t_hop it becomes t_hop g_e|phi_j(u)-phi_j(v)|^2. Otherwise
there is the extra term (lambda_J-t_hop)g_e(|phi_j(u)|^2+|phi_j(v)|^2),
even when the UNPERTURBED regular graph's transport differs only by an
overall phase. Propagation alone therefore cannot fix this edge-work law.
The source implementation and its work must be specified if it is used
experimentally. A physical stress claim additionally requires the complete
BS source response, including incidence, storage, feedback and contacts;
the carrier derivative (8) is not by itself that stress.

Even when (1) reduces to t_hop L_G, evolution is exp(-it_hop L_G T/hbar),
not a diffusion semigroup. Neighbor probability starts quadratically as
(2), whereas Markov diffusion starts linearly. Dephasing or a controlled
coarse-graining would need a same-parent derivation before replacing one
by the other. Nor does an elliptic graph Laplacian establish a Lorentzian
clock or common gravitational cone.

## 5. Fixed node count and the actual history question

At fixed N the BS action acts on a fixed set of node registers and link
qubits. Onsite record formation can change q_v and energy exchange; it does
not create node Hilbert factors. Incidence can still evolve, and a derived
physical volume could conceivably change at fixed node count, but no such
volume map follows from (1). During a time-independent closed hold total
energy is conserved. With explicit formation controls g_a(T),
d<H>/dT=sum_a dot(g_a)<K_a>+<partial_T H_port>, including every controlled
term. A geometry/preparation account must retain that work ledger rather
than identify increased stored records with free network growth.

The constructive next comparison is therefore concrete: on the SAME
prospectively prepared connected graph and fixed native coefficients, test
the local probabilities, collective survival and declared source-work
responses above, applying their full-flip errors at the chosen times. Then
use actual record-driven incidence histories to predict how these probes
change. Their mutually constrained responses test operational geometry;
none silently supplies graph preparation, physical expansion or gravity.
