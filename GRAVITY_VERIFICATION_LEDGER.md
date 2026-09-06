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
native carrier rings.

### Connected L8 carrier-ring stress — PASS, CONTROLLED NUMERICAL

`DEVELOPMENT_R_CONNECTED_L8_RING_STRESS_V001/` and
`AUDIT_R_CONNECTED_L8_RING_STRESS_V001/` pass at prepared numerical scope.
Thirty-two connected eight-site rings cover all 256 retained L8 heads. Each
site participates in two native transfer terms. The run produces alternating
occupations approximately `0.3125888646/0.6874111354`, alternating integrated
currents `+/-0.0937055677`, and nonzero nearest-neighbor connected occupation
correlation `-0.0261331605`.

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

### Connected-ring time/coupling scan — PASS, CONTROLLED NUMERICAL

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

### Connected L8 paired-ring circuit — PASS, CONTROLLED NUMERICAL

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
explicit ordered circuit is the selected finite parent and is not claimed to
equal a simultaneous continuum evolution. No individual post-mixing lineage,
generic retention law, criticality, continuum, Ward structure, mature macro
dynamics, or gravity is established.

### Connected L8 circuit-depth trajectory — PASS, CONTROLLED NUMERICAL

`DEVELOPMENT_R_CONNECTED_L8_CIRCUIT_DEPTH_TRAJECTORY_V001/` and
`AUDIT_R_CONNECTED_L8_CIRCUIT_DEPTH_TRAJECTORY_V001/` pass after a documented
pre-audit tolerance repair. The selected 16-record circuit is repeated from
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

### Connected L8 owner-once order screen — PASS, CONTROLLED NUMERICAL

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
proved numerical conclusion is limited: owner-once support and conservation
do not select one accumulated distribution for noncommuting circuit events.
Schedule must remain explicit selected-parent record data. No preferred
order, schedule measure, averaging rule, or selection law is derived.

The raw residuals remain unassigned, not physical defects. No physical grid,
generic retention law, criticality, continuum behavior, Ward structure,
mature macro dynamics, or gravity is promoted.

### Gate A-P — CONTINUUM/MACROSCOPIC RESPONSE: POST-ACCUMULATION, OPEN

The former plan-level global physical Hessian, support/recoil/Maxwell shell,
lawful 1PI/Schur quotient, `delta_dual`, and continuum Ward diagnostics now
belong to Gate A-P and the later M-series. They remain `OWNER_INCOMPLETE` or
`UNDEFINED`. They do not block Gate B-R microscopic accumulation.

## Claim boundary

No statement in this ledger derives a physical Ward identity,
Einstein/Fierz--Pauli response, \(1/r\) exchange, gravity, \(C_R\), or \(G\).
