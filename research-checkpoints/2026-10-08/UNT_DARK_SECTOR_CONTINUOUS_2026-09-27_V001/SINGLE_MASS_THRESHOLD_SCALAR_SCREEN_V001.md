# Fixed-mass threshold: conditional retained-scalar screen

2026-09-27. Exact analytic result; no numerical execution, adopted spectrum, new native field, or change to historical sources.

## 1. Scope and read evidence

Both resident files were read completely after flag checks:

- `SCALE_ONLY_RETAINED_SCALAR_DARK_SCREEN_V001.md`, SHA256 `aa4e6442825cb43c5d429ab676ca40a2cdc569e718f6027d3074f4bbb1511005`.
- `program-worktree/LANE_CROSS_RFT_MGFT_INDUCED_EH_BACKREACTION_V001/THEOREM.md`, SHA256 `e73c077d1402ebab9a6061b060b9b24e9ac323b25809cccc706f4365da7a5e2f`.

RIEHB IB02/IB09 supplies the proper-time mass factor, including the exact constant-mass integral rather than only its light-mass expansion. Continue the **conditional** metric scalar interface of the first note: an independently retained physical scalar controls a crossover κ, fixed x = μ/κ lies in (0,1), no pre/matching contributions or extra retained potential, and zero Jordan kinetic coefficient. A common nonnegative mass m is physically fixed, not proportional to κ. Its mass endomorphism is constant and factors as exp(−m²s) at the two displayed heat-kernel orders.

The convention-matched constants obey A₀ > 0 and A₁ < 0, giving positive vacuum coefficient V and positive stiffness F. This assumes the same mass threshold multiplies both complete coefficient sums; it does not assert that UNT supplies this spectrum, that raw signed species ranks have these signs, or that different masses/nonminimal couplings share the required relative weighting. All RIEHB geometry, derivative-expansion, matching and complete-variation premises remain unearned where previously unearned. Exact treatment of a constant mass factor does not control omitted curvature/gradient operators.

## 2. Positive single-mass coefficients and strict monotonicity

Let L = (4π)², b = x⁻² > 1, z = m²/κ², and

\[
 J_0(z)=\int_1^b u^{-3}e^{-zu}\,du,\qquad
 J_1(z)=\int_1^b u^{-2}e^{-zu}\,du,\qquad
 J_2(z)=\int_1^b u^{-1}e^{-zu}\,du.
\]

With positive constants f = −ħA₁/L and v = ħA₀/(2L), the shell gives

\[
 F=f\kappa^2J_1(z)>0,\qquad
 V=v\kappa^4J_0(z)>0,\qquad
 B:=\frac{V}{F^2}=\frac{v}{f^2}\frac{J_0(z)}{J_1(z)^2}. \tag{1}
\]

Normalize the positive measures proportional to u⁻³e⁻ᶻᵘ and u⁻²e⁻ᶻᵘ on [1,b], and write their means as

\[
 a_0=\langle u\rangle_0=J_1/J_0,\qquad
 a_1=\langle u\rangle_1=J_2/J_1.
\]

The second measure is the u-tilt of the first. Consequently

\[
 a_1-a_0=\frac{\operatorname{Var}_0(u)}{a_0}>0,
 \qquad
 \boxed{\frac{d\ln B}{dz}=2a_1-a_0
       =a_0+\frac{2\operatorname{Var}_0(u)}{a_0}>0.} \tag{2}
\]

The strict variance holds for this nonzero-width continuous shell; positivity of the last expression does not require strict variance. There is no cancellation or fitted numerical threshold in (2).

At fixed physical m, dz/dlnκ = −2z, and

\[
 \frac{d\ln F}{d\ln\kappa}=2(1+za_1)>0,
 \qquad
 F_\chi=\frac{2F}{\kappa}(1+za_1)\kappa_\chi. \tag{3}
\]

Thus F is strictly increasing with κ, and any regular monotone κ(χ) patch remains a regular monotone F(χ) patch. Set y = ln(F/M²). For m > 0 and any finite κ > 0,

\[
 \boxed{\frac{B_y}{B}
 =-\frac{z(2a_1-a_0)}{1+za_1}<0.} \tag{4}
\]

In the stated zero-Jordan-kinetic metric interface, φ = √(3/2) M y and U = M⁴B in ħ = c = 1 units. Equation (4) rules out every finite regular stationary vacuum B_y = 0 in this single-common-mass branch. A fixed mass makes the ratio nonconstant but does **not** supply the positive nondegenerate minimum required by the preceding scalar screen. It does not rule out rolling solutions, matter-induced effective extrema, another retained field, or another complete spectrum.

An imposed κχ = 0 is not a minimum of B(F): it makes this scalar field redefinition/kinetic interface degenerate. Such a distinct completion must be analyzed with its actual independent variables and gradient action; it is not covered by (4).

## 3. Exact massless case and boundary limits

For m = 0, z remains exactly zero as κ changes. Although the derivative with respect to a hypothetical z in (2) is positive at zero, the physical κ derivative is zero:

\[
 J_0(0)=\frac{1-x^4}{2},\quad J_1(0)=1-x^2,\quad
 B=\frac{L A_0}{4\hbar A_1^2}\frac{1+x^2}{1-x^2}.
\]

This is precisely the flat-potential, zero vacuum-mass result, not an isolated minimum.

For fixed m > 0, κ → ∞ gives z → 0 and B approaches this same positive constant **from above**, while F grows without bound. It is an asymptotic plateau, not a stationary point at finite F. At κ → 0, z → ∞, fixed b > 1 gives

\[
 J_0\sim J_1\sim e^{-z}/z,\quad
 F\sim f m^2e^{-z}/z^2\to0,\quad
 V\sim v m^4e^{-z}/z^3\to0,\quad
 B\sim(v/f^2)ze^z\to\infty.
\]

The F = 0 boundary is not a healthy finite-stiffness Einstein-frame vacuum. These are limits of the defined integrals, not a claim that the emergent metric parent or derivative expansion remains valid at either endpoint.

## 4. Restricted extension: aligned positive fixed masses

The no-stationary conclusion also holds for a finite set of fixed masses mᵢ ≥ 0 **only under the additional exact alignment** that the same weights wᵢ ≥ 0, not all zero, enter V and F up to fixed positive overall constants. Define

\[
 K(u)=\sum_i w_i e^{-m_i^2u/\kappa^2},\quad
 J_j=\int_1^b u^{j-3}K(u)\,du\ (j=0,1),\quad
 T_j=\frac{\int_1^b u^{j-3}[-uK'(u)]\,du}{J_j}\ge0.
\]

Here the prime is the u derivative. With F = fκ²J₁ and V = vκ⁴J₀,

\[
 \frac{d\ln B}{d\ln\kappa}=2T_0-4T_1,
 \qquad \frac{d\ln F}{d\ln\kappa}=2(1+T_1)>0. \tag{5}
\]

Let k₋ = K(1), k₊ = K(b), so k₋ ≥ k₊ > 0. Integration by parts yields

\[
 2T_1-T_0=
 \frac{2(k_- -k_+/b)}{J_1}
 -\frac{k_- -k_+/b^2}{J_0}. \tag{6}
\]

Since K is nonincreasing, weighting the u⁻³ measure by K cannot increase its mean u. Hence

\[
 \frac{J_1}{J_0}\le\frac{2b}{b+1}
 \le\frac{2(k_- -k_+/b)}{k_- -k_+/b^2}. \tag{7}
\]

The second inequality is strict whenever some positively weighted mass is nonzero, since then k₋ > k₊. Equations (6)–(7) give 2T₁−T₀ > 0, so B_y < 0. If all positively weighted masses vanish, both inequalities are equalities and B is constant. This proof does not assume a sign for the correlation between u and the species mass.

Alignment is substantially stronger than separately positive total F and V, or separately positive but unequal species weights in those coefficients. A signed spectrum, differing volume/curvature weights (including species-dependent nonminimal curvature couplings), changing masses/couplings or shell ratio, and extra physical matching terms are outside this extension. No conclusion about all spectra is justified.

## 5. What this rules out and the next owned datum

The result closes one minimal candidate: merely giving the otherwise scale-only, positive aligned shell a physically fixed mass or aligned positive mass distribution does not create a finite retained-scalar vacuum minimum. It supplies a specific mathematical rejection criterion, not a general dark-sector or UNT no-go.

For a single common mass, the mean/tilt proof (2) also survives multiplication of both integrands by the same fixed nonnegative profile in u, when the integrals and first moments exist. It does not cover a κ-dependent profile, different profiles at the two orders, or the multispecies extension for an arbitrary profile: (6)–(7) used the sharp shell explicitly.

A constructive next datum must therefore be an **owned** departure not erased by this theorem—for example unequal signed spectral threshold content in the two coefficients, a physical crossover-ratio response, or independently fixed matching contributions—together with its scalar variation and kinetic/derivative-expansion checks. Whether any such same-parent datum actually exists and yields B > 0, B_y = 0, B_yy > 0 remains a calculation, not permission to choose a desired potential. Nothing here identifies κ with record density, a clock, physical volume, or a native microscopic UNT observable.
