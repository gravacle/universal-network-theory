# Pre-output execution compatibility repair

Date: 2026-09-22

Status: `DOCUMENTED_BEFORE_PHYSICAL_OUTPUT__REFREEZE_REQUIRED`

The first authorized hostile execution was started with the exact frozen
authorization token and `PYTHONWARNINGS=error`.  It stopped at the initial
L4 diagnostic checkpoint before `HOSTILE_RESULT.json` was written.  The local
Apple BLAS implementation emitted:

```text
RuntimeWarning: divide by zero encountered in matmul
```

The warning arose in a witness-readout reduction.  It was not a nonfinite
state value, failed control, changed physical result, or target comparison.
The strict warning policy converted it to an exception as intended.

The compatibility repair replaces every BLAS-backed `matmul`/`dot` reduction
inside the witness readout and its direct controls with explicit NumPy
elementwise multiplication followed by summation.  These expressions are
algebraically identical finite sums over the same frozen arrays and indices.
The repair changes none of the following:

- parent graph, basis, initial state, or event order;
- admission or transport implementation;
- `phi`, dwell, Taylor order, or 64/128 substep schedule;
- witness, sham, or shuffle definitions;
- checkpoint schedule, tolerances, or classification rule; or
- deterministic output schema.

No hostile result file existed after the stopped attempt.  No target source,
output, array, matrix, value, or message was inspected.  Synthetic L2/L3
tests must pass and all source hashes must be regenerated before physical
execution resumes.
