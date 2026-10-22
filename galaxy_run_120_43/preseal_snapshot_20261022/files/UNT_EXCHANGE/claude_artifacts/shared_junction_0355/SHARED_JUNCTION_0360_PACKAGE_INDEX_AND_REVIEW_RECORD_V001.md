# SHARED_JUNCTION_0360_PACKAGE_INDEX_AND_REVIEW_RECORD_V001 (launch-ready inert package V003)

**Task:** Codex1 0360, with the 0362 addendum. This index supersedes the 0355 package index V001 as the launch candidate; that index and every V001/V002 file are retained.

- Claude executed no native case.
- Nothing has been placed in CODEX1.
- Root alone places, reviews, accepts and launches.
- This package does not release the full galaxy run.

**Roles:**
- Producer author: helper a548f8dd1aacae44e.
- Launcher author: helper a08addddfc941b24d.
- Distinct reviewer: helper ab750e45705a5599e, who wrote neither the mv extension nor the launcher changes.
- Coordinator: CLAUDE2 main.

## 1. What changed and what stayed identical

**Producer V003** (44448458…):
- **Identical:**
  - Lines 80–134 match the reviewed V007 matrix-matrix block (V007 lines 69–123) byte for byte.
  - The frozen physics, tolerances, coefficients, pins (except the spec pin), dependency state string and all scientific spans in root's V002 static review (6fe6a6a6…) are unchanged. The only exceptions are the declared lines: the `mv` substitutions, the `tag` argument, the schema label, the spec version check and the docstring nits.
  - Output content is bit-identical to V002 on generic toys at N = 18, 24 and 36.
- **Added:** a delimited MV block (lines 136–173):
  - `MV_TAGS`, 24 `MV_SITES`, `_reference_mv` (a non-BLAS einsum, used as a TEST-ONLY injection point) and `mv(site, A, x)`.
  - `mv` equals `mm` under exactly four substitutions, so it inherits the reviewed fail-closed logic.
  - The FLAG_EVENTS field set is the same as `mm`'s, so the unchanged `flag_report` and `backend_flag_unverified` cover the `mv` sites.
- **Changed:**
  - Contraction mat-vec products in the literal, reverse (C_OT), solve/spectral and recursive paths now call `mv` with explicit site names: 24 sites, 344 products per case (288 literal + 56 recursion).
  - Spec V003 adds `matvec_verification.sites`, enforced by E_SPEC_MATVEC.
  - 0362 docstring nits: the spec version, and the description of the "minimum demonstrably below E1" conservative block.
- **Left bare:** the two 1-D endpoint dot products. A reviewer sweep found 1-D·1-D matmul flags only at N = 1024.

**Spec V003** (97d6bef9…): changes only `version` and `authored_by`, and adds `matvec_verification`.

**Wrapper V003** (264a09f2…): changes only:
- the producer path;
- PRODUCER/SPEC sha;
- the spec path;
- labels and `derived_from`;
- honest envelope wording in the docstring:
  - sampled monitoring cannot guarantee zero transient overshoot;
  - any observed breach fails and terminates;
  - no kernel enforcement;
  - no limit raised.

**Outer V003** (75fcb5da…): changes the wrapper path/sha and labels, plus one **disclosed preflight change**.
- Before creating any capture or receipt file, it checks:
  - all 11 `PREFLIGHT_PINS` (the producer, the spec and the nine bound documents);
  - the prelaunch review (present, correct hash, not identical to a pinned file);
  - the wrapper hash.
- It reports every problem in one refusal and writes nothing.
- A missing or changed placed file or dependency therefore no longer consumes the single attempt.

## 2. Review record

| Part | Verdict | Key evidence |
|---|---|---|
| A: producer V003 | **PASS** (3 notes) | V007 block `cmp`-identical. `mv` equals `mm` under 4 substitutions. 13 adversarial generic probes found no path to "verified" with any non-finite or unevaluated quantity, and the returned product was always bit-identical. Static and runtime coverage: 24 sites, 344 products per case. Bit-identity to V002 at N = 18/24/36. All 325 reviewed span lines checked at the author's offsets. Spec diff and E_SPEC_MATVEC verified. Harness 92/92. Cost at N=36: 0.049 s, 31.8 MiB, 0.77 MB. |
| B: launcher V003 | **PASS** (2 notes) | Syntax-tree diffs are limited to the allowed categories. The preflight sits before the `lexists` refusal and the first file creation. `PREFLIGHT_PINS` equals the wrapper `PINS`, which equals producer V003's table plus the producer. Self-check 41 + 15. All 17 dummy scenarios: every preflight refusal created 0 files, and multiple failures are listed together. Four integrated generic launches (author's and reviewer's scripts, default and `PYTHONWARNINGS=error`, N = 24/36): COMPLETED_WITHIN_ENVELOPE, `root_attention_required` false, stderr 0, all `mm`/`mv` sites verified, `check_failures` [], 0 leftover processes. |

**Notes:**
- **A-N1:** a blocked contraction is not itself a `check_failures` entry. It always co-occurs with rank-2 and family-gap failures (Δ_family ≈ 0.011 is far above the margin), so an empty `check_failures` implies both contractions were evaluated. Root should still read `cases[*]/contraction/status` directly. Making it explicit would be an optional future change.
- **A-N2:** an exception inside verification leaves the counter invariant unbalanced. This is expected: the run goes to CASE_ERROR with the site NOT_VERIFIED and `all_within` null, the same as reviewed V007.
- **A-N3:** the endpoint-dot justification is independently confirmed.
- **B-N1:** the author's receipt omits the failed-predicate list for the defence-in-depth scenario. The re-run shows the expected set, and the behaviour matches.
- **B-N2:** still outside the preflight, see §3 step 7.

## 3. Launch order for root (one attempt)

`<CODEX1>` = `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1`

1. **Place the four files byte-identically** from `claude_artifacts/shared_junction_0355/` to `<CODEX1>/`:

   | Source | Destination in `<CODEX1>/` |
   |---|---|
   | `producer_A/owned_shared_junction_reference_producer_v003.py` | same name |
   | `producer_A/SHARED_JUNCTION_REFERENCE_FROZEN_SPEC_V003.json` | same name |
   | `launcher_B/shared_junction_reference_root_launch_wrapper_v003.py` | same name |
   | `launcher_B/shared_junction_reference_outer_driver_v003.py` | same name |

2. **Run `shasum -a 256` on the four placed files.** Expected values:
   - producer `44448458823510fefbbcb15d5104fc64755cc9435312d31b9f219ca70d355383`
   - spec `97d6bef9741d027fcc12e03d450547f0990de41fcdcfa38666eec34a2a5ab644`
   - wrapper `264a09f2cc3f8eb6c2bf6ebfe85a5494b2098bb55aabffa58d53f6730374c78c`
   - outer `75fcb5daacd6ca11a0edce01d5ca42e21dcb014a0e1006b5e6f2064f26883940`

   The outer driver cannot verify its own hash, so this step is the only check of it. The outer preflight checks the other three and the nine bound documents before writing anything.
3. **Confirm the nine bound documents are unchanged.** The hashes are the same as in the 0355 index §2 step 3, and the outer preflight refuses without writing if any differs.
4. **Confirm none of the nine result paths exists** in `<CODEX1>`. Each is `SHARED_JUNCTION_REFERENCE_` followed by:
   - `OUTPUT_V001.json`
   - `JOURNAL_V001.jsonl`
   - `STDOUT_V001.jsonl`
   - `STDERR_V001.txt`
   - `ROOT_RECEIPT_V001.json`
   - `ROOT_TERMINAL_RECEIPT_V001.json`
   - `OUTER_RECEIPT_V001.json`
   - `OUTER_DRIVER_STDOUT_V001.txt`
   - `OUTER_DRIVER_STDERR_V001.txt`

   Read-only verification shows none exists today.
5. **Confirm `/bin/ps` is permitted.** A denial is detected only inside the wrapper, after captures exist, so it **would consume the attempt**.
6. **Write a distinct prelaunch review** of the four files' bytes and hash it.
7. **Run exactly once**, as the user whose site-packages hold NumPy 2.0.2, with no sudo, `-I`, `-s`, `-O` or `PYTHONNOUSERSITE`:

   `/Applications/Xcode.app/Contents/Developer/usr/bin/python3 -B "<CODEX1>/shared_junction_reference_outer_driver_v003.py" "<prelaunch review path>" <its sha256>`

   The preflight cannot catch these **(B-N2)**, and each would consume the attempt:
   - interpreter or environment misconfiguration, such as the wrong user or PYTHONNOUSERSITE, which causes a NumPy import failure;
   - a dependency changed between the outer preflight and the wrapper's own check. The wrapper's defence-in-depth refusal catches this, but only after captures exist.
8. **Acceptance.** Root's saved-result review needs all of:
   - an outer receipt COMPLETED_WITHIN_ENVELOPE;
   - `root_attention_required` false;
   - `check_failures` empty;
   - both cases' `contraction/status` evaluated;
   - coefficient, gap and reference statuses all successful;
   - every `mm`/`mv` site classified `FLAGGED_PRODUCTS_FINITE_WITHIN_NONBLAS_ROUNDING_BOUND`. This does not establish that the flags were spurious.

   COMPLETED alone, or exit 0 alone, is not sufficient. Never launch any V001 or V002 producer, spec, wrapper or outer driver.

## 4. Envelope and remaining root decisions

**Envelope.** One thread, 10 s, 256 MiB sampled RSS, 32 MiB output: unchanged and inherited. Monitoring is sampled, every 20–30 ms through `/bin/ps` for memory and through result-file sizes for output, so it **cannot guarantee zero transient overshoot**. Observed overshoots before the kill were 281–313 MiB and 31–32 MiB. Any observed breach fails acceptance and terminates. There is no kernel enforcement: RLIMIT_AS/DATA/RSS cannot be set to 256 MiB on this host. No limit has been raised.

**Expected at the real sizes:**
- L4 (N = 24): no mat-vec flags at tested sizes, and the matrix-matrix flags are verified.
- L6 (N = 36): all 344 mat-vec products per case flagged and verified.

**Remaining items:**
- the three 0354 files under UNT_EXCHANGE must stay in place;
- NumPy from the user site;
- the interpreter is recorded but not pinned;
- the duplicated pin list in the outer driver, which the self-check enforces as equal to the wrapper's.

## 5. Hashes (each computed from final bytes)

| File | sha256 |
|---|---|
| `producer_A/owned_shared_junction_reference_producer_v003.py` | 44448458823510fefbbcb15d5104fc64755cc9435312d31b9f219ca70d355383 |
| `producer_A/SHARED_JUNCTION_REFERENCE_FROZEN_SPEC_V003.json` | 97d6bef9741d027fcc12e03d450547f0990de41fcdcfa38666eec34a2a5ab644 |
| `launcher_B/shared_junction_reference_root_launch_wrapper_v003.py` | 264a09f2cc3f8eb6c2bf6ebfe85a5494b2098bb55aabffa58d53f6730374c78c |
| `launcher_B/shared_junction_reference_outer_driver_v003.py` | 75fcb5daacd6ca11a0edce01d5ca42e21dcb014a0e1006b5e6f2064f26883940 |
| `producer_A/producer_V002_to_V003.diff` | abf013081bbaf14d523b3d05a6edb0af0209f93bce79ea18784389af33521f5b |
| `producer_A/SPEC_V002_TO_V003_DIFF.json` | 5c5aa70306534d602fa15da5e5168c86af29364fcc1a6510d08cd6979f9f6b22 |
| `producer_A/IMPLEMENTATION_NOTES_V003.md` | ee22e40fe779f8d7b6d1df4ffbf4601c457488bce0b332ea4ac0f5ad53d09c03 |
| `producer_A/test_shared_junction_producer_synthetic_v003.py` | 6e6b294ca213d5d0a3c5a0542bb4dfec3a4d6ab6b2d47cfe26d7f1a9b98b108d |
| `producer_A/SYNTHETIC_TEST_RECEIPT_0360A_V003.json` | 8cdf8815ba0ef09bcad6629eb933d74be61a97b6766a0528ad83fc48597888d2 |
| `producer_A/FILE_MANIFEST_0360A_V003.json` | f8060dedf0fdb4c73024c9f3ef435e71ed19c69a4b798bbee5c6a27eb4c62190 |
| `launcher_B/shared_junction_wrapper_V002_to_V003.diff` | a541477cb484acdc80e3fa7cb9b02ed3f2cf25ab5b0d518967ed174383095fd9 |
| `launcher_B/shared_junction_outer_V002_to_V003.diff` | d1da55582215cdacf05bd74a5914731187766e1f5ae091410ad5b09e6a19cf80 |
| `launcher_B/DIFFERENCES_V003.md` | b8376865e9355daf4108f1631a5164bc339a420fbf84a309a6407b71873a0c38 |
| `launcher_B/DUMMY_TEST_RECEIPT_V003.json` | e572d83629b5751d1b9dd9bb8ac7460c639c7c9bb9e65be5ecaaae619d5e2de7 |
| `launcher_B/selfcheck_0355_v003.py` | 3f10e9dabe472aaa5d502a02ba6550122b04472a03e1bff08ef69df0ddd4f104 |
| `launcher_B/dummy_launch_harness_0355_v003.py` | 3729cd2b13384824347c8e32a6d8f5ee80e0a71d31f3c6c19e06c53558fc02d0 |
| `launcher_B/integrated_generic_launch_0360_v003.py` | eccd818f9008d7c0fcc3dae83bc8e8770a7d399add7a39c4d4e25e2f20413e7d |
| `launcher_B/build_0355_v003.py` | 3a4d7c551a6b2810f0ab957ef557916b89b6b20360fc788ae61b4123c9a5d898 |
| `launcher_B/FILE_MANIFEST_V003.json` | debd62d60da70bc171bdd1f5be77373dd97dbbf7bea1749015aeaacfee6ccbdb |

| Superseded, retained (never launch) | sha256 |
|---|---|
| `producer_A/owned_shared_junction_reference_producer_v002.py` | d5238c5295e3edc99d00450e2f4caa7c40a7234757215c773cd173a38866ec51 |
| `producer_A/SHARED_JUNCTION_REFERENCE_FROZEN_SPEC_V002.json` | 1a0b4c49d8ea2bb3ebb5f60dbbe5ae4a0a8a1b0e46a65f4167652fc9ad982525 |
| `launcher_B/shared_junction_reference_root_launch_wrapper_v002.py` | e03da7d8ac6cb16851cff0c288e9bc277303517cfcce438dc94b2d04cbb054dc |
| `launcher_B/shared_junction_reference_outer_driver_v002.py` | 67dd3c8f0175c21d6a0b658cf38a38452bcf525ca2ca9484fecdb8056a7a065e |
| `SHARED_JUNCTION_0355_PACKAGE_INDEX_AND_REVIEW_RECORD_V001.md` | 6d332664f1a145af08d24d17c8a73ca937fff55d0b2afc934d316f9a94f1584d |
| `producer_A/owned_shared_junction_reference_producer_v001.py` | bc3bed35a1d5f96b9754c51061180e1d16ac999737d2f5aa7dbdf8932aec1f37 |
| `launcher_B/shared_junction_reference_root_launch_wrapper_v001.py` | 57fb374bfb20b4b50833d6d699e6dd6ffe0b553260d4bfab33a709d6a080c087 |
| `launcher_B/shared_junction_reference_outer_driver_v001.py` | 7a5ad7ef57b2e0bae743aa33bbdbef5fef626ba8c8ba87fde3b38fbf8b96c628 |

| Review evidence (read-only copies) | sha256 |
|---|---|
| `review_0360A/adversarial_mv.py` | 99f3a39e5bda2dd2258dfc0e5199455ba2528451e591bfa4899734dd04d029c7 |
| `review_0360A/adversarial_mv_results.json` | e3dd73cbbd014c41de601ce5038887423a7ff5a3da12a1474452b9587c01ca32 |
| `review_0360A/harness_v003_stderr.txt` | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| `review_0360A/harness_v003_stdout.txt` | 5dba369299cfb36d071d3a13dc307afc3996fca234c0592b1a0e9730827370f8 |
| `review_0360A/probe_bitid_coverage.py` | 4f5ba22275cb21154fc25a003279ef23ba2e295646dff24030fac320ca9f994d |
| `review_0360A/probe_bitid_coverage_stdout.txt` | bcba2f043151014ebfd3354e93e8a10493dadcc046f7f3d079abb7584d5a1c9d |
| `review_0360A/probe_vecdot.py` | 2ba17e349e86900b927101826a4e3f3f16693ffcacd21433efb0176d92fe2221 |
| `review_0360A/probe_vecdot_stdout.txt` | d01e863c5d0b44a4c6aa35336e3cf8670da1c29fa8e1ea84341e73bec69c17ff |
| `review_0360A/span_mapping_check.txt` | bc58bd3d1f6af7cf7c0d321464b3a68507bfabd4131bfcc1e8e5d71f1cb54a53 |
| `review_0360B/astdiff.py` | b761e55b3e79f28a400ba0a78f51ee6be23e0bfe1b35419e5ed46857f8bcd335 |
| `review_0360B/harness_summary.txt` | d7fe230c296f95e3313778f8a251ae6067c1569962f0d1f4d3e27ca3e3b1d81c |
| `review_0360B/hashes.txt` | f8dac65f60cc7d01ab9663211944598f2e4766aa645f9250ac0b0042db90e419 |
| `review_0360B/integ_mine_stdout.txt` | 1021e5e06dcf50dd5e1a4c0818e2fad0d3cbf52626d43124af425c60845f2a7f |
| `review_0360B/integ_results_integ_1792087984.json` | a888944ed8096e99b287a1fe973ef5eda20cdab6a137adb2ae444beb98a789da |
| `review_0360B/integ_sj_v003.py` | 41aebf1d7c9eb55393d7d4dcfcb928a84677f34ded736e15190ef7fa5876296e |
| `review_0360B/integrated_author_stdout.txt` | fe10e10120df2b1dba3feecea7da9345a1c49df70bd5df97f86ad883d126035c |
| `review_0360B/pin_crosscheck.txt` | f282c8eee4dec75c471e194943fb898f6196b943ea0cc9b5ae0cf9a2dc8556bf |
| `review_0360B/results_runs_1792087930.json` | b0f3c593c42fa67728a6b3456523bf8f5d105a51fd77b18c3feb297d6604fd6b |
| `review_0360B/selfcheck_stdout.txt` | 9b9a298ea0b93e46bb4569a225598923e325ed9b9a4752cc9f8c135fb3f0244f |

The 0355 index V001 hashes (6d332664…) and its review copies remain valid for the superseded V002 package.

**Status:** producer V003 REVIEWED (PASS); launcher V003 REVIEWED (PASS). Nothing has been placed in CODEX1, and no native case has been executed.
