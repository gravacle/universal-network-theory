# Exact repeated-scale native interaction trajectory

## 1. Common prepared family

For even `L`, the R-B preparation leaves `L^3/2` head qutrits at odd first
coordinate, each in `(|B>+|x>)/sqrt2`. Pair them along the second generator
from even to odd second coordinate. This gives `L^3/4` disjoint native R-C
interaction blocks, each with the same Hamiltonian and duration.

This is a fixed-density prepared family. The adopted `alpha=r0` attachment is
`r0=14441248/6075`, is not derived from bare F3, and is not changed with `L`.
At each size the terminal instrument is the inherited complete product of
qutrit, controller `{OK,FAILURE}`, work, and reference effects. Zero-probability
failure outcomes remain in the alphabet and no outcome is conditioned away.

## 2. Exact trajectory

Each block preserves expected retained occupation one, carries absolute
oriented interaction throughput `1/4`, changes its complete positional read
by TV `1/4`, and has zero endpoint residuals. Therefore

\[
 N_{\rm block}(L)={L^3\over4},\quad
 Q_{\rm ret}(L)={L^3\over4},\quad
 \mathcal A_{\rm int}(L)={L^3\over16},
\tag{D01}
\]

\[
 Q_{\rm low}(L)={L^3\over16},\qquad
 Q_{\rm high}(L)={3L^3\over16},\qquad
 r_1(L)=r_\infty(L)=0.
\tag{D02}
\]

The raw values are:

| quantity | L=4 | L=8 | ratio |
|---|---:|---:|---:|
| cells | 64 | 512 | 8 |
| interaction blocks | 16 | 128 | 8 |
| expected retained total | 16 | 128 | 8 |
| interaction throughput | 4 | 32 | 8 |
| low/high positional expectations | 4 / 12 | 32 / 96 | 8 / 8 |
| record-ledger residual `r_1` | 0 | 0 | exact |
| record-ledger residual `r_infinity` | 0 | 0 | exact |

The observed factor eight follows exactly from the declared fixed-density,
disjoint-block preparation. It is not fitted and is not evidence for a
continuum exponent or critical state. The trajectory establishes reproducible
microscopic accumulation and interaction accounting across the two sizes.

## 3. Scope ceiling

The result does not test overlapping interactions, feedback between blocks,
long histories, generic lineage retention, or a critical accumulation state.
A future nonzero residual is unclassified until its owner is determined.
No Ward or gravity observable is evaluated.
