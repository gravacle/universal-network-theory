# URM current validation — 2026-09-16

## Disposition

The current scientific proof surfaces pass their focused validators and their
aggregate URM chains.  The aggregate command is not all-green only because two
ancillary replay contracts refer to historical local files that are absent
from this audited checkout.  Both contracts explicitly carry zero scientific
or proof weight.  No replacement fixture has been invented.

## Aggregate command

```sh
python3 -B model/validate_urm.py
```

Result: exit `1` after `218.4 s` reported by the validator (`218.59 s` real
wall time). This run was performed after the Alpha V002 interval certificate
and the corresponding Gravity Formation role-marker synchronization.

Passing aggregate surfaces:

- T-54 families: `176/176` PASS, with the expected gate census intact.
- ARROW: `27/27` PASS.
- Count law: `40/40` PASS.
- Reachable classes: `52/52` PASS.
- Writing: `57/57` PASS.
- Geometry: `33/33` PASS.
- Project/D-25 chain: `24/24` PASS.
- Generic formation input: `38/38` PASS; scientific weight zero.
- Public-data proof frontier: `82/82` PASS; missing data remains typed and
  authoritative proof output remains zero.
- Physical-alpha role: `121/121` PASS; all seven theorem/audit/witness custody
  pins authenticate, the exact construction-scoped interval is exposed, and
  `ALLOW` / `REQUIRE` / `SELECT` remain separately typed.
- U-DCL: PASS; natural validity remains open.
- Historywise-gravity formal discriminant: PASS; physical and empirical proof
  weight zero.
- Gravity Formation Theory: PASS.
- Gravity microscopic progress: `249/249` PASS.
- Relational accumulation and `ARGER-GATE-1`: `174` checks PASS.

The aggregate failure is limited to these unavailable historical replay
inputs:

1. **World-observation adapter replay — zero scientific weight.**
   `model/checks_lakeshore_vsm.py` and `model/lakeshore_vsm.py` are absent.
   The underlying world-observation core still reports `28/28` PASS, but the
   adapter and public-door replay cannot be completed without those files.
2. **Synthetic gamma-flow replay — synthetic proof weight zero.**
   The fixture builder pins thirteen framework documents plus its principal
   decision document.  Those fourteen files are absent from this checkout, so
   neither the core synthetic fixture nor its public URM delegation can be
   reconstructed.  The first missing file reported is
   `HANDOFF_2026-08-22.md`.

These missing inputs are not used by the physical-alpha role certificate,
`ARGER-GATE-1`, the finite/discrete GFT `z=1` certificate, the exact L4--L12
record-block theorem, the microscopic-gravity progress layer, or the
record-first conditional Gravity Formation Theory.
They are retained as explicit reproduction debts rather than replaced with
newly fabricated content.

## Focused release checks

The following focused commands were also run on the same working tree:

```sh
python3 -B model/validate_relational_accumulation.py
python3 -B model/validate_relational_provenance_archive.py
python3 -B -m unittest DEVELOPMENT_R_ARGER_GATE_V001/test_arger_gate.py
python3 -B model/validate_alpha_role.py
python3 -B model/validate_gravity_formation_theory.py
python3 -B model/validate_gravity_microscopic_progress.py
python3 -B model/validate_udcl_postulate.py
python3 -B model/validate_project.py
python3 -B proofsrc/assemble.py
python3 -B replicate/check_proof.py PROOF_V002.md
```

Results:

- Governing relational certificate: `174` checks PASS.
- Separate Git-only relational provenance archive: `75` checks PASS.
- `ARGER-GATE-1` unit tests: `2/2` PASS.
- Physical-alpha role certificate: `121/121` PASS.
- Gravity Formation Theory: PASS.
- Gravity microscopic progress: `249/249` PASS.
- U-DCL: `34/34` PASS; natural validity remains open.
- Project model: `24/24` PASS.
- Generated proof gate: PASS across `89` claim blocks and `120` distinct cited
  rows; all ten proof-contract rules pass.

The governing relational module and validator contain no reference to the
retired classifier, adjudication, or equivalence machinery.  Historical
provenance is isolated in `model/relational_accumulation_historical.py` and
`model/validate_relational_provenance_archive.py`; it is not part of the public
URM certificate or the Zenodo governing closure.

## Release meaning

This record supports a review-ready release of the current proof surfaces.  It
does not represent a completely green replay of every historical auxiliary
fixture ever named by the repository.  The two unavailable zero-weight replay
contracts must remain disclosed in the Git history and excluded from any claim
that the entire historical corpus is reproducible from this checkout.
