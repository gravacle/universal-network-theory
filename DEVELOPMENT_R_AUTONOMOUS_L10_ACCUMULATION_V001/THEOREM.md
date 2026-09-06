# L10 finite autonomous BS09 accumulation rung

## 1. Exact reduction and census

Continue the hostile-audited source-off BS09 trajectory on the same
conditional cycle program. At L10 there are 1,000 carrier sites split into
two F3 layers of 500, 250,000 possible adjacent-layer links, and 1,000 active
cycle edges. The support factors into 100 disjoint ten-site cycles. The
F3-MDC source preparation supplies 500 lineages at half expected occupation,
so the expected retained total is 250.

The alternating preparation, cycle Hamiltonian, and terminal observables are
invariant under translation by two sites. Reflection reverses oriented current
and removes the uniform circulation component. The integrated continuity law

\[
 \Delta q_i+J_i-J_{i-1}=0                            \tag{L10-01}
\]

then fixes

\[
 J_i=-{1\over2}\Delta q_i.                          \tag{L10-02}
\]

Before using (L10-02), the verifier applies it to every directly integrated
edge current in all 30 hostile-audited L4/L6/L8 `kappa` rows. The maximum
absolute difference is recorded in `RESULT.json` and must remain below
`8e-12`. Thus the L10 reduction is checked against the lower-size owner-once
current computation rather than assumed from occupation conservation alone.

## 2. L10 records

The ten-point `kappa=t tau/hbar` list is unchanged:
`0, pi/16, pi/8, pi/4, 3pi/8, pi/2, 3pi/4, pi, 3pi/2, 2pi`.
At zero the integrated currents vanish. At every positive sampled value all
ten supports per cycle carry nonzero oriented current. Expected retained total
stays 250, and the full carrier-number law is conserved.

`RESULT.json` records every L10 occupation/current vector, raw throughput,
connected correlation, record-ledger residual, norm/energy/number control,
and the L10/L8 throughput ratios. The computation also records runtime and
maximum resident set on the 48 GiB environment. It uses the exact product of
100 identical disjoint cycle histories; it does not allocate or imply a
global `2^1000` wavefunction.

| `kappa` | L10 throughput total | per retained record | L10/L8 per-record ratio |
|---:|---:|---:|---:|
| `0` | `<7.78e-14` roundoff | `<3.11e-16` | undefined at zero |
| `pi/16` | 27.698301 | 0.110793 | 1.000000 |
| `pi/8` | 97.212552 | 0.388850 | 1.000000 |
| `pi/4` | 223.709514 | 0.894838 | 1.000000 |
| `3pi/8` | 176.521896 | 0.706088 | 0.999999 |
| `pi/2` | 61.480350 | 0.245921 | 0.999901 |
| `3pi/4` | 174.997337 | 0.699989 | 0.996452 |
| `pi` | 82.926232 | 0.331705 | 0.932373 |
| `3pi/2` | 96.311751 | 0.385247 | 1.647847 |
| `2pi` | 91.862740 | 0.367451 | 0.867804 |

The exact zero-`kappa` current is zero; the displayed raw value is the
eigendecomposition roundoff and lies below the `1e-12` active-current
threshold. The current reduction differs from all directly integrated lower
size currents by at most `5.829e-16`. L10 raw residual maxima are
`1.763e-15` L1 and `3.470e-16` Linf per cycle, with tiled L1 bound
`1.763e-13`. Norm, energy, and number-law errors stay below
`8.882e-16`, `1.051e-15`, and `4.441e-16`.

The frozen 48 GiB execution observation records `0.4769145 s` runtime and
`80.53125 MiB` maximum RSS. These are environment/run observations, not exact
or universal complexity claims.

Degenerate numerical eigenspaces can change last-bit floating ordering across
BLAS runs. `RESULT.json` therefore freezes one raw canonical run; replay
recomputes all fields and accepts only differences below `8e-12` rather than
claiming byte-identical floating output. The frozen observation is not rounded
or silently replaced on replay.

## 3. Claim boundary

**Proved:** the L10 census and disjoint-cycle factorization; the
period-two/reflection current reduction; retained-total and number-law
conservation; and the cellwise owner-once continuity identity.

**Adopted:** the inherited F3-MDC attachment `alpha=r0`.

**Conditional:** the fixed cycle support, sampled `kappa`, separate hopping
and clock calibration, content sector, source routing, and complete read.

**Empirical/numerical:** the ten L10 trajectory rows, L10/L8 ratios, residuals,
correlations, and execution resource record.

**Open:** autonomous support and coefficient/clock selection; connected-cycle
accumulation under a physical parent; generic phase behavior; and all
macroscopic response questions.

Residuals are raw unassigned record-ledger terms, not physical defects. The
enumeration labels are not a physical grid. No continuum behavior, Ward
identity, mature macro dynamics, graviton, or gravity is inferred.
