# Finite L8 accumulated-write transit and connector statement

## Declared operational protocol

Use the audited owner-once L8 prism: two eight-site rails and eight
connectors, 16 sites and 24 degree-three support edges. Start from the
conditional all-blank parent. Place the probe write at Rail-1 node zero and
the `N` accumulated writes at adjacent nodes `1..N`, for `N=0,1,2,3`. Every
write is the authenticated blank-target map with `W_R=1/2`; all transport is
off during writing. The source and writers are off during subsequent
transport under the same hopping Hamiltonian.

The target at Rail-1 node four is graph distance four from the probe. These
labels and this distance belong to the finite support only. They are not a
physical metric or grid.

Individual carrier lineage is not available after hard-core mixing. Define
the operational probe signal by subtraction:

\[
 A_N(t)=q_4^{\text{background }N+\text{probe}}(t)
       -q_4^{\text{background }N}(t).
\]

The transit time `tau(N)` is fixed before evaluation as the first positive
local maximum of `A_N` above `1e-8` in `0<t<=2*pi`, with a three-point
parabolic vertex refinement. This is a first-arrival diagnostic, not a clock
metric.

Over the common capacity window `0<=t<=pi/2`, define the complete
background-subtracted current vector and connector capacity by

\[
 \delta J_e^{(N)}=J_e^{N+\mathrm{probe}}-J_e^N,
 \qquad
 J_{\rm connector}(N)=\sum_{e\in\mathrm{connector}}
 |\delta J_e^{(N)}|.
\]

This L1 quantity avoids cancellation of oppositely oriented connector
currents. The signed sum is retained separately.

## Finite result

| N | accumulated sites | `J_connector(N)` | signed connector sum | `tau(N)` | first peak `A_N` |
|---:|---|---:|---:|---:|---:|
| 0 | — | `0.5000000000039362` | `0.5000000000039362` | `1.222689868854405` | `0.0010923892891643826` |
| 1 | `1` | `0.42815973374869076` | `0.42815973374869076` | `1.3455677498194254` | `0.001557931321984419` |
| 2 | `1,2` | `0.36531361324457556` | `0.3563681524480833` | `2.971600967337824` | `0.10363914917295328` |
| 3 | `1,2,3` | `0.3308471281165849` | `0.3284440503536715` | `2.86146468598496` | `0.08531515936994283` |

The probe-accessible connector L1 throughput decreases strictly over the four
rows. A least-squares linear finite-window diagnostic gives

```text
J(N) = 0.4916258292033723 - 0.05703047361661693 N
R^2 = 0.9778724186839928
formal zero = 8.620405864210246
```

The formal zero exceeds the maximum six distinct background sites available
on this finite rail after reserving probe and target. It is therefore not an
admissible `N_crit`; pinch-off is unmeasured.

Transit time increases through `N=2` but decreases from
`2.971600967337824` at `N=2` to `2.86146468598496` at `N=3`. Strict monotone
latency is not observed. The largest coarse/fine transit-time difference is
`1.631e-5`.

## Numerical and claim boundary

All histories occupy at most four particles. Because the hopping Hamiltonian
conserves number, the `0..4` sectors contain all reachable histories and have
dimension `2517` inside the complete `2^16=65536` word space. Order-ten
direct polynomial propagation uses 1,024/2,048 search steps. Maximum
capacity-current refinement is `1.284e-10`; maximum target differential
ledger L1 is `1.270e-10`; capacity energy drift is below `4.9e-15`.

**Proved:** owner-once finite L8 topology, blank-target write ledgers, and the
declared operational subtraction identities.

**Adopted:** `alpha=r0`, the two bounded time windows, canonical rail cluster,
and first-peak rule.

**Conditional:** all-blank parent, common write phase, background subtraction,
and numerical representation.

**Empirical:** the four connector and transit rows, monotone connector
depletion over `N=0..3`, nonmonotone first-arrival times, and the inadmissible
linear zero diagnostic.

**Open:** independent hostile audit; other clusters, phases, arrival rules,
and windows; larger `N` and `L`; pinch-off; a physical metric and clock;
Gate R-C and Gate A-P.

No individual lineage transit, critical mass, physical metric strain,
gravitational time dilation, Shapiro delay, continuum behavior, or gravity is
claimed.
