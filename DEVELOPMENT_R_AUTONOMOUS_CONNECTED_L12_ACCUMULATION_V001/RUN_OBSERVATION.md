# L12 connected-run observation

Environment and command:

- declared host memory: 48 GiB;
- operating system/architecture: `Darwin 25.4.0 arm64`;
- interpreter: `Python 3.9.6`;
- command: `PYTHONWARNINGS=error REPORT_RESOURCES=1 python3 -B compute_connected_l12.py`.

Passing 512/1,024-panel run:

- wall time observed inside the process: `321.367049417 s`;
- maximum resident set observed by `getrusage(RUSAGE_SELF)`: `2,399,076,352`
  bytes = `2.23431396484375 GiB`;
- result: `PASS__R_AUTONOMOUS_CONNECTED_L12_ACCUMULATION__22/22`.

These values are a single environment observation, not a universal runtime or
complexity claim. The sandbox did not permit an independent `hw.memsize`
query, so 48 GiB is the declared environment capacity rather than a value
measured by this script.
