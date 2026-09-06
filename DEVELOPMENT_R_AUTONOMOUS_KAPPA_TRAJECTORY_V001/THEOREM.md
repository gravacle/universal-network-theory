# Finite autonomous BS09 record trajectory in `kappa=t tau/hbar`

## 1. Physical parameter and scope

On the conditional fixed cycle word, source-off literal BS09 is

\[
 H_{car}=\epsilon_\psi Q-tA,\qquad
 U(\tau)=\exp(-iH_{car}\tau/\hbar).                 \tag{K01}
\]

`Q` commutes with `A` and with the recorded occupation, current, and
number-law observables. The uniform onsite part is therefore irrelevant to
those expectations. After changing variables from physical time to
`s=t tau'/hbar`, the remaining record trajectory depends on

\[
 \kappa={t\tau\over\hbar}.                          \tag{K02}
\]

This reduction does not select `t` or `tau`. It only identifies the
dimensionless combination probed by this declared mission.

## 2. Finite scan

Use the audited source preparation: even tails are blank, odd heads are
`(B+x)/sqrt(2)`, and sources are off during accumulation. For each of L4, L6,
and L8, evolve every length-L cycle simultaneously under (K01) at

\[
 \kappa\in\{0,\pi/16,\pi/8,\pi/4,3\pi/8,\pi/2,
 3\pi/4,\pi,3\pi/2,2\pi\}.                         \tag{K03}
\]

There are `L^2` cycles, `L^3/2` prepared source lineages, and expected retained
total `L^3/4`, giving respectively

| L | cycles | source lineages | expected retained total |
|---:|---:|---:|---:|
| 4 | 16 | 32 | 16 |
| 6 | 36 | 108 | 54 |
| 8 | 64 | 256 | 128 |

At `kappa=0`, every integrated current is zero. At every scanned positive
`kappa`, the raw absolute integrated throughput is positive; at the audited
`pi/2` baseline every support is active. The `pi/2` L4/L8 rows reproduce the
prior hostile-audited autonomous record packet to maximum absolute difference
below `5e-12`.

The complete numerical rows and L8/L4 ratios are retained in `RESULT.json`.
Throughput is nonmonotone over the finite scan for all three sizes. No curve,
exponent, critical point, or limiting law is fitted.

The raw absolute integrated throughput totals are:

| `kappa` | L4 | L6 | L8 | L8/L4 per retained record |
|---:|---:|---:|---:|---:|
| `0` | 0 | 0 | 0 | undefined at zero |
| `pi/16` | 1.772731 | 5.982833 | 14.181530 | 0.999978 |
| `pi/8` | 6.223937 | 20.997912 | 49.772826 | 0.999625 |
| `pi/4` | 14.422799 | 48.321777 | 114.539271 | 0.992693 |
| `3pi/8` | 11.927586 | 38.150049 | 90.379289 | 0.947167 |
| `pi/2` | 5.065021 | 13.507233 | 31.481053 | 0.776923 |
| `3pi/4` | 8.287034 | 40.094056 | 89.917633 | 1.356300 |
| `pi` | 7.432865 | 15.019279 | 45.537807 | 0.765819 |
| `3pi/2` | 1.106941 | 33.516845 | 29.924873 | 3.379229 |
| `2pi` | 2.107720 | 26.658043 | 54.198543 | 3.214288 |

These ratios range across and away from volume replication as finite
recurrences develop. They are raw record comparisons, not a scaling ansatz.

## 3. Ledger and claim boundary

For every row, expected retained total and the full carrier-number law are
conserved. The independently integrated edge currents close the cellwise
continuity equation; the maximum raw per-cycle residual is reported directly
with norm and energy controls. Across all 30 rows the maxima are
`2.554e-15` L1 and `8.188e-16` Linf per cycle, with maximum tiled L1 bound
`1.635e-13`; norm, energy, and number-law controls are at most
`7.772e-16`, `2.015e-15`, and `6.107e-16`. Residuals are unassigned
record-ledger terms, not physical defects.

**Proved:** reduction of the declared uniform-onsite BS09 record observables
to dependence on `kappa`; exact retained/lineage census; and the finite
owner-once continuity identity used by the computation.

**Adopted:** the inherited F3-MDC attachment `alpha=r0`.

**Conditional:** fixed cycle support, the ten sampled `kappa` values, content
sector, source/clock calibration, and complete terminal read.

**Empirical/numerical:** the L4/L6/L8 occupation, current, correlation,
throughput, residual, and ratio rows.

**Open:** autonomous support selection; separate selection of `t` and `tau`;
generic preparation/phase behavior; and all macroscopic response questions.

This is a microscopic accumulation map. It assumes no physical grid and no
mature continuum behavior. It inserts no graph reward, graviton, Ward axiom,
or gravity claim.
