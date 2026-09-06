# L14 connected-run observations

Environment and successful command:

- declared host memory: 48 GiB;
- operating system/architecture: `Darwin 25.4.0 arm64`;
- interpreter: `Python 3.9.6`;
- observed Numba worker count: 14;
- command: `PYTHONWARNINGS=error python3 -B compute_connected_l14.py`.

The successful 512/1,024-panel run observed:

- process wall time: `1528.396889875 s`;
- maximum resident set: `6,118,227,968` bytes =
  `5.6980438232421875 GiB`;
- result: `PASS__R_AUTONOMOUS_CONNECTED_L14_ACCUMULATION__27/27` before
  the append-only connector-comparator check was added arithmetically from
  the same sealed output and inputs, giving canonical target `28/28`.

The preceding bounded structural run observed `26.615857542 s` and
`5,347,344,384` bytes = `4.9801025390625 GiB`, including the warmed gather
action and serial/parallel operator cross-checks.

One earlier full attempt completed both numerical histories but failed closed
before emitting a result when `PYTHONWARNINGS=error` surfaced a floating-status
warning in the final small BLAS incidence product. The equivalent explicit
owner-edge balance sum replaced that product. No value from the failed attempt
is promoted.

These are single-environment observations, not runtime, memory-complexity, or
scaling laws. The 48 GiB capacity is declared rather than measured by the
script.
