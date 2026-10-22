# Final compare r10 binding/numerics review

`date -u`: Sun Oct 18 17:09:38 UTC 2026

**FAIL — component review.** TESTED: 125/137 predicates pass; 12 mismatches. This is a requirements test count, not a scientific pass rate. The main suite is 122/131; a bounded follow-up is 3/6 (positive GQ baseline and two hygiene checks pass; three false PASS cases fail the requirement).

Candidate before/after SHA256: `e801adc41462bbc9dd8e81ff915b93981c3f2ec4930cb1fb9df26a78cbe18b93`.

| Item | TESTED result | Disposition |
|---|---|---|
| A75 P-SF1 / A05 | Three correct-plus-wrong same-name GQ geometries read PASS; three wrong-only geometries read FAIL, not RECORD_DEFECT | Blocking, one family; deduplicate parallel A71 finding |
| A75 P-N2 | SR_K marker refuses at loader and gate guard; other 48 marker predicates pass | Current ruling mismatch; NEW-61 declares older restriction |
| A75 CHK-1 | Matched128 passes and mismatched context refuses; matched64 also refuses | Current ruling mismatch for LO/GQ; DOUBLING is stricter extension under RI03/NEW-67 |
| A73 F2 | 9/9 LO gas/embedded-tail/build echo mismatches reject | PASS |
| A69.1 | 9/9 path, byte, registry and actual-gate controls pass | PASS |
| A72 | 11/11 custody controls pass; two map-negative controls pass; extra map accepted | Informational declared-contract gap, not standalone blocker |
| RB_FP / numeric / ties | 12/12, 12/12, 5/5 | PASS in owned synthetic scope |

The GQ false PASS has an exact-byte registered record, a real owned producer file whose bytes are hashed, and root-registry-shaped synthetic production node counts. It passes actual `evaluate_gate` without substituting any gate function. Every required correct roster remains present; an added same-name C2T_KB256, C3T_KB256 or C4T_KB512 is self-consistent but violates the fixed roster map. Required-roster coverage is met by the correct entry. No whole-decision ADOPT_TAIL or production result is claimed.

The current A75 snapshot says the final round must close these items. R10 BUILD acknowledges contrary interpretations in NEW-61 (SR_K), NEW-66 (GQ outcome), and NEW-67 (constant128). Those declarations are not treated as amendments to the ruling. The M_s64 probes are direct gate binding controls, not a claim that a production M_s64 case is admitted. DOUBLING still has a separate RI03 production128 rule; LO/GQ are the direct A75.8 cases.

For A72, only the selected custody validation was tested. The declared BUILD phrase “remaps nothing else” is stronger than the implemented selected-pin check. An unrelated extra map entry passes, but a full legitimate cascade has additional mappings; this is reported as an informational scope/wording gap. Scientific cache equivalence, adoption conditions, production build validity and full sealed-mode workflow are UNTESTED.

Guarding and scope: before the candidate was executed from its hashed bytes, the harness installed open/list/scandir audit guards and wrappers for os.stat, os.lstat and os.readlink. Production runs, runs_ext, /.vol and session-log paths reject before access. c5h_path_hit was never called. Successful runs have zero blocked events. No production evidence imports, supplied tests, solver launches, network, git writes, overwrites or deletions. All fixture writes are exclusive. A first harness version blocked the ordinary argparse stdlib import; it is preserved and excluded from counts; immutable v002 preloads inspected stdlib imports.

Every cited file below is byte-pinned; all owned files and these inputs are covered by HASHES_CX2V001.txt.

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r10/kmax_tail_compare_c2v007_r10.py` — SHA256 `e801adc41462bbc9dd8e81ff915b93981c3f2ec4930cb1fb9df26a78cbe18b93`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r10/COMPARE_V007_IMPL_R10.md` — SHA256 `fd6f877910e89c5a9b182e92d3cb95faa8285581d6f000e05e7b0c48c0a1ad06`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/OPEN_RULINGS_SNAPSHOT_CX2V001.md` — SHA256 `2da736b5f4f8f6c007035996218f98838c2766b4a4daf11ca62ab3d3ec254827`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/INPUT_PINS_START_CX2V001.json` — SHA256 `cd140f3c02c5a58bdbf79bf508708842f47309ee1015b5b20444a366172bac6a`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/prep/REQUIREMENTS_TEST_CROSSWALK_CX2V001.json` — SHA256 `727bb76e6876aa07a0ce8154546fee1ad92439921de9783b6a8c07999059db14`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/binding_numerics/probe_binding_numerics_cx2v002.py` — SHA256 `6850d2a3a692228a8d47196985a2f56c3b9d1c63b85adf7634c98e0df2ba97fc`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/binding_numerics/probe_gq_fixed_map_extra_cx2v001.py` — SHA256 `ccef031e6bea07e0ed8f67cccf6113d1e642f38ce1a97ff30865e1c62805da34`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/binding_numerics/run_20261018T170832Z_89887/RESULTS.json` — SHA256 `d492b2a6cbd0e1320935e07e64a021a25a5ef9b3b38bd1a71f84931c2168893b`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/binding_numerics/run_20261018T170914Z_92452/RESULTS.json` — SHA256 `51ef6269be3fcc32f8b00589f8e265a2151d72fa06dd47b63980799383685664`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/binding_numerics/FINDINGS_CX2V001.json` — SHA256 `278aa5f47b8861f3325625aeb78e86ae4cc00346e2c49376dd1d2db6a3cc0e88`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/binding_numerics/SUMMARY_CX2V001.json` — SHA256 `039105fd0732aa0fccdabf24d1e776e23d17caf1f1689073f2fddb7f21de1dbf`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/binding_numerics/REPRODUCTION_INPUTS_CX2V001.json` — SHA256 `b82af2cb7fb149d2a3e55c063ddd25777cd2a19c1c574fcb6324de0aa2461fb6`
