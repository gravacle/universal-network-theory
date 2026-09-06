# Finite L8 periodic-rail-wrap removal statement

## Declared topological comparison

Start from the sealed owner-once L8 prism. Remove exactly the Rail-1 owner edge
`7 -> 0` and Rail-2 owner edge `15 -> 8`; retain the other 22 owners,
including all eight connectors. Keep the authenticated probe at node zero,
background writes at nodes `1..N`, target node four, and the periodic packet's
measurement rules.

The target contrast is

\[
 A_N(t)=q_4^{\mathrm{background}+\mathrm{probe}}(t)
       -q_4^{\mathrm{background}}(t).
\]

`tau_open(N)` is its first positive local maximum above `1e-8` on
`0<t<=2*pi`. Connector throughput is the L1 norm of the background-subtracted
integrated connector-current vector over `0<=t<=pi/2`.

## Classification rule

- If `tau_open(3)<tau_open(2)`, the inversion survives removal of the two
  periodic rail wraps and is classified as finite open-support mode
  reorganization, not periodic rail-wrap-mediated interference.
- If the inversion disappears and `tau_open` is strictly increasing, classify
  it as ring-mediated in this declared periodic-versus-open comparison.
- If the `N=3/N=2` inversion disappears but another nonmonotonic step remains,
  the binary classification is unresolved.

The open support has one shortest length-four forward path. The retained
connector network also supplies two length-six routes avoiding nodes `1,2,3`;
therefore this control does not establish a unique route for every history.

## Claim boundary

The result is a finite topological classification under owner-once
conservation. Background subtraction is not individual lineage. No physical
metric, time dilation, Shapiro delay, macroscopic emergence, or gravity claim
follows. Numerical observations remain candidates pending independent hostile
audit.
