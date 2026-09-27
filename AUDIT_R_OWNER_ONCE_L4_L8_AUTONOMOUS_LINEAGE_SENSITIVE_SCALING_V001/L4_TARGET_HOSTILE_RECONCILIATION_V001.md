# L4 target/hostile lineage-response reconciliation

Disposition: `PASS_TARGET_HOSTILE_L4_EVENT0_NUMERICAL_RECONCILIATION__AUDIT_ONLY_EVENTS1_3_NOT_CROSS_RECONCILED`.

Target result SHA-256: `509d96ad59268cd75ee3b1275fd095b4b8642d498750e81b9d145374c6ac8c4c`.
Hostile result SHA-256: `8f46b0a64f49591650613c0b2a4f2032156ce96fce8b1267f36fe6d50db61756`.
Hostile pre-unblinding seal SHA-256: `0add3a7197dcdda0a67e2e6f5469fa28ef5de48a73eed02ee3b13968392dae62`.

## Numerical gate

All common registered fields pass with base absolute tolerance `1.0e-10`. The maximum non-`T_dyn` absolute difference is `6.106226635438361e-16`.

For `T_dyn = Delta_C/tau`, the propagated absolute tolerance is `1`; its raw absolute difference is `3.0994415283203125e-06`. The maximum difference/tolerance fraction over positive-tolerance fields is `6.106226635438361e-06`.

The target label and hostile label are intentionally not identical strings: the target certifies dense reproduction, while the hostile lane certifies a resolved independent event-0 response. Their typed pass dispositions are compatible.

## Scope

The target result contains event 0 only. Hostile events 1--3 are retained as audit-only results and are not cross-reconciled. This establishes no L6/L8 persistence, scaling exponent, all-L result, curvature, geometry, or gravity.

Per-sector carrier trace distances, actual/product traces, signed traces, and transport invariance agree. Target per-sector configuration-TV and occupation vectors had no pre-sealed hostile counterparts and are reported but excluded from the cross-lane gate.

## Resources

Target: `0.903229917` s, `35176448` peak RSS bytes, `19443` persisted checkpoint bytes.
Hostile: `1.134873375` s, `36945920` peak RSS bytes, `0` persisted checkpoint bytes, with `7920` logical terminal-checkpoint bytes held in memory.

Storage figures are not like-for-like: the target retained restart custody, while the hostile run persisted only result custody. Energy was not metered.
