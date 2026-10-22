# REVIEW_RECORD_0357_V001: distinct review of fail-closed verification (patch proposals V006 → V007)

**Task:** Codex1 0357. Per 0358, this is one coherent correction folded into the 0354 lineage.

| Role | Who |
|---|---|
| Author | CLAUDE2 main lane |
| Distinct reviewer | Claude helper ab750e45705a5599e (wrote none of the reviewed code) |

## Round 1: V006 (d4dd3125…) with evidence r2 (20/20). Verdict PASS_WITH_NOTES

**Hashes.** All seven files matched, and both diffs matched the real changes.

**(a) No path assigns the verified label when any of these is non-finite or unevaluated: the product, the inputs, the reference, the bound or the deviation.** In every probe the returned product was bit-identical to a plain matmul, no warning leaked, and state was restored. The reviewer's adversarial generic probes:

| Probe | Case | Result |
|---|---|---|
| A1 | Deviation overflow | NOT_VERIFIED; `verification_fp_kinds` overflow recorded |
| A2 | NaN in the reference only | NOT_VERIFIED |
| A3 | inf product with inf reference | Counted as non-finite |
| A4 | inf input against a zero row | NOT_VERIFIED. Accelerate returns NaN; the inputs-finite gate is a backstop. |
| A5 | Subnormal-scale bound | Evaluated and VERIFIED, which is correct |
| A6 | Reference off by 1e-15 / 1e-9 | VERIFIED / bound_failed |
| A8 | Mixed good and bad products at one site | NOT_VERIFIED |
| A9 | Unflagged finite product | Not recorded |
| A10 | Outer `errstate(all='raise')` | Restored after a verification exception |

**(b)** Bit-identical to V002 in the pipeline: normal, below-E1 and `PYTHONWARNINGS=error`. Flagged calls were 64/64/62/62, and every site was VERIFIED.

**(c)** D1 is closed. The counter invariant holds by construction on every normal return.

**(d)** Verification events are visible through `verification_fp_kinds`. ErrState and seterrcall are restored in both nested uses.

**(e)** E12a–E14 prove their claims. E12b's TEST-ONLY injection is disclosed and restored in `finally`.

**(f)** Nothing else changed apart from the stated rename `max_abs_deviation_over_evaluated_products`.

**Findings:**
- **R1 (NOTE):** an exception inside verification left `all_within_nonblas_bound` reading true. The site was correctly NOT_VERIFIED and the exception propagated. This was reachable only by injection or MemoryError. **Fixed in V007.**
- **R2 (NOTE, for 0355):** copying `mm()` verbatim also requires `_reference`, `FLAG_EVENTS`, `EPS`, `TINY_SUB`, `Counter`, `flag_report` and the label constants. This was passed to the 0355 implementer.

## Round 2 (delta): V007 (944531eb…) with evidence V007 (21/21). Verdict PASS

**(a)** The diff is exactly the stated change: `evaluated_all` includes `bound_evaluated == calls_with_flags`, plus the schema label and docstring. `ok` is logically identical to V006, so no label can change.

**(b)** A7 now gives null and NOT_VERIFIED. The other ten adversarial probes are identical between V006 and V007.

**(c)** The pipeline is JSON-equal to V002 in all three toy pairs. Every site is VERIFIED, there are no `backend_flag_unverified` failures, and stderr is empty.

**(d)** E15 proves its claim: the exception propagates, the field is null, the result is NOT_VERIFIED, and state is restored.

## Register

Evidence r1 (`patch_evidence_v006.py`) ran 18/19. E12a wrongly expected the einsum overflow to be reported as an FP event; einsum, like `np.dot`, does not check FP status. The code was correct. The expectation was fixed in r2 and E12d was added. All files are retained.

## Evidence copies (read-only)

| File | sha256 |
|---|---|
| `review_0357/adversarial_probe.py` | a198670aac97f5e870fe21796cf66f4e6bef45b464b5d9d06f7cb1537c7bff88 |
| `review_0357/adversarial_results.json` | 54466868f8e1e16b5b16096820fc40a5a92caf3c48417a67f7cec4e5feb6bbee |
| `review_0357/patch_equivalence_probe_v006.py` | eb47319024ceca4099bfebfb432eb733099d98bc1681ddebfc75d32b7e89f0f1 |
| `review_0357/evidence_rerun_stdout.txt` | 9a8c8af5e3deb5cb85880882bd4156f96695b296c9c5cba5d98d26f554dbe4bc |
| `review_0357_v007/adversarial_probe_v007.py` | 64c9f89adf00fe2947a9949e4be3601077a69524a552207d1bfc0c882f2e091f |
| `review_0357_v007/adversarial_results_v007.json` | 0ad5da838c646bbb0375edefb1fbd57ec6bdfe7ed16602f6e8c9379706e563b5 |
| `review_0357_v007/patch_equivalence_probe_v007.py` | 817b4511ae388447c616262982d16d9808fe6fbed16c371978f827388222891b |
| `review_0357_v007/evidence_v007_stdout.txt` | b388661f0e6ee47c7491a4ec0a246093b1fca58e0bc32dd02c7c03a610d2748b |
| `review_0357_v007/equiv_v007_stdout.txt` | d8e602259997f0fcf9bbc4369113e9620c2f1dfd5202d365011d6bba54df603f |

## Status

V007 is **REVIEWED** and is the final reviewed helper for 0355. It is inert. Root alone decides any native attempt.
