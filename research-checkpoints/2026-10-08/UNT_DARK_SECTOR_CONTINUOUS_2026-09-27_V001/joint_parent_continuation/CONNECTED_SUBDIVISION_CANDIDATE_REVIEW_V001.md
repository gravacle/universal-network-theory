# Independent review of the connected subdivision port

2026-09-29. Analytical review of CONNECTED_SUBDIVISION_GROWTH_CANDIDATE_V001.md
against the resident BS06–BS11 microscopic action and the declared controller.
No numerical worker, new initial state, source modification or adjacent-folder
inspection. The construction is a new port completion, not spontaneous growth
derived from the ports-off seed.

## Decision

The displayed identities (2)–(9), the source double commutator (13), backbone
bound (14) and strong-port bound (15) are correct within their stated domains.
No mathematical repair is required. The supplied energy, reverse support,
eligibility and native leakage cannot be dropped when interpreting this result.

## 1. Native action and both leakage directions

The map J is injective on P=n_a and annihilates its complement. Replacement
of one old occupied edge by three gives exactly two extra occupied links.
Every old degree is unchanged, while each added node has degree two. Thus
the blank-sector diagonal cost is

    c0=2Delta+2U_d(2-d_*)².

The old anchor flip has zero P compression. Each other old flip commutes
through the map, with coefficient changing from h_N=Omega/N to h'=Omega/(N+1).
This proves (2) and gives

    ||(h_N-h')S_rest||
       =(Omega/[N(N+1)])*(N²-1)=Omega*(N-1)/N.

For inherited N=2, c0=10 and the stated 9.5–10.5 compressed range follows.
The occupied four-cycle and its six-cycle image have diagonal energies
4Delta+4U_d(2-d_*)²=20 and 6Delta+6U_d(2-d_*)²=30.
These checks are algebra, not a new run.

On the source side, only -h_N X_a leaves P. On the target side, old X_a
and all 2N+1 new flips leave Q. Their images have different fixed-bit
violations and are pairwise orthogonal. Therefore

    L_B†L_B=h'²(2N+2)P,
    (1-P)H_N P=-h_N X_a P.

For an arbitrary old input the term -JH_N acting on (1-P) contributes
+h_N JX_a(1-P). This verifies the sign and necessity of the last term
of (6). Compression alone would omit it. Resolving H_(N+1)Jpsi into its
orthogonal Q and (1-Q) components proves the variance identity (7),
including its additive target leakage and the distinct source h_N² term.

## 2. Full register correction and carrier leakage

Old onsite/formation operators commute through J; new local formation
operators annihilate their completely blank controls. Old record feedback
is unchanged because each old endpoint retains its degree contribution,
and the added records are blank.

Removing the old hopping -t n_a T_uv gives the positive compressed change
+t T_uv. The old current square is q_u+q_v-2q_uq_v. The two path-end current
squares compress to q_u and q_v, while the middle blank pair contributes
zero. Their difference is exactly +2q_uq_v, proving (8), including its signs.

The two new carrier transfers land in distinct newly occupied registers.
Their squared norms are t²q_u and t²q_v, with no cross term. Neither image
overlaps the pure incidence-flip leakage, because the latter leaves every
new physical register blank. This proves (9) as an operator identity even
for retained old register entanglement. It is not a claim that those enlarged
register states have been numerically simulated.

## 3. Source work, backbone and reverse support

Every eligible map has the fixed insertion jump delta_b. Hence [B,T]=delta_b T
and [B,T†]=-delta_b T†. Directly applying the two commutators gives

    [B,[epsilon(T+T†),B]]=-epsilon*delta_b²*(T+T†).

The native contribution in (13) remains the weighted flip sum, because all
other displayed native bulk terms commute with incidence occupation. The
source, elastic and supply terms commute with B. This verifies the complete
source moment and the creation contribution to B_dot.

For the elastic controller, shifting the preferred size volume by d at fixed
g,V changes U by d*p_N+K_V*d²/2. The source jump is -gamma*g*delta_b and
the lowered supply costs -Delta_s. Thus the detuning (11) has all signs
consistent with one inclusive ledger. No pressure interpretation of c0 alone
follows from this equality.

The subdivision and its supported inverse preserve every old connected
component. More strongly, the indicator of the chosen old backbone equals
the indicator of its subdivided image whenever J acts, so Pi_back T=T Pi_back.
This remains true for extra old edges and for target states outside Q, where
the reverse map vanishes. The creation term cannot leak this backbone.

Native flips of distinct required backbone edges have orthogonal violation
patterns, with off-block norms h_N sqrt(M0) and h' sqrt(M0+2) in the two
size sectors. All other displayed terms preserve the backbone projector.
The norm of the combined two-sector off-block is their maximum. Duhamel
applied to a state initially in Pi_back gives exactly (14). It bounds the
probability outside the backbone at a specified readout, not a measurement-
dependent first-passage event. Remaining inside a connected backbone implies
connectedness, while leaving it need not disconnect the full graph.

## 4. State-uniform strong-port control

This part uses blank registers and clamped g,V, as explicitly required in
the candidate. Identify Q with P via J, and let A be the complete old
compressed Hamiltonian including its clamped source/controller and supply.
After the stated scalar supply calibration, the paired block is

    A tensor I_branch + epsilon*I tensor sigma_x
          +[(h_N-h')S_rest] tensor |target><target|.

Its detuning norm is delta_N=Omega(N-1)/N. The creation term itself has
no paired-to-complement matrix elements. The source/target native leakage
norms are h_N and h' sqrt(2N+2), so the off-block norm is ell_N as stated.
Keeping the actual complementary Hamiltonian in the reference removes an
unnecessary assumption about its energy or gap. The difference between the
actual and exactly swapping reference has norm at most delta_N+ell_N.

At t_swap=pi*hbar/(2|epsilon|), the reference maps every eligible source
state into exact target Q. The actual norm outside Q is therefore at most
pi(delta_N+ell_N)/(2|epsilon|). Squaring gives (15); convexity extends it
from pure states to density matrices supported in the eligible source.
No uncontrolled large-system or rotating-wave approximation is involved.

The assumed positive available supply gap, clamping, initial eligibility
and finite port strength remain substantive inputs. Equation (15) is a
sufficient bound; an uninformative value is not a failed exact identity or
permission to retune a prospective experiment. It does not apply unchanged
to a moving quantum controller or to the extra carrier detuning/leakage.

## 5. Meaning for the program

The result establishes a mathematically consistent connected-growth operation
with accountable energy, a reversible channel and bounded native leakage.
The path alternates the bipartite arrows, so only undirected connectivity is
proved, not a new directed causal path. It cannot join initially separate
old components and does not supply three-dimensional geometry.

Physical distance remains an independent operational question. Static series
conductance distinguishes unchanged edge calibration from refined calibration,
but cannot establish equality of finite-frequency probe dynamics. That
distinction is developed separately in SUBDIVISION_OPERATIONAL_RULER_V001.md.
No cosmological expansion, permanent growth, native selection of this port,
or physical volume law has been certified by this analytical review.
