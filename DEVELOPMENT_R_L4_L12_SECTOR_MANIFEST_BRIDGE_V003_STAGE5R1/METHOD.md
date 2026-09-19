# V003R1 Stage-5 Decimal representation repair

The frozen Stage-5 predecessor authenticates JSON with `parse_float=Decimal`.
The V003 bridge then compared the parsed exact `Decimal('1E-8')` tolerance to
the binary float literal `1e-8`. Those numerically intended values do not
compare equal in Python, so the bridge refused an exact Stage-4 result for
which all other identity and bound predicates passed.

Stage5R1 is limited to an in-memory type projection at that interface:

1. Require the parsed tolerance to have type `Decimal`.
2. Require it to equal exactly `Decimal('1e-8')`.
3. Copy the audit record and project only that value to the float representation
   expected by the unchanged frozen V003 validator.
4. Execute the complete original validator and frozen manifest builder.

The Stage-4 artifact on disk is never modified. Its SHA-256 remains the
canonical source binding. No threshold, numerical value, history, sector,
observable, or physical definition is changed.
