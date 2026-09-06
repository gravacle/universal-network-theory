# Hostile audit: Gate R-C L8 forward-edge arrival

This packet independently audits
`DEVELOPMENT_R_GATE_C_L8_FORWARD_EDGE_ARRIVAL_V001`. It imports no target
code, changes no target or authority document, and runs no support above L8.

The verifier rebuilds the 16-site, 24-edge owner-once prism and the oriented
Rail-1 edge `3 -> 4`. It evolves all eight background/probe histories using a
unitary fourth-order Suzuki--Yoshida factorization over three independently
reconstructed exact edge matchings. Separate 1,024/2,048-step runs reproduce
the first positive peak of the background-subtracted instantaneous directed
current, its current amplitude, and the node-four occupation contrast at the
same refined time. This method is materially distinct from the target's
order-ten Taylor propagation.

Run:

```sh
PYTHONWARNINGS=error python3 -B \
  AUDIT_R_GATE_C_L8_FORWARD_EDGE_ARRIVAL_V001/hostile_audit.py
```

The sealed result must finish:

```text
PASS__AUDIT_R_GATE_C_L8_FORWARD_EDGE_ARRIVAL__52/52
```

The audit confirms that `tau_fwd` is not strictly monotone and the
`N=3 < N=2` inversion survives. Option A selects final-edge inflow only: it
does not remove wraparound support, identify an earlier route, or create an
individual lineage tag. No metric, time-dilation, Shapiro-delay, or gravity
claim follows.

