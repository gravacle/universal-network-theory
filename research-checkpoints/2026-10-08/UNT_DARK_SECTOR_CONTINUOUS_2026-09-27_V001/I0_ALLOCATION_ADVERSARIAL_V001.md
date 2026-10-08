# I0 active/maintenance allocation — constructive adversarial analysis V001

2026-09-27. Analytical work only: no numerical physics, remote work, change to
the primary rule, or assignment of a physical volume or gravitational law.

Reviewed resident inputs:

- `UNT_DARK_SECTOR_JOINT_PLAN_V002.md`, SHA256
  `6b2a8bee520e828f4ccc583db920f289fe0c0a9eefd85fd78c22b6db90da2ccc`.
- `SCIENTIFIC_NEXT_CONSTRUCT.md`, SHA256
  `68fe8aa680290b6d9aef23487e9f77fca40bc72d0e655d0806cb9d5db997437a`.
- The resident physical-adversarial plan review. The older energy/volume
  audit was flagged dataless and was not read or hydrated in this turn.

Reviewer provenance: same-family agent; shared plan and finite-parent reports.
The counterextensions below are independently assembled analytical checks,
not independent observations or proposed replacements adopted into UNT.

## Verdict and constructive target

Causal capacity plus a retained-record count **does not yet identify** the
active/maintenance allocation, complete source energy, stress or abundance.
This is an identifiability result about the supplied premises, not a rejection
of a network explanation. The missing inputs can be made small and testable.

The shortest stress-specific addition is the **microscopic response of the
complete Hamiltonian to one declared uniform network deformation**, together
with its work convention. The shortest allocation-specific addition is an
**actual local generator/scheduler identifying the events needed to retain a
record**, including any noise/reliability premise. A population prediction
also needs formation/transport and initial-condition laws. These are distinct
closures: a single capacity constraint cannot substitute for all three.

## 1. Capacity supplies an admissible set, not an allocation

For an operational clock, write capacity C(t), active throughput A(t) and
maintenance throughput M(t), all in the same events/time units. Even granting
the stronger nonoverlapping accounting convention,

    A >= 0, M >= 0, A + M <= C,

every M(t) in [0,C(t)] leaves admissible choices of A. Granting saturation
only replaces the region by A=C-M; it does not choose a point. For R>0,

    M=0, A=C                       (passive-retention allocation)
    M=kappa R, A=C-kappa R          (service-rule allocation),

both satisfy the same constraint wherever 0<=kappa R<=C. The second relation
introduces a new rate kappa and a servicing rule; neither follows from R or
causality. These are counterexamples to implication, not evidence that the
native model realizes the second mechanism. If active and maintenance events
overlap, even the displayed additive convention must first be justified.
If the original capacity instead counts simultaneous storage/causal slots,
the same allocation ambiguity applies in slot units; converting slots into
throughput additionally requires a justified clock or service-time law.

Replacing <= by = is a substantive saturation assumption. A reversible
network may have idle capacity, and a capacity ceiling supplies no demand
or objective selecting a scheduler. Knowing C and R at many times still
cannot infer a unique M unless an event law connects them.

An energy per serviced event e turns M into a power eM, not an energy
density. Turning it into stored energy requires an actual residence/exchange
law; multiplying by a chosen time scale supplies another premise. Work
per event, stored energy and gravitational response are not interchangeable.

## 2. The existing native hold is a useful passive-retention control

The source-off parent has [H,q_v]=0 and fixed H. Thus record occupation is
retained, while the external parameter-work rate Tr(rho partial_t H)=0.
There is no required refresh of occupation in this closed hold. Link and
carrier dynamics can continue; this is not a claim that the entire network
has zero activity, zero internal exchange or arbitrary error tolerance.
Occupation retention alone also does not certify retention of every quantum
coherence or performance under an additional noise channel.

The actual record-dependent energy is

    H_rec = epsilon_r R - lambda_R sum_v q_v d_v,

not epsilon_r R alone. With the stated incidence convention,

    d<H_rec>/dt = -lambda_R h sum_(u,v) <(q_u+q_v)Y_(u,v)>.

Its interaction allocation can vary while R stays constant, compensated in
the complementary energy ledger. Consequently neither zero external power
nor conserved R fixes a separate conserved matter energy. This is a direct
constraint from the retained parent, not an imported cosmological law.

Any nonzero necessary-maintenance proposal should identify the microscopic
failure channel or other retention condition absent from this control and
the corrective dynamics that change the conclusion. Adding a bath, refresh
term, error threshold or new clock is an explicit construct addition. There
is no requirement to invent one if the native rule implies zero overhead.

## 3. Explicit same-history counterextensions for stress

Let H_* be the complete finite parent at its present fixed control setting.
Let K be a fixed positive local record-energy operator, for example k R with
k>0. Introduce a dimensionless deformation control u>0 with reference u=1.
For each real alpha, define the prospective Hamiltonian family

    H_alpha(u) = H_* + (u^alpha - 1) K.

All families agree **exactly** at u=1. For the same initial state and control
held at u=1, every native trajectory, record count, carrier response and
energy is identical. Their generalized deformation forces differ:

    F_u = -Tr(rho partial_u H_alpha),
    F_u |_(u=1) = -alpha <K>.

The local finite Hamiltonians are well defined near u=1; no large-volume
limit, ground-state replacement or statistical assumption is needed. With
K=kR, the extra term also preserves the record-occupation conservation.
Thus no amount of additional fixed-u evolution can identify alpha. It is
the missing deformation rule, not a hidden numerical precision problem.
In this hold [H_*,R]=0, so the extra evolution factor is a product of local
record phases. It adds no inter-register propagation or operator-support
spread; a causal propagation bound alone cannot select its coefficient.
An additional capacity definition involving local energies or clock rates
would itself need to be supplied and tested, rather than assumed equivalent
to such a propagation bound.

This proves underdetermination even after every fixed-graph energy and
correlation observable is known. These are deliberately different possible
extensions, not a claim that alpha is a licensed adjustable UNT parameter.
Fitting alpha to the desired cosmology would not be a microscopic derivation.

### Conditional illustration of equations of state, with premises visible

Only if a material-volume interface is **adopted**, u=V/V0, and isotropic
mechanical pressure is defined by P=-<partial_V H>, do the above forces
become P_alpha(1)=-alpha<K>/V0. No Einstein or Friedmann equation is used.
Without the volume/work interface this remains a generalized-force result,
not a physical pressure prediction.

For the particularly simple toy record sector H_R(u)=u^alpha kR with fixed
R and no other sector assigned to it,

    E_R=u^alpha k<R>, rho_R=E_R/V,
    P_R=-alpha E_R/V, w_R=P_R/rho_R=-alpha.

The choices alpha=0, 1, -1/3 give respectively w=0, -1, +1/3 for this
conditional isotropic energy law, despite identical reference record energy
and count. They are labels for the three toy responses, not claims of CDM,
vacuum or radiation perturbations. Their energy changes satisfy
dE_R=-P_R dV at fixed R: deformation does work. They do not create energy
for free. The full native Hamiltonian contains additional contributions;
its total stress cannot be read off from this toy sector alone.

For the actual formed state, the force is the expectation of partial_u H
in that state, including its actual populations and coherences. It is not
automatically the derivative of a relaxed ground energy. A uniform response
fixes only the isotropic component: shear, anisotropic stress and sound
response require the corresponding deformation and dynamical closures.

## 4. Abundance is a separate identifiability test

During the native hold, [H,R]=0. Starting in any allowed population sector
therefore preserves that sector; a mixture with different population weights
preserves those weights. The hold supplies no law choosing the initial
population. Causality can bound a reachable population after a finite write
history; it does not pick the history or its occupation probabilities.

At the coarse level a population balance has the form

    d<R_region>/dt = formation - removal - outward current.

The terms must be derived from declared network dynamics and a specified
region; a moving causal boundary contributes its own flux. This equation is
bookkeeping, not a proposed formation model. Occupation stationarity does
not make the count-density cosmological prediction unique.

Even matched counts need not match energies: the exact insertion operator
epsilon_r I-lambda_R d_v depends on degree, and the common background can
relax or exchange energy. Even matched initial total energies need not match
stress, as the counterextensions prove. A capacity fraction is therefore
not automatically either an abundance fraction or an energy-density ratio.

## 5. Smallest constructive next derivation and exact decision

Keep the primary active/maintenance construct; do not substitute the shorter
retained-defect branch for its unclosed allocation rule. Use one compact
closure record, with derived/adopted/calibrated/unknown status for each item:

1. **Events:** specify a local native generator and projector/counting rule
   for active and necessary-retention events. State whether events overlap;
   identify the clock and reliability condition. Compute M for the passive
   source-off control. If no event is required, preserve M=0 as the result.
2. **One deformation:** specify a microscopic u-change on the same state
   space, or a stated embedding if graph growth changes it, and derive
   K_def=partial_u H|_1 from that change. Keep every affected interaction.
   The immediate analytic discriminator is the generalized work response
   -Tr(rho_actual K_def), with the full actual formed state. This can be done
   before a cosmological gravity law or a large graph simulation exists.
3. **Population:** state the minimal write/source, reversal and transport
   law plus initial-state inputs determining R. A supplied baryon population
   may be a declared external input; an intended output must not choose its
   own formation normalization or be reused as independent validation.

**Pass for the next analytical closure:** two implementations of the same
declared microscopic rule give the same event allocation, deformation-work
operator and population balance, with a complete interaction/work ledger.
No claim of an observational pass follows. A capacity inequality without
an event law, an unspecified K_def, or an unspecified formation law leaves
the corresponding prediction incomplete. An exact contradictory identity
rejects that specified construct; a different explicit microscopic addition
requires its own construct identity and affected rechecks.

No new numerical experiment is recommended until at least one of these
closures supplies a distinct, frozen prediction. The cheapest useful result
now can be a zero-maintenance proof, a derived nonzero local maintenance
law, or a unique deformation-work operator. Each materially constrains the
joint mechanism without requiring a prior proof of all emergent gravity.

## Cross-review of the parallel derivation

2026-09-27. Read the complete resident `I0_ALLOCATION_DERIVATION_V001.md`
at SHA256
`6f68299d49da23bcc2aec48dcc49d615bb8f36c759a03bf703a8e74dba64c064`.
Independently checked its scalar balance derivations (1)–(14). With Q positive
from the vacuum-like to dust-like sector, the signs, supplies and utilization
factors agree: Q=rho[dot f+theta f(1-f)]+f S-S_d, and differentiating
E=(uC)[k_d alpha+k_v(1-alpha)] gives its rate-budget residual exactly.
The constant-ratio dilution law and the unequal-k zero-exchange specialization
also check. No blocking algebraic or physical-scope defect was identified.

Its dust/vacuum work laws, common rest frame and rate-energy transduction are
explicit conditional premises, not a covert gravity derivation. Its AM-min
rule is prospective and requires microscopic retention, demand and scheduler
inputs; it is not presented as native evidence. The passive native control
is correctly kept distinct from the primary active/maintenance parent.
Suggested only two optional clarifications: make nonnegative write demand
explicit, and distinguish net-energy closure S=0 from complete absence of
reservoir contacts if the individual supplies remain nonzero.

Also checked the resident root note `I0_ENERGY_ELASTICITY_ROUTE_V001.md`
(SHA256 `c073678ccb471540867635f50051bb88b9be16e347aba76116cd6b039c5dbbd1`).
Its fixed-population identity p=n e'(n)-e(n), interaction correction and
conditional barotropic derivative are algebraically consistent. It explicitly
separates cell-creation work, physical deformation, source/gravity assignment
and actual-state populations. No blocker was found. These cross-checks are
internal analytical review with shared sources, not empirical validation.

### Final derivation recheck — 2026-09-27

Read the final derivation completely and verified SHA256
`c7302c7f5b22699a3f356dad3b49106655e58984e0f98774c013d3e70f64b10a`.
This supersedes the reviewed derivation identity above, whose findings remain
as history. Nonnegative demand, net-energy closure, fixed-transduction scope,
prospective-test status and review provenance are now explicit. The upfront
zero-refresh statement is correctly limited to native register occupations,
not arbitrary coherence, absence of internal dynamics or all UNT parents.
The reviewed equations are unchanged; **no remaining blocker identified**.
This is an analytical recheck only, not a numerical run, A0 freeze or empirical
validation. No edits to the derivation were made by this reviewer.
