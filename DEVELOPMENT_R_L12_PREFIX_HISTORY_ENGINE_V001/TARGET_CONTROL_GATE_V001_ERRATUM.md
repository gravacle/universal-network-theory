# Target control comparator V001 erratum

The first post-output comparator returned `23/24` because it compared the
entire L6 sector-report dictionary for Python object equality. The selected
events, `q` endpoints, and density interval were identical. The enclosed and
discarded masses differed only by `1.1102230246251565e-16` from summation
order.

V002 preserves the failed `TARGET_CONTROL_GATE.json`, requires exact identity
of the structural interval fields, and applies the already frozen `1e-8`
history tolerance to the two numerical masses. It changes no engine output,
physics, sector selection, or preregistered tolerance.
