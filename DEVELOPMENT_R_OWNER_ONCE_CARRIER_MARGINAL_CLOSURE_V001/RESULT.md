# CMC-1 disposition

Date: 2026-09-22

Disposition:

```text
PASS_EXACT_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE__FINITE_ACCUMULATION_SCOPE_ONLY
```

The frozen analytic theorem, the repaired finite target verifier, and the
independently written hostile reconstruction agree.  During the declared
owner-once first pass, while lineage outcomes remain unread, tracing out the
lineage register gives exactly the carrier channel

\[
\Phi_e(\sigma)=K_{0,e}\sigma K_{0,e}^{\dagger}
                +K_{1,e}\sigma K_{1,e}^{\dagger},
\]

with

\[
K_{0,e}=P^1_e+\cos(\phi)P^0_e,
\qquad
K_{1,e}=-i\sin(\phi)a_e^{\dagger}P^0_e.
\]

The primary target passes L4 and L6.  Its maximum full-versus-reduced
disagreements are `2.220446049250313e-16` and
`7.771561172376096e-16`; its maximum norm/control errors are
`4.2021941482062175e-13` and `5.949463144361289e-12`.  Supplemental L8
also passes, with disagreement `5.384581669432009e-15` and control error
`3.526412495347131e-11`.

The hostile reconstruction uses a different basis ordering, different edge
traversal, independently written admission and transport code, and no target
matrices or result values.  It passes L4 and L6 with maximum disagreement
`2.220446049250313e-16` at both sizes and maximum control errors
`4.2033043712308427e-13` and `5.9497962112686764e-12`.  Its wrong closed-ladder
negative control is detected.

The reconciliation is machine-checked by `reconcile_closure.py`; all governing
documents, implementations, and result packets are SHA-256 pinned in
`CARRIER_MARGINAL_CLOSURE_DISPOSITION_V001.json`.

## Meaning

For every carrier-only observable in this finite owner-once engine, the fair
lineage-erased comparator is the same ladder plus the matched unread admission
channel.  The closed ladder alone is not the matched comparator.

This is a substantive model diagnosis: the explicit lineage register carries
history and custody, but under the present first-pass law it produces no
additional unconditional carrier signal beyond its reduced channel.

## Boundary

The disposition does not apply to lineage postselection, lineage-conditioned
observables, revisits, lineage-dependent schedules, or a future Hamiltonian or
measurement that reads a retained record.  It establishes no Gate,
Record--Geometry Realization Law, alpha, continuum, thermodynamic-limit, or
gravity conclusion.  The next registered test therefore concerns a joint
lineage--carrier observable, not another carrier-only statistic.
