# Autonomous connected L12 accumulation V001

This packet applies the hostile-audited order-`2L` finite prism-orbit basis to
the next conditional connected-support record. Seventy-two connected
twenty-four-site components cover 1,728 sites and own 2,592 internal and
connector edges once. The uniform F3-MDC source and simultaneous BS09
Hamiltonian at conditional `kappa=pi/2` are unchanged.

Run:

```sh
PYTHONWARNINGS=error python3 -B compute_connected_l12.py
```

The exact finite group compresses 16,777,216 component words to 704,370 orbit
states. To keep this finite run bounded, order-10 Taylor evolution compares
512-step and 1,024-step Simpson current integrations. The script validates
frozen `RESULT.json` within `3e-9` and must finish with
`PASS__R_AUTONOMOUS_CONNECTED_L12_ACCUMULATION__22/22`.

Set `REPORT_RESOURCES=1` to print wall time and maximum RSS without storing
run-dependent values in the canonical result. `RUN_OBSERVATION.md` freezes one
such observation on the declared 48 GiB host.

Only the finite orbit basis is exact. Evolution and current quadrature remain
numerical. Support and mission parameters remain conditional. The larger raw
numerical residual reflects the bounded quadrature and remains an unassigned
record-ledger term, not a defect. No grid, continuum, Ward, scaling, phase,
criticality, graviton, or gravity claim is made.
