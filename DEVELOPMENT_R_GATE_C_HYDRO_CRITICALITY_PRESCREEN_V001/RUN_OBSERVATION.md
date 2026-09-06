# Target run observation

The passing exact-through-L8 command was:

```text
PYTHONWARNINGS=error python3 -B compute_seed_screen.py
```

Observed on Darwin arm64 with Python 3.9.6, NumPy 2.0.2, and one declared BLAS
thread:

- total wall time: `320.461642042 s`;
- maximum worker wall time: `158.518236333 s`;
- maximum worker resident set: `8,034,484,224` bytes =
  `7.482696533 GiB`;
- target result: `NO_CANDIDATE_L4_L8__STOP_NO_L10_L12__36/36`.

The maximum worker remained below the frozen 12-GiB and 45-minute L8 guards.
No L10/L12 process was started.  These are observations from this environment,
not portable resource or complexity guarantees.
