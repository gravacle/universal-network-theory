# Codex3 identity comparator, Z2 token and R-PAIR review

date -u: Sun Oct 18 12:55:40 UTC 2026

Component verdicts: explicit Z2 token addition PASS; current requested R-PAIR member set FAIL against A53; comparator PASS_WITH_FINDINGS on source/synthetic coverage only. The three original UVT run-byte comparisons are UNTESTED because the principal directly forbids those reads. Certificate review is a separate component still in progress. No launch or scientific adoption is performed by this review.

TESTED: an independently written harness constructs32 small run pairs,16 each for Z2 and B0P_RERUN, from synthetic arrays and records. It imports only the pinned comparator, driver constants/definitions and checkpoint codec; it invokes the comparator in-process with no subprocess, network or scientific worker. An audit hook forbids destructive writes, forbidden-run reads and any overwrite. The first harness completed the B0P cases but stopped because the synthetic Z2 builder expected an explicit worker token inverse; the comparator intentionally derives that worker pair automatically. Its immutable successor supplies the actual documented base worker and completes both positive baselines. This is a harness correction, not a comparator repair.

Both baselines PASS. A one-ULP alteration of a compared result speed, stage JSON metric or NPZ numerical value FAILS. NPZ signed-zero, dtype changes and missing NPZ FAIL. A stray tail record fails B0P_RERUN; Z2 masks it by the registered tail-ON exception. No roundoff tolerance is applied to NPZ data: dtype, shape and raw array-byte hashes are compared.

TESTED limits, reproduced in both gates:

| Perturbation | Comparator result | Review finding |
|---|---|---|
| New-only numerical NPZ or JSON | PASS_BITWISE_EQUAL | Existing S2 reproduced: reference-only file enumeration misses extra outputs. |
| Existing stage field.npy changes1 to2 | PASS_BITWISE_EQUAL | The stage loop compares only NPZ/JSON/JSONL content; other file suffixes are checked for existence only. |
| Stage request numerical argv changes0.01 to0.99 | PASS_BITWISE_EQUAL | request.json is skipped by stage comparison. Other provenance may constrain a real run, but the comparator itself does not establish this identity. |
| Stage request script/hash and matching output worker hash change to an arbitrary successor | PASS_BITWISE_EQUAL | auto_tokens derives and admits custody pairs from compared requests. It does not enforce the driver's registered successor relation. |
| Result valid:true becomes1 or speed1.0 becomestrue | PASS_BITWISE_EQUAL | Python equality admits numerical/boolean type conflation. |
| JSON max_abs_change changes+0.0 to-0.0 | PASS_BITWISE_EQUAL | Mathematical equality here is weaker than byte identity; NPZ signed-zero is correctly detected. |

These probes establish comparator limits, not tampering in a real run. The common numerical array checks are strong; the unqualified all-output interpretation of PASS_BITWISE_EQUAL is too broad. New-only-file handling was already documented by the prior independent check. The additional probes and their exact saved reports make the other scope limits reviewable. An adoption owner must either constrain the accepted artifact schema and authenticate request custody separately, or require successor comparator checks. No comparator code is edited here.

TESTED: the new Z2 token file preserves its entire old declared list as a prefix and adds exactly16 entries, path/hash for each of8 driver SCRIPTS_UVT kinds. Each added pair was independently reconstructed from the pinned driver's SCRIPTS and SCRIPTS_UVT tables and the old GEO token chain. Actual base/reference/successor bytes match their hashes, and successor headers name the base. This verifies the explicit token addition. It does not close the comparator's additional auto_tokens behavior described above. Original UVT run records were read only as reports; original run directories remain unopened, so their PASS/FAIL labels are not independently revalidated.

TESTED: type-sensitive recursive leaf diff of each of the four requested R-PAIR members against its base matches the older A52 leaf list exactly. Both ROUTE_A members conform to A53. Both PICARD members fail A53: no admitted base route A, column_workers remains greater than1, and the C5H member still has ro1_workers=true. A53 explicitly amends A52.3 on these points. The immutable A53 excerpt records the text at review time. The inspected saved B0 records contain four nonempty planning reports,10 stages each, and12/13 output files; their recorded differences concern the older members. This review verifies those reports and file-byte pins, not an independent rerun of the old B0 classification algorithm. A53 successors need their own registered inputs and corresponding B0 evidence.

The final source review has peak RSS75218944bytes. The synthetic trees are deliberately small and contain no real targets. Direct run-byte verification and any end-to-end scientific behavior remain UNTESTED. No reviewed file was changed.

Cited files with SHA256 from bytes (the detailed evidence record additionally pins every inspected source and case report):
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_certs_gates_cx3/identity_specs_v002/REVIEW_RESULTS_V001.json` — `b4be4da90de617c2ae0aa7b2aa8863c4c7f3585367bb55db2da63851114136ea`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_certs_gates_cx3/identity_specs_v002/B0_RECORD_REVIEW_V001.json` — `d0c3a89496db936f059e5f8aeb168717aadcc5509ffa3b2c7fff3a202c116aac`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_certs_gates_cx3/identity_specs_v002/A53_READ_SNAPSHOT.txt` — `1d4e8a5238c28201f30b020fd8db809668999dd1fb8b587c4a659161b977265c`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_certs_gates_cx3/review_identity_specs_cx3v001.py` — `118df8a74999e58aee3834511ab916cc40fee41d92cfdf6f6fcecc92d55c3fba`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_certs_gates_cx3/review_identity_specs_cx3v002.py` — `8780dd0ac7d730fe9d9b0a3f24411d172cdd661c8dec7e891a95e1e35e7fe651`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0529_2026-10-18_codex3_laneB_crosslineage_review_certificates_and_comparator.md` — `5a44d4e5afa68b881b80532b80fdbe0e94e5d15bdb590f8eb1c13280374552a1`
- `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0530_2026-10-18_codex_all_A55_P128_r5_and_B0_ruling.md` — `4690c7ac94da89cfabd4b820bbed6a82e7c67d1c1e488a3f74d686795e6a3732`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v003/check/CHECK.md` — `2cf1c4404df705fa60a5014a4fbdf0a657ef4f7d80fb5d083db8fd7ca8584d06`
