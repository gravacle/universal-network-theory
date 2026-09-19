# URM post-reconciliation validation — 2026-09-15

> **HISTORICAL VALIDATION SNAPSHOT — SUPERSEDED FOR CURRENT STATUS ON
> 2026-09-16.** The command results below remain dated validation evidence, but
> their scientific-status language is not current authority. Use
> [`README.md`](README.md), [`PROOF_GUIDE.md`](PROOF_GUIDE.md), the adopted
> finite Gate in
> [`ARGER_GATE_ADOPTION_2026-09-16.md`](ARGER_GATE_ADOPTION_2026-09-16.md),
> and [`L14_RUN_DISPOSITION_2026-09-16.md`](L14_RUN_DISPOSITION_2026-09-16.md).
> L14 is `INCOMPLETE_PRESERVED_NO_SCIENTIFIC_RESULT`.

## Purpose

This record captures the aggregate and focused validation state after the
post-September-4 URM reconciliation was applied in the working tree.  It must
be read with
[`URM_VALIDATION_BASELINE_2026-09-15.md`](URM_VALIDATION_BASELINE_2026-09-15.md),
which records the inherited red inputs before these edits.

The result is intentionally not described as an all-green URM run.  The full
validator exits nonzero for the same three inherited conditions in the
baseline; the newly added Gravity Formation Theory and relational-accumulation
surfaces pass their focused and chained checks.

## Aggregate command and result

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B model/validate_urm.py
```

Executed from the repository root on 2026-09-15 local time
(2026-09-16 UTC).  The latest aggregate command exited `1` after `173.5 s`.

- T-54 family gates: `175/176` PASS, with the declared `176/176` gate census
  intact.
- Geometry/project chain: PASS (`33/33` geometry and `24/24` project checks).
- Formation-input chain: PASS (`38/38`; zero scientific weight).
- Proof-frontier chain: PASS (`82/82`; missing data remains typed and carries
  zero authoritative proof output).
- U-DCL chain: PASS (`32/32`; natural validity remains open).
- Historywise-gravity discriminant: PASS (`84/84`; zero physical or empirical
  proof promotion).
- Gravity Formation Theory gate: PASS.
- Sealed microscopic-gravity progress: PASS (`247/247`).
- Relational-accumulation gate: PASS (`205` checks), with Stage 7 false at L12
  and L14 still `PENDING_AUTHENTICATED_RESULT`.  The certificate keeps the
  Phase-2 reachability authorization, authenticated Phase-3 q8/q9 state, and
  final conservative finite-scout decision separately typed; pending decisions
  are `None`, not false verdicts.

## Inherited failures reproduced unchanged

1. **ARROW F-19 printed-anchor mismatch.**  ARROW remains `26/27`: the
   system-local-unitary invariance calculation gives `1.643e-14`, while the
   check asks for the sealed printed corroboration anchor `3.686e-14`.  Its
   neighboring covariance and fixed-label movement controls pass.
2. **World-observation local adapter absent.**  The zero-scientific-weight
   input chain cannot import `lakeshore_vsm` and cannot find
   `model/checks_lakeshore_vsm.py`; its core world-observation checks still
   report `28/28` PASS.
3. **Synthetic gamma-flow fixture input absent.**  The zero-proof-weight
   synthetic chain cannot find `HANDOFF_2026-08-22.md` in this audited
   checkout.

These are the same three conditions recorded before reconciliation.  This run
therefore found no new aggregate failure attributable to the Gravity Formation
Theory, relational-accumulation, proof-guide, or Zenodo-preparation work.

## Focused release-preparation checks

The focused checks were also run independently:

```sh
python3 -B model/validate_gravity_formation_theory.py
python3 -B model/validate_relational_accumulation.py
python3 -B model/validate_gravity_microscopic_progress.py
python3 -B model/validate_udcl_postulate.py
python3 publication/zenodo_reproduction_v001/sanitize_l12_release_inputs.py check
python3 publication/zenodo_reproduction_v001/build_capsule.py
python3 -m unittest \
  publication/zenodo_reproduction_v001/test_build_capsule.py \
  publication/zenodo_reproduction_v001/test_sanitize_l12_release_inputs.py
```

Results:

- Gravity Formation Theory: PASS.
- Relational accumulation: PASS (`205` checks).
- Microscopic progress: PASS (`247/247`).
- U-DCL: PASS (`32/32`), natural validity open.
- Deterministic L12 release-input sanitizer: `CHECK OK`, covering five
  sanitized public objects plus their aggregate provenance record.
- Zenodo capsule preparation check: `CHECK OK` in `PREPARATION` mode with
  `1,433` selected files, `281,260,782` bytes, and ten explicitly expected release
  inputs still pending.  `L02_CANONICAL_SELECTION.json` is present; the ten
  remaining inputs are:
  `CLEAN_REPRODUCTION_RESULT.json`, `L14_BRANCH_SOURCE_CUSTODY.json`,
  `L14_GATE_DECISION.json`, `L14_HOSTILE_RESULT.json`,
  `L14_RUN_PROVENANCE.json`, `L14_TARGET_RESTART_PROVENANCE.json`,
  `L14_TARGET_RESULT.json`, `LICENSE.txt`, `RELEASE_NOTES.md`, and
  `URM_VALIDATION_RESULT.json`.
- Full publication suite: `72/72` PASS, including `29/29` combined
  capsule-builder and sanitizer tests.

## Release disposition

The reconciliation itself is validated against the inherited baseline, but a
release must not claim that every URM input chain is green.  The L14 scientific
seam also remains closed until authenticated Target and Hostile outputs, merge,
the Phase-2 reachability authorization, authenticated Phase-3 q8/q9 evidence,
and the separate final conservative q-deduplicated finite-scout adjudication
exist.  Phase 2 alone cannot promote the L14 row, and a final finite-scout pass
would still not be an exact/asymptotic `z=1` emergence theorem.  No console
observation or branch-local intermediate may change that state.
