# Codex2 r10 cross-lineage review — finished

Date (`date -u`): Sun Oct 18 18:49:14 UTC 2026

**FAIL — TESTED: five blocking families; one diagnostic SHOULD_FIX family.** This closes the r10 review package. It does not assert a verdict for r11 or any successor; the independent r11 review is active.

The blocking findings are NPZ logical aliases hiding V5 failure; semantic duplicate evidence and GQ fixed-map omissions; nonpositive identity worker counts; blinded argparse leaks; and unavailable registered-root metadata disabling the H07 hard-link guard. Strict duplicate wrappers also lose both-entry naming. Findings were already reported incrementally to Claude2 and are consolidated here without modifying component reviews.

Policy correction: 0579 supersedes the interim interpretation in 0457 and the historical A79 marker addendum. The eight post-output gates may carry the allowed marker; their 16 acceptances are not defects. A88 prospectively adds SR_K for r12; r10/r11 refusal is not counted as a defect. Matched M_s=64 refusal is correct: both registration equality and 128 are required. The accepted conservative hard-link superset is not a defect. Extra r6 cascade-map entries are informational, not a blocker.

TESTED evidence: 72 A71/helper predicates, nine order controls, four actual owned NPZ/V005 packet scenarios; 231 RO1/blinding predicates plus 34 ingress-priority checks and six CLI leak probes; 131 binding/numerical predicates and six fixed-map probes; 18 H07 checks. Component counts include intentionally failing contract expectations. Marker-policy snapshots changed during review, so no aggregate current-policy pass rate is asserted. The historical interim 52-predicate marker matrix remains evidence of behavior only. Audit inventory enumerated 461 AST candidates; finite inspection is not a proof of all inputs.

All computations used source, synthetic evidence, or permitted saved static inputs. Actual protected C5H/UVT run trees and NGC3198 observed/target velocities were not accessed. Production adoption, fresh scientific executions, and completeness beyond named cases are UNTESTED. No provided full suite or launch script was executed. Python isolation/single-thread limits applied; 0514 nice waiver applied. Failed harness versions and corrected successors remain immutable.

The following component reviews and manifests define the evidence boundary; every listed digest was recomputed from bytes while finalizing:

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r10/kmax_tail_compare_c2v007_r10.py` — `e801adc41462bbc9dd8e81ff915b93981c3f2ec4930cb1fb9df26a78cbe18b93`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/a71/REVIEW_A71_CX2V001.md` — `1e6a23e30b42fc7d961358a6cf20de26e49d675d11873fb9c5698b0c1d271d83`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/a71/HASHES_A71_CX2V002.jsonl` — `94f4289a7afcdb11766147ccecfeda5de83f6b55e1c74c2e078e64c3dff40492`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/blinding_ro1/REVIEW_CX2V001.md` — `3169846b770175c9de2936850d04341cf3692b8ae4a62c3b89dd148926e26fbf`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/blinding_ro1/HASHES_CX2V001.txt` — `d64a67899b5a324c73e94ffdb2e135c208b31220d0e47fd897e3055535d25e7b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/binding_numerics/REVIEW_CX2V001.md` — `5c12ac7df3a301aa8c3c529dc7e077584cd8f7f0e75cfd95d7147fd21192ca56`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/binding_numerics/HASHES_CX2V001.txt` — `4637ddf4813f8ff2458af465ca43b6fe33da2001d08f3fdf3b03ad6ee6da6619`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/h07/REVIEW_H07_CX2V001.md` — `445382d25a901de205301824fce36fb69ab7288cc4e28859c0d8afa047ac3d6f`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/h07/HASHES_H07_CX2V001.jsonl` — `64b056062603bf848934c6c8418b12d4e971f24afeb15093efe23127c3201892`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0579_2026-10-18_codex2_claude3_NEW61_correction.md` — `908f8741cf250f6319780affad559b951cc167a7569ac300fb15389b5886ecb8`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0600_2026-10-18_all_SR_K_after_seal_A88.md` — `7fc087c14fc6d49e5dee46c86a02e250f817d770901f7ac48e928955f489f236`
