# I0: necessary active/maintenance allocation and energy law

Date: 2026-09-27. Scope: analytical necessary conditions and one proposed next test; no numerical run, cosmological fit, physical volume invention, or change to a prior construct.

## 1. Question, sources and premises

The primary question is whether a single network rule allocates its finite causal resources in a way that produces both dust-like and vacuum-like effective responses. Naming one share “active” and another “maintenance” does not establish this.

The earliest exact control is already available in the supporting native hold: retained register occupations are conserved without required refresh or ongoing external drive. That is an occupation-retention result, not absence of internal dynamics or preservation of every quantum phase. A positive maintenance burden for those occupations therefore needs an explicit additional requirement or mechanism. This control constrains that parent; it is not a universal UNT result.

This note follows the revised [joint plan, I0.1–I0.5](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_JOINT_PLAN_V002.md:99>), especially the separate obligations to derive capacity, allocation and an energy/work/stress map. Its [I1 scaling screens](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_JOINT_PLAN_V002.md:130>) explicitly distinguish physical stress from density slopes. The resident [same-parent energy audit](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/SCIENTIFIC_NEXT_CONSTRUCT.md:101>) supplies a useful supporting counterexample: conserved native records can exchange interaction energy, while source-off retention requires zero external power. It is not a derivation of the primary split.

The following assumptions are conditional imports, not findings about UNT:

1. A common clock and differentiable positive material volume \(V(t)\) have an independently specified operational meaning. Write \(\theta=\dot V/V\); only if a cosmological interface is adopted does \(V\propto a^3\) imply \(\theta=3H\).
2. Complete component energies include their declared shares of interactions/binding; remaining components, reservoirs and externally controlled terms are kept in the ledger.
3. Effective components share a homogeneous isotropic rest frame and admit pressure work. The proposed identification is active \(\leftrightarrow d\), maintained \(\leftrightarrow v\), with \(p_d=0\), \(p_v=-E_v/V\), and \(E_d,E_v\geq0\). This identification is to be tested, not defined into success.
4. The component balance used below follows either an explicitly adopted local perfect-fluid conservation interface, or a valid reversible/quasistatic work description. A total derivative along changing entropy, record number, graph-cell number or other controls is not automatically a pressure derivative.

No Einstein acceleration equation is needed for the algebra. Interpreting the result as gravitational acceleration, lensing or cosmological phenomenology needs the separately stated gravity/probe interface. The homogeneous split does not establish independent perturbation fluids, collisionlessness, stability or a universal geometry.

## 2. The stock, flow, energy and stress dictionary

These are different objects even if a model uses similar names:

| Object | Meaning | What does not follow |
|---|---|---|
| \(W(t)\) | Accumulated write events, with \(\dot W=\Gamma_{\rm write}\) for a stated convention | It is not the number of distinct records still retained. Rewrites may increase \(W\) without increasing storage. |
| \(D(t)\) | Live retained record occupation/count | It needs a stock equation: creation minus deletion/reversal and net outward transport. Constant \(D\) need not mean constant record-associated energy. |
| \(K_{\rm mem}\) | Available storage slots or another specified information-capacity measure | A storage bound is not an operation-rate bound or an energy density. |
| \(A,M,C\) | Actual active and maintenance rates and causal operation-rate capacity in the same clock/units | A bound on \(A+M\) does not say how much is used, or how it is allocated. |
| \(P_{\rm maint}\) | Actual maintenance work/heat supplied per unit time in a specified protocol | It is not a stock of energy. It can flow through a subsystem into another one without accumulating there. |
| \(E_i,p_i\) | Stored component energy and physical isotropic stress | They require a Hamiltonian/work coupling and state, including interactions; neither follows from the name of a count or rate. |

For disjoint operations of equal resource cost, a capacity constraint might be
\[
A+M\leq C.
\]
With overlap or different costs it must instead use a declared resource-accounting matrix, for example \(\sum_i c_{ri}\Gamma_i\leq C_r\). Counting an operation in both labels cannot consume the same physical resource twice. A finite causal bound alone also does not specify the accumulated initial record population.

In particular, \(E=P\tau\) requires a physical residence/storage time and a loss/work law, not an arbitrarily chosen averaging interval. A component energy obeys an integrated first law, not “energy equals ongoing cost” by definition.

In the supporting native hold, \([H,q_v]=0\), \(\partial_tH=0\), but the allocated record–link interaction energy can vary. Thus occupation retention, internal energy exchange and externally supplied power are demonstrably distinct [within that parent](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/SCIENTIFIC_NEXT_CONSTRUCT.md:103>). This cannot be transferred to a different primary parent without a map; it does rule out using that native hold as evidence for a compulsory positive maintenance power.

## 3. Most general necessary homogeneous allocation identity

Let \(Q\) be internal exchange power per unit volume, positive from the vacuum-like to the dust-like sector. Let \(S_d,S_v\) be all other net supplies per unit volume after pressure work is separated: external driving, heat, exchanges with omitted material, and any correctly derived boundary transport terms. Write \(S=S_d+S_v\).

The claimed component stresses require
\[
\dot E_d=V(Q+S_d),\qquad
\dot E_v=\theta E_v+V(-Q+S_v).                 \tag{1}
\]
For \(E=E_d+E_v>0\) and energy fraction \(f=E_d/E\),
\[
\boxed{\dot E=\theta(1-f)E+VS},               \tag{2}
\]
\[
\boxed{Q=\frac EV\left[\dot f+\theta f(1-f)\right]
                +fS-S_d}.                  \tag{3}
\]
These are necessary regardless of how the network realizes the split. They are also sufficient for the two scalar balance equations after assigning \(E_d=fE,E_v=(1-f)E\); that is an accounting sufficiency, not microscopic existence or correct physical stress.

Indeed, for any admissible differentiable \(f(t)\in[0,1]\) and specified supplies, put
\[
G(t)=\exp\!\left[\int_{t_0}^t\theta(s)(1-f(s))\,ds\right],
\qquad
E(t)=G(t)\left[E_0+\int_{t_0}^t\frac{V(s)S(s)}{G(s)}\,ds\right]. \tag{4}
\]
When this energy stays positive, equation (3) supplies a compatible exchange. Thus conservation alone leaves an entire function \(f(t)\), an energy normalization \(E_0\), and any unclosed supply histories undetermined. Choosing \(Q\) after choosing the desired \(f\) is not a prediction of allocation.

“Closed” below means net-energy-closed, \(S=0\), with no unaccounted non-pressure energy supply; this does not imply \(S_d=S_v=0\) individually, nor \(\dot E=0\) for an expanding pressure-bearing material region. Negative-pressure work gives the first term of (2). For an open causal/horizon region, its boundary flux must be derived before this closed specialization is used.

An additional non-identifiability warning: at this common-frame background level, any complete stress with \(-\rho\leq p\leq0\) admits the algebraic representation
\[
\rho_v=-p,\qquad \rho_d=\rho+p.
\]
This relabeling is not evidence for a record-allocation mechanism. A physical explanation must constrain the total stress and its responses independently of this decomposition.

### Two useful special cases

With \(S_d=S_v=0\) and \(Q=0\),
\[
E_d=\mathrm{constant},\quad E_v\propto V,\quad
\dot f=-\theta f(1-f),\quad
\frac{\rho_d}{\rho_v}\propto V^{-1}.          \tag{5}
\]
For \(V\propto a^3\), these are the separately standard \(a^{-3}\) and constant density laws. Their normalizations are not selected by (5).

If instead \(r=\rho_d/\rho_v=f/(1-f)>0\) is constant, the required exchange is
\[
Q=\theta\frac{\rho_d\rho_v}{\rho_d+\rho_v},\qquad
\rho_d,\rho_v\propto V^{-r/(1+r)}.            \tag{6}
\]
Both are then nonstandard separate density histories: constant ratio, separately standard dust dilution and constant vacuum density cannot all hold in an expanding closed two-component system. Specifying (6) preserves any initial \(r\); it does not select one.

A density slope also cannot substitute for the stress test:
\[
-\frac{\dot E_i}{\dot V}
=p_i-\frac{V(Q_i+S_i)}{\dot V}
\]
where the signed \(Q_i\) is the corresponding component exchange and \(\dot V\neq0\). Formation-powered energy growth can therefore mimic negative pressure in this path derivative even when the measured component stress is zero.

## 4. What a bandwidth-to-energy hypothesis would have to satisfy

To expose the missing constitutive input, consider—not adopt—the simplest linear map
\[
R=A+M=uC,\quad 0\leq u\leq1,\quad
\alpha=A/R,\quad
E_d=k_d\alpha R,\quad E_v=k_v(1-\alpha)R,       \tag{7}
\]
for \(R>0\), constant positive \(k_d,k_v\). These constants have units energy·time/operation if \(R\) is operations/time. They encode a physical storage/residence and transduction law; they are not merely energy per operation. Nonlinear/state-dependent maps are allowed but bring additional derivatives and must be derived and censused.

All exponent conclusions in this section rely on those constants remaining fixed. A scale-dependent residence/transduction law changes them and is a new physical input, not an exception silently allowed in the same test. No general prohibition on an area-based causal capacity follows.

Let
\[
K(\alpha)=k_d\alpha+k_v(1-\alpha),\qquad
g=\frac{\dot R}{R}=\frac{d\ln(uC)}{dt}.
\]
Equations (2)–(3) imply the exact necessary screen
\[
\boxed{K g+(k_d-k_v)\dot\alpha
       =\theta k_v(1-\alpha)+\frac{VS}{R}},     \tag{8}
\]
\[
Q+S_d=\frac{k_dR}{V}(\dot\alpha+\alpha g).     \tag{9}
\]
Internal exchange cannot repair a violation of (8), because it cancels from the total ledger. Neither a capacity inequality nor saturation \(u=1\) implies this identity.

For equal constants and no supply, (8) reduces, when \(\theta\neq0\), to
\[
1-\alpha=\frac{g}{\theta}.                    \tag{10}
\]
For expansion, \(0\leq g\leq\theta\) is therefore necessary in this particular map. If independent network and operational-volume laws fixed both \(g\) and \(\theta\), (10) would genuinely constrain allocation. Deriving those laws and the map, rather than selecting them to reproduce a target share, is the constructive opportunity. If utilization \(u\) is unfixed, a law for capacity \(C\) alone still does not fix \(g\).

For unequal constants, even a known bandwidth fraction is not the energy fraction:
\[
f=\frac{k_d\alpha}{k_d\alpha+k_v(1-\alpha)}.  \tag{11}
\]
Under (7), imposing zero exchange and zero supplies further forces
\[
\dot\alpha=-\theta\alpha(1-\alpha),\qquad
g=\theta(1-\alpha).                          \tag{12}
\]
A fixed nontrivial share with expansion cannot simultaneously realize both uncoupled standard density laws. If an allocation model predicts a fixed share, its required exchange and changed density histories must be carried into I1 rather than silently imposing the uncoupled laws.

## 5. Minimal explicit candidate rule—what must be new

A small prospective allocation rule, AM-min, is:
\[
M=\mu(s)D,\qquad
A=\min\{A_{\rm demand}(s),\,C(s)-M\},
\quad\text{provided }0\leq M\leq C.           \tag{13}
\]
Here \(s\) is the actual network state, \(A_{\rm demand}\geq0\), and \(\mu\) has units operations/(retained record·time). If \(M>C\), the declared retention requirement fails; the model must not silently cap maintenance while claiming the same fidelity. Unused capacity is allowed. This is a prospective rule, not frozen or executed physics.

This maintenance-first rule adds explicit assumptions: an operational retention/error tolerance, a local noise/recovery or intrinsic-refresh law determining \(\mu\), a write-demand/formation law determining \(A_{\rm demand}\), and the scheduling priority. Homogeneous per-record cost is itself a simplifying assumption; heterogeneous costs replace \(\mu D\) by a specified sum. These functions are not arbitrary cosmological fitting functions, and the initial stock must remain declared. If the chosen parent gives exact passive retention with no required refresh, its minimum operational \(\mu\) is zero. A positive value then needs new physics, not the fact that records remain present.

AM-min closes rates only after its inputs are fixed. It does not establish (7), manufacture a vacuum energy from power, or select a physical pressure. Those still come from the same-parent complete energy and deformation/work law. Any newly added noise, scheduler, transduction or strain rule receives a construct ID under V002; an adopted conditional interface can be tested without first deriving all gravity.

## 6. One implementable next test: exact derivative closure of the allocated budget

For the first frozen primary candidate, derive \(A,M,C\) from its generator and scheduling rule and derive \(E_d,E_v\) from its Hamiltonian and actual retained state. Do not project the actual state into a preferred ground branch or fit conversion constants to density targets. Use one explicitly supplied material-volume/work interface; do not vary graph-cell count while omitting the corresponding composition/chemical work.

If the candidate claims the linear map (7), calculate the symbolic residual
\[
\mathcal R=
K\,\frac{d\ln(uC)}{dt}
+(k_d-k_v)\dot\alpha
-\theta k_v(1-\alpha)-\frac{VS}{uC}.          \tag{14}
\]
It must vanish on every admitted history in the claimed regime. Also check the independently defined work response, rather than defining it from (14): the claimed total stress requires \(p_{\rm work}=-E_v/V\). A component claim needs its own consistent interaction/work allocation as well. Failure of either condition rejects that candidate's dust/vacuum identification without an abundance comparison. Passing is a necessary I1 entry condition, not proof of a dark-sector explanation.

When (7) is not claimed, use the unconverted exact residual \(\dot E_d+\dot E_v-\theta E_v-VS\) and the same independent work test. This is the same derivative-closure test, not a requirement to force a linear map.

The cheapest limiting case is source-off retention: any proposal that equates positive maintained energy directly to a minimum rate must survive the possibility \(M=0\) while records and stored energy remain. The supporting native parent already realizes that limit; the selected primary parent must be evaluated on its own terms.

**Next deliverable:** one exact same-parent evaluation of (14), or its unconverted form, and the independently specified work response. This remains a prospective test until a concrete allocation/transduction/work law is supplied. No known density target is needed; another fit of a chosen fraction or another one-link coordinate verification does not supply the missing law.

## Review scope

A same-family agent independently checked the signs and factors of (1)–(14), including the external-supply term, constant-r dilution, unequal-conversion zero-exchange case and residual. No blocking issue was found. Its two wording suggestions—nonnegative demand and the distinction between zero net supply and zero individual supplies—are incorporated. The root also independently hand-checked the algebra. These are analytical consistency checks using shared premises, not independent empirical confirmation, numerical execution or a frozen physical mechanism.
