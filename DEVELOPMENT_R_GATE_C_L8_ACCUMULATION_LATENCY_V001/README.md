# Gate R-C L8 accumulation latency diagnostic V001

This bounded packet tests operational connector capacity and first-arrival
time on one owner-once degree-three L8 prism component. It introduces no
metric, grid, or physical clock.

The conditional parent is all blank. A probe uses the authenticated
`W_R=1/2` write at Rail-1 node 0. Background histories contain `N=0,1,2,3`
authenticated writes at the adjacent Rail-1 nodes `1..N`; Rail-1 node 4 is
the target. Since individual lineage is not retained after mixing, the probe
signal is the background-subtracted target occupation

```text
q_target(background + probe) - q_target(background).
```

The operational transit time is the first positive local maximum of that
signal in `0 < kappa <= 2*pi`. Probe-accessible connector throughput is the
L1 norm of the background-subtracted vector of time-integrated connector
currents over the inherited fixed window `kappa=pi/2`. The signed connector
sum and both unsubtracted throughputs remain in `RESULT.json`.

Run:

```sh
PYTHONWARNINGS=error python3 -B \
  DEVELOPMENT_R_GATE_C_L8_ACCUMULATION_LATENCY_V001/compute_accumulation_latency.py
```

The target must finish
`PASS__R_GATE_C_L8_ACCUMULATION_LATENCY__17/17`.

Target status is candidate pending independent hostile audit. No latency or
throughput row is a physical metric, gravitational time dilation, Shapiro
delay, critical mass, or gravity result.
