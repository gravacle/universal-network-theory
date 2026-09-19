# URM validation baseline — 2026-09-15

## Purpose

This record captures the validation state before the post-September-4 URM
reconciliation. It prevents pre-existing environmental or numerical failures
from being attributed to the release-preparation edits.

## Command

```sh
PYTHONDONTWRITEBYTECODE=1 python3 model/validate_urm.py
```

The command exited `1` after `174.3 s`.

## Passing authoritative gravity surfaces

- `validate_gravity_formation_theory.py`: PASS
- `validate_gravity_microscopic_progress.py`: `247/247` PASS
- `validate_historywise_gravity_discriminant.py`: `84/84` PASS
- `validate_udcl_postulate.py`: `32/32` PASS, natural validity still open
- `validate_project.py`: `24/24` PASS
- `validate_formation_input.py`: `38/38` PASS
- `validate_proof_frontier.py`: `82/82` PASS

## Pre-existing failures

1. The ARROW family reported `26/27` PASS. The failing F-19 system-only-unitary
   invariance check computed `1.643e-14`; its message says it expected the
   sealed printed anchor `3.686e-14`. The surrounding instrument-covariance and
   fixed-label movement controls passed. This reconciliation does not alter the
   numerical arrow implementation.
2. The world-observation input chain could not import the local
   `lakeshore_vsm` adapter and could not find
   `model/checks_lakeshore_vsm.py`. The core world-observation checks still
   reported `28/28` PASS; this input chain carries zero scientific weight.
3. The gamma-flow input chain could not build its synthetic fixture because
   `HANDOFF_2026-08-22.md` is absent from this audited checkout. The chain is
   explicitly marked synthetic with zero proof weight.

## Baseline disposition

The aggregate URM validator is not green before the reconciliation. Release
preparation must therefore report both:

- the targeted validators for every newly changed URM surface; and
- the unchanged aggregate failures above, unless separately repaired and
  audited.

No release gate may represent the pre-existing aggregate state as a clean
all-URM pass. Conversely, these inherited failures do not invalidate the
separate `247/247` sealed microscopic-gravity certificate.
