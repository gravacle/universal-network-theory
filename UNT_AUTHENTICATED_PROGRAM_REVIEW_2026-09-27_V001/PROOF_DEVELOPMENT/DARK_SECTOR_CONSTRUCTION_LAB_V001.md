# A0 record-budget construction laboratory

Date: 2026-09-27. Version V001.

Status: **HYPOTHESIS_CONSTRUCTION_AND_CONDITIONAL_IDENTIFIABILITY_LEMMAS__PROJECT_INTERNAL_ANALYTIC_REVIEW_PASSED_AT_CONDITIONAL_SCOPE**.

An independent project reviewer checked the pressure/exchange signs, donor budget, ratio equation, no-acceleration and rate-attractor propositions, and reran all 33 exact rational toy checks. Review identified and repaired an unjustified stochastic mean-closure implication by retaining the finite-donor acceptance indicator and separating the deterministic fluid idealization. This accepts the conditional algebra/construction scope; it is not external peer review or validation of the proposed microscopic law as UNT physics.

This document begins building candidate missing elements. It is not a derived UNT dark-sector result, an accepted I0/A0 freeze, a cosmological fit, or a blind preregistration. The earlier proposal's comparison targets have already been seen; none is used here. This laboratory supplies explicit conditional bookkeeping, proves what that bookkeeping cannot identify, and offers one optional maintenance-rule family that can be rejected on its own predictions. Historical prerequisite failures remain historical facts; this new candidate must earn its own acceptance.

There are two possible research branches. The **effective-GR branch** below assumes a physical FRW metric and covariant stress conservation, then asks whether a specified record mechanism has distinctive consequences within that setting. The **fundamental UNT branch** must additionally derive/calibrate that common physical metric, stress, volume, and continuum correspondence. Work in the effective branch can proceed conditionally in parallel, but cannot be relabeled as completion of the fundamental branch.

## 1. Declared bookkeeping and assumptions

Adopt an FRW scale factor `a(t)>0`, proper time t, and `H=dot(a)/a`. Use units `c=1`. Select a fixed comoving reference region of coordinate volume V0, so its physical volume is

\[
V(t)=V_0a(t)^3.
\]

This is an assumed volume map, not a consequence of finite UNT record counts. No horizon volume is substituted: a moving horizon would introduce boundary flux and must be modeled separately.

For component i, define a nonnegative number/count expectation `N_i(t)` and mean physical stored energy per counted item `epsilon_i(t)>0`. Its comoving stored energy and physical density are

\[
E_i=\epsilon_iN_i,\qquad
\rho_i=\frac{\epsilon_iN_i}{V_0a^3}.
\tag{A0.1}
\]

Counts must be tied to a prospectively specified microscopic observable and population partition. The word “retained” can denote a property shared by active and maintained records; it must not become a third additive population unless a mutually exclusive partition is supplied. Energy stored in a record and energy spent maintaining it are distinct quantities. A maintenance power is a transfer rate, not another stored-energy density to add indefinitely.

Assume isotropic background stresses p_i and energy-transfer rates Q_i per physical volume and proper time, positive into component i:

\[
\dot\rho_i+3H(\rho_i+p_i)=Q_i,\qquad
\sum_iQ_i=0.
\tag{A0.2}
\]

Every energy donor, receiving bath, retained field, controller, and relevant interaction energy must appear once in the complete stress budget. A two-component model is closed only if its two Q values really sum to zero without an omitted reservoir. A consistent microscopic split must also specify the covariant transfer vectors `Q_i^mu`, whose FRW energy projections give (A0.2). Scalar background balance alone is not a full local stress theorem.

On intervals where H, N_i, and rho_i are nonzero, substitution gives the identity

\[
\frac{\dot\epsilon_i}{\epsilon_i}
+\frac{\dot N_i}{N_i}
+3H w_i=\frac{Q_i}{\rho_i},\qquad
w_i:=\frac{p_i}{\rho_i}.
\tag{A0.3}
\]

Equivalently,

\[
\dot E_i+3HVp_i=VQ_i.
\tag{A0.4}
\]

Use the nonsingular forms (A0.2)/(A0.4) at zeros or H=0. Equation (A0.3) is a constraint, not an equation-of-state derivation from record counting alone.

## 2. Proposition A: identical density histories do not fix pressure or exchange

Fix any positive differentiable density history rho_i(t) and an expanding background. For any chosen differentiable pressure p_i(t), define

\[
Q_i=\dot\rho_i+3H(\rho_i+p_i).
\]

It satisfies component conservation identically. Conversely, any selected Q_i determines a pressure through the same equation. Thus even a completely known N_i and epsilon_i history, which fixes rho_i, cannot separately determine both p_i and Q_i. The transformation

\[
p_i\longmapsto p_i+f_i(t),\qquad
Q_i\longmapsto Q_i+3Hf_i(t)
\tag{A0.5}
\]

leaves the density history unchanged. For a complete closed collection, choose `sum_i f_i=0` to preserve total exchange conservation and total pressure. Positivity, reservoir availability, and microscopic stress laws can restrict this freedom; the counting identity does not. QED.

There is a second algebraic ambiguity: for any positive function b_i(t), replacing `N_i -> b_i N_i` and `epsilon_i -> epsilon_i/b_i` leaves density invariant. This is a background identifiability statement for coarse-grained count expectations, not permission to relabel an already defined exact integer count. A fixed native count observable and an independently derived energy map must remove this ambiguity.

### Three informative cases

**Fixed count and fixed stored energy, no exchange.** If `dot N=dot epsilon=Q=0`, (A0.3) gives `w=0` on an expanding interval, and `rho proportional to a^-3`. This is conditional dust bookkeeping. Being a persistent record does not by itself supply negative pressure.

**Constant density as a separately conserved component.** If `dot rho=0` and Q=0, (A0.2) requires `p=-rho`. In count language, `epsilon N proportional to a^3`; that growth needs a microscopic/constitutive account. A closed comoving region has `dot E=-p dot V`, so negative-pressure work is consistent with increasing comoving energy in GR. Writing that equation is not a derivation of the required stress from records.

**The same constant density with dust pressure and injection.** If `dot rho=0` and p=0, then `Q=3Hrho`. It is replenished dust, not a separately conserved negative-pressure component. A donor must carry `Q_donor=-3Hrho` (or other components must supply the same complete outflow). With a pressureless donor,

\[
\frac{d}{dt}(\rho_{\rm donor}V)
=-3H\rho V=-\rho\dot V,
\]

so for constant recipient rho,

\[
E_{\rm donor}(t)=E_{\rm donor}(t_0)
-\rho\,[V(t)-V(t_0)].
\tag{A0.6}
\]

A finite nonnegative donor budget cannot sustain this prescription through arbitrarily large expansion. Once its energy is exhausted the rule fails or must change explicitly. Ignoring that donor would conceal a violation of the declared budget. Although the recipient density equals that of the previous case, its pressure and the complete system's evolution differ.

The frequently used algebraic “effective equation of state”

\[
w_i^{\rm eff}=w_i-\frac{Q_i}{3H\rho_i}
=-1-\frac{\dot\rho_i}{3H\rho_i}
\]

only describes the component's dilution law. It is not generally its physical stress ratio p_i/rho_i. In particular, injected dust with constant rho has `w_eff=-1` while its physical w remains zero.

## 3. Proposition B: the abundance ratio is not selected by the accounting identity

For two record components A and M in the same volume,

\[
r=\frac{\rho_M}{\rho_A}
=\frac{\epsilon_MN_M}{\epsilon_AN_A}.
\tag{A0.7}
\]

If they are a closed pair with `Q_M=Q=-Q_A`, their ratio obeys

\[
\frac{\dot r}{r}
=-3H(w_M-w_A)
+Q\left(\frac1{\rho_M}+\frac1{\rho_A}\right).
\tag{A0.8}
\]

If donors or baths exist, use their actual Q values rather than the closed-pair reduction. The initial ratio is independent input unless a formation law or a proved attractor removes it. Even fixed w_A,w_M and Q=0 give

\[
r(a)=r(a_0)(a/a_0)^{-3(w_M-w_A)}
\]

for constant w values. The normalization r(a_0) remains free. More generally, arbitrary positive ratio histories can be installed through free densities/pressures/exchange and a compatible energy partition. Thus a value chosen for a ratio is not a prediction merely because it solves the continuity equations. QED.

A stable attractor can remove sensitivity to some initial ratios. It becomes a prediction only if its location and relaxation timescale are fixed independently by the microscopic law, its basin includes the admitted initial-data class, and finite-time residual dependence is bounded. Choosing a rate ratio to place an attractor at a desired abundance is calibration, not an explanation of that abundance.

An especially direct underdetermination construction is available even with Q=0: for any positive count expectation N(a) and any chosen smooth w(a), let `E(a)=C exp[-3 integral w(a) dln(a)]` with arbitrary C>0 and set `epsilon(a)=E(a)/N(a)`. Equations (A0.1)–(A0.3) then realize that equation of state. The construction is a mathematical counterexample to identification from counts alone; it does not assert that every such epsilon has a healthy microscopic realization. A native energy/stress law is exactly what must restrict the freedom.

### Functional and initial-data count

For a specified a(t), n fluid backgrounds have `n densities + n pressures + (n-1) independent exchange functions`, a total of `3n-1` functions. Their n continuity equations leave `2n-1` functional choices before microscopic constitutive laws. Decomposing each density into epsilon_i and N_i adds n unidentifiable factorization functions if those quantities have no independent definitions. For two components, continuity alone therefore leaves three physical background functions plus two count/energy factorization choices.

This count concerns the continuity system with a given background; it is not a count of all GR degrees of freedom. Adding a Friedmann equation constrains the total background and a(t), but does not by itself identify component pressure, transfer, or abundance split. Once w_i and Q_i are specified as genuine constitutive functions of state and time, the first-order background system still needs component initial densities, subject to whatever gravitational constraint and formation conditions are separately imposed. Perturbations require further laws and initial data.

## 4. An optional microscopic token-maintenance family

The following explicit toy family is a **candidate construction**, not an adopted UNT law. It illustrates a legal energy budget and tests whether maintenance alone yields a dark-energy-like stress. Its assumptions must be replaced or earned before cosmological use.

1. There are `N_star>0` comoving memory tokens, each carrying a classical retained label and exactly one mutually exclusive status: active A or maintained M. A token cannot be counted in both. `N_A+N_M=N_star`. “Retained” denotes the live tokens jointly and adds no third density.
2. Both statuses have the same fixed stored rest energy epsilon>0. Tokens are assumed nonrelativistic with negligible kinetic/interaction pressure, so `p_A=p_M=0`. This is a physical-model assumption, not a consequence of the words active or maintained.
3. Each A token switches to M at rate alpha>=0; each M token switches to A at rate beta>=0. These symbols are local transition rates, unrelated to the electromagnetic fine-structure constant. The equal stored energies make these idealized status changes energy-neutral. Any real controller work beyond this idealization must be added to the budget.
4. Each M token undergoes a successful label-preserving maintenance event at rate nu>=0. An event consumes a positive energy e_kick from an explicit donor D and deposits exactly e_kick into bath B. The record's stored energy epsilon does not increase. The rule does not claim a microscopic implementation or assign a universal thermodynamic minimum cost. It states exactly where the hypothesized cost goes.
5. The donor is a finite pressureless energy store with nonnegative energy. The bath is assumed to be massless isotropic radiation, `p_B=rho_B/3`. These stress assignments are explicit candidate premises. Maintenance events are admitted only when the donor can pay. The model must stop or invoke a separately specified failure/decay law at exhaustion; it cannot borrow unrecorded energy.

For an individual live microscopic state, let n_M be its integer maintained count. The admissible maintenance jump intensity is exactly `nu n_M 1(E_D>=e_kick)`; an accepted jump changes `(E_D,E_B)` to `(E_D-e_kick,E_B+e_kick)`. Its total stored-energy change is exactly zero. For an ensemble of live states, the exact maintenance power is therefore `nu e_kick E[n_M 1(E_D>=e_kick)]/V`, not generally `mu E[n_M]/V`. Record count and donor availability can be correlated. A finite Poisson-driven donor can reach exhaustion with positive probability earlier than a mean-budget estimate, so no deterministic unexhausted interval is claimed for the stochastic process. A complete stochastic model must also specify the subsequent failed-maintenance/record-decay law.

For a separate **deterministic fluid idealization**, take N_A,N_M,E_D,E_B as continuous variables and stipulate the unsaturated maintenance rate `mu N_M`, where `mu=nu e_kick`. The following candidate equations hold only until deterministic donor exhaustion. They are not claimed to be exact closed first-moment equations for the finite-reservoir jump process:

\[
J=\alpha N_A-\beta N_M,\quad
\dot N_M=J,\quad\dot N_A=-J,\quad
P=\frac{\mu N_M}{V}.
\tag{A0.9}
\]

The component energy transfers are

\[
Q_A=-\frac{\epsilon J}{V},\quad
Q_M=+\frac{\epsilon J}{V},\quad
Q_D=-P,\quad Q_B=P.
\tag{A0.10}
\]

Their sum is exactly zero. The donor and bath energies obey

\[
\dot E_D=-\mu N_M,\qquad
\dot E_B+H E_B=\mu N_M.
\tag{A0.11}
\]

Radiation's H E_B term is its expansion work, not missing energy. For the full comoving volume,

\[
\frac{d}{dt}(E_A+E_M+E_D+E_B)=-H E_B=-p_{\rm total}\dot V.
\tag{A0.12}
\]

No maintenance energy is counted twice: token energies are counted once in A/M, depleted energy leaves D, and dissipated energy enters B. The cumulative integral of maintenance power is not added as another gravitational density after its energy is already in B or has been diluted by expansion.

### Proposition C: this maintenance family does not generate negative pressure

The total token energy is `epsilon N_star`, so the combined record density is exactly `epsilon N_star/(V0a^3)`. All assumed component pressures are nonnegative. Consequently this family has no physical negative-pressure component despite continuous maintenance.

If standard Einstein-FRW acceleration with positive G is additionally assumed, and no separate cosmological constant or other negative-pressure sector is inserted,

\[
\frac{\ddot a}{a}=-\frac{4\pi G}{3}
\sum_i(\rho_i+3p_i)\le0.
\tag{A0.13}
\]

Thus this explicitly budgeted maintenance model cannot produce accelerated expansion. This is a useful negative result for the specified candidate: “maintenance” alone is not an equation of state. It does not rule out every possible record mechanism. QED.

### Proposition D: the active/maintenance ratio in this family is tunable

For constant alpha,beta with alpha+beta>0, put `f=N_M/N_star`. Then

\[
\dot f=\alpha-(\alpha+\beta)f,
\quad
f(t)=\frac{\alpha}{\alpha+\beta}
+\left[f(t_0)-\frac{\alpha}{\alpha+\beta}\right]
e^{-(\alpha+\beta)(t-t_0)}.
\tag{A0.14}
\]

For alpha,beta>0 the asymptotic M/A energy ratio is alpha/beta. This attractor demonstrates selection by a **specified rate law**, but with alpha and beta freely chosen its location is a free model parameter. The relaxation timescale and finite donor lifetime also determine whether it is reached. With equal stored energies, maintenance expenditure mu does not fix that ratio. If `mu>0` and `N_M>=N_min>0` over an interval, a donor starting with finite E_D has support for at most `E_D/(mu N_min)` additional time under that lower bound. Extrapolating the attractor beyond energy exhaustion would invalidate its use. QED.

The toy therefore offers two early falsification gates: it fails as a source of acceleration under its stated stresses, and it fails as a parameter-free abundance selector until rates and admitted initial data are derived independently. Neither failure requires fitting observations.

### What remains free in the optional family

The candidate currently supplies free microscopic parameters alpha, beta, nu, e_kick, epsilon, a count/volume normalization, initial f, donor energy, and bath energy. A stochastic realization also needs its correlations and the fate of failed maintenance. The deterministic fluid equations above are a declared idealization; convergence from the budgeted jump process, moment closure, fluctuations, and cosmological coarse-graining are not proved. Treating any of these choices as a fitted parameter must be disclosed. No numerical value has been assigned here.

## 5. What would make a record rule predict w, a ratio, and perturbations

A viable successor must supply more than density bookkeeping:

| Required object | Concrete question to settle | What remains unidentifiable without it |
|---|---|---|
| Native population observable | Which microscopic states/operators define active versus maintained, exhaustively and without overlap? | Counts and their decomposition |
| Formation and maintenance generator | What creates, transfers, refreshes, or destroys records, with rates fixed by the parent rather than an abundance target? | N_i(t), rates, and normalization |
| Energy and stress construction | What Hamiltonian/action/metric variation gives stored energy, interaction energy, momentum, and pressure, counting each contribution once? | epsilon_i, physical w_i, conservation |
| Explicit resource genealogy | Which field/reservoir supplies each maintenance event, what stress does it carry, and where is dissipated energy stored or carried? | Q_i and total stress |
| Physical volume and coarse-graining | What selects V, maps records to it, and controls the finite-to-continuum error? | Density dimensions and cosmological interpretation |
| Initial-data selection or controlled attractor | What predicts populations, energy budgets, and the approach to an attractor over the admitted history? | Absolute abundance and ratios |
| Perturbative constitutive law | How do local rates, pressures, momenta, and transfers respond to density, velocity, entropy, fields, and metric perturbations? | Sound speed, stability, clustering, and discriminating observables |

Mechanical pressure cannot be read from a count label. In a suitable equilibrium system it is obtained from `p=-(partial E/partial V)_(entropy,N)`; more generally it comes from the complete stress tensor or action's metric variation. A proposal for constant density must therefore explain why the same microscopic rule gives the required negative pressure or explicit exchange, and verify that the complete budget remains consistent.

At linear perturbative level, background rho_i,p_i,Q_i are insufficient. One needs rest-frame pressure response and entropy perturbations, momentum densities/transport, anisotropic stress, the full `Q_i^mu` and its perturbation (including momentum transfer), rate responses and stochastic fluctuations, initial perturbations, and a well-posed stable causal closure. Assuming a numerical dark-energy perturbation prescription would close a chosen phenomenological model; it would not derive these ingredients from UNT. Likewise `w=0` is not enough to identify dark matter: production, phase-space transport, interactions, free streaming, and the relevant observable behavior remain separate obligations.

## 6. A constructive A0 work order

This open-design laboratory can now be used to build and reject candidates before expensive cosmology work:

1. Specify one candidate native partition and microscopic transition/maintenance rule with an explicit source of energy. Record whether each ingredient is derived, adopted for the test, or free.
2. Derive its component stored energies and stresses. Prove no double counting and either separate conservation or a complete exchange ledger, including every donor and bath.
3. Eliminate N_i and epsilon_i where possible to obtain autonomous constitutive equations. List every remaining function, constant, and initial datum; exhibit whether changing it changes the proposed ratio or w.
4. Prove an identifiability result or a no-prediction result. A freely adjustable normalization, exchange history, or rate ratio is a concrete failed prediction gate, not a reason to select a convenient value silently.
5. If the background is both closed and independently motivated, derive perturbations and stability from the same rule. Keep an effective-GR conditional test separate from a claimed microscopic derivation of the metric/gravity law.
6. Only after the candidate survives these analytic gates, prospectively freeze a new prediction and comparison procedure. Previously seen targets cannot become blind by omission from a later document; any genuinely held-out comparison needs new independent custody and an honest exposure history.

The immediate intellectual target is a **constitutive selection theorem**: a source-defined record dynamics plus a complete energy/stress ledger should force a restricted family of dilution, pressure, exchange, and perturbation laws, ideally with a rate/ratio fixed by symmetry or dynamics rather than observations. The optional family above does not yet achieve that target, but it makes the failure precise and identifies what a better mechanism must change. No A0 pass, dark matter, dark energy, or cosmological conclusion is claimed by this construction note.

## 7. Quick discriminating tests before a complete proof

The standard-library script `verify_dark_sector_construction_toy.py` checks the following with exact rational arithmetic. All fixture values are arbitrary small fractions, not observations, fitted constants, or nominated physical values. These are **model-construction kill tests**, not evidence for UNT physics. A failure of the implementation would invalidate the claimed algebraic check; a passing check can expose a failed physical interpretation of an otherwise consistent toy.

The local 2026-09-27 run passed **33 exact rational checks** in **0.000309292 seconds of measured in-process wall time**, excluding interpreter startup. No cosmological or stochastic simulation ran. The script also demonstrates why a finite donor's exact accepted maintenance rate cannot be replaced automatically by an unconditioned mean rate, and checks per-jump energy conservation.

| Quick test | Competing explanation it separates or rejects | What a pass actually establishes |
|---|---|---|
| Constant-density pressure/exchange contrast | “Constant density necessarily means physical negative pressure” versus replenished dust | Identical density histories can have different physical pressures and explicit donors |
| Pressure/exchange transformation | A density-derived equation of state versus an unspecified transfer law | Density alone cannot identify both physical p and Q |
| Donor exhaustion | “Maintenance/creation supplies energy indefinitely” versus finite resource custody | A claimed background fails beyond the actual energy budget unless new physics/resources are explicitly supplied |
| Complete A/M/D/B energy balance | A cumulative maintenance cost counted as new stored mass versus paid-through energy | The specified toy conserves its complete background energy budget without double counting |
| Finite-donor jump acceptance | An exact stochastic first-moment law versus an assumed deterministic mean-field closure | Donor availability must remain inside the expected event rate unless a closure is proved |
| Pressure/acceleration sign | “Maintenance alone explains acceleration” versus dust plus dissipative radiation | This particular funded-maintenance family cannot accelerate conditional Einstein-FRW expansion |
| Rate-attractor and finite-time initial-data variation | A predicted abundance versus freely placed attractor/initial ratio | The candidate's abundance is adjustable until its rates and initial-data selection are independently fixed |
| Count/energy-map variation | A ratio derived from record numbers versus an assumed per-record energy assignment | Counts do not fix an unearned energy-density ratio |

These tests earn modest but useful confidence: they eliminate specific unsupported inferences early and preserve only candidates that have actually survived a stated challenge. Positive support for a record mechanism would require a new native rule whose stress, exchange, and observable consequences outperform an explicitly frozen comparison, not merely a bookkeeping identity shared by generic fluids.

### Minimal fields for the next candidate-rule freeze

Before testing a new microscopic candidate, freeze one compact record containing:

1. candidate identifier, version, exact source hashes, prior exposure history, and which ingredients are derived versus hypothesized;
2. the native state space, active/maintained count operators or measurable predicates, exhaustive partition, and handling of dead/failed records;
3. the fixed generator/channel/transition rates, initial-state class, admitted controls, and boundary conditions;
4. stored energies, interaction/controller/reservoir ownership, complete stress definition, physical-volume map, and the declared gravitational premise;
5. every exchange channel and finite resource budget, with a nonnegative-energy/exhaustion/failure rule;
6. the chosen null/comparison candidate, which free parameters remain, the one predicted statistic or algebraic identity, numerical or exact acceptance rule, and what outcome would kill the proposed interpretation;
7. the perturbation law needed for any proposed clustering/stability claim, or an explicit background-only ceiling; and
8. a prospective record of the result and uncertainty, including nulls, before selecting a successor rule.

A cheap first native test should ask whether the independently specified record generator and energy/stress map actually constrain p and Q beyond the algebraic family in Proposition A. A second should vary allowed initial populations and resource budgets to test whether a claimed ratio is truly selected or merely normalized. These are high-information tests that do not require a survey likelihood or a large cosmological calculation. Their design can guide a later definitive selection theorem without claiming that a few successful tests prove the full UNT gravity chain.
