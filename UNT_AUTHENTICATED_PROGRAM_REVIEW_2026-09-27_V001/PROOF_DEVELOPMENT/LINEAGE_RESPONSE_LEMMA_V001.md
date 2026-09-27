# Operational sufficiency of sector marginals under a common continuation

Date: 2026-09-27. New analytic development, version V001.

Status: **SELF_CONTAINED_FINITE_DIMENSIONAL_LEMMA__PROJECT_INTERNAL_ANALYTIC_REVIEW_ACCEPTED_WITH_STATED_SCOPE**.

This note proves a linear-algebra criterion that organizes the already recognized L4 result and specifies what a further size-persistence proof would need. The lemma is new documentation of an elementary finite-dimensional channel argument; it is not a new numerical calculation, an originality claim for quantum information theory, or an empirical result. No historical protocol or result is changed. The proposed B3 test below is a candidate for a separate prospective freeze, not a production authorization.

## 1. Match to the frozen L4 construction

The [frozen L4 protocol](../../DEVELOPMENT_R_OWNER_ONCE_L4_AUTONOMOUS_LINEAGE_SENSITIVE_CONTINUATION_V001/PROTOCOL.md), sections 3–5, uses a lineage factor S and carrier factor C with matching sharp-q sectors. At its fixed checkpoint,

\[
|\Psi\rangle=\sum_q|\psi_q\rangle,\qquad
|\psi_q\rangle\in\mathcal H_{S,q}\otimes\mathcal H_{C,q},\qquad
p_q=\langle\psi_q|\psi_q\rangle.
\]

The actual and product-comparator inputs are

\[
\rho_A=\bigoplus_q|\psi_q\rangle\langle\psi_q|,
\quad
s_q=\operatorname{Tr}_C|\psi_q\rangle\langle\psi_q|,
\quad c_q=\operatorname{Tr}_S|\psi_q\rangle\langle\psi_q|,
\quad
\rho_P=\bigoplus_{q:p_q>0}\frac{s_q\otimes c_q}{p_q}.
\tag{1}
\]

Thus `Tr(s_q)=Tr(c_q)=p_q`; each comparator block has trace `p_q`, not `p_q^2`. Both arms remove coherence between different q sectors and retain complete within-q quantum marginals. This is not a product of the unconditional marginals, a diagonal-only product, or an intervention on just one arm's sector coherence.

Both inputs undergo the same fixed joint admission and then carrier transport,

\[
U=U_TU_A(0),\qquad
\Phi(X)=\operatorname{Tr}_{S'}(UXU^\dagger),\qquad
\Delta_C=\tfrac12\|\Phi(\rho_A-\rho_P)\|_1.
\tag{2}
\]

Here U acts on the physical full input/output space; its action can mix q. The theorem does not assume q is conserved during continuation. Every output is compared in one fixed carrier Hilbert space, not by identifying density matrices of different dimensions. For different L, each size has its own input/output spaces and channel.

## 2. General finite-dimensional setup

Let

\[
\mathcal V=\bigoplus_{q\in Q}
\operatorname{Herm}(\mathcal H_{S,q}\otimes\mathcal H_{C,q})
\]

be a real vector space. Its allowed full-domain states are every positive block-diagonal `rho` in this space with total trace one. Sector dimensions are finite and nonzero; Q is finite. Let `Phi: V -> Herm(H_C,out)` be the restriction of a fixed completely positive trace-preserving continuation/readout map. Explicit block inclusions into a larger physical input space are understood and held fixed. Linearity alone suffices for the main equivalence; CPTP is needed for the operational interpretation and contraction bound.

Define the linear retained-information map

\[
\mathcal R(X)=\big((\operatorname{Tr}_C X_q,
\operatorname{Tr}_S X_q)\big)_{q\in Q},
\]

and its correlation subspace

\[
\mathcal K=\ker\mathcal R
=\bigoplus_q\{X_q=X_q^\dagger:
\operatorname{Tr}_C X_q=0,\ \operatorname{Tr}_S X_q=0\}.
\tag{3}
\]

The sector weights are already included in R through the traces of its marginals. Both partial traces in (3) must vanish; zero total trace alone is insufficient.

For a state rho with marginals `s_q,c_q` and weights `p_q`, define P(rho) by the second expression in (1), taking a zero block when `p_q=0`. Positivity makes that zero-weight convention unambiguous. Then

\[
\mathcal R(P(\rho))=\mathcal R(\rho),\qquad
\Gamma(\rho):=\rho-P(\rho)\in\mathcal K.
\tag{4}
\]

P is generally **nonlinear**. No assertion below treats decorrelation as a single linear CPTP channel or assumes it can be physically applied to an unknown state from one copy.

## 3. The operational sufficiency theorem

The following four statements are equivalent on the full-domain state set above.

1. **Marginal sufficiency:** whenever two states have equal R, they have equal reduced outputs under Phi.
2. **Correlation annihilation:** `Phi(X)=0` for every `X in K`.
3. **Linear factorization:** there is a well-defined linear map `F` on the vector space `im R` such that `Phi=F R`.
4. **Product-comparator invariance:** `Phi(rho)=Phi(P(rho))` for every allowed state rho.

The factorization is an informational statement. It does not assert that F is a physically implementable CPTP operation that combines two separately supplied unknown marginals; `im R` is a space of compatible marginal tuples, not a canonically chosen quantum register.

### Proof

**2 implies 1.** Equal marginals imply `rho-rho' in K`; linearity gives `Phi(rho)-Phi(rho')=0`.

**1 implies 2.** Choose a full-rank, trace-one state omega on the total direct-sum space, with positive weight in every sector. For any nonzero Hermitian `X in K`, `Tr X=0`. For sufficiently small positive epsilon, both `omega+epsilon X` and `omega-epsilon X` are positive, trace-one allowed states. Their R values agree. Statement 1 therefore gives `2 epsilon Phi(X)=0`. The zero direction is immediate. Positivity is essential to this argument; it is why the full allowed state set or an equivalent spanning condition must be specified.

**2 implies 3.** Define `F(R(X))=Phi(X)`. If `R(X)=R(Y)`, then `X-Y in K`, so this definition is independent of the representative. It is linear on `im R`.

**3 implies 2.** If `R(X)=0`, then `Phi(X)=F(0)=0`.

**1 implies 4.** Equation (4) gives equal R for rho and its valid product comparator.

**4 implies 1.** If `R(rho)=R(rho')`, their product comparators are identical, since P depends only on the sector marginals and weights. Statement 4 then gives `Phi(rho)=Phi(P(rho))=Phi(P(rho'))=Phi(rho')`. QED.

Consequently, the phrase “separate marginals determine the future carrier state” has an exact test: the common continuation must annihilate the entire correlation subspace relevant to the declared state domain. An interacting continuation need not pass that test, but interaction by itself is not a proof of failure.

## 4. Dual criterion and an exact finite certificate

Use the real Hilbert–Schmidt pairing `Tr(XY)` on Hermitian matrices. Let `Phi*` denote its adjoint, including compression back onto the input block-diagonal algebra. Correlation annihilation is equivalent to

\[
\forall O=O^\dagger\text{ on }\mathcal H_{C,\mathrm{out}},
\quad
\Phi^*(O)\in\mathcal K^\perp.
\tag{5}
\]

For each q,

\[
\mathcal K_q^\perp
=\{A_q\otimes I_{C,q}+I_{S,q}\otimes B_q:
A_q=A_q^\dagger,\ B_q=B_q^\dagger\}.
\tag{6}
\]

**Proof of (5).** `Tr[O Phi(X)]=Tr[Phi*(O)X]`; a Hermitian output is zero exactly when its pairing with every Hermitian O is zero.

**Proof of (6).** Choose identity plus traceless Hermitian bases in each factor. Their tensor products decompose the joint Hermitian space orthogonally into identity/identity, lineage-traceless/identity, identity/carrier-traceless, and traceless/traceless pieces. Both partial traces vanish precisely on the last piece. Its orthogonal complement is the local-sum space (6). The A/B representation has the harmless gauge `A -> A+aI`, `B -> B-aI`. In dimensions dS,dC, the correlation subspace has dimension `(dS^2-1)(dC^2-1)`. QED.

This gives a constructive finite proof procedure. For every q choose traceless Hermitian bases `{S_q,i}` and `{C_q,j}`. Prove or calculate

\[
\Phi(S_{q,i}\otimes C_{q,j})=0
\quad\text{for all }q,i,j.
\tag{7}
\]

Exact zero for the complete basis certifies sufficiency. One nonzero image disproves full-domain sufficiency; the positivity construction in section 3 produces a valid pair of indistinguishable-marginal inputs. Equivalently, find one output observable whose pulled-back block contains a nonzero traceless/traceless component. A floating-point near-zero is not an exact annihilation proof unless a separate exact reduction or rigorous error bound justifies that conclusion.

For a particular physical checkpoint the stronger operational question is whether its actual `Gamma(rho)` is detected, not merely whether some direction in K is detectable. A channel can fail the universal test while annihilating that particular Gamma.

## 5. Restricted reachable states: the necessary qualification

The frozen owner-once protocol provides a specific state and comparator, not every density matrix in the full direct-sum algebra. Let A be any separately specified admissible family of states and define

\[
\mathcal K_A=\operatorname{span}_{\mathbb R}
\{\rho-\rho':\rho,\rho'\in A,
\ \mathcal R(\rho)=\mathcal R(\rho')\}.
\tag{8}
\]

For this family, marginal sufficiency is **exactly** equivalent to `Phi(K_A)=0`. The proof follows directly from linearity and the definition of the span. Since `K_A subset K`, global annihilation of K is sufficient for A, but it is not necessary unless `K_A=K`. The positive-interior argument cannot be imported into a family that does not contain the required perturbations.

If A is not closed under P, comparator invariance is a statement on the explicitly enlarged experimental comparison family, not automatically on A alone. In the L4 test the actual and product inputs are both deliberately included as mathematical experiment arms. The comparator need not have arisen under the same unmodified first-pass history; its purpose is to hold the marginal information fixed while testing the role of the joint state under a common continuation. This remains a controlled finite model intervention, not a claim of laboratory preparability.

## 6. Operational bounds and transport

For any actual/product pair, equations (2) and (4) give

\[
0\le\Delta_C
=\tfrac12\|\Phi(\Gamma)\|_1
\le\tfrac12\|\Gamma\|_1\le1.
\tag{9}
\]

The first upper bound is trace-distance contraction under the common CPTP channel. It says joint correlation provides a necessary resource for this contrast, but not that every correlation produces a response.

For any fixed Hermitian carrier observable O with operator norm at most one,

\[
\Delta_C\ge\tfrac12
\left|\operatorname{Tr}[O\Phi(\Gamma)]\right|
=\tfrac12\left|\operatorname{Tr}[\Phi^*(O)\Gamma]\right|.
\tag{10}
\]

Equivalently, any effect `0<=E<=I` gives `Delta_C >= |Tr[E Phi(Gamma)]|`. In particular, the already registered occupation projection `n_0` gives `Delta_C >= |delta_n_0|`. A weak or zero occupation witness does not force zero trace distance; the complete state difference may live in other observable directions.

If a carrier unitary V is applied after the joint continuation, the reduced difference becomes `V Phi(Gamma) V†`; its trace norm is unchanged. Thus frozen common carrier transport cannot amplify the primary Delta_C, although it can rotate the difference into or out of a fixed occupation/configuration readout. Any later common carrier CPTP map can only reduce the primary trace distance. This is consistent with the protocol's transport-invariance control.

A useful counterexample to careless reasoning is the identity continuation. It gives `Phi(X)=Tr_S X=0` on K even when the input has strong joint correlations. Conversely, a common joint interaction can expose those correlations. The accompanying exact rational toy verifies both situations in a two-bit diagonal subalgebra.

## 7. What the accepted L4 result establishes

The existing independent L4 result is `Delta_C=0.14761185701903007` at its registered numerical tolerance, with equal complete input marginals and weights and with the stated controls. Within that finite numerical certificate it supplies one concrete `Gamma_4 in K_4` for which `Phi_4(Gamma_4)` is resolved nonzero. Therefore the pair of separate marginals is insufficient to predict this frozen common continuation for the actual/product comparison family.

It also demonstrates failure of full-domain marginal sufficiency for that same channel, because the tested pair is contained in the full domain. The new theorem explains the logical implication; it does not convert finite-precision evidence into an exact symbolic nonzero proof. An exact analytic proof for the sealed numerical parent would require an exact representation or a certified error bound strictly below its nonzero effect.

The result does not invalidate the separately proved unread first-pass carrier closure: that statement uses a different continuation and domain. It does not prove failure for every state, every admissible future operation, or every system size. “Memory matters” here means the specified joint state affects a specified subsequent carrier state; it does not establish spacetime, classical gravity, consciousness, or a new force.

## 8. A falsifiable finite B3 target and an analytic extension route

**Proposed finite test, not yet frozen:** use the already specified independent owner-once constructions at `L=6,8`, the same symmetric sharp-q dephasing, complete same-q product comparator, event-zero reversible admission, frozen pulse/transport schedule, and post-transport carrier trace distance. Let `d4=0.14761185701903007` be the openly acknowledged development anchor and choose the explicit half-anchor floor `delta_star=d4/2`. This is a research convention, not a fundamental constant or a physically derived threshold.

Before opening any L6/L8 response, prospectively bind implementations, source/input custody, numerical tolerances, independent audit, and one acceptance rule. A concrete rule is:

\[
\min(\widehat\Delta_6-\varepsilon_6,
     \widehat\Delta_8-\varepsilon_8)\ge\delta_\star,
\tag{11}
\]

where epsilon_L is a justified upper bound on total numerical uncertainty. A rigorous interval entirely above the floor supports this finite persistence target; an upper bound entirely below the floor at either size refutes it; an interval straddling the floor is unresolved. Failed controls remain invalid/unresolved, not a zero. If only empirical coarse/fine tolerances are available, the outcome must be labeled a tolerance-based numerical certificate rather than a rigorous error-bound theorem. Report the raw Delta values regardless of the decision. A resolved nonzero effect below the floor still supports that size's mechanism while failing this stronger persistence target. No parameter, event, sign, graph, or observable may be replaced after results to rescue this test.

This proposal deliberately does not claim the existing L6 preproduction packet already authorizes equation (11); it would need its own review/freeze. The half-anchor choice may be revised during open design, but must then be fixed before new response access and kept in the historical record.

**A genuine all-size theorem would need more than a finite panel.** For a prospectively defined family `(rho_L,P_L,Phi_L)` and bounded output observables `||O_L||<=1`, prove from unchanged parent dynamics that

\[
\left|\operatorname{Tr}[\Phi_L^*(O_L)\Gamma_L]\right|
\ge 2\delta>0
\quad\text{for every L in the declared family}.
\tag{12}
\]

Then equation (10) immediately proves `Delta_L>=delta` uniformly. The work is to derive both a nonvanishing correlation component and its noncancelling channel/readout overlap. An input-correlation lower bound alone is insufficient because the continuation may annihilate it. Nonzero channel coupling alone is insufficient because the actual state can lie in its kernel. A structural proof should exploit the fixed local admission to control the pulled-back observable and separately bound the native checkpoint correlation it samples; carrier transport can be removed from the trace-distance question by unitary invariance. The fixed site occupation is a simple predeclared candidate witness, not guaranteed to provide a successful uniform bound.

For a stronger algebraic obstruction, proving `Phi_L(K_A,L)=0` would instead establish that the declared reachable family has no response of this type. Both the positive theorem and this negative theorem are informative. Neither follows from the L4 result or from two further numerical sizes. Even a successful uniform response theorem would establish persistent operational joint-state dependence; a derived metric, curvature, continuum, RGRL, and Einstein response would still require their own bridges.

## 9. Verification and review boundary

`verify_lineage_response_toy.py` uses only Python's standard library and exact rational arithmetic. It checks normalized correlated/product inputs with equal separate marginals; a common reversible XOR permutation producing output trace distance exactly `1/2`; identity and lineage-copy readouts annihilating the complete one-dimensional **classical diagonal** correlation subspace; and the full diagonal basis census. It is a transparent constructive example and a check on conventions, not a replacement for the general proof or an UNT calculation.

Independent review should specifically challenge: the chosen input algebra and output embeddings; full-domain versus restricted-family necessity; product-map nonlinearity; compatibility constraints on marginal tuples; both directions of the equivalence; the dual local-sum characterization; trace-distance factors of two; and the difference between a numerical certificate and a rigorous nonzero proof. That independent project-internal analytic review is now recorded in `INDEPENDENT_REVIEW_LINEAGE_RESPONSE_LEMMA_V001.md`, with verdict `ACCEPT_FINITE_DIMENSIONAL_MATHEMATICS_WITH_STATED_SCOPE`. This is not external peer review or verification that the UNT family satisfies the proposed all-size hypotheses.
