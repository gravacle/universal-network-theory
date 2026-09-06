# Intrinsic Admission Parent L4 result V001

## Result

```text
PASS_L4_INTRINSIC_ADMISSION__COHERENT_UNWRITING_ELIMINATED_ON_DECLARED_TRACE
```

The four-event one-pass relational trace passes all `10/10` target checks.
The independent dense-eigensystem reconstruction passes `12/12` checks and
agrees with the matrix-free target within `8.438e-15`.

| event | cursor vertex | `ALLOW` probability | blocked probability | `W_n` |
|---:|---:|---:|---:|---:|
| 1 | 0 | `1.000000000000` | `0` | `0.500000000000` |
| 2 | 1 | `1.000000000000` | `2.511e-30` | `0.500000000000` |
| 3 | 2 | `0.971605142431` | `0.028394857569` | `0.485802571216` |
| 4 | 3 | `0.895574041014` | `0.104425958986` | `0.447787020507` |

For every event,

```text
W_n = sin^2(pi/4) * Pr(ALLOW)
```

within `1.11e-16`. The occupied-target component is dynamically nonzero by
event 3 and reaches `0.104425958986` at event 4, so the null control is not
vacuous. Nevertheless, the norm of `(U_A-I)` on every blocked component is
exactly zero. No event has negative retained uptake, and every fresh cell has
zero reverse-support probability before its one allowed use.

## Ownership and resource accounting

The maximum residual among

```text
Delta Q_retained + Delta Q_genesis,
Delta B + W_n,
Delta L_sealed - W_n,
target owner balance,
genesis-cell owner balance
```

is `4.441e-16`. After four events,

```text
Q_retained = 1.933589591722506
Q_genesis  = 2.066410408277482
Q_total    = 3.999999999999988
```

Thus the new retained records are transferred from the internal connected
genesis cluster; no external content source exists. The expected depleted
bandwidth and sealed-lineage count both equal `1.933589591722513` within
roundoff.

The largest native-transport node-ledger L1 residual is `2.389e-10`, maximum
transport number drift is `3.331e-15`, and maximum norm error is `3.220e-15`.
The target used `24,657,920` bytes peak RSS and `2.490` seconds wall time on
the recorded environment.

## Interpretation

The negative third-write value `-0.284066355058273` in the sealed same-port
history was caused by coherently re-driving a previously used source-target
pair. In the revised parent, admission is a Hermitian exchange between a fresh
loaded internal cell and a blank retained target component. Occupied target
components lie exactly in the generator's kernel, while an internal one-pass
cursor prevents a spent cell from being driven in reverse. The negative-write
mechanism is therefore absent on this declared trace without measurement,
clipping, an external reservoir, or a nonunitary rule.

This construction does not make `ALLOW`, `REQUIRE`, or `SELECT` dynamical
operators. `ALLOW` classifies the represented configurations; the separately
defined local exchange supplies the motion; `REQUIRE` audits accepted-branch
lineage and cost; and `SELECT` describes the trajectory selected by the full
parent and initial state.

**Proved for the declared finite parent and trace:** occupied-target admission
components are exact null transitions; the four signed retained uptakes are
nonnegative; complete content, admission bandwidth, lineage, and owner-once
transport accounting close within the displayed guards.

**Adopted:** the uniform three-state admission cell, connected four-cell
genesis initial condition, one-pass internal cursor, `Phi=pi/4`,
`kappa=pi/2`, and finite L4 trace length.

**Empirical/numerically certified:** the table, finite transported state,
resource telemetry, and target/independent agreement.

**Open:** repeated autonomous genesis after one cursor pass; a scalable exact
representation of the complete lineage parent; an L4--L12 common accumulation
sector; criticality or `z=1`; macroscopic closure; universal coupling;
non-contact long-range response; metric/action dynamics; background
independence in a continuum sense; emergence; and gravity.

No grid, privileged boundary, external reservoir, absolute global clock,
graviton, Ward axiom, continuum assumption, Gate B promotion, emergence, or
gravity claim is introduced.
