# Autonomous BS09 kappa trajectory V001

This packet maps finite microscopic record observables at L4, L6, and L8 as a
function of the dimensionless physical evolution parameter
`kappa=t*tau/hbar`. It uses the audited F3-MDC source preparation and the
explicitly conditional fixed cycle support.

Run:

```sh
PYTHONWARNINGS=error python3 compute_kappa_trajectory.py
```

The run rewrites `RESULT.json` and must end with
`PASS__R_AUTONOMOUS_KAPPA_TRAJECTORY__15/15`.

The scan contains no finite gate order or node-dependent stagger. It does not
select `t`, a clock, or a support program, and it makes no grid, criticality,
continuum, Ward, or gravity inference.
