# Occupation-weighted source-specific carrier control

Date: 2026-09-27. Status: exact analytical hold identities for a new prospectively frozen source-specific test; no numerical reconstruction, propagation, old-state-file recovery, or record-readability assertion.

Source: resident recovered [BS microscopic action](recovered_sources/BS_MICRO_ACTION.md), SHA256 00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec, checked for resident flags before reading BS06–BS11. The signed-current convention and equal-state commutator method follow [fixed-source carrier current](NATIVE_FIXED_SOURCE_CARRIER_CURRENT_V001.md). This note keeps the actual retained occupation projector and removes only its own feedback contribution, not all record feedback.

## 1. Source, controls and inclusive readouts

On the N=2 slab, label links n_ij from Li to Rj. The formation targets in the intended fixed-content realization are L0 and R0. At the start of the hold, let ρ_* be the same complete, possibly complex and correlated state for every control. No carrier reset, record measurement, graph factorization or hard replacement of an occupied record is assumed.

Set

\[
 q=q^r_{R0},\qquad K_{R0}=n_{00}+n_{10},\qquad
 F_{R0}=-\lambda qK_{R0},\qquad A=H-F_{R0}.                           \tag{1}
\]

H is the native hold with all formation/copy couplings g=0 and no ports. A removes only the R0 record's contribution. In the two-target realization, the remaining L0 contribution −λq^r_(L0)(n_00+n_01) is retained, including its part on the shared link n_00. Storage, carrier hopping, current-squared feedback, graph flips and degree penalties are unchanged.

Define carrier-position operators N_v and the fixed readouts

\[
 D=N_{R0}-N_{R1},\qquad
 O=qD,\qquad B=(I-q)D,\qquad D=O+B.                                  \tag{2}
\]

O and B are unnormalized inclusive joint observables. They are not conditional expectations divided by an occupation probability. Positive O means that the occupied-R0 contribution favors carrier position R0 relative to R1; its sign or magnitude alone does not demonstrate newly generated motion.

## 2. Exact conservation and the all-time blank-control null

During this hold,

\[
 [H,q]=[A,q]=0,\qquad q^2=q,\qquad [q,D]=0.                           \tag{3}
\]

Thus p=Tr(ρ_*q) is conserved in both controls. On the blank sector Q_0=I−q, the removed term vanishes identically:

\[
 HQ_0=AQ_0,\qquad
 e^{-iH\tau/\hbar}Q_0=e^{-iA\tau/\hbar}Q_0.
\]

Consequently

\[
 B_H(\tau)=B_A(\tau)
 \quad\hbox{as operators for every }\tau,\qquad
 \Delta\langle B(\tau)\rangle=0.                                     \tag{4}
\]

Here Δ means native H minus source-only-ablated A, with the same ρ_*. This is the null of the CONTROL DIFFERENCE, not the claim B(τ)=0: carrier motion in the blank branch can occur under the common restricted Hamiltonian.

Initial coherences between occupied and blank record sectors do not invalidate (4). The holds conserve the sectors and the readouts are block diagonal in q. No physical measurement or branch postselection is required for the identity.

Equation (2) therefore gives the exact all-time equality

\[
 \Delta\langle D(\tau)\rangle=\Delta\langle O(\tau)\rangle.             \tag{5}
\]

Useful inclusive checks are

\[
 |\langle O(\tau)\rangle|\le p,\qquad
 |\langle B(\tau)\rangle|\le1-p,\qquad
 |\Delta\langle O(\tau)\rangle|\le2p.                                 \tag{6}
\]

All these bounds apply without dividing by p, including p=0. A small signal may reflect a small occupied weight; it must not be inflated by silently normalizing or replacing q by 1.

## 3. Source-specific early-time identity and sign

Use the native oriented current

\[
 J_{ij}=i(|Rj\rangle\langle Li|-|Li\rangle\langle Rj|).
\]

For D, its endpoint differences are +1 on links to R0 and −1 on links to R1. Thus

\[
 {i\over\hbar}[H,D]
 ={t\over\hbar}
 [n_{00}J_{00}+n_{10}J_{10}-n_{01}J_{01}-n_{11}J_{11}].               \tag{7}
\]

The same current operator holds for A. Multiplication by q gives the exact current of O, since q commutes with either hold.

Write ad_H(X)=[H,X]. The feedback F_R0 commutes with D and with [A,D], because it contains only commuting occupation projectors. Hence

\[
 \operatorname{ad}_H^kD=\operatorname{ad}_A^kD
 \quad(k=0,1,2).
\]

Multiplying by q proves the same identities for O. For B they extend to all orders by (4). The cubic operator difference is

\[
 \operatorname{ad}_H^3D-\operatorname{ad}_A^3D
 =[F_{R0},\operatorname{ad}_A^2D]
 =iht\lambda q(X_{00}J_{00}+X_{10}J_{10}),                           \tag{8}
\]

where h=Ω/N. Only the graph-flip part of the second commutator contributes: [X,n]=iY and [n,Y]=iX. The R1 terms in the current commute with this source-specific feedback, and the L0 feedback is not removed.

Because q²=q, the cubic operator difference for O is exactly the same as for D. Therefore

\[
 \Delta\langle O\rangle^{(k)}(0)
 =\Delta\langle D\rangle^{(k)}(0)=0\quad(k=0,1,2),
\]
\[
 \Delta\langle O\rangle'''(0)
 =\Delta\langle D\rangle'''(0)
 ={ht\lambda\over\hbar^3}
 \left\langle q(X_{00}J_{00}+X_{10}J_{10})\right\rangle_{\rho_*}.       \tag{9}
\]

Equivalently the cubic Taylor coefficient is the right side divided by 6. This is a joint record–link–carrier correlation, not a product of separately measured means. Its sign is not fixed by q≥0 or λ≥0.

If ρ_* is real in the computational graph/record/carrier basis, both hold readout expectations are even in time and (9) vanishes. An actual unitary post-write state need not be real even when its pre-write blank preparation was real. These identities require no such reality assumption.

The requested h=1, t=1/2, λ=1/2 give htλ=1/4. In a calculation using ħ=1, the source-specific joint moment in (9) equals four times the third DERIVATIVE difference, not four times its cubic Taylor coefficient. A previous all-feedback-off cubic result uses a different operator and cannot be reused as this source-only moment.

## 4. Explicit energy ownership

A physical sudden source-feedback removal at the shared initial state changes the Hamiltonian by −F_R0, so its work is

\[
 W_{R0}=\operatorname{Tr}\rho_*(A-H)
 =\lambda\langle q(n_{00}+n_{10})\rangle_{\rho_*}\ge0.                 \tag{10}
\]

This is additional to any common work associated with switching the formation coupling g to zero. The same density matrix in both holds does not mean the two hold energies are equal. R0 record storage is still present in A; the control neither deletes that energy nor turns an occupied record blank.

An offline paired propagation is a legitimate diagnostic of the term's contribution, but is not evidence that physical removal or record formation is free. The counterfactual keeps λ's role in all other record terms fixed.

## 5. Intended use and claim boundary

The requested reconstruction uses the previously specified native coefficients h=1, t=1/2, λ_R=1/2, U=1, d_*=1, Δ=4, λ_J=1/4 and ε_ψ=ε_r=1. Its prospective formation protocol starts with blank target records, an empty graph and a carrier at L0, uses the frozen g=1 write duration 1, then switches g to 0 for the hold. These numbers do not replace the required source matrices, unit conventions, state ordering and source-version hashes in the separate frozen 256-state protocol. This note neither reconstructs that state nor claims to recover the unavailable historical state file.

The theorem applies to whatever complete ρ_* that authenticated reconstruction produces. Hold curves should retain the initial values and report O(τ)−O(0) as well as the equal-state contrast ΔO(τ); a positive inherited joint occupation bias is not by itself a newly produced sourceward effect. The exact checks are conservation of p, the all-time blank difference (4), equality (5), and the first three derivative statements (9).

These are occupation-weighted inclusive observables, not claims that q=1 establishes REC, SEALED, hard readability, a successful history-conditioned mission, or a physical mass source. The records do not move in this hold. A verified nonzero (9) or finite-time ΔO would establish a source-specific native carrier response in the retained state, not a universal attractive force, metric, dark-matter transport law, or dark-energy stress.
