# Gate R-C L8 open-ladder topological control V001

This packet performs the literal Option-B control requested for the sealed L8
accumulation-latency screen. It removes only periodic rail owner edges
`7 -> 0` and `15 -> 8`. All eight inherited connectors and every other owner
edge remain active.

The authenticated probe, adjacent background writes, target, ensemble
subtraction, first-positive-peak rule, search window, connector-current window,
and numerical refinement match the periodic protocol. This isolates the
topological effect of the two rail-wrap edges.

The resulting support has a unique length-four shortest path
`0 -> 1 -> 2 -> 3 -> 4`. Because the inherited connector pattern is retained,
two length-six routes avoiding nodes `1,2,3` remain:
`0 -> 9 -> 8 -> 7 -> 6 -> 5 -> 4` and
`0 -> 9 -> 10 -> 11 -> 12 -> 13 -> 4`. “Open ladder” in this packet therefore
means exact removal of the two requested periodic rail wraps, not unique
all-history path or individual lineage.

Run:

```sh
PYTHONWARNINGS=error python3 -B \
  DEVELOPMENT_R_GATE_C_L8_OPEN_LADDER_CONTROL_V001/compute_open_ladder_control.py
```

The target must finish
`PASS__R_GATE_C_L8_OPEN_LADDER_CONTROL__21/21`. Results remain candidates
until an independent hostile audit passes.
