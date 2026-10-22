# Compare r8: independent noise and R-PAIR review

date -u: `Sun Oct 18 15:33:39 UTC 2026`

**PASS in the assigned numerical/R-PAIR slice. TESTED: 85/85 independent synthetic canaries.** No actionable false-pass finding was found in this slice. This is not the overall compare verdict and does not establish scientific or sealed adoption.

The target is imported from its unchanged bytes. The suite never imports the supplied tests or invokes build_context; the supplied tests have real-record reads at module scope. All histories, run dictionaries and manifests are independently constructed. A Fraction oracle computes bounds from the represented synthetic row values, independently of the target implementation. There are no target monkeypatches.

The applicable noise rule is the latest A58 RI-18 reading, overriding the cap still transcribed in draft r2: q/(1-q) without the 0.9 cap at norm level and for same-sign rows, q/(1+q) for alternating rows. Either of the last two norm ratios >= 1, or any last per-row ratio >= 1, makes E unavailable. Exactly one increment uses the norm directly. The geometric/contraction interpretation remains DECLARED; these finite histories verify code behavior, not a theorem about future iterates.

| Area | Independent evidence |
|---|---|
| Uncapped arithmetic | q=31/32 norm case and a slow same-sign row hidden by a faster norm; both retain the larger bound. The latter forces R-PAIR. |
| Alternating rows | A slow alternating row whose own bound dominates the norm; exact-rational oracle and sign-kind checked. |
| Unavailable E | Both NEW-7 ratio positions, same-sign and alternating q_i=1, zero previous/nonzero last, no increment. |
| Record problems | Pass gap, S9 sentinel, missing/nonfinite row and final-pass mismatch. Record defects do not become decidable. |
| Pair selection | Inclusive tau/8 equality; next float above it; worst normalized row; EA-dominant ROUTE_A; exact tie PICARD; unavailable E forces PICARD. |
| R-PAIR result | Missing pair pending; wrong branch or invalid member incomplete; still noisy member at iteration floor; member gap incomplete; member rows used after resolution. |
| A53 inheritance | Base flags retained for PICARD, member-only flags not substituted; PICARD EA entry substitution rejected and base EA retained. |
| RB_FP | Independent noise/kappa arithmetic; unavailable base triggers PICARD path; resolved members used; unresolved member or zero shell sum incomplete; ROUTE_A RB_FP manifest refused. |
| R3-4/V6 | Actual case_validity accepts planning column_workers=1 with admitted parallel base record; rejects serial-record substitution, changed base result/identity, changed tail record and unregistered numerics; ROUTE_A cannot reuse base identity. |

The R3-4 positive control explicitly asserts synthetic V4/V5 and I1T seams. It tests the actual case_validity R3-4/V6 code, but does not reconstruct a packet or certify I1T. Result/receipt dictionaries are synthetic adapter-layer fixtures; this suite does not prove real reader custody. The own manifests test manifest structure and RB_FP branch refusal; full CLI and complete global ADOPT_TAIL evaluation are UNTESTED by this slice.

Source review additionally checked the evaluate_v007 caller: it derives member validity, compares registered R-PAIR leaves between members, invalidates contradictory PICARD EA entries and detects aliased result hashes. Untriggered members are refused before T-tests are evaluated. The RB_FP leaf relies on load_manifest to enforce its PICARD-only branch; the independent own-manifest negative verifies that boundary. These caller observations are STATIC REVIEW, not a full scientific execution.

The run took 0.090434 s, peak RSS 55590912 bytes, isolated Python -I -B, single-thread BLAS environment, default priority under the 0514 waiver. No scientific launches, external run/receipt reads, observed targets, network, or session logs. The late-pass floating-point floor on the first real 12-pass member remains UNTESTED; the observed-ratio contraction assumption remains DECLARED.

The open V005 addendum is recorded by bytes at the test and final review; an append changes its hash and requires checking for newer relevant rulings. It is not represented as a frozen file. Its hash changed during this slice: **True**.

Source byte pins (all cited source files):

| File | SHA256 at final review |
|---|---|
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r8/kmax_tail_compare_c2v007_r8.py` | `bd51db152f700afd86c2156904a4998b4582deeac5c06d05def50b27b397e5c3` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r8/tests_kmax_tail_compare_c2v007_r8.py` | `1735a5e26d82b81d9e7424286d47eddea8c35f1ef1999191321720e393f90769` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r8/FIELDS_R8.md` | `40253fe52f04caf081080e1b28826c70625fa033fcf5343e418b29b8ff8e644b` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r8/COMPARE_V007_IMPL_R8.md` | `947248bbb239cd684c8521e0659238d35b8c7f795eb2e50d92bf03b7c0b1ccaa` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r2/KMAX_TAIL_PREREG_V007_FINAL_DRAFT.json` | `58a0b87d995ce06e13706c127e3783dc352a292f0ec1614cf9b9b877b6140bfa` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r2/CLAUSE_SOURCE_MAP.md` | `c6a0287c7d763286b5764fa073c1c7f0f7a3d0ceafeca4cc7ac1a157b0ebb6a1` |
| `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md` | `487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b` |
| `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md` | `b940c46fde1213c3536b28221c3bb51bbd6caca410b1fa157ca9ada839b2ca6b` |
| `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0558_2026-10-18_codex2_crosslineage_review_compare_r8.md` | `dbec760754966a7d4cbdb6ee00815eeb6750e0e8746bc20137adf5cdcfd1fe36` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/numerics/numerical_canaries_cx2v001.py` | `867ee9f1e8d2a47c7ffa6df540b4b1bdf2aa4cd0196149e404989285109cac96` |

Artifact byte pins:

| File | SHA256 |
|---|---|
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/numerics/NUMERICAL_REVIEW_CX2V001.json` | `289f7a7b4a6d2c9c84953d276b44f88f23e0127a906dbc7b06bd99db9f5a5ecc` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/numerics/finalize_numerical_review_cx2v001.py` | `3ebb59605f658d55b533a07fc29e958b76813d73ba57a8a1be8640e71b0bab4a` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/numerics/numerical_canaries_cx2v001.py` | `867ee9f1e8d2a47c7ffa6df540b4b1bdf2aa4cd0196149e404989285109cac96` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/numerics/synthetic_v001/NUMERICAL_CANARIES_CX2V001.json` | `1b9b2c50de892ceea4e1176a4356524cda68c5bc70adb3aa2fe914972fea2c9b` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/numerics/synthetic_v001/manifest_picard.json` | `61186679d45b05dc43a1870cd48280e98509d351a4c6c7b39d49e1364245b75b` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/numerics/synthetic_v001/manifest_rb_wrong_branch.json` | `5b07eec5efbfd8f0f531a65364940350080015497a957c5d25876dd79f1b32d1` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/numerics/synthetic_v001/synthetic_histories.json` | `324288d4489d7909c8f5947e5a3b7ce379b4f571e75435d69ee0562bf9837489` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/numerics/synthetic_v001/synthetic_result.json` | `2706fe58766de90d8948d92f717fbb29e2af6d5c765fea9d28fa0ce1e8597f14` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/numerics/synthetic_v001/synthetic_rpair_records.json` | `27a7f1a1fba2aff02a005c304e6c76854ad223283eedfc379d6b63b865f5658d` |

The companion HASHES_NUMERICAL_CX2V001.txt manifest includes this report and every local artifact. Its own hash is provided to the parent separately to avoid a self-reference.
