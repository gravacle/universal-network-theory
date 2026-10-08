# Independent review of the uniform native source bound

2026-09-30. Reviewer: `urm_dark_integration`. **PASS for the stated exact conditional bounds.** The proof applies to the specified isolated degree-two graph family and owned energy source. It neither completes the physical model nor excludes all static, high-band or nonstationary mechanisms. No numerical execution, scientific import, compilation, enumeration or eigensolve was performed.

## Exact reviewed sources

Paths are relative to `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation` in `/Users/bgm/Documents/ChatGPT/Universal Network Theory`.

| Source | SHA-256 |
| --- | --- |
| `NATIVE_REGULAR_GRAPH_UNIFORM_SOURCE_BOUND_V001.md` | `0d4785027238d9c3e69662fd918888ebf1769d435a26b7e5f2b049802fd7a2c3` |
| `NATIVE_REGULAR_GRAPH_ENERGY_SOURCE_SELECTOR_V001.md` | `daa31272997620537d7d0395d587d2fe954617d9796f52570f8018d6019adacb` |
| `NATIVE_REGULAR_GRAPH_ENERGY_SOURCE_SELECTOR_REVIEW_INDEPENDENT_V001.md` | `5efe4eda1000bcf7f16c1096f662b0b0889b25d73322f05e55adc073139d7d64` |
| `../NATIVE_UNIFORM_REGULAR_DEGREE_BOUND_V001.md` | `c1cf35ca125b809c748549df0f2bf5013245dc42a598189584f2b0fc85a5c592` |
| `NATIVE_SHARED_WORK_INTEGRABILITY_V001.md` | `ec4b6e2e8b02a39f567d34617520afc23cde7e7cb4fe44f4b1f5fe5d62a35755` |
| `NATIVE_ENERGY_DIPOLE_GRAVITY_BRIDGE_V001.md` | `81b3c455d761667e2645117699e8986c7030290de8b54bc45879112237d2db96` |

The new note was read fully and its final scope/sign amendments inspected. All listed bytes were rehashed directly. The applicable star-bound, isolated-band, source-selection and work premises had been read fully for this review and its immediately preceding selector review. This is an independent hand proof check, not a numerical reproduction or a complete audit of unrelated historical receipts.

## Whole-band quadratic form and source norm

The essential extension is valid: since every eigenvalue in the exact retained band is below C_N, every normalized superposition in that band also has expectation below C_N. Combining this with the statewise star inequality gives `kappa <= 2 Omega² b_N/a_N²`. No eigenvector-only estimate is improperly promoted to an operator bound.

For a real centered profile with absolute values at most one, the uniform c0 contribution cancels exactly. Bounding each weighted star before summation gives `(U+Omega q_N) kappa + Omega sqrt(2 b_N kappa)`. At the allowed maximal kappa, the square-root term equals `a_N kappa`; the coefficients sum to 2U. The displayed compressed Hermitian operator norm `L_N=4U Omega² b_N/a_N²` follows from its bound on every normalized retained vector.

The uniformity claim retains the strict small-Omega isolation condition and fixed microscopic coefficients. It is not a theorem at the inherited Omega=U=1. Nonuniform scalar source baselines must be subtracted or retained explicitly as affine work; they cannot be included in this centered norm bound without their own term. The author now states the uniform/absent spectator restriction.

## Ground subtraction and symmetry

The measure uses `Pi_ex=Pi-|0><0|`, so its weight is excited-state transition weight, not the norm of an unremoved mean energy. The Hermitian Gram matrix is positive semidefinite and invariant under independent layer permutations and layer exchange. Its two standard blocks are equal scalar matrices, their cross block vanishes, and the uniform and two-plane singlets have no low-band transitions. Hence `W_u=w_N Q_u` is exact, including internal degeneracies, rather than a fitted isotropy assumption.

The even-N balanced profile has Q=2N; the odd-N profile with one zero in each layer has Q=2(N-1). Both are bounded and separately centered on each layer. For the single-node centered profile Q=1-1/N, the stated `W_anchor <= L_N²/(2N)` holds for both parities, with the first displayed bound slightly tighter at even N. This gives an exact O(1/N) low-band source-weight bound at fixed calibration, not just a fourth-order extrapolation.

## Response and complete finite-source work

For the PLUS-source Hamiltonian, the response is minus the convolution with the displayed causal chi. The sine-kernel estimate gives `2W/hbar`; its finite-time integral is bounded by `2TW/hbar`. Maximizing `2Delta/(Delta²+(hbar zeta)²)` over positive Delta gives `1/(hbar zeta)`, proving the positive-imaginary-frequency bound. It supplies no pointwise bound at an undamped real-frequency resonance. It also does not bound static inverse-gap susceptibility: a vanishing weight can be concentrated at an even smaller gap.

The added finite-lapse result is independently valid without low-band perturbation theory. Positive lapse weights give a diagonal cost at least `U(1-epsilon)K` and flip bound at most `(1+epsilon)` times the unweighted star estimate. Minimizing the resulting quadratic in sqrt(kappa) produces the displayed B_N. A regular computational graph still has the complete energy C_N, so it gives the upper trial bound. Ground-energy concavity and the zero centered-source mean at theta=0 give equation (16) on both signs of theta; no evenness of E(theta) is assumed. Positive edge flip amplitudes retain the connected stoquastic hypercube and unique finite-N ground, justifying the local derivatives.

This second result bounds full finite-source work and averaged full curvature. It does not convert the preceding low-band spectral measure into a full-response measure, or bound pointwise static curvature uniformly in N. High-state contributions and induced contacts remain necessary after any elimination.

## Physical normalization and disposition

The conversion `Z=(R_N/c²)T_u`, the Q_x refinement, and the conditional volume bounds carry the appropriate squared source calibration. No physical V_N, radius law or volume proportional to node count is supplied by the graph theorem. Fixed theta is not fixed physical acceleration when R_N grows. The conditional extensive-volume and three-dimensional-radius examples preserve this distinction.

The harmonic gap in equation (18) must use both **low-band** weight and **low-band** static susceptibility. It is a necessary condition for a static mechanism claimed to arise from that band, not a bound on the neighboring full-response curvature. This locality of scope and the imaginary-frequency/real-resonance distinction were clarified during review; the final author bytes include both, together with the correct source sign and causal support. No coefficient or numerical tolerance was changed.

The result is stronger and more relevant than an unweighted soft-eigenvalue count: within the stated family, a proposed finite-time or positive-imaginary-frequency low-band response must respect the exact source-weight suppression. A surviving static proposal still owes a controlled weighted inverse-gap limit, nonlinear response, physical source/clock/volume and actual formation/readout. The theorem does not establish an attractor, select the universe's state, derive a metric or eliminate DM/DE assumptions.

No new oracle or numerical run is required to state these analytic bounds; any later implementation test needs its own frozen protocol and independent preflight. All eleven mandatory program lanes and physical-promotion gates remain open. The author note, earlier incomplete review, handoff snapshots, numerical evidence, main ledger and URM files were not edited by this reviewer. The writing skill guided the separation of theorem, assumptions and uncompleted physical obligations in this local review.
