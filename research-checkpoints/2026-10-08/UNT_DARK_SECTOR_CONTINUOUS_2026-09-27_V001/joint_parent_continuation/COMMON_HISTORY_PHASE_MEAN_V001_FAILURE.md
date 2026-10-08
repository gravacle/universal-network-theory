# V001 publication failure and additive serialization repair

2026-09-28. The V001 phase-mean postprocessor exited with code 1 after
approximately 0.52 seconds, while serializing the completed in-memory payload.
No result file was published. The traceback ends at `disk_solver.py:26`,
`json.dumps(..., allow_nan=False)`, with
`TypeError: Object of type bool is not JSON serializable`.

The quadrature pass comparison was a NumPy boolean, which the standard JSON
encoder does not accept. V001 source, protocol and freeze remain unchanged.
V002 reuses the entire frozen calculation and changes only publication by
recursively converting NumPy scalar values to Python scalars. It authenticates
the V001 source census before running and publishes to new V002 paths. No
equation, mode state, phase rule, tolerance, source or observational value is
changed. A rerun of this tiny deterministic postprocessor needs no checkpoint.
