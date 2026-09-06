# Autonomous connected L8 accumulation V001

This packet extends the hostile-audited connected L4/L6 support pattern to
L8: 32 connected sixteen-site components cover 512 sites and own 768 internal
and connector edges once. It uses the uniform F3-MDC preparation and one
simultaneous BS09 Hamiltonian at conditional `kappa=pi/2`.

Run:

```sh
PYTHONWARNINGS=error python3 -B compute_connected_l8.py
```

The 65,536-state component calculation is matrix-free. It uses order-10
unitary Taylor steps and compares 1,024-step and 2,048-step Simpson current
integrations. It validates the frozen raw `RESULT.json` within `5e-10` and
must finish with
`PASS__R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION__21/21`.

Set `REPORT_RESOURCES=1` to print wall time and maximum RSS without placing
run-dependent values in the canonical result. `RUN_OBSERVATION.md` freezes one
such observation on the declared 48 GiB host.

The refined integration is numerical, not exact. Support and mission
parameters remain conditional. No defect, grid, continuum, Ward, phase,
criticality, graviton, or gravity claim is made.
