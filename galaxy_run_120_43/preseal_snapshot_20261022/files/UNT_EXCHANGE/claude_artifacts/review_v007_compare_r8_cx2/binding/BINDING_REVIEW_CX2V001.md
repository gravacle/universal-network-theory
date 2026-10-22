# Codex2 binding and certificate-parser review of V007 compare r8

date -u: Sun Oct 18 15:35:21 UTC 2026

FAIL in the certificate-parser slice. TESTED: four duplicate-shell canaries return PASS despite an above-threshold entry. The source pin remained unchanged. No scientific execution, production inputs or full sealed CLI adoption was tested here.

B1 (blocking reader correctness): _shells maps shell ranges to scalar bounds with last-wins before _g_lo checks thresholds. A LO [4,5] entry with max_over_tau 0.1 followed by the normal 0.0001 entry returns PASS; its reversed ordering returns RECORD_DEFECT. A duplicate extended [363,370] pair also hides a 0.1 violation. The same required-shell issue reproduces for LO_NGC. FIELDS requires every LO shell <=0.005, and A54 S5 rejects a passing verdict that contradicts its data. Synthetic exact record-byte registration does not repair this semantic defect. The LO after-seal registry marker repeats the false PASS. Reject duplicate ranges before any dictionary construction and validate each raw shell entry; audit analogous list-to-dictionary conversions in an immutable successor.

These tests use owned synthetic record and registry files, an inert owned producer and the target's actual evaluate_gate. The NGC test uses only the literal operator SHA from source; no NGC operator, observed or target velocity file was opened. Full ADOPT_TAIL composition is owned by the separate admission slice, not claimed by these probes.

Deferred requirements, distinguished from B1: A68 CHK-1 explicitly assigns registered gas.M_s binding to a round after r8. An isolated g_LO/evaluate_gate call with a deliberately inconsistent M_s64 context accepts the hardcoded M_s128 certificate. The normal CLI rejects such an invalid registered case block, so this is not an end-to-end bypass. A69.1 explicitly assigns producer paths and producer-byte hashes to the successor: a registered claimed producer SHA plus a nonexistent producer path currently passes B2, both with exact record SHA and with the after-seal marker. The producer is never read. These three probes document declared pending work, not surprise r8 regressions.

A62.1/A67 N3 RB_FP shell-domain controls pass 12/12 using actual evaluate_gate and owned records: exact [4,sqrt(2)*128], low excess/shortfall, one-ULP top excess/shortfall, gap, overlap, missing ranges, extra dV key, false full-domain declaration, reversed interval and duplicate labels. No field-validator patching was used.

Counts: initial binding suite 13 checks (7 expected outcomes, 3 duplicate-shell false PASS cases, 3 deferred-rule probes); LO_NGC 4 checks (3 expected, 1 false PASS); RB_FP 12/12. Total29 observations,22 matching desired rejection/control expectations,7 mismatches classified above. This is not a pass percentage or scientific claim.

Binding precedence: A58 RI-18 removes the cap still transcribed in unsealed draft r2; numerical slice tests the newer ruling. V005 remains mutable; the saved snapshot records bytes observed at the start, not a seal. INPUT_PINS_CX2V001 omitted the provided suite because the singular test_ filename was guessed incorrectly; the actual plural tests_ file pin is listed below. No supplied fixture or test module was imported/executed.

Python -I -B, numpy/stdlib only; single-thread environment; nice unavailable under the 0514 waiver. Audit hooks restricted fixture/source reads and denied production run paths. All writes exclusive; reviewed files untouched.

## Byte hashes

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r8/kmax_tail_compare_c2v007_r8.py`
  sha256 `bd51db152f700afd86c2156904a4998b4582deeac5c06d05def50b27b397e5c3`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r8/tests_kmax_tail_compare_c2v007_r8.py`
  sha256 `1735a5e26d82b81d9e7424286d47eddea8c35f1ef1999191321720e393f90769`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r8/FIELDS_R8.md`
  sha256 `40253fe52f04caf081080e1b28826c70625fa033fcf5343e418b29b8ff8e644b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r8/COMPARE_V007_IMPL_R8.md`
  sha256 `947248bbb239cd684c8521e0659238d35b8c7f795eb2e50d92bf03b7c0b1ccaa`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/binding/test_binding_canaries_cx2v001.py`
  sha256 `7c08c5facc8ac50588f8753f47264a0c4da810d0aed610ad4d315f8842ad39f6`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/binding/BINDING_CANARIES_CX2V001.json`
  sha256 `388c3a0e26d09d0dab84728dee7d3f8f85edecce6c1915d0e9bc85c1999aaba3`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/binding/test_lo_ngc_duplicates_cx2v001.py`
  sha256 `0c19eacd709b5414c516cce96cc73e5d05245c8e5851902b87c3409bd28d474c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/binding/LO_NGC_DUPLICATE_RESULTS_CX2V001.json`
  sha256 `8c588c448bff2cbec9acdea33a5b8a73b229c3d7ed23b36da25d0bbeaf1ff52b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/binding/test_rbfp_ranges_cx2v001.py`
  sha256 `175c76ce719f5af140045850cf5e01bceccbdb8391503788d808c622e8c5b88a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/binding/RB_FP_RANGES_RESULTS_CX2V001.json`
  sha256 `c9fdf59b563b77e74bd0b13cd51ec58f66c84375b4b45f10f63e6460110de9a1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/INPUT_PINS_CX2V001.json`
  sha256 `56f722b47f3885b2a0c34a8607463c07272d2c3ef528a476e56f822334ed84a1`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_r8_cx2/V005_OPEN_RULINGS_SNAPSHOT_CX2V001.md`
  sha256 `a16069c2bc524f22ac59d67841899a95bc7fc4438d0b6edf31bcdd6db5ec3e09`
