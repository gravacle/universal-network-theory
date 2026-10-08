# Native finite-star response and the flat-rotation constitutive test

2026-09-27. Analytical screen only; no numerical run, new microscopic law, gravitational coupling, or state preparation. Construct ID: `NATIVE_Q4_STATIC_TO_LOCAL_GRAVITY_COMPARISON_V001`.

**Result.** The conditional finite-star minimum-energy envelope has a finite positive susceptibility and strictly positive analytic curvature at every interior selected state. This supplies neither spatial gravity nor an acceleration-dependent stiffness. In a separately specified local isotropic potential theory, an exactly flat, nonzero asymptotic circular speed requires a cubic field-gradient energy, not a real-analytic function of the squared gradient. The latter restriction is conditional, not a universal UNT no-go or a rejection of finite-range galaxy phenomenology.

## 1. Source-owned finite Hamiltonian and the conditional selection

Read completely after resident flag checks:

- `program-worktree/LANE_CROSS_RFT_GRA_GL6U_F3_DEGREE_INTERACTION_Q4_RESPONSE_V001/THEOREM.md`, SHA256 `3f23084cd7e5fa500d331c6e9739b6f0b3e7875bdce3b33f5369eafd54bc7965`; equations U04–U13 and the final scope restrictions.
- `NATIVE_Q4_METRIC_ENERGY_ENVELOPE_V001.md`, SHA256 `920e113132ebeda44f500c73af105ecd1bbff267b894e02b09cac27845778009`; equations (1)–(10).

The complete active four-link star, with its scalar retained, is

\[
 H=-2hJ_x+UJ_z^2-BJ_z+C,\qquad
 B=\Delta+U(5-4d_*),\quad h>0,\ U\geq0.                 \tag{1}
\]

Here \(C=2\Delta+U(6-8d_*+5d_*^2)+C_{\rm spec}\); the spectator/reference scalar is not an owned absolute gravitational energy. Define \(Q=J_z^2\), \(q=\langle Q\rangle\). In a permutation-invariant state, the **conditionally adopted** q4 covariance recipe gives \(F=fI_3\), \(f=(4-q)/3\). This q is a spin second moment, not retained record occupation.

The source's actual blank-prewait state evolves unitarily. The following minimization is a different, explicitly conditional static state selection:

\[
 \mathcal E(q)=\min_{\rho:\langle Q\rangle=q}\operatorname{Tr}(\rho H),
 \quad H_\eta=H+\eta Q,\quad e_0(\eta)=\min\operatorname{spec}H_\eta.
                                                               \tag{2}
\]

No cooling or realization of this selection is inferred.

## 2. Exact regularity and curvature at every interior selection

For every finite real \(\eta\), the full sixteen-dimensional \(H_\eta\) has strictly negative single-bit-flip off-diagonals on a connected hypercube. Shifting its negative by a sufficiently large identity gives an irreducible nonnegative matrix. Perron–Frobenius therefore gives a unique, strictly positive ground vector. Permutation symmetry then places that vector in the spin-two sector; uniqueness was not assumed from a five-state truncation. In finite dimension its gap \(\delta_\eta=E_1-E_0\) is strictly positive.

Local analyticity follows directly: on a resolvent contour of radius \(\delta_{\eta_0}/2\) around the simple ground eigenvalue, the Neumann series in \((\eta-\eta_0)Q\) converges when \(4|\eta-\eta_0|<\delta_{\eta_0}/2\), since \(\|Q\|=4\). Thus the isolated projector, energy and q-response are real analytic near every finite \(\eta_0\). This is not a uniform gap or convergence-radius claim in a singular parameter or size limit.

Hellmann–Feynman and differentiation of the eigenvector give

\[
 q=e_0'(\eta),\qquad
 \chi_Q:=-\frac{dq}{d\eta}
 =2\sum_{r>0}\frac{|\langle r|Q|0\rangle|^2}{E_r-E_0}>0.       \tag{3}
\]

Strictness follows because the full-support ground vector cannot be an eigenvector of the nonconstant diagonal Q. With \(W_\eta=E_{\max}-E_0\),

\[
 0<\frac{2\operatorname{Var}_0 Q}{W_\eta}
 \leq\chi_Q\leq\frac{2\operatorname{Var}_0 Q}{\delta_\eta}
 \leq\frac8{\delta_\eta}<\infty.                              \tag{4}
\]

The endpoint limits are \(q(+\infty)=0\) and \(q(-\infty)=4\). Hence every \(0<q<4\) selects a unique finite \(\eta\), with locally analytic inverse. Its ground state saturates \(\mathcal E(q)=e_0(\eta)-\eta q\), so

\[
 \boxed{\mathcal E_q'=-\eta,\quad
 \mathcal E_{qq}''=\chi_Q^{-1}>0,\qquad
 \mathcal E_f'=3\eta,\quad
 \mathcal E_{ff}''=9\chi_Q^{-1}>0.}                          \tag{5}
\]

In particular, at an interior \(f_0\),

\[
 \mathcal E(f_0+u)=\mathcal E(f_0)+3\eta_0u
                   +\frac9{2\chi_{Q,0}}u^2+O(u^3).           \tag{6}
\]

Only the unbiased selection \(\eta_0=0\) has zero linear term. The susceptibility has inverse-energy units; \(\mathcal E_{ff}''\) has energy units, not automatically modulus or gravitational-coupling units.

Equation (5) is a genuine finite native constitutive *candidate*: it describes the response to a formal constraint bias. But \(\eta\) is not yet an environmental acceleration or physical deformation source; f is not a potential gradient. GL6U's double-commutator pair response is also not a normalized spatial Hessian. An owned work coupling, common physical probes, overlapping-cell dynamics and a spatial action would be needed to make those identifications. Equal f can already have different native energies away from the extra minimizing selection, as the envelope note proves.

## 3. Separate local-potential theorem: what asymptotic flat rotation needs

Adopt, **only for comparison**, ordinary test-body inertia, a physical three-dimensional space, a static potential \(\Phi\), acceleration \(-\nabla\Phi\), and a local isotropic first-gradient functional with constant coefficients:

\[
 \mathcal I[\Phi]=\int d^3x\left[
 \frac{W(\boldsymbol g)}{4\pi G_*}+\rho\Phi\right],\quad
 \boldsymbol g=\nabla\Phi,\quad g=|\boldsymbol g|,\quad
 W(\boldsymbol g)=w(g^2).                                    \tag{7}
\]

\(G_*>0\) is a declared comparison constant, not a derived UNT value. Variation of compact support gives

\[
 \nabla\cdot\boldsymbol D=4\pi G_*\rho,
 \qquad \boldsymbol D=\frac{\partial W}{\partial\boldsymbol g}
                    =2w'(g^2)\boldsymbol g.                  \tag{8}
\]

For an isolated spherical source of finite nonzero mass M, on the attractive radial branch with \(g\to0\), Gauss's law gives \(r^2D_r\to G_*M\). Suppose the leading nonconstant term is

\[
 W-W(0)\sim c_p(g^2)^p,\qquad c_p>0,\quad p>\tfrac12,
                                                               \tag{9}
\]

with the corresponding differentiated asymptotic \(D_r\sim2pc_p g^{2p-1}\). The latter follows automatically for a Taylor leading term; for a general nonanalytic asymptotic it is an explicit regularity requirement. Then

\[
 g\sim\left(\frac{G_*M}{2pc_p}\right)^{1/(2p-1)}
               r^{-2/(2p-1)},\qquad
 v_c^2=rg\ \propto\ r^{(2p-3)/(2p-1)}.                       \tag{10}
\]

Consequently a finite nonzero asymptotic flat speed requires \(p=3/2\). Real analyticity of w at zero instead makes its first nonzero power an integer \(p\geq1\). If every such coefficient vanishes, w is locally constant and cannot carry the nonzero exterior flux. Thus no theory satisfying all the premises of (7) with real-analytic w at zero has that exact flat asymptote. For example, \(p=1\) gives Keplerian falloff; \(p=2\) gives \(v_c^2\propto r^{1/3}\), not a constant.

The familiar AQUAL comparison is \(W\sim g^3/(3a_0)\): then \(D_r=g^2/a_0\) and \(v_\infty^4=G_*Ma_0\). This is an established example of the required nonanalyticity in \(s=g^2\), not a derivation or adoption of \(a_0\) or AQUAL by UNT. See Bekenstein and Milgrom's original action, field equation and spherical/far-field discussion, equations (2b)–(8), [Astrophysical Journal 286 (1984), 7–14](https://adsabs.harvard.edu/pdf/1984ApJ...286....7B), DOI [10.1086/162570](https://doi.org/10.1086/162570). No finite total field energy or \(\Phi\to0\) boundary condition is assumed; a flat-speed logarithmic potential would not satisfy the latter.

## 4. Scope and the smallest useful next discrimination

The native result does **not** by itself prove that a physical W is analytic: the source-to-field map does not yet exist. With an independently owned analytic coupling and regular analytic elimination of finitely many gapped variables, analyticity would persist locally. A derivation of the cubic term must then identify which premise ceases to hold, rather than calling the finite response gravitational stiffness.

- An analytic law can mimic the cubic law over a finite range bounded away from \(g=0\), or cross over later. The theorem does not rule out an observed finite-radius plateau or provide a galaxy fit.
- A closing gap, critical collective/infinite-size limit, endpoint selection, or \(h\to0\) singular limit can invalidate finite-branch analyticity; limits must be controlled rather than interchanged.
- Nonlocality, higher spatial gradients, extra fields with varying backgrounds, or nonisolated external fields invalidate the one-variable radial flux inference. An external-field background also changes the point about which a response is expanded.
- Nonanalytic microscopic coupling or a nonanalytic source-to-geometry map could supply the needed term, but would require independent ownership. Inserting it by hand is not its derivation from GL6U.

The next discriminating question is therefore concrete: **what same-parent physical source couples the finite response to a potential gradient, and does its derived long-distance flux satisfy \(D(g)\propto g^2\) over the intended low-acceleration regime?** Equation (5) gives a controlled regular baseline for that future comparison, not the missing force law. Neither galaxy gravity nor record-growth-driven cosmic acceleration is established by this static screen.
