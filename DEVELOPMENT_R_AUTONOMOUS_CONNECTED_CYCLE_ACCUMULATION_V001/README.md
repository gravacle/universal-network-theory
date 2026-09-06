# Autonomous connected-cycle accumulation V001

This packet constructs the smallest connected-cycle physical-parent witness:
two four-site cycles joined by four opposite-parity connectors and evolved by
one simultaneous BS09 Hamiltonian. Eight identical components cover all 64
L4 sites. The ordinary uniform F3-MDC head/tail preparation is used; no node
stagger, finite gate order, or extra source-routing asymmetry is introduced.

Run:

```sh
PYTHONWARNINGS=error python3 compute_connected_cycle.py
```

The run validates the frozen raw `RESULT.json` within `8e-12` and must end
with `PASS__R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION__18/18`.

Support and `kappa=pi/2` remain conditional. The finite CTP expression is an
owner-once bookkeeping functional, not a Ward, continuum, phase, or gravity
claim.
