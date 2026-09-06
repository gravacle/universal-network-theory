# Marked-source response run observations

Environment for the guarded executions:

- declared host memory: 48 GiB;
- operating system/architecture: `Darwin 25.4.0 arm64`;
- interpreter: `Python 3.9.6`;
- observed Numba worker count: 14;
- environment: `PYTHONWARNINGS=error`.

Passing single-process observations:

| L | checks | observed runtime (s) | observed maximum RSS (bytes) |
|---:|---:|---:|---:|
| 6 | 35/35 | 5.211946500 | 129,122,304 |
| 8 | 35/35 | 8.818417792 | 147,275,776 |
| 10 | 29/29 | 80.036708375 | 412,352,512 |
| 12 | 29/29 | 954.524951709 | 4,980,539,392 |

The L10 canonical custody replay separately observed `79.984204000 s` and
`411,189,248` bytes. These are single-environment telemetry records, not
runtime or memory-complexity laws.

The L14 screen passes its five structural/custody checks but rejects
execution under the current representation: `94.89795542508364 GiB`
conservative numeric-payload upper bound versus the `40 GiB` process guard.
No L14 response arrays were allocated.

One initial L6 validation attempt failed closed at `33/34` because it required
the perturbed current to vanish immediately after transport was restored.
That requirement confused the terms-off write slice with the later
terms-restored slice: the authenticated phase insertion lawfully gives an
instantaneous restored current of magnitude `0.5`. The validator was narrowed
to require zero restored current only for the baseline and finite current for
the perturbed history. No intervention, evolution, response value, or emitted
canonical result was changed or promoted from the failed attempt.
