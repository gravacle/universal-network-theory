# Correlation-only record: exact two-component toy investigation

Date: 2026-10-28

Status: **Exploratory checked quantum toy model. Not an UNT theorem, a physical implementation, or an electromagnetism derivation.**

## Question and assumed primitives

Can a supplied input-event bit be written into two components so that neither component alone reveals it, but a fixed source-blind read of their correlations retrieves it after an isolated hold?

Assume two abstract qubits, ordinary tensor-product quantum mechanics, the blank state `|00>`, a controllable preparation and write, a specified interacting hold Hamiltonian, and an available joint read. These operations and interactions are supplied assumptions. No electromagnetic field, current, Maxwell action, visible charge, or value of alpha is assumed or derived.

## Complete write–hold–read specification

1. **Common blank and preparation:** begin with `|00>`. Apply a Hadamard to A and a controlled-NOT from A to B. This yields `Phi+ = (|00> + |11>)/sqrt(2)` for either possible input event.
2. **Event-dependent write:** an externally supplied classical bit `e` selects `(Z_A)^e`. The written state is `Phi+` for `e=0`, and `Phi- = (|00> - |11>)/sqrt(2)` for `e=1`.
3. **Source isolation:** disconnect that event source after writing. Neither the subsequent hold nor the read receives `e` or accesses the source.
4. **Fixed hold:** evolve under `H_hold = 1.0 X_A X_B + 0.3 Z_A Z_B`, with dimensionless time and hbar equal to one. This is a nontrivial interacting Hamiltonian. The two record states are eigenstates with energies `1.3` and `-0.7`, respectively, so their density matrices remain fixed for every hold time.
5. **Fixed read:** measure the two projectors `(I + X_A X_B)/2` and `(I - X_A X_B)/2`. Decode plus as zero and minus as one. Equivalently, measure each component in the X basis and compare parity; either local outcome alone is uninformative.

## Actual checked results

The script computes density matrices, partial traces, trace distances, matrix-exponential evolution, and fixed-read probabilities using NumPy and SciPy.

| Quantity | Exact result |
|---|---:|
| Joint trace distance between the two written records | 1 |
| Trace distance between the two A-component states | 0 |
| Trace distance between the two B-component states | 0 |
| Fixed-read output contrast | 1 |
| Equal-prior correct decoding probability | 1 |

Each local density matrix is `I/2`. The event bit is wholly in correlations within this accessible two-component record. Ideal hold was numerically checked at `t = 0, 0.5, 1, 2, 5, 10`. Correct decoding and fidelity with the respective written state remain one to floating-point precision; the eigenstate relation establishes ideal preservation for all times.

## One declared noise comparison

Apply an event-independent phase-flip channel to A after the hold:

`rho -> (1-p(t)) rho + p(t) Z_A rho Z_A`, with `p(t) = (1-exp(-0.2 t))/2`.

For this state family the same result follows from continuous local dephasing during the hold: all intermediate mixtures commute with `H_hold`. Joint trace distance and fixed-read contrast are `exp(-0.2 t)`, while local trace distances remain zero. Correct decoding is `(1+exp(-0.2 t))/2`.

| Dimensionless hold time | Joint distance / contrast | Correct decoding |
|---:|---:|---:|
| 0 | 1.000000000 | 1.000000000 |
| 0.5 | 0.904837418 | 0.952418709 |
| 1 | 0.818730753 | 0.909365377 |
| 2 | 0.670320046 | 0.835160023 |
| 5 | 0.367879441 | 0.683939721 |
| 10 | 0.135335283 | 0.567667642 |

Under this assumed noise model, correct decoding stays at least 0.9 through `t = -ln(0.8)/0.2`, approximately `1.115717757`. These are dimensionless toy times, not measured physical lifetimes.

Maximum analytic-metric discrepancy was `7.771561172376096e-16`; maximum trace/Hermiticity/positivity sanity discrepancy was `8.881784197001252e-16`, within the declared `1e-12` guard. Runtime versions: NumPy `2.3.5`, SciPy `1.17.0`.

## Interpretation and limits

This is an explicit record **of a supplied input event**, written into a common prepared system and later readable without its source. It demonstrates that event information can reside in joint correlations while both local states are identical. It does not create information from nothing or explain the origin of the input event, qubits, preparation, write rule, interaction, read apparatus, or underlying quantum dynamics.

The model does not derive any of these primitives from UNT; close control, work, or energy accounting; establish autonomous record genesis; or generate electromagnetic dynamics. Its ideal durability uses an eigenstate encoding under the stipulated Hamiltonian. Its noisy survival result is specific to the declared phase-flip model and is not a general robustness claim.

## Reproduction

Run `python correlation_record.py` with NumPy and SciPy installed. It writes `correlation_record_results.json` beside the script and prints a compact summary. The optional `--output PATH` argument selects another JSON destination.
