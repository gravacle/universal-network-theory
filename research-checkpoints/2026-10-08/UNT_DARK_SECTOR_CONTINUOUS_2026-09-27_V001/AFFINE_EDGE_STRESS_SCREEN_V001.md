# Conditional affine-edge stress and a finite accelerating-window test

2026-09-27. Analytical mechanism screen only; no numerical run, fitted density, new adopted interaction or replacement of the primary active/maintenance hypothesis.

Exploratory comparison construct ID: `UNT_ELASTIC_COMPARISON_CENTRAL_EDGE_V001`.

## 1. Explicit added interface and source scope

Assume a fixed-topology graph has an independently declared three-dimensional physical embedding. Under uniform dilation, \(x_v=aX_v\), every edge has \(\ell_e=a\ell_{e0}\), and an independently calibrated material volume satisfies \(V=V_0a^3\). These are additional physical premises, not consequences of BS layers or incidence.

Assume differentiable central edge energies \(E_e(\ell_e)\), a complete geometry-independent energy \(M\) containing the assigned rest/storage/reference constants once, and all remaining energy \(E_{\rm other}(a)\). The derivative below holds the declared state/material variables fixed:
\[
E_{\rm tot}=M+\sum_e E_e(\ell_e)+E_{\rm other}(a).
\]
The physical Hamiltonian must own this deformation dependence. A total derivative along an arbitrarily changing state is not the work-pressure derivative.

The resident [recovered-parent screen](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/RECOVERED_PARENT_PHYSICAL_SCREEN_V001.md:79>) establishes the conditional FU mutual Coulomb scaling, not a complete BS mechanical energy law. The current [absolute-stress analysis](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/VACUUM_STRESS_IDENTIFIABILITY_V001.md>) explains why identity/reference terms cannot be discarded. FU's detailed contact note became dataless: a mistakenly queued read was stopped without receiving bytes; this derivation uses its previously inspected content and the resident recovered-parent summary.

## 2. Complete dilation identity

Put
\[
D_E=\sum_e\ell_e E'_e(\ell_e),\qquad
D_{\rm other}=a\,\partial_aE_{\rm other}.
\]
The exact mean work pressure and energy density are
\[
\boxed{p=-\frac{D_E+D_{\rm other}}{3V}},\qquad
\rho=\frac{E_{\rm tot}}V,
\]
\[
\boxed{V(\rho+3p)=E_{\rm tot}-D_E-D_{\rm other}.}
\]
For central edges, the instantaneous stress contribution is
\[
\Pi_{ij}^{\rm edge}
=-\frac1V\sum_e\ell_e E'_e\,n_{e,i}n_{e,j},
\qquad n_e=(x_v-x_u)/\ell_e.
\]
Uniform dilation fixes its trace, not the absence of shear. Interpreting \(\rho+3p<0\) as homogeneous acceleration additionally requires an isotropic coarse-grained state and the adopted Einstein/cosmological interface with controlled corrections. It does not itself show that the network expands.

Only when all non-edge terms are geometry-independent does the numerator reduce to \(E_{\rm tot}-D_E\). A genuine constant density contribution \(\rho_bV\) instead has \(D_{\rm other}=3\rho_bV\), pressure \(-\rho_b\) and numerator \(-2\rho_bV\). Inserting such a term would already supply a vacuum law; it is not derived by renaming stored energy.

## 3. Exact component screens

For one component, define \(\mathcal A=E-\ell E'\); divide the pressure column by the full cell volume. Constants belong once in the stated energy, not both here and in \(M\).

| Assigned component energy | Pressure contribution | \(\mathcal A\) |
|---|---|---|
| Coulomb \(E=C/\ell\), signed \(C\) | \(E/(3V)\) | \(2E\) |
| Positive linear tension \(E=T\ell\) | \(-E/(3V)\) | \(0\) |
| Quadratic stretch \(E=k\ell^2/2,\ k>0\) | \(-2E/(3V)\) | \(-E\) |
| Rest/reference energy \(E=M\), independent of geometry | \(0\) | \(M\) |
| Hooke bond \(E=C+k(\ell-\ell_*)^2/2\) | \(-k\ell(\ell-\ell_*)/(3V)\) | \(C+k(\ell_*^2-\ell^2)/2\) |

Consequences for the stated components:

- Coulomb alone has \(p=\rho/3\), even if its pair energy is negative. Negative binding can contribute an accelerating-sign term, but omitting the rest, kinetic, self/reference or supporting contributions cannot establish the complete sign.
- Positive linear tension with \(M\geq0\) is at most the \(\rho+3p=0\) boundary; it does not provide the negative total numerator.
- Positive quadratic bonds give a negative numerator, but with complete constant energy \(M\geq0\) acceleration requires \(E_b>M\), where \(E_b=\sum k_e\ell_e^2/2\).
- A Hooke bond is unstressed at \(\ell=\ell_*\). It is not the same law as a pure quadratic bond. The complete accelerating-sign condition is
  \[
  \sum_e k_e\ell_e^2>
  2M+2\sum_e C_e+\sum_e k_e\ell_{*,e}^2
  \]
  when no other volume-dependent terms are present.

For a pure positive power \(E_e\propto\ell^r\), the edge-only scaling gives \(w=-r/3\) and \(\mathcal A=(1-r)E\). This is a conditional constitutive consequence, not a derivation of any exponent. Vacuum-form stress requires the stronger full identity \(D_E+D_{\rm other}=3E_{\rm tot}\).

## 4. Relaxation and the missing support must be tested

For a finite free classical network with only central potentials, let every vertex coordinate be free and suppose the configuration is stationary with no external forces. Euler's dilation identity gives
\[
\sum_v x_v\cdot\nabla_vE_{\rm edge}
=\sum_e\ell_eE'_e=0.
\]
Therefore its configurational mean pressure is zero. A finite freely relaxed configuration cannot be assumed to retain a nonzero dilation tension just because an imposed affine configuration had it.

If ordinary Newtonian node kinetics is additionally specified, the exact virial identity is
\[
\frac12\ddot I=2T-D_E,\qquad I=\sum_vm_v|x_v|^2.
\]
For a bounded stationary/time-averaged isolated state with the required boundary limits, \(2\langle T\rangle=\langle D_E\rangle\). At a fixed averaging volume, the complete kinetic-plus-central mean pressure is therefore zero. If the assigned volume itself varies during averaging, this identity fixes \(\langle Vp\rangle=0\), not necessarily \(\langle p\rangle=0\).

These are cheap finite-free prototype checks, not conditions imposed on cosmological expansion and not cosmological no-go results. Fixed-volume boundaries, periodic winding/topology, constrained internal coordinates, ongoing expansion or unrelaxed dynamics change the hypotheses. They require an owned support/topology/history and work ledger. For relaxation only over internal coordinates at a prescribed volume, the envelope theorem preserves the partial volume derivative on a smooth stationary branch; it does not force that pressure to zero. The pressure of the constraining system must not be silently omitted when that system is part of the claimed source.

An additive bond reference \(C_e\) changes energy and the gravitational numerator without changing bond forces. It cannot be chosen freely after a desired acceleration result is known. Kinetic/thermal energy and its strain dependence likewise cannot be dropped merely because the potential-energy screen passes.

## 5. How long can the quadratic candidate remain in the screened window?

The separate [central-edge elasticity derivation](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/CENTRAL_EDGE_ELASTICITY_COMPARISON_V001.md>) introduces further isotropic, nondispersive relativistic-material and prestress-response assumptions, with a common physical cone whose speed is one. Under that conditional closure, a pure quadratic bond medium has acausal squared characteristic speeds 2. It is not made viable by its negative pressure.

With a positive **dynamically tied** co-moving rest energy \(M\), define
\[
f=\frac{E_b}{M+E_b}.
\]
That same material closure gives
\[
w=-\frac{2f}{3},\qquad
c_T^2=c_L^2=\frac{2f}{3-2f}.
\]
Acceleration and subluminal characteristics together require
\[
\boxed{\tfrac12<f\leq\tfrac34}
\quad\Longleftrightarrow\quad
\boxed{M<E_b\leq3M}.
\]
This is not established for an unrelated dust component merely added to the energy ledger; its inertia must participate in the same material displacement dynamics.

For the fixed topology and fixed quadratic couplings assumed here,
\[
E_b(a)=E_{b0}a^2,\qquad M=\mathrm{constant}.
\]
The entire available accelerating-and-causal interval therefore spans at most
\[
\boxed{\frac{a_{\max}}{a_{\min}}\leq\sqrt3,\qquad
\Delta\ln a\leq\tfrac12\ln3,}
\]
with the acceleration onset itself excluded by its strict inequality. Starting inside the interval shortens the remaining span. This is an exact internal history screen, independent of any observed density target or choice of \(E_{b0}/M\). It does not establish viable perturbations, nonlinear stability, preparation or persistence.

## Next scientific decision

For a proposed affine-edge completion, first provide its actual physical length law and absolute energy normalization, then identify what prevents the tension from relaxing and what inertia carries its perturbations. For the quadratic-plus-tied-rest candidate, derive whether that same rule can sustain the finite interval above. Extending it by changing topology, couplings, rest mass or constitutive law is new dynamical content requiring its own derivation—not a silent adjustment of the scaling ansatz.

The native FU Coulomb subterm supplies neither this quadratic law nor its stress-support mechanism; BS supplies no physical embedding by itself. The result is a discriminating conditional mechanism test, not an adopted UNT dark-sector explanation.
