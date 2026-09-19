# V003 whole-workset accounting erratum

The frozen V002 L4 control was numerically resolved, but its ordinary-path
telemetry left `maximum_live_bytes` at zero and its batch formula counted the
retained Lanczos basis without four simultaneous recurrence/endpoint/sample
vectors.

V003, before any L6/L8/L10 V002-family output:

- records maximum live bytes for every batch;
- uses `(maximum_basis_vectors + 4) * vector_bytes` for the ordinary-path
  dispatch and batch limit; and
- retains the already frozen `1,000,000,000 B` cap.

No operator, state, branch, tolerance, quadrature, Krylov checkpoint, result
threshold, or claim is changed. The V002 L4 output is preserved and is not a
promotion input.
