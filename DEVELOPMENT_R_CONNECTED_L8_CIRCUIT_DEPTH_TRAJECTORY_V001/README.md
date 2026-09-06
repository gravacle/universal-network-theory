# Connected L8 circuit-depth trajectory V001

This packet follows the already-audited 16-record paired-ring circuit from
depth zero through depth eight. It records both net cumulative edge transport
and absolute gate-event traffic so that transport reversals are not erased.

Run:

```sh
PYTHONWARNINGS=error python3 compute_depth_trajectory.py
```

The run rewrites `RESULT.json` and must finish with
`PASS__R_CONNECTED_L8_CIRCUIT_DEPTH_TRAJECTORY__12/12`.

The selected support is inherited finite-family incidence, not a physical
grid. This is a microscopic record trajectory, not a continuum diagnostic.
