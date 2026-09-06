# Exact density-controlled L4-to-L8 record accumulation

## 1. Declared history family

For even `L`, use the inherited periodic record family
`V_L=(Z/LZ)^3`. Pair every cell with even first coordinate to its positive
first-generator neighbor:

\[
 E_L^{\rm act}=\{((2r,y,z),(2r+1,y,z))\},\qquad
 |E_L^{\rm act}|={L^3\over2}.
\tag{B01}
\]

The edges are disjoint and each occurs once. Allocate one fixed-content
writer and one blank retained carrier at every tail, and one blank retained
carrier at every head. Writers, controllers, targets, and complete terminal
reads are distinct tensor factors. This is a conditional prepared family,
not a generic interacting state or selected phase.

## 2. Exact module and tensor product

On each active edge apply the already audited two-stage module:

1. the adopted F3-MDC attachment
   `alpha=r0=14441248/6075`, with
   `epsilon_star=pi/(4r0)`, producing `Phi=pi/4` at the tail;
2. source off;
3. native F3 transfer `H_e=-tT_e` for `t tau/hbar=pi/2`.

Every module yields

\[
 W_e={1\over2},\qquad
 \mathcal J_e={1\over2},\qquad
 (\mathcal R_{\rm tail},\mathcal R_{\rm head})=(0,0),
\tag{B02}
\]

and final retained occupation `1/2` at the head. Disjoint modules commute and
their complete history is the tensor product. Therefore

The normalization `alpha=r0` is replicated from the audited conditional
F3-MDC member. It is not derived from bare F3 and is not refitted at `L=8`.

\[
 Q_L^{\rm final}=W_L=\mathcal A_L={L^3\over4},
\qquad \mathcal R_L=0,
\tag{B03}
\]

where `A_L=sum_(e in E_act)|mathcal J_e|` is the integrated oriented seam
**throughput**, not a net flux through the closed periodic family. The net
global boundary flux is zero because every active seam is internal and enters
the two endpoint ledgers with opposite signs.

Define the microscopic carrier ledger-residual trajectory without continuum
normalization by

\[
 r_1(L)=\sum_{v\in V_L}|\mathcal R_v|,
 \qquad r_\infty(L)=\max_{v\in V_L}|\mathcal R_v|.
\tag{B03a}
\]

Every tail has `0+1/2-1/2=0`; every head has `1/2-1/2=0`. Hence
`r_1(4)=r_infinity(4)=r_1(8)=r_infinity(8)=0`. This maps the exact
record-ledger residual across the expanded finite family. A future nonzero
value is an unclassified term until its owner is determined; it is not
automatically a defect. This quantity is not the continuum Ward diagnostic
`widehat delta(L)` and supplies no infrared exponent.

At `L=4`, `(modules,Q,W,J)=(32,16,16,16)`. At `L=8`,
`(256,128,128,128)`, where the fourth entry is `A_L`. Hence

\[
 {Q_8\over Q_4}=8={8^3\over4^3},\qquad
 {Q_L\over L^3}={1\over4}.
\tag{B04}
\]

This is exact extensive accumulation for the declared fixed-density prepared
history. It does not show spontaneous formation, generic-state accumulation,
interaction stability, a thermodynamic phase, or continuum behavior.

## 3. Record lineage and complete read

There are `L^3/2` independently owned source lineages. Each module has an
explicit finite controller/history factor with complete terminal effects
`{E_OK,E_FAILURE}`, `E_OK+E_FAILURE=I`; any work/reference factor is likewise
read in a complete fixed basis. The ideal declared unitary has failure
probability zero, but the failure outcome remains in the alphabet. Each final
head qutrit has probabilities `(blank,x)=(1/2,1/2)`. The terminal instrument
is the product of the complete qutrit, controller/failure, work, and reference
PVMs across every module. It retains the entire raw outcome string and no
success conditioning is performed.
The expected number of retained occupied lineages is `L^3/4`; the number of
possible lineage-resolved terminal strings is `2^(L^3/2)` on the active
blank/content alphabet.

The covariance is binomial only because this packet declares a tensor-product
preparation:

\[
 \operatorname{Var}(Q_L)={L^3\over8}.
\tag{B05}
\]

It is empirical-model output at this prepared scope, not a universal record
law.

## 4. Disposition

This packet passes R-B's first accumulation census if independently audited:
retained total increases eightfold under an eightfold volume increase, every
active physical seam current is nonzero, and the owner-once ledger remains
exact. No continuum exponent, correlation length, Ward score, or gravity
claim is defined or required.

The raw side-by-side trajectory is:

| quantity | L=4 | L=8 | ratio / disposition |
|---|---:|---:|---|
| cells | 64 | 512 | 8 |
| source lineages | 32 | 256 | 8 |
| expected retained total | 16 | 128 | 8 |
| retained density | 1/4 | 1/4 | fixed |
| absolute oriented seam throughput | 16 | 128 | 8 |
| net periodic boundary flux | 0 | 0 | exact |
| carrier residual `r_1` | 0 | 0 | exact |
| carrier residual `r_infinity` | 0 | 0 | exact |
| prepared variance | 8 | 64 | 8 |

`EXECUTION_CUSTODY.json` records the run on the 48 GiB environment: `0.07 s`
wall time, maximum RSS `11,075,584` bytes (`10.5625 MiB`), peak memory
footprint `7,110,968` bytes (`6.7815 MiB`), and zero swaps. These small
resources are expected because the verifier evaluates exact factorized
combinatorics; it does not allocate a dense `3^512` state vector.

R-C interaction/retention stress remains open. The M-series common physical
parent and all gravity claims remain open.
