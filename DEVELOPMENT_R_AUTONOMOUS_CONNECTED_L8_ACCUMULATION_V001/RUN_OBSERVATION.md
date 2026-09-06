# L8 connected-run observation

Environment and command:

- declared host memory: 48 GiB;
- operating system/architecture: `Darwin 25.4.0 arm64`;
- interpreter: `Python 3.9.6`;
- command: `PYTHONWARNINGS=error REPORT_RESOURCES=1 python3 -B compute_connected_l8.py`.

Passing 1,024/2,048-panel run:

- wall time observed inside the process: `55.522473084 s`;
- maximum resident set observed by `getrusage(RUSAGE_SELF)`: `73,613,312`
  bytes = `70.203125 MiB`;
- result: `PASS__R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION__21/21`.

These values are a single environment observation, not a universal runtime or
complexity claim. The sandbox did not permit an independent `hw.memsize`
query, so 48 GiB is the declared environment capacity rather than a value
measured by this script.

The first pre-result run completed the physical/numerical solve but stopped
before ledger evaluation because Python 3.9 lacks `int.bit_count`. It wrote no
`RESULT.json`. The implementation-only call was replaced by the portable
population count already used in the sealed L6 packet; the preparation,
Hamiltonian, step counts, quadrature, and acceptance bounds were unchanged.
The passing observation above is from the corrected warning-as-error run.
