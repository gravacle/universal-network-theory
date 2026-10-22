# Seal tools v003 C01 — provisional T3/builder integration review

date -u: Sun Oct 18 22:52:44 UTC 2026

**PASS within this provisional integration scope: 46/46 checks; zero new blocking findings.** The tested tuple is the immutable snapshot_v003 manifest, not current author development files. This is not final tool selection, a real seal, scientific acceptance or launch approval.

Actual snapshot common/T1/T2/T3/builder code ran under a read/write/process fence with exclusively created invented fixtures. The scientific comparator was an explicitly owned inert API double; its synthetic certificate and build assertions carry no production meaning. No actual comparator or protected run was imported or read. The prior complete integration harness was adapted under a new name; its old outputs remain unchanged.

**TESTED parameter and evidence flow.** Builder `addendum_at_text_of_record` reaches T3's `text_of_record_addendum`, then T1, unchanged alongside the exact disposition path/digest. T1 returns the verified old-copy {path, sha256}; T3 carries it through; the builder requires it and includes it in the returned record. The complete positive uses a cited pre-table A62 change and later A102. Returned disposition content, raw text and digest exactly equal the input bytes. The record hash matches the builder's reported hash.

**TESTED failure propagation.** Missing, nonexistent or wrong-byte old copies refuse through T3 and builder, and the builder returns no record. Supplying the old copy without frozen context refuses. Removing the verified old-copy pin from T3's returned evidence refuses at the builder. Wrong disposition pins, empty reasons and wrong section hashes refuse. Injecting different disposition bytes at the builder's reread refuses even when the parsed object is semantically the same.

**TESTED CLI behavior.** Actual in-process T3 and builder CLI parsing carries the new flag and exact disposition pair. The positive CLI record retains both evidence objects and hashes correctly. Missing old-copy and wrong disposition-pin invocations exit 2 with refusal evidence on stderr and empty builder stdout. No subprocess was used for these CLI checks.

**Source delta confirmed.** T3 adds one optional API/CLI old-copy parameter, forwards it to T1, carries the verified result, and refuses the parameter without frozen context. The builder forwards that parameter, requires its verified result, and includes the pin in its record. Common/T2/tool5 are unchanged in the provided snapshot comparison. This review does not alter or widen their contracts.

**Custody limit.** The old addendum is read once by T1. The builder carries that verified snapshot pin; it does not reread old bytes after T1, whereas it rereads disposition bytes. This establishes the stated snapshot-evidence flow, not ongoing file immutability or protection against arbitrary concurrent path replacement. All source modules were byte-checked before compiling their exact buffers.

**UNTESTED / separate scope:** exhaustive C01/0640 T1 semantics belong to the independent helper; actual production comparator behavior, certificate/registry admissibility, native seal and scientific outcomes remain untested. C02–C08 are outside this assignment. Final publication and root-script integration still require their own exact selected-tuple review. No target arrays, protected-run metadata, network, session logs, overwrite or deletion was used. Python ran isolated (-I -B), nice10 and single-thread BLAS; unexpected audit denials were zero.

## SHA256 from bytes

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/c01_integration_cx1v001/controls/RESULTS_CX1V001.json` — `d38d6d5f0b643db18bee73f73a61204e71bb060075fba5d7fda0fce3daa7d41d` (12100 bytes)
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/c01_integration_cx1v001/review_full_integration_cx1v002.py` — `35d279cce9e6a845fa653365bf07a927ab26ed543efb05407d06218a90ce42bb` (19647 bytes)
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/review_full_integration_cx1v001.py` — `cd16ae7dc7041737b69136a235d05292d7673e5dc7c892ac15d3a92612daa475` (13921 bytes)
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/provisional_snapshot_v003/SNAPSHOT_CX1V003.json` — `efeaf91ba122e72101898f4574dea79964487f3222af1591dd8dc207791bf996` (2912 bytes)
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0640_2026-10-18_claude4_claude3_D05_rule_and_contract.md` — `03b4ff4987fd3a82a3a46692a7ab75beddd9d78788373863ea3b2dcd3db91138` (1235 bytes)
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE4/0109_2026-10-18_r5_check_r6_recommended_v002_check_scope.md` — `d0b20717170661f7bcc7b5866fd6f8c074dc5058929c4e669d0515c962983bc7` (4676 bytes)
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/provisional_snapshot_v003/seal_common_c4v003.py` — `101a3aeb9846a21c35993e8e7e4b50a8f1206ed4202b131afd12d7e496c5ab21` (12990 bytes)
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/provisional_snapshot_v003/check_frozen_addendum_c4v003.py` — `a56f8d793750151920b1b47e77b46aebbfadea71fe77730f360beb02af788fb4` (33207 bytes)
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/provisional_snapshot_v003/check_sealed_compare_c4v003.py` — `c2c5dfc5ddba1e44ff82811a38d4c05b0a669f2294b229efe3437623d596f9f1` (10934 bytes)
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/provisional_snapshot_v003/check_slot_fill_c4v003.py` — `316973a1abf5aa2151dc1a517733d970ce1004313395d05fe590f82ed439b0af` (40090 bytes)
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/provisional_snapshot_v003/build_seal_record_c4v003.py` — `de0ceb15ebfb95e04227730bd2785eb46af8cb5980012de91de98f34ea226b96` (34429 bytes)
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/provisional_snapshot_v003/print_driver_build_record_c4v003.py` — `e5bedffe3c91650d5dba7fbd1ed5476e228158679d8959dfea0e2eff436ebdea` (4192 bytes)
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/c01_integration_cx1v001/controls/RETURNED_SYNTHETIC_NOT_AUTHORITY.json` — `4bc68f2db5e733ab5335a8ad32d2eaecd20e5df089302ac05fa71ff257d5f586` (19858 bytes)
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1/c01_integration_cx1v001/INTEGRATION_REVIEW_CX1V001.json` — `7c47eb5be7010a1a7cb526ecb8d98f2927f8744b60771028c74213fc3a7af9cb` (5070 bytes)
