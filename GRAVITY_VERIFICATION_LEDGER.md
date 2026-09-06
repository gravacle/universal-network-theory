# Gravity verification ledger

**Status:** active, fail-closed verification ledger  
**Authority:** Gate A-R / Gate A-P split adopted by user, 2026-09-05

## Tier separation

The microscopic requirement is exact discrete ledger conservation, not a
one-cell continuum Ward identity.  For a declared finite region \(R\), the
target law is

\[
\Delta Q_R+\sum_{e\in\partial R}J_e-W_R=0.
\]

`Q` is authenticated retained lineage, `J` is an owned transported graph
current, and `W` is an explicitly owned write/read/source contribution.
On a periodic closed member, paired transported seam currents must telescope
exactly.  Continuum-style Ward decay is a separate post-accumulation infrared
question, not a microscopic record-accumulation requirement:

\[
\widehat\delta(L)=
 {\|P_{\rm bulk}{\cal R}_L\|\over Z_L|k_L|^3}
 \longrightarrow 0.
\]

The second expression is meaningful only after the same-parent family,
physical source/read map, bulk projector, response scale \(Z_L\), and error
control have been earned.

## L=4 baseline — PASS at finite selected-response scope

`RESULT_G_GL6FJ_M001_FULL_CU_C64_RESPONSE_V003/` and its independent result
audit `AUDIT_G_GL6FJ_M001_RESULT_V001/` pass.  The finite unaliased selected
response has final eigenvalue interval

\[
[3.3147386524,\;177.5395794604],
\]

with independent six-owner reconstruction residual
\(6.73\times10^{-16}\).  This is not a physical 1PI kernel, a Ward null, or
gravity.

## Raw 64-character source classification — PASS, PARTIAL

`AUDIT_G_GL6CY_RAW_SOURCE_COMPOSITION_V001/INDEPENDENT_RESULT.json` records
an independent 983-check reconstruction of the declared raw source
composition

\[
{\cal R}^{\rm raw}_{sr}=H_{,AB}\eta_{A,s}\eta_{B,r}
                         +H_{,A}\eta_{A,sr}.
\]

The nonlinear \(\eta_{sr}\) is nonzero and was explicitly included.  On the
declared path its contraction with \(H_{,A}\) vanishes by the inherited
locked/alternating structure; it was not set to zero.  The source-owned
periodic zero-mode is nevertheless nonzero:

\[
{\cal R}^{h4}_{\rm raw}(0)={32128\over27}S,
\qquad
{\cal R}^{h6,\rm diag+cyc}_{\rm raw}(0)
 ={7212448\over6075}S,
\]

where \(S_{xy,z}=-1\), \(S_{xz,y}=+1\), and all other displayed entries
vanish.

| Component | Disposition | Reason |
| --- | --- | --- |
| Source | `OWNED_PARTIAL` | The complete raw H6 source owner is reconstructed. |
| Boundary/seam | `ALGEBRAIC_TELESCOPING_PROVED__PHYSICAL_FLUX_UNPROVED` | GL6DA proves oriented cochain cancellation and retained periods, not a physical stress/current flux. |
| Lattice | `NOT_PURE_LATTICE` | The raw periodic zero mode above is nonzero. |
| Bulk | `PARTIAL_COHERENT_ZERO_MODE` | A raw source-only periodic bulk component is present; it is not a physical anomaly because the total physical owner composition is absent. |

Thus the raw source residual is neither a demonstrated probability/energy
leak nor an emergent Ward remainder.  It is an exact partial owner balance
that must be combined with state, measure, retained-field, boundary,
matching, constraint, and lawful quotient owners.

## Audited L=4 single-history UV witness — PASS, CONDITIONAL

`DEVELOPMENT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001/` and its distinct
audit `AUDIT_G_GATE_A_UV_L4_SINGLE_HISTORY_LEDGER_V001/` now provide one
fully declared finite F3 write history on

$$
G_4=(\\mathbb Z/4\\mathbb Z)^3.
$$

The source controller, fixed-content writer, and blank retained target are
co-located at one cell; the other 63 cells are blank spectators during the
declared exact terms-off write slice.  All six spatial boundary transfer
terms of the one-cell region vanish individually.  This is a conditional
F3-MDC member with an explicit source attachment, not a bare-F3 derivation of
that attachment.

The audited raw source coefficient and fixed pulse are

$$
r_0={14441248\\over6075},\\qquad
j_R(t;\\epsilon)={\\hbar r_0\\epsilon\\over\\tau}
\\mathbf 1_{[0,\\tau]}(t),\\qquad
\\epsilon_\\star={\\pi\\over4r_0},\\qquad
\\Phi_\\star={\\pi\\over4}.
$$

The hostile audit independently reconstructs the F3 blank-target unitary and
the source integral, rather than assigning the write term from the retained
charge.  It obtains

$$
\\Delta Q_R={1\\over2},\\qquad
J_{+x}=J_{-x}=J_{+y}=J_{-y}=J_{+z}=J_{-z}=0,\\qquad W_R={1\\over2},
$$

and hence the exact single-history balance

$$
\\boxed{\\Delta Q_R+\\sum_{e\\in\\partial R}J_e-W_R
={1\\over2}+0-{1\\over2}=0.}
$$

The target verifier passes `10/10`; the independent reconstruction passes
`10/10`; and audit custody/anti-circularity checks pass `24/24`.  The audit
finds no hidden boundary current or fitted cancellation **within this
declared terms-off witness**.  It explicitly retains the source attachment as
a declared, falsifiable F3-MDC member and refuses a bare-F3 or gravity
promotion.

| Component | Disposition | Reason |
| --- | --- | --- |
| Retained charge | `EXACT_UNITARY_WITNESS` | The audited blank-target F3 unitary gives `Q_R(0)=0`, `Q_R(tau)=1/2`. |
| Boundary current | `EXACT_ZERO_ON_DECLARED_TERMS_OFF_SLICE` | Each of the six physical spatial transfer terms is zero in this history. |
| Source write | `EXACT_UNITARY_WITNESS_WITH_DECLARED_ATTACHMENT` | `W_R` is the independently evaluated Heisenberg source integral. |
| Source attachment | `CONDITIONAL_F3_MDC_MEMBER__NOT_BARE_F3_DERIVED` | The raw-Jet-to-writer map is explicit and audited, but not yet uniquely derived by the complete parent. |

## Audited active multi-cell UV continuation — PASS AFTER REPAIR, BOUNDED

`DEVELOPMENT_G_GATE_A_F3_MDC_ACTIVE_SEAM_OWNER_ONCE_V001/` and its distinct
hostile audit `AUDIT_G_GATE_A_F3_MDC_ACTIVE_SEAM_OWNER_ONCE_V001/` continue
the finite ledger on two adjacent cells of `G_4`.

Bare F3 leaves the real physical-port coefficient free: unequal positive
coefficients preserve the same Hermitian, content-covariant F3 operator
algebra while producing unequal pulse areas.  Thus `alpha=r0` is not
identifiable from bare F3.  It remains an adopted F3-MDC member.

After the `Phi=pi/4` write, the native BS07--BS09 carrier Hamiltonian
transports the occupied branch across one active seam, giving

$$
\mathcal J_{a\to b}={1\over2},\qquad
(\mathcal R_a,\mathcal R_b)=(0,0),\qquad
\mathcal R_{\rm global}=0.
$$

This is a Hamiltonian-owned transfer current, not an algebraic overlap
cochain.  The repaired finite CTP generator includes branch propagators,
the initial density operator, and complete terminal effects.  The hostile
re-audit obtains equal-branch `Z=1`, reconstruction `10/10`, and custody/scope
`17/17`, with verdict `PASS_AFTER_REPAIR`.

The sixteen-category GK02 compilation is only a fail-closed census.  It
retains undefined global owners, so the stationary global action remains
`OWNER_INCOMPLETE` and physical descent and Ward residuals remain
`UNDEFINED`.

## Audited stationary G4 carrier sector — PASS, SECTOR-QUALIFIED

`DEVELOPMENT_G_GATE_A_G4_STATIONARY_CARRIER_SEAM_SECTOR_V001/` and
`AUDIT_G_GATE_A_G4_STATIONARY_CARRIER_SEAM_SECTOR_V001/` extend the active
edge to all native carrier supports of the inherited periodic `G_4` family.
The canonical positive-generator orientation has 64 cells and 192 distinct
undirected supports, each owned once.  The exact incidence equation gives
regional continuity, `16+16` paired supports across a transverse slab, and
global periodic telescoping.  The audited current-`1/2` history embeds as a
nonstationary solution of the same operator equation.

A finite Gibbs member and the complete product-qutrit terminal instrument
give a normalized stationary CTP generator for the carrier sector.  The
independent reconstruction passes `81/81` and custody/scope passes `21/21`,
with disposition `PASS_SECTOR_QUALIFIED`.

The qualifier is mandatory: connector, seam/period, state, and measure are
explicit only for the native carrier sector.  They are not completed global
GK02 rows.  Physical state selection and all non-carrier owners remain open;
the global action is still `OWNER_INCOMPLETE` and descent/Ward residuals are
still `UNDEFINED`.

## Gate dispositions

### Gate A-R — RECORD OWNERSHIP AND CONSERVATION: CLOSED

Gate A-R is the prerequisite for microscopic accumulation. It is closed by
the following exact record-level evidence:

1. the independently audited single-history ledger
   `1/2 + 0 - 1/2 = 0`;
2. the independently audited active physical seam current `1/2`, with exact
   zero endpoint and global residuals;
3. the sector-qualified `G_4` owner-once incidence theorem with 192 distinct
   carrier supports and exact regional/periodic telescoping; and
4. the same-parent join screen `28/28`, which distinguishes missing optional
   macro-parent bindings from debts in the explicitly selected record parent.

The raw-source normalization remains an adopted F3-MDC attachment, not a
bare-F3 derivation. That status rides every dependent result. Gate A-R closure
does not promote a generic interacting state or complete macro parent.

### Gate B-R — MICROSCOPIC RECORD ACCUMULATION: AUTHORIZED

The baseline `L=8` record-accumulation workflow is authorized. Its observables
are retained-lineage count and distribution, owned current throughput, and
the cellwise/global discrete carrier-ledger residual under a common declared
normalization. No continuum exponent, correlation length, Ward score, or
gravity-shaped behavior is presumed.

A nonzero residual at a later interacting accumulation state is not called a
defect before classification. It may be a necessary source, boundary,
collective, or newly active owner. It is an accounting failure only if it
remains unowned after the complete selected-parent census.

#### L=8 baseline — PASS at prepared accumulation scope

`DEVELOPMENT_R_GATE_B_L8_DENSITY_CONTROLLED_ACCUMULATION_V001/` and its
distinct hostile audit
`AUDIT_R_GATE_B_L8_DENSITY_CONTROLLED_ACCUMULATION_V001/` pass after repair.
The exact raw trajectory is:

| record quantity | L=4 | L=8 |
|---|---:|---:|
| cells | 64 | 512 |
| source lineages | 32 | 256 |
| expected retained total | 16 | 128 |
| retained density | 1/4 | 1/4 |
| absolute oriented seam throughput | 16 | 128 |
| net periodic boundary flux | 0 | 0 |
| carrier residual `r_1` | 0 | 0 |
| carrier residual `r_infinity` | 0 | 0 |
| prepared variance | 8 | 64 |

The retained total and lineage count rise by exactly eight under the
eightfold cell-count increase. The zero residual is a result of this prepared
factorized history, not an assumption about later interacting accumulation.
A future nonzero residual remains unclassified until its necessary owner or
collective origin is tested.

On the 48 GiB environment, the exact combinatorial verifier ran in `0.07 s`
wall (`0.02 s` user, `0.01 s` system), with maximum RSS `11,075,584` bytes
(`10.5625 MiB`), peak memory footprint `7,110,968` bytes (`6.7815 MiB`), and
zero swaps. This is not a dense `3^512` state evolution. Target verification
passes `28/28`; independent reconstruction passes `28/28`; audit custody and
scope pass `31/31` before final result-status sealing.

This closes only the first prepared Gate B-R baseline. Generic interacting
accumulation and retention stress remain Gate R-C work.

### Gate R-C — FIRST INTERACTION/RETENTION STRESS: PASS, CONDITIONAL

`DEVELOPMENT_R_GATE_C_L8_INTERACTION_RETENTION_STRESS_V001/` and
`AUDIT_R_GATE_C_L8_INTERACTION_RETENTION_STRESS_V001/` pass at conditional
prepared-interaction scope. On 128 disjoint native two-record blocks, the raw
pair distribution changes from `(1/4,1/4,1/4,1/4)` to
`(1/4,1/2,0,1/4)`, with positional TV `1/4` per block. Expected local
occupations redistribute from `(1/2,1/2)` to `(1/4,3/4)`.

Total retained occupation remains `128`, retention fraction is `1`, absolute
oriented interaction throughput is `32`, and all cell residuals remain zero.
This is interaction-driven redistribution, not loss. Individual source-lineage
motion, criticality, generic interacting accumulation, and continuum behavior
are not claimed. Target verification passes `18/18`, independent
reconstruction `17/17`, and audit custody/scope `22/22` before final
result-status sealing.

### Gate R-D — REPEATED-SCALE INTERACTION TRAJECTORY: PASS, PREPARED SCOPE

`DEVELOPMENT_R_GATE_D_REPEATED_SCALE_INTERACTION_TRAJECTORY_V001/` and
`AUDIT_R_GATE_D_REPEATED_SCALE_INTERACTION_TRAJECTORY_V001/` pass. The exact
`L=4 -> L=8` rows are `(cells,blocks,retained,throughput,low,high) =
(64,16,16,4,4,12) -> (512,128,128,32,32,96)`, with record-ledger residuals
zero at both sizes. Every nonzero raw quantity has ratio eight.

The hostile audit accepts eight only as exact fixed-density disjoint-block
volume replication. It is not a continuum, critical, or generic accumulation
exponent. Target verification passes `25/25`, independent reconstruction
`40/40`, and custody/scope `24/24` before final result-status sealing.

The next calculation removes the disjoint-block restriction through connected
carrier-transfer rings.

> **Authoritative physical-parent reclassification.** The hostile audit of
> `DEVELOPMENT_R_PHYSICAL_PARENT_AUTONOMOUS_RING_SELECTION_V001/` found that
> literal BS09 has a uniform onsite term and a simultaneous hopping sum. The
> node-dependent stagger and finite transfer-gate orders used in the connected
> packets below are absent from autonomous BS09. Their numerical results and
> owner-once controller ledgers remain valid, but they are conditional
> programmed-control records, not physical-parent-selected autonomous
> histories. This paragraph supersedes any broader wording retained inside
> their immutable, hash-audited packets.

### Connected L8 carrier-ring stress — PASS, CONDITIONAL PROGRAMMED CONTROL

`DEVELOPMENT_R_CONNECTED_L8_RING_STRESS_V001/` and
`AUDIT_R_CONNECTED_L8_RING_STRESS_V001/` pass at prepared numerical scope.
Thirty-two connected eight-site rings cover all 256 retained L8 heads. Each
site participates in two native transfer terms. The run produces alternating
occupations approximately `0.3125888646/0.6874111354`, alternating integrated
currents `+/-0.0937055677`, and nonzero nearest-neighbor connected occupation
correlation `-0.0261331605`.

Its node-dependent stagger is a supplied control term, not the uniform BS09
onsite term. The simultaneous numerical Hamiltonian is therefore a
conditional programmed Hamiltonian, not autonomous BS09 selection.

Expected retained total remains `128` within `3e-14`; absolute oriented
throughput is `23.988625329874075`; signed ring-current sum is
`7.11e-15`. The ring residual is `r_1=1.59e-15`,
`r_infinity=3.47e-16`, below preregistered tolerances and beside norm, energy,
and number-law controls. These floating-point values are classified as
controlled numerical evidence, not exact equalities or physical defects.

The warning-free target passes `10/10`, independent reconstruction `24/24`,
and custody/result/scope `29/29` before final status sealing. Generic
retention, individual lineage motion, criticality, continuum behavior, Ward
structure, and gravity remain unclaimed.

### Connected-ring time/coupling scan — PASS, CONDITIONAL PROGRAMMED CONTROL

`DEVELOPMENT_R_CONNECTED_RING_PARAMETER_SCAN_V001/` and
`AUDIT_R_CONNECTED_RING_PARAMETER_SCAN_V001/` pass without repair. The 12
points combine `delta=(0,1/2,1,2)` with three declared pulse times. Across
the scan, staggered occupation amplitude reaches `0.5688670625126272`,
absolute owned throughput reaches `1.1377341250252546` per ring, and absolute
nearest-neighbor connected correlation reaches `0.06132656332408998`.

The raw record-ledger residual envelope is `r_1=2.56e-15` and
`r_infinity=5.56e-16` per ring. Retained-total, norm, energy, and number-law
controls are all at or below `2.67e-15`. These residuals remain unassigned
pending owner classification: they are neither promoted to exact zero nor
called physical defects. The `delta=0` control retains half occupation and
near-zero oriented throughput while still forming correlations, separating
those record observables.

The warning-as-error target passes `13/13`; independent reconstruction passes
`108/108`; custody, all point-field comparisons, and scope pass `189/189`.
The scan is non-monotone and no fit is promoted. It establishes neither a
generic retention law nor criticality, continuum behavior, Ward structure,
mature macro dynamics, or gravity. The next bounded accumulation stress may
connect the separate eight-site rings while preserving gate-level owner
custody.

Only the `delta=0` members omit the nonuniform onsite control. The remaining
points are programmed-control records; the scan supplies no BS09 selection
law.

### Connected L8 paired-ring circuit — PASS, CONDITIONAL PROGRAMMED CONTROL

`DEVELOPMENT_R_CONNECTED_L8_LADDER_CIRCUIT_V001/` and its hostile audit
`AUDIT_R_CONNECTED_L8_LADDER_CIRCUIT_V001/` pass without repair. Sixteen
connected 16-record clusters partition all 256 retained L8 heads. Each
cluster uses two inherited native-generator cycles and their eight inherited
third-generator supports; the finite tuple labels are enumeration, not a
physical grid.

All 24 supports carry nonzero cumulative current after the reversed-stagger
prepared circuit. Absolute gate-owned throughput is `2.6742223590371705` per
cluster, maximum absolute connected edge correlation is
`0.06592583672451707`, and expected L8 retained total remains `128` within
`1.5e-14`. The raw per-cluster residual is `r_1=1.66e-14` and
`r_infinity=2.95e-15`, beside norm and number-law controls below `4.5e-16`.
It remains unassigned pending owner classification and is not called a
physical defect or promoted to exact zero.

The warning-free target passes `12/12`; the independent full 65,536-state
reconstruction passes `18/18`; custody/result/scope passes `36/36`. The
explicit ordered circuit is a declared finite programmed-controller history,
not autonomous BS09 evolution. No individual post-mixing lineage,
generic retention law, criticality, continuum, Ward structure, mature macro
dynamics, or gravity is established.

### Connected L8 circuit-depth trajectory — PASS, CONDITIONAL PROGRAMMED CONTROL

`DEVELOPMENT_R_CONNECTED_L8_CIRCUIT_DEPTH_TRAJECTORY_V001/` and
`AUDIT_R_CONNECTED_L8_CIRCUIT_DEPTH_TRAJECTORY_V001/` pass after a documented
pre-audit tolerance repair. The programmed 16-record circuit is repeated from
depth zero through eight. Every positive-depth checkpoint has all 24
cumulative supports active, including all eight inter-cycle supports, and the
eight-depth census contains 192 owner-once gate events.

At depth eight, absolute gate-event traffic is `5.387857637651692` per
cluster, cumulative net edge throughput is `5.102760095563551`, and
cumulative net inter-cycle throughput is `2.0433764227644584`. Keeping event
traffic separate from net support current retains transport reversals.
Connected correlation is non-monotone and peaks in absolute value at
`0.06592583672451707` at depth three.

Expected L8 retained total remains `128` within `7.11e-13`. The raw
per-cluster residual envelope is `r_1=4.53e-14` and
`r_infinity=4.95e-15`; norm and record-number-law controls remain below
`4.67e-15` and `6.39e-16`. The initial `5e-13` L8 drift bound failed and was
repaired before audit to `1e-12`; the independent audit reproduces both the
failure and passing replacement. This is numerical-tolerance provenance, not
a physical term.

The target passes warning-free `12/12`, independent reconstruction `16/16`,
and full custody/result/scope verification `47/47`. Raw residuals remain
unassigned pending owner classification, not physical defects. Circuit depth
is not continuum time, and no scaling fit, criticality, Ward structure,
mature macro dynamics, or gravity is claimed.

### Connected L8 owner-once order screen — PASS, CONDITIONAL PROGRAMMED CONTROL

`DEVELOPMENT_R_CONNECTED_L8_CIRCUIT_ORDER_SCREEN_V001/` and
`AUDIT_R_CONNECTED_L8_CIRCUIT_ORDER_SCREEN_V001/` pass without repair. At
fixed preparation and depth three, forward, exact-reverse, and interleaved
schedules each use the same 24 unique native supports exactly once per depth.
All 24 cumulative currents, including all eight inter-cycle currents, remain
active in every schedule, and every schedule closes the finite record ledger
within the declared numerical controls.

Nevertheless, schedule changes materially alter the accumulated terminal
record. Pairwise full-distribution total variation reaches
`0.36653420105732926`, minimum state fidelity is `0.5157506266148363`, and
maximum occupation L1 distance is `0.49438317494441975`. Expected L8 retained
total remains `128` within `2.14e-13`; the raw residual envelope is
`r_1=2.30e-14`, `r_infinity=3.78e-15` per cluster, with norm and number-law
controls below `1.12e-15` and `2.50e-16`.

The target passes warning-free `14/14`, independent reconstruction `12/12`,
and custody/result/scope verification `34/34` across 216 gate events. The
proved numerical conclusion is limited: distinct finite controller schedules
on the same supports produce distinct programmed records. This is not an
ambiguity of the autonomous BS09 parent, whose fixed Hamiltonian selects its
chronological exponential. No preferred programmed order, schedule measure,
averaging rule, or autonomous selection law is derived by this screen.

The raw residuals remain unassigned, not physical defects. No physical grid,
generic retention law, criticality, continuum behavior, Ward structure,
mature macro dynamics, or gravity is promoted.

### Connected L8 onsite-program screen — PASS, CONDITIONAL PROGRAMMED CONTROL

`DEVELOPMENT_R_CONNECTED_L8_PREPARATION_PATTERN_SCREEN_V001/` and
`AUDIT_R_CONNECTED_L8_PREPARATION_PATTERN_SCREEN_V001/` pass without repair.
The support, forward schedule, depth three, source attachment, and complete
read are held fixed while four node-dependent onsite controller labels are
screened. These are not alternative source preparations and are absent from
literal uniform-onsite BS09.

The equal-pattern control has all 16 internal cycle supports active but zero
of eight inter-cycle supports active; its net inter-cycle throughput is
`7.22e-16`. Reversed and both one-cycle-only preparations activate all 24
supports and all eight inter-cycle supports. Their inter-cycle throughputs
are respectively `0.9477610039941`, `0.4179092011731279`, and
`0.4179092011731274` per cluster. The two one-cycle-only results agree after
the exact cycle-label swap with terminal-distribution TV `3.01e-16`.

Across all patterns, full-distribution TV reaches `0.6574390434811216`,
minimum state fidelity is `0.0937061883806159`, and maximum occupation L1
distance is `2.959881706601889`. Expected L8 retained total stays `128`
within `2.28e-13`; the raw residual envelope is `r_1=2.64e-14`,
`r_infinity=3.61e-15` per cluster, beside norm and number-law controls below
`2.11e-15` and `2.78e-16`.

The target passes warning-free `16/16`, independent reconstruction `14/14`,
and custody/result/scope verification `41/41` across 288 gate events. The
audited conclusion is local: onsite-program asymmetry is necessary for active
inter-cycle transport in this fixed symmetric programmed circuit. No
universal preparation theorem, preferred onsite program, measure, or
averaging rule is derived. Patterns remain raw controller-history labels;
residuals remain
unassigned rather than physical defects. No grid, criticality, continuum,
Ward structure, mature macro dynamics, or gravity is promoted.

### Connected L4-L6-L8 programmed trajectory — PASS, CONDITIONAL CONTROL

`DEVELOPMENT_R_CONNECTED_L4_L6_L8_TRAJECTORY_V001/` and
`AUDIT_R_CONNECTED_L4_L6_L8_TRAJECTORY_V001/` pass without repair. The prior
hostile-audited L4/L8 result is hash-pinned and an L6 row is independently
inserted under the same reversed onsite program, forward controller schedule,
and depth-three labels. At L6, nine 12-record components partition 108 heads; all 18
native supports per component, including all six inter-cycle supports, are
active across 54 owner-once events.

Per retained head, gate-event traffic is
`0.1873029450 -> 0.1819357914 -> 0.1831009165`; net edge throughput is
`0.1621539198 -> 0.1658328077 -> 0.1671388974`; and net inter-cycle
throughput is `0.0608123878 -> 0.0585992499 -> 0.0592350627`. Thus event and
inter-cycle traffic fall then rise, while net edge throughput rises in these
three records. No smooth trend is imposed.

Expected retained totals are `16 -> 54 -> 128` within numerical closure. The
new L6 raw residual is `r_1=6.00e-15`, `r_infinity=1.17e-15` per component;
its tiled L1 bound is `5.40e-14`, with norm and number-law errors below
`1.23e-15` and `2.23e-16`. The target passes warning-free `15/15`, independent
L6 reconstruction `6/6`, and custody/result/scope verification `17/17`.

This is a three-size programmed-control record trajectory, not an autonomous
BS09 trajectory and not an interpolation formula,
exponent, convergence claim, generic law, or critical signal. Schedule and
onsite program remain explicit controller labels, residuals remain unassigned rather than
physical defects, and no grid, continuum, Ward structure, mature macro
dynamics, or gravity is promoted.

### Connected L4-to-L8 programmed trajectory — PASS, CONDITIONAL CONTROL

`DEVELOPMENT_R_CONNECTED_L4_L8_NATIVE_COMPONENT_TRAJECTORY_V001/` and
`AUDIT_R_CONNECTED_L4_L8_NATIVE_COMPONENT_TRAJECTORY_V001/` pass without
repair. The same reversed onsite program, forward controller schedule, and
depth-three labeled recipe is applied to connected components at L4 and L8. Four
eight-record L4 components partition 32 heads; sixteen 16-record L8
components partition 256 heads. Every native support is active: 12 per L4
component and 24 per L8 component, including all four and eight inter-cycle
supports respectively.

Expected retained total changes `16 -> 128`, ratio eight. The raw total
gate-event, net edge, and net inter-cycle throughput ratios are instead
`7.8205248293612035`, `8.245938064939383`, and `7.792499510125264`.
Per retained head the corresponding ratios are `0.9775656036701504`,
`1.0307422581174228`, and `0.974062438765658`. They are recorded without
forcing factor eight or fitting an exponent or limit.

The per-component raw ledger residuals remain below
`3.72e-15/8.33e-16` L1/Linf at L4 and `1.66e-14/2.95e-15` at L8; tiled L1
bounds are `1.49e-14` and `2.65e-13`. The target passes warning-free `14/14`,
independent reconstruction `11/11`, and custody/result/scope verification
`15/15`. The L8 row independently matches the earlier audited circuit.

This is a controlled two-size programmed record trajectory, not autonomous
BS09 evolution or a generic scaling law. Schedule and onsite program remain
explicit controller labels, residuals are
unassigned rather than physical defects, and no grid, criticality, continuum,
Ward structure, mature macro dynamics, or gravity is promoted.

### Physical-parent autonomous ring selection — PASS AFTER RECLASSIFICATION

`DEVELOPMENT_R_PHYSICAL_PARENT_AUTONOMOUS_RING_SELECTION_V001/` and
`AUDIT_R_PHYSICAL_PARENT_AUTONOMOUS_RING_SELECTION_V001/` derive the first
post-decision physical-parent trajectory. The adopted F3-MDC write at
`Phi=pi/4` followed by native transfer at `theta=pi/2` cancels the pulse
phases and selects a blank tail with `(B+x)/sqrt(2)` on each retained head.
After source shutdown, fixed literal BS09 selects
`U=exp(-i H_car tau/hbar)` (or the chronological exponential for declared
time-dependent coefficients), not a finite gate order. The uniform onsite
term commutes with the hopping generator and all recorded number-conserving
observables; no node-dependent stagger is used.

On conditional fixed-program first-generator cycles, all `4/4` L4 and `8/8`
L8 supports carry nonzero alternating integrated currents. Expected retained
totals remain `16` and `128`. Absolute throughput totals are
`5.065021368165664` and `31.481053477075946`, giving raw ratio
`6.215384139332278` and per-retained-record ratio `0.7769230174165348`.
The per-cycle raw residuals are below `1.84e-15` L1 and `4.31e-16` Linf;
norm, energy, number-law, preparation-vector, and uniform-onsite commutator
controls pass.

The target passes warning-free `16/16`, independent reconstruction `8/8`,
and hostile verification `18/18`. Its final audit verdict is
`PASS__PROMOTION_CONDITION_SATISFIED`; the required reclassification is the
authoritative correction above and in `CURRENT_CONTINUATION.md` and the
governing accumulation plan.

This selects preparation and chronological evolution only conditionally on
the adopted source attachment and declared physical Hamiltonian. The fixed
support program, `t`, `tau`, content sector, and read remain conditional.
Autonomous support/program selection, coefficient derivation, and generic
phase selection remain open. Residuals remain unassigned, not defects. No
grid, continuum, Ward structure, mature macro dynamics, or gravity is
promoted.

### Physical-parent support-selection screen — PASS, EXACT NON-SELECTION

`DEVELOPMENT_R_PHYSICAL_PARENT_SUPPORT_SELECTION_SCREEN_V001/` and
`AUDIT_R_PHYSICAL_PARENT_SUPPORT_SELECTION_SCREEN_V001/` screen the supplied
cycle incidence word against the unchanged BS06/BS09/BS10/BS11 and FPSS
parent. Under the exact even/odd bipartite realization, L4 has `32+32` sites,
`1024` possible F3 links, and a selected degree-two cover of `64` links in 16
four-cycles. L8 has `256+256` sites, `65536` possible links, and a selected
degree-two cover of `512` links in 64 eight-cycles.

At zero raw incidence flip, `U_d>0` and `0<Delta<2U_d` make degree two the
unique per-vertex classical minimum. They do not choose a labeled cover: an
explicit right-layer exchange gives a distinct cover with identical degrees
and BS06 diagonal energy (`64` at L4 and `512` at L8 for
`Delta=U_d=1`). With the raw flip active, the finite incidence-only BS06
ground state is unique, strictly positive on every word, and permutation
invariant, not an exact cycle word. An exact `K_(3,3)` diagonalization
corroborates this boundary with six classical ground words and positive
transverse gap `0.06056937459032419`.

BS09, BS10, and BS11 commute with every incidence occupation and cannot
prepare the word. FPSS prepares and passively retains it only from a supplied
orthogonal address/edge/source/controller/port program. The declared uniform
right-source/blank-left carrier preparation does not break the explicit
competitor symmetry; any label-distinguishing lineage or port map is itself
additional conditional selector data requiring complete ownership.

The target passes warning-free `29/29`; independent reconstruction passes
`18/18`; hostile verification passes `14/14` with no repair required. The
proved result is non-selection by the unchanged parent, not failure of the
conditional microscopic accumulation records and not a reopening of Gate
A-R. Autonomous label-anchored support selection remains open; coefficient
and clock selection remain conditional. No grid, graph reward, defect,
continuum, Ward structure, mature macro dynamics, or gravity is promoted.

### Autonomous BS09 `kappa` trajectory — PASS, CONDITIONAL ACCUMULATION MAP

`DEVELOPMENT_R_AUTONOMOUS_KAPPA_TRAJECTORY_V001/` and
`AUDIT_R_AUTONOMOUS_KAPPA_TRAJECTORY_V001/` map the source-prepared
simultaneous BS09 evolution at L4, L6, and L8 for ten declared values of
`kappa=t tau/hbar` from zero through `2pi`. The uniform onsite term commutes
with hopping and the recorded number-conserving observables, so these declared
observables depend on `t` and `tau` only through `kappa`. This identity does
not select either coefficient or the clock.

The 30 rows retain respectively `32/108/256` source lineages and expected
totals `16/54/128`. The zero-`kappa` control has zero integrated current. At
every positive sampled `kappa`, raw absolute throughput is nonzero, and the
`pi/2` L4/L8 rows reproduce the earlier audited physical-parent baseline
exactly in the target computation. Raw L8/L4 per-retained throughput ratios
vary from near one at early `kappa` to `0.776923` at `pi/2`, `1.356300` at
`3pi/4`, and `3.379229` at `3pi/2`; this nonmonotone finite recurrence is not
fit to a scaling law.

The target passes warning-free `15/15`, independent reconstruction `9/9`,
and hostile verification `52/52`. Every occupation and integrated-current
vector was independently compared, including the continuity sign
`q(kappa)-q(0)+J_out-J_in=0`. Target per-cycle raw residual maxima are
`2.554e-15` L1 and `8.188e-16` Linf; independent floating-order maxima are
`2.943e-15` and `8.744e-16`, within the declared controls.

The support program, sampled `kappa`, separate `t` and `tau`, content sector,
clock/source calibration, and complete read remain conditional. Residuals are
unassigned record-ledger terms, not defects. No finite gate order, node
stagger, coefficient selection, physical grid, continuum, Ward structure,
critical law, mature macro dynamics, or gravity is promoted.

### Autonomous BS09 L10 accumulation — PASS AFTER CUSTODY REPAIR

`DEVELOPMENT_R_AUTONOMOUS_L10_ACCUMULATION_V001/` and
`AUDIT_R_AUTONOMOUS_L10_ACCUMULATION_V001/` extend the same conditional
support and ten-point `kappa` scan to 1,000 sites. The exact census is 500
sites per F3 layer, 250,000 possible links, 100 disjoint ten-site cycles,
1,000 selected cycle edges, 500 source lineages, and expected retained total
250. Exact factorization uses one 1,024-dimensional cycle calculation rather
than a fictitious global `2^1000` state.

Translation by two makes `Delta q` alternate; reflection preserves the
prepared history while reversing oriented current and removes uniform
circulation. The owner-once continuity equation therefore fixes
`J_i=-Delta q_i/2`. This reduction agrees with every directly integrated
current in the 30 hostile-audited L4/L6/L8 rows within `5.829e-16` in the
target and `6.107e-16` independently. All ten L10 supports are active at
every positive sampled `kappa`; expected retained total stays 250.

Raw L10 throughput totals include `61.480350` at `pi/2`, `174.997337` at
`3pi/4`, and `96.311751` at `3pi/2`. The corresponding L10/L8 per-retained
ratios are `0.999901`, `0.996452`, and `1.647847`. These are finite recurrence
records, not a fit. Target per-cycle residual maxima are `1.763e-15` L1 and
`3.470e-16` Linf; the independent maxima are `2.499e-15` and `5.829e-16`.
The exact zero-`kappa` current is zero; displayed sub-threshold values are raw
eigensolver roundoff, not physical current or a defect.

The frozen 48 GiB run observation is `0.4769145 s` and `80.53125 MiB` maximum
RSS. These are one-run environment observations, not universal complexity
claims. The target passes warning-free `18/18`, independent reconstruction
`6/6`, and hostile verification `34/34`. The audit first caught that degenerate
eigenspaces prevent byte-identical raw floats; after repair, one raw canonical
result is frozen and every field is recomputed with exact structural and
`8e-12` floating agreement. Two consecutive replays preserve its hash.

Support, sampled `kappa`, separate `t` and `tau`, clock, content, source
routing, and complete read remain conditional. Connected-cycle accumulation
under a physical parent and generic phase behavior remain open. No physical
grid, continuum, Ward structure, critical law, mature macro dynamics, or
gravity is promoted.

### Autonomous connected-cycle accumulation — PASS, CONDITIONAL SUPPORT

`DEVELOPMENT_R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001/` and
`AUDIT_R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001/` replace the disjoint
L4 cycle support with eight identical connected eight-site components. Each
component contains two four-cycles and four opposite-parity connector/seam
edges, is degree three and BFS-connected, and owns eight internal plus four
connector edges once. Globally the declared support covers 64 sites in
`32+32` F3 layers with 96 unique active edges and 32 source lineages.

The input remains the uniform audited F3-MDC preparation: every even tail is
blank and every odd head is `(B+x)/sqrt(2)`. No component receives a different
source rule. One simultaneous BS09 exponential at conditional `kappa=pi/2`
activates all `8/8` internal and `4/4` connector supports per component. Each
integrated current has magnitude `0.0828962696834657`. Raw absolute throughput
is `0.9947552362015891` per component and `7.958041889612713` globally; the
connector/seam contribution is `0.3315850787338629` per component and
`2.652680629870903` globally. Expected retained total remains 16, and total
throughput is `1.5711763704749737` times the disjoint L4 baseline.

The finite owner-once CTP bookkeeping functional assigns one deformation
source to each of the 96 unique Hamiltonian edges and obeys
`Z[0,0]=Tr(rho)=1`. It is not a 1PI action or Ward identity. Direct integration
of all twelve component currents closes
`Delta q+B J=0`; raw per-component residual maxima are `2.110e-15` L1 and
`6.662e-16` Linf. The target passes two canonical warning-free `18/18`
replays, independent reconstruction `10/10`, and hostile verification
`13/13`.

This proves a finite connected-support accumulation witness, not autonomous
selection of that support or a generic connected phase. Support,
`kappa`, separate `t` and `tau`, clock, content, source routing, and complete
read remain conditional. Residuals remain unassigned rather than defects. No
grid, continuum, Ward structure, critical law, mature macro dynamics,
graviton, or gravity is promoted.

### Autonomous connected L6 accumulation — PASS, CONDITIONAL SUPPORT

`DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION_V001/` and
`AUDIT_R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION_V001/` extend the same uniform
F3-MDC preparation and simultaneous BS09 Hamiltonian from the connected L4
witness to L6. Eighteen identical twelve-site components cover all 216 sites
in `108+108` F3 layers. Each component consists of two six-cycles and six
opposite-parity connector/seam edges, is degree three and BFS-connected, and
owns 12 internal plus 6 connector edges once. The global census is 11,664
possible F3 links, 324 selected edges, 108 source lineages, and expected
retained total 54.

At conditional `kappa=pi/2`, one simultaneous BS09 exponential activates all
`12/12` internal and `6/6` connector supports per component. Refined current
magnitudes are `0.0882107462` internally and `0.0836430325` on connectors.
Raw absolute throughput is `1.5603871492` per component and
`28.0869686859` globally; connector/seam throughput is `0.5018581948` per
component and `9.0334475069` globally. Expected retained total is 54. The
finite L6/L4 total-throughput ratio is `3.5293818600`, and its per-retained
ratio is `1.0457427733`; neither is a fitted scaling law.

The 4,096-state component calculation is matrix-free. Its order-10 Taylor
evolution and Simpson current integral were refined from 1,024 to 2,048
panels. The current refinement is `1.973e-12`; fine raw residuals are
`4.740e-12` L1 and `4.073e-13` Linf per component, with global tiled L1 bound
`8.532e-11`. These are unassigned numerical record-ledger residuals, not
defects. One refinement pair is a convergence diagnostic, not exact
quadrature. A distinct hostile matrix-free RK4(4096)+Simpson reconstruction
agrees with all occupations and signed currents, retention, correlations,
conserved quantities, residuals, and ratios. The target passes `20/20`; the
hostile audit passes `32/32` and requires no correction.

The finite owner-once CTP assigns one deformation source to each of the 324
unique Hamiltonian edges and has `Z[0,0]=1`; it is not a 1PI action or Ward
identity. This is a second finite connected-support accumulation record, not
autonomous selection of that support or a generic connected phase. Support,
`kappa`, separate `t` and `tau`, clock, content, source routing, and complete
read remain conditional. No grid, continuum, Ward structure, critical law,
mature macro dynamics, graviton, or gravity is promoted.

### Autonomous connected L8 accumulation — PASS, CONDITIONAL SUPPORT

`DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001/` and
`AUDIT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001/` extend the same uniform
F3-MDC preparation and simultaneous BS09 Hamiltonian to L8. Thirty-two
identical sixteen-site components cover all 512 sites in `256+256` F3 layers.
Each component contains two eight-cycles and eight opposite-parity
connector/seam edges, is degree three and BFS-connected, and owns 16 internal
plus 8 connector edges once. The global census is 65,536 possible F3 links,
768 selected edges, 256 source lineages, and expected retained total 128.

At conditional `kappa=pi/2`, all `16/16` internal and `8/8` connector supports
per component are active. Refined current magnitudes are `0.0882983706`
internally and `0.0841011442` on connectors. Raw absolute throughput is
`2.0855830833` per component and `66.7386586644` globally; connector/seam
throughput is `0.6728091539` per component and `21.5298929261` globally.
Expected retained total is 128. Finite total/per-retained ratios are
`8.3863165827/1.0482895728` against L4 and
`2.3761431648/1.0024353977` against L6. They are comparator records, not a
fitted scaling law.

The 65,536-state component calculation is matrix-free. Order-10 Taylor
evolution and Simpson current integration refined from 1,024 to 2,048 panels
give current difference `1.976e-12`. Fine raw residuals are `6.321e-12` L1
and `4.034e-13` Linf per component, with global tiled L1 bound `2.023e-10`.
These remain unassigned numerical record-ledger residuals, not defects; one
refinement pair is not exact quadrature. A distinct hostile matrix-free
RK4(4096)+Simpson reconstruction agrees with all occupations and signed
currents, retention, correlation, conservation, residuals, and size ratios.
The target passes `21/21`; hostile verification passes `35/35` and requires
no correction.

One passing 1,024/2,048 run on the declared 48 GiB host took
`55.522473084 s` and used `73,613,312` bytes (`70.203125 MiB`) maximum RSS.
These are one-run host observations, not complexity claims. The documented
pre-result Python 3.9 compatibility failure is author-recorded custody rather
than independently reproduced evidence; it generated no result and supports
no physics claim.

The finite owner-once CTP assigns one deformation source to each of the 768
unique Hamiltonian edges and has `Z[0,0]=1`; it is not a 1PI action or Ward
identity. This is a third finite connected-support accumulation record, not
autonomous selection of that support or a generic connected phase. Support,
`kappa`, separate `t` and `tau`, clock, content, source routing, and complete
read remain conditional. No grid, continuum, Ward structure, critical law,
mature macro dynamics, graviton, or gravity is promoted.

### Gate A-P — CONTINUUM/MACROSCOPIC RESPONSE: POST-ACCUMULATION, OPEN

The former plan-level global physical Hessian, support/recoil/Maxwell shell,
lawful 1PI/Schur quotient, `delta_dual`, and continuum Ward diagnostics now
belong to Gate A-P and the later M-series. They remain `OWNER_INCOMPLETE` or
`UNDEFINED`. They do not block Gate B-R microscopic accumulation.

## Claim boundary

No statement in this ledger derives a physical Ward identity,
Einstein/Fierz--Pauli response, \(1/r\) exchange, gravity, \(C_R\), or \(G\).
