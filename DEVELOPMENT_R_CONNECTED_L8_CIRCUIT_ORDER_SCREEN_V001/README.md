# Connected L8 circuit order screen V001

This packet compares forward, reverse, and interleaved owner-once schedules
on the same audited 16-record connected support at fixed depth three. It
measures schedule dependence in the full terminal record distribution and in
the finite owner ledger.

Run:

```sh
PYTHONWARNINGS=error python3 compute_order_screen.py
```

The run rewrites `RESULT.json` and must finish with
`PASS__R_CONNECTED_L8_CIRCUIT_ORDER_SCREEN__14/14`.

Schedule is selected-parent data. No order is assumed to approximate a
continuum or privileged physical time ordering.
