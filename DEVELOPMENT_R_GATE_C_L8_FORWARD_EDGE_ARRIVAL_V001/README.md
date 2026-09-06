# Gate R-C L8 forward-edge arrival control V001

This is the bounded Option-A control for the nonmonotone node-occupation
arrival observed in the sealed L8 accumulation-latency screen. It leaves the
audited owner-once degree-three prism unchanged and measures only inflow on
the directed Rail-1 edge `3 -> 4`.

For each `N=0,1,2,3`, the observable is the instantaneous ensemble contrast

```text
delta J_3->4(t) = J_3->4(background N + probe) - J_3->4(background N).
```

`tau_fwd(N)` is the first positive local maximum of this directed-current
contrast above `1e-8` on `0<t<=2*pi`, using a three-point parabolic vertex.
The packet records both its peak current and the background-subtracted node-4
occupation evaluated at the same refined time.

This isolates the final forward-edge inflow observable; it does not remove the
counter-clockwise support and does not create an individual carrier tag.

Run:

```sh
PYTHONWARNINGS=error python3 -B \
  DEVELOPMENT_R_GATE_C_L8_FORWARD_EDGE_ARRIVAL_V001/compute_forward_edge_arrival.py
```

The target must finish
`PASS__R_GATE_C_L8_FORWARD_EDGE_ARRIVAL__14/14`. Results remain candidates
until a solver-independent hostile audit passes.
