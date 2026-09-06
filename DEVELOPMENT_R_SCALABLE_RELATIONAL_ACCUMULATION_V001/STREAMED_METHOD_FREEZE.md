# Streamed L10/L12 history method gate

## Scope

This gate replaces the seed calculation's global action-list representation
with two exact sharp-number block representations. It changes numerical
propagation only. The physical parent, graph, admission operator, dwell,
observables, sector rule, thresholds, and claim boundary remain those frozen
in `PROTOCOL.md`.

The target orders basis states by spent genesis mask and carrier word and uses
an adaptive Hermitian Lanczos exponential action. The independent method uses
reversed combination order, a different edge order, and a
Gershgorin-scaled Chebyshev polynomial Krylov action. Neither imports the
other's code or matrices. Both retain all

```text
D_L = binomial(3L,L)
```

basis states. Sharp carrier-number blocks are exact invariant blocks during
transport. Genesis rows are streamed through memory-bounded batches; batching
does not identify, delete, average, or truncate states.

For each event, both implementations independently evolve actual and
null-admission histories, integrate every oriented edge current, reconstruct
the node continuity residual, and retain the exact sharp-q weights. Target
coarse/fine and blind rough/sharp propagations are separate histories.

## Frozen numerical controls

Target:

- adaptive Lanczos dimensions `12,18,24,32,48` (coarse) and
  `16,24,32,48,64` (fine);
- endpoint exponential-action differences `2e-9` and `5e-11`;
- Gauss-Legendre current orders `16` and `24`; and
- at most `1,400,000,000` bytes of retained Krylov basis per row batch.

Independent:

- Chebyshev degrees `16,24,32,48,64,80` (rough) and
  `24,32,48,64,80,96` (sharp);
- endpoint differences `3e-9` and `8e-11`, with a 32-term Bessel-tail
  convergence indicator;
- Gauss-Legendre current orders `18` and `28`; and
- at most `1,400,000,000` bytes of polynomial basis per row batch.

L4/L6/L8 validation must reproduce the already sealed histories within
`2e-8`, target and blind must agree within `1e-8`, and all original ledger and
sector gates remain in force. A method that does not converge at its frozen
cap returns `UNRESOLVED`; the cap is not enlarged after L10 output.

## Resource decision

The measured block-kernel benchmark and complete L8 validation are inputs to
a twofold-safety L10 projection. L10 may start only if each projected method
is below the original two-hour and 4-GiB limits. Actual L10 telemetry is
authoritative and can still fail the gate.

L12 remains separately fail-closed. The frozen protocol requires at least
`60 GiB` free scratch before it starts. A failed free-space check is recorded;
it is not bypassed through truncation, compression, deletion, or a relaxed
guard. No L12 output may be generated until both the L4--L10 physics gate and
this environmental guard pass.

This method gate makes no claim about a critical sector, scale-free response,
continuum behavior, emergence, or gravity.
