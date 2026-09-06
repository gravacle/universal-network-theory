# Localized authenticated-write response protocol V001

This packet defines the finite perturbed-minus-baseline response to the
smallest already authenticated source write: `W_R=1/2`,
`r0=14441248/6075`, `Phi=pi/4`. The write acts on one baseline-blank even
carrier site while connected transport is off; the source then turns off and
the original owner-once connected support evolves at `kappa=pi/2`.

Run:

```sh
PYTHONWARNINGS=error python3 -B verify_protocol.py
```

The verifier must finish with
`PASS__R_GATE_AP_LOCALIZED_SOURCE_RESPONSE_PROTOCOL__20/20`.

The protocol defines complete signed occupation/current differences and an
edge-shell profile by finite support-graph distance. Localization breaks the
full symmetry of the uniform baseline, so execution requires a marked-source
or equivalent noninvariant-sector engine, full-space L6/L8 validation, and a
separate resource screen at each larger size. L14 may not be forced.

The unperturbed values near `0.5213/0.1682` are an empirical finite-window
reference only. No asymptotic plateau, response result, physical grid or
distance, scaling law, continuum, Ward structure, phase, graviton, or gravity
is claimed.
