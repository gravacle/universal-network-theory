# Hostile audit: Gate R-C L8 open-ladder control

This packet independently audits
`DEVELOPMENT_R_GATE_C_L8_OPEN_LADDER_CONTROL_V001`. It imports no target code,
changes no target or authority document, and runs no support larger than L8.

The verifier reconstructs the periodic owner-once L8 prism and removes exactly
`(7,0,rail_1)` and `(15,8,rail_2)`. It independently verifies the open-support
degree and path census, then evolves all eight `B0/P0` through `B3/P3`
histories with a unitary fourth-order Suzuki--Yoshida factorization over three
commuting edge matchings. Separate 1,024/2,048-step runs recompute target-
occupation arrival peaks and the complete integrated current vectors. This is
materially distinct from the target's order-ten Taylor solver.

Run:

```sh
PYTHONWARNINGS=error python3 -B \
  AUDIT_R_GATE_C_L8_OPEN_LADDER_CONTROL_V001/hostile_audit.py
```

The sealed result must finish:

```text
PASS__AUDIT_R_GATE_C_L8_OPEN_LADDER_CONTROL__67/67
```

The audit confirms that `tau_open` is strictly increasing and the periodic
`N=3 < N=2` inversion disappears under the exact two-edge cut. “Ring-mediated”
is retained only as the declared finite periodic-versus-open classification.
Two length-six bypasses remain; subtraction is not lineage; and no metric,
time-dilation, Shapiro-delay, macroscopic-emergence, or gravity claim follows.

