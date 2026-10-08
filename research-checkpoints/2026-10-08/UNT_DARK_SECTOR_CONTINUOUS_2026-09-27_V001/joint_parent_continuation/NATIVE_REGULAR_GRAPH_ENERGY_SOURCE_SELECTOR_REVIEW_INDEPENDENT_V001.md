# Independent review of the native graph energy source selector

2026-09-30. Reviewer: `urm_dark_integration`. This completes the source-only review paused in `NATIVE_REGULAR_GRAPH_ENERGY_SOURCE_SELECTOR_REVIEW_INCOMPLETE_V001.md`; that checkpoint and the author note remain unchanged.

**Verdict: PASS for the conditional analytic selector and its stated finite-N leading coefficients.** No blocking algebra or source-provenance defect was found. This is not numerical reproduction, a finite-h error certificate, an execution preflight, physical source completion or Stage 3 qualification. No scientific source was imported, compiled or executed, and no combinatorial enumeration or eigensolve was performed.

## Reviewed identities

Paths are relative to `UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation` under the sole project root `/Users/bgm/Documents/ChatGPT/Universal Network Theory`.

| Source | SHA-256 |
| --- | --- |
| `NATIVE_REGULAR_GRAPH_ENERGY_SOURCE_SELECTOR_V001.md` | `daa31272997620537d7d0395d587d2fe954617d9796f52570f8018d6019adacb` |
| `../recovered_sources/BS_MICRO_ACTION.md` | `00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec` |
| `../NATIVE_UNIFORM_REGULAR_DEGREE_BOUND_V001.md` | `c1cf35ca125b809c748549df0f2bf5013245dc42a598189584f2b0fc85a5c592` |
| `../NATIVE_DEGREE_MANIFOLD_CORRELATION_SELECTION_V001.md` | `0c0f7c16a12d07122811b7a6e62e27605ed12464f358c342530a9928e4fcfaaf` |
| `NATIVE_DEGREE_SWITCH_CHANNEL_V001.md` | `bd52d3200aa758613471f9d1053a402d8c3e7560420a3da99357787acf082f23` |
| `NATIVE_SWITCH_GRAPH_RESULT_V001.md` | `8c672140d11a44681eb8c46e0253f7d504a9b512c1398bbff5aab70199a2c8df` |
| `NATIVE_RECORD_CONNECTIVITY_PATHWAY_V001.md` | `81bbb3b72e00c03475b8efcc63c861907adb8b0da72bd50f27c89a6bc0b6775c` |
| `NATIVE_ENERGY_DIPOLE_GRAVITY_BRIDGE_V001.md` | `81b3c455d761667e2645117699e8986c7030290de8b54bc45879112237d2db96` |
| `NATIVE_SHARED_WORK_INTEGRABILITY_V001.md` | `ec4b6e2e8b02a39f567d34617520afc23cde7e7cb4fe44f4b1f5fe5d62a35755` |
| Preserved incomplete review | `48ab524c927c78999c825b5d6083fd996195974845d2caf8c172fe28743d330e` |

The author note and the applicable mathematical/source premises were read fully across the initial and resumed review. These final byte identities were checked directly. The earlier N=4 numerical result is used only as recorded provenance, not independently reproduced here.

## Source ownership and exact selection rules

BS06 and BS11 give the stated graph restriction when carriers are blank, record occupations are uniformly fixed and formation/graph-dependent ports are off. Completing the square with `a=Delta-2 lambda_R q` and `d_star=k+a/(4U)` yields the complete constant C_N and the displayed local constant c0. Neither is a disposable energy shift in source or volume work. This centered degree family is a declared parameter restriction, not a consequence of the inherited blank-state formation dynamics.

The symmetric endpoint allocation in the energy-dipole bridge reduces to the stated local h_v in this carrier-free sector. BS03 requires permutation-covariant comparisons or physically anchored ports; BS12 is a completion slot, not an already supplied apparatus. Thus fixed x_v, c, positive weak lapses and their energy-conjugate interpretation remain adopted calibration/source data. The author correctly does not infer them from node count, degree or graph labels. Spectator terms must remain located and accounted for if included; adding graph-dependent ports or carriers would require a fresh selection analysis.

For k=1, opposite-layer transitivity excludes the left-standard/right-trivial and right-standard/left-trivial representations in the matching space, whose singlet is unique. The node-energy source acting on the invariant ground can therefore have no excited low-band component. For feasible degree-two N at most four, stabilizer transitivity similarly excludes the single-layer standard representations. Each degree-two topology is layer-transpose equivalent, so the orbit singlets are layer-even. Together with total-energy conservation of the uniform source, this proves the two-plane source is dark in the isolated low band for every feasible degree-two N.

These statements use the full graph Hamiltonian's unique invariant ground at h>0 and isolated-band transport preserving both node permutations and layer exchange. They do not apply to arbitrary excited/prepared states, nor remove high-band response. The positive-cost connectivity bound and the centered small-Omega band theorem have different premises, as the author states. No gap theorem at inherited Omega=U=1 is inferred from either bound.

## Dressed insertion and diagonal terms

The four flip numerators and three intermediate denominators make each complete switch amplitude homogeneous of degree one in its four node lapses. Rectangle symmetry makes the four first derivatives equal at unit lapse, giving `g4/4`. The sign remains negative in the effective Hamiltonian and its off-diagonal source insertion. The local-energy perturbation, rather than an independently normalized edge probe, is essential to this coefficient.

The projected canonical connection begins at order h²; the zero-source terms through second order are scalar on P. Hence its first commutator with the non-scalar fourth-order switch operator enters at order h⁶. This justifies the leading insertion, not omission of finite-h connection or contact terms.

Returning paths through order four cannot introduce a graph-dependent centered diagonal source. At second order each edge-return contribution is `-h²(ell_u+ell_v)/(4U)`, giving equal per-vertex derivatives. At fourth order a diagonal path uses one edge repeatedly or two distinct edges twice. The derivative can distinguish a shared center, a shared leaf or a disjoint endpoint, but all these counts are fixed by N and k. For example, at a fixed vertex the shared-center occupied/occupied, empty/empty and mixed pair counts are `binom(k,2)`, `binom(N-k,2)` and `k(N-k)`; the corresponding shared-leaf counts are `k(k-1)`, `(N-k)(N-k-1)` and `2k(N-k)`. Disjoint counts follow by subtracting the two endpoint stars from the fixed global occupied/empty totals. Folded second-order contributions and their first derivatives are scalar as well. The centered first derivative therefore vanishes without dropping its absolute or uniform-source energy.

## N5 bright line and its limitations

The hand derivation confirms the 1,440/600 topology counts, switch rows 15+10 and 24+3, quotient off-diagonal `4 sqrt(15)`, maximum eigenvalue `9+2 sqrt(69)` and per-graph ratio `(sqrt(69)-3)/5`. The distinction between normalized orbit amplitudes and per-graph coefficients is preserved.

On C4+C6, the merging-switch vertex counts 12/8 give `4 X4`, and the three internal C6 switches give `-2 X4`. Their weighted source action is consequently `-g4(u-v/2)X4/c²`. Vertex transitivity cancels the C10 contribution. The same symmetry makes the sum over split targets zero at C10, while the three internal switches preserve X4, proving the adjacency eigenvalue 3. Uniform independent two-subsets of each five-node layer give variance `3 Q_x/10`; multiplication by 600 yields `sum X4²=180 Q_x`.

The displayed gap and weight therefore give the entire **leading** low-band measure for this conditional ground branch. At finite h the higher-order operator may split or redistribute the leading line. The error symbols hold at fixed finite N, U and calibrated profile, with no numerical error constant supplied. Uniform separation from the Q band does not control the remainder relative to a shrinking within-band spectral window as N grows. The first bright case means the first in this specified k=1/k=2 sequence, not the first possible native mechanism generally.

For fixed finite N, weakening h makes both this gap and its static susceptibility vanish as h⁴. It does not create the required continuum weight by itself. A two-plane profile has Q_x=0 and retains the exact dark control. Changing the anchored profile is a different declared apparatus, not a derived emergent geometry or a free normalization.

## Coupled work and next gate

Under the explicitly adopted restricted A scaling, energies/gaps scale as exp(-eta) while the centered dipole stays fixed, so susceptibility scales as exp(eta). Under B the scalar baseline shifts without changing gaps and the dipole scales as exp(eta), yielding exp(2 eta). The shared-work mixed derivative identity follows from the same differentiable ground branch and independent source coordinates. The raw affine source has zero microscopic acceleration contact, but eliminated-state/chart contacts and high-band response remain compulsory in total work.

These checks leave source calibration, physical volume/density, absolute B baseline, formation and a controlled increasing-size nonlinear reduction unresolved. A positive ground-state line is not proof that the actual network prepares a passive state or reproduces galaxy and expansion data. All eleven mandatory lanes and physical-promotion gates remain open.

The next implementation step may be the proposed exact finite combinatorial/source oracle, but it still needs its own prospective source, protocol, resource limits and independent execution preflight. This review does not create or authorize that numerical packet. No author source, incomplete review, handoff snapshot, frozen result, URM integration or main ledger was changed. The writing skill was applied only to keep this local review explicit about provenance and claim scope.
