# Marked-source finite response engine

This packet executes the hostile-audited localized-write protocol without
placing the localized history in the invalid fully invariant carrier basis.
It uses exactly the order-two stabilizer of source site zero, evolves the
sealed baseline and perturbed histories in the same quotient, reconstructs
every site occupation and every owner-once signed edge current, and retains
the complete vectors beside their finite graph-distance bins.

The engine passes complete direct full-space parity at L6 and L8. The guarded
L10 and L12 response rows pass all structural, baseline-reproduction,
coarse/fine, ledger, norm, energy, number-law, and profile-partition checks.
The combined target passes `23/23`.

The current unaggregated two-history representation is not eligible at L14:
its conservative fixed-width upper bound is `94.89795542508364 GiB`, above
the `40 GiB` process guard on the declared 48 GiB host. No L14 arrays are
allocated and no L14 response value is inferred.

The available L6--L12 rows empirically show nonuniform, signed oscillatory
current response concentrated on the inner finite graph shells. Radius two
has the largest aggregate L1 response at every available size, while the
farthest-shell share falls from about `8.01e-2` at L6 to `2.52e-4` at L12.
This is a finite-window graph-support description, not a locality or scaling
law. No physical distance or physical boundary map has been supplied.

Status: candidate target pending an independent hostile audit. Gate A-P
remains open.

Run:

```text
PYTHONWARNINGS=error python3 -B compute_marked_response.py --length 6
PYTHONWARNINGS=error python3 -B compute_marked_response.py --length 8
PYTHONWARNINGS=error python3 -B compute_marked_response.py --length 10
PYTHONWARNINGS=error python3 -B compute_marked_response.py --length 12
PYTHONWARNINGS=error python3 -B compute_marked_response.py --length 14 --screen-only
PYTHONWARNINGS=error python3 -B compile_response.py
```

The scripts compare against canonical JSON if it is present and fail closed
on any mismatch.
