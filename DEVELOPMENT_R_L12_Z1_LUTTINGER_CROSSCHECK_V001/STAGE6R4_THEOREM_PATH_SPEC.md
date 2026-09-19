# Quarantined Stage6R4 compatibility sketch

Date: 2026-09-16

Status: `QUARANTINED__NOT_A_Z1_PROOF_INPUT__NO_IMPLEMENTATION_AUTHORIZED`

## Why this file is quarantined

An earlier draft tried to express the new z=1 route as a successor to an old
adjudication workflow. That imported machinery which was designed for another
proof surface. It is not needed to decide the physics and must not govern the
primary argument.

In particular, the primary z=1 proof does **not** depend on:

- any earlier Stage6 verdict or closure contract;
- a `THEOREM_PASS` workflow predicate;
- historical fit gates or stop conditions;
- an L10/L12 adjacent-pair requirement;
- a Stage6R4 disposition label;
- registrar, Stage7, URM, or gravity-gate rules; or
- permission to overwrite or reinterpret an older result.

The governing documents are now:

- [`README.md`](README.md), which states the evidence boundary and current
  result;
- [`CONDITIONAL_Z1_BRIDGE_THEOREM.md`](CONDITIONAL_Z1_BRIDGE_THEOREM.md), which
  states the conditional physical theorem; and
- [`analyze_centerline.py`](analyze_centerline.py), which reads the finite data
  through direct pinned hashes without consuming an old verdict.

## Physics hypotheses extracted from the draft

Only the following substantive requirements survived the separation. They are
theorem hypotheses or source-integrity requirements, not adjudicator gates.

1. **Fixed model.** The finite Hamiltonian is exactly the clean periodic
   two-leg hard-core-boson ladder at `t=t_perp=1`.
2. **Fixed observable.** The density observable is explicitly defined and its
   symmetric/antisymmetric decomposition is proved algebraically.
3. **Fixed block.** The only record block in scope is `A009--A016`, with exact
   density interval `[7/48,13/48)`.
4. **Full-domain inclusion.** Every density in every full cell lies inside the
   domain of the adopted physical premise.
5. **Linear visible mode.** The premise or an internal theorem supplies both a
   finite-velocity linear symmetric mode and nonzero thermodynamic overlap with
   the fixed observable.
6. **Independent record statement.** Bounded membership and deduplicated
   `pbar>0.50` are established from the record data separately from `z=1`.

These requirements are restated and proved or labeled in the primary theorem.

## Historical mass table

The numerical facts that motivated the compatibility sketch remain valid, but
their validity comes from the record theorem and direct reconstruction rather
than from this file:

| L | selected q sectors | pbar mass |
|---:|:---|---:|
| 4 | 1--2 | `0.7260206189754993` |
| 6 | 2--3 | `0.5846615608350367` |
| 8 | 2--4 | `0.7373965730354166` |
| 10 | 3--5 | `0.6500987927669427` |
| 12 | 4--6 | `0.5695649839332784` |

This file issues no verdict and defines no future implementation.
