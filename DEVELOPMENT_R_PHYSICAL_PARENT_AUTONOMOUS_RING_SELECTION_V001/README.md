# Physical-parent autonomous ring selection V001

This packet derives the retained-head preparation from the audited F3-MDC
write and tail-to-head transfer, then evolves it with the simultaneous BS09
carrier Hamiltonian on fixed programmed first-generator cycles. There is no
node-dependent stagger and no arbitrary gate order.

Run:

```sh
PYTHONWARNINGS=error python3 compute_autonomous_ring.py
```

The run rewrites `RESULT.json` and must finish with
`PASS__R_PHYSICAL_PARENT_AUTONOMOUS_RING_SELECTION__16/16`.

The support program, hopping coefficient, pulse duration, and `alpha=r0`
attachment remain conditional. The packet does not claim autonomous support
formation, a selected phase, continuum behavior, or gravity.
