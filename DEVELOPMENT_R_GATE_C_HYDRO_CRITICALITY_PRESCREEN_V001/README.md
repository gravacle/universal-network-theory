# R Gate C hydrodynamic criticality pre-screen target

This directory contains the frozen protocol and target implementation for the
exact-through-L8 spectral seed screen.

Run from this directory with:

```bash
PYTHONWARNINGS=error python3 -B compute_seed_screen.py
```

The driver verifies the protocol digest, runs one fixed-`q` dense
diagonalization at a time, retains each complete spectrum under `RAW/`, and
discards eigenvectors before moving to the next sector.  Child workers use
the available 12-GiB resource limits and the driver enforces the 45-minute
wall limit.  The executable contains no L10/L12 calculation and always stops
after the L4/L6/L8 seed decision.

`RESULT.json` is the machine-readable summary, `RESULT.md` is the human
summary, and `RUN_OBSERVATION.md` records the environment-specific resource
observation.  The result awaits an independently frozen hostile replay before
any promotion.
