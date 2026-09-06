# L10 connected-run observation

Environment and command:

- declared host memory: 48 GiB;
- operating system/architecture: `Darwin 25.4.0 arm64`;
- interpreter: `Python 3.9.6`;
- command: `PYTHONWARNINGS=error REPORT_RESOURCES=1 python3 -B compute_connected_l10.py`.

Passing 1,024/2,048-panel run:

- wall time observed inside the process: `48.279534083 s`;
- maximum resident set observed by `getrusage(RUSAGE_SELF)`: `349,585,408`
  bytes = `333.390625 MiB`;
- result: `PASS__R_AUTONOMOUS_CONNECTED_L10_ACCUMULATION__24/24`.

These values are a single environment observation, not a universal runtime or
complexity claim. The sandbox did not permit an independent `hw.memsize`
query, so 48 GiB is the declared environment capacity rather than a value
measured by this script.
