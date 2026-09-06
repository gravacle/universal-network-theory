# Gravity verification ledger

**Status:** active, fail-closed verification ledger  
**Authority:** two-tier UV/IR verification structure, adopted 2026-09-05

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
exactly.  Continuum-style Ward decay is a separate infrared question:

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

## Gate dispositions

### Gate A–UV — SINGLE-HISTORY WITNESS CLOSED; PLAN-LEVEL GATE OPEN

The two-tier structure now has one independently audited, exact physical
ledger witness.  This closes the **single-history** Gate-A UV requirement.
The plan-level Gate A remains open because the witness is a controlled source
attachment rather than the complete global F3-MDC owner compilation.  The
following remain required for plan-level closure:

1. supply a physical law beyond bare F3 that uniquely fixes the screened
   raw-Jet-to-writer/source normalization; the adopted value alone does not
   close this plan-level requirement;
2. extend the audited bounded nonzero seam history to the stationary global
   family rather than treating one active edge as generic;
3. replace every undefined category in the compiled global owner census by
   one common physical formula and then evaluate its residual; and
4. show that no unowned term remains after state, measure, retained field,
   boundary, matching, constraint, and lawful quotient owners are included.

This is a discrete requirement.  It does not require
\(\delta_{\rm dual}(4)=0\), a smooth manifold, or a continuum gauge quotient.

### Gate B–IR — DEFINED, NOT YET LAUNCH-AUTHORIZED

The Gate-B observable and acceptance criterion are now formally fixed by
\(\widehat\delta(L)\) above.  An \(L=8\) production run remains unauthorized
until Gate A–UV has the required physical ledger; otherwise an apparent
defect decay would have no physical normalization or ownership meaning.

## Claim boundary

No statement in this ledger derives a physical Ward identity,
Einstein/Fierz--Pauli response, \(1/r\) exchange, gravity, \(C_R\), or \(G\).
