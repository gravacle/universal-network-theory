# SHARED_JUNCTION_0355_PACKAGE_INDEX_AND_REVIEW_RECORD_V001

**Task:** Codex1 0355, with 0357/0358/0359 binding. This is one inert package: frozen spec, producer, wrapper/outer driver, tests, distinct reviews, exact pins and fresh output paths. Claude ran no native case at any stage. Root alone decides and launches the single bounded attempt.

**Coordinator:** CLAUDE2 main.

**Authors:**
- Producer and spec: helper a548f8dd1aacae44e.
- Launcher: helper a08addddfc941b24d.

**Distinct reviewer:** helper ab750e45705a5599e, who authored none of the reviewed code.

## 1. Review record

### Part A: producer V001. Verdict PASS_WITH_NOTES
- **(a) Spec fidelity**
  - Frozen values and definitional relations are exact; a failure exits 2.
  - A structure probe at non-frozen L = 2 and 3 passed 274/274 checks:
    - indexing is cycle·2L + n; there are three periodic rings;
    - bridge u is (0,0)–(1,0) and bridge v is (0,0)–(2,0);
    - qa, qb and qd sit on the three n0 sites;
    - the scalar matches equation (1) for all 32 words;
    - the OLD and ALT scalars equal a_eff, and DOUBLE equals 2a_eff + 2U_d − r;
    - Adj(1,1) equals I3⊗C + S3⊗P0, and leaf exchange maps M(OLD) to M(ALT).
  - Code reading:
    - E1 is the lowest eigenvalue of M(OLD) and enters every denominator.
    - Contacts are the identity for the flips and p_b, p_d for the Binds; qa is fixed at 1.
    - There are 24 orders and 14 subsets, plus the reverse coefficient C_OT; −h²g²C_TO is reported.
    - No relaxed-q denominators are used.
    - Δ_family is the minimum of the five terms of equation (6); the ceiling is 24/Δ³.
    - The secular equations, the double-star equation and the tanh certificate are correct, and the 0351 tolerances are used.
- **(b) Contractions:** the literal and recursive contractions are organized independently.
  - The reviewer's independent full-space Feshbach oracle (whole 32-word × carrier space, generic three-ring toys at N = 9, 12, 15; 6 cases) gives:
    - degrees 1–3 equal to 0;
    - degree 4 equal to −C_TO within 1e-10;
    - all eight producer totals equal to a direct 24-order sum.
  - The author's harness re-ran 65/65.
- **(c) Shared check block:** producer lines 80–134 are byte-identical to 0354/0357 V007 lines 69–123, and each copied name has a single definition. `mm` is used at exactly the four N×N sites.
- **(d) Blocking:** BELOW_E1 or RESONANT_OR_UNRESOLVED blocks every inverse in that case. There is no clipping, broadening or pseudo-inverse.
- **(e) Pins and outputs:**
  - Pins are verified before the journal opens.
  - Output and journal are exclusive; the JSON is strict and fsynced.
  - Exit codes are 1 for CASE_ERROR or post-analysis error, 2 for coded errors and 3 for unexpected ones.
  - `full_parent_ready` is false.
- **(f) Generic toys at N = 24 and 36:**
  - Run: COMPLETED, 0.10 s, 35.8 MiB peak, 0.60 MB output. Under `PYTHONWARNINGS=error` the result is identical and stderr is empty.
  - Flag accounting: `mm` 32/32/14/14, all verified.
  - Warnings: **0 at N = 24 and 1376 at N = 36** (see item N1 in section 3).
- **Findings and dispositions:**

  | Finding | Disposition |
  |---|---|
  | S1 SHOULD-FIX: stale dependency state, unpinned 0357 root receipt | Fixed in V002 |
  | N2: freezing document pinned at the FROM_CODEX path | Fixed in V002 (CODEX1 copy) |
  | N1: mat-vec flags | Root decision |
  | N3: four judgement calls (endpoint positivity on the joined component; algebra failures recorded rather than exiting; rank-2 failure non-blocking; spec placed by root) | Reviewer agrees |

### Part A delta: producer V002. Verdict PASS
- The diff is exactly:
  - S1: the state string, plus the pin `dependency_0354.root_review_0357` = b4720449…;
  - N2: the freezing document at its CODEX1 copy, same 971f235a…;
  - version and schema labels;
  - spec V002 at the CODEX1 path.
- The spec diff touches only version, authored_by, freezing path, dependency state and the added receipt entry.
- The verbatim block is unchanged.
- The harness passes 68/68; three new tests check that a mismatched receipt, a missing receipt, or a missing spec entry each exits 2 with nothing written.
- Real pins were hash-checked only: 9 of 10 are present. The CODEX1 spec copy is absent until root places it.

### Part B: launcher V002. Verdict PASS_WITH_NOTES
- **(a) Changes vs the reviewed 0351 launcher V002** (syntax-tree diff) are exactly:
  - names and pins;
  - the base path;
  - the `Pin pending (None)` and `Pinned input missing` refusals.
  
  Everything else is 0351 behaviour, and the self-checks pass 41 + 21.
- **(b) Pins:** PRODUCER d5238c52…, SPEC 1a0b4c49…, and the driver's WRAPPER e03da7d8… all match the bytes. The nine bound documents equal the producer's pin table (10 = 10). The launcher never writes the CODEX1 spec copy; a missing or mismatched copy is refused.
- **(c) End to end** (scratch copies of the launcher pair with a generic test copy of producer V002, N = 24 and 36):
  - COMPLETED_WITHIN_ENVELOPE with `root_attention_required` false, and stderr empty;
  - journal START, CASE, CASE, END, with all END checks true;
  - 0 warnings at L4 and 1376 captured at L6;
  - 0.16 s and a 52 MiB conservative peak.
- **(d) Dummy scenarios:** all 39 reproduced. The killpg-PermissionError scenario sets `root_attention_required` true and leaves 2 leftover processes at receipt, falling to 0 after the wall. Every other scenario leaves 0.
- **(e) Resources:** U1–U3 are accurately reported and are root decisions (section 3).
- **Findings and dispositions:**

  | Finding | Disposition |
  |---|---|
  | F1 SHOULD-FIX: launch order lacked explicit hash confirmation of the four placed files | Fixed by section 2 below, which supersedes `launcher_B/DIFFERENCES_V002.md` §Launch order. Section 2 is to be confirmed by the reviewer before return. |
  | F2: cap overshoots vary with timing (281 vs 313 MiB; 31 vs 32 MiB), all fail-closed | Noted |
  | F3: 0354 files must stay in place | Noted |

## 2. Launch order for root (one attempt; supersedes DIFFERENCES_V002.md §Launch order per review F1)

`<CODEX1>` = `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1`

1. **Place the four files, byte-identical, from `claude_artifacts/shared_junction_0355/`:**
   - `producer_A/owned_shared_junction_reference_producer_v002.py` → `<CODEX1>/owned_shared_junction_reference_producer_v002.py`
   - `producer_A/SHARED_JUNCTION_REFERENCE_FROZEN_SPEC_V002.json` → `<CODEX1>/SHARED_JUNCTION_REFERENCE_FROZEN_SPEC_V002.json`
   - `launcher_B/shared_junction_reference_root_launch_wrapper_v002.py` → `<CODEX1>/shared_junction_reference_root_launch_wrapper_v002.py`
   - `launcher_B/shared_junction_reference_outer_driver_v002.py` → `<CODEX1>/shared_junction_reference_outer_driver_v002.py`
2. **Confirm with `shasum -a 256` that the four placed files are exactly:**
   - producer `d5238c5295e3edc99d00450e2f4caa7c40a7234757215c773cd173a38866ec51`
   - spec `1a0b4c49d8ea2bb3ebb5f60dbbe5ae4a0a8a1b0e46a65f4167652fc9ad982525`
   - wrapper `e03da7d8ac6cb16851cff0c288e9bc277303517cfcce438dc94b2d04cbb054dc`
   - outer `67dd3c8f0175c21d6a0b658cf38a38452bcf525ca2ca9484fecdb8056a7a065e`

   **Why this step matters:** a missing or mismatched producer or spec is otherwise caught only inside the wrapper. By then the outer driver has already created its capture files and a FAILED outer receipt, whose names block any rerun. So that refusal consumes the single attempt.
3. **Confirm the nine bound documents are present and unchanged.** Paths under FIRST_CONSTRUCTION_REVIEW_2026-10-13 unless marked UNT_EXCHANGE:
   - `helpers/recovered_packet_audit/OWNED_THREE_CYCLE_SHARED_JUNCTION_REFERENCE_BAND_PROPOSED_V001.md` `b41be4c2b39292016324442a92754a48c78c5a9b16a36c5736f68490fc7f465f`
   - `helpers/coefficient_method/OWNED_THREE_CYCLE_SHARED_JUNCTION_BAND_DISTINCT_REVIEW_V001.md` `b0170c02a3d69b27ce070cd9f53d6011a4dc77ae7cc4553ac164c981dbeb5805`
   - `helpers/recovered_packet_audit/OWNED_BRIDGE_BAND_FIRST_OMITTED_PORT3_RESONANCE_PROPOSED_V001.md` `8eb0d18bbc891be1bfd62759e5b3055650d963b17f1a1c56f92a1515a1cea6f6`
   - `helpers/coefficient_method/OWNED_BRIDGE_BAND_OMITTED_PORT3_RESONANCE_DISTINCT_REVIEW_V001.md` `3f853643715254369477fbd048d5499e21ec80e7ab13ea7701578ebdaf85e1eb`
   - `CODEX1/CLAUDE_SHARED_JUNCTION_INERT_INTERFACE_TASK_0355_V001.md` `971f235a2d9bbbb1f1cbefc2e869d34954d4f3228427032103e7353962ed85d8`
   - `CODEX1/FLOATING_VERIFICATION_HELPER_ROOT_REVIEW_0357_V001.json` `b47204492675aea36f39f1bb4ea44fe2a52d4e02f21e85188a414c1ad0cdde98`
   - UNT_EXCHANGE `claude_artifacts/fp_warning_diagnostic_0354/PATCH_PROPOSAL_bind_producer_v007.py` `944531eb5b3d6a8981cfb1c7dec60bc76c6536658c8ffdb24ace7ce311e94c2a`
   - UNT_EXCHANGE `claude_artifacts/fp_warning_diagnostic_0354/DIAGNOSIS_0354_V001.md` `a83200b6b81f2f2c3ad7009eddad54310e668e19a056000bdf08d46c308fbf01`
   - UNT_EXCHANGE `claude_artifacts/fp_warning_diagnostic_0354/NOTES_0357_V006.md` `c3923f15a973fc0706bea38d0936c3d62f24f986f7e7e212106b29b276ca86fa`
4. **Confirm none of the nine fresh result paths exists in `<CODEX1>`:** `SHARED_JUNCTION_REFERENCE_` +
   - `OUTPUT_V001.json`
   - `JOURNAL_V001.jsonl`
   - `STDOUT_V001.jsonl`
   - `STDERR_V001.txt`
   - `ROOT_RECEIPT_V001.json`
   - `ROOT_TERMINAL_RECEIPT_V001.json`
   - `OUTER_RECEIPT_V001.json`
   - `OUTER_DRIVER_STDOUT_V001.txt`
   - `OUTER_DRIVER_STDERR_V001.txt`
5. **Confirm `/bin/ps` is permitted.**
6. **Write a distinct prelaunch review** of the exact four files' bytes, and hash it.
7. **Run exactly once,** as the user whose site-packages hold NumPy 2.0.2. Do not use sudo, `-I`, `-s`, `-O` or `PYTHONNOUSERSITE`:

   `/Applications/Xcode.app/Contents/Developer/usr/bin/python3 -B "<CODEX1>/shared_junction_reference_outer_driver_v002.py" "<prelaunch review path>" <its sha256>`
8. **Acceptance requires:**
   - an outer receipt COMPLETED_WITHIN_ENVELOPE with `root_attention_required` false;
   - a separate saved-result review.

   COMPLETED means the computation finished; it is not a scientific pass. Never launch the V001 producer, spec, wrapper or outer files.

## 3. Root decision items (reported, not worked around)

- **N1. L6 matrix-vector backend flags.**
  - At N = 36 the contraction mat-vec products raise 4 flags × 344 products = 1376 RuntimeWarnings per case (288 literal + 56 recursion).
  - They are the same Accelerate artefact class as 0354:
    - a C-ordered mat-vec sweep flags at exactly N ≥ 32;
    - results are exact against einsum, and zero vectors flag too.
  - The warnings are captured, counted and visible, with stderr at 0. They are not `mm`-verified.
  - They are cross-checked indirectly by literal-vs-recursion and solve-vs-spectral agreement, and a non-finite result fails through `fin()`.
  - At L4 (N = 24) there are none.
  - **Options:** accept them as documented and non-gating, or commission a reviewed mat-vec extension of `mm` in a new version.
- **U1/U2. Memory and output caps.**
  - Both caps are sampled through `/bin/ps` every 20–30 ms; they are not kernel-enforced.
  - Overshoots of 281 and 313 MiB were sampled before the memory kill, and 31–32 MiB before the output kill. All runs fail closed.
  - On this host RLIMIT_AS, RLIMIT_DATA and RLIMIT_RSS cannot be set to 256 MiB (`ValueError: current limit exceeds maximum limit`), consistent with the 0353 metadata failure.
  - The resource policy is root's.
- **U3.** Any stderr text fails acceptance. The producer captures its warnings, so stderr is 0.
- **U4.** The three 0354 files under UNT_EXCHANGE are pinned and must stay in place until launch.
- **U5.** Lineage items inherited from 0347/0351:
  - the thread environment is set explicitly;
  - NumPy comes from the user site;
  - the interpreter is recorded but not pinned;
  - near the wall, a stop may be labelled WRAPPER_ERROR rather than WALL_CAP.

## 4. Hashes (each computed from the file bytes)

| File | sha256 |
|---|---|
| `producer_A/owned_shared_junction_reference_producer_v002.py` | d5238c5295e3edc99d00450e2f4caa7c40a7234757215c773cd173a38866ec51 |
| `producer_A/SHARED_JUNCTION_REFERENCE_FROZEN_SPEC_V002.json` | 1a0b4c49d8ea2bb3ebb5f60dbbe5ae4a0a8a1b0e46a65f4167652fc9ad982525 |
| `producer_A/producer_V001_to_V002.diff` | e79f8128fe7ba35a0e007c846ce584d9b8442dc1afd5fb95a64bf034eeeafe21 |
| `producer_A/SPEC_V001_TO_V002_DIFF.json` | e17d34aa1c17129376d7c46a320d48daaf31a8a3cd254f29d59b7775a5e0e961 |
| `producer_A/producer_0351V002_to_0355V001.diff` | 8131892f1fdfdf5ad0b9ddf8bfb5c146d526ccccb4621a3d62c7c0615215f1ed |
| `producer_A/IMPLEMENTATION_NOTES_V001.md` | d0663510ad52cca3a094cc9e1aec44b798d7edd6b9d773df25703be75a092c01 |
| `producer_A/IMPLEMENTATION_NOTES_V002.md` | 5c315655c099d22c692094ec844bc3de9b269752ed9b47c791fb72538790118f |
| `producer_A/test_shared_junction_producer_synthetic_v002.py` | 8e12f28f827ae7e8f0a59676baa656fa6212ac0f3130cf8857da6c30d99a9b3f |
| `producer_A/SYNTHETIC_TEST_RECEIPT_0355A_V002.json` | 31c48272e1cc3876daae7bc5751ecbda6104fe9a4090dc43bd00577a94da32ab |
| `producer_A/FILE_MANIFEST_0355A_V002.json` | 40bc2aab7947192f986044c71ab3aba848b25f0682f19532c21276cb509ba3fb |
| `launcher_B/shared_junction_reference_root_launch_wrapper_v002.py` | e03da7d8ac6cb16851cff0c288e9bc277303517cfcce438dc94b2d04cbb054dc |
| `launcher_B/shared_junction_reference_outer_driver_v002.py` | 67dd3c8f0175c21d6a0b658cf38a38452bcf525ca2ca9484fecdb8056a7a065e |
| `launcher_B/bind_V002_to_shared_junction_wrapper_V002.diff` | bec1cc20466fb401c7c657872d5f2e653c9229f51ad9c2708111a5cb1699d8e8 |
| `launcher_B/bind_V002_to_shared_junction_outer_V002.diff` | 16bc9110c5115a1e12531fb25c42d98f634f1345eb7aefd7184097efef9879ff |
| `launcher_B/shared_junction_wrapper_V001_to_V002.diff` | cb403ae31c3971b5257c92ef249e79425aedaaebdbbbeeffe515ca2fe1d6a404 |
| `launcher_B/shared_junction_outer_V001_to_V002.diff` | d64ae3d8945f4e5d7f3ac61e519e0df0ff0afcbfb6bc65d774dc5916643f7498 |
| `launcher_B/DIFFERENCES_V002.md` | 7a4c32c5efa91c15021937605610d94a4df79943600a9b1913a77fbf0af75aab |
| `launcher_B/DUMMY_TEST_RECEIPT_V002.json` | ffc674dda6dc56061ab1d6daba18d12d261efe8b4096544ce6f14d984fecc0ae |
| `launcher_B/dummy_launch_harness_0355_v002.py` | 42dab89b16bdd7cc5c70ee10f3153df6ec4f300f01eb51ad3b5db6903d86b443 |
| `launcher_B/selfcheck_0355_v002.py` | df44935585cf87f6e0a70cb043129e0e407370c388ee075159ce33ae9fae433d |
| `launcher_B/build_0355_v002.py` | f5f047962db7b5f166faf50b2eb99be700b5d26483b06553bcb22d73e3d55b65 |
| `launcher_B/RLIMIT_PROBE_V001.py` | 7541a6989f7df83d11870b689ca6841eedeec45b72db1874c795b15d83623420 |
| `launcher_B/RLIMIT_PROBE_RESULT_V001.json` | a8ab45b9c3bc69a2120ff77d7d26c21f980c1c9389955ee0ed8e6e15f1f41d6d |
| `launcher_B/FILE_MANIFEST_V002.json` | 4449da80047d24124366681e3e418175be174ba3471a0ad3933b9fd493d9360c |

| Superseded, retained (do not launch) | sha256 |
|---|---|
| `producer_A/owned_shared_junction_reference_producer_v001.py` | bc3bed35a1d5f96b9754c51061180e1d16ac999737d2f5aa7dbdf8932aec1f37 |
| `producer_A/SHARED_JUNCTION_REFERENCE_FROZEN_SPEC_V001.json` | 72cc00f1f409fc9157b5cd93695186b839b1d54f736b1330a7012342268bfe46 |
| `producer_A/FILE_MANIFEST_0355A_V001.json` | 426b34fe1a36a107379e0548153771d2e91bcd8f3774f09d576bc41b56770405 |
| `launcher_B/shared_junction_reference_root_launch_wrapper_v001.py` | 57fb374bfb20b4b50833d6d699e6dd6ffe0b553260d4bfab33a709d6a080c087 |
| `launcher_B/shared_junction_reference_outer_driver_v001.py` | 7a5ad7ef57b2e0bae743aa33bbdbef5fef626ba8c8ba87fde3b38fbf8b96c628 |
| `launcher_B/FILE_MANIFEST_V001.json` | 1e2f47598a34a53f0b1eb7fe618c271ce1e72b0698df1d880ebee52ef6217c3e |

| Review evidence (read-only copies) | sha256 |
|---|---|
| `review_0355A/harness_stderr.txt` | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| `review_0355A/harness_stdout.txt` | 5bee98e990270633b5f09539e3765c6e5999a9b0ad3547abbaef65969c448b1d |
| `review_0355A/probe_matvec.py` | 8085d19a3b9d86142db4f7848b6f9fd28ffc6e8bb6f6b8cdb632b14faf2a5278 |
| `review_0355A/probe_matvec_stdout.txt` | b3954d40efc9a3ce733077aa617d92e86239b60e819f6ff39ca97fc597864e2d |
| `review_0355A/probe_oracle.py` | 2251186bfe5471ed437782095d6690007238491d53833c6229ed4bebdf5126c3 |
| `review_0355A/probe_oracle_stdout.txt` | eb2482ea695f34d81a778fd6be1bfbe49ec339d3b1e42530d6e513f50985d1c0 |
| `review_0355A/probe_resources.py` | 3b6ce0e1f9adecf36f45f29d0ffe69e03e05eeb724c9bab274e6abd362bb1a97 |
| `review_0355A/probe_resources_stdout.txt` | 4b61bbeae23aa5c285775aaeac2926d344389e3cd32e009aab6f5ffd5a615d0a |
| `review_0355A/probe_structure.py` | 86ee3d0680a08d4ffd1ba022f87164fad07803d61956af064a3f286217b2dc91 |
| `review_0355A/probe_structure_stdout.txt` | 3115773628693c81ecec964865d58a3efd1e81d15267ce95bbefc6a940dad398 |
| `review_0355A/sj_probe_lib.py` | d19d87b8ea61b389d09206af205df114fd10d8625e54a3709fcda6fa0d05447c |
| `review_0355A_v002/harness_v002_stderr.txt` | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| `review_0355A_v002/harness_v002_stdout.txt` | 93b1bccb08a909a83aa3b07797cdbe8882057c5efb8482796eb3506b41eb89a5 |
| `review_0355A_v002/real_pin_hash_check.txt` | ec557c1beddc110128d69b67319f1d87b7226004253e6f5733a950eb433e6f34 |
| `review_0355B/astdiff.py` | b761e55b3e79f28a400ba0a78f51ee6be23e0bfe1b35419e5ed46857f8bcd335 |
| `review_0355B/harness_summary.txt` | faafd58ca6073f9fcf7265900727960cc9f6f6d87fe174c0085adfc38cd6dc5b |
| `review_0355B/integ_results.json` | 05f9752c7442722af488d39062912da2a8276d055d737aca5eddc35e8bb2a0c8 |
| `review_0355B/integ_sj.py` | 26ab9262968b1fc15bce7a4590f6977d1c8e91cacdd5111db737a520cf4537ca |
| `review_0355B/integ_stdout.txt` | 8866de5f7d8b4c577049e9f30f831bad1cfcc9914eeb208f99354ddc11b15039 |
| `review_0355B/launcher_B_hashes.txt` | 36fa234c5bc6d27e0900ec492fe816d85a6c9d2e1ece3aecab6334ebf3a6ff5d |
| `review_0355B/pin_crosscheck.txt` | 6e8b19c6b111e8a3df6f236458f5fec4493f77e6ab7ab4e3b8e04bb7e80f5a0b |
| `review_0355B/results_runs_1792085441.json` | 4a34da5544ec5f4e0789aacec087529b291a014c00281be41e848d14b0dfce3c |
| `review_0355B/rlimit_probe_rerun.json` | 733da359ac5fd675920ee2ae7c289061fa51268bf84c413b804b5a4a77360ab6 |
| `review_0355B/selfcheck_stdout.txt` | acba71dfd4690d7e5c07b1bcb30b5b502585ff5cd5df85ee49360cef6ff97d05 |

Earlier review-evidence copies and the remaining V001-phase launcher evidence are listed in `launcher_B/FILE_MANIFEST_V002.json` and `producer_A/FILE_MANIFEST_0355A_V002.json`.

**Status:** producer A REVIEWED; launcher B REVIEWED; this index's launch-order fix (F1) awaits the reviewer's confirmation. No native case was executed by Claude.
