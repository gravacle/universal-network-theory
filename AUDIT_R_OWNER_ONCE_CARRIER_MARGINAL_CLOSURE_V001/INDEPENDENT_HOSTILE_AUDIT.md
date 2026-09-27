# Independent hostile audit -- exact owner-once carrier marginal

Date: 2026-09-22

## Verdict

```text
PASS_EXACT_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE__FINITE_ACCUMULATION_SCOPE_ONLY
```

The independently reconstructed `L=4` and `L=6` controls pass every frozen
condition.  The maximum full-versus-reduced disagreement is
`2.220446049250313e-16` at both sizes.  The maximum absolute norm/control
errors are `4.2033043712308427e-13` at L4 and
`5.9497962112686764e-12` at L6.  Every pre-admission fresh-lineage
probability is exactly zero in the executed basis.

This is the hostile packet's disposition.  Final cross-packet promotion under
the frozen protocol also requires the separately maintained finite target to
agree with the analytic theorem; this audit does not read target results.

## 1. Question tested

For the frozen owner-once first pass, compare:

1. the complete joint lineage--carrier evolution; and
2. the carrier-only evolution under the unread channel

   ```text
   K0 = P_occupied + cos(phi) P_blank
   K1 = -i sin(phi) a_event^dagger P_blank.
   ```

The hostile calculation asks whether tracing the joint lineage register gives
exactly the second evolution after every admission and at every transport
checkpoint.  Closed carrier transport without this channel is a deliberately
wrong comparator, not the matched null.

## 2. Independent reconstruction

The executable reconstructs from the frozen written protocols:

- a two-rail periodic prism with one connector per site;
- fixed-particle carrier sectors in descending integer-word order;
- fixed-weight lineage sectors in the same independently chosen descending
  order;
- connector edges before rail edges, each in reverse site order;
- full admission as a two-child rotation in joint lineage--carrier amplitudes;
- reduced admission as separately stacked `K1` then `K0` Kraus factors;
- matrix-free hopping action and order-12 Taylor transport over 16 substeps;
  and
- Simpson-integrated oriented edge currents for actual and null histories.

The hostile program does not import the target verifier, target matrices,
target basis maps, historical executable matrices, or target result values.
Only the frozen theorem and protocol documents are hashed as dependencies.
All paths in the JSON result are repository-relative; it contains no host,
timestamp, or absolute-path field.

## 3. Mandatory observations

At initialization and after every admission and transport, the reconstruction
compares:

- complete reduced carrier blocks sector by sector;
- Hilbert--Schmidt residuals;
- factor singular values;
- an explicit dense trace distance at L4 and a factor/Frobenius trace bound at
  L6;
- sharp-particle-number weights;
- all site occupations;
- all instantaneous oriented currents; and
- actual, null, and actual-minus-null integrated currents.

For every event it separately records ALLOW, blocked, and expected-write
disagreements, fresh-lineage probability, per-branch norm drift, and absolute
post-admission and post-transport norm errors.  The Taylor-tail bound is
`4.328375076759148e-16` and is kept separate from model disagreement.

## 4. Numerical findings

| Quantity | L=4 maximum | L=6 maximum |
|---|---:|---:|
| Reduced carrier Hilbert--Schmidt residual | `0.0` | `0.0` |
| Explicit reduced-state trace distance | `0.0` | not densely evaluated |
| Trace-distance upper bound | `0.0` | `0.0` |
| Factor singular-value residual | `2.220446049250313e-16` | `1.942890293094024e-16` |
| Sector-weight disagreement | `0.0` | `5.551115123125783e-17` |
| Occupation disagreement | `0.0` | `0.0` |
| Instantaneous-current disagreement | `2.7755575615628914e-17` | `5.551115123125783e-17` |
| ALLOW disagreement | `0.0` | `2.220446049250313e-16` |
| Blocked disagreement | `0.0` | `2.220446049250313e-16` |
| Expected-write disagreement | `0.0` | `0.0` |
| Actual integrated-current disagreement | `2.7755575615628914e-17` | `2.7755575615628914e-17` |
| Null integrated-current disagreement | `2.7755575615628914e-17` | `1.3877787807814457e-17` |
| Delta integrated-current disagreement | `2.7755575615628914e-17` | `2.7755575615628914e-17` |
| Absolute norm/control error | `4.2033043712308427e-13` | `5.9497962112686764e-12` |

All required observables and all required events are present and finite.  Both
mandatory sizes clear the frozen `2e-10` thresholds by wide margins.

## 5. Negative control

The test suite compares the first admitted joint state with a carrier ladder
that received no `K0/K1` channel.  Both its trace-distance and sector-weight
disagreements exceed `0.1`.  The audit therefore detects the known-wrong
closed-ladder comparator rather than passing every implementation
indiscriminately.

## 6. Exact conclusion and boundary

The results confirm the theorem's finite operational content: during the
declared owner-once pass, the lineage register is a Stinespring record of the
admission outcomes, and every unconditional carrier observable is reproduced
by the matched unread channel.  Explicit lineage remains indispensable for
custody, selected-mask questions, lineage-conditioned states, and joint
correlations.

The audit does not cover a revisit, a lineage-dependent event schedule,
postselection, or any later Hamiltonian or measurement that reads a retained
record.  In particular, it does not reduce the separate record-sensitive
GL6T construction.  It proves no Gate, Record--Geometry Realization Law,
alpha statement, thermodynamic limit, continuum result, or gravity theorem.

