# Hostile audit: L4 + L4 to L8 composition closure

## Verdict

**PASS_HOSTILE_AUDIT_OBSTRUCTION_STOP__EXACT_D8_UNRESOLVED**

This is a pass for the bounded obstruction and mandatory stop boundary only. It is not an exact-rank certification, a scalable truncation rule, or a gravity/emergence result.

## Independent track

The independent computation was frozen before the target result was inspected. It used matrix-free Hermitian Lanczos as the primary solver and a unitary fourth-order Suzuki-Yoshida product formula as the materially distinct cross-solver. A subsequent finer Suzuki record and an owner-current conservation record were also frozen before comparison. Scope was L=4 and L=8 only; no L=6 or L=12 run was performed.

The exact six-remove/six-add surgery maps the two isolated L4 owner sets to the canonical 24-owner degree-three L8 prism. The uniform source factorization error is exactly zero.

## Rank disposition

- L4 has D4=16 with minimum singular value `4.0401508261786266e-6`; it is well separated from the solver discrepancy.
- Both independent solvers give the solver-stable L8 lower bound D8>=251.
- The final modes do not support an exact rank promotion. The target's threshold estimate is 254; the independent absolute-threshold estimates run 251, 253, 255, and 256 across `1e-8` through `1e-14`. These are not forced into agreement.
- Exact D8 therefore remains unresolved in `[251,256]`.
- Retaining D=256 reconstructs the numerical coefficient matrix to the recorded floating-point error.
- The certified obstruction ratios are D8/D4>=251/16=`15.6875` and D8/256>=251/256=`0.98046875`.

The correct promotion is the exponential lower-bound stop rule, not an exact D8 claim.

## Conservation and reconstruction comparison

Independent fine-grid observables agree with the target within:

| L | q Linf | integrated-current Linf | correlation-max difference | tail-checkpoint Linf | independent ledger L1 | target ledger L1 |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 4.3841e-11 | 1.4617e-11 | 8.3811e-13 | 1.5544e-15 | 6.9882e-10 | 7.7729e-10 |
| 8 | 3.3201e-12 | 9.0764e-13 | 2.4602e-13 | 2.2205e-15 | 9.1352e-11 | 1.0103e-10 |

The optimal Schmidt-tail checkpoints agree, and both owner-once ledgers close within the independently recorded integration controls.

## Lower-order boundary collision

The independent audit constructed a lawful finite-block collision from interior roots 1 and 2: identical total Q, port reduced density matrix, incident currents, and port correlations produce a future port-record Linf separation of `0.17085904112241262`. The target adversarial packet independently passes 19/19 using a different collision. This establishes failure of that equal-time lower-order boundary summary. It does not claim that the uniform source selects either adversarial root and is not a process-tensor minimality theorem.

## Claim boundary

Proved here: exact topology, exact source factorization, the Schmidt-minimality identity, and the exact candidate-map rank/nullity and equality of the collision input record.

Empirical/numerically certified: well-separated numerical `D4=16`, the cross-solver-stable numerical lower bound `D8>=251`, reconstruction at `D=256` within recorded floating-point error, future-read collision separation, and the finite-L spectra and conservation observations. Conditional: the finite-L record result under the frozen protocol and adopted microscopic model.

Open: exact D8 within `[251,256]`, larger-L behavior, accumulation-critical behavior, and all continuum/macroscopic response questions. No grid, continuum/Ward axiom, phase, graviton, emergence, or gravity claim is made.
