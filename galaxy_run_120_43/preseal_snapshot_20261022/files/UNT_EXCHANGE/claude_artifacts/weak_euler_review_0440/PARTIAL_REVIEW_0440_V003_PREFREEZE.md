# Claude4 partial review 0440, V003: pre-freeze evaluation of Claude3's module

Lead: Claude4. 2026-10-16, about 19:06 UTC. **This is not the verdict.** Claude3 had not posted 0002_2026-10-16_done-0439.md, so the evaluated file is a pinned pre-freeze snapshot. The verdict will name the frozen hash Claude3 reports. If that hash differs from the one below, everything here is re-run.

## Evaluated object

- Live file: claude_artifacts/weak_euler_0439/weak_euler_assembly_c3v001.py, 344 lines, mtime 14:01 local.
- Byte-identical copy (cmp verified): c3_snapshot_8632bda6/weak_euler_assembly_c3v001.py.
- SHA-256 **8632bda6d4a80d0d25bfa90ef4b1066954b6bc67c90f184d0a78c232bf3013da**, the same before and after every run. The live file was never imported; only the copy was.

## Results so far

1. **Static check** (AST only, static_check_c4lead_v001.py; report c3_snapshot_8632bda6/STATIC_REPORT_c4lead.json):
   - Only numpy, math and numbers are imported; math and numbers are stdlib.
   - There are no linalg, solve, inv, pinv, svd, eig, clip, diag, eye or identity calls, no I/O or print, and no module-level executable statements.
   - All 23 parameters are required keyword-only, with no defaults, *args or **kwargs.
   - All 19 in-place writes target locals (E, PM, VP, Y, A, b), never a parameter.
   - The test-side transposes at L277, L287, L295, L301 and L319-321 are all `.conj().T`.
2. **Line trace against the contract** (lead reading, to be repeated by H1 on the frozen file):

   | Contract item | Lines |
   |---|---|
   | E | L221-222 |
   | PM | L228-229 |
   | VR | L234 |
   | VP | L238-240 |
   | VZ | L244 |
   | AR, then x w rho, then the density-gradient term -(w P_R/rho) G | L272-275 |
   | AP, then x w rho | L282-285 |
   | AZ, then x w rho, then the density-gradient term -(w P_z/rho) G | L291-293 |
   | Pressure term, -divU^H diag(w) PM | L299-301 |
   | Normalization of A only | L304 |
   | b with w rho f, and its normalization | L313-322 |

   Each term carries the volume weight exactly once. Trial-side maps are never conjugated. G is used verbatim. There is no m0 or Phi0 term. Returned E, PM, VR, VP and VZ are never scaled.
3. **H2 harness** (fixtures_weak_euler_h2v001.py): **266 checks, 235 pass, 31 record-only, 0 fail**. The result is identical under the root interpreter (Python 3.12.14, numpy 2.3.5, single-thread BLAS) and under /usr/bin/python3 (3.9.6, numpy 2.0.2). The checks were:
   - F0, the hand case, 2/2.
   - F1, the loop-reference comparison including the square npoints == nfree case, 9/9.
   - F2, term isolation including vertical shear alone, 15/15.
   - F3, reference-free properties (phase, column phase, weight and normalization scaling, m-polynomial, R-scaling), 13/13.
   - F4, G verbatim, no mutation, shapes and dtypes, 5 pass plus 2 record.
   - F5, no hidden forcing, 2/2.
   - F6, malformed inputs, 189 pass plus 29 record.

   Results: c3_snapshot_8632bda6/fixture_results_c4lead_pre_py312.json and fixture_results_c4lead_pre_py39.json.
4. **Record-only behaviors where the contract is silent.** None conflicts with the contract.
   - Accepted: real-dtype maps and forcing, cast losslessly. This matches PARTIAL_REVIEW_0440_V002_MAP_STRUCTURE.md: root's U_R and U_z are real. Python-list, int64 and float32 vectors are accepted. normalization_scale given as the integer 2 is accepted.
   - Rejected: bool for m and for normalization_scale. numpy.int64 for m, which matches the prior v002 at L18. Whitespace-only provenance and non-string provenance. **Complex-dtype "real" vectors even with zero imaginary part**: this is strict but safe. Usability note for root: background vectors must be passed with real dtype; if one is computed through a complex path, root must take .real explicitly.
   - No output shares memory with an input.

## Pending before the verdict

- Claude3's done-0439 with frozen hashes.
- H2's structured return and the adversarial cross-check of H1's oracle against H2's reference.
- Phase 2 on the frozen file: H1's line review, the H2 run with the root-structured F8, the H1 oracle against the module, and a skeptical verification of any candidate defect.
