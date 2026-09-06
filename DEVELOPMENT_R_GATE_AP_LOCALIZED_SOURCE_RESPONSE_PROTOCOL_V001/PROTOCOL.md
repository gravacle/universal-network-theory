# Minimal bounded localized authenticated-write response protocol

## Intervention

For each `L=6,8,10,12,14`, take the sealed unperturbed connected component.
Choose canonical component zero and its even site `s0=0`, which is blank in
the baseline preparation. With all connected transport edges off, apply the
independently audited local F3-MDC write

\[
 r_0=\frac{14441248}{6075},\qquad
 \Phi=\frac\pi4,\qquad
 \epsilon=\frac{\pi}{4r_0},\qquad
 |B\rangle\mapsto\frac{|B\rangle-i|x\rangle}{\sqrt2}.
\]

The selected site's source-slice ledger is exact:

\[
 \Delta Q_{s_0}+\sum_{e\in\partial s_0}J_e-W_R
 =\frac12+0-\frac12=0.
\]

This is the authenticated blank-target insertion itself, not a modulation of
an already occupied head. After the write, turn the source and writer off,
restore the original owner-once connected support, and evolve with the same
simultaneous BS09 Hamiltonian at conditional `kappa=pi/2`.

## Differential record

For the perturbed and sealed baseline histories, retain complete vectors

\[
 \Delta q_i=q_i^{\rm perturbed}-q_i^{\rm baseline},\qquad
 \Delta J_e=J_e^{\rm perturbed}-J_e^{\rm baseline}.
\]

With the pre-insertion baseline state as the common initial reference, the
full differential ledger is

\[
 \Delta q^{\rm after}+B\Delta J
 -\frac12\,\mathbf e_{s_0}=r_{\rm num}^{\rm differential}.
\]

Owner-incidence columns telescope exactly, so the global number response must
obey `sum_i Delta q_i=1/2` within the separately controlled numerical error.
The remainder is retained raw and unassigned; it is not called a defect.

Report the changes in total and connector absolute throughput as direct
differences of the two finite histories. Complete signed edge differences are
primary and cannot be replaced by absolute values.

## Finite radial profile

Let `d(s0,v)` be shortest-path distance on the declared finite support graph,
not physical distance. Assign an edge `e=(u,v)` to

\[
 r_e=\min\{d(s_0,u),d(s_0,v)\}.
\]

For every `L`, radius, and edge kind (internal or connector), publish edge
count, signed `sum Delta J_e`, `sum |Delta J_e|`, mean absolute response, and
maximum absolute response, beside the complete edge vector. Optional site
shells must likewise remain beside the complete `Delta q` vector.

The final empirical description must distinguish:

- near-source concentration that persists as the finite support grows;
- approximately shell-uniform spreading; and
- far-shell enhancement or sign reversal associated with finite periodic
  return.

These are finite profile descriptions. “Periodic return” is not a physical
boundary reflection unless a later physical geometry map is supplied.

## Valid representation and resource gates

The local insertion breaks the full source-preserving symmetry used by the
uniform L12/L14 solver. The old invariant orbit basis cannot represent this
history. The canonical-source stabilizer has order two, yielding exact
marked-source orbit dimensions:

| L | dimension |
|---:|---:|
| 6 | 2,176 |
| 8 | 33,280 |
| 10 | 526,336 |
| 12 | 8,396,800 |
| 14 | 134,250,496 |

Before promotion, the response calculation must reproduce each sealed
baseline, validate its marked-source or equivalent engine against direct
full-space L6/L8 occupation and current vectors, and pass a separate resource
screen at each larger size. L14 is not forced. All numerical histories require
coarse/fine evolution and current-quadrature controls and an independent
hostile audit.

## Status

The hostile-audited L4--L14 throughput values are the empirical reference
baseline. They do not prove an asymptotic or invariant plateau. This packet
defines an insertion and measurement; it contains no perturbed response data.

**Proved:** authenticated finite write and terms-off ledger; finite support,
radial partitions, and marked-source stabilizer counts.

**Adopted:** F3-MDC `alpha=r0` and the canonical source label.

**Conditional:** support, `kappa`, separate `t` and `tau`, content, routing,
complete read, and numerical representation.

**Empirical:** the unperturbed L4--L14 reference only.

**Open:** all localized response values and profile classifications, per-size
resource eligibility, physical distance, global response owners, lawful
quotient, and Gate A-P.

No scaling law, physical grid, continuum behavior, Ward identity, phase,
graviton, gravity, `C_R`, or `G` is inserted or inferred.
