# Same-coefficient record feedback: exact ground response and paid-sector example

Date: 2026-09-27. Status: analytical ground-state comparison in a declared source-off, graph-only BS restriction. No numerical run, formation protocol, physical-volume rule, stress identification, or dark-sector abundance prediction.

Sources checked after resident-file flags: recovered [BS microscopic action](recovered_sources/BS_MICRO_ACTION.md), SHA256 00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec, especially BS06/BS10/BS11/BS13; and [native degree-manifold selection](NATIVE_DEGREE_MANIFOLD_CORRELATION_SELECTION_V001.md), SHA256 0c0f7c16a12d07122811b7a6e62e27605ed12464f358c342530a9928e4fcfaaf. The latter's fourth-order derivation and finite-N bounds are inherited, not numerically rerun here.

## 1. Generic finite-N theorem, without the selected coefficient example

In one N+N slab, take no carriers, all formation couplings off, uniform fixed record occupation q, and absent or graph-independent ports. Write the graph part as

\[
 H_g(a)=U\sum_v(d_v-d_*)^2+aM-h\sum_eX_e,\qquad
 M=\sum_e n_e,\quad a=\Delta-2\lambda_Rq,\quad h=\Omega/N>0.             \tag{1}
\]

All native coefficients are fixed when q changes between its physical values 0 and 1. For finite N≥1, the negative link-flip matrix elements connect the entire graph bit hypercube. The graph-only ground state is consequently unique and has strictly positive amplitudes on every graph configuration. Let E_g(a) denote its energy. Finite-dimensional ground-state perturbation theory gives

\[
 {dE_g\over da}=\langle M\rangle_a,\qquad
 {d^2E_g\over da^2}
 =-2\sum_{\nu>0}
 {|\langle\nu|M|g\rangle|^2\over E_\nu-E_g}<0.                          \tag{2}
\]

Strictness follows because a state positive on every bit string cannot be an M eigenstate: Var_g(M)>0, so at least one numerator is nonzero. Degenerate excited eigenvalues do not obstruct the summed formula. Thus at the SAME coefficients, for λ_R>0,

\[
 \langle M\rangle_{q=1}>\langle M\rangle_{q=0}.                         \tag{3}
\]

The comparison is valid at arbitrary h>0, not just in a weak-flip expansion. At h=0 degeneracies may occur, so strict smooth response is not asserted. Nor is a local clustering law or a response of an arbitrary retained state asserted.

One may use a continuous parameter x∈[0,1] to interpolate the two Hamiltonians, with a(x)=Δ−2λ_Rx. This is a differentiation device, not an assertion that the qutrit occupation eigenvalues are continuously variable. Along it, d⟨M⟩/dx=−2λ_R E_g''>0. Equation (2) is a static spectral derivative; no time-evolution convention for ħ is being suppressed.

## 2. Complete energy and an exact cost bound

Uniform record storage adds 2Nε_rq, not an arbitrary energy-zero adjustment. With the same other constants,

\[
 {\cal E}(q)=E_g(\Delta-2\lambda_Rq)+2N\epsilon_rq+E_{\rm other}.
\]

Identifying the same graph Hilbert space in the two fixed-record sectors,

\[
 H_1-H_0=2N\epsilon_r I-2\lambda_RM,\qquad 0\le M\le N^2I.
\]

The min–max principle therefore gives the exact, all-h comparison

\[
 2N(\epsilon_r-\lambda_RN)
 \le {\cal E}(1)-{\cal E}(0)
 \le 2N\epsilon_r.                                                     \tag{4}
\]

Equivalently,

\[
 {\cal E}(1)-{\cal E}(0)
 =2N\epsilon_r-\int_{\Delta-2\lambda_R}^{\Delta}
       \langle M\rangle_a\,da.                                        \tag{5}
\]

These statements include graph relaxation; they are not comparisons at an artificially common fixed graph. A sufficient strictly positive per-record insertion bound is

\[
 \Delta H_v=\epsilon_rI-\lambda_Rd_v
 \succeq(\epsilon_r-\lambda_RN)I>0.                                   \tag{6}
\]

This stronger condition is not supplied by a positive bare ε_r alone. It is checked explicitly in the example below.

## 3. One fixed coefficient set connects two degree manifolds

Choose once, for N=4,

\[
 U>0,\quad \lambda_R=2U,\quad \Delta=5U,\quad
 d_*={9\over4},\quad \epsilon_r=9U,\quad h={\Omega\over4}>0,
\]

with all g=0, no carriers, and no ports. The other onsite constants can be kept identical. For an explicit full BS13 sufficient-domain choice set the inactive carrier hopping coefficient t=0, giving δ_E=U. If retaining an inactive nonzero t for a separate prospective carrier use, |t|<U permits δ_E=U−|t|>0; absence of carriers does not erase the |t| in BS13's stated full-parent sufficient bound.

The same parameters give

\[
 d_{\rm eff}(q)
 =d_*-{\Delta-2\lambda_Rq\over4U}=1+q.                                \tag{7}
\]

Completing the square, with every constant retained, yields

\[
 H_q=C_q+U\sum_v[d_v-(1+q)]^2-h\sum_eX_e,
\]
\[
 C_0={65\over2}U,\qquad
 C_1={17\over2}U+8\epsilon_r={161\over2}U,                              \tag{8}
\]

apart from the same E_other on both sides. At h=0 the ground-sector energy difference is therefore 48U. No coefficient or energy reference was changed between q sectors. This is a selected illustrative subfamily chosen to expose the native mechanism, not a parameter determination from record formation, cosmological data, or the primary allocation hypothesis.

The all-h operator difference is

\[
 H_1-H_0=72U I-4UM,\qquad
 8U I\preceq H_1-H_0\preceq72U I.                                    \tag{9}
\]

Also each local insertion obeys ΔH_v=9U−2Ud_v≥U. In the unrestricted source-off record-occupation family this means the all-blank record sector has lower ground energy than any occupied sector. The occupied-sector graph ground state is conditional on its retained q pattern, not the full system's global ground state.

There is a sharper example-specific lower bound for h>0. At q=1 the completed graph Hamiltonian is invariant under global link complement, so ⟨M⟩_(a=U)=8 exactly. Strict monotonicity gives 0<⟨M⟩_a<8 for U<a≤5U. Inserting this into (5),

\[
 40U<{\cal E}(1)-{\cal E}(0)<72U\qquad(h>0).                            \tag{10}
\]

Thus positive cost is exact and does not depend on trusting a truncated expansion.

## 4. Weak-flip ground energies and correlation comparison

For q=0, d0=1: the regular manifold contains 4!=24 perfect matchings. An alternating-square switch exchanges the assigned right partners of two left nodes, so every matching has C(4,2)=6 switches. The positive uniform orbit vector has switch eigenvalue 6. The fourth-order diagonal coefficient from the inherited derivation is −2h⁴/U³. Hence

\[
 {\cal E}(0)=E_{\rm other}+{65\over2}U
 -{8h^2\over U}-{17h^4\over U^3}+O(h^6/U^5).                          \tag{11}
\]

For q=1, d0=2: the 72 C8 and 18 two-C4 configurations have normalized switch quotient [[8,8],[8,0]], largest eigenvalue 4+4√5, and diagonal correction −(14/3)h⁴/U³. Therefore

\[
 {\cal E}(1)=E_{\rm other}+{161\over2}U-{8h^2\over U}
 -\left({44\over3}+10\sqrt5\right){h^4\over U^3}
 +O(h^6/U^5),                                                        \tag{12}
\]
\[
 {\cal E}(1)-{\cal E}(0)
 =48U+\left({7\over3}-10\sqrt5\right){h^4\over U^3}
 +O(h^6/U^5).                                                        \tag{13}
\]

The equal second-order terms cancel; the quartic difference lowers, but does not eliminate, the paid storage-sector gap. These are fixed-N asymptotic formulas for the isolated weak-flip ground branches. The inherited conservative sufficient band-isolation condition is 16h/U=4Ω/U<1; substantially smaller values control the expansion. No numerical remainder coefficient is certified.

Within the corresponding ground-state limits, q=0 has mean link 1/4 and square count 0. For q=1, mean link 1/2 is exact for every h>0, while the weak-flip square expectation tends to 1−1/√5. Thus the same record-dependent native energy law can change both preferred degree and correlation selection, with no microscopic loop term added. This does not make weighted mean K_(4,4) a local geometry or identify these variables with physical mass or stress.

## 5. What the result does and does not supply

Equations (2)–(3) are a generic conditional ground-response law; equations (7)–(13) are one explicitly selected same-coefficient illustration. They show that record occupation can change the graph energy landscape and its low-energy correlation structure without parameter retuning. This is forward mechanism content beyond a one-link response.

In this hold, all record q_v are conserved. An initial q=0 state cannot reach q=1 under that hold, and a closed unitary does not automatically track either ground branch. To use the comparison as a formation mechanism, the native formation/source completion must supply the positive energy and a demonstrated route to the appropriate graph state. Neither passive retention nor an energy-lowering link feedback makes formation free.

The next falsifiable analytical target is the same-coefficient conditional ground comparison (11)–(13) together with the native square observable, under a prospectively owned ground-preparation or ground-validation protocol. This note itself performs no such protocol and does not substitute this subfamily for the primary active/maintenance construction.
