# Connected L4-to-L8 native-component trajectory V001

This packet applies the same explicit reversed-preparation, forward-schedule,
depth-three recipe to connected native components at L=4 and L=8. It reports
raw record ratios without fitting an exponent or assuming continuum behavior.

Run:

```sh
PYTHONWARNINGS=error python3 compute_connected_scale_trajectory.py
```

The run rewrites `RESULT.json` and must finish with
`PASS__R_CONNECTED_L4_L8_NATIVE_COMPONENT_TRAJECTORY__14/14`.

The finite tuple labels are inherited enumeration, not a physical grid. The
schedule and preparation remain explicit record labels, not universal laws.
