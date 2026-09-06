# Autonomous connected L6 accumulation V001

This packet extends the hostile-audited connected L4 support pattern to L6:
18 connected twelve-site components cover 216 sites and own 324 internal and
connector edges once. It uses the uniform F3-MDC preparation and one
simultaneous BS09 Hamiltonian at conditional `kappa=pi/2`.

Run:

```sh
PYTHONWARNINGS=error python3 compute_connected_l6.py
```

The matrix-free calculation uses order-10 unitary Taylor steps and compares
1024-step and 2048-step current integrations. It validates the frozen raw
`RESULT.json` within `2e-11` and must finish with
`PASS__R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION__20/20`.

The refined integration is numerical, not exact. Support and mission
parameters remain conditional. No defect, grid, continuum, Ward, phase,
criticality, or gravity claim is made.
