# Independent hard-barotrope provider preflight V001

2026-09-29. Full read-only review of the standalone header, C source and protocol.
No compiler, import, material evaluation, orbit inversion or numerical producer
was run. This is source/mathematical acceptance, not numerical qualification.

Reviewed bytes:

- `unt_hard_barotrope_v001.h`:
  `abfade89af77e4000bccd169c1ea18226315621f7dcb665901efa879e3a4aab6`
- `unt_hard_barotrope_v001.c`:
  `3003b89d4dcd14a599cf924390b6b4a2151bb14e4221a2336458d89509a3c39d`
- `UNT_HARD_BAROTROPE_PROVIDER_PROTOCOL_V001.md`:
  `308c605954106d70b7376b5665ae2ed2b47725b4a10b663509089ebf539a567a`

## Load-bearing checks

For `q=1+r(1+sin² theta)/2`, the implemented positive quadratures give
`I/R³=(2/pi)r integral cos²(theta)sqrt(q) dtheta` and
`omega/R=pi/[2 integral q^(-1/2)dtheta]`. With period/action weighted means
`alpha=<t>_P`, `bta=<t>_A`, `t=(q-1)/q`,

    d ln I/d ln b = 2+bta,
    d ln omega/d ln b = alpha,
    ca2 = alpha/(2+bta).

The period weight has logarithmic derivative `-t+alpha`; the action weight
has `t-bta`. Thus the two centered-variance formulas have the correct opposite
variance signs, and the implemented `dca2/dln a` includes both the action
chain rule and `dln I/dln a=-3`. The stable pressure and trace formulas avoid
harmonic/quartic subtraction, respectively, and agree with the virial identity.

The action inversion bracket is valid. The two lower bounds on f give
`r_hi=min(2i,2i^(2/3))`; `r_lo=r_hi/4` is below the solution using
`f(r)<=r sqrt(1+r)/2`, separately for `i<=1` and `i>=1`.
The Newton derivative `dln f/dln r=1+bta/2`, bracket checks and explicit
iteration/range failures are consistent. No fitted bracket or state-dependent
dust replacement is introduced.

The retained I1, not supplied e1, determines the orbit. The 2e-10 saved-energy
check and exposed discrepancy bound the declared numerical normalization at
a=1. The density derivatives satisfy

    rho_ln=-3(rho+p), p_ln=ca2*rho_ln,
    rho_lnln=9(rho+p)(1+ca2),
    w_ln=-3(1+w)(ca2-w).

The positive initial-density integral is `ln[rho(a)/rho1]`. I checked its sign
against pinned CLASS `background_w_fld` and the initial-density multiplication
by `exp(integral_fld)`. The supplied stress and RHS agree with the CLASS
non-PPF fluid equations when the rest-frame sound speed equals ca2: the entropy
term vanishes, while the Euler friction becomes `-Hconf(1-3ca2)theta`.
The radiation/matter split `3p` and `rho-3p` is explicitly bookkeeping, not two
populations or permission to omit the hard component from metric sources.

## Interface and scope

The code has no I/O, allocation, process execution, mutable global state or
CLASS dependency. It uses caller-owned immutable contexts, explicit finite
domains and returned error statuses. Undefined ideal-dust orbit coordinates
are NaN by declaration and require labeled nulls in any JSON wrapper; callers
must not use partially written outputs after an error.

The physical normalization preserves the separate vacuum and ordinary species.
The protocol correctly requires candidate changes at background, initialization,
all stress/RHS and matter-output sites, and matching atomic history. Merely
linking this material module or replacing a stock w(a) function is not the
candidate implementation. No arbitrary-Q, native clock, isotropic preparation,
recombination or observational success follows from this preflight.

**Outcome: no load-bearing mathematical or source-interface defect found.**
The prospectively declared Simpson/saved-anchor, quadrature, derivative and
failure tests remain root-owned and unexecuted by this reviewer.
