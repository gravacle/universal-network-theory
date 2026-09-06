# Connected L4-L6-L8 trajectory V001

This packet inserts an L=6 connected record between the hostile-audited L4
and L8 rows. It preserves the same explicit preparation, schedule, depth,
source attachment, and complete terminal read.

Run:

```sh
PYTHONWARNINGS=error python3 compute_l6_interpolation.py
```

The run hash-pins its L4/L8 parent result, rewrites `RESULT.json`, and must end
with `PASS__R_CONNECTED_L4_L6_L8_TRAJECTORY__15/15`.

Only raw adjacent ratios are reported. No exponent, interpolation formula,
continuum trend, or preferred history is inferred.
