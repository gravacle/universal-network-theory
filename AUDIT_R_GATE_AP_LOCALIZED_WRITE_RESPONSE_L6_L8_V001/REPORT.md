# Hostile audit report — localized-write response L6/L8 V001

## Verdict

**PASS at direct finite L6/L8 response scope.** The target rows each pass
`24/24`, their pinned compilation passes `16/16`, and the independent
full-space reconstruction passes `30/30`. The independent engine imports no
target compute code and uses classical RK4 rather than the target's
tenth-order Taylor evolution. No target correction was required.

The audited target hashes are:

- L6 result: `8ae5a0dbaf27b7a1b1bcd0e023b58498920b2cacd0664dc1093df6ac060e900a`;
- L8 result: `b73ba9e1c660a5285a075fd8c040c6b04621e4badc0dbecf42483d5c0a1c72fb`;
- compiled result: `eb6dd30ddba32c9278dfc54794d4b3bc374a38568d867c9ed00c1004e64dbe49`;
- target compute: `2050a2f73de7cca0d2c1c59e4737e11a89bf125177eceedf292e5fcef2626368`;
- target compiler: `1160081f62a6419b7f4592fd2f54ecfd005b79b18235d4717f1ff8befc7eac47`.

## Independent histories and complete vectors

The audit independently constructs blank even tails with
`(|B>+|x>)/sqrt(2)` on every odd head, then tensors the authenticated
`(|B>-i|x>)/sqrt(2)` insertion at even site zero for the perturbed history.
Both histories evolve under the same source-off owner-once hopping support at
`kappa=pi/2`.

The independently computed complete occupation and oriented-current vectors
are retained in `INDEPENDENT_RESULT.json`. Their largest discrepancies from
the target are:

| comparison | L6 Linf | L8 Linf |
|---|---:|---:|
| baseline terminal occupation | `8.39e-12` | `1.77e-11` |
| perturbed terminal occupation | `8.03e-12` | `2.09e-11` |
| differential occupation | `9.45e-12` | `1.71e-11` |
| baseline integrated current | `2.32e-12` | `4.78e-12` |
| perturbed integrated current | `3.56e-12` | `7.38e-12` |
| differential integrated current | `5.10e-12` | `9.75e-12` |
| radial-shell numeric fields | `1.77e-11` | `3.04e-11` |

The independently reconstructed baseline also agrees with the separately
sealed L6/L8 accumulation records at the same scale. The target compilation
is reconstructed exactly as parsed; its canonical JSON SHA-256 is
`380f4ab10ff5a598b9b82392b22c623d781c4ae9a2a899afee57675813ff610c`.

## Differential ledger and numerical controls

For every owner-once edge `e=(u,v)`, the incidence column has `+1` at `u` and
`-1` at `v`. With the perturbed-minus-baseline initial difference
`(1/2)e_0`, the checked sign is

\[
 \Delta q^{\rm after}+B\Delta J-	frac12e_0
 =r_{\rm num}^{\rm differential}.
\]

The target L1 remainders are `1.63147e-12` at L6 and `1.65368e-12` at L8.
The independent RK4/Simpson remainders are `1.29969e-11` and `2.85200e-11`;
they are consistent with its separate coarse/fine controls. Its maximum
coarse/fine occupation differences are `1.27e-10` and `3.17e-10`, and its
maximum current differences are `5.32e-11` and `1.12e-10`. Norm, energy, and
number-law checks also pass.

The terminal source amounts are independently `0.4999999999998381` and
`0.4999999999995774`, agreeing with the target values
`0.5000000000000504` and `0.5000000000000144`. All numerical remainders stay
raw and unassigned; none is classified as a defect.

## Finite support profiles

Independent BFS on the degree-three support reproduces every edge radius and
every internal/connector shell. All 18 L6 and 24 L8 differential edge currents
are nonzero at `1e-10`. The target aggregate shell L1 records are:

- L6 radii 0--3: `0.5036822, 0.4729591, 0.6920286, 0.1453026`;
- L8 radii 0--4: `0.5045314, 0.4844919, 0.7561383, 0.2519039, 0.0482926`.

The radius-two aggregate exceeds the farthest shell at both sizes. The direct
total absolute-throughput changes are `+0.3087514330` and `+0.4509448412`;
the connector changes are `-0.0911596651` and `-0.0936681007`.

This supports only the target's lower-size description: nonuniform,
oscillatory spreading across the finite support shells. It is not a locality
or scaling law. Graph radius is not physical distance, and the far shell is
not a physical boundary reflection.

## Runtime and failed-attempt custody

The pinned `RUN_OBSERVATION.md` records:

| run | runtime (s) | maximum RSS (bytes) |
|---|---:|---:|
| L6 canonical creation | `24.111255334` | `28,655,616` |
| L6 optimized replay | `22.340707750` | `28,819,456` |
| L8 canonical optimized | `451.841224708` | `88,162,304` |
| L8 prior allocation-heavy | `492.273888208` | `85,032,960` |

These figures are custody-checked single-environment observations, not
independently reconstructed timings and not complexity laws. The present host
matches the declared Darwin/arm64 Python 3.9.6 environment and independently
confirms that `int.bit_count()` is absent. The first failed L6 attempt cannot
be replayed from a result because it failed closed before result emission; its
historical occurrence is therefore document-custodied, while the causal
compatibility fact is independently checked. No value from that attempt is
promoted.

## Claim ceiling

The direct L6/L8 vectors and finite profiles are empirical. Support,
`kappa`, content, routing, and read remain conditional. L10/L12/L14 response,
the full-ladder profile classification, physical distance, and Gate A-P remain
open. This audit does not establish a locality or scaling law, physical
boundary reflection, grid, continuum behavior, Ward identity, phase,
graviton, gravity, `C_R`, or `G`.
