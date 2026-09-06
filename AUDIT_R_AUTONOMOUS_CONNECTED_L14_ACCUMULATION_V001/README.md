# Independent hostile audit: connected L14 accumulation

This packet repairs the prior fail-closed audit by executing a separate,
memory-bounded L14 numerical reconstruction. The implementation imports no
target or inherited engine function.

It uses compiled generator-BFS orbit assignment, fixed-width aggregated CSR
Hamiltonian/current rows, representative-only diagonals, and classical RK4
with coarse/fine Simpson current quadrature. L4 formulas are first checked
against the full 256-word space.

Run the saved-result verifier:

```sh
PYTHONWARNINGS=error python3 -B AUDIT_R_AUTONOMOUS_CONNECTED_L14_ACCUMULATION_V001/verify_audit.py
```

Replaying `independent_reconstruction.py` is a roughly 22-minute single-host
calculation. The result is conditional microscopic numerical evidence only.
