# REVIEW_RECORD_0354_V001: independent review of the floating-point warning diagnosis and inert patch proposal

**Task:** Codex1 0354.

| Role | Who |
|---|---|
| Author | CLAUDE2 main lane: diagnosis, patch proposals V003/V004/V005, evidence, addendum |
| Independent reviewer | Claude helper ab750e45705a5599e (wrote none of the reviewed code) |

## Round 1: diagnosis V001 + proposal V003 + evidence V003. Verdict PASS_WITH_NOTES

**Hashes.** All 11 files matched. `diff.v2` matched the real V002→V003 change. The saved-run metadata the reviewer read (warnings, environment and pins only) matched the diagnosis: 1008 warnings per case, and the 50 retained entries split 13/12/13/12 across the four kinds.

**(a) Diagnosis: correct.**
- The reviewer re-ran diagnostics v001 and v002; every flagged pair and every exact result reproduced.
- The reviewer's own generic probes added:
  - the dtype and output-shape dependence;
  - random floats at 0.09–0.14 of the γ_k bound against exact Fraction arithmetic;
  - flags are not sticky;
  - genuine overflow, NaN and underflow at N = 16 raise all four flags, so the flag kinds carry no information;
  - `np.dot` stays silent on a genuine overflow.

**(b) The 252-product accounting: correct.**
- By code: 64 + 64 + 62 + 62 = 252 flagged products per case.
- By generic runs: 1008 per case, or 512 when the inverse loop is skipped.
- Attribution of the 958 unretained warnings is inferred from the count.

**(c) Patch: correct.**
- Bit-identical to V002 on three toy pairs, including under `PYTHONWARNINGS=error`.
- Exactly four sites changed.
- Local errstate/seterrcall is restored, including after an exception and inside an outer `errstate(all='raise')`.
- The bound is sound, and a 1e-11 relative perturbation is detected.
- Out-of-site warnings stay visible: 1 per case under the patch vs 1009 under V002.

**(d) Evidence V003:** reproduced 9/9.

**Notes and how each was handled:**

| Note | Finding | Handling |
|---|---|---|
| N1 | Non-finite product left `all_within_nonblas_bound` true | Fixed: tri-state field plus counters |
| N2 | The "verified" label overclaimed | Fixed: renamed, with a matching meaning text |
| N3 | No absolute underflow term in the bound | Fixed: `+ 64·k·smallest_subnormal` |
| N4 | Diagnosis refinements | Covered by `DIAGNOSIS_0354_ADDENDUM_V001.md` |
| N5 | Missing tests | Added E8–E11 |

V004 carried N1–N3, but its `classification_meaning` always described the verified label. **V005** matches the meaning to the assigned label. V003 and V004 are retained as superseded.

## Round 2: delta review of V005 + evidence V005 + addendum. Verdict PASS_WITH_NOTES

**Hashes.** All seven matched. Each diff matches its real file pair.

**(a) Bit-identity to V002: confirmed.**
- Three generic toy pairs (16 and 24 dims; normal, below-E1 block, `PYTHONWARNINGS=error`) give JSON-equal content and empty stderr.
- Flagged calls per case are 64/64/62/62, or 64/64 when the inverse loop is skipped.
- Every site was labelled verified.
- Out-of-site warning visibility: 1 per case under V005 vs 1009 (or 513) under V002.

**(b) N1–N3 are correct.**
- Every flagged product increments exactly one of `nonfinite_products` / `bound_evaluated_products`.
- The tri-state field is correct, and a NaN deviation counts as a bound failure.
- The verified label requires evaluated == calls_with_flags.
- `classification_meaning` follows the assigned label.
- The absolute term is about 7.6e-321 at k = 24.

**(c) Evidence V005:** reproduced 14/14.
- **E8** is a TEST-ONLY `solve` wrapper, active only for square 2-D right-hand sides. It acts after `eigh` succeeds and reaches `mm('inverse_residual')`.
  - Result: nonfinite = 1, bound null, NOT_VERIFIED; L4 CASE_ERROR; run FAILED with exit 1; L6 unaffected.
  - The assertion is weaker than the observed outcome: it accepts exit 0 or 1, and either CASE_ERROR or a check failure.
- **E11** would pass vacuously if the product were unflagged; it was flagged.

**(d) Addendum: accurate,** with one correction recorded here.
- Correction to `DIAGNOSIS_0354_ADDENDUM_V001.md` item 1: the reviewer's dtype probe tested only N = 8, 16 and 24.
- The correct statement: float32, complex64 and complex128 flag at N = 16 and 24 and not at 8. Their exact threshold was not measured.
- The addendum is immutable, so the correction lives in this record.

**Notes (NOTE severity, reproduced in `review_0354_delta/edge_probe_results.txt`):**
- **D1:** `mm` inspects only products that raised a flag.
  - At N < 15, an infinite input with no new floating-point event (inf·1 + 0) gives a non-finite product with no flag, and `mm` does not record it.
  - Such a product still fails downstream through `fin()` (CASE_ERROR), and N×N products at N = 16 and 24 always flag.
  - Closure: check finiteness on every call.
- **D2:** a finite product whose |A||B| overflows (entries near 1e308 that cancel) gets an infinite bound and is labelled verified vacuously.
  - This is unreachable at the producer's magnitudes.
  - Closure: treat a non-finite bound as "not evaluated".

**Disposition of D1/D2.** Both are recorded as documented limits of V005: unreachable at the producer's sizes and magnitudes, and fail-safe downstream for D1. No V006 of the 0354 proposal is issued. The 0355 shared-junction producer, whose N = 24 and 36, adopts V005's `mm()` together with both closures, declared as a delta over V005. Those closures are checked in 0355's distinct review.

## Evidence copies (read-only)

**`review_0354/` (round 1):**

| File | sha256 |
|---|---|
| reviewer_fp_probes.py | 88cb99be36e103fdf3ebf6c9d1c39c3ce8f6641708281155b90f771a4566393e |
| reviewer_fp_probes_results.json | ec8d524717941c63997d1c3315b91e8800a1d74086cc4a550354150d08e6793b |
| patch_equivalence_probe.py | b91d1becd7d48137f119e6522db096a7436de4428fd12fd6d9f0538e2d84bb38 |
| rerun_diag_v001.json | e20bc290f06fa4d5d45e6d28885352293e8cffd051375131b5bbec784fe9fd0c |
| rerun_diag_v002.json | b36f4f3c960c97e3405eeb993c1a4c1cd9f00eeb971222411118165812e0115d |

**`review_0354_delta/` (round 2):**

| File | sha256 |
|---|---|
| patch_equivalence_probe_v005.py | 14fd36bb236023ade66d77b8fad6d50378668de38443edaba254c1bc49c3a918 |
| edge_probe.py | f7bcca86bc8b3297599a6f2c67cdb21180056b6fda195ec03ad3ef884ee7daf4 |
| edge_probe_results.txt | 7168ea98d680505fc6ed9d4c7977a1961f0f1d9e2106ddbc08c1f9db79a942db |

## Constraints observed (author and reviewer)

- Generic matrices only: no UNT matrices, spectra, frozen cases or output-derived numbers.
- From the saved output, only warning, environment and pin metadata were read.
- Bounded single-thread subprocesses; scratch writes only.
- No network, installation, environment change or deletion.
- The saved output is unchanged.

## Status

The diagnosis and inert proposal V005 are **REVIEWED** (two rounds).
- This is not a launch version.
- Any root attempt needs a separately reviewed producer version on fresh immutable paths, a new launcher pin and an explicit root decision.
- Numerical acceptance of 0351 remains root's.
