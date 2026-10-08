# Controlled dressed-probe bridge in the native one-link hold model

2026-09-27. Analytical derivation/review only; no numerical execution or claim that the formed history prepares a ground branch. The one-link Hamiltonian and inherited coefficients are those of [the resident BS source](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_RECORD_TO_GEOMETRY_MINIMAL_JOIN_2026-09-27_V001/compute_join.py:36>), as reduced in `ENERGY_VOLUME_BRIDGE_AUDIT.md`. Distinguishable additional probes are an explicitly stated extension of that one-link model, not a completed multi-edge gravity construction.

## Exact branch map and spectral gap

Fix the conserved record occupation \(q\), take \(h>0\), and omit only a displayed sector-constant storage energy. The hold generator is

\[
H=-hX_a+\left(b-\sum_\alpha j_\alpha X_\alpha\right)n,
\qquad b=A-\lambda_Rq.
\]

The inherited one-probe values are \(h=1\), \(A=9/4\), \(\lambda_R=1/2\), hence \(b=9/4\) or \(7/4\). A multiple-probe extension must specify whether each new probe adds its own current-squared term: \(\lambda_JnJ_\alpha^2=\lambda_Jn\) adds link bias and must then be included in \(b\). Adding only a second hopping term while retaining the one-probe bias is a distinct, explicitly declared extension. Probe \(X_\alpha\) operators commute because the probes are distinguishable subsystems. In their joint eigenbranch \(s\), put \(x_s=b-\sum_\alpha j_\alpha s_\alpha\). The link energies are

\[
f(x)=\frac{x-d(x)}2<0,\quad g(x)=\frac{x+d(x)}2>0,
\qquad d(x)=\sqrt{x^2+4h^2}.
\]

If |g(x)⟩ denotes the normalized lower-link eigenstate, the map

\[
W|s\rangle=|g(x_s)\rangle\otimes|s\rangle,
\qquad W^\dagger W=I,
\qquad HW=WH_{\rm eff},
\]

\[
\boxed{H_{\rm eff}=f\left(b-\sum_\alpha j_\alpha X_\alpha\right)}
\]

is exact. Orthogonality of the probe labels makes \(W\) an isometry although the link states overlap. This is an invariant dressed subspace, not an approximation obtained by tracing out the link.

For \(J=\sum_\alpha|j_\alpha|\), the separation between the union of lower branches and the union of upper branches, at fixed \(q\), is exactly

\[
\Gamma=g(b-J)-f(b+J)
=\frac{d(b-J)+d(b+J)}2-J>0.
\]

The strict inequality holds for every finite \(J\) with \(h>0\), though it need not stay uniformly large when \(J\) increases. Each individual branch gap is at least \(2h\). Different record sectors have different storage offsets: their direct sum remains invariant, but it must not be called the globally lowest isolated spectral band without checking ordering across those offsets.

## One probe: common leading response with a controlled error

For one probe,

\[
H_{\rm eff}=E_0I-t_{\rm eff}X,
\quad t_{\rm eff}=\frac{f(b+j)-f(b-j)}2,
\quad p(b)=f'(b)=\frac{1-b/d(b)}2.
\]

For nonzero \(j\), \(t_{\rm eff}/j\) is the symmetric interval average of \(p\). Therefore

\[
p(b+|j|)\le\frac{t_{\rm eff}}j\le p(b-|j|).
\]

The derivatives needed for explicit bounds are

\[
f''(x)=-\frac{2h^2}{d(x)^3},\qquad
f'''(x)=\frac{6h^2x}{d(x)^5},\qquad
f''''(x)=\frac{24h^2(h^2-x^2)}{d(x)^7}.
\]

With \(M_3=\sup_{x\in[b-|j|,b+|j|]}|f'''(x)|\), symmetry cancels the linear Taylor term and gives the rigorous interval bound

\[
\left|\frac{t_{\rm eff}}j-p(b)\right|\le\frac{j^2M_3}{6}
\le\boxed{\frac{j^2}{25\sqrt5\,h^2}}.
\]

The last inequality uses the exact global maximum \(\sup|f'''|=6/(25\sqrt5h^2)\). Thus separately tested probes with different weak couplings share the leading ratio \(t_{\rm eff}/j\to p(b)\), with a specified finite-coupling correction. For \(b>|j|>0\), the correction is positive because \(p\) is strictly convex on that interval. This supplies a testable common leading hopping factor, not yet a physical metric, volume, or equivalence-principle result.

For the inherited \(j=1/2\), useful exact reference expressions are

\[
t_{\rm eff}(q=0)=\frac{4+\sqrt{113}-\sqrt{185}}{16},
\qquad
t_{\rm eff}(q=1)=\frac{4+\sqrt{89}-\sqrt{145}}{16}.
\]

## Two probes: exact induced coupling and fourth-order remainder

The coefficient of \(X_1X_2\) is the exact Walsh coefficient

\[
K_{12}=\frac14\left[f(b-j_1-j_2)-f(b-j_1+j_2)
-f(b+j_1-j_2)+f(b+j_1+j_2)\right].
\]

For nonzero couplings, \(K_{12}/(j_1j_2)\) is the average of \(f''(b+u+v)\) over \(u\in[-|j_1|,|j_1|]\), \(v\in[-|j_2|,|j_2|]\). It is strictly negative, including beyond perturbation theory. Let \(M_4=\sup_{x\in[b-J,b+J]}|f''''(x)|\). Then

\[
\left|K_{12}-j_1j_2f''(b)\right|
\le\frac{|j_1j_2|(j_1^2+j_2^2)M_4}{6}
\le\boxed{\frac{|j_1j_2|(j_1^2+j_2^2)}{32h^3}}.
\]

Here \(\sup|f''''|=3/(16h^3)\). The remainder is fourth total order in the couplings when they scale to zero together. The negative coefficient favors certain probe-\(X\) correlations; it is not spatial attraction. Simultaneous probes also shift each other's individual hopping at third total order, so the common factor \(p(b)\) is a leading weak-coupling statement, not an exact independent-probe law.

## Preparation and bare-observable limitations

The real positive ground-state convention gives the exact overlap

\[
|\langle g(x)|g(y)\rangle|^2
=\frac12\left[1+\frac{xy+4h^2}{d(x)d(y)}\right].
\]

For \(x,y\) in an interval whose minimum gap is \(d_*\),

\[
1-|\langle g(x)|g(y)\rangle|^2
\le\frac{h^2(x-y)^2}{d_*^4}.
\]

Consequently, starting with a genuinely prepared |g(b)⟩ and arbitrary independent probes, a sudden switch to the desired couplings leaves at most \(h^2J^2/d_*^4\) weight outside the dressed lower-link subspace, with \(d_*\) minimized over \([b-J,b+J]\). This is a preparation bound for that stated initial state, not for the existing formed state. Switching work must remain in the energy ledger.

Slow switching is another conditional preparation mechanism. A branch has

\[
|\langle e(x_s)|\dot g(x_s)\rangle|
=\frac{h|\dot x_s|}{d(x_s)^2},
\qquad
\frac{h|\dot x_s|}{d(x_s)^3}
\]

as its derivative coupling and dimensionless local adiabatic diagnostic. Smallness of that diagnostic alone is not a rigorous finite-time leakage guarantee; a specified smooth schedule and its endpoint/derivative bounds are still required. Adiabatic evolution also does not cool an initially populated upper branch into the lower one.

For a measured initial state \(\rho\), the more direct test is its actual lower-link weight: \(\eta=1-\operatorname{Tr}(P\rho)\), \(P=WW^\dagger\). Since \([P,H]=0\), that leakage weight is constant during hold. For \(\eta<1\), use the normalized projected logical state \(\rho_{\rm eff}=W^\dagger\rho W/(1-\eta)\) and the correctly dressed observable \(O_{\rm eff}=W^\dagger OW\). Their exact dressed evolution approximates the full expectation uniformly in hold time with

\[
\boxed{|\langle O\rangle_{\rm full}(t)-\langle O_{\rm eff}\rangle_{\rm eff}(t)|
\le2\|O\|\sqrt\eta.}
\]

This follows from the trace-distance bound for normalized projection and unitary invariance; it applies to mixed initial states as well. A large measured \(\eta\) removes the proposed controlled description of that history, even though the exact invariant subspace exists.

Tracing the link from a dressed state multiplies each logical coherence \(\rho_{ss'}\) by \(\langle g(x_{s'})|g(x_s)\rangle\). Thus a coherent dressed evolution can have a mixed bare carrier. Carrier position readouts require this overlap factor or an actual decoding operation. This explains why the construction does not contradict the earlier fresh-bare-probe decoherence test: it changes the encoded degrees of freedom and the initial-state premise openly.

## Multi-edge caution and concrete disposition

For the root's proposed many-edge single-particle extension, \(J_e^2=N_u+N_v\) gives the first-order mean Hamiltonian

\[
H_{\rm mean}=\sum_e p_e[-tT_e+\lambda_J(N_u+N_v)]
=tL_p+(\lambda_J-t)D_p.
\]

This algebra is correct when \(L_p=D_p-A_p\) and the indicated edge/current operators are the parent operators. The inherited \(\lambda_J=1/4\), \(t=1/2\) retain the site potential \(-D_p/4\). It becomes a carrier-state-independent shift only at uniform weighted degree; even then it remains in a complete work ledger. Removing it, imposing \(\lambda_J=t\), or interpreting it as a lapse/potential needs separate physical justification. The exact commuting-probe diagonalization above also does not automatically extend to overlapping graph-edge hopping operators, which need not commute.

This is a concrete controlled effective-propagation route beyond a failed bare mean-link replacement: it provides an exact encoded generator, a physical leakage check, common leading probe response, and bounded nonlinear corrections. The route is not yet an energy–volume or gravitational derivation.

**Two implementable tests:** (1) check the exact one-probe hopping and two-probe coupling against the displayed interval/global bounds, including the exact radicals at the inherited parameters; (2) measure the existing formed state's actual lower-link dressed-subspace weight and compare dressed predictions using \(W^\dagger OW\), with the \(2\|O\|\sqrt\eta\) ceiling. The second test decides whether this controlled construction describes the already produced history or requires a separately costed preparation.
