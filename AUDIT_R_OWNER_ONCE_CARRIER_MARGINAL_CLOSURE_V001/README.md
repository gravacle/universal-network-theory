# Independent hostile audit: owner-once carrier-marginal closure

This directory contains an independently written finite reconstruction of the
candidate exact closure theorem in
[`DEVELOPMENT_R_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_V001`](../DEVELOPMENT_R_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_V001/).
It tests the mandatory `L=4` and `L=6` controls frozen before hostile output.

The hostile code represents the full lineage--carrier state directly and
separately represents the carrier-only channel as an unread Kraus ensemble.
It uses descending integer-word bases and a connector-first reversed edge
traversal.  It imports neither the target verifier nor historical basis,
matrix, or result implementations.

Run the audit:

```sh
PYTHONWARNINGS=error python3 -B \
  AUDIT_R_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_V001/hostile_carrier_closure.py
```

Run the deterministic test suite:

```sh
PYTHONWARNINGS=error python3 -B \
  AUDIT_R_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_V001/test_hostile_carrier_closure.py
```

The sealed hostile disposition is:

```text
PASS_EXACT_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE__FINITE_ACCUMULATION_SCOPE_ONLY
```

The exact maxima are:

| Control | L=4 | L=6 | Frozen limit |
|---|---:|---:|---:|
| Full-versus-reduced disagreement | `2.220446049250313e-16` | `2.220446049250313e-16` | `2e-10` |
| Absolute norm/control error | `4.2033043712308427e-13` | `5.9497962112686764e-12` | `2e-10` |
| Fresh-lineage probability | `0.0` | `0.0` | `2e-10` |

The result establishes the exact carrier marginal for the frozen finite
owner-once accumulation pass when lineage outcomes remain unread.  It does
not erase lineage custody, cover revisits or record-sensitive future
dynamics, establish a thermodynamic limit, or prove any Gate, alpha,
continuum, or gravity claim.

Files:

- `hostile_carrier_closure.py` -- independent reconstruction and reporter;
- `test_hostile_carrier_closure.py` -- deterministic positive and negative
  controls;
- `HOSTILE_RESULT.json` -- canonical machine-readable result;
- `INDEPENDENT_HOSTILE_AUDIT.md` -- method, findings, and exact scope;
- `VERIFICATION.txt` -- commands and captured pass output; and
- `SOURCE_HASHES.sha256` -- final packet hashes.

