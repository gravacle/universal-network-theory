# Fixed-source native carrier current and equal-state feedback control

Date: 2026-09-27. Status: exact operator identities and short-time conditions; no numerical job, mean-link replacement, new hopping term, formation reset, or physical-force identification.

Source: resident recovered [BS microscopic action](recovered_sources/BS_MICRO_ACTION.md), SHA256 00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec. Flags were checked before reading BS06–BS11. Work on one slab, in the one-carrier fixed-content sector, with all formation/copy couplings g=0 and no ports. Record occupations are fixed on the hold. The operator identities below also allow retained quantum q_v projectors and a correlated initial state, because the proof uses their commutation properties, not a projection onto a particular q pattern.

## 1. Signed current into a prospectively fixed source set

Write N_v=|v⟩⟨v| for carrier position and orient each possible link e=(u,v) from the left to the right layer. The native BS07 convention is

\[
 T_e=|v\rangle\langle u|+|u\rangle\langle v|,\qquad
 J_e=i(|v\rangle\langle u|-|u\rangle\langle v|),\qquad
 J_e^2=N_u+N_v.
\]

The carrier terms are

\[
 H_\psi=\epsilon_\psi I-t\sum_e n_eT_e
              +\lambda_J\sum_e n_e(N_u+N_v).
\]

For a fixed, prospectively declared label set S, let P_S=Σ_(v∈S)N_v and δ_S(e)=1_S(v)−1_S(u). The exact inward carrier current is

\[
 I_S={i\over\hbar}[H,P_S]
 ={t\over\hbar}\sum_e\delta_S(e)n_eJ_e,\qquad
 {d\over d\tau}\langle P_S\rangle=\langle I_S\rangle.                  \tag{1}
\]

For S={v} at the right endpoint, positive t⟨n_eJ_e⟩/ħ is inward; the left endpoint has the opposite sign. Internal edges cancel from a set's net current. This is a native continuity statement for the mobile ψ carrier, not for the record r: every q_v remains conserved on this hold.

The graph flips, graph degree energy, record feedback and storage commute with P_S. So does the current-squared energy λ_JΣ n_e(N_u+N_v). They do not contribute directly to (1), but can change the state and all later current responses. Commutation with P_S is not permission to discard their energies or dynamics.

## 2. A localized launch measures incidence at leading order

Suppose the actual initial preparation is ρ_G⊗|u⟩⟨u|, with u outside S, and G includes retained record factors if needed. Then

\[
 \langle P_S(\tau)\rangle
 ={t^2\tau^2\over\hbar^2}
   \sum_{\substack{v\in S\\(u,v)\ {\rm possible}}}
       \langle n_{uv}\rangle_{\rho_G}
 +O(\tau^3).                                                        \tag{2}
\]

This follows from the exact first-arrival norm Tr[ρ H P_S H]/ħ² and n_e²=n_e; no replacement of n_e by its mean inside the Hamiltonian is made. If the initial density matrix is real in the graph/position basis, the probability is even in τ and the remainder after (2) is O(τ⁴).

For a disjoint matched blank set B, with the same number and prospective possible-link relationship to u,

\[
 \langle P_S(\tau)-P_B(\tau)\rangle
 ={t^2\tau^2\over\hbar^2}
 \left[\sum_{v\in S}\langle n_{uv}\rangle
       -\sum_{w\in B}\langle n_{uw}\rangle\right]+O(\tau^3).           \tag{3}
\]

A strictly positive bracket establishes a positive sufficiently-small-time access difference. Positive arrival at S alone merely shows conductance; B can have the same or greater arrival. Equal means remove this leading difference but do not determine later signs.

An exactly pure localized carrier marginal already forces factorization with the rest of the system. A generic post-formation joint state need not have such a marginal. Conditioning it on finding the carrier at u selects a conditional graph state; resetting the carrier to u discards correlations. Neither operation may be substituted silently for retaining the actual formed joint state.

For a general correlated initial state, the instantaneous current is the joint expectation in (1), not ⟨n_e⟩⟨J_e⟩. If the carrier already overlaps S or B, report the net change

\[
 G_{S,B}(\tau)=
 \langle(P_S-P_B)(\tau)\rangle-\langle P_S-P_B\rangle_0
\]

alongside its initial bias and current. Carrier coherence between several launch nodes can also make higher joint link correlations enter the first-arrival norm. Equation (3) is not a formula for an arbitrary formed state.

## 3. Equal-initial-state feedback removal: first two derivatives are identical

Separate the record–incidence feedback from all the otherwise unchanged native terms:

\[
 H=A+F,\qquad
 F=-\lambda_R\sum_e r_e n_e,\qquad r_e=q_u+q_v.
\]

Compare evolution under H and A starting from the SAME complete density matrix ρ_0, using the SAME fixed readout P_S. This removes feedback during hold; it does not erase records, change their storage energy, or substitute a separately formed blank-control state.

Writing ad_H(O)=[H,O],

\[
 [F,P_S]=0,\qquad [F,[A,P_S]]=0.
\]

The second identity holds because [A,P_S]=−itΣ_eδ_S(e)n_eJ_e and F commutes with every n_eJ_e. Hence the operator identities

\[
 \operatorname{ad}_H^kP_S=\operatorname{ad}_A^kP_S
 \quad(k=0,1,2),
\]
\[
 \operatorname{ad}_H^3P_S-\operatorname{ad}_A^3P_S
 =[F,\operatorname{ad}_A^2P_S]                                      \tag{4}
\]

hold for every shared initial state, including complex formed states.

There is an explicit native form for the cubic term. With h=Ω/N and the standard Pauli Y, [X_e,n_e]=iY_e and [n_e,Y_e]=iX_e. Only the graph-flip contribution to ad_A²P_S fails to commute with F; it is −htΣ_eδ_S(e)Y_eJ_e. Therefore

\[
 [F,\operatorname{ad}_A^2P_S]
 =i h t\lambda_R\sum_e\delta_S(e)r_eX_eJ_e,
\]
\[
 \left.{d^3\over d\tau^3}
  [\langle P_S(\tau)\rangle_H-\langle P_S(\tau)\rangle_A]
 \right|_{\tau=0}
 ={h t\lambda_R\over\hbar^3}
       \sum_e\delta_S(e)\langle r_eX_eJ_e\rangle_{\rho_0}.              \tag{5}
\]

Thus the leading possible equal-state feedback effect is

\[
 \langle P_S(\tau)\rangle_H-\langle P_S(\tau)\rangle_A
 ={h t\lambda_R\tau^3\over6\hbar^3}
       \sum_e\delta_S(e)\langle r_eX_eJ_e\rangle_{\rho_0}
 +O(\tau^4).                                                        \tag{6}
\]

All units are explicit: I_S has inverse-time units, and the cubic coefficient has inverse-time cubed units.

For real ρ_0 in this basis, the expectation in (5) vanishes, since X_eJ_e is purely imaginary. In fact both position probabilities are then even in time. Fixed record occupations alone do not make a post-write quantum state real. A complex formed joint state can have a nonzero third derivative. A strictly localized pure carrier also makes (5) vanish by factorization and ⟨J_e⟩=0, even if the graph state is complex.

The same identities apply to P_S−P_B by linearity. They show why a source-side τ² access excess does not by itself isolate ongoing feedback: that excess is already encoded in the shared initial incidence state and survives through second order with F removed.

## 4. The empty-graph counterpoint is a separate, stronger preparation assumption

For N=2, source R0, matched blank R1 and launch L0, an initially empty graph has no τ² arrival. The independently checked [native record-anchored carrier-access derivation](NATIVE_RECORD_ANCHORED_CARRIER_ACCESS_V001.md) keeps all four link flips, carrier hopping and λ_J terms. It finds equal leading τ⁴ arrivals and a τ⁶ source-minus-blank bias whose sign can be either positive or negative at admissible fixed coefficients.

That result applies to its real empty-graph preparation, not to every state with equal mean links and not automatically to an actual formed joint state. Its exact source-swap control preserves initial energy and holds the readout labels fixed. Its full word expansion and sign examples are owned by that note, not duplicated here.

## 5. Honest control and interpretation

The equal-state H versus A comparison is an analytical Hamiltonian ablation. A physical sudden removal of F would perform work

\[
 W_{\rm removal}
 =\operatorname{Tr}\rho_0(A-H)
 =-\langle F\rangle_0
 =\lambda_R\sum_e\langle r_en_e\rangle_0\ge0,                          \tag{7}
\]

and needs a declared controller. This is not an energy-matched control merely because its initial density matrix is identical. An offline matched-state propagation can still diagnose the feedback contribution without claiming that switching is free.

The source and blank sets must be fixed before examining the response. Permutation-covariant source/readout exchanges can test label artifacts, but changing the readout with the source would change the comparison. A formed-state test should preserve its actual correlations and compare matched readouts and Hamiltonian controls before asserting sourceward influence.

These observables measure native carrier access and current relative to declared labels. They do not move the conserved records, establish a physical spatial force, or derive a metric or gravitational mass. The immediate source-owned test is the equal-actual-state feedback-on/off comparison, including the initial current and the first nonvanishing difference, rather than a reconstructed product-state substitute.
