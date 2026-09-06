# Connected record trajectory L4--L10 V001

This packet compiles the four hostile-audited connected-support records at
conditional `kappa=pi/2`. It reports raw L4/L6/L8/L10 record quantities and
adjacent finite comparators without fitting or extrapolating them.

Run:

```sh
PYTHONWARNINGS=error python3 -B compile_trajectory.py
```

The compiler pins all four input `RESULT.json` hashes, preserves their raw
floating values, and must finish with
`PASS__R_CONNECTED_RECORD_TRAJECTORY_L4_L10__33/33`. Canonical output is
validated within `5e-12`.

The first pre-promotion compilation used binary-float equality for the check
that prepared retained and site ratios coincide. It stopped with that check
failed and generated a candidate carrying the failure label. That candidate
was deleted. The check now uses an explicit `1e-12` tolerance; no input data,
compiled observable, or physical rule changed.

Residuals remain raw unassigned numerical record-ledger terms, not defects.
The table is not evidence for monotonicity, a limit, exponent, continuum,
critical phase, Ward structure, graviton, or gravity.
