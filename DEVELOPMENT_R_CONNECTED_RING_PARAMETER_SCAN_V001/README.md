# Connected-ring parameter scan V001

This packet scans the already-audited connected eight-record carrier ring at
four staggered onsite strengths and three pulse times. It is a bounded
microscopic accumulation diagnostic, not a search for continuum behavior.

Run:

```sh
PYTHONWARNINGS=error python3 compute_parameter_scan.py
```

The run rewrites `RESULT.json` and must finish with
`PASS__R_CONNECTED_RING_PARAMETER_SCAN__13/13`.

The inherited `alpha=r0` source attachment remains adopted F3-MDC input and
is not a bare-F3 derivation. The complete failure-inclusive terminal product
PVM remains part of the selected parent.

